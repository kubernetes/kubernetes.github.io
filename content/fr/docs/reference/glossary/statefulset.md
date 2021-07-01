---
title: StatefulSet
id: statefulset
date: 2018-04-12
full_link: /fr/docs/concepts/workloads/controllers/statefulset/
short_description: >
  Gère le déploiement et la mise à l'échelle d'un ensemble de Pods, avec un stockage durable et des identifiants persistants pour chaque Pod.

aka: 
tags:
- fundamental
- core-object
- workload
- storage
---
 Gère le déploiement et la mise à l'échelle d'un ensemble de {{< glossary_tooltip text="Pods" term_id="pod" >}}, *et fournit des garanties sur l'ordre et l'unicité* de ces Pods.

<!--more--> 

Comme un {{< glossary_tooltip term_id="deployment" >}}, un StatefulSet gère des Pods qui sont basés sur une même spécification de conteneur. Contrairement à un Deployment, un StatefulSet maintient une identité pour chacun de ces Pods. Ces Pods sont créés à partir de la même spec, mais ne sont pas interchangeables : chacun a un identifiant persistant qu'il garde à travers tous ses re-scheduling.

Si vous voulez utiliser des volumes de stockage pour fournir de la persistance à votre charge de travail, vous pouvez utiliser un StatefulSet comme partie de la solution. Même si des Pods individuels d'un StatefulSet sont susceptibles d'échouer, les identifiants persistants des Pods rendent plus facile de faire correspondre les volumes existants aux nouveaux Pods remplaçant ceux ayant échoué.
