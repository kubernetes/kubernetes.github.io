---
title: "Pod"
content_type: concept
weight: 10
no_list: true
card:
  name: concepts
  weight: 60
---

*Pod*は、Kubernetes内で作成・管理できるコンピューティングの最小のデプロイ可能なユニットです(Podという名前は、たとえばクジラの群れ(pod of whales)やえんどう豆のさや(pea pod)などの表現と同じような意味です)。

*Pod*は、1つまたは複数の{{< glossary_tooltip text="コンテナ" term_id="container" >}}のグループであり、ストレージやネットワークの共有リソースを持ち、コンテナの実行方法に関する仕様を持っています。同じPodに含まれるリソースは、常に同じ場所で同時にスケジューリングされ、共有されたコンテキストの中で実行されます。Podはアプリケーションに特化した「論理的なホスト」をモデル化します。つまり、1つのPod内には、1つまたは複数の比較的密に結合されたアプリケーションコンテナが含まれます。クラウド外の文脈で説明すると、アプリケーションが同じ物理ホストや同じバーチャルマシンで実行されることが、クラウドアプリケーションの場合には同じ論理ホスト上で実行されることに相当します。

アプリケーションコンテナと同様に、Podでも、Podのスタートアップ時に実行される[initコンテナ](/ja/docs/concepts/workloads/pods/init-containers/)を含めることができます。また、クラスターで利用できる場合には、[エフェメラルコンテナ](/ja/docs/concepts/workloads/pods/ephemeral-containers/)を注入してデバッグすることもできます。

<!-- body -->

## Podとは何か？

