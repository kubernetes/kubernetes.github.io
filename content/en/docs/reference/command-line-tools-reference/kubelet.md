---
title: kubelet
content_type: tool-reference
weight: 28
---

## {{% heading "synopsis" %}}


The kubelet is the primary "node agent" that runs on each
node. It can register the node with the apiserver using one of: the hostname; a flag to override the hostname; or specific logic for a cloud provider.

The kubelet works in terms of a PodSpec. A PodSpec is a YAML or JSON object
that describes a pod. The kubelet takes a set of PodSpecs that are provided through various mechanisms (primarily through the apiserver) and ensures that the containers described in those PodSpecs are running and healthy. The kubelet doesn't manage containers which were not created by Kubernetes.

Other than from a PodSpec from the apiserver, there are three ways that a container manifest can be provided to the Kubelet.

File: Path passed as a flag on the command line. Files under this path will be monitored periodically for updates. The monitoring period is 20s by default and is configurable via a flag.

HTTP endpoint: HTTP endpoint passed as a parameter on the command line. This endpoint is checked every 20 seconds (also configurable with a flag).

HTTP server: The kubelet can also listen for HTTP and respond to a simple API (underspec'd currently) to submit a new manifest.

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
<td></td><td style="line-height: 130%; word-wrap: break-word;">If true, adds the file directory to the header of the log messages</td>
</tr>
    
<tr>
<td colspan="2">--address ip&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: 0.0.0.0 </td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">The IP address for the Kubelet to serve on (set to `0.0.0.0` for all IPv4 interfaces and `::` for all IPv6 interfaces)  (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>
    
<tr>
<td colspan="2">--allowed-unsafe-sysctls strings</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Comma-separated whitelist of unsafe sysctls or unsafe sysctl patterns (ending in `*`). Use these at your own risk. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--alsologtostderr</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">log to standard error as well as files</td>
</tr>

<tr>
<td colspan="2">--anonymous-auth&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: true</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Enables anonymous requests to the Kubelet server. Requests that are not rejected by another authentication method are treated as anonymous requests. Anonymous requests have a username of `system:anonymous`, and a group name of `system:unauthenticated`. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--authentication-token-webhook</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Use the `TokenReview` API to determine authentication for bearer tokens. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--authentication-token-webhook-cache-ttl duration&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: `2m0s`</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">The duration to cache responses from the webhook token authenticator. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--authorization-mode string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Authorization mode for Kubelet server. Valid options are `AlwaysAllow` or `Webhook`. `Webhook` mode uses the `SubjectAccessReview` API to determine authorization. (default "AlwaysAllow" when `--config` flag is not provided; "Webhook" when `--config` flag presents.) (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's --config flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--authorization-webhook-cache-authorized-ttl duration&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: `5m0s`</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">The duration to cache 'authorized' responses from the webhook authorizer. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--authorization-webhook-cache-unauthorized-ttl duration&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: `30s`</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">The duration to cache 'unauthorized' responses from the webhook authorizer. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--azure-container-registry-config string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Path to the file containing Azure container registry configuration information.</td>
</tr>

<tr>
<td colspan="2">--bootstrap-kubeconfig string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Path to a kubeconfig file that will be used to get client certificate for kubelet. If the file specified by `--kubeconfig` does not exist, the bootstrap kubeconfig is used to request a client certificate from the API server. On success, a kubeconfig file referencing the generated client certificate and key is written to the path specified by `--kubeconfig`. The client certificate and key file will be stored in the directory pointed by `--cert-dir`.</td>
</tr>

<tr>
<td colspan="2">--cert-dir string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: `/var/lib/kubelet/pki`</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">The directory where the TLS certs are located. If `--tls-cert-file` and `--tls-private-key-file` are provided, this flag will be ignored.</td>
</tr>

<tr>
<td colspan="2">--cgroup-driver string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: `cgroupfs`</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Driver that the kubelet uses to manipulate cgroups on the host.  Possible values: `cgroupfs`, `systemd`. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)/td>
</tr>

<tr>
<td colspan="2">--cgroup-root string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: `''`</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Optional root cgroup to use for pods. This is handled by the container runtime on a best effort basis. Default: '', which means use the container runtime default. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's --config flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--cgroups-per-qos&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: `true`</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Enable creation of QoS cgroup hierarchy, if true top level QoS and pod cgroups are created. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--chaos-chance float</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">If &gt; 0.0, introduce random client errors and latency. Intended for testing. (DEPRECATED: will be removed in a future version.)</td>
</tr>

