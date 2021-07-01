---
reviewers:
- erictune
- foxish
- davidopp
title: Disruptions
content_type: concept
weight: 60
---

<!-- overview -->
This guide is for application owners who want to build
highly available applications, and thus need to understand
what types of disruptions can happen to Pods.

It is also for cluster administrators who want to perform automated
cluster actions, like upgrading and autoscaling clusters.

<!-- body -->

## Voluntary and involuntary disruptions

Pods do not disappear until someone (a person or a controller) destroys them, or
there is an unavoidable hardware or system software error.

We call these unavoidable cases *involuntary disruptions* to
an application.  Examples are:

- a hardware failure of the physical machine backing the node
- cluster administrator deletes VM (instance) by mistake
- cloud provider or hypervisor failure makes VM disappear
- a kernel panic
- the node disappears from the cluster due to cluster network partition
- eviction of a pod due to the node being [out-of-resources](/docs/tasks/administer-cluster/out-of-resource/).

Except for the out-of-resources condition, all these conditions
should be familiar to most users; they are not specific
to Kubernetes.

We call other cases *voluntary disruptions*.  These include both
actions initiated by the application owner and those initiated by a Cluster
Administrator.  Typical application owner actions include:

- deleting the deployment or other controller that manages the pod
- updating a deployment's pod template causing a restart
- directly deleting a pod (e.g. by accident)

Cluster administrator actions include:

