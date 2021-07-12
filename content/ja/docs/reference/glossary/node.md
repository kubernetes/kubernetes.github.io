---
title: ノード
id: node
date: 2018-04-12
full_link: /ja/docs/concepts/architecture/nodes/
short_description: >
  ノードはKubernetesのワーカーマシンです。

aka: 
tags:
- fundamental
---
 ノードはKubernetesのワーカーマシンです。

<!--more--> 

ワーカーノードは、クラスターに応じてVMまたは物理マシンの場合があります。{{< glossary_tooltip text="Pod" term_id="pod" >}}の実行に必要なローカルデーモンまたはサービスがあり、コントロールプレーンによって管理されます。ノード上のデーモンには、{{< glossary_tooltip text="kubelet" term_id="kubelet" >}}、{{< glossary_tooltip text="kube-proxy" term_id="kube-proxy" >}}、および{{< glossary_tooltip term_id="docker" >}}などの{{< glossary_tooltip text="CRI" term_id="cri" >}}を実装するコンテナランタイムが含まれます。
Kubernetesの初期バージョンでは、ノードは"Minion"と呼ばれていました。
