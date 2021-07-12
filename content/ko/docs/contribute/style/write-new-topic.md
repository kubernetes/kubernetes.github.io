---
title: 새로운 주제의 문서 작성
content_type: task
weight: 20
---

<!-- overview -->
이 페이지는 쿠버네티스 문서에서 새로운 주제를 생성하는 방법을 보여준다.


## {{% heading "prerequisites" %}}

[PR 열기](/ko/docs/contribute/new-content/open-a-pr/)에 설명된 대로 쿠버네티스
문서 저장소의 포크(fork)를 생성하자.


<!-- steps -->

## 페이지 타입 선택

새로운 주제 작성을 준비할 때는, 콘텐츠에 가장 적합한 페이지 타입을 고려하자.

{{< table caption = "페이지 타입 선택 지침" >}}
타입 | 설명
:--- | :----------
개념 | 개념 페이지는 쿠버네티스의 일부 측면을 설명한다. 예를 들어 개념 페이지는 쿠버네티스 디플로이먼트 오브젝트를 설명하고 배치, 확장 및 업데이트되는 동안 애플리케이션으로서 수행하는 역할을 설명할 수 있다. 일반적으로 개념 페이지는 일련의 단계가 포함되지 않지만 대신 태스크나 튜토리얼에 대한 링크를 제공한다. 개념 문서의 예로서 <a href="/ko/docs/concepts/architecture/nodes/">노드</a>를 참조하자.
태스크 | 태스크 페이지는 단일 작업을 수행하는 방법을 보여준다. 아이디어는 독자가 페이지를 읽을 때 실제로 수행할 수 있는 일련의 단계를 제공하는 것이다. 태스크 페이지는 한 영역에 집중되어 있으면 짧거나 길 수 있다. 태스크 페이지에서 수행할 단계와 간단한 설명을 혼합하는 것은 괜찮지만, 긴 설명을 제공해야 하는 경우에는 개념 문서에서 수행해야 한다. 관련 태스크와 개념 문서는 서로 연결되어야 한다. 짧은 태스크 페이지의 예제는 <a href="/docs/tasks/configure-pod-container/configure-volume-storage/">저장소에 볼륨을 사용하도록 파드 구성</a>을 참조하자. 더 긴 태스크 페이지의 예제는 <a href="/docs/tasks/configure-pod-container/configure-liveness-readiness-probes/">활동성 및 준비성 프로브 구성</a>을 참조하자.
튜토리얼 | 튜토리얼 페이지는 여러 쿠버네티스의 특징들을 하나로 묶어서 목적을 달성하는 방법을 보여준다. 튜토리얼은 독자들이 페이지를 읽을 때 실제로 할 수 있는 몇 가지 단계의 순서를 제공한다. 또는 관련 코드 일부에 대한 설명을 제공할 수도 있다. 예를 들어 튜토리얼은 코드 샘플의 연습을 제공할 수 있다. 튜토리얼에는 쿠버네티스의 특징에 대한 간략한 설명이 포함될 수 있지만 개별 기능에 대한 자세한 설명은 관련 개념 문서과 연결지어야 한다.
{{< /table >}}

### 새 페이지 작성

