---
title: Scheduling Policies
content_type: concept
weight: 10
---

<!-- overview -->

A scheduling Policy can be used to specify the *predicates* and *priorities*
that the {{< glossary_tooltip text="kube-scheduler" term_id="kube-scheduler" >}}
runs to [filter and score nodes](/docs/concepts/scheduling-eviction/kube-scheduler/#kube-scheduler-implementation),
respectively.

You can set a scheduling policy by running
`kube-scheduler --policy-config-file <filename>` or
`kube-scheduler --policy-configmap <ConfigMap>`
and using the [Policy type](/docs/reference/config-api/kube-scheduler-policy-config.v1/).

<!-- body -->

## Predicates

The following *predicates* implement filtering:

- `PodFitsHostPorts`: Checks if a Node has free ports (the network protocol kind)
  for the Pod ports the Pod is requesting.

- `PodFitsHost`: Checks if a Pod specifies a specific Node by its hostname.

- `PodFitsResources`: Checks if the Node has free resources (eg, CPU and Memory)
  to meet the requirement of the Pod.

- `MatchNodeSelector`: Checks if a Pod's Node {{< glossary_tooltip term_id="selector" >}}
   matches the Node's {{< glossary_tooltip text="label(s)" term_id="label" >}}.

- `NoVolumeZoneConflict`: Evaluate if the {{< glossary_tooltip text="Volumes" term_id="volume" >}}
  that a Pod requests are available on the Node, given the failure zone restrictions for
  that storage.

- `NoDiskConflict`: Evaluates if a Pod can fit on a Node due to the volumes it requests,
   and those that are already mounted.

- `MaxCSIVolumeCount`: Decides how many {{< glossary_tooltip text="CSI" term_id="csi" >}}
  volumes should be attached, and whether that's over a configured limit.

- `PodToleratesNodeTaints`: checks if a Pod's {{< glossary_tooltip text="tolerations" term_id="toleration" >}}
  can tolerate the Node's {{< glossary_tooltip text="taints" term_id="taint" >}}.

- `CheckVolumeBinding`: Evaluates if a Pod can fit due to the volumes it requests.
  This applies for both bound and unbound
  {{< glossary_tooltip text="PVCs" term_id="persistent-volume-claim" >}}.

## Priorities

The following *priorities* implement scoring:

- `SelectorSpreadPriority`: Spreads Pods across hosts, considering Pods that
   belong to the same {{< glossary_tooltip text="Service" term_id="service" >}},
   {{< glossary_tooltip term_id="statefulset" >}} or
   {{< glossary_tooltip term_id="replica-set" >}}.

- `InterPodAffinityPriority`: Implements preferred
  [inter pod affininity and antiaffinity](/docs/concepts/scheduling-eviction/assign-pod-node/#inter-pod-affinity-and-anti-affinity).

- `LeastRequestedPriority`: Favors nodes with fewer requested resources. In other
  words, the more Pods that are placed on a Node, and the more resources those
  Pods use, the lower the ranking this policy will give.

- `MostRequestedPriority`: Favors nodes with most requested resources. This policy
  will fit the scheduled Pods onto the smallest number of Nodes needed to run your
  overall set of workloads.

- `RequestedToCapacityRatioPriority`: Creates a requestedToCapacity based ResourceAllocationPriority using default resource scoring function shape.

- `BalancedResourceAllocation`: Favors nodes with balanced resource usage.

- `NodePreferAvoidPodsPriority`: Prioritizes nodes according to the node annotation
  `scheduler.alpha.kubernetes.io/preferAvoidPods`. You can use this to hint that
  two different Pods shouldn't run on the same Node.

- `NodeAffinityPriority`: Prioritizes nodes according to node affinity scheduling
   preferences indicated in PreferredDuringSchedulingIgnoredDuringExecution.
   You can read more about this in [Assigning Pods to Nodes](/docs/concepts/scheduling-eviction/assign-pod-node/).

- `TaintTolerationPriority`: Prepares the priority list for all the nodes, based on
  the number of intolerable taints on the node. This policy adjusts a node's rank
  taking that list into account.

- `ImageLocalityPriority`: Favors nodes that already have the
  {{< glossary_tooltip text="container images" term_id="image" >}} for that
  Pod cached locally.

- `ServiceSpreadingPriority`: For a given Service, this policy aims to make sure that
  the Pods for the Service run on different nodes. It favours scheduling onto nodes
  that don't have Pods for the service already assigned there. The overall outcome is
  that the Service becomes more resilient to a single Node failure.

- `EqualPriority`: Gives an equal weight of one to all nodes.

- `EvenPodsSpreadPriority`: Implements preferred
  [pod topology spread constraints](/docs/concepts/workloads/pods/pod-topology-spread-constraints/).

## {{% heading "whatsnext" %}}

* Learn about [scheduling](/docs/concepts/scheduling-eviction/kube-scheduler/)
* Learn about [kube-scheduler Configuration](/docs/reference/scheduling/config/)
* Read the [kube-scheduler configuration reference (v1beta2)](/docs/reference/config-api/kube-scheduler-config.v1beta2)
* Read the [kube-scheduler Policy reference (v1)](/docs/reference/config-api/kube-scheduler-policy-config.v1/)

