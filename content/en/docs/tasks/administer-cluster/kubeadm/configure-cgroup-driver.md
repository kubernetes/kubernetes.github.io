---
title: Configuring a cgroup driver
content_type: task
weight: 10
---

<!-- overview -->

This page explains how to configure the kubelet cgroup driver to match the container
runtime cgroup driver for kubeadm clusters.

## {{% heading "prerequisites" %}}

You should be familiar with the Kubernetes
[container runtime requirements](/docs/setup/production-environment/container-runtimes).

<!-- steps -->

## Configuring the container runtime cgroup driver

The [Container runtimes](/docs/setup/production-environment/container-runtimes) page
explains that the `systemd` driver is recommended for kubeadm based setups instead
of the `cgroupfs` driver, because kubeadm manages the kubelet as a systemd service.

The page also provides details on how to setup a number of different container runtimes with the
`systemd` driver by default.

## Configuring the kubelet cgroup driver

kubeadm allows you to pass a `KubeletConfiguration` structure during `kubeadm init`.
This `KubeletConfiguration` can include the `cgroupDriver` field which controls the cgroup
driver of the kubelet.

{{< note >}}

In v1.22, if the user is not setting the `cgroupDriver` field under `KubeletConfiguration`,
`kubeadm` will default it to `systemd`.
{{< /note >}}

A minimal example of configuring the field explicitly:

```yaml
# kubeadm-config.yaml
kind: ClusterConfiguration
apiVersion: kubeadm.k8s.io/v1beta3
kubernetesVersion: v1.21.0
---
kind: KubeletConfiguration
apiVersion: kubelet.config.k8s.io/v1beta1
cgroupDriver: systemd
```

Such a configuration file can then be passed to the kubeadm command:

```shell
kubeadm init --config kubeadm-config.yaml
```

{{< note >}}
Kubeadm uses the same `KubeletConfiguration` for all nodes in the cluster.
The `KubeletConfiguration` is stored in a [ConfigMap](/docs/concepts/configuration/configmap)
object under the `kube-system` namespace.

Executing the sub commands `init`, `join` and `upgrade` would result in kubeadm
writing the `KubeletConfiguration` as a file under `/var/lib/kubelet/config.yaml`
and passing it to the local node kubelet.
{{< /note >}}

## Using the `cgroupfs` driver

As this guide explains using the `cgroupfs` driver with kubeadm is not recommended.

To continue using `cgroupfs` and to prevent `kubeadm upgrade` from modifying the
`KubeletConfiguration` cgroup driver on existing setups, you must be explicit
about its value. This applies to a case where you do not wish future versions
of kubeadm to apply the `systemd` driver by default.

See the below section on "Modify the kubelet ConfigMap" for details on
how to be explicit about the value.

If you wish to configure a container runtime to use the `cgroupfs` driver,
you must refer to the documentation of the container runtime of your choice.

## Migrating to the `systemd` driver

To change the cgroup driver of an existing kubeadm cluster to `systemd` in-place,
a similar procedure to a kubelet upgrade is required. This must include both
steps outlined below.

{{< note >}}
Alternatively, it is possible to replace the old nodes in the cluster with new ones
that use the `systemd` driver. This requires executing only the first step below
before joining the new nodes and ensuring the workloads can safely move to the new
nodes before deleting the old nodes.
{{< /note >}}

### Modify the kubelet ConfigMap

- Find the kubelet ConfigMap name using `kubectl get cm -n kube-system | grep kubelet-config`.
- Call `kubectl edit cm kubelet-config-x.yy -n kube-system` (replace `x.yy` with
the Kubernetes version).
- Either modify the existing `cgroupDriver` value or add a new field that looks like this:

  ```yaml
  cgroupDriver: systemd
  ```
  This field must be present under the `kubelet:` section of the ConfigMap.

### Update the cgroup driver on all nodes

For each node in the cluster:

- [Drain the node](/docs/tasks/administer-cluster/safely-drain-node) using `kubectl drain <node-name> --ignore-daemonsets`
- Stop the kubelet using `systemctl stop kubelet`
- Stop the container runtime
- Modify the container runtime cgroup driver to `systemd`
- Set `cgroupDriver: systemd` in `/var/lib/kubelet/config.yaml`
- Start the container runtime
- Start the kubelet using `systemctl start kubelet`
- [Uncordon the node](/docs/tasks/administer-cluster/safely-drain-node) using `kubectl uncordon <node-name>`

Execute these steps on nodes one at a time to ensure workloads
have sufficient time to schedule on different nodes.

Once the process is complete ensure that all nodes and workloads are healthy.
