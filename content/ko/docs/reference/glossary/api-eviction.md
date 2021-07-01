---
title: API를 이용한 축출(Eviction)
id: api-eviction
date: 2021-04-27
full_link: /docs/concepts/scheduling-eviction/pod-eviction/#api-eviction
short_description: >
  API를 이용한 축출은 축출 API를 사용하여 파드의 정상 종료를 트리거하는
  축출 오브젝트를 만드는 프로세스이다
aka:
tags:
  - operation
---

API를 이용한 축출은 [축출 API](/docs/reference/generated/kubernetes-api/{{<param "version">}}/#create-eviction-pod-v1-core)를 사용하여
생성된 `Eviction` 오브젝트로 파드를 정상 종료한다.

<!--more-->

`kubectl drain` 명령과 같은 kube-apiserver의 클라이언트를 사용하여
축출 API를 직접 호출해 축출 요청을 할 수 있다.
`Eviction` 오브젝트가 생성되면, API 서버가 파드를 종료한다.

API를 이용한 축출은 [노드-압박 축출](/docs/concepts/scheduling-eviction/eviction/#kubelet-eviction)과 동일하지 않다.
