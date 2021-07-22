---
title: StatefulSetの基本
content_type: tutorial
weight: 10
---

<!-- overview -->
このチュートリアルでは、{{< glossary_tooltip text="StatefulSet" term_id="statefulset" >}}を使用したアプリケーションを管理するための基本を説明します。StatefulSetのPodを作成、削除、スケール、そして更新する方法について紹介します。

## {{% heading "prerequisites" %}}

このチュートリアルを始める前に、以下のKubernetesの概念について理解しておく必要があります。

* [Pod](/ja/docs/concepts/workloads/pods/)
* [Cluster DNS](/ja/docs/concepts/services-networking/dns-pod-service/)
* [Headless Service](/ja/docs/concepts/services-networking/service/#headless-services)
* [PersistentVolume](/ja/docs/concepts/storage/persistent-volumes/)
* [PersistentVolumeのプロビジョニング](https://github.com/kubernetes/examples/tree/{{< param "githubbranch" >}}/staging/persistent-volume-provisioning/)
* [StatefulSet](/ja/docs/concepts/workloads/controllers/statefulset/)
* [kubectl](/docs/reference/kubectl/kubectl/)コマンドラインツール

{{< note >}}
このチュートリアルでは、クラスターがPersistentVolumeの動的なプロビジョニングが行われるように設定されていることを前提としています。クラスターがそのように設定されていない場合、チュートリアルを始める前に1GiBのボリュームを2つ手動でプロビジョニングする必要があります。
{{< /note >}}

## {{% heading "objectives" %}}

StatefulSetはステートフルアプリケーションや分散システムで使用するために存在します。しかし、Kubernetes上のステートフルアプリケーションや分散システムは、広範で複雑なトピックです。StatefulSetの基本的な機能を示すという目的のため、また、ステートフルアプリケーションを分散システムと混同しないようにするために、ここでは、Statefulsetを使用する単純なウェブアプリケーションのデプロイを行います。

このチュートリアルを終えると、以下のことが理解できるようになります。

* StatefulSetの作成方法
* StatefulSetがどのようにPodを管理するのか
* StatefulSetの削除方法
* StatefulSetのスケール方法
* StatefulSetが管理するPodの更新方法

<!-- lessoncontent -->

## StatefulSetを作成する {#ordered-pod-creation}

はじめに、以下の例を使ってStatefulSetを作成しましょう。これは、コンセプトの[StatefulSet](/ja/docs/concepts/workloads/controllers/statefulset/)のページで使ったものと同じような例です。`nginx`という[headless Service](/ja/docs/concepts/services-networking/service/#headless-services)を作成し、`web`というStatefulSet内のPodのIPアドレスを公開します。

{{< codenew file="application/web/web.yaml" >}}

上の例をダウンロードして、`web.yaml`という名前で保存します。

ここでは、ターミナルウィンドウを2つ使う必要があります。1つ目のターミナルでは、[`kubectl get`](/docs/reference/generated/kubectl/kubectl-commands/#get)を使って、StatefulSetのPodの作成を監視します。

```shell
kubectl get pods -w -l app=nginx
```

2つ目のターミナルでは、[`kubectl apply`](/docs/reference/generated/kubectl/kubectl-commands/#apply)を使って、`web.yaml`に定義されたheadless ServiceとStatefulSetを作成します。

```shell
kubectl apply -f web.yaml
```
```
service/nginx created
statefulset.apps/web created
```

上のコマンドを実行すると、2つのPodが作成され、それぞれのPodで[NGINX](https://www.nginx.com)ウェブサーバーが実行されます。`nginx`Serviceを取得してみましょう。
```shell
kubectl get service nginx
```
```
NAME      TYPE         CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
nginx     ClusterIP    None         <none>        80/TCP    12s
```
そして、`web`StatefulSetを取得して、2つのリソースの作成が成功したことも確認します。
```shell
kubectl get statefulset web
```
```
NAME      DESIRED   CURRENT   AGE
web       2         1         20s
```

### 順序付きPodの作成

_n_ 個のレプリカを持つStatefulSetは、Podをデプロイするとき、1つずつ順番に作成し、 _{0..n-1}_ という順序付けを行います。1つ目のターミナルで`kubectl get`コマンドの出力を確認しましょう。最終的に、以下の例のような出力が表示されるはずです。

```shell
kubectl get pods -w -l app=nginx
```
```
NAME      READY     STATUS    RESTARTS   AGE
web-0     0/1       Pending   0          0s
web-0     0/1       Pending   0         0s
web-0     0/1       ContainerCreating   0         0s
web-0     1/1       Running   0         19s
web-1     0/1       Pending   0         0s
web-1     0/1       Pending   0         0s
web-1     0/1       ContainerCreating   0         0s
web-1     1/1       Running   0         18s
```

`web-0`Podが _Running_ ([Pod Phase](/ja/docs/concepts/workloads/pods/pod-lifecycle/#pod-phase)を参照)かつ _Ready_ ([Pod Conditions](/ja/docs/concepts/workloads/pods/pod-lifecycle/#pod-conditions)の`type`を参照)の状態になるまでは、`web-1`Podが起動していないことに注目してください。

## StatefulSet内のPod

StatefulSet内のPodは、ユニークな順序インデックスと安定したネットワーク識別子を持ちます。

### Podの順序インデックスを確かめる

StatefulSetのPodを取得します。

```shell
kubectl get pods -l app=nginx
```
```
NAME      READY     STATUS    RESTARTS   AGE
web-0     1/1       Running   0          1m
web-1     1/1       Running   0          1m
```

[StatefulSet](/ja/docs/concepts/workloads/controllers/statefulset/)のコンセプトで説明したように、StatefulSet内のPodは安定したユニークな識別子を持ちます。この識別子は、StatefulSet{{< glossary_tooltip term_id="controller" text="コントローラー">}}によって各Podに割り当てられる、ユニークな順序インデックスに基づいて付けられます。Podの名前は、`<statefulsetの名前>-<順序インデックス>`という形式です。`web`StatefulSetは2つのレプリカを持つため、`web-0`と`web-1`という2つのPodを作成します。

### 安定したネットワーク識別子の使用

各Podは、順序インデックスに基づいた安定したホスト名を持ちます。[`kubectl exec`](/docs/reference/generated/kubectl/kubectl-commands/#exec)を使用して、各Pod内で`hostname`コマンドを実行してみましょう。

```shell
for i in 0 1; do kubectl exec "web-$i" -- sh -c 'hostname'; done
```
```
web-0
web-1
```

[`kubectl run`](/docs/reference/generated/kubectl/kubectl-commands/#run)を使用して、`dnsutils`パッケージの`nslookup`コマンドを提供するコンテナを実行します。Podのホスト名に対して`nslookup`を実行すると、クラスター内のDNSアドレスが確認できます。

```shell
kubectl run -i --tty --image busybox:1.28 dns-test --restart=Never --rm
```
これにより、新しいシェルが起動します。新しいシェルで、次のコマンドを実行します。
```shell
# このコマンドは、dns-testコンテナのシェルで実行してください
nslookup web-0.nginx
```
出力は次のようになります。
```
Server:    10.0.0.10
Address 1: 10.0.0.10 kube-dns.kube-system.svc.cluster.local

Name:      web-0.nginx
Address 1: 10.244.1.6

nslookup web-1.nginx
Server:    10.0.0.10
Address 1: 10.0.0.10 kube-dns.kube-system.svc.cluster.local

Name:      web-1.nginx
Address 1: 10.244.2.6
```

(コンテナのシェルを終了するために、`exit`コマンドを実行してください。)

headless serviceのCNAMEは、SRVレコードを指しています(1つのレコードがRunningかつReadyのPodに対応します)。SRVレコードは、PodのIPアドレスを含むAレコードを指します。

1つ目のターミナルで、StatefulSetのPodを監視します。

```shell
kubectl get pod -w -l app=nginx
```
2つ目のターミナルで、[`kubectl delete`](/docs/reference/generated/kubectl/kubectl-commands/#delete)を使用して、StatefulSetのすべてのPodを削除します。

```shell
kubectl delete pod -l app=nginx
```
```
pod "web-0" deleted
pod "web-1" deleted
```

StatefulSetがPodを再起動して、2つのPodがRunningかつReadyの状態に移行するのを待ちます。

```shell
kubectl get pod -w -l app=nginx
```
```
NAME      READY     STATUS              RESTARTS   AGE
web-0     0/1       ContainerCreating   0          0s
NAME      READY     STATUS    RESTARTS   AGE
web-0     1/1       Running   0          2s
web-1     0/1       Pending   0         0s
web-1     0/1       Pending   0         0s
web-1     0/1       ContainerCreating   0         0s
web-1     1/1       Running   0         34s
```

`kubectl exec`と`kubectl run`コマンドを使用して、Podのホスト名とクラスター内DNSエントリーを確認します。まず、Podのホスト名を見てみましょう。

```shell
for i in 0 1; do kubectl exec web-$i -- sh -c 'hostname'; done
```
```
web-0
web-1
```
その後、次のコマンドを実行します。
```
kubectl run -i --tty --image busybox:1.28 dns-test --restart=Never --rm /bin/sh
```
これにより、新しいシェルが起動します。新しいシェルで、次のコマンドを実行します。
```shell
# このコマンドは、dns-testコンテナのシェルで実行してください
nslookup web-0.nginx
```
出力は次のようになります。
```
Server:    10.0.0.10
Address 1: 10.0.0.10 kube-dns.kube-system.svc.cluster.local

Name:      web-0.nginx
Address 1: 10.244.1.7

nslookup web-1.nginx
Server:    10.0.0.10
Address 1: 10.0.0.10 kube-dns.kube-system.svc.cluster.local

Name:      web-1.nginx
Address 1: 10.244.2.8
```

(コンテナのシェルを終了するために、`exit`コマンドを実行してください。)

Podの順序インデックス、ホスト名、SRVレコード、そしてAレコード名は変化していませんが、Podに紐付けられたIPアドレスは変化する可能性があります。このチュートリアルで使用しているクラスターでは、IPアドレスは変わりました。このようなことがあるため、他のアプリケーションがStatefulSet内のPodに接続するときには、IPアドレスで指定しないことが重要です。

StatefulSetの有効なメンバーを探して接続する必要がある場合は、headless ServiceのCNAME(`nginx.default.svc.cluster.local`)をクエリしなければなりません。CNAMEに紐付けられたSRVレコードには、StatefulSet内のRunnningかつReadyなPodだけが含まれます。

アプリケーションがlivenessとreadinessをテストするコネクションのロジックをすでに実装している場合、PodのSRVレコード(`web-0.nginx.default.svc.cluster.local`、`web-1.nginx.default.svc.cluster.local`)をPodが安定しているものとして使用できます。PodがRunning and Readyな状態に移行すれば、アプリケーションはPodのアドレスを発見できるようになります。

### 安定したストレージへの書き込み {#writing-to-stable-storage}

`web-0`および`web-1`のためのPersistentVolumeClaimを取得しましょう。

```shell
kubectl get pvc -l app=nginx
```
出力は次のようになります。
```
NAME        STATUS    VOLUME                                     CAPACITY   ACCESSMODES   AGE
www-web-0   Bound     pvc-15c268c7-b507-11e6-932f-42010a800002   1Gi        RWO           48s
www-web-1   Bound     pvc-15c79307-b507-11e6-932f-42010a800002   1Gi        RWO           48s
```

StatefulSetコントローラーは、2つの{{< glossary_tooltip text="PersistentVolume" term_id="persistent-volume" >}}にバインドされた2つの{{< glossary_tooltip text="PersistentVolumeClaim" term_id="persistent-volume-claim" >}}を作成しています。

このチュートリアルで使用しているクラスターでは、PersistentVolumeの動的なプロビジョニングが設定されているため、PersistentVolumeが自動的に作成されてバインドされています。

デフォルトでは、NGINXウェブサーバーは`/usr/share/nginx/html/index.html`に置かれたindexファイルを配信します。StatefulSetの`spec`内の`volumeMounts`フィールドによって、`/usr/share/nginx/html`ディレクトリがPersistentVolume上にあることが保証されます。

Podのホスト名を`index.html`ファイルに書き込むことで、NGINXウェブサーバーがホスト名を配信することを検証しましょう。

```shell
for i in 0 1; do kubectl exec "web-$i" -- sh -c 'echo "$(hostname)" > /usr/share/nginx/html/index.html'; done

for i in 0 1; do kubectl exec -i -t "web-$i" -- curl http://localhost/; done
```
```
web-0
web-1
```

{{< note >}}
上記のcurlコマンドに対して代わりに**403 Forbidden**というレスポンスが返ってくる場合、`volumeMounts`でマウントしたディレクトリのパーミッションを修正する必要があります(これは、[hostPathボリュームを使用したときに起こるバグ](https://github.com/kubernetes/kubernetes/issues/2630)が原因です)。この問題に対処するには、上の`curl`コマンドを再実行する前に、次のコマンドを実行します。

`for i in 0 1; do kubectl exec web-$i -- chmod 755 /usr/share/nginx/html; done`
{{< /note >}}

1つ目のターミナルで、StatefulSetのPodを監視します。

```shell
kubectl get pod -w -l app=nginx
```

2つ目のターミナルで、StatefulSetのすべてのPodを削除します。

```shell
kubectl delete pod -l app=nginx
```
```
pod "web-0" deleted
pod "web-1" deleted
```
1つ目のターミナルで`kubectl get`コマンドの出力を確認して、すべてのPodがRunningかつReadyの状態に変わるまで待ちます。

```shell
kubectl get pod -w -l app=nginx
```
```
NAME      READY     STATUS              RESTARTS   AGE
web-0     0/1       ContainerCreating   0          0s
NAME      READY     STATUS    RESTARTS   AGE
web-0     1/1       Running   0          2s
web-1     0/1       Pending   0         0s
web-1     0/1       Pending   0         0s
web-1     0/1       ContainerCreating   0         0s
web-1     1/1       Running   0         34s
```

ウェブサーバーがホスト名を配信し続けていることを確認します。

```
for i in 0 1; do kubectl exec -i -t "web-$i" -- curl http://localhost/; done
```
```
web-0
web-1
```

もし`web-0`および`web-1`が再スケジュールされたとしても、Podは同じホスト名を配信し続けます。これは、PodのPersistentVolumeClaimに紐付けられたPersistentVolumeが、Podの`volumeMounts`に再マウントされるためです。`web-0`と`web-1`がどんなノードにスケジュールされたとしても、PodのPersistentVolumeは適切なマウントポイントにマウントされます。

## StatefulSetをスケールする

StatefulSetのスケールとは、レプリカ数を増減することを意味します。これは、`replicas`フィールドを更新することによって実現できます。StatefulSetのスケールには、[`kubectl scale`](/docs/reference/generated/kubectl/kubectl-commands/#scale)と
[`kubectl patch`](/docs/reference/generated/kubectl/kubectl-commands/#patch)のどちらも使用できます。

### スケールアップ

1つ目のターミナルで、StatefulSet内のPodを監視します。

```shell
kubectl get pods -w -l app=nginx
```

2つ目のターミナルで、`kubectl scale`を使って、レプリカ数を5にスケールします。

```shell
kubectl scale sts web --replicas=5
```
```
statefulset.apps/web scaled
```

1つ目のターミナルの`kubectl get`コマンドの出力を確認して、3つの追加のPodがRunningかつReadyの状態に変わるまで待ちます。

```shell
kubectl get pods -w -l app=nginx
```
```
NAME      READY     STATUS    RESTARTS   AGE
web-0     1/1       Running   0          2h
web-1     1/1       Running   0          2h
NAME      READY     STATUS    RESTARTS   AGE
web-2     0/1       Pending   0          0s
web-2     0/1       Pending   0         0s
web-2     0/1       ContainerCreating   0         0s
web-2     1/1       Running   0         19s
web-3     0/1       Pending   0         0s
web-3     0/1       Pending   0         0s
web-3     0/1       ContainerCreating   0         0s
web-3     1/1       Running   0         18s
web-4     0/1       Pending   0         0s
web-4     0/1       Pending   0         0s
web-4     0/1       ContainerCreating   0         0s
web-4     1/1       Running   0         19s
```

StatefulSetコントローラーはレプリカ数をスケールします。
[StatefulSetを作成する](#ordered-pod-creation)で説明したように、StatefulSetコントローラーは各Podを順序インデックスに従って1つずつ作成し、次のPodを起動する前に、1つ前のPodがRunningかつReadyの状態になるまで待ちます。

### スケールダウン {#scaling-down}

1つ目のターミナルで、StatefulSetのPodを監視します。

```shell
kubectl get pods -w -l app=nginx
```

2つ目のターミナルで、`kubectl patch`コマンドを使用して、StatefulSetを3つのレプリカにスケールダウンします。

```shell
kubectl patch sts web -p '{"spec":{"replicas":3}}'
```
```
statefulset.apps/web patched
```

`web-4`および`web-3`がTerminatingの状態になるまで待ちます。

```shell
kubectl get pods -w -l app=nginx
```
```
NAME      READY     STATUS              RESTARTS   AGE
web-0     1/1       Running             0          3h
web-1     1/1       Running             0          3h
web-2     1/1       Running             0          55s
web-3     1/1       Running             0          36s
web-4     0/1       ContainerCreating   0          18s
NAME      READY     STATUS    RESTARTS   AGE
web-4     1/1       Running   0          19s
web-4     1/1       Terminating   0         24s
web-4     1/1       Terminating   0         24s
web-3     1/1       Terminating   0         42s
web-3     1/1       Terminating   0         42s
```

### 順序付きPodを削除する

コントローラーは、順序インデックスの逆順に1度に1つのPodを削除し、次のPodを削除する前には、各Podが完全にシャットダウンするまで待機しています。

StatefulSetのPersistentVolumeClaimを取得しましょう。

```shell
kubectl get pvc -l app=nginx
```
```
NAME        STATUS    VOLUME                                     CAPACITY   ACCESSMODES   AGE
www-web-0   Bound     pvc-15c268c7-b507-11e6-932f-42010a800002   1Gi        RWO           13h
www-web-1   Bound     pvc-15c79307-b507-11e6-932f-42010a800002   1Gi        RWO           13h
www-web-2   Bound     pvc-e1125b27-b508-11e6-932f-42010a800002   1Gi        RWO           13h
www-web-3   Bound     pvc-e1176df6-b508-11e6-932f-42010a800002   1Gi        RWO           13h
www-web-4   Bound     pvc-e11bb5f8-b508-11e6-932f-42010a800002   1Gi        RWO           13h

```

まだ、5つのPersistentVolumeClaimと5つのPersistentVolumeが残っています。[安定したストレージへの書き込み](#writing-to-stable-storage)を読むと、StatefulSetのPodが削除されても、StatefulSetのPodにマウントされたPersistentVolumeは削除されないと書かれています。このことは、StatefulSetのスケールダウンによってPodが削除された場合にも当てはまります。

## StatefulSetsを更新する {#updating-statefulsets}

Kubernetes 1.7以降では、StatefulSetコントローラーは自動アップデートをサポートしています。使われる戦略は、StatefulSet APIオブジェクトの`spec.updateStrategy`フィールドによって決まります。この機能はコンテナイメージのアップグレード、リソースのrequestsやlimits、ラベル、StatefulSet内のPodのアノテーションの更新時に利用できます。有効なアップデートの戦略は、`RollingUpdate`と`OnDelete`の2種類です。

`RollingUpdate`は、StatefulSetのデフォルトのアップデート戦略です。

### RollingUpdate

`RollingUpdate`アップデート戦略は、StatefulSetの保証を尊重しながら、順序インデックスの逆順にStatefulSet内のすべてのPodをアップデートします。

`web`StatefulSetにpatchを当てて、`RollingUpdate`アップデート戦略を適用しましょう。

```shell
kubectl patch statefulset web -p '{"spec":{"updateStrategy":{"type":"RollingUpdate"}}}'
```
```
statefulset.apps/web patched
```

1つ目のターミナルで、`web`StatefulSetに再度patchを当てて、コンテナイメージを変更します。

```shell
kubectl patch statefulset web --type='json' -p='[{"op": "replace", "path": "/spec/template/spec/containers/0/image", "value":"gcr.io/google_containers/nginx-slim:0.8"}]'
```
```
statefulset.apps/web patched
```

2つ目のターミナルで、StatefulSet内のPodを監視します。

```shell
kubectl get pod -l app=nginx -w
```
出力は次のようになります。
```
NAME      READY     STATUS    RESTARTS   AGE
web-0     1/1       Running   0          7m
web-1     1/1       Running   0          7m
web-2     1/1       Running   0          8m
web-2     1/1       Terminating   0         8m
web-2     1/1       Terminating   0         8m
web-2     0/1       Terminating   0         8m
web-2     0/1       Terminating   0         8m
web-2     0/1       Terminating   0         8m
web-2     0/1       Terminating   0         8m
web-2     0/1       Pending   0         0s
web-2     0/1       Pending   0         0s
web-2     0/1       ContainerCreating   0         0s
web-2     1/1       Running   0         19s
web-1     1/1       Terminating   0         8m
web-1     0/1       Terminating   0         8m
web-1     0/1       Terminating   0         8m
web-1     0/1       Terminating   0         8m
web-1     0/1       Pending   0         0s
web-1     0/1       Pending   0         0s
web-1     0/1       ContainerCreating   0         0s
web-1     1/1       Running   0         6s
web-0     1/1       Terminating   0         7m
web-0     1/1       Terminating   0         7m
web-0     0/1       Terminating   0         7m
web-0     0/1       Terminating   0         7m
web-0     0/1       Terminating   0         7m
web-0     0/1       Terminating   0         7m
web-0     0/1       Pending   0         0s
web-0     0/1       Pending   0         0s
web-0     0/1       ContainerCreating   0         0s
web-0     1/1       Running   0         10s
```

StatefulSet内のPodは、順序インデックスの逆順に更新されました。StatefulSetコントローラーは各Podを終了させ、次のPodを更新する前に、新しいPodがRunningかつReadyの状態に変わるまで待機します。ここで、StatefulSetコントローラーは順序インデックスの前のPodがRunningかつReadyの状態になるまで次のPodの更新を始めず、現在の状態へのアップデートに失敗したPodがあった場合、そのPodをリストアすることに注意してください。

すでにアップデートを受け取ったPodは、アップデートされたバージョンにリストアされます。まだアップデートを受け取っていないPodは、前のバージョンにリストアされます。このような方法により、もし途中で失敗が起こっても、コントローラはアプリケーションが健全な状態を保ち続けられるようにし、更新が一貫したものになるようにします。

Podを取得して、コンテナイメージを確認してみましょう。

```shell
for p in 0 1 2; do kubectl get pod "web-$p" --template '{{range $i, $c := .spec.containers}}{{$c.image}}{{end}}'; echo; done
```
```
k8s.gcr.io/nginx-slim:0.8
k8s.gcr.io/nginx-slim:0.8
k8s.gcr.io/nginx-slim:0.8

```

現在、StatefulSet内のすべてのPodは、前のコンテナイメージを実行しています。

{{< note >}}
`kubectl rollout status sts/<name>`を使って、StatefulSetへのローリングアップデートの状態を確認することもできます。
{{< /note >}}

#### ステージングアップデート {#staging-an-update}

`RollingUpdate`アップデート戦略に`partition`パラメーターを使用すると、StatefulSetへのアップデートをステージングすることができます。ステージングアップデートを利用すれば、StatefulSet内のすべてのPodを現在のバージョンにしたまま、StatefulSetの`.spec.template`を変更することが可能になります。

`web`StatefulSetにpatchを当てて、`updateStrategy`フィールドにpartitionを追加しましょう。

```shell
kubectl patch statefulset web -p '{"spec":{"updateStrategy":{"type":"RollingUpdate","rollingUpdate":{"partition":3}}}}'
```
```
statefulset.apps/web patched
```

StatefulSetに再度patchを当てて、コンテナイメージを変更します。

```shell
kubectl patch statefulset web --type='json' -p='[{"op": "replace", "path": "/spec/template/spec/containers/0/image", "value":"k8s.gcr.io/nginx-slim:0.7"}]'
```
```
statefulset.apps/web patched
```

StatefulSet内のPodを削除します。

```shell
kubectl delete pod web-2
```
```
pod "web-2" deleted
```

PodがRunningかつReadyになるまで待ちます。

```shell
kubectl get pod -l app=nginx -w
```
```
NAME      READY     STATUS              RESTARTS   AGE
web-0     1/1       Running             0          4m
web-1     1/1       Running             0          4m
web-2     0/1       ContainerCreating   0          11s
web-2     1/1       Running   0         18s
```

Podのコンテナイメージを取得します。

```shell
kubectl get pod web-2 --template '{{range $i, $c := .spec.containers}}{{$c.image}}{{end}}'
```
```
k8s.gcr.io/nginx-slim:0.8
```

アップデート戦略が`RollingUpdate`であっても、StatefulSetが元のコンテナを持つPodをリストアしたことがわかります。これは、Podの順序インデックスが`updateStrategy`で指定した`partition`より小さいためです。

#### カナリア版をロールアウトする {#rolling-out-a-canary}

[ステージングアップデート](#staging-an-update)のときに指定した`partition`を小さくすることで、変更をテストするためのカナリア版をロールアウトできます。

StatefulSetにpatchを当てて、partitionを小さくします。

```shell
kubectl patch statefulset web -p '{"spec":{"updateStrategy":{"type":"RollingUpdate","rollingUpdate":{"partition":2}}}}'
```
```
statefulset.apps/web patched
```

`web-2`がRunningかつReadyの状態になるまで待ちます。

```shell
kubectl get pod -l app=nginx -w
```
```
NAME      READY     STATUS              RESTARTS   AGE
web-0     1/1       Running             0          4m
web-1     1/1       Running             0          4m
web-2     0/1       ContainerCreating   0          11s
web-2     1/1       Running   0         18s
```

Podのコンテナを取得します。

```shell
kubectl get pod web-2 --template '{{range $i, $c := .spec.containers}}{{$c.image}}{{end}}'
```
```
k8s.gcr.io/nginx-slim:0.7

```

`partition`を変更すると、StatefulSetコントローラーはPodを自動的に更新します。Podの順序インデックスが`partition`以上の値であるためです。

`web-1`Podを削除します。

```shell
kubectl delete pod web-1
```
```
pod "web-1" deleted
```

`web-1`PodがRunningかつReadyになるまで待ちます。

```shell
kubectl get pod -l app=nginx -w
```
出力は次のようになります。
```
NAME      READY     STATUS        RESTARTS   AGE
web-0     1/1       Running       0          6m
web-1     0/1       Terminating   0          6m
web-2     1/1       Running       0          2m
web-1     0/1       Terminating   0         6m
web-1     0/1       Terminating   0         6m
web-1     0/1       Terminating   0         6m
web-1     0/1       Pending   0         0s
web-1     0/1       Pending   0         0s
web-1     0/1       ContainerCreating   0         0s
web-1     1/1       Running   0         18s
```

`web-1`Podのコンテナイメージを取得します。

```shell
kubectl get pod web-1 --template '{{range $i, $c := .spec.containers}}{{$c.image}}{{end}}'
```
```
k8s.gcr.io/nginx-slim:0.8
```

Podの順序インデックスがpartitionよりも小さいため、`web-1`は元の設定のコンテナイメージにリストアされました。partitionを指定すると、StatefulSetの`.spec.template`が更新されたときに、順序インデックスがそれ以上の値を持つすべてのPodがアップデートされます。partitionよりも小さな順序インデックスを持つPodが削除されたり終了されたりすると、元の設定のPodにリストアされます。

#### フェーズロールアウト

[カナリア版](#rolling-out-a-canary)をロールアウトするのと同じような方法でパーティションされたローリングアップデートを使用すると、フェーズロールアウト(例: 線形、幾何級数的、指数関数的ロールアウト)を実行できます。フェーズロールアウトを実行するには、コントローラーがアップデートを途中で止めてほしい順序インデックスを`partition`に設定します。

現在、partitionは`2`に設定されています。partitionを`0`に設定します。

```shell
kubectl patch statefulset web -p '{"spec":{"updateStrategy":{"type":"RollingUpdate","rollingUpdate":{"partition":0}}}}'
```
```
statefulset.apps/web patched
```

StatefulSet内のすべてのPodがRunningかつReadyの状態になるまで待ちます。

```shell
kubectl get pod -l app=nginx -w
```
出力は次のようになります。
```
NAME      READY     STATUS              RESTARTS   AGE
web-0     1/1       Running             0          3m
web-1     0/1       ContainerCreating   0          11s
web-2     1/1       Running             0          2m
web-1     1/1       Running   0         18s
web-0     1/1       Terminating   0         3m
web-0     1/1       Terminating   0         3m
web-0     0/1       Terminating   0         3m
web-0     0/1       Terminating   0         3m
web-0     0/1       Terminating   0         3m
web-0     0/1       Terminating   0         3m
web-0     0/1       Pending   0         0s
web-0     0/1       Pending   0         0s
web-0     0/1       ContainerCreating   0         0s
web-0     1/1       Running   0         3s
```

StatefulSet内のPodのコンテナイメージの詳細を取得します。

```shell
for p in 0 1 2; do kubectl get pod "web-$p" --template '{{range $i, $c := .spec.containers}}{{$c.image}}{{end}}'; echo; done
```
```
k8s.gcr.io/nginx-slim:0.7
k8s.gcr.io/nginx-slim:0.7
k8s.gcr.io/nginx-slim:0.7
```

`partition`を`0`に移動することで、StatefulSetがアップデート処理を続けられるようにできます。

### OnDelete

`OnDelete`アップデート戦略は、(1.6以前の)レガシーな動作を実装しています。このアップデート戦略を選択すると、StatefulSetの`.spec.template`フィールドへ変更を加えても、StatefulSetコントローラーが自動的にPodを更新しなくなります。この戦略を選択するには、`.spec.template.updateStrategy.type`に`OnDelete`を設定します。

## StatefulSetを削除する

StatefulSetは、非カスケードな削除とカスケードな削除の両方をサポートしています。非カスケードな削除では、StatefulSetが削除されても、StatefulSet内のPodは削除されません。カスケードな削除では、StatefulSetとPodが一緒に削除されます。

### 非カスケードな削除

1つ目のターミナルで、StatefulSet内のPodを監視します

```
kubectl get pods -w -l app=nginx
```

[`kubectl delete`](/docs/reference/generated/kubectl/kubectl-commands/#delete)を使用して、StatefulSetを削除します。このとき、`--cascade=orphan`パラメーターをコマンドに与えてください。このパラメーターは、Kubernetesに対して、StatefulSetだけを削除して配下のPodは削除しないように指示します。

```shell
kubectl delete statefulset web --cascade=orphan
```
```
statefulset.apps "web" deleted
```

Podを取得して、ステータスを確認します。

```shell
kubectl get pods -l app=nginx
```
```
NAME      READY     STATUS    RESTARTS   AGE
web-0     1/1       Running   0          6m
web-1     1/1       Running   0          7m
web-2     1/1       Running   0          5m
```

`web`が削除されても、すべてのPodはまだRunningかつReadyの状態のままです。`web-0`を削除します。

```shell
kubectl delete pod web-0
```
```
pod "web-0" deleted
```

StatefulSetのPodを取得します。

```shell
kubectl get pods -l app=nginx
```
```
NAME      READY     STATUS    RESTARTS   AGE
web-1     1/1       Running   0          10m
web-2     1/1       Running   0          7m
```

`web`StatefulSetはすでに削除されているため、`web-0`は再起動しません。

1つ目のターミナルで、StatefulSetのPodを監視します。

```shell
kubectl get pods -w -l app=nginx
```

2つ目のターミナルで、StatefulSetを再作成します。もし`nginx`Serviceを削除しなかった場合(この場合は削除するべきではありませんでした)、Serviceがすでに存在することを示すエラーが表示されます。

```shell
kubectl apply -f web.yaml
```
```
statefulset.apps/web created
service/nginx unchanged
```

このエラーは無視してください。このメッセージは、すでに存在する _nginx_ というheadless Serviceを作成しようと試みたということを示しているだけです。

1つ目のターミナルで、`kubectl get`コマンドの出力を確認します。

```shell
kubectl get pods -w -l app=nginx
```
```
NAME      READY     STATUS    RESTARTS   AGE
web-1     1/1       Running   0          16m
web-2     1/1       Running   0          2m
NAME      READY     STATUS    RESTARTS   AGE
web-0     0/1       Pending   0          0s
web-0     0/1       Pending   0         0s
web-0     0/1       ContainerCreating   0         0s
web-0     1/1       Running   0         18s
web-2     1/1       Terminating   0         3m
web-2     0/1       Terminating   0         3m
web-2     0/1       Terminating   0         3m
web-2     0/1       Terminating   0         3m
```

 `web`StatefulSetが再作成されると、最初に`web-0`を再実行します。`web-1`はすでにRunningかつReadyの状態であるため、`web-0`がRunningかつReadyの状態に移行すると、StatefulSetは単純にこのPodを選びます。StatefulSetを`replicas`を2にして再作成したため、一度`web-0`が再作成されて、`web-1`がすでにRunningかつReadyの状態であることが判明したら、`web-2`は停止されます。

Podのウェブサーバーが配信している`index.html`ファイルのコンテンツをもう一度見てみましょう。

```shell
for i in 0 1; do kubectl exec -i -t "web-$i" -- curl http://localhost/; done
```
```
web-0
web-1
```

たとえStatefulSetと`web-0`Podの両方が削除されても、Podは最初に`index.html`ファイルに書き込んだホスト名をまだ配信しています。これは、StatefulSetがPodに紐付けられたPersistentVolumeを削除しないためです。StatefulSetを再作成して`web-0`を再実行すると、元のPersistentVolumeが再マウントされます。

### カスケードな削除

1つ目のターミナルで、StatefulSet内のPodを監視します。

```shell
kubectl get pods -w -l app=nginx
```

2つ目のターミナルで、StatefulSetをもう一度削除します。今回は、`--cascade=orphan`パラメーターを省略します。

```shell
kubectl delete statefulset web
```
```
statefulset.apps "web" deleted
```

1つ目のターミナルで実行している`kubectl get`コマンドの出力を確認し、すべてのPodがTerminatingの状態に変わるまで待ちます。

```shell
kubectl get pods -w -l app=nginx
```
```
NAME      READY     STATUS    RESTARTS   AGE
web-0     1/1       Running   0          11m
web-1     1/1       Running   0          27m
NAME      READY     STATUS        RESTARTS   AGE
web-0     1/1       Terminating   0          12m
web-1     1/1       Terminating   0         29m
web-0     0/1       Terminating   0         12m
web-0     0/1       Terminating   0         12m
web-0     0/1       Terminating   0         12m
web-1     0/1       Terminating   0         29m
web-1     0/1       Terminating   0         29m
web-1     0/1       Terminating   0         29m

```

[スケールダウン](#scaling-down)のセクションで見たように、順序インデックスの逆順に従って、Podは一度に1つずつ終了します。StatefulSetコントローラーは、次のPodを終了する前に、前のPodが完全に終了するまで待ちます。

{{< note >}}
カスケードな削除ではStatefulSetがPodとともに削除されますが、StatefulSetと紐付けられたheadless Serviceは削除されません。そのため、`nginx`Serviceは手動で削除する必要があります。
{{< /note >}}


```shell
kubectl delete service nginx
```
```
service "nginx" deleted
```

さらにもう一度、StatefulSetとheadless Serviceを再作成します。

```shell
kubectl apply -f web.yaml
```
```
service/nginx created
statefulset.apps/web created
```

StatefulSet上のすべてのPodがRunningかつReadyの状態に変わったら、Pod上の`index.html`ファイルのコンテンツを取得します。

```shell
for i in 0 1; do kubectl exec -i -t "web-$i" -- curl http://localhost/; done
```
```
web-0
web-1
```

StatefulSetを完全に削除して、すべてのPodが削除されたとしても、PersistentVolumeがマウントされたPodが再生成されて、`web-0`と`web-1`はホスト名の配信を続けます。

最後に、`web`StatefulSetを削除します。

```shell
kubectl delete service nginx
```
```
service "nginx" deleted
```
そして、`nginx`Serviceも削除します。
```shell
kubectl delete statefulset web
```
```
statefulset "web" deleted
```

## Pod管理ポリシー

分散システムによっては、StatefulSetの順序の保証が不必要であったり望ましくない場合もあります。こうしたシステムでは、一意性と同一性だけが求められます。この問題に対処するために、Kubernetes 1.7でStatefulSet APIオブジェクトに`.spec.podManagementPolicy`が導入されました。

### OrderedReadyのPod管理

`OrderedReady`のPod管理はStatefulSetのデフォルトの設定です。StatefulSetコントローラーに対して、これまでに紹介したような順序の保証を尊重するように指示します。

### ParallelのPod管理

`Parallel`のPod管理では、StatefulSetコントローラーに対して、PodがRunningかつReadyの状態や完全に停止するまで待たないように指示し、すべてのPodを並列に起動または停止させるようにします。

{{< codenew file="application/web/web-parallel.yaml" >}}

上の例をダウンロードして、`web-parallel.yaml`という名前でファイルに保存してください。

このマニフェストは、`.spec.podManagementPolicy`が`Parallel`に設定されている以外は、前にダウンロードした`web`StatefulSetと同一です。

1つ目のターミナルで、StatefulSet内のPodを監視します。

```shell
kubectl get pod -l app=nginx -w
```

2つ目のターミナルで、マニフェスト内のStatefulSetとServiceを作成します。

```shell
kubectl apply -f web-parallel.yaml
```
```
service/nginx created
statefulset.apps/web created
```

1つ目のターミナルで実行した`kubectl get`コマンドの出力を確認します。

```shell
kubectl get pod -l app=nginx -w
```
```
NAME      READY     STATUS    RESTARTS   AGE
web-0     0/1       Pending   0          0s
web-0     0/1       Pending   0         0s
web-1     0/1       Pending   0         0s
web-1     0/1       Pending   0         0s
web-0     0/1       ContainerCreating   0         0s
web-1     0/1       ContainerCreating   0         0s
web-0     1/1       Running   0         10s
web-1     1/1       Running   0         10s
```

StatefulSetコントローラーは`web-0`と`web-1`を同時に起動しています。

2つ目のターミナルで、StatefulSetをスケールしてみます。

```shell
kubectl scale statefulset/web --replicas=4
```
```
statefulset.apps/web scaled
```

`kubectl get`コマンドを実行しているターミナルの出力を確認します。

```
web-3     0/1       Pending   0         0s
web-3     0/1       Pending   0         0s
web-3     0/1       Pending   0         7s
web-3     0/1       ContainerCreating   0         7s
web-2     1/1       Running   0         10s
web-3     1/1       Running   0         26s
```

StatefulSetが2つのPodを実行し、1つ目のPodがRunningかつReadyの状態になるのを待たずに2つ目のPodを実行しているのがわかります。

## {{% heading "cleanup" %}}

2つのターミナルが開かれているはずなので、クリーンアップの一部として`kubectl`コマンドを実行する準備ができています。

```shell
kubectl delete sts web
# stsは、statefulsetの略です。
```

`kubectl get`を監視すると、Podが削除されていく様子を確認できます。

```shell
kubectl get pod -l app=nginx -w
```
```
web-3     1/1       Terminating   0         9m
web-2     1/1       Terminating   0         9m
web-3     1/1       Terminating   0         9m
web-2     1/1       Terminating   0         9m
web-1     1/1       Terminating   0         44m
web-0     1/1       Terminating   0         44m
web-0     0/1       Terminating   0         44m
web-3     0/1       Terminating   0         9m
web-2     0/1       Terminating   0         9m
web-1     0/1       Terminating   0         44m
web-0     0/1       Terminating   0         44m
web-2     0/1       Terminating   0         9m
web-2     0/1       Terminating   0         9m
web-2     0/1       Terminating   0         9m
web-1     0/1       Terminating   0         44m
web-1     0/1       Terminating   0         44m
web-1     0/1       Terminating   0         44m
web-0     0/1       Terminating   0         44m
web-0     0/1       Terminating   0         44m
web-0     0/1       Terminating   0         44m
web-3     0/1       Terminating   0         9m
web-3     0/1       Terminating   0         9m
web-3     0/1       Terminating   0         9m
```

削除の間、StatefulSetはすべてのPodを並列に削除し、順序インデックスが1つ前のPodが停止するのを待つことはありません。

`kubectl get`コマンドを実行しているターミナルを閉じて、`nginx`Serviceを削除します。

```shell
kubectl delete svc nginx
```

{{< note >}}
このチュートリアルで使用したPersistentVolumeのための永続ストレージも削除する必要があります。

すべてのストレージが再利用できるようにするために、環境、ストレージの設定、プロビジョニング方法に基づいて必要な手順に従ってください。
{{< /note >}}
