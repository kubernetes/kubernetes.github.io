---
title: Quickstart
content_type: task
weight: 40
---

<!-- overview -->

This page shows how to use the `update-imported-docs` script to generate
the Kubernetes reference documentation. The script automates
the build setup and generates the reference documentation for a release.

## {{% heading "prerequisites" %}}

{{< include "prerequisites-ref-docs.md" >}}

<!-- steps -->

## Getting the docs repository

Make sure your `website` fork is up-to-date with the `kubernetes/website` remote on
GitHub (`main` branch), and clone your `website` fork.

```shell
mkdir github.com
cd github.com
git clone git@github.com:<your_github_username>/website.git
```

Determine the base directory of your clone. For example, if you followed the
preceding step to get the repository, your base directory is
`github.com/website.` The remaining steps refer to your base directory as
`<web-base>`.

{{< note>}}
If you want to change the content of the component tools and API reference,
see the [contributing upstream guide](/docs/contribute/generate-ref-docs/contribute-upstream).
{{< /note >}}

## Overview of update-imported-docs

The `update-imported-docs` script is located in the `<web-base>/update-imported-docs/`
directory.

The script builds the following references:

* Component and tool reference pages
* The `kubectl` command reference
* The Kubernetes API reference

The `update-imported-docs` script generates the Kubernetes reference documentation
from the Kubernetes source code. The script creates a temporary directory
under `/tmp` on your machine and clones the required repositories: `kubernetes/kubernetes` and
`kubernetes-sigs/reference-docs` into this directory.
The script sets your `GOPATH` to this temporary directory.
Three additional environment variables are set:

* `K8S_RELEASE`
* `K8S_ROOT`
* `K8S_WEBROOT`

The script requires two arguments to run successfully:

* A YAML configuration file (`reference.yml`)
* A release version, for example:`1.17`

The configuration file contains a `generate-command` field.
The `generate-command` field defines a series of build instructions
from `kubernetes-sigs/reference-docs/Makefile`. The `K8S_RELEASE` variable
determines the version of the release.

The `update-imported-docs` script performs the following steps:

1. Clones the related repositories specified in a configuration file. For the
   purpose of generating reference docs, the repository that is cloned by
   default is `kubernetes-sigs/reference-docs`.
1. Runs commands under the cloned repositories to prepare the docs generator and
   then generates the HTML and Markdown files.
1. Copies the generated HTML and Markdown files to a local clone of the `<web-base>`
   repository under locations specified in the configuration file.
1. Updates `kubectl` command links from `kubectl`.md to the refer to
   the sections in the `kubectl` command reference.

When the generated files are in your local clone of the `<web-base>`
repository, you can submit them in a [pull request](/docs/contribute/new-content/open-a-pr/)
to `<web-base>`.

## Configuration file format

Each configuration file may contain multiple repos that will be imported together. When
necessary, you can customize the configuration file by manually editing it. You
may create new config files for importing other groups of documents.
The following is an example of the YAML configuration file:

```yaml
repos:
- name: community
  remote: https://github.com/kubernetes/community.git
  branch: master
  files:
  - src: contributors/devel/README.md
    dst: docs/imported/community/devel.md
  - src: contributors/guide/README.md
    dst: docs/imported/community/guide.md
```

Single page Markdown documents, imported by the tool, must adhere to
the [Documentation Style Guide](/docs/contribute/style/style-guide/).

## Customizing reference.yml

