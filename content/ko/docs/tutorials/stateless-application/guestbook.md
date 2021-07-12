---
title: "예시: Redis를 사용한 PHP 방명록 애플리케이션 배포하기"



content_type: tutorial
weight: 20
card:
  name: tutorials
  weight: 30
  title: "상태를 유지하지 않는 예제: Redis를 사용한 PHP 방명록"
min-kubernetes-server-version: v1.14
source: https://cloud.google.com/kubernetes-engine/docs/tutorials/guestbook
---

<!-- overview -->
이 튜토리얼에서는 쿠버네티스와 [Docker](https://www.docker.com/)를 사용하여 간단한 _(운영 수준이 아닌)_ 멀티 티어 웹 애플리케이션을 빌드하고 배포하는 방법을 보여준다. 이 예제는 다음과 같은 구성으로 이루어져 있다.

* 방명록 항목을 저장하기 위한 단일 인스턴스 [Redis](https://www.redis.com/)
* 여러 개의 웹 프론트엔드 인스턴스

## {{% heading "objectives" %}}

* Redis 리더를 실행
* 2개의 Redis 팔로워를 실행
* 방명록 프론트엔드를 실행
* 프론트엔드 서비스를 노출하고 확인
* 정리하기

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}}

{{< version-check >}}

<!-- lessoncontent -->

## Redis 데이터베이스를 실행

방명록 애플리케이션은 Redis를 사용하여 데이터를 저장한다.

### Redis 디플로이먼트를 생성하기

아래의 매니페스트 파일은 단일 복제본 Redis 파드를 실행하는 디플로이먼트 컨트롤러에 대한 명세를 담고 있다.

{{< codenew file="application/guestbook/redis-leader-deployment.yaml" >}}

1. 매니페스트 파일을 다운로드한 디렉터리에서 터미널 창을 시작한다.
1. `redis-leader-deployment.yaml` 파일을 이용하여 Redis 디플로이먼트를 생성한다.

      <!--
      로컬에 있는 파일로 테스트하려면 다음과 같이 상대 경로로 기재한다.
      kubectl apply -f ./content/en/examples/application/guestbook/redis-leader-deployment.yaml
      -->

      ```shell
      kubectl apply -f https://k8s.io/examples/application/guestbook/redis-leader-deployment.yaml
      ```

1. 파드의 목록을 질의하여 Redis 파드가 실행 중인지 확인한다.

      ```shell
      kubectl get pods
      ```

      결과는 아래와 같은 형태로 나타난다.

      ```
      NAME                            READY     STATUS    RESTARTS   AGE
      redis-leader-fb76b4755-xjr2n   1/1     Running   0          13s
      ```

2. Redis 리더 파드의 로그를 보려면 다음 명령어를 실행한다.

     ```shell
     kubectl logs -f deployment/redis-leader
     ```

### Redis 리더 서비스 생성하기

방명록 애플리케이션에서 데이터를 쓰려면 Redis와 통신해야 한다. Redis 파드로 트래픽을 프록시하려면 [서비스](/ko/docs/concepts/services-networking/service/)를 생성해야 한다. 서비스는 파드에 접근하기 위한 정책을 정의한다.

{{< codenew file="application/guestbook/redis-leader-service.yaml" >}}

1. `redis-leader-service.yaml` 파일을 이용하여 Redis 서비스를 실행한다.

      <!--
      로컬에 있는 파일로 테스트하려면 다음과 같이 상대 경로로 기재한다.
      kubectl apply -f ./content/en/examples/application/guestbook/redis-leader-service.yaml
      -->

      ```shell
      kubectl apply -f https://k8s.io/examples/application/guestbook/redis-leader-service.yaml
      ```

1. 서비스의 목록을 질의하여 Redis 서비스가 실행 중인지 확인한다.

      ```shell
      kubectl get service
      ```

      결과는 아래와 같은 형태로 나타난다.

      ```
      NAME           TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)    AGE
      kubernetes     ClusterIP   10.0.0.1     <none>        443/TCP    1m
      redis-leader   ClusterIP   10.103.78.24 <none>        6379/TCP   16s
      ```

{{< note >}}
이 매니페스트 파일은 이전에 정의된 레이블과 일치하는 레이블 집합을 가진 `redis-leader`라는 서비스를 생성하므로, 서비스는 네트워크 트래픽을 Redis 파드로 라우팅한다.
{{< /note >}}

