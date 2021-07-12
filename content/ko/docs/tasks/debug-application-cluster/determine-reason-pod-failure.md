---
title: 파드 실패의 원인 검증하기
content_type: task
---

<!-- overview -->

이 페이지는 컨테이너 종료 메시지를 읽고 쓰는
방법을 보여준다.

종료 메시지는 컨테이너가 치명적인 이벤트에 대한 정보를,
대시보드나 모니터링 소프트웨어 도구와 같이
쉽게 조회 및 표시할 수 있는 위치에
기록하는 방법을 제공한다.
대부분의 경우에 종료 메시지에 넣는 정보는
일반
[쿠버네티스 로그](/ko/docs/concepts/cluster-administration/logging/)에도 쓰여져야 한다.




## {{% heading "prerequisites" %}}


{{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}




<!-- steps -->

## 종료 메시지 읽기 및 쓰기

이 예제에서는, 하나의 컨테이너를 실행하는 파드를 생성한다.
하단의 설정 파일은 컨테이너가 시작될 때 수행하는
명령어를 지정한다.

{{< codenew file="debug/termination.yaml" >}}

1. 다음의 YAML 설정 파일에 기반한 파드를 생성한다.

        kubectl apply -f https://k8s.io/examples/debug/termination.yaml

	   YAML 파일에 있는 `command` 와 `args` 필드에서 컨테이너가 10초 간 잠든 뒤에
	   "Sleep expired" 문자열을 `/dev/termination-log` 파일에 기록하는
	   것을 확인할 수 있다. 컨테이너는 "Sleep expired" 메시지를
	   기록한 후에 종료된다.

1. 파드와 관련된 정보를 출력한다.

        kubectl get pod termination-demo

	   파드가 더 이상 실행되지 않을 때까지 앞선 명령어를 반복한다.

1. 파드에 관한 상세 정보를 출력한다.

        kubectl get pod termination-demo --output=yaml

	   결과는 "Sleep expired" 메시지를 포함한다.

        apiVersion: v1
        kind: Pod
        ...
            lastState:
              terminated:
                containerID: ...
                exitCode: 0
                finishedAt: ...
                message: |
                  Sleep expired
                ...

1. 종료 메시지만을 포함하는 출력 결과를 보기
위해서는 Go 템플릿을 사용한다.

        kubectl get pod termination-demo -o go-template="{{range .status.containerStatuses}}{{.lastState.terminated.message}}{{end}}"

## 종료 메시지 사용자 정의하기

쿠버네티스는 컨테이너의 `terminationMessagePath` 필드에 지정된
종료 메시지 파일에서 종료 메시지를 검색하며, 이 필드의 기본값은
`/dev/termination-log` 이다. 이 필드를 사용자 정의 함으로써
쿠버네티스가 종료 메시지를 검색할 때 다른 파일을 사용하도록 조정할 수 있다.
쿠버네티스는 지정된 파일의 내용을 사용하여 컨테이너의 성공 및 실패에 대한 상태 메시지를 채운다.

종료 메시지는 assertion failure 메세지처럼 간결한 최종 상태로 생성된다.
kubelet은 4096 바이트보다 긴 메시지를 자른다. 모든 컨테이너의 총 메시지 길이는
12KiB로 제한된다. 기본 종료 메시지 경로는 `/dev/termination-log`이다.
파드가 시작된 후에는 종료 메시지 경로를 설정할 수 없다.

다음의 예제에서 컨테이너는, 쿠버네티스가 조회할 수 있도록
`/tmp/my-log` 파일에 종료 메시지를 기록한다.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: msg-path-demo
spec:
  containers:
  - name: msg-path-demo-container
    image: debian
    terminationMessagePath: "/tmp/my-log"
```

또한 사용자는 추가적인 사용자 정의를 위해 컨테이너의 `terminationMessagePolicy`
필드를 설정할 수 있다. 이 필드의 기본 값은 `File` 이며,
이는 오직 종료 메시지 파일에서만 종료 메시지가 조회되는 것을 의미한다.
`terminationMessagePolicy` 필드의 값을 "`FallbackToLogsOnError` 으로
설정함으로써, 종료 메시지 파일이 비어 있고 컨테이너가 오류와 함께 종료 되었을 경우
쿠버네티스가 컨테이너 로그 출력의 마지막 청크를 사용하도록 지시할 수 있다.
로그 출력은 2048 바이트나 80 행 중 더 작은 값으로 제한된다.



## {{% heading "whatsnext" %}}


* [컨테이너](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#container-v1-core)
  에 있는 `terminationMessagePath` 에 대해 읽어보기.
* [로그 검색](/ko/docs/concepts/cluster-administration/logging/)에 대해 배워보기.
* [Go 템플릿](https://golang.org/pkg/text/template/)에 대해 배워보기.
