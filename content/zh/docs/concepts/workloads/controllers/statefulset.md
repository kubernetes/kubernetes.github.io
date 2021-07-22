---
title: StatefulSets
content_type: concept
weight: 30
---

<!--
title: StatefulSets
content_type: concept
weight: 40
-->

<!-- overview -->

<!--
StatefulSet is the workload API object used to manage stateful applications.
-->
StatefulSet 是用来管理有状态应用的工作负载 API 对象。

{{< glossary_definition term_id="statefulset" length="all" >}}

<!-- body -->

<!--
## Using StatefulSets

StatefulSets are valuable for applications that require one or more of the
following.
-->
## 使用 StatefulSets

StatefulSets 对于需要满足以下一个或多个需求的应用程序很有价值：

<!--
* Stable, unique network identifiers.
* Stable, persistent storage.
* Ordered, graceful deployment and scaling.
* Ordered, automated rolling updates.
-->
* 稳定的、唯一的网络标识符。
* 稳定的、持久的存储。
* 有序的、优雅的部署和缩放。
* 有序的、自动的滚动更新。

<!--
In the above, stable is synonymous with persistence across Pod (re)scheduling.
If an application doesn't require any stable identifiers or ordered deployment,
deletion, or scaling, you should deploy your application using a workload object
that provides a set of stateless replicas.
[Deployment](/docs/concepts/workloads/controllers/deployment/) or
[ReplicaSet](/docs/concepts/workloads/controllers/replicaset/) may be better suited to your stateless needs.
-->
在上面描述中，“稳定的”意味着 Pod 调度或重调度的整个过程是有持久性的。
如果应用程序不需要任何稳定的标识符或有序的部署、删除或伸缩，则应该使用
由一组无状态的副本控制器提供的工作负载来部署应用程序，比如
[Deployment](/zh/docs/concepts/workloads/controllers/deployment/) 或者
[ReplicaSet](/zh/docs/concepts/workloads/controllers/replicaset/)
可能更适用于你的无状态应用部署需要。

<!--
## Limitations
-->
## 限制  {#limitations}

