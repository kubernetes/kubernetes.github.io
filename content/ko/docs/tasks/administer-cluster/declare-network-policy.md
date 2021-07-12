---



title: 네트워크 폴리시(Network Policy) 선언하기
min-kubernetes-server-version: v1.8
content_type: task
---
<!-- overview -->
이 문서는 사용자가 쿠버네티스 [네트워크폴리시 API](/ko/docs/concepts/services-networking/network-policies/)를 사용하여 파드(Pod)가 서로 통신하는 방법을 제어하는 네트워크 폴리시를 선언하는데 도움을 준다.

{{% thirdparty-content %}}

## {{% heading "prerequisites" %}}


{{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}

네트워크 폴리시를 지원하는 네트워크 제공자를 구성하였는지 확인해야 한다. 다음과 같이 네트워크폴리시를 지원하는 많은 네트워크 제공자들이 있다.

* [Antrea](/docs/tasks/administer-cluster/network-policy-provider/antrea-network-policy/)
* [캘리코(Calico)](/ko/docs/tasks/administer-cluster/network-policy-provider/calico-network-policy/)
* [실리움(Cilium)](/ko/docs/tasks/administer-cluster/network-policy-provider/cilium-network-policy/)
* [Kube-router](/ko/docs/tasks/administer-cluster/network-policy-provider/kube-router-network-policy/)
* [로마나(Romana)](/ko/docs/tasks/administer-cluster/network-policy-provider/romana-network-policy/)
* [위브넷(Weave Net)](/ko/docs/tasks/administer-cluster/network-policy-provider/weave-network-policy/)

<!-- steps -->

## `nginx` 디플로이먼트(Deployment)를 생성하고 서비스(Service)를 통해 노출하기

쿠버네티스 네트워크 폴리시가 어떻게 동작하는지 확인하기 위해서, `nginx` 디플로이먼트를 생성한다.

```console
kubectl create deployment nginx --image=nginx
```
```none
deployment.apps/nginx created
```

`nginx` 라는 이름의 서비스를 통해 디플로이먼트를 노출한다.

```console
kubectl expose deployment nginx --port=80
```

```none
service/nginx exposed
```

위 명령어들은 nginx 파드에 대한 디플로이먼트를 생성하고, `nginx` 라는 이름의 서비스를 통해 디플로이먼트를 노출한다. `nginx` 파드와 디플로이먼트는 `default` 네임스페이스(namespace)에 존재한다.

```console
kubectl get svc,pod
```

```none
NAME                        CLUSTER-IP    EXTERNAL-IP   PORT(S)    AGE
service/kubernetes          10.100.0.1    <none>        443/TCP    46m
service/nginx               10.100.0.16   <none>        80/TCP     33s

NAME                        READY         STATUS        RESTARTS   AGE
pod/nginx-701339712-e0qfq   1/1           Running       0          35s
```

## 다른 파드에서 접근하여 서비스 테스트하기

사용자는 다른 파드에서 새 `nginx` 서비스에 접근할 수 있어야 한다. `default` 네임스페이스에 있는 다른 파드에서 `nginx` 서비스에 접근하기 위하여, busybox 컨테이너를 생성한다.

```console
kubectl run busybox --rm -ti --image=busybox -- /bin/sh
```

사용자 쉘에서, 다음의 명령을 실행한다.

```shell
wget --spider --timeout=1 nginx
```

```none
Connecting to nginx (10.100.0.16:80)
remote file exists
```

## `nginx` 서비스에 대해 접근 제한하기

`access: true` 레이블을 가지고 있는 파드만 `nginx` 서비스에 접근할 수 있도록 하기 위하여, 다음과 같은 네트워크폴리시 오브젝트를 생성한다.

{{< codenew file="service/networking/nginx-policy.yaml" >}}

네트워크폴리시 오브젝트의 이름은 유효한
[DNS 서브도메인 이름](/ko/docs/concepts/overview/working-with-objects/names/#dns-서브도메인-이름)이어야 한다.

{{< note >}}
네트워크폴리시는 정책이 적용되는 파드의 그룹을 선택하는 `podSelector` 를 포함한다. 사용자는 이 정책이 `app=nginx` 레이블을 갖는 파드를 선택하는 것을 볼 수 있다. 레이블은 `nginx` 디플로이먼트에 있는 파드에 자동으로 추가된다. 빈 `podSelector` 는 네임스페이스의 모든 파드를 선택한다.
{{< /note >}}

## 서비스에 정책 할당하기

kubectl을 사용하여 위 `nginx-policy.yaml` 파일로부터 네트워크폴리시를 생성한다.

```console
kubectl apply -f https://k8s.io/examples/service/networking/nginx-policy.yaml
```

```none
networkpolicy.networking.k8s.io/access-nginx created
```

## access 레이블이 정의되지 않은 서비스에 접근 테스트
올바른 레이블이 없는 파드에서 `nginx` 서비스에 접근하려 할 경우, 요청 타임 아웃이 발생한다.

```console
kubectl run busybox --rm -ti --image=busybox -- /bin/sh
```

사용자 쉘에서, 다음의 명령을 실행한다.

```shell
wget --spider --timeout=1 nginx
```

```none
Connecting to nginx (10.100.0.16:80)
wget: download timed out
```

## 접근 레이블을 정의하고 다시 테스트

사용자는 요청이 허용되도록 하기 위하여 올바른 레이블을 갖는 파드를 생성한다.

```console
kubectl run busybox --rm -ti --labels="access=true" --image=busybox -- /bin/sh
```

사용자 쉘에서, 다음의 명령을 실행한다.

```shell
wget --spider --timeout=1 nginx
```

```none
Connecting to nginx (10.100.0.16:80)
remote file exists
```
