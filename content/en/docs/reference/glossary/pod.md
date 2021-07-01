---
title: Pod
id: pod
date: 2018-04-12
full_link: /docs/concepts/workloads/pods/
short_description: >
  A Pod represents a set of running containers in your cluster.

aka: 
tags:
- core-object
- fundamental
---
 The smallest and simplest Kubernetes object. A Pod represents a set of running {{< glossary_tooltip text="containers" term_id="container" >}} on your cluster.

<!--more--> 

A Pod is typically set up to run a single primary container. It can also run optional sidecar containers that add supplementary features like logging. Pods are commonly managed by a {{< glossary_tooltip term_id="deployment" >}}.

