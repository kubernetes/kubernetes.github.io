---
title: "Install Tools"
description: Set up Kubernetes tools on your computer.
weight: 10
no_list: true
---

## kubectl

<!-- overview -->
The Kubernetes command-line tool, [kubectl](/docs/reference/kubectl/kubectl/), allows
you to run commands against Kubernetes clusters.
You can use kubectl to deploy applications, inspect and manage cluster resources,
and view logs. For more information including a complete list of kubectl operations, see the
[`kubectl` reference documentation](/docs/reference/kubectl/).

kubectl is installable on a variety of Linux platforms, macOS and Windows. 
Find your preferred operating system below.

- [Install kubectl on Linux](/docs/tasks/tools/install-kubectl-linux)
- [Install kubectl on macOS](/docs/tasks/tools/install-kubectl-macos)
- [Install kubectl on Windows](/docs/tasks/tools/install-kubectl-windows)

## kind

[`kind`](https://kind.sigs.k8s.io/docs/) lets you run Kubernetes on
your local computer. This tool requires that you have
[Docker](https://docs.docker.com/get-docker/) installed and configured.

The kind [Quick Start](https://kind.sigs.k8s.io/docs/user/quick-start/) page
shows you what you need to do to get up and running with kind.

<a class="btn btn-primary" href="https://kind.sigs.k8s.io/docs/user/quick-start/" role="button" aria-label="View kind Quick Start Guide">View kind Quick Start Guide</a>

## minikube

Like `kind`, [`minikube`](https://minikube.sigs.k8s.io/) is a tool that lets you run Kubernetes
locally. `minikube` runs a single-node Kubernetes cluster on your personal
computer (including Windows, macOS and Linux PCs) so that you can try out
Kubernetes, or for daily development work.

You can follow the official
[Get Started!](https://minikube.sigs.k8s.io/docs/start/) guide if your focus is
on getting the tool installed.

<a class="btn btn-primary" href="https://minikube.sigs.k8s.io/docs/start/" role="button" aria-label="View minikube Get Started! Guide">View minikube Get Started! Guide</a>

Once you have `minikube` working, you can use it to
[run a sample application](/docs/tutorials/hello-minikube/).

## kubeadm

You can use the {{< glossary_tooltip term_id="kubeadm" text="kubeadm" >}} tool to create and manage Kubernetes clusters.
It performs the actions necessary to get a minimum viable, secure cluster up and running in a user friendly way.

[Installing kubeadm](/docs/setup/production-environment/tools/kubeadm/install-kubeadm/) shows you how to install kubeadm.
Once installed, you can use it to [create a cluster](/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/).

<a class="btn btn-primary" href="/docs/setup/production-environment/tools/kubeadm/install-kubeadm/" role="button" aria-label="View kubeadm Install Guide">View kubeadm Install Guide</a>
