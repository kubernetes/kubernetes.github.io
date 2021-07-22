---
layout: blog
title: "Kubernetes Memory manager moves to beta"
date: 2021-07-21
slug: kubernetes-1-22-feature-topoloy-manager-beta
---

# Memory manager moves to beta

The blog post describes the internals of the memory manager, a beta feature of Kubernetes 1.22. The **Memory Manager** is a component in the **kubelet** ecosystem proposed to enable the feature of guaranteed memory (and hugepages) allocation for pods in the Guaranteed QoS class.

This blog post covers:

1. Why do you need it?
2. The internal details of how the **MemoryManager** works
3. Current limitations of the **MemoryManager**
4. Future work for the **MemoryManager**

## Why do you need it?

To get the best performance and latency for the workload container, container CPUs, PCI devices, and memory should be aligned to the same NUMA node. The kubelet already provides a set of managers to align CPUs and PCI devices, but you did not have a way to align memory. By default, the kernel will try to allocate the memory from the same NUMA node where container CPUs are placed, but it can not guarantee it.

## How does it work?

The memory manager is doing two main things:
- provides the topology hint to the topology manager
- allocates the memory for containers and updates the state

The overall sequence of the Memory Manager

<p>
  <img src="/images/blog/2021-07-21-memory-manager-beta/MemoryManagerDiagram.png">
</p>

During the Admission phase:

1. During the admission, the **Kubelet** calling the **TopologyManager** `Admit()` method.
2. The **TopologyManager** is calling `GetTopologyHints()` for every hint provider including the **MemoryManager**.
3. The **MemoryManager** calculates all possible NUMA nodes combinations for every container inside the pod and returns hints to the **TopologyManager**.
4. The **TopologyManager** calls to `Allocate()` for every hint provider including the **MemoryManager**.
5. The **MemoryManager** allocates the memory under the state according to the hint that the **TopologyManager** chose.

During the creation phase:

1. The **Kubelet** calls `PreCreateContainer()`.
2. The **MemoryManager** get the NUMA nodes where it allocated the memory for the container and returns it to **Kubelet**.
3. The **Kubelet** creates the container via CRI with the spec updated according to the **MemoryManager** information.

### Let's talk about the configuration

By default, the **MemoryManager** runs with the `None` policy, meaning it will just relax and will not do anything. To enable the **MemoryManager**, you should provide two **Kubelet** flags:

- `--memory-manager-policy=Static`
- `--reserved-memory="<numaNodeID>:<resourceName>=<quantity>"`

It is clear what value you should set for the `--memory-manager-policy` parameter. But it does not 100% clear how you should configure the `--reserved-memory` parameter. To configure it correctly, you should follow two main rules:

- The amount of reserved memory for the `memory` resource must be greater than zero.
- The amount of reserved memory for the resource type must be equal to `kube-reserved + system-reserved + eviction-hard` for the resource.

<p>
  <img src="/images/blog/2021-07-21-memory-manager-beta/ReservedMemory.png">
</p>

## Current limitations

The 1.22 release and promotion to the beta brings along some enhancements and fixes, but the **MemoryManager** still has several limitations.

### Single vs Cross NUMA node allocation

The NUMA node can not have both single and cross NUMA node allocations. When the container memory is pinned to two or more NUMA nodes, we can not know from which NUMA node the container will consume the memory.

<p>
  <img src="/images/blog/2021-07-21-memory-manager-beta/SingleCrossNUMAAllocation.png">
</p>

1. The `container1` started on the NUMA node 0 and requests *5Gi* of the memory but currently is consuming only *3Gi* of the memory.
2. The `container2` the memory request is *10Gi*, and none single NUMA node can satisfy it.
3. The `container2` consumes *3.5Gi* of the memory from the NUMA node 0, but once the `container1` will require more memory, it will not have it, and the kernel will kill one of the containers with the **OOM** error.

To prevent such issues, the **MemoryManager** will fail the admission of the `container2` until the machine, will have two NUMA nodes without a single NUMA node allocation.

### Works only for guaranteed pods

The **MemoryManager** can not guarantee memory allocation for burstable pods, also when the burstable pod has specified equal memory limit and request.
Let's assume you have two burstable pods, `pod1` has containers with equal memory request and limits, and `pod2` has containers only with the memory request. We want to guarantee memory allocation for the `pod1`. Both pods have the same **OOM** score, so once the kernel will not have enough memory, it can kill `pod1`.

### Memory fragmentation

The sequence of containers that start and stop can fragment the memory on NUMA nodes. Currently, we do not have any components under the kubelet that can balance pods and defragment memory back.

## Future work for the **MemoryManager**

We do not want to stop with the current state of the **MemoryManager** and looking for places for improvements.

### Make the MemoryManager allocation algorithm smarter

The current algorithm ignores distances between NUMA nodes during the calculation of the allocation. We can get better performance when the **MemoryManager** will use the closest NUMA nodes for cross NUMA node allocation.

### Reduce the number of admission errors

The default Kubernetes scheduler not aware of the node's NUMA topology, and it can be a reason for many admission errors during the pod start.
A [KEP]([https://https://github.com/kubernetes/enhancements/pull/2787) for this work is currently under review, and a prototype is underway to get this feature implemented very soon.


## Conclusion
With the promotion of the **MemoryManager** to beta in 1.22, we encourage everyone to give it a try and look forward to any feedback you may have. While there are still several limitations, we have a set of enhancements planned to address them and look forward to providing you with many new features in upcoming releases.
If you have ideas for additional enhancements or a desire for certain features, please let us know. The team is always open to suggestions to enhance and improve the **MemoryManager**.
We hope you have found this blog informative and helpful! Let us know if you have any questions or comments.