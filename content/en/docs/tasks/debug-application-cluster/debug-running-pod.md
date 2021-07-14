---
reviewers:
- verb
- soltysh
title: Debug Running Pods
content_type: task
---

<!-- overview -->

This page explains how to debug Pods running (or crashing) on a Node.



## {{% heading "prerequisites" %}}


* Your {{< glossary_tooltip text="Pod" term_id="pod" >}} should already be
  scheduled and running. If your Pod is not yet running, start with [Troubleshoot
  Applications](/docs/tasks/debug-application-cluster/debug-application/).
* For some of the advanced debugging steps you need to know on which Node the
  Pod is running and have shell access to run commands on that Node. You don't
  need that access to run the standard debug steps that use `kubectl`.



<!-- steps -->

## Examining pod logs {#examine-pod-logs}

First, look at the logs of the affected container:

```shell
kubectl logs ${POD_NAME} ${CONTAINER_NAME}
```

If your container has previously crashed, you can access the previous container's crash log with:

```shell
kubectl logs --previous ${POD_NAME} ${CONTAINER_NAME}
```

## Debugging with container exec {#container-exec}

If the {{< glossary_tooltip text="container image" term_id="image" >}} includes
debugging utilities, as is the case with images built from Linux and Windows OS
base images, you can run commands inside a specific container with
`kubectl exec`:

```shell
kubectl exec ${POD_NAME} -c ${CONTAINER_NAME} -- ${CMD} ${ARG1} ${ARG2} ... ${ARGN}
```

{{< note >}}
`-c ${CONTAINER_NAME}` is optional. You can omit it for Pods that only contain a single container.
{{< /note >}}

As an example, to look at the logs from a running Cassandra pod, you might run

```shell
kubectl exec cassandra -- cat /var/log/cassandra/system.log
```

You can run a shell that's connected to your terminal using the `-i` and `-t`
arguments to `kubectl exec`, for example:

```shell
kubectl exec -it cassandra -- sh
```

For more details, see [Get a Shell to a Running Container](
/docs/tasks/debug-application-cluster/get-shell-running-container/).

## Debugging with an ephemeral debug container {#ephemeral-container}

{{< feature-state state="alpha" for_k8s_version="v1.22" >}}

