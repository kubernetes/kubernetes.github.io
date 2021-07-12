---



title: 파드 시큐리티 폴리시
content_type: concept
weight: 30
---

<!-- overview -->

{{< feature-state for_k8s_version="v1.21" state="deprecated" >}}

파드시큐리티폴리시(PodSecurityPolicy)는 쿠버네티스 v1.21부터 더이상 사용되지 않으며, v1.25에서 제거된다.

파드 시큐리티 폴리시를 사용하면 파드 생성 및 업데이트에 대한 세분화된 권한을
부여할 수 있다.

<!-- body -->

## 파드 시큐리티 폴리시란?

_Pod Security Policy_ 는 파드 명세의 보안 관련 측면을 제어하는 ​​클러스터-레벨의
리소스이다. [파드시큐리티폴리시](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#podsecuritypolicy-v1beta1-policy) 오브젝트는
관련 필드에 대한 기본값뿐만 아니라 시스템에 적용하기 위해 파드가 실행해야만 하는
조건 셋을 정의한다. 관리자는
다음을 제어할 수 있다.

| 제어 측면                                            | 필드 이름                                 |
| ----------------------------------------------------| ------------------------------------------- |
| 특권을 가진(privileged) 컨테이너의 실행                                | [`privileged`](#특권을-가진)                                |
| 호스트 네임스페이스의 사용                                 | [`hostPID`, `hostIPC`](#호스트-네임스페이스)    |
| 호스트 네트워킹과 포트의 사용                               | [`hostNetwork`, `hostPorts`](#호스트-네임스페이스) |
| 볼륨 유형의 사용                                        | [`volumes`](#볼륨-및-파일시스템)      |
| 호스트 파일시스템의 사용                                  | [`allowedHostPaths`](#볼륨-및-파일시스템) |
| 특정 FlexVolume 드라이버의 허용                         | [`allowedFlexVolumes`](#flexvolume-드라이버) |
| 파드 볼륨을 소유한 FSGroup 할당                           | [`fsGroup`](#볼륨-및-파일시스템)      |
| 읽기 전용 루트 파일시스템 사용 필요                          | [`readOnlyRootFilesystem`](#볼륨-및-파일시스템) |
| 컨테이너의 사용자 및 그룹 ID                               | [`runAsUser`, `runAsGroup`, `supplementalGroups`](#사용자-및-그룹) |
| 루트 특권으로의 에스컬레이션 제한                            | [`allowPrivilegeEscalation`, `defaultAllowPrivilegeEscalation`](#권한-에스컬레이션) |
| 리눅스 기능                                             | [`defaultAddCapabilities`, `requiredDropCapabilities`, `allowedCapabilities`](#기능) |
| 컨테이너의 SELinux 컨텍스트                               | [`seLinux`](#selinux)                       |
| 컨테이너에 허용된 Proc 마운트 유형                           | [`allowedProcMountTypes`](#allowedprocmounttypes) |
| 컨테이너가 사용하는 AppArmor 프로파일                        | [어노테이션](#apparmor)                    |
| 컨테이너가 사용하는 seccomp 프로파일                         | [어노테이션](#seccomp)                     |
| 컨테이너가 사용하는 sysctl 프로파일                          | [`forbiddenSysctls`,`allowedUnsafeSysctls`](#sysctl)                      |


## 파드 시큐리티 폴리시 활성화

파드 시큐리티 폴리시 제어는 선택 사항(하지만 권장함)인
[어드미션
컨트롤러](/docs/reference/access-authn-authz/admission-controllers/#podsecuritypolicy)로
구현된다. [어드미션 컨트롤러 활성화](/docs/reference/access-authn-authz/admission-controllers/#how-do-i-turn-on-an-admission-control-plug-in)하면
파드시큐리티폴리시가 적용되지만,
정책을 승인하지 않고 활성화하면 클러스터에
**파드가 생성되지 않는다.**

파드 시큐리티 폴리시 API(`policy/v1beta1/podsecuritypolicy`)는
어드미션 컨트롤러와 독립적으로 활성화되므로 기존 클러스터의 경우
어드미션 컨트롤러를 활성화하기 전에 정책을 추가하고 권한을
부여하는 것이 좋다.

## 정책 승인

파드시큐리티폴리시 리소스가 생성되면 아무 것도 수행하지 않는다. 이를 사용하려면
요청 사용자 또는 대상 파드의
[서비스 어카운트](/docs/tasks/configure-pod-container/configure-service-account/)는
정책에서 `use` 동사를 허용하여 정책을 사용할 권한이 있어야 한다.

대부분의 쿠버네티스 파드는 사용자가 직접 만들지 않는다. 대신 일반적으로
컨트롤러 관리자를 통해
[디플로이먼트](/ko/docs/concepts/workloads/controllers/deployment/),
[레플리카셋](/ko/docs/concepts/workloads/controllers/replicaset/), 또는 기타
템플릿 컨트롤러의 일부로 간접적으로 생성된다. 컨트롤러에 정책에 대한 접근 권한을 부여하면
해당 컨트롤러에 의해 생성된 *모든* 파드에 대한 접근 권한이 부여되므로 정책을 승인하는
기본 방법은 파드의 서비스 어카운트에 대한 접근 권한을
부여하는 것이다([예](#다른-파드를-실행) 참고).

### RBAC을 통한 방법

[RBAC](/docs/reference/access-authn-authz/rbac/)은 표준 쿠버네티스 권한 부여 모드이며,
정책 사용 권한을 부여하는 데 쉽게 사용할 수 있다.

먼저, `Role` 또는 `ClusterRole`은 원하는 정책을 `use` 하려면 접근 권한을 부여해야 한다.
접근 권한을 부여하는 규칙은 다음과 같다.

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: <role name>
rules:
- apiGroups: ['policy']
  resources: ['podsecuritypolicies']
  verbs:     ['use']
  resourceNames:
  - <list of policies to authorize>
```

그런 다음 `(Cluster)Role`이 승인된 사용자에게 바인딩된다.

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: <binding name>
roleRef:
  kind: ClusterRole
  name: <role name>
  apiGroup: rbac.authorization.k8s.io
subjects:
# Authorize specific service accounts:
- kind: ServiceAccount
  name: <authorized service account name>
  namespace: <authorized pod namespace>
# Authorize specific users (not recommended):
- kind: User
  apiGroup: rbac.authorization.k8s.io
  name: <authorized user name>
```

`RoleBinding`(`ClusterRoleBinding` 아님)을 사용하는 경우, 바인딩과 동일한 네임스페이스에서
실행되는 파드에 대해서만 사용 권한을 부여한다. 네임스페이스에서 실행되는 모든 파드에 접근 권한을
부여하기 위해 시스템 그룹과 쌍을 이룰 수 있다.
```yaml
# Authorize all service accounts in a namespace:
- kind: Group
  apiGroup: rbac.authorization.k8s.io
  name: system:serviceaccounts
# Or equivalently, all authenticated users in a namespace:
- kind: Group
  apiGroup: rbac.authorization.k8s.io
  name: system:authenticated
```

RBAC 바인딩에 대한 자세한 예는,
[역할 바인딩 예제](/docs/reference/access-authn-authz/rbac#role-binding-examples)를 참고하길 바란다.
파드시큐리티폴리시 인증에 대한 전체 예제는
[아래](#예제)를 참고하길 바란다.


### 문제 해결

- [컨트롤러 관리자](/docs/reference/command-line-tools-reference/kube-controller-manager/)는
보안 API 포트에 대해 실행되어야 하며 수퍼유저 권한이 없어야 한다.
API 서버 접근 제어에 대한 자세한 내용은
[쿠버네티스 API에 대한 접근 제어](/ko/docs/concepts/security/controlling-access)를 참고하길 바란다.
컨트롤러 관리자가 신뢰할 수 있는 API 포트(`localhost` 리스너라고도 함)를
통해 연결된 경우, 요청이 인증 및 권한 부여 모듈을 우회하고,
모든 파드시큐리티폴리시 오브젝트가 허용되며 사용자는 특권을 가진 컨테이너를
만들 수 있는 권한을 부여할 수 있다.

컨트롤러 관리자 권한 구성에 대한 자세한 내용은
[컨트롤러 역할](/docs/reference/access-authn-authz/rbac/#controller-roles)을 참고하기 바란다.

## 정책 순서

파드 생성 및 업데이트를 제한할 뿐만 아니라 파드 시큐리티 폴리시를 사용하여
제어하는 ​​많은 필드에 기본값을 제공할 수도 있다. 여러 정책을
사용할 수 있는 경우 파드 시큐리티 폴리시 컨트롤러는
다음 기준에 따라 정책을 선택한다.

1. 기본 설정을 변경하거나 파드를 변경하지 않고 파드를 있는 그대로 허용하는 파드시큐리티폴리시가
   선호된다. 이러한 비-변이(non-mutating) 파드시큐리티폴리시의
   순서는 중요하지 않다.
2. 파드를 기본값으로 설정하거나 변경해야 하는 경우, 파드를 허용할 첫 번째 파드시큐리티폴리시
   (이름순)가 선택된다.

{{< note >}}
업데이트 작업 중(파드 스펙에 대한 변경이 허용되지 않는 동안) 비-변이 파드시큐리티폴리시만
파드의 유효성을 검사하는 데 사용된다.
{{< /note >}}

## 예제

_이 예에서는 파드시큐리티폴리시 어드미션 컨트롤러가 활성화된 클러스터가 실행 중이고
클러스터 관리자 권한이 있다고 가정한다._

### 설정

이 예제와 같이 네임스페이스와 서비스 어카운트를 설정한다.
이 서비스 어카운트를 사용하여 관리자가 아닌 사용자를 조정한다.

```shell
kubectl create namespace psp-example
kubectl create serviceaccount -n psp-example fake-user
kubectl create rolebinding -n psp-example fake-editor --clusterrole=edit --serviceaccount=psp-example:fake-user
```

어떤 사용자로 활동하고 있는지 명확하게 하고 입력 내용을 저장하려면 2개의 별칭(alias)을
만든다.

```shell
alias kubectl-admin='kubectl -n psp-example'
alias kubectl-user='kubectl --as=system:serviceaccount:psp-example:fake-user -n psp-example'
```

### 정책과 파드 생성

파일에서 예제 파드시큐리티폴리시 오브젝트를 정의한다. 이는 특권있는 파드를
만들지 못하게 하는 정책이다.
파드시큐리티폴리시 오브젝트의 이름은 유효한
[DNS 서브도메인 이름](/ko/docs/concepts/overview/working-with-objects/names#dns-서브도메인-이름)이어야 한다.

{{< codenew file="policy/example-psp.yaml" >}}

그리고 kubectl로 생성한다.

```shell
kubectl-admin create -f example-psp.yaml
```

이제 권한이 없는 사용자로서 간단한 파드를 생성해보자.

```shell
kubectl-user create -f- <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: pause
spec:
  containers:
    - name: pause
      image: k8s.gcr.io/pause
EOF
```

이것의 출력은 다음과 같을 것이다.

```
Error from server (Forbidden): error when creating "STDIN": pods "pause" is forbidden: unable to validate against any pod security policy: []
```

**무슨 일이 일어났나?** 파드시큐리티폴리시가 생성되었지만, 파드의 서비스 어카운트나 `fake-user`는
새 정책을 사용할 권한이 없다.

```shell
kubectl-user auth can-i use podsecuritypolicy/example
no
```

예제 정책에서 `fake-user`에게 `use` 동사를 부여하는 rolebinding을
생성한다.

{{< note >}}
이 방법은 권장하지 않는다! 선호하는 방법은 [다음 절](#다른-파드를-실행)을
참고하길 바란다.
{{< /note >}}

```shell
kubectl-admin create role psp:unprivileged \
    --verb=use \
    --resource=podsecuritypolicy \
    --resource-name=example
role "psp:unprivileged" created

kubectl-admin create rolebinding fake-user:psp:unprivileged \
    --role=psp:unprivileged \
    --serviceaccount=psp-example:fake-user
rolebinding "fake-user:psp:unprivileged" created

kubectl-user auth can-i use podsecuritypolicy/example
yes
```

이제 파드 생성을 다시 시도하자.

```shell
kubectl-user create -f- <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: pause
spec:
  containers:
    - name: pause
      image: k8s.gcr.io/pause
EOF
```

이것의 출력은 다음과 같을 것이다.

```
pod "pause" created
```

예상대로 작동한다! 그러나 특권있는 파드를 만들려는 시도는 여전히
거부되어야 한다.

```shell
kubectl-user create -f- <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: privileged
spec:
  containers:
    - name: pause
      image: k8s.gcr.io/pause
      securityContext:
        privileged: true
EOF
```

이것의 출력은 다음과 같을 것이다.

```
Error from server (Forbidden): error when creating "STDIN": pods "privileged" is forbidden: unable to validate against any pod security policy: [spec.containers[0].securityContext.privileged: Invalid value: true: Privileged containers are not allowed]
```

계속 진행하기 전에 파드를 삭제하자.

```shell
kubectl-user delete pod pause
```

### 다른 파드를 실행

약간 다르게 다시 시도해보자.

```shell
kubectl-user create deployment pause --image=k8s.gcr.io/pause
deployment "pause" created

kubectl-user get pods
No resources found.

kubectl-user get events | head -n 2
LASTSEEN   FIRSTSEEN   COUNT     NAME              KIND         SUBOBJECT                TYPE      REASON                  SOURCE                                  MESSAGE
1m         2m          15        pause-7774d79b5   ReplicaSet                            Warning   FailedCreate            replicaset-controller                   Error creating: pods "pause-7774d79b5-" is forbidden: no providers available to validate pod request
```

**무슨 일이 일어났나?** 우리는 이미 `fake-user`에 대해 `psp:unprivileged` 역할을 바인딩했는데,
`Error creating: pods "pause-7774d79b5-" is
forbidden: no providers available to validate pod request` 오류가
발생하는 이유는 무엇인가? 그 답은 소스인 `replicaset-controller`에 있다. Fake-user가
디플로이먼트를 성공적으로 생성했지만(레플리카셋을 성공적으로 생성했음), 레플리카셋이
파드를 생성했을 때 podsecuritypolicy 예제를
사용할 권한이 없었다.

이 문제를 해결하려면 `psp:unprivileged` 역할을 파드의 서비스 어카운트에 대신
바인딩한다. 이 경우(지정하지 않았으므로) 서비스 어카운트는
`default`이다.

```shell
kubectl-admin create rolebinding default:psp:unprivileged \
    --role=psp:unprivileged \
    --serviceaccount=psp-example:default
rolebinding "default:psp:unprivileged" created
```

이제 다시 한번 해본다면 replicaset-controller가
파드를 성공적으로 생성할 것이다.

```shell
kubectl-user get pods --watch
NAME                    READY     STATUS    RESTARTS   AGE
pause-7774d79b5-qrgcb   0/1       Pending   0         1s
pause-7774d79b5-qrgcb   0/1       Pending   0         1s
pause-7774d79b5-qrgcb   0/1       ContainerCreating   0         1s
pause-7774d79b5-qrgcb   1/1       Running   0         2s
```

### 정리

네임스페이스를 삭제하여 대부분의 예제 리소스를 정리한다.

```shell
kubectl-admin delete ns psp-example
namespace "psp-example" deleted
```

`PodSecurityPolicy` 리소스는 네임스페이스에 포함되지 않으므로 별도로
정리해야 한다.

```shell
kubectl-admin delete psp example
podsecuritypolicy "example" deleted
```

### 정책 예제

다음은 파드 시큐리티 폴리시 어드미션 컨트롤러를 사용하지 않는 것과 동일하게 만들 수 있는
최소한의 제한 정책이다.

{{< codenew file="policy/privileged-psp.yaml" >}}

다음은 권한이 없는 사용자로서의 실행을 필요로 하고, 루트로의 에스컬레이션(escalation) 가능성을 차단하고,
여러 보안 메커니즘을 사용을 필요로 하는 제한적
정책의 예제이다.

{{< codenew file="policy/restricted-psp.yaml" >}}

더 많은 예제는 [파드 보안 표준](/docs/concepts/security/pod-security-standards/#policy-instantiation)을 본다.

## 정책 레퍼런스

### 특권을 가진

**Privileged** - 파드의 컨테이너가 특권 모드를 사용할 수 있는지 여부를 결정한다.
기본적으로 컨테이너는 호스트의 모든 장치에 접근할 수 없지만
"특권을 가진" 컨테이너는 호스트의 모든 장치에 접근할 수 있다. 이것은
컨테이너가 호스트에서 실행되는 프로세스와 거의 동일한 접근을 허용한다.
이것은 네트워크 스택 조작 및 장치 접근과 같은
리눅스 기능을 사용하려는 컨테이너에 유용하다.

### 호스트 네임스페이스

**HostPID** - 파드 컨테이너가 호스트 프로세스 ID 네임스페이스를 공유할 수 있는지 여부를
제어한다. ptrace와 함께 사용하면 컨테이너 외부로 권한을 에스컬레이션하는 데 사용할 수
있다(ptrace는 기본적으로 금지되어 있음).

**HostIPC** - 파드 컨테이너가 호스트 IPC 네임스페이스를 공유할 수 있는지 여부를
제어한다.

**HostNetwork** - 파드가 노드 네트워크 네임스페이스를 사용할 수 있는지 여부를 제어한다.
이렇게 하면 파드에 루프백 장치에 접근 권한을 주고, 서비스는 로컬호스트(localhost)를 리스닝할 수 있으며,
동일한 노드에 있는 다른 파드의 네트워크 활동을 스누핑(snoop)하는 데
사용할 수 있다.

**HostPorts** - 호스트 네트워크 네임스페이스에 허용되는 포트 범위의 목록을
제공한다. `min`과 `max`를 포함하여 `HostPortRange`의 목록으로 정의된다.
기본값은 허용하는 호스트 포트 없음(no allowed host ports)이다.

### 볼륨 및 파일시스템

**Volumes** - 허용되는 볼륨 유형의 목록을 제공한다. 허용 가능한 값은
볼륨을 생성할 때 정의된 볼륨 소스에 따른다. 볼륨 유형의 전체 목록은
[볼륨 유형들](/ko/docs/concepts/storage/volumes/#볼륨-유형들)에서 참고한다.
또한 `*`를 사용하여 모든 볼륨 유형을
허용할 수 있다.

새 PSP에 허용되는 볼륨의 **최소 권장 셋** 은 다음과 같다.

- 컨피그맵
- 다운워드API
- emptyDir
- 퍼시스턴트볼륨클레임
- 시크릿
- 프로젝티드(projected)

{{< warning >}}
파드시큐리티폴리시는 `PersistentVolumeClaim`이 참조할 수 있는 `PersistentVolume`
오브젝트의 유형을 제한하지 않으며 hostPath 유형
`PersistentVolumes`은 읽기-전용 접근 모드를 지원하지 않는다. 신뢰할 수 있는 사용자만
`PersistentVolume` 오브젝트를 생성할 수 있는 권한을 부여 받아야 한다.
{{< /warning >}}

**FSGroup** - 일부 볼륨에 적용되는 보충 그룹(supplemental group)을 제어한다.

- *MustRunAs* - 하나 이상의 `range`를 지정해야 한다. 첫 번째 범위의 최솟값을
기본값으로 사용한다. 모든 범위에 대해 검증한다.
- *MayRunAs* - 하나 이상의 `range`를 지정해야 한다. 기본값을 제공하지 않고
`FSGroups`을 설정하지 않은 상태로 둘 수 있다. `FSGroups`이 설정된 경우 모든 범위에 대해
유효성을 검사한다.
- *RunAsAny* - 기본값은 제공되지 않는다. 어떠한 `fsGroup` ID의 지정도 허용한다.

**AllowedHostPaths** - hostPath 볼륨에서 사용할 수 있는 호스트 경로의 목록을
지정한다. 빈 목록은 사용되는 호스트 경로에 제한이 없음을 의미한다.
이는 단일 `pathPrefix` 필드가 있는 오브젝트 목록으로 정의되며, hostPath 볼륨은
허용된 접두사로 시작하는 경로를 마운트할 수 있으며 `readOnly` 필드는
읽기-전용으로 마운트 되어야 함을 나타낸다.
예를 들면 다음과 같습니다.

```yaml
 allowedHostPaths:
   # 이 정책은 "/foo", "/foo/", "/foo/bar" 등을 허용하지만,
   # "/fool", "/etc/foo" 등은 허용하지 않는다.
   # "/foo/../" 는 절대 유효하지 않다.
   - pathPrefix: "/foo"
     readOnly: true # 읽기 전용 마운트만 허용
```

{{< warning >}}호스트 파일시스템에 제한없는 접근을 부여하며, 컨테이너가 특권을 에스컬레이션
(다른 컨테이너들에 있는 데이터를 읽고, 시스템 서비스의 자격 증명을 어뷰징(abusing)하는 등)할
수 있도록 만드는 다양한 방법이 있다. 예를 들면, Kubelet과 같다.

쓰기 가능한 hostPath 디렉터리 볼륨을 사용하면, 컨테이너가 `pathPrefix` 외부의
호스트 파일시스템에 대한 통행을 허용하는 방식으로 컨테이너의 파일시스템 쓰기(write)를 허용한다.
쿠버네티스 1.11 이상 버전에서 사용 가능한 `readOnly: true`는 지정된 `pathPrefix`에 대한
접근을 효과적으로 제한하기 위해 **모든** `allowedHostPaths`에서 사용해야 한다.
{{< /warning >}}

**ReadOnlyRootFilesystem** - 컨테이너는 읽기-전용 루트 파일시스템(즉, 쓰기 가능한 레이어 없음)으로
실행해야 한다.

### FlexVolume 드라이버

flexvolume에서 사용할 수 있는 FlexVolume 드라이버의 목록을 지정한다.
빈 목록 또는 nil은 드라이버에 제한이 없음을 의미한다.
[`volumes`](#볼륨-및-파일시스템) 필드에 `flexVolume` 볼륨 유형이 포함되어
있는지 확인한다. 그렇지 않으면 FlexVolume 드라이버가 허용되지 않는다.

예를 들면 다음과 같다.

```yaml
apiVersion: policy/v1beta1
kind: PodSecurityPolicy
metadata:
  name: allow-flex-volumes
spec:
  # ... 다른 스펙 필드
  volumes:
    - flexVolume
  allowedFlexVolumes:
    - driver: example/lvm
    - driver: example/cifs
```

### 사용자 및 그룹

**RunAsUser** - 컨테이너를 실행할 사용자 ID를 제어힌다.

- *MustRunAs* - 하나 이상의 `range`를 지정해야 한다. 첫 번째 범위의 최솟값을
기본값으로 사용한다. 모든 범위에 대해 검증한다.
- *MustRunAsNonRoot* - 파드가 0이 아닌 `runAsUser`로 제출되거나
이미지에 `USER` 지시문이 정의되어 있어야 한다(숫자 UID 사용). `runAsNonRoot` 또는
`runAsUser` 설정을 지정하지 않은 파드는 `runAsNonRoot=true`를 설정하도록
변경되므로 컨테이너에 0이 아닌 숫자가 정의된 `USER` 지시문이
필요하다. 기본값은 제공되지 않는다.
이 전략에서는 `allowPrivilegeEscalation=false`를 설정하는 것이 좋다.
- *RunAsAny* - 기본값은 제공되지 않는다. 어떠한 `runAsUser`의 지정도 허용한다.

**RunAsGroup** - 컨테이너가 실행될 기본 그룹 ID를 제어한다.

- *MustRunAs* - 하나 이상의 `range`를 지정해야 한다. 첫 번째 범위의 최솟값을
기본값으로 사용한다. 모든 범위에 대해 검증한다.
- *MayRunAs* - `RunAsGroup`을 지정할 필요가 없다. 그러나 `RunAsGroup`을 지정하면
정의된 범위에 속해야 한다.
- *RunAsAny* - 기본값은 제공되지 않는다. 어떠한 `runAsGroup`의 지정도 허용한다.


**SupplementalGroups** - 컨테이너가 추가할 그룹 ID를 제어한다.

- *MustRunAs* - 하나 이상의 `range`를 지정해야 한다. 첫 번째 범위의 최솟값을
기본값으로 사용한다. 모든 범위에 대해 검증한다.
- *MayRunAs* - 하나 이상의 `range`를 지정해야 한다. `supplementalGroups`에
기본값을 제공하지 않고 설정하지 않은 상태로 둘 수 있다.
`supplementalGroups`가 설정된 경우 모든 범위에 대해 유효성을 검증한다.
- *RunAsAny* - 기본값은 제공되지 않는다. 어떠한 `supplementalGroups`의 지정도
허용한다.

### 권한 에스컬레이션

이 옵션은 `allowPrivilegeEscalation` 컨테이너 옵션을 제어한다. 이 bool은
컨테이너 프로세스에서
[`no_new_privs`](https://www.kernel.org/doc/Documentation/prctl/no_new_privs.txt)
플래그가 설정되는지 여부를 직접 제어한다. 이 플래그는 `setuid` 바이너리가
유효 사용자 ID를 변경하지 못하게 하고 파일에 추가 기능을 활성화하지 못하게
한다(예: `ping` 도구 사용을 못하게 함). `MustRunAsNonRoot`를 효과적으로
강제하려면 이 동작이 필요하다.

**AllowPrivilegeEscalation** - 사용자가 컨테이너의 보안 컨텍스트를
`allowPrivilegeEscalation=true`로 설정할 수 있는지 여부를 게이트한다.
이 기본값은 setuid 바이너리를 중단하지 않도록 허용한다. 이를 `false`로 설정하면
컨테이너의 하위 프로세스가 상위 프로세스보다 더 많은 권한을 얻을 수 없다.

**DefaultAllowPrivilegeEscalation** - `allowPrivilegeEscalation` 옵션의
기본값을 설정한다. 이것이 없는 기본 동작은 setuid 바이너리를 중단하지 않도록
권한 에스컬레이션을 허용하는 것이다. 해당 동작이 필요하지 않은 경우 이 필드를 사용하여
기본적으로 허용하지 않도록 설정할 수 있지만 파드는 여전히 `allowPrivilegeEscalation`을
명시적으로 요청할 수 있다.

### 기능

리눅스 기능은 전통적으로 슈퍼유저와 관련된 권한을 보다 세밀하게 분류한다.
이러한 기능 중 일부는 권한 에스컬레이션 또는 컨테이너 분류에 사용될 수 있으며
파드시큐리티폴리시에 의해 제한될 수 있다. 리눅스 기능에 대한 자세한 내용은
[기능(7)](http://man7.org/linux/man-pages/man7/capabilities.7.html)을
참고하길 바란다.

다음 필드는 대문자로 표기된 기능 이름 목록을
`CAP_` 접두사 없이 가져온다.

**AllowedCapabilities** - 컨테이너에 추가될 수 있는 기능의 목록을
제공한다. 기본적인 기능 셋은 암시적으로 허용된다. 비어있는 셋은
기본 셋을 넘어서는 추가 기능이 추가되지 않는 것을
의미한다. `*`는 모든 기능을 허용하는 데 사용할 수 있다.

**RequiredDropCapabilities** - 컨테이너에서 삭제해야 하는 기능이다.
이러한 기능은 기본 셋에서 제거되며 추가해서는 안된다.
`RequiredDropCapabilities`에 나열된 기능은 `AllowedCapabilities` 또는
`DefaultAddCapabilities`에 포함되지 않아야 한다.

**DefaultAddCapabilities** - 런타임 기본값 외에 기본적으로 컨테이너에 추가되는 기능이다.
도커 런타임을 사용할 때 기본 기능 목록은
[도커 문서](https://docs.docker.com/engine/reference/run/#runtime-privilege-and-linux-capabilities)를
참고하길 바란다.

### SELinux

- *MustRunAs* - `seLinuxOptions`을 구성해야 한다.
`seLinuxOptions`을 기본값으로 사용한다. `seLinuxOptions`에 대해 유효성을 검사한다.
- *RunAsAny* - 기본값은 제공되지 않는다. 어떠한 `seLinuxOptions`의 지정도
허용한다.

### AllowedProcMountTypes

`allowedProcMountTypes`는 허용된 ProcMountTypes의 목록이다.
비어 있거나 nil은 `DefaultProcMountType`만 사용할 수 있음을 나타낸다.

`DefaultProcMount`는 /proc의 읽기 전용 및 마스킹(masking)된 경로에 컨테이너 런타임
기본값을 사용한다. 대부분의 컨테이너 런타임은 특수 장치나 정보가 실수로 보안에
노출되지 않도록 /proc의 특정 경로를 마스킹한다. 이것은 문자열
`Default`로 표시된다.

유일하게 다른 ProcMountType은 `UnmaskedProcMount`로, 컨테이너 런타임의
기본 마스킹 동작을 무시하고 새로 작성된 /proc 컨테이너가 수정없이
그대로 유지되도록 한다. 이 문자열은
`Unmasked`로 표시된다.

### AppArmor

파드시큐리티폴리시의 어노테이션을 통해 제어된다. [AppArmor
문서](/ko/docs/tutorials/clusters/apparmor/#podsecuritypolicy-annotations)를 참고하길 바란다.

### Seccomp

쿠버네티스 v1.19부터 파드나 컨테이너의 `securityContext` 에서
`seccompProfile` 필드를 사용하여 [seccomp 프로파일 사용을
제어](/docs/tutorials/clusters/seccomp)할 수 있다. 이전 버전에서는, 파드에
어노테이션을 추가하여 seccomp를 제어했다. 두 버전에서 동일한 파드시큐리티폴리시를 사용하여
이러한 필드나 어노테이션이 적용되는 방식을 적용할 수 있다.

**seccomp.security.alpha.kubernetes.io/defaultProfileName** - 컨테이너에
적용할 기본 seccomp 프로파일을 지정하는 어노테이션이다. 가능한 값은
다음과 같다.

- `unconfined` - 대안이 제공되지 않으면 Seccomp가 컨테이너 프로세스에 적용되지
  않는다(쿠버네티스의 기본값임).
- `runtime/default` - 기본 컨테이너 런타임 프로파일이 사용된다.
- `docker/default` - 도커 기본 seccomp 프로파일이 사용된다. 쿠버네티스 1.11 부터 사용 중단(deprecated)
  되었다. 대신 `runtime/default` 사용을 권장한다.
- `localhost/<path>` - `<seccomp_root>/<path>`에 있는 노드에서 파일을 프로파일로
  지정한다. 여기서 `<seccomp_root>`는 Kubelet의 `--seccomp-profile-root` 플래그를
  통해 정의된다. `--seccomp-profile-root` 플래그가
  정의되어 있지 않으면, `<root-dir>` 이 `--root-dir` 플래그로
  지정된 `<root-dir>/seccomp` 기본 경로가 사용된다.

{{< note >}}
  `--seccomp-profile-root` 플래그는 쿠버네티스 v1.19부터 더 이상 사용되지
  않는다. 사용자는 기본 경로를 사용하는 것이 좋다.
{{< /note >}}

**seccomp.security.alpha.kubernetes.io/allowedProfileNames** - 파드 seccomp
어노테이션에 허용되는 값을 지정하는 어노테이션. 쉼표로 구분된
허용된 값의 목록으로 지정된다. 가능한 값은 위에 나열된 값과
모든 프로파일을 허용하는 `*` 이다.
이 주석이 없으면 기본값을 변경할 수 없다.

### Sysctl

기본적으로 모든 안전한 sysctls가 허용된다.

- `forbiddenSysctls` - 특정 sysctls를 제외한다. 목록에서 안전한 것과 안전하지 않은 sysctls의 조합을 금지할 수 있다. 모든 sysctls 설정을 금지하려면 자체적으로 `*`를 사용한다.
- `allowedUnsafeSysctls` - `forbiddenSysctls`에 나열되지 않는 한 기본 목록에서 허용하지 않은 특정 sysctls를 허용한다.

[Sysctl 문서](
/docs/tasks/administer-cluster/sysctl-cluster/#podsecuritypolicy)를 참고하길 바란다.

## {{% heading "whatsnext" %}}

- 폴리시 권장 사항에 대해서는 [파드 보안 표준](/docs/concepts/security/pod-security-standards/)을 참조한다.
- API 세부 정보는 [파드 시큐리티 폴리시 레퍼런스](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#podsecuritypolicy-v1beta1-policy) 참조한다.
