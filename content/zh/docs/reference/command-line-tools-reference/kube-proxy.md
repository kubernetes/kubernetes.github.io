---
title: kube-proxy
content_type: tool-reference
weight: 30
---
<!-- 
title: kube-proxy
content_type: tool-reference
weight: 28
-->

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
The Kubernetes network proxy runs on each node. This
reflects services as defined in the Kubernetes API on each node and can do simple
TCP, UDP, and SCTP stream forwarding or round robin TCP, UDP, and SCTP forwarding across a set of backends.
Service cluster IPs and ports are currently found through Docker-links-compatible
environment variables specifying ports opened by the service proxy. There is an optional
addon that provides cluster DNS for these cluster IPs. The user must create a service
with the apiserver API to configure the proxy.
-->
Kubernetes 网络代理在每个节点上运行。网络代理反映了每个节点上 Kubernetes API
中定义的服务，并且可以执行简单的 TCP、UDP 和 SCTP 流转发，或者在一组后端进行
循环 TCP、UDP 和 SCTP 转发。
当前可通过 Docker-links-compatible 环境变量找到服务集群 IP 和端口，
这些环境变量指定了服务代理打开的端口。
有一个可选的插件，可以为这些集群 IP 提供集群 DNS。
用户必须使用 apiserver API 创建服务才能配置代理。

