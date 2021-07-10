---
title: Assign CPU Resources to Containers and Pods
content_type: task
weight: 20
---

<!-- overview -->

This page shows how to assign a CPU *request* and a CPU *limit* to
a container. Containers cannot use more CPU than the configured limit.
Provided the system has CPU time free, a container is guaranteed to be
allocated as much CPU as it requests.




## {{% heading "prerequisites" %}}


{{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}

Your cluster must have at least 1 CPU available for use to run the task examples.

A few of the steps on this page require you to run the
[metrics-server](https://github.com/kubernetes-sigs/metrics-server)
service in your cluster. If you have the metrics-server
running, you can skip those steps.

If you are running {{< glossary_tooltip term_id="minikube" >}}, run the
following command to enable metrics-server:

```shell
minikube addons enable metrics-server
```

To see whether metrics-server (or another provider of the resource metrics
API, `metrics.k8s.io`) is running, type the following command:

```shell
kubectl get apiservices
```

If the resource metrics API is available, the output will include a
reference to `metrics.k8s.io`.


```
NAME
v1beta1.metrics.k8s.io
```




<!-- steps -->

## Create a namespace

Create a {{< glossary_tooltip term_id="namespace" >}} so that the resources you
create in this exercise are isolated from the rest of your cluster.

```shell
kubectl create namespace cpu-example
```

## Specify a CPU request and a CPU limit

To specify a CPU request for a container, include the `resources:requests` field
in the Container resource manifest. To specify a CPU limit, include `resources:limits`.

In this exercise, you create a Pod that has one container. The container has a request
of 0.5 CPU and a limit of 1 CPU. Here is the configuration file for the Pod:

{{< codenew file="pods/resource/cpu-request-limit.yaml" >}}

The `args` section of the configuration file provides arguments for the container when it starts.
The `-cpus "2"` argument tells the Container to attempt to use 2 CPUs.

Create the Pod:

```shell
kubectl apply -f https://k8s.io/examples/pods/resource/cpu-request-limit.yaml --namespace=cpu-example
```

Verify that the Pod is running:

```shell
kubectl get pod cpu-demo --namespace=cpu-example
```

View detailed information about the Pod:

```shell
kubectl get pod cpu-demo --output=yaml --namespace=cpu-example
```

The output shows that the one container in the Pod has a CPU request of 500 milliCPU
and a CPU limit of 1 CPU.

```yaml
resources:
  limits:
    cpu: "1"
  requests:
    cpu: 500m
```

Use `kubectl top` to fetch the metrics for the pod:

```shell
kubectl top pod cpu-demo --namespace=cpu-example
```

This example output shows that the Pod is using 974 milliCPU, which is
slightly less than the limit of 1 CPU specified in the Pod configuration.

```
NAME                        CPU(cores)   MEMORY(bytes)
cpu-demo                    974m         <something>
```

Recall that by setting `-cpu "2"`, you configured the Container to attempt to use 2 CPUs, but the Container is only being allowed to use about 1 CPU. The container's CPU use is being throttled, because the container is attempting to use more CPU resources than its limit.

{{< note >}}
Another possible explanation for the CPU use being below 1.0 is that the Node might not have
enough CPU resources available. Recall that the prerequisites for this exercise require your cluster to have at least 1 CPU available for use. If your Container runs on a Node that has only 1 CPU, the Container cannot use more than 1 CPU regardless of the CPU limit specified for the Container.
{{< /note >}}

## CPU units

The CPU resource is measured in *CPU* units. One CPU, in Kubernetes, is equivalent to:

* 1 AWS vCPU
* 1 GCP Core
* 1 Azure vCore
* 1 Hyperthread on a bare-metal Intel processor with Hyperthreading

Fractional values are allowed. A Container that requests 0.5 CPU is guaranteed half as much
CPU as a Container that requests 1 CPU. You can use the suffix m to mean milli. For example
100m CPU, 100 milliCPU, and 0.1 CPU are all the same. Precision finer than 1m is not allowed.

CPU is always requested as an absolute quantity, never as a relative quantity; 0.1 is the same
amount of CPU on a single-core, dual-core, or 48-core machine.

Delete your Pod:

```shell
kubectl delete pod cpu-demo --namespace=cpu-example
```

## Specify a CPU request that is too big for your Nodes

CPU requests and limits are associated with Containers, but it is useful to think
of a Pod as having a CPU request and limit. The CPU request for a Pod is the sum
of the CPU requests for all the Containers in the Pod. Likewise, the CPU limit for
a Pod is the sum of the CPU limits for all the Containers in the Pod.

Pod scheduling is based on requests. A Pod is scheduled to run on a Node only if
the Node has enough CPU resources available to satisfy the Pod CPU request.

In this exercise, you create a Pod that has a CPU request so big that it exceeds
the capacity of any Node in your cluster. Here is the configuration file for a Pod
that has one Container. The Container requests 100 CPU, which is likely to exceed the
capacity of any Node in your cluster.

{{< codenew file="pods/resource/cpu-request-limit-2.yaml" >}}

Create the Pod:

```shell
kubectl apply -f https://k8s.io/examples/pods/resource/cpu-request-limit-2.yaml --namespace=cpu-example
```

View the Pod status:

```shell
kubectl get pod cpu-demo-2 --namespace=cpu-example
```

The output shows that the Pod status is Pending. That is, the Pod has not been
scheduled to run on any Node, and it will remain in the Pending state indefinitely:


```
NAME         READY     STATUS    RESTARTS   AGE
cpu-demo-2   0/1       Pending   0          7m
```

View detailed information about the Pod, including events:


```shell
kubectl describe pod cpu-demo-2 --namespace=cpu-example
```

The output shows that the Container cannot be scheduled because of insufficient
CPU resources on the Nodes:


```
Events:
  Reason                        Message
  ------                        -------
  FailedScheduling      No nodes are available that match all of the following predicates:: Insufficient cpu (3).
```

Delete your Pod:

```shell
kubectl delete pod cpu-demo-2 --namespace=cpu-example
```

## If you do not specify a CPU limit

If you do not specify a CPU limit for a Container, then one of these situations applies:

* The Container has no upper bound on the CPU resources it can use. The Container
could use all of the CPU resources available on the Node where it is running.

* The Container is running in a namespace that has a default CPU limit, and the
Container is automatically assigned the default limit. Cluster administrators can use a
{{< api-reference page="policy-resources/limit-range-v1" >}}
to specify a default value for the CPU limit.

## If you specify a CPU limit but do not specify a CPU request

If you specify a CPU limit for a Container but do not specify a CPU request, Kubernetes automatically
assigns a CPU request that matches the limit. Similarly, if a Container specifies its own memory limit,
but does not specify a memory request, Kubernetes automatically assigns a memory request that matches
the limit.

## Motivation for CPU requests and limits

By configuring the CPU requests and limits of the Containers that run in your
cluster, you can make efficient use of the CPU resources available on your cluster
Nodes. By keeping a Pod CPU request low, you give the Pod a good chance of being
scheduled. By having a CPU limit that is greater than the CPU request, you accomplish two things:

* The Pod can have bursts of activity where it makes use of CPU resources that happen to be available.
* The amount of CPU resources a Pod can use during a burst is limited to some reasonable amount.

## Clean up

Delete your namespace:

```shell
kubectl delete namespace cpu-example
```



## {{% heading "whatsnext" %}}



### For app developers

* [Assign Memory Resources to Containers and Pods](/docs/tasks/configure-pod-container/assign-memory-resource/)

* [Configure Quality of Service for Pods](/docs/tasks/configure-pod-container/quality-service-pod/)

### For cluster administrators

* [Configure Default Memory Requests and Limits for a Namespace](/docs/tasks/administer-cluster/manage-resources/memory-default-namespace/)

* [Configure Default CPU Requests and Limits for a Namespace](/docs/tasks/administer-cluster/manage-resources/cpu-default-namespace/)

* [Configure Minimum and Maximum Memory Constraints for a Namespace](/docs/tasks/administer-cluster/manage-resources/memory-constraint-namespace/)

* [Configure Minimum and Maximum CPU Constraints for a Namespace](/docs/tasks/administer-cluster/manage-resources/cpu-constraint-namespace/)

* [Configure Memory and CPU Quotas for a Namespace](/docs/tasks/administer-cluster/manage-resources/quota-memory-cpu-namespace/)

* [Configure a Pod Quota for a Namespace](/docs/tasks/administer-cluster/manage-resources/quota-pod-namespace/)

* [Configure Quotas for API Objects](/docs/tasks/administer-cluster/quota-api-object/)


