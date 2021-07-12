---
title: DaemonSet
id: daemonset
date: 2018-04-12
full_link: /docs/concepts/workloads/controllers/daemonset
short_description: >
  Assicura che una copia di un Pod è attiva su tutti nodi di un cluster.

aka: 
tags:
- fundamental
- core-object
- workload
---
 Assicura che una copia del {{< glossary_tooltip text="Pod" term_id="pod" >}} è attiva su tutti nodi di un {{< glossary_tooltip text="cluster" term_id="cluster" >}}.

<!--more--> 

Utilizzato per il deploy di demoni di sistema come collettori di log e agenti di monitoraggio che tipicamente girano in ogni {{< glossary_tooltip term_id="node" >}}.