### Redis 팔로워 구성하기

Redis 리더는 단일 파드이지만, 몇 개의 Redis 팔로워 또는 복제본을 추가하여 가용성을 높이고 트래픽 요구를 충족할 수 있다.

{{< codenew file="application/guestbook/redis-follower-deployment.yaml" >}}

1. `redis-follower-deployment.yaml` 파일을 이용하여 Redis 서비스를 실행한다.

      <!---
      로컬에 있는 파일로 테스트하려면 다음과 같이 상대 경로로 기재한다.
      kubectl apply -f ./content/en/examples/application/guestbook/redis-follower-deployment.yaml
      -->

      ```shell
      kubectl apply -f https://k8s.io/examples/application/guestbook/redis-follower-deployment.yaml
      ```

1. 파드의 목록을 질의하여 2개의 Redis 팔로워 레플리카가 실행 중인지 확인한다.

      ```shell
      kubectl get pods
      ```

      결과는 아래와 같은 형태로 나타난다.

      ```
      NAME                             READY   STATUS    RESTARTS   AGE
      redis-follower-dddfbdcc9-82sfr   1/1     Running   0          37s
      redis-follower-dddfbdcc9-qrt5k   1/1     Running   0          38s
      redis-leader-fb76b4755-xjr2n     1/1     Running   0          11m
      ```

### Redis 팔로워 서비스 생성하기

방명록 애플리케이션이 데이터를 읽으려면 Redis 팔로워와 통신해야 한다. Redis 팔로워를 발견 가능(discoverable)하게 만드려면, 새로운 [서비스](/ko/docs/concepts/services-networking/service/)를 구성해야 한다.

{{< codenew file="application/guestbook/redis-follower-service.yaml" >}}

1. `redis-follower-service.yaml` 파일을 이용하여 Redis 서비스를 실행한다.

      <!---
      로컬에 있는 파일로 테스트하려면 다음과 같이 상대 경로로 기재한다.
      kubectl apply -f ./content/en/examples/application/guestbook/redis-follower-service.yaml
      -->

      ```shell
      kubectl apply -f https://k8s.io/examples/application/guestbook/redis-follower-service.yaml
      ```

1. 서비스의 목록을 질의하여 Redis 서비스가 실행 중인지 확인한다.

      ```shell
      kubectl get service
      ```

      결과는 아래와 같은 형태로 나타난다.

      ```
     NAME             TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
     kubernetes       ClusterIP   10.96.0.1       <none>        443/TCP    3d19h
     redis-follower   ClusterIP   10.110.162.42   <none>        6379/TCP   9s
     redis-leader     ClusterIP   10.103.78.24    <none>        6379/TCP   6m10s
      ```

{{< note >}}
이 매니페스트 파일은 이전에 정의된 레이블과 일치하는 레이블 집합을 가진 `redis-follower`라는 서비스를 생성하므로, 서비스는 네트워크 트래픽을 Redis 파드로 라우팅한다.
{{< /note >}}

## 방명록 프론트엔드를 설정하고 노출하기

방명록을 위한 Redis 저장소를 구성하고 실행했으므로, 이제 방명록 웹 서버를 실행한다. Redis 팔로워와 마찬가지로, 프론트엔드는 쿠버네티스 디플로이먼트(Deployment)를 사용하여 배포된다.

방명록 앱은 PHP 프론트엔드를 사용한다. DB에 대한 요청이 읽기인지 쓰기인지에 따라, Redis 팔로워 또는 리더 서비스와 통신하도록 구성된다. 프론트엔드는 JSON 인터페이스를 노출하고, jQuery-Ajax 기반 UX를 제공한다.

### 방명록 프론트엔드의 디플로이먼트 생성하기

{{< codenew file="application/guestbook/frontend-deployment.yaml" >}}

1. `frontend-deployment.yaml` 파일을 이용하여 프론트엔드 디플로이먼트를 생성한다.

      <!--
      로컬에 있는 파일로 테스트하려면 다음과 같이 상대 경로로 기재한다.
      kubectl apply -f ./content/en/examples/application/guestbook/frontend-deployment.yaml
      -->

      ```shell
      kubectl apply -f https://k8s.io/examples/application/guestbook/frontend-deployment.yaml
      ```

