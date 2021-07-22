---
title: DaemonSet
content_type: concept
weight: 50
---

<!--
title: DaemonSet
content_type: concept
weight: 50
--->

<!-- overview -->

<!--
A _DaemonSet_ ensures that all (or some) Nodes run a copy of a Pod.  As nodes are added to the
cluster, Pods are added to them.  As nodes are removed from the cluster, those Pods are garbage
collected.  Deleting a DaemonSet will clean up the Pods it created.
--->
_DaemonSet_ 确保全部（或者某些）节点上运行一个 Pod 的副本。
当有节点加入集群时， 也会为他们新增一个 Pod 。
当有节点从集群移除时，这些 Pod 也会被回收。删除 DaemonSet 将会删除它创建的所有 Pod。

<!--
Some typical uses of a DaemonSet are:

- running a cluster storage daemon on every node
- running a logs collection daemon on every node
- running a node monitoring daemon on every node
-->
DaemonSet 的一些典型用法：

- 在每个节点上运行集群守护进程
- 在每个节点上运行日志收集守护进程
- 在每个节点上运行监控守护进程

<!--
In a simple case, one DaemonSet, covering all nodes, would be used for each type of daemon.
A more complex setup might use multiple DaemonSets for a single type of daemon, but with
different flags and/or different memory and cpu requests for different hardware types.
-->
一种简单的用法是为每种类型的守护进程在所有的节点上都启动一个 DaemonSet。
一个稍微复杂的用法是为同一种守护进程部署多个 DaemonSet；每个具有不同的标志，
并且对不同硬件类型具有不同的内存、CPU 要求。

<!-- body -->

<!--
## Writing a DaemonSet Spec

### Create a DaemonSet
-->
## 编写 DaemonSet Spec 

### 创建 DaemonSet

<!--
You can describe a DaemonSet in a YAML file. For example, the `daemonset.yaml` file below describes a DaemonSet that runs the fluentd-elasticsearch Docker image:
-->
你可以在 YAML 文件中描述 DaemonSet。
例如，下面的 daemonset.yaml 文件描述了一个运行 fluentd-elasticsearch Docker 镜像的 DaemonSet：

{{< codenew file="controllers/daemonset.yaml" >}}

<!--
Create a DaemonSet based on the YAML file:
-->
基于 YAML 文件创建 DaemonSet：

```
kubectl apply -f https://k8s.io/examples/controllers/daemonset.yaml
```

<!--
### Required Fields

As with all other Kubernetes config, a DaemonSet needs `apiVersion`, `kind`, and `metadata` fields.  For
general information about working with config files, see
 [running stateless applications](/docs/tasks/run-application/run-stateless-application-deployment/),
[configuring containers](/docs/tasks/), and [object management using kubectl](/docs/concepts/overview/working-with-objects/object-management/) documents.

