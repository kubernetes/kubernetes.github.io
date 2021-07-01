---
title: kube-controller-manager
id: kube-controller-manager
date: 2018-04-12
full_link: /docs/reference/generated/kube-controller-manager/
short_description: >
  Composant du master qui exécute les contrôleurs.

aka:
tags:
- architecture
- fundamental
---
 Composant du master qui exécute les {{< glossary_tooltip text="contrôleurs" term_id="controller" >}}.

<!--more-->

Logiquement, chaque {{< glossary_tooltip text="contrôleur" term_id="controller" >}} est un processus à part mais,
pour réduire la complexité, les contrôleurs sont tous compilés dans un seul binaire et s'exécutent dans un seul processus.
