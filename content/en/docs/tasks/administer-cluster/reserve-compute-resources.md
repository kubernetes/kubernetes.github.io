---
reviewers:
- vishh
- derekwaynecarr
- dashpole
title: Reserve Compute Resources for System Daemons
content_type: task
min-kubernetes-server-version: 1.8
---

<!-- overview -->

Kubernetes nodes can be scheduled to `Capacity`. Pods can consume all the
available capacity on a node by default. This is an issue because nodes
typically run quite a few system daemons that power the OS and Kubernetes
itself. Unless resources are set aside for these system daemons, pods and system
daemons compete for resources and lead to resource starvation issues on the
node.

The `kubelet` exposes a feature named 'Node Allocatable' that helps to reserve
compute resources for system daemons. Kubernetes recommends cluster
administrators to configure 'Node Allocatable' based on their workload density
on each node.

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}
Your Kubernetes server must be at or later than version 1.17 to use
the kubelet command line option `--reserved-cpus` to set an
[explicitly reserved CPU list](#explicitly-reserved-cpu-list).

<!-- steps -->

## Node Allocatable

![node capacity](/images/docs/node-capacity.svg)

'Allocatable' on a Kubernetes node is defined as the amount of compute resources
that are available for pods. The scheduler does not over-subscribe
'Allocatable'. 'CPU', 'memory' and 'ephemeral-storage' are supported as of now.

Node Allocatable is exposed as part of `v1.Node` object in the API and as part
of `kubectl describe node` in the CLI.

Resources can be reserved for two categories of system daemons in the `kubelet`.

### Enabling QoS and Pod level cgroups

To properly enforce node allocatable constraints on the node, you must
enable the new cgroup hierarchy via the `--cgroups-per-qos` flag. This flag is
enabled by default. When enabled, the `kubelet` will parent all end-user pods
under a cgroup hierarchy managed by the `kubelet`.

### Configuring a cgroup driver

The `kubelet` supports manipulation of the cgroup hierarchy on
the host using a cgroup driver. The driver is configured via the
`--cgroup-driver` flag.

The supported values are the following:

* `cgroupfs` is the default driver that performs direct manipulation of the
cgroup filesystem on the host in order to manage cgroup sandboxes.
* `systemd` is an alternative driver that manages cgroup sandboxes using
transient slices for resources that are supported by that init system.

Depending on the configuration of the associated container runtime,
operators may have to choose a particular cgroup driver to ensure
proper system behavior. For example, if operators use the `systemd`
cgroup driver provided by the `docker` runtime, the `kubelet` must
be configured to use the `systemd` cgroup driver.

### Kube Reserved

- **Kubelet Flag**: `--kube-reserved=[cpu=100m][,][memory=100Mi][,][ephemeral-storage=1Gi][,][pid=1000]`
- **Kubelet Flag**: `--kube-reserved-cgroup=`

`kube-reserved` is meant to capture resource reservation for kubernetes system
daemons like the `kubelet`, `container runtime`, `node problem detector`, etc.
It is not meant to reserve resources for system daemons that are run as pods.
`kube-reserved` is typically a function of `pod density` on the nodes.

In addition to `cpu`, `memory`, and `ephemeral-storage`, `pid` may be
specified to reserve the specified number of process IDs for
kubernetes system daemons.

To optionally enforce `kube-reserved` on kubernetes system daemons, specify the parent
control group for kube daemons as the value for `--kube-reserved-cgroup` kubelet
flag.

It is recommended that the kubernetes system daemons are placed under a top
level control group (`runtime.slice` on systemd machines for example). Each
system daemon should ideally run within its own child control group. Refer to
[the design proposal](https://git.k8s.io/community/contributors/design-proposals/node/node-allocatable.md#recommended-cgroups-setup)
for more details on recommended control group hierarchy.

Note that Kubelet **does not** create `--kube-reserved-cgroup` if it doesn't
exist. Kubelet will fail if an invalid cgroup is specified.

### System Reserved

- **Kubelet Flag**: `--system-reserved=[cpu=100m][,][memory=100Mi][,][ephemeral-storage=1Gi][,][pid=1000]`
- **Kubelet Flag**: `--system-reserved-cgroup=`

`system-reserved` is meant to capture resource reservation for OS system daemons
like `sshd`, `udev`, etc. `system-reserved` should reserve `memory` for the
`kernel` too since `kernel` memory is not accounted to pods in Kubernetes at this time.
Reserving resources for user login sessions is also recommended (`user.slice` in
systemd world).

In addition to `cpu`, `memory`, and `ephemeral-storage`, `pid` may be
specified to reserve the specified number of process IDs for OS system
daemons.

To optionally enforce `system-reserved` on system daemons, specify the parent
control group for OS system daemons as the value for `--system-reserved-cgroup`
kubelet flag.

It is recommended that the OS system daemons are placed under a top level
control group (`system.slice` on systemd machines for example).

Note that `kubelet` **does not** create `--system-reserved-cgroup` if it doesn't
exist. `kubelet` will fail if an invalid cgroup is specified.

### Explicitly Reserved CPU List

{{< feature-state for_k8s_version="v1.17" state="stable" >}}

**Kubelet Flag**: `--reserved-cpus=0-3`

`reserved-cpus` is meant to define an explicit CPU set for OS system daemons and
kubernetes system daemons. `reserved-cpus` is for systems that do not intend to
define separate top level cgroups for OS system daemons and kubernetes system daemons
with regard to cpuset resource.
If the Kubelet **does not** have `--system-reserved-cgroup` and `--kube-reserved-cgroup`,
the explicit cpuset provided by `reserved-cpus` will take precedence over the CPUs
defined by `--kube-reserved` and `--system-reserved` options.

This option is specifically designed for Telco/NFV use cases where uncontrolled
interrupts/timers may impact the workload performance. you can use this option
to define the explicit cpuset for the system/kubernetes daemons as well as the
interrupts/timers, so the rest CPUs on the system can be used exclusively for
workloads, with less impact from uncontrolled interrupts/timers. To move the
system daemon, kubernetes daemons and interrupts/timers to the explicit cpuset
defined by this option, other mechanism outside Kubernetes should be used.
For example: in Centos, you can do this using the tuned toolset.

### Eviction Thresholds

**Kubelet Flag**: `--eviction-hard=[memory.available<500Mi]`

Memory pressure at the node level leads to System OOMs which affects the entire
node and all pods running on it. Nodes can go offline temporarily until memory
has been reclaimed. To avoid (or reduce the probability of) system OOMs kubelet
provides [out of resource](/docs/concepts/scheduling-eviction/node-pressure-eviction/)
management. Evictions are
supported for `memory` and `ephemeral-storage` only. By reserving some memory via
`--eviction-hard` flag, the `kubelet` attempts to evict pods whenever memory
availability on the node drops below the reserved value. Hypothetically, if
system daemons did not exist on a node, pods cannot use more than `capacity -
eviction-hard`. For this reason, resources reserved for evictions are not
available for pods.

### Enforcing Node Allocatable

**Kubelet Flag**: `--enforce-node-allocatable=pods[,][system-reserved][,][kube-reserved]`

The scheduler treats 'Allocatable' as the available `capacity` for pods.

`kubelet` enforce 'Allocatable' across pods by default. Enforcement is performed
by evicting pods whenever the overall usage across all pods exceeds
'Allocatable'. More details on eviction policy can be found
on the [node pressure eviction](/docs/concepts/scheduling-eviction/node-pressure-eviction/)
page. This enforcement is controlled by
specifying `pods` value to the kubelet flag `--enforce-node-allocatable`.

Optionally, `kubelet` can be made to enforce `kube-reserved` and
`system-reserved` by specifying `kube-reserved` & `system-reserved` values in
the same flag. Note that to enforce `kube-reserved` or `system-reserved`,
`--kube-reserved-cgroup` or `--system-reserved-cgroup` needs to be specified
respectively.

## General Guidelines

System daemons are expected to be treated similar to 'Guaranteed' pods. System
daemons can burst within their bounding control groups and this behavior needs
to be managed as part of kubernetes deployments. For example, `kubelet` should
have its own control group and share `kube-reserved` resources with the
container runtime. However, Kubelet cannot burst and use up all available Node
resources if `kube-reserved` is enforced.

Be extra careful while enforcing `system-reserved` reservation since it can lead
to critical system services being CPU starved, OOM killed, or unable
to fork on the node. The
recommendation is to enforce `system-reserved` only if a user has profiled their
nodes exhaustively to come up with precise estimates and is confident in their
ability to recover if any process in that group is oom-killed.

* To begin with enforce 'Allocatable' on `pods`.
* Once adequate monitoring and alerting is in place to track kube system
  daemons, attempt to enforce `kube-reserved` based on usage heuristics.
* If absolutely necessary, enforce `system-reserved` over time.

The resource requirements of kube system daemons may grow over time as more and
more features are added. Over time, kubernetes project will attempt to bring
down utilization of node system daemons, but that is not a priority as of now.
So expect a drop in `Allocatable` capacity in future releases.

<!-- discussion -->

## Example Scenario

Here is an example to illustrate Node Allocatable computation:

* Node has `32Gi` of `memory`, `16 CPUs` and `100Gi` of `Storage`
* `--kube-reserved` is set to `cpu=1,memory=2Gi,ephemeral-storage=1Gi`
* `--system-reserved` is set to `cpu=500m,memory=1Gi,ephemeral-storage=1Gi`
* `--eviction-hard` is set to `memory.available<500Mi,nodefs.available<10%`

Under this scenario, 'Allocatable' will be 14.5 CPUs, 28.5Gi of memory and
`88Gi` of local storage.
Scheduler ensures that the total memory `requests` across all pods on this node does
not exceed 28.5Gi and storage doesn't exceed 88Gi.
Kubelet evicts pods whenever the overall memory usage across pods exceeds 28.5Gi,
or if overall disk usage exceeds 88Gi If all processes on the node consume as
much CPU as they can, pods together cannot consume more than 14.5 CPUs.

If `kube-reserved` and/or `system-reserved` is not enforced and system daemons
exceed their reservation, `kubelet` evicts pods whenever the overall node memory
usage is higher than 31.5Gi or `storage` is greater than 90Gi.

