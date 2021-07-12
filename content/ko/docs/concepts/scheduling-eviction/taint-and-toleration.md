---
title: 테인트(Taints)와 톨러레이션(Tolerations)
content_type: concept
weight: 40
---


<!-- overview -->
[_노드 어피니티_](/ko/docs/concepts/scheduling-eviction/assign-pod-node/#어피니티-affinity-와-안티-어피니티-anti-affinity)는
{{< glossary_tooltip text="노드" term_id="node" >}} 셋을
(기본 설정 또는 어려운 요구 사항으로) *끌어들이는* {{< glossary_tooltip text="파드" term_id="pod" >}}의 속성이다.
_테인트_ 는 그 반대로, 노드가 파드 셋을 제외할 수 있다.

_톨러레이션_ 은 파드에 적용되며, 파드를 일치하는 테인트가 있는 노드에
스케줄되게 하지만 필수는 아니다.

테인트와 톨러레이션은 함께 작동하여 파드가 부적절한 노드에 스케줄되지
않게 한다. 하나 이상의 테인트가 노드에 적용된다. 이것은
노드가 테인트를 용인하지 않는 파드를 수용해서는 안 되는 것을 나타낸다.



<!-- body -->

## 개요

[kubectl taint](/docs/reference/generated/kubectl/kubectl-commands#taint)를 사용하여 노드에 테인트을 추가한다.
예를 들면 다음과 같다.

```shell
kubectl taint nodes node1 key1=value1:NoSchedule
```

`node1` 노드에 테인트을 배치한다. 테인트에는 키 `key1`, 값 `value1` 및 테인트 이펙트(effect) `NoSchedule` 이 있다.
이는 일치하는 톨러레이션이 없으면 파드를 `node1` 에 스케줄할 수 없음을 의미한다.

위의 명령으로 추가한 테인트를 제거하려면, 다음을 실행한다.
```shell
kubectl taint nodes node1 key1=value1:NoSchedule-
```

PodSpec에서 파드에 대한 톨러레이션를 지정한다. 다음의 톨러레이션은
위의 `kubectl taint` 라인에 의해 생성된 테인트와 "일치"하므로, 어느 쪽 톨러레이션을 가진 파드이던
`node1` 에 스케줄 될 수 있다.

```yaml
tolerations:
- key: "key1"
  operator: "Equal"
  value: "value1"
  effect: "NoSchedule"
```

```yaml
tolerations:
- key: "key1"
  operator: "Exists"
  effect: "NoSchedule"
```

톨러레이션을 사용하는 파드의 예는 다음과 같다.

{{< codenew file="pods/pod-with-toleration.yaml" >}}

지정하지 않으면 `operator` 의 기본값은 `Equal` 이다.

톨러레이션은 키가 동일하고 이펙트가 동일한 경우, 테인트와 "일치"한다. 그리고 다음의 경우에도 마찬가지다.

* `operator` 가 `Exists` 인 경우(이 경우 `value` 를 지정하지 않아야 함), 또는
* `operator` 는 `Equal` 이고 `value` 는 `value` 로 같다.

{{< note >}}

두 가지 특별한 경우가 있다.

operator `Exists` 가 있는 비어있는 `key` 는 모든 키, 값 및 이펙트와 일치하므로
모든 것이 톨러레이션 된다.

비어있는 `effect` 는 모든 이펙트를 키 `key1` 와 일치시킨다.

{{< /note >}}

위의 예는 `NoSchedule` 의 `effect` 를 사용했다. 또는, `PreferNoSchedule` 의 `effect` 를 사용할 수 있다.
이것은 `NoSchedule` 의 "기본 설정(preference)" 또는 "소프트(soft)" 버전이다. 시스템은 노드의 테인트를 허용하지 않는
파드를 배치하지 않으려고 *시도* 하지만, 필요하지는 않다. 세 번째 종류의 `effect` 는
나중에 설명할 `NoExecute` 이다.

동일한 노드에 여러 테인트를, 동일한 파드에 여러 톨러레이션을 둘 수 있다.
쿠버네티스가 여러 테인트 및 톨러레이션을 처리하는 방식은 필터와 같다.
모든 노드의 테인트로 시작한 다음, 파드에 일치하는 톨러레이션이 있는 것을 무시한다.
무시되지 않은 나머지 테인트는 파드에 표시된 이펙트를 가진다. 특히,

* `NoSchedule` 이펙트가 있는 무시되지 않은 테인트가 하나 이상 있으면 쿠버네티스는 해당 노드에
파드를 스케줄하지 않는다.
* `NoSchedule` 이펙트가 있는 무시되지 않은 테인트가 없지만 `PreferNoSchedule` 이펙트가 있는
무시되지 않은 테인트가 하나 이상 있으면 쿠버네티스는 파드를 노드에 스케쥴하지 않으려고 *시도* 한다
* `NoExecute` 이펙트가 있는 무시되지 않은 테인트가 하나 이상 있으면
파드가 노드에서 축출되고(노드에서 이미 실행 중인 경우), 노드에서
스케줄되지 않는다(아직 실행되지 않은 경우).

예를 들어, 이와 같은 노드를 테인트하는 경우는 다음과 같다.

```shell
kubectl taint nodes node1 key1=value1:NoSchedule
kubectl taint nodes node1 key1=value1:NoExecute
kubectl taint nodes node1 key2=value2:NoSchedule
```

그리고 파드에는 두 가지 톨러레이션이 있다.

```yaml
tolerations:
- key: "key1"
  operator: "Equal"
  value: "value1"
  effect: "NoSchedule"
- key: "key1"
  operator: "Equal"
  value: "value1"
  effect: "NoExecute"
```

이 경우, 세 번째 테인트와 일치하는 톨러레이션이 없기 때문에, 파드는
노드에 스케줄 될 수 없다. 그러나 세 번째 테인트가 파드에서 용인되지 않는 세 가지 중
하나만 있기 때문에, 테인트가 추가될 때 노드에서 이미 실행 중인 경우,
파드는 계속 실행할 수 있다.

일반적으로, `NoExecute` 이펙트가 있는 테인트가 노드에 추가되면, 테인트를
용인하지 않는 파드는 즉시 축출되고, 테인트를 용인하는 파드는
축출되지 않는다. 그러나 `NoExecute` 이펙트가 있는 톨러레이션은
테인트가 추가된 후 파드가 노드에 바인딩된 시간을 지정하는
선택적 `tolerationSeconds` 필드를 지정할 수 있다. 예를 들어,

```yaml
tolerations:
- key: "key1"
  operator: "Equal"
  value: "value1"
  effect: "NoExecute"
  tolerationSeconds: 3600
```

이것은 이 파드가 실행 중이고 일치하는 테인트가 노드에 추가되면,
파드는 3600초 동안 노드에 바인딩된 후, 축출된다는 것을 의미한다. 그 전에
테인트를 제거하면, 파드가 축출되지 않는다.

## 유스케이스 예시

테인트 및 톨러레이션은 파드를 노드에서 *멀어지게* 하거나 실행되지 않아야 하는
파드를 축출할 수 있는 유연한 방법이다. 유스케이스 중 일부는 다음과 같다.

* **전용 노드**: 특정 사용자들이 독점적으로 사용하도록
노드 셋을 전용하려면, 해당 노드에 테인트를 추가(예:
`kubectl taint nodes nodename dedicated=groupName:NoSchedule`)한 다음 해당
톨러레이션을 그들의 파드에 추가할 수 있다(사용자 정의 [어드미션 컨트롤러]
(/docs/reference/access-authn-authz/admission-controllers/)를 작성하면 가장 쉽게 수행할 수 있음).
그런 다음 톨러레이션이 있는 파드는 테인트된(전용) 노드와
클러스터의 다른 노드를 사용할 수 있다. 노드를 특정 사용자들에게 전용으로 지정하고 *그리고*
그 사용자들이 전용 노드 *만* 사용하려면, 동일한 노드 셋에
테인트와 유사한 레이블을 추가해야 하고(예: `dedicated=groupName`),
어드미션 컨트롤러는 추가로 파드가 `dedicated=groupName` 으로 레이블이 지정된 노드에만
스케줄될 수 있도록 노드 어피니티를 추가해야 한다.

* **특별한 하드웨어가 있는 노드**: 작은 서브셋의 노드에 특별한
하드웨어(예: GPU)가 있는 클러스터에서는, 특별한 하드웨어가 필요하지 않는 파드를
해당 노드에서 분리하여, 나중에 도착하는 특별한 하드웨어가 필요한 파드를 위한 공간을
남겨두는 것이 바람직하다. 이는 특별한 하드웨어가 있는
노드(예: `kubectl taint nodes nodename special=true:NoSchedule` 또는
`kubectl taint nodes nodename special=true:PreferNoSchedule`)에 테인트를 추가하고
특별한 하드웨어를 사용하는 파드에 해당 톨러레이션을 추가하여 수행할 수 있다. 전용 노드 유스케이스에서와 같이,
사용자 정의 [어드미션 컨트롤러](/docs/reference/access-authn-authz/admission-controllers/)를
사용하여 톨러레이션를 적용하는 것이 가장 쉬운 방법이다.
예를 들어, [확장된
리소스](/ko/docs/concepts/configuration/manage-resources-containers/#확장된-리소스)를
사용하여 특별한 하드웨어를 나타내고, 확장된 리소스 이름으로
특별한 하드웨어 노드를 테인트시키고
[ExtendedResourceToleration](/docs/reference/access-authn-authz/admission-controllers/#extendedresourcetoleration)
어드미션 컨트롤러를 실행하는 것을 권장한다. 이제, 노드가 테인트되었으므로, 톨러레이션이 없는
파드는 스케줄되지 않는다. 그러나 확장된 리소스를 요청하는 파드를 제출하면,
`ExtendedResourceToleration` 어드미션 컨트롤러가
파드에 올바른 톨러레이션을 자동으로 추가하고 해당 파드는
특별한 하드웨어 노드에서 스케줄된다. 이렇게 하면 이러한 특별한 하드웨어 노드가
해당 하드웨어를 요청하는 파드가 전용으로 사용하며 파드에 톨러레이션을
수동으로 추가할 필요가 없다.

* **테인트 기반 축출**: 노드 문제가 있을 때 파드별로
구성 가능한 축출 동작은 다음 섹션에서 설명한다.

## 테인트 기반 축출

{{< feature-state for_k8s_version="v1.18" state="stable" >}}

앞에서 우리는 노드에서 이미 실행 중인 파드에 영향을 주는 `NoExecute` 테인트 이펙트를
다음과 같이 언급했다.

 * 테인트를 용인하지 않는 파드는 즉시 축출된다.
 * 톨러레이션 명세에 `tolerationSeconds` 를 지정하지 않고
   테인트를 용인하는 파드는 계속 바인딩된다.
 * `tolerationSeconds` 가 지정된 테인트를 용인하는 파드는 지정된
  시간 동안 바인딩된 상태로 유지된다.

노드 컨트롤러는 특정 조건이 참일 때 자동으로
노드를 테인트시킨다. 다음은 빌트인 테인트이다.

 * `node.kubernetes.io/not-ready`: 노드가 준비되지 않았다. 이는 NodeCondition
   `Ready` 가 "`False`"로 됨에 해당한다.
 * `node.kubernetes.io/unreachable`: 노드가 노드 컨트롤러에서 도달할 수 없다. 이는
   NodeCondition `Ready` 가 "`Unknown`"로 됨에 해당한다.
 * `node.kubernetes.io/memory-pressure`: 노드에 메모리 할당 압박이 있다.
 * `node.kubernetes.io/disk-pressure`: 노드에 디스크 할당 압박이 있다.
 * `node.kubernetes.io/pid-pressure`: 노드에 PID 할당 압박이 있다.
 * `node.kubernetes.io/network-unavailable`: 노드의 네트워크를 사용할 수 없다.
 * `node.kubernetes.io/unschedulable`: 노드를 스케줄할 수 없다.
 * `node.cloudprovider.kubernetes.io/uninitialized`: "외부" 클라우드 공급자로
    kubelet을 시작하면, 이 테인트가 노드에서 사용 불가능으로 표시되도록
    설정된다. 클라우드-컨트롤러-관리자의 컨트롤러가 이 노드를 초기화하면,
    kubelet이 이 테인트를 제거한다.

노드가 축출될 경우, 노드 컨트롤러 또는 kubelet은 `NoExecute` 이펙트로 관련
테인트를 추가한다. 장애 상태가 정상으로 돌아오면 kubelet 또는 노드 컨트롤러가
관련 테인트를 제거할 수 있다.

{{< note >}}
콘트롤 플레인은 노드에 새 테인트를 추가하는 비율을 제한한다.
이 비율-제한은 많은 노드가 동시에 도달할 수 없을 때(예를 들어, 네트워크 중단으로)
트리거될 축출 개수를 관리한다.
{{< /note >}}

이 기능을 `tolerationSeconds` 와 함께 사용하면, 파드에서
이러한 문제 중 하나 또는 둘 다가 있는 노드에 바인딩된 기간을 지정할 수 있다.

예를 들어, 로컬 상태가 많은 애플리케이션은 네트워크 분할의 장애에서
네트워크가 복구된 후에 파드가 축출되는 것을 피하기 위해
오랫동안 노드에 바인딩된 상태를 유지하려고 할 수 있다.
이 경우 파드가 사용하는 톨러레이션은 다음과 같다.

```yaml
tolerations:
- key: "node.kubernetes.io/unreachable"
  operator: "Exists"
  effect: "NoExecute"
  tolerationSeconds: 6000
```

{{< note >}}
쿠버네티스는 사용자나 컨트롤러에서 명시적으로 설정하지 않았다면, 자동으로
`node.kubernetes.io/not-ready` 와 `node.kubernetes.io/unreachable` 에 대해
`tolerationSeconds=300` 으로
톨러레이션을 추가한다.

자동으로 추가된 이 톨러레이션은 이러한 문제 중 하나가 감지된 후 5분 동안
파드가 노드에 바인딩된 상태를 유지함을 의미한다.
{{< /note >}}

[데몬셋](/ko/docs/concepts/workloads/controllers/daemonset/) 파드는 `tolerationSeconds` 가 없는
다음 테인트에 대해 `NoExecute` 톨러레이션를 가지고 생성된다.

  * `node.kubernetes.io/unreachable`
  * `node.kubernetes.io/not-ready`

이렇게 하면 이러한 문제로 인해 데몬셋 파드가 축출되지 않는다.

## 컨디션별 노드 테인트하기

노드 라이프사이클 컨트롤러는 `NoSchedule` 이펙트가 있는 노드 컨디션에 해당하는
테인트를 자동으로 생성한다.
마찬가지로 스케줄러는 노드 컨디션을 확인하지 않는다. 대신 스케줄러는 테인트를 확인한다. 이렇게 하면 노드 컨디션이 노드에 스케줄된 내용에 영향을 미치지 않는다. 사용자는 적절한 파드 톨러레이션을 추가하여 노드의 일부 문제(노드 컨디션으로 표시)를 무시하도록 선택할 수 있다.

쿠버네티스 1.8 버전부터 데몬셋 컨트롤러는 다음의 `NoSchedule` 톨러레이션을
모든 데몬에 자동으로 추가하여, 데몬셋이 중단되는 것을 방지한다.

  * `node.kubernetes.io/memory-pressure`
  * `node.kubernetes.io/disk-pressure`
  * `node.kubernetes.io/pid-pressure` (1.14 이상)
  * `node.kubernetes.io/unschedulable` (1.10 이상)
  * `node.kubernetes.io/network-unavailable` (*호스트 네트워크만 해당*)

이러한 톨러레이션을 추가하면 이전 버전과의 호환성이 보장된다. 데몬셋에
임의의 톨러레이션을 추가할 수도 있다.


## {{% heading "whatsnext" %}}

* [리소스 부족 다루기](/docs/concepts/scheduling-eviction/node-pressure-eviction/)와 어떻게 구성하는지에 대해 알아보기
* [파드 우선순위](/ko/docs/concepts/scheduling-eviction/pod-priority-preemption/)에 대해 알아보기
