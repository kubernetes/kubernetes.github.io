---
title: Server-Side Apply
reviewers:
- smarterclayton
- apelisse
- lavalamp
- liggitt
content_type: concept
weight: 25
min-kubernetes-server-version: 1.16
---

<!-- overview -->

{{< feature-state for_k8s_version="v1.16" state="beta" >}}

## Introduction

Server Side Apply helps users and controllers manage their resources through
declarative configurations. Clients can create and modify their
[objects](/docs/concepts/overview/working-with-objects/kubernetes-objects/)
declaratively by sending their fully specified intent.

A fully specified intent is a partial object that only includes the fields and
values for which the user has an opinion. That intent either creates a new
object or is [combined](#merge-strategy), by the server, with the existing object.

The system supports multiple appliers collaborating on a single object.

Changes to an object's fields are tracked through a "[field management](#field-management)"
mechanism. When a field's value changes, ownership moves from its current
manager to the manager making the change. When trying to apply an object,
fields that have a different value and are owned by another manager will
result in a [conflict](#conflicts). This is done in order to signal that the
operation might undo another collaborator's changes. Conflicts can be forced,
in which case the value will be overridden, and the ownership will be
transferred.

If you remove a field from a configuration and apply the configuration, server
side apply checks if there are any other field managers that also own the
field.  If the field is not owned by any other field managers, it is either
deleted from the live object or reset to its default value, if it has one. The
same rule applies to associative list or map items.

Server side apply is meant both as a replacement for the original `kubectl
apply` and as a simpler mechanism for controllers to enact their changes.

If you have Server Side Apply enabled, the control plane tracks managed fields
for all newly created objects.

## Field Management

Compared to the `last-applied` annotation managed by `kubectl`, Server Side
Apply uses a more declarative approach, which tracks a user's field management,
rather than a user's last applied state. This means that as a side effect of
using Server Side Apply, information about which field manager manages each
field in an object also becomes available.

For a user to manage a field, in the Server Side Apply sense, means that the
user relies on and expects the value of the field not to change. The user who
last made an assertion about the value of a field will be recorded as the
current field manager. This can be done either by changing the value with
`POST`, `PUT`, or non-apply `PATCH`, or by including the field in a config sent
to the Server Side Apply endpoint. When using Server-Side Apply, trying to
change a field which is managed by someone else will result in a rejected
request (if not forced, see [Conflicts](#conflicts)).

When two or more appliers set a field to the same value, they share ownership of
that field. Any subsequent attempt to change the value of the shared field, by any of
the appliers, results in a conflict. Shared field owners may give up ownership
of a field by removing it from their configuration.

Field management is stored in a`managedFields` field that is part of an object's
{{< api-reference page="common-definitions/object-meta" text="`metadata`" >}}.

A simple example of an object created by Server Side Apply could look like this:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: test-cm
  namespace: default
  labels:
    test-label: test
  managedFields:
  - manager: kubectl
    operation: Apply
    apiVersion: v1
    time: "2010-10-10T0:00:00Z"
    fieldsType: FieldsV1
    fieldsV1:
      f:metadata:
        f:labels:
          f:test-label: {}
      f:data:
        f:key: {}
data:
  key: some value
```

The above object contains a single manager in `metadata.managedFields`. The
manager consists of basic information about the managing entity itself, like
operation type, API version, and the fields managed by it.

{{< note >}}
This field is managed by the  API server and should not be changed by
the user.
{{< /note >}}

Nevertheless it is possible to change `metadata.managedFields` through an
`Update` operation. Doing so is highly discouraged, but might be a reasonable
option to try if, for example, the `managedFields` get into an inconsistent
state (which clearly should not happen).

The format of the `managedFields` is described in the
{{< api-reference page="common-definitions/object-meta" anchor="FieldsV1" text="API" >}}.

## Conflicts

A conflict is a special status error that occurs when an `Apply` operation tries
to change a field, which another user also claims to manage. This prevents an
applier from unintentionally overwriting the value set by another user. When
this occurs, the applier has 3 options to resolve the conflicts:

* **Overwrite value, become sole manager:** If overwriting the value was
  intentional (or if the applier is an automated process like a controller) the
  applier should set the `force` query parameter to true and make the request
  again. This forces the operation to succeed, changes the value of the field,
  and removes the field from all other managers' entries in managedFields.

* **Don't overwrite value, give up management claim:** If the applier doesn't
  care about the value of the field anymore, they can remove it from their
  config and make the request again. This leaves the value unchanged, and causes
  the field to be removed from the applier's entry in managedFields.

* **Don't overwrite value, become shared manager:** If the applier still cares
  about the value of the field, but doesn't want to overwrite it, they can
  change the value of the field in their config to match the value of the object
  on the server, and make the request again. This leaves the value unchanged,
  and causes the field's management to be shared by the applier and all other
  field managers that already claimed to manage it.

## Managers

Managers identify distinct workflows that are modifying the object (especially
useful on conflicts!), and can be specified through the `fieldManager` query
parameter as part of a modifying request. It is required for the apply endpoint,
though kubectl will default it to `kubectl`. For other updates, its default is
computed from the user-agent.

## Apply and Update

The two operation types considered by this feature are `Apply` (`PATCH` with
content type `application/apply-patch+yaml`) and `Update` (all other operations
which modify the object). Both operations update the `managedFields`, but behave
a little differently.

{{< note >}}
Whether you are submitting JSON data or YAML data, use
`application/apply-patch+yaml` as the `Content-Type` header value.

All JSON documents are valid YAML.
{{< /note >}}

For instance, only the apply operation fails on conflicts while update does
not. Also, apply operations are required to identify themselves by providing a
`fieldManager` query parameter, while the query parameter is optional for update
operations. Finally, when using the apply operation you cannot have
`managedFields` in the object that is being applied.

An example object with multiple managers could look like this:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: test-cm
  namespace: default
  labels:
    test-label: test
  managedFields:
  - manager: kubectl
    operation: Apply
    apiVersion: v1
    fields:
      f:metadata:
        f:labels:
          f:test-label: {}
  - manager: kube-controller-manager
    operation: Update
    apiVersion: v1
    time: '2019-03-30T16:00:00.000Z'
    fields:
      f:data:
        f:key: {}
data:
  key: new value
```

In this example, a second operation was run as an `Update` by the manager called
`kube-controller-manager`. The update changed a value in the data field which
caused the field's management to change to the `kube-controller-manager`.

If this update would have been an `Apply` operation, the operation
would have failed due to conflicting ownership.

## Merge strategy

The merging strategy, implemented with Server Side Apply, provides a generally
more stable object lifecycle. Server Side Apply tries to merge fields based on
the actor who manages them instead of overruling based on values. This way
multiple actors can update the same object without causing unexpected interference.

When a user sends a "fully-specified intent" object to the Server Side Apply
endpoint, the server merges it with the live object favoring the value in the
applied config if it is specified in both places. If the set of items present in
the applied config is not a superset of the items applied by the same user last
time, each missing item not managed by any other appliers is removed. For
more information about how an object's schema is used to make decisions when
merging, see
[sigs.k8s.io/structured-merge-diff](https://sigs.k8s.io/structured-merge-diff).

A number of markers were added in Kubernetes 1.16 and 1.17, to allow API
developers to describe the merge strategy supported by lists, maps, and
structs. These markers can be applied to objects of the respective type,
in Go files or in the OpenAPI schema definition of the
{{< api-reference page="extend-resources/custom-resource-definition-v1" anchor="JSONSchemaProps" text="CRD" >}}:

| Golang marker | OpenAPI extension | Accepted values | Description | Introduced in |
|---|---|---|---|---|
| `//+listType` | `x-kubernetes-list-type` | `atomic`/`set`/`map` | Applicable to lists. `set` applies to lists that include only scalar elements. These elements must be unique. `map` applies to lists of nested types only. The key values (see `listMapKey`) must be unique in the list. `atomic` can apply to any list. If configured as `atomic`, the entire list is replaced during merge. At any point in time, a single manager owns the list. If `set` or `map`, different managers can manage entries separately. | 1.16          |
| `//+listMapKey` | `x-kubernetes-list-map-keys` | List of field names, e.g. `["port", "protocol"]` | Only applicable when `+listType=map`. A list of field names whose values uniquely identify entries in the list. While there can be multiple keys, `listMapKey` is singular because keys need to be specified individually in the Go type. The key fields must be scalars. | 1.16 |
| `//+mapType` | `x-kubernetes-map-type` | `atomic`/`granular` | Applicable to maps. `atomic` means that the map can only be entirely replaced by a single manager. `granular` means that the map supports separate managers updating individual fields. | 1.17 |
| `//+structType` | `x-kubernetes-map-type` | `atomic`/`granular` | Applicable to structs; otherwise same usage and OpenAPI annotation as `//+mapType`.| 1.17 |

If `listType` is missing, the API server interprets a
`patchMergeStrategy=merge` marker as a `listType=map` and the
corresponding `patchMergeKey` marker as a `listMapKey`.

The `atomic` list type is recursive.

These markers are specified as comments and don't have to be repeated as
field tags.

### Compatibility across topology changes

On rare occurrences, a CRD or built-in type author may want to change the
specific topology of a field in their resource without incrementing its
version. Changing the topology of types, by upgrading the cluster or
updating the CRD, has different consequences when updating existing
objects. There are two categories of changes: when a field goes from
`map`/`set`/`granular` to `atomic` and the other way around.

When the `listType`, `mapType`, or `structType` changes from
`map`/`set`/`granular` to `atomic`, the whole list, map, or struct of
existing objects will end-up being owned by actors who owned an element
of these types. This means that any further change to these objects
would cause a conflict.

When a list, map, or struct changes from `atomic` to
`map`/`set`/`granular`, the API server won't be able to infer the new
ownership of these fields. Because of that, no conflict will be produced
when objects have these fields updated. For that reason, it is not
recommended to change a type from `atomic` to `map`/`set`/`granular`.

Take for example, the custom resource:

```yaml
apiVersion: example.com/v1
kind: Foo
metadata:
  name: foo-sample
  managedFields:
  - manager: manager-one
    operation: Apply
    apiVersion: example.com/v1
    fields:
      f:spec:
        f:data: {}
spec:
  data:
    key1: val1
    key2: val2
```

Before `spec.data` gets changed from `atomic` to `granular`,
`manager-one` owns the field `spec.data`, and all the fields within it
(`key1` and `key2`). When the CRD gets changed to make `spec.data`
`granular`, `manager-one` continues to own the top-level field
`spec.data` (meaning no other managers can delete the map called `data`
without a conflict), but it no longer owns `key1` and `key2`, so another
manager can then modify or delete those fields without conflict.

## Custom Resources

By default, Server Side Apply treats custom resources as unstructured data. All
keys are treated the same as struct fields, and all lists are considered atomic.

If the Custom Resource Definition defines a
{{< api-reference page="extend-resources/custom-resource-definition-v1" anchor="JSONSchemaProps" text="schema" >}}
that contains annotations as defined in the previous "Merge Strategy"
section, these annotations will be used when merging objects of this
type.

## Using Server-Side Apply in a controller

As a developer of a controller, you can use server-side apply as a way to
simplify the update logic of your controller. The main differences with a
read-modify-write and/or patch are the following:

* the applied object must contain all the fields that the controller cares about.
* there is no way to remove fields that haven't been applied by the controller
  before (controller can still send a PATCH/UPDATE for these use-cases).
* the object doesn't have to be read beforehand, `resourceVersion` doesn't have
  to be specified.

It is strongly recommended for controllers to always "force" conflicts, since they
might not be able to resolve or act on these conflicts.

## Transferring Ownership

In addition to the concurrency controls provided by [conflict resolution](#conflicts),
Server Side Apply provides ways to perform coordinated
field ownership transfers from users to controllers.

This is best explained by example. Let's look at how to safely transfer
ownership of the `replicas` field from a user to a controller while enabling
automatic horizontal scaling for a Deployment, using the HorizontalPodAutoscaler
resource and its accompanying controller.

Say a user has defined deployment with `replicas` set to the desired value:

{{< codenew file="application/ssa/nginx-deployment.yaml" >}}

And the user has created the deployment using server side apply like so:

```shell
kubectl apply -f https://k8s.io/examples/application/ssa/nginx-deployment.yaml --server-side
```

Then later, HPA is enabled for the deployment, e.g.:

```shell
kubectl autoscale deployment nginx-deployment --cpu-percent=50 --min=1 --max=10
```

Now, the user would like to remove `replicas` from their configuration, so they
don't accidentally fight with the HPA controller. However, there is a race: it
might take some time before HPA feels the need to adjust `replicas`, and if
the user removes `replicas` before the HPA writes to the field and becomes
its owner, then apiserver will set `replicas` to 1, its default value. This
is not what the user wants to happen, even temporarily.

There are two solutions:

- (basic) Leave `replicas` in the configuration; when HPA eventually writes to that
  field, the system gives the user a conflict over it. At that point, it is safe
  to remove from the configuration.

- (more advanced) If, however, the user doesn't want to wait, for example
  because they want to keep the cluster legible to coworkers, then they can take
  the following steps to make it safe to remove `replicas` from their
  configuration:

First, the user defines a new configuration containing only the `replicas` field:

{{< codenew file="application/ssa/nginx-deployment-replicas-only.yaml" >}}

The user applies that configuration using the field manager name `handover-to-hpa`:

```shell
kubectl apply -f https://k8s.io/examples/application/ssa/nginx-deployment-replicas-only.yaml \
  --server-side --field-manager=handover-to-hpa \
  --validate=false
```

If the apply results in a conflict with the HPA controller, then do nothing. The
conflict indicates the controller has claimed the field earlier in the
process than it sometimes does.

At this point the user may remove the `replicas` field from their configuration.

{{< codenew file="application/ssa/nginx-deployment-no-replicas.yaml" >}}

Note that whenever the HPA controller sets the `replicas` field to a new value,
the temporary field manager will no longer own any fields and will be
automatically deleted. No clean up is required.

### Transferring Ownership Between Users

Users can transfer ownership of a field between each other by setting the field
to the same value in both of their applied configs, causing them to share
ownership of the field. Once the users share ownership of the field, one of them
can remove the field from their applied configuration to give up ownership and
complete the transfer to the other user.

## Comparison with Client Side Apply

A consequence of the conflict detection and resolution implemented by Server
Side Apply is that an applier always has up to date field values in their local
state. If they don't, they get a conflict the next time they apply. Any of the
three options to resolve conflicts results in the applied configuration being an
up to date subset of the object on the server's fields.

This is different from Client Side Apply, where outdated values which have been
overwritten by other users are left in an applier's local config. These values
only become accurate when the user updates that specific field, if ever, and an
applier has no way of knowing whether their next apply will overwrite other
users' changes.

Another difference is that an applier using Client Side Apply is unable to
change the API version they are using, but Server Side Apply supports this use
case.

## Upgrading from client-side apply to server-side apply

Client-side apply users who manage a resource with `kubectl apply` can start
using server-side apply with the following flag.

```shell
kubectl apply --server-side [--dry-run=server]
```

By default, field management of the object transfers from client-side apply to
kubectl server-side apply without encountering conflicts.

{{< caution >}}
Keep the `last-applied-configuration` annotation up to date.
The annotation infers client-side apply's managed fields.
Any fields not managed by client-side apply raise conflicts.

For example, if you used `kubectl scale` to update the replicas field after
client-side apply, then this field is not owned by client-side apply and
creates conflicts on `kubectl apply --server-side`.
{{< /caution >}}

This behavior applies to server-side apply with the `kubectl` field manager.
As an exception, you can opt-out of this behavior by specifying a different,
non-default field manager, as seen in the following example. The default field
manager for kubectl server-side apply is `kubectl`.

```shell
kubectl apply --server-side --field-manager=my-manager [--dry-run=server]
```

## Downgrading from server-side apply to client-side apply

If you manage a resource with `kubectl apply --server-side`,
you can downgrade to client-side apply directly with `kubectl apply`.

Downgrading works because kubectl server-side apply keeps the
`last-applied-configuration` annotation up-to-date if you use
`kubectl apply`.

This behavior applies to server-side apply with the `kubectl` field manager.
As an exception, you can opt-out of this behavior by specifying a different,
non-default field manager, as seen in the following example. The default field
manager for kubectl server-side apply is `kubectl`.

```shell
kubectl apply --server-side --field-manager=my-manager [--dry-run=server]
```

## API Endpoint

With the Server Side Apply feature enabled, the `PATCH` endpoint accepts the
additional `application/apply-patch+yaml` content type. Users of Server Side
Apply can send partially specified objects as YAML to this endpoint.  When
applying a configuration, one should always include all the fields that they
have an opinion about.

## Clearing ManagedFields

It is possible to strip all managedFields from an object by overwriting them
using `MergePatch`, `StrategicMergePatch`, `JSONPatch`, or `Update`, so every
non-apply operation. This can be done by overwriting the managedFields field
with an empty entry. Two examples are:

```console
PATCH /api/v1/namespaces/default/configmaps/example-cm
Content-Type: application/merge-patch+json
Accept: application/json
Data: {"metadata":{"managedFields": [{}]}}
```

```console
PATCH /api/v1/namespaces/default/configmaps/example-cm
Content-Type: application/json-patch+json
Accept: application/json
Data: [{"op": "replace", "path": "/metadata/managedFields", "value": [{}]}]
```

This will overwrite the managedFields with a list containing a single empty
entry that then results in the managedFields being stripped entirely from the
object. Note that setting the managedFields to an empty list will not
reset the field. This is on purpose, so managedFields never get stripped by
clients not aware of the field.

In cases where the reset operation is combined with changes to other fields
than the managedFields, this will result in the managedFields being reset
first and the other changes being processed afterwards. As a result the
applier takes ownership of any fields updated in the same request.

{{< caution >}}
Server Side Apply does not correctly track ownership on
sub-resources that don't receive the resource object type. If you are
using Server Side Apply with such a sub-resource, the changed fields
won't be tracked.
{{< /caution >}}

## Disabling the feature

Server Side Apply is a beta feature, so it is enabled by default. To turn this
[feature gate](/docs/reference/command-line-tools-reference/feature-gates) off,
you need to include the `--feature-gates ServerSideApply=false` flag when
starting `kube-apiserver`. If you have multiple `kube-apiserver` replicas, all
should have the same flag setting.
