---
title: 데몬셋(DaemonSet)
id: daemonset
date: 2018-04-12
full_link: /ko/docs/concepts/workloads/controllers/daemonset
short_description: >
  파드의 복제본을 클러스터 노드 집합에서 동작하게 한다.

aka:
tags:
- fundamental
- core-object
- workload
---
 {{< glossary_tooltip text="파드" term_id="pod" >}} 복제본을 {{< glossary_tooltip text="클러스터" term_id="cluster" >}} 노드 집합에서 동작하게 한다.

<!--more-->

일반적으로 모든 {{< glossary_tooltip text="노드" term_id="node" >}}에서 실행돼야 하는 로그 수집기 및 모니터링 에이전트 등의 시스템 데몬을 배포하기 위해서 사용된다.

