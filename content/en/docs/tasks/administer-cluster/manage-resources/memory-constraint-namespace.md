---
title: Configure Minimum and Maximum Memory Constraints for a Namespace
content_type: task
weight: 30
---


<!-- overview -->

This page shows how to set minimum and maximum values for memory used by Containers
running in a namespace. You specify minimum and maximum memory values in a
{{< api-reference page="policy-resources/limit-range-v1" >}}
object. If a Pod does not meet the constraints imposed by the LimitRange,
it cannot be created in the namespace.




## {{% heading "prerequisites" %}}


{{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}

Each node in your cluster must have at least 1 GiB of memory.




<!-- steps -->

## Create a namespace

Create a namespace so that the resources you create in this exercise are
isolated from the rest of your cluster.

```shell
kubectl create namespace constraints-mem-example
```

## Create a LimitRange and a Pod

Here's the configuration file for a LimitRange:

{{< codenew file="admin/resource/memory-constraints.yaml" >}}

Create the LimitRange:

```shell
kubectl apply -f https://k8s.io/examples/admin/resource/memory-constraints.yaml --namespace=constraints-mem-example
```

View detailed information about the LimitRange:

```shell
kubectl get limitrange mem-min-max-demo-lr --namespace=constraints-mem-example --output=yaml
```

The output shows the minimum and maximum memory constraints as expected. But
notice that even though you didn't specify default values in the configuration
file for the LimitRange, they were created automatically.

```
  limits:
  - default:
      memory: 1Gi
    defaultRequest:
      memory: 1Gi
    max:
      memory: 1Gi
    min:
      memory: 500Mi
    type: Container
```

Now whenever a Container is created in the constraints-mem-example namespace, Kubernetes
performs these steps:

* If the Container does not specify its own memory request and limit, assign the default
memory request and limit to the Container.

* Verify that the Container has a memory request that is greater than or equal to 500 MiB.

* Verify that the Container has a memory limit that is less than or equal to 1 GiB.

Here's the configuration file for a Pod that has one Container. The Container manifest
specifies a memory request of 600 MiB and a memory limit of 800 MiB. These satisfy the
minimum and maximum memory constraints imposed by the LimitRange.

{{< codenew file="admin/resource/memory-constraints-pod.yaml" >}}

Create the Pod:

```shell
kubectl apply -f https://k8s.io/examples/admin/resource/memory-constraints-pod.yaml --namespace=constraints-mem-example
```

Verify that the Pod's Container is running:

```shell
kubectl get pod constraints-mem-demo --namespace=constraints-mem-example
```

View detailed information about the Pod:

```shell
kubectl get pod constraints-mem-demo --output=yaml --namespace=constraints-mem-example
```

The output shows that the Container has a memory request of 600 MiB and a memory limit
of 800 MiB. These satisfy the constraints imposed by the LimitRange.

```yaml
resources:
  limits:
     memory: 800Mi
  requests:
    memory: 600Mi
```

Delete your Pod:

```shell
kubectl delete pod constraints-mem-demo --namespace=constraints-mem-example
```

## Attempt to create a Pod that exceeds the maximum memory constraint

Here's the configuration file for a Pod that has one Container. The Container specifies a
memory request of 800 MiB and a memory limit of 1.5 GiB.

{{< codenew file="admin/resource/memory-constraints-pod-2.yaml" >}}

Attempt to create the Pod:

```shell
kubectl apply -f https://k8s.io/examples/admin/resource/memory-constraints-pod-2.yaml --namespace=constraints-mem-example
```

The output shows that the Pod does not get created, because the Container specifies a memory limit that is
too large:

```
Error from server (Forbidden): error when creating "examples/admin/resource/memory-constraints-pod-2.yaml":
pods "constraints-mem-demo-2" is forbidden: maximum memory usage per Container is 1Gi, but limit is 1536Mi.
```

## Attempt to create a Pod that does not meet the minimum memory request

Here's the configuration file for a Pod that has one Container. The Container specifies a
memory request of 100 MiB and a memory limit of 800 MiB.

{{< codenew file="admin/resource/memory-constraints-pod-3.yaml" >}}

Attempt to create the Pod:

```shell
kubectl apply -f https://k8s.io/examples/admin/resource/memory-constraints-pod-3.yaml --namespace=constraints-mem-example
```

The output shows that the Pod does not get created, because the Container specifies a memory
request that is too small:

```
Error from server (Forbidden): error when creating "examples/admin/resource/memory-constraints-pod-3.yaml":
pods "constraints-mem-demo-3" is forbidden: minimum memory usage per Container is 500Mi, but request is 100Mi.
```

## Create a Pod that does not specify any memory request or limit



Here's the configuration file for a Pod that has one Container. The Container does not
specify a memory request, and it does not specify a memory limit.

{{< codenew file="admin/resource/memory-constraints-pod-4.yaml" >}}

Create the Pod:

```shell
kubectl apply -f https://k8s.io/examples/admin/resource/memory-constraints-pod-4.yaml --namespace=constraints-mem-example
```

View detailed information about the Pod:

```
kubectl get pod constraints-mem-demo-4 --namespace=constraints-mem-example --output=yaml
```

The output shows that the Pod's Container has a memory request of 1 GiB and a memory limit of 1 GiB.
How did the Container get those values?

```
resources:
  limits:
    memory: 1Gi
  requests:
    memory: 1Gi
```

Because your Container did not specify its own memory request and limit, it was given the
[default memory request and limit](/docs/tasks/administer-cluster/manage-resources/memory-default-namespace/)
from the LimitRange.

At this point, your Container might be running or it might not be running. Recall that a prerequisite
for this task is that your Nodes have at least 1 GiB of memory. If each of your Nodes has only
1 GiB of memory, then there is not enough allocatable memory on any Node to accommodate a memory
request of 1 GiB. If you happen to be using Nodes with 2 GiB of memory, then you probably have
enough space to accommodate the 1 GiB request.

Delete your Pod:

```
kubectl delete pod constraints-mem-demo-4 --namespace=constraints-mem-example
```

## Enforcement of minimum and maximum memory constraints

The maximum and minimum memory constraints imposed on a namespace by a LimitRange are enforced only
when a Pod is created or updated. If you change the LimitRange, it does not affect
Pods that were created previously.

## Motivation for minimum and maximum memory constraints

As a cluster administrator, you might want to impose restrictions on the amount of memory that Pods can use.
For example:

* Each Node in a cluster has 2 GB of memory. You do not want to accept any Pod that requests
more than 2 GB of memory, because no Node in the cluster can support the request.

* A cluster is shared by your production and development departments.
You want to allow production workloads to consume up to 8 GB of memory, but
you want development workloads to be limited to 512 MB. You create separate namespaces
for production and development, and you apply memory constraints to each namespace.

## Clean up

Delete your namespace:

```shell
kubectl delete namespace constraints-mem-example
```



## {{% heading "whatsnext" %}}


### For cluster administrators

* [Configure Default Memory Requests and Limits for a Namespace](/docs/tasks/administer-cluster/manage-resources/memory-default-namespace/)

* [Configure Default CPU Requests and Limits for a Namespace](/docs/tasks/administer-cluster/manage-resources/cpu-default-namespace/)

* [Configure Minimum and Maximum CPU Constraints for a Namespace](/docs/tasks/administer-cluster/manage-resources/cpu-constraint-namespace/)

* [Configure Memory and CPU Quotas for a Namespace](/docs/tasks/administer-cluster/manage-resources/quota-memory-cpu-namespace/)

* [Configure a Pod Quota for a Namespace](/docs/tasks/administer-cluster/manage-resources/quota-pod-namespace/)

* [Configure Quotas for API Objects](/docs/tasks/administer-cluster/quota-api-object/)

### For app developers

* [Assign Memory Resources to Containers and Pods](/docs/tasks/configure-pod-container/assign-memory-resource/)

* [Assign CPU Resources to Containers and Pods](/docs/tasks/configure-pod-container/assign-cpu-resource/)

* [Configure Quality of Service for Pods](/docs/tasks/configure-pod-container/quality-service-pod/)







