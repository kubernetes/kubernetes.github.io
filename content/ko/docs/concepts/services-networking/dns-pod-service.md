---



title: 서비스 및 파드용 DNS
content_type: concept
weight: 20
---
<!-- overview -->

쿠버네티스는 파드와 서비스를 위한 DNS 레코드를 생성한다. 사용자는 IP 주소 대신에
일관된 DNS 네임을 통해서 서비스에 접속할 수 있다.

<!-- body -->

## 소개

쿠버네티스 DNS는 클러스터의 서비스와 DNS 파드를 관리하며,
개별 컨테이너들이 DNS 네임을 해석할 때
DNS 서비스의 IP를 사용하도록 kubelets를 구성한다.

클러스터 내의 모든 서비스(DNS 서버 자신도 포함하여)에는 DNS 네임이 할당된다.
기본적으로 클라이언트 파드의 DNS 검색 리스트는 파드 자체의 네임스페이스와
클러스터의 기본 도메인을 포함한다.

### 서비스의 네임스페이스

DNS 쿼리는 그것을 생성하는 파드의 네임스페이스에 따라 다른 결과를 반환할 수
있다. 네임스페이스를 지정하지 않은 DNS 쿼리는 파드의 네임스페이스에
국한된다. DNS 쿼리에 네임스페이스를 명시하여 다른 네임스페이스에 있는 서비스에 접속한다.

예를 들어, `test` 네임스페이스에 있는 파드를 생각해보자. `data` 서비스는
`prod` 네임스페이스에 있다.

이 경우, `data` 에 대한 쿼리는 파드의 `test` 네임스페이스를 사용하기 때문에 결과를 반환하지 않을 것이다.

`data.prod` 로 쿼리하면 의도한 결과를 반환할 것이다. 왜냐하면
네임스페이스가 명시되어 있기 때문이다.

