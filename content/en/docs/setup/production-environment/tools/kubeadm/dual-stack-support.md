---
title: Dual-stack support with kubeadm
content_type: task
weight: 110
min-kubernetes-server-version: 1.21
---

<!-- overview -->

{{< feature-state for_k8s_version="v1.21" state="beta" >}}

Your Kubernetes cluster can run in [dual-stack](/docs/concepts/services-networking/dual-stack/) networking mode, which means that cluster networking lets you use either address family. In a dual-stack cluster, the control plane can assign both an IPv4 address and an IPv6 address to a single {{< glossary_tooltip text="Pod" term_id="pod" >}} or a {{< glossary_tooltip text="Service" term_id="service" >}}.

<!-- body -->

## {{% heading "prerequisites" %}}

You need to have installed the {{< glossary_tooltip text="kubeadm" term_id="kubeadm" >}} tool, following the steps from [Installing kubeadm](/docs/setup/production-environment/tools/kubeadm/install-kubeadm/).

For each server that you want to use as a {{< glossary_tooltip text="node" term_id="node" >}}, make sure it allows IPv6 forwarding. On Linux, you can set this by running run `sysctl -w net.ipv6.conf.all.forwarding=1` as the root user on each server.

You need to have an IPv4 and and IPv6 address range to use. Cluster operators typically
use private address ranges for IPv4. For IPv6, a cluster operator typically chooses a global
unicast address block from within `2000::/3`, using a range that is assigned to the operator.
You don't have to route the cluster's IP address ranges to the public internet.

The size of the IP address allocations should be suitable for the number of Pods and
Services that you are planning to run.

{{< note >}}
If you are upgrading an existing cluster then, by default, the `kubeadm upgrade` command
changes the [feature gate](/docs/reference/command-line-tools-reference/feature-gates/)
`IPv6DualStack` to `true` if that is not already enabled.
However, `kubeadm` does not support making modifications to the pod IP address range
(“cluster CIDR”) nor to the cluster's Service address range (“Service CIDR”).
{{< /note >}}

### Create a dual-stack cluster

To create a dual-stack cluster with `kubeadm init` you can pass command line arguments
similar to the following example:

```shell
# These address ranges are examples
kubeadm init --pod-network-cidr=10.244.0.0/16,2001:db8:42:0::/56 --service-cidr=10.96.0.0/16,2001:db8:42:1::/112
```

To make things clearer, here is an example kubeadm [configuration file](https://pkg.go.dev/k8s.io/kubernetes/cmd/kubeadm/app/apis/kubeadm/v1beta3) `kubeadm-config.yaml` for the primary dual-stack control plane node.

```yaml
---
apiVersion: kubeadm.k8s.io/v1beta3
kind: ClusterConfiguration
featureGates:
  IPv6DualStack: true
networking:
  podSubnet: 10.244.0.0/16,2001:db8:42:0::/56
  serviceSubnet: 10.96.0.0/16,2001:db8:42:1::/112
---
apiVersion: kubeadm.k8s.io/v1beta3
kind: InitConfiguration
localAPIEndpoint:
  advertiseAddress: "10.100.0.1"
  bindPort: 6443
nodeRegistration:
  kubeletExtraArgs:
    node-ip: 10.100.0.2,fd00:1:2:3::2
```

`advertiseAddress` in InitConfiguration specifies the IP address that the API Server will advertise it is listening on. The value of `advertiseAddress` equals the `--apiserver-advertise-address` flag of `kubeadm init`

Run kubeadm to initiate the dual-stack control plane node:

```shell
kubeadm init --config=kubeadm-config.yaml
```

Currently, the kube-controller-manager flags `--node-cidr-mask-size-ipv4|--node-cidr-mask-size-ipv6` are being left with default values. See [enable IPv4/IPv6 dual stack](/docs/concepts/services-networking/dual-stack#enable-ipv4ipv6-dual-stack).

{{< note >}}
The `--apiserver-advertise-address` flag does not support dual-stack.
{{< /note >}}

### Join a node to dual-stack cluster

Before joining a node, make sure that the node has IPv6 routable network interface and allows IPv6 forwarding.

Here is an example kubeadm [configuration file](https://pkg.go.dev/k8s.io/kubernetes/cmd/kubeadm/app/apis/kubeadm/v1beta3) `kubeadm-config.yaml` for joining a worker node to the cluster.

```yaml
apiVersion: kubeadm.k8s.io/v1beta3
kind: JoinConfiguration
discovery:
  bootstrapToken:
    apiServerEndpoint: 10.100.0.1:6443
nodeRegistration:
  kubeletExtraArgs:
    node-ip: 10.100.0.3,fd00:1:2:3::3
```

Also, here is an example kubeadm [configuration file](https://pkg.go.dev/k8s.io/kubernetes/cmd/kubeadm/app/apis/kubeadm/v1beta3) `kubeadm-config.yaml` for joining another control plane node to the cluster.
```yaml
apiVersion: kubeadm.k8s.io/v1beta3
kind: JoinConfiguration
controlPlane:
  localAPIEndpoint:
    advertiseAddress: "10.100.0.2"
    bindPort: 6443
discovery:
  bootstrapToken:
    apiServerEndpoint: 10.100.0.1:6443
nodeRegistration:
  kubeletExtraArgs:
    node-ip: 10.100.0.4,fd00:1:2:3::4

```

`advertiseAddress` in JoinConfiguration.controlPlane specifies the IP address that the API Server will advertise it is listening on. The value of `advertiseAddress` equals the `--apiserver-advertise-address` flag of `kubeadm join`.

```shell
kubeadm join --config=kubeadm-config.yaml ...
```

### Create a single-stack cluster

{{< note >}}
Enabling the dual-stack feature doesn't mean that you need to use dual-stack addressing.
You can deploy a single-stack cluster that has the dual-stack networking feature enabled.
{{< /note >}}

In 1.21 the `IPv6DualStack` feature is Beta and the feature gate is defaulted to `true`. To disable the feature you must configure the feature gate to `false`. Note that once the feature is GA, the feature gate will be removed.

```shell
kubeadm init --feature-gates IPv6DualStack=false
```

To make things more clear, here is an example kubeadm [configuration file](https://pkg.go.dev/k8s.io/kubernetes/cmd/kubeadm/app/apis/kubeadm/v1beta3) `kubeadm-config.yaml` for the single-stack control plane node.

```yaml
apiVersion: kubeadm.k8s.io/v1beta3
kind: ClusterConfiguration
featureGates:
  IPv6DualStack: false
networking:
  podSubnet: 10.244.0.0/16
  serviceSubnet: 10.96.0.0/16
```

## {{% heading "whatsnext" %}}

* [Validate IPv4/IPv6 dual-stack](/docs/tasks/network/validate-dual-stack) networking
* Read about [Dual-stack](/docs/concepts/services-networking/dual-stack/) cluster networking
