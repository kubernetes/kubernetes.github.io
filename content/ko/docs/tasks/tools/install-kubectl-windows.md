---


title: 윈도우에 kubectl 설치 및 설정
content_type: task
weight: 10
card:
  name: tasks
  weight: 20
  title: 윈도우에 kubectl 설치하기
---

## {{% heading "prerequisites" %}}

클러스터의 마이너(minor) 버전 차이 내에 있는 kubectl 버전을 사용해야 한다. 예를 들어, v{{< skew latestVersion >}} 클라이언트는 v{{< skew prevMinorVersion >}}, v{{< skew latestVersion >}}, v{{< skew nextMinorVersion >}}의 컨트롤 플레인과 연동될 수 있다.
최신 버전의 kubectl을 사용하면 예기치 않은 문제를 피할 수 있다.

## 윈도우에 kubectl 설치

다음과 같은 방법으로 윈도우에 kubectl을 설치할 수 있다.

- [윈도우에서 curl을 사용하여 kubectl 바이너리 설치](#install-kubectl-binary-with-curl-on-windows)
- [Chocolatey 또는 Scoop을 사용하여 윈도우에 설치](#install-on-windows-using-chocolatey-or-scoop)


### 윈도우에서 curl을 사용하여 kubectl 바이너리 설치 {#install-kubectl-binary-with-curl-on-windows}

1. [최신 릴리스 {{< param "fullversion" >}}](https://dl.k8s.io/release/{{< param "fullversion" >}}/bin/windows/amd64/kubectl.exe)를 다운로드한다.

   또는 `curl` 을 설치한 경우, 다음 명령을 사용한다.

   ```powershell
   curl -LO https://dl.k8s.io/release/{{< param "fullversion" >}}/bin/windows/amd64/kubectl.exe
   ```

   {{< note >}}
   최신의 안정 버전(예: 스크립팅을 위한)을 찾으려면, [https://dl.k8s.io/release/stable.txt](https://dl.k8s.io/release/stable.txt)를 참고한다.
   {{< /note >}}

1. 바이너리를 검증한다. (선택 사항)

   kubectl 체크섬 파일을 다운로드한다.

   ```powershell
   curl -LO https://dl.k8s.io/{{< param "fullversion" >}}/bin/windows/amd64/kubectl.exe.sha256
   ```

   kubectl 바이너리를 체크섬 파일을 통해 검증한다.

   - 수동으로 `CertUtil` 의 출력과 다운로드한 체크섬 파일을 비교하기 위해서 커맨드 프롬프트를 사용한다.

     ```cmd
     CertUtil -hashfile kubectl.exe SHA256
     type kubectl.exe.sha256
     ```

   - `-eq` 연산자를 통해 `True` 또는 `False` 결과를 얻는 자동 검증을 위해서 PowerShell을 사용한다.

     ```powershell
     $($(CertUtil -hashfile .\kubectl.exe SHA256)[1] -replace " ", "") -eq $(type .\kubectl.exe.sha256)
     ```

1. 바이너리를 `PATH` 가 설정된 디렉터리에 추가한다.

1. `kubectl` 의 버전이 다운로드한 버전과 같은지 확인한다.

   ```cmd
   kubectl version --client
   ```

{{< note >}}
[윈도우용 도커 데스크톱](https://docs.docker.com/docker-for-windows/#kubernetes)은 자체 버전의 `kubectl` 을 `PATH` 에 추가한다.
도커 데스크톱을 이전에 설치한 경우, 도커 데스크톱 설치 프로그램에서 추가한 `PATH` 항목 앞에 `PATH` 항목을 배치하거나 도커 데스크톱의 `kubectl` 을 제거해야 할 수도 있다.
{{< /note >}}

### Chocolatey 또는 Scoop을 사용하여 윈도우에 설치 {#install-on-windows-using-chocolatey-or-scoop}

1. 윈도우에 kubectl을 설치하기 위해서 [Chocolatey](https://chocolatey.org) 패키지 관리자나 [Scoop](https://scoop.sh) 커맨드 라인 설치 프로그램을 사용할 수 있다.

   {{< tabs name="kubectl_win_install" >}}
   {{% tab name="choco" %}}
   ```powershell
    choco install kubernetes-cli
   ```
   {{% /tab %}}
   {{% tab name="scoop" %}}
   ```powershell
    scoop install kubectl
   ```
   {{% /tab %}}
   {{< /tabs >}}


1. 설치한 버전이 최신 버전인지 확인한다.

   ```powershell
   kubectl version --client
   ```

1. 홈 디렉터리로 이동한다.

   ```powershell
   # cmd.exe를 사용한다면, 다음을 실행한다. cd %USERPROFILE%
   cd ~
   ```

1. `.kube` 디렉터리를 생성한다.

   ```powershell
   mkdir .kube
   ```

1. 금방 생성한 `.kube` 디렉터리로 이동한다.

   ```powershell
   cd .kube
   ```

1. 원격 쿠버네티스 클러스터를 사용하도록 kubectl을 구성한다.

   ```powershell
   New-Item config -type file
   ```

{{< note >}}
메모장과 같은 텍스트 편집기를 선택하여 구성 파일을 편집한다.
{{< /note >}}

## kubectl 구성 확인

{{< include "included/verify-kubectl.md" >}}

## 선택적 kubectl 구성

### 셸 자동 완성 활성화

kubectl은 Bash 및 Zsh에 대한 자동 완성 지원을 제공하므로 입력을 위한 타이핑을 많이 절약할 수 있다.

다음은 Zsh에 대한 자동 완성을 설정하는 절차이다.

{{< include "included/optional-kubectl-configs-zsh.md" >}}

## {{% heading "whatsnext" %}}

{{< include "included/kubectl-whats-next.md" >}}
