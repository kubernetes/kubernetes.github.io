---
title: Eviction
id: eviction
date: 2021-03-05
full_link: /docs/concepts/scheduling-eviction/pod-eviction
short_description: >
  Reclaimation of resources by terminating one or more {{< glossary_tooltip text="pods" term_id="pod" >}} and deleting unused {{< glossary_tooltip text="images" term_id="image" >}} on a {{< glossary_tooltip text="nodes" term_id="node" >}}.

aka:
tags:
- fundamental
- operation
---
 Reclaimation of resources by terminating one or more {{< glossary_tooltip text="pods" term_id="pod" >}} and deleting unused {{< glossary_tooltip text="images" term_id="image" >}} on a {{< glossary_tooltip text="nodes" term_id="node" >}}.

<!--more-->

Eviction is a process performed by the {{< glossary_tooltip term_id="kubelet" >}} due to resource constraints on a {{< glossary_tooltip term_id="node" >}}, use of the {{< glossary_tooltip term_id="kubectl" >}} `drain` command, or an [Eviction API](/docs/tasks/administer-cluster/safely-drain-node/#eviction-api) request.