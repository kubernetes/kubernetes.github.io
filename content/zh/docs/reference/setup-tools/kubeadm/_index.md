---
title: "Kubeadm"
weight: 10
no_list: true
content_type: concept
card:
  name: reference
  weight: 40
---

<img src="https://raw.githubusercontent.com/kubernetes/kubeadm/master/logos/stacked/color/kubeadm-stacked-color.png" align="right" width="150px">

<!-- 
Kubeadm is a tool built to provide `kubeadm init` and `kubeadm join` as best-practice "fast paths" for creating Kubernetes clusters.
 -->
Kubeadm 是一个提供了 `kubeadm init` 和 `kubeadm join` 的工具，
作为创建 Kubernetes 集群的 “快捷途径” 的最佳实践。

<!-- 
kubeadm performs the actions necessary to get a minimum viable cluster up and running. By design, it cares only about bootstrapping,
not about provisioning machines. Likewise, installing various nice-to-have addons, like the Kubernetes Dashboard, monitoring solutions, and cloud-specific addons, is not in scope.
 -->
kubeadm 通过执行必要的操作来启动和运行最小可用集群。
按照设计，它只关注启动引导，而非配置机器。同样的，
安装各种 “锦上添花” 的扩展，例如 Kubernetes Dashboard、
监控方案、以及特定云平台的扩展，都不在讨论范围内。

<!-- 
Instead, we expect higher-level and more tailored tooling to be built on top of kubeadm, and ideally, using kubeadm as the basis of all deployments will make it easier to create conformant clusters.
 -->
相反，我们希望在 kubeadm 之上构建更高级别以及更加合规的工具，
理想情况下，使用 kubeadm 作为所有部署工作的基准将会更加易于创建一致性集群。

<!-- 
## How to install
 -->
## 如何安装

<!-- 
To install kubeadm, see the [installation guide](/docs/setup/production-environment/tools/kubeadm/install-kubeadm).
-->
要安装 kubeadm, 请查阅
[安装指南](/zh/docs/setup/production-environment/tools/kubeadm/install-kubeadm/).

## {{% heading "whatsnext" %}}

<!-- 
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
 -->
* [kubeadm init](/zh/docs/reference/setup-tools/kubeadm/kubeadm-init)
  用于搭建控制平面节点
* [kubeadm join](/zh/docs/reference/setup-tools/kubeadm/kubeadm-join)
  用于搭建工作节点并将其加入到集群中
* [kubeadm upgrade](/zh/docs/reference/setup-tools/kubeadm/kubeadm-upgrade)
  用于升级 Kubernetes 集群到新版本
* [kubeadm config](/zh/docs/reference/setup-tools/kubeadm/kubeadm-config)
  如果你使用了 v1.7.x 或更低版本的 kubeadm 版本初始化你的集群，则使用
  `kubeadm upgrade` 来配置你的集群
* [kubeadm token](/zh/docs/reference/setup-tools/kubeadm/kubeadm-token)
  用于管理 `kubeadm join` 使用的令牌
* [kubeadm reset](/zh/docs/reference/setup-tools/kubeadm/kubeadm-reset)
  用于恢复通过 `kubeadm init` 或者 `kubeadm join` 命令对节点进行的任何变更
* [kubeadm certs](/zh/docs/reference/setup-tools/kubeadm/kubeadm-certs)
  用于管理 Kubernetes 证书
* [kubeadm kubeconfig](/docs/reference/setup-tools/kubeadm/kubeadm-kubeconfig)
  用于管理 kubeconfig 文件
* [kubeadm version](/zh/docs/reference/setup-tools/kubeadm/kubeadm-version)
  用于打印 kubeadm 的版本信息
* [kubeadm alpha](/zh/docs/reference/setup-tools/kubeadm/kubeadm-alpha)
  用于预览一组可用于收集社区反馈的特性

