---
title: 스케줄러 구성
content_type: concept
weight: 20
---

{{< feature-state for_k8s_version="v1.19" state="beta" >}}

구성 파일을 작성하고 해당 경로를 커맨드 라인 인수로 전달하여
`kube-scheduler` 의 동작을 사용자 정의할 수 있다.

<!-- overview -->

<!-- body -->

스케줄링 프로파일(Profile)을 사용하면 {{< glossary_tooltip text="kube-scheduler" term_id="kube-scheduler" >}}에서
여러 단계의 스케줄링을 구성할 수 있다.
각 단계는 익스텐션 포인트(extension point)를 통해 노출된다. 플러그인은 이러한
익스텐션 포인트 중 하나 이상을 구현하여 스케줄링 동작을 제공한다.

[KubeSchedulerConfiguration (v1beta1)](/docs/reference/config-api/kube-scheduler-config.v1beta1/)
구조에 맞게 파일을 작성하고,
`kube-scheduler --config <filename>`을 실행하여
스케줄링 프로파일을 지정할 수 있다.

최소 구성은 다음과 같다.

```yaml
apiVersion: kubescheduler.config.k8s.io/v1beta1
kind: KubeSchedulerConfiguration
clientConnection:
  kubeconfig: /etc/srv/kubernetes/kube-scheduler/kubeconfig
```

## 프로파일

