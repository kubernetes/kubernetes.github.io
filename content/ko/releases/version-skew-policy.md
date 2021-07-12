---







title: 버전 차이(skew) 정책
type: docs
description: >
  다양한 쿠버네티스 구성 요소 간에 지원되는 최대 버전 차이
---

<!-- overview -->
이 문서는 다양한 쿠버네티스 구성 요소 간에 지원되는 최대 버전 차이를 설명한다.
특정 클러스터 배포 도구는 버전 차이에 대한 추가적인 제한을 설정할 수 있다.

<!-- body -->

## 지원되는 버전

쿠버네티스 버전은 **x.y.z** 로 표현되는데, 여기서 **x** 는 메이저 버전, **y** 는 마이너 버전, **z** 는 패치 버전을 의미하며, 이는 [시맨틱 버전](https://semver.org/) 용어에 따른 것이다.
자세한 내용은 [쿠버네티스 릴리스 버전](https://github.com/kubernetes/community/blob/master/contributors/design-proposals/release/versioning.md#kubernetes-release-versioning)을 참조한다.

쿠버네티스 프로젝트는 최근 세 개의 마이너 릴리스 ({{< skew latestVersion >}}, {{< skew prevMinorVersion >}}, {{< skew oldestMinorVersion >}}) 에 대한 릴리스 분기를 유지한다. 쿠버네티스 1.19 이상은 약 1년간의 패치 지원을 받는다. 쿠버네티스 1.18 이상은 약 9개월의 패치 지원을 받는다.

보안 수정사항을 포함한 해당 수정사항은 심각도와 타당성에 따라 세 개의 릴리스 브랜치로 백포트(backport) 될 수 있다.
패치 릴리스는 각 브랜치별로 [정기적인 주기](https://git.k8s.io/sig-release/releases/patch-releases.md#cadence)로 제공하며, 필요한 경우 추가 긴급 릴리스도 추가한다.

[릴리스 관리자](https://git.k8s.io/sig-release/release-managers.md) 그룹이 이러한 결정 권한을 가진다.

자세한 내용은 쿠버네티스 [패치 릴리스](https://git.k8s.io/sig-release/releases/patch-releases.md) 페이지를 참조한다.

## 지원되는 버전 차이

### kube-apiserver

[고가용성(HA) 클러스터](/docs/setup/production-environment/tools/kubeadm/high-availability/)에서 최신 및 가장 오래된 `kube-apiserver` 인스턴스가 각각 한 단계 마이너 버전 내에 있어야 한다.

예:

* 최신 `kube-apiserver`는 **{{< skew latestVersion >}}** 이다.
* 다른 `kube-apiserver` 인스턴스는 **{{< skew latestVersion >}}** 및 **{{< skew prevMinorVersion >}}** 을 지원한다.

### kubelet

`kubelet`은 `kube-apiserver`보다 최신일 수 없으며, 2단계의 낮은 마이너 버전까지 지원한다.

예:

* `kube-apiserver`가 **{{< skew latestVersion >}}** 이다.
* `kubelet`은 **{{< skew latestVersion >}}**, **{{< skew prevMinorVersion >}}** 및 **{{< skew oldestMinorVersion >}}** 을 지원한다.

{{< note >}}
HA 클러스터의 `kube-apiserver` 인스턴스 사이에 버전 차이가 있으면 허용되는 `kubelet` 버전의 범위도 줄어든다.
{{</ note >}}

예:

* `kube-apiserver` 인스턴스는 **{{< skew latestVersion >}}** 및 **{{< skew prevMinorVersion >}}** 이다.
* `kubelet`은 **{{< skew prevMinorVersion >}}** 및 **{{< skew oldestMinorVersion >}}** 을 지원한다(**{{< skew latestVersion >}}** 는  `kube-apiserver`의 **{{< skew prevMinorVersion >}}** 인스턴스보다 최신 버전이기 때문에 지원하지 않는다).

### kube-controller-manager, kube-scheduler 그리고 cloud-controller-manager

`kube-controller-manager`, `kube-scheduler` 그리고 `cloud-controller-manager`는 그들과 통신하는 `kube-apiserver` 인스턴스보다 최신 버전이면 안 된다. `kube-apiserver` 마이너 버전과 일치할 것으로 예상하지만, 최대 한 단계 낮은 마이너 버전까지는 허용한다(실시간 업그레이드를 지원하기 위해서).

예:

* `kube-apiserver`은 **{{< skew latestVersion >}}** 이다.
* `kube-controller-manager`, `kube-scheduler` 그리고 `cloud-controller-manager`는 **{{< skew latestVersion >}}** 과 **{{< skew prevMinorVersion >}}** 을 지원한다.

{{< note >}}
HA 클러스터의 `kube-apiserver` 인스턴스 간에 버전 차이가 존재하고 이러한 구성 요소가 클러스터의 모든 `kube-apiserver` 인스턴스와 통신할 수 있는 경우(예를 들어, 로드 밸런서를 통해서)에는 구성 요소의 허용하는 버전의 범위도 줄어든다.
{{< /note >}}

예:

* `kube-apiserver` 인스턴스는 **{{< skew latestVersion >}}** 및 **{{< skew prevMinorVersion >}}** 이다.
* `kube-controller-manager`, `kube-scheduler` 그리고 `cloud-controller-manager`는 모든 `kube-apiserver` 인스턴스로 라우팅하는 로드 밸런서와 통신한다.
* `kube-controller-manager`, `kube-scheduler` 그리고 `cloud-controller-manager`는 **{{< skew prevMinorVersion >}}** 에서 지원한다(**{{< skew latestVersion >}}** 는 `kube-apiserver` 인스턴스의 **{{< skew prevMinorVersion >}}** 버전보다 최신이기 때문에 지원하지 않는다).

### kubectl

`kubectl`은 `kube-apiserver`의 한 단계 마이너 버전(이전 또는 최신) 내에서 지원한다.

예:

* `kube-apiserver`은 **{{< skew latestVersion >}}** 이다.
* `kubectl`은 **{{< skew nextMinorVersion >}}**, **{{< skew latestVersion >}}** 및 **{{< skew prevMinorVersion >}}** 을 지원한다.

{{< note >}}
HA 클러스터의 `kube-apiserver` 인스턴스 간에 버전 차이가 있으면 지원되는 `kubectl` 버전의 범위도 줄어든다.
{{< /note >}}

예:

* `kube-apiserver` 인스턴스는 **{{< skew latestVersion >}}** 및 **{{< skew prevMinorVersion >}}** 이다.
* `kubectl`은 **{{< skew latestVersion >}}** 및 **{{< skew prevMinorVersion >}}** 에서 지원한다(다른 버전은 `kube-apiserver` 인스턴스 중에 한 단계 이상의 마이너 버전 차이가 난다).

## 지원되는 구성 요소 업그레이드 순서

구성요소 간 지원되는 버전 차이는 구성요소를 업그레이드하는 순서에 영향을 준다.
이 섹션에서는 기존 클러스터를 버전 **{{< skew prevMinorVersion >}}** 에서 버전 **{{< skew latestVersion >}}** 로 전환하기 위해 구성 요소를 업그레이드하는 순서를 설명한다.

### kube-apiserver

사전 요구 사항:

* 단일 인스턴스 클러스터에서 기존 `kube-apiserver` 인스턴스는 **{{< skew prevMinorVersion >}}** 이어야 한다.
* HA 클러스터에서 모든 `kube-apiserver` 인스턴스는 **{{< skew prevMinorVersion >}}** 또는 **{{< skew latestVersion >}}** 이어야 한다(이것은 `kube-apiserver` 인스턴스 간의 가장 최신과 오래된 버전의 차이를 최대 1개의 마이너 버전의 차이로 보장한다).
* 이 서버와 통신하는 `kube-controller-manager`, `kube-scheduler` 그리고 `cloud-controller-manager`의 버전은 **{{< skew prevMinorVersion >}}** 이어야 한다(이것은 기존 API서버 버전보다 최신 버전이 아니고 새로운 API서버 버전의 마이너 1개의 버전 내에 있음을 보장한다).
* 모든 `kubelet` 인스턴스는 버전  **{{< skew prevMinorVersion >}}** 또는 **{{< skew oldestMinorVersion >}}** 이어야 한다(이것은 기존 API서버 버전보다 최신 버전이 아니며, 새로운 API서버 버전의 2개의 마이너 버전 내에 있음을 보장한다).
* 등록된 어드미션 웹훅은 새로운 `kube-apiserver` 인스턴스가 전송하는 데이터를 처리할 수 있다:
  * `ValidatingWebhookConfiguration` 그리고 `MutatingWebhookConfiguration` 오브젝트는 **{{< skew latestVersion >}}** 에 추가된 REST 리소스의 새 버전을 포함하도록 업데이트한다(또는 v1.15 이상에서 사용 가능한 [`matchPolicy: Equivalent` option](/docs/reference/access-authn-authz/extensible-admission-controllers/#matching-requests-matchpolicy) 설정을 사용).
  * 웹훅은 자신에게 전송될 REST리소스의 새버전과 **{{< skew latestVersion >}}** 에서 기존 버전에 추가된 새로운 필드를 처리할 수 있다.

`kube-apiserver`를 **{{< skew latestVersion >}}** 으로 업그레이드

{{< note >}}
[API 지원 중단](/docs/reference/using-api/deprecation-policy/) 및
[API 변경 가이드라인](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api_changes.md)
에 대한 프로젝트 정책에서는 단일 클러스터일지라도 업그레이드할 때 `kube-apiserver`의 마이너 버전을 건너뛰지 않도록 요구한다.
{{< /note >}}

### kube-controller-manager, kube-scheduler 그리고 cloud-controller-manager

사전 요구 사항:

* `kube-apiserver` 인스턴스는 **{{< skew latestVersion >}}** 이여야 한다(HA 클러스터에서 `kube-apiserver` 인스턴스와 통신할 수 있는 구성 요소를 업그레이드 전에 모든 `kube-apiserver` 인스턴스는 업그레이드되어야 한다).

`kube-controller-manager`, `kube-scheduler` 및 `cloud-controller-manager` 를 **{{< skew latestVersion >}}** 으로 업그레이드한다.

### kubelet

사전 요구 사항:

*  `kubelet`과 통신하는 `kube-apiserver` 인스턴스는 **{{< skew latestVersion >}}** 이어야 한다.

필요에 따라서 `kubelet` 인스턴스를 **{{< skew latestVersion >}}** 으로 업그레이드할 수 있다(또는 **{{< skew prevMinorVersion >}}** 아니면 **{{< skew oldestMinorVersion >}}** 으로 유지할 수 있음).

{{< note >}}
`kubelet` 마이너 버전 업그레이드를 수행하기 전에, 해당 노드의 파드를 [드레인(drain)](/docs/tasks/administer-cluster/safely-drain-node/)해야 한다.
인플레이스(In-place) 마이너 버전 `kubelet` 업그레이드는 지원되지 않는다.
{{</ note >}}

{{< warning >}}
클러스터 안의 `kubelet` 인스턴스를 `kube-apiserver`의 버전보다 2단계 낮은 버전으로 실행하는 것을 권장하지 않는다:

* `kube-apiserver`를 업그레이드한다면 한 단계 낮은 버전으로 업그레이드해야 한다.
* 이것은 관리되고 있는 3단계의 마이너 버전보다 낮은 `kubelet`을 실행할 가능성을 높인다.
{{</ warning >}}

### kube-proxy

* `kube-proxy`는 반드시 `kubelet`과 동일한 마이너 버전이어야 한다.
* `kube-proxy`는 반드시 `kube-apiserver` 보다 최신 버전이면 안 된다.
* `kube-proxy`는 `kube-apiserver` 보다 2단계 낮은 마이너 버전 이내여야 한다.

예:

`kube-proxy` 버전이 **{{< skew oldestMinorVersion >}}** 인 경우:

* `kubelet` 버전도 반드시 **{{< skew oldestMinorVersion >}}** 와 동일한 마이너 버전이어야 한다.
* `kube-apiserver` 버전은 반드시 **{{< skew oldestMinorVersion >}}** 에서 **{{< skew latestVersion >}}** 사이 이어야 한다.
