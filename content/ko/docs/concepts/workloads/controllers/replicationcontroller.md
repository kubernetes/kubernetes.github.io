---



title: 레플리케이션 컨트롤러
feature:
  title: 자가 치유
  anchor: 레플리케이션 컨트롤러의 동작 방식
  description: >
    오류가 발생한 컨테이너를 재시작하고, 노드가 죽었을 때 컨테이너를 교체하기 위해 다시 스케줄하고, 사용자 정의 상태 체크에 응답하지 않는 컨테이너를 제거하며, 서비스를 제공할 준비가 될 때까지 클라이언트에 해당 컨테이너를 알리지 않는다.

content_type: concept
weight: 90
---

<!-- overview -->

{{< note >}}
[`ReplicaSet`](/ko/docs/concepts/workloads/controllers/replicaset/)을 구성하는 [`Deployment`](/ko/docs/concepts/workloads/controllers/deployment/)가 현재 권장하는 레플리케이션 설정 방법이다.
{{< /note >}}

_레플리케이션컨트롤러_ 는 언제든지 지정된 수의 파드 레플리카가
실행 중임을 보장한다.
다시 말하면, 레플리케이션 컨트롤러는 파드 또는 동일 종류의 파드의 셋이 항상 기동되고 사용 가능한지 확인한다.

<!-- body -->

## 레플리케이션 컨트롤러의 동작방식

파드가 너무 많으면 레플리케이션 컨트롤러가 추가적인 파드를 제거한다.
너무 적으면 레플리케이션 컨트롤러는 더 많은 파드를 시작한다.
수동으로 생성된 파드와 달리 레플리케이션 컨트롤러가 유지 관리하는 파드는 실패하거나 삭제되거나 종료되는 경우 자동으로 교체된다.
예를 들어, 커널 업그레이드와 같이 파괴적인 유지 보수 작업을 하고 난 이후의 노드에서 파드가 다시 생성된다.
따라서 애플리케이션에 하나의 파드만 필요한 경우에도 레플리케이션 컨트롤러를 사용해야 한다.
레플리케이션 컨트롤러는 프로세스 감시자(supervisor)와 유사하지만
단일 노드에서 개별 프로세스를 감시하는 대신 레플리케이션 컨트롤러는
여러 노드에서 여러 파드를 감시한다.

레플리케이션 컨트롤러는 디스커션에서 종종 "rc"로 축약되며
kubectl 명령에서 숏컷으로 사용된다.

간단한 경우는 하나의 레플리케이션 컨트롤러 오브젝트를 생성하여
한 개의 파드 인스턴스를 영구히 안정적으로 실행하는 것이다.
보다 복잡한 사용 사례는 웹 서버와 같이 복제된 서비스의 동일한 레플리카를 여러 개 실행하는 것이다.

## 레플리케이션 컨트롤러 예제 실행

레플리케이션 컨트롤러 예제의 config는 nginx 웹서버의 복사본 세 개를 실행한다.

{{< codenew file="controllers/replication.yaml" >}}

예제 파일을 다운로드한 후 다음 명령을 실행하여 예제 작업을 실행하라.

```shell
kubectl apply -f https://k8s.io/examples/controllers/replication.yaml
```

출력 결과는 다음과 같다.

```
replicationcontroller/nginx created
```

다음 명령을 사용하여 레플리케이션 컨트롤러의 상태를 확인하자.

```shell
kubectl describe replicationcontrollers/nginx
```

출력 결과는 다음과 같다.

```
Name:        nginx
Namespace:   default
Selector:    app=nginx
Labels:      app=nginx
Annotations:    <none>
Replicas:    3 current / 3 desired
Pods Status: 0 Running / 3 Waiting / 0 Succeeded / 0 Failed
Pod Template:
  Labels:       app=nginx
  Containers:
   nginx:
    Image:              nginx
    Port:               80/TCP
    Environment:        <none>
    Mounts:             <none>
  Volumes:              <none>
Events:
  FirstSeen       LastSeen     Count    From                        SubobjectPath    Type      Reason              Message
  ---------       --------     -----    ----                        -------------    ----      ------              -------
  20s             20s          1        {replication-controller }                    Normal    SuccessfulCreate    Created pod: nginx-qrm3m
  20s             20s          1        {replication-controller }                    Normal    SuccessfulCreate    Created pod: nginx-3ntk0
  20s             20s          1        {replication-controller }                    Normal    SuccessfulCreate    Created pod: nginx-4ok8v
```

이제 세 개의 파드가 생성되었으나 아직 이미지가 풀(pull)되지 않아서 어떤 파드도 시작되지 않았다.
조금 지난 후에 같은 명령이 다음과 같이 보일 것이다.

