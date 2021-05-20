---
reviewers:
- derekwaynecarr
- vishh
- timstclair
title: Configure Out of Resource Handling
content_type: concept
---

<!-- overview -->

This page explains how to configure out of resource handling with `kubelet`.

The `kubelet` needs to preserve node stability when available compute resources
are low. This is especially important when dealing with incompressible
compute resources, such as memory or disk space. If such resources are exhausted,
nodes become unstable.

<!-- body -->

### Eviction Signals

The `kubelet` supports eviction decisions based on the signals described in the following
table. The value of each signal is described in the Description column, which is based on
the `kubelet` summary API.

| Eviction Signal      | Description                                                                           |
|----------------------|---------------------------------------------------------------------------------------|
| `memory.available`   | `memory.available` := `node.status.capacity[memory]` - `node.stats.memory.workingSet` |
| `nodefs.available`   | `nodefs.available` := `node.stats.fs.available`                                       |
| `nodefs.inodesFree`  | `nodefs.inodesFree` := `node.stats.fs.inodesFree`                                     |
| `imagefs.available`  | `imagefs.available` := `node.stats.runtime.imagefs.available`                         |
| `imagefs.inodesFree` | `imagefs.inodesFree` := `node.stats.runtime.imagefs.inodesFree`                       |
| `pid.available`      | `pid.available` := `node.stats.rlimit.maxpid` - `node.stats.rlimit.curproc`           |

Each of the above signals supports either a literal or percentage based value.
The percentage based value is calculated relative to the total capacity
associated with each signal.

