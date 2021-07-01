---
title: 이미지
content_type: concept
weight: 10
---

<!-- overview -->

컨테이너 이미지는 애플리케이션과 모든 소프트웨어 의존성을 캡슐화하는 바이너리 데이터를
나타낸다. 컨테이너 이미지는 독립적으로 실행할 수 있고 런타임 환경에 대해
잘 정의된 가정을 만드는 실행 가능한 소프트웨어 번들이다.

일반적으로 {{< glossary_tooltip text="파드" term_id="pod" >}}에서
참조하기 전에 애플리케이션의 컨테이너 이미지를
생성해서 레지스트리로 푸시한다.

이 페이지는 컨테이너 이미지 개념의 개요를 제공한다.




<!-- body -->

## 이미지 이름

컨테이너 이미지는 일반적으로 `pause`, `example/mycontainer` 또는 `kube-apiserver` 와 같은 이름을 부여한다.
이미지는 또한 레지스트리 호스트 이름을 포함할 수 있다. 예를 들면, `fictional.registry.example/imagename`
과 같다. 그리고 포트 번호도 포함할 수 있다. 예를 들면, `fictional.registry.example:10443/imagename` 과 같다.

레지스트리 호스트 이름을 지정하지 않으면, 쿠버네티스는 도커 퍼블릭 레지스트리를 의미한다고 가정한다.

이미지 이름 부분 다음에 _tag_ 를 추가할 수 있다(`docker` 와 `podman`
등의 명령과 함께 사용).
태그를 사용하면 동일한 시리즈 이미지의 다른 버전을 식별할 수 있다.

이미지 태그는 소문자와 대문자, 숫자, 밑줄(`_`),
마침표(`.`) 및 대시(`-`)로 구성된다.
이미지 태그 안에서 구분 문자(`_`, `-` 그리고 `.`)를
배치할 수 있는 위치에 대한 추가 규칙이 있다.
태그를 지정하지 않으면, 쿠버네티스는 태그 `latest` 를 의미한다고 가정한다.

{{< caution >}}
프로덕션에서 컨테이너를 배포할 때는 `latest` 태그를 사용하지 않아야 한다.
실행 중인 이미지 버전을 추적하기가 어렵고
이전에 잘 동작하던 버전으로 롤백하기가 더 어렵다.

대신, `v1.42.0` 과 같은 의미있는 태그를 지정한다.
{{< /caution >}}

## 이미지 업데이트

{{< glossary_tooltip text="디플로이먼트" term_id="deployment" >}},
{{< glossary_tooltip text="스테이트풀셋" term_id="statefulset" >}}, 파드 또는 파드
템플릿은 포함하는 다른 오브젝트를 처음 만들 때 특별히 명시하지 않은 경우
기본적으로 해당 파드에 있는 모든 컨테이너의 풀(pull)
정책은 `IfNotPresent`로 설정된다. 이 정책은
{{< glossary_tooltip text="kubelet" term_id="kubelet" >}}이 이미 존재하는
이미지에 대한 풀을 생략하게 한다.

만약 항상 풀을 강제하고 싶다면, 다음 중 하나를 수행하면 된다.

- 컨테이너의 `imagePullPolicy`를 `Always`로 설정.
- `imagePullPolicy`를 생략하고 `:latest`를 사용할 이미지의 태그로 사용,
  쿠버네티스는 정책을 `Always`로 설정한다.
