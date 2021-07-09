---
reviewers:
title: DaemonSet
content_type: concept
weight: 40
---

<!-- overview -->

_DaemonSet_ は全て(またはいくつか)のNodeが単一のPodのコピーを稼働させることを保証します。Nodeがクラスターに追加されるとき、PodがNode上に追加されます。Nodeがクラスターから削除されたとき、それらのPodはガーベージコレクターにより除去されます。DaemonSetの削除により、DaemonSetが作成したPodもクリーンアップします。

DaemonSetのいくつかの典型的な使用例は以下の通りです。

- クラスターのストレージデーモンを全てのNode上で稼働させる。
- ログ集計デーモンを全てのNode上で稼働させる。
- Nodeのモニタリングデーモンを全てのNode上で稼働させる。

シンプルなケースとして、各タイプのデーモンにおいて、全てのNodeをカバーする1つのDaemonSetが使用されるケースがあります。さらに複雑な設定では、単一のタイプのデーモン用ですが、異なるフラグや、異なるハードウェアタイプに対するメモリー、CPUリクエストを要求する複数のDaemonSetを使用するケースもあります。




<!-- body -->

## DaemonSet Specの記述

### DaemonSetの作成

ユーザーはYAMLファイル内でDaemonSetの設定を記述することができます。例えば、下記の`daemonset.yaml`ファイルでは`fluentd-elasticsearch`というDockerイメージを稼働させるDaemonSetの設定を記述します。

{{< codenew file="controllers/daemonset.yaml" >}}

YAMLファイルに基づいてDaemonSetを作成します。

```
kubectl apply -f https://k8s.io/examples/controllers/daemonset.yaml
```

### 必須のフィールド

他の全てのKubernetesの設定と同様に、DaemonSetは`apiVersion`、`kind`と`metadata`フィールドが必須となります。設定ファイルの活用法に関する一般的な情報は、[ステートレスアプリケーションの稼働](/ja/docs/tasks/run-application/run-stateless-application-deployment/)、[コンテナの設定](/ja/docs/tasks/)、[kubectlを用いたオブジェクトの管理](/ja/docs/concepts/overview/working-with-objects/object-management/)といったドキュメントを参照ください。

