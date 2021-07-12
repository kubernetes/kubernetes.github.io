---


title: macOS에 kubectl 설치 및 설정
content_type: task
weight: 10
card:
  name: tasks
  weight: 20
  title: macOS에 kubectl 설치하기
---

## {{% heading "prerequisites" %}}

클러스터의 마이너(minor) 버전 차이 내에 있는 kubectl 버전을 사용해야 한다. 예를 들어, v{{< skew latestVersion >}} 클라이언트는 v{{< skew prevMinorVersion >}}, v{{< skew latestVersion >}}, v{{< skew nextMinorVersion >}}의 컨트롤 플레인과 연동될 수 있다.
최신 버전의 kubectl을 사용하면 예기치 않은 문제를 피할 수 있다.

## macOS에 kubectl 설치

다음과 같은 방법으로 macOS에 kubectl을 설치할 수 있다.

- [macOS에서 curl을 사용하여 kubectl 바이너리 설치](#install-kubectl-binary-with-curl-on-macos)
- [macOS에서 Homebrew를 사용하여 설치](#install-with-homebrew-on-macos)
- [macOS에서 Macports를 사용하여 설치](#install-with-macports-on-macos)

### macOS에서 curl을 사용하여 kubectl 바이너리 설치 {#install-kubectl-binary-with-curl-on-macos}

1. 최신 릴리스를 다운로드한다.

   {{< tabs name="download_binary_macos" >}}
   {{< tab name="Intel" codelang="bash" >}}
   curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/darwin/amd64/kubectl"
   {{< /tab >}}
   {{< tab name="Apple Silicon" codelang="bash" >}}
   curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/darwin/arm64/kubectl"
   {{< /tab >}}
   {{< /tabs >}}

   {{< note >}}
   특정 버전을 다운로드하려면, `$(curl -L -s https://dl.k8s.io/release/stable.txt)` 명령 부분을 특정 버전으로 바꾼다.

   예를 들어, Intel macOS에 버전 {{< param "fullversion" >}}을 다운로드하려면, 다음을 입력한다.

   ```bash
   curl -LO "https://dl.k8s.io/release/{{< param "fullversion" >}}/bin/darwin/amd64/kubectl"
   ```

   Apple Silicon의 macOS라면, 다음을 입력한다.

   ```bash
   curl -LO "https://dl.k8s.io/release/{{< param "fullversion" >}}/bin/darwin/arm64/kubectl"
   ```

   {{< /note >}}

1. 바이너리를 검증한다. (선택 사항)

   kubectl 체크섬 파일을 다운로드한다.

   {{< tabs name="download_checksum_macos" >}}
   {{< tab name="Intel" codelang="bash" >}}
   curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/darwin/amd64/kubectl.sha256"
   {{< /tab >}}
   {{< tab name="Apple Silicon" codelang="bash" >}}
   curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/darwin/arm64/kubectl.sha256"
   {{< /tab >}}
   {{< /tabs >}}

   kubectl 바이너리를 체크섬 파일을 통해 검증한다.

   ```bash
   echo "$(<kubectl.sha256)  kubectl" | shasum -a 256 --check
   ```

   검증이 성공한다면, 출력은 다음과 같다.

   ```bash
   kubectl: OK
   ```

   검증이 실패한다면, `shasum`이 0이 아닌 상태로 종료되며 다음과 유사한 결과를 출력한다.

   ```bash
   kubectl: FAILED
   shasum: WARNING: 1 computed checksum did NOT match
   ```

   {{< note >}}
   동일한 버전의 바이너리와 체크섬을 다운로드한다.
   {{< /note >}}

1. kubectl 바이너리를 실행 가능하게 한다.

   ```bash
   chmod +x ./kubectl
   ```

1. kubectl 바이너리를 시스템 `PATH` 의 파일 위치로 옮긴다.

   ```bash
   sudo mv ./kubectl /usr/local/bin/kubectl
   sudo chown root: /usr/local/bin/kubectl
   ```

   {{< note >}}
   `PATH` 환경 변수 안에 `/usr/local/bin` 이 있는지 확인한다.
   {{< /note >}}

1. 설치한 버전이 최신 버전인지 확인한다.

   ```bash
   kubectl version --client
   ```

### macOS에서 Homebrew를 사용하여 설치 {#install-with-homebrew-on-macos}

macOS에서 [Homebrew](https://brew.sh/) 패키지 관리자를 사용하는 경우, Homebrew로 kubectl을 설치할 수 있다.

1. 설치 명령을 실행한다.

   ```bash
   brew install kubectl
   ```

   또는

   ```bash
   brew install kubernetes-cli
   ```

1. 설치한 버전이 최신 버전인지 확인한다.

   ```bash
   kubectl version --client
   ```

### macOS에서 Macports를 사용하여 설치 {#install-with-macports-on-macos}

macOS에서 [Macports](https://macports.org/) 패키지 관리자를 사용하는 경우, Macports로 kubectl을 설치할 수 있다.

1. 설치 명령을 실행한다.

   ```bash
   sudo port selfupdate
   sudo port install kubectl
   ```

1. 설치한 버전이 최신 버전인지 확인한다.

   ```bash
   kubectl version --client
   ```

## kubectl 구성 확인

{{< include "included/verify-kubectl.md" >}}

## 선택적 kubectl 구성

### 셸 자동 완성 활성화

kubectl은 Bash 및 Zsh에 대한 자동 완성 지원을 제공하므로 입력을 위한 타이핑을 많이 절약할 수 있다.

다음은 Bash 및 Zsh에 대한 자동 완성을 설정하는 절차이다.

{{< tabs name="kubectl_autocompletion" >}}
{{< tab name="Bash" include="included/optional-kubectl-configs-bash-mac.md" />}}
{{< tab name="Zsh" include="included/optional-kubectl-configs-zsh.md" />}}
{{< /tabs >}}

## {{% heading "whatsnext" %}}

{{< include "included/kubectl-whats-next.md" >}}