- [Draining a node](/docs/tasks/administer-cluster/safely-drain-node/) for repair or upgrade.
- Draining a node from a cluster to scale the cluster down (learn about
[Cluster Autoscaling](https://github.com/kubernetes/autoscaler/#readme)
).
- Removing a pod from a node to permit something else to fit on that node.

These actions might be taken directly by the cluster administrator, or by automation
run by the cluster administrator, or by your cluster hosting provider.

Ask your cluster administrator or consult your cloud provider or distribution documentation
to determine if any sources of voluntary disruptions are enabled for your cluster.
If none are enabled, you can skip creating Pod Disruption Budgets.

{{< caution >}}
Not all voluntary disruptions are constrained by Pod Disruption Budgets. For example,
deleting deployments or pods bypasses Pod Disruption Budgets.
{{< /caution >}}

## Dealing with disruptions

Here are some ways to mitigate involuntary disruptions:

- Ensure your pod [requests the resources](/docs/tasks/configure-pod-container/assign-memory-resource) it needs.
- Replicate your application if you need higher availability.  (Learn about running replicated
  [stateless](/docs/tasks/run-application/run-stateless-application-deployment/)
  and [stateful](/docs/tasks/run-application/run-replicated-stateful-application/) applications.)
- For even higher availability when running replicated applications,
  spread applications across racks (using
  [anti-affinity](/docs/concepts/scheduling-eviction/assign-pod-node/#affinity-and-anti-affinity))
  or across zones (if using a
  [multi-zone cluster](/docs/setup/multiple-zones).)

The frequency of voluntary disruptions varies.  On a basic Kubernetes cluster, there are
no automated voluntary disruptions (only user-triggered ones).  However, your cluster administrator or hosting provider
may run some additional services which cause voluntary disruptions. For example,
rolling out node software updates can cause voluntary disruptions. Also, some implementations
of cluster (node) autoscaling may cause voluntary disruptions to defragment and compact nodes.
Your cluster administrator or hosting provider should have documented what level of voluntary
disruptions, if any, to expect. Certain configuration options, such as
[using PriorityClasses](/docs/concepts/scheduling-eviction/pod-priority-preemption/)
in your pod spec can also cause voluntary (and involuntary) disruptions.


## Pod disruption budgets

{{< feature-state for_k8s_version="v1.21" state="stable" >}}

Kubernetes offers features to help you run highly available applications even when you
introduce frequent voluntary disruptions.

As an application owner, you can create a PodDisruptionBudget (PDB) for each application.
A PDB limits the number of Pods of a replicated application that are down simultaneously from
voluntary disruptions. For example, a quorum-based application would
like to ensure that the number of replicas running is never brought below the
number needed for a quorum. A web front end might want to
ensure that the number of replicas serving load never falls below a certain
percentage of the total.

Cluster managers and hosting providers should use tools which
respect PodDisruptionBudgets by calling the [Eviction API](/docs/tasks/administer-cluster/safely-drain-node/#eviction-api)
instead of directly deleting pods or deployments.

For example, the `kubectl drain` subcommand lets you mark a node as going out of
service. When you run `kubectl drain`, the tool tries to evict all of the Pods on
the Node you're taking out of service. The eviction request that `kubectl` submits on
your behalf may be temporarily rejected, so the tool periodically retries all failed
requests until all Pods on the target node are terminated, or until a configurable timeout
is reached.

A PDB specifies the number of replicas that an application can tolerate having, relative to how
many it is intended to have.  For example, a Deployment which has a `.spec.replicas: 5` is
supposed to have 5 pods at any given time.  If its PDB allows for there to be 4 at a time,
then the Eviction API will allow voluntary disruption of one (but not two) pods at a time.

The group of pods that comprise the application is specified using a label selector, the same
as the one used by the application's controller (deployment, stateful-set, etc).

The "intended" number of pods is computed from the `.spec.replicas` of the workload resource
that is managing those pods. The control plane discovers the owning workload resource by
examining the `.metadata.ownerReferences` of the Pod.

PDBs cannot prevent [involuntary disruptions](#voluntary-and-involuntary-disruptions) from
occurring, but they do count against the budget.

Pods which are deleted or unavailable due to a rolling upgrade to an application do count
against the disruption budget, but workload resources (such as Deployment and StatefulSet)
are not limited by PDBs when doing rolling upgrades. Instead, the handling of failures
during application updates is configured in the spec for the specific workload resource.

When a pod is evicted using the eviction API, it is gracefully
[terminated](/docs/concepts/workloads/pods/pod-lifecycle/#pod-termination), honoring the
`terminationGracePeriodSeconds` setting in its [PodSpec](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#podspec-v1-core).

## PodDisruptionBudget example {#pdb-example}

Consider a cluster with 3 nodes, `node-1` through `node-3`.
The cluster is running several applications.  One of them has 3 replicas initially called
`pod-a`, `pod-b`, and `pod-c`.  Another, unrelated pod without a PDB, called `pod-x`, is also shown.
Initially, the pods are laid out as follows:

|       node-1         |       node-2        |       node-3       |
|:--------------------:|:-------------------:|:------------------:|
| pod-a  *available*   | pod-b *available*   | pod-c *available*  |
| pod-x  *available*   |                     |                    |

All 3 pods are part of a deployment, and they collectively have a PDB which requires
there be at least 2 of the 3 pods to be available at all times.

For example, assume the cluster administrator wants to reboot into a new kernel version to fix a bug in the kernel.
The cluster administrator first tries to drain `node-1` using the `kubectl drain` command.
That tool tries to evict `pod-a` and `pod-x`.  This succeeds immediately.
Both pods go into the `terminating` state at the same time.
This puts the cluster in this state:

|   node-1 *draining*  |       node-2        |       node-3       |
|:--------------------:|:-------------------:|:------------------:|
| pod-a  *terminating* | pod-b *available*   | pod-c *available*  |
| pod-x  *terminating* |                     |                    |

The deployment notices that one of the pods is terminating, so it creates a replacement
called `pod-d`.  Since `node-1` is cordoned, it lands on another node.  Something has
also created `pod-y` as a replacement for `pod-x`.

(Note: for a StatefulSet, `pod-a`, which would be called something like `pod-0`, would need
to terminate completely before its replacement, which is also called `pod-0` but has a
different UID, could be created.  Otherwise, the example applies to a StatefulSet as well.)

Now the cluster is in this state:

|   node-1 *draining*  |       node-2        |       node-3       |
|:--------------------:|:-------------------:|:------------------:|
| pod-a  *terminating* | pod-b *available*   | pod-c *available*  |
| pod-x  *terminating* | pod-d *starting*    | pod-y              |

At some point, the pods terminate, and the cluster looks like this:

|    node-1 *drained*  |       node-2        |       node-3       |
|:--------------------:|:-------------------:|:------------------:|
|                      | pod-b *available*   | pod-c *available*  |
|                      | pod-d *starting*    | pod-y              |

At this point, if an impatient cluster administrator tries to drain `node-2` or
`node-3`, the drain command will block, because there are only 2 available
pods for the deployment, and its PDB requires at least 2.  After some time passes, `pod-d` becomes available.

The cluster state now looks like this:

|    node-1 *drained*  |       node-2        |       node-3       |
|:--------------------:|:-------------------:|:------------------:|
|                      | pod-b *available*   | pod-c *available*  |
|                      | pod-d *available*   | pod-y              |

Now, the cluster administrator tries to drain `node-2`.
The drain command will try to evict the two pods in some order, say
`pod-b` first and then `pod-d`.  It will succeed at evicting `pod-b`.
But, when it tries to evict `pod-d`, it will be refused because that would leave only
one pod available for the deployment.

The deployment creates a replacement for `pod-b` called `pod-e`.
Because there are not enough resources in the cluster to schedule
`pod-e` the drain will again block.  The cluster may end up in this
state:

|    node-1 *drained*  |       node-2        |       node-3       | *no node*          |
|:--------------------:|:-------------------:|:------------------:|:------------------:|
|                      | pod-b *terminating* | pod-c *available*  | pod-e *pending*    |
|                      | pod-d *available*   | pod-y              |                    |

At this point, the cluster administrator needs to
add a node back to the cluster to proceed with the upgrade.

You can see how Kubernetes varies the rate at which disruptions
can happen, according to:

- how many replicas an application needs
- how long it takes to gracefully shutdown an instance
- how long it takes a new instance to start up
- the type of controller
- the cluster's resource capacity

## Separating Cluster Owner and Application Owner Roles

Often, it is useful to think of the Cluster Manager
and Application Owner as separate roles with limited knowledge
of each other.   This separation of responsibilities
may make sense in these scenarios:

- when there are many application teams sharing a Kubernetes cluster, and
  there is natural specialization of roles
- when third-party tools or services are used to automate cluster management

Pod Disruption Budgets support this separation of roles by providing an
interface between the roles.

If you do not have such a separation of responsibilities in your organization,
you may not need to use Pod Disruption Budgets.

## How to perform Disruptive Actions on your Cluster

If you are a Cluster Administrator, and you need to perform a disruptive action on all
the nodes in your cluster, such as a node or system software upgrade, here are some options:

- Accept downtime during the upgrade.
- Failover to another complete replica cluster.
   -  No downtime, but may be costly both for the duplicated nodes
     and for human effort to orchestrate the switchover.
- Write disruption tolerant applications and use PDBs.
   - No downtime.
   - Minimal resource duplication.
   - Allows more automation of cluster administration.
   - Writing disruption-tolerant applications is tricky, but the work to tolerate voluntary
     disruptions largely overlaps with work to support autoscaling and tolerating
     involuntary disruptions.




## {{% heading "whatsnext" %}}


* Follow steps to protect your application by [configuring a Pod Disruption Budget](/docs/tasks/run-application/configure-pdb/).

* Learn more about [draining nodes](/docs/tasks/administer-cluster/safely-drain-node/)

* Learn about [updating a deployment](/docs/concepts/workloads/controllers/deployment/#updating-a-deployment)
  including steps to maintain its availability during the rollout.

