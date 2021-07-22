---
title: 自定义 DNS 服务
content_type: task
min-kubernetes-server-version: v1.12
---
<!--
reviewers:
- bowei
- zihongz
title: Customizing DNS Service
content_type: task
min-kubernetes-server-version: v1.12
-->

<!-- overview -->
<!--
This page explains how to configure your DNS
{{< glossary_tooltip text="Pod(s)" term_id="pod" >}} and customize the
DNS resolution process in your cluster.
-->
本页说明如何配置 DNS {{< glossary_tooltip text="Pod(s)" term_id="pod" >}}，以及定制集群中 DNS 解析过程。

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}

<!--
Your cluster must be running the CoreDNS add-on.
[Migrating to CoreDNS](/docs/tasks/administer-cluster/coredns/#migrating-to-coredns)
explains how to use `kubeadm` to migrate from `kube-dns`.
-->
你的集群必须运行 CoreDNS 插件。
文档[迁移到 CoreDNS](/zh/docs/tasks/administer-cluster/coredns/#migrating-to-coredns)
解释了如何使用 `kubeadm` 从 `kube-dns` 迁移到 CoreDNS。

<!-- steps -->

<!--
## Introduction

DNS is a built-in Kubernetes service launched automatically
using the addon manager
[cluster add-on](https://releases.k8s.io/{{< param "githubbranch" >}}/cluster/addons/README.md).
-->
## 介绍

DNS 是使用[集群插件](https://releases.k8s.io/{{< param "githubbranch" >}}/cluster/addons/README.md)
管理器自动启动的内置的 Kubernetes 服务。

<!--
As of Kubernetes v1.12, CoreDNS is the recommended DNS Server, replacing kube-dns.  If your cluster
originally used kube-dns, you may still have `kube-dns` deployed rather than CoreDNS.
-->
从 Kubernetes v1.12 开始，CoreDNS 是推荐的 DNS 服务器，取代了 kube-dns。 如果
你的集群原来使用 kube-dns，你可能部署的仍然是 `kube-dns` 而不是 CoreDNS。

<!--
Both the CoreDNS and kube-dns Service are named `kube-dns` in the `metadata.name` field.  
This is so that there is greater interoperability with workloads that relied on the legacy `kube-dns` Service name to resolve addresses internal to the cluster. Using a Service named `kube-dns` abstracts away the implementation detail of which DNS provider is running behind that common name.
-->
{{< note >}}
CoreDNS 和 kube-dns 的 Service 都在其 `metadata.name` 字段使用名字 `kube-dns`。
这是为了能够与依靠传统 `kube-dns` 服务名称来解析集群内部地址的工作负载具有更好的互操作性。
使用 `kube-dns` 作为服务名称可以抽离共有名称之后运行的是哪个 DNS 提供程序这一实现细节。
{{< /note >}}

<!--
If you are running CoreDNS as a Deployment, it will typically be exposed as a Kubernetes Service with a static IP address.
The kubelet passes DNS resolver information to each container with the `-cluster-dns=<dns-service-ip>` flag.
-->
如果你在使用 Deployment 运行 CoreDNS，则该 Deployment 通常会向外暴露为一个具有
静态 IP 地址 Kubernetes 服务。
kubelet 使用 `--cluster-dns=<DNS 服务 IP>` 标志将 DNS 解析器的信息传递给每个容器。

<!--
DNS names also need domains. You configure the local domain in the kubelet
with the flag `-cluster-domain=<default-local-domain>`.
-->
DNS 名称也需要域名。 你可在 kubelet 中使用 `--cluster-domain=<默认本地域名>`
标志配置本地域名。

<!--
The DNS server supports forward lookups (A and AAAA records), port lookups (SRV records), reverse IP address lookups (PTR records),
and more. For more information, see [DNS for Services and Pods](/docs/concepts/services-networking/dns-pod-service/).
-->
DNS 服务器支持正向查找（A 和 AAAA 记录）、端口发现（SRV 记录）、反向 IP 地址发现（PTR 记录）等。
更多信息，请参见[Pod 和 服务的 DNS](/zh/docs/concepts/services-networking/dns-pod-service/)。

<!--
If a Pod's `dnsPolicy` is set to "`default`", it inherits the name resolution
configuration from the node that the Pod runs on. The Pod's DNS resolution
should behave the same as the node.
But see [Known issues](/docs/tasks/administer-cluster/dns-debugging-resolution/#known-issues).
-->
如果 Pod 的 `dnsPolicy` 设置为 "`default`"，则它将从 Pod 运行所在节点继承名称解析配置。
Pod 的 DNS 解析行为应该与节点相同。
但请参阅[已知问题](/zh/docs/tasks/administer-cluster/dns-debugging-resolution/#known-issues)。

<!--
If you don't want this, or if you want a different DNS config for pods, you can
use the kubelet's `-resolv-conf` flag.  Set this flag to "" to prevent Pods from
inheriting DNS. Set it to a valid file path to specify a file other than
`/etc/resolv.conf` for DNS inheritance.
-->
如果你不想这样做，或者想要为 Pod 使用其他 DNS 配置，则可以
使用 kubelet 的 `--resolv-conf` 标志。 将此标志设置为 "" 可以避免 Pod 继承 DNS。
将其设置为有别于 `/etc/resolv.conf` 的有效文件路径可以设定 DNS 继承不同的配置。

## CoreDNS

<!--
CoreDNS is a general-purpose authoritative DNS server that can serve as cluster DNS, complying with the [dns specifications]
(https://github.com/kubernetes/dns/blob/master/docs/specification.md).
-->
CoreDNS 是通用的权威 DNS 服务器，可以用作集群 DNS，符合
[DNS 规范](https://github.com/kubernetes/dns/blob/master/docs/specification.md)。

<!--
### CoreDNS ConfigMap options

CoreDNS is a DNS server that is modular and pluggable, and each plugin adds new functionality to CoreDNS.
This can be configured by maintaining a [Corefile](https://coredns.io/2017/07/23/corefile-explained/), which is the CoreDNS
configuration file. A cluster administrator can modify the ConfigMap for the CoreDNS Corefile to change how service discovery works.  
-->
### CoreDNS ConfigMap 选项  {#coredns-configmap-options}

CoreDNS 是模块化且可插拔的 DNS 服务器，每个插件都为 CoreDNS 添加了新功能。
可以通过维护 [Corefile](https://coredns.io/2017/07/23/corefile-explained/)，即 CoreDNS 配置文件，
来定制其行为。 集群管理员可以修改 CoreDNS Corefile 的 ConfigMap，以更改服务发现的工作方式。

<!--
In Kubernetes, CoreDNS is installed with the following default Corefile configuration.
-->
在 Kubernetes 中，CoreDNS 安装时使用如下默认 Corefile 配置。

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: coredns
  namespace: kube-system
data:
  Corefile: |
    .:53 {
        errors
        health {
            lameduck 5s
        }
        ready
        kubernetes cluster.local in-addr.arpa ip6.arpa {
           pods insecure
           fallthrough in-addr.arpa ip6.arpa
           ttl 30
        }
        prometheus :9153
        forward . /etc/resolv.conf
        cache 30
        loop
        reload
        loadbalance
    }
```

<!--
The Corefile configuration includes the following [plugins](https://coredns.io/plugins/) of CoreDNS:
-->
Corefile 配置包括以下 CoreDNS [插件](https://coredns.io/plugins/)：

<!--
* [errors](https://coredns.io/plugins/errors/): Errors are logged to stdout.
* [health](https://coredns.io/plugins/health/): Health of CoreDNS is reported to http://localhost:8080/health.
* [kubernetes](https://coredns.io/plugins/kubernetes/): CoreDNS will reply to DNS queries based on IP of the services and pods of Kubernetes. You can find more details [here](https://coredns.io/plugins/kubernetes/).  
-->
* [errors](https://coredns.io/plugins/errors/)：错误记录到标准输出。
* [health](https://coredns.io/plugins/health/)：在 http://localhost:8080/health 处提供 CoreDNS 的健康报告。
* [ready](https://coredns.io/plugins/ready/)：在端口 8181 上提供的一个 HTTP 末端，当所有能够
  表达自身就绪的插件都已就绪时，在此末端返回 200 OK。
* [kubernetes](https://coredns.io/plugins/kubernetes/)：CoreDNS 将基于 Kubernetes 的服务和 Pod 的
  IP 答复 DNS 查询。你可以在 CoreDNS 网站阅读[更多细节](https://coredns.io/plugins/kubernetes/)。
  你可以使用 `ttl` 来定制响应的 TTL。默认值是 5 秒钟。TTL 的最小值可以是 0 秒钟，
  最大值为 3600 秒。将 TTL 设置为 0 可以禁止对 DNS 记录进行缓存。

  <!--
  The `pods insecure` option is provided for backward compatibility with kube-dns. You can use the
  `pods verified` option, which returns an A record only if there exists a pod in same namespace
  with matching IP. The `pods disabled` option can be used if you don't use pod records.
  -->
  `pods insecure` 选项是为了与 kube-dns 向后兼容。你可以使用 `pods verified` 选项，该选项使得
  仅在相同名称空间中存在具有匹配 IP 的 Pod 时才返回 A 记录。如果你不使用 Pod 记录，则可以使用
  `pods disabled` 选项。

<!--
* [prometheus](https://coredns.io/plugins/prometheus/): Metrics of CoreDNS are available at http://localhost:9153/metrics in [Prometheus](https://prometheus.io/) format.
* [forward](https://coredns.io/plugins/forward/): Any queries that are not within the cluster domain of Kubernetes will be forwarded to predefined resolvers (/etc/resolv.conf).
* [cache](https://coredns.io/plugins/cache/): This enables a frontend cache.
* [loop](https://coredns.io/plugins/loop/): Detects simple forwarding loops and halts the CoreDNS process if a loop is found.
* [reload](https://coredns.io/plugins/reload): Allows automatic reload of a changed Corefile. After you edit the ConfigMap configuration, allow two minutes for your changes to take effect.
* [loadbalance](https://coredns.io/plugins/loadbalance): This is a round-robin DNS loadbalancer that randomizes the order of A, AAAA, and MX records in the answer.
-->
* [prometheus](https://coredns.io/plugins/prometheus/)：CoreDNS 的度量指标值以
  [Prometheus](https://prometheus.io/) 格式在 http://localhost:9153/metrics 上提供。
* [forward](https://coredns.io/plugins/forward/): 不在 Kubernetes 集群域内的任何查询都将转发到
  预定义的解析器 (/etc/resolv.conf).
* [cache](https://coredns.io/plugins/cache/)：启用前端缓存。
* [loop](https://coredns.io/plugins/loop/)：检测到简单的转发环，如果发现死循环，则中止 CoreDNS 进程。
* [reload](https://coredns.io/plugins/reload)：允许自动重新加载已更改的 Corefile。
  编辑 ConfigMap 配置后，请等待两分钟，以使更改生效。
* [loadbalance](https://coredns.io/plugins/loadbalance)：这是一个轮转式 DNS 负载均衡器，
  它在应答中随机分配 A、AAAA 和 MX 记录的顺序。

<!--
You can modify the default CoreDNS behavior by modifying the ConfigMap.
-->
你可以通过修改 ConfigMap 来更改默认的 CoreDNS 行为。

<!--
### Configuration of Stub-domain and upstream nameserver using CoreDNS

CoreDNS has the ability to configure stubdomains and upstream nameservers using the [forward plugin](https://coredns.io/plugins/forward/).
-->
### 使用 CoreDNS 配置存根域和上游域名服务器

CoreDNS 能够使用 [forward 插件](https://coredns.io/plugins/forward/)配置存根域和上游域名服务器。

<!--
#### Example

If a cluster operator has a [Consul](https://www.consul.io/) domain server located at 10.150.0.1, and all Consul names have the suffix .consul.local. To configure it in CoreDNS, the cluster administrator creates the following stanza in the CoreDNS ConfigMap.
-->
#### 示例

如果集群操作员在 10.150.0.1 处运行了 [Consul](https://www.consul.io/) 域服务器，
且所有 Consul 名称都带有后缀 `.consul.local`。要在 CoreDNS 中对其进行配置，
集群管理员可以在 CoreDNS 的 ConfigMap 中创建加入以下字段。

```
consul.local:53 {
        errors
        cache 30
        forward . 10.150.0.1
    }
```

<!--
To explicitly force all non-cluster DNS lookups to go through a specific nameserver at 172.16.0.1, point the  `forward` to the nameserver instead of `/etc/resolv.conf`
-->
要显式强制所有非集群 DNS 查找通过特定的域名服务器（位于 172.16.0.1），可将 `forward`
指向该域名服务器，而不是 `/etc/resolv.conf`。

```
forward .  172.16.0.1
```

<!--
The final ConfigMap along with the default `Corefile` configuration looks like:
-->
最终的包含默认的 `Corefile` 配置的 ConfigMap 如下所示：

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: coredns
  namespace: kube-system
data:
  Corefile: |
    .:53 {
        errors
        health
        kubernetes cluster.local in-addr.arpa ip6.arpa {
           pods insecure
           fallthrough in-addr.arpa ip6.arpa
        }
        prometheus :9153
        forward . 172.16.0.1
        cache 30
        loop
        reload
        loadbalance
    }
    consul.local:53 {
        errors
        cache 30
        forward . 10.150.0.1
    }
```

<!--
The `kubeadm` supports automatic translation of the CoreDNS ConfigMap from the kube-dns ConfigMap.
-->
工具 `kubeadm` 支持将 kube-dns ConfigMap 自动转换为 CoreDNS ConfigMap。

<!--
While kube-dns accepts an FQDN for stubdomain and nameserver (eg: ns.foo.com), CoreDNS does not support this feature.
During translation, all FQDN nameservers will be omitted from the CoreDNS config.***
-->
{{< note >}}
尽管 kube-dns 接受 FQDN（例如：ns.foo.com）作为存根域和名字服务器，CoreDNS 不支持此功能。
转换期间，CoreDNS 配置中将忽略所有的 FQDN 域名服务器。
{{< /note >}}

<!--
## CoreDNS configuration equivalent to kube-dns

CoreDNS supports the features of kube-dns and more.
A ConfigMap created for kube-dns to support `StubDomains`and `upstreamNameservers` translates to the `proxy` plugin in CoreDNS.
Similarly, the `Federations` plugin in kube-dns translates to the `federation` plugin in CoreDNS.

### Example

This example ConfigMap for kubedns specifies federations, stubdomains and upstreamnameservers:
-->
## CoreDNS 配置等同于 kube-dns

CoreDNS 不仅仅提供 kube-dns 的功能。
为 kube-dns 创建的 ConfigMap 支持 `StubDomains` 和 `upstreamNameservers` 转换为 CoreDNS 中的 `forward` 插件。
同样，kube-dns 中的 `Federations` 插件会转换为 CoreDNS 中的 `federation` 插件。

### 示例

用于 kubedns 的此示例 ConfigMap 描述了 federations、stubdomains and upstreamnameservers：

```yaml
apiVersion: v1
data:
  federations: |
    {"foo" : "foo.feddomain.com"}
  stubDomains: |
    {"abc.com" : ["1.2.3.4"], "my.cluster.local" : ["2.3.4.5"]}
  upstreamNameservers: |
    ["8.8.8.8", "8.8.4.4"]
kind: ConfigMap
```

<!--
The equivalent configuration in CoreDNS creates a Corefile:
-->
CoreDNS 中的等效配置将创建一个 Corefile：

* 针对 federations:

  ```yaml
  federation cluster.local {
      foo foo.feddomain.com
  }
  ```

* 针对 stubDomains:

  ```yaml
  abc.com:53 {
       errors
       cache 30
       proxy . 1.2.3.4
   }
   my.cluster.local:53 {
       errors
       cache 30
       proxy . 2.3.4.5
   }
   ```

<!--
The complete Corefile with the default plugins:
-->
带有默认插件的完整 Corefile：

```
.:53 {
    errors
    health
    kubernetes cluster.local in-addr.arpa ip6.arpa {
       pods insecure
       fallthrough in-addr.arpa ip6.arpa
    }
    federation cluster.local {
       foo foo.feddomain.com
    }
    prometheus :9153
    forward .  8.8.8.8 8.8.4.4
    cache 30
}
abc.com:53 {
    errors
    cache 30
    forward . 1.2.3.4
}
my.cluster.local:53 {
    errors
    cache 30
    forward . 2.3.4.5
}
```

<!--
## Migration to CoreDNS

To migrate from kube-dns to CoreDNS, [a detailed blog](https://coredns.io/2018/05/21/migration-from-kube-dns-to-coredns/) is available to help users adapt CoreDNS in place of kube-dns.
A cluster administrator can also migrate using [the deploy script](https://github.com/coredns/deployment/blob/master/kubernetes/deploy.sh).

-->
## 迁移到 CoreDNS

要从 kube-dns 迁移到 CoreDNS，我们提供了一篇详细的[博客](https://coredns.io/2018/05/21/migration-from-kube-dns-to-coredns/)
帮助用户将 kube-dns 替换为 CoreDNS。
集群管理员还可以使用[部署脚本](https://github.com/coredns/deployment/blob/master/kubernetes/deploy.sh)
进行迁移。

## {{% heading "whatsnext" %}}

<!--
- Read [Debugging DNS Resolution](/docs/tasks/administer-cluster/dns-debugging-resolution/).
-->
- 阅读[调试 DNS 解析](/zh/docs/tasks/administer-cluster/dns-debugging-resolution/)
