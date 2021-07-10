---
reviewers:
- verb
- yujuhong
title: Ephemeral Containers
content_type: concept
weight: 80
---

<!-- overview -->

{{< feature-state state="alpha" for_k8s_version="v1.16" >}}

This page provides an overview of ephemeral containers: a special type of container
that runs temporarily in an existing {{< glossary_tooltip term_id="pod" >}} to
accomplish user-initiated actions such as troubleshooting. You use ephemeral
containers to inspect services rather than to build applications.

{{< warning >}}
Ephemeral containers are in early alpha state and are not suitable for production
clusters. In accordance with the [Kubernetes Deprecation Policy](
/docs/reference/using-api/deprecation-policy/), this alpha feature could change
significantly in the future or be removed entirely.
{{< /warning >}}



<!-- body -->

## Understanding ephemeral containers

{{< glossary_tooltip text="Pods" term_id="pod" >}} are the fundamental building
block of Kubernetes applications. Since Pods are intended to be disposable and
replaceable, you cannot add a container to a Pod once it has been created.
Instead, you usually delete and replace Pods in a controlled fashion using
{{< glossary_tooltip text="deployments" term_id="deployment" >}}.

Sometimes it's necessary to inspect the state of an existing Pod, however, for
example to troubleshoot a hard-to-reproduce bug. In these cases you can run
an ephemeral container in an existing Pod to inspect its state and run
arbitrary commands.

### What is an ephemeral container?

Ephemeral containers differ from other containers in that they lack guarantees
for resources or execution, and they will never be automatically restarted, so
they are not appropriate for building applications.  Ephemeral containers are
described using the same `ContainerSpec` as regular containers, but many fields
are incompatible and disallowed for ephemeral containers.

- Ephemeral containers may not have ports, so fields such as `ports`,
  `livenessProbe`, `readinessProbe` are disallowed.
- Pod resource allocations are immutable, so setting `resources` is disallowed.
- For a complete list of allowed fields, see the
{{< api-reference page="workload-resources/ephemeral-containers-v1" >}}
reference documentation.

Ephemeral containers are created using a special `ephemeralcontainers` handler
in the API rather than by adding them directly to `pod.spec`, so it's not
possible to add an ephemeral container using `kubectl edit`.

Like regular containers, you may not change or remove an ephemeral container
after you have added it to a Pod.

## Uses for ephemeral containers

Ephemeral containers are useful for interactive troubleshooting when `kubectl
exec` is insufficient because a container has crashed or a container image
doesn't include debugging utilities.

In particular, [distroless images](https://github.com/GoogleContainerTools/distroless)
enable you to deploy minimal container images that reduce attack surface
and exposure to bugs and vulnerabilities. Since distroless images do not include a
shell or any debugging utilities, it's difficult to troubleshoot distroless
images using `kubectl exec` alone.

When using ephemeral containers, it's helpful to enable [process namespace
sharing](/docs/tasks/configure-pod-container/share-process-namespace/) so
you can view processes in other containers.

See [Debugging with Ephemeral Debug Container](
/docs/tasks/debug-application-cluster/debug-running-pod/#ephemeral-container)
for examples of troubleshooting using ephemeral containers.

## Ephemeral containers API

{{< note >}}
The examples in this section require the `EphemeralContainers` [feature
gate](/docs/reference/command-line-tools-reference/feature-gates/) to be
enabled, and Kubernetes client and server version v1.16 or later.
{{< /note >}}

The examples in this section demonstrate how ephemeral containers appear in
the API. You would normally use `kubectl debug` or another `kubectl`
[plugin](/docs/tasks/extend-kubectl/kubectl-plugins/) to automate these steps
rather than invoking the API directly.

Ephemeral containers are created using the `ephemeralcontainers` subresource
of Pod, which can be demonstrated using `kubectl --raw`. First describe
the ephemeral container to add as an `EphemeralContainers` list:

```json
{
    "apiVersion": "v1",
    "kind": "EphemeralContainers",
    "metadata": {
        "name": "example-pod"
    },
    "ephemeralContainers": [{
        "command": [
            "sh"
        ],
        "image": "busybox",
        "imagePullPolicy": "IfNotPresent",
        "name": "debugger",
        "stdin": true,
        "tty": true,
        "terminationMessagePolicy": "File"
    }]
}
```

To update the ephemeral containers of the already running `example-pod`:

```shell
kubectl replace --raw /api/v1/namespaces/default/pods/example-pod/ephemeralcontainers  -f ec.json
```

This will return the new list of ephemeral containers:

```json
{
   "kind":"EphemeralContainers",
   "apiVersion":"v1",
   "metadata":{
      "name":"example-pod",
      "namespace":"default",
      "selfLink":"/api/v1/namespaces/default/pods/example-pod/ephemeralcontainers",
      "uid":"a14a6d9b-62f2-4119-9d8e-e2ed6bc3a47c",
      "resourceVersion":"15886",
      "creationTimestamp":"2019-08-29T06:41:42Z"
   },
   "ephemeralContainers":[
      {
         "name":"debugger",
         "image":"busybox",
         "command":[
            "sh"
         ],
         "resources":{

         },
         "terminationMessagePolicy":"File",
         "imagePullPolicy":"IfNotPresent",
         "stdin":true,
         "tty":true
      }
   ]
}
```

You can view the state of the newly created ephemeral container using `kubectl describe`:

```shell
kubectl describe pod example-pod
```

```
...
Ephemeral Containers:
  debugger:
    Container ID:  docker://cf81908f149e7e9213d3c3644eda55c72efaff67652a2685c1146f0ce151e80f
    Image:         busybox
    Image ID:      docker-pullable://busybox@sha256:9f1003c480699be56815db0f8146ad2e22efea85129b5b5983d0e0fb52d9ab70
    Port:          <none>
    Host Port:     <none>
    Command:
      sh
    State:          Running
      Started:      Thu, 29 Aug 2019 06:42:21 +0000
    Ready:          False
    Restart Count:  0
    Environment:    <none>
    Mounts:         <none>
...
```

You can interact with the new ephemeral container in the same way as other
containers using `kubectl attach`, `kubectl exec`, and `kubectl logs`, for
example:

```shell
kubectl attach -it example-pod -c debugger
```


