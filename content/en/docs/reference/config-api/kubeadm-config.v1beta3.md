---
title: kubeadm Configuration (v1beta3)
content_type: tool-reference
package: kubeadm.k8s.io/v1beta3
auto_generated: true
---
Package v1beta3 defines the v1beta3 version of the kubeadm configuration file format.
This version improves on the v1beta2 format by fixing some minor issues and adding a few new fields.

A list of changes since v1beta2:

- The deprecated `ClusterConfiguration.useHyperKubeImage` field has been removed.
  Kubeadm no longer supports the hyperkube image.
- The `ClusterConfiguration.dns.type` field has been removed since CoreDNS is the only supported
  DNS server type by kubeadm.
- Include "datapolicy" tags on the fields that hold secrets.
  This would result in the field values to be omitted when API structures are printed with klog.
- Add `InitConfiguration.skipPhases`, `JoinConfiguration.skipPhases` to allow skipping
  a list of phases during kubeadm init/join command execution.
- Add `InitConfiguration.nodeRegistration.imagePullPolicy" and
  `JoinConfiguration.nodeRegistration.imagePullPolicy` to allow specifying
  the images pull policy during kubeadm "init" and "join". The value must be
  one of "Always", "Never" or "IfNotPresent". "IfNotPresent" is the default,
  which has been the existing behavior prior to this addition.
- Add `InitConfiguration.patches.directory`, `JoinConfiguration.patches.directory`
  to allow the user to configure a directory from which to take patches for
  components deployed by kubeadm.
- Move the `BootstrapToken&lowast;` API and related utilities out of the "kubeadm" API group
  to a new group "bootstraptoken". The kubeadm API version v1beta3 no longer contains
  the `BootstrapToken&lowast;` structures.

## Migration from old kubeadm config versions

- kubeadm v1.15.x and newer can be used to migrate from the v1beta1 to v1beta2.
- kubeadm v1.22.x no longer supports v1beta1 and older APIs, but can be used to migrate v1beta2 to v1beta3.

## Basics

The preferred way to configure kubeadm is to pass an YAML configuration file with the --config option. Some of the
configuration options defined in the kubeadm config file are also available as command line flags, but only
the most common/simple use case are supported with this approach.

A kubeadm config file could contain multiple configuration types separated using three dashes (“---”).

kubeadm supports the following configuration types:

```yaml
apiVersion: kubeadm.k8s.io/v1beta3
kind: InitConfiguration
---
apiVersion: kubeadm.k8s.io/v1beta3
kind: ClusterConfiguration
---
apiVersion: kubelet.config.k8s.io/v1beta1
kind: KubeletConfiguration
---
apiVersion: kubeproxy.config.k8s.io/v1alpha1
kind: KubeProxyConfiguration
---
apiVersion: kubeadm.k8s.io/v1beta3
kind: JoinConfiguration
```

To print the defaults for "init" and "join" actions use the following commands:

```shell
kubeadm config print init-defaults
kubeadm config print join-defaults
```

The list of configuration types that must be included in a configuration file depends by the action you are
performing (init or join) and by the configuration options you are going to use (defaults or advanced customization).

If some configuration types are not provided, or provided only partially, kubeadm will use default values; defaults
provided by kubeadm includes also enforcing consistency of values across components when required (e.g.
cluster-cidr flag on controller manager and clusterCIDR on kube-proxy).

Users are always allowed to override default values, with the only exception of a small subset of setting with
relevance for security (e.g. enforce authorization-mode Node and RBAC on api server)

If the user provides a configuration types that is not expected for the action you are performing, kubeadm will
ignore those types and print a warning.

## Kubeadm init configuration types

When executing kubeadm init with the `--config` option, the following configuration types could be used:
InitConfiguration, ClusterConfiguration, KubeProxyConfiguration, KubeletConfiguration, but only one
between InitConfiguration and ClusterConfiguration is mandatory.

```yaml
apiVersion: kubeadm.k8s.io/v1beta3
kind: InitConfiguration
bootstrapTokens:
  ...
nodeRegistration:
  ...
