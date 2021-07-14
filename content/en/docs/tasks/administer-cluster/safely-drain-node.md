---
reviewers:
- davidopp
- mml
- foxish
- kow3ns
title: Safely Drain a Node
content_type: task
min-kubernetes-server-version: 1.5
---

<!-- overview -->
This page shows how to safely drain a {{< glossary_tooltip text="node" term_id="node" >}},
optionally respecting the PodDisruptionBudget you have defined.

## {{% heading "prerequisites" %}}

{{% version-check %}}
This task also assumes that you have met the following prerequisites:
  1. You do not require your applications to be highly available during the
     node drain, or
  1. You have read about the [PodDisruptionBudget](/docs/concepts/workloads/pods/disruptions/) concept,
     and have [configured PodDisruptionBudgets](/docs/tasks/run-application/configure-pdb/) for
     applications that need them.



<!-- steps -->

## (Optional) Configure a disruption budget {#configure-poddisruptionbudget}

To endure that your workloads remain available during maintenance, you can
configure a [PodDisruptionBudget](/docs/concepts/workloads/pods/disruptions/).

If availability is important for any applications that run or could run on the node(s)
that you are draining, [configure a PodDisruptionBudgets](/docs/tasks/run-application/configure-pdb/)
first and the continue following this guide.

## Use `kubectl drain` to remove a node from service

You can use `kubectl drain` to safely evict all of your pods from a
node before you perform maintenance on the node (e.g. kernel upgrade,
hardware maintenance, etc.). Safe evictions allow the pod's containers
to [gracefully terminate](/docs/concepts/workloads/pods/pod-lifecycle/#pod-termination)
and will respect the PodDisruptionBudgets you have specified.

{{< note >}}
By default `kubectl drain` ignores certain system pods on the node
that cannot be killed; see
the [kubectl drain](/docs/reference/generated/kubectl/kubectl-commands/#drain)
documentation for more details.
{{< /note >}}

When `kubectl drain` returns successfully, that indicates that all of
the pods (except the ones excluded as described in the previous paragraph)
have been safely evicted (respecting the desired graceful termination period,
and respecting the PodDisruptionBudget you have defined). It is then safe to
bring down the node by powering down its physical machine or, if running on a
cloud platform, deleting its virtual machine.

First, identify the name of the node you wish to drain. You can list all of the nodes in your cluster with

```shell
kubectl get nodes
```

Next, tell Kubernetes to drain the node:

```shell
kubectl drain <node name>
```

Once it returns (without giving an error), you can power down the node
(or equivalently, if on a cloud platform, delete the virtual machine backing the node).
If you leave the node in the cluster during the maintenance operation, you need to run

```shell
kubectl uncordon <node name>
```
afterwards to tell Kubernetes that it can resume scheduling new pods onto the node.

## Draining multiple nodes in parallel

The `kubectl drain` command should only be issued to a single node at a
time. However, you can run multiple `kubectl drain` commands for
different nodes in parallel, in different terminals or in the
background. Multiple drain commands running concurrently will still
respect the PodDisruptionBudget you specify.

For example, if you have a StatefulSet with three replicas and have
set a PodDisruptionBudget for that set specifying `minAvailable: 2`,
`kubectl drain` only evicts a pod from the StatefulSet if all three
replicas pods are ready; if then you issue multiple drain commands in
parallel, Kubernetes respects the PodDisruptionBudget and ensure
that only 1 (calculated as `replicas - minAvailable`) Pod is unavailable
at any given time. Any drains that would cause the number of ready
replicas to fall below the specified budget are blocked.

## The Eviction API {#eviction-api}

If you prefer not to use [kubectl drain](/docs/reference/generated/kubectl/kubectl-commands/#drain) (such as
to avoid calling to an external command, or to get finer control over the pod
eviction process), you can also programmatically cause evictions using the eviction API.

You should first be familiar with using [Kubernetes language clients](/docs/tasks/administer-cluster/access-cluster-api/#programmatic-access-to-the-api) to access the API.

The eviction subresource of a
Pod can be thought of as a kind of policy-controlled DELETE operation on the Pod
itself. To attempt an eviction (more precisely: to attempt to
*create* an Eviction), you POST an attempted operation. Here's an example:

{{< tabs name="Eviction_example" >}}
{{% tab name="policy/v1" %}}
{{< note >}}
`policy/v1` Eviction is available in v1.22+. Use `policy/v1beta1` with prior releases.
{{< /note >}}

```json
{
  "apiVersion": "policy/v1",
  "kind": "Eviction",
  "metadata": {
    "name": "quux",
    "namespace": "default"
  }
}
```
{{% /tab %}}
{{% tab name="policy/v1beta1" %}}
{{< note >}}
Deprecated in v1.22 in favor of `policy/v1`
{{< /note >}}

```json
{
  "apiVersion": "policy/v1beta1",
  "kind": "Eviction",
  "metadata": {
    "name": "quux",
    "namespace": "default"
  }
}
```
{{% /tab %}}
{{< /tabs >}}

You can attempt an eviction using `curl`:

```bash
curl -v -H 'Content-type: application/json' https://your-cluster-api-endpoint.example/api/v1/namespaces/default/pods/quux/eviction -d @eviction.json
```

The API can respond in one of three ways:

- If the eviction is granted, then the Pod is deleted as if you sent
  a `DELETE` request to the Pod's URL and received back `200 OK`.
- If the current state of affairs wouldn't allow an eviction by the rules set
  forth in the budget, you get back `429 Too Many Requests`. This is
  typically used for generic rate limiting of *any* requests, but here we mean
  that this request isn't allowed *right now* but it may be allowed later.
- If there is some kind of misconfiguration; for example multiple PodDisruptionBudgets
  that refer the same Pod, you get a `500 Internal Server Error` response.

For a given eviction request, there are two cases:

- There is no budget that matches this pod. In this case, the server always
  returns `200 OK`.
- There is at least one budget. In this case, any of the three above responses may
 apply.

## Stuck evictions

In some cases, an application may reach a broken state, one where unless you intervene the
eviction API will never return anything other than 429 or 500.

For example: this can happen if ReplicaSet is creating Pods for your application but
the replacement Pods do not become `Ready`. You can also see similar symptoms if the
last Pod evicted has a very long termination grace period.

In this case, there are two potential solutions:

- Abort or pause the automated operation. Investigate the reason for the stuck application,
  and restart the automation.
- After a suitably long wait, `DELETE` the Pod from your cluster's control plane, instead
  of using the eviction API.

Kubernetes does not specify what the behavior should be in this case; it is up to the
application owners and cluster owners to establish an agreement on behavior in these cases.

## {{% heading "whatsnext" %}}


* Follow steps to protect your application by [configuring a Pod Disruption Budget](/docs/tasks/run-application/configure-pdb/).

