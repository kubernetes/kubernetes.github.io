---
title: 节点压力驱逐
content_type: concept
weight: 60
---
<!-- 
title: Node-pressure Eviction
content_type: concept
weight: 60 
-->

{{<glossary_definition term_id="node-pressure-eviction" length="short">}}</br>

<!-- 
The {{<glossary_tooltip term_id="kubelet" text="kubelet">}} monitors resources 
like CPU, memory, disk space, and filesystem inodes on your cluster's nodes. 
When one or more of these resources reach specific consumption levels, the 
kubelet can proactively fail one or more pods on the node to reclaim resources
and prevent starvation. 

During a node-pressure eviction, the kubelet sets the `PodPhase` for the
selected pods to `Failed`. This terminates the pods. 

Node-pressure eviction is not the same as 
[API-initiated eviction](/docs/concepts/scheduling-eviction/api-eviction/).
-->
{{<glossary_tooltip term_id="kubelet" text="kubelet">}}
监控集群节点的 CPU、内存、磁盘空间和文件系统的 inode 等资源。
当这些资源中的一个或者多个达到特定的消耗水平，
kubelet 可以主动地使节点上一个或者多个 Pod 失效，以回收资源防止饥饿。

在节点压力驱逐期间，kubelet 将所选 Pod 的 `PodPhase` 设置为 `Failed`。这将终止 Pod。

节点压力驱逐不同于 [API 发起的驱逐](/zh/docs/concepts/scheduling-eviction/api-eviction/)。

