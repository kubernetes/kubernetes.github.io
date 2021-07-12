---
title: 컨테이너
weight: 40
description: 런타임 의존성과 함께 애플리케이션을 패키징하는 기술
content_type: concept
no_list: true
---

<!-- overview -->

실행하는 각 컨테이너는 반복 가능하다. 의존성이 포함된 표준화는
어디에서 실행하던지 동일한 동작을 얻는다는 것을
의미한다.

컨테이너는 기본 호스트 인프라에서 애플리케이션을 분리한다.
따라서 다양한 클라우드 또는 OS 환경에서 보다 쉽게 ​​배포할 수 있다.




<!-- body -->

## 컨테이너 이미지
[컨테이너 이미지](/ko/docs/concepts/containers/images/)는 애플리케이션을
실행하는 데 필요한 모든 것이 포함된 실행할 준비가 되어있는(ready-to-run) 소프트웨어 패키지이다.
여기에는 실행하는 데 필요한 코드와 모든 런타임, 애플리케이션 및 시스템 라이브러리,
그리고 모든 필수 설정에 대한 기본값이 포함된다.

설계 상, 컨테이너는 변경할 수 없다. 이미 실행 중인 컨테이너의 코드를
변경할 수 없다. 컨테이너화된 애플리케이션이 있고
변경하려는 경우, 변경 사항이 포함된 새 이미지를 빌드한
다음, 업데이트된 이미지에서 시작하도록 컨테이너를 다시 생성해야 한다.

## 컨테이너 런타임

{{< glossary_definition term_id="container-runtime" length="all" >}}

## {{% heading "whatsnext" %}}

* [컨테이너 이미지](/ko/docs/concepts/containers/images/)에 대해 읽어보기
* [파드](/ko/docs/concepts/workloads/pods/)에 대해 읽어보기
