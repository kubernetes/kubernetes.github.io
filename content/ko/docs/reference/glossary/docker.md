---
title: 도커(Docker)
id: docker
date: 2018-04-12
full_link: https://docs.docker.com/engine/
short_description: >
  Docker는 운영 시스템 수준의 가상화를 제공하는 소프트웨어 기술이며, 컨테이너로도 알려져 있다.

aka:
tags:
- fundamental
---
도커(구체적으로, 도커 엔진)는 운영 시스템 수준의 가상화를 제공하는 소프트웨어 기술이며, {{< glossary_tooltip text="containers" term_id="container" >}} 로도 알려져 있다.

<!--more-->

Docker는 리눅스 커널의 리소스 격리 기능을 사용하며, 그 격리 기능의 예는 cgroups, 커널 네임스페이스, OverlayFS와 같은 조합 가능한 파일 시스템, 컨테이너가 단일 리눅스 인스턴스에서 독립적으로 실행되게 하여 가상 머신(VM)을 시작하고 관리하는 오버헤드를 피할 수 있도록 하는 기타 기능 등이 있다. 

