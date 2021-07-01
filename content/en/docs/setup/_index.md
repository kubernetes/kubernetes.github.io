---
reviewers:
- brendandburns
- erictune
- mikedanese
title: Getting started
main_menu: true
weight: 20
content_type: concept
no_list: true
card:
  name: setup
  weight: 20
  anchors:
  - anchor: "#learning-environment"
    title: Learning environment
  - anchor: "#production-environment"
    title: Production environment  
---

<!-- overview -->

This section lists the different ways to set up and run Kubernetes.
When you install Kubernetes, choose an installation type based on: ease of maintenance, security,
control, available resources, and expertise required to operate and manage a cluster.

You can [download Kubernetes](/releases/download/) to deploy a Kubernetes cluster
on a local machine, into the cloud, or for your own datacenter.

If you don't want to manage a Kubernetes cluster yourself, you could pick a managed service, including
[certified platforms](/docs/setup/production-environment/turnkey-solutions/).
There are also other standardized and custom solutions across a wide range of cloud and
bare metal environments.

<!-- body -->

## Learning environment

If you're learning Kubernetes, use the tools supported by the Kubernetes community,
or tools in the ecosystem to set up a Kubernetes cluster on a local machine.
See [Install tools](/docs/tasks/tools/).

## Production environment

When evaluating a solution for a
[production environment](/docs/setup/production-environment/), consider which aspects of
operating a Kubernetes cluster (or _abstractions_) you want to manage yourself and which you
prefer to hand off to a provider.

For a cluster you're managing yourself, the officially supported tool
for deploying Kubernetes is [kubeadm](/docs/setup/production-environment/tools/kubeadm/).

## {{% heading "whatsnext" %}}

- [Download Kubernetes](/releases/download/)
- Download and [install tools](/docs/tasks/tools/) including `kubectl`
- Select a [container runtime](/docs/setup/production-environment/container-runtimes/) for your new cluster
- Learn about [best practices](/docs/setup/best-practices/) for cluster setup

Kubernetes is designed for its {{< glossary_tooltip term_id="control-plane" text="control plane" >}} to
run on Linux. Within your cluster you can run applications on Linux or other operating systems, including
Windows.
- Learn to [set up clusters with Windows nodes](/docs/setup/production-environment/windows/)
