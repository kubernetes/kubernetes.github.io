---
title: Warstwa agregująca
id: aggregation-layer
date: 2018-10-08
full_link: /docs/concepts/extend-kubernetes/api-extension/apiserver-aggregation/
short_description: >
  Warstwa agregujące pozwala instalować dodatkowe API w Kubernetesie.

aka: 
tags:
- architecture
- extension
- operation
---
Warstwa agregujące pozwala instalować dodatkowe API w Kubernetesie.

<!--more-->

Po ustawieniu {{< glossary_tooltip text="serwera API Kubernetesa" term_id="kube-apiserver" >}}, aby [wspierał dodatkowe APIs](/docs/tasks/extend-kubernetes/configure-aggregation-layer/), można dodawać obiekty typu `APIService`, w celu "zarejestrowania" ścieżki w URL w API Kubernetes.
