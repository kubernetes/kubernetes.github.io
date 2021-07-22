---
reviewers:
- bsalamat
title: Scheduler Performance Tuning
content_type: concept
weight: 100
---

<!-- overview -->

{{< feature-state for_k8s_version="v1.14" state="beta" >}}

[kube-scheduler](/docs/concepts/scheduling-eviction/kube-scheduler/#kube-scheduler)
is the Kubernetes default scheduler. It is responsible for placement of Pods
on Nodes in a cluster.

Nodes in a cluster that meet the scheduling requirements of a Pod are
called _feasible_ Nodes for the Pod. The scheduler finds feasible Nodes
for a Pod and then runs a set of functions to score the feasible Nodes,
picking a Node with the highest score among the feasible ones to run
the Pod. The scheduler then notifies the API server about this decision
in a process called _Binding_.

This page explains performance tuning optimizations that are relevant for
large Kubernetes clusters.

<!-- body -->

In large clusters, you can tune the scheduler's behaviour balancing
scheduling outcomes between latency (new Pods are placed quickly) and
accuracy (the scheduler rarely makes poor placement decisions).

You configure this tuning setting via kube-scheduler setting
`percentageOfNodesToScore`. This KubeSchedulerConfiguration setting determines
a threshold for scheduling nodes in your cluster.

### Setting the threshold

The `percentageOfNodesToScore` option accepts whole numeric values between 0
and 100. The value 0 is a special number which indicates that the kube-scheduler
should use its compiled-in default.
If you set `percentageOfNodesToScore` above 100, kube-scheduler acts as if you
had set a value of 100.

To change the value, edit the
[kube-scheduler configuration file](/docs/reference/config-api/kube-scheduler-config.v1beta2/)
and then restart the scheduler.
In many cases, the configuration file can be found at `/etc/kubernetes/config/kube-scheduler.yaml`.

After you have made this change, you can run

```bash
kubectl get pods -n kube-system | grep kube-scheduler
```

to verify that the kube-scheduler component is healthy.

## Node scoring threshold {#percentage-of-nodes-to-score}

To improve scheduling performance, the kube-scheduler can stop looking for
feasible nodes once it has found enough of them. In large clusters, this saves
time compared to a naive approach that would consider every node.

You specify a threshold for how many nodes are enough, as a whole number percentage
of all the nodes in your cluster. The kube-scheduler converts this into an
integer number of nodes. During scheduling, if the kube-scheduler has identified
enough feasible nodes to exceed the configured percentage, the kube-scheduler
stops searching for more feasible nodes and moves on to the
[scoring phase](/docs/concepts/scheduling-eviction/kube-scheduler/#kube-scheduler-implementation).

[How the scheduler iterates over Nodes](#how-the-scheduler-iterates-over-nodes)
describes the process in detail.

### Default threshold

If you don't specify a threshold, Kubernetes calculates a figure using a
linear formula that yields 50% for a 100-node cluster and yields 10%
for a 5000-node cluster. The lower bound for the automatic value is 5%.

This means that, the kube-scheduler always scores at least 5% of your cluster no
matter how large the cluster is, unless you have explicitly set
`percentageOfNodesToScore` to be smaller than 5.

If you want the scheduler to score all nodes in your cluster, set
`percentageOfNodesToScore` to 100.

## Example

Below is an example configuration that sets `percentageOfNodesToScore` to 50%.

```yaml
apiVersion: kubescheduler.config.k8s.io/v1alpha1
kind: KubeSchedulerConfiguration
algorithmSource:
  provider: DefaultProvider

...

percentageOfNodesToScore: 50
```

## Tuning percentageOfNodesToScore

`percentageOfNodesToScore` must be a value between 1 and 100 with the default
value being calculated based on the cluster size. There is also a hardcoded
minimum value of 50 nodes.

{{< note >}}In clusters with less than 50 feasible nodes, the scheduler still
checks all the nodes because there are not enough feasible nodes to stop
the scheduler's search early.

In a small cluster, if you set a low value for `percentageOfNodesToScore`, your
change will have no or little effect, for a similar reason.

If your cluster has several hundred Nodes or fewer, leave this configuration option
at its default value. Making changes is unlikely to improve the
scheduler's performance significantly.
{{< /note >}}

An important detail to consider when setting this value is that when a smaller
number of nodes in a cluster are checked for feasibility, some nodes are not
sent to be scored for a given Pod. As a result, a Node which could possibly
score a higher value for running the given Pod might not even be passed to the
scoring phase. This would result in a less than ideal placement of the Pod.

You should avoid setting `percentageOfNodesToScore` very low so that kube-scheduler
does not make frequent, poor Pod placement decisions. Avoid setting the
percentage to anything below 10%, unless the scheduler's throughput is critical
for your application and the score of nodes is not important. In other words, you
prefer to run the Pod on any Node as long as it is feasible.

## How the scheduler iterates over Nodes

This section is intended for those who want to understand the internal details
of this feature.

In order to give all the Nodes in a cluster a fair chance of being considered
for running Pods, the scheduler iterates over the nodes in a round robin
fashion. You can imagine that Nodes are in an array. The scheduler starts from
the start of the array and checks feasibility of the nodes until it finds enough
Nodes as specified by `percentageOfNodesToScore`. For the next Pod, the
scheduler continues from the point in the Node array that it stopped at when
checking feasibility of Nodes for the previous Pod.

If Nodes are in multiple zones, the scheduler iterates over Nodes in various
zones to ensure that Nodes from different zones are considered in the
feasibility checks. As an example, consider six nodes in two zones:

```
Zone 1: Node 1, Node 2, Node 3, Node 4
Zone 2: Node 5, Node 6
```

The Scheduler evaluates feasibility of the nodes in this order:

```
Node 1, Node 5, Node 2, Node 6, Node 3, Node 4
```

After going over all the Nodes, it goes back to Node 1.

## {{% heading "whatsnext" %}}

* Check the [kube-scheduler configuration reference (v1beta2)](/docs/reference/config-api/kube-scheduler-config.v1beta2/)

