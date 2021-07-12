---
title: 클라우드 네이티브 보안 개요
content_type: concept
weight: 10
---

<!-- overview -->
이 개요는 클라우드 네이티브 보안의 맥락에서 쿠버네티스 보안에 대한 생각의 모델을 정의한다.

{{< warning >}}
이 컨테이너 보안 모델은 입증된 정보 보안 정책이 아닌 제안 사항을 제공한다.
{{< /warning >}}


<!-- body -->

## 클라우드 네이티브 보안의 4C

보안은 계층으로 생각할 수 있다. 클라우드 네이티브 보안의 4C는 클라우드(Cloud),
클러스터(Cluster), 컨테이너(Container)와 코드(Code)이다.

{{< note >}}
이 계층화된 접근 방식은 보안에 대한 [심층 방어](https://en.wikipedia.org/wiki/Defense_in_depth_(computing))
컴퓨팅 접근 방식을 강화하며, 소프트웨어 시스템의 보안을 위한 모범 사례로
널리 알려져 있다.
{{< /note >}}

{{< figure src="/images/docs/4c.png" title="클라우드 네이티브 보안의 4C" >}}

클라우드 네이티브 보안 모델의 각 계층은 다음의 가장 바깥쪽 계층을 기반으로 한다.
코드 계층은 강력한 기본(클라우드, 클러스터, 컨테이너) 보안 계층의 이점을 제공한다.
코드 수준에서 보안을 처리하여 기본 계층의 열악한 보안 표준을
보호할 수 없다.

## 클라우드

여러 면에서 클라우드(또는 공동 위치 서버, 또는 기업의 데이터 센터)는 쿠버네티스 클러스터 구성을 위한
[신뢰 컴퓨팅 기반(trusted computing base)](https://en.wikipedia.org/wiki/Trusted_computing_base)
이다. 클라우드 계층이 취약하거나 취약한 방식으로
구성된 경우 이 기반 위에서 구축된 구성 요소가 안전하다는
보장은 없다. 각 클라우드 공급자는 해당 환경에서 워크로드를 안전하게 실행하기
위한 보안 권장 사항을 제시한다.

### 클라우드 공급자 보안

자신의 하드웨어 또는 다른 클라우드 공급자에서 쿠버네티스 클러스터를 실행 중인 경우,
보안 모범 사례는 설명서를 참고한다.
다음은 인기있는 클라우드 공급자의 보안 문서 중 일부에 대한 링크이다.

{{< table caption="클라우드 공급자 보안" >}}

IaaS 공급자        | 링크 |
-------------------- | ------------ |
Alibaba Cloud | https://www.alibabacloud.com/trust-center |
Amazon Web Services | https://aws.amazon.com/security/ |
Google Cloud Platform | https://cloud.google.com/security/ |
IBM Cloud | https://www.ibm.com/cloud/security |
Microsoft Azure | https://docs.microsoft.com/en-us/azure/security/azure-security |
VMWare VSphere | https://www.vmware.com/security/hardening-guides.html |

{{< /table >}}

### 인프라스트럭처 보안 {#infrastructure-security}

쿠버네티스 클러스터에서 인프라 보안을 위한 제안은 다음과 같다.

{{< table caption="인프라스트럭처 보안" >}}

쿠버네티스 인프라에서 고려할 영역 | 추천 |
--------------------------------------------- | ------------ |
API 서버에 대한 네트워크 접근(컨트롤 플레인) | 쿠버네티스 컨트롤 플레인에 대한 모든 접근은 인터넷에서 공개적으로 허용되지 않으며 클러스터 관리에 필요한 IP 주소 집합으로 제한된 네트워크 접근 제어 목록에 의해 제어된다. |
노드에 대한 네트워크 접근(노드) | 지정된 포트의 컨트롤 플레인에서 _만_ (네트워크 접근 제어 목록을 통한) 연결을 허용하고 NodePort와 LoadBalancer 유형의 쿠버네티스 서비스에 대한 연결을 허용하도록 노드를 구성해야 한다. 가능하면 이러한 노드가 공용 인터넷에 완전히 노출되어서는 안된다.
클라우드 공급자 API에 대한 쿠버네티스 접근 | 각 클라우드 공급자는 쿠버네티스 컨트롤 플레인 및 노드에 서로 다른 권한 집합을 부여해야 한다. 관리해야하는 리소스에 대해 [최소 권한의 원칙](https://en.wikipedia.org/wiki/Principle_of_least_privilege)을 따르는 클라우드 공급자의 접근 권한을 클러스터에 구성하는 것이 가장 좋다. [Kops 설명서](https://github.com/kubernetes/kops/blob/master/docs/iam_roles.md#iam-roles)는 IAM 정책 및 역할에 대한 정보를 제공한다.
etcd에 대한 접근 | etcd(쿠버네티스의 데이터 저장소)에 대한 접근은 컨트롤 플레인으로만 제한되어야 한다. 구성에 따라 TLS를 통해 etcd를 사용해야 한다. 자세한 내용은 [etcd 문서](https://github.com/etcd-io/etcd/tree/master/Documentation)에서 확인할 수 있다.
etcd 암호화 | 가능한 한 모든 드라이브를 암호화하는 것이 좋은 방법이지만, etcd는 전체 클러스터(시크릿 포함)의 상태를 유지하고 있기에 특히 디스크는 암호화되어 있어야 한다.

{{< /table >}}

## 클러스터

쿠버네티스 보안에는 다음의 두 가지 영역이 있다.

* 설정 가능한 클러스터 컴포넌트의 보안
* 클러스터에서 실행되는 애플리케이션의 보안


### 클러스터의 컴포넌트 {#cluster-components}

우발적이거나 악의적인 접근으로부터 클러스터를 보호하고,
모범 사례에 대한 정보를 채택하기 위해서는
[클러스터 보안](/docs/tasks/administer-cluster/securing-a-cluster/)에 대한 조언을 읽고 따른다.

### 클러스터 내 컴포넌트(애플리케이션) {#cluster-applications}

애플리케이션의 공격 영역에 따라, 보안의 특정 측면에
중점을 둘 수 있다. 예를 들어, 다른 리소스 체인에 중요한 서비스(서비스 A)와
리소스 소진 공격에 취약한 별도의 작업 부하(서비스 B)를 실행하는 경우,
서비스 B의 리소스를 제한하지 않으면
서비스 A가 손상될 위험이 높다. 다음은 쿠버네티스에서
실행되는 워크로드를 보호하기 위한 보안 문제 및 권장 사항이 나와 있는 표이다.

워크로드 보안에서 고려할 영역 | 추천 |
------------------------------ | ------------ |
RBAC 인증(쿠버네티스 API에 대한 접근) | https://kubernetes.io/docs/reference/access-authn-authz/rbac/
인증 | https://kubernetes.io/ko/docs/concepts/security/controlling-access/
애플리케이션 시크릿 관리(및 유휴 상태에서의 etcd 암호화 등) | https://kubernetes.io/docs/concepts/configuration/secret/ <br> https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/
파드 보안 정책 | https://kubernetes.io/docs/concepts/policy/pod-security-policy/
서비스 품질(및 클러스터 리소스 관리) | https://kubernetes.io/docs/tasks/configure-pod-container/quality-service-pod/
네트워크 정책 | https://kubernetes.io/ko/docs/concepts/services-networking/network-policies/
쿠버네티스 인그레스를 위한 TLS | https://kubernetes.io/ko/docs/concepts/services-networking/ingress/#tls

## 컨테이너

컨테이너 보안은 이 가이드의 범위를 벗어난다. 다음은 일반적인 권장사항과
이 주제에 대한 링크이다.

컨테이너에서 고려할 영역 | 추천 |
------------------------------ | ------------ |
컨테이너 취약점 스캔 및 OS에 종속적인 보안 | 이미지 빌드 단계의 일부로 컨테이너에 알려진 취약점이 있는지 검사해야 한다.
이미지 서명 및 시행 | 컨테이너 이미지에 서명하여 컨테이너의 내용에 대한 신뢰 시스템을 유지한다.
권한있는 사용자의 비허용 | 컨테이너를 구성할 때 컨테이너의 목적을 수행하는데 필요한 최소 권한을 가진 사용자를 컨테이너 내에 만드는 방법에 대해서는 설명서를 참조한다.
더 강력한 격리로 컨테이너 런타임 사용 | 더 강력한 격리를 제공하는 [컨테이너 런타임 클래스](/ko/docs/concepts/containers/runtime-class/)를 선택한다.

## 코드

애플리케이션 코드는 가장 많은 제어를 할 수 있는 주요 공격 영역 중 하나이다.
애플리케이션 코드 보안은 쿠버네티스 보안 주제를 벗어나지만,
애플리케이션 코드를 보호하기 위한 권장 사항은 다음과 같다.

### 코드 보안

{{< table caption="코드 보안" >}}

코드에서 고려할 영역 | 추천 |
-------------------------| -------------- |
TLS를 통한 접근 | 코드가 TCP를 통해 통신해야 한다면, 미리 클라이언트와 TLS 핸드 셰이크를 수행한다. 몇 가지 경우를 제외하고, 전송 중인 모든 것을 암호화한다. 한 걸음 더 나아가, 서비스 간 네트워크 트래픽을 암호화하는 것이 좋다. 이것은 인증서를 가지고 있는 두 서비스의 양방향 검증을 [mTLS](https://en.wikipedia.org/wiki/Mutual_authentication)를 통해 수행할 수 있다. |
통신 포트 범위 제한 | 이 권장사항은 당연할 수도 있지만, 가능하면 통신이나 메트릭 수집에 꼭 필요한 서비스의 포트만 노출시켜야 한다. |
타사 종속성 보안 | 애플리케이션의 타사 라이브러리를 정기적으로 스캔하여 현재 알려진 취약점이 없는지 확인하는 것이 좋다. 각 언어에는 이런 검사를 자동으로 수행하는 도구를 가지고 있다. |
정적 코드 분석 | 대부분 언어에는 잠재적으로 안전하지 않은 코딩 방법에 대해 코드 스니펫을 분석할 수 있는 방법을 제공한다. 가능한 언제든지 일반적인 보안 오류에 대해 코드베이스를 스캔할 수 있는 자동화된 도구를 사용하여 검사를 한다. 도구는 다음에서 찾을 수 있다. https://owasp.org/www-community/Source_Code_Analysis_Tools |
동적 탐지 공격 | 잘 알려진 공격 중 일부를 서비스에 테스트할 수 있는 자동화된 몇 가지 도구가 있다. 여기에는 SQL 인젝션, CSRF 및 XSS가 포함된다. 가장 널리 사용되는 동적 분석 도구는 [OWASP Zed Attack 프록시](https://owasp.org/www-project-zap/)이다. |

{{< /table >}}

## {{% heading "whatsnext" %}}

쿠버네티스 보안 주제에 관련한 내용들을 배워보자.

* [파드 보안 표준](/docs/concepts/security/pod-security-standards/)
* [파드에 대한 네트워크 정책](/ko/docs/concepts/services-networking/network-policies/)
* [쿠버네티스 API 접근 제어하기](/ko/docs/concepts/security/controlling-access)
* [클러스터 보안](/docs/tasks/administer-cluster/securing-a-cluster/)
* 컨트롤 플레인을 위한 [전송 데이터 암호화](/ko/docs/tasks/tls/managing-tls-in-a-cluster/)
* [Rest에서 데이터 암호화](/docs/tasks/administer-cluster/encrypt-data/)
* [쿠버네티스 시크릿](/ko/docs/concepts/configuration/secret/)
* [런타임 클래스](/ko/docs/concepts/containers/runtime-class)
