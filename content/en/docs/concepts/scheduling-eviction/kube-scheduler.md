---
title: Kubernetes Scheduler
content_type: concept
weight: 10
---

<!-- overview -->

In Kubernetes, _scheduling_ refers to making sure that {{< glossary_tooltip text="Pods" term_id="pod" >}}
are matched to {{< glossary_tooltip text="Nodes" term_id="node" >}} so that
{{< glossary_tooltip term_id="kubelet" >}} can run them.

<!-- body -->

## Scheduling overview {#scheduling}

A scheduler watches for newly created Pods that have no Node assigned. For
every Pod that the scheduler discovers, the scheduler becomes responsible
for finding the best Node for that Pod to run on. The scheduler reaches
this placement decision taking into account the scheduling principles
described below.

If you want to understand why Pods are placed onto a particular Node,
or if you're planning to implement a custom scheduler yourself, this
page will help you learn about scheduling.

## kube-scheduler

[kube-scheduler](/docs/reference/command-line-tools-reference/kube-scheduler/)
is the default scheduler for Kubernetes and runs as part of the
{{< glossary_tooltip text="control plane" term_id="control-plane" >}}.
kube-scheduler is designed so that, if you want and need to, you can
write your own scheduling component and use that instead.

For every newly created pod or other unscheduled pods, kube-scheduler
selects an optimal node for them to run on. However, every container in
pods has different requirements for resources and every pod also has
different requirements. Therefore, existing nodes need to be filtered
according to the specific scheduling requirements.

In a cluster, Nodes that meet the scheduling requirements for a Pod
are called _feasible_ nodes. If none of the nodes are suitable, the pod
remains unscheduled until the scheduler is able to place it.

The scheduler finds feasible Nodes for a Pod and then runs a set of
functions to score the feasible Nodes and picks a Node with the highest
score among the feasible ones to run the Pod. The scheduler then notifies
the API server about this decision in a process called _binding_.

Factors that need taken into account for scheduling decisions include
individual and collective resource requirements, hardware / software /
policy constraints, affinity and anti-affinity specifications, data
locality, inter-workload interference, and so on.

### Node selection in kube-scheduler {#kube-scheduler-implementation}

kube-scheduler selects a node for the pod in a 2-step operation:

1. Filtering
1. Scoring

The _filtering_ step finds the set of Nodes where it's feasible to
schedule the Pod. For example, the PodFitsResources filter checks whether a
candidate Node has enough available resource to meet a Pod's specific
resource requests. After this step, the node list contains any suitable
Nodes; often, there will be more than one. If the list is empty, that
Pod isn't (yet) schedulable.

In the _scoring_ step, the scheduler ranks the remaining nodes to choose
the most suitable Pod placement. The scheduler assigns a score to each Node
that survived filtering, basing this score on the active scoring rules.

Finally, kube-scheduler assigns the Pod to the Node with the highest ranking.
If there is more than one node with equal scores, kube-scheduler selects
one of these at random.

There are two supported ways to configure the filtering and scoring behavior
of the scheduler:

1. [Scheduling Policies](/docs/reference/scheduling/policies) allow you to configure _Predicates_ for filtering and _Priorities_ for scoring.
1. [Scheduling Profiles](/docs/reference/scheduling/config/#profiles) allow you to configure Plugins that implement different scheduling stages, including: `QueueSort`, `Filter`, `Score`, `Bind`, `Reserve`, `Permit`, and others. You can also configure the kube-scheduler to run different profiles.

## {{% heading "whatsnext" %}}

* Read about [scheduler performance tuning](/docs/concepts/scheduling-eviction/scheduler-perf-tuning/)
* Read about [Pod topology spread constraints](/docs/concepts/workloads/pods/pod-topology-spread-constraints/)
* Read the [reference documentation](/docs/reference/command-line-tools-reference/kube-scheduler/) for kube-scheduler
* Read the [kube-scheduler config (v1beta2)](/docs/reference/config-api/kube-scheduler-config.v1beta2/) reference
* Learn about [configuring multiple schedulers](/docs/tasks/extend-kubernetes/configure-multiple-schedulers/)
* Learn about [topology management policies](/docs/tasks/administer-cluster/topology-manager/)
* Learn about [Pod Overhead](/docs/concepts/scheduling-eviction/pod-overhead/)
* Learn about scheduling of Pods that use volumes in:
  * [Volume Topology Support](/docs/concepts/storage/storage-classes/#volume-binding-mode)
  * [Storage Capacity Tracking](/docs/concepts/storage/storage-capacity/)
  * [Node-specific Volume Limits](/docs/concepts/storage/storage-limits/)

