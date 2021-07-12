---
title: 레플리카셋(ReplicaSet)
id: replica-set
date: 2018-04-12
full_link: /ko/docs/concepts/workloads/controllers/replicaset/
short_description: >
  레플리카셋은 지정된 수의 파드 레플리카가 동시에 실행이 되도록 보장한다

aka: 
tags:
- fundamental
- core-object
- workload
---
 레플리카셋은 (목표로) 주어진 시간에 실행되는 레플리카 파드 셋을 유지 관리 한다.

<!--more--> 

{{< glossary_tooltip term_id="deployment" >}} 와 같은 워크로드 오브젝트는 레플리카셋을
사용해서 해당 레플리카셋의 스펙에 따라 구성된 {{< glossary_tooltip term_id="pod" text="파드" >}} 의
수를 클러스터에서 실행한다.