작성하는 각각의 새 페이지에 대해 [콘텐츠 타입](/docs/contribute/style/page-content-types/)을
사용하자. 문서 사이트는 새 콘텐츠 페이지를 작성하기 위한 템플리트 또는
[Hugo archetypes](https://gohugo.io/content-management/archetypes/)을
제공한다. 새로운 타입의 페이지를 작성하려면, 작성하려는 파일의 경로로 `hugo new` 를
실행한다. 예를 들면, 다음과 같다.

```
hugo new docs/concepts/my-first-concept.md
```

## 제목과 파일 이름 선택

검색 엔진에서 찾을 키워드가 있는 제목을 선택하자.
제목에 있는 단어를 하이픈으로 구분하여 사용하는 파일 이름을 만들자.
예를 들어
[HTTP 프록시를 사용하여 쿠버네티스 API에 접근](/docs/tasks/extend-kubernetes/http-proxy-access-api/)
이라는 제목의 문서는 `http-proxy-access-api.md`라는 이름의 파일을 가진다.
"쿠버네티스"가 이미 해당 주제의 URL에 있기 때문에 파일 이름에 "쿠버네티스" 를 넣을 필요가 없다.
예를 들면 다음과 같다.

       /docs/tasks/extend-kubernetes/http-proxy-access-api/

## 전문에 항목 제목 추가

문서에서 [전문](https://gohugo.io/content-management/front-matter/)
에 `title` 필드를 입력하자.
전문은 페이지 상단의 3중 점선 사이에 있는
YAML 블록이다. 여기 예시가 있다.

    ---
    title: HTTP 프록시를 사용하여 쿠버네티스 API에 접근
    ---

## 디렉터리 선택

페이지 타입에 따라 새로운 파일을 다음 중 하나의 하위 디렉터리에 넣자.

* /content/en/docs/tasks/
* /content/en/docs/tutorials/
* /content/en/docs/concepts/

파일을 기존 하위 디렉터리에 넣거나 새 하위 디렉터리에
넣을 수 있다.

## 목차에 항목 배치

목차는 문서 소스의 디렉터리 구조를 사용하여
동적으로 작성된다. `/content/en/docs/` 아래의 최상위 디렉터리는 최상위 레벨 탐색 기능을
생성하고, 하위 디렉터리는 각각 목차에 항목을
갖는다.

각 하위 디렉터리에는 `_index.md` 파일이 있으며 이는 해당 하위 디렉터리의 컨텐츠에 대한
"홈" 페이지를 나타낸다. `_index.md`에는 템플릿이 필요없다. 그것은
하위 디렉터리의 항목에 대한 개요 내용을 포함할 수 있다.

디렉터리의 다른 파일들은 기본적으로 알파벳순으로 정렬된다. 이것은 거의
최적의 순서가 아니다. 하위 디렉터리에서 항목의 상대적 정렬을 제어하려면
`가중치:` 전문의 키를 정수로 설정하자. 일반적으로 우리는
나중에 항목을 추가하기 위해 10의 배수를 사용한다. 예를 들어 가중치가
`10`인 항목은 가중치가 `20`인 항목보다 우선한다.

## 문서에 코드 포함

문서에 코드를 포함시키려면 마크다운 코드 블록 구문을 사용하여
파일에 코드를 직접 삽입하자. 다음 경우에
권장된다. (전체 목록은 아님)

- 이 코드는 `kubectl get deploy mydeployment -o json | jq '.status'`와 같은
  명령어의 출력을 보여준다.
- 이 코드는 시도해보기에 적절하지 않다. 예를 들어
  특정 [FlexVolume](/ko/docs/concepts/storage/volumes#flexvolume) 구현에 따라
  파드를 만들기 위해 YAML 파일을
  포함할 수 있다.
- 이 코드의 목적은 더 큰 파일의 일부를 강조하는 것이기 때문에
  불완전한 예제다. 예를 들어 몇 가지 이유로
  [PodSecurityPolicy](/docs/tasks/administer-cluster/sysctl-cluster/#podsecuritypolicy)
  를 사용자 정의 방법을 설명할 때 문서 파일에서 직접 짧은 요약 정보를 제공할 수 있다.
- 이 코드는 사용자가 다른 이유로 시도하기 위한 것이 아니다. 예를 들어
  `kubectl edit` 명령을 사용하여 리소스에 새 속성을 추가하는 방법을
  설명할 때 추가할 만한 속성을 포함하는
  간단한 예를 제공할 수 있다.

## 다른 파일의 코드 포함

문서에 코드를 포함시키는 또 다른 방법은 새로운 완전한 샘플 파일
(또는 샘플 파일 그룹)을 만든 다음 문서의 샘플을 참조하는 것이다.
일반적이고 재사용 가능하며 독자가 스스로 실행해 볼 수 있도록 하는
샘플 YAML 파일을 포함시키려면 이 방법을 사용하자.

YAML 파일과 같은 새로운 독립형 샘플 파일을 추가할 때
`<LANG>/examples/` 의 하위 디렉터리 중 하나에 코드를 배치하자. 여기서 `<LANG>`은
주제에 관한 언어이다. 문서 파일에서 `codenew` 단축 코드(shortcode)를 사용하자.

```none
{{</* codenew file="<RELPATH>/my-example-yaml>" */>}}
```
여기서 `<RELPATH>` 는 `examples` 디렉터리와 관련하여 포함될
파일의 경로이다. 다음 Hugo 단축 코드(shortcode)는 `/content/en/examples/pods/storage/gce-volume.yaml`
에 있는 YAML 파일을 참조한다.

```none
{{</* codenew file="pods/storage/gce-volume.yaml" */>}}
```

{{< note >}}
위의 예와 같은 원시 Hugo 단축 코드(shortcode)를 표시하고 Hugo가
해석하지 못하게 하려면 `<` 문자 바로 다음과 `>` 문자 앞에 C 스타일 주석을 사용하자.
그 예로서 이 페이지의 코드를 확인하자.
{{< /note >}}

## 구성 파일에서 API 오브젝트를 작성하는 방법 표시

구성 파일을 기반으로 API 오브젝트를 생성하는 방법을 보여주려면
`<LANG>/examples` 아래의 하위 디렉터리 중 하나에
구성 파일을 배치하자.

문서에서 이 명령을 띄워보자.

```
kubectl create -f https://k8s.io/examples/pods/storage/gce-volume.yaml
```

{{< note >}}
`<LANG>/examples` 디렉터리에 새 YAMl 파일을 추가할 때 파일이
`<LANG>/examples_test.go` 파일에도 포함되어 있는지 확인하자.
웹 사이트의 Travis CI 는 PR이 제출될 때 이 예제를 자동으로
실행하여 모든 예제가 테스트를 통과하도록 한다.
{{< /note >}}

이 기술을 사용하는 문서의 예로
[단일 인스턴스 스테이트풀 어플리케이션 실행](/ko/docs/tasks/run-application/run-single-instance-stateful-application/)을 참조하자.

## 문서에 이미지 추가

이미지 파일을 `/images` 디렉터리에 넣는다. 기본
이미지 형식은 SVG 이다.



## {{% heading "whatsnext" %}}

* [페이지 콘텐츠 타입 사용](/docs/contribute/style/page-content-types/)에 대해 알아보기.
* [풀 리퀘스트 작성](/ko/docs/contribute/new-content/open-a-pr/)에 대해 알아보기.
