---
title: "Kubeadm"
weight: 10
no_list: true
content_type: concept
card:
  name: reference
  weight: 40
---

<img src="https://raw.githubusercontent.com/kubernetes/kubeadm/master/logos/stacked/color/kubeadm-stacked-color.png" align="right" width="150px">Kubeadm is a tool built to provide `kubeadm init` and `kubeadm join` as best-practice "fast paths" for creating Kubernetes clusters.

kubeadm performs the actions necessary to get a minimum viable cluster up and running. By design, it cares only about bootstrapping, not about provisioning machines. Likewise, installing various nice-to-have addons, like the Kubernetes Dashboard, monitoring solutions, and cloud-specific addons, is not in scope.

Instead, we expect higher-level and more tailored tooling to be built on top of kubeadm, and ideally, using kubeadm as the basis of all deployments will make it easier to create conformant clusters.

## How to install

To install kubeadm, see the [installation guide](/docs/setup/production-environment/tools/kubeadm/install-kubeadm).

## {{% heading "whatsnext" %}}

* [kubeadm init](/docs/reference/setup-tools/kubeadm/kubeadm-init) to bootstrap a Kubernetes control-plane node
* [kubeadm join](/docs/reference/setup-tools/kubeadm/kubeadm-join) to bootstrap a Kubernetes worker node and join it to the cluster
* [kubeadm upgrade](/docs/reference/setup-tools/kubeadm/kubeadm-upgrade) to upgrade a Kubernetes cluster to a newer version
* [kubeadm config](/docs/reference/setup-tools/kubeadm/kubeadm-config) if you initialized your cluster using kubeadm v1.7.x or lower, to configure your cluster for `kubeadm upgrade`
* [kubeadm token](/docs/reference/setup-tools/kubeadm/kubeadm-token) to manage tokens for `kubeadm join`
* [kubeadm reset](/docs/reference/setup-tools/kubeadm/kubeadm-reset) to revert any changes made to this host by `kubeadm init` or `kubeadm join`
* [kubeadm certs](/docs/reference/setup-tools/kubeadm/kubeadm-certs) to manage Kubernetes certificates
* [kubeadm kubeconfig](/docs/reference/setup-tools/kubeadm/kubeadm-kubeconfig) to manage kubeconfig files
* [kubeadm version](/docs/reference/setup-tools/kubeadm/kubeadm-version) to print the kubeadm version
* [kubeadm alpha](/docs/reference/setup-tools/kubeadm/kubeadm-alpha) to preview a set of features made available for gathering feedback from the community