```

The InitConfiguration type should be used to configure runtime settings, that in case of kubeadm init
are the configuration of the bootstrap token and all the setting which are specific to the node where kubeadm
is executed, including:

- NodeRegistration, that holds fields that relate to registering the new node to the cluster;
  use it to customize the node name, the CRI socket to use or any other settings that should apply to this
  node only (e.g. the node ip).

- LocalAPIEndpoint, that represents the endpoint of the instance of the API server to be deployed on this node;
  use it e.g. to customize the API server advertise address.

  ```yaml
  apiVersion: kubeadm.k8s.io/v1beta3
  kind: ClusterConfiguration
  networking:
      ...
  etcd:
      ...
  apiServer:
    extraArgs:
      ...
    extraVolumes:
      ...
  ...
  ```

The ClusterConfiguration type should be used to configure cluster-wide settings,
including settings for:

- Networking, that holds configuration for the networking topology of the cluster; use it e.g. to customize
  pod subnet or services subnet.
- Etcd configurations; use it e.g. to customize the local etcd or to configure the API server
  for using an external etcd cluster.
- kube-apiserver, kube-scheduler, kube-controller-manager configurations; use it to customize control-plane
  components by adding customized setting or overriding kubeadm default settings.

  ```yaml
  apiVersion: kubeproxy.config.k8s.io/v1alpha1
  kind: KubeProxyConfiguration
    ...
  ```

The KubeProxyConfiguration type should be used to change the configuration passed to kube-proxy instances deployed
in the cluster. If this object is not provided or provided only partially, kubeadm applies defaults.

See https://kubernetes.io/docs/reference/command-line-tools-reference/kube-proxy/ or https://godoc.org/k8s.io/kube-proxy/config/v1alpha1#KubeProxyConfiguration
for kube proxy official documentation.

```yaml
apiVersion: kubelet.config.k8s.io/v1beta1
kind: KubeletConfiguration
...
```

The KubeletConfiguration type should be used to change the configurations that will be passed to all kubelet instances
deployed in the cluster. If this object is not provided or provided only partially, kubeadm applies defaults.

See https://kubernetes.io/docs/reference/command-line-tools-reference/kubelet/ or https://godoc.org/k8s.io/kubelet/config/v1beta1#KubeletConfiguration
for kubelet official documentation.

Here is a fully populated example of a single YAML file containing multiple
configuration types to be used during a `kubeadm init` run.

```yaml
apiVersion: kubeadm.k8s.io/v1beta3
kind: InitConfiguration
bootstrapTokens:
  - token: "9a08jv.c0izixklcxtmnze7"
    description: "kubeadm bootstrap token"
    ttl: "24h"
  - token: "783bde.3f89s0fje9f38fhf"
    description: "another bootstrap token"
    usages:
      - authentication
      - signing
    groups:
      - system:bootstrappers:kubeadm:default-node-token
nodeRegistration:
  name: "ec2-10-100-0-1"
  criSocket: "/var/run/dockershim.sock"
  taints:
    - key: "kubeadmNode"
      value: "master"
      effect: "NoSchedule"
  kubeletExtraArgs:
    v: 4
  ignorePreflightErrors:
    - IsPrivilegedUser
  imagePullPolicy: "IfNotPresent"
localAPIEndpoint:
  advertiseAddress: "10.100.0.1"
  bindPort: 6443
certificateKey: "e6a2eb8581237ab72a4f494f30285ec12a9694d750b9785706a83bfcbbbd2204"
skipPhases:
  - add/kube-proxy
---
apiVersion: kubeadm.k8s.io/v1beta3
kind: ClusterConfiguration
etcd:
  # one of local or external
  local:
    imageRepository: "k8s.gcr.io"
    imageTag: "3.2.24"
    dataDir: "/var/lib/etcd"
    extraArgs:
      listen-client-urls: "http://10.100.0.1:2379"
    serverCertSANs:
      - "ec2-10-100-0-1.compute-1.amazonaws.com"
    peerCertSANs:
      - "10.100.0.1"
  # external:
    # endpoints:
    # - "10.100.0.1:2379"
    # - "10.100.0.2:2379"
    # caFile: "/etcd/kubernetes/pki/etcd/etcd-ca.crt"
    # certFile: "/etcd/kubernetes/pki/etcd/etcd.crt"
    # keyFile: "/etcd/kubernetes/pki/etcd/etcd.key"
networking:
  serviceSubnet: "10.96.0.0/12"
  podSubnet: "10.100.0.1/24"
  dnsDomain: "cluster.local"
kubernetesVersion: "v1.12.0"
controlPlaneEndpoint: "10.100.0.1:6443"
apiServer:
  extraArgs:
    authorization-mode: "Node,RBAC"
  extraVolumes:
    - name: "some-volume"
      hostPath: "/etc/some-path"
      mountPath: "/etc/some-pod-path"
      readOnly: false
      pathType: File
  certSANs:
    - "10.100.1.1"
    - "ec2-10-100-0-1.compute-1.amazonaws.com"
  timeoutForControlPlane: 4m0s
controllerManager:
  extraArgs:
    "node-cidr-mask-size": "20"
  extraVolumes:
    - name: "some-volume"
      hostPath: "/etc/some-path"
      mountPath: "/etc/some-pod-path"
      readOnly: false
      pathType: File
scheduler:
  extraArgs:
    address: "10.100.0.1"
  extraVolumes:
    - name: "some-volume"
      hostPath: "/etc/some-path"
      mountPath: "/etc/some-pod-path"
      readOnly: false
      pathType: File
