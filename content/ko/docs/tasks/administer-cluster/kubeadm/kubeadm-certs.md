---


title: kubeadm을 사용한 인증서 관리
content_type: task
weight: 10
---

<!-- overview -->

{{< feature-state for_k8s_version="v1.15" state="stable" >}}

[kubeadm](/ko/docs/reference/setup-tools/kubeadm/)으로 생성된 클라이언트 인증서는 1년 후에 만료된다. 이 페이지는 kubeadm으로 인증서 갱신을 관리하는 방법을 설명한다.

## {{% heading "prerequisites" %}}


[쿠버네티스의 PKI 인증서와 요구 조건](/ko/docs/setup/best-practices/certificates/)에 익숙해야 한다.

<!-- steps -->

## 사용자 정의 인증서 사용 {#custom-certificates}

기본적으로, kubeadm은 클러스터를 실행하는 데 필요한 모든 인증서를 생성한다.
사용자는 자체 인증서를 제공하여 이 동작을 무시할 수 있다.

이렇게 하려면, `--cert-dir` 플래그 또는 kubeadm `ClusterConfiguration` 의
`certificatesDir` 필드에 지정된 디렉터리에 배치해야 한다.
기본적으로  `/etc/kubernetes/pki` 이다.

`kubeadm init` 을 실행하기 전에 지정된 인증서와 개인 키(private key) 쌍이 존재하면,
kubeadm은 이를 덮어 쓰지 않는다. 이는 예를 들어, 기존 CA를
`/etc/kubernetes/pki/ca.crt` 와 `/etc/kubernetes/pki/ca.key` 에
복사할 수 있고, kubeadm은 이 CA를 사용하여 나머지 인증서에 서명한다는 걸 의미한다.

## 외부 CA 모드 {#external-ca-mode}

`ca.key` 파일이 아닌 `ca.crt` 파일만 제공할
수도 있다(이는 다른 인증서 쌍이 아닌 루트 CA 파일에만 사용 가능함).
다른 모든 인증서와 kubeconfig 파일이 있으면, kubeadm은 이 조건을
인식하고 "외부 CA" 모드를 활성화한다. kubeadm은 디스크에
CA 키없이 진행한다.

대신, `--controllers=csrsigner` 사용하여 controller-manager를
독립적으로 실행하고 CA 인증서와 키를 가리킨다.

[PKI 인증서와 요구 조건](/ko/docs/setup/best-practices/certificates/)은 외부 CA를
사용하도록 클러스터 설정에 대한 지침을 포함한다.

## 인증서 만료 확인

`check-expiration` 하위 명령을 사용하여 인증서가 만료되는 시기를 확인할 수 있다.

```
kubeadm certs check-expiration
```

출력 결과는 다음과 비슷하다.

```
CERTIFICATE                EXPIRES                  RESIDUAL TIME   CERTIFICATE AUTHORITY   EXTERNALLY MANAGED
admin.conf                 Dec 30, 2020 23:36 UTC   364d                                    no
apiserver                  Dec 30, 2020 23:36 UTC   364d            ca                      no
apiserver-etcd-client      Dec 30, 2020 23:36 UTC   364d            etcd-ca                 no
apiserver-kubelet-client   Dec 30, 2020 23:36 UTC   364d            ca                      no
controller-manager.conf    Dec 30, 2020 23:36 UTC   364d                                    no
etcd-healthcheck-client    Dec 30, 2020 23:36 UTC   364d            etcd-ca                 no
etcd-peer                  Dec 30, 2020 23:36 UTC   364d            etcd-ca                 no
etcd-server                Dec 30, 2020 23:36 UTC   364d            etcd-ca                 no
front-proxy-client         Dec 30, 2020 23:36 UTC   364d            front-proxy-ca          no
scheduler.conf             Dec 30, 2020 23:36 UTC   364d                                    no

CERTIFICATE AUTHORITY   EXPIRES                  RESIDUAL TIME   EXTERNALLY MANAGED
ca                      Dec 28, 2029 23:36 UTC   9y              no
etcd-ca                 Dec 28, 2029 23:36 UTC   9y              no
front-proxy-ca          Dec 28, 2029 23:36 UTC   9y              no
```

이 명령은 `/etc/kubernetes/pki` 폴더의 클라이언트 인증서와 kubeadm이 사용하는 KUBECONFIG 파일(`admin.conf`, `controller-manager.conf` 및 `scheduler.conf`)에 포함된 클라이언트 인증서의 만료/잔여 기간을 표시한다.

