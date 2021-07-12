---
title: TLS 启动引导
content_type: concept
---
<!--
reviewers:
- mikedanese
- liggitt
- smarterclayton
- awly
title: TLS bootstrapping
content_type: concept
-->

<!-- overview -->

<!--
In a Kubernetes cluster, the components on the worker nodes - kubelet and kube-proxy - need to communicate with Kubernetes master components, specifically kube-apiserver.
In order to ensure that communication is kept private, not interfered with, and ensure that each component of the cluster is talking to another trusted component, we strongly
recommend using client TLS certificates on nodes.
-->
在一个 Kubernetes 集群中，工作节点上的组件（kubelet 和 kube-proxy）需要与
Kubernetes 主控组件通信，尤其是 kube-apiserver。
为了确保通信本身是私密的、不被干扰，并且确保集群的每个组件都在与另一个
可信的组件通信，我们强烈建议使用节点上的客户端 TLS 证书。

<!--
The normal process of bootstrapping these components, especially worker nodes that need certificates so they can communicate safely with kube-apiserver,
can be a challenging process as it is often outside of the scope of Kubernetes and requires significant additional work.
This in turn, can make it challenging to initialize or scale a cluster.
-->
启动引导这些组件的正常过程，尤其是需要证书来与 kube-apiserver 安全通信的
工作节点，可能会是一个具有挑战性的过程，因为这一过程通常不受 Kubernetes 控制，
需要不少额外工作。
这也使得初始化或者扩缩一个集群的操作变得具有挑战性。