Open `<web-base>/update-imported-docs/reference.yml` for editing.
Do not change the content for the `generate-command` field unless you understand
how the command is used to build the references.
You should not need to update `reference.yml`. At times, changes in the
upstream source code, may require changes to the configuration file
(for example: golang version dependencies and third-party library changes).
If you encounter build issues, contact the SIG-Docs team on the
[#sig-docs Kubernetes Slack channel](https://kubernetes.slack.com).

{{< note >}}
The `generate-command` is an optional entry, which can be used to run a
given command or a short script to generate the docs from within a repository.
{{< /note >}}

In `reference.yml`, `files` contains a list of `src` and `dst` fields.
The `src` field contains the location of a generated Markdown file in the cloned
`kubernetes-sigs/reference-docs` build directory, and the `dst` field specifies
where to copy this file in the cloned `kubernetes/website` repository.
For example:

```yaml
repos:
- name: reference-docs
  remote: https://github.com/kubernetes-sigs/reference-docs.git
  files:
  - src: gen-compdocs/build/kube-apiserver.md
    dst: content/en/docs/reference/command-line-tools-reference/kube-apiserver.md
  ...
```

Note that when there are many files to be copied from the same source directory
to the same destination directory, you can use wildcards in the value given to
`src`. You must provide the directory name as the value for `dst`.
For example:

```yaml
  files:
  - src: gen-compdocs/build/kubeadm*.md
    dst: content/en/docs/reference/setup-tools/kubeadm/generated/
```

## Running the update-imported-docs tool

You can run the `update-imported-docs` tool as follows:

```shell
cd <web-base>/update-imported-docs
./update-imported-docs <configuration-file.yml> <release-version>
```

For example:

```shell
./update-imported-docs reference.yml 1.17
```

<!-- Revisit: is the release configuration used -->
## Fixing Links

The `release.yml` configuration file contains instructions to fix relative links.
To fix relative links within your imported files, set the`gen-absolute-links`
property to `true`. You can find an example of this in
[`release.yml`](https://github.com/kubernetes/website/blob/main/update-imported-docs/release.yml).

## Adding and committing changes in kubernetes/website

List the files that were generated and copied to `<web-base>`:

```shell
cd <web-base>
git status
```

The output shows the new and modified files. The generated output varies
depending upon changes made to the upstream source code.

### Generated component tool files

```
content/en/docs/reference/command-line-tools-reference/cloud-controller-manager.md
content/en/docs/reference/command-line-tools-reference/kube-apiserver.md
content/en/docs/reference/command-line-tools-reference/kube-controller-manager.md
content/en/docs/reference/command-line-tools-reference/kube-proxy.md
content/en/docs/reference/command-line-tools-reference/kube-scheduler.md
content/en/docs/reference/setup-tools/kubeadm/generated/kubeadm.md
content/en/docs/reference/kubectl/kubectl.md
```

### Generated kubectl command reference files

```
static/docs/reference/generated/kubectl/kubectl-commands.html
static/docs/reference/generated/kubectl/navData.js
static/docs/reference/generated/kubectl/scroll.js
static/docs/reference/generated/kubectl/stylesheet.css
static/docs/reference/generated/kubectl/tabvisibility.js
static/docs/reference/generated/kubectl/node_modules/bootstrap/dist/css/bootstrap.min.css
static/docs/reference/generated/kubectl/node_modules/highlight.js/styles/default.css
static/docs/reference/generated/kubectl/node_modules/jquery.scrollto/jquery.scrollTo.min.js
static/docs/reference/generated/kubectl/node_modules/jquery/dist/jquery.min.js
static/docs/reference/generated/kubectl/css/font-awesome.min.css
```

### Generated Kubernetes API reference directories and files

```
static/docs/reference/generated/kubernetes-api/{{< param "version" >}}/index.html
static/docs/reference/generated/kubernetes-api/{{< param "version" >}}/js/navData.js
static/docs/reference/generated/kubernetes-api/{{< param "version" >}}/js/scroll.js
static/docs/reference/generated/kubernetes-api/{{< param "version" >}}/js/query.scrollTo.min.js
static/docs/reference/generated/kubernetes-api/{{< param "version" >}}/css/font-awesome.min.css
static/docs/reference/generated/kubernetes-api/{{< param "version" >}}/css/bootstrap.min.css
static/docs/reference/generated/kubernetes-api/{{< param "version" >}}/css/stylesheet.css
static/docs/reference/generated/kubernetes-api/{{< param "version" >}}/fonts/FontAwesome.otf
static/docs/reference/generated/kubernetes-api/{{< param "version" >}}/fonts/fontawesome-webfont.eot
static/docs/reference/generated/kubernetes-api/{{< param "version" >}}/fonts/fontawesome-webfont.svg
static/docs/reference/generated/kubernetes-api/{{< param "version" >}}/fonts/fontawesome-webfont.ttf
static/docs/reference/generated/kubernetes-api/{{< param "version" >}}/fonts/fontawesome-webfont.woff
static/docs/reference/generated/kubernetes-api/{{< param "version" >}}/fonts/fontawesome-webfont.woff2
```

Run `git add` and `git commit` to commit the files.

## Creating a pull request

Create a pull request to the `kubernetes/website` repository. Monitor your
pull request, and respond to review comments as needed. Continue to monitor
your pull request until it is merged.

A few minutes after your pull request is merged, your updated reference
topics will be visible in the
[published documentation](/docs/home/).



## {{% heading "whatsnext" %}}


To generate the individual reference documentation by manually setting up the required build repositories and
running the build targets, see the following guides:

* [Generating Reference Documentation for Kubernetes Components and Tools](/docs/contribute/generate-ref-docs/kubernetes-components/)
* [Generating Reference Documentation for kubectl Commands](/docs/contribute/generate-ref-docs/kubectl/)
* [Generating Reference Documentation for the Kubernetes API](/docs/contribute/generate-ref-docs/kubernetes-api/)


