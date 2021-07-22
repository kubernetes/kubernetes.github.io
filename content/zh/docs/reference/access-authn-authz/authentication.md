---
title: 用户认证
content_type: concept
weight: 10
---
<!--
reviewers:
- erictune
- lavalamp
- ericchiang
- deads2k
- liggitt
title: Authenticating
content_type: concept
weight: 10
-->

<!-- overview -->
<!--
This page provides an overview of authenticating.
-->
本页提供身份认证有关的概述。

<!-- body -->
<!--
## Users in Kubernetes

All Kubernetes clusters have two categories of users: service accounts managed
by Kubernetes, and normal users.

It is assumed that a cluster-independent service manages normal users in the following ways:

- an administrator distributing private keys
- a user store like Keystone or Google Accounts
- a file with a list of usernames and passwords

In this regard, _Kubernetes does not have objects which represent normal user
accounts._ Normal users cannot be added to a cluster through an API call.
-->
## Kubernetes 中的用户  {#users-in-kubernetes}

所有 Kubernetes 集群都有两类用户：由 Kubernetes 管理的服务账号和普通用户。

Kubernetes 假定普通用户是由一个与集群无关的服务通过以下方式之一进行管理的：

- 负责分发私钥的管理员
- 类似 Keystone 或者 Google Accounts 这类用户数据库
- 包含用户名和密码列表的文件

有鉴于此，_Kubernetes 并不包含用来代表普通用户账号的对象_。
普通用户的信息无法通过 API 调用添加到集群中。

