---
title: HostAliases로 파드의 /etc/hosts 항목 추가하기
content_type: task
weight: 60
min-kubernetes-server-version: 1.7
---


<!-- overview -->

파드의 `/etc/hosts` 파일에 항목을 추가하는 것은 DNS나 다른 방법들이 적용되지 않을 때 파드 수준의 호스트네임 해석을 제공한다. PodSpec의 HostAliases 항목을 사용하여 이러한 사용자 정의 항목들을 추가할 수 있다.

HostAliases를 사용하지 않은 수정은 권장하지 않는데, 이는 호스트 파일이 kubelet에 의해 관리되고, 파드 생성/재시작 중에 덮어쓰여질 수 있기 때문이다.


<!-- steps -->

## 기본 호스트 파일 내용

파드 IP가 할당된 Nginx 파드를 시작한다.

```shell
kubectl run nginx --image nginx
```

```
pod/nginx created
```

파드 IP를 확인해보자.

```shell
kubectl get pods --output=wide
```

```
NAME     READY     STATUS    RESTARTS   AGE    IP           NODE
nginx    1/1       Running   0          13s    10.200.0.4   worker0
```

호스트 파일의 내용은 아래와 같을 것이다.

```shell
kubectl exec nginx -- cat /etc/hosts
```

```
# Kubernetes-managed hosts file.
127.0.0.1	localhost
::1	localhost ip6-localhost ip6-loopback
fe00::0	ip6-localnet
fe00::0	ip6-mcastprefix
fe00::1	ip6-allnodes
fe00::2	ip6-allrouters
10.200.0.4	nginx
```

기본적으로, `hosts` 파일은 `localhost`와 자기 자신의 호스트네임과 같은 IPv4와 IPv6
상용구들만 포함하고 있다.

## hostAliases를 사용하여 추가 항목들 추가하기

기본 상용구 이외에, 추가 항목들을 `hosts` 파일에
추가할 수 있다.
예를 들어, `foo.local`, `bar.local`이 `127.0.0.1`로,
`foo.remote`, `bar.remote`가 `10.1.2.3`로 해석될 수 있도록, `.spec.hostAliases` 항목에서 정의하여 파드에
HostAliases를 추가하면 가능하다.

{{< codenew file="service/networking/hostaliases-pod.yaml" >}}

다음을 실행하여 해당 구성으로 파드를 실행할 수 있다.

```shell
kubectl apply -f https://k8s.io/examples/service/networking/hostaliases-pod.yaml
```

```
pod/hostaliases-pod created
```

파드의 세부 정보를 검토하여 IPv4 주소와 상태를 확인해보자.

```shell
kubectl get pod --output=wide
```

```
NAME                           READY     STATUS      RESTARTS   AGE       IP              NODE
hostaliases-pod                0/1       Completed   0          6s        10.200.0.5      worker0
```

`hosts` 파일 내용은 아래와 같다.

```shell
kubectl logs hostaliases-pod
```

```
# Kubernetes-managed hosts file.
127.0.0.1	localhost
::1	localhost ip6-localhost ip6-loopback
fe00::0	ip6-localnet
fe00::0	ip6-mcastprefix
fe00::1	ip6-allnodes
fe00::2	ip6-allrouters
10.200.0.5	hostaliases-pod

# Entries added by HostAliases.
127.0.0.1	foo.local	bar.local
10.1.2.3	foo.remote	bar.remote
```

가장 마지막에 추가 항목들이 정의되어 있는 것을 확인할 수 있다.

## 왜 Kubelet이 호스트 파일을 관리하는가? {#why-does-kubelet-manage-the-hosts-file}

컨테이너가 이미 시작되고 난 후 도커가 파일을
[수정](https://github.com/moby/moby/issues/17190)하는 것을 방지하기 위해
Kubelet은 파드의 각 컨테이너의 `hosts` 파일을
[관리](https://github.com/kubernetes/kubernetes/issues/14633)한다.

{{< caution >}}
컨테이너 내부의 호스트 파일을 수동으로 변경하면 안된다.

호스트 파일을 수동으로 변경하면,
컨테이너가 종료되면 변경 사항이 손실된다.
{{< /caution >}}
