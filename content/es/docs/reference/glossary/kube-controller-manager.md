---
title: kube-controller-manager
id: kube-controller-manager
date: 2018-04-12
full_link: /docs/reference/command-line-tools-reference/kube-controller-manager/
short_description: >
  Componente del plano de control que ejecuta los controladores de Kubernetes.

aka:
tags:
- architecture
- fundamental
---

Componente del plano de control que ejecuta los {{< glossary_tooltip text="controladores" term_id="controller" >}} de Kubernetes.

<!--more-->

Lógicamente cada {{< glossary_tooltip text="controlador" term_id="controller" >}}
es un proceso independiente, pero para reducir la complejidad, todos se compilan
en un único binario y se ejecuta en un mismo proceso.
