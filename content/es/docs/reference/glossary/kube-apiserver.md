---
title: API Server
id: kube-apiserver
date: 2020-07-01
full_link: /docs/reference/generated/kube-apiserver/
short_description: >
  Componente del plano de control que expone la API de Kubernetes.

aka:
- Servidor de la API
- kube-apiserver
tags:
- architecture
- fundamental
---

El servidor de la API es el componente del {{< glossary_tooltip text="plano de control" term_id="control-plane" >}}
de Kubernetes que expone la API de Kubernetes. Se trata del frontend de Kubernetes,
recibe las peticiones y actualiza acordemente el estado en {{< glossary_tooltip term_id="etcd" length="all" >}}.

<!--more-->

La principal implementación de un servidor de la API de Kubernetes es
[kube-apiserver](/docs/reference/generated/kube-apiserver/).
Es una implementación preparada para ejecutarse en alta disponiblidad y que
puede escalar horizontalmente para balancear la carga entre varias instancias.