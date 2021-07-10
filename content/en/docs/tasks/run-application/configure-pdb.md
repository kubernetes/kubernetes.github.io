---
title: Specifying a Disruption Budget for your Application
content_type: task
weight: 110
min-kubernetes-server-version: v1.21
---

<!-- overview -->

{{< feature-state for_k8s_version="v1.21" state="stable" >}}

This page shows how to limit the number of concurrent disruptions
that your application experiences, allowing for higher availability
while permitting the cluster administrator to manage the clusters
nodes.



## {{% heading "prerequisites" %}}

{{< version-check >}}

* You are the owner of an application running on a Kubernetes cluster that requires
  high availability.
* You should know how to deploy [Replicated Stateless Applications](/docs/tasks/run-application/run-stateless-application-deployment/)
  and/or [Replicated Stateful Applications](/docs/tasks/run-application/run-replicated-stateful-application/).
* You should have read about [Pod Disruptions](/docs/concepts/workloads/pods/disruptions/).
* You should confirm with your cluster owner or service provider that they respect
  Pod Disruption Budgets.


<!-- steps -->

## Protecting an Application with a PodDisruptionBudget

1. Identify what application you want to protect with a PodDisruptionBudget (PDB).
1. Think about how your application reacts to disruptions.
1. Create a PDB definition as a YAML file.
1. Create the PDB object from the YAML file.



<!-- discussion -->

## Identify an Application to Protect

The most common use case when you want to protect an application
specified by one of the built-in Kubernetes controllers:

- Deployment
- ReplicationController
- ReplicaSet
- StatefulSet

In this case, make a note of the controller's `.spec.selector`; the same
selector goes into the PDBs `.spec.selector`.

