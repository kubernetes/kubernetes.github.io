---
title: 쿠버네티스 확장
weight: 110
description: 쿠버네티스 클러스터의 동작을 변경하는 다양한 방법
feature:
  title: 확장성을 고려하여 설계됨
  description: >
    쿠버네티스 업스트림 소스 코드 수정 없이 쿠버네티스 클러스터에 기능을 추가할 수 있다.
content_type: concept
no_list: true
---

<!-- overview -->

쿠버네티스는 매우 유연하게 구성할 수 있고 확장 가능하다. 결과적으로
쿠버네티스 프로젝트를 포크하거나 코드에 패치를 제출할 필요가
거의 없다.

이 가이드는 쿠버네티스 클러스터를 사용자 정의하기 위한 옵션을 설명한다.
쿠버네티스 클러스터를 업무 환경의 요구에 맞게
조정하는 방법을 이해하려는 {{< glossary_tooltip text="클러스터 운영자" term_id="cluster-operator" >}}를 대상으로 한다.
잠재적인 {{< glossary_tooltip text="플랫폼 개발자" term_id="platform-developer" >}} 또는 쿠버네티스 프로젝트 {{< glossary_tooltip text="컨트리뷰터" term_id="contributor" >}}인 개발자에게도
어떤 익스텐션(extension) 포인트와 패턴이 있는지,
그리고 그것의 트레이드오프와 제약을 이해하는 데 도움이 될 것이다.

<!-- body -->

## 개요

사용자 정의 방식은 크게 플래그, 로컬 구성 파일 또는 API 리소스 변경만 포함하는 *구성* 과 추가 프로그램이나 서비스 실행과 관련된 *익스텐션* 으로 나눌 수 있다. 이 문서는 주로 익스텐션에 관한 것이다.

## 구성

*구성 파일* 및 *플래그* 는 온라인 문서의 레퍼런스 섹션에 각 바이너리 별로 문서화되어 있다.

* [kubelet](/docs/reference/command-line-tools-reference/kubelet/)
* [kube-apiserver](/docs/reference/command-line-tools-reference/kube-apiserver/)
* [kube-controller-manager](/docs/reference/command-line-tools-reference/kube-controller-manager/)
* [kube-scheduler](/docs/reference/command-line-tools-reference/kube-scheduler/).

호스팅된 쿠버네티스 서비스 또는 매니지드 설치 환경의 배포판에서 플래그 및 구성 파일을 항상 변경할 수 있는 것은 아니다. 변경 가능한 경우 일반적으로 클러스터 관리자만 변경할 수 있다. 또한 향후 쿠버네티스 버전에서 변경될 수 있으며, 이를 설정하려면 프로세스를 다시 시작해야 할 수도 있다. 이러한 이유로 다른 옵션이 없는 경우에만 사용해야 한다.

[리소스쿼터](/ko/docs/concepts/policy/resource-quotas/), [파드시큐리티폴리시(PodSecurityPolicy)](/ko/docs/concepts/policy/pod-security-policy/), [네트워크폴리시](/ko/docs/concepts/services-networking/network-policies/) 및 역할 기반 접근 제어([RBAC](/docs/reference/access-authn-authz/rbac/))와 같은 *빌트인 정책 API(built-in Policy API)* 는 기본적으로 제공되는 쿠버네티스 API이다. API는 일반적으로 호스팅된 쿠버네티스 서비스 및 매니지드 쿠버네티스 설치 환경과 함께 사용된다. 그것들은 선언적이며 파드와 같은 다른 쿠버네티스 리소스와 동일한 규칙을 사용하므로, 새로운 클러스터 구성을 반복할 수 있고 애플리케이션과 동일한 방식으로 관리할 수 있다. 또한, 이들 API가 안정적인 경우, 다른 쿠버네티스 API와 같이 [정의된 지원 정책](/docs/reference/using-api/deprecation-policy/)을 사용할 수 있다. 이러한 이유로 인해 *구성 파일* 과 *플래그* 보다 선호된다.

## 익스텐션

익스텐션은 쿠버네티스를 확장하고 쿠버네티스와 긴밀하게 통합되는 소프트웨어 컴포넌트이다.
이들 컴포넌트는 쿠버네티스가 새로운 유형과 새로운 종류의 하드웨어를 지원할 수 있게 해준다.

