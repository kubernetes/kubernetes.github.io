---
title: 쿠버네티스 API
content_type: concept
weight: 30
description: >
  쿠버네티스 API를 사용하면 쿠버네티스 오브젝트들의 상태를 쿼리하고 조작할 수 있다.
  쿠버네티스 컨트롤 플레인의 핵심은 API 서버와 그것이 노출하는 HTTP API이다. 사용자와 클러스터의 다른 부분 및 모든 외부 컴포넌트는 API 서버를 통해 서로 통신한다.
card:
  name: concepts
  weight: 30
---

<!-- overview -->

쿠버네티스 {{< glossary_tooltip text="컨트롤 플레인" term_id="control-plane" >}}의 핵심은
{{< glossary_tooltip text="API 서버" term_id="kube-apiserver" >}}이다. API 서버는
최종 사용자, 클러스터의 다른 부분 그리고 외부 컴포넌트가 서로 통신할
수 있도록 HTTP API를 제공한다.

쿠버네티스 API를 사용하면 쿠버네티스의 API 오브젝트(예:
파드(Pod), 네임스페이스(Namespace), 컨피그맵(ConfigMap) 그리고 이벤트(Event))를 질의(query)하고 조작할 수 있다.

대부분의 작업은 [kubectl](/ko/docs/reference/kubectl/overview/)
커맨드 라인 인터페이스 또는 API를 사용하는
[kubeadm](/ko/docs/reference/setup-tools/kubeadm/)과
같은 다른 커맨드 라인 도구를 통해 수행할 수 있다.
그러나, REST 호출을 사용하여 API에 직접 접근할 수도 있다.

쿠버네티스 API를 사용하여 애플리케이션을 작성하는 경우
[클라이언트 라이브러리](/ko/docs/reference/using-api/client-libraries/) 중 하나를 사용하는 것이 좋다.

<!-- body -->

## OpenAPI 명세 {#api-specification}

