---
title: RBAC(역할 기반 엑세스 제어)
id: rbac
date: 2018-04-12
full_link: /docs/reference/access-authn-authz/rbac/
short_description: >
  인가 결정을 관리하며, 운영자가 쿠버네티스 API를 통해서 동적으로 엑세스 정책을 설정하게 한다.

aka: 
tags:
- security
- fundamental
---
 인가 결정을 관리하며, 운영자가 {{< glossary_tooltip text="쿠버네티스 API" term_id="kubernetes-api" >}}를 통해서 동적으로 엑세스 정책을 설정하게 해준다.

<!--more--> 

RBAC은 퍼미션(permission) 규칙을 포함하는 *역할* 과 역할에 정의된 퍼미션을 사용자 집합에 부여하는 *역할 바인딩* 을 이용한다.