DNS 쿼리는 파드의 `/etc/resolv.conf` 를 사용하여 확장될 수 있을 것이다. Kubelet은
각 파드에 대해서 파일을 설정한다. 예를 들어, `data` 만을 위한 쿼리는
`data.test.cluster.local` 로 확장된다. `search` 옵션의 값은
쿼리를 확장하기 위해서 사용된다. DNS 쿼리에 대해 더 자세히 알고 싶은 경우,
[`resolv.conf` 설명 페이지.](https://www.man7.org/linux/man-pages/man5/resolv.conf.5.html)를 참고한다.

```
nameserver 10.32.0.10
search <namespace>.svc.cluster.local svc.cluster.local cluster.local
options ndots:5
```

요약하면, _test_ 네임스페이스에 있는 파드는 `data.prod` 또는
`data.prod.cluster.local` 중 하나를 통해 성공적으로 해석될 수 있다.

### DNS 레코드

어떤 오브젝트가 DNS 레코드를 가지는가?

1. 서비스
2. 파드

다음 섹션은 지원되는 DNS 레코드의 종류 및 레이아웃에 대한 상세
내용이다. 혹시 동작시킬 필요가 있는 다른 레이아웃, 네임, 또는 쿼리는
구현 세부 사항으로 간주되며 경고 없이 변경될 수 있다.
최신 명세 확인을 위해서는,
[쿠버네티스 DNS-기반 서비스 디스커버리](https://github.com/kubernetes/dns/blob/master/docs/specification.md)를 본다.

## 서비스

### A/AAAA 레코드

"노멀"(헤드리스가 아닌) 서비스는 서비스 IP 계열에 따라
`my-svc.my-namespace.svc.cluster-domain.example`
형식의 이름을 가진 DNS A 또는 AAAA 레코드가 할당된다. 이는 서비스의 클러스터
IP로 해석된다.

"헤드리스"(클러스터 IP가 없는) 서비스 또한 서비스 IP 계열에 따라
`my-svc.my-namespace.svc.cluster-domain.example`
형식의 이름을 가진 DNS A 또는 AAAA 레코드가 할당된다.
노멀 서비스와는 다르게 이는 서비스에 의해 선택된 파드들의 IP 집합으로 해석된다.
클라이언트는 해석된 IP 집합에서 IP를 직접 선택하거나 표준 라운드로빈을
통해 선택할 수 있다.

### SRV 레코드

SRV 레코드는 노멀 서비스 또는
[헤드리스 서비스](/ko/docs/concepts/services-networking/service/#헤드리스-headless-서비스)에
속하는 네임드 포트를 위해 만들어졌다. 각각의 네임드 포트에 대해서 SRV 레코드는 다음과 같은 형식을 가질 수 있다.
`_my-port-name._my-port-protocol.my-svc.my-namespace.svc.cluster-domain.example`.
정규 서비스의 경우, 이는 포트 번호와 도메인 네임으로 해석된다.
`my-svc.my-namespace.svc.cluster-domain.example`.
헤드리스 서비스의 경우, 서비스를 지원하는 각 파드에 대해 하나씩 복수 응답으로 해석되며 이 응답은 파드의
포트 번호와 도메인 이름을 포함한다.
`auto-generated-name.my-svc.my-namespace.svc.cluster-domain.example`.

## 파드

### A/AAAA 레코드

일반적으로 파드에는 다음과 같은 DNS 주소를 갖는다.

`pod-ip-address.my-namespace.pod.cluster-domain.example`.

예를 들어, `default` 네임스페이스의 파드에 IP 주소 172.17.0.3이 있고,
클러스터의 도메인 이름이 `cluster.local` 이면, 파드는 다음과 같은 DNS 주소를 갖는다.

`172-17-0-3.default.pod.cluster.local`.

서비스에 의해 노출된 디플로이먼트(Deployment)나 데몬셋(DaemonSet)에 의해 생성된
모든 파드는 다음과 같은 DNS 주소를 갖는다.

`pod-ip-address.deployment-name.my-namespace.svc.cluster-domain.example`.

### 파드의 hostname 및 subdomain 필드

파드가 생성되면 hostname은 해당 파드의 `metadata.name` 값이 된다.

파드 스펙(Pod spec)에는 선택적 필드인 `hostname`이 있다.
이 필드는 파드의 호스트네임을 지정할 수 있다.
`hostname` 필드가 지정되면, 파드의 이름보다 파드의 호스트네임이 우선시된다.
예를 들어 `hostname` 필드가 "`my-host`"로 설정된 파드는 호스트네임이 "`my-host`"로 설정된다.

또한, 파드 스펙에는 선택적 필드인 `subdomain`이 있다. 이 필드는 서브도메인을 지정할 수 있다.
예를 들어 "`my-namespace`" 네임스페이스에서, `hostname` 필드가 "`foo`"로 설정되고,
`subdomain` 필드가 "`bar`"로 설정된 파드는 전체 주소 도메인 네임(FQDN)을 가지게 된다.
"`foo.bar.my-namespace.svc.cluster-domain.example`".

예시:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: default-subdomain
spec:
  selector:
    name: busybox
  clusterIP: None
  ports:
  - name: foo # 사실 포트는 필요하지 않다.
    port: 1234
    targetPort: 1234
---
apiVersion: v1
kind: Pod
metadata:
  name: busybox1
  labels:
    name: busybox
spec:
  hostname: busybox-1
  subdomain: default-subdomain
  containers:
  - image: busybox:1.28
    command:
      - sleep
      - "3600"
    name: busybox
---
apiVersion: v1
kind: Pod
metadata:
  name: busybox2
  labels:
    name: busybox
spec:
  hostname: busybox-2
  subdomain: default-subdomain
  containers:
  - image: busybox:1.28
    command:
      - sleep
      - "3600"
    name: busybox
```

파드와 동일한 네임스페이스 내에 같은 서브도메인 이름을 가진 헤드리스 서비스가 있다면,
클러스터의 DNS 서버는 파드의 전체 주소 호스트네임(fully qualified hostname)인 A 또는 AAAA 레코드를 반환한다.
예를 들어 호스트네임이 "`busybox-1`"이고,
서브도메인이 "`default-subdomain`"이고,
같은 네임스페이스 내 헤드리스 서비스의 이름이 "`default-subdomain`"이면,
파드는 다음과 같이 자기 자신의 FQDN을 얻게 된다.
"`busybox-1.default-subdomain.my-namespace.svc.cluster-domain.example`".
DNS는 위 FQDN에 대해 파드의 IP를 가리키는 A 또는 AAAA 레코드를 제공한다.
"`busybox1`"와 "`busybox2`" 파드 모두 각 파드를 구분 가능한 A 또는 AAAA 레코드를 가지고 있다.

엔드포인트 오브젝트는 `hostname` 필드를
임의의 엔드포인트 IP 주소로 지정할 수 있다.

{{< note >}}
A 또는 AAAA 레코드는 파드의 이름으로 생성되지 않기 때문에
파드의 A 또는 AAAA 레코드를 생성하기 위해서는 `hostname` 필드를 작성해야 한다.
`hostname` 필드는 없고 `subdomain` 필드만 있는 파드는 파드의 IP 주소를 가리키는 헤드리스 서비스의
A 또는 AAAA 레코드만 생성할 수 있다. (`default-subdomain.my-namespace.svc.cluster-domain.example`)
또한 서비스에서 `publishNotReadyAddresses=True` 를 설정하지 않았다면, 파드가 준비 상태가 되어야 레코드를 가질 수 있다.
{{< /note >}}

### 파드의 setHostnameAsFQDN 필드 {#pod-sethostnameasfqdn-field}

{{< feature-state for_k8s_version="v1.20" state="beta" >}}

파드가 전체 주소 도메인 이름(FQDN)을 갖도록 구성된 경우, 해당 호스트네임은 짧은 호스트네임이다. 예를 들어, 전체 주소 도메인 이름이 `busybox-1.default-subdomain.my-namespace.svc.cluster-domain.example` 인 파드가 있는 경우, 기본적으로 해당 파드 내부의 `hostname` 명령어는 `busybox-1` 을 반환하고 `hostname --fqdn` 명령은 FQDN을 반환한다.

파드 명세에서 `setHostnameAsFQDN: true` 를 설정하면, kubelet은 파드의 FQDN을 해당 파드 네임스페이스의 호스트네임에 기록한다. 이 경우, `hostname` 과 `hostname --fqdn` 은 모두 파드의 FQDN을 반환한다.

{{< note >}}
리눅스에서, 커널의 호스트네임 필드(`struct utsname` 의 `nodename` 필드)는 64자로 제한된다.

파드에서 이 기능을 사용하도록 설정하고 FQDN이 64자보다 길면, 시작되지 않는다. 파드는 파드 호스트네임과 클러스터 도메인에서 FQDN을 구성하지 못한다거나, FQDN `long-FDQN` 이 너무 길다(최대 64자, 70자 요청인 경우)와 같은 오류 이벤트를 생성하는 `Pending` 상태(`kubectl` 에서 표시하는 `ContainerCreating`)로 유지된다. 이 시나리오에서 사용자 경험을 개선하는 한 가지 방법은 사용자가 최상위 레벨을 오브젝트(예를 들어, 디플로이먼트)를 생성할 때 FQDN 크기를 제어하기 위해 [어드미션 웹훅 컨트롤러](/docs/reference/access-authn-authz/extensible-admission-controllers/#admission-webhooks)를 생성하는 것이다.
{{< /note >}}

### 파드의 DNS 정책

DNS 정책은 파드별로 설정할 수 있다.
현재 쿠버네티스는 다음과 같은 파드별 DNS 정책을 지원한다.
이 정책들은 파드 스펙의 `dnsPolicy` 필드에서 지정할 수 있다.

- "`Default`": 파드는 파드가 실행되고 있는 노드로부터 네임 해석 설정(the name resolution configuration)을 상속받는다.
  자세한 내용은
  [관련 논의](/ko/docs/tasks/administer-cluster/dns-custom-nameservers/)에서
  확인할 수 있다.
- "`ClusterFirst`": "`www.kubernetes.io`"와 같이 클러스터 도메인 suffix 구성과
  일치하지 않는 DNS 쿼리는 노드에서 상속된 업스트림 네임서버로 전달된다.
  클러스터 관리자는 추가 스텁-도메인(stub-domain)과 업스트림 DNS 서버를 구축할 수 있다.
  그러한 경우 DNS 쿼리를 어떻게 처리하는지에 대한 자세한 내용은
  [관련 논의](/ko/docs/tasks/administer-cluster/dns-custom-nameservers/)에서
  확인할 수 있다.
- "`ClusterFirstWithHostNet`": hostNetwork에서 running 상태인 파드의 경우 DNS 정책인
  "`ClusterFirstWithHostNet`"을 명시적으로 설정해야 한다.
- "`None`": 이 정책은 파드가 쿠버네티스 환경의 DNS 설정을 무시하도록 한다.
  모든 DNS 설정은 파드 스펙 내에 `dnsConfig`필드를 사용하여 제공해야 한다.
  아래 절인 [파드의 DNS 설정](#pod-dns-config)에서
  자세한 내용을 확인할 수 있다.

{{< note >}}
"Default"는 기본 DNS 정책이 아니다. `dnsPolicy`가 명시적으로 지정되어있지 않다면
"ClusterFirst"가 기본값으로 사용된다.
{{< /note >}}


아래 예시는 `hostNetwork`필드가 `true`로 설정되어 있어서
DNS 정책이 "`ClusterFirstWithHostNet`"으로 설정된 파드를 보여준다.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: busybox
  namespace: default
spec:
  containers:
  - image: busybox:1.28
    command:
      - sleep
      - "3600"
    imagePullPolicy: IfNotPresent
    name: busybox
  restartPolicy: Always
  hostNetwork: true
  dnsPolicy: ClusterFirstWithHostNet
```

### 파드의 DNS 설정 {#pod-dns-config}

{{< feature-state for_k8s_version="v1.14" state="stable" >}}

사용자들은 파드의 DNS 설정을 통해서 직접 파드의 DNS를 세팅할 수 있다.

`dnsConfig` 필드는 선택적이고, `dnsPolicy` 세팅과 함께 동작한다.
이때, 파드의 `dnsPolicy`의 값이 "`None`"으로 설정되어 있어야
`dnsConfig` 필드를 지정할 수 있다.

사용자는 `dnsConfig` 필드에서 다음과 같은 속성들을 지정할 수 있다.

- `nameservers`: 파드의 DNS 서버가 사용할 IP 주소들의 목록이다.
   파드의 `dnsPolicy`가 "`None`" 으로 설정된 경우에는
   적어도 하나의 IP 주소가 포함되어야 하며,
   그렇지 않으면 이 속성은 생략할 수 있다.
   `nameservers`에 나열된 서버는 지정된 DNS 정책을 통해 생성된 기본 네임 서버와 합쳐지며
   중복되는 주소는 제거된다.
- `searches`: 파드의 호스트네임을 찾기 위한 DNS 검색 도메인의 목록이다.
   이 속성은 생략이 가능하며,
   값을 지정한 경우 나열된 검색 도메인은 지정된 DNS 정책을 통해 생성된 기본 검색 도메인에 합쳐진다.
   병합 시 중복되는 도메인은 제거되며,
   쿠버네티스는 최대 6개의 검색 도메인을 허용하고 있다.
- `options`: `name` 속성(필수)과 `value` 속성(선택)을 가질 수 있는 오브젝트들의 선택적 목록이다.
   이 속성의 내용은 지정된 DNS 정책에서 생성된 옵션으로 병합된다.
   이 속성의 내용은 지정된 DNS 정책을 통해 생성된 옵션으로 합쳐지며,
   병합 시 중복되는 항목은 제거된다.

다음은 커스텀 DNS 세팅을 한 파드의 예시이다.

{{< codenew file="service/networking/custom-dns.yaml" >}}

위에서 파드가 생성되면,
컨테이너 `test`의 `/etc/resolv.conf` 파일에는 다음과 같은 내용이 추가된다.

```
nameserver 1.2.3.4
search ns1.svc.cluster-domain.example my.dns.search.suffix
options ndots:2 edns0
```

IPv6 셋업을 위해서 검색 경로와 네임 서버 셋업은 다음과 같아야 한다:

```shell
kubectl exec -it dns-example -- cat /etc/resolv.conf
```
출력은 다음과 같은 형식일 것이다.
```shell
nameserver fd00:79:30::a
search default.svc.cluster-domain.example svc.cluster-domain.example cluster-domain.example
options ndots:5
```

## {{% heading "whatsnext" %}}


DNS 구성 관리에 대한 지침은
[DNS 서비스 구성](/ko/docs/tasks/administer-cluster/dns-custom-nameservers/)에서 확인할 수 있다.
