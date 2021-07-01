---
title: Container Runtime
id: container-runtime
date: 2019-06-05
full_link: /docs/setup/production-environment/container-runtimes
short_description: >
  El _Container Runtime_, entorno de ejecución de un contenedor, es el software responsable de ejecutar contenedores.

aka:
tags:
- fundamental
- workload
---
El _Container Runtime_ es el software responsable de ejecutar contenedores.

<!--more-->

Kubernetes soporta varios _Container Runtimes_: [Docker](http://www.docker.com),
[containerd](https://containerd.io), [cri-o](https://cri-o.io/),
[rktlet](https://github.com/kubernetes-incubator/rktlet) y cualquier implementación de 
[Kubernetes CRI (Container Runtime Interface)](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-node/container-runtime-interface.md).
