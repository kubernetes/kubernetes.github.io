---
title: Container Runtime
id: container-runtime
date: 2019-06-05
full_link: /docs/setup/production-environment/container-runtimes
short_description: >
  Il container runtime è il software che è responsabile per l'esecuzione dei container.

aka:
tags:
- fundamental
- workload
---
 Il container runtime è il software che è responsabile per l'esecuzione dei container.

<!--more-->

Kubernetes supporta diversi container runtimes: [Docker](http://www.docker.com),
[containerd](https://containerd.io), [cri-o](https://cri-o.io/),
[rktlet](https://github.com/kubernetes-incubator/rktlet) e tutte le implementazioni di
[Kubernetes CRI (Container Runtime Interface)](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-node/container-runtime-interface.md).
