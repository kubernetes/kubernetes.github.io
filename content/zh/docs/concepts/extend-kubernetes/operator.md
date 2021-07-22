---
title: Operator 模式
content_type: concept
weight: 30
---

<!--
title: Operator pattern
content_type: concept
weight: 30
-->

<!-- overview -->

<!--
Operators are software extensions to Kubernetes that make use of [custom
resources](/docs/concepts/extend-kubernetes/api-extension/custom-resources/)
to manage applications and their components. Operators follow
Kubernetes principles, notably the [control loop](/docs/concepts/architecture/controller/).
-->
Operator 是 Kubernetes 的扩展软件，它利用
[定制资源](/zh/docs/concepts/extend-kubernetes/api-extension/custom-resources/)
管理应用及其组件。
Operator 遵循 Kubernetes 的理念，特别是在[控制器](/zh/docs/concepts/architecture/controller/)
方面。

<!-- body -->

<!--
## Motivation

The Operator pattern aims to capture the key aim of a human operator who
is managing a service or set of services. Human operators who look after
specific applications and services have deep knowledge of how the system
ought to behave, how to deploy it, and how to react if there are problems.

People who run workloads on Kubernetes often like to use automation to take
care of repeatable tasks. The Operator pattern captures how you can write
code to automate a task beyond what Kubernetes itself provides.
-->
## 初衷

Operator 模式旨在捕获（正在管理一个或一组服务的）运维人员的关键目标。
负责特定应用和 service 的运维人员，在系统应该如何运行、如何部署以及出现问题时如何处理等方面有深入的了解。

在 Kubernetes 上运行工作负载的人们都喜欢通过自动化来处理重复的任务。
Operator 模式会封装你编写的（Kubernetes 本身提供功能以外的）任务自动化代码。

<!--
## Operators in Kubernetes

Kubernetes is designed for automation. Out of the box, you get lots of
built-in automation from the core of Kubernetes. You can use Kubernetes
to automate deploying and running workloads, *and* you can automate how
Kubernetes does that.

Kubernetes' {{< glossary_tooltip text="controllers" term_id="controller" >}}
concept lets you extend the cluster's behaviour without modifying the code
of Kubernetes itself.
Operators are clients of the Kubernetes API that act as controllers for
a [Custom Resource](/docs/concepts/extend-kubernetes/api-extension/custom-resources/).
-->
## Kubernetes 上的 Operator

Kubernetes 为自动化而生。无需任何修改，你即可以从 Kubernetes 核心中获得许多内置的自动化功能。
你可以使用 Kubernetes 自动化部署和运行工作负载， *甚至* 可以自动化 Kubernetes 自身。

Kubernetes {{< glossary_tooltip text="控制器" term_id="controller" >}}
使你无需修改 Kubernetes 自身的代码，即可以扩展集群的行为。
Operator 是 Kubernetes API 的客户端，充当
[定制资源](/zh/docs/concepts/extend-kubernetes/api-extension/custom-resources/)
的控制器。

<!--
## An example Operator {#example}

Some of the things that you can use an operator to automate include:

* deploying an application on demand
* taking and restoring backups of that application's state
* handling upgrades of the application code alongside related changes such
  as database schemas or extra configuration settings
* publishing a Service to applications that don't support Kubernetes APIs to
  discover them
* simulating failure in all or part of your cluster to test its resilience
* choosing a leader for a distributed application without an internal
  member election process
-->
## Operator 示例 {#example}

使用 Operator 可以自动化的事情包括：

* 按需部署应用
* 获取/还原应用状态的备份
* 处理应用代码的升级以及相关改动。例如，数据库 schema 或额外的配置设置
* 发布一个 service，要求不支持 Kubernetes API 的应用也能发现它
* 模拟整个或部分集群中的故障以测试其稳定性
* 在没有内部成员选举程序的情况下，为分布式应用选择首领角色

