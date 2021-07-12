---
title: 런타임클래스(RuntimeClass)
content_type: concept
weight: 20
---

<!-- overview -->

{{< feature-state for_k8s_version="v1.20" state="stable" >}}

이 페이지는 런타임클래스 리소스와 런타임 선택 메커니즘에 대해서 설명한다.

런타임클래스는 컨테이너 런타임을 구성을 선택하는 기능이다. 컨테이너 런타임
구성은 파드의 컨테이너를 실행하는 데 사용된다.




<!-- body -->

## 동기

서로 다른 파드간에 런타임클래스를 설정하여
성능과 보안의 균형을 유지할 수 있다.
예를 들어, 일부 작업에서 높은 수준의 정보 보안 보증이 요구되는 경우,
하드웨어 가상화를 이용하는 컨테이너 런타임으로 파드를 실행하도록 예약하는 선택을 할 수 있다.
그러면 몇가지 추가적인 오버헤드는 있지만
대체 런타임을 추가 분리하는 유익이 있다.

또한 런타임클래스를 사용하여 컨테이너 런타임이 같으나 설정이 다른
여러 파드를 실행할 수 있다.

## 셋업

1. CRI 구현(implementation)을 노드에 설정(런타임에 따라서).
2. 상응하는 런타임클래스 리소스 생성.

### 1. CRI 구현을 노드에 설정

