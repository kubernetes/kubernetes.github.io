---






title: 데몬셋
content_type: concept
weight: 40
---

<!-- overview -->

_데몬셋_ 은 모든(또는 일부) 노드가 파드의 사본을 실행하도록 한다. 노드가 클러스터에 추가되면
파드도 추가된다. 노드가 클러스터에서 제거되면 해당 파드는 가비지(garbage)로
수집된다. 데몬셋을 삭제하면 데몬셋이 생성한 파드들이 정리된다.

데몬셋의 일부 대표적인 용도는 다음과 같다.

- 모든 노드에서 클러스터 스토리지 데몬 실행
- 모든 노드에서 로그 수집 데몬 실행
- 모든 노드에서 노드 모니터링 데몬 실행

단순한 케이스에서는, 각 데몬 유형의 처리를 위해서 모든 노드를 커버하는 하나의 데몬셋이 사용된다.
더 복잡한 구성에서는 단일 유형의 데몬에 여러 데몬셋을 사용할 수 있지만,
각기 다른 하드웨어 유형에 따라 서로 다른 플래그, 메모리, CPU 요구가 달라진다.

<!-- body -->

## 데몬셋 사양 작성

### 데몬셋 생성

YAML 파일에 데몬셋 명세를 작성할 수 있다. 예를 들어 아래 `daemonset.yaml` 파일은 
fluentd-elasticsearch 도커 이미지를 실행하는 데몬셋을 설명한다.

{{< codenew file="controllers/daemonset.yaml" >}}

YAML 파일을 기반으로 데몬셋을 생성한다.

```
kubectl apply -f https://k8s.io/examples/controllers/daemonset.yaml
```

### 필수 필드

다른 모든 쿠버네티스 설정과 마찬가지로 데몬셋에는 `apiVersion`, `kind` 그리고 `metadata` 필드가 필요하다.
일반적인 설정파일 작업에 대한 정보는
[스테이트리스 애플리케이션 실행하기](/docs/tasks/run-application/run-stateless-application-deployment/)와
 [kubectl을 사용한 오브젝트 관리](/ko/docs/concepts/overview/working-with-objects/object-management/)를 참고한다.

