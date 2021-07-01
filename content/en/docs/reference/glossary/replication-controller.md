---
title: ReplicationController
id: replication-controller
date: 2018-04-12
full_link: 
short_description: >
  A (deprecated) API object that manages a replicated application.

aka: 
tags:
- workload
- core-object
---
 A workload resource that manages a replicated application, ensuring that
a specific number of instances of a {{< glossary_tooltip text="Pod" term_id="pod" >}} are running.

<!--more-->

The control plane ensures that the defined number of Pods are running, even if some
Pods fail, if you delete Pods manually, or if too many are started by mistake.

{{< note >}}
ReplicationController is deprecated. See
{{< glossary_tooltip text="Deployment" term_id="deployment" >}}, which is similar.
{{< /note >}}