<tr>
<td colspan="2">--client-ca-file string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">If set, any request presenting a client certificate signed by one of the authorities in the client-ca-file is authenticated with an identity corresponding to the CommonName of the client certificate. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's --config flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--cloud-config string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">The path to the cloud provider configuration file. Empty string for no configuration file. (DEPRECATED: will be removed in 1.23, in favor of removing cloud providers code from Kubelet.)</td>
</tr>

<tr>
<td colspan="2">--cloud-provider string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">The provider for cloud services. Set to empty string for running with no cloud provider. If set, the cloud provider determines the name of the node (consult cloud provider documentation to determine if and how the hostname is used). (DEPRECATED: will be removed in 1.23, in favor of removing cloud provider code from Kubelet.)</td>
</tr>

<tr>
<td colspan="2">--cluster-dns strings</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Comma-separated list of DNS server IP address. This value is used for containers DNS server in case of Pods with "dnsPolicy=ClusterFirst". Note: all DNS servers appearing in the list MUST serve the same set of records otherwise name resolution within the cluster may not work correctly. There is no guarantee as to which DNS server may be contacted for name resolution. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--cluster-domain string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Domain for this cluster. If set, kubelet will configure all containers to search this domain in addition to the host's search domains (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--cni-bin-dir string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: `/opt/cni/bin`</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">&lt;Warning: Alpha feature&gt; A comma-separated list of full paths of directories in which to search for CNI plugin binaries. This docker-specific flag only works when container-runtime is set to `docker`.</td>
</tr>

<tr>
<td colspan="2">--cni-cache-dir string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: `/var/lib/cni/cache`</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">&lt;Warning: Alpha feature&gt; The full path of the directory in which CNI should store cache files. This docker-specific flag only works when container-runtime is set to `docker`.</td>
</tr>

<tr>
<td colspan="2">--cni-conf-dir string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: `/etc/cni/net.d`</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">&lt;Warning: Alpha feature&gt; The full path of the directory in which to search for CNI config files. This docker-specific flag only works when container-runtime is set to `docker`.</td>
</tr>

<tr>
<td colspan="2">--config string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">The Kubelet will load its initial configuration from this file. The path may be absolute or relative; relative paths start at the Kubelet's current working directory. Omit this flag to use the built-in default configuration values. Command-line flags override configuration from this file.</td>
</tr>

<tr>
<td colspan="2">--container-log-max-files int32&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: 5</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Set the maximum number of container log files that can be present for a container. The number must be &ge; 2. This flag can only be used with `--container-runtime=remote`. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's --config flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--container-log-max-size string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: `10Mi`</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Set the maximum size (e.g. 10Mi) of container log file before it is rotated. This flag can only be used with `--container-runtime=remote`.  (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's --config flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--container-runtime string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: `docker`</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">The container runtime to use. Possible values: `docker`, `remote`.</td>
</tr>

