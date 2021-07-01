---
title: Pods
content_type: concept
weight: 10
no_list: true
card:
  name: concepts
  weight: 60
---
<!--
reviewers:
- erictune
title: Pods
content_type: concept
weight: 10
no_list: true
card:
  name: concepts
  weight: 60
-->

<!-- overview -->

<!--
_Pods_ are the smallest deployable units of computing that you can create and manage in Kubernetes.

A _Pod_ (as in a pod of whales or pea pod) is a group of one or more
{{< glossary_tooltip text="containers" term_id="container" >}}
with shared storage and network resources, and a specification
for how to run the containers. A Pod's contents are always co-located and
co-scheduled, and run in a shared context. A Pod models an
application-specific "logical host": it contains one or more application
containers which are relatively tightly coupled. 
In non-cloud contexts, applications executed on the same physical or virtual machine are analogous to cloud applications executed on the same logical host.
-->
_Pod_ 是可以在 Kubernetes 中创建和管理的、最小的可部署的计算单元。

_Pod_ （就像在鲸鱼荚或者豌豆荚中）是一组（一个或多个）
{{< glossary_tooltip text="容器" term_id="container" >}}；
这些容器共享存储、网络、以及怎样运行这些容器的声明。
Pod 中的内容总是并置（colocated）的并且一同调度，在共享的上下文中运行。
Pod 所建模的是特定于应用的“逻辑主机”，其中包含一个或多个应用容器，
这些容器是相对紧密的耦合在一起的。
在非云环境中，在相同的物理机或虚拟机上运行的应用类似于
在同一逻辑主机上运行的云应用。

<!--
As well as application containers, a Pod can contain
[init containers](/docs/concepts/workloads/pods/init-containers/) that run
during Pod startup. You can also inject
[ephemeral containers](/docs/concepts/workloads/pods/ephemeral-containers/)
for debugging if your cluster offers this.
-->
除了应用容器，Pod 还可以包含在 Pod 启动期间运行的
[Init 容器](/zh/docs/concepts/workloads/pods/init-containers/)。
你也可以在集群中支持[临时性容器](/zh/docs/concepts/workloads/pods/ephemeral-containers/)
的情况下，为调试的目的注入临时性容器。

<!-- body -->

## 什么是 Pod？   {#what-is-a-pod}