{{< glossary_tooltip text="Ephemeral containers" term_id="ephemeral-container" >}}
are useful for interactive troubleshooting when `kubectl exec` is insufficient
because a container has crashed or a container image doesn't include debugging
utilities, such as with [distroless images](
https://github.com/GoogleContainerTools/distroless).

### Example debugging using ephemeral containers {#ephemeral-container-example}

{{< note >}}
The examples in this section require the `EphemeralContainers` [feature gate](
/docs/reference/command-line-tools-reference/feature-gates/) enabled in your
cluster and `kubectl` version v1.22 or later.
{{< /note >}}

You can use the `kubectl debug` command to add ephemeral containers to a
running Pod. First, create a pod for the example:

```shell
kubectl run ephemeral-demo --image=k8s.gcr.io/pause:3.1 --restart=Never
```

The examples in this section use the `pause` container image because it does not
contain debugging utilities, but this method works with all container
images.

If you attempt to use `kubectl exec` to create a shell you will see an error
because there is no shell in this container image.

```shell
kubectl exec -it ephemeral-demo -- sh
```

```
OCI runtime exec failed: exec failed: container_linux.go:346: starting container process caused "exec: \"sh\": executable file not found in $PATH": unknown
```

You can instead add a debugging container using `kubectl debug`. If you
specify the `-i`/`--interactive` argument, `kubectl` will automatically attach
to the console of the Ephemeral Container.

```shell
kubectl debug -it ephemeral-demo --image=busybox --target=ephemeral-demo
```

```
Defaulting debug container name to debugger-8xzrl.
If you don't see a command prompt, try pressing enter.
/ #
```

This command adds a new busybox container and attaches to it. The `--target`
parameter targets the process namespace of another container. It's necessary
here because `kubectl run` does not enable [process namespace sharing](
/docs/tasks/configure-pod-container/share-process-namespace/) in the pod it
creates.

{{< note >}}
The `--target` parameter must be supported by the {{< glossary_tooltip
text="Container Runtime" term_id="container-runtime" >}}. When not supported,
the Ephemeral Container may not be started, or it may be started with an
isolated process namespace so that `ps` does not reveal processes in other
containers.
{{< /note >}}

You can view the state of the newly created ephemeral container using `kubectl describe`:

```shell
kubectl describe pod ephemeral-demo
```

```
...
Ephemeral Containers:
  debugger-8xzrl:
    Container ID:   docker://b888f9adfd15bd5739fefaa39e1df4dd3c617b9902082b1cfdc29c4028ffb2eb
    Image:          busybox
    Image ID:       docker-pullable://busybox@sha256:1828edd60c5efd34b2bf5dd3282ec0cc04d47b2ff9caa0b6d4f07a21d1c08084
    Port:           <none>
    Host Port:      <none>
    State:          Running
      Started:      Wed, 12 Feb 2020 14:25:42 +0100
    Ready:          False
    Restart Count:  0
    Environment:    <none>
    Mounts:         <none>
...
```

Use `kubectl delete` to remove the Pod when you're finished:

```shell
kubectl delete pod ephemeral-demo
```

## Debugging using a copy of the Pod

Sometimes Pod configuration options make it difficult to troubleshoot in certain
situations. For example, you can't run `kubectl exec` to troubleshoot your
container if your container image does not include a shell or if your application
crashes on startup. In these situations you can use `kubectl debug` to create a
copy of the Pod with configuration values changed to aid debugging.

### Copying a Pod while adding a new container

Adding a new container can be useful when your application is running but not
behaving as you expect and you'd like to add additional troubleshooting
utilities to the Pod.

For example, maybe your application's container images are built on `busybox`
but you need debugging utilities not included in `busybox`. You can simulate
this scenario using `kubectl run`:

```shell
kubectl run myapp --image=busybox --restart=Never -- sleep 1d
```

Run this command to create a copy of `myapp` named `myapp-debug` that adds a
new Ubuntu container for debugging:

```shell
kubectl debug myapp -it --image=ubuntu --share-processes --copy-to=myapp-debug
```

```
Defaulting debug container name to debugger-w7xmf.
If you don't see a command prompt, try pressing enter.
root@myapp-debug:/#
```

{{< note >}}
* `kubectl debug` automatically generates a container name if you don't choose
  one using the `--container` flag.
* The `-i` flag causes `kubectl debug` to attach to the new container by
  default.  You can prevent this by specifying `--attach=false`. If your session
  becomes disconnected you can reattach using `kubectl attach`.
* The `--share-processes` allows the containers in this Pod to see processes
  from the other containers in the Pod. For more information about how this
  works, see [Share Process Namespace between Containers in a Pod](
  /docs/tasks/configure-pod-container/share-process-namespace/).
{{< /note >}}

Don't forget to clean up the debugging Pod when you're finished with it:

```shell
kubectl delete pod myapp myapp-debug
```

### Copying a Pod while changing its command

Sometimes it's useful to change the command for a container, for example to
add a debugging flag or because the application is crashing.

To simulate a crashing application, use `kubectl run` to create a container
that immediately exits:

```
kubectl run --image=busybox myapp -- false
```

You can see using `kubectl describe pod myapp` that this container is crashing:

```
Containers:
  myapp:
    Image:         busybox
    ...
    Args:
      false
    State:          Waiting
      Reason:       CrashLoopBackOff
    Last State:     Terminated
      Reason:       Error
      Exit Code:    1
```

You can use `kubectl debug` to create a copy of this Pod with the command
changed to an interactive shell:

```
kubectl debug myapp -it --copy-to=myapp-debug --container=myapp -- sh
```

```
If you don't see a command prompt, try pressing enter.
/ #
```

Now you have an interactive shell that you can use to perform tasks like
checking filesystem paths or running the container command manually.

{{< note >}}
* To change the command of a specific container you must
  specify its name using `--container` or `kubectl debug` will instead
  create a new container to run the command you specified.
* The `-i` flag causes `kubectl debug` to attach to the container by default.
  You can prevent this by specifying `--attach=false`. If your session becomes
  disconnected you can reattach using `kubectl attach`.
{{< /note >}}

Don't forget to clean up the debugging Pod when you're finished with it:

```shell
kubectl delete pod myapp myapp-debug
```

### Copying a Pod while changing container images

In some situations you may want to change a misbehaving Pod from its normal
production container images to an image containing a debugging build or
additional utilities.

As an example, create a Pod using `kubectl run`:

```
kubectl run myapp --image=busybox --restart=Never -- sleep 1d
```

Now use `kubectl debug` to make a copy and change its container image
to `ubuntu`:

```
kubectl debug myapp --copy-to=myapp-debug --set-image=*=ubuntu
```

The syntax of `--set-image` uses the same `container_name=image` syntax as
`kubectl set image`. `*=ubuntu` means change the image of all containers
to `ubuntu`.

Don't forget to clean up the debugging Pod when you're finished with it:

```shell
kubectl delete pod myapp myapp-debug
```

## Debugging via a shell on the node {#node-shell-session}

If none of these approaches work, you can find the Node on which the Pod is
running and create a privileged Pod running in the host namespaces. To create
an interactive shell on a node using `kubectl debug`, run:

```shell
kubectl debug node/mynode -it --image=ubuntu
```

```
Creating debugging pod node-debugger-mynode-pdx84 with container debugger on node mynode.
If you don't see a command prompt, try pressing enter.
root@ek8s:/#
```

When creating a debugging session on a node, keep in mind that:

* `kubectl debug` automatically generates the name of the new Pod based on
  the name of the Node.
* The container runs in the host IPC, Network, and PID namespaces.
* The root filesystem of the Node will be mounted at `/host`.

Don't forget to clean up the debugging Pod when you're finished with it:

```shell
kubectl delete pod node-debugger-mynode-pdx84
```
