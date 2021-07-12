---
title: "스케줄링, 선점(Preemption), 축출(Eviction)"
weight: 90
content_type: concept
description: >
  쿠버네티스에서, 스케줄링은 kubelet이 파드를 실행할 수 있도록 
  파드를 노드에 할당하는 것을 말한다.
  선점은 우선순위가 높은 파드가 노드에 스케줄될 수 있도록 
  우선순위가 낮은 파드를 종료시키는 과정을 말한다.
  축출은 리소스가 부족한 노드에서 하나 이상의 파드를 사전에 종료시키는 프로세스이다.
no_list: true
---

쿠버네티스에서, 스케줄링은 {{<glossary_tooltip text="kubelet" term_id="kubelet">}}이 파드를 실행할 수 있도록 
{{<glossary_tooltip text="파드" term_id="pod">}}를 
{{<glossary_tooltip text="노드" term_id="node">}}에 할당하는 것을 말한다.
선점은 {{<glossary_tooltip text="우선순위" term_id="pod-priority">}}가 높은 파드가 노드에 스케줄될 수 있도록 
우선순위가 낮은 파드를 종료시키는 과정을 말한다.
축출은 리소스가 부족한 노드에서 하나 이상의 파드를 사전에 종료시키는 프로세스이다.

## 스케줄링

* [쿠버네티스 스케줄러](/ko/docs/concepts/scheduling-eviction/kube-scheduler/)
* [노드에 파드 할당하기](/ko/docs/concepts/scheduling-eviction/assign-pod-node/)
* [파드 오버헤드](/ko/docs/concepts/scheduling-eviction/pod-overhead/)
* [테인트(Taints)와 톨러레이션(Tolerations)](/ko/docs/concepts/scheduling-eviction/taint-and-toleration/)
* [스케줄링 프레임워크](/docs/concepts/scheduling-eviction/scheduling-framework/)
* [스케줄러 성능 튜닝](/ko/docs/concepts/scheduling-eviction/scheduler-perf-tuning/)
* [확장된 리소스를 위한 리소스 빈 패킹(bin packing)](/ko/docs/concepts/scheduling-eviction/resource-bin-packing/)

## 파드 중단(disruption)

{{<glossary_definition term_id="pod-disruption" length="all">}}

* [파드 우선순위와 선점](/ko/docs/concepts/scheduling-eviction/pod-priority-preemption/)
* [노드-압박 축출](/docs/concepts/scheduling-eviction/node-pressure-eviction/)
* [API를 이용한 축출](/ko/docs/concepts/scheduling-eviction/api-eviction/)
