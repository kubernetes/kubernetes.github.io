---
title: Horizontal Pod Autoscaler
id: horizontal-pod-autoscaler
date: 2018-04-12
full_link: /docs/tasks/run-application/horizontal-pod-autoscale/
short_description: >
  An API resource that automatically scales the number of pod replicas based on targeted CPU utilization or custom metric targets.

aka: 
- HPA
tags:
- operation
---
 An API resource that automatically scales the number of {{< glossary_tooltip term_id="pod" >}} replicas based on targeted CPU utilization or custom metric targets.

<!--more--> 

HPA is typically used with {{< glossary_tooltip text="ReplicationControllers" term_id="replication-controller" >}}, {{< glossary_tooltip text="Deployments" term_id="deployment" >}}, or {{< glossary_tooltip text="ReplicaSets" term_id="replica-set" >}}. It cannot be applied to objects that cannot be scaled, for example {{< glossary_tooltip text="DaemonSets" term_id="daemonset" >}}.

