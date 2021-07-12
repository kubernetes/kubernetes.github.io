---
layout: blog
title: 'Pod Priority and Preemption in Kubernetes'
date: 2019-04-16
---

**Author**: Bobby Salamat

Kubernetes is well-known for running scalable workloads. It scales your workloads based on their resource usage. When a workload is scaled up, more instances of the application get created. When the application is critical for your product, you want to make sure that these new instances are scheduled even when your cluster is under resource pressure. One obvious solution to this problem is to over-provision your cluster resources to have some amount of slack resources available for scale-up situations. This approach often works, but costs more as you would have to pay for the resources that are idle most of the time.

[Pod priority and preemption](/docs/concepts/scheduling-eviction/pod-priority-preemption/) is a scheduler feature made generally available in Kubernetes 1.14 that allows you to achieve high levels of scheduling confidence for your critical workloads without overprovisioning your clusters. It also provides a way to improve resource utilization in your clusters without sacrificing the reliability of your essential workloads.

## Guaranteed scheduling with controlled cost

[Kubernetes Cluster Autoscaler](https://github.com/kubernetes/autoscaler/) is an excellent tool in the ecosystem which adds more nodes to your cluster when your applications need them. However, cluster autoscaler has some limitations and may not work for all users:

- It does not work in physical clusters.
- Adding more nodes to the cluster costs more.
- Adding nodes is not instantaneous and could take minutes before those nodes become available for scheduling.

An alternative is Pod Priority and Preemption. In this approach, you combine multiple workloads in a single cluster. For example, you may run your CI/CD pipeline, ML workloads, and your critical service in the same cluster. When multiple workloads run in the same cluster, the size of your cluster is larger than a cluster that you would use to run only your critical service. If you give your critical service the highest priority and your CI/CD and ML workloads lower priority, when your service needs more computing resources, the scheduler preempts (evicts) enough pods of your lower priority workloads, e.g., ML workload, to allow all your higher priority pods to schedule.

With pod priority and preemption you can set a maximum size for your cluster in the Autoscaler configuration to ensure your costs get controlled without sacrificing availability of your service. Moreover, preemption is much faster than adding new nodes to the cluster. Within seconds your high priority pods are scheduled, which is critical for latency sensitive services.

## Improve cluster resource utilization

Cluster operators who run critical services learn over time a rough estimate of the number of nodes that they need in their clusters to achieve high service availability. The estimate is usually conservative. Such estimates take bursts of traffic into account to find the number of required nodes. Cluster autoscaler can be configured never to reduce the size of the cluster below this level. The only problem is that such estimates are often conservative and cluster resources may remain underutilized most of the time. Pod priority and preemption allows you to improve resource utilization significantly by running a non-critical workload in the cluster.

The non-critical workload may have many more pods that can fit in the cluster. If you give a negative priority to your non-critical workload, Cluster Autoscaler does not add more nodes to your cluster when the non-critical pods are pending. Therefore, you won’t incur higher expenses. When your critical workload requires more computing resources, the scheduler preempts non-critical pods and schedules critical ones.

The non-critical pods fill the “holes” in your cluster resources which improves resource utilization without raising your costs.

## Get Involved

If you have feedback for this feature or are interested in getting involved with the design and development, join the [Scheduling Special Interest Group](https://github.com/kubernetes/community/tree/master/sig-scheduling). 
