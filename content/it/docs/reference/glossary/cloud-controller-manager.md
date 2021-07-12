---
title: Cloud Controller Manager
id: cloud-controller-manager
date: 2018-04-12
full_link: /docs/concepts/architecture/cloud-controller/
short_description: >
  Componente della control plane che integra Kubernetes con cloud providers di terze parti.
aka: 
tags:
- core-object
- architecture
- operation
---
Un componente della {{< glossary_tooltip text="control plane" term_id="control-plane" >}} di Kubernetes 
che aggiunge logiche di controllo specifiche per il cloud. Il cloud-controller-manager ti permette di collegare il tuo
cluster con le API del cloud provider e separa le componenti che interagiscono
con la piattaforma cloud dai componenti che interagiscono solamente col cluster.

<!--more-->

Disaccoppiando la logica di interoperabilità tra Kubernetes e l'infrastruttura cloud sottostante,
il componente cloud-controller-manager abilità i cloud provider di rilasciare
funzionalità a un ritmo diverso rispetto al progetto principale Kubernetes. 

