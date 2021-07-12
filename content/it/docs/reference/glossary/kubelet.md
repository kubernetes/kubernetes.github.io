---
title: Kubelet
id: kubelet
date: 2018-04-12
full_link: /docs/reference/generated/kubelet
short_description: >
  Un agente che è eseguito su ogni nodo del cluster. Si assicura che i container siano eseguiti in un pod.

aka: 
tags:
- fundamental
- core-object
---
 Un agente che è eseguito su ogni nodo del cluster. Si assicura che i container siano eseguiti in un pod.

<!--more--> 

La kubelet riceve un set di PodSpecs che vengono forniti attraverso vari meccanismi, e si assicura che i container descritti in questi PodSpecs funzionino correttamente e siano sani. La kubelet non gestisce i container che non sono stati creati da Kubernetes.

