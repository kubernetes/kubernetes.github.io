---
title: Kubernetes API 概念
content_type: concept
weight: 20
---
<!--
title: Kubernetes API Concepts
reviewers:
- smarterclayton
- lavalamp
- liggitt
content_type: concept
weight: 20
-->

<!-- overview -->
<!--
This page describes common concepts in the Kubernetes API.
-->
本页描述 Kubernetes API 的通用概念。

<!-- body -->
<!--
The Kubernetes API is a resource-based (RESTful) programmatic interface provided via HTTP. It supports retrieving, creating,
updating, and deleting primary resources via the standard HTTP verbs (POST, PUT, PATCH, DELETE, GET), includes additional subresources for many objects that allow fine grained authorization (such as binding a pod to a node), and can accept and serve those resources in different representations for convenience or efficiency. It also supports efficient change notifications on resources via "watches" and consistent lists to allow other components to effectively cache and synchronize the state of resources.
-->
Kubernetes API 是基于资源的（RESTful）、通过 HTTP 提供的编程接口。
API 支持通过标准的 HTTP 动词（POST、PUT、PATCH、DELETE 和  GET）
检视、创建、更新和删除主要资源，为很多允许细粒度权限控制的对象提供子资源
（如将 Pod 绑定到节点上），并且出于便利性或效率考虑，支持并提供这些资源的
不同表示形式。
Kubernetes  API 还通过 "watch" 和一致性的列表支持高效的资源变更通知，
从而允许其他组件对资源的状态进行高效的缓存和同步。

<!--
## Standard API terminology

