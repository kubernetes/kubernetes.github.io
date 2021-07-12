---
title: Persistent Volume Claim
id: persistent-volume-claim
date: 2018-04-12
full_link: /docs/concepts/storage/persistent-volumes/
short_description: >
  Reserva el recurso de almacenamiento definido en un PersistentVolume para poderlo montar como un volúmen en un contenedor.

aka:
tags:
- core-object
- storage
---
 Reserva el recurso de almacenamiento definido en un PersistentVolume para poderlo montar como un volúmen en un contenedor.

<!--more-->

Especifica la cantidad de almacenamiento, cómo acceder a él (sólo lectura, lectura y escritura y/o exclusivo) y qué hacer una vez eliminemos el PersistentVolumeClaim (mantener, reciclar o eliminar). Los detalles sobre almacenamiento están disponibles en la especificación de PersistentVolume.
