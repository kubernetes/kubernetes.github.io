---
title: 其他工具
content_type: concept
weight: 80
no_list: true
---

<!-- 
title: Other Tools
reviewers:
- janetkuo
content_type: concept
weight: 80
no_list: true
-->

<!-- overview -->
<!-- 
Kubernetes contains several built-in tools to help you work with the Kubernetes system.
-->
Kubernetes 包含多个内置工具来帮助你使用 Kubernetes 系统。


<!-- body -->

<!--  
## Minikube

[`minikube`](https://minikube.sigs.k8s.io/docs/) is a tool that
runs a single-node Kubernetes cluster locally on your workstation for
development and testing purposes.
-->
## Minikube

[`minikube`](https://minikube.sigs.k8s.io/docs/)
是一种在你的工作站上本地运行单节点 Kubernetes 集群的工具，用于开发和测试。

<!-- 
## Dashboard

[`Dashboard`](/docs/tasks/access-application-cluster/web-ui-dashboard/), the web-based user interface of Kubernetes, allows you to deploy containerized applications
to a Kubernetes cluster, troubleshoot them, and manage the cluster and its resources itself.
-->
## 仪表盘

[`Dashboard`](/zh/docs/tasks/access-application-cluster/web-ui-dashboard/)，
基于 Web 的 Kubernetes 用户界面，
允许你将容器化的应用程序部署到 Kubernetes 集群，
对它们进行故障排查，并管理集群及其资源本身。

<!-- 
## Helm

[`Kubernetes Helm`](https://github.com/kubernetes/helm) is a tool for managing packages of pre-configured
Kubernetes resources, aka Kubernetes charts.
-->
## Helm

[`Kubernetes Helm`](https://github.com/kubernetes/helm)
是一个用于管理预配置 Kubernetes 资源包的工具，也就是 Kubernetes 图表。

<!-- 
Use Helm to:

* Find and use popular software packaged as Kubernetes charts
* Share your own applications as Kubernetes charts
* Create reproducible builds of your Kubernetes applications
* Intelligently manage your Kubernetes manifest files
* Manage releases of Helm packages
-->
使用 Helm 来：

* 查找和使用打包为 Kubernetes 图表的流行软件
* 将你自己的应用程序共享为 Kubernetes 图表
* 为你的 Kubernetes 应用程序创建可重现的构建
* 智能管理你的 Kubernetes 清单文件
* 管理 Helm 包的发布

<!-- 
## Kompose

[`Kompose`](https://github.com/kubernetes/kompose) is a tool to help Docker Compose users move to Kubernetes.
-->
## Kompose

[`Kompose`](https://github.com/kubernetes/kompose)
是一个帮助 Docker Compose 用户迁移到 Kubernetes 的工具。

<!-- 
Use Kompose to:

* Translate a Docker Compose file into Kubernetes objects
* Go from local Docker development to managing your application via Kubernetes
* Convert v1 or v2 Docker Compose `yaml` files or [Distributed Application Bundles](https://docs.docker.com/compose/bundles/)
-->

使用 Kompose：

* 将 Docker Compose 文件翻译成 Kubernetes 对象
* 从本地 Docker 开发转到通过 Kubernetes 管理你的应用程序
* 转换 Docker Compose v1 或 v2 版本的 `yaml` 文件或[分布式应用程序包](https://docs.docker.com/compose/bundles/)