---
title: 安装一个扩展的 API server
content_type: task
weight: 15
---

<!--
title: Setup an extension API server
reviewers:
- lavalamp
- cheftako
- chenopis
content_type: task
weight: 15
-->

<!-- overview -->

<!--
Setting up an extension API server to work the aggregation layer allows the Kubernetes apiserver to be extended with additional APIs, which are not part of the core Kubernetes APIs.
-->
安装扩展的 API 服务器来使用聚合层以让 Kubernetes API 服务器使用
其它 API 进行扩展，
这些 API 不是核心 Kubernetes API 的一部分。

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}

<!--
* You must [configure the aggregation layer](/docs/tasks/access-kubernetes-api/configure-aggregation-layer/) and enable the apiserver flags.
-->
* 你必须[配置聚合层](/zh/docs/tasks/extend-kubernetes/configure-aggregation-layer/)
  并且启用 API 服务器的相关参数。

<!-- steps -->

<!--
## Setup an extension api-server to work with the aggregation layer

The following steps describe how to set up an extension-apiserver *at a high level*. These steps apply regardless if you're using YAML configs or using APIs. An attempt is made to specifically identify any differences between the two. For a concrete example of how they can be implemented using YAML configs, you can look at the [sample-apiserver](https://github.com/kubernetes/sample-apiserver/blob/master/README.md) in the Kubernetes repo.

