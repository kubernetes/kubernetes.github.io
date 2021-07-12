---
title: Cloud Controller Manager
id: cloud-controller-manager
date: 2018-04-12
full_link: /docs/concepts/architecture/cloud-controller/
short_description: >
  Element warstwy sterowania, który integruje Kubernetesa z zewnętrznymi usługami chmurowymi.
aka: 
tags:
- core-object
- architecture
- operation
---
Element składowy {{< glossary_tooltip text="warstwy sterowania" term_id="control-plane" >}} Kubernetesa,
który zarządza usługami realizowanymi po stronie chmur obliczeniowych. Cloud controller manager umożliwia
połączenie Twojego klastra z API operatora usług chmurowych i rozdziela składniki operujące na platformie
chmurowej od tych, które dotyczą wyłącznie samego klastra.

<!--more-->

Dzięki rozdzieleniu logiki zarządzającej pomiędzy klaster Kubernetesa i leżącą poniżej infrastrukturę chmurową,
cloud-controller-manager umożliwia operatorom usług chmurowych na dostarczanie nowych funkcjonalności
niezależnie od cyklu wydawniczego głównego projektu Kubernetes.
