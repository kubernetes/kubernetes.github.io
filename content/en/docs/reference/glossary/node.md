---
title: Node
id: node
date: 2018-04-12
full_link: /docs/concepts/architecture/nodes/
short_description: >
  A node is a worker machine in Kubernetes.

aka:
tags:
- fundamental
---
 A node is a worker machine in Kubernetes.

<!--more-->

A worker node may be a VM or physical machine, depending on the cluster. It has local daemons or services necessary to run {{< glossary_tooltip text="Pods" term_id="pod" >}} and is managed by the control plane. The daemons on a node include {{< glossary_tooltip text="kubelet" term_id="kubelet" >}}, {{< glossary_tooltip text="kube-proxy" term_id="kube-proxy" >}}, and a container runtime implementing the {{< glossary_tooltip text="CRI" term_id="cri" >}} such as {{< glossary_tooltip term_id="docker" >}}.

In early Kubernetes versions, Nodes were called "Minions".
