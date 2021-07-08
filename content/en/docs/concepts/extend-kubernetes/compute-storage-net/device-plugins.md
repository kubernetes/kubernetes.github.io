---
reviewers:
title: Device Plugins
description: Use the Kubernetes device plugin framework to implement plugins for GPUs, NICs, FPGAs, InfiniBand, and similar resources that require vendor-specific setup.
content_type: concept
weight: 20
---

<!-- overview -->
{{< feature-state for_k8s_version="v1.10" state="beta" >}}

Kubernetes provides a [device plugin framework](https://github.com/kubernetes/community/blob/master/contributors/design-proposals/resource-management/device-plugin.md)
that you can use to advertise system hardware resources to the
{{< glossary_tooltip term_id="kubelet" >}}.

Instead of customizing the code for Kubernetes itself, vendors can implement a
device plugin that you deploy either manually or as a {{< glossary_tooltip term_id="daemonset" >}}.
The targeted devices include GPUs, high-performance NICs, FPGAs, InfiniBand adapters,
and other similar computing resources that may require vendor specific initialization
and setup.

<!-- body -->

## Device plugin registration

The kubelet exports a `Registration` gRPC service:

```gRPC
service Registration {
	rpc Register(RegisterRequest) returns (Empty) {}
}
```

A device plugin can register itself with the kubelet through this gRPC service.
During the registration, the device plugin needs to send:

  * The name of its Unix socket.
  * The Device Plugin API version against which it was built.
  * The `ResourceName` it wants to advertise. Here `ResourceName` needs to follow the
    [extended resource naming scheme](/docs/concepts/configuration/manage-resources-containers/#extended-resources)
    as `vendor-domain/resourcetype`.
    (For example, an NVIDIA GPU is advertised as `nvidia.com/gpu`.)

Following a successful registration, the device plugin sends the kubelet the
list of devices it manages, and the kubelet is then in charge of advertising those
resources to the API server as part of the kubelet node status update.
For example, after a device plugin registers `hardware-vendor.example/foo` with the kubelet
and reports two healthy devices on a node, the node status is updated
to advertise that the node has 2 "Foo" devices installed and available.

Then, users can request devices in a
{{< api-reference page="workload-resources/pod-v1" anchor="Container" >}}
specification as they request other types of resources, with the following limitations:

* Extended resources are only supported as integer resources and cannot be overcommitted.
* Devices cannot be shared among Containers.

Suppose a Kubernetes cluster is running a device plugin that advertises resource `hardware-vendor.example/foo`
on certain nodes. Here is an example of a pod requesting this resource to run a demo workload:

```yaml
---
apiVersion: v1
kind: Pod
metadata:
  name: demo-pod
spec:
  containers:
    - name: demo-container-1
      image: k8s.gcr.io/pause:2.0
      resources:
        limits:
          hardware-vendor.example/foo: 2
#
# This Pod needs 2 of the hardware-vendor.example/foo devices
# and can only schedule onto a Node that's able to satisfy
# that need.
#
# If the Node has more than 2 of those devices available, the
# remainder would be available for other Pods to use.
```

## Device plugin implementation

The general workflow of a device plugin includes the following steps:

* Initialization. During this phase, the device plugin performs vendor specific
  initialization and setup to make sure the devices are in a ready state.

* The plugin starts a gRPC service, with a Unix socket under host path
  `/var/lib/kubelet/device-plugins/`, that implements the following interfaces:

  ```gRPC
  service DevicePlugin {
        // GetDevicePluginOptions returns options to be communicated with Device Manager.
        rpc GetDevicePluginOptions(Empty) returns (DevicePluginOptions) {}

        // ListAndWatch returns a stream of List of Devices
        // Whenever a Device state change or a Device disappears, ListAndWatch
        // returns the new list
        rpc ListAndWatch(Empty) returns (stream ListAndWatchResponse) {}

        // Allocate is called during container creation so that the Device
        // Plugin can run device specific operations and instruct Kubelet
        // of the steps to make the Device available in the container
        rpc Allocate(AllocateRequest) returns (AllocateResponse) {}

        // GetPreferredAllocation returns a preferred set of devices to allocate
        // from a list of available ones. The resulting preferred allocation is not
        // guaranteed to be the allocation ultimately performed by the
        // devicemanager. It is only designed to help the devicemanager make a more
        // informed allocation decision when possible.
        rpc GetPreferredAllocation(PreferredAllocationRequest) returns (PreferredAllocationResponse) {}

        // PreStartContainer is called, if indicated by Device Plugin during registeration phase,
        // before each container start. Device plugin can run device specific operations
        // such as resetting the device before making devices available to the container.
        rpc PreStartContainer(PreStartContainerRequest) returns (PreStartContainerResponse) {}
  }
  ```

  {{< note >}}
  Plugins are not required to provide useful implementations for
  `GetPreferredAllocation()` or `PreStartContainer()`. Flags indicating which
  (if any) of these calls are available should be set in the `DevicePluginOptions`
  message sent back by a call to `GetDevicePluginOptions()`. The `kubelet` will
  always call `GetDevicePluginOptions()` to see which optional functions are
  available, before calling any of them directly.
  {{< /note >}}

* The plugin registers itself with the kubelet through the Unix socket at host
  path `/var/lib/kubelet/device-plugins/kubelet.sock`.

* After successfully registering itself, the device plugin runs in serving mode, during which it keeps
monitoring device health and reports back to the kubelet upon any device state changes.
It is also responsible for serving `Allocate` gRPC requests. During `Allocate`, the device plugin may
do device-specific preparation; for example, GPU cleanup or QRNG initialization.
If the operations succeed, the device plugin returns an `AllocateResponse` that contains container
runtime configurations for accessing the allocated devices. The kubelet passes this information
to the container runtime.

### Handling kubelet restarts

A device plugin is expected to detect kubelet restarts and re-register itself with the new
kubelet instance. In the current implementation, a new kubelet instance deletes all the existing Unix sockets
under `/var/lib/kubelet/device-plugins` when it starts. A device plugin can monitor the deletion
of its Unix socket and re-register itself upon such an event.

## Device plugin deployment

You can deploy a device plugin as a DaemonSet, as a package for your node's operating system,
or manually.

The canonical directory `/var/lib/kubelet/device-plugins` requires privileged access,
so a device plugin must run in a privileged security context.
If you're deploying a device plugin as a DaemonSet, `/var/lib/kubelet/device-plugins`
must be mounted as a {{< glossary_tooltip term_id="volume" >}}
in the plugin's
{{< api-reference page="workload-resources/pod-v1" anchor="PodSpec" >}}.

If you choose the DaemonSet approach you can rely on Kubernetes to: place the device plugin's
Pod onto Nodes, to restart the daemon Pod after failure, and to help automate upgrades.

## API compatibility

Kubernetes device plugin support is in beta. The API may change before stabilization,
in incompatible ways. As a project, Kubernetes recommends that device plugin developers:

* Watch for changes in future releases.
* Support multiple versions of the device plugin API for backward/forward compatibility.

If you enable the DevicePlugins feature and run device plugins on nodes that need to be upgraded to
a Kubernetes release with a newer device plugin API version, upgrade your device plugins
to support both versions before upgrading these nodes. Taking that approach will
ensure the continuous functioning of the device allocations during the upgrade.

## Monitoring Device Plugin Resources

{{< feature-state for_k8s_version="v1.15" state="beta" >}}

In order to monitor resources provided by device plugins, monitoring agents need to be able to
discover the set of devices that are in-use on the node and obtain metadata to describe which
container the metric should be associated with. [Prometheus](https://prometheus.io/) metrics
exposed by device monitoring agents should follow the
[Kubernetes Instrumentation Guidelines](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-instrumentation/instrumentation.md),
identifying containers using `pod`, `namespace`, and `container` prometheus labels.

The kubelet provides a gRPC service to enable discovery of in-use devices, and to provide metadata
for these devices:

```gRPC
// PodResourcesLister is a service provided by the kubelet that provides information about the
// node resources consumed by pods and containers on the node
service PodResourcesLister {
    rpc List(ListPodResourcesRequest) returns (ListPodResourcesResponse) {}
    rpc GetAllocatableResources(AllocatableResourcesRequest) returns (AllocatableResourcesResponse) {}
}
```

The `List` endpoint provides information on resources of running pods, with details such as the
id of exclusively allocated CPUs, device id as it was reported by device plugins and id of
the NUMA node where these devices are allocated.

```gRPC
// ListPodResourcesResponse is the response returned by List function
message ListPodResourcesResponse {
    repeated PodResources pod_resources = 1;
}

// PodResources contains information about the node resources assigned to a pod
message PodResources {
    string name = 1;
    string namespace = 2;
    repeated ContainerResources containers = 3;
}

// ContainerResources contains information about the resources assigned to a container
message ContainerResources {
    string name = 1;
    repeated ContainerDevices devices = 2;
    repeated int64 cpu_ids = 3;
}

// Topology describes hardware topology of the resource
message TopologyInfo {
        repeated NUMANode nodes = 1;
}

// NUMA representation of NUMA node
message NUMANode {
        int64 ID = 1;
}

// ContainerDevices contains information about the devices assigned to a container
message ContainerDevices {
    string resource_name = 1;
    repeated string device_ids = 2;
    TopologyInfo topology = 3;
}
```

GetAllocatableResources provides information on resources initially available on the worker node.
It provides more information than kubelet exports to APIServer.

```gRPC
// AllocatableResourcesResponses contains informations about all the devices known by the kubelet
message AllocatableResourcesResponse {
    repeated ContainerDevices devices = 1;
    repeated int64 cpu_ids = 2;
}

```

`ContainerDevices` do expose the topology information declaring to which NUMA cells the device is affine.
The NUMA cells are identified using a opaque integer ID, which value is consistent to what device
plugins report [when they register themselves to the kubelet](/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/#device-plugin-integration-with-the-topology-manager).


The gRPC service is served over a unix socket at `/var/lib/kubelet/pod-resources/kubelet.sock`.
Monitoring agents for device plugin resources can be deployed as a daemon, or as a DaemonSet.
The canonical directory `/var/lib/kubelet/pod-resources` requires privileged access, so monitoring
agents must run in a privileged security context.  If a device monitoring agent is running as a
DaemonSet, `/var/lib/kubelet/pod-resources` must be mounted as a
{{< glossary_tooltip term_id="volume" >}} in the device monitoring agent's
{{< api-reference page="workload-resources/pod-v1" anchor="PodSpec" >}}.

Support for the `PodResourcesLister service` requires `KubeletPodResources` [feature gate](/docs/reference/command-line-tools-reference/feature-gates/) to be enabled.
It is enabled by default starting with Kubernetes 1.15 and is v1 since Kubernetes 1.20.

## Device Plugin integration with the Topology Manager

{{< feature-state for_k8s_version="v1.18" state="beta" >}}

The Topology Manager is a Kubelet component that allows resources to be co-ordinated in a Topology aligned manner. In order to do this, the Device Plugin API was extended to include a `TopologyInfo` struct.


```gRPC
message TopologyInfo {
	repeated NUMANode nodes = 1;
}

message NUMANode {
    int64 ID = 1;
}
```
Device Plugins that wish to leverage the Topology Manager can send back a populated TopologyInfo struct as part of the device registration, along with the device IDs and the health of the device. The device manager will then use this information to consult with the Topology Manager and make resource assignment decisions.

`TopologyInfo` supports a `nodes` field that is either `nil` (the default) or a list of NUMA nodes. This lets the Device Plugin publish that can span NUMA nodes.

An example `TopologyInfo` struct populated for a device by a Device Plugin:

```
pluginapi.Device{ID: "25102017", Health: pluginapi.Healthy, Topology:&pluginapi.TopologyInfo{Nodes: []*pluginapi.NUMANode{&pluginapi.NUMANode{ID: 0,},}}}
```

## Device plugin examples {#examples}

Here are some examples of device plugin implementations:

* The [AMD GPU device plugin](https://github.com/RadeonOpenCompute/k8s-device-plugin)
* The [Intel device plugins](https://github.com/intel/intel-device-plugins-for-kubernetes) for Intel GPU, FPGA and QuickAssist devices
* The [KubeVirt device plugins](https://github.com/kubevirt/kubernetes-device-plugins) for hardware-assisted virtualization
* The [NVIDIA GPU device plugin](https://github.com/NVIDIA/k8s-device-plugin)
    * Requires [nvidia-docker](https://github.com/NVIDIA/nvidia-docker) 2.0, which allows you to run GPU-enabled Docker containers.
* The [NVIDIA GPU device plugin for Container-Optimized OS](https://github.com/GoogleCloudPlatform/container-engine-accelerators/tree/master/cmd/nvidia_gpu)
* The [RDMA device plugin](https://github.com/hustcat/k8s-rdma-device-plugin)
* The [Solarflare device plugin](https://github.com/vikaschoudhary16/sfc-device-plugin)
* The [SR-IOV Network device plugin](https://github.com/intel/sriov-network-device-plugin)
* The [Xilinx FPGA device plugins](https://github.com/Xilinx/FPGA_as_a_Service/tree/master/k8s-fpga-device-plugin) for Xilinx FPGA devices


## {{% heading "whatsnext" %}}


* Learn about [scheduling GPU resources](/docs/tasks/manage-gpus/scheduling-gpus/) using device plugins
* Learn about [advertising extended resources](/docs/tasks/administer-cluster/extended-resource-node/) on a node
* Read about using [hardware acceleration for TLS ingress](https://kubernetes.io/blog/2019/04/24/hardware-accelerated-ssl/tls-termination-in-ingress-controllers-using-kubernetes-device-plugins-and-runtimeclass/) with Kubernetes
* Learn about the [Topology Manager](/docs/tasks/administer-cluster/topology-manager/)
