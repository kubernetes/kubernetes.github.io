---
title: Persistent Volume Claim
id: persistent-volume-claim
date: 2018-04-12
full_link: /docs/concepts/storage/persistent-volumes/
short_description: >
  Claims storage resources defined in a PersistentVolume so that it can be mounted as a volume in a container.

aka: 
tags:
- core-object
- storage
---
 Claims storage resources defined in a {{< glossary_tooltip text="PersistentVolume" term_id="persistent-volume" >}} so that it can be mounted as a volume in a {{< glossary_tooltip text="container" term_id="container" >}}.

<!--more--> 

Specifies the amount of storage, how the storage will be accessed (read-only, read-write and/or exclusive) and how it is reclaimed (retained, recycled or deleted). Details of the storage itself are described in the PersistentVolume object.
