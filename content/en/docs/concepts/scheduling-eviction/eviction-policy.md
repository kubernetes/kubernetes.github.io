---
title: Eviction Policy
content_type: concept
weight: 60
---

<!-- overview -->

{{< glossary_definition term_id="eviction" length="all" prepend="In Kubernetes, ">}}

<!-- body -->

## Eviction due to resource constraints

The {{< glossary_tooltip text="kubelet" term_id="kubelet" >}} proactively monitors for
and prevents total starvation of PIDs, memory, or filesystem storage. In those cases, the `kubelet` can reclaim
the starved resource by failing one or more Pods. When the `kubelet` fails
a Pod, it terminates all of its containers and transitions its `PodPhase` to `Failed`.
If the evicted Pod is managed by a Deployment, the Deployment creates another Pod
to be scheduled by Kubernetes.

A number of other control plane features and logic affect how and when pods are evicted, including:

* [Eviction thresholds](/docs/tasks/administer-cluster/out-of-resource/#eviction-thresholds), which define the triggers at which the kubelet starts to reclaim resources
* [Quality of Service for Pods](/docs/tasks/configure-pod-container/quality-service-pod/), which is a set of classes for Pods that effect how and when they are evicted. Pods are evicted in the following order:
  * Pods that are assigned with the `BestEffort` class 
  * Pods that are assigned the `Burstable` class and are using *more* of the starved resources than they requested
  * Pods that are assigned the `Burstable` class and are using *less* of the starved resources than they requested
  * Pods assigned with the `Guaranteed` class
* [Pod resource requests and limits](/docs/tasks/configure-pod-container/assign-memory-resource/), which plays a part in defining the Quality of Service class that is assigned to a Pod, which in turn affects the priority order of eviction 
* [Preemption](/docs/concepts/configuration/pod-priority-preemption/#preemption), which as the name suggests is the preemptive eviction of one or more pods to allow for the scheduling of a higher-priority pod and the avoidance of the resource starvation.

## Eviction due to a specific request

As well as being triggered due to resource constraints, evictions can also be triggered by a {{< glossary_tooltip term_id="cluster-operator" >}} or client application.

If you need to perform maintenance on a node, you can safely evict all the pods running on that node using the [kubectl drain](/docs/reference/generated/kubectl/kubectl-commands#drain) command.

If you prefer not to use kubectl drain (such as to avoid calling to an external command, or to get finer control over the pod eviction process), you can also programmatically cause evictions using the [eviction API](/docs/tasks/administer-cluster/safely-drain-node/#eviction-api).


## {{% heading "whatsnext" %}}

- Learn how to [safely drain a node](/docs/tasks/administer-cluster/safely-drain-node)
- Learn how to [configure out of resource handling](/docs/tasks/administer-cluster/out-of-resource/) with eviction signals and thresholds.
- Learn how to [configure Pod resource requests and limits](/docs/tasks/configure-pod-container/assign-memory-resource/)
- Learn how to [configure Quality of Service for Pods](/docs/tasks/configure-pod-container/quality-service-pod/)
