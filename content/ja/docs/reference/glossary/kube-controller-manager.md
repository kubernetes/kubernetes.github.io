---
title: kube-controller-manager
id: kube-controller-manager
date: 2018-04-12
full_link: /docs/reference/command-line-tools-reference/kube-controller-manager/
short_description: >
  コントロールプレーン上で動作するコンポーネントで、複数のコントローラープロセスを実行します。

aka: 
tags:
- architecture
- fundamental
---
 コントロールプレーン上で動作するコンポーネントで、複数の{{< glossary_tooltip text="コントローラー" term_id="controller" >}}プロセスを実行します。

<!--more--> 

論理的には、各{{< glossary_tooltip text="コントローラー" term_id="controller" >}}は個別のプロセスですが、複雑さを減らすために一つの実行ファイルにまとめてコンパイルされ、単一のプロセスとして動きます。
