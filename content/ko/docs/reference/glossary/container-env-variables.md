---
title: 컨테이너 환경 변수(Container Environment Variables)
id: container-env-variables
date: 2018-04-12
full_link: /ko/docs/concepts/containers/container-environment/
short_description: >
  컨테이너 환경 변수는 파드에서 동작 중인 컨테이너에 유용한 정보를 제공하기 위한 이름=값 쌍이다.

aka:
tags:
- fundamental
---
 컨테이너 환경 변수는 {{< glossary_tooltip text="파드" term_id="pod" >}}에서 동작 중인 컨테이너에 유용한 정보를 제공하기 위한 이름=값 쌍이다.

<!--more-->

컨테이너 환경 변수는 중요한 리소스에 대한 정보와 함께 실행 중인 컨테이너화 된 애플리케이션이 요구하는 정보를 해당 {{< glossary_tooltip text="컨테이너" term_id="container" >}}에 제공한다. 예를 들면, 파일 시스템 상세 정보, 컨테이너 스스로에 대한 정보, 서비스 엔드포인트와 같은 다른 클러스터 리소스에 대한 정보 등이 있다.