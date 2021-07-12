---
title: Namespace
id: namespace
date: 2018-04-12
full_link: /es/docs/concepts/overview/working-with-objects/namespaces/
short_description: >
  Abstracción utilizada por Kubernetes para soportar múltiples clústeres virtuales en el mismo clúster físico.
aka:
- Espacio de nombres
tags:
- fundamental
---

Abstracción utilizada por Kubernetes para soportar múltiples clústeres virtuales
en el mismo {{< glossary_tooltip text="clúster" term_id="cluster" >}} físico.

<!--more-->

Los Namespaces, espacios de nombres, se utilizan para organizar objetos del clúster
proporcionando un mecanismo para dividir los recusos del clúster. Los nombres de los
objetos tienen que ser únicos dentro del mismo namespace, pero se pueden repetir en
otros namespaces del mismo clúster.