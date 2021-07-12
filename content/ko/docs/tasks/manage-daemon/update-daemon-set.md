---


title: 데몬셋(DaemonSet)에서 롤링 업데이트 수행
content_type: task
weight: 10
---

<!-- overview -->
이 페이지는 데몬셋에서 롤링 업데이트를 수행하는 방법을 보여준다.

## {{% heading "prerequisites" %}}

<!-- steps -->

## 데몬셋 업데이트 전략

데몬셋에는 두 가지 업데이트 전략 유형이 있다.

* `OnDelete`: `OnDelete` 업데이트 전략을 사용하여, 데몬셋 템플릿을 업데이트한 후,
  이전 데몬셋 파드를 수동으로 삭제할 때 *만* 새 데몬셋 파드가
  생성된다. 이것은 쿠버네티스 버전 1.5 이하에서의 데몬셋의 동작과
  동일하다.
* `RollingUpdate`: 기본 업데이트 전략이다.
  `RollingUpdate` 업데이트 전략을 사용하여, 데몬셋 템플릿을
  업데이트한 후, 오래된 데몬셋 파드가 종료되고, 새로운 데몬셋 파드는
  제어 방식으로 자동 생성된다. 전체 업데이트 프로세스 동안 
  데몬셋의 최대 하나의 파드가 각 노드에서 실행된다.

## 롤링 업데이트 수행

데몬셋의 롤링 업데이트 기능을 사용하려면,
`.spec.updateStrategy.type` 에 `RollingUpdate` 를 설정해야 한다.

