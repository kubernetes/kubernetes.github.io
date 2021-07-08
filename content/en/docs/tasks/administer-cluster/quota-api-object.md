---
title: Configure Quotas for API Objects
content_type: task
---


<!-- overview -->

This page shows how to configure quotas for API objects, including
PersistentVolumeClaims and Services. A quota restricts the number of
objects, of a particular type, that can be created in a namespace.
You specify quotas in a
{{< api-reference page="policy-resources/resource-quota-v1" >}}
object.




## {{% heading "prerequisites" %}}


{{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}




<!-- steps -->

## Create a namespace

Create a namespace so that the resources you create in this exercise are
isolated from the rest of your cluster.

```shell
kubectl create namespace quota-object-example
```

## Create a ResourceQuota

Here is the configuration file for a ResourceQuota object:

{{< codenew file="admin/resource/quota-objects.yaml" >}}

Create the ResourceQuota:

```shell
kubectl apply -f https://k8s.io/examples/admin/resource/quota-objects.yaml --namespace=quota-object-example
```

View detailed information about the ResourceQuota:

```shell
kubectl get resourcequota object-quota-demo --namespace=quota-object-example --output=yaml
```

The output shows that in the quota-object-example namespace, there can be at most
one PersistentVolumeClaim, at most two Services of type LoadBalancer, and no Services
of type NodePort.

```yaml
status:
  hard:
    persistentvolumeclaims: "1"
    services.loadbalancers: "2"
    services.nodeports: "0"
  used:
    persistentvolumeclaims: "0"
    services.loadbalancers: "0"
    services.nodeports: "0"
```

## Create a PersistentVolumeClaim

Here is the configuration file for a PersistentVolumeClaim object:

{{< codenew file="admin/resource/quota-objects-pvc.yaml" >}}

Create the PersistentVolumeClaim:

```shell
kubectl apply -f https://k8s.io/examples/admin/resource/quota-objects-pvc.yaml --namespace=quota-object-example
```

Verify that the PersistentVolumeClaim was created:

```shell
kubectl get persistentvolumeclaims --namespace=quota-object-example
```

The output shows that the PersistentVolumeClaim exists and has status Pending:

```shell
NAME             STATUS
pvc-quota-demo   Pending
```

## Attempt to create a second PersistentVolumeClaim

Here is the configuration file for a second PersistentVolumeClaim:

{{< codenew file="admin/resource/quota-objects-pvc-2.yaml" >}}

Attempt to create the second PersistentVolumeClaim:

```shell
kubectl apply -f https://k8s.io/examples/admin/resource/quota-objects-pvc-2.yaml --namespace=quota-object-example
```

The output shows that the second PersistentVolumeClaim was not created,
because it would have exceeded the quota for the namespace.

```
persistentvolumeclaims "pvc-quota-demo-2" is forbidden:
exceeded quota: object-quota-demo, requested: persistentvolumeclaims=1,
used: persistentvolumeclaims=1, limited: persistentvolumeclaims=1
```

## Notes

These are the strings used to identify API resources that can be constrained
by quotas:

<table>
<tr><th>String</th><th>API Object</th></tr>
<tr><td>"pods"</td><td>Pod</td></tr>
<tr><td>"services"</td><td>Service</td></tr>
<tr><td>"replicationcontrollers"</td><td>ReplicationController</td></tr>
<tr><td>"resourcequotas"</td><td>ResourceQuota</td></tr>
<tr><td>"secrets"</td><td>Secret</td></tr>
<tr><td>"configmaps"</td><td>ConfigMap</td></tr>
<tr><td>"persistentvolumeclaims"</td><td>PersistentVolumeClaim</td></tr>
<tr><td>"services.nodeports"</td><td>Service of type NodePort</td></tr>
<tr><td>"services.loadbalancers"</td><td>Service of type LoadBalancer</td></tr>
</table>

## Clean up

Delete your namespace:

```shell
kubectl delete namespace quota-object-example
```



## {{% heading "whatsnext" %}}


### For cluster administrators

* [Configure Default Memory Requests and Limits for a Namespace](/docs/tasks/administer-cluster/manage-resources/memory-default-namespace/)

* [Configure Default CPU Requests and Limits for a Namespace](/docs/tasks/administer-cluster/manage-resources/cpu-default-namespace/)

* [Configure Minimum and Maximum Memory Constraints for a Namespace](/docs/tasks/administer-cluster/manage-resources/memory-constraint-namespace/)

* [Configure Minimum and Maximum CPU Constraints for a Namespace](/docs/tasks/administer-cluster/manage-resources/cpu-constraint-namespace/)

* [Configure Memory and CPU Quotas for a Namespace](/docs/tasks/administer-cluster/manage-resources/quota-memory-cpu-namespace/)

* [Configure a Pod Quota for a Namespace](/docs/tasks/administer-cluster/manage-resources/quota-pod-namespace/)

### For app developers

* [Assign Memory Resources to Containers and Pods](/docs/tasks/configure-pod-container/assign-memory-resource/)

* [Assign CPU Resources to Containers and Pods](/docs/tasks/configure-pod-container/assign-cpu-resource/)

* [Configure Quality of Service for Pods](/docs/tasks/configure-pod-container/quality-service-pod/)








