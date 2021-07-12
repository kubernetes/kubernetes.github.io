---
title: 역할과 책임
content_type: concept
weight: 10
---

<!-- overview -->

누구나 쿠버네티스에 기여할 수 있다. SIG Docs에 대한 기여가 커짐에 따라,
커뮤니티의 다양한 멤버십을 신청할 수 있다.
이러한 역할을 통해 커뮤니티 내에서 더 많은 책임을 질 수 있다.
각 역할마다 많은 시간과 노력이 필요하다. 역할은 다음과 같다.

- 모든 사람: 쿠버네티스 문서에 정기적으로 기여하는 기여자
- 멤버: 이슈를 할당, 심사하고 풀 리퀘스트에 대한 구속력 없는 리뷰를 제공할 수 있다.
- 리뷰어: 문서의 풀 리퀘스트에 대한 리뷰를 리딩할 수 있으며 변경 사항에 대한 품질을 보증할 수 있다.
- 승인자: 문서에 대한 리뷰를 리딩하고 변경 사항을 병합할 수 있다

<!-- body -->

## 모든 사람

GitHub 계정을 가진 누구나 쿠버네티스에 기여할 수 있다. SIG Docs는 모든 새로운 기여자를 환영한다!

모든 사람은 다음의 작업을 할 수 있다.

