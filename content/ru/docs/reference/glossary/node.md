---
title: Node
id: node
date: 2018-04-12
full_link: /docs/concepts/architecture/nodes/
short_description: >
  Узел — рабочая машина в Kubernetes.

aka:
tags:
- fundamental
---
 Узел — рабочая машина в Kubernetes.

<!--more-->

Рабочий узел может быть как виртуальной, так и физической машиной, в зависимости от кластера. У него есть локальные демоны или сервисы, необходимые для запуска {{< glossary_tooltip text="подов" term_id="pod" >}}, а сам он управляется плоскостью управления. Демоны на узле включают в себя {{< glossary_tooltip text="kubelet" term_id="kubelet" >}}, {{< glossary_tooltip text="kube-proxy" term_id="kube-proxy" >}} и среду выполнения контейнера, основанную на {{< glossary_tooltip text="CRI" term_id="cri" >}}, например {{< glossary_tooltip term_id="docker" >}}.
