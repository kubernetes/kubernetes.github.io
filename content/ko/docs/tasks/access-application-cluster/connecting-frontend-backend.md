---
title: 서비스를 사용하여 프론트엔드를 백엔드에 연결
content_type: tutorial
weight: 70
---

<!-- overview -->

이 작업은 _프론트엔드_ 와 _백엔드_ 마이크로서비스를 어떻게 생성하는지를 설명한다. 백엔드
마이크로서비스는 인사하기(hello greeter)이다. 프론트엔드는 nginx 및 쿠버네티스
{{< glossary_tooltip term_id="service" text="서비스" >}} 오브젝트를 사용해 백엔드를 노출한다.

## {{% heading "objectives" %}}

* {{< glossary_tooltip term_id="deployment" text="디플로이먼트(Deployment)" >}} 오브젝트를 사용해
  샘플 `hello` 백엔드 마이크로서비스를 생성하고 실행한다.
* 서비스 오브젝트를 사용하여 백엔드 마이크로서비스의 여러 복제본으로 트래픽을 보낸다.
* 디플로이먼트 오브젝트를 사용하여 `nginx` 프론트엔드 마이크로서비스를 생성하고 실행한다.
* 트래픽을 백엔드 마이크로서비스로 보내도록 프론트엔드 마이크로서비스를 구성한다.
* `type=LoadBalancer` 의 서비스 오브젝트를 사용해 클러스터 외부에 프론트엔드 마이크로서비스를
  노출한다.

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}

