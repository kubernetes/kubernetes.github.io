---


title: 도구
content_type: concept
---

<!-- overview -->
쿠버네티스는 쿠버네티스 시스템으로 작업하는 데 도움이되는 몇 가지 기본 제공 도구를 포함한다.


<!-- body -->
## Kubectl

[`kubectl`](/ko/docs/tasks/tools/#kubectl)은 쿠버네티스를 위한 커맨드라인 툴이며, 쿠버네티스 클러스터 매니저을 제어한다.

## Kubeadm

[`kubeadm`](/ko/docs/setup/production-environment/tools/kubeadm/install-kubeadm/)은 물리적 환경, 클라우드 서버, 또는 가상머신 상에서 안전한 쿠버네티스를 쉽게 프로비저닝하기 위한 커맨드라인 툴이다(현재는 알파 상태).

## Minikube

[`minikube`](https://minikube.sigs.k8s.io/docs/)는 개발과 테스팅 목적으로
단일 노드 쿠버네티스 클러스터를 로컬 워크스테이션에서
실행하는 도구이다.

## 대시보드

[`대시보드`](/ko/docs/tasks/access-application-cluster/web-ui-dashboard/), 는 쿠버네티스의 웹기반 유저 인터페이스이며 컨테이너화된 애플리케이션을 쿠버네티스 클러스터로 배포하고
클러스터 및 클러스터 자원의 문제를 해결하며 관리할 수 있게 해준다.

## Helm

[`쿠버네티스 Helm`](https://github.com/kubernetes/helm)은 사전 구성된 쿠버네티스 리소스를 관리하기위한 도구이며
또한 Helm의 쿠버네티스 차트라고도 한다.

Helm의 용도

* 쿠버네티스 차트로 배포된 인기있는 소프트웨어를 검색하고 사용
* 쿠버네티스 차트로 나의 애플리케이션을 공유
* 쿠버네티스 애플리케이션의 반복가능한 빌드 및 생성
* 매니페스트 파일의 지능화된 관리
* Helm 패키지의 릴리스 관리

## Kompose

[`Kompose`](https://github.com/kubernetes/kompose)는 도커 컴포즈 유저들이 쿠버네티스로 이동하는데 도움이 되는 도구이다.

Kompose의 용도

* 도커 컴포즈 파일을 쿠버네티스 오브젝트로 변환
* 로컬 도커 개발 환경에서 나의 애플리케이션을 쿠버네티스를 통해 관리하도록 이전
* V1 또는 V2 도커 컴포즈 `yaml` 파일 또는 [분산 애플리케이션 번들](https://docs.docker.com/compose/bundles/)을 변환
