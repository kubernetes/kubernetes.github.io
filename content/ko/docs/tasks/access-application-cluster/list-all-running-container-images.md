---
title: 클러스터 내 모든 컨테이너 이미지 목록 보기
content_type: task
weight: 100
---

<!-- overview -->

이 문서는 kubectl을 이용하여 클러스터 내 모든 컨테이너 이미지 목록을
조회하는 방법에 관해 설명한다.

## {{% heading "prerequisites" %}} 

{{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}

<!-- steps -->

이 작업에서는 kubectl을 사용하여 클러스터 내 모든 파드의 정보를
조회하고, 결과값의 서식을 변경하여 각 파드에 대한 컨테이너 이미지 목록으로
재구성할 것이다.

## 모든 네임스페이스의 모든 컨테이너 이미지 가져오기

- `kubectl get pods --all-namespaces` 를 사용하여 모든 네임스페이스의 모든 파드 정보를 가져온다.
- 컨테이너 이미지 이름만 출력하기 위해 `-o jsonpath={.items[*].spec.containers[*].image}` 를 사용한다.
  이 명령어는 결과값으로 받은 json을 반복적으로 파싱하여,
  `image` 필드만을 출력한다.
  - jsonpath를 사용하는 방법에 대해 더 많은 정보를 얻고 싶다면
    [Jsonpath 지원](/ko/docs/reference/kubectl/jsonpath/)을 확인한다.
- 다음의 표준 툴을 이용해서 결과값을 처리한다. `tr`, `sort`, `uniq`
  - `tr` 을 사용하여 공백을 줄 바꾸기로 대체한다.
  - `sort` 를 사용하여 결과값을 정렬한다.
  - `uniq` 를 사용하여 이미지 개수를 합산한다.

```shell
kubectl get pods --all-namespaces -o jsonpath="{.items[*].spec.containers[*].image}" |\
tr -s '[[:space:]]' '\n' |\
sort |\
uniq -c
```

이 커맨드는 결과값으로 나온 모든 아이템 중에 `image` 라고 명명된 필드를
모두 출력한다.

이와 다른 방법으로 파드 이미지 필드 값의 절대 경로를 사용할 수 있다.
이것은 필드명이 반복될 때에도
정확한 값을 출력하도록 보장한다.
예) 결과값 중에 많은 필드들이 `name`으로 명명되었을 경우,

```shell
kubectl get pods --all-namespaces -o jsonpath="{.items[*].spec.containers[*].image}"
```

이 jsonpath는 다음과 같이 해석할 수 있다.

- `.items[*]`: 각 결과값에 대하여
- `.spec`: spec 값을 가져온다.
- `.containers[*]`: 각 컨테이너에 대하여
- `.image`: image 값을 가져온다.

{{< note >}}
명령어로 하나의 파드를 가져올 때, 예를 들어 `kubectl get pod nginx` 라면,
jsonpath에서 `.items[*]` 부분은 생략해야 하는데, 이는 명령어가 아이템 목록이 아닌
단 한 개의 아이템(여기선 파드)으로 결과값을 주기 때문이다.
{{< /note >}}

## 각 파드의 컨테이너 이미지 보기

`range` 연산을 사용하여 명령어의 결과값에서 각각의 요소들을
반복하여 출력할 수 있다.

```shell
kubectl get pods --all-namespaces -o=jsonpath='{range .items[*]}{"\n"}{.metadata.name}{":\t"}{range .spec.containers[*]}{.image}{", "}{end}{end}' |\
sort
```

## 파드 레이블로 필터링된 컨테이너 이미지 목록 보기

특정 레이블에 맞는 파드를 지정하기 위해서 -l 플래그를 사용한다. 아래의
명령어 결과값은 `app=nginx` 레이블에 일치하는 파드만 출력한다.

```shell
kubectl get pods --all-namespaces -o=jsonpath="{.items[*].spec.containers[*].image}" -l app=nginx
```

## 파드 네임스페이스로 필터링된 컨테이너 이미지 목록 보기

특정 네임스페이스의 파드를 지정하려면, 네임스페이스 플래그를 사용한다.
아래의 명령어 결과값은 `kube-system` 네임스페이스에 있는 파드만 출력한다.

```shell
kubectl get pods --namespace kube-system -o jsonpath="{.items[*].spec.containers[*].image}"
```

## jsonpath 대신 Go 템플릿을 사용하여 컨테이너 이미지 목록 보기

jsonpath의 대안으로 Kubectl은 [Go 템플릿](https://golang.org/pkg/text/template/)을 지원한다.
다음과 같이 결과값의 서식을 지정할 수 있다.

```shell
kubectl get pods --all-namespaces -o go-template --template="{{range .items}}{{range .spec.containers}}{{.image}} {{end}}{{end}}"
```

## {{% heading "whatsnext" %}}

### 참조

* [Jsonpath](/ko/docs/reference/kubectl/jsonpath/) 참조
* [Go 템플릿](https://golang.org/pkg/text/template/) 참조
