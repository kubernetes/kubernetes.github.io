---
title: DNS 서비스 사용자 정의하기
content_type: task
min-kubernetes-server-version: v1.12
---

<!-- overview -->
이 페이지는 클러스터 안에서 사용자의
DNS {{< glossary_tooltip text="파드(Pod)" term_id="pod" >}} 를 설정하고
DNS 변환(DNS resolution) 절차를 사용자 정의하는 방법을 설명한다.

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}}

클러스터는 CoreDNS 애드온을 구동하고 있어야 한다.
[CoreDNS로 이관하기](/ko/docs/tasks/administer-cluster/coredns/#coredns로-이관하기)
는 `kubeadm` 을 이용하여 `kube-dns` 로부터 이관하는 방법을 설명한다.  

{{% version-check %}}

<!-- steps -->

## 소개

DNS는 _애드온 관리자_ 인 [클러스터 애드온](https://releases.k8s.io/{{< param "githubbranch" >}}/cluster/addons/README.md)을
사용하여 자동으로 시작되는 쿠버네티스
내장 서비스이다.

쿠버네티스 v1.12 부터, CoreDNS는 kube-dns를 대체하여 권장되는 DNS 서버이다. 만약 사용자의 클러스터가 원래 kube-dns를 사용하였을 경우,
CoreDNS 대신 `kube-dns` 를 계속 사용할 수도 있다.

{{< note >}}
CoreDNS 서비스는 `metadata.name` 필드에 `kube-dns` 로 이름이 지정된다.
이를 통해, 기존의 `kube-dns` 서비스 이름을 사용하여 클러스터 내부의 주소를 확인하는 워크로드에 대한 상호 운용성이 증가된다. `kube-dns` 로 서비스 이름을 사용하면, 해당 DNS 공급자가 어떤 공통 이름으로 실행되고 있는지에 대한 구현 세부 정보를 추상화한다.
{{< /note >}}

CoreDNS를 디플로이먼트(Deployment)로 실행하고 있을 경우, 일반적으로 고정 IP 주소를 갖는 쿠버네티스 서비스로 노출된다.
Kubelet 은 `--cluster-dns=<dns-service-ip>` 플래그를 사용하여 DNS 확인자 정보를 각 컨테이너에 전달한다.

DNS 이름에도 도메인이 필요하다. 사용자는 kubelet 에 있는 `--cluster-domain=<default-local-domain>` 플래그를
통하여 로컬 도메인을 설정할 수 있다.

DNS 서버는 정방향 조회(A 및 AAAA 레코드), 포트 조회(SRV 레코드), 역방향 IP 주소 조회(PTR 레코드) 등을 지원한다.
더 자세한 내용은 [서비스 및 파드용 DNS](/ko/docs/concepts/services-networking/dns-pod-service/)를 참고한다.

만약 파드의 `dnsPolicy` 가 `default` 로 지정되어 있는 경우,
파드는 자신이 실행되는 노드의 이름 변환(name resolution) 구성을 상속한다.
파드의 DNS 변환도 노드와 동일하게 작동해야 한다.
그 외에는 [알려진 이슈](/docs/tasks/administer-cluster/dns-debugging-resolution/#known-issues)를 참고한다.

만약 위와 같은 방식을 원하지 않거나, 파드를 위해 다른 DNS 설정이 필요한 경우,
사용자는 kubelet 의 `--resolv-conf` 플래그를 사용할 수 있다.
파드가 DNS를 상속받지 못하도록 하기 위해 이 플래그를 ""로 설정한다.
DNS 상속을 위해 `/etc/resolv.conf` 이외의 파일을 지정할 경우 유효한 파일 경로를 설정한다.

## CoreDNS

CoreDNS는 [dns 명세](https://github.com/kubernetes/dns/blob/master/docs/specification.md)를 준수하며 클러스터 DNS 역할을 할 수 있는, 범용적인 권한을 갖는 DNS 서버이다.

### CoreDNS 컨피그맵(ConfigMap) 옵션

CoreDNS는 모듈형이자 플러그인이 가능한 DNS 서버이며, 각 플러그인들은 CoreDNS에 새로운 기능을 부가한다.
이는 CoreDNS 구성 파일인 [Corefile](https://coredns.io/2017/07/23/corefile-explained/)을 관리하여 구성할 수 있다.
클러스터 관리자는 CoreDNS Corefile에 대한 {{< glossary_tooltip text="컨피그맵" term_id="configmap" >}}을 수정하여
해당 클러스터에 대한 DNS 서비스 검색 동작을
변경할 수 있다.

쿠버네티스에서 CoreDNS는 아래의 기본 Corefile 구성으로 설치된다.

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: coredns
  namespace: kube-system
data:
  Corefile: |
    .:53 {
        errors
        health {
            lameduck 5s
        }
        ready
        kubernetes cluster.local in-addr.arpa ip6.arpa {
            pods insecure
            fallthrough in-addr.arpa ip6.arpa
            ttl 30
        }
        prometheus :9153
        forward . /etc/resolv.conf
        cache 30
        loop
        reload
        loadbalance
    }
```

Corefile의 구성은 CoreDNS의 아래 [플러그인](https://coredns.io/plugins)을 포함한다.

* [errors](https://coredns.io/plugins/errors/): 오류가 표준 출력(stdout)에 기록된다.
* [health](https://coredns.io/plugins/health/): CoreDNS의 상태(healthy)가 `http://localhost:8080/health` 에 기록된다. 이 확장 구문에서 `lameduck` 은 프로세스를 비정상 상태(unhealthy)로 만들고, 프로세스가 종료되기 전에 5초 동안 기다린다.
* [ready](https://coredns.io/plugins/ready/): 8181 포트의 HTTP 엔드포인트가, 모든 플러그인이 준비되었다는 신호를 보내면 200 OK 를 반환한다.
* [kubernetes](https://coredns.io/plugins/kubernetes/): CoreDNS가 쿠버네티스의 서비스 및 파드의 IP를 기반으로 DNS 쿼리에 대해 응답한다. 해당 플러그인에 대한 [세부 사항](https://coredns.io/plugins/kubernetes/)은 CoreDNS 웹사이트에서 확인할 수 있다. `ttl` 을 사용하면 응답에 대한 사용자 정의 TTL 을 지정할 수 있으며, 기본값은 5초이다. 허용되는 최소 TTL은 0초이며, 최대값은 3600초이다. 레코드가 캐싱되지 않도록 할 경우, TTL을 0으로 설정한다.
  `pods insecure` 옵션은 _kube-dns_ 와의 하위 호환성을 위해 제공된다. `pods verified` 옵션을 사용하여, 일치하는 IP의 동일 네임스페이스(Namespace)에 파드가 존재하는 경우에만 A 레코드를 반환하게 할 수 있다. `pods disabled` 옵션은 파드 레코드를 사용하지 않을 경우 사용된다.
* [prometheus](https://coredns.io/plugins/metrics/): CoreDNS의 메트릭은 [프로메테우스](https://prometheus.io/) 형식(OpenMetrics 라고도 알려진)의 `http://localhost:9153/metrics` 에서 사용 가능하다.
* [forward](https://coredns.io/plugins/forward/): 쿠버네티스 클러스터 도메인에 없는 쿼리들은 모두 사전에 정의된 리졸버(/etc/resolv.conf)로 전달된다.
* [cache](https://coredns.io/plugins/cache/): 프론트 엔드 캐시를 활성화한다.
* [loop](https://coredns.io/plugins/loop/): 간단한 전달 루프(loop)를 감지하고, 루프가 발견되면 CoreDNS 프로세스를 중단(halt)한다.
* [reload](https://coredns.io/plugins/reload): 변경된 Corefile을 자동으로 다시 로드하도록 한다. 컨피그맵 설정을 변경한 후에 변경 사항이 적용되기 위하여 약 2분정도 소요된다.
* [loadbalance](https://coredns.io/plugins/loadbalance): 응답에 대하여 A, AAAA, MX 레코드의 순서를 무작위로 선정하는 라운드-로빈 DNS 로드밸런서이다.

사용자는 컨피그맵을 변경하여 기본 CoreDNS 동작을 변경할 수 있다.

### CoreDNS를 사용하는 스텁 도메인(Stub-domain)과 업스트림 네임서버(nameserver)의 설정

CoreDNS는 [포워드 플러그인](https://coredns.io/plugins/forward/)을 사용하여 스텁 도메인 및 업스트림 네임서버를 구성할 수 있다.

#### 예시
만약 클러스터 운영자가 10.150.0.1 에 위치한 [Consul](https://www.consul.io/) 도메인 서버를 가지고 있고, 모든 Consul 이름의 접미사가 .consul.local 인 경우, CoreDNS에서 이를 구성하기 위해 클러스터 관리자는 CoreDNS 컨피그맵에서 다음 구문을 생성한다.

```
consul.local:53 {
        errors
        cache 30
        forward . 10.150.0.1
    }
```

모든 비 클러스터의 DNS 조회가 172.16.0.1 의 특정 네임서버를 통과하도록 할 경우, `/etc/resolv.conf` 대신 `forward` 를 네임서버로 지정한다.

```
forward .  172.16.0.1
```

기본 `Corefile` 구성에 따른 최종 컨피그맵은 다음과 같다.

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: coredns
  namespace: kube-system
data:
  Corefile: |
    .:53 {
        errors
        health
        kubernetes cluster.local in-addr.arpa ip6.arpa {
           pods insecure
           fallthrough in-addr.arpa ip6.arpa
        }
        prometheus :9153
        forward . 172.16.0.1
        cache 30
        loop
        reload
        loadbalance
    }
    consul.local:53 {
        errors
        cache 30
        forward . 10.150.0.1
    }
```

`Kubeadm` 툴은 kube-dns 컨피그맵에서 동일한 설정의 CoreDNS 컨피그맵으로의
자동 변환을 지원한다.

{{< note >}}
kube-dns는 스텁 도메인 및 네임서버(예: ns.foo.com)에 대한 FQDN을 허용하지만 CoreDNS에서는 이 기능을 지원하지 않는다.
변환 과정에서, 모든 FQDN 네임서버는 CoreDNS 설정에서 생략된다.
{{< /note >}}

## kube-dns에 대응되는 CoreDNS 설정

CoreDNS는 kube-dns 이상의 기능을 지원한다.
`StubDomains` 과 `upstreamNameservers` 를 지원하도록 생성된 kube-dns의 컨피그맵은 CoreDNS의 `forward` 플러그인으로 변환된다.

### 예시

kube-dns에 대한 이 컨피그맵 예제는 stubDomains 및 upstreamNameservers를 지정한다.

```yaml
apiVersion: v1
data:
  stubDomains: |
    {"abc.com" : ["1.2.3.4"], "my.cluster.local" : ["2.3.4.5"]}
  upstreamNameservers: |
    ["8.8.8.8", "8.8.4.4"]
kind: ConfigMap
```

CoreDNS에서는 동등한 설정으로 Corefile을 생성한다.

* stubDomains 에 대응하는 설정:
```yaml
abc.com:53 {
    errors
    cache 30
    forward . 1.2.3.4
}
my.cluster.local:53 {
    errors
    cache 30
    forward . 2.3.4.5
}
```

기본 플러그인으로 구성된 완전한 Corefile.

```
.:53 {
    errors
    health
    kubernetes cluster.local in-addr.arpa ip6.arpa {
        pods insecure
        fallthrough in-addr.arpa ip6.arpa
    }
    federation cluster.local {
        foo foo.feddomain.com
    }
    prometheus :9153
    forward . 8.8.8.8 8.8.4.4
    cache 30
}
abc.com:53 {
    errors
    cache 30
    forward . 1.2.3.4
}
my.cluster.local:53 {
    errors
    cache 30
    forward . 2.3.4.5
}
```

## CoreDNS로의 이관

kube-dns에서 CoreDNS로 이관하기 위하여,
kube-dns를 CoreDNS로 교체하여 적용하는 방법에 대한 상세 정보는
[블로그 기사](https://coredns.io/2018/05/21/migration-from-kube-dns-to-coredns/)를 참고한다.

또한 공식적인 CoreDNS [배포 스크립트](https://github.com/coredns/deployment/blob/master/kubernetes/deploy.sh)를
사용하여 이관할 수도 있다.


## {{% heading "whatsnext" %}}

- [DNS 변환 디버깅하기](/docs/tasks/administer-cluster/dns-debugging-resolution/) 읽기
