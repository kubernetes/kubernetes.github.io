---
title: Contributing to the Upstream Kubernetes Code
content_type: task
weight: 20
---

<!-- overview -->

This page shows how to contribute to the upstream `kubernetes/kubernetes` project.
You can fix bugs found in the Kubernetes API documentation or the content of
the Kubernetes components such as `kubeadm`, `kube-apiserver`, and `kube-controller-manager`.

If you instead want to regenerate the reference documentation for the Kubernetes
API or the `kube-*` components from the upstream code, see the following instructions:

- [Generating Reference Documentation for the Kubernetes API](/docs/contribute/generate-ref-docs/kubernetes-api/)
- [Generating Reference Documentation for the Kubernetes Components and Tools](/docs/contribute/generate-ref-docs/kubernetes-components/)



## {{% heading "prerequisites" %}}


- You need to have these tools installed:

  - [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
  - [Golang](https://golang.org/doc/install) version 1.13+
  - [Docker](https://docs.docker.com/engine/installation/)
  - [etcd](https://github.com/coreos/etcd/)

- Your `GOPATH` environment variable must be set, and the location of `etcd`
  must be in your `PATH` environment variable.

- You need to know how to create a pull request to a GitHub repository.
  Typically, this involves creating a fork of the repository.
  For more information, see [Creating a Pull Request](https://help.github.com/articles/creating-a-pull-request/)
  and [GitHub Standard Fork & Pull Request Workflow](https://gist.github.com/Chaser324/ce0505fbed06b947d962).



<!-- steps -->

## The big picture

The reference documentation for the Kubernetes API and the `kube-*` components
such as `kube-apiserver`, `kube-controller-manager` are automatically generated
from the source code in the [upstream Kubernetes](https://github.com/kubernetes/kubernetes/).

When you see bugs in the generated documentation, you may want to consider
creating a patch to fix it in the upstream project.

## Cloning the Kubernetes repository

If you don't already have the kubernetes/kubernetes repository, get it now:

```shell
mkdir $GOPATH/src
cd $GOPATH/src
go get github.com/kubernetes/kubernetes
```

Determine the base directory of your clone of the
[kubernetes/kubernetes](https://github.com/kubernetes/kubernetes) repository.
For example, if you followed the preceding step to get the repository, your
base directory is `$GOPATH/src/github.com/kubernetes/kubernetes.`
The remaining steps refer to your base directory as `<k8s-base>`.

Determine the base directory of your clone of the
[kubernetes-sigs/reference-docs](https://github.com/kubernetes-sigs/reference-docs) repository.
For example, if you followed the preceding step to get the repository, your
base directory is `$GOPATH/src/github.com/kubernetes-sigs/reference-docs.`
The remaining steps refer to your base directory as `<rdocs-base>`.

## Editing the Kubernetes source code

The Kubernetes API reference documentation is automatically generated from
an OpenAPI spec, which is generated from the Kubernetes source code. If you
want to change the API reference documentation, the first step is to change one
or more comments in the Kubernetes source code.

The documentation for the `kube-*` components is also generated from the upstream
source code. You must change the code related to the component
you want to fix in order to fix the generated documentation.

### Making changes to the upstream source code

{{< note >}}
The following steps are an example, not a general procedure. Details 
will be different in your situation.
{{< /note >}}

Here's an example of editing a comment in the Kubernetes source code.

In your local kubernetes/kubernetes repository, check out the primary branch,
and make sure it is up to date:

```shell
cd <k8s-base>
git checkout master
git pull https://github.com/kubernetes/kubernetes master
```

Suppose this source file in that primary branch has the typo "atmost":

[kubernetes/kubernetes/staging/src/k8s.io/api/apps/v1/types.go](https://github.com/kubernetes/kubernetes/blob/master/staging/src/k8s.io/api/apps/v1/types.go)

In your local environment, open `types.go`, and change "atmost" to "at most".

Verify that you have changed the file:

```shell
git status
```

The output shows that you are on the master branch, and that the `types.go`
source file has been modified:

```shell
On branch master
...
    modified:   staging/src/k8s.io/api/apps/v1/types.go
```

### Committing your edited file

Run `git add` and `git commit` to commit the changes you have made so far. In the next step,
you will do a second commit. It is important to keep your changes separated into two commits.

### Generating the OpenAPI spec and related files

Go to `<k8s-base>` and run these scripts:

```shell
hack/update-generated-swagger-docs.sh
hack/update-openapi-spec.sh
hack/update-generated-protobuf.sh
```

Run `git status` to see what was generated.

```shell
On branch master
...
    modified:   api/openapi-spec/swagger.json
    modified:   staging/src/k8s.io/api/apps/v1/generated.proto
    modified:   staging/src/k8s.io/api/apps/v1/types.go
    modified:   staging/src/k8s.io/api/apps/v1/types_swagger_doc_generated.go
```

View the contents of `api/openapi-spec/swagger.json` to make sure the typo is fixed.
For example, you could run `git diff -a api/openapi-spec/swagger.json`.
This is important, because `swagger.json` is the input to the second stage of
the doc generation process.

Run `git add` and `git commit` to commit your changes. Now you have two commits:
one that contains the edited `types.go` file, and one that contains the generated OpenAPI spec
and related files. Keep these two commits separate. That is, do not squash your commits.

Submit your changes as a
[pull request](https://help.github.com/articles/creating-a-pull-request/) to the
master branch of the
[kubernetes/kubernetes](https://github.com/kubernetes/kubernetes) repository.
Monitor your pull request, and respond to reviewer comments as needed. Continue
to monitor your pull request until it is merged.

[PR 57758](https://github.com/kubernetes/kubernetes/pull/57758)
is an example of a pull request that fixes a typo in the Kubernetes source code.

{{< note >}}
It can be tricky to determine the correct source file to be changed. In the
preceding example, the authoritative source file is in the `staging` directory
in the `kubernetes/kubernetes` repository. But in your situation,the `staging` directory
might not be the place to find the authoritative source. For guidance, check the
`README` files in
[kubernetes/kubernetes](https://github.com/kubernetes/kubernetes/tree/master/staging)
repository and in related repositories, such as
[kubernetes/apiserver](https://github.com/kubernetes/apiserver/blob/master/README.md).
{{< /note >}}

### Cherry picking your commit into a release branch

In the preceding section, you edited a file in the master branch and then ran scripts
to generate an OpenAPI spec and related files. Then you submitted your changes in a pull request
to the master branch of the kubernetes/kubernetes repository. Now suppose you want to backport
your change into a release branch. For example, suppose the master branch is being used to develop
Kubernetes version 1.10, and you want to backport your change into the release-1.9 branch.

Recall that your pull request has two commits: one for editing `types.go`
and one for the files generated by scripts. The next step is to propose a cherry pick of your first 
commit into the release-1.9 branch. The idea is to cherry pick the commit that edited `types.go`, but not
the commit that has the results of running the scripts. For instructions, see
[Propose a Cherry Pick](https://git.k8s.io/community/contributors/devel/sig-release/cherry-picks.md).

{{< note >}}
Proposing a cherry pick requires that you have permission to set a label and a milestone in your
pull request. If you don't have those permissions, you will need to work with someone who can set the label
and milestone for you.
{{< /note >}}

When you have a pull request in place for cherry picking your one commit into the release-1.9 branch,
the next step is to run these scripts in the release-1.9 branch of your local environment.

```shell
hack/update-generated-swagger-docs.sh
hack/update-openapi-spec.sh
hack/update-generated-protobuf.sh
hack/update-api-reference-docs.sh
```

Now add a commit to your cherry-pick pull request that has the recently generated OpenAPI spec
and related files. Monitor your pull request until it gets merged into the release-1.9 branch.

At this point, both the master branch and the release-1.9 branch have your updated `types.go`
file and a set of generated files that reflect the change you made to `types.go`. Note that the
generated OpenAPI spec and other generated files in the release-1.9 branch are not necessarily
the same as the generated files in the master branch. The generated files in the release-1.9 branch
contain API elements only from Kubernetes 1.9. The generated files in the master branch might contain
API elements that are not in 1.9, but are under development for 1.10.

## Generating the published reference docs

The preceding section showed how to edit a source file and then generate
several files, including `api/openapi-spec/swagger.json` in the
`kubernetes/kubernetes` repository.
The `swagger.json` file is the OpenAPI definition file to use for generating
the API reference documentation.

You are now ready to follow the [Generating Reference Documentation for the Kubernetes API](/docs/contribute/generate-ref-docs/kubernetes-api/) guide to generate the
[published Kubernetes API reference documentation](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/).



## {{% heading "whatsnext" %}}


* [Generating Reference Documentation for the Kubernetes API](/docs/contribute/generate-ref-docs/kubernetes-api/)
* [Generating Reference Docs for Kubernetes Components and Tools](/docs/contribute/generate-ref-docs/kubernetes-components/)
* [Generating Reference Documentation for kubectl Commands](/docs/contribute/generate-ref-docs/kubectl/)


