---
title: Storage Class
id: storageclass
date: 2018-04-12
full_link: /docs/concepts/storage/storage-classes
short_description: >
  A StorageClass provides a way for administrators to describe different available storage types.

aka: 
tags:
- core-object
- storage
---
 A StorageClass provides a way for administrators to describe different available storage types.

<!--more--> 

StorageClasses can map to quality-of-service levels, backup policies, or to arbitrary policies determined by cluster administrators. Each StorageClass contains the fields `provisioner`, `parameters`, and `reclaimPolicy`, which are used when a {{< glossary_tooltip text="Persistent Volume" term_id="persistent-volume" >}} belonging to the class needs to be dynamically provisioned. Users can request a particular class using the name of a StorageClass object.

