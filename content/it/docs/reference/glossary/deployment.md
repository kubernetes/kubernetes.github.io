---
title: Deployment
id: deployment
date: 2018-04-12
full_link: /docs/concepts/workloads/controllers/deployment/
short_description: >
  Gestisce una applicazione replicata nel tuo cluster.

aka: 
tags:
- fundamental
- core-object
- workload
---
 Un oggetto API che gestisce un'applicazione replicatata, tipicamente esegue Pod senza stato locale.

<!--more--> 
Ogni replica è rappresentata da un {{< glossary_tooltip term_id="pod" >}}, e i Pod sono distribuiti attraverso i 
{{< glossary_tooltip text="nodi" term_id="node" >}} di un cluster.
Per i carichi di lavoro che hanno bisogno di uno stato locale, cosidera l'utilizzo di un {{< glossary_tooltip term_id="StatefulSet" >}}.
