---
title: 쿠버네티스 API 활성화 혹은 비활성화하기
content_type: task
---

<!-- overview -->
이 페이지는 클러스터 {{< glossary_tooltip text="컨트롤 플레인" term_id="control-plane" >}}의
특정한 API 버전을 활성화하거나 비활성화하는 방법에 대해 설명한다.

<!-- steps -->


API 서버에 `--runtime-config=api/<version>` 커맨드 라인 인자를 사용함으로서 특정한 API 버전을 
활성화하거나 비활성화할 수 있다. 이 인자에 대한 값으로는 콤마로 구분된 API 버전의 목록을 사용한다.
뒤쪽에 위치한 값은 앞쪽의 값보다 우선적으로 사용된다.

이 `runtime-config` 커맨드 라인 인자에는 다음의 두 개의 특수 키를 사용할 수도 있다.

- `api/all`: 사용할 수 있는 모든 API를 선택한다.
- `api/legacy`: 레거시 API만을 선택한다. 여기서 레거시 API란 명시적으로
   [사용이 중단된](/docs/reference/using-api/deprecation-policy/) 모든 API를 가리킨다.

예를 들어서, v1을 제외한 모든 API 버전을 비활성화하기 위해서는 `kube-apiserver`에 
`--runtime-config=api/all=false,api/v1=true` 인자를 사용한다.

## {{% heading "whatsnext" %}}

`kube-apiserver` 컴포넌트에 대한 더 자세한 내용은 다음의 [문서](/docs/reference/command-line-tools-reference/kube-apiserver/)
를 참고한다.
