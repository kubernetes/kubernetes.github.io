---
title: kubectl
content_type: tool-reference
weight: 30
---

## {{% heading "synopsis" %}}


kubectl은 쿠버네티스 클러스터 관리자를 제어한다.

 자세한 정보는 [kubectl 개요](/ko/docs/reference/kubectl/overview/)를 확인한다.

```
kubectl [flags]
```

## {{% heading "options" %}}

   <table style="width: 100%; table-layout: fixed;">
<colgroup>
<col span="1" style="width: 10px;" />
<col span="1" />
</colgroup>
<tbody>

<tr>
<td colspan="2">--add-dir-header</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">true인 경우, 로그 메시지의 헤더에 파일 디렉터리를 추가한다.</td>
</tr>

<tr>
<td colspan="2">--alsologtostderr</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">표준 에러와 파일에 로그를 기록한다.</td>
</tr>

<tr>
<td colspan="2">--as string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">작업을 수행할 사용자 이름</td>
</tr>

<tr>
<td colspan="2">--as-group stringArray</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">작업을 수행할 그룹. 이 플래그를 반복해서 여러 그룹을 지정할 수 있다.</td>
</tr>

<tr>
<td colspan="2">--azure-container-registry-config string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Azure 컨테이너 레지스트리 구성 정보가 포함된 파일의 경로이다.</td>
</tr>

<tr>
<td colspan="2">--cache-dir string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;기본값: "$HOME/.kube/cache"</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">기본 캐시 디렉터리</td>
</tr>

<tr>
<td colspan="2">--certificate-authority string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">인증 기관의 인증서에 대한 파일 경로</td>
</tr>

<tr>
<td colspan="2">--client-certificate string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">TLS용 클라이언트 인증서의 파일 경로</td>
</tr>

<tr>
<td colspan="2">--client-key string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">TLS용 클라이언트 키의 파일 경로</td>
</tr>

<tr>
<td colspan="2">--cloud-provider-gce-l7lb-src-cidrs cidrs&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;기본값: 130.211.0.0/22,35.191.0.0/16</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">L7 LB 트래픽 프록시 및 상태 확인을 위해 GCE 방화벽에서 오픈된 CIDR</td>
</tr>

<tr>
<td colspan="2">--cloud-provider-gce-lb-src-cidrs cidrs&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;기본값: 130.211.0.0/22,209.85.152.0/22,209.85.204.0/22,35.191.0.0/16</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">L4 LB 트래픽 프록시 및 상태 확인을 위해 GCE 방화벽에서 오픈된 CIDR</td>
</tr>

<tr>
<td colspan="2">--cluster string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">사용할 kubeconfig 클러스터의 이름</td>
</tr>

<tr>
<td colspan="2">--context string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">사용할 kubeconfig 콘텍스트의 이름</td>
</tr>

<tr>
<td colspan="2">--default-not-ready-toleration-seconds int&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;기본값: 300</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">아직 톨러레이션(toleration)이 없는 모든 파드에 기본적으로 추가되는 notReady:NoExecute에 대한 톨러레이션의 tolerationSeconds를 나타낸다.</td>
</tr>

<tr>
<td colspan="2">--default-unreachable-toleration-seconds int&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;기본값: 300</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">아직 톨러레이션이 없어서 기본인 unreachable:NoExecute가 추가된 모든 파드에 대한 톨러레이션의 tolerationSeconds를 나타낸다.</td>
</tr>

<tr>
<td colspan="2">-h, --help</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">kubectl에 대한 도움말</td>
</tr>

<tr>
<td colspan="2">--insecure-skip-tls-verify</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">true인 경우, 서버 인증서의 유효성을 확인하지 않는다. 이렇게 하면 사용자의 HTTPS 연결이 안전하지 않게 된다.</td>
</tr>

<tr>
<td colspan="2">--kubeconfig string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">CLI 요청에 사용할 kubeconfig 파일의 경로이다.</td>
</tr>

<tr>
<td colspan="2">--log-backtrace-at traceLocation&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;기본값: :0</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">로깅이 file:N에 도달했을 때 스택 트레이스를 내보낸다.</td>
</tr>

<tr>
<td colspan="2">--log-dir string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">비어 있지 않으면, 이 디렉터리에 로그 파일을 작성한다.</td>
</tr>

<tr>
<td colspan="2">--log-file string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">비어 있지 않으면, 이 로그 파일을 사용한다.</td>
</tr>

<tr>
<td colspan="2">--log-file-max-size uint&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;기본값: 1800</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">로그 파일이 커질 수 있는 최대 크기를 정의한다. 단위는 메가 바이트이다. 값이 0이면, 파일의 최대 크기는 무제한이다.</td>
</tr>

<tr>
<td colspan="2">--log-flush-frequency duration&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;기본값: 5s</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">로그를 비우는 간격의 최대 시간(초)</td>
</tr>

<tr>
<td colspan="2">--logtostderr&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;기본값: true</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">파일 대신 표준 에러에 기록</td>
</tr>