또한, kubeadm은 인증서가 외부에서 관리되는지를 사용자에게 알린다. 이 경우 사용자는 수동으로 또는 다른 도구를 사용해서 인증서 갱신 관리를 해야 한다.

{{< warning >}}
`kubeadm` 은 외부 CA가 서명한 인증서를 관리할 수 없다.
{{< /warning >}}

{{< note >}}
`kubelet.conf` 는 위 목록에 포함되어 있지 않은데, 이는
kubeadm이 [자동 인증서 갱신](/ko/docs/tasks/tls/certificate-rotation/)을 위해 
`/var/lib/kubelet/pki`에 있는 갱신 가능한 인증서를 이용하여 kubelet을 구성하기 때문이다.
만료된 kubelet 클라이언트 인증서를 갱신하려면 
[kubelet 클라이언트 갱신 실패](/docs/setup/production-environment/tools/kubeadm/troubleshooting-kubeadm/#kubelet-client-cert) 섹션을 확인한다.
{{< /note >}}

{{< warning >}}
kubeadm 1.17 이전의 버전에서 `kubeadm init` 으로 작성된 노드에는
`kubelet.conf` 의 내용을 수동으로 수정해야 하는 [버그](https://github.com/kubernetes/kubeadm/issues/1753)가 있다. `kubeadm init` 수행 완료 후, `client-certificate-data` 및 `client-key-data` 를 다음과 같이 교체하여,
로테이트된 kubelet 클라이언트 인증서를 가리키도록 `kubelet.conf` 를 업데이트해야 한다.

```yaml
client-certificate: /var/lib/kubelet/pki/kubelet-client-current.pem
client-key: /var/lib/kubelet/pki/kubelet-client-current.pem
```
{{< /warning >}}

## 자동 인증서 갱신

kubeadm은 컨트롤 플레인 [업그레이드](/ko/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/) 동안 모든 인증서를 갱신한다.

이 기능은 가장 간단한 유스케이스를 해결하기 위해 설계되었다.
인증서 갱신에 대해 특별한 요구 사항이 없고 쿠버네티스 버전 업그레이드를 정기적으로(매 1년 이내 업그레이드 수행) 수행하는 경우, kubeadm은 클러스터를 최신 상태로 유지하고 합리적으로 보안을 유지한다.

{{< note >}}
보안을 유지하려면 클러스터를 자주 업그레이드하는 것이 가장 좋다.
{{< /note >}}

인증서 갱신에 대해 보다 복잡한 요구 사항이 있는 경우, `--certificate-renewal=false` 를 `kubeadm upgrade apply` 또는 `kubeadm upgrade node` 와 함께 사용하여 기본 동작이 수행되지 않도록 할 수 있다.

{{< warning >}}
kubeadm 1.17 이전 버전에는 `kubeadm upgrade node` 명령에서
`--certificate-renewal` 의 기본값이 `false` 인 [버그](https://github.com/kubernetes/kubeadm/issues/1818)가
있다. 이 경우 `--certificate-renewal=true` 를 명시적으로 설정해야 한다.
{{< /warning >}}

## 수동 인증서 갱신

`kubeadm certs renew` 명령을 사용하여 언제든지 인증서를 수동으로 갱신할 수 있다.

이 명령은 `/etc/kubernetes/pki` 에 저장된 CA(또는 프론트 프록시 CA) 인증서와 키를 사용하여 갱신을 수행한다.

{{< warning >}}
HA 클러스터를 실행 중인 경우, 모든 컨트롤 플레인 노드에서 이 명령을 실행해야 한다.
{{< /warning >}}

{{< note >}}
`certs renew` 는 기존 인증서를 kubeadm-config 컨피그맵(ConfigMap) 대신 속성(공통 이름, 조직, SAN 등)의 신뢰할 수 있는 소스로 사용한다. 둘 다 동기화 상태를 유지하는 것을 강력히 권장한다.
{{< /note >}}

`kubeadm certs renew` 는 다음의 옵션을 제공한다.

쿠버네티스 인증서는 일반적으로 1년 후 만료일에 도달한다.

- `--csr-only` 는 실제로 인증서를 갱신하지 않고 인증서 서명 요청을 생성하여 외부 CA로 인증서를 갱신하는 데 사용할 수 있다. 자세한 내용은 다음 단락을 참고한다.

- 모든 인증서 대신 단일 인증서를 갱신할 수도 있다.

## 쿠버네티스 인증서 API를 사용하여 인증서 갱신

이 섹션에서는 쿠버네티스 인증서 API를 사용하여 수동 인증서 갱신을 실행하는 방법에 대한 자세한 정보를 제공한다.

{{< caution >}}
조직의 인증서 인프라를 kubeadm으로 생성된 클러스터에 통합해야 하는 사용자를 위한 고급 주제이다. 기본 kubeadm 구성이 요구 사항을 충족하면 kubeadm이 인증서를 대신 관리하도록 해야 한다.
{{< /caution >}}

### 서명자 설정

쿠버네티스 인증 기관(Certificate Authority)은 기본적으로 작동하지 않는다.
[cert-manager](https://docs.cert-manager.io/en/latest/tasks/issuers/setup-ca.html)와 같은 외부 서명자를 설정하거나, 빌트인 서명자를 사용할 수 있다.

빌트인 서명자는 [`kube-controller-manager`](/docs/reference/command-line-tools-reference/kube-controller-manager/)의 일부이다.

빌트인 서명자를 활성화하려면, `--cluster-signing-cert-file` 와 `--cluster-signing-key-file` 플래그를 전달해야 한다.

새 클러스터를 생성하는 경우, kubeadm [구성 파일](https://godoc.org/k8s.io/kubernetes/cmd/kubeadm/app/apis/kubeadm/v1beta2)을 사용할 수 있다.

```yaml
apiVersion: kubeadm.k8s.io/v1beta2
kind: ClusterConfiguration
controllerManager:
  extraArgs:
    cluster-signing-cert-file: /etc/kubernetes/pki/ca.crt
    cluster-signing-key-file: /etc/kubernetes/pki/ca.key
```

### 인증서 서명 요청(CSR) 생성

쿠버네티스 API로 CSR을 작성하려면 [CertificateSigningRequest 생성](/docs/reference/access-authn-authz/certificate-signing-requests/#create-certificatesigningrequest)을 본다.

## 외부 CA로 인증서 갱신

이 섹션에서는 외부 CA를 사용하여 수동 인증서 갱신을 실행하는 방법에 대한 자세한 정보를 제공한다.

외부 CA와 보다 효과적으로 통합하기 위해 kubeadm은 인증서 서명 요청(CSR)을 생성할 수도 있다.
CSR은 클라이언트의 서명된 인증서에 대한 CA 요청을 나타낸다.
kubeadm 관점에서, 일반적으로 온-디스크(on-disk) CA에 의해 서명되는 모든 인증서는 CSR로 생성될 수 있다. 그러나 CA는 CSR로 생성될 수 없다.

### 인증서 서명 요청(CSR) 생성

`kubeadm certs renew --csr-only` 로 인증서 서명 요청을 만들 수 있다.

CSR과 함께 제공되는 개인 키가 모두 출력된다.
`--csr-dir` 로 사용할 디텍터리를 전달하여 지정된 위치로 CSR을 출력할 수 있다.
`--csr-dir` 을 지정하지 않으면, 기본 인증서 디렉터리(`/etc/kubernetes/pki`)가 사용된다.

`kubeadm certs renew --csr-only` 로 인증서를 갱신할 수 있다.
`kubeadm init` 과 마찬가지로 출력 디렉터리를 `--csr-dir` 플래그로 지정할 수 있다.

CSR에는 인증서 이름, 도메인 및 IP가 포함되지만, 용도를 지정하지는 않는다.
인증서를 발행할 때 [올바른 인증서 용도](/ko/docs/setup/best-practices/certificates/#모든-인증서)를
지정하는 것은 CA의 책임이다.

* `openssl` 의 경우
  [`openssl ca` 명령](https://superuser.com/questions/738612/openssl-ca-keyusage-extension)으로 수행한다.
* `cfssl` 의 경우
  [설정 파일에 용도](https://github.com/cloudflare/cfssl/blob/master/doc/cmd/cfssl.txt#L170)를 지정한다.

선호하는 방법으로 인증서에 서명한 후, 인증서와 개인 키를 PKI 디렉터리(기본적으로 `/etc/kubernetes/pki`)에 복사해야 한다.

## 인증 기관(CA) 순환(rotation) {#certificate-authority-rotation}

Kubeadm은 CA 인증서의 순환이나 교체 기능을 기본적으로 지원하지 않는다.

CA의 수동 순환이나 교체에 대한 보다 상세한 정보는 [CA 인증서 수동 순환](/docs/tasks/tls/manual-rotation-of-ca-certificates/) 문서를 참조한다.

## 서명된 kubelet 인증서 활성화하기 {#kubelet-serving-certs}

기본적으로 kubeadm에 의해서 배포된 kubelet 인증서는 자가 서명된(self-signed) 것이다.
이것은 [metrics-server](https://github.com/kubernetes-sigs/metrics-server)와
같은 외부 서비스의 kubelet에 대한 연결은
TLS로 보안되지 않음을 의미한다.

제대로 서명된 인증서를 얻기 위해서 신규 kubeadm 클러스터의 kubelet을 구성하려면
다음의 최소 구성을 `kubeadm init` 에 전달해야 한다.

```yaml
apiVersion: kubeadm.k8s.io/v1beta2
kind: ClusterConfiguration
---
apiVersion: kubelet.config.k8s.io/v1beta1
kind: KubeletConfiguration
serverTLSBootstrap: true
```

만약 이미 클러스터를 생성했다면 다음을 따라 이를 조정해야 한다.
 - `kube-system` 네임스페이스에서 `kubelet-config-{{< skew latestVersion >}}` 컨피그맵을 찾아서 수정한다.
해당 컨피그맵에는 `kubelet` 키가
[KubeletConfiguration](/docs/reference/config-api/kubelet-config.v1beta1/#kubelet-config-k8s-io-v1beta1-KubeletConfiguration)
문서를 값으로 가진다. `serverTLSBootstrap: true` 가 되도록 KubeletConfiguration 문서를 수정한다.
- 각 노드에서, `serverTLSBootstrap: true` 필드를 `/var/lib/kubelet/config.yaml` 에 추가한다.
그리고 `systemctl restart kubelet` 로 kubelet을 재시작한다.

`serverTLSBootstrap: true` 필드는 kubelet 인증서를 이용한 부트스트랩을
`certificates.k8s.io` API에 요청함으로써 활성화할 것이다. 한 가지 알려진 제약은
이 인증서들에 대한 CSR(인증서 서명 요청)들이 kube-controller-manager -
[`kubernetes.io/kubelet-serving`](/docs/reference/access-authn-authz/certificate-signing-requests/#kubernetes-signers)의
기본 서명자(default signer)에 의해서 자동으로 승인될 수 없다는 점이다.
이것은 사용자나 제 3의 컨트롤러의 액션을 필요로 할 것이다.

이 CSR들은 다음을 통해 볼 수 있다.

```shell
kubectl get csr
NAME        AGE     SIGNERNAME                        REQUESTOR                      CONDITION
csr-9wvgt   112s    kubernetes.io/kubelet-serving     system:node:worker-1           Pending
csr-lz97v   1m58s   kubernetes.io/kubelet-serving     system:node:control-plane-1    Pending
```

이를 승인하기 위해서는 다음을 수행한다.
```shell
kubectl certificate approve <CSR-name>
```

기본적으로, 이 인증서는 1년 후에 만기될 것이다. Kubeadm은
`KubeletConfiguration` 필드의 `rotateCertificates` 를 `true` 로 설정한다. 이것은 만기가
다가오면 인증서를 위한 신규 CSR 세트가 생성되는 것을 의미하며,
해당 순환(rotation)을 완료하기 위해서는 승인이 되어야 한다는 것을 의미한다. 더 상세한 이해를 위해서는
[인증서 순환](/docs/reference/command-line-tools-reference/kubelet-tls-bootstrapping/#certificate-rotation)를 확인한다.

만약 이 CSR들의 자동 승인을 위한 솔루션을 찾고 있다면 클라우드 제공자와
연락하여 대역 외 메커니즘(out of band mechanism)을 통해 노드의 신분을 검증할 수 있는
CSR 서명자를 가지고 있는지 문의하는 것을 추천한다.

{{% thirdparty-content %}}

제 3 자 커스텀 컨트롤러도 사용될 수 있다.
- [kubelet-rubber-stamp](https://github.com/kontena/kubelet-rubber-stamp)

이러한 컨트롤러는 CSR의 CommonName과 요청된 IPs 및 도메인 네임을
모두 검증하지 않는 한, 보안이 되는 메커니즘이 아니다. 이것을 통해 악의적 행위자가
kubelet 인증서(클라이언트 인증)를 사용하여 아무 IP나 도메인 네임에 대해 인증서를
요청하는 CSR의 생성을 방지할 수 있을 것이다.
