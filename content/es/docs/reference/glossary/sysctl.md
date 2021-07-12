---
title: sysctl
id: sysctl
date: 2019-02-12
full_link: /docs/tasks/administer-cluster/sysctl-cluster/
short_description: >
  Una interfaz para obtener y asignar valores a parámetros del núcleo Unix activo.

aka:
tags:
- tool
---
 `sysctl` es una interfaz común usada para consultar o modificar atributos del
 núcleo Unix durante su ejecución.

<!--more-->

En los sistemas Unix-like, `sysctl` es el comando que usan los administradores,
para ver o modificar esos valores y también el nombre de la llamada al sistema
que realiza esta función.

La ejecución del {{< glossary_tooltip text="Contenedor" term_id="container" >}}
y de los complementos de red puede depender de los valores asignados via `sysctl`.
