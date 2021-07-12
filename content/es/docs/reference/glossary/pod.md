---
title: Pod
id: pod
date: 2018-05-16
full_link: /docs/concepts/workloads/pods/pod-overview/
short_description: >
  El objeto más pequeño y simple de Kubernetes. Un Pod es la unidad mínima de computación en Kubernetes y representa uno o más contenedores ejecutándose en el clúster.

aka:
tags:
- core-object
- fundamental
---
  El objeto más pequeño y simple de Kubernetes. Un Pod es la unidad mínima de computación en Kubernetes y representa uno o más {{< glossary_tooltip text="contenedores" term_id="container" >}} ejecutándose en el clúster.

<!--more-->

Normalmente un Pod se configura para ejecutar un solo contenedor primario, pero también puede ejecutar contenedores adicionales para implementar diferentes patrones como _sidecar_ o _ambassador_. Estos contenedores pueden ser parte de la aplicación o simplemente añadir funcionalidades adicionales como gestión de logs o actuar de proxy. Los Pods son comúnmente gestionados por un {{< glossary_tooltip term_id="deployment" >}}.

