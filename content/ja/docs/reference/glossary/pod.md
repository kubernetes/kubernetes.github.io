---
title: Pod
id: pod
date: 2018-04-12
full_link: /ja/docs/concepts/workloads/pods/pod-overview/
short_description: >
  一番小さく一番シンプルな Kubernetes のオブジェクト。Pod とはクラスターで動作しているいくつかのコンテナのまとまりです。

aka: 
tags:
- core-object
- fundamental
---
  一番小さく一番シンプルなKubernetesのオブジェクト。Podとはクラスターで動作しているいくつかの{{< glossary_tooltip text="コンテナ" term_id="container" >}}のまとまりです。

<!--more--> 

通常、Pod は一つの主コンテナを実行するように設定されます。ロギングなどの補足機能を付加する、取り外し可能なサイドカーコンテナを実行することもできます。Pod は通常 {{< glossary_tooltip term_id="deployment" >}} によって管理されます。

