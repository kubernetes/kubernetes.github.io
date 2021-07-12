---
title: Deployment
id: deployment
date: 2018-04-12
full_link: /ja/docs/concepts/workloads/controllers/deployment/
short_description: >
  クラスター上の複製されたアプリケーションを管理します。

aka: 
tags:
- fundamental
- core-object
- workload
---
 複製されたアプリケーションを管理するAPIオブジェクトで、通常はステートレスなPodを実行します。

<!--more--> 

各レプリカは{{< glossary_tooltip text="Pod" term_id="pod" >}}で表され、Podはクラスターの{{< glossary_tooltip text="ノード" term_id="node" >}}間で分散されます。
ローカル状態を要求するワークロードには、{{< glossary_tooltip term_id="StatefulSet" >}}の利用を考えてください。
