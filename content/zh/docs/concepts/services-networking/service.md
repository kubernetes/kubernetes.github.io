---
title: 服务
feature:
  title: 服务发现与负载均衡
  description: >
    无需修改你的应用程序即可使用陌生的服务发现机制。Kubernetes 为容器提供了自己的 IP 地址和一个 DNS 名称，并且可以在它们之间实现负载均衡。

content_type: concept
weight: 10
---

<!--
title: Service
feature:
  title: Service discovery and load balancing
  description: >
    No need to modify your application to use an unfamiliar service discovery mechanism. Kubernetes gives Pods their own IP addresses and a single DNS name for a set of Pods, and can load-balance across them.

content_type: concept
weight: 10
-->

<!-- overview -->

{{< glossary_definition term_id="service" length="short" >}}

<!--
With Kubernetes you don't need to modify your application to use an unfamiliar service discovery mechanism.
Kubernetes gives Pods their own IP addresses and a single DNS name for a set of Pods,
and can load-balance across them.
-->
使用 Kubernetes，你无需修改应用程序即可使用不熟悉的服务发现机制。
Kubernetes 为 Pods 提供自己的 IP 地址，并为一组 Pod 提供相同的 DNS 名，
并且可以在它们之间进行负载均衡。

<!-- body -->

<!--
## Motivation

Kubernetes {{< glossary_tooltip term_id="pod" text="Pods" >}} are created and destroyed
to match the state of your cluster. Pods are nonpermanent resources.
If you use a {{< glossary_tooltip term_id="deployment" >}} to run your app,
it can create and destroy Pods dynamically.

Each Pod gets its own IP address, however in a Deployment, the set of Pods
running in one moment in time could be different from
the set of Pods running that application a moment later.

This leads to a problem: if some set of Pods (call them "backends") provides
functionality to other Pods (call them "frontends") inside your cluster,
how do the frontends find out and keep track of which IP address to connect
to, so that the frontend can use the backend part of the workload?

Enter _Services_.
-->

## 动机

创建和销毁 Kubernetes {{< glossary_tooltip term_id="pod" text="Pod" >}} 以匹配集群状态。
Pod 是非永久性资源。
如果你使用 {{< glossary_tooltip term_id="deployment">}}
来运行你的应用程序，则它可以动态创建和销毁 Pod。

每个 Pod 都有自己的 IP 地址，但是在 Deployment 中，在同一时刻运行的 Pod 集合可能与稍后运行该应用程序的 Pod 集合不同。

这导致了一个问题： 如果一组 Pod（称为“后端”）为集群内的其他 Pod（称为“前端”）提供功能，
那么前端如何找出并跟踪要连接的 IP 地址，以便前端可以使用提供工作负载的后端部分？

进入 _Services_。

<!--
## Service resources {#service-resource}
-->
## Service 资源 {#service-resource}

