---
title: ConfigMap
id: configmap
date: 2018-04-12
full_link: /docs/tasks/configure-pod-container/configure-pod-configmap/
short_description: >
  Un objet API utilisé pour stocker des données non confidentielles dans des paires clé-valeur. Peut être utilisé comme variable d'environnement, argument de ligne de commande ou fichier de configuration dans un volume.

aka:
tags:
- core-object
---
 Un objet API utilisé pour stocker des données non confidentielles dans des paires clé-valeur. Peut être utilisé comme variable d'environnement, argument de ligne de commande ou fichier de configuration dans un {{< glossary_tooltip text="volume" term_id="volume" >}}.

<!--more-->

Permet de dissocier la configuration spécifique à l'environnement de vos {{< glossary_tooltip text="images de conteneurs" term_id="container" >}}, de sorte que vos applications soient facilement portable. Lorsque vous stockez des données confidentielles, utilisez un [Secret](/docs/concepts/configuration/secret/).
