---
title: 서비스어카운트(ServiceAccount)
id: service-account
date: 2018-04-12
full_link: /docs/tasks/configure-pod-container/configure-service-account/
short_description: >
  파드에서 실행 중인 프로세스를 위한 신원(identity)을 제공한다.

aka:
tags:
- fundamental
- core-object
---
 {{< glossary_tooltip text="파드" term_id="pod" >}}에서 실행 중인 프로세스를 위한 신원(identity)을 제공한다.

<!--more-->

파드 내부의 프로세스가 클러스터에 엑세스할 때, API 서버에 의해서 특별한 서비스 어카운트(예를 들면, 기본(default))로 인증된다. 파드를 생성할 때, 서비스 어카운트를 명시하지 않는다면, 동일한 {{< glossary_tooltip text="네임스페이스" term_id="namespace" >}}의 기본 서비스 어카운트가 자동적으로 할당된다.

