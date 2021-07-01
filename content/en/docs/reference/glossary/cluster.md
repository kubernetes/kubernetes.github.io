---
title: Cluster
id: cluster
date: 2019-06-15
full_link: 
short_description: >
   A set of worker machines, called nodes, that run containerized applications. Every cluster has at least one worker node.

aka: 
tags:
- fundamental
- operation
---
A set of worker machines, called {{< glossary_tooltip text="nodes" term_id="node" >}},
that run containerized applications. Every cluster has at least one worker node.

<!--more-->
The worker node(s) host the {{< glossary_tooltip text="Pods" term_id="pod" >}} that are
the components of the application workload. The
{{< glossary_tooltip text="control plane" term_id="control-plane" >}} manages the worker
nodes and the Pods in the cluster. In production environments, the control plane usually
runs across multiple computers and a cluster usually runs multiple nodes, providing
fault-tolerance and high availability.
