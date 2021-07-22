---
title: 访问集群上运行的服务
content_type: task
---

<!-- overview -->
<!--
This page shows how to connect to services running on the Kubernetes cluster.
-->
本文展示了如何连接 Kubernetes 集群上运行的服务。

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}

<!-- steps -->

<!--
## Accessing services running on the cluster

In Kubernetes, [nodes](/docs/concepts/architecture/nodes/),
[pods](/docs/concepts/workloads/pods/) and [services](/docs/concepts/services-networking/service/) all have
their own IPs.  In many cases, the node IPs, pod IPs, and some service IPs on a cluster will not be
routable, so they will not be reachable from a machine outside the cluster,
such as your desktop machine.
-->
## 访问集群上运行的服务

在 Kubernetes 里，[节点](/zh/docs/concepts/architecture/nodes/)、
[Pod](/zh/docs/concepts/workloads/pods/) 和
[服务](/zh/docs/concepts/services-networking/service/) 都有自己的 IP。
许多情况下，集群上的节点 IP、Pod IP 和某些服务 IP 是路由不可达的，
所以不能从集群之外访问它们，例如从你自己的台式机。

<!--
### Ways to connect

You have several options for connecting to nodes, pods and services from outside the cluster:
-->
### 连接方式   {#ways-to-connect}

你有多种可选方式从集群外连接节点、Pod 和服务：

