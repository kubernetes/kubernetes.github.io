---




title: 네트워크 정책
content_type: concept
weight: 50
---

<!-- overview -->

IP 주소 또는 포트 수준(OSI 계층 3 또는 4)에서 트래픽 흐름을 제어하려는 경우, 클러스터의 특정 애플리케이션에 대해 쿠버네티스 네트워크폴리시(NetworkPolicy) 사용을 고려할 수 있다. 네트워크폴리시는 {{< glossary_tooltip text="파드" term_id="pod" >}}가 네트워크 상의 다양한 네트워크 "엔티티"(여기서는 "엔티티"를 사용하여 쿠버네티스에서 특별한 의미로 사용되는 "엔드포인트" 및 "서비스"와 같은 일반적인 용어가 중의적으로 표현되는 것을 방지함)와 통신할 수 있도록 허용하는 방법을 지정할 수 있는 애플리케이션 중심 구조이다.

파드가 통신할 수 있는 엔티티는 다음 3개의 식별자 조합을 통해 식별된다.

1. 허용되는 다른 파드(예외: 파드는 자신에 대한 접근을 차단할 수 없음)
2. 허용되는 네임스페이스
3. IP 블록(예외: 파드 또는 노드의 IP 주소와 관계없이 파드가 실행 중인 노드와의 트래픽은 항상 허용됨)

pod- 또는 namespace- 기반의 네트워크폴리시를 정의할 때, {{< glossary_tooltip text="셀렉터" term_id="selector" >}}를 사용하여 셀렉터와 일치하는 파드와 주고받는 트래픽을 지정한다.

한편, IP 기반의 네트워크폴리시가 생성되면, IP 블록(CIDR 범위)을 기반으로 정책을 정의한다.

<!-- body -->
## 전제 조건

네트워크 정책은 [네트워크 플러그인](/ko/docs/concepts/extend-kubernetes/compute-storage-net/network-plugins/)으로 구현된다. 네트워크 정책을 사용하려면 네트워크폴리시를 지원하는 네트워킹 솔루션을 사용해야만 한다. 이를 구현하는 컨트롤러 없이 네트워크폴리시 리소스를 생성해도 아무런 효과가 없기 때문이다.

## 격리 및 격리되지 않은 파드

기본적으로, 파드는 격리되지 않는다. 이들은 모든 소스에서 오는 트래픽을 받아들인다.

파드는 파드를 선택한 네트워크폴리시에 의해서 격리된다. 네임스페이스에 특정 파드를 선택하는 네트워크폴리시가 있으면 해당 파드는 네트워크폴리시에서 허용하지 않는 모든 연결을 거부한다. (네임스페이스 내에서 어떠한 네트워크폴리시에도 선택 받지 않은 다른 파드들은 계속해서 모든 트래픽을 받아들인다.)

네트워크 정책은 충돌하지 않으며, 추가된다. 만약 어떤 정책 또는 정책들이 파드를 선택하면, 해당 정책의 인그레스(수신)/이그레스(송신) 규칙을 통합하여 허용되는 범위로 파드가 제한된다. 따라서 평가 순서는 정책 결과에 영향을 미치지 않는다.

두 파드간 네트워크 흐름을 허용하기 위해서는, 소스 파드의 이그레스 정책과 목적지 파드의 인그레스 정책 모두가 해당 트래픽을 허용해야 한다. 만약 소스의 이그레스 정책이나 목적지의 인그레스 정책 중 한쪽이라도 트래픽을 거절하게 되어 있다면, 해당 트래픽은 거절될 것이다.

## 네트워크폴리시 리소스 {#networkpolicy-resource}

