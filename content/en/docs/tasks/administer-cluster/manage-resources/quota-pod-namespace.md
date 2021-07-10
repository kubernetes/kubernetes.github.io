---
title: Configure a Pod Quota for a Namespace
content_type: task
weight: 60
---


<!-- overview -->

This page shows how to set a quota for the total number of Pods that can run
in a namespace. You specify quotas in a
{{< api-reference page="policy-resources/resource-quota-v1" >}}
object.




## {{% heading "prerequisites" %}}


{{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}




<!-- steps -->

## Create a namespace

Create a namespace so that the resources you create in this exercise are
isolated from the rest of your cluster.

```shell
kubectl create namespace quota-pod-example
```

## Create a ResourceQuota

Here is the configuration file for a ResourceQuota object:

{{< codenew file="admin/resource/quota-pod.yaml" >}}

Create the ResourceQuota:

```shell
kubectl apply -f https://k8s.io/examples/admin/resource/quota-pod.yaml --namespace=quota-pod-example
```

View detailed information about the ResourceQuota:

```shell
kubectl get resourcequota pod-demo --namespace=quota-pod-example --output=yaml
```

The output shows that the namespace has a quota of two Pods, and that currently there are
no Pods; that is, none of the quota is used.

```yaml
spec:
  hard:
    pods: "2"
status:
  hard:
    pods: "2"
  used:
    pods: "0"
```

Here is the configuration file for a Deployment:

{{< codenew file="admin/resource/quota-pod-deployment.yaml" >}}

In the configuration file, `replicas: 3` tells Kubernetes to attempt to create three Pods, all running the same application.

Create the Deployment:

```shell
kubectl apply -f https://k8s.io/examples/admin/resource/quota-pod-deployment.yaml --namespace=quota-pod-example
```

View detailed information about the Deployment:

```shell
kubectl get deployment pod-quota-demo --namespace=quota-pod-example --output=yaml
```

The output shows that even though the Deployment specifies three replicas, only two
Pods were created because of the quota.

```yaml
spec:
  ...
  replicas: 3
...
status:
  availableReplicas: 2
...
lastUpdateTime: 2017-07-07T20:57:05Z
    message: 'unable to create pods: pods "pod-quota-demo-1650323038-" is forbidden:
      exceeded quota: pod-demo, requested: pods=1, used: pods=2, limited: pods=2'
```

## Clean up

Delete your namespace:

```shell
kubectl delete namespace quota-pod-example
```



## {{% heading "whatsnext" %}}


### For cluster administrators

* [Configure Default Memory Requests and Limits for a Namespace](/docs/tasks/administer-cluster/manage-resources/memory-default-namespace/)

* [Configure Default CPU Requests and Limits for a Namespace](/docs/tasks/administer-cluster/manage-resources/cpu-default-namespace/)

* [Configure Minimum and Maximum Memory Constraints for a Namespace](/docs/tasks/administer-cluster/manage-resources/memory-constraint-namespace/)

* [Configure Minimum and Maximum CPU Constraints for a Namespace](/docs/tasks/administer-cluster/manage-resources/cpu-constraint-namespace/)

* [Configure Memory and CPU Quotas for a Namespace](/docs/tasks/administer-cluster/manage-resources/quota-memory-cpu-namespace/)

* [Configure Quotas for API Objects](/docs/tasks/administer-cluster/quota-api-object/)

### For app developers

* [Assign Memory Resources to Containers and Pods](/docs/tasks/configure-pod-container/assign-memory-resource/)

* [Assign CPU Resources to Containers and Pods](/docs/tasks/configure-pod-container/assign-cpu-resource/)

* [Configure Quality of Service for Pods](/docs/tasks/configure-pod-container/quality-service-pod/)