런타임클래스를 통한 가능한 구성은 컨테이너 런타임 인터페이스(CRI) 구현에 의존적이다.
사용자의 CRI 구현에 따른 설정 방법은
연관된 문서를 통해서 확인한다([아래](#cri-configuration)).

{{< note >}}
런타임클래스는 기본적으로 클러스터 전체에 걸쳐 동질의 노드 설정
(모든 노드가 컨테이너 런타임에 준하는 동일한 방식으로 설정되었음을 의미)을 가정한다.
이종의(heterogeneous) 노드 설정을 지원하기 위해서는, 아래 [스케줄](#스케줄)을 참고한다.
{{< /note >}}

해당 설정은 상응하는 `handler` 이름을 가지며, 이는 런타임클래스에 의해서 참조된다.
런타임 핸들러는 유효한 DNS 1123 서브도메인(알파-숫자 + `-`와 `.`문자)을 가져야 한다.

### 2. 상응하는 런타임클래스 리소스 생성

1단계에서 셋업 한 설정은 연관된 `handler` 이름을 가져야 하며, 이를 통해서 설정을 식별할 수 있다.
각 런타임 핸들러(그리고 선택적으로 비어있는 `""` 핸들러)에 대해서, 상응하는 런타임클래스 오브젝트를 생성한다.

현재 런타임클래스 리소스는 런타임클래스 이름(`metadata.name`)과 런타임 핸들러
(`handler`)로 단 2개의 중요 필드만 가지고 있다. 오브젝트 정의는 다음과 같은 형태이다.

```yaml
apiVersion: node.k8s.io/v1  # 런타임클래스는 node.k8s.io API 그룹에 정의되어 있음
kind: RuntimeClass
metadata:
  name: myclass  # 런타임클래스는 해당 이름을 통해서 참조됨
  # 런타임클래스는 네임스페이스가 없는 리소스임
handler: myconfiguration  # 상응하는 CRI 설정의 이름임
```

런타임클래스 오브젝트의 이름은 유효한
[DNS 레이블 이름](/ko/docs/concepts/overview/working-with-objects/names/#dns-레이블-이름)어이야 한다.

{{< note >}}
런타임클래스 쓰기 작업(create/update/patch/delete)은
클러스터 관리자로 제한할 것을 권장한다. 이것은 일반적으로 기본 설정이다.
더 자세한 정보는 [권한 개요](/ko/docs/reference/access-authn-authz/authorization/)를 참고한다.
{{< /note >}}

## 사용

클러스터를 위해서 런타임클래스를 설정하고 나면, 그것을 사용하는 것은 매우 간단하다. 파드 스펙에
`runtimeClassName`를 명시한다. 예를 들면 다음과 같다.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: mypod
spec:
  runtimeClassName: myclass
  # ...
```

이것은 kubelet이 지명된 런타임클래스를 사용하여 해당 파드를 실행하도록 지시할 것이다.
만약 지명된 런타임클래스가 없거나, CRI가 상응하는 핸들러를 실행할 수 없는 경우, 파드는
`Failed` 터미널 [단계](/ko/docs/concepts/workloads/pods/pod-lifecycle/#파드의-단계-phase)로 들어간다.
에러 메시지에 상응하는 [이벤트](/docs/tasks/debug-application-cluster/debug-application-introspection/)를
확인한다.

만약 명시된 `runtimeClassName`가 없다면, 기본 런타임 핸들러가 사용되며,
런타임클래스 기능이 비활성화되었을 때와 동일하게 동작한다.

### CRI 구성 {#cri-configuration}

CRI 런타임 설치에 대한 자세한 내용은 [CRI 설치](/ko/docs/setup/production-environment/container-runtimes/)를 확인한다.

#### dockershim

dockershim을 사용하는 경우 RuntimeClass는 런타임 핸들러를 `docker`로 고정한다.
dockershim은 사용자 정의 런타임 핸들러를 지원하지 않는다.

#### {{< glossary_tooltip term_id="containerd" >}}

런타임 핸들러는 containerd의 구성 파일인 `/etc/containerd/config.toml` 통해 설정한다.
유효한 핸들러는 runtimes 단락 아래에서 설정한다.

```
[plugins.cri.containerd.runtimes.${HANDLER_NAME}]
```

더 자세한 containerd의 구성 문서를 살펴본다.
https://github.com/containerd/cri/blob/master/docs/config.md

#### {{< glossary_tooltip term_id="cri-o" >}}

런타임 핸들러는 CRI-O의 구성파일인 `/etc/crio/crio.conf`을 통해 설정한다.
[crio.runtime 테이블](https://github.com/cri-o/cri-o/blob/master/docs/crio.conf.5.md#crioruntime-table) 아래에
유효한 핸들러를 설정한다.

```
[crio.runtime.runtimes.${HANDLER_NAME}]
  runtime_path = "${PATH_TO_BINARY}"
```

더 자세한 것은 CRI-O의 [설정 문서](https://github.com/cri-o/cri-o/blob/master/docs/crio.conf.5.md)를 본다.

## 스케줄

{{< feature-state for_k8s_version="v1.16" state="beta" >}}

RuntimeClass에 `scheduling` 필드를 지정하면, 이 RuntimeClass로 실행되는 파드가 
이를 지원하는 노드로 예약되도록 제약 조건을 설정할 수 있다.
`scheduling`이 설정되지 않은 경우 이 RuntimeClass는 모든 노드에서 지원되는 것으로 간주된다.

파드가 지정된 런타임클래스를 지원하는 노드에 안착한다는 것을 보장하려면,
해당 노드들은 `runtimeClass.scheduling.nodeSelector` 필드에서 선택되는 공통 레이블을 가져야한다.
런타임 클래스의 nodeSelector는 파드의 nodeSelector와 어드미션 시 병합되어서, 실질적으로
각각에 의해 선택된 노드의 교집합을 취한다. 충돌이 있는 경우,
파드는 거부된다.

지원되는 노드가 테인트(taint)되어서 다른 런타임클래스 파드가 노드에서 구동되는 것을 막고 있다면,
`tolerations`를 런타임클래스에 추가할 수 있다. `nodeSelector`를 사용하면, 어드미션 시
해당 톨러레이션(toleration)이 파드의 톨러레이션과 병합되어, 실질적으로 각각에 의해 선택된
노드의 합집합을 취한다.

노드 셀렉터와 톨러레이션 설정에 대해 더 배우려면
[노드에 파드 할당](/ko/docs/concepts/scheduling-eviction/assign-pod-node/)을 참고한다.

### 파드 오버헤드

{{< feature-state for_k8s_version="v1.18" state="beta" >}}

파드 실행과 연관되는 _오버헤드_ 리소스를 지정할 수 있다. 오버헤드를 선언하면
클러스터(스케줄러 포함)가 파드와 리소스에 대한 결정을 내릴 때 처리를 할 수 있다.
PodOverhead를 사용하려면, PodOverhead [기능 게이트](/ko/docs/reference/command-line-tools-reference/feature-gates/)
를 활성화 시켜야 한다. (기본으로 활성화 되어 있다.)

파드 오버헤드는 런타임 클래스에서 `overhead` 필드를 통해 정의된다. 이 필드를 사용하면,
해당 런타임 클래스를 사용해서 구동 중인 파드의 오버헤드를 특정할 수 있고 이 오버헤드가
쿠버네티스 내에서 처리된다는 것을 보장할 수 있다.


## {{% heading "whatsnext" %}}


- [런타임클래스 설계](https://github.com/kubernetes/enhancements/blob/master/keps/sig-node/585-runtime-class/README.md)
- [런타임클래스 스케줄링 설계](https://github.com/kubernetes/enhancements/blob/master/keps/sig-node/585-runtime-class/README.md#runtimeclass-scheduling)
- [파드 오버헤드](/ko/docs/concepts/scheduling-eviction/pod-overhead/) 개념에 대해 읽기
- [파드 오버헤드 기능 설계](https://github.com/kubernetes/enhancements/tree/master/keps/sig-node/688-pod-overhead)