<!--
What might an Operator look like in more detail? Here's an example in more
detail:

1. A custom resource named SampleDB, that you can configure into the cluster.
2. A Deployment that makes sure a Pod is running that contains the
   controller part of the operator.
3. A container image of the operator code.
4. Controller code that queries the control plane to find out what SampleDB
   resources are configured.
5. The core of the Operator is code to tell the API server how to make
   reality match the configured resources.
   * If you add a new SampleDB, the operator sets up PersistentVolumeClaims
     to provide durable database storage, a StatefulSet to run SampleDB and
     a Job to handle initial configuration.
   * If you delete it, the Operator takes a snapshot, then makes sure that
     the StatefulSet and Volumes are also removed.
6. The operator also manages regular database backups. For each SampleDB
   resource, the operator determines when to create a Pod that can connect
   to the database and take backups. These Pods would rely on a ConfigMap
   and / or a Secret that has database connection details and credentials.
7. Because the Operator aims to provide robust automation for the resource
   it manages, there would be additional supporting code. For this example,
   code checks to see if the database is running an old version and, if so,
   creates Job objects that upgrade it for you.
-->

想要更详细的了解 Operator？这儿有一个详细的示例：

1. 有一个名为 SampleDB 的自定义资源，你可以将其配置到集群中。
2. 一个包含 Operator 控制器部分的 Deployment，用来确保 Pod 处于运行状态。
3. Operator 代码的容器镜像。
4. 控制器代码，负责查询控制平面以找出已配置的 SampleDB 资源。
5. Operator 的核心是告诉 API 服务器，如何使现实与代码里配置的资源匹配。
   * 如果添加新的 SampleDB，Operator 将设置 PersistentVolumeClaims 以提供
     持久化的数据库存储，设置 StatefulSet 以运行 SampleDB，并设置 Job
     来处理初始配置。
   * 如果你删除它，Operator 将建立快照，然后确保 StatefulSet 和 Volume 已被删除。
6. Operator 也可以管理常规数据库的备份。对于每个 SampleDB 资源，Operator
   会确定何时创建（可以连接到数据库并进行备份的）Pod。这些 Pod 将依赖于
   ConfigMap 和/或具有数据库连接详细信息和凭据的 Secret。
7. 由于 Operator 旨在为其管理的资源提供强大的自动化功能，因此它还需要一些
   额外的支持性代码。在这个示例中，代码将检查数据库是否正运行在旧版本上，
   如果是，则创建 Job 对象为你升级数据库。

<!--
## Deploying Operators

The most common way to deploy an Operator is to add the
Custom Resource Definition and its associated Controller to your cluster.
The Controller will normally run outside of the
{{< glossary_tooltip text="control plane" term_id="control-plane" >}},
much as you would run any containerized application.
For example, you can run the controller in your cluster as a Deployment.
-->
## 部署 Operator

部署 Operator 最常见的方法是将自定义资源及其关联的控制器添加到你的集群中。
跟运行容器化应用一样，控制器通常会运行在
{{< glossary_tooltip text="控制平面" term_id="control-plane" >}} 之外。
例如，你可以在集群中将控制器作为 Deployment 运行。

<!--
## Using an Operator {#using-operators}

Once you have an Operator deployed, you'd use it by adding, modifying or
deleting the kind of resource that the Operator uses. Following the above
example, you would set up a Deployment for the Operator itself, and then:

```shell
kubectl get SampleDB                   # find configured databases

kubectl edit SampleDB/example-database # manually change some settings
```
-->
## 使用 Operator {#using-operators}

部署 Operator 后，你可以对 Operator 所使用的资源执行添加、修改或删除操作。
按照上面的示例，你将为 Operator 本身建立一个 Deployment，然后：

```shell
kubectl get SampleDB                   # 查找所配置的数据库

kubectl edit SampleDB/example-database # 手动修改某些配置
```

