---
reviewers:
- davidopp
- lavalamp
title: Considerations for large clusters
weight: 20
---

A cluster is a set of {{< glossary_tooltip text="nodes" term_id="node" >}} (physical
or virtual machines) running Kubernetes agents, managed by the
{{< glossary_tooltip text="control plane" term_id="control-plane" >}}.
Kubernetes {{< param "version" >}} supports clusters with up to 5000 nodes. More specifically,
Kubernetes is designed to accommodate configurations that meet *all* of the following criteria:

* No more than 110 pods per node
* No more than 5000 nodes
* No more than 150000 total pods
* No more than 300000 total containers

You can scale your cluster by adding or removing nodes. The way you do this depends
on how your cluster is deployed.

## Cloud provider resource quotas {#quota-issues}

To avoid running into cloud provider quota issues, when creating a cluster with many nodes,
consider:
* Requesting a quota increase for cloud resources such as:
    * Computer instances
    * CPUs
    * Storage volumes
    * In-use IP addresses
    * Packet filtering rule sets
    * Number of load balancers
    * Network subnets
    * Log streams
* Gating the cluster scaling actions to bring up new nodes in batches, with a pause
  between batches, because some cloud providers rate limit the creation of new instances.

## Control plane components

For a large cluster, you need a control plane with sufficient compute and other
resources.

Typically you would run one or two control plane instances per failure zone,
scaling those instances vertically first and then scaling horizontally after reaching
the point of falling returns to (vertical) scale.

You should run at least one instance per failure zone to provide fault-tolerance. Kubernetes
nodes do not automatically steer traffic towards control-plane endpoints that are in the
same failure zone; however, your cloud provider might have its own mechanisms to do this.

For example, using a managed load balancer, you configure the load balancer to send traffic
that originates from the kubelet and Pods in failure zone _A_, and direct that traffic only
to the control plane hosts that are also in zone _A_. If a single control-plane host or
endpoint failure zone _A_ goes offline, that means that all the control-plane traffic for
nodes in zone _A_ is now being sent between zones. Running multiple control plane hosts in
each zone makes that outcome less likely.

### etcd storage

To improve performance of large clusters, you can store Event objects in a separate
dedicated etcd instance.

When creating a cluster, you can (using custom tooling):

* start and configure additional etcd instance
* configure the {{< glossary_tooltip term_id="kube-apiserver" text="API server" >}} to use it for storing events

See [Operating etcd clusters for Kubernetes](/docs/tasks/administer-cluster/configure-upgrade-etcd/) and
[Set up a High Availability etcd cluster with kubeadm](/docs/setup/production-environment/tools/kubeadm/setup-ha-etcd-with-kubeadm/)
for details on configuring and managing etcd for a large cluster.

## Addon resources

Kubernetes [resource limits](/docs/concepts/configuration/manage-resources-containers/)
help to minimize the impact of memory leaks and other ways that pods and containers can
impact on other components. These resource limits apply to
{{< glossary_tooltip text="addon" term_id="addons" >}} resources just as they apply to application workloads.

For example, you can set CPU and memory limits for a logging component:

```yaml
  ...
  containers:
  - name: fluentd-cloud-logging
    image: fluent/fluentd-kubernetes-daemonset:v1
    resources:
      limits:
        cpu: 100m
        memory: 200Mi
```

Addons' default limits are typically based on data collected from experience running
each addon on small or medium Kubernetes clusters. When running on large
clusters, addons often consume more of some resources than their default limits.
If a large cluster is deployed without adjusting these values, the addon(s)
may continuously get killed because they keep hitting the memory limit.
Alternatively, the addon may run but with poor performance due to CPU time
slice restrictions.

To avoid running into cluster addon resource issues, when creating a cluster with
many nodes, consider the following:

* Some addons scale vertically - there is one replica of the addon for the cluster
  or serving a whole failure zone. For these addons, increase requests and limits
  as you scale out your cluster.
* Many addons scale horizontally - you add capacity by running more pods - but with
  a very large cluster you may also need to raise CPU or memory limits slightly.
  The VerticalPodAutoscaler can run in _recommender_ mode to provide suggested
  figures for requests and limits.
* Some addons run as one copy per node, controlled by a {{< glossary_tooltip text="DaemonSet"
  term_id="daemonset" >}}: for example, a node-level log aggregator. Similar to
  the case with horizontally-scaled addons, you may also need to raise CPU or memory
  limits slightly.

## {{% heading "whatsnext" %}}

`VerticalPodAutoscaler` is a custom resource that you can deploy into your cluster
to help you manage resource requests and limits for pods.  
Visit [Vertical Pod Autoscaler](https://github.com/kubernetes/autoscaler/tree/master/vertical-pod-autoscaler#readme)
to learn more about `VerticalPodAutoscaler` and how you can use it to scale cluster
components, including cluster-critical addons.

The [cluster autoscaler](https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler#readme)
integrates with a number of cloud providers to help you run the right number of
nodes for the level of resource demand in your cluster.

The [addon resizer](https://github.com/kubernetes/autoscaler/tree/master/addon-resizer#readme)
helps you in resizing the addons automatically as your cluster's scale changes.