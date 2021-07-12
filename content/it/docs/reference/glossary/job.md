---
title: Job
id: job
date: 2018-04-12
full_link: /docs/concepts/workloads/controllers/jobs-run-to-completion
short_description: >
  Uno o più lavori (task) che vengono eseguiti fino al loro completamento.

aka: 
tags:
- fundamental
- core-object
- workload
---
 Uno o più lavori (task) che vengono eseguiti fino al loro completamento.

<!--more--> 

Crea uno o più oggetti di tipo {{< glossary_tooltip term_id="pod" >}} ed assicura che un numero preciso di questi venga completato con successo. Quando i _Pod_ vengono eseguiti con successo, il _Job_ tiene traccia della completamento andato a buon fine.

