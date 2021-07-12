---
title: kube-apiserver
content_type: tool-reference
weight: 30
auto_generated: true
---

<!--
The file is auto-generated from the Go source code of the component using a generic
[generator](https://github.com/kubernetes-sigs/reference-docs/). To learn how
to generate the reference documentation, please read
[Contributing to the reference documentation](/docs/contribute/generate-ref-docs/).
To update the reference conent, please follow the 
[Contributing upstream](/docs/contribute/generate-ref-docs/contribute-upstream/)
guide. You can file document formatting bugs against the
[reference-docs](https://github.com/kubernetes-sigs/reference-docs/) project.
-->

## {{% heading "synopsis" %}}


<!-- 
The Kubernetes API server validates and configures data
for the api objects which include pods, services, replicationcontrollers, and
others. The API Server services REST operations and provides the frontend to the
cluster's shared state through which all other components interact.
-->
Kubernetes API 服务器验证并配置 API 对象的数据，
这些对象包括 pods、services、replicationcontrollers 等。 
API 服务器为 REST 操作提供服务，并为集群的共享状态提供前端，
所有其他组件都通过该前端进行交互。

```
kube-apiserver [flags]
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
If true, adds the file directory to the header of the log messages
-->
<p>如果为 true，则将文件目录添加到日志消息的标题中</p>
</td>
</tr>

<tr>
<td colspan="2">--admission-control-config-file string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
File with admission control configuration.
-->
<p>包含准入控制配置的文件。</p>
</td>
</tr>

<tr>
<td colspan="2">--advertise-address string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
The IP address on which to advertise the apiserver to members of the cluster. 
This address must be reachable by the rest of the cluster. If blank, 
the --bind-address will be used. If --bind-address is unspecified, 
the host's default interface will be used.
-->
<p>
向集群成员通知 apiserver 消息的 IP 地址。
这个地址必须能够被集群中其他成员访问。
如果 IP 地址为空，将会使用 --bind-address，
如果未指定 --bind-address，将会使用主机的默认接口地址。
</p>
</td>
</tr>

<tr>
<td colspan="2">--allow-metric-labels stringToString&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：[]</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
<!--
The map from metric-label to value allow-list of this label. The key's format is &lt;MetricName&gt;,&lt;LabelName&gt;. The value's format is &lt;allowed_value&gt;,&lt;allowed_value&gt;...e.g. metric1,label1='v1,v2,v3', metric1,label2='v1,v2,v3' metric2,label1='v1,v2,v3'.
-->
允许使用的指标标签到指标值的映射列表。键的格式为 &lt;MetricName&gt;,&lt;LabelName&gt;.
值的格式为 &lt;allowed_value&gt;,&lt;allowed_value&gt;...。 
例如：<code>metric1,label1='v1,v2,v3', metric1,label2='v1,v2,v3' metric2,label1='v1,v2,v3'</code>。
</p></td>
</tr>


<tr>
<td colspan="2">--allow-privileged</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
If true, allow privileged containers. [default=false]
-->
如果为 true, 将允许特权容器。[默认值=false]
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
在向文件输出日志的同时，也将日志写到标准输出。
</td>
</tr>

<tr>
<td colspan="2">--anonymous-auth&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：true</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Enables anonymous requests to the secure port of the API server. 
Requests that are not rejected by another authentication method 
are treated as anonymous requests. Anonymous requests have a 
username of system:anonymous, and a group name of system:unauthenticated.
-->
启用到 API 服务器的安全端口的匿名请求。
未被其他认证方法拒绝的请求被当做匿名请求。
匿名请求的用户名为 <code>system:anonymous</code>，
用户组名为 </code>system:unauthenticated</code>。
</td>
</tr>

<tr>
<td colspan="2">--api-audiences strings</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Identifiers of the API. The service account token authenticator will 
validate that tokens used against the API are bound to at least one 
of these audiences. If the --service-account-issuer flag is configured 
and this flag is not, this field defaults to a single element list 
containing the issuer URL.
-->
API 的标识符。 
服务帐户令牌验证者将验证针对 API 使用的令牌是否已绑定到这些受众中的至少一个。 
如果配置了 <code>--service-account-issuer</code> 标志，但未配置此标志，
则此字段默认为包含发布者 URL 的单个元素列表。
</td>
</tr>

<tr>
<td colspan="2">--apiserver-count int&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：1</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
The number of apiservers running in the cluster, must be a positive number. 
(In use when --endpoint-reconciler-type=master-count is enabled.)
-->
集群中运行的 API 服务器数量，必须为正数。
（在启用 --endpoint-reconciler-type=master-count 时使用。）
</td>
</tr>

<tr>
<td colspan="2">--audit-log-batch-buffer-size int&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：10000</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
The size of the buffer to store events before batching and writing. Only used in batch mode.
-->
批处理和写入之前用于存储事件的缓冲区大小。
仅在批处理模式下使用。
</td>
</tr>

<tr>
<td colspan="2">--audit-log-batch-max-size int&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：1</td>
</tr><tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
The maximum size of a batch. Only used in batch mode.
-->
每个批次的最大大小。仅在批处理模式下使用。
</td>
</tr>

<tr>
<td colspan="2">--audit-log-batch-max-wait duration</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
The amount of time to wait before force writing the batch that hadn't reached the max size. 
Only used in batch mode.
-->
强制写入尚未达到最大大小的批次之前要等待的时间。
仅在批处理模式下使用。
</td>
</tr>

<tr>
<td colspan="2">--audit-log-batch-throttle-burst int</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Maximum number of requests sent at the same moment if ThrottleQPS was not utilized before. 
Only used in batch mode.
-->
如果之前未使用 ThrottleQPS，则为同时发送的最大请求数。
仅在批处理模式下使用。
</td>
</tr>

<tr>
<td colspan="2">--audit-log-batch-throttle-enable</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Whether batching throttling is enabled. Only used in batch mode.
-->
是否启用了批量限制。仅在批处理模式下使用。
</td>
</tr>

<tr>
<td colspan="2">--audit-log-batch-throttle-qps float</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Maximum average number of batches per second. Only used in batch mode.
-->
每秒的最大平均批次数。仅在批处理模式下使用。
</td>
</tr>

<tr>
<td colspan="2">--audit-log-compress</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
If set, the rotated log files will be compressed using gzip.
-->
若设置了此标志，则被轮换的日志文件会使用 gzip 压缩。
</td>

</tr>

<tr>
<td colspan="2">--audit-log-format string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值："json" </td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Format of saved audits. "legacy" indicates 1-line text format for each event. 
"json" indicates structured json format. Known formats are legacy,json.
-->
所保存的审计格式。
"legacy" 表示每行一个事件的文本格式。"json" 表示结构化的 JSON 格式。
已知格式为 legacy，json。
</td>
</tr>

<tr>
<td colspan="2">--audit-log-maxage int</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
The maximum number of days to retain old audit log files based on the timestamp encoded in their filename.
-->
根据文件名中编码的时间戳保留旧审计日志文件的最大天数。
</td>
</tr>

<tr>
<td colspan="2">--audit-log-maxbackup int</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
The maximum number of old audit log files to retain.
-->
要保留的旧的审计日志文件个数上限。
</td>
</tr>

<tr>
<td colspan="2">--audit-log-maxsize int</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
The maximum size in megabytes of the audit log file before it gets rotated.
-->
轮换之前，审计日志文件的最大大小（以兆字节为单位）。
</td>
</tr>

<tr>
<td colspan="2">--audit-log-mode string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值："blocking"</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Strategy for sending audit events. Blocking indicates sending events should block server responses. 
Batch causes the backend to buffer and write events asynchronously. 
Known modes are batch,blocking,blocking-strict.
-->
用来发送审计事件的策略。
阻塞（blocking）表示发送事件应阻止服务器响应。
批处理（batch）会导致后端异步缓冲和写入事件。
已知的模式是批处理（batch），阻塞（blocking），严格阻塞（blocking-strict）。
</td>
</tr>

<tr>
<td colspan="2">--audit-log-path string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
If set, all requests coming to the apiserver will be logged to this file.
'-' means standard out.
-->
如果设置，则所有到达 API 服务器的请求都将记录到该文件中。
"-" 表示标准输出。
</td>
</tr>

<tr>
<td colspan="2">--audit-log-truncate-enabled</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Whether event and batch truncating is enabled.
-->
是否启用事件和批次截断。
</td>
</tr>

<tr>
<td colspan="2">--audit-log-truncate-max-batch-size int&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：10485760</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Maximum size of the batch sent to the underlying backend. Actual serialized size can be 
several hundreds of bytes greater. If a batch exceeds this limit, it is split into 
several batches of smaller size.
-->
发送到下层后端的每批次的最大数据量。
实际的序列化大小可能会增加数百个字节。
如果一个批次超出此限制，则将其分成几个较小的批次。
</td>
</tr>

<tr>
<td colspan="2">--audit-log-truncate-max-event-size int&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：102400</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Maximum size of the audit event sent to the underlying backend. If the size of an event
is greater than this number, first request and response are removed, and if this doesn't 
reduce the size enough, event is discarded.
-->
发送到下层后端的每批次的最大数据量。
如果事件的大小大于此数字，则将删除第一个请求和响应；
如果这样做没有减小足够大的程度，则将丢弃事件。
</td>
</tr>

<tr>
<td colspan="2">--audit-log-version string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值："audit.k8s.io/v1"</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
API group and version used for serializing audit events written to log.
-->
用于对写入日志的审计事件执行序列化的 API 组和版本。
</td>
</tr>

<tr>
<td colspan="2">--audit-policy-file string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Path to the file that defines the audit policy configuration.
-->
定义审计策略配置的文件的路径。
</td>
</tr>

<tr>
<td colspan="2">--audit-webhook-batch-buffer-size int&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：10000</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
The size of the buffer to store events before batching and writing. Only used in batch mode.
-->
划分批次和写入之前用于存储事件的缓冲区大小。
仅在批处理模式下使用。
</td>
</tr>

<tr>
<td colspan="2">--audit-webhook-batch-max-size int&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：400</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
The maximum size of a batch. Only used in batch mode.
-->
批次的最大大小。
仅在批处理模式下使用。
</td>
</tr>

<tr>
<td colspan="2">--audit-webhook-batch-max-wait duration&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：30s</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
The amount of time to wait before force writing the batch that hadn't reached the max size. 
Only used in batch mode.
-->
强制写入尚未达到最大大小的批处理之前要等待的时间。
仅在批处理模式下使用。
</td>
</tr>

<tr>
<td colspan="2">--audit-webhook-batch-throttle-burst int&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：15</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Maximum number of requests sent at the same moment if ThrottleQPS was not utilized before. 
Only used in batch mode.
-->
如果之前未使用 ThrottleQPS，同时发送的最大请求数。
仅在批处理模式下使用。
</td>
</tr>

<tr>
<td colspan="2">--audit-webhook-batch-throttle-enable&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：true</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Whether batching throttling is enabled. Only used in batch mode.
-->
是否启用了批量限制。仅在批处理模式下使用。
</td>
</tr>

<tr>
<td colspan="2">--audit-webhook-batch-throttle-qps float32&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：10</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Maximum average number of batches per second. Only used in batch mode.
-->
每秒的最大平均批次数。仅在批处理模式下使用。
</td>
</tr>

<tr>
<td colspan="2">--audit-webhook-config-file string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Path to a kubeconfig formatted file that defines the audit webhook configuration.
-->
定义审计 webhook 配置的 kubeconfig 格式文件的路径。
</tr>

<tr>
<td colspan="2">--audit-webhook-initial-backoff duration&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：10s</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
The amount of time to wait before retrying the first failed request.
-->
重试第一个失败的请求之前要等待的时间。
</td>
</tr>

<tr>
<td colspan="2">--audit-webhook-mode string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值："batch"</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Strategy for sending audit events. Blocking indicates sending events should block server responses. 
Batch causes the backend to buffer and write events asynchronously. Known modes are batch,blocking,blocking-strict.
-->
发送审计事件的策略。
阻止（Blocking）表示发送事件应阻止服务器响应。
批处理（Batch）导致后端异步缓冲和写入事件。
已知的模式是批处理（batch），阻塞（blocking），严格阻塞（blocking-strict）。
</td>
</tr>

<tr>
<td colspan="2">--audit-webhook-truncate-enabled</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Whether event and batch truncating is enabled.
-->
是否启用事件和批处理截断。
</td>
</tr>

<tr>
<td colspan="2">--audit-webhook-truncate-max-batch-size int&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：10485760</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!-- 
Maximum size of the batch sent to the underlying backend. Actual serialized size can be 
several hundreds of bytes greater. If a batch exceeds this limit, it is split into 
several batches of smaller size.
-->
发送到下层后端的批次的最大数据量。
实际的序列化大小可能会增加数百个字节。
如果一个批次超出此限制，则将其分成几个较小的批次。
</td>
</tr>

<tr>
<td colspan="2">--audit-webhook-truncate-max-event-size int&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：102400</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Maximum size of the audit event sent to the underlying backend. If the size of an event
is greater than this number, first request and response are removed, and if this doesn't
reduce the size enough, event is discarded.
-->
发送到下层后端的批次的最大数据量。
如果事件的大小大于此数字，则将删除第一个请求和响应；
如果事件和事件的大小没有减小到一定幅度，则将丢弃事件。
</td>
</tr>

<tr>
<td colspan="2">--audit-webhook-version string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值："audit.k8s.io/v1"
</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
API group and version used for serializing audit events written to webhook.
-->
用于序列化写入 Webhook 的审计事件的 API 组和版本。
</td>
</tr>

<tr>
<td colspan="2">--authentication-token-webhook-cache-ttl duration&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->2m0s</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
The duration to cache responses from the webhook token authenticator.
-->
对来自 Webhook 令牌身份验证器的响应的缓存时间。
</td>
</tr>

<tr>
<td colspan="2">--authentication-token-webhook-config-file string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
File with webhook configuration for token authentication in kubeconfig format. 
The API server will query the remote service to determine authentication for bearer tokens.
-->
包含 Webhook 配置的 kubeconfig 格式文件，用于进行令牌认证。
API 服务器将查询远程服务，以对持有者令牌进行身份验证。
</td>
</tr>

<tr>
<td colspan="2">--authentication-token-webhook-version string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值："v1beta1"
</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
The API version of the authentication.k8s.io TokenReview to send to and expect from the webhook.
-->
与 Webhook 之间交换 authentication.k8s.io TokenReview 时使用的 API 版本。
</td>
</tr>

<tr>
<td colspan="2">--authorization-mode stringSlice&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值："AlwaysAllow"</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Ordered list of plug-ins to do authorization on secure port. Comma-delimited list of: 
AlwaysAllow,AlwaysDeny,ABAC,Webhook,RBAC,Node.
-->
在安全端口上进行鉴权的插件的顺序列表。
逗号分隔的列表：AlwaysAllow、AlwaysDeny、ABAC、Webhook、RBAC、Node。
</td>
</tr>

<tr>
<td colspan="2">--authorization-policy-file string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
File with authorization policy in json line by line format, 
used with --authorization-mode=ABAC, on the secure port.
-->
包含鉴权策略的文件，其内容为分行 JSON 格式，
在安全端口上与 --authorization-mode=ABAC 一起使用。
</td>
</tr>

<tr>
<td colspan="2">--authorization-webhook-cache-authorized-ttl duration&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：5m0s</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
The duration to cache 'authorized' responses from the webhook authorizer.
-->
对来自 Webhook 鉴权组件的 “授权（authorized）” 响应的缓存时间。
</td>
</tr>

<tr>
<td colspan="2">--authorization-webhook-cache-unauthorized-ttl duration&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：30s</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
The duration to cache 'unauthorized' responses from the webhook authorizer.
-->
对来自 Webhook 鉴权模块的 “未授权（unauthorized）” 响应的缓存时间。
</td>
</tr>

<tr>
<td colspan="2">--authorization-webhook-config-file string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
File with webhook configuration in kubeconfig format, used with --authorization-mode=Webhook. 
The API server will query the remote service to determine access on the API server's secure port.
-->
包含 Webhook 配置的文件，其格式为 kubeconfig，
与 --authorization-mode=Webhook 一起使用。
API 服务器将查询远程服务，以对 API 服务器的安全端口的访问执行鉴权。
</td>
</tr>

<tr>
<td colspan="2">--authorization-webhook-version string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值："v1beta1"</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
The API version of the authorization.k8s.io SubjectAccessReview to send to and expect from the webhook.
-->
与 Webhook 之间交换 authorization.k8s.io SubjectAccessReview 时使用的 API 版本。
</td>
</tr>

<tr>
<td colspan="2">--azure-container-registry-config string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Path to the file containing Azure container registry configuration information.
-->
包含 Azure 容器仓库配置信息的文件的路径。
</td>
</tr>

<tr>
<td colspan="2">--bind-address string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值："0.0.0.0"</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
The IP address on which to listen for the --secure-port port. The associated interface(s) 
must be reachable by the rest of the cluster, and by CLI/web clients. If blank or an 
unspecified address (0.0.0.0 or ::), all interfaces will be used.
-->
用来监听 <code>--secure-port</code> 端口的 IP 地址。
集群的其余部分以及 CLI/web 客户端必须可以访问所关联的接口。
如果为空白或未指定地址（<tt>0.0.0.0</tt> 或 <tt>::</tt>），则将使用所有接口。
</td>
</tr>

<tr>
<td colspan="2">--cert-dir string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值："/var/run/kubernetes"</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
The directory where the TLS certs are located. If --tls-cert-file and 
--tls-private-key-file are provided, this flag will be ignored.
-->
TLS 证书所在的目录。
如果提供了 <code>--tls-cert-file</code> 和 <code>--tls-private-key-file</code>
标志值，则将忽略此标志。
</td>
</tr>

<tr>
<td colspan="2">--client-ca-file string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
If set, any request presenting a client certificate signed by one of the authorities 
in the client-ca-file is authenticated with an identity corresponding to the CommonName 
of the client certificate.
-->
如果已设置，则使用与客户端证书的 CommonName 对应的标识对任何出示由
client-ca 文件中的授权机构之一签名的客户端证书的请求进行身份验证。
</td>
</tr>

<tr>
<td colspan="2">--cloud-config string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
The path to the cloud provider configuration file. Empty string for no configuration file.
-->
云厂商配置文件的路径。空字符串表示无配置文件。
</td>
</tr>

<tr>
<td colspan="2">--cloud-provider string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
The provider for cloud services. Empty string for no provider.
-->
云服务提供商。空字符串表示没有云厂商。
</td>
</tr>

<tr>
<td colspan="2">--cloud-provider-gce-l7lb-src-cidrs cidrs&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值："130.211.0.0/22,35.191.0.0/16"</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
CIDRs opened in GCE firewall for L7 LB traffic proxy & health checks
-->
在 GCE 防火墙中打开 CIDR，以进行第 7 层负载均衡流量代理和健康状况检查。
</td>
</tr>

<tr>
<td colspan="2">--contention-profiling</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Enable lock contention profiling, if profiling is enabled
-->
如果启用了性能分析，则启用锁争用性能分析。
</td>
</tr>

<tr>
<td colspan="2">--cors-allowed-origins strings</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
List of allowed origins for CORS, comma separated.  
An allowed origin can be a regular expression to support subdomain matching. 
If this list is empty CORS will not be enabled.
-->
CORS 允许的来源清单，以逗号分隔。
允许的来源可以是支持子域匹配的正则表达式。
如果此列表为空，则不会启用 CORS。
</td>
</tr>

<tr>
<td colspan="2">--default-not-ready-toleration-seconds int&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default: -->默认值：300</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Indicates the tolerationSeconds of the toleration for notReady:NoExecute that is added by default to every pod that does not already have such a toleration.
-->
对污点 NotReady:NoExecute 的容忍时长（以秒计）。 
默认情况下这一容忍度会被添加到尚未具有此容忍度的每个 pod 中。
</td>
</tr>

<tr>
<td colspan="2">--default-unreachable-toleration-seconds int&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：300</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Indicates the tolerationSeconds of the toleration for unreachable:NoExecute 
that is added by default to every pod that does not already have such a toleration.
-->
对污点 Unreachable:NoExecute 的容忍时长（以秒计）
默认情况下这一容忍度会被添加到尚未具有此容忍度的每个 pod 中。
</td>
</tr>

<tr>
<td colspan="2">--default-watch-cache-size int&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：100</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Default watch cache size. If zero, watch cache will be disabled for resources 
that do not have a default watch size set.
-->
默认监听（watch）缓存大小。
如果为零，则将为没有设置默认监视大小的资源禁用监视缓存。
</td>
</tr>

<tr>
<td colspan="2">--delete-collection-workers int&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值： 1</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Number of workers spawned for DeleteCollection call. These are used to speed up namespace cleanup.
-->
为 DeleteCollection 调用而产生的工作线程数。
这些用于加速名字空间清理。
</td>
</tr>

<tr>
<td colspan="2">--disable-admission-plugins strings</td>
</tr>
<tr>

<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
admission plugins that should be disabled although they are in the default enabled plugins list (NamespaceLifecycle, LimitRanger, ServiceAccount, TaintNodesByCondition, Priority, DefaultTolerationSeconds, DefaultStorageClass, StorageObjectInUseProtection, PersistentVolumeClaimResize, RuntimeClass, CertificateApproval, CertificateSigning, CertificateSubjectRestriction, DefaultIngressClass, MutatingAdmissionWebhook, ValidatingAdmissionWebhook, ResourceQuota). Comma-delimited list of admission plugins: AlwaysAdmit, AlwaysDeny, AlwaysPullImages, CertificateApproval, CertificateSigning, CertificateSubjectRestriction, DefaultIngressClass, DefaultStorageClass, DefaultTolerationSeconds, DenyServiceExternalIPs, EventRateLimit, ExtendedResourceToleration, ImagePolicyWebhook, LimitPodHardAntiAffinityTopology, LimitRanger, MutatingAdmissionWebhook, NamespaceAutoProvision, NamespaceExists, NamespaceLifecycle, NodeRestriction, OwnerReferencesPermissionEnforcement, PersistentVolumeClaimResize, PersistentVolumeLabel, PodNodeSelector, PodSecurityPolicy, PodTolerationRestriction, Priority, ResourceQuota, RuntimeClass, SecurityContextDeny, ServiceAccount, StorageObjectInUseProtection, TaintNodesByCondition, ValidatingAdmissionWebhook. The order of plugins in this flag does not matter.
-->
尽管位于默认启用的插件列表中（NamespaceLifecycle、LimitRanger、ServiceAccount、TaintNodesByCondition、Priority、DefaultTolerationSeconds、DefaultStorageClass、StorageObjectInUseProtection、PersistentVolumeClaimResize、RuntimeClass、CertificateApproval、CertificateSigning、CertificateSubjectRestriction、DefaultIngressClass、MutatingAdmissionWebhook、ValidatingAdmissionWebhook、ResourceQuota）仍须被禁用的插件。
<br/>取值为逗号分隔的准入插件列表：AlwaysAdmit、AlwaysDeny、AlwaysPullImages、CertificateApproval、CertificateSigning、CertificateSubjectRestriction、DefaultIngressClass、DefaultStorageClass、DefaultTolerationSeconds、DenyServiceExternalIPs、EventRateLimit、ExtendedResourceToleration、ImagePolicyWebhook、LimitPodHardAntiAffinityTopology、LimitRanger、MutatingAdmissionWebhook、NamespaceAutoProvision、NamespaceExists、NamespaceLifecycle、NodeRestriction、OwnerReferencesPermissionEnforcement、PersistentVolumeClaimResize、PersistentVolumeLabel、PodNodeSelector、PodSecurityPolicy、PodTolerationRestriction、Priority、ResourceQuota、RuntimeClass、SecurityContextDeny、ServiceAccount、StorageObjectInUseProtection、TaintNodesByCondition、ValidatingAdmissionWebhook。
<br/>该标志中插件的顺序无关紧要。
</td>
</tr>

<tr>
<td colspan="2">--disabled-metrics strings</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
This flag provides an escape hatch for misbehaving metrics. You must provide the fully qualified metric name in order to disable it. Disclaimer: disabling metrics is higher in precedence than showing hidden metrics.
-->
此标志为行为不正确的度量指标提供一种处理方案。
你必须提供完全限定的指标名称才能将其禁止。
声明：禁用度量值的行为优先于显示已隐藏的度量值。
</td>
</tr>


<tr>
<td colspan="2">--egress-selector-config-file string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
File with apiserver egress selector configuration.
-->
带有 API 服务器出站选择器配置的文件。
</td>
</tr>

<tr>
<td colspan="2">--enable-admission-plugins stringSlice</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
admission plugins that should be enabled in addition to default enabled ones (
NamespaceLifecycle, LimitRanger, ServiceAccount, TaintNodesByCondition, Priority, DefaultTolerationSeconds, DefaultStorageClass, StorageObjectInUseProtection, PersistentVolumeClaimResize, RuntimeClass, CertificateApproval, CertificateSigning, CertificateSubjectRestriction, DefaultIngressClass, MutatingAdmissionWebhook, ValidatingAdmissionWebhook, ResourceQuota).
Comma-delimited list of admission plugins:
AlwaysAdmit, AlwaysDeny, AlwaysPullImages, CertificateApproval, CertificateSigning, CertificateSubjectRestriction, DefaultIngressClass, DefaultStorageClass, DefaultTolerationSeconds, DenyServiceExternalIPs, EventRateLimit, ExtendedResourceToleration, ImagePolicyWebhook, LimitPodHardAntiAffinityTopology, LimitRanger, MutatingAdmissionWebhook, NamespaceAutoProvision, NamespaceExists, NamespaceLifecycle, NodeRestriction, OwnerReferencesPermissionEnforcement, PersistentVolumeClaimResize, PersistentVolumeLabel, PodNodeSelector, PodSecurityPolicy, PodTolerationRestriction, Priority, ResourceQuota, RuntimeClass, SecurityContextDeny, ServiceAccount, StorageObjectInUseProtection, TaintNodesByCondition, ValidatingAdmissionWebhook.
The order of plugins in this flag does not matter.
-->
除了默认启用的插件（NamespaceLifecycle、LimitRanger、ServiceAccount、TaintNodesByCondition、Priority、DefaultTolerationSeconds、DefaultStorageClass、StorageObjectInUseProtection、PersistentVolumeClaimResize、RuntimeClass、CertificateApproval、CertificateSigning、CertificateSubjectRestriction、DefaultIngressClass、MutatingAdmissionWebhook、ValidatingAdmissionWebhook、ResourceQuota）之外要启用的插件
</br>取值为逗号分隔的准入插件列表：AlwaysAdmit、AlwaysDeny、AlwaysPullImages、CertificateApproval、CertificateSigning、CertificateSubjectRestriction、DefaultIngressClass、DefaultStorageClass、DefaultTolerationSeconds、DenyServiceExternalIPs、EventRateLimit、ExtendedResourceToleration、ImagePolicyWebhook、LimitPodHardAntiAffinityTopology、LimitRanger、MutatingAdmissionWebhook、NamespaceAutoProvision、NamespaceExists、NamespaceLifecycle、NodeRestriction、OwnerReferencesPermissionEnforcement、PersistentVolumeClaimResize、PersistentVolumeLabel、PodNodeSelector、PodSecurityPolicy、PodTolerationRestriction、Priority、ResourceQuota、RuntimeClass、SecurityContextDeny、ServiceAccount、StorageObjectInUseProtection、TaintNodesByCondition、ValidatingAdmissionWebhook
<br/>该标志中插件的顺序无关紧要。
</td>
</tr>

<tr>
<td colspan="2">--enable-aggregator-routing</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Turns on aggregator routing requests to endpoints IP rather than cluster IP.
-->
允许聚合器将请求路由到端点 IP 而非集群 IP。
</td>
</tr>

<tr>
<td colspan="2">--enable-bootstrap-token-auth</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Enable to allow secrets of type 'bootstrap.kubernetes.io/token' in the 'kube-system'
namespace to be used for TLS bootstrapping authentication.
-->
启用以允许将 "kube-system" 名字空间中类型为 "bootstrap.kubernetes.io/token"
的 Secret 用于 TLS 引导身份验证。
</td>
</tr>

<tr>
<td colspan="2">--enable-garbage-collector&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：true</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Enables the generic garbage collector. MUST be synced with the corresponding flag of the kube-controller-manager.
-->
启用通用垃圾收集器。必须与 kube-controller-manager 的相应标志同步。
</td>
</tr>

<tr>
<td colspan="2">--enable-priority-and-fairness&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：true</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
If true and the APIPriorityAndFairness feature gate is enabled, 
replace the max-in-flight handler with an enhanced one that queues 
and dispatches with priority and fairness
-->
如果为 true 且启用了 <code>APIPriorityAndFairness</code> 特性门控，
请使用增强的处理程序替换 max-in-flight 处理程序，
以便根据优先级和公平性完成排队和调度。
</td>
</tr>

<tr>
<td colspan="2">--encryption-provider-config string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
The file containing configuration for encryption providers to be used for storing secrets in etcd
-->
包含加密提供程序配置信息的文件，用在 etcd 中所存储的 Secret 上。
</td>
</tr>

<tr>
<td colspan="2">--endpoint-reconciler-type string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值："lease"</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Use an endpoint reconciler (master-count, lease, none)
-->
使用端点协调器（<code>master-count</code>、<code>lease</code> 或 <code>none</code>）。
</td>
</tr>

<tr>
<td colspan="2">--etcd-cafile string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
SSL Certificate Authority file used to secure etcd communication.
-->
用于保护 etcd 通信的 SSL 证书颁发机构文件。
</td>
</tr>

<tr>
<td colspan="2">--etcd-certfile string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
SSL certification file used to secure etcd communication.
-->
用于保护 etcd 通信的 SSL 证书文件。
</td>
</tr>

<tr>
<td colspan="2">--etcd-compaction-interval duration&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：5m0s</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
The interval of compaction requests. If 0, the compaction request from apiserver is disabled.
-->
压缩请求的间隔。
如果为0，则禁用来自 API 服务器的压缩请求。
</td>
</tr>

<tr>
<td colspan="2">--etcd-count-metric-poll-period duration&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：1m0s</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Frequency of polling etcd for number of resources per type. 0 disables the metric collection.
-->
针对每种类型的资源数量轮询 etcd 的频率。
0 值表示禁用度量值收集。
</td>
</tr>

<tr>
<td colspan="2">--etcd-db-metric-poll-interval duration&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：30s</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
The interval of requests to poll etcd and update metric. 0 disables the metric collection
-->
轮询 etcd 和更新度量值的请求间隔。0 值表示禁用度量值收集。
</td>
</tr>

<tr>
<td colspan="2">--etcd-healthcheck-timeout duration&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:—->默认值：2s</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
The timeout to use when checking etcd health.
-->
检查 etcd 健康状况时使用的超时时长。
</td>
</tr>

<tr>
<td colspan="2">--etcd-keyfile string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
SSL key file used to secure etcd communication.<
-->
用于保护 etcd 通信的 SSL 密钥文件。
</td>
</tr>

<tr>
<td colspan="2">--etcd-prefix string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值："/registry"</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
The prefix to prepend to all resource paths in etcd.
-->
要在 etcd 中所有资源路径之前添加的前缀。
</td>
</tr>

<tr>
<td colspan="2">--etcd-servers strings</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
List of etcd servers to connect with (scheme://ip:port), comma separated.
-->
要连接的 etcd 服务器列表（<code>scheme://ip:port</code>），以逗号分隔。
</td>
</tr>

<tr>
<td colspan="2">--etcd-servers-overrides strings</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Per-resource etcd servers overrides, comma separated. 
The individual override format: group/resource#servers, 
where servers are URLs, semicolon separated.
-->
etcd 服务器针对每个资源的重载设置，以逗号分隔。
单个替代格式：组/资源#服务器（group/resource#servers），
其中服务器是 URL，以分号分隔。
</td>
</tr>

<tr>
<td colspan="2">--event-ttl duration&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：1h0m0s</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Amount of time to retain events.
-->
事件的保留时长。
</td>
</tr>

<tr>
<td colspan="2">--experimental-logging-sanitization</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--[Experimental] When enabled prevents logging of fields tagged as sensitive (passwords, keys, tokens).<br/>Runtime log sanitization may introduce significant computation overhead and therefore should not be enabled in production.
-->
[试验性功能] 启用此标志时，被标记为敏感的字段（密码、密钥、令牌）都不会被日志输出。<br/>
运行时的日志清理可能会引入相当程度的计算开销，因此不应该在产品环境中启用。
</td>
</tr>

<tr>
<td colspan="2">--external-hostname string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
The hostname to use when generating externalized URLs for this master 
(e.g. Swagger API Docs or OpenID Discovery).
-->
为此主机生成外部化 UR L时要使用的主机名（例如 Swagger API 文档或 OpenID 发现）。
</td>
</tr>

<tr>
<td colspan="2">--feature-gates &lt;逗号分隔的 'key=True|False' 键值对&gt;</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
A set of key=value pairs that describe feature gates for alpha/experimental features. Options are:<br/>
APIListChunking=true|false (BETA - default=true)<br/>
APIPriorityAndFairness=true|false (BETA - default=true)<br/>
APIResponseCompression=true|false (BETA - default=true)<br/>
APIServerIdentity=true|false (ALPHA - default=false)<br/>
AllAlpha=true|false (ALPHA - default=false)<br/>
AllBeta=true|false (BETA - default=false)<br/>
AnyVolumeDataSource=true|false (ALPHA - default=false)<br/>
AppArmor=true|false (BETA - default=true)<br/>
BalanceAttachedNodeVolumes=true|false (ALPHA - default=false)<br/>
BoundServiceAccountTokenVolume=true|false (BETA - default=true)<br/>
CPUManager=true|false (BETA - default=true)<br/>
CSIInlineVolume=true|false (BETA - default=true)<br/>
CSIMigration=true|false (BETA - default=true)<br/>
CSIMigrationAWS=true|false (BETA - default=false)<br/>
CSIMigrationAzureDisk=true|false (BETA - default=false)<br/>
CSIMigrationAzureFile=true|false (BETA - default=false)<br/>
CSIMigrationGCE=true|false (BETA - default=false)<br/>
CSIMigrationOpenStack=true|false (BETA - default=true)<br/>
CSIMigrationvSphere=true|false (BETA - default=false)<br/>
CSIMigrationvSphereComplete=true|false (BETA - default=false)<br/>
CSIServiceAccountToken=true|false (BETA - default=true)<br/>
CSIStorageCapacity=true|false (BETA - default=true)<br/>
CSIVolumeFSGroupPolicy=true|false (BETA - default=true)<br/>
CSIVolumeHealth=true|false (ALPHA - default=false)<br/>
ConfigurableFSGroupPolicy=true|false (BETA - default=true)<br/>
ControllerManagerLeaderMigration=true|false (ALPHA - default=false)<br/>
CronJobControllerV2=true|false (BETA - default=true)<br/>
CustomCPUCFSQuotaPeriod=true|false (ALPHA - default=false)<br/>
DaemonSetUpdateSurge=true|false (ALPHA - default=false)<br/>
DefaultPodTopologySpread=true|false (BETA - default=true)<br/>
DevicePlugins=true|false (BETA - default=true)<br/>
DisableAcceleratorUsageMetrics=true|false (BETA - default=true)<br/>
DownwardAPIHugePages=true|false (BETA - default=false)<br/>
DynamicKubeletConfig=true|false (BETA - default=true)<br/>
EfficientWatchResumption=true|false (BETA - default=true)<br/>
EndpointSliceProxying=true|false (BETA - default=true)<br/>
EndpointSliceTerminatingCondition=true|false (ALPHA - default=false)<br/>
EphemeralContainers=true|false (ALPHA - default=false)<br/>
ExpandCSIVolumes=true|false (BETA - default=true)<br/>
ExpandInUsePersistentVolumes=true|false (BETA - default=true)<br/>
ExpandPersistentVolumes=true|false (BETA - default=true)<br/>
ExperimentalHostUserNamespaceDefaulting=true|false (BETA - default=false)<br/>
GenericEphemeralVolume=true|false (BETA - default=true)<br/>
GracefulNodeShutdown=true|false (BETA - default=true)<br/>
HPAContainerMetrics=true|false (ALPHA - default=false)<br/>
HPAScaleToZero=true|false (ALPHA - default=false)<br/>
HugePageStorageMediumSize=true|false (BETA - default=true)<br/>
IPv6DualStack=true|false (BETA - default=true)<br/>
InTreePluginAWSUnregister=true|false (ALPHA - default=false)<br/>
InTreePluginAzureDiskUnregister=true|false (ALPHA - default=false)<br/>
InTreePluginAzureFileUnregister=true|false (ALPHA - default=false)<br/>
InTreePluginGCEUnregister=true|false (ALPHA - default=false)<br/>
InTreePluginOpenStackUnregister=true|false (ALPHA - default=false)<br/>
InTreePluginvSphereUnregister=true|false (ALPHA - default=false)<br/>
IndexedJob=true|false (ALPHA - default=false)<br/>
IngressClassNamespacedParams=true|false (ALPHA - default=false)<br/>
KubeletCredentialProviders=true|false (ALPHA - default=false)<br/>
KubeletPodResources=true|false (BETA - default=true)<br/>
KubeletPodResourcesGetAllocatable=true|false (ALPHA - default=false)<br/>
LocalStorageCapacityIsolation=true|false (BETA - default=true)<br/>
LocalStorageCapacityIsolationFSQuotaMonitoring=true|false (ALPHA - default=false)<br/>
LogarithmicScaleDown=true|false (ALPHA - default=false)<br/>
MemoryManager=true|false (ALPHA - default=false)<br/>
MixedProtocolLBService=true|false (ALPHA - default=false)<br/>
NamespaceDefaultLabelName=true|false (BETA - default=true)<br/>
NetworkPolicyEndPort=true|false (ALPHA - default=false)<br/>
NonPreemptingPriority=true|false (BETA - default=true)<br/>
PodAffinityNamespaceSelector=true|false (ALPHA - default=false)<br/>
PodDeletionCost=true|false (ALPHA - default=false)<br/>
PodOverhead=true|false (BETA - default=true)<br/>
PreferNominatedNode=true|false (ALPHA - default=false)<br/>
ProbeTerminationGracePeriod=true|false (ALPHA - default=false)<br/>
ProcMountType=true|false (ALPHA - default=false)<br/>
QOSReserved=true|false (ALPHA - default=false)<br/>
RemainingItemCount=true|false (BETA - default=true)<br/>
RemoveSelfLink=true|false (BETA - default=true)<br/>
RotateKubeletServerCertificate=true|false (BETA - default=true)<br/>
ServerSideApply=true|false (BETA - default=true)<br/>
ServiceInternalTrafficPolicy=true|false (ALPHA - default=false)<br/>
ServiceLBNodePortControl=true|false (ALPHA - default=false)<br/>
ServiceLoadBalancerClass=true|false (ALPHA - default=false)<br/>
ServiceTopology=true|false (ALPHA - default=false)<br/>
SetHostnameAsFQDN=true|false (BETA - default=true)<br/>
SizeMemoryBackedVolumes=true|false (ALPHA - default=false)<br/>
StorageVersionAPI=true|false (ALPHA - default=false)<br/>
StorageVersionHash=true|false (BETA - default=true)<br/>
SuspendJob=true|false (ALPHA - default=false)<br/>
TTLAfterFinished=true|false (BETA - default=true)<br/>
TopologyAwareHints=true|false (ALPHA - default=false)<br/>
TopologyManager=true|false (BETA - default=true)<br/>
ValidateProxyRedirects=true|false (BETA - default=true)<br/>
VolumeCapacityPriority=true|false (ALPHA - default=false)<br/>
WarningHeaders=true|false (BETA - default=true)<br/>
WinDSR=true|false (ALPHA - default=false)<br/>
WinOverlay=true|false (BETA - default=true)<br/>
WindowsEndpointSliceProxying=true|false (BETA - default=true)
-->
<p>一组 key=value 对，用来描述测试性/试验性功能的特性门控。可选项有：
APIListChunking=true|false (BETA - 默认值=true)<br/>
APIPriorityAndFairness=true|false (BETA - 默认值=true)<br/>
APIResponseCompression=true|false (BETA - 默认值=true)<br/>
APIServerIdentity=true|false (ALPHA - 默认值=false)<br/>
AllAlpha=true|false (ALPHA - 默认值=false)<br/>
AllBeta=true|false (BETA - 默认值=false)<br/>
AnyVolumeDataSource=true|false (ALPHA - 默认值=false)<br/>
AppArmor=true|false (BETA - 默认值=true)<br/>
BalanceAttachedNodeVolumes=true|false (ALPHA - 默认值=false)<br/>
BoundServiceAccountTokenVolume=true|false (BETA - 默认值=true)<br/>
CPUManager=true|false (BETA - 默认值=true)<br/>
CSIInlineVolume=true|false (BETA - 默认值=true)<br/>
CSIMigration=true|false (BETA - 默认值=true)<br/>
CSIMigrationAWS=true|false (BETA - 默认值=false)<br/>
CSIMigrationAzureDisk=true|false (BETA - 默认值=false)<br/>
CSIMigrationAzureFile=true|false (BETA - 默认值=false)<br/>
CSIMigrationGCE=true|false (BETA - 默认值=false)<br/>
CSIMigrationOpenStack=true|false (BETA - 默认值=true)<br/>
CSIMigrationvSphere=true|false (BETA - 默认值=false)<br/>
CSIMigrationvSphereComplete=true|false (BETA - 默认值=false)<br/>
CSIServiceAccountToken=true|false (BETA - 默认值=true)<br/>
CSIStorageCapacity=true|false (BETA - 默认值=true)<br/>
CSIVolumeFSGroupPolicy=true|false (BETA - 默认值=true)<br/>
CSIVolumeHealth=true|false (ALPHA - 默认值=false)<br/>
ConfigurableFSGroupPolicy=true|false (BETA - 默认值=true)<br/>
ControllerManagerLeaderMigration=true|false (ALPHA - 默认值=false)<br/>
CronJobControllerV2=true|false (BETA - 默认值=true)<br/>
CustomCPUCFSQuotaPeriod=true|false (ALPHA - 默认值=false)<br/>
DaemonSetUpdateSurge=true|false (ALPHA - 默认值=false)<br/>
DefaultPodTopologySpread=true|false (BETA - 默认值=true)<br/>
DevicePlugins=true|false (BETA - 默认值=true)<br/>
DisableAcceleratorUsageMetrics=true|false (BETA - 默认值=true)<br/>
DownwardAPIHugePages=true|false (BETA - 默认值=false)<br/>
DynamicKubeletConfig=true|false (BETA - 默认值=true)<br/>
EfficientWatchResumption=true|false (BETA - 默认值=true)<br/>
EndpointSliceProxying=true|false (BETA - 默认值=true)<br/>
EndpointSliceTerminatingCondition=true|false (ALPHA - 默认值=false)<br/>
EphemeralContainers=true|false (ALPHA - 默认值=false)<br/>
ExpandCSIVolumes=true|false (BETA - 默认值=true)<br/>
ExpandInUsePersistentVolumes=true|false (BETA - 默认值=true)<br/>
ExpandPersistentVolumes=true|false (BETA - 默认值=true)<br/>
ExperimentalHostUserNamespace默认值ing=true|false (BETA - 默认值=false)<br/>
GenericEphemeralVolume=true|false (BETA - 默认值=true)<br/>
GracefulNodeShutdown=true|false (BETA - 默认值=true)<br/>
HPAContainerMetrics=true|false (ALPHA - 默认值=false)<br/>
HPAScaleToZero=true|false (ALPHA - 默认值=false)<br/>
HugePageStorageMediumSize=true|false (BETA - 默认值=true)<br/>
IPv6DualStack=true|false (BETA - 默认值=true)<br/>
InTreePluginAWSUnregister=true|false (ALPHA - 默认值=false)<br/>
InTreePluginAzureDiskUnregister=true|false (ALPHA - 默认值=false)<br/>
InTreePluginAzureFileUnregister=true|false (ALPHA - 默认值=false)<br/>
InTreePluginGCEUnregister=true|false (ALPHA - 默认值=false)<br/>
InTreePluginOpenStackUnregister=true|false (ALPHA - 默认值=false)<br/>
InTreePluginvSphereUnregister=true|false (ALPHA - 默认值=false)<br/>
IndexedJob=true|false (ALPHA - 默认值=false)<br/>
IngressClassNamespacedParams=true|false (ALPHA - 默认值=false)<br/>
KubeletCredentialProviders=true|false (ALPHA - 默认值=false)<br/>
KubeletPodResources=true|false (BETA - 默认值=true)<br/>
KubeletPodResourcesGetAllocatable=true|false (ALPHA - 默认值=false)<br/>
LocalStorageCapacityIsolation=true|false (BETA - 默认值=true)<br/>
LocalStorageCapacityIsolationFSQuotaMonitoring=true|false (ALPHA - 默认值=false)<br/>
LogarithmicScaleDown=true|false (ALPHA - 默认值=false)<br/>
MemoryManager=true|false (ALPHA - 默认值=false)<br/>
MixedProtocolLBService=true|false (ALPHA - 默认值=false)<br/>
NamespaceDefaultLabelName=true|false (BETA - 默认值=true)<br/>
NetworkPolicyEndPort=true|false (ALPHA - 默认值=false)<br/>
NonPreemptingPriority=true|false (BETA - 默认值=true)<br/>
PodAffinityNamespaceSelector=true|false (ALPHA - 默认值=false)<br/>
PodDeletionCost=true|false (ALPHA - 默认值=false)<br/>
PodOverhead=true|false (BETA - 默认值=true)<br/>
PreferNominatedNode=true|false (ALPHA - 默认值=false)<br/>
ProbeTerminationGracePeriod=true|false (ALPHA - 默认值=false)<br/>
ProcMountType=true|false (ALPHA - 默认值=false)<br/>
QOSReserved=true|false (ALPHA - 默认值=false)<br/>
RemainingItemCount=true|false (BETA - 默认值=true)<br/>
RemoveSelfLink=true|false (BETA - 默认值=true)<br/>
RotateKubeletServerCertificate=true|false (BETA - 默认值=true)<br/>
ServerSideApply=true|false (BETA - 默认值=true)<br/>
ServiceInternalTrafficPolicy=true|false (ALPHA - 默认值=false)<br/>
ServiceLBNodePortControl=true|false (ALPHA - 默认值=false)<br/>
ServiceLoadBalancerClass=true|false (ALPHA - 默认值=false)<br/>
ServiceTopology=true|false (ALPHA - 默认值=false)<br/>
SetHostnameAsFQDN=true|false (BETA - 默认值=true)<br/>
SizeMemoryBackedVolumes=true|false (ALPHA - 默认值=false)<br/>
StorageVersionAPI=true|false (ALPHA - 默认值=false)<br/>
StorageVersionHash=true|false (BETA - 默认值=true)<br/>
SuspendJob=true|false (ALPHA - 默认值=false)<br/>
TTLAfterFinished=true|false (BETA - 默认值=true)<br/>
TopologyAwareHints=true|false (ALPHA - 默认值=false)<br/>
TopologyManager=true|false (BETA - 默认值=true)<br/>
ValidateProxyRedirects=true|false (BETA - 默认值=true)<br/>
VolumeCapacityPriority=true|false (ALPHA - 默认值=false)<br/>
WarningHeaders=true|false (BETA - 默认值=true)<br/>
WinDSR=true|false (ALPHA - 默认值=false)<br/>
WinOverlay=true|false (BETA - 默认值=true)<br/>
WindowsEndpointSliceProxying=true|false (BETA - 默认值=true)</p>
</td>
</tr>

<tr>
<td colspan="2">--goaway-chance float</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
To prevent HTTP/2 clients from getting stuck on a single apiserver, 
randomly close a connection (GOAWAY). The client's other in-flight 
requests won't be affected, and the client will reconnect, likely 
landing on a different apiserver after going through the load 
balancer again. This argument sets the fraction of requests that 
will be sent a GOAWAY. Clusters with single apiservers, or which 
don't use a load balancer, should NOT enable this. Min is 0 (off), 
Max is .02 (1/50 requests); .001 (1/1000) is a recommended starting point.
-->
为防止 HTTP/2 客户端卡在单个 API 服务器上，可启用随机关闭连接（GOAWAY）。
客户端的其他运行中请求将不会受到影响，并且客户端将重新连接，
可能会在再次通过负载平衡器后登陆到其他 API 服务器上。 
此参数设置将发送 GOAWAY 的请求的比例。 
具有单个 API 服务器或不使用负载平衡器的群集不应启用此功能。 
最小值为0（关闭），最大值为 .02（1/50 请求）； 建议使用 .001（1/1000）。
</td>
</tr>

<tr>
<td colspan="2">-h, --help</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
help for kube-apiserver
-->
kube-apiserver 的帮助命令
</td>
</tr>

<tr>
<td colspan="2">--http2-max-streams-per-connection int</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
The limit that the server gives to clients for the maximum number 
of streams in an HTTP/2 connection. Zero means to use golang's default.
-->
服务器为客户端提供的 HTTP/2 连接中最大流数的限制。
零表示使用 GoLang 的默认值。
</td>
</tr>

<tr>
<td colspan="2">--identity-lease-duration-seconds int&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：3600</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
The duration of kube-apiserver lease in seconds, must be a positive number. (In use when the APIServerIdentity feature gate is enabled.)
-->
kube-apiserver 租约时长（按秒计），必须是正数。
（当 APIServerIdentity 特性门控被启用时使用此标志值）
</td>
</tr>

<tr>
<td colspan="2">--identity-lease-renew-interval-seconds int&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：10</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
The interval of kube-apiserver renewing its lease in seconds, must be a positive number. (In use when the APIServerIdentity feature gate is enabled.)
-->
kube-apiserver 对其租约进行续期的时间间隔（按秒计），必须是正数。
（当 APIServerIdentity 特性门控被启用时使用此标志值）
</td>
</tr>

<tr>
<td colspan="2">--kubelet-certificate-authority string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Path to a cert file for the certificate authority.
-->
证书颁发机构的证书文件的路径。
</td>
</tr>

<tr>
<td colspan="2">--kubelet-client-certificate string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Path to a client cert file for TLS.
-->
TLS 的客户端证书文件的路径。
</td>
</tr>

<tr>
<td colspan="2">--kubelet-client-key string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Path to a client key file for TLS.
-->
TLS 客户端密钥文件的路径。
</td>
</tr>

<tr>
<td colspan="2">--kubelet-preferred-address-types strings&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：Hostname,InternalDNS,InternalIP,ExternalDNS,ExternalIP</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
List of the preferred NodeAddressTypes to use for kubelet connections.
-->
用于 kubelet 连接的首选 NodeAddressTypes 列表。
</td>
</tr>

<tr>
<td colspan="2">--kubelet-timeout duration&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：5s</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Timeout for kubelet operations.
-->
kubelet 操作超时时间。
</td>
</tr>

<tr>
<td colspan="2">--kubernetes-service-node-port int</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
If non-zero, the Kubernetes master service (which apiserver creates/maintains) 
will be of type NodePort, using this as the value of the port. If zero, 
the Kubernetes master service will be of type ClusterIP.
-->
如果非零，那么 Kubernetes 主服务（由 apiserver 创建/维护）将是 NodePort 类型，
使用它作为端口的值。
如果为零，则 Kubernetes 主服务将为 ClusterIP 类型。
</td>
</tr>

<tr>
<td colspan="2">--lease-reuse-duration-seconds int&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：60</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
The time in seconds that each lease is reused. A lower value could avoid large number of objects reusing the same lease. Notice that a too small value may cause performance problems at storage layer.
-->
每个租约被重用的时长。
如果此值比较低，可以避免大量对象重用此租约。
注意，如果此值过小，可能导致存储层出现性能问题。
</td>
</tr>

<tr>
<td colspan="2">--livez-grace-period duration</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
This option represents the maximum amount of time it should take for apiserver 
to complete its startup sequence and become live. From apiserver's start time 
to when this amount of time has elapsed, /livez will assume that unfinished 
post-start hooks will complete successfully and therefore return true.
-->
此选项代表 API 服务器完成启动序列并生效所需的最长时间。
从 API 服务器的启动时间到这段时间为止，
<tt>/livez</tt> 将假定未完成的启动后钩子将成功完成，因此返回 true。
</td>
</tr>

<tr>
<td colspan="2">--log-backtrace-at traceLocation&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：<tt>:0</tt></td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
when logging hits line file:N, emit a stack trace
-->
当日志机制执行到'文件 :N'时，生成堆栈跟踪。
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
如果为非空，则在此目录中写入日志文件。
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
如果为非空，使用此值作为日志文件。
</td>
</tr>

<tr>
<td colspan="2">--log-file-max-size uint&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：1800</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Defines the maximum size a log file can grow to. Unit is megabytes. 
If the value is 0, the maximum file size is unlimited.
-->
定义日志文件可以增长到的最大大小。单位为兆字节。
如果值为 0，则最大文件大小为无限制。
</td>
</tr>

<tr>
<td colspan="2">--log-flush-frequency duration&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：5s</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Maximum number of seconds between log flushes
-->
两次日志刷新之间的最大秒数
</td>
</tr>

<tr>
<td colspan="2">--logging-format string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值："text"</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Sets the log format. Permitted formats: "json", "text".<br/>Non-default formats don't honor these flags: --add_dir_header, --alsologtostderr, --log_backtrace_at, --log_dir, --log_file, --log_file_max_size, --logtostderr, --one_output, --skip_headers, --skip_log_headers, --stderrthreshold, --vmodule, --log-flush-frequency.<br/>Non-default choices are currently alpha and subject to change without warning.
-->
设置日志格式。允许的格式："json"，"json"。<br/>
非默认格式不支持以下标志：<code>--add-dir-header</code>、<code>--alsologtostderr</code>、<code>--log-backtrace-at</code>、<code>--log-dir</code>、<code>--log-file</code>、<code>--log-file-max-size</code>、<code>--logtostderr</code>、<code>--one-output</code>、<code>-skip-headers</code>、<code>-skip-log-headers</code>、<code>--stderrthreshold</code>、<code>-vmodule</code> 和 <code>--log-flush-frequency</code>。<br/>
当前非默认选择为 alpha，会随时更改而不会发出警告。
</td>
</tr>

<tr>
<td colspan="2">--logtostderr&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：true</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
log to standard error instead of files
-->
在标准错误而不是文件中输出日志记录。
</td>
</tr>

<tr>
<td colspan="2">--master-service-namespace string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值："default"</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
DEPRECATED: the namespace from which the Kubernetes master services should be injected into pods.
-->
已废弃：应该从其中将 Kubernetes 主服务注入到 Pod 中的名字空间。
</td>
</tr>

<tr>
<td colspan="2">--max-connection-bytes-per-sec int</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
If non-zero, throttle each user connection to this number of bytes/sec. Currently only applies to long-running requests.
-->
如果不为零，则将每个用户连接限制为该数（字节数/秒）。
当前仅适用于长时间运行的请求。
</td>
</tr>

<tr>
<td colspan="2">--max-mutating-requests-inflight int&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：200</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
The maximum number of mutating requests in flight at a given time. 
When the server exceeds this, it rejects requests. Zero for no limit.
-->
在给定时间内进行中变更类型请求的最大个数。
当超过该值时，服务将拒绝所有请求。
零表示无限制。
</td>
</tr>

<tr>
<td colspan="2">--max-requests-inflight int&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：400</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
The maximum number of non-mutating requests in flight at a given time. 
When the server exceeds this, it rejects requests. Zero for no limit.
-->
在给定时间内进行中非变更类型请求的最大数量。
当超过该值时，服务将拒绝所有请求。
零表示无限制。
</td>
</tr>

<tr>
<td colspan="2">--min-request-timeout int&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：1800</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--  
An optional field indicating the minimum number of seconds a handler must 
keep a request open before timing it out. Currently only honored by the 
watch request handler, which picks a randomized value above this number 
as the connection timeout, to spread out load.
-->
可选字段，表示处理程序在请求超时前，必须保持其处于打开状态的最小秒数。
当前只对监听（Watch）请求的处理程序有效，它基于这个值选择一个随机数作为连接超时值，
以达到分散负载的目的。
</td>
</tr>

<tr>
<td colspan="2">--oidc-ca-file string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
If set, the OpenID server's certificate will be verified by one of 
the authorities in the oidc-ca-file, otherwise the host's root CA set will be used.
-->
如果设置该值，将会使用 oidc-ca-file 中的机构之一对 OpenID 服务的证书进行验证，
否则将会使用主机的根 CA 对其进行验证。
</td>
</tr>

<tr>
<td colspan="2">--oidc-client-id string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
The client ID for the OpenID Connect client, must be set if oidc-issuer-url is set.
-->
OpenID 连接客户端的要使用的客户 ID，如果设置了 oidc-issuer-url，则必须设置这个值。
</td>
</tr>

<tr>
<td colspan="2">--oidc-groups-claim string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
If provided, the name of a custom OpenID Connect claim for specifying user groups. 
The claim value is expected to be a string or array of strings. 
This flag is experimental, please see the authentication documentation for further details.
-->
如果提供该值，这个自定义 OpenID 连接声明将被用来设定用户组。
该声明值需要是一个字符串或字符串数组。
此标志为实验性的，请查阅身份认证相关文档进一步了解详细信息。
</td>
</tr>

<tr>
<td colspan="2">--oidc-groups-prefix string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
If provided, all groups will be prefixed with this value to 
prevent conflicts with other authentication strategies.
-->
如果提供了此值，则所有组都将以该值作为前缀，以防止与其他身份认证策略冲突。
</td>
</tr>

<tr>
<td colspan="2">--oidc-issuer-url string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
The URL of the OpenID issuer, only HTTPS scheme will be accepted. 
If set, it will be used to verify the OIDC JSON Web Token (JWT).
-->
OpenID 颁发者 URL，只接受 HTTPS 方案。
如果设置该值，它将被用于验证 OIDC JSON Web Token(JWT)。
</td>
</tr>

<tr>
<td colspan="2">--oidc-required-claim &lt;逗号分隔的 'key=value' 键值对列表&gt;</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
A key=value pair that describes a required claim in the ID Token. 
If set, the claim is verified to be present in the ID Token with a matching value. 
Repeat this flag to specify multiple claims.
-->
描述 ID 令牌中必需声明的键值对。
如果设置此值，则会验证 ID 令牌中存在与该声明匹配的值。
重复此标志以指定多个声明。
</td>
</tr>

<tr>
<td colspan="2">--oidc-signing-algs strings&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：RS256</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Comma-separated list of allowed JOSE asymmetric signing algorithms. 
JWTs with a 'alg' header value not in this list will be rejected. 
Values are defined by RFC 7518 https://tools.ietf.org/html/rfc7518#section-3.1.
-->
允许的 JOSE 非对称签名算法的逗号分隔列表。
若 JWT 所带的 "alg" 标头值不在列表中，则该 JWT 将被拒绝。
取值依据 RFC 7518 https://tools.ietf.org/html/rfc7518#section-3.1 定义。
</td>
</tr>

<tr>
<td colspan="2">--oidc-username-claim string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值："sub"</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
The OpenID claim to use as the user name. Note that claims other than
 the default ('sub') is not guaranteed to be unique and immutable. 
 This flag is experimental, please see the authentication documentation for further details.
-->
要用作用户名的 OpenID 声明。
请注意，除默认声明（"sub"）以外的其他声明不能保证是唯一且不可变的。
此标志是实验性的，请参阅身份认证文档以获取更多详细信息。
</td>
</tr>

<tr>
<td colspan="2">--oidc-username-prefix string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
If provided, all usernames will be prefixed with this value. 
If not provided, username claims other than 'email' are prefixed
 by the issuer URL to avoid clashes. To skip any prefixing, provide the value '-'.
-->
如果提供，则所有用户名都将以该值作为前缀。
如果未提供，则除 "email" 之外的用户名声明都会添加颁发者 URL 作为前缀，以避免冲突。
要略过添加前缀处理，请设置值为 "-"。
</td>
</tr>

<tr>
<td colspan="2">--one-output</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
If true, only write logs to their native severity level (vs also writing to each lower severity level
-->
此标志为真时，日志只会被写入到其原生的严重性级别中（而不是同时写到所有较低
严重性级别中）。
</td>
</tr>

<tr>
<td colspan="2">--permit-address-sharing&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：false</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
<!--If true, SO_REUSEADDR will be used when binding the port. This allows binding to wildcard IPs like 0.0.0.0 and specific IPs in parallel, and it avoids waiting for the kernel to release sockets in TIME_WAIT state.
-->
若此标志为 true，则使用 <tt>SO_REUSEADDR</tt> 来绑定端口。
这样设置可以同时绑定到用通配符表示的类似 0.0.0.0 这种 IP 地址，
以及特定的 IP 地址。也可以避免等待内核释放 <tt>TIME_WAIT</tt> 状态的套接字。
</p></td>
</tr>

<tr>
<td colspan="2">--permit-port-sharing&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：false</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
If true, SO_REUSEPORT will be used when binding the port, 
which allows more than one instance to bind on the same address and port. [default=false]
-->
如果为 true，则在绑定端口时将使用 <tt>SO_REUSEPORT</tt>，
这样多个实例可以绑定到同一地址和端口上。
</td>
</tr>

<tr>
<td colspan="2">--profiling&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：true</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Enable profiling via web interface host:port/debug/pprof/
-->
通过 Web 接口 <code>host:port/debug/pprof/</code> 启用性能分析。
</td>
</tr>

<tr>
<td colspan="2">--proxy-client-cert-file string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Client certificate used to prove the identity of the aggregator or 
kube-apiserver when it must call out during a request. This includes 
proxying requests to a user api-server and calling out to webhook 
admission plugins. It is expected that this cert includes a signature 
from the CA in the --requestheader-client-ca-file flag. That CA is 
published in the 'extension-apiserver-authentication' configmap in 
the kube-system namespace. Components receiving calls from kube-aggregator 
should use that CA to perform their half of the mutual TLS verification.
-->
当必须调用外部程序以处理请求时，用于证明聚合器或者 kube-apiserver 的身份的客户端证书。
包括代理转发到用户 api-server 的请求和调用 Webhook 准入控制插件的请求。
Kubernetes 期望此证书包含来自于 --requestheader-client-ca-file 标志中所给 CA 的签名。
该 CA 在 kube-system 命名空间的 "extension-apiserver-authentication" ConfigMap 中公开。
从 kube-aggregator 收到调用的组件应该使用该 CA 进行各自的双向 TLS 验证。
</td>
</tr>

<tr>
<td colspan="2">--proxy-client-key-file string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Private key for the client certificate used to prove the identity of 
the aggregator or kube-apiserver when it must call out during a request. 
This includes proxying requests to a user api-server and calling out to 
webhook admission plugins.
-->
当必须调用外部程序来处理请求时，用来证明聚合器或者 kube-apiserver 的身份的客户端私钥。
这包括代理转发给用户 api-server 的请求和调用 Webhook 准入控制插件的请求。
</td>
</tr>

<tr>
<td colspan="2">--request-timeout duration&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：1m0s</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
An optional field indicating the duration a handler must keep a request 
open before timing it out. This is the default request timeout for 
requests but may be overridden by flags such as --min-request-timeout 
for specific types of requests.
-->
可选字段，指示处理程序在超时之前必须保持打开请求的持续时间。 
这是请求的默认请求超时，但对于特定类型的请求，可能会被
<code>--min-request-timeout</code>等标志覆盖。
</td>
</tr>

<tr>
<td colspan="2">--requestheader-allowed-names strings</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
List of client certificate common names to allow to provide usernames 
in headers specified by --requestheader-username-headers. If empty, 
any client certificate validated by the authorities in 
--requestheader-client-ca-file is allowed.
-->
此值为客户端证书通用名称（Common Name）的列表；表中所列的表项可以用来提供用户名，
方式是使用 <code>--requestheader-username-headers</code> 所指定的头部。
如果为空，能够通过 <code>--requestheader-client-ca-file</code> 中机构
认证的客户端证书都是被允许的。
</td>
</tr>

<tr>
<td colspan="2">--requestheader-client-ca-file string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Root certificate bundle to use to verify client certificates on 
incoming requests before trusting usernames in headers specified 
by --requestheader-username-headers. WARNING: generally do not 
depend on authorization being already done for incoming requests.
-->
在信任请求头中以 <code>--requestheader-username-headers</code> 指示的用户名之前，
用于验证接入请求中客户端证书的根证书包。
警告：一般不要假定传入请求已被授权。
</td>
</tr>

<tr>
<td colspan="2">--requestheader-extra-headers-prefix strings</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
List of request header prefixes to inspect. X-Remote-Extra- is suggested.
-->
用于查验请求头部的前缀列表。建议使用 <code>X-Remote-Extra-</code>。
</td>
</tr>

<tr>
<td colspan="2">--requestheader-group-headers strings</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
List of request headers to inspect for groups. X-Remote-Group is suggested.
-->
用于查验用户组的请求头部列表。建议使用 <code>X-Remote-Group</code>。
</td>
</tr>

<tr>
<td colspan="2">--requestheader-username-headers strings</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
List of request headers to inspect for usernames. X-Remote-User is common.
-->
用于查验用户名的请求头头列表。建议使用 <code>X-Remote-User</code>。
</td>
</tr>

<tr>
<td colspan="2">--runtime-config &lt;逗号分隔的 'key=value' 对列表&gt;</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
A set of key=value pairs that enable or disable built-in APIs. Supported options are:
<br/>v1=true|false for the core API group
<br/>&lt;group&gt;/&lt;version&gt;=true|false for a specific API group and version (e.g. apps/v1=true)
<br/>api/all=true|false controls all API versions
<br/>api/ga=true|false controls all API versions of the form v[0-9]+
<br/>api/beta=true|false controls all API versions of the form v[0-9]+beta[0-9]+
<br/>api/alpha=true|false controls all API versions of the form v[0-9]+alpha[0-9]+
<br/>api/legacy is deprecated, and will be removed in a future version
-->
一组启用或禁用内置 API 的键值对。支持的选项包括：
<br/>v1=true|false（针对核心 API 组）
<br/>&lt;group&gt;/&lt;version&gt;=true|false（针对特定 API 组和版本，例如：apps/v1=true） 
<br/>api/all=true|false 控制所有 API 版本
<br/>api/ga=true|false 控制所有 v[0-9]+ API 版本
<br/>api/beta=true|false 控制所有 v[0-9]+beta[0-9]+ API 版本
<br/>api/alpha=true|false 控制所有 v[0-9]+alpha[0-9]+ API 版本
<br/>api/legacy 已弃用，并将在以后的版本中删除
</td>
</tr>

<tr>
<td colspan="2">--secure-port int&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：6443</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
The port on which to serve HTTPS with authentication and authorization. 
It cannot be switched off with 0.
-->
带身份验证和鉴权机制的 HTTPS 服务端口。
不能用 0 关闭。
</td>
</tr>

<tr>
<td colspan="2">--service-account-extend-token-expiration&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：true</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Turns on projected service account expiration extension during token generation, 
which helps safe transition from legacy token to bound service account token feature. 
If this flag is enabled, admission injected tokens would be extended up to 
1 year to prevent unexpected failure during transition, ignoring value of service-account-max-token-expiration.
-->
在生成令牌时，启用投射服务帐户到期时间扩展，
这有助于从旧版令牌安全地过渡到绑定的服务帐户令牌功能。
如果启用此标志，则准入插件注入的令牌的过期时间将延长至 1 年，以防止过渡期间发生意外故障，
并忽略 service-account-max-token-expiration 的值。
</td>
</tr>

<tr>
<td colspan="2">--service-account-issuer string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Identifier of the service account token issuer. The issuer will assert this 
identifier in "iss" claim of issued tokens. This value is a string or URI. 
If this option is not a valid URI per the OpenID Discovery 1.0 spec, 
the ServiceAccountIssuerDiscovery feature will remain disabled, even if 
the feature gate is set to true. It is highly recommended that this value 
comply with the OpenID spec: https://openid.net/specs/openid-connect-discovery-1_0.html. 
In practice, this means that service-account-issuer must be an https URL. 
It is also highly recommended that this URL be capable of serving OpenID 
discovery documents at {service-account-issuer}/.well-known/openid-configuration.
-->
服务帐号令牌颁发者的标识符。
颁发者将在已办法令牌的 "iss" 声明中检查此标识符。
此值为字符串或 URI。
如果根据 OpenID Discovery 1.0 规范检查此选项不是有效的 URI，则即使特性门控设置为 true，
ServiceAccountIssuerDiscovery 功能也将保持禁用状态。 
强烈建议该值符合 OpenID 规范：https://openid.net/specs/openid-connect-discovery-1_0.html。 
实践中，这意味着 service-account-issuer 取值必须是 HTTPS URL。 
还强烈建议此 URL 能够在 {service-account-issuer}/.well-known/openid-configuration
处提供 OpenID 发现文档。
</td>
</tr>

<tr>
<td colspan="2">--service-account-jwks-uri string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Overrides the URI for the JSON Web Key Set in the discovery doc served at 
/.well-known/openid-configuration. This flag is useful if the discovery 
docand key set are served to relying parties from a URL other than the 
API server's external (as auto-detected or overridden with external-hostname). 
Only valid if the ServiceAccountIssuerDiscovery feature gate is enabled.
-->
覆盖 <code>/.well-known/openid-configuration</code> 提供的发现文档中 JSON Web 密钥集的 URI。
如果发现文档和密钥集是通过 API 服务器外部
（而非自动检测到或被外部主机名覆盖）之外的 URL 提供给依赖方的，则此标志很有用。
仅在启用 ServiceAccountIssuerDiscovery 特性门控的情况下有效。
</td>
</tr>

<tr>
<td colspan="2">--service-account-key-file strings</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
File containing PEM-encoded x509 RSA or ECDSA private or public keys,
used to verify ServiceAccount tokens. The specified file can contain 
multiple keys, and the flag can be specified multiple times with 
different files. If unspecified, --tls-private-key-file is used. 
Must be specified when --service-account-signing-key is provided
-->
包含 PEM 编码的 x509 RSA 或 ECDSA 私钥或公钥的文件，用于验证 ServiceAccount 令牌。
指定的文件可以包含多个键，并且可以使用不同的文件多次指定标志。
如果未指定，则使用 <code>--tls-private-key-file</code>。
提供 <code>--service-account-signing-key</code> 时必须指定。
</td>
</tr>

<tr>
<td colspan="2">--service-account-lookup&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：true</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
If true, validate ServiceAccount tokens exist in etcd as part of authentication.
-->
如果为 true，则在身份认证时验证 etcd 中是否存在 ServiceAccount 令牌。
</td>
</tr>

<tr>
<td colspan="2">--service-account-max-token-expiration duration</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
The maximum validity duration of a token created by the service account token issuer. 
If an otherwise valid TokenRequest with a validity duration larger than this value is requested, 
a token will be issued with a validity duration of this value.
-->
服务帐户令牌发布者创建的令牌的最长有效期。
如果请求有效期大于此值的有效令牌请求，将使用此值的有效期颁发令牌。
</td>
</tr>

<tr>
<td colspan="2">--service-account-signing-key-file string</td>
</tr>
<tr>

<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Path to the file that contains the current private key of the service account token issuer. 
The issuer will sign issued ID tokens with this private key. 
-->
包含服务帐户令牌颁发者当前私钥的文件的路径。
颁发者将使用此私钥签署所颁发的 ID 令牌。
</td>
</tr>

<tr>
<td colspan="2">--service-cluster-ip-range string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
A CIDR notation IP range from which to assign service cluster IPs. 
This must not overlap with any IP ranges assigned to nodes or pods.
-->
CIDR 表示的 IP 范围用来为服务分配集群 IP。
此地址不得与指定给节点或 Pod 的任何 IP 范围重叠。
</td>
</tr>

<tr>
<td colspan="2">--service-node-port-range &lt;形式为 'N1-N2' 的字符串&gt;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：30000-32767</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
A port range to reserve for services with NodePort visibility. 
Example: '30000-32767'. Inclusive at both ends of the range.
-->
保留给具有 NodePort 可见性的服务的端口范围。
例如："30000-32767"。范围的两端都包括在内。
</td>
</tr>

<tr>
<td colspan="2">--show-hidden-metrics-for-version string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
The previous version for which you want to show hidden metrics. Only the 
previous minor version is meaningful, other values will not be allowed. 
The format is &lt;major&gt;.&lt;minor&gt;, e.g.: '1.16'. The purpose of 
this format is make sure you have the opportunity to notice if the next
release hides additional metrics, rather than being surprised when they 
are permanently removed in the release after that.
-->
你要显示隐藏指标的先前版本。仅先前的次要版本有意义，不允许其他值。
格式为 &lt;major&gt;.&lt;minor&gt;，例如："1.16"。
这种格式的目的是确保你有机会注意到下一个版本是否隐藏了其他指标，
而不是在此之后将它们从发行版中永久删除时感到惊讶。
</td>
</tr>

<tr>
<td colspan="2">--shutdown-delay-duration duration</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Time to delay the termination. During that time the server keeps serving requests normally. 
The endpoints /healthz and /livez will return success, but /readyz immediately returns failure. 
Graceful termination starts after this delay has elapsed. 
This can be used to allow load balancer to stop sending traffic to this server.
-->
延迟终止时间。在此期间，服务器将继续正常处理请求。
端点 /healthz 和 /livez 将返回成功，但是 /readyz 立即返回失败。
在此延迟过去之后，将开始正常终止。
这可用于允许负载平衡器停止向该服务器发送流量。
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
如果为 true，日志消息中避免标题前缀。
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
如果为 true，则在打开日志文件时避免标题。
</td>
</tr>

<tr>
<td colspan="2">--stderrthreshold int&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：2</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
logs at or above this threshold go to stderr
-->
将达到或超过此阈值的日志写到标准错误输出
</td>
</tr>

<tr>
<td colspan="2">--storage-backend string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
The storage backend for persistence. Options: 'etcd3' (default).
-->
持久化存储后端。选项："etcd3"（默认）。
</td>
</tr>

<tr>
<td colspan="2">--storage-media-type string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值："application/vnd.kubernetes.protobuf"</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
The media type to use to store objects in storage. 
Some resources or storage backends may only support a specific media type and will ignore this setting.
-->
用于在存储中存储对象的媒体类型。
某些资源或存储后端可能仅支持特定的媒体类型，并且将忽略此设置。
</td>
</tr>

<tr>
<td colspan="2">--strict-transport-security-directives strings</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
<!--
List of directives for HSTS, comma separated. If this list is empty, then HSTS directives will not be added. Example: 'max-age=31536000,includeSubDomains,preload'
-->
为 HSTS 所设置的指令列表，用逗号分隔。
如果此列表为空，则不会添加 HSTS 指令。
例如： 'max-age=31536000,includeSubDomains,preload'
</p></td>
</tr>


<tr>
<td colspan="2">--tls-cert-file string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
File containing the default x509 Certificate for HTTPS. 
(CA cert, if any, concatenated after server cert).
If HTTPS serving is enabled, and --tls-cert-file and --tls-private-key-file are not provided, 
a self-signed certificate and key are generated for 
the public address and saved to the directory specified by --cert-dir.
-->
包含用于 HTTPS 的默认 x509 证书的文件。（CA 证书（如果有）在服务器证书之后并置）。
如果启用了 HTTPS 服务，并且未提供 <code>--tls-cert-file</code> 和
<code>--tls-private-key-file</code>，
为公共地址生成一个自签名证书和密钥，并将其保存到 <code>--cert-dir</code> 指定的目录中。
</td>
</tr>

<tr>
<td colspan="2">--tls-cipher-suites strings</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Comma-separated list of cipher suites for the server. 
If omitted, the default Go cipher suites will be used. 
<br/>Preferred values:
TLS_AES_128_GCM_SHA256, TLS_AES_256_GCM_SHA384, TLS_CHACHA20_POLY1305_SHA256, TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA, TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256, TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA, TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384, TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305, TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256, TLS_ECDHE_RSA_WITH_3DES_EDE_CBC_SHA, TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA, TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256, TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA, TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384, TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305, TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256, TLS_RSA_WITH_3DES_EDE_CBC_SHA, TLS_RSA_WITH_AES_128_CBC_SHA, TLS_RSA_WITH_AES_128_GCM_SHA256, TLS_RSA_WITH_AES_256_CBC_SHA, TLS_RSA_WITH_AES_256_GCM_SHA384.<br/>
Insecure values: 
TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256, TLS_ECDHE_ECDSA_WITH_RC4_128_SHA, TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256, TLS_ECDHE_RSA_WITH_RC4_128_SHA, TLS_RSA_WITH_AES_128_CBC_SHA256, TLS_RSA_WITH_RC4_128_SHA.
-->
服务器的密码套件的列表，以逗号分隔。如果省略，将使用默认的 Go 密码套件。
<br/>首选值：
TLS_AES_128_GCM_SHA256、TLS_AES_256_GCM_SHA384、TLS_CHACHA20_POLY1305_SHA256、TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA、TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256、TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA、TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384、TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305、TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256、TLS_ECDHE_RSA_WITH_3DES_EDE_CBC_SHA、TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA、TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256、TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA、TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384、TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305、TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256、TLS_RSA_WITH_3DES_EDE_CBC_SHA、TLS_RSA_WITH_AES_128_CBC_SHA、TLS_RSA_WITH_AES_128_GCM_SHA256、 TLS_RSA_WITH_AES_256_CBC_SHA, TLS_RSA_WITH_AES_256_GCM_SHA384.
不安全的值有：
TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256、TLS_ECDHE_ECDSA_WITH_RC4_128_SHA、TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256、TLS_ECDHE_RSA_WITH_RC4_128_SHA、TLS_RSA_WITH_AES_128_CBC_SHA256、TLS_RSA_WITH_RC4_128_SHA。
</td>
</tr>

<tr>
<td colspan="2">--tls-min-version string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Minimum TLS version supported. Possible values: VersionTLS10, VersionTLS11, VersionTLS12, VersionTLS13
-->
支持的最低 TLS 版本。可能的值：VersionTLS10，VersionTLS11，VersionTLS12，VersionTLS13
</td>
</tr>

<tr>
<td colspan="2">--tls-private-key-file string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
File containing the default x509 private key matching --tls-cert-file.
-->
包含匹配 <code>--tls-cert-file</code> 的 x509 证书私钥的文件。
</td>
</tr>

<tr>
<td colspan="2">--tls-sni-cert-key string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值： []</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
A pair of x509 certificate and private key file paths, optionally 
suffixed with a list of domain patterns which are fully qualified 
domain names, possibly with prefixed wildcard segments. The domain 
patterns also allow IP addresses, but IPs should only be used if 
the apiserver has visibility to the IP address requested by a client. 
If no domain patterns are provided, the names of the certificate are 
extracted. Non-wildcard matches trump over wildcard matches, explicit
domain patterns trump over extracted names. For multiple key/certificate 
pairs, use the --tls-sni-cert-key multiple times. Examples: 
"example.crt,example.key" or "foo.crt,foo.key:*.foo.com,foo.com".
-->
一对 x509 证书和私钥文件路径，（可选）后缀为全限定域名的域名模式列表，可以使用带有通配符的前缀。
域模式也允许使用 IP 地址，但仅当 apiserver 对客户端请求的IP地址具有可见性时，才应使用 IP。
如果未提供域模式，则提取证书的名称。
非通配符匹配优先于通配符匹配，显式域模式优先于提取出的名称。
对于多个密钥/证书对，请多次使用 <code>--tls-sni-cert-key</code>。
示例："example.crt,example.key" 或 "foo.crt,foo.key:\*.foo.com,foo.com"。
</td>
</tr>

<tr>
<td colspan="2">--token-auth-file string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
If set, the file that will be used to secure the secure port of the API server via token authentication.
-->
如果设置该值，这个文件将被用于通过令牌认证来保护 API 服务的安全端口。
</td>
</tr>

<tr>
<td colspan="2">-v, --v int</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
number for the log level verbosity
-->
日志级别详细程度的数字。
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
打印版本信息并退出
</td>
</tr>

<tr>
<td colspan="2">--vmodule &lt;用逗号分隔的多个 'pattern=N' 配置字符串&gt;</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
comma-separated list of pattern=N settings for file-filtered logging
-->
以逗号分隔的 <code>pattern=N</code> 设置列表，用于文件过滤的日志记录。
</td>
</tr>

<tr>
<td colspan="2">--watch-cache&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：true</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Enable watch caching in the apiserver
-->
在 API 服务器中启用监视缓存。
</td>
</tr>

<tr>
<td colspan="2">--watch-cache-sizes strings</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Watch cache size settings for some resources (pods, nodes, etc.), comma separated. 
The individual setting format: resource[.group]#size, where resource is lowercase 
plural (no version), group is omitted for resources of apiVersion v1 (the legacy 
core API) and included for others, and size is a number. It takes effect when 
watch-cache is enabled. Some resources (replicationcontrollers, endpoints, nodes,
pods, services, apiservices.apiregistration.k8s.io) have system defaults set by 
heuristics, others default to default-watch-cache-size
-->
某些资源（Pods、Nodes 等）的监视缓存大小设置，以逗号分隔。
每个资源对应的设置格式：<code>resource[.group]#size</code>，其中
<code>resource</code> 为小写复数（无版本），
对于 apiVersion v1（旧版核心 API）的资源要省略 <code>group</code>，
对其它资源要给出 <code>group</code>；<code>size 为一个数字</code>。
启用 <code>watch-cache</code> 时，此功能生效。
某些资源（<code>replicationcontrollers</code>、<code>endpoints</code>、
<code>nodes</code>、<code>pods</code>、<code>services</code>、
<code>apiservices.apiregistration.k8s.io</code>）
具有通过启发式设置的系统默认值，其他资源默认为
<code>default-watch-cache-size<code>。
</td>
</tr>

</tbody>
</table>

