---
title: "Kubeadm"
weight: 10
no_list: true
content_type: concept
card:
  name: reference
  weight: 40
---

<img src="https://raw.githubusercontent.com/kubernetes/kubeadm/master/logos/stacked/color/kubeadm-stacked-color.png" align="right" width="150px">kubeadmは、`kubeadm init`や`kubeadm join`などのコマンドを提供するツールで、Kubernetesクラスターを構築する上でのベストプラクティスを反映した「近道」を提供するものとして開発されました。

kubeadmは実用最小限のクラスターをセットアップするための処理を実行します。設計上、kubeadmはブートストラップのみを行い、マシンのプロビジョニングは行いません。同様に、Kubernetesダッシュボード、モニタリングソリューション、クラウド向けのアドオンなど、あれば便利でもなくても支障のない各種アドオンのインストールも範囲外です。

その代わりに、高度な特定用途向けのツールはkubeadmをベースに構築されることが期待されています。理想的には、すべてのデプロイのベースとしてkubeadmを使用することで、適合テストに通るクラスターを簡単に作れるようになります。

## インストール方法

kubeadmをインストールするには、[インストールガイド](/ja/docs/setup/production-environment/tools/kubeadm/install-kubeadm)を参照してください。

## {{% heading "whatsnext" %}}

* [kubeadm init](/docs/reference/setup-tools/kubeadm/kubeadm-init)を使用して、Kubernetesのコントロールプレーンノードをブートストラップする
* [kubeadm join](/docs/reference/setup-tools/kubeadm/kubeadm-join)を使用して、Kubernetesのワーカーノードをブートストラップし、クラスターに参加させる
* [kubeadm upgrade](/docs/reference/setup-tools/kubeadm/kubeadm-upgrade)で、Kubernetesクラスターを新しいバージョンにアップグレードする
* [kubeadm config](/docs/reference/setup-tools/kubeadm/kubeadm-config)を使用して、kubeadm v1.7.x以前で初期化されたクラスターを、`kubeadm upgrade`を利用できるように設定する
* [kubeadm token](/docs/reference/setup-tools/kubeadm/kubeadm-token)で、`kubeadm join`のためのトークンを管理する
* [kubeadm reset](/docs/reference/setup-tools/kubeadm/kubeadm-reset)を使用して、`kubeadm init`または`kubeadm join`でホストに行われた変更を元に戻す
* [kubeadm version](/docs/reference/setup-tools/kubeadm/kubeadm-version)で、kubeadmのバージョンを表示する
* [kubeadm alpha](/docs/reference/setup-tools/kubeadm/kubeadm-alpha)で、コミュニティからのフィードバックを集めるために有効にされた各種機能を試用する