<!--
While Kubernetes supports more
{{< glossary_tooltip text="container runtimes" term_id="container-runtime" >}}
than just Docker, [Docker](https://www.docker.com/) is the most commonly known
runtime, and it helps to describe Pods using some terminology from Docker.
-->
{{< note >}}
除了 Docker 之外，Kubernetes 支持
很多其他{{< glossary_tooltip text="容器运行时" term_id="container-runtime" >}}，
[Docker](https://www.docker.com/) 是最有名的运行时，
使用 Docker 的术语来描述 Pod 会很有帮助。
{{< /note >}}

<!--
The shared context of a Pod is a set of Linux namespaces, cgroups, and
potentially other facets of isolation - the same things that isolate a Docker
container.  Within a Pod's context, the individual applications may have
further sub-isolations applied.

In terms of Docker concepts, a Pod is similar to a group of Docker containers
with shared namespaces and shared filesystem volumes.
-->
Pod 的共享上下文包括一组 Linux 名字空间、控制组（cgroup）和可能一些其他的隔离
方面，即用来隔离 Docker 容器的技术。
在 Pod 的上下文中，每个独立的应用可能会进一步实施隔离。

就 Docker 概念的术语而言，Pod 类似于共享名字空间和文件系统卷的一组 Docker
容器。

<!--
## Using Pods

Usually you don't need to create Pods directly, even singleton Pods. 
Instead, create them using workload resources such as {{< glossary_tooltip text="Deployment"
term_id="deployment" >}} or {{< glossary_tooltip text="Job" term_id="job" >}}.
If your Pods need to track state, consider the 
{{< glossary_tooltip text="StatefulSet" term_id="statefulset" >}} resource.

Pods in a Kubernetes cluster are used in two main ways:
-->
## 使用 Pod   {#using-pods}

通常你不需要直接创建 Pod，甚至单实例 Pod。
相反，你会使用诸如
{{< glossary_tooltip text="Deployment" term_id="deployment" >}} 或
{{< glossary_tooltip text="Job" term_id="job" >}} 这类工作负载资源
来创建 Pod。如果 Pod 需要跟踪状态，
可以考虑 {{< glossary_tooltip text="StatefulSet" term_id="statefulset" >}}
资源。

Kubernetes 集群中的 Pod 主要有两种用法：

<!--
* **Pods that run a single container**. The "one-container-per-Pod" model is the
  most common Kubernetes use case; in this case, you can think of a Pod as a
  wrapper around a single container; Kubernetes manages Pods rather than managing
  the containers directly.
* **Pods that run multiple containers that need to work together**. A Pod can
  encapsulate an application composed of multiple co-located containers that are
  tightly coupled and need to share resources. These co-located containers
  form a single cohesive unit of service—for example, one container serving data
  stored in a shared volume to the public, while a separate _sidecar_ container
  refreshes or updates those files.  
  The Pod wraps these containers, storage resources, and an ephemeral network
  identity together as a single unit.

  Grouping multiple co-located and co-managed containers in a single Pod is a
  relatively advanced use case. You should use this pattern only in specific
  instances in which your containers are tightly coupled.
-->
* **运行单个容器的 Pod**。"每个 Pod 一个容器"模型是最常见的 Kubernetes 用例；
  在这种情况下，可以将 Pod 看作单个容器的包装器，并且 Kubernetes 直接管理 Pod，而不是容器。
* **运行多个协同工作的容器的 Pod**。
  Pod 可能封装由多个紧密耦合且需要共享资源的共处容器组成的应用程序。
  这些位于同一位置的容器可能形成单个内聚的服务单元 —— 一个容器将文件从共享卷提供给公众，
  而另一个单独的“边车”（sidecar）容器则刷新或更新这些文件。
  Pod 将这些容器和存储资源打包为一个可管理的实体。

  {{< note >}}
  将多个并置、同管的容器组织到一个 Pod 中是一种相对高级的使用场景。
  只有在一些场景中，容器之间紧密关联时你才应该使用这种模式。  
  {{< /note >}}

<!--
Each Pod is meant to run a single instance of a given application. If you want to
scale your application horizontally (to provide more overall resources by running
more instances), you should use multiple Pods, one for each instance. In
Kubernetes, this is typically referred to as _replication_.
Replicated Pods are usually created and managed as a group by a workload resource
and its {{< glossary_tooltip text="controller" term_id="controller" >}}.

See [Pods and controllers](#pods-and-controllers) for more information on how
Kubernetes uses workload resources, and their controllers, to implement application
scaling and auto-healing.
-->

每个 Pod 都旨在运行给定应用程序的单个实例。如果希望横向扩展应用程序（例如，运行多个实例
以提供更多的资源），则应该使用多个 Pod，每个实例使用一个 Pod。
在 Kubernetes 中，这通常被称为 _副本（Replication）_。
通常使用一种工作负载资源及其{{< glossary_tooltip text="控制器" term_id="controller" >}}
来创建和管理一组 Pod 副本。

参见 [Pod 和控制器](#pods-and-controllers)以了解 Kubernetes
如何使用工作负载资源及其控制器以实现应用的扩缩和自动修复。

<!--
### How Pods manage multiple containers

Pods are designed to support multiple cooperating processes (as containers) that form
a cohesive unit of service. The containers in a Pod are automatically co-located and
co-scheduled on the same physical or virtual machine in the cluster. The containers
can share resources and dependencies, communicate with one another, and coordinate
when and how they are terminated.
-->
### Pod 怎样管理多个容器

Pod 被设计成支持形成内聚服务单元的多个协作过程（形式为容器）。
Pod 中的容器被自动安排到集群中的同一物理机或虚拟机上，并可以一起进行调度。
容器之间可以共享资源和依赖、彼此通信、协调何时以及何种方式终止自身。

<!--
For example, you might have a container that
acts as a web server for files in a shared volume, and a separate "sidecar" container
that updates those files from a remote source, as in the following diagram:
-->

例如，你可能有一个容器，为共享卷中的文件提供 Web 服务器支持，以及一个单独的
“sidecar（挂斗）”容器负责从远端更新这些文件，如下图所示：

{{< figure src="/images/docs/pod.svg" alt="example pod diagram" width="50%" >}}

<!--
Some Pods have {{< glossary_tooltip text="init containers" term_id="init-container" >}}
as well as {{< glossary_tooltip text="app containers" term_id="app-container" >}}.
Init containers run and complete before the app containers are started.

Pods natively provide two kinds of shared resources for their constituent containers:
[networking](#pod-networking) and [storage](#pod-storage).
-->
有些 Pod 具有 {{< glossary_tooltip text="Init 容器" term_id="init-container" >}} 和
{{< glossary_tooltip text="应用容器" term_id="app-container" >}}。
Init 容器会在启动应用容器之前运行并完成。

Pod 天生地为其成员容器提供了两种共享资源：[网络](#pod-networking)和
[存储](#pod-storage)。

<!--
## Working with Pods

You'll rarely create individual Pods directly in Kubernetes—even singleton Pods. This
is because Pods are designed as relatively ephemeral, disposable entities. When
a Pod gets created (directly by you, or indirectly by a
{{< glossary_tooltip text="controller" term_id="controller" >}}), the new Pod is
scheduled to run on a {{< glossary_tooltip term_id="node" >}} in your cluster.
The Pod remains on that node until the Pod finishes execution, the Pod object is deleted,
the Pod is *evicted* for lack of resources, or the node fails.
-->
## 使用 Pod   {#working-with-pods}

你很少在 Kubernetes 中直接创建一个个的 Pod，甚至是单实例（Singleton）的 Pod。
这是因为 Pod 被设计成了相对临时性的、用后即抛的一次性实体。
当 Pod 由你或者间接地由 {{< glossary_tooltip text="控制器" term_id="controller" >}}
创建时，它被调度在集群中的{{< glossary_tooltip text="节点" term_id="node" >}}上运行。
Pod 会保持在该节点上运行，直到 Pod 结束执行、Pod 对象被删除、Pod 因资源不足而被
*驱逐* 或者节点失效为止。

<!--
Restarting a container in a Pod should not be confused with restarting a Pod. A Pod
is not a process, but an environment for running container(s). A Pod persists until
it is deleted.
-->
{{< note >}}
重启 Pod 中的容器不应与重启 Pod 混淆。
Pod 不是进程，而是容器运行的环境。
在被删除之前，Pod 会一直存在。
{{< /note >}}

<!--
When you create the manifest for a Pod object, make sure the name specified is a valid
[DNS subdomain name](/docs/concepts/overview/working-with-objects/names#dns-subdomain-names).
-->
当你为 Pod 对象创建清单时，要确保所指定的 Pod 名称是合法的
[DNS 子域名](/zh/docs/concepts/overview/working-with-objects/names#dns-subdomain-names)。

<!--
### Pods and controllers

You can use workload resources to create and manage multiple Pods for you. A controller
for the resource handles replication and rollout and automatic healing in case of
Pod failure. For example, if a Node fails, a controller notices that Pods on that
Node have stopped working and creates a replacement Pod. The scheduler places the
replacement Pod onto a healthy Node.

Here are some examples of workload resources that manage one or more Pods:
-->
### Pod 和控制器    {#pods-and-controllers}

你可以使用工作负载资源来创建和管理多个 Pod。
资源的控制器能够处理副本的管理、上线，并在 Pod 失效时提供自愈能力。
例如，如果一个节点失败，控制器注意到该节点上的 Pod 已经停止工作，
就可以创建替换性的 Pod。调度器会将替身 Pod 调度到一个健康的节点执行。

下面是一些管理一个或者多个 Pod 的工作负载资源的示例：

* {{< glossary_tooltip text="Deployment" term_id="deployment" >}}
* {{< glossary_tooltip text="StatefulSet" term_id="statefulset" >}}
* {{< glossary_tooltip text="DaemonSet" term_id="daemonset" >}}

<!--
### Pod templates

Controllers for {{< glossary_tooltip text="workload" term_id="workload" >}} resources create Pods
from a _pod template_ and manage those Pods on your behalf.

PodTemplates are specifications for creating Pods, and are included in workload resources such as
[Deployments](/docs/concepts/workloads/controllers/deployment/),
[Jobs](/docs/concepts/workloads/controllers/job/), and
[DaemonSets](/docs/concepts/workloads/controllers/daemonset/).
-->
### Pod 模版    {#pod-templates}

{{< glossary_tooltip text="负载" term_id="workload" >}}资源的控制器通常使用
_Pod 模板（Pod Template）_ 来替你创建 Pod 并管理它们。

Pod 模板是包含在工作负载对象中的规范，用来创建 Pod。这类负载资源包括
[Deployment](/zh/docs/concepts/workloads/controllers/deployment/)、
[Job](/zh/docs/concepts/workloads/controllers/job/) 和
[DaemonSets](/zh/docs/concepts/workloads/controllers/daemonset/)等。

<!--
Each controller for a workload resource uses the `PodTemplate` inside the workload
object to make actual Pods. The `PodTemplate` is part of the desired state of whatever
workload resource you used to run your app.

The sample below is a manifest for a simple Job with a `template` that starts one
container. The container in that Pod prints a message then pauses.
-->
工作负载的控制器会使用负载对象中的 `PodTemplate` 来生成实际的 Pod。
`PodTemplate` 是你用来运行应用时指定的负载资源的目标状态的一部分。

下面的示例是一个简单的 Job 的清单，其中的 `template` 指示启动一个容器。
该 Pod 中的容器会打印一条消息之后暂停。

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: hello
spec:
  template:
    # 这里是 Pod 模版
    spec:
      containers:
      - name: hello
        image: busybox
        command: ['sh', '-c', 'echo "Hello, Kubernetes!" && sleep 3600']
      restartPolicy: OnFailure
    # 以上为 Pod 模版
```

<!--
Modifying the pod template or switching to a new pod template has no effect on the
Pods that already exist. Pods do not receive template updates directly. Instead,
a new Pod is created to match the revised pod template.

For example, the deployment controller ensures that the running Pods match the current
pod template for each Deployment object. If the template is updated, the Deployment has
to remove the existing Pods and create new Pods based on the updated template. Each workload
resource implements its own rules for handling changes to the Pod template.
-->
修改 Pod 模版或者切换到新的 Pod 模版都不会对已经存在的 Pod 起作用。
Pod 不会直接收到模版的更新。相反，
新的 Pod 会被创建出来，与更改后的 Pod 模版匹配。

例如，Deployment 控制器针对每个 Deployment 对象确保运行中的 Pod 与当前的 Pod
模版匹配。如果模版被更新，则 Deployment 必须删除现有的 Pod，基于更新后的模版
创建新的 Pod。每个工作负载资源都实现了自己的规则，用来处理对 Pod 模版的更新。

<!--
On Nodes, the {{< glossary_tooltip term_id="kubelet" text="kubelet" >}} does not
directly observe or manage any of the details around pod templates and updates; those
details are abstracted away. That abstraction and separation of concerns simplifies
system semantics, and makes it feasible to extend the cluster's behavior without
changing existing code.
-->
在节点上，{{< glossary_tooltip term_id="kubelet" text="kubelet" >}}并不直接监测
或管理与 Pod 模版相关的细节或模版的更新，这些细节都被抽象出来。
这种抽象和关注点分离简化了整个系统的语义，并且使得用户可以在不改变现有代码的
前提下就能扩展集群的行为。

<!--
## Pod update and replacement

As mentioned in the previous section, when the Pod template for a workload
resource is changed, the controller creates new Pods based on the updated
template instead of updating or patching the existing Pods.
-->
## Pod 更新与替换   {#pod-update-and-replacement}

正如前面章节所述，当某工作负载的 Pod 模板被改变时，控制器会基于更新的模板
创建新的 Pod 对象而不是对现有 Pod 执行更新或者修补操作。

<!--
Kubernetes doesn't prevent you from managing Pods directly. It is possible to
update some fields of a running Pod, in place. However, Pod update operations
like 
[`patch`](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#patch-pod-v1-core), and
[`replace`](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#replace-pod-v1-core)
have some limitations:
-->
Kubernetes 并不禁止你直接管理 Pod。对运行中的 Pod 的某些字段执行就地更新操作
还是可能的。不过，类似
[`patch`](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#patch-pod-v1-core) 和
[`replace`](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#replace-pod-v1-core)
这类更新操作有一些限制：

<!--
- Most of the metadata about a Pod is immutable. For example, you cannot
  change the `namespace`, `name`, `uid`, or `creationTimestamp` fields;
  the `generation` field is unique. It only accepts updates that increment the
  field's current value.
- If the `metadata.deletionTimestamp` is set, no new entry can be added to the
  `metadata.finalizers` list.
- Pod updates may not change fields other than `spec.containers[*].image`,
  `spec.initContainers[*].image`, `spec.activeDeadlineSeconds` or
  `spec.tolerations`. For `spec.tolerations`, you can only add new entries.
- When updating the `spec.activeDeadlineSeconds` field, two types of updates
  are allowed:

  1. setting the unassigned field to a positive number; 
  1. updating the field from a positive number to a smaller, non-negative
     number.
-->
- Pod 的绝大多数元数据都是不可变的。例如，你不可以改变其 `namespace`、`name`、
  `uid` 或者 `creationTimestamp` 字段；`generation` 字段是比较特别的，如果更新
  该字段，只能增加字段取值而不能减少。
- 如果 `metadata.deletionTimestamp` 已经被设置，则不可以向 `metadata.finalizers`
  列表中添加新的条目。
- Pod 更新不可以改变除 `spec.containers[*].image`、`spec.initContainers[*].image`、
  `spec.activeDeadlineSeconds` 或 `spec.tolerations` 之外的字段。
  对于 `spec.tolerations`，你只被允许添加新的条目到其中。
- 在更新`spec.activeDeadlineSeconds` 字段时，以下两种更新操作是被允许的：

  1. 如果该字段尚未设置，可以将其设置为一个正数；
  1. 如果该字段已经设置为一个正数，可以将其设置为一个更小的、非负的整数。

<!--
## Resource sharing and communication

Pods enable data sharing and communication among their constituent
containters.
-->
### 资源共享和通信    {#resource-sharing-and-communication}

Pod 使它的成员容器间能够进行数据共享和通信。

<!--
### Storage in Pods {#pod-storage}

A Pod can specify a set of shared storage
{{< glossary_tooltip text="volumes" term_id="volume" >}}. All containers
in the Pod can access the shared volumes, allowing those containers to
share data. Volumes also allow persistent data in a Pod to survive
in case one of the containers within needs to be restarted. See
[Storage](/docs/concepts/storage/) for more information on how
Kubernetes implements shared storage and makes it available to Pods.
-->
### Pod 中的存储 {#pod-storage}

一个 Pod 可以设置一组共享的存储{{< glossary_tooltip text="卷" term_id="volume" >}}。
Pod 中的所有容器都可以访问该共享卷，从而允许这些容器共享数据。
卷还允许 Pod 中的持久数据保留下来，即使其中的容器需要重新启动。
有关 Kubernetes 如何在 Pod 中实现共享存储并将其提供给 Pod 的更多信息，
请参考[卷](/zh/docs/concepts/storage/)。

<!--
### Pod networking

Each Pod is assigned a unique IP address for each address family. Every
container in a Pod shares the network namespace, including the IP address and
network ports. Inside a Pod (and **only** then), the containers that belong to the Pod
can communicate with one another using `localhost`. When containers in a Pod communicate
with entities *outside the Pod*,
they must coordinate how they use the shared network resources (such as ports).
-->
### Pod 联网    {#pod-networking}

每个 Pod 都在每个地址族中获得一个唯一的 IP 地址。
Pod 中的每个容器共享网络名字空间，包括 IP 地址和网络端口。
*Pod 内* 的容器可以使用 `localhost` 互相通信。
当 Pod 中的容器与 *Pod 之外* 的实体通信时，它们必须协调如何使用共享的网络资源
（例如端口）。

<!--
Within a Pod, containers share an IP address and port space, and
can find each other via `localhost`. The containers in a Pod can also communicate
with each other using standard inter-process communications like SystemV semaphores
or POSIX shared memory.  Containers in different Pods have distinct IP addresses
and can not communicate by IPC without
[special configuration](/docs/concepts/policy/pod-security-policy/).
Containers that want to interact with a container running in a different Pod can
use IP networking to communicate.
-->
在同一个 Pod 内，所有容器共享一个 IP 地址和端口空间，并且可以通过 `localhost` 发现对方。
他们也能通过如 SystemV 信号量或 POSIX 共享内存这类标准的进程间通信方式互相通信。
不同 Pod 中的容器的 IP 地址互不相同，没有
[特殊配置](/zh/docs/concepts/policy/pod-security-policy/) 就不能使用 IPC 进行通信。
如果某容器希望与运行于其他 Pod 中的容器通信，可以通过 IP 联网的方式实现。

<!--
Containers within the Pod see the system hostname as being the same as the configured
`name` for the Pod. There's more about this in the [networking](/docs/concepts/cluster-administration/networking/)
section.
-->
Pod 中的容器所看到的系统主机名与为 Pod 配置的 `name` 属性值相同。
[网络](/zh/docs/concepts/cluster-administration/networking/)部分提供了更多有关此内容的信息。

<!--
## Privileged mode for containers

Any container in a Pod can enable privileged mode, using the `privileged` flag on
the [security context](/docs/tasks/configure-pod-container/security-context/) of the container spec. This is useful for containers that want to use operating system administrative capabilities such as manipulating the network stack or accessing hardware devices.
Processes within a privileged container get almost the same privileges that are available to processes outside a container.
-->
## 容器的特权模式     {#privileged-mode-for-containers}

Pod 中的任何容器都可以使用容器规约中的
[安全性上下文](/zh/docs/tasks/configure-pod-container/security-context/)中的
`privileged` 参数启用特权模式。
这对于想要使用操作系统管理权能（Capabilities，如操纵网络堆栈和访问设备）
的容器很有用。
容器内的进程几乎可以获得与容器外的进程相同的特权。

<!--
Your {< glossary_tooltip text="container runtime" term_id="container-runtime" >}} must support the concept of a privileged container for this setting to be relevant.
-->
{{< note >}}
你的{{< glossary_tooltip text="容器运行时" term_id="container-runtime" >}}必须支持
特权容器的概念才能使用这一配置。
{{< /note >}}

<!--
## Static Pods

_Static Pods_ are managed directly by the kubelet daemon on a specific node,
without the {{< glossary_tooltip text="API server" term_id="kube-apiserver" >}}
observing them.
Whereas most Pods are managed by the control plane (for example, a
{{< glossary_tooltip text="Deployment" term_id="deployment" >}}), for static
Pods, the kubelet directly supervises each static Pod (and restarts it if it fails).
-->
## 静态 Pod    {#static-pods}

_静态 Pod（Static Pod）_ 直接由特定节点上的 `kubelet` 守护进程管理，
不需要{{< glossary_tooltip text="API 服务器" term_id="kube-apiserver" >}}看到它们。
尽管大多数 Pod 都是通过控制面（例如，{{< glossary_tooltip text="Deployment" term_id="deployment" >}}）
来管理的，对于静态 Pod 而言，`kubelet` 直接监控每个 Pod，并在其失效时重启之。

<!--
Static Pods are always bound to one {{< glossary_tooltip term_id="kubelet" >}} on a specific node.
The main use for static Pods is to run a self-hosted control plane: in other words,
using the kubelet to supervise the individual [control plane components](/docs/concepts/overview/components/#control-plane-components).

The kubelet automatically tries to create a {{< glossary_tooltip text="mirror Pod" term_id="mirror-pod" >}}
on the Kubernetes API server for each static Pod.
This means that the Pods running on a node are visible on the API server,
but cannot be controlled from there.
-->
静态 Pod 通常绑定到某个节点上的 {{< glossary_tooltip text="kubelet" term_id="kubelet" >}}。
其主要用途是运行自托管的控制面。
在自托管场景中，使用 `kubelet` 来管理各个独立的
[控制面组件](/zh/docs/concepts/overview/components/#control-plane-components)。

`kubelet` 自动尝试为每个静态 Pod 在 Kubernetes API 服务器上创建一个
{{< glossary_tooltip text="镜像 Pod" term_id="mirror-pod" >}}。
这意味着在节点上运行的 Pod 在 API 服务器上是可见的，但不可以通过 API
服务器来控制。

## {{% heading "whatsnext" %}}

<!--
* Learn about the [lifecycle of a Pod](/docs/concepts/workloads/pods/pod-lifecycle/).
* Learn about [RuntimeClass](/docs/concepts/containers/runtime-class/) and how you can use it to
  configure different Pods with different container runtime configurations.
* Read about [Pod topology spread constraints](/docs/concepts/workloads/pods/pod-topology-spread-constraints/).
* Read about [PodDisruptionBudget](https://kubernetes.io/docs/concepts/workloads/pods/disruptions/) and how you can use it to manage application availability during disruptions.
* Pod is a top-level resource in the Kubernetes REST API.  
  The [Pod](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#pod-v1-core)
  object definition describes the object in detail.
* [The Distributed System Toolkit: Patterns for Composite Containers](https://kubernetes.io/blog/2015/06/the-distributed-system-toolkit-patterns) explains common layouts for Pods with more than one container.
--
* 了解 [Pod 生命周期](/zh/docs/concepts/workloads/pods/pod-lifecycle/)
* 了解 [RuntimeClass](/zh/docs/concepts/containers/runtime-class/)，以及如何使用它
  来配置不同的 Pod 使用不同的容器运行时配置
* 了解 [Pod 拓扑分布约束](/zh/docs/concepts/workloads/pods/pod-topology-spread-constraints/)
* 了解 [PodDisruptionBudget](/zh/docs/concepts/workloads/pods/disruptions/)，以及你
  如何可以利用它在出现干扰因素时管理应用的可用性
* Pod 在 Kubernetes REST API 中是一个顶层资源；
  [Pod](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#pod-v1-core)
  对象的定义中包含了更多的细节信息。
* 博客 [分布式系统工具箱：复合容器模式](https://kubernetes.io/blog/2015/06/the-distributed-system-toolkit-patterns)
  中解释了在同一 Pod 中包含多个容器时的几种常见布局。

<!--
To understand the context for why Kubernetes wraps a common Pod API in other resources (such as {{< glossary_tooltip text="StatefulSets" term_id="statefulset" >}} or {{< glossary_tooltip text="Deployments" term_id="deployment" >}}), you can read about the prior art, including:
-->
要了解为什么 Kubernetes 会在其他资源
（如 {{< glossary_tooltip text="StatefulSet" term_id="statefulset" >}}
或 {{< glossary_tooltip text="Deployment" term_id="deployment" >}}）
封装通用的 Pod API，相关的背景信息可以在前人的研究中找到。具体包括：

* [Aurora](https://aurora.apache.org/documentation/latest/reference/configuration/#job-schema)
* [Borg](https://research.google.com/pubs/pub43438.html)
* [Marathon](https://mesosphere.github.io/marathon/docs/rest-api.html)
* [Omega](https://research.google/pubs/pub41684/)
* [Tupperware](https://engineering.fb.com/data-center-engineering/tupperware/).

