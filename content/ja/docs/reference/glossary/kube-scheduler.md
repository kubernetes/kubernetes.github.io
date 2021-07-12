---
title: kube-scheduler
id: kube-scheduler
date: 2018-04-12
full_link: /docs/reference/generated/kube-scheduler/
short_description: >
  コントロールプレーン上で動作するコンポーネントで、新しく作られたPodにノードが割り当てられているか監視し、割り当てられていなかった場合にそのPodを実行するノードを選択します。

aka: 
tags:
- architecture
---
  コントロールプレーン上で動作するコンポーネントで、新しく作られた{{< glossary_tooltip term_id="pod" text="Pod" >}}に{{< glossary_tooltip term_id="node" text="ノード" >}}が割り当てられているか監視し、割り当てられていなかった場合にそのPodを実行するノードを選択します。

<!--more--> 

スケジューリングの決定は、PodあるいはPod群のリソース要求量、ハードウェア/ソフトウェア/ポリシーによる制約、アフィニティおよびアンチアフィニティの指定、データの局所性、ワークロード間の干渉、有効期限などを考慮して行われます。
