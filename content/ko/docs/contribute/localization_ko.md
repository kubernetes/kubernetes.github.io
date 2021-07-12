---
title: 쿠버네티스 문서 한글화 가이드
content_type: concept
---

<!-- overview -->

쿠버네티스 문서 한글화를 위한 가이드




<!-- body -->

## 팀 마일스톤 관리

쿠버네티스 문서 한글화팀은 커뮤니티의
[현지화 가이드](/docs/contribute/localization/#branching-strategy)에 따라 한글화를
위한 팀 마일스톤과 개발 브랜치를 관리한다. 본 섹션은 한글화팀의 팀 마일스톤 관리에 특화된
내용을 다룬다.

한글화팀은 `master` 브랜치에서 분기한 개발 브랜치를 사용한다. 개발 브랜치 이름은 다음과 같은
구조를 갖는다.

`dev-<소스 버전>-ko.<팀 마일스톤>`

개발 브랜치는 약 2주에서 3주 사이의 팀 마일스톤 기간 동안 공동의 작업을 위해 사용되며, 팀
마일스톤이 종료될 때 원 브랜치로 병합(merge)된다.

업스트림(upstream)의 릴리스 주기(약 3개월)에 따라 다음 버전으로 마일스톤을 변경하는 시점에는
일시적으로 `release-<소스 버전>` 브랜치를 원 브랜치로 사용하는 개발 브랜치를 추가로 운영한다.

[한글화팀의 정기 화상 회의 일정](https://github.com/kubernetes/community/tree/master/sig-docs#meetings)과
팀 마일스톤 주기는 대체로 일치하며, 정기 회의를 통해 팀 마일스톤마다 PR 랭글러(wrangler)를
지정한다.

한글화팀의 PR 랭글러가 갖는 의무는 업스트림의
[PR 랭글러](/ko/docs/contribute/advanced/#일주일-동안-pr-랭글러-wrangler-되기)가 갖는
의무와 유사하다. 단, 업스트림의 PR 랭글러와는 달리 승인자가 아니어도 팀 마일스톤의 PR 랭글러가
될 수 있다. 그래서, 보다 상위 권한이 필요한 업무가 발생한 경우, PR 랭글러는 해당 권한을 가진
한글화팀 멤버에게 처리를 요청한다.

업스트림의 [PR 랭글러에게 유용한 GitHub 쿼리](/ko/docs/contribute/advanced/#랭글러에게-유용한-github-쿼리)를
기반으로 작성한, 한글화팀의 PR 랭글러에게 유용한 쿼리를 아래에 나열한다.

- [CLA 서명 없음, 병합할 수 없음](https://github.com/kubernetes/website/pulls?q=is%3Aopen+is%3Apr+label%3A%22cncf-cla%3A+no%22+-label%3Ado-not-merge+label%3Alanguage%2Fko)
- [LGTM 필요](https://github.com/kubernetes/website/pulls?utf8=%E2%9C%93&q=is%3Aopen+is%3Apr+-label%3Ado-not-merge+label%3Alanguage%2Fko+-label%3Algtm+)
- [LGTM 보유, 문서 승인 필요](https://github.com/kubernetes/website/pulls?q=is%3Aopen+is%3Apr+-label%3Ado-not-merge+label%3Alanguage%2Fko+label%3Algtm)
- [퀵윈(Quick Wins)](https://github.com/kubernetes/website/pulls?utf8=%E2%9C%93&q=is%3Apr+is%3Aopen+base%3Amaster+-label%3A%22do-not-merge%2Fwork-in-progress%22+-label%3A%22do-not-merge%2Fhold%22+label%3A%22cncf-cla%3A+yes%22+label%3A%22size%2FXS%22+label%3A%22language%2Fko%22+)

팀 마일스톤 일정과 PR 랭글러는 커뮤니티 슬랙 내 [#kubernetes-docs-ko 채널](https://kubernetes.slack.com/archives/CA1MMR86S)에 공지된다.

## 문체 가이드

### 높임말

평어체 사용을 원칙으로 하나, 일부 페이지(예: [https://kubernetes.io/ko](https://kubernetes.io/ko))에 한해 예외적으로
높임말을 사용한다.

### 명령형

어떤 일을 하도록 청자에게 요구하는 명령형 표현은 간결하고 부드러운 표현으로 정확한 의미를 전달하기 위해
어떤 일을 함께 하기를 요청하는 청유형 또는 객관적으로 진술하는 평어체로 번역한다.

명령형 문장 | 번역체
--- | ---
사이트를 방문하라 | 사이트를 방문하자 (청유형)
가이드를 참고하라 | 가이드를 참고한다 (평어체)


### 번역체 지양

우리글로서 자연스럽고 무리가 없도록 번역한다.

번역체 | 자연스러운 문장
--- | ---
-되어지다 (이중 피동 표현) | -되다
짧은 다리를 가진 돼지 | 다리가 짧은 돼지
그는 그의 손으로 숟가락을 들어 그의 밥을 먹었다 | 그는 손으로 숟가락을 들어 밥을 먹었다
접시를 씻고 | 설거지를 하고
가게에 배들, 사과들, 복숭아들이 있다 (과다한 복수형) | 가게에 배, 사과, 복숭아들이 있다

## 문서 코딩 가이드

### 가로폭은 원문을 따름

유지보수의 편의를 위해서 원문의 가로폭을 따른다.

즉, 원문이 한 문단을 줄바꿈하지 않고 한 행에 길게 기술했다면 한글화 시에도 한 행에 길게 기술하고, 원문이 한 문단을
줄바꿈해서 여러 행으로 기술한 경우에는 한글화 시에도 가로폭을 원문과 비슷하게 유지한다.

### 리뷰어 삭제

때때로 원문의 코드 상단에 리뷰어가 명시되어 있는 경우가 있다. 일반적으로 원문 페이지의 리뷰어가 한글화 된 페이지를 리뷰하기 어려우므로 리소스 메타데이터에서 리뷰어 관련 코드를
삭제한다.

아래는 리뷰어 관련 코드를 삭제하는 예시를 보여준다.

```diff
- reviews:
- - reviewer1
- - reviewer
- title: Kubernetes Components
+
+
+
+ title: 쿠버네티스 컴포넌트
content_type: concept
weight: 10
```

## 용어 한글화 가이드

### 용어 한글화의 일반적 방침

영문 용어를 한글화할 때는 다음의 우선 순위를 따르나, 자연스럽지 않은 용어를 무리하게 선택하지는 않는다.

* 한글 단어
  * 순 우리말 단어
  * 한자어 (예: 운영 체제), 외래어 (예: 쿠버네티스, 파드)
* 한영 병기 (예: 훅(hook))
* 영어 단어 (예: Kubelet)

단, 자연스러움을 판단하는 기준은 주관적이므로 [한글화 용어집](#한글화-용어집)을 준용하고
기존에 번역된 문서를 참고한다.

{{% note %}}
한영 병기는 페이지 내에서 해당 용어가 처음 사용될 때, 1회 적용하고 이후에는 한글만 표기한다.
그러나 필요(예: 자연스러움, 명확성 향상 등)에 따라 추가적인 한영 병기를 허용한다.
한영 병기의 대상에는 제목도 포함된다.
{{% /note %}}

### API 오브젝트 용어 한글화 방침

일반적으로 `kubectl api-resources` 결과의 `kind` 에 해당하는 API 오브젝트는
[국립국어원 외래어 표기법](https://kornorms.korean.go.kr/regltn/regltnView.do?regltn_code=0003#a)에
따라 한글로 표기하고 영문을 병기한다. 예를 들면 다음과 같다.

API 오브젝트(kind)      | 한글화(외래어 표기 및 영문 병기)
---                   | ---
ClusterRoleBinding    | 클러스터롤바인딩(ClusterRoleBinding)
ConfigMap             | 컨피그맵(ConfigMap)
Deployment            | 디플로이먼트(Deployment)
PersistentVolumeClaim | 퍼시스턴트볼륨클레임(PersistentVolumeClaim)
...                   | ...

`kind` 에 속하는 API 오브젝트 중에서도 일부는 표현의 간결함을 위해 한영병기를 하지 않는 등의 예외가 있으며,
예외에 대해서는 [한글화 용어집](#한글화-용어집)에 등록된 방식을 준용한다. 예를 들면 다음과 같다.

API 오브젝트(kind)      | 한글화(외래어 표기)
---                   | ---
Pod                   | 파드
Service               | 서비스
...                   | ...


`kind` 에 속하지 않는 API 오브젝트는, [한글화 용어집](#한글화-용어집)에 등록된 용어인 경우를 제외하고,
모두 원문 그대로 표기한다. 예를 들면 다음과 같다.

API 오브젝트(kind가 아닌 경우) | 한글화(원문 유지)
---                        | ---
ClusterRoleBindingList     | ClusterRoleBindingList
ClusterRoleList            | ClusterRoleList
ConfigMapEnvSource         | ConfigMapEnvSource
ConfigMapKeySelector       | ConfigMapKeySelector
PersistentVolumeClaimList  | PersistentVolumeClaimList
PersistentVolumeClaimSpec  | PersistentVolumeClaimSpec
...                        | ...

{{% note %}}
단, API 오브젝트 한글화 원칙에 예외가 있을 수 있으며, 이 경우에는 가능한
[한글화 용어집](#한글화-용어집)을 준용한다. (예를 들면, Horizontal Pod Autoscaler
는 API 오브젝트에 대해 외래어 표기법을 적용하지 않고 원문 그대로 표기한다.)
{{% /note %}}

{{% note %}}
원문에서는 API 오브젝트를 camelCase(예: configMap)로 표기하는 것을 가이드하고 있다.
그러나 한글에는 대소문자 구분이 없으므로 이를 띄어쓰기 없이 붙여서 처리한다.
(예: configMap -> 컨피그맵, config Map -> 컨피그맵)
{{% /note %}}

{{% note %}}
API 오브젝트의 필드 이름, 파일 이름, 경로와 같은 내용은 독자가 구성 파일이나
커맨드라인에서 그대로 사용할 가능성이 높으므로 한글로 옮기지 않고 원문을 유지한다.
단, 주석에 포함된 내용은 한글로 옮길 수 있다.
{{% /note %}}

### 기능 게이트(feature gate) 한글화 방침

쿠버네티스의 [기능 게이트](/ko/docs/reference/command-line-tools-reference/feature-gates/)를
의미하는 용어는 한글화하지 않고 원문 형태를 유지한다.

기능 게이트의 예시는 다음과 같다.
- Accelerators
- AdvancedAuditing
- AffinityInAnnotations
- AllowExtTrafficLocalEndpoints
- ...

전체 기능 게이트 목록은
[여기](/ko/docs/reference/command-line-tools-reference/feature-gates/#feature-gates)를 참고한다.

{{% note %}}
단, 해당 원칙에는 예외가 있을 수 있으며, 이 경우에는 가능한
[한글화 용어집](#한글화-용어집)을 준용한다.
{{% /note %}}

{{% note %}}
기능 게이트는 쿠버네티스 버전에 따라 변경될 수 있으므로,
쿠버네티스 및 쿠버네티스 문서의 버전에 맞는 기능 게이트 목록을 적용하여 한글화를 진행한다.
{{% /note %}}

### 한글화 용어집 정보

쿠버네티스 [한글화 용어집](#한글화-용어집)은 한글화된 쿠버네티스 문서의 일관성을 위해서
각 영문 용어에 대한 한글화 방법을 제시한다.
한글화 용어집에 포함된 용어는 쿠버네티스 문서 한글화팀 회의를 통해 결정되었으며,
본 문서에 대한 ISSUE 및 PR을 통해서 개선한다.

#### 한글화 용어집 개선 가이드

한글화 용어집의 개선(추가, 수정, 삭제 등)을 위한 과정은 다음과 같다.

1. 컨트리뷰터가 개선이 필요한 용어을 파악하면, ISSUE를 생성하여 개선 필요성을 공유하거나 `master` 브랜치에
PR을 생성하여 개선된 용어를 제안한다.

1. 개선 제안에 대한 논의는 ISSUE 및 PR을 통해서 이루어지며, 한글화팀 회의를 통해 확정한다.

1. 리뷰어 및 승인자는 작업 중인 한글화 작업 브랜치(예: dev-1.17-ko.3)에 영향을 최소화 하기 위해서,
신규 한글화 작업 브랜치(예: dev-1.17-ko.4) 생성 시점에 맞춰 확정된 PR을 승인한다.
개선된 한글화 용어집은 신규 한글화 작업 브랜치부터 적용한다.

1. 개선된 한글화 용어집에 따라 기존의 한글 문서에 대한 업데이트가 필요하며,
컨트리뷰션을 통해서 업데이트를 진행한다.

#### 한글화 용어집


English | 한글 | 비고
--- | --- | ---
Access | 접근 |
Active | Active | 잡의 상태
Active Job | 액티브 잡 |
Addons | 애드온 |
admission controller | 어드미션 컨트롤러 |
Age | 기간 |
Allocation | 할당량 |
alphanumeric | 영숫자 |
Annotation | 어노테이션 |
APIService | API서비스(APIService) | API 오브젝트인 경우
App | 앱 |
Appendix | 부록 |
Application | 애플리케이션 |
Args | Args | 약어의 형태이므로 한글화하지 않고 영문 표기
array | 배열 |
autoscaler | 오토스케일러 |
availability zone | 가용성 영역(availability zone) |
bare pod | 베어(bare) 파드 |
beta | 베타 |
Binding | 바인딩(Binding) | API 오브젝트인 경우
boilerplate | 상용구 |
Boot | 부트 |
Build | 빌드 |
Cache | 캐시 |
Calico | 캘리코(Calico) |
canary | 카나리(canary) | 릴리스 방식에 관련한 용어인 경우에 한함
cascading | 캐스케이딩(cascading) |
CertificateSigningRequest | CertificateSigningRequest | API 오브젝트인 경우
character set | 캐릭터 셋 |
Charts | 차트 |
checkpoint | 체크포인트 |
Cilium | 실리움(Cilium) |
CLI | CLI |
Cluster | 클러스터 |
ClusterRole | 클러스터롤(ClusterRole) | API 오브젝트인 경우
ClusterRoleBinding | 클러스터롤바인딩(ClusterRoleBinding) | API 오브젝트인 경우
Command Line Tool | 커맨드라인 툴 |
ComponentStatus | 컴포넌트스테이터스(ComponentStatus) | API 오브젝트인 경우
ConfigMap | 컨피그맵(ConfigMap) | API 오브젝트인 경우
configuration | 구성, 설정 |
Connection | 연결 |
containerized | 컨테이너화 된 |
Context | 컨텍스트  |
Control Plane | 컨트롤 플레인 |
controller | 컨트롤러 |
ControllerRevision | 컨트롤러리비전(ControllerRevision) | API 오브젝트인 경우
cron job | 크론 잡 |
CronJob | 크론잡(CronJob) | API 오브젝트인 경우
CSIDriver | CSI드라이버(CSIDriver) | API 오브젝트인 경우
CSINode | CSI노드(CSINode) | API 오브젝트인 경우
custom metrics | 사용자 정의 메트릭 |
custom resource | 사용자 정의 리소스 |
CustomResourceDefinition | 커스텀리소스데피니션(CustomResourceDefinition) | API 오브젝트인 경우
Daemon | 데몬 |
DaemonSet | 데몬셋(DaemonSet) | API 오브젝트인 경우
Dashboard | 대시보드 |
Data Plane | 데이터 플레인 |
Deployment | 디플로이먼트(Deployment) | API 오브젝트인 경우
deprecated | 사용 중단(deprecated) |
descriptor | 디스크립터, 식별자 |
Desired number of pods | 의도한 파드의 수 |
Desired State | 의도한 상태 |
disruption | 중단(disruption) |
distros | 배포판 |
Docker | 도커 |
Dockerfile | Dockerfile |
Docker Swarm | Docker Swarm |
Downward API | 다운워드(Downward) API |
draining | 드레이닝(draining) |
egress | 이그레스, 송신(egress) |
endpoint | 엔드포인트 |
EndpointSlice | 엔드포인트슬라이스(EndpointSlice) | API 오브젝트인 경우
Endpoints | 엔드포인트(Endpoints) | API 오브젝트인 경우
entry point | 진입점 |
Event | 이벤트(Event) | API 오브젝트인 경우
evict | 축출하다 |
eviction | 축출 |
Exec | Exec |
expose | 노출시키다 |
extension | 익스텐션(extension) |
Failed | Failed | 파드의 상태에 한함
Federation | 페더레이션 |
field | 필드 |
Flannel | 플란넬(Flannel) |
form | 형식 |
Google Compute Engine | Google Compute Engine |
hash | 해시 |
headless | 헤드리스 |
health check | 헬스 체크 |
Heapster | 힙스터(Heapster) |
Heartbeat | 하트비트 |
Homebrew | Homebrew |
hook | 훅(hook) |
Horizontal Pod Autoscaler | Horizontal Pod Autoscaler | 예외적으로 API 오브젝트에 대해 외래어 표기법 적용하지 않고 원문 그대로 표기
hosted zone | 호스팅 영역 |
hostname | 호스트네임 |
Huge page | Huge page |
Hypervisor | 하이퍼바이저 |
idempotent | 멱등성 |
Image | 이미지 |
Image Pull Secrets | 이미지 풀(Pull) 시크릿 |
Ingress | 인그레스(Ingress) | API 오브젝트인 경우
IngressClass | 인그레스클래스(IngressClass) | API 오브젝트인 경우
Init Container | 초기화 컨테이너 |
Instance group | 인스턴스 그룹 |
introspection | 인트로스펙션(introspection) |
Istio | 이스티오(Istio) |
Job | 잡(Job) | API 오브젝트인 경우
kube-proxy | kube-proxy |
Kubelet | Kubelet |
Kubernetes | 쿠버네티스 |
Kube-router | Kube-router |
label | 레이블 |
Lease | 리스(Lease) | API 오브젝트인 경우
lifecycle | 라이프사이클 |
LimitRange | 리밋레인지(LimitRange) | API 오브젝트인 경우
limit | 한도(limit) | 리소스의 개수나 용량을 한정하기 위한 수치로 사용된 경우 선택적으로 사용 (API 오브젝트의 속성으로 limit을 사용한 경우는 가능한 영문 유지)
Linux | 리눅스 |
load | 부하 |
LocalSubjectAccessReview | 로컬서브젝트액세스리뷰(LocalSubjectAccessReview) | API 오브젝트인 경우
Log | 로그 |
loopback | 루프백(loopback) |
Lost | Lost | 클레임의 상태에 한함
Machine | 머신 |
manifest | 매니페스트 |
Master | 마스터 |
metadata | 메타데이터 |
metric | 메트릭 |
masquerading | 마스커레이딩 |
Minikube | Minikube |
Mirror pod | 미러 파드(mirror pod) |
monitoring | 모니터링 |
multihomed | 멀티홈드(multihomed) |
MutatingWebhookConfiguration | MutatingWebhookConfiguration | API 오브젝트인 경우
naked pod | 네이키드(naked) 파드 |
Namespace | 네임스페이스(Namespace) | API 오브젝트인 경우
netfilter | 넷필터(netfilter) |
NetworkPolicy | 네트워크폴리시(NetworkPolicy) | API 오브젝트인 경우
Node | 노드(Node) | API 오브젝트인 경우
node lease | 노드 리스(lease)
Object | 오브젝트 |
Orchestrate | 오케스트레이션하다 |
Output | 출력 |
parameter | 파라미터 |
patch | 패치 |
Pending | Pending | 파드, 클레임의 상태에 한함
PersistentVolume | 퍼시스턴트볼륨(PersistentVolume) | API 오브젝트인 경우
PersistentVolumeClaim | 퍼시스턴트볼륨클레임(PersistentVolumeClaim) | API 오브젝트인 경우
pipeline | 파이프라인 |
placeholder pod | 플레이스홀더(placeholder) 파드 |
Pod | 파드 | API 오브젝트인 경우에도 표현의 간결함을 위해 한영병기를 하지 않음
Pod Preset | 파드 프리셋 |
PodAntiAffinity | 파드안티어피니티(PodAntiAffinity) |
PodDisruptionBudget | PodDisruptionBudget | API 오브젝트인 경우
PodSecurityPolicy | 파드시큐리티폴리시(PodSecurityPolicy) | API 오브젝트인 경우
PodTemplate | 파드템플릿(PodTemplate) | API 오브젝트인 경우
postfix | 접미사 |
prefix | 접두사 |
PriorityClass | 프라이어리티클래스(PriorityClass) | API 오브젝트인 경우
Privileged | 특권을 가진(privileged) |
Prometheus | 프로메테우스 |
proof of concept | 개념 증명 |
Pull Request | 풀 리퀘스트 |
Pull Secret Credentials | 풀(Pull) 시크릿 자격증명 |
QoS Class | QoS 클래스 |
Quota | 쿼터 |
readiness gate | 준비성 게이트(readiness gate) |
readiness probe | 준비성 프로브(readiness probe) |
Ready | Ready |
Reclaim Policy | 반환 정책 |
redirect | 리다이렉트(redirect) |
redirection | 리다이렉션 |
Registry | 레지스트리 |
Release | 릴리스 |
ReplicaSet | 레플리카셋(ReplicaSet) | API 오브젝트인 경우
replicas | 레플리카 |
ReplicationController | 레플리케이션컨트롤러(ReplicationController) | API 오브젝트인 경우
repository | 리포지터리 |
request | 요청(request) | 리소스의 개수나 용량에 대한 요청 수치를 표현하기 위해 사용된 경우 선택적으로 사용 (API 오브젝트 속성으로 request를 사용한 경우는 가능한 영문을 유지)
resource | 리소스 |
ResourceQuota | 리소스쿼터(ResourceQuota) | API 오브젝트인 경우
return | 반환하다 |
revision | 리비전 |
Role | 롤(Role) | API 오브젝트인 경우
RoleBinding | 롤바인딩(RoleBinding) | API 오브젝트인 경우
rollback | 롤백 |
rolling update | 롤링 업데이트 |
rollout | 롤아웃 |
Romana | 로마나(Romana) |
Running | Running | 파드의 상태에 한함
runtime | 런타임 |
RuntimeClass | 런타임클래스(RuntimeClass) | API 오브젝트인 경우
Scale | 스케일 |
Secret | 시크릿(Secret) | API 오브젝트인 경우
segment | 세그먼트 |
Selector | 셀렉터 |
Self-healing | 자가 치유 |
SelfSubjectAccessReview | 셀프서브젝트액세스리뷰(SelfSubjectAccessReview) | API 오브젝트인 경우
SelfSubjectRulesReview | SelfSubjectRulesReview | API 오브젝트이지만 용어를 구성하는 단어 중 복수형 Rules를 '룰스'로 외래어 표기하는 경우 한국어 독자에게 다소 생경할 수 있어 예외적으로 영문 용어를 사용함
Service | 서비스 | API 오브젝트인 경우에도 표현의 간결함을 위해 한영병기를 하지 않음
ServiceAccount | 서비스어카운트(ServiceAccount) | API 오브젝트인 경우
service discovery | 서비스 디스커버리 |
service mesh | 서비스 메시 |
Session | 세션 |
Session Affinity | 세션 어피니티(Affinity) |
Setting | 세팅 |
Shell | 셸 |
Sign In | 로그인 |
Sign Out | 로그아웃 |
skew | 차이(skew) |
snippet | 스니펫(snippet) |
spec | 명세, 스펙, 사양 |
specification | 명세 |
StatefulSet | 스테이트풀셋(StatefulSet) | API 오브젝트인 경우
stateless | 스테이트리스 |
Static pod | 스태틱(static) 파드 |
StorageClass | 스토리지클래스(StorageClass) | API 오브젝트인 경우
SubjectAccessReview | 서브젝트액세스리뷰(SubjectAccessReview) | API 오브젝트인 경우
Sub-Object | 서브-오브젝트 |
support | 지원 |
Surge | 증가율 | 롤링업데이트 전략에 한함
System | 시스템 |
taint | 테인트(taint) |
Task | 태스크 |
Terminated | Terminated | 파드의 상태에 한함
TokenReview | 토큰리뷰(TokenReview) | API 오브젝트인 경우
tolerations | 톨러레이션(toleration) |
Topology spread constraints | 토폴로지 분배 제약 조건 |
Tools  | 도구 |
traffic | 트래픽 |
Type | 타입 |
ubuntu | 우분투 |
use case | 유스케이스 |
userspace | 유저스페이스(userspace) |
Utilization | 사용량, 사용률 |
ValidatingWebhookConfiguration | ValidatingWebhookConfiguration | API 오브젝트인 경우
verbosity | 로그 상세 레벨(verbosity) |
virtualization | 가상화 |
Volume | 볼륨 |
VolumeAttachment | 볼륨어태치먼트(VolumeAttachment) | API 오브젝트인 경우
Waiting | Waiting | 파드의 상태에 한함
Walkthrough | 연습 |
Weave-net | 위브넷(Weave Net) | Weaveworks 사의 솔루션 공식 명칭은 'Weave Net'이므로 한영병기 시 공식 명칭 사용
Windows | 윈도우 |
Worker | 워커 | 노드의 형태에 한함
Workload | 워크로드 |
YAML | YAML |
