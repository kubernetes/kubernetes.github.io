---
title: 网络策略
content_type: concept
weight: 50
---

<!-- 
title: Network Policies
content_type: concept
weight: 50
-->

<!-- overview -->

<!--
If you want to control traffic flow at the IP address or port level (OSI layer 3 or 4), then you might consider using Kubernetes NetworkPolicies for particular applications in your cluster.  NetworkPolicies are an application-centric construct which allow you to specify how a {{< glossary_tooltip text="pod" term_id="pod">}} is allowed to communicate with various network "entities" (we use the word "entity" here to avoid overloading the more common terms such as "endpoints" and "services", which have specific Kubernetes connotations) over the network.
-->
如果你希望在 IP 地址或端口层面（OSI 第 3 层或第 4 层）控制网络流量，
则你可以考虑为集群中特定应用使用 Kubernetes 网络策略（NetworkPolicy）。
NetworkPolicy 是一种以应用为中心的结构，允许你设置如何允许
{{< glossary_tooltip text="Pod" term_id="pod">}} 与网络上的各类网络“实体”
（我们这里使用实体以避免过度使用诸如“端点”和“服务”这类常用术语，
这些术语在 Kubernetes 中有特定含义）通信。

<!--
The entities that a Pod can communicate with are identified through a combination of the following 3 identifiers:

1. Other pods that are allowed (exception: a pod cannot block access to itself)
2. Namespaces that are allowed
3. IP blocks (exception: traffic to and from the node where a Pod is running is always allowed, regardless of the IP address of the Pod or the node)
-->
Pod 可以通信的 Pod 是通过如下三个标识符的组合来辩识的：

1. 其他被允许的 Pods（例外：Pod 无法阻塞对自身的访问）
2. 被允许的名字空间
3. IP 组块（例外：与 Pod 运行所在的节点的通信总是被允许的，
   无论 Pod 或节点的 IP 地址）

<!--
When defining a pod- or namespace- based NetworkPolicy, you use a {{< glossary_tooltip text="selector" term_id="selector">}} to specify what traffic is allowed to and from the Pod(s) that match the selector.

Meanwhile, when IP based NetworkPolicies are created, we define policies based on IP blocks (CIDR ranges).
-->
在定义基于 Pod 或名字空间的 NetworkPolicy 时，你会使用 
{{< glossary_tooltip text="选择算符" term_id="selector">}} 来设定哪些流量
可以进入或离开与该算符匹配的 Pod。

同时，当基于 IP 的 NetworkPolicy 被创建时，我们基于 IP 组块（CIDR 范围）
来定义策略。

<!-- body -->

<!--
## Prerequisites

Network policies are implemented by the [network plugin](/docs/concepts/extend-kubernetes/compute-storage-net/network-plugins/). To use network policies, you must be using a networking solution which supports NetworkPolicy. Creating a NetworkPolicy resource without a controller that implements it will have no effect.
-->
## 前置条件   {#prerequisites}

网络策略通过[网络插件](/zh/docs/concepts/extend-kubernetes/compute-storage-net/network-plugins/)
来实现。要使用网络策略，你必须使用支持 NetworkPolicy 的网络解决方案。
创建一个 NetworkPolicy 资源对象而没有控制器来使它生效的话，是没有任何作用的。

<!--
## Isolated and Non-isolated Pods

By default, pods are non-isolated; they accept traffic from any source.

Pods become isolated by having a NetworkPolicy that selects them. Once there is any NetworkPolicy in a namespace selecting a particular pod, that pod will reject any connections that are not allowed by any NetworkPolicy. (Other pods in the namespace that are not selected by any NetworkPolicy will continue to accept all traffic.)

Network policies do not conflict; they are additive. If any policy or policies select a pod, the pod is restricted to what is allowed by the union of those policies' ingress/egress rules. Thus, order of evaluation does not affect the policy result.

For a network flow between two pods to be allowed, both the egress policy on the source pod and the ingress policy on the destination pod need to allow the traffic. If either the egress policy on the source, or the ingress policy on the destination denies the traffic, the traffic will be denied.
-->
## 隔离和非隔离的 Pod   {#isolated-and-non-isolated-pods}

