---




title: 노드에 파드 할당하기
content_type: concept
weight: 20
---


<!-- overview -->

특정한 {{< glossary_tooltip text="노드(들)" term_id="node" >}} 집합에서만 동작하도록
{{< glossary_tooltip text="파드" term_id="pod" >}}를 제한할 수 있다.
이를 수행하는 방법에는 여러 가지가 있으며 권장되는 접근 방식은 모두
[레이블 셀렉터](/ko/docs/concepts/overview/working-with-objects/labels/)를 사용하여 선택을 용이하게 한다.
보통 스케줄러가 자동으로 합리적인 배치(예: 자원이 부족한 노드에 파드를 배치하지 않도록
노드 간에 파드를 분배하는 등)를 수행하기에 이러한 제약 조건은 필요하지 않지만
간혹 파드가 배포할 노드를 제어해야 하는 경우가 있다.
예를 들어 SSD가 장착된 머신에 파드가 연결되도록 하거나 또는 동일한 가용성 영역(availability zone)에서
많은 것을 통신하는 두 개의 서로 다른 서비스의 파드를 같이 배치할 수 있다.


<!-- body -->

## 노드 셀렉터(nodeSelector)

`nodeSelector` 는 가장 간단하고 권장되는 노드 선택 제약 조건의 형태이다.
`nodeSelector` 는 PodSpec의 필드이다. 이는 키-값 쌍의 매핑으로 지정한다. 파드가 노드에서 동작할 수 있으려면,
노드는 키-값의 쌍으로 표시되는 레이블을 각자 가지고 있어야 한다(이는 추가 레이블을 가지고 있을 수 있다).
일반적으로 하나의 키-값 쌍이 사용된다.

`nodeSelector` 를 어떻게 사용하는지 예시를 통해 알아보도록 하자.

### 0 단계: 사전 준비

이 예시는 쿠버네티스 파드에 대한 기본적인 이해를 하고 있고 [쿠버네티스 클러스터가 설정](/ko/docs/setup/)되어 있다고 가정한다.

### 1 단계: 노드에 레이블 붙이기

`kubectl get nodes` 를 실행해서 클러스터 노드 이름을 가져온다. 이 중에 레이블을 추가하기 원하는 것 하나를 선택한 다음에 `kubectl label nodes <노드 이름> <레이블 키>=<레이블 값>` 을 실행해서 선택한 노드에 레이블을 추가한다. 예를 들어 노드의 이름이 'kubernetes-foo-node-1.c.a-robinson.internal' 이고, 원하는 레이블이 'disktype=ssd' 라면, `kubectl label nodes kubernetes-foo-node-1.c.a-robinson.internal disktype=ssd` 를 실행한다.

`kubectl get nodes --show-labels` 를 다시 실행해서 노드가 현재 가진 레이블을 확인하여, 이 작업을 검증할 수 있다. 또한 `kubectl describe node "노드 이름"` 을 사용해서 노드에 주어진 레이블의 전체 목록을 확인할 수 있다.

### 2 단계: 파드 설정에 nodeSelector 필드 추가하기

실행하고자 하는 파드의 설정 파일을 가져오고, 이처럼 nodeSelector 섹션을 추가한다. 예를 들어 이것이 파드 설정이라면,

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
  labels:
    env: test
spec:
  containers:
  - name: nginx
    image: nginx
```

이 다음에 nodeSelector 를 다음과 같이 추가한다.

{{< codenew file="pods/pod-nginx.yaml" >}}

그런 다음에 `kubectl apply -f https://k8s.io/examples/pods/pod-nginx.yaml` 을
실행하면, 레이블이 붙여진 노드에 파드가 스케줄된다.
`kubectl get pods -o wide` 를 실행해서 파드가 할당된
"NODE" 를 보면 작동하는지 검증할 수 있다.

## 넘어가기 전에: 내장 노드 레이블들 {#built-in-node-labels}

