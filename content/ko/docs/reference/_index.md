---
title: 레퍼런스


linkTitle: "레퍼런스"
main_menu: true
weight: 70
content_type: concept
no_list: true
---

<!-- overview -->

쿠버네티스 문서의 본 섹션에서는 레퍼런스를 다룬다.



<!-- body -->

## API 레퍼런스

* [표준 용어집](/ko/docs/reference/glossary/) -  포괄적이고, 표준화 된 쿠버네티스 용어 목록

* [쿠버네티스 API 레퍼런스](/docs/reference/kubernetes-api/)
* [쿠버네티스 {{< param "version" >}}용 원페이지(One-page) API 레퍼런스](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/)
* [쿠버네티스 API 사용](/ko/docs/reference/using-api/) - 쿠버네티스 API에 대한 개요
* [API 접근 제어](/ko/docs/reference/access-authn-authz/) - 쿠버네티스가 API 접근을 제어하는 방법에 대한 세부사항
* [잘 알려진 레이블, 어노테이션과 테인트](/docs/reference/labels-annotations-taints/)

## 공식적으로 지원되는 클라이언트 라이브러리

프로그래밍 언어에서 쿠버네티스 API를 호출하기 위해서,
[클라이언트 라이브러리](/ko/docs/reference/using-api/client-libraries/)를 사용할 수 있다.
공식적으로 지원되는 클라이언트 라이브러리는 다음과 같다.

- [쿠버네티스 Go 클라이언트 라이브러리](https://github.com/kubernetes/client-go/)
- [쿠버네티스 Python 클라이언트 라이브러리](https://github.com/kubernetes-client/python)
- [쿠버네티스 Java 클라이언트 라이브러리](https://github.com/kubernetes-client/java)
- [쿠버네티스 JavaScript 클라이언트 라이브러리](https://github.com/kubernetes-client/javascript)
- [쿠버네티스 C# 클라이언트 라이브러리](https://github.com/kubernetes-client/csharp)
- [쿠버네티스 Haskell 클라이언트 라이브러리](https://github.com/kubernetes-client/haskell)

## CLI

* [kubectl](/ko/docs/reference/kubectl/overview/) - 명령어를 실행하거나 쿠버네티스 클러스터를 관리하기 위해 사용하는 주된 CLI 도구.
    * [JSONPath](/ko/docs/reference/kubectl/jsonpath/) - kubectl에서 [JSONPath 표현](https://goessner.net/articles/JsonPath/)을 사용하기 위한 문법 가이드.
* [kubeadm](/ko/docs/reference/setup-tools/kubeadm/) - 안정적인 쿠버네티스 클러스터를 쉽게 프로비전하기 위한 CLI 도구.

## 컴포넌트

* [kubelet](/docs/reference/command-line-tools-reference/kubelet/) - 각 
노드에서 구동되는 주요한 에이전트. kubelet은 PodSpecs 집합을 가지며 
기술된 컨테이너가 구동되고 있는지, 정상 작동하는지를 보장한다.
* [kube-apiserver](/docs/reference/command-line-tools-reference/kube-apiserver/) - 
파드, 서비스, 레플리케이션 컨트롤러와 같은 API 오브젝트에 대한 검증과 구성을 
수행하는 REST API.
* [kube-controller-manager](/docs/reference/command-line-tools-reference/kube-controller-manager/) - 쿠버네티스에 탑재된 핵심 제어 루프를 포함하는 데몬.
* [kube-proxy](/ko/docs/reference/command-line-tools-reference/kube-proxy/) - 간단한 
TCP/UDP 스트림 포워딩이나 백-엔드 집합에 걸쳐서 라운드-로빈 TCP/UDP 포워딩을 
할 수 있다.
* [kube-scheduler](/docs/reference/command-line-tools-reference/kube-scheduler/) - 가용성, 성능 및 용량을 관리하는 스케줄러.

  * [kube-scheduler 정책](/ko/docs/reference/scheduling/policies)
  * [kube-scheduler 프로파일](/ko/docs/reference/scheduling/config/#여러-프로파일)

## 환경설정 API

이 섹션은 쿠버네티스 구성요소 또는 도구를 환경설정하는 데에 사용되는 
"미발표된" API를 다룬다. 이 API들은 사용자나 관리자가 클러스터를 
사용/관리하는 데에 중요하지만, 이들 API의 대부분은 아직 API 서버가 
제공하지 않는다.

* [kubelet 환경설정 (v1beta1)](/docs/reference/config-api/kubelet-config.v1beta1/)
* [kube-scheduler 환경설정 (v1beta1)](/docs/reference/config-api/kube-scheduler-config.v1beta1/)
* [kube-scheduler 정책 레퍼런스 (v1)](/docs/reference/config-api/kube-scheduler-policy-config.v1/)
* [kube-proxy 환경설정 (v1alpha1)](/docs/reference/config-api/kube-proxy-config.v1alpha1/)
* [`audit.k8s.io/v1` API](/docs/reference/config-api/apiserver-audit.v1/)
* [클라이언트 인증 API (v1beta1)](/docs/reference/config-api/client-authentication.v1beta1/)
* [WebhookAdmission 환경설정 (v1)](/docs/reference/config-api/apiserver-webhookadmission.v1/)

## 설계 문서

쿠버네티스 기능에 대한 설계 문서의 아카이브.
[쿠버네티스 아키텍처](https://git.k8s.io/community/contributors/design-proposals/architecture/architecture.md)와
[쿠버네티스 디자인 개요](https://git.k8s.io/community/contributors/design-proposals)가 좋은 출발점이다.