[`.spec.updateStrategy.rollingUpdate.maxUnavailable`](/ko/docs/concepts/workloads/controllers/deployment/#최대-불가max-unavailable)
(기본값은 1)과
[`.spec.minReadySeconds`](/ko/docs/concepts/workloads/controllers/deployment/#최소-대기-시간초)
(기본값은 0)으로 
설정할 수도 있다.

### `RollingUpdate` 업데이트 전략으로 데몬셋 생성

이 YAML 파일은 'RollingUpdate'를 업데이트 전략으로 사용하여 데몬셋을 명시한다.

{{< codenew file="controllers/fluentd-daemonset.yaml" >}}

데몬셋 매니페스트의 업데이트 전략을 확인한 후, 데몬셋을 생성한다.

```shell
kubectl create -f https://k8s.io/examples/controllers/fluentd-daemonset.yaml
```

또는, `kubectl apply` 로 데몬셋을 업데이트하려는 경우, 동일한 데몬셋을
생성하는 데 `kubectl apply` 를 사용한다.

```shell
kubectl apply -f https://k8s.io/examples/controllers/fluentd-daemonset.yaml
```

### 데몬셋 `RollingUpdate` 업데이트 전략 확인

데몬셋의 업데이트 전략을 확인하고, `RollingUpdate` 로 설정되어 있는지
확인한다.

```shell
kubectl get ds/fluentd-elasticsearch -o go-template='{{.spec.updateStrategy.type}}{{"\n"}}' -n kube-system
```

시스템에서 데몬셋을 생성하지 않은 경우, 대신 다음의 명령으로
데몬셋 매니페스트를 확인한다.

```shell
kubectl apply -f https://k8s.io/examples/controllers/fluentd-daemonset.yaml --dry-run=client -o go-template='{{.spec.updateStrategy.type}}{{"\n"}}'
```

두 명령의 출력 결과는 다음과 같아야 한다.

```shell
RollingUpdate
```

출력 결과가 `RollingUpdate` 가 아닌 경우, 이전 단계로 돌아가서 데몬셋 오브젝트나 매니페스트를
적절히 수정한다.


### 데몬셋 템플릿 업데이트

`RollingUpdate` 데몬셋 `.spec.template` 에 대한 업데이트는 롤링 업데이트를
트리거한다. 새 YAML 파일을 적용하여 데몬셋을 업데이트한다. 이것은 여러 가지 다른 `kubectl` 명령으로 수행할 수 있다.

{{< codenew file="controllers/fluentd-daemonset-update.yaml" >}}

#### 선언적 커맨드

[구성 파일](/ko/docs/tasks/manage-kubernetes-objects/declarative-config/)을
사용하여 데몬셋을 업데이트하는 경우,
`kubectl apply` 를 사용한다.

```shell
kubectl apply -f https://k8s.io/examples/controllers/fluentd-daemonset-update.yaml
```

#### 명령형 커맨드

[명령형 커맨드](/ko/docs/tasks/manage-kubernetes-objects/imperative-command/)를
사용하여 데몬셋을 업데이트하는 경우,
`kubectl edit` 를 사용한다.

```shell
kubectl edit ds/fluentd-elasticsearch -n kube-system
```

##### 컨테이너 이미지만 업데이트

데몬셋 템플릿(예: `.spec.template.spec.containers[*].image`)에 의해 정의된 컨테이너 이미지만 업데이트하려면, 
`kubectl set image` 를 사용한다.

```shell
kubectl set image ds/fluentd-elasticsearch fluentd-elasticsearch=quay.io/fluentd_elasticsearch/fluentd:v2.6.0 -n kube-system
```

### 롤링 업데이트 상태 관찰

마지막으로, 최신 데몬셋 롤링 업데이트의 롤아웃 상태를 관찰한다.

```shell
kubectl rollout status ds/fluentd-elasticsearch -n kube-system
```

롤아웃이 완료되면, 출력 결과는 다음과 비슷하다.

```shell
daemonset "fluentd-elasticsearch" successfully rolled out
```

## 문제 해결

### 데몬셋 롤링 업데이트가 더 이상 진행되지 않는다(stuck)

가끔씩, 데몬셋 롤링 업데이트가 더 이상 진행되지 않을 수 있다. 이와 같은 상황이 발생할 수 있는 원인은
다음과 같다.

#### 일부 노드에 리소스가 부족하다

적어도 하나의 노드에서 새 데몬셋 파드를 스케줄링할 수 없어서 롤아웃이
중단되었다. 노드에 [리소스가 부족](/docs/concepts/scheduling-eviction/node-pressure-eviction/)할 때
발생할 수 있다.

이 경우, `kubectl get nodes` 의 출력 결과와 다음의 출력 결과를 비교하여
데몬셋 파드가 스케줄링되지 않은 노드를 찾는다.

```shell
kubectl get pods -l name=fluentd-elasticsearch -o wide -n kube-system
```

해당 노드를 찾으면, 데몬셋이 아닌 파드를 노드에서 삭제하여
새 데몬셋 파드를 위한 공간을 생성한다.

{{< note >}}
삭제된 파드가 컨트롤러에 의해 제어되지 않거나 파드가 복제되지 않은 경우 서비스 중단이
발생한다. 이 때 [PodDisruptionBudget](/docs/tasks/run-application/configure-pdb/)정책도 적용되지
않는다.
{{< /note >}}

#### 롤아웃 실패

최근 데몬셋 템플릿 업데이트가 중단된 경우(예를 들어, 컨테이너가
계속 크래시되거나, 컨테이너 이미지가 존재하지 않는 경우(종종 오타로 인해)),
데몬셋 롤아웃이 진행되지 않는다.

이 문제를 해결하려면, 데몬셋 템플릿을 다시 업데이트한다. 이전의 비정상 롤아웃으로 인해
새로운 롤아웃이 차단되지는 않는다.

#### 클럭 차이(skew)

데몬셋에 `.spec.minReadySeconds` 가 명시된 경우, 마스터와 노드 사이의
클럭 차이로 인해 데몬셋이 올바른 롤아웃 진행 상황을 감지할 수
없다.

## 정리

네임스페이스에서 데몬셋을 삭제한다.

```shell
kubectl delete ds fluentd-elasticsearch -n kube-system
```

## {{% heading "whatsnext" %}}

* [데몬셋에서 롤백 수행](/ko/docs/tasks/manage-daemon/rollback-daemon-set/)을 참고한다.
* [기존 데몬셋 파드를 채택하기 위한 데몬셋 생성](/ko/docs/concepts/workloads/controllers/daemonset/)을 참고한다.
