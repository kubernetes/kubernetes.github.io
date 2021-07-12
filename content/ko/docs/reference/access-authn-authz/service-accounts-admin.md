---
title: 서비스 어카운트 관리하기
content_type: concept
weight: 50
---

<!-- overview -->

이것은 서비스 어카운트에 대한 클러스터 관리자 안내서다.
독자는 [쿠버네티스 서비스 어카운트 설정](/docs/tasks/configure-pod-container/configure-service-account/)에 익숙하다고 가정한다.

인증 및 사용자 어카운트에 대한 지원은 아직 준비 중이다.
서비스 어카운트를 더 잘 설명하기 위해, 때때로 미완성 기능이 언급될 수 있다.

<!-- body -->

## 사용자 어카운트와 서비스 어카운트 비교

쿠버네티스는 여러 가지 이유로 사용자 어카운트와 서비스 어카운트의 개념을
구분한다.

- 사용자 어카운트는 사람을 위한 것이다. 서비스 어카운트는 파드에서 실행되는 프로세스를
  위한 것이다.
- 사용자 어카운트는 전역을 대상으로 고려된다.
  클러스터의 모든 네임스페이스에 걸쳐 이름이 고유해야 한다. 서비스 어카운트는 네임스페이스에 할당된다.
- 일반적으로 클러스터의 사용자 어카운트는 기업 데이터베이스로부터 동기화될 수 있으며,
  여기서 새로운 사용자 어카운트를 생성하려면 특별한 권한이 필요하며 복잡한 비즈니스 프로세스에 연결된다.
  서비스 어카운트 생성은
  클러스터 사용자가 최소 권한 원칙에 따라 특정 작업을 위한 서비스 어카운트를 만들 수 있도록
  보다 가볍게 만들어졌다.
- 사람과 서비스 어카운트에 대한 감사 항목은 다를 수 있다.
- 복잡한 시스템의 설정들은 그 시스템의 구성요소에 대한 다양한 서비스 어카운트 정의를 포함할 수 있다.
  서비스 어카운트는 많은 제약없이 만들 수 있고 네임스페이스에 할당된 이름을 가질 수 있기 때문에
  이러한 설정은 이식성이 좋다.

## 서비스 어카운트 자동화

서비스 계정 자동화를 구현하기 위해 세 가지 개별 요소가 협력한다.

- `ServiceAccount` 어드미션 컨트롤러
- 토큰 컨트롤러
- `ServiceAccount` 컨트롤러

### 서비스어카운트(ServiceAccount) 어드미션 컨트롤러

파드 수정은 [어드미션 컨트롤러](/docs/reference/access-authn-authz/admission-controllers/)라는
플러그인을 통해 구현된다.
이것은 API 서버의 일부이다.
파드가 생성되거나 수정될 때 파드를 수정하기 위해 동기적으로 동작한다.
이 플러그인이 활성 상태(대부분의 배포에서 기본값)인 경우 파드 생성 또는 수정 시 다음 작업을 수행한다.

1. 파드에 `ServiceAccount` 가 없다면, `ServiceAccount` 를 `default` 로 설정한다.
1. 이전 단계는 파드에 참조되는 `ServiceAccount` 가 있도록 하고, 그렇지 않으면 이를 거부한다.
1. 서비스어카운트 `automountServiceAccountToken` 와 파드의 `automountServiceAccountToken` 중 어느 것도 `false` 로 설정되어 있지 않다면, API 접근을 위한 토큰이 포함된 `volume` 을 파드에 추가한다.
1. 이전 단계에서 서비스어카운트 토큰을 위한 볼륨이 만들어졌다면, `/var/run/secrets/kubernetes.io/serviceaccount` 에 마운트된 파드의 각 컨테이너에 `volumeSource` 를 추가한다.
1. 파드에 `imagePullSecrets` 이 없는 경우, `ServiceAccount` 의 `imagePullSecrets` 이 파드에 추가된다.

#### 바인딩된 서비스 어카운트 토큰 볼륨

{{< feature-state for_k8s_version="v1.21" state="beta" >}}

`BoundServiceAccountTokenVolume` [기능 게이트](/ko/docs/reference/command-line-tools-reference/feature-gates/)가 활성화되면, 
토큰 컨트롤러에 의해 생성된 무기한 서비스 어카운트 토큰을 위해, 서비스 어카운트 어드미션 컨트롤러가 시크릿 기반 볼륨 대신 다음과 같은 프로젝티드 볼륨을 추가한다.