<!--
* The storage for a given Pod must either be provisioned by a [PersistentVolume Provisioner](https://github.com/kubernetes/examples/tree/{{< param "githubbranch" >}}/staging/persistent-volume-provisioning/README.md) based on the requested `storage class`, or pre-provisioned by an admin.
* Deleting and/or scaling a StatefulSet down will *not* delete the volumes associated with the StatefulSet. This is done to ensure data safety, which is generally more valuable than an automatic purge of all related StatefulSet resources.
* StatefulSets currently require a [Headless Service](/docs/concepts/services-networking/service/#headless-services) to be responsible for the network identity of the Pods. You are responsible for creating this Service.
* StatefulSets do not provide any guarantees on the termination of pods when a StatefulSet is deleted. To achieve ordered and graceful termination of the pods in the StatefulSet, it is possible to scale the StatefulSet down to 0 prior to deletion.
* When using [Rolling Updates](#rolling-updates) with the default
  [Pod Management Policy](#pod-management-policies) (`OrderedReady`),
  it's possible to get into a broken state that requires
  [manual intervention to repair](#forced-rollback).
-->
* 给定 Pod 的存储必须由
  [PersistentVolume 驱动](https://github.com/kubernetes/examples/tree/{{< param "githubbranch" >}}/staging/persistent-volume-provisioning/README.md)
  基于所请求的 `storage class` 来提供，或者由管理员预先提供。
* 删除或者收缩 StatefulSet 并*不会*删除它关联的存储卷。
  这样做是为了保证数据安全，它通常比自动清除 StatefulSet 所有相关的资源更有价值。
* StatefulSet 当前需要[无头服务](/zh/docs/concepts/services-networking/service/#headless-services)
  来负责 Pod 的网络标识。你需要负责创建此服务。
* 当删除 StatefulSets 时，StatefulSet 不提供任何终止 Pod 的保证。
  为了实现 StatefulSet 中的 Pod 可以有序地且体面地终止，可以在删除之前将 StatefulSet
  缩放为 0。
* 在默认 [Pod 管理策略](#pod-management-policies)(`OrderedReady`) 时使用
  [滚动更新](#rolling-updates)，可能进入需要[人工干预](#forced-rollback)
  才能修复的损坏状态。

<!--
## Components
The example below demonstrates the components of a StatefulSet.
-->
## 组件  {#components}

下面的示例演示了 StatefulSet 的组件。

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx
  labels:
    app: nginx
spec:
  ports:
  - port: 80
    name: web
  clusterIP: None
  selector:
    app: nginx
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: web
spec:
  selector:
    matchLabels:
      app: nginx # has to match .spec.template.metadata.labels
  serviceName: "nginx"
  replicas: 3 # by default is 1
  template:
    metadata:
      labels:
        app: nginx # has to match .spec.selector.matchLabels
    spec:
      terminationGracePeriodSeconds: 10
      containers:
      - name: nginx
        image: k8s.gcr.io/nginx-slim:0.8
        ports:
        - containerPort: 80
          name: web
        volumeMounts:
        - name: www
          mountPath: /usr/share/nginx/html
  volumeClaimTemplates:
  - metadata:
      name: www
    spec:
      accessModes: [ "ReadWriteOnce" ]
      storageClassName: "my-storage-class"
      resources:
        requests:
          storage: 1Gi
```

<!--
In the above example:

* A Headless Service, named `nginx`, is used to control the network domain.
* The StatefulSet, named `web`, has a Spec that indicates that 3 replicas of the nginx container will be launched in unique Pods.
* The `volumeClaimTemplates` will provide stable storage using [PersistentVolumes](/docs/concepts/storage/persistent-volumes/) provisioned by a PersistentVolume Provisioner.

The name of a StatefulSet object must be a valid
[DNS subdomain name](/docs/concepts/overview/working-with-objects/names#dns-subdomain-names).

-->
上述例子中：

* 名为 `nginx` 的 Headless Service 用来控制网络域名。
* 名为 `web` 的 StatefulSet 有一个 Spec，它表明将在独立的 3 个 Pod 副本中启动 nginx 容器。
* `volumeClaimTemplates` 将通过 PersistentVolumes 驱动提供的
  [PersistentVolumes](/zh/docs/concepts/storage/persistent-volumes/) 来提供稳定的存储。

StatefulSet 的命名需要遵循[DNS 子域名](/zh/docs/concepts/overview/working-with-objects/names#dns-subdomain-names)规范。

<!--
## Pod Selector
-->
## Pod 选择算符     {#pod-selector}

<!--
You must set the `.spec.selector` field of a StatefulSet to match the labels of its `.spec.template.metadata.labels`. Prior to Kubernetes 1.8, the `.spec.selector` field was defaulted when omitted. In 1.8 and later versions, failing to specify a matching Pod Selector will result in a validation error during StatefulSet creation.
-->
你必须设置 StatefulSet 的 `.spec.selector` 字段，使之匹配其在
`.spec.template.metadata.labels` 中设置的标签。在 Kubernetes 1.8 版本之前，
被忽略 `.spec.selector` 字段会获得默认设置值。
在 1.8 和以后的版本中，未指定匹配的 Pod 选择器将在创建 StatefulSet 期间导致验证错误。

<!--
## Pod Identity

StatefulSet Pods have a unique identity that is comprised of an ordinal, a
stable network identity, and stable storage. The identity sticks to the Pod,
regardless of which node it's (re)scheduled on.
-->
## Pod 标识   {#pod-identity}

StatefulSet Pod 具有唯一的标识，该标识包括顺序标识、稳定的网络标识和稳定的存储。
该标识和 Pod 是绑定的，不管它被调度在哪个节点上。

<!--
### Ordinal Index

For a StatefulSet with N replicas, each Pod in the StatefulSet will be
assigned an integer ordinal, from 0 up through N-1, that is unique over the Set.
-->
### 有序索引   {#ordinal-index}

对于具有 N 个副本的 StatefulSet，StatefulSet 中的每个 Pod 将被分配一个整数序号，
从 0 到 N-1，该序号在 StatefulSet 上是唯一的。

<!--
### Stable Network ID

Each Pod in a StatefulSet derives its hostname from the name of the StatefulSet
and the ordinal of the Pod. The pattern for the constructed hostname
is `$(statefulset name)-$(ordinal)`. The example above will create three Pods
named `web-0,web-1,web-2`.
A StatefulSet can use a [Headless Service](/docs/concepts/services-networking/service/#headless-services)
to control the domain of its Pods. The domain managed by this Service takes the form:
`$(service name).$(namespace).svc.cluster.local`, where "cluster.local" is the
cluster domain.
As each Pod is created, it gets a matching DNS subdomain, taking the form:
`$(podname).$(governing service domain)`, where the governing service is defined
by the `serviceName` field on the StatefulSet.
-->
### 稳定的网络 ID   {#stable-network-id}

StatefulSet 中的每个 Pod 根据 StatefulSet 的名称和 Pod 的序号派生出它的主机名。
组合主机名的格式为`$(StatefulSet 名称)-$(序号)`。
上例将会创建三个名称分别为 `web-0、web-1、web-2` 的 Pod。
StatefulSet 可以使用 [无头服务](/zh/docs/concepts/services-networking/service/#headless-services)
控制它的 Pod 的网络域。管理域的这个服务的格式为：
`$(服务名称).$(命名空间).svc.cluster.local`，其中 `cluster.local` 是集群域。
一旦每个 Pod 创建成功，就会得到一个匹配的 DNS 子域，格式为：
`$(pod 名称).$(所属服务的 DNS 域名)`，其中所属服务由 StatefulSet 的 `serviceName` 域来设定。

<!--
Depending on how DNS is configured in your cluster, you may not be able to look up the DNS
name for a newly-run Pod immediately. This behavior can occur when other clients in the
cluster have already sent queries for the hostname of the Pod before it was created.
Negative caching (normal in DNS) means that the results of previous failed lookups are
remembered and reused, even after the Pod is running, for at least a few seconds.

If you need to discover Pods promptly after they are created, you have a few options:

- Query the Kubernetes API directly (for example, using a watch) rather than relying on DNS lookups.
- Decrease the time of caching in your Kubernetes DNS provider (typically this means editing the config map for CoreDNS, which currently caches for 30 seconds).


As mentioned in the [limitations](#limitations) section, you are responsible for
creating the [Headless Service](/docs/concepts/services-networking/service/#headless-services)
responsible for the network identity of the pods.

-->
取决于集群域内部 DNS 的配置，有可能无法查询一个刚刚启动的 Pod 的 DNS 命名。
当集群内其他客户端在 Pod 创建完成前发出 Pod 主机名查询时，就会发生这种情况。
负缓存 (在 DNS 中较为常见) 意味着之前失败的查询结果会被记录和重用至少若干秒钟，
即使 Pod 已经正常运行了也是如此。

如果需要在 Pod 被创建之后及时发现它们，有以下选项：

- 直接查询 Kubernetes API（比如，利用 watch 机制）而不是依赖于 DNS 查询
- 缩短 Kubernetes DNS 驱动的缓存时长（通常这意味着修改 CoreDNS 的 ConfigMap，目前缓存时长为 30 秒）

正如[限制](#limitations)中所述，你需要负责创建[无头服务](/zh/docs/concepts/services-networking/service/#headless-services)
以便为 Pod 提供网络标识。

<!--
Here are some examples of choices for Cluster Domain, Service name,
StatefulSet name, and how that affects the DNS names for the StatefulSet's Pods.


Cluster Domain | Service (ns/name) | StatefulSet (ns/name)  | StatefulSet Domain  | Pod DNS | Pod Hostname |
-------------- | ----------------- | ----------------- | -------------- | ------- | ------------ |
 cluster.local | default/nginx     | default/web       | nginx.default.svc.cluster.local | web-{0..N-1}.nginx.default.svc.cluster.local | web-{0..N-1} |
 cluster.local | foo/nginx         | foo/web           | nginx.foo.svc.cluster.local     | web-{0..N-1}.nginx.foo.svc.cluster.local     | web-{0..N-1} |
 kube.local    | foo/nginx         | foo/web           | nginx.foo.svc.kube.local        | web-{0..N-1}.nginx.foo.svc.kube.local        | web-{0..N-1} |

-->
下面给出一些选择集群域、服务名、StatefulSet 名、及其怎样影响 StatefulSet 的 Pod 上的 DNS 名称的示例：

集群域名       | 服务（名字空间/名字）| StatefulSet（名字空间/名字） | StatefulSet 域名 | Pod DNS | Pod 主机名   |
-------------- | -------------------- | ---------------------------- | ---------------- | ------- | ------------ |
 cluster.local | default/nginx     | default/web       | nginx.default.svc.cluster.local | web-{0..N-1}.nginx.default.svc.cluster.local | web-{0..N-1} |
 cluster.local | foo/nginx         | foo/web           | nginx.foo.svc.cluster.local     | web-{0..N-1}.nginx.foo.svc.cluster.local     | web-{0..N-1} |
 kube.local    | foo/nginx         | foo/web           | nginx.foo.svc.kube.local        | web-{0..N-1}.nginx.foo.svc.kube.local        | web-{0..N-1} |

<!--
Cluster Domain will be set to `cluster.local` unless
[otherwise configured](/docs/concepts/services-networking/dns-pod-service/#how-it-works).
-->
{{< note >}}
集群域会被设置为 `cluster.local`，除非有[其他配置](/zh/docs/concepts/services-networking/dns-pod-service/)。
{{< /note >}}

<!--
### Stable Storage

Kubernetes creates one [PersistentVolume](/docs/concepts/storage/persistent-volumes/) for each
VolumeClaimTemplate. In the nginx example above, each Pod will receive a single PersistentVolume
with a StorageClass of `my-storage-class` and 1 Gib of provisioned storage. If no StorageClass
is specified, then the default StorageClass will be used. When a Pod is (re)scheduled
onto a node, its `volumeMounts` mount the PersistentVolumes associated with its
PersistentVolume Claims. Note that, the PersistentVolumes associated with the
Pods' PersistentVolume Claims are not deleted when the Pods, or StatefulSet are deleted.
This must be done manually.
-->
### 稳定的存储  {#stable-storage}

Kubernetes 为每个 VolumeClaimTemplate 创建一个 [PersistentVolume](/zh/docs/concepts/storage/persistent-volumes/)。
在上面的 nginx 示例中，每个 Pod 将会得到基于 StorageClass `my-storage-class` 提供的
1 Gib 的 PersistentVolume。如果没有声明 StorageClass，就会使用默认的 StorageClass。
当一个 Pod 被调度（重新调度）到节点上时，它的 `volumeMounts` 会挂载与其 
PersistentVolumeClaims 相关联的 PersistentVolume。
请注意，当 Pod 或者 StatefulSet 被删除时，与 PersistentVolumeClaims 相关联的 
PersistentVolume 并不会被删除。要删除它必须通过手动方式来完成。

<!--
### Pod Name Label

When the StatefulSet {{< glossary_tooltip term_id="controller" >}} creates a Pod,
it adds a label, `statefulset.kubernetes.io/pod-name`, that is set to the name of
the Pod. This label allows you to attach a Service to a specific Pod in
the StatefulSet.
-->
### Pod 名称标签   {#pod-name-label}

当 StatefulSet {{< glossary_tooltip term_id="controller" >}} 创建 Pod 时，
它会添加一个标签 `statefulset.kubernetes.io/pod-name`，该标签值设置为 Pod 名称。
这个标签允许你给 StatefulSet 中的特定 Pod 绑定一个 Service。

<!--
## Deployment and Scaling Guarantees

* For a StatefulSet with N replicas, when Pods are being deployed, they are created sequentially, in order from {0..N-1}.
* When Pods are being deleted, they are terminated in reverse order, from {N-1..0}.
* Before a scaling operation is applied to a Pod, all of its predecessors must be Running and Ready.
* Before a Pod is terminated, all of its successors must be completely shutdown.
-->
## 部署和扩缩保证   {#deployment-and-scaling-guarantees}

* 对于包含 N 个 副本的 StatefulSet，当部署 Pod 时，它们是依次创建的，顺序为 `0..N-1`。
* 当删除 Pod 时，它们是逆序终止的，顺序为 `N-1..0`。
* 在将缩放操作应用到 Pod 之前，它前面的所有 Pod 必须是 Running 和 Ready 状态。
* 在 Pod 终止之前，所有的继任者必须完全关闭。

<!--
The StatefulSet should not specify a `pod.Spec.TerminationGracePeriodSeconds` of 0. This practice is unsafe and strongly discouraged. For further explanation, please refer to [force deleting StatefulSet Pods](/docs/tasks/run-application/force-delete-stateful-set-pod/).
-->
StatefulSet 不应将 `pod.Spec.TerminationGracePeriodSeconds` 设置为 0。
这种做法是不安全的，要强烈阻止。更多的解释请参考
[强制删除 StatefulSet Pod](/zh/docs/tasks/run-application/force-delete-stateful-set-pod/)。

<!--
When the nginx example above is created, three Pods will be deployed in the order
web-0, web-1, web-2. web-1 will not be deployed before web-0 is
[Running and Ready](/docs/user-guide/pod-states/), and web-2 will not be deployed until
web-1 is Running and Ready. If web-0 should fail, after web-1 is Running and Ready, but before
web-2 is launched, web-2 will not be launched until web-0 is successfully relaunched and
becomes Running and Ready.
-->
在上面的 nginx 示例被创建后，会按照 web-0、web-1、web-2 的顺序部署三个 Pod。
在 web-0 进入 [Running 和 Ready](/zh/docs/concepts/workloads/pods/pod-lifecycle/)
状态前不会部署 web-1。在 web-1 进入 Running 和 Ready 状态前不会部署 web-2。
如果 web-1 已经处于 Running 和 Ready 状态，而 web-2 尚未部署，在此期间发生了
web-0 运行失败，那么 web-2 将不会被部署，要等到 web-0 部署完成并进入 Running 和
Ready 状态后，才会部署 web-2。

<!--
If a user were to scale the deployed example by patching the StatefulSet such that
`replicas=1`, web-2 would be terminated first. web-1 would not be terminated until web-2
is fully shutdown and deleted. If web-0 were to fail after web-2 has been terminated and
is completely shutdown, but prior to web-1's termination, web-1 would not be terminated
until web-0 is Running and Ready.
-->
如果用户想将示例中的 StatefulSet 收缩为 `replicas=1`，首先被终止的是 web-2。
在 web-2 没有被完全停止和删除前，web-1 不会被终止。
当 web-2 已被终止和删除、web-1 尚未被终止，如果在此期间发生 web-0 运行失败，
那么就不会终止 web-1，必须等到 web-0 进入 Running 和 Ready 状态后才会终止 web-1。

<!--
### Pod Management Policies

In Kubernetes 1.7 and later, StatefulSet allows you to relax its ordering guarantees while
preserving its uniqueness and identity guarantees via its `.spec.podManagementPolicy` field.
-->
### Pod 管理策略 {#pod-management-policies}

在 Kubernetes 1.7 及以后的版本中，StatefulSet 允许你放宽其排序保证，
同时通过它的 `.spec.podManagementPolicy` 域保持其唯一性和身份保证。

<!--
#### OrderedReady Pod Management

`OrderedReady` pod management is the default for StatefulSets. It implements the behavior
described [above](#deployment-and-scaling-guarantees).
-->
#### OrderedReady Pod 管理

`OrderedReady` Pod 管理是 StatefulSet 的默认设置。它实现了
[上面](#deployment-and-scaling-guarantees)描述的功能。

<!--
#### Parallel Pod Management

`Parallel` pod management tells the StatefulSet controller to launch or
terminate all Pods in parallel, and to not wait for Pods to become Running
and Ready or completely terminated prior to launching or terminating another
Pod. This option only affects the behavior for scaling operations. Updates are not affected.

-->
#### 并行 Pod 管理   {#parallel-pod-management}

`Parallel` Pod 管理让 StatefulSet 控制器并行的启动或终止所有的 Pod，
启动或者终止其他 Pod 前，无需等待 Pod 进入 Running 和 ready 或者完全停止状态。
这个选项只会影响伸缩操作的行为，更新则不会被影响。

<!--
## Update Strategies

In Kubernetes 1.7 and later, StatefulSet's `.spec.updateStrategy` field allows you to configure
and disable automated rolling updates for containers, labels, resource request/limits, and
annotations for the Pods in a StatefulSet.
-->
## 更新策略  {#update-strategies}

在 Kubernetes 1.7 及以后的版本中，StatefulSet 的 `.spec.updateStrategy` 字段让
你可以配置和禁用掉自动滚动更新 Pod 的容器、标签、资源请求或限制、以及注解。

<!--
### On Delete

The `OnDelete` update strategy implements the legacy (1.6 and prior) behavior. When a StatefulSet's
`.spec.updateStrategy.type` is set to `OnDelete`, the StatefulSet controller will not automatically
update the Pods in a StatefulSet. Users must manually delete Pods to cause the controller to
create new Pods that reflect modifications made to a StatefulSet's `.spec.template`.
-->
### 关于删除策略  {#on-delete}

`OnDelete` 更新策略实现了 1.6 及以前版本的历史遗留行为。当 StatefulSet 的
`.spec.updateStrategy.type` 设置为 `OnDelete` 时，它的控制器将不会自动更新
StatefulSet 中的 Pod。
用户必须手动删除 Pod 以便让控制器创建新的 Pod，以此来对 StatefulSet 的
`.spec.template` 的变动作出反应。

<!--
### Rolling Updates

The `RollingUpdate` update strategy implements automated, rolling update for the Pods in a
StatefulSet. It is the default strategy when `.spec.updateStrategy` is left unspecified. When a StatefulSet's `.spec.updateStrategy.type` is set to `RollingUpdate`, the
StatefulSet controller will delete and recreate each Pod in the StatefulSet. It will proceed
in the same order as Pod termination (from the largest ordinal to the smallest), updating
each Pod one at a time. It will wait until an updated Pod is Running and Ready prior to
updating its predecessor.
-->
### 滚动更新 {#rolling-updates}

`RollingUpdate` 更新策略对 StatefulSet 中的 Pod 执行自动的滚动更新。
在没有声明 `.spec.updateStrategy` 时，`RollingUpdate` 是默认配置。
当 StatefulSet 的 `.spec.updateStrategy.type` 被设置为 `RollingUpdate` 时，
StatefulSet 控制器会删除和重建 StatefulSet 中的每个 Pod。
它将按照与 Pod 终止相同的顺序（从最大序号到最小序号）进行，每次更新一个 Pod。
它会等到被更新的 Pod 进入 Running 和 Ready 状态，然后再更新其前身。

<!--
#### Partitions

The `RollingUpdate` update strategy can be partitioned, by specifying a
`.spec.updateStrategy.rollingUpdate.partition`. If a partition is specified, all Pods with an
ordinal that is greater than or equal to the partition will be updated when the StatefulSet's
`.spec.template` is updated. All Pods with an ordinal that is less than the partition will not
be updated, and, even if they are deleted, they will be recreated at the previous version. If a
StatefulSet's `.spec.updateStrategy.rollingUpdate.partition` is greater than its `.spec.replicas`,
updates to its `.spec.template` will not be propagated to its Pods.
In most cases you will not need to use a partition, but they are useful if you want to stage an
update, roll out a canary, or perform a phased roll out.
-->
#### 分区   {#partitions}

通过声明 `.spec.updateStrategy.rollingUpdate.partition` 的方式，`RollingUpdate`
更新策略可以实现分区。
如果声明了一个分区，当 StatefulSet 的 `.spec.template` 被更新时，
所有序号大于等于该分区序号的 Pod 都会被更新。
所有序号小于该分区序号的 Pod 都不会被更新，并且，即使他们被删除也会依据之前的版本进行重建。
如果 StatefulSet 的 `.spec.updateStrategy.rollingUpdate.partition` 大于它的
`.spec.replicas`，对它的 `.spec.template` 的更新将不会传递到它的 Pod。
在大多数情况下，你不需要使用分区，但如果你希望进行阶段更新、执行金丝雀或执行
分阶段上线，则这些分区会非常有用。

<!--
#### Forced Rollback

When using [Rolling Updates](#rolling-updates) with the default
[Pod Management Policy](#pod-management-policies) (`OrderedReady`),
it's possible to get into a broken state that requires manual intervention to repair.

If you update the Pod template to a configuration that never becomes Running and
Ready (for example, due to a bad binary or application-level configuration error),
StatefulSet will stop the rollout and wait.
-->
#### 强制回滚 {#forced-rollback}

在默认 [Pod 管理策略](#pod-management-policies)(`OrderedReady`) 下使用
[滚动更新](#rolling-updates) ，可能进入需要人工干预才能修复的损坏状态。

如果更新后 Pod 模板配置进入无法运行或就绪的状态（例如，由于错误的二进制文件
或应用程序级配置错误），StatefulSet 将停止回滚并等待。

<!--
In this state, it's not enough to revert the Pod template to a good configuration.
Due to a [known issue](https://github.com/kubernetes/kubernetes/issues/67250),
StatefulSet will continue to wait for the broken Pod to become Ready
(which never happens) before it will attempt to revert it back to the working
configuration.

After reverting the template, you must also delete any Pods that StatefulSet had
already attempted to run with the bad configuration.
StatefulSet will then begin to recreate the Pods using the reverted template.
-->
在这种状态下，仅将 Pod 模板还原为正确的配置是不够的。由于
[已知问题](https://github.com/kubernetes/kubernetes/issues/67250)，StatefulSet
将继续等待损坏状态的 Pod 准备就绪（永远不会发生），然后再尝试将其恢复为正常工作配置。

恢复模板后，还必须删除 StatefulSet 尝试使用错误的配置来运行的 Pod。这样，
StatefulSet 才会开始使用被还原的模板来重新创建 Pod。

## {{% heading "whatsnext" %}}

<!--
* Follow an example of [deploying a stateful application](/docs/tutorials/stateful-application/basic-stateful-set/).
* Follow an example of [deploying Cassandra with Stateful Sets](/docs/tutorials/stateful-application/cassandra/).
* Follow an example of [running a replicated stateful application](/docs/tasks/run-application/run-replicated-stateful-application/).
-->
* 示例一：[部署有状态应用](/zh/docs/tutorials/stateful-application/basic-stateful-set/)。
* 示例二：[使用 StatefulSet 部署 Cassandra](/zh/docs/tutorials/stateful-application/cassandra/)。
* 示例三：[运行多副本的有状态应用程序](/zh/docs/tasks/run-application/run-replicated-stateful-application/)。
