---
title: Podの概観
content_type: concept
weight: 10
card:
  name: concepts
  weight: 60
---

<!-- overview -->
このページでは、Kubernetesのオブジェクトモデルにおいて、デプロイ可能な最小単位のオブジェクトである`Pod`に関して説明します。


<!-- body -->
## Podについて理解する {#understanding-pods}

*Pod* は、Kubernetesアプリケーションの基本的な実行単位です。これは、作成またはデプロイするKubernetesオブジェクトモデルの中で最小かつ最も単純な単位です。Podは、{{< glossary_tooltip term_id="cluster" >}}で実行されているプロセスを表します。

Podは、アプリケーションのコンテナ(いくつかの場合においては複数のコンテナ)、ストレージリソース、ユニークなネットワークIP、およびコンテナの実行方法を管理するオプションをカプセル化します。Podはデプロイメントの単位、すなわち*Kubernetesのアプリケーションの単一インスタンス* で、単一の{{< glossary_tooltip term_id="container" >}}または密結合なリソースを共有する少数のコンテナで構成される場合があります。

[Docker](https://www.docker.com)はKubernetesのPod内で使われる最も一般的なコンテナランタイムですが、Podは他の[コンテナランタイム](/ja/docs/setup/production-environment/container-runtimes/)も同様にサポートしています。

Kubernetesクラスター内でのPodは2つの主な方法で使うことができます。

* **単一のコンテナを稼働させるPod** : いわゆる*「1Pod1コンテナ」* 構成のモデルは、最も一般的なKubernetesのユースケースです。
このケースでは、ユーザーはPodを単一のコンテナのラッパーとして考えることができ、Kubernetesはコンテナを直接扱うというよりは、Podを管理することになります。
* **協調して稼働させる必要がある複数のコンテナを稼働させるPod** : 単一のPodは、リソースを共有する必要があるような、密接に連携した複数の同じ環境にあるコンテナからなるアプリケーションをカプセル化することもできます。  これらの同じ環境にあるコンテナ群は、サービスの結合力の強いユニットを構成することができます。
-- 1つのコンテナが、共有されたボリュームからファイルをパブリックな場所に送信し、一方では分割された*サイドカー* コンテナがそれらのファイルを更新します。そのPodはそれらのコンテナとストレージリソースを、単一の管理可能なエンティティとしてまとめます。

[Kubernetes Blog](https://kubernetes.io/blog)にて、Podのユースケースに関するいくつかの追加情報を見ることができます。さらなる情報を得たい場合は、下記のページを参照ください。

  * [The Distributed System Toolkit: Patterns for Composite Containers](https://kubernetes.io/blog/2015/06/the-distributed-system-toolkit-patterns)
  * [Container Design Patterns](https://kubernetes.io/blog/2016/06/container-design-patterns)

各Podは、与えられたアプリケーションの単一のインスタンスを稼働するためのものです。もしユーザーのアプリケーションを水平にスケールさせたい場合(例: 複数インスタンスを稼働させる)、複数のPodを使うべきです。1つのPodは各インスタンスに対応しています。
Kubernetesにおいて、これは一般的に _レプリケーション_ と呼ばれます。
レプリケーションされたPodは、通常コントローラーと呼ばれる抽象概念によって単一のグループとして作成、管理されます。
さらなる情報に関しては[Podとコントローラー](#pods-and-controllers)を参照して下さい。

### Podがどのように複数のコンテナを管理しているか

Podは凝集性の高いサービスのユニットを構成するような複数の協調プロセス(コンテナ）をサポートするためにデザインされました。
単一のPod内のコンテナ群は、クラスター内において同一の物理マシンもしくは仮想マシン上において自動で同じ環境に配備され、スケジュールされます。コンテナはリソースや依存関係を共有し、お互いにコミュニケートし、それらがいつ、どのように削除されるかを調整できます。

注意点として、単一のPod内で同じ環境に配備され、同時管理される複数のコンテナをグルーピングするのは、比較的に発展的なユースケースとなります。
ユーザーは、コンテナ群が密接に連携するような、特定のインスタンスにおいてのみこのパターンを使用するべきです。
例えば、ユーザーが共有ボリューム内にあるファイル用のWebサーバとして稼働するコンテナと、下記のダイアグラムにあるような、リモートのソースからファイルを更新するような分離された*サイドカー* コンテナを持っているような場合です。

{{< figure src="/images/docs/pod.svg" alt="Podのダイアグラム" width="50%" >}}

Podは、Podによって構成されたコンテナ群のために2種類の共有リソースを提供します。 *ネットワーキング* と*ストレージ* です。

#### ネットワーキング

各Podは固有のIPアドレスを割り当てられます。単一のPod内の各コンテナは、IPアドレスやネットワークポートを含む、そのネットワークの名前空間を共有します。*Pod内の* コンテナは`localhost`を使用してお互いに疎通できます。単一のPod内のコンテナが*Pod外* のエンティティと疎通する場合、共有されたネットワークリソース(ポートなど）をどのように使うかに関して調整しなければなりません。

#### ストレージ

単一のPodは共有されたストレージ{{< glossary_tooltip term_id="volume" >}}のセットを指定できます。Pod内の全てのコンテナは、その共有されたボリュームにアクセスでき、コンテナ間でデータを共有することを可能にします。ボリュームもまた、もしPod内のコンテナの1つが再起動が必要になった場合に備えて、データを永続化できます。
単一のPod内での共有ストレージをKubernetesがどう実装しているかについてのさらなる情報については、[Volumes](/docs/concepts/storage/volumes/)を参照してください。

## Podを利用する

ユーザーはまれに、Kubernetes内で独立したPodを直接作成する場合があります(シングルトンPodなど)。
これはPodが比較的、一時的な使い捨てエンティティとしてデザインされているためです。Podが作成された時(ユーザーによって直接的、またはコントローラーによって間接的に作成された場合)、ユーザーのクラスター内の単一の{{< glossary_tooltip term_id="node" >}}上で稼働するようにスケジューリングされます。そのPodはプロセスが停止されたり、Podオブジェクトが削除されたり、Podがリソースの欠如のために*追い出され* たり、ノードが故障するまでノード上に残り続けます。

{{< note >}}
単一のPod内でのコンテナを再起動することと、そのPodを再起動することを混同しないでください。Podはそれ自体は実行されませんが、コンテナが実行される環境であり、削除されるまで存在し続けます。
{{< /note >}}

Podは、Podそれ自体によって自己修復しません。もし、稼働されていないノード上にPodがスケジュールされた場合や、スケジューリング操作自体が失敗した場合、Podが削除されます。同様に、Podはリソースの欠如や、ノードのメンテナンスによる追い出しがあった場合はそこで停止します。Kubernetesは*コントローラー* と呼ばれる高レベルの抽象概念を使用し、それは比較的使い捨て可能なPodインスタンスの管理を行います。
このように、Podを直接使うのは可能ですが、コントローラーを使用したPodを管理する方がより一般的です。KubernetesがPodのスケーリングと修復機能を実現するためにコントローラーをどのように使うかに関する情報は[Podとコントローラー](#pods-and-controllers)を参照してください。

### Podとコントローラー

単一のコントローラーは、ユーザーのために複数のPodを作成・管理し、レプリケーションやロールアウト、クラスターのスコープ内で自己修復の機能をハンドリングします。例えば、もしノードが故障した場合、コントローラーは異なるノード上にPodを置き換えるようにスケジューリングすることで、自動的にリプレース可能となります。

1つまたはそれ以上のPodを含むコントローラーの例は下記の通りです。

* [Deployment](/ja/docs/concepts/workloads/controllers/deployment/)
* [StatefulSet](/ja/docs/concepts/workloads/controllers/statefulset/)
* [DaemonSet](/ja/docs/concepts/workloads/controllers/daemonset/)

通常は、コントローラーはユーザーが作成したPodテンプレートを使用して、担当するPodを作成します。

## Podテンプレート

Podテンプレートは、[ReplicationController](/docs/concepts/workloads/controllers/replicationcontroller/)、 [Job](/docs/concepts/jobs/run-to-completion-finite-workloads/)や、
[DaemonSet](/ja/docs/concepts/workloads/controllers/daemonset/)のような他のオブジェクト内で含まれるPodの仕様となります。
コントローラーは実際のPodを作成するためにPodテンプレートを使用します。
下記のサンプルは、メッセージを表示する単一のコンテナを含んだ、シンプルなPodのマニフェストとなります。

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
  labels:
    app: myapp
spec:
  containers:
  - name: myapp-container
    image: busybox
    command: ['sh', '-c', 'echo Hello Kubernetes! && sleep 3600']
```

全てのレプリカの現在の理想的な状態を指定するというよりも、Podテンプレートはクッキーの抜き型のようなものです。一度クッキーがカットされると、そのクッキーは抜き型から離れて関係が無くなります。そこにはいわゆる”量子もつれ”といったものはありません。テンプレートに対するその後の変更や新しいテンプレートへの切り替えは、すでに作成されたPod上には直接的な影響はありません。
同様に、ReplicationControllerによって作成されたPodは、変更後に直接更新されます。これはPodとの意図的な違いとなり、そのPodに属する全てのコンテナの現在の理想的な状態を指定します。このアプローチは根本的にシステムのセマンティクスを単純化し、機能の柔軟性を高めます。



## {{% heading "whatsnext" %}}

* [Pod](/ja/docs/concepts/workloads/pods/pod/)についてさらに学びましょう
* Podの振る舞いに関して学ぶには下記を参照してください
   * [Podの停止](/ja/docs/concepts/workloads/pods/pod/#termination-of-pods)
   * [Podのライフサイクル](/ja/docs/concepts/workloads/pods/pod-lifecycle/)

