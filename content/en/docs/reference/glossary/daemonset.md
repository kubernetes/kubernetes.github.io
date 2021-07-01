---
title: DaemonSet
id: daemonset
date: 2018-04-12
full_link: /docs/concepts/workloads/controllers/daemonset
short_description: >
  Ensures a copy of a Pod is running across a set of nodes in a cluster.

aka: 
tags:
- fundamental
- core-object
- workload
---
 Ensures a copy of a {{< glossary_tooltip text="Pod" term_id="pod" >}} is running across a set of nodes in a {{< glossary_tooltip text="cluster" term_id="cluster" >}}.

<!--more--> 

Used to deploy system daemons such as log collectors and monitoring agents that typically must run on every {{< glossary_tooltip term_id="node" >}}.

