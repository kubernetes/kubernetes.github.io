---
title: Pod
id: pod
date: 2020-04-19
full_link: /docs/concepts/workloads/pods/pod-overview/
short_description: >
  O menor e mais simples objeto Kubernetes. Um Pod representa um conjunto de contêineres em execução no seu cluster.
aka: 
tags:
- core-object
- fundamental
---
 O menor e mais simples objeto Kubernetes. Um Pod representa um conjunto de {{< glossary_tooltip text="contêineres" term_id="container" >}} em execução no seu cluster.

<!--more--> 

Um Pod é normalmente configurado para executar um único contêiner primário. Ele também pode executar contêineres opcionais que adicionam recursos adicionais, como registro em log. Os pods são geralmente gerenciados por um {{< glossary_tooltip term_id="deployment" >}}.