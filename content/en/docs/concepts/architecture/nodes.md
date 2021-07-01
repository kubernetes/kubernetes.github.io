---
reviewers:
- caesarxuchao
- dchen1107
title: Nodes
content_type: concept
weight: 10
---

<!-- overview -->

Kubernetes runs your workload by placing containers into Pods to run on _Nodes_.
A node may be a virtual or physical machine, depending on the cluster. Each node
is managed by the
{{< glossary_tooltip text="control plane" term_id="control-plane" >}}
and contains the services necessary to run
{{< glossary_tooltip text="Pods" term_id="pod" >}}

Typically you have several nodes in a cluster; in a learning or resource-limited
environment, you might have only one node.

The [components](/docs/concepts/overview/components/#node-components) on a node include the
{{< glossary_tooltip text="kubelet" term_id="kubelet" >}}, a
{{< glossary_tooltip text="container runtime" term_id="container-runtime" >}}, and the
{{< glossary_tooltip text="kube-proxy" term_id="kube-proxy" >}}.

<!-- body -->

## Management

There are two main ways to have Nodes added to the {{< glossary_tooltip text="API server" term_id="kube-apiserver" >}}:

1. The kubelet on a node self-registers to the control plane
2. You (or another human user) manually add a Node object

After you create a Node object, or the kubelet on a node self-registers, the
control plane checks whether the new Node object is valid. For example, if you
try to create a Node from the following JSON manifest:

```json
{
  "kind": "Node",
  "apiVersion": "v1",
  "metadata": {
    "name": "10.240.79.157",
    "labels": {
      "name": "my-first-k8s-node"
    }
  }
}
```

Kubernetes creates a Node object internally (the representation). Kubernetes checks
that a kubelet has registered to the API server that matches the `metadata.name`
field of the Node. If the node is healthy (i.e. all necessary services are running),
then it is eligible to run a Pod. Otherwise, that node is ignored for any cluster activity
until it becomes healthy.

{{< note >}}
Kubernetes keeps the object for the invalid Node and continues checking to see whether
it becomes healthy.

You, or a {{< glossary_tooltip term_id="controller" text="controller">}}, must explicitly
delete the Node object to stop that health checking.
{{< /note >}}

The name of a Node object must be a valid
[DNS subdomain name](/docs/concepts/overview/working-with-objects/names#dns-subdomain-names).

### Node name uniqueness

The [name](/docs/concepts/overview/working-with-objects/names#names) identifies a Node. Two Nodes
cannot have the same name at the same time. Kubernetes also assumes that a resource with the same
name is the same object. In case of a Node, it is implicitly assumed that an instance using the
same name will have the same state (e.g. network settings, root disk contents). This may lead to
inconsistencies if an instance was modified without changing its name. If the Node needs to be
replaced or updated significantly, the existing Node object needs to be removed from API server
first and re-added after the update.

### Self-registration of Nodes

When the kubelet flag `--register-node` is true (the default), the kubelet will attempt to
register itself with the API server.  This is the preferred pattern, used by most distros.

For self-registration, the kubelet is started with the following options:

  - `--kubeconfig` - Path to credentials to authenticate itself to the API server.
  - `--cloud-provider` - How to talk to a {{< glossary_tooltip text="cloud provider" term_id="cloud-provider" >}} to read metadata about itself.
  - `--register-node` - Automatically register with the API server.
  - `--register-with-taints` - Register the node with the given list of {{< glossary_tooltip text="taints" term_id="taint" >}} (comma separated `<key>=<value>:<effect>`).

    No-op if `register-node` is false.
  - `--node-ip` - IP address of the node.
  - `--node-labels` - {{< glossary_tooltip text="Labels" term_id="label" >}} to add when registering the node in the cluster (see label restrictions enforced by the [NodeRestriction admission plugin](/docs/reference/access-authn-authz/admission-controllers/#noderestriction)).
  - `--node-status-update-frequency` - Specifies how often kubelet posts node status to master.

When the [Node authorization mode](/docs/reference/access-authn-authz/node/) and
[NodeRestriction admission plugin](/docs/reference/access-authn-authz/admission-controllers/#noderestriction) are enabled,
kubelets are only authorized to create/modify their own Node resource.

### Manual Node administration

You can create and modify Node objects using
{{< glossary_tooltip text="kubectl" term_id="kubectl" >}}.

When you want to create Node objects manually, set the kubelet flag `--register-node=false`.

You can modify Node objects regardless of the setting of `--register-node`.
For example, you can set labels on an existing Node or mark it unschedulable.

You can use labels on Nodes in conjunction with node selectors on Pods to control
scheduling. For example, you can constrain a Pod to only be eligible to run on
a subset of the available nodes.

Marking a node as unschedulable prevents the scheduler from placing new pods onto
that Node but does not affect existing Pods on the Node. This is useful as a
preparatory step before a node reboot or other maintenance.

To mark a Node unschedulable, run:

```shell
kubectl cordon $NODENAME
```

{{< note >}}
Pods that are part of a {{< glossary_tooltip term_id="daemonset" >}} tolerate
being run on an unschedulable Node. DaemonSets typically provide node-local services
that should run on the Node even if it is being drained of workload applications.
{{< /note >}}

## Node status

A Node's status contains the following information:

* [Addresses](#addresses)
* [Conditions](#condition)
* [Capacity and Allocatable](#capacity)
* [Info](#info)

You can use `kubectl` to view a Node's status and other details:

```shell
kubectl describe node <insert-node-name-here>
```

Each section of the output is described below.

### Addresses

The usage of these fields varies depending on your cloud provider or bare metal configuration.

* HostName: The hostname as reported by the node's kernel. Can be overridden via the kubelet `--hostname-override` parameter.
* ExternalIP: Typically the IP address of the node that is externally routable (available from outside the cluster).
* InternalIP: Typically the IP address of the node that is routable only within the cluster.


### Conditions {#condition}

The `conditions` field describes the status of all `Running` nodes. Examples of conditions include:

{{< table caption = "Node conditions, and a description of when each condition applies." >}}
| Node Condition       | Description |
|----------------------|-------------|
| `Ready`              | `True` if the node is healthy and ready to accept pods, `False` if the node is not healthy and is not accepting pods, and `Unknown` if the node controller has not heard from the node in the last `node-monitor-grace-period` (default is 40 seconds) |
| `DiskPressure`       | `True` if pressure exists on the disk size--that is, if the disk capacity is low; otherwise `False` |
| `MemoryPressure`     | `True` if pressure exists on the node memory--that is, if the node memory is low; otherwise `False` |
| `PIDPressure`        | `True` if pressure exists on the processes—that is, if there are too many processes on the node; otherwise `False` |
| `NetworkUnavailable` | `True` if the network for the node is not correctly configured, otherwise `False` |
{{< /table >}}

{{< note >}}
If you use command-line tools to print details of a cordoned Node, the Condition includes
`SchedulingDisabled`. `SchedulingDisabled` is not a Condition in the Kubernetes API; instead,
cordoned nodes are marked Unschedulable in their spec.
{{< /note >}}

The node condition is represented as a JSON object. For example, the following structure describes a healthy node:

```json
"conditions": [
  {
    "type": "Ready",
    "status": "True",
    "reason": "KubeletReady",
    "message": "kubelet is posting ready status",
    "lastHeartbeatTime": "2019-06-05T18:38:35Z",
    "lastTransitionTime": "2019-06-05T11:41:27Z"
  }
]
```

If the Status of the Ready condition remains `Unknown` or `False` for longer than the `pod-eviction-timeout` (an argument passed to the {{< glossary_tooltip text="kube-controller-manager" term_id="kube-controller-manager" >}}), then all the Pods on the node are scheduled for deletion by the node controller. The default eviction timeout duration is **five minutes**. In some cases when the node is unreachable, the API server is unable to communicate with the kubelet on the node. The decision to delete the pods cannot be communicated to the kubelet until communication with the API server is re-established. In the meantime, the pods that are scheduled for deletion may continue to run on the partitioned node.

The node controller does not force delete pods until it is confirmed that they have stopped
running in the cluster. You can see the pods that might be running on an unreachable node as
being in the `Terminating` or `Unknown` state. In cases where Kubernetes cannot deduce from the
underlying infrastructure if a node has permanently left a cluster, the cluster administrator
may need to delete the node object by hand. Deleting the node object from Kubernetes causes
all the Pod objects running on the node to be deleted from the API server and frees up their
names.

The node lifecycle controller automatically creates
[taints](/docs/concepts/scheduling-eviction/taint-and-toleration/) that represent conditions.
The scheduler takes the Node's taints into consideration when assigning a Pod to a Node.
Pods can also have tolerations which let them tolerate a Node's taints.

See [Taint Nodes by Condition](/docs/concepts/scheduling-eviction/taint-and-toleration/#taint-nodes-by-condition)
for more details.

### Capacity and Allocatable {#capacity}

Describes the resources available on the node: CPU, memory, and the maximum
number of pods that can be scheduled onto the node.

The fields in the capacity block indicate the total amount of resources that a
Node has. The allocatable block indicates the amount of resources on a
Node that is available to be consumed by normal Pods.

You may read more about capacity and allocatable resources while learning how
to [reserve compute resources](/docs/tasks/administer-cluster/reserve-compute-resources/#node-allocatable)
on a Node.

### Info

Describes general information about the node, such as kernel version, Kubernetes version (kubelet and kube-proxy version), Docker version (if used), and OS name.
This information is gathered by Kubelet from the node.

### Node controller

The node {{< glossary_tooltip text="controller" term_id="controller" >}} is a
Kubernetes control plane component that manages various aspects of nodes.

The node controller has multiple roles in a node's life. The first is assigning a
CIDR block to the node when it is registered (if CIDR assignment is turned on).

The second is keeping the node controller's internal list of nodes up to date with
the cloud provider's list of available machines. When running in a cloud
environment and whenever a node is unhealthy, the node controller asks the cloud
provider if the VM for that node is still available. If not, the node
controller deletes the node from its list of nodes.

The third is monitoring the nodes' health. The node controller is
responsible for:
- Updating the NodeReady condition of NodeStatus to ConditionUnknown when a node
  becomes unreachable, as the node controller stops receiving heartbeats for some
  reason such as the node being down.
- Evicting all the pods from the node using graceful termination if
  the node continues to be unreachable. The default timeouts are 40s to start
  reporting ConditionUnknown and 5m after that to start evicting pods.

The node controller checks the state of each node every `--node-monitor-period` seconds.

#### Heartbeats

Heartbeats, sent by Kubernetes nodes, help determine the availability of a node.

There are two forms of heartbeats: updates of `NodeStatus` and the
[Lease object](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#lease-v1-coordination-k8s-io).
Each Node has an associated Lease object in the `kube-node-lease`
{{< glossary_tooltip term_id="namespace" text="namespace">}}.
Lease is a lightweight resource, which improves the performance
of the node heartbeats as the cluster scales.

The kubelet is responsible for creating and updating the `NodeStatus` and
a Lease object.

- The kubelet updates the `NodeStatus` either when there is change in status
  or if there has been no update for a configured interval. The default interval
  for `NodeStatus` updates is 5 minutes, which is much longer than the 40 second default
  timeout for unreachable nodes.
- The kubelet creates and then updates its Lease object every 10 seconds
  (the default update interval). Lease updates occur independently from the
  `NodeStatus` updates. If the Lease update fails, the kubelet retries with
  exponential backoff starting at 200 milliseconds and capped at 7 seconds.

#### Reliability

 In most cases, the node controller limits the eviction rate to
`--node-eviction-rate` (default 0.1) per second, meaning it won't evict pods
from more than 1 node per 10 seconds.

The node eviction behavior changes when a node in a given availability zone
becomes unhealthy. The node controller checks what percentage of nodes in the zone
are unhealthy (NodeReady condition is ConditionUnknown or ConditionFalse) at
the same time:
- If the fraction of unhealthy nodes is at least `--unhealthy-zone-threshold`
  (default 0.55), then the eviction rate is reduced.
- If the cluster is small (i.e. has less than or equal to
  `--large-cluster-size-threshold` nodes - default 50), then evictions are stopped.
- Otherwise, the eviction rate is reduced to `--secondary-node-eviction-rate`
  (default 0.01) per second.

The reason these policies are implemented per availability zone is because one
availability zone might become partitioned from the master while the others remain
connected. If your cluster does not span multiple cloud provider availability zones,
then there is only one availability zone (i.e. the whole cluster).

A key reason for spreading your nodes across availability zones is so that the
workload can be shifted to healthy zones when one entire zone goes down.
Therefore, if all nodes in a zone are unhealthy, then the node controller evicts at
the normal rate of `--node-eviction-rate`.  The corner case is when all zones are
completely unhealthy (i.e. there are no healthy nodes in the cluster). In such a
case, the node controller assumes that there is some problem with master
connectivity and stops all evictions until some connectivity is restored.

The node controller is also responsible for evicting pods running on nodes with
`NoExecute` taints, unless those pods tolerate that taint.
The node controller also adds {{< glossary_tooltip text="taints" term_id="taint" >}}
corresponding to node problems like node unreachable or not ready. This means
that the scheduler won't place Pods onto unhealthy nodes.

### Node capacity

Node objects track information about the Node's resource capacity: for example, the amount
of memory available and the number of CPUs.
Nodes that [self register](#self-registration-of-nodes) report their capacity during
registration. If you [manually](#manual-node-administration) add a Node, then
you need to set the node's capacity information when you add it.

The Kubernetes {{< glossary_tooltip text="scheduler" term_id="kube-scheduler" >}} ensures that
there are enough resources for all the Pods on a Node. The scheduler checks that the sum
of the requests of containers on the node is no greater than the node's capacity.
That sum of requests includes all containers managed by the kubelet, but excludes any
containers started directly by the container runtime, and also excludes any
processes running outside of the kubelet's control.

{{< note >}}
If you want to explicitly reserve resources for non-Pod processes, see
[reserve resources for system daemons](/docs/tasks/administer-cluster/reserve-compute-resources/#system-reserved).
{{< /note >}}

## Node topology

{{< feature-state state="alpha" for_k8s_version="v1.16" >}}

If you have enabled the `TopologyManager`
[feature gate](/docs/reference/command-line-tools-reference/feature-gates/), then
the kubelet can use topology hints when making resource assignment decisions.
See [Control Topology Management Policies on a Node](/docs/tasks/administer-cluster/topology-manager/)
for more information.

## Graceful node shutdown {#graceful-node-shutdown}

{{< feature-state state="beta" for_k8s_version="v1.21" >}}

The kubelet attempts to detect node system shutdown and terminates pods running on the node.

Kubelet ensures that pods follow the normal [pod termination process](/docs/concepts/workloads/pods/pod-lifecycle/#pod-termination) during the node shutdown.

The Graceful node shutdown feature depends on systemd since it takes advantage of
[systemd inhibitor locks](https://www.freedesktop.org/wiki/Software/systemd/inhibit/) to
delay the node shutdown with a given duration.

Graceful node shutdown is controlled with the `GracefulNodeShutdown`
[feature gate](/docs/reference/command-line-tools-reference/feature-gates/) which is
enabled by default in 1.21.

Note that by default, both configuration options described below,
`ShutdownGracePeriod` and `ShutdownGracePeriodCriticalPods` are set to zero,
thus not activating Graceful node shutdown functionality.
To activate the feature, the two kubelet config settings should be configured appropriately and set to non-zero values.

During a graceful shutdown, kubelet terminates pods in two phases:

1. Terminate regular pods running on the node.
2. Terminate [critical pods](/docs/tasks/administer-cluster/guaranteed-scheduling-critical-addon-pods/#marking-pod-as-critical) running on the node.

Graceful node shutdown feature is configured with two [`KubeletConfiguration`](/docs/tasks/administer-cluster/kubelet-config-file/) options:
* `ShutdownGracePeriod`:
  * Specifies the total duration that the node should delay the shutdown by. This is the total grace period for pod termination for both regular and [critical pods](/docs/tasks/administer-cluster/guaranteed-scheduling-critical-addon-pods/#marking-pod-as-critical).
* `ShutdownGracePeriodCriticalPods`:
  * Specifies the duration used to terminate [critical pods](/docs/tasks/administer-cluster/guaranteed-scheduling-critical-addon-pods/#marking-pod-as-critical) during a node shutdown. This value should be less than `ShutdownGracePeriod`.

For example, if `ShutdownGracePeriod=30s`, and
`ShutdownGracePeriodCriticalPods=10s`, kubelet will delay the node shutdown by
30 seconds. During the shutdown, the first 20 (30-10) seconds would be reserved
for gracefully terminating normal pods, and the last 10 seconds would be
reserved for terminating [critical pods](/docs/tasks/administer-cluster/guaranteed-scheduling-critical-addon-pods/#marking-pod-as-critical).

{{< note >}}
When pods were evicted during the graceful node shutdown, they are marked as failed.
Running `kubectl get pods` shows the status of the the evicted pods as `Shutdown`.
And `kubectl describe pod` indicates that the pod was evicted because of node shutdown:

```
Status:         Failed
Reason:         Shutdown
Message:        Node is shutting, evicting pods
```

Failed pod objects will be preserved until explicitly deleted or [cleaned up by the GC](/docs/concepts/workloads/pods/pod-lifecycle/#pod-garbage-collection).
This is a change of behavior compared to abrupt node termination.
{{< /note >}}

## {{% heading "whatsnext" %}}

* Learn about the [components](/docs/concepts/overview/components/#node-components) that make up a node.
* Read the [API definition for Node](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#node-v1-core).
* Read the [Node](https://git.k8s.io/community/contributors/design-proposals/architecture/architecture.md#the-kubernetes-node)
  section of the architecture design document.
* Read about [taints and tolerations](/docs/concepts/scheduling-eviction/taint-and-toleration/).
