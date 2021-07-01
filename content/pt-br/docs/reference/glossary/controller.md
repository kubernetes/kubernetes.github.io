---
title: Controlador
id: controller
date: 2020-03-23
full_link: /docs/concepts/architecture/controller/
short_description: >
  Um ciclo de controle que observa o estado partilhado do cluster através do API Server e efetua
  mudanças tentando mover o estado atual em direção ao estado desejado.

aka: 
tags:
- architecture
- fundamental
---
No Kubernetes, controladores são ciclos de controle que observam o estado do seu
{{< glossary_tooltip term_id="cluster" text="cluster">}}, e então fazer ou requisitar
mudanças onde necessário.
Cada controlador tenta mover o estado atual do cluster mais perto do estado desejado.

<!--more-->

Controladores observam o estado partilhado do cluster através do
{{< glossary_tooltip text="apiserver" term_id="kube-apiserver" >}} (parte do
{{< glossary_tooltip term_id="control-plane" >}}).

Alguns controladores também correm dentro do plano de controle, fornecendo ciclos
de controle que são centrais às operações do Kubernetes. Por exemplo: o controlador
de *deployments*, o controlador de *daemonsets*, o controlador de *namespaces*, e o 
controlador de volumes persistentes (*persistent volumes*) (e outros) todos correm
dentro do {{< glossary_tooltip term_id="kube-controller-manager" >}}.