<tr>
<td colspan="2">--match-server-version</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">클라이언트 버전과 일치하는 서버 버전 필요</td>
</tr>

<tr>
<td colspan="2">-n, --namespace string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">지정된 경우, 해당 네임스페이스가 CLI 요청의 범위가 됨</td>
</tr>

<tr>
<td colspan="2">--one-output</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">true이면, 로그를 기본 심각도 수준으로만 기록한다(그렇지 않으면 각각의 더 낮은 심각도 수준에도 기록함).</td>
</tr>

<tr>
<td colspan="2">--password string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">API 서버에 대한 기본 인증을 위한 비밀번호</td>
</tr>

<tr>
<td colspan="2">--profile string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;기본값: "none"</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">캡처할 프로파일의 이름. (none|cpu|heap|goroutine|threadcreate|block|mutex) 중 하나</td>
</tr>

<tr>
<td colspan="2">--profile-output string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;기본값: "profile.pprof"</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">프로파일을 쓸 파일의 이름</td>
</tr>

<tr>
<td colspan="2">--request-timeout string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;기본값: "0"</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">단일 서버 요청을 포기하기 전에 대기하는 시간이다. 0이 아닌 값에는 해당 시간 단위(예: 1s, 2m, 3h)가 포함되어야 한다. 값이 0이면 요청 시간이 초과되지 않는다.</td>
</tr>

<tr>
<td colspan="2">-s, --server string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">쿠버네티스 API 서버의 주소와 포트</td>
</tr>

<tr>
<td colspan="2">--skip-headers</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">true이면, 로그 메시지에서 헤더 접두사를 사용하지 않는다.</td>
</tr>

<tr>
<td colspan="2">--skip-log-headers</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">true이면, 로그 파일을 열 때 헤더를 사용하지 않는다.</td>
</tr>

<tr>
<td colspan="2">--stderrthreshold severity&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;기본값: 2</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">이 임계값 이상의 로그는 표준 에러로 이동한다.</td>
</tr>

<tr>
<td colspan="2">--tls-server-name string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">서버 인증서 유효성 검사에 사용할 서버 이름. 제공되지 않으면, 서버에 접속하는 데 사용되는 호스트 이름이 사용된다.</td>
</tr>

<tr>
<td colspan="2">--token string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">API 서버 인증을 위한 베어러(Bearer) 토큰</td>
</tr>

<tr>
<td colspan="2">--user string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">사용할 kubeconfig 사용자의 이름</td>
</tr>

<tr>
<td colspan="2">--username string</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">API 서버에 대한 기본 인증을 위한 사용자 이름</td>
</tr>

<tr>
<td colspan="2">-v, --v Level</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">로그 수준의 자세한 정도를 나타내는 숫자</td>
</tr>

<tr>
<td colspan="2">--version version[=true]</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">버전 정보를 출력하고 종료</td>
</tr>

<tr>
<td colspan="2">--vmodule moduleSpec</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">파일 필터링 로깅을 위한 쉼표로 구분된 pattern=N 설정 목록</td>
</tr>

<tr>
<td colspan="2">--warnings-as-errors</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">서버에서 받은 경고를 오류로 처리하고 0이 아닌 종료 코드로 종료</td>
</tr>

</tbody>
</table>



## {{% heading "seealso" %}}