[붙인](#1-단계-노드에-레이블-붙이기) 레이블뿐만 아니라, 노드에는
표준 레이블 셋이 미리 채워져 있다. 이들 목록은 [잘 알려진 레이블, 어노테이션 및 테인트](/docs/reference/labels-annotations-taints/)를 참고한다.

{{< note >}}
이 레이블들의 값은 클라우드 공급자에 따라 다르고 신뢰성이 보장되지 않는다.
예를 들어 `kubernetes.io/hostname` 은 어떤 환경에서는 노드 이름과 같지만,
다른 환경에서는 다른 값일 수 있다.
{{< /note >}}

## 노드 격리(isolation)/제한(restriction)

노드 오브젝트에 레이블을 추가하면 파드가 특정 노드 또는 노드 그룹을 목표 대상으로 할 수 있게 된다.
이는 특정 파드가 어떤 격리, 보안, 또는 규제 속성이 있는 노드에서만 실행되도록 사용할 수 있다.
이 목적으로 레이블을 사용하는 경우, 노드에서 kubelet 프로세스로 수정할 수 없는 레이블 키를 선택하는 것을 권장한다.
이렇게 하면 손상된 노드가 해당 kubelet 자격 증명을 사용해서 해당 레이블을 자체 노드 오브젝트에 설정하고,
스케줄러가 손상된 노드로 워크로드를 스케줄 하는 것을 방지할 수 있다.

`NodeRestriction` 어드미션 플러그인은 kubelet이 `node-restriction.kubernetes.io/` 접두사로 레이블을 설정 또는 수정하지 못하게 한다.
노드 격리에 해당 레이블 접두사를 사용하려면 다음과 같이 한다.

1. [노드 권한부여자](/docs/reference/access-authn-authz/node/)를 사용하고 있고, [NodeRestriction 어드미션 플러그인](/docs/reference/access-authn-authz/admission-controllers/#noderestriction)을 _활성화_ 해야 한다.
2. 노드 오브젝트의 `node-restriction.kubernetes.io/` 접두사 아래에 레이블을 추가하고, 해당 레이블을 노드 셀렉터에서 사용한다.
예를 들어, `example.com.node-restriction.kubernetes.io/fips=true` 또는 `example.com.node-restriction.kubernetes.io/pci-dss=true` 이다.

## 어피니티(affinity)와 안티-어피니티(anti-affinity)

`nodeSelector` 는 파드를 특정 레이블이 있는 노드로 제한하는 매우 간단한 방법을 제공한다.
어피니티/안티-어피니티 기능은 표현할 수 있는 제약 종류를 크게 확장한다. 주요 개선 사항은 다음과 같다.

1. 어피니티/안티-어피니티 언어가 더 표현적이다. 언어는 논리 연산자인 AND 연산으로 작성된
   정확한 매칭 항목 이외에 더 많은 매칭 규칙을 제공한다.
2. 규칙이 엄격한 요구 사항이 아니라 "유연한(soft)"/"선호(preference)" 규칙을 나타낼 수 있기에 스케줄러가 규칙을 만족할 수 없더라도,
   파드가 계속 스케줄되도록 한다.
3. 노드 자체에 레이블을 붙이기보다는 노드(또는 다른 토폴로지 도메인)에서 실행 중인 다른 파드의 레이블을 제한할 수 있다.
   이를 통해 어떤 파드가 함께 위치할 수 있는지와 없는지에 대한 규칙을 적용할 수 있다.

어피니티 기능은 "노드 어피니티" 와 "파드 간 어피니티/안티-어피니티" 두 종류의 어피니티로 구성된다.
노드 어피니티는 기존 `nodeSelector` 와 비슷하지만(그러나 위에서 나열된 첫째와 두 번째 이점이 있다.),
파드 간 어피니티/안티-어피니티는 위에서 나열된 세번째 항목에 설명된 대로
노드 레이블이 아닌 파드 레이블에 대해 제한되고 위에서 나열된 첫 번째와 두 번째 속성을 가진다.

### 노드 어피니티

노드 어피니티는 개념적으로 `nodeSelector` 와 비슷하다 -- 이는 노드의 레이블을 기반으로 파드를
스케줄할 수 있는 노드를 제한할 수 있다.

여기에 현재 `requiredDuringSchedulingIgnoredDuringExecution` 와 `preferredDuringSchedulingIgnoredDuringExecution` 로 부르는
두 가지 종류의 노드 어피니티가 있다. 전자는 파드가 노드에 스케줄되도록 *반드시*
규칙을 만족해야 하는 것(`nodeSelector` 와 비슷하나 보다 표현적인 구문을 사용해서)을 지정하고,
후자는 스케줄러가 시도하려고는 하지만, 보증하지 않는 *선호(preferences)* 를 지정한다는 점에서
이를 각각 "엄격함(hard)" 과 "유연함(soft)" 으로 생각할 수 있다.
이름의 "IgnoredDuringExecution" 부분은 `nodeSelector` 작동 방식과 유사하게 노드의
레이블이 런타임 중에 변경되어 파드의 어피니티 규칙이 더 이상 충족되지 않으면 파드가 그 노드에서
동작한다는 의미이다. 향후에는 파드의 노드 어피니티 요구 사항을 충족하지 않는 노드에서 파드를 제거한다는
점을 제외하고는 `preferredDuringSchedulingIgnoredDuringExecution` 와 동일한 `requiredDuringSchedulingIgnoredDuringExecution` 를 제공할 계획이다.

따라서 `requiredDuringSchedulingIgnoredDuringExecution` 의 예로는 "인텔 CPU가 있는 노드에서만 파드 실행"이
될 수 있고, `preferredDuringSchedulingIgnoredDuringExecution` 의 예로는 "장애 조치 영역 XYZ에 파드 집합을 실행하려고
하지만, 불가능하다면 다른 곳에서 일부를 실행하도록 허용"이 있을 것이다.

노드 어피니티는 PodSpec의 `affinity` 필드의 `nodeAffinity` 필드에서 지정된다.

여기에 노드 어피니티를 사용하는 파드 예시가 있다.

{{< codenew file="pods/pod-with-node-affinity.yaml" >}}

이 노드 어피니티 규칙은 키가 `kubernetes.io/e2e-az-name` 이고 값이 `e2e-az1` 또는 `e2e-az2` 인
레이블이 있는 노드에만 파드를 배치할 수 있다고 말한다. 또한, 이 기준을 충족하는 노드들
중에서 키가 `another-node-label-key` 이고 값이 `another-node-label-value` 인 레이블이 있는 노드를
선호하도록 한다.

예시에서 연산자 `In` 이 사용되고 있는 것을 볼 수 있다. 새로운 노드 어피니티 구문은 다음의 연산자들을 지원한다. `In`, `NotIn`, `Exists`, `DoesNotExist`, `Gt`, `Lt`.
`NotIn` 과 `DoesNotExist` 를 사용해서 안티-어피니티를 수행하거나,
특정 노드에서 파드를 쫓아내는 [노드 테인트(taint)](/ko/docs/concepts/scheduling-eviction/taint-and-toleration/)를 설정할 수 있다.

`nodeSelector` 와 `nodeAffinity` 를 모두 지정한다면 파드가 후보 노드에 스케줄되기 위해서는
*둘 다* 반드시 만족해야 한다.

`nodeAffinity` 유형과 연관된 `nodeSelectorTerms` 를 지정하면, `nodeSelectorTerms` 중 **하나라도** 만족시키는 노드에 파드가 스케줄된다.

`nodeSelectorTerms` 와 연관된 여러 `matchExpressions` 를 지정하면, 파드는 `matchExpressions` 를 **모두** 만족하는 노드에만 스케줄된다.

파드가 스케줄된 노드의 레이블을 지우거나 변경해도 파드는 제거되지 않는다. 다시 말해서 어피니티 선택은 파드를 스케줄링 하는 시점에만 작동한다.

`preferredDuringSchedulingIgnoredDuringExecution` 의 `weight` 필드의 범위는 1-100이다. 모든 스케줄링 요구 사항 (리소스 요청, RequiredDuringScheduling 어피니티 표현식 등)을 만족하는 각 노드들에 대해 스케줄러는 이 필드의 요소들을 반복해서 합계를 계산하고 노드가 MatchExpressions 에 일치하는 경우 합계에 "가중치(weight)"를 추가한다. 이후에 이 점수는 노드에 대한 다른 우선순위 함수의 점수와 합쳐진다. 전체 점수가 가장 높은 노드를 가장 선호한다.

#### 스케줄링 프로파일당 노드 어피니티

{{< feature-state for_k8s_version="v1.20" state="beta" >}}

여러 [스케줄링 프로파일](/ko/docs/reference/scheduling/config/#여러-프로파일)을 구성할 때
노드 어피니티가 있는 프로파일을 연결할 수 있는데, 이는 프로파일이 특정 노드 집합에만 적용되는 경우 유용하다.
이렇게 하려면 [스케줄러 구성](/ko/docs/reference/scheduling/config/)에 있는
[`NodeAffinity` 플러그인](/ko/docs/reference/scheduling/config/#스케줄링-플러그인-1)의 인수에 `addedAffinity`를 추가한다. 예를 들면

```yaml
apiVersion: kubescheduler.config.k8s.io/v1beta1
kind: KubeSchedulerConfiguration

profiles:
  - schedulerName: default-scheduler
  - schedulerName: foo-scheduler
    pluginConfig:
      - name: NodeAffinity
        args:
          addedAffinity:
            requiredDuringSchedulingIgnoredDuringExecution:
              nodeSelectorTerms:
              - matchExpressions:
                - key: scheduler-profile
                  operator: In
                  values:
                  - foo
```

`addedAffinity`는 `.spec.schedulerName`을 `foo-scheduler`로 설정하는 모든 파드에 적용되며
PodSpec에 지정된 NodeAffinity도 적용된다.
즉, 파드를 매칭시키려면, 노드가 `addedAffinity`와 파드의 `.spec.NodeAffinity`를 충족해야 한다.

`addedAffinity`는 엔드 유저에게 표시되지 않으므로, 예상치 못한 동작이 일어날 수 있다. 프로파일의
스케줄러 이름과 명확한 상관 관계가 있는 노드 레이블을 사용하는 것이 좋다.

{{< note >}}
[데몬셋용 파드를 생성](/ko/docs/concepts/workloads/controllers/daemonset/#기본-스케줄러로-스케줄)하는 데몬셋 컨트롤러는
스케줄링 프로파일을 인식하지 못한다.
따라서 `addedAffinity`없이 `default-scheduler`와 같은 스케줄러 프로파일을 유지하는 것이 좋다. 그런 다음 데몬셋의 파드 템플릿이 스케줄러 이름을 사용해야 한다.
그렇지 않으면, 데몬셋 컨트롤러에 의해 생성된 일부 파드가 스케줄되지 않은 상태로 유지될 수 있다.
{{< /note >}}

### 파드간 어피니티와 안티-어피니티

파드간 어피니티와 안티-어피니티를 사용하면 노드의 레이블을 기반으로 하지 않고, *노드에서 이미 실행 중인 파드 레이블을 기반으로*
파드가 스케줄될 수 있는 노드를 제한할 수 있다. 규칙은 "X가 규칙 Y를 충족하는 하나 이상의 파드를 이미 실행중인 경우
이 파드는 X에서 실행해야 한다(또는 안티-어피니티가 없는 경우에는 동작하면 안된다)"는 형태이다. Y는
선택적으로 연관된 네임스페이스 목록을 가진 LabelSelector로 표현된다. 노드와는 다르게 파드는 네임스페이스이기에
(그리고 따라서 파드의 레이블은 암암리에 네임스페이스이다) 파드 레이블위의 레이블 셀렉터는 반드시
셀렉터가 적용될 네임스페이스를 지정해야만 한다. 개념적으로 X는 노드, 랙,
클라우드 공급자 영역, 클라우드 공급자 지역 등과 같은 토폴로지 도메인이다. 시스템이 이런 토폴로지
도메인을 나타내는 데 사용하는 노드 레이블 키인 `topologyKey` 를 사용하여 이를 표현한다.
예: [넘어가기 전에: 빌트인 노드 레이블](#built-in-node-labels) 섹션 위에 나열된 레이블 키를 본다.

{{< note >}}
파드간 어피니티와 안티-어피니티에는 상당한 양의 프로세싱이 필요하기에
대규모 클러스터에서는 스케줄링 속도가 크게 느려질 수 있다.
수백 개의 노드를 넘어가는 클러스터에서 이를 사용하는 것은 추천하지 않는다.
{{< /note >}}

{{< note >}}
파드 안티-어피니티에서는 노드에 일관된 레이블을 지정해야 한다. 즉, 클러스터의 모든 노드는 `topologyKey` 와 매칭되는 적절한 레이블을 가지고 있어야 한다. 일부 또는 모든 노드에 지정된 `topologyKey` 레이블이 없는 경우에는 의도하지 않은 동작이 발생할 수 있다.
{{< /note >}}

노드 어피니티와 마찬가지로 현재 파드 어피니티와 안티-어피니티로 부르는 "엄격함" 대 "유연함"의 요구사항을 나타내는 `requiredDuringSchedulingIgnoredDuringExecution` 와
`preferredDuringSchedulingIgnoredDuringExecution` 두 가지 종류가 있다.
앞의 노드 어피니티 섹션의 설명을 본다.
`requiredDuringSchedulingIgnoredDuringExecution` 어피니티의 예시는
"서로 많은 통신을 하기 때문에 서비스 A와 서비스 B를 같은 영역에 함께 위치시키는 것"이고,
`preferredDuringSchedulingIgnoredDuringExecution` 안티-어피니티의 예시는 "서비스를 여러 영역에 걸쳐서 분배하는 것"이다
(엄격한 요구사항은 영역보다 파드가 더 많을 수 있기 때문에 엄격한 요구사항은 의미가 없다).

파드간 어피니티는 PodSpec에서 `affinity` 필드 중 `podAffinity` 필드로 지정한다.
그리고 파드간 안티-어피니티는 PodSpec에서 `affinity` 필드 중 `podAntiAffinity` 필드로 지정한다.

#### 파드 어피니티를 사용하는 파드의 예시

{{< codenew file="pods/pod-with-pod-affinity.yaml" >}}

이 파드의 어피니티는 하나의 파드 어피니티 규칙과 하나의 파드 안티-어피니티 규칙을 정의한다.
이 예시에서 `podAffinity` 는 `requiredDuringSchedulingIgnoredDuringExecution` 이고 `podAntiAffinity` 는
`preferredDuringSchedulingIgnoredDuringExecution` 이다. 파드 어피니티 규칙에 의하면 키 "security" 와 값
"S1"인 레이블이 있는 하나 이상의 이미 실행 중인 파드와 동일한 영역에 있는 경우에만 파드를 노드에 스케줄할 수 있다.
(보다 정확하게는, 클러스터에 키 "security"와 값 "S1"인 레이블을 가지고 있는 실행 중인 파드가 있는 키
`topology.kubernetes.io/zone` 와 값 V인 노드가 최소 하나 이상 있고,
노드 N이 키 `topology.kubernetes.io/zone` 와
일부 값이 V인 레이블을 가진다면 파드는 노드 N에서 실행할 수 있다.)
파드 안티-어피니티 규칙에 의하면 파드는 키 "security"와 값 "S2"인 레이블을 가진 파드와
동일한 영역의 노드에 스케줄되지 않는다.
[디자인 문서](https://git.k8s.io/community/contributors/design-proposals/scheduling/podaffinity.md)를 통해
`requiredDuringSchedulingIgnoredDuringExecution` 와 `preferredDuringSchedulingIgnoredDuringExecution` 의
파드 어피니티와 안티-어피니티에 대한 많은 예시를 맛볼 수 있다.

파드 어피니티와 안티-어피니티의 적합한 연산자는 `In`, `NotIn`, `Exists`, `DoesNotExist` 이다.

원칙적으로, `topologyKey` 는 적법한 어느 레이블-키도 될 수 있다.
하지만, 성능과 보안상의 이유로 topologyKey에는 몇 가지 제약조건이 있다.

1. 파드 어피니티에서 `requiredDuringSchedulingIgnoredDuringExecution` 와 `preferredDuringSchedulingIgnoredDuringExecution` 는
`topologyKey` 의 빈 값을 허용하지 않는다.
2. 파드 안티-어피니티에서도 `requiredDuringSchedulingIgnoredDuringExecution` 와 `preferredDuringSchedulingIgnoredDuringExecution` 는
`topologyKey` 의 빈 값을 허용하지 않는다.
3. `requiredDuringSchedulingIgnoredDuringExecution` 파드 안티-어피니티에서 `topologyKey` 를 `kubernetes.io/hostname` 로 제한하기 위해 어드미션 컨트롤러 `LimitPodHardAntiAffinityTopology` 가 도입되었다. 사용자 지정 토폴로지를 사용할 수 있도록 하려면, 어드미션 컨트롤러를 수정하거나 아니면 이를 비활성화해야 한다.
4. 위의 경우를 제외하고, `topologyKey` 는 적법한 어느 레이블-키도 가능하다.

`labelSelector` 와 `topologyKey` 외에도 `labelSelector` 와 일치해야 하는 네임스페이스 목록 `namespaces` 를
선택적으로 지정할 수 있다(이것은 `labelSelector` 와 `topologyKey` 와 같은 수준의 정의이다).
생략되어있거나 비어있을 경우 어피니티/안티-어피니티 정의가 있는 파드의 네임스페이스가 기본 값이다.

파드를 노드에 스케줄하려면 `requiredDuringSchedulingIgnoredDuringExecution` 어피니티와 안티-어피니티와
연관된 `matchExpressions` 가 모두 충족되어야 한다.

#### 네임스페이스 셀렉터
{{< feature-state for_k8s_version="v1.21" state="alpha" >}}

사용자는 네임스페이스 집합에 대한 레이블 쿼리인 `namespaceSelector` 를 사용하여 일치하는 네임스페이스를 선택할 수도 있다.
어피니티 용어는 `namespaceSelector` 에서 선택한 네임스페이스와 `namespaces` 필드에 나열된 네임스페이스의 결합에 적용된다.
빈 `namespaceSelector` ({})는 모든 네임스페이스와 일치하는 반면, null 또는 빈 `namespaces` 목록과
null `namespaceSelector` 는 "이 파드의 네임스페이스"를 의미한다.

이 기능은 알파이며 기본적으로 비활성화되어 있다. kube-apiserver 및 kube-scheduler 모두에서
[기능 게이트](/ko/docs/reference/command-line-tools-reference/feature-gates/)
`PodAffinityNamespaceSelector` 를 설정하여 활성화할 수 있다.

#### 더 실용적인 유스케이스

파드간 어피니티와 안티-어피니티는 레플리카셋, 스테이트풀셋, 디플로이먼트 등과 같은
상위 레벨 모음과 함께 사용할 때 더욱 유용할 수 있다. 워크로드 집합이 동일한 노드와 같이
동일하게 정의된 토폴로지와 같은 위치에 배치되도록 쉽게 구성할 수 있다.

##### 항상 같은 노드에 위치시키기

세 개의 노드가 있는 클러스터에서 웹 애플리케이션에는 redis와 같은 인-메모리 캐시가 있다. 웹 서버가 가능한 캐시와 함께 위치하기를 원한다.

다음은 세 개의 레플리카와 셀렉터 레이블이 `app=store` 가 있는 간단한 redis 디플로이먼트의 yaml 스니펫이다. 디플로이먼트에는 스케줄러가 단일 노드에서 레플리카를 함께 배치하지 않도록 `PodAntiAffinity` 가 구성되어 있다.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis-cache
spec:
  selector:
    matchLabels:
      app: store
  replicas: 3
  template:
    metadata:
      labels:
        app: store
    spec:
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchExpressions:
              - key: app
                operator: In
                values:
                - store
            topologyKey: "kubernetes.io/hostname"
      containers:
      - name: redis-server
        image: redis:3.2-alpine
```

아래 yaml 스니펫의 웹서버 디플로이먼트는 `podAntiAffinity` 와 `podAffinity` 설정을 가지고 있다. 이렇게 하면 스케줄러에 모든 레플리카는 셀렉터 레이블이 `app=store` 인 파드와 함께 위치해야 한다. 또한 각 웹 서버 레플리카가 단일 노드의 같은 위치에 있지 않도록 한다.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-server
spec:
  selector:
    matchLabels:
      app: web-store
  replicas: 3
  template:
    metadata:
      labels:
        app: web-store
    spec:
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchExpressions:
              - key: app
                operator: In
                values:
                - web-store
            topologyKey: "kubernetes.io/hostname"
        podAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchExpressions:
              - key: app
                operator: In
                values:
                - store
            topologyKey: "kubernetes.io/hostname"
      containers:
      - name: web-app
        image: nginx:1.16-alpine
```

만약 위의 두 디플로이먼트를 생성하면 세 개의 노드가 있는 클러스터는 다음과 같아야 한다.

|       node-1         |       node-2        |       node-3       |
|:--------------------:|:-------------------:|:------------------:|
| *webserver-1*        |   *webserver-2*     |    *webserver-3*   |
|  *cache-1*           |     *cache-2*       |     *cache-3*      |

여기서 볼 수 있듯이 `web-server` 의 세 레플리카들이 기대했던 것처럼 자동으로 캐시와 함께 위치하게 된다.

```
kubectl get pods -o wide
```
출력은 다음과 유사할 것이다.
```
NAME                           READY     STATUS    RESTARTS   AGE       IP           NODE
redis-cache-1450370735-6dzlj   1/1       Running   0          8m        10.192.4.2   kube-node-3
redis-cache-1450370735-j2j96   1/1       Running   0          8m        10.192.2.2   kube-node-1
redis-cache-1450370735-z73mh   1/1       Running   0          8m        10.192.3.1   kube-node-2
web-server-1287567482-5d4dz    1/1       Running   0          7m        10.192.2.3   kube-node-1
web-server-1287567482-6f7v5    1/1       Running   0          7m        10.192.4.3   kube-node-3
web-server-1287567482-s330j    1/1       Running   0          7m        10.192.3.2   kube-node-2
```

##### 절대 동일한 노드에 위치시키지 않게 하기

위의 예시에서 `topologyKey:"kubernetes.io/hostname"` 과 함께 `PodAntiAffinity` 규칙을 사용해서
두 개의 인스터스가 동일한 호스트에 있지 않도록 redis 클러스터를 배포한다.
같은 기술을 사용해서 고 가용성을 위해 안티-어피니티로 구성된 스테이트풀셋의 예시는
[ZooKeeper 튜토리얼](/ko/docs/tutorials/stateful-application/zookeeper/#노드-실패-방지)을 본다.

## nodeName

`nodeName` 은 가장 간단한 형태의 노트 선택 제약 조건이지만,
한계로 인해 일반적으로는 사용하지 않는다.
`nodeName` 은 PodSpec의 필드이다. 만약 비어있지 않으면, 스케줄러는
파드를 무시하고 명명된 노드에서 실행 중인 kubelet이
파드를 실행하려고 한다. 따라서 만약 PodSpec에 `nodeName` 가
제공된 경우, 노드 선택을 위해 위의 방법보다 우선한다.

`nodeName` 을 사용해서 노드를 선택할 때의 몇 가지 제한은 다음과 같다.

-   만약 명명된 노드가 없으면, 파드가 실행되지 않고
    따라서 자동으로 삭제될 수 있다.
-   만약 명명된 노드에 파드를 수용할 수 있는
    리소스가 없는 경우 파드가 실패하고, 그 이유는 다음과 같이 표시된다.
    예: OutOfmemory 또는 OutOfcpu.
-   클라우드 환경의 노드 이름은 항상 예측 가능하거나
    안정적인 것은 아니다.

여기에 `nodeName` 필드를 사용하는 파드 설정 파일 예시가 있다.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
spec:
  containers:
  - name: nginx
    image: nginx
  nodeName: kube-01
```

위 파드는 kube-01 노드에서 실행될 것이다.



## {{% heading "whatsnext" %}}


[테인트](/ko/docs/concepts/scheduling-eviction/taint-and-toleration/)는 노드가 특정 파드들을 *쫓아낼* 수 있다.

[노드 어피니티](https://git.k8s.io/community/contributors/design-proposals/scheduling/nodeaffinity.md)와
[파드간 어피니티/안티-어피니티](https://git.k8s.io/community/contributors/design-proposals/scheduling/podaffinity.md)에 대한 디자인 문서에는
이러한 기능에 대한 추가 배경 정보가 있다.

파드가 노드에 할당되면 kubelet은 파드를 실행하고 노드의 로컬 리소스를 할당한다.
[토폴로지 매니저](/docs/tasks/administer-cluster/topology-manager/)는
노드 수준의 리소스 할당 결정에 참여할 수 있다.