이 작업은
지원되는 환경이 필요한
[외부 로드밸런서가 있는 서비스](/docs/tasks/access-application-cluster/create-external-load-balancer/)를 사용한다. 만약, 이를 지원하지 않는 환경이라면, [노드포트](/ko/docs/concepts/services-networking/service/#nodeport) 서비스 타입을
대신 사용할 수 있다.

<!-- lessoncontent -->

## 디플로이먼트를 사용해 백엔드 생성하기

백엔드는 인사하기라는 간단한 마이크로서비스이다. 여기에 백엔드 디플로이먼트
구성 파일이 있다.

{{< codenew file="service/access/backend-deployment.yaml" >}}

백엔드 디플로이먼트를 생성한다.

```shell
kubectl apply -f https://k8s.io/examples/service/access/backend-deployment.yaml
```

백엔드 디플로이먼트에 관한 정보를 본다.

```shell
kubectl describe deployment backend
```

결과는 아래와 같다.

```
Name:                           backend
Namespace:                      default
CreationTimestamp:              Mon, 24 Oct 2016 14:21:02 -0700
Labels:                         app=hello
                                tier=backend
                                track=stable
Annotations:                    deployment.kubernetes.io/revision=1
Selector:                       app=hello,tier=backend,track=stable
Replicas:                       3 desired | 3 updated | 3 total | 3 available | 0 unavailable
StrategyType:                   RollingUpdate
MinReadySeconds:                0
RollingUpdateStrategy:          1 max unavailable, 1 max surge
Pod Template:
  Labels:       app=hello
                tier=backend
                track=stable
  Containers:
   hello:
    Image:              "gcr.io/google-samples/hello-go-gke:1.0"
    Port:               80/TCP
    Environment:        <none>
    Mounts:             <none>
  Volumes:              <none>
Conditions:
  Type          Status  Reason
  ----          ------  ------
  Available     True    MinimumReplicasAvailable
  Progressing   True    NewReplicaSetAvailable
OldReplicaSets:                 <none>
NewReplicaSet:                  hello-3621623197 (3/3 replicas created)
Events:
...
```

## `hello` 서비스 오브젝트 생성하기

프론트엔드에서 백엔드로 요청을 보내는 핵심은 백엔드
서비스이다. 서비스는 백엔드 마이크로서비스에 언제든 도달하기 위해
변하지 않는 IP 주소와 DNS 이름 항목을 생성한다. 서비스는
트래픽을 보내는 파드를 찾기 위해
{{< glossary_tooltip text="selectors" term_id="selector" text="셀렉터" >}}를 사용한다.

먼저, 서비스 구성 파일을 살펴보자.

{{< codenew file="service/access/backend-service.yaml" >}}

구성 파일에서 `hello` 라는 이름의 서비스가 `app: hello` 및 `tier: backend` 레이블을 갖는
파드에 트래픽을 보내는 것을 볼 수 있다.

백엔드 서비스를 생성한다.

```shell
kubectl apply -f https://k8s.io/examples/service/access/backend-service.yaml
```

이 시점에서 `hello` 애플리케이션의 복제본 3개를 실행하는 `backend`
디플로이먼트가 있고, 해당 백엔드로 트래픽을 보내는 서비스가 있다. 그러나, 이
서비스는 클러스터 외부에서 사용할 수 없거나 확인할 수 없다.

## 프론트엔드 생성하기

이제 백엔드를 실행했으므로, 클러스터 외부에서 접근할 수 있는
프론트엔드를 만들고, 백엔드로의 요청을 프록시하여 백엔드에 연결할 수 있다.

프론트엔드는 백엔드 서비스에 지정된 DNS 이름을 사용하여 백엔드
워커 파드에 요청을 보낸다. DNS 이름은
`examples/service/access/backend-service.yaml` 구성 파일의
`name` 필드 값인 `hello` 이다.

프론트엔드 디플로이먼트 안의 파드는 `hello` 백엔드 서비스에 대한 요청을
프록시하도록 구성된 nginx 이미지를 실행한다. 다음은 nginx 구성 파일이다.

{{< codenew file="service/access/frontend-nginx.conf" >}}

백엔드와 같이, 프론트엔드는 디플로이먼트와 서비스를 갖고 있다. 백엔드
서비스와 프론트엔드 서비스 간에 주목해야 할 중요한 차이점은 프론트엔드
서비스의 구성에 `type: LoadBalancer` 가 있다는 것이다. 즉,
서비스가 클라우드 공급자가 프로비저닝한 로드 밸런서를 사용하고
클러스터 외부에서 접근할 수 있음을 의미한다.

{{< codenew file="service/access/frontend-service.yaml" >}}

{{< codenew file="service/access/frontend-deployment.yaml" >}}

프론트엔드 디플로이먼트와 서비스를 생성한다.

```shell
kubectl apply -f https://k8s.io/examples/service/access/frontend-deployment.yaml
kubectl apply -f https://k8s.io/examples/service/access/frontend-service.yaml
```

결과는 두 리소스가 생성되었음을 확인한다.

```
deployment.apps/frontend created
service/frontend created
```

{{< note >}}
nginx 구성은 [컨테이너 이미지](/examples/service/access/Dockerfile)에
반영 되었다. 이를 실행하는 더 좋은 방법은
구성을
보다 쉽게 변경할
수 있는 [컨피그맵(ConfigMap)](/docs/tasks/configure-pod-container/configure-pod-configmap/)을 사용하는 것이다.
{{< /note >}}

## 프론트엔드 서비스와 통신하기

일단 로드밸런서 타입의 서비스를 생성하면, 이 명령어를
사용해 외부 IP를 찾을 수 있다.

```shell
kubectl get service frontend --watch
```

`frontend` 서비스의 구성을 보여주고, 변경 사항을
주시한다. 처음에, 외부 IP는 `<pending>` 으로 나열된다.

```
NAME       TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)  AGE
frontend   LoadBalancer   10.51.252.116   <pending>     80/TCP   10s
```

하지만, 외부 IP가 생성되자마자 구성은
`EXTERNAL-IP` 제목 아래에 새로운 IP를 포함하여 갱신한다.

```
NAME       TYPE           CLUSTER-IP      EXTERNAL-IP        PORT(S)  AGE
frontend   LoadBalancer   10.51.252.116   XXX.XXX.XXX.XXX    80/TCP   1m
```

이제 해당 IP는 클러스터 외부에서 `frontend` 서비스와 통신하는데
사용된다.

## 프론트엔드 통해서 트래픽 보내기

이제 프론트엔드와 백엔드가 연결되었다. 프론트엔드 서비스의 외부 IP에서
curl 명령을 사용해 엔드포인트에 도달할 수 있다.

```shell
curl http://${EXTERNAL_IP} # 앞의 예에서 본 EXTERNAL-IP로 수정한다
```

결과로 백엔드에서 생성된 메시지가 보인다.

```json
{"message":"Hello"}
```

## {{% heading "cleanup" %}}

서비스를 삭제하기 위해, 아래 명령어를 입력하자.

```shell
kubectl delete services frontend backend
```

백엔드와 프론트엔드 애플리케이션에서 실행 중인 디플로이먼트, 레플리카셋, 파드를 삭제하기 위해, 아래 명령어를 입력하자.

```shell
kubectl delete deployment frontend backend
```

## {{% heading "whatsnext" %}}

* [서비스](/ko/docs/concepts/services-networking/service/)에 대해 더 알아본다.
* [컨피그맵](/docs/tasks/configure-pod-container/configure-pod-configmap/)에 대해 더 알아본다.
* [서비스와 파드용 DNS](/ko/docs/concepts/services-networking/dns-pod-service/)에 대해 더 알아본다.
