---
title: 控制节点上的 CPU 管理策略
content_type: task
---
<!--
title: Control CPU Management Policies on the Node
reviewers:
- sjenning
- ConnorDoyle
- balajismaniam
content_type: task
-->

<!-- overview -->

{{< feature-state for_k8s_version="v1.12" state="beta" >}}

<!--
Kubernetes keeps many aspects of how pods execute on nodes abstracted
from the user. This is by design.  However, some workloads require
stronger guarantees in terms of latency and/or performance in order to operate
acceptably. The kubelet provides methods to enable more complex workload
placement policies while keeping the abstraction free from explicit placement
directives.
-->
按照设计，Kubernetes 对 pod 执行相关的很多方面进行了抽象，使得用户不必关心。
然而，为了正常运行，有些工作负载要求在延迟和/或性能方面有更强的保证。
为此，kubelet 提供方法来实现更复杂的负载放置策略，同时保持抽象，避免显式的放置指令。

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}

<!-- steps -->

<!--
## CPU Management Policies

By default, the kubelet uses [CFS quota](https://en.wikipedia.org/wiki/Completely_Fair_Scheduler)
to enforce pod CPU limits.  When the node runs many CPU-bound pods,
the workload can move to different CPU cores depending on
whether the pod is throttled and which CPU cores are available at
scheduling time.  Many workloads are not sensitive to this migration and thus
work fine without any intervention.
-->
## CPU 管理策略

默认情况下，kubelet 使用 [CFS 配额](https://en.wikipedia.org/wiki/Completely_Fair_Scheduler)
来执行 Pod 的 CPU 约束。
当节点上运行了很多 CPU 密集的 Pod 时，工作负载可能会迁移到不同的 CPU 核，
这取决于调度时 Pod 是否被扼制，以及哪些 CPU 核是可用的。
许多工作负载对这种迁移不敏感，因此无需任何干预即可正常工作。

<!--
However, in workloads where CPU cache affinity and scheduling latency
significantly affect workload performance, the kubelet allows alternative CPU
management policies to determine some placement preferences on the node.
-->
然而，有些工作负载的性能明显地受到 CPU 缓存亲和性以及调度延迟的影响。
对此，kubelet 提供了可选的 CPU 管理策略，来确定节点上的一些分配偏好。

<!--
### Configuration

The CPU Manager policy is set with the `-cpu-manager-policy` kubelet
option. There are two supported policies:
-->
### 配置

CPU 管理策略通过 kubelet 参数 `--cpu-manager-policy` 来指定。支持两种策略：

<!--
* `none`: the default, which represents the existing scheduling behavior.
* `static`: allows pods with certain resource characteristics to be
  granted increased CPU affinity and exclusivity on the node.
-->
* `none`: 默认策略，表示现有的调度行为。
* `static`: 允许为节点上具有某些资源特征的 pod 赋予增强的 CPU 亲和性和独占性。

<!--
The CPU manager periodically writes resource updates through the CRI in
order to reconcile in-memory CPU assignments with cgroupfs. The reconcile
frequency is set through a new Kubelet configuration value
`-cpu-manager-reconcile-period`. If not specified, it defaults to the same
duration as `-node-status-update-frequency`.
-->
CPU 管理器定期通过 CRI 写入资源更新，以保证内存中 CPU 分配与 cgroupfs 一致。
同步频率通过新增的 Kubelet 配置参数 `--cpu-manager-reconcile-period` 来设置。
如果不指定，默认与 `--node-status-update-frequency` 的周期相同。

<!--
### None policy

The `none` policy explicitly enables the existing default CPU
affinity scheme, providing no affinity beyond what the OS scheduler does
automatically.  Limits on CPU usage for
[Guaranteed pods](/docs/tasks/configure-pod-container/quality-service-pod/) and
[Burstable pods](/docs/tasks/configure-pod-container/quality-service-pod/)
are enforced using CFS quota.
-->
### none 策略

`none` 策略显式地启用现有的默认 CPU 亲和方案，不提供操作系统调度器默认行为之外的亲和性策略。
通过 CFS 配额来实现 [Guaranteed pods](/zh/docs/tasks/configure-pod-container/quality-service-pod/)
的 CPU 使用限制。

<!--
### Static policy

The `static` policy allows containers in `Guaranteed` pods with integer CPU
`requests` access to exclusive CPUs on the node. This exclusivity is enforced
using the [cpuset cgroup controller](https://www.kernel.org/doc/Documentation/cgroup-v1/cpusets.txt).
-->
### static 策略

`static` 策略针对具有整数型 CPU `requests` 的 `Guaranteed` Pod ，它允许该类 Pod
中的容器访问节点上的独占 CPU 资源。这种独占性是使用
[cpuset cgroup 控制器](https://www.kernel.org/doc/Documentation/cgroup-v1/cpusets.txt) 来实现的。

<!--
System services such as the container runtime and the kubelet itself can continue to run on these exclusive CPUs.  The exclusivity only extends to other pods.
-->
{{< note >}}
诸如容器运行时和 kubelet 本身的系统服务可以继续在这些独占 CPU 上运行。独占性仅针对其他 Pod。
{{< /note >}}

<!--
CPU Manager doesn't support offlining and onlining of
CPUs at runtime. Also, if the set of online CPUs changes on the node,
the node must be drained and CPU manager manually reset by deleting the
state file `cpu_manager_state` in the kubelet root directory.
-->
{{< note >}}
CPU 管理器不支持运行时下线和上线 CPUs。此外，如果节点上的在线 CPUs 集合发生变化，
则必须驱逐节点上的 Pod，并通过删除 kubelet 根目录中的状态文件 `cpu_manager_state`
来手动重置 CPU 管理器。
{{< /note >}}

<!--
This policy manages a shared pool of CPUs that initially contains all CPUs in the
node. The amount of exclusively allocatable CPUs is equal to the total
number of CPUs in the node minus any CPU reservations by the kubelet `--kube-reserved` or
`--system-reserved` options. From 1.17, the CPU reservation list can be specified
explicitly by kubelet `--reserved-cpus` option. The explicit CPU list specified by
`--reserved-cpus` takes precedence over the CPU reservation specified by
`--kube-reserved` and `--system-reserved`. CPUs reserved by these options are taken, in
integer quantity, from the initial shared pool in ascending order by physical
core ID.  This shared pool is the set of CPUs on which any containers in
`BestEffort` and `Burstable` pods run. Containers in `Guaranteed` pods with fractional
CPU `requests` also run on CPUs in the shared pool. Only containers that are
both part of a `Guaranteed` pod and have integer CPU `requests` are assigned
exclusive CPUs.
--->
该策略管理一个共享 CPU 资源池，最初，该资源池包含节点上所有的 CPU 资源。可用
的独占性 CPU 资源数量等于节点的 CPU 总量减去通过 `--kube-reserved` 或 `--system-reserved` 参数保留的 CPU 。从1.17版本开始，CPU保留列表可以通过 kublet 的 '--reserved-cpus' 参数显式地设置。
通过 '--reserved-cpus' 指定的显式CPU列表优先于使用 '--kube-reserved' 和 '--system-reserved' 参数指定的保留CPU。 通过这些参数预留的 CPU 是以整数方式，按物理内
核 ID 升序从初始共享池获取的。 共享池是 `BestEffort` 和 `Burstable` pod 运行
的 CPU 集合。`Guaranteed` pod 中的容器，如果声明了非整数值的 CPU `requests` ，也将运行在共享池的 CPU 上。只有 `Guaranteed` pod 中，指定了整数型 CPU `requests` 的容器，才会被分配独占 CPU 资源。

<!--
The kubelet requires a CPU reservation greater than zero be made
using either `--kube-reserved` and/or `--system-reserved`  or `--reserved-cpus` when the static
policy is enabled. This is because zero CPU reservation would allow the shared
pool to become empty.
--->
{{< note >}}
当启用 static 策略时，要求使用 `--kube-reserved` 和/或 `--system-reserved` 或
`--reserved-cpus` 来保证预留的 CPU 值大于零。
这是因为零预留 CPU 值可能使得共享池变空。
{{< /note >}}

<!--
As `Guaranteed` pods whose containers fit the requirements for being statically
assigned are scheduled to the node, CPUs are removed from the shared pool and
placed in the cpuset for the container. CFS quota is not used to bound
the CPU usage of these containers as their usage is bound by the scheduling domain
itself. In others words, the number of CPUs in the container cpuset is equal to the integer
CPU `limit` specified in the pod spec. This static assignment increases CPU
affinity and decreases context switches due to throttling for the CPU-bound
workload.

Consider the containers in the following pod specs:
-->
当 `Guaranteed` Pod 调度到节点上时，如果其容器符合静态分配要求，
相应的 CPU 会被从共享池中移除，并放置到容器的 cpuset 中。
因为这些容器所使用的 CPU 受到调度域本身的限制，所以不需要使用 CFS 配额来进行 CPU 的绑定。
换言之，容器 cpuset  中的 CPU 数量与 Pod 规约中指定的整数型 CPU `limit` 相等。
这种静态分配增强了 CPU 亲和性，减少了 CPU 密集的工作负载在节流时引起的上下文切换。

考虑以下 Pod 规格的容器：

```yaml
spec:
  containers:
  - name: nginx
    image: nginx
```

<!--
This pod runs in the `BestEffort` QoS class because no resource `requests` or
`limits` are specified. It runs in the shared pool.
-->
该 Pod 属于 `BestEffort` QoS 类型，因为其未指定 `requests` 或 `limits` 值。
所以该容器运行在共享 CPU 池中。

```yaml
spec:
  containers:
  - name: nginx
    image: nginx
    resources:
      limits:
        memory: "200Mi"
      requests:
        memory: "100Mi"
```

<!--
This pod runs in the `Burstable` QoS class because resource `requests` do not
equal `limits` and the `cpu` quantity is not specified. It runs in the shared
pool.
-->
该 Pod 属于 `Burstable` QoS 类型，因为其资源 `requests` 不等于 `limits`，且未指定 `cpu` 数量。
所以该容器运行在共享 CPU 池中。

```yaml
spec:
  containers:
  - name: nginx
    image: nginx
    resources:
      limits:
        memory: "200Mi"
        cpu: "2"
      requests:
        memory: "100Mi"
        cpu: "1"
```

<!--
This pod runs in the `Burstable` QoS class because resource `requests` do not
equal `limits`. It runs in the shared pool.
-->
该 pod 属于 `Burstable` QoS 类型，因为其资源 `requests` 不等于 `limits`。
所以该容器运行在共享 CPU 池中。

```yaml
spec:
  containers:
  - name: nginx
    image: nginx
    resources:
      limits:
        memory: "200Mi"
        cpu: "2"
      requests:
        memory: "200Mi"
        cpu: "2"
```

<!--
This pod runs in the `Guaranteed` QoS class because `requests` are equal to `limits`.
And the container's resource limit for the CPU resource is an integer greater than
or equal to one. The `nginx` container is granted 2 exclusive CPUs.
-->
该 Pod 属于 `Guaranteed` QoS 类型，因为其 `requests` 值与 `limits`相等。
同时，容器对 CPU 资源的限制值是一个大于或等于 1 的整数值。
所以，该 `nginx` 容器被赋予 2 个独占 CPU。

```yaml
spec:
  containers:
  - name: nginx
    image: nginx
    resources:
      limits:
        memory: "200Mi"
        cpu: "1.5"
      requests:
        memory: "200Mi"
        cpu: "1.5"
```

<!--
This pod runs in the `Guaranteed` QoS class because `requests` are equal to `limits`.
But the container's resource limit for the CPU resource is a fraction. It runs in
the shared pool.
-->
该 Pod 属于 `Guaranteed` QoS 类型，因为其 `requests` 值与 `limits`相等。
但是容器对 CPU 资源的限制值是一个小数。所以该容器运行在共享 CPU 池中。

```yaml
spec:
  containers:
  - name: nginx
    image: nginx
    resources:
      limits:
        memory: "200Mi"
        cpu: "2"
```

<!--
This pod runs in the `Guaranteed` QoS class because only `limits` are specified
and `requests` are set equal to `limits` when not explicitly specified. And the
container's resource limit for the CPU resource is an integer greater than or
equal to one. The `nginx` container is granted 2 exclusive CPUs.
-->
该 Pod 属于 `Guaranteed` QoS 类型，因其指定了 `limits` 值，同时当未显式指定时，
`requests` 值被设置为与 `limits` 值相等。
同时，容器对 CPU 资源的限制值是一个大于或等于 1 的整数值。
所以，该 `nginx` 容器被赋予 2 个独占 CPU。