* [kubectl annotate](/docs/reference/generated/kubectl/kubectl-commands#annotate)	 - 리소스에 대한 어노테이션 업데이트
* [kubectl api-resources](/docs/reference/generated/kubectl/kubectl-commands#api-resources)	 - 서버에서 지원되는 API 리소스 출력
* [kubectl api-versions](/docs/reference/generated/kubectl/kubectl-commands#api-versions)	 - "그룹/버전" 형식으로 서버에서 지원되는 API 버전을 출력
* [kubectl apply](/docs/reference/generated/kubectl/kubectl-commands#apply)	 - 파일명 또는 표준 입력으로 리소스에 구성 적용
* [kubectl attach](/docs/reference/generated/kubectl/kubectl-commands#attach)	 - 실행 중인 컨테이너에 연결
* [kubectl auth](/docs/reference/generated/kubectl/kubectl-commands#auth)	 - 권한 검사
* [kubectl autoscale](/docs/reference/generated/kubectl/kubectl-commands#autoscale)	 - 디플로이먼트(Deployment), 레플리카셋(ReplicaSet) 또는 레플리케이션컨트롤러(ReplicationController) 자동 스케일링
* [kubectl certificate](/docs/reference/generated/kubectl/kubectl-commands#certificate)	 - 인증서 리소스 수정
* [kubectl cluster-info](/docs/reference/generated/kubectl/kubectl-commands#cluster-info)	 - 클러스터 정보 표시
* [kubectl completion](/docs/reference/generated/kubectl/kubectl-commands#completion)	 - 지정된 셸(bash 또는 zsh)에 대한 셸 완성 코드 출력
* [kubectl config](/docs/reference/generated/kubectl/kubectl-commands#config)	 - kubeconfig 파일 수정
* [kubectl cordon](/docs/reference/generated/kubectl/kubectl-commands#cordon)	 - 노드를 unschedulable로 표시
* [kubectl cp](/docs/reference/generated/kubectl/kubectl-commands#cp)	 - 컨테이너 간에 파일과 디렉터리 복사
* [kubectl create](/docs/reference/generated/kubectl/kubectl-commands#create)	 - 파일 또는 표준 입력에서 리소스를 생성
* [kubectl debug](/docs/reference/generated/kubectl/kubectl-commands#debug)	 - 워크로드와 노드의 문제 해결을 위한 디버깅 세션 생성
* [kubectl delete](/docs/reference/generated/kubectl/kubectl-commands#delete)	 - 파일명, 표준 입력, 리소스 및 이름, 또는 리소스 및 레이블 셀렉터로 리소스 삭제
* [kubectl describe](/docs/reference/generated/kubectl/kubectl-commands#describe)	 - 특정 리소스 또는 리소스 그룹의 세부 정보를 표시
* [kubectl diff](/docs/reference/generated/kubectl/kubectl-commands#diff)	 - 적용 예정 버전과 라이브 버전 비교
* [kubectl drain](/docs/reference/generated/kubectl/kubectl-commands#drain)	 - 유지 보수 준비 중 노드 드레인
* [kubectl edit](/docs/reference/generated/kubectl/kubectl-commands#edit)	 - 서버에서 리소스 편집
* [kubectl exec](/docs/reference/generated/kubectl/kubectl-commands#exec)	 - 컨테이너에서 커맨드 실행
* [kubectl explain](/docs/reference/generated/kubectl/kubectl-commands#explain)	 - 리소스의 문서
* [kubectl expose](/docs/reference/generated/kubectl/kubectl-commands#expose)	 - 레플리케이션 컨트롤러, 서비스, 디플로이먼트 또는 파드를 가져와서 새로운 쿠버네티스 서비스로 노출
* [kubectl get](/docs/reference/generated/kubectl/kubectl-commands#get)	 - 하나 이상의 리소스 표시
* [kubectl kustomize](/docs/reference/generated/kubectl/kubectl-commands#kustomize)	 - 디렉터리 또는 원격 URL에서 kustomization 대상을 빌드
* [kubectl label](/docs/reference/generated/kubectl/kubectl-commands#label)	 - 리소스의 레이블 업데이트
* [kubectl logs](/docs/reference/generated/kubectl/kubectl-commands#logs)	 - 파드의 컨테이너에 대한 로그 출력
* [kubectl options](/docs/reference/generated/kubectl/kubectl-commands#options)	 - 모든 커맨드에서 상속된 플래그 목록을 출력
* [kubectl patch](/docs/reference/generated/kubectl/kubectl-commands#patch)	 - 리소스 필드를 업데이트
* [kubectl plugin](/docs/reference/generated/kubectl/kubectl-commands#plugin)	 - 플러그인과 상호 작용하기 위한 유틸리티를 제공
* [kubectl port-forward](/docs/reference/generated/kubectl/kubectl-commands#port-forward)	 - 하나 이상의 로컬 포트를 파드로 전달
* [kubectl proxy](/docs/reference/generated/kubectl/kubectl-commands#proxy)	 - 쿠버네티스 API 서버에 대한 프록시 실행
* [kubectl replace](/docs/reference/generated/kubectl/kubectl-commands#replace)	 - 파일명 또는 표준 입력으로 리소스 교체
* [kubectl rollout](/docs/reference/generated/kubectl/kubectl-commands#rollout)	 - 리소스 롤아웃 관리
* [kubectl run](/docs/reference/generated/kubectl/kubectl-commands#run)	 - 클러스터에서 특정 이미지 실행
* [kubectl scale](/docs/reference/generated/kubectl/kubectl-commands#scale)	 - 디플로이먼트, 레플리카셋 또는 레플리케이션 컨트롤러의 새 크기 설정
* [kubectl set](/docs/reference/generated/kubectl/kubectl-commands#set)	 - 오브젝트에 특정 기능 설정
* [kubectl taint](/docs/reference/generated/kubectl/kubectl-commands#taint)	 - 하나 이상의 노드에서 테인트(taint) 업데이트
* [kubectl top](/docs/reference/generated/kubectl/kubectl-commands#top)	 - 리소스(CPU/메모리/스토리지) 사용량을 표시
* [kubectl uncordon](/docs/reference/generated/kubectl/kubectl-commands#uncordon)	 - 노드를 schedulable로 표시
* [kubectl version](/docs/reference/generated/kubectl/kubectl-commands#version)	 - 클라이언트 및 서버 버전 정보 출력
* [kubectl wait](/docs/reference/generated/kubectl/kubectl-commands#wait)	 - 실험적(experimental) 기능: 하나 이상의 리소스에 대해서 특정 조건이 만족될 때까지 대기(wait)
