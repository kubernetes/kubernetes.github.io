---
title: PR 랭글러(PR Wrangler)
content_type: concept
weight: 20
---

<!-- overview -->

SIG Docs [승인자](/ko/docs/contribute/participate/roles-and-responsibilities/#승인자)는 리포지터리에 대해 일주일 동안 교대로 [풀 리퀘스트 관리](https://github.com/kubernetes/website/wiki/PR-Wranglers)를 수행한다.

이 섹션은 PR 랭글러의 의무에 대해 다룬다. 좋은 리뷰 제공에 대한 자세한 내용은 [Reviewing changes](/ko/docs/contribute/review/)를 참고한다.

<!-- body -->

## 의무

PR 랭글러는 일주일 간 매일 다음의 일을 해야 한다.

- 매일 새로 올라오는 이슈를 심사하고 태그를 지정한다. SIG Docs가 메타데이터를 사용하는 방법에 대한 지침은 [이슈 심사 및 분류](/ko/docs/contribute/review/for-approvers/#이슈-심사와-분류)를 참고한다.
- [스타일](/docs/contribute/style/style-guide/)과 [콘텐츠](/docs/contribute/style/content-guide/) 가이드를 준수하는지에 대해 [열린(open) 풀 리퀘스트](https://github.com/kubernetes/website/pulls)를 매일 리뷰한다.
  - 가장 작은 PR(`size/XS`)부터 시작하고, 가장 큰(`size/XXL`) PR까지 리뷰한다. 가능한 한 많은 PR을 리뷰한다.
- PR 기여자들이 [CLA](https://github.com/kubernetes/community/blob/master/CLA.md)에 서명했는지 확인한다.
  - CLA에 서명하지 않은 기여자에게 CLA에 서명하도록 알리려면 [이](https://github.com/zparnold/k8s-docs-pr-botherer) 스크립트를 사용한다.
- 제안된 변경 사항에 대한 피드백을 제공하고 다른 SIG의 멤버에게 기술 리뷰를 요청한다.
  - 제안된 콘텐츠 변경에 대해 PR에 인라인 제안(inline suggestion)을 제공한다.
  - 내용을 확인해야 하는 경우, PR에 코멘트를 달고 자세한 내용을 요청한다.
  - 관련 `sig/` 레이블을 할당한다.
  - 필요한 경우, 파일의 머리말(front matter)에 있는 `reviewers:` 블록의 리뷰어를 할당한다.
- PR을 병합하려면 승인을 위한 `approve` 코멘트를 사용한다. 준비가 되면 PR을 병합한다.
  - 병합하기 전에 PR은 다른 멤버의 `/lgtm` 코멘트를 받아야 한다.
  - [스타일 지침]을 충족하지 않지만 기술적으로는 정확한 PR은 수락하는 것을 고려한다. 스타일 문제를 해결하는 `good first issue` 레이블의 새로운 이슈를 올리면 된다.

### 랭글러를 위해 도움이 되는 GitHub 쿼리

다음의 쿼리는 랭글러에게 도움이 된다.
이 쿼리들을 수행하여 작업한 후에는, 리뷰할 나머지 PR 목록은 일반적으로 작다.
이 쿼리들은 특히 현지화 PR을 제외한다. 모든 쿼리는 마지막 쿼리를 제외하고 메인 브렌치를 대상으로 한다.

- [CLA 서명 없음, 병합할 수 없음](https://github.com/kubernetes/website/pulls?q=is%3Aopen+is%3Apr+label%3A%22cncf-cla%3A+no%22+-label%3A%22do-not-merge%2Fwork-in-progress%22+-label%3A%22do-not-merge%2Fhold%22+label%3Alanguage%2Fen):
  CLA에 서명하도록 기여자에게 상기시킨다. 봇과 사람이 이미 알렸다면, PR을 닫고
  CLA에 서명한 후 PR을 열 수 있음을 알린다.
  **작성자가 CLA에 서명하지 않은 PR은 리뷰하지 않는다!**
- [LGTM 필요](https://github.com/kubernetes/website/pulls?q=is%3Aopen+is%3Apr+-label%3A%22cncf-cla%3A+no%22+-label%3Ado-not-merge%2Fwork-in-progress+-label%3Ado-not-merge%2Fhold+label%3Alanguage%2Fen+-label%3Algtm):
  멤버의 LGTM이 필요한 PR을 나열한다. PR에 기술 리뷰가 필요한 경우, 봇이 제안한 리뷰어 중 한 명을
  지정한다. 콘텐츠에 대한 작업이 필요하다면, 제안하거나 인라인 피드백을 추가한다.
- [LGTM 보유, 문서 승인 필요](https://github.com/kubernetes/website/pulls?q=is%3Aopen+is%3Apr+-label%3Ado-not-merge%2Fwork-in-progress+-label%3Ado-not-merge%2Fhold+label%3Alanguage%2Fen+label%3Algtm+):
  병합을 위해 `/approve` 코멘트가 필요한 PR을 나열한다.
- [퀵윈(Quick Wins)](https://github.com/kubernetes/website/pulls?utf8=%E2%9C%93&q=is%3Apr+is%3Aopen+base%3Amaster+-label%3A%22do-not-merge%2Fwork-in-progress%22+-label%3A%22do-not-merge%2Fhold%22+label%3A%22cncf-cla%3A+yes%22+label%3A%22size%2FXS%22+label%3A%22language%2Fen%22): 명확한 결격 사유가 없는 메인 브랜치에 대한 PR을 나열한다. ([XS, S, M, L, XL, XXL] 크기의 PR을 작업할 때 크기 레이블에서 "XS"를 변경한다)
- [메인 브랜치이외의 브랜치에 대한 PR](https://github.com/kubernetes/website/pulls?q=is%3Aopen+is%3Apr+label%3Alanguage%2Fen+-base%3Amaster): `dev-` 브랜치에 대한 것일 경우, 곧 출시될 예정인 릴리스이다. `/assign @<meister's_github-username>` 을 사용하여 [문서 릴리스 관리자](https://github.com/kubernetes/sig-release/tree/master/release-team#kubernetes-release-team-roles)를 할당한다. 오래된 브랜치에 대한 PR인 경우, PR 작성자가 가장 적합한 브랜치를 대상으로 하고 있는지 여부를 파악할 수 있도록 도와준다.

### 랭글러를 위한 유용한 Prow 명령어

```
# 한글 레이블 추가
/language ko

# 둘 이상의 커밋인 경우 PR에 스쿼시 레이블 추가
/label tide/merge-method-squash

# Prow를 통해 PR 제목 변경(예: 진행 중인 작업(work-in-progress) [WIP] 또는 PR의 더 상세한 내용)
/retitle [WIP] <TITLE>
```

### 풀 리퀘스트를 종료하는 시기

리뷰와 승인은 PR 대기열을 최신 상태로 유지하는 도구 중 하나이다. 또 다른 도구는 종료(closure)이다.

다음의 상황에서 PR을 닫는다.
- 작성자가 CLA에 2주 동안 서명하지 않았다.

    작성자는 CLA에 서명한 후 PR을 다시 열 수 있다. 이는 어떤 것도 CLA 서명없이 병합되지 않게 하는 위험이 적은 방법이다.

- 작성자가 2주 이상 동안 코멘트나 피드백에 응답하지 않았다.

풀 리퀘스트를 닫는 것을 두려워하지 말자. 기여자는 진행 중인 작업을 쉽게 다시 열고 다시 시작할 수 있다. 종종 종료 통지는 작성자가 기여를 재개하고 끝내도록 자극하는 것이다.

풀 리퀘스트를 닫으려면, PR에 `/close` 코멘트를 남긴다.

{{< note >}}

[`fejta-bot`](https://github.com/fejta-bot)이라는 봇은 90일 동안 활동이 없으면 이슈를 오래된 것(stale)으로 표시한다. 30일이 더 지나면 rotten으로 표시하고 종료한다. PR 랭글러는 14-30일 동안 활동이 없으면 이슈를 닫아야 한다.

{{< /note >}}
