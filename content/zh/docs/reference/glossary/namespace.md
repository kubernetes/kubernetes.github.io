---
title: 名字空间（Namespace）
id: namespace
date: 2018-04-12
full_link: /zh/docs/concepts/overview/working-with-objects/namespaces/
short_description: >
  名字空间是 Kubernetes 为了在同一物理集群上支持多个虚拟集群而使用的一种抽象。

aka: 
tags:
- fundamental
---

<!--
---
title: Namespace
id: namespace
date: 2018-04-12
full_link: /docs/concepts/overview/working-with-objects/namespaces/
short_description: >
  An abstraction used by Kubernetes to support multiple virtual clusters on the same physical cluster.

aka: 
tags:
- fundamental
---
-->

<!--
 An abstraction used by Kubernetes to support multiple virtual clusters on the same physical {{< glossary_tooltip text="cluster" term_id="cluster" >}}.
-->

名字空间是 Kubernetes 为了在同一物理集群上支持多个虚拟集群而使用的一种抽象。

<!--more--> 

<!--
Namespaces are used to organize objects in a cluster and provide a way to divide cluster resources. Names of resources need to be unique within a namespace, but not across namespaces.
-->

名字空间用来组织集群中对象，并为集群资源划分提供了一种方法。同一名字空间内的资源名称必须唯一，但跨名字空间时不作要求。
在一些文档里名字空间也称为命名空间。
