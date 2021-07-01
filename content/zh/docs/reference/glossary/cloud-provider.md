---
title: 云供应商（Cloud Provider）
id: cloud-provider
date: 2018-04-12
short_description: >
  一个提供云计算平台的组织。

aka:
- 云服务供应商（Cloud Service Provider）
tags:
- community
---

<!--
---
title: Cloud Provider
id: cloud-provider
date: 2018-04-12
short_description: >
  An organization that offers a cloud computing platform.

aka:
- Cloud Service Provider
tags:
- community
---
-->

<!--
 A business or other organization that offers a cloud computing platform.
-->
 一个提供云计算平台的商业机构或其他组织。



<!--more-->

<!--
Cloud providers, sometimes called Cloud Service Providers (CSPs), offer
cloud computing platforms or services.

Many cloud providers offer managed infrastructure (also called
Infrastructure as a Service or IaaS).
With managed infrastructure the cloud provider is responsible for
servers, storage, and networking while you manage layers on top of that
such as running a Kubernetes cluster.

You can also find Kubernetes as a managed service; sometimes called
Platform as a Service, or PaaS. With managed Kubernetes, your
cloud provider is responsible for the Kubernetes control plane as well
as the {{< glossary_tooltip term_id="node" text="nodes" >}} and the
infrastructure they rely on: networking, storage, and possibly other
elements such as load balancers.
-->
云供应商，有时也称作云服务供应商（CSPs）提供云计算平台或服务。

很多云供应商提供托管的基础设施（也称作基础设施即服务或 IaaS）。
针对托管的基础设施，云供应商负责服务器、存储和网络，而用户（你）
负责管理其上运行的各层软件，例如运行一个 Kubernetes 集群。

你也会看到 Kubernetes 被作为托管服务提供；有时也称作平台即服务或 PaaS。
针对托管的 Kubernetes，你的云供应商负责 Kubernetes 的控制面以及
 {{< glossary_tooltip term_id="node" text="节点" >}} 及他们所依赖的基础设施：
网络、存储以及其他一些诸如负载均衡器之类的元素。

