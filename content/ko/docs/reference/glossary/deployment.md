---
title: 디플로이먼트(Deployment)
id: deployment
date: 2018-04-12
full_link: /ko/docs/concepts/workloads/controllers/deployment/
short_description: >
  클러스터에서 복제된 애플리케이션을 관리한다.

aka:
tags:
- fundamental
- core-object
- workload
---
 일반적으로 로컬 상태가 없는 파드를 실행하여 복제된 애플리케이션을 관리하는 API 오브젝트.

<!--more-->

각 레플리카는 {{< glossary_tooltip text="파드" term_id="pod" >}}로 표현되며,
파드는 클러스터의 {{< glossary_tooltip text="노드" term_id="node" >}}에 분산된다.
로컬 상태가 필요한 워크로드의 경우 {{< glossary_tooltip term_id="StatefulSet" >}}의 사용을 고려한다.