1. 파드의 목록을 질의하여 세 개의 프론트엔드 복제본이 실행되고 있는지 확인한다.

      ```shell
      kubectl get pods -l app=guestbook -l tier=frontend
      ```

      결과는 아래와 같은 형태로 나타난다.

      ```
     NAME                        READY   STATUS    RESTARTS   AGE
     frontend-85595f5bf9-5tqhb   1/1     Running   0          47s
     frontend-85595f5bf9-qbzwm   1/1     Running   0          47s
     frontend-85595f5bf9-zchwc   1/1     Running   0          47s
      ```

### 프론트엔드 서비스 생성하기

서비스의 기본 유형은 [ClusterIP](/ko/docs/concepts/services-networking/service/#publishing-services-service-types)이기 때문에 생성한 `Redis` 서비스는 컨테이너 클러스터 내에서만 접근할 수 있다. `ClusterIP`는 서비스가 가리키는 파드 집합에 대한 단일 IP 주소를 제공한다. 이 IP 주소는 클러스터 내에서만 접근할 수 있다.

게스트가 방명록에 접근할 수 있도록 하려면, 외부에서 볼 수 있도록 프론트엔드 서비스를 구성해야 한다. 그렇게 하면 클라이언트가 쿠버네티스 클러스터 외부에서 서비스를 요청할 수 있다. 그러나 쿠버네티스 사용자는 `ClusterIP`를 사용하더라도 `kubectl port-forward`를 사용해서 서비스에 접근할 수 있다.

{{< note >}}
Google Compute Engine 또는 Google Kubernetes Engine과 같은 일부 클라우드 공급자는 외부 로드 밸런서를 지원한다. 클라우드 공급자가 로드 밸런서를 지원하고 이를 사용하려면 `type : LoadBalancer`의 주석을 제거해야 한다.
{{< /note >}}

{{< codenew file="application/guestbook/frontend-service.yaml" >}}

1. `frontend-service.yaml` 파일을 이용하여 프론트엔드 서비스를 실행한다.

      <!--
      로컬에 있는 파일로 테스트하려면 다음과 같이 상대 경로로 기재한다.
      kubectl apply -f ./content/en/examples/application/guestbook/frontend-service.yaml
      -->

      ```shell
      kubectl apply -f https://k8s.io/examples/application/guestbook/frontend-service.yaml
      ```

1. 서비스의 목록을 질의하여 프론트엔드 서비스가 실행 중인지 확인한다.

      ```shell
      kubectl get services
      ```

      결과는 아래와 같은 형태로 나타난다.

      ```
     NAME             TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
     frontend         ClusterIP   10.97.28.230    <none>        80/TCP     19s
     kubernetes       ClusterIP   10.96.0.1       <none>        443/TCP    3d19h
     redis-follower   ClusterIP   10.110.162.42   <none>        6379/TCP   5m48s
     redis-leader     ClusterIP   10.103.78.24    <none>        6379/TCP   11m
      ```

### `kubectl port-forward`를 통해 프론트엔드 서비스 확인하기

1. 다음 명령어를 실행해서 로컬 머신의 `8080` 포트를 서비스의 `80` 포트로 전달한다.

      ```shell
      kubectl port-forward svc/frontend 8080:80
      ```

      결과는 아래와 같은 형태로 나타난다.

      ```
      Forwarding from 127.0.0.1:8080 -> 80
      Forwarding from [::1]:8080 -> 80
      ```

1. 방명록을 보기위해 브라우저에서 [http://localhost:8080](http://localhost:8080) 페이지를 로드한다.

### `LoadBalancer`를 통해 프론트엔드 서비스 확인하기

`frontend-service.yaml` 매니페스트를 `LoadBalancer`와 함께 배포한 경우, 방명록을 보기 위해 IP 주소를 찾아야 한다.

1. 프론트엔드 서비스의 IP 주소를 얻기 위해 아래 명령어를 실행한다.

      ```shell
      kubectl get service frontend
      ```

      결과는 아래와 같은 형태로 나타난다.

      ```
      NAME       TYPE           CLUSTER-IP      EXTERNAL-IP        PORT(S)        AGE
      frontend   LoadBalancer   10.51.242.136   109.197.92.229     80:32372/TCP   1m
      ```

1. IP 주소를 복사하고, 방명록을 보기 위해 브라우저에서 페이지를 로드한다.

{{< note >}}
메시지를 입력하고 'Submit'을 클릭하여 방명록에 글을 작성해 본다. 입력한 메시지가 프론트엔드에 나타난다. 이 메시지는 앞서 생성한 서비스를 통해 데이터가 Redis에 성공적으로 입력되었음을 나타낸다.
{{< /note >}}

## 웹 프론트엔드 확장하기

서버가 디플로이먼트 컨트롤러를 사용하는 서비스로 정의되어 있으므로 필요에 따라 확장 또는 축소할 수 있다.

1. 프론트엔드 파드의 수를 확장하기 위해 아래 명령어를 실행한다.

      ```shell
      kubectl scale deployment frontend --replicas=5
      ```

1. 파드의 목록을 질의하여 실행 중인 프론트엔드 파드의 수를 확인한다.

      ```shell
      kubectl get pods
      ```

      결과는 아래와 같은 형태로 나타난다.

      ```
      NAME                             READY   STATUS    RESTARTS   AGE
      frontend-85595f5bf9-5df5m        1/1     Running   0          83s
      frontend-85595f5bf9-7zmg5        1/1     Running   0          83s
      frontend-85595f5bf9-cpskg        1/1     Running   0          15m
      frontend-85595f5bf9-l2l54        1/1     Running   0          14m
      frontend-85595f5bf9-l9c8z        1/1     Running   0          14m
      redis-follower-dddfbdcc9-82sfr   1/1     Running   0          97m
      redis-follower-dddfbdcc9-qrt5k   1/1     Running   0          97m
      redis-leader-fb76b4755-xjr2n     1/1     Running   0          108m
      ```

1. 프론트엔드 파드의 수를 축소하기 위해 아래 명령어를 실행한다.

      ```shell
      kubectl scale deployment frontend --replicas=2
      ```

1. 파드의 목록을 질의하여 실행 중인 프론트엔드 파드의 수를 확인한다.

      ```shell
      kubectl get pods
      ```

      결과는 아래와 같은 형태로 나타난다.

      ```
      NAME                            READY     STATUS    RESTARTS   AGE
      frontend-85595f5bf9-cpskg        1/1     Running   0          16m
      frontend-85595f5bf9-l9c8z        1/1     Running   0          15m
      redis-follower-dddfbdcc9-82sfr   1/1     Running   0          98m
      redis-follower-dddfbdcc9-qrt5k   1/1     Running   0          98m
      redis-leader-fb76b4755-xjr2n     1/1     Running   0          109m
      ```

## {{% heading "cleanup" %}}

디플로이먼트 및 서비스를 삭제하면 실행 중인 모든 파드도 삭제된다. 레이블을 사용하여 하나의 명령어로 여러 자원을 삭제해보자.

1. 모든 파드, 디플로이먼트, 서비스를 삭제하기 위해 아래 명령어를 실행한다.

      ```shell
      kubectl delete deployment -l app=redis
      kubectl delete service -l app=redis
      kubectl delete deployment frontend
      kubectl delete service frontend
      ```

      결과는 아래와 같은 형태로 나타난다.

      ```
      deployment.apps "redis-follower" deleted
      deployment.apps "redis-leader" deleted
      deployment.apps "frontend" deleted
      service "frontend" deleted
      ```

1. 파드의 목록을 질의하여 실행 중인 파드가 없는지 확인한다.

      ```shell
      kubectl get pods
      ```

      결과는 아래와 같은 형태로 나타난다.

      ```
      No resources found in default namespace.
      ```

## {{% heading "whatsnext" %}}

* [쿠버네티스 기초](/ko/docs/tutorials/kubernetes-basics/) 튜토리얼을 완료
* [MySQL과 Wordpress을 위한 퍼시스턴트 볼륨](/ko/docs/tutorials/stateful-application/mysql-wordpress-persistent-volume/#visit-your-new-wordpress-blog)을 사용하여 블로그 생성하는데 쿠버네티스 이용하기
* [애플리케이션 접속](/ko/docs/concepts/services-networking/connect-applications-service/)에 대해 더 알아보기
* [자원 관리](/ko/docs/concepts/cluster-administration/manage-deployment/#효과적인-레이블-사용)에 대해 더 알아보기
