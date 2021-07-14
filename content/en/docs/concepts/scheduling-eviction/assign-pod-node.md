---
reviewers:
- davidopp
- kevin-wangzefeng
- bsalamat
title: Assigning Pods to Nodes
content_type: concept
weight: 20
---


<!-- overview -->

You can constrain a {{< glossary_tooltip text="Pod" term_id="pod" >}} so that it can only run on particular set of
{{< glossary_tooltip text="Node(s)" term_id="node" >}}.
There are several ways to do this and the recommended approaches all use
[label selectors](/docs/concepts/overview/working-with-objects/labels/) to facilitate the selection.
Generally such constraints are unnecessary, as the scheduler will automatically do a reasonable placement
(e.g. spread your pods across nodes so as not place the pod on a node with insufficient free resources, etc.)
but there are some circumstances where you may want to control which node the pod deploys to - for example to ensure
that a pod ends up on a machine with an SSD attached to it, or to co-locate pods from two different
services that communicate a lot into the same availability zone.


<!-- body -->

## nodeSelector

`nodeSelector` is the simplest recommended form of node selection constraint.
`nodeSelector` is a field of PodSpec. It specifies a map of key-value pairs. For the pod to be eligible
to run on a node, the node must have each of the indicated key-value pairs as labels (it can have
additional labels as well). The most common usage is one key-value pair.

Let's walk through an example of how to use `nodeSelector`.

### Step Zero: Prerequisites

This example assumes that you have a basic understanding of Kubernetes pods and that you have [set up a Kubernetes cluster](/docs/setup/).

### Step One: Attach label to the node

Run `kubectl get nodes` to get the names of your cluster's nodes. Pick out the one that you want to add a label to, and then run `kubectl label nodes <node-name> <label-key>=<label-value>` to add a label to the node you've chosen. For example, if my node name is 'kubernetes-foo-node-1.c.a-robinson.internal' and my desired label is 'disktype=ssd', then I can run `kubectl label nodes kubernetes-foo-node-1.c.a-robinson.internal disktype=ssd`.

You can verify that it worked by re-running `kubectl get nodes --show-labels` and checking that the node now has a label. You can also use `kubectl describe node "nodename"` to see the full list of labels of the given node.

### Step Two: Add a nodeSelector field to your pod configuration

Take whatever pod config file you want to run, and add a nodeSelector section to it, like this. For example, if this is my pod config:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
  labels:
    env: test
spec:
  containers:
  - name: nginx
    image: nginx
```

Then add a nodeSelector like so:

{{< codenew file="pods/pod-nginx.yaml" >}}

When you then run `kubectl apply -f https://k8s.io/examples/pods/pod-nginx.yaml`,
the Pod will get scheduled on the node that you attached the label to. You can
verify that it worked by running `kubectl get pods -o wide` and looking at the
"NODE" that the Pod was assigned to.

## Interlude: built-in node labels {#built-in-node-labels}

