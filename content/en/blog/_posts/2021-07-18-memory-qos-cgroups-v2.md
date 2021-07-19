---
layout: blog
title: 'Support memory qos with cgroups v2'
date: 2021-07-18
slug: memory-qos-cgroups-v2
---

**Authors:** Tim Xu (Tencent Cloud)

Memory QoS is used to memory protection and usage throttle on pod / container to increase memory isolation and service quality.

In traditional cgroups v1 in Kubernetes, cpu resources can be very well protected. Kubernetes uses `cpu_shares / cpu_set / cpu_quota / cpu_period` to isolate cpu. But the memory is not well guaranteed, especially at cgroup level. Kubernetes only uses `memory.limit_in_bytes=sum(pod.spec.containers.resources.limits[memory])` with cgroups v1 and `memory.max=sum(pod.spec.containers.resources.limits[memory])` with cgroups v2 to limit memory usage. `resources.requests[memory]` is not yet used neither by cgroups v1 nor cgroups v2 to protect memory requests. About memory protection, we use `oom_scores` to determine order of killing container process when OOM occurs.

It may cause:
- Pod / Container memory requests can't be fully reserved, page cache is at risk of being recycled
- Pod / Container memory allocation is not well protected, there may occur allocation latency frequently when node memory nearly runs out
- Memory overcommit of container is not throttled, there may increase risk of node memory pressure

Kubernetes 1.22 brings Memory QoS to alpha to pay attention on the quality of service of memory resources. It uses cgroup v2 new capabilities `memory.min / memory.high` in memory controller to retain memory requests and throttle overcommit limits. This feature can improve memory availability and reduce memory requests reclamation, which is of great significance to ensure the stability of both workloads and nodes.

## How does it work?
It uses two interfaces `memory.min / memory.high` of cgroup v2 memory controller to work.
| File | Description |
| -------- | -------- |
| memory.min | memory.min specifies a minimum amount of memory the cgroup must always retain, i.e., memory that can never be reclaimed by the system. If the cgroup's memory usage reaches this low limit and can’t be increased, the system OOM killer will be invoked. **We map it to `requests.memory`.** |
| memory.high | memory.high is the memory usage throttle limit. This is the main mechanism to control a cgroup's memory use. If a cgroup's memory use goes over the high boundary specified here, the cgroup’s processes are throttled and put under heavy reclaim pressure. The default is max, meaning there is no limit. **We use a formula to calculate `memory.high` depending on `limits.memory/node allocatable memory` and a memory throttling factor.** |

Both container and pod are considered. When cgroup v2 unified and MemoryQoS feature gate are both enabled, kubelet sets `requests.memory` to `memory.min` at container / pod level cgroup. And it also sets `memory.high` to throttle container memory overcommit allocation. 

![](https://i.imgur.com/FpR0cUK.png)

The formula is as follows:
```
// Container
/cgroup2/kubepods/pod<UID>/<container-id>/memory.min=pod.spec.containers[i].resources.requests[memory]
/cgroup2/kubepods/pod<UID>/<container-id>/memory.high=(pod.spec.containers[i].resources.limits[memory]/node allocatable memory)*memory throttling factor // Burstable
// Pod
/cgroup2/kubepods/pod<UID>/memory.min=sum(pod.spec.containers[i].resources.requests[memory])
// QoS ancestor cgroup
/cgroup2/kubepods/burstable/memory.min=sum(pod[i].spec.containers[j].resources.requests[memory])

```

Cgroup v2 memory controller would retain memory requests or throttle memory usages in the pod or container cgroup based on the set value. Because effective min boundary is limited by `memory.min` values of all ancestor cgroups, kubelet also sets qos or root cgroup if necessary.

## How do I use it?
All prerequisites must be met to enable the memory qos feature.

1. Kubernetes since v1.22
2. runc since v1.0.0-rc93, containerd since 1.14
3. Linux kernel minimum version: 4.15, recommended version: 5.2+
4. Kernel enables cgroups v2 unified hierarchy, add `systemd.unified_cgroup_hierarchy=1` to the kernel cmdline

After that, user can enable memory qos in feature gate, add `--feature-gates="...,MemoryQoS=true"` to kubelet flag.

## How can I learn more?

You can find more details as follows:
- KEPs
    - Memory QoS https://github.com/kubernetes/enhancements/tree/master/keps/sig-node/2570-memory-qos
    - Cgroup v2 https://github.com/kubernetes/enhancements/tree/master/keps/sig-node/2254-cgroup-v2
- PRs
    - Feature: add unified on CRI to support cgroup v2 https://github.com/kubernetes/kubernetes/pull/102578
    - Feature: Support memory qos with cgroups v2 https://github.com/kubernetes/kubernetes/pull/102970
## How do I get involved?
You can touch us through the community.
- Slack: [#sig-node](https://kubernetes.slack.com/messages/sig-node)
- [Mailing list](https://groups.google.com/forum/#!forum/kubernetes-sig-node)
- [Open Community Issues/PRs](https://github.com/kubernetes/community/labels/sig%2Fnode)

Or you can contact me directly.
- GH / Slack: xiaoxubeii
- Email: xiaoxubeii@gmail.com
