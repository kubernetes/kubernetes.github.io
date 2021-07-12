---
title: 쿠버네티스에서 윈도우 컨테이너 스케줄링을 위한 가이드
content_type: concept
weight: 75
---

<!-- overview -->

많은 조직에서 실행하는 서비스와 애플리케이션의 상당 부분이 윈도우 애플리케이션으로 구성된다.
이 가이드는 쿠버네티스에서 윈도우 컨테이너를 구성하고 배포하는 단계를 안내한다.



<!-- body -->

## 목표

* 윈도우 노드에서 윈도우 컨테이너를 실행하는 예시 디플로이먼트를 구성한다.
* (선택) 그룹 매니지드 서비스 어카운트(GMSA)를 이용한 사용자 파드를 위한 액티브 디렉터리 신원(Active Directory Identity)을 구성한다.

## 시작하기 전에

* [윈도우 서버에서 운영하는 마스터와 워커 노드](/ko/docs/tasks/administer-cluster/kubeadm/adding-windows-nodes)를
포함한 쿠버네티스 클러스터를 생성한다.
* 쿠버네티스에서 서비스와 워크로드를 생성하고 배포하는 것은 리눅스나 윈도우 컨테이너
모두 비슷한 방식이라는 것이 중요하다.
[Kubectl 커맨드](/ko/docs/reference/kubectl/overview/)로 클러스터에 접속하는 것은 동일하다.
아래 단원의 예시를 통해 윈도우 컨테이너와 좀 더 빨리 친숙해질 수 있다.

## 시작하기: 윈도우 컨테이너 배포하기

쿠버네티스에서 윈도우 컨테이너를 배포하려면, 먼저 예시 애플리케이션을 생성해야 한다.
아래 예시 YAML 파일은 간단한 웹서버 애플리케이션을 생성한다.
아래 내용으로 채운 서비스 스펙을 `win-webserver.yaml`로 생성하자.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: win-webserver
  labels:
    app: win-webserver
spec:
  ports:
    # 이 서비스에서 제공하는 포트
    - port: 80
      targetPort: 80
  selector:
    app: win-webserver
  type: NodePort
---
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: win-webserver
  name: win-webserver
spec:
  replicas: 2
  selector:
    matchLabels:
      app: win-webserver
  template:
    metadata:
      labels:
        app: win-webserver
      name: win-webserver
    spec:
     containers:
      - name: windowswebserver
        image: mcr.microsoft.com/windows/servercore:ltsc2019
        command:
        - powershell.exe
        - -command
        - "<#code used from https://gist.github.com/19WAS85/5424431#> ; $$listener = New-Object System.Net.HttpListener ; $$listener.Prefixes.Add('http://*:80/') ; $$listener.Start() ; $$callerCounts = @{} ; Write-Host('Listening at http://*:80/') ; while ($$listener.IsListening) { ;$$context = $$listener.GetContext() ;$$requestUrl = $$context.Request.Url ;$$clientIP = $$context.Request.RemoteEndPoint.Address ;$$response = $$context.Response ;Write-Host '' ;Write-Host('> {0}' -f $$requestUrl) ;  ;$$count = 1 ;$$k=$$callerCounts.Get_Item($$clientIP) ;if ($$k -ne $$null) { $$count += $$k } ;$$callerCounts.Set_Item($$clientIP, $$count) ;$$ip=(Get-NetAdapter | Get-NetIpAddress); $$header='<html><body><H1>Windows Container Web Server</H1>' ;$$callerCountsString='' ;$$callerCounts.Keys | % { $$callerCountsString+='<p>IP {0} callerCount {1} ' -f $$ip[1].IPAddress,$$callerCounts.Item($$_) } ;$$footer='</body></html>' ;$$content='{0}{1}{2}' -f $$header,$$callerCountsString,$$footer ;Write-Output $$content ;$$buffer = [System.Text.Encoding]::UTF8.GetBytes($$content) ;$$response.ContentLength64 = $$buffer.Length ;$$response.OutputStream.Write($$buffer, 0, $$buffer.Length) ;$$response.Close() ;$$responseStatus = $$response.StatusCode ;Write-Host('< {0}' -f $$responseStatus)  } ; "
     nodeSelector:
      kubernetes.io/os: windows
