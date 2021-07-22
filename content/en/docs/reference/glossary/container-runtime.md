---
title: Container Runtime
id: container-runtime
date: 2019-06-05
full_link: /docs/setup/production-environment/container-runtimes
short_description: >
 The container runtime is the software that is responsible for running containers.

aka:
tags:
- fundamental
- workload
---
 The container runtime is the software that is responsible for running containers.

<!--more-->

Kubernetes supports several container runtimes: {{< glossary_tooltip term_id="docker">}},
{{< glossary_tooltip term_id="containerd" >}}, {{< glossary_tooltip term_id="cri-o" >}},
and any implementation of the [Kubernetes CRI (Container Runtime
Interface)](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-node/container-runtime-interface.md).

Note that {{< glossary_tooltip term_id="docker">}} support is deprecated since `v1.20`
and is planned to be removed in `v1.22`. For more information and a list of
alternatives, refer to [this FAQ blog
post](https://kubernetes.io/blog/2020/12/02/dockershim-faq/).
