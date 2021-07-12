---
title: 스토리지 클래스
content_type: concept
weight: 30
---

<!-- overview -->

이 문서는 쿠버네티스의 스토리지클래스의 개념을 설명한다.
[볼륨](/ko/docs/concepts/storage/volumes/)과
[퍼시스턴트 볼륨](/ko/docs/concepts/storage/persistent-volumes)에 익숙해지는 것을 권장한다.

<!-- body -->

## 소개

스토리지클래스는 관리자가 제공하는 스토리지의 "classes"를 설명할 수 있는
방법을 제공한다. 다른 클래스는 서비스의 품질 수준 또는
백업 정책, 클러스터 관리자가 정한 임의의 정책에
매핑될 수 있다. 쿠버네티스 자체는 클래스가 무엇을 나타내는지에
대해 상관하지 않는다. 다른 스토리지 시스템에서는 이 개념을
"프로파일"이라고도 한다.

## 스토리지클래스 리소스

각 스토리지클래스에는 해당 스토리지클래스에 속하는 퍼시스턴트볼륨을 동적으로 프로비저닝
할 때 사용되는 `provisioner`, `parameters` 와
`reclaimPolicy` 필드가 포함된다.

스토리지클래스 오브젝트의 이름은 중요하며, 사용자가 특정
클래스를 요청할 수 있는 방법이다. 관리자는 스토리지클래스 오브젝트를
처음 생성할 때 클래스의 이름과 기타 파라미터를 설정하며,
일단 생성된 오브젝트는 업데이트할 수 없다.

