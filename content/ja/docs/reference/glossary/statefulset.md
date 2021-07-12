---
title: StatefulSet
id: statefulset
date: 2018-04-12
full_link: /ja/docs/concepts/workloads/controllers/statefulset/
short_description: >
  StatefulSetはDeploymentとPodのセットのスケーリングを管理し、永続化ストレージと各Podの永続的な識別子を備えています。

aka: 
tags:
- fundamental
- core-object
- workload
- storage
---

StatefulSetはDeploymentと{{< glossary_tooltip text="Pod" term_id="pod" >}}のセットのスケーリングを管理し、それらのPodの*順序と一意性を保証* します。

<!--more--> 

{{< glossary_tooltip term_id="deployment" >}}のように、StatefulSetは指定したコンテナのspecに基づいてPodを管理します。Deploymentとは異なり、StatefulSetは各Podにおいて管理が大変な同一性を維持します。これらのPodは同一のspecから作成されますが、それらは交換可能ではなく、リスケジュール処理をまたいで維持される永続的な識別子を持ちます。

ワークロードに永続性を持たせるためにストレージボリュームを使いたい場合は、解決策の1つとしてStatefulSetが利用できます。StatefulSet内の個々のPodは障害の影響を受けやすいですが、永続化したPodの識別子は既存のボリュームと障害によって置換された新しいPodの紐付けを簡単にします。
