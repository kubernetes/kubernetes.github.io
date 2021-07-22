---
title: 访问集群
weight: 20
content_type: concept
---

<!--
title: Accessing Clusters
weight: 20
content_type: concept
-->

<!-- overview -->

<!--
This topic discusses multiple ways to interact with clusters.
-->
本文阐述多种与集群交互的方法。

{{< toc >}}

<!-- body -->

<!--
## Accessing for the first time with kubectl

When accessing the Kubernetes API for the first time, we suggest using the
Kubernetes CLI, `kubectl`.

To access a cluster, you need to know the location of the cluster and have credentials
to access it.  Typically, this is automatically set-up when you work through
a [Getting started guide](/docs/setup/),
or someone else setup the cluster and provided you with credentials and a location.

Check the location and credentials that kubectl knows about with this command:
-->
## 使用 kubectl 完成集群的第一次访问

当你第一次访问 Kubernetes API 的时候，我们建议你使用 Kubernetes CLI，`kubectl`。

访问集群时，你需要知道集群的地址并且拥有访问的凭证。通常，这些在你通过
[启动安装](/zh/docs/setup/)安装集群时都是自动安装好的，或者其他人安装时
也应该提供了凭证和集群地址。

通过以下命令检查 kubectl 是否知道集群地址及凭证：

```shell
kubectl config view
```

<!--
Many of the [examples](/docs/user-guide/kubectl-cheatsheet) provide an introduction to using
kubectl and complete documentation is found in the [kubectl manual](/docs/user-guide/kubectl-overview).
-->
有许多 [例子](/zh/docs/reference/kubectl/cheatsheet/) 介绍了如何使用 kubectl，
可以在 [kubectl手册](/zh/docs/reference/kubectl/overview/) 中找到更完整的文档。

<!--
## Directly accessing the REST API

Kubectl handles locating and authenticating to the apiserver.
If you want to directly access the REST API with an http client like
curl or wget, or a browser, there are several ways to locate and authenticate:

  - Run kubectl in proxy mode.
    - Recommended approach.
    - Uses stored apiserver location.
    - Verifies identity of apiserver using self-signed cert.  No MITM possible.
    - Authenticates to apiserver.
    - In future, may do intelligent client-side load-balancing and failover.
  - Provide the location and credentials directly to the http client.
    - Alternate approach.
    - Works with some types of client code that are confused by using a proxy.
    - Need to import a root cert into your browser to protect against MITM.
-->
## 直接访问 REST API

Kubectl 处理 apiserver 的定位和身份验证。
如果要使用 curl 或 wget 等 http 客户端或浏览器直接访问 REST API，可以通过
多种方式查找和验证：

- 以代理模式运行 kubectl。
  - 推荐此方式。
  - 使用已存储的 apiserver 地址。
  - 使用自签名的证书来验证 apiserver 的身份。杜绝 MITM 攻击。
  - 对 apiserver 进行身份验证。
  - 未来可能会实现智能化的客户端负载均衡和故障恢复。
- 直接向 http 客户端提供位置和凭据。
  - 可选的方案。
  - 适用于代理可能引起混淆的某些客户端类型。
  - 需要引入根证书到你的浏览器以防止 MITM 攻击。

<!--
### Using kubectl proxy

The following command runs kubectl in a mode where it acts as a reverse proxy.  It handles
locating the apiserver and authenticating.
Run it like this:
-->
### 使用 kubectl proxy

以下命令以反向代理的模式运行 kubectl。它处理 apiserver 的定位和验证。
像这样运行：

```shell
kubectl proxy --port=8080 &
```

