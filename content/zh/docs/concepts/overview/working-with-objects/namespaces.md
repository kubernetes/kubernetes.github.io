---
title: 名字空间
content_type: concept
weight: 30
---
<!--
reviewers:
- derekwaynecarr
- mikedanese
- thockin
title: Namespaces
content_type: concept
weight: 30
-->

<!-- overview -->

<!--
Kubernetes supports multiple virtual clusters backed by the same physical cluster.
These virtual clusters are called namespaces.
-->
Kubernetes 支持多个虚拟集群，它们底层依赖于同一个物理集群。
这些虚拟集群被称为名字空间。
在一些文档里名字空间也称为命名空间。

<!-- body -->

<!--
## When to Use Multiple Namespaces
-->
## 何时使用多个名字空间

<!--
Namespaces are intended for use in environments with many users spread across multiple
teams, or projects.  For clusters with a few to tens of users, you should not
need to create or think about namespaces at all.  Start using namespaces when you
need the features they provide.
-->
名字空间适用于存在很多跨多个团队或项目的用户的场景。对于只有几到几十个用户的集群，根本不需要创建或考虑名字空间。当需要名称空间提供的功能时，请开始使用它们。

<!--
Namespaces provide a scope for names.  Names of resources need to be unique within a namespace,
but not across namespaces. Namespaces can not be nested inside one another and each Kubernetes
resource can only be in one namespace.
-->
名字空间为名称提供了一个范围。资源的名称需要在名字空间内是唯一的，但不能跨名字空间。
名字空间不能相互嵌套，每个 Kubernetes 资源只能在一个名字空间中。

<!--
Namespaces are a way to divide cluster resources between multiple users (via [resource quota](/docs/concepts/policy/resource-quotas/)).
-->
名字空间是在多个用户之间划分集群资源的一种方法（通过[资源配额](/zh/docs/concepts/policy/resource-quotas/)）。

<!--
It is not necessary to use multiple namespaces to separate slightly different
resources, such as different versions of the same software: use
{{< glossary_tooltip text="labels" term_id="label" >}} to distinguish
resources within the same namespace.
-->
不必使用多个名字空间来分隔仅仅轻微不同的资源，例如同一软件的不同版本：
应该使用{{< glossary_tooltip text="标签" term_id="label" >}}
来区分同一名字空间中的不同资源。

<!--
## Working with Namespaces

Creation and deletion of namespaces are described in the [Admin Guide documentation
for namespaces](/docs/tasks/administer-cluster/namespaces/).
-->
## 使用名字空间

名字空间的创建和删除在[名字空间的管理指南文档](/zh/docs/tasks/administer-cluster/namespaces/)描述。

<!--
Avoid creating namespaces with the prefix `kube-`, since it is reserved for Kubernetes system namespaces.
-->
{{< note >}}
避免使用前缀 `kube-` 创建名字空间，因为它是为 Kubernetes 系统名字空间保留的。
{{< /note >}}

<!--
### Viewing namespaces

You can list the current namespaces in a cluster using:
-->
### 查看名字空间

你可以使用以下命令列出集群中现存的名字空间：

```shell
kubectl get namespace
```
```
NAME          STATUS    AGE
default       Active    1d
kube-node-lease   Active   1d
kube-system   Active    1d
kube-public   Active    1d
```

<!--
Kubernetes starts with four initial namespaces:

* `default` The default namespace for objects with no other namespace
* `kube-system` The namespace for objects created by the Kubernetes system
* `kube-public` This namespace is created automatically and is readable by all users (including those not authenticated). This namespace is mostly reserved for cluster usage, in case that some resources should be visible and readable publicly throughout the whole cluster. The public aspect of this namespace is only a convention, not a requirement.
* `kube-node-lease` This namespace for the lease objects associated with each node which improves the performance of the node heartbeats as the cluster scales.
-->
Kubernetes 会创建四个初始名字空间：

* `default` 没有指明使用其它名字空间的对象所使用的默认名字空间
* `kube-system` Kubernetes 系统创建对象所使用的名字空间
* `kube-public` 这个名字空间是自动创建的，所有用户（包括未经过身份验证的用户）都可以读取它。
  这个名字空间主要用于集群使用，以防某些资源在整个集群中应该是可见和可读的。
  这个名字空间的公共方面只是一种约定，而不是要求。
