---
title: 调度框架
content_type: concept
weight: 90
---

<!--
---
reviewers:
- ahg-g
title: Scheduling Framework
content_type: concept
weight: 90
---
-->

<!-- overview -->

{{< feature-state for_k8s_version="1.15" state="alpha" >}}

<!--
The scheduling framework is a pluggable architecture for the Kubernetes scheduler.
It adds a new set of "plugin" APIs to the existing scheduler. Plugins are compiled into the scheduler. The APIs allow most scheduling features to be implemented as plugins, while keeping the
scheduling "core" lightweight and maintainable. Refer to the [design proposal of the
scheduling framework][kep] for more technical information on the design of the
framework.
-->

调度框架是面向 Kubernetes 调度器的一种插件架构，
它为现有的调度器添加了一组新的“插件” API。插件会被编译到调度器之中。
这些 API 允许大多数调度功能以插件的形式实现，同时使调度“核心”保持简单且可维护。
请参考[调度框架的设计提案](https://github.com/kubernetes/enhancements/blob/master/keps/sig-scheduling/624-scheduling-framework/README.md)
获取框架设计的更多技术信息。

<!-- body -->

<!--
# Framework workflow
-->
# 框架工作流程

<!--
The Scheduling Framework defines a few extension points. Scheduler plugins
register to be invoked at one or more extension points. Some of these plugins
can change the scheduling decisions and some are informational only.
-->
调度框架定义了一些扩展点。调度器插件注册后在一个或多个扩展点处被调用。
这些插件中的一些可以改变调度决策，而另一些仅用于提供信息。

<!--
Each attempt to schedule one Pod is split into two phases, the **scheduling
cycle** and the **binding cycle**.
-->
每次调度一个 Pod 的尝试都分为两个阶段，即 **调度周期** 和 **绑定周期**。

<!--
## Scheduling Cycle & Binding Cycle
-->
## 调度周期和绑定周期

<!--
The scheduling cycle selects a node for the Pod, and the binding cycle applies
that decision to the cluster. Together, a scheduling cycle and binding cycle are
referred to as a "scheduling context".
-->
调度周期为 Pod 选择一个节点，绑定周期将该决策应用于集群。
调度周期和绑定周期一起被称为“调度上下文”。

<!--
Scheduling cycles are run serially, while binding cycles may run concurrently.
-->
调度周期是串行运行的，而绑定周期可能是同时运行的。

<!--
A scheduling or binding cycle can be aborted if the Pod is determined to
be unschedulable or if there is an internal error. The Pod will be returned to
the queue and retried.
-->
如果确定 Pod 不可调度或者存在内部错误，则可以终止调度周期或绑定周期。
Pod 将返回队列并重试。

<!--
## Extension points
-->
## 扩展点

<!--
The following picture shows the scheduling context of a Pod and the extension
points that the scheduling framework exposes. In this picture "Filter" is
equivalent to "Predicate" and "Scoring" is equivalent to "Priority function".
-->
下图显示了一个 Pod 的调度上下文以及调度框架公开的扩展点。
在此图片中，“过滤器”等同于“断言”，“评分”相当于“优先级函数”。

<!--
One plugin may register at multiple extension points to perform more complex or
stateful tasks.
-->
一个插件可以在多个扩展点处注册，以执行更复杂或有状态的任务。

<!--
{{< figure src="/images/docs/scheduling-framework-extensions.png" title="scheduling framework extension points" >}}
-->
{{< figure src="/images/docs/scheduling-framework-extensions.png" title="调度框架扩展点" >}}

<!--
### QueueSort {#queue-sort}
-->
### 队列排序 {#queue-sort}

<!--
These plugins are used to sort Pods in the scheduling queue. A queue sort plugin
essentially provides a `less(Pod1, Pod2)` function. Only one queue sort
plugin may be enabled at a time.
-->
队列排序插件用于对调度队列中的 Pod 进行排序。
队列排序插件本质上提供 `less(Pod1, Pod2)` 函数。
一次只能启动一个队列插件。

<!--
### PreFilter {#pre-filter}
-->
### 前置过滤 {#pre-filter}

<!--
These plugins are used to pre-process info about the Pod, or to check certain
conditions that the cluster or the Pod must meet. If a PreFilter plugin returns
an error, the scheduling cycle is aborted.
-->
前置过滤插件用于预处理 Pod 的相关信息，或者检查集群或 Pod 必须满足的某些条件。
如果 PreFilter 插件返回错误，则调度周期将终止。

<!--
### Filter
-->
### 过滤

<!--
These plugins are used to filter out nodes that cannot run the Pod. For each
node, the scheduler will call filter plugins in their configured order. If any
filter plugin marks the node as infeasible, the remaining plugins will not be
called for that node. Nodes may be evaluated concurrently.
-->
过滤插件用于过滤出不能运行该 Pod 的节点。对于每个节点，
调度器将按照其配置顺序调用这些过滤插件。如果任何过滤插件将节点标记为不可行，
则不会为该节点调用剩下的过滤插件。节点可以被同时进行评估。

<!--
### PostFilter {#post-filter}
-->
### 后置过滤 {#post-filter}

<!--
These plugins are called after Filter phase, but only when no feasible nodes
were found for the pod. Plugins are called in their configured order. If
any postFilter plugin marks the node as `Schedulable`, the remaining plugins
will not be called. A typical PostFilter implementation is preemption, which
tries to make the pod schedulable by preempting other Pods.
-->

这些插件在筛选阶段后调用，但仅在该 Pod 没有可行的节点时调用。
插件按其配置的顺序调用。如果任何后过滤器插件标记节点为“可调度”，
则其余的插件不会调用。典型的后筛选实现是抢占，试图通过抢占其他 Pod
的资源使该 Pod 可以调度。

<!--
### PreScore {#pre-score}
 -->
### 前置评分 {#pre-score}

<!--
These plugins are used to perform "pre-scoring" work, which generates a sharable
state for Score plugins to use. If a PreScore plugin returns an error, the
scheduling cycle is aborted.
 -->
前置评分插件用于执行 “前置评分” 工作，即生成一个可共享状态供评分插件使用。
如果 PreScore 插件返回错误，则调度周期将终止。

<!--
### Score {#scoring}
 -->
### 评分 {#scoring}

<!--
These plugins are used to rank nodes that have passed the filtering phase. The
scheduler will call each scoring plugin for each node. There will be a well
defined range of integers representing the minimum and maximum scores. After the
[NormalizeScore](#normalize-scoring) phase, the scheduler will combine node
scores from all plugins according to the configured plugin weights.
-->
评分插件用于对通过过滤阶段的节点进行排名。调度器将为每个节点调用每个评分插件。
将有一个定义明确的整数范围，代表最小和最大分数。
在[标准化评分](#normalize-scoring)阶段之后，调度器将根据配置的插件权重
合并所有插件的节点分数。

<!--
### NormalizeScore {#normalize-scoring}
-->
### 标准化评分 {#normalize-scoring}

<!--
These plugins are used to modify scores before the scheduler computes a final
ranking of Nodes. A plugin that registers for this extension point will be
called with the [Score](#scoring) results from the same plugin. This is called
once per plugin per scheduling cycle.
-->
标准化评分插件用于在调度器计算节点的排名之前修改分数。
在此扩展点注册的插件将使用同一插件的[评分](#scoring) 结果被调用。
每个插件在每个调度周期调用一次。

<!--
For example, suppose a plugin `BlinkingLightScorer` ranks Nodes based on how
many blinking lights they have.
-->
例如，假设一个 `BlinkingLightScorer` 插件基于具有的闪烁指示灯数量来对节点进行排名。

```go
func ScoreNode(_ *v1.pod, n *v1.Node) (int, error) {
   return getBlinkingLightCount(n)
}
```

<!--
However, the maximum count of blinking lights may be small compared to
`NodeScoreMax`. To fix this, `BlinkingLightScorer` should also register for this
extension point.
-->
然而，最大的闪烁灯个数值可能比 `NodeScoreMax` 小。要解决这个问题，
`BlinkingLightScorer` 插件还应该注册该扩展点。

```go
func NormalizeScores(scores map[string]int) {
   highest := 0
   for _, score := range scores {
      highest = max(highest, score)
   }
   for node, score := range scores {
      scores[node] = score*NodeScoreMax/highest
   }
}
```

<!--
If any NormalizeScore plugin returns an error, the scheduling cycle is
aborted.
-->
如果任何 NormalizeScore 插件返回错误，则调度阶段将终止。

<!--
Plugins wishing to perform "pre-reserve" work should use the
NormalizeScore extension point.
-->
{{< note >}}
希望执行“预保留”工作的插件应该使用 NormalizeScore 扩展点。
{{< /note >}}

<!--
### Reserve
-->
### Reserve

<!--
This is an informational extension point. Plugins which maintain runtime state
(aka "stateful plugins") should use this extension point to be notified by the
scheduler when resources on a node are being reserved for a given Pod. This
happens before the scheduler actually binds the Pod to the Node, and it exists
to prevent race conditions while the scheduler waits for the bind to succeed.
-->
Reserve 是一个信息性的扩展点。
管理运行时状态的插件（也称为“有状态插件”）应该使用此扩展点，以便
调度器在节点给指定 Pod 预留了资源时能够通知该插件。
这是在调度器真正将 Pod 绑定到节点之前发生的，并且它存在是为了防止
在调度器等待绑定成功时发生竞争情况。

<!--
This is the last step in a scheduling cycle. Once a Pod is in the reserved
state, it will either trigger [Unreserve](#unreserve) plugins (on failure) or
[PostBind](#post-bind) plugins (on success) at the end of the binding cycle.
-->
这个是调度周期的最后一步。
一旦 Pod 处于保留状态，它将在绑定周期结束时触发[不保留](#unreserve) 插件
（失败时）或 [绑定后](#post-bind) 插件（成功时）。

<!--
### Permit
-->
### Permit

<!--
_Permit_ plugins are invoked at the end of the scheduling cycle for each Pod, to
prevent or delay the binding to the candidate node. A permit plugin can do one of
the three things:
-->
_Permit_ 插件在每个 Pod 调度周期的最后调用，用于防止或延迟 Pod 的绑定。
一个允许插件可以做以下三件事之一：

<!--
1.  **approve** \
    Once all Permit plugins approve a Pod, it is sent for binding.
-->
1.  **批准** \
    一旦所有 Permit 插件批准 Pod 后，该 Pod 将被发送以进行绑定。

<!--
1.  **deny** \
    If any Permit plugin denies a Pod, it is returned to the scheduling queue.
    This will trigger [Unreserve](#unreserve) plugins.
-->
1.  **拒绝** \
    如果任何 Permit 插件拒绝 Pod，则该 Pod 将被返回到调度队列。
    这将触发[Unreserve](#unreserve) 插件。

<!--
1.  **wait** (with a timeout) \
    If a Permit plugin returns "wait", then the Pod is kept in an internal "waiting"
    Pods list, and the binding cycle of this Pod starts but directly blocks until it
    gets [approved](#frameworkhandle). If a timeout occurs, **wait** becomes **deny**
    and the Pod is returned to the scheduling queue, triggering [Unreserve](#unreserve)
    plugins.
-->
1.  **等待**（带有超时） \
    如果一个 Permit 插件返回 “等待” 结果，则 Pod 将保持在一个内部的 “等待中”
    的 Pod 列表，同时该 Pod 的绑定周期启动时即直接阻塞直到得到
    [批准](#frameworkhandle)。如果超时发生，**等待** 变成 **拒绝**，并且 Pod
    将返回调度队列，从而触发 [Unreserve](#unreserve) 插件。


<!--
While any plugin can access the list of "waiting" Pods and approve them
(see [`FrameworkHandle`](https://git.k8s.io/enhancements/keps/sig-scheduling/624-scheduling-framework#frameworkhandle)), we expect only the permit
plugins to approve binding of reserved Pods that are in "waiting" state. Once a Pod
is approved, it is sent to the [PreBind](#pre-bind) phase.
 -->
{{< note >}}
尽管任何插件可以访问 “等待中” 状态的 Pod 列表并批准它们
(查看 [`FrameworkHandle`](https://git.k8s.io/enhancements/keps/sig-scheduling/624-scheduling-framework#frameworkhandle))。
我们期望只有允许插件可以批准处于 “等待中” 状态的预留 Pod 的绑定。
一旦 Pod 被批准了，它将发送到[预绑定](#pre-bind) 阶段。
{{< /note >}}

<!--
### Pre-bind {#pre-bind}
-->
### 预绑定 {#pre-bind}

<!--
These plugins are used to perform any work required before a Pod is bound. For
example, a pre-bind plugin may provision a network volume and mount it on the
target node before allowing the Pod to run there.
-->
预绑定插件用于执行 Pod 绑定前所需的任何工作。
例如，一个预绑定插件可能需要提供网络卷并且在允许 Pod 运行在该节点之前
将其挂载到目标节点上。

<!--
If any PreBind plugin returns an error, the Pod is [rejected](#unreserve) and
returned to the scheduling queue.
-->
如果任何 PreBind 插件返回错误，则 Pod 将被[拒绝](#unreserve) 并且
退回到调度队列中。

<!--
### Bind
-->
### Bind

<!--
These plugins are used to bind a Pod to a Node. Bind plugins will not be called
until all PreBind plugins have completed. Each bind plugin is called in the
configured order. A bind plugin may choose whether or not to handle the given
Pod. If a bind plugin chooses to handle a Pod, **the remaining bind plugins are
skipped**.
-->
Bind 插件用于将 Pod 绑定到节点上。直到所有的 PreBind 插件都完成，Bind 插件才会被调用。
各绑定插件按照配置顺序被调用。绑定插件可以选择是否处理指定的 Pod。
如果绑定插件选择处理 Pod，**剩余的绑定插件将被跳过**。

<!--
### PostBind {#post-bind}
-->
### 绑定后 {#post-bind}

<!--
This is an informational extension point. Post-bind plugins are called after a
Pod is successfully bound. This is the end of a binding cycle, and can be used
to clean up associated resources.
-->
这是个信息性的扩展点。
绑定后插件在 Pod 成功绑定后被调用。这是绑定周期的结尾，可用于清理相关的资源。

<!--
### Unreserve
-->
### Unreserve

<!--
This is an informational extension point. If a Pod was reserved and then
rejected in a later phase, then unreserve plugins will be notified. Unreserve
plugins should clean up state associated with the reserved Pod.
-->
这是个信息性的扩展点。
如果 Pod 被保留，然后在后面的阶段中被拒绝，则 Unreserve 插件将被通知。
Unreserve 插件应该清楚保留 Pod 的相关状态。

<!--
Plugins that use this extension point usually should also use
[Reserve](#reserve).
-->
使用此扩展点的插件通常也使用[Reserve](#reserve)。

<!--
## Plugin API
-->
## 插件 API

<!--
There are two steps to the plugin API. First, plugins must register and get
configured, then they use the extension point interfaces. Extension point
interfaces have the following form.
-->
插件 API 分为两个步骤。首先，插件必须完成注册并配置，然后才能使用扩展点接口。
扩展点接口具有以下形式。

```go
type Plugin interface {
   Name() string
}

type QueueSortPlugin interface {
   Plugin
   Less(*v1.pod, *v1.pod) bool
}

type PreFilterPlugin interface {
   Plugin
   PreFilter(context.Context, *framework.CycleState, *v1.pod) error
}

// ...
```

<!--
# Plugin Configuration
-->
# 插件配置

<!--
You can enable or disable plugins in the scheduler configuration. If you are using
Kubernetes v1.18 or later, most scheduling
[plugins](/docs/reference/scheduling/config/#scheduling-plugins) are in use and
enabled by default.
 -->
你可以在调度器配置中启用或禁用插件。
如果你在使用 Kubernetes v1.18 或更高版本，大部分调度
[插件](/zh/docs/reference/scheduling/config/#scheduling-plugins)
都在使用中且默认启用。

<!--
In addition to default plugins, you can also implement your own scheduling
plugins and get them configured along with default plugins. You can visit
[scheduler-plugins](https://github.com/kubernetes-sigs/scheduler-plugins) for more details.
 -->
除了默认的插件，你还可以实现自己的调度插件并且将它们与默认插件一起配置。
你可以访问[scheduler-plugins](https://github.com/kubernetes-sigs/scheduler-plugins)
了解更多信息。

<!--
If you are using Kubernetes v1.18 or later, you can configure a set of plugins as
a scheduler profile and then define multiple profiles to fit various kinds of workload.
Learn more at [multiple profiles](/docs/reference/scheduling/config/#multiple-profiles).
 -->
如果你正在使用 Kubernetes v1.18 或更高版本，你可以将一组插件设置为
一个调度器配置文件，然后定义不同的配置文件来满足各类工作负载。
了解更多关于[多配置文件](/zh/docs/reference/scheduling/config/#multiple-profiles)。