The value for `memory.available` is derived from the cgroupfs instead of tools
like `free -m`. This is important because `free -m` does not work in a
container, and if users use the [node
allocatable](/docs/tasks/administer-cluster/reserve-compute-resources/#node-allocatable) feature, out of resource decisions
are made local to the end user Pod part of the cgroup hierarchy as well as the
root node. This [script](/examples/admin/resource/memory-available.sh)
reproduces the same set of steps that the `kubelet` performs to calculate
`memory.available`. The `kubelet` excludes inactive_file (i.e. # of bytes of
file-backed memory on inactive LRU list) from its calculation as it assumes that
memory is reclaimable under pressure.

`kubelet` supports only two filesystem partitions.

1. The `nodefs` filesystem that kubelet uses for volumes, daemon logs, etc.
1. The `imagefs` filesystem that container runtimes uses for storing images and
   container writable layers.

`imagefs` is optional. `kubelet` auto-discovers these filesystems using
cAdvisor. `kubelet` does not care about any other filesystems. Any other types
of configurations are not currently supported by the kubelet. For example, it is
_not OK_ to store volumes and logs in a dedicated `filesystem`.

In future releases, the `kubelet` will deprecate the existing [garbage
collection](/docs/concepts/cluster-administration/kubelet-garbage-collection/)
support in favor of eviction in response to disk pressure.

### Eviction Thresholds

The `kubelet` supports the ability to specify eviction thresholds that trigger the `kubelet` to reclaim resources.

Each threshold has the following form:

`[eviction-signal][operator][quantity]`

where:

* `eviction-signal` is an eviction signal token as defined in the previous table.
* `operator` is the desired relational operator, such as `<` (less than).
* `quantity` is the eviction threshold quantity, such as `1Gi`. These tokens must match the quantity representation used by Kubernetes. An eviction threshold can also be expressed as a percentage using the `%` token.

For example, if a node has `10Gi` of total memory and you want trigger eviction if
the available memory falls below `1Gi`, you can define the eviction threshold as
either `memory.available<10%` or `memory.available<1Gi`. You cannot use both.

#### Soft Eviction Thresholds

A soft eviction threshold pairs an eviction threshold with a required
administrator-specified grace period. No action is taken by the `kubelet`
to reclaim resources associated with the eviction signal until that grace
period has been exceeded. If no grace period is provided, the `kubelet`
returns an error on startup.

In addition, if a soft eviction threshold has been met, an operator can
specify a maximum allowed Pod termination grace period to use when evicting
pods from the node. If specified, the `kubelet` uses the lesser value among
the `pod.Spec.TerminationGracePeriodSeconds` and the max allowed grace period.
If not specified, the `kubelet` kills Pods immediately with no graceful
termination.

To configure soft eviction thresholds, the following flags are supported:

* `eviction-soft` describes a set of eviction thresholds (e.g. `memory.available<1.5Gi`) that if met over a corresponding grace period would trigger a Pod eviction.
* `eviction-soft-grace-period` describes a set of eviction grace periods (e.g. `memory.available=1m30s`) that correspond to how long a soft eviction threshold must hold before triggering a Pod eviction.
* `eviction-max-pod-grace-period` describes the maximum allowed grace period (in seconds) to use when terminating pods in response to a soft eviction threshold being met.

#### Hard Eviction Thresholds

A hard eviction threshold has no grace period, and if observed, the `kubelet`
will take immediate action to reclaim the associated starved resource. If a
hard eviction threshold is met, the `kubelet` kills the Pod immediately
with no graceful termination.

To configure hard eviction thresholds, the following flag is supported:

* `eviction-hard` describes a set of eviction thresholds (e.g. `memory.available<1Gi`) that if met would trigger a Pod eviction.

The `kubelet` has the following default hard eviction threshold:

* `memory.available<100Mi`
* `nodefs.available<10%`
* `imagefs.available<15%`

On a Linux node, the default value also includes `nodefs.inodesFree<5%`.

### Eviction Monitoring Interval

The `kubelet` evaluates eviction thresholds per its configured housekeeping interval.

* `housekeeping-interval` is the interval between container housekeepings which defaults to `10s`.

### Node Conditions

The `kubelet` maps one or more eviction signals to a corresponding node condition.

If a hard eviction threshold has been met, or a soft eviction threshold has been met
independent of its associated grace period, the `kubelet` reports a condition that
reflects the node is under pressure.

The following node conditions are defined that correspond to the specified eviction signal.

| Node Condition    | Eviction Signal                                                                       | Description                                                                                                                  |
|-------------------|---------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------|
| `MemoryPressure`  | `memory.available`                                                                    | Available memory on the node has satisfied an eviction threshold                                                             |
| `DiskPressure`    | `nodefs.available`, `nodefs.inodesFree`, `imagefs.available`, or `imagefs.inodesFree` | Available disk space and inodes on either the node's root filesystem or image filesystem has satisfied an eviction threshold |
| `PIDPressure`     | `pid.available`                                                                       | Available processes identifiers on the (Linux) node has fallen below an eviction threshold                                   |                                                         |

The `kubelet` continues to report node status updates at the frequency specified by
`--node-status-update-frequency` which defaults to `10s`.

### Oscillation of node conditions

If a node is oscillating above and below a soft eviction threshold, but not exceeding
its associated grace period, it would cause the corresponding node condition to
constantly oscillate between true and false, and could cause poor scheduling decisions
as a consequence.

To protect against this oscillation, the following flag is defined to control how
long the `kubelet` must wait before transitioning out of a pressure condition.

* `eviction-pressure-transition-period` is the duration for which the `kubelet` has to wait before transitioning out of an eviction pressure condition.

The `kubelet` would ensure that it has not observed an eviction threshold being met
for the specified pressure condition for the period specified before toggling the
condition back to `false`.

### Reclaiming node level resources

If an eviction threshold has been met and the grace period has passed,
the `kubelet` initiates the process of reclaiming the pressured resource
until it has observed the signal has gone below its defined threshold.

The `kubelet` attempts to reclaim node level resources prior to evicting end-user Pods. If
disk pressure is observed, the `kubelet` reclaims node level resources differently if the
machine has a dedicated `imagefs` configured for the container runtime.

#### With `imagefs`

If `nodefs` filesystem has met eviction thresholds, `kubelet` frees up disk space by deleting the dead Pods and their containers.

If `imagefs` filesystem has met eviction thresholds, `kubelet` frees up disk space by deleting all unused images.

#### Without `imagefs`

If `nodefs` filesystem has met eviction thresholds, `kubelet` frees up disk space in the following order:

1. Delete dead Pods and their containers
1. Delete all unused images

### Evicting end-user Pods

If the `kubelet` is unable to reclaim sufficient resource on the node, `kubelet` begins evicting Pods.

The `kubelet` ranks Pods for eviction first by whether or not their usage of the starved resource exceeds requests,
then by [Priority](/docs/concepts/configuration/pod-priority-preemption/), and then by the consumption of the starved compute resource relative to the Pods' scheduling requests.

As a result, `kubelet` ranks and evicts Pods in the following order:

* Pods violating the requests for the resource being starved. Any pod in violation of the starved resource gets grouped here - this includes Pods that have no request set for that resource.

* Pods are then ranked by priority, lowest being grouped first.

* Lastly, Pods are ranked by their consumption of the starved resource relative to it's requests.

If necessary, `kubelet` evicts Pods one at a time to reclaim disk when `DiskPressure`
is encountered. `Kubelet` checks after each eviction to see if the condition is still true. This process continues through the pods in the lowest-priority group that is in violation of the request, moving on to the next priority if needed.

> It's important to ensure that critical pods contain appropriately set requests and limits for CPU, Memory, and ephemeral-storage to avoid scenarios where critical Pods may unexpectedly get evicted. 

If the `kubelet` is responding to `inode` starvation, it reclaims
`inodes` by evicting Pods with the lowest quality of service first. If the `kubelet`
is responding to lack of available disk, it ranks Pods within a quality of service
that consumes the largest amount of disk and kills those first.

#### With `imagefs`

If `nodefs` is triggering evictions, `kubelet` sorts Pods based on the usage on `nodefs`

- local volumes + logs of all its containers.

If `imagefs` is triggering evictions, `kubelet` sorts Pods based on the writable layer usage of all its containers.

#### Without `imagefs`

If `nodefs` is triggering evictions, `kubelet` sorts Pods based on their total disk usage

- local volumes + logs & writable layer of all its containers.

### Minimum eviction reclaim

In certain scenarios, eviction of Pods could result in reclamation of small amount of resources. This can result in
`kubelet` hitting eviction thresholds in repeated successions. In addition to that, eviction of resources like `disk`, is time consuming.

To mitigate these issues, `kubelet` can have a per-resource `minimum-reclaim`. Whenever `kubelet` observes
resource pressure, `kubelet` attempts to reclaim at least `minimum-reclaim` amount of resource below
the configured eviction threshold.

For example, with the following configuration:

```
--eviction-hard=memory.available<500Mi,nodefs.available<1Gi,imagefs.available<100Gi
--eviction-minimum-reclaim="memory.available=0Mi,nodefs.available=500Mi,imagefs.available=2Gi"`
```

If an eviction threshold is triggered for `memory.available`, the `kubelet` works to ensure
that `memory.available` is at least `500Mi`. For `nodefs.available`, the `kubelet` works
to ensure that `nodefs.available` is at least `1.5Gi`, and for `imagefs.available` it
works to ensure that `imagefs.available` is at least `102Gi` before no longer reporting pressure
on their associated resources.

The default `eviction-minimum-reclaim` is `0` for all resources.

### Scheduler

The node reports a condition when a compute resource is under pressure. The
scheduler views that condition as a signal to dissuade placing additional
pods on the node.

| Node Condition    | Scheduler Behavior                                  |
| ------------------| ----------------------------------------------------|
| `MemoryPressure`  | No new `BestEffort` Pods are scheduled to the node. |
| `DiskPressure`    | No new Pods are scheduled to the node.              |

## Node OOM Behavior

If the node experiences a system OOM (out of memory) event prior to the `kubelet` being able to reclaim memory,
the node depends on the [oom_killer](https://lwn.net/Articles/391222/) to respond.

The `kubelet` sets a `oom_score_adj` value for each container based on the quality of service for the Pod.

| Quality of Service | oom_score_adj                                                                     |
|--------------------|-----------------------------------------------------------------------------------|
| `Guaranteed`       | -998                                                                              |
| `BestEffort`       | 1000                                                                              |
| `Burstable`        | min(max(2, 1000 - (1000 * memoryRequestBytes) / machineMemoryCapacityBytes), 999) |

If the `kubelet` is unable to reclaim memory prior to a node experiencing system OOM, the `oom_killer` calculates
an `oom_score` based on the percentage of memory it's using on the node, and then add the `oom_score_adj` to get an
effective `oom_score` for the container, and then kills the container with the highest score.

The intended behavior should be that containers with the lowest quality of service that
are consuming the largest amount of memory relative to the scheduling request should be killed first in order
to reclaim memory.

Unlike Pod eviction, if a Pod container is OOM killed, it may be restarted by the `kubelet` based on its `RestartPolicy`.

## Best Practices

The following sections describe best practices for out of resource handling.

### Schedulable resources and eviction policies

Consider the following scenario:

* Node memory capacity: `10Gi`
* Operator wants to reserve 10% of memory capacity for system daemons (kernel, `kubelet`, etc.)
* Operator wants to evict Pods at 95% memory utilization to reduce incidence of system OOM.

To facilitate this scenario, the `kubelet` would be launched as follows:

```
--eviction-hard=memory.available<500Mi
--system-reserved=memory=1.5Gi
```

Implicit in this configuration is the understanding that "System reserved" should include the amount of memory
covered by the eviction threshold.

To reach that capacity, either some Pod is using more than its request, or the system is using more than `1.5Gi - 500Mi = 1Gi`.

This configuration ensures that the scheduler does not place Pods on a node that immediately induce memory pressure
and trigger eviction assuming those Pods use less than their configured request.

### DaemonSet

As `Priority` is a key factor in the eviction strategy, if you do not want pods belonging to a `DaemonSet` to be evicted, specify a sufficiently high priorityClass in the pod spec template. If you want pods belonging to a `DaemonSet` to run only if there are sufficient resources, specify a lower or default priorityClass.


## Deprecation of existing feature flags to reclaim disk

`kubelet` has been freeing up disk space on demand to keep the node stable.

As disk based eviction matures, the following `kubelet` flags are marked for deprecation
in favor of the simpler configuration supported around eviction.

| Existing Flag                              | New Flag                                |
| ------------------------------------------ | ----------------------------------------|
| `--image-gc-high-threshold`                | `--eviction-hard` or `eviction-soft`    |
| `--image-gc-low-threshold`                 | `--eviction-minimum-reclaim`            |
| `--maximum-dead-containers`                | deprecated                              |
| `--maximum-dead-containers-per-container`  | deprecated                              |
| `--minimum-container-ttl-duration`         | deprecated                              |
| `--low-diskspace-threshold-mb`             | `--eviction-hard` or `eviction-soft`    |
| `--outofdisk-transition-frequency`         | `--eviction-pressure-transition-period` |

## Known issues

The following sections describe known issues related to out of resource handling.

### kubelet may not observe memory pressure right away

The `kubelet` currently polls `cAdvisor` to collect memory usage stats at a regular interval. If memory usage
increases within that window rapidly, the `kubelet` may not observe `MemoryPressure` fast enough, and the `OOMKiller`
will still be invoked. We intend to integrate with the `memcg` notification API in a future release to reduce this
latency, and instead have the kernel tell us when a threshold has been crossed immediately.

If you are not trying to achieve extreme utilization, but a sensible measure of overcommit, a viable workaround for
this issue is to set eviction thresholds at approximately 75% capacity. This increases the ability of this feature
to prevent system OOMs, and promote eviction of workloads so cluster state can rebalance.

### kubelet may evict more Pods than needed

The Pod eviction may evict more Pods than needed due to stats collection timing gap. This can be mitigated by adding
the ability to get root container stats on an on-demand basis [(https://github.com/google/cadvisor/issues/1247)](https://github.com/google/cadvisor/issues/1247) in the future.

### active_file memory is not considered as available memory

On Linux, the kernel tracks the number of bytes of file-backed memory on active LRU list as the `active_file` statistic. The kubelet treats `active_file` memory areas as not reclaimable. For workloads that make intensive use of block-backed local storage, including ephemeral local storage, kernel-level caches of file and block data means that many recently accessed cache pages are likely to be counted as `active_file`. If enough of these kernel block buffers are on the active LRU list, the kubelet is liable to observe this as high resource use and taint the node as experiencing memory pressure - triggering Pod eviction.

For more more details, see [https://github.com/kubernetes/kubernetes/issues/43916](https://github.com/kubernetes/kubernetes/issues/43916)

You can work around that behavior by setting the memory limit and memory request the same for containers likely to perform intensive I/O activity. You will need to estimate or measure an optimal memory limit value for that container.

