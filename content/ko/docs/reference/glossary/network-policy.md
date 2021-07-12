---
title: 네트워크 폴리시(Network Policy)
id: network-policy
date: 2018-04-12
full_link: /docs/concepts/services-networking/network-policies/
short_description: >
  파드 그룹들이 서로에 대한 그리고 다른 네트워크 엔드포인트에 대한 통신이 어떻게 허용되는지에 대한 명세이다.

aka: 
tags:
- networking
- architecture
- extension
---
 파드 그룹들이 서로에 대한 그리고 다른 네트워크 엔드포인트에 대한 통신이 어떻게 허용되는지에 대한 명세이다. 

<!--more--> 

네트워크 폴리시는 어떤 파드들의 연결을 서로 허용할지, 어떤 네임스페이스가 통신 가능하도록 허용할지, 더 상세하게는 어떤 포트 번호에 각 정책을 시행할지도 선언적으로 구성할 수 있게 도와준다. `NetworkPolicy` 리소스는 파드를 선택하고 선택된 파드에 어떤 트래픽을 허용할지 명시하는 규칙을 정의하기 위해서 레이블을 사용한다. 네트워크 폴리시는 네트워크 프로바이더에 의해 제공되는 네트워크 플러그인 지원에 의해 구현된다. 네트워크 리소스를 그것을 구현하는 컨트롤러 없이 생성하는 것은 아무런 효과가 없음을 주의하기 바란다.

