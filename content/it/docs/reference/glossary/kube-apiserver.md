---
title: API server
id: kube-apiserver
date: 2018-04-12
full_link: /docs/reference/generated/kube-apiserver/
short_description: >
  Componente della Control plane che serve le Kubernetes API.

aka:
- kube-apiserver
tags:
- architecture
- fundamental
---
 L'API server è un componente di Kubernetes
{{< glossary_tooltip text="control plane" term_id="control-plane" >}} che espone le Kubernetes API.
L'API server è il front end del control plane di Kubernetes.

<!--more-->

La principale implementazione di un server Kubernetes API è [kube-apiserver](/docs/reference/generated/kube-apiserver/).
kube-apiserver è progettato per scalare orizzontalmente, cioè scala aumentando il numero di istanze.
Puoi eseguire multiple istanze di kube-apiserver e bilanciare il traffico tra queste istanze.
