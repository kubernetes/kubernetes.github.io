---
title: 管理服务账号
content_type: concept
weight: 50
---

<!--
reviewers:
- bprashanth
- davidopp
- lavalamp
- liggitt
title: Managing Service Accounts
content_type: concept
weight: 50
-->

<!-- overview -->
<!--
This is a Cluster Administrator guide to service accounts. You should be familiar with 
[configuring Kubernetes service accounts](/docs/tasks/configure-pod-container/configure-service-account/).

Support for authorization and user accounts is planned but incomplete. Sometimes
incomplete features are referred to in order to better describe service accounts.
-->
这是一篇针对服务账号的集群管理员指南。你应该熟悉
[配置 Kubernetes 服务账号](/zh/docs/tasks/configure-pod-container/configure-service-account/)。

对鉴权和用户账号的支持已在规划中，当前并不完备。
为了更好地描述服务账号，有时这些不完善的特性也会被提及。

<!-- body -->

<!--
## User accounts versus service accounts

Kubernetes distinguishes between the concept of a user account and a service account
for a number of reasons:
-->
## 用户账号与服务账号  {#user-accounts-versus-service-accounts}

Kubernetes 区分用户账号和服务账号的概念，主要基于以下原因：

<!--
- User accounts are for humans. Service accounts are for processes, which run
  in pods.
- User accounts are intended to be global. Names must be unique across all
  namespaces of a cluster. Service accounts are namespaced.
- Typically, a cluster's user accounts might be synced from a corporate
  database, where new user account creation requires special privileges and is
  tied to complex business processes. Service account creation is intended to be
  more lightweight, allowing cluster users to create service accounts for
  specific tasks by following the principle of least privilege.
- Auditing considerations for humans and service accounts may differ.
- A config bundle for a complex system may include definition of various service
  accounts for components of that system. Because service accounts can be created
  without many constraints and have namespaced names, such config is portable.
-->
- 用户账号是针对人而言的。 服务账号是针对运行在 Pod 中的进程而言的。
- 用户账号是全局性的。其名称跨集群中名字空间唯一的。服务账号是名字空间作用域的。
- 通常情况下，集群的用户账号可能会从企业数据库进行同步，其创建需要特殊权限，
  并且涉及到复杂的业务流程。
  服务账号创建有意做得更轻量，允许集群用户为了具体的任务创建服务账号 
  以遵从权限最小化原则。
- 对人员和服务账号审计所考虑的因素可能不同。
- 针对复杂系统的配置包可能包含系统组件相关的各种服务账号的定义。因为服务账号
  的创建约束不多并且有名字空间域的名称，这种配置是很轻量的。

<!--
## Service account automation

Three separate components cooperate to implement the automation around service accounts:

- A `ServiceAccount` admission controller
- A Token controller
- A `ServiceAccount` controller
-->
## 服务账号的自动化   {#service-account-automation}

三个独立组件协作完成服务账号相关的自动化：

- `ServiceAccount` 准入控制器
- Token 控制器
- `ServiceAccount` 控制器

<!--
### ServiceAccount Admission Controller

The modification of pods is implemented via a plugin
called an [Admission Controller](/docs/reference/access-authn-authz/admission-controllers/).
It is part of the API server.
It acts synchronously to modify pods as they are created or updated. When this plugin is active
(and it is by default on most distributions), then it does the following when a pod is created or modified:
-->
### ServiceAccount 准入控制器   {#serviceaccount-admission-controller}

对 Pod 的改动通过一个被称为
[准入控制器](/zh/docs/reference/access-authn-authz/admission-controllers/)
的插件来实现。它是 API 服务器的一部分。
当 Pod 被创建或更新时，它会同步地修改 Pod。
如果该插件处于激活状态（在大多数发行版中都是默认激活的），当 Pod 被创建
或更新时它会进行以下操作：

<!--
1. If the pod does not have a `ServiceAccount` set, it sets the `ServiceAccount` to `default`.
1. It ensures that the `ServiceAccount` referenced by the pod exists, and otherwise rejects it.
1. It adds a `volume` to the pod which contains a token for API access
   if neither the ServiceAccount `automountServiceAccountToken` nor the Pod's
   `automountServiceAccountToken` is set to `false`.
