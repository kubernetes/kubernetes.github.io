---
title: ReplicationController
feature:
  title: 自我修复
  anchor: ReplicationController 如何工作
  description: >
    重新启动失败的容器，在节点死亡时替换并重新调度容器，杀死不响应用户定义的健康检查的容器，并且在它们准备好服务之前不会将它们公布给客户端。
content_type: concept
weight: 90
---     

<!--
reviewers:
- bprashanth
- janetkuo
title: ReplicationController
feature:
  title: Self-healing
  anchor: How a ReplicationController Works
  description: >
    Restarts containers that fail, replaces and reschedules containers when nodes die, kills containers that don't respond to your user-defined health check, and doesn't advertise them to clients until they are ready to serve.

content_type: concept
weight: 90
-->

<!-- overview -->

<!--
A [`Deployment`](/docs/concepts/workloads/controllers/deployment/) that configures a [`ReplicaSet`](/docs/concepts/workloads/controllers/replicaset/) is now the recommended way to set up replication.
-->
{{< note >}}
现在推荐使用配置 [`ReplicaSet`](/zh/docs/concepts/workloads/controllers/replicaset/) 的
[`Deployment`](/zh/docs/concepts/workloads/controllers/deployment/) 来建立副本管理机制。
{{< /note >}}

<!--
A _ReplicationController_ ensures that a specified number of pod replicas are running at any one
time. In other words, a ReplicationController makes sure that a pod or a homogeneous set of pods is
always up and available.
-->
_ReplicationController_ 确保在任何时候都有特定数量的 Pod 副本处于运行状态。
换句话说，ReplicationController 确保一个 Pod 或一组同类的 Pod 总是可用的。

<!-- body -->

<!--
## How a ReplicationController Works

If there are too many pods, the ReplicationController terminates the extra pods. If there are too few, the
ReplicationController starts more pods. Unlike manually created pods, the pods maintained by a
ReplicationController are automatically replaced if they fail, are deleted, or are terminated.
For example, your pods are re-created on a node after disruptive maintenance such as a kernel upgrade.
For this reason, you should use a ReplicationController even if your application requires
only a single pod. A ReplicationController is similar to a process supervisor,
but instead of supervising individual processes on a single node, the ReplicationController supervises multiple pods
across multiple nodes.
-->
## ReplicationController 如何工作

当 Pod 数量过多时，ReplicationController 会终止多余的 Pod。当 Pod 数量太少时，ReplicationController 将会启动新的 Pod。
与手动创建的 Pod 不同，由 ReplicationController 创建的 Pod 在失败、被删除或被终止时会被自动替换。
例如，在中断性维护（如内核升级）之后，你的 Pod 会在节点上重新创建。
因此，即使你的应用程序只需要一个 Pod，你也应该使用 ReplicationController 创建 Pod。
ReplicationController 类似于进程管理器，但是 ReplicationController 不是监控单个节点上的单个进程，而是监控跨多个节点的多个 Pod。

<!--
ReplicationController is often abbreviated to "rc" in discussion, and as a shortcut in
kubectl commands.

A simple case is to create one ReplicationController object to reliably run one instance of
a Pod indefinitely.  A more complex use case is to run several identical replicas of a replicated
service, such as web servers.
-->
在讨论中，ReplicationController 通常缩写为 "rc"，并作为 kubectl 命令的快捷方式。

一个简单的示例是创建一个 ReplicationController 对象来可靠地无限期地运行 Pod 的一个实例。
更复杂的用例是运行一个多副本服务（如 web 服务器）的若干相同副本。

<!--
## Running an example ReplicationController

This example ReplicationController config runs three copies of the nginx web server.
-->
## 运行一个示例 ReplicationController

这个示例 ReplicationController 配置运行 nginx Web 服务器的三个副本。

{{< codenew file="controllers/replication.yaml" >}}

<!--
Run the example job by downloading the example file and then running this command:
-->
通过下载示例文件并运行以下命令来运行示例任务:

