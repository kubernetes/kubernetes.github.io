---
title: オペレーターパターン
content_type: concept
weight: 30
---

<!-- overview -->

オペレーターは[カスタムリソース](/ja/docs/concepts/extend-kubernetes/api-extension/custom-resources/)を使用するKubernetesへのソフトウェア拡張です。
オペレーターは、特に[制御ループ](/ja/docs/concepts/#kubernetes-control-plane)のようなKubernetesが持つ仕組みに準拠しています。



<!-- body -->

## モチベーション

オペレーターパターンはサービス、またはサービス群を管理している運用担当者の主な目的をキャプチャすることが目標です。
特定のアプリケーション、サービスの面倒を見ている運用担当者は、システムがどのように振る舞うべきか、どのようにデプロイをするか、何らかの問題があったときにどのように対応するかについて深い知識を持っています。

Kubernetes上でワークロードを稼働させている人は、しばしば繰り返し可能なタスクを自動化することを好みます。
オペレーターパターンは、Kubernetes自身が提供している機能を超えて、あなたがタスクを自動化するために、どのようにコードを書くかをキャプチャします。

## Kubernetesにおけるオペレーター

Kubernetesは自動化のために設計されています。追加の作業、設定無しに、Kubernetesのコア機能によって多数のビルトインされた自動化機能が提供されます。
ワークロードのデプロイおよび稼働を自動化するためにKubernetesを使うことができます。 *さらに* Kubernetesがそれをどのように行うかの自動化も可能です。

Kubernetesの{{< glossary_tooltip text="コントローラー" term_id="controller" >}}コンセプトは、Kubernetesのソースコードを修正すること無く、クラスターの振る舞いを拡張することを可能にします。
オペレーターはKubernetes APIのクライアントで、[Custom Resource](/docs/concepts/extend-kubernetes/api-extension/custom-resources/)にとっての、コントローラーのように振る舞います。

## オペレーターの例 {#example}

オペレーターを使い自動化できるいくつかのことは、下記のようなものがあります:

* 必要に応じてアプリケーションをデプロイする
* アプリケーションの状態のバックアップを取得、リストアする
* アプリケーションコードの更新と同時に、例えばデータベーススキーマ、追加の設定修正など必要な変更の対応を行う
* Kubernetes APIをサポートしていないアプリケーションに、サービスを公開してそれらを発見する
* クラスターの回復力をテストするために、全て、または一部分の障害をシミュレートする
* 内部のリーダー選出プロセス無しに、分散アプリケーションのリーダーを選択する

オペレーターをもっと詳しく見るとどのように見えるでしょうか？より詳細な例を示します:

1. クラスターに設定可能なSampleDBという名前のカスタムリソース
2. オペレーターの、コントローラー部分を含むPodが実行されていることを保証するDeployment
3. オペレーターのコードを含んだコンテナイメージ
4. 設定されているSampleDBのリソースを見つけるために、コントロールプレーンに問い合わせるコントローラーのコード
5. オペレーターのコアは、現実を、設定されているリソースにどのように合わせるかをAPIサーバーに伝えるコードです。
   * もし新しいSampleDBを追加した場合、オペレーターは永続化データベースストレージを提供するためにPersistentVolumeClaimsをセットアップし、StatefulSetがSampleDBの起動と、初期設定を担うJobを走らせます
   * もしそれを削除した場合、オペレーターはスナップショットを取り、StatefulSetとVolumeも合わせて削除されたことを確認します
6. オペレーターは定期的なデータベースのバックアップも管理します。それぞれのSampleDBリソースについて、オペレーターはデータベースに接続可能な、バックアップを取得するPodをいつ作成するかを決定します。これらのPodはデータベース接続の詳細情報、クレデンシャルを保持するConfigMapとSecret、もしくはどちらかに依存するでしょう。
7. オペレーターは、管理下のリソースの堅牢な自動化を提供することを目的としているため、補助的な追加コードが必要になるかもしれません。この例では、データベースが古いバージョンで動いているかどうかを確認するコードで、その場合、アップグレードを行うJobをあなたに代わり作成します。

## オペレーターのデプロイ

オペレーターをデプロイする最も一般的な方法は、Custom Resource Definitionとそれに関連するコントローラーをクラスターに追加することです。
このコントローラーは通常、あなたがコンテナアプリケーションを動かすのと同じように、{{< glossary_tooltip text="コントロールプレーン" term_id="control-plane" >}}外で動作します。

例えば、コントローラーをDeploymentとしてクラスター内で動かすことができます。

## オペレーターを利用する {#using-operators}

一度オペレーターをデプロイすると、そのオペレーターを使って、それ自身が使うリソースの種類を追加、変更、または削除できます。
上記の利用例に従ってオペレーターそのもののためのDeploymentをセットアップし、以下のようなコマンドを実行します:

```shell
kubectl get SampleDB                   # 設定したデータベースを発見します

kubectl edit SampleDB/example-database # 手動でいくつかの設定を変更します
```

これだけです！オペレーターが変更の適用だけでなく既存のサービスがうまく稼働し続けるように面倒を見てくれます。

## 自分でオペレーターを書く {#writing-operator}

必要な振る舞いを実装したオペレーターがエコシステム内に無い場合、自分で作成することができます。
[次の項目](#whats-next)で、自分でクラウドネイティブオペレーターを作るときに利用できるライブラリやツールのリンクを見つけることができます。

オペレーター（すなわち、コントローラー）はどの言語/ランタイムでも実装でき、[Kubernetes APIのクライアント](/docs/reference/using-api/client-libraries/)として機能させることができます。



## {{% heading "whatsnext" %}}


* [Custom Resources](/ja/docs/concepts/extend-kubernetes/api-extension/custom-resources/)をより深く学びます
* ユースケースに合わせた、既製のオペレーターを[OperatorHub.io](https://operatorhub.io/)から見つけます
* 自前のオペレーターを書くために既存のツールを使います、例:
  * [KUDO](https://kudo.dev/)（Kubernetes Universal Declarative Operator）を使います
  * [kubebuilder](https://book.kubebuilder.io/)を使います
  * [Metacontroller](https://metacontroller.github.io/metacontroller/intro.html)を自分で実装したWebHooksと一緒に使います
  * [Operator Framework](https://operatorframework.io)を使います
* 自前のオペレーターを他のユーザーのために[公開](https://operatorhub.io/)します
* オペレーターパターンを紹介している[CoreOSオリジナル記事](https://coreos.com/blog/introducing-operators.html)を読みます
* Google Cloudが出したオペレーター作成のベストプラクティス[記事](https://cloud.google.com/blog/products/containers-kubernetes/best-practices-for-building-kubernetes-operators-and-stateful-apps)を読みます

