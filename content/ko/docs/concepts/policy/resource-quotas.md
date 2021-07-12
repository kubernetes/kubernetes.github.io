---


title: 리소스 쿼터
content_type: concept
weight: 20
---

<!-- overview -->

여러 사용자나 팀이 정해진 수의 노드로 클러스터를 공유할 때
한 팀이 공정하게 분배된 리소스보다 많은 리소스를 사용할 수 있다는 우려가 있다.

리소스 쿼터는 관리자가 이 문제를 해결하기 위한 도구이다.

<!-- body -->

`ResourceQuota` 오브젝트로 정의된 리소스 쿼터는 네임스페이스별 총 리소스 사용을 제한하는
제약 조건을 제공한다. 유형별로 네임스페이스에서 만들 수 있는 오브젝트 수와
해당 네임스페이스의 리소스가 사용할 수 있는 총 컴퓨트 리소스의 양을
제한할 수 있다.

리소스 쿼터는 다음과 같이 작동한다.

- 다른 팀은 다른 네임스페이스에서 작동한다. 현재 이것은 자발적이지만 ACL을 통해 이 필수 사항을
  적용하기 위한 지원이 계획되어 있다.

- 관리자는 각 네임스페이스에 대해 하나의 리소스쿼터를 생성한다.

- 사용자는 네임스페이스에서 리소스(파드, 서비스 등)를 생성하고 쿼터 시스템은
  사용량을 추적하여 리소스쿼터에 정의된 하드(hard) 리소스 제한을 초과하지 않도록 한다.

- 리소스를 생성하거나 업데이트할 때 쿼터 제약 조건을 위반하면 위반된 제약 조건을 설명하는
  메시지와 함께 HTTP 상태 코드 `403 FORBIDDEN`으로 요청이 실패한다.

- `cpu`, `memory`와 같은 컴퓨트 리소스에 대해 네임스페이스에서 쿼터가 활성화된 경우
  사용자는 해당값에 대한 요청 또는 제한을 지정해야 한다. 그렇지 않으면 쿼터 시스템이
  파드 생성을 거부할 수 있다. 힌트: 컴퓨트 리소스 요구 사항이 없는 파드를 기본값으로 설정하려면 `LimitRanger` 어드미션 컨트롤러를 사용하자.

  이 문제를 회피하는 방법에 대한 예제는
  [연습](/ko/docs/tasks/administer-cluster/manage-resources/quota-memory-cpu-namespace/)을 참고하길 바란다.

