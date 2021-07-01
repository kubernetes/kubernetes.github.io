---
title: Nó
id: node
date: 2020-04-19
full_link: /docs/concepts/architecture/nodes/
short_description: >
  Um Nó é uma máquina de trabalho no Kubernetes.

aka: 
tags:
- fundamental
---
 Um Nó é uma máquina de trabalho no Kubernetes.

<!--more--> 

Um Nó pode ser uma máquina virtual ou física, dependendo do cluster. Possui daemons ou serviços locais necessários para executar {{< glossary_tooltip text="Pods" term_id="pod" >}} e é gerenciado pelo {{< glossary_tooltip text="ambiente de gerenciamento" term_id="control-plane" >}}. Os daemons em um Node incluem  {{< glossary_tooltip text="kubelet" term_id="kubelet" >}}, {{< glossary_tooltip text="kube-proxy" term_id="kube-proxy" >}} e um contêiner runtime implementando o {{< glossary_tooltip text="CRI" term_id="cri" >}} como por exemplo o {{< glossary_tooltip term_id="docker" >}}.