* `kube-node-lease` 此名字空间用于与各个节点相关的租期（Lease）对象；
  此对象的设计使得集群规模很大时节点心跳检测性能得到提升。

<!--
### Setting the namespace for a request

To set the namespace for a current request, use the `-namespace` flag.

For example:
-->
### 为请求设置名字空间

要为当前请求设置名字空间，请使用 `--namespace` 参数。

例如：

```shell
kubectl run nginx --image=nginx --namespace=<名字空间名称>
kubectl get pods --namespace=<名字空间名称>
```

<!--
### Setting the namespace preference

You can permanently save the namespace for all subsequent kubectl commands in that
context.
-->
### 设置名字空间偏好

你可以永久保存名字空间，以用于对应上下文中所有后续 kubectl 命令。

```shell
kubectl config set-context --current --namespace=<名字空间名称>
# 验证之
kubectl config view | grep namespace:
```

<!--
## Namespaces and DNS

When you create a [Service](/docs/user-guide/services), it creates a corresponding [DNS entry](/docs/concepts/services-networking/dns-pod-service/).
-->
## 名字空间和 DNS

当你创建一个[服务](/zh/docs/concepts/services-networking/service/) 时，
Kubernetes 会创建一个相应的 [DNS 条目](/zh/docs/concepts/services-networking/dns-pod-service/)。

<!--
This entry is of the form `<service-name>.<namespace-name>.svc.cluster.local`, which means
that if a container only uses `<service-name>`, it will resolve to the service which
is local to a namespace.  This is useful for using the same configuration across
multiple namespaces such as Development, Staging and Production.  If you want to reach
across namespaces, you need to use the fully qualified domain name (FQDN).
-->
该条目的形式是 `<服务名称>.<名字空间名称>.svc.cluster.local`，这意味着如果容器只使用
`<服务名称>`，它将被解析到本地名字空间的服务。这对于跨多个名字空间（如开发、分级和生产）
使用相同的配置非常有用。如果你希望跨名字空间访问，则需要使用完全限定域名（FQDN）。

<!--
## Not All Objects are in a Namespace
-->
## 并非所有对象都在名字空间中

<!--
Most Kubernetes resources (e.g. pods, services, replication controllers, and others) are
in some namespaces.  However namespace resources are not themselves in a namespace.
And low-level resources, such as [nodes](/docs/concepts/architecture/nodes/) and
persistentVolumes, are not in any namespace.
-->
大多数 kubernetes 资源（例如 Pod、Service、副本控制器等）都位于某些名字空间中。
但是名字空间资源本身并不在名字空间中。而且底层资源，例如
[节点](/zh/docs/concepts/architecture/nodes/) 和持久化卷不属于任何名字空间。

<!--
To see which Kubernetes resources are and aren't in a namespace:
-->
查看哪些 Kubernetes 资源在名字空间中，哪些不在名字空间中：

```shell
# 位于名字空间中的资源
kubectl api-resources --namespaced=true

# 不在名字空间中的资源
kubectl api-resources --namespaced=false
```

<!--
## Automatic labelling
-->
## 自动打标签   {#automatic-labelling}

{{< feature-state state="beta" for_k8s_version="1.21" >}}

<!--
The Kubernetes control plane sets an immutable {{< glossary_tooltip text="label" term_id="label" >}}
`kubernetes.io/metadata.name` on all namespaces, provided that the `NamespaceDefaultLabelName`
[feature gate](/docs/reference/command-line-tools-reference/feature-gates/) is enabled.
The value of the label is the namespace name.
-->
Kubernetes 控制面会为所有名字空间设置一个不可变更的
{{< glossary_tooltip text="标签" term_id="label" >}}
`kubernetes.io/metadata.name`，只要 `NamespaceDefaultLabelName` 这一
[特性门控](/zh/docs/reference/command-line-tools-reference/feature-gates/)
被启用。标签的值是名字空间的名称。

## {{% heading "whatsnext" %}}

<!--
* Learn more about [creating a new namespace](/docs/tasks/administer-cluster/namespaces/#creating-a-new-namespace).
* Learn more about [deleting a namespace](/docs/tasks/administer-cluster/namespaces/#deleting-a-namespace).
-->
* 进一步了解[建立新的名字空间](/zh/docs/tasks/administer-cluster/namespaces/#creating-a-new-namespace)。
* 进一步了解[删除名字空间](/zh/docs/tasks/administer-cluster/namespaces/#deleting-a-namespace)。
