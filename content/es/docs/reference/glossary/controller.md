---
title: Controlador
id: controller
date: 2018-04-12
full_link: /docs/concepts/architecture/controller/
short_description: >
  Los controladores son bucles de control que observan el estado del clúster,
  y ejecutan o solicitan los cambios que sean necesarios para alcanzar el estado
  deseado.

aka:
tags:
- architecture
- fundamental
---

En Kubernetes, los controladores son bucles de control que observan el estado del
{{< glossary_tooltip term_id="cluster" text="clúster">}}, y ejecutan o solicitan
los cambios que sean necesarios para llevar el estado actual del clúster más
cerca del estado deseado.

<!--more-->

Los controladores observan el estado compartido del clúster a través del
{{< glossary_tooltip text="API Server" term_id="kube-apiserver" >}} (parte del
{{< glossary_tooltip term_id="control-plane" text="plano de control" >}}).

Algunos controladores también se ejecutan dentro del mismo plano de control,
proporcionado los bucles de control necesarios para las operaciones principales
de Kubernetes. Por ejemplo, el controlador de Deployments, el controlador de
DaemonSets, el controlador de Namespaces y el controlador de volúmenes
persistentes, entre otros, se ejecutan dentro del
{{< glossary_tooltip term_id="kube-controller-manager" >}}.
