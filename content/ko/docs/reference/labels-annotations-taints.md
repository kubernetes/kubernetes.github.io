---
title: 잘 알려진 레이블, 어노테이션, 테인트(Taint)
content_type: concept
weight: 20
---

<!-- overview -->

쿠버네티스는 모든 레이블과 어노테이션을 `kubernetes.io` 네임스페이스 아래에 정의해 놓았다.

이 문서는 각 값에 대한 레퍼런스를 제공하며, 값을 할당하기 위한 협력 포인트도 제공한다.



<!-- body -->

## kubernetes.io/arch

예시: `kubernetes.io/arch=amd64`

적용 대상: 노드

Go에 의해 정의된 `runtime.GOARCH` 값을 kubelet이 읽어서 이 레이블의 값으로 채운다. arm 노드와 x86 노드를 혼합하여 사용하는 경우 유용할 수 있다.

## kubernetes.io/os

예시: `kubernetes.io/os=linux`

적용 대상: 노드

Go에 의해 정의된 `runtime.GOOS` 값을 kubelet이 읽어서 이 레이블의 값으로 채운다. 클러스터에서 여러 운영체제를 혼합하여 사용(예: 리눅스 및 윈도우 노드)하는 경우 유용할 수 있다.

## kubernetes.io/metadata.name

예시: `kubernetes.io/metadata.name=mynamespace`

적용 대상: 네임스페이스

`NamespaceDefaultLabelName` [기능 게이트](/ko/docs/reference/command-line-tools-reference/feature-gates/)가 
활성화되어 있으면, 
쿠버네티스 API 서버가 모든 네임스페이스에 이 레이블을 적용한다. 
레이블의 값은 네임스페이스의 이름으로 적용된다.

레이블 {{< glossary_tooltip text="셀렉터" term_id="selector" >}}를 이용하여 특정 네임스페이스를 지정하고 싶다면 
이 레이블이 유용할 수 있다.

## beta.kubernetes.io/arch (사용 중단됨)

이 레이블은 사용 중단되었다. 대신 `kubernetes.io/arch` 을 사용한다.

## beta.kubernetes.io/os (사용 중단됨)

이 레이블은 사용 중단되었다. 대신 `kubernetes.io/os` 을 사용한다.

## kubernetes.io/hostname {#kubernetesiohostname}

예시: `kubernetes.io/hostname=ip-172-20-114-199.ec2.internal`

적용 대상: 노드

kubelet이 호스트네임을 읽어서 이 레이블의 값으로 채운다. `kubelet` 에 `--hostname-override` 플래그를 전달하여 실제 호스트네임과 다른 값으로 설정할 수도 있다.

