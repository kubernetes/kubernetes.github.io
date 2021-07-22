---
title: ノード
content_type: concept
weight: 10
---

<!-- overview -->

Kubernetesはコンテナを _Node_ 上で実行されるPodに配置することで、ワークロードを実行します。
ノードはクラスターによりますが、1つのVMまたは物理的なマシンです。
各ノードは{{< glossary_tooltip text="Pod" term_id="pod" >}}やそれを制御する{{< glossary_tooltip text="コントロールプレーン" term_id="control-plane" >}}を実行するのに必要なサービスを含んでいます。

通常、1つのクラスターで複数のノードを持ちます。学習用途やリソースの制限がある環境では、1ノードかもしれません。

1つのノード上の[コンポーネント](/ja/docs/concepts/overview/components/#node-components)には、{{< glossary_tooltip text="kubelet" term_id="kubelet" >}}、{{< glossary_tooltip text="コンテナランタイム" term_id="container-runtime" >}}、{{< glossary_tooltip text="kube-proxy" term_id="kube-proxy" >}}が含まれます。

<!-- body -->

## 管理 {#management}

ノードを{{< glossary_tooltip text="APIサーバー" term_id="kube-apiserver" >}}に加えるには2つの方法があります:

1. ノード上のkubeletが、コントロールプレーンに自己登録する。
2. あなた、もしくは他のユーザーが手動でNodeオブジェクトを追加する。

Nodeオブジェクトの作成、もしくはノード上のkubeketによる自己登録の後、コントロールプレーンはNodeオブジェクトが有効かチェックします。例えば、下記のjsonマニフェストでノードを作成してみましょう:

```json
{
  "kind": "Node",
  "apiVersion": "v1",
  "metadata": {
    "name": "10.240.79.157",
    "labels": {
      "name": "my-first-k8s-node"
    }
  }
}
```

Kubernetesは内部的にNodeオブジェクトを作成します。 APIサーバーに登録したkubeletがノードの`metadata.name`フィールドが一致しているか検証します。ノードが有効な場合、つまり必要なサービスがすべて実行されている場合は、Podを実行する資格があります。それ以外の場合、該当ノードが有効になるまではいかなるクラスターの活動に対しても無視されます。

{{< note >}}
Kubernetesは無効なNodeのオブジェクトを保持し、それが有効になるまで検証を続けます。

ヘルスチェックを止めるためには、あなた、もしくは{{< glossary_tooltip term_id="controller" text="コントローラー">}}が明示的にNodeを削除する必要があります。
{{< /note >}}

Nodeオブジェクトの名前は有効な[DNSサブドメイン名](/ja/docs/concepts/overview/working-with-objects/names#dns-subdomain-names)である必要があります。

### ノードの自己登録 {#self-registration-of-nodes}

kubeletのフラグ `--register-node`がtrue（デフォルト）のとき、kubeletは自分自身をAPIサーバーに登録しようとします。これはほとんどのディストリビューションで使用されている推奨パターンです。

自己登録については、kubeletは以下のオプションを伴って起動されます:

  - `--kubeconfig` - 自分自身をAPIサーバーに対して認証するための資格情報へのパス
  - `--cloud-provider` - 自身に関するメタデータを読むために{{< glossary_tooltip text="クラウドプロバイダー" term_id="cloud-provider" >}}と会話する方法
  - `--register-node` - 自身をAPIサーバーに自動的に登録
  - `--register-with-taints` - 与えられた{{< glossary_tooltip text="taint" term_id="taint" >}}のリストでノードを登録します (カンマ区切りの `<key>=<value>:<effect>`)。 
  
  `register-node`がfalseの場合、このオプションは機能しません
  - `--node-ip` - ノードのIPアドレス
  - `--node-labels` - ノードをクラスターに登録するときに追加する{{< glossary_tooltip text="Label" term_id="label" >}}（[NodeRestriction許可プラグイン](/docs/reference/access-authn-authz/admission-controllers/#noderestriction)によって適用されるラベルの制限を参照）
  - `--node-status-update-frequency` - kubeletがノードのステータスをマスターにPOSTする頻度の指定

[ノード認証モード](/docs/reference/access-authn-authz/node/)および[NodeRestriction許可プラグイン](/docs/reference/access-authn-authz/admission-controllers/#noderestriction)が有効になっている場合、kubeletは自分自身のノードリソースを作成/変更することのみ許可されています。

### 手動によるノード管理 {#manual-node-administration}

クラスター管理者は{{< glossary_tooltip text="kubectl" term_id="kubectl" >}}を使用してNodeオブジェクトを作成および変更できます。

管理者が手動でNodeオブジェクトを作成したい場合は、kubeletフラグ `--register-node = false`を設定してください。

管理者は`--register-node`の設定に関係なくNodeオブジェクトを変更することができます。
例えば、ノードにラベルを設定し、それをunschedulableとしてマークすることが含まれます。

ノード上のラベルは、スケジューリングを制御するためにPod上のノードセレクターと組み合わせて使用できます。
例えば、Podをノードのサブセットでのみ実行する資格があるように制限します。

ノードをunschedulableとしてマークすると、新しいPodがそのノードにスケジュールされるのを防ぎますが、ノード上の既存のPodには影響しません。
これは、ノードの再起動などの前の準備ステップとして役立ちます。

ノードにスケジュール不可能のマークを付けるには、次のコマンドを実行します:

```shell
kubectl cordon $ノード名
```

{{< note >}}
{{< glossary_tooltip term_id="daemonset" >}}によって作成されたPodはノード上のunschedulable属性を考慮しません。
これは、再起動の準備中にアプリケーションからアプリケーションが削除されている場合でも、DaemonSetがマシンに属していることを前提としているためです。
{{< /note >}}

## ノードのステータス

ノードのステータスは以下の情報を含みます:

* [Addresses](#addresses)
* [Conditions](#condition)
* [CapacityとAllocatable](#capacity)
* [Info](#info)

`kubectl`を使用し、ノードのステータスや詳細を確認できます:

```shell
kubectl describe node <ノード名をここに挿入>
```

出力情報の各箇所について、以下で説明します。

### Addresses

これらのフィールドの使い方は、お使いのクラウドプロバイダーやベアメタルの設定内容によって異なります。

* HostName: ノードのカーネルによって伝えられたホスト名です。kubeletの`--hostname-override`パラメーターによって上書きすることができます。
* ExternalIP: 通常は、外部にルーティング可能(クラスターの外からアクセス可能)なノードのIPアドレスです。
* InternalIP: 通常は、クラスター内でのみルーティング可能なノードのIPアドレスです。


### Conditions {#condition}

`conditions`フィールドは全ての`Running`なノードのステータスを表します。例として、以下のような状態を含みます:

{{< table caption = "ノードのConditionと、各condition適用時の概要" >}}
| ノードのCondition       | 概要 |
|----------------------|-------------|
| `Ready`              | ノードの状態が有効でPodを配置可能な場合に`True`になります。ノードの状態に問題があり、Podが配置できない場合に`False`になります。ノードコントローラーが、`node-monitor-grace-period`で設定された時間内(デフォルトでは40秒)に該当ノードと疎通できない場合、`Unknown`になります。 |
| `DiskPressure`       | ノードのディスク容量が圧迫されているときに`True`になります。圧迫とは、ディスクの空き容量が少ないことを指します。それ以外のときは`False`です。 |
| `MemoryPressure`     | ノードのメモリが圧迫されているときに`True`になります。圧迫とは、メモリの空き容量が少ないことを指します。それ以外のときは`False`です。 |
| `PIDPressure`        | プロセスが圧迫されているときに`True`になります。圧迫とは、プロセス数が多すぎることを指します。それ以外のときは`False`です。 |
| `NetworkUnavailable` | ノードのネットワークが適切に設定されていない場合に`True`になります。それ以外のときは`False`です。 |
{{< /table >}}

{{< note >}}
コマンドラインを使用してcordonされたNodeを表示する場合、Conditionは`SchedulingDisabled`を含みます。
`SchedulingDisabled`はKubernetesのAPIにおけるConditionではありません;その代わり、cordonされたノードはUnschedulableとしてマークされます。
{{< /note >}}

ノードのConditionはJSONオブジェクトで表現されます。例えば、正常なノードの場合は以下のような構造体が表示されます。

```json
"conditions": [
  {
    "type": "Ready",
    "status": "True",
    "reason": "KubeletReady",
    "message": "kubelet is posting ready status",
    "lastHeartbeatTime": "2019-06-05T18:38:35Z",
    "lastTransitionTime": "2019-06-05T11:41:27Z"
  }
]
```

Ready conditionが`pod-eviction-timeout`({{< glossary_tooltip text="kube-controller-manager" term_id="kube-controller-manager" >}}に渡された引数)に設定された時間を超えても`Unknown`や`False`のままになっている場合、該当ノード上にあるPodはノードコントローラーによって削除がスケジュールされます。デフォルトの退役のタイムアウトの時間は**5分**です。ノードが到達不能ないくつかの場合においては、APIサーバーが該当ノードのkubeletと疎通できない状態になっています。その場合、APIサーバーがkubeletと再び通信を確立するまでの間、Podの削除を行うことはできません。削除がスケジュールされるまでの間、削除対象のPodは切り離されたノードの上で稼働を続けることになります。

ノードコントローラーはクラスター内でPodが停止するのを確認するまでは強制的に削除しないようになりました。到達不能なノード上で動いているPodは`Terminating`または`Unknown`のステータスになります。Kubernetesが基盤となるインフラストラクチャーを推定できない場合、クラスター管理者は手動でNodeオブジェクトを削除する必要があります。KubernetesからNodeオブジェクトを削除すると、そのノードで実行されているすべてのPodオブジェクトがAPIサーバーから削除され、それらの名前が解放されます。

ノードのライフサイクルコントローラーがconditionを表した[taint](/ja/docs/concepts/scheduling-eviction/taint-and-toleration/)を自動的に生成します。
スケジューラーがPodをノードに割り当てる際、ノードのtaintを考慮します。Podが許容するtaintは例外です。

詳細は[条件によるtaintの付与](/ja/docs/concepts/scheduling-eviction/taint-and-toleration/#taint-nodes-by-condition)を参照してください。

### CapacityとAllocatable {#capacity}

ノードで利用可能なリソース（CPU、メモリ、およびノードでスケジュールできる最大Pod数）について説明します。

capacityブロック内のフィールドは、ノードが持っているリソースの合計量を示します。
allocatableブロックは、通常のPodによって消費されるノード上のリソースの量を示します。

CapacityとAllocatableについて深く知りたい場合は、ノード上でどのように[コンピュートリソースが予約されるか](/docs/tasks/administer-cluster/reserve-compute-resources/#node-allocatable)を読みながら学ぶことができます。

### Info {#info}

カーネルのバージョン、Kubernetesのバージョン（kubeletおよびkube-proxyのバージョン）、（使用されている場合）Dockerのバージョン、OS名など、ノードに関する一般的な情報です。
この情報はノードからkubeletを通じて取得されます。

## 管理 {#management}

[Pod](/ja/docs/concepts/workloads/pods/pod/)や[Service](/ja/docs/concepts/services-networking/service/)と違い、ノードは本質的にはKubernetesによって作成されません。GCPのようなクラウドプロバイダーによって外的に作成されるか、VMや物理マシンのプールに存在するものです。そのため、Kubernetesがノードを作成すると、そのノードを表すオブジェクトが作成されます。作成後、Kubernetesはそのノードが有効かどうかを確認します。 たとえば、次の内容からノードを作成しようとしたとします:

```json
{
  "kind": "Node",
  "apiVersion": "v1",
  "metadata": {
    "name": "10.240.79.157",
    "labels": {
      "name": "my-first-k8s-node"
    }
  }
}
```

Kubernetesは内部的にNodeオブジェクトを作成し、 `metadata.name`フィールドに基づくヘルスチェックによってノードを検証します。ノードが有効な場合、つまり必要なサービスがすべて実行されている場合は、Podを実行する資格があります。それ以外の場合、該当ノードが有効になるまではいかなるクラスターの活動に対しても無視されます。
Nodeオブジェクトの名前は有効な[DNSサブドメイン名](/ja/docs/concepts/overview/working-with-objects/names#dns-subdomain-names)である必要があります。

{{< note >}}
Kubernetesは無効なノードのためにオブジェクトを保存し、それをチェックし続けます。
このプロセスを停止するには、Nodeオブジェクトを明示的に削除する必要があります。
{{< /note >}}

現在、Kubernetesのノードインターフェースと相互作用する3つのコンポーネントがあります。ノードコントローラー、kubelet、およびkubectlです。

### ノードコントローラー

ノード{{< glossary_tooltip text="コントローラー" term_id="controller" >}}は、ノードのさまざまな側面を管理するKubernetesのコントロールプレーンコンポーネントです。

ノードコントローラーは、ノードの存続期間中に複数の役割を果たします。1つ目は、ノードが登録されたときにCIDRブロックをノードに割り当てることです（CIDR割り当てがオンになっている場合）。

2つ目は、ノードコントローラーの内部ノードリストをクラウドの利用可能なマシンのリストと一致させることです。
クラウド環境で実行している場合、ノードに異常があると、ノードコントローラーはクラウドプロバイダーにそのNodeのVMがまだ使用可能かどうかを問い合わせます。
使用可能でない場合、ノードコントローラーはノードのリストから該当ノードを削除します。

3つ目は、ノードの状態を監視することです。
ノードが到達不能(例えば、ノードがダウンしているなどので理由で、ノードコントローラーがハートビートの受信を停止した場合)になると、ノードコントローラーは、NodeStatusのNodeReady conditionをConditionUnknownに変更する役割があります。その後も該当ノードが到達不能のままであった場合、Graceful Terminationを使って全てのPodを退役させます。デフォルトのタイムアウトは、ConditionUnknownの報告を開始するまで40秒、その後Podの追い出しを開始するまで5分に設定されています。

ノードコントローラーは、`--node-monitor-period`に設定された秒数ごとに各ノードの状態をチェックします。

#### ハートビート
ハートビートは、Kubernetesノードから送信され、ノードが利用可能か判断するのに役立ちます。
２つのハートビートがあります：`NodeStatus`の更新と[Lease object](/docs/reference/generated/kubernetes-api/{{< latest-version >}}#lease-v1-coordination-k8s-io)です。
各ノードは`kube-node-lease`という{{< glossary_tooltip term_id="namespace" text="namespace">}}に関連したLeaseオブジェクトを持ちます。
Leaseは軽量なリソースで、クラスターのスケールに応じてノードのハートビートにおけるパフォーマンスを改善します。

kubeletが`NodeStatus`とLeaseオブジェクトの作成および更新を担当します。

- kubeletは、ステータスに変化があったり、設定した間隔の間に更新がない時に`NodeStatus`を更新します。`NodeStatus`更新のデフォルト間隔は５分です。（到達不能の場合のデフォルトタイムアウトである40秒よりもはるかに長いです）
- kubeletは10秒間隔(デフォルトの更新間隔)でLeaseオブジェクトの生成と更新を実施します。Leaseの更新は`NodeStatus`の更新とは独立されて行われます。Leaseの更新が失敗した場合、kubeletは200ミリ秒から始まり7秒を上限とした指数バックオフでリトライします。

#### 信頼性

ほとんどの場合、排除の速度は1秒あたり`--node-eviction-rate`に設定された数値（デフォルトは秒間0.1）です。つまり、10秒間に1つ以上のPodをノードから追い出すことはありません。

特定のアベイラビリティーゾーン内のノードのステータスが異常になると、ノード排除の挙動が変わります。ノードコントローラーは、ゾーン内のノードの何%が異常（NodeReady条件がConditionUnknownまたはConditionFalseである）であるかを同時に確認します。
異常なノードの割合が少なくとも `--healthy-zone-threshold`に設定した値を下回る場合（デフォルトは0.55）であれば、退役率は低下します。クラスターが小さい場合（すなわち、 `--large-cluster-size-threshold`の設定値よりもノード数が少ない場合。デフォルトは50）、退役は停止し、そうでない場合、退役率は秒間で`--secondary-node-eviction-rate`の設定値（デフォルトは0.01）に減少します。

これらのポリシーがアベイラビリティーゾーンごとに実装されているのは、1つのアベイラビリティーゾーンがマスターから分割される一方、他のアベイラビリティーゾーンは接続されたままになる可能性があるためです。
クラスターが複数のクラウドプロバイダーのアベイラビリティーゾーンにまたがっていない場合、アベイラビリティーゾーンは1つだけです（クラスター全体）。

ノードを複数のアベイラビリティゾーンに分散させる主な理由は、1つのゾーン全体が停止したときにワークロードを正常なゾーンに移動できることです。
したがって、ゾーン内のすべてのノードが異常である場合、ノードコントローラーは通常のレート `--node-eviction-rate`で退役します。
コーナーケースは、すべてのゾーンが完全にUnhealthyである（すなわち、クラスタ内にHealthyなノードがない）場合です。
このような場合、ノードコントローラーはマスター接続に問題があると見なし、接続が回復するまですべての退役を停止します。

ノードコントローラーは、Podがtaintを許容しない場合、 `NoExecute`のtaintを持つノード上で実行されているPodを排除する責務もあります。
さらに、ノードコントローラーはノードに到達できない、または準備ができていないなどのノードの問題に対応する{{< glossary_tooltip text="taint" term_id="taint" >}}を追加する責務があります。これはスケジューラーが、問題のあるノードにPodを配置しない事を意味しています。

{{< caution >}}
`kubectl cordon`はノードに'unschedulable'としてマークします。それはロードバランサーのターゲットリストからノードを削除するという
サービスコントローラーの副次的な効果をもたらします。これにより、ロードバランサトラフィックの流入をcordonされたノードから効率的に除去する事ができます。
{{< /caution >}}

### ノードのキャパシティ

Nodeオブジェクトはノードのリソースキャパシティ（CPUの数とメモリの量）を監視します。
[自己登録](#self-registration-of-nodes)したノードは、Nodeオブジェクトを作成するときにキャパシティを報告します。
[手動によるノード管理](#manual-node-administration)を実行している場合は、ノードを追加するときにキャパシティを設定する必要があります。

Kubernetes{{< glossary_tooltip text="スケジューラー" term_id="kube-scheduler" >}}は、ノード上のすべてのPodに十分なリソースがあることを確認します。スケジューラーは、ノード上のコンテナが要求するリソースの合計がノードキャパシティ以下であることを確認します。
これは、kubeletによって管理されたすべてのコンテナを含みますが、コンテナランタイムによって直接開始されたコンテナやkubeletの制御外で実行されているプロセスは含みません。

{{< note >}}
Pod以外のプロセス用にリソースを明示的に予約したい場合は、[Systemデーモン用にリソースを予約](/docs/tasks/administer-cluster/reserve-compute-resources/#system-reserved)を参照してください。
{{< /note >}}

## ノードのトポロジー

{{< feature-state state="alpha" for_k8s_version="v1.16" >}}
`TopologyManager`の[フィーチャーゲート](/ja/docs/reference/command-line-tools-reference/feature-gates/)を有効にすると、
kubeletはリソースの割当を決定する際にトポロジーのヒントを利用できます。
詳細は、[ノードのトポロジー管理ポリシーを制御する](/docs/tasks/administer-cluster/topology-manager/)を参照してください。

## {{% heading "whatsnext" %}}

* [ノードコンポーネント](/ja/docs/concepts/overview/components/#node-components)について学習する。
* [Node APIオブジェクト](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#node-v1-core)について読む。
* アーキテクチャ設計文書の[Node](https://git.k8s.io/community/contributors/design-proposals/architecture/architecture.md#the-kubernetes-node)という章を読む。
* [TaintとToleration](/ja/docs/concepts/scheduling-eviction/taint-and-toleration/)について読む。
