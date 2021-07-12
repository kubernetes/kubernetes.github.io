---
title: QoS 클래스(QoS Class)
id: qos-class
date: 2019-04-15
full_link:
short_description: >
  QoS 클래스(서비스 품질 클래스)는 쿠버네티스가 클러스터 안의 파드들을 여러 클래스로 구분하고, 스케줄링과 축출(eviction)에 대한 결정을 내리는 방법을 제공한다.

aka:
tags:
- core-object
- fundamental
- architecture
related:
- pod

---
  QoS 클래스(서비스 품질 클래스)는 쿠버네티스가 클러스터 안의 파드들을 여러 클래스로 구분하고, 스케줄링과 축출(eviction)에 대한 결정을 내리는 방법을 제공한다.

<!--more-->
파드의 QoS 클래스는 생성 시점의 컴퓨팅 리소스 요청량과 제한 값에 기반해서 설정된다. QoS 클래스는 파드의 스케줄링과 축출을 위한 결정을 내릴 때 사용된다.
쿠버네티스는 파드에 `Guaranteed`, `Burstable` 또는 `BestEffort` 중 하나를 QoS 클래스로 할당할 수 있다.
