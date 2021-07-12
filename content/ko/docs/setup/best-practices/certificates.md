---
title: PKI 인증서 및 요구 사항
content_type: concept
weight: 40
---

<!-- overview -->

쿠버네티스는 TLS를 통한 인증을 위해서 PKI 인증서가 필요하다.
만약 [kubeadm](/ko/docs/reference/setup-tools/kubeadm/)으로 쿠버네티스를 설치한다면, 클러스터에 필요한 인증서는 자동으로 생성된다.
또한 더 안전하게 자신이 소유한 인증서를 생성할 수 있다. 이를 테면, 개인키를 API 서버에 저장하지 않으므로 더 안전하게 보관할 수 있다.
이 페이지는 클러스터가 필요로 하는 인증서에 대해서 설명한다.



<!-- body -->

## 클러스터에서 인증서가 이용되는 방식

쿠버네티스는 다음 작업에서 PKI를 필요로 한다.

* kubelet에서 API 서버 인증서를 인증시 사용하는 클라이언트 인증서
* API 서버 엔드포인트를 위한 서버 인증서
* API 서버에 클러스터 관리자 인증을 위한 클라이언트 인증서
* API 서버에서 kubelet과 통신을 위한 클라이언트 인증서
* API 서버에서 etcd 간의 통신을 위한 클라이언트 인증서
* 컨트롤러 매니저와 API 서버 간의 통신을 위한 클라이언트 인증서/kubeconfig
* 스케줄러와 API 서버간 통신을 위한 클라이언트 인증서/kubeconfig
* [front-proxy](/docs/tasks/extend-kubernetes/configure-aggregation-layer/)를 위한 클라이언트와 서버 인증서

{{< note >}}
`front-proxy` 인증서는 kube-proxy에서 [API 서버 확장](/ko/docs/tasks/extend-kubernetes/setup-extension-api-server/)을 지원할 때만 kube-proxy에서 필요하다.
{{< /note >}}

etcd 역시 클라이언트와 피어 간에 상호 TLS 인증을 구현한다.

## 인증서를 저장하는 위치

만약 쿠버네티스를 kubeadm으로 설치했다면 인증서는 `/etc/kubernetes/pki`에 저장된다. 이 문서에 언급된 모든 파일 경로는 그 디렉터리에 상대적이다.

## 인증서 수동 설정

필요한 인증서를 kubeadm으로 생성하기 싫다면 다음 방법 중 하나로 생성할 수 있다.

### 단일 루트 CA

관리자에 의해 제어되는 단일 루트 CA를 만들 수 있다. 이 루트 CA는 여러 중간 CA를 생성할 수 있고, 모든 추가 생성에 관해서도 쿠버네티스 자체에 위임할 수 있다.

필요 CA:

| 경로                   | 기본 CN                   | 설명                      |
|------------------------|---------------------------|----------------------------------|
| ca.crt,key             | kubernetes-ca             | 쿠버네티스 일반 CA               |
| etcd/ca.crt,key        | etcd-ca                   | 모든 etcd 관련 기능을 위해서     |
| front-proxy-ca.crt,key | kubernetes-front-proxy-ca | [front-end proxy](/docs/tasks/extend-kubernetes/configure-aggregation-layer/) 위해서  |

위의 CA외에도, 서비스 계정 관리를 위한 공개/개인 키 쌍인 `sa.key` 와 `sa.pub` 을 얻는 것이 필요하다.

### 모든 인증서

이런 개인키를 API 서버에 복사하기 원치 않는다면, 모든 인증서를 스스로 생성할 수 있다.

필요한 인증서:

