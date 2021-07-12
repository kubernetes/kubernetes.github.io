---
title: kube-proxy
id: kube-proxy
date: 2018-04-12
full_link: /docs/reference/command-line-tools-reference/kube-proxy/
short_description: >
  `kube-proxy` è un proxy eseguito su ogni nodo del cluster.

aka:
tags:
- fundamental
- networking
---
 [kube-proxy](/docs/reference/command-line-tools-reference/kube-proxy/) è un
proxy eseguito su ogni nodo del cluster, responsabile della gestione dei
Kubernetes {{< glossary_tooltip term_id="service">}}.

<!--more-->

I kube-proxy mantengono le regole di networking sui nodi.
Queste regole permettono la comunicazione verso gli altri nodi del cluster o l'esterno.

Il kube-proxy usa le librerie del sistema operativo quando possible; in caso contrario il kube-proxy gestisce il traffico direttamente.
