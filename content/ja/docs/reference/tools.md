---
title: ツール
content_type: concept
---

<!-- overview -->
Kubernetesには、Kubernetesシステムの操作に役立ついくつかの組み込みツールが含まれています。

<!-- body -->
## Kubectl
[`kubectl`](/docs/tasks/tools/install-kubectl/)は、Kubernetesのためのコマンドラインツールです。このコマンドはKubernetes cluster managerを操作します。

## Kubeadm
[`kubeadm`](docs/setup/production-environment/tools/kubeadm/install-kubeadm/)は、物理サーバやクラウドサーバ、仮想マシン上にKubernetesクラスタを容易にプロビジョニングするためのコマンドラインツールです(現在はアルファ版です)。

## Minikube
[`minikube`](https://minikube.sigs.k8s.io/docs/)は、開発やテストのためにワークステーション上でシングルノードのKubernetesクラスタをローカルで実行するツールです。

## Dashboard
[`Dashboard`](/docs/tasks/access-application-cluster/web-ui-dashboard/)は、KubernetesのWebベースのユーザインタフェースで、コンテナ化されたアプリケーションをKubernetesクラスタにデプロイしたり、トラブルシューティングしたり、クラスタとそのリソース自体を管理したりすることが出来ます。

## Helm
[`Kubernetes Helm`](https://github.com/helm/helm)は、事前に設定されたKubernetesリソースのパッケージ、別名Kubernetes chartsを管理するためのツールです。

Helmを用いて以下のことを行います。

* Kubernetes chartsとしてパッケージ化された人気のあるソフトウェアの検索と利用

* Kubernetes chartsとして所有するアプリケーションを共有すること

* Kubernetesアプリケーションの再現性のあるビルドの作成

* Kubernetesマニフェストファイルを知的な方法で管理

* Helmパッケージのリリース管理

## Kompose
[`Kompose`](https://github.com/kubernetes/kompose)は、Docker ComposeユーザがKubernetesに移行する手助けをするツールです。

Komposeを用いて以下のことを行います。

* Docker ComposeファイルのKubernetesオブジェクトへの変換

* ローカルのDocker開発からKubernetesを経由したアプリケーション管理への移行

* v1またはv2のDocker Compose用 `yaml` ファイルならびに[分散されたアプリケーションバンドル](https://docs.docker.com/compose/bundles/)の変換