대부분의 클러스터 관리자는 쿠버네티스의 호스팅 또는 배포판 인스턴스를 사용한다.
결과적으로 대부분의 쿠버네티스 사용자는 익스텐션 기능을 설치할 필요가 없고
새로운 익스텐션 기능을 작성할 필요가 있는 사람은 더 적다.

## 익스텐션 패턴

쿠버네티스는 클라이언트 프로그램을 작성하여 자동화 되도록 설계되었다.
쿠버네티스 API를 읽고 쓰는 프로그램은 유용한 자동화를 제공할 수 있다.
*자동화* 는 클러스터 상에서 또는 클러스터 밖에서 실행할 수 있다. 이 문서의 지침에 따라
고가용성과 강력한 자동화를 작성할 수 있다.
자동화는 일반적으로 호스트 클러스터 및 매니지드 설치 환경을 포함한 모든
쿠버네티스 클러스터에서 작동한다.

쿠버네티스와 잘 작동하는 클라이언트 프로그램을 작성하기 위한 특정 패턴은 *컨트롤러* 패턴이라고 한다.
컨트롤러는 일반적으로 오브젝트의 `.spec`을 읽고, 가능한 경우 수행한 다음
오브젝트의 `.status`를 업데이트 한다.

컨트롤러는 쿠버네티스의 클라이언트이다. 쿠버네티스가 클라이언트이고
원격 서비스를 호출할 때 이를 *웹훅(Webhook)* 이라고 한다. 원격 서비스를
*웹훅 백엔드* 라고 한다. 컨트롤러와 마찬가지로 웹훅은 장애 지점을
추가한다.