| 기본 CN                       | 부모 CA                   | O (주체에서)   | 종류                                   | 호스트  (SAN)                                |
|-------------------------------|---------------------------|----------------|----------------------------------------|---------------------------------------------|
| kube-etcd                     | etcd-ca                   |                | server, client                         | `localhost`, `127.0.0.1`                        |
| kube-etcd-peer                | etcd-ca                   |                | server, client                         | `<hostname>`, `<Host_IP>`, `localhost`, `127.0.0.1` |
| kube-etcd-healthcheck-client  | etcd-ca                   |                | client                                 |                                             |
| kube-apiserver-etcd-client    | etcd-ca                   | system:masters | client                                 |                                             |
| kube-apiserver                | kubernetes-ca             |                | server                                 | `<hostname>`, `<Host_IP>`, `<advertise_IP>`, `[1]` |
| kube-apiserver-kubelet-client | kubernetes-ca             | system:masters | client                                 |                                             |
| front-proxy-client            | kubernetes-front-proxy-ca |                | client                                 |                                             |

[1]: 클러스터에 접속한 다른 IP 또는 DNS 이름([kubeadm](/ko/docs/reference/setup-tools/kubeadm/) 이 사용하는 로드 밸런서 안정 IP 또는 DNS 이름, `kubernetes`, `kubernetes.default`, `kubernetes.default.svc`,
`kubernetes.default.svc.cluster`, `kubernetes.default.svc.cluster.local`)