Most Kubernetes API resource types are [objects](/docs/concepts/overview/working-with-objects/kubernetes-objects/#kubernetes-objects): they represent a concrete instance of a concept on the cluster, like a pod or namespace. A smaller number of API resource types are "virtual" - they often represent operations rather than objects, such as a permission check (use a POST with a JSON-encoded body of `SubjectAccessReview` to the `subjectaccessreviews` resource). All objects will have a unique name to allow idempotent creation and retrieval, but virtual resource types may not have unique names if they are not retrievable or do not rely on idempotency.
-->
## 标准 API 术语  {#standard-api-terminology}

大多数 Kubernetes API 资源类型都是
[对象](/zh/docs/concepts/overview/working-with-objects/kubernetes-objects/#kubernetes-objects)：
它们代表的是集群中某一概念的具体实例，例如一个 Pod 或名字空间。
为数不多的几个 API 资源类型是“虚拟的” - 它们通常代表的是操作而非对象本身，
例如访问权限检查（使用 POST 请求发送一个 JSON 编码的 `SubjectAccessReview`
负载到 `subjectaccessreviews` 资源）。
所有对象都有一个唯一的名字，以便支持幂等的创建和检视操作，不过如果虚拟资源类型
不可检视或者不要求幂等，可以不具有唯一的名字。

<!--
Kubernetes generally leverages standard RESTful terminology to describe the API concepts:

* A **resource type** is the name used in the URL (`pods`, `namespaces`, `services`)
* All resource types have a concrete representation in JSON (their object schema) which is called a **kind**
* A list of instances of a resource type is known as a **collection**
* A single instance of the resource type is called a **resource**
-->
Kubernetes 一般会利用标准的 RESTful 术语来描述 API 概念：

* **资源类型（Resource Type）** 是在 URL 中使用的名称（`pods`、`namespaces`、`services`）
* 所有资源类型都有具有一个 JSON 形式（其对象的模式定义）的具体表示，称作**类别（Kind）**
* 某资源类型的实例的列表称作 **集合（Collection）**
* 资源类型的单个实例被称作 **资源（Resource）**

<!--
All resource types are either scoped by the cluster (`/apis/GROUP/VERSION/*`) or to a namespace (`/apis/GROUP/VERSION/namespaces/NAMESPACE/*`). A namespace-scoped resource type will be deleted when its namespace is deleted and access to that resource type is controlled by authorization checks on the namespace scope. The following paths are used to retrieve collections and resources:

* Cluster-scoped resources:
  * `GET /apis/GROUP/VERSION/RESOURCETYPE` - return the collection of resources of the resource type
  * `GET /apis/GROUP/VERSION/RESOURCETYPE/NAME` - return the resource with NAME under the resource type
* Namespace-scoped resources:
  * `GET /apis/GROUP/VERSION/RESOURCETYPE` - return the collection of all instances of the resource type across all namespaces
  * `GET /apis/GROUP/VERSION/namespaces/NAMESPACE/RESOURCETYPE` - return collection of all instances of the resource type in NAMESPACE
  * `GET /apis/GROUP/VERSION/namespaces/NAMESPACE/RESOURCETYPE/NAME` - return the instance of the resource type with NAME in NAMESPACE
-->
所有资源类型要么是集群作用域的（`/apis/GROUP/VERSION/*`），要么是名字空间
作用域的（`/apis/GROUP/VERSION/namespaces/NAMESPACE/*`）。
名字空间作用域的资源类型会在其名字空间被删除时也被删除，并且对该资源类型的
访问是由定义在名字空间域中的授权检查来控制的。
下列路径用来检视集合和资源：

* 集群作用域的资源：
  * `GET /apis/GROUP/VERSION/RESOURCETYPE` - 返回指定资源类型的资源的集合
  * `GET /apis/GROUP/VERSION/RESOURCETYPE/NAME` - 返回指定资源类型下名称为 NAME 的资源
* 名字空间作用域的资源：
  * `GET /apis/GROUP/VERSION/RESOURCETYPE` - 返回所有名字空间中指定资源类型的全部实例的集合
  * `GET /apis/GROUP/VERSION/namespaces/NAMESPACE/RESOURCETYPE` - 返回名字空间 NAMESPACE 内给定资源类型的全部实例的集合
  * `GET /apis/GROUP/VERSION/namespaces/NAMESPACE/RESOURCETYPE/NAME` - 返回名字空间 NAMESPACE 中给定资源类型的名称为 NAME 的实例

<!--
Since a namespace is a cluster-scoped resource type, you can retrieve the list of all namespaces with `GET /api/v1/namespaces` and details about a particular namespace with `GET /api/v1/namespaces/NAME`.

Almost all object resource types support the standard HTTP verbs - GET, POST, PUT, PATCH, and DELETE. Kubernetes uses the term **list** to describe returning a collection of resources to distinguish from retrieving a single resource which is usually called a **get**.
-->
由于名字空间本身是一个集群作用域的资源类型，你可以通过 `GET /api/v1/namespaces/`
检视所有名字空间的列表，使用 `GET /api/v1/namespaces/NAME` 查看特定名字空间的
详细信息。

几乎所有对象资源类型都支持标准的 HTTP 动词 - GET、POST、PUT、PATCH 和 DELETE。
Kubernetes 使用术语 **list** 来描述返回资源集合的操作，以便与返回单个资源的、
通常称作 **get** 的操作相区分。

<!--
Some resource types will have one or more sub-resources, represented as sub paths below the resource:

* Cluster-scoped subresource: `GET /apis/GROUP/VERSION/RESOURCETYPE/NAME/SUBRESOURCE`
* Namespace-scoped subresource: `GET /apis/GROUP/VERSION/namespaces/NAMESPACE/RESOURCETYPE/NAME/SUBRESOURCE`

The verbs supported for each subresource will differ depending on the object - see the API documentation more information. It is not possible to access sub-resources across multiple resources - generally a new virtual resource type would be used if that becomes necessary.
-->
某些资源类型有一个或多个子资源（Sub-resource），表现为对应资源下面的子路径：

* 集群作用域的子资源：`GET /apis/GROUP/VERSION/RESOURCETYPE/NAME/SUBRESOURCE`
* 名字空间作用域的子资源：`GET /apis/GROUP/VERSION/namespaces/NAMESPACE/RESOURCETYPE/NAME/SUBRESOURCE`

取决于对象是什么，每个子资源所支持的动词有所不同 - 参见 API 文档以了解更多信息。
跨多个资源来访问其子资源是不可能的 - 如果需要这一能力，则通常意味着需要一种
新的虚拟资源类型了。

<!--
## Efficient detection of changes

To enable clients to build a model of the current state of a cluster, all Kubernetes object resource types are required to support consistent lists and an incremental change notification feed called a **watch**.  Every Kubernetes object has a `resourceVersion` field representing the version of that resource as stored in the underlying database. When retrieving a collection of resources (either namespace or cluster scoped), the response from the server will contain a `resourceVersion` value that can be used to initiate a watch against the server. The server will return all changes (creates, deletes, and updates) that occur after the supplied `resourceVersion`. This allows a client to fetch the current state and then watch for changes without missing any updates. If the client watch is disconnected they can restart a new watch from the last returned `resourceVersion`, or perform a new collection request and begin again. See [Resource Version Semantics](#resource-versions) for more detail.

For example:
-->
## 高效检测变更  {#efficient-detection-of-changes}

为了使客户端能够构造一个模型来表达集群的当前状态，所有 Kubernetes 对象资源类型
都需要支持一致的列表和一个称作 **watch** 的增量变更通知信源（feed）。
每个 Kubernetes 对象都有一个 `resourceVersion` 字段，代表该资源在下层数据库中
存储的版本。检视资源集合（名字空间作用域或集群作用域）时，服务器返回的响应
中会包含 `resourceVersion` 值，可用来向服务器发起 watch 请求。
服务器会返回所提供的 `resourceVersion` 之后发生的所有变更（创建、删除和更新）。
这使得客户端能够取回当前的状态并监视其变更，且不会错过任何变更事件。
客户端的监视连接被断开时，可以从最后返回的 `resourceVersion` 重启新的监视连接，
或者执行一个新的集合请求之后从头开始监视操作。
参阅[资源版本语义](#resource-versions)以了解更多细节。

例如：

<!--
1. List all of the pods in a given namespace.
-->
1. 列举给定名字空间中的所有 Pods：

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

<!--
2. Starting from resource version 10245, receive notifications of any creates, deletes, or updates as individual JSON objects.
-->
2. 从资源版本 10245 开始，以 JSON 对象的形式接收所有创建、删除或更新操作的通知：

   ```console
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

<!--
A given Kubernetes server will only preserve a historical list of changes for a limited time. Clusters using etcd3 preserve changes in the last 5 minutes by default.  When the requested watch operations fail because the historical version of that resource is not available, clients must handle the case by recognizing the status code `410 Gone`, clearing their local cache, performing a list operation, and starting the watch from the `resourceVersion` returned by that new list operation. Most client libraries offer some form of standard tool for this logic. (In Go this is called a `Reflector` and is located in the `k8s.io/client-go/cache` package.)
-->
给定的 Kubernetes 服务器只会保留一定的时间内发生的历史变更列表。
使用 etcd3 的集群默认保存过去 5 分钟内发生的变更。
当所请求的 watch 操作因为资源的历史版本不存在而失败，客户端必须能够处理
因此而返回的状态代码 `410 Gone`，清空其本地的缓存，重新执行 list 操作，
并基于新的 list 操作所返回的 `resourceVersion` 来开始新的 watch 操作。
大多数客户端库都能够提供某种形式的、包含此逻辑的工具。
（在 Go 语言客户端库中，这一设施称作 `Reflector`，位于
`k8s.io/client-go/cache` 包中。)

<!--
### Watch bookmarks

To mitigate the impact of short history window, we introduced a concept of `bookmark` watch event. It is a special kind of event to mark that all changes up to a given `resourceVersion` the client is requesting have already been sent. Object returned in that event is of the type requested by the request, but only `resourceVersion` field is set, e.g.:
-->
### 监视书签  {#Watch-bookmark}

为了处理历史窗口过短的问题，我们引入了 `bookmark（书签）` 监视事件的概念。
该事件是一种特殊事件，用来标示客户端所请求的、指定的 `resourceVersion` 之前
的所有变更都以被发送。该事件中返回的对象是所请求的资源类型，但其中仅包含
`resourceVersion` 字段，例如：

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

<!--
`Bookmark` events can be requested by `allowWatchBookmarks=true` option in watch requests, but clients shouldn't assume bookmarks are returned at any specific interval, nor may they assume the server will send any `bookmark` event.
-->
通过在 watch 请求中设置 `allowWatchBookmarks=true` 选项，可以请求 `bookmark`
事件，但是客户端不能假定服务器端会按某特定时间间隔返回书签事件，甚至也不能
假定服务器一定会发送 `bookmark` 事件。

<!--
## Retrieving large results sets in chunks
-->
## 分块检视大体量结果  {#retrieving-large-results-sets-in-chunks}

{{< feature-state for_k8s_version="v1.9" state="beta" >}}

<!--
On large clusters, retrieving the collection of some resource types may result in very large responses that can impact the server and client. For instance, a cluster may have tens of thousands of pods, each of which is 1-2kb of encoded JSON. Retrieving all pods across all namespaces may result in a very large response (10-20MB) and consume a large amount of server resources. Starting in Kubernetes 1.9 the server supports the ability to break a single large collection request into many smaller chunks while preserving the consistency of the total request. Each chunk can be returned sequentially which reduces both the total size of the request and allows user-oriented clients to display results incrementally to improve responsiveness.
-->
在较大规模的集群中，检视某些资源类型的集合时可能会返回较大体量的响应数据，对
服务器和客户端都会造成影响。例如，某集群可能包含数万个 Pod，每个 Pod 的 JSON
编码都有 1-2 KB 的大小。返回所有名字空间的全部 Pod 时，其结果可能体量很大
（10-20 MB）且耗用大量的服务器资源。
从 Kubernetes 1.9 开始，服务器支持将单一的大体量集合请求分解成多个小数据块
同时还保证整个请求的一致性的能力。
各个数据块可以按顺序返回，进而降低请求的尺寸，允许面向用户的客户端以增量形式
呈现返回结果，改进系统响应效果。

<!--
To retrieve a single list in chunks, two new parameters `limit` and `continue`
are supported on collection requests and a new field `continue` is returned
from all list operations in the list `metadata` field. A client should specify
the maximum results they wish to receive in each chunk with `limit` and the
server will return up to `limit` resources in the result and include a
`continue` value if there are more resources in the collection. The client can
then pass this `continue` value to the server on the next request to instruct
the server to return the next chunk of results. By continuing until the server
returns an empty `continue` value the client can consume the full set of
results.
-->
为了用分块的形式返回一个列表，集合请求上可以设置两个新的参数 `limit` 和
`continue`，并且所有 list 操作的返回结果列表的 `metadata` 字段中会包含一个
新的 `continue` 字段。
客户端应该将 `limit` 设置为希望在每个数据块中收到的结果个数上限，而服务器则
会在结果中至多返回 `limit` 个资源并在集合中还有更多资源的时候包含一个
`continue` 值。客户端在下次请求时则可以将此 `continue` 值传递给服务器，
告知后者要从何处开始返回结果的下一个数据块。
通过重复这一操作直到服务器端返回空的 `continue` 值，客户端可以受到结果的
全集。

<!--
Like a watch operation, a `continue` token will expire after a short amount of time (by default 5 minutes) and return a `410 Gone` if more results cannot be returned. In this case, the client will need to start from the beginning or omit the `limit` parameter.

For example, if there are 1,253 pods on the cluster and the client wants to receive chunks of 500 pods at a time, they would request those chunks as follows:
-->
与 watch 操作类似，`continue` 令牌也会在很短的时间（默认为 5 分钟）内过期，
并在无法返回更多结果时返回 `410 Gone` 代码。
这时，客户端需要从头开始执行上述检视操作或者忽略 `limit` 参数。

例如，如果集群上有 1253 个 Pods，客户端希望每次收到包含至多 500 个 Pod 的
数据块，它应按下面的步骤来请求数据块：

<!--
1. List all of the pods on a cluster, retrieving up to 500 pods each time.
-->
1. 列举集群中所有 Pod，每次接收至多 500 个 Pods：

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
<!--
2. Continue the previous call, retrieving the next set of 500 pods.
-->
2. 继续前面的调用，返回下一组 500 个 Pods：

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

<!--
3. Continue the previous call, retrieving the last 253 pods.
-->
3. 继续前面的调用，返回最后 253 个 Pods：

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

<!--
Note that the `resourceVersion` of the list remains constant across each request, indicating the server is showing us a consistent snapshot of the pods. Pods that are created, updated, or deleted after version `10245` would not be shown unless the user makes a list request without the `continue` token.  This allows clients to break large requests into smaller chunks and then perform a watch operation on the full set without missing any updates.
-->
注意 list 操作的 `resourceVersion` 在每个请求中都设置的是同一个数值，
这表明服务器要向我们展示一个一致的 Pods 快照视图。
在版本 `10245` 之后创建、更新或删除的 Pods 都不会显示出来，除非用户发出
list 请求时不指定 `continue` 令牌。
这一设计使得客户端能够将较大的响应切分为较小的数据块，且能够对较大的集合
执行监视动作而不会错失任何更新事件。

<!--
## Receiving resources as Tables

The output from the `kubectl get` command is a simple tabular representation of one or more instances of a particular resource type. In the past, clients were required to reproduce the tabular and describe output implemented in `kubectl` to perform simple lists of objects.
A few limitations of that approach include non-trivial logic when dealing with certain objects. Additionally, types provided by API aggregation or third party resources are not known at compile time. This means that generic implementations had to be in place for types unrecognized by a client.
-->
## 以表格形式接收资源  {#receiving-resources-as-tables}

`kubectl get` 命令的输出是一个包含一个或多个资源的简单表格形式。
过去，客户端需要重复 `kubectl` 中所实现的表格输出和描述输出逻辑，以执行
简单的对象列表操作。
这一方法在处理某些对象时，需要引入不容忽视的逻辑。
此外，[API 聚合](/zh/docs/concepts/extend-kubernetes/api-extension/apiserver-aggregation/)
和[定制资源](/zh/docs/concepts/extend-kubernetes/api-extension/custom-resources/)
所提供的资源类型都是编译时不可预知的。这意味着，客户端必须针对无法
识别的类型提供通用的实现逻辑。

<!--
In order to avoid potential limitations as described above, clients may request the Table representation of objects, delegating specific details of printing to the server. The Kubernetes API implements standard HTTP content type negotiation: passing an `Accept` header containing a value of `application/json;as=Table;g=meta.k8s.io;v=v1beta1` with a `GET` call will request that the server return objects in the Table content type.

For example:
-->
为了避免上述各种潜在的局限性，客户端可以请求服务器端返回对象的表格（Table）
表现形式，从而将打印输出的特定细节委托给服务器。
Kubernetes API 实现标准的 HTTP 内容类型（Content Type）协商：为 `GET` 调用
传入一个值为 `application/json;as=Table;g=meta.k8s.io;v=v1beta1` 的 `Accept`
头部即可请求服务器以 Table 的内容类型返回对象。

例如，以 Table 格式列举集群中所有 Pods：

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

<!--
For API resource types that do not have a custom Table definition on the
server, a default Table response is returned by the server, consisting of the
resource's `name` and `creationTimestamp` fields.
-->
对于在服务器上不存在定制的 Table 定义的 API 资源类型而言，服务器会返回
一个默认的 Table 响应，其中包含资源的 `name` 和 `creationTimestamp` 字段。

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

<!--
Table responses are available beginning in version 1.10 of the kube-apiserver.
As such, not all API resource types will support a Table response,
specifically when using a client against older clusters. Clients that must
work against all resource types, or can potentially deal with older clusters,
should specify multiple content types in their `Accept` header to support
fallback to non-Tabular JSON:
-->
`kube-apiserver` 从 1.10 版本开始提供 Table 响应。
因此，并非所有 API 资源类型都支持 Table 响应，尤其是使用客户端访问较老的集群时。
如果客户端需要能够处理所有资源类型，或者有可能需要与较老的集群交互，
则需要在其 `Accept` 头部设定多个内容类型值，以便可以回退到非表格形式的 JSON
表示。

```
Accept: application/json;as=Table;g=meta.k8s.io;v=v1beta1, application/json
```

<!--
## Alternate representations of resources

By default, Kubernetes returns objects serialized to JSON with content type `application/json`. This is the default serialization format for the API. However, clients may request the more efficient Protobuf representation of these objects for better performance at scale. The Kubernetes API implements standard HTTP content type negotiation: passing an `Accept` header with a `GET` call will request that the server return objects in the provided content type, while sending an object in Protobuf to the server for a `PUT` or `POST` call takes the `Content-Type` header. The server will return a `Content-Type` header if the requested format is supported, or the `406 Not acceptable` error if an invalid content type is provided.

See the API documentation for a list of supported content types for each API.

For example:
-->
## 资源的其他表示形式  {#alternate-representations-of-resources}

默认情况下，Kubernetes 返回 JSON 序列化的的对象并设定内容类型为
`application/json`。这是 API 的默认序列化格式。
不过，客户端也可出于大规模环境中更佳性能的需求而请求对象的更为高效的 Protobuf
表现形式。
Kubernetes API 实现了标准的 HTTP 内容类型协商：为 `GET` 调用传递一个 `Accept`
头部来请求服务器以所指定的内容类型返回对象，同时在通过 `PUT` 或 `POST` 调用
向服务器发送 Protobuf 格式的对象时提供 `Content-Type` 头部。
服务器会能够支持所请求的格式时返回 `Content-Type` 头部，并在所提供的内容类型
不合法时返回 `406 Not acceptable（无法接受）` 错误。

请参阅 API 文档了解每个 API 所支持的内容类型。

例如：

<!--
1. List all of the pods on a cluster in Protobuf format.
-->
1. 以 Protobuf 格式列举集群上的所有 Pods：

```console
GET /api/v1/pods
Accept: application/vnd.kubernetes.protobuf
---
200 OK
Content-Type: application/vnd.kubernetes.protobuf

... binary encoded PodList object
```

<!--
2. Create a pod by sending Protobuf encoded data to the server, but request a response in JSON.
-->
2. 通过向服务器发送 Protobuf 编码的数据创建 Pod，但请求以 JSON 形式接收响应：

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

<!--
Not all API resource types will support Protobuf, specifically those defined
via Custom Resource Definitions or those that are API extensions. Clients that
must work against all resource types should specify multiple content types in
their `Accept` header to support fallback to JSON:
-->
并非所有 API 资源类型都支持 Protobuf，尤其是那些通过定制资源定义（CRD）或通过
API 扩展而加入的资源。如果客户端必须能够处理所有资源类型，则应在其 `Accept`
头部指定多种内容类型以便可以回退到 JSON 格式：

```console
Accept: application/vnd.kubernetes.protobuf, application/json
```

<!--
### Protobuf encoding

Kubernetes uses an envelope wrapper to encode Protobuf responses. That wrapper starts with a 4 byte magic number to help identify content in disk or in etcd as Protobuf (as opposed to JSON), and then is followed by a Protobuf encoded wrapper message, which describes the encoding and type of the underlying object and then contains the object.

The wrapper format is:
-->
### Protobuf encoding

Kubernetes 使用封套形式来对 Protobuf 响应进行编码。
封套外层由 4 个字节的特殊数字开头，便于从磁盘文件或 etcd 中辩识 Protobuf
格式的（而不是 JSON）数据。
接下来存放的是 Protobuf 编码的封套消息，其中描述下层对象的编码和类型，最后
才是对象本身。

封套格式如下：

<!--
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
-->
```console
四个字节的特殊数字前缀：
  字节 0-3: "k8s\x00" [0x6b, 0x38, 0x73, 0x00]

使用下面 IDL 来编码的 Protobuf 消息：
  message Unknown {
    // typeMeta 应该包含 "kind" 和 "apiVersion" 的字符串值，就像
    // 对应的 JSON 对象中所设置的那样
    optional TypeMeta typeMeta = 1;

    // raw 中将保存用 protobuf 序列化的完整对象。
    // 参阅客户端库中为指定 kind 所作的 protobuf 定义
    optional bytes raw = 2;

    // contentEncoding 用于 raw 数据的编码格式。未设置此值意味着没有特殊编码。
    optional string contentEncoding = 3;

    // contentType 包含 raw 数据所采用的序列化方法。
    // 未设置此值意味着  application/vnd.kubernetes.protobuf，且通常被忽略
    optional string contentType = 4;
  }

  message TypeMeta {
    // apiVersion 是 type 对应的组名/版本
    optional string apiVersion = 1;
    // kind 是对象模式定义的名称。此对象应该存在一个 protobuf 定义。
    optional string kind = 2;
  }
```

<!--
Clients that receive a response in `application/vnd.kubernetes.protobuf` that does not match the expected prefix should reject the response, as future versions may need to alter the serialization format in an incompatible way and will do so by changing the prefix.
-->
收到 `application/vnd.kubernetes.protobuf` 格式响应的客户端在响应与预期的前缀
不匹配时应该拒绝响应，因为将来的版本可能需要以某种不兼容的方式更改序列化格式，
并且这种更改是通过变更前缀完成的。

<!--
## Resource deletion

Resources are deleted in two phases: 1) finalization, and 2) removal.
-->
## 资源删除  {#resource-deletion}

资源删除要经过两个阶段：1) 终止（finalization），和 2）去除。

```json
{
  "kind": "ConfigMap",
  "apiVersion": "v1",
  "metadata": {
    "finalizers": {"url.io/neat-finalization", "other-url.io/my-finalizer"},
    "deletionTimestamp": nil,
  }
}
```

<!--
When a client first deletes a resource, the `.metadata.deletionTimestamp` is
set to the current time.  Once the `.metadata.deletionTimestamp` is set,
external controllers that act on finalizers may start performing their cleanup
work at any time, in any order.  Order is NOT enforced because it introduces
significant risk of stuck `.metadata.finalizers`.  `.metadata.finalizers` is a
shared field, any actor with permission can reorder it.  If the finalizer list
is processed in order, then this can lead to a situation in which the
component responsible for the first finalizer in the list is waiting for a
signal (field value, external system, or other) produced by a component
responsible for a finalizer later in the list, resulting in a deadlock.
Without enforced ordering finalizers are free to order amongst themselves and
are not vulnerable to ordering changes in the list.

Once the last finalizer is removed, the resource is actually removed from
etcd.
-->
当客户端首先删除某资源时，其 `.metadata.deletionTimestamp` 会被设置为当前时间。
一旦 `.metadata.deletionTimestamp` 被设置，则对终结器（finalizers）执行动作
的外部控制器就可以在任何时候、以任何顺序执行其清理工作。
这里不强调顺序是因为很可能带来 `.metadata.finalizers` 被锁定的风险。
`.metadata.finalizers` 是一个共享的字段，任何具有相关权限的主体都可以对其
执行重排序的操作。如果终结器列表要按顺序处理，则很可能导致负责列表中第一个
终结器的组件要等待负责列表中排序靠后的终结器的组件的信号（可能是字段值变更、
外部系统或者其他形式），从而导致死锁行为。
在不对终结器顺序作强制要求的情况下，终结器可以自行排序，且不会因为其在列表
中的顺序而引入任何不稳定因素。

当最后一个终结器也被移除时，资源才真正从 etcd 中移除。

<!--
## Single resource API

API verbs GET, CREATE, UPDATE, PATCH, DELETE and PROXY support single resources only.
These verbs with single resource support have no support for submitting
multiple resources together in an ordered or unordered list or transaction.
Clients including kubectl will parse a list of resources and make
single-resource API requests.

API verbs LIST and WATCH support getting multiple resources, and
DELETECOLLECTION supports deleting multiple resources.
-->
## 单个资源 API  {#single-resource-api}

API 动词 GET、CREATE、UPDATE、PATCH、DELETE 和 PROXY 仅支持单个资源。
这些支持单一资源的动词不支持以有序或无序列表甚或事务的形式同时提交给
多个资源。
包括 kubectl 在内的客户端将解析资源的列表，并执行单一资源的 API 请求。

API 动词 LIST 和 WATCH 支持获取多个资源，而 DELETECOLLECTION 支持删除多个
资源。

<!--
## Dry-run
-->
## 试运行  {#dry-run}

{{< feature-state for_k8s_version="v1.18" state="stable" >}}

<!--
The modifying verbs (`POST`, `PUT`, `PATCH`, and `DELETE`) can accept requests in a _dry run_ mode. Dry run mode helps to evaluate a request through the typical request stages (admission chain, validation, merge conflicts) up until persisting objects to storage. The response body for the request is as close as possible to a non-dry-run response. The system guarantees that dry-run requests will not be persisted in storage or have any other side effects.
-->
修改性质的动词（`POST`、`PUT`、`PATCH` 和 `DELETE`）可以支持 _试运行（dry
run）_ 模式的请求。试运行模式可帮助通过典型的请求阶段（准入控制链、合法性
检查、合并冲突）来评估请求，只是最终的对象不会写入存储。请求的响应主体与
非试运行模式下的响应尽可能接近。系统会保证试运行模式的请求不会被写入到存储
中，也不会产生其他副作用。

<!--
### Make a dry-run request

Dry-run is triggered by setting the `dryRun` query parameter. This parameter is a string, working as an enum, and the only accepted values are:

* `All`: Every stage runs as normal, except for the final storage stage. Admission controllers are run to check that the request is valid, mutating controllers mutate the request, merge is performed on `PATCH`, fields are defaulted, and schema validation occurs. The changes are not persisted to the underlying storage, but the final object which would have been persisted is still returned to the user, along with the normal status code. If the request would trigger an admission controller which would have side effects, the request will be failed rather than risk an unwanted side effect. All built in admission control plugins support dry-run. Additionally, admission webhooks can declare in their [configuration object](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#webhook-v1beta1-admissionregistration-k8s-io) that they do not have side effects by setting the sideEffects field to "None". If a webhook actually does have side effects, then the sideEffects field should be set to "NoneOnDryRun", and the webhook should also be modified to understand the `DryRun` field in AdmissionReview, and prevent side effects on dry-run requests.
* Leave the value empty, which is also the default: Keep the default modifying behavior.

For example:
-->
### 发起试运行请求  {#make-a-dry-run-request}

通过设置 `dryRun` 查询参数可以触发试运行模式。此参数是一个字符串，以枚举值
的形式工作且可接受的值只有：

* `All`：每个阶段被会正常运行，除了最后的存储阶段。准入控制器会被运行来检查请求
  是否合法，变更性（Mutating）控制器会变更请求，`PATCH` 请求也会触发合并操作，
  对象字段的默认值也会被设置，且基于模式定义的合法性检查也会被执行。
  所生成的变更不会被写入到下层的持久性存储中，但本来会写入到数据库中的最终对象
  会和正常的状态代码一起被返回给用户。如果请求会触发准入控制器而该准入控制器
  带有一定的副作用，则请求会失败而不是冒险产生不希望的副作用。
  所有的内置准入控制器插件都支持试运行模式。此外，准入控制 Webhook 也可在其
  [配置对象](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#webhook-v1beta1-admissionregistration-k8s-io)
  中通过将 `sideEffects` 字段设置为 "None" 来声明自身不会产生副作用。
  如果某 Webhook 确实会产生副作用，那么 `sideEffects` 字段应该设置为 "NoneOnDryRun"，
  并且 Webhook 应该被更改以支持 AdmissionReview 中的 `dryRun` 字段，从而避免
  在试运行时产生副作用。

* 空字符串（也即默认值）：保留默认的修改行为。

例如：

```console
POST /api/v1/namespaces/test/pods?dryRun=All
Content-Type: application/json
Accept: application/json
```

<!--
The response would look the same as for non-dry-run request, but the values of some generated fields may differ.
-->
响应会与非试运行模式请求的响应看起来相同，只是某些生成字段的值可能会不同。

<!--
### Dry-run authorization

Authorization for dry-run and non-dry-run requests is identical. Thus, to make
a dry-run request, the user must be authorized to make the non-dry-run request.

For example, to run a dry-run `PATCH` for Deployments, you must have the
`PATCH` permission for Deployments, as in the example of the RBAC rule below.
-->
### 试运行的授权    {#dry-run-authorization}

试运行和非试运行请求的鉴权是完全相同的。因此，要发起一个试运行请求，用户必须
被授权执行非试运行请求。

例如，要在 Deployment 对象上试运行 `PATCH` 操作，你必须具有对 Deployment 执行
`PATCH` 操作的访问权限，如下面的 RBAC 规则所示：

```yaml
rules:
- apiGroups: ["extensions", "apps"]
  resources: ["deployments"]
  verbs: ["patch"]
```

<!--
See [Authorization Overview](/docs/reference/access-authn-authz/authorization/).
-->
参阅[鉴权概述](/zh/docs/reference/access-authn-authz/authorization/)以了解鉴权细节。

<!--
### Generated values

Some values of an object are typically generated before the object is persisted. It is important not to rely upon the values of these fields set by a dry-run request, since these values will likely be different in dry-run mode from when the real request is made. Some of these fields are:

* `name`: if `generateName` is set, `name` will have a unique random name
* `creationTimestamp`/`deletionTimestamp`: records the time of creation/deletion
* `UID`: uniquely identifies the object and is randomly generated (non-deterministic)
* `resourceVersion`: tracks the persisted version of the object
* Any field set by a mutating admission controller
* For the `Service` resource: Ports or IPs that kube-apiserver assigns to v1.Service objects
-->
### 生成的值  {#generated-values}

对象的某些值通常是在对象被写入数据库之前生成的。很重要的一点是不要依赖试运行
请求为这些字段所设置的值，因为试运行模式下所得到的这些值与真实请求所获得的
值很可能不同。这类字段有：

* `name`：如果设置了 `generateName` 字段，则 `name` 会获得一个唯一的随机名称
* `creationTimestamp`/`deletionTimestamp`：记录对象的创建/删除时间
* `UID`：唯一性标识对象，取值随机生成（非确定性）
* `resourceVersion`： 跟踪对象的持久化（存储）版本
* 变更性准入控制器所设置的字段
* 对于 `Service` 资源：`kube-apiserver` 为 `v1.Service` 对象分配的端口和 IP

<!--
## Server Side Apply
-->
## 服务器端应用  {#server-side-apply}

{{< feature-state for_k8s_version="v1.16" state="beta" >}}

<!--
Starting from Kubernetes v1.18, you can enable the
[Server Side Apply](/docs/reference/using-api/server-side-apply/)
feature so that the control plane tracks managed fields for all newly created objects.
Server Side Apply provides a clear pattern for managing field conflicts,
offers server-side `Apply` and `Update` operations, and replaces the
client-side functionality of `kubectl apply`. For more details about this
feature, see the section on
[Server Side Apply](/docs/reference/using-api/server-side-apply/).
-->
从 Kubernetes v1.18 开始，可以启用[服务器端应用](/zh/docs/reference/using-api/server-side-apply/)功能
特性，启用该特性后，控制面会跟踪所有新创建的对象的托管字段。服务器端应用提供了一种简洁的模式来管理字段冲突，提供服务器端的 `Apply` 和 `Update` 操作，并取代了
`kubectl apply` 的客户端功能。有关该特性的详细描述，请参见[服务器端应用](/zh/docs/reference/using-api/server-side-apply/)章节

<!--
## Resource Versions

Resource versions are strings that identify the server's internal version of an object. Resource versions can be used by clients to determine when objects have changed, or to express data consistency requirements when getting, listing and watching resources. Resource versions must be treated as opaque by clients and passed unmodified back to the server. For example, clients must not assume resource versions are numeric, and may only compare two resource version for equality (i.e. must not compare resource versions for greater-than or less-than relationships).
-->
## 资源版本   {#resource-versions}

资源版本采用字符串来表达，用来标示对象的服务器端内部版本。
客户端可以使用资源版本来判定对象是否被更改，或者在读取、列举或监视资源时
用来表达数据一致性需求。
客户端必需将资源版本视为不透明的对象，将其原封不动地传递回服务器端。
例如，客户端一定不能假定资源版本是某种数值标识，也不可以对两个资源版本值
进行比较看其是否相同（也就是不可以比较两个版本值以判断其中一个比另一个
大或小）。

<!--
### ResourceVersion in metadata

Clients find resource versions in resources, including the resources in watch events, and list responses returned from the server:

[v1.meta/ObjectMeta](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#objectmeta-v1-meta) - The `metadata.resourceVersion` of a resource instance identifies the resource version the instance was last modified at.

[v1.meta/ListMeta](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#listmeta-v1-meta) - The `metadata.resourceVersion` of a resource collection (i.e. a list response) identifies the resource version at which the list response was constructed.
-->
### `metadata` 中的 `resourceVersion`  {#resourceVersion-in-metadata}

客户端可以在资源中看到资源版本信息，这里的资源包括从服务器返回的 Watch 事件
以及 list 操作响应：

[v1.meta/ObjectMeta](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#objectmeta-v1-meta) - 资源
的 `metadata.resourceVersion` 值标明该实例上次被更改时的资源版本。

[v1.meta/ListMeta](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#listmeta-v1-meta) - 资源集合
（即 list 操作的响应）的 `metadata.resourceVersion` 所标明的是 list 响应被构造
时的资源版本。

<!--
### The ResourceVersion Parameter

The get, list and watch operations support the `resourceVersion` parameter.

The exact meaning of this parameter differs depending on the operation and the value of `resourceVersion`.

For get and list, the semantics of resource version are:

**Get:**
-->
### `resourceVersion` 参数   {#the-resourceversion-parameter}

GET、LIST 和 WATCH 操作都支持 `resourceVersion` 参数。

参数的具体含义取决于所执行的操作和所给的 `resourceVersion` 值：

对于 GET 和 LIST 而言，资源版本的语义为：

**GET：**

<!--
| resourceVersion unset | resourceVersion="0" | resourceVersion="{value other than 0}" |
|------------------------|---------------------|----------------------------------------|
| Most Recent           | Any                 | Not older than                         |
-->
| resourceVersion 未设置 | resourceVersion="0" | resourceVersion="\<非零值\>" |
|------------------------|---------------------|----------------------------------------|
| 最新版本               | 任何版本            | 不老于给定版本                         |


**LIST：**

<!--
v1.19+ API servers and newer support the `resourceVersionMatch` parameter, which
determines how resourceVersion is applied to list calls.  It is highly
recommended that `resourceVersionMatch` be set for list calls where
`resourceVersion` is set. If `resourceVersion` is unset, `resourceVersionMatch`
is not allowed.  For backward compatibility, clients must tolerate the server
ignoring `resourceVersionMatch`:
-->
v1.19 及以上版本的 API 服务器支持 `resourceVersionMatch` 参数，用以确定如何对
LIST 调用应用 resourceVersion 值。
强烈建议在为 LIST 调用设置了 `resourceVersion` 时也设置 `resourceVersionMatch`。
如果 `resourceVersion` 未设置，则 `resourceVersionMatch` 是不允许设置的。
为了向后兼容，客户端必须能够容忍服务器在某些场景下忽略 `resourceVersionMatch` 的行为：

<!--
- When using `resourceVersionMatch=NotOlderThan` and limit is set, clients must
  handle HTTP 410 "Gone" responses. For example, the client might retry with a
  newer `resourceVersion` or fall back to `resourceVersion=""`.

- When using `resourceVersionMatch=Exact` and `limit` is unset, clients must
  verify that the `resourceVersion` in the `ListMeta` of the response matches
  the requested `resourceVersion`, and handle the case where it does not. For
  example, the client might fall back to a request with `limit` set.
-->
- 当设置 `resourceVersionMatch=NotOlderThan` 且指定了 `limit` 时，客户端必须能够
  处理 HTTP 410 "Gone" 响应。例如，客户端可以使用更新一点的 `resourceVersion`
  来重试，或者回退到 `resourceVersion=""` （即允许返回任何版本）。

- 当设置了 `resourceVersionMatch=Exact` 且未指定 `limit` 时，客户端必须验证
  响应数据中 `ListMeta` 的 `resourceVersion` 与所请求的 `resourceVersion` 匹配，
  并处理二者可能不匹配的情况。例如，客户端可以重试设置了 `limit` 的请求。

<!--
Unless you have strong consistency requirements, using `resourceVersionMatch=NotOlderThan` and
a known `resourceVersion` is preferable since it can achieve better performance and scalability
of your cluster than leaving `resourceVersion` and `resourceVersionMatch` unset, which requires
quorum read to be served.
-->
除非你对一致性有着非常强烈的需求，使用 `resourceVersionMatch=NotOlderThan`
同时为 `resourceVersion` 设定一个已知值是优选的交互方式，因为与不设置
`resourceVersion` 和 `resourceVersionMatch` 相比，这种配置可以取得更好的
集群性能和可扩缩性。后者需要提供带票选能力的读操作。

<!--
{{</* table caption="resourceVersionMatch and paging parameters for list" */>}}

| resourceVersionMatch param            | paging params                 | resourceVersion unset | resourceVersion="0"                       | resourceVersion="{value other than 0}" |
|---------------------------------------|-------------------------------|-----------------------|-------------------------------------------|----------------------------------------|
| resourceVersionMatch unset            | limit unset                   | Most Recent           | Any                                       | Not older than                         |
| resourceVersionMatch unset            | limit=\<n\>, continue unset     | Most Recent           | Any                                       | Exact                                  |
| resourceVersionMatch unset            | limit=\<n\>, continue=\<token\> | Continue Token, Exact | Invalid, treated as Continue Token, Exact | Invalid, HTTP `400 Bad Request`        |
| resourceVersionMatch=Exact [1]        | limit unset                   | Invalid               | Invalid                                   | Exact                                  |
| resourceVersionMatch=Exact [1]        | limit=\<n\>, continue unset     | Invalid               | Invalid                                   | Exact                                  |
| resourceVersionMatch=NotOlderThan [1] | limit unset                   | Invalid               | Any                                       | Not older than                         |
| resourceVersionMatch=NotOlderThan [1] | limit=\<n\>, continue unset     | Invalid               | Any                                       | Not older than                         |

{{</* /table */>}}

**Footnotes:**

[1] If the server does not honor the `resourceVersionMatch` parameter, it is treated as if it is unset.
-->

{{< table caption="list 操作的 resourceVersionMatch 与分页参数" >}}

| resourceVersionMatch 参数               | 分页参数                        | resourceVersion 未设置  | resourceVersion="0"                     | resourceVersion="\<非零值\>"     |
|-----------------------------------------|---------------------------------|-------------------------|-----------------------------------------|----------------------------------|
| resourceVersionMatch 未设置             | limit 未设置                      | 最新版本                | 任意版本                                | 不老于指定版本                   |
| resourceVersionMatch 未设置             | limit=\<n\>, continue 未设置        | 最新版本                | 任意版本                                | 精确匹配                         |
| resourceVersionMatch 未设置             | limit=\<n\>, continue=\<token\>     | 从 token 开始、精确匹配 | 非法请求，视为从 token 开始、精确匹配  | 非法请求，返回 HTTP `400 Bad Request` |
| resourceVersionMatch=Exact [1]         | limit 未设置                      | 非法请求                | 非法请求                                | 精确匹配                         |
| resourceVersionMatch=Exact [1]         | limit=\<n\>, continue 未设置        | 非法请求                | 非法请求                                | 精确匹配                         |
| resourceVersionMatch=NotOlderThan [1]  | limit 未设置             | 非法请求                | 任意版本                                | 不老于指定版本                   |
| resourceVersionMatch=NotOlderThan [1]  | limit=\<n\>, continue 未设置 | 非法请求                | 任意版本                                | 不老于指定版本                   |

{{< /table >}}

**脚注：**

[1] 如果服务器无法正确处理 `resourceVersionMatch` 参数，其行为与未设置该参数相同。
</small>

<!--
The meaning of the get and list semantics are:

- **Most Recent:** Return data at the most recent resource version. The returned data must be
  consistent (i.e. served from etcd via a quorum read).
- **Any:** Return data at any resource version. The newest available resource version is preferred,
  but strong consistency is not required; data at any resource version may be served. It is possible
  for the request to return data at a much older resource version that the client has previously
  observed, particularly in high availability configurations, due to partitions or stale
  caches. Clients that cannot tolerate this should not use this semantic.
-->
GET 和 LIST 操作的语义含义如下：

- **最新版本：** 返回资源版本为最新的数据。所返回的数据必须一致
  （通过票选读操作从 etcd 中取出）。
- **任意版本：** 返回任意资源版本的数据。优选最新可用的资源版本，不过不能保证
  强一致性；返回的数据可能是任何资源版本的。请求返回的数据有可能是客户端以前
  看到过的很老的资源版本。尤其在某些高可用配置环境中，网络分区或者高速缓存
  未被更新等状态都可能导致这种状况。不能容忍这种不一致性的客户端不应采用此
  语义。
<!--
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
-->
- **不老于指定版本：** 返回至少比所提供的 `resourceVersion` 还要新的数据。
  优选最新的可用数据，不过最终提供的可能是不老于所给 `resourceVersion` 的任何版本。
  对于发给能够正确处理 `resourceVersionMatch` 参数的服务器的 LIST 请求，此语义
  保证 `ListMeta` 中的 `resourceVersion` 不老于请求的 `resourceVersion`，不过
  不对列表条目之 `ObjectMeta` 的 `resourceVersion` 提供任何保证。
  这是因为 `ObjectMeta.resourceVersion` 所跟踪的是列表条目对象上次更新的时间，
  而不是对象被返回时是否是最新。

- **确定版本：** 返回精确匹配所给资源版本的数据。如果所指定的 resourceVersion
  的数据不可用，服务器会响应 HTTP 410 "Gone"。
  对于发送给能够正确处理 `resourceVersionMatch` 参数的服务器的 LIST 请求而言，
  此语义会保证 ListMeta 中的 `resourceVersion` 与所请求的 `resourceVersion`
  匹配， 不过不对列表条目之 `ObjectMeta` 的 `resourceVersion` 提供任何保证。
  这是因为 `ObjectMeta.resourceVersion` 所跟踪的是列表条目对象上次更新的时间，
  而不是对象被返回时是否是最新。

- **Continue 令牌、精确匹配：** 返回原先带分页参数的 LIST 调用中指定的资源版本的数据。
  在最初的带分页参数的 LIST 调用之后，所有分页式的 LIST 调用都使用所返回的 Continue
  令牌来跟踪最初提供的资源版本，

<!--
For watch, the semantics of resource version are:
-->
对于 WATCH 操作而言，资源版本的语义如下：

**WATCH：**

<!--
{{< table caption="resourceVersion for watch" >}}

| resourceVersion unset               | resourceVersion="0"        | resourceVersion="{value other than 0}" |
|-------------------------------------|----------------------------|----------------------------------------|
| Get State and Start at Most Recent  | Get State and Start at Any | Start at Exact                         |

{{< /table >}}
-->

{{< table caption="watch 操作的 resourceVersion 设置" >}}

| resourceVersion 未设置    | resourceVersion="0"      | resourceVersion="\<非零值\>" |
|---------------------------|--------------------------|------------------------------|
| 读取状态并从最新版本开始  | 读取状态并从任意版本开始 | 从指定版本开始               |

{{< /table >}}

<!--
The meaning of the watch semantics are:

- **Get State and Start at Most Recent:** Start a watch at the most recent
  resource version, which must be consistent (i.e. served from etcd via a
  quorum read). To establish initial state, the watch begins with synthetic
  "Added" events of all resources instances that exist at the starting resource
  version. All following watch events are for all changes that occurred after
  the resource version the watch started at.
-->
WATCH 操作语义的含义如下：

- **读取状态并从最新版本开始：** 从最新的资源版本开始 WATCH 操作。这里的
  最新版本必须是一致的（即通过票选读操作从 etcd 中取出）。为了建立初始状态，
  WATCH 首先会处理一组合成的 "Added" 事件，这些事件涵盖在初始资源版本中存在
  的所有资源实例。
  所有后续的 WATCH 事件都是关于 WATCH 开始时所处资源版本之后发生的变更。

<!--
- **Get State and Start at Any:** Warning: Watches initialize this way may
  return arbitrarily stale data! Please review this semantic before using it,
  and favor the other semantics where possible. Start a watch at any resource
  version, the most recent resource version available is preferred, but not
  required; any starting resource version is allowed. It is possible for the
  watch to start at a much older resource version that the client has previously
  observed, particularly in high availability configurations, due to partitions
  or stale caches. Clients that cannot tolerate this should not start a watch
  with this semantic. To establish initial state, the watch begins with
  synthetic "Added" events for all resources instances that exist at the
  starting resource version. All following watch events are for all changes that
  occurred after the resource version the watch started at.
-->
- **读取状态并从任意版本开始：** 警告：通过这种方式初始化的 WATCH 操作可能会
  返回任何状态的停滞数据。请在使用此语义之前执行复核，并在可能的情况下采用其他
  语义。此语义会从任意资源版本开始执行 WATCH 操作，优选最新的可用的资源版本，
  不过不是必须的；采用任何资源版本作为起始版本都是被允许的。
  WATCH 操作有可能起始于客户端已经观测到的很老的版本。在高可用配置环境中，因为
  网络分裂或者高速缓存未及时更新的原因都会造成此现象。
  如果客户端不能容忍这种不一致性，就不要使用此语义来启动 WATCH 操作。
  为了建立初始状态，WATCH 首先会处理一组合成的 "Added" 事件，这些事件涵盖在
  初始资源版本中存在的所有资源实例。
  所有后续的 WATCH 事件都是关于 WATCH 开始时所处资源版本之后发生的变更。

<!--
- **Start at Exact:** Start a watch at an exact resource version. The watch
  events are for all changes after the provided resource version. Unlike "Get
  State and Start at Most Recent" and "Get State and Start at Any", the watch is
  not started with synthetic "Added" events for the provided resource version.
  The client is assumed to already have the initial state at the starting
  resource version since the client provided the resource version.
-->
- **从指定版本开始：** 从某确切资源版本开始执行 WATCH 操作。WATCH 事件都是
  关于 WATCH 开始时所处资源版本之后发生的变更。与前面两种语义不同，WATCH 操作
  开始的时候不会生成或处理为所提供资源版本合成的 "Added" 事件。
  我们假定客户端既然能够提供确切资源版本，就应该已经拥有了起始资源版本对应的初始状态。

<!--
### "410 Gone" responses

Servers are not required to serve all older resource versions and may return a
HTTP `410 (Gone)` status code if a client requests a resourceVersion older
than the server has retained. Clients must be able to tolerate `410 (Gone)`
responses. See [Efficient detection of
changes](#efficient-detection-of-changes) for details on how to handle `410
(Gone)` responses when watching resources.

If you request a a resourceVersion outside the applicable limit then,
depending on whether a request is served from cache or not, the API server may
reply with a `410 Gone` HTTP response.
-->
### "410 Gone" 响应     {#410-gone-responses}

服务器不需要提供所有老的资源版本，在客户端请求的是早于服务器端所保留版本的
`resourceVersion` 时，可以返回 HTTP `410 (Gone)` 状态码。
客户端必须能够容忍 `410 (Gone)` 响应。
参阅[高效检测变更](#efficient-detection-of-changes)以了解如何在监测资源时
处理 `410 (Gone)` 响应。

如果所请求的 `resourceVersion` 超出了可应用的 `limit`，那么取决于请求是否
是通过高速缓存来满足的，API 服务器可能会返回一个 `410 Gone` HTTP 响应。

<!--
### Unavailable resource versions

Servers are not required to serve unrecognized resource versions. List and Get requests for unrecognized resource versions may wait briefly for the resource version to become available, should timeout with a `504 (Gateway Timeout)` if the provided resource versions does not become available in a reasonable amount of time, and may respond with a `Retry-After` response header indicating how many seconds a client should wait before retrying the request. Currently the kube-apiserver also identifies these responses with a "Too large resource version" message. Watch requests for a unrecognized resource version may wait indefinitely (until the request timeout) for the resource version to become available.
-->
### 不可用的资源版本  {#unavailable-resource-versions}

服务器不必未无法识别的资源版本提供服务。针对无法识别的资源版本的 LIST 和 GET 请求
可能会短暂等待，以期资源版本可用。如果所给的资源版本在一定的时间段内仍未变得
可用，服务器应该超时并返回 `504 (Gateway Timeout)`，且可在响应中添加
`Retry-After` 响应头部字段，标明客户端在再次尝试之前应该等待多少秒钟。
目前，`kube-apiserver` 也能使用 `Too large resource version（资源版本过高）`
消息来标识这类响应。针对某无法识别的资源版本的 WATCH 操作可能会无限期
（直到请求超时）地等待下去，直到资源版本可用。

