---
title: Scheduler Configuration
content_type: concept
weight: 20
---

{{< feature-state for_k8s_version="v1.19" state="beta" >}}

You can customize the behavior of the `kube-scheduler` by writing a configuration
file and passing its path as a command line argument.

<!-- overview -->

<!-- body -->

A scheduling Profile allows you to configure the different stages of scheduling
in the {{< glossary_tooltip text="kube-scheduler" term_id="kube-scheduler" >}}.
Each stage is exposed in a extension point. Plugins provide scheduling behaviors
by implementing one or more of these extension points.

You can specify scheduling profiles by running `kube-scheduler --config <filename>`,
using the
KubeSchedulerConfiguration ([v1beta1](/docs/reference/config-api/kube-scheduler-config.v1beta1/)
or [v1beta2](/docs/reference/config-api/kube-scheduler-config.v1beta2/)) 
struct.

A minimal configuration looks as follows:

```yaml
apiVersion: kubescheduler.config.k8s.io/v1beta2
kind: KubeSchedulerConfiguration
clientConnection:
  kubeconfig: /etc/srv/kubernetes/kube-scheduler/kubeconfig
```

## Profiles

A scheduling Profile allows you to configure the different stages of scheduling
in the {{< glossary_tooltip text="kube-scheduler" term_id="kube-scheduler" >}}.
Each stage is exposed in an [extension point](#extension-points).
[Plugins](#scheduling-plugins) provide scheduling behaviors by implementing one
or more of these extension points.

You can configure a single instance of `kube-scheduler` to run
[multiple profiles](#multiple-profiles).

### Extension points

Scheduling happens in a series of stages that are exposed through the following
extension points:

1. `queueSort`: These plugins provide an ordering function that is used to
   sort pending Pods in the scheduling queue. Exactly one queue sort plugin
   may be enabled at a time.
1. `preFilter`: These plugins are used to pre-process or check information
   about a Pod or the cluster before filtering. They can mark a pod as
   unschedulable.
1. `filter`: These plugins are the equivalent of Predicates in a scheduling
   Policy and are used to filter out nodes that can not run the Pod. Filters
   are called in the configured order. A pod is marked as unschedulable if no
   nodes pass all the filters.
1. `postFilter`: These plugins are called in their configured order when no
   feasible nodes were found for the pod. If any `postFilter` plugin marks the
   Pod _schedulable_, the remaining plugins are not called.
1. `preScore`: This is an informational extension point that can be used
   for doing pre-scoring work.
1. `score`: These plugins provide a score to each node that has passed the
   filtering phase. The scheduler will then select the node with the highest
   weighted scores sum.
1. `reserve`: This is an informational extension point that notifies plugins
   when resources have been reserved for a given Pod. Plugins also implement an
   `Unreserve` call that gets called in the case of failure during or after
   `Reserve`.
1. `permit`: These plugins can prevent or delay the binding of a Pod.
1. `preBind`: These plugins perform any work required before a Pod is bound.
1. `bind`: The plugins bind a Pod to a Node. `bind` plugins are called in order
   and once one has done the binding, the remaining plugins are skipped. At
   least one bind plugin is required.
1. `postBind`: This is an informational extension point that is called after
   a Pod has been bound.

For each extension point, you could disable specific [default plugins](#scheduling-plugins)
or enable your own. For example:

```yaml
apiVersion: kubescheduler.config.k8s.io/v1beta2
kind: KubeSchedulerConfiguration
profiles:
  - plugins:
      score:
        disabled:
        - name: NodeResourcesLeastAllocated
        enabled:
        - name: MyCustomPluginA
          weight: 2
        - name: MyCustomPluginB
          weight: 1
```

You can use `*` as name in the disabled array to disable all default plugins
for that extension point. This can also be used to rearrange plugins order, if
desired.
   
### Scheduling plugins

The following plugins, enabled by default, implement one or more of these
extension points:

- `ImageLocality`: Favors nodes that already have the container images that the
  Pod runs.
  Extension points: `score`.
- `TaintToleration`: Implements
  [taints and tolerations](/docs/concepts/scheduling-eviction/taint-and-toleration/).
  Implements extension points: `filter`, `preScore`, `score`.
- `NodeName`: Checks if a Pod spec node name matches the current node.
  Extension points: `filter`.
- `NodePorts`: Checks if a node has free ports for the requested Pod ports.
  Extension points: `preFilter`, `filter`.
- `NodePreferAvoidPods`: Scores nodes according to the node
  {{< glossary_tooltip text="annotation" term_id="annotation" >}}
  `scheduler.alpha.kubernetes.io/preferAvoidPods`.
  Extension points: `score`.
- `NodeAffinity`: Implements
  [node selectors](/docs/concepts/scheduling-eviction/assign-pod-node/#nodeselector)
  and [node affinity](/docs/concepts/scheduling-eviction/assign-pod-node/#node-affinity).
  Extension points: `filter`, `score`.
- `PodTopologySpread`: Implements
  [Pod topology spread](/docs/concepts/workloads/pods/pod-topology-spread-constraints/).
  Extension points: `preFilter`, `filter`, `preScore`, `score`.
- `NodeUnschedulable`: Filters out nodes that have `.spec.unschedulable` set to
  true.
  Extension points: `filter`.
- `NodeResourcesFit`: Checks if the node has all the resources that the Pod is
  requesting. The score can use one of three strategies: `LeastAllocated`
  (default), `MostAllocated` and `RequestedToCapacityRatio`.
  Extension points: `preFilter`, `filter`, `score`.
- `NodeResourcesBalancedAllocation`: Favors nodes that would obtain a more
  balanced resource usage if the Pod is scheduled there.
  Extension points: `score`.
- `VolumeBinding`: Checks if the node has or if it can bind the requested
  {{< glossary_tooltip text="volumes" term_id="volume" >}}.
  Extension points: `preFilter`, `filter`, `reserve`, `preBind`, `score`.
  {{< note >}}
  `score` extension point is enabled when `VolumeCapacityPriority` feature is
  enabled. It prioritizes the smallest PVs that can fit the requested volume
  size.
  {{< /note >}}
- `VolumeRestrictions`: Checks that volumes mounted in the node satisfy
  restrictions that are specific to the volume provider.
  Extension points: `filter`.
- `VolumeZone`: Checks that volumes requested satisfy any zone requirements they
  might have.
  Extension points: `filter`.
- `NodeVolumeLimits`: Checks that CSI volume limits can be satisfied for the
  node.
  Extension points: `filter`.
- `EBSLimits`: Checks that AWS EBS volume limits can be satisfied for the node.
  Extension points: `filter`.
- `GCEPDLimits`: Checks that GCP-PD volume limits can be satisfied for the node.
  Extension points: `filter`.
- `AzureDiskLimits`: Checks that Azure disk volume limits can be satisfied for
  the node.
  Extension points: `filter`.
- `InterPodAffinity`: Implements
  [inter-Pod affinity and anti-affinity](/docs/concepts/scheduling-eviction/assign-pod-node/#inter-pod-affinity-and-anti-affinity).
  Extension points: `preFilter`, `filter`, `preScore`, `score`.
- `PrioritySort`: Provides the default priority based sorting.
  Extension points: `queueSort`.
- `DefaultBinder`: Provides the default binding mechanism.
  Extension points: `bind`.
- `DefaultPreemption`: Provides the default preemption mechanism.
  Extension points: `postFilter`.
  
You can also enable the following plugins, through the component config APIs,
that are not enabled by default:

- `SelectorSpread`: Favors spreading across nodes for Pods that belong to
  {{< glossary_tooltip text="Services" term_id="service" >}},
  {{< glossary_tooltip text="ReplicaSets" term_id="replica-set" >}} and
  {{< glossary_tooltip text="StatefulSets" term_id="statefulset" >}}.
  Extension points: `preScore`, `score`.
- `CinderLimits`: Checks that [OpenStack Cinder](https://docs.openstack.org/cinder/)
  volume limits can be satisfied for the node.
  Extension points: `filter`.
  
The following plugins are deprecated and can only be enabled in a `v1beta1`
configuration:

- `NodeResourcesLeastAllocated`: Favors nodes that have a low allocation of
  resources.
  Extension points: `score`.
- `NodeResourcesMostAllocated`: Favors nodes that have a high allocation of
  resources.
  Extension points: `score`.
- `RequestedToCapacityRatio`: Favor nodes according to a configured function of
  the allocated resources.
  Extension points: `score`.
- `NodeLabel`: Filters and / or scores a node according to configured
  {{< glossary_tooltip text="label(s)" term_id="label" >}}.
  Extension points: `filter`, `score`.
- `ServiceAffinity`: Checks that Pods that belong to a
  {{< glossary_tooltip term_id="service" >}} fit in a set of nodes defined by
  configured labels. This plugin also favors spreading the Pods belonging to a
  Service across nodes.
  Extension points: `preFilter`, `filter`, `score`.
- `NodePreferAvoidPods`: Prioritizes nodes according to the node annotation
  `scheduler.alpha.kubernetes.io/preferAvoidPods`.
  Extension points: `score`.
  
### Multiple profiles

You can configure `kube-scheduler` to run more than one profile.
Each profile has an associated scheduler name and can have a different set of
plugins configured in its [extension points](#extension-points).

With the following sample configuration, the scheduler will run with two
profiles: one with the default plugins and one with all scoring plugins
disabled.

```yaml
apiVersion: kubescheduler.config.k8s.io/v1beta2
kind: KubeSchedulerConfiguration
profiles:
  - schedulerName: default-scheduler
  - schedulerName: no-scoring-scheduler
    plugins:
      preScore:
        disabled:
        - name: '*'
      score:
        disabled:
        - name: '*'
```

Pods that want to be scheduled according to a specific profile can include
the corresponding scheduler name in its `.spec.schedulerName`.

By default, one profile with the scheduler name `default-scheduler` is created.
This profile includes the default plugins described above. When declaring more
than one profile, a unique scheduler name for each of them is required.

If a Pod doesn't specify a scheduler name, kube-apiserver will set it to
`default-scheduler`. Therefore, a profile with this scheduler name should exist
to get those pods scheduled.

{{< note >}}
Pod's scheduling events have `.spec.schedulerName` as the ReportingController.
Events for leader election use the scheduler name of the first profile in the
list.
{{< /note >}}

{{< note >}}
All profiles must use the same plugin in the `queueSort` extension point and have
the same configuration parameters (if applicable). This is because the scheduler
only has one pending pods queue.
{{< /note >}}

## {{% heading "whatsnext" %}}

* Read the [kube-scheduler reference](/docs/reference/command-line-tools-reference/kube-scheduler/)
* Learn about [scheduling](/docs/concepts/scheduling-eviction/kube-scheduler/)
* Read the [kube-scheduler configuration (v1beta1)](/docs/reference/config-api/kube-scheduler-config.v1beta1/) reference
* Read the [kube-scheduler configuration (v1beta2)](/docs/reference/config-api/kube-scheduler-config.v1beta2/) reference

