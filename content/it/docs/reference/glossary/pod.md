---
title: Pod
id: pod
date: 2018-04-12
full_link: /docs/concepts/workloads/pods/pod-overview/
short_description: >
  Un Pod rappresenta un gruppo di container nel tuo cluster.

aka: 
tags:
- core-object
- fundamental
---
 Il più piccolo e semplice oggetto in Kubernetes. Un pod rappresenta un gruppo di {{< glossary_tooltip text="container" term_id="container" >}} nel tuo cluster.

<!--more--> 

Un pod è tipicamente progettato per eseguire un singolo container primario. Può opzionalmente eseguire sidecar container che aggiungono funzionalità supplementari come logging. I Pod sono generalmetne gestiti da un {{< glossary_tooltip term_id="deployment" >}}.

