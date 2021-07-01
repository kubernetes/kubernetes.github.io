---
title: kube-scheduler
id: kube-scheduler
date: 2018-04-12
full_link: /docs/reference/generated/kube-scheduler/
short_description: >
  Composant sur le master qui surveille les pods nouvellement créés qui ne sont pas assignés à un nœud et sélectionne un nœud sur lequel ils vont s'exécuter.

aka:
tags:
- architecture
---
 Composant sur le master qui surveille les pods nouvellement créés qui ne sont pas assignés à un nœud et sélectionne un nœud sur lequel ils vont s'exécuter.

<!--more-->

Les facteurs pris en compte pour les décisions de planification (scheduling) comprennent les exigences individuelles et collectives en ressources, les contraintes matérielles/logicielles/politiques, les spécifications d'affinité et d'anti-affinité, la localité des données, les interférences entre charges de travail et les dates limites.

