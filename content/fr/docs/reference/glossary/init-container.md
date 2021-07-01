---
title: Init Container
id: init-container
date: 2018-04-12
full_link:
short_description: >
  Un ou plusieurs conteneurs d'initialisation qui doivent être exécutés jusqu'à la fin, avant l'exécution de tout conteneur d'application.

aka:
tags:
- fundamental
---
 Un ou plusieurs conteneurs d'initialisation qui doivent être exécutés jusqu'à la fin, avant l'exécution de tout conteneur d'application.

<!--more-->

Les conteneurs d'initialisation (init containers en anglais) sont comme les conteneurs d'applications classiques, à une différence près : les conteneurs d'initialisation doivent être exécutés jusqu'au bout, avant que les conteneurs d'applications puissent démarrer. Les conteneurs d'initialisation fonctionnent en série : chaque conteneur d'initialisation doit fonctionner jusqu'à la complétion avant que le conteneur d'initialisation suivant ne commence.
