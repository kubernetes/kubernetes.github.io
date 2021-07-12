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
This page describes common concepts in the Kubernetes API.


<!-- body -->
The Kubernetes API is a resource-based (RESTful) programmatic interface provided via HTTP. It supports retrieving, creating,
updating, and deleting primary resources via the standard HTTP verbs (POST, PUT, PATCH, DELETE, GET), includes additional subresources for many objects that allow fine grained authorization (such as binding a pod to a node), and can accept and serve those resources in different representations for convenience or efficiency. It also supports efficient change notifications on resources via "watches" and consistent lists to allow other components to effectively cache and synchronize the state of resources.

## Standard API terminology

Most Kubernetes API resource types are [objects](/docs/concepts/overview/working-with-objects/kubernetes-objects/#kubernetes-objects): they represent a concrete instance of a concept on the cluster, like a pod or namespace. A smaller number of API resource types are "virtual" - they often represent operations rather than objects, such as a permission check (use a POST with a JSON-encoded body of `SubjectAccessReview` to the `subjectaccessreviews` resource). All objects will have a unique name to allow idempotent creation and retrieval, but virtual resource types may not have unique names if they are not retrievable or do not rely on idempotency.

Kubernetes generally leverages standard RESTful terminology to describe the API concepts:

* A **resource type** is the name used in the URL (`pods`, `namespaces`, `services`)
* All resource types have a concrete representation in JSON (their object schema) which is called a **kind**
* A list of instances of a resource type is known as a **collection**
* A single instance of the resource type is called a **resource**

All resource types are either scoped by the cluster (`/apis/GROUP/VERSION/*`) or to a namespace (`/apis/GROUP/VERSION/namespaces/NAMESPACE/*`). A namespace-scoped resource type will be deleted when its namespace is deleted and access to that resource type is controlled by authorization checks on the namespace scope. The following paths are used to retrieve collections and resources:

* Cluster-scoped resources:

  * `GET /apis/GROUP/VERSION/RESOURCETYPE` - return the collection of resources of the resource type
  * `GET /apis/GROUP/VERSION/RESOURCETYPE/NAME` - return the resource with NAME under the resource type

* Namespace-scoped resources:

  * `GET /apis/GROUP/VERSION/RESOURCETYPE` - return the collection of all instances of the resource type across all namespaces
  * `GET /apis/GROUP/VERSION/namespaces/NAMESPACE/RESOURCETYPE` - return collection of all instances of the resource type in NAMESPACE
  * `GET /apis/GROUP/VERSION/namespaces/NAMESPACE/RESOURCETYPE/NAME` - return the instance of the resource type with NAME in NAMESPACE

Since a namespace is a cluster-scoped resource type, you can retrieve the list of all namespaces with `GET /api/v1/namespaces` and details about a particular namespace with `GET /api/v1/namespaces/NAME`.

Almost all object resource types support the standard HTTP verbs - GET, POST, PUT, PATCH, and DELETE. Kubernetes uses the term **list** to describe returning a collection of resources to distinguish from retrieving a single resource which is usually called a **get**.

Some resource types will have one or more sub-resources, represented as sub paths below the resource:

* Cluster-scoped subresource: `GET /apis/GROUP/VERSION/RESOURCETYPE/NAME/SUBRESOURCE`
* Namespace-scoped subresource: `GET /apis/GROUP/VERSION/namespaces/NAMESPACE/RESOURCETYPE/NAME/SUBRESOURCE`

The verbs supported for each subresource will differ depending on the object - see the API documentation for more information. It is not possible to access sub-resources across multiple resources - generally a new virtual resource type would be used if that becomes necessary.


## Efficient detection of changes

To enable clients to build a model of the current state of a cluster, all Kubernetes object resource types are required to support consistent lists and an incremental change notification feed called a **watch**.  Every Kubernetes object has a `resourceVersion` field representing the version of that resource as stored in the underlying database. When retrieving a collection of resources (either namespace or cluster scoped), the response from the server will contain a `resourceVersion` value that can be used to initiate a watch against the server. The server will return all changes (creates, deletes, and updates) that occur after the supplied `resourceVersion`. This allows a client to fetch the current state and then watch for changes without missing any updates. If the client watch is disconnected they can restart a new watch from the last returned `resourceVersion`, or perform a new collection request and begin again. See [Resource Version Semantics](#resource-versions) for more detail.

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

2. Starting from resource version 10245, receive notifications of any creates, deletes, or updates as individual JSON objects.

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

A given Kubernetes server will only preserve a historical list of changes for a limited time. Clusters using etcd3 preserve changes in the last 5 minutes by default.  When the requested watch operations fail because the historical version of that resource is not available, clients must handle the case by recognizing the status code `410 Gone`, clearing their local cache, performing a list operation, and starting the watch from the `resourceVersion` returned by that new list operation. Most client libraries offer some form of standard tool for this logic. (In Go this is called a `Reflector` and is located in the `k8s.io/client-go/cache` package.)

### Watch bookmarks

To mitigate the impact of short history window, we introduced a concept of `bookmark` watch event. It is a special kind of event to mark that all changes up to a given `resourceVersion` the client is requesting have already been sent. Object returned in that event is of the type requested by the request, but only `resourceVersion` field is set, e.g.:

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

`Bookmark` events can be requested by `allowWatchBookmarks=true` option in watch requests, but clients shouldn't assume bookmarks are returned at any specific interval, nor may they assume the server will send any `bookmark` event.

## Retrieving large results sets in chunks

{{< feature-state for_k8s_version="v1.9" state="beta" >}}

On large clusters, retrieving the collection of some resource types may result in very large responses that can impact the server and client. For instance, a cluster may have tens of thousands of pods, each of which is 1-2kb of encoded JSON. Retrieving all pods across all namespaces may result in a very large response (10-20MB) and consume a large amount of server resources. Starting in Kubernetes 1.9 the server supports the ability to break a single large collection request into many smaller chunks while preserving the consistency of the total request. Each chunk can be returned sequentially which reduces both the total size of the request and allows user-oriented clients to display results incrementally to improve responsiveness.

To retrieve a single list in chunks, two new parameters `limit` and `continue` are supported on collection requests and a new field `continue` is returned from all list operations in the list `metadata` field. A client should specify the maximum results they wish to receive in each chunk with `limit` and the server will return up to `limit` resources in the result and include a `continue` value if there are more resources in the collection. The client can then pass this `continue` value to the server on the next request to instruct the server to return the next chunk of results. By continuing until the server returns an empty `continue` value the client can consume the full set of results.

Like a watch operation, a `continue` token will expire after a short amount of time (by default 5 minutes) and return a `410 Gone` if more results cannot be returned. In this case, the client will need to start from the beginning or omit the `limit` parameter.

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

Note that the `resourceVersion` of the list remains constant across each request, 
indicating the server is showing us a consistent snapshot of the pods. Pods that 
are created, updated, or deleted after version `10245` would not be shown unless 
the user makes a list request without the `continue` token.  This allows clients 
to break large requests into smaller chunks and then perform a watch operation 
on the full set without missing any updates. 

`remainingItemCount` is the number of subsequent items in the list which are not 
included in this list response. If the list request contained label or field selectors, 
then the number of remaining items is unknown and the API server does not include 
a `remainingItemCount` field in its response. If the list is complete (either 
because it is not chunking or because this is the last chunk), then there are no 
more remaining items and the API server does not include a `remainingItemCount` 
field in its response. The intended use of the `remainingItemCount` is estimating 
the size of a collection.


## Receiving resources as Tables

`kubectl get` is a simple tabular representation of one or more instances of a particular resource type. In the past, clients were required to reproduce the tabular and describe output implemented in `kubectl` to perform simple lists of objects.
A few limitations of that approach include non-trivial logic when dealing with certain objects. Additionally, types provided by API aggregation or third party resources are not known at compile time. This means that generic implementations had to be in place for types unrecognized by a client.

In order to avoid potential limitations as described above, clients may request the Table representation of objects, delegating specific details of printing to the server. The Kubernetes API implements standard HTTP content type negotiation: passing an `Accept` header containing a value of `application/json;as=Table;g=meta.k8s.io;v=v1beta1` with a `GET` call will request that the server return objects in the Table content type.

For example, list all of the pods on a cluster in the Table format.

```console
GET /api/v1/pods
Accept: application/json;as=Table;g=meta.k8s.io;v=v1beta1
---
200 OK
Content-Type: application/json

{
    "kind": "Table",
    "apiVersion": "meta.k8s.io/v1beta1",
    ...
    "columnDefinitions": [
        ...
    ]
}
```

For API resource types that do not have a custom Table definition on the server, a default Table response is returned by the server, consisting of the resource's `name` and `creationTimestamp` fields.

```console
GET /apis/crd.example.com/v1alpha1/namespaces/default/resources
---
200 OK
Content-Type: application/json
...

{
    "kind": "Table",
    "apiVersion": "meta.k8s.io/v1beta1",
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

Table responses are available beginning in version 1.10 of the kube-apiserver. As such, not all API resource types will support a Table response, specifically when using a client against older clusters. Clients that must work against all resource types, or can potentially deal with older clusters, should specify multiple content types in their `Accept` header to support fallback to non-Tabular JSON:

```console
Accept: application/json;as=Table;g=meta.k8s.io;v=v1beta1, application/json
```


## Alternate representations of resources

By default, Kubernetes returns objects serialized to JSON with content type `application/json`. This is the default serialization format for the API. However, clients may request the more efficient Protobuf representation of these objects for better performance at scale. The Kubernetes API implements standard HTTP content type negotiation: passing an `Accept` header with a `GET` call will request that the server return objects in the provided content type, while sending an object in Protobuf to the server for a `PUT` or `POST` call takes the `Content-Type` header. The server will return a `Content-Type` header if the requested format is supported, or the `406 Not acceptable` error if an invalid content type is provided.

See the API documentation for a list of supported content types for each API.

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

Not all API resource types will support Protobuf, specifically those defined via Custom Resource Definitions or those that are API extensions. Clients that must work against all resource types should specify multiple content types in their `Accept` header to support fallback to JSON:

```console
Accept: application/vnd.kubernetes.protobuf, application/json
```

### Protobuf encoding

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

Clients that receive a response in `application/vnd.kubernetes.protobuf` that does not match the expected prefix should reject the response, as future versions may need to alter the serialization format in an incompatible way and will do so by changing the prefix.

## Resource deletion

Resources are deleted in two phases: 1) finalization, and 2) removal.

```go
{
  "kind": "ConfigMap",
  "apiVersion": "v1",
  "metadata": {
    "finalizers": {"url.io/neat-finalization", "other-url.io/my-finalizer"},
    "deletionTimestamp": nil,
  }
}
```

When a client first deletes a resource, the `.metadata.deletionTimestamp` is set to the current time.
Once the `.metadata.deletionTimestamp` is set, external controllers that act on finalizers
may start performing their cleanup work at any time, in any order.
Order is NOT enforced because it introduces significant risk of stuck `.metadata.finalizers`.
`.metadata.finalizers` is a shared field, any actor with permission can reorder it.
If the finalizer list is processed in order, then this can lead to a situation
in which the component responsible for the first finalizer in the list is
waiting for a signal (field value, external system, or other) produced by a
component responsible for a finalizer later in the list, resulting in a deadlock.
Without enforced ordering finalizers are free to order amongst themselves and
are not vulnerable to ordering changes in the list.

Once the last finalizer is removed, the resource is actually removed from etcd.


## Single resource API

API verbs GET, CREATE, UPDATE, PATCH, DELETE and PROXY support single resources only.
These verbs with single resource support have no support for submitting
multiple resources together in an ordered or unordered list or transaction.
Clients including kubectl will parse a list of resources and make
single-resource API requests.

API verbs LIST and WATCH support getting multiple resources, and
DELETECOLLECTION supports deleting multiple resources.

## Dry-run

 {{< feature-state for_k8s_version="v1.18" state="stable" >}}

The modifying verbs (`POST`, `PUT`, `PATCH`, and `DELETE`) can accept requests in a _dry run_ mode. Dry run mode helps to evaluate a request through the typical request stages (admission chain, validation, merge conflicts) up until persisting objects to storage. The response body for the request is as close as possible to a non-dry-run response. The system guarantees that dry-run requests will not be persisted in storage or have any other side effects.


### Make a dry-run request

Dry-run is triggered by setting the `dryRun` query parameter. This parameter is a string, working as an enum, and the only accepted values are:

* `All`: Every stage runs as normal, except for the final storage stage. Admission controllers are run to check that the request is valid, mutating controllers mutate the request, merge is performed on `PATCH`, fields are defaulted, and schema validation occurs. The changes are not persisted to the underlying storage, but the final object which would have been persisted is still returned to the user, along with the normal status code. If the request would trigger an admission controller which would have side effects, the request will be failed rather than risk an unwanted side effect. All built in admission control plugins support dry-run. Additionally, admission webhooks can declare in their [configuration object](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#webhook-v1beta1-admissionregistration-k8s-io) that they do not have side effects by setting the sideEffects field to "None". If a webhook actually does have side effects, then the sideEffects field should be set to "NoneOnDryRun", and the webhook should also be modified to understand the `DryRun` field in AdmissionReview, and prevent side effects on dry-run requests.
* Leave the value empty, which is also the default: Keep the default modifying behavior.

For example:

```console
POST /api/v1/namespaces/test/pods?dryRun=All
Content-Type: application/json
Accept: application/json
```

The response would look the same as for non-dry-run request, but the values of some generated fields may differ.

### Dry-run authorization

Authorization for dry-run and non-dry-run requests is identical. Thus, to make
a dry-run request, the user must be authorized to make the non-dry-run request.

For example, to run a dry-run `PATCH` for Deployments, you must have the
`PATCH` permission for Deployments, as in the example of the RBAC rule below.

```yaml
rules:
- apiGroups: ["extensions", "apps"]
  resources: ["deployments"]
  verbs: ["patch"]
```

See [Authorization Overview](/docs/reference/access-authn-authz/authorization/).

### Generated values

Some values of an object are typically generated before the object is persisted. It is important not to rely upon the values of these fields set by a dry-run request, since these values will likely be different in dry-run mode from when the real request is made. Some of these fields are:

* `name`: if `generateName` is set, `name` will have a unique random name
* `creationTimestamp`/`deletionTimestamp`: records the time of creation/deletion
* `UID`: uniquely identifies the object and is randomly generated (non-deterministic)
* `resourceVersion`: tracks the persisted version of the object
* Any field set by a mutating admission controller
* For the `Service` resource: Ports or IPs that kube-apiserver assigns to v1.Service objects

## Server Side Apply

Starting from Kubernetes v1.18, you can enable the
[Server Side Apply](/docs/reference/using-api/server-side-apply/)
feature so that the control plane tracks managed fields for all newly created objects.
Server Side Apply provides a clear pattern for managing field conflicts,
offers server-side `Apply` and `Update` operations, and replaces the
client-side functionality of `kubectl apply`. For more details about this
feature, see the section on
[Server Side Apply](/docs/reference/using-api/server-side-apply/).

## Resource Versions

Resource versions are strings that identify the server's internal version of an object. Resource versions can be used by clients to determine when objects have changed, or to express data consistency requirements when getting, listing and watching resources. Resource versions must be treated as opaque by clients and passed unmodified back to the server. For example, clients must not assume resource versions are numeric, and may only compare two resource versions for equality (i.e. must not compare resource versions for greater-than or less-than relationships).

### ResourceVersion in metadata

Clients find resource versions in resources, including the resources in watch events, and list responses returned from the server:

[v1.meta/ObjectMeta](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#objectmeta-v1-meta) - The `metadata.resourceVersion` of a resource instance identifies the resource version the instance was last modified at.

[v1.meta/ListMeta](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#listmeta-v1-meta) - The `metadata.resourceVersion` of a resource collection (i.e. a list response) identifies the resource version at which the list response was constructed.

### The ResourceVersion Parameter

The get, list, and watch operations support the `resourceVersion` parameter.

The exact meaning of this parameter differs depending on the operation and the value of `resourceVersion`.

For get and list, the semantics of resource version are:

**Get:**

| resourceVersion unset | resourceVersion="0" | resourceVersion="{value other than 0}" |
|-----------------------|---------------------|----------------------------------------|
| Most Recent           | Any                 | Not older than                         |

**List:**

v1.19+ API servers support the `resourceVersionMatch` parameter, which
determines how resourceVersion is applied to list calls.  It is highly
recommended that `resourceVersionMatch` be set for list calls where
`resourceVersion` is set. If `resourceVersion` is unset, `resourceVersionMatch`
is not allowed.  For backward compatibility, clients must tolerate the server
ignoring `resourceVersionMatch`:

- When using `resourceVersionMatch=NotOlderThan` and limit is set, clients must
  handle HTTP 410 "Gone" responses. For example, the client might retry with a
  newer `resourceVersion` or fall back to `resourceVersion=""`.
- When using `resourceVersionMatch=Exact` and `limit` is unset, clients must
  verify that the `resourceVersion` in the `ListMeta` of the response matches
  the requested `resourceVersion`, and handle the case where it does not. For
  example, the client might fall back to a request with `limit` set.

Unless you have strong consistency requirements, using `resourceVersionMatch=NotOlderThan` and
a known `resourceVersion` is preferable since it can achieve better performance and scalability
of your cluster than leaving `resourceVersion` and `resourceVersionMatch` unset, which requires
quorum read to be served.

{{< table caption="resourceVersionMatch and paging parameters for list" >}}

| resourceVersionMatch param            | paging params                 | resourceVersion unset | resourceVersion="0"                       | resourceVersion="{value other than 0}" |
|---------------------------------------|-------------------------------|-----------------------|-------------------------------------------|----------------------------------------|
| resourceVersionMatch unset            | limit unset                   | Most Recent           | Any                                       | Not older than                         |
| resourceVersionMatch unset            | limit=\<n\>, continue unset     | Most Recent           | Any                                       | Exact                                  |
| resourceVersionMatch unset            | limit=\<n\>, continue=\<token\> | Continue Token, Exact | Invalid, treated as Continue Token, Exact | Invalid, HTTP `400 Bad Request`        |
| resourceVersionMatch=Exact [1]        | limit unset                   | Invalid               | Invalid                                   | Exact                                  |
| resourceVersionMatch=Exact [1]        | limit=\<n\>, continue unset     | Invalid               | Invalid                                   | Exact                                  |
| resourceVersionMatch=NotOlderThan [1] | limit unset                   | Invalid               | Any                                       | Not older than                         |
| resourceVersionMatch=NotOlderThan [1] | limit=\<n\>, continue unset     | Invalid               | Any                                       | Not older than                         |

{{< /table >}}

**Footnotes:**

[1] If the server does not honor the `resourceVersionMatch` parameter, it is treated as if it is unset.

The meaning of the get and list semantics are:

- **Most Recent:** Return data at the most recent resource version. The returned data must be
  consistent (i.e. served from etcd via a quorum read).

- **Any:** Return data at any resource version. The newest available resource version is preferred,
  but strong consistency is not required; data at any resource version may be served. It is possible
  for the request to return data at a much older resource version that the client has previously
  observed, particularly in high availability configurations, due to partitions or stale
  caches. Clients that cannot tolerate this should not use this semantic.
- **Not older than:** Return data at least as new as the provided resourceVersion. The newest
  available data is preferred, but any data not older than the provided resourceVersion may be
  served.  For list requests to servers that honor the resourceVersionMatch parameter, this
  guarantees that resourceVersion in the ListMeta is not older than the requested resourceVersion,
  but does not make any guarantee about the resourceVersion in the ObjectMeta of the list items
  since ObjectMeta.resourceVersion tracks when an object was last updated, not how up-to-date the
  object is when served.

- **Exact:** Return data at the exact resource version provided. If the provided resourceVersion is
  unavailable, the server responds with HTTP 410 "Gone".  For list requests to servers that honor the
  resourceVersionMatch parameter, this guarantees that resourceVersion in the ListMeta is the same as
  the requested resourceVersion, but does not make any guarantee about the resourceVersion in the
  ObjectMeta of the list items since ObjectMeta.resourceVersion tracks when an object was last
  updated, not how up-to-date the object is when served.
- **Continue Token, Exact:** Return data at the resource version of the initial paginated list
  call. The returned Continue Tokens are responsible for keeping track of the initially provided
  resource version for all paginated list calls after the initial paginated list call.

For watch, the semantics of resource version are:

**Watch:**

{{< table caption="resourceVersion for watch" >}}

| resourceVersion unset               | resourceVersion="0"        | resourceVersion="{value other than 0}" |
|-------------------------------------|----------------------------|----------------------------------------|
| Get State and Start at Most Recent  | Get State and Start at Any | Start at Exact                         |

{{< /table >}}

The meaning of the watch semantics are:

- **Get State and Start at Most Recent:** Start a watch at the most recent resource version, which must be consistent (i.e. served from etcd via a quorum read). To establish initial state, the watch begins with synthetic "Added" events of all resources instances that exist at the starting resource version. All following watch events are for all changes that occurred after the resource version the watch started at.
- **Get State and Start at Any:** Warning: Watches initialize this way may return arbitrarily stale data! Please review this semantic before using it, and favor the other semantics where possible. Start a watch at any resource version, the most recent resource version available is preferred, but not required; any starting resource version is allowed. It is possible for the watch to start at a much older resource version that the client has previously observed, particularly in high availability configurations, due to partitions or stale caches. Clients that cannot tolerate this should not start a watch with this semantic. To establish initial state, the watch begins with synthetic "Added" events for all resources instances that exist at the starting resource version. All following watch events are for all changes that occurred after the resource version the watch started at.
- **Start at Exact:** Start a watch at an exact resource version. The watch events are for all changes after the provided resource version. Unlike "Get State and Start at Most Recent" and "Get State and Start at Any", the watch is not started with synthetic "Added" events for the provided resource version. The client is assumed to already have the initial state at the starting resource version since the client provided the resource version.

### "410 Gone" responses

Servers are not required to serve all older resource versions and may return a HTTP `410 (Gone)` status code if a client requests a resourceVersion older than the server has retained. Clients must be able to tolerate `410 (Gone)` responses. See [Efficient detection of changes](#efficient-detection-of-changes) for details on how to handle `410 (Gone)` responses when watching resources.

If you request a a resourceVersion outside the applicable limit then, depending on whether a request is served from cache or not, the API server may reply with a `410 Gone` HTTP response.

### Unavailable resource versions

Servers are not required to serve unrecognized resource versions. List and Get requests for unrecognized resource versions may wait briefly for the resource version to become available, should timeout with a `504 (Gateway Timeout)` if the provided resource versions does not become available in a reasonable amount of time, and may respond with a `Retry-After` response header indicating how many seconds a client should wait before retrying the request. Currently, the kube-apiserver also identifies these responses with a "Too large resource version" message. Watch requests for an unrecognized resource version may wait indefinitely (until the request timeout) for the resource version to become available.
