---
title: Kubernetes API Concepts
reviewers:
- smarterclayton
- lavalamp
- liggitt
content_type: concept
weight: 20
---

<!-- overview -->
The Kubernetes API is a resource-based (RESTful) programmatic interface
provided via HTTP. It supports retrieving, creating, updating, and deleting
primary resources via the standard HTTP verbs (POST, PUT, PATCH, DELETE,
GET).

The API includes additional subresources for many objects that allow
fine grained authorization (such as a separating viewing details for a Pod from
retrieving its logs), and can accept and serve those resources in different
representations for convenience or efficiency.

Kubernetes supports efficient change notifications on resources via *watches*.
Kubernetes also provides consistent list operations so that API clients can
effectively cache, track, and synchronize the state of resources.

You can view the [API reference](/docs/reference/kubernetes-api/) online,
or read on to learn about the API in general.

<!-- body -->
## Kubernetes API terminology {#standard-api-terminology}

Kubernetes generally leverages standard RESTful terminology to describe the API concepts:

* A *resource type* is the name used in the URL (`pods`, `namespaces`, `services`)
* All resource types have a concrete representation in JSON (their object schema) which is called a *kind*
* A list of instances of a resource type is known as a *collection*
* A single instance of the resource type is called a *resource*
* Some resource types have one or more *sub-resources*, represented as URI paths below the resource

