---
reviewers:
title: 고가용성 쿠버네티스 클러스터 컨트롤 플레인 설정하기
content_type: task
---

<!-- overview -->

{{< feature-state for_k8s_version="v1.5" state="alpha" >}}

구글 컴퓨트 엔진(Google Compute Engine, 이하 GCE)의 `kube-up`이나 `kube-down` 스크립트에 쿠버네티스 컨트롤 플레인 노드를 복제할 수 있다.
이 문서는 kube-up/down 스크립트를 사용하여 고가용(HA) 컨트롤 플레인을 관리하는 방법과 GCE와 함께 사용하기 위해 HA 컨트롤 플레인을 구현하는 방법에 관해 설명한다.




## {{% heading "prerequisites" %}}


{{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}



<!-- steps -->

## HA 호환 클러스터 시작

새 HA 호환 클러스터를 생성하려면, `kube-up` 스크립트에 다음 플래그를 설정해야 한다.

* `MULTIZONE=true` - 서버의 기본 영역(zone)과 다른 영역에서 컨트롤 플레인 kubelet이 제거되지 않도록 한다.
여러 영역에서 컨트롤 플레인 노드를 실행(권장됨)하려는 경우에 필요하다.

* `ENABLE_ETCD_QUORUM_READ=true` - 모든 API 서버에서 읽은 내용이 최신 데이터를 반환하도록 하기 위한 것이다.
true인 경우, Etcd의 리더 복제본에서 읽는다.
이 값을 true로 설정하는 것은 선택 사항이다. 읽기는 더 안정적이지만 느리게 된다.

선택적으로, 첫 번째 컨트롤 플레인 노드가 생성될 GCE 영역을 지정할 수 있다.
다음 플래그를 설정한다.

* `KUBE_GCE_ZONE=zone` - 첫 번째 컨트롤 플레인 노드가 실행될 영역.

다음 샘플 커맨드는 europe-west1-b GCE 영역에 HA 호환 클러스터를 구성한다.

```shell
MULTIZONE=true KUBE_GCE_ZONE=europe-west1-b  ENABLE_ETCD_QUORUM_READS=true ./cluster/kube-up.sh
```

위의 커맨드는 하나의 컨트롤 플레인 노드를 포함하는 클러스터를 생성한다.
그러나 후속 커맨드로 새 컨트롤 플레인 노드를 추가할 수 있다.

## 새 컨트롤 플레인 노드 추가

HA 호환 클러스터를 생성했다면, 여기에 컨트롤 플레인 노드를 추가할 수 있다.
`kube-up` 스크립트에 다음 플래그를 사용하여 컨트롤 플레인 노드를 추가한다.

* `KUBE_REPLICATE_EXISTING_MASTER=true` - 기존 컨트롤 플레인 노드의 복제본을
만든다.

* `KUBE_GCE_ZONE=zone` - 컨트롤 플레인 노드가 실행될 영역.
반드시 다른 컨트롤 플레인 노드가 존재하는 영역과 동일한 지역(region)에 있어야 한다.

HA 호환 클러스터를 시작할 때, 상속되는 `MULTIZONE`이나 `ENABLE_ETCD_QUORUM_READS` 플래그를 따로
설정할 필요는 없다.

다음 샘플 커맨드는 기존 HA 호환 클러스터에서 
컨트롤 플레인 노드를 복제한다.

```shell
KUBE_GCE_ZONE=europe-west1-c KUBE_REPLICATE_EXISTING_MASTER=true ./cluster/kube-up.sh
```

## 컨트롤 플레인 노드 제거

다음 플래그가 있는 `kube-down` 스크립트를 사용하여 HA 클러스터에서 컨트롤 플레인 노드를 제거할 수 있다.

* `KUBE_DELETE_NODES=false` - kubelet을 삭제하지 않기 위한 것이다.

* `KUBE_GCE_ZONE=zone` - 컨트롤 플레인 노드가 제거될 영역.

* `KUBE_REPLICA_NAME=replica_name` - (선택) 제거할 컨트롤 플레인 노드의 이름.
명시하지 않으면, 해당 영역의 모든 복제본이 제거된다.

다음 샘플 커맨드는 기존 HA 클러스터에서 컨트롤 플레인 노드를 제거한다.

```shell
KUBE_DELETE_NODES=false KUBE_GCE_ZONE=europe-west1-c ./cluster/kube-down.sh
```

## 동작에 실패한 컨트롤 플레인 노드 처리

HA 클러스터의 컨트롤 플레인 노드 중 하나가 동작에 실패하면,
클러스터에서 해당 노드를 제거하고 동일한 영역에 새 컨트롤 플레인 노드를 추가하는 것이 가장 좋다.
다음 샘플 커맨드로 이 과정을 시연한다.

1. 손상된 복제본을 제거한다.

    ```shell
    KUBE_DELETE_NODES=false KUBE_GCE_ZONE=replica_zone KUBE_REPLICA_NAME=replica_name ./cluster/kube-down.sh
    ```

1. 기존 복제본 대신 새 노드를 추가한다.

    ```shell
    KUBE_GCE_ZONE=replica-zone KUBE_REPLICATE_EXISTING_MASTER=true ./cluster/kube-up.sh
    ```

## HA 클러스터에서 컨트롤 플레인 노드 복제에 관한 모범 사례

* 다른 영역에 컨트롤 플레인 노드를 배치하도록 한다. 한 영역이 동작에 실패하는 동안, 
해당 영역에 있는 컨트롤 플레인 노드도 모두 동작에 실패할 것이다.
영역 장애를 극복하기 위해 노드를 여러 영역에 배치한다
(더 자세한 내용은 [멀티 영역](/ko/docs/setup/best-practices/multiple-zones/)를 참조한다).

* 두 개의 노드로 구성된 컨트롤 플레인은 사용하지 않는다. 두 개의 노드로 구성된 
컨트롤 플레인에서의 합의를 위해서는 지속적 상태(persistent state) 변경 시 두 컨트롤 플레인 노드가 모두 정상적으로 동작 중이어야 한다.
결과적으로 두 컨트롤 플레인 노드 모두 필요하고, 둘 중 한 컨트롤 플레인 노드에만 장애가 발생해도 
클러스터의 심각한 장애 상태를 초래한다.
따라서 HA 관점에서는 두 개의 노드로 구성된 컨트롤 플레인은 
단일 노드로 구성된 컨트롤 플레인보다도 못하다.

* 컨트롤 플레인 노드를 추가하면, 클러스터의 상태(Etcd)도 새 인스턴스로 복사된다.
클러스터가 크면, 이 상태를 복제하는 시간이 오래 걸릴 수 있다.
이 작업은 [etcd 관리 가이드](https://etcd.io/docs/v2.3/admin_guide/#member-migration)에 기술한 대로
Etcd 데이터 디렉터리를 마이그레이션하여 속도를 높일 수 있다(향후에 Etcd 데이터 디렉터리 마이그레이션 지원 추가를 고려 중이다).



<!-- discussion -->

## 구현 지침

![ha-master-gce](/images/docs/ha-master-gce.png)

### 개요

각 컨트롤 플레인 노드는 다음 모드에서 다음 구성 요소를 실행한다.

* Etcd 인스턴스: 모든 인스턴스는 합의를 사용하여 함께 클러스터화 한다.

* API 서버: 각 서버는 내부 Etcd와 통신한다. 클러스터의 모든 API 서버가 가용하게 된다.

* 컨트롤러, 스케줄러, 클러스터 오토스케일러: 임대 방식을 이용한다. 각 인스턴스 중 하나만이 클러스터에서 활성화된다.

* 애드온 매니저: 각 매니저는 애드온의 동기화를 유지하려고 독립적으로 작업한다.

또한 API 서버 앞단에 외부/내부 트래픽을 라우팅하는 로드 밸런서가 있을 것이다.

### 로드 밸런싱

두 번째 컨트롤 플레인 노드를 배치할 때, 두 개의 복제본에 대한 로드 밸런서가 생성될 것이고, 첫 번째 복제본의 IP 주소가 로드 밸런서의 IP 주소로 승격된다.
비슷하게 끝에서 두 번째의 컨트롤 플레인 노드를 제거한 후에는 로드 밸런서가 제거되고
해당 IP 주소는 마지막으로 남은 복제본에 할당된다.
로드 밸런서 생성 및 제거는 복잡한 작업이며, 이를 전파하는 데 시간(~20분)이 걸릴 수 있다.

### 마스터 서비스와 Kubelet

쿠버네티스 서비스에서 최신의 쿠버네티스 API 서버 목록을 유지하는 대신,
시스템은 모든 트래픽을 외부 IP 주소로 보낸다.

* 단일 노드 컨트롤 플레인의 경우, IP 주소는 단일 컨트롤 플레인 노드를 가리킨다.

* 고가용성 컨트롤 플레인의 경우, IP 주소는 마스터 앞의 로드밸런서를 가리킨다.

마찬가지로 Kubelet은 외부 IP 주소를 사용하여 컨트롤 플레인과 통신한다.

### 컨트롤 플레인 노드 인증서

쿠버네티스는 각 컨트롤 플레인 노드의 외부 퍼블릭 IP 주소와 내부 IP 주소를 대상으로 TLS 인증서를 발급한다.
컨트롤 플레인 노드의 임시 퍼블릭 IP 주소에 대한 인증서는 없다.
임시 퍼블릭 IP 주소를 통해 컨트롤 플레인 노드에 접근하려면, TLS 검증을 건너뛰어야 한다.

### etcd 클러스터화

etcd를 클러스터로 구축하려면, etcd 인스턴스간 통신에 필요한 포트를 열어야 한다(클러스터 내부 통신용).
이러한 배포를 안전하게 하기 위해, etcd 인스턴스간의 통신은 SSL을 이용하여 승인한다.

### API 서버 신원

{{< feature-state state="alpha" for_k8s_version="v1.20" >}}

API 서버 식별 기능은
[기능 게이트](/ko/docs/reference/command-line-tools-reference/feature-gates/)에
의해 제어되며 기본적으로 활성화되지 않는다.
{{< glossary_tooltip text="API 서버" term_id="kube-apiserver" >}}
시작 시 `APIServerIdentity` 라는 기능 게이트를 활성화하여 API 서버 신원을 활성화할 수 있다.

```shell
kube-apiserver \
--feature-gates=APIServerIdentity=true \
 # …다른 플래그는 평소와 같다.
```

부트스트랩 중에 각 kube-apiserver는 고유한 ID를 자신에게 할당한다. ID는
`kube-apiserver-{UUID}` 형식이다. 각 kube-apiserver는
_kube-system_ {{< glossary_tooltip text="네임스페이스" term_id="namespace">}}에
[임대](/docs/reference/generated/kubernetes-api/{{< param "version" >}}//#lease-v1-coordination-k8s-io)를 생성한다.
임대 이름은 kube-apiserver의 고유 ID이다. 임대에는
`k8s.io/component=kube-apiserver` 라는 레이블이 있다. 각 kube-apiserver는
`IdentityLeaseRenewIntervalSeconds` (기본값은 10초)마다 임대를 새로 갱신한다. 각
kube-apiserver는 `IdentityLeaseDurationSeconds` (기본값은 3600초)마다
모든 kube-apiserver 식별 ID 임대를 확인하고,
`IdentityLeaseDurationSeconds` 이상 갱신되지 않은 임대를 삭제한다.
`IdentityLeaseRenewIntervalSeconds` 및 `IdentityLeaseDurationSeconds`는
kube-apiserver 플래그 `identity-lease-renew-interval-seconds`
및 `identity-lease-duration-seconds`로 구성된다.

이 기능을 활성화하는 것은 HA API 서버 조정과 관련된 기능을
사용하기 위한 전제조건이다(예: `StorageVersionAPI` 기능 게이트).

## 추가 자료

[자동화된 HA 마스터 배포 - 제안 문서](https://git.k8s.io/community/contributors/design-proposals/cluster-lifecycle/ha_master.md)
