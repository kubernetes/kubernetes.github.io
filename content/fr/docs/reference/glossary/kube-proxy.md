---
title: kube-proxy
id: kube-proxy
date: 2018-04-12
full_link: /docs/reference/command-line-tools-reference/kube-proxy/
short_description: >
  `kube-proxy` est un proxy réseau qui s'exécute sur chaque nœud du cluster.

aka:
tags:
- fundamental
- networking
---
 [kube-proxy](/docs/reference/command-line-tools-reference/kube-proxy/) est un
proxy réseau qui s'exécute sur chaque nœud du cluster et implémente une partie du
concept Kubernetes de {{< glossary_tooltip term_id="service">}}.

<!--more-->

kube-proxy maintient les règles réseau sur les nœuds. Ces règles réseau permettent
une communication réseau vers les Pods depuis des sessions réseau à l'intérieur ou à l'extérieur
du cluster.

kube-proxy utilise la couche de filtrage de paquets du système d'exploitation s'il y en a une et qu'elle est disponible. Sinon, kube-proxy transmet le trafic lui-même.
