---
title: Kubelet
id: kubelet
date: 2020-04-19
full_link: /docs/reference/generated/kubelet
short_description: >
  Um agente que é executado em cada node no cluster. Ele garante que os contêineres estejam sendo executados em um pod.

aka: 
tags:
- fundamental
- core-object
---
 Um agente que é executado em cada {{< glossary_tooltip text="node" term_id="node" >}} no cluster. Ele garante que os {{< glossary_tooltip text="contêineres" term_id="container" >}} estejam sendo executados em um {{< glossary_tooltip text="Pod" term_id="pod" >}}.

<!--more--> 

O kubelet utiliza um conjunto de PodSpecs que são fornecidos por vários mecanismos e garante que os contêineres descritos nesses PodSpecs estejam funcionando corretamente. O kubelet não gerencia contêineres que não foram criados pelo Kubernetes.
