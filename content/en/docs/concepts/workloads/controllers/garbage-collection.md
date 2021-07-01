---
title: Garbage Collection
content_type: concept
weight: 60
---

<!-- overview -->

The role of the Kubernetes garbage collector is to delete certain objects
that once had an owner, but no longer have an owner.


<!-- body -->

## Owners and dependents

Some Kubernetes objects are owners of other objects. For example, a ReplicaSet
is the owner of a set of Pods. The owned objects are called *dependents* of the
owner object. Every dependent object has a `metadata.ownerReferences` field that
points to the owning object.

Sometimes, Kubernetes sets the value of `ownerReference` automatically. For
example, when you create a ReplicaSet, Kubernetes automatically sets the
`ownerReference` field of each Pod in the ReplicaSet. In 1.8, Kubernetes
automatically sets the value of `ownerReference` for objects created or adopted
by ReplicationController, ReplicaSet, StatefulSet, DaemonSet, Deployment, Job
and CronJob.

You can also specify relationships between owners and dependents by manually
setting the `ownerReference` field.

Here's a configuration file for a ReplicaSet that has three Pods:

{{< codenew file="controllers/replicaset.yaml" >}}

If you create the ReplicaSet and then view the Pod metadata, you can see
OwnerReferences field:

```shell
kubectl apply -f https://k8s.io/examples/controllers/replicaset.yaml
kubectl get pods --output=yaml
```

The output shows that the Pod owner is a ReplicaSet named `my-repset`:

```yaml
apiVersion: v1
kind: Pod
metadata:
  ...
  ownerReferences:
  - apiVersion: apps/v1
    controller: true
    blockOwnerDeletion: true
    kind: ReplicaSet
    name: my-repset
    uid: d9607e19-f88f-11e6-a518-42010a800195
  ...
```

{{< note >}}
Cross-namespace owner references are disallowed by design.

Namespaced dependents can specify cluster-scoped or namespaced owners.
A namespaced owner **must** exist in the same namespace as the dependent.
If it does not, the owner reference is treated as absent, and the dependent
is subject to deletion once all owners are verified absent.

Cluster-scoped dependents can only specify cluster-scoped owners.
In v1.20+, if a cluster-scoped dependent specifies a namespaced kind as an owner,
it is treated as having an unresolvable owner reference, and is not able to be garbage collected.

In v1.20+, if the garbage collector detects an invalid cross-namespace `ownerReference`,
or a cluster-scoped dependent with an `ownerReference` referencing a namespaced kind, a warning Event 
with a reason of `OwnerRefInvalidNamespace` and an `involvedObject` of the invalid dependent is reported.
You can check for that kind of Event by running
`kubectl get events -A --field-selector=reason=OwnerRefInvalidNamespace`.
{{< /note >}}

## Controlling how the garbage collector deletes dependents

When you delete an object, you can specify whether the object's dependents are
also deleted automatically. Deleting dependents automatically is called *cascading
deletion*.  There are two modes of *cascading deletion*: *background* and *foreground*.

If you delete an object without deleting its dependents
automatically, the dependents are said to be *orphaned*.

### Foreground cascading deletion

In *foreground cascading deletion*, the root object first
enters a "deletion in progress" state. In the "deletion in progress" state,
the following things are true:

 * The object is still visible via the REST API
 * The object's `deletionTimestamp` is set
 * The object's `metadata.finalizers` contains the value "foregroundDeletion".

Once the "deletion in progress" state is set, the garbage
collector deletes the object's dependents. Once the garbage collector has deleted all
"blocking" dependents (objects with `ownerReference.blockOwnerDeletion=true`), it deletes
the owner object.

Note that in the "foregroundDeletion", only dependents with
`ownerReference.blockOwnerDeletion=true` block the deletion of the owner object.
Kubernetes version 1.7 added an [admission controller](/docs/reference/access-authn-authz/admission-controllers/#ownerreferencespermissionenforcement) that controls user access to set
`blockOwnerDeletion` to true based on delete permissions on the owner object, so that
unauthorized dependents cannot delay deletion of an owner object.

If an object's `ownerReferences` field is set by a controller (such as Deployment or ReplicaSet),
blockOwnerDeletion is set automatically and you do not need to manually modify this field.

### Background cascading deletion

In *background cascading deletion*, Kubernetes deletes the owner object
immediately and the garbage collector then deletes the dependents in
the background.

### Setting the cascading deletion policy

To control the cascading deletion policy, set the `propagationPolicy`
field on the `deleteOptions` argument when deleting an Object. Possible values include "Orphan",
"Foreground", or "Background".

Here's an example that deletes dependents in background:

```shell
kubectl proxy --port=8080
curl -X DELETE localhost:8080/apis/apps/v1/namespaces/default/replicasets/my-repset \
  -d '{"kind":"DeleteOptions","apiVersion":"v1","propagationPolicy":"Background"}' \
  -H "Content-Type: application/json"
```

Here's an example that deletes dependents in foreground:

```shell
kubectl proxy --port=8080
curl -X DELETE localhost:8080/apis/apps/v1/namespaces/default/replicasets/my-repset \
  -d '{"kind":"DeleteOptions","apiVersion":"v1","propagationPolicy":"Foreground"}' \
  -H "Content-Type: application/json"
```

Here's an example that orphans dependents:

```shell
kubectl proxy --port=8080
curl -X DELETE localhost:8080/apis/apps/v1/namespaces/default/replicasets/my-repset \
  -d '{"kind":"DeleteOptions","apiVersion":"v1","propagationPolicy":"Orphan"}' \
  -H "Content-Type: application/json"
```

kubectl also supports cascading deletion.

To delete dependents in the foreground using kubectl, set `--cascade=foreground`.  To
orphan dependents, set `--cascade=orphan`. 

The default behavior is to delete the dependents in the background which is the
behavior when `--cascade` is omitted or explicitly set to `background`.

Here's an example that orphans the dependents of a ReplicaSet:

```shell
kubectl delete replicaset my-repset --cascade=orphan
```

### Additional note on Deployments

Prior to 1.7, When using cascading deletes with Deployments you *must* use `propagationPolicy: Foreground`
to delete not only the ReplicaSets created, but also their Pods. If this type of _propagationPolicy_
is not used, only the ReplicaSets will be deleted, and the Pods will be orphaned.
See [kubeadm/#149](https://github.com/kubernetes/kubeadm/issues/149#issuecomment-284766613) for more information.

## Known issues

Tracked at [#26120](https://github.com/kubernetes/kubernetes/issues/26120)



## {{% heading "whatsnext" %}}


[Design Doc 1](https://git.k8s.io/community/contributors/design-proposals/api-machinery/garbage-collection.md)

[Design Doc 2](https://git.k8s.io/community/contributors/design-proposals/api-machinery/synchronous-garbage-collection.md)