관리자는 특정 클래스에 바인딩을 요청하지 않는 PVC에 대해서만 기본
스토리지클래스를 지정할 수 있다. 자세한 내용은
[퍼시스턴트볼륨클레임 섹션](/ko/docs/concepts/storage/persistent-volumes/#퍼시스턴트볼륨클레임)을
본다.

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: standard
provisioner: kubernetes.io/aws-ebs
parameters:
  type: gp2
reclaimPolicy: Retain
allowVolumeExpansion: true
mountOptions:
  - debug
volumeBindingMode: Immediate
```

### 프로비저너

각 스토리지클래스에는 PV 프로비저닝에 사용되는 볼륨 플러그인을 결정하는
프로비저너가 있다. 이 필드는 반드시 지정해야 한다.

| 볼륨 플러그인        | 내부 프로비저너     |  설정 예시                           |
| :---                 |     :---:           |    :---:                             |
| AWSElasticBlockStore | &#x2713;            | [AWS EBS](#aws-ebs)                          |
| AzureFile            | &#x2713;            | [Azure 파일](#azure-파일)            |
| AzureDisk            | &#x2713;            | [Azure 디스크](#azure-디스크)            |
| CephFS               | -                   | -                                    |
| Cinder               | &#x2713;            | [OpenStack Cinder](#openstack-cinder)|
| FC                   | -                   | -                                    |
| FlexVolume           | -                   | -                                    |
| Flocker              | &#x2713;            | -                                    |
| GCEPersistentDisk    | &#x2713;            | [GCE PD](#gce-pd)                          |
| Glusterfs            | &#x2713;            | [Glusterfs](#glusterfs)              |
| iSCSI                | -                   | -                                    |
| Quobyte              | &#x2713;            | [Quobyte](#quobyte)                  |
| NFS                  | -                   | -                                    |
| RBD                  | &#x2713;            | [Ceph RBD](#ceph-rbd)                |
| VsphereVolume        | &#x2713;            | [vSphere](#vsphere)                  |
| PortworxVolume       | &#x2713;            | [Portworx 볼륨](#portworx-볼륨)  |
| ScaleIO              | &#x2713;            | [ScaleIO](#scaleio)                  |
| StorageOS            | &#x2713;            | [StorageOS](#storageos)              |
| Local                | -                   | [Local](#local)              |

여기 목록에서 "내부" 프로비저너를 지정할 수 있다(이
이름은 "kubernetes.io" 가 접두사로 시작하고, 쿠버네티스와
함께 제공된다). 또한, 쿠버네티스에서 정의한
[사양](https://git.k8s.io/community/contributors/design-proposals/storage/volume-provisioning.md)을
따르는 독립적인 프로그램인 외부 프로비저너를 실행하고 지정할 수 있다.
외부 프로비저너의 작성자는 코드의 수명, 프로비저너의
배송 방법, 실행 방법, (Flex를 포함한)볼륨 플러그인
등에 대한 완전한 재량권을 가진다. [kubernetes-sigs/sig-storage-lib-external-provisioner](https://github.com/kubernetes-sigs/sig-storage-lib-external-provisioner)
리포지터리에는 대량의 사양을 구현하는 외부 프로비저너를 작성하기
위한 라이브러리가 있다. 일부 외부 프로비저너의 목록은
[kubernetes-sigs/sig-storage-lib-external-provisioner](https://github.com/kubernetes-sigs/sig-storage-lib-external-provisioner) 리포지터리에 있다.

예를 들어, NFS는 내부 프로비저너를 제공하지 않지만, 외부
프로비저너를 사용할 수 있다. 타사 스토리지 업체가 자체 외부
프로비저너를 제공하는 경우도 있다.

### 리클레임 정책

스토리지클래스에 의해 동적으로 생성된 퍼시스턴트볼륨은 클래스의
`reclaimPolicy` 필드에 지정된 리클레임 정책을 가지는데,
이는 `Delete` 또는 `Retain` 이 될 수 있다. 스토리지클래스 오브젝트가
생성될 때 `reclaimPolicy` 가 지정되지 않으면 기본값은 `Delete` 이다.

수동으로 생성되고 스토리지클래스를 통해 관리되는 퍼시스턴트볼륨에는
생성 시 할당된 리클레임 정책이 있다.

### 볼륨 확장 허용

{{< feature-state for_k8s_version="v1.11" state="beta" >}}

퍼시스턴트볼륨은 확장이 가능하도록 구성할 수 있다. 이 기능을 `true` 로 설정하면
해당 PVC 오브젝트를 편집하여 볼륨 크기를 조정할 수 있다.

다음 볼륨 유형은 기본 스토리지클래스에서 `allowVolumeExpansion` 필드가
true로 설정된 경우 볼륨 확장을 지원한다.

{{< table caption = "Table of Volume types and the version of Kubernetes they require"  >}}

볼륨 유형 | 요구되는 쿠버네티스 버전
:---------- | :--------------------------
gcePersistentDisk | 1.11
awsElasticBlockStore | 1.11
Cinder | 1.11
glusterfs | 1.11
rbd | 1.11
Azure File | 1.11
Azure Disk | 1.11
Portworx | 1.11
FlexVolume | 1.13
CSI | 1.14 (alpha), 1.16 (beta)

{{< /table >}}


{{< note >}}
볼륨 확장 기능을 사용해서 볼륨을 확장할 수 있지만, 볼륨을 축소할 수는 없다.
{{< /note >}}

### 마운트 옵션

스토리지클래스에 의해 동적으로 생성된 퍼시스턴트볼륨은
클래스의 `mountOptions` 필드에 지정된 마운트 옵션을 가진다.

만약 볼륨 플러그인이 마운트 옵션을 지원하지 않는데, 마운트
옵션을 지정하면 프로비저닝은 실패한다. 마운트 옵션은 클래스 또는 PV에서
검증되지 않는다. PV 마운트가 유효하지 않으면, 마운트가 실패하게 된다.

### 볼륨 바인딩 모드

`volumeBindingMode` 필드는 [볼륨 바인딩과 동적
프로비저닝](/ko/docs/concepts/storage/persistent-volumes/#프로비저닝)의 시작 시기를 제어한다. 설정되어 있지 않으면, `Immediate` 모드가 기본으로 사용된다.

`Immediate` 모드는 퍼시스턴트볼륨클레임이 생성되면 볼륨
바인딩과 동적 프로비저닝이 즉시 발생하는 것을 나타낸다. 토폴로지 제약이
있고 클러스터의 모든 노드에서 전역적으로 접근할 수 없는 스토리지
백엔드의 경우, 파드의 스케줄링 요구 사항에 대한 지식 없이 퍼시스턴트볼륨이
바인딩되거나 프로비저닝된다. 이로 인해 스케줄되지 않은 파드가 발생할 수 있다.

클러스터 관리자는 `WaitForFirstConsumer` 모드를 지정해서 이 문제를 해결할 수 있는데
이 모드는 퍼시스턴트볼륨클레임을 사용하는 파드가 생성될 때까지 퍼시스턴트볼륨의 바인딩과 프로비저닝을 지연시킨다.
퍼시스턴트볼륨은 파드의 스케줄링 제약 조건에 의해 지정된 토폴로지에
따라 선택되거나 프로비전된다. 여기에는
[리소스 요구 사항](/ko/docs/concepts/configuration/manage-resources-containers/),
[노드 셀렉터](/ko/docs/concepts/scheduling-eviction/assign-pod-node/#노드-셀렉터-nodeselector),
[파드 어피니티(affinity)와
안티-어피니티(anti-affinity)](/ko/docs/concepts/scheduling-eviction/assign-pod-node/#어피니티-affinity-와-안티-어피니티-anti-affinity)
그리고 [테인트(taint)와 톨러레이션(toleration)](/ko/docs/concepts/scheduling-eviction/taint-and-toleration/)이 포함된다.

다음 플러그인은 동적 프로비저닝과 `WaitForFirstConsumer` 를 지원한다.

* [AWSElasticBlockStore](#aws-ebs)
* [GCEPersistentDisk](#gce-pd)
* [Azure디스크](#azure-디스크)

다음 플러그인은 사전에 생성된 퍼시스턴트볼륨 바인딩으로 `WaitForFirstConsumer` 를 지원한다.

* 위에서 언급한 모든 플러그인
* [Local](#local)

{{< feature-state state="stable" for_k8s_version="v1.17" >}}
[CSI 볼륨](/ko/docs/concepts/storage/volumes/#csi)은 동적 프로비저닝과
사전에 생성된 PV에서도 지원되지만, 지원되는 토폴로지 키와 예시를 보려면 해당
CSI 드라이버에 대한 문서를 본다.

{{< note >}}
   `waitForFirstConsumer`를 사용한다면, 노드 어피니티를 지정하기 위해서 파드 스펙에 `nodeName`을 사용하지는 않아야 한다.
   만약 `nodeName`을 사용한다면, 스케줄러가 바이패스되고 PVC가 `pending` 상태로 있을 것이다.

   대신, 아래와 같이 호스트네임을 이용하는 노드셀렉터를 사용할 수 있다.
{{< /note >}}

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: task-pv-pod
spec:
  nodeSelector:
    kubernetes.io/hostname: kube-01
  volumes:
    - name: task-pv-storage
      persistentVolumeClaim:
        claimName: task-pv-claim
  containers:
    - name: task-pv-container
      image: nginx
      ports:
        - containerPort: 80
          name: "http-server"
      volumeMounts:
        - mountPath: "/usr/share/nginx/html"
          name: task-pv-storage
```

### 허용된 토폴로지

클러스터 운영자가 `WaitForFirstConsumer` 볼륨 바인딩 모드를 지정하면, 대부분의 상황에서
더 이상 특정 토폴로지로 프로비저닝을 제한할 필요가 없다. 그러나
여전히 필요한 경우에는 `allowedTopologies` 를 지정할 수 있다.

이 예시는 프로비전된 볼륨의 토폴로지를 특정 영역으로 제한하는 방법을
보여 주며 지원되는 플러그인의 `zone` 과 `zones` 파라미터를 대체하는
데 사용해야 한다.

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: standard
provisioner: kubernetes.io/gce-pd
parameters:
  type: pd-standard
volumeBindingMode: WaitForFirstConsumer
allowedTopologies:
- matchLabelExpressions:
  - key: failure-domain.beta.kubernetes.io/zone
    values:
    - us-central1-a
    - us-central1-b
```

## 파라미터

스토리지 클래스에는 스토리지 클래스에 속하는 볼륨을 설명하는 파라미터가
있다. `provisioner` 에 따라 다른 파라미터를 사용할 수 있다. 예를 들어,
파라미터 `type` 에 대한 값 `io1` 과 파라미터 `iopsPerGB` 는
EBS에만 사용할 수 있다. 파라미터 생략 시 일부 기본값이
사용된다.

스토리지클래스에 대해 최대 512개의 파라미터를 정의할 수 있다.
키와 값을 포함하여 파라미터 오브젝터의 총 길이는 256 KiB를
초과할 수 없다.

### AWS EBS

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: slow
provisioner: kubernetes.io/aws-ebs
parameters:
  type: io1
  iopsPerGB: "10"
  fsType: ext4
```

* `type`: `io1`, `gp2`, `sc1`, `st1`. 자세한 내용은
  [AWS 문서](https://docs.aws.amazon.com/ko_kr/AWSEC2/latest/UserGuide/ebs-volume-types.html)를
  본다. 기본값: `gp2`.
* `zone` (사용 중단(deprecated)): AWS 영역. `zone` 과 `zones` 를 지정하지 않으면, 일반적으로
  쿠버네티스 클러스터의 노드가 있는 모든 활성화된 영역에 걸쳐 볼륨이
  라운드 로빈으로 조정된다. `zone` 과 `zones` 파라미터를 동시에 사용해서는 안된다.
* `zones` (사용 중단): 쉼표로 구분된 AWS 영역의 목록. `zone` 과 `zones` 를
  지정하지 않으면, 일반적으로 쿠버네티스 클러스터의 노드가 있는 모든 활성화된 영역에 걸쳐
  볼륨이 라운드 로빈으로 조정된다. `zone` 과 `zones` 파라미터를
  동시에 사용해서는 안된다.
* `iopsPerGB`: `io1` 볼륨 전용이다. 1초당 GiB에 대한 I/O 작업 수이다. AWS
  볼륨 플러그인은 요청된 볼륨 크기에 곱셈하여 볼륨의 IOPS를
  계산하고 이를 20,000 IOPS로 제한한다(AWS에서 지원하는 최대값으로,
  [AWS 문서](https://docs.aws.amazon.com/ko_kr/AWSEC2/latest/UserGuide/ebs-volume-types.html)를 본다).
  여기에는 문자열, 즉 `10` 이 아닌, `"10"` 이 필요하다.
* `fsType`: fsType은 쿠버네티스에서 지원된다. 기본값: `"ext4"`.
* `encrypted`: EBS 볼륨의 암호화 여부를 나타낸다.
  유효한 값은 `"ture"` 또는 `"false"` 이다. 여기에는 문자열,
  즉 `true` 가 아닌, `"true"` 가 필요하다.
* `kmsKeyId`: 선택 사항. 볼륨을 암호화할 때 사용할 키의 전체 Amazon
  리소스 이름이다. 아무것도 제공되지 않지만, `encrypted` 가 true라면
  AWS에 의해 키가 생성된다. 유효한 ARN 값은 AWS 문서를 본다.

{{< note >}}
`zone` 과 `zones` 파라미터는 사용 중단 되었으며,
[allowedTopologies](#allowed-topologies)로 대체되었다.
{{< /note >}}

### GCE PD

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: slow
provisioner: kubernetes.io/gce-pd
parameters:
  type: pd-standard
  fstype: ext4
  replication-type: none
```

* `type`: `pd-standard` 또는 `pd-ssd`. 기본값: `pd-standard`
* `zone` (사용 중단): GCE 영역. `zone` 과 `zones` 를 모두 지정하지 않으면, 쿠버네티스 클러스터의
  노드가 있는 모든 활성화된 영역에 걸쳐 볼륨이 라운드 로빈으로
  조정된다. `zone` 과 `zones` 파라미터를 동시에 사용해서는 안된다.
* `zones` (사용 중단): 쉼표로 구분되는 GCE 영역의 목록. `zone` 과 `zones` 를 모두
  지정하지 않으면, 쿠버네티스 클러스터의 노드가 있는 모든 활성화된 영역에
  걸쳐 볼륨이 라운드 로빈으로 조정된다. `zone` 과 `zones` 파라미터를
  동시에 사용해서는 안된다.
* `fstype`: `ext4` 또는 `xfs`. 기본값: `ext4`. 정의된 파일시스템 유형은 호스트 운영체제에서 지원되어야 한다.

* `replication-type`: `none` 또는 `regional-pd`. 기본값: `none`.

`replication-type` 을 `none` 으로 설정하면 (영역) PD가 프로비전된다.

`replication-type` 이 `regional-pd` 로 설정되면,
[지역 퍼시스턴트 디스크](https://cloud.google.com/compute/docs/disks/#repds)
가 프로비전된다. 이는 퍼시스턴트볼륨클레임과 스토리지클래스를 소모하는 파드를
생성할 때 지역 퍼시스턴트 디스크는 두개의 영역으로
프로비전되기에 `volumeBindingMode: WaitForFirstConsumer` 를
설정하는 것을 강력히 권장한다. 하나의 영역은 파드가 스케줄된
영역과 동일하다. 다른 영역은 클러스터에서 사용할 수
있는 영역에서 임의로 선택된다. 디스크 영역은 `allowedTopologies` 를
사용하면 더 제한할 수 있다.

{{< note >}}
`zone` 과 `zones` 파라미터는 사용 중단 되었으며,
[allowedTopologies](#allowed-topologies)로 대체되었다.
{{< /note >}}

### Glusterfs

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: slow
provisioner: kubernetes.io/glusterfs
parameters:
  resturl: "http://127.0.0.1:8081"
  clusterid: "630372ccdc720a92c681fb928f27b53f"
  restauthenabled: "true"
  restuser: "admin"
  secretNamespace: "default"
  secretName: "heketi-secret"
  gidMin: "40000"
  gidMax: "50000"
  volumetype: "replicate:3"
```

* `resturl`: 필요에 따라 gluster 볼륨을 프로비전하는 Gluster REST 서비스/Heketi
  서비스 url 이다. 일반적인 형식은 `IPaddress:Port` 이어야 하며 이는 GlusterFS
  동적 프로비저너의 필수 파라미터이다. Heketi 서비스가 openshift/kubernetes
  설정에서 라우팅이 가능한 서비스로 노출이 되는 경우 이것은 fqdn이 해석할 수 있는
  Heketi 서비스 url인 `http://heketi-storage-project.cloudapps.mystorage.com` 과
  유사한 형식을 가질 수 있다.
* `restauthenabled` : REST 서버에 대한 인증을 가능하게 하는 Gluster REST 서비스
  인증 부울이다. 이 값이 `"true"` 이면, `restuser` 와 `restuserkey`
  또는 `secretNamespace` + `secretName` 을 채워야 한다. 이 옵션은
  사용 중단이며, `restuser`, `restuserkey`, `secretName` 또는
  `secretNamespace` 중 하나를 지정하면 인증이 활성화된다.
* `restuser` : Gluster REST 서비스/Heketi 사용자로 Gluster Trusted Pool에서
  볼륨을 생성할 수 있다.
* `restuserkey` : REST 서버에 대한 인증에 사용될 Gluster REST 서비스/Heketi
  사용자의 암호이다. 이 파라미터는 `secretNamespace` + `secretName` 을 위해
  사용 중단 되었다.
* `secretNamespace`, `secretName` : Gluster REST 서비스와 통신할 때 사용할
  사용자 암호가 포함된 시크릿 인스턴스를 식별한다. 이 파라미터는
  선택 사항으로 `secretNamespace` 와 `secretName` 을 모두 생략하면
  빈 암호가 사용된다. 제공된 시크릿은 `"kubernetes.io/glusterfs"` 유형이어야
  하며, 예를 들어 다음과 같이 생성한다.

    ```
    kubectl create secret generic heketi-secret \
      --type="kubernetes.io/glusterfs" --from-literal=key='opensesame' \
      --namespace=default
    ```

    시크릿의 예시는
    [glusterfs-provisioning-secret.yaml](https://github.com/kubernetes/examples/tree/master/staging/persistent-volume-provisioning/glusterfs/glusterfs-secret.yaml)에서 찾을 수 있다.

* `clusterid`: `630372ccdc720a92c681fb928f27b53f` 는 볼륨을 프로비저닝할
  때 Heketi가 사용할 클러스터의 ID이다. 또한, 예시와 같이 클러스터
  ID 목록이 될 수 있다. 예:
  `"8452344e2becec931ece4e33c4674e4e,42982310de6c63381718ccfa6d8cf397"`. 이것은
  선택적 파라미터이다.
* `gidMin`, `gidMax` : 스토리지클래스에 대한 GID 범위의 최소값과
  최대값이다. 이 범위( gidMin-gidMax )의 고유한 값(GID)은 동적으로
  프로비전된 볼륨에 사용된다. 이것은 선택적인 값이다. 지정하지 않으면,
  볼륨은 각각 gidMin과 gidMax의 기본값인 2000-2147483647
  사이의 값으로 프로비전된다.
* `volumetype` : 볼륨 유형과 파라미터는 이 선택적 값으로 구성할
  수 있다. 볼륨 유형을 언급하지 않는 경우, 볼륨 유형을 결정하는 것은
  프로비저너의 책임이다.

    예를 들어:
    * 레플리카 볼륨: `volumetype: replicate:3` 여기서 '3'은 레플리카의 수이다.
    * Disperse/EC 볼륨: `volumetype: disperse:4:2` 여기서 '4'는 데이터이고 '2'는 중복 횟수이다.
    * Distribute 볼륨: `volumetype: none`

    사용 가능한 볼륨 유형과 관리 옵션에 대해서는
    [관리 가이드](https://access.redhat.com/documentation/en-US/Red_Hat_Storage/3.1/html/Administration_Guide/part-Overview.html)를 참조한다.

    자세한 정보는
    [Heketi 구성 방법](https://github.com/heketi/heketi/wiki/Setting-up-the-topology)을 참조한다.

    퍼시스턴트 볼륨이 동적으로 프로비전되면 Gluster 플러그인은
    `gluster-dynamic-<claimname>` 이라는 이름으로 엔드포인트와
    헤드리스 서비스를 자동으로 생성한다. 퍼시스턴트 볼륨 클레임을
    삭제하면 동적 엔드포인트와 서비스가 자동으로 삭제된다.

### OpenStack Cinder

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: gold
provisioner: kubernetes.io/cinder
parameters:
  availability: nova
```

* `availability`: 가용성 영역. 지정하지 않으면, 일반적으로 쿠버네티스 클러스터의
  노드가 있는 모든 활성화된 영역에 걸쳐 볼륨이 라운드 로빈으로 조정된다.

{{< note >}}
{{< feature-state state="deprecated" for_k8s_version="v1.11" >}}
이 OpenStack 내부 프로비저너는 사용 중단 되었다. [OpenStack용 외부 클라우드 공급자](https://github.com/kubernetes/cloud-provider-openstack)를 사용한다.
{{< /note >}}

### vSphere

vSphere 스토리지 클래스에는 두 가지 유형의 프로비저닝 도구가 있다.

- [CSI 프로비저닝 도구](#csi-프로비저닝-도구): `csi.vsphere.vmware.com`
- [vCP 프로비저닝 도구](#vcp-프로비저닝-도구): `kubernetes.io/vsphere-volume`

인-트리 프로비저닝 도구는 [사용 중단](/blog/2019/12/09/kubernetes-1-17-feature-csi-migration-beta/#why-are-we-migrating-in-tree-plugins-to-csi)되었다. CSI 프로비저닝 도구에 대한 자세한 내용은 [쿠버네티스 vSphere CSI 드라이버](https://vsphere-csi-driver.sigs.k8s.io/) 및 [vSphereVolume CSI 마이그레이션](/ko/docs/concepts/storage/volumes/#csi-마이그레이션)을 참고한다.

#### CSI 프로비저닝 도구 {#vsphere-provisioner-csi}

vSphere CSI 스토리지클래스 프로비저닝 도구는 Tanzu 쿠버네티스 클러스터에서 작동한다. 예시는 [vSphere CSI 리포지터리](https://raw.githubusercontent.com/kubernetes-sigs/vsphere-csi-driver/master/example/vanilla-k8s-file-driver/example-sc.yaml)를 참조한다.

#### vCP 프로비저닝 도구

다음 예시에서는 VMware 클라우드 공급자(vCP) 스토리지클래스 프로비저닝 도구를 사용한다.

1. 사용자 지정 디스크 형식으로 스토리지클래스를 생성한다.

    ```yaml
    apiVersion: storage.k8s.io/v1
    kind: StorageClass
    metadata:
      name: fast
    provisioner: kubernetes.io/vsphere-volume
    parameters:
      diskformat: zeroedthick
    ```

    `diskformat`: `thin`, `zeroedthick` 와 `eagerzeroedthick`. 기본값: `"thin"`.

2. 사용자 지정 데이터스토어에 디스크 형식으로 스토리지클래스를 생성한다.

    ```yaml
    apiVersion: storage.k8s.io/v1
    kind: StorageClass
    metadata:
      name: fast
    provisioner: kubernetes.io/vsphere-volume
    parameters:
        diskformat: zeroedthick
        datastore: VSANDatastore
    ```

    `datastore`: 또한, 사용자는 스토리지클래스에서 데이터스토어를 지정할 수 있다.
    볼륨은 스토리지클래스에 지정된 데이터스토어에 생성되며,
    이 경우 `VSANDatastore` 이다. 이 필드는 선택 사항이다. 데이터스토어를
    지정하지 않으면, vSphere 클라우드 공급자를 초기화하는데 사용되는 vSphere
    설정 파일에 지정된 데이터스토어에 볼륨이
    생성된다.

3. 쿠버네티스 내부 스토리지 정책을 관리한다.

    * 기존 vCenter SPBM 정책을 사용한다.

        vSphere 스토리지 관리의 가장 중요한 기능 중 하나는
        정책 기반 관리이다. 스토리지 정책 기반 관리(Storage Policy Based Management (SPBM))는
        광범위한 데이터 서비스와 스토리지 솔루션에서 단일 통합 컨트롤 플레인을
        제공하는 스토리지 정책 프레임워크이다. SPBM을 통해 vSphere 관리자는 용량 계획,
        차별화된 서비스 수준과 용량의 헤드룸(headroom) 관리와 같은
        선행 스토리지 프로비저닝 문제를
        극복할 수 있다.

        SPBM 정책은 `storagePolicyName` 파라미터를 사용하면
        스토리지클래스에서 지정할 수 있다.

    * 쿠버네티스 내부의 가상 SAN 정책 지원

        Vsphere 인프라스트럭쳐(Vsphere Infrastructure (VI)) 관리자는
        동적 볼륨 프로비저닝 중에 사용자 정의 가상 SAN 스토리지
        기능을 지정할 수 있다. 이제 동적 볼륨 프로비저닝 중에 스토리지
        기능의 형태로 성능 및 가용성과 같은 스토리지 요구 사항을 정의할
        수 있다. 스토리지 기능 요구 사항은 가상 SAN 정책으로 변환된
        퍼시스턴트 볼륨(가상 디스크)을 생성할 때
        가상 SAN 계층으로 푸시된다. 가상 디스크는 가상 SAN 데이터
        스토어에 분산되어 요구 사항을 충족시키게 된다.

        퍼시스턴트 볼륨 관리에 스토리지 정책을 사용하는 방법에 대한 자세한 내용은
        [볼륨의 동적 프로비저닝을 위한 스토리지 정책 기반 관리(SPBM)](https://vmware.github.io/vsphere-storage-for-kubernetes/documentation/policy-based-mgmt.html)를
        참조한다.

vSphere용 쿠버네티스 내에서 퍼시스턴트 볼륨 관리를 시도하는
[vSphere 예시](https://github.com/kubernetes/examples/tree/master/staging/volumes/vsphere)는
거의 없다.

### Ceph RBD

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast
provisioner: kubernetes.io/rbd
parameters:
  monitors: 10.16.153.105:6789
  adminId: kube
  adminSecretName: ceph-secret
  adminSecretNamespace: kube-system
  pool: kube
  userId: kube
  userSecretName: ceph-secret-user
  userSecretNamespace: default
  fsType: ext4
  imageFormat: "2"
  imageFeatures: "layering"
```

* `monitors`: 쉼표로 구분된 Ceph 모니터. 이 파라미터는 필수이다.
* `adminId`: 풀에 이미지를 생성할 수 있는 Ceph 클라이언트 ID.
  기본값은 "admin".
* `adminSecretName`: `adminId` 의 시크릿 이름. 이 파라미터는 필수이다.
  제공된 시크릿은 "kubernetes.io/rbd" 유형이어야 한다.
* `adminSecretNamespace`: `adminSecretName` 의 네임스페이스. 기본값은 "default".
* `pool`: Ceph RBD 풀. 기본값은 "rbd".
* `userId`: RBD 이미지를 매핑하는 데 사용하는 Ceph 클라이언트 ID. 기본값은
  `adminId` 와 동일하다.
* `userSecretName`: RDB 이미지를 매핑하기 위한 `userId` 에 대한 Ceph 시크릿 이름. PVC와
  동일한 네임스페이스에 존재해야 한다. 이 파라미터는 필수이다.
  제공된 시크릿은 "kubernetes.io/rbd" 유형이어야 하며, 다음의 예시와 같이
  생성되어야 한다.

    ```shell
    kubectl create secret generic ceph-secret --type="kubernetes.io/rbd" \
      --from-literal=key='QVFEQ1pMdFhPUnQrSmhBQUFYaERWNHJsZ3BsMmNjcDR6RFZST0E9PQ==' \
      --namespace=kube-system
    ```
* `userSecretNamespace`: `userSecretName` 의 네임스페이스.
* `fsType`: 쿠버네티스가 지원하는 fsType. 기본값: `"ext4"`.
* `imageFormat`: Ceph RBD 이미지 형식, "1" 또는 "2". 기본값은 "2".
* `imageFeatures`: 이 파라미터는 선택 사항이며, `imageFormat` 을 "2"로 설정한
  경우에만 사용해야 한다. 현재 `layering` 에서만 기능이 지원된다.
  기본값은 ""이며, 기능이 설정되어 있지 않다.

### Quobyte

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
   name: slow
provisioner: kubernetes.io/quobyte
parameters:
    quobyteAPIServer: "http://138.68.74.142:7860"
    registry: "138.68.74.142:7861"
    adminSecretName: "quobyte-admin-secret"
    adminSecretNamespace: "kube-system"
    user: "root"
    group: "root"
    quobyteConfig: "BASE"
    quobyteTenant: "DEFAULT"
```

* `quobyteAPIServer`: `"http(s)://api-server:7860"` 형식의
  Quobyte의 API 서버이다.
* `registry`: 볼륨을 마운트하는 데 사용할 Quobyte 레지스트리이다. 레지스트리를
  ``<host>:<port>`` 의 쌍으로 지정하거나 여러 레지스트리를
  지정하려면 쉼표만 있으면 된다.
  예: ``<host1>:<port>,<host2>:<port>,<host3>:<port>``
  호스트는 IP 주소이거나 DNS가 작동 중인 경우
  DNS 이름을 제공할 수도 있다.
* `adminSecretNamespace`: `adminSecretName` 의 네임스페이스.
  기본값은 "default".
* `adminSecretName`: 시크릿은 API 서버에 대해 인증하기 위한 Quobyte 사용자와 암호에
  대한 정보를 담고 있다. 제공된 시크릿은 "kubernetes.io/quobyte"
  유형과 `user` 및 `password` 키를 가져야 하며, 예를 들면
  다음과 같다.

    ```shell
    kubectl create secret generic quobyte-admin-secret \
      --type="kubernetes.io/quobyte" --from-literal=user='admin' --from-literal=password='opensesame' \
      --namespace=kube-system
    ```

* `user`: 이 사용자에 대한 모든 접근을 매핑한다. 기본값은 "root".
* `group`: 이 그룹에 대한 모든 접근을 매핑한다. 기본값은 "nfsnobody".
* `quobyteConfig`: 지정된 구성을 사용해서 볼륨을 생성한다. 웹 콘솔
  또는 quobyte CLI를 사용해서 새 구성을 작성하거나 기존 구성을
  수정할 수 있다. 기본값은 "BASE".
* `quobyteTenant`: 지정된 테넌트 ID를 사용해서 볼륨을 생성/삭제한다.
  이 Quobyte 테넌트는 이미 Quobyte에 있어야 한다.
  기본값은 "DEFAULT".

### Azure 디스크

#### Azure 비관리 디스크 스토리지 클래스 {#azure-unmanaged-disk-storage-class}

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: slow
provisioner: kubernetes.io/azure-disk
parameters:
  skuName: Standard_LRS
  location: eastus
  storageAccount: azure_storage_account_name
```

* `skuName`: Azure 스토리지 계정 Sku 계층. 기본값은 없음.
* `location`: Azure 스토리지 계정 지역. 기본값은 없음.
* `storageAccount`: Azure 스토리지 계정 이름. 스토리지 계정이 제공되면, 클러스터와 동일한
  리소스 그룹에 있어야 하며, `location` 은 무시된다. 스토리지 계정이
  제공되지 않으면, 클러스터와 동일한 리소스
  그룹에 새 스토리지 계정이 생성된다.

#### Azure 디스크 스토리지 클래스(v1.7.2부터 제공) {#azure-disk-storage-class}

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: slow
provisioner: kubernetes.io/azure-disk
parameters:
  storageaccounttype: Standard_LRS
  kind: managed
```

* `storageaccounttype`: Azure 스토리지 계정 Sku 계층. 기본값은 없음.
* `kind`: 가능한 값은 `shared`, `dedicated`, 그리고 `managed` (기본값) 이다.
  `kind` 가 `shared` 인 경우, 모든 비관리 디스크는 클러스터와
  동일한 리소스 그룹에 있는 몇 개의 공유 스토리지 계정에 생성된다. `kind` 가
  `dedicated` 인 경우, 클러스터와 동일한 리소스 그룹에서 새로운
  비관리 디스크에 대해 새로운 전용 스토리지 계정이 생성된다. `kind` 가
  `managed` 인 경우, 모든 관리 디스크는 클러스터와 동일한 리소스
  그룹에 생성된다.
* `resourceGroup`: Azure 디스크를 만들 리소스 그룹을 지정한다.
   기존에 있는 리소스 그룹 이름이어야 한다. 지정되지 않는 경우, 디스크는
   현재 쿠버네티스 클러스터와 동일한 리소스 그룹에 배치된다.

- 프리미엄 VM은 표준 LRS(Standard_LRS)와 프리미엄 LRS(Premium_LRS) 디스크를 모두 연결할 수 있는 반면에,
  표준 VM은 표준 LRS(Standard_LRS) 디스크만 연결할 수 있다.
- 관리되는 VM은 관리되는 디스크만 연결할 수 있고,
  비관리 VM은 비관리 디스크만 연결할 수 있다.

### Azure 파일

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: azurefile
provisioner: kubernetes.io/azure-file
parameters:
  skuName: Standard_LRS
  location: eastus
  storageAccount: azure_storage_account_name
```

* `skuName`: Azure 스토리지 계정 Sku 계층. 기본값은 없음.
* `location`: Azure 스토리지 계정 지역. 기본값은 없음.
* `storageAccount`: Azure 스토리지 계정 이름. 기본값은 없음. 스토리지 계정이
  제공되지 않으면, 리소스 그룹과 관련된 모든 스토리지 계정이
  검색되어 `skuName` 과 `location` 이 일치하는 것을 찾는다. 스토리지 계정이
  제공되면, 클러스터와 동일한 리소스 그룹에 있어야
  하며 `skuName` 과 `location` 은 무시된다.
* `secretNamespace`: Azure 스토리지 계정 이름과 키가 포함된 시크릿
  네임스페이스. 기본값은 파드와 동일하다.
* `secretName`: Azure 스토리지 계정 이름과 키가 포함된 시크릿 이름.
  기본값은 `azure-storage-account-<accountName>-secret`
* `readOnly`: 스토리지가 읽기 전용으로 마운트되어야 하는지 여부를 나타내는 플래그.
  읽기/쓰기 마운트를 의미하는 기본값은 false. 이 설정은
  볼륨마운트(VolumeMounts)의 `ReadOnly` 설정에도 영향을 준다.

스토리지 프로비저닝 중에 마운트 자격증명에 대해 `secretName`
이라는 시크릿이 생성된다. 클러스터에
[RBAC](/docs/reference/access-authn-authz/rbac/)과
[컨트롤러의 롤(role)들](/docs/reference/access-authn-authz/rbac/#controller-roles)을
모두 활성화한 경우, clusterrole `system:controller:persistent-volume-binder`
에 대한 `secret` 리소스에 `create` 권한을 추가한다.

다중 테넌시 컨텍스트에서 `secretNamespace` 의 값을 명시적으로 설정하는
것을 권장하며, 그렇지 않으면 다른 사용자가 스토리지 계정 자격증명을
읽을 수 있기 때문이다.

### Portworx 볼륨

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: portworx-io-priority-high
provisioner: kubernetes.io/portworx-volume
parameters:
  repl: "1"
  snap_interval:   "70"
  priority_io:  "high"

```

* `fs`: 배치할 파일 시스템: `none/xfs/ext4` (기본값: `ext4`)
* `block_size`: Kbytes 단위의 블록 크기(기본값: `32`).
* `repl`: 레플리케이션 팩터 `1..3` (기본값: `1`)의 형태로 제공될
  동기 레플리카의 수. 여기에는 문자열,
  즉 `0` 이 아닌, `"0"` 이 필요하다.
* `priority_io`: 볼륨이 고성능 또는 우선 순위가 낮은 스토리지에서
  생성될 것인지를 결정한다 `high/medium/low` (기본값: `low`).
* `snap_interval`: 스냅샷을 트리거할 때의 시각/시간 간격(분).
  스냅샷은 이전 스냅샷과의 차이에 따라 증분되며, 0은 스냅을
  비활성화 한다(기본값: `0`). 여기에는 문자열,
  즉 `70` 이 아닌, `"70"` 이 필요하다.
* `aggregation_level`: 볼륨이 분배될 청크 수를 지정하며, 0은 집계되지 않은
  볼륨을 나타낸다(기본값: `0`). 여기에는 문자열,
  즉 `0` 이 아닌, `"0"` 이 필요하다.
* `ephemeral`: 마운트 해제 후 볼륨을 정리해야 하는지 혹은 지속적이어야
  하는지를 지정한다. `emptyDir` 에 대한 유스케이스는 이 값을 true로
  설정할 수 있으며, `persistent volumes` 에 대한 유스케이스인
  카산드라와 같은 데이터베이스는 false로 설정해야 한다. `true/false` (기본값 `false`)
  여기에는 문자열, 즉 `true` 가 아닌, `"true"` 가 필요하다.

### ScaleIO

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: slow
provisioner: kubernetes.io/scaleio
parameters:
  gateway: https://192.168.99.200:443/api
  system: scaleio
  protectionDomain: pd0
  storagePool: sp1
  storageMode: ThinProvisioned
  secretRef: sio-secret
  readOnly: false
  fsType: xfs
```

* `provisioner`: 속성이 `kubernetes.io/scaleio` 로 설정되어 있다.
* `gateway`: ScaleIO API 게이트웨이 주소(필수)
* `system`: ScaleIO 시스템의 이름(필수)
* `protectionDomain`: ScaleIO 보호 도메인의 이름(필수)
* `storagePool`: 볼륨 스토리지 풀의 이름(필수)
* `storageMode`: 스토리지 프로비전 모드: `ThinProvisioned` (기본값) 또는
  `ThickProvisioned`
* `secretRef`: 구성된 시크릿 오브젝트에 대한 참조(필수)
* `readOnly`: 마운트된 볼륨에 대한 접근 모드의 지정(기본값: false)
* `fsType`: 볼륨에 사용할 파일 시스템 유형(기본값: ext4)

ScaleIO 쿠버네티스 볼륨 플러그인에는 구성된 시크릿 오브젝트가 필요하다.
시크릿은 다음 명령에 표시된 것처럼 `kubernetes.io/scaleio` 유형으로
작성해야 하며, PVC와 동일한 네임스페이스
값을 사용해야 한다.

```shell
kubectl create secret generic sio-secret --type="kubernetes.io/scaleio" \
--from-literal=username=sioadmin --from-literal=password=d2NABDNjMA== \
--namespace=default
```

### StorageOS

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast
provisioner: kubernetes.io/storageos
parameters:
  pool: default
  description: Kubernetes volume
  fsType: ext4
  adminSecretNamespace: default
  adminSecretName: storageos-secret
```

* `pool`: 볼륨을 프로비전할 StorageOS 분산 용량
  풀의 이름. 지정되지 않은 경우 일반적으로 존재하는 `default` 풀을 사용한다.
* `description`: 동적으로 생성된 볼륨에 할당할 설명.
  모든 볼륨 설명은 스토리지 클래스에 대해 동일하지만, 서로 다른
  유스케이스에 대한 설명을 허용하기 위해 다른 스토리지 클래스를 사용할 수 있다.
  기본값은 `Kubernetes volume`.
* `fsType`: 요청할 기본 파일 시스템 유형. StorageOS 내의 사용자
  정의 규칙이 이 값을 무시할 수 있다. 기본 값은 `ext4`.
* `adminSecretNamespace`: API 구성 시크릿이 있는 네임스페이스.
  adminSecretName 이 설정된 경우 필수이다.
* `adminSecretName`: StorageOS API 자격증명을 얻는 데 사용할 시크릿의 이름.
  지정하지 않으면 기본값이 시도된다.

StorageOS 쿠버네티스 볼륨 플러그인은 시크릿 오브젝트를 사용해서 StorageOS API에
접근하기 위한 엔드포인트와 자격증명을 지정할 수 있다. 이것은 기본값이
변경된 경우에만 필요하다.
시크릿은 다음의 명령과 같이 `kubernetes.io/storageos` 유형으로
만들어야 한다.

```shell
kubectl create secret generic storageos-secret \
--type="kubernetes.io/storageos" \
--from-literal=apiAddress=tcp://localhost:5705 \
--from-literal=apiUsername=storageos \
--from-literal=apiPassword=storageos \
--namespace=default
```

동적으로 프로비전된 볼륨에 사용되는 시크릿은 모든 네임스페이스에서
생성할 수 있으며 `adminSecretNamespace` 파라미터로 참조될 수 있다.
사전에 프로비전된 볼륨에서 사용하는 시크릿은 이를 참조하는 PVC와
동일한 네임스페이스에서 작성해야 한다.

### Local

{{< feature-state for_k8s_version="v1.14" state="stable" >}}

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: local-storage
provisioner: kubernetes.io/no-provisioner
volumeBindingMode: WaitForFirstConsumer
```

로컬 볼륨은 현재 동적 프로비저닝을 지원하지 않지만, 파드 스케줄링까지
볼륨 바인딩을 지연시키기 위해서는 스토리지클래스가 여전히 생성되어야 한다. 이것은
`WaitForFirstConsumer` 볼륨 바인딩 모드에 의해 지정된다.

볼륨 바인딩을 지연시키면 스케줄러가 퍼시스턴트볼륨클레임에
적절한 퍼시스턴트볼륨을 선택할 때 파드의 모든 스케줄링
제약 조건을 고려할 수 있다.
