---
title: Pod 优先级和抢占
content_type: concept
weight: 50
---

<!-- 
reviewers:
- davidopp
- wojtek-t
title: Pod Priority and Preemption
content_type: concept
weight: 50
-->

<!-- overview -->

{{< feature-state for_k8s_version="v1.14" state="stable" >}}

<!--  
[Pods](/docs/concepts/workloads/pods/) can have _priority_. Priority indicates the
importance of a Pod relative to other Pods. If a Pod cannot be scheduled, the
scheduler tries to preempt (evict) lower priority Pods to make scheduling of the
pending Pod possible.
-->
[Pod](/zh/docs/concepts/workloads/pods/) 可以有 _优先级_。
优先级表示一个 Pod 相对于其他 Pod 的重要性。
如果一个 Pod 无法被调度，调度程序会尝试抢占（驱逐）较低优先级的 Pod，
以使悬决 Pod 可以被调度。

<!-- body -->

{{< warning >}}
<!-- 
In a cluster where not all users are trusted, a malicious user could create Pods
at the highest possible priorities, causing other Pods to be evicted/not get
scheduled.
An administrator can use ResourceQuota to prevent users from creating pods at
high priorities.

See [limit Priority Class consumption by default](/docs/concepts/policy/resource-quotas/#limit-priority-class-consumption-by-default)
for details.
-->
在一个并非所有用户都是可信的集群中，恶意用户可能以最高优先级创建 Pod，
导致其他 Pod 被驱逐或者无法被调度。
管理员可以使用 ResourceQuota 来阻止用户创建高优先级的 Pod。
参见[默认限制优先级消费](/zh/docs/concepts/policy/resource-quotas/#limit-priority-class-consumption-by-default)。

{{< /warning >}}

<!--  
## How to use priority and preemption

To use priority and preemption:

1.  Add one or more [PriorityClasses](#priorityclass).

1.  Create Pods with[`priorityClassName`](#pod-priority) set to one of the added
    PriorityClasses. Of course you do not need to create the Pods directly;
    normally you would add `priorityClassName` to the Pod template of a
    collection object like a Deployment.

Keep reading for more information about these steps.
-->
## 如何使用优先级和抢占

要使用优先级和抢占：

1.  新增一个或多个 [PriorityClass](#priorityclass)。

1.  创建 Pod，并将其 [`priorityClassName`](#pod-priority) 设置为新增的 PriorityClass。
    当然你不需要直接创建 Pod；通常，你将会添加 `priorityClassName` 到集合对象（如 Deployment）
    的 Pod 模板中。

继续阅读以获取有关这些步骤的更多信息。

{{< note >}}
<!-- 
Kubernetes already ships with two PriorityClasses:
`system-cluster-critical` and `system-node-critical`.
These are common classes and are used to [ensure that critical components are always scheduled first](/docs/tasks/administer-cluster/guaranteed-scheduling-critical-addon-pods/).
-->
Kubernetes 已经提供了 2 个 PriorityClass：
`system-cluster-critical` 和 `system-node-critical`。
这些是常见的类，用于[确保始终优先调度关键组件](/zh/docs/tasks/administer-cluster/guaranteed-scheduling-critical-addon-pods/)。
{{< /note >}}

<!-- 
## PriorityClass

A PriorityClass is a non-namespaced object that defines a mapping from a
priority class name to the integer value of the priority. The name is specified
in the `name` field of the PriorityClass object's metadata. The value is
specified in the required `value` field. The higher the value, the higher the
priority.
The name of a PriorityClass object must be a valid
[DNS subdomain name](/docs/concepts/overview/working-with-objects/names#dns-subdomain-names),
and it cannot be prefixed with `system-`.
-->
## PriorityClass {#priorityclass}

PriorityClass 是一个无名称空间对象，它定义了从优先级类名称到优先级整数值的映射。
名称在 PriorityClass 对象元数据的 `name` 字段中指定。
值在必填的 `value` 字段中指定。值越大，优先级越高。
PriorityClass 对象的名称必须是有效的
[DNS 子域名](/zh/docs/concepts/overview/working-with-objects/names#dns-subdomain-names)，
并且它不能以 `system-` 为前缀。

<!--  
A PriorityClass object can have any 32-bit integer value smaller than or equal
to 1 billion. Larger numbers are reserved for critical system Pods that should
not normally be preempted or evicted. A cluster admin should create one
PriorityClass object for each such mapping that they want.

PriorityClass also has two optional fields: `globalDefault` and `description`.
The `globalDefault` field indicates that the value of this PriorityClass should
be used for Pods without a `priorityClassName`. Only one PriorityClass with
`globalDefault` set to true can exist in the system. If there is no
PriorityClass with `globalDefault` set, the priority of Pods with no
`priorityClassName` is zero.

The `description` field is an arbitrary string. It is meant to tell users of the
cluster when they should use this PriorityClass.
-->
PriorityClass 对象可以设置任何小于或等于 10 亿的 32 位整数值。
较大的数字是为通常不应被抢占或驱逐的关键的系统 Pod 所保留的。
集群管理员应该为这类映射分别创建独立的 PriorityClass 对象。

PriorityClass 还有两个可选字段：`globalDefault` 和 `description`。
`globalDefault` 字段表示这个 PriorityClass 的值应该用于没有 `priorityClassName` 的 Pod。
系统中只能存在一个 `globalDefault` 设置为 true 的 PriorityClass。
如果不存在设置了 `globalDefault` 的 PriorityClass，
则没有 `priorityClassName` 的 Pod 的优先级为零。

`description` 字段是一个任意字符串。
它用来告诉集群用户何时应该使用此 PriorityClass。

<!--  
### Notes about PodPriority and existing clusters

-   If you upgrade an existing cluster without this feature, the priority
    of your existing Pods is effectively zero.

-   Addition of a PriorityClass with `globalDefault` set to `true` does not
    change the priorities of existing Pods. The value of such a PriorityClass is
    used only for Pods created after the PriorityClass is added.

-   If you delete a PriorityClass, existing Pods that use the name of the
    deleted PriorityClass remain unchanged, but you cannot create more Pods that
    use the name of the deleted PriorityClass.
-->
### 关于 PodPriority 和现有集群的注意事项

-   如果你升级一个已经存在的但尚未使用此特性的集群，该集群中已经存在的 Pod 的优先级等效于零。

-   添加一个将 `globalDefault` 设置为 `true` 的 PriorityClass 不会改变现有 Pod 的优先级。
    此类 PriorityClass 的值仅用于添加 PriorityClass 后创建的 Pod。

-   如果你删除了某个 PriorityClass 对象，则使用被删除的 PriorityClass 名称的现有 Pod 保持不变，
    但是你不能再创建使用已删除的 PriorityClass 名称的 Pod。

<!-- ### Example PriorityClass -->
### PriorityClass 示例

```yaml
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: high-priority
value: 1000000
globalDefault: false
description: "此优先级类应仅用于 XYZ 服务 Pod。"
```

<!--  
## Non-preempting PriorityClass {#non-preempting-priority-class}

{{< feature-state for_k8s_version="v1.19" state="beta" >}}

Pods with `PreemptionPolicy: Never` will be placed in the scheduling queue
ahead of lower-priority pods,
but they cannot preempt other pods.
A non-preempting pod waiting to be scheduled will stay in the scheduling queue,
until sufficient resources are free,
and it can be scheduled.
Non-preempting pods,
like other pods,
are subject to scheduler back-off.
This means that if the scheduler tries these pods and they cannot be scheduled,
they will be retried with lower frequency,
allowing other pods with lower priority to be scheduled before them.

Non-preempting pods may still be preempted by other,
high-priority pods.
-->
## 非抢占式 PriorityClass {#non-preempting-priority-class}

{{< feature-state for_k8s_version="v1.19" state="beta" >}}

配置了 `PreemptionPolicy: Never` 的 Pod 将被放置在调度队列中较低优先级 Pod 之前，
但它们不能抢占其他 Pod。等待调度的非抢占式 Pod 将留在调度队列中，直到有足够的可用资源，
它才可以被调度。非抢占式 Pod，像其他 Pod 一样，受调度程序回退的影响。
这意味着如果调度程序尝试这些 Pod 并且无法调度它们，它们将以更低的频率被重试，
从而允许其他优先级较低的 Pod 排在它们之前。

非抢占式 Pod 仍可能被其他高优先级 Pod 抢占。

<!--  
`PreemptionPolicy` defaults to `PreemptLowerPriority`,
which will allow pods of that PriorityClass to preempt lower-priority pods
(as is existing default behavior).
If `PreemptionPolicy` is set to `Never`,
pods in that PriorityClass will be non-preempting.

An example use case is for data science workloads.
A user may submit a job that they want to be prioritized above other workloads,
but do not wish to discard existing work by preempting running pods.
The high priority job with `PreemptionPolicy: Never` will be scheduled
ahead of other queued pods,
as soon as sufficient cluster resources "naturally" become free.
-->
`PreemptionPolicy` 默认为 `PreemptLowerPriority`，
这将允许该 PriorityClass 的 Pod 抢占较低优先级的 Pod（现有默认行为也是如此）。
如果 `PreemptionPolicy` 设置为 `Never`，则该 PriorityClass 中的 Pod 将是非抢占式的。

数据科学工作负载是一个示例用例。用户可以提交他们希望优先于其他工作负载的作业，
但不希望因为抢占运行中的 Pod 而导致现有工作被丢弃。
设置为 `PreemptionPolicy: Never` 的高优先级作业将在其他排队的 Pod 之前被调度，
只要足够的集群资源“自然地”变得可用。

<!-- ### Example Non-preempting PriorityClass -->
### 非抢占式 PriorityClass 示例

```yaml
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: high-priority-nonpreempting
value: 1000000
preemptionPolicy: Never
globalDefault: false
description: "This priority class will not cause other pods to be preempted."
```

<!-- 
## Pod priority

After you have one or more PriorityClasses, you can create Pods that specify one
of those PriorityClass names in their specifications. The priority admission
controller uses the `priorityClassName` field and populates the integer value of
the priority. If the priority class is not found, the Pod is rejected.

The following YAML is an example of a Pod configuration that uses the
PriorityClass created in the preceding example. The priority admission
controller checks the specification and resolves the priority of the Pod to
1000000.
-->
## Pod 优先级 {#pod-priority}

在你拥有一个或多个 PriorityClass 对象之后，
你可以创建在其规约中指定这些 PriorityClass 名称之一的 Pod。
优先级准入控制器使用 `priorityClassName` 字段并填充优先级的整数值。
如果未找到所指定的优先级类，则拒绝 Pod。

以下 YAML 是 Pod 配置的示例，它使用在前面的示例中创建的 PriorityClass。
优先级准入控制器检查 Pod 规约并将其优先级解析为 1000000。

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
    imagePullPolicy: IfNotPresent
  priorityClassName: high-priority
```

<!--  
### Effect of Pod priority on scheduling order

When Pod priority is enabled, the scheduler orders pending Pods by
their priority and a pending Pod is placed ahead of other pending Pods
with lower priority in the scheduling queue. As a result, the higher
priority Pod may be scheduled sooner than Pods with lower priority if
its scheduling requirements are met. If such Pod cannot be scheduled,
scheduler will continue and tries to schedule other lower priority Pods.
-->
### Pod 优先级对调度顺序的影响

当启用 Pod 优先级时，调度程序会按优先级对悬决 Pod 进行排序，
并且每个悬决的 Pod 会被放置在调度队列中其他优先级较低的悬决 Pod 之前。
因此，如果满足调度要求，较高优先级的 Pod 可能会比具有较低优先级的 Pod 更早调度。
如果无法调度此类 Pod，调度程序将继续并尝试调度其他较低优先级的 Pod。

<!-- 
## Preemption

When Pods are created, they go to a queue and wait to be scheduled. The
scheduler picks a Pod from the queue and tries to schedule it on a Node. If no
Node is found that satisfies all the specified requirements of the Pod,
preemption logic is triggered for the pending Pod. Let's call the pending Pod P.
Preemption logic tries to find a Node where removal of one or more Pods with
lower priority than P would enable P to be scheduled on that Node. If such a
Node is found, one or more lower priority Pods get evicted from the Node. After
the Pods are gone, P can be scheduled on the Node.
-->
## 抢占    {#preemption}

Pod 被创建后会进入队列等待调度。
调度器从队列中挑选一个 Pod 并尝试将它调度到某个节点上。
如果没有找到满足 Pod 的所指定的所有要求的节点，则触发对悬决 Pod 的抢占逻辑。
让我们将悬决 Pod 称为 P。抢占逻辑试图找到一个节点，
在该节点中删除一个或多个优先级低于 P 的 Pod，则可以将 P 调度到该节点上。
如果找到这样的节点，一个或多个优先级较低的 Pod 会被从节点中驱逐。
被驱逐的 Pod 消失后，P 可以被调度到该节点上。

<!--  
### User exposed information

When Pod P preempts one or more Pods on Node N, `nominatedNodeName` field of Pod
P's status is set to the name of Node N. This field helps scheduler track
resources reserved for Pod P and also gives users information about preemptions
in their clusters.

Please note that Pod P is not necessarily scheduled to the "nominated Node".
After victim Pods are preempted, they get their graceful termination period. If
another node becomes available while scheduler is waiting for the victim Pods to
terminate, scheduler will use the other node to schedule Pod P. As a result
`nominatedNodeName` and `nodeName` of Pod spec are not always the same. Also, if
scheduler preempts Pods on Node N, but then a higher priority Pod than Pod P
arrives, scheduler may give Node N to the new higher priority Pod. In such a
case, scheduler clears `nominatedNodeName` of Pod P. By doing this, scheduler
makes Pod P eligible to preempt Pods on another Node.
-->
### 用户暴露的信息

当 Pod P 抢占节点 N 上的一个或多个 Pod 时，
Pod P 状态的 `nominatedNodeName` 字段被设置为节点 N 的名称。
该字段帮助调度程序跟踪为 Pod P 保留的资源，并为用户提供有关其集群中抢占的信息。

请注意，Pod P 不一定会调度到“被提名的节点（Nominated Node）”。
在 Pod 因抢占而牺牲时，它们将获得体面终止期。
如果调度程序正在等待牺牲者 Pod 终止时另一个节点变得可用，
则调度程序将使用另一个节点来调度 Pod P。
因此，Pod 规约中的 `nominatedNodeName` 和 `nodeName` 并不总是相同。
此外，如果调度程序抢占节点 N 上的 Pod，但随后比 Pod P 更高优先级的 Pod 到达，
则调度程序可能会将节点 N 分配给新的更高优先级的 Pod。
在这种情况下，调度程序会清除 Pod P 的 `nominatedNodeName`。
通过这样做，调度程序使 Pod P 有资格抢占另一个节点上的 Pod。

<!-- 
### Limitations of preemption

#### Graceful termination of preemption victims

When Pods are preempted, the victims get their
[graceful termination period](/docs/concepts/workloads/pods/pod-lifecycle/#pod-termination).
They have that much time to finish their work and exit. If they don't, they are
killed. This graceful termination period creates a time gap between the point
that the scheduler preempts Pods and the time when the pending Pod (P) can be
scheduled on the Node (N). In the meantime, the scheduler keeps scheduling other
pending Pods. As victims exit or get terminated, the scheduler tries to schedule
Pods in the pending queue. Therefore, there is usually a time gap between the
point that scheduler preempts victims and the time that Pod P is scheduled. In
order to minimize this gap, one can set graceful termination period of lower
priority Pods to zero or a small number.
-->
### 抢占的限制

#### 被抢占牺牲者的体面终止

当 Pod 被抢占时，牺牲者会得到他们的
[体面终止期](/zh/docs/concepts/workloads/pods/pod-lifecycle/#pod-termination)。
它们可以在体面终止期内完成工作并退出。如果它们不这样做就会被杀死。
这个体面终止期在调度程序抢占 Pod 的时间点和待处理的 Pod (P) 
可以在节点 (N) 上调度的时间点之间划分出了一个时间跨度。
同时，调度器会继续调度其他待处理的 Pod。当牺牲者退出或被终止时，
调度程序会尝试在待处理队列中调度 Pod。
因此，调度器抢占牺牲者的时间点与 Pod P 被调度的时间点之间通常存在时间间隔。
为了最小化这个差距，可以将低优先级 Pod 的体面终止时间设置为零或一个小数字。

<!-- 
#### PodDisruptionBudget is supported, but not guaranteed

A [PodDisruptionBudget](/docs/concepts/workloads/pods/disruptions/) (PDB)
allows application owners to limit the number of Pods of a replicated application
that are down simultaneously from voluntary disruptions. Kubernetes supports
PDB when preempting Pods, but respecting PDB is best effort. The scheduler tries
to find victims whose PDB are not violated by preemption, but if no such victims
are found, preemption will still happen, and lower priority Pods will be removed
despite their PDBs being violated.
-->
#### 支持 PodDisruptionBudget，但不保证

[PodDisruptionBudget](/zh/docs/concepts/workloads/pods/disruptions/) 
(PDB) 允许多副本应用程序的所有者限制因自愿性质的干扰而同时终止的 Pod 数量。
Kubernetes 在抢占 Pod 时支持 PDB，但对 PDB 的支持是基于尽力而为原则的。
调度器会尝试寻找不会因被抢占而违反 PDB 的牺牲者，但如果没有找到这样的牺牲者，
抢占仍然会发生，并且即使违反了 PDB 约束也会删除优先级较低的 Pod。

<!-- 
#### Inter-Pod affinity on lower-priority Pods

A Node is considered for preemption only when the answer to this question is
yes: "If all the Pods with lower priority than the pending Pod are removed from
the Node, can the pending Pod be scheduled on the Node?"

{{< note >}}
Preemption does not necessarily remove all lower-priority
Pods. If the pending Pod can be scheduled by removing fewer than all
lower-priority Pods, then only a portion of the lower-priority Pods are removed.
Even so, the answer to the preceding question must be yes. If the answer is no,
the Node is not considered for preemption.
{{< /note >}}
-->
#### 与低优先级 Pod 之间的 Pod 间亲和性

只有当这个问题的答案是肯定的时，才考虑在一个节点上执行抢占操作：
“如果从此节点上删除优先级低于悬决 Pod 的所有 Pod，悬决 Pod 是否可以在该节点上调度？”

{{< note >}}
抢占并不一定会删除所有较低优先级的 Pod。
如果悬决 Pod 可以通过删除少于所有较低优先级的 Pod 来调度，
那么只有一部分较低优先级的 Pod 会被删除。
即便如此，上述问题的答案必须是肯定的。
如果答案是否定的，则不考虑在该节点上执行抢占。
{{< /note >}}

<!-- 
If a pending Pod has inter-pod affinity to one or more of the lower-priority
Pods on the Node, the inter-Pod affinity rule cannot be satisfied in the absence
of those lower-priority Pods. In this case, the scheduler does not preempt any
Pods on the Node. Instead, it looks for another Node. The scheduler might find a
suitable Node or it might not. There is no guarantee that the pending Pod can be
scheduled.

Our recommended solution for this problem is to create inter-Pod affinity only
towards equal or higher priority Pods.
-->
如果悬决 Pod 与节点上的一个或多个较低优先级 Pod 具有 Pod 间亲和性，
则在没有这些较低优先级 Pod 的情况下，无法满足 Pod 间亲和性规则。
在这种情况下，调度程序不会抢占节点上的任何 Pod。
相反，它寻找另一个节点。调度程序可能会找到合适的节点，
也可能不会。无法保证悬决 Pod 可以被调度。

我们针对此问题推荐的解决方案是仅针对同等或更高优先级的 Pod 设置 Pod 间亲和性。

<!-- 
#### Cross node preemption

Suppose a Node N is being considered for preemption so that a pending Pod P can
be scheduled on N. P might become feasible on N only if a Pod on another Node is
preempted. Here's an example:

*   Pod P is being considered for Node N.
*   Pod Q is running on another Node in the same Zone as Node N.
*   Pod P has Zone-wide anti-affinity with Pod Q (`topologyKey:
    topology.kubernetes.io/zone`).
*   There are no other cases of anti-affinity between Pod P and other Pods in
    the Zone.
*   In order to schedule Pod P on Node N, Pod Q can be preempted, but scheduler
    does not perform cross-node preemption. So, Pod P will be deemed
    unschedulable on Node N.

If Pod Q were removed from its Node, the Pod anti-affinity violation would be
gone, and Pod P could possibly be scheduled on Node N.

We may consider adding cross Node preemption in future versions if there is
enough demand and if we find an algorithm with reasonable performance.
-->
#### 跨节点抢占

假设正在考虑在一个节点 N 上执行抢占，以便可以在 N 上调度待处理的 Pod P。
只有当另一个节点上的 Pod 被抢占时，P 才可能在 N 上变得可行。
下面是一个例子：

*   正在考虑将 Pod P 调度到节点 N 上。
*   Pod Q 正在与节点 N 位于同一区域的另一个节点上运行。
*   Pod P 与 Pod Q 具有 Zone 维度的反亲和（`topologyKey:topology.kubernetes.io/zone`）。
*   Pod P 与 Zone 中的其他 Pod 之间没有其他反亲和性设置。
*   为了在节点 N 上调度 Pod P，可以抢占 Pod Q，但调度器不会进行跨节点抢占。
    因此，Pod P 将被视为在节点 N 上不可调度。

如果将 Pod Q 从所在节点中移除，则不会违反 Pod 间反亲和性约束，
并且 Pod P 可能会被调度到节点 N 上。

如果有足够的需求，并且如果我们找到性能合理的算法，
我们可能会考虑在未来版本中添加跨节点抢占。

<!-- 
## Troubleshooting

Pod priority and pre-emption can have unwanted side effects. Here are some
examples of potential problems and ways to deal with them.
-->
## 故障排除

Pod 优先级和抢占可能会产生不必要的副作用。以下是一些潜在问题的示例以及处理这些问题的方法。

<!--  
### Pods are preempted unnecessarily

Preemption removes existing Pods from a cluster under resource pressure to make
room for higher priority pending Pods. If you give high priorities to
certain Pods by mistake, these unintentionally high priority Pods may cause
preemption in your cluster. Pod priority is specified by setting the
`priorityClassName` field in the Pod's specification. The integer value for
priority is then resolved and populated to the `priority` field of `podSpec`.

To address the problem, you can change the `priorityClassName` for those Pods
to use lower priority classes, or leave that field empty. An empty
`priorityClassName` is resolved to zero by default.

When a Pod is preempted, there will be events recorded for the preempted Pod.
Preemption should happen only when a cluster does not have enough resources for
a Pod. In such cases, preemption happens only when the priority of the pending
Pod (preemptor) is higher than the victim Pods. Preemption must not happen when
there is no pending Pod, or when the pending Pods have equal or lower priority
than the victims. If preemption happens in such scenarios, please file an issue.
-->
### Pod 被不必要地抢占

抢占在资源压​​力较大时从集群中删除现有 Pod，为更高优先级的悬决 Pod 腾出空间。
如果你错误地为某些 Pod 设置了高优先级，这些无意的高优先级 Pod 可能会导致集群中出现抢占行为。
Pod 优先级是通过设置 Pod 规约中的 `priorityClassName` 字段来指定的。
优先级的整数值然后被解析并填充到 `podSpec` 的 `priority` 字段。

为了解决这个问题，你可以将这些 Pod 的 `priorityClassName` 更改为使用较低优先级的类，
或者将该字段留空。默认情况下，空的 `priorityClassName` 解析为零。

当 Pod 被抢占时，集群会为被抢占的 Pod 记录事件。只有当集群没有足够的资源用于 Pod 时，
才会发生抢占。在这种情况下，只有当悬决 Pod（抢占者）的优先级高于受害 Pod 时才会发生抢占。
当没有悬决 Pod，或者悬决 Pod 的优先级等于或低于牺牲者时，不得发生抢占。
如果在这种情况下发生抢占，请提出问题。

<!-- 
### Pods are preempted, but the preemptor is not scheduled

When pods are preempted, they receive their requested graceful termination
period, which is by default 30 seconds. If the victim Pods do not terminate within
this period, they are forcibly terminated. Once all the victims go away, the
preemptor Pod can be scheduled.

While the preemptor Pod is waiting for the victims to go away, a higher priority
Pod may be created that fits on the same Node. In this case, the scheduler will
schedule the higher priority Pod instead of the preemptor.

This is expected behavior: the Pod with the higher priority should take the place
of a Pod with a lower priority.
-->
### 有 Pod 被抢占，但抢占者并没有被调度

当 Pod 被抢占时，它们会收到请求的体面终止期，默认为 30 秒。
如果受害 Pod 在此期限内没有终止，它们将被强制终止。
一旦所有牺牲者都离开，就可以调度抢占者 Pod。

在抢占者 Pod 等待牺牲者离开的同时，可能某个适合同一个节点的更高优先级的 Pod 被创建。
在这种情况下，调度器将调度优先级更高的 Pod 而不是抢占者。

这是预期的行为：具有较高优先级的 Pod 应该取代具有较低优先级的 Pod。

<!-- 
### Higher priority Pods are preempted before lower priority pods

The scheduler tries to find nodes that can run a pending Pod. If no node is
found, the scheduler tries to remove Pods with lower priority from an arbitrary
node in order to make room for the pending pod.
If a node with low priority Pods is not feasible to run the pending Pod, the scheduler
may choose another node with higher priority Pods (compared to the Pods on the
other node) for preemption. The victims must still have lower priority than the
preemptor Pod.

When there are multiple nodes available for preemption, the scheduler tries to
choose the node with a set of Pods with lowest priority. However, if such Pods
have PodDisruptionBudget that would be violated if they are preempted then the
scheduler may choose another node with higher priority Pods.

When multiple nodes exist for preemption and none of the above scenarios apply,
the scheduler chooses a node with the lowest priority.
-->
### 优先级较高的 Pod 在优先级较低的 Pod 之前被抢占

调度程序尝试查找可以运行悬决 Pod 的节点。如果没有找到这样的节点，
调度程序会尝试从任意节点中删除优先级较低的 Pod，以便为悬决 Pod 腾出空间。
如果具有低优先级 Pod 的节点无法运行悬决 Pod，
调度器可能会选择另一个具有更高优先级 Pod 的节点（与其他节点上的 Pod 相比）进行抢占。
牺牲者的优先级必须仍然低于抢占者 Pod。

当有多个节点可供执行抢占操作时，调度器会尝试选择具有一组优先级最低的 Pod 的节点。
但是，如果此类 Pod 具有 PodDisruptionBudget，当它们被抢占时，
则会违反 PodDisruptionBudget，那么调度程序可能会选择另一个具有更高优先级 Pod 的节点。

当存在多个节点抢占且上述场景均不适用时，调度器会选择优先级最低的节点。

<!-- 
## Interactions between Pod priority and quality of service {#interactions-of-pod-priority-and-qos}

Pod priority and {{< glossary_tooltip text="QoS class" term_id="qos-class" >}}
are two orthogonal features with few interactions and no default restrictions on
setting the priority of a Pod based on its QoS classes. The scheduler's
preemption logic does not consider QoS when choosing preemption targets.
Preemption considers Pod priority and attempts to choose a set of targets with
the lowest priority. Higher-priority Pods are considered for preemption only if
the removal of the lowest priority Pods is not sufficient to allow the scheduler
to schedule the preemptor Pod, or if the lowest priority Pods are protected by
`PodDisruptionBudget`.
-->
## Pod 优先级和服务质量之间的相互作用 {#interactions-of-pod-priority-and-qos}

Pod 优先级和 {{<glossary_tooltip text="QoS 类" term_id="qos-class" >}}
是两个正交特征，交互很少，并且对基于 QoS 类设置 Pod 的优先级没有默认限制。
调度器的抢占逻辑在选择抢占目标时不考虑 QoS。
抢占会考虑 Pod 优先级并尝试选择一组优先级最低的目标。
仅当移除优先级最低的 Pod 不足以让调度程序调度抢占式 Pod，
或者最低优先级的 Pod 受 PodDisruptionBudget 保护时，才会考虑优先级较高的 Pod。

<!-- 
The kubelet uses Priority to determine pod order for [out-of-resource eviction](/docs/tasks/administer-cluster/out-of-resource/).
You can use the QoS class to estimate the order in which pods are most likely
to get evicted. The kubelet ranks pods for eviction based on the following factors:

  1. Whether the starved resource usage exceeds requests
  1. Pod Priority
  1. Amount of resource usage relative to requests 

See [evicting end-user pods](/docs/tasks/administer-cluster/out-of-resource/#evicting-end-user-pods)
for more details.

kubelet out-of-resource eviction does not evict Pods when their
usage does not exceed their requests. If a Pod with lower priority is not
exceeding its requests, it won't be evicted. Another Pod with higher priority
that exceeds its requests may be evicted.
-->
kubelet 使用优先级来确定
[资源不足时驱逐](/zh/docs/tasks/administer-cluster/out-of-resource/) Pod 的顺序。
你可以使用 QoS 类来估计 Pod 最有可能被驱逐的顺序。kubelet 根据以下因素对 Pod 进行驱逐排名：

  1. 对紧俏资源的使用是否超过请求值
  1. Pod 优先级
  1. 相对于请求的资源使用量

有关更多详细信息，请参阅[驱逐最终用户的 Pod](/zh/docs/tasks/administer-cluster/out-of-resource/#evicting-end-user-pods)。

当某 Pod 的资源用量未超过其请求时，kubelet 资源不足驱逐不会驱逐该 Pod。
如果优先级较低的 Pod 没有超过其请求，则不会被驱逐。
另一个优先级高于其请求的 Pod 可能会被驱逐。

## {{% heading "whatsnext" %}}

<!-- 
* Read about using ResourceQuotas in connection with PriorityClasses: 
  [limit Priority Class consumption by default](/docs/concepts/policy/resource-quotas/#limit-priority-class-consumption-by-default)
* Learn about [Pod Disruption](/docs/concepts/workloads/pods/disruptions/)
* Learn about [API-initiated Eviction](/docs/concepts/scheduling-eviction/api-eviction/)
* Learn about [Node-pressure Eviction](/docs/concepts/scheduling-eviction/node-pressure-eviction/)
-->
* 阅读有关将 ResourceQuota 与 PriorityClass 结合使用的信息：
  [默认限制优先级消费](/zh/docs/concepts/policy/resource-quotas/#limit-priority-class-consumption-by-default)
* 了解 [Pod 干扰](/zh/docs/concepts/workloads/pods/disruptions/)
* 了解 [API 发起的驱逐](/zh/docs/concepts/scheduling-eviction/api-eviction/)
* 了解[节点压力驱逐](/zh/docs/concepts/scheduling-eviction/node-pressure-eviction/)