<!-- 
The kubelet does not respect your configured `PodDisruptionBudget` or the pod's
`terminationGracePeriodSeconds`. If you use [soft eviction thresholds](#soft-eviction-thresholds),
the kubelet respects your configured `eviction-max-pod-grace-period`. If you use
[hard eviction thresholds](#hard-eviction-thresholds), it uses a `0s` grace period for termination.

If the pods are managed by a {{< glossary_tooltip text="workload" term_id="workload" >}}
resource (such as {{< glossary_tooltip text="StatefulSet" term_id="statefulset" >}}
or {{< glossary_tooltip text="Deployment" term_id="deployment" >}}) that
replaces failed pods, the control plane or `kube-controller-manager` creates new 
pods in place of the evicted pods.
-->
kubelet 并不理会你配置的 `PodDisruptionBudget` 或者是 Pod 的 `terminationGracePeriodSeconds`。
如果你使用了[软驱逐条件](#soft-eviction-thresholds)，kubelet 会考虑你所配置的
`eviction-max-pod-grace-period`。
如果你使用了[硬驱逐条件](#hard-eviction-thresholds)，它使用 `0s` 宽限期来终止 Pod。

如果 Pod 是由替换失败 Pod 的{{< glossary_tooltip text="工作负载" term_id="workload" >}}资源
（例如 {{< glossary_tooltip text="StatefulSet" term_id="statefulset" >}}
或者 {{< glossary_tooltip text="Deployment" term_id="deployment" >}}）管理，
则控制平面或 `kube-controller-manager` 会创建新的 Pod 来代替被驱逐的 Pod。

{{<note>}}
<!-- 
The kubelet attempts to [reclaim node-level resources](#reclaim-node-resources)
before it terminates end-user pods. For example, it removes unused container
images when disk resources are starved.
-->
kubelet 在终止最终用户 Pod 之前会尝试[回收节点级资源](#reclaim-node-resources)。
例如，它会在磁盘资源不足时删除未使用的容器镜像。
{{</note>}}

<!-- 
The kubelet uses various parameters to make eviction decisions, like the following:

  * Eviction signals
  * Eviction thresholds
  * Monitoring intervals
-->
kubelet 使用各种参数来做出驱逐决定，如下所示：

  * 驱逐信号
  * 驱逐条件
  * 监控间隔

<!-- 
### Eviction signals {#eviction-signals}

Eviction signals are the current state of a particular resource at a specific
point in time. Kubelet uses eviction signals to make eviction decisions by
comparing the signals to eviction thresholds, which are the minimum amount of 
the resource that should be available on the node. 

Kubelet uses the following eviction signals:
-->
### 驱逐信号 {#eviction-signals}

驱逐信号是特定资源在特定时间点的当前状态。
kubelet 使用驱逐信号，通过将信号与驱逐条件进行比较来做出驱逐决定，
驱逐条件是节点上应该可用资源的最小量。

kubelet 使用以下驱逐信号：

| 驱逐信号              | 描述                                                                                   |
|----------------------|---------------------------------------------------------------------------------------|
| `memory.available`   | `memory.available` := `node.status.capacity[memory]` - `node.stats.memory.workingSet` |
| `nodefs.available`   | `nodefs.available` := `node.stats.fs.available`                                       |
| `nodefs.inodesFree`  | `nodefs.inodesFree` := `node.stats.fs.inodesFree`                                     |
| `imagefs.available`  | `imagefs.available` := `node.stats.runtime.imagefs.available`                         |
| `imagefs.inodesFree` | `imagefs.inodesFree` := `node.stats.runtime.imagefs.inodesFree`                       |
| `pid.available`      | `pid.available` := `node.stats.rlimit.maxpid` - `node.stats.rlimit.curproc`           |

<!-- 
In this table, the `Description` column shows how kubelet gets the value of the
signal. Each signal supports either a percentage or a literal value. Kubelet 
calculates the percentage value relative to the total capacity associated with
the signal. 
-->
在上表中，`描述`列显示了 kubelet 如何获取信号的值。每个信号支持百分比值或者是字面值。
kubelet 计算相对于与信号有关的总量的百分比值。

<!--
The value for `memory.available` is derived from the cgroupfs instead of tools
like `free -m`. This is important because `free -m` does not work in a
container, and if users use the [node
allocatable](/docs/tasks/administer-cluster/reserve-compute-resources/#node-allocatable) feature, out of resource decisions
are made local to the end user Pod part of the cgroup hierarchy as well as the
root node. This [script](/examples/admin/resource/memory-available.sh)
reproduces the same set of steps that the kubelet performs to calculate
`memory.available`. The kubelet excludes inactive_file (i.e. # of bytes of
file-backed memory on inactive LRU list) from its calculation as it assumes that
memory is reclaimable under pressure.  
-->
`memory.available` 的值来自 cgroupfs，而不是像 `free -m` 这样的工具。
这很重要，因为 `free -m` 在容器中不起作用，如果用户使用
[节点可分配资源](/zh/docs/tasks/administer-cluster/reserve-compute-resources/#node-allocatable)
这一功能特性，资源不足的判定是基于 CGroup 层次结构中的用户 Pod 所处的局部及 CGroup 根节点作出的。
这个[脚本](/zh/examples/admin/resource/memory-available.sh)
重现了 kubelet 为计算 `memory.available` 而执行的相同步骤。
kubelet 在其计算中排除了 inactive_file（即非活动 LRU 列表上基于文件来虚拟的内存的字节数），
因为它假定在压力下内存是可回收的。

<!--
The kubelet supports the following filesystem partitions:

1. `nodefs`: The node's main filesystem, used for local disk volumes, emptyDir,
   log storage, and more. For example, `nodefs` contains `/var/lib/kubelet/`. 
1. `imagefs`: An optional filesystem that container runtimes use to store container
   images and container writable layers.

Kubelet auto-discovers these filesystems and ignores other filesystems. Kubelet
does not support other configurations. 
-->
kubelet 支持以下文件系统分区：

1. `nodefs`：节点的主要文件系统，用于本地磁盘卷、emptyDir、日志存储等。
   例如，`nodefs` 包含 `/var/lib/kubelet/`。
1. `imagefs`：可选文件系统，供容器运行时存储容器镜像和容器可写层。

kubelet 会自动发现这些文件系统并忽略其他文件系统。kubelet 不支持其他配置。

{{<note>}}
<!-- 
Some kubelet garbage collection features are deprecated in favor of eviction.
For a list of the deprecated features, see [kubelet garbage collection deprecation](/docs/concepts/cluster-administration/kubelet-garbage-collection/#deprecation).
-->
一些 kubelet 垃圾收集功能已被弃用，以支持驱逐。
有关已弃用功能的列表，请参阅
[kubelet 垃圾收集弃用](/zh/docs/concepts/cluster-administration/kubelet-garbage-collection/#deprecation)。
{{</note>}}

<!-- 
### Eviction thresholds

You can specify custom eviction thresholds for the kubelet to use when it makes
eviction decisions.

Eviction thresholds have the form `[eviction-signal][operator][quantity]`, where:

* `eviction-signal` is the [eviction signal](#eviction-signals) to use.
* `operator` is the [relational operator](https://en.wikipedia.org/wiki/Relational_operator#Standard_relational_operators)
  you want, such as `<` (less than).
* `quantity` is the eviction threshold amount, such as `1Gi`. The value of `quantity`
  must match the quantity representation used by Kubernetes. You can use either
  literal values or percentages (`%`).
-->
### 驱逐条件 {#eviction-thresholds}

你可以为 kubelet 指定自定义驱逐条件，以便在作出驱逐决定时使用。

驱逐条件的形式为 `[eviction-signal][operator][quantity]`，其中：

* `eviction-signal` 是要使用的[驱逐信号](#eviction-signals)。
* `operator` 是你想要的[关系运算符](https://en.wikipedia.org/wiki/Relational_operator#Standard_relational_operators)，
  比如 `<`（小于）。
* `quantity` 是驱逐条件数量，例如 `1Gi`。
  `quantity` 的值必须与 Kubernetes 使用的数量表示相匹配。
  你可以使用文字值或百分比（`%`）。

<!--
For example, if a node has `10Gi` of total memory and you want trigger eviction if
the available memory falls below `1Gi`, you can define the eviction threshold as
either `memory.available<10%` or `memory.available<1Gi`. You cannot use both.

You can configure soft and hard eviction thresholds.  
-->
例如，如果一个节点的总内存为 10Gi 并且你希望在可用内存低于 1Gi 时触发驱逐，
则可以将驱逐条件定义为 `memory.available<10%` 或 `memory.available< 1G`。
你不能同时使用二者。

你可以配置软和硬驱逐条件。

<!--  
#### Soft eviction thresholds {#soft-eviction-thresholds}

A soft eviction threshold pairs an eviction threshold with a required
administrator-specified grace period. The kubelet does not evict pods until the
grace period is exceeded. The kubelet returns an error on startup if there is no
specified grace period. 
-->
#### 软驱逐条件 {#soft-eviction-thresholds}

软驱逐条件将驱逐条件与管理员所必须指定的宽限期配对。
在超过宽限期之前，kubelet 不会驱逐 Pod。
如果没有指定的宽限期，kubelet 会在启动时返回错误。

<!-- 
You can specify both a soft eviction threshold grace period and a maximum
allowed pod termination grace period for kubelet to use during evictions. If you
specify a maximum allowed grace period and the soft eviction threshold is met, 
the kubelet uses the lesser of the two grace periods. If you do not specify a
maximum allowed grace period, the kubelet kills evicted pods immediately without
graceful termination.
-->
你可以既指定软驱逐条件宽限期，又指定 Pod 终止宽限期的上限，，给 kubelet 在驱逐期间使用。
如果你指定了宽限期的上限并且 Pod 满足软驱逐阈条件，则 kubelet 将使用两个宽限期中的较小者。
如果你没有指定宽限期上限，kubelet 会立即杀死被驱逐的 Pod，不允许其体面终止。

<!--  
You can use the following flags to configure soft eviction thresholds:

* `eviction-soft`: A set of eviction thresholds like `memory.available<1.5Gi`
  that can trigger pod eviction if held over the specified grace period.
* `eviction-soft-grace-period`: A set of eviction grace periods like `memory.available=1m30s`
  that define how long a soft eviction threshold must hold before triggering a Pod eviction.
* `eviction-max-pod-grace-period`: The maximum allowed grace period (in seconds)
  to use when terminating pods in response to a soft eviction threshold being met.
-->
你可以使用以下标志来配置软驱逐条件：

* `eviction-soft`：一组驱逐条件，如 `memory.available<1.5Gi`，
  如果驱逐条件持续时长超过指定的宽限期，可以触发 Pod 驱逐。
* `eviction-soft-grace-period`：一组驱逐宽限期，
  如 `memory.available=1m30s`，定义软驱逐条件在触发 Pod 驱逐之前必须保持多长时间。
* `eviction-max-pod-grace-period`：在满足软驱逐条件而终止 Pod 时使用的最大允许宽限期（以秒为单位）。 

<!-- 
#### Hard eviction thresholds {#hard-eviction-thresholds}

A hard eviction threshold has no grace period. When a hard eviction threshold is
met, the kubelet kills pods immediately without graceful termination to reclaim
the starved resource.

You can use the `eviction-hard` flag to configure a set of hard eviction 
thresholds like `memory.available<1Gi`. 
-->
#### 硬驱逐条件 {#hard-eviction-thresholds}

硬驱逐条件没有宽限期。当达到硬驱逐条件时，
kubelet 会立即杀死 pod，而不会正常终止以回收紧缺的资源。

你可以使用 `eviction-hard` 标志来配置一组硬驱逐条件，
例如 `memory.available<1Gi`。

<!-- 
The kubelet has the following default hard eviction thresholds:

* `memory.available<100Mi`
* `nodefs.available<10%`
* `imagefs.available<15%`
* `nodefs.inodesFree<5%` (Linux nodes)
-->
kubelet 具有以下默认硬驱逐条件：

* `memory.available<100Mi`
* `nodefs.available<10%`
* `imagefs.available<15%`
* `nodefs.inodesFree<5%`（Linux 节点）

<!--  
### Eviction monitoring interval

The kubelet evaluates eviction thresholds based on its configured `housekeeping-interval`
which defaults to `10s`.
-->
### 驱逐监测间隔

kubelet 根据其配置的 `housekeeping-interval`（默认为 `10s`）评估驱逐条件。

<!--
### Node conditions {#node-conditions}

The kubelet reports node conditions to reflect that the node is under pressure
because hard or soft eviction threshold is met, independent of configured grace
periods. 
-->
### 节点条件 {#node-conditions}

kubelet 报告节点状况以反映节点处于压力之下，因为满足硬或软驱逐条件，与配置的宽限期无关。

<!--  
The kubelet maps eviction signals to node conditions as follows: 

| Node Condition    | Eviction Signal                                                                       | Description                                                                                                                  |
|-------------------|---------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------|
| `MemoryPressure`  | `memory.available`                                                                    | Available memory on the node has satisfied an eviction threshold                                                             |
| `DiskPressure`    | `nodefs.available`, `nodefs.inodesFree`, `imagefs.available`, or `imagefs.inodesFree` | Available disk space and inodes on either the node's root filesystem or image filesystem has satisfied an eviction threshold |
| `PIDPressure`     | `pid.available`                                                                       | Available processes identifiers on the (Linux) node has fallen below an eviction threshold                                   |

The kubelet updates the node conditions based on the configured 
`--node-status-update-frequency`, which defaults to `10s`.
-->
kubelet 根据下表将驱逐信号映射为节点状况：

| 节点条件 | 驱逐信号 | 描述 |
|---------|--------|------|
| `MemoryPressure` | `memory.available` | 节点上的可用内存已满足驱逐条件 |
| `DiskPressure`   | `nodefs.available`、`nodefs.inodesFree`、`imagefs.available` 或 `imagefs.inodesFree` | 节点的根文件系统或映像文件系统上的可用磁盘空间和 inode 已满足驱逐条件 |
| `PIDPressure`    | `pid.available` | (Linux) 节点上的可用进程标识符已低于驱逐条件 |

kubelet 根据配置的 `--node-status-update-frequency` 更新节点条件，默认为 `10s`。

<!-- 
#### Node condition oscillation

In some cases, nodes oscillate above and below soft eviction thresholds without
holding for the defined grace periods. This causes the reported node condition
to constantly switch between `true` and `false`, leading to bad eviction decisions.

To protect against oscillation, you can use the `eviction-pressure-transition-period`
flag, which controls how long the kubelet must wait before transitioning a node
condition to a different state. The transition period has a default value of `5m`.
-->
#### 节点条件振荡

在某些情况下，节点在软驱逐条件上下振荡，而没有保持定义的宽限期。
这会导致报告的节点条件在 `true` 和 `false` 之间不断切换，从而导致错误的驱逐决策。

为了防止振荡，你可以使用 `eviction-pressure-transition-period` 标志，
该标志控制 kubelet 在将节点条件转换为不同状态之前必须等待的时间。
过渡期的默认值为 `5m`。

<!-- 
### Reclaiming node level resources {#reclaim-node-resources}

The kubelet tries to reclaim node-level resources before it evicts end-user pods.

When a `DiskPressure` node condition is reported, the kubelet reclaims node-level
resources based on the filesystems on the node. 
-->
### 回收节点级资源 {#reclaim-node-resources}

kubelet 在驱逐最终用户 Pod 之前会先尝试回收节点级资源。

当报告 `DiskPressure` 节点状况时，kubelet 会根据节点上的文件系统回收节点级资源。

<!--
#### With `imagefs`

If the node has a dedicated `imagefs` filesystem for container runtimes to use,
the kubelet does the following:

  * If the `nodefs` filesystem meets the eviction threshlds, the kubelet garbage collects
    dead pods and containers. 
  * If the `imagefs` filesystem meets the eviction thresholds, the kubelet
    deletes all unused images.
-->
#### 有 `imagefs`

如果节点有一个专用的 `imagefs` 文件系统供容器运行时使用，kubelet 会执行以下操作：

   * 如果 `nodefs` 文件系统满足驱逐条件，kubelet 垃圾收集死亡 Pod 和容器。
   * 如果 `imagefs` 文件系统满足驱逐条件，kubelet 将删除所有未使用的镜像。

<!-- 
#### Without `imagefs`

If the node only has a `nodefs` filesystem that meets eviction thresholds,
the kubelet frees up disk space in the following order:

1. Garbage collect dead pods and containers
1. Delete unused images
-->
#### 没有 `imagefs`

如果节点只有一个满足驱逐条件的 `nodefs` 文件系统，
kubelet 按以下顺序释放磁盘空间：

1. 对死亡的 Pod 和容器进行垃圾收集
1. 删除未使用的镜像

<!-- 
### Pod selection for kubelet eviction

If the kubelet's attempts to reclaim node-level resources don't bring the eviction
signal below the threshold, the kubelet begins to evict end-user pods. 

The kubelet uses the following parameters to determine pod eviction order:

1. Whether the pod's resource usage exceeds requests
1. [Pod Priority](/docs/concepts/configuration/pod-priority-preemption/)
1. The pod's resource usage relative to requests
-->
### kubelet 驱逐时 Pod 的选择

如果 kubelet 回收节点级资源的尝试没有使驱逐信号低于条件，
则 kubelet 开始驱逐最终用户 Pod。

kubelet 使用以下参数来确定 Pod 驱逐顺序：

1. Pod 的资源使用是否超过其请求
1. [Pod 优先级](/zh/docs/concepts/configuration/pod-priority-preemption/)
1. Pod 相对于请求的资源使用情况

<!-- 
As a result, kubelet ranks and evicts pods in the following order:

1. `BestEffort` or `Burstable` pods where the usage exceeds requests. These pods
   are evicted based on their Priority and then by how much their usage level
   exceeds the request.
1. `Guaranteed` pods and `Burstable` pods where the usage is less than requests
   are evicted last, based on their Priority.
-->
因此，kubelet 按以下顺序排列和驱逐 Pod：

1. 首先考虑资源使用量超过其请求的 `BestEffort` 或 `Burstable` Pod。
   这些 Pod 会根据它们的优先级以及它们的资源使用级别超过其请求的程度被逐出。
1. 资源使用量少于请求量的 `Guaranted` Pod 和 `Burstable` Pod 根据其优先级被最后驱逐。

{{<note>}}
<!-- 
The kubelet does not use the pod's QoS class to determine the eviction order.
You can use the QoS class to estimate the most likely pod eviction order when 
reclaiming resources like memory. QoS does not apply to EphemeralStorage requests,
so the above scenario will not apply if the node is, for example, under `DiskPressure`.
-->
kubelet 不使用 Pod 的 QoS 类来确定驱逐顺序。
在回收内存等资源时，你可以使用 QoS 类来估计最可能的 Pod 驱逐顺序。
QoS 不适用于临时存储（EphemeralStorage）请求，
因此如果节点在 `DiskPressure` 下，则上述场景将不适用。
{{</note>}}

<!-- 
`Guaranteed` pods are guaranteed only when requests and limits are specified for
all the containers and they are equal. These pods will never be evicted because
of another pod's resource consumption. If a system daemon (such as `kubelet`,
`docker`, and `journald`) is consuming more resources than were reserved via 
`system-reserved` or `kube-reserved` allocations, and the node only has
`Guaranteed` or `Burstable` pods using less resources than requests left on it,
then the kubelet must choose to evict one of these pods to preserve node stability
and to limit the impact of resource starvation on other pods. In this case, it
will choose to evict pods of lowest Priority first.
-->
仅当 `Guaranted` Pod 中所有容器都被指定了请求和限制并且二者相等时，才保证 Pod 不被驱逐。
这些 Pod 永远不会因为另一个 Pod 的资源消耗而被驱逐。
如果系统守护进程（例如 `kubelet`、`docker` 和 `journald`）
消耗的资源比通过 `system-reserved` 或 `kube-reserved` 分配保留的资源多，
并且该节点只有 `Guaranteed` 或 `Burstable` Pod 使用的资源少于其上剩余的请求，
那么 kubelet 必须选择驱逐这些 Pod 中的一个以保持节点稳定性并减少资源匮乏对其他 Pod 的影响。 
在这种情况下，它会选择首先驱逐最低优先级的 Pod。

<!--  
When the kubelet evicts pods in response to `inode` or `PID` starvation, it uses
the Priority to determine the eviction order, because `inodes` and `PIDs` have no
requests.

The kubelet sorts pods differently based on whether the node has a dedicated
`imagefs` filesystem:
-->
当 kubelet 因 inode 或 PID 不足而驱逐 pod 时，
它使用优先级来确定驱逐顺序，因为 inode 和 PID 没有请求。

kubelet 根据节点是否具有专用的 `imagefs` 文件系统对 Pod 进行不同的排序：

<!-- 
#### With `imagefs`

If `nodefs` is triggering evictions, the kubelet sorts pods based on `nodefs`
usage (`local volumes + logs of all containers`).

If `imagefs` is triggering evictions, the kubelet sorts pods based on the
writable layer usage of all containers.

#### Without `imagefs`

If `nodefs` is triggering evictions, the kubelet sorts pods based on their total
disk usage (`local volumes + logs & writable layer of all containers`)
-->
#### 有 `imagefs`

如果 `nodefs` 触发驱逐，
kubelet 会根据 `nodefs` 使用情况（`本地卷 + 所有容器的日志`）对 Pod 进行排序。

如果 `imagefs` 触发驱逐，kubelet 会根据所有容器的可写层使用情况对 Pod 进行排序。

#### 没有 `imagefs`

如果 `nodefs` 触发驱逐，
kubelet 会根据磁盘总用量（`本地卷 + 日志和所有容器的可写层`）对 Pod 进行排序。

<!-- 
### Minimum eviction reclaim

In some cases, pod eviction only reclaims a small amount of the starved resource.
This can lead to the kubelet repeatedly hitting the configured eviction thresholds
and triggering multiple evictions. 
-->
### 最小驱逐回收  {#minimum-eviction-reclaim}

在某些情况下，驱逐 Pod 只会回收少量的紧俏资源。
这可能导致 kubelet 反复达到配置的驱逐条件并触发多次驱逐。

<!-- 
You can use the `--eviction-minimum-reclaim` flag or a [kubelet config file](/docs/tasks/administer-cluster/kubelet-config-file/)
to configure a minimum reclaim amount for each resource. When the kubelet notices
that a resource is starved, it continues to reclaim that resource until it
reclaims the quantity you specify. 

For example, the following configuration sets minimum reclaim amounts: 
-->
你可以使用 `--eviction-minimum-reclaim` 标志或
[kubelet 配置文件](/zh/docs/tasks/administer-cluster/kubelet-config-file/)
为每个资源配置最小回收量。
当 kubelet 注意到某个资源耗尽时，它会继续回收该资源，直到回收到你所指定的数量为止。

例如，以下配置设置最小回收量：

```yaml
apiVersion: kubelet.config.k8s.io/v1beta1
kind: KubeletConfiguration
evictionHard:
  memory.available: "500Mi"
  nodefs.available: "1Gi"
  imagefs.available: "100Gi"
evictionMinimumReclaim:
  memory.available: "0Mi"
  nodefs.available: "500Mi"
  imagefs.available: "2Gi"
```

<!-- 
In this example, if the `nodefs.available` signal meets the eviction threshold,
the kubelet reclaims the resource until the signal reaches the threshold of `1Gi`,
and then continues to reclaim the minimum amount of `500Mi` it until the signal
reaches `1.5Gi`. 

Similarly, the kubelet reclaims the `imagefs` resource until the `imagefs.available`
signal reaches `102Gi`. 

The default `eviction-minimum-reclaim` is `0` for all resources.
-->
在这个例子中，如果 `nodefs.available` 信号满足驱逐条件，
kubelet 会回收资源，直到信号达到 `1Gi` 的条件，
然后继续回收至少 `500Mi` 直到信号达到 `1.5Gi`。

类似地，kubelet 会回收 `imagefs` 资源，直到 `imagefs.available` 信号达到 `102Gi`。

对于所有资源，默认的 `eviction-minimum-reclaim` 为 `0`。

<!-- 
### Node out of memory behavior

If the node experiences an out of memory (OOM) event prior to the kubelet
being able to reclaim memory, the node depends on the [oom_killer](https://lwn.net/Articles/391222/)
to respond.

The kubelet sets an `oom_score_adj` value for each container based on the QoS for the pod.
-->
### 节点内存不足行为

如果节点在 kubelet 能够回收内存之前遇到内存不足（OOM）事件，
则节点依赖 [oom_killer](https://lwn.net/Articles/391222/) 来响应。

kubelet 根据 Pod 的服务质量（QoS）为每个容器设置一个 `oom_score_adj` 值。

| 服务质量            | oom_score_adj                                                                     |
|--------------------|-----------------------------------------------------------------------------------|
| `Guaranteed`       | -997                                                                              |
| `BestEffort`       | 1000                                                                              |
| `Burstable`        | min(max(2, 1000 - (1000 * memoryRequestBytes) / machineMemoryCapacityBytes), 999) |

{{<note>}}
<!-- 
The kubelet also sets an `oom_score_adj` value of `-997` for containers in Pods that have
`system-node-critical` {{<glossary_tooltip text="Priority" term_id="pod-priority">}}
-->
kubelet 还将具有 `system-node-critical`
{{<glossary_tooltip text="优先级" term_id="pod-priority">}}
的 Pod 中的容器 `oom_score_adj` 值设为 `-997`。
{{</note>}}

<!-- 
If the kubelet can't reclaim memory before a node experiences OOM, the
`oom_killer` calculates an `oom_score` based on the percentage of memory it's
using on the node, and then adds the `oom_score_adj` to get an effective `oom_score`
for each container. It then kills the container with the highest score.

This means that containers in low QoS pods that consume a large amount of memory
relative to their scheduling requests are killed first.

Unlike pod eviction, if a container is OOM killed, the `kubelet` can restart it 
based on its `RestartPolicy`.
-->
如果 kubelet 在节点遇到 OOM 之前无法回收内存，
则 `oom_killer` 根据它在节点上使用的内存百分比计算 `oom_score`，
然后加上 `oom_score_adj` 得到每个容器有效的 `oom_score`。
然后它会杀死得分最高的容器。

这意味着低 QoS Pod 中相对于其调度请求消耗内存较多的容器，将首先被杀死。

与 Pod 驱逐不同，如果容器被 OOM 杀死，
`kubelet` 可以根据其 `RestartPolicy` 重新启动它。

<!-- 
### Best practices {#node-pressure-eviction-good-practices}

The following sections describe best practices for eviction configuration.
-->
### 最佳实践 {#node-pressure-eviction-good-practices}

以下部分描述了驱逐配置的最佳实践。

<!-- 
#### Schedulable resources and eviction policies

When you configure the kubelet with an eviction policy, you should make sure that
the scheduler will not schedule pods if they will trigger eviction because they
immediately induce memory pressure.
-->
#### 可调度的资源和驱逐策略

当你为 kubelet 配置驱逐策略时，
你应该确保调度程序不会在 Pod 触发驱逐时对其进行调度，因为这类 Pod 会立即引起内存压力。

<!-- 
Consider the following scenario:

* Node memory capacity: `10Gi`
* Operator wants to reserve 10% of memory capacity for system daemons (kernel, `kubelet`, etc.)
* Operator wants to evict Pods at 95% memory utilization to reduce incidence of system OOM.
-->
考虑以下场景：

* 节点内存容量：`10Gi`
* 操作员希望为系统守护进程（内核、`kubelet` 等）保留 10% 的内存容量
* 操作员希望驱逐内存利用率为 95% 的Pod，以减少系统 OOM 的概率。

<!-- 
For this to work, the kubelet is launched as follows:
-->
为此，kubelet 启动设置如下：

```
--eviction-hard=memory.available<500Mi
--system-reserved=memory=1.5Gi
```

<!-- 
In this configuration, the `--system-reserved` flag reserves `1.5Gi` of memory
for the system, which is `10% of the total memory + the eviction threshold amount`. 

The node can reach the eviction threshold if a pod is using more than its request,
or if the system is using more than `1Gi` of memory, which makes the `memory.available`
signal fall below `500Mi` and triggers the threshold. 
-->
在此配置中，`--system-reserved` 标志为系统预留了 `1.5Gi` 的内存，
即 `总内存的 10% + 驱逐条件量`。

如果 Pod 使用的内存超过其请求值或者系统使用的内存超过 `1Gi`，
则节点可以达到驱逐条件，这使得 `memory.available` 信号低于 `500Mi` 并触发条件。

<!-- 
#### DaemonSet

Pod Priority is a major factor in making eviction decisions. If you do not want
the kubelet to evict pods that belong to a `DaemonSet`, give those pods a high
enough `priorityClass` in the pod spec. You can also use a lower `priorityClass`
or the default to only allow `DaemonSet` pods to run when there are enough 
resources.
-->
### DaemonSet

Pod 优先级是做出驱逐决定的主要因素。
如果你不希望 kubelet 驱逐属于 `DaemonSet` 的 Pod，
请在 Pod 规约中为这些 Pod 提供足够高的 `priorityClass`。
你还可以使用优先级较低的 `priorityClass` 或默认配置，
仅在有足够资源时才运行 `DaemonSet` Pod。

<!-- 
### Known issues

The following sections describe known issues related to out of resource handling.
-->
### 已知问题

以下部分描述了与资源不足处理相关的已知问题。

<!-- 
#### kubelet may not observe memory pressure right away

By default, the kubelet polls `cAdvisor` to collect memory usage stats at a
regular interval. If memory usage increases within that window rapidly, the
kubelet may not observe `MemoryPressure` fast enough, and the `OOMKiller`
will still be invoked. 
-->
#### kubelet 可能不会立即观察到内存压力

默认情况下，kubelet 轮询 `cAdvisor` 以定期收集内存使用情况统计信息。
如果该轮询时间窗口内内存使用量迅速增加，kubelet 可能无法足够快地观察到 `MemoryPressure`，
但是 `OOMKiller` 仍将被调用。

<!-- 
You can use the `--kernel-memcg-notification` flag to enable the `memcg`
notification API on the kubelet to get notified immediately when a threshold
is crossed.

If you are not trying to achieve extreme utilization, but a sensible measure of
overcommit, a viable workaround for this issue is to use the `--kube-reserved`
and `--system-reserved` flags to allocate memory for the system. 
-->
你可以使用 `--kernel-memcg-notification`
标志在 kubelet 上启用 `memcg` 通知 API，以便在超过条件时立即收到通知。

如果你不是追求极端利用率，而是要采取合理的过量使用措施，
则解决此问题的可行方法是使用 `--kube-reserved` 和 `--system-reserved` 标志为系统分配内存。

<!-- 
#### active_file memory is not considered as available memory

On Linux, the kernel tracks the number of bytes of file-backed memory on active 
LRU list as the `active_file` statistic. The kubelet treats `active_file` memory
areas as not reclaimable. For workloads that make intensive use of block-backed 
local storage, including ephemeral local storage, kernel-level caches of file 
and block data means that many recently accessed cache pages are likely to be 
counted as `active_file`. If enough of these kernel block buffers are on the 
active LRU list, the kubelet is liable to observe this as high resource use and 
taint the node as experiencing memory pressure - triggering pod eviction.
-->
#### active_file 内存未被视为可用内存

在 Linux 上，内核跟踪活动 LRU 列表上的基于文件所虚拟的内存字节数作为 `active_file` 统计信息。
kubelet 将 `active_file` 内存区域视为不可回收。
对于大量使用块设备形式的本地存储（包括临时本地存储）的工作负载，
文件和块数据的内核级缓存意味着许多最近访问的缓存页面可能被计为 `active_file`。
如果这些内核块缓冲区中在活动 LRU 列表上有足够多，
kubelet 很容易将其视为资源用量过量并为节点设置内存压力污点，从而触发 Pod 驱逐。

<!-- 
For more more details, see [https://github.com/kubernetes/kubernetes/issues/43916](https://github.com/kubernetes/kubernetes/issues/43916)

You can work around that behavior by setting the memory limit and memory request
the same for containers likely to perform intensive I/O activity. You will need 
to estimate or measure an optimal memory limit value for that container.
-->
更多细节请参见 [https://github.com/kubernetes/kubernetes/issues/43916](https://github.com/kubernetes/kubernetes/issues/43916)

你可以通过为可能执行 I/O 密集型活动的容器设置相同的内存限制和内存请求来应对该行为。
你将需要估计或测量该容器的最佳内存限制值。

## {{% heading "whatsnext" %}}

<!-- 
* Learn about [API-initiated Eviction](/docs/concepts/scheduling-eviction/api-eviction/)
* Learn about [Pod Priority and Preemption](/docs/concepts/scheduling-eviction/pod-priority-preemption/)
* Learn about [PodDisruptionBudgets](/docs/tasks/run-application/configure-pdb/)
* Learn about [Quality of Service](/docs/tasks/configure-pod-container/quality-service-pod/) (QoS)
* Check out the [Eviction API](/docs/reference/generated/kubernetes-api/{{<param "version">}}/#create-eviction-pod-v1-core)
-->
* 了解 [API 发起的驱逐](/zh/docs/concepts/scheduling-eviction/api-eviction/)
* 了解 [Pod 优先级和驱逐](/zh/docs/concepts/scheduling-eviction/pod-priority-preemption/)
* 了解 [PodDisruptionBudgets](/docs/tasks/run-application/configure-pdb/)
* 了解[服务质量](/zh/docs/tasks/configure-pod-container/quality-service-pod/)（QoS）
* 查看[驱逐 API](/docs/reference/generated/kubernetes-api/{{<param "version">}}/#create-eviction-pod-v1-core)