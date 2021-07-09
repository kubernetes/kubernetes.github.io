---
reviewers:
title: リソースクォータ
content_type: concept
weight: 10
---

<!-- overview -->

複数のユーザーやチームが決められた数のノードを持つクラスターを共有しているとき、1つのチームが公平に使えるリソース量を超えて使用するといった問題が出てきます。

リソースクォータはこの問題に対処するための管理者向けツールです。



<!-- body -->

`ResourceQuota`オブジェクトによって定義されるリソースクォータは、名前空間ごとの総リソース消費を制限するための制約を提供します。リソースクォータは同じ名前空間のクラスター内でタイプごとに作成できるオブジェクト数や、名前空間内のリソースによって消費されるコンピュートリソースの総量を制限できます。

リソースクォータは下記のように働きます。

- 異なる名前空間で異なるチームが存在するとき。現時点ではこれは自主的なものですが、将来的にはACLsを介してリソースクォータの設定を強制するように計画されています。
- 管理者は各名前空間で1つの`ResourceQuota`を作成します。
- ユーザーが名前空間内でリソース(Pod、Serviceなど)を作成し、クォータシステムが`ResourceQuota`によって定義されたハードリソースリミットを超えないことを保証するために、リソースの使用量をトラッキングします。
- リソースの作成や更新がクォータの制約に違反しているとき、そのリクエストはHTTPステータスコード`403 FORBIDDEN`で失敗し、違反した制約を説明するメッセージが表示されます。
- `cpu`や`memory`といったコンピューターリソースに対するクォータが名前空間内で有効になっているとき、ユーザーはそれらの値に対する`requests`や`limits`を設定する必要があります。設定しないとクォータシステムがPodの作成を拒否します。 ヒント: コンピュートリソースの要求を設定しないPodに対してデフォルト値を強制するために、`LimitRanger`アドミッションコントローラーを使用してください。この問題を解決する例は[walkthrough](/docs/tasks/administer-cluster/manage-resources/quota-memory-cpu-namespace/)で参照できます。

