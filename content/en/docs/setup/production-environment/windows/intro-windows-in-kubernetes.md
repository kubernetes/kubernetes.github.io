---
title: Intro to Windows support in Kubernetes
content_type: concept
weight: 65
reviewers:
- jayunit100
- jsturtevant
- marosset
- perithompson
---

<!-- overview -->

Windows applications constitute a large portion of the services and
applications that run in many organizations.
[Windows containers](https://aka.ms/windowscontainers) provide a modern way to
encapsulate processes and package dependencies, making it easier to use DevOps
practices and follow cloud native patterns for Windows applications.
Kubernetes has become the defacto standard container orchestrator, and the
release of Kubernetes 1.14 includes production support for scheduling Windows
containers on Windows nodes in a Kubernetes cluster, enabling a vast ecosystem
of Windows applications to leverage the power of Kubernetes. Organizations
with investments in Windows-based applications and Linux-based applications
don't have to look for separate orchestrators to manage their workloads,
leading to increased operational efficiencies across their deployments,
regardless of operating system.

<!-- body -->

## Windows containers in Kubernetes

To enable the orchestration of Windows containers in Kubernetes, include
Windows nodes in your existing Linux cluster. Scheduling Windows containers in
{{< glossary_tooltip text="Pods" term_id="pod" >}} on Kubernetes is similar to
scheduling Linux-based containers.

In order to run Windows containers, your Kubernetes cluster must include
multiple operating systems, with control plane nodes running Linux and workers
running either Windows or Linux depending on your workload needs. Windows
Server 2019 is the only Windows operating system supported, enabling
[Kubernetes Node](https://github.com/kubernetes/community/blob/master/contributors/design-proposals/architecture/architecture.md#the-kubernetes-node)
on Windows (including kubelet,
[container runtime](https://docs.microsoft.com/en-us/virtualization/windowscontainers/deploy-containers/containerd),
and kube-proxy). For a detailed explanation of Windows distribution channels
see the [Microsoft documentation](https://docs.microsoft.com/en-us/windows-server/get-started-19/servicing-channels-19).

The Kubernetes control plane, including the
[master components](/docs/concepts/overview/components/),
continues to run on Linux.
There are no plans to have a Windows-only Kubernetes cluster.

In this document, when we talk about Windows containers we mean Windows
containers with process isolation. Windows containers with
[Hyper-V isolation](https://docs.microsoft.com/en-us/virtualization/windowscontainers/manage-containers/hyperv-container)
is planned for a future release.

## Supported Functionality and Limitations

### Supported Functionality

#### Windows OS Version Support

Refer to the following table for Windows operating system support in
Kubernetes. A single heterogeneous Kubernetes cluster can have both Windows
and Linux worker nodes. Windows containers have to be scheduled on Windows
nodes and Linux containers on Linux nodes.

| Kubernetes version | Windows Server LTSC releases | Windows Server SAC releases |
| --- | --- | --- | --- |
| *Kubernetes v1.19* | Windows Server 2019 | Windows Server ver 1909, Windows Server ver 2004 |
| *Kubernetes v1.20* | Windows Server 2019 | Windows Server ver 1909, Windows Server ver 2004 |
| *Kubernetes v1.21* | Windows Server 2019 | Windows Server ver 2004, Windows Server ver 20H2 |


Information on the different Windows Server servicing channels including their
support models can be found at
[Windows Server servicing channels](https://docs.microsoft.com/en-us/windows-server/get-started-19/servicing-channels-19).

We don't expect all Windows customers to update the operating system for their
apps frequently. Upgrading your applications is what dictates and necessitates
upgrading or introducing new nodes to the cluster. For the customers that
chose to upgrade their operating system for containers running on Kubernetes,
we will offer guidance and step-by-step instructions when we add support for a
new operating system version. This guidance will include recommended upgrade
procedures for upgrading user applications together with cluster nodes.
Windows nodes adhere to Kubernetes
[version-skew policy](/docs/setup/release/version-skew-policy/) (node to control plane
versioning) the same way as Linux nodes do today.


The Windows Server Host Operating System is subject to the
[Windows Server ](https://www.microsoft.com/en-us/cloud-platform/windows-server-pricing)
licensing. The Windows Container images are subject to the
[Supplemental License Terms for Windows containers](https://docs.microsoft.com/en-us/virtualization/windowscontainers/images-eula).

Windows containers with process isolation have strict compatibility rules,
[where the host OS version must match the container base image OS version](https://docs.microsoft.com/en-us/virtualization/windowscontainers/deploy-containers/version-compatibility).
Once we support Windows containers with Hyper-V isolation in Kubernetes, the
limitation and compatibility rules will change.

#### Pause Image

Microsoft maintains a Windows pause infrastructure container at
`mcr.microsoft.com/oss/kubernetes/pause:3.4.1`.
Kubernetes maintains a multi-architecture image `k8s.gcr.io/pause:3.5` that
supports Linux as well as Windows.

#### Compute

From an API and kubectl perspective, Windows containers behave in much the
same way as Linux-based containers. However, there are some notable
differences in key functionality which are outlined in the
[limitation section](#limitations).

Key Kubernetes elements work the same way in Windows as they do in Linux. In
this section, we talk about some of the key workload enablers and how they map
to Windows.

* [Pods](/docs/concepts/workloads/pods/)

  A Pod is the basic building block of Kubernetes–the smallest and simplest
  unit in the Kubernetes object model that you create or deploy. You may not
  deploy Windows and Linux containers in the same Pod. All containers in a Pod
  are scheduled onto a single Node where each Node represents a specific
  platform and architecture. The following Pod capabilities, properties and
  events are supported with Windows containers:

  * Single or multiple containers per Pod with process isolation and volume sharing
  * Pod status fields
  * Readiness and Liveness probes
  * postStart & preStop container lifecycle events
  * ConfigMap, Secrets: as environment variables or volumes
  * EmptyDir
  * Named pipe host mounts
  * Resource limits
* [Controllers](/docs/concepts/workloads/controllers/)

  Kubernetes controllers handle the desired state of Pods. The following
  workload controllers are supported with Windows containers:

  * ReplicaSet
  * ReplicationController
  * Deployments
  * StatefulSets
  * DaemonSet
  * Job
  * CronJob

* [Services](/docs/concepts/services-networking/service/)

  A Kubernetes Service is an abstraction which defines a logical set of Pods
  and a policy by which to access them - sometimes called a micro-service. You
  can use services for cross-operating system connectivity. In Windows, services
  can utilize the following types, properties and capabilities:

  * Service Environment variables
  * NodePort
  * ClusterIP
  * LoadBalancer
  * ExternalName
  * Headless services

Pods, Controllers and Services are critical elements to managing Windows
workloads on Kubernetes. However, on their own they are not enough to enable
the proper lifecycle management of Windows workloads in a dynamic cloud native
environment. We added support for the following features:

* Pod and container metrics
* Horizontal Pod Autoscaler support
* kubectl Exec
* Resource Quotas
* Scheduler preemption

#### Container Runtime

##### Docker EE

{{< feature-state for_k8s_version="v1.14" state="stable" >}}

Docker EE-basic 19.03+ is the recommended container runtime for all Windows
Server versions. This works with the dockershim code included in the kubelet.

##### CRI-ContainerD

{{< feature-state for_k8s_version="v1.20" state="stable" >}}

{{< glossary_tooltip term_id="containerd" text="ContainerD" >}} 1.4.0+ can
also be used as the container runtime for Windows Kubernetes nodes.

Learn how to
[install ContainerD on a Windows](/docs/setup/production-environment/container-runtimes/#install-containerd).

#### Persistent Storage

Kubernetes [volumes](/docs/concepts/storage/volumes/) enable complex
applications, with data persistence and Pod volume sharing requirements, to be
deployed on Kubernetes. Management of persistent volumes associated with a
specific storage back-end or protocol includes actions such as:
provisioning/de-provisioning/resizing of volumes, attaching/detaching a volume
to/from a Kubernetes node and mounting/dismounting a volume to/from individual
containers in a pod that needs to persist data. The code implementing these
volume management actions for a specific storage back-end or protocol is
shipped in the form of a Kubernetes volume
[plugin](/docs/concepts/storage/volumes/#types-of-volumes). The following
broad classes of Kubernetes volume plugins are supported on Windows:

##### In-tree Volume Plugins

Code associated with in-tree volume plugins ship as part of the core
Kubernetes code base. Deployment of in-tree volume plugins do not require
installation of additional scripts or deployment of separate containerized
plugin components. These plugins can handle: provisioning/de-provisioning and
resizing of volumes in the storage backend, attaching/detaching of volumes
to/from a Kubernetes node and mounting/dismounting a volume to/from individual
containers in a pod. The following in-tree plugins support Windows nodes:

* [awsElasticBlockStore](/docs/concepts/storage/volumes/#awselasticblockstore)
* [azureDisk](/docs/concepts/storage/volumes/#azuredisk)
* [azureFile](/docs/concepts/storage/volumes/#azurefile)
* [gcePersistentDisk](/docs/concepts/storage/volumes/#gcepersistentdisk)
* [vsphereVolume](/docs/concepts/storage/volumes/#vspherevolume)

##### FlexVolume Plugins

Code associated with [FlexVolume](/docs/concepts/storage/volumes/#flexVolume)
plugins ship as out-of-tree scripts or binaries that need to be deployed
directly on the host. FlexVolume plugins handle attaching/detaching of volumes
to/from a Kubernetes node and mounting/dismounting a volume to/from individual
containers in a pod. Provisioning/De-provisioning of persistent volumes
associated with FlexVolume plugins may be handled through an external
provisioner that is typically separate from the FlexVolume plugins. The
following FlexVolume
[plugins](https://github.com/Microsoft/K8s-Storage-Plugins/tree/master/flexvolume/windows),
deployed as powershell scripts on the host, support Windows nodes:

* [SMB](https://github.com/microsoft/K8s-Storage-Plugins/tree/master/flexvolume/windows/plugins/microsoft.com~smb.cmd)
* [iSCSI](https://github.com/microsoft/K8s-Storage-Plugins/tree/master/flexvolume/windows/plugins/microsoft.com~iscsi.cmd)

##### CSI Plugins

{{< feature-state for_k8s_version="v1.19" state="beta" >}}

Code associated with {{< glossary_tooltip text="CSI" term_id="csi" >}} plugins
ship as out-of-tree scripts and binaries that are typically distributed as
container images and deployed using standard Kubernetes constructs like
DaemonSets and StatefulSets. CSI plugins handle a wide range of volume
management actions in Kubernetes: provisioning/de-provisioning/resizing of
volumes, attaching/detaching of volumes to/from a Kubernetes node and
mounting/dismounting a volume to/from individual containers in a pod,
backup/restore of persistent data using snapshots and cloning. CSI plugins
typically consist of node plugins (that run on each node as a DaemonSet) and
controller plugins.

CSI node plugins (especially those associated with persistent volumes exposed
as either block devices or over a shared file-system) need to perform various
privileged operations like scanning of disk devices, mounting of file systems,
etc. These operations differ for each host operating system. For Linux worker
nodes, containerized CSI node plugins are typically deployed as privileged
containers. For Windows worker nodes, privileged operations for containerized
CSI node plugins is supported using
[csi-proxy](https://github.com/kubernetes-csi/csi-proxy), a community-managed,
stand-alone binary that needs to be pre-installed on each Windows node. Please
refer to the deployment guide of the CSI plugin you wish to deploy for further
details.

#### Networking

Networking for Windows containers is exposed through
[CNI plugins](/docs/concepts/extend-kubernetes/compute-storage-net/network-plugins/).
Windows containers function similarly to virtual machines in regards to
networking. Each container has a virtual network adapter (vNIC) which is
connected to a Hyper-V virtual switch (vSwitch). The Host Networking Service
(HNS) and the Host Compute Service (HCS) work together to create containers
and attach container vNICs to networks. HCS is responsible for the management
of containers whereas HNS is responsible for the management of networking
resources such as:

* Virtual networks (including creation of vSwitches)
* Endpoints / vNICs
* Namespaces
* Policies (Packet encapsulations, Load-balancing rules, ACLs, NAT'ing rules, etc.)

The following service spec types are supported:

* NodePort
* ClusterIP
* LoadBalancer
* ExternalName

##### Network modes

Windows supports five different networking drivers/modes: L2bridge, L2tunnel,
Overlay, Transparent, and NAT. In a heterogeneous cluster with Windows and
Linux worker nodes, you need to select a networking solution that is
compatible on both Windows and Linux. The following out-of-tree plugins are
supported on Windows, with recommendations on when to use each CNI:

<table>
 <thead>
  <tr>
   <th>Network Driver</th>
   <th>Description</th>
   <th>Container Packet Modifications</th>
   <th>Network Plugins</th>
   <th>Network Plugin Characteristics</th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>L2bridge</td>
   <td>Containers are attached to an external vSwitch. Containers are attached
      to the underlay network, although the physical network doesn't need to learn
      the container. MACs because they are rewritten on ingress/egress.
   </td>
   <td>
      MAC is rewritten to host MAC, IP may be rewritten to host IP using HNS
      OutboundNAT policy.
   </td>
   <td>
    <a href="https://github.com/containernetworking/plugins/tree/master/plugins/main/windows/win-bridge">win-bridge<a>,
    <a href="https://github.com/Azure/azure-container-networking/blob/master/docs/cni.md">Azure-CNI</a>,
    Flannel host-gateway uses win-bridge
   </td>
   <td>
    win-bridge uses L2bridge network mode,
    connects containers to the underlay of hosts, offering best performance.
    Requires user-defined routes (UDR) for inter-node connectivity.
   </td>
  </tr>
  <tr>
   <td>L2Tunnel</td>
   <td>
    This is a special case of l2bridge, but only used on Azure. All packets
    are sent to the virtualization host where SDN policy is applied.
   </td>
   <td>
    MAC rewritten, IP visible on the underlay network
   </td>
   <td>
    <a href="https://github.com/Azure/azure-container-networking/blob/master/docs/cni.md">Azure-CNI</a>
   </td>
   <td>
      Azure-CNI allows integration of containers with Azure vNET, and allows them
      to leverage the set of capabilities that
      <a href="https://azure.microsoft.com/en-us/services/virtual-network/">Azure Virtual Network</a>
      provides. For example, securely connect to Azure services or use Azure NSGs.
      See <a href="https://docs.microsoft.com/en-us/azure/aks/concepts-network#azure-cni-advanced-networking">azure-cni</a>
      for some examples.
   </td>
  </tr>
  <tr>
   <td>Overlay (Overlay networking for Windows in Kubernetes is in <B>Alpha</B> stage)</td>
   <td>
    Containers are given a vNIC connected to an external vSwitch. Each overlay
    network gets its own IP subnet, defined by a custom IP prefix.The overlay
    network driver uses VXLAN encapsulation.
   </td>
   <td>
    Encapsulated with an outer header.
   </td>
   <td>
    <a href="https://github.com/containernetworking/plugins/tree/master/plugins/main/windows/win-overlay">Win-overlay</a>,
    Flannel VXLAN (uses win-overlay)
   </td>
   <td>
    win-overlay should be used when virtual container networks are desired to
    be isolated from underlay of hosts (e.g. for security reasons). Allows for IPs
    to be re-used for different overlay networks (which have different VNID tags)
    if you are restricted on IPs in your datacenter.  This option requires
    <a href="https://support.microsoft.com/help/4489899">KB4489899</a> on Windows Server
    2019.
   </td>
  </tr>
  <tr>
   <td>
    Transparent (special use case for <a href="https://github.com/openvswitch/ovn-kubernetes">ovn-kubernetes</a>)
   </td>
   <td>
    Requires an external vSwitch. Containers are attached to an external
    vSwitch which enables intra-pod communication via logical networks (logical
    switches and routers).
   </td>
   <td>
    Packet is encapsulated either via
    <a href="https://datatracker.ietf.org/doc/draft-gross-geneve/">GENEVE</a>,
    <a href="https://datatracker.ietf.org/doc/draft-davie-stt/">STT</a> tunneling to reach
    pods which are not on the same host.<br/> Packets are forwarded or dropped
    via the tunnel metadata information supplied by the ovn network controller.
    <br/>
    NAT is done for north-south communication.
   </td>
   <td>
    <a href="https://github.com/openvswitch/ovn-kubernetes">ovn-kubernetes</a>
   </td>
   <td>
     Deploy via <a href="https://github.com/openvswitch/ovn-kubernetes/tree/master/contrib">Ansible</a>.
     Distributed ACLs can be applied via Kubernetes policies. IPAM support.
     Load-balancing can be achieved without kube-proxy. NATing is done without
     using iptables/netsh.
   </td>
  </tr>
  <tr>
   <td>NAT (<B>not used in Kubernetes</B>)</td>
   <td>
    Containers are given a vNIC connected to an internal vSwitch. DNS/DHCP is
    provided using an internal component called
    <a href="https://blogs.technet.microsoft.com/virtualization/2016/05/25/windows-nat-winnat-capabilities-and-limitations">WinNAT</a>.
   </td>
   <td>
    MAC and IP is rewritten to host MAC/IP.
   </td>
   <td>
    <a href="https://github.com/Microsoft/windows-container-networking/tree/master/plugins/nat">nat</a>
   </td>
   <td>
    Included here for completeness
   </td>
  </tr>
 </tbody>
</table>

As outlined above, the [Flannel](https://github.com/coreos/flannel) CNI
[meta plugin](https://github.com/containernetworking/plugins/tree/master/plugins/meta/flannel)
is also supported on
[Windows](https://github.com/containernetworking/plugins/tree/master/plugins/meta/flannel#windows-support-experimental)
via the [VXLAN network backend](https://github.com/coreos/flannel/blob/master/Documentation/backends.md#vxlan)
(**alpha support** ; delegates to win-overlay) and
[host-gateway network backend](https://github.com/coreos/flannel/blob/master/Documentation/backends.md#host-gw)
(stable support; delegates to win-bridge). This plugin supports delegating to
one of the reference CNI plugins (win-overlay, win-bridge), to work in
conjunction with Flannel daemon on Windows (Flanneld) for automatic node
subnet lease assignment and HNS network creation. This plugin reads in its own
configuration file (cni.conf), and aggregates it with the environment
variables from the FlannelD generated subnet.env file. It then delegates to
one of the reference CNI plugins for network plumbing, and sends the correct
configuration containing the node-assigned subnet to the IPAM plugin (e.g.
host-local).

For the node, pod, and service objects, the following network flows are
supported for TCP/UDP traffic:

* Pod -> Pod (IP)
* Pod -> Pod (Name)
* Pod -> Service (Cluster IP)
* Pod -> Service (PQDN, but only if there are no ".")
* Pod -> Service (FQDN)
* Pod -> External (IP)
* Pod -> External (DNS)
* Node -> Pod
* Pod -> Node

##### IP address management (IPAM) {#ipam}

The following IPAM options are supported on Windows:

* [Host-local](https://github.com/containernetworking/plugins/tree/master/plugins/ipam/host-local)
* HNS IPAM (Inbox platform IPAM, this is a fallback when no IPAM is set)
* [Azure-vnet-ipam](https://github.com/Azure/azure-container-networking/blob/master/docs/ipam.md) (for azure-cni only)

##### Load balancing and Services

On Windows, you can use the following settings to configure Services and load
balancing behavior:

{{< table caption="Windows Service Settings" >}}

<table>
 <thead>
  <tr>
   <th>Feature</th>
   <th>Description</th>
   <th>Supported Kubernetes version</th>
   <th>Supported Windows OS build</th>
   <th>How to enable</th>
  </tr>
 <thead>
 <tbody>
  <tr>
   <td>Session affinity</td>
   <td>
    Ensures that connections from a particular client are passed to the same
    Pod each time.
   </td>
   <td>v1.20+</td>
   <td>
    <a href="https://blogs.windows.com/windowsexperience/2020/01/28/announcing-windows-server-vnext-insider-preview-build-19551/">Windows Server vNext Insider Preview Build 19551</a> (or higher)
   </td>
   <td>
    Set <code>service.spec.sessionAffinity</code> to "ClientIP"
   </td>
  </tr>
  <tr>
   <td>Direct Server Return (DSR) </td>
   <td>
    Load balancing mode where the IP address fixups and the LBNAT occurs at
    the container vSwitch port directly; service traffic arrives with the source
    IP set as the originating pod IP.
   </td>
   <td>v1.20+</td>
   <td>
    Windows Server 2019
   </td>
   <td>
    Set the following flags in kube-proxy:
    <code>--feature-gates="WinDSR=true" --enable-dsr=true</code>
   </td>
  </tr>
  <tr>
   <td>Preserve-Destination</td>
   <td>
    Skips DNAT of service traffic, thereby preserving the virtual IP of the target
    service in packets reaching the backend Pod. Also disables node-node forwarding.
   </td>
   <td>v1.20+</td>
   <td>Windows Server, version 1903 (or higher)</td>
   <td>
    Set <code>"preserve-destination": "true"</code> in service annotations
    and enable DSR in kube-proxy.
   </td>
  </tr>
  <tr>
   <td>IPv4/IPv6 dual-stack networking</td>
   <td>
    Native IPv4-to-IPv4 in parallel with IPv6-to-IPv6 communications to, from,
    and within a cluster
   </td>
   <td>v1.19+</td>
   <td>Windows Server, version 2004 (or higher)</td>
   <td>
    See <a href="#ipv4ipv6-dual-stack">IPv4/IPv6 dual-stack</a>
   </td>
  </tr>
  <tr>
   <td>Client IP preservation</td>
   <td>
    Ensures that source IP of incoming ingress traffic gets preserved. Also
    disables node-node forwarding.
   </td>
   <td>v1.20+</td>
   <td>Windows Server, version 2019 (or higher)</td>
   <td>
    Set <code>service.spec.externalTrafficPolicy</code> to "Local" and enable
    DSR in kube-proxy.
   </td>
  </tr>
 </tbody>
</table>

{{< /table >}}

#### IPv4/IPv6 dual-stack

You can enable IPv4/IPv6 dual-stack networking for `l2bridge` networks using
the `IPv6DualStack` [feature gate](/docs/reference/command-line-tools-reference/feature-gates/). See
[enable IPv4/IPv6 dual stack](/docs/concepts/services-networking/dual-stack#enable-ipv4ipv6-dual-stack)
for more details.

On Windows, using IPv6 with Kubernetes require Windows Server, version 2004
(kernel version 10.0.19041.610) or later.

Overlay (VXLAN) networks on Windows do not support dual-stack networking today.

### Limitations

Windows is only supported as a worker node in the Kubernetes architecture and
component matrix. This means that a Kubernetes cluster must always include
Linux master nodes, zero or more Linux worker nodes, and zero or more Windows
worker nodes.

#### Resource Handling

Linux cgroups are used as a pod boundary for resource controls in Linux.
Containers are created within that boundary for network, process and file
system isolation. The cgroups APIs can be used to gather cpu/io/memory stats.
In contrast, Windows uses a Job object per container with a system namespace
filter to contain all processes in a container and provide logical isolation
from the host. There is no way to run a Windows container without the
namespace filtering in place. This means that system privileges cannot be
asserted in the context of the host, and thus privileged containers are not
available on Windows. Containers cannot assume an identity from the host
because the Security Account Manager (SAM) is separate.

#### Resource Reservations

##### Memory Reservations

Windows does not have an out-of-memory process killer as Linux does. Windows
always treats all user-mode memory allocations as virtual, and pagefiles are
mandatory. The net effect is that Windows won't reach out of memory conditions
the same way Linux does, and processes page to disk instead of being subject
to out of memory (OOM) termination. If memory is over-provisioned and all
physical memory is exhausted, then paging can slow down performance.

Keeping memory usage within reasonable bounds is possible using the kubelet
parameters `--kubelet-reserve` and/or `--system-reserve` to account for memory
usage on the node (outside of containers). This reduces
[NodeAllocatable](/docs/tasks/administer-cluster/reserve-compute-resources/#node-allocatable). 

As you deploy workloads, use resource limits (must set only limits or limits
must equal requests) on containers. This also subtracts from NodeAllocatable
and prevents the scheduler from adding more pods once a node is full.

A best practice to avoid over-provisioning is to configure the kubelet with a
system reserved memory of at least 2GB to account for Windows, Docker, and
Kubernetes processes.

##### CPU Reservations

To account for Windows, Docker and other Kubernetes host processes it is
recommended to reserve a percentage of CPU so they are able to respond to
events. This value needs to be scaled based on the number of CPU cores
available on the Windows node.To determine this percentage a user should
identify the maximum pod density for each of their nodes and monitor the CPU
usage of the system services choosing a value that meets their workload needs.

Keeping CPU usage within reasonable bounds is possible using the kubelet
parameters `--kubelet-reserve` and/or `--system-reserve` to account for CPU
usage on the node (outside of containers). This reduces
[NodeAllocatable](/docs/tasks/administer-cluster/reserve-compute-resources/#node-allocatable). 

#### Feature Restrictions

* TerminationGracePeriod: not implemented
* Single file mapping: to be implemented with CRI-ContainerD
* Termination message: to be implemented with CRI-ContainerD
* Privileged Containers: not currently supported in Windows containers
* HugePages: not currently supported in Windows containers
* The existing node problem detector is Linux-only and requires privileged
  containers. In general, we don't expect this to be used on Windows because
  privileged containers are not supported
* Not all features of shared namespaces are supported (see API section for
  more details)

#### Difference in behavior of flags when compared to Linux

The behavior of the following kubelet flags is different on Windows nodes as described below:

* `--kubelet-reserve`, `--system-reserve` , and `--eviction-hard` flags update
  Node Allocatable

* Eviction by using `--enforce-node-allocable` is not implemented.

* Eviction by using `--eviction-hard` and `--eviction-soft` are not implemented.

* `MemoryPressure` Condition is not implemented.

* There are no OOM eviction actions taken by the kubelet.

* Kubelet running on the windows node does not have memory restrictions.
  `--kubelet-reserve` and `--system-reserve` do not set limits on kubelet or
  processes running on the host. This means kubelet or a process on the host
  could cause memory resource starvation outside the node-allocatable and
  scheduler

* An additional flag to set the priority of the kubelet process is available
  on the Windows nodes called `--windows-priorityclass`. This flag allows
  kubelet process to get more CPU time slices when compared to other processes
  running on the Windows host. More information on the allowable values and
  their meaning is available at
  [Windows Priority Classes](https://docs.microsoft.com/en-us/windows/win32/procthread/scheduling-priorities#priority-class).
  In order for kubelet to always have enough CPU cycles it is recommended to set
  this flag to `ABOVE_NORMAL_PRIORITY_CLASS` and above.

#### Storage

Windows has a layered filesystem driver to mount container layers and create a
copy filesystem based on NTFS. All file paths in the container are resolved
only within the context of that container.

* With Docker Volume mounts can only target a directory in the container, and
  not an individual file. This limitation does not exist with CRI-containerD.

* Volume mounts cannot project files or directories back to the host
  filesystem

* Read-only filesystems are not supported because write access is always
  required for the Windows registry and SAM database. However, read-only
  volumes are supported

* Volume user-masks and permissions are not available. Because the SAM is not
  shared between the host & container, there's no mapping between them. All
  permissions are resolved within the context of the container

As a result, the following storage functionality is not supported on Windows nodes:

* Volume subpath mounts. Only the entire volume can be mounted in a Windows container.
* Subpath volume mounting for Secrets
* Host mount projection
* DefaultMode (due to UID/GID dependency)
* Read-only root filesystem. Mapped volumes still support readOnly
* Block device mapping
* Memory as the storage medium
* File system features like uui/guid, per-user Linux filesystem permissions
* NFS based storage/volume support
* Expanding the mounted volume (resizefs)

#### Networking {#networking-limitations}

Windows Container Networking differs in some important ways from Linux
networking. The [Microsoft documentation for Windows Container Networking](https://docs.microsoft.com/en-us/virtualization/windowscontainers/container-networking/architecture)
contains additional details and background.

The Windows host networking service and virtual switch implement namespacing
and can create virtual NICs as needed for a pod or container. However, many
configurations such as DNS, routes, and metrics are stored in the Windows
registry database rather than /etc/... files as they are on Linux. The Windows
registry for the container is separate from that of the host, so concepts like
mapping /etc/resolv.conf from the host into a container don't have the same
effect they would on Linux. These must be configured using Windows APIs run in
the context of that container. Therefore CNI implementations need to call the
HNS instead of relying on file mappings to pass network details into the pod
or container.

The following networking functionality is not supported on Windows nodes

* Host networking mode is not available for Windows pods.

* Local NodePort access from the node itself fails (works for other nodes or
  external clients).

* Accessing service VIPs from nodes will be available with a future release of
  Windows Server.

* A single service can only support up to 64 backend pods / unique destination IPs.

* Overlay networking support in kube-proxy is a beta feature. In addition, it
  requires [KB4482887](https://support.microsoft.com/en-us/help/4482887/windows-10-update-kb4482887)
  to be installed on Windows Server 2019.

* Local Traffic Policy in non-DSR mode.

* Windows containers connected to overlay networks do not support
  communicating over the IPv6 stack. There is outstanding Windows platform
  work required to enable this network driver to consume IPv6 addresses and
  subsequent Kubernetes work in kubelet, kube-proxy, and CNI plugins.

* Outbound communication using the ICMP protocol via the win-overlay,
  win-bridge, and Azure-CNI plugin. Specifically, the Windows data plane
  ([VFP](https://www.microsoft.com/en-us/research/project/azure-virtual-filtering-platform/))
  doesn't support ICMP packet transpositions. This means:

  * ICMP packets directed to destinations within the same network (e.g. pod to
    pod communication via ping) work as expected and without any limitations

  * TCP/UDP packets work as expected and without any limitations

  * ICMP packets directed to pass through a remote network (e.g. pod to
    external internet communication via ping) cannot be transposed and thus
    will not be routed back to their source

  * Since TCP/UDP packets can still be transposed, one can substitute
    `ping <destination>` with `curl <destination>` to be able to debug connectivity
    to the outside world.

These features were added in Kubernetes v1.15:

* `kubectl port-forward`

##### CNI Plugins

* Windows reference network plugins `win-bridge` and `win-overlay` do not
  currently implement [CNI spec](https://github.com/containernetworking/cni/blob/master/SPEC.md)
  v0.4.0 due to missing "CHECK" implementation.

* The Flannel VXLAN CNI has the following limitations on Windows:

  1. Node-pod connectivity isn't possible by design. It's only possible for
     local pods with Flannel v0.12.0 (or higher).

  1. We are restricted to using VNI 4096 and UDP port 4789. The VNI limitation
     is being worked on and will be overcome in a future release (open-source
     flannel changes). See the official
     [Flannel VXLAN](https://github.com/coreos/flannel/blob/master/Documentation/backends.md#vxlan)
     backend docs for more details on these parameters.

##### DNS {#dns-limitations}

* ClusterFirstWithHostNet is not supported for DNS. Windows treats all names
  with a '.' as a FQDN and skips PQDN resolution

* On Linux, you have a DNS suffix list, which is used when trying to resolve
  PQDNs. On Windows, we only have 1 DNS suffix, which is the DNS suffix
  associated with that pod's namespace (mydns.svc.cluster.local for example).
  Windows can resolve FQDNs and services or names resolvable with only that
  suffix. For example, a pod spawned in the default namespace, will have the DNS
  suffix `default.svc.cluster.local`. On a Windows pod, you can resolve both
  `kubernetes.default.svc.cluster.local` and `kubernetes`, but not the
  in-betweens, like `kubernetes.default` or `kubernetes.default.svc`.

* On Windows, there are multiple DNS resolvers that can be used. As these come
  with slightly different behaviors, using the `Resolve-DNSName` utility for
  name query resolutions is recommended.

##### IPv6

Kubernetes on Windows does not support single-stack "IPv6-only" networking.
However,dual-stack IPv4/IPv6 networking for pods and nodes with single-family
services is supported.
See [IPv4/IPv6 dual-stack networking](#ipv4ipv6-dual-stack) for more details.

##### Session affinity

Setting the maximum session sticky time for Windows services using
`service.spec.sessionAffinityConfig.clientIP.timeoutSeconds` is not supported.

##### Security

Secrets are written in clear text on the node's volume (as compared to
tmpfs/in-memory on linux). This means customers have to do two things:

1. Use file ACLs to secure the secrets file location
1. Use volume-level encryption using
   [BitLocker](https://docs.microsoft.com/en-us/windows/security/information-protection/bitlocker/bitlocker-how-to-deploy-on-windows-server)

[RunAsUsername](/docs/tasks/configure-pod-container/configure-runasusername)
can be specified for Windows Pod's or Container's to execute the Container
processes as a node-default user. This is roughly equivalent to
[RunAsUser](/docs/concepts/policy/pod-security-policy/#users-and-groups).

Linux specific pod security context privileges such as SELinux, AppArmor,
Seccomp, Capabilities (POSIX Capabilities), and others are not supported.

In addition, as mentioned already, privileged containers are not supported on
Windows.

#### API

There are no differences in how most of the Kubernetes APIs work for Windows.
The subtleties around what's different come down to differences in the OS and
container runtime. In certain situations, some properties on workload APIs
such as Pod or Container were designed with an assumption that they are
implemented on Linux, failing to run on Windows.

At a high level, these OS concepts are different:

* Identity - Linux uses userID (UID) and groupID (GID) which are represented
  as integer types. User and group names are not canonical - they are an alias
  in `/etc/groups` or `/etc/passwd` back to UID+GID. Windows uses a larger
  binary security identifier (SID) which is stored in the Windows Security
  Access Manager (SAM) database. This database is not shared between the host
  and containers, or between containers.

* File permissions - Windows uses an access control list based on SIDs, rather
  than a bitmask of permissions and UID+GID

* File paths - convention on Windows is to use `\` instead of `/`. The Go IO
  libraries accept both types of file path separators. However, when you're
  setting a path or command line that's interpreted inside a container, `\` may
  be needed.

* Signals - Windows interactive apps handle termination differently, and can
  implement one or more of these:

  * A UI thread handles well-defined messages including `WM_CLOSE`

  * Console apps handle ctrl-c or ctrl-break using a Control Handler

  * Services register a Service Control Handler function that can accept
    `SERVICE_CONTROL_STOP` control codes

Exit Codes follow the same convention where 0 is success, nonzero is failure.
The specific error codes may differ across Windows and Linux. However, exit
codes passed from the Kubernetes components (kubelet, kube-proxy) are
unchanged.

##### V1.Container

* V1.Container.ResourceRequirements.limits.cpu and
  V1.Container.ResourceRequirements.limits.memory - Windows doesn't use hard
  limits for CPU allocations. Instead, a share system is used. The existing
  fields based on millicores are scaled into relative shares that are followed
  by the Windows scheduler.
  See [kuberuntime/helpers_windows.go](https://github.com/kubernetes/kubernetes/blob/master/pkg/kubelet/kuberuntime/helpers_windows.go),
  and [resource controls in Microsoft docs](https://docs.microsoft.com/en-us/virtualization/windowscontainers/manage-containers/resource-controls)

  * Huge pages are not implemented in the Windows container runtime, and are
    not available. They require
    [asserting a user privilege](https://docs.microsoft.com/en-us/windows/desktop/Memory/large-page-support)
    that's not configurable for containers.

* V1.Container.ResourceRequirements.requests.cpu and
  V1.Container.ResourceRequirements.requests.memory - Requests are subtracted
  from node available resources, so they can be used to avoid overprovisioning a
  node. However, they cannot be used to guarantee resources in an
  overprovisioned node. They should be applied to all containers as a best
  practice if the operator wants to avoid overprovisioning entirely.

* V1.Container.SecurityContext.allowPrivilegeEscalation - not possible on
  Windows, none of the capabilities are hooked up

* V1.Container.SecurityContext.Capabilities - POSIX capabilities are not
  implemented on Windows

* V1.Container.SecurityContext.privileged - Windows doesn't support privileged
  containers

* V1.Container.SecurityContext.procMount - Windows doesn't have a /proc filesystem

* V1.Container.SecurityContext.readOnlyRootFilesystem - not possible on
  Windows, write access is required for registry & system processes to run
  inside the container

* V1.Container.SecurityContext.runAsGroup - not possible on Windows, no GID support

* V1.Container.SecurityContext.runAsNonRoot - Windows does not have a root
  user. The closest equivalent is ContainerAdministrator which is an identity
  that doesn't exist on the node.

* V1.Container.SecurityContext.runAsUser - not possible on Windows, no UID
  support as int.

* V1.Container.SecurityContext.seLinuxOptions - not possible on Windows, no SELinux

* V1.Container.terminationMessagePath - this has some limitations in that
  Windows doesn't support mapping single files. The default value is
  `/dev/termination-log`, which does work because it does not exist on Windows by
  default.

##### V1.Pod

* V1.Pod.hostIPC, v1.pod.hostpid - host namespace sharing is not possible on Windows

* V1.Pod.hostNetwork - There is no Windows OS support to share the host network

* V1.Pod.dnsPolicy - `ClusterFirstWithHostNet` is not supported because Host
  Networking is not supported on Windows.

* V1.Pod.podSecurityContext - see V1.PodSecurityContext below

* V1.Pod.shareProcessNamespace - this is a beta feature, and depends on Linux
  namespaces which are not implemented on Windows. Windows cannot share
  process namespaces or the container's root filesystem. Only the network can be
  shared.

* V1.Pod.terminationGracePeriodSeconds - this is not fully implemented in
  Docker on Windows, see:
  [reference](https://github.com/moby/moby/issues/25982). The behavior today is
  that the `ENTRYPOINT` process is sent `CTRL_SHUTDOWN_EVENT`, then Windows waits 5
  seconds by default, and finally shuts down all processes using the normal
  Windows shutdown behavior. The 5 second default is actually in the Windows
  registry [inside the container](https://github.com/moby/moby/issues/25982#issuecomment-426441183),
  so it can be overridden when the container is built.

* V1.Pod.volumeDevices - this is a beta feature, and is not implemented on
  Windows. Windows cannot attach raw block devices to pods.

* V1.Pod.volumes - EmptyDir, Secret, ConfigMap, HostPath - all work and have
  tests in TestGrid

  * V1.emptyDirVolumeSource - the Node default medium is disk on Windows.
    Memory is not supported, as Windows does not have a built-in RAM disk.

* V1.VolumeMount.mountPropagation - mount propagation is not supported on Windows.

##### V1.PodSecurityContext

None of the PodSecurityContext fields work on Windows. They're listed here for
reference.

* V1.PodSecurityContext.SELinuxOptions - SELinux is not available on Windows

* V1.PodSecurityContext.RunAsUser - provides a UID, not available on Windows

* V1.PodSecurityContext.RunAsGroup - provides a GID, not available on Windows

* V1.PodSecurityContext.RunAsNonRoot - Windows does not have a root user. The
  closest equivalent is ContainerAdministrator which is an identity that
  doesn't exist on the node.

* V1.PodSecurityContext.SupplementalGroups - provides GID, not available on Windows

* V1.PodSecurityContext.Sysctls - these are part of the Linux sysctl
  interface. There's no equivalent on Windows.

#### Operating System Version Restrictions

Windows has strict compatibility rules, where the host OS version must match
the container base image OS version. Only Windows containers with a container
operating system of Windows Server 2019 are supported. Hyper-V isolation of
containers, enabling some backward compatibility of Windows container image
versions, is planned for a future release.

## Getting Help and Troubleshooting {#troubleshooting}

Your main source of help for troubleshooting your Kubernetes cluster should
start with this
[section](/docs/tasks/debug-application-cluster/troubleshooting/). Some
additional, Windows-specific troubleshooting help is included in this section.
Logs are an important element of troubleshooting issues in Kubernetes. Make
sure to include them any time you seek troubleshooting assistance from other
contributors. Follow the instructions in the SIG-Windows
[contributing guide on gathering logs](https://github.com/kubernetes/community/blob/master/sig-windows/CONTRIBUTING.md#gathering-logs).

* How do I know start.ps1 completed successfully?

  You should see kubelet, kube-proxy, and (if you chose Flannel as your
  networking solution) flanneld host-agent processes running on your node, with
  running logs being displayed in separate PowerShell windows. In addition to
  this, your Windows node should be listed as "Ready" in your Kubernetes
  cluster.

* Can I configure the Kubernetes node processes to run in the background as services?

  Kubelet and kube-proxy are already configured to run as native Windows
  Services, offering resiliency by re-starting the services automatically in the
  event of failure (for example a process crash). You have two options for
  configuring these node components as services.

  * As native Windows Services

    Kubelet & kube-proxy can be run as native Windows Services using `sc.exe`.

    ```powershell
    # Create the services for kubelet and kube-proxy in two separate commands
    sc.exe create <component_name> binPath= "<path_to_binary> --service <other_args>"

    # Please note that if the arguments contain spaces, they must be escaped.
    sc.exe create kubelet binPath= "C:\kubelet.exe --service --hostname-override 'minion' <other_args>"

    # Start the services
    Start-Service kubelet
    Start-Service kube-proxy

    # Stop the service
    Stop-Service kubelet (-Force)
    Stop-Service kube-proxy (-Force)

    # Query the service status
    Get-Service kubelet
    Get-Service kube-proxy
    ```

  * Using nssm.exe

    You can also always use alternative service managers like
    [`nssm.exe`](https://nssm.cc/) to run these processes (flanneld, kubelet &
    kube-proxy) in the background for you. You can use this
    [sample script](https://github.com/Microsoft/SDN/tree/master/Kubernetes/flannel/register-svc.ps1),
    leveraging `nssm.exe` to register kubelet, kube-proxy, and `flanneld.exe`
    to run as Windows services in the background.

    ```powershell
    register-svc.ps1 -NetworkMode <Network mode> -ManagementIP <Windows Node IP> -ClusterCIDR <Cluster subnet> -KubeDnsServiceIP <Kube-dns Service IP> -LogDir <Directory to place logs>
    ```

    The parameters are explained below:

    - `NetworkMode`: The network mode l2bridge (flannel host-gw, also the
      default value) or overlay (flannel vxlan) chosen as a network solution
    - `ManagementIP`: The IP address assigned to the Windows node. You can use
      `ipconfig` to find this.
    - `ClusterCIDR`: The cluster subnet range. (Default: 10.244.0.0/16)
    - `KubeDnsServiceIP`: The Kubernetes DNS service IP. (Default: 10.96.0.10)
    - `LogDir`: The directory where kubelet and kube-proxy logs are redirected
      into their respective output files. (Default value C:\k)

    If the above referenced script is not suitable, you can manually configure
    `nssm.exe` using the following examples.

    Register flanneld.exe:

    ```powershell
    nssm install flanneld C:\flannel\flanneld.exe
    nssm set flanneld AppParameters --kubeconfig-file=c:\k\config --iface=<ManagementIP> --ip-masq=1 --kube-subnet-mgr=1
    nssm set flanneld AppEnvironmentExtra NODE_NAME=<hostname>
    nssm set flanneld AppDirectory C:\flannel
    nssm start flanneld
    ```

    Register kubelet.exe:

    ```powershell
    # Microsoft releases the pause infrastructure container at mcr.microsoft.com/oss/kubernetes/pause:3.4.1
    nssm install kubelet C:\k\kubelet.exe
    nssm set kubelet AppParameters --hostname-override=<hostname> --v=6 --pod-infra-container-image=mcr.microsoft.com/oss/kubernetes/pause:3.4.1 --resolv-conf="" --allow-privileged=true --enable-debugging-handlers --cluster-dns=<DNS-service-IP> --cluster-domain=cluster.local --kubeconfig=c:\k\config --hairpin-mode=promiscuous-bridge --image-pull-progress-deadline=20m --cgroups-per-qos=false  --log-dir=<log directory> --logtostderr=false --enforce-node-allocatable="" --network-plugin=cni --cni-bin-dir=c:\k\cni --cni-conf-dir=c:\k\cni\config
    nssm set kubelet AppDirectory C:\k
    nssm start kubelet
    ```

    Register kube-proxy.exe (l2bridge / host-gw):

    ```powershell
    nssm install kube-proxy C:\k\kube-proxy.exe
    nssm set kube-proxy AppDirectory c:\k
    nssm set kube-proxy AppParameters --v=4 --proxy-mode=kernelspace --hostname-override=<hostname>--kubeconfig=c:\k\config --enable-dsr=false --log-dir=<log directory> --logtostderr=false
    nssm.exe set kube-proxy AppEnvironmentExtra KUBE_NETWORK=cbr0
    nssm set kube-proxy DependOnService kubelet
    nssm start kube-proxy
    ```

    Register kube-proxy.exe (overlay / vxlan):

    ```powershell
    nssm install kube-proxy C:\k\kube-proxy.exe
    nssm set kube-proxy AppDirectory c:\k
    nssm set kube-proxy AppParameters --v=4 --proxy-mode=kernelspace --feature-gates="WinOverlay=true" --hostname-override=<hostname> --kubeconfig=c:\k\config --network-name=vxlan0 --source-vip=<source-vip> --enable-dsr=false --log-dir=<log directory> --logtostderr=false
    nssm set kube-proxy DependOnService kubelet
    nssm start kube-proxy
    ```

    For initial troubleshooting, you can use the following flags in
    [`nssm.exe`](https://nssm.cc/) to redirect stdout and stderr to a output file:

    ```powershell
    nssm set <Service Name> AppStdout C:\k\mysvc.log
    nssm set <Service Name> AppStderr C:\k\mysvc.log
    ```

    For additional details, see official [nssm usage](https://nssm.cc/usage) docs.

* My Windows Pods do not have network connectivity

  If you are using virtual machines, ensure that MAC spoofing is enabled on
  all the VM network adapter(s).

* My Windows Pods cannot ping external resources

  Windows Pods do not have outbound rules programmed for the ICMP protocol
  today. However, TCP/UDP is supported. When trying to demonstrate connectivity
  to resources outside of the cluster, please substitute `ping <IP>` with
  corresponding `curl <IP>` commands.

  If you are still facing problems, most likely your network configuration in
  [cni.conf](https://github.com/Microsoft/SDN/blob/master/Kubernetes/flannel/l2bridge/cni/config/cni.conf)
  deserves some extra attention. You can always edit this static file. The
  configuration update will apply to any newly created Kubernetes resources.

  One of the Kubernetes networking requirements (see
  [Kubernetes network model](/docs/concepts/cluster-administration/networking/))
  is for cluster communication to occur without NAT internally. To honor this
  requirement, there is an
  [ExceptionList](https://github.com/Microsoft/SDN/blob/master/Kubernetes/flannel/l2bridge/cni/config/cni.conf#L20)
  for all the communication where we do not want outbound NAT to occur. However,
  this also means that you need to exclude the external IP you are trying to
  query from the ExceptionList. Only then will the traffic originating from your
  Windows pods be SNAT'ed correctly to receive a response from the outside
  world. In this regard, your ExceptionList in `cni.conf` should look as
  follows:

  ```conf
  "ExceptionList": [
      "10.244.0.0/16",  # Cluster subnet
      "10.96.0.0/12",   # Service subnet
      "10.127.130.0/24" # Management (host) subnet
  ]
  ```

* My Windows node cannot access NodePort service

  Local NodePort access from the node itself fails. This is a known
  limitation. NodePort access works from other nodes or external clients.

* vNICs and HNS endpoints of containers are being deleted

  This issue can be caused when the `hostname-override` parameter is not
  passed to
  [kube-proxy](/docs/reference/command-line-tools-reference/kube-proxy/).
  To resolve it, users need to pass the hostname to kube-proxy as follows:

  ```powershell
  C:\k\kube-proxy.exe --hostname-override=$(hostname)
  ```

* With flannel my nodes are having issues after rejoining a cluster

  Whenever a previously deleted node is being re-joined to the cluster,
  flannelD tries to assign a new pod subnet to the node. Users should remove the
  old pod subnet configuration files in the following paths:

  ```powershell
  Remove-Item C:\k\SourceVip.json
  Remove-Item C:\k\SourceVipRequest.json
  ```

* After launching `start.ps1`, flanneld is stuck in "Waiting for the Network
  to be created"

  There are numerous reports of this
  [issue](https://github.com/coreos/flannel/issues/1066); most likely it is a
  timing issue for when the management IP of the flannel network is set. A
  workaround is to relaunch start.ps1 or relaunch it manually as follows:

  ```powershell
  PS C:> [Environment]::SetEnvironmentVariable("NODE_NAME", "<Windows_Worker_Hostname>")
  PS C:> C:\flannel\flanneld.exe --kubeconfig-file=c:\k\config --iface=<Windows_Worker_Node_IP> --ip-masq=1 --kube-subnet-mgr=1
  ```

* My Windows Pods cannot launch because of missing `/run/flannel/subnet.env`

  This indicates that Flannel didn't launch correctly. You can either try to
  restart flanneld.exe or you can copy the files over manually from
  `/run/flannel/subnet.env` on the Kubernetes master to
  `C:\run\flannel\subnet.env` on the Windows worker node and modify the
  `FLANNEL_SUBNET` row to a different number. For example, if node subnet
  10.244.4.1/24 is desired:

  ```none
  FLANNEL_NETWORK=10.244.0.0/16
  FLANNEL_SUBNET=10.244.4.1/24
  FLANNEL_MTU=1500
  FLANNEL_IPMASQ=true
  ```

* My Windows node cannot access my services using the service IP

  This is a known limitation of the current networking stack on Windows.
  Windows Pods are able to access the service IP however.

* No network adapter is found when starting kubelet

  The Windows networking stack needs a virtual adapter for Kubernetes
  networking to work. If the following commands return no results (in an admin
  shell), virtual network creation — a necessary prerequisite for Kubelet to
  work — has failed:

  ```powershell
  Get-HnsNetwork | ? Name -ieq "cbr0"
  Get-NetAdapter | ? Name -Like "vEthernet (Ethernet*"
  ```

  Often it is worthwhile to modify the
  [InterfaceName](https://github.com/microsoft/SDN/blob/master/Kubernetes/flannel/start.ps1#L7)
  parameter of the start.ps1 script, in cases where the host's network adapter
  isn't "Ethernet". Otherwise, consult the output of the `start-kubelet.ps1`
  script to see if there are errors during virtual network creation.

* My Pods are stuck at "Container Creating" or restarting over and over

  Check that your pause image is compatible with your OS version. The
  [instructions](https://docs.microsoft.com/en-us/virtualization/windowscontainers/kubernetes/deploying-resources)
  assume that both the OS and the containers are version 1803. If you have a
  later version of Windows, such as an Insider build, you need to adjust the
  images accordingly. Please refer to the Microsoft's
  [Docker repository](https://hub.docker.com/u/microsoft/) for images.
  Regardless, both the pause image Dockerfile and the sample service expect
  the image to be tagged as :latest.

* DNS resolution is not properly working

  Check the [DNS limitations for Windows](#dns-limitations).

* `kubectl port-forward` fails with "unable to do port forwarding: wincat not found"

  This was implemented in Kubernetes 1.15 by including wincat.exe in the
  pause infrastructure container `mcr.microsoft.com/oss/kubernetes/pause:3.4.1`.
  Be sure to use these versions or newer ones.  If you would like to build your
  own pause infrastructure container be sure to include
  [wincat](https://github.com/kubernetes-sigs/sig-windows-tools/tree/master/cmd/wincat).

* My Kubernetes installation is failing because my Windows Server node is
  behind a proxy

  If you are behind a proxy, the following PowerShell environment variables
  must be defined:

  ```PowerShell
  [Environment]::SetEnvironmentVariable("HTTP_PROXY", "http://proxy.example.com:80/", [EnvironmentVariableTarget]::Machine)
  [Environment]::SetEnvironmentVariable("HTTPS_PROXY", "http://proxy.example.com:443/", [EnvironmentVariableTarget]::Machine)
  ```

* What is a `pause` container?

  In a Kubernetes Pod, an infrastructure or "pause" container is first created
  to host the container endpoint. Containers that belong to the same pod,
  including infrastructure and worker containers, share a common network
  namespace and endpoint (same IP and port space). Pause containers are needed
  to accommodate worker containers crashing or restarting without losing any of
  the networking configuration.

  The "pause" (infrastructure) image is hosted on Microsoft Container Registry
  (MCR). You can access it using `mcr.microsoft.com/oss/kubernetes/pause:3.4.1`.
  For more details, see the
  [DOCKERFILE](https://github.com/kubernetes-sigs/windows-testing/blob/master/images/pause/Dockerfile).

### Further investigation

If these steps don't resolve your problem, you can get help running Windows
containers on Windows nodes in Kubernetes through:

* StackOverflow [Windows Server Container](https://stackoverflow.com/questions/tagged/windows-server-container) topic

* Kubernetes Official Forum [discuss.kubernetes.io](https://discuss.kubernetes.io/)

* Kubernetes Slack [#SIG-Windows Channel](https://kubernetes.slack.com/messages/sig-windows)

## Reporting Issues and Feature Requests

If you have what looks like a bug, or you would like to make a feature
request, please use the
[GitHub issue tracking system](https://github.com/kubernetes/kubernetes/issues).
You can open issues on
[GitHub](https://github.com/kubernetes/kubernetes/issues/new/choose) and
assign them to SIG-Windows. You should first search the list of issues in case
it was reported previously and comment with your experience on the issue and
add additional logs. SIG-Windows Slack is also a great avenue to get some
initial support and troubleshooting ideas prior to creating a ticket.

If filing a bug, please include detailed information about how to reproduce
the problem, such as:

* Kubernetes version: kubectl version
* Environment details: Cloud provider, OS distro, networking choice and
  configuration, and Docker version
* Detailed steps to reproduce the problem
* [Relevant logs](https://github.com/kubernetes/community/blob/master/sig-windows/CONTRIBUTING.md#gathering-logs)
* Tag the issue sig/windows by commenting on the issue with `/sig windows` to
  bring it to a SIG-Windows member's attention

## {{% heading "whatsnext" %}}

We have a lot of features in our roadmap. An abbreviated high level list is
included below, but we encourage you to view our
[roadmap project](https://github.com/orgs/kubernetes/projects/8) and help us make
Windows support better by
[contributing](https://github.com/kubernetes/community/blob/master/sig-windows/).

### Hyper-V isolation

Hyper-V isolation is required to enable the following use cases for Windows
containers in Kubernetes:

* Hypervisor-based isolation between pods for additional security

* Backwards compatibility allowing a node to run a newer Windows Server
  version without requiring containers to be rebuilt

* Specific CPU/NUMA settings for a pod

* Memory isolation and reservations

Hyper-V isolation support will be added in a later release and will require
CRI-Containerd.

### Deployment with kubeadm and cluster API

Kubeadm is becoming the de facto standard for users to deploy a Kubernetes
cluster. Windows node support in kubeadm is currently a work-in-progress but a
guide is available
[here](/docs/tasks/administer-cluster/kubeadm/adding-windows-nodes/). We are
also making investments in cluster API to ensure Windows nodes are properly
provisioned.

