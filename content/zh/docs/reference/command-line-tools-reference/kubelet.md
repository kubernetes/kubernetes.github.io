---
title: kubelet
content_type: tool-reference
weight: 28
---

## {{% heading "synopsis" %}}


<!--
The kubelet is the primary "node agent" that runs on each
node. It can register the node with the apiserver using one of: the hostname; a flag to override the hostname; or specific logic for a cloud provider.
-->
kubelet 是在每个 Node 节点上运行的主要 “节点代理”。它可以使用以下之一向 apiserver 注册：
主机名（hostname）；覆盖主机名的参数；某云驱动的特定逻辑。

<!--
The kubelet works in terms of a PodSpec. A PodSpec is a YAML or JSON object
that describes a pod. The kubelet takes a set of PodSpecs that are provided through various mechanisms (primarily through the apiserver) and ensures that the containers described in those PodSpecs are running and healthy. The kubelet doesn't manage containers which were not created by Kubernetes.
-->
kubelet 是基于 PodSpec 来工作的。每个 PodSpec 是一个描述 Pod 的 YAML 或 JSON 对象。
kubelet 接受通过各种机制（主要是通过 apiserver）提供的一组 PodSpec，并确保这些
PodSpec 中描述的容器处于运行状态且运行状况良好。
kubelet 不管理不是由 Kubernetes 创建的容器。

<!--
Other than from an PodSpec from the apiserver, there are three ways that a container manifest can be provided to the Kubelet.
-->
除了来自 apiserver 的 PodSpec 之外，还可以通过以下三种方式将容器清单（manifest）提供给 kubelet。

<!--
File: Path passed as a flag on the command line. Files under this path will be monitored periodically for updates. The monitoring period is 20s by default and is configurable via a flag.
-->
文件（File）：利用命令行参数传递路径。kubelet 周期性地监视此路径下的文件是否有更新。
监视周期默认为 20s，且可通过参数进行配置。

<!--
HTTP endpoint: HTTP endpoint passed as a parameter on the command line. This endpoint is checked every 20 seconds (also configurable with a flag).
-->
HTTP 端点（HTTP endpoint）：利用命令行参数指定 HTTP 端点。
此端点的监视周期默认为 20 秒，也可以使用参数进行配置。

