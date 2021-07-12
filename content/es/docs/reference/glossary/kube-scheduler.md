---
title: kube-scheduler
id: kube-scheduler
date: 2018-04-12
full_link: /docs/reference/generated/kube-scheduler/
short_description: >
  Componente del plano de control que está pendiente de los pods que no tienen
  ningún nodo asignado y seleciona uno dónde ejecutarlo.

aka:
tags:
- architecture
---

Componente del plano de control que está pendiente de los
{{< glossary_tooltip term_id="pod" text="Pods" >}} que no tienen ningún
{{< glossary_tooltip term_id="node" text="nodo">}} asignado
y seleciona uno donde ejecutarlo.

<!--more-->

Para decidir en qué {{< glossary_tooltip term_id="node" text="nodo">}}
se ejecutará el {{< glossary_tooltip term_id="pod" text="pod" >}}, se tienen
en cuenta diversos factores: requisitos de recursos, restricciones de hardware/software/políticas,
afinidad y anti-afinidad, localización de datos dependientes, entre otros.
