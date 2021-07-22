---
title: Other Tools
reviewers:
- janetkuo
content_type: concept
weight: 80
no_list: true
---

<!-- overview -->
Kubernetes contains several built-in tools and external tools that are commonly used or relevant that may as well be seen as required for Kubernetes to function.


<!-- body -->

## Minikube

[`minikube`](https://minikube.sigs.k8s.io/docs/) is a tool that
runs a single-node Kubernetes cluster locally on your workstation for
development and testing purposes.

## Dashboard

[`Dashboard`](/docs/tasks/access-application-cluster/web-ui-dashboard/), the web-based user interface of Kubernetes, allows you to deploy containerized applications
to a Kubernetes cluster, troubleshoot them, and manage the cluster and its resources itself.

## Helm

[Helm](https://helm.sh/) is a tool for managing packages of pre-configured
Kubernetes resources. These packages are known as _Helm charts_.

Use Helm to:

* Find and use popular software packaged as Kubernetes charts
* Share your own applications as Kubernetes charts
* Create reproducible builds of your Kubernetes applications
* Intelligently manage your Kubernetes manifest files
* Manage releases of Helm packages

## Kompose

[`Kompose`](https://github.com/kubernetes/kompose) is a tool to help Docker Compose users move to Kubernetes.

Use Kompose to:

* Translate a Docker Compose file into Kubernetes objects
* Go from local Docker development to managing your application via Kubernetes
* Convert v1 or v2 Docker Compose `yaml` files or [Distributed Application Bundles](https://docs.docker.com/compose/bundles/)