certificatesDir: "/etc/kubernetes/pki"
imageRepository: "k8s.gcr.io"
clusterName: "example-cluster"
---
apiVersion: kubelet.config.k8s.io/v1beta1
kind: KubeletConfiguration
# kubelet specific options here
---
apiVersion: kubeproxy.config.k8s.io/v1alpha1
kind: KubeProxyConfiguration
# kube-proxy specific options here
```

## Kubeadm join configuration types

When executing kubeadm join with the `--config` option, the JoinConfiguration type should be provided.

```yaml
apiVersion: kubeadm.k8s.io/v1beta3
kind: JoinConfiguration
...
```

The JoinConfiguration type should be used to configure runtime settings, that in case of kubeadm join
are the discovery method used for accessing the cluster info and all the setting which are specific
to the node where kubeadm is executed, including:

- NodeRegistration, that holds fields that relate to registering the new node to the cluster;
  use it to customize the node name, the CRI socket to use or any other settings that should apply to this
  node only (e.g. the node ip).
- APIEndpoint, that represents the endpoint of the instance of the API server to be eventually
  deployed on this node.

## Resource Types 


- [ClusterConfiguration](#kubeadm-k8s-io-v1beta3-ClusterConfiguration)
- [InitConfiguration](#kubeadm-k8s-io-v1beta3-InitConfiguration)
- [JoinConfiguration](#kubeadm-k8s-io-v1beta3-JoinConfiguration)
  
    


## `ClusterConfiguration`     {#kubeadm-k8s-io-v1beta3-ClusterConfiguration}
    




ClusterConfiguration contains cluster-wide configuration for a kubeadm cluster

<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
<tbody>
    
<tr><td><code>apiVersion</code><br/>string</td><td><code>kubeadm.k8s.io/v1beta3</code></td></tr>
<tr><td><code>kind</code><br/>string</td><td><code>ClusterConfiguration</code></td></tr>
    

  
  
<tr><td><code>etcd</code><br/>
<a href="#kubeadm-k8s-io-v1beta3-Etcd"><code>Etcd</code></a>
</td>
<td>
   `etcd` holds configuration for etcd.</td>
</tr>
    
  
<tr><td><code>networking</code><br/>
<a href="#kubeadm-k8s-io-v1beta3-Networking"><code>Networking</code></a>
</td>
<td>
   `networking` holds configuration for the networking topology of the cluster.</td>
</tr>
    
  
<tr><td><code>kubernetesVersion</code><br/>
<code>string</code>
</td>
<td>
   `kubernetesVersion` is the target version of the control plane.</td>
</tr>
    
  
<tr><td><code>controlPlaneEndpoint</code><br/>
<code>string</code>
</td>
<td>
   `controlPlaneEndpoint` sets a stable IP address or DNS name for the control plane; it
can be a valid IP address or a RFC-1123 DNS subdomain, both with optional TCP port.
In case the `controlPlaneEndpoint` is not specified, the `advertiseAddress` + `bindPort`
are used; in case the `controlPlaneEndpoint` is specified but without a TCP port,
the `bindPort` of the `localAPIEndpoint` is used.
Possible usages are:

- In a cluster with more than one control plane instances, this field should be
  assigned the address of the external load balancer in front of the
  control plane instances.
- In environments with enforced node recycling, the ControlPlaneEndpoint
  could be used for assigning a stable DNS to the control plane.</td>
</tr>
    
  
<tr><td><code>apiServer</code><br/>
<a href="#kubeadm-k8s-io-v1beta3-APIServer"><code>APIServer</code></a>
</td>
<td>
   `apiServer` contains extra settings for the API server.</td>
</tr>
    
  
<tr><td><code>controllerManager</code><br/>
<a href="#kubeadm-k8s-io-v1beta3-ControlPlaneComponent"><code>ControlPlaneComponent</code></a>
</td>
<td>
   `controllerManager` contains extra settings for the controller manager.</td>
</tr>
    
  
<tr><td><code>scheduler</code><br/>
<a href="#kubeadm-k8s-io-v1beta3-ControlPlaneComponent"><code>ControlPlaneComponent</code></a>
</td>
<td>
   `scheduler` contains extra settings for the scheduler.</td>
</tr>
    
  
<tr><td><code>dns</code><br/>
<a href="#kubeadm-k8s-io-v1beta3-DNS"><code>DNS</code></a>
</td>
<td>
   `dns` defines the options for the DNS add-on.</td>
</tr>
    
  
<tr><td><code>certificatesDir</code><br/>
<code>string</code>
</td>
<td>
   `certificatesDir` specifies where to store or look for all required certificates.</td>
</tr>
    
  
<tr><td><code>imageRepository</code><br/>
<code>string</code>
</td>
<td>
   `imageRepository` sets the container registry to pull images from.
If empty, `k8s.gcr.io` will be used by default; in case of kubernetes version is
a CI build (kubernetes version starts with `ci/` or `ci-cross/`)
`gcr.io/k8s-staging-ci-images` will be used as a default for control plane
components and for kube-proxy, while `k8s.gcr.io` will be used for all the other images.</td>
</tr>
    
  
<tr><td><code>featureGates</code><br/>
<code>map[string]bool</code>
</td>
<td>
   Feature gates enabled by the user.</td>
</tr>
    
  
<tr><td><code>clusterName</code><br/>
<code>string</code>
</td>
<td>
   The cluster name.</td>
</tr>
    
  
</tbody>
</table>
    


## `InitConfiguration`     {#kubeadm-k8s-io-v1beta3-InitConfiguration}
    




InitConfiguration contains a list of elements that is specific "kubeadm init"-only runtime
information.

<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
<tbody>
    
<tr><td><code>apiVersion</code><br/>string</td><td><code>kubeadm.k8s.io/v1beta3</code></td></tr>
<tr><td><code>kind</code><br/>string</td><td><code>InitConfiguration</code></td></tr>
    

  
  
<tr><td><code>bootstrapTokens</code><br/>
<a href="#BootstrapToken"><code>[]BootstrapToken</code></a>
</td>
<td>
   `bootstrapTokens` is respected at `kubeadm init` time and describes a set of Bootstrap Tokens to create.
This information IS NOT uploaded to the kubeadm cluster configmap, partly because of its sensitive nature.</td>
</tr>
    
  
<tr><td><code>nodeRegistration</code><br/>
<a href="#kubeadm-k8s-io-v1beta3-NodeRegistrationOptions"><code>NodeRegistrationOptions</code></a>
</td>
<td>
   `nodeRegistration` holds fields that relate to registering the new control-plane node to the cluster</td>
</tr>
    
  
<tr><td><code>localAPIEndpoint</code><br/>
<a href="#kubeadm-k8s-io-v1beta3-APIEndpoint"><code>APIEndpoint</code></a>
</td>
<td>
   `localAPIEndpoint` represents the endpoint of the API server instance that's deployed on this control plane node
In HA setups, this differs from ClusterConfiguration.ControlPlaneEndpoint in the sense that ControlPlaneEndpoint
is the global endpoint for the cluster, which then loadbalances the requests to each individual API server. This
configuration object lets you customize what IP/DNS name and port the local API server advertises it's accessible
on. By default, kubeadm tries to auto-detect the IP of the default interface and use that, but in case that process
fails you may set the desired value here.</td>
</tr>
    
  
<tr><td><code>certificateKey</code><br/>
<code>string</code>
</td>
<td>
   `certificateKey` sets the key with which certificates and keys are encrypted prior to being uploaded in
a Secret in the cluster during the "uploadcerts" init phase.</td>
</tr>
    
  
<tr><td><code>skipPhases</code><br/>
<code>[]string</code>
</td>
<td>
   `skipPhases` is a list of phases to skip during command execution.
The list of phases can be obtained with the `kubeadm init --help` command.
The flag `--skip-phases` takes precedence over this field.</td>
</tr>
    
  
<tr><td><code>patches</code><br/>
<a href="#kubeadm-k8s-io-v1beta3-Patches"><code>Patches</code></a>
</td>
<td>
   `patches` contains options related to applying patches to components deployed by kubeadm during
"kubeadm init".</td>
</tr>
    
  
</tbody>
</table>
    


## `JoinConfiguration`     {#kubeadm-k8s-io-v1beta3-JoinConfiguration}
    




JoinConfiguration contains elements describing a particular node.

<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
<tbody>
    
<tr><td><code>apiVersion</code><br/>string</td><td><code>kubeadm.k8s.io/v1beta3</code></td></tr>
<tr><td><code>kind</code><br/>string</td><td><code>JoinConfiguration</code></td></tr>
    

  
  
<tr><td><code>nodeRegistration</code><br/>
<a href="#kubeadm-k8s-io-v1beta3-NodeRegistrationOptions"><code>NodeRegistrationOptions</code></a>
</td>
<td>
   `nodeRegistration` holds fields that relate to registering the new control-plane
node to the cluster</td>
</tr>
    
  
<tr><td><code>caCertPath</code><br/>
<code>string</code>
</td>
<td>
   `caCertPath` is the path to the SSL certificate authority used to
secure comunications between node and control-plane.
Defaults to "/etc/kubernetes/pki/ca.crt".</td>
</tr>
    
  
<tr><td><code>discovery</code> <B>[Required]</B><br/>
<a href="#kubeadm-k8s-io-v1beta3-Discovery"><code>Discovery</code></a>
</td>
<td>
   `discovery` specifies the options for the kubelet to use during the TLS Bootstrap process.</td>
</tr>
    
  
<tr><td><code>controlPlane</code><br/>
<a href="#kubeadm-k8s-io-v1beta3-JoinControlPlane"><code>JoinControlPlane</code></a>
</td>
<td>
   `controlPlane` defines the additional control plane instance to be deployed on the
joining node. If nil, no additional control plane instance will be deployed.</td>
</tr>
    
  
<tr><td><code>skipPhases</code><br/>
<code>[]string</code>
</td>
<td>
   `skipPhases` is a list of phases to skip during command execution.
The list of phases can be obtained with the `kubeadm join --help` command.
The flag `--skip-phases` takes precedence over this field.</td>
</tr>
    
  
<tr><td><code>patches</code><br/>
<a href="#kubeadm-k8s-io-v1beta3-Patches"><code>Patches</code></a>
</td>
<td>
   `patches` contains options related to applying patches to components deployed by kubeadm during
`kubeadm join`.</td>
</tr>
    
  
</tbody>
</table>
    


## `APIEndpoint`     {#kubeadm-k8s-io-v1beta3-APIEndpoint}
    



**Appears in:**

- [InitConfiguration](#kubeadm-k8s-io-v1beta3-InitConfiguration)

- [JoinControlPlane](#kubeadm-k8s-io-v1beta3-JoinControlPlane)


APIEndpoint struct contains elements of API server instance deployed on a node.

<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
<tbody>
    

  
<tr><td><code>advertiseAddress</code><br/>
<code>string</code>
</td>
<td>
   `advertiseAddress` sets the IP address for the API server to advertise.</td>
</tr>
    
  
<tr><td><code>bindPort</code><br/>
<code>int32</code>
</td>
<td>
   `bindPort` sets the secure port for the API Server to bind to. Defaults to 6443.</td>
</tr>
    
  
</tbody>
</table>
    


## `APIServer`     {#kubeadm-k8s-io-v1beta3-APIServer}
    



**Appears in:**

- [ClusterConfiguration](#kubeadm-k8s-io-v1beta3-ClusterConfiguration)


APIServer holds settings necessary for API server deployments in the cluster

<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
<tbody>
    

  
<tr><td><code>ControlPlaneComponent</code> <B>[Required]</B><br/>
<a href="#kubeadm-k8s-io-v1beta3-ControlPlaneComponent"><code>ControlPlaneComponent</code></a>
</td>
<td>(Members of <code>ControlPlaneComponent</code> are embedded into this type.)
   <span class="text-muted">No description provided.</span>
   </td>
</tr>
    
  
<tr><td><code>certSANs</code><br/>
<code>[]string</code>
</td>
<td>
   `certSANs` sets extra Subject Alternative Names for the API Server signing cert.</td>
</tr>
    
  
<tr><td><code>timeoutForControlPlane</code><br/>
<code>invalid type</code>
</td>
<td>
   `timeoutForControlPlane` controls the timeout that we use for API server to appear</td>
</tr>
    
  
</tbody>
</table>
    


## `BootstrapTokenDiscovery`     {#kubeadm-k8s-io-v1beta3-BootstrapTokenDiscovery}
    



**Appears in:**

- [Discovery](#kubeadm-k8s-io-v1beta3-Discovery)


BootstrapTokenDiscovery is used to set the options for bootstrap token based discovery

<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
<tbody>
    

  
<tr><td><code>token</code> <B>[Required]</B><br/>
<code>string</code>
</td>
<td>
   `token` is a token used to validate cluster information fetched from the control-plane.</td>
</tr>
    
  
<tr><td><code>apiServerEndpoint</code><br/>
<code>string</code>
</td>
<td>
   `apiServerEndpoint` is an IP or domain name to the API server from which
information will be fetched.</td>
</tr>
    
  
<tr><td><code>caCertHashes</code><br/>
<code>[]string</code>
</td>
<td>
   CACertHashes specifies a set of public key pins to verify when token-based
discovery is used. The root CA found during discovery must match one of these
values. Specifying an empty set disables root CA pinning, which can be unsafe.
Each hash is specified as `<type>:<value>`, where the only currently supported
type is "sha256". This is a hex-encoded SHA-256 hash of the Subject Public Key
Info (SPKI) object in DER-encoded ASN.1. These hashes can be calculated using,
for example, OpenSSL.</td>
</tr>
    
  
<tr><td><code>unsafeSkipCAVerification</code><br/>
<code>bool</code>
</td>
<td>
   `unsafeSkipCAVerification` allows token-based discovery without CA verification
via `caCertHashes`. This can weaken the security of kubeadm since other nodes
can impersonate the control-plane.</td>
</tr>
    
  
</tbody>
</table>
    


## `ControlPlaneComponent`     {#kubeadm-k8s-io-v1beta3-ControlPlaneComponent}
    



**Appears in:**

- [ClusterConfiguration](#kubeadm-k8s-io-v1beta3-ClusterConfiguration)

- [APIServer](#kubeadm-k8s-io-v1beta3-APIServer)


ControlPlaneComponent holds settings common to control plane component of the cluster

<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
<tbody>
    

  
<tr><td><code>extraArgs</code><br/>
<code>map[string]string</code>
</td>
<td>
   `extraArgs` is an extra set of flags to pass to the control plane component.
A key in this map is the flag name as it appears on the
command line except without leading dash(es).</td>
</tr>
    
  
<tr><td><code>extraVolumes</code><br/>
<a href="#kubeadm-k8s-io-v1beta3-HostPathMount"><code>[]HostPathMount</code></a>
</td>
<td>
   `extraVolumes` is an extra set of host volumes, mounted to the control plane component.</td>
</tr>
    
  
</tbody>
</table>
    


## `DNS`     {#kubeadm-k8s-io-v1beta3-DNS}
    



**Appears in:**

- [ClusterConfiguration](#kubeadm-k8s-io-v1beta3-ClusterConfiguration)


DNS defines the DNS addon that should be used in the cluster

<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
<tbody>
    

  
<tr><td><code>ImageMeta</code> <B>[Required]</B><br/>
<a href="#kubeadm-k8s-io-v1beta3-ImageMeta"><code>ImageMeta</code></a>
</td>
<td>(Members of <code>ImageMeta</code> are embedded into this type.)
   `imageMeta` allows to customize the image used for the DNS component.</td>
</tr>
    
  
</tbody>
</table>
    


## `DNSAddOnType`     {#kubeadm-k8s-io-v1beta3-DNSAddOnType}
    
(Alias of `string`)



DNSAddOnType defines string identifying DNS add-on types


    


## `Discovery`     {#kubeadm-k8s-io-v1beta3-Discovery}
    



**Appears in:**

- [JoinConfiguration](#kubeadm-k8s-io-v1beta3-JoinConfiguration)


Discovery specifies the options for the kubelet to use during the TLS Bootstrap process

<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
<tbody>
    

  
<tr><td><code>bootstrapToken</code><br/>
<a href="#kubeadm-k8s-io-v1beta3-BootstrapTokenDiscovery"><code>BootstrapTokenDiscovery</code></a>
</td>
<td>
   `bootstrapToken` is used to set the options for bootstrap token based discovery.
`bootstrapToken` and `file` are mutually exclusive.</td>
</tr>
    
  
<tr><td><code>file</code><br/>
<a href="#kubeadm-k8s-io-v1beta3-FileDiscovery"><code>FileDiscovery</code></a>
</td>
<td>
   `file` specifies a file or URL to a kubeconfig file from which to load cluster information.
`bootstrapToken` and `file` are mutually exclusive.</td>
</tr>
    
  
<tr><td><code>tlsBootstrapToken</code><br/>
<code>string</code>
</td>
<td>
   `tlsBootstrapToken` is a token used for TLS bootstrapping.
If `bootstrapToken` is set, this field is defaulted to `bootstrapToken.token`,
but can be overridden.
If `file` is set, this field &lowast;&lowast;must be set&lowast;&lowast; in case the KubeConfigFile does
not contain any other authentication information</td>
</tr>
    
  
<tr><td><code>timeout</code><br/>
<code>invalid type</code>
</td>
<td>
   `timeout` modifies the discovery timeout.</td>
</tr>
    
  
</tbody>
</table>
    


## `Etcd`     {#kubeadm-k8s-io-v1beta3-Etcd}
    



**Appears in:**

- [ClusterConfiguration](#kubeadm-k8s-io-v1beta3-ClusterConfiguration)


Etcd contains elements describing Etcd configuration.

<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
<tbody>
    

  
<tr><td><code>local</code><br/>
<a href="#kubeadm-k8s-io-v1beta3-LocalEtcd"><code>LocalEtcd</code></a>
</td>
<td>
   `local` provides configuration knobs for configuring the local etcd instance.
`local` and `external` are mutually exclusive.</td>
</tr>
    
  
<tr><td><code>external</code><br/>
<a href="#kubeadm-k8s-io-v1beta3-ExternalEtcd"><code>ExternalEtcd</code></a>
</td>
<td>
   `external` describes how to connect to an external etcd cluster.
`local` and `external` are mutually exclusive.</td>
</tr>
    
  
</tbody>
</table>
    


## `ExternalEtcd`     {#kubeadm-k8s-io-v1beta3-ExternalEtcd}
    



**Appears in:**

- [Etcd](#kubeadm-k8s-io-v1beta3-Etcd)


ExternalEtcd describes an external etcd cluster.
Kubeadm has no knowledge of where certificate files live and they must be supplied.

<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
<tbody>
    

  
<tr><td><code>endpoints</code> <B>[Required]</B><br/>
<code>[]string</code>
</td>
<td>
   `endpoints` are endpoints of etcd members. This field is required.</td>
</tr>
    
  
<tr><td><code>caFile</code> <B>[Required]</B><br/>
<code>string</code>
</td>
<td>
   `caFile` is an SSL Certificate Authority file used to secure etcd communication.
Required if using a TLS connection.</td>
</tr>
    
  
<tr><td><code>certFile</code> <B>[Required]</B><br/>
<code>string</code>
</td>
<td>
   `certFile` is an SSL certification file used to secure etcd communication.
Required if using a TLS connection.</td>
</tr>
    
  
<tr><td><code>keyFile</code> <B>[Required]</B><br/>
<code>string</code>
</td>
<td>
   `keyFile` is an SSL key file used to secure etcd communication.
Required if using a TLS connection.</td>
</tr>
    
  
</tbody>
</table>
    


## `FileDiscovery`     {#kubeadm-k8s-io-v1beta3-FileDiscovery}
    



**Appears in:**

- [Discovery](#kubeadm-k8s-io-v1beta3-Discovery)


FileDiscovery is used to specify a file or URL to a kubeconfig file from which to load cluster information

<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
<tbody>
    

  
<tr><td><code>kubeConfigPath</code> <B>[Required]</B><br/>
<code>string</code>
</td>
<td>
   `kubeConfigPath` specifies the actual file path or URL to the kubeconfig file
from which to load cluster information</td>
</tr>
    
  
</tbody>
</table>
    


## `HostPathMount`     {#kubeadm-k8s-io-v1beta3-HostPathMount}
    



**Appears in:**

- [ControlPlaneComponent](#kubeadm-k8s-io-v1beta3-ControlPlaneComponent)


HostPathMount contains elements describing volumes that are mounted from the host.

<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
<tbody>
    

  
<tr><td><code>name</code> <B>[Required]</B><br/>
<code>string</code>
</td>
<td>
   `name` is the volume name inside the Pod template.</td>
</tr>
    
  
<tr><td><code>hostPath</code> <B>[Required]</B><br/>
<code>string</code>
</td>
<td>
   `hostPath` is the path in the host that will be mounted inside the Pod.</td>
</tr>
    
  
<tr><td><code>mountPath</code> <B>[Required]</B><br/>
<code>string</code>
</td>
<td>
   `mountPath` is the path inside the Pod where the `hostPath` volume is mounted.</td>
</tr>
    
  
<tr><td><code>readOnly</code><br/>
<code>bool</code>
</td>
<td>
   `readOnly` controls write access to the volume.</td>
</tr>
    
  
<tr><td><code>pathType</code><br/>
<code>invalid type</code>
</td>
<td>
   `pathType` is the type of the `hostPath` volume.</td>
</tr>
    
  
</tbody>
</table>
    


## `ImageMeta`     {#kubeadm-k8s-io-v1beta3-ImageMeta}
    



**Appears in:**

- [DNS](#kubeadm-k8s-io-v1beta3-DNS)

- [LocalEtcd](#kubeadm-k8s-io-v1beta3-LocalEtcd)


ImageMeta allows to customize the image used for components that are not
originated from the Kubernetes/Kubernetes release process

<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
<tbody>
    

  
<tr><td><code>imageRepository</code><br/>
<code>string</code>
</td>
<td>
   `imageRepository` sets the container registry to pull images from.
If not set, the ImageRepository defined in ClusterConfiguration will be used instead.</td>
</tr>
    
  
<tr><td><code>imageTag</code><br/>
<code>string</code>
</td>
<td>
   `imageTag` allows to specify a tag for the image.
In case this value is set, kubeadm does not change automatically the
version of the above components during upgrades.</td>
</tr>
    
  
</tbody>
</table>
    


## `JoinControlPlane`     {#kubeadm-k8s-io-v1beta3-JoinControlPlane}
    



**Appears in:**

- [JoinConfiguration](#kubeadm-k8s-io-v1beta3-JoinConfiguration)


JoinControlPlane contains elements describing an additional control plane instance to be deployed on the joining node.

<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
<tbody>
    

  
<tr><td><code>localAPIEndpoint</code><br/>
<a href="#kubeadm-k8s-io-v1beta3-APIEndpoint"><code>APIEndpoint</code></a>
</td>
<td>
   `localAPIEndpoint` represents the endpoint of the API server instance to be deployed
on this node.</td>
</tr>
    
  
<tr><td><code>certificateKey</code><br/>
<code>string</code>
</td>
<td>
   `certificateKey` is the key that is used for decryption of certificates after they
are downloaded from the secret upon joining a new control plane node. The
corresponding encryption key is in the InitConfiguration.</td>
</tr>
    
  
</tbody>
</table>
    


## `LocalEtcd`     {#kubeadm-k8s-io-v1beta3-LocalEtcd}
    



**Appears in:**

- [Etcd](#kubeadm-k8s-io-v1beta3-Etcd)


LocalEtcd describes that kubeadm should run an etcd cluster locally

<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
<tbody>
    

  
<tr><td><code>ImageMeta</code> <B>[Required]</B><br/>
<a href="#kubeadm-k8s-io-v1beta3-ImageMeta"><code>ImageMeta</code></a>
</td>
<td>(Members of <code>ImageMeta</code> are embedded into this type.)
   `ImageMeta` allows to customize the container used for etcd.</td>
</tr>
    
  
<tr><td><code>dataDir</code> <B>[Required]</B><br/>
<code>string</code>
</td>
<td>
   `dataDir` is the directory etcd will place its data.
Defaults to "/var/lib/etcd".</td>
</tr>
    
  
<tr><td><code>extraArgs</code><br/>
<code>map[string]string</code>
</td>
<td>
   `extraArgs` are extra arguments provided to the etcd binary
when run inside a static pod.
A key in this map is the flag name as it appears on the command line except
without leading dash(es).</td>
</tr>
    
  
<tr><td><code>serverCertSANs</code><br/>
<code>[]string</code>
</td>
<td>
   `serverCertSANs` sets extra Subject Alternative Names for the etcd server signing cert.</td>
</tr>
    
  
<tr><td><code>peerCertSANs</code><br/>
<code>[]string</code>
</td>
<td>
   `peerCertSANs` sets extra Subject Alternative Names for the etcd peer signing cert.</td>
</tr>
    
  
</tbody>
</table>
    


## `Networking`     {#kubeadm-k8s-io-v1beta3-Networking}
    



**Appears in:**

- [ClusterConfiguration](#kubeadm-k8s-io-v1beta3-ClusterConfiguration)


Networking contains elements describing cluster's networking configuration

<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
<tbody>
    

  
<tr><td><code>serviceSubnet</code><br/>
<code>string</code>
</td>
<td>
   `serviceSubnet` is the subnet used by k8s services. Defaults to "10.96.0.0/12".</td>
</tr>
    
  
<tr><td><code>podSubnet</code><br/>
<code>string</code>
</td>
<td>
   `podSubnet` is the subnet used by Pods.</td>
</tr>
    
  
<tr><td><code>dnsDomain</code><br/>
<code>string</code>
</td>
<td>
   `dnsDomain` is the DNS domain used by k8s services. Defaults to "cluster.local".</td>
</tr>
    
  
</tbody>
</table>
    


## `NodeRegistrationOptions`     {#kubeadm-k8s-io-v1beta3-NodeRegistrationOptions}
    



**Appears in:**

- [InitConfiguration](#kubeadm-k8s-io-v1beta3-InitConfiguration)

- [JoinConfiguration](#kubeadm-k8s-io-v1beta3-JoinConfiguration)


NodeRegistrationOptions holds fields that relate to registering a new control-plane or node to the cluster, either via "kubeadm init" or "kubeadm join"

<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
<tbody>
    

  
<tr><td><code>name</code><br/>
<code>string</code>
</td>
<td>
   `name` is the `.metadata.name` field of the Node API object that will be created in this
`kubeadm init` or `kubeadm join` operation.
This field is also used in the `CommonName` field of the kubelet's client certificate to the
API server. Defaults to the hostname of the node if not provided.</td>
</tr>
    
  
<tr><td><code>criSocket</code><br/>
<code>string</code>
</td>
<td>
   `criSocket` is used to retrieve container runtime info. This information will be
annotated to the Node API object, for later re-use.</td>
</tr>
    
  
<tr><td><code>taints</code> <B>[Required]</B><br/>
<code>[]invalid type</code>
</td>
<td>
   `taints` specifies the taints the Node API object should be registered with. If
this field is unset, i.e. nil, in the `kubeadm init` process, it will be defaulted
to `['"node-role.kubernetes.io/master"=""']`. If you don't want to taint your
control-plane node, set this field to an empty list, i.e. `taints: []` in the YAML
file. This field is solely used for Node registration.</td>
</tr>
    
  
<tr><td><code>kubeletExtraArgs</code><br/>
<code>map[string]string</code>
</td>
<td>
   `kubeletExtraArgs` passes through extra arguments to the kubelet. The arguments here
are passed to the kubelet command line via the environment file kubeadm writes at
runtime for the kubelet to source. This overrides the generic base-level
configuration in the "kubelet-config-1.X" ConfigMap. Flags have higher priority when
parsing. These values are local and specific to the node kubeadm is executing on.
A key in this map is the flag name as it appears on the command line except without
leading dash(es).</td>
</tr>
    
  
<tr><td><code>ignorePreflightErrors</code><br/>
<code>[]string</code>
</td>
<td>
   `ignorePreflightErrors` provides a slice of pre-flight errors to be ignored when
the current node is registered.</td>
</tr>
    
  
<tr><td><code>imagePullPolicy</code><br/>
<code>invalid type</code>
</td>
<td>
   `imagePullPolicy` specifies the policy for image pulling during `kubeadm init` and
`kubeadm join` operations.
The value of this field must be one of "Always", "IfNotPresent" or "Never".
If this field is unset kubeadm will default it to "IfNotPresent", or pull the required
images if not present on the host.</td>
</tr>
    
  
</tbody>
</table>
    


## `Patches`     {#kubeadm-k8s-io-v1beta3-Patches}
    



**Appears in:**

- [InitConfiguration](#kubeadm-k8s-io-v1beta3-InitConfiguration)

- [JoinConfiguration](#kubeadm-k8s-io-v1beta3-JoinConfiguration)


Patches contains options related to applying patches to components deployed by kubeadm.

<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
<tbody>
    

  
<tr><td><code>directory</code><br/>
<code>string</code>
</td>
<td>
   `directory` is a path to a directory that contains files named
`target[suffix][+patchtype].extension`.
For example, `kube-apiserver0+merge.yaml` or just `etcd.json`. `target` can be one of
"kube-apiserver", "kube-controller-manager", "kube-scheduler", "etcd". `patchtype` can be one
of "strategic", "merge" or "json" and they match the patch formats supported by kubectl.
The default `patchtype` is "strategic". `extension` must be either "json" or "yaml".
`suffix` is an optional string that can be used to determine which patches are applied
first alpha-numerically.</td>
</tr>
    
  
</tbody>
</table>
    
  
  
    

## `BootstrapToken`     {#BootstrapToken}
    



**Appears in:**

- [InitConfiguration](#kubeadm-k8s-io-v1beta3-InitConfiguration)


BootstrapToken describes one bootstrap token, stored as a Secret in the cluster

<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
<tbody>
    

  
<tr><td><code>token</code> <B>[Required]</B><br/>
<a href="#BootstrapTokenString"><code>BootstrapTokenString</code></a>
</td>
<td>
   `token` is used for establishing bidirectional trust between nodes and control-planes.
Used for joining nodes in the cluster.</td>
</tr>
    
  
<tr><td><code>description</code><br/>
<code>string</code>
</td>
<td>
   `description` sets a human-friendly message why this token exists and what it's used
for, so other administrators can know its purpose.</td>
</tr>
    
  
<tr><td><code>ttl</code><br/>
<code>invalid type</code>
</td>
<td>
   `ttl` defines the time to live for this token. Defaults to `24h`.
`expires` and `ttl` are mutually exclusive.</td>
</tr>
    
  
<tr><td><code>expires</code><br/>
<code>invalid type</code>
</td>
<td>
   `expires` specifies the timestamp when this token expires. Defaults to being set
dynamically at runtime based on the `ttl`. `expires` and `ttl` are mutually exclusive.</td>
</tr>
    
  
<tr><td><code>usages</code><br/>
<code>[]string</code>
</td>
<td>
   `usages` describes the ways in which this token can be used. Can by default be used
for establishing bidirectional trust, but that can be changed here.</td>
</tr>
    
  
<tr><td><code>groups</code><br/>
<code>[]string</code>
</td>
<td>
   `groups` specifies the extra groups that this token will authenticate as when/if
used for authentication</td>
</tr>
    
  
</tbody>
</table>

## `BootstrapTokenString`     {#BootstrapTokenString}
    



**Appears in:**

- [BootstrapToken](#BootstrapToken)


BootstrapTokenString is a token of the format `abcdef.abcdef0123456789` that is used
for both validation of the practically of the API server from a joining node's point
of view and as an authentication method for the node in the bootstrap phase of
"kubeadm join". This token is and should be short-lived.

<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
<tbody>
    

  
<tr><td><code>-</code> <B>[Required]</B><br/>
<code>string</code>
</td>
<td>
   <span class="text-muted">No description provided.</span>
   </td>
</tr>
    
  
<tr><td><code>-</code> <B>[Required]</B><br/>
<code>string</code>
</td>
<td>
   <span class="text-muted">No description provided.</span>
   </td>
</tr>
    
  
</tbody>
</table>