웹훅 모델에서 쿠버네티스는 원격 서비스에 네트워크 요청을 한다.
*바이너리 플러그인* 모델에서 쿠버네티스는 바이너리(프로그램)를 실행한다.
바이너리 플러그인은 kubelet(예:
[Flex Volume 플러그인](/ko/docs/concepts/storage/volumes/#flexVolume)과
[네트워크 플러그인](/ko/docs/concepts/extend-kubernetes/compute-storage-net/network-plugins/))과
kubectl에서
사용한다.

아래는 익스텐션 포인트가 쿠버네티스 컨트롤 플레인과 상호 작용하는 방법을
보여주는 다이어그램이다.

<!-- image source drawing https://docs.google.com/drawings/d/1muJ7Oxuj_7Gtv7HV9-2zJbOnkQJnjxq-v1ym_kZfB-4/edit?ts=5a01e054 -->

![익스텐션 포인트와 컨트롤 플레인](/ko/docs/concepts/extend-kubernetes/control-plane.png)

## 익스텐션 포인트

이 다이어그램은 쿠버네티스 시스템의 익스텐션 포인트를 보여준다.

<!-- image source diagrams: https://docs.google.com/drawings/d/1k2YdJgNTtNfW7_A8moIIkij-DmVgEhNrn3y2OODwqQQ/view -->

![익스텐션 포인트](/docs/concepts/extend-kubernetes/extension-points.png)

1.   사용자는 종종 `kubectl`을 사용하여 쿠버네티스 API와 상호 작용한다. [Kubectl 플러그인](/ko/docs/tasks/extend-kubectl/kubectl-plugins/)은 kubectl 바이너리를 확장한다. 개별 사용자의 로컬 환경에만 영향을 미치므로 사이트 전체 정책을 적용할 수는 없다.
2.   apiserver는 모든 요청을 처리한다. apiserver의 여러 유형의 익스텐션 포인트는 요청을 인증하거나, 콘텐츠를 기반으로 요청을 차단하거나, 콘텐츠를 편집하고, 삭제 처리를 허용한다. 이 내용은 [API 접근 익스텐션](#api-접근-익스텐션) 섹션에 설명되어 있다.
3.   apiserver는 다양한 종류의 *리소스* 를 제공한다. `pods`와 같은 *빌트인 리소스 종류* 는 쿠버네티스 프로젝트에 의해 정의되며 변경할 수 없다. 직접 정의한 리소스를 추가할 수도 있고, [커스텀 리소스](#사용자-정의-유형) 섹션에 설명된 대로 *커스텀 리소스* 라고 부르는 다른 프로젝트에서 정의한 리소스를 추가할 수도 있다. 커스텀 리소스는 종종 API 접근 익스텐션과 함께 사용된다.
4.   쿠버네티스 스케줄러는 파드를 배치할 노드를 결정한다. 스케줄링을 확장하는 몇 가지 방법이 있다. 이들은 [스케줄러 익스텐션](#스케줄러-익스텐션) 섹션에 설명되어 있다.
5.   쿠버네티스의 많은 동작은 API-Server의 클라이언트인 컨트롤러(Controller)라는 프로그램으로 구현된다. 컨트롤러는 종종 커스텀 리소스와 함께 사용된다.
6.   kubelet은 서버에서 실행되며 파드가 클러스터 네트워크에서 자체 IP를 가진 가상 서버처럼 보이도록 한다. [네트워크 플러그인](#네트워크-플러그인)을 사용하면 다양한 파드 네트워킹 구현이 가능하다.
7.   kubelet은 컨테이너의 볼륨을 마운트 및 마운트 해제한다. 새로운 유형의 스토리지는 [스토리지 플러그인](#스토리지-플러그인)을 통해 지원될 수 있다.

어디서부터 시작해야 할지 모르겠다면, 이 플로우 차트가 도움이 될 수 있다. 일부 솔루션에는 여러 유형의 익스텐션이 포함될 수 있다.

<!-- image source drawing: https://docs.google.com/drawings/d/1sdviU6lDz4BpnzJNHfNpQrqI9F19QZ07KnhnxVrp2yg/edit -->

![익스텐션 플로우차트](/ko/docs/concepts/extend-kubernetes/flowchart.png)

## API 익스텐션
### 사용자 정의 유형

새 컨트롤러, 애플리케이션 구성 오브젝트 또는 기타 선언적 API를 정의하고 `kubectl` 과 같은 쿠버네티스 도구를 사용하여 관리하려면 쿠버네티스에 커스텀 리소스를 추가하자.

애플리케이션, 사용자 또는 모니터링 데이터의 데이터 저장소로 커스텀 리소스를 사용하지 않는다.

커스텀 리소스에 대한 자세한 내용은 [커스텀 리소스 개념 가이드](/ko/docs/concepts/extend-kubernetes/api-extension/custom-resources/)를 참고하길 바란다.


### 새로운 API와 자동화의 결합

사용자 정의 리소스 API와 컨트롤 루프의 조합을 [오퍼레이터(operator) 패턴](/ko/docs/concepts/extend-kubernetes/operator/)이라고 한다. 오퍼레이터 패턴은 특정 애플리케이션, 일반적으로 스테이트풀(stateful) 애플리케이션을 관리하는 데 사용된다. 이러한 사용자 정의 API 및 컨트롤 루프를 사용하여 스토리지나 정책과 같은 다른 리소스를 제어할 수도 있다.

### 빌트인 리소스 변경

사용자 정의 리소스를 추가하여 쿠버네티스 API를 확장하면 추가된 리소스는 항상 새로운 API 그룹에 속한다. 기존 API 그룹을 바꾸거나 변경할 수 없다.
API를 추가해도 기존 API(예: 파드)의 동작에 직접 영향을 미치지는 않지만 API 접근 익스텐션은 영향을 준다.


### API 접근 익스텐션

요청이 쿠버네티스 API 서버에 도달하면 먼저 인증이 되고, 그런 다음 승인된 후 다양한 유형의 어드미션 컨트롤이 적용된다. 이 흐름에 대한 자세한 내용은 [쿠버네티스 API에 대한 접근 제어](/ko/docs/concepts/security/controlling-access/)를 참고하길 바란다.

이러한 각 단계는 익스텐션 포인트를 제공한다.

쿠버네티스에는 이를 지원하는 몇 가지 빌트인 인증 방법이 있다. 또한 인증 프록시 뒤에 있을 수 있으며 인증 헤더에서 원격 서비스로 토큰을 전송하여 확인할 수 있다(웹훅). 이러한 방법은 모두 [인증 설명서](/docs/reference/access-authn-authz/authentication/)에 설명되어 있다.

### 인증

[인증](/docs/reference/access-authn-authz/authentication/)은 모든 요청의 헤더 또는 인증서를 요청하는 클라이언트의 사용자 이름에 매핑한다.

쿠버네티스는 몇 가지 빌트인 인증 방법과 필요에 맞지 않는 경우 [인증 웹훅](/docs/reference/access-authn-authz/authentication/#webhook-token-authentication) 방법을 제공한다.


### 인가

[인가](/docs/reference/access-authn-authz/webhook/)는 특정 사용자가 API 리소스에서 읽고, 쓰고, 다른 작업을 수행할 수 있는지를 결정한다. 전체 리소스 레벨에서 작동하며 임의의 오브젝트 필드를 기준으로 구별하지 않는다. 빌트인 인증 옵션이 사용자의 요구를 충족시키지 못하면 [인가 웹훅](/docs/reference/access-authn-authz/webhook/)을 통해 사용자가 제공한 코드를 호출하여 인증 결정을 내릴 수 있다.


### 동적 어드미션 컨트롤

요청이 승인된 후, 쓰기 작업인 경우 [어드미션 컨트롤](/docs/reference/access-authn-authz/admission-controllers/) 단계도 수행된다. 빌트인 단계 외에도 몇 가지 익스텐션이 있다.

*   [이미지 정책 웹훅](/docs/reference/access-authn-authz/admission-controllers/#imagepolicywebhook)은 컨테이너에서 실행할 수 있는 이미지를 제한한다.
*   임의의 어드미션 컨트롤 결정을 내리기 위해 일반적인 [어드미션 웹훅](/docs/reference/access-authn-authz/extensible-admission-controllers/#admission-webhooks)을 사용할 수 있다. 어드미션 웹훅은 생성 또는 업데이트를 거부할 수 있다.

## 인프라스트럭처 익스텐션


### 스토리지 플러그인

[Flex Volumes](https://github.com/kubernetes/community/blob/master/contributors/design-proposals/storage/flexvolume-deployment.md)을 사용하면
Kubelet이 바이너리 플러그인을 호출하여 볼륨을 마운트하도록 함으로써
빌트인 지원 없이 볼륨 유형을 마운트 할 수 있다.


### 장치 플러그인

장치 플러그인은 노드가 [장치 플러그인](/ko/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/)을
통해 새로운 노드 리소스(CPU 및 메모리와 같은 빌트인 자원 외에)를
발견할 수 있게 해준다.


### 네트워크 플러그인

노드-레벨의 [네트워크 플러그인](/ko/docs/concepts/extend-kubernetes/compute-storage-net/network-plugins/)을 통해 다양한 네트워킹 패브릭을 지원할 수 있다.

### 스케줄러 익스텐션

스케줄러는 파드를 감시하고 파드를 노드에 할당하는 특수한 유형의
컨트롤러이다. 다른 쿠버네티스 컴포넌트를 계속 사용하면서
기본 스케줄러를 완전히 교체하거나,
[여러 스케줄러](/docs/tasks/extend-kubernetes/configure-multiple-schedulers/)를
동시에 실행할 수 있다.

이것은 중요한 부분이며, 거의 모든 쿠버네티스 사용자는 스케줄러를 수정할
필요가 없다는 것을 알게 된다.

스케줄러는 또한 웹훅 백엔드(스케줄러 익스텐션)가
파드에 대해 선택된 노드를 필터링하고 우선 순위를 지정할 수 있도록 하는
[웹훅](https://github.com/kubernetes/community/blob/master/contributors/design-proposals/scheduling/scheduler_extender.md)을
지원한다.

## {{% heading "whatsnext" %}}


* [커스텀 리소스](/ko/docs/concepts/extend-kubernetes/api-extension/custom-resources/)에 대해 더 알아보기
* [동적 어드미션 컨트롤](/docs/reference/access-authn-authz/extensible-admission-controllers/)에 대해 알아보기
* 인프라스트럭처 익스텐션에 대해 더 알아보기
  * [네트워크 플러그인](/ko/docs/concepts/extend-kubernetes/compute-storage-net/network-plugins/)
  * [장치 플러그인](/ko/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/)
* [kubectl 플러그인](/ko/docs/tasks/extend-kubectl/kubectl-plugins/)에 대해 알아보기
* [오퍼레이터 패턴](/ko/docs/concepts/extend-kubernetes/operator/)에 대해 알아보기
