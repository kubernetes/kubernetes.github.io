---
title: 파드(Pod)
id: pod
date: 2018-04-12
full_link: /ko/docs/concepts/workloads/pods/
short_description: >
  파드는 클러스터에서 실행 중인 컨테이너의 집합을 나타낸다.

aka:
tags:
- core-object
- fundamental
---
 가장 작고 단순한 쿠버네티스 오브젝트. 파드는 사용자 클러스터에서 동작하는 {{< glossary_tooltip text="컨테이너" term_id="container" >}}의 집합을 나타낸다.

<!--more-->

파드는 일반적으로 하나의 기본 컨테이너를 실행하기 위해서 구성된다. 또한 파드는 로깅과 같이 보완적인 기능을 추가하기 위한 사이드카 컨테이너를 선택적으로 실행할 수 있다. 파드는 보통 {{< glossary_tooltip text="디플로이먼트" term_id="deployment" >}}에 의해서 관리된다.
