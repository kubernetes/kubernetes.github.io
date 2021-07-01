---
title: 节点压力驱逐
id: node-pressure-eviction
date: 2021-05-13
full_link: /zh/docs/concepts/scheduling-eviction/node-pressure-eviction/
short_description: >
  节点压力驱逐是 kubelet 主动使 Pod 失败以回收节点上的资源的过程。
aka:
- kubelet eviction
tags:
- operation
---
<!-- 
---
title: Node-pressure eviction
id: node-pressure-eviction
date: 2021-05-13
full_link: /docs/concepts/scheduling-eviction/node-pressure-eviction/
short_description: >
  Node-pressure eviction is the process by which the kubelet proactively fails
  pods to reclaim resources on nodes.
aka:
- kubelet eviction
tags:
- operation
---
-->

<!-- 
Node-pressure eviction is the process by which the {{<glossary_tooltip term_id="kubelet" text="kubelet">}} proactively terminates
pods to reclaim resources on nodes.
-->
节点压力驱逐是 {{<glossary_tooltip term_id="kubelet" text="kubelet">}} 主动终止 Pod 以回收节点上资源的过程。

<!--more-->

<!-- 
The kubelet monitors resources like CPU, memory, disk space, and filesystem 
inodes on your cluster's nodes. When one or more of these resources reach
specific consumption levels, the kubelet can proactively fail one or more pods
on the node to reclaim resources and prevent starvation. 
-->
kubelet 监控集群节点上的 CPU、内存、磁盘空间和文件系统 inode 等资源。
当这些资源中的一个或多个达到特定消耗水平时，
kubelet 可以主动使节点上的一个或多个 Pod 失效，以回收资源并防止饥饿。

<!-- 
Node-pressure eviction is not the same as [API-initiated eviction](/docs/concepts/scheduling-eviction/api-eviction/).
-->
节点压力驱逐不用于 [API 发起的驱逐](/zh/docs/concepts/scheduling-eviction/api-eviction/)。
