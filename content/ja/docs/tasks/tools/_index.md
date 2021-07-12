---
title: "ツールのインストール"
description: Kubernetesのツールをローカルのコンピュータ上にセットアップします。
weight: 10
no_list: true
---

## kubectl

Kubernetesのコマンドラインツール`kubectl`を使用すると、Kubernetesクラスターに対してコマンドを実行できるようになります。kubectlは、アプリケーションのデプロイ、クラスターリソースの調査と管理、ログの表示などに使用できます。

`kubectl`のダウンロードとインストールを行い、クラスターへのアクセスをセットアップする方法については、[kubectlのインストールおよびセットアップ](/ja/docs/tasks/tools/install-kubectl/)を参照してください。

また、[`kubectl`リファレンスドキュメント](/ja/docs/reference/kubectl/)も参照できます。

## Minikube

[Minikube](https://minikube.sigs.k8s.io/)は、Kubernetesをローカルで実行するツールです。MinikubeはシングルノードのKubernetesクラスターをパーソナルコンピューター上(Windows、macOS、Linux PCを含む)で実行することで、Kubernetesを試したり、日常的な開発作業のために利用できます。

ツールのインストールについて知りたい場合は、公式の[Get Started!](https://minikube.sigs.k8s.io/docs/start/)のガイドに従ってください。

Minikubeが起動したら、[サンプルアプリケーションの実行](/ja/docs/tutorials/hello-minikube/)を試すことができます。

## kind

Minikubeと同じように、[kind](https://kind.sigs.k8s.io/docs/)もローカルコンピューター上でKubernetesを実行するツールです。Minikubeとは違い、kindは1種類のコンテナランタイム上でしか動作しません。実行には[Docker](https://docs.docker.com/get-docker/)のインストールと設定が必要です。

[Quick Start](https://kind.sigs.k8s.io/docs/user/quick-start/)に、kindの起動に必要な手順が説明されています。