1. It adds a `volumeSource` to each container of the pod mounted at
   `/var/run/secrets/kubernetes.io/serviceaccount`, if the previous step has
   created a volume for ServiceAccount token.
1. If the pod does not contain any `ImagePullSecrets`, then `ImagePullSecrets` of the `ServiceAccount` are added to the pod.
-->
1. 如果该 Pod 没有设置 `ServiceAccount`，将其 `ServiceAccount` 设为 `default`。
1. 保证 Pod 所引用的 `ServiceAccount` 确实存在，否则拒绝该 Pod。
1. 如果服务账号的 `automountServiceAccountToken` 或 Pod 的
   `automountServiceAccountToken` 都未设置为 `false`，则为 Pod 创建一个
   `volume`，在其中包含用来访问 API 的令牌。
1. 如果前一步中为服务账号令牌创建了卷，则为 Pod 中的每个容器添加一个
   `volumeSource`，挂载在其 `/var/run/secrets/kubernetes.io/serviceaccount`
   目录下。
1. 如果 Pod 不包含 `imagePullSecrets` 设置，将 `ServiceAccount` 所引用
   的服务账号中的 `imagePullSecrets` 信息添加到 Pod 中。

<!--
#### Bound Service Account Token Volume
-->
#### 绑定的服务账号令牌卷  {#bound-service-account-token-volume}


{{< feature-state for_k8s_version="v1.21" state="beta" >}}

<!--
When the `BoundServiceAccountTokenVolume` [feature gate](/docs/reference/command-line-tools-reference/feature-gates/) is enabled, the service account admission controller will
add the following projected volume instead of a Secret-based volume for the non-expiring service account token created by Token Controller.
-->
当 `BoundServiceAccountTokenVolume`
[特性门控](/zh/docs/reference/command-line-tools-reference/feature-gates/)
被启用时，服务账号准入控制器将添加如下投射卷，而不是为令牌控制器
所生成的不过期的服务账号令牌而创建的基于 Secret 的卷。

```yaml
- name: kube-api-access-<随机后缀>
  projected:
    defaultMode: 420 # 0644
    sources:
      - serviceAccountToken:
          expirationSeconds: 3600
          path: token
      - configMap:
          items:
            - key: ca.crt
              path: ca.crt
          name: kube-root-ca.crt
      - downwardAPI:
          items:
            - fieldRef:
                apiVersion: v1
                fieldPath: metadata.namespace
              path: namespace
```

<!--
This projected volume consists of three sources:

1. A ServiceAccountToken acquired from kube-apiserver via TokenRequest API. It will expire after 1 hour by default or when the pod is deleted. It is bound to the pod and has kube-apiserver as the audience.
1. A ConfigMap containing a CA bundle used for verifying connections to the kube-apiserver. This feature depends on the `RootCAConfigMap` feature gate being enabled, which publishes a "kube-root-ca.crt" ConfigMap to every namespace. `RootCAConfigMap` is enabled by default in 1.20, and always enabled in 1.21+.
1. A DownwardAPI that references the namespace of the pod.
-->
此投射卷有三个数据源：

1. 通过 TokenRequest API 从 kube-apiserver 处获得的 ServiceAccountToken。
   这一令牌默认会在一个小时之后或者 Pod 被删除时过期。
   该令牌绑定到 Pod 实例上，并将 kube-apiserver 作为其受众（audience）。
1. 包含用来验证与 kube-apiserver 连接的 CA 证书包的 ConfigMap 对象。
   这一特性依赖于 `RootCAConfigMap` 特性门控被启用。该特性被启用时，
   控制面会公开一个名为 `kube-root-ca.crt` 的 ConfigMap 给所有名字空间。
   `RootCAConfigMap` 在 1.20 版本中是默认被启用的，在 1.21 及之后版本中
   总是被启用。
1. 引用 Pod 名字空间的一个 DownwardAPI。

<!--
See more details about [projected volumes](/docs/tasks/configure-pod-container/configure-projected-volume-storage/).