<!--
In order to simplify the process, beginning in version 1.4, Kubernetes introduced a certificate request and signing API to simplify the process. The proposal can be
found [here](https://github.com/kubernetes/kubernetes/pull/20439).

This document describes the process of node initialization, how to set up TLS client certificate bootstrapping for
kubelets, and how it works.
-->
为了简化这一过程，从 1.4 版本开始，Kubernetes 引入了一个证书请求和签名
API 以便简化此过程。该提案可在
[这里](https://github.com/kubernetes/kubernetes/pull/20439)看到。

本文档描述节点初始化的过程，如何为 kubelet 配置 TLS 客户端证书启动引导，
以及其背后的工作原理。

<!-- body -->

<!--
## Initialization Process

When a worker node starts up, the kubelet does the following:
-->
## 初始化过程   {#initialization-process}

当工作节点启动时，kubelet 执行以下操作：

<!--
1. Look for its `kubeconfig` file
2. Retrieve the URL of the API server and credentials, normally a TLS key and signed certificate from the `kubeconfig` file
3. Attempt to communicate with the API server using the credentials.
-->
1. 寻找自己的 `kubeconfig` 文件
2. 检索 API 服务器的 URL 和凭据，通常是来自 `kubeconfig` 文件中的
   TLS 密钥和已签名证书
3. 尝试使用这些凭据来与 API 服务器通信

<!--
Assuming that the kube-apiserver successfully validates the kubelet's credentials, it will treat the kubelet as a valid node, and begin to assign pods to it.

Note that the above process depends upon:

* Existence of a key and certificate on the local host in the `kubeconfig`
* The certificate having been signed by a Certificate Authority (CA) trusted by the kube-apiserver
-->
假定 kube-apiserver 成功地认证了 kubelet 的凭据数据，它会将 kubelet 视为
一个合法的节点并开始将 Pods 分派给该节点。

注意，签名的过程依赖于：

* `kubeconfig` 中包含密钥和本地主机的证书
* 证书被 kube-apiserver 所信任的一个证书机构（CA）所签名

<!--
All of the following are responsibilities of whoever sets up and manages the cluster:

1. Creating the CA key and certificate
2. Distributing the CA certificate to the master nodes, where kube-apiserver is running
3. Creating a key and certificate for each kubelet; strongly recommended to have a unique one, with a unique CN, for each kubelet
4. Signing the kubelet certificate using the CA key
5. Distributing the kubelet key and signed certificate to the specific node on which the kubelet is running

The TLS Bootstrapping described in this document is intended to simplify, and partially or even completely automate, steps 3 onwards, as these are the most common when initializing or scaling
a cluster.
-->
负责部署和管理集群的人有以下责任：

1. 创建 CA 密钥和证书
2. 将 CA 证书发布到 kube-apiserver 运行所在的主控节点上
3. 为每个 kubelet 创建密钥和证书；强烈建议为每个 kubelet 使用独一无二的、
   CN 取值与众不同的密钥和证书
4. 使用 CA 密钥对 kubelet 证书签名
5. 将 kubelet 密钥和签名的证书发布到 kubelet 运行所在的特定节点上

本文中描述的 TLS 启动引导过程有意简化甚至完全自动化上述过程，尤其是
第三步之后的操作，因为这些步骤是初始化或者扩缩集群时最常见的操作。

<!--
### Bootstrap Initialization

In the bootstrap initialization process, the following occurs:
-->
### 启动引导初始化   {#bootstrap-initialization}

在启动引导初始化过程中，会发生以下事情：

<!--
1. kubelet begins
2. kubelet sees that it does _not_ have a `kubeconfig` file
3. kubelet searches for and finds a `bootstrap-kubeconfig` file
4. kubelet reads its bootstrap file, retrieving the URL of the API server and a limited usage "token"
5. kubelet connects to the API server, authenticates using the token
6. kubelet now has limited credentials to create and retrieve a certificate signing request (CSR)
7. kubelet creates a CSR for itself with the signerName set to `kubernetes.io/kube-apiserver-client-kubelet`
8. CSR is approved in one of two ways:
  * If configured, kube-controller-manager automatically approves the CSR
  * If configured, an outside process, possibly a person, approves the CSR using the Kubernetes API or via `kubectl`
9. Certificate is created for the kubelet
-->
1. kubelet 启动
2. kubelet 看到自己 *没有* 对应的 `kubeconfig` 文件
3. kubelet 搜索并发现 `bootstrap-kubeconfig` 文件
4. kubelet 读取该启动引导文件，从中获得 API 服务器的 URL 和用途有限的
   一个“令牌（Token）”
5. kubelet 建立与 API 服务器的连接，使用上述令牌执行身份认证
6. kubelet 现在拥有受限制的凭据来创建和取回证书签名请求（CSR）
7. kubelet 为自己创建一个 CSR，并将其 signerName 设置为 `kubernetes.io/kube-apiserver-client-kubelet`
8. CSR 被以如下两种方式之一批复：
  * 如果配置了，kube-controller-manager 会自动批复该 CSR
  * 如果配置了，一个外部进程，或者是人，使用 Kubernetes API 或者使用 `kubectl`
    来批复该 CSR
9. kubelet 所需要的证书被创建
<!--
10. Certificate is issued to the kubelet
11. kubelet retrieves the certificate
12. kubelet creates a proper `kubeconfig` with the key and signed certificate
13. kubelet begins normal operation
14. Optional: if configured, kubelet automatically requests renewal of the certificate when it is close to expiry
15. The renewed certificate is approved and issued, either automatically or manually, depending on configuration.
-->
10. 证书被发放给 kubelet
11. kubelet 取回该证书
12. kubelet 创建一个合适的 `kubeconfig`，其中包含密钥和已签名的证书
13. kubelet 开始正常操作
14. 可选地，如果配置了，kubelet 在证书接近于过期时自动请求更新证书
15. 更新的证书被批复并发放；取决于配置，这一过程可能是自动的或者手动完成

<!--
The rest of this document describes the necessary steps to configure TLS Bootstrapping, and its limitations.
-->
本文的其余部分描述配置 TLS 启动引导的必要步骤及其局限性。

<!--
## Configuration

To configure for TLS bootstrapping and optional automatic approval, you must configure options on the following components:

* kube-apiserver
* kube-controller-manager
* kubelet
* in-cluster resources: `ClusterRoleBinding` and potentially `ClusterRole`

In addition, you need your Kubernetes Certificate Authority (CA).
-->
## 配置    {#configuration}

要配置 TLS 启动引导及可选的自动批复，你必须配置以下组件的选项：

* kube-apiserver
* kube-controller-manager
* kubelet
* 集群内的资源：`ClusterRoleBinding` 以及可能需要的 `ClusterRole`

此外，你需要有 Kubernetes 证书机构（Certificate Authority，CA）。

<!--
## Certificate Authority

As without bootstrapping, you will need a Certificate Authority (CA) key and certificate. As without bootstrapping, these will be used
to sign the kubelet certificate. As before, it is your responsibility to distribute them to master nodes.
-->
## 证书机构   {#certificate-authority}

就像在没有启动引导的情况下，你会需要证书机构（CA）密钥和证书。
这些数据会被用来对 kubelet 证书进行签名。
如前所述，将证书机构密钥和证书发布到主控节点是你的责任。

<!--
For the purposes of this document, we will assume these have been distributed to master nodes at `/var/lib/kubernetes/ca.pem` (certificate) and `/var/lib/kubernetes/ca-key.pem` (key).
We will refer to these as "Kubernetes CA certificate and key".

All Kubernetes components that use these certificates - kubelet, kube-apiserver, kube-controller-manager - assume the key and certificate to be PEM-encoded.
-->
就本文而言，我们假定这些数据被发布到主控节点上的
`/var/lib/kubernetes/ca.pem`（证书）和
`/var/lib/kubernetes/ca-key.pem`（密钥）文件中。
我们将这两个文件称作“Kubernetes CA 证书和密钥”。
所有 Kubernetes 组件（kubelet、kube-apiserver、kube-controller-manager）都使用
这些凭据，并假定这里的密钥和证书都是 PEM 编码的。

<!--
## kube-apiserver configuration

The kube-apiserver has several requirements to enable TLS bootstrapping:

* Recognizing CA that signs the client certificate
* Authenticating the bootstrapping kubelet to the `system:bootstrappers` group
* Authorize the bootstrapping kubelet to create a certificate signing request (CSR)
-->
## kube-apiserver 配置   {#kube-apiserver-configuration}

启用 TLS 启动引导对 kube-apiserver 有若干需求：

* 能够识别对客户端证书进行签名的 CA
* 能够对启动引导的 kubelet 执行身份认证，并将其置入 `system:bootstrappers` 组
* 能够对启动引导的 kubelet 执行鉴权操作，允许其创建证书签名请求（CSR）

<!--
### Recognizing client certificates

This is normal for all client certificate authentication.
If not already set, add the `--client-ca-file=FILENAME` flag to the kube-apiserver command to enable
client certificate authentication, referencing a certificate authority bundle
containing the signing certificate, for example
`--client-ca-file=/var/lib/kubernetes/ca.pem`.
-->
### 识别客户证书    {#recognizing-client-certificates}

对于所有客户端证书的认证操作而言，这是很常见的。
如果还没有设置，要为 kube-apiserver 命令添加 `--client-ca-file=FILENAME`
标志来启用客户端证书认证，在标志中引用一个包含用来签名的证书的证书机构包，
例如：`--client-ca-file=/var/lib/kubernetes/ca.pem`。

<!--
### Initial bootstrap authentication

In order for the bootstrapping kubelet to connect to kube-apiserver and request a certificate, it must first authenticate to the server.
You can use any [authenticator](/docs/reference/access-authn-authz/authentication/) that can authenticate the kubelet.
-->
### 初始启动引导认证     {#initial-bootstrap-authentication}

为了让启动引导的 kubelet 能够连接到 kube-apiserver 并请求证书，
它必须首先在服务器上认证自身身份。你可以使用任何一种能够对 kubelet 执行身份认证的
[身份认证组件](/zh/docs/reference/access-authn-authz/authentication/)。

<!--
While any authentication strategy can be used for the kubelet's initial
bootstrap credentials, the following two authenticators are recommended for ease
of provisioning.

1. [Bootstrap Tokens](#bootstrap-tokens)
2. [Token authentication file](#token-authentication-file)
-->
尽管所有身份认证策略都可以用来对 kubelet 的初始启动凭据来执行认证，
出于容易准备的因素，建议使用如下两个身份认证组件：

1. [启动引导令牌（Bootstrap Token）](#bootstrap-tokens)
2. [令牌认证文件](#token-authentication-file)

<!--
Bootstrap tokens are a simpler and more easily managed method to authenticate kubelets, and do not require any additional flags when starting kube-apiserver.
Using bootstrap tokens is currently __beta__ as of Kubernetes version 1.12.
-->
启动引导令牌是一种对 kubelet 进行身份认证的方法，相对简单且容易管理，
且不需要在启动 kube-apiserver 时设置额外的标志。
启动引导令牌从 Kubernetes 1.12 开始是一种 __Beta__ 功能特性。

<!--
Whichever method you choose, the requirement is that the kubelet be able to authenticate as a user with the rights to:

1. create and retrieve CSRs
2. be automatically approved to request node client certificates, if automatic approval is enabled.
-->
无论选择哪种方法，这里的需求是 kubelet 能够被身份认证为某个具有如下权限的用户：

1. 创建和读取 CSR
2. 在启用了自动批复时，能够在请求节点客户端证书时得到自动批复

<!--
A kubelet authenticating using bootstrap tokens is authenticated as a user in the group `system:bootstrappers`, which is the standard method to use.
-->
使用启动引导令牌执行身份认证的 kubelet 会被认证为 `system:bootstrappers`
组中的用户。这是使用启动引导令牌的一种标准方法。

<!--
As this feature matures, you
should ensure tokens are bound to a Role Based Access Control (RBAC) policy
which limits requests (using the [bootstrap token](/docs/reference/access-authn-authz/bootstrap-tokens/)) strictly to client
requests related to certificate provisioning. With RBAC in place, scoping the
tokens to a group allows for great flexibility. For example, you could disable a
particular bootstrap group's access when you are done provisioning the nodes.
-->
随着这个功能特性的逐渐成熟，你需要确保令牌绑定到某基于角色的的访问控制（RBAC）
策略上，从而严格限制请求（使用[启动引导令牌](/zh/docs/reference/access-authn-authz/bootstrap-tokens/)）
仅限于客户端申请提供证书。当 RBAC 被配置启用时，可以将令牌限制到某个组，从而
提高灵活性。例如，你可以在准备节点期间禁止某特定启动引导组的访问。

<!--
#### Bootstrap tokens

Bootstrap tokens are described in detail [here](/docs/reference/access-authn-authz/bootstrap-tokens/). These are tokens that are stored as secrets in the Kubernetes cluster,
and then issued to the individual kubelet. You can use a single token for an entire cluster, or issue one per worker node.
-->
#### 启动引导令牌   {#bootstrap-tokens}

启动引导令牌的细节在[这里](/zh/docs/reference/access-authn-authz/bootstrap-tokens/)
详述。启动引导令牌在 Kubernetes 集群中存储为 Secret 对象，被发放给各个 kubelet。
你可以在整个集群中使用同一个令牌，也可以为每个节点发放单独的令牌。

<!--
The process is two-fold:

1. Create a Kubernetes secret with the token ID, secret and scope(s).
2. Issue the token to the kubelet
-->
这一过程有两个方面：

1. 基于令牌 ID、机密数据和范畴信息创建 Kubernetes Secret
2. 将令牌发放给 kubelet

<!--
From the kubelet's perspective, one token is like another and has no special meaning.
From the kube-apiserver's perspective, however, the bootstrap token is special. Due to its `type`, `namespace` and `name`, kube-apiserver recognizes it as a special token,
and grants anyone authenticating with that token special bootstrap rights, notably treating them as a member of the `system:bootstrappers` group. This fulfills a basic requirement
for TLS bootstrapping.
-->
从 kubelet 的角度，所有令牌看起来都很像，没有特别的含义。
从 kube-apiserver 服务器的角度，启动引导令牌是很特殊的。
根据其 `type`、`namespace` 和 `name`，kube-apiserver 能够将认作特殊的令牌，
并授予携带该令牌的任何人特殊的启动引导权限，换言之，将其视为
`system:bootstrappers` 组的成员。这就满足了 TLS 启动引导的基本需求。

<!--
The details for creating the secret are available [here](/docs/reference/access-authn-authz/bootstrap-tokens/).

If you want to use bootstrap tokens, you must enable it on kube-apiserver with the flag:
-->
关于创建 Secret 的进一步细节可访问[这里](/zh/docs/reference/access-authn-authz/bootstrap-tokens/)。

如果你希望使用启动引导令牌，你必须在 kube-apiserver 上使用下面的标志启用之：

```console
--enable-bootstrap-token-auth=true
```

<!--
#### Token authentication file

kube-apiserver has an ability to accept tokens as authentication.
These tokens are arbitrary but should represent at least 128 bits of entropy derived
from a secure random number generator (such as `/dev/urandom` on most modern Linux
systems). There are multiple ways you can generate a token. For example:
-->
#### 令牌认证文件    {#token-authentication-file}

kube-apiserver 能够将令牌视作身份认证依据。
这些令牌可以是任意数据，但必须表示为基于某安全的随机数生成器而得到的
至少 128 位混沌数据。这里的随机数生成器可以是现代 Linux 系统上的
`/dev/urandom`。生成令牌的方式有很多种。例如：

```shell
head -c 16 /dev/urandom | od -An -t x | tr -d ' '
```

<!--
will generate tokens that look like `02b50b05283e98dd0fd71db496ef01e8`.

The token file should look like the following example, where the first three
values can be anything and the quoted group name should be as depicted:
-->
上面的命令会生成类似于 `02b50b05283e98dd0fd71db496ef01e8` 这样的令牌。 

令牌文件看起来是下面的例子这样，其中前面三个值可以是任何值，用引号括起来
的组名称则只能用例子中给的值。

```console
02b50b05283e98dd0fd71db496ef01e8,kubelet-bootstrap,10001,"system:bootstrappers"
```

<!--
Add the `--token-auth-file=FILENAME` flag to the kube-apiserver command (in your
systemd unit file perhaps) to enable the token file.  See docs
[here](/docs/reference/access-authn-authz/authentication/#static-token-file) for
further details.
-->
向 kube-apiserver 添加 `--token-auth-file=FILENAME` 标志（或许这要对 systemd
的单元文件作修改）以启用令牌文件。参见
[这里](/zh/docs/reference/access-authn-authz/authentication/#static-token-file)
的文档以了解进一步的细节。

<!--
### Authorize kubelet to create CSR

Now that the bootstrapping node is _authenticated_ as part of the
`system:bootstrappers` group, it needs to be _authorized_ to create a
certificate signing request (CSR) as well as retrieve it when done.
Fortunately, Kubernetes ships with a `ClusterRole` with precisely these (and
only these) permissions, `system:node-bootstrapper`.

To do this, you only need to create a `ClusterRoleBinding` that binds the `system:bootstrappers` group to the cluster role `system:node-bootstrapper`.
-->
### 授权 kubelet 创建 CSR    {#authorize-kubelet-to-create-csr}

现在启动引导节点被身份认证为 `system:bootstrapping` 组的成员，它需要被 _授权_
创建证书签名请求（CSR）并在证书被签名之后将其取回。
幸运的是，Kubernetes 提供了一个 `ClusterRole`，其中精确地封装了这些许可，
`system:node-bootstrapper`。

为了实现这一点，你只需要创建 `ClusterRoleBinding`，将 `system:bootstrappers`
组绑定到集群角色 `system:node-bootstrapper`。

```yaml
# 允许启动引导节点创建 CSR
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: create-csrs-for-bootstrapping
subjects:
- kind: Group
  name: system:bootstrappers
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: system:node-bootstrapper
  apiGroup: rbac.authorization.k8s.io
```

<!--
## kube-controller-manager configuration

While the apiserver receives the requests for certificates from the kubelet and authenticates those requests,
the controller-manager is responsible for issuing actual signed certificates.
-->
## kube-controller-manager 配置   {#kube-controller-manager-configuration}

API 服务器从 kubelet 收到证书请求并对这些请求执行身份认证，但真正负责发放
签名证书的是控制器管理器。

<!--
The controller-manager performs this function via a certificate-issuing control loop.
This takes the form of a
[cfssl](https://blog.cloudflare.com/introducing-cfssl/) local signer using
assets on disk. Currently, all certificates issued have one year validity and a
default set of key usages.
-->
控制器管理器通过一个证书发放的控制回路来执行此操作。该操作的执行方式是使用磁盘上
的文件用 [cfssl](https://blog.cloudflare.com/introducing-cfssl/) 本地签名组件
来完成。目前，所发放的所有证书都有一年的有效期，并设定了默认的一组密钥用法。

<!--
In order for the controller-manager to sign certificates, it needs the following:

* access to the "Kubernetes CA key and certificate" that you created and distributed
* enabling CSR signing
-->
为了让控制器管理器对证书签名，它需要：

* 能够访问你之前所创建并分发的“Kubernetes CA 密钥和证书”
* 启用 CSR 签名

<!--
### Access to key and certificate

As described earlier, you need to create a Kubernetes CA key and certificate, and distribute it to the master nodes.
These will be used by the controller-manager to sign the kubelet certificates.
-->
### 访问密钥和证书   {#access-to-key-and-certificate}

如前所述，你需要创建一个 Kubernetes CA 密钥和证书，并将其发布到主控节点。
这些数据会被控制器管理器来对 kubelet 证书进行签名。

<!--
Since these signed certificates will, in turn, be used by the kubelet to authenticate as a regular kubelet to kube-apiserver, it is important that the CA
provided to the controller-manager at this stage also be trusted by kube-apiserver for authentication. This is provided to kube-apiserver
with the flag `--client-ca-file=FILENAME` (for example, `--client-ca-file=/var/lib/kubernetes/ca.pem`), as described in the kube-apiserver configuration section.

To provide the Kubernetes CA key and certificate to kube-controller-manager, use the following flags:
-->
由于这些被签名的证书反过来会被 kubelet 用来在 kube-apiserver 执行普通的
kubelet 身份认证，很重要的一点是为控制器管理器所提供的 CA 也被 kube-apiserver
信任用来执行身份认证。CA 密钥和证书是通过 kube-apiserver 的标志
`--client-ca-file=FILENAME`（例如，`--client-ca-file=/var/lib/kubernetes/ca.pem`)，
来设定的，正如 kube-apiserver 配置节所述。

要将 Kubernetes CA 密钥和证书提供给 kube-controller-manager，可使用以下标志：

```shell
--cluster-signing-cert-file="/etc/path/to/kubernetes/ca/ca.crt" --cluster-signing-key-file="/etc/path/to/kubernetes/ca/ca.key"
```

<!--
For example:
-->
例如：

```shell
--cluster-signing-cert-file="/var/lib/kubernetes/ca.pem" --cluster-signing-key-file="/var/lib/kubernetes/ca-key.pem"
```

<!--
The validity duration of signed certificates can be configured with flag:
-->
所签名的证书的合法期限可以通过下面的标志来配置：

```shell
--cluster-signing-duration
```

<!--
### Approval

In order to approve CSRs, you need to tell the controller-manager that it is acceptable to approve them. This is done by granting
RBAC permissions to the correct group.
-->
### 批复    {#approval}

为了对 CSR 进行批复，你需要告诉控制器管理器批复这些 CSR 是可接受的。
这是通过将 RBAC 访问权限授予正确的组来实现的。

<!--
There are two distinct sets of permissions:

* `nodeclient`: If a node is creating a new certificate for a node, then it does not have a certificate yet. It is authenticating using one of the tokens listed above, and thus is part of the group `system:bootstrappers`.
* `selfnodeclient`: If a node is renewing its certificate, then it already has a certificate (by definition), which it uses continuously to authenticate as part of the group `system:nodes`.
-->
许可权限有两组：

* `nodeclient`：如果节点在为节点创建新的证书，则该节点还没有证书。该节点
  使用前文所列的令牌之一来执行身份认证，因此是组 `system:bootstrappers` 组
  的成员。
* `selfnodeclient`：如果节点在对证书执行续期操作，则该节点已经拥有一个证书。
  节点持续使用现有的证书将自己认证为 `system:nodes` 组的成员。

<!--
To enable the kubelet to request and receive a new certificate, create a `ClusterRoleBinding` that binds the group in which the bootstrapping node is a member `system:bootstrappers` to the `ClusterRole` that grants it permission, `system:certificates.k8s.io:certificatesigningrequests:nodeclient`:
-->
要允许 kubelet 请求并接收新的证书，可以创建一个 `ClusterRoleBinding` 将启动
引导节点所处的组 `system:bootstrappers` 绑定到为其赋予访问权限的
`ClusterRole` `system:certificates.k8s.io:certificatesigningrequests:nodeclient`：

```yaml
# 批复 "system:bootstrappers" 组的所有 CSR
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: auto-approve-csrs-for-group
subjects:
- kind: Group
  name: system:bootstrappers
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: system:certificates.k8s.io:certificatesigningrequests:nodeclient
  apiGroup: rbac.authorization.k8s.io
```

<!--
To enable the kubelet to renew its own client certificate, create a `ClusterRoleBinding` that binds the group in which the fully functioning node is a member `system:nodes` to the `ClusterRole` that
grants it permission, `system:certificates.k8s.io:certificatesigningrequests:selfnodeclient`:
-->
要允许 kubelet 对其客户端证书执行续期操作，可以创建一个 `ClusterRoleBinding`
将正常工作的节点所处的组 `system:nodes` 绑定到为其授予访问许可的 `ClusterRole`
`system:certificates.k8s.io:certificatesigningrequests:selfnodeclient`：

```yaml
# 批复 "system:nodes" 组的 CSR 续约请求
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: auto-approve-renewals-for-nodes
subjects:
- kind: Group
  name: system:nodes
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: system:certificates.k8s.io:certificatesigningrequests:selfnodeclient
  apiGroup: rbac.authorization.k8s.io
```

<!--
The `csrapproving` controller that ships as part of
[kube-controller-manager](/docs/admin/kube-controller-manager/) and is enabled
by default. The controller uses the [`SubjectAccessReview`
API](/docs/reference/access-authn-authz/authorization/#checking-api-access) to
determine if a given user is authorized to request a CSR, then approves based on
the authorization outcome. To prevent conflicts with other approvers, the
builtin approver doesn't explicitly deny CSRs. It only ignores unauthorized
requests. The controller also prunes expired certificates as part of garbage
collection.
-->
作为 [kube-controller-manager](/zh/docs/reference/generated/kube-controller-manager/)
的一部分的 `csrapproving` 控制器是自动被启用的。
该控制器使用 [`SubjectAccessReview` API](/zh/docs/reference/access-authn-authz/authorization/#checking-api-access)
来确定是否某给定用户被授权请求 CSR，之后基于鉴权结果执行批复操作。
为了避免与其它批复组件发生冲突，内置的批复组件不会显式地拒绝任何 CSRs。
该组件仅是忽略未被授权的请求。
控制器也会作为垃圾收集的一部分清除已过期的证书。

<!--
## kubelet configuration

Finally, with the master nodes properly set up and all of the necessary authentication and authorization in place, we can configure the kubelet.
-->
## kubelet 配置   {#kubelet-configuration}

最后，当主控节点被正确配置并且所有必要的身份认证和鉴权机制都就绪时，
我们可以配置 kubelet。

<!--
The kubelet requires the following configuration to bootstrap:

* A path to store the key and certificate it generates (optional, can use default)
* A path to a `kubeconfig` file that does not yet exist; it will place the bootstrapped config file here
* A path to a bootstrap `kubeconfig` file to provide the URL for the server and bootstrap credentials, e.g. a bootstrap token
* Optional: instructions to rotate certificates
-->
kubelet 需要以下配置来执行启动引导：

* 一个用来存储所生成的密钥和证书的路径（可选，可以使用默认配置）
* 一个用来指向尚不存在的 `kubeconfig` 文件的路径；kubelet 会将启动引导
  配置文件放到这个位置
* 一个指向启动引导 `kubeconfig` 文件的路径，用来提供 API 服务器的 URL
  和启动引导凭据，例如，启动引导令牌
* 可选的：轮换证书的指令

<!--
The bootstrap `kubeconfig` should be in a path available to the kubelet, for example `/var/lib/kubelet/bootstrap-kubeconfig`.

Its format is identical to a normal `kubeconfig` file. A sample file might look as follows:
-->
启动引导 `kubeconfig` 文件应该放在一个 kubelet 可访问的路径下，例如
`/var/lib/kubelet/bootstrap-kubeconfig`。

其格式与普通的 `kubeconfig` 文件完全相同。实例文件可能看起来像这样：

```yaml
apiVersion: v1
kind: Config
clusters:
- cluster:
    certificate-authority: /var/lib/kubernetes/ca.pem
    server: https://my.server.example.com:6443
  name: bootstrap
contexts:
- context:
    cluster: bootstrap
    user: kubelet-bootstrap
  name: bootstrap
current-context: bootstrap
preferences: {}
users:
- name: kubelet-bootstrap
  user:
    token: 07401b.f395accd246ae52d
```

<!--
The important elements to note are:

* `certificate-authority`: path to a CA file, used to validate the server certificate presented by kube-apiserver
* `server`: URL to kube-apiserver
* `token`: the token to use
-->
需要额外注意的一些因素有：

* `certificate-authority`：指向 CA 文件的路径，用来对 kube-apiserver 所出示
  的服务器证书进行验证
* `server`： 用来访问 kube-apiserver 的 URL
* `token`：要使用的令牌

<!--
The format of the token does not matter, as long as it matches what kube-apiserver expects. In the above example, we used a bootstrap token.
As stated earlier, _any_ valid authentication method can be used, not only tokens.

Because the bootstrap `kubeconfig` _is_ a standard `kubeconfig`, you can use `kubectl` to generate it. To create the above example file:
-->
令牌的格式并不重要，只要它与 kube-apiserver 的期望匹配即可。
在上面的例子中，我们使用的是启动引导令牌。
如前所述，任何合法的身份认证方法都可以使用，不限于令牌。

因为启动引导 `kubeconfig` 文件是一个标准的 `kubeconfig` 文件，你可以使用
`kubectl` 来生成该文件。要生成上面的示例文件：

```
kubectl config --kubeconfig=/var/lib/kubelet/bootstrap-kubeconfig set-cluster bootstrap --server='https://my.server.example.com:6443' --certificate-authority=/var/lib/kubernetes/ca.pem
kubectl config --kubeconfig=/var/lib/kubelet/bootstrap-kubeconfig set-credentials kubelet-bootstrap --token=07401b.f395accd246ae52d
kubectl config --kubeconfig=/var/lib/kubelet/bootstrap-kubeconfig set-context bootstrap --user=kubelet-bootstrap --cluster=bootstrap
kubectl config --kubeconfig=/var/lib/kubelet/bootstrap-kubeconfig use-context bootstrap
```

<!--
To indicate to the kubelet to use the bootstrap `kubeconfig`, use the following kubelet flag:
-->
要指示 kubelet 使用启动引导 `kubeconfig` 文件，可以使用下面的 kubelet 标志：

```
--bootstrap-kubeconfig="/var/lib/kubelet/bootstrap-kubeconfig" --kubeconfig="/var/lib/kubelet/kubeconfig"
```

<!--
When starting the kubelet, if the file specified via `--kubeconfig` does not
exist, the bootstrap kubeconfig specified via `--bootstrap-kubeconfig` is used
to request a client certificate from the API server. On approval of the
certificate request and receipt back by the kubelet, a kubeconfig file
referencing the generated key and obtained certificate is written to the path
specified by `--kubeconfig`. The certificate and key file will be placed in the
directory specified by `--cert-dir`.
-->
在启动 kubelet 时，如果 `--kubeconfig` 标志所指定的文件并不存在，会使用通过标志
`--bootstrap-kubeconfig` 所指定的启动引导 kubeconfig 配置来向 API 服务器请求
客户端证书。在证书请求被批复并被 kubelet 收回时，一个引用所生成的密钥和所获得
证书的 kubeconfig 文件会被写入到通过 `--kubeconfig` 所指定的文件路径下。
证书和密钥文件会被放到 `--cert-dir` 所指定的目录中。

<!--
### Client and Serving Certificates

All of the above relate to kubelet _client_ certificates, specifically, the certificates a kubelet
uses to authenticate to kube-apiserver.
-->
### 客户和服务证书   {#client-and-serving-certificates}

前文所述的内容都与 kubelet _客户端_ 证书相关，尤其是 kubelet 用来向
kube-apiserver 认证自身身份的证书。

<!--
A kubelet also can use _serving_ certificates. The kubelet itself exposes an https endpoint for certain features.
To secure these, the kubelet can do one of:

* use provided key and certificate, via the `--tls-private-key-file` and `--tls-cert-file` flags
* create self-signed key and certificate, if a key and certificate are not provided
* request serving certificates from the cluster server, via the CSR API
-->
kubelet 也可以使用 _服务（Serving）_ 证书。kubelet 自身向外提供一个
HTTPS 末端，包含若干功能特性。要保证这些末端的安全性，kubelet 可以执行以下操作
之一：

* 使用通过 `--tls-private-key-file` 和 `--tls-cert-file` 所设置的密钥和证书
* 如果没有提供密钥和证书，则创建自签名的密钥和证书
* 通过 CSR API 从集群服务器请求服务证书

<!--
The client certificate provided by TLS bootstrapping is signed, by default, for `client auth` only, and thus cannot
be used as serving certificates, or `server auth`.

However, you _can_ enable its server certificate, at least partially, via certificate rotation.
-->
TLS 启动引导所提供的客户端证书默认被签名为仅用于 `client auth`（客户端认证），
因此不能作为提供服务的证书，或者 `server auth`。

不过，你可以启用服务器证书，至少可以部分地通过证书轮换来实现这点。

<!--
### Certificate Rotation

Kubernetes v1.8 and higher kubelet implements __beta__ features for enabling
rotation of its client and/or serving certificates.  These can be enabled through
the respective `RotateKubeletClientCertificate` and
`RotateKubeletServerCertificate` feature flags on the kubelet and are enabled by
default.
-->
### 证书轮换    {#certificate-rotation}

Kubernetes v1.8 和更高版本的 kubelet 实现了对客户端证书与/或服务证书进行轮换
这一 Beta 特性。这一特性通过 kubelet 对应的 `RotateKubeletClientCertificate` 和
`RotateKubeletServerCertificate` 特性门控标志来控制，并且是默认启用的。

<!--
`RotateKubeletClientCertificate` causes the kubelet to rotate its client
certificates by creating new CSRs as its existing credentials expire. To enable
this feature pass the following flag to the kubelet:
-->
`RotateKubeletClientCertificate` 会导致 kubelet 在其现有凭据即将过期时通过
创建新的 CSR 来轮换其客户端证书。要启用此功能特性，可将下面的标志传递给
kubelet：

```
--rotate-certificates
```

<!--
`RotateKubeletServerCertificate` causes the kubelet **both** to request a serving
certificate after bootstrapping its client credentials **and** to rotate that
certificate. To enable this feature pass the following flag to the kubelet:
-->
`RotateKubeletServerCertificate` 会让 kubelet 在启动引导其客户端凭据之后请求
一个服务证书 **且** 对该服务证书执行轮换操作。要启用此功能特性，将下面的标志
传递给 kubelet：

```
--rotate-server-certificates
```

{{< note >}}
<!--
The CSR approving controllers implemented in core Kubernetes do not
approve node _serving_ certificates for [security
reasons](https://github.com/kubernetes/community/pull/1982). To use
`RotateKubeletServerCertificate` operators need to run a custom approving
controller, or manually approve the serving certificate requests.
-->
Kubernetes 核心中所实现的 CSR 批复控制器出于
[安全原因](https://github.com/kubernetes/community/pull/1982)
并不会自动批复节点的 _服务_ 证书。
要使用 `RotateKubeletServerCertificate` 功能特性，集群运维人员需要运行一个
定制的控制器或者手动批复服务证书的请求。

<!--
A deployment-specific approval process for kubelet serving certificates should typically only approve CSRs which:

1. are requested by nodes (ensure the `spec.username` field is of the form 
   `system:node:<nodeName>` and `spec.groups` contains `system:nodes`) 
2. request usages for a serving certificate (ensure `spec.usages` contains `server auth`, 
   optionally contains `digital signature` and `key encipherment`, and contains no other usages)
3. only have IP and DNS subjectAltNames that belong to the requesting node, 
   and have no URI and Email subjectAltNames (parse the x509 Certificate Signing Request 
   in `spec.request` to verify `subjectAltNames`)
-->
对 kubelet 服务证书的批复过程因集群部署而异，通常应该仅批复如下 CSR：

1. 由节点发出的请求（确保 `spec.username` 字段形式为 `system:node:<nodeName>`
   且 `spec.groups` 包含 `system:nodes`）
2. 请求中包含服务证书用法（确保 `spec.usages` 中包含 `server auth`，可选地也可 
   包含 `digital signature` 和 `key encipherment`，且不包含其它用法）
3. 仅包含隶属于请求节点的 IP 和 DNS 的 `subjectAltNames`，没有 URI 和 Email
   形式的 `subjectAltNames`（解析 `spec.request` 中的 x509 证书签名请求可以
   检查 `subjectAltNames`）
{{< /note >}}

<!--
## Other authenticating components

All of TLS bootstrapping described in this document relates to the kubelet. However,
other components may need to communicate directly with kube-apiserver. Notable is kube-proxy, which
is part of the Kubernetes control plane and runs on every node, but may also include other components such as monitoring or networking.
-->
## 其它身份认证组件   {#other-authenticating-components}

本文所描述的所有 TLS 启动引导内容都与 kubelet 相关。不过，其它组件也可能需要
直接与 kube-apiserver 直接通信。容易想到的是 kube-proxy，同样隶属于
Kubernetes 的控制面并且运行在所有节点之上，不过也可能包含一些其它负责
监控或者联网的组件。

<!--
Like the kubelet, these other components also require a method of authenticating to kube-apiserver.
You have several options for generating these credentials:
-->
与 kubelet 类似，这些其它组件也需要一种向 kube-apiserver 认证身份的方法。
你可以用几种方法来生成这类凭据：

<!--
* The old way: Create and distribute certificates the same way you did for kubelet before TLS bootstrapping
* DaemonSet: Since the kubelet itself is loaded on each node, and is sufficient to start base services, you can run kube-proxy and other node-specific services not as a standalone process, but rather as a daemonset in the `kube-system` namespace. Since it will be in-cluster, you can give it a proper service account with appropriate permissions to perform its activities. This may be the simplest way to configure such services.
-->
* 较老的方式：和 kubelet 在 TLS 启动引导之前所做的一样，用类似的方式
  创建和分发证书
* DaemonSet：由于 kubelet 自身被加载到所有节点之上，并且有足够能力来启动基本服务，
  你可以运行将 kube-proxy 和其它特定节点的服务作为 `kube-system` 名字空间中的
  DaemonSet 来执行，而不是独立的进程。由于 DaemonSet 位于集群内部，你可以为其
  指派一个合适的服务账户，使之具有适当的访问权限来完成其使命。这也许是配置此类
  服务的最简单的方法。

<!--
## kubectl approval

CSRs can be approved outside of the approval flows builtin to the controller
manager.
-->
## kubectl 批复    {#kubectl-approval}

CSRs 可以在控制器管理其内置的批复工作流之外被批复。

<!--
The signing controller does not immediately sign all certificate requests.
Instead, it waits until they have been flagged with an "Approved" status by an
appropriately-privileged user. This flow is intended to allow for automated
approval handled by an external approval controller or the approval controller
implemented in the core controller-manager. However cluster administrators can
also manually approve certificate requests using kubectl. An administrator can
list CSRs with `kubectl get csr` and describe one in detail with `kubectl
describe csr <name>`. An administrator can approve or deny a CSR with `kubectl
certificate approve <name>` and `kubectl certificate deny <name>`.
-->
签名控制器并不会立即对所有证书请求执行签名操作。相反，它会等待这些请求被某
具有适当特权的用户标记为 “Approved（已批准）”状态。
这一流程有意允许由外部批复控制器来自动执行的批复，或者由控制器管理器内置的
批复控制器来自动批复。
不过，集群管理员也可以使用 `kubectl` 来手动批准证书请求。
管理员可以通过 `kubectl get csr` 来列举所有的 CSR，使用
`kubectl descsribe csr <name>` 来描述某个 CSR 的细节。
管理员可以使用 `kubectl certificate approve <name` 来批准某 CSR，或者
`kubectl certificate deny <name>` 来拒绝某 CSR。

