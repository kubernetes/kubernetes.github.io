---
title: 노드(Node)
id: node
date: 2018-04-12
full_link: /ko/docs/concepts/architecture/nodes/
short_description: >
  노드는 쿠버네티스의 작업 장비(worker machine)이다.

aka:
tags:
- fundamental
---
 노드는 쿠버네티스의 작업 장비(worker machine)이다.

<!--more-->

작업 노드는 클러스터에 따라 VM이거나 물리 머신일 것이다. {{< glossary_tooltip text="파드" term_id="pod" >}} 실행에 필요한 로컬 데몬과 서비스를 가지고 있으며, 콘트롤 플레인에 의해서 관리된다. 노드에 있는 데몬은 {{< glossary_tooltip text="kubelet" term_id="kubelet" >}}, {{< glossary_tooltip text="kube-proxy" term_id="kube-proxy" >}}와 {{< glossary_tooltip term_id="docker" >}} 같이 컨테이너 런타임을 구현한 {{< glossary_tooltip text="CRI" term_id="cri" >}}를 포함한다.

초기 쿠버네티스 버전에서는 노드를 "미니언(Minions)"으로 불렀었다.