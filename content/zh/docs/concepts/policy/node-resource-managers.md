---
title: 节点资源管理器
content_type: concept
weight: 50
---
<!-- 
---
reviewers:
- derekwaynecarr
- klueska
title: Node Resource Managers 
content_type: concept
weight: 50
---
-->

<!-- overview -->

<!-- 
In order to support latency-critical and high-throughput workloads, Kubernetes offers a suite of Resource Managers. The managers aim to co-ordinate and optimise node's resources alignment for pods configured with a specific requirement for CPUs, devices, and memory (hugepages) resources. 
-->
Kubernetes 提供了一组资源管理器，用于支持延迟敏感的、高吞吐量的工作负载。
资源管理器的目标是协调和优化节点资源，以支持对 CPU、设备和内存（巨页）等资源有特殊需求的 Pod。

<!-- body -->

<!-- 
The main manager, the Topology Manager, is a Kubelet component that co-ordinates the overall resource management process through its [policy](/docs/tasks/administer-cluster/topology-manager/).

The configuration of individual managers is elaborated in dedicated documents:
-->
主管理器，也叫拓扑管理器（Topology Manager），是一个 Kubelet 组件，
它通过[策略](/zh/docs/tasks/administer-cluster/topology-manager/)，
协调全局的资源管理过程。

各个管理器的配置方式会在专项文档中详细阐述：

<!-- 
- [CPU Manager Policies](/docs/tasks/administer-cluster/cpu-management-policies/)
- [Device Manager](/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/#device-plugin-integration-with-the-topology-manager)
- [Memory Manager Policies](/docs/tasks/administer-cluster/memory-manager/)
-->
- [CPU 管理器策略](/zh/docs/tasks/administer-cluster/cpu-management-policies/)
- [设备管理器](/zh/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/#device-plugin-integration-with-the-topology-manager)
- [内存管理器策略](/zh/docs/tasks/administer-cluster/memory-manager/)
