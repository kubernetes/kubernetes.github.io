---
title: kubeadm 설치하기
content_type: task
weight: 10
card:
  name: setup
  weight: 20
  title: kubeadm 설정 도구 설치
---

<!-- overview -->

<img src="https://raw.githubusercontent.com/kubernetes/kubeadm/master/logos/stacked/color/kubeadm-stacked-color.png" align="right" width="150px">이 페이지에서는 `kubeadm` 툴박스를 설치하는 방법을 보여준다.
이 설치 프로세스를 수행한 후 kubeadm으로 클러스터를 만드는 방법에 대한 자세한 내용은 [kubeadm을 사용하여 클러스터 생성하기](/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/) 페이지를 참고한다.



## {{% heading "prerequisites" %}}


* 호환되는 리눅스 머신. 쿠버네티스 프로젝트는 데비안 기반 배포판, 레드햇 기반 배포판, 그리고 패키지 매니저를 사용하지 않는 경우에 대한 일반적인 가이드를 제공한다.
* 2 GB 이상의 램을 장착한 머신. (이 보다 작으면 사용자의 앱을 위한 공간이 거의 남지 않음)
* 2 이상의 CPU.
* 클러스터의 모든 머신에 걸친 전체 네트워크 연결. (공용 또는 사설 네트워크면 괜찮음)
* 모든 노드에 대해 고유한 호스트 이름, MAC 주소 및 product_uuid. 자세한 내용은 [여기](#verify-mac-address)를 참고한다.
* 컴퓨터의 특정 포트들 개방. 자세한 내용은 [여기](#check-required-ports)를 참고한다.
* 스왑의 비활성화. kubelet이 제대로 작동하게 하려면 **반드시** 스왑을 사용하지 않도록 설정한다.



<!-- steps -->

## MAC 주소 및 product_uuid가 모든 노드에 대해 고유한지 확인 {#verify-mac-address}
* 사용자는 `ip link` 또는 `ifconfig -a` 명령을 사용하여 네트워크 인터페이스의 MAC 주소를 확인할 수 있다.
* product_uuid는 `sudo cat /sys/class/dmi/id/product_uuid` 명령을 사용하여 확인할 수 있다.

일부 가상 머신은 동일한 값을 가질 수 있지만 하드웨어 장치는 고유한 주소를 가질
가능성이 높다. 쿠버네티스는 이러한 값을 사용하여 클러스터의 노드를 고유하게 식별한다.
이러한 값이 각 노드에 고유하지 않으면 설치 프로세스가
[실패](https://github.com/kubernetes/kubeadm/issues/31)할 수 있다.  

## 네트워크 어댑터 확인

네트워크 어댑터가 두 개 이상이고, 쿠버네티스 컴포넌트가 디폴트 라우트(default route)에서 도달할 수 없는
경우, 쿠버네티스 클러스터 주소가 적절한 어댑터를 통해 이동하도록 IP 경로를 추가하는 것이 좋다.

## iptables가 브리지된 트래픽을 보게 하기

`br_netfilter` 모듈이 로드되었는지 확인한다. `lsmod | grep br_netfilter` 를 실행하면 된다. 명시적으로 로드하려면 `sudo modprobe br_netfilter` 를 실행한다.

리눅스 노드의 iptables가 브리지된 트래픽을 올바르게 보기 위한 요구 사항으로, `sysctl` 구성에서 `net.bridge.bridge-nf-call-iptables` 가 1로 설정되어 있는지 확인해야 한다. 다음은 예시이다.

```bash
cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
br_netfilter
EOF

cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
EOF
sudo sysctl --system
```

자세한 내용은 [네트워크 플러그인 요구 사항](/ko/docs/concepts/extend-kubernetes/compute-storage-net/network-plugins/#네트워크-플러그인-요구-사항) 페이지를 참고한다.

## 필수 포트 확인 {#check-required-ports}

### 컨트롤 플레인 노드

| 프로토콜   | 방향       | 포트 범위    | 목적                      | 사용자                     |
|----------|-----------|------------|-------------------------|---------------------------|
| TCP      | 인바운드    | 6443\*      | 쿠버네티스 API 서버         | 모두                       |
| TCP      | 인바운드    | 2379-2380  | etcd 서버 클라이언트 API    | kube-apiserver, etcd      |
| TCP      | 인바운드    | 10250      | kubelet API             | 자체, 컨트롤 플레인          |
| TCP      | 인바운드    | 10251      | kube-scheduler          | 자체                      |
| TCP      | 인바운드    | 10252      | kube-controller-manager | 자체                      |

### 워커 노드

| 프로토콜   | 방향       | 포트 범위      | 목적                   | 사용자                   |
|----------|-----------|-------------|-----------------------|-------------------------|
| TCP      | 인바운드    | 10250       | kubelet API           | 자체, 컨트롤 플레인        |
| TCP      | 인바운드    | 30000-32767 | NodePort 서비스†        | 모두                     |

† [NodePort 서비스](/ko/docs/concepts/services-networking/service/)의 기본 포트 범위.

*로 표시된 모든 포트 번호는 재정의할 수 있으므로, 사용자 지정 포트도
열려 있는지 확인해야 한다.

etcd 포트가 컨트롤 플레인 노드에 포함되어 있지만, 외부 또는 사용자 지정 포트에서
자체 etcd 클러스터를 호스팅할 수도 있다.

사용자가 사용하는 파드 네트워크 플러그인(아래 참조)은 특정 포트를 열어야 할 수도
있다. 이것은 각 파드 네트워크 플러그인마다 다르므로, 필요한 포트에 대한
플러그인 문서를 참고한다.

## 런타임 설치 {#installing-runtime}

파드에서 컨테이너를 실행하기 위해, 쿠버네티스는
{{< glossary_tooltip term_id="container-runtime" text="컨테이너 런타임" >}}을 사용한다.

{{< tabs name="container_runtime" >}}
{{% tab name="리눅스 노드" %}}

기본적으로, 쿠버네티스는
{{< glossary_tooltip term_id="cri" text="컨테이너 런타임 인터페이스">}}(CRI)를
사용하여 사용자가 선택한 컨테이너 런타임과 인터페이스한다.

런타임을 지정하지 않으면, kubeadm은 잘 알려진 유닉스 도메인 소켓 목록을 검색하여
설치된 컨테이너 런타임을 자동으로 감지하려고 한다.
다음 표에는 컨테이너 런타임 및 관련 소켓 경로가 나열되어 있다.

{{< table caption = "컨테이너 런타임과 소켓 경로" >}}
| 런타임       | 유닉스 도메인 소켓 경로                |
|------------|-----------------------------------|
| 도커        | `/var/run/dockershim.sock`            |
| containerd | `/run/containerd/containerd.sock` |
| CRI-O      | `/var/run/crio/crio.sock`         |
{{< /table >}}

<br />
도커와 containerd가 모두 감지되면 도커가 우선시된다. 이것이 필요한 이유는 도커 18.09에서
도커만 설치한 경우에도 containerd와 함께 제공되므로 둘 다 감지될 수 있기
때문이다.
다른 두 개 이상의 런타임이 감지되면, kubeadm은 오류와 함께 종료된다.

kubelet은 빌트인 `dockershim` CRI 구현을 통해 도커와 통합된다.

자세한 내용은 [컨테이너 런타임](/ko/docs/setup/production-environment/container-runtimes/)을
참고한다.
{{% /tab %}}
{{% tab name="다른 운영 체제" %}}
기본적으로, kubeadm은 컨테이너 런타임으로 {{< glossary_tooltip term_id="docker" >}}를 사용한다.
kubelet은 빌트인 `dockershim` CRI 구현을 통해 도커와 통합된다.

자세한 내용은 [컨테이너 런타임](/ko/docs/setup/production-environment/container-runtimes/)을
참고한다.
{{% /tab %}}
{{< /tabs >}}


## kubeadm, kubelet 및 kubectl 설치

모든 머신에 다음 패키지들을 설치한다.

* `kubeadm`: 클러스터를 부트스트랩하는 명령이다.

* `kubelet`: 클러스터의 모든 머신에서 실행되는 파드와 컨테이너 시작과
    같은 작업을 수행하는 컴포넌트이다.

* `kubectl`: 클러스터와 통신하기 위한 커맨드 라인 유틸리티이다.

kubeadm은 `kubelet` 또는 `kubectl` 을 설치하거나 관리하지 **않으므로**, kubeadm이
설치하려는 쿠버네티스 컨트롤 플레인의 버전과 일치하는지
확인해야 한다. 그렇지 않으면, 예상치 못한 버그 동작으로 이어질 수 있는
버전 차이(skew)가 발생할 위험이 있다. 그러나, kubelet과 컨트롤 플레인 사이에 _하나의_
마이너 버전 차이가 지원되지만, kubelet 버전은 API 서버 버전 보다
높을 수 없다. 예를 들어, 1.7.0 버전의 kubelet은 1.8.0 API 서버와 완전히 호환되어야 하지만,
그 반대의 경우는 아니다.

`kubectl` 설치에 대한 정보는 [kubectl 설치 및 설정](/ko/docs/tasks/tools/)을 참고한다.

{{< warning >}}
이 지침은 모든 시스템 업그레이드에서 모든 쿠버네티스 패키지를 제외한다.
이는 kubeadm 및 쿠버네티스를
[업그레이드 하는 데 특별한 주의](/ko/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/)가 필요하기 때문이다.
{{</ warning >}}

버전 차이에 대한 자세한 내용은 다음을 참고한다.

* 쿠버네티스 [버전 및 버전-차이 정책](/ko/releases/version-skew-policy/)
* Kubeadm 관련 [버전 차이 정책](/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/#version-skew-policy)

{{< tabs name="k8s_install" >}}
{{% tab name="데비안 기반 배포판" %}}

1. `apt` 패키지 색인을 업데이트하고, 쿠버네티스 `apt` 리포지터리를 사용하는 데 필요한 패키지를 설치한다.

   ```shell
   sudo apt-get update
   sudo apt-get install -y apt-transport-https ca-certificates curl
   ```

2. 구글 클라우드의 공개 사이닝 키를 다운로드 한다.

   ```shell
   sudo curl -fsSLo /usr/share/keyrings/kubernetes-archive-keyring.gpg https://packages.cloud.google.com/apt/doc/apt-key.gpg
   ```

3. 쿠버네티스 `apt` 리포지터리를 추가한다.

   ```shell
   echo "deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list
   ```

4. `apt` 패키지 색인을 업데이트하고, kubelet, kubeadm, kubectl을 설치하고 해당 버전을 고정한다.

   ```shell
   sudo apt-get update
   sudo apt-get install -y kubelet kubeadm kubectl
   sudo apt-mark hold kubelet kubeadm kubectl
   ```

{{% /tab %}}
{{% tab name="레드햇 기반 배포판" %}}
```bash
cat <<EOF | sudo tee /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-\$basearch
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
exclude=kubelet kubeadm kubectl
EOF

# permissive 모드로 SELinux 설정(효과적으로 비활성화)
sudo setenforce 0
sudo sed -i 's/^SELINUX=enforcing$/SELINUX=permissive/' /etc/selinux/config

sudo yum install -y kubelet kubeadm kubectl --disableexcludes=kubernetes

sudo systemctl enable --now kubelet
```

  **참고:**

  - `setenforce 0` 및 `sed ...` 를 실행하여 permissive 모드로 SELinux를 설정하면 효과적으로 비활성화된다.
    컨테이너가 호스트 파일시스템(예를 들어, 파드 네트워크에 필요한)에 접근하도록 허용하는 데 필요하다.
    kubelet에서 SELinux 지원이 개선될 때까지 이 작업을 수행해야 한다.

  - 구성 방법을 알고 있는 경우 SELinux를 활성화된 상태로 둘 수 있지만 kubeadm에서 지원하지 않는 설정이 필요할 수 있다.

{{% /tab %}}
{{% tab name="패키지 매니저를 사용하지 않는 경우" %}}
CNI 플러그인 설치(대부분의 파드 네트워크에 필요)

```bash
CNI_VERSION="v0.8.2"
sudo mkdir -p /opt/cni/bin
curl -L "https://github.com/containernetworking/plugins/releases/download/${CNI_VERSION}/cni-plugins-linux-amd64-${CNI_VERSION}.tgz" | sudo tar -C /opt/cni/bin -xz
```

명령어 파일을 다운로드할 디렉터리 정의

{{< note >}}
`DOWNLOAD_DIR` 변수는 쓰기 가능한 디렉터리로 설정되어야 한다.
Flatcar Container Linux를 실행 중인 경우, `DOWNLOAD_DIR=/opt/bin` 을 설정한다.
{{< /note >}}

```bash
DOWNLOAD_DIR=/usr/local/bin
sudo mkdir -p $DOWNLOAD_DIR
```

crictl 설치(kubeadm / Kubelet 컨테이너 런타임 인터페이스(CRI)에 필요)

```bash
CRICTL_VERSION="v1.17.0"
curl -L "https://github.com/kubernetes-sigs/cri-tools/releases/download/${CRICTL_VERSION}/crictl-${CRICTL_VERSION}-linux-amd64.tar.gz" | sudo tar -C $DOWNLOAD_DIR -xz
```

`kubeadm`, `kubelet`, `kubectl` 설치 및 `kubelet` systemd 서비스 추가

```bash
RELEASE="$(curl -sSL https://dl.k8s.io/release/stable.txt)"
cd $DOWNLOAD_DIR
sudo curl -L --remote-name-all https://storage.googleapis.com/kubernetes-release/release/${RELEASE}/bin/linux/amd64/{kubeadm,kubelet,kubectl}
sudo chmod +x {kubeadm,kubelet,kubectl}

RELEASE_VERSION="v0.4.0"
curl -sSL "https://raw.githubusercontent.com/kubernetes/release/${RELEASE_VERSION}/cmd/kubepkg/templates/latest/deb/kubelet/lib/systemd/system/kubelet.service" | sed "s:/usr/bin:${DOWNLOAD_DIR}:g" | sudo tee /etc/systemd/system/kubelet.service
sudo mkdir -p /etc/systemd/system/kubelet.service.d
curl -sSL "https://raw.githubusercontent.com/kubernetes/release/${RELEASE_VERSION}/cmd/kubepkg/templates/latest/deb/kubeadm/10-kubeadm.conf" | sed "s:/usr/bin:${DOWNLOAD_DIR}:g" | sudo tee /etc/systemd/system/kubelet.service.d/10-kubeadm.conf
```

`kubelet` 활성화 및 시작

```bash
systemctl enable --now kubelet
```

{{< note >}}
Flatcar Container Linux 배포판은 `/usr` 디렉터리를 읽기 전용 파일시스템으로 마운트한다.
클러스터를 부트스트랩하기 전에, 쓰기 가능한 디렉터리를 구성하기 위한 추가 단계를 수행해야 한다.
쓰기 가능한 디렉터리를 설정하는 방법을 알아 보려면 [Kubeadm 문제 해결 가이드](/docs/setup/production-environment/tools/kubeadm/troubleshooting-kubeadm/#usr-mounted-read-only/)를 참고한다.
{{< /note >}}
{{% /tab %}}
{{< /tabs >}}


kubelet은 이제 kubeadm이 수행할 작업을 알려 줄 때까지 크래시루프(crashloop) 상태로
기다려야 하므로 몇 초마다 다시 시작된다.

## cgroup 드라이버 구성

컨테이너 런타임과 kubelet은 
["cgroup 드라이버"](/ko/docs/setup/production-environment/container-runtimes/)라는 속성을 갖고 있으며, 
cgroup 드라이버는 리눅스 머신의 cgroup 관리 측면에 있어서 중요하다.

{{< warning >}}
컨테이너 런타임과 kubelet의 cgroup 드라이버를 일치시켜야 하며, 그렇지 않으면 kubelet 프로세스에 오류가 발생한다.
 
더 자세한 사항은 [cgroup 드라이버 설정하기](/docs/tasks/administer-cluster/kubeadm/configure-cgroup-driver/)를 참고한다.
{{< /warning >}}

## 문제 해결

kubeadm에 문제가 있는 경우, [문제 해결 문서](/docs/setup/production-environment/tools/kubeadm/troubleshooting-kubeadm/)를 참고한다.

## {{% heading "whatsnext" %}}

* [kubeadm을 사용하여 클러스터 생성](/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/)
