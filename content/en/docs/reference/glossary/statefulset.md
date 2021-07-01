---
title: StatefulSet
id: statefulset
date: 2018-04-12
full_link: /docs/concepts/workloads/controllers/statefulset/
short_description: >
  Manages deployment and scaling of a set of Pods, with durable storage and persistent identifiers for each Pod.

aka: 
tags:
- fundamental
- core-object
- workload
- storage
---
 Manages the deployment and scaling of a set of {{< glossary_tooltip text="Pods" term_id="pod" >}}, *and provides guarantees about the ordering and uniqueness* of these Pods.

<!--more--> 

Like a {{< glossary_tooltip term_id="deployment" >}}, a StatefulSet manages Pods that are based on an identical container spec. Unlike a Deployment, a StatefulSet maintains a sticky identity for each of their Pods. These pods are created from the same spec, but are not interchangeable&#58; each has a persistent identifier that it maintains across any rescheduling.

If you want to use storage volumes to provide persistence for your workload, you can use a StatefulSet as part of the solution. Although individual Pods in a StatefulSet are susceptible to failure, the persistent Pod identifiers make it easier to match existing volumes to the new Pods that replace any that have failed.
