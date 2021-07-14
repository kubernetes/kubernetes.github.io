---
reviewers:
- luxas
- jbeda
title: kubeadm config
content_type: concept
weight: 50
---

<!-- overview -->
During `kubeadm init`, kubeadm uploads the `ClusterConfiguration` object to your cluster
in a ConfigMap called `kubeadm-config` in the `kube-system` namespace. This configuration is then read during
`kubeadm join`, `kubeadm reset` and `kubeadm upgrade`.

You can use `kubeadm config print` to print the default configuration and `kubeadm config migrate` to
convert your old configuration files to a newer version. `kubeadm config images list` and
`kubeadm config images pull` can be used to list and pull the images that kubeadm requires.

For more information navigate to
[Using kubeadm init with a configuration file](/docs/reference/setup-tools/kubeadm/kubeadm-init/#config-file)
or [Using kubeadm join with a configuration file](/docs/reference/setup-tools/kubeadm/kubeadm-join/#config-file).

You can also configure several kubelet-configuration options with `kubeadm init`. These options will be the same on any node in your cluster.
See [Configuring each kubelet in your cluster using kubeadm](/docs/setup/production-environment/tools/kubeadm/kubelet-integration/) for details.

In Kubernetes v1.13.0 and later to list/pull kube-dns images instead of the CoreDNS image
the `--config` method described [here](/docs/reference/setup-tools/kubeadm/kubeadm-init-phase/#cmd-phase-addon)
has to be used.

<!-- body -->
## kubeadm config print {#cmd-config-print}

{{< include "generated/kubeadm_config_print.md" >}}

## kubeadm config print init-defaults {#cmd-config-print-init-defaults}

{{< include "generated/kubeadm_config_print_init-defaults.md" >}}

## kubeadm config print join-defaults {#cmd-config-print-join-defaults}

{{< include "generated/kubeadm_config_print_join-defaults.md" >}}

## kubeadm config migrate {#cmd-config-migrate}

{{< include "generated/kubeadm_config_migrate.md" >}}

## kubeadm config images list {#cmd-config-images-list}

{{< include "generated/kubeadm_config_images_list.md" >}}

## kubeadm config images pull {#cmd-config-images-pull}

{{< include "generated/kubeadm_config_images_pull.md" >}}

## {{% heading "whatsnext" %}}

* [kubeadm upgrade](/docs/reference/setup-tools/kubeadm/kubeadm-upgrade/) to upgrade a Kubernetes cluster to a newer version