- `imagePullPolicy`와 사용할 이미지의 태그를 생략.
- [AlwaysPullImages](/docs/reference/access-authn-authz/admission-controllers/#alwayspullimages) 어드미션 컨트롤러를 활성화.

{{< note >}}
컨테이너의 `imagePullPolicy` 값은 오브젝트가 처음 _created_ 일 때 항상
설정되고 나중에 이미지 태그가 변경되더라도 업데이트되지 않는다.

예를 들어, 태그가 `:latest`가 아닌 이미지로 디플로이먼트를 생성하고,
나중에 해당 디플로이먼트의 이미지를 `:latest` 태그로 업데이트하면
`imagePullPolicy` 필드가 `Always` 로 변경되지 않는다. 오브젝트를
처음 생성 한 후 모든 오브젝트의 풀 정책을 수동으로 변경해야 한다.
{{< /note >}}

`imagePullPolicy` 가 특정값 없이 정의되면, `Always` 로 설정된다.

## 이미지 인덱스가 있는 다중 아키텍처 이미지

바이너리 이미지를 제공할 뿐만 아니라, 컨테이너 레지스트리는 [컨테이너 이미지 인덱스](https://github.com/opencontainers/image-spec/blob/master/image-index.md)를 제공할 수도 있다. 이미지 인덱스는 컨테이너의 아키텍처별 버전에 대한 여러 [이미지 매니페스트](https://github.com/opencontainers/image-spec/blob/master/manifest.md)를 가리킬 수 있다. 아이디어는 이미지의 이름(예를 들어, `pause`, `example/mycontainer`, `kube-apiserver`)을 가질 수 있다는 것이다. 그래서 다른 시스템들이 사용하고 있는 컴퓨터 아키텍처에 적합한 바이너리 이미지를 가져올 수 있다.

쿠버네티스 자체는 일반적으로 `-$(ARCH)` 접미사로 컨테이너 이미지의 이름을 지정한다. 이전 버전과의 호환성을 위해, 접미사가 있는 오래된 이미지를 생성한다. 아이디어는 모든 아키텍처에 대한 매니페스트가 있는 `pause` 이미지와 이전 구성 또는 이전에 접미사로 이미지를 하드 코딩한 YAML 파일과 호환되는 `pause-amd64` 라고 하는 이미지를 생성한다.

## 프라이빗 레지스트리 사용

프라이빗 레지스트리는 해당 레지스트리에서 이미지를 읽을 수 있는 키를 요구할 것이다.
자격 증명(credential)은 여러 가지 방법으로 제공될 수 있다.
  - 프라이빗 레지스트리에 대한 인증을 위한 노드 구성
    - 모든 파드는 구성된 프라이빗 레지스트리를 읽을 수 있음
    - 클러스터 관리자에 의한 노드 구성 필요
  - 미리 내려받은(pre-pulled) 이미지
    - 모든 파드는 노드에 캐시된 모든 이미지를 사용 가능
    - 셋업을 위해서는 모든 노드에 대해서 root 접근이 필요
  - 파드에 ImagePullSecrets을 명시
    - 자신의 키를 제공하는 파드만 프라이빗 레지스트리에 접근 가능
  - 공급 업체별 또는 로컬 확장
    - 사용자 정의 노드 구성을 사용하는 경우, 사용자(또는 클라우드
      제공자)가 컨테이너 레지스트리에 대한 노드 인증 메커니즘을
      구현할 수 있다.

이들 옵션은 아래에서 더 자세히 설명한다.

### 프라이빗 레지스트리에 인증하도록 노드 구성

노드에서 도커를 실행하는 경우, 프라이빗 컨테이너 레지스트리를 인증하도록
도커 컨테이너 런타임을 구성할 수 있다.

이 방법은 노드 구성을 제어할 수 있는 경우에 적합하다.

{{< note >}}
기본 쿠버네티스는 도커 구성에서 `auths` 와 `HttpHeaders` 섹션만 지원한다.
도커 자격 증명 도우미(`credHelpers` 또는 `credsStore`)는 지원되지 않는다.
{{< /note >}}


도커는 프라이빗 레지스트리를 위한 키를 `$HOME/.dockercfg` 또는 `$HOME/.docker/config.json` 파일에 저장한다. 만약 동일한 파일을
아래의 검색 경로 리스트에 넣으면, kubelet은 이미지를 풀 할 때 해당 파일을 자격 증명 공급자로 사용한다.

* `{--root-dir:-/var/lib/kubelet}/config.json`
* `{cwd of kubelet}/config.json`
* `${HOME}/.docker/config.json`
* `/.docker/config.json`
* `{--root-dir:-/var/lib/kubelet}/.dockercfg`
* `{cwd of kubelet}/.dockercfg`
* `${HOME}/.dockercfg`
* `/.dockercfg`

{{< note >}}
kubelet 프로세스의 환경 변수에서 `HOME=/root` 를 명시적으로 설정해야 할 수 있다.
{{< /note >}}

프라이빗 레지스트리를 사용도록 사용자의 노드를 구성하기 위해서 권장되는 단계는 다음과 같다. 이
예제의 경우, 사용자의 데스크탑/랩탑에서 아래 내용을 실행한다.

   1. 사용하고 싶은 각 자격 증명 세트에 대해서 `docker login [서버]`를 실행한다. 이것은 여러분 PC의 `$HOME/.docker/config.json`를 업데이트한다.
   1. 편집기에서 `$HOME/.docker/config.json`를 보고 사용하고 싶은 자격 증명만 포함하고 있는지 확인한다.
   1. 노드의 리스트를 구한다. 예를 들면 다음과 같다.
      - 이름을 원하는 경우: `nodes=$( kubectl get nodes -o jsonpath='{range.items[*].metadata}{.name} {end}' )`
      - IP를 원하는 경우: `nodes=$( kubectl get nodes -o jsonpath='{range .items[*].status.addresses[?(@.type=="ExternalIP")]}{.address} {end}' )`
   1. 로컬의 `.docker/config.json`를 위의 검색 경로 리스트 중 하나에 복사한다.
      - 이를 테스트하기 위한 예: `for n in $nodes; do scp ~/.docker/config.json root@"$n":/var/lib/kubelet/config.json; done`

{{< note >}}
프로덕션 클러스터의 경우, 이 설정을 필요한 모든 노드에 적용할 수 있도록
구성 관리 도구를 사용한다.
{{< /note >}}

프라이빗 이미지를 사용하는 파드를 생성하여 검증한다. 예를 들면 다음과 같다.

```shell
kubectl apply -f - <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: private-image-test-1
spec:
  containers:
    - name: uses-private-image
      image: $PRIVATE_IMAGE_NAME
      imagePullPolicy: Always
      command: [ "echo", "SUCCESS" ]
EOF
```
```
pod/private-image-test-1 created
```

만약 모든 것이 잘 작동한다면, 잠시 후에, 다음을 실행할 수 있다.

```shell
kubectl logs private-image-test-1
```
그리고 커맨드 출력을 본다.
```
SUCCESS
```

명령이 실패한 것으로 의심되는 경우 다음을 실행할 수 있다.
```shell
kubectl describe pods/private-image-test-1 | grep 'Failed'
```
실패하는 케이스에는 출력이 다음과 유사하다.
```
  Fri, 26 Jun 2015 15:36:13 -0700    Fri, 26 Jun 2015 15:39:13 -0700    19    {kubelet node-i2hq}    spec.containers{uses-private-image}    failed        Failed to pull image "user/privaterepo:v1": Error: image user/privaterepo:v1 not found
```


클러스터의 모든 노드가 반드시 동일한 `.docker/config.json`를 가져야 한다. 그렇지 않으면, 파드가
일부 노드에서만 실행되고 다른 노드에서는 실패할 것이다. 예를 들어, 노드 오토스케일링을 사용한다면, 각 인스턴스
템플릿은 `.docker/config.json`을 포함하거나 그것을 포함한 드라이브를 마운트해야 한다.

프라이빗 레지스트리 키가 `.docker/config.json`에 추가되고 나면 모든 파드는
프라이빗 레지스트리의 이미지에 읽기 접근 권한을 가지게 될 것이다.

### 미리 내려받은 이미지

{{< note >}}
Google 쿠버네티스 엔진에서 동작 중이라면, 이미 각 노드에 Google 컨테이너 레지스트리에 대한 자격 증명과 함께 `.dockercfg`가 있을 것이다. 그렇다면 이 방법은 쓸 수 없다.
{{< /note >}}

{{< note >}}
이 방법은 노드의 구성을 제어할 수 있는 경우에만 적합하다. 이 방법은
클라우드 제공자가 노드를 관리하고 자동으로 교체한다면 안정적으로
작동하지 않을 것이다.
{{< /note >}}

기본적으로, kubelet은 지정된 레지스트리에서 각 이미지를 풀 하려고 한다.
그러나, 컨테이너의 `imagePullPolicy` 속성이 `IfNotPresent` 또는 `Never`으로 설정되어 있다면,
로컬 이미지가 사용된다(우선적으로 또는 배타적으로).

레지스트리 인증의 대안으로 미리 풀 된 이미지에 의존하고 싶다면,
클러스터의 모든 노드가 동일한 미리 내려받은 이미지를 가지고 있는지 확인해야 한다.

이것은 특정 이미지를 속도를 위해 미리 로드하거나 프라이빗 레지스트리에 대한 인증의 대안으로 사용될 수 있다.

모든 파드는 미리 내려받은 이미지에 대해 읽기 접근 권한을 가질 것이다.

### 파드에 ImagePullSecrets 명시

{{< note >}}
이 방법은 프라이빗 레지스트리의 이미지를 기반으로 컨테이너를 실행하는 데
권장된다.
{{< /note >}}

쿠버네티스는 파드에 컨테이너 이미지 레지스트리 키를 명시하는 것을 지원한다.

#### 도커 구성으로 시크릿 생성

대문자 값을 적절히 대체하여, 다음 커맨드를 실행한다.

```shell
kubectl create secret docker-registry <name> --docker-server=DOCKER_REGISTRY_SERVER --docker-username=DOCKER_USER --docker-password=DOCKER_PASSWORD --docker-email=DOCKER_EMAIL
```

만약 도커 자격 증명 파일이 이미 존재한다면, 위의 명령을 사용하지 않고,
자격 증명 파일을 쿠버네티스 {{< glossary_tooltip text="시크릿" term_id="secret" >}}으로
가져올 수 있다.
[기존 도커 자격 증명으로 시크릿 생성](/ko/docs/tasks/configure-pod-container/pull-image-private-registry/#registry-secret-existing-credentials)에서 관련 방법을 설명하고 있다.

`kubectl create secret docker-registry`는
하나의 프라이빗 레지스트리에서만 작동하는 시크릿을 생성하기 때문에,
여러 프라이빗 컨테이너 레지스트리를 사용하는 경우 특히 유용하다.

{{< note >}}
파드는 이미지 풀 시크릿을 자신의 네임스페이스에서만 참조할 수 있다.
따라서 이 과정은 네임스페이스 당 한 번만 수행될 필요가 있다.
{{< /note >}}

#### 파드의 imagePullSecrets 참조

이제, `imagePullSecrets` 섹션을 파드의 정의에 추가함으로써 해당 시크릿을
참조하는 파드를 생성할 수 있다.

예를 들면 다음과 같다.

```shell
cat <<EOF > pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: foo
  namespace: awesomeapps
spec:
  containers:
    - name: foo
      image: janedoe/awesomeapp:v1
  imagePullSecrets:
    - name: myregistrykey
EOF

cat <<EOF >> ./kustomization.yaml
resources:
- pod.yaml
EOF
```

이것은 프라이빗 레지스트리를 사용하는 각 파드에 대해서 수행될 필요가 있다.

그러나, 이 필드의 셋팅은 [서비스 어카운트](/docs/tasks/configure-pod-container/configure-service-account/) 리소스에
imagePullSecrets을 셋팅하여 자동화할 수 있다.

자세한 지침을 위해서는 [서비스 어카운트에 ImagePullSecrets 추가](/docs/tasks/configure-pod-container/configure-service-account/#add-imagepullsecrets-to-a-service-account)를 확인한다.

이것은 노드 당 `.docker/config.json`와 함께 사용할 수 있다. 자격 증명은
병합될 것이다.

## 유스케이스

프라이빗 레지스트리를 구성하기 위한 많은 솔루션이 있다. 다음은 여러 가지
일반적인 유스케이스와 제안된 솔루션이다.

1. 비소유 이미지(예를 들어, 오픈소스)만 실행하는 클러스터의 경우. 이미지를 숨길 필요가 없다.
   - 도커 허브의 퍼블릭 이미지를 사용한다.
     - 설정이 필요 없다.
     - 일부 클라우드 제공자는 퍼블릭 이미지를 자동으로 캐시하거나 미러링하므로, 가용성이 향상되고 이미지를 가져오는 시간이 줄어든다.
1. 모든 클러스터 사용자에게는 보이지만, 회사 외부에는 숨겨야하는 일부 독점 이미지를
   실행하는 클러스터의 경우.
   - 호스트 된 프라이빗 [도커 레지스트리](https://docs.docker.com/registry/)를 사용한다.
     - 그것은 [도커 허브](https://hub.docker.com/signup)에 호스트 되어 있거나, 다른 곳에 되어 있을 것이다.
     - 위에 설명된 바와 같이 수동으로 .docker/config.json을 구성한다.
   - 또는, 방화벽 뒤에서 읽기 접근 권한을 가진 내부 프라이빗 레지스트리를 실행한다.
     - 쿠버네티스 구성은 필요 없다.
   - 이미지 접근을 제어하는 ​​호스팅된 컨테이너 이미지 레지스트리 서비스를 사용한다.
     - 그것은 수동 노드 구성에 비해서 클러스터 오토스케일링과 더 잘 동작할 것이다.
   - 또는, 노드의 구성 변경이 불편한 클러스터에서는, `imagePullSecrets`를 사용한다.
1. 독점 이미지를 가진 클러스터로, 그 중 일부가 더 엄격한 접근 제어를 필요로 하는 경우.
   - [AlwaysPullImages 어드미션 컨트롤러](/docs/reference/access-authn-authz/admission-controllers/#alwayspullimages)가 활성화되어 있는지 확인한다. 그렇지 않으면, 모든 파드가 잠재적으로 모든 이미지에 접근 권한을 가진다.
   - 민감한 데이터는 이미지 안에 포장하는 대신, "시크릿" 리소스로 이동한다.
1. 멀티-테넌트 클러스터에서 각 테넌트가 자신의 프라이빗 레지스트리를 필요로 하는 경우.
   - [AlwaysPullImages 어드미션 컨트롤러](/docs/reference/access-authn-authz/admission-controllers/#alwayspullimages)가 활성화되어 있는지 확인한다. 그렇지 않으면, 모든 파드가 잠재적으로 모든 이미지에 접근 권한을 가진다.
   - 인가가 요구되도록 프라이빗 레지스트리를 실행한다.
   - 각 테넌트에 대한 레지스트리 자격 증명을 생성하고, 시크릿에 넣고, 각 테넌트 네임스페이스에 시크릿을 채운다.
   - 테넌트는 해당 시크릿을 각 네임스페이스의 imagePullSecrets에 추가한다.


다중 레지스트리에 접근해야 하는 경우, 각 레지스트리에 대해 하나의 시크릿을 생성할 수 있다.
Kubelet은 모든 `imagePullSecrets` 파일을 하나의 가상 `.docker/config.json` 파일로 병합한다.

## {{% heading "whatsnext" %}}

* [OCI 이미지 매니페스트 명세](https://github.com/opencontainers/image-spec/blob/master/manifest.md) 읽어보기
