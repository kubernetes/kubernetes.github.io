---
title: 高度な貢献
slug: advanced
content_type: concept
weight: 98
---

<!-- overview -->

このページはあなたが[新しいコンテンツに貢献し](/ja/docs/contribute/new-content/overview)、[他の人の作業をレビューする](/ja/docs/contribute/review/reviewing-prs/)方法を理解しており、さらに貢献する方法について学ぶ準備ができていることを前提としています。
これらのタスクの一部には、Gitコマンドラインクライアントとその他のツールを使用する必要があります。

<!-- body -->

## 改善の提案

<!-- TODO: update this link after translated this page -->
SIG Docsの[メンバー](/docs/contribute/participate/roles-and-responsibilities/#members)は改善を提案できます。

<!-- TODO: update this link after translated this page -->
Kubernetesのドキュメントへの貢献をしばらく行っていると、[スタイルガイド](/docs/contribute/style/style-guide/) 、[コンテンツガイド](/ja/docs/contribute/style/content-guide/)、ドキュメントの作成に使用されるツールチェーン、Webサイトのスタイル、プルリクエストのレビューとマージのプロセス、またはドキュメントの他の側面について、改善のアイデアが浮かんでくるかもしれません。
最大限の透明性を得るために、この種の提案はSIG Docsミーティングまたは[kubernetes-sig-docsメーリングリスト](https://groups.google.com/forum/#!forum/kubernetes-sig-docs)で議論する必要があります。
さらに抜本的な変更を提案する前に現在の仕組みや過去の決定が行われた理由について、ある程度の文脈を理解しておくと非常に役立ちます。
ドキュメントが、現在どのように機能しているかについての質問の回答を得る最も簡単な方法は、[kubernetes.slack.com](https://kubernetes.slack.com) の `#sig-docs` Slackチャネルで質問することです。

議論が行われ、SIG が望ましい結果について合意した後、最も適切な方法で提案された変更に取り組むことができます。
たとえば、スタイルガイドやWebサイトの機能の更新にはプルリクエストを開くことが含まれ、ドキュメントのテストに関連する変更には sig-testing の作業が含まれる場合があります。

## Kubernetesリリースのドキュメントを調整する

<!-- TODO: update this link after translated this page -->
SIG Docsの[approver](/docs/contribute/participate/roles-and-responsibilities/#approvers)はKubernetesリリースのドキュメントを調整できます。

Kubernetesの各リリースは、sig-release Special Interest Group (SIG)に参加しているチームによって調整されます。
1つのリリースを行うリリースチームには、リリース全体のリーダーや、sig-testingなどの代表者が含まれます。
Kubernetesのリリースプロセスの詳細については[https://github.com/kubernetes/sig-release](https://github.com/kubernetes/sig-release) を参照してください。

1つのリリースのSIG Docsの担当者は以下のタスクを調整します:

- ドキュメントに影響を与える新機能または変更された機能がないか、機能追跡スプレッドシートを監視します。
  特定の機能のドキュメントがリリースの準備ができていない場合、その機能をリリースに入れることが許可されない場合があります。
- sig-release ミーティングに定期的に参加し、リリースに関するドキュメントのステータスに関する最新情報を提供します。
- 機能の実装を担当するSIGによって作成された機能ドキュメントのドラフトをレビュー〜編集します。
- リリース関連のプルリクエストをマージし、リリース用のGitのfeatureブランチをメンテナンスします。
- 将来この役割を行う方法を学びたい他のSIG Docs 貢献者を指導します。
  これは「シャドーイング」として知られています。
- リリースアーティファクトが公開されたときに、リリースに関連するドキュメントの変更を公開します。

リリースの調整は通常3〜4か月のコミットメントであり、この責務はSIG Docsのapproverの間でローテーションされます。

## Serve as a New Contributor Ambassador

SIG Docs [approvers](/docs/contribute/participate/roles-and-responsibilities/#approvers)
can serve as New Contributor Ambassadors.

New Contributor Ambassadors welcome new contributors to SIG-Docs,
suggest PRs to new contributors, and mentor new contributors through their first
few PR submissions.

Responsibilities for New Contributor Ambassadors include:

- Monitoring the [#sig-docs Slack channel](https://kubernetes.slack.com) for questions from new contributors.
- Working with PR wranglers to identify good first issues for new contributors.
- Mentoring new contributors through their first few PRs to the docs repo.
- Helping new contributors create the more complex PRs they need to become Kubernetes members.
- [Sponsoring contributors](/docs/contribute/advanced/#sponsor-a-new-contributor) on their path to becoming Kubernetes members.

Current New Contributor Ambassadors are announced at each SIG-Docs meeting, and in the [Kubernetes #sig-docs channel](https://kubernetes.slack.com).

## Sponsor a new contributor

SIG Docs [reviewers](/docs/contribute/participate/roles-and-responsibilities/#reviewers)
can sponsor new contributors.

After a new contributor has successfully submitted 5 substantive pull requests
to one or more Kubernetes repositories, they are eligible to apply for
[membership](/docs/contribute/participate/roles-and-responsibilities/#members)
in the Kubernetes organization. The contributor's membership needs to be
backed by two sponsors who are already reviewers.

New docs contributors can request sponsors by asking in the #sig-docs channel
on the [Kubernetes Slack instance](https://kubernetes.slack.com) or on the
[SIG Docs mailing list](https://groups.google.com/forum/#!forum/kubernetes-sig-docs).
If you feel confident about the applicant's work, you volunteer to sponsor them.
When they submit their membership application, reply to the application with a
"+1" and include details about why you think the applicant is a good fit for
membership in the Kubernetes organization.

## Serve as a SIG Co-chair

SIG Docs [approvers](/docs/contribute/participate/roles-and-responsibilities/#approvers)
can serve a term as a co-chair of SIG Docs.

### Prerequisites

Approvers must meet the following requirements to be a co-chair:

- Have been a SIG Docs approver for at least 6 months
- Have [led a Kubernetes docs release](/docs/contribute/advanced/#coordinate-docs-for-a-kubernetes-release) or shadowed two releases
- Understand SIG Docs workflows and tooling: git, Hugo, localization, blog subproject
- Understand how other Kubernetes SIGs and repositories affect the SIG Docs
  workflow, including:
  [teams in k/org](https://github.com/kubernetes/org/blob/master/config/kubernetes/sig-docs/teams.yaml),
  [process in k/community](https://github.com/kubernetes/community/tree/master/sig-docs),
  plugins in [k/test-infra](https://github.com/kubernetes/test-infra/), and the role of
  [SIG Architecture](https://github.com/kubernetes/community/tree/master/sig-architecture).
- Commit at least 5 hours per week (and often more) to the role for a minimum of 6 months

### Responsibilities

The role of co-chair is one of service: co-chairs build contributor capacity, handle process and policy, schedule and run meetings, schedule PR wranglers, advocate for docs in the Kubernetes community, make sure that docs succeed in Kubernetes release cycles, and keep SIG Docs focused on effective priorities.

Responsibilities include:

- Keep SIG Docs focused on maximizing developer happiness through excellent documentation
- Exemplify the [community code of conduct](https://github.com/cncf/foundation/blob/master/code-of-conduct.md) and hold SIG members accountable to it
- Learn and set best practices for the SIG by updating contribution guidelines
- Schedule and run SIG meetings: weekly status updates, quarterly retro/planning sessions, and others as needed
- Schedule and run doc sprints at KubeCon events and other conferences
- Recruit for and advocate on behalf of SIG Docs with the {{< glossary_tooltip text="CNCF" term_id="cncf" >}} and its platinum partners, including Google, Oracle, Azure, IBM, and Huawei
- Keep the SIG running smoothly

### Running effective meetings

To schedule and run effective meetings, these guidelines show what to do, how to do it, and why.

**Uphold the [community code of conduct](https://github.com/cncf/foundation/blob/master/code-of-conduct.md)**:

- Hold respectful, inclusive discussions with respectful, inclusive language.

**Set a clear agenda**:

- Set a clear agenda of topics
- Publish the agenda in advance

For weekly meetings, copypaste the previous week's notes into the "Past meetings" section of the notes

**Collaborate on accurate notes**:

- Record the meeting's discussion
- Consider delegating the role of note-taker

**Assign action items clearly and accurately**:

- Record the action item, who is assigned to it, and the expected completion date

**Moderate as needed**:

- If discussion strays from the agenda, refocus participants on the current topic
- Make room for different discussion styles while keeping the discussion focused and honoring folks' time

**Honor folks' time**:

Begin and end meetings on time.

**Use Zoom effectively**:

- Familiarize yourself with [Zoom guidelines for Kubernetes](https://github.com/kubernetes/community/blob/master/communication/zoom-guidelines.md)
- Claim the host role when you log in by entering the host key

<img src="/images/docs/contribute/claim-host.png" width="75%" alt="Claiming the host role in Zoom" />

### Recording meetings on Zoom

When you're ready to start the recording, click Record to Cloud.

When you're ready to stop recording, click Stop.

The video uploads automatically to YouTube.
