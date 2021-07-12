---
title: StatefulSet
id: statefulset
date: 2018-04-12
full_link: /docs/concepts/workloads/controllers/statefulset/
short_description: >
  Gestisce deployment e la scalabilità di un gruppo di Pod, con storage e identificativi persistenti per ogni Pod.

aka: 
tags:
- fundamental
- core-object
- workload
- storage
---
 Gestisce deployment e la scalabilità di un gruppo di {{< glossary_tooltip text="Pods" term_id="pod" >}}, *e garantisce il corretto ordine e unicità* di questi Pods.

<!--more--> 

Come un {{< glossary_tooltip term_id="deployment" >}}, uno StatefulSet gestisce Pod che sono basati sulla stessa specifica di container. Contrariamente da un Deployment, uno StatefulSet mantiente una specifica identita per ogni Pod. Questi pod sono creati dalla stessa specifica, ma  non sono intercambiabili: ogni pod a un identificativo persistente che si mantiene attraverso ogni rischedulazione.

Se vuoi usare un volume dello storage per avere la persistenza per il tuo carico di lavoro, puoi usare uno StatefulSet come parte della tua soluzione. Anche se i singoli Pod in uno StatefulSet sono suscettibili al fallimento, l'identificativo persistente del Pod rende semplice il collegamento dei volumi esistenti ai nuovi Pods che sostituiscono quelli falliti.