```

{{< note >}}
포트 매핑도 지원하지만, 간략한 예시를 위해
컨테이너 포트 80을 직접 서비스로 노출한다.
{{< /note >}}

1. 모든 노드가 건강한지 확인한다.

    ```bash
    kubectl get nodes
    ```

1. 서비스를 배포하고 파드 갱신을 지켜보자.

    ```bash
    kubectl apply -f win-webserver.yaml
    kubectl get pods -o wide -w
    ```

    이 서비스가 정확히 배포되면 모든 파드는 Ready로 표기된다. 지켜보기를 중단하려면, Ctrl+C 를 누르자.

1. 이 디플로이먼트가 성공적인지 확인한다. 다음을 검토하자.

    * 윈도우 노드에 파드당 두 컨테이너가 존재하는지 확인하려면, `docker ps`를 사용한다.
    * 리눅스 마스터에서 나열된 두 파드가 존재하는지 확인하려면, `kubectl get pods`를 사용한다.
    * 네트워크를 통한 노드에서 파드로의 통신이 되는지 확인하려면, 리눅스 마스터에서 `curl`을
      파드 IP 주소의 80 포트로 실행하여 웹 서버 응답을 확인한다.
    * 파드 간 통신이 되는지 확인하려면, `docker exec` 나 `kubectl exec`를 이용해 파드 간에
      핑(ping)한다(윈도우 노드가 2대 이상이라면, 서로 다른 노드에 있는 파드 간 통신도 확인할 수 있다).
    * 서비스에서 파드로의 통신이 되는지 확인하려면, 리눅스 마스터와 독립 파드에서 `curl`을 가상 서비스
      IP 주소(`kubectl get services`로 볼 수 있는)로 실행한다.
    * 서비스 검색(discovery)이 되는지 확인하려면, 쿠버네티스 [기본 DNS 접미사](/ko/docs/concepts/services-networking/dns-pod-service/#서비스)와 서비스 이름으로 `curl`을 실행한다.
    * 인바운드 연결이 되는지 확인하려면, 클러스터 외부 장비나 리눅스 마스터에서 NodePort로 `curl`을 실행한다.
    * 아웃바운드 연결이 되는지 확인하려면, `kubectl exec`를 이용해서 파드에서 외부 IP 주소로 `curl`을 실행한다.

{{< note >}}
윈도우 컨테이너 호스트는 현재 윈도우 네트워킹 스택의 플랫폼 제한으로 인해, 그 안에서 스케줄링하는 서비스의 IP 주소로 접근할 수 없다.
윈도우 파드만 서비스 IP 주소로 접근할 수 있다.
{{< /note >}}

## 가시성

### 워크로드에서 로그 캡쳐하기

로그는 가시성의 중요한 요소이다. 로그는 사용자가 워크로드의 운영측면을
파악할 수 있도록 하며 문제 해결의 핵심 요소이다.
윈도우 컨테이너, 그리고 윈도우 컨테이너 내의 워크로드는 리눅스 컨테이너와는 다르게 동작하기 때문에,
사용자가 로그를 수집하기 어려웠고 이로 인해 운영 가시성이 제한되어 왔다.
예를 들어 윈도우 워크로드는 일반적으로 ETW(Event Tracing for Windows)에 로그인하거나
애플리케이션 이벤트 로그에 항목을 푸시하도록 구성한다.
Microsoft의 오픈 소스 도구인 [LogMonitor](https://github.com/microsoft/windows-container-tools/tree/master/LogMonitor)는
윈도우 컨테이너 안에 구성된 로그 소스를 모니터링하는 권장하는 방법이다.
LogMonitor는 이벤트 로그, ETW 공급자 그리고 사용자 정의 애플리케이션 로그 모니터링을 지원하고
`kubectl logs <pod>` 에 의한 사용을 위해 STDOUT으로 파이프한다.

LogMonitor GitHub 페이지의 지침에 따라 모든 컨테이너 바이너리와 설정 파일을 복사하고,
LogMonitor가 로그를 STDOUT으로 푸시할 수 있도록 필요한 엔트리포인트를 추가한다.

## 설정 가능한 컨테이너 username 사용하기

쿠버네티스 v1.16 부터, 윈도우 컨테이너는 이미지 기본 값과는 다른 username으로 엔트리포인트와 프로세스를
실행하도록 설정할 수 있다.
이 방식은 리눅스 컨테이너에서 지원되는 방식과는 조금 차이가 있다.
[여기](/ko/docs/tasks/configure-pod-container/configure-runasusername/)에서 이에 대해 추가적으로 배울 수 있다.

## 그룹 매니지드 서비스 어카운트를 이용하여 워크로드 신원 관리하기

쿠버네티스 v1.14부터 윈도우 컨테이너 워크로드는 그룹 매니지드 서비스 어카운트(GMSA, Group Managed Service Account)를 이용하여 구성할 수 있다.
그룹 매니지드 서비스 어카운트는 액티브 디렉터리 어카운트의 특정한 종류로 자동 암호 관리 기능,
단순화된 서비스 주체 이름(SPN, simplified service principal name), 여러 서버의 다른 관리자에게 관리를 위임하는 기능을 제공한다.
GMSA로 구성한 컨테이너는 GMSA로 구성된 신원을 들고 있는 동안 외부 액티브 디렉터리 도메인 리소스를 접근할 수 있다.
윈도우 컨테이너를 위한 GMSA를 이용하고 구성하는 방법은 [여기](/docs/tasks/configure-pod-container/configure-gmsa/)에서 알아보자.

## 테인트(Taint)와 톨러레이션(Toleration)

오늘날 사용자는 리눅스와 윈도우 워크로드를 (동일한 OS를 실행하는) 적절한 노드에 할당되도록 하기 위해 테인트와
노드셀렉터(nodeSelector)의 조합을 이용해야 한다.
이것은 윈도우 사용자에게만 부담을 줄 것으로 보인다. 아래는 권장되는 방식의 개요인데,
이것의 주요 목표 중에 하나는 이 방식이 기존 리눅스 워크로드와 호환되어야 한다는 것이다.

### 특정 OS 워크로드를 적절한 컨테이너 호스트에서 처리하도록 보장하기

사용자는 테인트와 톨러레이션을 이용하여 윈도우 컨테이너가 적절한 호스트에서 스케줄링되기를 보장할 수 있다.
오늘날 모든 쿠버네티스 노드는 다음 기본 레이블을 가지고 있다.

* kubernetes.io/os = [windows|linux]
* kubernetes.io/arch = [amd64|arm64|...]

파드 사양에 노드 셀렉터를 `"kubernetes.io/os": windows`와 같이 지정하지 않았다면,
그 파드는 리눅스나 윈도우, 아무 호스트에나 스케줄링될 수 있다.
윈도우 컨테이너는 윈도우에서만 운영될 수 있고 리눅스 컨테이너는 리눅스에서만 운영될 수 있기 때문에 이는 문제를 일으킬 수 있다.
가장 좋은 방법은 노드 셀렉터를 사용하는 것이다.

그러나 많은 경우 사용자는 이미 존재하는 대량의 리눅스 컨테이너용 디플로이먼트를 가지고 있을 뿐만 아니라,
헬름(Helm) 차트 커뮤니티 같은 상용 구성의 에코시스템이나, 오퍼레이터(Operator) 같은 프로그래밍 방식의 파드 생성 사례가 있음을 알고 있다.
이런 상황에서는 노드 셀렉터를 추가하는 구성 변경을 망설일 수 있다.
이에 대한 대안은 테인트를 사용하는 것이다. Kubelet은 등록하는 동안 테인트를 설정할 수 있기 때문에,
윈도우에서만 운영할 때에 자동으로 테인트를 추가하기 쉽다.

예를 들면,  `--register-with-taints='os=windows:NoSchedule'`

모든 윈도우 노드에 테인트를 추가하여 아무 것도 거기에 스케줄링하지 않게 될 것이다(존재하는 리눅스 파드를 포함하여).
윈도우 파드가 윈도우 노드에 스케줄링되려면,
윈도우를 선택하기 위한 노드 셀렉터 및 적합하게 일치하는 톨러레이션이 모두 필요하다.

```yaml
nodeSelector:
    kubernetes.io/os: windows
    node.kubernetes.io/windows-build: '10.0.17763'
