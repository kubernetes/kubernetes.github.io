---
reviewers:
- jszczepkowski
title: Set up a High-Availability Control Plane
content_type: task
aliases: [ '/docs/tasks/administer-cluster/highly-available-master/' ]
---

<!-- overview -->

{{< feature-state for_k8s_version="v1.5" state="alpha" >}}

You can replicate Kubernetes control plane nodes in `kube-up` or `kube-down` scripts for Google Compute Engine. However this scripts are not suitable for any sort of production use, it's widely used in the project's CI.
This document describes how to use kube-up/down scripts to manage a highly available (HA) control plane and how HA control planes are implemented for use with GCE.




## {{% heading "prerequisites" %}}


{{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}



<!-- steps -->

## Starting an HA-compatible cluster

To create a new HA-compatible cluster, you must set the following flags in your `kube-up` script:

* `MULTIZONE=true` - to prevent removal of control plane kubelets from zones different than server's default zone.
Required if you want to run control plane nodes in different zones, which is recommended.

* `ENABLE_ETCD_QUORUM_READ=true` - to ensure that reads from all API servers will return most up-to-date data.
If true, reads will be directed to leader etcd replica.
Setting this value to true is optional: reads will be more reliable but will also be slower.

Optionally, you can specify a GCE zone where the first control plane node is to be created.
Set the following flag:

* `KUBE_GCE_ZONE=zone` - zone where the first control plane node will run.

The following sample command sets up a HA-compatible cluster in the GCE zone europe-west1-b:

```shell
MULTIZONE=true KUBE_GCE_ZONE=europe-west1-b  ENABLE_ETCD_QUORUM_READS=true ./cluster/kube-up.sh
```

Note that the commands above create a cluster with one control plane node;
however, you can add new control plane nodes to the cluster with subsequent commands.

## Adding a new control plane node

After you have created an HA-compatible cluster, you can add control plane nodes to it.
You add control plane nodes by using a `kube-up` script with the following flags:

* `KUBE_REPLICATE_EXISTING_MASTER=true` - to create a replica of an existing control plane
node.

* `KUBE_GCE_ZONE=zone` - zone where the control plane node will run.
Must be in the same region as other control plane nodes' zones.

You don't need to set the `MULTIZONE` or `ENABLE_ETCD_QUORUM_READS` flags,
as those are inherited from when you started your HA-compatible cluster.

The following sample command replicates the control plane node on an existing
HA-compatible cluster:

```shell
KUBE_GCE_ZONE=europe-west1-c KUBE_REPLICATE_EXISTING_MASTER=true ./cluster/kube-up.sh
```

## Removing a control plane node

You can remove a control plane node from an HA cluster by using a `kube-down` script with the following flags:

* `KUBE_DELETE_NODES=false` - to restrain deletion of kubelets.

* `KUBE_GCE_ZONE=zone` - the zone from where the control plane node will be removed.

* `KUBE_REPLICA_NAME=replica_name` - (optional) the name of control plane node to
remove. If empty: any replica from the given zone will be removed.

The following sample command removes a control plane node from an existing HA cluster:

```shell
KUBE_DELETE_NODES=false KUBE_GCE_ZONE=europe-west1-c ./cluster/kube-down.sh
```

## Handling control plane node failures

If one of the control plane nodes in your HA cluster fails,
the best practice is to remove the node from your cluster and add a new control plane
node in the same zone.
The following sample commands demonstrate this process:

1. Remove the broken replica:

```shell
KUBE_DELETE_NODES=false KUBE_GCE_ZONE=replica_zone KUBE_REPLICA_NAME=replica_name ./cluster/kube-down.sh
```

<ol start="2"><li>Add a new node in place of the old one:</li></ol>

```shell
KUBE_GCE_ZONE=replica-zone KUBE_REPLICATE_EXISTING_MASTER=true ./cluster/kube-up.sh
```

## Best practices for replicating control plane nodes for HA clusters

* Try to place control plane nodes in different zones. During a zone failure, all
control plane nodes placed inside the zone will fail.
To survive zone failure, also place nodes in multiple zones
(see [multiple-zones](/docs/setup/best-practices/multiple-zones/) for details).

* Do not use a cluster with two control plane nodes. Consensus on a two-node
control plane requires both nodes running when changing persistent state.
As a result, both nodes are needed and a failure of any node turns the cluster
into majority failure state.
A two-node control plane is thus inferior, in terms of HA, to a cluster with
one control plane node.

* When you add a control plane node, cluster state (etcd) is copied to a new instance.
If the cluster is large, it may take a long time to duplicate its state.
This operation may be sped up by migrating the etcd data directory, as described in
the [etcd administration guide](https://etcd.io/docs/v2.3/admin_guide/#member-migration)
(we are considering adding support for etcd data dir migration in the future).



<!-- discussion -->

## Implementation notes

![ha-master-gce](/images/docs/ha-master-gce.png)

### Overview

Each of the control plane nodes will run the following components in the following mode:

* etcd instance: all instances will be clustered together using consensus;

* API server: each server will talk to local etcd - all API servers in the cluster will be available;

* controllers, scheduler, and cluster auto-scaler: will use lease mechanism - only one instance of each of them will be active in the cluster;

* add-on manager: each manager will work independently trying to keep add-ons in sync.

In addition, there will be a load balancer in front of API servers that will route external and internal traffic to them.

### Load balancing

When starting the second control plane node, a load balancer containing the two replicas will be created
and the IP address of the first replica will be promoted to IP address of load balancer.
Similarly, after removal of the penultimate control plane node, the load balancer will be removed and its IP address will be assigned to the last remaining replica.
Please note that creation and removal of load balancer are complex operations and it may take some time (~20 minutes) for them to propagate.

### Control plane service & kubelets

Instead of trying to keep an up-to-date list of Kubernetes apiserver in the Kubernetes service,
the system directs all traffic to the external IP:

* in case of a single node control plane, the IP points to the control plane node,

* in case of an HA control plane, the IP points to the load balancer in-front of the control plane nodes.

Similarly, the external IP will be used by kubelets to communicate with the control plane.

### Control plane node certificates

Kubernetes generates TLS certificates for the external public IP and local IP for each control plane node.
There are no certificates for the ephemeral public IP for control plane nodes;
to access a control plane node via its ephemeral public IP, you must skip TLS verification.

### Clustering etcd

To allow etcd clustering, ports needed to communicate between etcd instances will be opened (for inside cluster communication).
To make such deployment secure, communication between etcd instances is authorized using SSL.

### API server identity

{{< feature-state state="alpha" for_k8s_version="v1.20" >}}

The API Server Identity feature is controlled by a
[feature gate](/docs/reference/command-line-tools-reference/feature-gates/)
and is not enabled by default. You can activate API Server Identity by enabling
the feature gate named `APIServerIdentity` when you start the
{{< glossary_tooltip text="API Server" term_id="kube-apiserver" >}}:

```shell
kube-apiserver \
--feature-gates=APIServerIdentity=true \
 # …and other flags as usual
```

During bootstrap, each kube-apiserver assigns a unique ID to itself. The ID is
in the format of `kube-apiserver-{UUID}`. Each kube-apiserver creates a
[Lease](/docs/reference/generated/kubernetes-api/{{< param "version" >}}//#lease-v1-coordination-k8s-io)
in the _kube-system_ {{< glossary_tooltip text="namespaces" term_id="namespace">}}.
The Lease name is the unique ID for the kube-apiserver. The Lease contains a
label `k8s.io/component=kube-apiserver`. Each kube-apiserver refreshes its
Lease every `IdentityLeaseRenewIntervalSeconds` (defaults to 10s). Each
kube-apiserver also checks all the kube-apiserver identity Leases every
`IdentityLeaseDurationSeconds` (defaults to 3600s), and deletes Leases that
hasn't got refreshed for more than `IdentityLeaseDurationSeconds`.
`IdentityLeaseRenewIntervalSeconds` and `IdentityLeaseDurationSeconds` can be
configured by kube-apiserver flags `identity-lease-renew-interval-seconds`
and `identity-lease-duration-seconds`.

Enabling this feature is a prerequisite for using features that involve HA API
server coordination (for example, the `StorageVersionAPI` feature gate).

## Additional reading

[Automated HA master deployment - design doc](https://git.k8s.io/community/contributors/design-proposals/cluster-lifecycle/ha_master.md)