스케줄링 프로파일을 사용하면 {{< glossary_tooltip text="kube-scheduler" term_id="kube-scheduler" >}}에서
여러 단계의 스케줄링을 구성할 수 있다.
각 단계는 [익스텐션 포인트](#익스텐션-포인트)에 노출된다.
[플러그인](#스케줄링-플러그인)은 이러한 익스텐션 포인트 중
하나 이상을 구현하여 스케줄링 동작을 제공한다.

`kube-scheduler` 의 단일 인스턴스를 구성하여
[여러 프로파일](#여러-프로파일)을 실행할 수 있다.

### 익스텐션 포인트

스케줄링은 다음 익스텐션 포인트를 통해 노출되는 일련의 단계에서
발생한다.

1. `QueueSort`: 이 플러그인은 스케줄링 대기열에서 보류 중인 파드를
   정렬하는 데 사용되는 정렬 기능을 제공한다. 대기열 정렬 플러그인은 한 번에 단 하나만 활성화될 수 있다.
   사용할 수 있다.
1. `PreFilter`: 이 플러그인은 필터링하기 전에 파드 또는 클러스터에 대한 정보를
   사전 처리하거나 확인하는 데 사용된다. 이 플러그인은 파드를 unschedulable로
   표시할 수 있다.
1. `Filter`: 이 플러그인은 스케줄링 정책의 단정(Predicates)과 동일하며
   파드를 실행할 수 없는 노드를 필터링하는 데 사용된다. 필터는
   구성된 순서대로 호출된다. 노드가 모든 필터를 통과하지 않으면 파드는 unschedulable로
   표시된다.
1. `PreScore`: 이것은 사전 스코어링 작업을 수행하는 데 사용할 수 있는
   정보성 익스텐션 포인트이다.
1. `Score`: 이 플러그인은 필터링 단계를 통과한 각 노드에 점수를
   제공한다. 그런 다음 스케줄러는 가중치 합계가 가장 높은
   노드를 선택한다.
1. `Reserve`: 지정된 파드에 리소스가 예약된 경우 플러그인에
   알리는 정보성 익스텐션 포인트이다. 플러그인은 또한
   `Reserve` 도중 또는 이후에 실패한 경우 호출 되는 `Unreserve` 호출을
   구현한다.
1. `Permit`: 이 플러그인은 파드 바인딩을 방지하거나 지연시킬 수 있다.
1. `PreBind`: 이 플러그인은 파드가 바인딩되기 전에 필요한 모든 작업을 수행한다.
1. `Bind`: 플러그인은 파드를 노드에 바인딩한다. Bind 플러그인은 순서대로 호출되며
   일단 바인딩이 완료되면 나머지 플러그인은 건너뛴다. Bind
   플러그인은 적어도 하나 이상 필요하다.
1. `PostBind`: 파드가 바인드된 후 호출되는
   정보성 익스텐션 포인트이다.

각 익스텐션 포인트에 대해 특정 [기본 플러그인](#스케줄링-플러그인)을 비활성화하거나
자체 플러그인을 활성화할 수 있다. 예를 들면, 다음과 같다.

```yaml
apiVersion: kubescheduler.config.k8s.io/v1beta1
kind: KubeSchedulerConfiguration
profiles:
  - plugins:
      score:
        disabled:
        - name: NodeResourcesLeastAllocated
        enabled:
        - name: MyCustomPluginA
          weight: 2
        - name: MyCustomPluginB
          weight: 1
```

비활성화된 배열의 이름으로 `*` 를 사용하여 해당 익스텐션 포인트에 대한
모든 기본 플러그인을 비활성화할 수 있다. 원하는 경우, 플러그인 순서를 재정렬하는 데
사용할 수도 있다.

### 스케줄링 플러그인

1. `UnReserve`: 파드가 예약된 후 거부되고 `Permit` 플러그인에 의해 보류된 경우
   호출되는 정보성 익스텐션 포인트이다.

## 스케줄링 플러그인

기본적으로 활성화된 다음의 플러그인은 이들 익스텐션 포인트 중
하나 이상을 구현한다.

- `SelectorSpread`: {{< glossary_tooltip text="서비스" term_id="service" >}},
  {{< glossary_tooltip text="레플리카셋(ReplicaSets)" term_id="replica-set" >}} 및
  {{< glossary_tooltip text="스테이트풀셋(StatefulSets)" term_id="statefulset" >}}에
  속하는 파드에 대해 노드 간 분산을 선호한다.
  익스텐션 포인트: `PreScore`, `Score`.
- `ImageLocality`: 파드가 실행하는 컨테이너 이미지가 이미 있는 노드를
  선호한다.
  익스텐션 포인트: `Score`.
- `TaintToleration`: [테인트(taint)와 톨러레이션(toleration)](/ko/docs/concepts/scheduling-eviction/taint-and-toleration/)을
  구현한다.
  익스텐션 포인트 구현: `Filter`, `Prescore`, `Score`.
- `NodeName`: 파드 명세 노드 이름이 현재 노드와 일치하는지 확인한다.
  익스텐션 포인트: `Filter`.
- `NodePorts`: 노드에 요청된 파드 포트에 대해 사용 가능한 포트가 있는지 확인한다.
  익스텐션 포인트: `PreFilter`, `Filter`.
- `NodePreferAvoidPods`: 노드 {{< glossary_tooltip text="어노테이션" term_id="annotation" >}}
  `scheduler.alpha.kubernetes.io/preferAvoidPods` 에 따라
  노드 점수를 매긴다.
  익스텐션 포인트: `Score`.
- `NodeAffinity`: [노드 셀렉터](/ko/docs/concepts/scheduling-eviction/assign-pod-node/#노드-셀렉터-nodeselector)와
  [노드 어피니티](/ko/docs/concepts/scheduling-eviction/assign-pod-node/#노드-어피니티)를
  구현한다.
  익스텐션 포인트: `Filter`, `Score`.
- `PodTopologySpread`: [파드 토폴로지 분배](/ko/docs/concepts/workloads/pods/pod-topology-spread-constraints/)를
  구현한다.
  익스텐션 포인트: `PreFilter`, `Filter`, `PreScore`, `Score`.
- `NodeUnschedulable`: `.spec.unschedulable` 이 true로 설정된 노드를
  필터링한다.
  익스텐션 포인트: `Filter`.
- `NodeResourcesFit`: 노드에 파드가 요청하는 모든 리소스가 있는지
  확인한다.
  익스텐션 포인트: `PreFilter`, `Filter`.
- `NodeResourcesBalancedAllocation`: 파드가 스케줄된 경우, 보다 균형잡힌 리소스 사용량을
  얻을 수 있는 노드를 선호한다.
  익스텐션 포인트: `Score`.
- `NodeResourcesLeastAllocated`: 리소스 할당이 적은 노드를
  선호한다.
  익스텐션 포인트: `Score`.
- `VolumeBinding`: 노드에 요청된 {{< glossary_tooltip text="볼륨" term_id="volume" >}}이 있는지
  또는 바인딩할 수 있는지 확인한다.
  익스텐션 포인트: `PreFilter`, `Filter`, `Reserve`, `PreBind`, `Score`.
  {{< note >}}
  `Score` 익스텐션 포인트는 `VolumeCapacityPriority` 기능이
  활성화되어 있어야 활성화되며,
  요청된 볼륨 사이즈를 만족하는 가장 작은 PV들을 우선순위 매긴다.
  {{< /note >}}
- `VolumeRestrictions`: 노드에 마운트된 볼륨이 볼륨 제공자에 특정한
  제한 사항을 충족하는지 확인한다.
  익스텐션 포인트: `Filter`.
- `VolumeZone`: 요청된 볼륨이 가질 수 있는 영역 요구 사항을 충족하는지
  확인한다.
  익스텐션 포인트: `Filter`.
- `NodeVolumeLimits`: 노드에 대해 CSI 볼륨 제한을 충족할 수 있는지
  확인한다.
  익스텐션 포인트: `Filter`.
- `EBSLimits`: 노드에 대해 AWS EBS 볼륨 제한을 충족할 수 있는지 확인한다.
  익스텐션 포인트: `Filter`.
- `GCEPDLimits`: 노드에 대해 GCP-PD 볼륨 제한을 충족할 수 있는지 확인한다.
  익스텐션 포인트: `Filter`.
- `AzureDiskLimits`: 노드에 대해 Azure 디스크 볼륨 제한을 충족할 수 있는지
  확인한다.
  익스텐션 포인트: `Filter`.
- `InterPodAffinity`: [파드 간 어피니티 및 안티-어피니티](/ko/docs/concepts/scheduling-eviction/assign-pod-node/#파드간-어피니티와-안티-어피니티)를
  구현한다.
  익스텐션 포인트: `PreFilter`, `Filter`, `PreScore`, `Score`.
- `PrioritySort`: 기본 우선 순위 기반 정렬을 제공한다.
  익스텐션 포인트: `QueueSort`.
- `DefaultBinder`: 기본 바인딩 메커니즘을 제공한다.
  익스텐션 포인트: `Bind`.
- `DefaultPreemption`: 기본 선점 메커니즘을 제공한다.
  익스텐션 포인트: `PostFilter`.

기본으로 활성화되지 않는 다음의 플러그인을
컴포넌트 구성 API를 통해 활성화할 수도 있다.

- `NodeResourcesMostAllocated`: 리소스 할당이 많은 노드를
  선호한다.
  익스텐션 포인트: `Score`.
- `RequestedToCapacityRatio`: 할당된 리소스의 구성된 기능에 따라 노드를
  선호한다.
  익스텐션 포인트: `Score`.
- `CinderVolume`: 노드에 대해 OpenStack Cinder 볼륨 제한을 충족할 수 있는지
  확인한다.
  익스텐션 포인트: `Filter`.
- `NodeLabel`: Filters and / or scores a node according to configured
  {{< glossary_tooltip text="label(s)" term_id="label" >}}.
  익스텐션 포인트: `Filter`, `Score`.
- `ServiceAffinity`: {{< glossary_tooltip text="서비스" term_id="service" >}}에
  속한 파드가 구성된 레이블로 정의된 노드 집합에 맞는지
  확인한다. 이 플러그인은 또한 서비스에 속한 파드를 노드 간에
  분산하는 것을 선호한다.
  익스텐션 포인트: `PreFilter`, `Filter`, `Score`.

### 여러 프로파일

둘 이상의 프로파일을 실행하도록 `kube-scheduler` 를 구성할 수 있다.
각 프로파일에는 연관된 스케줄러 이름이 있으며 [익스텐션 포인트](#익스텐션-포인트)에 구성된
다른 플러그인 세트를 가질 수 있다.

다음의 샘플 구성을 사용하면, 스케줄러는 기본 플러그인이 있는
프로파일과 모든 스코어링 플러그인이 비활성화된 프로파일의 두 가지 프로파일로
실행된다.

```yaml
apiVersion: kubescheduler.config.k8s.io/v1beta1
kind: KubeSchedulerConfiguration
profiles:
  - schedulerName: default-scheduler
  - schedulerName: no-scoring-scheduler
    plugins:
      preScore:
        disabled:
        - name: '*'
      score:
        disabled:
        - name: '*'
```

특정 프로파일에 따라 스케줄하려는 파드는
`.spec.schedulerName` 에 해당 스케줄러 이름을 포함할 수 있다.

기본적으로, 스케줄러 이름 `default-scheduler` 를 가진 하나의 프로파일이 생성된다.
이 프로파일에는 위에서 설명한 기본 플러그인이 포함되어 있다. 둘 이상의
프로파일을 선언할 때, 각각에 대한 고유한 스케줄러 이름이 필요하다.

파드가 스케줄러 이름을 지정하지 않으면, kube-apiserver는 이를 `default-scheduler` 로
설정한다. 따라서, 해당 파드를 스케줄하려면 이 스케줄러 이름을 가진 프로파일이
있어야 한다.

{{< note >}}
파드의 스케줄링 이벤트에는 ReportingController로 `.spec.schedulerName` 이 있다.
리더 선출을 위한 이벤트는 목록에서 첫 번째 프로파일의 스케줄러 이름을
사용한다.
{{< /note >}}

{{< note >}}
모든 프로파일은 QueueSort 익스텐션 포인트에서 동일한 플러그인을 사용해야 하며
동일한 구성 파라미터(해당하는 경우)를 가져야 한다. 그 이유는 스케줄러가 보류 중 상태인 파드 대기열을
단 하나만 가질 수 있기 때문이다.
{{< /note >}}

## {{% heading "whatsnext" %}}

* [kube-scheduler 레퍼런스](/docs/reference/command-line-tools-reference/kube-scheduler/) 읽어보기
* [스케줄링](/ko/docs/concepts/scheduling-eviction/kube-scheduler/)에 대해 알아보기
* [kube-scheduler configuration (v1beta1)](/docs/reference/config-api/kube-scheduler-config.v1beta1/) 레퍼런스 읽어보기
