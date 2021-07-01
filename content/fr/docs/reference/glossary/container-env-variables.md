---
title: Variables d'Environnement de Conteneur
id: container-env-variables
date: 2018-04-12
full_link: /docs/concepts/containers/container-environment-variables/
short_description: >
  Les variables d'environnement de conteneur sont des paires nom=valeur qui fournissent des informations utiles aux conteneurs fonctionnant au sein d'un Pod.

aka:
tags:
- fundamental
---
 Les variables d'environnement de conteneur sont des paires nom=valeur qui fournissent des informations utiles aux conteneurs fonctionnant au sein d'un Pod.

<!--more-->

Les variables d'environnement de conteneur fournissent les informations requises par les applications conteneurisées en cours d'exécution, ainsi que des informations sur les ressources importantes aux {{< glossary_tooltip text="Conteneurs" term_id="container" >}} comme les détails du système de fichiers, les informations sur le conteneur lui-même et d'autres ressources du cluster telles que les terminaux de services par exemple.
