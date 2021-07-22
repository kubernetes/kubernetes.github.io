---
layout: blog
title: "How to choose a SIG as a non-code Kubernetes contributor"
linkTitle: "How to choose a SIG as a non-code Kubernetes contributor"
Author: Chris Short
date: 2021-07-19
slug: how-to-choose-a-sig-as-a-non-code-kubernetes-contributor
canonicalUrl: https://www.k8s.dev/blog/2021/07/09/how-to-choose-a-sig-as-a-non-code-kubernetes-contributor/
---

Kubernetes contributors aren't people in capes or part of some secret society. How to start committing to the GitHub repos that make up the project [is well documented](https://www.kubernetes.dev/docs/guide/), yet it remains intimidating for many.

A few years ago, I spoke at an event and jokingly said, "Kubernetes is just a bunch of APIs and YAML... I'm a contributor; you don't believe me?" After that talk, someone pulled me aside and asked if I was the Kubernetes contributor. They wanted to get involved in the community. Then came the real question, "I don't know which special interest group (SIG) I would work in."

The SIG you work in depends on your skills and what you want to do with your (or your company's) free time.

I’ll start with myself as an example.

# How I found my SIG

I do not code as part of my day-to-day work; I never have. While I have made bits of code into programs here and there, I always had a helping hand. It's also possible my definition of a coder is busted too. But, I consider myself a non-code contributor to Kubernetes.

I'm an Ops person that embraced DevOps early. This meant that I contributed bash scripts, documentation, and configuration files to repos left and right. I still struggle with git from time to time, but I feel like that's the norm, not the exception. If you're familiar with git and GitHub, you're ahead of the game when it comes to contributing to Kubernetes.

My first work in the cloud native world was working with the [SIG Docs](https://github.com/kubernetes/community/tree/master/sig-docs) team. I helped review some documentation and learned some of their processes. I wasn't there long before I found out about another great SIG: [Contributor Experience](https://github.com/kubernetes/community/blob/master/sig-contributor-experience/README.md). Contributor Experience is all about improving the workflow, removing bottlenecks, and generally making Kubernetes a great project to contribute your time and effort. I knew ContribEx (as it’s called) is where I could make an impact.

My philosophy is if things were hard or confusing for me, they'd likely be hard for a large swath of folks. Process improvements can come from anyone. Why not me?

I found early on this: continually showing up to SIG meetings is one way to add value to the community. Regular participation gives you growing context in Kubernetes, and it helps in the long run.

# How I contribute

For me, contributing to Kubernetes is all about helping other contributors. I love talking to new contributors about why something is the way it is and they come up with some alternatives to doing that task. That thought exercise can be an enormously helpful contribution. That has been a part of what I've done in the community. Asking why something is the way it is can be a potent tool for improving things. I’ve helped with [new contributor workshops](https://github.com/kubernetes/community/blob/master/events/2018/05-contributor-summit/new-contributor-workshop.md), which meant showing up and sharing my knowledge. I’ve helped onboard folks into the Kubernetes GitHub organization. I’ve hosted community meetings.

To be honest, I think the most complicated contributions to Kubernetes I’ve made involved the [community link shortener](https://github.com/kubernetes/k8s.io/blob/master/k8s.io/configmap-nginx.yaml). That consisted of editing a [ConfigMap](https://kubernetes.io/docs/concepts/configuration/configmap/). I had to ask for help once because something wasn’t apparent to me, I think, and there was feedback to create more consistency with already created URLs. But, at no point in time was anyone reluctant to help or the feedback negative. It was a genuinely fantastic experience. Plus, I don’t have to remember the YouTube page URL anymore. I type in [yt.k8s.io](https://yt.k8s.io). Speaking of, we have [YouTube, Slack, and other admins](https://www.kubernetes.dev/docs/comms/moderators/) for tools used throughout the community. They all need administration and, more importantly, participants. These things don’t necessarily require coding knowledge but familiarity with the tool that’s in use.

My work now is focusing more on contributing to our [Contributor Marketing](https://github.com/kubernetes/community/tree/master/communication/marketing-team) subproject. The Contributor Marketing sub project's purpose is to get the word out about how to get involved. Writing this article was an output of one of those meetings. Our community does amazing things every day.

None of those things required me to write code. Non-code contributors are an essential part of our community.

# Hop into the Kubernetes community

To join the Kubernetes community, I recommend finding a SIG where your skills align, doing things you want to do in your off time. There's a list of [Kubernetes SIGs](https://www.kubernetes.dev/community/community-groups/) with a lot of great options. If you’re not sure where to go, start with [Contributor Experience](https://github.com/kubernetes/community/tree/master/sig-contributor-experience). We’re here to help.

Often, all you have to do to get started as a contributor is show up to a SIG meeting and seeing if the work going is something that interests you. Being a fly on the wall is a practical way to get started. Once you get started on something, in particular, folks will be more than happy to move whatever hurdles are in your way to help you be productive. There will be some hurdles, of course--Kubernetes is a massive project--but we are all in it together.

Fresh perspectives are essential to healthy projects. We need developers of all kinds to build Kubernetes and its toolchain, which is well-known. What’s lesser known is just how crucial non-code contributions are to the project’s health. If you’re interested in contributing to Kubernetes and aren’t sure how or where to get involved, feel free to join #sig-contribex in [Kubernetes Slack](https://slack.k8s.io/). Or, if it’s easier, reach out to me directly; we’ll figure out where you belong.

Last but not least, if you’re already a contributor, [reach out to the Marketing subgroup](https://github.com/kubernetes/community/issues/new?assignees=&labels=area%2Fcontributor-comms%2C+sig%2Fcontributor-experience&template=marketing-request.md&title=REQUEST%3A+New+blog+proposal) and share your own story. It helps others know they’re welcome.