```shell
Pods Status:    3 Running / 0 Waiting / 0 Succeeded / 0 Failed
```

레플리케이션 컨트롤러에 속한 모든 파드를 머신이 읽을 수 있는 형식으로 나열하기 위해 다음과 같은 명령을 사용할 수 있다.

```shell
pods=$(kubectl get pods --selector=app=nginx --output=jsonpath={.items..metadata.name})
echo $pods
```

출력 결과는 다음과 같다.

```
nginx-3ntk0 nginx-4ok8v nginx-qrm3m
```

여기서 셀렉터는 레플리케이션컨트롤러(`kubectl describe` 의 출력에서 보인)의 셀렉터와 같고,
다른 형식의 파일인 `replication.yaml` 의 것과 동일하다. `--output=jsonpath` 은
반환된 목록의 각 파드의 이름을 출력하도록 하는 옵션이다.


## 레플리케이션 컨트롤러의 Spec 작성

다른 모든 쿠버네티스 컨피그와 마찬가지로 레플리케이션 컨트롤러는 `apiVersion`, `kind`, `metadata` 와 같은 필드가 필요하다.
레플리케이션 컨트롤러 오브젝트의 이름은 유효한
[DNS 서브도메인 이름](/ko/docs/concepts/overview/working-with-objects/names/#dns-서브도메인-이름)이어야 한다.
환경설정 파일의 동작에 관련된 일반적인 정보는 [쿠버네티스 오브젝트 관리](/ko/docs/concepts/overview/working-with-objects/object-management/)를 참고한다.

레플리케이션 컨트롤러는 또한 [`.spec` section](https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status)도 필요하다.

### 파드 템플릿

`.spec.template` 는 오직 `.spec` 필드에서 요구되는 것이다.

`.spec.template` 는 [파드 템플릿](/ko/docs/concepts/workloads/pods/#파드-템플릿)이다. 정확하게 {{< glossary_tooltip text="파드" term_id="pod" >}} 스키마와 동일하나, 중첩되어 있고 `apiVersion` 혹은 `kind`를 갖지 않는다.

파드에 필요한 필드 외에도 레플리케이션 컨트롤러의 파드 템플릿은 적절한 레이블과 적절한 재시작 정책을 지정해야 한다. 레이블의 경우 다른 컨트롤러와
중첩되지 않도록 하라. [파드 셀렉터](#파드-셀렉터)를 참조하라.

오직 `Always` 와 동일한 [`.spec.template.spec.restartPolicy`](/ko/docs/concepts/workloads/pods/pod-lifecycle/#재시작-정책)만 허용되며, 특별히 지정되지 않으면 기본값이다.

로컬 컨테이너의 재시작의 경우, 레플리케이션 컨트롤러는 노드의 에이전트에게 위임한다.
예를 들어 [Kubelet](/docs/reference/command-line-tools-reference/kubelet/) 혹은 도커이다.

### 레플리케이션 컨트롤러에서 레이블

레플리케이션 컨트롤러 자체는 레이블 (`.metadata.labels`) 을 가질 수 있다. 일반적으로 이것을 `.spec.template.metadata.labels` 와 동일하게 설정할 것이다. `.metadata.labels` 가 지정되어 있지 않은 경우,
기본은 `.spec.template.metadata.labels` 이다. 하지만 레이블은
다른 것이 허용되며, `.metadata.labels` 라벨은 레플리케이션 컨트롤러의
동작에 영향을 미치지 않는다.

### 파드 셀렉터

`.spec.selector` 필드는 [레이블 셀렉터](/ko/docs/concepts/overview/working-with-objects/labels/#레이블-셀렉터)이다. 레플리케이션 컨트롤러는 셀렉터와 일치하는 레이블이 있는 모든 파드를 관리한다.
직접 생성하거나 삭제된 파드와 다른 사람이나 프로세스가 생성하거나
삭제한 파드를 구분하지 않는다. 이렇게 하면 실행중인 파드에 영향을 주지 않고
레플리케이션 컨트롤러를 교체할 수 있다.

지정된 경우 `.spec.template.metadata.labels` 은
`.spec.selector` 와 동일해야 하며 그렇지 않으면 API에 의해 거부된다. `.spec.selector` 가 지정되지 않은 경우 기본값은
`.spec.template.metadata.labels` 이다.

또한 일반적으로 이 셀렉터와 레이블이 일치하는 파드를 직접
다른 레플리케이션 컨트롤러 또는 잡과 같은 다른 컨트롤러로 작성해서는 안된다.
그렇게 하면 레플리케이션 컨트롤러는 다른 파드를 생성했다고 생각한다.
쿠버네티스는 이런 작업을 중단해 주지 않는다.

중첩된 셀렉터들을 갖는 다수의 컨트롤러들을 종료하게 되면, 삭제된 것들은 스스로 관리를 해야 한다
([아래](#레플리케이션-컨트롤러-사용하기)를 참조).

### 다수의 레플리카

`.spec.replicas` 를 동시에 실행하고 싶은 파드의 수로 설정함으로써
실행할 파드의 수를 지정할 수 있다. 레플리카가 증가 또는 감소한 경우 또는
파드가 정상적으로 종료되고 교체가 일찍 시작되는 경우라면
언제든지 실행중인 수가 더 높거나 낮을 수 있다.

`.spec.replicas` 를 지정하지 않으면 기본값은 1이다.

## 레플리케이션 컨트롤러 사용하기

### 레플리케이션 컨트롤러와 레플리케이션 컨트롤러의 파드 삭제

레플리케이션 컨트롤러와 레플리케이션의 모든 파드를 삭제하려면 [`kubectl
delete`](/docs/reference/generated/kubectl/kubectl-commands#delete) 를 사용하라.
Kubectl은 레플리케이션 컨트롤러를 0으로 스케일하고 레플리케이션 컨트롤러 자체를
삭제하기 전에 각 파드를 삭제하기를 기다린다. 이 kubectl 명령이 인터럽트되면 다시 시작할 수 있다.

REST API나 Go 클라이언트 라이브러리를 사용하는 경우 명시적으로 단계를 수행해야 한다(레플리카를 0으로 스케일하고 파드의 삭제를 기다린 이후,
레플리케이션 컨트롤러를 삭제).

### 레플리케이션 컨트롤러만 삭제

해당 파드에 영향을 주지 않고 레플리케이션 컨트롤러를 삭제할 수 있다.

kubectl을 사용하여, [`kubectl delete`](/docs/reference/generated/kubectl/kubectl-commands#delete)에 옵션으로 `--cascade=orphan`를 지정하라.

REST API나 Go 클라이언트 라이브러리를 사용하는 경우 레플리케이션 컨트롤러 오브젝트를 삭제하라.

원본이 삭제되면 대체할 새로운 레플리케이션 컨트롤러를 생성하여 교체할 수 있다. 오래된 파드와 새로운 파드의 `.spec.selector` 가 동일하다면,
새로운 레플리케이션 컨트롤러는 오래된 파드를 채택할 것이다. 그러나 기존 파드를
새로운 파드 템플릿과 일치시키려는 노력은 하지 않을 것이다.
새로운 spec에 대한 파드를 제어된 방법으로 업데이트하려면 [롤링 업데이트](#롤링-업데이트)를 사용하라.

### 레플리케이션 컨트롤러에서 파드 격리

파드는 레이블을 변경하여 레플리케이션 컨트롤러의 대상 셋에서 제거될 수 있다. 이 기술은 디버깅과 데이터 복구를 위해 서비스에서 파드를 제거하는 데 사용될 수 있다. 이 방법으로 제거된 파드는 자동으로 교체된다 (레플리카 수가 변경되지 않는다고 가정).

## 일반적인 사용법 패턴

### 다시 스케줄하기

위에서 언급했듯이, 실행하려는 파드가 한 개 혹은 1000개이든 관계없이 레플리케이션 컨트롤러는 노드 실패 또는 파드 종료시 지정된 수의 파드가 존재하도록 보장한다 (예 : 다른 제어 에이전트에 의한 동작으로 인해).

### 스케일링

레플리케이션컨트롤러는 `replicas` 필드를 업데이트하여, 수동으로 또는 오토 스케일링 제어 에이전트를 통해, 레플리카의 수를 늘리거나 줄일 수 있다.

### 롤링 업데이트

레플리케이션 컨트롤러는 파드를 하나씩 교체함으로써 서비스에 대한 롤링 업데이트를 쉽게 하도록 설계되었다.

[#1353](https://issue.k8s.io/1353)에서 설명한 것처럼, 권장되는 접근법은 1 개의 레플리카를 가진 새로운 레플리케이션 컨트롤러를 생성하고 새로운 (+1) 컨트롤러 및 이전 (-1) 컨트롤러를 차례대로 스케일한 후 0개의 레플리카가 되면 이전 컨트롤러를 삭제하는 것이다. 예상치 못한 오류와 상관없이 파드 세트를 예측 가능하게 업데이트한다.

이상적으로 롤링 업데이트 컨트롤러는 애플리케이션 준비 상태를 고려하며 주어진 시간에 충분한 수의 파드가 생산적으로 제공되도록 보장할 것이다.

두 레플리케이션 컨트롤러는 일반적으로 롤링 업데이트를 동기화 하는 이미지 업데이트이기 때문에 파드의 기본 컨테이너 이미지 태그와 같이 적어도 하나의 차별화된 레이블로 파드를 생성해야 한다.

### 다수의 릴리스 트랙

롤링 업데이트가 진행되는 동안 다수의 애플리케이션 릴리스를 실행하는 것 외에도 다수의 릴리스 트랙을 사용하여 장기간에 걸쳐 또는 연속적으로 실행하는 것이 일반적이다. 트랙은 레이블 별로 구분된다.

예를 들어, 서비스는 `tier in (frontend), environment in (prod)` 이 있는 모든 파드를 대상으로 할 수 있다. 이제 이 계층을 구성하는 10 개의 복제된 파드가 있다고 가정해 보자. 하지만 이 구성 요소의 새로운 버전을 '카나리' 하기를 원한다. 대량의 레플리카에 대해 `replicas` 를 9로 설정하고 `tier=frontend, environment=prod, track=stable` 레이블을 설정한 레플리케이션 컨트롤러와, 카나리에 `replicas` 가 1로 설정된 다른 레플리케이션 컨트롤러에 `tier=frontend, environment=prod, track=canary` 라는 레이블을 설정할 수 있다. 이제 이 서비스는 카나리와 카나리 이외의 파드 모두를 포함한다. 그러나 레플리케이션 컨트롤러를 별도로 조작하여 테스트하고 결과를 모니터링하는 등의 작업이 혼란스러울 수 있다.

### 서비스와 레플리케이션컨트롤러 사용

하나의 서비스 뒤에 여러 개의 레플리케이션컨트롤러가 있을 수 있다.
예를 들어 일부 트래픽은 이전 버전으로 이동하고 일부는 새 버전으로 이동한다.

레플리케이션컨트롤러는 자체적으로 종료되지 않지만, 서비스만큼 오래 지속될 것으로 기대되지는 않는다. 서비스는 여러 레플리케이션컨트롤러에 의해 제어되는 파드로 구성될 수 있으며, 서비스 라이프사이클 동안(예를 들어, 서비스를 실행하는 파드 업데이트 수행을 위해) 많은 레플리케이션컨트롤러가 생성 및 제거될 것으로 예상된다. 서비스 자체와 클라이언트 모두 파드를 유지하는 레플리케이션컨트롤러를 의식하지 않는 상태로 남아 있어야 한다.

## 레플리케이션을 위한 프로그램 작성

레플리케이션 컨트롤러에 의해 생성된 파드는 해당 구성이 시간이 지남에 따라 이질적이 될 수 있지만 균일하고 의미상 동일하도록 설계되었다. 이는 레플리카된 상태 스테이트리스 서버에 적합하지만 레플리케이션 컨트롤러를 사용하여 마스터 선출, 샤드 및 워크-풀 애플리케이션의 가용성을 유지할 수도 있다. [RabbitMQ work queues](https://www.rabbitmq.com/tutorials/tutorial-two-python.html)와 같은 애플리케이션은 안티패턴으로 간주되는 각 파드의 구성에 대한 정적/일회성 사용자 정의와 반대로 동적 작업 할당 메커니즘을 사용해야 한다. 리소스의 수직 자동 크기 조정 (예 : CPU 또는 메모리)과 같은 수행된 모든 파드 사용자 정의는 레플리케이션 컨트롤러 자체와 달리 다른 온라인 컨트롤러 프로세스에 의해 수행되어야 한다.

## 레플리케이션 컨트롤러의 책임

레플리케이션 컨트롤러는 의도한 수의 파드가 해당 레이블 셀렉터와 일치하고 동작하는지를 확인한다. 현재, 종료된 파드만 해당 파드의 수에서 제외된다. 향후 시스템에서 사용할 수 있는 [readiness](https://issue.k8s.io/620) 및 기타 정보가 고려될 수 있으며 교체 정책에 대한 통제를 더 추가 할 수 있고 외부 클라이언트가 임의로 정교한 교체 또는 스케일 다운 정책을 구현하기 위해 사용할 수 있는 이벤트를 내보낼 계획이다.

레플리케이션 컨트롤러는 이 좁은 책임에 영원히 제약을 받는다. 그 자체로는 준비성 또는 활성 프로브를 실행하지 않을 것이다. 오토 스케일링을 수행하는 대신, 외부 오토 스케일러 ([#492](https://issue.k8s.io/492)에서 논의된)가 레플리케이션 컨트롤러의 `replicas` 필드를 변경함으로써 제어되도록 의도되었다. 레플리케이션 컨트롤러에 스케줄링 정책 (예를 들어 [spreading](https://issue.k8s.io/367#issuecomment-48428019))을 추가하지 않을 것이다. 오토사이징 및 기타 자동화 된 프로세스를 방해할 수 있으므로 제어된 파드가 현재 지정된 템플릿과 일치하는지 확인해야 한다. 마찬가지로 기한 완료, 순서 종속성, 구성 확장 및 기타 기능은 다른 곳에 속한다. 대량의 파드 생성 메커니즘 ([#170](https://issue.k8s.io/170))까지도 고려해야 한다.

레플리케이션 컨트롤러는 조합 가능한 빌딩-블록 프리미티브가 되도록 고안되었다. 향후 사용자의 편의를 위해 더 상위 수준의 API 및/또는 도구와 그리고 다른 보완적인 기본 요소가 그 위에 구축 될 것으로 기대한다. 현재 kubectl이 지원하는 "매크로" 작업 (실행, 스케일)은 개념 증명의 예시이다. 예를 들어 [Asgard](https://techblog.netflix.com/2012/06/asgard-web-based-cloud-management-and.html)와 같이 레플리케이션 컨트롤러, 오토 스케일러, 서비스, 정책 스케줄링, 카나리 등을 관리할 수 있다.

## API 오브젝트

레플리케이션 컨트롤러는 쿠버네티스 REST API의 최상위 수준의 리소스이다.
API 오브젝트에 대한 더 자세한 것은
[ReplicationController API object](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#replicationcontroller-v1-core) 에서 찾을 수 있다.

## 레플리케이션 컨트롤러의 대안

### 레플리카셋

[`ReplicaSet`](/ko/docs/concepts/workloads/controllers/replicaset/)은 새로운 [집합성 기준 레이블 셀렉터](/ko/docs/concepts/overview/working-with-objects/labels/#집합성-기준-요건)이다.
이것은 주로 [디플로이먼트](/ko/docs/concepts/workloads/controllers/deployment/)에 의해 파드의 생성, 삭제 및 업데이트를 오케스트레이션 하는 메커니즘으로 사용된다.
사용자 지정 업데이트 조정이 필요하거나 업데이트가 필요하지 않은 경우가 아니면 레플리카셋을 직접 사용하는 대신 디플로이먼트를 사용하는 것이 좋다.

### 디플로이먼트 (권장됨)

[`Deployment`](/ko/docs/concepts/workloads/controllers/deployment/)는 기본 레플리카셋과 그 파드를 업데이트하는 상위 수준의 API 오브젝트이다. 선언적이며, 서버 사이드이고, 추가 기능이 있기 때문에 롤링 업데이트 기능을 원한다면 디플로이먼트를 권장한다.

### 베어 파드

사용자가 직접 파드를 만든 경우와 달리 레플리케이션 컨트롤러는 노드 오류 또는 커널 업그레이드와 같은 장애가 발생하는 노드 유지 관리의 경우와 같이 어떤 이유로든 삭제되거나 종료된 파드를 대체한다. 따라서 애플리케이션에 하나의 파드만 필요한 경우에도 레플리케이션 컨트롤러를 사용하는 것이 좋다. 프로세스 관리자와 비슷하게 생각하면, 단지 단일 노드의 개별 프로세스가 아닌 여러 노드에서 여러 파드를 감독하는 것이다. 레플리케이션 컨트롤러는 로컬 컨테이너가 노드의 에이전트로 (예를 들어 Kubelet 또는 도커 ) 재시작하도록 위임한다.

### 잡

자체적으로 제거될 것으로 예상되는 파드 (즉, 배치 잡)의 경우
레플리케이션 컨트롤러 대신 [`Job`](/ko/docs/concepts/workloads/controllers/job/)을 사용하라.

### 데몬셋

머신 모니터링이나 머신 로깅과 같은 머신 레벨 기능을 제공하는 파드에는 레플리케이션 컨트롤러 대신
[`DaemonSet`](/ko/docs/concepts/workloads/controllers/daemonset/)을 사용하라. 이런 파드들의 수명은 머신의 수명에 달려 있다.
다른 파드가 시작되기 전에 파드가 머신에서 실행되어야 하며,
머신이 재부팅/종료 준비가 되어 있을 때 안전하게 종료된다.

## 더 자세한 정보는

[스테이트리스 애플리케이션 디플로이먼트 실행하기](/docs/tasks/run-application/run-stateless-application-deployment/)를 참고한다.
