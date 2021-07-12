---
title: クラウドコントローラーマネージャー
id: cloud-controller-manager
date: 2018-04-12
full_link: /ja/docs/concepts/architecture/cloud-controller/
short_description: >
  サードパーティクラウドプロバイダーにKubernetewを結合するコントロールプレーンコンポーネント
aka: 
tags:
- core-object
- architecture
- operation
---
 クラウド特有の制御ロジックを組み込むKubernetesの{{< glossary_tooltip text="control plane" term_id="control-plane" >}}コンポーネントです。クラウドコントロールマネージャーは、クラスターをクラウドプロバイダーAPIをリンクし、クラスタのみで相互作用するコンポーネントからクラウドプラットフォームで相互作用するコンポーネントを分離します。

<!--more-->

Kubernetesと下のクラウドインフラストラクチャー間の相互運用ロジックを分離することで、cloud-controller-managerコンポーネントはクラウドプロバイダを主なKubernetesプロジェクトと比較し異なるペースで機能をリリース可能にします。
