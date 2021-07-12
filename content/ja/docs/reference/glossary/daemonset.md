---
title: DaemonSet
id: daemonset
date: 2018-04-12
full_link: /docs/concepts/workloads/controllers/daemonset
short_description: >
  Podのコピーがクラスター内の一連のNodeに渡って実行されることを保証します。

aka: 
tags:
- fundamental
- core-object
- workload
---
  {{< glossary_tooltip text="Pod" term_id="pod" >}}のコピーが{{< glossary_tooltip text="クラスター" term_id="cluster" >}}内の一連のNodeに渡って実行されることを保証します。

<!--more--> 

通常{{< glossary_tooltip term_id="node" >}}で実行する必要があるログコレクターや監視エージェントなどのシステムデーモンをデプロイするために使用します。

