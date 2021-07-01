---
title: 云控制器管理器（Cloud Controller Manager）
id: cloud-controller-manager
date: 2018-04-12
full_link: /zh/docs/tasks/administer-cluster/running-cloud-controller/
short_description: >
  云控制器管理器是 1.8 的 alpha 特性。在未来发布的版本中，这是将 Kubernetes 与任何其他云集成的最佳方式。

aka: 
tags:
- core-object
- architecture
- operation
---

<!--
---
title: Cloud Controller Manager
id: cloud-controller-manager
date: 2018-04-12
full_link: /docs/concepts/architecture/cloud-controller/
short_description: >
  Cloud Controller Manager is an alpha feature in 1.8. In upcoming releases it will be the preferred way to integrate Kubernetes with any cloud.

aka: 
tags:
- core-object
- architecture
- operation
---
-->


<!--
 A Kubernetes {{< glossary_tooltip text="control plane" term_id="control-plane" >}} component
that embeds cloud-specific control logic. The cloud controller manager lets you link your
cluster into your cloud provider's API, and separates out the components that interact
with that cloud platform from components that only interact with your cluster.
-->

云控制器管理器是指嵌入特定云的控制逻辑的
{{< glossary_tooltip text="控制平面" term_id="control-plane" >}}组件。
云控制器管理器允许您链接集群到云提供商的应用编程接口中，
并把和该云平台交互的组件与只和您的集群交互的组件分离开。

<!--more--> 

<!--
By decoupling the interoperability logic between Kubernetes and the underlying cloud
infrastructure, the cloud-controller-manager component enables cloud providers to release
features at a different pace compared to the main Kubernetes project.
-->
通过分离 Kubernetes 和底层云基础设置之间的互操作性逻辑，
云控制器管理器组件使云提供商能够以不同于 Kubernetes 主项目的速度进行发布新特征。