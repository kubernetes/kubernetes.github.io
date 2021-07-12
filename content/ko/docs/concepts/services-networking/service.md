---


title: 서비스
feature:
  title: 서비스 디스커버리와 로드 밸런싱
  description: >
    쿠버네티스를 사용하면 익숙하지 않은 서비스 디스커버리 메커니즘을 사용하기 위해 애플리케이션을 수정할 필요가 없다. 쿠버네티스는 파드에게 고유한 IP 주소와 파드 집합에 대한 단일 DNS 명을 부여하고, 그것들 간에 로드-밸런스를 수행할 수 있다.

content_type: concept
weight: 10
---


<!-- overview -->

{{< glossary_definition term_id="service" length="short" >}}

쿠버네티스를 사용하면 익숙하지 않은 서비스 디스커버리 메커니즘을 사용하기 위해 애플리케이션을 수정할 필요가 없다.
쿠버네티스는 파드에게 고유한 IP 주소와 파드 집합에 대한 단일 DNS 명을 부여하고,
그것들 간에 로드-밸런스를 수행할 수 있다.

<!-- body -->

## 동기

쿠버네티스 {{< glossary_tooltip term_id="pod" text="파드" >}}는 클러스터 상태와
일치하도록 생성되고 삭제된다. 파드는 비영구적 리소스이다.
만약 앱을 실행하기 위해 {{< glossary_tooltip term_id="deployment" text="디플로이먼트" >}}를 사용한다면,
동적으로 파드를 생성하고 제거할 수 있다.

각 파드는 고유한 IP 주소를 갖지만, 디플로이먼트에서는
한 시점에 실행되는 파드 집합이
잠시 후 실행되는 해당 파드 집합과 다를 수 있다.

이는 다음과 같은 문제를 야기한다. ("백엔드"라 불리는) 일부 파드 집합이
클러스터의 ("프론트엔드"라 불리는) 다른 파드에 기능을 제공하는 경우,
프론트엔드가 워크로드의 백엔드를 사용하기 위해,
프론트엔드가 어떻게 연결할 IP 주소를 찾아서 추적할 수 있는가?

_서비스_ 로 들어가보자.

## 서비스 리소스 {#service-resource}

