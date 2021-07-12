---
title: Controller
id: controller
date: 2018-04-12
full_link: /docs/concepts/architecture/controller/
short_description: >
  クラスターの状態をAPIサーバーから取得、見張る制御ループで、現在の状態を望ましい状態に移行するように更新します。

aka: 
tags:
- architecture
- fundamental
---
Kubernetesにおいて、コントローラーは{{< glossary_tooltip term_id="cluster" text="クラスター" >}}の状態を監視し、必要に応じて変更を加えたり要求したりする制御ループです。それぞれのコントローラーは現在のクラスターの状態を望ましい状態に近づけるように動作します。

<!--more--> 

コントローラーはクラスターの状態を{{< glossary_tooltip term_id="control-plane" text="コントロールプレーン" >}}の一部である{{< glossary_tooltip text="kube-apiserver" term_id="kube-apiserver" >}}から取得します。

コントロールプレーン内部で動くいくつかのコントローラーは、Kubernetesの主要な操作に対する制御ループを提供します。
例えば、Deploymentコントローラー、Daemonsetコントローラー、Namespaceコントローラー、Persistent Volumeコントローラー等は{{< glossary_tooltip term_id="kube-controller-manager" text="kube-controller-manager" >}}の内部で動作します。
