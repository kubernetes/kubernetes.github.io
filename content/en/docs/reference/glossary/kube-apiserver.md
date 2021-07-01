---
title: API server
id: kube-apiserver
date: 2018-04-12
full_link: /docs/concepts/overview/components/#kube-apiserver
short_description: >
  Control plane component that serves the Kubernetes API.

aka:
- kube-apiserver
tags:
- architecture
- fundamental
---
 The API server is a component of the Kubernetes
{{< glossary_tooltip text="control plane" term_id="control-plane" >}} that exposes the Kubernetes API.
The API server is the front end for the Kubernetes control plane.

<!--more-->

The main implementation of a Kubernetes API server is [kube-apiserver](/docs/reference/generated/kube-apiserver/).
kube-apiserver is designed to scale horizontally&mdash;that is, it scales by deploying more instances.
You can run several instances of kube-apiserver and balance traffic between those instances.