<!--
&hellip;and that's it! The Operator will take care of applying the changes as well as keeping the existing service in good shape.
-->
可以了！Operator 会负责应用所作的更改并保持现有服务处于良好的状态。

<!--
## Writing your own Operator {#writing-operator}
-->

## 编写你自己的 Operator {#writing-operator}

<!--
If there isn't an Operator in the ecosystem that implements the behavior you
want, you can code your own.

You also implement an Operator (that is, a Controller) using any language / runtime
that can act as a [client for the Kubernetes API](/docs/reference/using-api/client-libraries/).
-->

如果生态系统中没可以实现你目标的 Operator，你可以自己编写代码。

你还可以使用任何支持 [Kubernetes API 客户端](/zh/docs/reference/using-api/client-libraries/)
的语言或运行时来实现 Operator（即控制器）。

<!--
Following are a few libraries and tools you can use to write your own cloud native
Operator.

{{% thirdparty-content %}}

* [Charmed Operator Framework](https://juju.is/)
* [kubebuilder](https://book.kubebuilder.io/)
* [KUDO](https://kudo.dev/) (Kubernetes Universal Declarative Operator)
* [Metacontroller](https://metacontroller.app/) along with WebHooks that
  you implement yourself
* [Operator Framework](https://operatorframework.io)
* [shell-operator](https://github.com/flant/shell-operator)
-->
以下是一些库和工具，你可用于编写自己的云原生 Operator。

{{% thirdparty-content %}}

* [Charmed Operator Framework](https://juju.is/)
* [kubebuilder](https://book.kubebuilder.io/)
* [KUDO](https://kudo.dev/) (Kubernetes 通用声明式 Operator)
* [Metacontroller](https://metacontroller.app/)，可与 Webhooks 结合使用，以实现自己的功能。
* [Operator Framework](https://operatorframework.io)
* [shell-operator](https://github.com/flant/shell-operator)

## {{% heading "whatsnext" %}}

<!--
* Read the {{< glossary_tooltip text="CNCF" term_id="cncf" >}} [Operator White Paper](https://github.com/cncf/tag-app-delivery/blob/eece8f7307f2970f46f100f51932db106db46968/operator-wg/whitepaper/Operator-WhitePaper_v1-0.md).
* Learn more about [Custom Resources](/docs/concepts/extend-kubernetes/api-extension/custom-resources/)
* Find ready-made operators on [OperatorHub.io](https://operatorhub.io/) to suit your use case
* [Publish](https://operatorhub.io/) your operator for other people to use
* Read [CoreOS' original article](https://web.archive.org/web/20170129131616/https://coreos.com/blog/introducing-operators.html) that introduced the Operator pattern (this is an archived version of the original article).
* Read an [article](https://cloud.google.com/blog/products/containers-kubernetes/best-practices-for-building-kubernetes-operators-and-stateful-apps) from Google Cloud about best practices for building Operators
-->

* 阅读 {{<glossary_tooltip text="CNCF" term_id="cncf" >}} [Operator白皮书](https://github.com/cncf/tag-app-delivery/blob/eece8f7307f2970f46f100f51932db106db46968/operator-wg/whitepaper/Operator-WhitePaper_v1-0.md）。
* 详细了解 [定制资源](/zh/docs/concepts/extend-kubernetes/api-extension/custom-resources/)
* 在 [OperatorHub.io](https://operatorhub.io/) 上找到现成的、适合你的 Operator
* [发布](https://operatorhub.io/)你的 Operator，让别人也可以使用
* 阅读 [CoreOS 原始文章](https://web.archive.org/web/20170129131616/https://coreos.com/blog/introducing-operators.html)，它介绍了 Operator 模式（这是一个存档版本的原始文章）。
* 阅读这篇来自谷歌云的关于构建 Operator 最佳实践的
  [文章](https://cloud.google.com/blog/products/containers-kubernetes/best-practices-for-building-kubernetes-operators-and-stateful-apps)
