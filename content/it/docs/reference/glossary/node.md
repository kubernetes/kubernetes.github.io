---
title: Node
id: node
date: 2018-04-12
full_link: /docs/concepts/architecture/nodes/
short_description: >
  Un node è una macchina worker in Kubernetes.

aka: 
tags:
- fundamental
---
 Un node è una macchina worker in Kubernetes.

<!--more--> 

Un worker node può essere una VM o una macchina fisica, in base al cluster. Possiede daemon locali o servizi ncessari a eseguire {{< glossary_tooltip text="Pods" term_id="pod" >}} e viene gestito dalla control plane. I deamon i un node includono {{< glossary_tooltip text="kubelet" term_id="kubelet" >}}, {{< glossary_tooltip text="kube-proxy" term_id="kube-proxy" >}}, e un container runtiome che implementa {{< glossary_tooltip text="CRI" term_id="cri" >}} come ad esempio {{< glossary_tooltip term_id="docker" >}}.

Nelle prime versioni di Kubernetes, i Node venivano chiamati "Minion".
