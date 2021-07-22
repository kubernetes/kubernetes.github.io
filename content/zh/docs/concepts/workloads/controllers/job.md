---
title: Jobs
content_type: concept
feature:
  title: 批量执行
  description: >
    除了服务之外，Kubernetes 还可以管理你的批处理和 CI 工作负载，在期望时替换掉失效的容器。
weight: 50
---
<!--
reviewers:
- erictune
- soltysh
title: Jobs
content_type: concept
feature:
  title: Batch execution
  description: >
    In addition to services, Kubernetes can manage your batch and CI workloads, replacing containers that fail, if desired.
weight: 50
-->

<!-- overview -->
<!--
A Job creates one or more Pods and will continue to retry execution of the Pods until a specified number of them successfully terminate.
As pods successfully complete, the Job tracks the successful completions.  When a specified number
of successful completions is reached, the task (ie, Job) is complete.  Deleting a Job will clean up
the Pods it created. Suspending a Job will delete its active Pods until the Job
is resumed again.

A simple case is to create one Job object in order to reliably run one Pod to completion.
The Job object will start a new Pod if the first Pod fails or is deleted (for example
due to a node hardware failure or a node reboot).

You can also use a Job to run multiple Pods in parallel.
-->
Job 会创建一个或者多个 Pods，并将继续重试 Pods 的执行，直到指定数量的 Pods 成功终止。
随着 Pods 成功结束，Job 跟踪记录成功完成的 Pods 个数。
当数量达到指定的成功个数阈值时，任务（即 Job）结束。
删除 Job 的操作会清除所创建的全部 Pods。
挂起 Job 的操作会删除 Job 的所有活跃 Pod，直到 Job 被再次恢复执行。

一种简单的使用场景下，你会创建一个 Job 对象以便以一种可靠的方式运行某 Pod 直到完成。
当第一个 Pod 失败或者被删除（比如因为节点硬件失效或者重启）时，Job
对象会启动一个新的 Pod。

你也可以使用 Job 以并行的方式运行多个 Pod。

<!-- body -->
<!--
## Running an example Job

Here is an example Job config.  It computes π to 2000 places and prints it out.
It takes around 10s to complete.
-->
## 运行示例 Job     {#running-an-example-job}

下面是一个 Job 配置示例。它负责计算 π 到小数点后 2000 位，并将结果打印出来。
此计算大约需要 10 秒钟完成。

{{< codenew file="controllers/job.yaml" >}}

<!--You can run the example with this command:-->
你可以使用下面的命令来运行此示例：

```shell
kubectl apply -f https://kubernetes.io/examples/controllers/job.yaml
```

输出类似于：

```
job.batch/pi created
```

<!-- Check on the status of the Job with `kubectl`: -->
使用 `kubectl` 来检查 Job 的状态：

```shell
kubectl describe jobs/pi
```

输出类似于：

```
Name:           pi
Namespace:      default
Selector:       controller-uid=c9948307-e56d-4b5d-8302-ae2d7b7da67c
Labels:         controller-uid=c9948307-e56d-4b5d-8302-ae2d7b7da67c
                job-name=pi
Annotations:    kubectl.kubernetes.io/last-applied-configuration:
                  {"apiVersion":"batch/v1","kind":"Job","metadata":{"annotations":{},"name":"pi","namespace":"default"},"spec":{"backoffLimit":4,"template":...
Parallelism:    1
Completions:    1
Start Time:     Mon, 02 Dec 2019 15:20:11 +0200
Completed At:   Mon, 02 Dec 2019 15:21:16 +0200
Duration:       65s
Pods Statuses:  0 Running / 1 Succeeded / 0 Failed
Pod Template:
  Labels:  controller-uid=c9948307-e56d-4b5d-8302-ae2d7b7da67c
           job-name=pi
  Containers:
   pi:
    Image:      perl
    Port:       <none>
    Host Port:  <none>
    Command:
      perl
      -Mbignum=bpi
      -wle
      print bpi(2000)
    Environment:  <none>
    Mounts:       <none>
  Volumes:        <none>
Events:
  Type    Reason            Age   From            Message
  ----    ------            ----  ----            -------
  Normal  SuccessfulCreate  14m   job-controller  Created pod: pi-5rwd7
```

<!--
To view completed Pods of a Job, use `kubectl get pods`.

To list all the Pods that belong to a Job in a machine readable form, you can use a command like this:
-->
要查看 Job 对应的已完成的 Pods，可以执行 `kubectl get pods`。

要以机器可读的方式列举隶属于某 Job 的全部 Pods，你可以使用类似下面这条命令：

```shell
pods=$(kubectl get pods --selector=job-name=pi --output=jsonpath='{.items[*].metadata.name}')
echo $pods
```

输出类似于：

```
pi-5rwd7
```

<!--
Here, the selector is the same as the selector for the Job.  The `-output=jsonpath` option specifies an expression
with the name from each Pod in the returned list.

View the standard output of one of the pods:
-->
这里，选择算符与 Job 的选择算符相同。`--output=jsonpath` 选项给出了一个表达式，
用来从返回的列表中提取每个 Pod 的 name 字段。

查看其中一个 Pod 的标准输出：

```shell
kubectl logs $pods
```

<!--The output is similar to this:-->
输出类似于：

```
3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679821480865132823066470938446095505822317253594081284811174502841027019385211055596446229489549303819644288109756659334461284756482337867831652712019091456485669234603486104543266482133936072602491412737245870066063155881748815209209628292540917153643678925903600113305305488204665213841469519415116094330572703657595919530921861173819326117931051185480744623799627495673518857527248912279381830119491298336733624406566430860213949463952247371907021798609437027705392171762931767523846748184676694051320005681271452635608277857713427577896091736371787214684409012249534301465495853710507922796892589235420199561121290219608640344181598136297747713099605187072113499999983729780499510597317328160963185950244594553469083026425223082533446850352619311881710100031378387528865875332083814206171776691473035982534904287554687311595628638823537875937519577818577805321712268066130019278766111959092164201989380952572010654858632788659361533818279682303019520353018529689957736225994138912497217752834791315155748572424541506959508295331168617278558890750983817546374649393192550604009277016711390098488240128583616035637076601047101819429555961989467678374494482553797747268471040475346462080466842590694912933136770289891521047521620569660240580381501935112533824300355876402474964732639141992726042699227967823547816360093417216412199245863150302861829745557067498385054945885869269956909272107975093029553211653449872027559602364806654991198818347977535663698074265425278625518184175746728909777727938000816470600161452491921732172147723501414419735685481613611573525521334757418494684385233239073941433345477624168625189835694855620992192221842725502542568876717904946016534668049886272327917860857843838279679766814541009538837863609506800642251252051173929848960841284886269456042419652850222106611863067442786220391949450471237137869609563643719172874677646575739624138908658326459958133904780275901
```
<!--
## Writing a Job spec