<tr>
<td colspan="2">--container-runtime-endpoint string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: `unix:///var/run/dockershim.sock`</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">[Experimental] The endpoint of remote runtime service. Currently unix socket endpoint is supported on Linux, while npipe and tcp endpoints are supported on windows. Examples: `unix:///var/run/dockershim.sock`, `npipe:////./pipe/dockershim`.</td>
</tr>

   
<tr>
<td colspan="2">--contention-profiling</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Enable lock contention profiling, if profiling is enabled (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--cpu-cfs-quota&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: `true`</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Enable CPU CFS quota enforcement for containers that specify CPU limits (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--cpu-cfs-quota-period duration&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: `100ms`</td>
   </tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Sets CPU CFS quota period value, `cpu.cfs_period_us`, defaults to Linux Kernel default. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--cpu-manager-policy string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: `none`</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">CPU Manager policy to use. Possible values: `none`, `static`. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--cpu-manager-policy-options strings</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Comma-separated list of options to fine-tune the behavior of the CPU Manager policy to use. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--cpu-manager-reconcile-period duration&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: `10s`</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">&lt;Warning: Alpha feature&gt; CPU Manager reconciliation period. Examples: `10s`, or `1m`. If not supplied, defaults to node status update frequency. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--docker-endpoint string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: `unix:///var/run/docker.sock`</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Use this for the `docker` endpoint to communicate with. This docker-specific flag only works when container-runtime is set to `docker`.</td>
</tr>

<tr>
<td colspan="2">--dynamic-config-dir string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">The Kubelet will use this directory for checkpointing downloaded configurations and tracking configuration health. The Kubelet will create this directory if it does not already exist. The path may be absolute or relative; relative paths start at the Kubelet's current working directory. Providing this flag enables dynamic Kubelet configuration. The `DynamicKubeletConfig` feature gate must be enabled to pass this flag; this gate currently defaults to `true` because the feature is beta.</td>
</tr>

<tr>
<td colspan="2">--enable-controller-attach-detach&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: `true`</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Enables the Attach/Detach controller to manage attachment/detachment of volumes scheduled to this node, and disables kubelet from executing any attach/detach operations.</td>
</tr>

<tr>
<td colspan="2">--enable-debugging-handlers&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: `true`</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Enables server endpoints for log collection and local running of containers and commands. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--enable-server&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: `true`</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Enable the Kubelet's server. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--enforce-node-allocatable strings&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: `pods`</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">A comma separated list of levels of node allocatable enforcement to be enforced by kubelet. Acceptable options are `none`, `pods`, `system-reserved`, and `kube-reserved`. If the latter two options are specified, `--system-reserved-cgroup` and `--kube-reserved-cgroup` must also be set, respectively. If `none` is specified, no additional options should be set. See https://kubernetes.io/docs/tasks/administer-cluster/reserve-compute-resources/ for more details. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's --config flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--event-burst int32&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: 10</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Maximum size of a bursty event records, temporarily allows event records to burst to this number, while still not exceeding `--event-qps`. The number must be >= 0. If 0 will use DefaultBurst: 10. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--event-qps int32&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: 5</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">QPS to limit event creations. The number must be >= 0. If 0 will use DefaultQPS: 5. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--eviction-hard mapStringString&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: `imagefs.available<15%,memory.available<100Mi,nodefs.available<10%`</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">A set of eviction thresholds (e.g. `memory.available<1Gi`) that if met would trigger a pod eviction. On a Linux node, the default value also includes `nodefs.inodesFree<5%`. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--eviction-max-pod-grace-period int32</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"> Maximum allowed grace period (in seconds) to use when terminating pods in response to a soft eviction threshold being met. If negative, defer to pod specified value. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--eviction-minimum-reclaim mapStringString</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">A set of minimum reclaims (e.g. `imagefs.available=2Gi`) that describes the minimum amount of resource the kubelet will reclaim when performing a pod eviction if that resource is under pressure. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--eviction-pressure-transition-period duration&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: `5m0s`</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Duration for which the kubelet has to wait before transitioning out of an eviction pressure condition. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--eviction-soft mapStringString</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">A set of eviction thresholds (e.g. `memory.available>1.5Gi`) that if met over a corresponding grace period would trigger a pod eviction. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--eviction-soft-grace-period mapStringString</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">A set of eviction grace periods (e.g. `memory.available=1m30s`) that correspond to how long a soft eviction threshold must hold before triggering a pod eviction. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--exit-on-lock-contention</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Whether kubelet should exit upon lock-file contention.</td>
</tr>

<tr>
<td colspan="2">--experimental-allocatable-ignore-eviction&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: `false`</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">When set to `true`, Hard eviction thresholds will be ignored while calculating node allocatable. See https://kubernetes.io/docs/tasks/administer-cluster/reserve-compute-resources/ for more details. (DEPRECATED: will be removed in 1.23)</td>
</tr>
    
<tr>
<td colspan="2">--experimental-bootstrap-kubeconfig string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">DEPRECATED: Use `--bootstrap-kubeconfig`</td>
</tr>

<tr>
<td colspan="2">--experimental-check-node-capabilities-before-mount</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">[Experimental] if set to `true`, the kubelet will check the underlying node for required components (binaries, etc.) before performing the mount (DEPRECATED: will be removed in 1.23, in favor of using CSI.)</td>
</tr>

<tr>
<td colspan="2">--experimental-kernel-memcg-notification</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">If enabled, the kubelet will integrate with the kernel memcg notification to determine if memory eviction thresholds are crossed rather than polling. This flag will be removed in 1.23. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--experimental-log-sanitization bool</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">[Experimental] When enabled prevents logging of fields tagged as sensitive (passwords, keys, tokens). Runtime log sanitization may introduce significant computation overhead and therefore should not be enabled in production. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's --config flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
</tr>

<tr>
<td colspan="2">--experimental-mounter-path string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: `mount`</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">[Experimental] Path of mounter binary. Leave empty to use the default `mount`. (DEPRECATED: will be removed in 1.23, in favor of using CSI.)</td>
</tr>

<tr>
<td colspan="2">--fail-swap-on&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: `true`</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Makes the Kubelet fail to start if swap is enabled on the node. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--feature-gates mapStringBool</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">A set of `key=value` pairs that describe feature gates for alpha/experimental features. Options are:<br/>
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
SeccompDefault=true|false (ALPHA - default=false)<br/>
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
(DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--file-check-frequency duration&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: `20s`</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Duration between checking config files for new data. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--hairpin-mode string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: `promiscuous-bridge`</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">How should the kubelet setup hairpin NAT. This allows endpoints of a Service to load balance back to themselves if they should try to access their own Service. Valid values are `promiscuous-bridge`, `hairpin-veth` and `none`. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--healthz-bind-address ip&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: `127.0.0.1`</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">The IP address for the healthz server to serve on (set to `0.0.0.0` for all IPv4 interfaces and `::` for all IPv6 interfaces). (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--healthz-port int32&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: 10248</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">The port of the localhost healthz endpoint (set to `0` to disable). (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">-h, --help</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">help for kubelet</td>
</tr>

<tr>
<td colspan="2">--hostname-override string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">If non-empty, will use this string as identification instead of the actual hostname. If `--cloud-provider` is set, the cloud provider determines the name of the node (consult cloud provider documentation to determine if and how the hostname is used).</td>
</tr>

<tr>
<td colspan="2">--housekeeping-interval duration&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: `10s`</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Interval between container housekeepings.</td>
</tr>

<tr>
<td colspan="2">--http-check-frequency duration&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: `20s`</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Duration between checking HTTP for new data. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--image-credential-provider-bin-dir string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">The path to the directory where credential provider plugin binaries are located.</td>
</tr>

<tr>
<td colspan="2">--image-credential-provider-config string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">The path to the credential provider plugin config file.</td>
</tr>

<tr>
<td colspan="2">--image-gc-high-threshold int32&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: 85</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">The percent of disk usage after which image garbage collection is always run. Values must be within the range [0, 100], To disable image garbage collection, set to 100.   (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--image-gc-low-threshold int32&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: 80</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">The percent of disk usage before which image garbage collection is never run. Lowest disk usage to garbage collect to. Values must be within the range [0, 100] and should not be larger than that of `--image-gc-high-threshold`. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--image-pull-progress-deadline duration&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: `1m0s`</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">If no pulling progress is made before this deadline, the image pulling will be cancelled. This docker-specific flag only works when container-runtime is set to `docker`.</td>
</tr>

<tr>
<td colspan="2">--image-service-endpoint string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">[Experimental] The endpoint of remote image service. If not specified, it will be the same with `--container-runtime-endpoint` by default. Currently UNIX socket endpoint is supported on Linux, while npipe and TCP endpoints are supported on Windows.  Examples: `unix:///var/run/dockershim.sock`, `npipe:////./pipe/dockershim`</td>
</tr>
    
<tr>
<td colspan="2">--iptables-drop-bit int32&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: 15</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">The bit of the `fwmark` space to mark packets for dropping. Must be within the range [0, 31]. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>
    
<tr>
<td colspan="2">--iptables-masquerade-bit int32&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: 14</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">The bit of the `fwmark` space to mark packets for SNAT. Must be within the range [0, 31]. Please match this parameter with corresponding parameter in `kube-proxy`. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>
    
<tr>
<td colspan="2">--keep-terminated-pod-volumes</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Keep terminated pod volumes mounted to the node after the pod terminates. Can be useful for debugging volume related issues. (DEPRECATED: will be removed in a future version)</td>
</tr>

<tr>
<td colspan="2">--kernel-memcg-notification</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">If enabled, the kubelet will integrate with the kernel memcg notification to determine if memory eviction thresholds are crossed rather than polling. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--kube-api-burst int32&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: 10</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Burst to use while talking with kubernetes API server. The number must be >= 0. If 0 will use DefaultBurst: 10. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--kube-api-content-type string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: `application/vnd.kubernetes.protobuf`</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Content type of requests sent to apiserver. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--kube-api-qps int32&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: 5</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">QPS to use while talking with kubernetes API server. The number must be >= 0. If 0 will use DefaultQPS: 5. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--kube-reserved mapStringString&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: &lt;None&gt;</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">A set of `<resource name>=<resource quantity>` (e.g. `cpu=200m,memory=500Mi,ephemeral-storage=1Gi,pid='100'`) pairs that describe resources reserved for kubernetes system components. Currently `cpu`, `memory` and local `ephemeral-storage` for root file system are supported. See http://kubernetes.io/docs/user-guide/compute-resources for more detail. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--kube-reserved-cgroup string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: `''`</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Absolute name of the top level cgroup that is used to manage kubernetes components for which compute resources were reserved via `--kube-reserved` flag. Ex. `/kube-reserved`. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--kubeconfig string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Path to a kubeconfig file, specifying how to connect to the API server. Providing `--kubeconfig` enables API server mode, omitting `--kubeconfig` enables standalone mode. </td>
</tr>

<tr>
<td colspan="2">--kubelet-cgroups string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Optional absolute name of cgroups to create and run the Kubelet in. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--lock-file string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">&lt;Warning: Alpha feature&gt; The path to file for kubelet to use as a lock file.</td>
</tr>

<tr>
<td colspan="2">--log-backtrace-at traceLocation&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: `:0`</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">When logging hits line `<file>:<N>`, emit a stack trace.</td>
</tr>

<tr>
<td colspan="2">--log-dir string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">If non-empty, write log files in this directory</td>
</tr>

<tr>
<td colspan="2">--log-file string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">If non-empty, use this log file</td>
</tr>

<tr>
<td colspan="2">--log-file-max-size uint&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: 1800</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Defines the maximum size a log file can grow to. Unit is megabytes. If the value is 0, the maximum file size is unlimited.</td>
</tr>

<tr>
<td colspan="2">--log-flush-frequency duration&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: `5s`</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Maximum number of seconds between log flushes.</td>
</tr>

<tr>
<td colspan="2">--logging-format string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: `text`</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Sets the log format. Permitted formats: `text`, `json`.\nNon-default formats don't honor these flags: `--add-dir-header`, `--alsologtostderr`, `--log-backtrace-at`, `--log-dir`, `--log-file`, `--log-file-max-size`, `--logtostderr`, `--skip_headers`, `--skip_log_headers`, `--stderrthreshold`, `--log-flush-frequency`.\nNon-default choices are currently alpha and subject to change without warning. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--logtostderr&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: `true`</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">log to standard error instead of files.</td>
</tr>

<tr>
<td colspan="2">--make-iptables-util-chains&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: `true`</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">If true, kubelet will ensure `iptables` utility rules are present on host. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--manifest-url string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">URL for accessing additional Pod specifications to run (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--manifest-url-header string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Comma-separated list of HTTP headers to use when accessing the URL provided to `--manifest-url`. Multiple headers with the same name will be added in the same order provided. This flag can be repeatedly invoked. For example: `--manifest-url-header 'a:hello,b:again,c:world' --manifest-url-header 'b:beautiful'` (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>
<tr>
<td colspan="2">--master-service-namespace string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: `default`</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">The namespace from which the kubernetes master services should be injected into pods. (DEPRECATED: This flag will be removed in a future version.)</td>
</tr>
    
<tr>
<td colspan="2">--max-open-files int&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: 1000000</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Number of files that can be opened by Kubelet process. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--max-pods int32&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: 110</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Number of Pods that can run on this Kubelet. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--maximum-dead-containers int32&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: -1</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Maximum number of old instances of containers to retain globally. Each container takes up some disk space. To disable, set to a negative number. (DEPRECATED: Use `--eviction-hard` or `--eviction-soft` instead. Will be removed in a future version.)</td>
</tr>

 <tr>
<td colspan="2">--maximum-dead-containers-per-container int32&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: 1</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Maximum number of old instances to retain per container.  Each container takes up some disk space. (DEPRECATED: Use `--eviction-hard` or `--eviction-soft` instead. Will be removed in a future version.)</td>
</tr>

<tr>
<td colspan="2">--minimum-container-ttl-duration duration</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Minimum age for a finished container before it is garbage collected.  Examples: `300ms`, `10s` or `2h45m` (DEPRECATED: Use `--eviction-hard` or `--eviction-soft` instead. Will be removed in a future version.)</td>
</tr>

<tr>
<td colspan="2">--minimum-image-ttl-duration duration&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: `2m0s`</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Minimum age for an unused image before it is garbage collected.  Examples: `300ms`, `10s` or `2h45m`. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--network-plugin string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">&lt;Warning: Alpha feature&gt; The name of the network plugin to be invoked for various events in kubelet/pod lifecycle. This docker-specific flag only works when container-runtime is set to `docker`.</td>
</tr>

<tr>
<td colspan="2">--network-plugin-mtu int32</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">&lt;Warning: Alpha feature&gt; The MTU to be passed to the network plugin, to override the default. Set to `0` to use the default 1460 MTU. This docker-specific flag only works when container-runtime is set to `docker`.</td>
</tr>

<tr>
<td colspan="2">--node-ip string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">IP address of the node. If set, kubelet will use this IP address for the node</td>
</tr>

<tr>
<td colspan="2">--node-labels mapStringString</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">&lt;Warning: Alpha feature&gt;Labels to add when registering the node in the cluster. Labels must be `key=value pairs` separated by `,`. Labels in the `kubernetes.io` namespace must begin with an allowed prefix (`kubelet.kubernetes.io`, `node.kubernetes.io`) or be in the specifically allowed set (`beta.kubernetes.io/arch`, `beta.kubernetes.io/instance-type`, `beta.kubernetes.io/os`, `failure-domain.beta.kubernetes.io/region`, `failure-domain.beta.kubernetes.io/zone`, `kubernetes.io/arch`, `kubernetes.io/hostname`, `kubernetes.io/os`, `node.kubernetes.io/instance-type`, `topology.kubernetes.io/region`, `topology.kubernetes.io/zone`)</td>
</tr>

<tr>
<td colspan="2">--node-status-max-images int32&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: 50</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">The maximum number of images to report in `node.status.images`. If `-1` is specified, no cap will be applied. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--node-status-update-frequency duration&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: `10s`</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Specifies how often kubelet posts node status to master. Note: be cautious when changing the constant, it must work with nodeMonitorGracePeriod in Node controller. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--non-masquerade-cidr string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: `10.0.0.0/8`</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Traffic to IPs outside this range will use IP masquerade. Set to `0.0.0.0/0` to never masquerade. (DEPRECATED: will be removed in a future version)</td>
</tr>

<tr>
<td colspan="2">--one-output</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">If true, only write logs to their native severity level (vs also writing to each lower severity level.
</td>
</tr>

<tr>
<td colspan="2">--oom-score-adj int32&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: -999</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">The oom-score-adj value for kubelet process. Values must be within the range [-1000, 1000]. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--pod-cidr string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">The CIDR to use for pod IP addresses, only used in standalone mode. In cluster mode, this is obtained from the master. For IPv6, the maximum number of IP's allocated is 65536 (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--pod-infra-container-image string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: `k8s.gcr.io/pause:3.2`</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"> Specified image will not be pruned by the image garbage collector. When container-runtime is set to `docker`, all containers in each pod will use the network/ipc namespaces from this image. Other CRI implementations have their own configuration to set this image.</td>
</tr>

<tr>
<td colspan="2">--pod-manifest-path string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Path to the directory containing static pod files to run, or the path to a single static pod file. Files starting with dots will be ignored. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--pod-max-pids int&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: -1</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Set the maximum number of processes per pod.  If `-1`, the kubelet defaults to the node allocatable PID capacity. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--pods-per-core int32</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Number of Pods per core that can run on this Kubelet. The total number of Pods on this Kubelet cannot exceed `--max-pods`, so `--max-pods` will be used if this calculation results in a larger number of Pods allowed on the Kubelet. A value of `0` disables this limit. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--port int32&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: 10250</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">The port for the Kubelet to serve on. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--protect-kernel-defaults</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;"> Default kubelet behaviour for kernel tuning. If set, kubelet errors if any of kernel tunables is different than kubelet defaults. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--provider-id string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Unique identifier for identifying the node in a machine database, i.e cloud provider. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--qos-reserved mapStringString</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">&lt;Warning: Alpha feature&gt; A set of `<resource name>=<percentage>` (e.g. `memory=50%`) pairs that describe how pod resource requests are reserved at the QoS level. Currently only memory is supported. Requires the `QOSReserved` feature gate to be enabled. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--read-only-port int32&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: 10255</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">The read-only port for the Kubelet to serve on with no authentication/authorization (set to `0` to disable). (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--really-crash-for-testing</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">If true, when panics occur crash. Intended for testing. (DEPRECATED: will be removed in a future version.)</td>
</tr>

<tr>
<td colspan="2">--redirect-container-streaming</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Enables container streaming redirect. If false, kubelet will proxy container streaming data between the API server and container runtime; if `true`, kubelet will return an HTTP redirect to the API server, and the API server will access container runtime directly. The proxy approach is more secure, but introduces some overhead. The redirect approach is more performant, but less secure because the connection between apiserver and container runtime may not be authenticated. (DEPRECATED: Container streaming redirection will be removed from the kubelet in v1.20, and this flag will be removed in v1.22. For more details, see http://git.k8s.io/enhancements/keps/sig-node/20191205-container-streaming-requests.md)</td>
</tr>

<tr>
<td colspan="2">--register-node&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: `true`</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Register the node with the API server. If `--kubeconfig` is not provided, this flag is irrelevant, as the Kubelet won't have an API server to register with. Default to `true`.</td>
</tr>

<tr>
<td colspan="2">--register-schedulable&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: `true`</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Register the node as schedulable. Won't have any effect if `--register-node` is false. (DEPRECATED: will be removed in a future version)</td>
  </tr>

<tr>
<td colspan="2">--register-with-taints mapStringString</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Register the node with the given list of taints (comma separated `<key>=<value>:<effect>`). No-op if `--register-node` is `false`.</td>
</tr>

<tr>
<td colspan="2">--registry-burst int32&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: 10</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Maximum size of a bursty pulls, temporarily allows pulls to burst to this number, while still not exceeding `--registry-qps`. Only used if `--registry-qps > 0`. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--registry-qps int32&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: 5</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">If &gt; 0, limit registry pull QPS to this value.  If `0`, unlimited. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--reserved-cpus string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">A comma-separated list of CPUs or CPU ranges that are reserved for system and kubernetes usage. This specific list will supersede cpu counts in `--system-reserved` and `--kube-reserved`. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--resolv-conf string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: `/etc/resolv.conf`</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Resolver configuration file used as the basis for the container DNS resolution configuration. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--root-dir string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: `/var/lib/kubelet`</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Directory path for managing kubelet files (volume mounts, etc).</td>
</tr>

<tr>
<td colspan="2">--rotate-certificates</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">&lt;Warning: Beta feature&gt; Auto rotate the kubelet client certificates by requesting new certificates from the `kube-apiserver` when the certificate expiration approaches. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--rotate-server-certificates</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Auto-request and rotate the kubelet serving certificates by requesting new certificates from the `kube-apiserver` when the certificate expiration approaches. Requires the `RotateKubeletServerCertificate` feature gate to be enabled, and approval of the submitted `CertificateSigningRequest` objects. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--runonce</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">If `true`, exit after spawning pods from local manifests or remote urls. Exclusive with `--enable-server` (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's --config flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--runtime-cgroups string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Optional absolute name of cgroups to create and run the runtime in.</td>
</tr>

<tr>
<td colspan="2">--runtime-request-timeout duration&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: `2m0s`</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Timeout of all runtime requests except long running request - `pull`, `logs`, `exec` and `attach`. When timeout exceeded, kubelet will cancel the request, throw out an error and retry later. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--seccomp-default RuntimeDefault&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: `false`</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">&lt;Warning: Alpha feature&gt; Enable the use of RuntimeDefault as the default seccomp profile for all workloads. The SeccompDefault feature gate must be enabled to allow this flag, which is disabled per default.</td>
</tr>

<tr>
<td colspan="2">--seccomp-profile-root string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: `/var/lib/kubelet/seccomp`</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">&lt;Warning: Alpha feature&gt; Directory path for seccomp profiles. (DEPRECATED: will be removed in 1.23, in favor of using the `<root-dir>/seccomp` directory)
</td>
</tr>

<tr>
<td colspan="2">--serialize-image-pulls&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: `true`</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Pull images one at a time. We recommend *not* changing the default value on nodes that run docker daemon with version &lt; 1.9 or an `aufs` storage backend. Issue #10959 has more details. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--skip-headers</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">If `true`, avoid header prefixes in the log messages</td>
</tr>

<tr>
<td colspan="2">--skip-log-headers</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">If `true`, avoid headers when opening log files</td>
</tr>

<tr>
<td colspan="2">--stderrthreshold int&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: 2</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">logs at or above this threshold go to stderr.</td>
</tr>

<tr>
<td colspan="2">--streaming-connection-idle-timeout duration&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: `4h0m0s`</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Maximum time a streaming connection can be idle before the connection is automatically closed. `0` indicates no timeout. Example: `5m`. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--sync-frequency duration&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: `1m0s`</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Max period between synchronizing running containers and config. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--system-cgroups string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Optional absolute name of cgroups in which to place all non-kernel processes that are not already inside a cgroup under `/`. Empty for no container. Rolling back the flag requires a reboot. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--system-reserved mapStringString&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: \<none\></td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">A set of `<resource name>=<resource quantity>` (e.g. `cpu=200m,memory=500Mi,ephemeral-storage=1Gi,pid='100'`) pairs that describe resources reserved for non-kubernetes components. Currently only `cpu` and `memory` are supported. See http://kubernetes.io/docs/user-guide/compute-resources for more detail. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--system-reserved-cgroup string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: `''`</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Absolute name of the top level cgroup that is used to manage non-kubernetes components for which compute resources were reserved via `--system-reserved` flag. Ex. `/system-reserved`. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--tls-cert-file string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">File containing x509 Certificate used for serving HTTPS (with intermediate certs, if any, concatenated after server cert). If `--tls-cert-file` and `--tls-private-key-file` are not provided, a self-signed certificate and key are generated for the public address and saved to the directory passed to `--cert-dir`. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--tls-cipher-suites stringSlice</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Comma-separated list of cipher suites for the server. If omitted, the default Go cipher suites will be used.<br/>
Preferred values:
TLS_AES_128_GCM_SHA256, TLS_AES_256_GCM_SHA384, TLS_CHACHA20_POLY1305_SHA256, TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA, TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256, TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA, TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384, TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305, TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256, TLS_ECDHE_RSA_WITH_3DES_EDE_CBC_SHA, TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA, TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256, TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA, TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384, TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305, TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256, TLS_RSA_WITH_3DES_EDE_CBC_SHA, TLS_RSA_WITH_AES_128_CBC_SHA, TLS_RSA_WITH_AES_128_GCM_SHA256, TLS_RSA_WITH_AES_256_CBC_SHA, TLS_RSA_WITH_AES_256_GCM_SHA384.<br/> 
Insecure values: TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256, TLS_ECDHE_ECDSA_WITH_RC4_128_SHA, TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256, TLS_ECDHE_RSA_WITH_RC4_128_SHA, TLS_RSA_WITH_AES_128_CBC_SHA256, TLS_RSA_WITH_RC4_128_SHA. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's --config flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
</tr>

<tr>
<td colspan="2">--tls-min-version string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Minimum TLS version supported. Possible values: `VersionTLS10`, `VersionTLS11`, `VersionTLS12`, `VersionTLS13` (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--tls-private-key-file string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">File containing x509 private key matching `--tls-cert-file`. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>


<tr>
<td colspan="2">--topology-manager-policy string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: `none`</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Topology Manager policy to use. Possible values: `none`, `best-effort`, `restricted`, `single-numa-node`. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--topology-manager-scope string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: `container`</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Scope to which topology hints applied. Topology Manager collects hints from Hint Providers and applies them to defined scope to ensure the pod admission. Possible values: 'container' (default), 'pod'. (default "container") (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's --config flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">-v, --v Level</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Number for the log level verbosity</td>
</tr>

<tr>
<td colspan="2">--version version[=true]</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Print version information and quit</td>
</tr>

<tr>
<td colspan="2">--vmodule moduleSpec</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Comma-separated list of `pattern=N` settings for file-filtered logging</td>
</tr>

<tr>
<td colspan="2">--volume-plugin-dir string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: `/usr/libexec/kubernetes/kubelet-plugins/volume/exec/`</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">The full path of the directory in which to search for additional third party volume plugins. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>

<tr>
<td colspan="2">--volume-stats-agg-period duration&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Default: `1m0s`</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Specifies interval for kubelet to calculate and cache the volume disk usage for all pods and volumes. To disable volume calculations, set to `0`. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's `--config` flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)</td>
</tr>
</tbody>
</table>