<!--
HTTP server: The kubelet can also listen for HTTP and respond to a simple API (underspec'd currently) to submit a new manifest.
-->
HTTP 服务器（HTTP server）：kubelet 还可以侦听 HTTP 并响应简单的 API
（目前没有完整规范）来提交新的清单。

```
kubelet [flags]
```

## {{% heading "options" %}}

   <table style="width: 100%; table-layout: fixed;">
<colgroup>
<col span="1" style="width: 10px;" />
<col span="1" />
</colgroup>
<tbody>

<tr>
<td colspan="2">--add-dir-header</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
If true, adds the file directory to the header
-->
设置为 true 表示将文件目录添加到日志消息的头部
</td>
</tr>

<tr>
<td colspan="2">--address ip&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：0.0.0.0</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
The IP address for the Kubelet to serve on (set to `0.0.0.0` for all IPv4 interfaces and `::` for all IPv6 interfaces)  (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
kubelet 用来提供服务的 IP 地址（设置为<code>0.0.0.0</code> 表示使用所有 IPv4 接口，
设置为 <code>::</code> 表示使用所有 IPv6 接口）。已弃用：应在 <code>--config</code> 所给的
配置文件中进行设置。（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--allowed-unsafe-sysctls strings</td>
</tr>  
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Comma-separated whitelist of unsafe sysctls or unsafe sysctl patterns (ending in `*`). Use these at your own risk. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
用逗号分隔的字符串序列设置允许使用的非安全的 sysctls 或 sysctl 模式（以 <code>*</code> 结尾) 。
使用此参数时风险自担。已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）.
</td>
</tr>

<tr>
<td colspan="2">--alsologtostderr</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
log to standard error as well as files
-->
设置为 true 表示将日志输出到文件的同时输出到 stderr
</td>
</tr>

<tr>
<td colspan="2">--anonymous-auth&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：true</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Enables anonymous requests to the Kubelet server. Requests that are not rejected by another authentication method are treated as anonymous requests. Anonymous requests have a username of `system:anonymous`, and a group name of `system:unauthenticated`. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
设置为 true 表示 kubelet 服务器可以接受匿名请求。未被任何认证组件拒绝的请求将被视为匿名请求。
匿名请求的用户名为 <code>system:anonymous</code>，用户组为 <code>system:unauthenticated</code>。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--authentication-token-webhook</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Use the TokenReview API to determine authentication for bearer tokens. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's --config flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
使用 <code>TokenReview</code> API 对持有者令牌进行身份认证。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--authentication-token-webhook-cache-ttl duration&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：<code>2m0s</code></td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
The duration to cache responses from the webhook token authenticator. (default 2m0s) (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's --config flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
对 Webhook 令牌认证组件所返回的响应的缓存时间。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--authorization-mode string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Authorization mode for Kubelet server. Valid options are `AlwaysAllow` or `Webhook`. `Webhook` mode uses the `SubjectAccessReview` API to determine authorization. (default "AlwaysAllow" when `--config` flag is not provided; "Webhook" when `--config` flag presents.) (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's --config flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
kubelet 服务器的鉴权模式。可选值包括：<code>AlwaysAllow</code>、<code>Webhook</code>。<code>Webhook</code> 模式使用 <code>SubjectAccessReview</code> API 鉴权。
当 <code>--config</code> 参数未被设置时，默认值为 <code>AlwaysAllow</code>，当使用了
<code>--config</code> 时，默认值为 <code>Webhook</code>。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--authorization-webhook-cache-authorized-ttl duration&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：<code>5m0s</code></td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
The duration to cache 'authorized' responses from the webhook authorizer. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
对 Webhook 认证组件所返回的 “Authorized（已授权）” 应答的缓存时间。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--authorization-webhook-cache-unauthorized-ttl duration&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: `30s`-->默认值：<code>30s</code></td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
The duration to cache 'unauthorized' responses from the webhook authorizer. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
对 Webhook 认证组件所返回的 “Unauthorized（未授权）” 应答的缓存时间。
<code>--config</code> 时，默认值为 <code>Webhook</code>。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--azure-container-registry-config string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Path to the file container Azure container registry configuration information.
-->
包含 Azure 容器镜像库配置信息的文件的路径。
</td>
</tr>

<tr>
<td colspan="2">--bootstrap-kubeconfig string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Path to a kubeconfig file that will be used to get client certificate for kubelet. If the file specified by `--kubeconfig` does not exist, the bootstrap kubeconfig is used to request a client certificate from the API server. On success, a kubeconfig file referencing the generated client certificate and key is written to the path specified by `--kubeconfig`. The client certificate and key file will be stored in the directory pointed by `--cert-dir`.
-->
某 kubeconfig 文件的路径，该文件将用于获取 kubelet 的客户端证书。
如果 <code>--kubeconfig</code> 所指定的文件不存在，则使用引导所用 kubeconfig
从 API 服务器请求客户端证书。成功后，将引用生成的客户端证书和密钥的 kubeconfig
写入 --kubeconfig 所指定的路径。客户端证书和密钥文件将存储在 <code>--cert-dir</code>
所指的目录。
</td>
</tr>

<tr>
<td colspan="2">--cert-dir string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: `/var/lib/kubelet/pki`-->默认值：<code>/var/lib/kubelet/pki</code></td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
The directory where the TLS certs are located. If `--tls-cert-file` and `--tls-private-key-file` are provided, this flag will be ignored.
-->
TLS 证书所在的目录。如果设置了 <code>--tls-cert-file</code> 和 <code>--tls-private-key-file</code>，
则此标志将被忽略。
</td>
</tr>

<tr>
<td colspan="2">--cgroup-driver string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!-- Default: `cgroupfs`-->默认值：<code>cgroupfs</code></td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Driver that the kubelet uses to manipulate cgroups on the host.  Possible values: `cgroupfs`, `systemd`. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
kubelet 用来操作本机 cgroup 时使用的驱动程序。支持的选项包括 <code>cgroupfs</code>
和 <code>systemd</code>。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
/td>
</tr>

<tr>
<td colspan="2">--cgroup-root string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: `''`-->默认值：<code>""</code></td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Optional root cgroup to use for pods. This is handled by the container runtime on a best effort basis. Default: '', which means use the container runtime default. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's --config flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
可选的选项，为 Pod 设置根 cgroup。容器运行时会尽可能使用此配置。
默认值 <code>""</code> 意味着将使用容器运行时的默认设置。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--cgroups-per-qos&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!-- Default: `true`-->默认值：<code>true</code></td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Enable creation of QoS cgroup hierarchy, if true top level QoS and pod cgroups are created. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
启用创建 QoS cgroup 层次结构。此值为 true 时 kubelet 为 QoS 和 Pod 创建顶级的 cgroup。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--chaos-chance float</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
If &gt; 0.0, introduce random client errors and latency. Intended for testing. (DEPRECATED: will be removed in a future version.)
-->
如果此值大于 0.0，则引入随机客户端错误和延迟。用于测试。
已启用：将在未来版本中移除。
</td>
</tr>

<tr>
<td colspan="2">--client-ca-file string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
If set, any request presenting a client certificate signed by one of the authorities in the client-ca-file is authenticated with an identity corresponding to the CommonName of the client certificate. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's --config flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
如果设置了此参数，则使用对应文件中机构之一检查请求中所携带的客户端证书。
若客户端证书通过身份认证，则其对应身份为其证书中所设置的 CommonName。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--cloud-config string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
The path to the cloud provider configuration file. Empty string for no configuration file. (DEPRECATED: will be removed in 1.23, in favor of removing cloud providers code from Kubelet.)
-->
云驱动配置文件的路径。空字符串表示没有配置文件。
已弃用：将在 1.23 版本中移除，以便于从 kubelet 中去除云驱动代码。
</td>
</tr>

<tr>
<td colspan="2">--cloud-provider string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
The provider for cloud services. Set to empty string for running with no cloud provider. If set, the cloud provider determines the name of the node (consult cloud provider documentation to determine if and how the hostname is used). (DEPRECATED: will be removed in 1.23, in favor of removing cloud provider code from Kubelet.)
-->
云服务的提供者。设置为空字符串表示在没有云驱动的情况下运行。
如果设置了此标志，则云驱动负责确定节点的名称（参考云提供商文档以确定是否以及如何使用主机名）。
已弃用：将在 1.23 版本中移除，以便于从 kubelet 中去除云驱动代码。
</td>
</tr>

<tr>
<td colspan="2">--cluster-dns strings</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Comma-separated list of DNS server IP address. This value is used for containers DNS server in case of Pods with "dnsPolicy=ClusterFirst". Note: all DNS servers appearing in the list MUST serve the same set of records otherwise name resolution within the cluster may not work correctly. There is no guarantee as to which DNS server may be contacted for name resolution. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
DNS 服务器的 IP 地址，以逗号分隔。此标志值用于 Pod 中设置了 “<code>dnsPolicy=ClusterFirst</code>”
时为容器提供 DNS 服务。注意：列表中出现的所有 DNS 服务器必须包含相同的记录组，
否则集群中的名称解析可能无法正常工作。至于名称解析过程中会牵涉到哪些 DNS 服务器，
这一点无法保证。
<code>--config</code> 时，默认值为 <code>Webhook</code>。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--cluster-domain string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Domain for this cluster. If set, kubelet will configure all containers to search this domain in addition to the host's search domains (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
集群的域名。如果设置了此值，kubelet 除了将主机的搜索域配置到所有容器之外，还会为其
配置所搜这里指定的域名。
<code>--config</code> 时，默认值为 <code>Webhook</code>。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--cni-bin-dir string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!-- Default: `/opt/cni/bin`-->默认值：<code>/opt/cni/bin</code></td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
&lt;Warning: Alpha feature&gt; A comma-separated list of full paths of directories in which to search for CNI plugin binaries. This docker-specific flag only works when container-runtime is set to `docker`.
-->
&lt;警告：alpha 特性&gt; 此值为以逗号分隔的完整路径列表。
kubelet 将在所指定路径中搜索 CNI 插件的可执行文件。
仅当容器运行环境设置为 <code>docker</code> 时，此特定于 docker 的参数才有效。
</td>
</tr>

<tr>
<td colspan="2">--cni-cache-dir string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!-- Default: `/var/lib/cni/cache`-->默认值：<code>/var/lib/cni/cache</code></td>
</tr>
<tr>                                            
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
&lt;Warning: Alpha feature&gt; The full path of the directory in which CNI should store cache files. This docker-specific flag only works when container-runtime is set to `docker`.
-->
&lt;警告：alpha 特性&gt; 此值为一个目录的全路径名。CNI 将在其中缓存文件。
仅当容器运行环境设置为 <code>docker</code> 时，此特定于 docker 的参数才有效。
</td>
</tr>

<tr>
<td colspan="2">--cni-conf-dir string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!-- Default: `/etc/cni/net.d`-->默认值：<code>/etc/cni/net.d</code></td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
&lt;Warning: Alpha feature&gt; The full path of the directory in which to search for CNI config files. This docker-specific flag only works when container-runtime is set to `docker`.
-->
&lt;警告：alpha 特性&gt; 此值为某目录的全路径名。kubelet 将在其中搜索 CNI 配置文件。
仅当容器运行环境设置为 <code>docker</code> 时，此特定于 docker 的参数才有效。
</td>
</tr>

<tr>
<td colspan="2">--config string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
The Kubelet will load its initial configuration from this file. The path may be absolute or relative; relative paths start at the Kubelet's current working directory. Omit this flag to use the built-in default configuration values. Command-line flags override configuration from this file.
-->
kubelet 将从此标志所指的文件中加载其初始配置。此路径可以是绝对路径，也可以是相对路径。
相对路径按 kubelet 的当前工作目录起计。省略此参数时 kubelet 会使用内置的默认配置值。
命令行参数会覆盖此文件中的配置。
</td>
</tr>

<tr>
<td colspan="2">--container-log-max-files int32&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: 5-->默认值：5</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Set the maximum number of container log files that can be present for a container. The number must be &ge; 2. This flag can only be used with `--container-runtime=remote`. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's --config flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
设置容器的日志文件个数上限。此值必须不小于 2。
此标志只能与 <code>--container-runtime=remote</code> 标志一起使用。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>    

<tr>
<td colspan="2">--container-log-max-size string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!-- Default: `10Mi`-->默认值：<code>10Mi</code></td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Set the maximum size (e.g. 10Mi) of container log file before it is rotated. This flag can only be used with `--container-runtime=remote`.  (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's --config flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
设置容器日志文件在轮换生成新文件时之前的最大值（例如，<code>10Mi</code>）。
此标志只能与 <code>--container-runtime=remote</code> 标志一起使用。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--container-runtime string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: `docker`-->默认值：<code>docker</code></td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
The container runtime to use. Possible values: `docker`, `remote`.
-->
要使用的容器运行时。目前支持 <code>docker<code>、</code>remote</code>。
</td>
</tr>

<tr>
<td colspan="2">--container-runtime-endpoint string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: `unix:///var/run/dockershim.sock`-->默认值：<code>unix:///var/run/dockershim.sock</code></td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
[Experimental] The endpoint of remote runtime service. Currently unix socket endpoint is supported on Linux, while npipe and tcp endpoints are supported on windows. Examples: `unix:///var/run/dockershim.sock`, `npipe:////./pipe/dockershim`.
-->
[实验性特性] 远程运行时服务的端点。目前支持 Linux 系统上的 UNIX 套接字和
Windows 系统上的 npipe 和 TCP 端点。例如：
<code>unix:///var/run/dockershim.sock</code>、
<code>npipe:////./pipe/dockershim</code>。
</td>
</tr>

<tr>
<td colspan="2">--contention-profiling</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Enable lock contention profiling, if profiling is enabled (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's --config flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
当启用了性能分析时，启用锁竞争分析。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--cpu-cfs-quota&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: `true`-->默认值：<code>true</code></td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Enable CPU CFS quota enforcement for containers that specify CPU limits (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
为设置了 CPU 限制的容器启用 CPU CFS 配额保障。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--cpu-cfs-quota-period duration&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: `100ms`-->默认值：<code>100ms</code></td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Sets CPU CFS quota period value, `cpu.cfs_period_us`, defaults to Linux Kernel default. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
设置 CPU CFS 配额周期 <code>cpu.cfs_period_us</code>。默认使用 Linux 内核所设置的默认值 。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--cpu-manager-policy string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;默认值：<code>none</code></td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
CPU Manager policy to use. Possible values: 'none', 'static'. Default: 'none' (default "none") (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's --config flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
要使用的 CPU 管理器策略。可选值包括：<code>none</code> 和 <code>static</code>。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--cpu-manager-reconcile-period duration&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: `10s`-->默认值：<code>10s</code></td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
&lt;Warning: Alpha feature&gt; CPU Manager reconciliation period. Examples: `10s`, or `1m`. If not supplied, defaults to node status update frequency. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
&lt;警告：alpha 特性&gt; 设置 CPU 管理器的调和时间。例如：<code>10s</code> 或者 <code>1m</code>。
如果未设置，默认使用节点状态更新频率。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--docker-endpoint string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: `unix:///var/run/docker.sock`-->默认值：<code>unix:///var/run/docker.sock</code></td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Use this for the `docker` endpoint to communicate with. This docker-specific flag only works when container-runtime is set to `docker`.
-->
使用这里的端点与 docker 端点通信。
仅当容器运行环境设置为 <code>docker</code> 时，此特定于 docker 的参数才有效。
</td>
</tr>

<tr>
<td colspan="2">--dynamic-config-dir string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
The Kubelet will use this directory for checkpointing downloaded configurations and tracking configuration health. The Kubelet will create this directory if it does not already exist. The path may be absolute or relative; relative paths start at the Kubelet's current working directory. Providing this flag enables dynamic Kubelet configuration. The `DynamicKubeletConfig` feature gate must be enabled to pass this flag; this gate currently defaults to `true` because the feature is beta.
-->
kubelet 使用此目录来保存所下载的配置，跟踪配置运行状况。
如果目录不存在，则 kubelet 创建该目录。此路径可以是绝对路径，也可以是相对路径。
相对路径从 kubelet 的当前工作目录计算。
设置此参数将启用动态 kubelet 配置。必须启用 <code>DynamicKubeletConfig</code>
特性门控之后才能设置此标志；由于此特性为 beta 阶段，对应的特性门控当前默认为
<code>true</code>。
</td>
</tr>

<tr>
<td colspan="2">--enable-controller-attach-detach&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: `true`-->默认值：<code>true</code></td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Enables the Attach/Detach controller to manage attachment/detachment of volumes scheduled to this node, and disables kubelet from executing any attach/detach operations.
-->
启用 Attach/Detach 控制器来挂接和摘除调度到该节点的卷，同时禁用 kubelet 执行挂接和摘除操作。
</td>
</tr>

<tr>
<td colspan="2">--enable-debugging-handlers&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: `true`</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Enables server endpoints for log collection and local running of containers and commands (default true) (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's --config flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
启用服务器上用于日志收集和在本地运行容器和命令的端点。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--enable-server&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!-- Default: `true`--></td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Enable the Kubelet's server. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
启用 kubelet 服务器。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--enforce-node-allocatable strings&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: `pods`</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
A comma separated list of levels of node allocatable enforcement to be enforced by kubelet. Acceptable options are `none`, `pods`, `system-reserved`, and `kube-reserved`. If the latter two options are specified, `--system-reserved-cgroup` and `--kube-reserved-cgroup` must also be set, respectively. If `none` is specified, no additional options should be set. See https://kubernetes.io/docs/tasks/administer-cluster/reserve-compute-resources/ for more details. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's --config flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
用逗号分隔的列表，包含由 kubelet 强制执行的节点可分配资源级别。
可选配置为：<code>none</code>、<code>pods</code>、<code>system-reserved</code> 和 <code>kube-reserved</code>。
在设置 <code>system-reserved</code> 和 <code>kube-reserved</code> 这两个值时，同时要求设置
<code>--system-reserved-cgroup</code> 和 <code>--kube-reserved-cgroup</code> 这两个参数。
如果设置为 <code>none</code>，则不需要设置其他参数。
<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/reserve-compute-resources/">参考相关文档</a>。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--event-burst int32&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!-- Default: 10-->默认值：10</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Maximum size of a bursty event records, temporarily allows event records to burst to this number, while still not exceeding `--event-qps`. Only used if `--event-qps` &gt; 0. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
事件记录的个数的突发峰值上限，在遵从 <code>--event-qps</code> 阈值约束的前提下
临时允许事件记录达到此数目。仅在 <code>--event-qps</code> 大于 0 时使用。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--event-qps int32&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: 5</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
If &gt; `0`, limit event creations per second to this value. If `0`, unlimited. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
设置大于 0 的值表示限制每秒可生成的事件数量。设置为 0 表示不限制。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--eviction-hard string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: `imagefs.available<15%,memory.available<100Mi,nodefs.available<10%`-->默认值：<code>imagefs.available&lt;15%,memory.available&lt;100Mi,nodefs.available&lt;10%</code></td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
A set of eviction thresholds (e.g. `memory.available<1Gi`) that if met would trigger a pod eviction. On a Linux node, the default value also includes `nodefs.inodesFree<5%`. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
触发 Pod 驱逐操作的一组硬性门限（例如：<code>memory.available&lt;1Gi</code>
（内存可用值小于 1 G））设置。在 Linux 节点上，默认值还包括
<code>nodefs.inodesFree<5%</code>。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--eviction-max-pod-grace-period int32</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Maximum allowed grace period (in seconds) to use when terminating pods in response to a soft eviction threshold being met. If negative, defer to pod specified value. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
响应满足软性驱逐阈值（Soft Eviction Threshold）而终止 Pod 时使用的最长宽限期（以秒为单位）。
如果设置为负数，则遵循 Pod 的指定值。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--eviction-minimum-reclaim mapStringString</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
A set of minimum reclaims (e.g. `imagefs.available=2Gi`) that describes the minimum amount of resource the kubelet will reclaim when performing a pod eviction if that resource is under pressure. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
当某资源压力过大时，kubelet 将执行 Pod 驱逐操作。
此参数设置软性驱逐操作需要回收的资源的最小数量（例如：<code>imagefs.available=2Gi</code>）。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--eviction-pressure-transition-period duration&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: `5m0s`-->默认值：<code>5m0s</code></td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Duration for which the kubelet has to wait before transitioning out of an eviction pressure condition. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
kubelet 在驱逐压力状况解除之前的最长等待时间。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--eviction-soft mapStringString</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
A set of eviction thresholds (e.g. `memory.available>1.5Gi`) that if met over a corresponding grace period would trigger a pod eviction. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
设置一组驱逐阈值（例如：<code>memory.available&lt;1.5Gi</code>）。
如果在相应的宽限期内达到该阈值，则会触发 Pod 驱逐操作。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--eviction-soft-grace-period mapStringString</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
A set of eviction grace periods (e.g. `memory.available=1m30s`) that correspond to how long a soft eviction threshold must hold before triggering a pod eviction. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
设置一组驱逐宽限期（例如，<code>memory.available=1m30s</code>），对应于触发软性 Pod
驱逐操作之前软性驱逐阈值所需持续的时间长短。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--exit-on-lock-contention</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Whether kubelet should exit upon lock-file contention.
-->
设置为 true 表示当发生锁文件竞争时 kubelet 可以退出。
</td>
</tr>

<tr>
<td colspan="2">--experimental-allocatable-ignore-eviction&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: `false`-->默认值：<code>false</code></td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
When set to `true`, Hard eviction thresholds will be ignored while calculating node allocatable. See https://kubernetes.io/docs/tasks/administer-cluster/reserve-compute-resources/ for more details. (DEPRECATED: will be removed in 1.23)
-->
设置为 <code>true</code> 表示在计算节点可分配资源数量时忽略硬性逐出阈值设置。
参考<a href="https://kubernetes.io/docs/tasks/administer-cluster/reserve-compute-resources/">
相关文档</a>。
已启用：将在 1.23 版本中移除。
</td>
</tr>

<tr>
<td colspan="2">--experimental-bootstrap-kubeconfig string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
(DEPRECATED: Use --bootstrap-kubeconfig)
-->
已弃用：应使用 <code>--bootstrap-kubeconfig</code> 标志
</td>
</tr>

<tr>
<td colspan="2">--experimental-check-node-capabilities-before-mount</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
[Experimental] if set to `true`, the kubelet will check the underlying node for required components (binaries, etc.) before performing the mount (DEPRECATED: will be removed in 1.23, in favor of using CSI.)
-->
[实验性特性] 设置为 <code>true</code> 表示 kubelet 在进行挂载卷操作之前要
在本节点上检查所需的组件（如可执行文件等）是否存在。
已弃用：将在 1.23 版本中移除，以便使用 CSI。
</td>
</tr>

<tr>
<td colspan="2">--experimental-kernel-memcg-notification</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
If enabled, the kubelet will integrate with the kernel memcg notification to determine if memory eviction thresholds are crossed rather than polling. This flag will be removed in 1.23. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
设置为 true 表示 kubelet 将会集成内核的 memcg 通知机制而不是使用轮询机制来
判断是否达到了内存驱逐阈值。
此标志将在 1.23 版本移除。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--experimental-log-sanitization</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
[Experimental] When enabled prevents logging of fields tagged as sensitive (passwords, keys, tokens). Runtime log sanitization may introduce significant computation overhead and therefore should not be enabled in production. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's --config flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
[试验性功能] 启用此标志之后，kubelet 会避免将标记为敏感的字段（密码、密钥、令牌等）
写入日志中。运行时的日志清理可能会带来相当的计算开销，因此不应该在
产品环境中启用。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</tr>

<tr>
<td colspan="2">--experimental-mounter-path string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: `mount`-->默认值：<code>mount</code></td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
[Experimental] Path of mounter binary. Leave empty to use the default `mount`. (DEPRECATED: will be removed in 1.23, in favor of using CSI.)
-->
[实验性特性] 卷挂载器（mounter）的可执行文件的路径。设置为空表示使用默认挂载器 <code>mount</code>。
已弃用：将在 1.23 版本移除以支持 CSI。
</td>
</tr>

<tr>
<td colspan="2">--fail-swap-on&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: `true`-->默认值：<code>true</code></td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Makes the Kubelet fail to start if swap is enabled on the node. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
设置为 true 表示如果主机启用了交换分区，kubelet 将直接失败。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--feature-gates mapStringBool</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
A set of `key=value` pairs that describe feature gates for alpha/experimental features. Options are:<br/>
APIListChunking=true|false (BETA - default=true)<br/>
APIPriorityAndFairness=true|false (BETA - default=true)<br/>
APIResponseCompression=true|false (BETA - default=true)<br/>
APIServerIdentity=true|false (ALPHA - default=false)<br/>
AllAlpha=true|false (ALPHA - default=false)<br/>
AllBeta=true|false (BETA - default=false)<br/>
AllowInsecureBackendProxy=true|false (BETA - default=true)<br/>
AnyVolumeDataSource=true|false (ALPHA - default=false)<br/>
AppArmor=true|false (BETA - default=true)<br/>
BalanceAttachedNodeVolumes=true|false (ALPHA - default=false)<br/>
BoundServiceAccountTokenVolume=true|false (ALPHA - default=false)<br/>
CPUManager=true|false (BETA - default=true)<br/>
CSIInlineVolume=true|false (BETA - default=true)<br/>
CSIMigration=true|false (BETA - default=true)<br/>
CSIMigrationAWS=true|false (BETA - default=false)<br/>
CSIMigrationAWSComplete=true|false (ALPHA - default=false)<br/>
CSIMigrationAzureDisk=true|false (BETA - default=false)<br/>
CSIMigrationAzureDiskComplete=true|false (ALPHA - default=false)<br/>
CSIMigrationAzureFile=true|false (ALPHA - default=false)<br/>
CSIMigrationAzureFileComplete=true|false (ALPHA - default=false)<br/>
CSIMigrationGCE=true|false (BETA - default=false)<br/>
CSIMigrationGCEComplete=true|false (ALPHA - default=false)<br/>
CSIMigrationOpenStack=true|false (BETA - default=false)<br/>
CSIMigrationOpenStackComplete=true|false (ALPHA - default=false)<br/>
CSIMigrationvSphere=true|false (BETA - default=false)<br/>
CSIMigrationvSphereComplete=true|false (BETA - default=false)<br/>
CSIServiceAccountToken=true|false (ALPHA - default=false)<br/>
CSIStorageCapacity=true|false (ALPHA - default=false)<br/>
CSIVolumeFSGroupPolicy=true|false (BETA - default=true)<br/>
ConfigurableFSGroupPolicy=true|false (BETA - default=true)<br/>
CronJobControllerV2=true|false (ALPHA - default=false)<br/>
CustomCPUCFSQuotaPeriod=true|false (ALPHA - default=false)<br/>
DefaultPodTopologySpread=true|false (BETA - default=true)<br/>
DevicePlugins=true|false (BETA - default=true)<br/>
DisableAcceleratorUsageMetrics=true|false (BETA - default=true)<br/>
DownwardAPIHugePages=true|false (ALPHA - default=false)<br/>
DynamicKubeletConfig=true|false (BETA - default=true)<br/>
EfficientWatchResumption=true|false (ALPHA - default=false)<br/>
EndpointSlice=true|false (BETA - default=true)<br/>
EndpointSliceNodeName=true|false (ALPHA - default=false)<br/>
EndpointSliceProxying=true|false (BETA - default=true)<br/>
EndpointSliceTerminatingCondition=true|false (ALPHA - default=false)<br/>
EphemeralContainers=true|false (ALPHA - default=false)<br/>
ExpandCSIVolumes=true|false (BETA - default=true)<br/>
ExpandInUsePersistentVolumes=true|false (BETA - default=true)<br/>
ExpandPersistentVolumes=true|false (BETA - default=true)<br/>
ExperimentalHostUserNamespaceDefaulting=true|false (BETA - default=false)<br/>
GenericEphemeralVolume=true|false (ALPHA - default=false)<br/>
GracefulNodeShutdown=true|false (ALPHA - default=false)<br/>
HPAContainerMetrics=true|false (ALPHA - default=false)<br/>
HPAScaleToZero=true|false (ALPHA - default=false)<br/>
HugePageStorageMediumSize=true|false (BETA - default=true)<br/>
IPv6DualStack=true|false (ALPHA - default=false)<br/>
ImmutableEphemeralVolumes=true|false (BETA - default=true)<br/>
KubeletCredentialProviders=true|false (ALPHA - default=false)<br/>
KubeletPodResources=true|false (BETA - default=true)<br/>
LegacyNodeRoleBehavior=true|false (BETA - default=true)<br/>
LocalStorageCapacityIsolation=true|false (BETA - default=true)<br/>
LocalStorageCapacityIsolationFSQuotaMonitoring=true|false (ALPHA - default=false)<br/>
MixedProtocolLBService=true|false (ALPHA - default=false)<br/>
NodeDisruptionExclusion=true|false (BETA - default=true)<br/>
NonPreemptingPriority=true|false (BETA - default=true)<br/>
PodDisruptionBudget=true|false (BETA - default=true)<br/>
PodOverhead=true|false (BETA - default=true)<br/>
ProcMountType=true|false (ALPHA - default=false)<br/>
QOSReserved=true|false (ALPHA - default=false)<br/>
RemainingItemCount=true|false (BETA - default=true)<br/>
RemoveSelfLink=true|false (BETA - default=true)<br/>
RootCAConfigMap=true|false (BETA - default=true)<br/>
RotateKubeletServerCertificate=true|false (BETA - default=true)<br/>
RunAsGroup=true|false (BETA - default=true)<br/>
ServerSideApply=true|false (BETA - default=true)<br/>
ServiceAccountIssuerDiscovery=true|false (BETA - default=true)<br/>
ServiceLBNodePortControl=true|false (ALPHA - default=false)<br/>
ServiceNodeExclusion=true|false (BETA - default=true)<br/>
ServiceTopology=true|false (ALPHA - default=false)<br/>
SetHostnameAsFQDN=true|false (BETA - default=true)<br/>
SizeMemoryBackedVolumes=true|false (ALPHA - default=false)<br/>
StorageVersionAPI=true|false (ALPHA - default=false)<br/>
StorageVersionHash=true|false (BETA - default=true)<br/>
Sysctls=true|false (BETA - default=true)<br/>
TTLAfterFinished=true|false (ALPHA - default=false)<br/>
TopologyManager=true|false (BETA - default=true)<br/>
ValidateProxyRedirects=true|false (BETA - default=true)<br/>
WarningHeaders=true|false (BETA - default=true)<br/>
WinDSR=true|false (ALPHA - default=false)<br/>
WinOverlay=true|false (BETA - default=true)<br/>
WindowsEndpointSliceProxying=true|false (ALPHA - default=false)<br/>
(DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
用于 alpha 实验性质的特性开关组，每个开关以 key=value 形式表示。当前可用开关包括：
APIListChunking=true|false (BETA - 默认值为 true)<br/>
APIPriorityAndFairness=true|false (BETA - 默认值为 true)<br/>
APIResponseCompression=true|false (BETA - 默认值为 true)<br/>
APIServerIdentity=true|false (ALPHA - 默认值为 false)<br/>
AllAlpha=true|false (ALPHA - 默认值为 false)<br/>
AllBeta=true|false (BETA - 默认值为 false)<br/>
AllowInsecureBackendProxy=true|false (BETA - 默认值为 true)<br/>
AnyVolumeDataSource=true|false (ALPHA - 默认值为 false)<br/>
AppArmor=true|false (BETA - 默认值为 true)<br/>
BalanceAttachedNodeVolumes=true|false (ALPHA - 默认值为 false)<br/>
BoundServiceAccountTokenVolume=true|false (ALPHA - 默认值为 false)<br/>
CPUManager=true|false (BETA - 默认值为 true)<br/>
CSIInlineVolume=true|false (BETA - 默认值为 true)<br/>
CSIMigration=true|false (BETA - 默认值为 true)<br/>
CSIMigrationAWS=true|false (BETA - 默认值为 false)<br/>
CSIMigrationAWSComplete=true|false (ALPHA - 默认值为 false)<br/>
CSIMigrationAzureDisk=true|false (BETA - 默认值为 false)<br/>
CSIMigrationAzureDiskComplete=true|false (ALPHA - 默认值为 false)<br/>
CSIMigrationAzureFile=true|false (ALPHA - 默认值为 false)<br/>
CSIMigrationAzureFileComplete=true|false (ALPHA - 默认值为 false)<br/>
CSIMigrationGCE=true|false (BETA - 默认值为 false)<br/>
CSIMigrationGCEComplete=true|false (ALPHA - 默认值为 false)<br/>
CSIMigrationOpenStack=true|false (BETA - 默认值为 false)<br/>
CSIMigrationOpenStackComplete=true|false (ALPHA - 默认值为 false)<br/>
CSIMigrationvSphere=true|false (BETA - 默认值为 false)<br/>
CSIMigrationvSphereComplete=true|false (BETA - 默认值为 false)<br/>
CSIServiceAccountToken=true|false (ALPHA - 默认值为 false)<br/>
CSIStorageCapacity=true|false (ALPHA - 默认值为 false)<br/>
CSIVolumeFSGroupPolicy=true|false (BETA - 默认值为 true)<br/>
ConfigurableFSGroupPolicy=true|false (BETA - 默认值为 true)<br/>
CronJobControllerV2=true|false (ALPHA - 默认值为 false)<br/>
CustomCPUCFSQuotaPeriod=true|false (ALPHA - 默认值为 false)<br/>
DefaultPodTopologySpread=true|false (BETA - 默认值为 true)<br/>
DevicePlugins=true|false (BETA - 默认值为 true)<br/>
DisableAcceleratorUsageMetrics=true|false (BETA - 默认值为 true)<br/>
DownwardAPIHugePages=true|false (ALPHA - 默认值为 false)<br/>
DynamicKubeletConfig=true|false (BETA - 默认值为 true)<br/>
EfficientWatchResumption=true|false (ALPHA - 默认值为 false)<br/>
EndpointSlice=true|false (BETA - 默认值为 true)<br/>
EndpointSliceNodeName=true|false (ALPHA - 默认值为 false)<br/>
EndpointSliceProxying=true|false (BETA - 默认值为 true)<br/>
EndpointSliceTerminatingCondition=true|false (ALPHA - 默认值为 false)<br/>
EphemeralContainers=true|false (ALPHA - 默认值为 false)<br/>
ExpandCSIVolumes=true|false (BETA - 默认值为 true)<br/>
ExpandInUsePersistentVolumes=true|false (BETA - 默认值为 true)<br/>
ExpandPersistentVolumes=true|false (BETA - 默认值为 true)<br/>
ExperimentalHostUserNamespaceDefaulting=true|false (BETA - 默认值为 false)<br/>
GenericEphemeralVolume=true|false (ALPHA - 默认值为 false)<br/>
GracefulNodeShutdown=true|false (ALPHA - 默认值为 false)<br/>
HPAContainerMetrics=true|false (ALPHA - 默认值为 false)<br/>
HPAScaleToZero=true|false (ALPHA - 默认值为 false)<br/>
HugePageStorageMediumSize=true|false (BETA - 默认值为 true)<br/>
IPv6DualStack=true|false (ALPHA - 默认值为 false)<br/>
ImmutableEphemeralVolumes=true|false (BETA - 默认值为 true)<br/>
KubeletCredentialProviders=true|false (ALPHA - 默认值为 false)<br/>
KubeletPodResources=true|false (BETA - 默认值为 true)<br/>
LegacyNodeRoleBehavior=true|false (BETA - 默认值为 true)<br/>
LocalStorageCapacityIsolation=true|false (BETA - 默认值为 true)<br/>
LocalStorageCapacityIsolationFSQuotaMonitoring=true|false (ALPHA - 默认值为 false)<br/>
MixedProtocolLBService=true|false (ALPHA - 默认值为 false)<br/>
NodeDisruptionExclusion=true|false (BETA - 默认值为 true)<br/>
NonPreemptingPriority=true|false (BETA - 默认值为 true)<br/>
PodDisruptionBudget=true|false (BETA - 默认值为 true)<br/>
PodOverhead=true|false (BETA - 默认值为 true)<br/>
ProcMountType=true|false (ALPHA - 默认值为 false)<br/>
QOSReserved=true|false (ALPHA - 默认值为 false)<br/>
RemainingItemCount=true|false (BETA - 默认值为 true)<br/>
RemoveSelfLink=true|false (BETA - 默认值为 true)<br/>
RootCAConfigMap=true|false (BETA - 默认值为 true)<br/>
RotateKubeletServerCertificate=true|false (BETA - 默认值为 true)<br/>
RunAsGroup=true|false (BETA - 默认值为 true)<br/>
ServerSideApply=true|false (BETA - 默认值为 true)<br/>
ServiceAccountIssuerDiscovery=true|false (BETA - 默认值为 true)<br/>
ServiceLBNodePortControl=true|false (ALPHA - 默认值为 false)<br/>
ServiceNodeExclusion=true|false (BETA - 默认值为 true)<br/>
ServiceTopology=true|false (ALPHA - 默认值为 false)<br/>
SetHostnameAsFQDN=true|false (BETA - 默认值为 true)<br/>
SizeMemoryBackedVolumes=true|false (ALPHA - 默认值为 false)<br/>
StorageVersionAPI=true|false (ALPHA - 默认值为 false)<br/>
StorageVersionHash=true|false (BETA - 默认值为 true)<br/>
Sysctls=true|false (BETA - 默认值为 true)<br/>
TTLAfterFinished=true|false (ALPHA - 默认值为 false)<br/>
TopologyManager=true|false (BETA - 默认值为 true)<br/>
ValidateProxyRedirects=true|false (BETA - 默认值为 true)<br/>
WarningHeaders=true|false (BETA - 默认值为 true)<br/>
WinDSR=true|false (ALPHA - 默认值为 false)<br/>
WinOverlay=true|false (BETA - 默认值为 true)<br/>
WindowsEndpointSliceProxying=true|false (ALPHA - 默认值为 false)<br/>
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--file-check-frequency duration&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: `20s`-->默认值：<code>20s</code></td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Duration between checking config files for new data. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
检查配置文件中新数据的时间间隔。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--hairpin-mode string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: `promiscuous-bridge`-->默认值：<code>promiscuous-bridge</code></td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
How should the kubelet setup hairpin NAT. This allows endpoints of a Service to load balance back to themselves if they should try to access their own Service. Valid values are `promiscuous-bridge`, `hairpin-veth` and `none`. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
设置 kubelet 执行发夹模式（hairpin）网络地址转译的方式。
该模式允许后端端点对其自身服务的访问能够再次经由负载均衡转发回自身。
可选项包括 “<code>promiscuous-bridge</code>”、“<code>hairpin-veth</code>” 和 “<code>none</code>”。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--healthz-bind-address ip&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: `127.0.0.1`-->默认值：<code>127.0.0.1</code></td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
The IP address for the healthz server to serve on (set to `0.0.0.0` for all IPv4 interfaces and `::` for all IPv6 interfaces). (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
用于运行 healthz 服务器的 IP 地址（设置为 <code>0.0.0.0</code> 表示使用所有 IPv4 接口，
设置为 <code>::</code> 表示使用所有 IPv6 接口。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--healthz-port int32&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: 10248-->默认值：10248</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
The port of the localhost healthz endpoint (set to `0` to disable). (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
本地 healthz 端点使用的端口（设置为 0 表示禁用）。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">-h, --help</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
help for kubelet
-->
kubelet 操作的帮助命令
</td>
</tr>

<tr>
<td colspan="2">--hostname-override string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
If non-empty, will use this string as identification instead of the actual hostname. If `--cloud-provider` is set, the cloud provider determines the name of the node (consult cloud provider documentation to determine if and how the hostname is used).
-->
如果为非空，将使用此字符串而不是实际的主机名作为节点标识。如果设置了
<code>--cloud-provider</code>，则云驱动将确定节点的名称
（请查阅云服务商文档以确定是否以及如何使用主机名）。
</td>
</tr>

<tr>
<td colspan="2">--housekeeping-interval duration&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: `10s`-->默认值：<code>10s</code></td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Interval between container housekeepings (default 10s)
-->
清理容器操作的时间间隔。
</td>
</tr>

<tr>
<td colspan="2">--http-check-frequency duration&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: `20s`-->默认值：<code>20s</code></td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Duration between checking HTTP for new data. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
HTTP 服务以获取新数据的时间间隔。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--image-credential-provider-bin-dir string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
The path to the directory where credential provider plugin binaries are located.
-->
指向凭据提供组件可执行文件所在目录的路径。
</td>
</tr>

<tr>
<td colspan="2">--image-credential-provider-config string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
The path to the credential provider plugin config file.</td>
-->
指向凭据提供插件配置文件所在目录的路径。
</tr>

<tr>
<td colspan="2">--image-gc-high-threshold int32&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: 85-->默认值：85</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
The percent of disk usage after which image garbage collection is always run. Values must be within the range [0, 100], To disable image garbage collection, set to 100.   (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
镜像垃圾回收上限。磁盘使用空间达到该百分比时，镜像垃圾回收将持续工作。
值必须在 [0，100] 范围内。要禁用镜像垃圾回收，请设置为 100。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--image-gc-low-threshold int32&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: 80-->默认值：80</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
The percent of disk usage before which image garbage collection is never run. Lowest disk usage to garbage collect to. Values must be within the range [0, 100] and should not be larger than that of `--image-gc-high-threshold`. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
镜像垃圾回收下限。磁盘使用空间在达到该百分比之前，镜像垃圾回收操作不会运行。
值必须在 [0，100] 范围内，并且不得大于 <code>--image-gc-high-threshold</code>的值。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--image-pull-progress-deadline duration&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: `1m0s`-->默认值：<code>1m0s</code></td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
If no pulling progress is made before this deadline, the image pulling will be cancelled. This docker-specific flag only works when container-runtime is set to `docker`.
-->
如果在该参数值所设置的期限之前没有拉取镜像的进展，镜像拉取操作将被取消。
仅当容器运行环境设置为 <code>docker</code> 时，此特定于 docker 的参数才有效。
</td>
</tr>

<tr>
<td colspan="2">--image-service-endpoint string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
[Experimental] The endpoint of remote image service. If not specified, it will be the same with `--container-runtime-endpoint` by default. Currently UNIX socket endpoint is supported on Linux, while npipe and TCP endpoints are supported on Windows.  Examples: `unix:///var/run/dockershim.sock`, `npipe:////./pipe/dockershim`
-->
[实验性特性] 远程镜像服务的端点。若未设定则默认情况下使用 <code>--container-runtime-endpoint</code>
的值。目前支持的类型包括在 Linux 系统上的 UNIX 套接字端点和 Windows 系统上的 npipe 和 TCP 端点。
例如：<code>unix:///var/run/dockershim.sock</code>、<code>npipe:////./pipe/dockershim</code>。
</td>
</tr>

<tr>
<td colspan="2">--iptables-drop-bit int32&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: 15-->默认值：15</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
The bit of the `fwmark` space to mark packets for dropping. Must be within the range [0, 31]. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
标记数据包将被丢弃的 fwmark 位设置。必须在 [0，31] 范围内。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--iptables-masquerade-bit int32&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: 14-->默认值：14</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
The bit of the `fwmark` space to mark packets for SNAT. Must be within the range [0, 31]. Please match this parameter with corresponding parameter in `kube-proxy`. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
标记数据包将进行 SNAT 的 fwmark 空间位设置。必须在 [0，31] 范围内。
请将此参数与 <code>kube-proxy</code> 中的相应参数匹配。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--keep-terminated-pod-volumes</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Keep terminated pod volumes mounted to the node after the pod terminates. Can be useful for debugging volume related issues. (DEPRECATED: will be removed in a future version)
-->
设置为 true 表示 Pod 终止后仍然保留之前挂载过的卷，常用于调试与卷有关的问题。
已弃用：将未来版本中移除。
</td>
</tr>

<tr>
<td colspan="2">--kernel-memcg-notification</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
If enabled, the kubelet will integrate with the kernel memcg notification to determine if memory eviction thresholds are crossed rather than polling. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
若启用，则 kubelet 将与内核中的 memcg 通知机制集成，不再使用轮询的方式来判定
是否 Pod 达到内存驱逐阈值。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--kube-api-burst int32&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: 10-->默认值：10</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Burst to use while talking with kubernetes apiserver. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's --config flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
每秒发送到 apiserver 的突发请求数量上限。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--kube-api-content-type string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: `application/vnd.kubernetes.protobuf`-->默认值：<code>application/vnd.kubernetes.protobuf</code></td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Content type of requests sent to apiserver. (default "application/vnd.kubernetes.protobuf") (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's --config flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
发送到 apiserver 的请求的内容类型。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--kube-api-qps int32&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: 5-->默认值：5</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
QPS to use while talking with kubernetes apiserver. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's --config flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
与 apiserver 通信的每秒查询个数（QPS）。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--kube-reserved mapStringString&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: &lt;None&gt;-->默认值：&lt;None&gt;</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
A set of `<resource name>=<resource quantity>` (e.g. `cpu=200m,memory=500Mi,ephemeral-storage=1Gi,pid='100'`) pairs that describe resources reserved for kubernetes system components. Currently `cpu`, `memory` and local `ephemeral-storage` for root file system are supported. See http://kubernetes.io/docs/user-guide/compute-resources for more detail. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
kubernetes 系统预留的资源配置，以一组 <code>资源名称=资源数量</code> 格式表示。
（例如：<code>cpu=200m,memory=500Mi,ephemeral-storage=1Gi,pid='100'</code>）。
当前支持 <code>cpu</code>、<code>memory</code> 和用于根文件系统的 <code>ephemeral-storage</code>。
请参阅<a href="http://kubernetes.io/zh/docs/concepts/configuration/manage-resources-containers/">相关文档</a>获取更多信息。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--kube-reserved-cgroup string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: `''`-->默认值：<code>""</code></td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Absolute name of the top level cgroup that is used to manage kubernetes components for which compute resources were reserved via `--kube-reserved` flag. Ex. `/kube-reserved`. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
给出某个顶层 cgroup 绝对名称，该 cgroup 用于管理通过标志 <code>--kube-reserved</code>
为 kubernetes 组件所预留的计算资源。例如：<code>"/kube-reserved"</code>。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--kubeconfig string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Path to a kubeconfig file, specifying how to connect to the API server. Providing `--kubeconfig` enables API server mode, omitting `--kubeconfig` enables standalone mode. 
-->
kubeconfig 配置文件的路径，指定如何连接到 API 服务器。
提供 <code>--kubeconfig</code> 将启用 API 服务器模式，而省略 <code>--kubeconfig</code> 将启用独立模式。
</td>
</tr>

<tr>
<td colspan="2">--kubelet-cgroups string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Optional absolute name of cgroups to create and run the Kubelet in. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's --config flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
用于创建和运行 kubelet 的 cgroup 的绝对名称。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--lock-file string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
<Warning: Alpha feature> The path to file for kubelet to use as a lock file.
-->
&lt;警告：alpha 特性&gt; kubelet 使用的锁文件的路径。
</td>
</tr>

<tr>
<td colspan="2">--log-backtrace-at traceLocation&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: `:0`-->默认值：<code>:0</code></td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
When logging hits line `<file>:<N>`, emit a stack trace.
-->
形式为 <code>&lt;file&gt;:&lt;N&gt;</code>。
当日志逻辑执行到命中 &lt;file&gt; 的第 &lt;N&gt; 行时，转储调用堆栈。
</td>
</tr>

<tr>
<td colspan="2">--log-dir string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
If non-empty, write log files in this directory
-->
如果此值为非空，则在所指定的目录中写入日志文件。
</td>
</tr>

<tr>
<td colspan="2">--log-file string</td>  
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
If non-empty, use this log file
-->
如果此值非空，使用所给字符串作为日志文件名。
</td>
</tr>

<tr>
<td colspan="2">--log-file-max-size uint&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: 1800-->默认值：1800</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Defines the maximum size a log file can grow to. Unit is megabytes. If the value is 0, the maximum file size is unlimited.
-->
设置日志文件的最大值。单位为兆字节（M）。如果值为 0，则表示文件大小无限制。
</td>
</tr>

<tr>
<td colspan="2">--log-flush-frequency duration&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: `5s`-->默认值：<code>5s</code></td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Maximum number of seconds between log flushes
-->
两次日志刷新之间的最大秒数（默认值为 5s）。
</td>
</tr>

<tr>
<td colspan="2">--logging-format string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: `text`-->默认值：<code>"text"</code></td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Sets the log format. Permitted formats: `text`, `json`.\nNon-default formats don't honor these flags: `--add-dir-header`, `--alsologtostderr`, `--log-backtrace-at`, `--log_dir`, `--log-file`, `--log-file-max-size`, `--logtostderr`, `--skip_headers`, `--skip_log_headers`, `--stderrthreshold`, `--log-flush-frequency`.\nNon-default choices are currently alpha and subject to change without warning. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
设置日志文件格式。可以设置的格式有：<code>"text"</code>、<code>"json"</code>。
非默认的格式不会使用以下标志的配置：<code>--add-dir-header</code>, <code>--alsologtostderr</code>,
<code>--log-backtrace-at</code>, <code>--log-dir</code>, <code>--log-file</code>,
<code>--log-file-max-size</code>, <code>--logtostderr</code>, <code>--skip-headers</code>,
<code>--skip-log-headers</code>, <code>--stderrthreshold</code>, <code>--log-flush-frequency</code>。
非默认选项的其它值都应视为 Alpha 特性，将来出现更改时不会额外警告。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--logtostderr&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: `true`-->默认值：<code>true</code></td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
log to standard error instead of files (default true)
-->
日志输出到 stderr 而不是文件。
</td>
</tr>

<tr>
<td colspan="2">--make-iptables-util-chains&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: `true`-->默认值：<code>true</code></td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
If true, kubelet will ensure `iptables` utility rules are present on host. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
设置为 true 表示 kubelet 将确保 <code>iptables</code> 规则在主机上存在。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--manifest-url string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
URL for accessing additional Pod specifications to run (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
用于访问要运行的其他 Pod 规范的 URL。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--manifest-url-header string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Comma-separated list of HTTP headers to use when accessing the URL provided to `--manifest-url`. Multiple headers with the same name will be added in the same order provided. This flag can be repeatedly invoked. For example: `--manifest-url-header 'a:hello,b:again,c:world' --manifest-url-header 'b:beautiful'` (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
取值为由 HTTP 头部组成的逗号分隔列表，在访问 <code>--manifest-url</code> 所给出的 URL 时使用。
名称相同的多个头部将按所列的顺序添加。该参数可以多次使用。例如：
<code>--manifest-url-header 'a:hello,b:again,c:world' --manifest-url-header 'b:beautiful'</code>。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>
<tr>
<td colspan="2">--master-service-namespace string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: `default`-->默认值：<code>default</code></td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
The namespace from which the kubernetes master services should be injected into pods. (DEPRECATED: This flag will be removed in a future version.)
-->
kubelet 向 Pod 注入 Kubernetes 主控服务信息时使用的命名空间。
已弃用：此标志将在未来的版本中删除。
</td>
</tr>

<tr>
<td colspan="2">--max-open-files int&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: 1000000-->默认值：1000000</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Number of files that can be opened by Kubelet process. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
kubelet 进程可以打开的最大文件数量。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--max-pods int32&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: 110-->默认值：110</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Number of Pods that can run on this Kubelet. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
此 kubelet 能运行的 Pod 最大数量。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--maximum-dead-containers int32&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: -1-->默认值：-1</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Maximum number of old instances of containers to retain globally. Each container takes up some disk space. To disable, set to a negative number. (DEPRECATED: Use `--eviction-hard` or `--eviction-soft` instead. Will be removed in a future version.)
-->
设置全局可保留的已停止容器实例个数上限。
每个实例会占用一些磁盘空间。要禁用，请设置为负数。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--maximum-dead-containers-per-container int32&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: 1-->默认值：1</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Maximum number of old instances to retain per container. Each container takes up some disk space. (DEPRECATED: Use --eviction-hard or --eviction-soft instead. Will be removed in a future version.)
-->
每个已停止容器可以保留的的最大实例数量。每个容器占用一些磁盘空间。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--minimum-container-ttl-duration duration</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Minimum age for a finished container before it is garbage collected.  Examples: '300ms', '10s' or '2h45m' (DEPRECATED: Use --eviction-hard or --eviction-soft instead. Will be removed in a future version.)
-->
已结束的容器在被垃圾回收清理之前的最少存活时间。
例如：<code>300ms</code>、<code>10s</code> 或者 <code>2h45m</code>。
已弃用：请改用 <code>--eviction-hard</code> 或者 <code>--eviction-soft</code>。
此标志将在未来的版本中删除。
</td>
</tr>

<tr>
<td colspan="2">--minimum-image-ttl-duration duration&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: `2m0s`-->默认值：<code>2m0s</code></td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Minimum age for an unused image before it is garbage collected.  Examples: `300ms`, `10s` or `2h45m`. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
不再使用的镜像在被垃圾回收清理之前的最少存活时间。
例如：<code>300ms</code>、<code>10s</code> 或者 <code>2h45m</code>。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--network-plugin string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
<Warning: Alpha feature> The name of the network plugin to be invoked for various events in kubelet/pod lifecycle. This docker-specific flag only works when container-runtime is set to docker.
-->
&lt;警告：alpha 特性&gt; 设置 kubelet/Pod 生命周期中各种事件调用的网络插件的名称。
仅当容器运行环境设置为 <code>docker</code> 时，此特定于 docker 的参数才有效。
</td>
</tr>

<tr>
<td colspan="2">--network-plugin-mtu int32</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
<Warning: Alpha feature> The MTU to be passed to the network plugin, to override the default. Set to 0 to use the default 1460 MTU. This docker-specific flag only works when container-runtime is set to docker.
-->
&lt;警告：alpha 特性&gt; 传递给网络插件的 MTU 值，将覆盖默认值。
设置为 0 则使用默认的 MTU 1460。仅当容器运行环境设置为 <code>docker</code> 时，
此特定于 docker 的参数才有效。
</td>
</tr>

<tr>
<td colspan="2">--node-ip string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
IP address of the node. If set, kubelet will use this IP address for the node
-->
节点的 IP 地址。如果设置，kubelet 将使用该 IP 地址作为节点的 IP 地址。
</td>
</tr>

<tr>
<td colspan="2">--node-labels mapStringString</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
&lt;Warning: Alpha feature&gt;Labels to add when registering the node in the cluster. Labels must be `key=value pairs` separated by `,`. Labels in the `kubernetes.io` namespace must begin with an allowed prefix (`kubelet.kubernetes.io`, `node.kubernetes.io`) or be in the specifically allowed set (`beta.kubernetes.io/arch`, `beta.kubernetes.io/instance-type`, `beta.kubernetes.io/os`, `failure-domain.beta.kubernetes.io/region`, `failure-domain.beta.kubernetes.io/zone`, `kubernetes.io/arch`, `kubernetes.io/hostname`, `kubernetes.io/os`, `node.kubernetes.io/instance-type`, `topology.kubernetes.io/region`, `topology.kubernetes.io/zone`)
-->
&lt;警告：alpha 特性&gt; kubelet 在集群中注册本节点时设置的标签。标签以
<code>key=value</code> 的格式表示，多个标签以逗号分隔。名字空间 <code>kubernetes.io</code>
中的标签必须以 <code>kubelet.kubernetes.io</code> 或 <code>node.kubernetes.io</code> 为前缀，
或者在以下明确允许范围内：
<code>beta.kubernetes.io/arch</code>, <code>beta.kubernetes.io/instance-type</code>,
<code>beta.kubernetes.io/os</code>, <code>failure-domain.beta.kubernetes.io/region</code>,
<code>failure-domain.beta.kubernetes.io/zone</code>, <code>kubernetes.io/arch</code>,
<code>kubernetes.io/hostname</code>, <code>kubernetes.io/os</code>,
<code>node.kubernetes.io/instance-type</code>, <code>topology.kubernetes.io/region</code>,
<code>topology.kubernetes.io/zone</code>。
</td>
</tr>

<tr>
<td colspan="2">--node-status-max-images int32&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: 50-->默认值：50</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
The maximum number of images to report in `node.status.images`. If `-1` is specified, no cap will be applied. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
在 <code>node.status.images</code> 中可以报告的最大镜像数量。如果指定为 -1，则不设上限。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--node-status-update-frequency duration&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: `10s`-->默认值：<code>10s</code></td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Specifies how often kubelet posts node status to master. Note: be cautious when changing the constant, it must work with nodeMonitorGracePeriod in Node controller. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
指定 kubelet 向主控节点汇报节点状态的时间间隔。注意：更改此常量时请务必谨慎，
它必须与节点控制器中的 <code>nodeMonitorGracePeriod</code> 一起使用。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--non-masquerade-cidr string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: `10.0.0.0/8`-->默认值：<code>10.0.0.0/8</code></td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Traffic to IPs outside this range will use IP masquerade. Set to '0.0.0.0/0' to never masquerade. (default "10.0.0.0/8") (DEPRECATED: will be removed in a future version)
-->
kubelet 向该 IP 段之外的 IP 地址发送的流量将使用 IP 伪装技术。
设置为 <code>0.0.0.0/0</code> 则不使用伪装。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--one-output</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
If true, only write logs to their native severity level (vs also writing to each lower severity level.
-->
如果设置此标志为 <code>true</code>，则仅将日志写入其原来的严重性级别中，
而不是同时将其写入更低严重性级别中。
</td>
</tr>

<tr>
<td colspan="2">--oom-score-adj int32&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: -999-->默认值：-999</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
The oom-score-adj value for kubelet process. Values must be within the range [-1000, 1000] (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's --config flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
kubelet 进程的 oom-score-adj 参数值。有效范围为 <code>[-1000，1000]</code>。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--pod-cidr string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
The CIDR to use for pod IP addresses, only used in standalone mode. In cluster mode, this is obtained from the master. For IPv6, the maximum number of IP's allocated is 65536 (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
用于给 Pod 分配 IP 地址的 CIDR 地址池，仅在独立运行模式下使用。
在集群模式下，CIDR 设置是从主服务器获取的。对于 IPv6，分配的 IP 的最大数量为 65536。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--pod-infra-container-image string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: `k8s.gcr.io/pause:3.2`-->默认值：<code>k8s.gcr.io/pause:3.2</code></td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
 Specified image will not be pruned by the image garbage collector. When container-runtime is set to `docker`, all containers in each pod will use the network/ipc namespaces from this image. Other CRI implementations have their own configuration to set this image.
-->
所指定的镜像不会被镜像垃圾收集器删除。
当容器运行环境设置为 <code>docker</code> 时，各个 Pod 中的所有容器都会
使用此镜像中的网络和 IPC 名字空间。
其他 CRI 实现有自己的配置来设置此镜像。
</td>
</tr>

<tr>
<td colspan="2">--pod-manifest-path string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Path to the directory containing static pod files to run, or the path to a single static pod file. Files starting with dots will be ignored. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
设置包含要运行的静态 Pod 的文件的路径，或单个静态 Pod 文件的路径。以点（<code>.</code>）
开头的文件将被忽略。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--pod-max-pids int&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: -1-->默认值：-1</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Set the maximum number of processes per pod.  If `-1`, the kubelet defaults to the node allocatable PID capacity. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
设置每个 Pod 中的最大进程数目。如果为 -1，则 kubelet 使用节点可分配的 PID 容量作为默认值。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--pods-per-core int32</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Number of Pods per core that can run on this Kubelet. The total number of Pods on this Kubelet cannot exceed `--max-pods`, so `--max-pods` will be used if this calculation results in a larger number of Pods allowed on the Kubelet. A value of `0` disables this limit. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
kubelet 在每个处理器核上可运行的 Pod 数量。此 kubelet 上的 Pod 总数不能超过
<code>--max-pods</code> 标志值。因此，如果此计算结果导致在 kubelet 
上允许更多数量的 Pod，则使用 <code>--max-pods</code> 值。值为 0 表示不作限制。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--port int32&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: 10250-->默认值：10250</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
The port for the Kubelet to serve on. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's --config flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
kubelet 服务监听的本机端口号。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--protect-kernel-defaults</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Default kubelet behaviour for kernel tuning. If set, kubelet errors if any of kernel tunables is different than kubelet defaults. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's --config flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
设置 kubelet 的默认内核调整行为。如果已设置该参数，当任何内核可调参数与
kubelet 默认值不同时，kubelet 都会出错。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--provider-id string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Unique identifier for identifying the node in a machine database, i.e cloud provider. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
设置主机数据库（即，云驱动）中用来标识节点的唯一标识。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--qos-reserved mapStringString</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
&lt;Warning: Alpha feature&gt; A set of `<resource name>=<percentage>` (e.g. `memory=50%`) pairs that describe how pod resource requests are reserved at the QoS level. Currently only memory is supported. Requires the `QOSReserved` feature gate to be enabled. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
&lt;警告：alpha 特性&gt; 设置在指定的 QoS 级别预留的 Pod 资源请求，以一组
<code>"资源名称=百分比"</code> 的形式进行设置，例如 <code>memory=50%</code>。
当前仅支持内存（memory）。要求启用 <code>QOSReserved</code> 特性门控。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--read-only-port int32&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: 10255-->默认值：10255</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
The read-only port for the Kubelet to serve on with no authentication/authorization (set to `0` to disable). (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
kubelet 可以在没有身份验证/鉴权的情况下提供只读服务的端口（设置为 0 表示禁用）。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--really-crash-for-testing</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
If true, when panics occur crash. Intended for testing. (DEPRECATED: will be removed in a future version.)
-->
设置为 true 表示发生失效时立即崩溃。仅用于测试。
已弃用：将在未来版本中移除。
</td>
</tr>

<tr>
<td colspan="2">--redirect-container-streaming</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Enables container streaming redirect. If false, kubelet will proxy container streaming data between the API server and container runtime; if `true`, kubelet will return an HTTP redirect to the API server, and the API server will access container runtime directly. The proxy approach is more secure, but introduces some overhead. The redirect approach is more performant, but less secure because the connection between apiserver and container runtime may not be authenticated. (DEPRECATED: Container streaming redirection will be removed from the kubelet in v1.20, and this flag will be removed in v1.22. For more details, see http://git.k8s.io/enhancements/keps/sig-node/20191205-container-streaming-requests.md)
-->
启用容器流数据重定向。如果设置为 false，则 kubelet 将在 apiserver 和容器运行时
之间转发容器流数据；如果设置为 true，则 kubelet 将返回指向 apiserver 的 HTTP 重定向信息，
而 apiserver 将直接访问容器运行时。代理方法更安全，但会带来一些开销。
重定向方法性能更高，但安全性较低，因为 apiserver 和容器运行时之间的连接可能未通过身份验证。<br/>
已弃用：容器流数据重定向会在 v1.20 中从 kubelet 中移除，此标志会在 v1.22
中移除。
相关信息可参见<a href="http://git.k8s.io/enhancements/keps/sig-node/20191205-container-streaming-requests.md">改进说明</a>。
</td>
</tr>

<tr>
<td colspan="2">--register-node&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: `true`-->默认值：<code>true</code></td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Register the node with the API server. If `--kubeconfig` is not provided, this flag is irrelevant, as the Kubelet won't have an API server to register with.
-->
将本节点注册到 API 服务器。如果未提供 <code>--kubeconfig</code> 标志设置，
则此参数无关紧要，因为 kubelet 将没有要注册的 API 服务器。
</td>
</tr>

<tr>
<td colspan="2">--register-schedulable&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: `true`-->默认值：true</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Register the node as schedulable. Won't have any effect if `--register-node` is false. (DEPRECATED: will be removed in a future version)
-->
注册本节点为可调度的节点。当 <code>--register-node</code>标志为 false 时此设置无效。
已弃用：此参数将在未来的版本中删除。
</td>
</tr>

<tr>
<td colspan="2">--register-with-taints mapStringString</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Register the node with the given list of taints (comma separated `<key>=<value>:<effect>`). No-op if `--register-node` is `false`. (DEPRECATED: will be removed in a future version)
-->
设置本节点的污点标记，格式为 <code>&lt;key&gt;=&lt;value&gt;:&lt;effect&gt;</code>，
以逗号分隔。当 <code>--register-node</code> 为 false 时此标志无效。
已弃用：将在未来版本中移除。
</td>
</tr>

<tr>
<td colspan="2">--registry-burst int32&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: 10-->默认值：10</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Maximum size of a bursty pulls, temporarily allows pulls to burst to this number, while still not exceeding `--registry-qps`. Only used if `--registry-qps > 0`. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
设置突发性镜像拉取的个数上限，在不超过 <code>--registration-qps</code> 设置值的前提下
暂时允许此参数所给的镜像拉取个数。仅在 <code>--registry-qps</code> 大于 0 时使用。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--registry-qps int32&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: 5</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
If &gt; 0, limit registry pull QPS to this value.  If `0`, unlimited. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
如此值大于 0，可用来限制镜像仓库的 QPS 上限。设置为 0，表示不受限制。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--reserved-cpus string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
A comma-separated list of CPUs or CPU ranges that are reserved for system and kubernetes usage. This specific list will supersede cpu counts in `--system-reserved` and `--kube-reserved`. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
用逗号分隔的一组 CPU 或 CPU 范围列表，给出为系统和 Kubernetes 保留使用的 CPU。
此列表所给出的设置优先于通过 <code>--system-reserved</code> 和
<code>--kube-reskube-reserved</code> 所保留的 CPU 个数配置。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--resolv-conf string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: `/etc/resolv.conf`-->默认值：<code>/etc/resolv.conf</code></td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Resolver configuration file used as the basis for the container DNS resolution configuration. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
名字解析服务的配置文件名，用作容器 DNS 解析配置的基础。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--root-dir string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: `/var/lib/kubelet`-->默认值：<code>/var/lib/kubelet</code></td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Directory path for managing kubelet files (volume mounts, etc).
-->
设置用于管理 kubelet 文件的根目录（例如挂载卷的相关文件等）。
</td>
</tr>

<tr>
<td colspan="2">--rotate-certificates</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
&lt;Warning: Beta feature&gt; Auto rotate the kubelet client certificates by requesting new certificates from the `kube-apiserver` when the certificate expiration approaches. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
&lt;警告：Beta 特性&gt; 设置当客户端证书即将过期时 kubelet 自动从
<code>kube-apiserver</code> 请求新的证书进行轮换。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--rotate-server-certificates</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Auto-request and rotate the kubelet serving certificates by requesting new certificates from the `kube-apiserver` when the certificate expiration approaches. Requires the `RotateKubeletServerCertificate` feature gate to be enabled, and approval of the submitted `CertificateSigningRequest` objects. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
当 kubelet 的服务证书即将过期时自动从 kube-apiserver 请求新的证书进行轮换。
要求启用 <code>RotateKubeletServerCertificate</code> 特性门控，以及对提交的
<code>CertificateSigningRequest</code> 对象进行批复（Approve）操作。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--runonce</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
If `true`, exit after spawning pods from local manifests or remote urls. Exclusive with `--enable-server` (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's --config flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
设置为 true 表示从本地清单或远程 URL 创建完 Pod 后立即退出 kubelet 进程。
与 <code>--enable-server</code> 标志互斥。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--runtime-cgroups string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Optional absolute name of cgroups to create and run the runtime in.
-->
设置用于创建和运行容器运行时的 cgroup 的绝对名称。
</td>
</tr>

<tr>
<td colspan="2">--runtime-request-timeout duration&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: `2m0s`-->默认值：<code>2m0s</code></td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Timeout of all runtime requests except long running request - `pull`, `logs`, `exec` and `attach`. When timeout exceeded, kubelet will cancel the request, throw out an error and retry later. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
设置除了长时间运行的请求（包括 <code>pull</code>、<code>logs</code>、<code>exec</code>
和 <code>attach</code> 等操作）之外的其他运行时请求的超时时间。
到达超时时间时，请求会被取消，抛出一个错误并会等待重试。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--seccomp-profile-root string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: `/var/lib/kubelet/seccomp`-->默认值：<code>/var/lib/kubelet/seccomp</code></td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
&lt;Warning: Alpha feature&gt; Directory path for seccomp profiles. (DEPRECATED: will be removed in 1.23, in favor of using the `<root-dir>/seccomp` directory)
-->
&lt;警告：alpha 特性&gt; seccomp 配置文件目录。
已弃用：将在 1.23 版本中移除，以使用 <code>&lt;root-dir&gt;/seccomp</code> 目录。
</td>
</tr>

<tr>
<td colspan="2">--serialize-image-pulls&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: `true`-->默认值：<code>true</code></td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Pull images one at a time. We recommend *not* changing the default value on nodes that run docker daemon with version &lt; 1.9 or an `aufs` storage backend. Issue #10959 has more details. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
逐一拉取镜像。建议 *不要* 在 docker 守护进程版本低于 1.9 或启用了 Aufs 存储后端的节点上
更改默认值。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--skip-headers</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
If true, avoid header prefixes in the log messages
-->
设置为 true 时在日志消息中去掉标头前缀。
</td>
</tr>

<tr>
<td colspan="2">--skip-log-headers</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
If true, avoid headers when opening log files
-->
设置为 true，打开日志文件时去掉标头。
</td>
</tr>

<tr>
<td colspan="2">--stderrthreshold int&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: 2-->默认值：2</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
logs at or above this threshold go to stderr.
-->
设置严重程度达到或超过此阈值的日志输出到标准错误输出。
</td>
</tr>

<tr>
<td colspan="2">--streaming-connection-idle-timeout duration&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: `4h0m0s`-->默认值：<code>4h0m0s</code></td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Maximum time a streaming connection can be idle before the connection is automatically closed. `0` indicates no timeout. Example: `5m`. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
设置流连接在自动关闭之前可以空闲的最长时间。0 表示没有超时限制。
例如：<code>5m</code>。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--sync-frequency duration&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: `1m0s`-->默认值：<code>1m0s</code></td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Max period between synchronizing running containers and config. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
在运行中的容器与其配置之间执行同步操作的最长时间间隔。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--system-cgroups /</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Optional absolute name of cgroups in which to place all non-kernel processes that are not already inside a cgroup under `/`. Empty for no container. Rolling back the flag requires a reboot. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
此标志值为一个 cgroup 的绝对名称，用于所有尚未放置在根目录下某 cgroup 内的非内核进程。
空值表示不指定 cgroup。回滚该参数需要重启机器。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--system-reserved mapStringString&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: none-->默认值：无</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
A set of `<resource name>=<resource quantity>` (e.g. `cpu=200m,memory=500Mi,ephemeral-storage=1Gi,pid='100'`) pairs that describe resources reserved for non-kubernetes components. Currently only `cpu` and `memory` are supported. See http://kubernetes.io/docs/user-guide/compute-resources for more detail. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
系统预留的资源配置，以一组 <code>资源名称=资源数量</code> 的格式表示，
（例如：<code>cpu=200m,memory=500Mi,ephemeral-storage=1Gi,pid='100'</code>）。
目前仅支持 <code>cpu</code> 和 <code>memory</code> 的设置。
更多细节可参考
<a href="http://kubernetes.io/zh/docs/concepts/configuration/manage-resources-containers/">相关文档</a>。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--system-reserved-cgroup string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: `''`-->默认值：<code>""</code></td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Absolute name of the top level cgroup that is used to manage non-kubernetes components for which compute resources were reserved via `--system-reserved` flag. Ex. `/system-reserved`. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
此标志给出一个顶层 cgroup 绝对名称，该 cgroup 用于管理非 kubernetes 组件，
这些组件的计算资源通过 <code>--system-reserved</code> 标志进行预留。
例如 <code>"/system-reserved"</code>。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--tls-cert-file string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
File containing x509 Certificate used for serving HTTPS (with intermediate certs, if any, concatenated after server cert). If `--tls-cert-file` and `--tls-private-key-file` are not provided, a self-signed certificate and key are generated for the public address and saved to the directory passed to `--cert-dir`. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
包含 x509 证书的文件路径，用于 HTTPS 认证。
如果有中间证书，则中间证书要串接在在服务器证书之后。
如果未提供 <code>--tls-cert-file</code> 和 <code>--tls-private-key-file</code>，
kubelet 会为公开地址生成自签名证书和密钥，并将其保存到通过
<code>--cert-dir</code> 指定的目录中。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--tls-cipher-suites string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Comma-separated list of cipher suites for the server. If omitted, the default Go cipher suites will be used. Possible values: TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA,TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256,TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA,TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384,TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305,TLS_ECDHE_ECDSA_WITH_RC4_128_SHA,TLS_ECDHE_RSA_WITH_3DES_EDE_CBC_SHA,TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA,TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256,TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA,TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384,TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305,TLS_ECDHE_RSA_WITH_RC4_128_SHA,TLS_RSA_WITH_3DES_EDE_CBC_SHA,TLS_RSA_WITH_AES_128_CBC_SHA,TLS_RSA_WITH_AES_128_CBC_SHA256,TLS_RSA_WITH_AES_128_GCM_SHA256,TLS_RSA_WITH_AES_256_CBC_SHA,TLS_RSA_WITH_AES_256_GCM_SHA384,TLS_RSA_WITH_RC4_128_SHA (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's --config flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
服务器端加密算法列表，以逗号分隔。如果不设置，则使用 Go 语言加密包的默认算法列表。<br/>
可选加密算法包括：TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA,TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256,TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA,TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384,TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305,TLS_ECDHE_ECDSA_WITH_RC4_128_SHA,TLS_ECDHE_RSA_WITH_3DES_EDE_CBC_SHA,TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA,TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256,TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA,TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384,TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305,TLS_ECDHE_RSA_WITH_RC4_128_SHA,TLS_RSA_WITH_3DES_EDE_CBC_SHA,TLS_RSA_WITH_AES_128_CBC_SHA,TLS_RSA_WITH_AES_128_CBC_SHA256,TLS_RSA_WITH_AES_128_GCM_SHA256,TLS_RSA_WITH_AES_256_CBC_SHA,TLS_RSA_WITH_AES_256_GCM_SHA384,TLS_RSA_WITH_RC4_128_SHA <br/>
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--tls-min-version string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Minimum TLS version supported. Possible values: `VersionTLS10`, `VersionTLS11`, `VersionTLS12`, `VersionTLS13` (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
设置支持的最小 TLS 版本号，可选的版本号包括：<code>VersionTLS10</code>、
<code>VersionTLS11</code>、<code>VersionTLS12</code> 和 <code>VersionTLS13</code>。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--tls-private-key-file string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
File containing x509 private key matching `--tls-cert-file`. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
包含与 <code>--tls-cert-file</code> 对应的 x509 私钥文件路径。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--topology-manager-policy string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: `none`-->默认值：<code>none</code></td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Topology Manager policy to use. Possible values: `none`, `best-effort`, `restricted`, `single-numa-node`. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
设置拓扑管理策略（Topology Manager policy）。可选值包括：<code>none</code>、
<code>best-effort</code>、<code>restricted</code> 和 <code>single-numa-node</code>。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--topology-manager-scope string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: `container`-->默认值：<code>container</code></td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Scope to which topology hints applied. Topology Manager collects hints from Hint Providers and applies them to defined scope to ensure the pod admission. Possible values: 'container' (default), 'pod'. (default "container") (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's --config flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
拓扑提示信息使用范围。拓扑管理器从提示提供者（Hints Providers）处收集提示信息，
并将其应用到所定义的范围以确保 Pod 准入。
可选值包括：<code>container</code>（默认）、<code>pod</code>。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">-v, --v Level</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
number for the log level verbosity
-->
设置 kubelet 日志级别详细程度的数值。
</td>
</tr>

<tr>
<td colspan="2">--version version[=true]</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Print version information and quit
-->
打印 kubelet 版本信息并退出。
</td>
</tr>

<tr>
<td colspan="2">--vmodule moduleSpec</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Comma-separated list of `pattern=N` settings for file-filtered logging
-->
以逗号分隔的 <code>pattern=N</code> 设置列表，用于文件过滤的日志记录
</td>
</tr>

<tr>
<td colspan="2">--volume-plugin-dir string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: `/usr/libexec/kubernetes/kubelet-plugins/volume/exec/`-->默认值：<code>/usr/libexec/kubernetes/kubelet-plugins/volume/exec/</code></td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
The full path of the directory in which to search for additional third party volume plugins. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
用来搜索第三方存储卷插件的目录。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>

<tr>
<td colspan="2">--volume-stats-agg-period duration&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: `1m0s`-->默认值：<code>1m0s</code></td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Specifies interval for kubelet to calculate and cache the volume disk usage for all pods and volumes. To disable volume calculations, set to `0`. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
-->
指定 kubelet 计算和缓存所有 Pod 和卷的磁盘用量总值的时间间隔。要禁用磁盘用量计算，
请设置为 0。
已弃用：应在 <code>--config</code> 所给的配置文件中进行设置。
（<a href="https://kubernetes.io/zh/docs/tasks/administer-cluster/kubelet-config-file/">进一步了解</a>）
</td>
</tr>
</tbody>
</table>