As with all other Kubernetes config, a Job needs `apiVersion`, `kind`, and `metadata` fields.
Its name must be a valid [DNS subdomain name](/docs/concepts/overview/working-with-objects/names#dns-subdomain-names).

A Job also needs a [`.spec` section](https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status).
-->
## 编写 Job 规约

与 Kubernetes 中其他资源的配置类似，Job 也需要 `apiVersion`、`kind` 和 `metadata` 字段。
Job 的名字必须是合法的 [DNS 子域名](/zh/docs/concepts/overview/working-with-objects/names#dns-subdomain-names)。

Job 配置还需要一个[`.spec` 节](https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status)。

<!--
### Pod Template

The `.spec.template` is the only required field of the `.spec`.

The `.spec.template` is a [pod template](/docs/concepts/workloads/pods/#pod-templates). It has exactly the same schema as a {{< glossary_tooltip text="Pod" term_id="pod" >}}, except it is nested and does not have an `apiVersion` or `kind`.

In addition to required fields for a Pod, a pod template in a Job must specify appropriate
labels (see [pod selector](#pod-selector)) and an appropriate restart policy.

Only a [`RestartPolicy`](/docs/concepts/workloads/pods/pod-lifecycle/#restart-policy) equal to `Never` or `OnFailure` is allowed.
-->
### Pod 模版

Job 的 `.spec` 中只有 `.spec.template` 是必需的字段。

字段 `.spec.template` 的值是一个 [Pod 模版](/zh/docs/concepts/workloads/pods/#pod-templates)。
其定义规范与 {{< glossary_tooltip text="Pod" term_id="pod" >}}
完全相同，只是其中不再需要 `apiVersion` 或 `kind` 字段。

除了作为 Pod 所必需的字段之外，Job 中的 Pod 模版必需设置合适的标签
（参见[Pod 选择算符](#pod-selector)）和合适的重启策略。

Job 中 Pod 的 [`RestartPolicy`](/zh/docs/concepts/workloads/pods/pod-lifecycle/#restart-policy)
只能设置为 `Never` 或 `OnFailure` 之一。

<!--
### Pod selector

The `.spec.selector` field is optional.  In almost all cases you should not specify it.
See section [specifying your own pod selector](#specifying-your-own-pod-selector).
-->
### Pod 选择算符   {#pod-selector}

字段 `.spec.selector` 是可选的。在绝大多数场合，你都不需要为其赋值。
参阅[设置自己的 Pod 选择算符](#specifying-your-own-pod-selector).

<!--
### Parallel execution for Jobs {#parallel-jobs}

There are three main types of task suitable to run as a Job:
-->
### Job 的并行执行 {#parallel-jobs}

适合以 Job 形式来运行的任务主要有三种：
<!--
1. Non-parallel Jobs
   - normally, only one Pod is started, unless the Pod fails.
   - the Job is complete as soon as its Pod terminates successfully.
1. Parallel Jobs with a *fixed completion count*:
   - specify a non-zero positive value for `.spec.completions`.
   - the Job represents the overall task, and is complete when there are `.spec.completions` successful Pods.
   - when using `.spec.completionMode="Indexed"`, each Pod gets a different index in the range 0 to `.spec.completions-1`.
1. Parallel Jobs with a *work queue*:
   - do not specify `.spec.completions`, default to `.spec.parallelism`.
   - the Pods must coordinate amongst themselves or an external service to determine what each should work on. For example, a Pod might fetch a batch of up to N items from the work queue.
   - each Pod is independently capable of determining whether or not all its peers are done, and thus that the entire Job is done.
   - when _any_ Pod from the Job terminates with success, no new Pods are created.
   - once at least one Pod has terminated with success and all Pods are terminated, then the Job is completed with success.
   - once any Pod has exited with success, no other Pod should still be doing any work for this task or writing any output.  They should all be in the process of exiting.
-->
1. 非并行 Job：
   - 通常只启动一个 Pod，除非该 Pod 失败。
   - 当 Pod 成功终止时，立即视 Job 为完成状态。
1. 具有 *确定完成计数* 的并行 Job：
   - `.spec.completions` 字段设置为非 0 的正数值。
   - Job 用来代表整个任务，当成功的 Pod 个数达到 `.spec.completions` 时，Job 被视为完成。
   - 当使用 `.spec.completionMode="Indexed"` 时，每个 Pod 都会获得一个不同的
     索引值，介于 0 和 `.spec.completions-1` 之间。
1. 带 *工作队列* 的并行 Job：
   - 不设置 `spec.completions`，默认值为 `.spec.parallelism`。
   - 多个 Pod 之间必须相互协调，或者借助外部服务确定每个 Pod 要处理哪个工作条目。
     例如，任一 Pod 都可以从工作队列中取走最多 N 个工作条目。
   - 每个 Pod 都可以独立确定是否其它 Pod 都已完成，进而确定 Job 是否完成。
   - 当 Job 中 _任何_ Pod 成功终止，不再创建新 Pod。
   - 一旦至少 1 个 Pod 成功完成，并且所有 Pod 都已终止，即可宣告 Job 成功完成。
   - 一旦任何 Pod 成功退出，任何其它 Pod 都不应再对此任务执行任何操作或生成任何输出。
     所有 Pod 都应启动退出过程。

<!--
For a _non-parallel_ Job, you can leave both `.spec.completions` and `.spec.parallelism` unset.  When both are
unset, both are defaulted to 1.

For a _fixed completion count_ Job, you should set `.spec.completions` to the number of completions needed.
You can set `.spec.parallelism`, or leave it unset and it will default to 1.

For a _work queue_ Job, you must leave `.spec.completions` unset, and set `.spec.parallelism` to
a non-negative integer.

For more information about how to make use of the different types of job, see the [job patterns](#job-patterns) section.
-->
对于 _非并行_ 的 Job，你可以不设置 `spec.completions` 和 `spec.parallelism`。
这两个属性都不设置时，均取默认值 1。

对于 _确定完成计数_ 类型的 Job，你应该设置 `.spec.completions` 为所需要的完成个数。
你可以设置 `.spec.parallelism`，也可以不设置。其默认值为 1。

对于一个 _工作队列_ Job，你不可以设置 `.spec.completions`，但要将`.spec.parallelism`
设置为一个非负整数。

关于如何利用不同类型的 Job 的更多信息，请参见 [Job 模式](#job-patterns)一节。

<!--
#### Controlling parallelism

The requested parallelism (`.spec.parallelism`) can be set to any non-negative value.
If it is unspecified, it defaults to 1.
If it is specified as 0, then the Job is effectively paused until it is increased.

Actual parallelism (number of pods running at any instant) may be more or less than requested
parallelism, for a variety of reasons:
-->
#### 控制并行性   {#controlling-parallelism}

并行性请求（`.spec.parallelism`）可以设置为任何非负整数。
如果未设置，则默认为 1。
如果设置为 0，则 Job 相当于启动之后便被暂停，直到此值被增加。

实际并行性（在任意时刻运行状态的 Pods 个数）可能比并行性请求略大或略小，
原因如下：

<!--
- For _fixed completion count_ Jobs, the actual number of pods running in parallel will not exceed the number of
  remaining completions.   Higher values of `.spec.parallelism` are effectively ignored.
- For _work queue_ Jobs, no new Pods are started after any Pod has succeeded - remaining Pods are allowed to complete, however.
- If the Job {{< glossary_tooltip term_id="controller" >}} has not had time to react.
- If the Job controller failed to create Pods for any reason (lack of `ResourceQuota`, lack of permission, etc.),
  then there may be fewer pods than requested.
- The Job controller may throttle new Pod creation due to excessive previous pod failures in the same Job.
- When a Pod is gracefully shut down, it takes time to stop.
-->
- 对于 _确定完成计数_ Job，实际上并行执行的 Pods 个数不会超出剩余的完成数。
  如果 `.spec.parallelism` 值较高，会被忽略。
- 对于 _工作队列_ Job，有任何 Job 成功结束之后，不会有新的 Pod 启动。
  不过，剩下的 Pods 允许执行完毕。
- 如果 Job {{< glossary_tooltip text="控制器" term_id="controller" >}} 没有来得及作出响应，或者
- 如果 Job 控制器因为任何原因（例如，缺少 `ResourceQuota` 或者没有权限）无法创建 Pods。
  Pods 个数可能比请求的数目小。
- Job 控制器可能会因为之前同一 Job 中 Pod 失效次数过多而压制新 Pod 的创建。
- 当 Pod 处于体面终止进程中，需要一定时间才能停止。

<!--
### Completion mode
-->
### 完成模式   {#completion-mode}

{{< feature-state for_k8s_version="v1.21" state="alpha" >}}

{{< note >}}
<!--
To be able to create Indexed Jobs, make sure to enable the `IndexedJob`
[feature gate](/docs/reference/command-line-tools-reference/feature-gates/)
on the [API server](/docs/reference/command-line-tools-reference/kube-apiserver/)
and the [controller manager](/docs/reference/command-line-tools-reference/kube-controller-manager/).
-->
若想创建带索引的 Job（Indexed Job），请确保
[API 服务器](/zh/docs/reference/command-line-tools-reference/kube-apiserver/)
和[控制器管理器](/docs/reference/command-line-tools-reference/kube-controller-manager/)
上的
[特性门控](/zh/docs/reference/command-line-tools-reference/feature-gates/)
`IndexedJob` 被启用。
{{< /note >}}

<!--
Jobs with _fixed completion count_ - that is, jobs that have non null
`.spec.completions` - can have a completion mode that is specified in `.spec.completionMode`:
-->
带有 *确定完成计数* 的 Job，即 `.spec.completions` 不为 null 的 Job，
都可以在其 `.spec.completionMode` 中设置完成模式：

<!--
- `NonIndexed` (default): the Job is considered complete when there have been
  `.spec.completions` successfully completed Pods. In other words, each Pod
  completion is homologous to each other. Note that Jobs that have null
  `.spec.completions` are implicitly `NonIndexed`.
- `Indexed`: the Pods of a Job get an associated completion index from 0 to
  `.spec.completions-1`, available in the annotation `batch.kubernetes.io/job-completion-index`.
  The Job is considered complete when there is one successfully completed Pod
  for each index. For more information about how to use this mode, see
  [Indexed Job for Parallel Processing with Static Work Assignment](/docs/tasks/job/indexed-parallel-processing-static/).
  Note that, although rare, more than one Pod could be started for the same
  index, but only one of them will count towards the completion count.
-->
- `NonIndexed` （默认值）：当成功完成的 Pod 个数达到 `.spec.completions` 所
  设值时认为 Job 已经完成。换言之，每个 Job 完成事件都是独立无关且同质的。
  要注意的是，当 `.spec.completions` 取值为 null 时，Job 被隐式处理为 `NonIndexed`。
- `Indexed`：Job 的 Pod 会获得对应的完成索引，取值为 0 到 `.spec.completions-1`，
  存放在注解 `batch.kubernetes.io/job-completion-index` 中。
  当每个索引都对应一个完成完成的 Pod 时，Job 被认为是已完成的。
  关于如何使用这种模式的更多信息，可参阅
  [用带索引的 Job 执行基于静态任务分配的并行处理](/zh/docs/tasks/job/indexed-parallel-processing-static/)。
  需要注意的是，对同一索引值可能被启动的 Pod 不止一个，尽管这种情况很少发生。
  这时，只有一个会被记入完成计数中。

<!--
## Handling Pod and container failures

A container in a Pod may fail for a number of reasons, such as because the process in it exited with
a non-zero exit code, or the container was killed for exceeding a memory limit, etc.  If this
happens, and the `.spec.template.spec.restartPolicy = "OnFailure"`, then the Pod stays
on the node, but the container is re-run.  Therefore, your program needs to handle the case when it is
restarted locally, or else specify `.spec.template.spec.restartPolicy = "Never"`.
See [pod lifecycle](/docs/concepts/workloads/pods/pod-lifecycle/#example-states) for more information on `restartPolicy`.
-->

## 处理 Pod 和容器失效

Pod 中的容器可能因为多种不同原因失效，例如因为其中的进程退出时返回值非零，
或者容器因为超出内存约束而被杀死等等。
如果发生这类事件，并且 `.spec.template.spec.restartPolicy = "OnFailure"`，
Pod 则继续留在当前节点，但容器会被重新运行。
因此，你的程序需要能够处理在本地被重启的情况，或者要设置
`.spec.template.spec.restartPolicy = "Never"`。
关于 `restartPolicy` 的更多信息，可参阅
[Pod 生命周期](/zh/docs/concepts/workloads/pods/pod-lifecycle/#example-states)。

<!--
An entire Pod can also fail, for a number of reasons, such as when the pod is kicked off the node
(node is upgraded, rebooted, deleted, etc.), or if a container of the Pod fails and the
`.spec.template.spec.restartPolicy = "Never"`.  When a Pod fails, then the Job controller
starts a new Pod.  This means that your application needs to handle the case when it is restarted in a new
pod.  In particular, it needs to handle temporary files, locks, incomplete output and the like
caused by previous runs.
-->
整个 Pod 也可能会失败，且原因各不相同。
例如，当 Pod 启动时，节点失效（被升级、被重启、被删除等）或者其中的容器失败而
`.spec.template.spec.restartPolicy = "Never"`。
当 Pod 失败时，Job 控制器会启动一个新的 Pod。
这意味着，你的应用需要处理在一个新 Pod 中被重启的情况。
尤其是应用需要处理之前运行所产生的临时文件、锁、不完整的输出等问题。

<!--
Note that even if you specify `.spec.parallelism = 1` and `.spec.completions = 1` and
`.spec.template.spec.restartPolicy = "Never"`, the same program may
sometimes be started twice.

If you do specify `.spec.parallelism` and `.spec.completions` both greater than 1, then there may be
multiple pods running at once.  Therefore, your pods must also be tolerant of concurrency.
-->
注意，即使你将 `.spec.parallelism` 设置为 1，且将 `.spec.completions` 设置为
1，并且 `.spec.template.spec.restartPolicy` 设置为 "Never"，同一程序仍然有可能被启动两次。

如果你确实将 `.spec.parallelism` 和 `.spec.completions` 都设置为比 1 大的值，
那就有可能同时出现多个 Pod 运行的情况。
为此，你的 Pod 也必须能够处理并发性问题。

<!--
### Pod backoff failure policy

There are situations where you want to fail a Job after some amount of retries
due to a logical error in configuration etc.
To do so, set `.spec.backoffLimit` to specify the number of retries before
considering a Job as failed. The back-off limit is set by default to 6. Failed
Pods associated with the Job are recreated by the Job controller with an
exponential back-off delay (10s, 20s, 40s ...) capped at six minutes. The
back-off count is reset when a Job's Pod is deleted or successful without any
other Pods for the Job failing around that time.
-->
### Pod 回退失效策略

在有些情形下，你可能希望 Job 在经历若干次重试之后直接进入失败状态，因为这很
可能意味着遇到了配置错误。
为了实现这点，可以将 `.spec.backoffLimit` 设置为视 Job 为失败之前的重试次数。
失效回退的限制值默认为 6。
与 Job 相关的失效的 Pod 会被 Job 控制器重建，回退重试时间将会按指数增长
（从 10 秒、20 秒到 40 秒）最多至 6 分钟。
当 Job 的 Pod 被删除时，或者 Pod 成功时没有其它 Pod 处于失败状态，失效回退的次数也会被重置（为 0）。

<!--
If your job has `restartPolicy = "OnFailure"`, keep in mind that your container running the Job
will be terminated once the job backoff limit has been reached. This can make debugging the Job's executable more difficult. We suggest setting
`restartPolicy = "Never"` when debugging the Job or using a logging system to ensure output
from failed Jobs is not lost inadvertently.
-->
{{< note >}}
如果你的 Job 的 `restartPolicy` 被设置为 "OnFailure"，就要注意运行该 Job 的容器
会在 Job 到达失效回退次数上限时自动被终止。
这会使得调试 Job 中可执行文件的工作变得非常棘手。
我们建议在调试 Job 时将 `restartPolicy` 设置为 "Never"，
或者使用日志系统来确保失效 Jobs 的输出不会意外遗失。
{{< /note >}}

<!--
## Job termination and cleanup

When a Job completes, no more Pods are created, but the Pods are not deleted either.  Keeping them around
allows you to still view the logs of completed pods to check for errors, warnings, or other diagnostic output.
The job object also remains after it is completed so that you can view its status.  It is up to the user to delete
old jobs after noting their status.  Delete the job with `kubectl` (e.g. `kubectl delete jobs/pi` or `kubectl delete -f ./job.yaml`). When you delete the job using `kubectl`, all the pods it created are deleted too.
-->
## Job 终止与清理

Job 完成时不会再创建新的 Pod，不过已有的 Pod 也不会被删除。
保留这些 Pod 使得你可以查看已完成的 Pod 的日志输出，以便检查错误、警告
或者其它诊断性输出。
Job 完成时 Job 对象也一样被保留下来，这样你就可以查看它的状态。
在查看了 Job 状态之后删除老的 Job 的操作留给了用户自己。
你可以使用 `kubectl` 来删除 Job（例如，`kubectl delete jobs/pi`
或者 `kubectl delete -f ./job.yaml`）。
当使用 `kubectl` 来删除 Job 时，该 Job 所创建的 Pods 也会被删除。

<!--
By default, a Job will run uninterrupted unless a Pod fails (`restartPolicy=Never`) or a Container exits in error (`restartPolicy=OnFailure`), at which point the Job defers to the
`.spec.backoffLimit` described above. Once `.spec.backoffLimit` has been reached the Job will be marked as failed and any running Pods will be terminated.

Another way to terminate a Job is by setting an active deadline.
Do this by setting the `.spec.activeDeadlineSeconds` field of the Job to a number of seconds.
The `activeDeadlineSeconds` applies to the duration of the job, no matter how many Pods are created.
Once a Job reaches `activeDeadlineSeconds`, all of its running Pods are terminated and the Job status will become `type: Failed` with `reason: DeadlineExceeded`.
-->
默认情况下，Job 会持续运行，除非某个 Pod 失败（`restartPolicy=Never`）
或者某个容器出错退出（`restartPolicy=OnFailure`）。
这时，Job 基于前述的 `spec.backoffLimit` 来决定是否以及如何重试。
一旦重试次数到达 `.spec.backoffLimit` 所设的上限，Job 会被标记为失败，
其中运行的 Pods 都会被终止。

终止 Job 的另一种方式是设置一个活跃期限。
你可以为 Job 的 `.spec.activeDeadlineSeconds` 设置一个秒数值。
该值适用于 Job 的整个生命期，无论 Job 创建了多少个 Pod。
一旦 Job 运行时间达到 `activeDeadlineSeconds` 秒，其所有运行中的 Pod
都会被终止，并且 Job 的状态更新为 `type: Failed`
及 `reason: DeadlineExceeded`。

<!--
Note that a Job's `.spec.activeDeadlineSeconds` takes precedence over its `.spec.backoffLimit`. Therefore, a Job that is retrying one or more failed Pods will not deploy additional Pods once it reaches the time limit specified by `activeDeadlineSeconds`, even if the `backoffLimit` is not yet reached.

Example:
-->
注意 Job 的 `.spec.activeDeadlineSeconds` 优先级高于其 `.spec.backoffLimit` 设置。
因此，如果一个 Job 正在重试一个或多个失效的 Pod，该 Job 一旦到达
`activeDeadlineSeconds` 所设的时限即不再部署额外的 Pod，即使其重试次数还未
达到 `backoffLimit` 所设的限制。

例如：

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: pi-with-timeout
spec:
  backoffLimit: 5
  activeDeadlineSeconds: 100
  template:
    spec:
      containers:
      - name: pi
        image: perl
        command: ["perl",  "-Mbignum=bpi", "-wle", "print bpi(2000)"]
      restartPolicy: Never
```
<!--
Note that both the Job spec and the [Pod template spec](/docs/concepts/workloads/pods/init-containers/#detailed-behavior) within the Job have an `activeDeadlineSeconds` field. Ensure that you set this field at the proper level.

Keep in mind that the `restartPolicy` applies to the Pod, and not to the Job itself: there is no automatic Job restart once the Job status is `type: Failed`.
That is, the Job termination mechanisms activated with `.spec.activeDeadlineSeconds` and `.spec.backoffLimit` result in a permanent Job failure that requires manual intervention to resolve.
-->
注意 Job 规约和 Job 中的
[Pod 模版规约](/zh/docs/concepts/workloads/pods/init-containers/#detailed-behavior)
都有 `activeDeadlineSeconds` 字段。
请确保你在合适的层次设置正确的字段。

还要注意的是，`restartPolicy` 对应的是 Pod，而不是 Job 本身：
一旦 Job 状态变为 `type: Failed`，就不会再发生 Job 重启的动作。
换言之，由 `.spec.activeDeadlineSeconds` 和 `.spec.backoffLimit` 所触发的 Job 终结机制
都会导致 Job 永久性的失败，而这类状态都需要手工干预才能解决。

<!--
## Clean up finished jobs automatically

Finished Jobs are usually no longer needed in the system. Keeping them around in
the system will put pressure on the API server. If the Jobs are managed directly
by a higher level controller, such as
[CronJobs](/docs/concepts/workloads/controllers/cron-jobs/), the Jobs can be
cleaned up by CronJobs based on the specified capacity-based cleanup policy.

### TTL mechanism for finished Jobs
-->
## 自动清理完成的 Job   {#clean-up-finished-jobs-automatically}

完成的 Job 通常不需要留存在系统中。在系统中一直保留它们会给 API
服务器带来额外的压力。
如果 Job 由某种更高级别的控制器来管理，例如
[CronJobs](/zh/docs/concepts/workloads/controllers/cron-jobs/)，
则 Job 可以被 CronJob 基于特定的根据容量裁定的清理策略清理掉。

### 已完成 Job 的 TTL 机制  {#ttl-mechanisms-for-finished-jobs}

{{< feature-state for_k8s_version="v1.12" state="alpha" >}}

<!--
Another way to clean up finished Jobs (either `Complete` or `Failed`)
automatically is to use a TTL mechanism provided by a
[TTL controller](/docs/concepts/workloads/controllers/ttlafterfinished/) for
finished resources, by specifying the `.spec.ttlSecondsAfterFinished` field of
the Job.

When the TTL controller cleans up the Job, it will delete the Job cascadingly,
i.e. delete its dependent objects, such as Pods, together with the Job. Note
that when the Job is deleted, its lifecycle guarantees, such as finalizers, will
be honored.

For example:
-->
自动清理已完成 Job （状态为 `Complete` 或 `Failed`）的另一种方式是使用由
[TTL 控制器](/zh/docs/concepts/workloads/controllers/ttlafterfinished/)所提供
的 TTL 机制。
通过设置 Job 的 `.spec.ttlSecondsAfterFinished` 字段，可以让该控制器清理掉
已结束的资源。

TTL 控制器清理 Job 时，会级联式地删除 Job 对象。
换言之，它会删除所有依赖的对象，包括 Pod 及 Job 本身。
注意，当 Job 被删除时，系统会考虑其生命周期保障，例如其 Finalizers。

例如：

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: pi-with-ttl
spec:
  ttlSecondsAfterFinished: 100
  template:
    spec:
      containers:
      - name: pi
        image: perl
        command: ["perl",  "-Mbignum=bpi", "-wle", "print bpi(2000)"]
      restartPolicy: Never
```

<!--
The Job `pi-with-ttl` will be eligible to be automatically deleted, `100`
seconds after it finishes.

If the field is set to `0`, the Job will be eligible to be automatically deleted
immediately after it finishes. If the field is unset, this Job won't be cleaned
up by the TTL controller after it finishes.

Note that this TTL mechanism is alpha, with feature gate `TTLAfterFinished`. For
more information, see the documentation for
[TTL controller](/docs/concepts/workloads/controllers/ttlafterfinished/) for
finished resources.
-->
Job `pi-with-ttl` 在结束 100 秒之后，可以成为被自动删除的对象。

如果该字段设置为 `0`，Job 在结束之后立即成为可被自动删除的对象。
如果该字段没有设置，Job 不会在结束之后被 TTL 控制器自动清除。

注意这种 TTL 机制仍然是一种 Alpha 状态的功能特性，需要配合 `TTLAfterFinished`
特性门控使用。有关详细信息，可参考
[TTL 控制器](/zh/docs/concepts/workloads/controllers/ttlafterfinished/)的文档。

<!--
## Job patterns

The Job object can be used to support reliable parallel execution of Pods.  The Job object is not
designed to support closely-communicating parallel processes, as commonly found in scientific
computing.  It does support parallel processing of a set of independent but related *work items*.
These might be emails to be sent, frames to be rendered, files to be transcoded, ranges of keys in a
NoSQL database to scan, and so on.
-->
## Job 模式  {#job-patterns}

Job 对象可以用来支持多个 Pod 的可靠的并发执行。
Job 对象不是设计用来支持相互通信的并行进程的，后者一般在科学计算中应用较多。
Job 的确能够支持对一组相互独立而又有所关联的 *工作条目* 的并行处理。
这类工作条目可能是要发送的电子邮件、要渲染的视频帧、要编解码的文件、NoSQL
数据库中要扫描的主键范围等等。

<!--
In a complex system, there may be multiple different sets of work items.  Here we are just
considering one set of work items that the user wants to manage together &mdash; a *batch job*.

There are several different patterns for parallel computation, each with strengths and weaknesses.
The tradeoffs are:
-->
在一个复杂系统中，可能存在多个不同的工作条目集合。这里我们仅考虑用户希望一起管理的
工作条目集合之一 &mdash; *批处理作业*。

并行计算的模式有好多种，每种都有自己的强项和弱点。这里要权衡的因素有：

<!--
- One Job object for each work item, vs. a single Job object for all work items.  The latter is
  better for large numbers of work items.  The former creates some overhead for the user and for the
  system to manage large numbers of Job objects.
- Number of pods created equals number of work items, vs. each Pod can process multiple work items.
  The former typically requires less modification to existing code and containers.  The latter
  is better for large numbers of work items, for similar reasons to the previous bullet.
- Several approaches use a work queue.  This requires running a queue service,
  and modifications to the existing program or container to make it use the work queue.
  Other approaches are easier to adapt to an existing containerised application.
-->
- 每个工作条目对应一个 Job 或者所有工作条目对应同一 Job 对象。
  后者更适合处理大量工作条目的场景；
  前者会给用户带来一些额外的负担，而且需要系统管理大量的 Job 对象。
- 创建与工作条目相等的 Pod 或者令每个 Pod 可以处理多个工作条目。
  前者通常不需要对现有代码和容器做较大改动；
  后者则更适合工作条目数量较大的场合，原因同上。
- 有几种技术都会用到工作队列。这意味着需要运行一个队列服务，并修改现有程序或容器
  使之能够利用该工作队列。
  与之比较，其他方案在修改现有容器化应用以适应需求方面可能更容易一些。

<!--
The tradeoffs are summarized here, with columns 2 to 4 corresponding to the above tradeoffs.
The pattern names are also links to examples and more detailed description.
-->
下面是对这些权衡的汇总，列 2 到 4 对应上面的权衡比较。
模式的名称对应了相关示例和更详细描述的链接。

| 模式  | 单个 Job 对象 | Pods 数少于工作条目数？ | 直接使用应用无需修改? |
| ----- |:-------------:|:-----------------------:|:---------------------:|
| [每工作条目一 Pod 的队列](/zh/docs/tasks/job/coarse-parallel-processing-work-queue/) | ✓ | | 有时 |
| [Pod 数量可变的队列](/zh/docs/tasks/job/fine-parallel-processing-work-queue/) | ✓ | ✓ |  |
| [静态任务分派的带索引的 Job](/zh/docs/tasks/job/indexed-parallel-processing-static) | ✓ |  | ✓ |
| [Job 模版扩展](/zh/docs/tasks/job/parallel-processing-expansion/)  |  |  | ✓ |

<!--
When you specify completions with `.spec.completions`, each Pod created by the Job controller
has an identical [`spec`](https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status).  This means that
all pods for a task will have the same command line and the same
image, the same volumes, and (almost) the same environment variables.  These patterns
are different ways to arrange for pods to work on different things.

This table shows the required settings for `.spec.parallelism` and `.spec.completions` for each of the patterns.
Here, `W` is the number of work items.
-->
当你使用 `.spec.completions` 来设置完成数时，Job 控制器所创建的每个 Pod
使用完全相同的 [`spec`](https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status)。
这意味着任务的所有 Pod 都有相同的命令行，都使用相同的镜像和数据卷，甚至连
环境变量都（几乎）相同。
这些模式是让每个 Pod 执行不同工作的几种不同形式。

下表显示的是每种模式下 `.spec.parallelism` 和 `.spec.completions` 所需要的设置。
其中，`W` 表示的是工作条目的个数。

| 模式  | `.spec.completions` |  `.spec.parallelism` |
| ----- |:-------------------:|:--------------------:|
| [每工作条目一 Pod 的队列](/zh/docs/tasks/job/coarse-parallel-processing-work-queue/) | W | 任意值 |
| [Pod 个数可变的队列](/zh/docs/tasks/job/fine-parallel-processing-work-queue/) | 1 | 任意值 |
| [静态任务分派的带索引的 Job](/zh/docs/tasks/job/indexed-parallel-processing-static) | W |  | 任意值 |
| [Job 模版扩展](/zh/docs/tasks/job/parallel-processing-expansion/) | 1 | 应该为 1 |

<!--
## Advanced usage

### Suspending a Job
-->
## 高级用法   {#advanced-usage}

### 挂起 Job   {#suspending-a-job}

{{< feature-state for_k8s_version="v1.21" state="alpha" >}}

{{< note >}}
<!--
Suspending Jobs is available in Kubernetes versions 1.21 and above. You must
enable the `SuspendJob` [feature gate](/docs/reference/command-line-tools-reference/feature-gates/)
on the [API server](/docs/reference/command-line-tools-reference/kube-apiserver/)
and the [controller manager](/docs/reference/command-line-tools-reference/kube-controller-manager/)
in order to use this feature.
-->
在 Kubernetes 1.21 及更高版本中可以执行挂起（Suspending）Job 的操作。
你必须在
[API 服务器](/zh/docs/reference/command-line-tools-reference/kube-apiserver/)
和[控制器管理器](/zh/docs/reference/command-line-tools-reference/kube-controller-manager/)
上启用 `SuspendJob` 这一
[特性门控](/docs/reference/command-line-tools-reference/feature-gates/)
才能执行此操作，
{{< /note >}}

<!--
When a Job is created, the Job controller will immediately begin creating Pods
to satisfy the Job's requirements and will continue to do so until the Job is
complete. However, you may want to temporarily suspend a Job's execution and
resume it later. To suspend a Job, you can update the `.spec.suspend` field of
the Job to true; later, when you want to resume it again, update it to false.
Creating a Job with `.spec.suspend` set to true will create it in the suspended
state.
-->
Job 被创建时，Job 控制器会马上开始执行 Pod 创建操作以满足 Job 的需求，
并持续执行此操作直到 Job 完成为止。
不过你可能想要暂时挂起 Job 执行，之后再恢复其执行。
要挂起一个 Job，你可以将 Job 的 `.spec.suspend` 字段更新为 true。
之后，当你希望恢复其执行时，将其更新为 false。
创建一个 `.spec.suspend` 被设置为 true 的 Job 本质上会将其创建为被挂起状态。

<!--
When a Job is resumed from suspension, its `.status.startTime` field will be
reset to the current time. This means that the `.spec.activeDeadlineSeconds`
timer will be stopped and reset when a Job is suspended and resumed.
-->
当 Job 被从挂起状态恢复执行时，其 `.status.startTime` 字段会被重置为
当前的时间。这意味着 `.spec.activeDeadlineSeconds` 计时器会在 Job 挂起时
被停止，并在 Job 恢复执行时复位。

<!--
Remember that suspending a Job will delete all active Pods. When the Job is
suspended, your [Pods will be terminated](/docs/concepts/workloads/pods/pod-lifecycle/#pod-termination)
with a SIGTERM signal. The Pod's graceful termination period will be honored and
your Pod must handle this signal in this period. This may involve saving
progress for later or undoing changes. Pods terminated this way will not count
towards the Job's `completions` count.
-->
要记住的是，挂起 Job 会删除其所有活跃的 Pod。当 Job 被挂起时，你的 Pod 会
收到 SIGTERM 信号而被[终止](/docs/concepts/workloads/pods/pod-lifecycle/#pod-termination)。
Pod 的体面终止期限会被考虑，不过 Pod 自身也必须在此期限之内处理完信号。
处理逻辑可能包括保存进度以便将来恢复，或者取消已经做出的变更等等。
Pod 以这种形式终止时，不会被记入 Job 的 `completions` 计数。

<!--
An example Job definition in the suspended state can be like so:
-->
处于被挂起状态的 Job 的定义示例可能是这样子：

```shell
kubectl get job myjob -o yaml
```

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: myjob
spec:
  suspend: true
  parallelism: 1
  completions: 5
  template:
    spec:
      ...
```

<!--
The Job's status can be used to determine if a Job is suspended or has been
suspended in the past:
-->
Job 的 `status` 可以用来确定 Job 是否被挂起，或者曾经被挂起。

```shell
kubectl get jobs/myjob -o yaml
```

```json
apiVersion: batch/v1
kind: Job
# .metadata and .spec omitted
status:
  conditions:
  - lastProbeTime: "2021-02-05T13:14:33Z"
    lastTransitionTime: "2021-02-05T13:14:33Z"
    status: "True"
    type: Suspended
  startTime: "2021-02-05T13:13:48Z"
```

<!--
The Job condition of type "Suspended" with status "True" means the Job is
suspended; the `lastTransitionTime` field can be used to determine how long the
Job has been suspended for. If the status of that condition is "False", then the
Job was previously suspended and is now running. If such a condition does not
exist in the Job's status, the Job has never been stopped.

Events are also created when the Job is suspended and resumed:
-->
Job 的 "Suspended" 类型的状况在状态值为 "True" 时意味着 Job 正被
挂起；`lastTransitionTime` 字段可被用来确定 Job 被挂起的时长。
如果此状况字段的取值为 "False"，则 Job 之前被挂起且现在在运行。
如果 "Suspended" 状况在 `status` 字段中不存在，则意味着 Job 从未
被停止执行。

当 Job 被挂起和恢复执行时，也会生成事件：

```shell
kubectl describe jobs/myjob
```

```
Name:           myjob
...
Events:
  Type    Reason            Age   From            Message
  ----    ------            ----  ----            -------
  Normal  SuccessfulCreate  12m   job-controller  Created pod: myjob-hlrpl
  Normal  SuccessfulDelete  11m   job-controller  Deleted pod: myjob-hlrpl
  Normal  Suspended         11m   job-controller  Job suspended
  Normal  SuccessfulCreate  3s    job-controller  Created pod: myjob-jvb44
  Normal  Resumed           3s    job-controller  Job resumed
```

<!--
The last four events, particularly the "Suspended" and "Resumed" events, are
directly a result of toggling the `.spec.suspend` field. In the time between
these two events, we see that no Pods were created, but Pod creation restarted
as soon as the Job was resumed.
-->
最后四个四件，特别是 "Suspended" 和 "Resumed" 事件，都是因为 `.spec.suspend`
字段值被改来改去造成的。在这两个事件之间，我们看到没有 Pod 被创建，不过当
Job 被恢复执行时，Pod 创建操作立即被重启执行。

<!--
### Specifying your own Pod selector {#specifying-your-own-pod-selector}

Normally, when you create a Job object, you do not specify `.spec.selector`.
The system defaulting logic adds this field when the Job is created.
It picks a selector value that will not overlap with any other jobs.

However, in some cases, you might need to override this automatically set selector.
To do this, you can specify the `.spec.selector` of the Job.
-->
### 指定你自己的 Pod 选择算符 {#specifying-your-own-pod-selector}

通常，当你创建一个 Job 对象时，你不会设置 `.spec.selector`。
系统的默认值填充逻辑会在创建 Job 时添加此字段。
它会选择一个不会与任何其他 Job 重叠的选择算符设置。

不过，有些场合下，你可能需要重载这个自动设置的选择算符。
为了实现这点，你可以手动设置 Job 的 `spec.selector` 字段。

<!--
Be very careful when doing this.  If you specify a label selector which is not
unique to the pods of that Job, and which matches unrelated Pods, then pods of the unrelated
job may be deleted, or this Job may count other Pods as completing it, or one or both
Jobs may refuse to create Pods or run to completion.  If a non-unique selector is
chosen, then other controllers (e.g. ReplicationController) and their Pods may behave
in unpredictable ways too.  Kubernetes will not stop you from making a mistake when
specifying `.spec.selector`.
-->
做这个操作时请务必小心。
如果你所设定的标签选择算符并不唯一针对 Job 对应的 Pod 集合，甚或该算符还能匹配
其他无关的 Pod，这些无关的 Job 的 Pod 可能会被删除。
或者当前 Job 会将另外一些 Pod 当作是完成自身工作的 Pods，
又或者两个 Job 之一或者二者同时都拒绝创建 Pod，无法运行至完成状态。
如果所设置的算符不具有唯一性，其他控制器（如 RC 副本控制器）及其所管理的 Pod
集合可能会变得行为不可预测。
Kubernetes 不会在你设置 `.spec.selector` 时尝试阻止你犯这类错误。

<!--
Here is an example of a case when you might want to use this feature.

Say Job `old` is already running.  You want existing Pods
to keep running, but you want the rest of the Pods it creates
to use a different pod template and for the Job to have a new name.
You cannot update the Job because these fields are not updatable.
Therefore, you delete Job `old` but _leave its pods
running_, using `kubectl delete jobs/old -cascade=orphan`.
Before deleting it, you make a note of what selector it uses:
-->
下面是一个示例场景，在这种场景下你可能会使用刚刚讲述的特性。

假定名为 `old` 的 Job 已经处于运行状态。
你希望已有的 Pod 继续运行，但你希望 Job 接下来要创建的其他 Pod
使用一个不同的 Pod 模版，甚至希望 Job 的名字也发生变化。
你无法更新现有的 Job，因为这些字段都是不可更新的。
因此，你会删除 `old` Job，但 _允许该 Job 的 Pod 集合继续运行_。
这是通过 `kubectl delete jobs/old --cascade=orphan` 实现的。
在删除之前，我们先记下该 Job 所使用的选择算符。

```shell
kubectl get job old -o yaml
```

输出类似于：

```yaml
kind: Job
metadata:
  name: old
  ...
spec:
  selector:
    matchLabels:
      controller-uid: a8f3d00d-c6d2-11e5-9f87-42010af00002
  ...
```

<!--
Then you create a new Job with name `new` and you explicitly specify the same selector.
Since the existing Pods have label `controller-uid=a8f3d00d-c6d2-11e5-9f87-42010af00002`,
they are controlled by Job `new` as well.

You need to specify `manualSelector: true` in the new Job since you are not using
the selector that the system normally generates for you automatically.
-->
接下来你会创建名为 `new` 的新 Job，并显式地为其设置相同的选择算符。
由于现有 Pod 都具有标签 `controller-uid=a8f3d00d-c6d2-11e5-9f87-42010af00002`，
它们也会被名为 `new` 的 Job 所控制。

你需要在新 Job 中设置 `manualSelector: true`，因为你并未使用系统通常自动为你
生成的选择算符。 

```yaml
kind: Job
metadata:
  name: new
  ...
spec:
  manualSelector: true
  selector:
    matchLabels:
      controller-uid: a8f3d00d-c6d2-11e5-9f87-42010af00002
  ...
```

<!--
The new Job itself will have a different uid from `a8f3d00d-c6d2-11e5-9f87-42010af00002`.  Setting
`manualSelector: true` tells the system to that you know what you are doing and to allow this
mismatch.
-->
新的 Job 自身会有一个不同于 `a8f3d00d-c6d2-11e5-9f87-42010af00002` 的唯一 ID。
设置 `manualSelector: true` 是在告诉系统你知道自己在干什么并要求系统允许这种不匹配
的存在。

<!--
## Alternatives

### Bare Pods

When the node that a Pod is running on reboots or fails, the pod is terminated
and will not be restarted.  However, a Job will create new Pods to replace terminated ones.
For this reason, we recommend that you use a Job rather than a bare Pod, even if your application
requires only a single Pod.
-->
## 替代方案  {#alternatives}

### 裸 Pod  {#bare-pods}

当 Pod 运行所在的节点重启或者失败，Pod 会被终止并且不会被重启。
Job 会重新创建新的 Pod 来替代已终止的 Pod。
因为这个原因，我们建议你使用 Job 而不是独立的裸 Pod，
即使你的应用仅需要一个 Pod。

<!--
### Replication Controller

Jobs are complementary to [Replication Controllers](/docs/user-guide/replication-controller).
A Replication Controller manages Pods which are not expected to terminate (e.g. web servers), and a Job
manages Pods that are expected to terminate (e.g. batch tasks).

As discussed in [Pod Lifecycle](/docs/concepts/workloads/pods/pod-lifecycle/), `Job` is *only* appropriate
for pods with `RestartPolicy` equal to `OnFailure` or `Never`.
(Note: If `RestartPolicy` is not set, the default value is `Always`.)
-->
### 副本控制器    {#replication-controller}

Job 与[副本控制器](/zh/docs/concepts/workloads/controllers/replicationcontroller/)是彼此互补的。
副本控制器管理的是那些不希望被终止的 Pod （例如，Web 服务器），
Job 管理的是那些希望被终止的 Pod（例如，批处理作业）。

正如在 [Pod 生命期](/zh/docs/concepts/workloads/pods/pod-lifecycle/) 中讨论的，
`Job` 仅适合于 `restartPolicy` 设置为 `OnFailure` 或 `Never` 的 Pod。
注意：如果 `restartPolicy` 未设置，其默认值是 `Always`。

<!--
### Single Job starts controller Pod

Another pattern is for a single Job to create a Pod which then creates other Pods, acting as a sort
of custom controller for those Pods.  This allows the most flexibility, but may be somewhat
complicated to get started with and offers less integration with Kubernetes.
-->
### 单个 Job 启动控制器 Pod

另一种模式是用唯一的 Job 来创建 Pod，而该 Pod 负责启动其他 Pod，因此扮演了一种
后启动 Pod 的控制器的角色。
这种模式的灵活性更高，但是有时候可能会把事情搞得很复杂，很难入门，
并且与 Kubernetes 的集成度很低。

<!--
One example of this pattern would be a Job which starts a Pod which runs a script that in turn
starts a Spark master controller (see [spark example](https://github.com/kubernetes/examples/tree/{{< param "githubbranch" >}}/staging/spark/README.md)), runs a spark
driver, and then cleans up.

An advantage of this approach is that the overall process gets the completion guarantee of a Job
object, but maintains complete control over what Pods are created and how work is assigned to them.
-->
这种模式的实例之一是用 Job 来启动一个运行脚本的 Pod，脚本负责启动 Spark
主控制器（参见 [Spark 示例](https://github.com/kubernetes/examples/tree/{{< param "githubbranch" >}}/staging/spark/README.md)），
运行 Spark 驱动，之后完成清理工作。

这种方法的优点之一是整个过程得到了 Job 对象的完成保障，
同时维持了对创建哪些 Pod、如何向其分派工作的完全控制能力，

<!--
## Cron Jobs {#cron-jobs}

You can use a [`CronJob`](/docs/concepts/workloads/controllers/cron-jobs/) to create a Job that will run at specified times/dates, similar to the Unix tool `cron`.
-->
## Cron Jobs {#cron-jobs}

你可以使用 [`CronJob`](/zh/docs/concepts/workloads/controllers/cron-jobs/)
创建一个在指定时间/日期运行的 Job，类似于 UNIX 系统上的 `cron` 工具。