완전한 API 상세 내용은 [OpenAPI](https://www.openapis.org/)를 활용해서 문서화했다.

OpenAPI 규격은 `/openapi/v2` 엔드포인트에서만 제공된다.
다음과 같은 요청 헤더를 사용해서 응답 형식을 요청할 수 있다.

<table>
  <caption style="display:none">Valid request header values for OpenAPI v2 queries</caption>
  <thead>
     <tr>
        <th>Header</th>
        <th style="min-width: 50%;">Possible values</th>
        <th>Notes</th>
     </tr>
  </thead>
  <tbody>
     <tr>
        <td><code>Accept-Encoding</code></td>
        <td><code>gzip</code></td>
        <td><em>not supplying this header is also acceptable</em></td>
     </tr>
     <tr>
        <td rowspan="3"><code>Accept</code></td>
        <td><code>application/com.github.proto-openapi.spec.v2@v1.0+protobuf</code></td>
        <td><em>mainly for intra-cluster use</em></td>
     </tr>
     <tr>
        <td><code>application/json</code></td>
        <td><em>default</em></td>
     </tr>
     <tr>
        <td><code>*</code></td>
        <td><em>serves </em><code>application/json</code></td>
     </tr>
  </tbody>
</table>

쿠버네티스는 주로 클러스터 내부 통신을 위해 대안적인
Protobuf에 기반한 직렬화 형식을 구현한다. 이 형식에 대한
자세한 내용은 [쿠버네티스 Protobuf 직렬화](https://github.com/kubernetes/community/blob/master/contributors/design-proposals/api-machinery/protobuf.md) 디자인 제안과
API 오브젝트를 정의하는 Go 패키지에 들어있는 각각의 스키마에 대한
IDL(인터페이스 정의 언어) 파일을 참고한다.

## 지속성

쿠버네티스는 오브젝트의 직렬화된 상태를
{{< glossary_tooltip term_id="etcd" >}}에 기록하여 저장한다.

## API 그룹과 버전 규칙

필드를 쉽게 제거하거나 리소스 표현을 재구성하기 위해,
쿠버네티스는 각각 `/api/v1` 또는 `/apis/rbac.authorization.k8s.io/v1alpha1` 과
같은 서로 다른 API 경로에서 여러 API 버전을 지원한다.

버전 규칙은 리소스나 필드 수준이 아닌 API 수준에서 수행되어
API가 시스템 리소스 및 동작에 대한 명확하고 일관된 보기를 제공하고
수명 종료 및/또는 실험적 API에 대한 접근을
제어할 수 있도록 한다.

보다 쉽게 발전하고 API를 확장하기 위해, 쿠버네티스는
[활성화 또는 비활성화](/ko/docs/reference/using-api/#api-그룹-활성화-또는-비활성화)가
가능한 [API 그룹](/ko/docs/reference/using-api/#api-그룹)을 구현한다.

API 리소스는 API 그룹, 리소스 유형, 네임스페이스
(네임스페이스 리소스용) 및 이름으로 구분된다. API 서버는 API 버전 간의
변환을 투명하게 처리한다. 서로 다른 모든 버전은 실제로
동일한 지속 데이터의 표현이다. API 서버는 여러 API 버전을 통해
동일한 기본 데이터를 제공할 수 있다.

예를 들어, 동일한 리소스에 대해  `v1` 과 `v1beta1` 이라는 두 가지 API 버전이
있다고 가정한다. 원래 API의 `v1beta1` 버전을 사용하여 오브젝트를
만든 경우, 나중에 `v1beta1` 또는 `v1` API 버전을 사용하여 해당 오브젝트를
읽거나, 업데이트하거나, 삭제할 수 있다.

## API 변경 사항

성공적인 시스템은 새로운 유스케이스가 등장하거나 기존 사례가 변경됨에 따라 성장하고 변화해야 한다.
따라서, 쿠버네티스는 쿠버네티스 API가 지속적으로 변경되고 성장할 수 있도록 설계했다.
쿠버네티스 프로젝트는 기존 클라이언트와의 호환성을 깨지 _않고_ 다른 프로젝트가
적응할 기회를 가질 수 있도록 장기간 해당 호환성을 유지하는 것을 목표로 한다.

일반적으로, 새 API 리소스와 새 리소스 필드는 자주 추가될 수 있다.
리소스 또는 필드를 제거하려면
[API 지원 중단 정책](/docs/reference/using-api/deprecation-policy/)을 따라야 한다.

쿠버네티스는 일반적으로 API 버전 `v1` 에서 안정 버전(GA)에 도달하면, 공식 쿠버네티스 API에
대한 호환성 유지를 강력하게 이행한다. 또한,
쿠버네티스는 가능한 경우 _베타_ API 버전에서도 호환성을 유지한다.
베타 API를 채택하면 기능이 안정된 후에도 해당 API를 사용하여 클러스터와
계속 상호 작용할 수 있다.

{{< note >}}
쿠버네티스는 또한 _알파_ API 버전에 대한 호환성을 유지하는 것을 목표로 하지만, 일부
상황에서는 호환성이 깨진다. 알파 API 버전을 사용하는 경우, API가 변경된 경우 클러스터를
업그레이드할 때 쿠버네티스에 대한 릴리스 정보를 확인한다.
{{< /note >}}

API 버전 수준 정의에 대한 자세한 내용은
[API 버전 레퍼런스](/ko/docs/reference/using-api/#api-버전-규칙)를 참조한다.



## API 확장

쿠버네티스 API는 다음 두 가지 방법 중 하나로 확장할 수 있다.

1. [커스텀 리소스](/ko/docs/concepts/extend-kubernetes/api-extension/custom-resources/)를
   사용하면 API 서버가 선택한 리소스 API를 제공하는 방법을 선언적으로 정의할 수 있다.
1. [애그리게이션 레이어(aggregation layer)](/ko/docs/concepts/extend-kubernetes/api-extension/apiserver-aggregation/)를
   구현하여 쿠버네티스 API를 확장할 수도 있다.

## {{% heading "whatsnext" %}}

- 자체 [CustomResourceDefinition](/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/)을
  추가하여 쿠버네티스 API를 확장하는 방법에 대해 배우기.
- [쿠버네티스 API 접근 제어하기](/ko/docs/concepts/security/controlling-access/)는
  클러스터가 API 접근을 위한 인증 및 권한을 관리하는 방법을 설명한다.
- [API 레퍼런스](/docs/reference/kubernetes-api/)를
  읽고 API 엔드포인트, 리소스 유형 및 샘플에 대해 배우기.
- [API 변경 사항](https://git.k8s.io/community/contributors/devel/sig-architecture/api_changes.md#readme)에서
  호환 가능한 변경 사항을 구성하고, API를 변경하는 방법에 대해 알아본다.
