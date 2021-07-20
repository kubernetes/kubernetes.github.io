---
reviewers:
- sig-cluster-lifecycle
title: Upgrading kubeadm clusters
content_type: task
weight: 20
---

<!-- overview -->

This page explains how to upgrade a Kubernetes cluster created with kubeadm from version
{{< skew currentVersionAddMinor -1 >}}.x to version {{< skew currentVersion >}}.x, and from version
{{< skew currentVersion >}}.x to {{< skew currentVersion >}}.y (where `y > x`). Skipping MINOR versions
when upgrading is unsupported.

To see information about upgrading clusters created using older versions of kubeadm,
please refer to following pages instead:

- [Upgrading a kubeadm cluster from {{< skew currentVersionAddMinor -2 >}} to {{< skew currentVersionAddMinor -1 >}}](https://v{{< skew currentVersionAddMinor -1 "-" >}}.docs.kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/)
- [Upgrading a kubeadm cluster from {{< skew currentVersionAddMinor -3 >}} to {{< skew currentVersionAddMinor -2 >}}](https://v{{< skew currentVersionAddMinor -2 "-" >}}.docs.kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/)
- [Upgrading a kubeadm cluster from {{< skew currentVersionAddMinor -4 >}} to {{< skew currentVersionAddMinor -3 >}}](https://v{{< skew currentVersionAddMinor -3 "-" >}}.docs.kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/)
- [Upgrading a kubeadm cluster from {{< skew currentVersionAddMinor -5 >}} to {{< skew currentVersionAddMinor -4 >}}](https://v{{< skew currentVersionAddMinor -4 "-" >}}.docs.kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/)

The upgrade workflow at high level is the following:

1. Upgrade a primary control plane node.
1. Upgrade additional control plane nodes.
1. Upgrade worker nodes.

## {{% heading "prerequisites" %}}

- Make sure you read the [release notes]({{< latest-release-notes >}}) carefully.
- The cluster should use a static control plane and etcd pods or external etcd.
- Make sure to back up any important components, such as app-level state stored in a database.
  `kubeadm upgrade` does not touch your workloads, only components internal to Kubernetes, but backups are always a best practice.
- [Swap must be disabled](https://serverfault.com/questions/684771/best-way-to-disable-swap-in-linux).

### Additional information

- [Draining nodes](/docs/tasks/administer-cluster/safely-drain-node/) before kubelet MINOR version
  upgrades is required. In the case of control plane nodes, they could be running CoreDNS Pods or other critical workloads.
- All containers are restarted after upgrade, because the container spec hash value is changed.

<!-- steps -->

## Determine which version to upgrade to

Find the latest stable {{< skew currentVersion >}} version using the OS package manager:

{{< tabs name="k8s_install_versions" >}}
{{% tab name="Ubuntu, Debian or HypriotOS" %}}
    apt update
    apt-cache madison kubeadm
    # find the latest {{< skew currentVersion >}} version in the list
    # it should look like {{< skew currentVersion >}}.x-00, where x is the latest patch
{{% /tab %}}
{{% tab name="CentOS, RHEL or Fedora" %}}
    yum list --showduplicates kubeadm --disableexcludes=kubernetes
    # find the latest {{< skew currentVersion >}} version in the list
    # it should look like {{< skew currentVersion >}}.x-0, where x is the latest patch
{{% /tab %}}
{{< /tabs >}}

## Upgrading control plane nodes

The upgrade procedure on control plane nodes should be executed one node at a time.
Pick a control plane node that you wish to upgrade first. It must have the `/etc/kubernetes/admin.conf` file.

### Call "kubeadm upgrade"

**For the first control plane node**

-  Upgrade kubeadm:

{{< tabs name="k8s_install_kubeadm_first_cp" >}}
{{% tab name="Ubuntu, Debian or HypriotOS" %}}
    # replace x in {{< skew currentVersion >}}.x-00 with the latest patch version
    apt-mark unhold kubeadm && \
    apt-get update && apt-get install -y kubeadm={{< skew currentVersion >}}.x-00 && \
    apt-mark hold kubeadm
    -
    # since apt-get version 1.1 you can also use the following method
    apt-get update && \
    apt-get install -y --allow-change-held-packages kubeadm={{< skew currentVersion >}}.x-00
{{% /tab %}}
{{% tab name="CentOS, RHEL or Fedora" %}}
    # replace x in {{< skew currentVersion >}}.x-0 with the latest patch version
    yum install -y kubeadm-{{< skew currentVersion >}}.x-0 --disableexcludes=kubernetes
{{% /tab %}}
{{< /tabs >}}

-  Verify that the download works and has the expected version:

    ```shell
    kubeadm version
    ```

-   Verify the upgrade plan:

    ```shell
    kubeadm upgrade plan
    ```

    This command checks that your cluster can be upgraded, and fetches the versions you can upgrade to.
    It also shows a table with the component config version states.

{{< note >}}
`kubeadm upgrade` also automatically renews the certificates that it manages on this node.
To opt-out of certificate renewal the flag `--certificate-renewal=false` can be used.
For more information see the [certificate management guide](/docs/tasks/administer-cluster/kubeadm/kubeadm-certs).
{{</ note >}}

{{< note >}}
If `kubeadm upgrade plan` shows any component configs that require manual upgrade, users must provide
a config file with replacement configs to `kubeadm upgrade apply` via the `--config` command line flag.
Failing to do so will cause `kubeadm upgrade apply` to exit with an error and not perform an upgrade.
{{</ note >}}

-  Choose a version to upgrade to, and run the appropriate command. For example:

    ```shell
    # replace x with the patch version you picked for this upgrade
    sudo kubeadm upgrade apply v{{< skew currentVersion >}}.x
    ```

    Once the command finishes you should see:

    ```
    [upgrade/successful] SUCCESS! Your cluster was upgraded to "v{{< skew currentVersion >}}.x". Enjoy!

    [upgrade/kubelet] Now that your control plane is upgraded, please proceed with upgrading your kubelets if you haven't already done so.
    ```

-  Manually upgrade your CNI provider plugin.

    Your Container Network Interface (CNI) provider may have its own upgrade instructions to follow.
    Check the [addons](/docs/concepts/cluster-administration/addons/) page to
    find your CNI provider and see whether additional upgrade steps are required.

    This step is not required on additional control plane nodes if the CNI provider runs as a DaemonSet.

**For the other control plane nodes**

Same as the first control plane node but use:

```
sudo kubeadm upgrade node
```

instead of:

```
sudo kubeadm upgrade apply
```

Also calling `kubeadm upgrade plan` and upgrading the CNI provider plugin is no longer needed.

### Drain the node

-  Prepare the node for maintenance by marking it unschedulable and evicting the workloads:

    ```shell
    # replace <node-to-drain> with the name of your node you are draining
    kubectl drain <node-to-drain> --ignore-daemonsets
    ```

### Upgrade kubelet and kubectl

-  Upgrade the kubelet and kubectl

{{< tabs name="k8s_install_kubelet" >}}
{{< tab name="Ubuntu, Debian or HypriotOS" >}}
    <pre>
    # replace x in {{< skew currentVersion >}}.x-00 with the latest patch version
    apt-mark unhold kubelet kubectl && \
    apt-get update && apt-get install -y kubelet={{< skew currentVersion >}}.x-00 kubectl={{< skew currentVersion >}}.x-00 && \
    apt-mark hold kubelet kubectl
    -
    # since apt-get version 1.1 you can also use the following method
    apt-get update && \
    apt-get install -y --allow-change-held-packages kubelet={{< skew currentVersion >}}.x-00 kubectl={{< skew currentVersion >}}.x-00
    </pre>
{{< /tab >}}
{{< tab name="CentOS, RHEL or Fedora" >}}
    <pre>
    # replace x in {{< skew currentVersion >}}.x-0 with the latest patch version
    yum install -y kubelet-{{< skew currentVersion >}}.x-0 kubectl-{{< skew currentVersion >}}.x-0 --disableexcludes=kubernetes
    </pre>
{{< /tab >}}
{{< /tabs >}}

-  Restart the kubelet:

    ```shell
    sudo systemctl daemon-reload
    sudo systemctl restart kubelet
    ```

### Uncordon the node

-   Bring the node back online by marking it schedulable:

    ```shell
    # replace <node-to-drain> with the name of your node
    kubectl uncordon <node-to-drain>
    ```

## Upgrade worker nodes

The upgrade procedure on worker nodes should be executed one node at a time or few nodes at a time,
without compromising the minimum required capacity for running your workloads.

### Upgrade kubeadm

-  Upgrade kubeadm:

{{< tabs name="k8s_install_kubeadm_worker_nodes" >}}
{{% tab name="Ubuntu, Debian or HypriotOS" %}}
    # replace x in {{< skew currentVersion >}}.x-00 with the latest patch version
    apt-mark unhold kubeadm && \
    apt-get update && apt-get install -y kubeadm={{< skew currentVersion >}}.x-00 && \
    apt-mark hold kubeadm
    -
    # since apt-get version 1.1 you can also use the following method
    apt-get update && \
    apt-get install -y --allow-change-held-packages kubeadm={{< skew currentVersion >}}.x-00
{{% /tab %}}
{{% tab name="CentOS, RHEL or Fedora" %}}
    # replace x in {{< skew currentVersion >}}.x-0 with the latest patch version
    yum install -y kubeadm-{{< skew currentVersion >}}.x-0 --disableexcludes=kubernetes
{{% /tab %}}
{{< /tabs >}}

### Call "kubeadm upgrade"

-  For worker nodes this upgrades the local kubelet configuration:

    ```shell
    sudo kubeadm upgrade node
    ```

### Drain the node

-  Prepare the node for maintenance by marking it unschedulable and evicting the workloads:

    ```shell
    # replace <node-to-drain> with the name of your node you are draining
    kubectl drain <node-to-drain> --ignore-daemonsets
    ```

### Upgrade kubelet and kubectl

-  Upgrade the kubelet and kubectl:

{{< tabs name="k8s_kubelet_and_kubectl" >}}
{{% tab name="Ubuntu, Debian or HypriotOS" %}}
    # replace x in {{< skew currentVersion >}}.x-00 with the latest patch version
    apt-mark unhold kubelet kubectl && \
    apt-get update && apt-get install -y kubelet={{< skew currentVersion >}}.x-00 kubectl={{< skew currentVersion >}}.x-00 && \
    apt-mark hold kubelet kubectl
    -
    # since apt-get version 1.1 you can also use the following method
    apt-get update && \
    apt-get install -y --allow-change-held-packages kubelet={{< skew currentVersion >}}.x-00 kubectl={{< skew currentVersion >}}.x-00
{{% /tab %}}
{{% tab name="CentOS, RHEL or Fedora" %}}
    # replace x in {{< skew currentVersion >}}.x-0 with the latest patch version
    yum install -y kubelet-{{< skew currentVersion >}}.x-0 kubectl-{{< skew currentVersion >}}.x-0 --disableexcludes=kubernetes
{{% /tab %}}
{{< /tabs >}}

-  Restart the kubelet:

    ```shell
    sudo systemctl daemon-reload
    sudo systemctl restart kubelet
    ```

### Uncordon the node

-   Bring the node back online by marking it schedulable:

    ```shell
    # replace <node-to-drain> with the name of your node
    kubectl uncordon <node-to-drain>
    ```

## Verify the status of the cluster

After the kubelet is upgraded on all nodes verify that all nodes are available again by running the following command
from anywhere kubectl can access the cluster:

```shell
kubectl get nodes
```

The `STATUS` column should show `Ready` for all your nodes, and the version number should be updated.

## Recovering from a failure state

If `kubeadm upgrade` fails and does not roll back, for example because of an unexpected shutdown during execution, you can run `kubeadm upgrade` again.
This command is idempotent and eventually makes sure that the actual state is the desired state you declare.

To recover from a bad state, you can also run `kubeadm upgrade apply --force` without changing the version that your cluster is running.

During upgrade kubeadm writes the following backup folders under `/etc/kubernetes/tmp`:
- `kubeadm-backup-etcd-<date>-<time>`
- `kubeadm-backup-manifests-<date>-<time>`

`kubeadm-backup-etcd` contains a backup of the local etcd member data for this control plane Node.
In case of an etcd upgrade failure and if the automatic rollback does not work, the contents of this folder
can be manually restored in `/var/lib/etcd`. In case external etcd is used this backup folder will be empty.

`kubeadm-backup-manifests` contains a backup of the static Pod manifest files for this control plane Node.
In case of a upgrade failure and if the automatic rollback does not work, the contents of this folder can be
manually restored in `/etc/kubernetes/manifests`. If for some reason there is no difference between a pre-upgrade
and post-upgrade manifest file for a certain component, a backup file for it will not be written.

## How it works

`kubeadm upgrade apply` does the following:

- Checks that your cluster is in an upgradeable state:
  - The API server is reachable
  - All nodes are in the `Ready` state
  - The control plane is healthy
- Enforces the version skew policies.
- Makes sure the control plane images are available or available to pull to the machine.
- Generates replacements and/or uses user supplied overwrites if component configs require version upgrades.
- Upgrades the control plane components or rollbacks if any of them fails to come up.
- Applies the new `kube-dns` and `kube-proxy` manifests and makes sure that all necessary RBAC rules are created.
- Creates new certificate and key files of the API server and backs up old files if they're about to expire in 180 days.

`kubeadm upgrade node` does the following on additional control plane nodes:

- Fetches the kubeadm `ClusterConfiguration` from the cluster.
- Optionally backups the kube-apiserver certificate.
- Upgrades the static Pod manifests for the control plane components.
- Upgrades the kubelet configuration for this node.

`kubeadm upgrade node` does the following on worker nodes:

- Fetches the kubeadm `ClusterConfiguration` from the cluster.
- Upgrades the kubelet configuration for this node.
