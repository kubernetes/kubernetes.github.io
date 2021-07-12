---
title: Job
id: job
date: 2018-04-12
full_link: /docs/concepts/workloads/controllers/jobs-run-to-completion
short_description: >
  Una tarea finita o por lotes que se ejecuta hasta su finalización.

aka:
tags:
- fundamental
- core-object
- workload
---
 Una tarea finita o por lotes que se ejecuta hasta su finalización.

<!--more-->

Crea uno o más objetos {{< glossary_tooltip term_id="pod" >}} y se asegura que un número específico de los mismos finalicen con éxito. A medida que los Pods terminan, el objeto Job registra las ejecuciones completadas correctamente.