DaemonSetオブジェクトの名前は、有効な
[DNSサブドメイン名](/ja/docs/concepts/overview/working-with-objects/names#dns-subdomain-names)である必要があります。

また、DaemonSetにおいて[`.spec`](https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status)セクションも必須となります。

### Podテンプレート

`.spec.template`は`.spec`内での必須のフィールドの1つです。

`.spec.template`は[Podテンプレート](/docs/concepts/workloads/pods/#pod-templates)となります。これはフィールドがネストされていて、`apiVersion`や`kind`をもたないことを除いては、{{< glossary_tooltip text="Pod" term_id="pod" >}}のテンプレートと同じスキーマとなります。

Podに対する必須のフィールドに加えて、DaemonSet内のPodテンプレートは適切なラベルを指定しなくてはなりません([Podセレクター](#pod-selector)の項目を参照ください)。

DaemonSet内のPodテンプレートでは、[`RestartPolicy`](/ja/docs/concepts/workloads/pods/pod-lifecycle/#restart-policy)フィールドを指定せずにデフォルトの`Always`を使用するか、明示的に`Always`を設定するかのどちらかである必要があります。

### Podセレクター

`.spec.selector`フィールドはPodセレクターとなります。これは[Job](/docs/concepts/workloads/controllers/job/)の`.spec.selector`と同じものです。

Kubernetes1.8のように、ユーザーは`.spec.template`のラベルにマッチするPodセレクターを指定しなくてはいけません。Podセレクターは、値を空のままにしてもデフォルト設定にならなくなりました。セレクターのデフォルト化は`kubectl apply`と互換性はありません。また、一度DaemonSetが作成されると、その`.spec.selector`は変更不可能になります。Podセレクターの変更は、意図しないPodの孤立を引き起こし、ユーザーにとってやっかいなものとなります。

`.spec.selector`は2つのフィールドからなるオブジェクトです。

* `matchLabels` - [ReplicationController](/docs/concepts/workloads/controllers/replicationcontroller/)の`.spec.selector`と同じように機能します。
* `matchExpressions` - キーと、値のリストとさらにはそれらのキーとバリューに関連したオペレーターを指定することにより、より洗練された形式のセレクターを構成できます。

上記の2つが指定された場合は、2つの条件をANDでどちらも満たすものを結果として返します。

もし`spec.selector`が指定されたとき、`.spec.template.metadata.labels`とマッチしなければなりません。この2つの値がマッチしない設定をした場合、APIによってリジェクトされます。

### 選択したNode上でPodを稼働させる

もしユーザーが`.spec.template.spec.nodeSelector`を指定したとき、DaemonSetコントローラーは、その[node
selector](/ja/docs/concepts/scheduling-eviction/assign-pod-node/)にマッチするPodをNode上に作成します。同様に、もし`.spec.template.spec.affinity`を指定したとき、DaemonSetコントローラーは[node affinity](/ja/docs/concepts/scheduling-eviction/assign-pod-node/)マッチするPodをNode上に作成します。
もしユーザーがどちらも指定しないとき、DaemonSetコントローラーは全てのNode上にPodを作成します。

## Daemon Podがどのようにスケジューリングされるか

### デフォルトスケジューラーによってスケジューリングされる場合

{{< feature-state state="stable" for-kubernetes-version="1.17" >}}

DaemonSetは全ての利用可能なNodeが単一のPodのコピーを稼働させることを保証します。通常、Podが稼働するNodeはKubernetesスケジューラーによって選択されます。しかし、DaemonSetのPodは代わりにDaemonSetコントローラーによって作成され、スケジューリングされます。   
下記の問題について説明します:

 * 矛盾するPodのふるまい: スケジューリングされるのを待っている通常のPodは、作成されているが`Pending`状態となりますが、DaemonSetのPodは`Pending`状態で作成されません。これはユーザーにとって困惑するものです。
 * [Podプリエンプション(Pod preemption)](/ja/docs/concepts/configuration/pod-priority-preemption/)はデフォルトスケジューラーによってハンドルされます。もしプリエンプションが有効な場合、そのDaemonSetコントローラーはPodの優先順位とプリエンプションを考慮することなくスケジューリングの判断を行います。

`ScheduleDaemonSetPods`は、DaemonSetのPodに対して`NodeAffinity`項目を追加することにより、DaemonSetコントローラーの代わりにデフォルトスケジューラーを使ってDaemonSetのスケジュールを可能にします。その際に、デフォルトスケジューラーはPodをターゲットのホストにバインドします。もしDaemonSetのNodeAffinityが存在するとき、それは新しいものに置き換えられます(ターゲットホストを選択する前に、元のNodeAffinityが考慮されます)。DaemonSetコントローラーはDaemonSetのPodの作成や修正を行うときのみそれらの操作を実施します。そしてDaemonSetの`.spec.template`フィールドに対しては何も変更が加えられません。

```yaml
nodeAffinity:
  requiredDuringSchedulingIgnoredDuringExecution:
    nodeSelectorTerms:
    - matchFields:
      - key: metadata.name
        operator: In
        values:
        - target-host-name
```

さらに、`node.kubernetes.io/unschedulable:NoSchedule`というtolarationがDaemonSetのPodに自動的に追加されます。デフォルトスケジューラーは、DaemonSetのPodのスケジューリングのときに、`unschedulable`なNodeを無視します。

### TaintsとTolerations

DaemonSetのPodは[TaintsとTolerations](/docs/concepts/scheduling-eviction/taint-and-toleration/)の設定を尊重します。下記のTolerationsは、関連する機能によって自動的にDaemonSetのPodに追加されます。

| Toleration Key                           | Effect     | Version | Description |
| ---------------------------------------- | ---------- | ------- | ----------- |
| `node.kubernetes.io/not-ready`           | NoExecute  | 1.13+   | DaemonSetのPodはネットワーク分割のようなNodeの問題が発生したときに除外されません。|
| `node.kubernetes.io/unreachable`         | NoExecute  | 1.13+   | DaemonSetのPodはネットワーク分割のようなNodeの問題が発生したときに除外されません。|
| `node.kubernetes.io/disk-pressure`       | NoSchedule | 1.8+    | |
| `node.kubernetes.io/memory-pressure`     | NoSchedule | 1.8+    | |
| `node.kubernetes.io/unschedulable`       | NoSchedule | 1.12+   | DaemonSetのPodはデフォルトスケジューラーによってスケジュール不可能な属性を許容(tolerate)します。 |
| `node.kubernetes.io/network-unavailable` | NoSchedule | 1.12+   | ホストネットワークを使うDaemonSetのPodはデフォルトスケジューラーによってネットワーク利用不可能な属性を許容(tolerate)します。 |

## Daemon Podとのコミュニケーション

DaemonSet内のPodとのコミュニケーションをする際に考えられるパターンは以下の通りです。:

- **Push**: DaemonSet内のPodは他のサービスに対して更新情報を送信するように設定されます。
- **NodeIPとKnown Port**: PodがNodeIPを介して疎通できるようにするため、DaemonSet内のPodは`hostPort`を使用できます。慣例により、クライアントはNodeIPのリストとポートを知っています。
- **DNS**: 同じPodセレクターを持つ[HeadlessService](/ja/docs/concepts/services-networking/service/#headless-service)を作成し、`endpoints`リソースを使ってDaemonSetを探すか、DNSから複数のAレコードを取得します。
- **Service**: 同じPodセレクターを持つServiceを作成し、複数のうちのいずれかのNode上のDaemonに疎通させるためにそのServiceを使います。

## DaemonSetの更新

もしNodeラベルが変更されたとき、そのDaemonSetは直ちに新しくマッチしたNodeにPodを追加し、マッチしなくなったNodeからPodを削除します。

ユーザーはDaemonSetが作成したPodを修正可能です。しかし、Podは全てのフィールドの更新を許可していません。また、DaemonSetコントローラーは次のNode(同じ名前でも)が作成されたときにオリジナルのテンプレートを使ってPodを作成します。

ユーザーはDaemonSetを削除可能です。`kubectl`コマンドで`--cascade=false`を指定するとDaemonSetのPodはNode上に残り続けます。その後、同じセレクターで新しいDaemonSetを作成すると、新しいDaemonSetは既存のPodを再利用します。PodでDaemonSetを置き換える必要がある場合は、`updateStrategy`に従ってそれらを置き換えます。

ユーザーはDaemonSet上で[ローリングアップデートの実施](/docs/tasks/manage-daemon/update-daemon-set/)が可能です。

## DaemonSetの代替案

### Initスクリプト

Node上で直接起動することにより(例: `init`、`upstartd`、`systemd`を使用する)、デーモンプロセスを稼働することが可能です。この方法は非常に良いですが、このようなプロセスをDaemonSetを介して起動することはいくつかの利点があります。

- アプリケーションと同じ方法でデーモンの監視とログの管理ができる。
- デーモンとアプリケーションで同じ設定用の言語とツール(例: Podテンプレート、`kubectl`)を使える。
- リソースリミットを使ったコンテナ内でデーモンを稼働させることにより、デーモンとアプリケーションコンテナの分離を促進します。しかし、これはPod内でなく、コンテナ内でデーモンを稼働させることにより可能です(Dockerを介して直接起動する)。

### ベアPod

特定のNode上で稼働するように指定したPodを直接作成することは可能です。しかし、DaemonSetはNodeの故障やNodeの破壊的なメンテナンスやカーネルのアップグレードなど、どのような理由に限らず、削除されたもしくは停止されたPodを置き換えます。このような理由で、ユーザーはPod単体を作成するよりもむしろDaemonSetを使うべきです。

### 静的Pod Pods

Kubeletによって監視されているディレクトリに対してファイルを書き込むことによって、Podを作成することが可能です。これは[静的Pod](/docs/tasks/configure-pod-container/static-pod/)と呼ばれます。DaemonSetと違い、静的Podはkubectlや他のKubernetes APIクライアントで管理できません。静的PodはApiServerに依存しておらず、クラスターの自立起動時に最適です。また、静的Podは将来的には廃止される予定です。

### Deployment

DaemonSetは、Podの作成し、そのPodが停止されることのないプロセスを持つことにおいて[Deployment](/ja/docs/concepts/workloads/controllers/deployment/)と同様です(例: webサーバー、ストレージサーバー)。

フロントエンドのようなServiceのように、どのホスト上にPodが稼働するか制御するよりも、レプリカ数をスケールアップまたはスケールダウンしたりローリングアップデートする方が重要であるような、状態をもたないServiceに対してDeploymentを使ってください。
Podのコピーが全てまたは特定のホスト上で常に稼働していることが重要な場合や、他のPodの前に起動させる必要があるときにDaemonSetを使ってください。