```
kube-proxy [flags]
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
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
<!--
If true, adds the file directory to the header of the log messages
-->
若此标志为 true，则将文件目录添加到日志消息的头部。
</p></td>
</tr>

<tr>
<td colspan="2">--alsologtostderr</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
<!--
log to standard error as well as files
-->
将日志输出到文件时也输出到标准错误输出（stderr）。
</p></td>
</tr>

<tr>
<td colspan="2">--azure-container-registry-config string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
<!--
Path to the file containing Azure container registry configuration information.
-->
包含 Azure 容器仓库配置信息的文件的路径。
</p>
</td>
</tr>

<tr>
<td colspan="2">--bind-address 0.0.0.0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：0.0.0.0</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
<!--
The IP address for the proxy server to serve on (set to '0.0.0.0' for all IPv4 interfaces and '::' for all IPv6 interfaces)
-->
代理服务器要使用的 IP 地址（设置为 '0.0.0.0' 表示要使用所有 IPv4 接口；
设置为 '::' 表示使用所有 IPv6 接口）。
</p>
</td>
</tr>

<tr>
<td colspan="2">--bind-address-hard-fail</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
<!--
If true kube-proxy will treat failure to bind to a port as fatal and exit
-->
若此标志为 true，kube-proxy 会将无法绑定端口的失败操作视为致命错误并退出。
</p></td>
</tr>

<tr>
<td colspan="2">--boot-id-file string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值："/proc/sys/kernel/random/boot_id"</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
<!--
Comma-separated list of files to check for boot-id. Use the first one that exists.
-->
用来检查 Boot-ID 的文件名，用逗号隔开。
第一个存在的文件会被使用。
</p></td>
</tr>

<tr>
<td colspan="2">--cleanup</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
<!--
If true cleanup iptables and ipvs rules and exit.
-->
如果为 true，清理 iptables 和 ipvs 规则并退出。
</p>
</td>
</tr>

<tr>
<td colspan="2">--cluster-cidr string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
<!--
The CIDR range of pods in the cluster. When configured, traffic sent to a Service cluster IP from outside this range will be masqueraded and traffic sent from pods to an external LoadBalancer IP will be directed to the respective cluster IP instead
-->
集群中 Pod 的 CIDR 范围。配置后，将从该范围之外发送到服务集群 IP
的流量被伪装，从 Pod 发送到外部 LoadBalancer IP 的流量将被重定向
到相应的集群 IP。
</p>
</td>
</tr>

<tr>
<td colspan="2">--config string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
<!--
The path to the configuration file.
-->
配置文件的路径。
</p>
</td>
</tr>

<tr>
<td colspan="2">--config-sync-period duration&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：15m0s</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
<!--
How often configuration from the apiserver is refreshed.  Must be greater than 0.
-->
来自 apiserver 的配置的刷新频率。必须大于 0。
</p>
</td>
</tr>

<tr>
<td colspan="2">--conntrack-max-per-core int32&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：32768</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
<!--
Maximum number of NAT connections to track per CPU core (0 to leave the limit as-is and ignore conntrack-min).
-->
每个 CPU 核跟踪的最大 NAT 连接数（0 表示保留当前限制并忽略 conntrack-min 设置）。
</p>
</td>
</tr>

<tr>
<td colspan="2">--conntrack-min int32&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：131072</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
<!--
Minimum number of conntrack entries to allocate, regardless of conntrack-max-per-core (set conntrack-max-per-core=0 to leave the limit as-is).
-->
无论 <code>conntrack-max-per-core</code> 多少，要分配的 conntrack
条目的最小数量（将 <code>conntrack-max-per-core</code> 设置为 0 即可
保持当前的限制）。
</p>
</td>
</tr>

<tr>
<td colspan="2">--conntrack-tcp-timeout-close-wait duration&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：1h0m0s
</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
<!--
NAT timeout for TCP connections in the CLOSE_WAIT state
-->
处于 <code>CLOSE_WAIT</code> 状态的 TCP 连接的 NAT 超时。
</p>
</td>
</tr>

<tr>
<td colspan="2">--conntrack-tcp-timeout-established duration&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：24h0m0s</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
<!--
Idle timeout for established TCP connections (0 to leave as-is)
-->
已建立的 TCP 连接的空闲超时（0 保持当前设置）。
</p>
</td>
</tr>

<tr>
<td colspan="2">--detect-local-mode LocalMode</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
<!-- Mode to use to detect local traffic -->
用于检测本地流量的模式。
</p>
</td>
</tr>

<tr>
<td colspan="2">--feature-gates &lt;<!--comma-separated 'key=True|False' pairs-->逗号分隔的 'key=True|False' 对’&gt;</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
<!--
A set of key=value pairs that describe feature gates for alpha/experimental features. Options are:
<br/>
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
一组键=值（key=value）对，描述了 alpha/experimental 的特征。可选项有：
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
ExperimentalHostUserNamespaceDefaulting=true|false (BETA - 默认值=false)<br/>
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
WindowsEndpointSliceProxying=true|false (BETA - 默认值=true)
</p>
</td>
</tr>

<tr>
<td colspan="2">--healthz-bind-address 0.0.0.0&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：<code>0.0.0.0:10256</code></td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
<!--  
The IP address with port for the health check server to serve on 
(set to '0.0.0.0:10256' for all IPv4 interfaces and '[::]:10256' for all IPv6 interfaces). 
Set empty to disable.
-->
服务健康状态检查的 IP 地址和端口（设置为 '0.0.0.0:10256' 表示使用所有
IPv4 接口，设置为 '[::]:10256' 表示使用所有 IPv6 接口）；
设置为空则禁用。
</p>
</td>
</tr>

<tr>
<td colspan="2">-h, --help</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
<!--
help for kube-proxy
-->
kube-proxy 操作的帮助命令。
</p>
</td>
</tr>

<tr>
<td colspan="2">--hostname-override string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
<!--
If non-empty, will use this string as identification instead of the actual hostname.
-->
如果非空，将使用此字符串而不是实际的主机名作为标识。
</p>
</td>
</tr>

<tr>
<td colspan="2">--iptables-masquerade-bit int32&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：14</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
<!--
If using the pure iptables proxy, the bit of the fwmark space to mark packets requiring SNAT with.  Must be within the range [0, 31].
-->
在使用纯 iptables 代理时，用来设置 fwmark 空间的 bit，标记需要
SNAT 的数据包。必须在 [0,31] 范围内。
</p>
</td>
</tr>

<tr>
<td colspan="2">--iptables-min-sync-period duration&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：1s</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
<!--
The minimum interval of how often the iptables rules can be refreshed as endpoints and services change (e.g. '5s', '1m', '2h22m').
-->
iptables 规则可以随着端点和服务的更改而刷新的最小间隔（例如 '5s'、'1m'、'2h22m'）。
</p>
</td>
</tr>

<tr>
<td colspan="2">--iptables-sync-period duration&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：30s</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
<!--
The maximum interval of how often iptables rules are refreshed (e.g. '5s', '1m', '2h22m').  Must be greater than 0.
-->
刷新 iptables 规则的最大间隔（例如 '5s'、'1m'、'2h22m'）。必须大于 0。
</p>
</td>
</tr>

<tr>
<td colspan="2">--ipvs-exclude-cidrs strings</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
<!--
A comma-separated list of CIDR's which the ipvs proxier should not touch when cleaning up IPVS rules.
-->
逗号分隔的 CIDR 列表，ipvs 代理在清理 IPVS 规则时不会此列表中的地址范围。
</p>
</td>
</tr>

<tr>
<td colspan="2">--ipvs-min-sync-period duration</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
<!--
The minimum interval of how often the ipvs rules can be refreshed as endpoints and services change (e.g. '5s', '1m', '2h22m').
-->
ipvs 规则可以随着端点和服务的更改而刷新的最小间隔（例如 '5s'、'1m'、'2h22m'）。
</p>
</td>
</tr>

<tr>
<td colspan="2">--ipvs-scheduler string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
<!--
The ipvs scheduler type when proxy mode is ipvs
-->
代理模式为 ipvs 时所选的 ipvs 调度器类型。
</p>
</td>
</tr>

<tr>
<td colspan="2">--ipvs-strict-arp</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
<!--
Enable strict ARP by setting arp_ignore to 1 and arp_announce to 2
-->
通过将 <code>arp_ignore</code> 设置为 1 并将 <code>arp_announce</code>
设置为 2 启用严格的 ARP。
</p>
</td>
</tr>

<tr>
<td colspan="2">--ipvs-sync-period duration&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：30s</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
<!--
The maximum interval of how often ipvs rules are refreshed (e.g. '5s', '1m', '2h22m').  Must be greater than 0.
-->
刷新 ipvs 规则的最大间隔（例如 '5s'、'1m'、'2h22m'）。必须大于 0。
</p>
</td>
</tr>


<tr>
<td colspan="2">--ipvs-tcp-timeout duration</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
<!--  
The timeout for idle IPVS TCP connections, 0 to leave as-is. (e.g. '5s', '1m', '2h22m').
-->
空闲 IPVS TCP 连接的超时时间，0 保持连接（例如 '5s'、'1m'、'2h22m'）。
</p>
</td>
</tr>

<tr>
<td colspan="2">--ipvs-tcpfin-timeout duration</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
<!--  
The timeout for IPVS TCP connections after receiving a FIN packet, 0 to leave as-is. (e.g. '5s', '1m', '2h22m').
-->
收到 FIN 数据包后，IPVS TCP 连接的超时，0 保持当前设置不变。（例如 '5s'、'1m'、'2h22m'）。
</p>
</td>
</tr>

<tr>
<td colspan="2">--ipvs-udp-timeout duration</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
<!--  
The timeout for IPVS UDP packets, 0 to leave as-is. (e.g. '5s', '1m', '2h22m').
-->
IPVS UDP 数据包的超时，0 保持当前设置不变。（例如 '5s'、'1m'、'2h22m'）。
</p>
</td>
</tr>

<tr>
<td colspan="2">--kube-api-burst int32&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：10</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
<!--
Burst to use while talking with kubernetes apiserver
-->
与 kubernetes apiserver 通信的突发数量。
</p>
</td>
</tr>

<tr>
<td colspan="2">--kube-api-content-type string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值："application/vnd.kubernetes.protobuf"</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
<!--
Content type of requests sent to apiserver.
-->
发送到 apiserver 的请求的内容类型。
</p>
</td>
</tr>

<tr>
<td colspan="2">--kube-api-qps float32&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：5</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
<!--
QPS to use while talking with kubernetes apiserver
-->
与 kubernetes apiserver 交互时使用的 QPS。
</p>
</td>
</tr>

<tr>
<td colspan="2">--kubeconfig string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
<!--
Path to kubeconfig file with authorization information (the master location is set by the master flag).
-->
包含鉴权信息的 kubeconfig 文件的路径（主控节点位置由 master 标志设置）。
</p>
</td>
</tr>

<tr>
<td colspan="2">--log-backtrace-at &lt;<!--a string in the form 'file:N'-->形式为 'file:N' 的字符串&gt;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: :0</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
<!--
when logging hits line file:N, emit a stack trace
-->
当日志逻辑执行到文件 file 的第 N 行时，输出调用堆栈跟踪。
</p></td>

</tr>

<tr>
<td colspan="2">--log-dir string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
<!--
If non-empty, write log files in this directory
-->
若此标志费控，则将日志文件写入到此标志所给的目录下。
</p>
</td>
</tr>

<tr>
<td colspan="2">--log-file string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
<!--
If non-empty, use this log file
-->
若此标志非空，则该字符串作为日志文件名。
</p></td>
</tr>

<tr>
<td colspan="2">--log-file-max-size uint&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：1800</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
<!--
Defines the maximum size a log file can grow to. Unit is megabytes. If the value is 0, the maximum file size is unlimited.
-->
定义日志文件可增长到的最大尺寸。单位是兆字节（MB）。
如果此值为 0，则最大文件大小无限制。
</p></td>
</tr>


<tr>
<td colspan="2">--log-flush-frequency duration&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：5s
</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">
<!--
Maximum number of seconds between log flushes
-->
两次日志刷新之间的最大秒数。
</td>
</tr>

<tr>
<td colspan="2">--machine-id-file string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值："/etc/machine-id,/var/lib/dbus/machine-id"</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
<!--
Comma-separated list of files to check for machine-id. Use the first one that exists.
-->
用来检查 Machine-ID 的文件列表，用逗号分隔。
使用找到的第一个文件。
</p></td>
</tr>

<tr>
<td colspan="2">--masquerade-all</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
<!--
If using the pure iptables proxy, SNAT all traffic sent via Service cluster IPs (this not commonly needed)
-->
如果使用纯 iptables 代理，则对通过服务集群 IP 发送的所有流量
进行 SNAT（通常不需要）。
</p>
</td>
</tr>

<tr>
<td colspan="2">--master string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
<!--
The address of the Kubernetes API server (overrides any value in kubeconfig)
-->
Kubernetes API 服务器的地址（覆盖 kubeconfig 中的相关值）。
</p>
</td>
</tr>

<tr>
<td colspan="2">--metrics-bind-address ipport&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：<code>127.0.0.1:10249</code></td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
<!--
The IP address with port for the metrics server to serve on 
(set to '0.0.0.0:10249' for all IPv4 interfaces and '[::]:10249' for all IPv6 interfaces). 
Set empty to disable.
-->
metrics 服务器要使用的 IP 地址和端口
（设置为 '0.0.0.0:10249' 则使用所有 IPv4 接口，设置为 '[::]:10249' 则使用所有 IPv6 接口）
设置为空则禁用。
</p>
</td>
</tr>

<tr>
<td colspan="2">--nodeport-addresses strings</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
<!--
A string slice of values which specify the addresses to use for NodePorts. Values may be valid IP blocks (e.g. 1.2.3.0/24, 1.2.3.4/32). The default empty string slice ([]) means to use all local addresses.
-->
一个字符串值，指定用于 NodePort 服务的地址。
值可以是有效的 IP 块（例如 1.2.3.0/24, 1.2.3.4/32）。
默认的空字符串切片（[]）表示使用所有本地地址。
</p>
</td>
</tr>

<tr>
<td colspan="2">--one-output</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
<!--
If true, only write logs to their native severity level (vs also writing to each lower severity level)
-->
若此标志为 true，则仅将日志写入到其原本的严重性级别之下
（而不是将其写入到所有更低严重性级别中）。
</p></td>
</tr>

<tr>
<td colspan="2">--oom-score-adj int32&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：-999</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
<!--
The oom-score-adj value for kube-proxy process. Values must be within the range [-1000, 1000]
-->
kube-proxy 进程中的 oom-score-adj 值，必须在 [-1000,1000] 范围内。
</p>
</td>
</tr>

<tr>
<td colspan="2">--profiling</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
<!--
If true enables profiling via web interface on /debug/pprof handler.
-->
如果为 true，则通过 Web 接口 <code>/debug/pprof</code> 启用性能分析。
</p>
</td>
</tr>

<tr>
<td colspan="2">--proxy-mode string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
<!--
Which proxy mode to use: 'userspace' (older) or 'iptables' (faster) or 'ipvs'. If blank, use the best-available proxy (currently iptables).  If the iptables proxy is selected, regardless of how, but the system's kernel or iptables versions are insufficient, this always falls back to the userspace proxy.
-->
使用哪种代理模式：'userspace'（较旧）或 'iptables'（较快）或 'ipvs'。
如果为空，使用最佳可用代理（当前为 iptables）。
如果选择了 iptables 代理（无论是否为显式设置），但系统的内核或
iptables 版本较低，总是会回退到 userspace 代理。
</p>
</td>
</tr>

<tr>
<td colspan="2">--proxy-port-range port-range</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
<!--
Range of host ports (beginPort-endPort, single port or beginPort+offset, inclusive) that may be consumed in order to proxy service traffic. If (unspecified, 0, or 0-0) then ports will be randomly chosen.
-->
可以用来代理服务流量的主机端口范围（包括'起始端口-结束端口'、
'单个端口'、'起始端口+偏移'几种形式）。
如果未指定或者设置为 0（或 0-0），则随机选择端口。
</p>
</td>
</tr>

<tr>
<td colspan="2">--show-hidden-metrics-for-version string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
<!--  
The previous version for which you want to show hidden metrics. Only the previous minor version is meaningful, other values will not be allowed. The format is &lt;major&gt;.&lt;minor&gt;, e.g.: '1.16'. The purpose of this format is make sure you have the opportunity to notice if the next release hides additional metrics, rather than being surprised when they are permanently removed in the release after that.
-->
要显示隐藏指标的先前版本。 
仅先前的次要版本有意义，不允许其他值。
格式为 &lt;major&gt;.&lt;minor&gt; ，例如：'1.16'。 
这种格式的目的是确保你有机会注意到下一个发行版是否隐藏了其他指标，
而不是在之后将其永久删除时感到惊讶。
</p>
</td>
</tr>

<tr>
<td colspan="2">--skip-headers</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
<!--
If true, avoid header prefixes in the log messages
-->
若此标志为 true，则避免在日志消息中包含头部前缀。
</p></td>
</tr>

<tr>
<td colspan="2">--skip-log-headers</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
<!--
If true, avoid headers when opening log files
-->
如果此标志为 true，则避免在打开日志文件时使用头部。
</p></td>
</tr>

<tr>
<td colspan="2">--stderrthreshold int&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：2</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
<!--
logs at or above this threshold go to stderr
-->
如果日志消息处于或者高于此阈值所设置的级别，则将其输出到标准错误输出（stderr）。
</p></td>
</tr>

<tr>
<td colspan="2">--udp-timeout duration&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<!--Default:-->默认值：250ms</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
<!--
How long an idle UDP connection will be kept open (e.g. '250ms', '2s').  Must be greater than 0. Only applicable for proxy-mode=userspace
-->
空闲 UDP 连接将保持打开的时长（例如 '250ms'，'2s'）。必须大于 0。
仅适用于 proxy-mode=userspace。
</p>
</td>
</tr>

<tr>
<td colspan="2">-v, --v int</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
<!--
number for the log level verbosity
-->
用来设置日志详细程度的数值。
</p></td>
</tr>

<tr>
<td colspan="2">--version version[=true]</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
<!--
Print version information and quit
-->
打印版本信息并退出。
</p>
</td>
</tr>

<tr>
<td colspan="2">--vmodule &lt;<!--comma-separated 'pattern=N' settings-->逗号分隔的 'pattern=N' 设置’&gt;</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
<!--
comma-separated list of pattern=N settings for file-filtered logging
-->
用逗号分隔的列表，其中每一项为 'pattern=N' 格式。
用来支持基于文件过滤的日志机制。
</p></td>
</tr>

<tr>
<td colspan="2">--write-config-to string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"><p>
<!--
If set, write the default configuration values to this file and exit.
-->
如果设置，将默认配置信息写入此文件并退出。
</p>
</td>
</tr>

</tbody>
</table>




