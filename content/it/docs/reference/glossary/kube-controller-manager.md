---
title: kube-controller-manager
id: kube-controller-manager
date: 2018-04-12
full_link: /docs/reference/command-line-tools-reference/kube-controller-manager/
short_description: >
  Componente della Control Plane che gestisce i controller.

aka: 
tags:
- architecture
- fundamental
---
 Componente della Control Plane che gestisce {{< glossary_tooltip text="controllers" term_id="controller" >}}.

<!--more-->

Da un punto di vista logico, ogni {{< glossary_tooltip text="controller" term_id="controller" >}} è un processo separato, ma per ridurre la complessità, tutti i principali controller di Kubernetes vengono raggruppati in un unico container ed eseguiti in un singolo processo.
