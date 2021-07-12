---
title: 파드 시큐리티 폴리시(Pod Security Policy)
id: pod-security-policy
date: 2018-04-12
full_link: /docs/concepts/policy/pod-security-policy/
short_description: >
  파드 생성과 업데이트에 대한 세밀한 인가를 활성화한다.

aka: 
tags:
- core-object
- fundamental
---
 {{< glossary_tooltip text="파드" term_id="pod" >}} 생성과 업데이트에 대한 세밀한 인가를 활성화한다.

<!--more--> 

파드 명세에서 보안에 민감한 측면을 제어하는 클러스터 수준의 리소스. `PodSecurityPolicy` 오브젝트는 파드가 시스템에 수용될 수 있도록 파드가 실행해야 하는 조건의 집합과 관련된 필드의 기본 값을 정의한다. 파드 시큐리티 폴리시 제어는 선택적인 어드미션 컨트롤러로서 구현된다.

