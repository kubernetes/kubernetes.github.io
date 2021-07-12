---


title: 리눅스에 kubectl 설치 및 설정
content_type: task
weight: 10
card:
  name: tasks
  weight: 20
  title: 리눅스에 kubectl 설치하기
---

## {{% heading "prerequisites" %}}

클러스터의 마이너(minor) 버전 차이 내에 있는 kubectl 버전을 사용해야 한다. 예를 들어, v{{< skew latestVersion >}} 클라이언트는 v{{< skew prevMinorVersion >}}, v{{< skew latestVersion >}}, v{{< skew nextMinorVersion >}}의 컨트롤 플레인과 연동될 수 있다.
최신 버전의 kubectl을 사용하면 예기치 않은 문제를 피할 수 있다.

## 리눅스에 kubectl 설치

다음과 같은 방법으로 리눅스에 kubectl을 설치할 수 있다.

- [리눅스에 curl을 사용하여 kubectl 바이너리 설치](#install-kubectl-binary-with-curl-on-linux)
- [기본 패키지 관리 도구를 사용하여 설치](#install-using-native-package-management)
- [다른 패키지 관리 도구를 사용하여 설치](#install-using-other-package-management)

### 리눅스에서 curl을 사용하여 kubectl 바이너리 설치 {#install-kubectl-binary-with-curl-on-linux}

1. 다음 명령으로 최신 릴리스를 다운로드한다.

   ```bash
   curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
   ```

   {{< note >}}
특정 버전을 다운로드하려면, `$(curl -L -s https://dl.k8s.io/release/stable.txt)` 명령 부분을 특정 버전으로 바꾼다.

예를 들어, 리눅스에서 버전 {{< param "fullversion" >}}을 다운로드하려면, 다음을 입력한다.

   ```bash
   curl -LO https://dl.k8s.io/release/{{< param "fullversion" >}}/bin/linux/amd64/kubectl
   ```
   {{< /note >}}

1. 바이너리를 검증한다. (선택 사항)

   kubectl 체크섬(checksum) 파일을 다운로드한다.

   ```bash
   curl -LO "https://dl.k8s.io/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl.sha256"
   ```

   kubectl 바이너리를 체크섬 파일을 통해 검증한다.

   ```bash
   echo "$(<kubectl.sha256) kubectl" | sha256sum --check
   ```

   검증이 성공한다면, 출력은 다음과 같다.

   ```bash
   kubectl: OK
   ```

   검증이 실패한다면, `shasum`이 0이 아닌 상태로 종료되며 다음과 유사한 결과를 출력한다.

   ```bash
   kubectl: FAILED
   sha256sum: WARNING: 1 computed checksum did NOT match
   ```

   {{< note >}}
   동일한 버전의 바이너리와 체크섬을 다운로드한다.
   {{< /note >}}

1. kubectl 설치

   ```bash
   sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
   ```

   {{< note >}}
   대상 시스템에 root 접근 권한을 가지고 있지 않더라도, `~/.local/bin` 디렉터리에 kubectl을 설치할 수 있다.

   ```bash
   mkdir -p ~/.local/bin/kubectl
   mv ./kubectl ~/.local/bin/kubectl
   # 그리고 ~/.local/bin/kubectl을 $PATH에 추가
   ```

   {{< /note >}}

1. 설치한 버전이 최신인지 확인한다.

   ```bash
   kubectl version --client
   ```

### 기본 패키지 관리 도구를 사용하여 설치 {#install-using-native-package-management}

{{< tabs name="kubectl_install" >}}
{{% tab name="데비안 기반의 배포판" %}}

1. `apt` 패키지 색인을 업데이트하고 쿠버네티스 `apt` 리포지터리를 사용하는 데 필요한 패키지들을 설치한다.

   ```shell
   sudo apt-get update
   sudo apt-get install -y apt-transport-https ca-certificates curl
   ```

2. 구글 클라우드 공개 사이닝 키를 다운로드한다.

   ```shell
   sudo curl -fsSLo /usr/share/keyrings/kubernetes-archive-keyring.gpg https://packages.cloud.google.com/apt/doc/apt-key.gpg
   ```

3. 쿠버네티스 `apt` 리포지터리를 추가한다.

   ```shell
   echo "deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list
   ```

4. 새 리포지터리의 `apt` 패키지 색인을 업데이트하고 kubectl을 설치한다.

   ```shell
   sudo apt-get update
   sudo apt-get install -y kubectl
   ```

{{% /tab %}}

{{< tab name="레드햇 기반의 배포판" codelang="bash" >}}
cat <<EOF > /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
EOF
yum install -y kubectl
{{< /tab >}}
{{< /tabs >}}

### 다른 패키지 관리 도구를 사용하여 설치 {#install-using-other-package-management}

{{< tabs name="other_kubectl_install" >}}
{{% tab name="Snap" %}}
[snap](https://snapcraft.io/docs/core/install) 패키지 관리자를 지원하는 Ubuntu 또는 다른 리눅스 배포판을 사용하는 경우, kubectl을 [snap](https://snapcraft.io/) 애플리케이션으로 설치할 수 있다.

```shell
snap install kubectl --classic
kubectl version --client
```

{{% /tab %}}

{{% tab name="Homebrew" %}}
리눅스 상에서 [Homebrew](https://docs.brew.sh/Homebrew-on-Linux) 패키지 관리자를 사용한다면, [설치](https://docs.brew.sh/Homebrew-on-Linux#install)를 통해 kubectl을 사용할 수 있다.

```shell
brew install kubectl
kubectl version --client
```

{{% /tab %}}

{{< /tabs >}}

## kubectl 구성 확인

{{< include "included/verify-kubectl.md" >}}

## 선택적 kubectl 구성

### 셸 자동 완성 활성화

kubectl은 Bash 및 Zsh에 대한 자동 완성 지원을 제공하므로 입력을 위한 타이핑을 많이 절약할 수 있다.

다음은 Bash 및 Zsh에 대한 자동 완성을 설정하는 절차이다.

{{< tabs name="kubectl_autocompletion" >}}
{{< tab name="Bash" include="included/optional-kubectl-configs-bash-linux.md" />}}
{{< tab name="Zsh" include="included/optional-kubectl-configs-zsh.md" />}}
{{< /tabs >}}

## {{% heading "whatsnext" %}}

{{< include "included/kubectl-whats-next.md" >}}
