---
title: kube-proxy
id: kube-proxy
date: 2018-04-12
full_link: /docs/reference/command-line-tools-reference/kube-proxy/
short_description: >
  `kube-proxy`はクラスター内の各Nodeで動作しているネットワークプロキシです。

aka:
tags:
- fundamental
- networking
---
  kube-proxyはクラスター内の各{{< glossary_tooltip text="node" term_id="node" >}}で動作しているネットワークプロキシで、Kubernetesの{{< glossary_tooltip term_id="service">}}コンセプトの一部を実装しています。

<!--more-->

[kube-proxy](/docs/reference/command-line-tools-reference/kube-proxy/)は、Nodeのネットワークルールをメンテナンスします。これらのネットワークルールにより、クラスターの内部または外部のネットワークセッションからPodへのネットワーク通信が可能になります。

kube-proxyは、オペレーティングシステムにパケットフィルタリング層があり、かつ使用可能な場合、パケットフィルタリング層を使用します。それ以外の場合は自身でトラフィックを転送します。
