---
title: 프라이빗 레지스트리에서 이미지 받아오기
content_type: task
weight: 100
---

<!-- overview -->

이 페이지는 프라이빗 도커 레지스트리나 리포지터리로부터 이미지를 받아오기 위해 시크릿(Secret)을 
사용하는 파드를 생성하는 방법을 보여준다.

## {{% heading "prerequisites" %}}

* {{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}

* 이 실습을 수행하기 위해, 
[도커 ID](https://docs.docker.com/docker-id/)와 비밀번호가 필요하다.

<!-- steps -->

## 도커 로그인

노트북에 프라이빗 이미지를 받아오기 위하여 레지스트리 인증을 필수로 수행해야 한다.

```shell
docker login
```

프롬프트가 나타나면, 도커 사용자 이름(username)과 비밀번호(password)를 입력하자.

로그인 프로세스는 권한 토큰 정보를 가지고 있는 `config.json` 파일을 생성하거나 업데이트 한다.

`config.json` 파일을 확인하자.

```shell
cat ~/.docker/config.json
```

하단과 유사한 결과를 확인할 수 있다.

```json
{
    "auths": {
        "https://index.docker.io/v1/": {
            "auth": "c3R...zE2"
        }
    }
}
```

{{< note >}}
도커 자격 증명 저장소를 사용하는 경우, `auth` 항목이 아닌, 저장소의 이름을 값으로 사용하는 `credsStore` 항목을 확인할 수 있다.
{{< /note >}}

## 기존의 도커 자격 증명을 기반으로 시크릿 생성하기 {#registry-secret-existing-credentials}

쿠버네티스 클러스터는 프라이빗 이미지를 받아올 때, 컨테이너 레지스트리에 인증하기 위하여 
`kubernetes.io/dockerconfigjson` 타입의 시크릿을 사용한다.

만약 이미 `docker login` 을 수행하였다면, 이 때 생성된 자격 증명을 쿠버네티스 클러스터로 복사할 수 있다.

```shell
kubectl create secret generic regcred \
    --from-file=.dockerconfigjson=<path/to/.docker/config.json> \
    --type=kubernetes.io/dockerconfigjson
```

오브젝트에 대한 더 세밀한 제어(새로운 시크릿에 대한 네임스페이스나 레이블을 지정하는 등)가 필요할 경우, 
시크릿을 사용자 정의한 후에 저장할 수도 있다.
다음을 확인하자.

- 데이터 항목의 이름을 `.dockerconfigjson` 으로 설정한다
- 도커 파일을 base64로 인코딩하고 그 문자열을 `data[".dockerconfigjson"]` 
  필드에 자르지 않고 한 줄로 이어서 붙여넣는다
- `type` 을 `kubernetes.io/dockerconfigjson` 으로 설정한다

예: 

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: myregistrykey
  namespace: awesomeapps
data:
  .dockerconfigjson: UmVhbGx5IHJlYWxseSByZWVlZWVlZWVlZWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWxsbGxsbGxsbGxsbGxsbGxsbGxsbGxsbGxsbGxsbGx5eXl5eXl5eXl5eXl5eXl5eXl5eSBsbGxsbGxsbGxsbGxsbG9vb29vb29vb29vb29vb29vb29vb29vb29vb25ubm5ubm5ubm5ubm5ubm5ubm5ubm5ubmdnZ2dnZ2dnZ2dnZ2dnZ2dnZ2cgYXV0aCBrZXlzCg==
type: kubernetes.io/dockerconfigjson
```

만약 `error: no objects passed to create` 메세지가 출력될 경우, base64로 인코딩된 문자열이 유효하지 않음을 의미한다.
또한 `Secret "myregistrykey" is invalid: data[.dockerconfigjson]: invalid value ...` 메세지가 출력될 경우,
base64로 인코딩된 문자열이 정상적으로 디코딩되었으나, `.docker/config.json` 파일로 파싱되지 못한 것을 의미한다.

## 커맨드 라인에서 자격 증명을 통하여 시크릿 생성하기 

`regcred` 라는 이름의 시크릿을 생성하자.

```shell
kubectl create secret docker-registry regcred --docker-server=<your-registry-server> --docker-username=<your-name> --docker-password=<your-pword> --docker-email=<your-email>
```

아래의 각 항목에 대한 설명을 참고한다.

* `<your-registry-server>` 은 프라이빗 도커 저장소의 FQDN 주소이다.
  도커허브(DockerHub)는 `https://index.docker.io/v2/` 를 사용한다.
* `<your-name>` 은 도커 사용자의 계정이다.
* `<your-pword>` 은 도커 사용자의 비밀번호이다.
* `<your-email>` 은 도커 사용자의 이메일 주소이다.

이를 통해 `regcred` 라는 시크릿으로 클러스터 내에서 도커 자격 증명을 생성했다.

{{< note >}}
커맨드 라인에서 시크릿을 입력하는 경우, 보호되지 않는 셸 히스토리에 내용이 저장될 수 있으며, 
이러한 시크릿들은 `kubectl` 이 구동 중인 동안 사용자의 PC의 다른 사용자들에게 
보일 수도 있다.
{{< /note >}}


## 시크릿 `regcred` 검증하기

방금 생성한 `regcred` 시크릿의 내용을 확인하기 위하여, YAML 형식으로 시크릿을 확인하자.

```shell
kubectl get secret regcred --output=yaml
```

결과는 다음과 같다.

```yaml
apiVersion: v1
kind: Secret
metadata:
  ...
  name: regcred
  ...
data:
  .dockerconfigjson: eyJodHRwczovL2luZGV4L ... J0QUl6RTIifX0=
type: kubernetes.io/dockerconfigjson
```

`.dockerconfigjson` 필드의 값은 도커 자격 증명의 base64 인코딩 결과이다.

`.dockerconfigjson`  필드의 값을 확인하기 위하여, 시크릿 데이터를 읽을 수 있는 
형식으로 변경한다.

```shell
kubectl get secret regcred --output="jsonpath={.data.\.dockerconfigjson}" | base64 --decode
```

결과는 다음과 같다.

```json
{"auths":{"your.private.registry.example.com":{"username":"janedoe","password":"xxxxxxxxxxx","email":"jdoe@example.com","auth":"c3R...zE2"}}}
```

`auth` 필드의 값을 확인하기 위하여, base64로 인코딩된 데이터를 읽을 수 있는 형식으로 변경한다.

```shell
echo "c3R...zE2" | base64 --decode
```

결과로, 사용자 이름과 비밀번호가 `:` 로 연결되어 아래와 같이 표현된다.

```none
janedoe:xxxxxxxxxxx
```

참고로 시크릿 데이터에는 사용자의 로컬에 있는 `~/.docker/config.json` 파일과 유사한 인증 토큰이 포함되어 있다.

이를 통해 `regcred` 라는 시크릿으로 클러스터 내에서 도커 자격 증명을 생성했다.

## 시크릿을 사용하는 파드 생성하기

다음은 `regcred` 에 있는 도커 자격 증명에 접근해야 하는 파드의 구성 파일이다.

{{< codenew file="pods/private-reg-pod.yaml" >}}

아래의 파일을 다운로드받는다.

```shell
wget -O my-private-reg-pod.yaml https://k8s.io/examples/pods/private-reg-pod.yaml
```

`my-private-reg-pod.yaml` 파일 안에서, `<your-private-image>` 값을 다음과 같은 프라이빗 저장소 안의 이미지 경로로 변경한다.

```none
your.private.registry.example.com/janedoe/jdoe-private:v1
```

프라이빗 저장소에서 이미지를 받아오기 위하여, 쿠버네티스에서 자격 증명이 필요하다.
구성 파일의 `imagePullSecrets` 필드를 통해 쿠버네티스가
`regcred` 라는 시크릿으로부터 자격 증명을 가져올 수 있다.

시크릿을 사용해서 파드를 생성하고, 파드가 실행되는지 확인하자.

```shell
kubectl apply -f my-private-reg-pod.yaml
kubectl get pod private-reg
```

## {{% heading "whatsnext" %}}

* [시크릿](/ko/docs/concepts/configuration/secret/)에 대해 더 배워 보기.
* [프라이빗 레지스트리 사용](/ko/docs/concepts/containers/images/#프라이빗-레지스트리-사용)에 대해 더 배워 보기.
* [서비스 어카운트에 풀 시크릿(pull secret) 추가하기](/docs/tasks/configure-pod-container/configure-service-account/#add-imagepullsecrets-to-a-service-account)에 대해 더 배워 보기.
* [kubectl create secret docker-registry](/docs/reference/generated/kubectl/kubectl-commands/#-em-secret-docker-registry-em-)에 대해 읽어보기.
* [시크릿](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#secret-v1-core)에 대해 읽어보기.
* [PodSpec](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#podspec-v1-core)의 `imagePullSecrets` 필드에 대해 읽어보기.
