---
title: 노드-압박 축출
content_type: concept
weight: 60
---

{{<glossary_definition term_id="node-pressure-eviction" length="short">}}</br>

{{<glossary_tooltip term_id="kubelet" text="kubelet">}}은 
클러스터 노드의 CPU, 메모리, 디스크 공간, 파일시스템 inode와 같은 자원을 모니터링한다.
이러한 자원 중 하나 이상이 특정 소모 수준에 도달하면, 
kubelet은 하나 이상의 파드를 능동적으로 중단시켜 
자원을 회수하고 고갈 상황을 방지할 수 있다.

노드-압박 축출 과정에서, kubelet은 축출할 파드의 `PodPhase`를 
`Failed`로 설정한다. 이로써 파드가 종료된다.

노드-압박 축출은 
[API를 이용한 축출](/ko/docs/concepts/scheduling-eviction/api-eviction/)과는 차이가 있다.

kubelet은 이전에 설정된 `PodDisruptionBudget` 값이나 파드의 `terminationGracePeriodSeconds` 값을 따르지 않는다. 
[소프트 축출 임계값](#soft-eviction-thresholds)을 사용하는 경우, 
kubelet은 이전에 설정된 `eviction-max-pod-grace-period` 값을 따른다. 
[하드 축출 임계값](#hard-eviction-thresholds)을 사용하는 경우, 파드 종료 시 `0s` 만큼 기다린 후 종료한다(즉, 기다리지 않고 바로 종료한다).

실패한 파드를 새로운 파드로 교체하는 
{{< glossary_tooltip text="워크로드" term_id="workload" >}} 리소스(예: 
{{< glossary_tooltip text="스테이트풀셋(StatefulSet)" term_id="statefulset" >}} 또는 
{{< glossary_tooltip text="디플로이먼트(Deployment)" term_id="deployment" >}})가 파드를 관리하는 경우, 
컨트롤 플레인이나 `kube-controller-manager`가 축출된 파드를 대신할 새 파드를 생성한다.

{{<note>}}
kubelet은 최종 사용자 파드를 종료하기 전에 
먼저 [노드 수준 자원을 회수](#reclaim-node-resources)하려고 시도한다. 
예를 들어, 디스크 자원이 부족하면 먼저 사용하지 않는 컨테이너 이미지를 제거한다.
{{</note>}}

kubelet은 축출 결정을 내리기 위해 다음과 같은 다양한 파라미터를 사용한다.

  * 축출 신호
  * 축출 임계값
  * 모니터링 간격

### 축출 신호 {#eviction-signals}

축출 신호는 특정 시점에서 특정 자원의 현재 상태이다. 
Kubelet은 노드에서 사용할 수 있는 리소스의 최소량인 
축출 임계값과 축출 신호를 비교하여 
축출 결정을 내린다.

Kubelet은 다음과 같은 축출 신호를 사용한다.

| 축출 신호      | 설명                                                                           |
|----------------------|---------------------------------------------------------------------------------------|
| `memory.available`   | `memory.available` := `node.status.capacity[memory]` - `node.stats.memory.workingSet` |
| `nodefs.available`   | `nodefs.available` := `node.stats.fs.available`                                       |
| `nodefs.inodesFree`  | `nodefs.inodesFree` := `node.stats.fs.inodesFree`                                     |
| `imagefs.available`  | `imagefs.available` := `node.stats.runtime.imagefs.available`                         |
| `imagefs.inodesFree` | `imagefs.inodesFree` := `node.stats.runtime.imagefs.inodesFree`                       |
| `pid.available`      | `pid.available` := `node.stats.rlimit.maxpid` - `node.stats.rlimit.curproc`           |

이 표에서, `설명` 열은 kubelet이 축출 신호 값을 계산하는 방법을 나타낸다. 
각 축출 신호는 백분율 또는 숫자값을 지원한다. 
kubelet은 총 용량 대비 축출 신호의 백분율 값을 
계산한다.

`memory.available` 값은 `free -m`과 같은 도구가 아니라 cgroupfs로부터 도출된다. 
이는 `free -m`이 컨테이너 안에서는 동작하지 않고, 또한 사용자가 
[node allocatable](/docs/tasks/administer-cluster/reserve-compute-resources/#node-allocatable) 
기능을 사용하는 경우 자원 부족에 대한 결정은 루트 노드뿐만 아니라 
cgroup 계층구조의 최종 사용자 파드 부분에서도 지역적으로 이루어지기 때문에 중요하다. 
[이 스크립트](/examples/admin/resource/memory-available.sh)는 
kubelet이 `memory.available`을 계산하기 위해 수행하는 동일한 단계들을 재현한다. 
kubelet은 메모리 압박 상황에서 메모리가 회수 가능하다고 가정하므로, 
inactive_file(즉, 비활성 LRU 목록의 파일 기반 메모리 바이트 수)을 
계산에서 제외한다.

kubelet은 다음과 같은 파일시스템 파티션을 지원한다.

1. `nodefs`: 노드의 메인 파일시스템이며, 로컬 디스크 볼륨, emptyDir, 
   로그 스토리지 등에 사용된다. 예를 들어 `nodefs`는 `/var/lib/kubelet/`을 포함한다.
1. `imagefs`: 컨테이너 런타임이 컨테이너 이미지 및 
   컨테이너 쓰기 가능 레이어를 저장하는 데 사용하는 선택적 파일시스템이다.

Kubelet은 이러한 파일 시스템을 자동으로 검색하고 다른 파일 시스템은 무시한다. 
Kubelet은 다른 구성은 지원하지 않는다.

{{<note>}}
일부 kubelet 가비지 수집 기능은 더 이상 사용되지 않으며 축출로 대체되었다.
사용 중지된 기능의 목록은 [kubelet 가비지 수집 사용 중단](/ko/docs/concepts/cluster-administration/kubelet-garbage-collection/#사용-중단-deprecation)을 참조한다.
{{</note>}}

### 축출 임계값

kubelet이 축출 결정을 내릴 때 사용하는 축출 임계값을 
사용자가 임의로 설정할 수 있다.

축출 임계값은 `[eviction-signal][operator][quantity]` 형태를 갖는다.

* `eviction-signal`에는 사용할 [축출 신호](#eviction-signals)를 적는다.
* `operator`에는 [관계연산자](https://ko.wikipedia.org/wiki/관계연산자#표준_관계연산자)를 
  적는다(예: `<` - 미만)
* `quantity`에는 `1Gi`와 같이 축출 임계값 수치를 적는다. 
  `quantity`에 들어가는 값은 쿠버네티스가 사용하는 수치 표현 방식과 맞아야 한다. 
  숫자값 또는 백분율(`%`)을 사용할 수 있다.

예를 들어, 노드에 총 `10Gi`의 메모리가 있고 
`1Gi` 아래로 내려갔을 때 축출이 시작되도록 만들고 싶으면, 축출 임계값을 
`memory.available<10%` 또는 `memory.available<1Gi` 형태로 정할 수 있다. 둘을 동시에 사용할 수는 없다.

소프트 축출 임계값과 하드 축출 임계값을 설정할 수 있다.

#### 소프트 축출 임계값 {#soft-eviction-thresholds}

소프트 축출 임계값은 관리자가 설정하는 유예 시간(필수)과 함께 정의된다. 
kubelet은 유예 시간이 초과될 때까지 파드를 제거하지 않는다. 
유예 시간이 지정되지 않으면 kubelet 시작 시 
오류가 반환된다.

kubelet이 축출 과정에서 사용할 수 있도록, 
'소프트 축출 임계값'과 '최대 허용 파드 종료 유예 시간' 둘 다를 설정할 수 있다. 
'최대 허용 파드 종료 유예 시간'이 설정되어 있는 상태에서 '소프트 축출 임계값'에 도달하면, 
kubelet은 두 유예 시간 중 작은 쪽을 적용한다. 
'최대 허용 파드 종료 유예 시간'을 설정하지 않으면, 
kubelet은 축출된 파드를 유예 시간 없이 즉시 종료한다.

소프트 축출 임계값을 설정할 때 다음과 같은 플래그를 사용할 수 있다.

* `eviction-soft`: 축출 임계값(예: `memory.available<1.5Gi`)의 집합이며, 
  지정된 유예 시간동안 이 축출 임계값 조건이 충족되면 파드 축출이 트리거된다.
* `eviction-soft-grace-period`: 축출 유예 시간의 집합이며, 
  소프트 축출 임계값 조건이 이 유예 시간동안 충족되면 파드 축출이 트리거된다.
* `eviction-max-pod-grace-period`: '최대 허용 파드 종료 유예 시간(단위: 초)'이며, 
  소프트 축출 임계값 조건이 충족되어 파드를 종료할 때 사용한다.

#### 하드 축출 임계값 {#hard-eviction-thresholds}

하드 축출 임계값에는 유예 시간이 없다. 하드 축출 임계값 조건이 충족되면, 
kubelet은 고갈된 자원을 회수하기 위해 파드를 유예 시간 없이 
즉시 종료한다.

`eviction-hard` 플래그를 사용하여 하드 축출 
임계값(예: `memory.available<1Gi`)을 설정할 수 있다.

kubelet은 다음과 같은 하드 축출 임계값을 기본적으로 설정하고 있다.

* `memory.available<100Mi`
* `nodefs.available<10%`
* `imagefs.available<15%`
* `nodefs.inodesFree<5%` (리눅스 노드)

### 축출 모니터링 시간 간격

kubelet은 `housekeeping-interval`에 설정된 시간 간격(기본값: `10s`)마다 
축출 임계값을 확인한다.

### 노드 컨디션 {#node-conditions}

kubelet은 하드/소프트 축출 임계값 조건이 충족되어 
노드 압박이 발생했다는 것을 알리기 위해, 
설정된 유예 시간과는 관계없이 노드 컨디션을 보고한다.

kubelet은 다음과 같이 노드 컨디션과 축출 신호를 매핑한다.

| 노드 컨디션    | 축출 신호                                                                       | 설명                                                                                                                  |
|-------------------|---------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------|
| `MemoryPressure`  | `memory.available`                                                                    | 노드의 가용 메모리 양이 축출 임계값에 도달했다                                                             |
| `DiskPressure`    | `nodefs.available`, `nodefs.inodesFree`, `imagefs.available`, or `imagefs.inodesFree` | 노드의 루트 파일시스템 또는 이미지 파일시스템의 가용 디스크 공간 또는 inode의 수가 축출 임계값에 도달했다 |
| `PIDPressure`     | `pid.available`                                                                       | (리눅스) 노드의 가용 프로세스 ID(PID)가 축출 임계값 이하로 내려왔다                                   |

kubelet은 `--node-status-update-frequency`에 설정된 
시간 간격(기본값: `10s`)마다 노드 컨디션을 업데이트한다.

#### 노드 컨디션 진동(oscillation)

경우에 따라, 노드의 축출 신호값이 사전에 설정된 유예 시간 동안 유지되지 않고 
소프트 축출 임계값을 중심으로 진동할 수 있다. 이로 인해 노드 컨디션이 계속 
`true`와 `false`로 바뀌며, 잘못된 축출 결정을 야기할 수 있다.

이러한 진동을 방지하기 위해, `eviction-pressure-transition-period` 플래그를 
사용하여 kubelet이 노드 컨디션을 다른 상태로 바꾸기 위해 기다려야 하는 시간을 
설정할 수 있다. 기본값은 `5m`이다.

### 노드-수준 자원 회수하기 {#reclaim-node-resources}

kubelet은 최종 사용자 파드를 축출하기 전에 노드-수준 자원 회수를 시도한다.

`DiskPressure` 노드 컨디션이 보고되면, 
kubelet은 노드의 파일시스템을 기반으로 노드-수준 자원을 회수한다.

#### `imagefs`가 있는 경우

컨테이너 런타임이 사용할 전용 `imagefs` 파일시스템이 노드에 있으면, 
kubelet은 다음 작업을 수행한다.

  * `nodefs` 파일시스템이 축출 임계값 조건을 충족하면, 
    kubelet은 종료된 파드와 컨테이너에 대해 가비지 수집을 수행한다.
  * `imagefs` 파일시스템이 축출 임계값 조건을 충족하면, 
    kubelet은 모든 사용중이지 않은 이미지를 삭제한다.

#### `imagefs`가 없는 경우

노드에 `nodefs` 파일시스템만 있고 이것이 축출 임계값 조건을 충족한 경우, 
kubelet은 다음 순서로 디스크 공간을 확보한다.

1. 종료된 파드와 컨테이너에 대해 가비지 수집을 수행한다
1. 사용중이지 않은 이미지를 삭제한다

### kubelet 축출을 위한 파드 선택

kubelet이 노드-수준 자원을 회수했음에도 축출 신호가 임계값 아래로 내려가지 않으면, 
kubelet은 최종 사용자 파드 축출을 시작한다.

kubelet은 파드 축출 순서를 결정하기 위해 다음의 파라미터를 활용한다.

1. 파드의 자원 사용량이 요청량을 초과했는지 여부
1. [파드 우선순위](/ko/docs/concepts/scheduling-eviction/pod-priority-preemption/)
1. 파드의 자원 요청량 대비 자원 사용량

결과적으로, kubelet은 다음과 같은 순서로 파드의 축출 순서를 정하고 축출을 수행한다.

1. `BestEffort` 또는 `Burstable` 파드 중 자원 사용량이 요청량을 초과한 파드. 
   이 파드들은 파드들의 우선순위, 그리고 자원 사용량이 요청량을 
   얼마나 초과했는지에 따라 축출된다.
1. `Guaranteed`, `Burstable` 파드 중 자원 사용량이 요청량보다 낮은 파드는 
   우선순위에 따라 후순위로 축출된다.

{{<note>}}
kubelet이 파드 축출 순서를 결정할 때 파드의 QoS 클래스는 이용하지 않는다. 
메모리 등의 자원을 회수할 때, QoS 클래스를 이용하여 가장 가능성이 높은 파드 축출 순서를 예측할 수는 있다. 
QoS는 EphemeralStorage 요청에 적용되지 않으므로, 
노드가 예를 들어 'DiskPressure' 아래에 있는 경우 위의 시나리오가 적용되지 않는다.
{{</note>}}

`Guaranteed` 파드는 모든 컨테이너에 대해 자원 요청량과 제한이 명시되고 
그 둘이 동일할 때에만 보장(guaranteed)된다. 다른 파드의 자원 사용으로 인해 
`Guaranteed` 파드가 축출되는 일은 발생하지 않는다. 만약 시스템 데몬(예: 
`kubelet`, `docker`, `journald`)이 `system-reserved` 또는 `kube-reserved` 
할당을 통해 예약된 것보다 더 많은 자원을 소비하고, 노드에는 요청량보다 적은 양의 
자원을 사용하고 있는 `Guaranteed` / `Burstable` 파드만 존재한다면, 
kubelet은 노드 안정성을 유지하고 자원 고갈이 다른 파드에 미칠 영향을 통제하기 위해 
이러한 파드 중 하나를 골라 축출해야 한다. 
이 경우, 가장 낮은 `Priority`를 갖는 파드가 선택된다.

`inodes`와 `PIDs`에 대한 요청량은 정의하고 있지 않기 때문에, kubelet이 `inode` 
또는 `PID` 고갈 때문에 파드를 축출할 때에는 파드의 `Priority`를 이용하여 축출 
순위를 정한다.

노드에 전용 'imagefs' 파일 시스템이 있는지 여부에 따라 kubelet이 파드 축출 순서를 
정하는 방식에 차이가 있다.

#### `imagefs`가 있는 경우

`nodefs`로 인한 축출의 경우, kubelet은 `nodefs` 
사용량(`모든 컨테이너의 로컬 볼륨 + 로그`)을 기준으로 축출 순서를 정한다.

`imagefs`로 인한 축출의 경우, kubelet은 모든 컨테이너의 
쓰기 가능한 레이어(writable layer) 사용량을 기준으로 축출 순서를 정한다.

#### `imagefs`가 없는 경우

`nodefs`로 인한 축출의 경우, kubelet은 각 파드의 총 
디스크 사용량(`모든 컨테이너의 로컬 볼륨 + 로그 + 쓰기 가능한 레이어`)을 기준으로 축출 순서를 정한다.

### 최소 축출 회수량

경우에 따라, 파드를 축출했음에도 적은 양의 자원만이 회수될 수 있다. 
이로 인해 kubelet이 반복적으로 축출 임계값 도달을 감지하고 
여러 번의 축출을 수행할 수 있다.

`--eviction-minimum-reclaim` 플래그 또는 
[kubelet 설정 파일](/docs/tasks/administer-cluster/kubelet-config-file/)을 이용하여 
각 자원에 대한 최소 회수량을 설정할 수 있다. kubelet이 자원 부족 상황을 감지하면, 
앞서 설정한 최소 회수량에 도달할때까지 회수를 계속 진행한다.

예를 들어, 다음 YAML은 최소 회수량을 정의하고 있다.

```yaml
apiVersion: kubelet.config.k8s.io/v1beta1
kind: KubeletConfiguration
evictionHard:
  memory.available: "500Mi"
  nodefs.available: "1Gi"
  imagefs.available: "100Gi"
evictionMinimumReclaim:
  memory.available: "0Mi"
  nodefs.available: "500Mi"
  imagefs.available: "2Gi"
```

이 예제에서, 만약 `nodefs.available` 축출 신호가 축출 임계값 조건에 도달하면, 
kubelet은 축출 신호가 임계값인 `1Gi`에 도달할 때까지 자원을 회수하며, 
이어서 축출 신호가 `1.5Gi`에 도달할 때까지 최소 `500Mi` 이상의 자원을 
회수한다.

유사한 방식으로, kubelet은 `imagefs.available` 축출 신호가 
`102Gi`에 도달할 때까지 `imagefs` 자원을 회수한다.

모든 자원에 대해 `eviction-minimum-reclaim`의 기본값은 `0`이다.

### 노드 메모리 부족 시의 동작

kubelet의 메모리 회수가 가능하기 이전에 
노드에 메모리 부족(out of memory, 이하 OOM) 이벤트가 발생하면, 
노드는 [oom_killer](https://lwn.net/Articles/391222/)에 의존한다.

kubelet은 각 파드에 설정된 QoS를 기반으로 각 컨테이너에 `oom_score_adj` 값을 설정한다.

| Quality of Service | oom_score_adj                                                                     |
|--------------------|-----------------------------------------------------------------------------------|
| `Guaranteed`       | -997                                                                              |
| `BestEffort`       | 1000                                                                              |
| `Burstable`        | min(max(2, 1000 - (1000 * memoryRequestBytes) / machineMemoryCapacityBytes), 999) |

{{<note>}}
또한, kubelet은 `system-node-critical` {{<glossary_tooltip text="Priority" term_id="pod-priority">}}를 갖는 파드의 컨테이너에 
`oom_score_adj` 값을 `-997`로 설정한다.
{{</note>}}

노드가 OOM을 겪기 전에 kubelet이 메모리를 회수하지 못하면, `oom_killer`가 노드의 
메모리 사용률 백분율을 이용하여 `oom_score`를 계산하고, 각 컨테이너의 실질 
`oom_score`를 구하기 위해 `oom_score_adj`를 더한다. 그 뒤 `oom_score`가 가장 높은 
컨테이너부터 종료시킨다.

이는 곧, 스케줄링 요청에 비해 많은 양의 메모리를 사용하면서 
QoS가 낮은 파드에 속한 컨테이너가 먼저 종료됨을 의미한다.

파드 축출과 달리, 컨테이너가 OOM으로 인해 종료되면, 
`kubelet`이 컨테이너의 `RestartPolicy`를 기반으로 컨테이너를 다시 실행할 수 있다.

### 추천 예시 {#node-pressure-eviction-good-practices}

아래 섹션에서 축출 설정에 대한 추천 예시를 소개한다.

#### 스케줄 가능한 자원과 축출 정책

kubelet에 축출 정책을 설정할 때, 만약 어떤 파드 배치가 즉시 메모리 압박을 
야기하기 때문에 축출을 유발한다면 스케줄러가 그 파드 배치를 수행하지 않도록 
설정해야 한다. 

다음 시나리오를 가정한다.

* 노드 메모리 용량: `10Gi`
* 운영자는 시스템 데몬(커널, `kubelet` 등)을 위해 메모리 용량의 10%를 확보해 놓고 싶어 한다.
* 운영자는 시스템 OOM 발생을 줄이기 위해 메모리 사용률이 95%인 상황에서 파드를 축출하고 싶어한다.

이것이 실현되도록, kubelet이 다음과 같이 실행된다.

```
--eviction-hard=memory.available<500Mi
--system-reserved=memory=1.5Gi
```

이 환경 설정에서, `--system-reserved` 플래그는 시스템 용으로 `1.5Gi` 메모리를 
확보하는데, 이는 `총 메모리의 10% + 축출 임계값`에 해당된다.

파드가 요청량보다 많은 메모리를 사용하거나 시스템이 `1Gi` 이상의 메모리를 
사용하여, `memory.available` 축출 신호가 `500Mi` 아래로 내려가면 노드가 축출 
임계값에 도달할 수 있다.

#### 데몬셋(DaemonSet)

파드 우선 순위(Priority)는 파드 축출 결정을 내릴 때의 주요 요소이다. 
kubelet이 `DaemonSet`에 속하는 파드를 축출하지 않도록 하려면 
해당 파드의 파드 스펙에 충분히 높은 `priorityClass`를 지정한다. 
또는 낮은 `priorityClass`나 기본값을 사용하여 
리소스가 충분할 때만 `DaemonSet` 파드가 실행되도록 허용할 수도 있다.

### 알려진 이슈

다음 섹션에서는 리소스 부족 처리와 관련된 알려진 이슈에 대해 다룬다.

#### kubelet이 메모리 압박을 즉시 감지하지 못할 수 있음

기본적으로 kubelet은 'cAdvisor'를 폴링하여 
일정한 간격으로 메모리 사용량 통계를 수집한다. 
해당 타임 윈도우 내에서 메모리 사용량이 빠르게 증가하면 kubelet이 
`MemoryPressure`를 충분히 빠르게 감지하지 못해 `OOMKiller`가 계속 호출될 수 있다.

`--kernel-memcg-notification` 플래그를 사용하여 
kubelet의 `memcg` 알림 API가 임계값을 초과할 때 즉시 알림을 받도록 
할 수 있다.

극도의 활용도를 달성하려는 것이 아니라 오버커밋에 대한 합리적인 조치를 원하는 경우, 
이 문제에 대한 현실적인 해결 방법은 `--kube-reserved` 및 
`--system-reserved` 플래그를 사용하여 시스템에 메모리를 할당하는 것이다.

#### `active_file` 메모리가 사용 가능한 메모리로 간주되지 않음

리눅스에서, 커널은 활성 LRU 목록의 파일 지원 메모리 바이트 수를 `active_file` 
통계로 추적한다. kubelet은 `active_file` 메모리 영역을 회수할 수 없는 것으로 
취급한다. 임시 로컬 스토리지를 포함하여 블록 지원 로컬 스토리지를 집중적으로 
사용하는 워크로드의 경우 파일 및 블록 데이터의 커널 수준 캐시는 최근에 액세스한 
많은 캐시 페이지가 `active_file`로 계산될 가능성이 있음을 의미한다. 활성 LRU 
목록에 이러한 커널 블록 버퍼가 충분히 많으면, kubelet은 이를 높은 자원 사용 
상태로 간주하고 노드가 메모리 압박을 겪고 있다고 테인트를 표시할 수 있으며, 이는 
파드 축출을 유발한다.

더 자세한 사항은 [https://github.com/kubernetes/kubernetes/issues/43916](https://github.com/kubernetes/kubernetes/issues/43916)를 참고한다.

집중적인 I/O 작업을 수행할 가능성이 있는 컨테이너에 대해 메모리 제한량 및 메모리 
요청량을 동일하게 설정하여 이 문제를 해결할 수 있다. 해당 컨테이너에 대한 최적의 
메모리 제한량을 추정하거나 측정해야 한다.

## {{% heading "whatsnext" %}}

* [API를 이용한 축출](/ko/docs/concepts/scheduling-eviction/api-eviction/)에 대해 알아본다.
* [파드 우선순위와 선점](/ko/docs/concepts/scheduling-eviction/pod-priority-preemption/)에 대해 알아본다.
* [PodDisruptionBudgets](/docs/tasks/run-application/configure-pdb/)에 대해 알아본다.
* [서비스 품질](/ko/docs/tasks/configure-pod-container/quality-service-pod/)(QoS)에 대해 알아본다.
* [축출 API](/docs/reference/generated/kubernetes-api/{{<param "version">}}/#create-eviction-pod-v1-core)를 확인한다.
