---
title: kube-scheduler Configuration (v1beta2)
content_type: tool-reference
package: kubescheduler.config.k8s.io/v1beta2
auto_generated: true
---


## Resource Types 


- [DefaultPreemptionArgs](#kubescheduler-config-k8s-io-v1beta2-DefaultPreemptionArgs)
- [InterPodAffinityArgs](#kubescheduler-config-k8s-io-v1beta2-InterPodAffinityArgs)
- [KubeSchedulerConfiguration](#kubescheduler-config-k8s-io-v1beta2-KubeSchedulerConfiguration)
- [NodeAffinityArgs](#kubescheduler-config-k8s-io-v1beta2-NodeAffinityArgs)
- [NodeResourcesFitArgs](#kubescheduler-config-k8s-io-v1beta2-NodeResourcesFitArgs)
- [NodeResourcesLeastAllocatedArgs](#kubescheduler-config-k8s-io-v1beta2-NodeResourcesLeastAllocatedArgs)
- [NodeResourcesMostAllocatedArgs](#kubescheduler-config-k8s-io-v1beta2-NodeResourcesMostAllocatedArgs)
- [PodTopologySpreadArgs](#kubescheduler-config-k8s-io-v1beta2-PodTopologySpreadArgs)
- [RequestedToCapacityRatioArgs](#kubescheduler-config-k8s-io-v1beta2-RequestedToCapacityRatioArgs)
- [VolumeBindingArgs](#kubescheduler-config-k8s-io-v1beta2-VolumeBindingArgs)
- [Policy](#kubescheduler-config-k8s-io-v1-Policy)
  
    


## `DefaultPreemptionArgs`     {#kubescheduler-config-k8s-io-v1beta2-DefaultPreemptionArgs}
    




DefaultPreemptionArgs holds arguments used to configure the
DefaultPreemption plugin.

<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
<tbody>
    
<tr><td><code>apiVersion</code><br/>string</td><td><code>kubescheduler.config.k8s.io/v1beta2</code></td></tr>
<tr><td><code>kind</code><br/>string</td><td><code>DefaultPreemptionArgs</code></td></tr>
    

  
  
<tr><td><code>minCandidateNodesPercentage</code> <B>[Required]</B><br/>
<code>int32</code>
</td>
<td>
   MinCandidateNodesPercentage is the minimum number of candidates to
shortlist when dry running preemption as a percentage of number of nodes.
Must be in the range [0, 100]. Defaults to 10% of the cluster size if
unspecified.</td>
</tr>
    
  
<tr><td><code>minCandidateNodesAbsolute</code> <B>[Required]</B><br/>
<code>int32</code>
</td>
<td>
   MinCandidateNodesAbsolute is the absolute minimum number of candidates to
shortlist. The likely number of candidates enumerated for dry running
preemption is given by the formula:
numCandidates = max(numNodes &lowast; minCandidateNodesPercentage, minCandidateNodesAbsolute)
We say "likely" because there are other factors such as PDB violations
that play a role in the number of candidates shortlisted. Must be at least
0 nodes. Defaults to 100 nodes if unspecified.</td>
</tr>
    
  
</tbody>
</table>
    


## `InterPodAffinityArgs`     {#kubescheduler-config-k8s-io-v1beta2-InterPodAffinityArgs}
    




InterPodAffinityArgs holds arguments used to configure the InterPodAffinity plugin.

<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
<tbody>
    
<tr><td><code>apiVersion</code><br/>string</td><td><code>kubescheduler.config.k8s.io/v1beta2</code></td></tr>
<tr><td><code>kind</code><br/>string</td><td><code>InterPodAffinityArgs</code></td></tr>
    

  
  
<tr><td><code>hardPodAffinityWeight</code> <B>[Required]</B><br/>
<code>int32</code>
</td>
<td>
   HardPodAffinityWeight is the scoring weight for existing pods with a
matching hard affinity to the incoming pod.</td>
</tr>
    
  
</tbody>
</table>
    


## `KubeSchedulerConfiguration`     {#kubescheduler-config-k8s-io-v1beta2-KubeSchedulerConfiguration}
    




KubeSchedulerConfiguration configures a scheduler

<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
<tbody>
    
<tr><td><code>apiVersion</code><br/>string</td><td><code>kubescheduler.config.k8s.io/v1beta2</code></td></tr>
<tr><td><code>kind</code><br/>string</td><td><code>KubeSchedulerConfiguration</code></td></tr>
    

  
  
<tr><td><code>parallelism</code> <B>[Required]</B><br/>
<code>int32</code>
</td>
<td>
   Parallelism defines the amount of parallelism in algorithms for scheduling a Pods. Must be greater than 0. Defaults to 16</td>
</tr>
    
  
<tr><td><code>leaderElection</code> <B>[Required]</B><br/>
<a href="#LeaderElectionConfiguration"><code>LeaderElectionConfiguration</code></a>
</td>
<td>
   LeaderElection defines the configuration of leader election client.</td>
</tr>
    
  
<tr><td><code>clientConnection</code> <B>[Required]</B><br/>
<a href="#ClientConnectionConfiguration"><code>ClientConnectionConfiguration</code></a>
</td>
<td>
   ClientConnection specifies the kubeconfig file and client connection
settings for the proxy server to use when communicating with the apiserver.</td>
</tr>
    
  
<tr><td><code>healthzBindAddress</code> <B>[Required]</B><br/>
<code>string</code>
</td>
<td>
   HealthzBindAddress is the IP address and port for the health check server to serve on,
defaulting to 0.0.0.0:10251</td>
</tr>
    
  
<tr><td><code>metricsBindAddress</code> <B>[Required]</B><br/>
<code>string</code>
</td>
<td>
   MetricsBindAddress is the IP address and port for the metrics server to
serve on, defaulting to 0.0.0.0:10251.</td>
</tr>
    
  
<tr><td><code>DebuggingConfiguration</code> <B>[Required]</B><br/>
<a href="#DebuggingConfiguration"><code>DebuggingConfiguration</code></a>
</td>
<td>(Members of <code>DebuggingConfiguration</code> are embedded into this type.)
   DebuggingConfiguration holds configuration for Debugging related features
TODO: We might wanna make this a substruct like Debugging componentbaseconfigv1alpha1.DebuggingConfiguration</td>
</tr>
    
  
<tr><td><code>percentageOfNodesToScore</code> <B>[Required]</B><br/>
<code>int32</code>
</td>
<td>
   PercentageOfNodesToScore is the percentage of all nodes that once found feasible
for running a pod, the scheduler stops its search for more feasible nodes in
the cluster. This helps improve scheduler's performance. Scheduler always tries to find
at least "minFeasibleNodesToFind" feasible nodes no matter what the value of this flag is.
Example: if the cluster size is 500 nodes and the value of this flag is 30,
then scheduler stops finding further feasible nodes once it finds 150 feasible ones.
When the value is 0, default percentage (5%--50% based on the size of the cluster) of the
nodes will be scored.</td>
</tr>
    
  
<tr><td><code>podInitialBackoffSeconds</code> <B>[Required]</B><br/>
<code>int64</code>
</td>
<td>
   PodInitialBackoffSeconds is the initial backoff for unschedulable pods.
If specified, it must be greater than 0. If this value is null, the default value (1s)
will be used.</td>
</tr>
    
  
<tr><td><code>podMaxBackoffSeconds</code> <B>[Required]</B><br/>
<code>int64</code>
</td>
<td>
   PodMaxBackoffSeconds is the max backoff for unschedulable pods.
If specified, it must be greater than podInitialBackoffSeconds. If this value is null,
the default value (10s) will be used.</td>
</tr>
    
  
<tr><td><code>profiles</code> <B>[Required]</B><br/>
<a href="#kubescheduler-config-k8s-io-v1beta2-KubeSchedulerProfile"><code>[]KubeSchedulerProfile</code></a>
</td>
<td>
   Profiles are scheduling profiles that kube-scheduler supports. Pods can
choose to be scheduled under a particular profile by setting its associated
scheduler name. Pods that don't specify any scheduler name are scheduled
with the "default-scheduler" profile, if present here.</td>
</tr>
    
  
<tr><td><code>extenders</code> <B>[Required]</B><br/>
<a href="#kubescheduler-config-k8s-io-v1beta2-Extender"><code>[]Extender</code></a>
</td>
<td>
   Extenders are the list of scheduler extenders, each holding the values of how to communicate
with the extender. These extenders are shared by all scheduler profiles.</td>
</tr>
    
  
</tbody>
</table>
    


## `NodeAffinityArgs`     {#kubescheduler-config-k8s-io-v1beta2-NodeAffinityArgs}
    




NodeAffinityArgs holds arguments to configure the NodeAffinity plugin.

<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
<tbody>
    
<tr><td><code>apiVersion</code><br/>string</td><td><code>kubescheduler.config.k8s.io/v1beta2</code></td></tr>
<tr><td><code>kind</code><br/>string</td><td><code>NodeAffinityArgs</code></td></tr>
    

  
  
<tr><td><code>addedAffinity</code><br/>
<a href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.20/#nodeaffinity-v1-core"><code>core/v1.NodeAffinity</code></a>
</td>
<td>
   AddedAffinity is applied to all Pods additionally to the NodeAffinity
specified in the PodSpec. That is, Nodes need to satisfy AddedAffinity
AND .spec.NodeAffinity. AddedAffinity is empty by default (all Nodes
match).
When AddedAffinity is used, some Pods with affinity requirements that match
a specific Node (such as Daemonset Pods) might remain unschedulable.</td>
</tr>
    
  
</tbody>
</table>
    


## `NodeResourcesFitArgs`     {#kubescheduler-config-k8s-io-v1beta2-NodeResourcesFitArgs}
    




NodeResourcesFitArgs holds arguments used to configure the NodeResourcesFit plugin.

<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
<tbody>
    
<tr><td><code>apiVersion</code><br/>string</td><td><code>kubescheduler.config.k8s.io/v1beta2</code></td></tr>
<tr><td><code>kind</code><br/>string</td><td><code>NodeResourcesFitArgs</code></td></tr>
    

  
  
<tr><td><code>ignoredResources</code> <B>[Required]</B><br/>
<code>[]string</code>
</td>
<td>
   IgnoredResources is the list of resources that NodeResources fit filter
should ignore.</td>
</tr>
    
  
<tr><td><code>ignoredResourceGroups</code> <B>[Required]</B><br/>
<code>[]string</code>
</td>
<td>
   IgnoredResourceGroups defines the list of resource groups that NodeResources fit filter should ignore.
e.g. if group is ["example.com"], it will ignore all resource names that begin
with "example.com", such as "example.com/aaa" and "example.com/bbb".
A resource group name can't contain '/'.</td>
</tr>
    
  
</tbody>
</table>
    


## `NodeResourcesLeastAllocatedArgs`     {#kubescheduler-config-k8s-io-v1beta2-NodeResourcesLeastAllocatedArgs}
    




NodeResourcesLeastAllocatedArgs holds arguments used to configure NodeResourcesLeastAllocated plugin.

<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
<tbody>
    
<tr><td><code>apiVersion</code><br/>string</td><td><code>kubescheduler.config.k8s.io/v1beta2</code></td></tr>
<tr><td><code>kind</code><br/>string</td><td><code>NodeResourcesLeastAllocatedArgs</code></td></tr>
    

  
  
<tr><td><code>resources</code> <B>[Required]</B><br/>
<a href="#kubescheduler-config-k8s-io-v1beta2-ResourceSpec"><code>[]ResourceSpec</code></a>
</td>
<td>
   Resources to be managed, if no resource is provided, default resource set with both
the weight of "cpu" and "memory" set to "1" will be applied.
Resource with "0" weight will not accountable for the final score.</td>
</tr>
    
  
</tbody>
</table>
    


## `NodeResourcesMostAllocatedArgs`     {#kubescheduler-config-k8s-io-v1beta2-NodeResourcesMostAllocatedArgs}
    




NodeResourcesMostAllocatedArgs holds arguments used to configure NodeResourcesMostAllocated plugin.

<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
<tbody>
    
<tr><td><code>apiVersion</code><br/>string</td><td><code>kubescheduler.config.k8s.io/v1beta2</code></td></tr>
<tr><td><code>kind</code><br/>string</td><td><code>NodeResourcesMostAllocatedArgs</code></td></tr>
    

  
  
<tr><td><code>resources</code> <B>[Required]</B><br/>
<a href="#kubescheduler-config-k8s-io-v1beta2-ResourceSpec"><code>[]ResourceSpec</code></a>
</td>
<td>
   Resources to be managed, if no resource is provided, default resource set with both
the weight of "cpu" and "memory" set to "1" will be applied.
Resource with "0" weight will not accountable for the final score.</td>
</tr>
    
  
</tbody>
</table>
    


## `PodTopologySpreadArgs`     {#kubescheduler-config-k8s-io-v1beta2-PodTopologySpreadArgs}
    




PodTopologySpreadArgs holds arguments used to configure the PodTopologySpread plugin.

<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
<tbody>
    
<tr><td><code>apiVersion</code><br/>string</td><td><code>kubescheduler.config.k8s.io/v1beta2</code></td></tr>
<tr><td><code>kind</code><br/>string</td><td><code>PodTopologySpreadArgs</code></td></tr>
    

  
  
<tr><td><code>defaultConstraints</code><br/>
<a href="https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.20/#topologyspreadconstraint-v1-core"><code>[]core/v1.TopologySpreadConstraint</code></a>
</td>
<td>
   DefaultConstraints defines topology spread constraints to be applied to
Pods that don't define any in `pod.spec.topologySpreadConstraints`.
`.defaultConstraints[&lowast;].labelSelectors` must be empty, as they are
deduced from the Pod's membership to Services, ReplicationControllers,
ReplicaSets or StatefulSets.
When not empty, .defaultingType must be "List".</td>
</tr>
    
  
<tr><td><code>defaultingType</code><br/>
<a href="#kubescheduler-config-k8s-io-v1beta2-PodTopologySpreadConstraintsDefaulting"><code>PodTopologySpreadConstraintsDefaulting</code></a>
</td>
<td>
   DefaultingType determines how .defaultConstraints are deduced. Can be one
of "System" or "List".

- "System": Use kubernetes defined constraints that spread Pods among
  Nodes and Zones.
- "List": Use constraints defined in .defaultConstraints.

Defaults to "List" if feature gate DefaultPodTopologySpread is disabled
and to "System" if enabled.</td>
</tr>
    
  
</tbody>
</table>
    


## `RequestedToCapacityRatioArgs`     {#kubescheduler-config-k8s-io-v1beta2-RequestedToCapacityRatioArgs}
    




RequestedToCapacityRatioArgs holds arguments used to configure RequestedToCapacityRatio plugin.

<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
<tbody>
    
<tr><td><code>apiVersion</code><br/>string</td><td><code>kubescheduler.config.k8s.io/v1beta2</code></td></tr>
<tr><td><code>kind</code><br/>string</td><td><code>RequestedToCapacityRatioArgs</code></td></tr>
    

  
  
<tr><td><code>shape</code> <B>[Required]</B><br/>
<a href="#kubescheduler-config-k8s-io-v1beta2-UtilizationShapePoint"><code>[]UtilizationShapePoint</code></a>
</td>
<td>
   Points defining priority function shape</td>
</tr>
    
  
<tr><td><code>resources</code> <B>[Required]</B><br/>
<a href="#kubescheduler-config-k8s-io-v1beta2-ResourceSpec"><code>[]ResourceSpec</code></a>
</td>
<td>
   Resources to be managed</td>
</tr>
    
  
</tbody>
</table>
    


## `VolumeBindingArgs`     {#kubescheduler-config-k8s-io-v1beta2-VolumeBindingArgs}
    




VolumeBindingArgs holds arguments used to configure the VolumeBinding plugin.

<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
<tbody>
    
<tr><td><code>apiVersion</code><br/>string</td><td><code>kubescheduler.config.k8s.io/v1beta2</code></td></tr>
<tr><td><code>kind</code><br/>string</td><td><code>VolumeBindingArgs</code></td></tr>
    

  
  
<tr><td><code>bindTimeoutSeconds</code> <B>[Required]</B><br/>
<code>int64</code>
</td>
<td>
   BindTimeoutSeconds is the timeout in seconds in volume binding operation.
Value must be non-negative integer. The value zero indicates no waiting.
If this value is nil, the default value (600) will be used.</td>
</tr>
    
  
</tbody>
</table>
    


## `Extender`     {#kubescheduler-config-k8s-io-v1beta2-Extender}
    



**Appears in:**

- [KubeSchedulerConfiguration](#kubescheduler-config-k8s-io-v1beta2-KubeSchedulerConfiguration)


Extender holds the parameters used to communicate with the extender. If a verb is unspecified/empty,
it is assumed that the extender chose not to provide that extension.

<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
<tbody>
    

  
<tr><td><code>urlPrefix</code> <B>[Required]</B><br/>
<code>string</code>
</td>
<td>
   URLPrefix at which the extender is available</td>
</tr>
    
  
<tr><td><code>filterVerb</code> <B>[Required]</B><br/>
<code>string</code>
</td>
<td>
   Verb for the filter call, empty if not supported. This verb is appended to the URLPrefix when issuing the filter call to extender.</td>
</tr>
    
  
<tr><td><code>preemptVerb</code> <B>[Required]</B><br/>
<code>string</code>
</td>
<td>
   Verb for the preempt call, empty if not supported. This verb is appended to the URLPrefix when issuing the preempt call to extender.</td>
</tr>
    
  
<tr><td><code>prioritizeVerb</code> <B>[Required]</B><br/>
<code>string</code>
</td>
<td>
   Verb for the prioritize call, empty if not supported. This verb is appended to the URLPrefix when issuing the prioritize call to extender.</td>
</tr>
    
  
<tr><td><code>weight</code> <B>[Required]</B><br/>
<code>int64</code>
</td>
<td>
   The numeric multiplier for the node scores that the prioritize call generates.
The weight should be a positive integer</td>
</tr>
    
  
<tr><td><code>bindVerb</code> <B>[Required]</B><br/>
<code>string</code>
</td>
<td>
   Verb for the bind call, empty if not supported. This verb is appended to the URLPrefix when issuing the bind call to extender.
If this method is implemented by the extender, it is the extender's responsibility to bind the pod to apiserver. Only one extender
can implement this function.</td>
</tr>
    
  
<tr><td><code>enableHTTPS</code> <B>[Required]</B><br/>
<code>bool</code>
</td>
<td>
   EnableHTTPS specifies whether https should be used to communicate with the extender</td>
</tr>
    
  
<tr><td><code>tlsConfig</code> <B>[Required]</B><br/>
<a href="#kubescheduler-config-k8s-io-v1-ExtenderTLSConfig"><code>ExtenderTLSConfig</code></a>
</td>
<td>
   TLSConfig specifies the transport layer security config</td>
</tr>
    
  
<tr><td><code>httpTimeout</code> <B>[Required]</B><br/>
<a href="https://godoc.org/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
</td>
<td>
   HTTPTimeout specifies the timeout duration for a call to the extender. Filter timeout fails the scheduling of the pod. Prioritize
timeout is ignored, k8s/other extenders priorities are used to select the node.</td>
</tr>
    
  
<tr><td><code>nodeCacheCapable</code> <B>[Required]</B><br/>
<code>bool</code>
</td>
<td>
   NodeCacheCapable specifies that the extender is capable of caching node information,
so the scheduler should only send minimal information about the eligible nodes
assuming that the extender already cached full details of all nodes in the cluster</td>
</tr>
    
  
<tr><td><code>managedResources</code><br/>
<a href="#kubescheduler-config-k8s-io-v1-ExtenderManagedResource"><code>[]ExtenderManagedResource</code></a>
</td>
<td>
   ManagedResources is a list of extended resources that are managed by
this extender.
- A pod will be sent to the extender on the Filter, Prioritize and Bind
  (if the extender is the binder) phases iff the pod requests at least
  one of the extended resources in this list. If empty or unspecified,
  all pods will be sent to this extender.
- If IgnoredByScheduler is set to true for a resource, kube-scheduler
  will skip checking the resource in predicates.</td>
</tr>
    
  
<tr><td><code>ignorable</code> <B>[Required]</B><br/>
<code>bool</code>
</td>
<td>
   Ignorable specifies if the extender is ignorable, i.e. scheduling should not
fail when the extender returns an error or is not reachable.</td>
</tr>
    
  
</tbody>
</table>
    


## `KubeSchedulerProfile`     {#kubescheduler-config-k8s-io-v1beta2-KubeSchedulerProfile}
    



**Appears in:**

- [KubeSchedulerConfiguration](#kubescheduler-config-k8s-io-v1beta2-KubeSchedulerConfiguration)


KubeSchedulerProfile is a scheduling profile.

<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
<tbody>
    

  
<tr><td><code>schedulerName</code> <B>[Required]</B><br/>
<code>string</code>
</td>
<td>
   SchedulerName is the name of the scheduler associated to this profile.
If SchedulerName matches with the pod's "spec.schedulerName", then the pod
is scheduled with this profile.</td>
</tr>
    
  
<tr><td><code>plugins</code> <B>[Required]</B><br/>
<a href="#kubescheduler-config-k8s-io-v1beta2-Plugins"><code>Plugins</code></a>
</td>
<td>
   Plugins specify the set of plugins that should be enabled or disabled.
Enabled plugins are the ones that should be enabled in addition to the
default plugins. Disabled plugins are any of the default plugins that
should be disabled.
When no enabled or disabled plugin is specified for an extension point,
default plugins for that extension point will be used if there is any.
If a QueueSort plugin is specified, the same QueueSort Plugin and
PluginConfig must be specified for all profiles.</td>
</tr>
    
  
<tr><td><code>pluginConfig</code> <B>[Required]</B><br/>
<a href="#kubescheduler-config-k8s-io-v1beta2-PluginConfig"><code>[]PluginConfig</code></a>
</td>
<td>
   PluginConfig is an optional set of custom plugin arguments for each plugin.
Omitting config args for a plugin is equivalent to using the default config
for that plugin.</td>
</tr>
    
  
</tbody>
</table>
    


## `Plugin`     {#kubescheduler-config-k8s-io-v1beta2-Plugin}
    



**Appears in:**

- [PluginSet](#kubescheduler-config-k8s-io-v1beta2-PluginSet)


Plugin specifies a plugin name and its weight when applicable. Weight is used only for Score plugins.

<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
<tbody>
    

  
<tr><td><code>name</code> <B>[Required]</B><br/>
<code>string</code>
</td>
<td>
   Name defines the name of plugin</td>
</tr>
    
  
<tr><td><code>weight</code> <B>[Required]</B><br/>
<code>int32</code>
</td>
<td>
   Weight defines the weight of plugin, only used for Score plugins.</td>
</tr>
    
  
</tbody>
</table>
    


## `PluginConfig`     {#kubescheduler-config-k8s-io-v1beta2-PluginConfig}
    



**Appears in:**

- [KubeSchedulerProfile](#kubescheduler-config-k8s-io-v1beta2-KubeSchedulerProfile)


PluginConfig specifies arguments that should be passed to a plugin at the time of initialization.
A plugin that is invoked at multiple extension points is initialized once. Args can have arbitrary structure.
It is up to the plugin to process these Args.

<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
<tbody>
    

  
<tr><td><code>name</code> <B>[Required]</B><br/>
<code>string</code>
</td>
<td>
   Name defines the name of plugin being configured</td>
</tr>
    
  
<tr><td><code>args</code> <B>[Required]</B><br/>
<a href="https://godoc.org/k8s.io/apimachinery/pkg/runtime/#RawExtension"><code>k8s.io/apimachinery/pkg/runtime.RawExtension</code></a>
</td>
<td>
   Args defines the arguments passed to the plugins at the time of initialization. Args can have arbitrary structure.</td>
</tr>
    
  
</tbody>
</table>
    


## `PluginSet`     {#kubescheduler-config-k8s-io-v1beta2-PluginSet}
    



**Appears in:**

- [Plugins](#kubescheduler-config-k8s-io-v1beta2-Plugins)


PluginSet specifies enabled and disabled plugins for an extension point.
If an array is empty, missing, or nil, default plugins at that extension point will be used.

<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
<tbody>
    

  
<tr><td><code>enabled</code> <B>[Required]</B><br/>
<a href="#kubescheduler-config-k8s-io-v1beta2-Plugin"><code>[]Plugin</code></a>
</td>
<td>
   Enabled specifies plugins that should be enabled in addition to default plugins.
These are called after default plugins and in the same order specified here.</td>
</tr>
    
  
<tr><td><code>disabled</code> <B>[Required]</B><br/>
<a href="#kubescheduler-config-k8s-io-v1beta2-Plugin"><code>[]Plugin</code></a>
</td>
<td>
   Disabled specifies default plugins that should be disabled.
When all default plugins need to be disabled, an array containing only one "&lowast;" should be provided.</td>
</tr>
    
  
</tbody>
</table>
    


## `Plugins`     {#kubescheduler-config-k8s-io-v1beta2-Plugins}
    



**Appears in:**

- [KubeSchedulerProfile](#kubescheduler-config-k8s-io-v1beta2-KubeSchedulerProfile)


Plugins include multiple extension points. When specified, the list of plugins for
a particular extension point are the only ones enabled. If an extension point is
omitted from the config, then the default set of plugins is used for that extension point.
Enabled plugins are called in the order specified here, after default plugins. If they need to
be invoked before default plugins, default plugins must be disabled and re-enabled here in desired order.

<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
<tbody>
    

  
<tr><td><code>queueSort</code> <B>[Required]</B><br/>
<a href="#kubescheduler-config-k8s-io-v1beta2-PluginSet"><code>PluginSet</code></a>
</td>
<td>
   QueueSort is a list of plugins that should be invoked when sorting pods in the scheduling queue.</td>
</tr>
    
  
<tr><td><code>preFilter</code> <B>[Required]</B><br/>
<a href="#kubescheduler-config-k8s-io-v1beta2-PluginSet"><code>PluginSet</code></a>
</td>
<td>
   PreFilter is a list of plugins that should be invoked at "PreFilter" extension point of the scheduling framework.</td>
</tr>
    
  
<tr><td><code>filter</code> <B>[Required]</B><br/>
<a href="#kubescheduler-config-k8s-io-v1beta2-PluginSet"><code>PluginSet</code></a>
</td>
<td>
   Filter is a list of plugins that should be invoked when filtering out nodes that cannot run the Pod.</td>
</tr>
    
  
<tr><td><code>postFilter</code> <B>[Required]</B><br/>
<a href="#kubescheduler-config-k8s-io-v1beta2-PluginSet"><code>PluginSet</code></a>
</td>
<td>
   PostFilter is a list of plugins that are invoked after filtering phase, no matter whether filtering succeeds or not.</td>
</tr>
    
  
<tr><td><code>preScore</code> <B>[Required]</B><br/>
<a href="#kubescheduler-config-k8s-io-v1beta2-PluginSet"><code>PluginSet</code></a>
</td>
<td>
   PreScore is a list of plugins that are invoked before scoring.</td>
</tr>
    
  
<tr><td><code>score</code> <B>[Required]</B><br/>
<a href="#kubescheduler-config-k8s-io-v1beta2-PluginSet"><code>PluginSet</code></a>
</td>
<td>
   Score is a list of plugins that should be invoked when ranking nodes that have passed the filtering phase.</td>
</tr>
    
  
<tr><td><code>reserve</code> <B>[Required]</B><br/>
<a href="#kubescheduler-config-k8s-io-v1beta2-PluginSet"><code>PluginSet</code></a>
</td>
<td>
   Reserve is a list of plugins invoked when reserving/unreserving resources
after a node is assigned to run the pod.</td>
</tr>
    
  
<tr><td><code>permit</code> <B>[Required]</B><br/>
<a href="#kubescheduler-config-k8s-io-v1beta2-PluginSet"><code>PluginSet</code></a>
</td>
<td>
   Permit is a list of plugins that control binding of a Pod. These plugins can prevent or delay binding of a Pod.</td>
</tr>
    
  
<tr><td><code>preBind</code> <B>[Required]</B><br/>
<a href="#kubescheduler-config-k8s-io-v1beta2-PluginSet"><code>PluginSet</code></a>
</td>
<td>
   PreBind is a list of plugins that should be invoked before a pod is bound.</td>
</tr>
    
  
<tr><td><code>bind</code> <B>[Required]</B><br/>
<a href="#kubescheduler-config-k8s-io-v1beta2-PluginSet"><code>PluginSet</code></a>
</td>
<td>
   Bind is a list of plugins that should be invoked at "Bind" extension point of the scheduling framework.
The scheduler call these plugins in order. Scheduler skips the rest of these plugins as soon as one returns success.</td>
</tr>
    
  
<tr><td><code>postBind</code> <B>[Required]</B><br/>
<a href="#kubescheduler-config-k8s-io-v1beta2-PluginSet"><code>PluginSet</code></a>
</td>
<td>
   PostBind is a list of plugins that should be invoked after a pod is successfully bound.</td>
</tr>
    
  
</tbody>
</table>
    


## `PodTopologySpreadConstraintsDefaulting`     {#kubescheduler-config-k8s-io-v1beta2-PodTopologySpreadConstraintsDefaulting}
    
(Alias of `string`)


**Appears in:**

- [PodTopologySpreadArgs](#kubescheduler-config-k8s-io-v1beta2-PodTopologySpreadArgs)


PodTopologySpreadConstraintsDefaulting defines how to set default constraints
for the PodTopologySpread plugin.


    


## `ResourceSpec`     {#kubescheduler-config-k8s-io-v1beta2-ResourceSpec}
    



**Appears in:**

- [NodeResourcesLeastAllocatedArgs](#kubescheduler-config-k8s-io-v1beta2-NodeResourcesLeastAllocatedArgs)

- [NodeResourcesMostAllocatedArgs](#kubescheduler-config-k8s-io-v1beta2-NodeResourcesMostAllocatedArgs)

- [RequestedToCapacityRatioArgs](#kubescheduler-config-k8s-io-v1beta2-RequestedToCapacityRatioArgs)


ResourceSpec represents single resource and weight for bin packing of priority RequestedToCapacityRatioArguments.

<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
<tbody>
    

  
<tr><td><code>name</code> <B>[Required]</B><br/>
<code>string</code>
</td>
<td>
   Name of the resource to be managed by RequestedToCapacityRatio function.</td>
</tr>
    
  
<tr><td><code>weight</code> <B>[Required]</B><br/>
<code>int64</code>
</td>
<td>
   Weight of the resource.</td>
</tr>
    
  
</tbody>
</table>
    


## `UtilizationShapePoint`     {#kubescheduler-config-k8s-io-v1beta2-UtilizationShapePoint}
    



**Appears in:**

- [RequestedToCapacityRatioArgs](#kubescheduler-config-k8s-io-v1beta2-RequestedToCapacityRatioArgs)


UtilizationShapePoint represents single point of priority function shape.

<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
<tbody>
    

  
<tr><td><code>utilization</code> <B>[Required]</B><br/>
<code>int32</code>
</td>
<td>
   Utilization (x axis). Valid values are 0 to 100. Fully utilized node maps to 100.</td>
</tr>
    
  
<tr><td><code>score</code> <B>[Required]</B><br/>
<code>int32</code>
</td>
<td>
   Score assigned to given utilization (y axis). Valid values are 0 to 10.</td>
</tr>
    
  
</tbody>
</table>
    
  
  
    


## `Policy`     {#kubescheduler-config-k8s-io-v1-Policy}
    




Policy describes a struct for a policy resource used in api.

<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
<tbody>
    
<tr><td><code>apiVersion</code><br/>string</td><td><code>kubescheduler.config.k8s.io/v1</code></td></tr>
<tr><td><code>kind</code><br/>string</td><td><code>Policy</code></td></tr>
    

  
  
<tr><td><code>predicates</code> <B>[Required]</B><br/>
<a href="#kubescheduler-config-k8s-io-v1-PredicatePolicy"><code>[]PredicatePolicy</code></a>
</td>
<td>
   Holds the information to configure the fit predicate functions</td>
</tr>
    
  
<tr><td><code>priorities</code> <B>[Required]</B><br/>
<a href="#kubescheduler-config-k8s-io-v1-PriorityPolicy"><code>[]PriorityPolicy</code></a>
</td>
<td>
   Holds the information to configure the priority functions</td>
</tr>
    
  
<tr><td><code>extenders</code> <B>[Required]</B><br/>
<a href="#kubescheduler-config-k8s-io-v1-LegacyExtender"><code>[]LegacyExtender</code></a>
</td>
<td>
   Holds the information to communicate with the extender(s)</td>
</tr>
    
  
<tr><td><code>hardPodAffinitySymmetricWeight</code> <B>[Required]</B><br/>
<code>int32</code>
</td>
<td>
   RequiredDuringScheduling affinity is not symmetric, but there is an implicit PreferredDuringScheduling affinity rule
corresponding to every RequiredDuringScheduling affinity rule.
HardPodAffinitySymmetricWeight represents the weight of implicit PreferredDuringScheduling affinity rule, in the range 1-100.</td>
</tr>
    
  
<tr><td><code>alwaysCheckAllPredicates</code> <B>[Required]</B><br/>
<code>bool</code>
</td>
<td>
   When AlwaysCheckAllPredicates is set to true, scheduler checks all
the configured predicates even after one or more of them fails.
When the flag is set to false, scheduler skips checking the rest
of the predicates after it finds one predicate that failed.</td>
</tr>
    
  
</tbody>
</table>
    


## `ExtenderManagedResource`     {#kubescheduler-config-k8s-io-v1-ExtenderManagedResource}
    



**Appears in:**

- [Extender](#kubescheduler-config-k8s-io-v1beta2-Extender)

- [LegacyExtender](#kubescheduler-config-k8s-io-v1-LegacyExtender)


ExtenderManagedResource describes the arguments of extended resources
managed by an extender.

<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
<tbody>
    

  
<tr><td><code>name</code> <B>[Required]</B><br/>
<code>string</code>
</td>
<td>
   Name is the extended resource name.</td>
</tr>
    
  
<tr><td><code>ignoredByScheduler</code> <B>[Required]</B><br/>
<code>bool</code>
</td>
<td>
   IgnoredByScheduler indicates whether kube-scheduler should ignore this
resource when applying predicates.</td>
</tr>
    
  
</tbody>
</table>
    


## `ExtenderTLSConfig`     {#kubescheduler-config-k8s-io-v1-ExtenderTLSConfig}
    



**Appears in:**

- [Extender](#kubescheduler-config-k8s-io-v1beta2-Extender)

- [LegacyExtender](#kubescheduler-config-k8s-io-v1-LegacyExtender)


ExtenderTLSConfig contains settings to enable TLS with extender

<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
<tbody>
    

  
<tr><td><code>insecure</code> <B>[Required]</B><br/>
<code>bool</code>
</td>
<td>
   Server should be accessed without verifying the TLS certificate. For testing only.</td>
</tr>
    
  
<tr><td><code>serverName</code> <B>[Required]</B><br/>
<code>string</code>
</td>
<td>
   ServerName is passed to the server for SNI and is used in the client to check server
certificates against. If ServerName is empty, the hostname used to contact the
server is used.</td>
</tr>
    
  
<tr><td><code>certFile</code> <B>[Required]</B><br/>
<code>string</code>
</td>
<td>
   Server requires TLS client certificate authentication</td>
</tr>
    
  
<tr><td><code>keyFile</code> <B>[Required]</B><br/>
<code>string</code>
</td>
<td>
   Server requires TLS client certificate authentication</td>
</tr>
    
  
<tr><td><code>caFile</code> <B>[Required]</B><br/>
<code>string</code>
</td>
<td>
   Trusted root certificates for server</td>
</tr>
    
  
<tr><td><code>certData</code> <B>[Required]</B><br/>
<code>[]byte</code>
</td>
<td>
   CertData holds PEM-encoded bytes (typically read from a client certificate file).
CertData takes precedence over CertFile</td>
</tr>
    
  
<tr><td><code>keyData</code> <B>[Required]</B><br/>
<code>[]byte</code>
</td>
<td>
   KeyData holds PEM-encoded bytes (typically read from a client certificate key file).
KeyData takes precedence over KeyFile</td>
</tr>
    
  
<tr><td><code>caData</code> <B>[Required]</B><br/>
<code>[]byte</code>
</td>
<td>
   CAData holds PEM-encoded bytes (typically read from a root certificates bundle).
CAData takes precedence over CAFile</td>
</tr>
    
  
</tbody>
</table>
    


## `LabelPreference`     {#kubescheduler-config-k8s-io-v1-LabelPreference}
    



**Appears in:**

- [PriorityArgument](#kubescheduler-config-k8s-io-v1-PriorityArgument)


LabelPreference holds the parameters that are used to configure the corresponding priority function

<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
<tbody>
    

  
<tr><td><code>label</code> <B>[Required]</B><br/>
<code>string</code>
</td>
<td>
   Used to identify node "groups"</td>
</tr>
    
  
<tr><td><code>presence</code> <B>[Required]</B><br/>
<code>bool</code>
</td>
<td>
   This is a boolean flag
If true, higher priority is given to nodes that have the label
If false, higher priority is given to nodes that do not have the label</td>
</tr>
    
  
</tbody>
</table>
    


## `LabelsPresence`     {#kubescheduler-config-k8s-io-v1-LabelsPresence}
    



**Appears in:**

- [PredicateArgument](#kubescheduler-config-k8s-io-v1-PredicateArgument)


LabelsPresence holds the parameters that are used to configure the corresponding predicate in scheduler policy configuration.

<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
<tbody>
    

  
<tr><td><code>labels</code> <B>[Required]</B><br/>
<code>[]string</code>
</td>
<td>
   The list of labels that identify node "groups"
All of the labels should be either present (or absent) for the node to be considered a fit for hosting the pod</td>
</tr>
    
  
<tr><td><code>presence</code> <B>[Required]</B><br/>
<code>bool</code>
</td>
<td>
   The boolean flag that indicates whether the labels should be present or absent from the node</td>
</tr>
    
  
</tbody>
</table>
    


## `LegacyExtender`     {#kubescheduler-config-k8s-io-v1-LegacyExtender}
    



**Appears in:**

- [Policy](#kubescheduler-config-k8s-io-v1-Policy)


LegacyExtender holds the parameters used to communicate with the extender. If a verb is unspecified/empty,
it is assumed that the extender chose not to provide that extension.

<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
<tbody>
    

  
<tr><td><code>urlPrefix</code> <B>[Required]</B><br/>
<code>string</code>
</td>
<td>
   URLPrefix at which the extender is available</td>
</tr>
    
  
<tr><td><code>filterVerb</code> <B>[Required]</B><br/>
<code>string</code>
</td>
<td>
   Verb for the filter call, empty if not supported. This verb is appended to the URLPrefix when issuing the filter call to extender.</td>
</tr>
    
  
<tr><td><code>preemptVerb</code> <B>[Required]</B><br/>
<code>string</code>
</td>
<td>
   Verb for the preempt call, empty if not supported. This verb is appended to the URLPrefix when issuing the preempt call to extender.</td>
</tr>
    
  
<tr><td><code>prioritizeVerb</code> <B>[Required]</B><br/>
<code>string</code>
</td>
<td>
   Verb for the prioritize call, empty if not supported. This verb is appended to the URLPrefix when issuing the prioritize call to extender.</td>
</tr>
    
  
<tr><td><code>weight</code> <B>[Required]</B><br/>
<code>int64</code>
</td>
<td>
   The numeric multiplier for the node scores that the prioritize call generates.
The weight should be a positive integer</td>
</tr>
    
  
<tr><td><code>bindVerb</code> <B>[Required]</B><br/>
<code>string</code>
</td>
<td>
   Verb for the bind call, empty if not supported. This verb is appended to the URLPrefix when issuing the bind call to extender.
If this method is implemented by the extender, it is the extender's responsibility to bind the pod to apiserver. Only one extender
can implement this function.</td>
</tr>
    
  
<tr><td><code>enableHttps</code> <B>[Required]</B><br/>
<code>bool</code>
</td>
<td>
   EnableHTTPS specifies whether https should be used to communicate with the extender</td>
</tr>
    
  
<tr><td><code>tlsConfig</code> <B>[Required]</B><br/>
<a href="#kubescheduler-config-k8s-io-v1-ExtenderTLSConfig"><code>ExtenderTLSConfig</code></a>
</td>
<td>
   TLSConfig specifies the transport layer security config</td>
</tr>
    
  
<tr><td><code>httpTimeout</code> <B>[Required]</B><br/>
<a href="https://godoc.org/time#Duration"><code>time.Duration</code></a>
</td>
<td>
   HTTPTimeout specifies the timeout duration for a call to the extender. Filter timeout fails the scheduling of the pod. Prioritize
timeout is ignored, k8s/other extenders priorities are used to select the node.</td>
</tr>
    
  
<tr><td><code>nodeCacheCapable</code> <B>[Required]</B><br/>
<code>bool</code>
</td>
<td>
   NodeCacheCapable specifies that the extender is capable of caching node information,
so the scheduler should only send minimal information about the eligible nodes
assuming that the extender already cached full details of all nodes in the cluster</td>
</tr>
    
  
<tr><td><code>managedResources</code><br/>
<a href="#kubescheduler-config-k8s-io-v1-ExtenderManagedResource"><code>[]ExtenderManagedResource</code></a>
</td>
<td>
   ManagedResources is a list of extended resources that are managed by
this extender.
- A pod will be sent to the extender on the Filter, Prioritize and Bind
  (if the extender is the binder) phases iff the pod requests at least
  one of the extended resources in this list. If empty or unspecified,
  all pods will be sent to this extender.
- If IgnoredByScheduler is set to true for a resource, kube-scheduler
  will skip checking the resource in predicates.</td>
</tr>
    
  
<tr><td><code>ignorable</code> <B>[Required]</B><br/>
<code>bool</code>
</td>
<td>
   Ignorable specifies if the extender is ignorable, i.e. scheduling should not
fail when the extender returns an error or is not reachable.</td>
</tr>
    
  
</tbody>
</table>
    


## `PredicateArgument`     {#kubescheduler-config-k8s-io-v1-PredicateArgument}
    



**Appears in:**

- [PredicatePolicy](#kubescheduler-config-k8s-io-v1-PredicatePolicy)


PredicateArgument represents the arguments to configure predicate functions in scheduler policy configuration.
Only one of its members may be specified

<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
<tbody>
    

  
<tr><td><code>serviceAffinity</code> <B>[Required]</B><br/>
<a href="#kubescheduler-config-k8s-io-v1-ServiceAffinity"><code>ServiceAffinity</code></a>
</td>
<td>
   The predicate that provides affinity for pods belonging to a service
It uses a label to identify nodes that belong to the same "group"</td>
</tr>
    
  
<tr><td><code>labelsPresence</code> <B>[Required]</B><br/>
<a href="#kubescheduler-config-k8s-io-v1-LabelsPresence"><code>LabelsPresence</code></a>
</td>
<td>
   The predicate that checks whether a particular node has a certain label
defined or not, regardless of value</td>
</tr>
    
  
</tbody>
</table>
    


## `PredicatePolicy`     {#kubescheduler-config-k8s-io-v1-PredicatePolicy}
    



**Appears in:**

- [Policy](#kubescheduler-config-k8s-io-v1-Policy)


PredicatePolicy describes a struct of a predicate policy.

<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
<tbody>
    

  
<tr><td><code>name</code> <B>[Required]</B><br/>
<code>string</code>
</td>
<td>
   Identifier of the predicate policy
For a custom predicate, the name can be user-defined
For the Kubernetes provided predicates, the name is the identifier of the pre-defined predicate</td>
</tr>
    
  
<tr><td><code>argument</code> <B>[Required]</B><br/>
<a href="#kubescheduler-config-k8s-io-v1-PredicateArgument"><code>PredicateArgument</code></a>
</td>
<td>
   Holds the parameters to configure the given predicate</td>
</tr>
    
  
</tbody>
</table>
    


## `PriorityArgument`     {#kubescheduler-config-k8s-io-v1-PriorityArgument}
    



**Appears in:**

- [PriorityPolicy](#kubescheduler-config-k8s-io-v1-PriorityPolicy)


PriorityArgument represents the arguments to configure priority functions in scheduler policy configuration.
Only one of its members may be specified

<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
<tbody>
    

  
<tr><td><code>serviceAntiAffinity</code> <B>[Required]</B><br/>
<a href="#kubescheduler-config-k8s-io-v1-ServiceAntiAffinity"><code>ServiceAntiAffinity</code></a>
</td>
<td>
   The priority function that ensures a good spread (anti-affinity) for pods belonging to a service
It uses a label to identify nodes that belong to the same "group"</td>
</tr>
    
  
<tr><td><code>labelPreference</code> <B>[Required]</B><br/>
<a href="#kubescheduler-config-k8s-io-v1-LabelPreference"><code>LabelPreference</code></a>
</td>
<td>
   The priority function that checks whether a particular node has a certain label
defined or not, regardless of value</td>
</tr>
    
  
<tr><td><code>requestedToCapacityRatioArguments</code> <B>[Required]</B><br/>
<a href="#kubescheduler-config-k8s-io-v1-RequestedToCapacityRatioArguments"><code>RequestedToCapacityRatioArguments</code></a>
</td>
<td>
   The RequestedToCapacityRatio priority function is parametrized with function shape.</td>
</tr>
    
  
</tbody>
</table>
    


## `PriorityPolicy`     {#kubescheduler-config-k8s-io-v1-PriorityPolicy}
    



**Appears in:**

- [Policy](#kubescheduler-config-k8s-io-v1-Policy)


PriorityPolicy describes a struct of a priority policy.

<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
<tbody>
    

  
<tr><td><code>name</code> <B>[Required]</B><br/>
<code>string</code>
</td>
<td>
   Identifier of the priority policy
For a custom priority, the name can be user-defined
For the Kubernetes provided priority functions, the name is the identifier of the pre-defined priority function</td>
</tr>
    
  
<tr><td><code>weight</code> <B>[Required]</B><br/>
<code>int64</code>
</td>
<td>
   The numeric multiplier for the node scores that the priority function generates
The weight should be non-zero and can be a positive or a negative integer</td>
</tr>
    
  
<tr><td><code>argument</code> <B>[Required]</B><br/>
<a href="#kubescheduler-config-k8s-io-v1-PriorityArgument"><code>PriorityArgument</code></a>
</td>
<td>
   Holds the parameters to configure the given priority function</td>
</tr>
    
  
</tbody>
</table>
    


## `RequestedToCapacityRatioArguments`     {#kubescheduler-config-k8s-io-v1-RequestedToCapacityRatioArguments}
    



**Appears in:**

- [PriorityArgument](#kubescheduler-config-k8s-io-v1-PriorityArgument)


RequestedToCapacityRatioArguments holds arguments specific to RequestedToCapacityRatio priority function.

<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
<tbody>
    

  
<tr><td><code>shape</code> <B>[Required]</B><br/>
<a href="#kubescheduler-config-k8s-io-v1-UtilizationShapePoint"><code>[]UtilizationShapePoint</code></a>
</td>
<td>
   Array of point defining priority function shape.</td>
</tr>
    
  
<tr><td><code>resources</code> <B>[Required]</B><br/>
<a href="#kubescheduler-config-k8s-io-v1-ResourceSpec"><code>[]ResourceSpec</code></a>
</td>
<td>
   <span class="text-muted">No description provided.</span>
   </td>
</tr>
    
  
</tbody>
</table>
    


## `ResourceSpec`     {#kubescheduler-config-k8s-io-v1-ResourceSpec}
    



**Appears in:**

- [RequestedToCapacityRatioArguments](#kubescheduler-config-k8s-io-v1-RequestedToCapacityRatioArguments)


ResourceSpec represents single resource and weight for bin packing of priority RequestedToCapacityRatioArguments.

<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
<tbody>
    

  
<tr><td><code>name</code> <B>[Required]</B><br/>
<code>string</code>
</td>
<td>
   Name of the resource to be managed by RequestedToCapacityRatio function.</td>
</tr>
    
  
<tr><td><code>weight</code> <B>[Required]</B><br/>
<code>int64</code>
</td>
<td>
   Weight of the resource.</td>
</tr>
    
  
</tbody>
</table>
    


## `ServiceAffinity`     {#kubescheduler-config-k8s-io-v1-ServiceAffinity}
    



**Appears in:**

- [PredicateArgument](#kubescheduler-config-k8s-io-v1-PredicateArgument)


ServiceAffinity holds the parameters that are used to configure the corresponding predicate in scheduler policy configuration.

<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
<tbody>
    

  
<tr><td><code>labels</code> <B>[Required]</B><br/>
<code>[]string</code>
</td>
<td>
   The list of labels that identify node "groups"
All of the labels should match for the node to be considered a fit for hosting the pod</td>
</tr>
    
  
</tbody>
</table>
    


## `ServiceAntiAffinity`     {#kubescheduler-config-k8s-io-v1-ServiceAntiAffinity}
    



**Appears in:**

- [PriorityArgument](#kubescheduler-config-k8s-io-v1-PriorityArgument)


ServiceAntiAffinity holds the parameters that are used to configure the corresponding priority function

<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
<tbody>
    

  
<tr><td><code>label</code> <B>[Required]</B><br/>
<code>string</code>
</td>
<td>
   Used to identify node "groups"</td>
</tr>
    
  
</tbody>
</table>
    


## `UtilizationShapePoint`     {#kubescheduler-config-k8s-io-v1-UtilizationShapePoint}
    



**Appears in:**

- [RequestedToCapacityRatioArguments](#kubescheduler-config-k8s-io-v1-RequestedToCapacityRatioArguments)


UtilizationShapePoint represents single point of priority function shape.

<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
<tbody>
    

  
<tr><td><code>utilization</code> <B>[Required]</B><br/>
<code>int32</code>
</td>
<td>
   Utilization (x axis). Valid values are 0 to 100. Fully utilized node maps to 100.</td>
</tr>
    
  
<tr><td><code>score</code> <B>[Required]</B><br/>
<code>int32</code>
</td>
<td>
   Score assigned to given utilization (y axis). Valid values are 0 to 10.</td>
</tr>
    
  
</tbody>
</table>
    
  
  
    

## `ClientConnectionConfiguration`     {#ClientConnectionConfiguration}
    



**Appears in:**

- [KubeSchedulerConfiguration](#kubescheduler-config-k8s-io-v1beta2-KubeSchedulerConfiguration)


ClientConnectionConfiguration contains details for constructing a client.

<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
<tbody>
    

  
<tr><td><code>kubeconfig</code> <B>[Required]</B><br/>
<code>string</code>
</td>
<td>
   kubeconfig is the path to a KubeConfig file.</td>
</tr>
    
  
<tr><td><code>acceptContentTypes</code> <B>[Required]</B><br/>
<code>string</code>
</td>
<td>
   acceptContentTypes defines the Accept header sent by clients when connecting to a server, overriding the
default value of 'application/json'. This field will control all connections to the server used by a particular
client.</td>
</tr>
    
  
<tr><td><code>contentType</code> <B>[Required]</B><br/>
<code>string</code>
</td>
<td>
   contentType is the content type used when sending data to the server from this client.</td>
</tr>
    
  
<tr><td><code>qps</code> <B>[Required]</B><br/>
<code>float32</code>
</td>
<td>
   qps controls the number of queries per second allowed for this connection.</td>
</tr>
    
  
<tr><td><code>burst</code> <B>[Required]</B><br/>
<code>int32</code>
</td>
<td>
   burst allows extra queries to accumulate when a client is exceeding its rate.</td>
</tr>
    
  
</tbody>
</table>

## `DebuggingConfiguration`     {#DebuggingConfiguration}
    



**Appears in:**

- [KubeSchedulerConfiguration](#kubescheduler-config-k8s-io-v1beta2-KubeSchedulerConfiguration)


DebuggingConfiguration holds configuration for Debugging related features.

<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
<tbody>
    

  
<tr><td><code>enableProfiling</code> <B>[Required]</B><br/>
<code>bool</code>
</td>
<td>
   enableProfiling enables profiling via web interface host:port/debug/pprof/</td>
</tr>
    
  
<tr><td><code>enableContentionProfiling</code> <B>[Required]</B><br/>
<code>bool</code>
</td>
<td>
   enableContentionProfiling enables lock contention profiling, if
enableProfiling is true.</td>
</tr>
    
  
</tbody>
</table>

## `LeaderElectionConfiguration`     {#LeaderElectionConfiguration}
    



**Appears in:**

- [KubeSchedulerConfiguration](#kubescheduler-config-k8s-io-v1beta2-KubeSchedulerConfiguration)


LeaderElectionConfiguration defines the configuration of leader election
clients for components that can run with leader election enabled.

<table class="table">
<thead><tr><th width="30%">Field</th><th>Description</th></tr></thead>
<tbody>
    

  
<tr><td><code>leaderElect</code> <B>[Required]</B><br/>
<code>bool</code>
</td>
<td>
   leaderElect enables a leader election client to gain leadership
before executing the main loop. Enable this when running replicated
components for high availability.</td>
</tr>
    
  
<tr><td><code>leaseDuration</code> <B>[Required]</B><br/>
<a href="https://godoc.org/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
</td>
<td>
   leaseDuration is the duration that non-leader candidates will wait
after observing a leadership renewal until attempting to acquire
leadership of a led but unrenewed leader slot. This is effectively the
maximum duration that a leader can be stopped before it is replaced
by another candidate. This is only applicable if leader election is
enabled.</td>
</tr>
    
  
<tr><td><code>renewDeadline</code> <B>[Required]</B><br/>
<a href="https://godoc.org/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
</td>
<td>
   renewDeadline is the interval between attempts by the acting master to
renew a leadership slot before it stops leading. This must be less
than or equal to the lease duration. This is only applicable if leader
election is enabled.</td>
</tr>
    
  
<tr><td><code>retryPeriod</code> <B>[Required]</B><br/>
<a href="https://godoc.org/k8s.io/apimachinery/pkg/apis/meta/v1#Duration"><code>meta/v1.Duration</code></a>
</td>
<td>
   retryPeriod is the duration the clients should wait between attempting
acquisition and renewal of a leadership. This is only applicable if
leader election is enabled.</td>
</tr>
    
  
<tr><td><code>resourceLock</code> <B>[Required]</B><br/>
<code>string</code>
</td>
<td>
   resourceLock indicates the resource object type that will be used to lock
during leader election cycles.</td>
</tr>
    
  
<tr><td><code>resourceName</code> <B>[Required]</B><br/>
<code>string</code>
</td>
<td>
   resourceName indicates the name of resource object that will be used to lock
during leader election cycles.</td>
</tr>
    
  
<tr><td><code>resourceNamespace</code> <B>[Required]</B><br/>
<code>string</code>
</td>
<td>
   resourceName indicates the namespace of resource object that will be used to lock
during leader election cycles.</td>
</tr>
    
  
</tbody>
</table>
