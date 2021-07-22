---
reviewers:
title: ReplicaSet
content_type: concept
weight: 20
---

<!-- overview -->

ReplicaSetの目的は、どのような時でも安定したレプリカPodのセットを維持することです。これは、理想的なレプリカ数のPodが利用可能であることを保証するものとして使用されます。




<!-- body -->

## ReplicaSetがどのように動くか

ReplicaSetは、ReplicaSetが対象とするPodをどう特定するかを示すためのセレクターや、稼働させたいPodのレプリカ数、Podテンプレート(理想のレプリカ数の条件を満たすために作成される新しいPodのデータを指定するために用意されるもの)といったフィールドとともに定義されます。ReplicaSetは、指定された理想のレプリカ数にするためにPodの作成と削除を行うことにより、その目的を達成します。ReplicaSetが新しいPodを作成するとき、ReplicaSetはそのPodテンプレートを使用します。

ReplicaSetがそのPod群と連携するためのリンクは、Podの[metadata.ownerReferences](/ja/docs/concepts/workloads/controllers/garbage-collection/#owners-and-dependents)というフィールド(現在のオブジェクトが所有されているリソースを指定する)を介して作成されます。ReplicaSetによって所持された全てのPodは、それらの`ownerReferences`フィールドにReplicaSetを特定する情報を保持します。このリンクを通じて、ReplicaSetは管理しているPodの状態を把握したり、その後の実行計画を立てます。

ReplicaSetは、そのセレクターを使用することにより、所有するための新しいPodを特定します。もし`ownerReference`フィールドの値を持たないPodか、`ownerReference`フィールドの値が {{< glossary_tooltip text="コントローラー" term_id="controller" >}}でないPodで、そのPodがReplicaSetのセレクターとマッチした場合に、そのPodは即座にそのReplicaSetによって所有されます。

## ReplicaSetを使うとき

ReplicaSetはどんな時でも指定された数のPodのレプリカが稼働することを保証します。しかし、DeploymentはReplicaSetを管理する、より上位レベルの概念で、Deploymentはその他の多くの有益な機能と共に、宣言的なPodのアップデート機能を提供します。それゆえ、我々はユーザーが独自のアップデートオーケストレーションを必要としたり、アップデートを全く必要としないような場合を除いて、ReplicaSetを直接使うよりも代わりにDeploymentを使うことを推奨します。

これは、ユーザーがReplicaSetのオブジェクトを操作する必要が全く無いことを意味します。
代わりにDeploymentを使用して、`spec`セクションにユーザーのアプリケーションを定義してください。

## ReplicaSetの使用例

{{< codenew file="controllers/frontend.yaml" >}}

上記のマニフェストを`frontend.yaml`ファイルに保存しKubernetesクラスターに適用すると、マニフェストに定義されたReplicaSetとそれが管理するPod群を作成します。

```shell
kubectl apply -f http://k8s.io/examples/controllers/frontend.yaml
```

ユーザーはデプロイされた現在のReplicaSetの情報も取得できます。
```shell
kubectl get rs
```

そして、ユーザーが作成したfrontendリソースについての情報も取得できます。
```shell
NAME       DESIRED   CURRENT   READY   AGE
frontend   3         3         3       6s
```

ユーザーはまたReplicaSetの状態も確認できます。
```shell
kubectl describe rs/frontend
```

その結果は以下のようになります。
```shell
Name:		frontend
Namespace:	default
Selector:	tier=frontend
Labels:		app=guestbook
		tier=frontend
Annotations:	kubectl.kubernetes.io/last-applied-configuration:
                {"apiVersion":"apps/v1","kind":"ReplicaSet","metadata":{"annotations":{},"labels":{"app":"guestbook","tier":"frontend"},"name":"frontend",...
Replicas:	3 current / 3 desired
Pods Status:	3 Running / 0 Waiting / 0 Succeeded / 0 Failed
Pod Template:
  Labels:  tier=frontend
  Containers:
   php-redis:
    Image:        gcr.io/google_samples/gb-frontend:v3
    Port:         <none>
    Host Port:    <none>
    Environment:  <none>
    Mounts:       <none>
  Volumes:        <none>
Events:
  Type    Reason            Age   From                   Message
  ----    ------            ----  ----                   -------
  Normal  SuccessfulCreate  117s  replicaset-controller  Created pod: frontend-wtsmm
  Normal  SuccessfulCreate  116s  replicaset-controller  Created pod: frontend-b2zdv
  Normal  SuccessfulCreate  116s  replicaset-controller  Created pod: frontend-vcmts
```

そして最後に、ユーザーはReplicaSetによって作成されたPodもチェックできます。
```shell
kubectl get pods
```

表示されるPodに関する情報は以下のようになります。
```shell
NAME             READY   STATUS    RESTARTS   AGE
frontend-b2zdv   1/1     Running   0          6m36s
frontend-vcmts   1/1     Running   0          6m36s
frontend-wtsmm   1/1     Running   0          6m36s
```

ユーザーはまた、それらのPodの`ownerReferences`が`frontend`ReplicaSetに設定されていることも確認できます。
これを確認するためには、稼働しているPodの中のどれかのyamlファイルを取得します。
```shell
kubectl get pods frontend-b2zdv -o yaml
```

その表示結果は、以下のようになります。その`frontend`ReplicaSetの情報が`metadata`の`ownerReferences`フィールドにセットされています。
```shell
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: "2020-02-12T07:06:16Z"
  generateName: frontend-
  labels:
    tier: frontend
  name: frontend-b2zdv
  namespace: default
  ownerReferences:
  - apiVersion: apps/v1
    blockOwnerDeletion: true
    controller: true
    kind: ReplicaSet
    name: frontend
    uid: f391f6db-bb9b-4c09-ae74-6a1f77f3d5cf
...
```

## テンプレートなしのPodの所有

ユーザーが問題なくベアPod(Bare Pod: ここではPodテンプレート無しのPodのこと)を作成しているとき、そのベアPodがユーザーのReplicaSetの中のいずれのセレクターともマッチしないことを確認することを強く推奨します。
この理由として、ReplicaSetは、所有対象のPodがReplicaSetのテンプレートによって指定されたPodのみに限定されていないからです(ReplicaSetは前のセクションで説明した方法によって他のPodも所有できます)。

前のセクションで取り上げた`frontend`ReplicaSetと、下記のマニフェストのPodをみてみます。

{{< codenew file="pods/pod-rs.yaml" >}}

これらのPodは`ownerReferences`に何のコントローラー(もしくはオブジェクト)も指定されておらず、そして`frontend`ReplicaSetにマッチするセレクターをもっており、これらのPodは即座に`frontend`ReplicaSetによって所有されます。

この`frontend`ReplicaSetがデプロイされ、初期のPodレプリカがレプリカ数の要求を満たすためにセットアップされた後で、ユーザーがそのPodを作成することを考えます。

```shell
kubectl apply -f http://k8s.io/examples/pods/pod-rs.yaml
```

新しいPodはそのReplicaSetによって所有され、そのReplicaSetのレプリカ数が、設定された理想のレプリカ数を超えた場合すぐにそれらのPodは削除されます。

下記のコマンドでPodを取得できます。
```shell
kubectl get pods
```

その表示結果で、新しいPodがすでに削除済みか、削除中のステータスになっているのを確認できます。
```shell
NAME             READY   STATUS        RESTARTS   AGE
frontend-b2zdv   1/1     Running       0          10m
frontend-vcmts   1/1     Running       0          10m
frontend-wtsmm   1/1     Running       0          10m
pod1             0/1     Terminating   0          1s
pod2             0/1     Terminating   0          1s
```

もしユーザーがそのPodを最初に作成する場合
```shell
kubectl apply -f http://k8s.io/examples/pods/pod-rs.yaml
```

そしてその後に`frontend`ReplicaSetを作成すると、
```shell
kubectl apply -f http://k8s.io/examples/controllers/frontend.yaml
```

ユーザーはそのReplicaSetが作成したPodを所有し、さらにもともと存在していたPodと今回新たに作成されたPodの数が、理想のレプリカ数になるまでPodを作成するのを確認できます。
ここでまたPodの状態を取得します。
```shell
kubectl get pods
```

取得結果は下記のようになります。
```shell
NAME             READY   STATUS    RESTARTS   AGE
frontend-hmmj2   1/1     Running   0          9s
pod1             1/1     Running   0          36s
pod2             1/1     Running   0          36s
```

この方法で、ReplicaSetはテンプレートで指定されたもの以外のPodを所有することができます。

## ReplicaSetのマニフェストを記述する。

他の全てのKubernetes APIオブジェクトのように、ReplicaSetは`apiVersion`、`kind`と`metadata`フィールドを必要とします。
ReplicaSetでは、`kind`フィールドの値は`ReplicaSet`です。
Kubernetes1.9において、ReplicaSetは`apps/v1`というAPIバージョンが現在のバージョンで、デフォルトで有効です。`apps/v1beta2`というAPIバージョンは廃止されています。先ほど作成した`frontend.yaml`ファイルの最初の行を参考にしてください。

ReplicaSetオブジェクトの名前は、有効な
[DNSサブドメイン名](/ja/docs/concepts/overview/working-with-objects/names#dns-subdomain-names)である必要があります。

また、ReplicaSetは[`.spec` セクション](https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status)も必須です。

### Pod テンプレート

`.spec.template`はラベルを持つことが必要な[Pod テンプレート](/ja/docs/concepts/workloads/pods/#podテンプレート) です。先ほど作成した`frontend.yaml`の例では、`tier: frontend`というラベルを1つ持っています。
他のコントローラーがこのPodを所有しようとしないためにも、他のコントローラーのセレクターでラベルを上書きしないように注意してください。

テンプレートの[再起動ポリシー](/docs/concepts/workloads/Pods/pod-lifecycle/#restart-policy)のためのフィールドである`.spec.template.spec.restartPolicy`は`Always`のみ許可されていて、そしてそれがデフォルト値です。

### Pod セレクター

`.spec.selector`フィールドは[ラベルセレクター](/ja/docs/concepts/overview/working-with-objects/labels/)です。
[先ほど](#how-a-replicaset-works)議論したように、ReplicaSetが所有するPodを指定するためにそのラベルが使用されます。
先ほどの`frontend.yaml`の例では、そのセレクターは下記のようになっていました
```yaml
matchLabels:
  tier: frontend
```

そのReplicaSetにおいて、`.spec.template.metadata.labels`フィールドの値は`spec.selector`と一致しなくてはならず、一致しない場合はAPIによって拒否されます。

{{< note >}}
2つのReplicaSetが同じ`.spec.selector`の値を設定しているが、それぞれ異なる`.spec.template.metadata.labels`と`.spec.template.spec`フィールドの値を持っていたとき、それぞれのReplicaSetはもう一方のReplicaSetによって作成されたPodを無視します。
{{< /note >}}

### レプリカ数について

ユーザーは`.spec.replicas`フィールドの値を設定することにより、いくつのPodを同時に稼働させるか指定できます。そのときReplicaSetはレプリカ数がこの値に達するまでPodを作成、または削除します。

もしユーザーが`.spec.replicas`を指定しない場合、デフォルト値として1がセットされます。

## ReplicaSetを利用する

### ReplicaSetとPodの削除

ReplicaSetとそれが所有する全てのPod削除したいときは、[`kubectl delete`](/docs/reference/generated/kubectl/kubectl-commands#delete)コマンドを使ってください。  
[ガベージコレクター](/ja/docs/concepts/workloads/controllers/garbage-collection/)がデフォルトで自動的に全ての依存するPodを削除します。

REST APIもしくは`client-go`ライブラリーを使用するとき、ユーザーは`-d`オプションで`propagationPolicy`を`Background`か`Foreground`と指定しなくてはなりません。
例えば下記のように実行します。
```shell
kubectl proxy --port=8080
curl -X DELETE  'localhost:8080/apis/apps/v1/namespaces/default/replicasets/frontend' \
> -d '{"kind":"DeleteOptions","apiVersion":"v1","propagationPolicy":"Foreground"}' \
> -H "Content-Type: application/json"
```

### ReplicaSetのみを削除する

ユーザーは[`kubectl delete`](/docs/reference/generated/kubectl/kubectl-commands#delete)コマンドで`--cascade=orphan`オプションを付けることにより、所有するPodに影響を与えることなくReplicaSetを削除できます。
REST APIもしくは`client-go`ライブラリーを使用するとき、ユーザーは`-d`オプションで`propagationPolicy`を`Orphan`と指定しなくてはなりません。
```shell
kubectl proxy --port=8080
curl -X DELETE  'localhost:8080/apis/apps/v1/namespaces/default/replicasets/frontend' \
> -d '{"kind":"DeleteOptions","apiVersion":"v1","propagationPolicy":"Orphan"}' \
> -H "Content-Type: application/json"
```

一度元のReplicaSetが削除されると、ユーザーは新しいものに置き換えるため新しいReplicaSetを作ることができます。新旧のReplicaSetの`.spec.selector`の値が同じである間、新しいReplicaSetは古いReplicaSetで稼働していたPodを取り入れます。
しかし、存在するPodが新しく異なるPodテンプレートとマッチさせようとするとき、この仕組みは機能しません。
ユーザーのコントロール下において新しいspecのPodをアップデートしたい場合は、[ローリングアップデート](#rolling-updates)を使用してください。

### PodをReplicaSetから分離させる

ユーザーはPodのラベルを変更することにより、ReplicaSetからそのPodを削除できます。この手法はデバッグや、データ修復などのためにサービスからPodを削除したいときに使用できます。
この方法で削除されたPodは自動的に新しいものに置き換えられます。(レプリカ数は変更されないものと仮定します。)

### ReplicaSetのスケーリング

ReplicaSetは、ただ`.spec.replicas`フィールドを更新することによって簡単にスケールアップまたはスケールダウンできます。ReplicaSetコントローラーは、ラベルセレクターにマッチするような指定した数のPodが利用可能であり、操作可能であることを保証します。

### HorizontalPodAutoscaler(HPA)のターゲットとしてのReplicaSet

ReplicaSetはまた、[Horizontal Pod Autoscalers (HPA)](/docs/tasks/run-application/horizontal-pod-autoscale/)のターゲットにもなることができます。
これはつまりReplicaSetがHPAによってオートスケールされうることを意味します。
ここではHPAが、前の例で作成したReplicaSetをターゲットにする例を示します。

{{< codenew file="controllers/hpa-rs.yaml" >}}

このマニフェストを`hpa-rs.yaml`に保存し、Kubernetesクラスターに適用すると、レプリケートされたPodのCPU使用量にもとづいてターゲットのReplicaSetをオートスケールするHPAを作成します。

```shell
kubectl apply -f https://k8s.io/examples/controllers/hpa-rs.yaml
```

同様のことを行うための代替案として、`kubectl autoscale`コマンドも使用できます。(こちらの方がより簡単です。)

```shell
kubectl autoscale rs frontend --max=10 --min=3 --cpu-percent=50
```

## ReplicaSetの代替案

### Deployment (推奨)

[`Deployment`](/ja/docs/concepts/workloads/controllers/deployment/)はReplicaSetを所有することのできるオブジェクトで、宣言的なサーバサイドのローリングアップデートを介してReplicaSetとPodをアップデートできます。
ReplicaSetは単独で使用可能ですが、現在では、ReplicaSetは主にPodの作成、削除とアップデートを司るためのメカニズムとしてDeploymentによって使用されています。ユーザーがDeploymentを使用するとき、Deploymentによって作成されるReplicaSetの管理について心配する必要はありません。DeploymentはReplicaSetを所有し、管理します。
このため、もしユーザーがReplicaSetを必要とするとき、Deploymentの使用を推奨します。

### ベアPod(Bare Pods)

ユーザーがPodを直接作成するケースとは異なり、ReplicaSetはNodeの故障やカーネルのアップグレードといった破壊的なNodeのメンテナンスなど、どのような理由に限らず削除または停止されたPodを置き換えます。
このため、我々はもしユーザーのアプリケーションが単一のPodのみ必要とする場合でもReplicaSetを使用することを推奨します。プロセスのスーパーバイザーについても同様に考えると、それは単一Node上での独立したプロセスの代わりに複数のNodeにまたがった複数のPodを監視します。
ReplicaSetは、Node上のいくつかのエージェント(例えば、KubeletやDocker）に対して、ローカルのコンテナ再起動を移譲します。

### Job

PodをPodそれ自身で停止させたいような場合(例えば、バッチ用のジョブなど)は、ReplicaSetの代わりに[`Job`](/docs/concepts/workloads/controllers/job/)を使用してください。

### DaemonSet

マシンの監視やロギングなど、マシンレベルの機能を提供したい場合は、ReplicaSetの代わりに[`DaemonSet`](/ja/docs/concepts/workloads/controllers/daemonset/)を使用してください。
これらのPodはマシン自体のライフタイムに紐づいています: そのPodは他のPodが起動する前に、そのマシン上で稼働される必要があり、マシンが再起動またはシャットダウンされるときには、安全に停止されます。

### ReplicationController

ReplicaSetは[_ReplicationControllers_](/docs/concepts/workloads/controllers/replicationcontroller/)の後継となるものです。
この2つは、ReplicationControllerが[ラベルについてのユーザーガイド](/ja/docs/concepts/overview/working-with-objects/labels/#label-selectors)に書かれているように、集合ベース(set-based)のセレクター要求をサポートしていないことを除いては、同じ目的を果たし、同じようにふるまいます。  
このように、ReplicaSetはReplicationControllerよりも好まれます。


