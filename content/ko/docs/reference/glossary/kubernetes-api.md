---
title: 쿠버네티스 API(Kubernetes API)
id: kubernetes-api
date: 2018-04-12
full_link: /ko/docs/concepts/overview/kubernetes-api/
short_description: >
  RESTful 인터페이스를 통해서 쿠버네티스 기능을 제공하고 클러스터의 상태를 저장하는 애플리케이션.

aka: 
tags:
- fundamental
- architecture
---
 RESTful 인터페이스를 통해서 쿠버네티스 기능을 제공하고 클러스터의 상태를 저장하는 애플리케이션.

<!--more--> 

쿠버네티스 리소스와 "의도에 대한 레코드"는 모두 API 오브젝트로 저장되며, API로의 RESTful 호출을 통해서 수정된다. API는 구성이 선언적인 방법으로 관리되도록 한다. 사용자는 쿠버네티스 API와 직접 상호 작용할 수 있으며, `kubectl`과 같은 툴을 사용할 수도 있다. 쿠버네티스 API의 핵심은 유연하며 사용자 정의 리소스를 지원하기 위해 확장될 수도 있다.

