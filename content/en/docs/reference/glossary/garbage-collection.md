---
title: Garbage Collection
id: garbage-collection
date: 2021-07-07
full_link: /docs/concepts/workloads/controllers/garbage-collection/
short_description: >
  A collective term for the various mechanisms Kubernetes uses to clean up cluster
  resources.

aka: 
tags:
- fundamental
- operation
---
 Garbage collection is a collective term for the various mechanisms Kubernetes uses to clean up
 cluster resources. 

<!--more-->

Kubernetes uses garbage collection to clean up resources like [unused containers and images](/docs/concepts/workloads/controllers/garbage-collection/#containers-images),
[failed Pods](/docs/concepts/workloads/pods/pod-lifecycle/#pod-garbage-collection),
[objects owned by the targeted resource](/docs/concepts/overview/working-with-objects/owners-dependents/),
[completed Jobs](/docs/concepts/workloads/controllers/ttlafterfinished/), and resources
that have expired or failed.