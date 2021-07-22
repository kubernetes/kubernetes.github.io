---
title: Finalizer
id: finalizer
date: 2021-07-07
full_link: /docs/concepts/overview/working-with-objects/finalizers/
short_description: >
  A namespaced key that tells Kubernetes to wait until specific conditions are met
  before it fully deletes an object marked for deletion.
aka: 
tags:
- fundamental
- operation
---
Finalizers are namespaced keys that tell Kubernetes to wait until specific
conditions are met before it fully deletes resources marked for deletion.
Finalizers alert {{<glossary_tooltip text="controllers" term_id="controller">}}
to clean up resources the deleted object owned.

<!--more-->

When you tell Kubernetes to delete an object that has finalizers specified for
it, the Kubernetes API marks the object for deletion, putting it into a
read-only state. The target object remains in a terminating state while the
control plane, or other components, take the actions defined by the finalizers.
After these actions are complete, the controller removes the relevant finalizers
from the target object. When the `metadata.finalizers` field is empty,
Kubernetes considers the deletion complete.

You can use finalizers to control {{<glossary_tooltip text="garbage collection" term_id="garbage-collection">}}
of resources. For example, you can define a finalizer to clean up related resources or
infrastructure before the controller deletes the target resource.