이 레이블은 토폴로지 계층의 일부로도 사용된다. [`topology.kubernetes.io/zone`](#topologykubernetesiozone)에서 세부 사항을 확인한다.


## controller.kubernetes.io/pod-deletion-cost {#pod-deletion-cost}

예시: `controller.kubernetes.io/pod-deletion-cost=10`

적용 대상: Pod

이 어노테이션은 레플리카셋(ReplicaSet) 다운스케일 순서를 조정할 수 있는 요소인 [파드 삭제 비용](/ko/docs/concepts/workloads/controllers/replicaset/#파드-삭제-비용)을 
설정하기 위해 사용한다. 명시된 값은 `int32` 타입으로 파싱된다.

## beta.kubernetes.io/instance-type (사용 중단됨)

{{< note >}} v1.17부터, [`node.kubernetes.io/instance-type`](#nodekubernetesioinstance-type)으로 대체되었다. {{< /note >}}

## node.kubernetes.io/instance-type {#nodekubernetesioinstance-type}

예시: `node.kubernetes.io/instance-type=m3.medium`

적용 대상: 노드

`클라우드 제공자`에 의해 정의된 인스턴스 타입의 값을 kubelet이 읽어서 이 레이블의 값으로 채운다. 
`클라우드 제공자`를 사용하는 경우에만 이 레이블이 설정된다. 
특정 워크로드를 특정 인스턴스 타입에 할당하고 싶다면 이 레이블이 유용할 수 있다. 
하지만 일반적으로는 자원 기반 스케줄링을 수행하는 쿠버네티스 스케줄러를 이용하게 된다. 인스턴스 타입 보다는 특성을 기준으로 스케줄링을 고려해야 한다(예: `g2.2xlarge` 를 요구하기보다는, GPU가 필요하다고 요구한다).

## failure-domain.beta.kubernetes.io/region (사용 중단됨) {#failure-domainbetakubernetesioregion}

[`topology.kubernetes.io/region`](#topologykubernetesioregion)을 확인한다.

{{< note >}} v1.17부터, [`topology.kubernetes.io/region`](#topologykubernetesioregion)으로 대체되었다. {{< /note >}}

## failure-domain.beta.kubernetes.io/zone (사용 중단됨) {#failure-domainbetakubernetesiozone}

[`topology.kubernetes.io/zone`](#topologykubernetesiozone)을 확인한다.

{{< note >}} v1.17부터, [`topology.kubernetes.io/zone`](#topologykubernetesiozone)으로 대체되었다. {{< /note >}}

## statefulset.kubernetes.io/pod-name {#statefulsetkubernetesiopod-name}

예시:

`statefulset.kubernetes.io/pod-name=mystatefulset-7`

스테이트풀셋(StatefulSet) 컨트롤러가 파드를 위한 스테이트풀셋을 생성하면, 컨트롤 플레인이 파드에 이 레이블을 설정한다. 
생성되는 파드의 이름을 이 레이블의 값으로 설정한다.

스테이트풀셋 문서의 [파드 이름 레이블](/ko/docs/concepts/workloads/controllers/statefulset/#파드-이름-레이블)에서 
상세 사항을 확인한다.

## topology.kubernetes.io/region {#topologykubernetesioregion}

예시:

`topology.kubernetes.io/region=us-east-1`

[`topology.kubernetes.io/zone`](#topologykubernetesiozone)을 확인한다.

## topology.kubernetes.io/zone {#topologykubernetesiozone}

예시:

`topology.kubernetes.io/zone=us-east-1c`

적용 대상: 노드, 퍼시스턴트볼륨(PersistentVolume)

노드의 경우: `클라우드 제공자`가 제공하는 값을 이용하여 `kubelet` 또는 외부 `cloud-controller-manager`가 이 어노테이션의 값을 설정한다. `클라우드 제공자`를 사용하는 경우에만 이 레이블이 설정된다. 하지만, 토폴로지 내에서 의미가 있는 경우에만 이 레이블을 노드에 설정해야 한다.

퍼시스턴트볼륨의 경우: 토폴로지 어웨어 볼륨 프로비저너가 자동으로 퍼시스턴트볼륨에 노드 어피니티 제약을 설정한다.

영역(zone)은 논리적 고장 도메인을 나타낸다. 가용성 향상을 위해 일반적으로 쿠버네티스 클러스터는 여러 영역에 걸쳐 구성된다. 영역에 대한 정확한 정의는 사업자 별 인프라 구현에 따라 다르지만, 일반적으로 영역은 '영역 내 매우 낮은 네트워크 지연시간, 영역 내 네트워크 트래픽 비용 없음, 다른 영역의 고장에 독립적임' 등의 공통적인 특성을 갖는다. 예를 들어, 같은 영역 내의 노드는 하나의 네트워크 스위치를 공유하여 활용할 수 있으며, 반대로 다른 영역에 있는 노드는 하나의 네트워크 스위치를 공유해서는 안 된다.

지역(region)은 하나 이상의 영역으로 구성된 더 큰 도메인을 나타낸다. 쿠버네티스 클러스터가 여러 지역에 걸쳐 있는 경우는 드물다. 영역이나 지역에 대한 정확한 정의는 사업자 별 인프라 구현에 따라 다르지만, 일반적으로 지역은 '지역 내 네트워크 지연시간보다 지역 간 네트워크 지연시간이 큼, 지역 간 네트워크 트래픽은 비용이 발생함, 다른 영역/지역의 고장에 독립적임' 등의 공통적인 특성을 갖는다. 예를 들어, 같은 지역 내의 노드는 전력 인프라(예: UPS 또는 발전기)를 공유하여 활용할 수 있으며, 반대로 다른 지역에 있는 노드는 일반적으로 전력 인프라를 공유하지 않는다.

쿠버네티스는 영역과 지역의 구조에 대해 다음과 같이 가정한다.
1) 지역과 영역은 계층적이다. 영역은 지역의 엄격한 부분집합(strict subset)이며, 하나의 영역이 두 개의 지역에 속할 수는 없다.
2) 영역 이름은 모든 지역에 걸쳐서 유일하다. 예를 들어, "africa-east-1" 라는 지역은 "africa-east-1a" 와 "africa-east-1b" 라는 영역으로 구성될 수 있다.

토폴로지 레이블이 변경되는 일은 없다고 가정할 수 있다. 일반적으로 레이블의 값은 변경될 수 있지만, 특정 노드가 삭제 후 재생성되지 않고서는 다른 영역으로 이동할 수 없기 때문이다.

쿠버네티스는 이 정보를 다양한 방식으로 활용할 수 있다. 예를 들어, 단일 영역 클러스터에서는 스케줄러가 자동으로 레플리카셋의 파드를 여러 노드에 퍼뜨린다(노드 고장의 영향을 줄이기 위해 - [`kubernetes.io/hostname`](#kubernetesiohostname) 참고). 복수 영역 클러스터에서는, 여러 영역에 퍼뜨린다(영역 고장의 영향을 줄이기 위해). 이는 _SelectorSpreadPriority_ 를 통해 실현된다.

_SelectorSpreadPriority_ 는 최선 노력(best effort) 배치 방법이다. 클러스터가 위치한 영역들의 특성이 서로 다르다면(예: 노드 숫자가 다름, 노드 타입이 다름, 파드 자원 요구사항이 다름), 파드 숫자를 영역별로 다르게 하여 배치할 수 있다. 필요하다면, 영역들의 특성(노드 숫자/타입)을 일치시켜 불균형 배치의 가능성을 줄일 수 있다.

스케줄러도 (_VolumeZonePredicate_ 표시자를 이용하여) '파드가 요청하는 볼륨'이 위치하는 영역과 같은 영역에 파드를 배치한다. 여러 영역에서 볼륨에 접근할 수는 없다.

`PersistentVolumeLabel`이 퍼시스턴트볼륨의 자동 레이블링을 지원하지 않는다면, 레이블을 수동으로 추가하거나 `PersistentVolumeLabel`이 동작하도록 변경할 수 있다. 
`PersistentVolumeLabel`이 설정되어 있으면, 스케줄러는 파드가 다른 영역에 있는 볼륨에 마운트하는 것을 막는다. 만약 사용 중인 인프라에 이러한 제약이 없다면, 볼륨에 영역 레이블을 추가할 필요가 전혀 없다.

## node.kubernetes.io/windows-build {#nodekubernetesiowindows-build}

예시: `node.kubernetes.io/windows-build=10.0.17763`

적용 대상: 노드

kubelet이 Microsoft 윈도우에서 실행되고 있다면, 사용 중인 Windows Server 버전을 기록하기 위해 kubelet이 노드에 이 레이블을 추가한다.

이 레이블의 값은 "MajorVersion.MinorVersion.BuildNumber"의 형태를 갖는다.

## service.kubernetes.io/headless {#servicekubernetesioheadless}

예시: `service.kubernetes.io/headless=""`

적용 대상: 서비스

서비스가 헤드리스(headless)이면, 컨트롤 플레인이 엔드포인트(Endpoints) 오브젝트에 이 레이블을 추가한다.

## kubernetes.io/service-name {#kubernetesioservice-name}

예시: `kubernetes.io/service-name="nginx"`

적용 대상: 서비스

쿠버네티스가 여러 서비스를 구분하기 위해 이 레이블을 사용한다. 현재는 `ELB`(Elastic Load Balancer) 를 위해서만 사용되고 있다.

## endpointslice.kubernetes.io/managed-by {#endpointslicekubernetesiomanaged-by}

예시: `endpointslice.kubernetes.io/managed-by="controller"`

적용 대상: 엔드포인트슬라이스(EndpointSlices)

이 레이블은 엔드포인트슬라이스(EndpointSlice)를 어떤 컨트롤러나 엔티티가 관리하는지를 나타내기 위해 사용된다. 이 레이블을 사용함으로써 한 클러스터 내에서 여러 엔드포인트슬라이스 오브젝트가 각각 다른 컨트롤러나 엔티티에 의해 관리될 수 있다.

## endpointslice.kubernetes.io/skip-mirror {#endpointslicekubernetesioskip-mirror}

예시: `endpointslice.kubernetes.io/skip-mirror="true"`

적용 대상: 엔드포인트(Endpoints)

특정 자원에 이 레이블을 `"true"` 로 설정하여, EndpointSliceMirroring 컨트롤러가 엔드포인트슬라이스를 이용하여 해당 자원을 미러링하지 않도록 지시할 수 있다.

## service.kubernetes.io/service-proxy-name {#servicekubernetesioservice-proxy-name}

예시: `service.kubernetes.io/service-proxy-name="foo-bar"`

적용 대상: 서비스

kube-proxy 에는 커스텀 프록시를 위한 이와 같은 레이블이 있으며, 이 레이블은 서비스 컨트롤을 커스텀 프록시에 위임한다.

## experimental.windows.kubernetes.io/isolation-type

예시: `experimental.windows.kubernetes.io/isolation-type: "hyperv"`

적용 대상: 파드

Hyper-V 격리(isolation)를 사용하여 윈도우 컨테이너를 실행하려면 이 어노테이션을 사용한다. Hyper-V 격리 기능을 활성화하고 Hyper-V 격리가 적용된 컨테이너를 생성하기 위해, kubelet은 기능 게이트 `HyperVContainer=true` 로 설정하여 실행되어야 하며, 파드에는 `experimental.windows.kubernetes.io/isolation-type=hyperv` 어노테이션이 설정되어 있어야 한다.

{{< note >}}
이 어노테이션은 하나의 컨테이너로 구성된 파드에만 설정할 수 있다.
{{< /note >}}

## ingressclass.kubernetes.io/is-default-class

예시: `ingressclass.kubernetes.io/is-default-class: "true"`

적용 대상: 인그레스클래스(IngressClass)

하나의 인그레스클래스 리소스에 이 어노테이션이 `"true"`로 설정된 경우, 클래스가 명시되지 않은 새로운 인그레스(Ingress) 리소스는 해당 기본 클래스로 할당될 것이다.

## kubernetes.io/ingress.class (사용 중단됨)

{{< note >}}
v1.18부터, `spec.ingressClassName`으로 대체되었다.
{{< /note >}}

## storageclass.kubernetes.io/is-default-class

예시: `storageclass.kubernetes.io/is-default-class=true`

적용 대상: 스토리지클래스(StorageClass)

하나의 스토리지클래스(StorageClass) 리소스에 이 어노테이션이 `"true"`로 설정된 경우, 
클래스가 명시되지 않은 새로운 퍼시스턴트볼륨클레임(PersistentVolumeClaim) 리소스는 해당 기본 클래스로 할당될 것이다.

## alpha.kubernetes.io/provided-node-ip

예시: `alpha.kubernetes.io/provided-node-ip: "10.0.0.1"`

적용 대상: 노드

kubelet이 노드에 할당된 IPv4 주소를 명시하기 위해 이 어노테이션을 사용할 수 있다.

kubelet이 "외부" 클라우드 제공자에 의해 실행되었다면, 명령줄 플래그(`--node-ip`)를 통해 설정된 IP 주소를 명시하기 위해 kubelet이 이 어노테이션을 노드에 설정한다. cloud-controller-manager는 클라우드 제공자에게 이 IP 주소가 유효한지를 검증한다.

## batch.kubernetes.io/job-completion-index

예시: `batch.kubernetes.io/job-completion-index: "3"`

적용 대상: 파드

kube-controller-manager의 잡(Job) 컨트롤러는 
`Indexed` [완료 모드](/ko/docs/concepts/workloads/controllers/job/#완료-모드)로 생성된 파드에 이 어노테이션을 추가한다.

## kubectl.kubernetes.io/default-container

예시: `kubectl.kubernetes.io/default-container: "front-end-app"`

파드의 기본 컨테이너로 사용할 컨테이너 이름을 지정하는 어노테이션이다. 예를 들어, `kubectl logs` 또는 `kubectl exec` 명령을 사용할 때 `-c` 또는 `--container` 플래그를 지정하지 않으면, 이 어노테이션으로 명시된 기본 컨테이너를 대상으로 실행될 것이다.

## endpoints.kubernetes.io/over-capacity

예시: `endpoints.kubernetes.io/over-capacity:warning`

적용 대상: 엔드포인트(Endpoints)

v1.21 이상의 쿠버네티스 클러스터에서, 엔드포인트(Endpoints) 컨트롤러가 1000개 이상의 엔드포인트를 관리하고 있다면 각 엔드포인트 리소스에 이 어노테이션을 추가한다. 이 어노테이션은 엔드포인트 리소스가 용량 초과 되었음을 나타낸다.

**이 이후로 나오는 테인트는 모두 '적용 대상: 노드' 이다.**

## node.kubernetes.io/not-ready

예시: `node.kubernetes.io/not-ready:NoExecute`

노드 컨트롤러는 노드의 헬스를 모니터링하여 노드가 사용 가능한 상태인지를 감지하고 그에 따라 이 테인트를 추가하거나 제거한다.

## node.kubernetes.io/unreachable

예시: `node.kubernetes.io/unreachable:NoExecute`

노드 컨트롤러는 [노드 컨디션](/ko/docs/concepts/architecture/nodes/#condition)이 `Ready`에서 `Unknown`으로 변경된 노드에 이 테인트를 추가한다.

## node.kubernetes.io/unschedulable

예시: `node.kubernetes.io/unschedulable:NoSchedule`

경쟁 상태(race condition) 발생을 막기 위해, 생성 중인 노드에 이 테인트가 추가된다.

## node.kubernetes.io/memory-pressure

예시: `node.kubernetes.io/memory-pressure:NoSchedule`

kubelet은 노드의 `memory.available`와 `allocatableMemory.available`을 관측하여 메모리 압박을 감지한다. 그 뒤, 관측한 값을 kubelet에 설정된 문턱값(threshold)과 비교하여 노드 컨디션과 테인트의 추가/삭제 여부를 결정한다.

## node.kubernetes.io/disk-pressure

예시: `node.kubernetes.io/disk-pressure:NoSchedule`

kubelet은 노드의 `imagefs.available`, `imagefs.inodesFree`, `nodefs.available`, `nodefs.inodesFree`(리눅스에 대해서만)를 관측하여 디스크 압박을 감지한다. 그 뒤, 관측한 값을 kubelet에 설정된 문턱값(threshold)과 비교하여 노드 컨디션과 테인트의 추가/삭제 여부를 결정한다.

## node.kubernetes.io/network-unavailable

예시: `node.kubernetes.io/network-unavailable:NoSchedule`

사용 중인 클라우드 공급자가 추가 네트워크 환경설정을 필요로 한다고 명시하면, kubelet이 이 테인트를 설정한다. 클라우드 상의 네트워크 경로가 올바르게 구성되어야, 클라우드 공급자가 이 테인트를 제거할 것이다.

## node.kubernetes.io/pid-pressure

예시: `node.kubernetes.io/pid-pressure:NoSchedule`

kubelet은 '`/proc/sys/kernel/pid_max`의 크기의 D-값'과 노드에서 쿠버네티스가 사용 중인 PID를 확인하여, `pid.available` 지표라고 불리는 '사용 가능한 PID 수'를 가져온다. 그 뒤, 관측한 지표를 kubelet에 설정된 문턱값(threshold)과 비교하여 노드 컨디션과 테인트의 추가/삭제 여부를 결정한다.

## node.cloudprovider.kubernetes.io/uninitialized

예시: `node.cloudprovider.kubernetes.io/uninitialized:NoSchedule`

kubelet이 "외부" 클라우드 공급자에 의해 실행되었다면 노드가 '사용 불가능'한 상태라고 표시하기 위해 이 테인트가 추가되며, 추후 cloud-controller-manager가 이 노드를 초기화하고 이 테인트를 제거한다.

## node.cloudprovider.kubernetes.io/shutdown

예시: `node.cloudprovider.kubernetes.io/shutdown:NoSchedule`

노드의 상태가 클라우드 공급자가 정의한 'shutdown' 상태이면, 이에 따라 노드에 `node.cloudprovider.kubernetes.io/shutdown` 테인트가 `NoSchedule` 값으로 설정된다.
