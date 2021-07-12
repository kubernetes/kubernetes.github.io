---
title: 干扰（Disruption）
id: disruption
date: 2019-09-10
full_link: /zh/docs/concepts/workloads/pods/disruptions/
short_description: >
   导致 Pod 服务停止的事件。
aka:
tags:
- fundamental
---
 干扰是指导致一个或者多个 {{< glossary_tooltip term_id="pod" text="Pod" >}} 服务停止的事件。
干扰会影响工作负载资源，比如 {{< glossary_tooltip term_id="deployment" >}} 这种依赖于受影响 Pod 的资源。

<!-- 
---
title: Disruption
id: disruption
date: 2019-09-10
full_link: /docs/concepts/workloads/pods/disruptions/
short_description: >
  An event that leads to Pod(s) going out of service
aka:
tags:
- fundamental
---
 Disruptions are events that lead to one or more
{{< glossary_tooltip term_id="pod" text="Pods" >}} going out of service.
A disruption has consequences for workload resources, such as
{{< glossary_tooltip term_id="deployment" >}}, that rely on the affected
Pods.
 -->

<!--more-->

<!-- 
If you, as cluster operator, destroy a Pod that belongs to an application,
Kubernetes terms that a _voluntary disruption_. If a Pod goes offline
because of a Node failure, or an outage affecting a wider failure zone,
Kubernetes terms that an _involuntary disruption_.

See [Disruptions](/docs/concepts/workloads/pods/disruptions/) for more information.
 -->
如果您作为一个集群操作人员，销毁了一个从属于某个应用的 Pod, Kubernetes 视之为 _自愿干扰（Voluntary Disruption）_。如果由于节点故障
或者影响更大区域故障的断电导致 Pod 离线，kubernetes 视之为 _非愿干扰（Involuntary Disruption）_。

更多信息请查阅[Disruptions](/zh/docs/concepts/workloads/pods/disruptions/)