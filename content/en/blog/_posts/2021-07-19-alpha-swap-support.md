---
layout: blog
title: 'New in Kubernetes v1.22: alpha support for using swap memory'
date: 2021-07-19
slug: run-nodes-with-swap-alpha
---

**Author:** Elana Hashman (Red Hat)

The 1.22 release introduced alpha support for configuring swap memory usage for
Kubernetes workloads on a per-node basis.

In prior releases, Kubernetes did not support the use of swap memory on Linux,
as it is difficult to provide guarantees and account for pod memory utilization
when swap is involved. As part of Kubernetes' earlier design, swap support was
considered out of scope, and a kubelet would by default fail to start if swap
was detected on a node.

However, there are a number of [use cases](https://github.com/kubernetes/enhancements/blob/9d127347773ad19894ca488ee04f1cd3af5774fc/keps/sig-node/2400-node-swap/README.md#user-stories)
that would benefit from Kubernetes nodes supporting swap, including  improved
node stability, better support for applications with high memory overhead but
smaller working sets, the use of memory-constrained devices, and memory
flexibility.

Hence, over the past two releases, [SIG Node](https://github.com/kubernetes/community/tree/master/sig-node#readme) has
been working to gather appropriate use cases and feedback, and propose a design
for adding swap support to nodes in a controlled, predictable manner so that
Kubernetes users can perform testing and provide data to continue building
cluster capabilities on top of swap. The alpha graduation of swap memory
support for nodes is our first milestone towards this goal!

## How does it work?

There are a number of possible ways that one could envision swap use on a node.
To keep the scope manageable for this initial implementation, when swap is
already provisioned and available on a node, [we have proposed](https://github.com/kubernetes/enhancements/blob/9d127347773ad19894ca488ee04f1cd3af5774fc/keps/sig-node/2400-node-swap/README.md#proposal)
the kubelet should be able to be configured such that:

- It can start with swap on.
- It will direct the CRI to allocate Kubernetes workloads zero swap memory by
  default.
- You can configure the kubelet to specify swap utilization for the entire node.

Swap configuration on a node is exposed to a cluster admin via the
[`memorySwap` in the KubeletConfiguration](/docs/reference/config-api/kubelet-config.v1beta1/).
As a cluster administrator, you can specify the node's behaviour in the
presence of swap memory by setting `memorySwap.swapBehavior`.

This is possible through the addition of a `memory_swap_limit_in_bytes` field
to the container runtime interface (CRI). The kubelet's config will control how
much swap memory the kubelet instructs the container runtime to allocate to
each container via the CRI. The container runtime will then write the swap
settings to the container level cgroup.

## How do I use it?

On a node where swap memory is already provisioned, Kubernetes use of swap on a
node can be enabled by enabling the `NodeSwap` feature gate on the kubelet, and
disabling the `failSwapOn` [configuration setting](/docs/reference/config-api/kubelet-config.v1beta1/#kubelet-config-k8s-io-v1beta1-KubeletConfiguration)
or the `--fail-swap-on` command line flag.

You can also optionally configure `memorySwap.swapBehavior` in order to
specify how a node will use swap memory. For example,

```yaml
memorySwap:
  swapBehavior: LimitedSwap
```

The available configuration options for `swapBehavior` are:

- `LimitedSwap` (default): Kubernetes workloads are limited in how much swap
  they can use. Workloads on the node not managed by Kubernetes can still swap.
- `UnlimitedSwap`: Kubernetes workloads can use as much swap memory as they
  request, up to the system limit.

If configuration for `memorySwap` is not specified and the feature gate is
enabled, by default the kubelet will apply the same behaviour as the
`LimitedSwap` setting.

The behaviour of the `LimitedSwap` setting depends if the node is running with
v1 or v2 of control groups (also known as "cgroups"):

- **cgroupsv1:** Kubernetes workloads can use any combination of memory and
  swap, up to the pod's memory limit, if set.
- **cgroupsv2:** Kubernetes workloads cannot use swap memory.

### Caveats

Having swap available on a system reduces predictability. Swap's performance is
worse than regular memory, sometimes by many orders of magnitude, which can
cause unexpected performance regressions. Furthermore, swap changes a system's
behaviour under memory pressure, and applications cannot directly control what
portions of their memory usage are swapped out. Since enabling swap permits
greater memory usage for workloads in Kubernetes that cannot be predictably
accounted for, it also increases the risk of noisy neighbours and unexpected
packing configurations, as the scheduler cannot account for swap memory usage.

Hence, we do not recommend the use of swap for certain performance-constrained
workloads. Cluster administrators and developers should benchmark their nodes
and applications before using swap in production scenarios, and [we need your
help](#how-do-i-get-involved) with that!

## Looking ahead

The Kubernetes 1.22 release introduces alpha support for swap memory on nodes,
and we will continue to work towards beta graduation in the 1.23 release. This
will include:

* Adding support for controlling swap consumption at the Pod level via cgroups.
   * This will include the ability to set a system-reserved quantity of swap
     from what kubelet detects on the host.
* Determining a set of metrics for node QoS in order to evaluate the
  performance and stabiliy of nodes with and without swap enabled.
* Collecting feedback from test user cases.
  * We will consider introducing new configuration modes for swap, such as a
    node-wide swap limit for workloads.

## How can I learn more?

You can review the current [documentation](https://kubernetes.io/docs/concepts/architecture/nodes/#swap-memory)
on the Kubernetes website.

For more information, and to assist with testing and provide feedback, please
see [KEP-2400](https://github.com/kubernetes/enhancements/issues/2400) and its
[design proposal](https://github.com/kubernetes/enhancements/blob/master/keps/sig-node/2400-node-swap/README.md).

## How do I get involved?

Your feedback is always welcome! SIG Node [meets regularly](https://github.com/kubernetes/community/tree/master/sig-node#meetings)
and [can be reached](https://github.com/kubernetes/community/tree/master/sig-node#contact)
via [Slack](https://slack.k8s.io/) (channel **#sig-node**), or the SIG's
[mailing list](https://groups.google.com/forum/#!forum/kubernetes-sig-node).
Feel free to reach out to me, Elana Hashman (**@ehashman** on Slack and GitHub)
if you'd like to help.