tolerations:
    - key: "os"
      operator: "Equal"
      value: "windows"
      effect: "NoSchedule"
```

### 동일 클러스터에서 여러 윈도우 버전을 조작하는 방법

파드에서 사용하는 윈도우 서버 버전은 노드의 윈도우 서버 버전과 일치해야 한다. 만약 동일한 클러스터에서 여러 윈도우
서버 버전을 사용하려면, 추가로 노드 레이블과 nodeSelectors를 설정해야 한다.

쿠버네티스 1.17은 이것을 단순화하기 위해 새로운 레이블인 `node.kubernetes.io/windows-build` 를 자동으로 추가한다.
만약 이전 버전을 실행 중인 경우, 이 레이블을 윈도우 노드에 수동으로 추가하는 것을 권장한다.

이 레이블은 호환성을 위해 일치시켜야 하는 윈도우 메이저, 마이너 및 빌드 번호를 나타낸다.
각 윈도우 서버 버전에 대해 현재 사용하고 있는 빌드 번호는 다음과 같다.

| 제품 이름                            |   빌드 번호            |
|--------------------------------------|------------------------|
| 윈도우 서버 2019                      | 10.0.17763             |
| 윈도우 서버 버전 1809                 | 10.0.17763             |
| 윈도우 서버 버전 1903                 | 10.0.18362             |


### RuntimeClass로 단순화

[런타임클래스(RuntimeClass)](/ko/docs/concepts/containers/runtime-class/)를 사용해서 테인트(taint)와 톨러레이션(toleration)을 사용하는 프로세스를 간소화 할 수 있다.
클러스터 관리자는 이 테인트와 톨러레이션을 캡슐화하는 데 사용되는 `RuntimeClass` 오브젝트를 생성할 수 있다.


1. 이 파일을 `runtimeClasses.yml` 로 저장한다. 여기에는 윈도우 OS,
아키텍처 및 버전에 적합한 `nodeSelector` 가 포함되어 있다.

```yaml
apiVersion: node.k8s.io/v1
kind: RuntimeClass
metadata:
  name: windows-2019
