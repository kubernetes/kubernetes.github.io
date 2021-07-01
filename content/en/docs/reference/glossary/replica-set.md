---
title: ReplicaSet
id: replica-set
date: 2018-04-12
full_link: /docs/concepts/workloads/controllers/replicaset/
short_description: >
 ReplicaSet ensures that a specified number of Pod replicas are running at one time

aka: 
tags:
- fundamental
- core-object
- workload
---
 A ReplicaSet (aims to) maintain a set of replica Pods running at any given time.

<!--more-->

Workload objects such as {{< glossary_tooltip term_id="deployment" >}} make use of ReplicaSets
to ensure that the configured number of {{< glossary_tooltip term_id="pod" text="Pods" >}} are
running in your cluster, based on the spec of that ReplicaSet.
