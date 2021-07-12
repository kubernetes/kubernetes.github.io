---
title: 服务器端应用（Server-Side Apply）
content_type: concept
weight: 25
min-kubernetes-server-version: 1.16
---
<!-- 
title: Server-Side Apply
reviewers:
- smarterclayton
- apelisse
- lavalamp
- liggitt
content_type: concept
weight: 25
min-kubernetes-server-version: 1.16
-->

<!-- overview -->

{{< feature-state for_k8s_version="v1.16" state="beta" >}}

<!-- 
## Introduction

Server Side Apply helps users and controllers manage their resources through
declarative configurations. Clients can create and/or modify their
[objects](/docs/concepts/overview/working-with-objects/kubernetes-objects/)
declaratively by sending their fully specified intent.
-->
## 简介 {#introduction}

服务器端应用协助用户、控制器通过声明式配置的方式管理他们的资源。
客户端可以发送完整描述的目标（A fully specified intent），
声明式地创建和/或修改
[对象](/zh/docs/concepts/overview/working-with-objects/kubernetes-objects/)。

<!-- 
A fully specified intent is a partial object that only includes the fields and
values for which the user has an opinion. That intent either creates a new
object or is [combined](#merge-strategy), by the server, with the existing object.

The system supports multiple appliers collaborating on a single object.
-->
一个完整描述的目标并不是一个完整的对象，仅包括能体现用户意图的字段和值。
该目标（intent）可以用来创建一个新对象，
也可以通过服务器来实现与现有对象的[合并](#merge-strategy)。

系统支持多个应用者（appliers）在同一个对象上开展协作。

<!-- 
Changes to an object's fields are tracked through a "[field management](#field-management)"
mechanism. When a field's value changes, ownership moves from its current
manager to the manager making the change. When trying to apply an object,
fields that have a different value and are owned by another manager will
result in a [conflict](#conflicts). This is done in order to signal that the
operation might undo another collaborator's changes. Conflicts can be forced,
in which case the value will be overridden, and the ownership will be
transferred.
-->
“[字段管理（field management）](#field-management)”机制追踪对象字段的变化。
当一个字段值改变时，其所有权从当前管理器（manager）转移到施加变更的管理器。
当尝试将新配置应用到一个对象时，如果字段有不同的值，且由其他管理器管理，
将会引发[冲突](#conflicts)。
冲突引发警告信号：此操作可能抹掉其他协作者的修改。
冲突可以被刻意忽略，这种情况下，值将会被改写，所有权也会发生转移。

<!-- 
If you remove a field from a configuration and apply the configuration, server
side apply checks if there are any other field managers that also own the
field.  If the field is not owned by any other field managers, it is either
deleted from the live object or reset to its default value, if it has one. The
same rule applies to associative list or map items.
-->
当你从配置文件中删除一个字段，然后应用这个配置文件，
这将触发服务端应用检查此字段是否还被其他字段管理器拥有。
如果没有，那就从活动对象中删除该字段；如果有，那就重置为默认值。
该规则同样适用于 list 或 map 项目。

<!-- 
Server side apply is meant both as a replacement for the original `kubectl
apply` and as a simpler mechanism for controllers to enact their changes.

If you have Server Side Apply enabled, the control plane tracks managed fields
for all newly created objects.
-->
服务器端应用既是原有 `kubectl apply` 的替代品，
也是控制器发布自身变化的一个简化机制。

如果你启用了服务器端应用，控制平面就会跟踪被所有新创建对象管理的字段。

<!-- 
## Field Management

Compared to the `last-applied` annotation managed by `kubectl`, Server Side
Apply uses a more declarative approach, which tracks a user's field management,
rather than a user's last applied state. This means that as a side effect of
using Server Side Apply, information about which field manager manages each
field in an object also becomes available.
-->
## 字段管理 {#field-management}

相对于通过 `kubectl` 管理的注解 `last-applied`，
服务器端应用使用了一种更具声明式特点的方法：
它持续的跟踪用户的字段管理，而不仅仅是最后一次的执行状态。
这就意味着，作为服务器端应用的一个副作用，
关于用哪一个字段管理器负责管理对象中的哪个字段的这类信息，都要对外界开放了。

<!-- 
For a user to manage a field, in the Server Side Apply sense, means that the
user relies on and expects the value of the field not to change. The user who
last made an assertion about the value of a field will be recorded as the
current field manager. This can be done either by changing the value with
`POST`, `PUT`, or non-apply `PATCH`, or by including the field in a config sent
to the Server Side Apply endpoint. When using Server-Side Apply, trying to
change a field which is managed by someone else will result in a rejected
request (if not forced, see [Conflicts](#conflicts)).
-->
用户管理字段这件事，在服务器端应用的场景中，意味着用户依赖并期望字段的值不要改变。
最后一次对字段值做出断言的用户将被记录到当前字段管理器。
这可以通过发送 `POST`、 `PUT`、 
或非应用（non-apply）方式的 `PATCH` 等命令来修改字段值的方式实现，
或通过把字段放在配置文件中，然后发送到服务器端应用的服务端点的方式实现。
当使用服务器端应用，尝试着去改变一个被其他人管理的字段，
会导致请求被拒绝（在没有设置强制执行时，参见[冲突](#conflicts)）。

<!-- 
When two or more appliers set a field to the same value, they share ownership of
that field. Any subsequent attempt to change the value of the shared field, by any of
the appliers, results in a conflict. Shared field owners may give up ownership
of a field by removing it from their configuration.

Field management is stored in a`managedFields` field that is part of an object's
[`metadata`](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#objectmeta-v1-meta).

A simple example of an object created by Server Side Apply could look like this:
-->
如果两个或以上的应用者均把同一个字段设置为相同值，他们将共享此字段的所有权。
后续任何改变共享字段值的尝试，不管由那个应用者发起，都会导致冲突。
共享字段的所有者可以放弃字段的所有权，这只需从配置文件中删除该字段即可。

字段管理的信息存储在 `managedFields` 字段中，该字段是对象的 
[`metadata`](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#objectmeta-v1-meta)
中的一部分。

服务器端应用创建对象的简单示例如下：

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

<!-- 
The above object contains a single manager in `metadata.managedFields`. The
manager consists of basic information about the managing entity itself, like
operation type, API version, and the fields managed by it.

This field is managed by the  API server and should not be changed by
the user.
-->
上述对象在 `metadata.managedFields` 中包含了唯一的管理器。
管理器由管理实体自身的基本信息组成，比如操作类型、API 版本、以及它管理的字段。

{{< note >}}
该字段由 API 服务器管理，用户不应该改动它。
{{< /note >}}

<!-- 
Nevertheless it is possible to change `metadata.managedFields` through an
`Update` operation. Doing so is highly discouraged, but might be a reasonable
option to try if, for example, the `managedFields` get into an inconsistent
state (which clearly should not happen).

The format of the `managedFields` is described in the
[API](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#fieldsv1-v1-meta).
-->
不过，执行 `Update` 操作修改 `metadata.managedFields` 也是可实现的。
强烈不鼓励这么做，但当发生如下情况时，
比如 `managedFields` 进入不一致的状态（显然不应该发生这种情况），
这么做也是一个合理的尝试。

`managedFields` 的格式在
[API](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#fieldsv1-v1-meta)
文档中描述。

<!-- 
## Conflicts

A conflict is a special status error that occurs when an `Apply` operation tries
to change a field, which another user also claims to manage. This prevents an
applier from unintentionally overwriting the value set by another user. When
this occurs, the applier has 3 options to resolve the conflicts:
-->
## 冲突 {#conflicts}

冲突是一种特定的错误状态，
发生在执行 `Apply` 改变一个字段，而恰巧该字段被其他用户声明过主权时。
这可以防止一个应用者不小心覆盖掉其他用户设置的值。
冲突发生时，应用者有三种办法来解决它：

<!-- 
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
-->
* **覆盖前值，成为唯一的管理器：** 如果打算覆盖该值（或应用者是一个自动化部件，比如控制器），
  应用者应该设置查询参数 `force` 为 true，然后再发送一次请求。
  这将强制操作成功，改变字段的值，从所有其他管理器的 managedFields 条目中删除指定字段。

* **不覆盖前值，放弃管理权：** 如果应用者不再关注该字段的值，
  可以从配置文件中删掉它，再重新发送请求。
  这就保持了原值不变，并从 managedFields 的应用者条目中删除该字段。

* **不覆盖前值，成为共享的管理器：** 如果应用者仍然关注字段值，并不想覆盖它，
  他们可以在配置文件中把字段的值改为和服务器对象一样，再重新发送请求。
  这样在不改变字段值的前提下，
  就实现了字段管理被应用者和所有声明了管理权的其他的字段管理器共享。

<!-- 
## Managers

Managers identify distinct workflows that are modifying the object (especially
useful on conflicts!), and can be specified through the `fieldManager` query
parameter as part of a modifying request. It is required for the apply endpoint,
though kubectl will default it to `kubectl`. For other updates, its default is
computed from the user-agent.
-->
## 管理器 {#managers}

管理器识别出正在修改对象的工作流程（在冲突时尤其有用）,
管理器可以通过修改请求的参数 `fieldManager` 指定。
虽然 kubectl 默认发往 `kubectl` 服务端点，但它则请求到应用的服务端点（apply endpoint）。
对于其他的更新，它默认的是从用户代理计算得来。

<!-- 
## Apply and Update

The two operation types considered by this feature are `Apply` (`PATCH` with
content type `application/apply-patch+yaml`) and `Update` (all other operations
which modify the object). Both operations update the `managedFields`, but behave
a little differently.

Whether you are submitting JSON data or YAML data, use
`application/apply-patch+yaml` as the `Content-Type` header value.

All JSON documents are valid YAML.
-->
## 应用和更新 {#apply-and-update}

此特性涉及两类操作，分别是 `Apply`
（内容类型为 `application/apply-patch+yaml` 的 `PATCH` 请求）
和 `Update` （所有修改对象的其他操作）。
这两类操作都会更新字段 `managedFields`，但行为表现有一点不同。

{{< note >}}
不管你提交的是 JSON 数据还是 YAML 数据，
都要使用 `application/apply-patch+yaml` 作为 `Content-Type` 的值。

所有的 JSON 文档 都是合法的 YAML。
{{< /note >}}

<!-- 
For instance, only the apply operation fails on conflicts while update does
not. Also, apply operations are required to identify themselves by providing a
`fieldManager` query parameter, while the query parameter is optional for update
operations. Finally, when using the apply operation you cannot have
`managedFields` in the object that is being applied.

An example object with multiple managers could look like this:
-->
例如，在冲突发生的时候，只有 `apply` 操作失败，而 `update` 则不会。
此外，`apply` 操作必须通过提供一个 `fieldManager` 查询参数来标识自身，
而此查询参数对于 `update` 操作则是可选的。
最后，当使用 `apply` 命令时，你不能在应用中的对象中持有 `managedFields`。

一个包含多个管理器的对象，示例如下：

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

<!-- 
In this example, a second operation was run as an `Update` by the manager called
`kube-controller-manager`. The update changed a value in the data field which
caused the field's management to change to the `kube-controller-manager`.

If this update would have been an `Apply` operation, the operation
would have failed due to conflicting ownership.
-->
在这个例子中，
第二个操作被管理器 `kube-controller-manager` 以 `Update` 的方式运行。
此 `update` 更改 data 字段的值，
并使得字段管理器被改为 `kube-controller-manager`。

如果把 `update` 操作改为 `Apply`，那就会因为所有权冲突的原因，导致操作失败。

<!-- 
## Merge strategy

The merging strategy, implemented with Server Side Apply, provides a generally
more stable object lifecycle. Server Side Apply tries to merge fields based on
the actor who manages them instead of overruling based on values. This way
multiple actors can update the same object without causing unexpected interference.
-->
## 合并策略 {#merge-strategy}

由服务器端应用实现的合并策略，提供了一个总体更稳定的对象生命周期。
服务器端应用试图依据负责管理它们的主体来合并字段，而不是根据值来否决。
这么做是为了多个主体可以更新同一个对象，且不会引起意外的相互干扰。

<!-- 
When a user sends a "fully-specified intent" object to the Server Side Apply
endpoint, the server merges it with the live object favoring the value in the
applied config if it is specified in both places. If the set of items present in
the applied config is not a superset of the items applied by the same user last
time, each missing item not managed by any other appliers is removed. For
more information about how an object's schema is used to make decisions when
merging, see
[sigs.k8s.io/structured-merge-diff](https://sigs.k8s.io/structured-merge-diff).
-->
当用户发送一个“完整描述的目标”对象到服务器端应用的服务端点，
服务器会将它和活动对象做一次合并，如果两者中有重复定义的值，那就以配置文件的为准。
如果配置文件中的项目集合不是此用户上一次操作项目的超集，
所有缺少的、没有其他应用者管理的项目会被删除。
关于合并时用来做决策的对象规格的更多信息，参见
[sigs.k8s.io/structured-merge-diff](https://sigs.k8s.io/structured-merge-diff).

<!-- 
A number of markers were added in Kubernetes 1.16 and 1.17, to allow API
developers to describe the merge strategy supported by lists, maps, and
structs. These markers can be applied to objects of the respective type,
in Go files or in the OpenAPI schema definition of the
[CRD](/docs/reference/generated/kubernetes-api/{{< param "version" >}}#jsonschemaprops-v1-apiextensions-k8s-io):
-->
Kubernetes 1.16 和 1.17 中添加了一些标记，
允许 API 开发人员描述由 list、map、和 structs 支持的合并策略。
这些标记可应用到相应类型的对象，在 Go 文件或在
[CRD](/docs/reference/generated/kubernetes-api/{{< param "version" >}}#jsonschemaprops-v1-apiextensions-k8s-io)
的 OpenAPI 的模式中定义：

<!-- 
| Golang marker | OpenAPI extension | Accepted values | Description | Introduced in |
|---|---|---|---|---|
| `//+listType` | `x-kubernetes-list-type` | `atomic`/`set`/`map` | Applicable to lists. `set` applies to lists that include only scalar elements. These elements must be unique. `map` applies to lists of nested types only. The key values (see `listMapKey`) must be unique in the list. `atomic` can apply to any list. If configured as `atomic`, the entire list is replaced during merge. At any point in time, a single manager owns the list. If `set` or `map`, different managers can manage entries separately. | 1.16          |
| `//+listMapKey` | `x-kubernetes-list-map-keys` | List of field names, e.g. `["port", "protocol"]` | Only applicable when `+listType=map`. A list of field names whose values uniquely identify entries in the list. While there can be multiple keys, `listMapKey` is singular because keys need to be specified individually in the Go type. The key fields must be scalars. | 1.16 |
| `//+mapType` | `x-kubernetes-map-type` | `atomic`/`granular` | Applicable to maps. `atomic` means that the map can only be entirely replaced by a single manager. `granular` means that the map supports separate managers updating individual fields. | 1.17 |
| `//+structType` | `x-kubernetes-map-type` | `atomic`/`granular` | Applicable to structs; otherwise same usage and OpenAPI annotation as `//+mapType`.| 1.17 |
-->
| Golang 标记 | OpenAPI extension | 可接受的值 | 描述 | 引入版本 |
|---|---|---|---|---|
| `//+listType` | `x-kubernetes-list-type` | `atomic`/`set`/`map` | 适用于 list。`set` 适用于仅包含标量元素的列表。这些元素必须是不重复的。`map` 仅适用于包含嵌套类型的列表。列表中的键（参见 `listMapKey`）不可以重复。`atomic` 适用于任何类型的列表。如果配置为 `atomic`，则合并时整个列表会被替换掉。任何时候，只有一个管理器负责管理指定列表。如果配置为 `set` 或 `map`，不同的管理器也可以分开管理条目。 | 1.16          |
| `//+listMapKey` | `x-kubernetes-list-map-keys` | 字段名称的列表，例如，`["port", "protocol"]` | 仅当 `+listType=map` 时适用。取值为字段名称的列表，这些字段值的组合能够唯一标识列表中的条目。尽管可以存在多个键，`listMapKey` 是单数的，这是因为键名需要在 Go 类型中各自独立指定。键字段必须是标量。 | 1.16 |
| `//+mapType` | `x-kubernetes-map-type` | `atomic`/`granular` | 适用于 map。 `atomic` 指 map 只能被单个的管理器整个的替换。 `granular` 指 map 支持多个管理器各自更新自己的字段。 | 1.17 |
| `//+structType` | `x-kubernetes-map-type` | `atomic`/`granular` | 适用于 structs；否则就像 `//+mapType` 有相同的用法和 openapi 注释.| 1.17 |

<!--
If `listType` is missing, the API server interprets a
`patchMergeStrategy=merge` marker as a `listType=map` and the
corresponding `patchMergeKey` marker as a `listMapKey`.

The `atomic` list type is recursive.

These markers are specified as comments and don't have to be repeated as
field tags.
-->
若未指定 `listType`，API 服务器将 `patchMergeStrategy=merge` 标记解释为
`listType=map` 并且视对应的 `patchMergeKey` 标记为 `listMapKey` 取值。

`atomic` 列表类型是递归的。

这些标记都是用源代码注释的方式给出的，不必作为字段标签（tag）再重复。

<!--
### Compatibility across topology changes
-->
### 拓扑变化时的兼容性  {#compatibility-across-toplogy-changes}

<!--
On rare occurences, a CRD or built-in type author may want to change the
specific topology of a field in their resource without incrementing its
version. Changing the topology of types, by upgrading the cluster or
updating the CRD, has different consequences when updating existing
objects. There are two categories of changes: when a field goes from
`map`/`set`/`granular` to `atomic` and the other way around.
-->
在极少的情况下，CRD 或者内置类型的作者可能希望更改其资源中的某个字段的
拓扑配置，同时又不提升版本号。
通过升级集群或者更新 CRD 来更改类型的拓扑信息与更新现有对象的结果不同。
变更的类型有两种：一种是将字段从 `map`/`set`/`granular` 更改为 `atomic`，
另一种是做逆向改变。

<!--
When the `listType`, `mapType`, or `structType` changes from
`map`/`set`/`granular` to `atomic`, the whole list, map or struct of
existing objects will end-up being owned by actors who owned an element
of these types. This means that any further change to these objects
would cause a conflict.
-->
当 `listType`、`mapType` 或 `structType` 从 `map`/`set`/`granular` 改为
`atomic` 时，现有对象的整个列表、映射或结构的属主都会变为这些类型的
元素之一的属主。这意味着，对这些对象的进一步变更会引发冲突。

<!--
When a list, map, or struct changes from `atomic` to
`map`/`set`/`granular`, the API server won't be able to infer the new
ownership of these fields. Because of that, no conflict will be produced
when objects have these fields updated. For that reason, it is not
recommended to change a type from `atomic` to `map`/`set`/`granular`.

Take for example, the custom resource:
-->
当一个列表、映射或结构从 `atomic` 改为 `map`/`set`/`granular` 之一
时，API 服务器无法推导这些字段的新的属主。因此，当对象的这些字段
再次被更新时不会引发冲突。出于这一原因，不建议将某类型从 `atomic` 改为
`map`/`set`/`granular`。

以下面的自定义资源为例：

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

<!--
Before `spec.data` gets changed from `atomic` to `granular`,
`manager-one` owns the field `spec.data`, and all the fields within it
(`key1` and `key2`). When the CRD gets changed to make `spec.data`
`granular`, `manager-one` continues to own the top-level field
`spec.data` (meaning no other managers can delete the map called `data`
without a conflict), but it no longer owns `key1` and `key2`, so another
manager can then modify or delete those fields without conflict.
-->
在 `spec.data` 从 `atomic` 改为 `granular` 之前，`manager-one` 是
`spec.data` 字段及其所包含字段（`key1` 和 `key2`）的属主。
当对应的 CRD 被更改，使得 `spec.data` 变为 `granular` 拓扑时，
`manager-one` 继续拥有顶层字段 `spec.data`（这意味着其他管理者想
删除名为 `data` 的映射而不引起冲突是不可能的），但不再拥有
`key1` 和 `key2`。因此，其他管理者可以在不引起冲突的情况下更改
或删除这些字段。

<!-- 
### Custom Resources

By default, Server Side Apply treats custom resources as unstructured data. All
keys are treated the same as struct fields, and all lists are considered atomic.

If the Custom Resource Definition defines a
[schema](/docs/reference/generated/kubernetes-api/{{< param "version" >}}#jsonschemaprops-v1-apiextensions-k8s-io)
that contains annotations as defined in the previous "Merge Strategy"
section, these annotations will be used when merging objects of this
type.
-->
### 自定义资源 {#custom-resources}

默认情况下，服务器端应用把自定义资源看做非结构化数据。
所有的键值（keys）就像 struct 的字段一样被处理，
所有的 list 被认为是原子性的。

如果自定义资源定义（Custom Resource Definition，CRD）定义了一个 
[模式](/docs/reference/generated/kubernetes-api/{{< param "version" >}}#jsonschemaprops-v1-apiextensions-k8s-io)，
它包含类似以前“合并策略”章节中定义过的注解，
这些注解将在合并此类型的对象时使用。

<!-- 
## Using Server-Side Apply in a controller

As a developer of a controller, you can use server-side apply as a way to
simplify the update logic of your controller. The main differences with a
read-modify-write and/or patch are the following:

* the applied object must contain all the fields that the controller cares about.
* there are no way to remove fields that haven't been applied by the controller
  before (controller can still send a PATCH/UPDATE for these use-cases).
* the object doesn't have to be read beforehand, `resourceVersion` doesn't have
  to be specified.

It is strongly recommended for controllers to always "force" conflicts, since they
might not be able to resolve or act on these conflicts.
-->
## 在控制器中使用服务器端应用 {#using-server-side-apply-in-controller}

控制器的开发人员可以把服务器端应用作为简化控制器的更新逻辑的方式。
读-改-写 和/或 patch 的主要区别如下所示：

* 应用的对象必须包含控制器关注的所有字段。
* 对于在控制器没有执行过应用操作之前就已经存在的字段，不能删除。
  （控制器在这种用例环境下，依然可以发送一个 PATCH/UPDATE）
* 对象不必事先读取，`resourceVersion` 不必指定。

强烈推荐：设置控制器在冲突时强制执行，这是因为冲突发生时，它们没有其他解决方案或措施。

<!-- 
## Transferring Ownership

In addition to the concurrency controls provided by [conflict resolution](#conflicts),
Server Side Apply provides ways to perform coordinated
field ownership transfers from users to controllers.

This is best explained by example. Let's look at how to safely transfer
ownership of the `replicas` field from a user to a controller while enabling
automatic horizontal scaling for a Deployment, using the HorizontalPodAutoscaler
resource and its accompanying controller.

Say a user has defined deployment with `replicas` set to the desired value:
-->
## 转移所有权 {#transferring-ownership}

除了通过[冲突解决方案](#conflicts)提供的并发控制，
服务器端应用提供了一些协作方式来将字段所有权从用户转移到控制器。

最好通过例子来说明这一点。
让我们来看看，在使用 Horizo​​ntalPodAutoscaler 资源和与之配套的控制器，
且开启了 Deployment 的自动水平扩展功能之后，
怎么安全的将 `replicas` 字段的所有权从用户转移到控制器。

假设用户定义了 Deployment，且 `replicas` 字段已经设置为期望的值：

{{< codenew file="application/ssa/nginx-deployment.yaml" >}}

<!-- 
And the user has created the deployment using server side apply like so:
-->
并且，用户使用服务器端应用，像这样创建 Deployment：

```shell
kubectl apply -f https://k8s.io/examples/application/ssa/nginx-deployment.yaml --server-side
```

<!-- 
Then later, HPA is enabled for the deployment, e.g.:
-->
然后，为 Deployment 启用 HPA，例如：

```shell
kubectl autoscale deployment nginx-deployment --cpu-percent=50 --min=1 --max=10
```

<!-- 
Now, the user would like to remove `replicas` from their configuration, so they
don't accidentally fight with the HPA controller. However, there is a race: it
might take some time before HPA feels the need to adjust `replicas`, and if
the user removes `replicas` before the HPA writes to the field and becomes
its owner, then apiserver will set `replicas` to 1, its default value. This
is not what the user wants to happen, even temporarily.
-->
现在，用户希望从他们的配置中删除 `replicas`，所以他们总是和 HPA 控制器冲突。
然而，这里存在一个竟态：
在 HPA 需要调整 `replicas` 之前会有一个时间窗口，
如果在 HPA 写入字段成为所有者之前，用户删除了`replicas`，
那 API 服务器就会把 `replicas` 的值设为1， 也就是默认值。
这不是用户希望发生的事情，即使是暂时的。

<!-- 
There are two solutions:

- (basic) Leave `replicas` in the configuration; when HPA eventually writes to that
  field, the system gives the user a conflict over it. At that point, it is safe
  to remove from the configuration.

- (more advanced) If, however, the user doesn't want to wait, for example
  because they want to keep the cluster legible to coworkers, then they can take
  the following steps to make it safe to remove `replicas` from their
  configuration:

First, the user defines a new configuration containing only the `replicas` field:
-->
这里有两个解决方案：

- （基本操作）把 `replicas` 留在配置文件中；当 HPA 最终写入那个字段，
  系统基于此事件告诉用户：冲突发生了。在这个时间点，可以安全的删除配置文件。
- （高级操作）然而，如果用户不想等待，比如他们想为合作伙伴保持集群清晰，
  那他们就可以执行以下步骤，安全的从配置文件中删除 `replicas`。

首先，用户新定义一个只包含 `replicas` 字段的配置文件：

{{< codenew file="application/ssa/nginx-deployment-replicas-only.yaml" >}}

<!-- 
The user applies that configuration using the field manager name `handover-to-hpa`:
-->
用户使用名为 `handover-to-hpa` 的字段管理器，应用此配置文件。

```shell
kubectl apply -f https://k8s.io/examples/application/ssa/nginx-deployment-replicas-only.yaml \
  --server-side --field-manager=handover-to-hpa \
  --validate=false
```

<!-- 
If the apply results in a conflict with the HPA controller, then do nothing. The
conflict indicates the controller has claimed the field earlier in the
process than it sometimes does.

At this point the user may remove the `replicas` field from their configuration.
-->
如果应用操作和 HPA 控制器产生冲突，那什么都不做。
冲突表明控制器在更早的流程中已经对字段声明过所有权。

在此时间点，用户可以从配置文件中删除 `replicas` 。

{{< codenew file="application/ssa/nginx-deployment-no-replicas.yaml" >}}

<!-- 
Note that whenever the HPA controller sets the `replicas` field to a new value,
the temporary field manager will no longer own any fields and will be
automatically deleted. No clean up is required.
-->
注意，只要 HPA 控制器为 `replicas` 设置了一个新值，
该临时字段管理器将不再拥有任何字段，会被自动删除。
这里不需要执行清理工作。

<!-- 
### Transferring Ownership Between Users

Users can transfer ownership of a field between each other by setting the field
to the same value in both of their applied configs, causing them to share
ownership of the field. Once the users share ownership of the field, one of them
can remove the field from their applied configuration to give up ownership and
complete the transfer to the other user.
-->
### 在用户之间转移所有权 {#transferring-ownership-between-users}

通过在配置文件中把一个字段设置为相同的值，用户可以在他们之间转移字段的所有权，
从而共享了字段的所有权。
当用户共享了字段的所有权，任何一个用户可以从他的配置文件中删除该字段，
并应用该变更，从而放弃所有权，并实现了所有权向其他用户的转移。

<!-- 
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
-->
## 与客户端应用的对比 {#comparison-with-client-side-apply}

由服务器端应用实现的冲突检测和解决方案的一个结果就是，
应用者总是可以在本地状态中得到最新的字段值。
如果得不到最新值，下次执行应用操作时就会发生冲突。
解决冲突三个选项的任意一个都会保证：此应用过的配置文件是服务器上对象字段的最新子集。

这和客户端应用（Client Side Apply） 不同，如果有其他用户覆盖了此值，
过期的值被留在了应用者本地的配置文件中。
除非用户更新了特定字段，此字段才会准确，
应用者没有途径去了解下一次应用操作是否会覆盖其他用户的修改。

另一个区别是使用客户端应用的应用者不能改变他们正在使用的 API 版本，但服务器端应用支持这个场景。

<!-- 
## Upgrading from client-side apply to server-side apply

Client-side apply users who manage a resource with `kubectl apply` can start
using server-side apply with the following flag.
-->
## 从客户端应用升级到服务器端应用 {#upgrading-from-client-side-apply-to-server-side-apply}

客户端应用方式时，用户使用 `kubectl apply` 管理资源，
可以通过使用下面标记切换为使用服务器端应用。

```shell
kubectl apply --server-side [--dry-run=server]
```
<!-- 
By default, field management of the object transfers from client-side apply to
kubectl server-side apply without encountering conflicts.

Keep the `last-applied-configuration` annotation up to date.
The annotation infers client-side apply's managed fields.
Any fields not managed by client-side apply raise conflicts.

For example, if you used `kubectl scale` to update the replicas field after
client-side apply, then this field is not owned by client-side apply and
creates conflicts on `kubectl apply --server-side`.

This behavior applies to server-side apply with the `kubectl` field manager.
As an exception, you can opt-out of this behavior by specifying a different,
non-default field manager, as seen in the following example. The default field
manager for kubectl server-side apply is `kubectl`.
-->
默认情况下，对象的字段管理从客户端应用方式迁移到 kubectl 触发的服务器端应用时，不会发生冲突。

{{< caution >}}
保持注解 `last-applied-configuration` 是最新的。
从注解能推断出字段是由客户端应用管理的。
任何没有被客户端应用管理的字段将引发冲突。

举例说明，比如你在客户端应用之后，
使用 `kubectl scale` 去更新 `replicas` 字段，
可是该字段并没有被客户端应用所拥有，
在执行 `kubectl apply --server-side` 时就会产生冲突。
{{< /caution >}}

此操作以 `kubectl` 作为字段管理器来应用到服务器端应用。
作为例外，可以指定一个不同的、非默认字段管理器停止的这种行为，如下面的例子所示。
对于 kubectl 触发的服务器端应用，默认的字段管理器是 `kubectl`。

```shell
kubectl apply --server-side --field-manager=my-manager [--dry-run=server]
```

<!-- 
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
-->
## 从服务器端应用降级到客户端应用 {#downgrading-from-server-side-apply-to-client-side-apply}

如果你用 `kubectl apply --server-side` 管理一个资源，
可以直接用 `kubectl apply` 命令将其降级为客户端应用。

降级之所以可行，这是因为 `kubectl server-side apply`
会保存最新的 `last-applied-configuration` 注解。

此操作以 `kubectl` 作为字段管理器应用到服务器端应用。
作为例外，可以指定一个不同的、非默认字段管理器停止这种行为，如下面的例子所示。
对于 kubectl 触发的服务器端应用，默认的字段管理器是 `kubectl`。

```shell
kubectl apply --server-side --field-manager=my-manager [--dry-run=server]
```

<!-- 
## API Endpoint

With the Server Side Apply feature enabled, the `PATCH` endpoint accepts the
additional `application/apply-patch+yaml` content type. Users of Server Side
Apply can send partially specified objects as YAML to this endpoint.  When
applying a configuration, one should always include all the fields that they
have an opinion about.
-->
## API 端点 {#api-endpoint}

启用了服务器端应用特性之后，
`PATCH` 服务端点接受额外的内容类型 `application/apply-patch+yaml`。
服务器端应用的用户就可以把 YAMl 格式的
部分定义对象（partially specified objects）发送到此端点。
当一个配置文件被应用时，它应该包含所有体现你意图的字段。

<!-- 
## Clearing ManagedFields

It is possible to strip all managedFields from an object by overwriting them
using `MergePatch`, `StrategicMergePatch`, `JSONPatch` or `Update`, so every
non-apply operation. This can be done by overwriting the managedFields field
with an empty entry. Two examples are:
-->
## 清除 ManagedFields {#clearing-managedfields}

可以从对象中剥离所有 managedField，
实现方法是通过使用 `MergePatch`、 `StrategicMergePatch`、 
`JSONPatch`、 `Update`、以及所有的非应用方式的操作来覆盖它。
这可以通过用空条目覆盖 managedFields 字段的方式实现。

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

<!-- 
This will overwrite the managedFields with a list containing a single empty
entry that then results in the managedFields being stripped entirely from the
object. Note that setting the managedFields to an empty list will not
reset the field. This is on purpose, so managedFields never get stripped by
clients not aware of the field.

In cases where the reset operation is combined with changes to other fields
than the managedFields, this will result in the managedFields being reset
first and the other changes being processed afterwards. As a result the
applier takes ownership of any fields updated in the same request.
-->
这一操作将用只包含一个空条目的列表覆写 managedFields，
来实现从对象中整个的去除 managedFields。
注意，只把 managedFields 设置为空列表并不会重置字段。
这么做是有目的的，所以 managedFields 将永远不会被与该字段无关的客户删除。

在重置操作结合 managedFields 以外其他字段更改的场景中，
将导致 managedFields 首先被重置，其他改变被押后处理。
其结果是，应用者取得了同一个请求中所有字段的所有权。

<!-- 
Server Side Apply does not correctly track ownership on
sub-resources that don't receive the resource object type. If you are
using Server Side Apply with such a sub-resource, the changed fields
won't be tracked.
-->
{{< caution >}}
对于不接受资源对象类型的子资源（sub-resources），
服务器端应用不能正确地跟踪其所有权。
如果你对这样的子资源使用服务器端应用，变更的字段将不会被跟踪。
{{< /caution >}}

<!-- 
## Disabling the feature

Server Side Apply is a beta feature, so it is enabled by default. To turn this
[feature gate](/docs/reference/command-line-tools-reference/feature-gates) off,
you need to include the `--feature-gates ServerSideApply=false` flag when
starting `kube-apiserver`. If you have multiple `kube-apiserver` replicas, all
should have the same flag setting.
-->
## 禁用此功能 {#disabling-the-feature}

服务器端应用是一个 Beta 版特性，默认启用。
要关闭此[特性门控](/zh/docs/reference/command-line-tools-reference/feature-gates)，
你需要在启动 `kube-apiserver` 时包含参数 `--feature-gates ServerSideApply=false`。
如果你有多个 `kube-apiserver` 副本，它们的标志设置应该都相同。