`kind`는 하나 이상의 [x509 키 사용](https://godoc.org/k8s.io/api/certificates/v1beta1#KeyUsage) 종류를 가진다.

| 종류   | 키 사용                                                                         |
|--------|---------------------------------------------------------------------------------|
| server | digital signature, key encipherment, server auth                                |
| client | digital signature, key encipherment, client auth                                |

{{< note >}}
위에 나열된 호스트/SAN은 작업 중인 클러스터를 획득하는데 권장된다. 특정 설정이 필요한 경우, 모든 서버 인증서에 SAN을 추가할 수 있다.
{{< /note >}}

{{< note >}}
kubeadm 사용자만 해당:

* 개인 키 없이 클러스터 CA 인증서에 복사하는 시나리오는 kubeadm 문서에서 외부 CA라고 한다.
* 위 목록을 kubeadm이 생성한 PKI와 비교하는 경우, `kube-etcd`, `kube-etcd-peer` 와 `kube-etcd-healthcheck-client` 인증서는
  외부 etcd 케이스에서는 생성하지 않는 것을 알고 있어야 한다.

{{< /note >}}

### 인증서 파일 경로

인증서는 권고하는 파일 경로에 존재해야 한다([kubeadm](/ko/docs/reference/setup-tools/kubeadm/)에서 사용되는 것처럼). 경로는 위치에 관계없이 주어진 파라미터를 사용하여 지정해야 한다.

| 기본 CN                      | 권고되는 키 파일 경로         | 권고하는 인증서 파일 경로   | 명령어         | 키 파라미터                  | 인증서 파라미터                           |
|------------------------------|------------------------------|-----------------------------|----------------|------------------------------|-------------------------------------------|
| etcd-ca                      |     etcd/ca.key                         | etcd/ca.crt                 | kube-apiserver |                              | --etcd-cafile                             |
| kube-apiserver-etcd-client   | apiserver-etcd-client.key    | apiserver-etcd-client.crt   | kube-apiserver | --etcd-keyfile               | --etcd-certfile                           |
| kubernetes-ca                |    ca.key                          | ca.crt                      | kube-apiserver |                              | --client-ca-file                          |
| kubernetes-ca                |    ca.key                          | ca.crt                      | kube-controller-manager | --cluster-signing-key-file      | --client-ca-file, --root-ca-file, --cluster-signing-cert-file  |
| kube-apiserver               | apiserver.key                | apiserver.crt               | kube-apiserver | --tls-private-key-file       | --tls-cert-file                           |
| kube-apiserver-kubelet-client|     apiserver-kubelet-client.key                         | apiserver-kubelet-client.crt| kube-apiserver | --kubelet-client-key | --kubelet-client-certificate              |
| front-proxy-ca               |     front-proxy-ca.key                         | front-proxy-ca.crt          | kube-apiserver |                              | --requestheader-client-ca-file            |
| front-proxy-ca               |     front-proxy-ca.key                         | front-proxy-ca.crt          | kube-controller-manager |                              | --requestheader-client-ca-file |
| front-proxy-client           | front-proxy-client.key       | front-proxy-client.crt      | kube-apiserver | --proxy-client-key-file      | --proxy-client-cert-file                  |
| etcd-ca                      |         etcd/ca.key                     | etcd/ca.crt                 | etcd           |                              | --trusted-ca-file, --peer-trusted-ca-file |
| kube-etcd                    | etcd/server.key              | etcd/server.crt             | etcd           | --key-file                   | --cert-file                               |
| kube-etcd-peer               | etcd/peer.key                | etcd/peer.crt               | etcd           | --peer-key-file              | --peer-cert-file                          |
| etcd-ca                      |                              | etcd/ca.crt                 | etcdctl    |                              | --cacert                                  |
| kube-etcd-healthcheck-client | etcd/healthcheck-client.key  | etcd/healthcheck-client.crt | etcdctl     | --key                        | --cert                                    |

서비스 계정 키 쌍에도 동일한 고려 사항이 적용된다.

| 개인키 경로             | 공개 키 경로             | 명령어                 | 파라미터                             |
|------------------------------|-----------------------------|-------------------------|--------------------------------------|
|  sa.key                      |                             | kube-controller-manager | --service-account-private-key-file   |
|                              | sa.pub                      | kube-apiserver          | --service-account-key-file           |

## 각 사용자 계정을 위한 인증서 설정하기

반드시 이런 관리자 계정과 서비스 계정을 설정해야 한다.

| 파일명                | 자격증명 이름            | 기본 CN                     | O (주체에서) |
|-------------------------|----------------------------|--------------------------------|----------------|
| admin.conf              | default-admin              | kubernetes-admin               | system:masters |
| kubelet.conf            | default-auth               | system:node:`<nodeName>` (note를 보자) | system:nodes   |
| controller-manager.conf | default-controller-manager | system:kube-controller-manager |                |
| scheduler.conf          | default-scheduler          | system:kube-scheduler          |                |

{{< note >}}
`kubelet.conf`을 위한 `<nodeName>`값은 API 서버에 등록된 것처럼 kubelet에 제공되는 노드 이름 값과 **반드시** 정확히 일치해야 한다. 더 자세한 내용은 [노드 인증](/docs/reference/access-authn-authz/node/)을 살펴보자.
{{< /note >}}

1. 각 환경 설정에 대해 주어진 CN과 O를 이용하여 x509 인증서와 키쌍을 생성한다.

1. 각 환경 설정에 대해 다음과 같이 `kubectl`를 실행한다.

```shell
KUBECONFIG=<filename> kubectl config set-cluster default-cluster --server=https://<host ip>:6443 --certificate-authority <path-to-kubernetes-ca> --embed-certs
KUBECONFIG=<filename> kubectl config set-credentials <credential-name> --client-key <path-to-key>.pem --client-certificate <path-to-cert>.pem --embed-certs
KUBECONFIG=<filename> kubectl config set-context default-system --cluster default-cluster --user <credential-name>
KUBECONFIG=<filename> kubectl config use-context default-system
```

이 파일들은 다음과 같이 사용된다.

| 파일명                   | 명령어                  | 설명                                                                   |
|-------------------------|-------------------------|-----------------------------------------------------------------------|
| admin.conf              | kubectl                 | 클러스터 관리자를 설정한다.                                              |
| kubelet.conf            | kubelet                 | 클러스터 각 노드를 위해 필요하다.                            |
| controller-manager.conf | kube-controller-manager | 반드시 매니페스트를 `manifests/kube-controller-manager.yaml`에 추가해야 한다. |
| scheduler.conf          | kube-scheduler          | 반드시 매니페스트를 `manifests/kube-scheduler.yaml`에 추가해야 한다.          |
