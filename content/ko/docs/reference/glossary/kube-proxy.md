---
title: kube-proxy
id: kube-proxy
date: 2018-04-12
full_link: /docs/reference/command-line-tools-reference/kube-proxy/
short_description: >
  `kube-proxy`는 클러스터의 각 노드에서 실행되는 네트워크 프록시이다.

aka:
tags:
- fundamental
- networking
---
 kube-proxy는 클러스터의 각
 {{< glossary_tooltip text="노드" term_id="node" >}}에서
 실행되는 네트워크 프록시로, 쿠버네티스의
 {{< glossary_tooltip text="서비스" term_id="service">}} 개념의 구현부이다.

<!--more-->

[kube-proxy](/ko/docs/reference/command-line-tools-reference/kube-proxy/)는
노드의 네트워크 규칙을 유지 관리한다. 이 네트워크 규칙이 내부 네트워크
세션이나 클러스터 바깥에서 파드로 네트워크 통신을
할 수 있도록 해준다.

kube-proxy는 운영 체제에 가용한 패킷
필터링 계층이 있는 경우, 이를 사용한다. 그렇지 않으면, kube-proxy는 트래픽 자체를 포워드(forward)한다.
