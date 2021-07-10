---
title: Communicate Between Containers in the Same Pod Using a Shared Volume
content_type: task
weight: 110
---

<!-- overview -->

This page shows how to use a Volume to communicate between two Containers running
in the same Pod. See also how to allow processes to communicate by
[sharing process namespace](/docs/tasks/configure-pod-container/share-process-namespace/)
between containers.

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}

<!-- steps -->

##  Creating a Pod that runs two Containers

In this exercise, you create a Pod that runs two Containers. The two containers
share a Volume that they can use to communicate. Here is the configuration file
for the Pod:

{{< codenew file="pods/two-container-pod.yaml" >}}

In the configuration file, you can see that the Pod has a Volume named
`shared-data`.

The first container listed in the configuration file runs an nginx server. The
mount path for the shared Volume is `/usr/share/nginx/html`.
The second container is based on the debian image, and has a mount path of
`/pod-data`. The second container runs the following command and then terminates.

    echo Hello from the debian container > /pod-data/index.html

Notice that the second container writes the `index.html` file in the root
directory of the nginx server.

Create the Pod and the two Containers:

    kubectl apply -f https://k8s.io/examples/pods/two-container-pod.yaml

View information about the Pod and the Containers:

    kubectl get pod two-containers --output=yaml

Here is a portion of the output:

    apiVersion: v1
    kind: Pod
    metadata:
      ...
      name: two-containers
      namespace: default
      ...
    spec:
      ...
      containerStatuses:

      - containerID: docker://c1d8abd1 ...
        image: debian
        ...
        lastState:
          terminated:
            ...
        name: debian-container
        ...

      - containerID: docker://96c1ff2c5bb ...
        image: nginx
        ...
        name: nginx-container
        ...
        state:
          running:
        ...

You can see that the debian Container has terminated, and the nginx Container
is still running.

Get a shell to nginx Container:

    kubectl exec -it two-containers -c nginx-container -- /bin/bash

In your shell, verify that nginx is running:

    root@two-containers:/# apt-get update
    root@two-containers:/# apt-get install curl procps
    root@two-containers:/# ps aux

The output is similar to this:

    USER       PID  ...  STAT START   TIME COMMAND
    root         1  ...  Ss   21:12   0:00 nginx: master process nginx -g daemon off;

Recall that the debian Container created the `index.html` file in the nginx root
directory. Use `curl` to send a GET request to the nginx server:

```
root@two-containers:/# curl localhost
```

The output shows that nginx serves a web page written by the debian container:

```
Hello from the debian container
```

<!-- discussion -->

## Discussion

The primary reason that Pods can have multiple containers is to support
helper applications that assist a primary application. Typical examples of
helper applications are data pullers, data pushers, and proxies.
Helper and primary applications often need to communicate with each other.
Typically this is done through a shared filesystem, as shown in this exercise,
or through the loopback network interface, localhost. An example of this pattern is a
web server along with a helper program that polls a Git repository for new updates.

The Volume in this exercise provides a way for Containers to communicate during
the life of the Pod. If the Pod is deleted and recreated, any data stored in
the shared Volume is lost.

## {{% heading "whatsnext" %}}


* Learn more about [patterns for composite containers](https://kubernetes.io/blog/2015/06/the-distributed-system-toolkit-patterns).

* Learn about [composite containers for modular architecture](https://www.slideshare.net/Docker/slideshare-burns).

* See [Configuring a Pod to Use a Volume for Storage](/docs/tasks/configure-pod-container/configure-volume-storage/).

* See [Configure a Pod to share process namespace between containers in a Pod](/docs/tasks/configure-pod-container/share-process-namespace/)

* See {{< api-reference page="config-and-storage-resources/volume" >}}.

* See {{< api-reference page="workload-resources/pod-v1" >}}.

