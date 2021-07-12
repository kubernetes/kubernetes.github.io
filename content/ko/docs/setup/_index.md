---




title: 시작하기
main_menu: true
weight: 20
content_type: concept
no_list: true
card:
  name: setup
  weight: 20
  anchors:
  - anchor: "#학습-환경"
    title: 학습 환경
  - anchor: "#프로덕션-환경"
    title: 프로덕션 환경
---

<!-- overview -->

본 섹션에는 쿠버네티스를 설정하고 실행하는 다양한 방법이 나열되어 있다.
쿠버네티스를 설치할 때는 유지보수의 용이성, 보안, 제어, 사용 가능한 리소스, 그리고
클러스터를 운영하고 관리하기 위해 필요한 전문성을 기반으로 설치 유형을 선택한다.

[쿠버네티스를 다운로드](/releases/download/)하여 
로컬 머신에, 클라우드에, 데이터센터에 쿠버네티스 클러스터를 구축할 수 있다.

쿠버네티스 클러스터를 직접 관리하고 싶지 않다면, [인증된 플랫폼](/ko/docs/setup/production-environment/turnkey-solutions/)과 
같은 매니지드 서비스를 선택할 수도 있다.
광범위한 클라우드 또는 베어 메탈 환경에 걸쳐 사용할 수 있는 
표준화된/맞춤형 솔루션도 있다.

<!-- body -->

## 학습 환경

쿠버네티스를 배우고 있다면, 쿠버네티스 커뮤니티에서 지원하는 도구나, 
로컬 머신에서 쿠버네티스를 설치하기 위한 생태계 내의 도구를 사용한다.
[도구 설치](/ko/docs/tasks/tools/)를 살펴본다.

## 프로덕션 환경

[프로덕션 환경](/ko/docs/setup/production-environment/)을 위한 
솔루션을 평가할 때에는, 쿠버네티스 클러스터(또는 _추상화된 객체_) 
운영에 대한 어떤 측면을 스스로 관리하기를 원하는지, 
또는 제공자에게 넘기기를 원하는지 고려한다.

클러스터를 직접 관리하는 경우, 공식적으로 지원되는 쿠버네티스 구축 도구는 
[kubeadm](/ko/docs/setup/production-environment/tools/kubeadm/)이다.

## {{% heading "whatsnext" %}}

- [쿠버네티스를 다운로드](/releases/download/)한다.
- `kubectl`을 포함한 [도구를 설치](/ko/docs/tasks/tools/)한다.
- 새로운 클러스터에 사용할 [컨테이너 런타임](/ko/docs/setup/production-environment/container-runtimes/)을 선택한다.
- 클러스터 구성의 [모범 사례](/ko/docs/setup/best-practices/)를 확인한다.

쿠버네티스의 {{< glossary_tooltip term_id="control-plane" text="컨트롤 플레인" >}}은 
리눅스에서 실행되어야 한다. 클러스터 내에서는 리눅스 또는 
다른 운영 체제(예: 윈도우)에서 애플리케이션을 실행할 수 있다.
- [윈도우 노드를 포함하는 클러스터 구성하기](/ko/docs/setup/production-environment/windows/)를 살펴본다.