데몬셋 오브젝트의 이름은 유효한
[DNS 서브도메인 이름](/ko/docs/concepts/overview/working-with-objects/names/#dns-서브도메인-이름)이어야 한다.

데몬셋에는 
[`.spec`](https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status) 
섹션도 필요하다.

### 파드 템플릿

`.spec.template` 는 `.spec` 의 필수 필드 중 하나이다.

`.spec.template` 는 [파드 템플릿](/ko/docs/concepts/workloads/pods/#파드-템플릿)이다. 
이것은 중첩되어 있다는 점과 `apiVersion` 또는 `kind` 를 가지지 않는 것을 제외하면 
{{< glossary_tooltip text="파드" term_id="pod" >}}와 정확히 같은 스키마를 가진다.

데몬셋의 파드 템플릿에는 파드의 필수 필드 외에도 적절한 레이블이 명시되어야
한다([파드 셀렉터](#파드-셀렉터)를 본다).

데몬셋의 파드 템플릿의 [`RestartPolicy`](/ko/docs/concepts/workloads/pods/pod-lifecycle/#재시작-정책)는 `Always` 를 가져야 하며,
 명시되지 않은 경우 기본으로 `Always`가 된다.

### 파드 셀렉터

`.spec.selector` 필드는 파드 셀렉터이다. 이것은
[잡](/ko/docs/concepts/workloads/controllers/job/)의 `.spec.selector` 와 같은 동작을 한다.

쿠버네티스 1.8 부터는 레이블이 `.spec.template` 와 일치하는 파드 셀렉터를 명시해야 한다.
파드 셀렉터는 비워두면 더 이상 기본 값이 설정이 되지 않는다.
셀렉터의 기본 값은 `kubectl apply` 과 호환되지 않는다.
또한, 한 번 데몬셋이 만들어지면 `.spec.selector` 의 변형은 가능하지 않다.
파드 셀렉터를 변형하면 의도하지 않게 파드는 고아가 되거나 사용자에게 혼란을 주는 것으로 밝혀졌다.

`.spec.selector` 는 다음 2개의 필드로 구성된 오브젝트이다.

* `matchLabels` - [레플리케이션 컨트롤러](/ko/docs/concepts/workloads/controllers/replicationcontroller/)의 
`.spec.selector` 와 동일하게 작동한다.
* `matchExpressions` - 키, 값 목록 그리고 키 및 값에 관련된 연산자를
  명시해서 보다 정교한 셀렉터를 만들 수 있다.

2개의 필드가 명시되면 두 필드를 모두 만족하는 것(ANDed)이 결과가 된다.

만약 `.spec.selector` 를 명시하면, 이것은 `.spec.template.metadata.labels` 와 일치해야 한다. 
일치하지 않는 구성은 API에 의해 거부된다.

### 오직 일부 노드에서만 파드 실행

만약 `.spec.template.spec.nodeSelector` 를 명시하면 데몬셋 컨트롤러는
[노드 셀렉터](/ko/docs/concepts/scheduling-eviction/assign-pod-node/#노드-셀렉터-nodeselector)와
일치하는 노드에 파드를 생성한다. 
마찬가지로 `.spec.template.spec.affinity` 를 명시하면
데몬셋 컨트롤러는 [노드 어피니티](/ko/docs/concepts/scheduling-eviction/assign-pod-node/#노드-어피니티)와 일치하는 노드에 파드를 생성한다.
만약 둘 중 하나를 명시하지 않으면 데몬셋 컨트롤러는 모든 노드에서 파드를 생성한다.

## 데몬 파드가 스케줄 되는 방법

### 기본 스케줄러로 스케줄

{{< feature-state state="stable" for-kubernetes-version="1.17" >}}

데몬셋은 자격이 되는 모든 노드에서 파드 사본이 실행하도록 보장한다. 일반적으로
쿠버네티스 스케줄러에 의해 파드가 실행되는 노드가 선택된다. 그러나
데몬셋 파드는 데몬셋 컨트롤러에 의해 생성되고 스케줄된다.
이에 대한 이슈를 소개한다.

* 파드 동작의 불일치: 스케줄 되기 위해서 대기 중인 일반 파드는 `Pending` 상태로 생성된다.
  그러나 데몬셋 파드는 `Pending` 상태로 생성되지 않는다.
  이것은 사용자에게 혼란을 준다.
* [파드 선점](/ko/docs/concepts/scheduling-eviction/pod-priority-preemption/)은
  기본 스케줄러에서 처리한다. 선점이 활성화되면 데몬셋 컨트롤러는
  파드 우선순위와 선점을 고려하지 않고 스케줄 한다.

`ScheduleDaemonSetPods` 로 데몬셋 파드에 `.spec.nodeName` 용어 대신
`NodeAffinity` 용어를 추가해서 데몬셋 컨트롤러 대신 기본
스케줄러를 사용해서 데몬셋을 스케줄할 수 있다. 이후에 기본
스케줄러를 사용해서 대상 호스트에 파드를 바인딩한다. 만약 데몬셋 파드에
이미 노드 선호도가 존재한다면 교체한다(대상 호스트를 선택하기 전에 
원래 노드의 어피니티가 고려된다). 데몬셋 컨트롤러는
데몬셋 파드를 만들거나 수정할 때만 이런 작업을 수행하며,
데몬셋의 `spec.template` 은 변경되지 않는다.

```yaml
nodeAffinity:
  requiredDuringSchedulingIgnoredDuringExecution:
    nodeSelectorTerms:
    - matchFields:
      - key: metadata.name
        operator: In
        values:
        - target-host-name
```

또한, 데몬셋 파드에 `node.kubernetes.io/unschedulable:NoSchedule` 이 톨러레이션(toleration)으로
자동으로 추가된다. 기본 스케줄러는 데몬셋 파드를
스케줄링시 `unschedulable` 노드를 무시한다.

### 테인트(taints)와 톨러레이션(tolerations)

데몬 파드는
[테인트와 톨러레이션](/ko/docs/concepts/scheduling-eviction/taint-and-toleration/)을 존중하지만,
다음과 같이 관련 기능에 따라 자동적으로 데몬셋 파드에
톨러레이션을 추가한다.

| 톨러레이션 키                              | 영향       | 버전    | 설명                                                           |
| ---------------------------------------- | ---------- | ------- | ------------------------------------------------------------ |
| `node.kubernetes.io/not-ready`           | NoExecute  | 1.13+   | 네트워크 파티션과 같은 노드 문제가 발생해도 데몬셋 파드는 축출되지 않는다. |
| `node.kubernetes.io/unreachable`         | NoExecute  | 1.13+   | 네트워크 파티션과 같은 노드 문제가 발생해도 데몬셋 파드는 축출되지 않는다. |
| `node.kubernetes.io/disk-pressure`       | NoSchedule | 1.8+    | 데몬셋 파드는 기본 스케줄러에서 디스크-압박(disk-pressure) 속성을 허용한다. |
| `node.kubernetes.io/memory-pressure`     | NoSchedule | 1.8+    | 데몬셋 파드는 기본 스케줄러에서 메모리-압박(memory-pressure) 속성을 허용한다. |
| `node.kubernetes.io/unschedulable`       | NoSchedule | 1.12+   | 데몬셋 파드는 기본 스케줄러의 스케줄할 수 없는(unschedulable) 속성을 극복한다. |
| `node.kubernetes.io/network-unavailable` | NoSchedule | 1.12+   | 호스트 네트워크를 사용하는 데몬셋 파드는 기본 스케줄러에 의해 이용할 수 없는 네트워크(network-unavailable) 속성을 극복한다. |

## 데몬 파드와 통신

데몬셋의 파드와 통신할 수 있는 몇 가지 패턴은 다음과 같다.

- **푸시(Push)**: 데몬셋의 파드는 통계 데이터베이스와 같은 다른 서비스로 업데이트를 보내도록
  구성되어있다. 그들은 클라이언트들을 가지지 않는다.
- **노드IP와 알려진 포트**: 데몬셋의 파드는 `호스트 포트`를 사용할 수 있으며, 
  노드IP를 통해 파드에 접근할 수 있다. 
  클라이언트는 노드IP를 어떻게든지 알고 있으며, 관례에 따라 포트를 알고 있다.
- **DNS**: 동일한 파드 셀렉터로 [헤드리스 서비스](/ko/docs/concepts/services-networking/service/#헤드리스-headless-서비스)를 만들고,
  그 다음에 `엔드포인트` 리소스를 사용해서 데몬셋을 찾거나 
  DNS에서 여러 A레코드를 검색한다.
- **서비스**: 동일한 파드 셀렉터로 서비스를 생성하고, 서비스를 사용해서
  임의의 노드의 데몬에 도달한다(특정 노드에 도달할 방법이 없다).

## 데몬셋 업데이트

만약 노드 레이블이 변경되면, 데몬셋은 새로 일치하는 노드에 즉시 파드를 추가하고, 새로
일치하지 않는 노드에서 파드를 삭제한다.

사용자는 데몬셋이 생성하는 파드를 수정할 수 있다. 그러나 파드는 모든
필드가 업데이트 되는 것을 허용하지 않는다. 또한 데몬셋 컨트롤러는
다음에 노드(동일한 이름으로)가 생성될 때 원본 템플릿을 사용한다.

사용자는 데몬셋을 삭제할 수 있다. 만약 `kubectl` 에서 `--cascade=false` 를 명시하면
파드는 노드에 남게 된다. 이후에 동일한 셀렉터로 새 데몬셋을 생성하면,
새 데몬셋은 기존 파드를 채택한다. 만약 파드를 교체해야 하는 경우 데몬셋은
`updateStrategy` 에 따라 파드를 교체한다.

사용자는 데몬셋에서 [롤링 업데이트를 수행](/ko/docs/tasks/manage-daemon/update-daemon-set/)할 수 있다.

## 데몬셋의 대안

### 초기화 스크립트

데몬 프로세스를 직접 노드에서 시작해서 실행하는 것도 당연히 가능하다.
(예: `init`, `upstartd` 또는 `systemd` 를 사용). 이 방법도 문제는 전혀 없다. 그러나 데몬셋을 통해 데몬
프로세스를 실행하면 몇 가지 이점 있다.

- 애플리케이션과 동일한 방법으로 데몬을 모니터링하고 로그 관리를 할 수 있다.
- 데몬 및 애플리케이션과 동일한 구성 언어와 도구(예: 파드 템플릿, `kubectl`).
- 리소스 제한이 있는 컨테이너에서 데몬을 실행하면 앱 컨테이너에서
  데몬간의 격리를 증가시킨다.  그러나 이것은 파드가 아닌 컨테이너에서 데몬을 실행해서 이루어진다
  (예: 도커에서 직접적으로 시작).

### 베어(Bare) 파드

직접적으로 파드를 실행할 특정한 노드를 명시해서 파드를 생성할 수 있다. 그러나
데몬셋은 노드 장애 또는 커널 업그레이드와 같이 변경사항이 많은 노드 유지보수의 경우를 비롯하여
어떠한 이유로든 삭제되거나 종료된 파드를 교체한다. 따라서 개별 파드를
생성하는 것보다는 데몬 셋을 사용해야 한다.

### 스태틱(static) 파드

Kubelet이 감시하는 특정 디렉터리에 파일을 작성하는 파드를 생성할 수 있다. 이것을
[스태틱 파드](/ko/docs/tasks/configure-pod-container/static-pod/)라고 부른다.
데몬셋과는 다르게 스태틱 파드는 kubectl
또는 다른 쿠버네티스 API 클라이언트로 관리할 수 없다.  스태틱 파드는 API 서버에 의존하지
않기 때문에 클러스터 부트스트랩(bootstraping)하는 경우에 유용하다.  또한 스태틱 파드는 향후에 사용 중단될 수 있다.

### 디플로이먼트

데몬셋은 파드를 생성한다는 점에서 [디플로이먼트](/ko/docs/concepts/workloads/controllers/deployment/)와 유사하고,
해당 파드에서는 프로세스가 종료되지 않을 것으로
예상한다(예: 웹 서버).

파드가 실행되는 호스트를 정확하게 제어하는 것보다 레플리카의 수를 스케일링 업 및 다운 하고,
업데이트 롤아웃이 더 중요한 프런트 엔드와 같은 것은 스테이트리스 서비스의
디플로이먼트를 사용한다. 파드 사본이 항상 모든 호스트 또는 특정 호스트에서 실행되는 것이 중요하고,
다른 파드의 실행 이전에 필요한 경우에는 데몬셋을 사용한다.