ResourceQuotaのオブジェクト名は、有効な[DNSサブドメイン名](/ja/docs/concepts/overview/working-with-objects/names#dns-subdomain-names)である必要があります.

名前空間とクォータを使用して作成できるポリシーの例は以下の通りです。

- 32GiB RAM、16コアのキャパシティーを持つクラスターで、Aチームに20GiB、10コアを割り当て、Bチームに10GiB、4コアを割り当て、将来の割り当てのために2GiB、2コアを予約しておく。
- "testing"という名前空間に対して1コア、1GiB RAMの使用制限をかけ、"production"という名前空間には制限をかけない。

クラスターの総キャパシティーが、その名前空間のクォータの合計より少ない場合、リソースの競合が発生する場合があります。このとき、リソースの先着順で処理されます。

リソースの競合もクォータの変更も、作成済みのリソースには影響しません。

## リソースクォータを有効にする

多くのKubernetesディストリビューションにおいてリソースクォータはデフォルトで有効になっています。APIサーバーで`--enable-admission-plugins=`の値に`ResourceQuota`が含まれるときに有効になります。

特定の名前空間にResourceQuotaがあるとき、そのリソースクォータはその名前空間に適用されます。

## リソースクォータの計算

特定の名前空間において、[コンピュートリソース](/ja/docs/concepts/configuration/manage-resources-containers/)の合計に上限を設定できます。

下記のリソースタイプがサポートされています。


| リソース名 | 説明 |
| --------------------- | ----------------------------------------------------------- |
| `limits.cpu` | 停止していない状態の全てのPodで、CPUリミットの合計がこの値を超えることができません。 |
| `limits.memory` | 停止していない状態の全てのPodで、メモリーの合計がこの値を超えることができません。 |
| `requests.cpu` | 停止していない状態の全てのPodで、CPUリクエストの合計がこの値を超えることができません。 |
| `requests.memory` | 停止していない状態の全てのPodで、メモリーリクエストの合計がこの値を超えることができません。 |
| `hugepages-<size>` | 停止していない状態の全てのPodで, 指定されたサイズのHuge Pageリクエスト数がこの値を超えることができません。 |
| `cpu` | `requests.cpu`と同じ。 |
| `memory` | `requests.memory`と同じ。 |

### 拡張リソースのためのリソースクォータ

上記で取り上げたリソースに加えて、Kubernetes v1.10において、[拡張リソース](/ja/docs/concepts/configuration/manage-resources-containers/#extended-resources)のためのリソースクォータのサポートが追加されました。

拡張リソースに対するオーバーコミットが禁止されているのと同様に、リソースクォータで拡張リソース用に`requests`と`limits`の両方を指定しても意味がありません。現在、拡張リソースに対しては`requests.`というプレフィックスのついたクォータアイテムのみ設定できます。

GPUリソースを例にすると、もしリソース名が`nvidia.com/gpu`で、ユーザーが名前空間内でリクエストされるGPUの上限を4に指定するとき、下記のようにリソースクォータを定義します。

* `requests.nvidia.com/gpu: 4`

さらなる詳細は[クォータの確認と設定](#viewing-and-setting-quotas)を参照してください。


## ストレージのリソースクォータ

特定の名前空間において[ストレージリソース](/ja/docs/concepts/storage/persistent-volumes/)の総数に上限をかけることができます。

さらに、関連するストレージクラスに基づいて、ストレージリソースの消費量に上限をかけることもできます。

| リソース名 | 説明 |
| --------------------- | ----------------------------------------------------------- |
| `requests.storage` | 全てのPersistentVolumeClaimにおいて、ストレージのリクエストの合計がこの値を超えないようにします。 |
| `persistentvolumeclaims` | 特定の名前空間内で作成可能な[PersistentVolumeClaim](/ja/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims)の総数。 |
| `<storage-class-name>.storageclass.storage.k8s.io/requests.storage` | ストレージクラス名`<storage-class-name>`に関連する全てのPersistentVolumeClaimにおいて、ストレージリクエストの合計がこの値を超えないようにします。 |
| `<storage-class-name>.storageclass.storage.k8s.io/persistentvolumeclaims` | ストレージクラス名`<storage-class-name>`に関連する全てのPersistentVolumeClaimにおいて、特定の名前空間内で作成可能な[PersistentVolumeClaim](/ja/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims)の総数。 |

例えば、もし管理者が`gold`ストレージクラスを`bronze`ストレージクラスと分けてリソースクォータを設定するとき、管理者はリソースクォータを下記のように指定できます。

* `gold.storageclass.storage.k8s.io/requests.storage: 500Gi`
* `bronze.storageclass.storage.k8s.io/requests.storage: 100Gi`

Kubernetes v1.8において、ローカルのエフェメラルストレージに対するリソースクォータのサポートがα版の機能として追加されました。

| リソース名 | 説明 |
| ------------------------------- |----------------------------------------------------------- |
| `requests.ephemeral-storage` | 名前空間内の全てのPodで、ローカルのエフェメラルストレージのリクエストの合計がこの値を超えないようにします。 |
| `limits.ephemeral-storage` | 名前空間内の全てのPodで、ローカルのエフェメラルストレージのリミットの合計がこの値を超えないようにします。 |
| `ephemeral-storage` | `requests.ephemeral-storage`と同じ。 |

## オブジェクト数に対するクォータ

下記のシンタックスを使用して、名前空間に紐づいた全ての標準であるリソースタイプの中の特定のリソースの総数に対するリソースクォータを設定できます。

* `count/<resource>.<group>` コアでないグループのリソース用
* `count/<resource>` コアグループのリソース用

オブジェクト数に対するクォータでユーザーが設定するリソースの例は下記の通りです。

* `count/persistentvolumeclaims`
* `count/services`
* `count/secrets`
* `count/configmaps`
* `count/replicationcontrollers`
* `count/deployments.apps`
* `count/replicasets.apps`
* `count/statefulsets.apps`
* `count/jobs.batch`
* `count/cronjobs.batch`

カスタムリソースに対して同じシンタックスを使用できます。例えば、`example.com`というAPIグループ内の`widgets`というカスタムリソースのリソースクォータを設定するには`count/widgets.example.com`と記述します。

`count/*`リソースクォータの使用において、オブジェクトがサーバーストレージに存在するときオブジェクトはクォータの計算対象となります。このようなタイプのリソースクォータはストレージリソース浪費の防止に有効です。例えば、もしSecretが大量に存在するとき、そのSecretリソースの総数に対してリソースクォータの制限をかけたい場合です。クラスター内でSecretが大量にあると、サーバーとコントローラーの起動を妨げることになります。適切に設定されていないCronJobから保護するためにジョブのクォータを設定できます。名前空間内で大量のJobを作成するCronJobは、サービスを利用不可能にする可能性があります。

また、限定されたリソースのセットにおいて汎用オブジェクトカウントのリソースクォータを実行可能です。

下記のタイプのリソースがサポートされています。

| リソース名 | 説明 |
| ------------------------------- | ------------------------------------------------- |
| `configmaps` | 名前空間内で存在可能なConfigMapの総数。  |
| `persistentvolumeclaims` | 名前空間内で存在可能な[PersistentVolumeClaim](/ja/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims)の総数。 |
| `pods` | 名前空間内で存在可能な停止していないPodの総数。`.status.phase in (Failed, Succeeded)`がtrueのとき、Podは停止状態にあります。  |
| `replicationcontrollers` | 名前空間内で存在可能なReplicationControlerの総数。 |
| `resourcequotas` | 名前空間内で存在可能なResourceQuotaの総数。 |
| `services` | 名前空間内で存在可能なServiceの総数。 |
| `services.loadbalancers` | 名前空間内で存在可能なtype:LoadBalancerであるServiceの総数。 |
| `services.nodeports` | 名前空間内で存在可能なtype:NodePortであるServiceの総数。 |
| `secrets` | 名前空間内で存在可能なSecretの総数。 |

例えば、`pods`のリソースクォータは`Pod`の総数をカウントし、特定の名前空間内で作成された`Pod`の総数の最大数を設定します。またユーザーが多くのPodを作成し、クラスターのPodのIPが枯渇する状況を避けるために`pods`のリソースクォータを名前空間に設定したい場合があります。

## クォータのスコープについて

各リソースクォータには関連する`scope`のセットを関連づけることができます。クォータは、列挙されたscopeの共通部分と一致する場合にのみリソースの使用量を計測します。

スコープがクォータに追加されると、サポートするリソースの数がスコープに関連するリソースに制限されます。許可されたセット以外のクォータ上でリソースを指定するとバリデーションエラーになります。

| スコープ | 説明 |
| ----- | ----------- |
| `Terminating` | `.spec.activeDeadlineSeconds >= 0`であるPodに一致します。 |
| `NotTerminating` | `.spec.activeDeadlineSecondsがnil`であるPodに一致します。 |
| `BestEffort` | ベストエフォート型のサービス品質のPodに一致します。 |
| `NotBestEffort` | ベストエフォート型のサービス品質でないPodに一致します。 |
| `PriorityClass` | 指定された[優先度クラス](/docs/concepts/configuration/pod-priority-preemption)と関連付いているPodに一致します。 |

`BestEffort`スコープはリソースクォータを次のリソースに対するトラッキングのみに制限します:

* `pods`

`Terminating`、`NotTerminating`、`NotBestEffort`、`PriorityClass`スコープは、リソースクォータを次のリソースに対するトラッキングのみに制限します:

* `pods`
* `cpu`
* `memory`
* `requests.cpu`
* `requests.memory`
* `limits.cpu`
* `limits.memory`

同じクォータで`Terminating`と`NotTerminating`の両方のスコープを指定することはできず、また同じクォータで`BestEffort`と`NotBestEffort`の両方のスコープを指定することもできないことに注意してください。

`scopeSelector`は`operator` フィールドにおいて下記の値をサポートしています。:

* `In`
* `NotIn`
* `Exists`
* `DoesNotExist`

`scopeSelector`の定義において`scopeName`に下記のいずれかの値を使用する場合、`operator`に`Exists`を指定してください。 

* `Terminating`
* `NotTerminating`
* `BestEffort`
* `NotBestEffort`

`operator`が`In`または`NotIn`の場合、`values`フィールドには少なくとも1つの値が必要です。例えば以下のように記述します：

```yaml
  scopeSelector:
    matchExpressions:
      - scopeName: PriorityClass
        operator: In
        values:
          - middle
```

`operator`が`Exists`または`DoesNotExist`の場合、`values`フィールドは指定*しないでください*。

### PriorityClass毎のリソースクォータ

{{< feature-state for_k8s_version="v1.17" state="stable" >}}

Podは特定の[優先度](/ja/docs/concepts/configuration/pod-priority-preemption/#pod-priority)で作成されます。リソースクォータのSpec内にある`scopeSelector`フィールドを使用して、Podの優先度に基づいてPodのシステムリソースの消費をコントロールできます。

リソースクォータのSpec内の`scopeSelector`によってPodが選択されたときのみ、そのリソースクォータが一致し、消費されます。

リソースクォータが`scopeSelector`フィールドを使用して優先度クラスに対してスコープされる場合、リソースクォータのオプジェクトは、次のリソースのみトラッキングするように制限されます:

* `pods`
* `cpu`
* `memory`
* `ephemeral-storage`
* `limits.cpu`
* `limits.memory`
* `limits.ephemeral-storage`
* `requests.cpu`
* `requests.memory`
* `requests.ephemeral-storage`

この例ではリソースクォータのオブジェクトを作成し、特定の優先度を持つPodに一致させます。この例は下記のように動作します。

- クラスター内のPodは"low"、"medium"、"high"の3つの優先度クラスのうち1つをもちます。
- 1つのリソースクォータのオブジェクトは優先度毎に作成されます。

下記のYAMLを`quota.yml`というファイルに保存します。

```yaml
apiVersion: v1
kind: List
items:
- apiVersion: v1
  kind: ResourceQuota
  metadata:
    name: pods-high
  spec:
    hard:
      cpu: "1000"
      memory: 200Gi
      pods: "10"
    scopeSelector:
      matchExpressions:
      - operator : In
        scopeName: PriorityClass
        values: ["high"]
- apiVersion: v1
  kind: ResourceQuota
  metadata:
    name: pods-medium
  spec:
    hard:
      cpu: "10"
      memory: 20Gi
      pods: "10"
    scopeSelector:
      matchExpressions:
      - operator : In
        scopeName: PriorityClass
        values: ["medium"]
- apiVersion: v1
  kind: ResourceQuota
  metadata:
    name: pods-low
  spec:
    hard:
      cpu: "5"
      memory: 10Gi
      pods: "10"
    scopeSelector:
      matchExpressions:
      - operator : In
        scopeName: PriorityClass
        values: ["low"]
```

`kubectl create`を実行してYAMLの内容を適用します。

```shell
kubectl create -f ./quota.yml
```

```
resourcequota/pods-high created
resourcequota/pods-medium created
resourcequota/pods-low created
```

`kubectl describe quota`を実行して`Used`クォータが`0`であることを確認します。

```shell
kubectl describe quota
```

```
Name:       pods-high
Namespace:  default
Resource    Used  Hard
--------    ----  ----
cpu         0     1k
memory      0     200Gi
pods        0     10


Name:       pods-low
Namespace:  default
Resource    Used  Hard
--------    ----  ----
cpu         0     5
memory      0     10Gi
pods        0     10


Name:       pods-medium
Namespace:  default
Resource    Used  Hard
--------    ----  ----
cpu         0     10
memory      0     20Gi
pods        0     10
```

プライオリティーが"high"であるPodを作成します。下記の内容を`high-priority-pod.yml`というファイルに保存します。

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: high-priority
spec:
  containers:
  - name: high-priority
    image: ubuntu
    command: ["/bin/sh"]
    args: ["-c", "while true; do echo hello; sleep 10;done"]
    resources:
      requests:
        memory: "10Gi"
        cpu: "500m"
      limits:
        memory: "10Gi"
        cpu: "500m"
  priorityClassName: high
```

`kubectl create`でマニフェストを適用します。

```shell
kubectl create -f ./high-priority-pod.yml
```

`pods-high`という名前のプライオリティーが"high"のクォータにおける"Used"項目の値が変更され、それ以外の2つの値は変更されていないことを確認してください。

```shell
kubectl describe quota
```

```
Name:       pods-high
Namespace:  default
Resource    Used  Hard
--------    ----  ----
cpu         500m  1k
memory      10Gi  200Gi
pods        1     10


Name:       pods-low
Namespace:  default
Resource    Used  Hard
--------    ----  ----
cpu         0     5
memory      0     10Gi
pods        0     10


Name:       pods-medium
Namespace:  default
Resource    Used  Hard
--------    ----  ----
cpu         0     10
memory      0     20Gi
pods        0     10
```

## リクエスト vs リミット

コンピュートリソースを分配する際に、各コンテナはCPUとメモリーそれぞれのリクエストとリミット値を指定します。クォータはそれぞれの値を設定できます。

クォータに`requests.cpu`や`requests.memory`の値が指定されている場合は、コンテナはそれらのリソースに対する明示的な要求を行います。同様に、クォータに`limits.cpu`や`limits.memory`の値が指定されている場合は、コンテナはそれらのリソースに対する明示的な制限を行います。

## クォータの確認と設定 {#viewing-and-setting-quotas}

kubectlでは、クォータの作成、更新、確認をサポートしています。

```shell
kubectl create namespace myspace
```

```shell
cat <<EOF > compute-resources.yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: compute-resources
spec:
  hard:
    requests.cpu: "1"
    requests.memory: 1Gi
    limits.cpu: "2"
    limits.memory: 2Gi
    requests.nvidia.com/gpu: 4
EOF
```

```shell
kubectl create -f ./compute-resources.yaml --namespace=myspace
```

```shell
cat <<EOF > object-counts.yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: object-counts
spec:
  hard:
    configmaps: "10"
    persistentvolumeclaims: "4"
    pods: "4"
    replicationcontrollers: "20"
    secrets: "10"
    services: "10"
    services.loadbalancers: "2"
EOF
```

```shell
kubectl create -f ./object-counts.yaml --namespace=myspace
```

```shell
kubectl get quota --namespace=myspace
```

```
NAME                    AGE
compute-resources       30s
object-counts           32s
```

```shell
kubectl describe quota compute-resources --namespace=myspace
```

```
Name:                    compute-resources
Namespace:               myspace
Resource                 Used  Hard
--------                 ----  ----
limits.cpu               0     2
limits.memory            0     2Gi
requests.cpu             0     1
requests.memory          0     1Gi
requests.nvidia.com/gpu  0     4
```

```shell
kubectl describe quota object-counts --namespace=myspace
```

```
Name:                   object-counts
Namespace:              myspace
Resource                Used    Hard
--------                ----    ----
configmaps              0       10
persistentvolumeclaims  0       4
pods                    0       4
replicationcontrollers  0       20
secrets                 1       10
services                0       10
services.loadbalancers  0       2
```

また、kubectlは`count/<resource>.<group>`というシンタックスを用いることにより、名前空間に依存した全ての主要なリソースに対するオブジェクト数のクォータをサポートしています。

```shell
kubectl create namespace myspace
```

```shell
kubectl create quota test --hard=count/deployments.apps=2,count/replicasets.apps=4,count/pods=3,count/secrets=4 --namespace=myspace
```

```shell
kubectl create deployment nginx --image=nginx --namespace=myspace --replicas=2
```

```shell
kubectl describe quota --namespace=myspace
```

```
Name:                         test
Namespace:                    myspace
Resource                      Used  Hard
--------                      ----  ----
count/deployments.apps        1     2
count/pods                    2     3
count/replicasets.apps        1     4
count/secrets                 1     4
```

## クォータとクラスター容量

ResourceQuotaはクラスター容量に依存しません。またユニット数の絶対値で表されます。そのためクラスターにノードを追加したことにより、各名前空間が自動的により多くのリソースを消費するような機能が提供されるわけでは*ありません*。

下記のようなより複雑なポリシーが必要な状況があります。

- 複数チーム間でクラスターリソースの総量を分けあう。
- 各テナントが必要な時にリソース使用量を増やせるようにするが、偶発的なリソースの枯渇を防ぐために上限を設定する。
- 1つの名前空間に対してリソース消費の需要を検出し、ノードを追加し、クォータを増加させる。

このようなポリシーは、クォータの使用量の監視と、他のシグナルにしたがってクォータのハードの制限を調整する"コントローラー"を記述することにより、ResourceQuotaをビルディングブロックのように使用して実装できます。

リソースクォータは集約されたクラスターリソースを分割しますが、ノードに対しては何の制限も行わないことに注意して下さい。例: 複数の名前空間のPodは同一のノード上で稼働する可能性があります。

## デフォルトで優先度クラスの消費を制限する {#limit-priority-class-consumption-by-default}

例えば"cluster-services"のように、条件に一致するクォータオブジェクトが存在する場合に限り、特定の優先度のPodを名前空間で許可することが望ましい場合があります。

このメカニズムにより、オペレーターは特定の高優先度クラスの使用を限られた数の名前空間に制限することができ、全ての名前空間でこれらの優先度クラスをデフォルトで使用することはできなくなります。

これを実施するには、`kube-apiserver`の`--admission-control-config-file`というフラグを使い、下記の設定ファイルに対してパスを渡す必要がります。

```yaml
apiVersion: apiserver.config.k8s.io/v1
kind: AdmissionConfiguration
plugins:
- name: "ResourceQuota"
  configuration:
    apiVersion: apiserver.config.k8s.io/v1
    kind: ResourceQuotaConfiguration
    limitedResources:
    - resource: pods
      matchScopes:
      - scopeName: PriorityClass
        operator: In
        values: ["cluster-services"]
```

なお、"cluster-services"Podは、条件に一致する`scopeSelector`を持つクォータオブジェクトが存在する名前空間でのみ許可されます。

```yaml
    scopeSelector:
      matchExpressions:
      - scopeName: PriorityClass
        operator: In
        values: ["cluster-services"]
```

## {{% heading "whatsnext" %}}

- さらなる情報は[クォータの design doc](https://git.k8s.io/community/contributors/design-proposals/resource-management/admission_control_resource_quota.md)を参照してください。
- [リソースクォータの使用方法の例](/docs/tasks/administer-cluster/quota-api-object/)を参照してください。
- [優先度クラスに対するクォータサポートの design doc](https://github.com/kubernetes/community/blob/master/contributors/design-proposals/scheduling/pod-priority-resourcequota.md)を参照してください。
- [LimitedResources](https://github.com/kubernetes/kubernetes/pull/36765)を参照してください。
