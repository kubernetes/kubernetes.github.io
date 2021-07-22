---
title: Garbage Collection
content_type: concept
weight: 50
---

<!-- overview -->
{{<glossary_definition term_id="garbage-collection" length="short">}} This
allows the clean up of resources like the following:

  * [Failed pods](/docs/concepts/workloads/pods/pod-lifecycle/#pod-garbage-collection)
  * [Completed Jobs](/docs/concepts/workloads/controllers/ttlafterfinished/)
  * [Objects without owner references](#owners-dependents)
  * [Unused containers and container images](#containers-images)
  * [Dynamically provisioned PersistentVolumes with a StorageClass reclaim policy of Delete](/docs/concepts/storage/persistent-volumes/#delete)
  * [Stale or expired CertificateSigningRequests (CSRs)](/reference/access-authn-authz/certificate-signing-requests/#request-signing-process)
  * {{<glossary_tooltip text="Nodes" term_id="node">}} deleted in the following scenarios:
    * On a cloud when the cluster uses a [cloud controller manager](/docs/concepts/architecture/cloud-controller/)
    * On-premises when the cluster uses an addon similar to a cloud controller
      manager
  * [Node Lease objects](/docs/concepts/architecture/nodes/#heartbeats)

## Owners and dependents {#owners-dependents}

Many objects in Kubernetes link to each other through [*owner references*](/docs/concepts/overview/working-with-objects/owners-dependents/). 
Owner references tell the control plane which objects are dependent on others.
Kubernetes uses owner references to give the control plane, and other API
clients, the opportunity to clean up related resources before deleting an
object. In most cases, Kubernetes manages owner references automatically.

Ownership is different from the [labels and selectors](/docs/concepts/overview/working-with-objects/labels/)
mechanism that some resources also use. For example, consider a
{{<glossary_tooltip text="Service" term_id="service">}} that creates
`EndpointSlice` objects. The Service uses *labels* to allow the control plane to
determine which `EndpointSlice` objects are used for that Service. In addition
to the labels, each `EndpointSlice` that is managed on behalf of a Service has
an owner reference. Owner references help different parts of Kubernetes avoid
interfering with objects they don’t control.

## Cascading deletion {#cascading-deletion}

Kubernetes checks for and deletes objects that no longer have owner
references, like the pods left behind when you delete a ReplicaSet. When you
delete an object, you can control whether Kubernetes deletes the object's
dependents automatically, in a process called *cascading deletion*. There are
two types of cascading deletion, as follows: 

  * Foreground cascading deletion
  * Background cascading deletion

You can also control how and when garbage collection deletes resources that have
owner references using Kubernetes {{<glossary_tooltip text="finalizers" term_id="finalizer">}}. 

### Foreground cascading deletion {#foreground-deletion}

In foreground cascading deletion, the owner object you're deleting first enters
a *deletion in progress* state. In this state, the following happens to the
owner object: 

  * The Kubernetes API server sets the object's `metadata.deletionTimestamp`
    field to the time the object was marked for deletion.
  * The Kubernetes API server also sets the `metadata.finalizers` field to
    `foregroundDeletion`. 
  * The object remains visible through the Kubernetes API until the deletion
    process is complete.

After the owner object enters the deletion in progress state, the controller
deletes the dependents. After deleting all the dependent objects, the controller
deletes the owner object. At this point, the object is no longer visible in the
Kubernetes API. 

During foreground cascading deletion, the only dependents that block owner
deletion are those that have the `ownerReference.blockOwnerDeletion=true` field.
See [Use foreground cascading deletion](/docs/tasks/administer-cluster/use-cascading-deletion/#use-foreground-cascading-deletion)
to learn more.

### Background cascading deletion {#background-deletion}

In background cascading deletion, the Kubernetes API server deletes the owner
object immediately and the controller cleans up the dependent objects in
the background. By default, Kubernetes uses background cascading deletion unless
you manually use foreground deletion or choose to orphan the dependent objects.

See [Use background cascading deletion](/docs/tasks/administer-cluster/use-cascading-deletion/#use-background-cascading-deletion)
to learn more.

### Orphaned dependents

When Kubernetes deletes an owner object, the dependents left behind are called
*orphan* objects. By default, Kubernetes deletes dependent objects. To learn how
to override this behaviour, see [Delete owner objects and orphan dependents](/docs/tasks/administer-cluster/use-cascading-deletion/#set-orphan-deletion-policy).

## Garbage collection of unused containers and images {#containers-images}

The {{<glossary_tooltip text="kubelet" term_id="kubelet">}} performs garbage
collection on unused images every five minutes and on unused containers every
minute. You should avoid using external garbage collection tools, as these can
break the kubelet behavior and remove containers that should exist. 

To configure options for unused container and image garbage collection, tune the
kubelet using a [configuration file](/docs/tasks/administer-cluster/kubelet-config-file/)
and change the parameters related to garbage collection using the
[`KubeletConfiguration`](/docs/reference/config-api/kubelet-config.v1beta1/#kubelet-config-k8s-io-v1beta1-KubeletConfiguration)
resource type.

### Container image lifecycle

Kubernetes manages the lifecycle of all images through its *image manager*,
which is part of the kubelet, with the cooperation of cadvisor. The kubelet
considers the following disk usage limits when making garbage collection
decisions:

  * `HighThresholdPercent`
  * `LowThresholdPercent`

Disk usage above the configured `HighThresholdPercent` value triggers garbage
collection, which deletes images in order based on the last time they were used,
starting with the oldest first. The kubelet deletes images
until disk usage reaches the `LowThresholdPercent` value.

### Container image garbage collection {#container-image-garbage-collection}

The kubelet garbage collects unused containers based on the following variables,
which you can define: 

  * `MinAge`: the minimum age at which the kubelet can garbage collect a
    container. Disable by setting to `0`.
  * `MaxPerPodContainer`: the maximum number of dead containers each Pod pair
    can have. Disable by setting to less than `0`.
  * `MaxContainers`: the maximum number of dead containers the cluster can have.
    Disable by setting to less than `0`. 

In addition to these variables, the kubelet garbage collects unidentified and
deleted containers, typically starting with the oldest first. 

`MaxPerPodContainer` and `MaxContainer` may potentially conflict with each other
in situations where retaining the maximum number of containers per Pod
(`MaxPerPodContainer`) would go outside the allowable total of global dead
containers (`MaxContainers`). In this situation, the kubelet adjusts
`MaxPodPerContainer` to address the conflict. A worst-case scenario would be to
downgrade `MaxPerPodContainer` to `1` and evict the oldest containers.
Additionally, containers owned by pods that have been deleted are removed once
they are older than `MinAge`.

{{<note>}}
The kubelet only garbage collects the containers it manages.
{{</note>}}

## Configuring garbage collection {#configuring-gc}

You can tune garbage collection of resources by configuring options specific to
the controllers managing those resources. The following pages show you how to
configure garbage collection:

  * [Configuring cascading deletion of Kubernetes objects](/docs/tasks/administer-cluster/use-cascading-deletion/)
  * [Configuring cleanup of finished Jobs](/docs/concepts/workloads/controllers/ttlafterfinished/)
  
<!-- * [Configuring unused container and image garbage collection](/docs/tasks/administer-cluster/reconfigure-kubelet/) -->

## {{% heading "whatsnext" %}}

* Learn more about [ownership of Kubernetes objects](/docs/concepts/overview/working-with-objects/owners-dependents/).
* Learn more about Kubernetes [finalizers](/docs/concepts/overview/working-with-objects/finalizers/).
* Learn about the [TTL controller](/docs/concepts/workloads/controllers/ttlafterfinished/) (beta) that cleans up finished Jobs.