The name of a DaemonSet object must be a valid
[DNS subdomain name](/docs/concepts/overview/working-with-objects/names#dns-subdomain-names).

A DaemonSet also needs a [`.spec`](https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status) section.
-->
### 必需字段

和所有其他 Kubernetes 配置一样，DaemonSet 需要 `apiVersion`、`kind` 和 `metadata` 字段。
有关配置文件的基本信息，参见
[部署应用](/zh/docs/tasks/run-application/run-stateless-application-deployment/)、
[配置容器](/zh/docs/tasks/)和
[使用 kubectl 进行对象管理](/zh/docs/concepts/overview/working-with-objects/object-management/)
文档。

DaemonSet 对象的名称必须是一个合法的
[DNS 子域名](/zh/docs/concepts/overview/working-with-objects/names#dns-subdomain-names)。

DaemonSet 也需要一个 [`.spec`](https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status) 配置段。

<!--
### Pod Template

The `.spec.template` is one of the required fields in `.spec`.

The `.spec.template` is a [pod template](/docs/concepts/workloads/pods/pod-overview/#pod-templates). It has exactly the same schema as a [Pod](/docs/concepts/workloads/pods/pod/), except it is nested and does not have an `apiVersion` or `kind`.

In addition to required fields for a Pod, a Pod template in a DaemonSet has to specify appropriate
labels (see [pod selector](#pod-selector)).

A Pod Template in a DaemonSet must have a [`RestartPolicy`](/docs/concepts/workloads/pods/pod-lifecycle/#restart-policy)
 equal to `Always`, or be unspecified, which defaults to `Always`.
-->
### Pod 模板   {#pod-template}

`.spec` 中唯一必需的字段是 `.spec.template`。

`.spec.template` 是一个 [Pod 模板](/zh/docs/concepts/workloads/pods/#pod-templates)。
除了它是嵌套的，因而不具有 `apiVersion` 或 `kind` 字段之外，它与
{{< glossary_tooltip text="Pod" term_id="pod" >}} 具有相同的 schema。

除了 Pod 必需字段外，在 DaemonSet 中的 Pod 模板必须指定合理的标签（查看 [Pod 选择算符](#pod-selector)）。

在 DaemonSet 中的 Pod 模板必须具有一个值为 `Always` 的
[`RestartPolicy`](/zh/docs/concepts/workloads/pods/pod-lifecycle/#restart-policy)。
当该值未指定时，默认是 `Always`。

<!--
### Pod Selector

The `.spec.selector` field is a pod selector.  It works the same as the `.spec.selector` of
a [Job](/docs/concepts/jobs/run-to-completion-finite-workloads/).

As of Kubernetes 1.8, you must specify a pod selector that matches the labels of the
`.spec.template`. The pod selector will no longer be defaulted when left empty. Selector
defaulting was not compatible with `kubectl apply`. Also, once a DaemonSet is created,
its `.spec.selector` can not be mutated. Mutating the pod selector can lead to the
unintentional orphaning of Pods, and it was found to be confusing to users.
-->
### Pod 选择算符     {#pod-selector}

`.spec.selector` 字段表示 Pod 选择算符，它与
[Job](/zh/docs/concepts/workloads/controllers/job/) 的 `.spec.selector` 的作用是相同的。

从 Kubernetes 1.8 开始，您必须指定与 `.spec.template` 的标签匹配的 Pod 选择算符。
用户不指定 Pod 选择算符时，该字段不再有默认值。
选择算符的默认值生成结果与 `kubectl apply` 不兼容。 
此外，一旦创建了 DaemonSet，它的 `.spec.selector` 就不能修改。
修改 Pod 选择算符可能导致 Pod 意外悬浮，并且这对用户来说是费解的。

<!--
The `.spec.selector` is an object consisting of two fields:
-->
`spec.selector` 是一个对象，如下两个字段组成：

<!--
* `matchLabels` - works the same as the `.spec.selector` of a [ReplicationController](/docs/concepts/workloads/controllers/replicationcontroller/).
* `matchExpressions` - allows to build more sophisticated selectors by specifying key,
  list of values and an operator that relates the key and values.
-->
* `matchLabels` - 与 [ReplicationController](/zh/docs/concepts/workloads/controllers/replicationcontroller/)
  的 `.spec.selector` 的作用相同。
* `matchExpressions` - 允许构建更加复杂的选择器，可以通过指定 key、value
  列表以及将 key 和 value 列表关联起来的 operator。

<!--
When the two are specified the result is ANDed.
-->
当上述两个字段都指定时，结果会按逻辑与（AND）操作处理。

<!--
If the `.spec.selector` is specified, it must match the `.spec.template.metadata.labels`. Config with these not matching will be rejected by the API.
-->
如果指定了 `.spec.selector`，必须与 `.spec.template.metadata.labels` 相匹配。
如果与后者不匹配，则 DeamonSet 会被 API 拒绝。

<!--
### Running Pods on Only Some Nodes

If you specify a `.spec.template.spec.nodeSelector`, then the DaemonSet controller will
create Pods on nodes which match that [node
selector](/docs/concepts/configuration/assign-pod-node/). Likewise if you specify a `.spec.template.spec.affinity`,
then DaemonSet controller will create Pods on nodes which match that [node affinity](/docs/concepts/configuration/assign-pod-node/).
If you do not specify either, then the DaemonSet controller will create Pods on all nodes.
-->
### 仅在某些节点上运行 Pod

如果指定了 `.spec.template.spec.nodeSelector`，DaemonSet 控制器将在能够与
[Node 选择算符](/zh/docs/concepts/scheduling-eviction/assign-pod-node/) 匹配的节点上创建 Pod。
类似这种情况，可以指定 `.spec.template.spec.affinity`，之后 DaemonSet 控制器
将在能够与[节点亲和性](/zh/docs/concepts/scheduling-eviction/assign-pod-node/)
匹配的节点上创建 Pod。
如果根本就没有指定，则 DaemonSet Controller 将在所有节点上创建 Pod。

<!--
## How Daemon Pods are Scheduled

### Scheduled by default scheduler
-->
## Daemon Pods 是如何被调度的

### 通过默认调度器调度

{{< feature-state state="stable" for-kubernetes-version="1.17" >}}

<!--
A DaemonSet ensures that all eligible nodes run a copy of a Pod. Normally, the
node that a Pod runs on is selected by the Kubernetes scheduler. However,
DaemonSet pods are created and scheduled by the DaemonSet controller instead.
That introduces the following issues:

 * Inconsistent Pod behavior: Normal Pods waiting to be scheduled are created
   and in `Pending` state, but DaemonSet pods are not created in `Pending`
   state. This is confusing to the user.
 * [Pod preemption](/docs/concepts/configuration/pod-priority-preemption/)
   is handled by default scheduler. When preemption is enabled, the DaemonSet controller
   will make scheduling decisions without considering pod priority and preemption.
-->
DaemonSet 确保所有符合条件的节点都运行该 Pod 的一个副本。
通常，运行 Pod 的节点由 Kubernetes 调度器选择。
不过，DaemonSet Pods 由 DaemonSet 控制器创建和调度。这就带来了以下问题：

* Pod 行为的不一致性：正常 Pod 在被创建后等待调度时处于 `Pending` 状态，
  DaemonSet Pods 创建后不会处于 `Pending` 状态下。这使用户感到困惑。
* [Pod 抢占](/zh/docs/concepts/configuration/pod-priority-preemption/)
  由默认调度器处理。启用抢占后，DaemonSet 控制器将在不考虑 Pod 优先级和抢占
  的情况下制定调度决策。

<!--
`ScheduleDaemonSetPods` allows you to schedule DaemonSets using the default
scheduler instead of the DaemonSet controller, by adding the `NodeAffinity` term
to the DaemonSet pods, instead of the `.spec.nodeName` term. The default
scheduler is then used to bind the pod to the target host. If node affinity of
the DaemonSet pod already exists, it is replaced. The DaemonSet controller only
performs these operations when creating or modifying DaemonSet pods, and no
changes are made to the `spec.template` of the DaemonSet.
-->
`ScheduleDaemonSetPods` 允许您使用默认调度器而不是 DaemonSet 控制器来调度 DaemonSets，
方法是将 `NodeAffinity` 条件而不是 `.spec.nodeName` 条件添加到 DaemonSet Pods。
默认调度器接下来将 Pod 绑定到目标主机。
如果 DaemonSet Pod 的节点亲和性配置已存在，则被替换。
DaemonSet 控制器仅在创建或修改 DaemonSet Pod 时执行这些操作，
并且不会更改 DaemonSet 的 `spec.template`。

```yaml
nodeAffinity:
  requiredDuringSchedulingIgnoredDuringExecution:
    nodeSelectorTerms:
    - matchFields:
      - key: metadata.name
        operator: In
        values:
        - target-host-name
```

<!--
In addition, `node.kubernetes.io/unschedulable:NoSchedule` toleration is added
automatically to DaemonSet Pods. The default scheduler ignores
`unschedulable` Nodes when scheduling DaemonSet Pods.
-->
此外，系统会自动添加 `node.kubernetes.io/unschedulable：NoSchedule` 容忍度到
DaemonSet Pods。在调度 DaemonSet Pod 时，默认调度器会忽略 `unschedulable` 节点。

<!--
### Taints and Tolerations

Although Daemon Pods respect
[taints and tolerations](/docs/concepts/configuration/taint-and-toleration),
the following tolerations are added to DaemonSet Pods automatically according to
the related features.
-->
### 污点和容忍度   {#taint-and-toleration}

尽管 Daemon Pods 遵循[污点和容忍度](/zh/docs/concepts/scheduling-eviction/taint-and-toleration)
规则，根据相关特性，控制器会自动将以下容忍度添加到 DaemonSet Pod：

| 容忍度键名                               | 效果       | 版本    | 描述                                                         |
| ---------------------------------------- | ---------- | ------- | ------------------------------------------------------------ |
| `node.kubernetes.io/not-ready`           | NoExecute  | 1.13+   | 当出现类似网络断开的情况导致节点问题时，DaemonSet Pod 不会被逐出。 |
| `node.kubernetes.io/unreachable`         | NoExecute  | 1.13+   | 当出现类似于网络断开的情况导致节点问题时，DaemonSet Pod 不会被逐出。 |
| `node.kubernetes.io/disk-pressure`       | NoSchedule | 1.8+    | DaemonSet Pod 被默认调度器调度时能够容忍磁盘压力属性。 |
| `node.kubernetes.io/memory-pressure`     | NoSchedule | 1.8+    | DaemonSet Pod 被默认调度器调度时能够容忍内存压力属性。 |
| `node.kubernetes.io/unschedulable`       | NoSchedule | 1.12+   | DaemonSet Pod 能够容忍默认调度器所设置的 `unschedulable` 属性.  |
| `node.kubernetes.io/network-unavailable` | NoSchedule | 1.12+   | DaemonSet 在使用宿主网络时，能够容忍默认调度器所设置的 `network-unavailable` 属性。 |

<!--
## Communicating with Daemon Pods
-->

<!--
Some possible patterns for communicating with Pods in a DaemonSet are:

- **Push**: Pods in the DaemonSet are configured to send updates to another service, such
  as a stats database.  They do not have clients.
- **NodeIP and Known Port**: Pods in the DaemonSet can use a `hostPort`, so that the pods are reachable via the node IPs.  Clients know the list of node IPs somehow, and know the port by convention.
- **DNS**: Create a [headless service](/docs/concepts/services-networking/service/#headless-services) with the same pod selector,
  and then discover DaemonSets using the `endpoints` resource or retrieve multiple A records from
  DNS.
- **Service**: Create a service with the same Pod selector, and use the service to reach a
  daemon on a random node. (No way to reach specific node.)
-->
## 与 Daemon Pods 通信

与 DaemonSet 中的 Pod 进行通信的几种可能模式如下：

- **推送（Push）**：配置 DaemonSet 中的 Pod，将更新发送到另一个服务，例如统计数据库。
  这些服务没有客户端。

- **NodeIP 和已知端口**：DaemonSet 中的 Pod 可以使用 `hostPort`，从而可以通过节点 IP
  访问到 Pod。客户端能通过某种方法获取节点 IP 列表，并且基于此也可以获取到相应的端口。

- **DNS**：创建具有相同 Pod 选择算符的
  [无头服务](/zh/docs/concepts/services-networking/service/#headless-services)，
  通过使用 `endpoints` 资源或从 DNS 中检索到多个 A 记录来发现 DaemonSet。

- **Service**：创建具有相同 Pod 选择算符的服务，并使用该服务随机访问到某个节点上的
  守护进程（没有办法访问到特定节点）。

<!--
## Updating a DaemonSet

If node labels are changed, the DaemonSet will promptly add Pods to newly matching nodes and delete
Pods from newly not-matching nodes.

You can modify the Pods that a DaemonSet creates.  However, Pods do not allow all
fields to be updated.  Also, the DaemonSet controller will use the original template the next
time a node (even with the same name) is created.
-->
## 更新 DaemonSet

如果节点的标签被修改，DaemonSet 将立刻向新匹配上的节点添加 Pod，
同时删除不匹配的节点上的 Pod。

你可以修改 DaemonSet 创建的 Pod。不过并非 Pod 的所有字段都可更新。
下次当某节点（即使具有相同的名称）被创建时，DaemonSet 控制器还会使用最初的模板。

<!--
You can delete a DaemonSet.  If you specify `-cascade=orphan` with `kubectl`, then the Pods
will be left on the nodes.  If you subsequently create a new DaemonSet with the same selector,
the new DaemonSet adopts the existing Pods. If any Pods need replacing the DaemonSet replaces
them according to its `updateStrategy`.

You can [perform a rolling update](/docs/tasks/manage-daemon/update-daemon-set/) on a DaemonSet.
-->
您可以删除一个 DaemonSet。如果使用 `kubectl` 并指定 `--cascade=orphan` 选项，
则 Pod 将被保留在节点上。接下来如果创建使用相同选择算符的新 DaemonSet，
新的 DaemonSet 会收养已有的 Pod。
如果有 Pod 需要被替换，DaemonSet 会根据其 `updateStrategy` 来替换。

你可以对 DaemonSet [执行滚动更新](/zh/docs/tasks/manage-daemon/update-daemon-set/)操作。

<!--
## Alternatives to DaemonSet

### Init Scripts
-->
## DaemonSet 的替代方案

### init 脚本

<!--
It is certainly possible to run daemon processes by directly starting them on a node (e.g. using
`init`, `upstartd`, or `systemd`).  This is perfectly fine.  However, there are several advantages to
running such processes via a DaemonSet:

- Ability to monitor and manage logs for daemons in the same way as applications.
- Same config language and tools (e.g. Pod templates, `kubectl`) for daemons and applications.
- Running daemons in containers with resource limits increases isolation between daemons from app
  containers.  However, this can also be accomplished by running the daemons in a container but not in a Pod
  (e.g. start directly via Docker).
-->
直接在节点上启动守护进程（例如使用 `init`、`upstartd` 或 `systemd`）的做法当然是可行的。
不过，基于 DaemonSet 来运行这些进程有如下一些好处：

- 像所运行的其他应用一样，DaemonSet 具备为守护进程提供监控和日志管理的能力。

- 为守护进程和应用所使用的配置语言和工具（如 Pod 模板、`kubectl`）是相同的。

- 在资源受限的容器中运行守护进程能够增加守护进程和应用容器的隔离性。
  然而，这一点也可以通过在容器中运行守护进程但却不在 Pod 中运行之来实现。
  例如，直接基于 Docker 启动。

<!--
### Bare Pods

It is possible to create Pods directly which specify a particular node to run on.  However,
a DaemonSet replaces Pods that are deleted or terminated for any reason, such as in the case of
node failure or disruptive node maintenance, such as a kernel upgrade. For this reason, you should
use a DaemonSet rather than creating individual Pods.
-->
### 裸 Pod

直接创建 Pod并指定其运行在特定的节点上也是可以的。
然而，DaemonSet 能够替换由于任何原因（例如节点失败、例行节点维护、内核升级）
而被删除或终止的 Pod。
由于这个原因，你应该使用 DaemonSet 而不是单独创建 Pod。

<!--
### Static Pods

It is possible to create Pods by writing a file to a certain directory watched by Kubelet.  These
are called [static pods](/docs/tasks/configure-pod-container/static-pod/).
Unlike DaemonSet, static Pods cannot be managed with kubectl
or other Kubernetes API clients.  Static Pods do not depend on the apiserver, making them useful
in cluster bootstrapping cases.  Also, static Pods may be deprecated in the future.
-->
### 静态 Pod

通过在一个指定的、受 `kubelet` 监视的目录下编写文件来创建 Pod 也是可行的。
这类 Pod 被称为[静态 Pod](/zh/docs/tasks/configure-pod-container/static-pod/)。
不像 DaemonSet，静态 Pod 不受 `kubectl` 和其它 Kubernetes API 客户端管理。
静态 Pod 不依赖于 API 服务器，这使得它们在启动引导新集群的情况下非常有用。
此外，静态 Pod 在将来可能会被废弃。

<!--
### Deployments

DaemonSets are similar to [Deployments](/docs/concepts/workloads/controllers/deployment/) in that
they both create Pods, and those Pods have processes which are not expected to terminate (e.g. web servers,
storage servers).

Use a Deployment for stateless services, like frontends, where scaling up and down the
number of replicas and rolling out updates are more important than controlling exactly which host
the Pod runs on.  Use a DaemonSet when it is important that a copy of a Pod always run on
all or certain hosts, and when it needs to start before other Pods.
-->
### Deployments

DaemonSet 与 [Deployments](/zh/docs/concepts/workloads/controllers/deployment/) 非常类似，
它们都能创建 Pod，并且 Pod 中的进程都不希望被终止（例如，Web 服务器、存储服务器）。
建议为无状态的服务使用 Deployments，比如前端服务。
对这些服务而言，对副本的数量进行扩缩容、平滑升级，比精确控制 Pod 运行在某个主机上要重要得多。
当需要 Pod 副本总是运行在全部或特定主机上，并需要它们先于其他 Pod 启动时，
应该使用 DaemonSet。

