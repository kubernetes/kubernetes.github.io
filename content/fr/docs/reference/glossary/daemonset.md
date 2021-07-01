---
title: DaemonSet
id: daemonset
date: 2018-04-12
full_link: /docs/concepts/workloads/controllers/daemonset
short_description: >
  S'assure qu'une copie d'un Pod s'exécute sur un ensemble de nœuds d'un cluster.

aka:
tags:
- fundamental
- core-object
- workload
---
 S'assure qu'une copie d'un {{< glossary_tooltip text="Pod" term_id="pod" >}} s'exécute sur un ensemble de nœuds d'un {{< glossary_tooltip text="cluster" term_id="cluster" >}}.

<!--more-->

Utilisé pour déployer des démons système tels que les collecteurs de logs et les agents de surveillance qui doivent généralement fonctionner sur chaque {{< glossary_tooltip text="nœud" term_id="node" >}}.
