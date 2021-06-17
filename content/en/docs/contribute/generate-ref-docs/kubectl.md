---
title: Generating Reference Documentation for kubectl Commands
content_type: task
weight: 90
---

<!-- overview -->

This page shows how to generate the `kubectl` command reference.

{{< note >}}
This topic shows how to generate reference documentation for
[kubectl commands](/docs/reference/generated/kubectl/kubectl-commands)
like
[kubectl apply](/docs/reference/generated/kubectl/kubectl-commands#apply) and
[kubectl taint](/docs/reference/generated/kubectl/kubectl-commands#taint).
This topic does not show how to generate the
[kubectl](/docs/reference/generated/kubectl/kubectl-commands/)
options reference page. For instructions on how to generate the kubectl options
reference page, see
[Generating Reference Pages for Kubernetes Components and Tools](/docs/contribute/generate-ref-docs/kubernetes-components/).
{{< /note >}}

## {{% heading "prerequisites" %}}

{{< include "prerequisites-ref-docs.md" >}}

<!-- steps -->

## Setting up the local repositories

Create a local workspace and set your `GOPATH`.

```shell
mkdir -p $HOME/<workspace>

export GOPATH=$HOME/<workspace>
```

Get a local clone of the following repositories:

```shell
go get -u github.com/spf13/pflag
go get -u github.com/spf13/cobra
go get -u gopkg.in/yaml.v2
go get -u github.com/kubernetes-sigs/reference-docs
```

If you don't already have the kubernetes/website repository, get it now:

```shell
git clone https://github.com/<your-username>/website $GOPATH/src/github.com/<your-username>/website
```

Get a clone of the kubernetes/kubernetes repository as k8s.io/kubernetes:

```shell
git clone https://github.com/kubernetes/kubernetes $GOPATH/src/k8s.io/kubernetes
```

Remove the spf13 package from `$GOPATH/src/k8s.io/kubernetes/vendor/github.com`.

```shell
rm -rf $GOPATH/src/k8s.io/kubernetes/vendor/github.com/spf13
```

The kubernetes/kubernetes repository provides the `kubectl` and `kustomize` source code.

* Determine the base directory of your clone of the
[kubernetes/kubernetes](https://github.com/kubernetes/kubernetes) repository.
For example, if you followed the preceding step to get the repository, your
base directory is `$GOPATH/src/k8s.io/kubernetes.`
The remaining steps refer to your base directory as `<k8s-base>`.

* Determine the base directory of your clone of the
[kubernetes/website](https://github.com/kubernetes/website) repository.
For example, if you followed the preceding step to get the repository, your
base directory is `$GOPATH/src/github.com/<your-username>/website.`
The remaining steps refer to your base directory as `<web-base>`.

* Determine the base directory of your clone of the
[kubernetes-sigs/reference-docs](https://github.com/kubernetes-sigs/reference-docs) repository.
For example, if you followed the preceding step to get the repository, your
base directory is `$GOPATH/src/github.com/kubernetes-sigs/reference-docs.`
The remaining steps refer to your base directory as `<rdocs-base>`.

In your local k8s.io/kubernetes repository, check out the branch of interest,
and make sure it is up to date. For example, if you want to generate docs for
Kubernetes {{< skew prevMinorVersion >}}.0, you could use these commands:

```shell
cd <k8s-base>
git checkout v{{< skew prevMinorVersion >}}.0
git pull https://github.com/kubernetes/kubernetes {{< skew prevMinorVersion >}}.0
```

If you do not need to edit the `kubectl` source code, follow the instructions for
[Setting build variables](#setting-build-variables).

## Editing the kubectl source code

The kubectl command reference documentation is automatically generated from
the kubectl source code. If you want to change the reference documentation, the first step
is to change one or more comments in the kubectl source code. Make the change in your
local kubernetes/kubernetes repository, and then submit a pull request to the master branch of
[github.com/kubernetes/kubernetes](https://github.com/kubernetes/kubernetes).

[PR 56673](https://github.com/kubernetes/kubernetes/pull/56673/files)
is an example of a pull request that fixes a typo in the kubectl source code.

Monitor your pull request, and respond to reviewer comments. Continue to monitor your
pull request until it is merged into the target branch of the kubernetes/kubernetes repository.

## Cherry picking your change into a release branch

Your change is now in the master branch, which is used for development of the next
Kubernetes release. If you want your change to appear in the docs for a Kubernetes
version that has already been released, you need to propose that your change be
cherry picked into the release branch.

For example, suppose the master branch is being used to develop Kubernetes
{{< skew currentVersion >}}
and you want to backport your change to the release-{{< skew prevMinorVersion >}} branch. For
instructions on how to do this, see
[Propose a Cherry Pick](https://git.k8s.io/community/contributors/devel/sig-release/cherry-picks.md).

Monitor your cherry-pick pull request until it is merged into the release branch.

{{< note >}}
Proposing a cherry pick requires that you have permission to set a label and a
milestone in your pull request. If you don't have those permissions, you will
need to work with someone who can set the label and milestone for you.
{{< /note >}}

## Setting build variables

Go to `<rdocs-base>`. On you command line, set the following environment variables.

* Set `K8S_ROOT` to `<k8s-base>`.
* Set `K8S_WEBROOT` to `<web-base>`.
* Set `K8S_RELEASE` to the version of the docs you want to build.
  For example, if you want to build docs for Kubernetes {{< skew prevMinorVersion >}}, set `K8S_RELEASE` to {{< skew prevMinorVersion >}}.

For example:

```shell
export K8S_WEBROOT=$GOPATH/src/github.com/<your-username>/website
export K8S_ROOT=$GOPATH/src/k8s.io/kubernetes
export K8S_RELEASE={{< skew prevMinorVersion >}}
```

## Creating a versioned directory

The `createversiondirs` build target creates a versioned directory
and copies the kubectl reference configuration files to the versioned directory.
The versioned directory name follows the pattern of `v<major>_<minor>`.

In the `<rdocs-base>` directory, run the following build target:

```shell
cd <rdocs-base>
make createversiondirs
```

## Checking out a release tag in k8s.io/kubernetes

In your local `<k8s-base>` repository, checkout the branch that has
the version of Kubernetes that you want to document. For example, if you want
to generate docs for Kubernetes {{< skew prevMinorVersion >}}.0, check out the
`v{{< skew prevMinorVersion >}}` tag. Make sure
you local branch is up to date.

```shell
cd <k8s-base>
git checkout v{{< skew prevMinorVersion >}}.0
git pull https://github.com/kubernetes/kubernetes v{{< skew prevMinorVersion >}}.0
```

## Running the doc generation code

In your local `<rdocs-base>`, run the `copycli` build target. The command runs as `root`:

```shell
cd <rdocs-base>
make copycli
```

The `copycli` command cleans the temporary build directory, generates the kubectl command files,
and copies the collated kubectl command reference HTML page and assets to `<web-base>`.

## Locate the generated files

Verify that these two files have been generated:

```shell
[ -e "<rdocs-base>/gen-kubectldocs/generators/build/index.html" ] && echo "index.html built" || echo "no index.html"
[ -e "<rdocs-base>/gen-kubectldocs/generators/build/navData.js" ] && echo "navData.js built" || echo "no navData.js"
```

## Locate the copied files

Verify that all generated files have been copied to your `<web-base>`:

```shell
cd <web-base>
git status
```

The output should include the modified files:

```
static/docs/reference/generated/kubectl/kubectl-commands.html
static/docs/reference/generated/kubectl/navData.js
```

The output may also include:

```
static/docs/reference/generated/kubectl/scroll.js
static/docs/reference/generated/kubectl/stylesheet.css
static/docs/reference/generated/kubectl/tabvisibility.js
static/docs/reference/generated/kubectl/node_modules/bootstrap/dist/css/bootstrap.min.css
static/docs/reference/generated/kubectl/node_modules/highlight.js/styles/default.css
static/docs/reference/generated/kubectl/node_modules/jquery.scrollto/jquery.scrollTo.min.js
static/docs/reference/generated/kubectl/node_modules/jquery/dist/jquery.min.js
static/docs/reference/generated/kubectl/node_modules/font-awesome/css/font-awesome.min.css
```

## Locally test the documentation

Build the Kubernetes documentation in your local `<web-base>`.

```shell
cd <web-base>
git submodule update --init --recursive --depth 1 # if not already done
make container-serve
```

View the [local preview](https://localhost:1313/docs/reference/generated/kubectl/kubectl-commands/).

## Adding and committing changes in kubernetes/website

Run `git add` and `git commit` to commit the files.

## Creating a pull request

Create a pull request to the `kubernetes/website` repository. Monitor your
pull request, and respond to review comments as needed. Continue to monitor
your pull request until it is merged.

A few minutes after your pull request is merged, your updated reference
topics will be visible in the
[published documentation](/docs/home).



## {{% heading "whatsnext" %}}


* [Generating Reference Documentation Quickstart](/docs/contribute/generate-ref-docs/quickstart/)
* [Generating Reference Documentation for Kubernetes Components and Tools](/docs/contribute/generate-ref-docs/kubernetes-components/)
* [Generating Reference Documentation for the Kubernetes API](/docs/contribute/generate-ref-docs/kubernetes-api/)