<!--
In Kubernetes, a Service is an abstraction which defines a logical set of Pods
and a policy by which to access them (sometimes this pattern is called
a micro-service). The set of Pods targeted by a Service is usually determined
by a {{< glossary_tooltip text="selector" term_id="selector" >}}.
To learn about other ways to define Service endpoints,
see [Services _without_ selectors](#services-without-selectors).
-->
Kubernetes Service 定义了这样一种抽象：逻辑上的一组 Pod，一种可以访问它们的策略 —— 通常称为微服务。
Service 所针对的 Pods 集合通常是通过{{< glossary_tooltip text="选择算符" term_id="selector" >}}来确定的。
要了解定义服务端点的其他方法，请参阅[不带选择算符的服务](#services-without-selectors)。

<!--
For example, consider a stateless image-processing backend which is running with
3 replicas.  Those replicas are fungible&mdash;frontends do not care which backend
they use.  While the actual Pods that compose the backend set may change, the
frontend clients should not need to be aware of that, nor should they need to keep
track of the set of backends themselves.

The Service abstraction enables this decoupling.
-->
举个例子，考虑一个图片处理后端，它运行了 3 个副本。这些副本是可互换的 ——
前端不需要关心它们调用了哪个后端副本。
然而组成这一组后端程序的 Pod 实际上可能会发生变化，
前端客户端不应该也没必要知道，而且也不需要跟踪这一组后端的状态。

Service 定义的抽象能够解耦这种关联。

<!--
### Cloud-native service discovery

If you're able to use Kubernetes APIs for service discovery in your application,
you can query the {{< glossary_tooltip text="API server" term_id="kube-apiserver" >}}
for Endpoints, that get updated whenever the set of Pods in a Service changes.

For non-native applications, Kubernetes offers ways to place a network port or load
balancer in between your application and the backend Pods.
-->
### 云原生服务发现

如果你想要在应用程序中使用 Kubernetes API 进行服务发现，则可以查询
{{< glossary_tooltip text="API 服务器" term_id="kube-apiserver" >}}
的 Endpoints 资源，只要服务中的 Pod 集合发生更改，Endpoints 就会被更新。

对于非本机应用程序，Kubernetes 提供了在应用程序和后端 Pod 之间放置网络端口或负载均衡器的方法。

<!--
## Defining a Service

A Service in Kubernetes is a REST object, similar to a Pod.  Like all of the
REST objects, you can `POST` a Service definition to the API server to create
a new instance.
The name of a Service object must be a valid
[DNS label name](/docs/concepts/overview/working-with-objects/names#dns-label-names).

For example, suppose you have a set of Pods where each listens on TCP port 9376
and contains a label `app=MyApp`:
-->

## 定义 Service

Service 在 Kubernetes 中是一个 REST 对象，和 Pod 类似。
像所有的 REST 对象一样，Service 定义可以基于 `POST` 方式，请求 API server 创建新的实例。
Service 对象的名称必须是合法的
[DNS 标签名称](/zh/docs/concepts/overview/working-with-objects/names#dns-label-names)。

例如，假定有一组 Pod，它们对外暴露了 9376 端口，同时还被打上 `app=MyApp` 标签：

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  selector:
    app: MyApp
  ports:
    - protocol: TCP
      port: 80
      targetPort: 9376
```

<!--
This specification creates a new Service object named “my-service”, which
targets TCP port 9376 on any Pod with the `app=MyApp` label.

Kubernetes assigns this Service an IP address (sometimes called the "cluster IP"),
which is used by the Service proxies
(see [Virtual IPs and service proxies](#virtual-ips-and-service-proxies) below).

The controller for the Service selector continuously scans for Pods that
match its selector, and then POSTs any updates to an Endpoint object
also named "my-service".
-->
上述配置创建一个名称为 "my-service" 的 Service 对象，它会将请求代理到使用
TCP 端口 9376，并且具有标签 `"app=MyApp"` 的 Pod 上。

Kubernetes 为该服务分配一个 IP 地址（有时称为 "集群IP"），该 IP 地址由服务代理使用。
(请参见下面的 [VIP 和 Service 代理](#virtual-ips-and-service-proxies)).

服务选择算符的控制器不断扫描与其选择器匹配的 Pod，然后将所有更新发布到也称为
“my-service” 的 Endpoint 对象。

<!--
A Service can map _any_ incoming `port` to a `targetPort`. By default and
for convenience, the `targetPort` is set to the same value as the `port`
field.
-->
{{< note >}}
需要注意的是，Service 能够将一个接收 `port` 映射到任意的 `targetPort`。
默认情况下，`targetPort` 将被设置为与 `port` 字段相同的值。
{{< /note >}}

<!--
Port definitions in Pods have names, and you can reference these names in the
`targetPort` attribute of a Service. This works even if there is a mixture
of Pods in the Service using a single configured name, with the same network
protocol available via different port numbers.
This offers a lot of flexibility for deploying and evolving your Services.
For example, you can change the port numbers that Pods expose in the next
version of your backend software, without breaking clients.

The default protocol for Services is TCP; you can also use any other
[supported protocol](#protocol-support).

As many Services need to expose more than one port, Kubernetes supports multiple
port definitions on a Service object.
Each port definition can have the same `protocol`, or a different one.
-->
Pod 中的端口定义是有名字的，你可以在服务的 `targetPort` 属性中引用这些名称。
即使服务中使用单个配置的名称混合使用 Pod，并且通过不同的端口号提供相同的网络协议，此功能也可以使用。
这为部署和发展服务提供了很大的灵活性。
例如，你可以更改 Pods 在新版本的后端软件中公开的端口号，而不会破坏客户端。

服务的默认协议是 TCP；你还可以使用任何其他[受支持的协议](#protocol-support)。

由于许多服务需要公开多个端口，因此 Kubernetes 在服务对象上支持多个端口定义。
每个端口定义可以具有相同的 `protocol`，也可以具有不同的协议。

<!--
### Services without selectors

Services most commonly abstract access to Kubernetes Pods, but they can also
abstract other kinds of backends.
For example:

  * You want to have an external database cluster in production, but in your
    test environment you use your own databases.
  * You want to point your Service to a Service in a different
    {{< glossary_tooltip term_id="namespace" >}} or on another cluster.
* You are migrating a workload to Kubernetes. While evaluating the approach,
    you run only a portion of your backends in Kubernetes.

In any of these scenarios you can define a Service _without_ a Pod selector.
For example:
-->
### 没有选择算符的 Service   {#services-without-selectors}

服务最常见的是抽象化对 Kubernetes Pod 的访问，但是它们也可以抽象化其他种类的后端。
实例:

  * 希望在生产环境中使用外部的数据库集群，但测试环境使用自己的数据库。
  * 希望服务指向另一个 {{< glossary_tooltip term_id="namespace" >}} 中或其它集群中的服务。
  * 你正在将工作负载迁移到 Kubernetes。 在评估该方法时，你仅在 Kubernetes 中运行一部分后端。

在任何这些场景中，都能够定义没有选择算符的 Service。
实例:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  ports:
    - protocol: TCP
      port: 80
      targetPort: 9376
```

<!--
Because this Service has no selector, the corresponding Endpoints object is not
created automatically. You can manually map the Service to the network address and port
where it's running, by adding an Endpoints object manually:
-->
由于此服务没有选择算符，因此不会自动创建相应的 Endpoint 对象。
你可以通过手动添加 Endpoint 对象，将服务手动映射到运行该服务的网络地址和端口：

```yaml
apiVersion: v1
kind: Endpoints
metadata:
  name: my-service
subsets:
  - addresses:
      - ip: 192.0.2.42
    ports:
      - port: 9376
```
<!--
The name of the Endpoints object must be a valid
[DNS subdomain name](/docs/concepts/overview/working-with-objects/names#dns-subdomain-names).
-->
Endpoints 对象的名称必须是合法的
[DNS 子域名](/zh/docs/concepts/overview/working-with-objects/names#dns-subdomain-names)。

<!--
The endpoint IPs _must not_ be: loopback (127.0.0.0/8 for IPv4, ::1/128 for IPv6), or
link-local (169.254.0.0/16 and 224.0.0.0/24 for IPv4, fe80::/64 for IPv6).

Endpoint IP addresses cannot be the cluster IPs of other Kubernetes Services,
because {{< glossary_tooltip term_id="kube-proxy" >}} doesn't support virtual IPs
as a destination.
-->
{{< note >}}
端点 IPs _必须不可以_ 是：本地回路（IPv4 的 127.0.0.0/8, IPv6 的 ::1/128）或
本地链接（IPv4 的 169.254.0.0/16 和 224.0.0.0/24，IPv6 的 fe80::/64)。

端点 IP 地址不能是其他 Kubernetes 服务的集群 IP，因为
{{< glossary_tooltip term_id ="kube-proxy">}} 不支持将虚拟 IP 作为目标。
{{< /note >}}

<!--
Accessing a Service without a selector works the same as if it had a selector.
In the example above, traffic is routed to the single endpoint defined in
the YAML: `192.0.2.42:9376` (TCP).
-->
访问没有选择算符的 Service，与有选择算符的 Service 的原理相同。
请求将被路由到用户定义的 Endpoint，YAML 中为：`192.0.2.42:9376`（TCP）。

<!--
An ExternalName Service is a special case of Service that does not have
selectors and uses DNS names instead. For more information, see the
[ExternalName](#externalname) section later in this document.
-->
ExternalName Service 是 Service 的特例，它没有选择算符，但是使用 DNS 名称。
有关更多信息，请参阅本文档后面的[ExternalName](#externalname)。

<!--
### Over Capacity Endpoints

If an Endpoints resource has more than 1000 endpoints then a Kubernetes v1.21 (or later)
cluster annotates that Endpoints with `endpoints.kubernetes.io/over-capacity: warning`.
This annotation indicates that the affected Endpoints object is over capacity.
-->
### 超出容量的 Endpoints    {#over-capacity-endpoints}

如果某个 Endpoints 资源中包含的端点个数超过 1000，则 Kubernetes v1.21 版本
（及更新版本）的集群会将为该 Endpoints 添加注解
`endpoints.kubernetes.io/over-capacity: warning`。
这一注解表明所影响到的 Endpoints 对象已经超出容量。

<!--
### EndpointSlices
-->
### EndpointSlice

{{< feature-state for_k8s_version="v1.21" state="stable" >}}

<!--
Endpoint Slices are an API resource that can provide a more scalable alternative
to Endpoints. Although conceptually quite similar to Endpoints, Endpoint Slices
allow for distributing network endpoints across multiple resources. By default,
an Endpoint Slice is considered "full" once it reaches 100 endpoints, at which
point additional Endpoint Slices will be created to store any additional
endpoints.

Endpoint Slices provide additional attributes and functionality which is
described in detail in [EndpointSlices](/docs/concepts/services-networking/endpoint-slices/).
-->
Endpoint 切片是一种 API 资源，可以为 Endpoint 提供更可扩展的替代方案。
尽管从概念上讲与 Endpoint 非常相似，但 Endpoint 切片允许跨多个资源分布网络端点。
默认情况下，一旦到达100个 Endpoint，该 Endpoint 切片将被视为“已满”，
届时将创建其他 Endpoint 切片来存储任何其他 Endpoint。

Endpoint 切片提供了附加的属性和功能，这些属性和功能在
[EndpointSlices](/zh/docs/concepts/services-networking/endpoint-slices/)
中有详细描述。

<!--
### Application protocol

{{< feature-state for_k8s_version="v1.20" state="stable" >}}
The `appProtocol` field provides a way to specify an application protocol for
each Service port. The value of this field is mirrored by the corresponding
Endpoints and EndpointSlice objects.

This field follows standard Kubernetes label syntax. Values should either be
[IANA standard service names](https://www.iana.org/assignments/service-names) or
domain prefixed names such as `mycompany.com/my-custom-protocol`.
-->
### 应用协议   {#application-protocol}

{{< feature-state for_k8s_version="v1.20" state="stable" >}}

`appProtocol` 字段提供了一种为每个 Service 端口指定应用协议的方式。
此字段的取值会被映射到对应的 Endpoints 和 EndpointSlices 对象。

该字段遵循标准的 Kubernetes 标签语法。
其值可以是 [IANA 标准服务名称](https://www.iana.org/assignments/service-names)
或以域名为前缀的名称，如 `mycompany.com/my-custom-protocol`。
<!--
## Virtual IPs and service proxies

Every node in a Kubernetes cluster runs a `kube-proxy`. `kube-proxy` is
responsible for implementing a form of virtual IP for `Services` of type other
than [`ExternalName`](#externalname).
-->
## 虚拟 IP 和 Service 代理 {#virtual-ips-and-service-proxies}

在 Kubernetes 集群中，每个 Node 运行一个 `kube-proxy` 进程。
`kube-proxy` 负责为 Service 实现了一种 VIP（虚拟 IP）的形式，而不是
[`ExternalName`](#externalname) 的形式。

<!--
### Why not use round-robin DNS?

A question that pops up every now and then is why Kubernetes relies on
proxying to forward inbound traffic to backends. What about other
approaches? For example, would it be possible to configure DNS records that
have multiple A values (or AAAA for IPv6), and rely on round-robin name
resolution?

There are a few reasons for using proxying for Services:

 * There is a long history of DNS implementations not respecting record TTLs,
   and caching the results of name lookups after they should have expired.
 * Some apps do DNS lookups only once and cache the results indefinitely.
 * Even if apps and libraries did proper re-resolution, the low or zero TTLs
   on the DNS records could impose a high load on DNS that then becomes
   difficult to manage.
-->
### 为什么不使用 DNS 轮询？

时不时会有人问到为什么 Kubernetes 依赖代理将入站流量转发到后端。那其他方法呢？
例如，是否可以配置具有多个 A 值（或 IPv6 为 AAAA）的 DNS 记录，并依靠轮询名称解析？

使用服务代理有以下几个原因：

* DNS 实现的历史由来已久，它不遵守记录 TTL，并且在名称查找结果到期后对其进行缓存。
* 有些应用程序仅执行一次 DNS 查找，并无限期地缓存结果。
* 即使应用和库进行了适当的重新解析，DNS 记录上的 TTL 值低或为零也可能会给
  DNS 带来高负载，从而使管理变得困难。

<!--
### User space proxy mode {#proxy-mode-userspace}

In this mode, kube-proxy watches the Kubernetes control plane for the addition and
removal of Service and Endpoint objects. For each Service it opens a
port (randomly chosen) on the local node.  Any connections to this "proxy port"
are proxied to one of the Service's backend Pods (as reported via
Endpoints). kube-proxy takes the `SessionAffinity` setting of the Service into
account when deciding which backend Pod to use.

Lastly, the user-space proxy installs iptables rules which capture traffic to
the Service's `clusterIP` (which is virtual) and `port`. The rules
redirect that traffic to the proxy port which proxies the backend Pod.

By default, kube-proxy in userspace mode chooses a backend via a round-robin algorithm.

![Services overview diagram for userspace proxy](/images/docs/services-userspace-overview.svg)
-->
### userspace 代理模式 {#proxy-mode-userspace}

这种模式，kube-proxy 会监视 Kubernetes 控制平面对 Service 对象和 Endpoints 对象的添加和移除操作。
对每个 Service，它会在本地 Node 上打开一个端口（随机选择）。
任何连接到“代理端口”的请求，都会被代理到 Service 的后端 `Pods` 中的某个上面（如 `Endpoints` 所报告的一样）。
使用哪个后端 Pod，是 kube-proxy 基于 `SessionAffinity` 来确定的。

最后，它配置 iptables 规则，捕获到达该 Service 的 `clusterIP`（是虚拟 IP）
和 `Port` 的请求，并重定向到代理端口，代理端口再代理请求到后端Pod。

默认情况下，用户空间模式下的 kube-proxy 通过轮转算法选择后端。

![userspace 代理模式下 Service 概览图](/images/docs/services-userspace-overview.svg)

<!--
### `iptables` proxy mode {#proxy-mode-iptables}

In this mode, kube-proxy watches the Kubernetes control plane for the addition and
removal of Service and Endpoint objects. For each Service, it installs
iptables rules, which capture traffic to the Service's `clusterIP` and `port`,
and redirect that traffic to one of the Service's
backend sets.  For each Endpoint object, it installs iptables rules which
select a backend Pod.

By default, kube-proxy in iptables mode chooses a backend at random.

Using iptables to handle traffic has a lower system overhead, because traffic
is handled by Linux netfilter without the need to switch between userspace and the
kernel space. This approach is also likely to be more reliable.

If kube-proxy is running in iptables mode and the first Pod that's selected
does not respond, the connection fails. This is different from userspace
mode: in that scenario, kube-proxy would detect that the connection to the first
Pod had failed and would automatically retry with a different backend Pod.

You can use Pod [readiness probes](/docs/concepts/workloads/pods/pod-lifecycle/#container-probes)
to verify that backend Pods are working OK, so that kube-proxy in iptables mode
only sees backends that test out as healthy. Doing this means you avoid
having traffic sent via kube-proxy to a Pod that's known to have failed.

![Services overview diagram for iptables proxy](/images/docs/services-iptables-overview.svg)
-->
### iptables 代理模式 {#proxy-mode-iptables}

这种模式，`kube-proxy` 会监视 Kubernetes 控制节点对 Service 对象和 Endpoints 对象的添加和移除。
对每个 Service，它会配置 iptables 规则，从而捕获到达该 Service 的 `clusterIP`
和端口的请求，进而将请求重定向到 Service 的一组后端中的某个 Pod 上面。
对于每个 Endpoints 对象，它也会配置 iptables 规则，这个规则会选择一个后端组合。

默认的策略是，kube-proxy 在 iptables 模式下随机选择一个后端。

使用 iptables 处理流量具有较低的系统开销，因为流量由 Linux netfilter 处理，
而无需在用户空间和内核空间之间切换。 这种方法也可能更可靠。

如果 kube-proxy 在 iptables 模式下运行，并且所选的第一个 Pod 没有响应，
则连接失败。
这与用户空间模式不同：在这种情况下，kube-proxy 将检测到与第一个 Pod 的连接已失败，
并会自动使用其他后端 Pod 重试。

你可以使用 Pod [就绪探测器](/zh/docs/concepts/workloads/pods/pod-lifecycle/#container-probes)
验证后端 Pod 可以正常工作，以便 iptables 模式下的 kube-proxy 仅看到测试正常的后端。
这样做意味着你避免将流量通过 kube-proxy 发送到已知已失败的 Pod。

![iptables代理模式下Service概览图](/images/docs/services-iptables-overview.svg)

<!--
### IPVS proxy mode {#proxy-mode-ipvs}
-->
### IPVS 代理模式 {#proxy-mode-ipvs}

{{< feature-state for_k8s_version="v1.11" state="stable" >}}

<!--
In `ipvs` mode, kube-proxy watches Kubernetes Services and Endpoints,
calls `netlink` interface to create IPVS rules accordingly and synchronizes
IPVS rules with Kubernetes Services and Endpoints periodically.
This control loop ensures that IPVS status matches the desired
state.
When accessing a Service, IPVS directs traffic to one of the backend Pods.

The IPVS proxy mode is based on netfilter hook function that is similar to
iptables mode, but uses a hash table as the underlying data structure and works
in the kernel space.
That means kube-proxy in IPVS mode redirects traffic with lower latency than
kube-proxy in iptables mode, with much better performance when synchronising
proxy rules. Compared to the other proxy modes, IPVS mode also supports a
higher throughput of network traffic.

IPVS provides more options for balancing traffic to backend Pods;
these are:
-->
在 `ipvs` 模式下，kube-proxy 监视 Kubernetes 服务和端点，调用 `netlink` 接口相应地创建 IPVS 规则，
并定期将 IPVS 规则与 Kubernetes 服务和端点同步。 该控制循环可确保IPVS
状态与所需状态匹配。访问服务时，IPVS 将流量定向到后端Pod之一。

IPVS代理模式基于类似于 iptables 模式的 netfilter 挂钩函数，
但是使用哈希表作为基础数据结构，并且在内核空间中工作。
这意味着，与 iptables 模式下的 kube-proxy 相比，IPVS 模式下的 kube-proxy
重定向通信的延迟要短，并且在同步代理规则时具有更好的性能。
与其他代理模式相比，IPVS 模式还支持更高的网络流量吞吐量。

IPVS 提供了更多选项来平衡后端 Pod 的流量。 这些是：

* `rr`：轮替（Round-Robin）
* `lc`：最少链接（Least Connection），即打开链接数量最少者优先
* `dh`：目标地址哈希（Destination Hashing）
* `sh`：源地址哈希（Source Hashing）
* `sed`：最短预期延迟（Shortest Expected Delay）
* `nq`：从不排队（Never Queue）

<!--
To run kube-proxy in IPVS mode, you must make IPVS available on
the node before starting kube-proxy.

When kube-proxy starts in IPVS proxy mode, it verifies whether IPVS
kernel modules are available. If the IPVS kernel modules are not detected, then kube-proxy
falls back to running in iptables proxy mode.
-->
{{< note >}}
要在 IPVS 模式下运行 kube-proxy，必须在启动 kube-proxy 之前使 IPVS 在节点上可用。

当 kube-proxy 以 IPVS 代理模式启动时，它将验证 IPVS 内核模块是否可用。
如果未检测到 IPVS 内核模块，则 kube-proxy 将退回到以 iptables 代理模式运行。
{{< /note >}}

<!--
![Services overview diagram for IPVS proxy](/images/docs/services-ipvs-overview.svg)

In these proxy models, the traffic bound for the Service's IP:Port is
proxied to an appropriate backend without the clients knowing anything
about Kubernetes or Services or Pods.

If you want to make sure that connections from a particular client
are passed to the same Pod each time, you can select the session affinity based
on the client's IP addresses by setting `service.spec.sessionAffinity` to "ClientIP"
(the default is "None").
You can also set the maximum session sticky time by setting
`service.spec.sessionAffinityConfig.clientIP.timeoutSeconds` appropriately.
(the default value is 10800, which works out to be 3 hours).
-->

![IPVS代理的 Services 概述图](/images/docs/services-ipvs-overview.svg)

在这些代理模型中，关于绑定到服务 IP 的流量：
在客户端不了解 Kubernetes 或服务或 Pod 的任何信息的情况下，将 Port 代理到适当的后端。

如果要确保每次都将来自特定客户端的连接传递到同一 Pod，
则可以通过将 `service.spec.sessionAffinity` 设置为 "ClientIP"
（默认值是 "None"），来基于客户端的 IP 地址选择会话关联。
你还可以通过适当设置 `service.spec.sessionAffinityConfig.clientIP.timeoutSeconds`
来设置最大会话停留时间。
（默认值为 10800 秒，即 3 小时）。

<!--
## Multi-Port Services

For some Services, you need to expose more than one port.
Kubernetes lets you configure multiple port definitions on a Service object.
When using multiple ports for a Service, you must give all of your ports names
so that these are unambiguous.
For example:
-->
## 多端口 Service   {#multi-port-services}

对于某些服务，你需要公开多个端口。
Kubernetes 允许你在 Service 对象上配置多个端口定义。
为服务使用多个端口时，必须提供所有端口名称，以使它们无歧义。
例如：

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  selector:
    app: MyApp
  ports:
    - name: http
      protocol: TCP
      port: 80
      targetPort: 9376
    - name: https
      protocol: TCP
      port: 443
      targetPort: 9377
```

<!--
As with Kubernetes {{< glossary_tooltip term_id="name" text="names">}} in general, names for ports
must only contain lowercase alphanumeric characters and `-`. Port names must
also start and end with an alphanumeric character.

For example, the names `123-abc` and `web` are valid, but `123_abc` and `-web` are not.
-->
{{< note >}}
与一般的Kubernetes名称一样，端口名称只能包含小写字母数字字符 和 `-`。
端口名称还必须以字母数字字符开头和结尾。

例如，名称 `123-abc` 和 `web` 有效，但是 `123_abc` 和 `-web` 无效。
{{< /note >}}

<!--
## Choosing your own IP address

You can specify your own cluster IP address as part of a `Service` creation
request.  To do this, set the `.spec.clusterIP` field. For example, if you
already have an existing DNS entry that you wish to reuse, or legacy systems
that are configured for a specific IP address and difficult to re-configure.

The IP address that you choose must be a valid IPv4 or IPv6 address from within the
`service-cluster-ip-range` CIDR range that is configured for the API server.
If you try to create a Service with an invalid clusterIP address value, the API
server will return a 422 HTTP status code to indicate that there's a problem.
-->
## 选择自己的 IP 地址

在 `Service` 创建的请求中，可以通过设置 `spec.clusterIP` 字段来指定自己的集群 IP 地址。
比如，希望替换一个已经已存在的 DNS 条目，或者遗留系统已经配置了一个固定的 IP 且很难重新配置。

用户选择的 IP 地址必须合法，并且这个 IP 地址在 `service-cluster-ip-range` CIDR 范围内，
这对 API 服务器来说是通过一个标识来指定的。
如果 IP 地址不合法，API 服务器会返回 HTTP 状态码 422，表示值不合法。

<!--
## Discovering services

Kubernetes supports 2 primary modes of finding a Service - environment
variables and DNS.
-->
## 服务发现  {#discovering-services}

Kubernetes 支持两种基本的服务发现模式 —— 环境变量和 DNS。

<!--
### Environment variables

When a Pod is run on a Node, the kubelet adds a set of environment variables
for each active Service.  It supports both [Docker links
compatible](https://docs.docker.com/userguide/dockerlinks/) variables (see
[makeLinkVariables](https://releases.k8s.io/{{< param "githubbranch" >}}/pkg/kubelet/envvars/envvars.go#L49))
and simpler `{SVCNAME}_SERVICE_HOST` and `{SVCNAME}_SERVICE_PORT` variables,
where the Service name is upper-cased and dashes are converted to underscores.

For example, the Service `redis-master` which exposes TCP port 6379 and has been
allocated cluster IP address 10.0.0.11, produces the following environment
variables:
-->
### 环境变量   {#environment-variables}

当 Pod 运行在 `Node` 上，kubelet 会为每个活跃的 Service 添加一组环境变量。
它同时支持 [Docker links兼容](https://docs.docker.com/userguide/dockerlinks/) 变量
（查看 [makeLinkVariables](https://releases.k8s.io/{{< param "githubbranch" >}}/pkg/kubelet/envvars/envvars.go#L49)）、
简单的 `{SVCNAME}_SERVICE_HOST` 和 `{SVCNAME}_SERVICE_PORT` 变量。
这里 Service 的名称需大写，横线被转换成下划线。

举个例子，一个名称为 `redis-master` 的 Service 暴露了 TCP 端口 6379，
同时给它分配了 Cluster IP 地址 10.0.0.11，这个 Service 生成了如下环境变量：

```shell
REDIS_MASTER_SERVICE_HOST=10.0.0.11
REDIS_MASTER_SERVICE_PORT=6379
REDIS_MASTER_PORT=tcp://10.0.0.11:6379
REDIS_MASTER_PORT_6379_TCP=tcp://10.0.0.11:6379
REDIS_MASTER_PORT_6379_TCP_PROTO=tcp
REDIS_MASTER_PORT_6379_TCP_PORT=6379
REDIS_MASTER_PORT_6379_TCP_ADDR=10.0.0.11
```

<!--
When you have a Pod that needs to access a Service, and you are using
the environment variable method to publish the port and cluster IP to the client
Pods, you must create the Service *before* the client Pods come into existence.
Otherwise, those client Pods won't have their environment variables populated.

If you only use DNS to discover the cluster IP for a Service, you don't need to
worry about this ordering issue.
-->
{{< note >}}
当你具有需要访问服务的 Pod 时，并且你正在使用环境变量方法将端口和集群 IP 发布到客户端
Pod 时，必须在客户端 Pod 出现 *之前* 创建服务。
否则，这些客户端 Pod 将不会设定其环境变量。

如果仅使用 DNS 查找服务的集群 IP，则无需担心此设定问题。
{{< /note >}}

### DNS

<!--
You can (and almost always should) set up a DNS service for your Kubernetes
cluster using an [add-on](/docs/concepts/cluster-administration/addons/).

A cluster-aware DNS server, such as CoreDNS, watches the Kubernetes API for new
Services and creates a set of DNS records for each one.  If DNS has been enabled
throughout your cluster then all Pods should automatically be able to resolve
Services by their DNS name.
-->
你可以（几乎总是应该）使用[附加组件](/zh/docs/concepts/cluster-administration/addons/)
为 Kubernetes 集群设置 DNS 服务。

支持集群的 DNS 服务器（例如 CoreDNS）监视 Kubernetes API 中的新服务，并为每个服务创建一组 DNS 记录。
如果在整个集群中都启用了 DNS，则所有 Pod 都应该能够通过其 DNS 名称自动解析服务。

<!--
For example, if you have a Service called `my-service` in a Kubernetes
namespace `my-ns`, the control plane and the DNS Service acting together
create a DNS record for `my-service.my-ns`. Pods in the `my-ns` namespace
should be able to find the service by doing a name lookup for `my-service`
(`my-service.my-ns` would also work).

Pods in other Namespaces must qualify the name as `my-service.my-ns`. These names
will resolve to the cluster IP assigned for the Service.
-->
例如，如果你在 Kubernetes 命名空间 `my-ns` 中有一个名为 `my-service` 的服务，
则控制平面和 DNS 服务共同为 `my-service.my-ns` 创建 DNS 记录。
`my-ns` 命名空间中的 Pod 应该能够通过按名检索 `my-service` 来找到服务
（`my-service.my-ns` 也可以工作）。

其他命名空间中的 Pod 必须将名称限定为 `my-service.my-ns`。
这些名称将解析为为服务分配的集群 IP。

<!--
Kubernetes also supports DNS SRV (Service) records for named ports.  If the
`my-service.my-ns` Service has a port named `http` with the protocol set to
`TCP`, you can do a DNS SRV query for `_http._tcp.my-service.my-ns` to discover
the port number for `http`, as well as the IP address.

The Kubernetes DNS server is the only way to access `ExternalName` Services.
You can find more information about `ExternalName` resolution in
[DNS Pods and Services](/docs/concepts/services-networking/dns-pod-service/).
-->
Kubernetes 还支持命名端口的 DNS SRV（服务）记录。
如果 `my-service.my-ns` 服务具有名为 `http`　的端口，且协议设置为 TCP，
则可以对 `_http._tcp.my-service.my-ns` 执行 DNS SRV 查询查询以发现该端口号,
`"http"` 以及 IP 地址。

Kubernetes DNS 服务器是唯一的一种能够访问 `ExternalName` 类型的 Service 的方式。
更多关于 `ExternalName` 信息可以查看
[DNS Pod 和 Service](/zh/docs/concepts/services-networking/dns-pod-service/)。

<!--
## Headless Services  {#headless-services}

Sometimes you don't need load-balancing and a single Service IP.  In
this case, you can create what are termed "headless" Services, by explicitly
specifying `"None"` for the cluster IP (`.spec.clusterIP`).

You can use a headless Service to interface with other service discovery mechanisms,
without being tied to Kubernetes' implementation.

For headless `Services`, a cluster IP is not allocated, kube-proxy does not handle
these Services, and there is no load balancing or proxying done by the platform
for them. How DNS is automatically configured depends on whether the Service has
selectors defined:
-->
## 无头服务（Headless Services）  {#headless-services}

有时不需要或不想要负载均衡，以及单独的 Service IP。
遇到这种情况，可以通过指定 Cluster IP（`spec.clusterIP`）的值为 `"None"`
来创建 `Headless` Service。

你可以使用无头 Service 与其他服务发现机制进行接口，而不必与 Kubernetes
的实现捆绑在一起。

对这无头 Service 并不会分配 Cluster IP，kube-proxy 不会处理它们，
而且平台也不会为它们进行负载均衡和路由。
DNS 如何实现自动配置，依赖于 Service 是否定义了选择算符。

<!--
### With selectors

For headless Services that define selectors, the endpoints controller creates
`Endpoints` records in the API, and modifies the DNS configuration to return
A records (IP addresses) that point directly to the `Pods` backing the `Service`.
-->
### 带选择算符的服务 {#with-selectors}

对定义了选择算符的无头服务，Endpoint 控制器在 API 中创建了 Endpoints 记录，
并且修改 DNS 配置返回 A 记录（IP 地址），通过这个地址直接到达 `Service` 的后端 Pod 上。

<!--
### Without selectors

For headless Services that do not define selectors, the endpoints controller does
not create `Endpoints` records. However, the DNS system looks for and configures
either:

* CNAME records for [`ExternalName`](#externalname)-type Services.
* A records for any `Endpoints` that share a name with the Service, for all
  other types.
-->
### 无选择算符的服务  {#without-selectors}

对没有定义选择算符的无头服务，Endpoint 控制器不会创建 `Endpoints` 记录。
然而 DNS 系统会查找和配置，无论是：

* 对于 [`ExternalName`](#external-name) 类型的服务，查找其 CNAME 记录
* 对所有其他类型的服务，查找与 Service 名称相同的任何 `Endpoints` 的记录

<!--
## Publishing Services (ServiceTypes) {#publishing-services-service-types}

For some parts of your application (for example, frontends) you may want to expose a
Service onto an external IP address, that's outside of your cluster.

Kubernetes `ServiceTypes` allow you to specify what kind of Service you want.
The default is `ClusterIP`.

`Type` values and their behaviors are:
-->
## 发布服务（服务类型)      {#publishing-services-service-types}

对一些应用的某些部分（如前端），可能希望将其暴露给 Kubernetes 集群外部
的 IP 地址。

Kubernetes `ServiceTypes` 允许指定你所需要的 Service 类型，默认是 `ClusterIP`。

`Type` 的取值以及行为如下：

<!--
* `ClusterIP`: Exposes the Service on a cluster-internal IP. Choosing this value
  makes the Service only reachable from within the cluster. This is the
  default `ServiceType`.
* [`NodePort`](#nodeport): Exposes the Service on each Node's IP at a static port
  (the `NodePort`). A `ClusterIP` Service, to which the `NodePort` Service
  routes, is automatically created.  You'll be able to contact the `NodePort` Service,
  from outside the cluster,
  by requesting `<NodeIP>:<NodePort>`.
* [`LoadBalancer`](#loadbalancer): Exposes the Service externally using a cloud
  provider's load balancer. `NodePort` and `ClusterIP` Services, to which the external
  load balancer routes, are automatically created.
* [`ExternalName`](#externalname): Maps the Service to the contents of the
  `externalName` field (e.g. `foo.bar.example.com`), by returning a `CNAME` record
  with its value. No proxying of any kind is set up.
  {{< note >}}
  You need either kube-dns version 1.7 or CoreDNS version 0.0.8 or higher to use the `ExternalName` type.
  {{< /note >}}
-->
* `ClusterIP`：通过集群的内部 IP 暴露服务，选择该值时服务只能够在集群内部访问。
  这也是默认的 `ServiceType`。
* [`NodePort`](#nodeport)：通过每个节点上的 IP 和静态端口（`NodePort`）暴露服务。
  `NodePort` 服务会路由到自动创建的 `ClusterIP` 服务。
  通过请求 `<节点 IP>:<节点端口>`，你可以从集群的外部访问一个 `NodePort` 服务。
* [`LoadBalancer`](#loadbalancer)：使用云提供商的负载均衡器向外部暴露服务。
  外部负载均衡器可以将流量路由到自动创建的 `NodePort` 服务和 `ClusterIP` 服务上。
* [`ExternalName`](#externalname)：通过返回 `CNAME` 和对应值，可以将服务映射到
  `externalName` 字段的内容（例如，`foo.bar.example.com`）。
  无需创建任何类型代理。

  {{< note >}}
  你需要使用 kube-dns 1.7 及以上版本或者 CoreDNS 0.0.8 及以上版本才能使用 `ExternalName` 类型。
  {{< /note >}}

<!--
You can also use [Ingress](/docs/concepts/services-networking/ingress/) to expose your Service. Ingress is not a Service type, but it acts as the entry point for your cluster. It lets you consolidate your routing rules into a single resource as it can expose multiple services under the same IP address.
-->
你也可以使用 [Ingress](/zh/docs/concepts/services-networking/ingress/) 来暴露自己的服务。
Ingress 不是一种服务类型，但它充当集群的入口点。
它可以将路由规则整合到一个资源中，因为它可以在同一IP地址下公开多个服务。

<!--
### Type NodePort {#nodeport}

If you set the `type` field to `NodePort`, the Kubernetes control plane
allocates a port from a range specified by `--service-node-port-range` flag (default: 30000-32767).
Each node proxies that port (the same port number on every Node) into your Service.
Your Service reports the allocated port in its `.spec.ports[*].nodePort` field.

If you want to specify particular IP(s) to proxy the port, you can set the
`--nodeport-addresses` flag for kube-proxy or the equivalent `nodePortAddresses`
field of the
[kube-proxy configuration file](/docs/reference/config-api/kube-proxy-config.v1alpha1/)
to particular IP block(s).

This flag takes a comma-delimited list of IP blocks (e.g. `10.0.0.0/8`, `192.0.2.0/25`) to specify IP address ranges that kube-proxy should consider as local to this node.
-->
### NodePort 类型  {#nodeport}

如果你将 `type` 字段设置为 `NodePort`，则 Kubernetes 控制平面将在
`--service-node-port-range` 标志指定的范围内分配端口（默认值：30000-32767）。
每个节点将那个端口（每个节点上的相同端口号）代理到你的服务中。
你的服务在其 `.spec.ports[*].nodePort` 字段中要求分配的端口。

如果你想指定特定的 IP 代理端口，则可以设置 kube-proxy 中的 `--nodeport-addresses` 参数
或者将[kube-proxy 配置文件](/docs/reference/config-api/kube-proxy-config.v1alpha1/)
中的等效 `nodePortAddresses` 字段设置为特定的 IP 块。
该标志采用逗号分隔的 IP 块列表（例如，`10.0.0.0/8`、`192.0.2.0/25`）来指定
kube-proxy 应该认为是此节点本地的 IP 地址范围。

<!--
For example, if you start kube-proxy with the `--nodeport-addresses=127.0.0.0/8` flag, kube-proxy only selects the loopback interface for NodePort Services. The default for `--nodeport-addresses` is an empty list. This means that kube-proxy should consider all available network interfaces for NodePort. (That's also compatible with earlier Kubernetes releases).

If you want a specific port number, you can specify a value in the `nodePort`
field. The control plane will either allocate you that port or report that
the API transaction failed.
This means that you need to take care of possible port collisions yourself.
You also have to use a valid port number, one that's inside the range configured
for NodePort use.
-->
例如，如果你使用 `--nodeport-addresses=127.0.0.0/8` 标志启动 kube-proxy，
则 kube-proxy 仅选择 NodePort Services 的本地回路接口。
`--nodeport-addresses` 的默认值是一个空列表。
这意味着 kube-proxy 应该考虑 NodePort 的所有可用网络接口。
（这也与早期的 Kubernetes 版本兼容）。

如果需要特定的端口号，你可以在 `nodePort` 字段中指定一个值。
控制平面将为你分配该端口或报告 API 事务失败。
这意味着你需要自己注意可能发生的端口冲突。
你还必须使用有效的端口号，该端口号在配置用于 NodePort 的范围内。

<!--
Using a NodePort gives you the freedom to set up your own load balancing solution,
to configure environments that are not fully supported by Kubernetes, or even
to expose one or more nodes' IPs directly.

Note that this Service is visible as `<NodeIP>:spec.ports[*].nodePort`
and `.spec.clusterIP:spec.ports[*].port`.
If the `--nodeport-addresses` flag for kube-proxy or the equivalent field
in the kube-proxy configuration file is set, `<NodeIP>` would be filtered node IP(s).

For example:
-->
使用 NodePort 可以让你自由设置自己的负载均衡解决方案，
配置 Kubernetes 不完全支持的环境，
甚至直接暴露一个或多个节点的 IP。

需要注意的是，Service 能够通过 `<NodeIP>:spec.ports[*].nodePort` 和
`spec.clusterIp:spec.ports[*].port` 而对外可见。
如果设置了 kube-proxy 的 `--nodeport-addresses` 参数或 kube-proxy 配置文件中的等效字段，
 `<NodeIP>` 将被过滤 NodeIP。

例如：

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  type: NodePort
  selector:
    app: MyApp
  ports:
      # 默认情况下，为了方便起见，`targetPort` 被设置为与 `port` 字段相同的值。
    - port: 80
      targetPort: 80
      # 可选字段
      # 默认情况下，为了方便起见，Kubernetes 控制平面会从某个范围内分配一个端口号（默认：30000-32767）
      nodePort: 30007
```

<!--
### Type LoadBalancer {#loadbalancer}

On cloud providers which support external load balancers, setting the `type`
field to `LoadBalancer` provisions a load balancer for your Service.
The actual creation of the load balancer happens asynchronously, and
information about the provisioned balancer is published in the Service's
`.status.loadBalancer` field.
For example:
-->
### LoadBalancer 类型  {#loadbalancer}

在使用支持外部负载均衡器的云提供商的服务时，设置 `type` 的值为 `"LoadBalancer"`，
将为 Service 提供负载均衡器。
负载均衡器是异步创建的，关于被提供的负载均衡器的信息将会通过 Service 的
`status.loadBalancer` 字段发布出去。

实例：

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  selector:
    app: MyApp
  ports:
    - protocol: TCP
      port: 80
      targetPort: 9376
  clusterIP: 10.0.171.239
  type: LoadBalancer
status:
  loadBalancer:
    ingress:
      - ip: 192.0.2.127
```

<!--
Traffic from the external load balancer is directed at the backend Pods. The cloud provider decides how it is load balanced.
-->
来自外部负载均衡器的流量将直接重定向到后端 Pod 上，不过实际它们是如何工作的，这要依赖于云提供商。

<!--
Some cloud providers allow you to specify the `loadBalancerIP`. In those cases, the load-balancer is created
with the user-specified `loadBalancerIP`. If the `loadBalancerIP` field is not specified,
the loadBalancer is set up with an ephemeral IP address. If you specify a `loadBalancerIP`
but your cloud provider does not support the feature, the `loadbalancerIP` field that you
set is ignored.
-->
某些云提供商允许设置 `loadBalancerIP`。
在这些情况下，将根据用户设置的 `loadBalancerIP` 来创建负载均衡器。
如果没有设置 `loadBalancerIP` 字段，将会给负载均衡器指派一个临时 IP。
如果设置了 `loadBalancerIP`，但云提供商并不支持这种特性，那么设置的
`loadBalancerIP` 值将会被忽略掉。


<!--
On **Azure**, if you want to use a user-specified public type `loadBalancerIP`, you first need
to create a static type public IP address resource. This public IP address resource should
be in the same resource group of the other automatically created resources of the cluster.
For example, `MC_myResourceGroup_myAKSCluster_eastus`.

Specify the assigned IP address as loadBalancerIP. Ensure that you have updated the securityGroupName in the cloud provider configuration file. For information about troubleshooting `CreatingLoadBalancerFailed` permission issues see, [Use a static IP address with the Azure Kubernetes Service (AKS) load balancer](https://docs.microsoft.com/en-us/azure/aks/static-ip) or [CreatingLoadBalancerFailed on AKS cluster with advanced networking](https://github.com/Azure/AKS/issues/357).
-->
{{< note >}}
在 **Azure** 上，如果要使用用户指定的公共类型 `loadBalancerIP`，则
首先需要创建静态类型的公共 IP 地址资源。
此公共 IP 地址资源应与集群中其他自动创建的资源位于同一资源组中。
例如，`MC_myResourceGroup_myAKSCluster_eastus`。

将分配的 IP 地址设置为 loadBalancerIP。确保你已更新云提供程序配置文件中的
securityGroupName。
有关对 `CreatingLoadBalancerFailed` 权限问题进行故障排除的信息，
请参阅 [与 Azure Kubernetes 服务（AKS）负载平衡器一起使用静态 IP 地址](https://docs.microsoft.com/en-us/azure/aks/static-ip)
或[在 AKS 集群上使用高级联网时出现 CreatingLoadBalancerFailed](https://github.com/Azure/AKS/issues/357)。
{{< /note >}}
<!--
#### Load balancers with mixed protocol types

{{< feature-state for_k8s_version="v1.20" state="alpha" >}}

By default, for LoadBalancer type of Services, when there is more than one port defined, all
ports must have the same protocol, and the protocol must be one which is supported
by the cloud provider.

If the feature gate `MixedProtocolLBService` is enabled for the kube-apiserver it is allowed to use different protocols when there is more than one port defined.
-->
#### 混合协议类型的负载均衡器

{{< feature-state for_k8s_version="v1.20" state="alpha" >}}

默认情况下，对于 LoadBalancer 类型的服务，当定义了多个端口时，所有
端口必须具有相同的协议，并且该协议必须是受云提供商支持的协议。

如果为 kube-apiserver 启用了 `MixedProtocolLBService` 特性门控，
则当定义了多个端口时，允许使用不同的协议。

<!--
The set of protocols that can be used for LoadBalancer type of Services is still defined by the cloud provider.
-->
{{< note >}}
可用于 LoadBalancer 类型服务的协议集仍然由云提供商决定。
{{< /note >}}

<!--
#### Disabling load balancer NodePort allocation {#load-balancer-nodeport-allocation}
-->
### 禁用负载均衡器节点端口分配 {#load-balancer-nodeport-allocation}

{{< feature-state for_k8s_version="v1.20" state="alpha" >}}

<!--
Starting in v1.20, you can optionally disable node port allocation for a Service Type=LoadBalancer by setting
the field `spec.allocateLoadBalancerNodePorts` to `false`. This should only be used for load balancer implementations
that route traffic directly to pods as opposed to using node ports. By default, `spec.allocateLoadBalancerNodePorts`
is `true` and type LoadBalancer Services will continue to allocate node ports. If `spec.allocateLoadBalancerNodePorts`
is set to `false` on an existing Service with allocated node ports, those node ports will NOT be de-allocated automatically.
You must explicitly remove the `nodePorts` entry in every Service port to de-allocate those node ports.
You must enable the `ServiceLBNodePortControl` feature gate to use this field.
-->
从 v1.20 版本开始， 你可以通过设置 `spec.allocateLoadBalancerNodePorts` 为 `false`
对类型为 LoadBalancer 的服务禁用节点端口分配。
这仅适用于直接将流量路由到 Pod 而不是使用节点端口的负载均衡器实现。
默认情况下，`spec.allocateLoadBalancerNodePorts` 为 `true`，
LoadBalancer 类型的服务继续分配节点端口。
如果现有服务已被分配节点端口，将参数 `spec.allocateLoadBalancerNodePorts`
设置为 `false` 时，这些服务上已分配置的节点端口不会被自动释放。
你必须显式地在每个服务端口中删除 `nodePorts` 项以释放对应端口。
你必须启用 `ServiceLBNodePortControl` 特性门控才能使用该字段。

<!--
#### Specifying class of load balancer implementation {#load-balancer-class}
-->
#### 设置负载均衡器实现的类别 {#load-balancer-class}

{{< feature-state for_k8s_version="v1.21" state="alpha" >}}

<!--
Starting in v1.21, you can optionally specify the class of a load balancer implementation for
`LoadBalancer` type of Service by setting the field `spec.loadBalancerClass`.
By default, `spec.loadBalancerClass` is `nil` and a `LoadBalancer` type of Service uses
the cloud provider's default load balancer implementation.
If `spec.loadBalancerClass` is specified, it is assumed that a load balancer
implementation that matches the specified class is watching for Services.
Any default load balancer implementation (for example, the one provided by
the cloud provider) will ignore Services that have this field set.
`spec.loadBalancerClass` can be set on a Service of type `LoadBalancer` only.
Once set, it cannot be changed.
-->
从 v1.21 开始，你可以有选择地为 `LoadBalancer` 类型的服务设置字段
`.spec.loadBalancerClass`，以指定其负载均衡器实现的类别。
默认情况下，`.spec.loadBalancerClass` 的取值是 `nil`，`LoadBalancer` 类型
服务会使用云提供商的默认负载均衡器实现。
如果设置了 `.spec.loadBalancerClass`，则假定存在某个与所指定的类相匹配的
负载均衡器实现在监视服务变化。
所有默认的负载均衡器实现（例如，由云提供商所提供的）都会忽略设置了此字段
的服务。`.spec.loadBalancerClass` 只能设置到类型为 `LoadBalancer` 的 Service
之上，而且一旦设置之后不可变更。

<!--
The value of `spec.loadBalancerClass` must be a label-style identifier,
with an optional prefix such as "`internal-vip`" or "`example.com/internal-vip`".
Unprefixed names are reserved for end-users.
You must enable the `ServiceLoadBalancerClass` feature gate to use this field.
-->
`.spec.loadBalancerClass` 的值必须是一个标签风格的标识符，
可以有选择地带有类似 "`internal-vip`" 或 "`example.com/internal-vip`" 这类
前缀。没有前缀的名字是保留给最终用户的。
你必须启用 `ServiceLoadBalancerClass` 特性门控才能使用此字段。

<!--
#### Internal load balancer

In a mixed environment it is sometimes necessary to route traffic from Services inside the same
(virtual) network address block.

In a split-horizon DNS environment you would need two Services to be able to route both external and internal traffic to your endpoints.

To set an internal load balancer, add one of the following annotations to your Service
depending on the cloud Service provider you're using.
-->
#### 内部负载均衡器 {#internal-load-balancer}

在混合环境中，有时有必要在同一(虚拟)网络地址块内路由来自服务的流量。

在水平分割 DNS 环境中，你需要两个服务才能将内部和外部流量都路由到你的端点（Endpoints）。

如要设置内部负载均衡器，请根据你所使用的云运营商，为服务添加以下注解之一。

{{< tabs name="service_tabs" >}}
{{% tab name="Default" %}}
<!--
Select one of the tabs.
-->
选择一个标签
{{% /tab %}}
{{% tab name="GCP" %}}
```yaml
[...]
metadata:
    name: my-service
    annotations:
        cloud.google.com/load-balancer-type: "Internal"
[...]
```

{{% /tab %}}
{{% tab name="AWS" %}}

```yaml
[...]
metadata:
    name: my-service
    annotations:
        service.beta.kubernetes.io/aws-load-balancer-internal: "true"
[...]
```

{{% /tab %}}
{{% tab name="Azure" %}}

```yaml
[...]
metadata:
    name: my-service
    annotations:
        service.beta.kubernetes.io/azure-load-balancer-internal: "true"
[...]
```

{{% /tab %}}
{{% tab name="IBM Cloud" %}}

```yaml
[...]
metadata:
    name: my-service
    annotations:
        service.kubernetes.io/ibm-load-balancer-cloud-provider-ip-type: "private"
[...]
```

{{% /tab %}}
{{% tab name="OpenStack" %}}

```yaml
[...]
metadata:
    name: my-service
    annotations:
        service.beta.kubernetes.io/openstack-internal-load-balancer: "true"
[...]
```

{{% /tab %}}
{{% tab name="Baidu Cloud" %}}

```yaml
[...]
metadata:
    name: my-service
    annotations:
        service.beta.kubernetes.io/cce-load-balancer-internal-vpc: "true"
[...]
```

{{% /tab %}}
{{% tab name="Tencent Cloud" %}}

```yaml
[...]
metadata:
  annotations:
    service.kubernetes.io/qcloud-loadbalancer-internal-subnetid: subnet-xxxxx
[...]
```

{{% /tab %}}
{{% tab name="Alibaba Cloud" %}}

```yaml
[...]
metadata:
  annotations:
    service.beta.kubernetes.io/alibaba-cloud-loadbalancer-address-type: "intranet"
[...]
```

{{% /tab %}}
{{< /tabs >}}

<!--
#### TLS support on AWS {#ssl-support-on-aws}

For partial TLS / SSL support on clusters running on AWS, you can add three
annotations to a `LoadBalancer` service:
-->
### AWS TLS 支持 {#ssl-support-on-aws}

为了对在 AWS 上运行的集群提供 TLS/SSL 部分支持，你可以向 `LoadBalancer`
服务添加三个注解：

```yaml
metadata:
  name: my-service
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-ssl-cert: arn:aws:acm:us-east-1:123456789012:certificate/12345678-1234-1234-1234-123456789012
```

<!--
The first specifies the ARN of the certificate to use. It can be either a
certificate from a third party issuer that was uploaded to IAM or one created
within AWS Certificate Manager.
-->
第一个指定要使用的证书的 ARN。 它可以是已上载到 IAM 的第三方颁发者的证书，
也可以是在 AWS Certificate Manager 中创建的证书。

```yaml
metadata:
  name: my-service
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-backend-protocol: (https|http|ssl|tcp)
```

<!--
The second annotation specifies which protocol a Pod speaks. For HTTPS and
SSL, the ELB expects the Pod to authenticate itself over the encrypted
connection, using a certificate.

HTTP and HTTPS selects layer 7 proxying: the ELB terminates
the connection with the user, parses headers, and injects the `X-Forwarded-For`
header with the user's IP address (Pods only see the IP address of the
ELB at the other end of its connection) when forwarding requests.

TCP and SSL selects layer 4 proxying: the ELB forwards traffic without
modifying the headers.

In a mixed-use environment where some ports are secured and others are left unencrypted,
you can use the following annotations:
-->
第二个注解指定 Pod 使用哪种协议。 对于 HTTPS 和 SSL，ELB 希望 Pod 使用证书
通过加密连接对自己进行身份验证。

HTTP 和 HTTPS 选择第7层代理：ELB 终止与用户的连接，解析标头，并在转发请求时向
`X-Forwarded-For` 标头注入用户的 IP 地址（Pod 仅在连接的另一端看到 ELB 的 IP 地址）。

TCP 和 SSL 选择第4层代理：ELB 转发流量而不修改报头。

在某些端口处于安全状态而其他端口未加密的混合使用环境中，可以使用以下注解：

```yaml
    metadata:
      name: my-service
      annotations:
        service.beta.kubernetes.io/aws-load-balancer-backend-protocol: http
        service.beta.kubernetes.io/aws-load-balancer-ssl-ports: "443,8443"
```

<!--
In the above example, if the Service contained three ports, `80`, `443`, and
`8443`, then `443` and `8443` would use the SSL certificate, but `80` would be proxied HTTP.

From Kubernetes v1.9 onwards you can use [predefined AWS SSL policies](https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/elb-security-policy-table.html) with HTTPS or SSL listeners for your Services.
To see which policies are available for use, you can use the `aws` command line tool:
-->
在上例中，如果服务包含 `80`、`443` 和 `8443` 三个端口， 那么 `443` 和 `8443` 将使用 SSL 证书，
而 `80` 端口将转发 HTTP 数据包。

从 Kubernetes v1.9 起可以使用
[预定义的 AWS SSL 策略](https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/elb-security-policy-table.html)
为你的服务使用 HTTPS 或 SSL 侦听器。
要查看可以使用哪些策略，可以使用 `aws` 命令行工具：

```bash
aws elb describe-load-balancer-policies --query 'PolicyDescriptions[].PolicyName'
```

<!--
You can then specify any one of those policies using the
"`service.beta.kubernetes.io/aws-load-balancer-ssl-negotiation-policy`"
annotation; for example:
-->
然后，你可以使用 "`service.beta.kubernetes.io/aws-load-balancer-ssl-negotiation-policy`"
注解; 例如：

```yaml
    metadata:
      name: my-service
      annotations:
        service.beta.kubernetes.io/aws-load-balancer-ssl-negotiation-policy: "ELBSecurityPolicy-TLS-1-2-2017-01"
```

<!--
#### PROXY protocol support on AWS

To enable [PROXY protocol](https://www.haproxy.org/download/1.8/doc/proxy-protocol.txt)
support for clusters running on AWS, you can use the following service
annotation:
-->
#### AWS 上的 PROXY 协议支持

为了支持在 AWS 上运行的集群，启用
[PROXY 协议](https://www.haproxy.org/download/1.8/doc/proxy-protocol.txt)。
你可以使用以下服务注解：

```yaml
    metadata:
      name: my-service
      annotations:
        service.beta.kubernetes.io/aws-load-balancer-proxy-protocol: "*"
```

<!--
Since version 1.3.0, the use of this annotation applies to all ports proxied by the ELB
and cannot be configured otherwise.
-->
从 1.3.0 版开始，此注解的使用适用于 ELB 代理的所有端口，并且不能进行其他配置。
<!--
#### ELB Access Logs on AWS

There are several annotations to manage access logs for ELB Services on AWS.

The annotation `service.beta.kubernetes.io/aws-load-balancer-access-log-enabled`
controls whether access logs are enabled.

The annotation `service.beta.kubernetes.io/aws-load-balancer-access-log-emit-interval`
controls the interval in minutes for publishing the access logs. You can specify
an interval of either 5 or 60 minutes.

The annotation `service.beta.kubernetes.io/aws-load-balancer-access-log-s3-bucket-name`
controls the name of the Amazon S3 bucket where load balancer access logs are
stored.

The annotation `service.beta.kubernetes.io/aws-load-balancer-access-log-s3-bucket-prefix`
specifies the logical hierarchy you created for your Amazon S3 bucket.
-->
#### AWS 上的 ELB 访问日志

有几个注解可用于管理 AWS 上 ELB 服务的访问日志。

注解 `service.beta.kubernetes.io/aws-load-balancer-access-log-enabled` 控制是否启用访问日志。

注解 `service.beta.kubernetes.io/aws-load-balancer-access-log-emit-interval`
控制发布访问日志的时间间隔（以分钟为单位）。你可以指定 5 分钟或 60 分钟的间隔。

注解 `service.beta.kubernetes.io/aws-load-balancer-access-log-s3-bucket-name`
控制存储负载均衡器访问日志的 Amazon S3 存储桶的名称。

注解 `service.beta.kubernetes.io/aws-load-balancer-access-log-s3-bucket-prefix`
指定为 Amazon S3 存储桶创建的逻辑层次结构。

```yaml
    metadata:
      name: my-service
      annotations:
        service.beta.kubernetes.io/aws-load-balancer-access-log-enabled: "true"
        # 指定是否为负载均衡器启用访问日志
        service.beta.kubernetes.io/aws-load-balancer-access-log-emit-interval: "60"
        # 发布访问日志的时间间隔。你可以将其设置为 5 分钟或 60 分钟。
        service.beta.kubernetes.io/aws-load-balancer-access-log-s3-bucket-name: "my-bucket"
        # 用来存放访问日志的 Amazon S3 Bucket 名称
        service.beta.kubernetes.io/aws-load-balancer-access-log-s3-bucket-prefix: "my-bucket-prefix/prod"
        # 你为 Amazon S3 Bucket 所创建的逻辑层次结构，例如 `my-bucket-prefix/prod`
```

<!--
#### Connection Draining on AWS

Connection draining for Classic ELBs can be managed with the annotation
`service.beta.kubernetes.io/aws-load-balancer-connection-draining-enabled` set
to the value of `"true"`. The annotation
`service.beta.kubernetes.io/aws-load-balancer-connection-draining-timeout` can
also be used to set maximum time, in seconds, to keep the existing connections open before deregistering the instances.
-->
#### AWS 上的连接排空

可以将注解 `service.beta.kubernetes.io/aws-load-balancer-connection-draining-enabled`
设置为 `"true"` 来管理 ELB 的连接排空。
注解 `service.beta.kubernetes.io/aws-load-balancer-connection-draining-timeout`
也可以用于设置最大时间（以秒为单位），以保持现有连接在注销实例之前保持打开状态。

```yaml
    metadata:
      name: my-service
      annotations:
        service.beta.kubernetes.io/aws-load-balancer-connection-draining-enabled: "true"
        service.beta.kubernetes.io/aws-load-balancer-connection-draining-timeout: "60"
```

<!--
#### Other ELB annotations

There are other annotations to manage Classic Elastic Load Balancers that are described below.
-->
#### 其他 ELB 注解

还有其他一些注解，用于管理经典弹性负载均衡器，如下所述。

```yaml
    metadata:
      name: my-service
      annotations:
        # 按秒计的时间，表示负载均衡器关闭连接之前连接可以保持空闲
        # （连接上无数据传输）的时间长度
        service.beta.kubernetes.io/aws-load-balancer-connection-idle-timeout: "60"

        # 指定该负载均衡器上是否启用跨区的负载均衡能力
        service.beta.kubernetes.io/aws-load-balancer-cross-zone-load-balancing-enabled: "true"

        # 逗号分隔列表值，每一项都是一个键-值耦对，会作为额外的标签记录于 ELB 中
        service.beta.kubernetes.io/aws-load-balancer-additional-resource-tags: "environment=prod,owner=devops"

        # 将某后端视为健康、可接收请求之前需要达到的连续成功健康检查次数。
        # 默认为 2，必须介于 2 和 10 之间
        service.beta.kubernetes.io/aws-load-balancer-healthcheck-healthy-threshold: ""

        # 将某后端视为不健康、不可接收请求之前需要达到的连续不成功健康检查次数。
        # 默认为 6，必须介于 2 和 10 之间
        service.beta.kubernetes.io/aws-load-balancer-healthcheck-unhealthy-threshold: "3"

        # 对每个实例进行健康检查时，连续两次检查之间的大致间隔秒数
        # 默认为 10，必须介于 5 和 300 之间
        service.beta.kubernetes.io/aws-load-balancer-healthcheck-interval: "20"

        # 时长秒数，在此期间没有响应意味着健康检查失败
        # 此值必须小于 service.beta.kubernetes.io/aws-load-balancer-healthcheck-interval
        # 默认值为 5，必须介于 2 和 60 之间
        service.beta.kubernetes.io/aws-load-balancer-healthcheck-timeout: "5"

        # 由已有的安全组所构成的列表，可以配置到所创建的 ELB 之上。
        # 与注解 service.beta.kubernetes.io/aws-load-balancer-extra-security-groups 不同，
        # 这一设置会替代掉之前指定给该 ELB 的所有其他安全组，也会覆盖掉为此
        # ELB 所唯一创建的安全组。
        # 此列表中的第一个安全组 ID 被用来作为决策源，以允许入站流量流入目标工作节点
        # (包括服务流量和健康检查）。
        # 如果多个 ELB 配置了相同的安全组 ID，为工作节点安全组添加的允许规则行只有一个，
        # 这意味着如果你删除了这些 ELB 中的任何一个，都会导致该规则记录被删除，
        # 以至于所有共享该安全组 ID 的其他 ELB 都无法访问该节点。
        # 此注解如果使用不当，会导致跨服务的不可用状况。
        service.beta.kubernetes.io/aws-load-balancer-security-groups: "sg-53fae93f"

        # 额外的安全组列表，将被添加到所创建的 ELB 之上。
        # 添加时，会保留为 ELB 所专门创建的安全组。
        # 这样会确保每个 ELB 都有一个唯一的安全组 ID 和与之对应的允许规则记录，
        # 允许请求（服务流量和健康检查）发送到目标工作节点。
        # 这里顶一个安全组可以被多个服务共享。
        service.beta.kubernetes.io/aws-load-balancer-extra-security-groups: "sg-53fae93f,sg-42efd82e"

        # 用逗号分隔的一个键-值偶对列表，用来为负载均衡器选择目标节点
        service.beta.kubernetes.io/aws-load-balancer-target-node-labels: "ingress-gw,gw-name=public-api"
```

<!--
#### Network Load Balancer support on AWS {#aws-nlb-support}
-->
#### AWS 上网络负载均衡器支持 {#aws-nlb-support}

{{< feature-state for_k8s_version="v1.15" state="beta" >}}

<!--
To use a Network Load Balancer on AWS, use the annotation `service.beta.kubernetes.io/aws-load-balancer-type` with the value set to `nlb`.
-->
要在 AWS 上使用网络负载均衡器，可以使用注解
`service.beta.kubernetes.io/aws-load-balancer-type`，将其取值设为 `nlb`。

```yaml
    metadata:
      name: my-service
      annotations:
        service.beta.kubernetes.io/aws-load-balancer-type: "nlb"
```

<!--
NLB only works with certain instance classes; see the [AWS documentation](http://docs.aws.amazon.com/elasticloadbalancing/latest/network/target-group-register-targets.html#register-deregister-targets)
on Elastic Load Balancing for a list of supported instance types.
-->
{{< note >}}
NLB 仅适用于某些实例类。有关受支持的实例类型的列表，
请参见
[AWS文档](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/target-group-register-targets.html#register-deregister-targets)
中关于所支持的实例类型的 Elastic Load Balancing 说明。
{{< /note >}}

<!--
Unlike Classic Elastic Load Balancers, Network Load Balancers (NLBs) forward the
client's IP address through to the node. If a Service's `.spec.externalTrafficPolicy`
is set to `Cluster`, the client's IP address is not propagated to the end
Pods.

By setting `.spec.externalTrafficPolicy` to `Local`, the client IP addresses is
propagated to the end Pods, but this could result in uneven distribution of
traffic. Nodes without any Pods for a particular LoadBalancer Service will fail
the NLB Target Group's health check on the auto-assigned
`.spec.healthCheckNodePort` and not receive any traffic.
-->
与经典弹性负载平衡器不同，网络负载平衡器（NLB）将客户端的 IP 地址转发到该节点。
如果服务的 `.spec.externalTrafficPolicy` 设置为 `Cluster` ，则客户端的IP地址不会传达到最终的 Pod。

通过将 `.spec.externalTrafficPolicy` 设置为 `Local`，客户端IP地址将传播到最终的 Pod，
但这可能导致流量分配不均。
没有针对特定 LoadBalancer 服务的任何 Pod 的节点将无法通过自动分配的
`.spec.healthCheckNodePort` 进行 NLB 目标组的运行状况检查，并且不会收到任何流量。

<!--
In order to achieve even traffic, either use a DaemonSet, or specify a
[pod anti-affinity](/docs/concepts/scheduling-eviction/assign-pod-node/#affinity-and-anti-affinity)
to not locate on the same node.

You can also use NLB Services with the [internal load balancer](/docs/concepts/services-networking/service/#internal-load-balancer)
annotation.

In order for client traffic to reach instances behind an NLB, the Node security
groups are modified with the following IP rules:
-->

为了获得均衡流量，请使用 DaemonSet 或指定
[Pod 反亲和性](/zh/docs/concepts/scheduling-eviction/assign-pod-node/#affinity-and-anti-affinity)
使其不在同一节点上。

你还可以将 NLB 服务与[内部负载平衡器](/zh/docs/concepts/services-networking/service/#internal-load-balancer)
注解一起使用。

为了使客户端流量能够到达 NLB 后面的实例，使用以下 IP 规则修改了节点安全组：

| Rule | Protocol | Port(s) | IpRange(s) | IpRange Description |
|------|----------|---------|------------|---------------------|
| Health Check | TCP | NodePort(s) (`.spec.healthCheckNodePort` for `.spec.externalTrafficPolicy = Local`) | Subnet CIDR | kubernetes.io/rule/nlb/health=\<loadBalancerName\> |
| Client Traffic | TCP | NodePort(s) | `.spec.loadBalancerSourceRanges` (defaults to `0.0.0.0/0`) | kubernetes.io/rule/nlb/client=\<loadBalancerName\> |
| MTU Discovery | ICMP | 3,4 | `.spec.loadBalancerSourceRanges` (defaults to `0.0.0.0/0`) | kubernetes.io/rule/nlb/mtu=\<loadBalancerName\> |

<!--
In order to limit which client IP's can access the Network Load Balancer,
specify `loadBalancerSourceRanges`.
-->
为了限制哪些客户端IP可以访问网络负载平衡器，请指定 `loadBalancerSourceRanges`。

```yaml
spec:
  loadBalancerSourceRanges:
    - "143.231.0.0/16"
```

<!--
If `.spec.loadBalancerSourceRanges` is not set, Kubernetes
allows traffic from `0.0.0.0/0` to the Node Security Group(s). If nodes have
public IP addresses, be aware that non-NLB traffic can also reach all instances
in those modified security groups.
-->
{{< note >}}
如果未设置 `.spec.loadBalancerSourceRanges` ，则 Kubernetes 允许从 `0.0.0.0/0` 到节点安全组的流量。
如果节点具有公共 IP 地址，请注意，非 NLB 流量也可以到达那些修改后的安全组中的所有实例。
{{< /note >}}

<!--
#### Other CLB annotations on Tencent Kubernetes Engine (TKE)

There are other annotations for managing Cloud Load Balancers on TKE as shown below.

```yaml
    metadata:
      name: my-service
      annotations:
        # Bind Loadbalancers with specified nodes
        service.kubernetes.io/qcloud-loadbalancer-backends-label: key in (value1, value2)

        # ID of an existing load balancer
        service.kubernetes.io/tke-existed-lbid：lb-6swtxxxx

        # Custom parameters for the load balancer (LB), does not support modification of LB type yet
        service.kubernetes.io/service.extensiveParameters: ""

        # Custom parameters for the LB listener
        service.kubernetes.io/service.listenerParameters: ""

        # Specifies the type of Load balancer;
        # valid values: classic (Classic Cloud Load Balancer) or application (Application Cloud Load Balancer)
        service.kubernetes.io/loadbalance-type: xxxxx

        # Specifies the public network bandwidth billing method;
        # valid values: TRAFFIC_POSTPAID_BY_HOUR(bill-by-traffic) and BANDWIDTH_POSTPAID_BY_HOUR (bill-by-bandwidth).
        service.kubernetes.io/qcloud-loadbalancer-internet-charge-type: xxxxxx

        # Specifies the bandwidth value (value range: [1,2000] Mbps).
        service.kubernetes.io/qcloud-loadbalancer-internet-max-bandwidth-out: "10"

        # When this annotation is set，the loadbalancers will only register nodes
        # with pod running on it, otherwise all nodes will be registered.
        service.kubernetes.io/local-svc-only-bind-node-with-pod: true
```
-->
#### 腾讯 Kubernetes 引擎（TKE）上的 CLB 注解

以下是在 TKE 上管理云负载均衡器的注解。

```yaml
    metadata:
      name: my-service
      annotations:
        # 绑定负载均衡器到指定的节点。
        service.kubernetes.io/qcloud-loadbalancer-backends-label: key in (value1, value2)

        # 为已有负载均衡器添加 ID。
        service.kubernetes.io/tke-existed-lbid：lb-6swtxxxx

        # 负载均衡器（LB）的自定义参数尚不支持修改 LB 类型。
        service.kubernetes.io/service.extensiveParameters: ""

        # 自定义负载均衡监听器。
        service.kubernetes.io/service.listenerParameters: ""

        # 指定负载均衡类型。
        # 可用参数: classic (Classic Cloud Load Balancer) 或 application (Application Cloud Load Balancer)
        service.kubernetes.io/loadbalance-type: xxxxx

        # 指定公用网络带宽计费方法。
        # 可用参数: TRAFFIC_POSTPAID_BY_HOUR(bill-by-traffic) 和 BANDWIDTH_POSTPAID_BY_HOUR (bill-by-bandwidth).
        service.kubernetes.io/qcloud-loadbalancer-internet-charge-type: xxxxxx

        # 指定带宽参数 (取值范围： [1,2000] Mbps).
        service.kubernetes.io/qcloud-loadbalancer-internet-max-bandwidth-out: "10"

        # 当设置该注解时，负载平衡器将只注册正在运行 Pod 的节点，
        # 否则所有节点将会被注册。
        service.kubernetes.io/local-svc-only-bind-node-with-pod: true
```
<!--
### Type ExternalName {#externalname}

Services of type ExternalName map a Service to a DNS name, not to a typical selector such as
`my-service` or `cassandra`. You specify these Services with the `spec.externalName` parameter.

This Service definition, for example, maps
the `my-service` Service in the `prod` namespace to `my.database.example.com`:
-->

### ExternalName 类型         {#externalname}

类型为 ExternalName 的服务将服务映射到 DNS 名称，而不是典型的选择器，例如 `my-service` 或者 `cassandra`。
你可以使用 `spec.externalName` 参数指定这些服务。

例如，以下 Service 定义将 `prod` 名称空间中的 `my-service` 服务映射到 `my.database.example.com`：

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
  namespace: prod
spec:
  type: ExternalName
  externalName: my.database.example.com
```

<!--
ExternalName accepts an IPv4 address string, but as a DNS names comprised of digits, not as an IP address. ExternalNames that resemble IPv4 addresses are not resolved by CoreDNS or ingress-nginx because ExternalName
is intended to specify a canonical DNS name. To hardcode an IP address, consider using
[headless Services](#headless-services).
-->
{{< note >}}
ExternalName 服务接受 IPv4 地址字符串，但作为包含数字的 DNS 名称，而不是 IP 地址。
类似于 IPv4 地址的外部名称不能由 CoreDNS 或 ingress-nginx 解析，因为外部名称旨在指定规范的 DNS 名称。
要对 IP 地址进行硬编码，请考虑使用 [headless Services](#headless-services)。
{{< /note >}}

<!--
When looking up the host `my-service.prod.svc.cluster.local`, the cluster DNS Service
returns a `CNAME` record with the value `my.database.example.com`. Accessing
`my-service` works in the same way as other Services but with the crucial
difference that redirection happens at the DNS level rather than via proxying or
forwarding. Should you later decide to move your database into your cluster, you
can start its Pods, add appropriate selectors or endpoints, and change the
Service's `type`.
-->
当查找主机 `my-service.prod.svc.cluster.local` 时，集群 DNS 服务返回 `CNAME` 记录，
其值为 `my.database.example.com`。
访问 `my-service` 的方式与其他服务的方式相同，但主要区别在于重定向发生在 DNS 级别，而不是通过代理或转发。
如果以后你决定将数据库移到集群中，则可以启动其 Pod，添加适当的选择器或端点以及更改服务的 `type`。

<!--
{{< warning >}}
You may have trouble using ExternalName for some common protocols, including HTTP and HTTPS. If you use ExternalName then the hostname used by clients inside your cluster is different from the name that the ExternalName references.

For protocols that use hostnames this difference may lead to errors or unexpected responses. HTTP requests will have a `Host:` header that the origin server does not recognize; TLS servers will not be able to provide a certificate matching the hostname that the client connected to.
{{< /warning >}}
-->
{{< warning >}}
对于一些常见的协议，包括 HTTP 和 HTTPS，
你使用 ExternalName 可能会遇到问题。
如果你使用 ExternalName，那么集群内客户端使用的主机名
与 ExternalName 引用的名称不同。

对于使用主机名的协议，此差异可能会导致错误或意外响应。
HTTP 请求将具有源服务器无法识别的 `Host:` 标头；TLS 服
务器将无法提供与客户端连接的主机名匹配的证书。
{{< /warning >}}

<!--
This section is indebted to the [Kubernetes Tips - Part
1](https://akomljen.com/kubernetes-tips-part-1/) blog post from [Alen Komljen](https://akomljen.com/).
-->
{{< note >}}
本部分感谢 [Alen Komljen](https://akomljen.com/)的
[Kubernetes Tips - Part1](https://akomljen.com/kubernetes-tips-part-1/) 博客文章。
{{< /note >}}

<!--
### External IPs

If there are external IPs that route to one or more cluster nodes, Kubernetes Services can be exposed on those
`externalIPs`. Traffic that ingresses into the cluster with the external IP (as destination IP), on the Service port,
will be routed to one of the Service endpoints. `externalIPs` are not managed by Kubernetes and are the responsibility
of the cluster administrator.

In the Service spec, `externalIPs` can be specified along with any of the `ServiceTypes`.
In the example below, "`my-service`" can be accessed by clients on "`80.11.12.10:80`" (`externalIP:port`)
-->
### 外部 IP  {#external-ips}

如果外部的 IP 路由到集群中一个或多个 Node 上，Kubernetes Service 会被暴露给这些 externalIPs。
通过外部 IP（作为目的 IP 地址）进入到集群，打到 Service 的端口上的流量，
将会被路由到 Service 的 Endpoint 上。
`externalIPs` 不会被 Kubernetes 管理，它属于集群管理员的职责范畴。

根据 Service 的规定，`externalIPs` 可以同任意的 `ServiceType` 来一起指定。
在上面的例子中，`my-service` 可以在  "`80.11.12.10:80`"(`externalIP:port`) 上被客户端访问。

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  selector:
    app: MyApp
  ports:
    - name: http
      protocol: TCP
      port: 80
      targetPort: 9376
  externalIPs:
    - 80.11.12.10
```

<!--
## Shortcomings

Using the userspace proxy for VIPs works at small to medium scale, but will
not scale to very large clusters with thousands of Services.  The
[original design proposal for portals](https://github.com/kubernetes/kubernetes/issues/1107)
has more details on this.

Using the userspace proxy obscures the source IP address of a packet accessing
a Service.
This makes some kinds of network filtering (firewalling) impossible.  The iptables
proxy mode does not
obscure in-cluster source IPs, but it does still impact clients coming through
a load balancer or node-port.

The `Type` field is designed as nested functionality - each level adds to the
previous.  This is not strictly required on all cloud providers (e.g. Google Compute Engine does
not need to allocate a `NodePort` to make `LoadBalancer` work, but AWS does)
but the current API requires it.
-->
## 不足之处

为 VIP 使用用户空间代理，将只适合小型到中型规模的集群，不能够扩展到上千 Service 的大型集群。
查看[最初设计方案](https://github.com/kubernetes/kubernetes/issues/1107) 获取更多细节。

使用用户空间代理，隐藏了访问 Service 的数据包的源 IP 地址。
这使得一些类型的防火墙无法起作用。
iptables 代理不会隐藏 Kubernetes 集群内部的 IP 地址，但却要求客户端请求
必须通过一个负载均衡器或 Node 端口。

`Type` 字段支持嵌套功能 —— 每一层需要添加到上一层里面。
不会严格要求所有云提供商（例如，GCE 就没必要为了使一个 `LoadBalancer`
能工作而分配一个 `NodePort`，但是 AWS 需要 ），但当前 API 是强制要求的。

<!--
## Virtual IP implementation {#the-gory-details-of-virtual-ips}

The previous information should be sufficient for many people who want to
use Services.  However, there is a lot going on behind the scenes that may be
worth understanding.
-->
## 虚拟IP实施 {#the-gory-details-of-virtual-ips}

对很多想使用 Service 的人来说，前面的信息应该足够了。
然而，有很多内部原理性的内容，还是值去理解的。

<!--
### Avoiding collisions

One of the primary philosophies of Kubernetes is that you should not be
exposed to situations that could cause your actions to fail through no fault
of your own. For the design of the Service resource, this means not making
you choose your own port number if that choice might collide with
someone else's choice.  That is an isolation failure.

In order to allow you to choose a port number for your Services, we must
ensure that no two Services can collide. Kubernetes does that by allocating each
Service its own IP address.

To ensure each Service receives a unique IP, an internal allocator atomically
updates a global allocation map in {{< glossary_tooltip term_id="etcd" >}}
prior to creating each Service. The map object must exist in the registry for
Services to get IP address assignments, otherwise creations will
fail with a message indicating an IP address could not be allocated.

In the control plane, a background controller is responsible for creating that
map (needed to support migrating from older versions of Kubernetes that used
in-memory locking). Kubernetes also uses controllers to check for invalid
assignments (eg due to administrator intervention) and for cleaning up allocated
IP addresses that are no longer used by any Services.
-->
### 避免冲突

Kubernetes 最主要的哲学之一，是用户不应该暴露那些能够导致他们操作失败、但又不是他们的过错的场景。
对于 Service 资源的设计，这意味着如果用户的选择有可能与他人冲突，那就不要让用户自行选择端口号。
这是一个隔离性的失败。

为了使用户能够为他们的 Service 选择一个端口号，我们必须确保不能有2个 Service 发生冲突。
Kubernetes 通过为每个 Service 分配它们自己的 IP 地址来实现。

为了保证每个 Service 被分配到一个唯一的 IP，需要一个内部的分配器能够原子地更新
{{< glossary_tooltip term_id="etcd" >}} 中的一个全局分配映射表，
这个更新操作要先于创建每一个 Service。
为了使 Service 能够获取到 IP，这个映射表对象必须在注册中心存在，
否则创建 Service 将会失败，指示一个 IP 不能被分配。

在控制平面中，一个后台 Controller 的职责是创建映射表
（需要支持从使用了内存锁的 Kubernetes 的旧版本迁移过来）。
同时 Kubernetes 会通过控制器检查不合理的分配（如管理员干预导致的）
以及清理已被分配但不再被任何 Service 使用的 IP 地址。

<!--
### Service IP addresses {#ips-and-vips}

Unlike Pod IP addresses, which actually route to a fixed destination,
Service IPs are not actually answered by a single host.  Instead, kube-proxy
uses iptables (packet processing logic in Linux) to define _virtual_ IP addresses
which are transparently redirected as needed.  When clients connect to the
VIP, their traffic is automatically transported to an appropriate endpoint.
The environment variables and DNS for Services are actually populated in
terms of the Service's virtual IP address (and port).

kube-proxy supports three proxy modes&mdash;userspace, iptables and IPVS&mdash;which
each operate slightly differently.
-->
### Service IP 地址 {#ips-and-vips}

不像 Pod 的 IP 地址，它实际路由到一个固定的目的地，Service 的 IP 实际上
不能通过单个主机来进行应答。
相反，我们使用 `iptables`（Linux 中的数据包处理逻辑）来定义一个
虚拟 IP 地址（VIP），它可以根据需要透明地进行重定向。
当客户端连接到 VIP 时，它们的流量会自动地传输到一个合适的 Endpoint。
环境变量和 DNS，实际上会根据 Service 的 VIP 和端口来进行填充。

kube-proxy支持三种代理模式: 用户空间，iptables和IPVS；它们各自的操作略有不同。

#### Userspace  {#userspace}

<!--
As an example, consider the image processing application described above.
When the backend Service is created, the Kubernetes master assigns a virtual
IP address, for example 10.0.0.1.  Assuming the Service port is 1234, the
Service is observed by all of the kube-proxy instances in the cluster.
When a proxy sees a new Service, it opens a new random port, establishes an
iptables redirect from the virtual IP address to this new port, and starts accepting
connections on it.

When a client connects to the Service's virtual IP address, the iptables
rule kicks in, and redirects the packets to the proxy's own port.
The "Service proxy" chooses a backend, and starts proxying traffic from the client to the backend.

This means that Service owners can choose any port they want without risk of
collision.  Clients can connect to an IP and port, without being aware
of which Pods they are actually accessing.
-->

作为一个例子，考虑前面提到的图片处理应用程序。
当创建后端 Service 时，Kubernetes master 会给它指派一个虚拟 IP 地址，比如 10.0.0.1。
假设 Service 的端口是 1234，该 Service 会被集群中所有的 `kube-proxy` 实例观察到。
当代理看到一个新的 Service， 它会打开一个新的端口，建立一个从该 VIP 重定向到
新端口的 iptables，并开始接收请求连接。

当一个客户端连接到一个 VIP，iptables 规则开始起作用，它会重定向该数据包到
"服务代理" 的端口。
"服务代理" 选择一个后端，并将客户端的流量代理到后端上。

这意味着 Service 的所有者能够选择任何他们想使用的端口，而不存在冲突的风险。
客户端可以连接到一个 IP 和端口，而不需要知道实际访问了哪些 Pod。

#### iptables

<!--
Again, consider the image processing application described above.
When the backend Service is created, the Kubernetes control plane assigns a virtual
IP address, for example 10.0.0.1.  Assuming the Service port is 1234, the
Service is observed by all of the kube-proxy instances in the cluster.
When a proxy sees a new Service, it installs a series of iptables rules which
redirect from the virtual IP address  to per-Service rules.  The per-Service
rules link to per-Endpoint rules which redirect traffic (using destination NAT)
to the backends.

When a client connects to the Service's virtual IP address the iptables rule kicks in.
A backend is chosen (either based on session affinity or randomly) and packets are
redirected to the backend.  Unlike the userspace proxy, packets are never
copied to userspace, the kube-proxy does not have to be running for the virtual
IP address to work, and Nodes see traffic arriving from the unaltered client IP
address.

This same basic flow executes when traffic comes in through a node-port or
through a load-balancer, though in those cases the client IP does get altered.
-->
再次考虑前面提到的图片处理应用程序。
当创建后端 Service 时，Kubernetes 控制面板会给它指派一个虚拟 IP 地址，比如 10.0.0.1。
假设 Service 的端口是 1234，该 Service 会被集群中所有的 `kube-proxy` 实例观察到。
当代理看到一个新的 Service， 它会配置一系列的 iptables 规则，从 VIP 重定向到每个 Service 规则。
该特定于服务的规则连接到特定于 Endpoint 的规则，而后者会重定向（目标地址转译）到后端。

当客户端连接到一个 VIP，iptables 规则开始起作用。一个后端会被选择（或者根据会话亲和性，或者随机），
数据包被重定向到这个后端。
不像用户空间代理，数据包从来不拷贝到用户空间，kube-proxy 不是必须为该 VIP 工作而运行，
并且客户端 IP 是不可更改的。

当流量打到 Node 的端口上，或通过负载均衡器，会执行相同的基本流程，
但是在那些案例中客户端 IP 是可以更改的。

#### IPVS

<!--
iptables operations slow down dramatically in large scale cluster e.g 10,000 Services.
IPVS is designed for load balancing and based on in-kernel hash tables. So you can achieve performance consistency in large number of Services from IPVS-based kube-proxy. Meanwhile, IPVS-based kube-proxy has more sophisticated load balancing algorithms (least conns, locality, weighted, persistence).
-->
在大规模集群（例如 10000 个服务）中，iptables 操作会显着降低速度。 IPVS
专为负载平衡而设计，并基于内核内哈希表。
因此，你可以通过基于 IPVS 的 kube-proxy 在大量服务中实现性能一致性。
同时，基于 IPVS 的 kube-proxy 具有更复杂的负载均衡算法（最小连接、局部性、
加权、持久性）。

## API 对象

<!--
Service is a top-level resource in the Kubernetes REST API. You can find more details
about the API object at: [Service API object](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#service-v1-core).
-->
Service 是 Kubernetes REST API 中的顶级资源。你可以在以下位置找到有关 API 对象的更多详细信息：
[Service 对象 API](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#service-v1-core).

## 受支持的协议 {#protocol-support}

### TCP

<!--
You can use TCP for any kind of Service, and it's the default network protocol.
-->
你可以将 TCP 用于任何类型的服务，这是默认的网络协议。

### UDP

<!--
You can use UDP for most Services. For type=LoadBalancer Services, UDP support
depends on the cloud provider offering this facility.
-->
你可以将 UDP 用于大多数服务。 对于 type=LoadBalancer 服务，对 UDP 的支持取决于提供此功能的云提供商。

<!--

### SCTP

{{< feature-state for_k8s_version="v1.20" state="stable" >}}

When using a network plugin that supports SCTP traffic, you can use SCTP for
most Services. For type=LoadBalancer Services, SCTP support depends on the cloud
provider offering this facility. (Most do not).
-->
### SCTP

{{< feature-state for_k8s_version="v1.20" state="stable" >}}

一旦你使用了支持 SCTP 流量的网络插件，你就可以使用 SCTP 于更多的服务。
对于 type = LoadBalancer 的服务，SCTP 的支持取决于提供此设施的云供应商（大多数不支持）。

<!--
#### Warnings {#caveat-sctp-overview}

##### Support for multihomed SCTP associations {#caveat-sctp-multihomed}
-->
#### 警告 {#caveat-sctp-overview}

##### 支持多宿主 SCTP 关联 {#caveat-sctp-multihomed}

<!--
{{< warning >}}
The support of multihomed SCTP associations requires that the CNI plugin can support the assignment of multiple interfaces and IP addresses to a Pod.

NAT for multihomed SCTP associations requires special logic in the corresponding kernel modules.
{{< /warning >}}
-->
{{< warning >}}
支持多宿主SCTP关联要求 CNI 插件能够支持为一个 Pod 分配多个接口和IP地址。

用于多宿主 SCTP 关联的 NAT 在相应的内核模块中需要特殊的逻辑。
{{< /warning >}}

<!--
##### Windows {#caveat-sctp-windows-os}

{{< note >}}
SCTP is not supported on Windows based nodes.
{{< /note >}}
-->
##### Windows {#caveat-sctp-windows-os}

{{< note >}}
基于 Windows 的节点不支持 SCTP。
{{< /note >}}

<!--
##### Userspace kube-proxy {#caveat-sctp-kube-proxy-userspace}

{{< warning >}}
The kube-proxy does not support the management of SCTP associations when it is in userspace mode.
{{< /warning >}}
-->
##### 用户空间 kube-proxy {#caveat-sctp-kube-proxy-userspace}

{{< warning >}}
当 kube-proxy 处于用户空间模式时，它不支持 SCTP 关联的管理。
{{< /warning >}}

### HTTP

<!--
If your cloud provider supports it, you can use a Service in LoadBalancer mode
to set up external HTTP / HTTPS reverse proxying, forwarded to the Endpoints
of the Service.
-->
如果你的云提供商支持它，则可以在 LoadBalancer 模式下使用服务来设置外部
HTTP/HTTPS 反向代理，并将其转发到该服务的 Endpoints。

<!--
You can also use {{< glossary_tooltip term_id="ingress" >}} in place of Service
to expose HTTP / HTTPS Services.
-->
{{< note >}}
你还可以使用 {{< glossary_tooltip text="Ingress" term_id="ingress" >}} 代替
Service 来公开 HTTP/HTTPS 服务。
{{< /note >}}

<!--
### PROXY protocol

If your cloud provider supports it,
you can use a Service in LoadBalancer mode to configure a load balancer outside
of Kubernetes itself, that will forward connections prefixed with
[PROXY protocol](https://www.haproxy.org/download/1.8/doc/proxy-protocol.txt).

The load balancer will send an initial series of octets describing the
incoming connection, similar to this example
-->
### PROXY 协议

如果你的云提供商支持它，
则可以在 LoadBalancer 模式下使用 Service 在 Kubernetes 本身之外配置负载均衡器，
该负载均衡器将转发前缀为
[PROXY 协议](https://www.haproxy.org/download/1.8/doc/proxy-protocol.txt)
的连接。

负载平衡器将发送一系列初始字节，描述传入的连接，类似于此示例

```
PROXY TCP4 192.0.2.202 10.0.42.7 12345 7\r\n
```

<!--
followed by the data from the client.
-->
上述是来自客户端的数据。

## {{% heading "whatsnext" %}}

<!--
* Read [Connecting Applications with Services](/docs/concepts/services-networking/connect-applications-service/)
* Read about [Ingress](/docs/concepts/services-networking/ingress/)
* Read about [Endpoint Slices](/docs/concepts/services-networking/endpoint-slices/)
-->
* 阅读[使用服务访问应用](/zh/docs/concepts/services-networking/connect-applications-service/)
* 阅读了解 [Ingress](/zh/docs/concepts/services-networking/ingress/)
* 阅读了解[端点切片（Endpoint Slices）](/zh/docs/concepts/services-networking/endpoint-slices/)
