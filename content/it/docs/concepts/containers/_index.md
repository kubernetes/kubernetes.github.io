---
title: Containers
weight: 40
description: La tecnologia per distribuire un'applicazione insieme con le dipendenze necessarie per la sua esecuzione.
content_type: concept
no_list: true
---

<!-- overview -->

Ogni _container_ che viene eseguito è riproducibile; la pratica di includere le dipendenze all'interno di ciascuno _container_ permette di ottenere sempre lo stesso risultato ad ogni esecuzione del medesimo _container_. 

I _Container_ permettono di disaccoppiare le applicazioni dall'infrastruttura del host su cui vengono eseguite. Questo approccio rende più facile il _deployment_ su cloud o sitemi operativi differenti tra loro.

<!-- body -->

## Immagine di container
L'[immagine di un container](/docs/concepts/containers/images/) e' un pacchetto software che contiene tutto ciò che serve per eseguire un'applicazione: il codice sorgente e ciascun _runtime_ necessario, librerie applicative e di sistema, e le impostazioni predefinite per ogni configurazione necessaria.

Un _container_ è immutabile per definizione: non è possibile modificare il codice di un _container_ in esecuzione. Se si ha un'applicazione containerizzata e la si vuole modificare, si deve costruire un nuovo _container_ che includa il cambiamento desiderato, e quindi ricreare il _container_ partendo dalla nuova immagine aggiornata.

## Container runtimes

{{< glossary_definition term_id="container-runtime" length="all" >}}

## {{% heading "whatsnext" %}}

* Leggi in merito [immagine di container](/docs/concepts/containers/images/)
* Leggi in merito [Pods](/docs/concepts/workloads/pods/)

