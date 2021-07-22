---
title: 使用 RBAC 鉴权
content_type: concept
weight: 70
---

<!--
reviewers:
- erictune
- deads2k
- liggitt
title: Using RBAC Authorization
content_type: concept
weight: 70
-->

<!-- overview -->
<!--
Role-based access control (RBAC) is a method of regulating access to computer or
network resources based on the roles of individual users within your organization.
-->
基于角色（Role）的访问控制（RBAC）是一种基于组织中用户的角色来调节控制对
计算机或网络资源的访问的方法。

<!-- body -->
<!--
RBAC authorization uses the `rbac.authorization.k8s.io`
{{< glossary_tooltip text="API Group" term_id="api-group" >}} to drive authorization
decisions, allowing you to dynamically configure policies through the Kubernetes API.
-->
RBAC 鉴权机制使用 `rbac.authorization.k8s.io`
{{< glossary_tooltip text="API 组" term_id="api-group" >}}
来驱动鉴权决定，允许你通过 Kubernetes API 动态配置策略。

<!--
To enable RBAC, start the {{< glossary_tooltip text="API server" term_id="kube-apiserver" >}}
with the `-authorization-mode` flag set to a comma-separated list that includes `RBAC`;
for example:
-->
要启用 RBAC，在启动 {{< glossary_tooltip text="API 服务器" term_id="kube-apiserver" >}}
时将 `--authorization-mode` 参数设置为一个逗号分隔的列表并确保其中包含 `RBAC`。

```shell
kube-apiserver --authorization-mode=Example,RBAC --<其他选项> --<其他选项>
```

<!--
## API objects {#api-overview}

