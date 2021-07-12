---
title: 클러스터 관리



weight: 100
content_type: concept
description: >
  쿠버네티스 클러스터 생성 또는 관리에 관련된 로우-레벨(lower-level)의 세부 정보를 설명한다.
no_list: true
---

<!-- overview -->
클러스터 관리 개요는 쿠버네티스 클러스터를 생성하거나 관리하는 모든 사람들을 위한 것이다.
핵심 쿠버네티스 [개념](/ko/docs/concepts/)에 어느 정도 익숙하다고 가정한다.


<!-- body -->
## 클러스터 계획

쿠버네티스 클러스터를 계획, 설정 및 구성하는 방법에 대한 예는 [시작하기](/ko/docs/setup/)에 있는 가이드를 참고한다. 이 문서에 나열된 솔루션을 *배포판* 이라고 한다.

   {{< note  >}}
   모든 배포판이 활발하게 유지되는 것은 아니다. 최신 버전의 쿠버네티스에서 테스트된 배포판을 선택한다.
   {{< /note >}}

가이드를 선택하기 전에 고려해야 할 사항은 다음과 같다.

 - 컴퓨터에서 쿠버네티스를 한번 사용해보고 싶은가? 아니면, 고가용 멀티 노드 클러스터를 만들고 싶은가? 사용자의 필요에 따라 가장 적합한 배포판을 선택한다.
 - [구글 쿠버네티스 엔진(Google Kubernetes Engine)](https://cloud.google.com/kubernetes-engine/)과 같은 클라우드 제공자의 **쿠버네티스 클러스터 호스팅** 을 사용할 것인가? 아니면, **자체 클러스터를 호스팅** 할 것인가?
 - 클러스터가 **온-프레미스 환경** 에 있나? 아니면, **클라우드(IaaS)** 에 있나? 쿠버네티스는 하이브리드 클러스터를 직접 지원하지는 않는다. 대신 여러 클러스터를 설정할 수 있다.
 - **온-프레미스 환경에 쿠버네티스** 를 구성하는 경우, 어떤 [네트워킹 모델](/ko/docs/concepts/cluster-administration/networking/)이 가장 적합한 지 고려한다.
 - 쿠버네티스를 **"베어 메탈" 하드웨어** 에서 실행할 것인가? 아니면, **가상 머신(VM)** 에서 실행할 것인가?
 - **클러스터만 실행할 것인가?** 아니면, **쿠버네티스 프로젝트 코드를 적극적으로 개발** 하는 것을 기대하는가? 만약
   후자라면, 활발하게 개발이 진행되고 있는 배포판을 선택한다. 일부 배포판은 바이너리 릴리스만 사용하지만,
   더 다양한 선택을 제공한다.
 - 클러스터를 실행하는 데 필요한 [컴포넌트](/ko/docs/concepts/overview/components/)에 익숙해지자.


## 클러스터 관리

* [노드 관리](/ko/docs/concepts/architecture/nodes/) 방법을 배운다.

* 공유 클러스터에 대한 [리소스 쿼터](/ko/docs/concepts/policy/resource-quotas/)를 설정하고 관리하는 방법을 배운다.

## 클러스터 보안

* [인증서 생성](/ko/docs/tasks/administer-cluster/certificates/)은 다른 툴 체인을 사용하여 인증서를 생성하는 단계를 설명한다.

* [쿠버네티스 컨테이너 환경](/ko/docs/concepts/containers/container-environment/)은 쿠버네티스 노드에서 Kubelet으로 관리하는 컨테이너에 대한 환경을 설명한다.

* [쿠버네티스 API에 대한 접근 제어](/ko/docs/concepts/security/controlling-access)는 쿠버네티스가 자체 API에 대한 접근 제어를 구현하는 방법을 설명한다.

* [인증](/docs/reference/access-authn-authz/authentication/)은 다양한 인증 옵션을 포함한 쿠버네티스에서의 인증에 대해 설명한다.

* [인가](/ko/docs/reference/access-authn-authz/authorization/)는 인증과는 별개로, HTTP 호출 처리 방법을 제어한다.

* [어드미션 컨트롤러 사용하기](/docs/reference/access-authn-authz/admission-controllers/)는 인증과 권한 부여 후 쿠버네티스 API 서버에 대한 요청을 가로채는 플러그인에 대해 설명한다.

* [쿠버네티스 클러스터에서 Sysctls 사용하기](/docs/tasks/administer-cluster/sysctl-cluster/)는 관리자가 `sysctl` 커맨드라인 도구를 사용하여 커널 파라미터를 설정하는 방법에 대해 설명한다.

* [감사(audit)](/docs/tasks/debug-application-cluster/audit/)는 쿠버네티스의 감사 로그를 다루는 방법에 대해 설명한다.

### kubelet 보안
  * [컨트롤 플레인-노드 통신](/ko/docs/concepts/architecture/control-plane-node-communication/)
  * [TLS 부트스트래핑(bootstrapping)](/docs/reference/command-line-tools-reference/kubelet-tls-bootstrapping/)
  * [Kubelet 인증/인가](/ko/docs/reference/command-line-tools-reference/kubelet-authentication-authorization/)

## 선택적 클러스터 서비스

* [DNS 통합](/ko/docs/concepts/services-networking/dns-pod-service/)은 DNS 이름을 쿠버네티스 서비스로 직접 확인하는 방법을 설명한다.

* [클러스터 액티비티 로깅과 모니터링](/ko/docs/concepts/cluster-administration/logging/)은 쿠버네티스에서의 로깅이 어떻게 작동하는지와 구현 방법에 대해 설명한다.
