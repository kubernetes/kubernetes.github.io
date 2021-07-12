---
title: "도구 설치"
description: 컴퓨터에서 쿠버네티스 도구를 설정한다.
weight: 10
no_list: true
---

## kubectl

<!-- overview -->
쿠버네티스 커맨드 라인 도구인 [`kubectl`](/ko/docs/reference/kubectl/kubectl/)을 사용하면 
쿠버네티스 클러스터에 대해 명령을 실행할 수 있다. 
`kubectl` 을 사용하여 애플리케이션을 배포하고, 클러스터 리소스를 검사 및 관리하고, 
로그를 볼 수 있다. kubectl 전체 명령어를 포함한 추가 정보는
[`kubectl` 레퍼런스 문서](/ko/docs/reference/kubectl/)에서 확인할 수 있다.

`kubectl` 은 다양한 리눅스 플랫폼, macOS, 그리고 윈도우에 설치할 수 있다.
각각에 대한 설치 가이드는 다음과 같다.

- [리눅스에 `kubectl` 설치하기](/ko/docs/tasks/tools/install-kubectl-linux/)
- [macOS에 `kubectl` 설치하기](/ko/docs/tasks/tools/install-kubectl-macos/)
- [윈도우에 `kubectl` 설치하기](/ko/docs/tasks/tools/install-kubectl-windows/)

## kind

[kind](https://kind.sigs.k8s.io/docs/)를 사용하면 로컬 컴퓨터에서
쿠버네티스를 실행할 수 있다. 이 도구를 사용하려면
[도커](https://docs.docker.com/get-docker/)를 설치하고 구성해야 한다.

kind [퀵 스타트](https://kind.sigs.k8s.io/docs/user/quick-start/) 페이지는
kind를 시작하고 실행하기 위해 수행해야 하는 작업을 보여준다.

<a class="btn btn-primary" href="https://kind.sigs.k8s.io/docs/user/quick-start/" role="button" aria-label="kind 시작하기 가이드 보기">kind 시작하기 가이드 보기</a>

## minikube

`kind` 와 마찬가지로, [`minikube`](https://minikube.sigs.k8s.io/)는 쿠버네티스를 로컬에서 실행할 수 있는
도구이다. `minikube` 는 개인용 컴퓨터(윈도우, macOS 및 리눅스 PC 포함)에서
단일 노드 쿠버네티스 클러스터를 실행하여 쿠버네티스를 사용해보거나 일상적인 개발 작업을
수행할 수 있다.

도구 설치에 중점을 두고 있다면 공식 사이트에서의
[시작하기!](https://minikube.sigs.k8s.io/docs/start/)
가이드를 따라 해볼 수 있다.

<a class="btn btn-primary" href="https://minikube.sigs.k8s.io/docs/start/" role="button" aria-label="minikube 시작하기! 가이드 보기">minikube 시작하기! 가이드 보기</a>

`minikube` 가 작동하면, 이를 사용하여
[샘플 애플리케이션을 실행](/ko/docs/tutorials/hello-minikube/)해볼 수 있다.

## kubeadm

{{< glossary_tooltip term_id="kubeadm" text="kubeadm" >}} 도구를 사용하여 쿠버네티스 클러스터를 만들고 관리할 수 있다.
사용자 친화적인 방식으로 최소한의 실행 가능하고 안전한 클러스터를 설정하고 실행하는 데 필요한 작업을 수행한다.

[kubeadm 설치](/ko/docs/setup/production-environment/tools/kubeadm/install-kubeadm/) 페이지는 kubeadm 설치하는 방법을 보여준다.
설치가 끝나면, [클러스터 생성](/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/)이 가능하다.

<a class="btn btn-primary" href="/ko/docs/setup/production-environment/tools/kubeadm/install-kubeadm/" role="button" aria-label="kubeadm 설치 가이드 보기">kubeadm 설치 가이드 보기</a>
