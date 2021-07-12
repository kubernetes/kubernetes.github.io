---
title: kube-proxy
id: kube-proxy
date: 2018-04-12
full_link: /docs/reference/command-line-tools-reference/kube-proxy/
short_description: >
  `kube-proxy` es un componente de red que se ejecuta en cada nodo del clúster.

aka:
tags:
- fundamental
- networking
---
[kube-proxy](/es/docs/reference/command-line-tools-reference/kube-proxy/) es un
componente de red que se ejecuta en cada uno de los nodos del clúster, implementando
parte del concepto de Kubernetes {{< glossary_tooltip term_id="service">}}.

<!--more-->

kube-proxy mantiene las reglas de red en los nodos, permitiendo la
comunicación entre sus Pods desde las sesiones de red dentro o fuera
del clúster.

kube-proxy usa la capa de filtrado de paquetes del sistema operativo si la hay
y está disponible; de lo contrario, kube-proxy reenvía el tráfico por sí mismo.