From version 1.15 PDBs support custom controllers where the [scale subresource](/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/#scale-subresource) is enabled.

You can also use PDBs with pods which are not controlled by one of the above
controllers, or arbitrary groups of pods, but there are some restrictions,
described in [Arbitrary Controllers and Selectors](#arbitrary-controllers-and-selectors).


## Think about how your application reacts to disruptions

Decide how many instances can be down at the same time for a short period
due to a voluntary disruption.

- Stateless frontends:
  - Concern: don't reduce serving capacity by more than 10%. 
    - Solution: use PDB with minAvailable 90% for example.
- Single-instance Stateful Application:
  - Concern: do not terminate this application without talking to me.
    - Possible Solution 1: Do not use a PDB and tolerate occasional downtime.
    - Possible Solution 2: Set PDB with maxUnavailable=0.  Have an understanding
      (outside of Kubernetes) that the cluster operator needs to consult you before
      termination.  When the cluster operator contacts you, prepare for downtime,
      and then delete the PDB to indicate readiness for disruption.  Recreate afterwards.
- Multiple-instance Stateful application such as Consul, ZooKeeper, or etcd:
  - Concern: Do not reduce number of instances below quorum, otherwise writes fail.
    - Possible Solution 1: set maxUnavailable to 1 (works with varying scale of application).
    - Possible Solution 2: set minAvailable to quorum-size (e.g. 3 when scale is 5).  (Allows more disruptions at once).
- Restartable Batch Job:
  - Concern: Job needs to complete in case of voluntary disruption.
    - Possible solution: Do not create a PDB.  The Job controller will create a replacement pod.

### Rounding logic when specifying percentages

Values for `minAvailable` or `maxUnavailable` can be expressed as integers or as a percentage.

- When you specify an integer, it represents a number of Pods. For instance, if you set `minAvailable` to 10, then 10
  Pods must always be available, even during a disruption.
- When you specify a percentage by setting the value to a string representation of a percentage (eg. `"50%"`), it represents a percentage of
  total Pods. For instance, if you set `maxUnavailable` to `"50%"`, then only 50% of the Pods can be unavailable during a
  disruption.

When you specify the value as a percentage, it may not map to an exact number of Pods. For example, if you have 7 Pods and
you set `minAvailable` to `"50%"`, it's not immediately obvious whether that means 3 Pods or 4 Pods must be available.
Kubernetes rounds up to the nearest integer, so in this case, 4 Pods must be available. You can examine the
[code](https://github.com/kubernetes/kubernetes/blob/23be9587a0f8677eb8091464098881df939c44a9/pkg/controller/disruption/disruption.go#L539)
that controls this behavior.

## Specifying a PodDisruptionBudget

A `PodDisruptionBudget` has three fields: 

* A label selector `.spec.selector` to specify the set of
pods to which it applies. This field is required.
* `.spec.minAvailable` which is a description of the number of pods from that
set that must still be available after the eviction, even in the absence
of the evicted pod. `minAvailable` can be either an absolute number or a percentage.
* `.spec.maxUnavailable` (available in Kubernetes 1.7 and higher) which is a description 
of the number of pods from that set that can be unavailable after the eviction. 
It can be either an absolute number or a percentage.

{{< note >}}
The behavior for an empty selector differs between the policy/v1beta1 and policy/v1 APIs for
PodDisruptionBudgets. For policy/v1beta1 an empty selector matches zero pods, while
for policy/v1 an empty selector matches every pod in the namespace.
{{< /note >}}

You can specify only one of `maxUnavailable` and `minAvailable` in a single `PodDisruptionBudget`. 
`maxUnavailable` can only be used to control the eviction of pods 
that have an associated controller managing them. In the examples below, "desired replicas"
is the `scale` of the controller managing the pods being selected by the
`PodDisruptionBudget`.

Example 1: With a `minAvailable` of 5, evictions are allowed as long as they leave behind
5 or more healthy pods among those selected by the PodDisruptionBudget's `selector`.

Example 2: With a `minAvailable` of 30%, evictions are allowed as long as at least 30%
of the number of desired replicas are healthy. 

Example 3: With a `maxUnavailable` of 5, evictions are allowed as long as there are at most 5
unhealthy replicas among the total number of desired replicas.

Example 4: With a `maxUnavailable` of 30%, evictions are allowed as long as no more than 30% 
of the desired replicas are unhealthy.

In typical usage, a single budget would be used for a collection of pods managed by
a controller—for example, the pods in a single ReplicaSet or StatefulSet. 

{{< note >}}
A disruption budget does not truly guarantee that the specified
number/percentage of pods will always be up.  For example, a node that hosts a
pod from the collection may fail when the collection is at the minimum size
specified in the budget, thus bringing the number of available pods from the
collection below the specified size. The budget can only protect against
voluntary evictions, not all causes of unavailability.
{{< /note >}}

If you set `maxUnavailable` to 0% or 0, or you set `minAvailable` to 100% or the number of replicas,
you are requiring zero voluntary evictions. When you set zero voluntary evictions for a workload
object such as ReplicaSet, then you cannot successfully drain a Node running one of those Pods.
If you try to drain a Node where an unevictable Pod is running, the drain never completes. This is permitted as per the
semantics of `PodDisruptionBudget`.

You can find examples of pod disruption budgets defined below. They match pods with the label 
`app: zookeeper`.

Example PDB Using minAvailable:

{{< codenew file="policy/zookeeper-pod-disruption-budget-minavailable.yaml" >}}

Example PDB Using maxUnavailable:

{{< codenew file="policy/zookeeper-pod-disruption-budget-maxunavailable.yaml" >}}

For example, if the above `zk-pdb` object selects the pods of a StatefulSet of size 3, both
specifications have the exact same meaning. The use of `maxUnavailable` is recommended as it
automatically responds to changes in the number of replicas of the corresponding controller.

## Create the PDB object

You can create or update the PDB object with a command like `kubectl apply -f mypdb.yaml`.

## Check the status of the PDB

Use kubectl to check that your PDB is created.

Assuming you don't actually have pods matching `app: zookeeper` in your namespace,
then you'll see something like this:

```shell
kubectl get poddisruptionbudgets
```
```
NAME     MIN AVAILABLE   MAX UNAVAILABLE   ALLOWED DISRUPTIONS   AGE
zk-pdb   2               N/A               0                     7s
```

If there are matching pods (say, 3), then you would see something like this:

```shell
kubectl get poddisruptionbudgets
```
```
NAME     MIN AVAILABLE   MAX UNAVAILABLE   ALLOWED DISRUPTIONS   AGE
zk-pdb   2               N/A               1                     7s
```

The non-zero value for `ALLOWED DISRUPTIONS` means that the disruption controller has seen the pods,
counted the matching pods, and updated the status of the PDB.

You can get more information about the status of a PDB with this command:

```shell
kubectl get poddisruptionbudgets zk-pdb -o yaml
```
```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  annotations:
…
  creationTimestamp: "2020-03-04T04:22:56Z"
  generation: 1
  name: zk-pdb
…
status:
  currentHealthy: 3
  desiredHealthy: 2
  disruptionsAllowed: 1
  expectedPods: 3
  observedGeneration: 1
```

## Arbitrary Controllers and Selectors

You can skip this section if you only use PDBs with the built-in
application controllers (Deployment, ReplicationController, ReplicaSet, and StatefulSet),
with the PDB selector matching the controller's selector.

You can use a PDB with pods controlled by another type of controller, by an
"operator", or bare pods, but with these restrictions:

- only `.spec.minAvailable` can be used, not `.spec.maxUnavailable`.
- only an integer value can be used with `.spec.minAvailable`, not a percentage.

You can use a selector which selects a subset or superset of the pods belonging to a built-in
controller.  The eviction API will disallow eviction of any pod covered by multiple PDBs,
so most users will want to avoid overlapping selectors.  One reasonable use of overlapping
PDBs is when pods are being transitioned from one PDB to another.

## {{% heading "whatsnext" %}}
- PodDisruptionBudget is a top-level resource in the Kubernetes REST API.
  The {{< api-reference page="policy-resources/pod-disruption-budget-v1" >}} object definition describes the object in detail.
