---
title: ReplicaSet
id: replica-set
date: 2018-05-16
full_link: /docs/concepts/workloads/controllers/replicaset/
short_description: >
  El ReplicaSet es la nueva generación del ReplicationController.

aka:
tags:
- fundamental
- core-object
- workload
---
 El ReplicaSet es la nueva generación del ReplicationController.

<!--more-->

Un ReplicaSet, análogamente a un {{< glossary_tooltip text="ReplicationController" term_id="replication-controller" >}}, garantiza que un número establecido de réplicas de un pod estén corriendo en un momento dado. El ReplicaSet tiene soporte para selectores del tipo set-based, lo que permite el filtrado de claves por grupos de valores como por ejemplo todos los pods cuya etiqueta `environment` no sea `production` ni `qa`. Por otro lado, el ReplicationController solo soporta selectores equality-based, es decir, que solo puedes filtrar por valores exactos como por ejemplo, los pods que tengan la etiqueta `tier` con valor `frontend`.