In addition to labels you [attach](#step-one-attach-label-to-the-node), nodes come pre-populated
with a standard set of labels. See [Well-Known Labels, Annotations and Taints](/docs/reference/labels-annotations-taints/) for a list of these.

{{< note >}}
The value of these labels is cloud provider specific and is not guaranteed to be reliable.
For example, the value of `kubernetes.io/hostname` may be the same as the Node name in some environments
and a different value in other environments.
{{< /note >}}

## Node isolation/restriction

Adding labels to Node objects allows targeting pods to specific nodes or groups of nodes.
This can be used to ensure specific pods only run on nodes with certain isolation, security, or regulatory properties.
When using labels for this purpose, choosing label keys that cannot be modified by the kubelet process on the node is strongly recommended.
This prevents a compromised node from using its kubelet credential to set those labels on its own Node object,
and influencing the scheduler to schedule workloads to the compromised node.

The `NodeRestriction` admission plugin prevents kubelets from setting or modifying labels with a `node-restriction.kubernetes.io/` prefix.
To make use of that label prefix for node isolation:

1. Ensure you are using the [Node authorizer](/docs/reference/access-authn-authz/node/) and have _enabled_ the [NodeRestriction admission plugin](/docs/reference/access-authn-authz/admission-controllers/#noderestriction).
2. Add labels under the `node-restriction.kubernetes.io/` prefix to your Node objects, and use those labels in your node selectors.
For example, `example.com.node-restriction.kubernetes.io/fips=true` or `example.com.node-restriction.kubernetes.io/pci-dss=true`.

## Affinity and anti-affinity

`nodeSelector` provides a very simple way to constrain pods to nodes with particular labels. The affinity/anti-affinity
feature, greatly expands the types of constraints you can express. The key enhancements are

1. The affinity/anti-affinity language is more expressive. The language offers more matching rules
   besides exact matches created with a logical AND operation;
2. you can indicate that the rule is "soft"/"preference" rather than a hard requirement, so if the scheduler
   can't satisfy it, the pod will still be scheduled;
3. you can constrain against labels on other pods running on the node (or other topological domain),
   rather than against labels on the node itself, which allows rules about which pods can and cannot be co-located

The affinity feature consists of two types of affinity, "node affinity" and "inter-pod affinity/anti-affinity".
Node affinity is like the existing `nodeSelector` (but with the first two benefits listed above),
while inter-pod affinity/anti-affinity constrains against pod labels rather than node labels, as
described in the third item listed above, in addition to having the first and second properties listed above.

### Node affinity

Node affinity is conceptually similar to `nodeSelector` -- it allows you to constrain which nodes your
pod is eligible to be scheduled on, based on labels on the node.

There are currently two types of node affinity, called `requiredDuringSchedulingIgnoredDuringExecution` and
`preferredDuringSchedulingIgnoredDuringExecution`. You can think of them as "hard" and "soft" respectively,
in the sense that the former specifies rules that *must* be met for a pod to be scheduled onto a node (similar to
`nodeSelector` but using a more expressive syntax), while the latter specifies *preferences* that the scheduler
will try to enforce but will not guarantee. The "IgnoredDuringExecution" part of the names means that, similar
to how `nodeSelector` works, if labels on a node change at runtime such that the affinity rules on a pod are no longer
met, the pod continues to run on the node. In the future we plan to offer
`requiredDuringSchedulingRequiredDuringExecution` which will be identical to `requiredDuringSchedulingIgnoredDuringExecution`
except that it will evict pods from nodes that cease to satisfy the pods' node affinity requirements.

Thus an example of `requiredDuringSchedulingIgnoredDuringExecution` would be "only run the pod on nodes with Intel CPUs"
and an example `preferredDuringSchedulingIgnoredDuringExecution` would be "try to run this set of pods in failure
zone XYZ, but if it's not possible, then allow some to run elsewhere".

Node affinity is specified as field `nodeAffinity` of field `affinity` in the PodSpec.

Here's an example of a pod that uses node affinity:

{{< codenew file="pods/pod-with-node-affinity.yaml" >}}

This node affinity rule says the pod can only be placed on a node with a label whose key is
`kubernetes.io/e2e-az-name` and whose value is either `e2e-az1` or `e2e-az2`. In addition,
among nodes that meet that criteria, nodes with a label whose key is `another-node-label-key` and whose
value is `another-node-label-value` should be preferred.

You can see the operator `In` being used in the example. The new node affinity syntax supports the following operators: `In`, `NotIn`, `Exists`, `DoesNotExist`, `Gt`, `Lt`.
You can use `NotIn` and `DoesNotExist` to achieve node anti-affinity behavior, or use
[node taints](/docs/concepts/scheduling-eviction/taint-and-toleration/) to repel pods from specific nodes.

If you specify both `nodeSelector` and `nodeAffinity`, *both* must be satisfied for the pod
to be scheduled onto a candidate node.

If you specify multiple `nodeSelectorTerms` associated with `nodeAffinity` types, then the pod can be scheduled onto a node **if one of the** `nodeSelectorTerms` can be satisfied.

If you specify multiple `matchExpressions` associated with `nodeSelectorTerms`, then the pod can be scheduled onto a node **only if all** `matchExpressions` is satisfied.

If you remove or change the label of the node where the pod is scheduled, the pod won't be removed. In other words, the affinity selection works only at the time of scheduling the pod.

The `weight` field in `preferredDuringSchedulingIgnoredDuringExecution` is in the range 1-100. For each node that meets all of the scheduling requirements (resource request, RequiredDuringScheduling affinity expressions, etc.), the scheduler will compute a sum by iterating through the elements of this field and adding "weight" to the sum if the node matches the corresponding MatchExpressions. This score is then combined with the scores of other priority functions for the node. The node(s) with the highest total score are the most preferred.

#### Node affinity per scheduling profile

{{< feature-state for_k8s_version="v1.20" state="beta" >}}

When configuring multiple [scheduling profiles](/docs/reference/scheduling/config/#multiple-profiles), you can associate
a profile with a Node affinity, which is useful if a profile only applies to a specific set of Nodes.
To do so, add an `addedAffinity` to the args of the [`NodeAffinity` plugin](/docs/reference/scheduling/config/#scheduling-plugins)
in the [scheduler configuration](/docs/reference/scheduling/config/). For example:

```yaml
apiVersion: kubescheduler.config.k8s.io/v1beta1
kind: KubeSchedulerConfiguration

profiles:
  - schedulerName: default-scheduler
  - schedulerName: foo-scheduler
    pluginConfig:
      - name: NodeAffinity
        args:
          addedAffinity:
            requiredDuringSchedulingIgnoredDuringExecution:
              nodeSelectorTerms:
              - matchExpressions:
                - key: scheduler-profile
                  operator: In
                  values:
                  - foo
```

The `addedAffinity` is applied to all Pods that set `.spec.schedulerName` to `foo-scheduler`, in addition to the
NodeAffinity specified in the PodSpec.
That is, in order to match the Pod, Nodes need to satisfy `addedAffinity` and the Pod's `.spec.NodeAffinity`.

Since the `addedAffinity` is not visible to end users, its behavior might be unexpected to them. We
recommend to use node labels that have clear correlation with the profile's scheduler name.

{{< note >}}
The DaemonSet controller, which [creates Pods for DaemonSets](/docs/concepts/workloads/controllers/daemonset/#scheduled-by-default-scheduler)
is not aware of scheduling profiles. For this reason, it is recommended that you keep a scheduler profile, such as the
`default-scheduler`, without any `addedAffinity`. Then, the Daemonset's Pod template should use this scheduler name.
Otherwise, some Pods created by the Daemonset controller might remain unschedulable.
{{< /note >}}

### Inter-pod affinity and anti-affinity

Inter-pod affinity and anti-affinity allow you to constrain which nodes your pod is eligible to be scheduled *based on
labels on pods that are already running on the node* rather than based on labels on nodes. The rules are of the form
"this pod should (or, in the case of anti-affinity, should not) run in an X if that X is already running one or more pods that meet rule Y".
Y is expressed as a LabelSelector with an optional associated list of namespaces; unlike nodes, because pods are namespaced
(and therefore the labels on pods are implicitly namespaced),
a label selector over pod labels must specify which namespaces the selector should apply to. Conceptually X is a topology domain
like node, rack, cloud provider zone, cloud provider region, etc. You express it using a `topologyKey` which is the
key for the node label that the system uses to denote such a topology domain; for example, see the label keys listed above
in the section [Interlude: built-in node labels](#built-in-node-labels).

{{< note >}}
Inter-pod affinity and anti-affinity require substantial amount of
processing which can slow down scheduling in large clusters significantly. We do
not recommend using them in clusters larger than several hundred nodes.
{{< /note >}}

{{< note >}}
Pod anti-affinity requires nodes to be consistently labelled, in other words every node in the cluster must have an appropriate label matching `topologyKey`. If some or all nodes are missing the specified `topologyKey` label, it can lead to unintended behavior.
{{< /note >}}

As with node affinity, there are currently two types of pod affinity and anti-affinity, called `requiredDuringSchedulingIgnoredDuringExecution` and
`preferredDuringSchedulingIgnoredDuringExecution` which denote "hard" vs. "soft" requirements.
See the description in the node affinity section earlier.
An example of `requiredDuringSchedulingIgnoredDuringExecution` affinity would be "co-locate the pods of service A and service B
in the same zone, since they communicate a lot with each other"
and an example `preferredDuringSchedulingIgnoredDuringExecution` anti-affinity would be "spread the pods from this service across zones"
(a hard requirement wouldn't make sense, since you probably have more pods than zones).

Inter-pod affinity is specified as field `podAffinity` of field `affinity` in the PodSpec.
And inter-pod anti-affinity is specified as field `podAntiAffinity` of field `affinity` in the PodSpec.

#### An example of a pod that uses pod affinity:

{{< codenew file="pods/pod-with-pod-affinity.yaml" >}}

The affinity on this pod defines one pod affinity rule and one pod anti-affinity rule. In this example, the
`podAffinity` is `requiredDuringSchedulingIgnoredDuringExecution`
while the `podAntiAffinity` is `preferredDuringSchedulingIgnoredDuringExecution`. The
pod affinity rule says that the pod can be scheduled onto a node only if that node is in the same zone
as at least one already-running pod that has a label with key "security" and value "S1". (More precisely, the pod is eligible to run
on node N if node N has a label with key `topology.kubernetes.io/zone` and some value V
such that there is at least one node in the cluster with key `topology.kubernetes.io/zone` and
value V that is running a pod that has a label with key "security" and value "S1".) The pod anti-affinity
rule says that the pod should not be scheduled onto a node if that node is in the same zone as a pod with
label having key "security" and value "S2". See the
[design doc](https://git.k8s.io/community/contributors/design-proposals/scheduling/podaffinity.md)
for many more examples of pod affinity and anti-affinity, both the `requiredDuringSchedulingIgnoredDuringExecution`
flavor and the `preferredDuringSchedulingIgnoredDuringExecution` flavor.

The legal operators for pod affinity and anti-affinity are `In`, `NotIn`, `Exists`, `DoesNotExist`.

In principle, the `topologyKey` can be any legal label-key. However,
for performance and security reasons, there are some constraints on topologyKey:

1. For pod affinity, empty `topologyKey` is not allowed in both `requiredDuringSchedulingIgnoredDuringExecution`
and `preferredDuringSchedulingIgnoredDuringExecution`.
2. For pod anti-affinity, empty `topologyKey` is also not allowed in both `requiredDuringSchedulingIgnoredDuringExecution`
and `preferredDuringSchedulingIgnoredDuringExecution`.
3. For `requiredDuringSchedulingIgnoredDuringExecution` pod anti-affinity, the admission controller `LimitPodHardAntiAffinityTopology` was introduced to limit `topologyKey` to `kubernetes.io/hostname`. If you want to make it available for custom topologies, you may modify the admission controller, or disable it.
4. Except for the above cases, the `topologyKey` can be any legal label-key.

In addition to `labelSelector` and `topologyKey`, you can optionally specify a list `namespaces`
of namespaces which the `labelSelector` should match against (this goes at the same level of the definition as `labelSelector` and `topologyKey`).
If omitted or empty, it defaults to the namespace of the pod where the affinity/anti-affinity definition appears.

All `matchExpressions` associated with `requiredDuringSchedulingIgnoredDuringExecution` affinity and anti-affinity
must be satisfied for the pod to be scheduled onto a node.

#### Namespace selector
{{< feature-state for_k8s_version="v1.22" state="beta" >}}

Users can also select matching namespaces using `namespaceSelector`, which is a label query over the set of namespaces.
The affinity term is applied to the union of the namespaces selected by `namespaceSelector` and the ones listed in the `namespaces` field.
Note that an empty `namespaceSelector` ({}) matches all namespaces, while a null or empty `namespaces` list and 
null `namespaceSelector` means "this pod's namespace".

This feature is beta and enabled by default. You can disable it via the
[feature gate](/docs/reference/command-line-tools-reference/feature-gates/)
`PodAffinityNamespaceSelector` in both kube-apiserver and kube-scheduler.

#### More Practical Use-cases

Interpod Affinity and AntiAffinity can be even more useful when they are used with higher
level collections such as ReplicaSets, StatefulSets, Deployments, etc.  One can easily configure that a set of workloads should
be co-located in the same defined topology, eg., the same node.

##### Always co-located in the same node

In a three node cluster, a web application has in-memory cache such as redis. We want the web-servers to be co-located with the cache as much as possible.

Here is the yaml snippet of a simple redis deployment with three replicas and selector label `app=store`. The deployment has `PodAntiAffinity` configured to ensure the scheduler does not co-locate replicas on a single node.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis-cache
spec:
  selector:
    matchLabels:
      app: store
  replicas: 3
  template:
    metadata:
      labels:
        app: store
    spec:
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchExpressions:
              - key: app
                operator: In
                values:
                - store
            topologyKey: "kubernetes.io/hostname"
      containers:
      - name: redis-server
        image: redis:3.2-alpine
```

The below yaml snippet of the webserver deployment has `podAntiAffinity` and `podAffinity` configured. This informs the scheduler that all its replicas are to be co-located with pods that have selector label `app=store`. This will also ensure that each web-server replica does not co-locate on a single node.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-server
spec:
  selector:
    matchLabels:
      app: web-store
  replicas: 3
  template:
    metadata:
      labels:
        app: web-store
    spec:
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchExpressions:
              - key: app
                operator: In
                values:
                - web-store
            topologyKey: "kubernetes.io/hostname"
        podAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchExpressions:
              - key: app
                operator: In
                values:
                - store
            topologyKey: "kubernetes.io/hostname"
      containers:
      - name: web-app
        image: nginx:1.16-alpine
```

If we create the above two deployments, our three node cluster should look like below.

|       node-1         |       node-2        |       node-3       |
|:--------------------:|:-------------------:|:------------------:|
| *webserver-1*        |   *webserver-2*     |    *webserver-3*   |
|  *cache-1*           |     *cache-2*       |     *cache-3*      |

As you can see, all the 3 replicas of the `web-server` are automatically co-located with the cache as expected.

```
kubectl get pods -o wide
```
The output is similar to this:
```
NAME                           READY     STATUS    RESTARTS   AGE       IP           NODE
redis-cache-1450370735-6dzlj   1/1       Running   0          8m        10.192.4.2   kube-node-3
redis-cache-1450370735-j2j96   1/1       Running   0          8m        10.192.2.2   kube-node-1
redis-cache-1450370735-z73mh   1/1       Running   0          8m        10.192.3.1   kube-node-2
web-server-1287567482-5d4dz    1/1       Running   0          7m        10.192.2.3   kube-node-1
web-server-1287567482-6f7v5    1/1       Running   0          7m        10.192.4.3   kube-node-3
web-server-1287567482-s330j    1/1       Running   0          7m        10.192.3.2   kube-node-2
```

##### Never co-located in the same node

The above example uses `PodAntiAffinity` rule with `topologyKey: "kubernetes.io/hostname"` to deploy the redis cluster so that
no two instances are located on the same host.
See [ZooKeeper tutorial](/docs/tutorials/stateful-application/zookeeper/#tolerating-node-failure)
for an example of a StatefulSet configured with anti-affinity for high availability, using the same technique.

## nodeName

`nodeName` is the simplest form of node selection constraint, but due
to its limitations it is typically not used.  `nodeName` is a field of
PodSpec.  If it is non-empty, the scheduler ignores the pod and the
kubelet running on the named node tries to run the pod.  Thus, if
`nodeName` is provided in the PodSpec, it takes precedence over the
above methods for node selection.

Some of the limitations of using `nodeName` to select nodes are:

-   If the named node does not exist, the pod will not be run, and in
    some cases may be automatically deleted.
-   If the named node does not have the resources to accommodate the
    pod, the pod will fail and its reason will indicate why,
    for example OutOfmemory or OutOfcpu.
-   Node names in cloud environments are not always predictable or
    stable.

Here is an example of a pod config file using the `nodeName` field:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
spec:
  containers:
  - name: nginx
    image: nginx
  nodeName: kube-01
```

The above pod will run on the node kube-01.



## {{% heading "whatsnext" %}}


[Taints](/docs/concepts/scheduling-eviction/taint-and-toleration/) allow a Node to *repel* a set of Pods.

The design documents for
[node affinity](https://git.k8s.io/community/contributors/design-proposals/scheduling/nodeaffinity.md)
and for [inter-pod affinity/anti-affinity](https://git.k8s.io/community/contributors/design-proposals/scheduling/podaffinity.md) contain extra background information about these features.

Once a Pod is assigned to a Node, the kubelet runs the Pod and allocates node-local resources.
The [topology manager](/docs/tasks/administer-cluster/topology-manager/) can take part in node-level
resource allocation decisions. 


