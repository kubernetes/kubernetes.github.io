---



title: 컨테이너 런타임
content_type: concept
weight: 20
---
<!-- overview -->

파드가 노드에서 실행될 수 있도록 클러스터의 각 노드에
{{< glossary_tooltip text="컨테이너 런타임" term_id="container-runtime" >}}을
설치해야 한다. 이 페이지에서는 관련된 항목을 설명하고
노드 설정 관련 작업을 설명한다.

<!-- body -->

이 페이지에는 리눅스 환경의 쿠버네티스에서 여러 공통 컨테이너 런타임을 사용하는 방법에 대한
세부 정보가 있다.

- [containerd](#containerd)
- [CRI-O](#cri-o)
- [도커](#도커)

{{< note >}}
다른 운영 체제의 경우, 해당 플랫폼과 관련된 문서를 찾아보자.
{{< /note >}}

## Cgroup 드라이버

Control group은 프로세스에 할당된 리소스를 제한하는데 사용된다.

리눅스 배포판의 init 시스템이 [systemd](https://www.freedesktop.org/wiki/Software/systemd/)인
경우, init 프로세스는 root control group(`cgroup`)을
생성 및 사용하는 cgroup 관리자로 작동한다.
Systemd는 cgroup과의 긴밀한 통합을 통해 프로세스당 cgroup을 할당한다.
컨테이너 런타임과 kubelet이 `cgroupfs`를 사용하도록 설정할 수 있다. systemd와 함께
`cgroupfs`를 사용하면 두 개의 서로 다른 cgroup 관리자가 존재하게 된다는 뜻이다.

단일 cgroup 관리자는 할당되는 리소스가 무엇인지를 단순화하고,
기본적으로 사용할 수 있는 리소스와 사용 중인 리소스를 일관성있게 볼 수 있다.
시스템에 두 개의 cgroup 관리자가 있으면, 이런 리소스도 두 개의 관점에서 보게 된다.
현장에서 사람들은 kubelet과 도커에 `cgroupfs`를 사용하고,
나머지 프로세스는 `systemd`를 사용하도록 노드가 설정된 경우, 리소스가 부족할 때
불안정해지는 사례를 보고했다.

컨테이너 런타임과 kubelet이 `systemd`를 cgroup 드라이버로 사용하도록 설정을 변경하면
시스템이 안정화된다. 도커에 대해 구성하려면, `native.cgroupdriver=systemd`를 설정한다.

{{< caution >}}
클러스터에 결합되어 있는 노드의 cgroup 관리자를 변경하는 것은 신중하게 수행해야 한다.
하나의 cgroup 드라이버의 의미를 사용하여 kubelet이 파드를 생성해왔다면,
컨테이너 런타임을 다른 cgroup 드라이버로 변경하는 것은 존재하는 기존 파드에 대해 파드 샌드박스 재생성을 시도할 때, 에러가 발생할 수 있다.
kubelet을 재시작하는 것은 에러를 해결할 수 없을 것이다.

자동화가 가능하다면, 업데이트된 구성을 사용하여 노드를 다른 노드로
교체하거나, 자동화를 사용하여 다시 설치한다.
{{< /caution >}}

### kubeadm으로 생성한 클러스터의 드라이버를 `systemd`로 변경하기

kubeadm으로 생성한 클러스터의 cgroup 드라이버를 `systemd`로 변경하려면
[변경 가이드](/docs/tasks/administer-cluster/kubeadm/configure-cgroup-driver/)를 참고한다.

## 컨테이너 런타임

{{% thirdparty-content %}}

### containerd

이 섹션에는 containerd 를 CRI 런타임으로 사용하는 데 필요한 단계가 포함되어 있다.

필수 구성 요소를 설치 및 구성한다.

```shell
cat <<EOF | sudo tee /etc/modules-load.d/containerd.conf
overlay
br_netfilter
EOF

sudo modprobe overlay
sudo modprobe br_netfilter

# 필요한 sysctl 파라미터를 설정하면 재부팅 후에도 유지된다.
cat <<EOF | sudo tee /etc/sysctl.d/99-kubernetes-cri.conf
net.bridge.bridge-nf-call-iptables  = 1
net.ipv4.ip_forward                 = 1
net.bridge.bridge-nf-call-ip6tables = 1
EOF

# 재부팅하지 않고 sysctl 파라미터 적용
sudo sysctl --system
```

containerd를 설치한다.

{{< tabs name="tab-cri-containerd-installation" >}}
{{% tab name="Linux" %}}

1. 공식 도커 리포지터리에서 `containerd.io` 패키지를 설치한다.
각 리눅스 배포판에 대한 도커 리포지터리를 설정하고
`containerd.io` 패키지를 설치하는 방법은
[도커 엔진 설치](https://docs.docker.com/engine/install/#server)에서 찾을 수 있다.

2. containerd 설정

   ```shell
   sudo mkdir -p /etc/containerd
   containerd config default | sudo tee /etc/containerd/config.toml
   ```

3. containerd 재시작

   ```shell
   sudo systemctl restart containerd
   ```

{{% /tab %}}
{{% tab name="Windows (PowerShell)" %}}

PowerShell 세션을 시작하고 `$Version`을 원하는 버전으로
설정(예: `$Version:1.4.3`)한 후 다음 명령을 실행한다.

1. containerd 다운로드

   ```powershell
   curl.exe -L https://github.com/containerd/containerd/releases/download/v$Version/containerd-$Version-windows-amd64.tar.gz -o containerd-windows-amd64.tar.
gz
   tar.exe xvf .\containerd-windows-amd64.tar.gz
   ```

2. 추출과 설정

   ```powershell
   Copy-Item -Path ".\bin\" -Destination "$Env:ProgramFiles\containerd" -Recurse -Force
   cd $Env:ProgramFiles\containerd\
   .\containerd.exe config default | Out-File config.toml -Encoding ascii

   # 설정을 검토한다. 설정에 따라 다음을 조정할 수 있다.
   # - sandbox_image (쿠버네티스 일시중지 이미지)
   # - cni bin 폴더와 conf 폴더 위치
   Get-Content config.toml

   # (선택사항 - 그러나 적극 권장함) Windows 디펜더 검사에서 containerd 제외
   Add-MpPreference -ExclusionProcess "$Env:ProgramFiles\containerd\containerd.exe"
   ```

3. containerd 실행

   ```powershell
   .\containerd.exe --register-service
   Start-Service containerd
   ```

{{% /tab %}}
{{< /tabs >}}

#### `systemd` cgroup 드라이버의 사용 {#containerd-systemd}

`/etc/containerd/config.toml` 의 `systemd` cgroup 드라이버를 `runc` 에서 사용하려면, 다음과 같이 설정한다.

```
[plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc]
  ...
  [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc.options]
    SystemdCgroup = true
```

이 변경 사항을 적용하는 경우 containerd를 재시작한다.

```shell
sudo systemctl restart containerd
```

kubeadm을 사용하는 경우,
[kubelet용 cgroup 드라이버](/ko/docs/setup/production-environment/tools/kubeadm/install-kubeadm/#컨트롤-플레인-노드에서-kubelet이-사용하는-cgroup-드라이버-구성)를 수동으로 구성한다.

### CRI-O

이 섹션은 CRI-O를 컨테이너 런타임으로 설치하는 필수적인 단계를 담고 있다.

시스템에 CRI-O를 설치하기 위해서 다음의 커맨드를 사용한다.

{{< note >}}
CRI-O 메이저와 마이너 버전은 쿠버네티스 메이저와 마이너 버전이 일치해야 한다.
더 자세한 정보는 [CRI-O 호환 매트릭스](https://github.com/cri-o/cri-o#compatibility-matrix-cri-o--kubernetes)를 본다.
{{< /note >}}

필수 구성 요소를 설치하고 구성한다.

```shell
# .conf 파일을 만들어 부팅 시 모듈을 로드한다
cat <<EOF | sudo tee /etc/modules-load.d/crio.conf
overlay
br_netfilter
EOF

sudo modprobe overlay
sudo modprobe br_netfilter

# 요구되는 sysctl 파라미터 설정, 이 설정은 재부팅 간에도 유지된다.
cat <<EOF | sudo tee /etc/sysctl.d/99-kubernetes-cri.conf
net.bridge.bridge-nf-call-iptables  = 1
net.ipv4.ip_forward                 = 1
net.bridge.bridge-nf-call-ip6tables = 1
EOF

sudo sysctl --system
```

{{< tabs name="tab-cri-cri-o-installation" >}}
{{% tab name="Debian" %}}

다음의 운영 체제에서 CRI-O를 설치하려면, 환경 변수 `OS` 를
아래의 표에서 적절한 필드로 설정한다.

| 운영 체제          | `$OS`             |
| ---------------- | ----------------- |
| Debian Unstable  | `Debian_Unstable` |
| Debian Testing   | `Debian_Testing`  |

<br />
그런 다음, `$VERSION` 을 사용자의 쿠버네티스 버전과 일치하는 CRI-O 버전으로 설정한다.
예를 들어, CRI-O 1.20을 설치하려면, `VERSION=1.20` 로 설정한다.
사용자의 설치를 특정 릴리스에 고정할 수 있다.
버전 1.20.0을 설치하려면, `VERSION=1.20:1.20.0` 을 설정한다.
<br />

그런 다음, 아래를 실행한다.
```shell
cat <<EOF | sudo tee /etc/apt/sources.list.d/devel:kubic:libcontainers:stable.list
deb https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/$OS/ /
EOF
cat <<EOF | sudo tee /etc/apt/sources.list.d/devel:kubic:libcontainers:stable:cri-o:$VERSION.list
deb http://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable:/cri-o:/$VERSION/$OS/ /
EOF

curl -L https://download.opensuse.org/repositories/devel:kubic:libcontainers:stable:cri-o:$VERSION/$OS/Release.key | sudo apt-key --keyring /etc/apt/trusted.gpg.d/libcontainers.gpg add -
curl -L https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/$OS/Release.key | sudo apt-key --keyring /etc/apt/trusted.gpg.d/libcontainers.gpg add -

sudo apt-get update
sudo apt-get install cri-o cri-o-runc
```

{{% /tab %}}

{{% tab name="Ubuntu" %}}

다음의 운영 체제에서 CRI-O를 설치하려면, 환경 변수 `OS` 를
아래의 표에서 적절한 필드로 설정한다.

| 운영 체제          | `$OS`             |
| ---------------- | ----------------- |
| Ubuntu 20.04     | `xUbuntu_20.04`   |
| Ubuntu 19.10     | `xUbuntu_19.10`   |
| Ubuntu 19.04     | `xUbuntu_19.04`   |
| Ubuntu 18.04     | `xUbuntu_18.04`   |

<br />
그런 다음, `$VERSION` 을 사용자의 쿠버네티스 버전과 일치하는 CRI-O 버전으로 설정한다.
예를 들어, CRI-O 1.20을 설치하려면, `VERSION=1.20` 로 설정한다.
사용자의 설치를 특정 릴리스에 고정할 수 있다.
버전 1.20.0을 설치하려면, `VERSION=1.20:1.20.0` 을 설정한다.
<br />

그런 다음, 아래를 실행한다.
```shell
cat <<EOF | sudo tee /etc/apt/sources.list.d/devel:kubic:libcontainers:stable.list
deb https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/$OS/ /
EOF
cat <<EOF | sudo tee /etc/apt/sources.list.d/devel:kubic:libcontainers:stable:cri-o:$VERSION.list
deb http://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable:/cri-o:/$VERSION/$OS/ /
EOF

curl -L https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/$OS/Release.key | sudo apt-key --keyring /etc/apt/trusted.gpg.d/libcontainers.gpg add -
curl -L https://download.opensuse.org/repositories/devel:kubic:libcontainers:stable:cri-o:$VERSION/$OS/Release.key | sudo apt-key --keyring /etc/apt/trusted.gpg.d/libcontainers-cri-o.gpg add -

apt-get update
apt-get install cri-o cri-o-runc
```
{{% /tab %}}

{{% tab name="CentOS" %}}

다음의 운영 체제에서 CRI-O를 설치하려면, 환경 변수 `OS` 를
아래의 표에서 적절한 필드로 설정한다.

| 운영 체제          | `$OS`             |
| ---------------- | ----------------- |
| Centos 8         | `CentOS_8`        |
| Centos 8 Stream  | `CentOS_8_Stream` |
| Centos 7         | `CentOS_7`        |

<br />
그런 다음, `$VERSION` 을 사용자의 쿠버네티스 버전과 일치하는 CRI-O 버전으로 설정한다.
예를 들어, CRI-O 1.20을 설치하려면, `VERSION=1.20` 로 설정한다.
사용자의 설치를 특정 릴리스에 고정할 수 있다.
버전 1.20.0을 설치하려면, `VERSION=1.20:1.20.0` 을 설정한다.
<br />

그런 다음, 아래를 실행한다.
```shell
sudo curl -L -o /etc/yum.repos.d/devel:kubic:libcontainers:stable.repo https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/$OS/devel:kubic:libcontainers:stable.repo
sudo curl -L -o /etc/yum.repos.d/devel:kubic:libcontainers:stable:cri-o:$VERSION.repo https://download.opensuse.org/repositories/devel:kubic:libcontainers:stable:cri-o:$VERSION/$OS/devel:kubic:libcontainers:stable:cri-o:$VERSION.repo
sudo yum install cri-o
```

{{% /tab %}}

{{% tab name="openSUSE Tumbleweed" %}}

```shell
sudo zypper install cri-o
```
{{% /tab %}}
{{% tab name="Fedora" %}}

`$VERSION` 을 사용자의 쿠버네티스 버전과 일치하는 CRI-O 버전으로 설정한다.
예를 들어, CRI-O 1.20을 설치하려면, `VERSION=1.20` 로 설정한다.

사용할 수 있는 버전을 찾으려면 다음을 실행한다.
```shell
sudo dnf module list cri-o
```
CRI-O는 Fedora에서 특정 릴리스를 고정하여 설치하는 방법은 지원하지 않는다.

그런 다음, 아래를 실행한다.
```shell
sudo dnf module enable cri-o:$VERSION
sudo dnf install cri-o
```

{{% /tab %}}
{{< /tabs >}}

CRI-O를 시작한다.

```shell
sudo systemctl daemon-reload
sudo systemctl enable crio --now
```

자세한 사항은 [CRI-O 설치 가이드](https://github.com/cri-o/cri-o/blob/master/install.md)를
참고한다.


#### cgroup 드라이버

CRI-O는 기본적으로 systemd cgroup 드라이버를 사용한다. `cgroupfs` cgroup 드라이버로
전환하려면, `/etc/crio/crio.conf` 를 수정하거나 `/etc/crio/crio.conf.d/02-cgroup-manager.conf` 에
드롭-인(drop-in) 구성을 배치한다. 예를 들면, 다음과 같다.

```toml
[crio.runtime]
conmon_cgroup = "pod"
cgroup_manager = "cgroupfs"
```

또한 `cgroupfs` 와 함께 CRI-O를 사용할 때 `pod` 값으로 설정해야 하는
변경된 `conmon_cgroup` 에 유의한다. 일반적으로 kubelet(일반적으로 kubeadm을 통해 수행됨)과
CRI-O의 cgroup 드라이버 구성을 동기화 상태로
유지해야 한다.

### 도커

1. 각 노드에서 [도커 엔진 설치](https://docs.docker.com/engine/install/#server)에 따라
리눅스 배포판용 도커를 설치한다.
이 [의존성 파일](https://git.k8s.io/kubernetes/build/dependencies.yaml)에서
검증된 최신 버전의 도커를 찾을 수 있다.

2. 특히 컨테이너의 cgroup 관리에 systemd를 사용하도록 도커 데몬을 구성한다.

   ```shell
   sudo mkdir /etc/docker
   cat <<EOF | sudo tee /etc/docker/daemon.json
   {
     "exec-opts": ["native.cgroupdriver=systemd"],
     "log-driver": "json-file",
     "log-opts": {
       "max-size": "100m"
     },
     "storage-driver": "overlay2"
   }
   EOF
   ```

   {{< note >}}
   `overlay2`는 리눅스 커널 4.0 이상 또는 3.10.0-514 버전 이상을 사용하는 RHEL
   또는 CentOS를 구동하는 시스템에서 선호하는 스토리지 드라이버이다.
   {{< /note >}}

3. 도커 재시작과 부팅시 실행되게 설정

   ```shell
   sudo systemctl enable docker
   sudo systemctl daemon-reload
   sudo systemctl restart docker
   ```

{{< note >}}
더 자세한 내용은
  - [도커 데몬 설정](https://docs.docker.com/config/daemon/)
  - [systemd로 도커 제어](https://docs.docker.com/config/daemon/systemd/)
{{< /note >}}
