---
title: Controller
id: controller
date: 2018-04-12
full_link: /docs/concepts/architecture/controller/
short_description: >
  Un software che implementa un circuito di controllo che osserva lo stato condiviso del cluster attraverso l'API server e apporta le modifiche necessarie per portate lo stato corrente verso lo stato desiderato.

aka: 
tags:
- architecture
- fundamental
---
In Kubernetes, i _controller_ sono circuiti di controllo che osservano lo stato del {{< glossary_tooltip term_id="cluster" text="cluster">}}, e apportano o richiedono modifiche quando necessario. Ogni _controller_ prova a portare lo stato corrente del cluster verso lo stato desiderato.

<!--more-->

I _controller_ osservano lo stato condiviso del cluster attraverso il {{< glossary_tooltip text="apiserver" term_id="kube-apiserver" >}} (che è parte del {{< glossary_tooltip term_id="control-plane" >}}).

Alcuni _controller_ vengono eseguiti all'interno del _piano di controllo_ (_control plane_), e forniscono circuiti di controllo che sono parte dell'operatività base di Kubernetes. Ad esempio: il _deployment_ _controller_, il _daemonset_ _controller_, il _namespace_ _controller_, ed il _persistent volume_
_controller_ (e altri) vengono tutti eseguiti all'interno del {{< glossary_tooltip term_id="kube-controller-manager" >}}.
