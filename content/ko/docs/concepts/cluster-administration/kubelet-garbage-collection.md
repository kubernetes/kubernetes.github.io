---
title: kubelet 가비지(Garbage) 수집 설정하기
content_type: concept
weight: 70
---

<!-- overview -->

가비지 수집은 사용되지 않는 
[이미지](/ko/docs/concepts/containers/#컨테이너-이미지)들과 
[컨테이너](/ko/docs/concepts/containers/)들을 정리하는 kubelet의 유용한 기능이다. Kubelet은 
1분마다 컨테이너들에 대하여 가비지 수집을 수행하며, 5분마다 이미지들에 대하여 가비지 수집을 수행한다.

별도의 가비지 수집 도구들을 사용하는 것은, 이러한 도구들이 존재할 수도 있는 컨테이너들을 제거함으로써 
kubelet을 중단시킬 수도 있으므로 권장하지 않는다.

<!-- body -->

## 이미지 수집

쿠버네티스는 cadvisor와 imageManager를 통하여 모든 이미지들의
라이프사이클을 관리한다.

이미지들에 대한 가비지 수집 정책은 다음의 2가지 요소를 고려한다.
`HighThresholdPercent` 와 `LowThresholdPercent`. 임계값을 초과하는
디스크 사용량은 가비지 수집을 트리거 한다. 가비지 수집은 낮은 입계값에 도달 할 때까지 최근에 가장 적게 사용한
이미지들을 삭제한다.

## 컨테이너 수집

컨테이너에 대한 가비지 수집 정책은 세 가지 사용자 정의 변수들을 고려한다. 
`MinAge` 는 컨테이너를 가비지 수집할 수 있는 최소 연령이다. 
`MaxPerPodContainer` 는 모든 단일 파드(UID, 컨테이너 이름) 
쌍이 가질 수 있는 최대 비활성 컨테이너의 수량이다. 
`MaxContainers` 는 죽은 컨테이너의 최대 수량이다. 
이러한 변수는 `MinAge` 를 0으로 설정하고, 
`MaxPerPodContainer` 와 `MaxContainers` 를 각각 0 보다 작게 설정해서 비활성화할 수 있다.

Kubelet은 미확인, 삭제 또는 앞에서 언급한 
플래그가 설정한 경계를 벗어나거나, 확인되지 않은 컨테이너에 대해 조치를 취한다. 
일반적으로 가장 오래된 컨테이너가 먼저 제거된다. `MaxPerPodContainer` 와 `MaxContainer` 는 
파드 당 최대 
컨테이너 수(`MaxPerPodContainer`)가 허용 가능한 범위의 
전체 죽은 컨테이너의 수(`MaxContainers`)를 벗어나는 상황에서 잠재적으로 서로 충돌할 수 있다. 
다음의 상황에서 `MaxPerPodContainer` 가 조정된다. 
최악의 시나리오는 `MaxPerPodContainer` 를 1로 다운그레이드하고 
가장 오래된 컨테이너를 제거하는 것이다. 추가로, 삭제된 파드가 소유한 컨테이너는 
`MinAge` 보다 오래되면 제거된다.

kubelet이 관리하지 않는 컨테이너는 컨테이너 가비지 수집 대상이 아니다.

## 사용자 설정

여러분은 후술될 kubelet 플래그들을 통하여 이미지 가비지 수집을 조정하기 위하여 다음의 임계값을 조정할 수 있다.

1. `image-gc-high-threshold`, 이미지 가비지 수집을 발생시키는 디스크 사용량의 비율로
 기본값은 85% 이다.
2. `image-gc-low-threshold`, 이미지 가비지 수집을 더 이상 시도하지 않는 디스크 사용량의 비율로
 기본값은 80% 이다.

다음의 kubelet 플래그를 통해 가비지 수집 정책을 사용자 정의할 수 있다.

1. `minimum-container-ttl-duration`, 종료된 컨테이너가 가비지 수집
되기 전의 최소 시간. 기본 값은 0 분이며, 이 경우 모든 종료된 컨테이너는 바로 가비지 수집의 대상이 된다.
2. `maximum-dead-containers-per-container`, 컨테이너가 보유할 수 있는 오래된
인스턴스의 최대 수. 기본 값은 1 이다.
3. `maximum-dead-containers`, 글로벌하게 보유 할 컨테이너의 최대 오래된 인스턴스의 최대 수.
기본 값은 -1이며, 이 경우 인스턴스 수의 제한은 없다.

컨테이너들은 유용성이 만료되기 이전에도 가비지 수집이 될 수 있다. 이러한 컨테이너들은
문제 해결에 도움이 될 수 있는 로그나 다른 데이터를 포함하고 있을 수 있다. 컨테이너 당 적어도
1개의 죽은 컨테이너가 허용될 수 있도록 `maximum-dead-containers-per-container`
값을 충분히 큰 값으로 지정하는 것을 권장한다. 동일한 이유로 `maximum-dead-containers`
의 값도 상대적으로 더 큰 값을 권장한다.
자세한 내용은 [해당 이슈](https://github.com/kubernetes/kubernetes/issues/13287)를 참고한다.


## 사용 중단(Deprecation)

문서에 있는 몇 가지 kubelet의 가비지 수집 특징은 향후에 kubelet 축출(eviction) 기능으로 대체될 예정이다.

포함:

| 기존 Flag | 신규 Flag | 근거 |
| ------------- | -------- | --------- |
| `--image-gc-high-threshold` | `--eviction-hard` or `--eviction-soft` | 기존의 축출 신호로 인하여 이미지 가비지 수집이 트리거 될 수 있음 |
| `--image-gc-low-threshold` | `--eviction-minimum-reclaim` | 축출 리클레임 기능이 동일한 행동을 수행 |
| `--maximum-dead-containers` | | 컨테이너의 외부 영역에 오래된 로그가 저장되어 사용중단(deprecated)됨 |
| `--maximum-dead-containers-per-container` | | 컨테이너의 외부 영역에 오래된 로그가 저장되어 사용중단(deprecated)됨 |
| `--minimum-container-ttl-duration` | | 컨테이너의 외부 영역에 오래된 로그가 저장되어 사용중단(deprecated)됨 |
| `--low-diskspace-threshold-mb` | `--eviction-hard` or `eviction-soft` | 축출이 다른 리소스에 대한 디스크 임계값을 일반화 함 |
| `--outofdisk-transition-frequency` | `--eviction-pressure-transition-period` | 축출이 다른 리소스로의 디스크 압력전환을 일반화 함 |

## {{% heading "whatsnext" %}}

자세한 내용은 [리소스 부족 처리 구성](/docs/concepts/scheduling-eviction/node-pressure-eviction/)를 
본다.
