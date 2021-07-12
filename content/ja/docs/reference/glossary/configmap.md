---
title: ConfigMap
id: configmap
date: 2018-04-12
full_link: /ja/docs/concepts/configuration/configmap/
short_description: >
  機密性のないデータをキーと値のペアで保存するために使用されるAPIオブジェクトです。環境変数、コマンドライン引数、またはボリューム内の設定ファイルとして使用できます。
aka:
tags:
- core-object
---

 機密性のないデータをキーと値のペアで保存するために使用されるAPIオブジェクトです。{{< glossary_tooltip text="Pod" term_id="pod" >}}は、環境変数、コマンドライン引数、または{{< glossary_tooltip text="ボリューム" term_id="volume" >}}内の設定ファイルとしてConfigMapを使用できます。

<!--more-->

ConfigMapを使用すると、環境固有の設定を{{< glossary_tooltip text="コンテナイメージ" term_id="image" >}}から分離できるため、アプリケーションを簡単に移植できるようになります。
