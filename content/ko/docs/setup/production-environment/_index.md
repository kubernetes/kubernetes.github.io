---
title: "프로덕션 환경"
description: 프로덕션 수준의 쿠버네티스 클러스터 생성
weight: 30
no_list: true
---
<!-- overview -->

프로덕션 수준의 쿠버네티스 클러스터에는 계획과 준비가 필요하다.
쿠버네티스 클러스터에 중요한 워크로드를 실행하려면 클러스터를 탄력적이도록 구성해야 한다.
이 페이지에서는 프로덕션용 클러스터를 설정하거나 기존 클러스터를 프로덕션용으로 업그레이드하기 위해 
수행할 수 있는 단계를 설명한다.
이미 프로덕션 구성 내용에 익숙하여 단지 링크를 찾고 있다면, 
[다음 내용](#다음-내용)을 참고한다.

<!-- body -->

## 프로덕션 고려 사항

일반적으로 프로덕션 쿠버네티스 클러스터 환경에는 
개인 학습용, 개발용 또는 테스트 환경용 클러스터보다 더 많은 요구 사항이 있다. 
프로덕션 환경에는 많은 사용자의 보안 액세스, 일관된 가용성 및 
변화하는 요구를 충족하기 위한 리소스가 필요할 수 있다.

프로덕션 쿠버네티스 환경이 상주할 위치(온 프레미스 또는 클라우드)와 
직접 처리하거나 다른 사람에게 맡길 관리의 양을 결정할 때, 
쿠버네티스 클러스터에 대한 요구 사항이 
다음 이슈에 의해 어떻게 영향을 받는지 고려해야 한다.

- *가용성*: 단일 머신 쿠버네티스 [학습 환경](/ko/docs/setup/#학습-환경)은 SPOF(Single Point of Failure, 단일 장애 지점) 이슈를 갖고 있다.
고가용성 클러스터를 만드는 것에는 다음과 같은 고려 사항이 있다.
  - 컨트롤 플레인과 워크 노드를 분리
  - 컨트롤 플레인 구성요소를 여러 노드에 복제
  - 클러스터의 {{< glossary_tooltip term_id="kube-apiserver" text="API 서버" >}}로 가는 트래픽을 로드밸런싱
  - 워커 노드를 충분히 운영하거나, 워크로드 변경에 따라 빠르게 제공할 수 있도록 보장

- *스케일링*: 프로덕션 쿠버네티스 환경에 들어오는 요청의 양의 
일정할 것으로 예상된다면, 필요한 만큼의 용량(capacity)을 증설하고 
마무리할 수도 있다. 하지만, 요청의 양이 시간에 따라 점점 증가하거나 
계절, 이벤트 등에 의해 극적으로 변동할 것으로 예상된다면, 
컨트롤 플레인과 워커 노드로의 요청 증가로 인한 압박을 해소하기 위해 스케일 업 하거나 
잉여 자원을 줄이기 위해 스케일 다운 하는 것에 대해 고려해야 한다.

- *보안 및 접근 관리*: 학습을 위한 쿠버네티스 클러스터에는 
완전한 관리 권한을 가질 수 있다. 하지만 중요한 워크로드를 실행하며 
두 명 이상의 사용자가 있는 공유 클러스터에는 누가, 그리고 무엇이 클러스터 자원에 
접근할 수 있는지에 대해서 보다 정교한 접근 방식이 필요하다.
역할 기반 접근 제어([RBAC](/docs/reference/access-authn-authz/rbac/)) 및 
기타 보안 메커니즘을 사용하여, 사용자와 워크로드가 필요한 자원에 
액세스할 수 있게 하면서도 워크로드와 클러스터를 안전하게 유지할 수 있다. 
[정책](/ko/docs/concepts/policy/)과 
[컨테이너 리소스](/ko/docs/concepts/configuration/manage-resources-containers/)를 
관리하여, 사용자 및 워크로드가 접근할 수 있는 자원에 대한 제한을 설정할 수 있다.

쿠버네티스 프로덕션 환경을 직접 구축하기 전에, 이 작업의 일부 또는 전체를 
[턴키 클라우드 솔루션](/ko/docs/setup/production-environment/turnkey-solutions/) 
제공 업체 또는 기타 [쿠버네티스 파트너](/ko/partners/)에게 
넘기는 것을 고려할 수 있다.
다음과 같은 옵션이 있다.

- *서버리스*: 클러스터를 전혀 관리하지 않고 
타사 장비에서 워크로드를 실행하기만 하면 된다. 
CPU 사용량, 메모리 및 디스크 요청과 같은 항목에 대한 요금이 부과된다.
- *관리형 컨트롤 플레인*: 쿠버네티스 서비스 공급자가 
클러스터 컨트롤 플레인의 확장 및 가용성을 관리하고 패치 및 업그레이드를 처리하도록 한다.
- *관리형 워커 노드*: 필요에 맞는 노드 풀을 정의하면, 
쿠버네티스 서비스 공급자는 해당 노드의 가용성 및 
필요 시 업그레이드 제공을 보장한다.
- *통합*: 쿠버네티스를 스토리지, 컨테이너 레지스트리, 
인증 방법 및 개발 도구와 같이 
사용자가 필요로 하는 여러 서비스를 통합 제공하는 업체도 있다.

프로덕션 쿠버네티스 클러스터를 직접 구축하든 파트너와 협력하든, 
요구 사항이 *컨트롤 플레인*, *워커 노드*, 
*사용자 접근*, *워크로드 자원*과 관련되기 때문에, 
다음 섹션들을 검토하는 것이 바람직하다.

## 프로덕션 클러스터 구성

프로덕션 수준 쿠버네티스 클러스터에서, 
컨트롤 플레인은 다양한 방식으로 여러 컴퓨터에 분산될 수 있는 서비스들을 통해 
클러스터를 관리한다. 
반면, 각 워커 노드는 쿠버네티스 파드를 실행하도록 구성된 단일 엔티티를 나타낸다.

### 프로덕션 컨트롤 플레인

가장 간단한 쿠버네티스 클러스터는 모든 컨트롤 플레인 및 워커 노드 서비스가 
하나의 머신에 실행되는 클러스터이다. 
[쿠버네티스 컴포넌트](/ko/docs/concepts/overview/components/) 
그림에 명시된 대로, 워커 노드를 추가하여 해당 환경을 확장할 수 있다. 
클러스터를 단기간만 사용하거나, 
심각한 문제가 발생한 경우 폐기하는 것이 가능하다면, 이 방식을 선택할 수 있다.

그러나 더 영구적이고 가용성이 높은 클러스터가 필요한 경우 
컨트롤 플레인 확장을 고려해야 한다. 
설계 상, 단일 시스템에서 실행되는 단일 시스템 컨트롤 플레인 서비스는 
가용성이 높지 않다.
클러스터를 계속 유지하면서 문제가 발생한 경우 복구할 수 있는지 여부가 중요한 경우, 
다음 사항들을 고려한다.

- *배포 도구 선택*: kubeadm, kops, kubespray와 같은 도구를 이용해 
컨트롤 플레인을 배포할 수 있다. 
[배포 도구로 쿠버네티스 설치하기](/ko/docs/setup/production-environment/tools/)에서 
여러 배포 도구를 이용한 프로덕션 수준 배포에 대한 팁을 확인한다. 
배포 시, 다양한 
[컨테이너 런타임](/ko/docs/setup/production-environment/container-runtimes/)을 사용할 수 있다.
- *인증서 관리*: 컨트롤 플레인 서비스 간의 보안 통신은 인증서를 사용하여 구현된다. 
인증서는 배포 중에 자동으로 생성되거나, 또는 자체 인증 기관을 사용하여 생성할 수 있다. 
[PKI 인증서 및 요구 조건](/ko/docs/setup/best-practices/certificates/)에서 
상세 사항을 확인한다.
- *apiserver를 위한 로드밸런서 구성*: 여러 노드에서 실행되는 apiserver 서비스 인스턴스에 
외부 API 호출을 분산할 수 있도록 로드밸런서를 구성한다. 
[외부 로드밸런서 생성하기](/docs/tasks/access-application-cluster/create-external-load-balancer/)에서 
상세 사항을 확인한다.
- *etcd 서비스 분리 및 백업*: etcd 서비스는 
다른 컨트롤 플레인 서비스와 동일한 시스템에서 실행되거나, 
또는 추가 보안 및 가용성을 위해 별도의 시스템에서 실행될 수 있다. 
etcd는 클러스터 구성 데이터를 저장하므로 
필요한 경우 해당 데이터베이스를 복구할 수 있도록 etcd 데이터베이스를 정기적으로 백업해야 한다.
[etcd FAQ](https://etcd.io/docs/v3.4/faq/)에서 etcd 구성 및 사용 상세를 확인한다.
[쿠버네티스를 위한 etcd 클러스터 운영하기](/docs/tasks/administer-cluster/configure-upgrade-etcd/)와 
[kubeadm을 이용하여 고가용성 etcd 생성하기](/docs/setup/production-environment/tools/kubeadm/setup-ha-etcd-with-kubeadm/)에서 
상세 사항을 확인한다.
- *다중 컨트롤 플레인 시스템 구성*: 고가용성을 위해, 
컨트롤 플레인은 단일 머신으로 제한되지 않아야 한다. 
컨트롤 플레인 서비스가 init 서비스(예: systemd)에 의해 실행되는 경우, 
각 서비스는 최소 3대의 머신에서 실행되어야 한다. 
그러나, 컨트롤 플레인 서비스를 쿠버네티스 상의 파드 형태로 실행하면 
각 서비스 복제본 요청이 보장된다. 
스케줄러는 내결함성이 있어야 하고, 고가용성은 필요하지 않다.
일부 배포 도구는 쿠버네티스 서비스의 리더 선출을 수행하기 위해 
[Raft](https://raft.github.io/) 합의 알고리즘을 설정한다. 
리더를 맡은 서비스가 사라지면 다른 서비스가 스스로 리더가 되어 인계를 받는다.
- *다중 영역(zone)으로 확장*: 클러스터를 항상 사용 가능한 상태로 유지하는 것이 중요하다면 
여러 데이터 센터(클라우드 환경에서는 '영역'이라고 함)에서 실행되는 
클러스터를 만드는 것이 좋다. 
영역의 그룹을 지역(region)이라고 한다.
동일한 지역의 여러 영역에 클러스터를 분산하면 
하나의 영역을 사용할 수 없게 된 경우에도 클러스터가 계속 작동할 가능성을 높일 수 있다. 
[여러 영역에서 실행](/ko/docs/setup/best-practices/multiple-zones/)에서 상세 사항을 확인한다.
- *구동 중인 기능 관리*: 클러스터를 계속 유지하려면, 
상태 및 보안을 유지하기 위해 수행해야 하는 작업이 있다. 
예를 들어 kubeadm으로 클러스터를 생성한 경우, 
[인증서 관리](/ko/docs/tasks/administer-cluster/kubeadm/kubeadm-certs/)와 
[kubeadm 클러스터 업그레이드하기](/ko/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/)에 대해 도움이 되는 가이드가 있다.
[클러스터 운영하기](/ko/docs/tasks/administer-cluster/)에서 
더 많은 쿠버네티스 관리 작업을 볼 수 있다.

컨트롤 플레인 서비스를 실행할 때 사용 가능한 옵션에 대해 보려면, 
[kube-apiserver](/docs/reference/command-line-tools-reference/kube-apiserver/),
[kube-controller-manager](/docs/reference/command-line-tools-reference/kube-controller-manager/), 
[kube-scheduler](/docs/reference/command-line-tools-reference/kube-scheduler/)를 참조한다.
고가용성 컨트롤 플레인 예제는 
[고가용성 토폴로지를 위한 옵션](/ko/docs/setup/production-environment/tools/kubeadm/ha-topology/),
[kubeadm을 이용하여 고가용성 클러스터 생성하기](/docs/setup/production-environment/tools/kubeadm/high-availability/),
[쿠버네티스를 위한 etcd 클러스터 운영하기](/docs/tasks/administer-cluster/configure-upgrade-etcd/)를 참조한다.
etcd 백업 계획을 세우려면 
[etcd 클러스터 백업하기](/docs/tasks/administer-cluster/configure-upgrade-etcd/#backing-up-an-etcd-cluster)를 참고한다.

### 프로덕션 워커 노드

프로덕션 수준 워크로드는 복원력이 있어야 하고, 
이들이 의존하는 모든 것들(예: CoreDNS)도 복원력이 있어야 한다. 
컨트롤 플레인을 자체적으로 관리하든 
클라우드 공급자가 대신 수행하도록 하든 상관없이, 
워커 노드(간단히 *노드*라고도 함)를 어떤 방법으로 관리할지 고려해야 한다.

- *노드 구성하기*: 노드는 물리적 또는 가상 머신일 수 있다. 
직접 노드를 만들고 관리하려면 지원되는 운영 체제를 설치한 다음 
적절한 [노드 서비스](/ko/docs/concepts/overview/components/#노드-컴포넌트)를 추가하고 실행한다.
다음을 고려해야 한다.
  - 워크로드의 요구 사항 (노드가 적절한 메모리, CPU, 디스크 속도, 저장 용량을 갖도록 구성)
  - 일반적인 컴퓨터 시스템이면 되는지, 아니면 GPU, 윈도우 노드, 또는 VM 격리를 필요로 하는 워크로드가 있는지
- *노드 검증하기*: [노드 구성 검증하기](/ko/docs/setup/best-practices/node-conformance/)에서 
노드가 쿠버네티스 클러스터에 조인(join)에 필요한 요구 사항을 
만족하는지 확인하는 방법을 알아본다.
- *클러스터에 노드 추가하기*: 클러스터를 자체적으로 관리하는 경우, 
머신을 준비하고, 클러스터의 apiserver에 이를 수동으로 추가하거나 
또는 머신이 스스로 등록하도록 하여 노드를 추가할 수 있다. 
이러한 방식으로 노드를 추가하는 방법을 보려면 [노드](/ko/docs/concepts/architecture/nodes/) 섹션을 확인한다.
- *클러스터에 윈도우 노드 추가하기*: 윈도우 컨테이너로 구현된 워크로드를 
실행할 수 있도록, 쿠버네티스는 윈도우 워커 노드를 지원한다. 
[쿠버네티스에서의 윈도우](/ko/docs/setup/production-environment/windows/)에서 상세 사항을 확인한다.
- *노드 스케일링*: 클러스터가 최종적으로 필요로 하게 될 용량만큼 
확장하는 것에 대한 계획이 있어야 한다. 
실행해야 하는 파드 및 컨테이너 수에 따라 필요한 노드 수를 판별하려면 
[대형 클러스터에 대한 고려 사항](/ko/docs/setup/best-practices/cluster-large/)을 확인한다. 
만약 노드를 직접 관리한다면, 직접 물리적 장비를 구입하고 설치해야 할 수도 있음을 의미한다.
- *노드 자동 스케일링*: 대부분의 클라우드 공급자는 
비정상 노드를 교체하거나 수요에 따라 노드 수를 늘리거나 줄일 수 있도록 
[클러스터 오토스케일러](https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler#readme)를 지원한다. 
[자주 묻는 질문](https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/FAQ.md)에서 
오토스케일러가 어떻게 동작하는지, 
[배치](https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler#deployment) 섹션에서 
각 클라우드 공급자별로 어떻게 구현했는지를 확인한다. 
온프레미스의 경우, 필요에 따라 새 노드를 가동하도록 
스크립트를 구성할 수 있는 가상화 플랫폼이 있다.
- *노드 헬스 체크 구성*: 중요한 워크로드의 경우, 
해당 노드에서 실행 중인 노드와 파드의 상태가 정상인지 확인하고 싶을 것이다. 
[Node Problem Detector](/docs/tasks/debug-application-cluster/monitor-node-health/) 
데몬을 사용하면 노드가 정상인지 확인할 수 있다.

## 프로덕션 사용자 관리

프로덕션에서는, 클러스터를 한 명 또는 여러 명이 사용하던 모델에서 
수십에서 수백 명이 사용하는 모델로 바꿔야 하는 경우가 발생할 수 있다. 
학습 환경 또는 플랫폼 프로토타입에서는 모든 작업에 대한 단일 관리 계정으로도 
충분할 수 있다. 프로덕션에서는 여러 네임스페이스에 대한, 액세스 수준이 
각각 다른 더 많은 계정이 필요하다.

프로덕션 수준의 클러스터를 사용한다는 것은 
다른 사용자의 액세스를 선택적으로 허용할 방법을 결정하는 것을 의미한다. 
특히 클러스터에 액세스를 시도하는 사용자의 신원을 확인(인증, authentication)하고 
요청한 작업을 수행할 권한이 있는지 결정(인가, authorization)하기 위한 
다음과 같은 전략을 선택해야 한다.

- *인증*: apiserver는 클라이언트 인증서, 전달자 토큰, 인증 프록시 또는 
HTTP 기본 인증을 사용하여 사용자를 인증할 수 있다.
사용자는 인증 방법을 선택하여 사용할 수 있다.
apiserver는 또한 플러그인을 사용하여 
LDAP 또는 Kerberos와 같은 조직의 기존 인증 방법을 활용할 수 있다.
쿠버네티스 사용자를 인증하는 다양한 방법에 대한 설명은 
[인증](/docs/reference/access-authn-authz/authentication/)을 참조한다.
- *인가*: 일반 사용자 인가를 위해, RBAC 와 ABAC 중 하나를 선택하여 사용할 수 있다. [인가 개요](/ko/docs/reference/access-authn-authz/authorization/)에서 사용자 계정과 서비스 어카운트 인가를 위한 여러 가지 모드를 확인할 수 있다.
  - *역할 기반 접근 제어* ([RBAC](/docs/reference/access-authn-authz/rbac/)): 인증된 사용자에게 특정 권한 집합을 허용하여 클러스터에 대한 액세스를 할당할 수 있다. 특정 네임스페이스(Role) 또는 전체 클러스터(ClusterRole)에 권한을 할당할 수 있다. 그 뒤에 RoleBindings 및 ClusterRoleBindings를 사용하여 해당 권한을 특정 사용자에게 연결할 수 있다.
  - *속성 기반 접근 제어* ([ABAC](/docs/reference/access-authn-authz/abac/)): 클러스터의 리소스 속성을 기반으로 정책을 생성하고 이러한 속성을 기반으로 액세스를 허용하거나 거부할 수 있다. 정책 파일의 각 줄은 버전 관리 속성(apiVersion 및 종류), 그리고 '대상(사용자 또는 그룹)', '리소스 속성', '비 리소스 속성(`/version` 또는 `/apis`)' 및 '읽기 전용'과 일치하는 사양 속성 맵을 식별한다. 자세한 내용은 [예시](/docs/reference/access-authn-authz/abac/#examples)를 참조한다.

프로덕션 쿠버네티스 클러스터에 인증과 인가를 설정할 때, 다음의 사항을 고려해야 한다.

- *인가 모드 설정*: 쿠버네티스 API 서버([kube-apiserver](/docs/reference/command-line-tools-reference/kube-apiserver/))를 실행할 때, 
*`--authorization-mode`* 플래그를 사용하여 인증 모드를 설정해야 한다.
예를 들어, (*`/etc/kubernetes/manifests`*에 있는) 
*`kube-adminserver.yaml`* 파일 안의 플래그를 `Node,RBAC`으로 설정할 수 있다. 
이렇게 하여 인증된 요청이 Node 인가와 RBAC 인가를 사용할 수 있게 된다.
- *사용자 인증서와 롤 바인딩 생성(RBAC을 사용하는 경우)*: RBAC 인증을 사용하는 경우, 
사용자는 클러스터 CA가 서명한 CSR(CertificateSigningRequest)을 만들 수 있다. 
그 뒤에 각 사용자에게 역할 및 ClusterRoles를 바인딩할 수 있다.
자세한 내용은 
[인증서 서명 요청](/docs/reference/access-authn-authz/certificate-signing-requests/)을 참조한다.
- *속성을 포함하는 정책 생성(ABAC을 사용하는 경우)*: ABAC 인증을 사용하는 경우, 
속성의 집합으로 정책을 생성하여, 인증된 사용자 또는 그룹이 
특정 리소스(예: 파드), 네임스페이스, 또는 apiGroup에 접근할 수 있도록 한다. 
[예시](/docs/reference/access-authn-authz/abac/#examples)에서 
더 많은 정보를 확인한다.
- *어드미션 컨트롤러 도입 고려*: 
[웹훅 토큰 인증](/docs/reference/access-authn-authz/authentication/#webhook-token-authentication)은 
API 서버를 통해 들어오는 요청의 인가에 사용할 수 있는 추가적인 방법이다. 
웹훅 및 다른 인가 형식을 사용하려면 API 서버에 
[어드미션 컨트롤러](/docs/reference/access-authn-authz/admission-controllers/)를 
추가해야 한다.

## 워크로드에 자원 제한 걸기

프로덕션 워크로드의 요구 사항이 
쿠버네티스 컨트롤 플레인 안팎의 압박을 초래할 수 있다. 
워크로드의 요구 사항을 충족하도록 클러스터를 구성할 때 다음 항목을 고려한다.

- *네임스페이스 제한 설정*: 메모리, CPU와 같은 자원의 네임스페이스 별 쿼터를 설정한다. 
[메모리, CPU 와 API 리소스 관리](/ko/docs/tasks/administer-cluster/manage-resources/)에서 
상세 사항을 확인한다. 
[계층적 네임스페이스](/blog/2020/08/14/introducing-hierarchical-namespaces/)를 설정하여 
제한을 상속할 수도 있다.
- *DNS 요청에 대한 대비*: 워크로드가 대규모로 확장될 것으로 예상된다면, 
DNS 서비스도 확장할 준비가 되어 있어야 한다. 
[클러스터의 DNS 서비스 오토스케일링](/docs/tasks/administer-cluster/dns-horizontal-autoscaling/)을 확인한다.
- *추가적인 서비스 어카운트 생성*: 사용자 계정은 *클러스터*에서 사용자가 무엇을 할 수 있는지 결정하는 반면에, 
서비스 어카운트는 특정 네임스페이스 내의 파드 접근 권한을 결정한다. 
기본적으로, 파드는 자신의 네임스페이스의 기본 서비스 어카운트을 이용한다.
[서비스 어카운트 관리하기](/ko/docs/reference/access-authn-authz/service-accounts-admin/)에서 
새로운 서비스 어카운트을 생성하는 방법을 확인한다. 예를 들어, 다음의 작업을 할 수 있다.
  - 파드가 특정 컨테이너 레지스트리에서 이미지를 가져 오는 데 사용할 수 있는 시크릿을 추가한다. [파드를 위한 서비스 어카운트 구성하기](/docs/tasks/configure-pod-container/configure-service-account/)에서 예시를 확인한다.
  - 서비스 어카운트에 RBAC 권한을 할당한다. [서비스어카운트 권한](/docs/reference/access-authn-authz/rbac/#service-account-permissions)에서 상세 사항을 확인한다.

## {{% heading "whatsnext" %}}

- 프로덕션 쿠버네티스를 직접 구축할지, 
아니면 [턴키 클라우드 솔루션](/ko/docs/setup/production-environment/turnkey-solutions/) 또는 
[쿠버네티스 파트너](/ko/partners/)가 제공하는 서비스를 이용할지 결정한다.
- 클러스터를 직접 구축한다면, 
[인증서](/ko/docs/setup/best-practices/certificates/)를 어떻게 관리할지, 
[etcd](/docs/setup/production-environment/tools/kubeadm/setup-ha-etcd-with-kubeadm/)와 
[API 서버](/ko/docs/setup/production-environment/tools/kubeadm/ha-topology/) 
등의 기능에 대한 고가용성을 
어떻게 보장할지를 계획한다.
- 배포 도구로 [kubeadm](/ko/docs/setup/production-environment/tools/kubeadm/), [kops](/ko/docs/setup/production-environment/tools/kops/), [Kubespray](/ko/docs/setup/production-environment/tools/kubespray/) 중 
하나를 선택한다.
- [인증](/docs/reference/access-authn-authz/authentication/) 및 
[인가](/ko/docs/reference/access-authn-authz/authorization/) 방식을 선택하여 
사용자 관리 방법을 구성한다.
- [자원 제한](/ko/docs/tasks/administer-cluster/manage-resources/), 
[DNS 오토스케일링](/docs/tasks/administer-cluster/dns-horizontal-autoscaling/), 
[서비스 어카운트](/ko/docs/reference/access-authn-authz/service-accounts-admin/)를 설정하여 
애플리케이션 워크로드의 실행에 대비한다.
