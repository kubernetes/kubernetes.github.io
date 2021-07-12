---


title: 시크릿(Secret)
content_type: concept
feature:
  title: 시크릿과 구성 관리
  description: >
    사용자의 이미지를 다시 빌드하거나 스택 구성의 시크릿을 노출하지 않고 시크릿과 애플리케이션 구성을 배포하고 업데이트한다.
weight: 30
---

<!-- overview -->

쿠버네티스 시크릿을 사용하면 비밀번호, OAuth 토큰, ssh 키와 같은
민감한 정보를 저장하고 관리할 수 ​​있다. 기밀 정보를 시크릿에 저장하는 것이
{{< glossary_tooltip term_id="pod" >}} 정의나
{{< glossary_tooltip text="컨테이너 이미지" term_id="image" >}}
내에 그대로 두는 것보다 안전하고 유연하다.
자세한 내용은 [시크릿 디자인 문서](https://git.k8s.io/community/contributors/design-proposals/auth/secrets.md)를 참고한다.

시크릿은 암호, 토큰 또는 키와 같은 소량의 중요한 데이터를
포함하는 오브젝트이다. 그렇지 않으면  이러한 정보가 파드
명세나 이미지에 포함될 수 있다. 사용자는 시크릿을 만들 수 있고 시스템도
일부 시크릿을 만들 수 있다.

{{< caution >}}
쿠버네티스 시크릿은 기본적으로 암호화되지 않은 base64 인코딩 문자열로 저장된다.
기본적으로 API 액세스 권한이 있는 모든 사용자 또는 쿠버네티스의 기본 데이터 저장소 etcd에
액세스할 수 있는 모든 사용자가 일반 텍스트로 검색할 수 있다.
시크릿을 안전하게 사용하려면 (최소한) 다음과 같이 하는 것이 좋다.

1. 시크릿에 대한 [암호화 활성화](/docs/tasks/administer-cluster/encrypt-data/).
2. 시크릿 읽기 및 쓰기를 제한하는 [RBAC 규칙 활성화 또는 구성](/ko/docs/reference/access-authn-authz/authorization/). 파드를 만들 권한이 있는 모든 사용자는 시크릿을 암묵적으로 얻을 수 있다.
{{< /caution >}}

<!-- body -->

## 시크릿 개요

시크릿을 사용하려면, 파드가 시크릿을 참조해야 한다.
시크릿은 세 가지 방법으로 파드와 함께 사용할 수 있다.

- 하나 이상의 컨테이너에 마운트된
  {{< glossary_tooltip text="볼륨" term_id="volume" >}} 내의
  [파일](#시크릿을-파드의-파일로-사용하기)로써 사용.
- [컨테이너 환경 변수](#시크릿을-환경-변수로-사용하기)로써 사용.
- 파드의 [이미지를 가져올 때 kubelet](#imagepullsecrets-사용하기)에 의해 사용.

시크릿 오브젝트의 이름은 유효한
[DNS 서브도메인 이름](/ko/docs/concepts/overview/working-with-objects/names/#dns-서브도메인-이름)이어야 한다.
사용자는 시크릿을 위한 파일을 구성할 때 `data` 및 (또는) `stringData` 필드를
명시할 수 있다. 해당 `data` 와 `stringData` 필드는 선택적으로 명시할 수 있다.
`data` 필드의 모든 키(key)에 해당하는 값(value)은 base64로 인코딩된 문자열이어야 한다.
만약 사용자에게 base64로의 문자열 변환이 적합하지 않다면,
임의의 문자열을 값으로 받는 `stringData` 필드를 대신 사용할 수 있다.

`data` 및 `stringData`의 키는 영숫자 문자,
`-`, `_`, 또는 `.` 으로 구성되어야 한다. `stringData` 필드의 모든 키-값 쌍은 의도적으로
`data` 필드로 합쳐진다. 만약 키가 `data` 와 `stringData` 필드 모두에 정의되어
있으면, `stringData` 필드에 지정된 값이
우선적으로 사용된다.

## 시크릿 타입 {#secret-types}

시크릿을 생성할 때, [`Secret`](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#secret-v1-core)
리소스의 `type` 필드를 사용하거나, (활용 가능하다면) `kubectl` 의
유사한 특정 커맨드라인 플래그를 사용하여 시크릿의 타입을 명시할 수 있다.
시크릿 타입은 시크릿 데이터의 프로그래믹 처리를 촉진시키기 위해 사용된다.

쿠버네티스는 일반적인 사용 시나리오를 위해 몇 가지 빌트인 타입을 제공한다.
이 타입은 쿠버네티스가 부과하여 수행되는 검증 및 제약에
따라 달라진다.

| 빌트인 타입 | 사용처 |
|--------------|-------|
| `Opaque`     |  임의의 사용자 정의 데이터 |
| `kubernetes.io/service-account-token` | 서비스 어카운트 토큰 |
| `kubernetes.io/dockercfg` | 직렬화 된(serialized) `~/.dockercfg` 파일 |
| `kubernetes.io/dockerconfigjson` | 직렬화 된 `~/.docker/config.json` 파일 |
| `kubernetes.io/basic-auth` | 기본 인증을 위한 자격 증명(credential) |
| `kubernetes.io/ssh-auth` | SSH를 위한 자격 증명 |
| `kubernetes.io/tls` | TLS 클라이언트나 서버를 위한 데이터 |
| `bootstrap.kubernetes.io/token` | 부트스트랩 토큰 데이터 |

사용자는 시크릿 오브젝트의 `type` 값에 비어 있지 않은 문자열을 할당하여 자신만의 시크릿
타입을 정의하고 사용할 수 있다. 비어 있는 문자열은 `Opaque` 타입으로 인식된다.
쿠버네티스는 타입 명칭에 제약을 부과하지는 않는다. 그러나 만약
빌트인 타입 중 하나를 사용한다면, 해당 타입에 정의된 모든 요구 사항을
만족시켜야 한다.

### 불투명(Opaque) 시크릿

`Opaque` 은 시크릿 구성 파일에서 누락된 경우의 기본 시크릿 타입이다.
`kubectl` 을 사용하여 시크릿을 생성할 때 `Opaque` 시크릿 타입을 나타내기
위해서는 `generic` 하위 커맨드를 사용할 것이다. 예를 들어, 다음 커맨드는
타입 `Opaque` 의 비어 있는 시크릿을 생성한다.

```shell
kubectl create secret generic empty-secret
kubectl get secret empty-secret
```

출력은 다음과 같다.

```
NAME           TYPE     DATA   AGE
empty-secret   Opaque   0      2m6s
```

해당 `DATA` 열은 시크릿에 저장된 데이터 아이템의 수를 보여준다.
이 경우, `0` 은 비어 있는 시크릿을 하나 생성하였다는 것을 의미한다.

###  서비스 어카운트 토큰 시크릿

`kubernetes.io/service-account-token` 시크릿 타입은 서비스 어카운트를 확인하는 토큰을 저장하기 위해서 사용한다. 이 시크릿 타입을 사용할 때는,
`kubernetes.io/service-account.name` 어노테이션이 존재하는 서비스
어카운트 이름으로 설정되도록 해야 한다. 쿠버네티스 컨트롤러는
`kubernetes.io/service-account.uid` 및 실제 토큰
콘텐츠로 설정된 `data` 필드의 `token` 키와 같은,
몇 가지 다른 필드들을 채운다.

다음은 서비스 어카운트 토큰 시크릿의 구성 예시이다.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: secret-sa-sample
  annotations:
    kubernetes.io/service-account.name: "sa-name"
type: kubernetes.io/service-account-token
data:
  # 사용자는 불투명 시크릿을 사용하므로 추가적인 키 값 쌍을 포함할 수 있다.
  extra: YmFyCg==
```

`Pod` 를 생성할 때, 쿠버네티스는 자동으로 서비스 어카운트 시크릿을
생성하고 자동으로 파드가 해당 시크릿을 사용하도록 수정한다. 해당 서비스
어카운트 토큰 시크릿은 API 접속을 위한 자격 증명을 포함한다.

이러한 API 자격 증명의 자동 생성과 사용은 원하는 경우 해제하거나
기각할 수 있다. 그러나 만약 사용자가 API 서버에 안전하게 접근하는 것만
필요하다면, 이것이 권장되는 워크플로우이다.

[서비스 어카운트](/docs/tasks/configure-pod-container/configure-service-account/) 문서를 보면
서비스 어카운트가 동작하는 방법에 대한 더 자세한 정보를 얻을 수 있다.
또한 파드에서 서비스 어카운트를 참조하는 방법을
[`Pod`](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#pod-v1-core)의
`automountServiceAccountToken` 필드와 `serviceAccountName`
필드를 통해 확인할 수 있다.

### 도커 컨피그 시크릿

이미지에 대한 도커 레지스트리 접속 자격 증명을 저장하기 위한
시크릿을 생성하기 위해서 다음의 `type` 값 중 하나를 사용할 수 있다.

- `kubernetes.io/dockercfg`
- `kubernetes.io/dockerconfigjson`

`kubernetes.io/dockercfg` 는 직렬화 된 도커 커맨드라인 구성을
위한 기존(legacy) 포맷 `~/.dockercfg` 를 저장하기 위해 할당된 타입이다.
시크릿 타입을 사용할 때는, `data` 필드가 base64 포맷으로
인코딩된 `~/.dockercfg` 파일의 콘텐츠를 값으로 가지는 `.dockercfg` 키를 포함하고 있는지
확실히 확인해야 한다.

`kubernetes.io/dockerconfigjson` 타입은 `~/.dockercfg` 의
새로운 포맷인 `~/.docker/config.json` 파일과 동일한 포맷 법칙을
따르는 직렬화 된 JSON의 저장을 위해 디자인되었다.
이 시크릿 타입을 사용할 때는, 시크릿 오브젝트의 `data` 필드가 `.dockerconfigjson` 키를
꼭 포함해야 한다. `~/.docker/config.json` 파일을 위한 콘텐츠는
base64로 인코딩된 문자열으로 제공되어야 한다.

아래는 시크릿의 `kubernetes.io/dockercfg` 타입 예시이다.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: secret-dockercfg
type: kubernetes.io/dockercfg
data:
  .dockercfg: |
    "<base64 encoded ~/.dockercfg file>"
```

{{< note >}}
만약 base64 인코딩 수행을 원하지 않는다면, 그 대신 `stringData` 필드의
사용을 선택할 수 있다.
{{< /note >}}

이러한 타입들을 매니페스트를 사용하여 생성하는 경우, API
서버는 해당 `data` 필드에 기대하는 키가 존재하는지 확인하고,
제공된 값이 유효한 JSON으로 파싱될 수 있는지 검증한다. API
서버가 해당 JSON이 실제 도커 컨피그 파일인지를 검증하지는 않는다.

도커 컨피그 파일을 가지고 있지 않거나 도커 레지스트리 시크릿을 생성하기
위해 `kubectl` 을 사용하고 싶은 경우, 다음과 같이 처리할 수 있다.

```shell
kubectl create secret docker-registry secret-tiger-docker \
  --docker-username=tiger \
  --docker-password=pass113 \
  --docker-email=tiger@acme.com
```

이 커맨드는 `kubernetes.io/dockerconfigjson` 타입의 시크릿을 생성한다.
만약 `data` 필드로부터 `.dockerconfigjson` 콘텐츠를 복사(dump)해오면,
다음과 같이 유효한 도커 JSON 콘텐츠를
즉석에서 얻게 될 것이다.

```json
{
  "auths": {
    "https://index.docker.io/v1/": {
      "username": "tiger",
      "password": "pass113",
      "email": "tiger@acme.com",
      "auth": "dGlnZXI6cGFzczExMw=="
    }
  }
}
```

### 기본 인증 시크릿

`kubernetes.io/basic-auth` 타입은 기본 인증을 위한 자격 증명을 저장하기
위해 제공된다. 이 시크릿 타입을 사용할 때는 시크릿의 `data` 필드가
다음의 두 키를 포함해야 한다.

- `username`: 인증을 위한 사용자 이름
- `password`: 인증을 위한 암호나 토큰

위의 두 키에 대한 두 값은 모두 base64로 인코딩된 문자열이다. 물론,
시크릿 생성 시 `stringData` 를 사용하여 평문 텍스트 콘텐츠(clear text content)를 제공할
수도 있다.

다음의 YAML은 기본 인증 시크릿을 위한 구성 예시이다.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: secret-basic-auth
type: kubernetes.io/basic-auth
stringData:
  username: admin
  password: t0p-Secret
```

이 기본 인증 시크릿 타입은 사용자 편의만을 위해서 제공된다.
사용자는 기본 인증에서 사용되는 자격 증명을 위한 `Opaque` 를 생성할 수도 있다.
그러나, 빌트인 시크릿 타입을 사용하는 것은 사용자의 자격 증명들의 포맷을 통합하는 데 도움이 되고,
API 서버는 요구되는 키가 시크릿 구성에서 제공되고 있는지
검증도 한다.

### SSH 인증 시크릿

이 빌트인 타입 `kubernetes.io/ssh-auth` 는 SSH 인증에 사용되는 데이터를
저장하기 위해서 제공된다. 이 시크릿 타입을 사용할 때는 `ssh-privatekey`
키-값 쌍을 사용할 SSH 자격 증명으로 `data` (또는 `stringData`)
필드에 명시해야 할 것이다.

다음 YAML은 SSH 인증 시크릿의 구성 예시이다.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: secret-ssh-auth
type: kubernetes.io/ssh-auth
data:
  # 본 예시를 위해 축약된 데이터임
  ssh-privatekey: |
     MIIEpQIBAAKCAQEAulqb/Y ...
```

SSH 인증 시크릿 타입은 사용자 편의만을 위해서 제공된다.
사용자는 SSH 인증에서 사용되는 자격 증명을 위한 `Opaque` 를 생성할 수도 있다.
그러나, 빌트인 시크릿 타입을 사용하는 것은 사용자의 자격 증명들의 포맷을 통합하는 데 도움이 되고,
API 서버는 요구되는 키가 시크릿 구성에서 제공되고 있는지
검증도 한다.

{{< caution >}}
SSH 개인 키는 자체적으로 SSH 클라이언트와 호스트 서버 간에 신뢰할 수 있는 통신을
설정하지 않는다. 컨피그맵(ConfigMap)에 추가된 `known_hosts` 파일과 같은
"중간자(man in the middle)" 공격을 완화하려면 신뢰를 설정하는
2차 수단이 필요하다.
{{< /caution >}}

### TLS 시크릿

쿠버네티스는 보통 TLS를 위해 사용되는 인증서와 관련된 키를 저장하기 위해서
빌트인 시크릿 타입 `kubernetes.io/tls` 를 제공한다.
이 데이터는 인그레스 리소스의 TLS 종료에 주로 사용되지만, 다른
리소스나 워크로드에 의해 직접적으로 사용될 수도 있다.
이 타입의 시크릿을 사용할 때는 `tls.key` 와 `tls.crt` 키가 시크릿 구성의
`data` (또는 `stringData`) 필드에서 제공되어야 한다. 그러나, API
서버가 각 키에 대한 값이 유효한지 실제로 검증하지는 않는다.

다음 YAML은 TLS 시크릿을 위한 구성 예시를 포함한다.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: secret-tls
type: kubernetes.io/tls
data:
  # 본 예시를 위해 축약된 데이터임
  tls.crt: |
    MIIC2DCCAcCgAwIBAgIBATANBgkqh ...
  tls.key: |
    MIIEpgIBAAKCAQEA7yn3bRHQ5FHMQ ...
```

TLS 시크릿 타입은 사용자 편의만을 위해서 제공된다. 사용자는 TLS 서버 및/또는
클라이언트를 위해 사용되는 자격 증명을 위한 `Opaque` 를 생성할 수도 있다. 그러나, 빌트인
시크릿 타입을 사용하는 것은 사용자의 자격 증명들의 포맷을 통합하는 데 도움이 되고,
API 서버는 요구되는 키가 시크릿 구성에서 제공되고 있는지 검증도 한다.

`kubectl` 를 사용하여 TLS 시크릿을 생성할 때, `tls` 하위 커맨드를
다음 예시와 같이 사용할 수 있다.

```shell
kubectl create secret tls my-tls-secret \
  --cert=path/to/cert/file \
  --key=path/to/key/file
```

공개/개인 키 쌍은 사전에 존재해야 한다. `--cert` 를 위한 공개 키 인증서는
.PEM 으로 인코딩(Base64로 인코딩된 DER 포맷)되어야 하며, `--key` 를 위해 주어진
개인 키에 맞아야 한다.
개인 키는 일반적으로 PEM 개인 키 포맷이라고 하는,
암호화되지 않은 형태(unencrypted)이어야 한다. 두 가지 방식 모두에 대해서, PEM의
시작과 끝 라인(예를 들면, 인증서의 `--------BEGIN CERTIFICATE-----` 및 `-------END CERTIFICATE----`)
은 포함되면 *안* 된다.

### 부트스트랩 토큰 시크릿

부트스트랩 토큰 시크릿은 시크릿 `type` 을 `bootstrap.kubernetes.io/token` 으로
명확하게 지정하면 생성할 수 있다. 이 타입의 시크릿은 노드 부트스트랩 과정 중에 사용되는
토큰을 위해 디자인되었다. 이것은 잘 알려진 컨피그맵에 서명하는 데 사용되는
토큰을 저장한다.

부트스트랩 토큰 시크릿은 보통 `kube-system` 네임스페이스에 생성되며
`<token-id>` 가 해당 토큰 ID의 6개 문자의 문자열으로 구성된 `bootstrap-token-<token-id>` 형태로
이름이 지정된다.

쿠버네티스 매니페스트로서, 부트스트렙 토큰 시크릿은 다음과 유사할
것이다.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: bootstrap-token-5emitj
  namespace: kube-system
type: bootstrap.kubernetes.io/token
data:
  auth-extra-groups: c3lzdGVtOmJvb3RzdHJhcHBlcnM6a3ViZWFkbTpkZWZhdWx0LW5vZGUtdG9rZW4=
  expiration: MjAyMC0wOS0xM1QwNDozOToxMFo=
  token-id: NWVtaXRq
  token-secret: a3E0Z2lodnN6emduMXAwcg==
  usage-bootstrap-authentication: dHJ1ZQ==
  usage-bootstrap-signing: dHJ1ZQ==
```

부트스트랩 타입 시크릿은 `data` 아래 명시된 다음의 키들을 가진다.

- `token-id`: 토큰 식별자로 임의의 6개 문자의 문자열. 필수 사항.
- `token-secret`: 실제 토큰 시크릿으로 임의의 16개 문자의 문자열. 필수 사항.
- `description`: 토큰의 사용처를 설명하는 사람이 읽을 수 있는
  문자열. 선택 사항.
- `expiration`: 토큰이 만료되어야 하는 시기를 명시한 RFC3339를
  사용하는 절대 UTC 시간. 선택 사항.
- `usage-bootstrap-<usage>`: 부트스트랩 토큰의 추가적인 사용처를 나타내는
  불리언(boolean) 플래그.
- `auth-extra-groups`: `system:bootstrappers` 그룹에 추가로 인증될
  쉼표로 구분된 그룹 이름 목록.

위의 YAML은 모두 base64로 인코딩된 문자열 값이므로 혼란스러워 보일
수 있다. 사실은 다음 YAML을 사용하여 동일한 시크릿을 생성할 수 있다.

```yaml
apiVersion: v1
kind: Secret
metadata:
  # 시크릿 이름이 어떻게 지정되었는지 확인
  name: bootstrap-token-5emitj
  # 부트스트랩 토큰 시크릿은 일반적으로 kube-system 네임스페이스에 포함
  namespace: kube-system
type: bootstrap.kubernetes.io/token
stringData:
  auth-extra-groups: "system:bootstrappers:kubeadm:default-node-token"
  expiration: "2020-09-13T04:39:10Z"
  # 이 토큰 ID는 이름에 사용됨
  token-id: "5emitj"
  token-secret: "kq4gihvszzgn1p0r"
  # 이 토큰은 인증을 위해서 사용될 수 있음
  usage-bootstrap-authentication: "true"
  # 또한 서명(signing)에도 사용될 수 있음
  usage-bootstrap-signing: "true"
```

## 시크릿 생성하기

시크릿을 생성하기 위한 몇 가지 옵션이 있다.

- [`kubectl` 명령을 사용하여 시크릿 생성하기](/docs/tasks/configmap-secret/managing-secret-using-kubectl/)
- [구성 파일로 시크릿 생성하기](/docs/tasks/configmap-secret/managing-secret-using-config-file/)
- [kustomize를 사용하여 시크릿 생성하기](/docs/tasks/configmap-secret/managing-secret-using-kustomize/)

## 시크릿 편집하기

기존 시크릿은 다음 명령을 사용하여 편집할 수 있다.

```shell
kubectl edit secrets mysecret
```

이렇게 하면 기본으로 설정된 에디터가 열리고 `data` 필드에 base64로 인코딩된 시크릿 값을 업데이트할 수 있다.

```yaml
# 아래 오브젝트를 수정한다. '#'로 시작하는 줄은 무시되고,
# 빈 파일은 편집이 취소될 것이다. 이 파일을 저장하는 도중에 오류가 발생하면
# 관련 오류와 함께 다시 열린다.
#
apiVersion: v1
data:
  username: YWRtaW4=
  password: MWYyZDFlMmU2N2Rm
kind: Secret
metadata:
  annotations:
    kubectl.kubernetes.io/last-applied-configuration: { ... }
  creationTimestamp: 2016-01-22T18:41:56Z
  name: mysecret
  namespace: default
  resourceVersion: "164619"
  uid: cfee02d6-c137-11e5-8d73-42010af00002
type: Opaque
```

## 시크릿 사용하기

시크릿은 데이터 볼륨으로 마운트되거나 파드의 컨테이너에서 사용할
{{< glossary_tooltip text="환경 변수" term_id="container-env-variables" >}}로
노출될 수 있다. 또한, 시크릿은 파드에 직접 노출되지 않고,
시스템의 다른 부분에서도 사용할 수 있다. 예를 들어, 시크릿은
시스템의 다른 부분이 사용자를 대신해서 외부 시스템과 상호 작용하는 데 사용해야 하는
자격 증명을 보유할 수 있다.

### 시크릿을 파드의 파일로 사용하기

파드의 볼륨에서 시크릿을 사용하려면 다음과 같이 한다.

1. 시크릿을 생성하거나 기존 시크릿을 사용한다. 여러 파드가 동일한 시크릿을 참조할 수 있다.
1. `.spec.volumes[].` 아래에 볼륨을 추가하려면 파드 정의를 수정한다. 볼륨의 이름을 뭐든지 지정하고, 시크릿 오브젝트의 이름과 동일한 `.spec.volumes[].secret.secretName` 필드를 생성한다.
1. 시크릿이 필요한 각 컨테이너에 `.spec.containers[].volumeMounts[]` 를 추가한다. 시크릿을 표시하려는 사용되지 않은 디렉터리 이름에 `.spec.containers[].volumeMounts[].readOnly = true` 와 `.spec.containers[].volumeMounts[].mountPath` 를 지정한다.
1. 프로그램이 해당 디렉터리에서 파일을 찾도록 이미지 또는 커맨드 라인을 수정한다. 시크릿 `data` 맵의 각 키는 `mountPath` 아래의 파일명이 된다.

다음은 볼륨에 시크릿을 마운트하는 파드의 예시이다.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: mypod
spec:
  containers:
  - name: mypod
    image: redis
    volumeMounts:
    - name: foo
      mountPath: "/etc/foo"
      readOnly: true
  volumes:
  - name: foo
    secret:
      secretName: mysecret
```

사용하려는 각 시크릿은 `.spec.volumes` 에서 참조해야 한다.

파드에 여러 컨테이너가 있는 경우, 모든 컨테이너는
자체 `volumeMounts` 블록이 필요하지만, 시크릿에 대해서는 시크릿당 하나의 `.spec.volumes` 만 필요하다.

많은 파일을 하나의 시크릿으로 패키징하거나, 여러 시크릿을 사용할 수 있으며, 어느 쪽이든 편리한 방법을 사용하면 된다.

#### 특정 경로에 대한 시크릿 키 투영하기

시크릿 키가 투영되는 볼륨 내 경로를 제어할 수도 있다.
`.spec.volumes[].secret.items` 필드를 사용하여 각 키의 대상 경로를 변경할 수 있다.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: mypod
spec:
  containers:
  - name: mypod
    image: redis
    volumeMounts:
    - name: foo
      mountPath: "/etc/foo"
      readOnly: true
  volumes:
  - name: foo
    secret:
      secretName: mysecret
      items:
      - key: username
        path: my-group/my-username
```

다음과 같은 일들이 일어날 것이다.

* `username` 시크릿은 `/etc/foo/username` 대신 `/etc/foo/my-group/my-username` 아래의 파일에 저장된다.
* `password` 시크릿은 투영되지 않는다.

`.spec.volumes[].secret.items` 를 사용하면, `items` 에 지정된 키만 투영된다.
시크릿의 모든 키를 사용하려면, 모든 키가 `items` 필드에 나열되어야 한다.
나열된 모든 키는 해당 시크릿에 존재해야 한다. 그렇지 않으면, 볼륨이 생성되지 않는다.

#### 시크릿 파일 퍼미션

단일 시크릿 키에 대한 파일 접근 퍼미션 비트를 설정할 수 있다.
만약 사용자가 퍼미션을 지정하지 않는다면, 기본적으로 `0644` 가 사용된다.
전체 시크릿 볼륨에 대한 기본 모드를 설정하고 필요한 경우 키별로 오버라이드할 수도 있다.

예를 들어, 다음과 같은 기본 모드를 지정할 수 있다.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: mypod
spec:
  containers:
  - name: mypod
    image: redis
    volumeMounts:
    - name: foo
      mountPath: "/etc/foo"
  volumes:
  - name: foo
    secret:
      secretName: mysecret
      defaultMode: 0400
```

그러고 나면, 시크릿이 `/etc/foo` 에 마운트되고 시크릿 볼륨 마운트로 생성된
모든 파일의 퍼미션은 `0400` 이 될 것이다.

참고로 JSON 스펙은 8진수 표기법을 지원하지 않으므로, 0400 퍼미션에 대해서
값 256을 사용한다. 파드에 대해 JSON 대신 YAML을 사용하는 경우, 8진수 표기법을
사용하여 보다 자연스러운 방식으로 퍼미션을 지정할 수 있다.

참고로 파드에 `kubectl exec` 을 사용하는 경우, 예상되는 파일 모드를 찾기 위해
심볼릭 링크를 따라가야 한다. 예를 들면, 다음과 같다.

파드에서 시크릿 파일 모드를 확인한다.
```
kubectl exec mypod -it sh

cd /etc/foo
ls -l
```

출력 결과는 다음과 비슷하다.
```
total 0
lrwxrwxrwx 1 root root 15 May 18 00:18 password -> ..data/password
lrwxrwxrwx 1 root root 15 May 18 00:18 username -> ..data/username
```

올바른 파일 모드를 찾으려면 심볼릭 링크를 따라간다.

```
cd /etc/foo/..data
ls -l
```

출력 결과는 다음과 비슷하다.
```
total 8
-r-------- 1 root root 12 May 18 00:18 password
-r-------- 1 root root  5 May 18 00:18 username
```

이전 예제에서와 같이 매핑을 사용하여, 다음과 같이
다른 파일에 대해 다른 퍼미션을 지정할 수도 있다.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: mypod
spec:
  containers:
  - name: mypod
    image: redis
    volumeMounts:
    - name: foo
      mountPath: "/etc/foo"
  volumes:
  - name: foo
    secret:
      secretName: mysecret
      items:
      - key: username
        path: my-group/my-username
        mode: 0777
```

이 경우, `/etc/foo/my-group/my-username` 에 있는 파일은
결과적으로 `0777` 퍼미션 값을 갖게 된다. JSON을 사용하는 경우, JSON 제한으로 인해
10진수 표기법(`511`)으로 모드를 지정해야 한다.

참고로 이 퍼미션 값은 나중에 읽을 때 10진수 표기법으로
표시될 수 있다.

#### 볼륨에서 시크릿 값 사용하기

시크릿 볼륨을 마운트하는 컨테이너 내부에서, 시크릿 키는 파일로
나타나고 시크릿 값은 base64로 디코딩되어 이런 파일 내에 저장된다.
다음은 위의 예에서 컨테이너 내부에서 실행된 명령의 결과이다.

```shell
ls /etc/foo/
```

출력 결과는 다음과 비슷하다.

```
username
password
```

```shell
cat /etc/foo/username
```

출력 결과는 다음과 비슷하다.

```
admin
```

```shell
cat /etc/foo/password
```

출력 결과는 다음과 비슷하다.

```
1f2d1e2e67df
```

컨테이너의 프로그램은 파일에서 시크릿을 읽는 역할을
한다.

#### 마운트된 시크릿은 자동으로 업데이트됨

볼륨에서 현재 사용되는 시크릿이 업데이트되면, 투영된 키도 결국 업데이트된다.
kubelet은 마운트된 시크릿이 모든 주기적인 동기화에서 최신 상태인지 여부를 확인한다.
그러나, kubelet은 시크릿의 현재 값을 가져 오기 위해 로컬 캐시를 사용한다.
캐시의 유형은 [KubeletConfiguration 구조체](/docs/reference/config-api/kubelet-config.v1beta1/)의
`ConfigMapAndSecretChangeDetectionStrategy` 필드를 사용하여 구성할 수 있다.
시크릿은 watch(기본값), ttl 기반 또는 API 서버로 모든 요청을 직접
리디렉션하여 전파할 수 있다.
결과적으로, 시크릿이 업데이트된 순간부터 새로운 키가 파드에 투영되는
순간까지의 총 지연 시간은 kubelet 동기화 시간 + 캐시
전파 지연만큼 길 수 있다. 여기서 캐시 전파 지연은 선택한 캐시 유형에 따라
달라질 수 있다(캐시 전파 지연은 각 캐시 유형에 따라 watch 전파 지연, 캐시의 ttl, 또는 0 에 상응함).

{{< note >}}
시크릿을 [subPath](/ko/docs/concepts/storage/volumes/#subpath-사용하기)
볼륨 마운트로 사용하는 컨테이너는 시크릿 업데이트를
받지 않는다.
{{< /note >}}

### 시크릿을 환경 변수로 사용하기

파드에서 {{< glossary_tooltip text="환경 변수" term_id="container-env-variables" >}}에
시크릿을 사용하려면 다음과 같이 한다.

1. 시크릿을 생성하거나 기존 시크릿을 사용한다. 여러 파드가 동일한 시크릿을 참조할 수 있다.
1. 사용하려는 각 시크릿 키에 대한 환경 변수를 추가하려면 시크릿 키 값을 사용하려는 각 컨테이너에서 파드 정의를 수정한다. 시크릿 키를 사용하는 환경 변수는 시크릿의 이름과 키를 `env[].valueFrom.secretKeyRef` 에 채워야 한다.
1. 프로그램이 지정된 환경 변수에서 값을 찾도록 이미지 및/또는 커맨드 라인을 수정한다.

다음은 환경 변수의 시크릿을 사용하는 파드의 예시이다.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secret-env-pod
spec:
  containers:
  - name: mycontainer
    image: redis
    env:
      - name: SECRET_USERNAME
        valueFrom:
          secretKeyRef:
            name: mysecret
            key: username
      - name: SECRET_PASSWORD
        valueFrom:
          secretKeyRef:
            name: mysecret
            key: password
  restartPolicy: Never
```

#### 환경 변수에서 시크릿 값 사용하기

환경 변수에서 시크릿을 사용하는 컨테이너 내부에서, 시크릿 키는
시크릿 데이터의 base64 디코딩된 값을 포함하는 일반 환경 변수로 나타난다.
다음은 위의 예에서 컨테이너 내부에서 실행된 명령의 결과이다.

```shell
echo $SECRET_USERNAME
```

출력 결과는 다음과 비슷하다.

```
admin
```

```shell
echo $SECRET_PASSWORD
```

출력 결과는 다음과 비슷하다.

```
1f2d1e2e67df
```

#### 시크릿 업데이트 후 환경 변수가 업데이트되지 않음

컨테이너가 환경 변수에서 이미 시크릿을 사용하는 경우, 다시 시작하지 않는 한 컨테이너에서 시크릿 업데이트를 볼 수 없다.
시크릿이 변경될 때 재시작을 트리거하는 써드파티 솔루션이 있다.

## 변경할 수 없는(immutable) 시크릿 {#secret-immutable}

{{< feature-state for_k8s_version="v1.21" state="stable" >}}

쿠버네티스 기능인 _변경할 수 없는 시크릿과 컨피그맵_ 은
개별 시크릿과 컨피그맵을 변경할 수 없는 것으로 설정하는 옵션을 제공한다. 시크릿을 광범위하게 사용하는
클러스터(최소 수만 개의 고유한 시크릿이 파드에 마운트)의 경우, 데이터 변경을 방지하면
다음과 같은 이점이 있다.

- 애플리케이션 중단을 유발할 수 있는 우발적(또는 원하지 않는) 업데이트로부터 보호
- immutable로 표시된 시크릿에 대한 감시를 중단하여, kube-apiserver의 부하를
크게 줄임으로써 클러스터의 성능을 향상시킴

이 기능은 v1.19부터 기본적으로 활성화된 `ImmutableEphemeralVolumes`
[기능 게이트](/ko/docs/reference/command-line-tools-reference/feature-gates/)에
의해 제어된다. `immutable` 필드를 `true` 로 설정하여
변경할 수 없는 시크릿을 생성할 수 있다. 다음은 예시이다.
```yaml
apiVersion: v1
kind: Secret
metadata:
  ...
data:
  ...
immutable: true
```

{{< note >}}
시크릿 또는 컨피그맵을 immutable로 표시하면, 이 변경 사항을 되돌리거나
`data` 필드 내용을 변경할 수 _없다_. 시크릿을 삭제하고 다시 생성할 수만 있다.
기존 파드는 삭제된 시크릿에 대한 마운트 포인트를 유지하며, 이러한 파드를 다시 생성하는 것을
권장한다.
{{< /note >}}

### imagePullSecrets 사용하기

`imagePullSecrets` 필드는 동일한 네임스페이스의 시크릿에 대한 참조 목록이다.
`imagePullSecretsDocker` 를 사용하여 도커(또는 다른 컨테이너) 이미지 레지스트리
비밀번호가 포함된 시크릿을 kubelet에 전달할 수 있다. kubelet은 이 정보를 사용해서 파드를 대신하여 프라이빗 이미지를 가져온다.
`imagePullSecrets` 필드에 대한 자세한 정보는 [PodSpec API](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#podspec-v1-core)를 참고한다.

#### imagePullSecret 수동으로 지정하기

[컨테이너 이미지 문서](/ko/docs/concepts/containers/images/#파드에-imagepullsecrets-명시)에서 `ImagePullSecrets` 지정하는 방법을 배울 수 있다.

### imagePullSecrets가 자동으로 연결되도록 정렬하기

수동으로 `imagePullSecrets` 를 생성하고, 서비스어카운트(ServiceAccount)에서
참조할 수 있다. 해당 서비스어카운트로 생성되거나
기본적인 서비스어카운트로 생성된 모든 파드는 파드의 `imagePullSecrets`
필드를 가져오고 서비스 어카운트의 필드로 설정한다.
해당 프로세스에 대한 자세한 설명은
[서비스 어카운트에 ImagePullSecrets 추가하기](/docs/tasks/configure-pod-container/configure-service-account/#add-imagepullsecrets-to-a-service-account)를 참고한다.

## 상세 내용

### 제약 사항

시크릿 볼륨 소스는 지정된 오브젝트 참조가
실제로 시크릿 유형의 오브젝트를 가리키는지 확인하기 위해 유효성을 검사한다. 따라서, 시크릿에
의존하는 모든 파드보다 먼저 시크릿을 만들어야 한다.

시크릿 리소스는 {{< glossary_tooltip text="네임스페이스" term_id="namespace" >}}에 존재한다.
시크릿은 동일한 네임스페이스에 있는 파드에서만 참조할 수 있다.

개별 시크릿의 크기는 1MiB로 제한된다. 이는 API 서버와
kubelet 메모리를 소진시키는 매우 큰 시크릿 생성을 막기 위한 것이다.
그러나, 많은 작은 시크릿을 만들어도 메모리가 고갈될 수 있다. 시크릿으로
인한 메모리 사용에 대한 보다 포괄적인 제한은 향후 버전에 계획된 기능이다.

kubelet은 API 서버에서 시크릿을 가져오는 파드에 대한
시크릿 사용만 지원한다.
여기에는 `kubectl` 을 사용하거나, 레플리케이션 컨트롤러를 통해 간접적으로 생성된 모든
파드가 포함된다. kubelet의 `--manifest-url` 플래그, `--config` 플래그 또는
kubectl의 REST API(이 방법들은 파드를 생성하는 일반적인 방법이 아님)로
생성된 파드는 포함하지 않는다.

시크릿은 optional(선택 사항)로 표시되지 않는 한 파드에서 환경
변수로 사용되기 전에 생성되어야 한다. 존재하지 않는 시크릿을
참조하면 파드가 시작되지 않는다.

명명된 시크릿에 존재하지 않는 키에 대한 참조(`secretKeyRef` 필드)는
파드가 시작되지 않도록 한다.

잘못된 환경 변수 이름으로 간주되는 키가 있는 `envFrom` 필드로
환경 변수를 채우는 데 사용되는 시크릿은 해당 키를
건너뛴다. 이러면 해당 파드가 시작될 수 있다. 원인이 `InvalidVariableNames` 인
이벤트가 발생하며 건너뛴 유효하지 않은 키 목록이
포함된 메시지가 생성된다. 다음의 예는 2개의 유효하지 않은
키(`1badkey` 와 `2alsobad`)가 포함된 default/mysecret을 참조하는 파드를 보여준다.

```shell
kubectl get events
```

출력 결과는 다음과 비슷하다.

```
LASTSEEN   FIRSTSEEN   COUNT     NAME            KIND      SUBOBJECT                         TYPE      REASON
0s         0s          1         dapi-test-pod   Pod                                         Warning   InvalidEnvironmentVariableNames   kubelet, 127.0.0.1      Keys [1badkey, 2alsobad] from the EnvFrom secret default/mysecret were skipped since they are considered invalid environment variable names.
```

### 시크릿 및 파드 수명 상호 작용

쿠버네티스 API를 호출하여 파드가 생성될 때, 참조된 시크릿이 있는지 확인하지
않는다. 일단 파드가 스케줄되면, kubelet은 시크릿 값 가져오기를
시도한다. 시크릿이 존재하지 않거나 API 서버에 대한
일시적인 연결 부족으로 인해 시크릿을 가져올 수 없는 경우, kubelet은
주기적으로 재시도한다. kubelet은 아직 시작되지 않은 이유를 설명하는
파드에 대한 이벤트를 보고한다. 시크릿을 가져오면, kubelet은
이를 포함하는 볼륨을 생성하고 마운트한다. 모든 파드의 볼륨이
마운트될 때까지 파드의 컨테이너는 시작되지 않는다.

## 사용 사레

### 사용 사례: 컨테이너 환경 변수로 사용하기

시크릿 정의를 작성한다.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: mysecret
type: Opaque
data:
  USER_NAME: YWRtaW4=
  PASSWORD: MWYyZDFlMmU2N2Rm
```

시크릿을 생성한다.

```shell
kubectl apply -f mysecret.yaml
```

모든 시크릿 데이터를 컨테이너 환경 변수로 정의하는 데 `envFrom` 을 사용한다. 시크릿의 키는 파드의 환경 변수 이름이 된다.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secret-test-pod
spec:
  containers:
    - name: test-container
      image: k8s.gcr.io/busybox
      command: [ "/bin/sh", "-c", "env" ]
      envFrom:
      - secretRef:
          name: mysecret
  restartPolicy: Never
```

### 사용 사례: ssh 키가 있는 파드

몇 가지 ssh 키를 포함하는 시크릿을 생성한다.

```shell
kubectl create secret generic ssh-key-secret --from-file=ssh-privatekey=/path/to/.ssh/id_rsa --from-file=ssh-publickey=/path/to/.ssh/id_rsa.pub
```

출력 결과는 다음과 비슷하다.

```
secret "ssh-key-secret" created
```

ssh 키를 포함하는 `secretGenerator` 필드가 있는 `kustomization.yaml` 를 만들 수도 있다.

{{< caution >}}
사용자 자신의 ssh 키를 보내기 전에 신중하게 생각한다. 클러스터의 다른 사용자가 시크릿에 접근할 수 있다. 쿠버네티스 클러스터를 공유하는 모든 사용자가 접근할 수 있도록 하려는 서비스 어카운트를 사용하고, 사용자가 손상된 경우 이 계정을 취소할 수 있다.
{{< /caution >}}

이제 ssh 키를 가진 시크릿을 참조하고
볼륨에서 시크릿을 사용하는 파드를 만들 수 있다.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secret-test-pod
  labels:
    name: secret-test
spec:
  volumes:
  - name: secret-volume
    secret:
      secretName: ssh-key-secret
  containers:
  - name: ssh-test-container
    image: mySshImage
    volumeMounts:
    - name: secret-volume
      readOnly: true
      mountPath: "/etc/secret-volume"
```

컨테이너의 명령이 실행될 때, 다음 위치에서 키 부분을 사용할 수 있다.

```
/etc/secret-volume/ssh-publickey
/etc/secret-volume/ssh-privatekey
```

그러면 컨테이너는 ssh 연결을 맺기 위해 시크릿 데이터를 자유롭게 사용할 수 있다.

### 사용 사례: 운영 / 테스트 자격 증명이 있는 파드

이 예제에서는 운영 환경의 자격 증명이 포함된 시크릿을
사용하는 파드와 테스트 환경의 자격 증명이 있는 시크릿을 사용하는 다른 파드를
보여준다.

사용자는 `secretGenerator` 필드가 있는 `kustomization.yaml` 을 만들거나
`kubectl create secret` 을 실행할 수 있다.

```shell
kubectl create secret generic prod-db-secret --from-literal=username=produser --from-literal=password=Y4nys7f11
```

출력 결과는 다음과 비슷하다.

```
secret "prod-db-secret" created
```

테스트 환경의 자격 증명에 대한 시크릿을 만들 수도 있다.

```shell
kubectl create secret generic test-db-secret --from-literal=username=testuser --from-literal=password=iluvtests
```

출력 결과는 다음과 비슷하다.

```
secret "test-db-secret" created
```

{{< note >}}
`$`, `\`, `*`, `=` 그리고 `!` 와 같은 특수 문자는 사용자의 [셸](https://ko.wikipedia.org/wiki/셸)에 의해 해석되고 이스케이핑이 필요하다.
대부분의 셸에서 비밀번호를 이스케이프하는 가장 쉬운 방법은 작은 따옴표(`'`)로 묶는 것이다.
예를 들어, 실제 비밀번호가 `S!B\*d$zDsb=` 이면, 다음과 같은 명령을 실행해야 한다.

```shell
kubectl create secret generic dev-db-secret --from-literal=username=devuser --from-literal=password='S!B\*d$zDsb='
```

파일(`--from-file`)에서는 비밀번호의 특수 문자를 이스케이프할 필요가 없다.
{{< /note >}}

이제 파드를 생성한다.

```shell
cat <<EOF > pod.yaml
apiVersion: v1
kind: List
items:
- kind: Pod
  apiVersion: v1
  metadata:
    name: prod-db-client-pod
    labels:
      name: prod-db-client
  spec:
    volumes:
    - name: secret-volume
      secret:
        secretName: prod-db-secret
    containers:
    - name: db-client-container
      image: myClientImage
      volumeMounts:
      - name: secret-volume
        readOnly: true
        mountPath: "/etc/secret-volume"
- kind: Pod
  apiVersion: v1
  metadata:
    name: test-db-client-pod
    labels:
      name: test-db-client
  spec:
    volumes:
    - name: secret-volume
      secret:
        secretName: test-db-secret
    containers:
    - name: db-client-container
      image: myClientImage
      volumeMounts:
      - name: secret-volume
        readOnly: true
        mountPath: "/etc/secret-volume"
EOF
```

동일한 kustomization.yaml에 파드를 추가한다.

```shell
cat <<EOF >> kustomization.yaml
resources:
- pod.yaml
EOF
```

다음을 실행하여 API 서버에 이러한 모든 오브젝트를 적용한다.

```shell
kubectl apply -k .
```

두 컨테이너 모두 각 컨테이너의 환경에 대한 값을 가진 파일시스템에 다음의 파일이 존재한다.

```
/etc/secret-volume/username
/etc/secret-volume/password
```

두 파드의 사양이 한 필드에서만 어떻게 다른지 확인한다. 이를 통해
공통 파드 템플릿에서 다양한 기능을 가진 파드를 생성할 수 있다.

두 개의 서비스 어카운트를 사용하여 기본 파드 명세를 더욱 단순화할 수 있다.

1. `prod-db-secret` 을 가진 `prod-user`
1. `test-db-secret` 을 가진 `test-user`

파드 명세는 다음과 같이 단축된다.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: prod-db-client-pod
  labels:
    name: prod-db-client
spec:
  serviceAccount: prod-db-client
  containers:
  - name: db-client-container
    image: myClientImage
```

### 사용 사례: 시크릿 볼륨의 도트 파일(dotfile)

점으로 시작하는 키를 정의하여 데이터를 "숨김"으로 만들 수 있다.
이 키는 도트 파일 또는 "숨겨진" 파일을 나타낸다. 예를 들어, 다음 시크릿이 `secret-volume` 볼륨에
마운트되면 아래와 같다.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: dotfile-secret
data:
  .secret-file: dmFsdWUtMg0KDQo=
---
apiVersion: v1
kind: Pod
metadata:
  name: secret-dotfiles-pod
spec:
  volumes:
  - name: secret-volume
    secret:
      secretName: dotfile-secret
  containers:
  - name: dotfile-test-container
    image: k8s.gcr.io/busybox
    command:
    - ls
    - "-l"
    - "/etc/secret-volume"
    volumeMounts:
    - name: secret-volume
      readOnly: true
      mountPath: "/etc/secret-volume"
```

볼륨은 `.secret-file` 이라는 하나의 파일을 포함하고,
`dotfile-test-container` 는 `/etc/secret-volume/.secret-file` 경로에
이 파일을 가지게 된다.

{{< note >}}
`ls -l` 명령의 결과에서 숨겨진 점으로 시작하는 파일들은
디렉터리 내용을 나열할 때 `ls -la` 를 사용해야 이 파일들을 볼 수 있다.
{{< /note >}}

### 사용 사례: 파드의 한 컨테이너에 표시되는 시크릿

HTTP 요청을 처리하고, 복잡한 비즈니스 로직을 수행한 다음, HMAC이 있는 일부 메시지에
서명해야 하는 프로그램을 고려한다. 애플리케이션 로직이
복잡하기 때문에, 서버에서 눈에 띄지 않는 원격 파일 읽기 공격이
있을 수 있으며, 이로 인해 개인 키가 공격자에게 노출될 수 있다.

이는 두 개의 컨테이너의 두 개 프로세스로 나눌 수 있다. 사용자 상호 작용과
비즈니스 로직을 처리하지만, 개인 키를 볼 수 없는 프론트엔드 컨테이너와
개인 키를 볼 수 있고, 프론트엔드의 간단한 서명 요청(예를 들어, localhost 네트워킹을 통해)에
응답하는 서명자 컨테이너로 나눌 수 있다.

이 분할된 접근 방식을 사용하면, 공격자는 이제 애플리케이션 서버를 속여서
파일을 읽는 것보다 다소 어려운 임의적인 어떤 작업을 수행해야
한다.

<!-- TODO: explain how to do this while still using automation. -->

## 모범 사례

### 시크릿 API를 사용하는 클라이언트

시크릿 API와 상호 작용하는 애플리케이션을 배포할 때, 
[RBAC](/docs/reference/access-authn-authz/rbac/)과 같은 
[인가 정책](/ko/docs/reference/access-authn-authz/authorization/)을
사용하여 접근을 제한해야 한다.

시크릿은 종종 다양한 중요도에 걸친 값을 보유하며, 이 중 많은 부분이
쿠버네티스(예: 서비스 어카운트 토큰)와 외부 시스템으로 단계적으로
확대될 수 있다. 개별 앱이 상호 작용할 것으로 예상되는 시크릿의 힘에 대해 추론할 수 있더라도
동일한 네임스페이스 내의 다른 앱이 이러한 가정을
무효화할 수 있다.

이러한 이유로 네임스페이스 내 시크릿에 대한 `watch` 와 `list` 요청은
매우 강력한 기능이며, 시크릿을 나열하면 클라이언트가 해당 네임스페이스에
있는 모든 시크릿의 값을 검사할 수 있기 때문에 피해야 한다. 클러스터의
모든 시크릿을 감시(`watch`)하고 나열(`list`)하는 기능은 가장 특권이 있는 시스템 레벨의
컴포넌트에 대해서만 예약되어야 한다.

시크릿 API에 접근해야 하는 애플리케이션은 필요한 시크릿에 대한 `get` 요청을
수행해야 한다. 이를 통해 관리자는 앱에 필요한
[개별 인스턴스에 대한 접근을 허용 목록에 추가](/docs/reference/access-authn-authz/rbac/#referring-to-resources)하면서 모든 시크릿에 대한 접근을
제한할 수 있다.

`get` 반복을 통한 성능 향상을 위해, 클라이언트는 시크릿을
참조한 다음 리소스를 감시(`watch`)하고, 참조가 변경되면 시크릿을 다시 요청하는 리소스를
설계할 수 있다. 덧붙여, 클라이언트에게 개별 리소스를 감시(`watch`)하도록 하는 ["대량 감시" API](https://github.com/kubernetes/community/blob/master/contributors/design-proposals/api-machinery/bulk_watch.md)도
제안되었으며, 쿠버네티스의 후속 릴리스에서 사용할 수
있을 것이다.

## 보안 속성

### 보호

시크릿은 시크릿을 사용하는 파드와 독립적으로 생성될 수
있으므로, 파드 생성, 보기, 편집 워크플로 중에
시크릿이 노출될 위험이 적다. 또한 시스템은 가능한 경우
디스크에 기록하지 않는 등 시크릿에 대한 추가 예방 조치를
취할 수 있다.

해당 노드의 파드에 필요한 경우에만 시크릿이 노드로 전송된다.
kubelet은 시크릿이 디스크 저장소에 기록되지 않도록 시크릿을
`tmpfs` 에 저장한다. 일단 시크릿에 의존하는 파드가 삭제되면, kubelet은
시크릿 데이터의 로컬 복제본도 삭제한다.

동일한 노드의 여러 파드에 대한 시크릿이 있을 수 있다. 그러나
파드가 요청하는 시크릿만 해당 컨테이너 내에서 잠재적으로 볼 수 있다.
따라서, 하나의 파드는 다른 파드의 시크릿에 접근할 수 없다.

파드에는 여러 개의 컨테이너가 있을 수 있다. 그러나, 파드의 각 컨테이너는
컨테이너 내에서 볼 수 있도록 파드의 `volumeMounts` 에 있는 시크릿 볼륨을
요청해야 한다. 이것은 유용한 [파드 레벨에서의 보안
파티션](#사용-사례-파드의-한-컨테이너에-표시되는-시크릿)을 구성하는 데 사용할 수 있다.

대부분의 쿠버네티스 배포판에서, 사용자와 API 서버 간,
API 서버에서 kubelet으로의 통신은 SSL/TLS로 보호된다.
이러한 채널을 통해 전송될 때 시크릿이 보호된다.

{{< feature-state for_k8s_version="v1.13" state="beta" >}}

시크릿 데이터에 대해 [저장 시 암호화(encryption at rest)](/docs/tasks/administer-cluster/encrypt-data/)를
활성화할 수 있으며, 이를 통해 보안성에 대한 보장 없이는 시크릿이 {{< glossary_tooltip term_id="etcd" >}}에 저장되지 않도록 한다 .

### 위험

 - API 서버에서 시크릿 데이터는 {{< glossary_tooltip term_id="etcd" >}}에 저장된다.
   따라서,
   - 관리자는 클러스터 데이터에 대해 저장 시 암호화를 활성화해야 한다. (v1.13 이상 필요)
   - 관리자는 etcd에 대한 접근을 admin 사용자로 제한해야 한다.
   - 관리자는 더 이상 사용하지 않을 때 etcd에서 사용하는 디스크를 지우거나 폐기할 수 있다.
   - 클러스터에서 etcd를 실행하는 경우, 관리자는 etcd peer-to-peer 통신에 대해
     SSL/TLS를 사용해야 한다.
 - base64로 인코딩된 시크릿 데이터가 있는 매니페스트(JSON 또는 YAML)
   파일을 통해 시크릿을 구성하는 경우, 이 파일을 공유하거나 소스 리포지터리에
   체크인하면 시크릿이 손상된다. Base64 인코딩은 암호화 방법이 _아니며_
   일반 텍스트와 동일한 것으로 간주된다.
 - 실수로 기록하거나 신뢰할 수 없는 상대방에게 전송하지 않는 것과 같이,
   애플리케이션은 볼륨에서 읽은 후에 시크릿 값을 보호해야 한다.
 - 시크릿을 사용하는 파드를 생성할 수 있는 사용자는 해당 시크릿의 값도 볼 수 있다.
   API 서버 정책이 해당 사용자가 시크릿을 읽을 수 있도록 허용하지 않더라도, 사용자는
   시크릿을 노출하는 파드를 실행할 수 있다.
 - 현재, 모든 노드에 대한 루트 권한이 있는 모든 사용자는 kubelet을 가장하여
   API 서버에서 _모든_ 시크릿을 읽을 수 있다. 단일 노드에 대한 루트 취약점 공격의
   영향을 제한하기 위해, 실제로 필요한 노드에만 시크릿을 보내는 것이 앞으로 계획된
   기능이다.


## {{% heading "whatsnext" %}}

- [`kubectl` 을 사용한 시크릿 관리](/docs/tasks/configmap-secret/managing-secret-using-kubectl/)하는 방법 배우기
- [구성 파일을 사용한 시크릿 관리](/docs/tasks/configmap-secret/managing-secret-using-config-file/)하는 방법 배우기
- [kustomize를 사용한 시크릿 관리](/docs/tasks/configmap-secret/managing-secret-using-kustomize/)하는 방법 배우기
