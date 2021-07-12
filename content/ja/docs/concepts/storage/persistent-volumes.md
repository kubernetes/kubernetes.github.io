---
title: 永続ボリューム
feature:
  title: ストレージオーケストレーション
  description: >
    ローカルストレージや<a href="https://cloud.google.com/storage/">GCP</a>、<a href="https://aws.amazon.com/products/storage/">AWS</a>などのパブリッククラウドプロバイダー、もしくはNFS、iSCSI、Gluster、Ceph、Cinder、Flockerのようなネットワークストレージシステムの中から選択されたものを自動的にマウントします。

content_type: concept
weight: 20
---

<!-- overview -->

このドキュメントではKubernetesの _PersistentVolume_ について説明します。[ボリューム](/docs/concepts/storage/volumes/)を一読することをおすすめします。




<!-- body -->

## 概要

ストレージを管理することはインスタンスを管理することとは全くの別物です。PersistentVolumeサブシステムは、ストレージが何から提供されているか、どのように消費されているかをユーザーと管理者から抽象化するAPIを提供します。これを実現するためのPersistentVolumeとPersistentVolumeClaimという2つの新しいAPIリソースを紹介します。

_PersistentVolume_ (PV)は[ストレージクラス](/docs/concepts/storage/storage-classes/)を使って管理者もしくは動的にプロビジョニングされるクラスターのストレージの一部です。これはNodeと同じようにクラスターリソースの一部です。PVはVolumeのようなボリュームプラグインですが、PVを使う個別のPodとは独立したライフサイクルを持っています。このAPIオブジェクトはNFS、iSCSIやクラウドプロバイダー固有のストレージシステムの実装の詳細を捕捉します。

