---
title: Serwer API
id: kube-apiserver
date: 2018-04-12
full_link: /docs/concepts/overview/components/#kube-apiserver
short_description: >
  Składnik warstwy sterowania udostępniający API Kubernetesa.

aka:
- kube-apiserver
tags:
- architecture
- fundamental
---
Serwer API jest składnikiem
{{< glossary_tooltip text="warstwy sterowania" term_id="control-plane" >}} Kubernetesa, który udostępnia API.
Server API służy jako front-end warstwy sterowania Kubernetes.

<!--more-->

Podstawową implementacją serwera API Kubernetesa jest [kube-apiserver](/docs/reference/generated/kube-apiserver/).
kube-apiserver został zaprojektowany w taki sposób, aby móc skalować się horyzontalnie &mdash; to oznacza, że zwiększa swoją wydajność poprzez dodawanie kolejnych instancji.
Można uruchomić kilka instancji kube-apiserver i rozkładać między nimi ruch od klientów.
