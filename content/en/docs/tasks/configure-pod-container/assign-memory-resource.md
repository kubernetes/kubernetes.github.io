---
title: Assign Memory Resources to Containers and Pods
content_type: task
weight: 10
---

<!-- overview -->

This page shows how to assign a memory *request* and a memory *limit* to a
Container. A Container is guaranteed to have as much memory as it requests,
but is not allowed to use more memory than its limit.




## {{% heading "prerequisites" %}}


{{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}

Each node in your cluster must have at least 300 MiB of memory.

A few of the steps on this page require you to run the
[metrics-server](https://github.com/kubernetes-sigs/metrics-server)
service in your cluster. If you have the metrics-server
running, you can skip those steps.

If you are running Minikube, run the following command to enable the
metrics-server:

```shell
minikube addons enable metrics-server
```

To see whether the metrics-server is running, or another provider of the resource metrics
API (`metrics.k8s.io`), run the following command:

```shell
kubectl get apiservices
```

If the resource metrics API is available, the output includes a
reference to `metrics.k8s.io`.

```shell
NAME
v1beta1.metrics.k8s.io
```



<!-- steps -->

## Create a namespace

Create a namespace so that the resources you create in this exercise are
isolated from the rest of your cluster.

```shell
kubectl create namespace mem-example
```

## Specify a memory request and a memory limit

To specify a memory request for a Container, include the `resources:requests` field
in the Container's resource manifest. To specify a memory limit, include `resources:limits`.

In this exercise, you create a Pod that has one Container. The Container has a memory
request of 100 MiB and a memory limit of 200 MiB. Here's the configuration file
for the Pod:

{{< codenew file="pods/resource/memory-request-limit.yaml" >}}

The `args` section in the configuration file provides arguments for the Container when it starts.
The `"--vm-bytes", "150M"` arguments tell the Container to attempt to allocate 150 MiB of memory.

Create the Pod:

```shell
kubectl apply -f https://k8s.io/examples/pods/resource/memory-request-limit.yaml --namespace=mem-example
```

Verify that the Pod Container is running:

```shell
kubectl get pod memory-demo --namespace=mem-example
```

View detailed information about the Pod:

```shell
kubectl get pod memory-demo --output=yaml --namespace=mem-example
```

The output shows that the one Container in the Pod has a memory request of 100 MiB
and a memory limit of 200 MiB.


```yaml
...
resources:
  limits:
    memory: 200Mi
  requests:
    memory: 100Mi
...
```

Run `kubectl top` to fetch the metrics for the pod:

```shell
kubectl top pod memory-demo --namespace=mem-example
```

The output shows that the Pod is using about 162,900,000 bytes of memory, which
is about 150 MiB. This is greater than the Pod's 100 MiB request, but within the
Pod's 200 MiB limit.

```
NAME                        CPU(cores)   MEMORY(bytes)
memory-demo                 <something>  162856960
```

Delete your Pod:

```shell
kubectl delete pod memory-demo --namespace=mem-example
```

## Exceed a Container's memory limit

A Container can exceed its memory request if the Node has memory available. But a Container
is not allowed to use more than its memory limit. If a Container consumes more memory than
its limit, the Container becomes a candidate for termination. If the Container continues to
consume memory beyond its limit, the Container is terminated. If a terminated Container can be
restarted, the kubelet restarts it, as with any other type of runtime failure.

In this exercise, you create a Pod that attempts to consume more memory than its limit.
Here is the configuration file for a Pod that has one Container with a
memory request of 50 MiB and a memory limit of 100 MiB:

{{< codenew file="pods/resource/memory-request-limit-2.yaml" >}}

In the `args` section of the configuration file, you can see that the Container
will attempt to allocate 250 MiB of memory, which is well above the 100 MiB limit.

Create the Pod:

```shell
kubectl apply -f https://k8s.io/examples/pods/resource/memory-request-limit-2.yaml --namespace=mem-example
```

View detailed information about the Pod:

```shell
kubectl get pod memory-demo-2 --namespace=mem-example
```

At this point, the Container might be running or killed. Repeat the preceding command until the Container is killed:

```shell
NAME            READY     STATUS      RESTARTS   AGE
memory-demo-2   0/1       OOMKilled   1          24s
```

Get a more detailed view of the Container status:

```shell
kubectl get pod memory-demo-2 --output=yaml --namespace=mem-example
```

The output shows that the Container was killed because it is out of memory (OOM):

```shell
lastState:
   terminated:
     containerID: docker://65183c1877aaec2e8427bc95609cc52677a454b56fcb24340dbd22917c23b10f
     exitCode: 137
     finishedAt: 2017-06-20T20:52:19Z
     reason: OOMKilled
     startedAt: null
```

The Container in this exercise can be restarted, so the kubelet restarts it. Repeat
this command several times to see that the Container is repeatedly killed and restarted:

```shell
kubectl get pod memory-demo-2 --namespace=mem-example
```

The output shows that the Container is killed, restarted, killed again, restarted again, and so on:

```
kubectl get pod memory-demo-2 --namespace=mem-example
NAME            READY     STATUS      RESTARTS   AGE
memory-demo-2   0/1       OOMKilled   1          37s
```
```

kubectl get pod memory-demo-2 --namespace=mem-example
NAME            READY     STATUS    RESTARTS   AGE
memory-demo-2   1/1       Running   2          40s
```

View detailed information about the Pod history:

```
kubectl describe pod memory-demo-2 --namespace=mem-example
```

The output shows that the Container starts and fails repeatedly:

```
... Normal  Created   Created container with id 66a3a20aa7980e61be4922780bf9d24d1a1d8b7395c09861225b0eba1b1f8511
... Warning BackOff   Back-off restarting failed container
```

View detailed information about your cluster's Nodes:

```
kubectl describe nodes
```

The output includes a record of the Container being killed because of an out-of-memory condition:

```
Warning OOMKilling Memory cgroup out of memory: Kill process 4481 (stress) score 1994 or sacrifice child
```

Delete your Pod:

```shell
kubectl delete pod memory-demo-2 --namespace=mem-example
```

## Specify a memory request that is too big for your Nodes

Memory requests and limits are associated with Containers, but it is useful to think
of a Pod as having a memory request and limit. The memory request for the Pod is the
sum of the memory requests for all the Containers in the Pod. Likewise, the memory
limit for the Pod is the sum of the limits of all the Containers in the Pod.

Pod scheduling is based on requests. A Pod is scheduled to run on a Node only if the Node
has enough available memory to satisfy the Pod's memory request.

In this exercise, you create a Pod that has a memory request so big that it exceeds the
capacity of any Node in your cluster. Here is the configuration file for a Pod that has one
Container with a request for 1000 GiB of memory, which likely exceeds the capacity
of any Node in your cluster.

{{< codenew file="pods/resource/memory-request-limit-3.yaml" >}}

Create the Pod:

```shell
kubectl apply -f https://k8s.io/examples/pods/resource/memory-request-limit-3.yaml --namespace=mem-example
```

View the Pod status:

```shell
kubectl get pod memory-demo-3 --namespace=mem-example
```

The output shows that the Pod status is PENDING. That is, the Pod is not scheduled to run on any Node, and it will remain in the PENDING state indefinitely:

```
kubectl get pod memory-demo-3 --namespace=mem-example
NAME            READY     STATUS    RESTARTS   AGE
memory-demo-3   0/1       Pending   0          25s
```

View detailed information about the Pod, including events:

```shell
kubectl describe pod memory-demo-3 --namespace=mem-example
```

The output shows that the Container cannot be scheduled because of insufficient memory on the Nodes:

```shell
Events:
  ...  Reason            Message
       ------            -------
  ...  FailedScheduling  No nodes are available that match all of the following predicates:: Insufficient memory (3).
```

## Memory units

The memory resource is measured in bytes. You can express memory as a plain integer or a
fixed-point integer with one of these suffixes: E, P, T, G, M, K, Ei, Pi, Ti, Gi, Mi, Ki.
For example, the following represent approximately the same value:

```shell
128974848, 129e6, 129M , 123Mi
```

Delete your Pod:

```shell
kubectl delete pod memory-demo-3 --namespace=mem-example
```

## If you do not specify a memory limit

If you do not specify a memory limit for a Container, one of the following situations applies:

* The Container has no upper bound on the amount of memory it uses. The Container
could use all of the memory available on the Node where it is running which in turn could invoke the OOM Killer. Further, in case of an OOM Kill, a container with no resource limits will have a greater chance of being killed.

* The Container is running in a namespace that has a default memory limit, and the
Container is automatically assigned the default limit. Cluster administrators can use a
[LimitRange](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#limitrange-v1-core)
to specify a default value for the memory limit.

## Motivation for memory requests and limits

By configuring memory requests and limits for the Containers that run in your
cluster, you can make efficient use of the memory resources available on your cluster's
Nodes. By keeping a Pod's memory request low, you give the Pod a good chance of being
scheduled. By having a memory limit that is greater than the memory request, you accomplish two things:

* The Pod can have bursts of activity where it makes use of memory that happens to be available.
* The amount of memory a Pod can use during a burst is limited to some reasonable amount.

## Clean up

Delete your namespace. This deletes all the Pods that you created for this task:

```shell
kubectl delete namespace mem-example
```



## {{% heading "whatsnext" %}}


### For app developers

* [Assign CPU Resources to Containers and Pods](/docs/tasks/configure-pod-container/assign-cpu-resource/)

* [Configure Quality of Service for Pods](/docs/tasks/configure-pod-container/quality-service-pod/)

### For cluster administrators

* [Configure Default Memory Requests and Limits for a Namespace](/docs/tasks/administer-cluster/manage-resources/memory-default-namespace/)

* [Configure Default CPU Requests and Limits for a Namespace](/docs/tasks/administer-cluster/manage-resources/cpu-default-namespace/)

* [Configure Minimum and Maximum Memory Constraints for a Namespace](/docs/tasks/administer-cluster/manage-resources/memory-constraint-namespace/)

* [Configure Minimum and Maximum CPU Constraints for a Namespace](/docs/tasks/administer-cluster/manage-resources/cpu-constraint-namespace/)

* [Configure Memory and CPU Quotas for a Namespace](/docs/tasks/administer-cluster/manage-resources/quota-memory-cpu-namespace/)

* [Configure a Pod Quota for a Namespace](/docs/tasks/administer-cluster/manage-resources/quota-pod-namespace/)

* [Configure Quotas for API Objects](/docs/tasks/administer-cluster/quota-api-object/)





