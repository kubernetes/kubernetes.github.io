---
title: 클러스터(Cluster)
id: cluster
date: 2019-06-15
full_link:
short_description: >
   컨테이너화된 애플리케이션을 실행하는 노드라고 하는 워커 머신의 집합. 모든 클러스터는 최소 한 개의 워커 노드를 가진다.

aka:
tags:
- fundamental
- operation
---
컨테이너화된 애플리케이션을 실행하는 {{< glossary_tooltip text="노드" term_id="node" >}}라고
하는 워커 머신의 집합. 모든 클러스터는 최소 한 개의 워커 노드를 가진다.

<!--more-->
워커 노드는 애플리케이션의 구성요소인
{{< glossary_tooltip text="파드" term_id="pod" >}}를 호스트한다.
{{< glossary_tooltip text="컨트롤 플레인" term_id="control-plane" >}}은 워커 노드와
클러스터 내 파드를 관리한다. 프로덕션 환경에서는 일반적으로 컨트롤 플레인이
여러 컴퓨터에 걸쳐 실행되고, 클러스터는 일반적으로 여러 노드를
실행하므로 내결함성과 고가용성이 제공된다.