Alternatively, you can use an existing 3rd party solution, such as [apiserver-builder](https://github.com/Kubernetes-incubator/apiserver-builder/blob/master/README.md), which should generate a skeleton and automate all of the following steps for you.
-->
## 安装一个扩展的 API 服务器来使用聚合层

以下步骤描述如何 *在一个高层次* 设置一个扩展的 apiserver。无论你使用的是 YAML 配置还是使用 API，这些步骤都适用。
目前我们正在尝试区分出两者的区别。有关使用 YAML 配置的具体示例，你可以在 Kubernetes 库中查看
[sample-apiserver](https://github.com/kubernetes/sample-apiserver/blob/master/README.md)。

或者，你可以使用现有的第三方解决方案，例如
[apiserver-builder](https://github.com/Kubernetes-incubator/apiserver-builder/blob/master/README.md)，
它将生成框架并自动执行以下所有步骤。

<!--
1. Make sure the APIService API is enabled (check `-runtime-config`). It should be on by default, unless it's been deliberately turned off in your cluster.
1. You may need to make an RBAC rule allowing you to add APIService objects, or get your cluster administrator to make one. (Since API extensions affect the entire cluster, it is not recommended to do testing/development/debug of an API extension in a live cluster.)
1. Create the Kubernetes namespace you want to run your extension api-service in.
1. Create/get a CA cert to be used to sign the server cert the extension api-server uses for HTTPS.
1. Create a server cert/key for the api-server to use for HTTPS. This cert should be signed by the above CA. It should also have a CN of the Kube DNS name. This is derived from the Kubernetes service and be of the form `<service name>.<service name namespace>.svc`
1. Create a Kubernetes secret with the server cert/key in your namespace.
1. Create a Kubernetes deployment for the extension api-server and make sure you are loading the secret as a volume. It should contain a reference to a working image of your extension api-server. The deployment should also be in your namespace.
-->
1. 确保启用了 APIService API（检查 `--runtime-config`）。默认应该是启用的，除非被特意关闭了。
2. 你可能需要制定一个 RBAC 规则，以允许你添加 APIService 对象，或让你的集群管理员创建一个。
  （由于 API 扩展会影响整个集群，因此不建议在实时集群中对 API 扩展进行测试/开发/调试）
3. 创建 Kubernetes 命名空间，扩展的 api-service 将运行在该命名空间中。
4. 创建（或获取）用来签署服务器证书的 CA 证书，扩展 api-server 中将使用该证书做 HTTPS 连接。
5. 为 api-server 创建一个服务端的证书（或秘钥）以使用 HTTPS。这个证书应该由上述的 CA 签署。
   同时应该还要有一个 Kube DNS 名称的 CN，这是从 Kubernetes 服务派生而来的，
   格式为 `<service name>.<service name namespace>.svc`。
6. 使用命名空间中的证书（或秘钥）创建一个 Kubernetes secret。
7. 为扩展 api-server 创建一个 Kubernetes Deployment，并确保以卷的方式挂载了 Secret。
   它应该包含对扩展 api-server 镜像的引用。Deployment 也应该在同一个命名空间中。

<!--
1. Make sure that your extension-apiserver loads those certs from that volume and that they are used in the HTTPS handshake.
1. Create a Kubernetes service account in your namespace.
1. Create a Kubernetes cluster role for the operations you want to allow on your resources.
1. Create a Kubernetes cluster role binding from the service account in your namespace to the cluster role you created.
1. Create a Kubernetes cluster role binding from the service account in your namespace to the `system:auth-delegator` cluster role to delegate auth decisions to the Kubernetes core API server.
1. Create a Kubernetes role binding from the service account in your namespace to the `extension-apiserver-authentication-reader` role. This allows your extension api-server to access the `extension-apiserver-authentication` configmap.
-->
8.  确保你的扩展 apiserver 从该卷中加载了那些证书，并在 HTTPS 握手过程中使用它们。
9.  在你的命名空间中创建一个 Kubernetes 服务账号。
10. 为资源允许的操作创建 Kubernetes 集群角色。
11. 用你命名空间中的服务账号创建一个 Kubernetes 集群角色绑定，绑定到你创建的角色上。
12. 用你命名空间中的服务账号创建一个 Kubernetes 集群角色绑定，绑定到 `system:auth-delegator`
    集群角色，以将 auth 决策委派给 Kubernetes 核心 API 服务器。
13. 以你命名空间中的服务账号创建一个 Kubernetes 集群角色绑定，绑定到
    `extension-apiserver-authentication-reader` 角色。
    这将让你的扩展 api-server 能够访问 `extension-apiserver-authentication` configmap。

<!--
1. Create a Kubernetes apiservice. The CA cert above should be base64 encoded, stripped of new lines and used as the spec.caBundle in the apiservice. This should not be namespaced. If using the [kube-aggregator API](https://github.com/kubernetes/kube-aggregator/), only pass in the PEM encoded CA bundle because the base 64 encoding is done for you.
1. Use kubectl to get your resource. When run, kubectl should return "No resources found.". This message indicates that everything worked but you currently have no objects of that resource type created.
-->
14. 创建一个 Kubernetes apiservice。
    上述的 CA 证书应该使用 base64 编码，剥离新行并用作 apiservice 中的 spec.caBundle。
    该资源不应放到任何名字空间。如果使用了
    [kube-aggregator API](https://github.com/kubernetes/kube-aggregator/)，那么只需要传入
    PEM 编码的 CA 绑定，因为 base 64 编码已经完成了。
15. 使用 kubectl 来获得你的资源。
    它应该返回 "找不到资源"。此消息表示一切正常，但你目前还没有创建该资源类型的对象。

## {{% heading "whatsnext" %}}

<!--
* If you haven't already, [configure the aggregation layer](/docs/tasks/access-kubernetes-api/configure-aggregation-layer/) and enable the apiserver flags.
* For a high level overview, see [Extending the Kubernetes API with the aggregation layer](/docs/concepts/api-extension/apiserver-aggregation).
* Learn how to [Extend the Kubernetes API Using Custom Resource Definitions](/docs/tasks/access-kubernetes-api/extend-api-custom-resource-definitions/).
-->
* 如果你还未配置，请[配置聚合层](/zh/docs/tasks/extend-kubernetes/configure-aggregation-layer/)
  并启用 apiserver 的相关参数。
* 高级概述，请参阅[使用聚合层扩展 Kubernetes API](/zh/docs/concepts/extend-kubernetes/api-extension/apiserver-aggregation)。
* 了解如何[使用 Custom Resource Definition 扩展 Kubernetes API](/zh/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/)。
