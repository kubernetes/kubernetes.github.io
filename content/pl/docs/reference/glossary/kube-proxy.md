---
title: kube-proxy
id: kube-proxy
date: 2018-04-12
full_link: /docs/reference/command-line-tools-reference/kube-proxy/
short_description: >
  `kube-proxy` to *proxy* sieciowe, które uruchomione jest na każdym węźle klastra.

aka:
tags:
- fundamental
- networking
---
 kube-proxy to *proxy* sieciowe, które uruchomione jest na każdym
 {{< glossary_tooltip text="węźle" term_id="node" >}} klastra
 i uczestniczy w tworzeniu
 {{< glossary_tooltip text="serwisu" term_id="service">}}.

<!--more-->

[kube-proxy](/docs/reference/command-line-tools-reference/kube-proxy/)
utrzymuje reguły sieciowe na węźle. Dzięki tym regułom
sieci na zewnątrz i wewnątrz klastra mogą komunikować się
z podami.

kube-proxy używa warstwy filtrowania pakietów dostarczanych przez system operacyjny, o ile taka jest dostępna.
W przeciwnym przypadku, kube-proxy samo zajmuje sie przekazywaniem ruchu sieciowego.
