---
title: Service
id: service
date: 2018-04-12
full_link: /fr/docs/concepts/services-networking/service/
short_description: >
  Un moyen d'exposer une application s'exécutant sur un ensemble de pods en tant que service réseau.

aka:
tags:
- fundamental
- core-object
---
Une manière abstraite d'exposer une application s'exécutant sur un ensemble de {{< glossary_tooltip text="Pods" term_id="pod" >}} en tant que service réseau.

<!--more-->

L'ensemble des pods ciblés par un service est (généralement) déterminé par un {{< glossary_tooltip text="selecteur" term_id="selector" >}}.
Si plus de Pods sont ajoutés ou supprimés, l'ensemble de Pods correspondant au sélecteur changera.
Le service s'assure que le trafic réseau peut être dirigé vers l'ensemble actuel de pods pour la charge de travail.