<!--
  - Access services through public IPs.
    - Use a service with type `NodePort` or `LoadBalancer` to make the service reachable outside
      the cluster.  See the [services](/docs/concepts/services-networking/service/) and
      [kubectl expose](/docs/reference/generated/kubectl/kubectl-commands/#expose) documentation.
    - Depending on your cluster environment, this may just expose the service to your corporate network,
      or it may expose it to the internet.  Think about whether the service being exposed is secure.
      Does it do its own authentication?
    - Place pods behind services.  To access one specific pod from a set of replicas, such as for debugging,
      place a unique label on the pod and create a new service which selects this label.
    - In most cases, it should not be necessary for application developer to directly access
      nodes via their nodeIPs.
-->
- 通过公网 IP 访问服务
  - 使用类型为 `NodePort` 或 `LoadBalancer` 的服务，可以从外部访问它们。
    请查阅[服务](/zh/docs/concepts/services-networking/service/) 和
    [kubectl expose](/docs/reference/generated/kubectl/kubectl-commands/#expose) 文档。
  - 取决于你的集群环境，你可以仅把服务暴露在你的企业网络环境中，也可以将其暴露在
    因特网上。需要考虑暴露的服务是否安全，它是否有自己的用户认证？
  - 将 Pod 放置于服务背后。如果要访问一个副本集合中特定的 Pod，例如用于调试目的，
    请给 Pod 指定一个独特的标签并创建一个新服务选择该标签。
  - 大部分情况下，都不需要应用开发者通过节点 IP 直接访问节点。
<!--
  - Access services, nodes, or pods using the Proxy Verb.
    - Does apiserver authentication and authorization prior to accessing the remote service.
      Use this if the services are not secure enough to expose to the internet, or to gain
      access to ports on the node IP, or for debugging.
    - Proxies may cause problems for some web applications.
    - Only works for HTTP/HTTPS.
    - Described [here](#manually-constructing-apiserver-proxy-urls).
-->
- 通过 Proxy 动词访问服务、节点或者 Pod
  - 在访问远程服务之前，利用 API 服务器执行身份认证和鉴权。
    如果你的服务不够安全，无法暴露到因特网中，或者需要访问节点 IP 上的端口，
    又或者出于调试目的，可使用这种方式。
  - 代理可能给某些应用带来麻烦
  - 此方式仅适用于 HTTP/HTTPS
  - 进一步的描述在[这里](#manually-constructing-apiserver-proxy-urls)
  - 从集群中的 node 或者 pod 访问。
<!--
  - Access from a node or pod in the cluster.
    - Run a pod, and then connect to a shell in it using [kubectl exec](/docs/reference/generated/kubectl/kubectl-commands/#exec).
      Connect to other nodes, pods, and services from that shell.
    - Some clusters may allow you to ssh to a node in the cluster. From there you may be able to
      access cluster services. This is a non-standard method, and will work on some clusters but
      not others. Browsers and other tools may or may not be installed. Cluster DNS may not work.
-->
- 从集群中的一个节点或 Pod 访问
  - 运行一个 Pod，然后使用
    [kubectl exec](/docs/reference/generated/kubectl/kubectl-commands/#exec)
    连接到它的 Shell。从那个 Shell 连接其他的节点、Pod 和 服务
  - 某些集群可能允许你 SSH 到集群中的节点。你可能可以从那儿访问集群服务。
    这是一个非标准的方式，可能在一些集群上能工作，但在另一些上却不能。
    浏览器和其他工具可能已经安装也可能没有安装。集群 DNS 可能不会正常工作。

<!--
### Discovering builtin services

Typically, there are several services which are started on a cluster by kube-system. Get a list of these
with the `kubectl cluster-info` command:
-->
### 发现内置服务   {#discovering-builtin-services}

典型情况下，kube-system 名字空间中会启动集群的几个服务。
使用 `kubectl cluster-info` 命令获取这些服务的列表：

```shell
kubectl cluster-info
```

<!--
The output is similar to this:
-->
输出类似于：

```
Kubernetes master is running at https://104.197.5.247
elasticsearch-logging is running at https://104.197.5.247/api/v1/namespaces/kube-system/services/elasticsearch-logging/proxy
kibana-logging is running at https://104.197.5.247/api/v1/namespaces/kube-system/services/kibana-logging/proxy
kube-dns is running at https://104.197.5.247/api/v1/namespaces/kube-system/services/kube-dns/proxy
grafana is running at https://104.197.5.247/api/v1/namespaces/kube-system/services/monitoring-grafana/proxy
heapster is running at https://104.197.5.247/api/v1/namespaces/kube-system/services/monitoring-heapster/proxy
```

<!--
This shows the proxy-verb URL for accessing each service.
For example, this cluster has cluster-level logging enabled (using Elasticsearch), which can be reached
at `https://104.197.5.247/api/v1/namespaces/kube-system/services/elasticsearch-logging/proxy/` if suitable credentials are passed, or through a kubectl proxy at, for example:
`http://localhost:8080/api/v1/namespaces/kube-system/services/elasticsearch-logging/proxy/`.
-->
这一输出显示了用 proxy 动词访问每个服务时可用的 URL。例如，此集群
（使用 Elasticsearch）启用了集群层面的日志。如果提供合适的凭据，可以通过
`https://104.197.5.247/api/v1/namespaces/kube-system/services/elasticsearch-logging/proxy/`
访问，或通过一个 `kubectl proxy` 来访问：
`http://localhost:8080/api/v1/namespaces/kube-system/services/elasticsearch-logging/proxy/`。

<!--
See [Access Clusters Using the Kubernetes API](/docs/tasks/administer-cluster/access-cluster-api/#accessing-the-cluster-api) for how to pass credentials or use kubectl proxy.
-->
{{< note >}}
请参阅[使用 Kubernetes API 访问集群](/zh/docs/tasks/administer-cluster/access-cluster-api/#accessing-the-cluster-api)
了解如何传递凭据或如何使用 `kubectl proxy`。
{{< /note >}}

<!--
#### Manually constructing apiserver proxy URLs

As mentioned above, you use the `kubectl cluster-info` command to retrieve the service's proxy URL. To create proxy URLs that include service endpoints, suffixes, and parameters, you simply append to the service's proxy URL:
`http://`*`kubernetes_master_address`*`/api/v1/namespaces/`*`namespace_name`*`/services/`*`[https:]service_name[:port_name]`*`/proxy`

If you haven't specified a name for your port, you don't have to specify *port_name* in the URL.
-->
#### 手动构建 API 服务器代理 URLs   {#manually-constructing-apiserver-proxy-urls}

如前所述，你可以使用 `kubectl cluster-info` 命令取得服务的代理 URL。
为了创建包含服务末端、后缀和参数的代理 URLs，你可以简单地在服务的代理 URL 中添加：
`http://`*`kubernetes_master_address`*`/api/v1/namespaces/`*`namespace_name`*`/services/`*`service_name[:port_name]`*`/proxy`

如果还没有为你的端口指定名称，你可以不用在 URL 中指定 *port_name*。

<!--
##### Examples

* To access the Elasticsearch service endpoint `_search?q=user:kimchy`, you would use:
-->
##### 示例

* 如要访问 Elasticsearch 服务末端 `_search?q=user:kimchy`，你可以使用： 

  ```
  http://104.197.5.247/api/v1/namespaces/kube-system/services/elasticsearch-logging/proxy/_search?q=user:kimchy
  ```

<!--
* To access the Elasticsearch cluster health information `_cluster/health?pretty=true`, you would use:
-->
* 如要访问 Elasticsearch 集群健康信息`_cluster/health?pretty=true`，你会使用：

  ```
  https://104.197.5.247/api/v1/namespaces/kube-system/services/elasticsearch-logging/proxy/_cluster/health?pretty=true` 
  ```

  <!--
  The health information is similar to this:
  -->
  健康信息与下面的例子类似：

  ```json
  {
    "cluster_name" : "kubernetes_logging",
    "status" : "yellow",
    "timed_out" : false,
    "number_of_nodes" : 1,
    "number_of_data_nodes" : 1,
    "active_primary_shards" : 5,
    "active_shards" : 5,
    "relocating_shards" : 0,
    "initializing_shards" : 0,
    "unassigned_shards" : 5
  }
  ```

<!--
* To access the *https* Elasticsearch service health information `_cluster/health?pretty=true`, you would use:
-->
* 要访问 *https* Elasticsearch 服务健康信息 `_cluster/health?pretty=true`，你会使用：

  ```
  https://104.197.5.247/api/v1/namespaces/kube-system/services/https:elasticsearch-logging/proxy/_cluster/health?pretty=true
  ```

<!--
#### Using web browsers to access services running on the cluster

You may be able to put an apiserver proxy URL into the address bar of a browser. However:
-->
#### 通过 Web 浏览器访问集群中运行的服务

你或许能够将 API 服务器代理的 URL 放入浏览器的地址栏，然而：

<!--
- Web browsers cannot usually pass tokens, so you may need to use basic (password) auth. Apiserver can be configured to accept basic auth,
    but your cluster may not be configured to accept basic auth.
- Some web apps may not work, particularly those with client side javascript that construct URLs in a
    way that is unaware of the proxy path prefix.
-->
- Web 服务器通常不能传递令牌，所以你可能需要使用基本（密码）认证。 
  API 服务器可以配置为接受基本认证，但你的集群可能并没有这样配置。
- 某些 Web 应用可能无法工作，特别是那些使用客户端 Javascript 构造 URL 的
  应用，所构造的 URL 可能并不支持代理路径前缀。