默认情况下，Pod 是非隔离的，它们接受任何来源的流量。

Pod 在被某 NetworkPolicy 选中时进入被隔离状态。
一旦名字空间中有 NetworkPolicy 选择了特定的 Pod，该 Pod 会拒绝该 NetworkPolicy
所不允许的连接。 
（名字空间下其他未被 NetworkPolicy 所选择的 Pod 会继续接受所有的流量）

网络策略不会冲突，它们是累积的。
如果任何一个或多个策略选择了一个 Pod, 则该 Pod 受限于这些策略的
入站（Ingress）/出站（Egress）规则的并集。因此评估的顺序并不会影响策略的结果。

为了允许两个 Pods 之间的网络数据流，源端 Pod 上的出站（Egress）规则和
目标端 Pod 上的入站（Ingress）规则都需要允许该流量。
如果源端的出站（Egress）规则或目标端的入站（Ingress）规则拒绝该流量，
则流量将被拒绝。

<!--
## The NetworkPolicy resource {#networkpolicy-resource}

See the [NetworkPolicy](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#networkpolicy-v1-networking-k8s-io) reference for a full definition of the resource.

An example NetworkPolicy might look like this:
-->
## NetworkPolicy 资源 {#networkpolicy-resource}

参阅 [NetworkPolicy](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#networkpolicy-v1-networking-k8s-io)
来了解资源的完整定义。

下面是一个 NetworkPolicy 的示例:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: test-network-policy
  namespace: default
spec:
  podSelector:
    matchLabels:
      role: db
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - ipBlock:
        cidr: 172.17.0.0/16
        except:
        - 172.17.1.0/24
    - namespaceSelector:
        matchLabels:
          project: myproject
    - podSelector:
        matchLabels:
          role: frontend
    ports:
    - protocol: TCP
      port: 6379
  egress:
  - to:
    - ipBlock:
        cidr: 10.0.0.0/24
    ports:
    - protocol: TCP
      port: 5978
```

<!-- 
POSTing this to the API server for your cluster will have no effect unless your chosen networking solution supports network policy.
 -->
{{< note >}}
除非选择支持网络策略的网络解决方案，否则将上述示例发送到API服务器没有任何效果。
{{< /note >}}

<!--
__Mandatory Fields__: As with all other Kubernetes config, a NetworkPolicy
needs `apiVersion`, `kind`, and `metadata` fields.  For general information
about working with config files, see
[Configure Containers Using a ConfigMap](/docs/tasks/configure-pod-container/configure-pod-configmap/),
and [Object Management](/docs/concepts/overview/working-with-objects/object-management).

__spec__: NetworkPolicy [spec](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md#spec-and-status) has all the information needed to define a particular network policy in the given namespace.

__podSelector__: Each NetworkPolicy includes a `podSelector` which selects the grouping of pods to which the policy applies. The example policy selects pods with the label "role=db". An empty `podSelector` selects all pods in the namespace.
-->
__必需字段__：与所有其他的 Kubernetes 配置一样，NetworkPolicy 需要 `apiVersion`、
`kind` 和 `metadata` 字段。关于配置文件操作的一般信息，请参考
[使用 ConfigMap 配置容器](/zh/docs/tasks/configure-pod-container/configure-pod-configmap/),
和[对象管理](/zh/docs/concepts/overview/working-with-objects/object-management)。

__spec__：NetworkPolicy [规约](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md#spec-and-status)
中包含了在一个名字空间中定义特定网络策略所需的所有信息。

__podSelector__：每个 NetworkPolicy 都包括一个 `podSelector`，它对该策略所
适用的一组 Pod 进行选择。示例中的策略选择带有 "role=db" 标签的 Pod。
空的 `podSelector` 选择名字空间下的所有 Pod。

<!--
__policyTypes__: Each NetworkPolicy includes a `policyTypes` list which may include either `Ingress`, `Egress`, or both. The `policyTypes` field indicates whether or not the given policy applies to ingress traffic to selected pod, egress traffic from selected pods, or both. If no `policyTypes` are specified on a NetworkPolicy then by default `Ingress` will always be set and `Egress` will be set if the NetworkPolicy has any egress rules.

__ingress__: Each NetworkPolicy may include a list of allowed `ingress` rules.  Each rule allows traffic which matches both the `from` and `ports` sections. The example policy contains a single rule, which matches traffic on a single port, from one of three sources, the first specified via an `ipBlock`, the second via a `namespaceSelector` and the third via a `podSelector`.

__egress__: Each NetworkPolicy may include a list of allowed `egress` rules.  Each rule allows traffic which matches both the `to` and `ports` sections. The example policy contains a single rule, which matches traffic on a single port to any destination in `10.0.0.0/24`.
-->

__policyTypes__: 每个 NetworkPolicy 都包含一个 `policyTypes` 列表，其中包含
`Ingress` 或 `Egress` 或两者兼具。`policyTypes` 字段表示给定的策略是应用于
进入所选 Pod 的入站流量还是来自所选 Pod 的出站流量，或两者兼有。
如果 NetworkPolicy 未指定 `policyTypes` 则默认情况下始终设置 `Ingress`；
如果 NetworkPolicy 有任何出口规则的话则设置 `Egress`。

__ingress__: 每个 NetworkPolicy 可包含一个 `ingress` 规则的白名单列表。
每个规则都允许同时匹配 `from` 和 `ports` 部分的流量。示例策略中包含一条
简单的规则： 它匹配某个特定端口，来自三个来源中的一个，第一个通过 `ipBlock`
指定，第二个通过 `namespaceSelector` 指定，第三个通过 `podSelector` 指定。

__egress__: 每个 NetworkPolicy 可包含一个 `egress` 规则的白名单列表。
每个规则都允许匹配 `to` 和 `port` 部分的流量。该示例策略包含一条规则，
该规则将指定端口上的流量匹配到 `10.0.0.0/24` 中的任何目的地。

<!--
So, the example NetworkPolicy:

1. isolates "role=db" pods in the "default" namespace for both ingress and egress traffic (if they weren't already isolated)
2. (Ingress rules) allows connections to all pods in the “default” namespace with the label “role=db” on TCP port 6379 from:

   * any pod in the "default" namespace with the label "role=frontend"
   * any pod in a namespace with the label "project=myproject"
   * IP addresses in the ranges 172.17.0.0–172.17.0.255 and 172.17.2.0–172.17.255.255 (ie, all of 172.17.0.0/16 except 172.17.1.0/24)
3. (Egress rules) allows connections from any pod in the "default" namespace with the label "role=db" to CIDR 10.0.0.0/24 on TCP port 5978

See the [Declare Network Policy](/docs/tasks/administer-cluster/declare-network-policy/) walkthrough for further examples.
-->
所以，该网络策略示例:

1. 隔离 "default" 名字空间下 "role=db" 的 Pod （如果它们不是已经被隔离的话）。
2. （Ingress 规则）允许以下 Pod 连接到 "default" 名字空间下的带有 "role=db"
   标签的所有 Pod 的 6379 TCP 端口：

   * "default" 名字空间下带有 "role=frontend" 标签的所有 Pod
   * 带有 "project=myproject" 标签的所有名字空间中的 Pod
   * IP 地址范围为 172.17.0.0–172.17.0.255 和 172.17.2.0–172.17.255.255
     （即，除了 172.17.1.0/24 之外的所有 172.17.0.0/16）

3. （Egress 规则）允许从带有 "role=db" 标签的名字空间下的任何 Pod 到 CIDR
   10.0.0.0/24 下 5978 TCP 端口的连接。

参阅[声明网络策略](/zh/docs/tasks/administer-cluster/declare-network-policy/)演练
了解更多示例。

<!--
## Behavior of `to` and `from` selectors

There are four kinds of selectors that can be specified in an `ingress` `from` section or `egress` `to` section:

__podSelector__: This selects particular Pods in the same namespace as the NetworkPolicy which should be allowed as ingress sources or egress destinations.

__namespaceSelector__: This selects particular namespaces for which all Pods should be allowed as ingress sources or egress destinations.

__namespaceSelector__ *and* __podSelector__: A single `to`/`from` entry that specifies both `namespaceSelector` and `podSelector` selects particular Pods within particular namespaces. Be careful to use correct YAML syntax; this policy:
-->
## 选择器 `to` 和 `from` 的行为   {#behavior-of-to-and-from-selectors}

可以在 `ingress` 的 `from` 部分或 `egress` 的 `to` 部分中指定四种选择器：

__podSelector__: 此选择器将在与 NetworkPolicy 相同的名字空间中选择特定的
Pod，应将其允许作为入站流量来源或出站流量目的地。

__namespaceSelector__：此选择器将选择特定的名字空间，应将所有 Pod 用作其
入站流量来源或出站流量目的地。

__namespaceSelector__ *和* __podSelector__： 一个指定 `namespaceSelector`
和 `podSelector` 的 `to`/`from` 条目选择特定名字空间中的特定 Pod。
注意使用正确的 YAML 语法；下面的策略：

```yaml
  ...
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          user: alice
      podSelector:
        matchLabels:
          role: client
  ...
```

<!-- 
contains a single `from` element allowing connections from Pods with the label `role=client` in namespaces with the label `user=alice`. But *this* policy:
 -->
在 `from` 数组中仅包含一个元素，只允许来自标有 `role=client` 的 Pod 且
该 Pod 所在的名字空间中标有 `user=alice` 的连接。但是 *这项* 策略：

```yaml
  ...
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          user: alice
    - podSelector:
        matchLabels:
          role: client
  ...
```

<!--
contains two elements in the `from` array, and allows connections from Pods in the local Namespace with the label `role=client`, *or* from any Pod in any namespace with the label `user=alice`.
-->
在 `from` 数组中包含两个元素，允许来自本地名字空间中标有 `role=client` 的
Pod 的连接，*或* 来自任何标有 `user=alice`的名字空间中的任何 Pod 的连接。

<!--
When in doubt, use `kubectl describe` to see how Kubernetes has interpreted the policy.

__ipBlock__: This selects particular IP CIDR ranges to allow as ingress sources or egress destinations. These should be cluster-external IPs, since Pod IPs are ephemeral and unpredictable.

Cluster ingress and egress mechanisms often require rewriting the source or destination IP
of packets. In cases where this happens, it is not defined whether this happens before or
after NetworkPolicy processing, and the behavior may be different for different
combinations of network plugin, cloud provider, `Service` implementation, etc.

In the case of ingress, this means that in some cases you may be able to filter incoming
packets based on the actual original source IP, while in other cases, the "source IP" that
the NetworkPolicy acts on may be the IP of a `LoadBalancer` or of the Pod's node, etc.

For egress, this means that connections from pods to `Service` IPs that get rewritten to
cluster-external IPs may or may not be subject to `ipBlock`-based policies.
-->
如有疑问，请使用 `kubectl describe` 查看 Kubernetes 如何解释该策略。

__ipBlock__: 此选择器将选择特定的 IP CIDR 范围以用作入站流量来源或出站流量目的地。
这些应该是集群外部 IP，因为 Pod IP 存在时间短暂的且随机产生。

集群的入站和出站机制通常需要重写数据包的源 IP 或目标 IP。
在发生这种情况时，不确定在 NetworkPolicy 处理之前还是之后发生，
并且对于网络插件、云提供商、`Service` 实现等的不同组合，其行为可能会有所不同。

对入站流量而言，这意味着在某些情况下，你可以根据实际的原始源 IP 过滤传入的数据包，
而在其他情况下，NetworkPolicy 所作用的 `源IP` 则可能是 `LoadBalancer` 或
Pod 的节点等。

对于出站流量而言，这意味着从 Pod 到被重写为集群外部 IP 的 `Service` IP
的连接可能会或可能不会受到基于 `ipBlock` 的策略的约束。

<!--
## Default policies

By default, if no policies exist in a namespace, then all ingress and egress traffic is allowed to and from pods in that namespace. The following examples let you change the default behavior
in that namespace.
-->
## 默认策略   {#default-policies}

默认情况下，如果名字空间中不存在任何策略，则所有进出该名字空间中 Pod 的流量都被允许。
以下示例使你可以更改该名字空间中的默认行为。

<!--
### Default deny all ingress traffic

You can create a "default" isolation policy for a namespace by creating a NetworkPolicy that selects all pods but does not allow any ingress traffic to those pods.
-->
### 默认拒绝所有入站流量

你可以通过创建选择所有容器但不允许任何进入这些容器的入站流量的 NetworkPolicy 
来为名字空间创建 "default" 隔离策略。

{{< codenew file="service/networking/network-policy-default-deny-ingress.yaml" >}}

<!--
This ensures that even pods that aren't selected by any other NetworkPolicy will still be isolated. This policy does not change the default egress isolation behavior.
-->
这样可以确保即使容器没有选择其他任何 NetworkPolicy，也仍然可以被隔离。
此策略不会更改默认的出口隔离行为。

<!--
### Default allow all ingress traffic

If you want to allow all traffic to all pods in a namespace (even if policies are added that cause some pods to be treated as "isolated"), you can create a policy that explicitly allows all traffic in that namespace.
-->
### 默认允许所有入站流量

如果要允许所有流量进入某个名字空间中的所有 Pod（即使添加了导致某些 Pod 被视为
“隔离”的策略），则可以创建一个策略来明确允许该名字空间中的所有流量。

{{< codenew file="service/networking/network-policy-allow-all-ingress.yaml" >}}

<!--
### Default deny all egress traffic

You can create a "default" egress isolation policy for a namespace by creating a NetworkPolicy that selects all pods but does not allow any egress traffic from those pods.
-->
### 默认拒绝所有出站流量

你可以通过创建选择所有容器但不允许来自这些容器的任何出站流量的 NetworkPolicy 
来为名字空间创建 "default" egress 隔离策略。

{{< codenew file="service/networking/network-policy-default-deny-egress.yaml" >}}

<!--
This ensures that even pods that aren't selected by any other NetworkPolicy will not be allowed egress traffic. This policy does not
change the default ingress isolation behavior.
-->
此策略可以确保即使没有被其他任何 NetworkPolicy 选择的 Pod 也不会被允许流出流量。
此策略不会更改默认的入站流量隔离行为。

<!--
### Default allow all egress traffic

If you want to allow all traffic from all pods in a namespace (even if policies are added that cause some pods to be treated as "isolated"), you can create a policy that explicitly allows all egress traffic in that namespace.
-->
### 默认允许所有出站流量

如果要允许来自名字空间中所有 Pod 的所有流量（即使添加了导致某些 Pod 被视为“隔离”的策略），
则可以创建一个策略，该策略明确允许该名字空间中的所有出站流量。

{{< codenew file="service/networking/network-policy-allow-all-egress.yaml" >}}

<!--
### Default deny all ingress and all egress traffic

You can create a "default" policy for a namespace which prevents all ingress AND egress traffic by creating the following NetworkPolicy in that namespace.
-->
### 默认拒绝所有入口和所有出站流量

你可以为名字空间创建“默认”策略，以通过在该名字空间中创建以下 NetworkPolicy
来阻止所有入站和出站流量。

{{< codenew file="service/networking/network-policy-default-deny-all.yaml" >}}

<!--
This ensures that even pods that aren't selected by any other NetworkPolicy will not be allowed ingress or egress traffic.
-->
此策略可以确保即使没有被其他任何 NetworkPolicy 选择的 Pod 也不会被
允许入站或出站流量。

<!--
## SCTP support
-->
## SCTP 支持

{{< feature-state for_k8s_version="v1.19" state="beta" >}}

<!--
As a beta feature, this is enabled by default. To disable SCTP at a cluster level, you (or your cluster administrator) will need to disable the `SCTPSupport` [feature gate](/docs/reference/command-line-tools-reference/feature-gates/) for the API server with `-feature-gates=SCTPSupport=false,...`.
When the feature gate is enabled, you can set the `protocol` field of a NetworkPolicy to `SCTP`.
-->
作为一个 Beta 特性，SCTP 支持默认是被启用的。
要在集群层面禁用 SCTP，你（或你的集群管理员）需要为 API 服务器指定
`--feature-gates=SCTPSupport=false,...`
来禁用 `SCTPSupport` [特性门控](/zh/docs/reference/command-line-tools-reference/feature-gates/)。
启用该特性门控后，用户可以将 NetworkPolicy 的 `protocol` 字段设置为 `SCTP`。

{{< note >}}
<!-- 
You must be using a {{< glossary_tooltip text="CNI" term_id="cni" >}} plugin that supports SCTP protocol NetworkPolicies.
 -->
你必须使用支持 SCTP 协议网络策略的 {{< glossary_tooltip text="CNI" term_id="cni" >}} 插件。
{{< /note >}}

<!--
## Targeting a range of Ports
-->
## 针对某个端口范围   {#targeting-a-range-of-ports}

{{< feature-state for_k8s_version="v1.21" state="alpha" >}}

<!--
When writing a NetworkPolicy, you can target a range of ports instead of a single port.

This is achievable with the usage of the `endPort` field, as the following example:
-->
在编写 NetworkPolicy 时，你可以针对一个端口范围而不是某个固定端口。

这一目的可以通过使用 `endPort` 字段来实现，如下例所示：

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: multi-port-egress
  namespace: default
spec:
  podSelector:
    matchLabels:
      role: db
  policyTypes:
  - Egress
  egress:
  - to:
    - ipBlock:
        cidr: 10.0.0.0/24
    ports:
    - protocol: TCP
      port: 32000
      endPort: 32768
```

<!--
The above rule allows any Pod with label `db` on the namespace `default` to communicate with any IP within the range `10.0.0.0/24` over TCP, provided that the target port is between the range 32000 and 32768.
-->
上面的规则允许名字空间 `default` 中所有带有标签 `db` 的 Pod 使用 TCP 协议
与 `10.0.0.0/24` 范围内的 IP 通信，只要目标端口介于 32000 和 32768 之间就可以。

<!--
The following restrictions apply when using this field:
* As an alpha feature, this is disabled by default. To enable the `endPort` field at a cluster level, you (or your cluster administrator) need to enable the `NetworkPolicyEndPort` [feature gate](/docs/reference/command-line-tools-reference/feature-gates/) for the API server with `-feature-gates=NetworkPolicyEndPort=true,…`.
* The `endPort` field must be equal than or greater to the `port` field.
* `endPort` can only be defined if `port` is also defined.
* Both ports must be numeric.
-->
使用此字段时存在以下限制：

* 作为一种 Alpha 阶段的特性，端口范围设定默认是被禁用的。要在整个集群
  范围内允许使用 `endPort` 字段，你（或者你的集群管理员）需要为 API
  服务器设置 `-feature-gates=NetworkPolicyEndPort=true,...` 以启用
  `NetworkPolicyEndPort` 
  [特性门控](/zh/docs/reference/command-line-tools-reference/feature-gates/)。
* `endPort` 字段必须等于或者大于 `port` 字段的值。
* 两个字段的设置值都只能是数字。

{{< note >}}
<!--
Your cluster must be using a {{< glossary_tooltip text="CNI" term_id="cni" >}} plugin that
supports the `endPort` field in NetworkPolicy specifications.
-->
你的集群所使用的 {{< glossary_tooltip text="CNI" term_id="cni" >}} 插件
必须支持在 NetworkPolicy 规约中使用 `endPort` 字段。
{{< /note >}}

<!--
## Targeting a Namespace by its name
-->
## 基于名字指向某名字空间   {#targeting-a-namespace-by-its-name}

{{< feature-state state="beta" for_k8s_version="1.21" >}}

<!--
The Kubernetes control plane sets an immutable label `kubernetes.io/metadata.name` on all
namespaces, provided that the `NamespaceDefaultLabelName`
[feature gate](/docs/reference/command-line-tools-reference/feature-gates/) is enabled.
The value of the label is the namespace name.

While NetworkPolicy cannot target a namespace by its name with some object field, you can use the
standardized label to target a specific namespace.
-->
只要 `NamespaceDefaultLabelName`
[特性门控](/zh/docs/reference/command-line-tools-reference/feature-gates/)
被启用，Kubernetes 控制面会在所有名字空间上设置一个不可变更的标签
`kubernetes.io/metadata.name`。该标签的值是名字空间的名称。

如果 NetworkPolicy 无法在某些对象字段中指向某名字空间，你可以使用标准的
标签方式来指向特定名字空间。

<!--
## What you can't do with network policies (at least, not yet)

As of Kubernetes {{< skew latestVersion >}}, the following functionality does not exist in the NetworkPolicy API, but you might be able to implement workarounds using Operating System components (such as SELinux, OpenVSwitch, IPTables, and so on) or Layer 7 technologies (Ingress controllers, Service Mesh implementations) or admission controllers.  In case you are new to network security in Kubernetes, its worth noting that the following User Stories cannot (yet) be implemented using the NetworkPolicy API.
-->
## 通过网络策略（至少目前还）无法完成的工作

到 Kubernetes {{< skew latestVersion >}} 为止，NetworkPolicy API 还不支持以下功能，不过
你可能可以使用操作系统组件（如 SELinux、OpenVSwitch、IPTables 等等）
或者第七层技术（Ingress 控制器、服务网格实现）或准入控制器来实现一些
替代方案。
如果你对 Kubernetes 中的网络安全性还不太了解，了解使用 NetworkPolicy API
还无法实现下面的用户场景是很值得的。

<!--
- Forcing internal cluster traffic to go through a common gateway (this might be best served with a service mesh or other proxy).
- Anything TLS related (use a service mesh or ingress controller for this).
- Node specific policies (you can use CIDR notation for these, but you cannot target nodes by their Kubernetes identities specifically).
- Targeting of services by name (you can, however, target pods or namespaces by their {{< glossary_tooltip text="labels" term_id="label" >}}, which is often a viable workaround).
- Creation or management of "Policy requests" that are fulfilled by a third party.
-->
- 强制集群内部流量经过某公用网关（这种场景最好通过服务网格或其他代理来实现）；
- 与 TLS 相关的场景（考虑使用服务网格或者 Ingress 控制器）；
- 特定于节点的策略（你可以使用 CIDR 来表达这一需求不过你无法使用节点在
  Kubernetes 中的其他标识信息来辩识目标节点）；
- 基于名字来选择服务（不过，你可以使用 {{< glossary_tooltip text="标签" term_id="label" >}}
  来选择目标 Pod 或名字空间，这也通常是一种可靠的替代方案）；
- 创建或管理由第三方来实际完成的“策略请求”；
<!--
- Default policies which are applied to all namespaces or pods (there are some third party Kubernetes distributions and projects which can do this).
- Advanced policy querying and reachability tooling.
- The ability to log network security events (for example connections that are blocked or accepted).
- The ability to explicitly deny policies (currently the model for NetworkPolicies are deny by default, with only the ability to add allow rules).
- The ability to prevent loopback or incoming host traffic (Pods cannot currently block localhost access, nor do they have the ability to block access from their resident node).
-->
- 实现适用于所有名字空间或 Pods 的默认策略（某些第三方 Kubernetes 发行版本
  或项目可以做到这点）；
- 高级的策略查询或者可达性相关工具；
- 生成网络安全事件日志的能力（例如，被阻塞或接收的连接请求）；
- 显式地拒绝策略的能力（目前，NetworkPolicy 的模型默认采用拒绝操作，
  其唯一的能力是添加允许策略）；
- 禁止本地回路或指向宿主的网络流量（Pod 目前无法阻塞 localhost 访问，
  它们也无法禁止来自所在节点的访问请求）。

## {{% heading "whatsnext" %}}

<!--
- See the [Declare Network Policy](/docs/tasks/administer-cluster/declare-network-policy/)
  walkthrough for further examples.
- See more [recipes](https://github.com/ahmetb/kubernetes-network-policy-recipes) for common scenarios enabled by the NetworkPolicy resource.
-->
- 参阅[声明网络策略](/zh/docs/tasks/administer-cluster/declare-network-policy/)
  演练了解更多示例；
- 有关 NetworkPolicy 资源所支持的常见场景的更多信息，请参见
  [此指南](https://github.com/ahmetb/kubernetes-network-policy-recipes)。

