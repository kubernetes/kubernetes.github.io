---
title: ガベージコレクション
content_type: concept
weight: 60
---

<!-- overview -->

Kubernetesのガベージコレクターの役割は、かつてオーナーがいたが、現時点でもはやオーナーがいないようなオブジェクトの削除を行うことです。



<!-- body -->

## オーナーとその従属オブジェクト {#owners-and-dependents}

いくつかのKubernetesオブジェクトは他のオブジェクトのオーナーとなります。例えば、ReplicaSetはPodのセットに対するオーナーです。オーナーによって所有されたオブジェクトは、オーナーオブジェクトの*従属オブジェクト(Dependents)* と呼ばれます。全ての従属オブジェクトは、オーナーオブジェクトを指し示す`metadata.ownerReferences`というフィールドを持ちます。

時々、Kubernetesは`ownerReference`フィールドに値を自動的にセットします。例えば、ユーザーがReplicaSetを作成したとき、KubernetesはReplicaSet内の各Podの`ownerReference`フィールドに自動的に値をセットします。Kubernetes1.8において、KubernetesはReplicaController、ReplicaSet、StatefulSet、DaemonSet、Deployment、Job、CronJobによって作成され、適用されたオブジェクトの`ownerReference`フィールドに自動的にその値をセットします。

ユーザーはまた`ownerReference`フィールドに手動で値をセットすることにより、オーナーと従属オブジェクト間の関係を指定することができます。

下記の例は、3つのPodを持つReplicaSetの設定ファイルとなります。

{{< codenew file="controllers/replicaset.yaml" >}}

もしユーザーがReplicaSetを作成し、Podのメタデータを見る時、`ownerReference`フィールドの値を確認できます。

```shell
kubectl apply -f https://k8s.io/examples/controllers/replicaset.yaml
kubectl get pods --output=yaml
```

その出力結果によると、そのPodのオーナーは`my-repset`という名前のReplicaSetです。

```yaml
apiVersion: v1
kind: Pod
metadata:
  ...
  ownerReferences:
  - apiVersion: apps/v1
    controller: true
    blockOwnerDeletion: true
    kind: ReplicaSet
    name: my-repset
    uid: d9607e19-f88f-11e6-a518-42010a800195
  ...
```

{{< note >}}
ネームスペースをまたいだownerReferenceは意図的に許可されていません。これは以下のことを意味します。  
1) ネームスペース内のスコープの従属オブジェクトは、同一のネームスペース内のオーナーと、クラスターのスコープ内のオーナーのみ指定できます。  
2) クラスターのスコープ内の従属オブジェクトは、クラスターのスコープ内のオーナーオブジェクトのみ指定でき、ネームスペース内のスコープのオーナーオブジェクトは指定できません。
{{< /note >}}

## ガベージコレクターがどのように従属オブジェクトの削除をするかを制御する

ユーザーがオブジェクトを削除するとき、それに紐づく従属オブジェクトも自動で削除するか指定できます。従属オブジェクトの自動削除は、*カスケード削除(Cascading deletion)* と呼ばれます。*カスケード削除* には2つのモードがあり、*バックグラウンド* と*フォアグラウンド* があります。

もしユーザーが、従属オブジェクトの自動削除なしにあるオブジェクトを削除する場合、その従属オブジェクトは*みなしご(orphaned)* と呼ばれます。

### フォアグラウンドのカスケード削除

*フォアグラウンドのカスケード削除* において、そのルートオブジェクトは最初に"削除処理中"という状態に遷移します。その*削除処理中* 状態において、下記の項目は正となります。

 * そのオブジェクトはREST APIを介して確認可能です。
 * そのオブジェクトの`deletionTimestamp`がセットされます。
 * そのオブジェクトの`metadata.finalizers`フィールドは、`foregroundDeletion`という値を含みます。

一度"削除処理中"状態に遷移すると、そのガベージコレクターはオブジェクトの従属オブジェクトを削除します。一度そのガベージコレクターが全ての”ブロッキングしている”従属オブジェクトを削除すると(`ownerReference.blockOwnerDeletion=true`という値を持つオブジェクト)、それはオーナーのオブジェクトも削除します。