Most Kubernetes API resource types are
[objects](/docs/concepts/overview/working-with-objects/kubernetes-objects/#kubernetes-objects):
they represent a concrete instance of a concept on the cluster, like a
pod or namespace. A smaller number of API resource types are *virtual* in
they often represent operations on objects, rather than objects, such as a
permission check (use a POST with a JSON-encoded body of `SubjectAccessReview`
to the `subjectaccessreviews` resource), or the `eviction` sub-resource of a
Pod (used to trigger
[API-initiated eviction](/docs/concepts/scheduling-eviction/api-eviction/)).

All objects you can create via the API have a unique object name to allow idempotent
creation and retrieval, except that virtual resource types may not have unique names if
they are not retrievable, or do not rely on idempotency.

### API verbs

Almost all object resource types support the standard HTTP verbs - GET, POST, PUT, PATCH,
and DELETE. Kubernetes also uses its own verbs, which are often written lowercase to distinguish
them from HTTP verbs.

Kubernetes uses the term **list** to describe returning a collection of
resources to distinguish from retrieving a single resource which is usually called
a **get**. If you sent an HTTP GET request with the `?watch` query parameter,
Kubernetes calls this a **watch** and not a **get** (see
[Efficient detection of changes](#efficient-detection-of-changes) for more details).

For PUT requests, Kubernetes internally classifies these as either **create** or **update**
based on the state of the existing object. An **update** is different from a **patch**; the
HTTP verb for a **patch** is PATCH.

{{< note >}}
The *server-side apply* concept differentiates between `Apply` and `Update` operations. That
`Update` operation is a separate concept from the logical **update** verb described here.

See [Apply and Update](/docs/reference/using-api/server-side-apply/#apply-and-update) for
more details.
{{< /note >}}

## Resource URIs

All resource types are either scoped by the cluster (`/apis/GROUP/VERSION/*`) or to a namespace (`/apis/GROUP/VERSION/namespaces/NAMESPACE/*`). A namespace-scoped resource type will be deleted when its namespace is deleted and access to that resource type is controlled by authorization checks on the namespace scope.

You can also access collections of resources (for example: listing all Nodes).
The following paths are used to retrieve collections and resources:

* Cluster-scoped resources:

  * `GET /apis/GROUP/VERSION/RESOURCETYPE` - return the collection of resources of the resource type
  * `GET /apis/GROUP/VERSION/RESOURCETYPE/NAME` - return the resource with NAME under the resource type

* Namespace-scoped resources:

  * `GET /apis/GROUP/VERSION/RESOURCETYPE` - return the collection of all instances of the resource type across all namespaces
  * `GET /apis/GROUP/VERSION/namespaces/NAMESPACE/RESOURCETYPE` - return collection of all instances of the resource type in NAMESPACE
  * `GET /apis/GROUP/VERSION/namespaces/NAMESPACE/RESOURCETYPE/NAME` - return the instance of the resource type with NAME in NAMESPACE

Since a namespace is a cluster-scoped resource type, you can retrieve the list (“collection”) of all namespaces with `GET /api/v1/namespaces` and details about a particular namespace with `GET /api/v1/namespaces/NAME`.

* Cluster-scoped subresource: `GET /apis/GROUP/VERSION/RESOURCETYPE/NAME/SUBRESOURCE`
* Namespace-scoped subresource: `GET /apis/GROUP/VERSION/namespaces/NAMESPACE/RESOURCETYPE/NAME/SUBRESOURCE`

The verbs supported for each subresource will differ depending on the object - see the [API reference](/docs/reference/kubernetes-api/) for more information. It is not possible to access sub-resources across multiple resources - generally a new virtual resource type would be used if that becomes necessary.


## Efficient detection of changes

To enable clients to build a model of the current state of a cluster, all Kubernetes object resource types are required to support consistent **list** requests and an incremental change notification feed called a **watch**.  Every Kubernetes object has a `resourceVersion` field representing the version of that resource as stored in the underlying database. When retrieving a collection of resources (either namespace or cluster scoped), the response from the server will contain a `resourceVersion` value that can be used to initiate a **watch** against the server. The server returns all changes (the outcome of **create**s, **delete**s, and **update**s) that occur after the supplied `resourceVersion`. This allows a client to fetch the current state and then subscribe to subsequent changes, without missing any events.

If a client **watch** is disconnected then that client can start a new **watch** from the last returned `resourceVersion`; the client could also perform a fresh **get** / **list** request and begin again. See [Resource Version Semantics](#resource-versions) for more detail.

For example:

1. List all of the pods in a given namespace.

   ```console
   GET /api/v1/namespaces/test/pods
   ---
   200 OK
   Content-Type: application/json

   {
     "kind": "PodList",
     "apiVersion": "v1",
     "metadata": {"resourceVersion":"10245"},
     "items": [...]
   }
   ```

2. Starting from resource version 10245, receive notifications of any **create**s, **delete**s, or **update**s as individual JSON objects. The response is a series of JSON documents (served as `application/json`).

   ```
   GET /api/v1/namespaces/test/pods?watch=1&resourceVersion=10245
   ---
   200 OK
   Transfer-Encoding: chunked
   Content-Type: application/json

   {
     "type": "ADDED",
     "object": {"kind": "Pod", "apiVersion": "v1", "metadata": {"resourceVersion": "10596", ...}, ...}
   }
   {
     "type": "MODIFIED",
     "object": {"kind": "Pod", "apiVersion": "v1", "metadata": {"resourceVersion": "11020", ...}, ...}
   }
   ...
   ```

A given Kubernetes server will only preserve a historical record of changes for a limited time. Clusters using etcd3 preserve changes in the last 5 minutes by default.  When the requested **watch** operations fail because the historical version of that resource is not available, clients must handle the case by recognizing the status code `410 Gone`, clearing their local cache, performing a **get** or **list** operation, and starting the **watch** from the `resourceVersion` that was returned.i

For subscribing to collections, Kubernetes client libraries typically offer some form of standard tool for this **list**-then-**watch** logic. (In the Go client library, this is called a `Reflector` and is located in the `k8s.io/client-go/cache` package.)

### Watch bookmarks

To mitigate the impact of short history window, the Kubernetes API provides a watch event named `BOOKMARK`. It is a special kind of event to mark that all changes up to a given `resourceVersion` the client is requesting have already been sent. The document representing the `BOOKMARK` event is of the type requested by the request, but only includes a `.metadata.resourceVersion` field. For example:

```console
GET /api/v1/namespaces/test/pods?watch=1&resourceVersion=10245&allowWatchBookmarks=true
---
200 OK
Transfer-Encoding: chunked
Content-Type: application/json

{
  "type": "ADDED",
  "object": {"kind": "Pod", "apiVersion": "v1", "metadata": {"resourceVersion": "10596", ...}, ...}
}
...
{
  "type": "BOOKMARK",
  "object": {"kind": "Pod", "apiVersion": "v1", "metadata": {"resourceVersion": "12746"} }
}
```

As a client, you can request `BOOKMARK` events by setting the `allowWatchBookmarks=true` query parameter to a **watch** request, but you shouldn't assume bookmarks are returned at any specific interval, nor can clients assume that the API server will send any `BOOKMARK` event even when requested.

## Retrieving large results sets in chunks

{{< feature-state for_k8s_version="v1.9" state="beta" >}}

On large clusters, retrieving the collection of some resource types may result in very large responses that can impact the server and client. For instance, a cluster may have tens of thousands of Pods, each of which is equivalent to roughly 2 KiB of encoded JSON. Retrieving all pods across all namespaces may result in a very large response (10-20MB) and consume a large amount of server resources.

Provided that you don't explicitly disable the `APIListChunking` [feature gate](/docs/reference/command-line-tools-reference/feature-gates/), the Kubernetes API server supports the ability to break a single large collection request into many smaller chunks while preserving the consistency of the total request. Each chunk can be returned sequentially which reduces both the total size of the request and allows user-oriented clients to display results incrementally to improve responsiveness.

To retrieve a single list in chunks, two parameters `limit` and `continue` are supported on requests against collections, and another field `continue` is returned from all **list** operations in the collection's `metadata` field. A client should specify the maximum results they wish to receive in each chunk with `limit` and the server will return up to `limit` resources in the result and include a `continue` value if there are more resources in the collection. The client can then pass this `continue` value to the server on the next request to instruct the server to return the next chunk of results. By continuing until the server returns an empty `continue` value the client can consume the full set of results.

Like a **watch** operation, a `continue` token will expire after a short amount of time (by default 5 minutes) and return a `410 Gone` if more results cannot be returned. In this case, the client will need to start from the beginning or omit the `limit` parameter.

For example, if there are 1,253 pods on the cluster and the client wants to receive chunks of 500 pods at a time, they would request those chunks as follows:

1. List all of the pods on a cluster, retrieving up to 500 pods each time.

   ```console
   GET /api/v1/pods?limit=500
   ---
   200 OK
   Content-Type: application/json

   {
     "kind": "PodList",
     "apiVersion": "v1",
     "metadata": {
       "resourceVersion":"10245",
       "continue": "ENCODED_CONTINUE_TOKEN",
       ...
     },
     "items": [...] // returns pods 1-500
   }
   ```

2. Continue the previous call, retrieving the next set of 500 pods.

   ```console
   GET /api/v1/pods?limit=500&continue=ENCODED_CONTINUE_TOKEN
   ---
   200 OK
   Content-Type: application/json

   {
     "kind": "PodList",
     "apiVersion": "v1",
     "metadata": {
       "resourceVersion":"10245",
       "continue": "ENCODED_CONTINUE_TOKEN_2",
       ...
     },
     "items": [...] // returns pods 501-1000
   }
   ```

3. Continue the previous call, retrieving the last 253 pods.

   ```console
   GET /api/v1/pods?limit=500&continue=ENCODED_CONTINUE_TOKEN_2
   ---
   200 OK
   Content-Type: application/json

   {
     "kind": "PodList",
     "apiVersion": "v1",
     "metadata": {
       "resourceVersion":"10245",
       "continue": "", // continue token is empty because we have reached the end of the list
       ...
     },
     "items": [...] // returns pods 1001-1253
   }
   ```

Notice that the `resourceVersion` of the collection remains constant across each request,
indicating the server is showing us a consistent snapshot of the pods. Pods that
are created, updated, or deleted after version `10245` would not be shown unless
you make a separate **list** request without the `continue` token.  This allows you
to break large requests into smaller chunks and then perform a **watch** operation
on the full set without missing any updates.

`remainingItemCount` is the number of subsequent items in the collection that are not
included in this response. If the **list** request contained label or field
{{< glossary_tooltip text="selectors" term_id="selector">}} then the number of
remaining items is unknown and the API server does not include a `remainingItemCount`
field in its response.
If the **list** is complete (either because it is not chunking, or because this is the
last chunk), then there are no more remaining items and the API server does not include a
`remainingItemCount` field in its response. The intended use of the `remainingItemCount`
is estimating the size of a collection.

## Receiving resources as Tables

When you run `kubectl get`, the default output format is a simple tabular representation of one or more instances of a particular resource type. In the past, clients were required to reproduce the tabular and describe output implemented in `kubectl` to perform simple lists of objects.
A few limitations of that approach include non-trivial logic when dealing with certain objects. Additionally, types provided by API aggregation or third party resources are not known at compile time. This means that generic implementations had to be in place for types unrecognized by a client.

In order to avoid potential limitations as described above, clients may request the Table representation of objects, delegating specific details of printing to the server. The Kubernetes API implements standard HTTP content type negotiation: passing an `Accept` header containing a value of `application/json;as=Table;g=meta.k8s.io;v=v1` with a `GET` call will request that the server return objects in the Table content type.

For example, list all of the pods on a cluster in the Table format.

```console
GET /api/v1/pods
Accept: application/json;as=Table;g=meta.k8s.io;v=v1
---
200 OK
Content-Type: application/json

{
    "kind": "Table",
    "apiVersion": "meta.k8s.io/v1",
    ...
    "columnDefinitions": [
        ...
    ]
}
```

For API resource types that do not have a custom Table definition known to the control plane, the API server returns a default Table response that consists of the resource's `name` and `creationTimestamp` fields.

```console
GET /apis/crd.example.com/v1alpha1/namespaces/default/resources
---
200 OK
Content-Type: application/json
...

{
    "kind": "Table",
    "apiVersion": "meta.k8s.io/v1",
    ...
    "columnDefinitions": [
        {
            "name": "Name",
            "type": "string",
            ...
        },
        {
            "name": "Created At",
            "type": "date",
            ...
        }
    ]
}
```

Not all API resource types support a Table response; for example, a {{< glossary_tooltip term_id="CustomResourceDefinition" text="CustomResourceDefinitions" >}} might not define field-to-table mappings, and an APIService that [extends the core Kubernetes API](/docs/concepts/extend-kubernetes/api-extension/apiserver-aggregation/) might not serve Table responses at all. If you are implementing a client that uses the Table information and must work against all resource types, including extensions, you should make requests that specify multiple content types in the `Accept` header. For example:

```console
Accept: application/json;as=Table;g=meta.k8s.io;v=v1, application/json
```

## Alternate representations of resources

By default, Kubernetes returns objects serialized to JSON with content type `application/json`. This is the default serialization format for the API. However, clients may request the more efficient [Protobuf representation](#protobuf-encoding) of these objects for better performance at scale. The Kubernetes API implements standard HTTP content type negotiation: passing an `Accept` header with a `GET` call will request that the server tries to return a response in your preferred media type, while sending an object in Protobuf to the server for a `PUT` or `POST` call means that you must set the `Content-Type` header appropriately.

The server will return a response with a `Content-Type` header if the requested format is supported, or the `406 Not acceptable` error if none of the media types you requested are supported. All built-in resource types support the `application/json` media type.

See the Kubernetes [API reference](/docs/reference/kubernetes-api/) for a list of supported content types for each API.

For example:

1. List all of the pods on a cluster in Protobuf format.

   ```console
   GET /api/v1/pods
   Accept: application/vnd.kubernetes.protobuf
   ---
   200 OK
   Content-Type: application/vnd.kubernetes.protobuf

   ... binary encoded PodList object
   ```

2. Create a pod by sending Protobuf encoded data to the server, but request a response in JSON.

   ```console
   POST /api/v1/namespaces/test/pods
   Content-Type: application/vnd.kubernetes.protobuf
   Accept: application/json
   ... binary encoded Pod object
   ---
   200 OK
   Content-Type: application/json

   {
     "kind": "Pod",
     "apiVersion": "v1",
     ...
   }
   ```

Not all API resource types support Protobuf; specifically, Protobuf isn't available for resources that are defined as {{< glossary_tooltip term_id="CustomResourceDefinition" text="CustomResourceDefinitions" >}} or are served via the {{< glossary_tooltip text="aggregation layer" term_id="aggregation-layer" >}}. As a client, if you might need to work with extension types you should specify multiple content types in the request `Accept` header to support fallback to JSON. For example:

```console
Accept: application/vnd.kubernetes.protobuf, application/json
```

### Kubernetes Protobuf encoding {#protobuf-encoding}

Kubernetes uses an envelope wrapper to encode Protobuf responses. That wrapper starts with a 4 byte magic number to help identify content in disk or in etcd as Protobuf (as opposed to JSON), and then is followed by a Protobuf encoded wrapper message, which describes the encoding and type of the underlying object and then contains the object.

The wrapper format is:

```console
A four byte magic number prefix:
  Bytes 0-3: "k8s\x00" [0x6b, 0x38, 0x73, 0x00]

An encoded Protobuf message with the following IDL:
  message Unknown {
    // typeMeta should have the string values for "kind" and "apiVersion" as set on the JSON object
    optional TypeMeta typeMeta = 1;

    // raw will hold the complete serialized object in protobuf. See the protobuf definitions in the client libraries for a given kind.
    optional bytes raw = 2;

    // contentEncoding is encoding used for the raw data. Unspecified means no encoding.
    optional string contentEncoding = 3;

    // contentType is the serialization method used to serialize 'raw'. Unspecified means application/vnd.kubernetes.protobuf and is usually
    // omitted.
    optional string contentType = 4;
  }

  message TypeMeta {
    // apiVersion is the group/version for this type
    optional string apiVersion = 1;
    // kind is the name of the object schema. A protobuf definition should exist for this object.
    optional string kind = 2;
  }
```

{{< note >}}
Clients that receive a response in `application/vnd.kubernetes.protobuf` that does not match the expected prefix should reject the response, as future versions may need to alter the serialization format in an incompatible way and will do so by changing the prefix.
{{< /note >}}

## Resource deletion

When you **delete** a resource this takes place in two phases.

1. _finalization_
2. removal

```yaml
{
  "kind": "ConfigMap",
  "apiVersion": "v1",
  "metadata": {
    "finalizers": {"url.io/neat-finalization", "other-url.io/my-finalizer"},
    "deletionTimestamp": nil,
  }
}
```

When a client first **delete**s a resource, the `.metadata.deletionTimestamp` is set to the current time.
Once the `.metadata.deletionTimestamp` is set, external controllers that act on finalizers
may start performing their cleanup work at any time, in any order.

Order is **not** enforced between finalizers because it would introduce significant
risk of stuck `.metadata.finalizers`.

The `.metadata.finalizers` field is shared: any actor with permission can reorder it.
If the finalizer list were processed in order, then this might lead to a situation
in which the component responsible for the first finalizer in the list is
waiting for some signal (field value, external system, or other) produced by a
component responsible for a finalizer later in the list, resulting in a deadlock.

Without enforced ordering, finalizers are free to order amongst themselves and
are not vulnerable to ordering changes in the list.

Once the last finalizer is removed, the resource is actually removed from etcd.


## Single resource API

The Kubernetes API verbs **get**, **create**, **update**, **patch**, **delete** and
**proxy** support single resources only.
These verbs with single resource support have no support for submitting
multiple resources together in an ordered or unordered list or transaction.

When clients (including kubectl) act on a list of resources, the client makes a series
of single-resource API requests, then aggregates the responses if needed.

By contrast, the Kubernetes API verbs **list** and **watch** allow getting multiple
resources, and **deletecollection** allows deleting multiple resources.

## Dry-run

 {{< feature-state for_k8s_version="v1.18" state="stable" >}}

When you use an HTTP verbs that can modify resources (`POST`, `PUT`, `PATCH`, and `DELETE`), you can submit your request in a _dry run_ mode. Dry run mode helps to evaluate a request through the typical request stages (admission chain, validation, merge conflicts) up until persisting objects to storage. The response body for the request is as close as possible to a non-dry-run response. Kubernetes guarantees that dry-run requests will not be persisted in storage or have any other side effects.


### Make a dry-run request

Dry-run is triggered by setting the `dryRun` query parameter. This parameter is a string, working as an enum, and the only accepted values are:

[empty]
: Allow side effects. You request this with a query string such as `?dryRun` or `?dryRun&pretty=true`. The response is the final object that would have been persisted, or an error if the request could not be fulfilled.

`All`
: Every stage runs as normal, except for the final storage stage where side effects are prevented.


When you set `?dryRun=All`, admission controllers are run to check that the request is valid, mutating controllers mutate the request, merge is performed on `PATCH`, fields are defaulted, and schema validation occurs. The changes are not persisted to the underlying storage, but the final object which would have been persisted is still returned to the user, along with the normal status code.

If the request would trigger an admission controller which would have side effects, the request will be failed rather than risk an unwanted side effect. All built in admission control plugins support dry-run. Additionally, admission webhooks can declare in their [configuration object](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#webhook-v1beta1-admissionregistration-k8s-io) that they do not have side effects by setting their `sideEffects` field to `None`. If a webhook actually does have side effects, then the `sideEffects` field should be set to "NoneOnDryRun", and the webhook should also be modified to understand the `DryRun` field in AdmissionReview, and prevent side effects on dry-run requests.

Here is an example dry-run request that uses `?dryRun=All`:

```console
POST /api/v1/namespaces/test/pods?dryRun=All
Content-Type: application/json
Accept: application/json
```

The response would look the same as for non-dry-run request, but the values of some generated fields may differ.


### Generated values

Some values of an object are typically generated before the object is persisted. It is important not to rely upon the values of these fields set by a dry-run request, since these values will likely be different in dry-run mode from when the real request is made. Some of these fields are:

* `name`: if `generateName` is set, `name` will have a unique random name
* `creationTimestamp` / `deletionTimestamp`: records the time of creation/deletion
* `UID`: [uniquely identifies](/docs/concepts/overview/working-with-objects/names/#uids) the object and is randomly generated (non-deterministic)
* `resourceVersion`: tracks the persisted version of the object
* Any field set by a mutating admission controller
* For the `Service` resource: Ports or IP addresses that the kube-apiserver assigns to Service objects

### Dry-run authorization

Authorization for dry-run and non-dry-run requests is identical. Thus, to make
a dry-run request, you must be authorized to make the non-dry-run request.

For example, to run a dry-run **patch** for a Deployment, you must be authorized
to perform that **patch**. Here is an example of a rule for Kubernetes
{{< glossary_tooltip text="RBAC" term_id="rbac">}} that allows patching
Deployments:

```yaml
rules:
- apiGroups: ["apps"]
  resources: ["deployments"]
  verbs: ["patch"]
```

See [Authorization Overview](/docs/reference/access-authn-authz/authorization/).

## Server Side Apply

Kubernetes' [Server Side Apply](/docs/reference/using-api/server-side-apply/)
feature allows the control plane to track managed fields for newly created objects.
Server Side Apply provides a clear pattern for managing field conflicts,
offers server-side `Apply` and `Update` operations, and replaces the
client-side functionality of `kubectl apply`.

See [Server Side Apply](/docs/reference/using-api/server-side-apply/) for more details.

## Resource versions

Resource versions are strings that identify the server's internal version of an object. Resource versions can be used by clients to determine when objects have changed, or to express data consistency requirements when getting, listing and watching resources. Resource versions must be treated as opaque by clients and passed unmodified back to the server.

You must not assume resource versions are numeric or collatable. API clients may only compare two resource versions for equality (this means that you must not compare resource versions for greater-than or less-than relationships).

### `resourceVersion` fields in metadata {#resourceversion-in-metadata}

Clients find resource versions in resources, including the resources from the response stream for a **watch**, or when using **list** to enumerate resources.

[v1.meta/ObjectMeta](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#objectmeta-v1-meta) - The `metadata.resourceVersion` of a resource instance identifies the resource version the instance was last modified at.

[v1.meta/ListMeta](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#listmeta-v1-meta) - The `metadata.resourceVersion` of a resource collection (the response to a **list**) identifies the resource version at which the collection was constructed.

### `resourceVersion` parameters in query strings {#the-resourceversion-parameter}

The **get**, **list**, and **watch** operations support the `resourceVersion` parameter.
From version v1.19, Kubernetes API servers also support the `resourceVersionMatch`
parameter on _list_ requests.

The API server interprets the `resourceVersion` parameter differently depending on the
operation you request, and on the value of `resourceVersion`. If you set
`resourceVersionMatch` then this also affects the way matching happens.

### Semantics for **get** and **list**

For **get** and **list**, the semantics of `resourceVersion` are:

**get:**

| resourceVersion unset | resourceVersion="0" | resourceVersion="{value other than 0}" |
|-----------------------|---------------------|----------------------------------------|
| Most Recent           | Any                 | Not older than                         |

**list:**

From version v1.19, Kubernetes API servers support the `resourceVersionMatch` parameter
on _list_ requests. If you set both `resourceVersion` and `resourceVersionMatch`, the
`resourceVersionMatch` parameter determines how the API server interprets
`resourceVersion`.

You should always set the `resourceVersionMatch` parameter when setting
`resourceVersion` on a **list** request. However, be prepared to handle the case
where the API server that responds is unaware of `resourceVersionMatch`
and ignores it.

Unless you have strong consistency requirements, using `resourceVersionMatch=NotOlderThan` and
a known `resourceVersion` is preferable since it can achieve better performance and scalability
of your cluster than leaving `resourceVersion` and `resourceVersionMatch` unset, which requires
quorum read to be served.

Setting the `resourceVersionMatch` parameter without setting `resourceVersion` is not valid.


This table explains the behavior of **list** requests with various combinations of
`resourceVersion` and `resourceVersionMatch`:

{{< table caption="resourceVersionMatch and paging parameters for list" >}}

| resourceVersionMatch param            | paging params                 | resourceVersion not set | resourceVersion="0"                       | resourceVersion="{value other than 0}" |
|---------------------------------------|-------------------------------|-----------------------|-------------------------------------------|----------------------------------------|
| _unset_            | _limit unset_                   | Most Recent           | Any                                       | Not older than                         |
| _unset_            | limit=\<n\>, _continue unset_     | Most Recent           | Any                                       | Exact                                  |
| _unset_            | limit=\<n\>, continue=\<token\> | Continue Token, Exact | Invalid, treated as Continue Token, Exact | Invalid, HTTP `400 Bad Request`        |
| `resourceVersionMatch=Exact`        | _limit unset_                 | Invalid               | Invalid                                   | Exact                                  |
| `resourceVersionMatch=Exact`        | limit=\<n\>, _continue unset_ | Invalid               | Invalid                                   | Exact                                  |
| `resourceVersionMatch=NotOlderThan` | _limit unset_                 | Invalid               | Any                                       | Not older than                         |
| `resourceVersionMatch=NotOlderThan` | limit=\<n\>, _continue unset_ | Invalid               | Any                                       | Not older than                         |

{{< /table >}}

{{< note >}}
If your clusterserver does not honor the `resourceVersionMatch` parameter, the behavior is the same as if you did not set it.
{{< /note >}}

The meaning of the **get** and **list** semantics are:

Any
: Return data at any resource version. The newest available resource version is preferred,
  but strong consistency is not required; data at any resource version may be served. It is possible
  for the request to return data at a much older resource version that the client has previously
  observed, particularly in high availability configurations, due to partitions or stale
  caches. Clients that cannot tolerate this should not use this semantic.

Most recent
: Return data at the most recent resource version. The returned data must be
  consistent (in detail: served from etcd via a quorum read).

Not older than
: Return data at least as new as the provided `resourceVersion`. The newest
  available data is preferred, but any data not older than the provided `resourceVersion` may be
  served.  For **list** requests to servers that honor the `resourceVersionMatch` parameter, this
  guarantees that the collection's `.metadata.resourceVersion` is not older than the requested
  `resourceVersion`, but does not make any guarantee about the `.metadata.resourceVersion` of any
  of the items in that collection.

Exact
: Return data at the exact resource version provided. If the provided `resourceVersion` is
  unavailable, the server responds with HTTP 410 "Gone".  For **list** requests to servers that honor the
  `resourceVersionMatch` parameter, this guarantees that the collection's `.metadata.resourceVersion`
  is the same as the `resourceVersion` you requested in the query string. That guarantee does
  not apply to the `.metadata.resourceVersion` of any items within that collection.

Continue Token, Exact
: Return data at the resource version of the initial paginated **list** call. The returned _continue
  tokens_ are responsible for keeping track of the initially provided resource version for all paginated
  **list** calls after the initial paginated **list**.

{{< note >}}
When you **list** resources and receive a collection response, the response includes the
[metadata](/docs/reference/generated/kubernetes-api/v1.21/#listmeta-v1-meta) of the collection as
well as [object metadata](/docs/reference/generated/kubernetes-api/v1.21/#listmeta-v1-meta)
for each item in that collection. For individual objects found within a collection response,
`.metadata.resourceVersion` tracks when that object was last updated, and not how up-to-date
the object is when served.
{{< /note >}}

When using `resourceVersionMatch=NotOlderThan` and limit is set, clients must
handle HTTP 410 "Gone" responses. For example, the client might retry with a
newer `resourceVersion` or fall back to `resourceVersion=""`.

When using `resourceVersionMatch=Exact` and `limit` is unset, clients must
verify that the collection's `.metadata.resourceVersion` matches
the requested `resourceVersion`, and handle the case where it does not. For
example, the client might fall back to a request with `limit` set.

### Semantics for **watch**

For **watch**, the semantics of resource version are:

**watch:**

{{< table caption="resourceVersion for watch" >}}

| resourceVersion unset               | resourceVersion="0"        | resourceVersion="{value other than 0}" |
|-------------------------------------|----------------------------|----------------------------------------|
| Get State and Start at Most Recent  | Get State and Start at Any | Start at Exact                         |

{{< /table >}}

The meaning of those **watch** semantics are:

Get State and Start at Any
: {{< caution >}} Watches initialized this way may return arbitrarily stale data. Please review this semantic before using it, and favor the other semantics where possible.{{< /caution >}} Start a **watch** at any resource version; the most recent resource version available is preferred, but not required. Any starting resource version is allowed. It is possible for the **watch** to start at a much older resource version that the client has previously observed, particularly in high availability configurations, due to partitions or stale caches. Clients that cannot tolerate this apparent rewinding should not start a **watch** with this semantic. To establish initial state, the **watch** begins with synthetic "Added" events for all resources instances that exist at the starting resource version. All following watch events are for all changes that occurred after the resource version the **watch** started at.

Get State and Start at Most Recent
: Start a **watch** at the most recent resource version, which must be consistent (in detail: served from etcd via a quorum read). To establish initial state, the **watch** begins with synthetic "Added" events of all resources instances that exist at the starting resource version. All following watch events are for all changes that occurred after the resource version the **watch** started at.

Start at Exact
: Start a **watch** at an exact resource version. The watch events are for all changes after the provided resource version. Unlike "Get State and Start at Most Recent" and "Get State and Start at Any", the **watch** is not started with synthetic "Added" events for the provided resource version. The client is assumed to already have the initial state at the starting resource version since the client provided the resource version.

### "410 Gone" responses

Servers are not required to serve all older resource versions and may return a HTTP `410 (Gone)` status code if a client requests a `resourceVersion` older than the server has retained. Clients must be able to tolerate `410 (Gone)` responses. See [Efficient detection of changes](#efficient-detection-of-changes) for details on how to handle `410 (Gone)` responses when watching resources.

If you request a `resourceVersion` outside the applicable limit then, depending on whether a request is served from cache or not, the API server may reply with a `410 Gone` HTTP response.

### Unavailable resource versions

Servers are not required to serve unrecognized resource versions. If you request **list** or **get** for a resource version that the API server does not recognize, then the API server may either:

* wait briefly for the resource version to become available, then timeout with a `504 (Gateway Timeout)` if the provided resource versions does not become available in a reasonable amount of time;
* respond with a `Retry-After` response header indicating how many seconds a client should wait before retrying the request.

If you request a resource version that an API server does not recognize, the kube-apiserver additionally identifies its error responses with a "Too large resource version" message.

If you make a **watch** request for an unrecognized resource version, the API server may wait indefinitely (until the request timeout) for the resource version to become available.
