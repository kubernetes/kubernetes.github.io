---
title: Контроллер (Controller)
id: controller
date: 2018-04-12
full_link: /docs/concepts/architecture/controller/
short_description: >
  Управляющий цикл который отслеживает общее состояние кластера через API-сервер и вносит изменения пытаясь приветси текушее состояние к желаемому состоянию.

aka: 
tags:
- architecture
- fundamental
---
Контроллеры в Kubernetes - управляющие циклы, которые отслеживают состояние вашего
{{< glossary_tooltip term_id="cluster" text="кластера">}}, затем вносят или запрашивают
изменения там, где это необходимо.
Каждый контроллер пытается привести текущее состояние кластера ближе к желаемому состоянию.

<!--more-->

Контроллеры отсллеживают общее состояние вашего кластера через
{{< glossary_tooltip text="API-сервер" term_id="kube-apiserver" >}} (часть
{{< glossary_tooltip text="плоскости управления" term_id="control-plane" >}}).

Некоторые контроллеры также работают внутри плоскости управления, обеспечивая
управляющие циклы, которые являются ядром для операций Kubernetes. Например:
контроллер развертывания (deployment controller), контроллер daemonset (daemonset controller),
контроллер пространства имен (namespace controller) и контроллер постоянных томов (persistent volume
controller) (и другие) работают с {{< glossary_tooltip term_id="kube-controller-manager" >}}.
