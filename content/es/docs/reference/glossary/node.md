---
title: Node
id: node
date: 2018-04-12
full_link: /docs/concepts/architecture/nodes/
short_description: >
  Un Node, nodo en castellano, es una de las máquinas del clúster de Kubernetes.

aka:
tags:
- fundamental
---
 Un Node, nodo en castellano, es una de las máquinas del clúster de Kubernetes.

<!--more-->

Una máquina del clúster puede ser tanto una máquina virtual como una máquina física, dependiendo del clúster.
Tiene los servicios necesarios para ejecutar {{< glossary_tooltip text="Pods" term_id="pod" >}} y es manejado por los componentes maestros.
Los servicios de Kubernetes en un nodo incluyen la {{< glossary_tooltip text="container runtime interface" term_id="cri" >}}, kubelet y {{< glossary_tooltip text="kube-proxy" term_id="kube-proxy" >}}.
