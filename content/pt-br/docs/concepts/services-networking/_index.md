---
title: "Serviços, balanceamento de carga e conectividade"
weight: 60
description: >
  Conceitos e recursos por trás da conectividade no Kubernetes.
---

A conectividade do Kubernetes trata quatro preocupações:
- Contêineres em um Pod se comunicam via interface _loopback_.
- A conectividade do cluster provê a comunicação entre diferentes Pods.
- O recurso de _Service_ permite a você expor uma aplicação executando em um Pod, 
de forma a ser alcançável de fora de seu cluster.
- Você também pode usar os _Services_ para publicar serviços de consumo interno do 
seu cluster.