You can manually migrate a secret-based service account volume to a projected volume when
the `BoundServiceAccountTokenVolume` feature gate is not enabled by adding the above
projected volume to the pod spec. However, `RootCAConfigMap` needs to be enabled.
-->
参阅[投射卷](/zh/docs/tasks/configure-pod-container/configure-projected-volume-storage/)
了解进一步的细节。

如果 `BoundServiceAccountTokenVolume` 特性门控未被启用，
你可以手动地将一个基于 Secret 的服务账号卷升级为一个投射卷，
方法是将上述投射卷添加到 Pod 规约中。
不过，这时仍需要启用 `RootCAConfigMap` 特性门控。

<!--
### Token Controller

TokenController runs as part of `kube-controller-manager`. It acts asynchronously. It:

- watches ServiceAccount creation and creates a corresponding
  ServiceAccount token Secret to allow API access.
- watches ServiceAccount deletion and deletes all corresponding ServiceAccount
  token Secrets.
- watches ServiceAccount token Secret addition, and ensures the referenced
  ServiceAccount exists, and adds a token to the Secret if needed.
- watches Secret deletion and removes a reference from the corresponding
  ServiceAccount if needed.
-->
### Token 控制器    {#token-controller}

TokenController 作为 `kube-controller-manager` 的一部分运行，以异步的形式工作。
其职责包括：

- 监测 ServiceAccount 的创建并创建相应的服务账号令牌 Secret 以允许访问 API。
- 监测 ServiceAccount 的删除并删除所有相应的服务账号令牌 Secret。
- 监测服务账号令牌 Secret 的添加，保证相应的 ServiceAccount 存在，如有需要，
  向 Secret 中添加令牌。
- 监测服务账号令牌 Secret 的删除，如有需要，从相应的 ServiceAccount 中移除引用。

<!--
You must pass a service account private key file to the token controller in
the `kube-controller-manager` using the `--service-account-private-key-file`
flag. The private key is used to sign generated service account tokens.
Similarly, you must pass the corresponding public key to the `kube-apiserver`
using the `--service-account-key-file` flag. The public key will be used to
verify the tokens during authentication.
-->
你必须通过 `--service-account-private-key-file` 标志为 `kube-controller-manager`
的令牌控制器传入一个服务账号私钥文件。该私钥用于为所生成的服务账号令牌签名。
同样地，你需要通过 `--service-account-key-file` 标志将对应的公钥通知给
kube-apiserver。公钥用于在身份认证过程中校验令牌。

<!--
#### To create additional API tokens

A controller loop ensures a Secret with an API token exists for each
ServiceAccount. To create additional API tokens for a ServiceAccount, create a
Secret of type `kubernetes.io/service-account-token` with an annotation
referencing the ServiceAccount, and the controller will update it with a
generated token:

Below is a sample configuration for such a Secret:
-->
#### 创建额外的 API 令牌   {#to-create-additional-api-tokens}

控制器中有专门的循环来保证每个 ServiceAccount 都存在对应的包含 API 令牌的 Secret。
当需要为 ServiceAccount 创建额外的 API 令牌时，可以创建一个类型为
`kubernetes.io/service-account-token` 的 Secret，并在其注解中引用对应的
ServiceAccount。控制器会生成令牌并更新该 Secret：

下面是这种 Secret 的一个示例配置：

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: mysecretname
  annotations:
    kubernetes.io/service-account.name: myserviceaccount
type: kubernetes.io/service-account-token
```

```shell
kubectl create -f ./secret.json
kubectl describe secret mysecretname
```

<!--
#### To delete/invalidate a ServiceAccount token Secret
-->
#### 删除/废止服务账号令牌 Secret

```shell
kubectl delete secret mysecretname
```

<!--
### ServiceAccount controller

A ServiceAccount controller manages the ServiceAccounts inside namespaces, and
ensures a ServiceAccount named "default" exists in every active namespace.
-->
### 服务账号控制器   {#serviceaccount-controller}

服务账号控制器管理各名字空间下的 ServiceAccount 对象，并且保证每个活跃的
名字空间下存在一个名为 "default" 的 ServiceAccount。