The RBAC API declares four kinds of Kubernetes object: _Role_, _ClusterRole_,
_RoleBinding_ and _ClusterRoleBinding_. You can
[describe objects](/docs/concepts/overview/working-with-objects/kubernetes-objects/#understanding-kubernetes-objects),
or amend them, using tools such as `kubectl,` just like any other Kubernetes object.

-->
## API 对象  {#api-overview}

RBAC API 声明了四种 Kubernetes 对象：_Role_、_ClusterRole_、_RoleBinding_ 和
_ClusterRoleBinding_。你可以像使用其他 Kubernetes 对象一样，
通过类似 `kubectl` 这类工具
[描述对象](/zh/docs/concepts/overview/working-with-objects/kubernetes-objects/#understanding-kubernetes-objects),
或修补对象。

{{< caution >}}
<!--
These objects, by design, impose access restrictions. If you are making changes
to a cluster as you learn, see
[privilege escalation prevention and bootstrapping](#privilege-escalation-prevention-and-bootstrapping)
to understand how those restrictions can prevent you making some changes.
-->
这些对象在设计时即实施了一些访问限制。如果你在学习过程中对集群做了更改，请参考
[避免特权提升和引导](#privilege-escalation-prevention-and-bootstrapping)
一节，以了解这些限制会以怎样的方式阻止你做出修改。
{{< /caution >}}

<!--
### Role and ClusterRole

An RBAC _Role_ or _ClusterRole_ contains rules that represent a set of permissions.
Permissions are purely additive (there are no "deny" rules).

A Role always sets permissions within a particular {{< glossary_tooltip text="namespace" term_id="namespace" >}};
when you create a Role, you have to specify the namespace it belongs in.

ClusterRole, by contrast, is a non-namespaced resource. The resources have different names (Role
and ClusterRole) because a Kubernetes object always has to be either namespaced or not namespaced;
it can't be both.
-->
### Role 和 ClusterRole   {#role-and-clusterole}

RBAC 的 _Role_ 或 _ClusterRole_ 中包含一组代表相关权限的规则。
这些权限是纯粹累加的（不存在拒绝某操作的规则）。

Role 总是用来在某个{{< glossary_tooltip text="名字空间" term_id="namespace" >}}
内设置访问权限；在你创建 Role 时，你必须指定该 Role 所属的名字空间。

与之相对，ClusterRole 则是一个集群作用域的资源。这两种资源的名字不同（Role 和
ClusterRole）是因为 Kubernetes 对象要么是名字空间作用域的，要么是集群作用域的，
不可两者兼具。

<!--
ClusterRoles have several uses. You can use a ClusterRole to:

1. define permissions on namespaced resources and be granted within individual namespace(s)
1. define permissions on namespaced resources and be granted across all namespaces
1. define permissions on cluster-scoped resources

If you want to define a role within a namespace, use a Role; if you want to define
a role cluster-wide, use a ClusterRole.
-->
ClusterRole 有若干用法。你可以用它来：

1. 定义对某名字空间域对象的访问权限，并将在各个名字空间内完成授权；
1. 为名字空间作用域的对象设置访问权限，并跨所有名字空间执行授权；
1. 为集群作用域的资源定义访问权限。

如果你希望在名字空间内定义角色，应该使用 Role；
如果你希望定义集群范围的角色，应该使用 ClusterRole。

<!--
#### Role example

Here's an example Role in the "default" namespace that can be used to grant read access to
{{< glossary_tooltip text="pods" term_id="pod" >}}:
-->
#### Role 示例

下面是一个位于 "default" 名字空间的 Role 的示例，可用来授予对
{{< glossary_tooltip text="pods" term_id="pod" >}} 的读访问权限：

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: default
  name: pod-reader
rules:
- apiGroups: [""] # "" 标明 core API 组
  resources: ["pods"]
  verbs: ["get", "watch", "list"]
```

<!--
#### ClusterRole example

A ClusterRole can be used to grant the same permissions as a Role.
Because they are cluster-scoped, you can also use them to grant access to:

* cluster-scoped resources (like {{< glossary_tooltip text="nodes" term_id="node" >}})
* non-resource endpoints (like `/healthz`)
* namespaced resources (like Pods), across all namespaces
  For example: you can use a ClusterRole to allow a particular user to run
  `kubectl get pods -all-namespaces`
-->
###  ClusterRole 示例

ClusterRole 可以和 Role 相同完成授权。
因为 ClusterRole 属于集群范围，所以它也可以为以下资源授予访问权限：

* 集群范围资源（比如 {{< glossary_tooltip text="节点（Node）" term_id="node" >}}）
* 非资源端点（比如 `/healthz`）
* 跨名字空间访问的名字空间作用域的资源（如 Pods），比如，你可以使用
  ClusterRole 来允许某特定用户执行 `kubectl get pods --all-namespaces`

<!--
Here is an example of a ClusterRole that can be used to grant read access to
{{< glossary_tooltip text="secrets" term_id="secret" >}} in any particular namespace,
or across all namespaces (depending on how it is [bound](#rolebinding-and-clusterrolebinding)):
-->
下面是一个 ClusterRole 的示例，可用来为任一特定名字空间中的
{{< glossary_tooltip text="Secret" term_id="secret" >}} 授予读访问权限，
或者跨名字空间的访问权限（取决于该角色是如何[绑定](#rolebinding-and-clusterrolebinding)的）：

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  # "namespace" 被忽略，因为 ClusterRoles 不受名字空间限制
  name: secret-reader
rules:
- apiGroups: [""]
  # 在 HTTP 层面，用来访问 Secret 对象的资源的名称为 "secrets"
  resources: ["secrets"]
  verbs: ["get", "watch", "list"]
```

<!--
The name of a Role or a ClusterRole object must be a valid
[path segment name](/docs/concepts/overview/working-with-objects/names#path-segment-names).
-->
Role 或 ClusterRole 对象的名称必须是合法的
[路径区段名称](/zh/docs/concepts/overview/working-with-objects/names#path-segment-names)。

<!--
### RoleBinding and ClusterRoleBinding

A role binding grants the permissions defined in a role to a user or set of users.
It holds a list of *subjects* (users, groups, or service accounts), and a reference to the
role being granted.
A RoleBinding grants permissions within a specific namespace whereas a ClusterRoleBinding
grants that access cluster-wide.

A RoleBinding may reference any Role in the same namespace. Alternatively, a RoleBinding
can reference a ClusterRole and bind that ClusterRole to the namespace of the RoleBinding.
If you want to bind a ClusterRole to all the namespaces in your cluster, you use a
ClusterRoleBinding.

The name of a RoleBinding or ClusterRoleBinding object must be a valid
[path segment name](/docs/concepts/overview/working-with-objects/names#path-segment-names).
-->
### RoleBinding 和 ClusterRoleBinding   {#rolebinding-and-clusterrolebinding}

角色绑定（Role Binding）是将角色中定义的权限赋予一个或者一组用户。
它包含若干 **主体**（用户、组或服务账户）的列表和对这些主体所获得的角色的引用。
RoleBinding 在指定的名字空间中执行授权，而 ClusterRoleBinding 在集群范围执行授权。

一个 RoleBinding 可以引用同一的名字空间中的任何 Role。
或者，一个 RoleBinding 可以引用某 ClusterRole 并将该 ClusterRole 绑定到
RoleBinding 所在的名字空间。
如果你希望将某  ClusterRole 绑定到集群中所有名字空间，你要使用 ClusterRoleBinding。

RoleBinding 或 ClusterRoleBinding 对象的名称必须是合法的
[路径区段名称](/zh/docs/concepts/overview/working-with-objects/names#path-segment-names)。

<!--
#### RoleBinding examples {#rolebinding-example}

Here is an example of a RoleBinding that grants the "pod-reader" Role to the user "jane"
within the "default" namespace.
This allows "jane" to read pods in the "default" namespace.
-->
#### RoleBinding 示例   {#rolebinding-example}

下面的例子中的 RoleBinding 将 "pod-reader" Role 授予在 "default" 名字空间中的用户 "jane"。
这样，用户 "jane" 就具有了读取 "default" 名字空间中 pods 的权限。

```yaml
apiVersion: rbac.authorization.k8s.io/v1
# 此角色绑定允许 "jane" 读取 "default" 名字空间中的 Pods
kind: RoleBinding
metadata:
  name: read-pods
  namespace: default
subjects:
# 你可以指定不止一个“subject（主体）”
- kind: User
  name: jane # "name" 是不区分大小写的
  apiGroup: rbac.authorization.k8s.io
roleRef:
  # "roleRef" 指定与某 Role 或 ClusterRole 的绑定关系
  kind: Role # 此字段必须是 Role 或 ClusterRole
  name: pod-reader     # 此字段必须与你要绑定的 Role 或 ClusterRole 的名称匹配
  apiGroup: rbac.authorization.k8s.io
```

<!--
A RoleBinding can also reference a ClusterRole to grant the permissions defined in that
ClusterRole to resources inside the RoleBinding's namespace. This kind of reference
lets you define a set of common roles across your cluster, then reuse them within
multiple namespaces.

For instance, even though the following RoleBinding refers to a ClusterRole,
"dave" (the subject, case sensitive) will only be able to read Secrets in the "development"
namespace, because the RoleBinding's namespace (in its metadata) is "development".
-->
RoleBinding 也可以引用 ClusterRole，以将对应 ClusterRole 中定义的访问权限授予
RoleBinding 所在名字空间的资源。这种引用使得你可以跨整个集群定义一组通用的角色，
之后在多个名字空间中复用。

例如，尽管下面的 RoleBinding 引用的是一个 ClusterRole，"dave"（这里的主体，
不区分大小写）只能访问 "development" 名字空间中的 Secrets 对象，因为 RoleBinding
所在的名字空间（由其 metadata 决定）是 "development"。

```yaml
apiVersion: rbac.authorization.k8s.io/v1
# 此角色绑定使得用户 "dave" 能够读取 "development" 名字空间中的 Secrets
# 你需要一个名为 "secret-reader" 的 ClusterRole
kind: RoleBinding
metadata:
  name: read-secrets
  # RoleBinding 的名字空间决定了访问权限的授予范围。
  # 这里隐含授权仅在 "development" 名字空间内的访问权限。
  namespace: development
subjects:
- kind: User
  name: dave # 'name' 是不区分大小写的
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: secret-reader
  apiGroup: rbac.authorization.k8s.io
```

<!--
#### ClusterRoleBinding example

To grant permissions across a whole cluster, you can use a ClusterRoleBinding.
The following ClusterRoleBinding allows any user in the group "manager" to read
secrets in any namespace.
-->
#### ClusterRoleBinding 示例   {#clusterrolebinding-example}

要跨整个集群完成访问权限的授予，你可以使用一个 ClusterRoleBinding。
下面的 ClusterRoleBinding 允许 "manager" 组内的所有用户访问任何名字空间中的
Secrets。

```yaml
apiVersion: rbac.authorization.k8s.io/v1
# 此集群角色绑定允许 “manager” 组中的任何人访问任何名字空间中的 secrets
kind: ClusterRoleBinding
metadata:
  name: read-secrets-global
subjects:
- kind: Group
  name: manager # 'name' 是不区分大小写的
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: secret-reader
  apiGroup: rbac.authorization.k8s.io
```

<!--
After you create a binding, you cannot change the Role or ClusterRole that it refers to.
If you try to change a binding's `roleRef`, you get a validation error. If you do want
to change the `roleRef` for a binding, you need to remove the binding object and create
a replacement.

There are two reasons for this restriction:
-->
创建了绑定之后，你不能再修改绑定对象所引用的 Role 或 ClusterRole。
试图改变绑定对象的 `roleRef` 将导致合法性检查错误。
如果你想要改变现有绑定对象中 `roleRef` 字段的内容，必须删除重新创建绑定对象。

这种限制有两个主要原因：

<!--
1. A binding to a different role is a fundamentally different binding.
Requiring a binding to be deleted/recreated in order to change the `roleRef`
ensures the full list of subjects in the binding is intended to be granted
the new role (as opposed to enabling or accidentally modifying only the roleRef
without verifying all of the existing subjects should be given the new role's permissions).
2. Making `roleRef` immutable allows giving `update` permission on an existing binding object
to a user, which lets them manage the list of subjects, without being able to change the
role that is granted to those subjects.
-->
1. 针对不同角色的绑定是完全不一样的绑定。要求通过删除/重建绑定来更改 `roleRef`,
   这样可以确保要赋予绑定的所有主体会被授予新的角色（而不是在允许或者不小心修改
   了 `roleRef` 的情况下导致所有现有主体未经验证即被授予新角色对应的权限）。
1. 将 `roleRef` 设置为不可以改变，这使得可以为用户授予对现有绑定对象的 `update` 权限，
   这样可以让他们管理主体列表，同时不能更改被授予这些主体的角色。

<!--
The `kubectl auth reconcile` command-line utility creates or updates a manifest file containing RBAC objects,
and handles deleting and recreating binding objects if required to change the role they refer to.
See [command usage and examples](#kubectl-auth-reconcile) for more information.
-->
命令 `kubectl auth reconcile` 可以创建或者更新包含 RBAC 对象的清单文件，
并且在必要的情况下删除和重新创建绑定对象，以改变所引用的角色。
更多相关信息请参照[命令用法和示例](#kubectl-auth-reconcile)

<!--
### Referring to Resources

In the Kubernetes API, most resources are represented and accessed using a string representation of
their object name, such as `pods` for a Pod. RBAC refers to resources using exactly the same
name that appears in the URL for the relevant API endpoint.
Some Kubernetes APIs involve a
_subresource_, such as the logs for a Pod. A request for a Pod's logs looks like:
-->
### 对资源的引用    {#referring-to-resources}

在 Kubernetes API 中，大多数资源都是使用对象名称的字符串表示来呈现与访问的。
例如，对于 Pod 应使用 "pods"。
RBAC 使用对应 API 端点的 URL 中呈现的名字来引用资源。
有一些 Kubernetes API 涉及 **子资源（subresource）**，例如 Pod 的日志。
对 Pod 日志的请求看起来像这样：

```http
GET /api/v1/namespaces/{namespace}/pods/{name}/log
```

<!--
In this case, `pods` is the namespaced resource for Pod resources, and `log` is a
subresource of `pods`. To represent this in an RBAC role, use a slash (`/`) to
delimit the resource and subresource. To allow a subject to read `pods` and
also access the `log` subresource for each of those Pods, you write:
-->
在这里，`pods` 对应名字空间作用域的 Pod 资源，而 `log` 是 `pods` 的子资源。
在 RBAC 角色表达子资源时，使用斜线（`/`）来分隔资源和子资源。
要允许某主体读取 `pods` 同时访问这些 Pod 的 `log` 子资源，你可以这么写：

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: default
  name: pod-and-pod-logs-reader
rules:
- apiGroups: [""]
  resources: ["pods", "pods/log"]
  verbs: ["get", "list"]
```

<!--
You can also refer to resources by name for certain requests through the `resourceNames` list.
When specified, requests can be restricted to individual instances of a resource.
Here is an example that restricts its subject to only `get` or `update` a
{{< glossary_tooltip term_id="ConfigMap" >}} named `my-configmap`:
-->
对于某些请求，也可以通过 `resourceNames` 列表按名称引用资源。
在指定时，可以将请求限定为资源的单个实例。
下面的例子中限制可以 "get" 和 "update" 一个名为 `my-configmap` 的
{{< glossary_tooltip term_id="ConfigMap" >}}：

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: default
  name: configmap-updater
rules:
- apiGroups: [""]
  # 在 HTTP 层面，用来访问 ConfigMap 的资源的名称为 "configmaps"
  resources: ["configmaps"]
  resourceNames: ["my-configmap"]
  verbs: ["update", "get"]
```

{{< note >}}
<!--
You cannot restrict `create` or `deletecollection` requests by resourceName. For `create`, this
limitation is because the object name is not known at authorization time.
-->
你不能针对 `create` 或者 `deletecollection` 请求来实施 resourceName 限制。
对于 `create` 操作而言，这是因为在鉴权时还不知道对象名称。
{{< /note >}}

<!--
### Aggregated ClusterRoles

You can _aggregate_ several ClusterRoles into one combined ClusterRole.
A controller, running as part of the cluster control plane, watches for ClusterRole
objects with an `aggregationRule` set. The `aggregationRule` defines a label
{{< glossary_tooltip text="selector" term_id="selector" >}} that the controller
uses to match other ClusterRole objects that should be combined into the `rules`
field of this one.

Here is an example aggregated ClusterRole:
-->
### 聚合的 ClusterRole    {#aggregated-clusterroles}

你可以将若干 ClusterRole **聚合（Aggregate）** 起来，形成一个复合的 ClusterRole。
某个控制器作为集群控制面的一部分会监视带有 `aggregationRule` 的 ClusterRole
对象集合。`aggregationRule` 为控制器定义一个标签
{{< glossary_tooltip text="选择算符" term_id="selector" >}}供后者匹配
应该组合到当前 ClusterRole 的 `roles` 字段中的 ClusterRole 对象。

下面是一个聚合 ClusterRole 的示例：

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: monitoring
aggregationRule:
  clusterRoleSelectors:
  - matchLabels:
      rbac.example.com/aggregate-to-monitoring: "true"
rules: [] # 控制面自动填充这里的规则
```

<!--
If you create a new ClusterRole that matches the label selector of an existing aggregated ClusterRole,
that change triggers adding the new rules into the aggregated ClusterRole.
Here is an example that adds rules to the "monitoring" ClusterRole, by creating another
ClusterRole labeled `rbac.example.com/aggregate-to-monitoring: true`.
-->
如果你创建一个与某现有聚合 ClusterRole 的标签选择算符匹配的 ClusterRole，
这一变化会触发新的规则被添加到聚合 ClusterRole 的操作。
下面的例子中，通过创建一个标签同样为 `rbac.example.com/aggregate-to-monitoring: true`
的 ClusterRole，新的规则可被添加到 "monitoring" ClusterRole 中。

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: monitoring-endpoints
  labels:
    rbac.example.com/aggregate-to-monitoring: "true"
# 当你创建 "monitoring-endpoints" ClusterRole 时，
# 下面的规则会被添加到 "monitoring" ClusterRole 中
rules:
- apiGroups: [""]
  resources: ["services", "endpoints", "pods"]
  verbs: ["get", "list", "watch"]
```

<!--
The [default user-facing roles](#default-roles-and-role-bindings) use ClusterRole aggregation. This lets you,
as a cluster administrator, include rules for custom resources, such as those served by
{{< glossary_tooltip term_id="CustomResourceDefinition" text="CustomResourceDefinitions" >}}
or aggregated API servers, to extend the default roles.

For example: the following ClusterRoles let the "admin" and "edit" default roles manage the custom resource
named CronTab, whereas the "view" role can perform only read actions on CronTab resources.
You can assume that CronTab objects are named `"crontabs"` in URLs as seen by the API server.
-->
默认的[面向用户的角色](#default-roles-and-role-bindings) 使用 ClusterRole 聚合。
这使得作为集群管理员的你可以为扩展默认规则，包括为定制资源设置规则，
比如通过 CustomResourceDefinitions 或聚合 API 服务器提供的定制资源。

例如，下面的 ClusterRoles 让默认角色 "admin" 和 "edit" 拥有管理自定义资源 "CronTabs" 的权限，
 "view" 角色对 CronTab 资源拥有读操作权限。
你可以假定 CronTab 对象在 API 服务器所看到的 URL 中被命名为 `"crontabs"`。

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: aggregate-cron-tabs-edit
  labels:
    # 添加以下权限到默认角色 "admin" 和 "edit" 中
    rbac.authorization.k8s.io/aggregate-to-admin: "true"
    rbac.authorization.k8s.io/aggregate-to-edit: "true"
rules:
- apiGroups: ["stable.example.com"]
  resources: ["crontabs"]
  verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
---
kind: ClusterRole
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: aggregate-cron-tabs-view
  labels:
    # 添加以下权限到 "view" 默认角色中
    rbac.authorization.k8s.io/aggregate-to-view: "true"
rules:
- apiGroups: ["stable.example.com"]
  resources: ["crontabs"]
  verbs: ["get", "list", "watch"]
```

<!--
#### Role Examples

The following examples are excerpts from Role or ClusterRole objects, showing only
the `rules` section.

Allow reading `"pods"` resources in the core
{{< glossary_tooltip text="API Group" term_id="api-group" >}}:
-->
#### Role 示例   {#role-examples}

以下示例均为从 Role 或 CLusterRole 对象中截取出来，我们仅展示其 `rules` 部分。

允许读取在核心 {{< glossary_tooltip text="API 组" term_id="api-group" >}}下的
`"Pods"`：

```yaml
rules:
- apiGroups: [""]
  # 在 HTTP 层面，用来访问 Pod 的资源的名称为 "pods"
  resources: ["pods"]
  verbs: ["get", "list", "watch"]
```

<!--
Allow reading/writing Deployments (at the HTTP level: objects with `"deployments"`
in the resource part of their URL) in both the `"extensions"` and `"apps"` API groups:
-->
允许读/写在 "extensions" 和 "apps" API 组中的 Deployment（在 HTTP 层面，对应
URL 中资源部分为 "deployments"）：

```yaml
rules:
- apiGroups: ["extensions", "apps"]
  resources: ["deployments"]
  verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
```

<!--
Allow reading Pods in the core API group, as well as reading or writing Job
resources in the `"batch"` or `"extensions"` API groups:
-->
允许读取核心 API 组中的 "pods" 和读/写 `"batch"` 或 `"extensions"` API 组中的
"jobs"：

```yaml
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list", "watch"]
- apiGroups: ["batch", "extensions"]
  resources: ["jobs"]
  verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
```

<!--
Allow reading a ConfigMap named "my-config" (must be bound with a
RoleBinding to limit to a single ConfigMap in a single namespace):
-->
允许读取名称为 "my-config" 的 ConfigMap（需要通过 RoleBinding 绑定以
限制为某名字空间中特定的 ConfigMap）：

```yaml
rules:
- apiGroups: [""]
  resources: ["configmaps"]
  resourceNames: ["my-config"]
  verbs: ["get"]
```

<!--
Allow reading the resource `"nodes"` in the core group (because a
Node is cluster-scoped, this must be in a ClusterRole bound with a
ClusterRoleBinding to be effective):
-->
允许读取在核心组中的 "nodes" 资源（因为 `Node` 是集群作用域的，所以需要
ClusterRole 绑定到 ClusterRoleBinding 才生效）：

```yaml
rules:
- apiGroups: [""]
  resources: ["nodes"]
  verbs: ["get", "list", "watch"]
```

<!--
Allow GET and POST requests to the non-resource endpoint `/healthz` and
all subpaths (must be in a ClusterRole bound with a ClusterRoleBinding
to be effective):
-->
允许针对非资源端点 `/healthz` 和其子路径上发起 GET 和 POST 请求
（必须在 ClusterRole 绑定 ClusterRoleBinding 才生效）：

```yaml
rules:
  - nonResourceURLs: ["/healthz", "/healthz/*"] # nonResourceURL 中的 '*' 是一个全局通配符
    verbs: ["get", "post"]
```

<!--
### Referring to Subjects

A RoleBinding or ClusterRoleBinding binds a role to subjects.
Subjects can be groups, users or
{{< glossary_tooltip text="ServiceAccounts" term_id="service-account" >}}.

Kubernetes represents usernames as strings.
These can be: plain names, such as "alice"; email-style names, like "bob@example.com";
or numeric user IDs represented as a string.  It is up to you as a cluster administrator
to configure the [authentication modules](/docs/reference/access-authn-authz/authentication/)
so that authentication produces usernames in the format you want.
-->
### 对主体的引用   {#referring-to-subjects}

RoleBinding 或者 ClusterRoleBinding 可绑定角色到某 *主体（Subject）*上。
主体可以是组，用户或者
{{< glossary_tooltip text="服务账户" term_id="service-account" >}}。

Kubernetes 用字符串来表示用户名。
用户名可以是普通的用户名，像 "alice"；或者是邮件风格的名称，如 "bob@example.com"，
或者是以字符串形式表达的数字 ID。
你作为 Kubernetes 管理员负责配置
[身份认证模块](/zh/docs/reference/access-authn-authz/authentication/)
以便后者能够生成你所期望的格式的用户名。


{{< caution >}}
<!--
The prefix `system:` is reserved for Kubernetes system use, so you should ensure
that you don't have users or groups with names that start with `system:` by
accident.
Other than this special prefix, the RBAC authorization system does not require any format
for usernames.
-->
前缀 `system:` 是 Kubernetes 系统保留的，所以你要确保
所配置的用户名或者组名不能出现上述 `system:` 前缀。
除了对前缀的限制之外，RBAC 鉴权系统不对用户名格式作任何要求。
{{< /caution >}}

<!--
In Kubernetes, Authenticator modules provide group information.
Groups, like users, are represented as strings, and that string has no format requirements,
other than that the prefix `system:` is reserved.

[Service Accounts](/docs/tasks/configure-pod-container/configure-service-account/) have usernames with the `system:serviceaccount:` prefix and belong
to groups with the `system:serviceaccounts:` prefix.
-->
在 Kubernetes 中，鉴权模块提供用户组信息。
与用户名一样，用户组名也用字符串来表示，而且对该字符串没有格式要求，
只是不能使用保留的前缀 `system:`。

[服务账户](/zh/docs/tasks/configure-pod-container/configure-service-account/)
的用户名前缀为 `system:serviceaccount:`，属于前缀为 `system:serviceaccounts:`
的用户组。

{{< note >}}
<!--
- `system:serviceaccount:` (singular) is the prefix for service account usernames.
- `system:serviceaccounts:` (plural) is the prefix for service account groups.
-->
- `system:serviceaccount:` （单数）是用于服务账户用户名的前缀；
- `system:serviceaccounts:` （复数）是用于服务账户组名的前缀。
{{< /note >}}

<!--
#### Role Binding Examples

The following examples are `RoleBinding` excerpts that only
show the `subjects` section.

For a user named `alice@example.com`:
-->
#### RoleBinding 示例   {#role-binding-examples}

下面示例是 `RoleBinding` 中的片段，仅展示其 `subjects` 的部分。

对于名称为 `alice@example.com` 的用户：

```yaml
subjects:
- kind: User
  name: "alice@example.com"
  apiGroup: rbac.authorization.k8s.io
```

<!--
For a group named `frontend-admins`:
-->
对于名称为 `frontend-admins` 的用户组：

```yaml
subjects:
- kind: Group
  name: "frontend-admins"
  apiGroup: rbac.authorization.k8s.io
```

<!--
For the default service account in the "kube-system" namespace:
-->
对于 `kube-system` 名字空间中的默认服务账户：

```yaml
subjects:
- kind: ServiceAccount
  name: default
  namespace: kube-system
```

<!--
For all service accounts in the "qa" group in any namespace:
-->
对于任何名称空间中的 "qa" 组中所有的服务账户：

```yaml
subjects:
- kind: Group
  name: system:serviceaccounts:qa
  apiGroup: rbac.authorization.k8s.io
```

<!-- 
For all service accounts in the "dev" group in the "development" namespace:
-->
对于 "development" 名称空间中 "dev" 组中的所有服务帐户：

```yaml
subjects:
- kind: Group
  name: system:serviceaccounts:dev
  apiGroup: rbac.authorization.k8s.io
  namespace: development
```

<!--
For all service accounts in any namespace:
-->
对于在任何名字空间中的服务账户：

```yaml
subjects:
- kind: Group
  name: system:serviceaccounts
  apiGroup: rbac.authorization.k8s.io
```

<!--
For all authenticated users:
-->
对于所有已经过认证的用户：

```yaml
subjects:
- kind: Group
  name: system:authenticated
  apiGroup: rbac.authorization.k8s.io
```

<!--
For all unauthenticated users:
-->
对于所有未通过认证的用户：

```yaml
subjects:
- kind: Group
  name: system:unauthenticated
  apiGroup: rbac.authorization.k8s.io
```

<!--
For all users:
-->
对于所有用户：

```yaml
subjects:
- kind: Group
  name: system:authenticated
  apiGroup: rbac.authorization.k8s.io
- kind: Group
  name: system:unauthenticated
  apiGroup: rbac.authorization.k8s.io
```

<!--
## Default roles and role bindings

API servers create a set of default ClusterRole and ClusterRoleBinding objects.
Many of these are `system:` prefixed, which indicates that the resource is directly
managed by the cluster control plane.
All of the default ClusterRoles and ClusterRoleBindings are labeled with `kubernetes.io/bootstrapping=rbac-defaults`.
-->
## 默认 Roles 和 Role Bindings

API 服务器创建一组默认的 ClusterRole 和 ClusterRoleBinding 对象。
这其中许多是以 `system:` 为前缀的，用以标识对应资源是直接由集群控制面管理的。
所有的默认 ClusterRole 和 ClusterRoleBinding 都有
`kubernetes.io/bootstrapping=rbac-defaults`
标签。

{{< caution >}}
<!--
Take care when modifying ClusterRoles and ClusterRoleBindings with names
that have a `system:` prefix.
Modifications to these resources can result in non-functional clusters.
-->
在修改名称包含 `system:` 前缀的 ClusterRole 和 ClusterRoleBinding
时要格外小心。
对这些资源的更改可能导致集群无法继续工作。
{{< /caution >}}

<!--
### Auto-reconciliation

At each start-up, the API server updates default cluster roles with any missing permissions,
and updates default cluster role bindings with any missing subjects.
This allows the cluster to repair accidental modifications, and helps to keep roles and role bindings
up-to-date as permissions and subjects change in new releases.

To opt out of this reconciliation, set the `rbac.authorization.kubernetes.io/autoupdate`
annotation on a default cluster role or rolebinding to `false`.
Be aware that missing default permissions and subjects can result in non-functional clusters.

Auto-reconciliation is enabled by default if the RBAC authorizer is active.
-->
### 自动协商   {#auto-reconciliation}

在每次启动时，API 服务器都会更新默认 ClusterRole 以添加缺失的各种权限，并更新
默认的 ClusterRoleBinding 以增加缺失的各类主体。
这种自动协商机制允许集群去修复一些不小心发生的修改，并且有助于保证角色和角色绑定
在新的发行版本中有权限或主体变更时仍然保持最新。

如果要禁止此功能，请将默认 ClusterRole 以及 ClusterRoleBinding 的
`rbac.authorization.kubernetes.io/autoupdate` 注解设置成 `false`。
注意，缺少默认权限和角色绑定主体可能会导致集群无法正常工作。

如果基于 RBAC 的鉴权机制被启用，则自动协商功能默认是被启用的。

<!--
### API discovery roles {#discovery-roles}

Default role bindings authorize unauthenticated and authenticated users to read API information that is deemed safe to be publicly accessible (including CustomResourceDefinitions). To disable anonymous unauthenticated access add `--anonymous-auth=false` to the API server configuration.

To view the configuration of these roles via `kubectl` run:
-->
### API 发现角色  {#discovery-roles}

无论是经过身份验证的还是未经过身份验证的用户，默认的角色绑定都授权他们读取被认为
是可安全地公开访问的 API（ 包括 CustomResourceDefinitions）。
如果要禁用匿名的未经过身份验证的用户访问，请在 API 服务器配置中中添加
`--anonymous-auth=false` 的配置选项。

通过运行命令 `kubectl` 可以查看这些角色的配置信息:

```shell
kubectl get clusterroles system:discovery -o yaml
```

{{< note >}}
<!--
If you edit that ClusterRole, your changes will be overwritten on API server restart
via [auto-reconciliation](#auto-reconciliation). To avoid that overwriting,
either do not manually edit the role, or disable auto-reconciliation.
-->
如果你编辑该 ClusterRole，你所作的变更会被 API 服务器在重启时自动覆盖，这是通过
[自动协商](#auto-reconciliation)机制完成的。要避免这类覆盖操作，
要么不要手动编辑这些角色，要么禁止自动协商机制。
{{< /note >}}

<table>
<caption>
<!--
Kubernetes RBAC API discovery roles
-->
Kubernetes RBAC API 发现角色
</caption>
<colgroup><col width="25%"><col width="25%"><col></colgroup>
<thead>
<tr>
<!--
<th>Default ClusterRole</th>
<th>Default ClusterRoleBinding</th>
<th>Description</th>
-->
<th>默认 ClusterRole</th>
<th>默认 ClusterRoleBinding</th>
<th>描述</th>
</tr>
</thead>
<tbody>
<tr>
<td><b>system:basic-user</b></td>
<!-- 
<td><b>system:authenticated</b> group</td>
-->
<td><b>system:authenticated</b> 组</td>
<td>
<!-- 
Allows a user read-only access to basic information about themselves. 
Prior to 1.14, this role was also bound to <tt>system:unauthenticated</tt> by default.
-->
允许用户以只读的方式去访问他们自己的基本信息。在 1.14 版本之前，这个角色在默认情况下也绑定在 <tt>system:unauthenticated</tt> 上。
</td>
</tr>
<tr>
<td><b>system:discovery</b></td>
<!-- 
<td><b>system:authenticated</b> group</td>
-->
<td><b>system:authenticated</b> 组</td>
<td>
<!-- 
Allows read-only access to API discovery endpoints needed to discover and negotiate an API level. 
Prior to 1.14, this role was also bound to <tt>system:unauthenticated</tt> by default.
-->
允许以只读方式访问 API 发现端点，这些端点用来发现和协商 API 级别。
在 1.14 版本之前，这个角色在默认情况下绑定在 <tt>system:unauthenticated</tt> 上。
</td>
</tr>
<tr>
<td><b>system:public-info-viewer</b></td>
<!-- 
<td><b>system:authenticated</b> and <b>system:unauthenticated</b> groups</td>
-->
<td><b>system:authenticated</b> 和 <b>system:unauthenticated</b> 组</td>
<td>
<!-- 
Allows read-only access to non-sensitive information about the cluster. Introduced in Kubernetes v1.14.
-->
允许对集群的非敏感信息进行只读访问，它是在 1.14 版本中引入的。
</td>
</tr>
</tbody>
</table>

<!--
### User-facing roles

Some of the default ClusterRoles are not `system:` prefixed. These are intended to be user-facing roles.
They include super-user roles (`cluster-admin`), roles intended to be granted cluster-wide
using ClusterRoleBindings, and roles intended to be granted within particular
namespaces using RoleBindings (`admin`, `edit`, `view`).

User-facing ClusterRoles use [ClusterRole aggregation](#aggregated-clusterroles) to allow admins to include
rules for custom resources on these ClusterRoles. To add rules to the `admin`, `edit`, or `view` roles, create
a ClusterRole with one or more of the following labels:
-->
### 面向用户的角色   {#user-facing-roles}

一些默认的 ClusterRole 不是以前缀 `system:` 开头的。这些是面向用户的角色。
它们包括超级用户（Super-User）角色（`cluster-admin`）、
使用 ClusterRoleBinding 在集群范围内完成授权的角色（`cluster-status`）、
以及使用 RoleBinding 在特定名字空间中授予的角色（`admin`、`edit`、`view`）。

面向用户的 ClusterRole 使用 [ClusterRole 聚合](#aggregated-clusterroles)以允许管理员在
这些 ClusterRole 上添加用于定制资源的规则。如果想要添加规则到 `admin`、`edit` 或者 `view`，
可以创建带有以下一个或多个标签的 ClusterRole：

```yaml
metadata:
  labels:
    rbac.authorization.k8s.io/aggregate-to-admin: "true"
    rbac.authorization.k8s.io/aggregate-to-edit: "true"
    rbac.authorization.k8s.io/aggregate-to-view: "true"
```

<table>
<colgroup><col width="25%"><col width="25%"><col></colgroup>
<thead>
<tr>
<!--
<th>Default ClusterRole</th>
<th>Default ClusterRoleBinding</th>
<th>Description</th>
-->
<th>默认 ClusterRole</th>
<th>默认 ClusterRoleBinding</th>
<th>描述</th>
</tr>
</thead>
<tbody>
<tr>
<td><b>cluster-admin</b></td>
<!--
<td><b>system:masters</b> group</td>
-->
<td><b>system:masters</b> 组</td>
<td>
<!-- 
Allows super-user access to perform any action on any resource.
When used in a <b>ClusterRoleBinding</b>, it gives full control over every resource in the cluster and in all namespaces.
When used in a <b>RoleBinding</b>, it gives full control over every resource in the rolebinding's namespace, including the namespace itself.
-->
允许超级用户在平台上的任何资源上执行所有操作。
当在 <b>ClusterRoleBinding</b> 中使用时，可以授权对集群中以及所有名字空间中的全部资源进行完全控制。
当在 <b>RoleBinding</b> 中使用时，可以授权控制 RoleBinding 所在名字空间中的所有资源，包括名字空间本身。
</td>
</tr>
<tr>
<td><b>admin</b></td>
<!-- 
<td>None</td>
--->
<td>无</td>
<td>
<!-- 
Allows admin access, intended to be granted within a namespace using a <b>RoleBinding</b>.
If used in a <b>RoleBinding</b>, allows read/write access to most resources in a namespace,
including the ability to create roles and rolebindings within the namespace.
It does not allow write access to resource quota or to the namespace itself.
-->
允许管理员访问权限，旨在使用 <b>RoleBinding</b> 在名字空间内执行授权。
如果在 <b>RoleBinding</b> 中使用，则可授予对名字空间中的大多数资源的读/写权限，
包括创建角色和角色绑定的能力。
但是它不允许对资源配额或者名字空间本身进行写操作。
</td>
</tr>
<tr>
<td><b>edit</b></td>
<!-- 
<td>None</td>
-->
<td>无</td>
<td>
<!-- 
Allows read/write access to most objects in a namespace.
This role does not allow viewing or modifying roles or role bindings.
However, this role allows accessing Secrets and running Pods as any ServiceAccount in
the namespace, so it can be used to gain the API access levels of any ServiceAccount in
the namespace.
-->
允许对名字空间的大多数对象进行读/写操作。
它不允许查看或者修改角色或者角色绑定。
不过，此角色可以访问 Secret，以名字空间中任何 ServiceAccount 的身份运行 Pods，
所以可以用来了解名字空间内所有服务账户的 API 访问级别。
</td>
</tr>
<tr>
<td><b>view</b></td>
<!-- 
<td>None</td>
-->
<td>无</td>
<td>
<!-- 
Allows read-only access to see most objects in a namespace.
It does not allow viewing roles or rolebindings.
-->
允许对名字空间的大多数对象有只读权限。
它不允许查看角色或角色绑定。

<!--
This role does not allow viewing Secrets, since reading
the contents of Secrets enables access to ServiceAccount credentials
in the namespace, which would allow API access as any ServiceAccount
in the namespace (a form of privilege escalation). 
-->
此角色不允许查看 Secrets，因为读取 Secret 的内容意味着可以访问名字空间中
ServiceAccount 的凭据信息，进而允许利用名字空间中任何 ServiceAccount 的
身份访问 API（这是一种特权提升）。
</td>
</tr>
</tbody>
</table>

<!--
### Core component roles
-->
### 核心组件角色   {#core-component-roles}

<table>
<colgroup><col width="25%"><col width="25%"><col></colgroup>
<thead>
<tr>
<!--
<th>Default ClusterRole</th>
<th>Default ClusterRoleBinding</th>
<th>Description</th>
-->
<th>默认 ClusterRole</th>
<th>默认 ClusterRoleBinding</th>
<th>描述</th>
</tr>
</thead>
<tbody>
<tr>
<td><b>system:kube-scheduler</b></td>
<!-- 
<td><b>system:kube-scheduler</b> user</td> 
-->
<td><b>system:kube-scheduler</b> 用户</td>
<td>
<!-- 
Allows access to the resources required by the {{< glossary_tooltip term_id="kube-scheduler" text="scheduler" >}} component.
-->
允许访问 {{< glossary_tooltip term_id="kube-scheduler" text="scheduler" >}}
组件所需要的资源。
</td>
</tr>
<tr>
<td><b>system:volume-scheduler</b></td>
<!-- 
<td><b>system:kube-scheduler</b> user</td> 
-->
<td><b>system:kube-scheduler</b> 用户</td>
<td>
<!--
Allows access to the volume resources required by the kube-scheduler component.
-->
允许访问 kube-scheduler 组件所需要的卷资源。
</td>
</tr>
<tr>
<td><b>system:kube-controller-manager</b></td>
<!-- 
<td><b>system:kube-controller-manager</b> user</td> 
-->
<td><b>system:kube-controller-manager</b> 用户</td>
<td>
<!-- 
Allows access to the resources required by the {{< glossary_tooltip term_id="kube-controller-manager" text="controller manager" >}} component.
The permissions required by individual controllers are detailed in the <a href="#controller-roles">controller roles</a>.
-->
允许访问{{< glossary_tooltip term_id="kube-controller-manager" text="控制器管理器" >}}
组件所需要的资源。
各个控制回路所需要的权限在<a href="#controller-roles">控制器角色</a> 详述。
</td>
</tr>
<tr>
<td><b>system:node</b></td>
<!-- 
<td>None</td>
-->
<td>无</td>
<td>
<!--
Allows access to resources required by the kubelet, <b>including read access to all secrets, and write access to all pod status objects</b>.
-->
允许访问 kubelet 所需要的资源，<b>包括对所有 Secret 的读操作和对所有 Pod 状态对象的写操作。</b>

<!--  
You should use the <a href="/docs/reference/access-authn-authz/node/">Node authorizer</a> and 
<a href="/docs/reference/access-authn-authz/admission-controllers/#noderestriction">NodeRestriction admission plugin</a> 
instead of the <tt>system:node</tt> role, and allow granting API access to kubelets based on the Pods scheduled to run on them.
-->
你应该使用 <a href="/zh/docs/reference/access-authn-authz/node/">Node 鉴权组件</a> 和
<a href="/zh/docs/reference/access-authn-authz/admission-controllers/#noderestriction">NodeRestriction 准入插件</a>
而不是 <tt>system:node</tt> 角色。同时基于 kubelet 上调度执行的 Pod 来授权
kubelet 对 API 的访问。

<!--  
The <tt>system:node</tt> role only exists for compatibility with Kubernetes clusters upgraded from versions prior to v1.8.
-->
<tt>system:node</tt> 角色的意义仅是为了与从 v1.8 之前版本升级而来的集群兼容。
</td>
</tr>
<tr>
<td><b>system:node-proxier</b></td>
<!-- <td><b>system:kube-proxy</b> user</td> -->
<td><b>system:kube-proxy</b> 用户</td>
<!-- td>Allows access to the resources required by the {{< glossary_tooltip term_id="kube-proxy" text="kube-proxy" >}} component.</td-->
<td>允许访问 {{< glossary_tooltip term_id="kube-proxy" text="kube-proxy" >}}
组件所需要的资源。</td>
</tr>
</tbody>
</table>

<!--
### Other component roles
-->
### 其他组件角色    {#other-component-roles}

<table>
<colgroup><col width="25%"><col width="25%"><col></colgroup>
<thead>
<tr>
<!-- 
<th>Default ClusterRole</th>
<th>Default ClusterRoleBinding</th>
<th>Description</th> 
-->
<th>默认 ClusterRole</th>
<th>默认 ClusterRoleBinding</th>
<th>描述</th>
</tr>
</thead>
<tbody>
<tr>
<td><b>system:auth-delegator</b></td>
<!-- 
<td>None</td> 
-->
<td>无</td>
<td>
<!-- 
Allows delegated authentication and authorization checks.
This is commonly used by add-on API servers for unified authentication and authorization.
-->
允许将身份认证和鉴权检查操作外包出去。
这种角色通常用在插件式 API 服务器上，以实现统一的身份认证和鉴权。
</td>
</tr>
<tr>
<td><b>system:heapster</b></td>
<!-- 
<td>None</td> 
-->
<td>无</td>
<td>
<!--
Role for the <a href="https://github.com/kubernetes/heapster">Heapster</a> component (deprecated).
-->
为 <a href="https://github.com/kubernetes/heapster">Heapster</a> 组件（已弃用）定义的角色。
</td>
</tr>
<tr>
<td><b>system:kube-aggregator</b></td>
<!-- 
<td>None</td> 
-->
<td>无</td>
<!-- td>Role for the <a href="https://github.com/kubernetes/kube-aggregator">kube-aggregator</a> component.</td -->
<td>为 <a href="https://github.com/kubernetes/kube-aggregator">kube-aggregator</a> 组件定义的角色。</td>
</tr>
<tr>
<td><b>system:kube-dns</b></td>
<td>
<!--
<b>kube-dns</b> service account in the <b>kube-system</b> namespace</td 
-->
在 <b>kube-system</b> 名字空间中的 <b>kube-dns</b> 服务账户</td>
<!-- td>Role for the <a href="/docs/concepts/services-networking/dns-pod-service/">kube-dns</a> component.</td -->
<td>为 <a href="/docs/concepts/services-networking/dns-pod-service/">kube-dns</a> 组件定义的角色。
</td>
</tr>
<tr>
<td><b>system:kubelet-api-admin</b></td>
<!-- 
<td>None</td> 
-->
<td>无</td>
<td>
<!-- 
Allows full access to the kubelet API.
-->
允许 kubelet API 的完全访问权限。
</td>
</tr>  
<tr>
<td><b>system:node-bootstrapper</b></td>
<!-- 
<td>None</td> 
-->
<td>无</td>
<td>
<!-- 
Allows access to the resources required to perform
<a href="/docs/reference/command-line-tools-reference/kubelet-tls-bootstrapping/">Kubelet TLS bootstrapping</a>.
-->
允许访问执行
<a href="/docs/reference/command-line-tools-reference/kubelet-tls-bootstrapping/">kubelet TLS 启动引导</a>
所需要的资源。
</td>
</tr>
<tr>
<td><b>system:node-problem-detector</b></td>
<!-- 
<td>None</td> 
-->
<td>无</td>
<td>
<!-- 
Role for the <a href="https://github.com/kubernetes/node-problem-detector">node-problem-detector</a> component.
-->
为 <a href="https://github.com/kubernetes/node-problem-detector">node-problem-detector</a> 组件定义的角色。
</td>
</tr>
<tr>
<td><b>system:persistent-volume-provisioner</b></td>
<!-- 
<td>None</td> 
-->
<td>无</td>
<td>
<!-- 
Allows access to the resources required by most <a href="/docs/concepts/storage/persistent-volumes/#provisioner">dynamic volume provisioners</a>.
-->
允许访问大部分
<a href="/docs/concepts/storage/persistent-volumes/#provisioner">动态卷驱动
</a>
所需要的资源。</td>
</tr>
<tr>
<td><b>system:monitoring</b></td>
<!-- 
<td><b>system:monitoring</b> group</td>
-->
<td><b>system:monitoring</b> 组</td>
<td>
<!--
Allows read access to control-plane monitoring endpoints 
(i.e. {{< glossary_tooltip term_id="kube-apiserver" text="kube-apiserver" >}} liveness and readiness endpoints 
(<tt>/healthz</tt>, <tt>/livez</tt>, <tt>/readyz</tt>), the individual health-check endpoints 
(<tt>/healthz/*</tt>, <tt>/livez/*</tt>, <tt>/readyz/*</tt>),  and <tt>/metrics</tt>).
 Note that individual health check endpoints and the metric endpoint may expose sensitive information.
-->
允许对控制平面监控端点的读取访问（例如：{{< glossary_tooltip term_id="kube-apiserver" text="kube-apiserver" >}}
存活和就绪端点（<tt>/healthz</tt>、<tt>/livez</tt>、<tt>/readyz</tt>），
各个健康检查端点（<tt>/healthz/*</tt>、<tt>/livez/*</tt>、<tt>/readyz/*</tt>）和 <tt>/metrics</tt>）。
请注意，各个运行状况检查端点和度量标准端点可能会公开敏感信息。
</td>
</tr>
</tbody>
</table>

<!--
### Roles for built-in controllers {#controller-roles}

The Kubernetes {{< glossary_tooltip term_id="kube-controller-manager" text="controller manager" >}} runs
{{< glossary_tooltip term_id="controller" text="controllers" >}} that are built in to the Kubernetes
control plane.
When invoked with `-use-service-account-credentials`, kube-controller-manager starts each controller
using a separate service account.
Corresponding roles exist for each built-in controller, prefixed with `system:controller:`.
If the controller manager is not started with `-use-service-account-credentials`, it runs all control loops
using its own credential, which must be granted all the relevant roles.
These roles include:
-->
### 内置控制器的角色   {#controller-roles}

Kubernetes {{< glossary_tooltip term_id="kube-controller-manager" text="控制器管理器" >}}
运行内建于 Kubernetes 控制面的{{< glossary_tooltip term_id="controller" text="控制器" >}}。
当使用 `--use-service-account-credentials` 参数启动时, kube-controller-manager
使用单独的服务账户来启动每个控制器。
每个内置控制器都有相应的、前缀为 `system:controller:` 的角色。
如果控制管理器启动时未设置 `--use-service-account-credentials`，
它使用自己的身份凭据来运行所有的控制器，该身份必须被授予所有相关的角色。
这些角色包括:

* `system:controller:attachdetach-controller`
* `system:controller:certificate-controller`
* `system:controller:clusterrole-aggregation-controller`
* `system:controller:cronjob-controller`
* `system:controller:daemon-set-controller`
* `system:controller:deployment-controller`
* `system:controller:disruption-controller`
* `system:controller:endpoint-controller`
* `system:controller:expand-controller`
* `system:controller:generic-garbage-collector`
* `system:controller:horizontal-pod-autoscaler`
* `system:controller:job-controller`
* `system:controller:namespace-controller`
* `system:controller:node-controller`
* `system:controller:persistent-volume-binder`
* `system:controller:pod-garbage-collector`
* `system:controller:pv-protection-controller`
* `system:controller:pvc-protection-controller`
* `system:controller:replicaset-controller`
* `system:controller:replication-controller`
* `system:controller:resourcequota-controller`
* `system:controller:root-ca-cert-publisher`
* `system:controller:route-controller`
* `system:controller:service-account-controller`
* `system:controller:service-controller`
* `system:controller:statefulset-controller`
* `system:controller:ttl-controller`

<!--
## Privilege Escalation Prevention and Bootstrapping

The RBAC API prevents users from escalating privileges by editing roles or role bindings.
Because this is enforced at the API level, it applies even when the RBAC authorizer is not in use.
-->
## 初始化与预防权限提升

RBAC API 会阻止用户通过编辑角色或者角色绑定来提升权限。
由于这一点是在 API 级别实现的，所以在 RBAC 鉴权组件未启用的状态下依然可以正常工作。

<!--
### Restrictions on role creation or update

You can only create/update a role if at least one of the following things is true:

1. You already have all the permissions contained in the role, at the same scope as the object being modified
(cluster-wide for a ClusterRole, within the same namespace or cluster-wide for a Role).
2. You are granted explicit permission to perform the `escalate` verb on the `roles` or `clusterroles` resource in the `rbac.authorization.k8s.io` API group.
-->
### 对角色创建或更新的限制

只有在符合下列条件之一的情况下，你才能创建/更新角色:

1. 你已经拥有角色中包含的所有权限，且其作用域与正被修改的对象作用域相同。
  （对 ClusterRole 而言意味着集群范围，对 Role 而言意味着相同名字空间或者集群范围）。
2. 你被显式授权在 `rbac.authorization.k8s.io` API 组中的 `roles` 或 `clusterroles` 资源
   使用 `escalate` 动词。

<!--
For example, if `user-1` does not have the ability to list Secrets cluster-wide, they cannot create a ClusterRole
containing that permission. To allow a user to create/update roles:

1. Grant them a role that allows them to create/update Role or ClusterRole objects, as desired.
2. Grant them permission to include specific permissions in the roles they create/update:
    * implicitly, by giving them those permissions (if they attempt to create or modify a Role or ClusterRole with permissions they themselves have not been granted, the API request will be forbidden)
    * or explicitly allow specifying any permission in a `Role` or `ClusterRole` by giving them permission to perform the `escalate` verb on `roles` or `clusterroles` resources in the `rbac.authorization.k8s.io` API group
-->
例如，如果 `user-1` 没有列举集群范围所有 Secret 的权限，他将不能创建包含该权限的 ClusterRole。
若要允许用户创建/更新角色：

1. 根据需要赋予他们一个角色，允许他们根据需要创建/更新 Role 或者 ClusterRole 对象。
2. 授予他们在所创建/更新角色中包含特殊权限的权限:
   * 隐式地为他们授权（如果它们试图创建或者更改 Role 或 ClusterRole 的权限，
     但自身没有被授予相应权限，API 请求将被禁止）。
   * 通过允许他们在 Role 或 ClusterRole 资源上执行 `escalate` 动作显式完成授权。
     这里的 `roles` 和 `clusterroles` 资源包含在 `rbac.authorization.k8s.io` API 组中。

<!--
### Restrictions on role binding creation or update

You can only create/update a role binding if you already have all the permissions contained in the referenced role
(at the same scope as the role binding) *or* if you have been authorized to perform the `bind` verb on the referenced role.
For example, if `user-1` does not have the ability to list Secrets cluster-wide, they cannot create a ClusterRoleBinding
to a role that grants that permission. To allow a user to create/update role bindings:
-->
### 对角色绑定创建或更新的限制

只有你已经具有了所引用的角色中包含的全部权限时，或者你被授权在所引用的角色上执行 `bind`
动词时，你才可以创建或更新角色绑定。这里的权限与角色绑定的作用域相同。
例如，如果用户 `user-1` 没有列举集群范围所有 Secret 的能力，则他不可以创建
ClusterRoleBinding 引用授予该许可权限的角色。
如要允许用户创建或更新角色绑定：

<!--
1. Grant them a role that allows them to create/update RoleBinding or ClusterRoleBinding objects, as desired.
2. Grant them permissions needed to bind a particular role:
    * implicitly, by giving them the permissions contained in the role.
    * explicitly, by giving them permission to perform the `bind` verb on the particular Role (or ClusterRole).

For example, this ClusterRole and RoleBinding would allow `user-1` to grant other users the `admin`, `edit`, and `view` roles in the namespace `user-1-namespace`:
-->
1. 赋予他们一个角色，使得他们能够根据需要创建或更新 RoleBinding 或 ClusterRoleBinding
   对象。
2. 授予他们绑定某特定角色所需要的许可权限：
   * 隐式授权下，可以将角色中包含的许可权限授予他们；
   * 显式授权下，可以授权他们在特定 Role （或 ClusterRole）上执行 `bind` 动词的权限。

例如，下面的 ClusterRole 和 RoleBinding 将允许用户 `user-1` 把名字空间 `user-1-namespace`
中的 `admin`、`edit` 和 `view` 角色赋予其他用户：

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: role-grantor
rules:
- apiGroups: ["rbac.authorization.k8s.io"]
  resources: ["rolebindings"]
  verbs: ["create"]
- apiGroups: ["rbac.authorization.k8s.io"]
  resources: ["clusterroles"]
  verbs: ["bind"]
  # 忽略 resourceNames 意味着允许绑定任何 ClusterRole
  resourceNames: ["admin","edit","view"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: role-grantor-binding
  namespace: user-1-namespace
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: role-grantor
subjects:
- apiGroup: rbac.authorization.k8s.io
  kind: User
  name: user-1
```

<!--
When bootstrapping the first roles and role bindings, it is necessary for the initial user to grant permissions they do not yet have.
To bootstrap initial roles and role bindings:

* Use a credential with the `system:masters` group, which is bound to the `cluster-admin` super-user role by the default bindings.
* If your API server runs with the insecure port enabled (`-insecure-port`), you can also make API calls via that port, which does not enforce authentication or authorization.
-->
当启动引导第一个角色和角色绑定时，需要为初始用户授予他们尚未拥有的权限。
对初始角色和角色绑定进行初始化时需要：

* 使用用户组为 `system:masters` 的凭据，该用户组由默认绑定关联到 `cluster-admin`
  这个超级用户角色。
* 如果你的 API 服务器启动时启用了不安全端口（使用 `--insecure-port`）, 你也可以通过
  该端口调用 API ，这样的操作会绕过身份验证或鉴权。

<!--
## Command-line Utilities

### `kubectl create role`

Creates a `Role` object defining permissions within a single namespace. Examples:

* Create a Role named "pod-reader" that allows users to perform `get`, `watch` and `list` on pods:
-->
## 一些命令行工具

### `kubectl create role`

创建 Role 对象，定义在某一名字空间中的权限。例如:

* 创建名称为 "pod-reader" 的 Role 对象，允许用户对 Pods 执行 `get`、`watch` 和 `list` 操作：

  ```shell
  kubectl create role pod-reader --verb=get --verb=list --verb=watch --resource=pods
  ```

<!--
* Create a Role named "pod-reader" with resourceNames specified:
-->
* 创建名称为 "pod-reader" 的 Role 对象并指定 `resourceNames`：

  ```shell
  kubectl create role pod-reader --verb=get --resource=pods --resource-name=readablepod --resource-name=anotherpod
  ```

<!--
* Create a `Role` named "foo" with apiGroups specified:
-->
* 创建名为 "foo" 的 Role 对象并指定 `apiGroups`：

  ```shell
  kubectl create role foo --verb=get,list,watch --resource=replicasets.apps
  ```

<!--
* Create a Role named "foo" with subresource permissions:
-->
* 创建名为 "foo" 的 Role 对象并指定子资源权限:

  ```shell
  kubectl create role foo --verb=get,list,watch --resource=pods,pods/status
  ```

<!--
* Create a Role named "my-component-lease-holder" with permissions to get/update a resource with a specific name:
-->
* 创建名为 "my-component-lease-holder" 的 Role 对象，使其具有对特定名称的
  资源执行 get/update 的权限：

  ```shell
  kubectl create role my-component-lease-holder --verb=get,list,watch,update --resource=lease --resource-name=my-component
  ```

### `kubectl create clusterrole`

<!--
Creates a ClusterRole. Examples:

* Create a ClusterRole named "pod-reader" that allows user to perform `get`, `watch` and `list` on pods:
-->
创建 ClusterRole 对象。例如：

* 创建名称为 "pod-reader" 的 ClusterRole`对象，允许用户对 Pods 对象执行 `get`、
  `watch` 和 `list` 操作：

  ```shell
  kubectl create clusterrole pod-reader --verb=get,list,watch --resource=pods
  ```

<!--
* Create a ClusterRole named "pod-reader" with resourceNames specified:
-->
* 创建名为 "pod-reader" 的 ClusterRole 对象并指定 `resourceNames`：

  ```shell
  kubectl create clusterrole pod-reader --verb=get --resource=pods --resource-name=readablepod --resource-name=anotherpod
  ```

<!--
* Create a ClusterRole named "foo" with apiGroups specified:
-->
* 创建名为 "foo" 的 ClusterRole 对象并指定 `apiGroups`：

  ```shell
  kubectl create clusterrole foo --verb=get,list,watch --resource=replicasets.apps
  ```

<!--
* Create a ClusterRole named "foo" with subresource permissions:
-->
* 创建名为 "foo" 的 ClusterRole 对象并指定子资源:

  ```shell
  kubectl create clusterrole foo --verb=get,list,watch --resource=pods,pods/status
  ```

<!--
* Create a ClusterRole named "foo" with nonResourceURL specified:
-->
* 创建名为 "foo" 的 ClusterRole 对象并指定 `nonResourceURL`：

  ```shell
  kubectl create clusterrole "foo" --verb=get --non-resource-url=/logs/*
  ```

<!--
* Create a ClusterRole named "monitoring" with an aggregationRule specified:
-->
* 创建名为 "monitoring" 的 ClusterRole 对象并指定 `aggregationRule`：

  ```shell
  kubectl create clusterrole monitoring --aggregation-rule="rbac.example.com/aggregate-to-monitoring=true"
  ```

### `kubectl create rolebinding`

<!--
Grants a Role or ClusterRole within a specific namespace. Examples:

* Within the namespace "acme", grant the permissions in the "admin" ClusterRole to a user named "bob":
-->
在特定的名字空间中对 `Role` 或 `ClusterRole` 授权。例如：

* 在名字空间 "acme" 中，将名为 `admin` 的 ClusterRole 中的权限授予名称 "bob" 的用户:

  ```shell
  kubectl create rolebinding bob-admin-binding --clusterrole=admin --user=bob --namespace=acme
  ```

<!--
* Within the namespace "acme", grant the permissions in the "view" ClusterRole to the service account in the namespace "acme" named "myapp":
-->
* 在名字空间 "acme" 中，将名为 `view` 的 ClusterRole 中的权限授予名字空间 "acme"
  中名为 `myapp` 的服务账户：

  ```shell
  kubectl create rolebinding myapp-view-binding --clusterrole=view --serviceaccount=acme:myapp --namespace=acme
  ```

<!--
* Within the namespace "acme", grant the permissions in the "view" ClusterRole to a service account in the namespace "myappnamespace" named "myapp":
-->
* 在名字空间 "acme" 中，将名为 `view` 的 ClusterRole 对象中的权限授予名字空间
  "myappnamespace" 中名称为 `myapp` 的服务账户：

  ```shell
  kubectl create rolebinding myappnamespace-myapp-view-binding --clusterrole=view --serviceaccount=myappnamespace:myapp --namespace=acme
  ```

### `kubectl create clusterrolebinding`

<!--
Grants a ClusterRole across the entire cluster (all namespaces). Examples:

* Across the entire cluster, grant the permissions in the "cluster-admin" ClusterRole to a user named "root":
-->
在整个集群（所有名字空间）中用 ClusterRole 授权。例如：

* 在整个集群范围，将名为 `cluster-admin` 的 ClusterRole 中定义的权限授予名为
  "root" 用户：

  ```shell
  kubectl create clusterrolebinding root-cluster-admin-binding --clusterrole=cluster-admin --user=root
  ```

<!--
* Across the entire cluster, grant the permissions in the "system:node-proxier" ClusterRole to a user named "system:kube-proxy":
-->
* 在整个集群范围内，将名为 `system:node-proxier` 的 ClusterRole 的权限授予名为
  "system:kube-proxy" 的用户：

  ```shell
  kubectl create clusterrolebinding kube-proxy-binding --clusterrole=system:node-proxier --user=system:kube-proxy
  ```

<!--
* Across the entire cluster, grant the permissions in the "view" ClusterRole to a service account named "myapp" in the namespace "acme":
-->
* 在整个集群范围内，将名为 `view` 的 ClusterRole 中定义的权限授予 "acme" 名字空间中
  名为 "myapp" 的服务账户：

  ```shell
  kubectl create clusterrolebinding myapp-view-binding --clusterrole=view --serviceaccount=acme:myapp
  ```

### `kubectl auth reconcile` {#kubectl-auth-reconcile}

<!--
Creates or updates `rbac.authorization.k8s.io/v1` API objects from a manifest file.

Missing objects are created, and the containing namespace is created for namespaced objects, if required.

Existing roles are updated to include the permissions in the input objects,
and remove extra permissions if `--remove-extra-permissions` is specified.

Existing bindings are updated to include the subjects in the input objects,
and remove extra subjects if `--remove-extra-subjects` is specified.

Examples:
-->
使用清单文件来创建或者更新 `rbac.authorization.k8s.io/v1` API 对象。

尚不存在的对象会被创建，如果对应的名字空间也不存在，必要的话也会被创建。
已经存在的角色会被更新，使之包含输入对象中所给的权限。如果指定了
`--remove-extra-permissions`，可以删除额外的权限。

已经存在的绑定也会被更新，使之包含输入对象中所给的主体。如果指定了
`--remove-extra-permissions`，则可以删除多余的主体。

例如:

<!--
* Test applying a manifest file of RBAC objects, displaying changes that would be made:
-->
* 测试应用 RBAC 对象的清单文件，显示将要进行的更改：

  ```shell
  kubectl auth reconcile -f my-rbac-rules.yaml --dry-run
  ```

<!--
* Apply a manifest file of RBAC objects, preserving any extra permissions (in roles) and any extra subjects (in bindings):
-->
* 应用 RBAC 对象的清单文件，保留角色中的额外权限和绑定中的其他主体：

  ```shell
  kubectl auth reconcile -f my-rbac-rules.yaml
  ```

<!--
* Apply a manifest file of RBAC objects, removing any extra permissions (in roles) and any extra subjects (in bindings):
-->
* 应用 RBAC 对象的清单文件, 删除角色中的额外权限和绑定中的其他主体：

  ```shell
  kubectl auth reconcile -f my-rbac-rules.yaml --remove-extra-subjects --remove-extra-permissions
  ```

<!--
See the CLI help for detailed usage.
-->
查看 CLI 帮助获取详细的用法。

<!--
## ServiceAccount Permissions

Default RBAC policies grant scoped permissions to control-plane components, nodes,
and controllers, but grant *no permissions* to service accounts outside the `kube-system` namespace
(beyond discovery permissions given to all authenticated users).

This allows you to grant particular roles to particular service accounts as needed.
Fine-grained role bindings provide greater security, but require more effort to administrate.
Broader grants can give unnecessary (and potentially escalating) API access to service accounts, but are easier to administrate.
-->
## 服务账户权限   {#service-account-permissions}

默认的 RBAC 策略为控制面组件、节点和控制器授予权限。
但是不会对 `kube-system` 名字空间之外的服务账户授予权限。
（除了授予所有已认证用户的发现权限）

这使得你可以根据需要向特定服务账户授予特定权限。
细粒度的角色绑定可带来更好的安全性，但需要更多精力管理。
粗粒度的授权可能导致服务账户被授予不必要的 API 访问权限（甚至导致潜在的权限提升），
但更易于管理。

<!--
In order from most secure to least secure, the approaches are:

1. Grant a role to an application-specific service account (best practice)
-->
按从最安全到最不安全的顺序，存在以下方法：

1. 为特定应用的服务账户授予角色（最佳实践）

   <!--
   This requires the application to specify a `serviceAccountName` in its pod spec,
   and for the service account to be created (via the API, application manifest, `kubectl create serviceaccount`, etc.).

   For example, grant read-only permission within "my-namespace" to the "my-sa" service account:
   -->
   这要求应用在其 Pod 规约中指定 `serviceAccountName`，
   并额外创建服务账户（包括通过 API、应用程序清单、`kubectl create serviceaccount` 等）。  

   例如，在名字空间 "my-namespace" 中授予服务账户 "my-sa" 只读权限：

   ```shell
   kubectl create rolebinding my-sa-view \
     --clusterrole=view \
     --serviceaccount=my-namespace:my-sa \
     --namespace=my-namespace
   ```

<!--
2. Grant a role to the "default" service account in a namespace
-->
2. 将角色授予某名字空间中的 "default" 服务账户

   <!--
   If an application does not specify a `serviceAccountName`, it uses the "default" service account.

   {{< note >}}
   Permissions given to the "default" service account are available to any pod
   in the namespace that does not specify a `serviceAccountName`.
   {{< /note >}}

   For example, grant read-only permission within "my-namespace" to the "default" service account:
   -->
   如果某应用没有指定 `serviceAccountName`，那么它将使用 "default" 服务账户。

   {{< note >}}
   "default" 服务账户所具有的权限会被授予给名字空间中所有未指定
   `serviceAccountName` 的 Pod。
   {{< /note >}}

   例如，在名字空间 "my-namespace" 中授予服务账户 "default" 只读权限：

   ```shell
   kubectl create rolebinding default-view \
     --clusterrole=view \
     --serviceaccount=my-namespace:default \
     --namespace=my-namespace
   ```

   <!--
   Many [add-ons](/docs/concepts/cluster-administration/addons/) run as the
   "default" service account in the `kube-system` namespace.
   To allow those add-ons to run with super-user access, grant cluster-admin
   permissions to the "default" service account in the `kube-system` namespace.

   {{< note >}}
   Enabling this means the `kube-system` namespace contains Secrets
   that grant super-user access to the API.
   {{< /note >}}
   -->
   许多[插件组件](/zh/docs/concepts/cluster-administration/addons/) 在 `kube-system`
   名字空间以 "default" 服务账户运行。
   要允许这些插件组件以超级用户权限运行，需要将集群的 `cluster-admin` 权限授予
   `kube-system` 名字空间中的 "default" 服务账户。

   {{< note >}}
   启用这一配置意味着在 `kube-system` 名字空间中包含以超级用户账号来访问 API
   的 Secrets。
   {{< /note >}}

   ```shell
   kubectl create clusterrolebinding add-on-cluster-admin \
     --clusterrole=cluster-admin \
     --serviceaccount=kube-system:default
   ```
<!--
3. Grant a role to all service accounts in a namespace

   If you want all applications in a namespace to have a role, no matter what service account they use,
   you can grant a role to the service account group for that namespace.

   For example, grant read-only permission within "my-namespace" to all service accounts in that namespace:
-->
3. 将角色授予名字空间中所有服务账户

   如果你想要名字空间中所有应用都具有某角色，无论它们使用的什么服务账户，
   可以将角色授予该名字空间的服务账户组。

   例如，在名字空间 "my-namespace" 中的只读权限授予该名字空间中的所有服务账户：

   ```shell
   kubectl create rolebinding serviceaccounts-view \
     --clusterrole=view \
     --group=system:serviceaccounts:my-namespace \
     --namespace=my-namespace
   ```

<!--
4. Grant a limited role to all service accounts cluster-wide (discouraged)

   If you don't want to manage permissions per-namespace, you can grant a cluster-wide role to all service accounts.

   For example, grant read-only permission across all namespaces to all service accounts in the cluster:
-->
4. 在集群范围内为所有服务账户授予一个受限角色（不鼓励）

   如果你不想管理每一个名字空间的权限，你可以向所有的服务账户授予集群范围的角色。

   例如，为集群范围的所有服务账户授予跨所有名字空间的只读权限：


   ```shell
   kubectl create clusterrolebinding serviceaccounts-view \
     --clusterrole=view \
     --group=system:serviceaccounts
   ```

<!--
5. Grant super-user access to all service accounts cluster-wide (strongly discouraged)

   If you don't care about partitioning permissions at all, you can grant super-user access to all service accounts.

   {{< warning >}}
   This allows any application full access to your cluster, and also grants
   any user with read access to Secrets (or the ability to create any pod)
   full access to your cluster.
   {{< /warning >}}
-->
5. 授予超级用户访问权限给集群范围内的所有服务帐户（强烈不鼓励）

   如果你不关心如何区分权限，你可以将超级用户访问权限授予所有服务账户。

   {{< warning >}}
   这样做会允许所有应用都对你的集群拥有完全的访问权限，并将允许所有能够读取
   Secret（或创建 Pod）的用户对你的集群有完全的访问权限。
   {{< /warning >}}

   ```shell
   kubectl create clusterrolebinding serviceaccounts-cluster-admin \
     --clusterrole=cluster-admin \
     --group=system:serviceaccounts
   ```

<!--
## Upgrading from ABAC

Clusters that originally ran older Kubernetes versions often used
permissive ABAC policies, including granting full API access to all
service accounts.

Default RBAC policies grant scoped permissions to control-plane components, nodes,
and controllers, but grant *no permissions* to service accounts outside the `kube-system` namespace
(beyond discovery permissions given to all authenticated users).

While far more secure, this can be disruptive to existing workloads expecting to automatically receive API permissions.
Here are two approaches for managing this transition:
-->
## 从 ABAC 升级

原来运行较老版本 Kubernetes 的集群通常会使用限制宽松的 ABAC 策略，
包括授予所有服务帐户全权访问 API 的能力。

默认的 RBAC 策略为控制面组件、节点和控制器等授予有限的权限，但不会为
`kube-system` 名字空间外的服务账户授权
（除了授予所有认证用户的发现权限之外）。

这样做虽然安全得多，但可能会干扰期望自动获得 API 权限的现有工作负载。
这里有两种方法来完成这种转换:

<!--
### Parallel Authorizers

Run both the RBAC and ABAC authorizers, and specify a policy file that contains
[the legacy ABAC policy](/docs/reference/access-authn-authz/abac/#policy-file-format):
-->
### 并行鉴权    {#parallel-authorizers}

同时运行 RBAC 和 ABAC 鉴权模式, 并指定包含
[现有的 ABAC 策略](/zh/docs/reference/access-authn-authz/abac/#policy-file-format)
的策略文件：

```shell
--authorization-mode=RBAC,ABAC --authorization-policy-file=mypolicy.json
```

<!--
To explain that first command line option in detail: if earlier authorizers, such as Node,
deny a request, then the RBAC authorizer attempts to authorize the API request. If RBAC
also denies that API request, the ABAC authorizer is then run. This means that any request
allowed by *either* the RBAC or ABAC policies is allowed.
-->
关于命令行中的第一个选项：如果早期的鉴权组件，例如 Node，拒绝了某个请求，则
RBAC 鉴权组件尝试对该 API 请求鉴权。如果 RBAC 也拒绝了该 API 请求，则运行 ABAC
鉴权组件。这意味着被 RBAC 或 ABAC 策略所允许的任何请求都是被允许的请求。

<!--
When the apiserver is run with a log level of 5 or higher for the RBAC component
(`--vmodule=rbac*=5` or `--v=5`), you can see RBAC details in the apiserver log
(prefixed with `RBAC:`).
You can use that information to determine which roles need to be granted to which users, groups, or service accounts.
-->
如果 API 服务器启动时，RBAC 组件的日志级别为 5 或更高（`--vmodule=rbac*=5` 或 `--v=5`），
你可以在 API 服务器的日志中看到 RBAC 的细节 （前缀 `RBAC:`）
你可以使用这些信息来确定需要将哪些角色授予哪些用户、组或服务帐户。

<!--
Once you have [granted roles to service accounts](#service-account-permissions) and workloads
are running with no RBAC denial messages in the server logs, you can remove the ABAC authorizer.
-->
一旦你[将角色授予服务账户](#service-account-permissions) ，工作负载运行时
在服务器日志中没有出现 RBAC 拒绝消息，就可以删除 ABAC 鉴权器。

<!--
## Permissive RBAC Permissions

You can replicate a permissive policy using RBAC role bindings.
-->
## 宽松的 RBAC 权限   {#permissive-rbac-permissions}

你可以使用 RBAC 角色绑定在多个场合使用宽松的策略。

{{< warning >}}
<!--
The following policy allows **ALL** service accounts to act as cluster administrators.
Any application running in a container receives service account credentials automatically,
and could perform any action against the API, including viewing secrets and modifying permissions.
This is not a recommended policy.
-->
下面的策略允许 **所有** 服务帐户充当集群管理员。
容器中运行的所有应用程序都会自动收到服务帐户的凭据，可以对 API 执行任何操作，
包括查看 Secrets 和修改权限。这一策略是不被推荐的。

```shell
kubectl create clusterrolebinding permissive-binding \
  --clusterrole=cluster-admin \
  --user=admin \
  --user=kubelet \
  --group=system:serviceaccounts
```
{{< /warning >}}

<!--
After you have transitioned to use RBAC, you should adjust the access controls
for your cluster to ensure that these meet your information security needs.
-->
在你完成到 RBAC 的迁移后，应该调整集群的访问控制，确保相关的策略满足你的
信息安全需求。

