---
layout: blog
title: "An Introduction to the K8s-Infrastructure Working Group"
date: 2020-05-27
slug: an-introduction-to-the-k8s-infrastructure-working-group
---

**Author**: [Kiran "Rin" Oliver](https://twitter.com/kiran_oliver) Storyteller, Kubernetes Upstream Marketing Team

# An Introduction to the K8s-Infrastructure Working Group

*Welcome to part one of a new series introducing the K8s-Infrastructure working group!*

When Kubernetes was formed in 2014, Google undertook the task of building and maintaining the infrastructure necessary for keeping the project running smoothly. The tools itself were open source, but the Google Cloud Platform project used to run the infrastructure was internal-only, preventing contributors from being able to help out. In August 2018, Google granted the Cloud Native Computing Foundation [$9M in credits for the operation of Kubernetes](https://cloud.google.com/blog/products/gcp/google-cloud-grants-9m-in-credits-for-the-operation-of-the-kubernetes-project). The sentiment behind this was that a project such as Kubernetes should be both maintained and operated by the community itself rather than by a single vendor. 

A group of community members enthusiastically undertook the task of collaborating on the path forward, realizing that there was a [more formal infrastructure necessary](https://github.com/kubernetes/community/issues/2715). They joined together as a cross-team working group with ownership spanning across multiple Kubernetes SIGs (Architecture, Contributor Experience, Release, and Testing). [Aaron Crickenberger](https://twitter.com/spiffxp) worked with the Kubernetes Steering Committee to enable the formation of the working group, co-drafting a charter alongside long-time collaborator [Davanum Srinivas](https://twitter.com/dims), and by 2019 the working group was official.

## What Issues Does the K8s-Infrastructure Working Group Tackle?

The team took on the complex task of managing the many moving parts of the infrastructure that sustains Kubernetes as a project. 

The need started with necessity: the first problem they took on was a complete migration of all of the project's infrastructure from Google-owned infrastructure to the Cloud Native Computing Foundation (CNCF). This is being done so that the project is self-sustainable without the need of any direct assistance from individual vendors. This breaks down in the following ways:

* Identifying what infrastructure the Kubernetes project depends on.
    * What applications are running?
    * Where does it run?
    * Where is its source code?
    * What is custom built?
    * What is off-the-shelf?
    * What services depend on each other?
    * How is it administered?
* Documenting guidelines and policies for how to run the infrastructure as a community.
    * What are our access policies?
    * How do we keep track of billing?
    * How do we ensure privacy and security?
* Migrating infrastructure over to the CNCF as-is.
    * What is the path of least resistance to migration?
* Improving the state of the infrastructure for sustainability.
    *  Moving from humans running scripts to a more automated GitOps model (YAML all the things!)
    *  Supporting community members who wish to develop new infrastructure
* Documenting the state of our efforts, better defining goals, and completeness indicators.
    * The project and program management necessary to communicate this work to our [massive community of contributors](https://kubernetes.io/blog/2020/04/21/contributor-communication/)

## The challenge of K8s-Infrastructure is documentation

The most crucial problem the working group is trying to tackle is that the project is all volunteer-led. This leads to contributors, chairs, and others involved in the project quickly becoming overscheduled. As a result of this, certain areas such as documentation and organization often lack information, and efforts to progress are taking longer than the group would like to complete.

Some of the infrastructure that is being migrated over hasn't been updated in a while, and its original authors or directly responsible individuals have moved on from working on Kubernetes. While this is great from the perspective of the fact that the code was able to run untouched for a long period of time, from the perspective of trying to migrate, this makes it difficult to identify how to operate these components, and how to move these infrastructure pieces where they need to be effectively.  

The lack of documentation is being addressed head-on by group member [Bart Smykla](https://twitter.com/bartsmykla), but there is a definite need for others to support. If you're looking for a way to [get involved](https://github.com/kubernetes/community/labels/wg%2Fk8s-infra) and learn the infrastructure, you can become a new contributor to the working group!  

## Celebrating some Working Group wins

The team has made progress in the last few months that is well worth celebrating. 

- The K8s-Infrastructure Working Group released an automated billing report that they start every meeting off by reviewing as a group. 
- DNS for k8s.io and kubernetes.io are also fully [community-owned](https://groups.google.com/g/kubernetes-dev/c/LZTYJorGh7c/m/u-ydk-yNEgAJ), with community members able to [file issues](https://github.com/kubernetes/k8s.io/issues/new?assignees=&labels=wg%2Fk8s-infra&template=dns-request.md&title=DNS+REQUEST%3A+%3Cyour-dns-record%3E) to manage records.
- The container registry [k8s.gcr.io](https://github.com/kubernetes/k8s.io/tree/main/k8s.gcr.io) is also fully community-owned and available for all Kubernetes subprojects to use. 
- The Kubernetes [publishing-bot](https://github.com/kubernetes/publishing-bot) responsible for keeping k8s.io/kubernetes/staging repositories published to their own top-level repos (For example: [kubernetes/api](https://github.com/kubernetes/api)) runs on a community-owned cluster.
- The gcsweb.k8s.io service used to provide anonymous access to GCS buckets for kubernetes artifacts runs on a community-owned cluster.
- There is also an automated process of promoting all our container images. This includes a fully documented infrastructure, managed by the Kubernetes community, with automated processes for provisioning permissions. 

These are just a few of the things currently happening in the K8s Infrastructure working group. 

If you're interested in getting involved, be sure to join the [#wg-K8s-infra Slack Channel](https://app.slack.com/client/T09NY5SBT/CCK68P2Q2). Meetings are 60 minutes long, and are held every other Wednesday at 8:30 AM PT/16:30 UTC.

Join to help with the documentation, stay to learn about the amazing infrastructure supporting the Kubernetes community.
