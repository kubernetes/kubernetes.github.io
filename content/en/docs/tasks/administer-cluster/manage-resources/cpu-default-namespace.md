---
title: Configure Default CPU Requests and Limits for a Namespace
content_type: task
weight: 20
---

<!-- overview -->

This page shows how to configure default CPU requests and limits for a namespace.
A Kubernetes cluster can be divided into namespaces. If a Container is created in a namespace
that has a default CPU limit, and the Container does not specify its own CPU limit, then
the Container is assigned the default CPU limit. Kubernetes assigns a default CPU request
under certain conditions that are explained later in this topic. Kubernetes will also not allow 
a pod creation if the pod requests more than the default CPU limit configured in the LimitRange 
that is applied to the namespace where the pod creation request is made.



## {{% heading "prerequisites" %}}


{{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}


<!-- steps -->

## Create a namespace

Create a namespace so that the resources you create in this exercise are
isolated from the rest of your cluster.

```shell
kubectl create namespace default-cpu-example
```

## Create a LimitRange and a Pod

Here's the configuration file for a LimitRange object. The configuration specifies
a default CPU request and a default CPU limit.

{{< codenew file="admin/resource/cpu-defaults.yaml" >}}

Create the LimitRange in the default-cpu-example namespace:

```shell
kubectl apply -f https://k8s.io/examples/admin/resource/cpu-defaults.yaml --namespace=default-cpu-example
```

Now if a Container is created in the default-cpu-example namespace, and the
Container does not specify its own values for CPU request and CPU limit,
the Container is given a default CPU request of 0.5 and a default
CPU limit of 1.

Here's the configuration file for a Pod that has one Container. The Container
does not specify a CPU request and limit.

{{< codenew file="admin/resource/cpu-defaults-pod.yaml" >}}

Create the Pod.

```shell
kubectl apply -f https://k8s.io/examples/admin/resource/cpu-defaults-pod.yaml --namespace=default-cpu-example
```

View the Pod's specification:

```shell
kubectl get pod default-cpu-demo --output=yaml --namespace=default-cpu-example
```

The output shows that the Pod's Container has a CPU request of 500 millicpus and
a CPU limit of 1 cpu. These are the default values specified by the LimitRange.

```shell
containers:
- image: nginx
  imagePullPolicy: Always
  name: default-cpu-demo-ctr
  resources:
    limits:
      cpu: "1"
    requests:
      cpu: 500m
```

## What if you specify a Container's limit, but not its request?

Here's the configuration file for a Pod that has one Container. The Container
specifies a CPU limit, but not a request:

{{< codenew file="admin/resource/cpu-defaults-pod-2.yaml" >}}

Create the Pod:


```shell
kubectl apply -f https://k8s.io/examples/admin/resource/cpu-defaults-pod-2.yaml --namespace=default-cpu-example
```

View the Pod specification:

```
kubectl get pod default-cpu-demo-2 --output=yaml --namespace=default-cpu-example
```

The output shows that the Container's CPU request is set to match its CPU limit.
Notice that the Container was not assigned the default CPU request value of 0.5 cpu.

```
resources:
  limits:
    cpu: "1"
  requests:
    cpu: "1"
```

## What if you specify a Container's request, but not its limit?

Here's the configuration file for a Pod that has one Container. The Container
specifies a CPU request, but not a limit:

{{< codenew file="admin/resource/cpu-defaults-pod-3.yaml" >}}

Create the Pod:

```shell
kubectl apply -f https://k8s.io/examples/admin/resource/cpu-defaults-pod-3.yaml --namespace=default-cpu-example
```

View the Pod specification:

```
kubectl get pod default-cpu-demo-3 --output=yaml --namespace=default-cpu-example
```

The output shows that the Container's CPU request is set to the value specified in the
Container's configuration file. The Container's CPU limit is set to 1 cpu, which is the
default CPU limit for the namespace.

```
resources:
  limits:
    cpu: "1"
  requests:
    cpu: 750m
```

## Motivation for default CPU limits and requests

If your namespace has a
[resource quota](/docs/tasks/administer-cluster/manage-resources/quota-memory-cpu-namespace/),
it is helpful to have a default value in place for CPU limit.
Here are two of the restrictions that a resource quota imposes on a namespace:

* Every Container that runs in the namespace must have its own CPU limit.
* The total amount of CPU used by all Containers in the namespace must not exceed a specified limit.

If a Container does not specify its own CPU limit, it is given the default limit, and then
it can be allowed to run in a namespace that is restricted by a quota.

## Clean up

Delete your namespace:

```shell
kubectl delete namespace default-cpu-example
```



## {{% heading "whatsnext" %}}


### For cluster administrators

* [Configure Default Memory Requests and Limits for a Namespace](/docs/tasks/administer-cluster/manage-resources/memory-default-namespace/)

* [Configure Minimum and Maximum Memory Constraints for a Namespace](/docs/tasks/administer-cluster/manage-resources/memory-constraint-namespace/)

* [Configure Minimum and Maximum CPU Constraints for a Namespace](/docs/tasks/administer-cluster/manage-resources/cpu-constraint-namespace/)

* [Configure Memory and CPU Quotas for a Namespace](/docs/tasks/administer-cluster/manage-resources/quota-memory-cpu-namespace/)

* [Configure a Pod Quota for a Namespace](/docs/tasks/administer-cluster/manage-resources/quota-pod-namespace/)

* [Configure Quotas for API Objects](/docs/tasks/administer-cluster/quota-api-object/)

### For app developers

* [Assign Memory Resources to Containers and Pods](/docs/tasks/configure-pod-container/assign-memory-resource/)

* [Assign CPU Resources to Containers and Pods](/docs/tasks/configure-pod-container/assign-cpu-resource/)

* [Configure Quality of Service for Pods](/docs/tasks/configure-pod-container/quality-service-pod/)