```shell
kubectl apply -f https://k8s.io/examples/controllers/replication.yaml
```

<!--
The output is similar to this:
-->
输出类似于：

```
replicationcontroller/nginx created
```

<!--
Check on the status of the ReplicationController using this command:
-->
使用以下命令检查 ReplicationController 的状态:

```shell
kubectl describe replicationcontrollers/nginx
```

<!--
The output is similar to this:
-->
输出类似于：

```
Name:        nginx
Namespace:   default
Selector:    app=nginx
Labels:      app=nginx
Annotations:    <none>
Replicas:    3 current / 3 desired
Pods Status: 0 Running / 3 Waiting / 0 Succeeded / 0 Failed
Pod Template:
  Labels:       app=nginx
  Containers:
   nginx:
    Image:              nginx
    Port:               80/TCP
    Environment:        <none>
    Mounts:             <none>
  Volumes:              <none>
Events:
  FirstSeen       LastSeen     Count    From                        SubobjectPath    Type      Reason              Message
  ---------       --------     -----    ----                        -------------    ----      ------              -------
  20s             20s          1        {replication-controller }                    Normal    SuccessfulCreate    Created pod: nginx-qrm3m
  20s             20s          1        {replication-controller }                    Normal    SuccessfulCreate    Created pod: nginx-3ntk0
  20s             20s          1        {replication-controller }                    Normal    SuccessfulCreate    Created pod: nginx-4ok8v
```

<!--
Here, three pods are created, but none is running yet, perhaps because the image is being pulled.
A little later, the same command may show:
-->
在这里，创建了三个 Pod，但没有一个 Pod 正在运行，这可能是因为正在拉取镜像。
稍后，相同的命令可能会显示：

```
Pods Status:    3 Running / 0 Waiting / 0 Succeeded / 0 Failed
```

<!--
To list all the pods that belong to the ReplicationController in a machine readable form, you can use a command like this:
-->
要以机器可读的形式列出属于 ReplicationController 的所有 Pod，可以使用如下命令：

```shell
pods=$(kubectl get pods --selector=app=nginx --output=jsonpath={.items..metadata.name})
echo $pods
```

<!--
The output is similar to this:
-->
输出类似于：

```
nginx-3ntk0 nginx-4ok8v nginx-qrm3m
```

<!--
Here, the selector is the same as the selector for the ReplicationController (seen in the
`kubectl describe` output), and in a different form in `replication.yaml`.  The `--output=jsonpath` option
specifies an expression with the name from each pod in the returned list.
-->
这里，选择算符与 ReplicationController 的选择算符相同（参见 `kubectl describe` 输出），并以不同的形式出现在 `replication.yaml` 中。
`--output=jsonpath` 选项指定了一个表达式，仅从返回列表中的每个 Pod 中获取名称。

<!--
## Writing a ReplicationController Spec

As with all other Kubernetes config, a ReplicationController needs `apiVersion`, `kind`, and `metadata` fields.
For general information about working with configuration files, see [object management](/docs/concepts/overview/working-with-objects/object-management/).

A ReplicationController also needs a [`.spec` section](https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status).
-->
## 编写一个 ReplicationController 规约

与所有其它 Kubernetes 配置一样，ReplicationController 需要 `apiVersion`、
`kind` 和 `metadata` 字段。
有关使用配置文件的常规信息，参考
[对象管理](/zh/docs/concepts/overview/working-with-objects/object-management/)。

ReplicationController 也需要一个 [`.spec` 部分](https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status)。

<!--
### Pod Template

The `.spec.template` is the only required field of the `.spec`.

