---
title: kube-controller-manager
id: kube-controller-manager
date: 2018-04-12
full_link: /docs/reference/command-line-tools-reference/kube-controller-manager/
short_description: >
  Компонент Control Plane запускает процессы контроллера.

aka:
tags:
- architecture
- fundamental
---
 Компонент Control Plane запускает процессы {{< glossary_tooltip text="контроллера" term_id="controller" >}}.

<!--more-->

Вполне логично, что каждый {{< glossary_tooltip text="контроллер" term_id="controller" >}} в свою очередь представляет собой отдельный процесс, и для упрощения все такие процессы скомпилированы в один двоичный файл и выполняются в одном процессе.
