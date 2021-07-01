---
reviewers:
- derekwaynecarr
title: Process ID Limits And Reservations
content_type: concept
weight: 40
---

<!-- overview -->

{{< feature-state for_k8s_version="v1.20" state="stable" >}}

Kubernetes allow you to limit the number of process IDs (PIDs) that a
{{< glossary_tooltip term_id="Pod" text="Pod" >}} can use.
You can also reserve a number of allocatable PIDs for each {{< glossary_tooltip term_id="node" text="node" >}}
for use by the operating system and daemons (rather than by Pods).

<!-- body -->

Process IDs (PIDs) are a fundamental resource on nodes. It is trivial to hit the
task limit without hitting any other resource limits, which can then cause
instability to a host machine.

Cluster administrators require mechanisms to ensure that Pods running in the
cluster cannot induce PID exhaustion that prevents host daemons (such as the
{{< glossary_tooltip text="kubelet" term_id="kubelet" >}} or
{{< glossary_tooltip text="kube-proxy" term_id="kube-proxy" >}},
and potentially also the container runtime) from running.
In addition, it is important to ensure that PIDs are limited among Pods in order
to ensure they have limited impact on other workloads on the same node.

{{< note >}}
On certain Linux installations, the operating system sets the PIDs limit to a low default,
such as `32768`. Consider raising the value of `/proc/sys/kernel/pid_max`.
{{< /note >}}

You can configure a kubelet to limit the number of PIDs a given Pod can consume.
For example, if your node's host OS is set to use a maximum of `262144` PIDs and
expect to host less than `250` Pods, one can give each Pod a budget of `1000`
PIDs to prevent using up that node's overall number of available PIDs. If the
admin wants to overcommit PIDs similar to CPU or memory, they may do so as well
with some additional risks. Either way, a single Pod will not be able to bring
the whole machine down. This kind of resource limiting helps to prevent simple
fork bombs from affecting operation of an entire cluster.

Per-Pod PID limiting allows administrators to protect one Pod from another, but
does not ensure that all Pods scheduled onto that host are unable to impact the node overall.
Per-Pod limiting also does not protect the node agents themselves from PID exhaustion.

You can also reserve an amount of PIDs for node overhead, separate from the
allocation to Pods. This is similar to how you can reserve CPU, memory, or other
resources for use by the operating system and other facilities outside of Pods
and their containers.

PID limiting is a an important sibling to [compute
resource](/docs/concepts/configuration/manage-resources-containers/) requests
and limits. However, you specify it in a different way: rather than defining a
Pod's resource limit in the `.spec` for a Pod, you configure the limit as a
setting on the kubelet. Pod-defined PID limits are not currently supported.

{{< caution >}}
This means that the limit that applies to a Pod may be different depending on
where the Pod is scheduled. To make things simple, it's easiest if all Nodes use
the same PID resource limits and reservations.
{{< /caution >}}

## Node PID limits

Kubernetes allows you to reserve a number of process IDs for the system use. To
configure the reservation, use the parameter `pid=<number>` in the
`--system-reserved` and `--kube-reserved` command line options to the kubelet.
The value you specified declares that the specified number of process IDs will
be reserved for the system as a whole and for Kubernetes system daemons
respectively.

{{< note >}}
Before Kubernetes version 1.20, PID resource limiting with Node-level
reservations required enabling the [feature
gate](/docs/reference/command-line-tools-reference/feature-gates/)
`SupportNodePidsLimit` to work.
{{< /note >}}

## Pod PID limits

Kubernetes allows you to limit the number of processes running in a Pod. You
specify this limit at the node level, rather than configuring it as a resource
limit for a particular Pod. Each Node can have a different PID limit.  
To configure the limit, you can specify the command line parameter `--pod-max-pids`
to the kubelet, or set `PodPidsLimit` in the kubelet
[configuration file](/docs/tasks/administer-cluster/kubelet-config-file/).

{{< note >}}
Before Kubernetes version 1.20, PID resource limiting for Pods required enabling
the [feature gate](/docs/reference/command-line-tools-reference/feature-gates/)
`SupportPodPidsLimit` to work.
{{< /note >}}

## PID based eviction

You can configure kubelet to start terminating a Pod when it is misbehaving and consuming abnormal amount of resources.
This feature is called eviction. You can
[Configure Out of Resource Handling](/docs/concepts/scheduling-eviction/node-pressure-eviction/)
for various eviction signals.
Use `pid.available` eviction signal to configure the threshold for number of PIDs used by Pod.
You can set soft and hard eviction policies.
However, even with the hard eviction policy, if the number of PIDs growing very fast,
node can still get into unstable state by hitting the node PIDs limit.
Eviction signal value is calculated periodically and does NOT enforce the limit.

PID limiting - per Pod and per Node sets the hard limit.
Once the limit is hit, workload will start experiencing failures when trying to get a new PID.
It may or may not lead to rescheduling of a Pod,
depending on how workload reacts on these failures and how liveleness and readiness
probes are configured for the Pod. However, if limits were set correctly,
you can guarantee that other Pods workload and system processes will not run out of PIDs
when one Pod is misbehaving.

## {{% heading "whatsnext" %}}

- Refer to the [PID Limiting enhancement document](https://github.com/kubernetes/enhancements/blob/097b4d8276bc9564e56adf72505d43ce9bc5e9e8/keps/sig-node/20190129-pid-limiting.md) for more information.
- For historical context, read
  [Process ID Limiting for Stability Improvements in Kubernetes 1.14](/blog/2019/04/15/process-id-limiting-for-stability-improvements-in-kubernetes-1.14/).
- Read [Managing Resources for Containers](/docs/concepts/configuration/manage-resources-containers/).
- Learn how to [Configure Out of Resource Handling](/docs/concepts/scheduling-eviction/node-pressure-eviction/).
