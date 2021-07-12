---
title: APIサーバー
id: kube-apiserver
date: 2018-04-12
full_link: /docs/concepts/overview/components/#kube-apiserver
short_description: >
  Kubernetes APIを提供するコントロールプレーンのコンポーネントです。

aka:
- kube-apiserver
tags:
- architecture
- fundamental
---
 APIサーバーは、Kubernetes APIを外部に提供するKubernetes{{< glossary_tooltip text="コントロールプレーン" term_id="control-plane" >}}のコンポーネントです。
 APIサーバーはKubernetesコントロールプレーンのフロントエンドになります。

<!--more-->

Kubernetes APIサーバーの主な実装は[kube-apiserver](/docs/reference/generated/kube-apiserver/)です。
kube-apiserverは水平方向にスケールするように設計されています&mdash;つまり、インスタンスを追加することでスケールが可能です。
複数のkube-apiserverインスタンスを実行することで、インスタンス間でトラフィックを分散させることが可能です。