- [`kubernetes/website`](https://github.com/kubernetes/website)를 포함한 모든
  [쿠버네티스](https://github.com/kubernetes/) 리포지터리에서
  이슈를 올린다.
- 풀 리퀘스트에 대해 구속력 없는 피드백을 제공한다.
- 현지화에 기여한다.
- [슬랙](https://slack.k8s.io/) 또는
  [SIG docs 메일링 리스트](https://groups.google.com/forum/#!forum/kubernetes-sig-docs)에 개선을 제안한다.

[CLA에 서명](/ko/docs/contribute/new-content/overview/#sign-the-cla) 후에 누구나 다음을 할 수 있다.

- 기존 콘텐츠를 개선하거나, 새 콘텐츠를 추가하거나, 블로그 게시물 또는 사례연구 작성을 위해 풀 리퀘스트를 연다.
- 다이어그램, 그래픽 자산 그리고 포함할 수 있는 스크린캐스트와 비디오를 제작한다.

자세한 내용은 [새로운 콘텐츠 기여하기](/ko/docs/contribute/new-content/)를 참고한다.

## 멤버

멤버는 `kubernetes/website` 에 여러 개의 풀 리퀘스트를 제출한
사람이다. 멤버는
[쿠버네티스 GitHub 조직](https://github.com/kubernetes)의 회원이다.

멤버는 다음의 작업을 할 수 있다.

- [모든 사람](#모든-사람)에 나열된 모든 것을 한다.
- 풀 리퀘스트에 `/lgtm` 코멘트를 사용하여 LGTM(looks good to me) 레이블을 추가한다.

  {{< note >}}
  `/lgtm` 사용은 자동화를 트리거한다. 만약 구속력 없는 승인을 제공하려면, "LGTM" 코멘트를 남기는 것도 좋다!
  {{< /note >}}

- `/hold` 코멘트를 사용하여 풀 리퀘스트에 대한 병합을 차단한다.
- `/assign` 코멘트를 사용하여 풀 리퀘스트에 리뷰어를 지정한다.
- 풀 리퀘스트에 구속력 없는 리뷰를 제공한다.
- 자동화를 사용하여 이슈를 심사하고 분류한다.
- 새로운 기능에 대한 문서를 작성한다.

### 멤버 되기

최소 5개의 실질적인 풀 리퀘스트를 제출하고 다른
[요구 사항](https://github.com/kubernetes/community/blob/master/community-membership.md#member)을 충족시킨 후, 다음의 단계를 따른다.

1. 멤버십을 [후원](/ko/docs/contribute/advanced#새로운-기여자-후원)해줄 두 명의
   [리뷰어](#리뷰어) 또는 [승인자](#승인자)를
   찾는다.

   [슬랙의 #sig-docs 채널](https://kubernetes.slack.com) 또는
   [SIG Docs 메일링 리스트](https://groups.google.com/forum/#!forum/kubernetes-sig-docs)에서 후원을 요청한다.

   {{< note >}}
   SIG Docs 멤버 개인에게 직접 email을 보내거나
   슬랙 다이렉트 메시지를 보내지 않는다. 반드시 지원서를 제출하기 전에 후원을 요청해야 한다.
   {{< /note >}}

1. [`kubernetes/org`](https://github.com/kubernetes/org/) 리포지터리에
   GitHub 이슈를 등록한다.
   **Organization Membership Request** 이슈 템플릿을 사용한다.

1. 후원자에게 GitHub 이슈를 알린다. 다음 중 하나를 수행할 수 있다.
   - 이슈에서 후원자의 GitHub 사용자 이름을 코멘트로 추가한다. (`@<GitHub-username>`)
   - 슬랙 또는 이메일을 사용해 이슈 링크를 후원자에게 보낸다.

     후원자는 `+1` 투표로 여러분의 요청을 승인할 것이다. 후원자가 요청을 승인하면,
     쿠버네티스 GitHub 관리자가 여러분을 멤버로 추가한다.
     축하한다!

     만약 멤버십이 수락되지 않으면 피드백을 받게 될 것이다. 피드백의 내용을 해결한 후, 다시 지원하자.

1. 여러분의 이메일 계정으로 수신된 쿠버네티스 GitHub 조직으로의 초대를 수락한다.

   {{< note >}}
   GitHub은 초대를 여러분 계정의 기본 이메일 주소로 보낸다.
   {{< /note >}}

## 리뷰어

리뷰어는 열린 풀 리퀘스트를 리뷰할 책임이 있다. 멤버 피드백과는 달리,
여러분은 리뷰어의 피드백을 반드시 해결해야 한다. 리뷰어는
[@kubernetes/sig-docs-{language}-reviews](https://github.com/orgs/kubernetes/teams?query=sig-docs)
GitHub 팀의 멤버이다.

리뷰어는 다음의 작업을 수행할 수 있다.

- [모든 사람](#모든-사람)과 [멤버](#멤버)에 나열된 모든 것을 수행한다.
- 풀 리퀘스트 리뷰와 구속력 있는 피드백을 제공한다.

  {{< note >}}
  구속력 없는 피드백을 제공하려면, 코멘트에 "선택 사항: "과 같은 문구를 접두어로 남긴다.
  {{< /note >}}

- 코드에서 사용자 화면 문자열 편집
- 코드 코멘트 개선

여러분은 SIG DOcs 리뷰어이거나, 특정 주제 영역의 문서에 대한 리뷰어일 수 있다.

### 풀 리퀘스트에 대한 리뷰어 할당

자동화 시스템은 모든 풀 리퀘스트에 대해 리뷰어를 할당한다. `/assign
[@_github_handle]` 코멘트를 남겨 특정 사람에게 리뷰를 요청할 수
있다.

지정된 리뷰어가 PR에 코멘트를 남기지 않는다면, 다른 리뷰어가 개입할 수
있다. 필요에 따라 기술 리뷰어를 지정할 수도 있다.

### `/lgtm` 사용하기

LGTM은 "Looks good to me"의 약자이며 풀 리퀘스트가 기술적으로
정확하고 병합할 준비가 되었음을 나타낸다. 모든 PR은 리뷰어의 `/lgtm` 코멘트가
필요하고 병합을 위해 승인자의 `/approve` 코멘트가 필요하다.

리뷰어의 `/lgtm` 코멘트는 구속력 있고 자동화 시스템이 `lgtm` 레이블을 추가하도록 트리거한다.

### 리뷰어 되기

[요건](https://github.com/kubernetes/community/blob/master/community-membership.md#reviewer)을
충족하면, SIG Docs 리뷰어가 될 수 있다. 다른 SIG의 리뷰어는 SIG Docs의 리뷰어 자격에
반드시 별도로 지원해야 한다.

지원하려면, 다음을 수행한다.

1. `kubernetes/website` 리포지터리 내
   [OWNERS_ALIASES](https://github.com/kubernetes/website/blob/master/OWNERS) 파일의 섹션에
   여러분의 GitHub 사용자 이름을 추가하는 풀 리퀘스트를 연다.

  {{< note >}}
  자신을 추가할 위치가 확실하지 않으면, `sig-docs-ko-reviews` 에 추가한다.
  {{< /note >}}

1. PR을 하나 이상의 SIG-Docs 승인자(`sig-docs-{language}-owners` 에
   나열된 사용자 이름)에게 지정한다.

승인되면, SIG Docs 리더가 적당한 GitHub 팀에 여러분을 추가한다. 일단 추가되면,
[K8s-ci-robot](https://github.com/kubernetes/test-infra/tree/master/prow#bots-home)이
새로운 풀 리퀘스트에서 리뷰어로 여러분을 할당하고 제안한다.

## 승인자

승인자는 병합하기 위해 풀 리퀘스트를 리뷰하고 승인한다. 승인자는
[@kubernetes/sig-docs-{language}-owners](https://github.com/orgs/kubernetes/teams/?query=sig-docs)
GitHub 팀의 멤버이다.

승인자는 다음의 작업을 할 수 있다.

- [모든 사람](#모든-사람), [멤버](#멤버) 그리고 [리뷰어](#리뷰어) 하위의 모든 목록을 할 수 있다.
- 코멘트에 `/approve` 를 사용해서 풀 리퀘스트를 승인하고, 병합해서 기여자의 컨텐츠를 게시한다.
- 스타일 가이드 개선을 제안한다.
- 문서 테스트 개선을 제안한다.
- 쿠버네티스 웹사이트 또는 다른 도구 개선을 제안한다.

PR에 이미 `/lgtm` 이 있거나, 승인자도 `/lgtm` 코멘트를 남긴다면,
PR은 자동으로 병합된다. SIG Docs 승인자는 추가적인 기술 리뷰가 필요치 않는 변경에 대해서만
`/lgtm` 을 남겨야 한다.


### 풀 리퀘스트 승인

승인자와 SIG Docs 리더는 website 리포지터리로 풀 리퀘스트를 병합할 수 있는
유일한 사람들이다. 이것은 특정한 책임이 따른다.

- 승인자는 PR들을 리포지터리에 병합하는 `/approve` 명령을 사용할 수 있다.

  {{< warning >}}
  부주의한 머지로 인해 사이트를 파괴할 수 있으므로, 머지할 때에 그 의미를 확인해야 한다.
  {{< /warning >}}

- 제안된 변경이
  [컨트리뷰션 가이드 라인](/docs/contribute/style/content-guide/#contributing-content)에 적합한지 확인한다.

  질문이 생기거나 확실하지 않다면 자유롭게
  추가 리뷰를 요청한다.

- PR을 `/approve` 하기 전에 Netlify 테스트 결과를 검토한다.

    <img src="/images/docs/contribute/netlify-pass.png" width="75%" alt="승인 전에 반드시 Netlify 테스트를 통과해야 한다" />

- 승인 전에 PR에 대한 Netlify 프리뷰 페이지를 방문하여, 제대로 보이는지 확인한다.

- 주간 로테이션을 위해
  [PR Wrangler 로테이션 스케줄](https://github.com/kubernetes/website/wiki/PR-Wranglers)에
  참여한다. SIG Docs는 모든 승인자들이 이 로테이션에 참여할 것으로 기대한다. 자세한 내용은
  [PR 랭글러(PR wrangler)](/ko/docs/contribute/participate/pr-wranglers/)를
  참고한다.

## 승인자 되기

[요구 사항](https://github.com/kubernetes/community/blob/master/community-membership.md#approver)을
충족하면 SIG Docs 승인자가 될 수 있다.
다른 SIG의 승인자는 SIG Docs의 승인자 자격에 대해
별도로 신청해야 한다.

지원하려면 다음을 수행한다.

1. `kubernetes/website` 리포지터리 내
   [OWNERS_ALIASES](https://github.com/kubernetes/website/blob/master/OWNERS)
   파일의 섹션에 자신을 추가하는 풀 리퀘스트를 연다.

    {{< note >}}
    자신을 추가할 위치가 확실하지 않으면, `sig-docs-ko-owners` 에 추가한다.
    {{< /note >}}

2. PR에 한 명 이상의 현재 SIG Docs 승인자를 지정한다.

승인되면, SIG Docs 리더가 적당한 GitHub 팀에 여러분을 추가한다. 일단 추가되면,
[@k8s-ci-robot](https://github.com/kubernetes/test-infra/tree/master/prow#bots-home)이
새로운 풀 리퀘스트에서 승인자로 여러분을 할당하고 제안한다.

## {{% heading "whatsnext" %}}

- 모든 승인자가 교대로 수행하는 역할인 [PR 랭글러](/ko/docs/contribute/participate/pr-wranglers)에 대해 읽어보기
