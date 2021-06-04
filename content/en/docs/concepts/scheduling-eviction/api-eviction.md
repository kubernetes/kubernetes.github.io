---
title: API-initiated Eviction
content_type: concept
weight: 70
---

{{< glossary_definition term_id="api-eviction" length="short" >}} </br>

You can request eviction by calling the Eviction API directly, or programmatically
using a client of the kube-apiserver, like the `kubectl drain` command. This
creates an `Eviction` object, which causes the API server to terminate the Pod.

API-initiated evictions respect your configured [`PodDisruptionBudgets`](/docs/tasks/run-application/configure-pdb/)
and [`terminationGracePeriodSeconds`](/docs/concepts/workloads/pods/pod-lifecycle#pod-termination). 

Using the API to create an Eviction object for a Pod is like performing a
policy-controlled DELETE operation on the Pod. 

## Calling the Eviction API

You can use a [Kubernetes language client](/docs/tasks/administer-cluster/access-cluster-api/#programmatic-access-to-the-api)
to access the Kubernetes API and create an `Eviction` object. To do this, you
POST the attempted operation.

Alternatively, you can attempt an eviction operation by accessing the API using
`curl` or `wget`. 

## How API-initiated eviction works

When you attempt to create an `Eviction` object, the API responds in one of the
following ways:

* `200 OK`: the eviction is allowed and the Pod is deleted, similar to sending a
  `DELETE` request to the Pod URL.
* `429 Too Many Requests`: the eviction is not currently allowed because of the
  configured PodDisruptionBudget. You may be able to attempt the eviction again
  later.
* `500 Internal Server Error`: the eviction is not allowed because there is a
  misconfiguration, like if multiple PodDisruptionBudgets reference the same Pod.

If the Pod you want to evict doesn't have a PodDisruptionBudget, the server always
returns `200 OK` and allows the eviction.

[[Need more information about the eviction object. Once it's created, what happens
to cause the Pod to shut down? What control plane components work to get the job done?]]

## Troubleshooting stuck evictions

In some cases, your applications may enter a broken state, where the Eviction
API will only return `429` or `500` responses until you intervene. This can 
happen if, for example, a ReplicaSet creates pods for your application but new 
pods do not enter a `Ready` state. You may also notice this behavior in cases
where the last evicted Pod had a long termination grace period.

If you notice stuck evictions, try one of the following solutions: 

* Abort or pause the automated operation causing the issue. Investigate the stuck
  application before you restart the operation.
* Directly delete the Pod from your cluster control plane instead of using the
  Eviction API.

## {{% heading "whatsnext" %}}

* Learn how to protect your applications with a [Pod Disruption Budget](/docs/tasks/run-application/configure-pdb/).
* Learn about [Node-pressure Eviction](/docs/concepts/scheduling-eviction/node-pressure-eviction/).
* Learn about [Pod Priority and Preemption](/docs/concepts/scheduling-eviction/pod-priority-preemption/).
