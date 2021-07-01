---



title: 노드 리소스 매니저 
content_type: 개념
weight: 50
---

<!-- overview -->

쿠버네티스는 지연 시간에 민감하고 처리량이 많은 워크로드를 지원하기 위해 리소스 매니저 세트를 제공한다. 매니저는 CPU, 장치 및 메모리 (hugepages) 리소스와 같은 특정한 요구 사항으로 구성된 파드를 위해 노드의 리소스 할당을 조정하고 최적화하는 것을 목표로 한다. 

<!-- body -->

주 매니저인 토폴로지 매니저는 [정책](/docs/tasks/administer-cluster/topology-manager/)을 통해 전체 리소스 관리 프로세스를 조정하는 Kubelet 컴포넌트이다.

개별 매니저의 구성은 다음의 문서에 자세히 기술되어 있다.

- [CPU 관리 정책](/docs/tasks/administer-cluster/cpu-management-policies/)
- [장치 매니저](/ko/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/#토폴로지-관리자와-장치-플러그인-통합)
- [메모리 관리 정책](/docs/tasks/administer-cluster/memory-manager/)