```yaml
- name: kube-api-access-<random-suffix>
  projected:
    defaultMode: 420 # 0644
    sources:
      - serviceAccountToken:
          expirationSeconds: 3600
          path: token
      - configMap:
          items:
            - key: ca.crt
              path: ca.crt
          name: kube-root-ca.crt
      - downwardAPI:
          items:
            - fieldRef:
                apiVersion: v1
                fieldPath: metadata.namespace
              path: namespace
```

프로젝티드 볼륨은 세 가지로 구성된다.

1. kube-apiserver로부터 TokenRequest API를 통해 얻은 서비스어카운트토큰(ServiceAccountToken). 서비스어카운트토큰은 기본적으로 1시간 뒤에, 또는 파드가 삭제될 때 만료된다. 서비스어카운트토큰은 파드에 연결되며 kube-apiserver를 위해 존재한다.
1. kube-apiserver에 대한 연결을 확인하는 데 사용되는 CA 번들을 포함하는 컨피그맵(ConfigMap). 이 기능은 모든 네임스페이스에 "kube-root-ca.crt" 컨피그맵을 게시하는 기능 게이트인 `RootCAConfigMap`에 의해 동작한다. `RootCAConfigMap` 기능 게이트는 1.21에서 GA로 전환되었으며 기본적으로 활성화되어 있다. (이 플래그는 1.22에서 `--feature-gate` 인자에서 제외될 예정이다.)
1. 파드의 네임스페이스를 참조하는 DownwardAPI.

상세 사항은 [프로젝티드 볼륨](/docs/tasks/configure-pod-container/configure-projected-volume-storage/)을 참고한다.

`BoundServiceAccountTokenVolume` 기능 게이트가 활성화되어 있지 않은 경우, 
위의 프로젝티드 볼륨을 파드 스펙에 추가하여 
시크릿 기반 서비스 어카운트 볼륨을 프로젝티드 볼륨으로 수동으로 옮길 수 있다.

### 토큰 컨트롤러

토큰컨트롤러는 `kube-controller-manager` 의 일부로 실행된다. 이것은 비동기적으로 동작한다. 토큰 컨트롤러는,

- 서비스어카운트 생성을 감시하고 API에 접근할 수 있는 해당
  서비스어카운트 토큰 시크릿을 생성한다.
- 서비스어카운트 삭제를 감시하고 해당하는 모든 서비스어카운트
  토큰 시크릿을 삭제한다.
- 서비스어카운트 토큰 시크릿 추가를 감시하고, 참조된 서비스어카운트가
  존재하는지 확인하고, 필요한 경우 시크릿에 토큰을 추가한다.
- 시크릿 삭제를 감시하고 필요한 경우 해당 서비스어카운트에서
  참조를 제거한다.

서비스 어카운트 개인키 파일은 `--service-account-private-key-file`
플래그를 사용하여 `kube-controller-manager` 의 토큰 컨트롤러에 전달해야
한다. 개인키는 생성된 서비스 어카운트 토큰에 서명하는 데 사용될 것이다.
마찬가지로 `--service-account-key-file` 플래그를 사용하여 해당 공개키를
`kube-apiserver` 에 전달해야 한다. 공개키는 인증 과정에서 토큰을
검증하는 데 사용될 것이다.

#### 추가적인 API 토큰 생성

컨트롤러 루프는 API 토큰이 포함된 시크릿이 각 서비스어카운트에 존재하도록 보장한다.
서비스어카운트에 대한 추가적인 API 토큰을 생성하기 위해
서비스어카운트를 참조하는 어노테이션과 함께 `kubernetes.io/service-account-token` 유형의 시크릿을 생성하면
컨트롤러가 새로 생성된 토큰으로 갱신한다.

다음은 시크릿에 대한 샘플 구성이다.

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: mysecretname
  annotations:
    kubernetes.io/service-account.name: myserviceaccount
type: kubernetes.io/service-account-token
```

```shell
kubectl create -f ./secret.yaml
kubectl describe secret mysecretname
```

#### 서비스 어카운트 토큰 시크릿 삭제/무효화

```shell
kubectl delete secret mysecretname
```

### 서비스어카운트 컨트롤러

서비스어카운트 컨트롤러는 네임스페이스에 있는 서비스어카운트를 관리하고
"default"라는 이름의 서비스어카운트가 모든 활성 네임스페이스에 존재하는지 확인한다.