<!--
Even though normal user cannot be added via an API call, but any user that
presents a valid certificate signed by the cluster’s certificate authority
(CA) is considered authenticated. In this configuration, Kubernetes determines
the username from the common name field in the ‘subject’ of the cert (e.g.,
“/CN=bob”). From there, the role based access control (RBAC) sub-system would
determine whether the user is authorized to perform a specific operation on a
resource. For more details, refer to the normal users topic in
[certificate request](/docs/reference/access-authn-authz/certificate-signing-requests/#normal-user)
for more details about this.
-->
尽管无法通过 API 调用来添加普通用户，Kubernetes 仍然认为能够提供由集群的证书
机构签名的合法证书的用户是通过身份认证的用户。基于这样的配置，Kubernetes
使用证书中的 'subject' 的通用名称（Common Name）字段（例如，"/CN=bob"）来
确定用户名。接下来，基于角色访问控制（RBAC）子系统会确定用户是否有权针对
某资源执行特定的操作。进一步的细节可参阅
[证书请求](/zh/docs/reference/access-authn-authz/certificate-signing-requests/#normal-user)
下普通用户主题。

<!--
In contrast, service accounts are users managed by the Kubernetes API. They are
bound to specific namespaces, and created automatically by the API server or
manually through API calls. Service accounts are tied to a set of credentials
stored as `Secrets`, which are mounted into pods allowing in-cluster processes
to talk to the Kubernetes API.

API requests are tied to either a normal user or a service account, or are treated
as [anonymous requests](#anonymous-requests). This means every process inside or outside the cluster, from
a human user typing `kubectl` on a workstation, to `kubelets` on nodes, to members
of the control plane, must authenticate when making requests to the API server,
or be treated as an anonymous user.
-->
与此不同，服务账号是 Kubernetes API 所管理的用户。它们被绑定到特定的名字空间，
或者由 API 服务器自动创建，或者通过 API 调用创建。服务账号与一组以 Secret 保存
的凭据相关，这些凭据会被挂载到 Pod 中，从而允许集群内的进程访问 Kubernetes
API。

API 请求则或者与某普通用户相关联，或者与某服务账号相关联，亦或者被视作
[匿名请求](#anonymous-requests)。这意味着集群内外的每个进程在向 API 服务器发起
请求时都必须通过身份认证，否则会被视作匿名用户。这里的进程可以是在某工作站上
输入 `kubectl` 命令的操作人员，也可以是节点上的 `kubelet` 组件，还可以是控制面
的成员。

<!--
## Authentication strategies

Kubernetes uses client certificates, bearer tokens, an authenticating proxy, or HTTP basic auth to
authenticate API requests through authentication plugins. As HTTP requests are
made to the API server, plugins attempt to associate the following attributes
with the request:
-->
## 身份认证策略  {#authentication-strategies}

Kubernetes 使用身份认证插件利用客户端证书、持有者令牌（Bearer Token）、身份认证代理（Proxy）
或者 HTTP 基本认证机制来认证 API 请求的身份。HTTP 请求发给 API 服务器时，
插件会将以下属性关联到请求本身：

<!--
* Username: a string which identifies the end user. Common values might be `kube-admin` or `jane@example.com`.
* UID: a string which identifies the end user and attempts to be more consistent and unique than username.
* Groups: a set of strings, each of which indicates the user's membership in a named logical collection of users. Common values might be `system:masters` or `devops-team`.
* Extra fields: a map of strings to list of strings which holds additional information authorizers may find useful.
-->
* 用户名：用来辩识最终用户的字符串。常见的值可以是 `kube-admin` 或 `jane@example.com`。
* 用户 ID：用来辩识最终用户的字符串，旨在比用户名有更好的一致性和唯一性。
* 用户组：取值为一组字符串，其中各个字符串用来标明用户是某个命名的用户逻辑集合的成员。
  常见的值可能是 `system:masters` 或者 `devops-team` 等。
* 附加字段：一组额外的键-值映射，键是字符串，值是一组字符串；用来保存一些鉴权组件可能
  觉得有用的额外信息。

<!--
All values are opaque to the authentication system and only hold significance
when interpreted by an [authorizer](/docs/reference/access-authn-authz/authorization/).

You can enable multiple authentication methods at once. You should usually use at least two methods:

 - service account tokens for service accounts
 - at least one other method for user authentication.
-->
所有（属性）值对于身份认证系统而言都是不透明的，只有被
[鉴权组件](/zh/docs/reference/access-authn-authz/authorization/)
解释过之后才有意义。

你可以同时启用多种身份认证方法，并且你通常会至少使用两种方法：

- 针对服务账号使用服务账号令牌
- 至少另外一种方法对用户的身份进行认证

<!--
When multiple authenticator modules are enabled, the first module
to successfully authenticate the request short-circuits evaluation.
The API server does not guarantee the order authenticators run in.

The `system:authenticated` group is included in the list of groups for all authenticated users.

Integrations with other authentication protocols (LDAP, SAML, Kerberos, alternate x509 schemes, etc)
can be accomplished using an [authenticating proxy](#authenticating-proxy) or the
[authentication webhook](#webhook-token-authentication).
-->
当集群中启用了多个身份认证模块时，第一个成功地对请求完成身份认证的模块会
直接做出评估决定。API 服务器并不保证身份认证模块的运行顺序。

对于所有通过身份认证的用户，`system:authenticated` 组都会被添加到其组列表中。

与其它身份认证协议（LDAP、SAML、Kerberos、X509 的替代模式等等）都可以通过
使用一个[身份认证代理](#authenticating-proxy)或
[身份认证 Webhoook](#webhook-token-authentication)来实现。

<!--
### X509 Client Certs

Client certificate authentication is enabled by passing the `-client-ca-file=SOMEFILE`
option to API server. The referenced file must contain one or more certificate authorities
to use to validate client certificates presented to the API server. If a client certificate
is presented and verified, the common name of the subject is used as the user name for the
request. As of Kubernetes 1.4, client certificates can also indicate a user's group memberships
using the certificate's organization fields. To include multiple group memberships for a user,
include multiple organization fields in the certificate.

For example, using the `openssl` command line tool to generate a certificate signing request:
-->
### X509 客户证书   {#x509-client-certs}

通过给 API 服务器传递 `--client-ca-file=SOMEFILE` 选项，就可以启动客户端证书身份认证。
所引用的文件必须包含一个或者多个证书机构，用来验证向 API 服务器提供的客户端证书。
如果提供了客户端证书并且证书被验证通过，则 subject 中的公共名称（Common Name）就被
作为请求的用户名。
自 Kubernetes 1.4 开始，客户端证书还可以通过证书的 organization 字段标明用户的组成员信息。
要包含用户的多个组成员信息，可以在证书中包含多个 organization 字段。

例如，使用 `openssl` 命令行工具生成一个证书签名请求：

```bash
openssl req -new -key jbeda.pem -out jbeda-csr.pem -subj "/CN=jbeda/O=app1/O=app2"
```

<!--
This would create a CSR for the username "jbeda", belonging to two groups, "app1" and "app2".

See [Managing Certificates](/docs/concepts/cluster-administration/certificates/) for how to generate a client cert.
-->
此命令将使用用户名 `jbeda` 生成一个证书签名请求（CSR），且该用户属于 "app" 和
"app2" 两个用户组。

参阅[管理证书](/zh/docs/concepts/cluster-administration/certificates/)了解如何生成客户端证书。

<!--
### Static Token File

The API server reads bearer tokens from a file when given the `-token-auth-file=SOMEFILE` option on the command line.  Currently, tokens last indefinitely, and the token list cannot be
changed without restarting API server.

The token file is a csv file with a minimum of 3 columns: token, user name, user uid,
followed by optional group names.
-->
### 静态令牌文件  {#static-token-file}

当 API 服务器的命令行设置了 `--token-auth-file=SOMEFILE` 选项时，会从文件中
读取持有者令牌。目前，令牌会长期有效，并且在不重启 API 服务器的情况下
无法更改令牌列表。

令牌文件是一个 CSV 文件，包含至少 3 个列：令牌、用户名和用户的 UID。
其余列被视为可选的组名。

<!--
If you have more than one group the column must be double quoted e.g.

```conf
token,user,uid,"group1,group2,group3"
```
-->
{{< note >}}
如果要设置的组名不止一个，则对应的列必须用双引号括起来，例如

```conf
token,user,uid,"group1,group2,group3"
```
{{< /note >}}

<!--
#### Putting a Bearer Token in a Request

When using bearer token authentication from an http client, the API
server expects an `Authorization` header with a value of `Bearer
THETOKEN`.  The bearer token must be a character sequence that can be
put in an HTTP header value using no more than the encoding and
quoting facilities of HTTP.  For example: if the bearer token is
`31ada4fd-adec-460c-809a-9e56ceb75269` then it would appear in an HTTP
header as shown below.
-->
#### 在请求中放入持有者令牌   {#putting-a-bearer-token-in-a-request}

当使用持有者令牌来对某 HTTP 客户端执行身份认证时，API 服务器希望看到
一个名为 `Authorization` 的 HTTP 头，其值格式为 `Bearer THETOKEN`。
持有者令牌必须是一个可以放入 HTTP 头部值字段的字符序列，至多可使用
HTTP 的编码和引用机制。
例如：如果持有者令牌为 `31ada4fd-adec-460c-809a-9e56ceb75269`，则其
出现在 HTTP 头部时如下所示：

```http
Authorization: Bearer 31ada4fd-adec-460c-809a-9e56ceb75269
```

<!--
### Bootstrap Tokens
-->
### 启动引导令牌    {#bootstrap-tokens}

{{< feature-state for_k8s_version="v1.18" state="stable" >}}

<!--
To allow for streamlined bootstrapping for new clusters, Kubernetes includes a
dynamically-managed Bearer token type called a *Bootstrap Token*. These tokens
are stored as Secrets in the `kube-system` namespace, where they can be
dynamically managed and created. Controller Manager contains a TokenCleaner
controller that deletes bootstrap tokens as they expire.
-->
为了支持平滑地启动引导新的集群，Kubernetes 包含了一种动态管理的持有者令牌类型，
称作 *启动引导令牌（Bootstrap Token）*。
这些令牌以 Secret 的形式保存在 `kube-system` 名字空间中，可以被动态管理和创建。
控制器管理器包含的 `TokenCleaner` 控制器能够在启动引导令牌过期时将其删除。

<!--
The tokens are of the form `[a-z0-9]{6}.[a-z0-9]{16}`.  The first component is a
Token ID and the second component is the Token Secret.  You specify the token
in an HTTP header as follows:
-->
这些令牌的格式为 `[a-z0-9]{6}.[a-z0-9]{16}`。第一个部分是令牌的 ID；第二个部分
是令牌的 Secret。你可以用如下所示的方式来在 HTTP 头部设置令牌：

```http
Authorization: Bearer 781292.db7bc3a58fc5f07e
```

<!--
You must enable the Bootstrap Token Authenticator with the
`-enable-bootstrap-token-auth` flag on the API Server.  You must enable
the TokenCleaner controller via the `-controllers` flag on the Controller
Manager.  This is done with something like `-controllers=*,tokencleaner`.
`kubeadm` will do this for you if you are using it to bootstrap a cluster.
-->
你必须在 API 服务器上设置 `--enable-bootstrap-token-auth` 标志来启用基于启动
引导令牌的身份认证组件。
你必须通过控制器管理器的 `--controllers` 标志来启用 TokenCleaner 控制器；
这可以通过类似 `--controllers=*,tokencleaner` 这种设置来做到。
如果你使用 `kubeadm` 来启动引导新的集群，该工具会帮你完成这些设置。

<!--
The authenticator authenticates as `system:bootstrap:<Token ID>`.  It is
included in the `system:bootstrappers` group.  The naming and groups are
intentionally limited to discourage users from using these tokens past
bootstrapping.  The user names and group can be used (and are used by `kubeadm`)
to craft the appropriate authorization policies to support bootstrapping a
cluster.
-->
身份认证组件的认证结果为 `system:bootstrap:<令牌 ID>`，该用户属于
`system:bootstrappers` 用户组。
这里的用户名和组设置都是有意设计成这样，其目的是阻止用户在启动引导集群之后
继续使用这些令牌。
这里的用户名和组名可以用来（并且已经被 `kubeadm` 用来）构造合适的鉴权
策略，以完成启动引导新集群的工作。

<!--
Please see [Bootstrap Tokens](/docs/reference/access-authn-authz/bootstrap-tokens/) for in depth
documentation on the Bootstrap Token authenticator and controllers along with
how to manage these tokens with `kubeadm`.
-->
请参阅[启动引导令牌](/zh/docs/reference/access-authn-authz/bootstrap-tokens/)
以了解关于启动引导令牌身份认证组件与控制器的更深入的信息，以及如何使用
`kubeadm` 来管理这些令牌。

<!--
### Service Account Tokens

A service account is an automatically enabled authenticator that uses signed
bearer tokens to verify requests. The plugin takes two optional flags:

* `--service-account-key-file` A file containing a PEM encoded key for signing bearer tokens.
If unspecified, the API server's TLS private key will be used.
* `--service-account-lookup` If enabled, tokens which are deleted from the API will be revoked.
-->
### 服务账号令牌   {#service-account-tokens}

服务账号（Service Account）是一种自动被启用的用户认证机制，使用经过签名的
持有者令牌来验证请求。该插件可接受两个可选参数：

* `--service-account-key-file` 一个包含用来为持有者令牌签名的 PEM 编码密钥。
  若未指定，则使用 API 服务器的 TLS 私钥。
* `--service-account-lookup` 如果启用，则从 API 删除的令牌会被回收。

<!--
Service accounts are usually created automatically by the API server and
associated with pods running in the cluster through the `ServiceAccount`
[Admission Controller](/docs/reference/access-authn-authz/admission-controllers/). Bearer tokens are
mounted into pods at well-known locations, and allow in-cluster processes to
talk to the API server. Accounts may be explicitly associated with pods using the
`serviceAccountName` field of a `PodSpec`.
-->
服务账号通常由 API 服务器自动创建并通过 `ServiceAccount`
[准入控制器](/zh/docs/reference/access-authn-authz/admission-controllers/)
关联到集群中运行的 Pod 上。
持有者令牌会挂载到 Pod 中可预知的位置，允许集群内进程与 API 服务器通信。
服务账号也可以使用 Pod 规约的 `serviceAccountName` 字段显式地关联到 Pod 上。

<!--
`serviceAccountName` is usually omitted because this is done automatically.
-->
{{< note >}}
`serviceAccountName` 通常会被忽略，因为关联关系是自动建立的。
{{< /note >}}

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  namespace: default
spec:
  replicas: 3
  template:
    metadata:
    # ...
    spec:
      serviceAccountName: bob-the-bot
      containers:
      - name: nginx
        image: nginx:1.14.2
```

<!--
Service account bearer tokens are perfectly valid to use outside the cluster and
can be used to create identities for long standing jobs that wish to talk to the
Kubernetes API. To manually create a service account, simply use the `kubectl
create serviceaccount (NAME)` command. This creates a service account in the
current namespace and an associated secret.
-->
在集群外部使用服务账号持有者令牌也是完全合法的，且可用来为长时间运行的、需要与
Kubernetes  API 服务器通信的任务创建标识。要手动创建服务账号，可以使用
`kubectl create serviceaccount <名称>` 命令。此命令会在当前的名字空间中生成一个
服务账号和一个与之关联的 Secret。

```bash
kubectl create serviceaccount jenkins
```

```
serviceaccount/jenkins created
```

<!--
Check an associated secret:
-->
查验相关联的 Secret：

```bash
kubectl get serviceaccounts jenkins -o yaml
```

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  # ...
secrets:
- name: jenkins-token-1yvwg
```

<!--
The created secret holds the public CA of the API server and a signed JSON Web
Token (JWT).
-->
所创建的 Secret 中会保存 API 服务器的公开的 CA 证书和一个已签名的 JSON Web
令牌（JWT）。

```bash
kubectl get secret jenkins-token-1yvwg -o yaml
```

<!--
```yaml
apiVersion: v1
data:
  ca.crt: (APISERVER'S CA BASE64 ENCODED)
  namespace: ZGVmYXVsdA==
  token: (BEARER TOKEN BASE64 ENCODED)
kind: Secret
metadata:
  # ...
type: kubernetes.io/service-account-token
```
-->
```yaml
apiVersion: v1
data:
  ca.crt: <Base64 编码的 API 服务器 CA>
  namespace: ZGVmYXVsdA==
  token: <Base64 编码的持有者令牌>
kind: Secret
metadata:
  # ...
type: kubernetes.io/service-account-token
```

<!--
Values are base64 encoded because secrets are always base64 encoded.
-->
{{< note >}}
字段值是按 Base64 编码的，这是因为 Secret 数据总是采用 Base64 编码来存储。
{{< /note >}}

<!--
The signed JWT can be used as a bearer token to authenticate as the given service
account. See [above](#putting-a-bearer-token-in-a-request) for how the token is included
in a request.  Normally these secrets are mounted into pods for in-cluster access to
the API server, but can be used from outside the cluster as well.
-->
已签名的 JWT 可以用作持有者令牌，并将被认证为所给的服务账号。
关于如何在请求中包含令牌，请参阅[前文](#putting-a-bearer-token-in-a-request)。
通常，这些 Secret 数据会被挂载到 Pod 中以便集群内访问 API 服务器时使用，
不过也可以在集群外部使用。

<!--
Service accounts authenticate with the username `system:serviceaccount:(NAMESPACE):(SERVICEACCOUNT)`,
and are assigned to the groups `system:serviceaccounts` and `system:serviceaccounts:(NAMESPACE)`.

WARNING: Because service account tokens are stored in secrets, any user with
read access to those secrets can authenticate as the service account. Be cautious
when granting permissions to service accounts and read capabilities for secrets.
-->
服务账号被身份认证后，所确定的用户名为 `system:serviceaccount:<名字空间>:<服务账号>`，
并被分配到用户组 `system:serviceaccounts` 和 `system:serviceaccounts:<名字空间>`。

警告：由于服务账号令牌保存在 Secret 对象中，任何能够读取这些 Secret 的用户
都可以被认证为对应的服务账号。在为用户授予访问服务账号的权限时，以及对 Secret
的读权限时，要格外小心。

<!--
### OpenID Connect Tokens

[OpenID Connect](https://openid.net/connect/) is a flavor of OAuth2 supported by
some OAuth2 providers, notably Azure Active Directory, Salesforce, and Google.
The protocol's main extension of OAuth2 is an additional field returned with
the access token called an [ID Token](https://openid.net/specs/openid-connect-core-1_0.html#IDToken).
This token is a JSON Web Token (JWT) with well known fields, such as a user's
email, signed by the server.
-->
### OpenID Connect（OIDC）令牌   {#openid-connect-tokens}

[OpenID Connect](https://openid.net/connect/) 是一种 OAuth2  认证方式，
被某些 OAuth2 提供者支持，例如 Azure 活动目录、Salesforce 和 Google。
协议对 OAuth2 的主要扩充体现在有一个附加字段会和访问令牌一起返回，
这一字段称作 [ID Token（ID 令牌）](https://openid.net/specs/openid-connect-core-1_0.html#IDToken)。
ID 令牌是一种由服务器签名的 JSON Web 令牌（JWT），其中包含一些可预知的字段，
例如用户的邮箱地址，

<!--
To identify the user, the authenticator uses the `id_token` (not the `access_token`)
from the OAuth2 [token response](https://openid.net/specs/openid-connect-core-1_0.html#TokenResponse)
as a bearer token.  See [above](#putting-a-bearer-token-in-a-request) for how the token
is included in a request.
-->
要识别用户，身份认证组件使用 OAuth2
[令牌响应](https://openid.net/specs/openid-connect-core-1_0.html#TokenResponse)
中的 `id_token`（而非 `access_token`）作为持有者令牌。
关于如何在请求中设置令牌，可参见[前文](#putting-a-bearer-token-in-a-request)。

{{< mermaid >}}
sequenceDiagram
    participant user as 用户
    participant idp as 身份提供者 
    participant kube as Kubectl
    participant api as API 服务器

    user ->> idp: 1. 登录到 IdP
    activate idp
    idp -->> user: 2. 提供 access_token,<br>id_token, 和 refresh_token
    deactivate idp
    activate user
    user ->> kube: 3. 调用 Kubectl 并<br>设置 --token 为 id_token<br>或者将令牌添加到 .kube/config
    deactivate user
    activate kube
    kube ->> api: 4. Authorization: Bearer...
    deactivate kube
    activate api
    api ->> api: 5. JWT 签名合法么？
    api ->> api: 6. JWT 是否已过期？(iat+exp)
    api ->> api: 7. 用户被授权了么？
    api -->> kube: 8. 已授权：执行<br>操作并返回结果
    deactivate api
    activate kube
    kube --x user: 9. 返回结果
    deactivate kube
{{< /mermaid >}}

<!--
1.  Login to your identity provider
2.  Your identity provider will provide you with an `access_token`, `id_token` and a `refresh_token`
3.  When using `kubectl`, use your `id_token` with the `-token` flag or add it directly to your `kubeconfig`
4.  `kubectl` sends your `id_token` in a header called Authorization to the API server
5.  The API server will make sure the JWT signature is valid by checking against the certificate named in the configuration
6.  Check to make sure the `id_token` hasn't expired
7.  Make sure the user is authorized
8.  Once authorized the API server returns a response to `kubectl`
9.  `kubectl` provides feedback to the user
-->
1.  登录到你的身份服务（Identity Provider）
2.  你的身份服务将为你提供 `access_token`、`id_token` 和 `refresh_token`
3.  在使用 `kubectl` 时，将 `id_token` 设置为 `--token` 标志值，或者将其直接添加到
    `kubeconfig` 中
4.  `kubectl` 将你的 `id_token` 放到一个称作 `Authorization` 的头部，发送给 API 服务器
5.  API 服务器将负责通过检查配置中引用的证书来确认 JWT 的签名是合法的
6.  检查确认 `id_token` 尚未过期
7.  确认用户有权限执行操作
8.  鉴权成功之后，API 服务器向 `kubectl` 返回响应
9.  `kubectl` 向用户提供反馈信息

<!--
Since all of the data needed to validate who you are is in the `id_token`, Kubernetes doesn't need to
"phone home" to the identity provider.  In a model where every request is stateless this provides a very scalable
solution for authentication.  It does offer a few challenges:
-->
由于用来验证你是谁的所有数据都在 `id_token` 中，Kubernetes 不需要再去联系
身份服务。在一个所有请求都是无状态请求的模型中，这一工作方式可以使得身份认证
的解决方案更容易处理大规模请求。不过，此访问也有一些挑战：

<!--
1.  Kubernetes has no "web interface" to trigger the authentication process.  There is no browser or interface to collect credentials which is why you need to authenticate to your identity provider first.
2.  The `id_token` can't be revoked, it's like a certificate so it should be short-lived (only a few minutes) so it can be very annoying to have to get a new token every few minutes.
3.  There's no easy way to authenticate to the Kubernetes dashboard without using the `kubectl proxy` command or a reverse proxy that injects the `id_token`.
-->
1.  Kubernetes 没有提供用来触发身份认证过程的 "Web 界面"。
    因为不存在用来收集用户凭据的浏览器或用户接口，你必须自己先行完成
    对身份服务的认证过程。
2.  `id_token` 令牌不可收回。因其属性类似于证书，其生命期一般很短（只有几分钟），
    所以，每隔几分钟就要获得一个新的令牌这件事可能很让人头疼。
3.  如果不使用 `kubectl proxy` 命令或者一个能够注入 `id_token` 的反向代理，
    向 Kubernetes 控制面板执行身份认证是很困难的。

<!--
#### Configuring the API Server

To enable the plugin, configure the following flags on the API server:
-->
#### 配置 API 服务器    {#configuring-the-api-server}

要启用此插件，须在 API 服务器上配置以下标志：

<!--
| Parameter | Description | Example | Required |
| --------- | ----------- | ------- | ------- |
| `--oidc-issuer-url` | URL of the provider which allows the API server to discover public signing keys. Only URLs which use the `https://` scheme are accepted.  This is typically the provider's discovery URL without a path, for example "https://accounts.google.com" or "https://login.salesforce.com".  This URL should point to the level below .well-known/openid-configuration | If the discovery URL is `https://accounts.google.com/.well-known/openid-configuration`, the value should be `https://accounts.google.com` | Yes |
| `--oidc-client-id` |  A client id that all tokens must be issued for. | kubernetes | Yes |
| `--oidc-username-claim` | JWT claim to use as the user name. By default `sub`, which is expected to be a unique identifier of the end user. Admins can choose other claims, such as `email` or `name`, depending on their provider. However, claims other than `email` will be prefixed with the issuer URL to prevent naming clashes with other plugins. | sub | No |
| `--oidc-username-prefix` | Prefix prepended to username claims to prevent clashes with existing names (such as `system:` users). For example, the value `oidc:` will create usernames like `oidc:jane.doe`. If this flag isn't provided and `--oidc-username-claim` is a value other than `email` the prefix defaults to `( Issuer URL )#` where `( Issuer URL )` is the value of `--oidc-issuer-url`. The value `-` can be used to disable all prefixing. | `oidc:` | No |
| `--oidc-groups-claim` | JWT claim to use as the user's group. If the claim is present it must be an array of strings. | groups | No |
| `--oidc-groups-prefix` | Prefix prepended to group claims to prevent clashes with existing names (such as `system:` groups). For example, the value `oidc:` will create group names like `oidc:engineering` and `oidc:infra`. | `oidc:` | No |
| `--oidc-required-claim` | A key=value pair that describes a required claim in the ID Token. If set, the claim is verified to be present in the ID Token with a matching value. Repeat this flag to specify multiple claims. | `claim=value` | No |
| `--oidc-ca-file` | The path to the certificate for the CA that signed your identity provider's web certificate.  Defaults to the host's root CAs. | `/etc/kubernetes/ssl/kc-ca.pem` | No |
-->

| 参数 | 描述 | 示例 | 必需？ |
| --------- | ----------- | ------- | ------- |
| `--oidc-issuer-url` | 允许 API 服务器发现公开的签名密钥的服务的 URL。只接受模式为 `https://` 的 URL。此值通常设置为服务的发现 URL，不含路径。例如："https://accounts.google.com" 或 "https://login.salesforce.com"。此 URL 应指向 .well-known/openid-configuration 下一层的路径。 | 如果发现 URL 是 `https://accounts.google.com/.well-known/openid-configuration`，则此值应为 `https://accounts.google.com` | 是 |
| `--oidc-client-id` |  所有令牌都应发放给此客户 ID。 | kubernetes | 是 |
| `--oidc-username-claim` | 用作用户名的 JWT 申领（JWT Claim）。默认情况下使用 `sub` 值，即最终用户的一个唯一的标识符。管理员也可以选择其他申领，例如 `email` 或者 `name`，取决于所用的身份服务。不过，除了 `email` 之外的申领都会被添加令牌发放者的 URL 作为前缀，以免与其他插件产生命名冲突。 | sub | 否 |
| `--oidc-username-prefix` | 要添加到用户名申领之前的前缀，用来避免与现有用户名发生冲突（例如：`system:` 用户）。例如，此标志值为 `oidc:` 时将创建形如 `oidc:jane.doe` 的用户名。如果此标志未设置，且 `--oidc-username-claim` 标志值不是 `email`，则默认前缀为 `<令牌发放者的 URL>#`，其中 `<令牌发放者 URL >` 的值取自 `--oidc-issuer-url` 标志的设定。此标志值为 `-` 时，意味着禁止添加用户名前缀。 | `oidc:` | 否 |
| `--oidc-groups-claim` | 用作用户组名的 JWT 申领。如果所指定的申领确实存在，则其值必须是一个字符串数组。 | groups | 否 |
| `--oidc-groups-prefix` | 添加到组申领的前缀，用来避免与现有用户组名（如：`system:` 组）发生冲突。例如，此标志值为 `oidc:` 时，所得到的用户组名形如 `oidc:engineering` 和 `oidc:infra`。 | `oidc:` | 否 |
| `--oidc-required-claim` | 取值为一个 key=value 偶对，意为 ID 令牌中必须存在的申领。如果设置了此标志，则 ID 令牌会被检查以确定是否包含取值匹配的申领。此标志可多次重复，以指定多个申领。 | `claim=value` | 否 |
| `--oidc-ca-file` | 指向一个 CA 证书的路径，该 CA 负责对你的身份服务的 Web 证书提供签名。默认值为宿主系统的根 CA。 | `/etc/kubernetes/ssl/kc-ca.pem` | 否 |

<!--
Importantly, the API server is not an OAuth2 client, rather it can only be
configured to trust a single issuer. This allows the use of public providers,
such as Google, without trusting credentials issued to third parties. Admins who
wish to utilize multiple OAuth clients should explore providers which support the
`azp` (authorized party) claim, a mechanism for allowing one client to issue
tokens on behalf of another.
-->
很重要的一点是，API 服务器并非一个 OAuth2 客户端，相反，它只能被配置为
信任某一个令牌发放者。这使得使用公共服务（如 Google）的用户可以不信任发放给
第三方的凭据。
如果管理员希望使用多个 OAuth 客户端，他们应该研究一下那些支持 `azp`
（Authorized Party，被授权方）申领的服务。
`azp` 是一种允许某客户端代替另一客户端发放令牌的机制。

<!--
Kubernetes does not provide an OpenID Connect Identity Provider.
You can use an existing public OpenID Connect Identity Provider (such as Google, or
[others](https://connect2id.com/products/nimbus-oauth-openid-connect-sdk/openid-connect-providers)).
Or, you can run your own Identity Provider, such as CoreOS [dex](https://github.com/coreos/dex),
[Keycloak](https://github.com/keycloak/keycloak),
CloudFoundry [UAA](https://github.com/cloudfoundry/uaa), or
Tremolo Security's [OpenUnison](https://github.com/tremolosecurity/openunison).
-->
Kubernetes 并未提供 OpenID Connect 的身份服务。
你可以使用现有的公共的 OpenID Connect 身份服务（例如 Google 或者
[其他服务](https://connect2id.com/products/nimbus-oauth-openid-connect-sdk/openid-connect-providers)）。
或者，你也可以选择自己运行一个身份服务，例如
CoreOS [dex](https://github.com/coreos/dex)、
[Keycloak](https://github.com/keycloak/keycloak)、
CloudFoundry [UAA](https://github.com/cloudfoundry/uaa) 或者
Tremolo Security 的
[OpenUnison](https://github.com/tremolosecurity/openunison)。

<!--
For an identity provider to work with Kubernetes it must:

1.  Support [OpenID connect discovery](https://openid.net/specs/openid-connect-discovery-1_0.html); not all do.
2.  Run in TLS with non-obsolete ciphers
3.  Have a CA signed certificate (even if the CA is not a commercial CA or is self signed)
-->
要在 Kubernetes 环境中使用某身份服务，该服务必须：

1.  支持 [OpenID connect 发现](https://openid.net/specs/openid-connect-discovery-1_0.html)；
    但事实上并非所有服务都具备此能力
2.  运行 TLS 协议且所使用的加密组件都未过时
3.  拥有由 CA 签名的证书（即使 CA 不是商业 CA 或者是自签名的 CA 也可以）

<!--
A note about requirement #3 above, requiring a CA signed certificate.  If you deploy your own identity provider (as opposed to one of the cloud providers like Google or Microsoft) you MUST have your identity provider's web server certificate signed by a certificate with the `CA` flag set to `TRUE`, even if it is self signed.  This is due to GoLang's TLS client implementation being very strict to the standards around certificate validation.  If you don't have a CA handy, you can use [this script](https://github.com/dexidp/dex/blob/master/examples/k8s/gencert.sh) from the Dex team to create a simple CA and a signed certificate and key pair.
Or you can use [this similar script](https://raw.githubusercontent.com/TremoloSecurity/openunison-qs-kubernetes/master/src/main/bash/makessl.sh) that generates SHA256 certs with a longer life and larger key size.
-->
关于上述第三条需求，即要求具备 CA 签名的证书，有一些额外的注意事项。
如果你部署了自己的身份服务，而不是使用云厂商（如 Google 或 Microsoft）所提供的服务，
你必须对身份服务的 Web 服务器证书进行签名，签名所用证书的 `CA` 标志要设置为
`TRUE`，即使用的是自签名证书。这是因为 GoLang 的 TLS 客户端实现对证书验证
标准方面有非常严格的要求。如果你手头没有现成的 CA 证书，可以使用 CoreOS
团队所开发的[这个脚本](https://github.com/dexidp/dex/blob/master/examples/k8s/gencert.sh)
来创建一个简单的 CA 和被签了名的证书与密钥对。
或者你也可以使用
[这个类似的脚本](https://raw.githubusercontent.com/TremoloSecurity/openunison-qs-kubernetes/master/src/main/bash/makessl.sh)，
生成一个合法期更长、密钥尺寸更大的 SHA256 证书。

<!--
Setup instructions for specific systems:
-->
特定系统的安装指令：

- [UAA](https://docs.cloudfoundry.org/concepts/architecture/uaa.html)
- [Dex](https://dexidp.io/docs/kubernetes/)
- [OpenUnison](https://www.tremolosecurity.com/orchestra-k8s/)

<!--
#### Using kubectl

##### Option 1 - OIDC Authenticator

The first option is to use the kubectl `oidc` authenticator, which sets the `id_token` as a bearer token for all requests and refreshes the token once it expires. After you've logged into your provider, use kubectl to add your `id_token`, `refresh_token`, `client_id`, and `client_secret` to configure the plugin.

Providers that don't return an `id_token` as part of their refresh token response aren't supported by this plugin and should use "Option 2" below.
-->
#### 使用 kubectl   {#using-kubectl}

##### 选项一 - OIDC 身份认证组件

第一种方案是使用 kubectl 的 `oidc` 身份认证组件，该组件将 `id_token` 设置
为所有请求的持有者令牌，并且在令牌过期时自动刷新。在你登录到你的身份服务之后，
可以使用 kubectl 来添加你的 `id_token`、`refresh_token`、`client_id` 和
`client_secret`，以配置该插件。

如果服务在其刷新令牌响应中不包含 `id_token`，则此插件无法支持该服务。
这时你应该考虑下面的选项二。

```bash
kubectl config set-credentials USER_NAME \
   --auth-provider=oidc \
   --auth-provider-arg=idp-issuer-url=( issuer url ) \
   --auth-provider-arg=client-id=( your client id ) \
   --auth-provider-arg=client-secret=( your client secret ) \
   --auth-provider-arg=refresh-token=( your refresh token ) \
   --auth-provider-arg=idp-certificate-authority=( path to your ca certificate ) \
   --auth-provider-arg=id-token=( your id_token )
```

<!--
As an example, running the below command after authenticating to your identity provider:
-->
作为示例，在完成对你的身份服务的身份认证之后，运行下面的命令：

```bash
kubectl config set-credentials mmosley  \
        --auth-provider=oidc  \
        --auth-provider-arg=idp-issuer-url=https://oidcidp.tremolo.lan:8443/auth/idp/OidcIdP  \
        --auth-provider-arg=client-id=kubernetes  \
        --auth-provider-arg=client-secret=1db158f6-177d-4d9c-8a8b-d36869918ec5  \
        --auth-provider-arg=refresh-token=q1bKLFOyUiosTfawzA93TzZIDzH2TNa2SMm0zEiPKTUwME6BkEo6Sql5yUWVBSWpKUGphaWpxSVAfekBOZbBhaEW+VlFUeVRGcluyVF5JT4+haZmPsluFoFu5XkpXk5BXqHega4GAXlF+ma+vmYpFcHe5eZR+slBFpZKtQA= \
        --auth-provider-arg=idp-certificate-authority=/root/ca.pem \
        --auth-provider-arg=id-token=eyJraWQiOiJDTj1vaWRjaWRwLnRyZW1vbG8ubGFuLCBPVT1EZW1vLCBPPVRybWVvbG8gU2VjdXJpdHksIEw9QXJsaW5ndG9uLCBTVD1WaXJnaW5pYSwgQz1VUy1DTj1rdWJlLWNhLTEyMDIxNDc5MjEwMzYwNzMyMTUyIiwiYWxnIjoiUlMyNTYifQ.eyJpc3MiOiJodHRwczovL29pZGNpZHAudHJlbW9sby5sYW46ODQ0My9hdXRoL2lkcC9PaWRjSWRQIiwiYXVkIjoia3ViZXJuZXRlcyIsImV4cCI6MTQ4MzU0OTUxMSwianRpIjoiMm96US15TXdFcHV4WDlHZUhQdy1hZyIsImlhdCI6MTQ4MzU0OTQ1MSwibmJmIjoxNDgzNTQ5MzMxLCJzdWIiOiI0YWViMzdiYS1iNjQ1LTQ4ZmQtYWIzMC0xYTAxZWU0MWUyMTgifQ.w6p4J_6qQ1HzTG9nrEOrubxIMb9K5hzcMPxc9IxPx2K4xO9l-oFiUw93daH3m5pluP6K7eOE6txBuRVfEcpJSwlelsOsW8gb8VJcnzMS9EnZpeA0tW_p-mnkFc3VcfyXuhe5R3G7aa5d8uHv70yJ9Y3-UhjiN9EhpMdfPAoEB9fYKKkJRzF7utTTIPGrSaSU6d2pcpfYKaxIwePzEkT4DfcQthoZdy9ucNvvLoi1DIC-UocFD8HLs8LYKEqSxQvOcvnThbObJ9af71EwmuE21fO5KzMW20KtAeget1gnldOosPtz1G5EwvaQ401-RPQzPGMVBld0_zMCAwZttJ4knw
```

<!--
Which would produce the below configuration:
-->
此操作会生成以下配置：

```yaml
users:
- name: mmosley
  user:
    auth-provider:
      config:
        client-id: kubernetes
        client-secret: 1db158f6-177d-4d9c-8a8b-d36869918ec5
        id-token: eyJraWQiOiJDTj1vaWRjaWRwLnRyZW1vbG8ubGFuLCBPVT1EZW1vLCBPPVRybWVvbG8gU2VjdXJpdHksIEw9QXJsaW5ndG9uLCBTVD1WaXJnaW5pYSwgQz1VUy1DTj1rdWJlLWNhLTEyMDIxNDc5MjEwMzYwNzMyMTUyIiwiYWxnIjoiUlMyNTYifQ.eyJpc3MiOiJodHRwczovL29pZGNpZHAudHJlbW9sby5sYW46ODQ0My9hdXRoL2lkcC9PaWRjSWRQIiwiYXVkIjoia3ViZXJuZXRlcyIsImV4cCI6MTQ4MzU0OTUxMSwianRpIjoiMm96US15TXdFcHV4WDlHZUhQdy1hZyIsImlhdCI6MTQ4MzU0OTQ1MSwibmJmIjoxNDgzNTQ5MzMxLCJzdWIiOiI0YWViMzdiYS1iNjQ1LTQ4ZmQtYWIzMC0xYTAxZWU0MWUyMTgifQ.w6p4J_6qQ1HzTG9nrEOrubxIMb9K5hzcMPxc9IxPx2K4xO9l-oFiUw93daH3m5pluP6K7eOE6txBuRVfEcpJSwlelsOsW8gb8VJcnzMS9EnZpeA0tW_p-mnkFc3VcfyXuhe5R3G7aa5d8uHv70yJ9Y3-UhjiN9EhpMdfPAoEB9fYKKkJRzF7utTTIPGrSaSU6d2pcpfYKaxIwePzEkT4DfcQthoZdy9ucNvvLoi1DIC-UocFD8HLs8LYKEqSxQvOcvnThbObJ9af71EwmuE21fO5KzMW20KtAeget1gnldOosPtz1G5EwvaQ401-RPQzPGMVBld0_zMCAwZttJ4knw
        idp-certificate-authority: /root/ca.pem
        idp-issuer-url: https://oidcidp.tremolo.lan:8443/auth/idp/OidcIdP
        refresh-token: q1bKLFOyUiosTfawzA93TzZIDzH2TNa2SMm0zEiPKTUwME6BkEo6Sql5yUWVBSWpKUGphaWpxSVAfekBOZbBhaEW+VlFUeVRGcluyVF5JT4+haZmPsluFoFu5XkpXk5BXq
      name: oidc
```

<!--
Once your `id_token` expires, `kubectl` will attempt to refresh your `id_token` using your `refresh_token` and `client_secret` storing the new values for the `refresh_token` and `id_token` in your `.kube/config`.
-->
当你的 `id_token` 过期时，`kubectl` 会尝试使用你的 `refresh_token` 来刷新你的
`id_token`，并且在 `client_secret` 中存放 `refresh_token` 的新值，同时把
`id_token` 的新值写入到 `.kube/config` 文件中。

<!--
##### Option 2 - Use the `--token` Option

The `kubectl` command lets you pass in a token using the `--token` option.  Simply copy and paste the `id_token` into this option:
-->
##### 选项二 - 使用 `--token` 选项

`kubectl` 命令允许你使用 `--token` 选项传递一个令牌。
你可以将 `id_token` 的内容复制粘贴过来，作为此标志的取值：

```bash
kubectl --token=eyJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJodHRwczovL21sYi50cmVtb2xvLmxhbjo4MDQzL2F1dGgvaWRwL29pZGMiLCJhdWQiOiJrdWJlcm5ldGVzIiwiZXhwIjoxNDc0NTk2NjY5LCJqdGkiOiI2RDUzNXoxUEpFNjJOR3QxaWVyYm9RIiwiaWF0IjoxNDc0NTk2MzY5LCJuYmYiOjE0NzQ1OTYyNDksInN1YiI6Im13aW5kdSIsInVzZXJfcm9sZSI6WyJ1c2VycyIsIm5ldy1uYW1lc3BhY2Utdmlld2VyIl0sImVtYWlsIjoibXdpbmR1QG5vbW9yZWplZGkuY29tIn0.f2As579n9VNoaKzoF-dOQGmXkFKf1FMyNV0-va_B63jn-_n9LGSCca_6IVMP8pO-Zb4KvRqGyTP0r3HkHxYy5c81AnIh8ijarruczl-TK_yF5akjSTHFZD-0gRzlevBDiH8Q79NAr-ky0P4iIXS8lY9Vnjch5MF74Zx0c3alKJHJUnnpjIACByfF2SCaYzbWFMUNat-K1PaUk5-ujMBG7yYnr95xD-63n8CO8teGUAAEMx6zRjzfhnhbzX-ajwZLGwGUBT4WqjMs70-6a7_8gZmLZb2az1cZynkFRj2BaCkVT3A2RrjeEwZEtGXlMqKJ1_I2ulrOVsYx01_yD35-rw get nodes
```

<!--
### Webhook Token Authentication

Webhook authentication is a hook for verifying bearer tokens.

* `--authentication-token-webhook-config-file` a configuration file describing how to access the remote webhook service.
* `--authentication-token-webhook-cache-ttl` how long to cache authentication decisions. Defaults to two minutes.
-->
### Webhook 令牌身份认证   {#webhook-token-authentication}

Webhook 身份认证是一种用来验证持有者令牌的回调机制。

* `--authentication-token-webhook-config-file` 指向一个配置文件，其中描述
  如何访问远程的 Webhook 服务。
* `--authentication-token-webhook-cache-ttl` 用来设定身份认证决定的缓存时间。
  默认时长为 2 分钟。

<!--
The configuration file uses the [kubeconfig](/docs/concepts/configuration/organize-cluster-access-kubeconfig/)
file format. Within the file, `clusters` refers to the remote service and
`users` refers to the API server webhook. An example would be:
-->
配置文件使用 [kubeconfig](/zh/docs/concepts/configuration/organize-cluster-access-kubeconfig/)
文件的格式。文件中，`clusters` 指代远程服务，`users` 指代远程 API 服务
Webhook。下面是一个例子：

<!--
```yaml
# Kubernetes API version
apiVersion: v1
# kind of the API object
kind: Config
# clusters refers to the remote service.
clusters:
  - name: name-of-remote-authn-service
    cluster:
      certificate-authority: /path/to/ca.pem         # CA for verifying the remote service.
      server: https://authn.example.com/authenticate # URL of remote service to query. Must use 'https'.

# users refers to the API server's webhook configuration.
users:
  - name: name-of-api-server
    user:
      client-certificate: /path/to/cert.pem # cert for the webhook plugin to use
      client-key: /path/to/key.pem          # key matching the cert

# kubeconfig files require a context. Provide one for the API server.
current-context: webhook
contexts:
- context:
    cluster: name-of-remote-authn-service
    user: name-of-api-sever
  name: webhook
```
-->
```yaml
# Kubernetes API 版本
apiVersion: v1
# API 对象类别
kind: Config
# clusters 指代远程服务
clusters:
  - name: name-of-remote-authn-service
    cluster:
      certificate-authority: /path/to/ca.pem         # 用来验证远程服务的 CA
      server: https://authn.example.com/authenticate # 要查询的远程服务 URL。必须使用 'https'。

# users 指代 API 服务的 Webhook 配置
users:
  - name: name-of-api-server
    user:
      client-certificate: /path/to/cert.pem # Webhook 插件要使用的证书
      client-key: /path/to/key.pem          # 与证书匹配的密钥

# kubeconfig 文件需要一个上下文（Context），此上下文用于本 API 服务器
current-context: webhook
contexts:
- context:
    cluster: name-of-remote-authn-service
    user: name-of-api-sever
  name: webhook
```

<!--
When a client attempts to authenticate with the API server using a bearer token
as discussed [above](#putting-a-bearer-token-in-a-request),
the authentication webhook POSTs a JSON-serialized `authentication.k8s.io/v1beta1` `TokenReview` object containing the token
to the remote service. Kubernetes will not challenge a request that lacks such a header.
-->
当客户端尝试在 API 服务器上使用持有者令牌完成身份认证（
如[前](#putting-a-bearer-token-in-a-request)所述）时，
身份认证 Webhook 会用 POST 请求发送一个 JSON 序列化的对象到远程服务。
该对象是 `authentication.k8s.io/v1beta1` 组的 `TokenReview` 对象，
其中包含持有者令牌。
Kubernetes 不会强制请求提供此 HTTP 头部。

<!--
Note that webhook API objects are subject to the same [versioning compatibility rules](/docs/concepts/overview/kubernetes-api/)
as other Kubernetes API objects. Implementers should be aware of looser
compatibility promises for beta objects and check the "apiVersion" field of the
request to ensure correct deserialization. Additionally, the API server must
enable the `authentication.k8s.io/v1beta1` API extensions group (`--runtime-config=authentication.k8s.io/v1beta1=true`).

The POST body will be of the following format:
-->
要注意的是，Webhook API 对象和其他 Kubernetes API 对象一样，也要受到同一
[版本兼容规则](/zh/docs/concepts/overview/kubernetes-api/)约束。
实现者要了解对 Beta 阶段对象的兼容性承诺，并检查请求的 `apiVersion` 字段，
以确保数据结构能够正常反序列化解析。此外，API 服务器必须启用
`authentication.k8s.io/v1beta1` API 扩展组
（`--runtime-config=authentication.k8s.io/v1beta1=true`）。

POST 请求的 Body 部分将是如下格式：

<!--
```json
{
  "apiVersion": "authentication.k8s.io/v1beta1",
  "kind": "TokenReview",
  "spec": {
    "token": "(BEARERTOKEN)"
  }
}
```
-->
```json
{
  "apiVersion": "authentication.k8s.io/v1beta1",
  "kind": "TokenReview",
  "spec": {
    "token": "<持有者令牌>"
  }
}
```

<!--
The remote service is expected to fill the `status` field of
the request to indicate the success of the login. The response body's `spec`
field is ignored and may be omitted. A successful validation of the bearer
token would return:
-->
远程服务应该会填充请求的 `status` 字段，以标明登录操作是否成功。
响应的 Body 中的 `spec` 字段会被忽略，因此可以省略。
如果持有者令牌验证成功，应该返回如下所示的响应：

```json
{
  "apiVersion": "authentication.k8s.io/v1beta1",
  "kind": "TokenReview",
  "status": {
    "authenticated": true,
    "user": {
      "username": "janedoe@example.com",
      "uid": "42",
      "groups": [
        "developers",
        "qa"
      ],
      "extra": {
        "extrafield1": [
          "extravalue1",
          "extravalue2"
        ]
      }
    }
  }
}
```

<!--
An unsuccessful request would return:
-->
而不成功的请求会返回：

```json
{
  "apiVersion": "authentication.k8s.io/v1beta1",
  "kind": "TokenReview",
  "status": {
    "authenticated": false
  }
}
```

<!--
HTTP status codes can be used to supply additional error context.
-->
HTTP 状态码可用来提供进一步的错误语境信息。

<!--
### Authenticating Proxy

The API server can be configured to identify users from request header values, such as `X-Remote-User`.
It is designed for use in combination with an authenticating proxy, which sets the request header value.
-->
### 身份认证代理   {#authenticating-proxy}

API 服务器可以配置成从请求的头部字段值（如 `X-Remote-User`）中辩识用户。
这一设计是用来与某身份认证代理一起使用 API 服务器，代理负责设置请求的头部字段值。

<!--
* `--requestheader-username-headers` Required, case-insensitive. Header names to check, in order, for the user identity. The first header containing a value is used as the username.
* `--requestheader-group-headers` 1.6+. Optional, case-insensitive. "X-Remote-Group" is suggested. Header names to check, in order, for the user's groups. All values in all specified headers are used as group names.
* `-requestheader-extra-headers-prefix` 1.6+. Optional, case-insensitive. "X-Remote-Extra-" is suggested. Header prefixes to look for to determine extra information about the user (typically used by the configured authorization plugin). Any headers beginning with any of the specified prefixes have the prefix removed. The remainder of the header name is lowercased and [percent-decoded](https://tools.ietf.org/html/rfc3986#section-2.1) and becomes the extra key, and the header value is the extra value.
-->
* `--requestheader-username-headers` 必需字段，大小写不敏感。用来设置要获得用户身份所要检查的头部字段名称列表（有序）。第一个包含数值的字段会被用来提取用户名。
* `--requestheader-group-headers` 可选字段，在 Kubernetes 1.6 版本以后支持，大小写不敏感。
  建议设置为 "X-Remote-Group"。用来指定一组头部字段名称列表，以供检查用户所属的组名称。
  所找到的全部头部字段的取值都会被用作用户组名。
* `--requestheader-extra-headers-prefix` 可选字段，在 Kubernetes 1.6 版本以后支持，大小写不敏感。
  建议设置为 "X-Remote-Extra-"。用来设置一个头部字段的前缀字符串，API 服务器会基于所给
  前缀来查找与用户有关的一些额外信息。这些额外信息通常用于所配置的鉴权插件。
  API 服务器会将与所给前缀匹配的头部字段过滤出来，去掉其前缀部分，将剩余部分
  转换为小写字符串并在必要时执行[百分号解码](https://tools.ietf.org/html/rfc3986#section-2.1)
  后，构造新的附加信息字段键名。原来的头部字段值直接作为附加信息字段的值。

<!--
Prior to 1.11.3 (and 1.10.7, 1.9.11), the extra key could only contain characters which were [legal in HTTP header labels](https://tools.ietf.org/html/rfc7230#section-3.2.6).
For example, with this configuration:
-->
{{< note >}}
在 1.13.3 版本之前（包括 1.10.7、1.9.11），附加字段的键名只能包含
[HTTP 头部标签的合法字符](https://tools.ietf.org/html/rfc7230#section-3.2.6)。
{{< /note >}}

例如，使用下面的配置：

```
--requestheader-username-headers=X-Remote-User
--requestheader-group-headers=X-Remote-Group
--requestheader-extra-headers-prefix=X-Remote-Extra-
```

<!--
this request:
-->
针对所收到的如下请求：

```http
GET / HTTP/1.1
X-Remote-User: fido
X-Remote-Group: dogs
X-Remote-Group: dachshunds
X-Remote-Extra-Acme.com%2Fproject: some-project
X-Remote-Extra-Scopes: openid
X-Remote-Extra-Scopes: profile
```

<!--
would result in this user info:
-->
会生成下面的用户信息：

```yaml
name: fido
groups:
- dogs
- dachshunds
extra:
  acme.com/project:
  - some-project
  scopes:
  - openid
  - profile
```

<!--
In order to prevent header spoofing, the authenticating proxy is required to present a valid client
certificate to the API server for validation against the specified CA before the request headers are
checked. WARNING: do **not** reuse a CA that is used in a different context unless you understand
the risks and the mechanisms to protect the CA's usage.

* `--requestheader-client-ca-file` Required. PEM-encoded certificate bundle. A valid client certificate must be presented and validated against the certificate authorities in the specified file before the request headers are checked for user names.
* `--requestheader-allowed-names` Optional. List of Common Name values (CNs). If set, a valid client certificate with a CN in the specified list must be presented before the request headers are checked for user names. If empty, any CN is allowed.
-->
为了防范头部信息侦听，在请求中的头部字段被检视之前，
身份认证代理需要向 API 服务器提供一份合法的客户端证书，
供后者使用所给的 CA 来执行验证。
警告：*不要* 在不同的上下文中复用 CA 证书，除非你清楚这样做的风险是什么以及
应如何保护 CA 用法的机制。

* `--requestheader-client-ca-file` 必需字段，给出 PEM 编码的证书包。
  在检查请求的头部字段以提取用户名信息之前，必须提供一个合法的客户端证书，
  且该证书要能够被所给文件中的机构所验证。
* `--requestheader-allowed-names` 可选字段，用来给出一组公共名称（CN）。
  如果此标志被设置，则在检视请求中的头部以提取用户信息之前，必须提供
  包含此列表中所给的 CN 名的、合法的客户端证书。

<!--
## Anonymous requests

When enabled, requests that are not rejected by other configured authentication methods are
treated as anonymous requests, and given a username of `system:anonymous` and a group of
`system:unauthenticated`.
-->
## 匿名请求   {#anonymous-requests}

启用匿名请求支持之后，如果请求没有被已配置的其他身份认证方法拒绝，则被视作
匿名请求（Anonymous Requests）。这类请求获得用户名 `system:anonymous` 和
对应的用户组 `system:unauthenticated`。

<!--
For example, on a server with token authentication configured, and anonymous access enabled,
a request providing an invalid bearer token would receive a `401 Unauthorized` error.
A request providing no bearer token would be treated as an anonymous request.

In 1.5.1-1.5.x, anonymous access is disabled by default, and can be enabled by
passing the `--anonymous-auth=true` option to the API server.
-->
例如，在一个配置了令牌身份认证且启用了匿名访问的服务器上，如果请求提供了非法的
持有者令牌，则会返回 `401 Unauthorized` 错误。
如果请求没有提供持有者令牌，则被视为匿名请求。

在 1.5.1-1.5.x 版本中，匿名访问默认情况下是被禁用的，可以通过为 API 服务器设定
`--anonymous-auth=true` 来启用。

<!--
In 1.6+, anonymous access is enabled by default if an authorization mode other than `AlwaysAllow`
is used, and can be disabled by passing the `-anonymous-auth=false` option to the API server.
Starting in 1.6, the ABAC and RBAC authorizers require explicit authorization of the
`system:anonymous` user or the `system:unauthenticated` group, so legacy policy rules
that grant access to the `*` user or `*` group do not include anonymous users.
-->
在 1.6 及之后版本中，如果所使用的鉴权模式不是 `AlwaysAllow`，则匿名访问默认是被启用的。
从 1.6 版本开始，ABAC 和 RBAC 鉴权模块要求对 `system:anonymous` 用户或者
`system:unauthenticated` 用户组执行显式的权限判定，所以之前的为 `*` 用户或
`*` 用户组赋予访问权限的策略规则都不再包含匿名用户。

<!--
## User impersonation

A user can act as another user through impersonation headers. These let requests
manually override the user info a request authenticates as. For example, an admin
could use this feature to debug an authorization policy by temporarily
impersonating another user and seeing if a request was denied.
-->
## 用户伪装  {#user-impersonation}

一个用户可以通过伪装（Impersonation）头部字段来以另一个用户的身份执行操作。
使用这一能力，你可以手动重载请求被身份认证所识别出来的用户信息。
例如，管理员可以使用这一功能特性来临时伪装成另一个用户，查看请求是否被拒绝，
从而调试鉴权策略中的问题，

<!--
Impersonation requests first authenticate as the requesting user, then switch
to the impersonated user info.

* A user makes an API call with their credentials _and_ impersonation headers.
* API server authenticates the user.
* API server ensures the authenticated users have impersonation privileges.
* Request user info is replaced with impersonation values.
* Request is evaluated, authorization acts on impersonated user info.
-->
带伪装的请求首先会被身份认证识别为发出请求的用户，之后会切换到使用被伪装的用户
的用户信息。

* 用户发起 API 调用时 _同时_ 提供自身的凭据和伪装头部字段信息
* API 服务器对用户执行身份认证
* API 服务器确认通过认证的用户具有伪装特权
* 请求用户的信息被替换成伪装字段的值
* 评估请求，鉴权组件针对所伪装的用户信息执行操作

<!--
The following HTTP headers can be used to performing an impersonation request:

* `Impersonate-User`: The username to act as.
* `Impersonate-Group`: A group name to act as. Can be provided multiple times to set multiple groups. Optional. Requires "Impersonate-User"
* `Impersonate-Extra-( extra name )`: A dynamic header used to associate extra fields with the user. Optional. Requires "Impersonate-User". In order to be preserved consistently, `( extra name )` should be lower-case, and any characters which aren't [legal in HTTP header labels](https://tools.ietf.org/html/rfc7230#section-3.2.6) MUST be utf8 and [percent-encoded](https://tools.ietf.org/html/rfc3986#section-2.1).
-->
以下 HTTP 头部字段可用来执行伪装请求：

* `Impersonate-User`：要伪装成的用户名
* `Impersonate-Group`：要伪装成的用户组名。可以多次指定以设置多个用户组。
  可选字段；要求 "Impersonate-User" 必须被设置。
* `Impersonate-Extra-<附加名称>`：一个动态的头部字段，用来设置与用户相关的附加字段。
  此字段可选；要求 "Impersonate-User" 被设置。为了能够以一致的形式保留，
  `<附加名称>`部分必须是小写字符，如果有任何字符不是
  [合法的 HTTP 头部标签字符](https://tools.ietf.org/html/rfc7230#section-3.2.6)，
  则必须是 utf8 字符，且转换为[百分号编码](https://tools.ietf.org/html/rfc3986#section-2.1)。

<!--
Prior to 1.11.3 (and 1.10.7, 1.9.11), `( extra name )` could only contain characters which were [legal in HTTP header labels](https://tools.ietf.org/html/rfc7230#section-3.2.6).
-->
{{< note >}}
在 1.11.3 版本之前（以及 1.10.7、1.9.11），`<附加名称>` 只能包含
合法的 HTTP 标签字符。
{{< /note >}}

<!--
An example set of headers:
-->
头部字段集合的示例：

```http
Impersonate-User: jane.doe@example.com
Impersonate-Group: developers
Impersonate-Group: admins
Impersonate-Extra-dn: cn=jane,ou=engineers,dc=example,dc=com
Impersonate-Extra-acme.com%2Fproject: some-project
Impersonate-Extra-scopes: view
Impersonate-Extra-scopes: development
```

<!--
When using `kubectl` set the `--as` flag to configure the `Impersonate-User`
header, set the `--as-group` flag to configure the `Impersonate-Group` header.
-->
在使用 `kubectl` 时，可以使用 `--as` 标志来配置 `Impersonate-User` 头部字段值，
使用 `--as-group` 标志配置 `Impersonate-Group` 头部字段值。

```bash
kubectl drain mynode
```

```none
Error from server (Forbidden): User "clark" cannot get nodes at the cluster scope. (get nodes mynode)
```

<!--
Set the `--as` and `--as-group` flag:
-->
设置 `--as` 和 `--as-group` 标志：

```bash
kubectl drain mynode --as=superman --as-group=system:masters
```

```none
node/mynode cordoned
node/mynode drained
```

<!--
To impersonate a user, group, or set extra fields, the impersonating user must
have the ability to perform the "impersonate" verb on the kind of attribute
being impersonated ("user", "group", etc.). For clusters that enable the RBAC
authorization plugin, the following ClusterRole encompasses the rules needed to
set user and group impersonation headers:
-->
要伪装成某个用户、某个组或者设置附加字段，执行伪装操作的用户必须具有对所伪装的
类别（“user”、“group” 等）执行 “impersonate” 动词操作的能力。
对于启用了 RBAC 鉴权插件的集群，下面的 ClusterRole 封装了设置用户和组伪装字段
所需的规则：

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: impersonator
rules:
- apiGroups: [""]
  resources: ["users", "groups", "serviceaccounts"]
  verbs: ["impersonate"]
```

<!--
Extra fields are evaluated as sub-resources of the resource "userextras". To
allow a user to use impersonation headers for the extra field "scopes", a user
should be granted the following role:
-->
附加字段会被作为 `userextras` 资源的子资源来执行权限评估。
如果要允许用户为附加字段 “scopes” 设置伪装头部，该用户需要被授予以下规则：

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: scopes-impersonator
rules:
# 可以设置 "Impersonate-Extra-scopes" 头部
- apiGroups: ["authentication.k8s.io"]
  resources: ["userextras/scopes"]
  verbs: ["impersonate"]
```

<!--
The values of impersonation headers can also be restricted by limiting the set
of `resourceNames` a resource can take.
-->
你也可以通过约束资源可能对应的 `resourceNames` 限制伪装头部的取值：

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: limited-impersonator
rules:
# 可以伪装成用户 "jane.doe@example.com"
- apiGroups: [""]
  resources: ["users"]
  verbs: ["impersonate"]
  resourceNames: ["jane.doe@example.com"]

# 可以伪装成用户组 "developers" 和 "admins"
- apiGroups: [""]
  resources: ["groups"]
  verbs: ["impersonate"]
  resourceNames: ["developers","admins"]

# 可以将附加字段 "scopes" 伪装成 "view" 和 "development"
- apiGroups: ["authentication.k8s.io"]
  resources: ["userextras/scopes"]
  verbs: ["impersonate"]
  resourceNames: ["view", "development"]
```

<!--
## client-go credential plugins
-->
## client-go 凭据插件  {#client-go-credential-plugins}

{{< feature-state for_k8s_version="v1.11" state="beta" >}}

<!--
`k8s.io/client-go` and tools using it such as `kubectl` and `kubelet` are able to execute an
external command to receive user credentials.

This feature is intended for client side integrations with authentication protocols not natively
supported by `k8s.io/client-go` (LDAP, Kerberos, OAuth2, SAML, etc.). The plugin implements the
protocol specific logic, then returns opaque credentials to use. Almost all credential plugin
use cases require a server side component with support for the [webhook token authenticator](#webhook-token-authentication)
to interpret the credential format produced by the client plugin.
-->
`k8s.io/client-go` 及使用它的工具（如 `kubectl` 和 `kubelet`）可以执行某个外部
命令来获得用户的凭据信息。

这一特性的目的是便于客户端与 `k8s.io/client-go` 并不支持的身份认证协议（LDAP、
Kerberos、OAuth2、SAML 等）继承。
插件实现特定于协议的逻辑，之后返回不透明的凭据以供使用。
几乎所有的凭据插件使用场景中都需要在服务器端存在一个支持
[Webhook 令牌身份认证组件](#webhook-token-authentication)的模块，
负责解析客户端插件所生成的凭据格式。

<!--
### Example use case

In a hypothetical use case, an organization would run an external service that exchanges LDAP credentials
for user specific, signed tokens. The service would also be capable of responding to [webhook token
authenticator](#webhook-token-authentication) requests to validate the tokens. Users would be required
to install a credential plugin on their workstation.
-->
### 示例应用场景   {#example-use-case}

在一个假想的应用场景中，某组织运行这一个外部的服务，能够将特定用户的已签名的
令牌转换成 LDAP 凭据。此服务还能够对
[Webhook 令牌身份认证组件](#webhook-token-authentication)的请求做出响应以
验证所提供的令牌。用户需要在自己的工作站上安装一个凭据插件。

<!--
To authenticate against the API:

* The user issues a `kubectl` command.
* Credential plugin prompts the user for LDAP credentials, exchanges credentials with external service for a token.
* Credential plugin returns token to client-go, which uses it as a bearer token against the API server.
* API server uses the [webhook token authenticator](#webhook-token-authentication) to submit a `TokenReview` to the external service.
* External service verifies the signature on the token and returns the user's username and groups.
-->
要对 API 服务器认证身份时：

* 用户发出 `kubectl` 命令。
* 凭据插件提示用户输入 LDAP 凭据，并与外部服务交互，获得令牌。
* 凭据插件将令牌返回该 client-go，后者将其用作持有者令牌提交给 API 服务器。
* API 服务器使用[Webhook 令牌身份认证组件](#webhook-token-authentication)向
  外部服务发出 `TokenReview` 请求。
* 外部服务检查令牌上的签名，返回用户的用户名和用户组信息。

<!--
### Configuration

Credential plugins are configured through [kubectl config files](/docs/tasks/access-application-cluster/configure-access-multiple-clusters/)
as part of the user fields.
-->
### 配置  {#configuration}

凭据插件通过 [kubectl 配置文件](/zh/docs/tasks/access-application-cluster/configure-access-multiple-clusters/)
来作为 user 字段的一部分设置。

<!--
```yaml
apiVersion: v1
kind: Config
users:
- name: my-user
  user:
    exec:
      # Command to execute. Required.
      command: "example-client-go-exec-plugin"

      # API version to use when decoding the ExecCredentials resource. Required.
      #
      # The API version returned by the plugin MUST match the version listed here.
      #
      # To integrate with tools that support multiple versions (such as client.authentication.k8s.io/v1alpha1),
      # set an environment variable or pass an argument to the tool that indicates which version the exec plugin expects.
      apiVersion: "client.authentication.k8s.io/v1beta1"

      # Environment variables to set when executing the plugin. Optional.
      env:
      - name: "FOO"
        value: "bar"

      # Arguments to pass when executing the plugin. Optional.
      args:
      - "arg1"
      - "arg2"

      # Text shown to the user when the executable doesn't seem to be present. Optional.
      installHint: |
        example-client-go-exec-plugin is required to authenticate
        to the current cluster.  It can be installed:

        On macOS: brew install example-client-go-exec-plugin

        On Ubuntu: apt-get install example-client-go-exec-plugin

        On Fedora: dnf install example-client-go-exec-plugin

        ...

      # Whether or not to provide cluster information, which could potentially contain
      # very large CA data, to this exec plugin as a part of the KUBERNETES_EXEC_INFO
      # environment variable.
      provideClusterInfo: true
clusters:
- name: my-cluster
  cluster:
    server: "https://172.17.4.100:6443"
    certificate-authority: "/etc/kubernetes/ca.pem"
    extensions:
    - name: client.authentication.k8s.io/exec # reserved extension name for per cluster exec config
      extension:
        arbitrary: config
        this: can be provided via the KUBERNETES_EXEC_INFO environment variable upon setting provideClusterInfo
        you: ["can", "put", "anything", "here"]
contexts:
- name: my-cluster
  context:
    cluster: my-cluster
    user: my-user
current-context: my-cluster
```
-->
```yaml
apiVersion: v1
kind: Config
users:
- name: my-user
  user:
    exec:
      # 要执行的命令。必需。
      command: "example-client-go-exec-plugin"

      # 解析 ExecCredentials 资源时使用的 API 版本。必需。
      #
      # 插件返回的 API 版本必需与这里列出的版本匹配。
      #
      # 要与支持多个版本的工具（如 client.authentication.k8sio/v1alpha1）集成，
      # 可以设置一个环境变量或者向工具传递一个参数标明 exec 插件所期望的版本。
      apiVersion: "client.authentication.k8s.io/v1beta1"

      # 执行此插件时要设置的环境变量。可选字段。
      env:
      - name: "FOO"
        value: "bar"

      # 执行插件时要传递的参数。可选字段。
      args:
      - "arg1"
      - "arg2"

      # 当可执行文件不存在时显示给用户的文本。可选的。
      installHint: |
        需要 example-client-go-exec-plugin 来在当前集群上执行身份认证。可以通过以下命令安装：

        MacOS: brew install example-client-go-exec-plugin

        Ubuntu: apt-get install example-client-go-exec-plugin

        Fedora: dnf install example-client-go-exec-plugin

        ...

      # 是否使用 KUBERNETES_EXEC_INFO 环境变量的一部分向这个 exec 插件
      # 提供集群信息（可能包含非常大的 CA 数据）
      provideClusterInfo: true
clusters:
- name: my-cluster
  cluster:
    server: "https://172.17.4.100:6443"
    certificate-authority: "/etc/kubernetes/ca.pem"
    extensions:
    - name: client.authentication.k8s.io/exec # 为每个集群 exec 配置保留的扩展名
      extension:
        arbitrary: config
        this: 在设置 provideClusterInfo 时可通过环境变量 KUBERNETES_EXEC_INFO 指定
        you: ["can", "put", "anything", "here"]
contexts:
- name: my-cluster
  context:
    cluster: my-cluster
    user: my-user
current-context: my-cluster
```

<!--
Relative command paths are interpreted as relative to the directory of the config file. If
KUBECONFIG is set to `/home/jane/kubeconfig` and the exec command is `./bin/example-client-go-exec-plugin`,
the binary `/home/jane/bin/example-client-go-exec-plugin` is executed.
-->
解析相对命令路径时，kubectl 将其视为与配置文件比较而言的相对路径。
如果 KUBECONFIG 被设置为 `/home/jane/kubeconfig`，而 exec 命令为
`./bin/example-client-go-exec-plugin`，则要执行的可执行文件为
`/home/jane/bin/example-client-go-exec-plugin`。

```yaml
- name: my-user
  user:
    exec:
      # 对 kubeconfig 目录而言的相对路径
      command: "./bin/example-client-go-exec-plugin"
      apiVersion: "client.authentication.k8s.io/v1beta1"
```

<!--
### Input and output formats

The executed command prints an `ExecCredential` object to `stdout`. `k8s.io/client-go`
authenticates against the Kubernetes API using the returned credentials in the `status`.

When run from an interactive session, `stdin` is exposed directly to the plugin. Plugins should use a
[TTY check](https://godoc.org/golang.org/x/crypto/ssh/terminal#IsTerminal) to determine if it's
appropriate to prompt a user interactively.

To use bearer token credentials, the plugin returns a token in the status of the `ExecCredential`.
-->
### 输出和输出格式   {#input-and-output-formats}

所执行的命令会在 `stdout` 打印 `ExecCredential` 对象。
`k8s.io/client-go` 使用 `status` 中返回的凭据信息向 Kubernetes API 服务器
执行身份认证。

在交互式会话中运行时，`stdin` 是直接暴露给插件使用的。
插件应该使用
[TTY check](https://godoc.org/golang.org/x/crypto/ssh/terminal#IsTerminal)
来确定是否适合用交互方式请求用户输入。

与使用持有者令牌凭据，插件在 `ExecCredential` 的状态中返回一个令牌：

```json
{
  "apiVersion": "client.authentication.k8s.io/v1beta1",
  "kind": "ExecCredential",
  "status": {
    "token": "my-bearer-token"
  }
}
```

<!--
Alternatively, a PEM-encoded client certificate and key can be returned to use TLS client auth.
If the plugin returns a different certificate and key on a subsequent call, `k8s.io/client-go`
will close existing connections with the server to force a new TLS handshake.

If specified, `clientKeyData` and `clientCertificateData` must both must be present.

`clientCertificateData` may contain additional intermediate certificates to send to the server.
-->
另一种方案是，返回 PEM 编码的客户端证书和密钥，以便执行 TLS 客户端身份认证。
如果插件在后续调用中返回了不同的证书或密钥，`k8s.io/client-go`
会终止其与服务器的连接，从而强制执行新的 TLS 握手过程。

如果指定了这种方式，则 `clientKeyData` 和 `clientCertificateData` 字段都必需存在。

`clientCertificateData` 字段可能包含一些要发送给服务器的中间证书（Intermediate
Certificates）。

```json
{
  "apiVersion": "client.authentication.k8s.io/v1beta1",
  "kind": "ExecCredential",
  "status": {
    "clientCertificateData": "-----BEGIN CERTIFICATE-----\n...\n-----END CERTIFICATE-----",
    "clientKeyData": "-----BEGIN RSA PRIVATE KEY-----\n...\n-----END RSA PRIVATE KEY-----"
  }
}
```

<!--
Optionally, the response can include the expiry of the credential formatted as a
RFC3339 timestamp. Presence or absence of an expiry has the following impact:

- If an expiry is included, the bearer token and TLS credentials are cached until
  the expiry time is reached, or if the server responds with a 401 HTTP status code,
  or when the process exits.
- If an expiry is omitted, the bearer token and TLS credentials are cached until
  the server responds with a 401 HTTP status code or until the process exits.
-->
作为一种可选方案，响应中还可以包含以 RFC3339 时间戳格式给出的证书到期时间。
证书到期时间的有无会有如下影响：

- 如果响应中包含了到期时间，持有者令牌和 TLS 凭据会被缓存，直到到期期限到来、
  或者服务器返回 401 HTTP 状态码，或者进程退出。
- 如果未指定到期时间，则持有者令牌和 TLS 凭据会被缓存，直到服务器返回 401
  HTTP 状态码或者进程退出。

```json
{
  "apiVersion": "client.authentication.k8s.io/v1beta1",
  "kind": "ExecCredential",
  "status": {
    "token": "my-bearer-token",
    "expirationTimestamp": "2018-03-05T17:30:20-08:00"
  }
}
```

<!--
The plugin can optionally be called with an environment variable, `KUBERNETES_EXEC_INFO`,
that contains information about the cluster for which this plugin is obtaining
credentials. This information can be used to perform cluster-specific credential
acquisition logic. In order to enable this behavior, the `provideClusterInfo` field must
be set on the exec user field in the
[kubeconfig](/docs/concepts/configuration/organize-cluster-access-kubeconfig/). Here is an
example of the aforementioned `KUBERNETES_EXEC_INFO` environment variable.
-->

调用此插件时可以选择性地设置环境变量 `KUBERNETES_EXEC_INFO`。
该变量包含了此插件获取凭据所针对的集群信息。此信息可用于执行群集特定的凭据获取逻辑。
为了启用此行为，必须在 [kubeconfig](/zh/docs/concepts/configuration/organize-cluster-access-kubeconfig/)
中的 exec user 字段上设置`provideClusterInfo`字段。
下面是上述 `KUBERNETES_EXEC_INFO` 环境变量的示例。

```json
{
  "apiVersion": "client.authentication.k8s.io/v1beta1",
  "kind": "ExecCredential",
  "spec": {
    "cluster": {
      "server": "https://172.17.4.100:6443",
      "certificate-authority-data": "LS0t...",
      "config": {
        "arbitrary": "config",
        "this": "在设置 provideClusterInfo 时可通过环境变量 KUBERNETES_EXEC_INFO 指定",
        "you": ["can", "put", "anything", "here"]
      }
    }
  }
}
```
