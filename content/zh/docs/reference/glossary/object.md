---
title: 对象（Object）
id: object
date: 2020-10-12
full_link: /zh/docs/concepts/overview/working-with-objects/kubernetes-objects/#kubernetes-objects
short_description: >
   Kubernetes 系统中的实体, 代表了集群的部分状态。
aka: 
tags:
- fundamental
---
<!-- 
---
title: Object
id: object
date: 2020-10-12
full_link: https://kubernetes.io/docs/concepts/overview/working-with-objects/kubernetes-objects/#kubernetes-objects
short_description: >
   A entity in the Kubernetes system, representing part of the state of your cluster.
aka: 
tags:
- fundamental
---
-->
<!-- 
An entity in the Kubernetes system. The Kubernetes API uses these entities to represent the state
of your cluster.
-->
Kubernetes 系统中的实体。Kubernetes API 用这些实体表示集群的状态。

<!--more-->
<!-- 
A Kubernetes object is typically a “record of intent”—once you create the object, the Kubernetes
{{< glossary_tooltip text="control plane" term_id="control-plane" >}} works constantly to ensure
that the item it represents actually exists.
By creating an object, you're effectively telling the Kubernetes system what you want that part of
your cluster's workload to look like; this is your cluster's desired state.
-->
Kubernetes 对象通常是一个“目标记录”-一旦你创建了一个对象，Kubernetes 
{{< glossary_tooltip text="控制平面（Control Plane）" term_id="control-plane" >}} 
不断工作，以确保它代表的项目确实存在。
创建一个对象相当于告知 Kubernetes 系统：你期望这部分集群负载看起来像什么；这也就是你集群的期望状态。