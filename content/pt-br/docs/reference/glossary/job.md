---
title: Job
id: job
date: 2021-07-14
full_link: /docs/concepts/workloads/controllers/job
short_description: >
  Uma tarefa finita ou em lotes que executa até finalizar.

aka:
tags:
- fundamental
- core-object
- workload
---
Uma tarefa finita ou em lotes que executa até finalizar.

<!--more-->

Cria um ou mais objetos do tipo {{< glossary_tooltip term_id="pod" >}} e garante que um número determinado destes finaliza sua execução com sucesso. Conforme os Pods finalizam com sucesso, o Job observa as execuções bem-sucedidas.
