---
title: kube-scheduler
id: kube-scheduler
date: 2018-04-12
full_link: /docs/reference/generated/kube-scheduler/
short_description: >
  Componente della Control Plane che controlla i pod appena creati che non hanno un nodo assegnato, e dopo averlo identificato glielo assegna.

aka: 
tags:
- architecture
---
 Componente della Control Plane che controlla i pod appena creati che non hanno un nodo assegnato, e dopo averlo identificato glielo assegna.

<!--more--> 

I fattori presi in considerazioni nell'individuare un nodo a cui assegnare l'esecuzione di un Pod includono la richiesta di risorse del Pod stesso e degli altri workload presenti nel sistema, i vincoli delle hardware/software/policy, le indicazioni di affinity e di anti-affinity, requisiti relativi alla disponibilità di dati/Volumes, le interferenze tra diversi workload e le scadenze.

