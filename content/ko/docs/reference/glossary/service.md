---
title: 서비스(Service)
id: service
date: 2018-04-12
full_link: /docs/concepts/services-networking/service/
short_description: >
  네트워크 서비스로 파드 집합에서 실행 중인 애플리케이션을 노출하는 방법

aka: 
tags:
- fundamental
- core-object
---
{{< glossary_tooltip text="파드" term_id="pod" >}} 집합에서 실행중인 애플리케이션을 네트워크 서비스로 노출하는 추상화 방법

<!--more-->

서비스의 대상이 되는 파드 집합은 (보통) {{< glossary_tooltip text="셀렉터" term_id="selector" >}}로 결정된다. 많은 파드가 추가되거나 제거되면, 셀렉터와 일치하는 파드의 집합도 변경된다. 서비스는 네트워크 트래픽을 현재 워크로드를 위한 파드 집합으로 보낼 수 있는지 확인한다.
