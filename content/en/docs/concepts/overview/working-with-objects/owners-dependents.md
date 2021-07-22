---
title: Owners and Dependents
content_type: concept
weight: 60
---

<!-- overview -->

In Kubernetes, some objects are *owners* of other objects. For example, a
{{<glossary_tooltip text="ReplicaSet" term_id="replica-set">}} is the owner of a set of Pods. These owned objects are *dependents*
of their owner. 

Ownership is different from the [labels and selectors](/docs/concepts/overview/working-with-objects/labels/)
mechanism that some resources also use. For example, consider a Service that 
creates `EndpointSlice` objects. The Service uses labels to allow the control plane to
determine which `EndpointSlice` objects are used for that Service. In addition
to the labels, each `EndpointSlice` that is managed on behalf of a Service has
an owner reference. Owner references help different parts of Kubernetes avoid
interfering with objects they don’t control. 

## Owner references in object specifications

Dependent objects have a `metadata.ownerReferences` field that references their
owner object. A valid owner reference consists of the object name and a UID
within the same namespace as the dependent object. Kubernetes sets the value of
this field automatically for objects that are dependents of other objects like
ReplicaSets, DaemonSets, Deployments, Jobs and CronJobs, and ReplicationControllers.
You can also configure these relationships manually by changing the value of
this field. However, you usually don't need to and can allow Kubernetes to
automatically manage the relationships.

Dependent objects also have an `ownerReferences.blockOwnerDeletion` field that
takes a boolean value and controls whether specific dependents can block garbage
collection from deleting their owner object. Kubernetes automatically sets this
field to `true` if a {{<glossary_tooltip text="controller" term_id="controller">}} 
(for example, the Deployment controller) sets the value of the
`metadata.ownerReferences` field. You can also set the value of the
`blockOwnerDeletion` field manually to control which dependents block garbage
collection.

A Kubernetes admission controller controls user access to change this field for
dependent resources, based on the delete permissions of the owner. This control
prevents unauthorized users from delaying owner object deletion.

## Ownership and finalizers

When you tell Kubernetes to delete a resource, the API server allows the
managing controller to process any [finalizer rules](/docs/concepts/overview/working-with-objects/finalizers/)
for the resource. {{<glossary_tooltip text="Finalizers" term_id="finalizer">}}
prevent accidental deletion of resources your cluster may still need to function
correctly. For example, if you try to delete a `PersistentVolume` that is still
in use by a Pod, the deletion does not happen immediately because the
`PersistentVolume` has the `kubernetes.io/pv-protection` finalizer on it.
Instead, the volume remains in the `Terminating` status until Kubernetes clears
the finalizer, which only happens after the `PersistentVolume` is no longer
bound to a Pod. 

Kubernetes also adds finalizers to an owner resource when you use either
[foreground or orphan cascading deletion](/docs/concepts/architecture/garbage-collection/#cascading-deletion).
In foreground deletion, it adds the `foreground` finalizer so that the
controller must delete dependent resources that also have
`ownerReferences.blockOwnerDeletion=true` before it deletes the owner. If you
specify an orphan deletion policy, Kubernetes adds the `orphan` finalizer so
that the controller ignores dependent resources after it deletes the owner
object. 

## {{% heading "whatsnext" %}}

* Learn more about [Kubernetes finalizers](/docs/concepts/overview/working-with-objects/finalizers/).
* Learn about [garbage collection](/docs/concepts/architecture/garbage-collection).
* Read the API reference for [object metadata](/docs/reference/kubernetes-api/common-definitions/object-meta/#System).