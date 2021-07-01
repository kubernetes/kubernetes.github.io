---
title: Pod 安全策略
content_type: concept
weight: 30
---
<!--
reviewers:
- pweil-
- tallclair
title: Pod Security Policies
content_type: concept
weight: 30
-->

{{< feature-state for_k8s_version="v1.21" state="deprecated" >}}

<!--
PodSecurityPolicy is deprecated as of Kubernetes v1.21, and will be removed in v1.25.
-->
PodSecurityPolicy 在 Kubernetes v1.21 版本中被弃用，将在 v1.25 中删除。

<!--
Pod Security Policies enable fine-grained authorization of pod creation and
updates.
-->
Pod 安全策略使得对 Pod 创建和更新进行细粒度的权限控制成为可能。

<!--
## What is a Pod Security Policy?

A _Pod Security Policy_ is a cluster-level resource that controls security
sensitive aspects of the pod specification. The [PodSecurityPolicy](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#podsecuritypolicy-v1beta1-policy) objects
define a set of conditions that a pod must run with in order to be accepted into
the system, as well as defaults for the related fields. They allow an
administrator to control the following:
-->
## 什么是 Pod 安全策略？

_Pod 安全策略（Pod Security Policy）_ 是集群级别的资源，它能够控制 Pod 规约
中与安全性相关的各个方面。
[PodSecurityPolicy](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#podsecuritypolicy-v1beta1-policy)
对象定义了一组 Pod 运行时必须遵循的条件及相关字段的默认值，只有 Pod 满足这些条件
才会被系统接受。
Pod 安全策略允许管理员控制如下方面：

<!--
| Control Aspect                                      | Field Names                                 |
| ----------------------------------------------------| ----------------------------------------- |
| Running of privileged containers                    | [`privileged`](#privileged)                                |
| Usage of host namespaces                            | [`hostPID`, `hostIPC`](#host-namespaces)    |
| Usage of host networking and ports                  | [`hostNetwork`, `hostPorts`](#host-namespaces) |
| Usage of volume types                               | [`volumes`](#volumes-and-file-systems)      |
| Usage of the host filesystem                        | [`allowedHostPaths`](#volumes-and-file-systems) |
| Allow specific FlexVolume drivers                   | [`allowedFlexVolumes`](#flexvolume-drivers) |
| Allocating an FSGroup that owns the pod's volumes   | [`fsGroup`](#volumes-and-file-systems)      |
| Requiring the use of a read only root file system   | [`readOnlyRootFilesystem`](#volumes-and-file-systems) |
| The user and group IDs of the container             | [`runAsUser`, `runAsGroup`, `supplementalGroups`](#users-and-groups) |
| Restricting escalation to root privileges           | [`allowPrivilegeEscalation`, `defaultAllowPrivilegeEscalation`](#privilege-escalation) |
| Linux capabilities                                  | [`defaultAddCapabilities`, `requiredDropCapabilities`, `allowedCapabilities`](#capabilities) |
| The SELinux context of the container                | [`seLinux`](#selinux)                       |
| The Allowed Proc Mount types for the container      | [`allowedProcMountTypes`](#allowedprocmounttypes) |
| The AppArmor profile used by containers             | [annotations](#apparmor)                    |
| The seccomp profile used by containers              | [annotations](#seccomp)                     |
| The sysctl profile used by containers               | [`forbiddenSysctls`,`allowedUnsafeSysctls`](#sysctl)                      |
-->
| 控制的角度                          | 字段名称                          |
| ----------------------------------- | --------------------------------- |
| 运行特权容器                        | [`privileged`](#privileged) |
| 使用宿主名字空间                    | [`hostPID`、`hostIPC`](#host-namespaces) |
| 使用宿主的网络和端口                | [`hostNetwork`, `hostPorts`](#host-namespaces) |
| 控制卷类型的使用                    | [`volumes`](#volumes-and-file-systems) |
| 使用宿主文件系统                    | [`allowedHostPaths`](#volumes-and-file-systems) |
| 允许使用特定的 FlexVolume 驱动      | [`allowedFlexVolumes`](#flexvolume-drivers) |
| 分配拥有 Pod 卷的 FSGroup 账号      | [`fsGroup`](#volumes-and-file-systems)      |
| 以只读方式访问根文件系统            | [`readOnlyRootFilesystem`](#volumes-and-file-systems) |
| 设置容器的用户和组 ID               | [`runAsUser`, `runAsGroup`, `supplementalGroups`](#users-and-groups) |
| 限制 root 账号特权级提升             | [`allowPrivilegeEscalation`, `defaultAllowPrivilegeEscalation`](#privilege-escalation) |
| Linux 权能字（Capabilities）        | [`defaultAddCapabilities`, `requiredDropCapabilities`, `allowedCapabilities`](#capabilities) |
| 设置容器的 SELinux 上下文           | [`seLinux`](#selinux)                       |
| 指定容器可以挂载的 proc 类型        | [`allowedProcMountTypes`](#allowedprocmounttypes) |
| 指定容器使用的 AppArmor 模版        | [annotations](#apparmor)                    |
| 指定容器使用的 seccomp 模版         | [annotations](#seccomp)                     |
| 指定容器使用的 sysctl 模版          | [`forbiddenSysctls`,`allowedUnsafeSysctls`](#sysctl)  | 


_Pod 安全策略_ 由设置和策略组成，它们能够控制 Pod 访问的安全特征。这些设置分为如下三类：

- *基于布尔值控制* ：这种类型的字段默认为最严格限制的值。
- *基于被允许的值集合控制* ：这种类型的字段会与这组值进行对比，以确认值被允许。
- *基于策略控制* ：设置项通过一种策略提供的机制来生成该值，这种机制能够确保指定的值落在被允许的这组值中。

<!--
## Enabling Pod Security Policies

Pod security policy control is implemented as an optional (but recommended)
[admission
controller](/docs/reference/access-authn-authz/admission-controllers/#podsecuritypolicy). PodSecurityPolicies
are enforced by [enabling the admission
controller](/docs/reference/access-authn-authz/admission-controllers/#how-do-i-turn-on-an-admission-control-plug-in),
but doing so without authorizing any policies **will prevent any pods from being
created** in the cluster.
-->
## 启用 Pod 安全策略

Pod 安全策略实现为一种可选（但是建议启用）的
[准入控制器](/zh/docs/reference/access-authn-authz/admission-controllers/#podsecuritypolicy)。
[启用了准入控制器](/zh/docs/reference/access-authn-authz/admission-controllers/#how-do-i-turn-on-an-admission-control-plug-in)
即可强制实施 Pod 安全策略，不过如果没有授权认可策略之前即启用
准入控制器 **将导致集群中无法创建任何 Pod**。

<!--
Since the pod security policy API (`policy/v1beta1/podsecuritypolicy`) is
enabled independently of the admission controller, for existing clusters it is
recommended that policies are added and authorized before enabling the admission
controller.
-->
由于 Pod 安全策略 API（`policy/v1beta1/podsecuritypolicy`）是独立于准入控制器
来启用的，对于现有集群而言，建议在启用准入控制器之前先添加策略并对其授权。

<!--
## Authorizing Policies

When a PodSecurityPolicy resource is created, it does nothing. In order to use
it, the requesting user or target pod's [service
account](/docs/tasks/configure-pod-container/configure-service-account/) must be
authorized to use the policy, by allowing the `use` verb on the policy.
-->
## 授权策略    {#authorizing-policies}

PodSecurityPolicy 资源被创建时，并不执行任何操作。为了使用该资源，需要对
发出请求的用户或者目标 Pod 的
[服务账号](/zh/docs/tasks/configure-pod-container/configure-service-account/)
授权，通过允许其对策略执行 `use` 动词允许其使用该策略。

<!--
Most Kubernetes pods are not created directly by users. Instead, they are
typically created indirectly as part of a
[Deployment](/docs/concepts/workloads/controllers/deployment/),
[ReplicaSet](/docs/concepts/workloads/controllers/replicaset/), or other
templated controller via the controller manager. Granting the controller access
to the policy would grant access for *all* pods created by that controller,
so the preferred method for authorizing policies is to grant access to the
pod's service account (see [example](#run-another-pod)).
-->
大多数 Kubernetes Pod 不是由用户直接创建的。相反，这些 Pod 是由
[Deployment](/zh/docs/concepts/workloads/controllers/deployment/)、
[ReplicaSet](/zh/docs/concepts/workloads/controllers/replicaset/)
或者经由控制器管理器模版化的控制器创建。
赋予控制器访问策略的权限意味着对应控制器所创建的 *所有* Pod 都可访问策略。
因此，对策略进行授权的优先方案是为 Pod 的服务账号授予访问权限
（参见[示例](#run-another-pod)）。

<!--
### Via RBAC

[RBAC](/docs/reference/access-authn-authz/rbac/) is a standard Kubernetes
authorization mode, and can easily be used to authorize use of policies.

First, a `Role` or `ClusterRole` needs to grant access to `use` the desired
policies. The rules to grant access look like this:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: <role name>
rules:
- apiGroups: ['policy']
  resources: ['podsecuritypolicies']
  verbs:     ['use']
  resourceNames:
  - <list of policies to authorize>
```
-->
### 通过 RBAC 授权   {#via-rbac}

[RBAC](/zh/docs/reference/access-authn-authz/rbac/) 是一种标准的 Kubernetes
鉴权模式，可以很容易地用来授权策略访问。

首先，某 `Role` 或 `ClusterRole` 需要获得使用 `use` 访问目标策略的权限。
访问授权的规则看起来像这样：

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: <Role 名称>
rules:
- apiGroups: ['policy']
  resources: ['podsecuritypolicies']
  verbs:     ['use']
  resourceNames:
  - <要授权的策略列表>
```

<!--
Then the `(Cluster)Role` is bound to the authorized user(s):

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: <binding name>
roleRef:
  kind: ClusterRole
  name: <role name>
  apiGroup: rbac.authorization.k8s.io
subjects:
# Authorize specific service accounts:
- kind: ServiceAccount
  name: <authorized service account name>
  namespace: <authorized pod namespace>
# Authorize specific users (not recommended):
- kind: User
  apiGroup: rbac.authorization.k8s.io
  name: <authorized user name>
```
-->
接下来将该 `Role`（或 `ClusterRole`）绑定到授权的用户：

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: <绑定名称>
roleRef:
  kind: ClusterRole
  name: <角色名称>
  apiGroup: rbac.authorization.k8s.io
subjects:
# 授权特定的服务账号
- kind: ServiceAccount
  name: <要授权的服务账号名称>
  namespace: <authorized pod namespace>
# 授权特定的用户（不建议这样操作）
- kind: User
  apiGroup: rbac.authorization.k8s.io
  name: <要授权的用户名>
```

<!--
If a `RoleBinding` (not a `ClusterRoleBinding`) is used, it will only grant
usage for pods being run in the same namespace as the binding. This can be
paired with system groups to grant access to all pods run in the namespace:
```yaml
# Authorize all service accounts in a namespace:
- kind: Group
  apiGroup: rbac.authorization.k8s.io
  name: system:serviceaccounts
# Or equivalently, all authenticated users in a namespace:
- kind: Group
  apiGroup: rbac.authorization.k8s.io
  name: system:authenticated
```
-->
如果使用的是 `RoleBinding`（而不是 `ClusterRoleBinding`），授权仅限于
与该 `RoleBinding` 处于同一名字空间中的 Pods。
可以考虑将这种授权模式和系统组结合，对名字空间中的所有 Pod 授予访问权限。

```yaml
# 授权某名字空间中所有服务账号
- kind: Group
  apiGroup: rbac.authorization.k8s.io
  name: system:serviceaccounts
# 或者与之等价，授权给某名字空间中所有被认证过的用户
- kind: Group
  apiGroup: rbac.authorization.k8s.io
  name: system:authenticated
```

<!--
For more examples of RBAC bindings, see [Role Binding
Examples](/docs/reference/access-authn-authz/rbac#role-binding-examples).
For a complete example of authorizing a PodSecurityPolicy, see
[below](#example).
-->
参阅[角色绑定示例](/zh/docs/reference/access-authn-authz/rbac#role-binding-examples)
查看 RBAC 绑定的更多实例。
参阅[下文](#example)，查看对 PodSecurityPolicy 进行授权的完整示例。

<!--
### Troubleshooting

- The [Controller Manager](/docs/reference/command-line-tools-reference/kube-controller-manager/) must be run
against [the secured API port](/docs/reference/access-authn-authz/controlling-access/),
and must not have superuser permissions. Otherwise requests would bypass
authentication and authorization modules, all PodSecurityPolicy objects would be
allowed, and users would be able to create privileged containers. For more details
on configuring Controller Manager authorization, see
[Controller Roles](/docs/reference/access-authn-authz/rbac/#controller-roles).
-->
### 故障排查   {#troubleshooting}

- [控制器管理器组件](/zh/docs/reference/command-line-tools-reference/kube-controller-manager/)
  必须运行在
  [安全的 API 端口](/zh/docs/concepts/security/controlling-access/)，
  并且一定不能具有超级用户权限。
  否则其请求会绕过身份认证和鉴权模块控制，从而导致所有 PodSecurityPolicy 对象
  都被启用，用户亦能创建特权容器。
  关于配置控制器管理器鉴权相关的详细信息，可参阅
  [控制器角色](/zh/docs/reference/access-authn-authz/rbac/#controller-roles)。

<!--
## Policy Order

In addition to restricting pod creation and update, pod security policies can
also be used to provide default values for many of the fields that it
controls. When multiple policies are available, the pod security policy
controller selects policies according to the following criteria:
-->
## 策略顺序  {#policy-order}

除了限制 Pod 创建与更新，Pod 安全策略也可用来为其所控制的很多字段
设置默认值。当存在多个策略对象时，Pod 安全策略控制器依据以下条件选择
策略：

<!--
1. PodSecurityPolicies which allow the pod as-is, without changing defaults or
   mutating the pod, are preferred.  The order of these non-mutating
   PodSecurityPolicies doesn't matter.
2. If the pod must be defaulted or mutated, the first PodSecurityPolicy
   (ordered by name) to allow the pod is selected.
-->
1. 优先考虑允许 Pod 保持原样，不会更改 Pod 字段默认值或其他配置的 PodSecurityPolicy。
   这类非更改性质的 PodSecurityPolicy 对象之间的顺序无关紧要。
2. 如果必须要为 Pod 设置默认值或者其他配置，（按名称顺序）选择第一个允许
   Pod 操作的 PodSecurityPolicy 对象。

<!--
During update operations (during which mutations to pod specs are disallowed)
only non-mutating PodSecurityPolicies are used to validate the pod.
-->
{{< note >}}
在更新操作期间（这时不允许更改 Pod 规约），仅使用非更改性质的
PodSecurityPolicy 来对 Pod 执行验证操作。
{{< /note >}}

<!--
## Example

_This example assumes you have a running cluster with the PodSecurityPolicy
admission controller enabled and you have cluster admin privileges._
-->
## 示例   {#example}

_本示例假定你已经有一个启动了 PodSecurityPolicy 准入控制器的集群并且
你拥有集群管理员特权。_

<!--
### Set up

Set up a namespace and a service account to act as for this example. We'll use
this service account to mock a non-admin user.
-->
### 配置   {#set-up}

为运行此示例，配置一个名字空间和一个服务账号。我们将用这个服务账号来
模拟一个非管理员账号的用户。

```shell
kubectl create namespace psp-example
kubectl create serviceaccount -n psp-example fake-user
kubectl create rolebinding -n psp-example fake-editor --clusterrole=edit --serviceaccount=psp-example:fake-user
```

<!--
To make it clear which user we're acting as and save some typing, create 2
aliases:
-->
创建两个别名，以更清晰地展示我们所使用的用户账号，同时减少一些键盘输入：

```shell
alias kubectl-admin='kubectl -n psp-example'
alias kubectl-user='kubectl --as=system:serviceaccount:psp-example:fake-user -n psp-example'
```

<!--
### Create a policy and a pod

Define the example PodSecurityPolicy object in a file. This is a policy that
simply prevents the creation of privileged pods.
The name of a PodSecurityPolicy object must be a valid
[DNS subdomain name](/docs/concepts/overview/working-with-objects/names#dns-subdomain-names).
-->
### 创建一个策略和一个 Pod

在一个文件中定义一个示例的 PodSecurityPolicy 对象。
这里的策略只是用来禁止创建有特权要求的 Pods。
PodSecurityPolicy 对象的名称必须是合法的
[DNS 子域名](/zh/docs/concepts/overview/working-with-objects/names#dns-subdomain-names)。

{{< codenew file="policy/example-psp.yaml" >}}

<!-- And create it with kubectl: -->
使用 kubectl 执行创建操作：

```shell
kubectl-admin create -f example-psp.yaml
```

<!--
Now, as the unprivileged user, try to create a simple pod:
-->
现在，作为一个非特权用户，尝试创建一个简单的 Pod：

```shell
kubectl-user create -f- <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: pause
spec:
  containers:
    - name: pause
      image: k8s.gcr.io/pause
EOF
```

<!--
The output is similar to this:
-->
输出类似于：
```
Error from server (Forbidden): error when creating "STDIN": pods "pause" is forbidden: unable to validate against any pod security policy: []
```

<!--
**What happened?** Although the PodSecurityPolicy was created, neither the
pod's service account nor `fake-user` have permission to use the new policy:
-->
**发生了什么？** 尽管 PodSecurityPolicy 被创建，Pod 的服务账号或者
`fake-user` 用户都没有使用该策略的权限。

```shell
kubectl-user auth can-i use podsecuritypolicy/example
```

```
no
```
<!--
Create the rolebinding to grant `fake-user` the `use` verb on the example
policy:
-->
创建角色绑定，赋予 `fake-user` 使用 `use` 访问示例策略的权限：

<!--
This is not the recommended way! See the [next section](#run-another-pod)
for the preferred approach.
-->
{{< note >}}
不建议使用这种方法！
欲了解优先考虑的方法，请参见[下节](#run-another-pod)。
{{< /note >}}

```shell
kubectl-admin create role psp:unprivileged \
    --verb=use \
    --resource=podsecuritypolicy \
    --resource-name=example
```

输出：

```
role "psp:unprivileged" created
```

```shell
kubectl-admin create rolebinding fake-user:psp:unprivileged \
    --role=psp:unprivileged \
    --serviceaccount=psp-example:fake-user
```

输出：

```
rolebinding "fake-user:psp:unprivileged" created
```

```shell
kubectl-user auth can-i use podsecuritypolicy/example
```

输出：

```
yes
```

<!--
Now retry creating the pod:
-->
现在重试创建 Pod：

```shell
kubectl-user create -f- <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: pause
spec:
  containers:
    - name: pause
      image: k8s.gcr.io/pause
EOF
```
<!--
The output is similar to this:
-->
输出类似于：
```
pod "pause" created
```

<!--
It works as expected! But any attempts to create a privileged pod should still
be denied:
-->
此次尝试不出所料地成功了！
不过任何创建特权 Pod 的尝试还是会被拒绝：

```shell
kubectl-user create -f- <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: privileged
spec:
  containers:
    - name: pause
      image: k8s.gcr.io/pause
      securityContext:
        privileged: true
EOF
```

<!--
The output is similar to this:
-->

输出类似于：
```
Error from server (Forbidden): error when creating "STDIN": pods "privileged" is forbidden: unable to validate against any pod security policy: [spec.containers[0].securityContext.privileged: Invalid value: true: Privileged containers are not allowed]
```

<!--
Delete the pod before moving on:
-->
继续此例之前先删除该 Pod：

```shell
kubectl-user delete pod pause
```

<!--
### Run another pod

Let's try that again, slightly differently:
-->
### 运行另一个 Pod  {#run-another-pod}

我们再试一次，稍微有些不同：

```shell
kubectl-user create deployment pause --image=k8s.gcr.io/pause
```

输出为：

```
deployment "pause" created
```

```shell
kubectl-user get pods
```

输出为：

```
No resources found.
```

```shell
kubectl-user get events | head -n 2
```

输出为：
```
LASTSEEN   FIRSTSEEN   COUNT     NAME              KIND         SUBOBJECT                TYPE      REASON                  SOURCE                                  MESSAGE
1m         2m          15        pause-7774d79b5   ReplicaSet                            Warning   FailedCreate            replicaset-controller                   Error creating: pods "pause-7774d79b5-" is forbidden: no providers available to validate pod request
```

<!--
**What happened?** We already bound the `psp:unprivileged` role for our `fake-user`,
why are we getting the error `Error creating: pods "pause-7774d79b5-" is
forbidden: no providers available to validate pod request`? The answer lies in
the source - `replicaset-controller`. Fake-user successfully created the
deployment (which successfully created a replicaset), but when the replicaset
went to create the pod it was not authorized to use the example
podsecuritypolicy.
-->
**发生了什么？** 我们已经为用户 `fake-user` 绑定了 `psp:unprivileged` 角色，
为什么还会收到错误 `Error creating: pods "pause-7774d79b5-" is
forbidden: no providers available to validate pod request
（创建错误：pods "pause-7774d79b5" 被禁止：没有可用来验证 pod 请求的驱动）`？ 
答案在于源文件 - `replicaset-controller`。
`fake-user` 用户成功地创建了 Deployment，而后者也成功地创建了 ReplicaSet，
不过当 ReplicaSet 创建 Pod 时，发现未被授权使用示例 PodSecurityPolicy 资源。

<!--
In order to fix this, bind the `psp:unprivileged` role to the pod's service
account instead. In this case (since we didn't specify it) the service account
is `default`:
-->
为了修复这一问题，将 `psp:unprivileged` 角色绑定到 Pod 的服务账号。
在这里，因为我们没有给出服务账号名称，默认的服务账号是 `default`。

```shell
kubectl-admin create rolebinding default:psp:unprivileged \
    --role=psp:unprivileged \
    --serviceaccount=psp-example:default
```

输出为：

```
rolebinding "default:psp:unprivileged" created
```

<!--
Now if you give it a minute to retry, the replicaset-controller should
eventually succeed in creating the pod:
-->
现在如果你给 ReplicaSet 控制器一分钟的时间来重试，该控制器最终将能够
成功地创建 Pod：

```shell
kubectl-user get pods --watch
```

输出类似于：

```
NAME                    READY     STATUS    RESTARTS   AGE
pause-7774d79b5-qrgcb   0/1       Pending   0         1s
pause-7774d79b5-qrgcb   0/1       Pending   0         1s
pause-7774d79b5-qrgcb   0/1       ContainerCreating   0         1s
pause-7774d79b5-qrgcb   1/1       Running   0         2s
```

<!--
### Clean up

Delete the namespace to clean up most of the example resources:
-->
### 清理  {#clean-up}

删除名字空间即可清理大部分示例资源：

```shell
kubectl-admin delete ns psp-example
```

输出类似于：

```
namespace "psp-example" deleted
```

<!--
Note that `PodSecurityPolicy` resources are not namespaced, and must be cleaned
up separately:
-->
注意 `PodSecurityPolicy` 资源不是名字空间域的资源，必须单独清理：

```shell
kubectl-admin delete psp example
```

输出类似于：
```
podsecuritypolicy "example" deleted
```

<!--
### Example Policies

This is the least restrictive policy you can create, equivalent to not using the
pod security policy admission controller:
-->
### 示例策略  {#example-policies}

下面是一个你可以创建的约束性非常弱的策略，其效果等价于没有使用 Pod 安全
策略准入控制器：

{{< codenew file="policy/privileged-psp.yaml" >}}

<!--
This is an example of a restrictive policy that requires users to run as an
unprivileged user, blocks possible escalations to root, and requires use of
several security mechanisms.
-->
下面是一个具有约束性的策略，要求用户以非特权账号运行，禁止可能的向 root 权限
的升级，同时要求使用若干安全机制。

{{< codenew file="policy/restricted-psp.yaml" >}}

<!--
See [Pod Security Standards](/docs/concepts/security/pod-security-standards/#policy-instantiation) for more examples.
-->
更多的示例可参考
[Pod 安全标准](/zh/docs/concepts/security/pod-security-standards/#policy-instantiation)。

<!--
## Policy Reference

### Privileged

**Privileged** - determines if any container in a pod can enable privileged mode.
By default a container is not allowed to access any devices on the host, but a
"privileged" container is given access to all devices on the host. This allows
the container nearly all the same access as processes running on the host.
This is useful for containers that want to use linux capabilities like
manipulating the network stack and accessing devices.
-->
## 策略参考    {#policy-reference}

### Privileged

**Privileged** - 决定是否 Pod 中的某容器可以启用特权模式。
默认情况下，容器是不可以访问宿主上的任何设备的，不过一个“privileged（特权的）”
容器则被授权访问宿主上所有设备。
这种容器几乎享有宿主上运行的进程的所有访问权限。
对于需要使用 Linux 权能字（如操控网络堆栈和访问设备）的容器而言是有用的。

<!--
### Host namespaces

**HostPID** - Controls whether the pod containers can share the host process ID
namespace. Note that when paired with ptrace this can be used to escalate
privileges outside of the container (ptrace is forbidden by default).

**HostIPC** - Controls whether the pod containers can share the host IPC
namespace.

**HostNetwork** - Controls whether the pod may use the node network
namespace. Doing so gives the pod access to the loopback device, services
listening on localhost, and could be used to snoop on network activity of other
pods on the same node.

**HostPorts** - Provides a list of ranges of allowable ports in the host
network namespace. Defined as a list of `HostPortRange`, with `min`(inclusive)
and `max`(inclusive). Defaults to no allowed host ports.
-->
### 宿主名字空间   {#host-namespaces}

**HostPID** - 控制 Pod 中容器是否可以共享宿主上的进程 ID 空间。
注意，如果与 `ptrace` 相结合，这种授权可能被利用，导致向容器外的特权逃逸
（默认情况下 `ptrace` 是被禁止的）。

**HostIPC** - 控制 Pod 容器是否可共享宿主上的 IPC 名字空间。

**HostNetwork** - 控制是否 Pod 可以使用节点的网络名字空间。
此类授权将允许 Pod 访问本地回路（loopback）设备、在本地主机（localhost）
上监听的服务、还可能用来监听同一节点上其他 Pod 的网络活动。

**HostPorts** -提供可以在宿主网络名字空间中可使用的端口范围列表。 
该属性定义为一组 `HostPortRange` 对象的列表，每个对象中包含
`min`（含）与 `max`（含）值的设置。
默认不允许访问宿主端口。

<!--
### Volumes and file systems

**Volumes** - Provides a list of allowed volume types. The allowable values
correspond to the volume sources that are defined when creating a volume. For
the complete list of volume types, see [Types of
Volumes](/docs/concepts/storage/volumes/#types-of-volumes). Additionally, `*`
may be used to allow all volume types.

The **recommended minimum set** of allowed volumes for new PSPs are:
-->
### 卷和文件系统   {#volumes-and-file-systems}

**Volumes** - 提供一组被允许的卷类型列表。可被允许的值对应于创建卷时可以
设置的卷来源。卷类型的完整列表可参见
[卷类型](/zh/docs/concepts/storage/volumes/#types-of-volumes)。
此外， `*` 可以用来允许所有卷类型。

对于新的 Pod 安全策略设置而言，建议设置的卷类型的*最小列表*包含：

- configMap
- downwardAPI
- emptyDir
- persistentVolumeClaim
- secret
- projected

<!--
PodSecurityPolicy does not limit the types of `PersistentVolume` objects that
may be referenced by a `PersistentVolumeClaim`, and hostPath type
`PersistentVolumes` do not support read-only access mode. Only trusted users
should be granted permission to create `PersistentVolume` objects.
-->
{{< warning >}}
PodSecurityPolicy 并不限制可以被 `PersistentVolumeClaim` 所引用的
`PersistentVolume` 对象的类型。
此外 `hostPath` 类型的 `PersistentVolume` 不支持只读访问模式。
应该仅赋予受信用户创建 `PersistentVolume` 对象的访问权限。
{{< /warning >}}

<!--
**FSGroup** - Controls the supplemental group applied to some volumes.

- *MustRunAs* - Requires at least one `range` to be specified. Uses the
minimum value of the first range as the default. Validates against all ranges.
- *MayRunAs* - Requires at least one `range` to be specified. Allows
`FSGroups` to be left unset without providing a default. Validates against
all ranges if `FSGroups` is set.
- *RunAsAny* - No default provided. Allows any `fsGroup` ID to be specified.
-->
**FSGroup** - 控制应用到某些卷上的附加用户组。

  - *MustRunAs* - 要求至少指定一个 `range`。
    使用范围中的最小值作为默认值。所有 range 值都会被用来执行验证。
  - *MayRunAs* - 要求至少指定一个 `range`。
    允许不设置 `FSGroups`，且无默认值。
    如果 `FSGroup` 被设置，则所有 range 值都会被用来执行验证检查。
  - *RunAsAny* - 不提供默认值。允许设置任意 `fsGroup` ID 值。

<!--
**AllowedHostPaths** - This specifies a list of host paths that are allowed
to be used by hostPath volumes. An empty list means there is no restriction on
host paths used. This is defined as a list of objects with a single `pathPrefix`
field, which allows hostPath volumes to mount a path that begins with an
allowed prefix, and a `readOnly` field indicating it must be mounted read-only.
For example:
-->
**AllowedHostPaths** - 设置一组宿主文件目录，这些目录项可以在 `hostPath` 卷中
使用。列表为空意味着对所使用的宿主目录没有限制。
此选项定义包含一个对象列表，表中对象包含 `pathPrefix` 字段，用来表示允许
`hostPath` 卷挂载以所指定前缀开头的路径。
对象中还包含一个 `readOnly` 字段，用来表示对应的卷必须以只读方式挂载。
例如：

<!--
```yaml
allowedHostPaths:
  # This allows "/foo", "/foo/", "/foo/bar" etc., but
  # disallows "/fool", "/etc/foo" etc.
  # "/foo/../" is never valid.
  - pathPrefix: "/foo"
    readOnly: true # only allow read-only mounts
```
-->
```yaml
allowedHostPaths:
  # 下面的设置允许 "/foo"、"/foo/"、"/foo/bar" 等路径，但禁止
  # "/fool"、"/etc/foo" 这些路径。
  # "/foo/../" 总会被当作非法路径。
  - pathPrefix: "/foo"
    readOnly: true # 仅允许只读模式挂载
```

<!--
There are many ways a container with unrestricted access to the host
filesystem can escalate privileges, including reading data from other
containers, and abusing the credentials of system services, such as Kubelet.

Writeable hostPath directory volumes allow containers to write
to the filesystem in ways that let them traverse the host filesystem outside the `pathPrefix`.
`readOnly: true`, available in Kubernetes 1.11+, must be used on **all** `allowedHostPaths`
to effectively limit access to the specified `pathPrefix`.
-->

{{< warning >}}
容器如果对宿主文件系统拥有不受限制的访问权限，就可以有很多种方式提升自己的特权，
包括读取其他容器中的数据、滥用系统服务（如 `kubelet`）的凭据信息等。

由可写入的目录所构造的 `hostPath` 卷能够允许容器写入数据到宿主文件系统，
并且在写入时避开 `pathPrefix` 所设置的目录限制。
`readOnly: true` 这一设置在 Kubernetes 1.11 版本之后可用。
必须针对 `allowedHostPaths` 中的 *所有* 条目设置此属性才能有效地限制容器
只能访问 `pathPrefix` 所指定的目录。
{{< /warning >}}

**ReadOnlyRootFilesystem** - 要求容器必须以只读方式挂载根文件系统来运行
（即不允许存在可写入层）。

<!--
### FlexVolume drivers

This specifies a list of FlexVolume drivers that are allowed to be used
by flexvolume. An empty list or nil means there is no restriction on the drivers.
Please make sure [`volumes`](#volumes-and-file-systems) field contains the
`flexVolume` volume type; no FlexVolume driver is allowed otherwise.

For example:
-->
### FlexVolume 驱动  {#flexvolume-drivers}

此配置指定一个可以被 FlexVolume 卷使用的驱动程序的列表。
空的列表或者 nil 值意味着对驱动没有任何限制。
请确保[`volumes`](#volumes-and-file-systems) 字段包含了 `flexVolume` 卷类型，
否则所有 FlexVolume 驱动都被禁止。

<!--
```yaml
apiVersion: policy/v1beta1
kind: PodSecurityPolicy
metadata:
  name: allow-flex-volumes
spec:
  # ... other spec fields
  volumes:
    - flexVolume
  allowedFlexVolumes:
    - driver: example/lvm
    - driver: example/cifs
```
-->

```yaml
apiVersion: policy/v1beta1
kind: PodSecurityPolicy
metadata:
  name: allow-flex-volumes
spec:
  # spec d的其他字段
  volumes:
    - flexVolume
  allowedFlexVolumes:
    - driver: example/lvm
    - driver: example/cifs
```

<!--
### Users and groups

**RunAsUser** - Controls which user ID the containers are run with.

- *MustRunAs* - Requires at least one `range` to be specified. Uses the
minimum value of the first range as the default. Validates against all ranges.
- *MustRunAsNonRoot* - Requires that the pod be submitted with a non-zero
`runAsUser` or have the `USER` directive defined (using a numeric UID) in the
image. Pods which have specified neither `runAsNonRoot` nor `runAsUser` settings
will be mutated to set `runAsNonRoot=true`, thus requiring a defined non-zero 
numeric `USER` directive in the container. No default provided. Setting 
`allowPrivilegeEscalation=false` is strongly recommended with this strategy.
- *RunAsAny* - No default provided. Allows any `runAsUser` to be specified.
-->
### 用户和组    {#users-and-groups}

**RunAsUser** - 控制使用哪个用户 ID 来运行容器。

  - *MustRunAs* - 必须配置一个 `range`。使用该范围内的第一个值作为默认值。
    所有 range 值都被用于验证检查。
- *MustRunAsNonRoot* - 要求提交的 Pod 具有非零 `runAsUser` 值，或在镜像中
  （使用 UID 数值）定义了 `USER` 环境变量。
  如果 Pod 既没有设置 `runAsNonRoot`，也没有设置 `runAsUser`，则该 Pod 会被
  修改以设置 `runAsNonRoot=true`，从而要求容器通过 `USER` 指令给出非零的数值形式
  的用户 ID。此配置没有默认值。采用此配置时，强烈建议设置
   `allowPrivilegeEscalation=false`。
- *RunAsAny* - 没有提供默认值。允许指定任何 `runAsUser` 配置。

<!--
**RunAsGroup** - Controls which primary group ID the containers are run with.

  - *MustRunAs* - Requires at least one `range` to be specified. Uses the 
    minimum value of the first range as the default.
    Validates against all ranges.
  - *MayRunAs* - Does not require that RunAsGroup be specified. However, when RunAsGroup
is specified, they have to fall in the defined range.
  - *RunAsAny* - No default provided. Allows any `runAsGroup` to be specified.
-->
**RunAsGroup** - 控制运行容器时使用的主用户组 ID。

  - *MustRunAs* - 要求至少指定一个 `range` 值。第一个 range
    中的最小值作为默认值。所有 range 值都被用来执行验证检查。
  - *MayRunAs* - 不要求设置 `RunAsGroup`。
    不过，如果指定了 `RunAsGroup` 被设置，所设置值必须处于所定义的范围内。
  - *RunAsAny* - 未指定默认值。允许 `runAsGroup` 设置任何值。

<!--
**SupplementalGroups** - Controls which group IDs containers add.

  - *MustRunAs* - Requires at least one `range` to be specified. Uses the
minimum value of the first range as the default. Validates against all ranges.
  - *MayRunAs* - Requires at least one `range` to be specified. Allows
`supplementalGroups` to be left unset without providing a default.
Validates against all ranges if `supplementalGroups` is set.
  - *RunAsAny* - No default provided. Allows any `supplementalGroups` to be
specified.
-->
**SupplementalGroups** - 控制容器可以添加的组 ID。

  - *MustRunAs* - 要求至少指定一个 `range` 值。
    第一个 range 中的最小值用作默认值。
    所有 range 值都被用来执行验证检查。
  - *MayRunAs* - 要求至少指定一个 `range` 值。
    允许不指定 `supplementalGroups` 且不设置默认值。
    如果 `supplementalGroups` 被设置，则所有 range 值都被用来执行验证检查。
  - *RunAsAny* - 未指定默认值。允许为 `supplementalGroups` 设置任何值。

<!--
### Privilege Escalation

These options control the `allowPrivilegeEscalation` container option. This bool
directly controls whether the
[`no_new_privs`](https://www.kernel.org/doc/Documentation/prctl/no_new_privs.txt)
flag gets set on the container process. This flag will prevent `setuid` binaries
from changing the effective user ID, and prevent files from enabling extra
capabilities (e.g. it will prevent the use of the `ping` tool). This behavior is
required to effectively enforce `MustRunAsNonRoot`.
-->
### 特权提升   {#privilege-escalation}

这一组选项控制容器的`allowPrivilegeEscalation` 属性。该属性直接决定是否为
容器进程设置
[`no_new_privs`](https://www.kernel.org/doc/Documentation/prctl/no_new_privs.txt)
参数。此参数会禁止 `setuid` 属性的可执行文件更改有效用户 ID（EUID），并且
禁止启用额外权能的文件。例如，`no_new_privs` 会禁止使用 `ping` 工具。
如果想有效地实施 `MustRunAsNonRoot` 控制，需要配置这一选项。

<!--
**AllowPrivilegeEscalation** - Gates whether or not a user is allowed to set the
security context of a container to `allowPrivilegeEscalation=true`. This
defaults to allowed so as to not break setuid binaries. Setting it to `false`
ensures that no child process of a container can gain more privileges than its parent.
-->
**AllowPrivilegeEscalation** - 决定是否用户可以将容器的安全上下文设置为
`allowPrivilegeEscalation=true`。默认设置下，这样做是允许的，目的是避免
造成现有的 `setuid` 应用无法运行。将此选项设置为 `false` 可以确保容器的所有
子进程都无法获得比父进程更多的特权。

<!--
**DefaultAllowPrivilegeEscalation** - Sets the default for the
`allowPrivilegeEscalation` option. The default behavior without this is to allow
privilege escalation so as to not break setuid binaries. If that behavior is not
desired, this field can be used to default to disallow, while still permitting
pods to request `allowPrivilegeEscalation` explicitly.
-->
**DefaultAllowPrivilegeEscalation** - 为 `allowPrivilegeEscalation` 选项设置
默认值。不设置此选项时的默认行为是允许特权提升，以便运行 setuid 程序。
如果不希望运行 setuid 程序，可以使用此字段将选项的默认值设置为禁止，同时
仍然允许 Pod 显式地请求 `allowPrivilegeEscalation`。 

<!--
### Capabilities

Linux capabilities provide a finer grained breakdown of the privileges
traditionally associated with the superuser. Some of these capabilities can be
used to escalate privileges or for container breakout, and may be restricted by
the PodSecurityPolicy. For more details on Linux capabilities, see
[capabilities(7)](http://man7.org/linux/man-pages/man7/capabilities.7.html).

The following fields take a list of capabilities, specified as the capability
name in ALL_CAPS without the `CAP\_` prefix.
-->
### 权能字    {#capabilities}

Linux 权能字（Capabilities）将传统上与超级用户相关联的特权作了细粒度的分解。
其中某些权能字可以用来提升特权，打破容器边界，可以通过 PodSecurityPolicy
来限制。关于 Linux 权能字的更多细节，可参阅
[capabilities(7)](http://man7.org/linux/man-pages/man7/capabilities.7.html)。

下列字段都可以配置为权能字的列表。表中的每一项都是 `ALL_CAPS` 中的一个权能字
名称，只是需要去掉 `CAP_` 前缀。

<!--
**AllowedCapabilities** - Provides a list of capabilities that are allowed to be added
to a container. The default set of capabilities are implicitly allowed. The
empty set means that no additional capabilities may be added beyond the default
set. `*` can be used to allow all capabilities.
-->
**AllowedCapabilities** - 给出可以被添加到容器的权能字列表。
默认的权能字集合是被隐式允许的那些。空集合意味着只能使用默认权能字集合，
不允许添加额外的权能字。`*` 可以用来设置允许所有权能字。

<!--
**RequiredDropCapabilities** - The capabilities which must be dropped from
containers. These capabilities are removed from the default set, and must not be
added. Capabilities listed in `RequiredDropCapabilities` must not be included in
`AllowedCapabilities` or `DefaultAddCapabilities`.
-->
**RequiredDropCapabilities** - 必须从容器中去除的权能字。
所给的权能字会从默认权能字集合中去除，并且一定不可以添加。
`RequiredDropCapabilities` 中列举的权能字不能出现在
`AllowedCapabilities` 或 `DefaultAddCapabilities` 所给的列表中。

<!--
**DefaultAddCapabilities** - The capabilities which are added to containers by
default, in addition to the runtime defaults. See the [Docker
documentation](https://docs.docker.com/engine/reference/run/#runtime-privilege-and-linux-capabilities)
for the default list of capabilities when using the Docker runtime.
-->
**DefaultAddCapabilities** - 默认添加到容器的权能字集合。
这一集合是作为容器运行时所设值的补充。
关于使用 Docker 容器运行引擎时默认的权能字列表，可参阅
[Docker 文档](https://docs.docker.com/engine/reference/run/#runtime-privilege-and-linux-capabilities)。

<!--
### SELinux

- *MustRunAs* - Requires `seLinuxOptions` to be configured. Uses
`seLinuxOptions` as the default. Validates against `seLinuxOptions`.
- *RunAsAny* - No default provided. Allows any `seLinuxOptions` to be
specified.
-->
### SELinux

- *MustRunAs* - 要求必须配置 `seLinuxOptions`。默认使用 `seLinuxOptions`。
  针对 `seLinuxOptions` 所给值执行验证检查。
- *RunAsAny* - 没有提供默认值。允许任意指定的 `seLinuxOptions` 选项。

<!--
### AllowedProcMountTypes

`allowedProcMountTypes` is a list of allowed ProcMountTypes.
Empty or nil indicates that only the `DefaultProcMountType` may be used.

`DefaultProcMount` uses the container runtime defaults for readonly and masked
paths for /proc.  Most container runtimes mask certain paths in /proc to avoid
accidental security exposure of special devices or information. This is denoted
as the string `Default`.

The only other ProcMountType is `UnmaskedProcMount`, which bypasses the
default masking behavior of the container runtime and ensures the newly
created /proc the container stays intact with no modifications. This is
denoted as the string `Unmasked`.
-->
### AllowedProcMountTypes

`allowedProcMountTypes` 是一组可以允许的 proc 挂载类型列表。
空表或者 nil 值表示只能使用 `DefaultProcMountType`。

`DefaultProcMount` 使用容器运行时的默认值设置来决定 `/proc` 的只读挂载模式
和路径屏蔽。大多数容器运行时都会屏蔽 `/proc` 下面的某些路径以避免特殊设备或
信息被不小心暴露给容器。这一配置使所有 `Default` 字符串值来表示。

此外唯一的ProcMountType 是 `UnmaskedProcMount`，意味着即将绕过容器运行时的
路径屏蔽行为，确保新创建的 `/proc` 不会被容器修改。此配置用字符串
`Unmasked` 来表示。

<!--
### AppArmor

Controlled via annotations on the PodSecurityPolicy. Refer to the [AppArmor
documentation](/docs/tutorials/clusters/apparmor/#podsecuritypolicy-annotations).
-->
### AppArmor

通过 PodSecurityPolicy 上的注解来控制。
详情请参阅
[AppArmor 文档](/zh/docs/tutorials/clusters/apparmor/#podsecuritypolicy-annotations)。


<!--
### Seccomp

The use of seccomp profiles in pods can be controlled via annotations on the
PodSecurityPolicy. Seccomp is an alpha feature in Kubernetes.

**seccomp.security.alpha.kubernetes.io/defaultProfileName** - Annotation that
specifies the default seccomp profile to apply to containers. Possible values
are:
-->
### Seccomp

Pod 对 seccomp 模版的使用可以通过在 PodSecurityPolicy 上设置注解来控制。
Seccomp 是 Kubernetes 的一项 alpha 阶段特性。

**seccomp.security.alpha.kubernetes.io/defaultProfileName** - 注解用来
指定为容器配置默认的 seccomp 模版。可选值为：

<!--
- `unconfined` - Seccomp is not applied to the container processes (this is the
  default in Kubernetes), if no alternative is provided.
- `runtime/default` - The default container runtime profile is used.
- `docker/default` - The Docker default seccomp profile is used. Deprecated as of
  Kubernetes 1.11. Use `runtime/default` instead.
- `localhost/<path>` - Specify a profile as a file on the node located at
  `<seccomp_root>/<path>`, where `<seccomp_root>` is defined via the
  `-seccomp-profile-root` flag on the Kubelet.
-->
- `unconfined` - 如果没有指定其他替代方案，Seccomp 不会被应用到容器进程上
  （Kubernets 中的默认设置）。
- `runtime/default` - 使用默认的容器运行时模版。
- `docker/default` - 使用 Docker 的默认 seccomp 模版。自 1.11 版本废弃。
  应改为使用 `runtime/default`。
- `localhost/<路径名>` - 指定节点上路径 `<seccomp_root>/<路径名>` 下的一个
  文件作为其模版。其中 `<seccomp_root>` 是通过 `kubelet` 的标志
  `--seccomp-profile-root` 来指定的。

<!--
**seccomp.security.alpha.kubernetes.io/allowedProfileNames** - Annotation that
specifies which values are allowed for the pod seccomp annotations. Specified as
a comma-delimited list of allowed values. Possible values are those listed
above, plus `*` to allow all profiles. Absence of this annotation means that the
default cannot be changed.
-->
**seccomp.security.alpha.kubernetes.io/allowedProfileNames** - 指定可以为
Pod seccomp 注解配置的值的注解。取值为一个可用值的列表。
表中每项可以是上述各值之一，还可以是 `*`，用来表示允许所有的模版。
如果没有设置此注解，意味着默认的 seccomp 模版是不可更改的。

<!--
### Sysctl

By default, all safe sysctls are allowed. 
-->
### Sysctl

默认情况下，所有的安全的 sysctl 都是被允许的。

<!--
- `forbiddenSysctls` - excludes specific sysctls. You can forbid a combination of safe and unsafe sysctls in the list. To forbid setting any sysctls, use `*` on its own.
- `allowedUnsafeSysctls` - allows specific sysctls that had been disallowed by the default list, so long as these are not listed in `forbiddenSysctls`.
-->
- `forbiddenSysctls` - 用来排除某些特定的 sysctl。
  你可以在此列表中禁止一些安全的或者不安全的 sysctl。
  此选项设置为 `*` 意味着禁止设置所有 sysctl。
- `allowedUnsafeSysctls` - 用来启用那些被默认列表所禁用的 sysctl，
  前提是所启用的 sysctl 没有被列在 `forbiddenSysctls` 中。

参阅 [Sysctl 文档](/zh/docs/tasks/administer-cluster/sysctl-cluster/#podsecuritypolicy)。

## {{% heading "whatsnext" %}}

<!--
- See [Pod Security Standards](/docs/concepts/security/pod-security-standards/) for policy recommendations.

- Refer to [Pod Security Policy Reference](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#podsecuritypolicy-v1beta1-policy) for the api details.
-->
- 参阅[Pod 安全标准](/zh/docs/concepts/security/pod-security-standards/)
  了解策略建议。
- 阅读 [Pod 安全策略参考](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#podsecuritypolicy-v1beta1-policy)了解 API 细节。