The `.spec.template` is a [pod template](/docs/concepts/workloads/pods/pod-overview/#pod-templates). It has exactly the same schema as a [pod](/docs/concepts/workloads/pods/pod/), except it is nested and does not have an `apiVersion` or `kind`.
-->
### Pod 模板  {#pod-template}

`.spec.template` 是 `.spec` 的唯一必需字段。

`.spec.template` 是一个 [Pod 模板](/zh/docs/concepts/workloads/pods/#pod-templates)。
它的模式与 [Pod](/zh/docs/concepts/workloads/pods/) 完全相同，只是它是嵌套的，没有 `apiVersion` 或 `kind` 属性。

<!--
In addition to required fields for a Pod, a pod template in a ReplicationController must specify appropriate
labels and an appropriate restart policy. For labels, make sure not to overlap with other controllers. See [pod selector](#pod-selector).

Only a [`.spec.template.spec.restartPolicy`](/docs/concepts/workloads/pods/pod-lifecycle/#restart-policy) equal to `Always` is allowed, which is the default if not specified.

For local container restarts, ReplicationControllers delegate to an agent on the node,
for example the [Kubelet](/docs/admin/kubelet/) or Docker.
-->
除了 Pod 所需的字段外，ReplicationController 中的 Pod 模板必须指定适当的标签和适当的重新启动策略。
对于标签，请确保不与其他控制器重叠。参考 [Pod 选择算符](#pod-selector)。

只允许 [`.spec.template.spec.restartPolicy`](/zh/docs/concepts/workloads/pods/pod-lifecycle/#restart-policy) 等于 `Always`，如果没有指定，这是默认值。

对于本地容器重启，ReplicationController 委托给节点上的代理，
例如 [Kubelet](/zh/docs/reference/command-line-tools-reference/kubelet/) 或 Docker。

<!--
### Labels on the ReplicationController

The ReplicationController can itself have labels (`.metadata.labels`).  Typically, you
would set these the same as the `.spec.template.metadata.labels`; if `.metadata.labels` is not specified
then it defaults to  `.spec.template.metadata.labels`. However, they are allowed to be
different, and the `.metadata.labels` do not affect the behavior of the ReplicationController.
-->
### ReplicationController 上的标签

ReplicationController 本身可以有标签 （`.metadata.labels`）。
通常，你可以将这些设置为 `.spec.template.metadata.labels`； 
如果没有指定 `.metadata.labels` 那么它默认为 `.spec.template.metadata.labels`。  
但是，Kubernetes 允许它们是不同的，`.metadata.labels` 不会影响 ReplicationController 的行为。

<!--
### Pod Selector

The `.spec.selector` field is a [label selector](/docs/concepts/overview/working-with-objects/labels/#label-selectors). A ReplicationController
manages all the pods with labels that match the selector. It does not distinguish
between pods that it created or deleted and pods that another person or process created or
deleted. This allows the ReplicationController to be replaced without affecting the running pods.
-->
### Pod 选择算符 {#pod-selector}

`.spec.selector` 字段是一个[标签选择算符](/zh/docs/concepts/overview/working-with-objects/labels/#label-selectors)。 
ReplicationController 管理标签与选择算符匹配的所有 Pod。
它不区分它创建或删除的 Pod 和其他人或进程创建或删除的 Pod。
这允许在不影响正在运行的 Pod 的情况下替换 ReplicationController。

<!--
If specified, the `.spec.template.metadata.labels` must be equal to the `.spec.selector`, or it will
be rejected by the API.  If `.spec.selector` is unspecified, it will be defaulted to
`.spec.template.metadata.labels`.
-->
如果指定了 `.spec.template.metadata.labels`，它必须和 `.spec.selector` 相同，否则它将被 API 拒绝。
如果没有指定 `.spec.selector`，它将默认为 `.spec.template.metadata.labels`。

<!--
Also you should not normally create any pods whose labels match this selector, either directly, with
another ReplicationController, or with another controller such as Job. If you do so, the
ReplicationController thinks that it created the other pods.  Kubernetes does not stop you
from doing this.

If you do end up with multiple controllers that have overlapping selectors, you
will have to manage the deletion yourself (see [below](#working-with-replicationcontrollers)).
-->
另外，通常不应直接使用另一个 ReplicationController 或另一个控制器（例如 Job）
来创建其标签与该选择算符匹配的任何 Pod。如果这样做，ReplicationController 会认为它创建了这些 Pod。
Kubernetes 并没有阻止你这样做。

如果你的确创建了多个控制器并且其选择算符之间存在重叠，那么你将不得不自己管理删除操作（参考[后文](#working-with-replicationcontrollers)）。

<!--
### Multiple Replicas

You can specify how many pods should run concurrently by setting `.spec.replicas` to the number
of pods you would like to have running concurrently.  The number running at any time may be higher
or lower, such as if the replicas were just increased or decreased, or if a pod is gracefully
shutdown, and a replacement starts early.

If you do not specify `.spec.replicas`, then it defaults to 1.
-->
### 多个副本

你可以通过设置 `.spec.replicas` 来指定应该同时运行多少个 Pod。
在任何时候，处于运行状态的 Pod 个数都可能高于或者低于设定值。例如，副本个数刚刚被增加或减少时，或者一个 Pod 处于优雅终止过程中而其替代副本已经提前开始创建时。

如果你没有指定 `.spec.replicas` ，那么它默认是 1。

<!--
## Working with ReplicationControllers

### Deleting a ReplicationController and its Pods

To delete a ReplicationController and all its pods, use [`kubectl
delete`](/docs/reference/generated/kubectl/kubectl-commands#delete).  Kubectl will scale the ReplicationController to zero and wait
for it to delete each pod before deleting the ReplicationController itself.  If this kubectl
command is interrupted, it can be restarted.

When using the REST API or Go client library, you need to do the steps explicitly (scale replicas to
0, wait for pod deletions, then delete the ReplicationController).
-->
## 使用 ReplicationController {#working-with-replicationcontrollers}

### 删除一个 ReplicationController 以及它的 Pod

要删除一个 ReplicationController 以及它的 Pod，使用
[`kubectl delete`](/docs/reference/generated/kubectl/kubectl-commands#delete)。
kubectl 将 ReplicationController 缩放为 0 并等待以便在删除 ReplicationController 本身之前删除每个 Pod。
如果这个 kubectl 命令被中断，可以重新启动它。

当使用 REST API 或 Go 客户端库时，你需要明确地执行这些步骤（缩放副本为 0、
等待 Pod 删除，之后删除 ReplicationController 资源）。

<!--
### Deleting only a ReplicationController

You can delete a ReplicationController without affecting any of its pods.

Using kubectl, specify the `--cascade=orphan` option to [`kubectl delete`](/docs/reference/generated/kubectl/kubectl-commands#delete).

When using the REST API or Go client library, simply delete the ReplicationController object.
-->
### 只删除 ReplicationController

你可以删除一个 ReplicationController 而不影响它的任何 Pod。

使用 kubectl，为 [`kubectl delete`](/docs/reference/generated/kubectl/kubectl-commands#delete) 指定 `--cascade=orphan` 选项。

当使用 REST API 或 Go 客户端库时，只需删除 ReplicationController 对象。

<!--
Once the original is deleted, you can create a new ReplicationController to replace it.  As long
as the old and new `.spec.selector` are the same, then the new one will adopt the old pods.
However, it will not make any effort to make existing pods match a new, different pod template.
To update pods to a new spec in a controlled way, use a [rolling update](#rolling-updates).
-->
一旦原始对象被删除，你可以创建一个新的 ReplicationController 来替换它。
只要新的和旧的 `.spec.selector` 相同，那么新的控制器将领养旧的 Pod。
但是，它不会做出任何努力使现有的 Pod 匹配新的、不同的 Pod 模板。
如果希望以受控方式更新 Pod 以使用新的 spec，请执行[滚动更新](#rolling-updates)操作。

<!--
### Isolating pods from a ReplicationController

Pods may be removed from a ReplicationController's target set by changing their labels. This technique may be used to remove pods from service for debugging and data recovery. Pods that are removed in this way will be replaced automatically (assuming that the number of replicas is not also changed).
-->
### 从 ReplicationController 中隔离 Pod

通过更改 Pod 的标签，可以从 ReplicationController 的目标中删除 Pod。
此技术可用于从服务中删除 Pod 以进行调试、数据恢复等。以这种方式删除的 Pod
将被自动替换（假设复制副本的数量也没有更改）。

<!--
## Common usage patterns
-->
## 常见的使用模式

<!--
### Rescheduling

As mentioned above, whether you have 1 pod you want to keep running, or 1000, a ReplicationController will ensure that the specified number of pods exists, even in the event of node failure or pod termination (for example, due to an action by another control agent).
-->
### 重新调度   {#rescheduling}

如上所述，无论你想要继续运行 1 个 Pod 还是 1000 个 Pod，一个 ReplicationController 都将确保存在指定数量的 Pod，即使在节点故障或 Pod 终止(例如，由于另一个控制代理的操作)的情况下也是如此。
<!--
### Scaling

The ReplicationController enables scaling the number of replicas up or down, either manually or by an auto-scaling control agent, by updating the `replicas` field.
-->
### 扩缩容   {#scaling}

通过设置 `replicas` 字段，ReplicationController 可以允许扩容或缩容副本的数量。
你可以手动或通过自动缩放控制代理来控制 ReplicationController 执行此操作。

<!--
### Rolling updates

The ReplicationController is designed to facilitate rolling updates to a service by replacing pods one-by-one.

As explained in [#1353](http://issue.k8s.io/1353), the recommended approach is to create a new ReplicationController with 1 replica, scale the new (+1) and old (-1) controllers one by one, and then delete the old controller after it reaches 0 replicas. This predictably updates the set of pods regardless of unexpected failures.
-->
### 滚动更新 {#rolling-updates}

ReplicationController 的设计目的是通过逐个替换 Pod 以方便滚动更新服务。

如 [#1353](https://issue.k8s.io/1353) PR 中所述，建议的方法是使用 1 个副本创建一个新的 ReplicationController，
逐个扩容新的（+1）和缩容旧的（-1）控制器，然后在旧的控制器达到 0 个副本后将其删除。
这一方法能够实现可控的 Pod 集合更新，即使存在意外失效的状况。

<!--
Ideally, the rolling update controller would take application readiness into account, and would ensure that a sufficient number of pods were productively serving at any given time.

The two ReplicationControllers would need to create pods with at least one differentiating label, such as the image tag of the primary container of the pod, since it is typically image updates that motivate rolling updates.

Rolling update is implemented in the client tool
[`kubectl rolling-update`](/docs/reference/generated/kubectl/kubectl-commands#rolling-update). Visit [`kubectl rolling-update` task](/docs/tasks/run-application/rolling-update-replication-controller/) for more concrete examples.
-->
理想情况下，滚动更新控制器将考虑应用程序的就绪情况，并确保在任何给定时间都有足够数量的 Pod 有效地提供服务。

这两个 ReplicationController 将需要创建至少具有一个不同标签的 Pod，比如 Pod 主要容器的镜像标签，因为通常是镜像更新触发滚动更新。

滚动更新是在客户端工具 [`kubectl rolling-update`](/docs/reference/generated/kubectl/kubectl-commands#rolling-update)
中实现的。访问 [`kubectl rolling-update` 任务](/zh/docs/tasks/run-application/rolling-update-replication-controller/)以获得更多的具体示例。

<!--
### Multiple release tracks

In addition to running multiple releases of an application while a rolling update is in progress, it's common to run multiple releases for an extended period of time, or even continuously, using multiple release tracks. The tracks would be differentiated by labels.

For instance, a service might target all pods with `tier in (frontend), environment in (prod)`.  Now say you have 10 replicated pods that make up this tier.  But you want to be able to 'canary' a new version of this component.  You could set up a ReplicationController with `replicas` set to 9 for the bulk of the replicas, with labels `tier=frontend, environment=prod, track=stable`, and another ReplicationController with `replicas` set to 1 for the canary, with labels `tier=frontend, environment=prod, track=canary`.  Now the service is covering both the canary and non-canary pods.  But you can mess with the ReplicationControllers separately to test things out, monitor the results, etc.
-->
### 多个版本跟踪

除了在滚动更新过程中运行应用程序的多个版本之外，通常还会使用多个版本跟踪来长时间，
甚至持续运行多个版本。这些跟踪将根据标签加以区分。

例如，一个服务可能把具有 `tier in (frontend), environment in (prod)` 的所有 Pod 作为目标。
现在假设你有 10 个副本的 Pod 组成了这个层。但是你希望能够 `canary` （`金丝雀`）发布这个组件的新版本。
你可以为大部分副本设置一个 ReplicationController，其中 `replicas` 设置为 9，
标签为 `tier=frontend, environment=prod, track=stable` 而为 `canary`
设置另一个 ReplicationController，其中 `replicas` 设置为 1，
标签为 `tier=frontend, environment=prod, track=canary`。
现在这个服务覆盖了 `canary` 和非 `canary` Pod。但你可以单独处理
ReplicationController，以测试、监控结果等。

<!--
### Using ReplicationControllers with Services

Multiple ReplicationControllers can sit behind a single service, so that, for example, some traffic
goes to the old version, and some goes to the new version.

A ReplicationController will never terminate on its own, but it isn't expected to be as long-lived as services. Services may be composed of pods controlled by multiple ReplicationControllers, and it is expected that many ReplicationControllers may be created and destroyed over the lifetime of a service (for instance, to perform an update of pods that run the service). Both services themselves and their clients should remain oblivious to the ReplicationControllers that maintain the pods of the services.
-->
### 和服务一起使用 ReplicationController

多个 ReplicationController 可以位于一个服务的后面，例如，一部分流量流向旧版本，
一部分流量流向新版本。

一个 ReplicationController 永远不会自行终止，但它不会像服务那样长时间存活。
服务可以由多个 ReplicationController 控制的 Pod 组成，并且在服务的生命周期内
（例如，为了执行 Pod 更新而运行服务），可以创建和销毁许多 ReplicationController。
服务本身和它们的客户端都应该忽略负责维护服务 Pod 的 ReplicationController 的存在。

<!--
## Writing programs for Replication

Pods created by a ReplicationController are intended to be fungible and semantically identical, though their configurations may become heterogeneous over time. This is an obvious fit for replicated stateless servers, but ReplicationControllers can also be used to maintain availability of master-elected, sharded, and worker-pool applications. Such applications should use dynamic work assignment mechanisms, such as the [RabbitMQ work queues](https://www.rabbitmq.com/tutorials/tutorial-two-python.html), as opposed to static/one-time customization of the configuration of each pod, which is considered an anti-pattern. Any pod customization performed, such as vertical auto-sizing of resources (for example, cpu or memory), should be performed by another online controller process, not unlike the ReplicationController itself.
-->
## 编写多副本的应用

由 ReplicationController 创建的 Pod 是可替换的，语义上是相同的，
尽管随着时间的推移，它们的配置可能会变得异构。
这显然适合于多副本的无状态服务器，但是 ReplicationController 也可以用于维护主选、
分片和工作池应用程序的可用性。
这样的应用程序应该使用动态的工作分配机制，例如
[RabbitMQ 工作队列](https://www.rabbitmq.com/tutorials/tutorial-two-python.html)，
而不是静态的或者一次性定制每个 Pod 的配置，这被认为是一种反模式。
执行的任何 Pod 定制，例如资源的垂直自动调整大小（例如，CPU 或内存），
都应该由另一个在线控制器进程执行，这与 ReplicationController 本身没什么不同。

<!--
## Responsibilities of the ReplicationController

The ReplicationController ensures that the desired number of pods matches its label selector and are operational. Currently, only terminated pods are excluded from its count. In the future, [readiness](http://issue.k8s.io/620) and other information available from the system may be taken into account, we may add more controls over the replacement policy, and we plan to emit events that could be used by external clients to implement arbitrarily sophisticated replacement and/or scale-down policies.
-->
## ReplicationController 的职责

ReplicationController 仅确保所需的 Pod 数量与其标签选择算符匹配，并且是可操作的。
目前，它的计数中只排除终止的 Pod。
未来，可能会考虑系统提供的[就绪状态](https://issue.k8s.io/620)和其他信息，
我们可能会对替换策略添加更多控制，
我们计划发出事件，这些事件可以被外部客户端用来实现任意复杂的替换和/或缩减策略。

<!--
The ReplicationController is forever constrained to this narrow responsibility. It itself will not perform readiness nor liveness probes. Rather than performing auto-scaling, it is intended to be controlled by an external auto-scaler (as discussed in [#492](http://issue.k8s.io/492)), which would change its `replicas` field. We will not add scheduling policies (for example, [spreading](http://issue.k8s.io/367#issuecomment-48428019)) to the ReplicationController. Nor should it verify that the pods controlled match the currently specified template, as that would obstruct auto-sizing and other automated processes. Similarly, completion deadlines, ordering dependencies, configuration expansion, and other features belong elsewhere. We even plan to factor out the mechanism for bulk pod creation ([#170](http://issue.k8s.io/170)).
-->
ReplicationController 永远被限制在这个狭隘的职责范围内。
它本身既不执行就绪态探测，也不执行活跃性探测。
它不负责执行自动缩放，而是由外部自动缩放器控制（如
[#492](https://issue.k8s.io/492) 中所述），后者负责更改其 `replicas` 字段值。
我们不会向 ReplicationController 添加调度策略(例如，
[spreading](https://issue.k8s.io/367#issuecomment-48428019))。
它也不应该验证所控制的 Pod 是否与当前指定的模板匹配，因为这会阻碍自动调整大小和其他自动化过程。
类似地，完成期限、整理依赖关系、配置扩展和其他特性也属于其他地方。
我们甚至计划考虑批量创建 Pod 的机制（查阅 [#170](https://issue.k8s.io/170)）。

<!--
The ReplicationController is intended to be a composable building-block primitive. We expect higher-level APIs and/or tools to be built on top of it and other complementary primitives for user convenience in the future. The "macro" operations currently supported by kubectl (run, scale, rolling-update) are proof-of-concept examples of this. For instance, we could imagine something like [Asgard](http://techblog.netflix.com/2012/06/asgard-web-based-cloud-management-and.html) managing ReplicationControllers, auto-scalers, services, scheduling policies, canaries, etc.
-->
ReplicationController 旨在成为可组合的构建基元。
我们希望在它和其他补充原语的基础上构建更高级别的 API 或者工具，以便于将来的用户使用。
kubectl 目前支持的 "macro" 操作（运行、缩放、滚动更新）就是这方面的概念示例。
例如，我们可以想象类似于 [Asgard](https://techblog.netflix.com/2012/06/asgaard-web-based-cloud-management-and.html)
的东西管理 ReplicationController、自动定标器、服务、调度策略、金丝雀发布等。

<!--
## API Object

Replication controller is a top-level resource in the Kubernetes REST API. More details about the
API object can be found at:
[ReplicationController API object](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#replicationcontroller-v1-core).
-->
## API 对象

在 Kubernetes REST API 中 Replication controller 是顶级资源。
更多关于 API 对象的详细信息可以在
[ReplicationController API 对象](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#replicationcontroller-v1-core)找到。

<!--
## Alternatives to ReplicationController
### ReplicaSet

[`ReplicaSet`](/docs/concepts/workloads/controllers/replicaset/) is the next-generation ReplicationController that supports the new [set-based label selector](/docs/concepts/overview/working-with-objects/labels/#set-based-requirement).
It’s mainly used by [Deployment](/docs/concepts/workloads/controllers/deployment/) as a mechanism to orchestrate Pod creation, deletion and updates.
Note that we recommend using Deployments instead of directly using Replica Sets, unless you require custom update orchestration or don’t require updates at all.
-->
## ReplicationController 的替代方案

### ReplicaSet

[`ReplicaSet`](/zh/docs/concepts/workloads/controllers/replicaset/) 是下一代 ReplicationController，
支持新的[基于集合的标签选择算符](/zh/docs/concepts/overview/working-with-objects/labels/#set-based-requirement)。
它主要被 [`Deployment`](/zh/docs/concepts/workloads/controllers/deployment/)
用来作为一种编排 Pod 创建、删除及更新的机制。
请注意，我们推荐使用 Deployment 而不是直接使用 ReplicaSet，除非
你需要自定义更新编排或根本不需要更新。

<!--
### Deployment (Recommended)

[`Deployment`](/docs/concepts/workloads/controllers/deployment/) is a higher-level API object that updates its underlying Replica Sets and their Pods
in a similar fashion as `kubectl rolling-update`. Deployments are recommended if you want this rolling update functionality,
because unlike `kubectl rolling-update`, they are declarative, server-side, and have additional features.
-->
### Deployment （推荐）

[`Deployment`](/zh/docs/concepts/workloads/controllers/deployment/) 是一种更高级别的 API 对象，
它以类似于 `kubectl rolling-update` 的方式更新其底层 ReplicaSet 及其 Pod。
如果你想要这种滚动更新功能，那么推荐使用 Deployment，因为与 `kubectl rolling-update` 不同，
它们是声明式的、服务端的，并且具有其它特性。

<!--
### Bare Pods

Unlike in the case where a user directly created pods, a ReplicationController replaces pods that are deleted or terminated for any reason, such as in the case of node failure or disruptive node maintenance, such as a kernel upgrade. For this reason, we recommend that you use a ReplicationController even if your application requires only a single pod. Think of it similarly to a process supervisor, only it supervises multiple pods across multiple nodes instead of individual processes on a single node.  A ReplicationController delegates local container restarts to some agent on the node (for example, Kubelet or Docker).
-->
### 裸 Pod

与用户直接创建 Pod 的情况不同，ReplicationController 能够替换因某些原因
被删除或被终止的 Pod ，例如在节点故障或中断节点维护的情况下，例如内核升级。
因此，我们建议你使用 ReplicationController，即使你的应用程序只需要一个 Pod。
可以将其看作类似于进程管理器，它只管理跨多个节点的多个 Pod ，而不是单个节点上的单个进程。
ReplicationController 将本地容器重启委托给节点上的某个代理(例如，Kubelet 或 Docker)。

<!--
### Job

Use a [`Job`](/docs/concepts/jobs/run-to-completion-finite-workloads/) instead of a ReplicationController for Pods that are expected to terminate on their own
(that is, batch jobs).
-->
### Job

对于预期会自行终止的 Pod (即批处理任务)，使用
[`Job`](/zh/docs/concepts/workloads/controllers/job/) 而不是 ReplicationController。

<!--
### DaemonSet

Use a [`DaemonSet`](/docs/concepts/workloads/controllers/daemonset/) instead of a ReplicationController for pods that provide a
machine-level function, such as machine monitoring or machine logging.  These pods have a lifetime that is tied
to a machine lifetime: the pod needs to be running on the machine before other pods start, and are
safe to terminate when the machine is otherwise ready to be rebooted/shutdown.
-->
### DaemonSet

对于提供机器级功能（例如机器监控或机器日志记录）的 Pod，
使用 [`DaemonSet`](/zh/docs/concepts/workloads/controllers/daemonset/) 而不是
ReplicationController。
这些 Pod 的生命期与机器的生命期绑定：它们需要在其他 Pod 启动之前在机器上运行，
并且在机器准备重新启动或者关闭时安全地终止。

<!--
## For more information

Read [Run Stateless AP Replication Controller](/docs/tutorials/stateless-application/run-stateless-ap-replication-controller/).
-->
## 更多信息

请阅读[运行无状态的 ReplicationController](/zh/docs/tasks/run-application/run-stateless-application-deployment/)。