<!--
See [kubectl proxy](/docs/reference/generated/kubectl/kubectl-commands/#proxy) for more details.

Then you can explore the API with curl, wget, or a browser, replacing localhost
with [::1] for IPv6, like so:
-->
参阅 [kubectl proxy](/docs/reference/generated/kubectl/kubectl-commands/#proxy)
获取更多详细信息。

然后，你可以使用 curl、wget 或浏览器访问 API，如果是 IPv6 则用 [::1] 替换 localhost，
如下所示：

```shell
curl http://localhost:8080/api/
```
```json
{
  "kind": "APIVersions",
  "versions": [
    "v1"
  ],
  "serverAddressByClientCIDRs": [
    {
      "clientCIDR": "0.0.0.0/0",
      "serverAddress": "10.0.1.149:443"
    }
  ]
}
```

<!--
### Without kubectl proxy

In Kubernetes version 1.3 or later, `kubectl config view` no longer displays the token. Use `kubectl describe secret...` to get the token for the default service account, like this:
-->
### 不使用 kubectl proxy

在 Kubernetes 1.3 或更高版本中，`kubectl config view` 不再显示 token。
使用 `kubectl describe secret ...` 来获取默认服务帐户的 token，如下所示：

`grep/cut` 方法实现：

```shell
APISERVER=$(kubectl config view | grep server | cut -f 2- -d ":" | tr -d " ")
TOKEN=$(kubectl describe secret $(kubectl get secrets | grep default | cut -f1 -d ' ') | grep -E '^token' | cut -f2 -d':' | tr -d ' ')
curl $APISERVER/api --header "Authorization: Bearer $TOKEN" --insecure
```
```json
{
  "kind": "APIVersions",
  "versions": [
    "v1"
  ],
  "serverAddressByClientCIDRs": [
    {
      "clientCIDR": "0.0.0.0/0",
      "serverAddress": "10.0.1.149:443"
    }
  ]
}
```

`jsonpath` 方法实现：

```shell
APISERVER=$(kubectl config view --minify -o jsonpath='{.clusters[0].cluster.server}')
TOKEN=$(kubectl get secret $(kubectl get serviceaccount default -o jsonpath='{.secrets[0].name}') -o jsonpath='{.data.token}' | base64 --decode )
curl $APISERVER/api --header "Authorization: Bearer $TOKEN" --insecure
```

```json
{
  "kind": "APIVersions",
  "versions": [
    "v1"
  ],
  "serverAddressByClientCIDRs": [
    {
      "clientCIDR": "0.0.0.0/0",
      "serverAddress": "10.0.1.149:443"
    }
  ]
}
```

<!--
The above examples use the `--insecure` flag.  This leaves it subject to MITM
attacks.  When kubectl accesses the cluster it uses a stored root certificate
and client certificates to access the server.  (These are installed in the
`~/.kube` directory).  Since cluster certificates are typically self-signed, it
may take special configuration to get your http client to use root
certificate.

On some clusters, the apiserver does not require authentication; it may serve
on localhost, or be protected by a firewall.  There is not a standard
for this.  [Configuring Access to the API](/docs/admin/accessing-the-api)
describes how a cluster admin can configure this.  Such approaches may conflict
with future high-availability support.
-->
上面的例子使用了 `--insecure` 参数，这使得它很容易受到 MITM 攻击。
当 kubectl 访问集群时，它使用存储的根证书和客户端证书来访问服务器
（它们安装在 `~/.kube` 目录中）。
由于集群证书通常是自签名的，因此可能需要特殊配置才能让你的 http 客户端使用根证书。

在一些集群中，apiserver 不需要身份验证；它可能只服务于 localhost，或者被防火墙保护，
这个没有一定的标准。
[配置对 API 的访问](/zh/docs/concepts/security/controlling-access/)
描述了集群管理员如何进行配置。此类方法可能与未来的高可用性支持相冲突。

<!--
## Programmatic access to the API

Kubernetes officially supports [Go](#go-client) and [Python](#python-client)
client libraries.

### Go client

* To get the library, run the following command: `go get k8s.io/client-go/<version number>/kubernetes`. See [https://github.com/kubernetes/client-go](https://github.com/kubernetes/client-go) to see which versions are supported.
* Write an application atop of the client-go clients. Note that client-go defines its own API objects, so if needed, please import API definitions from client-go rather than from the main repository, e.g., `import "k8s.io/client-go/1.4/pkg/api/v1"` is correct.

The Go client can use the same [kubeconfig file](/docs/concepts/configuration/organize-cluster-access-kubeconfig/)
as the kubectl CLI does to locate and authenticate to the apiserver. See this [example](https://git.k8s.io/client-go/examples/out-of-cluster-client-configuration/main.go).

If the application is deployed as a Pod in the cluster, please refer to the [next section](#accessing-the-api-from-a-pod).
-->
## 以编程方式访问 API

Kubernetes 官方提供对 [Go](#go-client) 和 [Python](#python-client) 的客户端库支持。

### Go 客户端

* 想要获得这个库，请运行命令：`go get k8s.io/client-go/<version number>/kubernetes`。
  参阅 [https://github.com/kubernetes/client-go](https://github.com/kubernetes/client-go)
  来查看目前支持哪些版本。
* 基于这个 client-go 客户端库编写应用程序。
  请注意，client-go 定义了自己的 API 对象，因此如果需要，请从 client-go 而不是从主存储库
  导入 API 定义，例如，`import "k8s.io/client-go/1.4/pkg/api/v1"` 才是对的。

Go 客户端可以像 kubectl CLI 一样使用相同的
[kubeconfig 文件](/zh/docs/concepts/configuration/organize-cluster-access-kubeconfig/)
来定位和验证 apiserver。可参阅
[示例](https://git.k8s.io/client-go/examples/out-of-cluster-client-configuration/main.go)。

如果应用程序以 Pod 的形式部署在集群中，那么请参阅
[下一章](#accessing-the-api-from-a-pod)。

<!--
### Python client

To use [Python client](https://github.com/kubernetes-client/python), run the following command: `pip install kubernetes`. See [Python Client Library page](https://github.com/kubernetes-client/python) for more installation options.

The Python client can use the same [kubeconfig file](/docs/concepts/cluster-administration/authenticate-across-clusters-kubeconfig/)
as the kubectl CLI does to locate and authenticate to the apiserver. See this [example](https://github.com/kubernetes-client/python/tree/master/examples).

### Other languages

There are [client libraries](/docs/reference/using-api/client-libraries/) for accessing the API from other languages.
See documentation for other libraries for how they authenticate.
-->
### Python 客户端

如果想要使用 [Python 客户端](https://github.com/kubernetes-client/python)，
请运行命令：`pip install kubernetes`。参阅
[Python Client Library page](https://github.com/kubernetes-client/python)
以获得更详细的安装参数。

Python 客户端可以像 kubectl CLI 一样使用相同的
[kubeconfig 文件](/zh/docs/concepts/configuration/organize-cluster-access-kubeconfig/)
来定位和验证 apiserver，可参阅
[示例](https://github.com/kubernetes-client/python/tree/master/examples)。

### 其它语言

目前有多个[客户端库](/zh/docs/reference/using-api/client-libraries/)
为其它语言提供访问 API 的方法。
参阅其它库的相关文档以获取他们是如何验证的。

<!--
## Accessing the API from a Pod

When accessing the API from a pod, locating and authenticating
to the apiserver are somewhat different.

The recommended way to locate the apiserver within the pod is with
the `kubernetes.default.svc` DNS name, which resolves to a Service IP which in turn
will be routed to an apiserver.

The recommended way to authenticate to the apiserver is with a
[service account](/docs/tasks/configure-pod-container/configure-service-account/) credential. By kube-system, a pod
is associated with a service account, and a credential (token) for that
service account is placed into the filesystem tree of each container in that pod,
at `/var/run/secrets/kubernetes.io/serviceaccount/token`.
-->
### 从 Pod 中访问 API   {#accessing-the-api-from-a-pod}

当你从 Pod 中访问 API 时，定位和验证 apiserver 会有些许不同。

在 Pod 中定位 apiserver 的推荐方式是通过 `kubernetes.default.svc`
这个 DNS 名称，该名称将会解析为服务 IP，然后服务 IP 将会路由到 apiserver。

向 apiserver 进行身份验证的推荐方法是使用
[服务帐户](/zh/docs/tasks/configure-pod-container/configure-service-account/) 凭据。
通过 kube-system，Pod 与服务帐户相关联，并且该服务帐户的凭证（token）
被放置在该 Pod 中每个容器的文件系统中，位于
`/var/run/secrets/kubernetes.io/serviceaccount/token`。

<!--
If available, a certificate bundle is placed into the filesystem tree of each
container at `/var/run/secrets/kubernetes.io/serviceaccount/ca.crt`, and should be
used to verify the serving certificate of the apiserver.

Finally, the default namespace to be used for namespaced API operations is placed in a file
at `/var/run/secrets/kubernetes.io/serviceaccount/namespace` in each container.
-->
如果可用，则将证书放入每个容器的文件系统中的
`/var/run/secrets/kubernetes.io/serviceaccount/ca.crt`，
并且应该用于验证 apiserver 的服务证书。

最后，名字空间作用域的 API 操作所使用的 default 名字空间将被放置在
每个容器的 `/var/run/secrets/kubernetes.io/serviceaccount/namespace`
文件中。

<!--
From within a pod the recommended ways to connect to API are:

  - run `kubectl proxy` in a sidecar container in the pod, or as a background
    process within the container. This proxies the
    Kubernetes API to the localhost interface of the pod, so that other processes
    in any container of the pod can access it.
  - use the Go client library, and create a client using the `rest.InClusterConfig()` and `kubernetes.NewForConfig()` functions.
    They handle locating and authenticating to the apiserver. [example](https://git.k8s.io/client-go/examples/in-cluster-client-configuration/main.go)

In each case, the credentials of the pod are used to communicate securely with the apiserver.
-->
在 Pod 中，建议连接 API 的方法是：

- 在 Pod 的边车容器中运行 `kubectl proxy`，或者以后台进程的形式运行。
  这将把 Kubernetes API 代理到当前 Pod 的 localhost 接口，
  所以 Pod 中的所有容器中的进程都能访问它。
- 使用 Go 客户端库，并使用 `rest.InClusterConfig()` 和
  `kubernetes.NewForConfig()` 函数创建一个客户端。
  他们处理 apiserver 的定位和身份验证。
  [示例](https://git.k8s.io/client-go/examples/in-cluster-client-configuration/main.go)

在每种情况下，Pod 的凭证都是为了与 apiserver 安全地通信。

<!--
## Accessing services running on the cluster

The previous section was about connecting the Kubernetes API server.  This section is about
connecting to other services running on Kubernetes cluster.  In Kubernetes, the
[nodes](/docs/admin/node), [pods](/docs/user-guide/pods) and [services](/docs/user-guide/services) all have
their own IPs.  In many cases, the node IPs, pod IPs, and some service IPs on a cluster will not be
routable, so they will not be reachable from a machine outside the cluster,
such as your desktop machine.
-->
## 访问集群中正在运行的服务  {#accessing-services-running-on-the-cluster}

上一节介绍了如何连接 Kubernetes API 服务。本节介绍如何连接到 Kubernetes
集群上运行的其他服务。
在 Kubernetes 中，[节点](/zh/docs/concepts/architecture/nodes/)、
[pods](/zh/docs/concepts/workloads/pods/) 和
[服务](/zh/docs/concepts/services-networking/service/) 都有自己的 IP。
在许多情况下，集群上的节点 IP、Pod IP 和某些服务 IP 将无法路由，
因此无法从集群外部的计算机（例如桌面计算机）访问它们。

<!--
### Ways to connect

You have several options for connecting to nodes, pods and services from outside the cluster:

  - Access services through public IPs.
    - Use a service with type `NodePort` or `LoadBalancer` to make the service reachable outside
      the cluster.  See the [services](/docs/user-guide/services) and
      [kubectl expose](/docs/reference/generated/kubectl/kubectl-commands/#expose) documentation.
    - Depending on your cluster environment, this may only expose the service to your corporate network,
      or it may expose it to the internet.  Think about whether the service being exposed is secure.
      Does it do its own authentication?
    - Place pods behind services.  To access one specific pod from a set of replicas, such as for debugging,
      place a unique label on the pod and create a new service which selects this label.
    - In most cases, it should not be necessary for application developer to directly access
      nodes via their nodeIPs.
-->
### 连接的方法   {#ways-to-connect}

有多种方式可以从集群外部连接节点、Pod 和服务：

- 通过公共 IP 访问服务。

  - 类型为 `NodePort` 或 `LoadBalancer` 的服务，集群外部可以访问。
    请参阅 [服务](/zh/docs/concepts/services-networking/service/) 和
    [kubectl expose](/docs/reference/generated/kubectl/kubectl-commands/#expose) 文档。
  - 取决于你的集群环境，该服务可能仅暴露给你的公司网络，或者也可能暴露给
    整个互联网。
    请考虑公开该服务是否安全。它是否进行自己的身份验证？
  - 在服务后端放置 Pod。要从一组副本中访问一个特定的 Pod，例如进行调试，
    请在 Pod 上设置一个唯一的标签，然后创建一个选择此标签的新服务。
  - 在大多数情况下，应用程序开发人员不应该通过其 nodeIP 直接访问节点。

<!--
  - Access services, nodes, or pods using the Proxy Verb.
    - Does apiserver authentication and authorization prior to accessing the remote service.
      Use this if the services are not secure enough to expose to the internet, or to gain
      access to ports on the node IP, or for debugging.
    - Proxies may cause problems for some web applications.
    - Only works for HTTP/HTTPS.
    - Described [here](#manually-constructing-apiserver-proxy-urls).
-->
- 使用 proxy 动态访问服务、节点或者 Pod。
  - 在访问远程服务之前进行 apiserver 身份验证和授权。
    如果服务不能够安全地暴露到互联网，或者服务不能获得节点 IP 端口的
    访问权限，或者是为了调试，那么请使用此选项。
  - 代理可能会给一些 web 应用带来问题。
  - 只适用于 HTTP/HTTPS。
  - 更多详细信息在[这里](#manually-constructing-apiserver-proxy-urls)。

<!--
  - Access from a node or pod in the cluster.
    - Run a pod, and then connect to a shell in it using [kubectl exec](/docs/reference/generated/kubectl/kubectl-commands/#exec).
      Connect to other nodes, pods, and services from that shell.
    - Some clusters may allow you to ssh to a node in the cluster.  From there you may be able to
      access cluster services.  This is a non-standard method, and will work on some clusters but
      not others.  Browsers and other tools may or may not be installed.  Cluster DNS may not work.
-->
- 从集群中的节点或者 Pod 中访问。

  - 运行一个 Pod，然后使用 [kubectl exec](/docs/reference/generated/kubectl/kubectl-commands/#exec)
    来连接 Pod 里的 Shell。
    然后从 Shell 中连接其它的节点、Pod 和服务。
  - 有些集群可能允许你通过 SSH 连接到节点，从那你可能可以访问集群的服务。
    这是一个非正式的方式，可能可以运行在个别的集群上。
    浏览器和其它一些工具可能没有被安装。集群的 DNS 可能无法使用。

<!--
### Discovering builtin services

Typically, there are several services which are started on a cluster by kube-system. Get a list of these
with the `kubectl cluster-info` command:
-->
### 发现内建服务

通常来说，集群中会有 kube-system 创建的一些运行的服务。

通过 `kubectl cluster-info` 命令获得这些服务列表：

```shell
kubectl cluster-info
```

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
at `https://104.197.5.247/api/v1/namespaces/kube-system/services/elasticsearch-logging/proxy/` if suitable credentials are passed.  Logging can also be reached through a kubectl proxy, for example at:
`http://localhost:8080/api/v1/namespaces/kube-system/services/elasticsearch-logging/proxy/`.
(See [Access Clusters Using the Kubernetes API](/docs/tasks/administer-cluster/access-cluster-api/) for how to pass credentials or use kubectl proxy.)
-->
这展示了访问每个服务的 proxy-verb URL。
例如，如果集群启动了集群级别的日志（使用 Elasticsearch），并且传递合适的凭证，
那么可以通过
`https://104.197.5.247/api/v1/namespaces/kube-system/services/elasticsearch-logging/proxy/`
进行访问。日志也能通过 kubectl 代理获取，例如：
`http://localhost:8080/api/v1/namespaces/kube-system/services/elasticsearch-logging/proxy/`。
（参阅[使用 Kubernetes API 访问集群](/zh/docs/tasks/administer-cluster/access-cluster-api/)
了解如何传递凭据，或者使用 kubectl proxy）
<!--
#### Manually constructing apiserver proxy URLs

As mentioned above, you use the `kubectl cluster-info` command to retrieve the service's proxy URL. To create proxy URLs that include service endpoints, suffixes, and parameters, you append to the service's proxy URL:
`http://`*`kubernetes_master_address`*`/api/v1/namespaces/`*`namespace_name`*`/services/`*`service_name[:port_name]`*`/proxy`

If you haven't specified a name for your port, you don't have to specify *port_name* in the URL. You can also use the port number in place of the *port_name* for both named and unnamed ports.

By default, the API server proxies to your service using http. To use https, prefix the service name with `https:`:
`http://`*`kubernetes_master_address`*`/api/v1/namespaces/`*`namespace_name`*`/services/`*`https:service_name:[port_name]`*`/proxy`

The supported formats for the name segment of the URL are:

* `<service_name>` - proxies to the default or unnamed port using http
* `<service_name>:<port_name>` - proxies to the specified port name or port number using http
* `https:<service_name>:` - proxies to the default or unnamed port using https (note the trailing colon)
* `https:<service_name>:<port_name>` - proxies to the specified port name or port number using https
-->
#### 手动构建 apiserver 代理 URL {#manually-constructing-apiserver-proxy-urls}

如上所述，你可以使用 `kubectl cluster-info` 命令来获得服务的代理 URL。
要创建包含服务端点、后缀和参数的代理 URL，需添加到服务的代理 URL：
`http://`*`kubernetes_master_address`*`/api/v1/namespaces/`*`namespace_name`*`/services/`*`service_name[:port_name]`*`/proxy`

如果尚未为端口指定名称，则不必在 URL 中指定 *port_name*。
对于已命名和未命名的端口，也可以使用端口号代替 *port_name*。

默认情况下，API server 使用 HTTP 代理你的服务。
要使用 HTTPS，请在服务名称前加上 `https:`：
`http://`*`kubernetes_master_address`*`/api/v1/namespaces/`*`namespace_name`*`/services/`*`https:service_name:[port_name]`*`/proxy`

URL 名称段支持的格式为：

* `<service_name>` - 使用 http 代理到默认或未命名的端口
* `<service_name>:<port_name>` - 使用 http 代理到指定的端口名称或端口号
* `https:<service_name>:` - 使用 https 代理到默认或未命名的端口（注意后面的冒号）
* `https:<service_name>:<port_name>` - 使用 https 代理到指定的端口名称或端口号

<!--
##### Examples

 * To access the Elasticsearch service endpoint `_search?q=user:kimchy`, you would use:   `http://104.197.5.247/api/v1/namespaces/kube-system/services/elasticsearch-logging/proxy/_search?q=user:kimchy`
 * To access the Elasticsearch cluster health information `_cluster/health?pretty=true`, you would use:   `https://104.197.5.247/api/v1/namespaces/kube-system/services/elasticsearch-logging/proxy/_cluster/health?pretty=true`
-->
##### 示例

* 要访问 Elasticsearch  服务端点 `_search?q=user:kimchy`，你需要使用：
  `http://104.197.5.247/api/v1/namespaces/kube-system/services/elasticsearch-logging/proxy/_search?q=user:kimchy`
* 要访问 Elasticsearch 集群健康信息 `_cluster/health?pretty=true`，你需要使用：
  `https://104.197.5.247/api/v1/namespaces/kube-system/services/elasticsearch-logging/proxy/_cluster/health?pretty=true`

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
### Using web browsers to access services running on the cluster

You may be able to put an apiserver proxy url into the address bar of a browser. However:

  - Web browsers cannot usually pass tokens, so you may need to use basic (password) auth.  Apiserver can be configured to accept basic auth,
    but your cluster may not be configured to accept basic auth.
  - Some web apps may not work, particularly those with client side javascript that construct urls in a
    way that is unaware of the proxy path prefix.
-->
### 使用 web 浏览器访问运行在集群上的服务

你可以在浏览器地址栏中输入 apiserver 代理 URL。但是：

- Web 浏览器通常不能传递令牌，因此你可能需要使用基本（密码）身份验证。
  Apiserver 可以配置为接受基本身份验证，但你的集群可能未进行配置。
- 某些 Web 应用程序可能无法运行，尤其是那些使用客户端 javascript 
  以不知道代理路径前缀的方式构建 URL 的应用程序。

<!--
## Requesting redirects

The redirect capabilities have been deprecated and removed.  Please use a proxy (see below) instead.
-->
## 请求重定向

重定向功能已弃用并被删除。请改用代理（见下文）。

<!--
## So Many Proxies

There are several different proxies you may encounter when using Kubernetes:

1.  The [kubectl proxy](#directly-accessing-the-rest-api):

    - runs on a user's desktop or in a pod
    - proxies from a localhost address to the Kubernetes apiserver
    - client to proxy uses HTTP
    - proxy to apiserver uses HTTPS
    - locates apiserver
    - adds authentication headers

-->
## 多种代理

使用 Kubernetes 时可能会遇到几种不同的代理：

1. [kubectl 代理](#directly-accessing-the-rest-api)：

   - 在用户的桌面或 Pod 中运行
   - 代理从本地主机地址到 Kubernetes apiserver
   - 客户端到代理将使用 HTTP
   - 代理到 apiserver 使用 HTTPS
   - 定位 apiserver
   - 添加身份验证头部

<!--
1.  The [apiserver proxy](#discovering-builtin-services):

    - is a bastion built into the apiserver
    - connects a user outside of the cluster to cluster IPs which otherwise might not be reachable
    - runs in the apiserver processes
    - client to proxy uses HTTPS (or http if apiserver so configured)
    - proxy to target may use HTTP or HTTPS as chosen by proxy using available information
    - can be used to reach a Node, Pod, or Service
    - does load balancing when used to reach a Service
-->
2. [apiserver 代理](#discovering-builtin-services)：

   - 内置于 apiserver 中
   - 将集群外部的用户连接到集群 IP，否则这些 IP 可能无法访问
   - 运行在 apiserver 进程中
   - 客户端代理使用 HTTPS（也可配置为 http）
   - 代理将根据可用的信息决定使用 HTTP 或者 HTTPS 代理到目标
   - 可用于访问节点、Pod 或服务
   - 在访问服务时进行负载平衡

<!--
1.  The [kube proxy](/docs/concepts/services-networking/service/#ips-and-vips):

    - runs on each node
    - proxies UDP and TCP
    - does not understand HTTP
    - provides load balancing
    - is only used to reach services
-->
3. [kube proxy](/zh/docs/concepts/services-networking/service/#ips-and-vips)：

   - 运行在每个节点上
   - 代理 UDP 和 TCP
   - 不能代理 HTTP
   - 提供负载均衡
   - 只能用来访问服务

<!--
1.  A Proxy/Load-balancer in front of apiserver(s):

    - existence and implementation varies from cluster to cluster (e.g. nginx)
    - sits between all clients and one or more apiservers
    - acts as load balancer if there are several apiservers.
-->
4. 位于 apiserver 之前的 Proxy/Load-balancer：

   - 存在和实现因集群而异（例如 nginx）
   - 位于所有客户和一个或多个 apiserver 之间
   - 如果有多个 apiserver，则充当负载均衡器

<!--
1.  Cloud Load Balancers on external services:

    - are provided by some cloud providers (e.g. AWS ELB, Google Cloud Load Balancer)
    - are created automatically when the Kubernetes service has type `LoadBalancer`
    - use UDP/TCP only
    - implementation varies by cloud provider.

Kubernetes users will typically not need to worry about anything other than the first two types.  The cluster admin
will typically ensure that the latter types are setup correctly.
-->
5. 外部服务上的云负载均衡器：

   - 由一些云提供商提供（例如 AWS ELB，Google Cloud Load Balancer）
   - 当 Kubernetes 服务类型为 `LoadBalancer` 时自动创建
   - 只使用 UDP/TCP
   - 具体实现因云提供商而异。

除了前两种类型之外，Kubernetes 用户通常不需要担心任何其他问题。
集群管理员通常会确保后者的正确配置。
