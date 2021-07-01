---
title: Kubelet Configuration (v1beta1)
content_type: tool-reference
package: kubelet.config.k8s.io/v1beta1
auto_generated: true
---


## Resource Types 


- [KubeletConfiguration](#kubelet-config-k8s-io-v1beta1-KubeletConfiguration)
- [SerializedNodeConfigSource](#kubelet-config-k8s-io-v1beta1-SerializedNodeConfigSource)
  
    

## `LoggingConfiguration`     {#LoggingConfiguration}
    



**Appears in:**

- [KubeletConfiguration](#kubelet-config-k8s-io-v1beta1-KubeletConfiguration)


LoggingConfiguration contains logging options
Refer [Logs Options](https://github.com/kubernetes/component-base/blob/master/logs/options.go) for more information.

<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
<tbody>
    

  
<tr><td><code>format</code> <B>[Required]</B><br/>
<code>string</code>
</td>
<td>
   Format Flag specifies the structure of log messages.
default value of format is `text`</td>
</tr>
    
  
<tr><td><code>sanitization</code> <B>[Required]</B><br/>
<code>bool</code>
</td>
<td>
   [Experimental] When enabled prevents logging of fields tagged as sensitive (passwords, keys, tokens).
Runtime log sanitization may introduce significant computation overhead and therefore should not be enabled in production.`)</td>
</tr>
    
  
</tbody>
</table>
  
    


## `KubeletConfiguration`     {#kubelet-config-k8s-io-v1beta1-KubeletConfiguration}
    




KubeletConfiguration contains the configuration for the Kubelet

<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
<tbody>
    
<tr><td><code>apiVersion</code><br/>string</td><td><code>kubelet.config.k8s.io/v1beta1</code></td></tr>
<tr><td><code>kind</code><br/>string</td><td><code>KubeletConfiguration</code></td></tr>
    

  
  
<tr><td><code>enableServer</code> <B>[Required]</B><br/>
<code>bool</code>
</td>
<td>
   enableServer enables Kubelet's secured server.
Note: Kubelet's insecure port is controlled by the readOnlyPort option.
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
it may disrupt components that interact with the Kubelet server.
Default: true</td>
</tr>
    
  
<tr><td><code>staticPodPath</code><br/>
<code>string</code>
</td>
<td>
   staticPodPath is the path to the directory containing local (static) pods to
run, or the path to a single static pod file.
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
the set of static pods specified at the new path may be different than the
ones the Kubelet initially started with, and this may disrupt your node.
Default: ""</td>
</tr>
    
  
<tr><td><code>syncFrequency</code><br/>
<a href="https://godoc.org/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
</td>
<td>
   syncFrequency is the max period between synchronizing running
containers and config.
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
shortening this duration may have a negative performance impact, especially
as the number of Pods on the node increases. Alternatively, increasing this
duration will result in longer refresh times for ConfigMaps and Secrets.
Default: "1m"</td>
</tr>
    
  
<tr><td><code>fileCheckFrequency</code><br/>
<a href="https://godoc.org/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
</td>
<td>
   fileCheckFrequency is the duration between checking config files for
new data
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
shortening the duration will cause the Kubelet to reload local Static Pod
configurations more frequently, which may have a negative performance impact.
Default: "20s"</td>
</tr>
    
  
<tr><td><code>httpCheckFrequency</code><br/>
<a href="https://godoc.org/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
</td>
<td>
   httpCheckFrequency is the duration between checking http for new data
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
shortening the duration will cause the Kubelet to poll staticPodURL more
frequently, which may have a negative performance impact.
Default: "20s"</td>
</tr>
    
  
<tr><td><code>staticPodURL</code><br/>
<code>string</code>
</td>
<td>
   staticPodURL is the URL for accessing static pods to run
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
the set of static pods specified at the new URL may be different than the
ones the Kubelet initially started with, and this may disrupt your node.
Default: ""</td>
</tr>
    
  
<tr><td><code>staticPodURLHeader</code><br/>
<code>map[string][]string</code>
</td>
<td>
   staticPodURLHeader is a map of slices with HTTP headers to use when accessing the podURL
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
it may disrupt the ability to read the latest set of static pods from StaticPodURL.
Default: nil</td>
</tr>
    
  
<tr><td><code>address</code><br/>
<code>string</code>
</td>
<td>
   address is the IP address for the Kubelet to serve on (set to 0.0.0.0
for all interfaces).
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
it may disrupt components that interact with the Kubelet server.
Default: "0.0.0.0"</td>
</tr>
    
  
<tr><td><code>port</code><br/>
<code>int32</code>
</td>
<td>
   port is the port for the Kubelet to serve on.
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
it may disrupt components that interact with the Kubelet server.
Default: 10250</td>
</tr>
    
  
<tr><td><code>readOnlyPort</code><br/>
<code>int32</code>
</td>
<td>
   readOnlyPort is the read-only port for the Kubelet to serve on with
no authentication/authorization.
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
it may disrupt components that interact with the Kubelet server.
Default: 0 (disabled)</td>
</tr>
    
  
<tr><td><code>tlsCertFile</code><br/>
<code>string</code>
</td>
<td>
   tlsCertFile is the file containing x509 Certificate for HTTPS. (CA cert,
if any, concatenated after server cert). If tlsCertFile and
tlsPrivateKeyFile are not provided, a self-signed certificate
and key are generated for the public address and saved to the directory
passed to the Kubelet's --cert-dir flag.
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
it may disrupt components that interact with the Kubelet server.
Default: ""</td>
</tr>
    
  
<tr><td><code>tlsPrivateKeyFile</code><br/>
<code>string</code>
</td>
<td>
   tlsPrivateKeyFile is the file containing x509 private key matching tlsCertFile
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
it may disrupt components that interact with the Kubelet server.
Default: ""</td>
</tr>
    
  
<tr><td><code>tlsCipherSuites</code><br/>
<code>[]string</code>
</td>
<td>
   TLSCipherSuites is the list of allowed cipher suites for the server.
Values are from tls package constants (https://golang.org/pkg/crypto/tls/#pkg-constants).
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
it may disrupt components that interact with the Kubelet server.
Default: nil</td>
</tr>
    
  
<tr><td><code>tlsMinVersion</code><br/>
<code>string</code>
</td>
<td>
   TLSMinVersion is the minimum TLS version supported.
Values are from tls package constants (https://golang.org/pkg/crypto/tls/#pkg-constants).
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
it may disrupt components that interact with the Kubelet server.
Default: ""</td>
</tr>
    
  
<tr><td><code>rotateCertificates</code><br/>
<code>bool</code>
</td>
<td>
   rotateCertificates enables client certificate rotation. The Kubelet will request a
new certificate from the certificates.k8s.io API. This requires an approver to approve the
certificate signing requests.
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
disabling it may disrupt the Kubelet's ability to authenticate with the API server
after the current certificate expires.
Default: false</td>
</tr>
    
  
<tr><td><code>serverTLSBootstrap</code><br/>
<code>bool</code>
</td>
<td>
   serverTLSBootstrap enables server certificate bootstrap. Instead of self
signing a serving certificate, the Kubelet will request a certificate from
the certificates.k8s.io API. This requires an approver to approve the
certificate signing requests. The RotateKubeletServerCertificate feature
must be enabled.
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
disabling it will stop the renewal of Kubelet server certificates, which can
disrupt components that interact with the Kubelet server in the long term,
due to certificate expiration.
Default: false</td>
</tr>
    
  
<tr><td><code>authentication</code><br/>
<a href="#kubelet-config-k8s-io-v1beta1-KubeletAuthentication"><code>KubeletAuthentication</code></a>
</td>
<td>
   authentication specifies how requests to the Kubelet's server are authenticated
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
it may disrupt components that interact with the Kubelet server.
Defaults:
  anonymous:
    enabled: false
  webhook:
    enabled: true
    cacheTTL: "2m"</td>
</tr>
    
  
<tr><td><code>authorization</code><br/>
<a href="#kubelet-config-k8s-io-v1beta1-KubeletAuthorization"><code>KubeletAuthorization</code></a>
</td>
<td>
   authorization specifies how requests to the Kubelet's server are authorized
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
it may disrupt components that interact with the Kubelet server.
Defaults:
  mode: Webhook
  webhook:
    cacheAuthorizedTTL: "5m"
    cacheUnauthorizedTTL: "30s"</td>
</tr>
    
  
<tr><td><code>registryPullQPS</code><br/>
<code>int32</code>
</td>
<td>
   registryPullQPS is the limit of registry pulls per second.
Set to 0 for no limit.
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
it may impact scalability by changing the amount of traffic produced
by image pulls.
Default: 5</td>
</tr>
    
  
<tr><td><code>registryBurst</code><br/>
<code>int32</code>
</td>
<td>
   registryBurst is the maximum size of bursty pulls, temporarily allows
pulls to burst to this number, while still not exceeding registryPullQPS.
Only used if registryPullQPS > 0.
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
it may impact scalability by changing the amount of traffic produced
by image pulls.
Default: 10</td>
</tr>
    
  
<tr><td><code>eventRecordQPS</code><br/>
<code>int32</code>
</td>
<td>
   eventRecordQPS is the maximum event creations per second. If 0, there
is no limit enforced.
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
it may impact scalability by changing the amount of traffic produced by
event creations.
Default: 5</td>
</tr>
    
  
<tr><td><code>eventBurst</code><br/>
<code>int32</code>
</td>
<td>
   eventBurst is the maximum size of a burst of event creations, temporarily
allows event creations to burst to this number, while still not exceeding
eventRecordQPS. Only used if eventRecordQPS > 0.
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
it may impact scalability by changing the amount of traffic produced by
event creations.
Default: 10</td>
</tr>
    
  
<tr><td><code>enableDebuggingHandlers</code><br/>
<code>bool</code>
</td>
<td>
   enableDebuggingHandlers enables server endpoints for log access
and local running of containers and commands, including the exec,
attach, logs, and portforward features.
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
disabling it may disrupt components that interact with the Kubelet server.
Default: true</td>
</tr>
    
  
<tr><td><code>enableContentionProfiling</code><br/>
<code>bool</code>
</td>
<td>
   enableContentionProfiling enables lock contention profiling, if enableDebuggingHandlers is true.
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
enabling it may carry a performance impact.
Default: false</td>
</tr>
    
  
<tr><td><code>healthzPort</code><br/>
<code>int32</code>
</td>
<td>
   healthzPort is the port of the localhost healthz endpoint (set to 0 to disable)
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
it may disrupt components that monitor Kubelet health.
Default: 10248</td>
</tr>
    
  
<tr><td><code>healthzBindAddress</code><br/>
<code>string</code>
</td>
<td>
   healthzBindAddress is the IP address for the healthz server to serve on
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
it may disrupt components that monitor Kubelet health.
Default: "127.0.0.1"</td>
</tr>
    
  
<tr><td><code>oomScoreAdj</code><br/>
<code>int32</code>
</td>
<td>
   oomScoreAdj is The oom-score-adj value for kubelet process. Values
must be within the range [-1000, 1000].
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
it may impact the stability of nodes under memory pressure.
Default: -999</td>
</tr>
    
  
<tr><td><code>clusterDomain</code><br/>
<code>string</code>
</td>
<td>
   clusterDomain is the DNS domain for this cluster. If set, kubelet will
configure all containers to search this domain in addition to the
host's search domains.
Dynamic Kubelet Config (beta): Dynamically updating this field is not recommended,
as it should be kept in sync with the rest of the cluster.
Default: ""</td>
</tr>
    
  
<tr><td><code>clusterDNS</code><br/>
<code>[]string</code>
</td>
<td>
   clusterDNS is a list of IP addresses for the cluster DNS server. If set,
kubelet will configure all containers to use this for DNS resolution
instead of the host's DNS servers.
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
changes will only take effect on Pods created after the update. Draining
the node is recommended before changing this field.
Default: nil</td>
</tr>
    
  
<tr><td><code>streamingConnectionIdleTimeout</code><br/>
<a href="https://godoc.org/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
</td>
<td>
   streamingConnectionIdleTimeout is the maximum time a streaming connection
can be idle before the connection is automatically closed.
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
it may impact components that rely on infrequent updates over streaming
connections to the Kubelet server.
Default: "4h"</td>
</tr>
    
  
<tr><td><code>nodeStatusUpdateFrequency</code><br/>
<a href="https://godoc.org/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
</td>
<td>
   nodeStatusUpdateFrequency is the frequency that kubelet computes node
status. If node lease feature is not enabled, it is also the frequency that
kubelet posts node status to master.
Note: When node lease feature is not enabled, be cautious when changing the
constant, it must work with nodeMonitorGracePeriod in nodecontroller.
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
it may impact node scalability, and also that the node controller's
nodeMonitorGracePeriod must be set to N&lowast;NodeStatusUpdateFrequency,
where N is the number of retries before the node controller marks
the node unhealthy.
Default: "10s"</td>
</tr>
    
  
<tr><td><code>nodeStatusReportFrequency</code><br/>
<a href="https://godoc.org/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
</td>
<td>
   nodeStatusReportFrequency is the frequency that kubelet posts node
status to master if node status does not change. Kubelet will ignore this
frequency and post node status immediately if any change is detected. It is
only used when node lease feature is enabled. nodeStatusReportFrequency's
default value is 5m. But if nodeStatusUpdateFrequency is set explicitly,
nodeStatusReportFrequency's default value will be set to
nodeStatusUpdateFrequency for backward compatibility.
Default: "5m"</td>
</tr>
    
  
<tr><td><code>nodeLeaseDurationSeconds</code><br/>
<code>int32</code>
</td>
<td>
   nodeLeaseDurationSeconds is the duration the Kubelet will set on its corresponding Lease,
when the NodeLease feature is enabled. This feature provides an indicator of node
health by having the Kubelet create and periodically renew a lease, named after the node,
in the kube-node-lease namespace. If the lease expires, the node can be considered unhealthy.
The lease is currently renewed every 10s, per KEP-0009. In the future, the lease renewal interval
may be set based on the lease duration.
Requires the NodeLease feature gate to be enabled.
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
decreasing the duration may reduce tolerance for issues that temporarily prevent
the Kubelet from renewing the lease (e.g. a short-lived network issue).
Default: 40</td>
</tr>
    
  
<tr><td><code>imageMinimumGCAge</code><br/>
<a href="https://godoc.org/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
</td>
<td>
   imageMinimumGCAge is the minimum age for an unused image before it is
garbage collected.
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
it may trigger or delay garbage collection, and may change the image overhead
on the node.
Default: "2m"</td>
</tr>
    
  
<tr><td><code>imageGCHighThresholdPercent</code><br/>
<code>int32</code>
</td>
<td>
   imageGCHighThresholdPercent is the percent of disk usage after which
image garbage collection is always run. The percent is calculated as
this field value out of 100.
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
it may trigger or delay garbage collection, and may change the image overhead
on the node.
Default: 85</td>
</tr>
    
  
<tr><td><code>imageGCLowThresholdPercent</code><br/>
<code>int32</code>
</td>
<td>
   imageGCLowThresholdPercent is the percent of disk usage before which
image garbage collection is never run. Lowest disk usage to garbage
collect to. The percent is calculated as this field value out of 100.
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
it may trigger or delay garbage collection, and may change the image overhead
on the node.
Default: 80</td>
</tr>
    
  
<tr><td><code>volumeStatsAggPeriod</code><br/>
<a href="https://godoc.org/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
</td>
<td>
   How frequently to calculate and cache volume disk usage for all pods
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
shortening the period may carry a performance impact.
Default: "1m"</td>
</tr>
    
  
<tr><td><code>kubeletCgroups</code><br/>
<code>string</code>
</td>
<td>
   kubeletCgroups is the absolute name of cgroups to isolate the kubelet in
Dynamic Kubelet Config (beta): This field should not be updated without a full node
reboot. It is safest to keep this value the same as the local config.
Default: ""</td>
</tr>
    
  
<tr><td><code>systemCgroups</code><br/>
<code>string</code>
</td>
<td>
   systemCgroups is absolute name of cgroups in which to place
all non-kernel processes that are not already in a container. Empty
for no container. Rolling back the flag requires a reboot.
Dynamic Kubelet Config (beta): This field should not be updated without a full node
reboot. It is safest to keep this value the same as the local config.
Default: ""</td>
</tr>
    
  
<tr><td><code>cgroupRoot</code><br/>
<code>string</code>
</td>
<td>
   cgroupRoot is the root cgroup to use for pods. This is handled by the
container runtime on a best effort basis.
Dynamic Kubelet Config (beta): This field should not be updated without a full node
reboot. It is safest to keep this value the same as the local config.
Default: ""</td>
</tr>
    
  
<tr><td><code>cgroupsPerQOS</code><br/>
<code>bool</code>
</td>
<td>
   Enable QoS based Cgroup hierarchy: top level cgroups for QoS Classes
And all Burstable and BestEffort pods are brought up under their
specific top level QoS cgroup.
Dynamic Kubelet Config (beta): This field should not be updated without a full node
reboot. It is safest to keep this value the same as the local config.
Default: true</td>
</tr>
    
  
<tr><td><code>cgroupDriver</code><br/>
<code>string</code>
</td>
<td>
   driver that the kubelet uses to manipulate cgroups on the host (cgroupfs or systemd)
Dynamic Kubelet Config (beta): This field should not be updated without a full node
reboot. It is safest to keep this value the same as the local config.
Default: "cgroupfs"</td>
</tr>
    
  
<tr><td><code>cpuManagerPolicy</code><br/>
<code>string</code>
</td>
<td>
   CPUManagerPolicy is the name of the policy to use.
Requires the CPUManager feature gate to be enabled.
Dynamic Kubelet Config (beta): This field should not be updated without a full node
reboot. It is safest to keep this value the same as the local config.
Default: "None"</td>
</tr>
    
  
<tr><td><code>cpuManagerReconcilePeriod</code><br/>
<a href="https://godoc.org/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
</td>
<td>
   CPU Manager reconciliation period.
Requires the CPUManager feature gate to be enabled.
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
shortening the period may carry a performance impact.
Default: "10s"</td>
</tr>
    
  
<tr><td><code>memoryManagerPolicy</code><br/>
<code>string</code>
</td>
<td>
   MemoryManagerPolicy is the name of the policy to use by memory manager.
Requires the MemoryManager feature gate to be enabled.
Dynamic Kubelet Config (beta): This field should not be updated without a full node
reboot. It is safest to keep this value the same as the local config.
Default: "none"</td>
</tr>
    
  
<tr><td><code>topologyManagerPolicy</code><br/>
<code>string</code>
</td>
<td>
   TopologyManagerPolicy is the name of the policy to use.
Policies other than "none" require the TopologyManager feature gate to be enabled.
Dynamic Kubelet Config (beta): This field should not be updated without a full node
reboot. It is safest to keep this value the same as the local config.
Default: "none"</td>
</tr>
    
  
<tr><td><code>topologyManagerScope</code><br/>
<code>string</code>
</td>
<td>
   TopologyManagerScope represents the scope of topology hint generation
that topology manager requests and hint providers generate.
"pod" scope requires the TopologyManager feature gate to be enabled.
Default: "container"</td>
</tr>
    
  
<tr><td><code>qosReserved</code><br/>
<code>map[string]string</code>
</td>
<td>
   qosReserved is a set of resource name to percentage pairs that specify
the minimum percentage of a resource reserved for exclusive use by the
guaranteed QoS tier.
Currently supported resources: "memory"
Requires the QOSReserved feature gate to be enabled.
Dynamic Kubelet Config (beta): This field should not be updated without a full node
reboot. It is safest to keep this value the same as the local config.
Default: nil</td>
</tr>
    
  
<tr><td><code>runtimeRequestTimeout</code><br/>
<a href="https://godoc.org/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
</td>
<td>
   runtimeRequestTimeout is the timeout for all runtime requests except long running
requests - pull, logs, exec and attach.
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
it may disrupt components that interact with the Kubelet server.
Default: "2m"</td>
</tr>
    
  
<tr><td><code>hairpinMode</code><br/>
<code>string</code>
</td>
<td>
   hairpinMode specifies how the Kubelet should configure the container
bridge for hairpin packets.
Setting this flag allows endpoints in a Service to loadbalance back to
themselves if they should try to access their own Service. Values:
  "promiscuous-bridge": make the container bridge promiscuous.
  "hairpin-veth":       set the hairpin flag on container veth interfaces.
  "none":               do nothing.
Generally, one must set --hairpin-mode=hairpin-veth to achieve hairpin NAT,
because promiscuous-bridge assumes the existence of a container bridge named cbr0.
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
it may require a node reboot, depending on the network plugin.
Default: "promiscuous-bridge"</td>
</tr>
    
  
<tr><td><code>maxPods</code><br/>
<code>int32</code>
</td>
<td>
   maxPods is the number of pods that can run on this Kubelet.
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
changes may cause Pods to fail admission on Kubelet restart, and may change
the value reported in Node.Status.Capacity[v1.ResourcePods], thus affecting
future scheduling decisions. Increasing this value may also decrease performance,
as more Pods can be packed into a single node.
Default: 110</td>
</tr>
    
  
<tr><td><code>podCIDR</code><br/>
<code>string</code>
</td>
<td>
   The CIDR to use for pod IP addresses, only used in standalone mode.
In cluster mode, this is obtained from the master.
Dynamic Kubelet Config (beta): This field should always be set to the empty default.
It should only set for standalone Kubelets, which cannot use Dynamic Kubelet Config.
Default: ""</td>
</tr>
    
  
<tr><td><code>podPidsLimit</code><br/>
<code>int64</code>
</td>
<td>
   PodPidsLimit is the maximum number of pids in any pod.
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
lowering it may prevent container processes from forking after the change.
Default: -1</td>
</tr>
    
  
<tr><td><code>resolvConf</code><br/>
<code>string</code>
</td>
<td>
   ResolverConfig is the resolver configuration file used as the basis
for the container DNS resolution configuration.
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
changes will only take effect on Pods created after the update. Draining
the node is recommended before changing this field.
Default: "/etc/resolv.conf"</td>
</tr>
    
  
<tr><td><code>runOnce</code><br/>
<code>bool</code>
</td>
<td>
   RunOnce causes the Kubelet to check the API server once for pods,
run those in addition to the pods specified by static pod files, and exit.
Default: false</td>
</tr>
    
  
<tr><td><code>cpuCFSQuota</code><br/>
<code>bool</code>
</td>
<td>
   cpuCFSQuota enables CPU CFS quota enforcement for containers that
specify CPU limits.
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
disabling it may reduce node stability.
Default: true</td>
</tr>
    
  
<tr><td><code>cpuCFSQuotaPeriod</code><br/>
<a href="https://godoc.org/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
</td>
<td>
   CPUCFSQuotaPeriod is the CPU CFS quota period value, cpu.cfs_period_us.
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
limits set for containers will result in different cpu.cfs_quota settings. This
will trigger container restarts on the node being reconfigured.
Default: "100ms"</td>
</tr>
    
  
<tr><td><code>nodeStatusMaxImages</code><br/>
<code>int32</code>
</td>
<td>
   nodeStatusMaxImages caps the number of images reported in Node.Status.Images.
Note: If -1 is specified, no cap will be applied. If 0 is specified, no image is returned.
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
different values can be reported on node status.
Default: 50</td>
</tr>
    
  
<tr><td><code>maxOpenFiles</code><br/>
<code>int64</code>
</td>
<td>
   maxOpenFiles is Number of files that can be opened by Kubelet process.
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
it may impact the ability of the Kubelet to interact with the node's filesystem.
Default: 1000000</td>
</tr>
    
  
<tr><td><code>contentType</code><br/>
<code>string</code>
</td>
<td>
   contentType is contentType of requests sent to apiserver.
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
it may impact the ability for the Kubelet to communicate with the API server.
If the Kubelet loses contact with the API server due to a change to this field,
the change cannot be reverted via dynamic Kubelet config.
Default: "application/vnd.kubernetes.protobuf"</td>
</tr>
    
  
<tr><td><code>kubeAPIQPS</code><br/>
<code>int32</code>
</td>
<td>
   kubeAPIQPS is the QPS to use while talking with kubernetes apiserver
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
it may impact scalability by changing the amount of traffic the Kubelet
sends to the API server.
Default: 5</td>
</tr>
    
  
<tr><td><code>kubeAPIBurst</code><br/>
<code>int32</code>
</td>
<td>
   kubeAPIBurst is the burst to allow while talking with kubernetes apiserver
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
it may impact scalability by changing the amount of traffic the Kubelet
sends to the API server.
Default: 10</td>
</tr>
    
  
<tr><td><code>serializeImagePulls</code><br/>
<code>bool</code>
</td>
<td>
   serializeImagePulls when enabled, tells the Kubelet to pull images one
at a time. We recommend &lowast;not&lowast; changing the default value on nodes that
run docker daemon with version  < 1.9 or an Aufs storage backend.
Issue #10959 has more details.
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
it may impact the performance of image pulls.
Default: true</td>
</tr>
    
  
<tr><td><code>evictionHard</code><br/>
<code>map[string]string</code>
</td>
<td>
   Map of signal names to quantities that defines hard eviction thresholds. For example: {"memory.available": "300Mi"}.
To explicitly disable, pass a 0% or 100% threshold on an arbitrary resource.
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
it may trigger or delay Pod evictions.
Default:
  memory.available:  "100Mi"
  nodefs.available:  "10%"
  nodefs.inodesFree: "5%"
  imagefs.available: "15%"</td>
</tr>
    
  
<tr><td><code>evictionSoft</code><br/>
<code>map[string]string</code>
</td>
<td>
   Map of signal names to quantities that defines soft eviction thresholds.
For example: {"memory.available": "300Mi"}.
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
it may trigger or delay Pod evictions, and may change the allocatable reported
by the node.
Default: nil</td>
</tr>
    
  
<tr><td><code>evictionSoftGracePeriod</code><br/>
<code>map[string]string</code>
</td>
<td>
   Map of signal names to quantities that defines grace periods for each soft eviction signal.
For example: {"memory.available": "30s"}.
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
it may trigger or delay Pod evictions.
Default: nil</td>
</tr>
    
  
<tr><td><code>evictionPressureTransitionPeriod</code><br/>
<a href="https://godoc.org/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
</td>
<td>
   Duration for which the kubelet has to wait before transitioning out of an eviction pressure condition.
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
lowering it may decrease the stability of the node when the node is overcommitted.
Default: "5m"</td>
</tr>
    
  
<tr><td><code>evictionMaxPodGracePeriod</code><br/>
<code>int32</code>
</td>
<td>
   Maximum allowed grace period (in seconds) to use when terminating pods in
response to a soft eviction threshold being met. This value effectively caps
the Pod's TerminationGracePeriodSeconds value during soft evictions.
Note: Due to issue #64530, the behavior has a bug where this value currently just
overrides the grace period during soft eviction, which can increase the grace
period from what is set on the Pod. This bug will be fixed in a future release.
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
lowering it decreases the amount of time Pods will have to gracefully clean
up before being killed during a soft eviction.
Default: 0</td>
</tr>
    
  
<tr><td><code>evictionMinimumReclaim</code><br/>
<code>map[string]string</code>
</td>
<td>
   Map of signal names to quantities that defines minimum reclaims, which describe the minimum
amount of a given resource the kubelet will reclaim when performing a pod eviction while
that resource is under pressure. For example: {"imagefs.available": "2Gi"}
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
it may change how well eviction can manage resource pressure.
Default: nil</td>
</tr>
    
  
<tr><td><code>podsPerCore</code><br/>
<code>int32</code>
</td>
<td>
   podsPerCore is the maximum number of pods per core. Cannot exceed MaxPods.
If 0, this field is ignored.
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
changes may cause Pods to fail admission on Kubelet restart, and may change
the value reported in Node.Status.Capacity[v1.ResourcePods], thus affecting
future scheduling decisions. Increasing this value may also decrease performance,
as more Pods can be packed into a single node.
Default: 0</td>
</tr>
    
  
<tr><td><code>enableControllerAttachDetach</code><br/>
<code>bool</code>
</td>
<td>
   enableControllerAttachDetach enables the Attach/Detach controller to
manage attachment/detachment of volumes scheduled to this node, and
disables kubelet from executing any attach/detach operations
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
changing which component is responsible for volume management on a live node
may result in volumes refusing to detach if the node is not drained prior to
the update, and if Pods are scheduled to the node before the
volumes.kubernetes.io/controller-managed-attach-detach annotation is updated by the
Kubelet. In general, it is safest to leave this value set the same as local config.
Default: true</td>
</tr>
    
  
<tr><td><code>protectKernelDefaults</code><br/>
<code>bool</code>
</td>
<td>
   protectKernelDefaults, if true, causes the Kubelet to error if kernel
flags are not as it expects. Otherwise the Kubelet will attempt to modify
kernel flags to match its expectation.
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
enabling it may cause the Kubelet to crash-loop if the Kernel is not configured as
Kubelet expects.
Default: false</td>
</tr>
    
  
<tr><td><code>makeIPTablesUtilChains</code><br/>
<code>bool</code>
</td>
<td>
   If true, Kubelet ensures a set of iptables rules are present on host.
These rules will serve as utility rules for various components, e.g. KubeProxy.
The rules will be created based on IPTablesMasqueradeBit and IPTablesDropBit.
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
disabling it will prevent the Kubelet from healing locally misconfigured iptables rules.
Default: true</td>
</tr>
    
  
<tr><td><code>iptablesMasqueradeBit</code><br/>
<code>int32</code>
</td>
<td>
   iptablesMasqueradeBit is the bit of the iptables fwmark space to mark for SNAT
Values must be within the range [0, 31]. Must be different from other mark bits.
Warning: Please match the value of the corresponding parameter in kube-proxy.
TODO: clean up IPTablesMasqueradeBit in kube-proxy
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
it needs to be coordinated with other components, like kube-proxy, and the update
will only be effective if MakeIPTablesUtilChains is enabled.
Default: 14</td>
</tr>
    
  
<tr><td><code>iptablesDropBit</code><br/>
<code>int32</code>
</td>
<td>
   iptablesDropBit is the bit of the iptables fwmark space to mark for dropping packets.
Values must be within the range [0, 31]. Must be different from other mark bits.
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
it needs to be coordinated with other components, like kube-proxy, and the update
will only be effective if MakeIPTablesUtilChains is enabled.
Default: 15</td>
</tr>
    
  
<tr><td><code>featureGates</code><br/>
<code>map[string]bool</code>
</td>
<td>
   featureGates is a map of feature names to bools that enable or disable alpha/experimental
features. This field modifies piecemeal the built-in default values from
"k8s.io/kubernetes/pkg/features/kube_features.go".
Dynamic Kubelet Config (beta): If dynamically updating this field, consider the
documentation for the features you are enabling or disabling. While we
encourage feature developers to make it possible to dynamically enable
and disable features, some changes may require node reboots, and some
features may require careful coordination to retroactively disable.
Default: nil</td>
</tr>
    
  
<tr><td><code>failSwapOn</code><br/>
<code>bool</code>
</td>
<td>
   failSwapOn tells the Kubelet to fail to start if swap is enabled on the node.
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
setting it to true will cause the Kubelet to crash-loop if swap is enabled.
Default: true</td>
</tr>
    
  
<tr><td><code>containerLogMaxSize</code><br/>
<code>string</code>
</td>
<td>
   A quantity defines the maximum size of the container log file before it is rotated.
For example: "5Mi" or "256Ki".
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
it may trigger log rotation.
Default: "10Mi"</td>
</tr>
    
  
<tr><td><code>containerLogMaxFiles</code><br/>
<code>int32</code>
</td>
<td>
   Maximum number of container log files that can be present for a container.
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
lowering it may cause log files to be deleted.
Default: 5</td>
</tr>
    
  
<tr><td><code>configMapAndSecretChangeDetectionStrategy</code><br/>
<a href="#kubelet-config-k8s-io-v1beta1-ResourceChangeDetectionStrategy"><code>ResourceChangeDetectionStrategy</code></a>
</td>
<td>
   ConfigMapAndSecretChangeDetectionStrategy is a mode in which
config map and secret managers are running.
Default: "Watch"</td>
</tr>
    
  
<tr><td><code>systemReserved</code><br/>
<code>map[string]string</code>
</td>
<td>
   systemReserved is a set of ResourceName=ResourceQuantity (e.g. cpu=200m,memory=150G)
pairs that describe resources reserved for non-kubernetes components.
Currently only cpu and memory are supported.
See http://kubernetes.io/docs/user-guide/compute-resources for more detail.
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
it may not be possible to increase the reserved resources, because this
requires resizing cgroups. Always look for a NodeAllocatableEnforced event
after updating this field to ensure that the update was successful.
Default: nil</td>
</tr>
    
  
<tr><td><code>kubeReserved</code><br/>
<code>map[string]string</code>
</td>
<td>
   A set of ResourceName=ResourceQuantity (e.g. cpu=200m,memory=150G) pairs
that describe resources reserved for kubernetes system components.
Currently cpu, memory and local storage for root file system are supported.
See http://kubernetes.io/docs/user-guide/compute-resources for more detail.
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
it may not be possible to increase the reserved resources, because this
requires resizing cgroups. Always look for a NodeAllocatableEnforced event
after updating this field to ensure that the update was successful.
Default: nil</td>
</tr>
    
  
<tr><td><code>reservedSystemCPUs</code> <B>[Required]</B><br/>
<code>string</code>
</td>
<td>
   This ReservedSystemCPUs option specifies the cpu list reserved for the host level system threads and kubernetes related threads.
This provide a "static" CPU list rather than the "dynamic" list by system-reserved and kube-reserved.
This option overwrites CPUs provided by system-reserved and kube-reserved.</td>
</tr>
    
  
<tr><td><code>showHiddenMetricsForVersion</code><br/>
<code>string</code>
</td>
<td>
   The previous version for which you want to show hidden metrics.
Only the previous minor version is meaningful, other values will not be allowed.
The format is <major>.<minor>, e.g.: '1.16'.
The purpose of this format is make sure you have the opportunity to notice if the next release hides additional metrics,
rather than being surprised when they are permanently removed in the release after that.
Default: ""</td>
</tr>
    
  
<tr><td><code>systemReservedCgroup</code><br/>
<code>string</code>
</td>
<td>
   This flag helps kubelet identify absolute name of top level cgroup used to enforce `SystemReserved` compute resource reservation for OS system daemons.
Refer to [Node Allocatable](https://git.k8s.io/community/contributors/design-proposals/node/node-allocatable.md) doc for more information.
Dynamic Kubelet Config (beta): This field should not be updated without a full node
reboot. It is safest to keep this value the same as the local config.
Default: ""</td>
</tr>
    
  
<tr><td><code>kubeReservedCgroup</code><br/>
<code>string</code>
</td>
<td>
   This flag helps kubelet identify absolute name of top level cgroup used to enforce `KubeReserved` compute resource reservation for Kubernetes node system daemons.
Refer to [Node Allocatable](https://git.k8s.io/community/contributors/design-proposals/node/node-allocatable.md) doc for more information.
Dynamic Kubelet Config (beta): This field should not be updated without a full node
reboot. It is safest to keep this value the same as the local config.
Default: ""</td>
</tr>
    
  
<tr><td><code>enforceNodeAllocatable</code><br/>
<code>[]string</code>
</td>
<td>
   This flag specifies the various Node Allocatable enforcements that Kubelet needs to perform.
This flag accepts a list of options. Acceptable options are `none`, `pods`, `system-reserved` & `kube-reserved`.
If `none` is specified, no other options may be specified.
Refer to [Node Allocatable](https://git.k8s.io/community/contributors/design-proposals/node/node-allocatable.md) doc for more information.
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
removing enforcements may reduce the stability of the node. Alternatively, adding
enforcements may reduce the stability of components which were using more than
the reserved amount of resources; for example, enforcing kube-reserved may cause
Kubelets to OOM if it uses more than the reserved resources, and enforcing system-reserved
may cause system daemons to OOM if they use more than the reserved resources.
Default: ["pods"]</td>
</tr>
    
  
<tr><td><code>allowedUnsafeSysctls</code><br/>
<code>[]string</code>
</td>
<td>
   A comma separated whitelist of unsafe sysctls or sysctl patterns (ending in &lowast;).
Unsafe sysctl groups are kernel.shm&lowast;, kernel.msg&lowast;, kernel.sem, fs.mqueue.&lowast;, and net.&lowast;.
These sysctls are namespaced but not allowed by default.  For example: "kernel.msg&lowast;,net.ipv4.route.min_pmtu"
Default: []</td>
</tr>
    
  
<tr><td><code>volumePluginDir</code><br/>
<code>string</code>
</td>
<td>
   volumePluginDir is the full path of the directory in which to search
for additional third party volume plugins.
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that changing
the volumePluginDir may disrupt workloads relying on third party volume plugins.
Default: "/usr/libexec/kubernetes/kubelet-plugins/volume/exec/"</td>
</tr>
    
  
<tr><td><code>providerID</code><br/>
<code>string</code>
</td>
<td>
   providerID, if set, sets the unique id of the instance that an external provider (i.e. cloudprovider)
can use to identify a specific node.
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
it may impact the ability of the Kubelet to interact with cloud providers.
Default: ""</td>
</tr>
    
  
<tr><td><code>kernelMemcgNotification</code><br/>
<code>bool</code>
</td>
<td>
   kernelMemcgNotification, if set, the kubelet will integrate with the kernel memcg notification
to determine if memory eviction thresholds are crossed rather than polling.
Dynamic Kubelet Config (beta): If dynamically updating this field, consider that
it may impact the way Kubelet interacts with the kernel.
Default: false</td>
</tr>
    
  
<tr><td><code>logging</code> <B>[Required]</B><br/>
<a href="#LoggingConfiguration"><code>LoggingConfiguration</code></a>
</td>
<td>
   Logging specifies the options of logging.
Refer [Logs Options](https://github.com/kubernetes/component-base/blob/master/logs/options.go) for more information.
Defaults:
  Format: text</td>
</tr>
    
  
<tr><td><code>enableSystemLogHandler</code><br/>
<code>bool</code>
</td>
<td>
   enableSystemLogHandler enables system logs via web interface host:port/logs/
Default: true</td>
</tr>
    
  
<tr><td><code>shutdownGracePeriod</code><br/>
<a href="https://godoc.org/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
</td>
<td>
   ShutdownGracePeriod specifies the total duration that the node should delay the shutdown and total grace period for pod termination during a node shutdown.
Default: "0s"</td>
</tr>
    
  
<tr><td><code>shutdownGracePeriodCriticalPods</code><br/>
<a href="https://godoc.org/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
</td>
<td>
   ShutdownGracePeriodCriticalPods specifies the duration used to terminate critical pods during a node shutdown. This should be less than ShutdownGracePeriod.
For example, if ShutdownGracePeriod=30s, and ShutdownGracePeriodCriticalPods=10s, during a node shutdown the first 20 seconds would be reserved for gracefully terminating normal pods, and the last 10 seconds would be reserved for terminating critical pods.
Default: "0s"</td>
</tr>
    
  
<tr><td><code>reservedMemory</code><br/>
<a href="#kubelet-config-k8s-io-v1beta1-MemoryReservation"><code>[]MemoryReservation</code></a>
</td>
<td>
   ReservedMemory specifies a comma-separated list of memory reservations for NUMA nodes.
The parameter makes sense only in the context of the memory manager feature. The memory manager will not allocate reserved memory for container workloads.
For example, if you have a NUMA0 with 10Gi of memory and the ReservedMemory was specified to reserve 1Gi of memory at NUMA0,
the memory manager will assume that only 9Gi is available for allocation.
You can specify a different amount of NUMA node and memory types.
You can omit this parameter at all, but you should be aware that the amount of reserved memory from all NUMA nodes
should be equal to the amount of memory specified by the node allocatable features(https://kubernetes.io/docs/tasks/administer-cluster/reserve-compute-resources/#node-allocatable).
If at least one node allocatable parameter has a non-zero value, you will need to specify at least one NUMA node.
Also, avoid specifying:
1. Duplicates, the same NUMA node, and memory type, but with a different value.
2. zero limits for any memory type.
3. NUMAs nodes IDs that do not exist under the machine.
4. memory types except for memory and hugepages-<size>
Default: nil</td>
</tr>
    
  
<tr><td><code>enableProfilingHandler</code><br/>
<code>bool</code>
</td>
<td>
   enableProfilingHandler enables profiling via web interface host:port/debug/pprof/
Default: true</td>
</tr>
    
  
<tr><td><code>enableDebugFlagsHandler</code><br/>
<code>bool</code>
</td>
<td>
   enableDebugFlagsHandler enables flags endpoint via web interface host:port/debug/flags/v
Default: true</td>
</tr>
    
  
</tbody>
</table>
    


## `SerializedNodeConfigSource`     {#kubelet-config-k8s-io-v1beta1-SerializedNodeConfigSource}
    




SerializedNodeConfigSource allows us to serialize v1.NodeConfigSource.
This type is used internally by the Kubelet for tracking checkpointed dynamic configs.
It exists in the kubeletconfig API group because it is classified as a versioned input to the Kubelet.

<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
<tbody>
    
<tr><td><code>apiVersion</code><br/>string</td><td><code>kubelet.config.k8s.io/v1beta1</code></td></tr>
<tr><td><code>kind</code><br/>string</td><td><code>SerializedNodeConfigSource</code></td></tr>
    

  
  
<tr><td><code>source</code><br/>
<a href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.20/#nodeconfigsource-v1-core"><code>core/v1.NodeConfigSource</code></a>
</td>
<td>
   Source is the source that we are serializing</td>
</tr>
    
  
</tbody>
</table>
    


## `HairpinMode`     {#kubelet-config-k8s-io-v1beta1-HairpinMode}
    
(Alias of `string`)



HairpinMode denotes how the kubelet should configure networking to handle
hairpin packets.


    


## `KubeletAnonymousAuthentication`     {#kubelet-config-k8s-io-v1beta1-KubeletAnonymousAuthentication}
    



**Appears in:**

- [KubeletAuthentication](#kubelet-config-k8s-io-v1beta1-KubeletAuthentication)




<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
<tbody>
    

  
<tr><td><code>enabled</code><br/>
<code>bool</code>
</td>
<td>
   enabled allows anonymous requests to the kubelet server.
Requests that are not rejected by another authentication method are treated as anonymous requests.
Anonymous requests have a username of system:anonymous, and a group name of system:unauthenticated.</td>
</tr>
    
  
</tbody>
</table>
    


## `KubeletAuthentication`     {#kubelet-config-k8s-io-v1beta1-KubeletAuthentication}
    



**Appears in:**

- [KubeletConfiguration](#kubelet-config-k8s-io-v1beta1-KubeletConfiguration)




<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
<tbody>
    

  
<tr><td><code>x509</code><br/>
<a href="#kubelet-config-k8s-io-v1beta1-KubeletX509Authentication"><code>KubeletX509Authentication</code></a>
</td>
<td>
   x509 contains settings related to x509 client certificate authentication</td>
</tr>
    
  
<tr><td><code>webhook</code><br/>
<a href="#kubelet-config-k8s-io-v1beta1-KubeletWebhookAuthentication"><code>KubeletWebhookAuthentication</code></a>
</td>
<td>
   webhook contains settings related to webhook bearer token authentication</td>
</tr>
    
  
<tr><td><code>anonymous</code><br/>
<a href="#kubelet-config-k8s-io-v1beta1-KubeletAnonymousAuthentication"><code>KubeletAnonymousAuthentication</code></a>
</td>
<td>
   anonymous contains settings related to anonymous authentication</td>
</tr>
    
  
</tbody>
</table>
    


## `KubeletAuthorization`     {#kubelet-config-k8s-io-v1beta1-KubeletAuthorization}
    



**Appears in:**

- [KubeletConfiguration](#kubelet-config-k8s-io-v1beta1-KubeletConfiguration)




<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
<tbody>
    

  
<tr><td><code>mode</code><br/>
<a href="#kubelet-config-k8s-io-v1beta1-KubeletAuthorizationMode"><code>KubeletAuthorizationMode</code></a>
</td>
<td>
   mode is the authorization mode to apply to requests to the kubelet server.
Valid values are AlwaysAllow and Webhook.
Webhook mode uses the SubjectAccessReview API to determine authorization.</td>
</tr>
    
  
<tr><td><code>webhook</code><br/>
<a href="#kubelet-config-k8s-io-v1beta1-KubeletWebhookAuthorization"><code>KubeletWebhookAuthorization</code></a>
</td>
<td>
   webhook contains settings related to Webhook authorization.</td>
</tr>
    
  
</tbody>
</table>
    


## `KubeletAuthorizationMode`     {#kubelet-config-k8s-io-v1beta1-KubeletAuthorizationMode}
    
(Alias of `string`)


**Appears in:**

- [KubeletAuthorization](#kubelet-config-k8s-io-v1beta1-KubeletAuthorization)





    


## `KubeletWebhookAuthentication`     {#kubelet-config-k8s-io-v1beta1-KubeletWebhookAuthentication}
    



**Appears in:**

- [KubeletAuthentication](#kubelet-config-k8s-io-v1beta1-KubeletAuthentication)




<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
<tbody>
    

  
<tr><td><code>enabled</code><br/>
<code>bool</code>
</td>
<td>
   enabled allows bearer token authentication backed by the tokenreviews.authentication.k8s.io API</td>
</tr>
    
  
<tr><td><code>cacheTTL</code><br/>
<a href="https://godoc.org/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
</td>
<td>
   cacheTTL enables caching of authentication results</td>
</tr>
    
  
</tbody>
</table>
    


## `KubeletWebhookAuthorization`     {#kubelet-config-k8s-io-v1beta1-KubeletWebhookAuthorization}
    



**Appears in:**

- [KubeletAuthorization](#kubelet-config-k8s-io-v1beta1-KubeletAuthorization)




<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
<tbody>
    

  
<tr><td><code>cacheAuthorizedTTL</code><br/>
<a href="https://godoc.org/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
</td>
<td>
   cacheAuthorizedTTL is the duration to cache 'authorized' responses from the webhook authorizer.</td>
</tr>
    
  
<tr><td><code>cacheUnauthorizedTTL</code><br/>
<a href="https://godoc.org/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
</td>
<td>
   cacheUnauthorizedTTL is the duration to cache 'unauthorized' responses from the webhook authorizer.</td>
</tr>
    
  
</tbody>
</table>
    


## `KubeletX509Authentication`     {#kubelet-config-k8s-io-v1beta1-KubeletX509Authentication}
    



**Appears in:**

- [KubeletAuthentication](#kubelet-config-k8s-io-v1beta1-KubeletAuthentication)




<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
<tbody>
    

  
<tr><td><code>clientCAFile</code><br/>
<code>string</code>
</td>
<td>
   clientCAFile is the path to a PEM-encoded certificate bundle. If set, any request presenting a client certificate
signed by one of the authorities in the bundle is authenticated with a username corresponding to the CommonName,
and groups corresponding to the Organization in the client certificate.</td>
</tr>
    
  
</tbody>
</table>
    


## `MemoryReservation`     {#kubelet-config-k8s-io-v1beta1-MemoryReservation}
    



**Appears in:**

- [KubeletConfiguration](#kubelet-config-k8s-io-v1beta1-KubeletConfiguration)


MemoryReservation specifies the memory reservation of different types for each NUMA node

<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
<tbody>
    

  
<tr><td><code>numaNode</code> <B>[Required]</B><br/>
<code>int32</code>
</td>
<td>
   <span class="text-muted">No description provided.</span>
   </td>
</tr>
    
  
<tr><td><code>limits</code> <B>[Required]</B><br/>
<a href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.20/#resourcelist-v1-core"><code>core/v1.ResourceList</code></a>
</td>
<td>
   <span class="text-muted">No description provided.</span>
   </td>
</tr>
    
  
</tbody>
</table>
    


## `ResourceChangeDetectionStrategy`     {#kubelet-config-k8s-io-v1beta1-ResourceChangeDetectionStrategy}
    
(Alias of `string`)


**Appears in:**

- [KubeletConfiguration](#kubelet-config-k8s-io-v1beta1-KubeletConfiguration)


ResourceChangeDetectionStrategy denotes a mode in which internal
managers (secret, configmap) are discovering object changes.


    
  
