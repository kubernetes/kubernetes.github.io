---
title: Localizing Kubernetes documentation
content_type: concept
approvers:
- remyleone
- rlenferink
weight: 50
card:
  name: contribute
  weight: 50
  title: Translating the docs
---

<!-- overview -->

This page shows you how to [localize](https://blog.mozilla.org/l10n/2011/12/14/i18n-vs-l10n-whats-the-diff/) the docs for a different language.


<!-- body -->

## Contribute to an existing localization

You can help add or improve content to an existing localization. In [Kubernetes Slack](https://slack.k8s.io/) you'll find a channel for each localization. There is also a general [SIG Docs Localizations Slack channel](https://kubernetes.slack.com/messages/sig-docs-localizations) where you can say hello.

{{< note >}}
If you want to work on a localization that already exists, check
this page in that localization (if it exists), rather than the
English original. You might see extra details there.
{{< /note >}}

### Find your two-letter language code

First, consult the [ISO 639-1 standard](https://www.loc.gov/standards/iso639-2/php/code_list.php) to find your localization's two-letter language code. For example, the two-letter code for Korean is `ko`.

### Fork and clone the repo

First, [create your own fork](/docs/contribute/new-content/open-a-pr/#fork-the-repo) of the [kubernetes/website](https://github.com/kubernetes/website) repository.

Then, clone your fork and `cd` into it:

```shell
git clone https://github.com/<username>/website
cd website
```

The website content directory includes sub-directories for each language. The localization you want to help out with is inside `content/<two-letter-code>`.

### Suggest changes

Create or update your chosen localized page based on the English original. See
[translating content](#translating-content) for more details.

If you notice a technical inaccuracy or other problem with the upstream (English)
documentation, you should fix the upstream documentation first and then repeat the
equivalent fix by updating the localization you're working on.

Please limit pull requests to a single localization, since pull requests that change
content in multiple localizations could be difficult to review.

Follow [Suggesting Content Improvements](/docs/contribute/suggest-improvements/) to propose changes to
that localization. The process is very similar to proposing changes to the upstream (English) content.

## Start a new localization

If you want the Kubernetes documentation localized into a new language, here's what
you need to do.

Because contributors can't approve their own pull requests, you need _at least two contributors_
to begin a localization.

All localization teams must be self-sustaining. The Kubernetes website is happy to host your work, but
it's up to you to translate it and keep existing localized content current.

You'll need to know the two-letter language code for your language. Consult the
[ISO 639-1 standard](https://www.loc.gov/standards/iso639-2/php/code_list.php) to find your
localization's two-letter language code. For example, the two-letter code for Korean is
`ko`.

When you start a new localization, you must localize all the
[minimum required content](#minimum-required-content) before
the Kubernetes project can publish your changes to the live
website.

SIG Docs can help you work on a separate branch so that you
can incrementally work towards that goal.

### Find community

Let Kubernetes SIG Docs know you're interested in creating a localization! Join the [SIG Docs Slack channel](https://kubernetes.slack.com/messages/sig-docs) and the [SIG Docs Localizations Slack channel](https://kubernetes.slack.com/messages/sig-docs-localizations). Other localization teams are happy to help you get started and answer any questions you have.

Please also consider participating in the [SIG Docs Localization Subgroup meeting](https://github.com/kubernetes/community/tree/master/sig-docs).  The mission of the SIG Docs localization subgroup is to work across the SIG Docs localization teams to collaborate on defining and documenting the processes for creating localized contribution guides. In addition, the SIG Docs localization subgroup will look for opportunities for the creation and sharing of common tools across localization teams and also serve to identify new requirements to the SIG Docs Leadership team.  If you have questions about this meeting, please inquire on the [SIG Docs Localizations Slack channel](https://kubernetes.slack.com/messages/sig-docs-localizations).

You can also create a Slack channel for your localization in the `kubernetes/community` repository. For an example of adding a Slack channel, see the PR for [adding a channel for Persian](https://github.com/kubernetes/community/pull/4980).

### Join the Kubernetes GitHub organization

Once you've opened a localization PR, you can become members of the Kubernetes GitHub organization. Each person on the team needs to create their own [Organization Membership Request](https://github.com/kubernetes/org/issues/new/choose) in the `kubernetes/org` repository.

### Add your localization team in GitHub

Next, add your Kubernetes localization team to [`sig-docs/teams.yaml`](https://github.com/kubernetes/org/blob/main/config/kubernetes/sig-docs/teams.yaml). For an example of adding a localization team, see the PR to add the [Spanish localization team](https://github.com/kubernetes/org/pull/685).

Members of `@kubernetes/sig-docs-**-owners` can approve PRs that change content within (and only within) your localization directory: `/content/**/`.

For each localization, The `@kubernetes/sig-docs-**-reviews` team automates review assignment for new PRs.

Members of `@kubernetes/website-maintainers` can create new localization branches to coordinate translation efforts.

Members of `@kubernetes/website-milestone-maintainers` can use the `/milestone` [Prow command](https://prow.k8s.io/command-help) to assign a milestone to issues or PRs.

### Configure the workflow

Next, add a GitHub label for your localization in the `kubernetes/test-infra` repository. A label lets you filter issues and pull requests for your specific language.

For an example of adding a label, see the PR for adding the [Italian language label](https://github.com/kubernetes/test-infra/pull/11316).


### Modify the site configuration

The Kubernetes website uses Hugo as its web framework. The website's Hugo configuration resides in the  [`config.toml`](https://github.com/kubernetes/website/tree/main/config.toml) file. To support a new localization, you'll need to modify `config.toml`.

Add a configuration block for the new language to `config.toml`, under the existing `[languages]` block. The German block, for example, looks like:

```toml
[languages.de]
title = "Kubernetes"
description = "Produktionsreife Container-Verwaltung"
languageName = "Deutsch"
contentDir = "content/de"
weight = 3
```

When assigning a `weight` parameter for your block, find the language block with the highest weight and add 1 to that value.

For more information about Hugo's multilingual support, see "[Multilingual Mode](https://gohugo.io/content-management/multilingual/)".

### Add a new localization directory

Add a language-specific subdirectory to the [`content`](https://github.com/kubernetes/website/tree/main/content) folder in the repository. For example, the two-letter code for German is `de`:

```shell
mkdir content/de
```

You also need to create a directory inside `data/i18n` for
[localized strings](#site-strings-in-i18n); look at existing localizations
for an example. To use these new strings, you must also create a symbolic link
from `i18n/<localization>.toml` to the actual string configuration in
`data/i18n/<localization>/<localization>.toml` (remember to commit the symbolic
link).

For example, for German the strings live in `data/i18n/de/de.toml`, and
`i18n/de.toml` is a symbolic link to `data/i18n/de/de.toml`.

### Localize the community code of conduct

Open a PR against the [`cncf/foundation`](https://github.com/cncf/foundation/tree/master/code-of-conduct-languages) repository to add the code of conduct in your language.


### Setting up the OWNERS files

To set the roles of each user contributing to the localization, create an `OWNERS` file inside the language-specific subdirectory with:

- **reviewers**: A list of kubernetes teams with reviewer roles, in this case, the `sig-docs-**-reviews` team created in [Add your localization team in GitHub](#add-your-localization-team-in-github).
- **approvers**: A list of kubernetes teams with approvers roles, in this case, the `sig-docs-**-owners` team created in [Add your localization team in GitHub](#add-your-localization-team-in-github).
- **labels**: A list of GitHub labels to automatically apply to a PR, in this case, the language label created in [Configure the workflow](#configure-the-workflow).

More information about the `OWNERS` file can be found at [go.k8s.io/owners](https://go.k8s.io/owners).

The [Spanish OWNERS file](https://git.k8s.io/website/content/es/OWNERS), with language code `es`, looks like:

```yaml
# See the OWNERS docs at https://go.k8s.io/owners

# This is the localization project for Spanish.
# Teams and members are visible at https://github.com/orgs/kubernetes/teams.

reviewers:
- sig-docs-es-reviews

approvers:
- sig-docs-es-owners

labels:
- language/es
```

After adding the language-specific `OWNERS` file, update the [root `OWNERS_ALIASES`](https://git.k8s.io/website/OWNERS_ALIASES) file with the new Kubernetes teams for the localization, `sig-docs-**-owners` and `sig-docs-**-reviews`.

For each team, add the list of GitHub users requested in [Add your localization team in GitHub](#add-your-localization-team-in-github), in alphabetical order.

```diff
--- a/OWNERS_ALIASES
+++ b/OWNERS_ALIASES
@@ -48,6 +48,14 @@ aliases:
     - stewart-yu
     - xiangpengzhao
     - zhangxiaoyu-zidif
+  sig-docs-es-owners: # Admins for Spanish content
+    - alexbrand
+    - raelga
+  sig-docs-es-reviews: # PR reviews for Spanish content
+    - alexbrand
+    - electrocucaracha
+    - glo-pena
+    - raelga
   sig-docs-fr-owners: # Admins for French content
     - perriea
     - remyleone
```

### Open a pull request

Next, [open a pull request](/docs/contribute/new-content/open-a-pr/#open-a-pr) (PR) to add a localization to the `kubernetes/website` repository.

The PR must include all of the [minimum required content](#minimum-required-content) before it can be approved.

For an example of adding a new localization, see the PR to enable [docs in French](https://github.com/kubernetes/website/pull/12548).

### Add a localized README file

To guide other localization contributors, add a new [`README-**.md`](https://help.github.com/articles/about-readmes/) to the top level of [k/website](https://github.com/kubernetes/website/), where `**` is the two-letter language code. For example, a German README file would be `README-de.md`.

Provide guidance to localization contributors in the localized `README-**.md` file. Include the same information contained in `README.md` as well as:

- A point of contact for the localization project
- Any information specific to the localization

After you create the localized README, add a link to the file from the main English `README.md`, and include contact information in English. You can provide a GitHub ID, email address, [Slack channel](https://slack.com/), or other method of contact. You must also provide a link to your localized Community Code of Conduct.

### Launching your new localization

Once a localization meets requirements for workflow and minimum output, SIG Docs will:

- Enable language selection on the website
- Publicize the localization's availability through [Cloud Native Computing Foundation](https://www.cncf.io/about/) (CNCF) channels, including the [Kubernetes blog](https://kubernetes.io/blog/).

## Translating content

Localizing *all* of the Kubernetes documentation is an enormous task. It's okay to start small and expand over time.

### Minimum required content

At a minimum, all localizations must include:

Description | URLs
-----|-----
Home | [All heading and subheading URLs](/docs/home/)
Setup | [All heading and subheading URLs](/docs/setup/)
Tutorials | [Kubernetes Basics](/docs/tutorials/kubernetes-basics/), [Hello Minikube](/docs/tutorials/hello-minikube/)
Site strings | [All site strings](#Site-strings-in-i18n) in a new localized TOML file

Translated documents must reside in their own `content/**/` subdirectory, but otherwise follow the same URL path as the English source. For example, to prepare the [Kubernetes Basics](/docs/tutorials/kubernetes-basics/) tutorial for translation into German, create a subfolder under the `content/de/` folder and copy the English source:

```shell
mkdir -p content/de/docs/tutorials
cp content/en/docs/tutorials/kubernetes-basics.md content/de/docs/tutorials/kubernetes-basics.md
```

Translation tools can speed up the translation process. For example, some editors offers plugins to quickly translate text.

{{< caution >}}
Machine-generated translation is insufficient on its own. Localization requires extensive human review to meet minimum standards of quality.
{{< /caution >}}

To ensure accuracy in grammar and meaning, members of your localization team should carefully review all machine-generated translations before publishing.

### Source files

Localizations must be based on the English files from a specific release targeted by the localization team.
Each localization team can decide which release to target which is referred to as the _target version_ below.

To find source files for your target version:

1. Navigate to the Kubernetes website repository at https://github.com/kubernetes/website.
2. Select a branch for your target version from the following table:
    Target version | Branch
    -----|-----
    Latest version | [`main`](https://github.com/kubernetes/website/tree/main)
    Previous version | [`release-{{< skew prevMinorVersion >}}`](https://github.com/kubernetes/website/tree/release-{{< skew prevMinorVersion >}})
    Next version | [`dev-{{< skew nextMinorVersion >}}`](https://github.com/kubernetes/website/tree/dev-{{< skew nextMinorVersion >}})

The `main` branch holds content for the current release `{{< latest-version >}}`. The release team will create a `{{< release-branch >}}` branch before the next release: v{{< skew nextMinorVersion >}}.

### Site strings in i18n

Localizations must include the contents of [`data/i18n/en/en.toml`](https://github.com/kubernetes/website/blob/main/data/i18n/en/en.toml) in a new language-specific file. Using German as an example: `data/i18n/de/de.toml`.

Add a new localization directory and file to `data/i18n/`. For example, with German (`de`):

```bash
mkdir -p data/i18n/de
cp data/i18n/en/en.toml data/i18n/de/de.toml
```

Revise the comments at the top of the file to suit your localization,
then translate the value of each string. For example, this is the German-language
placeholder text for the search form:

```toml
[ui_search_placeholder]
other = "Suchen"
```

Localizing site strings lets you customize site-wide text and features: for example, the legal copyright text in the footer on each page.

### Language specific style guide and glossary

Some language teams have their own language-specific style guide and glossary. For example, see the [Korean Localization Guide](/ko/docs/contribute/localization_ko/).

## Branching strategy

Because localization projects are highly collaborative efforts, we
encourage teams to work in shared localization branches - especially
when starting out and the localization is not yet live.

To collaborate on a localization branch:

1. A team member of [@kubernetes/website-maintainers](https://github.com/orgs/kubernetes/teams/website-maintainers) opens a localization branch from a source branch on https://github.com/kubernetes/website.

    Your team approvers joined the `@kubernetes/website-maintainers` team when you [added your localization team](#add-your-localization-team-in-github) to the [`kubernetes/org`](https://github.com/kubernetes/org) repository.

    We recommend the following branch naming scheme:

    `dev-<source version>-<language code>.<team milestone>`

    For example, an approver on a German localization team opens the localization branch `dev-1.12-de.1` directly against the k/website repository, based on the source branch for Kubernetes v1.12.

2. Individual contributors open feature branches based on the localization branch.

    For example, a German contributor opens a pull request with changes to `kubernetes:dev-1.12-de.1` from `username:local-branch-name`.

3. Approvers review and merge feature branches into the localization branch.

4. Periodically, an approver merges the localization branch to its source branch by opening and approving a new pull request. Be sure to squash the commits before approving the pull request.

Repeat steps 1-4 as needed until the localization is complete. For example, subsequent German localization branches would be: `dev-1.12-de.2`, `dev-1.12-de.3`, etc.

Teams must merge localized content into the same branch from which the content was sourced.

For example:
- a localization branch sourced from `main` must be merged into `main`.
- a localization branch sourced from `release-{{ skew "prevMinorVersion" }}` must be merged into `release-{{ skew "prevMinorVersion" }}`.

{{< note >}}
If your localization branch was created from `main` branch but it is not merged into `main` before new release branch `{{< release-branch >}}` created, merge it into both `main` and new release branch `{{< release-branch >}}`. To merge your localization branch into new release branch `{{< release-branch >}}`, you need to switch upstream branch of your localization branch to `{{< release-branch >}}`.
{{< /note >}}

At the beginning of every team milestone, it's helpful to open an issue comparing upstream changes between the previous localization branch and the current localization branch. There are two scripts for comparing upstream changes. [`upstream_changes.py`](https://github.com/kubernetes/website/tree/main/scripts#upstream_changespy) is useful for checking the changes made to a specific file. And [`diff_l10n_branches.py`](https://github.com/kubernetes/website/tree/main/scripts#diff_l10n_branchespy) is useful for creating a list of outdated files for a specific localization branch.

While only approvers can open a new localization branch and merge pull requests, anyone can open a pull request for a new localization branch. No special permissions are required.

For more information about working from forks or directly from the repository, see ["fork and clone the repo"](#fork-and-clone-the-repo).

## Upstream contributions

SIG Docs welcomes upstream contributions and corrections to the English source.


