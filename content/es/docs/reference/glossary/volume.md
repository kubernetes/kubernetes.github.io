---
title: Volume
id: volume
date: 2018-04-12
full_link: /docs/concepts/storage/volumes/
short_description: >
  Un directorio que contiene datos y que es accesible desde los contenedores corriendo en un pod.

aka:
tags:
- core-object
- fundamental
---
 Un directorio que contiene datos y que es accesible desde los contenedores corriendo en un {{< glossary_tooltip text="pod" term_id="pod" >}}.

<!--more-->

Un volumen de Kubernetes vive mientras exista el {{< glossary_tooltip text="pod" term_id="pod" >}} que lo contiene, no depende de la vida del {{< glossary_tooltip text="contenedor" term_id="container" >}} por eso se conservan los datos entre los reinicios de los {{< glossary_tooltip text="contenedores" term_id="container" >}}.
