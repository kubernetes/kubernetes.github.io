---
title: Volume
id: volume
date: 2018-04-12
full_link: /docs/concepts/storage/volumes/
short_description: >
  A directory containing data, accessible to the containers in a pod.

aka:
tags:
- core-object
- fundamental
---
 A directory containing data, accessible to the {{< glossary_tooltip text="containers" term_id="container" >}} in a {{< glossary_tooltip term_id="pod" >}}.

<!--more-->

A Kubernetes volume lives as long as the Pod that encloses it. Consequently, a volume outlives any containers that run within the Pod, and data in the volume is preserved across container restarts.

See [storage](/docs/concepts/storage/) for more information.