{{< note >}}
KubernetesはDockerだけでなく複数の{{< glossary_tooltip text="コンテナランタイム" term_id="container-runtime" >}}をサポートしていますが、[Docker](https://www.docker.com/)が最も一般的に知られたランタイムであるため、Docker由来の用語を使ってPodを説明するのが理解の助けとなります。
{{< /note >}}

Podの共有コンテキストは、Dockerコンテナを隔離するのに使われているのと同じ、Linuxのnamespaces、cgroups、場合によっては他の隔離技術の集合を用いて作られます。Podのコンテキスト内では、各アプリケーションが追加の準隔離技術を適用することもあります。

Dockerの概念を使って説明すると、Podは共有の名前空間と共有ファイルシステムのボリュームを持つDockerコンテナのグループに似ています。

## Podを使用する

通常、たとえ単一のコンテナしか持たないシングルトンのPodだとしても、自分でPodを直接作成する必要はありません。その代わりに、{{< glossary_tooltip text="Deployment"
term_id="deployment" >}}や{{< glossary_tooltip text="Job" term_id="job" >}}などのワークロードリソースを使用してPodを作成します。もしPodが状態を保持する必要がある場合は、{{< glossary_tooltip text="StatefulSet" term_id="statefulset" >}}リソースを使用することを検討してください。

Kubernetesクラスター内のPodは、主に次の2種類の方法で使われます。

* **単一のコンテナを稼働させるPod**。「1Pod1コンテナ」構成のモデルは、Kubernetesでは最も一般的なユースケースです。このケースでは、ユーザーはPodを単一のコンテナのラッパーとして考えることができます。Kubernetesはコンテナを直接管理するのではなく、Podを管理します。
* **協調して稼働させる必要がある複数のコンテナを稼働させるPod**。単一のPodは、密に結合してリソースを共有する必要があるような、同じ場所で稼働する複数のコンテナからなるアプリケーションをカプセル化することもできます。これらの同じ場所で稼働するコンテナ群は、単一のまとまりのあるサービスのユニットを構成します。たとえば、1つのコンテナが共有ボリュームからファイルをパブリックに配信し、別の*サイドカー*コンテナがそれらのファイルを更新するという構成が考えられます。Podはこれらの複数のコンテナ、ストレージリソース、一時的なネットワークIDなどを、単一のユニットとしてまとめます。

  {{< note >}}
  複数のコンテナを同じ場所で同時に管理するように単一のPod内にグループ化するのは、比較的高度なユースケースです。このパターンを使用するのは、コンテナが密に結合しているような特定のインスタンス内でのみにするべきです。
  {{< /note >}}

各Podは、与えられたアプリケーションの単一のインスタンスを稼働するためのものです。もしユーザーのアプリケーションを水平にスケールさせたい場合(例: 複数インスタンスを稼働させる)、複数のPodを使うべきです。1つのPodは各インスタンスに対応しています。Kubernetesでは、これは一般的に*レプリケーション*と呼ばれます。レプリケーションされたPodは、通常ワークロードリソースと、それに対応する{{< glossary_tooltip text="コントローラー" term_id="controller" >}}によって、作成・管理されます。

Kubernetesがワークロードリソースとそのコントローラーを活用して、スケーラブルで自動回復するアプリケーションを実装する方法については、詳しくは[Podとコントローラー](#pods-and-controllers)を参照してください。

### Podが複数のコンテナを管理する方法

Podは、まとまりの強いサービスのユニットを構成する、複数の協調する(コンテナとして実行される)プロセスをサポートするために設計されました。単一のPod内の複数のコンテナは、クラスター内の同じ物理または仮想マシン上で、自動的に同じ場所に配置・スケジューリングされます。コンテナ間では、リソースや依存関係を共有したり、お互いに通信したり、停止するときにはタイミングや方法を協調して実行できます。

たとえば、あるコンテナが共有ボリューム内のファイルを配信するウェブサーバーとして動作し、別の「サイドカー」コンテナがリモートのリソースからファイルをアップデートするような構成が考えられます。この構成を以下のダイアグラムに示します。

{{< figure src="/images/docs/pod.svg" alt="Podのダイアグラムの例" width="50%" >}}

Podによっては、{{< glossary_tooltip text="appコンテナ" term_id="app-container" >}}に加えて{{< glossary_tooltip text="initコンテナ" term_id="init-container" >}}を持っている場合があります。initコンテナはappコンテナが起動する前に実行・完了するコンテナです。

Podは、Podを構成する複数のコンテナに対して、[ネットワーク](#pod-networking)と[ストレージ](#pod-storage)の2種類の共有リソースを提供します。

## Podを利用する

通常Kubernetesでは、たとえ単一のコンテナしか持たないシングルトンのPodだとしても、個別のPodを直接作成することはめったにありません。その理由は、Podがある程度一時的で使い捨てできる存在として設計されているためです。Podが作成されると(あなたが直接作成した場合でも、{{< glossary_tooltip text="コントローラー" term_id="controller" >}}が間接的に作成した場合でも)、新しいPodはクラスター内の{{< glossary_tooltip term_id="node" >}}上で実行されるようにスケジューリングされます。Podは、実行が完了するか、Podオブジェクトが削除されるか、リソース不足によって*強制退去*されるか、ノードが停止するまで、そのノード上にとどまります。

{{< note >}}
Pod内のコンテナの再起動とPodの再起動を混同しないでください。Podはプロセスではなく、コンテナが実行するための環境です。Podは削除されるまでは残り続けます。
{{< /note >}}

Podオブジェクトのためのマニフェストを作成したときは、指定したPodの名前が有効な[DNSサブドメイン名](/ja/docs/concepts/overview/working-with-objects/names#dns-subdomain-names)であることを確認してください。

### Podとコンテナコントローラー {#pods-and-controllers}

ワークロードリソースは、複数のPodを作成・管理するために利用できます。リソースに対応するコントローラーが、複製やロールアウトを扱い、Podの障害時には自動回復を行います。たとえば、あるノードに障害が発生した場合、コントローラーはそのノードの動作が停止したことを検知し、代わりのPodを作成します。そして、スケジューラーが代わりのPodを健全なノード上に配置します。

以下に、1つ以上のPodを管理するワークロードリソースの一例をあげます。

* {{< glossary_tooltip text="Deployment" term_id="deployment" >}}
* {{< glossary_tooltip text="StatefulSet" term_id="statefulset" >}}
* {{< glossary_tooltip text="DaemonSet" term_id="daemonset" >}}

### Podテンプレート

{{< glossary_tooltip text="workload" term_id="workload" >}}リソース向けのコントローラーは、Podを*Podテンプレート*を元に作成し、あなたの代わりにPodを管理してくれます。

PodTemplateはPodを作成するための仕様で、[Deployment](/ja/docs/concepts/workloads/controllers/deployment/)、[Job](/ja/docs/concepts/workloads/controllers/job/)、[DaemonSet](/ja/docs/concepts/workloads/controllers/daemonset/)などのワークロードリソースの中に含まれています。

ワークロードリソースに対応する各コントローラーは、ワークロードオブジェクト内にある`PodTemplate`を使用して実際のPodを作成します。`PodTemplate`は、アプリを実行するために使われるワークロードリソースがどんな種類のものであれ、その目的の状態の一部を構成するものです。

以下は、単純なJobのマニフェストの一例で、1つのコンテナを実行する`template`があります。Pod内のコンテナはメッセージを出力した後、一時停止します。

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: hello
spec:
  template:
    # これがPodテンプレートです
    spec:
      containers:
      - name: hello
        image: busybox
        command: ['sh', '-c', 'echo "Hello, Kubernetes!" && sleep 3600']
      restartPolicy: OnFailure
    # Podテンプレートはここまでです
```

Podテンプレートを修正するか新しいPodに切り替えたとしても、すでに存在するPodには直接の影響はありません。ワークロードリソース内のPodテンプレートを変更すると、そのリソースは更新されたテンプレートを使用して代わりとなるPodを作成する必要があります。

たとえば、StatefulSetコントローラーは、各StatefulSetごとに、実行中のPodが現在のPodテンプレートに一致することを保証します。Podテンプレートを変更するためにStatefulSetを編集すると、StatefulSetは更新されたテンプレートを元にした新しいPodを作成するようになります。最終的に、すべての古いPodが新しいPodで置き換えられ、更新は完了します。

各ワークロードリソースは、Podテンプレートへの変更を処理するための独自のルールを実装しています。特にStatefulSetについて更に詳しく知りたい場合は、StatefulSetの基本チュートリアル内の[アップデート戦略](/ja/docs/tutorials/stateful-application/basic-stateful-set/#updating-statefulsets)を読んでください。

ノード上では、{{< glossary_tooltip term_id="kubelet" text="kubelet" >}}はPodテンプレートに関する詳細について監視や管理を直接行うわけではありません。こうした詳細は抽象化されています。こうした抽象化や関心の分離のおかげでシステムのセマンティクスが単純化され、既存のコードを変更せずにクラスターの動作を容易に拡張できるようになっているのです。

## リソースの共有と通信

Podは、データの共有と構成するコンテナ間での通信を可能にします。

### Pod内のストレージ {#pod-storage}

Podでは、共有ストレージである{{< glossary_tooltip text="ボリューム" term_id="volume" >}}の集合を指定できます。Pod内のすべてのコンテナは共有ボリュームにアクセスできるため、それら複数のコンテナでデータを共有できるようになります。また、ボリュームを利用すれば、Pod内のコンテナの1つに再起動が必要になった場合にも、Pod内の永続化データを保持し続けられるようにできます。Kubernetesの共有ストレージの実装方法とPodで利用できるようにする方法に関するさらに詳しい情報は、[ストレージ](/ja/docs/concepts/storage/)を読んでください。

### Podネットワーク

各Podには、各アドレスファミリーごとにユニークなIPアドレスが割り当てられます。Pod内のすべてのコンテナは、IPアドレスとネットワークポートを含むネットワーク名前空間を共有します。Podの中では(かつその場合に**のみ**)、そのPod内のコンテナは`localhost`を使用して他のコンテナと通信できます。Podの内部にあるコンテナが*Podの外部にある*エンティティと通信する場合、(ポートなどの)共有ネットワークリソースの使い方をコンテナ間で調整しなければなりません。Pod内では、コンテナはIPアドレスとポートの空間を共有するため、`localhost`で他のコンテナにアクセスできます。また、Pod内のコンテナは、SystemVのセマフォやPOSIXの共有メモリなど、標準のプロセス間通信を使って他のコンテナと通信することもできます。異なるPod内のコンテナは異なるIPアドレスを持つため、[特別な設定](/docs/concepts/policy/pod-security-policy/)をしない限りIPCで通信することはできません。異なるPod上で実行中のコンテナ間でやり取りをしたい場合は、IPネットワークを使用して通信できます。

Pod内のコンテナは、システムのhostnameがPodに設定した`name`と同一であると考えます。ネットワークについての詳しい情報は、[ネットワーク](/ja/docs/concepts/cluster-administration/networking/)で説明しています。

## コンテナの特権モード

Pod内のどんなコンテナも、`privileged`フラグをコンテナのspecの[security context](/docs/tasks/configure-pod-container/security-context/)に設定することで、特権モード(privileged mode)を有効にできます。これは、ネットワークスタックの操作やハードウェアデバイスへのアクセスなど、オペレーティングシステムの管理者の権限が必要なコンテナの場合に役に立ちます。特権コンテナ内のプロセスはコンテナ外のプロセスが利用できるのとほぼ同等の権限を取得します。

{{< note >}}
この設定を有効にするには、{{< glossary_tooltip text="コンテナランタイム" term_id="container-runtime" >}}が特権コンテナの概念をサポートしていなければなりません。
{{< /note >}}

## static Pod

*static Pod*は、{{< glossary_tooltip text="APIサーバー" term_id="kube-apiserver" >}}には管理されない、特定のノード上でkubeletデーモンによって直接管理されるPodのことです。大部分のPodはコントロープレーン(たとえば{{< glossary_tooltip text="Deployment" term_id="deployment" >}})によって管理されますが、static Podの場合はkubeletが各static Podを直接管理します(障害時には再起動します)。

static Podは常に特定のノード上の1つの{{< glossary_tooltip term_id="kubelet" >}}に紐付けられます。static Podの主な用途は、セルフホストのコントロールプレーンを実行すること、言い換えると、kubeletを使用して個別の[コントロールプレーンコンポーネント](/ja/docs/concepts/overview/components/#control-plane-components)を管理することです。

kubeletは自動的にKubernetes APIサーバー上に各static Podに対応する{{< glossary_tooltip text="ミラーPod" term_id="mirror-pod" >}}の作成を試みます。つまり、ノード上で実行中のPodはAPIサーバー上でも見えるようになるけれども、APIサーバー上から制御はできないということです。

## {{% heading "whatsnext" %}}

* [Podのライフサイクル](/ja/docs/concepts/workloads/pods/pod-lifecycle/)について学ぶ。
* [PodPreset](/ja/docs/concepts/workloads/pods/podpreset/)について学ぶ。
* [RuntimeClass](/ja/docs/concepts/containers/runtime-class/)と、それを用いてPodごとに異なるコンテナランタイム設定する方法について学ぶ。
* [Podトポロジー分布制約](/docs/concepts/workloads/pods/pod-topology-spread-constraints/)について読む。
* [PodDisruptionBudget](/ja/docs/concepts/workloads/pods/disruptions/)と、それを使用してクラスターの停止(disruption)中にアプリケーションの可用性を管理する方法について読む。
* PodはKubernetes REST API内のトップレベルのリソースです。[Pod](/ja/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#pod-v1-core)オブジェクトの定義では、オブジェクトの詳細について記述されています。
* [The Distributed System Toolkit: Patterns for Composite Containers](https://kubernetes.io/blog/2015/06/the-distributed-system-toolkit-patterns)では、2つ以上のコンテナを利用する場合の一般的なレイアウトについて説明しています。

Kubernetesが共通のPod APIを他のリソース内(たとえば{{< glossary_tooltip text="StatefulSet" term_id="statefulset" >}}や{{< glossary_tooltip text="Deployment" term_id="deployment" >}}など)にラッピングしている理由の文脈を理解するためには、Kubernetes以前から存在する以下のような既存技術について読むのが助けになります。

  * [Aurora](https://aurora.apache.org/documentation/latest/reference/configuration/#job-schema)
  * [Borg](https://research.google.com/pubs/pub43438.html)
  * [Marathon](https://mesosphere.github.io/marathon/docs/rest-api.html)
  * [Omega](https://research.google/pubs/pub41684/)
  * [Tupperware](https://engineering.fb.com/data-center-engineering/tupperware/)