_PersistentVolumeClaim_ (PVC)はユーザーによって要求されるストレージです。これはPodと似ています。PodはNodeリソースを消費し、PVCはPVリソースを消費します。Podは特定レベルのCPUとメモリーリソースを要求することができます。クレームは特定のサイズやアクセスモード(例えば、ReadWriteOnce、ReadOnlyMany、ReadWriteManyにマウントできます。詳しくは[アクセスモード](#access-modes)を参照してください)を要求することができます。

PersistentVolumeClaimはユーザーに抽象化されたストレージリソースの消費を許可する一方、ユーザーは色々な問題に対処するためにパフォーマンスといった様々なプロパティを持ったPersistentVolumeを必要とすることは一般的なことです。クラスター管理者はユーザーに様々なボリュームがどのように実装されているかを表に出すことなく、サイズやアクセスモードだけではない色々な点で異なった、様々なPersistentVolumeを提供できる必要があります。これらのニーズに応えるために _StorageClass_ リソースがあります。

[実例を含む詳細なチュートリアル](/docs/tasks/configure-pod-container/configure-persistent-volume-storage/)を参照して下さい。


## ボリュームと要求のライフサイクル

PVはクラスター内のリソースです。PVCはこれらのリソースの要求でありまた、クレームのチェックとしても機能します。PVとPVCの相互作用はこのライフサイクルに従います。

### プロビジョニング

PVは静的か動的どちらかでプロビジョニングされます。

#### 静的

クラスター管理者は多数のPVを作成します。それらはクラスターのユーザーが使うことのできる実際のストレージの詳細を保持します。それらはKubernetes APIに存在し、利用できます。

#### 動的

ユーザーのPersistentVolumeClaimが管理者の作成したいずれの静的PVにも一致しない場合、クラスターはPVC用にボリュームを動的にプロビジョニングしようとする場合があります。
このプロビジョニングはStorageClassに基づいています。PVCは[ストレージクラス](/docs/concepts/storage/storage-classes/)の要求が必要であり、管理者は動的プロビジョニングを行うためにストレージクラスの作成・設定が必要です。ストレージクラスを""にしたストレージ要求は、自身の動的プロビジョニングを事実上無効にします。

ストレージクラスに基づいたストレージの動的プロビジョニングを有効化するには、クラスター管理者が`DefaultStorageClass`[アドミッションコントローラー](/docs/reference/access-authn-authz/admission-controllers/#defaultstorageclass)をAPIサーバーで有効化する必要があります。
これは例えば、`DefaultStorageClass`がAPIサーバーコンポーネントの`--enable-admission-plugins`フラグのコンマ区切りの順序付きリストの中に含まれているかで確認できます。
APIサーバーのコマンドラインフラグの詳細については[kube-apiserver](/docs/admin/kube-apiserver/)のドキュメントを参照してください。

### バインディング

ユーザは、特定のサイズのストレージとアクセスモードを指定した上でPersistentVolumeClaimを作成します（動的プロビジョニングの場合は、すでに作られています）。マスター内のコントロールループは、新しく作られるPVCをウォッチして、それにマッチするPVが見つかったときに、それらを紐付けます。PVが新しいPVC用に動的プロビジョニングされた場合、コントロールループは常にPVをそのPVCに紐付けます。そうでない場合、ユーザーは常に少なくとも要求したサイズ以上のボリュームを取得しますが、ボリュームは要求されたサイズを超えている可能性があります。一度紐付けされると、どのように紐付けられたかに関係なくPersistentVolumeClaimの紐付けは排他的（決められた特定のPVとしか結びつかない状態）になります。PVCからPVへの紐付けは、PersistentVolumeとPersistentVolumeClaim間の双方向の紐付けであるClaimRefを使用した1対1のマッピングになっています。

一致するボリュームが存在しない場合、クレームはいつまでも紐付けされないままになります。一致するボリュームが利用可能になると、クレームがバインドされます。たとえば、50GiのPVがいくつもプロビジョニングされているクラスターだとしても、100Giを要求するPVCとは一致しません。100GiのPVがクラスターに追加されると、PVCを紐付けできます。

### 使用

Podは要求をボリュームとして使用します。クラスターは、要求を検査して紐付けられたボリュームを見つけそのボリュームをPodにマウントします。複数のアクセスモードをサポートするボリュームの場合、ユーザーはPodのボリュームとしてクレームを使う時にどのモードを希望するかを指定します。

ユーザーがクレームを取得し、そのクレームがバインドされると、バインドされたPVは必要な限りそのユーザーに属します。ユーザーはPodをスケジュールし、Podのvolumesブロックに`persistentVolumeClaim`を含めることで、バインドされたクレームのPVにアクセスします。
[書式の詳細はこちらを確認して下さい。](#claims-as-volumes)

### 使用中のストレージオブジェクトの保護

使用中のストレージオブジェクト保護機能の目的はデータ損失を防ぐために、Podによって実際に使用されている永続ボリュームクレーム(PVC)と、PVCにバインドされている永続ボリューム(PV)がシステムから削除されないようにすることです。

{{< note >}}
PVCを使用しているPodオブジェクトが存在する場合、PVCはPodによって実際に使用されています。
{{< /note >}}

ユーザーがPodによって実際に使用されているPVCを削除しても、そのPVCはすぐには削除されません。PVCの削除は、PVCがPodで使用されなくなるまで延期されます。また、管理者がPVCに紐付けられているPVを削除しても、PVはすぐには削除されません。PVがPVCに紐付けられなくなるまで、PVの削除は延期されます。

PVCの削除が保護されているかは、PVCのステータスが`Terminating`になっていて、そして`Finalizers`のリストに`kubernetes.io/pvc-protection`が含まれているかで確認できます。

```shell
kubectl describe pvc hostpath
Name:          hostpath
Namespace:     default
StorageClass:  example-hostpath
Status:        Terminating
Volume:
Labels:        <none>
Annotations:   volume.beta.kubernetes.io/storage-class=example-hostpath
               volume.beta.kubernetes.io/storage-provisioner=example.com/hostpath
Finalizers:    [kubernetes.io/pvc-protection]
```

同様にPVの削除が保護されているかは、PVのステータスが`Terminating`になっていて、そして`Finalizers`のリストに`kubernetes.io/pv-protection`が含まれているかで確認できます。

```shell
kubectl describe pv task-pv-volume
Name:            task-pv-volume
Labels:          type=local
Annotations:     <none>
Finalizers:      [kubernetes.io/pv-protection]
StorageClass:    standard
Status:          Terminating
Claim:
Reclaim Policy:  Delete
Access Modes:    RWO
Capacity:        1Gi
Message:
Source:
    Type:          HostPath (bare host directory volume)
    Path:          /tmp/data
    HostPathType:
Events:            <none>
```

### 再クレーム

ユーザーは、ボリュームの使用が完了したら、リソースの再クレームを許可するAPIからPVCオブジェクトを削除できます。PersistentVolumeの再クレームポリシーはそのクレームが解放された後のボリュームの処理をクラスターに指示します。現在、ボリュームは保持、リサイクル、または削除できます。

#### 保持

`Retain`という再クレームポリシーはリソースを手動で再クレームすることができます。PersistentVolumeClaimが削除される時、PersistentVolumeは依然として存在はしますが、ボリュームは解放済みです。ただし、以前のクレームデータはボリューム上に残っているため、別のクレームにはまだ使用できません。管理者は次の手順でボリュームを手動で再クレームできます。

1. PersistentVolumeを削除します。PVが削除された後も、外部インフラストラクチャー(AWS EBS、GCE PD、Azure Disk、Cinderボリュームなど)に関連付けられたストレージアセットは依然として残ります。
1. ストレージアセットに関連するのデータを手動で適切にクリーンアップします。
1. 関連するストレージアセットを手動で削除するか、同じストレージアセットを再利用したい場合、新しいストレージアセット定義と共にPersistentVolumeを作成します。

#### 削除

`Delete`再クレームポリシーをサポートするボリュームプラグインの場合、削除するとPersistentVolumeオブジェクトがKubernetesから削除されるだけでなく、AWS EBS、GCE PD、Azure Disk、Cinderボリュームなどの外部インフラストラクチャーの関連ストレージアセットも削除されます。動的にプロビジョニングされたボリュームは、[StorageClassの再クレームポリシー](#reclaim-policy)を継承します。これはデフォルトで削除です。管理者は、ユーザーの需要に応じてStorageClassを構成する必要があります。そうでない場合、PVは作成後に編集またはパッチを適用する必要があります。[PersistentVolumeの再クレームポリシーの変更](/docs/tasks/administer-cluster/change-pv-reclaim-policy/)を参照してください。

#### リサイクル

{{< warning >}}
`Recycle`再クレームポリシーは非推奨になりました。代わりに、動的プロビジョニングを使用することをおすすめします。
{{< /warning >}}

基盤となるボリュームプラグインでサポートされている場合、`Recycle`再クレームポリシーはボリュームに対して基本的な削除(`rm -rf /thevolume/*`)を実行し、新しいクレームに対して再び利用できるようにします。

管理者は[reference](/docs/reference/command-line-tools-reference/kube-controller-manager/)で説明するように、Kubernetesコントローラーマネージャーのコマンドライン引数を使用して、カスタムリサイクラーPodテンプレートを構成できます。カスタムリサイクラーPodテンプレートには、次の例に示すように、`volumes`仕様が含まれている必要があります。



```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pv-recycler
  namespace: default
spec:
  restartPolicy: Never
  volumes:
  - name: vol
    hostPath:
      path: /any/path/it/will/be/replaced
  containers:
  - name: pv-recycler
    image: "k8s.gcr.io/busybox"
    command: ["/bin/sh", "-c", "test -e /scrub && rm -rf /scrub/..?* /scrub/.[!.]* /scrub/*  && test -z \"$(ls -A /scrub)\" || exit 1"]
    volumeMounts:
    - name: vol
      mountPath: /scrub
```
ただし、カスタムリサイクラーPodテンプレートの`volumes`パート内で指定された特定のパスは、リサイクルされるボリュームの特定のパスに置き換えられます。

### 永続ボリュームの予約

コントロールプレーンは、永続ボリュームクレームをクラスター内の一致する永続ボリュームに[バインド](#バインディング)できます。
ただし、永続ボリュームクレームを特定の永続ボリュームにバインドする場合、それらを事前にバインドする必要があります。

永続ボリュームクレームで永続ボリュームを指定することにより、その特定の永続ボリュームと永続ボリュームクレームの間のバインディングを宣言します。
永続ボリュームが存在し、その`claimRef`フィールドで永続ボリュームクレームを予約していない場合に永続ボリュームと永続ボリュームクレームがバインドされます。

バインディングは、ノードアフィニティを含むいくつかのボリュームの一致基準に関係なく発生します。
コントロールプレーンは、依然として[ストレージクラス](/docs/concepts/storage/storage-classes/)、アクセスモード、および要求されたストレージサイズが有効であることをチェックします。

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: foo-pvc
  namespace: foo
spec:
  storageClassName: "" # 空の文字列を明示的に指定する必要があります。そうしないとデフォルトのストレージクラスが設定されてしまいます。
  volumeName: foo-pv
  ...
```

この方法は、永続ボリュームへのバインド特権を保証するものではありません。
他の永続ボリュームクレームが指定した永続ボリュームを使用できる場合、最初にそのストレージボリュームを予約する必要があります。
永続ボリュームの`claimRef`フィールドに関連する永続ボリュームクレームを指定して、他の永続ボリュームクレームがその永続ボリュームにバインドできないようにしてください。


```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: foo-pv
spec:
  storageClassName: ""
  claimRef:
    name: foo-pvc
    namespace: foo
  ...
```

これは、既存の永続ボリュームを再利用する場合など、`claimPolicy`が`Retain`に設定されている永続ボリュームを使用する場合に役立ちます。

### 永続ボリュームクレームの拡大

{{< feature-state for_k8s_version="v1.11" state="beta" >}}

PersistentVolumeClaim(PVC)の拡大はデフォルトで有効です。次のボリュームの種類で拡大できます。

* gcePersistentDisk
* awsElasticBlockStore
* Cinder
* glusterfs
* rbd
* Azure File
* Azure Disk
* Portworx
* FlexVolumes
* CSI

そのストレージクラスの`allowVolumeExpansion`フィールドがtrueとなっている場合のみ、PVCを拡大できます。


``` yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: gluster-vol-default
provisioner: kubernetes.io/glusterfs
parameters:
  resturl: "http://192.168.10.100:8080"
  restuser: ""
  secretNamespace: ""
  secretName: ""
allowVolumeExpansion: true
```

PVCに対してさらに大きなボリュームを要求するには、PVCオブジェクトを編集してより大きなサイズを指定します。これによりPersistentVolumeを受け持つ基盤にボリュームの拡大がトリガーされます。クレームを満たすため新しくPersistentVolumeが作成されることはありません。代わりに既存のボリュームがリサイズされます。

#### CSIボリュームの拡張

{{< feature-state for_k8s_version="v1.16" state="beta" >}}

CSIボリュームの拡張のサポートはデフォルトで有効になっていますが、ボリューム拡張をサポートするにはボリューム拡張を利用できるCSIドライバーも必要です。詳細については、それぞれのCSIドライバーのドキュメントを参照してください。

#### ファイルシステムを含むボリュームのリサイズ

ファイルシステムがXFS、Ext3、またはExt4の場合にのみ、ファイルシステムを含むボリュームのサイズを変更できます。

ボリュームにファイルシステムが含まれる場合、新しいPodが`PersistentVolumeClaim`でReadWriteモードを使用している場合にのみ、ファイルシステムのサイズが変更されます。ファイルシステムの拡張は、Podの起動時、もしくはPodの実行時で基盤となるファイルシステムがオンラインの拡張をサポートする場合に行われます。

FlexVolumesでは、ドライバの`RequiresFSResize`機能がtrueに設定されている場合、サイズを変更できます。
FlexVolumeは、Podの再起動時にサイズ変更できます。

#### 使用中の永続ボリュームクレームのリサイズ

{{< feature-state for_k8s_version="v1.15" state="beta" >}}

{{< note >}}
使用中のPVCの拡張は、Kubernetes 1.15以降のベータ版と、1.11以降のアルファ版として利用可能です。`ExpandInUsePersistentVolume`機能を有効化する必要があります。これはベータ機能のため多くのクラスターで自動的に行われます。詳細については、[フィーチャーゲート](/docs/reference/command-line-tools-reference/feature-gates/)のドキュメントを参照してください。
{{< /note >}}

この場合、既存のPVCを使用しているPodまたはDeploymentを削除して再作成する必要はありません。使用中のPVCは、ファイルシステムが拡張されるとすぐにPodで自動的に使用可能になります。この機能は、PodまたはDeploymentで使用されていないPVCには影響しません。拡張を完了する前に、PVCを使用するPodを作成する必要があります。

他のボリュームタイプと同様、FlexVolumeボリュームは、Podによって使用されている最中でも拡張できます。

{{< note >}}
FlexVolumeのリサイズは、基盤となるドライバーがリサイズをサポートしている場合のみ可能です。
{{< /note >}}

{{< note >}}
EBSの拡張は時間がかかる操作です。また変更は、ボリュームごとに6時間に1回までというクォータもあります。
{{< /note >}}

#### ボリューム拡張時の障害からの復旧

基盤ストレージの拡張に失敗した際には、クラスターの管理者はPersistent Volume Claim (PVC)の状態を手動で復旧し、リサイズ要求をキャンセルします。それをしない限り、リサイズ要求は管理者の介入なしにコントローラーによって継続的に再試行されます。  

1. PersistentVolumeClaim(PVC)にバインドされているPersistentVolume(PV)を`Retain`再クレームポリシーとしてマークします。
2. PVCを削除します。PVは`Retain`再クレームポリシーを持っているため、PVCを再び作成したときにいかなるデータも失うことはありません。  
3. `claimRef`エントリーをPVスペックから削除して、新しいPVCがそれにバインドできるようにします。これによりPVは`Available`になります。  
4. PVより小さいサイズでPVCを再作成し、PVCの`volumeName`フィールドをPVの名前に設定します。これにより新しいPVCを既存のPVにバインドします。  
5. PVを再クレームポリシーを復旧することを忘れずに行ってください。  

## 永続ボリュームの種類

PersistentVolumeの種類はプラグインとして実装されます。Kubernetesは現在次のプラグインに対応しています。

* [`awsElasticBlockStore`](/docs/concepts/storage/volumes/#awselasticblockstore) - AWS Elastic Block Store (EBS)
* [`azureDisk`](/docs/concepts/storage/volumes/#azuredisk) - Azure Disk
* [`azureFile`](/docs/concepts/storage/volumes/#azurefile) - Azure File
* [`cephfs`](/docs/concepts/storage/volumes/#cephfs) - CephFS volume
* [`cinder`](/docs/concepts/storage/volumes/#cinder) - Cinder (OpenStack block storage)
  (**非推奨**)
* [`csi`](/docs/concepts/storage/volumes/#csi) - Container Storage Interface (CSI)
* [`fc`](/docs/concepts/storage/volumes/#fc) - Fibre Channel (FC) storage
* [`flexVolume`](/docs/concepts/storage/volumes/#flexVolume) - FlexVolume
* [`flocker`](/docs/concepts/storage/volumes/#flocker) - Flocker storage
* [`gcePersistentDisk`](/docs/concepts/storage/volumes/#gcepersistentdisk) - GCE Persistent Disk
* [`glusterfs`](/docs/concepts/storage/volumes/#glusterfs) - Glusterfs volume
* [`hostPath`](/docs/concepts/storage/volumes/#hostpath) - HostPath volume
  (テスト用の単一ノードのみ。マルチノードクラスターでは動作しません。代わりに`local`ボリュームを利用することを検討してください。)
* [`iscsi`](/docs/concepts/storage/volumes/#iscsi) - iSCSI (SCSI over IP) storage
* [`local`](/docs/concepts/storage/volumes/#local) - ノードにマウントされたローカルストレージデバイス
* [`nfs`](/docs/concepts/storage/volumes/#nfs) - Network File System (NFS) storage
* `photonPersistentDisk` - Photon controller persistent disk
  (対応するクラウドプロバイダーが削除されたため、このボリュームタイプは機能しなくなりました。)
* [`portworxVolume`](/docs/concepts/storage/volumes/#portworxvolume) - Portworx volume
* [`quobyte`](/docs/concepts/storage/volumes/#quobyte) - Quobyte volume
* [`rbd`](/docs/concepts/storage/volumes/#rbd) - Rados Block Device (RBD) volume
* [`scaleIO`](/docs/concepts/storage/volumes/#scaleio) - ScaleIO volume
  (**非推奨**)
* [`storageos`](/docs/concepts/storage/volumes/#storageos) - StorageOS volume
* [`vsphereVolume`](/docs/concepts/storage/volumes/#vspherevolume) - vSphere VMDK volume

## 永続ボリューム

各PVには、仕様とボリュームのステータスが含まれているspecとstatusが含まれています。
PersistentVolumeオブジェクトの名前は、有効な
[DNSサブドメイン名](/ja/docs/concepts/overview/working-with-objects/names#dns-subdomain-names)である必要があります。

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv0003
spec:
  capacity:
    storage: 5Gi
  volumeMode: Filesystem
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Recycle
  storageClassName: slow
  mountOptions:
    - hard
    - nfsvers=4.1
  nfs:
    path: /tmp
    server: 172.17.0.2
```

{{< note >}}
クラスター内でPersistentVolumeを使用するには、ボリュームタイプに関連するヘルパープログラムが必要な場合があります。
この例では、PersistentVolumeはNFSタイプで、NFSファイルシステムのマウントをサポートするためにヘルパープログラム`/sbin/mount.nfs`が必要になります。
{{< /note >}}

### 容量

通常、PVには特定のストレージ容量があります。これはPVの`capacity`属性を使用して設定されます。容量によって期待される単位を理解するためには、Kubernetesの[リソースモデル](https://git.k8s.io/community/contributors/design-proposals/scheduling/resources.md)を参照してください。

現在、設定または要求できるのはストレージサイズのみです。将来の属性には、IOPS、スループットなどが含まれます。

### ボリュームモード

{{< feature-state for_k8s_version="v1.18" state="stable" >}}

KubernetesはPersistentVolumesの2つの`volumeModes`をサポートしています: `Filesystem`と`Block`です。  
`volumeMode`は任意のAPIパラメーターです。  
`Filesystem`は`volumeMode`パラメーターが省略されたときに使用されるデフォルトのモードです。  

`volumeMode: Filesystem`であるボリュームはPodに*マウント*されてディレクトリになります。 ボリュームがブロックデバイスでデバイスが空の時、Kubernetesは初めてそれにマウントされる前にデバイスのファイルシステムを作成します。  

`volumeMode`の値を`Block`に設定してボリュームをRAWブロックデバイスとして使用します。  
このようなボリュームは、ファイルシステムを持たないブロックデバイスとしてPodに提示されます。  
このモードは、Podとボリュームの間のファイルシステムレイヤなしにボリュームにアクセスする可能な限り最速の方法をPodに提供するのに便利です。一方で、Pod上で実行しているアプリケーションはRAWブロックデバイスの扱い方を知っていなければなりません。  
Pod内で`volumeMode: Block`とともにボリュームを使用する例としては、[Raw Block Volume Support](#raw-block-volume-support)を参照してください。

### アクセスモード

PersistentVolumeは、リソースプロバイダーがサポートする方法でホストにマウントできます。次の表に示すように、プロバイダーにはさまざまな機能があり、各PVのアクセスモードは、その特定のボリュームでサポートされる特定のモードに設定されます。たとえば、NFSは複数の読み取り/書き込みクライアントをサポートできますが、特定のNFSのPVはサーバー上で読み取り専用としてエクスポートされる場合があります。各PVは、その特定のPVの機能を記述する独自のアクセスモードのセットを取得します。

アクセスモードは次の通りです。

* ReadWriteOnce –ボリュームは単一のNodeで読み取り/書き込みとしてマウントできます
* ReadOnlyMany –ボリュームは多数のNodeで読み取り専用としてマウントできます
* ReadWriteMany –ボリュームは多数のNodeで読み取り/書き込みとしてマウントできます

CLIではアクセスモードは次のように略されます。

* RWO - ReadWriteOnce
* ROX - ReadOnlyMany
* RWX - ReadWriteMany


> __Important!__ ボリュームは、多数のモードをサポートしていても、一度に1つのアクセスモードでしかマウントできません。たとえば、GCEPersistentDiskは、単一NodeではReadWriteOnceとして、または多数のNodeではReadOnlyManyとしてマウントできますが、同時にマウントすることはできません。


| ボリュームプラグイン | ReadWriteOnce    | ReadOnlyMany     | ReadWriteMany                   |
| :---                 | :---:            | :---:            | :---:                           |
| AWSElasticBlockStore | &#x2713;         | -                | -                               |
| AzureFile            | &#x2713;         | &#x2713;         | &#x2713;                        |
| AzureDisk            | &#x2713;         | -                | -                               |
| CephFS               | &#x2713;         | &#x2713;         | &#x2713;                        |
| Cinder               | &#x2713;         | -                | -                               |
| CSI                  | ドライバーに依存 | ドライバーに依存 | ドライバーに依存                |
| FC                   | &#x2713;         | &#x2713;         | -                               |
| FlexVolume           | &#x2713;         | &#x2713;         | ドライバーに依存                |
| Flocker              | &#x2713;         | -                | -                               |
| GCEPersistentDisk    | &#x2713;         | &#x2713;         | -                               |
| Glusterfs            | &#x2713;         | &#x2713;         | &#x2713;                        |
| HostPath             | &#x2713;         | -                | -                               |
| iSCSI                | &#x2713;         | &#x2713;         | -                               |
| Quobyte              | &#x2713;         | &#x2713;         | &#x2713;                        |
| NFS                  | &#x2713;         | &#x2713;         | &#x2713;                        |
| RBD                  | &#x2713;         | &#x2713;         | -                               |
| VsphereVolume        | &#x2713;         | -                | - (Podが連結されている場合のみ) |
| PortworxVolume       | &#x2713;         | -                | &#x2713;                        |
| ScaleIO              | &#x2713;         | &#x2713;         | -                               |
| StorageOS            | &#x2713;         | -                | -                               |

### Class

PVはクラスを持つことができます。これは`storageClassName`属性を[ストレージクラス](/docs/concepts/storage/storage-classes/)の名前に設定することで指定されます。特定のクラスのPVは、そのクラスを要求するPVCにのみバインドできます。`storageClassName`にクラスがないPVは、特定のクラスを要求しないPVCにのみバインドできます。

以前`volume.beta.kubernetes.io/storage-class`アノテーションは、`storageClassName`属性の代わりに使用されていました。このアノテーションはまだ機能しています。ただし、将来のKubernetesリリースでは完全に非推奨です。

### 再クレームポリシー {#reclaim-policy}

現在の再クレームポリシーは次のとおりです。

* 保持 -- 手動再クレーム
* リサイクル -- 基本的な削除 (`rm -rf /thevolume/*`)
* 削除 -- AWS EBS、GCE PD、Azure Disk、もしくはOpenStack Cinderボリュームに関連するストレージアセットを削除

現在、NFSとHostPathのみがリサイクルをサポートしています。AWS EBS、GCE PD、Azure Disk、およびCinder volumeは削除をサポートしています。

### マウントオプション

Kubernetes管理者は永続ボリュームがNodeにマウントされるときの追加マウントオプションを指定できます。

{{< note >}}
すべての永続ボリュームタイプがすべてのマウントオプションをサポートするわけではありません。
{{< /note >}}

次のボリュームタイプがマウントオプションをサポートしています。

* AWSElasticBlockStore
* AzureDisk
* AzureFile
* CephFS
* Cinder (OpenStackブロックストレージ)
* GCEPersistentDisk
* Glusterfs
* NFS
* Quobyte Volumes
* RBD (Ceph Block Device)
* StorageOS
* VsphereVolume
* iSCSI

マウントオプションは検証されないため、不正だった場合マウントは失敗します。

以前`volume.beta.kubernetes.io/mount-options`アノテーションが`mountOptions`属性の代わりに使われていました。このアノテーションはまだ機能しています。ただし、将来のKubernetesリリースでは完全に非推奨です。

### ノードアフィニティ

{{< note >}}
ほとんどのボリュームタイプはこのフィールドを設定する必要がありません。[AWS EBS](/docs/concepts/storage/volumes/#awselasticblockstore)、[GCE PD](/docs/concepts/storage/volumes/#gcepersistentdisk)、もしくは[Azure Disk](/docs/concepts/storage/volumes/#azuredisk)ボリュームブロックタイプの場合自動的に設定されます。[local](/docs/concepts/storage/volumes/#local)ボリュームは明示的に設定する必要があります。
{{< /note >}}

PVは[ノードアフィニティ](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#volumenodeaffinity-v1-core)を指定して、このボリュームにアクセスできるNodeを制限する制約を定義できます。PVを使用するPodは、ノードアフィニティによって選択されたNodeにのみスケジュールされます。

### フェーズ

ボリュームは次のフェーズのいずれかです。

* 利用可能 -- まだクレームに紐付いていない自由なリソース
* バウンド -- クレームに紐付いている
* リリース済み -- クレームが削除されたが、クラスターにまだクレームされている
* 失敗 -- 自動再クレームに失敗

CLIにはPVに紐付いているPVCの名前が表示されます。

## 永続ボリューム要求 {#persistentvolumeclaims}

各PVCにはspecとステータスが含まれます。これは、仕様とクレームのステータスです。

PersistentVolumeClaimオブジェクトの名前は、有効な
[DNSサブドメイン名](/ja/docs/concepts/overview/working-with-objects/names#dns-subdomain-names)である必要があります。

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: myclaim
spec:
  accessModes:
    - ReadWriteOnce
  volumeMode: Filesystem
  resources:
    requests:
      storage: 8Gi
  storageClassName: slow
  selector:
    matchLabels:
      release: "stable"
    matchExpressions:
      - {key: environment, operator: In, values: [dev]}
```

### アクセスモード

クレームは、特定のアクセスモードでストレージを要求するときにボリュームと同じ規則を使用します。

### ボリュームモード

クレームは、ボリュームと同じ規則を使用して、ファイルシステムまたはブロックデバイスとしてのボリュームの消費を示します。

### リソース

Podと同様に、クレームは特定の量のリソースを要求できます。この場合、要求はストレージ用です。同じ[リソースモデル](https://git.k8s.io/community/contributors/design-proposals/scheduling/resources.md)がボリュームとクレームの両方に適用されます。

### セレクター

クレームでは、[ラベルセレクター](/ja/docs/concepts/overview/working-with-objects/labels/#label-selectors)を指定して、ボリュームセットをさらにフィルター処理できます。ラベルがセレクターに一致するボリュームのみがクレームにバインドできます。セレクターは2つのフィールドで構成できます。

* `matchLabels` - ボリュームはこの値のラベルが必要です
* `matchExpressions` - キー、値のリスト、およびキーと値を関連付ける演算子を指定することによって作成された要件のリスト。有効な演算子は、In、NotIn、ExistsおよびDoesNotExistです。

`matchLabels`と`matchExpressions`の両方からのすべての要件はANDで結合されます。一致するには、すべてが一致する必要があります。

### クラス

クレームは、`storageClassName`属性を使用して[ストレージクラス](/docs/concepts/storage/storage-classes/)の名前を指定することにより、特定のクラスを要求できます。PVCにバインドできるのは、PVCと同じ`storageClassName`を持つ、要求されたクラスのPVのみです。

PVCは必ずしもクラスをリクエストする必要はありません。`storageClassName`が`""`に設定されているPVCは、クラスのないPVを要求していると常に解釈されるため、クラスのないPVにのみバインドできます（アノテーションがないか、`""`に等しい1つのセット）。`storageClassName`のないPVCはまったく同じではなく、[`DefaultStorageClass`アドミッションプラグイン](/docs/reference/access-authn-authz/admission-controllers/#defaultstorageclass)がオンになっているかどうかによって、クラスターによって異なる方法で処理されます。

* アドミッションプラグインがオンになっている場合、管理者はデフォルトの`StorageClass`を指定できます。`storageClassName`を持たないすべてのPVCは、そのデフォルトのPVにのみバインドできます。デフォルトの`StorageClass`の指定は、`StorageClass`オブジェクトで`storageclass.kubernetes.io/is-default-class`アノテーションを`true`に設定することにより行われます。管理者がデフォルトを指定しない場合、クラスターは、アドミッションプラグインがオフになっているかのようにPVC作成をレスポンスします。複数のデフォルトが指定されている場合、アドミッションプラグインはすべてのPVCの作成を禁止します。
* アドミッションプラグインがオフになっている場合、デフォルトの`StorageClass`の概念はありません。`storageClassName`を持たないすべてのPVCは、クラスを持たないPVにのみバインドできます。この場合、storageClassNameを持たないPVCは、`storageClassName`が`""`に設定されているPVCと同じように扱われます。

インストール方法によっては、インストール時にアドオンマネージャーによってデフォルトのストレージクラスがKubernetesクラスターにデプロイされる場合があります。

PVCが`selector`を要求することに加えて`StorageClass`を指定する場合、要件はANDで一緒に結合されます。要求されたクラスのPVと要求されたラベルのみがPVCにバインドされます。

{{< note >}}
現在、`selector`が空ではないPVCは、PVを動的にプロビジョニングできません。
{{< /note >}}

以前は、`storageClassName`属性の代わりに`volume.beta.kubernetes.io/storage-class`アノテーションが使用されていました。このアノテーションはまだ機能しています。ただし、今後のKubernetesリリースではサポートされません。

## ボリュームとしてのクレーム

Podは、クレームをボリュームとして使用してストレージにアクセスします。クレームは、そのクレームを使用するPodと同じ名前空間に存在する必要があります。クラスターは、Podの名前空間でクレームを見つけ、それを使用してクレームを支援しているPersistentVolumeを取得します。次に、ボリュームがホストとPodにマウントされます。

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: mypod
spec:
  containers:
    - name: myfrontend
      image: nginx
      volumeMounts:
      - mountPath: "/var/www/html"
        name: mypd
  volumes:
    - name: mypd
      persistentVolumeClaim:
        claimName: myclaim
```

### 名前空間に関する注意

PersistentVolumeバインドは排他的であり、PersistentVolumeClaimは名前空間オブジェクトであるため、"多"モード(`ROX`、`RWX`)でクレームをマウントすることは1つの名前空間内でのみ可能です。

## Rawブロックボリュームのサポート

{{< feature-state for_k8s_version="v1.18" state="stable" >}}

次のボリュームプラグインは、必要に応じて動的プロビジョニングを含むrawブロックボリュームをサポートします。

* AWSElasticBlockStore
* AzureDisk
* CSI
* FC (Fibre Channel)
* GCEPersistentDisk
* iSCSI
* Local volume
* OpenStack Cinder
* RBD (Ceph Block Device)
* VsphereVolume 

### Rawブロックボリュームを使用した永続ボリューム {#persistent-volume-using-a-raw-block-volume}

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: block-pv
spec:
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteOnce
  volumeMode: Block
  persistentVolumeReclaimPolicy: Retain
  fc:
    targetWWNs: ["50060e801049cfd1"]
    lun: 0
    readOnly: false
```

### Rawブロックボリュームを要求する永続ボリュームクレーム

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: block-pvc
spec:
  accessModes:
    - ReadWriteOnce
  volumeMode: Block
  resources:
    requests:
      storage: 10Gi
```

### コンテナにRawブロックデバイスパスを追加するPod仕様

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-with-block-volume
spec:
  containers:
    - name: fc-container
      image: fedora:26
      command: ["/bin/sh", "-c"]
      args: [ "tail -f /dev/null" ]
      volumeDevices:
        - name: data
          devicePath: /dev/xvda
  volumes:
    - name: data
      persistentVolumeClaim:
        claimName: block-pvc
```

{{< note >}}
Podにrawブロックデバイスを追加する場合は、マウントパスの代わりにコンテナーでデバイスパスを指定します。
{{< /note >}}

### ブロックボリュームのバインド

ユーザーがPersistentVolumeClaim specの`volumeMode`フィールドを使用してrawブロックボリュームの要求を示す場合、バインディングルールは、このモードをspecの一部として考慮しなかった以前のリリースとわずかに異なります。表にリストされているのは、ユーザーと管理者がrawブロックデバイスを要求するために指定可能な組み合わせの表です。この表は、ボリュームがバインドされるか、組み合わせが与えられないかを示します。静的にプロビジョニングされたボリュームのボリュームバインディングマトリクスはこちらです。

| PVボリュームモード | PVCボリュームモード | 結果         |
| -------------------|:-------------------:| ------------:|
|   未定義           | 未定義              | バインド     |
|   未定義           | ブロック            | バインドなし |
|   未定義           | ファイルシステム    | バインド     |
|   ブロック         | 未定義              | バインドなし |
|   ブロック         | ブロック            | バインド     |
|   ブロック         | ファイルシステム    | バインドなし |
|   ファイルシステム | ファイルシステム    | バインド     |
|   ファイルシステム | ブロック            | バインドなし |
|   ファイルシステム | 未定義              | バインド     |

{{< note >}}
アルファリリースでは、静的にプロビジョニングされたボリュームのみがサポートされます。管理者は、rawブロックデバイスを使用する場合、これらの値を考慮するように注意する必要があります。
{{< /note >}}

## ボリュームのスナップショットとスナップショットからのボリュームの復元のサポート

{{< feature-state for_k8s_version="v1.17" state="beta" >}}

ボリュームスナップショット機能は、CSIボリュームプラグインのみをサポートするために追加されました。詳細については、[ボリュームのスナップショット](/docs/concepts/storage/volume-snapshots/)を参照してください。

ボリュームスナップショットのデータソースからボリュームを復元する機能を有効にするには、apiserverおよびcontroller-managerで`VolumeSnapshotDataSource`フィーチャーゲートを有効にします。

### ボリュームスナップショットから永続ボリュームクレームを作成する {#create-persistent-volume-claim-from-volume-snapshot}

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: restore-pvc
spec:
  storageClassName: csi-hostpath-sc
  dataSource:
    name: new-snapshot-test
    kind: VolumeSnapshot
    apiGroup: snapshot.storage.k8s.io
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
```

## ボリュームの複製

[ボリュームの複製](/ja/docs/concepts/storage/volume-pvc-datasource/)はCSIボリュームプラグインにのみ利用可能です。

PVCデータソースからのボリューム複製機能を有効にするには、apiserverおよびcontroller-managerで`VolumeSnapshotDataSource`フィーチャーゲートを有効にします。

### 既存のPVCからの永続ボリュームクレーム作成 {#create-persistent-volume-claim-from-an-existing-pvc} 

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: cloned-pvc
spec:
  storageClassName: my-csi-plugin
  dataSource:
    name: existing-src-pvc-name
    kind: PersistentVolumeClaim
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
```

## 可搬性の高い設定の作成

もし幅広いクラスターで実行され、永続ボリュームが必要となる構成テンプレートやサンプルを作成している場合は、次のパターンを使用することをお勧めします。

- 構成にPersistentVolumeClaimオブジェクトを含める(DeploymentやConfigMapと共に)
- ユーザーが設定をインスタンス化する際にPersistentVolumeを作成する権限がない場合があるため、設定にPersistentVolumeオブジェクトを含めない。
- テンプレートをインスタンス化する時にストレージクラス名を指定する選択肢をユーザーに与える
  - ユーザーがストレージクラス名を指定する場合、persistentVolumeClaim.storageClassName フィールドにその値を入力する。これにより、クラスターが管理者によって有効にされたストレージクラスを持っている場合、PVCは正しいストレージクラスと一致する。
  - ユーザーがストレージクラス名を指定しない場合、`persistentVolumeClaim.storageClassName`フィールドはnilのままにする。これにより、PVはユーザーにクラスターのデフォルトストレージクラスで自動的にプロビジョニングされる。多くのクラスター環境ではデフォルトのストレージクラスがインストールされているが、管理者は独自のデフォルトストレージクラスを作成することができる。
- ツールがPVCを監視し、しばらくしてもバインドされないことをユーザーに表示する。これはクラスターが動的ストレージをサポートしない(この場合ユーザーは対応するPVを作成するべき)、もしくはクラスターがストレージシステムを持っていない(この場合ユーザーはPVCを必要とする設定をデプロイできない)可能性があることを示す。

  ## {{% heading "whatsnext" %}}

* [Creating a Persistent Volume](/docs/tasks/configure-pod-container/configure-persistent-volume-storage/#create-a-persistentvolume)について学ぶ
* [Creating a Persistent Volume Claim](/docs/tasks/configure-pod-container/configure-persistent-volume-storage/#create-a-persistentvolumeclaim)について学ぶ
* [Persistent Storage design document](https://git.k8s.io/community/contributors/design-proposals/storage/persistent-storage.md)を読む

### リファレンス

* [PersistentVolume](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#persistentvolume-v1-core)
* [PersistentVolumeSpec](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#persistentvolumespec-v1-core)
* [PersistentVolumeClaim](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#persistentvolumeclaim-v1-core)
* [PersistentVolumeClaimSpec](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#persistentvolumeclaimspec-v1-core)