리소스쿼터 오브젝트의 이름은 유효한
[DNS 서브도메인 이름](/ko/docs/concepts/overview/working-with-objects/names#dns-서브도메인-이름)이어야 한다.

네임스페이스와 쿼터를 사용하여 만들 수 있는 정책의 예는 다음과 같다.

- 용량이 32GiB RAM, 16 코어인 클러스터에서 A 팀이 20GiB 및 10 코어를 사용하고
  B 팀은 10GiB 및 4 코어를 사용하게 하고 2GiB 및 2 코어를 향후 할당을 위해 보유하도록 한다.
- "testing" 네임스페이스를 1 코어 및 1GiB RAM을 사용하도록 제한한다.
  "production" 네임스페이스에는 원하는 양을 사용하도록 한다.

클러스터의 총 용량이 네임스페이스의 쿼터 합보다 작은 경우 리소스에 대한 경합이 있을 수 있다.
이것은 선착순으로 처리된다.

경합이나 쿼터 변경은 이미 생성된 리소스에 영향을 미치지 않는다.

## 리소스 쿼터 활성화

많은 쿠버네티스 배포판에 기본적으로 리소스 쿼터 지원이 활성화되어 있다.
{{< glossary_tooltip text="API 서버" term_id="kube-apiserver" >}} 
`--enable-admission-plugins=` 플래그의 인수 중 하나로
`ResourceQuota`가 있는 경우 활성화된다.

해당 네임스페이스에 리소스쿼터가 있는 경우 특정 네임스페이스에
리소스 쿼터가 적용된다.

## 컴퓨트 리소스 쿼터

지정된 네임스페이스에서 요청할 수 있는 총 
[컴퓨트 리소스](/ko/docs/concepts/configuration/manage-resources-containers/) 
합을 제한할 수 있다.

다음과 같은 리소스 유형이 지원된다.

| 리소스 이름 | 설명        |
| --------------------- | ----------------------------------------------------------- |
| `limits.cpu` | 터미널이 아닌 상태의 모든 파드에서 CPU 제한의 합은 이 값을 초과할 수 없음. |
| `limits.memory` | 터미널이 아닌 상태의 모든 파드에서 메모리 제한의 합은 이 값을 초과할 수 없음. |
| `requests.cpu` | 터미널이 아닌 상태의 모든 파드에서 CPU 요청의 합은 이 값을 초과할 수 없음. |
| `requests.memory` | 터미널이 아닌 상태의 모든 파드에서 메모리 요청의 합은 이 값을 초과할 수 없음. |
| `hugepages-<size>` | 터미널 상태가 아닌 모든 파드에 걸쳐서, 지정된 사이즈의 휴즈 페이지 요청은 이 값을 초과하지 못함. |
| `cpu` | `requests.cpu` 와 같음. |
| `memory` | `requests.memory` 와 같음. |

### 확장된 리소스에 대한 리소스 쿼터

위에서 언급한 리소스 외에도 릴리스 1.10에서는
[확장된 리소스](/ko/docs/concepts/configuration/manage-resources-containers/#확장된-리소스)에 대한 쿼터 지원이 추가되었다.

확장된 리소스에는 오버커밋(overcommit)이 허용되지 않으므로 하나의 쿼터에서
동일한 확장된 리소스에 대한 `requests`와 `limits`을 모두 지정하는 것은 의미가 없다. 따라서 확장된
리소스의 경우 지금은 접두사 `requests.`이 있는 쿼터 항목만 허용된다.

예를 들어, 리소스 이름이 `nvidia.com/gpu`이고 네임스페이스에서 요청된 총 GPU 수를 4개로 제한하려는 경우,
GPU 리소스를 다음과 같이 쿼터를 정의할 수 있다.

* `requests.nvidia.com/gpu: 4`

자세한 내용은 [쿼터 보기 및 설정](#쿼터-보기-및-설정)을 참고하길 바란다.


## 스토리지 리소스 쿼터

지정된 네임스페이스에서 요청할 수 있는 총 [스토리지 리소스](/ko/docs/concepts/storage/persistent-volumes/) 합을 제한할 수 있다.

또한 연관된 ​​스토리지 클래스를 기반으로 스토리지 리소스 사용을 제한할 수 있다.

| 리소스 이름 | 설명        |
| --------------------- | ----------------------------------------------------------- |
| `requests.storage` | 모든 퍼시스턴트 볼륨 클레임에서 스토리지 요청의 합은 이 값을 초과할 수 없음 |
| `persistentvolumeclaims` | 네임스페이스에 존재할 수 있는 총 [퍼시스턴트 볼륨 클레임](/ko/docs/concepts/storage/persistent-volumes/#퍼시스턴트볼륨클레임) 수 |
| `<storage-class-name>.storageclass.storage.k8s.io/requests.storage` | storage-class-name과 관련된 모든 퍼시스턴트 볼륨 클레임에서 스토리지 요청의 합은 이 값을 초과할 수 없음 |
| `<storage-class-name>.storageclass.storage.k8s.io/persistentvolumeclaims` | `<storage-class-name>` 과 관련된 모든 퍼시스턴트 볼륨 클레임에서 네임스페이스에 존재할 수 있는 총 [퍼시스턴트 볼륨 클레임](/ko/docs/concepts/storage/persistent-volumes/#퍼시스턴트볼륨클레임) 수 |

예를 들어, 운영자가 `bronze` 스토리지 클래스와 별도로 `gold` 스토리지 클래스를 사용하여 스토리지에 쿼터를 지정하려는 경우 운영자는 다음과 같이
쿼터를 정의할 수 있다.

* `gold.storageclass.storage.k8s.io/requests.storage: 500Gi`
* `bronze.storageclass.storage.k8s.io/requests.storage: 100Gi`

릴리스 1.8에서는 로컬 임시 스토리지에 대한 쿼터 지원이 알파 기능으로 추가되었다.

| 리소스 이름 | 설명 |
| ------------------------------- |----------------------------------------------------------- |
| `requests.ephemeral-storage` | 네임스페이스의 모든 파드에서 로컬 임시 스토리지 요청의 합은 이 값을 초과할 수 없음. |
| `limits.ephemeral-storage` | 네임스페이스의 모든 파드에서 로컬 임시 스토리지 제한의 합은 이 값을 초과할 수 없음. |
| `ephemeral-storage` | `requests.ephemeral-storage` 와 같음. |

{{< note >}}
CRI 컨테이너 런타임을 사용할 때, 컨테이너 로그는 임시 스토리지 쿼터에 포함된다. 
이로 인해 스토리지 쿼터를 소진한 파드가 예기치 않게 축출될 수 있다. 
자세한 내용은 [로깅 아키텍처](/ko/docs/concepts/cluster-administration/logging/)를 참조한다.
{{< /note >}}

## 오브젝트 수 쿼터

다음 구문을 사용하여 모든 표준 네임스페이스 처리된(namespaced) 리소스 유형에 대한
특정 리소스 전체 수에 대하여 쿼터를 지정할 수 있다.

* 코어 그룹이 아닌(non-core) 리소스를 위한 `count/<resource>.<group>`
* 코어 그룹의 리소스를 위한 `count/<resource>`

다음은 사용자가 오브젝트 수 쿼터 아래에 배치하려는 리소스 셋의 예이다.

* `count/persistentvolumeclaims`
* `count/services`
* `count/secrets`
* `count/configmaps`
* `count/replicationcontrollers`
* `count/deployments.apps`
* `count/replicasets.apps`
* `count/statefulsets.apps`
* `count/jobs.batch`
* `count/cronjobs.batch`

사용자 정의 리소스를 위해 동일한 구문을 사용할 수 있다.
예를 들어 `example.com` API 그룹에서 `widgets` 사용자 정의 리소스에 대한 쿼터를 생성하려면 `count/widgets.example.com`을 사용한다.

`count/*` 리소스 쿼터를 사용할 때 서버 스토리지 영역에 있다면 오브젝트는 쿼터에 대해 과금된다.
이러한 유형의 쿼터는 스토리지 리소스 고갈을 방지하는 데 유용하다. 예를 들어,
크기가 큰 서버에서 시크릿 수에 쿼터를 지정할 수 있다. 클러스터에 시크릿이 너무 많으면 실제로 서버와
컨트롤러가 시작되지 않을 수 있다. 잘못 구성된 크론 잡으로부터의 보호를 위해
잡의 쿼터를 설정할 수 있다. 네임스페이스 내에서 너무 많은 잡을 생성하는 크론 잡은 서비스 거부를 유발할 수 있다.

또한 제한된 리소스 셋에 대해서 일반 오브젝트 수(generic object count) 쿼터를 적용하는 것도 가능하다.
다음 유형이 지원된다.

| 리소스 이름 | 설명 |
| ------------------------------- | ------------------------------------------------- |
| `configmaps` | 네임스페이스에 존재할 수 있는 총 컨피그맵 수 |
| `persistentvolumeclaims` | 네임스페이스에 존재할 수 있는 총 [퍼시스턴트 볼륨 클레임](/ko/docs/concepts/storage/persistent-volumes/#퍼시스턴트볼륨클레임) 수 |
| `pods` | 네임스페이스에 존재할 수 있는 터미널이 아닌 상태의 파드의 총 수. `.status.phase in (Failed, Succeeded)`가 true인 경우 파드는 터미널 상태임  |
| `replicationcontrollers` | 네임스페이스에 존재할 수 있는 총 레플리케이션컨트롤러 수 |
| `resourcequotas` | 네임스페이스에 존재할 수 있는 총 리소스쿼터 수 |
| `services` | 네임스페이스에 존재할 수 있는 총 서비스 수 |
| `services.loadbalancers` | 네임스페이스에 존재할 수 있는 `LoadBalancer` 유형의 총 서비스 수 |
| `services.nodeports` | 네임스페이스에 존재할 수 있는 `NodePort` 유형의 총 서비스 수 |
| `secrets` | 네임스페이스에 존재할 수 있는 총 시크릿 수 |

예를 들어, `pods` 쿼터는 터미널이 아닌 단일 네임스페이스에서 생성된 `pods` 수를
계산하고 최댓값을 적용한다. 사용자가 작은 파드를 많이 생성하여 클러스터의 파드 IP
공급이 고갈되는 경우를 피하기 위해 네임스페이스에
`pods` 쿼터를 설정할 수 있다.

## 쿼터 범위

각 쿼터에는 연결된 `scopes` 셋이 있을 수 있다. 쿼터는 열거된 범위의 교차 부분과 일치하는 경우에만
리소스 사용량을 측정한다.

범위가 쿼터에 추가되면 해당 범위와 관련된 리소스를 지원하는 리소스 수가 제한된다.
허용된 셋 이외의 쿼터에 지정된 리소스는 유효성 검사 오류가 발생한다.

| 범위 | 설명 |
| ----- | ----------- |
| `Terminating` | `.spec.activeDeadlineSeconds >= 0`에 일치하는 파드 |
| `NotTerminating` | `.spec.activeDeadlineSeconds is nil`에 일치하는 파드 |
| `BestEffort` | 최상의 서비스 품질을 제공하는 파드 |
| `NotBestEffort` | 서비스 품질이 나쁜 파드 |
| `PriorityClass` | 지정된 [프라이어리티클래스](/ko/docs/concepts/scheduling-eviction/pod-priority-preemption/)를 참조하여 일치하는 파드. |
| `CrossNamespacePodAffinity` | 크로스-네임스페이스 파드 [(안티)어피니티 용어]가 있는 파드 |

`BestEffort` 범위는 다음의 리소스를 추적하도록 쿼터를 제한한다.

* `pods`

`Terminating`, `NotTerminating`, `NotBestEffort` 및 `PriorityClass`
범위는 쿼터를 제한하여 다음의 리소스를 추적한다.

* `pods`
* `cpu`
* `memory`
* `requests.cpu`
* `requests.memory`
* `limits.cpu`
* `limits.memory`

`Terminating` 과 `NotTerminating` 범위를 동일한 쿼터 내에 모두
명시하지는 못하며, 마찬가지로 `BestEffort` 와
`NotBestEffort` 범위도 동일한 쿼터 내에서 모두 명시하지는 못한다.

`scopeSelector` 는 `operator` 필드에 다음의 값을 지원한다.

* `In`
* `NotIn`
* `Exists`
* `DoesNotExist`

`scopeSelector` 를 정의할 때, `scopeName` 으로 다음의 값 중 하나를 사용하는
경우, `operator` 는 `Exists` 이어야 한다.

* `Terminating`
* `NotTerminating`
* `BestEffort`
* `NotBestEffort`

만약 `operator` 가 `In` 또는 `NotIn` 인 경우, `values` 필드는 적어도 하나의 값은
가져야 한다. 예를 들면 다음과 같다.

```yaml
  scopeSelector:
    matchExpressions:
      - scopeName: PriorityClass
        operator: In
        values:
          - middle
```

만약 `operator` 가 `Exists` 또는 `DoesNotExist` 이라면, `values` 필드는 명시되면
*안된다*.

### PriorityClass별 리소스 쿼터

{{< feature-state for_k8s_version="v1.17" state="stable" >}}

특정 [우선 순위](/ko/docs/concepts/scheduling-eviction/pod-priority-preemption/#파드-우선순위)로 파드를 생성할 수 있다.
쿼터 스펙의 `scopeSelector` 필드를 사용하여 파드의 우선 순위에 따라 파드의 시스템 리소스 사용을
제어할 수 있다.

쿼터 스펙의 `scopeSelector`가 파드를 선택한 경우에만 쿼터가 일치하고 사용된다.

`scopeSelector` 필드를 사용하여 우선 순위 클래스의 쿼터 범위를 지정하면, 
쿼터 오브젝트는 다음의 리소스만 추적하도록 제한된다.

* `pods`
* `cpu`
* `memory`
* `ephemeral-storage`
* `limits.cpu`
* `limits.memory`
* `limits.ephemeral-storage`
* `requests.cpu`
* `requests.memory`
* `requests.ephemeral-storage`

이 예에서는 쿼터 오브젝트를 생성하여 특정 우선 순위의 파드와 일치시킨다.
예제는 다음과 같이 작동한다.

- 클러스터의 파드는 "low(낮음)", "medium(중간)", "high(높음)"의 세 가지 우선 순위 클래스 중 하나를 가진다.
- 각 우선 순위마다 하나의 쿼터 오브젝트가 생성된다.

다음 YAML을 `quota.yml` 파일에 저장한다.

```yaml
apiVersion: v1
kind: List
items:
- apiVersion: v1
  kind: ResourceQuota
  metadata:
    name: pods-high
  spec:
    hard:
      cpu: "1000"
      memory: 200Gi
      pods: "10"
    scopeSelector:
      matchExpressions:
      - operator : In
        scopeName: PriorityClass
        values: ["high"]
- apiVersion: v1
  kind: ResourceQuota
  metadata:
    name: pods-medium
  spec:
    hard:
      cpu: "10"
      memory: 20Gi
      pods: "10"
    scopeSelector:
      matchExpressions:
      - operator : In
        scopeName: PriorityClass
        values: ["medium"]
- apiVersion: v1
  kind: ResourceQuota
  metadata:
    name: pods-low
  spec:
    hard:
      cpu: "5"
      memory: 10Gi
      pods: "10"
    scopeSelector:
      matchExpressions:
      - operator : In
        scopeName: PriorityClass
        values: ["low"]
```

`kubectl create`를 사용하여 YAML을 적용한다.

```shell
kubectl create -f ./quota.yml
```

```
resourcequota/pods-high created
resourcequota/pods-medium created
resourcequota/pods-low created
```

`kubectl describe quota`를 사용하여 `Used` 쿼터가 `0`인지 확인하자.

```shell
kubectl describe quota
```

```
Name:       pods-high
Namespace:  default
Resource    Used  Hard
--------    ----  ----
cpu         0     1k
memory      0     200Gi
pods        0     10


Name:       pods-low
Namespace:  default
Resource    Used  Hard
--------    ----  ----
cpu         0     5
memory      0     10Gi
pods        0     10


Name:       pods-medium
Namespace:  default
Resource    Used  Hard
--------    ----  ----
cpu         0     10
memory      0     20Gi
pods        0     10
```

우선 순위가 "high"인 파드를 생성한다. 다음 YAML을
`high-priority-pod.yml` 파일에 저장한다.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: high-priority
spec:
  containers:
  - name: high-priority
    image: ubuntu
    command: ["/bin/sh"]
    args: ["-c", "while true; do echo hello; sleep 10;done"]
    resources:
      requests:
        memory: "10Gi"
        cpu: "500m"
      limits:
        memory: "10Gi"
        cpu: "500m"
  priorityClassName: high
```

`kubectl create`로 적용하자.

```shell
kubectl create -f ./high-priority-pod.yml
```

"high" 우선 순위 쿼터가 적용된 `pods-high`에 대한 "Used" 통계가 변경되었고
다른 두 쿼터는 변경되지 않았는지 확인한다.

```shell
kubectl describe quota
```

```
Name:       pods-high
Namespace:  default
Resource    Used  Hard
--------    ----  ----
cpu         500m  1k
memory      10Gi  200Gi
pods        1     10


Name:       pods-low
Namespace:  default
Resource    Used  Hard
--------    ----  ----
cpu         0     5
memory      0     10Gi
pods        0     10


Name:       pods-medium
Namespace:  default
Resource    Used  Hard
--------    ----  ----
cpu         0     10
memory      0     20Gi
pods        0     10
```

### 네임스페이스 간 파드 어피니티 쿼터

{{< feature-state for_k8s_version="v1.21" state="alpha" >}}

오퍼레이터는 네임스페이스를 교차하는 어피니티가 있는 파드를 가질 수 있는 네임스페이스를
제한하기 위해 `CrossNamespacePodAffinity` 쿼터 범위를 사용할 수 있다. 특히, 파드 어피니티 용어의
`namespaces` 또는 `namespaceSelector` 필드를 설정할 수 있는 파드를 제어한다.

안티-어피니티 제약 조건이 있는 파드는 장애 도메인에서 다른 모든 네임스페이스의 파드가 예약되지 않도록
차단할 수 있으므로 사용자가 네임스페이스 간 어피니티 용어를
사용하지 못하도록 하는 것이 바람직할 수 있다.

이 범위 오퍼레이터를 사용하면 `CrossNamespaceAffinity` 범위와 하드(hard) 제한이 0인
네임스페이스에 리소스 쿼터 오브젝트를 생성하여 특정 네임스페이스(아래 예에서 `foo-ns`)가 네임스페이스 간 파드 어피니티를
사용하는 파드를 사용하지 못하도록 방지할 수 있다.

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: disable-cross-namespace-affinity
  namespace: foo-ns
spec:
  hard:
    pods: "0"
  scopeSelector:
    matchExpressions:
    - scopeName: CrossNamespaceAffinity
```

오퍼레이터가 기본적으로 `namespaces` 및 `namespaceSelector` 사용을 허용하지 않고,
특정 네임스페이스에만 허용하려는 경우, kube-apiserver 플래그 --admission-control-config-file를
다음의 구성 파일의 경로로 설정하여 `CrossNamespaceAffinity` 를
제한된 리소스로 구성할 수 있다.

```yaml
apiVersion: apiserver.config.k8s.io/v1
kind: AdmissionConfiguration
plugins:
- name: "ResourceQuota"
  configuration:
    apiVersion: apiserver.config.k8s.io/v1
    kind: ResourceQuotaConfiguration
    limitedResources:
    - resource: pods
      matchScopes:
      - scopeName: CrossNamespaceAffinity
```

위의 구성을 사용하면, 파드는 생성된 네임스페이스에 `CrossNamespaceAffinity` 범위가 있는 리소스 쿼터 오브젝트가 있고,
해당 필드를 사용하는 파드 수보다 크거나 같은 하드 제한이 있는 경우에만
파드 어피니티에서 `namespaces` 및 `namespaceSelector` 를 사용할 수 있다.

이 기능은 알파이며 기본적으로 비활성화되어 있다. kube-apiserver 및 kube-scheduler 모두에서
[기능 게이트](/ko/docs/reference/command-line-tools-reference/feature-gates/)
`PodAffinityNamespaceSelector` 를 설정하여 활성화할 수 있다.

## 요청과 제한의 비교 {#requests-vs-limits}

컴퓨트 리소스를 할당할 때 각 컨테이너는 CPU 또는 메모리에 대한 요청과 제한값을 지정할 수 있다.
쿼터는 값에 대한 쿼터를 지정하도록 구성할 수 있다.

쿼터에 `requests.cpu`나 `requests.memory`에 지정된 값이 있으면 들어오는 모든
컨테이너가 해당 리소스에 대한 명시적인 요청을 지정해야 한다. 쿼터에 `limits.cpu`나
`limits.memory`에 지정된 값이 있으면 들어오는 모든 컨테이너가 해당 리소스에 대한 명시적인 제한을 지정해야 한다.

## 쿼터 보기 및 설정

Kubectl은 쿼터 생성, 업데이트 및 보기를 지원한다.

```shell
kubectl create namespace myspace
```

```shell
cat <<EOF > compute-resources.yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: compute-resources
spec:
  hard:
    requests.cpu: "1"
    requests.memory: 1Gi
    limits.cpu: "2"
    limits.memory: 2Gi
    requests.nvidia.com/gpu: 4
EOF
```

```shell
kubectl create -f ./compute-resources.yaml --namespace=myspace
```

```shell
cat <<EOF > object-counts.yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: object-counts
spec:
  hard:
    configmaps: "10"
    persistentvolumeclaims: "4"
    pods: "4"
    replicationcontrollers: "20"
    secrets: "10"
    services: "10"
    services.loadbalancers: "2"
EOF
```

```shell
kubectl create -f ./object-counts.yaml --namespace=myspace
```

```shell
kubectl get quota --namespace=myspace
```

```none
NAME                    AGE
compute-resources       30s
object-counts           32s
```

```shell
kubectl describe quota compute-resources --namespace=myspace
```

```none
Name:                    compute-resources
Namespace:               myspace
Resource                 Used  Hard
--------                 ----  ----
limits.cpu               0     2
limits.memory            0     2Gi
requests.cpu             0     1
requests.memory          0     1Gi
requests.nvidia.com/gpu  0     4
```

```shell
kubectl describe quota object-counts --namespace=myspace
```

```none
Name:                   object-counts
Namespace:              myspace
Resource                Used    Hard
--------                ----    ----
configmaps              0       10
persistentvolumeclaims  0       4
pods                    0       4
replicationcontrollers  0       20
secrets                 1       10
services                0       10
services.loadbalancers  0       2
```

Kubectl은 `count/<resource>.<group>` 구문을 사용하여 모든 표준 네임스페이스 리소스에 대한
오브젝트 수 쿼터를 지원한다.

```shell
kubectl create namespace myspace
```

```shell
kubectl create quota test --hard=count/deployments.apps=2,count/replicasets.apps=4,count/pods=3,count/secrets=4 --namespace=myspace
```

```shell
kubectl create deployment nginx --image=nginx --namespace=myspace --replicas=2
```

```shell
kubectl describe quota --namespace=myspace
```

```
Name:                         test
Namespace:                    myspace
Resource                      Used  Hard
--------                      ----  ----
count/deployments.apps        1     2
count/pods                    2     3
count/replicasets.apps        1     4
count/secrets                 1     4
```

## 쿼터 및 클러스터 용량

리소스쿼터는 클러스터 용량과 무관하다. 그것들은 절대 단위로 표현된다.
따라서 클러스터에 노드를 추가해도 각 네임스페이스에 더 많은 리소스를
사용할 수 있는 기능이 자동으로 부여되지는 *않는다*.

가끔 다음과 같은 보다 복잡한 정책이 필요할 수 있다.

- 여러 팀으로 전체 클러스터 리소스를 비례적으로 나눈다.
- 각 테넌트가 필요에 따라 리소스 사용량을 늘릴 수 있지만, 실수로 리소스가 고갈되는 것을
  막기 위한 충분한 제한이 있다.
- 하나의 네임스페이스에서 요구를 감지하고 노드를 추가하며 쿼터를 늘린다.

이러한 정책은 쿼터 사용을 감시하고 다른 신호에 따라 각 네임스페이스의 쿼터 하드 제한을
조정하는 "컨트롤러"를 작성하여 `ResourceQuotas`를 구성 요소로
사용하여 구현할 수 있다.

리소스 쿼터는 통합된 클러스터 리소스를 분할하지만 노드에 대한 제한은 없다.
여러 네임스페이스의 파드가 동일한 노드에서 실행될 수 있다.

## 기본적으로 우선 순위 클래스 소비 제한

파드가 특정 우선 순위, 예를 들어 일치하는 쿼터 오브젝트가 존재하는
경우에만 "cluster-services"가 네임스페이스에 허용되어야 한다.

이 메커니즘을 통해 운영자는 특정 우선 순위가 높은 클래스의 사용을
제한된 수의 네임스페이스로 제한할 수 있으며 모든 네임스페이스가
기본적으로 이러한 우선 순위 클래스를 사용할 수 있는 것은 아니다.

이를 적용하려면 kube-apiserver 플래그 `--admission-control-config-file` 을
사용하여 다음 구성 파일의 경로를 전달해야 한다.

```yaml
apiVersion: apiserver.config.k8s.io/v1
kind: AdmissionConfiguration
plugins:
- name: "ResourceQuota"
  configuration:
    apiVersion: apiserver.config.k8s.io/v1
    kind: ResourceQuotaConfiguration
    limitedResources:
    - resource: pods
      matchScopes:
      - scopeName: PriorityClass
        operator: In
        values: ["cluster-services"]
```

그리고, `kube-system` 네임스페이스에 리소스 쿼터 오브젝트를 생성한다.

{{< codenew file="policy/priority-class-resourcequota.yaml" >}}

```shell
kubectl apply -f https://k8s.io/examples/policy/priority-class-resourcequota.yaml -n kube-system
```

```none
resourcequota/pods-cluster-services created
```

이 경우, 파드 생성은 다음의 조건을 만족해야 허용될 것이다.

1.  파드의 `priorityClassName` 가 명시되지 않음.
1.  파드의 `priorityClassName` 가 `cluster-services` 이외의 다른 값으로 명시됨.
1.  파드의 `priorityClassName` 가 `cluster-services` 로 설정되고, 파드가 `kube-system`
   네임스페이스에 생성되었으며 리소스 쿼터 검증을 통과함.

파드 생성 요청은 `priorityClassName` 가 `cluster-services` 로 명시되고
`kube-system` 이외의 다른 네임스페이스에 생성되는 경우, 거절된다.

## {{% heading "whatsnext" %}}

- 자세한 내용은 [리소스쿼터 디자인 문서](https://git.k8s.io/community/contributors/design-proposals/resource-management/admission_control_resource_quota.md)를 참고한다.
- [리소스 쿼터를 사용하는 방법에 대한 자세한 예](/docs/tasks/administer-cluster/quota-api-object/)를 참고한다.
- [우선 순위 클래스에 대한 쿼터 지원 디자인 문서](https://github.com/kubernetes/community/blob/master/contributors/design-proposals/scheduling/pod-priority-resourcequota.md)를 읽는다.
- [제한된 자원](https://github.com/kubernetes/kubernetes/pull/36765)을 참고한다.