handler: 'docker'
scheduling:
  nodeSelector:
    kubernetes.io/os: 'windows'
    kubernetes.io/arch: 'amd64'
    node.kubernetes.io/windows-build: '10.0.17763'
  tolerations:
  - effect: NoSchedule
    key: os
    operator: Equal
    value: "windows"
```

2. 클러스터 관리자로 `kubectl create -f runtimeClasses.yml` 를 실행해서 사용한다.
3. 파드 사양에 적합한 `runtimeClassName: windows-2019` 를 추가한다.

예시:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: iis-2019
  labels:
    app: iis-2019
spec:
  replicas: 1
  template:
    metadata:
      name: iis-2019
      labels:
        app: iis-2019
    spec:
      runtimeClassName: windows-2019
      containers:
      - name: iis
        image: mcr.microsoft.com/windows/servercore/iis:windowsservercore-ltsc2019
        resources:
          limits:
            cpu: 1
            memory: 800Mi
          requests:
            cpu: .1
            memory: 300Mi
        ports:
          - containerPort: 80
 selector:
    matchLabels:
      app: iis-2019
---
apiVersion: v1
kind: Service
metadata:
  name: iis
spec:
  type: LoadBalancer
  ports:
  - protocol: TCP
    port: 80
  selector:
    app: iis-2019
```




[RuntimeClass]: https://kubernetes.io/docs/concepts/containers/runtime-class/