쿠버네티스에서 서비스는 파드의 논리적 집합과 그것들에 접근할 수 있는
정책을 정의하는 추상적 개념이다. (때로는 이 패턴을
마이크로-서비스라고 한다.) 서비스가 대상으로 하는 파드 집합은 일반적으로
{{< glossary_tooltip text="셀렉터" term_id="selector" >}}가 결정한다.
서비스 엔드포인트를 정의하는 다른 방법에 대한 자세한 내용은
[셀렉터가 _없는_ 서비스](#셀렉터가-없는-서비스)를 참고한다.

예를 들어, 3개의 레플리카로 실행되는 스테이트리스 이미지-처리 백엔드를
생각해보자. 이러한 레플리카는 대체 가능하다. 즉, 프론트엔드는 그것들이 사용하는 백엔드를
신경쓰지 않는다. 백엔드 세트를 구성하는 실제 파드는 변경될 수 있지만,
프론트엔드 클라이언트는 이를 인식할 필요가 없으며, 백엔드 세트 자체를 추적해야 할 필요도
없다.

서비스 추상화는 이러한 디커플링을 가능하게 한다.

### 클라우드-네이티브 서비스 디스커버리

애플리케이션에서 서비스 디스커버리를 위해 쿠버네티스 API를 사용할 수 있는 경우,
서비스 내 파드 세트가 변경될 때마다 업데이트되는 엔드포인트를 {{< glossary_tooltip text="API 서버" term_id="kube-apiserver" >}}에
질의할 수 ​​있다.

네이티브 애플리케이션이 아닌 (non-native applications) 경우, 쿠버네티스는 애플리케이션과 백엔드 파드 사이에 네트워크 포트 또는 로드
밸런서를 배치할 수 있는 방법을 제공한다.

## 서비스 정의

쿠버네티스의 서비스는 파드와 비슷한 REST 오브젝트이다. 모든 REST 오브젝트와
마찬가지로, 서비스 정의를 API 서버에 `POST`하여
새 인스턴스를 생성할 수 있다.
서비스 오브젝트의 이름은 유효한
[DNS 서브도메인 이름](/ko/docs/concepts/overview/working-with-objects/names/#dns-서브도메인-이름)이어야 한다.

예를 들어, 각각 TCP 포트 9376에서 수신하고
`app=MyApp` 레이블을 가지고 있는 파드 세트가 있다고 가정해 보자.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  selector:
    app: MyApp
  ports:
    - protocol: TCP
      port: 80
      targetPort: 9376
```

이 명세는 "my-service"라는 새로운 서비스 오브젝트를 생성하고,
`app=MyApp` 레이블을 가진 파드의 TCP 9376 포트를 대상으로 한다.

쿠버네티스는 이 서비스에 서비스 프록시가 사용하는 IP 주소 ("cluster IP"라고도 함)
를 할당한다.
(이하 [가상 IP와 서비스 프록시](#가상-ip와-서비스-프록시) 참고)

서비스 셀렉터의 컨트롤러는 셀렉터와 일치하는 파드를 지속적으로 검색하고,
"my-service"라는 엔드포인트 오브젝트에 대한
모든 업데이트를 POST한다.

{{< note >}}
서비스는 _모든_ 수신 `port`를 `targetPort`에 매핑할 수 있다. 기본적으로 그리고
편의상, `targetPort`는 `port`
필드와 같은 값으로 설정된다.
{{< /note >}}

파드의 포트 정의에는 이름이 있고, 서비스의 `targetPort` 속성에서 이 이름을
참조할 수 있다. 이것은 다른 포트 번호를 통한 가용한 동일 네트워크 프로토콜이 있고,
단일 구성 이름을 사용하는 서비스 내에
혼합된 파드가 존재해도 가능하다.
이를 통해 서비스를 배포하고 진전시키는데 많은 유연성을 제공한다.
예를 들어, 클라이언트를 망가뜨리지 않고, 백엔드 소프트웨어의 다음
버전에서 파드가 노출시키는 포트 번호를 변경할 수 있다.

서비스의 기본 프로토콜은 TCP이다. 다른
[지원되는 프로토콜](#protocol-support)을 사용할 수도 있다.

많은 서비스가 하나 이상의 포트를 노출해야 하기 때문에, 쿠버네티스는 서비스 오브젝트에서 다중
포트 정의를 지원한다.
각 포트는 동일한 `프로토콜` 또는 다른 프로토콜로 정의될 수 있다.

### 셀렉터가 없는 서비스

서비스는 일반적으로 쿠버네티스 파드에 대한 접근을 추상화하지만,
다른 종류의 백엔드를 추상화할 수도 있다.
예를 들면

* 프로덕션 환경에서는 외부 데이터베이스 클러스터를 사용하려고 하지만,
  테스트 환경에서는 자체 데이터베이스를 사용한다.
* 한 서비스에서 다른
  {{< glossary_tooltip term_id="namespace" text="네임스페이스">}} 또는 다른 클러스터의 서비스를 지정하려고 한다.
* 워크로드를 쿠버네티스로 마이그레이션하고 있다. 해당 방식을 평가하는 동안,
  쿠버네티스에서는 백엔드의 일부만 실행한다.

이러한 시나리오 중에서 파드 셀렉터 _없이_ 서비스를 정의 할 수 있다.
예를 들면

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  ports:
    - protocol: TCP
      port: 80
      targetPort: 9376
```

이 서비스에는 셀렉터가 없으므로, 해당 엔드포인트 오브젝트가 자동으로
생성되지 않는다. 엔드포인트 오브젝트를 수동으로 추가하여, 서비스를 실행 중인 네트워크 주소 및 포트에
서비스를 수동으로 매핑할 수 있다.

```yaml
apiVersion: v1
kind: Endpoints
metadata:
  name: my-service
subsets:
  - addresses:
      - ip: 192.0.2.42
    ports:
      - port: 9376
```

엔드포인트 오브젝트의 이름은 유효한
[DNS 서브도메인 이름](/ko/docs/concepts/overview/working-with-objects/names/#dns-서브도메인-이름)이어야 한다.

{{< note >}}
엔드포인트 IP는 루프백(loopback) (IPv4의 경우 127.0.0.0/8, IPv6의 경우 ::1/128), 또는
링크-로컬 (IPv4의 경우 169.254.0.0/16와 224.0.0.0/24, IPv6의 경우 fe80::/64)이 _되어서는 안된다_.

엔드포인트 IP 주소는 다른 쿠버네티스 서비스의 클러스터 IP일 수 없는데,
{{< glossary_tooltip term_id="kube-proxy" >}}는 가상 IP를
목적지(destination)로 지원하지 않기 때문이다.
{{< /note >}}

셀렉터가 없는 서비스에 접근하면 셀렉터가 있는 것처럼 동일하게 작동한다.
위의 예에서, 트래픽은 YAML에 정의된 단일 엔드 포인트로
라우팅된다. `192.0.2.42:9376` (TCP)

ExternalName 서비스는 셀렉터가 없고
DNS명을 대신 사용하는 특수한 상황의 서비스이다. 자세한 내용은
이 문서 뒷부분의 [ExternalName](#externalname) 섹션을 참조한다.

### 초과 용량 엔드포인트
엔드포인트 리소스에 1,000개가 넘는 엔드포인트가 있는 경우 쿠버네티스 v1.21(또는 그 이상)
클러스터는 해당 엔드포인트에 `endpoints.kubernetes.io/over-capacity: warning` 어노테이션을 추가한다.
이 어노테이션은 영향을 받는 엔드포인트 오브젝트가 용량을 초과했음을 나타낸다.

### 엔드포인트슬라이스

{{< feature-state for_k8s_version="v1.21" state="stable" >}}

엔드포인트슬라이스는 엔드포인트에 보다 확장 가능한 대안을 제공할 수 있는
API 리소스이다. 개념적으로 엔드포인트와 매우 유사하지만, 엔드포인트슬라이스를
사용하면 여러 리소스에 네트워크 엔드포인트를 분산시킬 수 있다. 기본적으로,
엔드포인트슬라이스는 100개의 엔드포인트에 도달하면 "가득찬 것"로 간주되며,
추가 엔드포인트를 저장하기 위해서는 추가 엔드포인트슬라이스가
생성된다.

엔드포인트슬라이스는 [엔드포인트슬라이스](/ko/docs/concepts/services-networking/endpoint-slices/)에서
자세하게 설명된 추가적인 속성 및 기능을 제공한다.

### 애플리케이션 프로토콜

{{< feature-state for_k8s_version="v1.20" state="stable" >}}

`appProtocol` 필드는 각 서비스 포트에 대한 애플리케이션 프로토콜을 지정하는 방법을 제공한다.
이 필드의 값은 해당 엔드포인트와 엔드포인트슬라이스
오브젝트에 의해 미러링된다.

이 필드는 표준 쿠버네티스 레이블 구문을 따른다. 값은
[IANA 표준 서비스 이름](https://www.iana.org/assignments/service-names) 또는
`mycompany.com/my-custom-protocol`과 같은 도메인 접두사 이름 중 하나여야 한다.

## 가상 IP와 서비스 프록시

쿠버네티스 클러스터의 모든 노드는 `kube-proxy`를 실행한다. `kube-proxy`는
[`ExternalName`](#externalname) 이외의 유형의 `서비스`에 대한
가상 IP 형식을 구현한다.

### 라운드-로빈 DNS를 사용하지 않는 이유

항상 발생하는 질문은 왜 쿠버네티스가 인바운드 트래픽을 백엔드로 전달하기 위해 프록시에
의존하는가 하는 점이다. 다른 접근법이
있는가? 예를 들어, 여러 A 값 (또는 IPv6의 경우 AAAA)을 가진
DNS 레코드를 구성하고, 라운드-로빈 이름 확인 방식을
취할 수 있는가?

서비스에 프록시를 사용하는 데는 몇 가지 이유가 있다.

* 레코드 TTL을 고려하지 않고, 만료된 이름 검색 결과를
  캐싱하는 DNS 구현에 대한 오래된 역사가 있다.
* 일부 앱은 DNS 검색을 한 번만 수행하고 결과를 무기한으로 캐시한다.
* 앱과 라이브러리가 적절히 재-확인을 했다고 하더라도, DNS 레코드의 TTL이
  낮거나 0이면 DNS에 부하가 높아 관리하기가
  어려워 질 수 있다.

### 유저 스페이스(User space) 프록시 모드 {#proxy-mode-userspace}

이 모드에서는, kube-proxy는 쿠버네티스 컨트롤 플레인의 서비스 및 엔드포인트 오브젝트의
추가와 제거를 감시한다. 각 서비스는 로컬 노드에서
포트(임의로 선택됨)를 연다. 이 "프록시 포트"에 대한 모든
연결은 (엔드포인트를 통해 보고된 대로) 서비스의 백엔드 파드 중 하나로 프록시된다.
kube-proxy는 사용할 백엔드 파드를 결정할 때 서비스의
`SessionAffinity` 설정을 고려한다.

마지막으로, 유저-스페이스 프록시는 서비스의
`clusterIP` (가상)와 `port` 에 대한 트래픽을 캡처하는 iptables 규칙을 설치한다. 이 규칙은
트래픽을 백엔드 파드를 프록시하는 프록시 포트로 리다이렉션한다.

기본적으로, 유저스페이스 모드의 kube-proxy는 라운드-로빈 알고리즘으로 백엔드를 선택한다.

![유저스페이스 프록시에 대한 서비스 개요 다이어그램](/images/docs/services-userspace-overview.svg)

### `iptables` 프록시 모드 {#proxy-mode-iptables}

이 모드에서는, kube-proxy는 쿠버네티스 컨트롤 플레인의 서비스, 엔드포인트 오브젝트의
추가와 제거를 감시한다. 각 서비스에 대해, 서비스의
`clusterIP` 및 `port`에 대한 트래픽을 캡처하고 해당 트래픽을 서비스의
백엔드 세트 중 하나로 리다이렉트(redirect)하는
iptables 규칙을 설치한다. 각 엔드포인트 오브젝트에 대해,
백엔드 파드를 선택하는 iptables 규칙을 설치한다.

기본적으로, iptables 모드의 kube-proxy는 임의의 백엔드를 선택한다.

트래픽을 처리하기 위해 iptables를 사용하면 시스템 오버헤드가 줄어드는데, 유저스페이스와
커널 스페이스 사이를 전환할 필요없이 리눅스 넷필터(netfilter)가 트래픽을 처리하기
때문이다. 이 접근 방식은 더 신뢰할 수 있기도 하다.

kube-proxy가 iptables 모드에서 실행 중이고 선택된 첫 번째 파드가
응답하지 않으면, 연결이 실패한다. 이는 userspace 모드와
다르다. 해당 시나리오에서는, kube-proxy는 첫 번째
파드에 대한 연결이 실패했음을 감지하고 다른 백엔드 파드로 자동으로 재시도한다.

파드 [준비성 프로브(readiness probe)](/ko/docs/concepts/workloads/pods/pod-lifecycle/#컨테이너-프로브-probe)를 사용하여
백엔드 파드가 제대로 작동하는지 확인할 수 있으므로, iptables 모드의 kube-proxy는
정상으로 테스트된 백엔드만 볼 수 있다. 이렇게 하면 트래픽이 kube-proxy를 통해
실패한 것으로 알려진 파드로 전송되는 것을 막을 수 있다.

![iptables 프록시에 대한 서비스 개요 다이어그램](/images/docs/services-iptables-overview.svg)

### IPVS 프록시 모드 {#proxy-mode-ipvs}

{{< feature-state for_k8s_version="v1.11" state="stable" >}}

`ipvs` 모드에서는, kube-proxy는 쿠버네티스 서비스와 엔드포인트를 감시하고,
`netlink` 인터페이스를 호출하여 그에 따라 IPVS 규칙을 생성하고
IPVS 규칙을 쿠버네티스 서비스와 엔드포인트와 주기적으로 동기화한다.
이 제어 루프는 IPVS 상태가 원하는 상태와 일치하도록
보장한다.
서비스에 접근하면, IPVS는 트래픽을 백엔드 파드 중 하나로 보낸다.

IPVS 프록시 모드는 iptables 모드와 유사한 넷필터 후크 기능을
기반으로 하지만, 해시 테이블을 기본 데이터 구조로 사용하고
커널 스페이스에서 동작한다.
이는 IPVS 모드의 kube-proxy는 iptables 모드의 kube-proxy보다
지연 시간이 짧은 트래픽을 리다이렉션하고, 프록시 규칙을 동기화할 때 성능이
훨씬 향상됨을 의미한다. 다른 프록시 모드와 비교했을 때, IPVS 모드는
높은 네트워크 트래픽 처리량도 지원한다.

IPVS는 트래픽을 백엔드 파드로 밸런싱하기 위한 추가 옵션을 제공한다.
다음과 같다.

* `rr`: 라운드-로빈
* `lc`: 최소 연결 (가장 적은 수의 열려있는 연결)
* `dh`: 목적지 해싱
* `sh`: 소스 해싱
* `sed`: 최단 예상 지연 (shortest expected delay)
* `nq`: 큐 미사용 (never queue)

{{< note >}}
IPVS 모드에서 kube-proxy를 실행하려면, kube-proxy를 시작하기 전에 노드에서 IPVS를
사용 가능하도록 해야 한다.

kube-proxy가 IPVS 프록시 모드에서 시작될 때, IPVS 커널 모듈을
사용할 수 있는지 확인한다. IPVS 커널 모듈이 감지되지 않으면, kube-proxy는
iptables 프록시 모드에서 다시 실행된다.
{{< /note >}}

![IPVS 프록시에 대한 서비스 개요 다이어그램](/images/docs/services-ipvs-overview.svg)

이 프록시 모델에서 클라이언트가 쿠버네티스 또는 서비스 또는 파드에
대해 알지 못하는 경우 서비스의 IP:포트로 향하는 트래픽은
적절한 백엔드로 프록시된다.

특정 클라이언트의 연결이 매번 동일한 파드로
전달되도록 하려면, `service.spec.sessionAffinity`를 "ClientIP"로 설정하여
클라이언트의 IP 주소를 기반으로 세션 어피니티(Affinity)를 선택할 수 있다.
(기본값은 "None")
`service.spec.sessionAffinityConfig.clientIP.timeoutSeconds`를 적절히 설정하여
최대 세션 고정 시간을 설정할 수도 있다.
(기본값은 10800으로, 3시간)

## 멀티-포트 서비스

일부 서비스의 경우, 둘 이상의 포트를 노출해야 한다.
쿠버네티스는 서비스 오브젝트에서 멀티 포트 정의를 구성할 수 있도록 지원한다.
서비스에 멀티 포트를 사용하는 경우, 모든 포트 이름을
명확하게 지정해야 한다.
예를 들면

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  selector:
    app: MyApp
  ports:
    - name: http
      protocol: TCP
      port: 80
      targetPort: 9376
    - name: https
      protocol: TCP
      port: 443
      targetPort: 9377
```

{{< note >}}
쿠버네티스의 일반적인 {{< glossary_tooltip term_id="name" text="이름">}}과 마찬가지로, 포트 이름은
소문자 영숫자와 `-` 만 포함해야 한다. 포트 이름은
영숫자로 시작하고 끝나야 한다.

예를 들어, `123-abc` 와 `web` 은 유효하지만, `123_abc` 와 `-web` 은 유효하지 않다.
{{< /note >}}

## 자신의 IP 주소 선택

`서비스` 생성 요청시 고유한 클러스터 IP 주소를 지정할 수
있다. 이를 위해, `.spec.clusterIP` 필드를 설정한다. 예를 들어,
재사용하려는 기존 DNS 항목이 있거나, 특정 IP 주소로 구성되어
재구성이 어려운 레거시 시스템인 경우이다.

선택한 IP 주소는 API 서버에 대해 구성된 `service-cluster-ip-range`
CIDR 범위 내의 유효한 IPv4 또는 IPv6 주소여야 한다.
유효하지 않은 clusterIP 주소 값으로 서비스를 생성하려고 하면, API 서버는
422 HTTP 상태 코드를 리턴하여 문제점이 있음을 알린다.

## 서비스 디스커버리하기

쿠버네티스는 서비스를 찾는 두 가지 기본 모드를 지원한다. - 환경
변수와 DNS

### 환경 변수

파드가 노드에서 실행될 때, kubelet은 각 활성화된 서비스에 대해
환경 변수 세트를 추가한다. [도커 링크
호환](https://docs.docker.com/userguide/dockerlinks/) 변수
([makeLinkVariables](https://releases.k8s.io/{{< param "githubbranch" >}}/pkg/kubelet/envvars/envvars.go#L49) 참조)와
보다 간단한 `{SVCNAME}_SERVICE_HOST` 및 `{SVCNAME}_SERVICE_PORT` 변수를 지원하고,
이때 서비스 이름은 대문자이고 대시는 밑줄로 변환된다.

예를 들어, TCP 포트 6379를 개방하고
클러스터 IP 주소 10.0.0.11이 할당된 서비스 `redis-master`는,
다음 환경 변수를 생성한다.

```shell
REDIS_MASTER_SERVICE_HOST=10.0.0.11
REDIS_MASTER_SERVICE_PORT=6379
REDIS_MASTER_PORT=tcp://10.0.0.11:6379
REDIS_MASTER_PORT_6379_TCP=tcp://10.0.0.11:6379
REDIS_MASTER_PORT_6379_TCP_PROTO=tcp
REDIS_MASTER_PORT_6379_TCP_PORT=6379
REDIS_MASTER_PORT_6379_TCP_ADDR=10.0.0.11
```

{{< note >}}
서비스에 접근이 필요한 파드가 있고, 환경 변수를
사용해 포트 및 클러스터 IP를 클라이언트 파드에 부여하는
경우, 클라이언트 파드가 생성되기 *전에* 서비스를 만들어야 한다.
그렇지 않으면, 해당 클라이언트 파드는 환경 변수를 생성할 수 없다.

DNS 만 사용하여 서비스의 클러스터 IP를 검색하는 경우, 이 순서
이슈에 대해 신경 쓸 필요가 없다.
{{< /note >}}

### DNS

[애드-온](/ko/docs/concepts/cluster-administration/addons/)을 사용하여 쿠버네티스
클러스터의 DNS 서비스를 설정할 수(대개는 필수적임) 있다.

CoreDNS와 같은, 클러스터-인식 DNS 서버는 새로운 서비스를 위해 쿠버네티스 API를 감시하고
각각에 대한 DNS 레코드 세트를 생성한다. 클러스터 전체에서 DNS가 활성화된 경우
모든 파드는 DNS 이름으로 서비스를 자동으로
확인할 수 있어야 한다.

예를 들면, 쿠버네티스 네임스페이스 `my-ns`에 `my-service`라는
서비스가 있는 경우, 컨트롤 플레인과 DNS 서비스가 함께 작동하여
`my-service.my-ns`에 대한 DNS 레코드를 만든다. `my-ns` 네임 스페이스의 파드들은
`my-service`(`my-service.my-ns` 역시 동작함)에 대한 이름 조회를
수행하여 서비스를 찾을 수 있어야 한다.

다른 네임스페이스의 파드들은 이름을 `my-service.my-ns`으로 사용해야 한다. 이 이름은
서비스에 할당된 클러스터 IP로 변환된다.

쿠버네티스는 또한 알려진 포트에 대한 DNS SRV (서비스) 레코드를 지원한다.
`my-service.my-ns` 서비스에 프로토콜이 `TCP`로 설정된 `http`라는 포트가 있는 경우,
IP 주소와 `http`에 대한 포트 번호를 검색하기 위해 `_http._tcp.my-service.my-ns` 에 대한
DNS SRV 쿼리를 수행할 수 있다.

쿠버네티스 DNS 서버는 `ExternalName` 서비스에 접근할 수 있는 유일한 방법이다.
[DNS 파드와 서비스](/ko/docs/concepts/services-networking/dns-pod-service/)에서
`ExternalName` 검색에 대한 자세한 정보를 찾을 수 있다.

## 헤드리스(Headless) 서비스

때때로 로드-밸런싱과 단일 서비스 IP는 필요치 않다. 이 경우,
"헤드리스" 서비스라는 것을 만들 수 있는데, 명시적으로
클러스터 IP (`.spec.clusterIP`)에 "None"을 지정한다.

쿠버네티스의 구현에 묶이지 않고, 헤드리스 서비스를 사용하여
다른 서비스 디스커버리 메커니즘과 인터페이스할 수 있다.

헤드리스 `서비스`의 경우, 클러스터 IP가 할당되지 않고, kube-proxy가
이러한 서비스를 처리하지 않으며, 플랫폼에 의해 로드 밸런싱 또는 프록시를
하지 않는다. DNS가 자동으로 구성되는 방법은 서비스에 셀렉터가 정의되어 있는지
여부에 달려있다.

### 셀렉터가 있는 경우

셀렉터를 정의하는 헤드리스 서비스의 경우, 엔드포인트 컨트롤러는
API에서 `엔드포인트` 레코드를 생성하고, DNS 구성을 수정하여
`서비스` 를 지원하는 `파드` 를 직접 가리키는 A 레코드(IP 주소)를 반환한다.

### 셀렉터가 없는 경우

셀렉터를 정의하지 않는 헤드리스 서비스의 경우, 엔드포인트 컨트롤러는
`엔드포인트` 레코드를 생성하지 않는다. 그러나 DNS 시스템은 다음 중 하나를 찾고
구성한다.

* [`ExternalName`](#externalname)-유형 서비스에 대한 CNAME 레코드
* 다른 모든 유형에 대해, 서비스의 이름을 공유하는 모든 `엔드포인트`에
  대한 레코드

## 서비스 퍼블리싱 (ServiceTypes) {#publishing-services-service-types}

애플리케이션 중 일부(예: 프론트엔드)는 서비스를 클러스터 밖에
위치한 외부 IP 주소에 노출하고 싶은 경우가 있을 것이다.

쿠버네티스 `ServiceTypes`는 원하는 서비스 종류를 지정할 수 있도록 해준다.
기본 값은 `ClusterIP`이다.

`Type` 값과 그 동작은 다음과 같다.

* `ClusterIP`: 서비스를 클러스터-내부 IP에 노출시킨다. 이 값을 선택하면
  클러스터 내에서만 서비스에 도달할 수 있다. 이것은
  `ServiceTypes`의 기본 값이다.
* [`NodePort`](#nodeport): 고정 포트 (`NodePort`)로 각 노드의 IP에 서비스를
  노출시킨다. `NodePort` 서비스가 라우팅되는 `ClusterIP` 서비스가
  자동으로 생성된다. `<NodeIP>:<NodePort>`를 요청하여,
  클러스터 외부에서
  `NodePort` 서비스에 접속할 수 있다.
* [`LoadBalancer`](#loadbalancer): 클라우드 공급자의 로드 밸런서를 사용하여
  서비스를 외부에 노출시킨다. 외부 로드 밸런서가 라우팅되는
  `NodePort`와 `ClusterIP` 서비스가 자동으로 생성된다.
* [`ExternalName`](#externalname): 값과 함께 CNAME 레코드를 리턴하여, 서비스를
  `externalName` 필드의 콘텐츠 (예:`foo.bar.example.com`)에
  매핑한다. 어떤 종류의 프록시도 설정되어 있지 않다.
  {{< note >}}`ExternalName` 유형을 사용하려면 kube-dns 버전 1.7 또는
  CoreDNS 버전 1.7 이상이 필요하다.
  {{< /note >}}

[인그레스](/ko/docs/concepts/services-networking/ingress/)를 사용하여 서비스를 노출시킬 수도 있다. 인그레스는 서비스 유형이 아니지만, 클러스터의 진입점 역할을 한다. 동일한 IP 주소로 여러 서비스를
노출시킬 수 있기 때문에 라우팅 규칙을 단일 리소스로 통합할 수 있다.

### NodePort 유형 {#nodeport}

`type` 필드를 `NodePort`로 설정하면, 쿠버네티스 컨트롤 플레인은
`--service-node-port-range` 플래그로 지정된 범위에서 포트를 할당한다 (기본값 : 30000-32767).
각 노드는 해당 포트 (모든 노드에서 동일한 포트 번호)를 서비스로 프록시한다.
서비스는 할당된 포트를 `.spec.ports[*].nodePort` 필드에 나타낸다.

포트를 프록시하기 위해 특정 IP를 지정하려면, kube-proxy에 대한
`--nodeport-addresses` 플래그 또는
[kube-proxy 구성 파일](/docs/reference/config-api/kube-proxy-config.v1alpha1/)의
동등한 `nodePortAddresses` 필드를
특정 IP 블록으로 설정할 수 있다.
이 플래그는 쉼표로 구분된 IP 블록 목록(예: `10.0.0.0/8`, `192.0.2.0/25`)을 사용하여 kube-proxy가 로컬 노드로 고려해야 하는 IP 주소 범위를 지정한다.

예를 들어, `--nodeport-addresses=127.0.0.0/8` 플래그로 kube-proxy를 시작하면, kube-proxy는 NodePort 서비스에 대하여 루프백(loopback) 인터페이스만 선택한다. `--nodeport-addresses`의 기본 값은 비어있는 목록이다. 이것은 kube-proxy가 NodePort에 대해 사용 가능한 모든 네트워크 인터페이스를 고려해야 한다는 것을 의미한다. (이는 이전 쿠버네티스 릴리스와도 호환된다).

특정 포트 번호를 원한다면, `nodePort` 필드에 값을 지정할 수
있다. 컨트롤 플레인은 해당 포트를 할당하거나 API 트랜잭션이
실패했다고 보고한다.
이는 사용자 스스로 포트 충돌의 가능성을 고려해야 한다는 의미이다.
또한 NodePort 사용을 위해 구성된 범위 내에 있는, 유효한 포트 번호를
사용해야 한다.

NodePort를 사용하면 자유롭게 자체 로드 밸런싱 솔루션을 설정하거나,
쿠버네티스가 완벽하게 지원하지 않는 환경을 구성하거나,
하나 이상의 노드 IP를 직접 노출시킬 수 있다.

이 서비스는 `<NodeIP>:spec.ports[*].nodePort`와
`.spec.clusterIP:spec.ports[*].port`로 표기된다.
kube-proxy에 대한 `--nodeport-addresses` 플래그 또는 kube-proxy 구성 파일의
동등한 필드가 설정된 경우, `<NodeIP>` 는 노드 IP를 필터링한다.

예를 들면

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  type: NodePort
  selector:
    app: MyApp
  ports:
      # 기본적으로 그리고 편의상 `targetPort` 는 `port` 필드와 동일한 값으로 설정된다.
    - port: 80
      targetPort: 80
      # 선택적 필드
      # 기본적으로 그리고 편의상 쿠버네티스 컨트롤 플레인은 포트 범위에서 할당한다(기본값: 30000-32767)
      nodePort: 30007
```

### 로드밸런서 유형 {#loadbalancer}

외부 로드 밸런서를 지원하는 클라우드 공급자 상에서, `type`
필드를 `LoadBalancer`로 설정하면 서비스에 대한 로드 밸런서를 프로비저닝한다.
로드 밸런서의 실제 생성은 비동기적으로 수행되고,
프로비저닝된 밸런서에 대한 정보는 서비스의
`.status.loadBalancer` 필드에 발행된다.
예를 들면

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  selector:
    app: MyApp
  ports:
    - protocol: TCP
      port: 80
      targetPort: 9376
  clusterIP: 10.0.171.239
  type: LoadBalancer
status:
  loadBalancer:
    ingress:
    - ip: 192.0.2.127
```

외부 로드 밸런서의 트래픽은 백엔드 파드로 전달된다. 클라우드 공급자는 로드 밸런싱 방식을 결정한다.

일부 클라우드 공급자는 `loadBalancerIP`를 지정할 수 있도록 허용한다. 이 경우, 로드 밸런서는
사용자 지정 `loadBalancerIP`로 생성된다. `loadBalancerIP` 필드가 지정되지 않으면,
임시 IP 주소로 loadBalancer가 설정된다. `loadBalancerIP`를 지정했지만
클라우드 공급자가 이 기능을 지원하지 않는 경우, 설정한 `loadbalancerIP` 필드는
무시된다.

{{< note >}}

**Azure** 에서 사용자 지정 공개(public) 유형 `loadBalancerIP`를 사용하려면, 먼저
정적 유형 공개 IP 주소 리소스를 생성해야 한다. 이 공개 IP 주소 리소스는
클러스터에서 자동으로 생성된 다른 리소스와 동일한 리소스 그룹에 있어야 한다.
예를 들면, `MC_myResourceGroup_myAKSCluster_eastus`이다.

할당된 IP 주소를 loadBalancerIP로 지정한다. 클라우드 공급자 구성 파일에서 securityGroupName을 업데이트했는지 확인한다. `CreatingLoadBalancerFailed` 권한 문제 해결에 대한 자세한 내용은 [Azure Kubernetes Service (AKS) 로드 밸런서에서 고정 IP 주소 사용](https://docs.microsoft.com/en-us/azure/aks/static-ip) 또는 [고급 네트워킹 AKS 클러스터에서 CreateLoadBalancerFailed](https://github.com/Azure/AKS/issues/357)를 참고한다.

{{< /note >}}

#### 프로토콜 유형이 혼합된 로드밸런서

{{< feature-state for_k8s_version="v1.20" state="alpha" >}}

기본적으로 로드밸런서 서비스 유형의 경우 둘 이상의 포트가 정의되어 있을 때 모든
포트는 동일한 프로토콜을 가져야 하며 프로토콜은 클라우드 공급자가
지원하는 프로토콜이어야 한다.

kube-apiserver에 대해 기능 게이트 `MixedProtocolLBService`가 활성화된 경우 둘 이상의 포트가 정의되어 있을 때 다른 프로토콜을 사용할 수 있다.

{{< note >}}

로드밸런서 서비스 유형에 사용할 수 있는 프로토콜 세트는 여전히 클라우드 제공 업체에서 정의한다.

{{< /note >}}

#### 로드밸런서 NodePort 할당 비활성화

{{< feature-state for_k8s_version="v1.20" state="alpha" >}}

v1.20부터는 `spec.allocateLoadBalancerNodePorts` 필드를 `false`로 설정하여 서비스 Type=LoadBalancer에
대한 노드 포트 할당을 선택적으로 비활성화 할 수 있다.
노드 포트를 사용하는 대신 트래픽을 파드로 직접 라우팅하는 로드 밸런서 구현에만 사용해야 한다.
기본적으로 `spec.allocateLoadBalancerNodePorts`는 `true`이며 로드밸런서 서비스 유형은 계속해서 노드 포트를 할당한다.
노드 포트가 할당된 기존 서비스에서 `spec.allocateLoadBalancerNodePorts`가 `false`로 설정된 경우 해당 노드 포트는 자동으로 할당 해제되지 않는다.
이러한 노드 포트를 할당 해제하려면 모든 서비스 포트에서 `nodePorts` 항목을 명시적으로 제거해야 한다.
이 필드를 사용하려면 `ServiceLBNodePortControl` 기능 게이트를 활성화해야 한다.

#### 로드 밸런서 구현 클래스 지정 {#load-balancer-class}

{{< feature-state for_k8s_version="v1.21" state="alpha" >}}

v1.21부터는, `spec.loadBalancerClass` 필드를 설정하여 `LoadBalancer` 서비스 유형에
대한 로드 밸런서 구현 클래스를 선택적으로 지정할 수 있다.
기본적으로, `spec.loadBalancerClass` 는 `nil` 이고 `LoadBalancer` 유형의 서비스는
클라우드 공급자의 기본 로드 밸런서 구현을 사용한다.
`spec.loadBalancerClass` 가 지정되면, 지정된 클래스와 일치하는 로드 밸런서
구현이 서비스를 감시하고 있다고 가정한다.
모든 기본 로드 밸런서 구현(예: 클라우드 공급자가 제공하는
로드 밸런서 구현)은 이 필드가 설정된 서비스를 무시한다.
`spec.loadBalancerClass` 는 `LoadBalancer` 유형의 서비스에서만 설정할 수 있다.
한 번 설정하면 변경할 수 없다.
`spec.loadBalancerClass` 의 값은 "`internal-vip`" 또는
"`example.com/internal-vip`" 와 같은 선택적 접두사가 있는 레이블 스타일 식별자여야 한다.
접두사가 없는 이름은 최종 사용자를 위해 예약되어 있다.
이 필드를 사용하려면 `ServiceLoadBalancerClass` 기능 게이트를 활성화해야 한다.

#### 내부 로드 밸런서

혼재된 환경에서는 서비스의 트래픽을 동일한 (가상) 네트워크 주소 블록 내로
라우팅해야 하는 경우가 있다.

수평 분할 DNS 환경에서는 외부와 내부 트래픽을 엔드포인트로 라우팅 할 수 있는 두 개의 서비스가 필요하다.

내부 로드 밸런서를 설정하려면, 사용 중인 클라우드 서비스 공급자에 따라
다음의 어노테이션 중 하나를 서비스에 추가한다.

{{< tabs name="service_tabs" >}}
{{% tab name="Default" %}}
탭 중 하나를 선택
{{% /tab %}}
{{% tab name="GCP" %}}

```yaml
[...]
metadata:
    name: my-service
    annotations:
        cloud.google.com/load-balancer-type: "Internal"
[...]
```

{{% /tab %}}
{{% tab name="AWS" %}}

```yaml
[...]
metadata:
    name: my-service
    annotations:
        service.beta.kubernetes.io/aws-load-balancer-internal: "true"
[...]
```

{{% /tab %}}
{{% tab name="Azure" %}}

```yaml
[...]
metadata:
    name: my-service
    annotations:
        service.beta.kubernetes.io/azure-load-balancer-internal: "true"
[...]
```

{{% /tab %}}
{{% tab name="IBM Cloud" %}}

```yaml
[...]
metadata:
    name: my-service
    annotations:
        service.kubernetes.io/ibm-load-balancer-cloud-provider-ip-type: "private"
[...]
```

{{% /tab %}}
{{% tab name="OpenStack" %}}

```yaml
[...]
metadata:
    name: my-service
    annotations:
        service.beta.kubernetes.io/openstack-internal-load-balancer: "true"
[...]
```

{{% /tab %}}
{{% tab name="Baidu Cloud" %}}

```yaml
[...]
metadata:
    name: my-service
    annotations:
        service.beta.kubernetes.io/cce-load-balancer-internal-vpc: "true"
[...]
```

{{% /tab %}}
{{% tab name="Tencent Cloud" %}}

```yaml
[...]
metadata:
  annotations:
    service.kubernetes.io/qcloud-loadbalancer-internal-subnetid: subnet-xxxxx
[...]
```

{{% /tab %}}
{{% tab name="Alibaba Cloud" %}}

```yaml
[...]
metadata:
  annotations:
    service.beta.kubernetes.io/alibaba-cloud-loadbalancer-address-type: "intranet"
[...]
```

{{% /tab %}}
{{< /tabs >}}

#### AWS에서 TLS 지원 {#ssl-support-on-aws}

AWS에서 실행되는 클러스터에서 부분적으로 TLS / SSL을 지원하기 위해, `LoadBalancer` 서비스에 세 가지
어노테이션을 추가할 수 있다.

```yaml
metadata:
  name: my-service
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-ssl-cert: arn:aws:acm:us-east-1:123456789012:certificate/12345678-1234-1234-1234-123456789012
```

첫 번째는 사용할 인증서의 ARN을 지정한다. IAM에 업로드된
써드파티 발급자의 인증서이거나 AWS Certificate Manager에서
생성된 인증서일 수 있다.

```yaml
metadata:
  name: my-service
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-backend-protocol: (https|http|ssl|tcp)
```

두 번째 어노테이션은 파드가 알려주는 프로토콜을 지정한다. HTTPS와
SSL의 경우, ELB는 인증서를 사용하여 암호화된 연결을 통해 파드가 스스로를
인증할 것으로 예상한다.

HTTP와 HTTPS는 7 계층 프록시를 선택한다. ELB는 요청을 전달할 때
사용자와의 연결을 종료하고, 헤더를 파싱하고 사용자의 IP 주소로 `X-Forwarded-For`
헤더를 삽입한다. (파드는 해당 연결의 다른 종단에서의
ELB의 IP 주소만 참조)

TCP 및 SSL은 4 계층 프록시를 선택한다. ELB는 헤더를 수정하지 않고
트래픽을 전달한다.

일부 포트는 보안성을 갖추고 다른 포트는 암호화되지 않은 혼재된 사용 환경에서는
다음 어노테이션을 사용할 수 있다.

```yaml
    metadata:
      name: my-service
      annotations:
        service.beta.kubernetes.io/aws-load-balancer-backend-protocol: http
        service.beta.kubernetes.io/aws-load-balancer-ssl-ports: "443,8443"
```

위의 예에서, 서비스에 `80`, `443`, `8443`의 3개 포트가 포함된 경우,
`443`, `8443`은 SSL 인증서를 사용하지만, `80`은 프록시하는 HTTP이다.

쿠버네티스 v1.9부터는 서비스에 대한 HTTPS 또는 SSL 리스너와 함께 [사전에 정의된 AWS SSL 정책](https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/elb-security-policy-table.html)을 사용할 수 있다.
사용 가능한 정책을 확인하려면, `aws` 커맨드라인 툴을 사용한다.

```bash
aws elb describe-load-balancer-policies --query 'PolicyDescriptions[].PolicyName'
```

그리고
"`service.beta.kubernetes.io/aws-load-balancer-ssl-negotiation-policy`"
어노테이션을 사용하여 이러한 정책 중 하나를 지정할 수 있다. 예를 들면

```yaml
    metadata:
      name: my-service
      annotations:
        service.beta.kubernetes.io/aws-load-balancer-ssl-negotiation-policy: "ELBSecurityPolicy-TLS-1-2-2017-01"
```

#### AWS에서 지원하는 프록시 프로토콜

AWS에서 실행되는 클러스터에 대한 [프록시 프로토콜](https://www.haproxy.org/download/1.8/doc/proxy-protocol.txt)
지원을 활성화하려면, 다음의 서비스 어노테이션을
사용할 수 있다.

```yaml
    metadata:
      name: my-service
      annotations:
        service.beta.kubernetes.io/aws-load-balancer-proxy-protocol: "*"
```

버전 1.3.0 부터, 이 어노테이션의 사용은 ELB에 의해 프록시되는 모든 포트에 적용되며
다르게 구성할 수 없다.

#### AWS의 ELB 접근 로그

AWS ELB 서비스의 접근 로그를 관리하기 위한 몇 가지 어노테이션이 있다.

`service.beta.kubernetes.io/aws-load-balancer-access-log-enabled` 어노테이션은
접근 로그의 활성화 여부를 제어한다.

`service.beta.kubernetes.io/aws-load-balancer-access-log-emit-interval` 어노테이션은
접근 로그를 게시하는 간격을 분 단위로 제어한다. 5분 또는 60분의
간격으로 지정할 수 있다.

`service.beta.kubernetes.io/aws-load-balancer-access-log-s3-bucket-name` 어노테이션은
로드 밸런서 접근 로그가 저장되는 Amazon S3 버킷의 이름을
제어한다.

`service.beta.kubernetes.io/aws-load-balancer-access-log-s3-bucket-prefix` 어노테이션은
Amazon S3 버킷을 생성한 논리적 계층을 지정한다.

```yaml
    metadata:
      name: my-service
      annotations:
        service.beta.kubernetes.io/aws-load-balancer-access-log-enabled: "true"
        # 로드 밸런서의 접근 로그 활성화 여부를 명시.
        service.beta.kubernetes.io/aws-load-balancer-access-log-emit-interval: "60"
        # 접근 로그를 게시하는 간격을 분 단위로 제어. 5분 또는 60분의 간격을 지정.
        service.beta.kubernetes.io/aws-load-balancer-access-log-s3-bucket-name: "my-bucket"
        # 로드 밸런서 접근 로그가 저장되는 Amazon S3 버킷의 이름 명시.
        service.beta.kubernetes.io/aws-load-balancer-access-log-s3-bucket-prefix: "my-bucket-prefix/prod"
        # Amazon S3 버킷을 생성한 논리적 계층을 지정. 예: `my-bucket-prefix/prod`
```

#### AWS의 연결 드레이닝(Draining)

Classic ELB의 연결 드레이닝은
`service.beta.kubernetes.io/aws-load-balancer-connection-draining-enabled` 어노테이션을
`"true"`값으로 설정하여 관리할 수 ​​있다. `service.beta.kubernetes.io/aws-load-balancer-connection-draining-timeout` 어노테이션을
사용하여 인스턴스를 해제하기 전에,
기존 연결을 열어 두는 목적으로 최대 시간을 초 단위로 설정할 수도 있다.

```yaml
    metadata:
      name: my-service
      annotations:
        service.beta.kubernetes.io/aws-load-balancer-connection-draining-enabled: "true"
        service.beta.kubernetes.io/aws-load-balancer-connection-draining-timeout: "60"
```

#### 다른 ELB 어노테이션

이하는 클래식 엘라스틱 로드 밸런서(Classic Elastic Load Balancers)를 관리하기 위한 다른 어노테이션이다.

```yaml
    metadata:
      name: my-service
      annotations:
        service.beta.kubernetes.io/aws-load-balancer-connection-idle-timeout: "60"
        # 로드 밸런서가 연결을 닫기 전에, 유휴 상태(연결을 통해 전송 된 데이터가 없음)의 연결을 허용하는 초단위 시간

        service.beta.kubernetes.io/aws-load-balancer-cross-zone-load-balancing-enabled: "true"
        # 로드 밸런서에 교차-영역(cross-zone) 로드 밸런싱을 사용할 지 여부를 지정

        service.beta.kubernetes.io/aws-load-balancer-additional-resource-tags: "environment=prod,owner=devops"
        # 쉼표로 구분된 key-value 목록은 ELB에
        # 추가 태그로 기록됨

        service.beta.kubernetes.io/aws-load-balancer-healthcheck-healthy-threshold: ""
        # 백엔드가 정상인 것으로 간주되는데 필요한 연속적인
        # 헬스 체크 성공 횟수이다. 기본값은 2이며, 2와 10 사이여야 한다.

        service.beta.kubernetes.io/aws-load-balancer-healthcheck-unhealthy-threshold: "3"
        # 백엔드가 비정상인 것으로 간주되는데 필요한
        # 헬스 체크 실패 횟수이다. 기본값은 6이며, 2와 10 사이여야 한다.

        service.beta.kubernetes.io/aws-load-balancer-healthcheck-interval: "20"
        # 개별 인스턴스의 상태 점검 사이의
        # 대략적인 간격 (초 단위). 기본값은 10이며, 5와 300 사이여야 한다.

        service.beta.kubernetes.io/aws-load-balancer-healthcheck-timeout: "5"
        # 헬스 체크 실패를 의미하는 무 응답의 총 시간 (초 단위)
        # 이 값은 service.beta.kubernetes.io/aws-load-balancer-healthcheck-interval
        # 값 보다 작아야한다. 기본값은 5이며, 2와 60 사이여야 한다.

        service.beta.kubernetes.io/aws-load-balancer-security-groups: "sg-53fae93f"
        # 생성된 ELB에 설정할 기존 보안 그룹(security group) 목록.
        # service.beta.kubernetes.io/aws-load-balancer-extra-security-groups 어노테이션과 달리, 이는 이전에 ELB에 할당된 다른 모든 보안 그룹을 대체하며,
        # '해당 ELB를 위한 고유 보안 그룹 생성'을 오버라이드한다.
        # 목록의 첫 번째 보안 그룹 ID는 인바운드 트래픽(서비스 트래픽과 헬스 체크)이 워커 노드로 향하도록 하는 규칙으로 사용된다.
        # 여러 ELB가 하나의 보안 그룹 ID와 연결되면, 1줄의 허가 규칙만이 워커 노드 보안 그룹에 추가된다.
        # 즉, 만약 여러 ELB 중 하나를 지우면, 1줄의 허가 규칙이 삭제되어, 같은 보안 그룹 ID와 연결된 모든 ELB에 대한 접속이 막힌다.
        # 적절하게 사용되지 않으면 이는 다수의 서비스가 중단되는 상황을 유발할 수 있다.

        service.beta.kubernetes.io/aws-load-balancer-extra-security-groups: "sg-53fae93f,sg-42efd82e"
        # 생성된 ELB에 추가할 추가 보안 그룹 목록
        # 이 방법을 사용하면 이전에 생성된 고유 보안 그룹이 그대로 유지되므로, 각 ELB가 고유 보안 그룹 ID와 그에 매칭되는 허가 규칙 라인을 소유하여
        # 트래픽(서비스 트래픽과 헬스 체크)이 워커 노드로 향할 수 있도록 한다. 여기에 기재되는 보안 그룹은 여러 서비스 간 공유될 수 있다.

        service.beta.kubernetes.io/aws-load-balancer-target-node-labels: "ingress-gw,gw-name=public-api"
        # 로드 밸런서의 대상 노드를 선택하는 데
        # 사용되는 키-값 쌍의 쉼표로 구분된 목록
```

#### AWS의 네트워크 로드 밸런서 지원 {#aws-nlb-support}

{{< feature-state for_k8s_version="v1.15" state="beta" >}}

AWS에서 네트워크 로드 밸런서를 사용하려면, `nlb` 값이 설정된 `service.beta.kubernetes.io/aws-load-balancer-type` 어노테이션을 사용한다.

```yaml
    metadata:
      name: my-service
      annotations:
        service.beta.kubernetes.io/aws-load-balancer-type: "nlb"
```

{{< note >}}
NLB는 특정 인스턴스 클래스에서만 작동한다. 지원되는 인스턴스 유형 목록은 엘라스틱 로드 밸런싱에 대한 [AWS 문서](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/target-group-register-targets.html#register-deregister-targets)
를 참고한다.
{{< /note >}}

클래식 엘라스틱 로드 밸런서와 달리, 네트워크 로드 밸런서 (NLB)는
클라이언트의 IP 주소를 노드로 전달한다. 서비스의 `.spec.externalTrafficPolicy`가
`Cluster`로 설정되어 있으면, 클라이언트의 IP 주소가 종단 파드로
전파되지 않는다.

`.spec.externalTrafficPolicy`를 `Local`로 설정하면, 클라이언트 IP 주소가
종단 파드로 전파되지만, 트래픽이 고르지 않게
분배될 수 있다. 특정 로드밸런서 서비스를 위한 파드가 없는 노드는 자동 할당된
`.spec.healthCheckNodePort`에 의해서 NLB 대상 그룹의
헬스 체크에 실패하고 트래픽을 수신하지 못하게 된다.

트래픽을 균일하게 하려면, DaemonSet을 사용하거나,
[파드 안티어피니티(pod anti-affinity)](/ko/docs/concepts/scheduling-eviction/assign-pod-node/#어피니티-affinity-와-안티-어피니티-anti-affinity)
를 지정하여 동일한 노드에 위치하지 않도록 한다.

[내부 로드 밸런서](/ko/docs/concepts/services-networking/service/#internal-load-balancer) 어노테이션과 함께 NLB 서비스를
사용할 수도 있다.

클라이언트 트래픽이 NLB 뒤의 인스턴스에 도달하기 위해, 노드 보안
그룹은 다음 IP 규칙으로 수정된다.

| 규칙 | 프로토콜 | 포트 | IP 범위 | IP 범위 설명 |
|------|----------|---------|------------|---------------------|
| 헬스 체크 | TCP | NodePort(s) (`.spec.healthCheckNodePort` for `.spec.externalTrafficPolicy = Local`) | Subnet CIDR | kubernetes.io/rule/nlb/health=\<loadBalancerName\> |
| 클라이언트 트래픽 | TCP | NodePort(s) | `.spec.loadBalancerSourceRanges` (defaults to `0.0.0.0/0`) | kubernetes.io/rule/nlb/client=\<loadBalancerName\> |
| MTU 탐색 | ICMP | 3,4 | `.spec.loadBalancerSourceRanges` (defaults to `0.0.0.0/0`) | kubernetes.io/rule/nlb/mtu=\<loadBalancerName\> |

네트워크 로드 밸런서에 접근할 수 있는 클라이언트 IP를 제한하려면,
`loadBalancerSourceRanges`를 지정한다.

```yaml
spec:
  loadBalancerSourceRanges:
    - "143.231.0.0/16"
```

{{< note >}}
`.spec.loadBalancerSourceRanges`가 설정되어 있지 않으면, 쿠버네티스는
`0.0.0.0/0`에서 노드 보안 그룹으로의 트래픽을 허용한다. 노드에 퍼블릭 IP 주소가
있는 경우, 비(non)-NLB 트래픽도 해당 수정된 보안 그룹의
모든 인스턴스에 도달할 수 있다.

{{< /note >}}

#### Tencent Kubernetes Engine (TKE)의 다른 CLB 어노테이션

아래 표시된 것처럼 TKE에서 클라우드 로드 밸런서를 관리하기 위한 다른 어노테이션이 있다.

```yaml
    metadata:
      name: my-service
      annotations:
        # 지정된 노드로 로드 밸런서 바인드
        service.kubernetes.io/qcloud-loadbalancer-backends-label: key in (value1, value2)

        # 기존 로드 밸런서의 ID
        service.kubernetes.io/tke-existed-lbid：lb-6swtxxxx

        # 로드 밸런서 (LB)에 대한 사용자 지정 매개 변수는 아직 LB 유형 수정을 지원하지 않음
        service.kubernetes.io/service.extensiveParameters: ""

        # LB 리스너의 사용자 정의 매개 변수
        service.kubernetes.io/service.listenerParameters: ""

        # 로드 밸런서 유형 지정
        # 유효 값 : 클래식 (클래식 클라우드 로드 밸런서) 또는 애플리케이션 (애플리케이션 클라우드 로드 밸런서)
        service.kubernetes.io/loadbalance-type: xxxxx

        # 퍼블릭 네트워크 대역폭 청구 방법 지정
        # 유효 값: TRAFFIC_POSTPAID_BY_HOUR (트래픽 별) 및 BANDWIDTH_POSTPAID_BY_HOUR (대역폭 별)
        service.kubernetes.io/qcloud-loadbalancer-internet-charge-type: xxxxxx

        # 대역폭 값 지정 (값 범위 : [1,2000] Mbps).
        service.kubernetes.io/qcloud-loadbalancer-internet-max-bandwidth-out: "10"

        # 이 어느테이션이 설정되면, 로드 밸런서는 파드가
        # 실행중인 노드만 등록하고, 그렇지 않으면 모든 노드가 등록됨
        service.kubernetes.io/local-svc-only-bind-node-with-pod: true
```

### ExternalName 유형 {#externalname}

ExternalName 유형의 서비스는 `my-service` 또는 `cassandra`와 같은 일반적인 셀렉터에 대한 서비스가 아닌,
DNS 이름에 대한 서비스에 매핑한다. `spec.externalName` 파라미터를 사용하여 이러한 서비스를 지정한다.

예를 들면, 이 서비스 정의는 `prod` 네임 스페이스의
`my-service` 서비스를 `my.database.example.com`에 매핑한다.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
  namespace: prod
spec:
  type: ExternalName
  externalName: my.database.example.com
```

{{< note >}}
ExternalName은 IPv4 주소 문자열을 허용하지만, IP 주소가 아닌 숫자로 구성된 DNS 이름을 허용한다. IPv4 주소와 유사한 ExternalName은 CoreDNS 또는 ingress-nginx에 의해 확인되지 않는데, ExternalName은
정식(canonical) DNS 이름을 지정하기 때문이다. IP 주소를 하드 코딩하려면,
[헤드리스(headless) 서비스](#헤드리스-headless-서비스) 사용을 고려한다.
{{< /note >}}

`my-service.prod.svc.cluster.local` 호스트를 검색하면, 클러스터 DNS 서비스는
`my.database.example.com` 값의 `CNAME` 레코드를 반환한다. `my-service`에 접근하는 것은
다른 서비스와 같은 방식으로 작동하지만, 리다이렉션은 프록시 또는
포워딩을 통하지 않고 DNS 수준에서 발생한다는 중요한
차이점이 있다. 나중에 데이터베이스를 클러스터로 이동하기로 결정한 경우, 해당
파드를 시작하고 적절한 셀렉터 또는 엔드포인트를 추가하고,
서비스의 `유형(type)`을 변경할 수 있다.

{{< warning >}}
HTTP 및 HTTPS를 포함한, 몇몇 일반적인 프로토콜에 ExternalName을 사용하는 것은 문제가 있을 수 있다. ExternalName을 사용하는 경우, 클러스터 내부의 클라이언트가 사용하는 호스트 이름(hostname)이 ExternalName이 참조하는 이름과 다르다.

호스트 이름을 사용하는 프로토콜의 경우, 이러한 차이로 인해 오류가 발생하거나 예기치 않은 응답이 발생할 수 있다. HTTP 요청에는 오리진(origin) 서버가 인식하지 못하는 `Host :` 헤더가 있다. TLS 서버는 클라이언트가 연결된 호스트 이름과 일치하는 인증서를 제공할 수 없다.
{{< /warning >}}

{{< note >}}
이 섹션은 [Alen Komljen](https://akomljen.com/)의 [쿠버네티스 팁 - Part
1](https://akomljen.com/kubernetes-tips-part-1/) 블로그 게시물에 대한 내용이다.
{{< /note >}}

### 외부 IP

하나 이상의 클러스터 노드로 라우팅되는 외부 IP가 있는 경우, 쿠버네티스 서비스는 이러한
`externalIPs`에 노출될 수 있다. 서비스 포트에서 외부 IP (목적지 IP)를 사용하여 클러스터로 들어오는 트래픽은
서비스 엔드포인트 중 하나로 라우팅된다. `externalIPs`는 쿠버네티스에 의해 관리되지 않으며
클러스터 관리자에게 책임이 있다.

서비스 명세에서, `externalIPs`는 모든 `ServiceTypes`와 함께 지정할 수 있다.
아래 예에서, 클라이언트는 "`80.11.12.10:80`"(`외부 IP:포트`)로 "`my-service`"에 접근할 수 있다.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  selector:
    app: MyApp
  ports:
    - name: http
      protocol: TCP
      port: 80
      targetPort: 9376
  externalIPs:
    - 80.11.12.10
```

## 단점

VIP용 유저스페이스 프록시를 사용하면 중소 규모의 스케일에서는 동작하지만, 수천 개의
서비스가 포함된 대규모 클러스터로는 확장되지 않는다.
[포털에 대한 독창적인 설계 제안](https://github.com/kubernetes/kubernetes/issues/1107)에 이에 대한 자세한 내용이
있다.

유저스페이스 프록시를 사용하면 서비스에 접근하는 패킷의 소스 IP 주소가
가려진다.
이것은 일종의 네트워크 필터링 (방화벽)을 불가능하게 만든다. iptables
프록시 모드는 클러스터 내
소스 IP를 가리지 않지만, 여전히 로드 밸런서 또는 노드-포트를 통해 오는
클라이언트에 영향을 미친다.

`Type` 필드는 중첩된 기능으로 설계되었다. - 각 레벨은 이전 레벨에
추가된다. 이는 모든 클라우드 공급자에 반드시 필요한 것은 아니지만, (예: Google Compute Engine는
`LoadBalancer`를 작동시키기 위해 `NodePort`를 할당할 필요는 없지만, AWS는 필요하다)
현재 API에는 필요하다.

## 가상 IP 구현 {#the-gory-details-of-virtual-ips}

서비스를 사용하려는 많은 사람들에게 이전 정보가
충분해야 한다. 그러나, 이해가 필요한 부분 뒤에는
많은 일이 있다.

### 충돌 방지

쿠버네티스의 주요 철학 중 하나는 잘못한 것이
없는 경우 실패할 수 있는 상황에 노출되어서는
안된다는 것이다. 서비스 리소스 설계 시, 다른 사람의 포트 선택과
충돌할 경우에 대비해 자신의 포트 번호를 선택하지
않아도 된다. 그것은 격리 실패이다.

서비스에 대한 포트 번호를 선택할 수 있도록 하기 위해, 두 개의
서비스가 충돌하지 않도록 해야 한다. 쿠버네티스는 각 서비스에 고유한 IP 주소를
할당하여 이를 수행한다.

각 서비스가 고유한 IP를 받도록 하기 위해, 내부 할당기는
각 서비스를 만들기 전에 {{< glossary_tooltip term_id="etcd" >}}에서
글로벌 할당 맵을 원자적으로(atomically) 업데이트한다. 서비스가 IP 주소 할당을 가져오려면
레지스트리에 맵 오브젝트가 있어야 하는데, 그렇지 않으면
IP 주소를 할당할 수 없다는 메시지와 함께 생성에 실패한다.

컨트롤 플레인에서, 백그라운드 컨트롤러는 해당 맵을
생성해야 한다. (인-메모리 잠금을 사용하는 이전 버전의 쿠버네티스에서 마이그레이션
지원 필요함) 쿠버네티스는 또한 컨트롤러를 사용하여 유효하지 않은
할당 (예: 관리자 개입으로)을 체크하고 더 이상 서비스에서 사용하지 않는 할당된
IP 주소를 정리한다.

### 서비스 IP 주소 {#ips-and-vips}

실제로 고정된 목적지로 라우팅되는 파드 IP 주소와 달리,
서비스 IP는 실제로 단일 호스트에서 응답하지 않는다. 대신에, kube-proxy는
iptables (리눅스의 패킷 처리 로직)를 필요에 따라
명백하게 리다이렉션되는 _가상_ IP 주소를 정의하기 위해 사용한다. 클라이언트가 VIP에
연결하면, 트래픽이 자동으로 적절한 엔드포인트로 전송된다.
환경 변수와 서비스 용 DNS는 실제로 서비스의
가상 IP 주소 (및 포트)로 채워진다.

kube-proxy는 조금씩 다르게 작동하는 세 가지 프록시 모드&mdash;유저스페이스, iptables and IPVS&mdash;를
지원한다.

#### 유저스페이스 (Userspace)

예를 들어, 위에서 설명한 이미지 처리 애플리케이션을 고려한다.
백엔드 서비스가 생성되면, 쿠버네티스 마스터는 가상
IP 주소(예 : 10.0.0.1)를 할당한다. 서비스 포트를 1234라고 가정하면, 서비스는
클러스터의 모든 kube-proxy 인스턴스에서 관찰된다.
프록시가 새 서비스를 발견하면, 새로운 임의의 포트를 열고, 가상 IP 주소에서
이 새로운 포트로 iptables 리다이렉션을 설정한 후,
연결을 수락하기 시작한다.

클라이언트가 서비스의 가상 IP 주소에 연결하면, iptables
규칙이 시작되고, 패킷을 프록시의 자체 포트로 리다이렉션한다.
"서비스 프록시"는 백엔드를 선택하고, 클라이언트에서 백엔드로의 트래픽을 프록시하기 시작한다.

이는 서비스 소유자가 충돌 위험 없이 원하는 어떤 포트든 선택할 수 있음을
의미한다. 클라이언트는 실제로 접근하는 파드를 몰라도, IP와 포트에
연결할 수 있다.

#### iptables

다시 한번, 위에서 설명한 이미지 처리 애플리케이션을 고려한다.
백엔드 서비스가 생성되면, 쿠버네티스 컨트롤 플레인은 가상
IP 주소(예 : 10.0.0.1)를 할당한다. 서비스 포트를 1234라고 가정하면, 서비스는
클러스터의 모든 kube-proxy 인스턴스에서 관찰된다.
프록시가 새로운 서비스를 발견하면, 가상 IP 주소에서 서비스-별 규칙으로
리다이렉션되는 일련의 iptables 규칙을 설치한다. 서비스-별
규칙은 트래픽을 (목적지 NAT를 사용하여) 백엔드로 리다이렉션하는 엔드포인트-별 규칙에
연결한다.

클라이언트가 서비스의 가상 IP 주소에 연결하면 iptables 규칙이 시작한다.
(세션 어피니티(Affinity)에 따라 또는 무작위로) 백엔드가 선택되고 패킷이
백엔드로 리다이렉션된다. 유저스페이스 프록시와 달리, 패킷은 유저스페이스로
복사되지 않으며, 가상 IP 주소가 작동하기 위해 kube-proxy가
실행 중일 필요는 없으며, 노드는 변경되지 않은 클라이언트 IP 주소에서 오는
트래픽을 본다.

트래픽이 노드-포트 또는 로드 밸런서를 통해 들어오는 경우에도,
이와 동일한 기본 흐름이 실행되지만, 클라이언트 IP는 변경된다.

#### IPVS

iptables 작업은 대규모 클러스터 (예: 10,000 서비스)에서 크게 느려진다.
IPVS는 로드 밸런싱을 위해 설계되었고 커널-내부 해시 테이블을 기반으로 한다. 따라서 IPVS 기반 kube-proxy로부터 많은 개수의 서비스에서 일관성 있는 성능을 가질 수 있다. 한편, IPVS 기반 kube-proxy는 보다 정교한 로드 밸런싱 알고리즘 (least conns, locality, weighted, persistence)을 가진다.

## API 오브젝트

서비스는 쿠버네티스 REST API의 최상위 리소스이다. API 오브젝트에 대한
자세한 내용은 다음을 참고한다. [서비스 API 오브젝트](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#service-v1-core)

## 지원되는 프로토콜 {#protocol-support}

### TCP

모든 종류의 서비스에 TCP를 사용할 수 있으며, 이는 기본 네트워크 프로토콜이다.

### UDP

대부분의 서비스에 UDP를 사용할 수 있다. type=LoadBalancer 서비스의 경우, UDP 지원은
이 기능을 제공하는 클라우드 공급자에 따라 다르다.

### SCTP

{{< feature-state for_k8s_version="v1.20" state="stable" >}}

SCTP 트래픽을 지원하는 네트워크 플러그인을 사용하는 경우 대부분의 서비스에 SCTP를 사용할 수 있다.
type=LoadBalancer 서비스의 경우 SCTP 지원은 이 기능을 제공하는
클라우드 공급자에 따라 다르다. (대부분 그렇지 않음)

#### 경고 {#caveat-sctp-overview}

##### 멀티홈드(multihomed) SCTP 연결을 위한 지원 {#caveat-sctp-multihomed}

{{< warning >}}
멀티홈 SCTP 연결을 위해서는 먼저 CNI 플러그인이 파드에 대해 멀티 인터페이스 및 IP 주소 할당이 지원되어야 한다.

멀티홈 SCTP 연결을 위한 NAT는 해당 커널 모듈 내에 특수한 로직을 필요로 한다.
{{< /warning >}}

##### 윈도우 {#caveat-sctp-windows-os}

{{< warning >}}
SCTP는 윈도우 기반 노드를 지원하지 않는다.
{{< /warning >}}

##### 유저스페이스 kube-proxy {#caveat-sctp-kube-proxy-userspace}

{{< warning >}}
kube-proxy는 유저스페이스 모드에 있을 때 SCTP 연결 관리를 지원하지 않는다.
{{< /warning >}}

### HTTP

클라우드 공급자가 이를 지원하는 경우, LoadBalancer 모드의
서비스를 사용하여 서비스의 엔드포인트로 전달하는 외부 HTTP / HTTPS 리버스 프록시를
설정할 수 있다.

{{< note >}}
서비스 대신 {{< glossary_tooltip term_id="ingress" text="인그레스" >}} 를 사용하여
HTTP/HTTPS 서비스를 노출할 수도 있다.
{{< /note >}}

### PROXY 프로토콜

클라우드 공급자가 지원하는 경우에,
LoadBalancer 모드의 서비스를 사용하여 쿠버네티스 자체 외부에
로드 밸런서를 구성할 수 있으며, 이때 접두사가
[PROXY 프로토콜](https://www.haproxy.org/download/1.8/doc/proxy-protocol.txt) 인 연결을 전달하게 된다.

로드 밸런서는 들어오는 연결을 설명하는 초기 일련의
옥텟(octets)을 전송하며, 이 예와 유사하게

```
PROXY TCP4 192.0.2.202 10.0.42.7 12345 7\r\n
```

클라이언트 데이터가 뒤따라온다.

## {{% heading "whatsnext" %}}

* [서비스와 애플리케이션 연결](/ko/docs/concepts/services-networking/connect-applications-service/) 알아보기
* [인그레스](/ko/docs/concepts/services-networking/ingress/)에 대해 알아보기
* [엔드포인트슬라이스](/ko/docs/concepts/services-networking/endpoint-slices/)에 대해 알아보기
