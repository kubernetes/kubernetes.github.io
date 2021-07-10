---
title: Attach Handlers to Container Lifecycle Events
content_type: task
weight: 140
---

<!-- overview -->

This page shows how to attach handlers to Container lifecycle events. Kubernetes supports
the postStart and preStop events. Kubernetes sends the postStart event immediately
after a Container is started, and it sends the preStop event immediately before the
Container is terminated. A Container may specify one handler per event.




## {{% heading "prerequisites" %}}


{{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}




<!-- steps -->

## Define postStart and preStop handlers

In this exercise, you create a Pod that has one Container. The Container has handlers
for the postStart and preStop events.

Here is the configuration file for the Pod:

{{< codenew file="pods/lifecycle-events.yaml" >}}

In the configuration file, you can see that the postStart command writes a `message`
file to the Container's `/usr/share` directory. The preStop command shuts down
nginx gracefully. This is helpful if the Container is being terminated because of a failure.

Create the Pod:

    kubectl apply -f https://k8s.io/examples/pods/lifecycle-events.yaml

Verify that the Container in the Pod is running:

    kubectl get pod lifecycle-demo

Get a shell into the Container running in your Pod:

    kubectl exec -it lifecycle-demo -- /bin/bash

In your shell, verify that the `postStart` handler created the `message` file:

    root@lifecycle-demo:/# cat /usr/share/message

The output shows the text written by the postStart handler:

    Hello from the postStart handler





<!-- discussion -->

## Discussion

Kubernetes sends the postStart event immediately after the Container is created.
There is no guarantee, however, that the postStart handler is called before
the Container's entrypoint is called. The postStart handler runs asynchronously
relative to the Container's code, but Kubernetes' management of the container
blocks until the postStart handler completes. The Container's status is not
set to RUNNING until the postStart handler completes.

Kubernetes sends the preStop event immediately before the Container is terminated.
Kubernetes' management of the Container blocks until the preStop handler completes,
unless the Pod's grace period expires. For more details, see
[Pod Lifecycle](/docs/concepts/workloads/pods/pod-lifecycle/).

{{< note >}}
Kubernetes only sends the preStop event when a Pod is *terminated*.
This means that the preStop hook is not invoked when the Pod is *completed*. 
This limitation is tracked in [issue #55087](https://github.com/kubernetes/kubernetes/issues/55807).
{{< /note >}}




## {{% heading "whatsnext" %}}


* Learn more about [Container lifecycle hooks](/docs/concepts/containers/container-lifecycle-hooks/).
* Learn more about the [lifecycle of a Pod](/docs/concepts/workloads/pods/pod-lifecycle/).


### Reference

* {{< api-reference page="workload-resources/pod-v1" anchor="Lifecycle" >}}
* {{< api-reference page="workload-resources/pod-v1" anchor="Container" >}}
* See `terminationGracePeriodSeconds` in {{< api-reference page="workload-resources/pod-v1" anchor="Lifecycle" text="PodSpec" >}}