리소스에 대한 전체 정의에 대한 참조는 [네트워크폴리시](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#networkpolicy-v1-networking-k8s-io) 를 본다.

네트워크폴리시 의 예시는 다음과 같다.

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: test-network-policy
  namespace: default
spec:
  podSelector:
    matchLabels:
      role: db
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - ipBlock:
        cidr: 172.17.0.0/16
        except:
        - 172.17.1.0/24
    - namespaceSelector:
        matchLabels:
          project: myproject
    - podSelector:
        matchLabels:
          role: frontend
    ports:
    - protocol: TCP
      port: 6379
  egress:
  - to:
    - ipBlock:
        cidr: 10.0.0.0/24
    ports:
    - protocol: TCP
      port: 5978
```

{{< note >}}
선택한 네트워킹 솔루션이 네트워킹 정책을 지원하지 않으면 클러스터의 API 서버에 이를 POST 하더라도 효과가 없다.
{{< /note >}}

__필수 필드들__: 다른 모든 쿠버네티스 설정과 마찬가지로 네트워크폴리시 에는
`apiVersion`, `kind`, 그리고 `metadata` 필드가 필요하다. 구성 파일
작업에 대한 일반적인 정보는
[컨피그 맵을 사용해서 컨테이너 구성하기](/docs/tasks/configure-pod-container/configure-pod-configmap/),
그리고 [오브젝트 관리](/ko/docs/concepts/overview/working-with-objects/object-management) 를 본다.

__spec__: 네트워크폴리시 [사양](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md#spec-and-status)에는 지정된 네임스페이스에서 특정 네트워크 정책을 정의하는데 필요한 모든 정보가 있다.

__podSelector__: 각 네트워크폴리시에는 정책이 적용되는 파드 그룹을 선택하는 `podSelector` 가 포함된다. 예시 정책은 "role=db" 레이블이 있는 파드를 선택한다. 비어있는 `podSelector` 는 네임스페이스의 모든 파드를 선택한다.

__policyTypes__: 각 네트워크폴리시에는 `Ingress`, `Egress` 또는 두 가지 모두를 포함할 수 있는 `policyTypes` 목록이 포함된다. `policyTypes` 필드는 선택한 파드에 대한 인그레스 트래픽 정책, 선택한 파드에 대한 이그레스 트래픽 정책 또는 두 가지 모두에 지정된 정책의 적용 여부를 나타낸다. 만약 네트워크폴리시에 `policyTypes` 가 지정되어 있지 않으면 기본적으로 `Ingress` 가 항상 설정되고, 네트워크폴리시에 `Egress` 가 있으면 이그레스 규칙이 설정된다.

__ingress__: 각 네트워크폴리시에는 화이트리스트 `ingress` 규칙 목록이 포함될 수 있다. 각 규칙은 `from` 과 `ports` 부분과 모두 일치하는 트래픽을 허용한다. 예시 정책에는 단일 규칙이 포함되어있는데 첫 번째 포트는 `ipBlock` 을 통해 지정되고, 두 번째는 `namespaceSelector` 를 통해 그리고 세 번째는 `podSelector` 를 통해 세 가지 소스 중 하나의 단일 포트에서 발생하는 트래픽과 일치 시킨다.

__egress__: 각 네트워크폴리시에는 화이트리스트 `egress` 규칙이 포함될 수 있다. 각 규칙은 `to` 와 `ports` 부분과 모두 일치하는 트래픽을 허용한다. 예시 정책에는 단일 포트의 트래픽을 `10.0.0.0/24` 의 모든 대상과 일치시키는 단일 규칙을 포함하고 있다.

따라서 예시의 네트워크폴리시는 다음과 같이 동작한다.

1. 인그레스 및 이그레스 트래픽에 대해 "default" 네임스페이스에서 "role=db"인 파드를 격리한다(아직 격리되지 않은 경우).
2. (인그레스 규칙)은 "role=db" 레이블을 사용하는 "default" 네임스페이스의 모든 파드에 대해서 TCP 포트 6397로의 연결을 허용한다. 인그레스을 허용 할 대상은 다음과 같다.

   * "role=frontend" 레이블이 있는 "default" 네임스페이스의 모든 파드
   * 네임스페이스와 "project=myproject" 를 레이블로 가지는 모든 파드
   * 172.17.0.0–172.17.0.255 와 172.17.2.0–172.17.255.255 의 범위를 가지는 IP 주소(예: 172.17.0.0/16 전체에서 172.17.1.0/24 를 제외)
3. (이그레스 규칙)은 "role=db" 레이블이 있는 "default" 네임스페이스의 모든 파드에서 TCP 포트 5978의 CIDR 10.0.0.0/24 로의 연결을 허용한다.

자세한 설명과 추가 예시는 [네트워크 정책 선언](/ko/docs/tasks/administer-cluster/declare-network-policy/)을 본다.

## `to` 및 `from` 셀럭터의 동작

`ingress` `from` 부분 또는 `egress` `to` 부분에 지정할 수 있는 네 종류의 셀렉터가 있다.

__podSelector__: 네트워크폴리시를 통해서, 인그레스 소스 또는 이그레스 목적지로 허용되야 하는 동일한 네임스페이스에 있는 특정 파드들을 선택한다.

__namespaceSelector__: 모든 파드가 인그레스 소스 또는 이그레스를 대상으로 허용되어야 하는 특정 네임스페이스를 선택한다.

__namespaceSelector__ *와* __podSelector__: `namespaceSelector` 와 `podSelector` 를 모두 지정하는 단일 `to`/`from` 항목은 특정 네임스페이스 내에서 특정 파드를 선택한다. 올바른 YAML 구문을 사용하도록 주의해야 한다. 이 정책:

```yaml
  ...
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          user: alice
      podSelector:
        matchLabels:
          role: client
  ...
```

네임스페이스에서 레이블이 `role=client` 인 것과 레이블이 `user=alice` 인 파드의 연결을 허용하는 단일 `from` 요소가 포함되어 있다. 그러나 *이* 정책:

```yaml
  ...
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          user: alice
    - podSelector:
        matchLabels:
          role: client
  ...
```

`from` 배열에 두 개의 요소가 포함되어 있으며, 로컬 네임스페이스에 레이블을 `role=client` 로 가지는 파드 *또는* 네임스페이스에 레이블을 `user=alice` 로 가지는 파드의 연결을 허용한다.

의심스러운 경우, `kubectl describe` 를 사용해서 쿠버네티스가 정책을 어떻게 해석하는지 확인해본다.

__ipBlock__: 인그레스 소스 또는 이그레스 대상으로 허용할 IP CIDR 범위를 선택한다. 파드 IP는 임시적이고 예측할 수 없기에 클러스터 외부 IP이어야 한다.

클러스터 인그레스 및 이그레스 매커니즘은 종종 패킷의 소스 또는 대상 IP의 재작성을
필요로 한다. 이러한 상황이 발생하는 경우, 네트워크폴리시의 처리 전 또는 후에
발생한 것인지 정의되지 않으며, 네트워크 플러그인, 클라우드 공급자,
`서비스` 구현 등의 조합에 따라 동작이 다를 수 있다.

인그레스 사례에서의 의미는 실제 원본 소스 IP를 기준으로 들어오는 패킷을
필터링할 수 있는 반면에 다른 경우에는 네트워크폴리시가 작동하는
"소스 IP"는 `LoadBalancer` 또는 파드가 속한 노드 등의 IP일 수 있다.

이그레스의 경우 파드에서 클러스터 외부 IP로 다시 작성된 `서비스` IP로의 연결은
`ipBlock` 기반의 정책의 적용을 받거나 받지 않을 수 있다는 것을 의미한다.

## 기본 정책

기본적으로 네임스페이스 정책이 없으면 해당 네임스페이스의 파드에 대한 모든 인그레스와 이그레스 트래픽이 허용된다. 다음 예시에서는 해당 네임스페이스의 기본 동작을
변경할 수 있다.

### 기본적으로 모든 인그레스 트래픽 거부

모든 파드를 선택하지만 해당 파드에 대한 인그레스 트래픽은 허용하지 않는 네트워크폴리시를 생성해서 네임스페이스에 대한 "기본" 격리 정책을 생성할 수 있다.

{{< codenew file="service/networking/network-policy-default-deny-ingress.yaml" >}}

이렇게 하면 다른 네트워크폴리시에서 선택하지 않은 파드도 여전히 격리된다. 이 정책은 기본 이그레스 격리 동작을 변경하지 않는다.

### 기본적으로 모든 인그레스 트래픽 허용

만약 네임스페이스의 모든 파드에 대한 모든 트래픽을 허용하려는 경우(일부 파드가 "격리 된" 것으로 처리되는 정책이 추가 된 경우에도) 해당 네임스페이스의 모든 트래픽을 명시적으로 허용하는 정책을 만들 수 있다.

{{< codenew file="service/networking/network-policy-allow-all-ingress.yaml" >}}

### 기본적으로 모든 이그레스 트래픽 거부

모든 파드를 선택하지만, 해당 파드의 이그레스 트래픽을 허용하지 않는 네트워크폴리시를 생성해서 네임스페이스에 대한 "기본" 이그레스 격리 정책을 생성할 수 있다.

{{< codenew file="service/networking/network-policy-default-deny-egress.yaml" >}}

이렇게 하면 다른 네트워크폴리시에서 선택하지 않은 파드조차도 이그레스 트래픽을 허용하지 않는다. 이 정책은
기본 인그레스 격리 정책을 변경하지 않는다.

### 기본적으로 모든 이그레스 트래픽 허용

만약 네임스페이스의 모든 파드의 모든 트래픽을 허용하려면 (일부 파드가 "격리 된"으로 처리되는 정책이 추가 된 경우에도) 해당 네임스페이스에서 모든 이그레스 트래픽을 명시적으로 허용하는 정책을 생성할 수 있다.

{{< codenew file="service/networking/network-policy-allow-all-egress.yaml" >}}

### 기본적으로 모든 인그레스와 모든 이그레스 트래픽 거부

해당 네임스페이스에 아래의 네트워크폴리시를 만들어 모든 인그레스와 이그레스 트래픽을 방지하는 네임스페이스에 대한 "기본" 정책을 만들 수 있다.

{{< codenew file="service/networking/network-policy-default-deny-all.yaml" >}}

이렇게 하면 다른 네트워크폴리시에서 선택하지 않은 파드도 인그레스 또는 이그레스 트래픽을 허용하지 않는다.

## SCTP 지원

{{< feature-state for_k8s_version="v1.20" state="stable" >}}

안정된 기능으로, 기본 활성화되어 있다. 클러스터 수준에서 SCTP를 비활성화하려면, 사용자(또는 클러스터 관리자)가 API 서버에 `--feature-gates=SCTPSupport=false,…` 를 사용해서 `SCTPSupport` [기능 게이트](/ko/docs/reference/command-line-tools-reference/feature-gates/)를 비활성화해야 한다.
해당 기능 게이트가 활성화되어 있는 경우, 네트워크폴리시의 `protocol` 필드를 `SCTP`로 지정할 수 있다.

{{< note >}}
SCTP 프로토콜 네트워크폴리시를 지원하는 {{< glossary_tooltip text="CNI" term_id="cni" >}} 플러그인을 사용하고 있어야 한다.
{{< /note >}}

## 포트 범위 지정

{{< feature-state for_k8s_version="v1.21" state="alpha" >}}

네트워크폴리시를 작성할 때, 단일 포트 대신 포트 범위를 대상으로 지정할 수 있다.

다음 예와 같이 `endPort` 필드를 사용하면, 이 작업을 수행할 수 있다.

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: multi-port-egress
  namespace: default
spec:
  podSelector:
    matchLabels:
      role: db
  policyTypes:
  - Egress
  egress:
  - to:
    - ipBlock:
        cidr: 10.0.0.0/24
    ports:
    - protocol: TCP
      port: 32000
      endPort: 32768
```

위 규칙은 대상 포트가 32000에서 32768 사이에 있는 경우, 네임스페이스 `default` 에 레이블이 `db` 인 모든 파드가 TCP를 통해 `10.0.0.0/24` 범위 내의 모든 IP와 통신하도록 허용한다.

이 필드를 사용할 때 다음의 제한 사항이 적용된다.
* 알파 기능으로, 기본적으로 비활성화되어 있다. 클러스터 수준에서 `endPort` 필드를 활성화하려면, 사용자(또는 클러스터 관리자)가 `--feature-gates=NetworkPolicyEndPort=true,…` 가 있는 API 서버에 대해 `NetworkPolicyEndPort` [기능 게이트](/ko/docs/reference/command-line-tools-reference/feature-gates/)를 활성화해야 한다.
* `endPort` 필드는 `port` 필드보다 크거나 같아야 한다.
* `endPort` 는 `port` 도 정의된 경우에만 정의할 수 있다.
* 두 포트 모두 숫자여야 한다.

{{< note >}}
클러스터는 {{< glossary_tooltip text="CNI" term_id="cni" >}} 플러그인을 사용해야 한다.
네트워크폴리시 명세에서 `endPort` 필드를 지원한다.
{{< /note >}}

## 이름으로 네임스페이스 지정

{{< feature-state state="beta" for_k8s_version="1.21" >}}

쿠버네티스 컨트롤 플레인은 `NamespaceDefaultLabelName`
[기능 게이트](/ko/docs/reference/command-line-tools-reference/feature-gates/)가 활성화된 경우
모든 네임스페이스에 변경할 수 없는(immutable) 레이블 `kubernetes.io/metadata.name` 을 설정한다.
레이블의 값은 네임스페이스 이름이다.

네트워크폴리시는 일부 오브젝트 필드가 있는 이름으로 네임스페이스를 대상으로 지정할 수 없지만, 표준화된 레이블을 사용하여
특정 네임스페이스를 대상으로 지정할 수 있다.

## 네트워크 정책으로 할 수 없는 것(적어도 아직은 할 수 없는)

쿠버네티스 {{< skew latestVersion >}}부터 다음의 기능은 네트워크폴리시 API에 존재하지 않지만, 운영 체제 컴포넌트(예: SELinux, OpenVSwitch, IPTables 등) 또는 Layer 7 기술(인그레스 컨트롤러, 서비스 메시 구현) 또는 어드미션 컨트롤러를 사용하여 제2의 해결책을 구현할 수 있다. 쿠버네티스의 네트워크 보안을 처음 사용하는 경우, 네트워크폴리시 API를 사용하여 다음의 사용자 스토리를 (아직) 구현할 수 없다는 점에 유의할 필요가 있다.

- 내부 클러스터 트래픽이 공통 게이트웨이를 통과하도록 강제한다(서비스 메시나 기타 프록시와 함께 제공하는 것이 가장 좋을 수 있음).
- TLS와 관련된 모든 것(이를 위해 서비스 메시나 인그레스 컨트롤러 사용).
- 노드별 정책(이에 대해 CIDR 표기법을 사용할 수 있지만, 특히 쿠버네티스 ID로 노드를 대상으로 지정할 수 없음).
- 이름으로 서비스를 타겟팅한다(그러나, {{< glossary_tooltip text="레이블" term_id="label" >}}로 파드나 네임스페이스를 타겟팅할 수 있으며, 이는 종종 실행할 수 있는 해결 방법임).
- 타사 공급사가 이행한 "정책 요청"의 생성 또는 관리.
- 모든 네임스페이스나 파드에 적용되는 기본 정책(이를 수행할 수 있는 타사 공급사의 쿠버네티스 배포본 및 프로젝트가 있음).
- 고급 정책 쿼리 및 도달 가능성 도구.
- 네트워크 보안 이벤트를 기록하는 기능(예: 차단되거나 수락된 연결).
- 명시적으로 정책을 거부하는 기능(현재 네트워크폴리시 모델은 기본적으로 거부하며, 허용 규칙을 추가하는 기능만 있음).
- 루프백 또는 들어오는 호스트 트래픽을 방지하는 기능(파드는 현재 로컬 호스트 접근을 차단할 수 없으며, 상주 노드의 접근을 차단할 수 있는 기능도 없음).

## {{% heading "whatsnext" %}}


- 자세한 설명과 추가 예시는
  [네트워크 정책 선언](/ko/docs/tasks/administer-cluster/declare-network-policy/)을 본다.
- 네트워크폴리시 리소스에서 사용되는 일반적인 시나리오는 [레시피](https://github.com/ahmetb/kubernetes-network-policy-recipes)를 본다.
