---
title: 다중 클러스터 접근 구성
content_type: task
weight: 30
card:
  name: tasks
  weight: 40
---

<!-- overview -->

이 페이지에서는 구성 파일을 사용하여 다수의 클러스터에 접근할 수 있도록
설정하는 방식을 보여준다. 클러스터, 사용자, 컨텍스트가 하나 이상의
구성 파일에 정의된 다음 `kubectl config use-context` 커맨드를
사용하여 클러스터를 빠르게 변경할 수 있다.

{{< note >}}
클러스터에 접근할 수 있도록 설정하는데 사용되는 파일은 종종 *kubeconfig file* 이라고
불린다. 이는 구성 파일을 참조하는 일반적인 방식으로 `kubeconfig`라는 이름을 가진 파일이
반드시 존재해야 한다는 것을 의미하는 것은 아니다.
{{< /note >}}

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}}

{{< glossary_tooltip text="kubectl" term_id="kubectl" >}}이 설치되었는지 확인하려면,
`kubectl version --client`을 실행한다. kubectl 버전은 클러스터의 API 서버 버전과
[마이너 버전 하나 차이 이내](/ko/releases/version-skew-policy/#kubectl)여야
한다.

<!-- steps -->

## 클러스터, 사용자, 컨텍스트 정의

당신이 개발 작업을 위한 클러스터와 스크래치 작업을 위한 클러스터를 가지고 있다고 가정해보자.
`development` 클러스터에서는 프런트 엔드 개발자들이 `frontend`라는 네임스페이스에서
작업을 하고 있고, 스토리지 개발자들은 `storage`라는 네임스페이스에서 작업을 하고 있다.
`scratch` 클러스터에서는 개발자들이 default 네임스페이스에서 개발하거나 필요에 따라 보조
네임스페이스들을 생성하고 있다. development 클러스터에 접근하려면 인증서로 인증을 해야 하고,
scratch 클러스터에 접근하려면 사용자네임과 패스워드로 인증을 해야 한다.

`config-exercise`라는 디렉터리를 생성한다. `config-exercise` 디렉터리에
다음 내용을 가진 `config-demo`라는 파일을 생성한다.

```yaml
apiVersion: v1
kind: Config
preferences: {}

clusters:
- cluster:
  name: development
- cluster:
  name: scratch

users:
- name: developer
- name: experimenter

contexts:
- context:
  name: dev-frontend
- context:
  name: dev-storage
- context:
  name: exp-scratch
```

구성 파일은 클러스터들, 사용자들, 컨텍스트들을 기술한다. `config-demo` 파일은 두 클러스터들과
두 사용자들, 세 컨텍스트들을 기술하기 위한 프레임워크를 가진다.

`config-exercise` 디렉터리로 이동한다. 그리고 다음 커맨드들을 실행하여 구성 파일에 클러스터의
세부사항들을 추가한다.

```shell
kubectl config --kubeconfig=config-demo set-cluster development --server=https://1.2.3.4 --certificate-authority=fake-ca-file
kubectl config --kubeconfig=config-demo set-cluster scratch --server=https://5.6.7.8 --insecure-skip-tls-verify
```

사용자의 세부사항들을 구성 파일에 추가한다.

```shell
kubectl config --kubeconfig=config-demo set-credentials developer --client-certificate=fake-cert-file --client-key=fake-key-seefile
kubectl config --kubeconfig=config-demo set-credentials experimenter --username=exp --password=some-password
```

{{< note >}}
- 사용자를 삭제하려면 `kubectl --kubeconfig=config-demo config unset users.<name>` 를 실행한다.
- 클러스터를 제거하려면 `kubectl --kubeconfig=config-demo config unset clusters.<name>` 를 실행한다.
- 컨텍스트를 제거하려면 `kubectl --kubeconfig=config-demo config unset contexts.<name>` 를 실행한다.
{{< /note >}}

컨텍스트 세부사항들을 구성 파일에 추가한다.

```shell
kubectl config --kubeconfig=config-demo set-context dev-frontend --cluster=development --namespace=frontend --user=developer
kubectl config --kubeconfig=config-demo set-context dev-storage --cluster=development --namespace=storage --user=developer
kubectl config --kubeconfig=config-demo set-context exp-scratch --cluster=scratch --namespace=default --user=experimenter
```

`config-demo` 파일을 열어서 세부사항들이 추가되었는지 확인한다. `config-demo` 파일을 열어보는
것 대신에 `config view` 커맨드를 사용할 수도 있다.

```shell
kubectl config --kubeconfig=config-demo view
```

두 클러스터, 두 사용자, 세 컨텍스트들이 출력 결과로 나온다.

```yaml
apiVersion: v1
clusters:
- cluster:
    certificate-authority: fake-ca-file
    server: https://1.2.3.4
  name: development
- cluster:
    insecure-skip-tls-verify: true
    server: https://5.6.7.8
  name: scratch
contexts:
- context:
    cluster: development
    namespace: frontend
    user: developer
  name: dev-frontend
- context:
    cluster: development
    namespace: storage
    user: developer
  name: dev-storage
- context:
    cluster: scratch
    namespace: default
    user: experimenter
  name: exp-scratch
current-context: ""
kind: Config
preferences: {}
users:
- name: developer
  user:
    client-certificate: fake-cert-file
    client-key: fake-key-file
- name: experimenter
  user:
    password: some-password
    username: exp
```

위 `fake-ca-file`, `fake-cert-file`, `fake-key-file`은 인증서 파일들의 실제 경로 이름을 위한
플레이스홀더(placeholder)이다.
당신의 환경에 맞게 이들을 실제 인증서 경로로 변경해줘야 한다.

만약 당신이 인증서 파일들의 경로 대신에 여기에 포함된 base64로 인코딩된 데이터를 사용하려고 한다면
이 경우 키에 `-data` 접미사를 추가해야 한다. 예를 들면 `certificate-authority-data`,
`client-certificate-data`, `client-key-data` 같이 사용할 수 있다.

컨텍스트는 세 가지(클러스터, 사용자, 네임스페이스) 요소들로 이뤄진다. 예를 들어
`dev-frontend` 컨텍스트는 "`development` 클러스터의 `frontend` 네임스페이스에 접근하는데
`developer` 사용자 자격증명을 사용하라고 알려준다."

현재 컨텍스트를 설정한다.

```shell
kubectl config --kubeconfig=config-demo use-context dev-frontend
```

이제 당신이 `kubectl` 커맨드를 입력할 때마다 `dev-frontend` 컨텍스트에 명시된 클러스터와
네임스페이스 상에서 동작하게 될 것이다. 그리고 커맨드는 `dev-frontend` 컨텍스트 내에 명시된
사용자 자격증명을 사용할 것이다.

현재 컨텍스트에 관련된 구성 정보만을 보려면
`--minify` 플래그를 사용한다.

```shell
kubectl config --kubeconfig=config-demo view --minify
```

`dev-frontend` 컨텍스트에 관련된 구성 정보가 출력 결과로 표시될 것이다.

```yaml
apiVersion: v1
clusters:
- cluster:
    certificate-authority: fake-ca-file
    server: https://1.2.3.4
  name: development
contexts:
- context:
    cluster: development
    namespace: frontend
    user: developer
  name: dev-frontend
current-context: dev-frontend
kind: Config
preferences: {}
users:
- name: developer
  user:
    client-certificate: fake-cert-file
    client-key: fake-key-file
```

이제 당신이 잠시 scratch 클러스터에서 작업하려고 한다고 가정해보자.

현재 컨텍스트를 `exp-scratch`로 변경한다.

```shell
kubectl config --kubeconfig=config-demo use-context exp-scratch
```

이제 당신이 실행하는 모든 `kubectl` 커맨드는 `scratch` 클러스터의
default 네임스페이스에 적용되며 `exp-scratch` 컨텍스트에 나열된
사용자의 자격증명을 사용할 것이다.

현재의 컨텍스트인 `exp-scratch`에 관련된 설정을 보자.

```shell
kubectl config --kubeconfig=config-demo view --minify
```

마지막으로 당신이 `development` 클러스터의 `storage` 네임스페이스에서
잠시 작업을 하려고 한다고 가정해보자.

현재 컨텍스트를 `dev-storage`로 변경한다.

```shell
kubectl config --kubeconfig=config-demo use-context dev-storage
```

현재 컨텍스트인 `dev-storage`에 관련된 설정을 보자.

```shell
kubectl config --kubeconfig=config-demo view --minify
```

## 두 번째 구성 파일 생성

`config-exercise` 디렉터리에서 다음 내용으로 `config-demo-2`라는 파일을 생성한다.

```yaml
apiVersion: v1
kind: Config
preferences: {}

contexts:
- context:
    cluster: development
    namespace: ramp
    user: developer
  name: dev-ramp-up
```

위 구성 파일은 `dev-ramp-up`이라는 신규 컨텍스트를 정의한다.

## KUBECONFIG 환경 변수 설정

`KUBECONFIG`라는 환경 변수를 가지고 있는지 확인해보자. 만약 가지고 있다면,
이후에 복원할 수 있도록 `KUBECONFIG` 환경 변수의 현재 값을 저장한다.
예:

### 리눅스

```shell
export KUBECONFIG_SAVED=$KUBECONFIG
```

### 윈도우 PowerShell

```powershell
$Env:KUBECONFIG_SAVED=$ENV:KUBECONFIG
```

`KUBECONFIG` 환경 변수는 구성 파일들의 경로의 리스트이다. 이 리스트는
리눅스와 Mac에서는 콜론으로 구분되며 윈도우에서는 세미콜론으로 구분된다.
`KUBECONFIG` 환경 변수를 가지고 있다면, 리스트에 포함된 구성 파일들에
익숙해지길 바란다.

다음 예와 같이 임시로 `KUBECONFIG` 환경 변수에 두 개의 경로들을 덧붙여보자.

### 리눅스

```shell
export KUBECONFIG=$KUBECONFIG:config-demo:config-demo-2
```

### 윈도우 PowerShell

```powershell
$Env:KUBECONFIG=("config-demo;config-demo-2")
```

`config-exercise` 디렉터리에서 다음 커맨드를 입력한다.

```shell
kubectl config view
```

당신의 `KUBECONFIG` 환경 변수에 나열된 모든 파일들이 합쳐진 정보가 출력 결과로
표시될 것이다. 특히, 합쳐진 정보가 `config-demo-2` 파일의 `dev-ramp-up`
컨텍스트와 `config-demo` 파일의 세 개의 컨텍스트들을
가지고 있다는 것에 주목하길 바란다.

```yaml
contexts:
- context:
    cluster: development
    namespace: frontend
    user: developer
  name: dev-frontend
- context:
    cluster: development
    namespace: ramp
    user: developer
  name: dev-ramp-up
- context:
    cluster: development
    namespace: storage
    user: developer
  name: dev-storage
- context:
    cluster: scratch
    namespace: default
    user: experimenter
  name: exp-scratch
```

kubeconfig 파일들을 어떻게 병합하는지에 대한 상세정보는
[kubeconfig 파일을 사용하여 클러스터 접근 구성하기](/ko/docs/concepts/configuration/organize-cluster-access-kubeconfig/)를 참조한다.

## $HOME/.kube 디렉터리 탐색

만약 당신이 이미 클러스터를 가지고 있고 `kubectl`을 사용하여
해당 클러스터를 제어하고 있다면, 아마 `$HOME/.kube` 디렉터리에 `config`라는
파일을 가지고 있을 것이다.

`$HOME/.kube`로 가서 어떤 파일들이 존재하는지 보자.
보통 `config`라는 파일이 존재할 것이다. 해당 디렉터리 내에는 다른 구성 파일들도 있을 수 있다.
간단하게 말하자면 당신은 이 파일들의 컨텐츠에 익숙해져야 한다.

## $HOME/.kube/config를 KUBECONFIG 환경 변수에 추가

당신이 `$HOME/.kube/config` 파일을 가지고 있는데 `KUBECONFIG`
환경 변수에 나타나지 않는다면 `KUBECONFIG` 환경 변수에 추가해보자.
예:

### 리눅스

```shell
export KUBECONFIG=$KUBECONFIG:$HOME/.kube/config
```

### 윈도우 Powershell

```powershell
$Env:KUBECONFIG="$Env:KUBECONFIG;$HOME\.kube\config"
```

이제 `KUBECONFIG` 환경 변수에 리스트에 포함된 모든 파일들이 합쳐진 구성 정보를 보자.
config-exercise 디렉터리에서 다음 커맨드를 실행한다.

```shell
kubectl config view
```

## 정리

`KUBECONFIG` 환경 변수를 원래 값으로 되돌려 놓자. 예를 들면:<br>

### 리눅스

```shell
export KUBECONFIG=$KUBECONFIG_SAVED
```

### 윈도우 PowerShell

```powershell
$Env:KUBECONFIG=$ENV:KUBECONFIG_SAVED
```

## {{% heading "whatsnext" %}}

* [kubeconfig 파일을 사용하여 클러스터 접근 구성하기](/ko/docs/concepts/configuration/organize-cluster-access-kubeconfig/)
* [kubectl config](/docs/reference/generated/kubectl/kubectl-commands#config)