注意点として、"フォアグラウンドのカスケード削除"において、`ownerReference.blockOwnerDeletion=true`フィールドを持つ従属オブジェクトのみ、そのオーナーオブジェクトの削除をブロックします。
Kubernetes1.7では、認証されていない従属オブジェクトがオーナーオブジェクトの削除を遅らせることができないようにするために[アドミッションコントローラー](/docs/reference/access-authn-authz/admission-controllers/#ownerreferencespermissionenforcement)が追加され、それは、オーナーオブジェクトの削除パーミッションに基づいて`blockOwnerDeletion`の値がtrueに設定してユーザーアクセスをコントロールします。

もしオブジェクトの`ownerReferences`フィールドがコントローラー(DeploymentやReplicaSetなど)によってセットされている場合、`blockOwnerDeletion`は自動的にセットされ、ユーザーはこのフィールドを手動で修正する必要はありません。

### バックグラウンドのカスケード削除

*バックグラウンドのカスケード削除* において、Kubernetesはそのオーナーオブジェクトを即座に削除し、ガベージコレクションはその従属オブジェクトをバックグラウンドで削除します。

### カスケード削除ポリシーの設定

カスケード削除ポリシーを制御するためには、オブジェクトをいつ設定するか`deleteOptions`引数上の`propagationPolicy`フィールドに設定してください。設定可能な値は`Orphan`、`Foreground`、もしくは`Background`のどれかです。


下記のコマンドは従属オブジェクトをバックグラウンドで削除する例です。

```shell
kubectl proxy --port=8080
curl -X DELETE localhost:8080/apis/apps/v1/namespaces/default/replicasets/my-repset \
  -d '{"kind":"DeleteOptions","apiVersion":"v1","propagationPolicy":"Background"}' \
  -H "Content-Type: application/json"
```

下記のコマンドは従属オブジェクトをフォアグラウンドで削除する例です。

```shell
kubectl proxy --port=8080
curl -X DELETE localhost:8080/apis/apps/v1/namespaces/default/replicasets/my-repset \
  -d '{"kind":"DeleteOptions","apiVersion":"v1","propagationPolicy":"Foreground"}' \
  -H "Content-Type: application/json"
```

下記のコマンドは従属オブジェクトをみなしご状態になった従属オブジェクトの例です。

```shell
kubectl proxy --port=8080
curl -X DELETE localhost:8080/apis/apps/v1/namespaces/default/replicasets/my-repset \
  -d '{"kind":"DeleteOptions","apiVersion":"v1","propagationPolicy":"Orphan"}' \
  -H "Content-Type: application/json"
```

kubectlもまたカスケード削除をサポートしています。  
kubectlを使って従属オブジェクトを自動的に削除するためには、`--cascade`をtrueにセットしてください。
従属オブジェクトを削除せず、みなしご状態にするには`--cascade`をfalseにセットしてください。
`--cascade`オプションのデフォルト値はtrueになります。

下記のコマンドは、ReplicaSetを削除し、その従属オブジェクトをみなしご状態にします。

```shell
kubectl delete replicaset my-repset --cascade=orphan
```

### Deploymentsに関する追記事項

Kubernetes1.7以前では、Deploymentに対するカスケード削除において、作成されたReplicaSetだけでなく、それらのPodも削除するためには、ユーザーは`propagationPolicy: Foreground`と指定*しなくてはなりません* 。もしこのタイプの*propagationPolicy*が使われなかった場合、そのReplicaSetは削除されますが、そのPodは削除されずみなしご状態になります。  
さらなる詳細に関しては[kubeadm/#149](https://github.com/kubernetes/kubeadm/issues/149#issuecomment-284766613)を参照してください。

## 既知の問題について

[#26120](https://github.com/kubernetes/kubernetes/issues/26120)にてイシューがトラックされています。




## {{% heading "whatsnext" %}}


[Design Doc 1](https://git.k8s.io/community/contributors/design-proposals/api-machinery/garbage-collection.md)

[Design Doc 2](https://git.k8s.io/community/contributors/design-proposals/api-machinery/synchronous-garbage-collection.md)





