---
title: 证书签名请求
content_type: concept
weight: 20
---
<!-- 
reviewers:
- liggitt
- mikedanese
- munnerz
title: Certificate Signing Requests
content_type: concept
weight: 20
-->

<!-- overview -->

{{< feature-state for_k8s_version="v1.19" state="stable" >}}

<!-- 
The Certificates API enables automation of
[X.509](https://www.itu.int/rec/T-REC-X.509) credential provisioning by providing
a programmatic interface for clients of the Kubernetes API to request and obtain
X.509 {{< glossary_tooltip term_id="certificate" text="certificates" >}} 
from a Certificate Authority (CA).

A CertificateSigningRequest (CSR) resource is used to request that a certificate be signed
by a denoted signer, after which the request may be approved or denied before
finally being signed.
-->
证书 API 支持 
[X.509](https://www.itu.int/rec/T-REC-X.509) 
的自动化配置，
它为 Kubernetes API 的客户端提供一个编程接口，
用于从证书颁发机构（CA）请求并获取 X.509 
{{< glossary_tooltip term_id="certificate" text="证书" >}}。

CertificateSigningRequest（CSR）资源用来向指定的签名者申请证书签名，
在最终签名之前，申请可能被批准，也可能被拒绝。

<!-- body -->

<!-- 
## Request signing process

The CertificateSigningRequest resource type allows a client to ask for an X.509 certificate
be issued, based on a signing request.

The CertificateSigningRequest object includes a PEM-encoded PKCS#10 signing request in
the `spec.request` field. The CertificateSigningRequest denotes the _signer_ (the
recipient that the request is being made to) using the `spec.signerName` field.
Note that `spec.signerName` is a required key after api version `certificates.k8s.io/v1`.
-->
## 请求签名流程 {#request-signing-process}

CertificateSigningRequest 资源类型允许客户使用它申请发放 X.509 证书。
CertificateSigningRequest 对象 在 `spec.request` 中包含一个 PEM 编码的 PKCS#10 签名请求。
CertificateSigningRequest 使用 `spec.signerName` 字段标示 _签名者_（请求的接收方）。
注意，`spec.signerName` 在 `certificates.k8s.io/v1` 之后的 API 版本是必填项。

<!-- 
Once created, a CertificateSigningRequest must be approved before it can be signed.
Depending on the signer selected, a CertificateSigningRequest may be automatically approved
by a {{< glossary_tooltip text="controller" term_id="controller" >}}.
Otherwise, a CertificateSigningRequest must be manually approved 
either via the REST API (or client-go)
or by running `kubectl certificate approve`. 
Likewise, a CertificateSigningRequest may also be denied,
which tells the configured signer that it must not sign the request.
-->
创建完成的 CertificateSigningRequest，要先通过批准，然后才能签名。
根据所选的签名者，CertificateSigningRequest 可能会被
{{< glossary_tooltip text="控制器" term_id="controller" >}}自动批准。
否则，就必须人工批准，
人工批准可以使用 REST API（或 go 客户端），也可以执行 `kubectl certificate approve` 命令。
同样，CertificateSigningRequest 也可能被驳回，
这就相当于通知了指定的签名者，这个证书不能签名。

<!--  
For certificates that have been approved, the next step is signing. 
The relevant signing controller
first validates that the signing conditions are met and then creates a certificate.
The signing controller then updates the CertificateSigningRequest, 
storing the new certificate into
the `status.certificate` field of the existing CertificateSigningRequest object. The
`status.certificate` field is either empty or contains a X.509 certificate, 
encoded in PEM format.
The CertificateSigningRequest `status.certificate` field is empty until the signer does this.
-->
对于已批准的证书，下一步是签名。
对应的签名控制器首先验证签名条件是否满足，然后才创建证书。
签名控制器然后更新 CertificateSigningRequest，
将新证书保存到现有 CertificateSigningRequest 对象的 `status.certificate` 字段中。
此时，字段 `status.certificate` 要么为空，要么包含一个用 PEM 编码的 X.509 证书。
直到签名完成前，CertificateSigningRequest 的字段 `status.certificate` 都为空。

<!-- 
Once the `status.certificate` field has been populated, 
the request has been completed and clients can now
fetch the signed certificate PEM data from the CertificateSigningRequest resource.
The signers can instead deny certificate signing if the approval conditions are not met.
-->
一旦 `status.certificate` 字段完成填充，请求既算完成，
客户端现在可以从 CertificateSigningRequest 资源中获取已签名的证书的 PEM 数据。
当然如果不满足签名条件，签名者可以拒签。

<!-- 
In order to reduce the number of old CertificateSigningRequest resources left 
in a cluster, a garbage collection
controller runs periodically. 
The garbage collection removes CertificateSigningRequests that have not changed
state for some duration:

* Approved requests: automatically deleted after 1 hour
* Denied requests: automatically deleted after 1 hour
* Pending requests: automatically deleted after 1 hour
-->
为了减少集群中遗留的过时的 CertificateSigningRequest 资源的数量，
一个垃圾收集控制器将会周期性地运行。
此垃圾收集器会清除在一段时间内没有改变过状态的 CertificateSigningRequests：

* 已批准的请求：1小时后自动删除
* 已拒绝的请求：1小时后自动删除
* 挂起的请求：1小时后自动删除

<!-- 
## Signers

Custom signerNames can also be specified. All signers should provide information about how they work 
so that clients can predict what will happen to their CSRs.
This includes:
-->
## 签名者 {#signers}

也可以指定自定义 signerName。
所有签名者都应该提供自己工作方式的信息，
以便客户端可以预期到他们的 CSR 将发生什么。
此类信息包括：

<!-- 
1. **Trust distribution**: how trust (CA bundles) are distributed.
2.  **Permitted subjects**: any restrictions on and behavior 
   when a disallowed subject is requested.
3. **Permitted x509 extensions**: including IP subjectAltNames, DNS subjectAltNames, 
   Email subjectAltNames, URI subjectAltNames etc, 
   and behavior when a disallowed extension is requested.
4. **Permitted key usages / extended key usages**: any restrictions on and behavior 
   when usages different than the signer-determined usages are specified in the CSR.
5. **Expiration/certificate lifetime**: whether it is fixed by the signer, 
   configurable by the admin, determined by the CSR object etc and the behavior 
   when an expiration is different than the signer-determined expiration 
   that is specified in the CSR.
6. **CA bit allowed/disallowed**: and behavior if a CSR contains a request 
   a for a CA certificate when the signer does not permit it.
-->
1. **信任分发**：信任（CA 证书包）是如何分发的。
2. **许可的主体**：当一个受限制的主体（subject）发送请求时，相应的限制和应对手段。
3. **许可的 x509 扩展**：包括 IP subjectAltNames、DNS subjectAltNames、
   Email subjectAltNames、URI subjectAltNames 等，请求一个受限制的扩展项时的应对手段。
4. **许可的密钥用途/扩展的密钥用途**：当用途和签名者在 CSR 中指定的用途不同时，
   相应的限制和应对手段。
5. **过期时间/证书有效期**：过期时间由签名者确定、由管理员配置，还是由 CSR 对象指定等，
   以及过期时间与签名者在 CSR 中指定过期时间不同时的应对手段。
6. **允许/不允许 CA 位**：当 CSR 包含一个签名者并不允许的 CA 证书的请求时，相应的应对手段。

<!-- 
Commonly, the `status.certificate` field contains a single PEM-encoded X.509
certificate once the CSR is approved and the certificate is issued. Some
signers store multiple certificates into the `status.certificate` field. In
that case, the documentation for the signer should specify the meaning of
additional certificates; for example, this might be the certificate plus
intermediates to be presented during TLS handshakes.
-->
一般来说，当 CSR 被批准通过，且证书被签名后，`status.certificate` 字段
将包含一个 PEM 编码的 X.509 证书。
有些签名者在 `status.certificate` 字段中存储多个证书。
在这种情况下，签名者的说明文档应当指明附加证书的含义。
例如，这是要在 TLS 握手时提供的证书和中继证书。

<!--
The PKCS#10 signing request format doesn't allow to specify a certificate
expiration or lifetime. The expiration or lifetime therefore has to be set
through e.g. an annotation on the CSR object. While it's theoretically
possible for a signer to use that expiration date, there is currently no
known implementation that does. (The built-in signers all use the same
`ClusterSigningDuration` configuration option, which defaults to 1 year,
and can be changed with the `--cluster-signing-duration` command-line
flag of the kube-controller-manager.)
-->
PKCS#10 签名请求格式不允许设置证书的过期时间或者生命期。因此，证书的过期
时间或者生命期必须通过类似 CSR 对象的注解字段这种形式来设置。
尽管让签名者使用过期日期从理论上来讲也是可行的，目前还不存在哪个实现这样做了。
（内置的签名者都是用相同的 `ClusterSigningDuration` 配置选项，而该选项
中将生命期的默认值设为 1 年，且可通过 kube-controller-manager 的命令行选项
`--cluster-signing-duration` 来更改。）

<!-- 
### Kubernetes signers

Kubernetes provides built-in signers that each have a well-known `signerName`:
-->
### Kubernetes 签名者 {#kubernetes-signers}

Kubernetes提供了内置的签名者，每个签名者都有一个众所周知的 `signerName`:

<!-- 
1. `kubernetes.io/kube-apiserver-client`: signs certificates that will be honored as client certificates by the API server.
  Never auto-approved by {{< glossary_tooltip term_id="kube-controller-manager" >}}.
    1. Trust distribution: signed certificates must be honored as client-certificates by the kube-apiserver. The CA bundle is not distributed by any other means.
    1. Permitted subjects - no subject restrictions, but approvers and signers may choose not to approve or sign.
       Certain subjects like cluster-admin level users or groups vary between distributions and installations,
       but deserve additional scrutiny before approval and signing.
       The `CertificateSubjectRestriction` admission plugin is enabled by default to restrict `system:masters`,
       but it is often not the only cluster-admin subject in a cluster.
    1. Permitted x509 extensions - honors subjectAltName and key usage extensions and discards other extensions.
    1. Permitted key usages - must include `["client auth"]`. Must not include key usages beyond `["digital signature", "key encipherment", "client auth"]`.
    1. Expiration/certificate lifetime - set by the `--cluster-signing-duration` option for the
       kube-controller-manager implementation of this signer.
    1. CA bit allowed/disallowed - not allowed.
-->
1. `kubernetes.io/kube-apiserver-client`：签名的证书将被 API 服务器视为客户证书。
   {{< glossary_tooltip term_id="kube-controller-manager" >}} 不会自动批准它。
   1. 信任分发：签名的证书将被 API 服务器视为客户端证书。CA 证书包不通过任何其他方式分发。
   1. 许可的主体：没有主体限制，但审核人和签名者可以选择不批准或不签署。
      某些主体，比如集群管理员级别的用户或组因部署和安装方式不同而不同，
      所以批准和签署之前需要进行额外仔细审查。
      用来限制 `system:masters` 的 CertificateSubjectRestriction 准入插件默认处于启用状态，
      但它通常不是集群中唯一的集群管理员主体。
   1. 许可的 x509 扩展：允许 subjectAltName 和 key usage 扩展，弃用其他扩展。
   1. 许可的密钥用途：必须包含 `["client auth"]`，但不能包含
      `["digital signature", "key encipherment", "client auth"]` 之外的键。
   1. 过期时间/证书有效期：通过 kube-controller-manager 中 `--cluster-signing-duration`
      标志来设置，由其中的签名者实施。
   1. 允许/不允许 CA 位：不允许。

<!-- 
1. `kubernetes.io/kube-apiserver-client-kubelet`: signs client certificates that will be honored as client certificates by the
   API server.
   May be auto-approved by {{< glossary_tooltip term_id="kube-controller-manager" >}}.
   1. Trust distribution: signed certificates must be honored as client certificates by the API server. The CA bundle
      is not distributed by any other means.
   1. Permitted subjects - organizations are exactly `["system:nodes"]`, common name starts with "`system:node:`".
   1. Permitted x509 extensions - honors key usage extensions, forbids subjectAltName extensions and drops other extensions.
   1. Permitted key usages - exactly `["key encipherment", "digital signature", "client auth"]`.
   1. Expiration/certificate lifetime - set by the `--cluster-signing-duration` option for the
      kube-controller-manager implementation of this signer.
   1. CA bit allowed/disallowed - not allowed.
-->
2. `kubernetes.io/kube-apiserver-client-kubelet`: 签名的证书将被 kube-apiserver 视为客户证书。
   {{< glossary_tooltip term_id="kube-controller-manager" >}} 可以自动批准它。

   1. 信任分发：签名的证书将被 API 服务器视为客户端证书。CA 证书包不通过任何其他方式分发。
   1. 许可的主体：组织名必须是 `["system:nodes"]`，用户名以 "`system:node:`" 开头
   1. 许可的 x509 扩展：允许 key usage 扩展，禁用 subjectAltName 扩展，并删除其他扩展。
   1. 许可的密钥用途：必须是 `["key encipherment", "digital signature", "client auth"]`
   1. 过期时间/证书有效期：通过 kube-controller-manager 中签名者的实现所对应的标志
      `--cluster-signing-duration` 来设置。
   1. 允许/不允许 CA 位：不允许。

<!-- 
1. `kubernetes.io/kubelet-serving`: signs serving certificates that are honored as a valid kubelet serving certificate
   by the API server, but has no other guarantees.
   Never auto-approved by {{< glossary_tooltip term_id="kube-controller-manager" >}}.
   1. Trust distribution: signed certificates must be honored by the kube-apiserver as valid to terminate connections to a kubelet. The CA bundle is not distributed by any other means.
   1. Permitted subjects - organizations are exactly `["system:nodes"]`, common name starts with "`system:node:`".
   1. Permitted x509 extensions - honors key usage and DNSName/IPAddress subjectAltName extensions, forbids EmailAddress and
      URI subjectAltName extensions, drops other extensions. At least one DNS or IP subjectAltName must be present.
   1. Permitted key usages - exactly `["key encipherment", "digital signature", "server auth"]`.
   1. Expiration/certificate lifetime - minimum of CSR signer or request.
   1. CA bit allowed/disallowed - not allowed.
-->
3. `kubernetes.io/kubelet-serving`: 签名服务证书，该服务证书被 API 服务器视为有效的 kubelet 服务证书，
   但没有其他保证。{{< glossary_tooltip term_id="kube-controller-manager" >}} 不会自动批准它。
   1. 信任分发：签名的证书必须被 kube-apiserver 认可，可有效的中止 kubelet 连接。CA 证书包不通过任何其他方式分发。
   1. 许可的主体：组织名必须是 `["system:nodes"]`，用户名以 "`system:node:`" 开头
   1. 许可的 x509 扩展：允许 key usage、DNSName/IPAddress subjectAltName 等扩展，
      禁止  EmailAddress、URI subjectAltName 等扩展，并丢弃其他扩展。
      至少有一个 DNS 或 IP 的 SubjectAltName 存在。
   1. 许可的密钥用途：必须是 `["key encipherment", "digital signature", "client auth"]`
   1. 过期日期/证书生命期：通过 kube-controller-manager 中签名者的实现所对应的标志
      `--cluster-signing-duration` 来设置。
   1. 允许/不允许 CA 位：不允许。

<!-- 
1. `kubernetes.io/legacy-unknown`:  has no guarantees for trust at all. Some third-party distributions of Kubernetes
   may honor client certificates signed by it. The stable CertificateSigningRequest API (version `certificates.k8s.io/v1` and later)
   does not allow to set the `signerName` as `kubernetes.io/legacy-unknown`.
   Never auto-approved by {{< glossary_tooltip term_id="kube-controller-manager" >}}.
   1. Trust distribution: None.  There is no standard trust or distribution for this signer in a Kubernetes cluster.
   1. Permitted subjects - any
   1. Permitted x509 extensions - honors subjectAltName and key usage extensions and discards other extensions.
   1. Permitted key usages - any
   1. Expiration/certificate lifetime - set by the `--cluster-signing-duration` option for the
       kube-controller-manager implementation of this signer.
   1. CA bit allowed/disallowed - not allowed.
-->
4. `kubernetes.io/legacy-unknown`: 不保证信任。Kubernetes 的一些第三方发行版可能会使用它签署的客户端证书。
   稳定版的 CertificateSigningRequest API（`certificates.k8s.io/v1` 以及之后的版本）不允许将
   `signerName` 设置为 `kubernetes.io/legacy-unknown`。
   {{< glossary_tooltip term_id="kube-controller-manager" >}} 不会自动批准这类请求。
   1. 信任分发：没有。这个签名者在 Kubernetes 集群中没有标准的信任或分发。
   1. 许可的主体：全部。
   1. 许可的 x509 扩展：允许 subjectAltName 和 key usage 等扩展，并弃用其他扩展。
   1. 许可的密钥用途：全部。
   1. 过期日期/证书生命期：通过 kube-controller-manager 中签名者的实现所对应的标志
      `--cluster-signing-duration` 来设置。
   1. 允许/不允许 CA 位 - 不允许。

{{< note >}}
<!--
Failures for all of these are only reported in kube-controller-manager logs.
-->
注意：所有这些故障仅在 kube-controller-manager 日志中报告。
{{< /note >}}

<!-- 
Distribution of trust happens out of band for these signers.  Any trust outside of those described above are strictly
coincidental. For instance, some distributions may honor `kubernetes.io/legacy-unknown` as client certificates for the
kube-apiserver, but this is not a standard.
None of these usages are related to ServiceAccount token secrets `.data[ca.crt]` in any way.  That CA bundle is only
guaranteed to verify a connection to the API server using the default service (`kubernetes.default.svc`).
-->
对于这些签名者，信任的分发发生在带外（out of band）。上述信任之外的任何信任都是完全巧合的。
例如，一些发行版可能会将 `kubernetes.io/legacy-unknown` 作为 kube-apiserver 的客户端证书，
但这个做法并不标准。
这些用途都没有以任何方式涉及到 ServiceAccount 中的 Secrets `.data[ca.crt]`。
此 CA 证书包只保证使用默认的服务（`kubernetes.default.svc`）来验证到 API 服务器的连接。

<!-- 
## Authorization

To allow creating a CertificateSigningRequest and retrieving any CertificateSigningRequest:

* Verbs: `create`, `get`, `list`, `watch`, group: `certificates.k8s.io`, resource: `certificatesigningrequests`

For example:
-->
## 鉴权 {#authorization}

授权创建 CertificateSigningRequest 和检索 CertificateSigningRequest:

* verbs（动词）: `create`、`get`、`list`、`watch`, 
  group（组）：`certificates.k8s.io`，
  resources：`certificatesigningrequests`

例如：

{{< codenew file="access/certificate-signing-request/clusterrole-create.yaml" >}}

<!-- 
To allow approving a CertificateSigningRequest:

* Verbs: `get`, `list`, `watch`, group: `certificates.k8s.io`, resource: `certificatesigningrequests`
* Verbs: `update`, group: `certificates.k8s.io`, resource: `certificatesigningrequests/approval`
* Verbs: `approve`, group: `certificates.k8s.io`, resource: `signers`, resourceName: `<signerNameDomain>/<signerNamePath>` or `<signerNameDomain>/*`

For example:
-->
授权批准 CertificateSigningRequest：

* verbs（动词）: `get`、`list`、`watch`，
  group（组）：`certificates.k8s.io`，
  resources（资源）：`certificatesigningrequests`
* verbs（动词）: `update`，
  group（组）：`certificates.k8s.io`，
  resources（资源）：`certificatesigningrequests/approval`
* verbs（动词）：`approve`，
  group（组）：`certificates.k8s.io`，
  resources（资源）：`signers`，
  resourceName：`<signerNameDomain>/<signerNamePath>` 或 `<signerNameDomain>/*`

例如：

{{< codenew file="access/certificate-signing-request/clusterrole-approve.yaml" >}}

<!-- 
To allow signing a CertificateSigningRequest:

* Verbs: `get`, `list`, `watch`, group: `certificates.k8s.io`, resource: `certificatesigningrequests`
* Verbs: `update`, group: `certificates.k8s.io`, resource: `certificatesigningrequests/status`
* Verbs: `sign`, group: `certificates.k8s.io`, resource: `signers`, resourceName: `<signerNameDomain>/<signerNamePath>` or `<signerNameDomain>/*`
-->
授权签名 CertificateSigningRequest：

* verbs（动词）：`get`、`list`、`watch`，
  group（组）：`certificates.k8s.io`，
  resources（资源）：`certificatesigningrequests`
* verbs（动词）：`update`，
  group（组）：`certificates.k8s.io`，
  resources（资源）：`certificatesigningrequests/status`
* verbs（动词）：`sign`，
  group（组）：`certificates.k8s.io`，
  resources（资源）：`signers`，
  resourceName：`<signerNameDomain>/<signerNamePath>` 或 `<signerNameDomain>/*`

{{< codenew file="access/certificate-signing-request/clusterrole-sign.yaml" >}}

<!-- 
## Normal User

A few steps are required in order to get a normal user to be able to
authenticate and invoke an API. First, this user must have certificate issued
by the Kubernetes cluster, and then present that Certificate to the API call
as the Certificate Header or through the kubectl.
-->
## 普通用户 {#normal-user}

为了让普通用户能够通过认证并调用 API，需要执行几个步骤。
首先，该用户必须拥有 Kubernetes 集群签发的证书，
然后将该证书作为 API 调用的 Certificate 头或通过 kubectl 提供。

<!-- 
### Create private key

The following scripts show how to generate PKI private key and CSR. It is
important to set CN and O attribute of the CSR. CN is the name of the user and
O is the group that this user will belong to. You can refer to
[RBAC](/docs/reference/access-authn-authz/rbac/) for standard groups.
-->
### 创建私钥 {#create-private-key}

下面的脚本展示了如何生成 PKI 私钥和 CSR。
设置 CSR 的 CN 和 O 属性很重要。CN 是用户名，O 是该用户归属的组。
你可以参考 [RBAC](/zh/docs/reference/access-authn-authz/rbac/) 了解标准组的信息。

```shell
openssl genrsa -out myuser.key 2048
openssl req -new -key myuser.key -out myuser.csr
```

<!-- 
### Create CertificateSigningRequest

Create a CertificateSigningRequest and submit it to a Kubernetes Cluster via kubectl. 
Below is a script to generate the CertificateSigningRequest.
-->
### 创建 CertificateSigningRequest {#create-certificatesigningrequest}

创建一个 CertificateSigningRequest，并通过 kubectl 将其提交到 Kubernetes 集群。
下面是生成 CertificateSigningRequest 的脚本。

```shell
cat <<EOF | kubectl apply -f -
apiVersion: certificates.k8s.io/v1
kind: CertificateSigningRequest
metadata:
  name: myuser
spec:
  groups:
  - system:authenticated
  request: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURSBSRVFVRVNULS0tLS0KTUlJQ1ZqQ0NBVDRDQVFBd0VURVBNQTBHQTFVRUF3d0dZVzVuWld4aE1JSUJJakFOQmdrcWhraUc5dzBCQVFFRgpBQU9DQVE4QU1JSUJDZ0tDQVFFQTByczhJTHRHdTYxakx2dHhWTTJSVlRWMDNHWlJTWWw0dWluVWo4RElaWjBOCnR2MUZtRVFSd3VoaUZsOFEzcWl0Qm0wMUFSMkNJVXBGd2ZzSjZ4MXF3ckJzVkhZbGlBNVhwRVpZM3ExcGswSDQKM3Z3aGJlK1o2MVNrVHF5SVBYUUwrTWM5T1Nsbm0xb0R2N0NtSkZNMUlMRVI3QTVGZnZKOEdFRjJ6dHBoaUlFMwpub1dtdHNZb3JuT2wzc2lHQ2ZGZzR4Zmd4eW8ybmlneFNVekl1bXNnVm9PM2ttT0x1RVF6cXpkakJ3TFJXbWlECklmMXBMWnoyalVnald4UkhCM1gyWnVVV1d1T09PZnpXM01LaE8ybHEvZi9DdS8wYk83c0x0MCt3U2ZMSU91TFcKcW90blZtRmxMMytqTy82WDNDKzBERHk5aUtwbXJjVDBnWGZLemE1dHJRSURBUUFCb0FBd0RRWUpLb1pJaHZjTgpBUUVMQlFBRGdnRUJBR05WdmVIOGR4ZzNvK21VeVRkbmFjVmQ1N24zSkExdnZEU1JWREkyQTZ1eXN3ZFp1L1BVCkkwZXpZWFV0RVNnSk1IRmQycVVNMjNuNVJsSXJ3R0xuUXFISUh5VStWWHhsdnZsRnpNOVpEWllSTmU3QlJvYXgKQVlEdUI5STZXT3FYbkFvczFqRmxNUG5NbFpqdU5kSGxpT1BjTU1oNndLaTZzZFhpVStHYTJ2RUVLY01jSVUyRgpvU2djUWdMYTk0aEpacGk3ZnNMdm1OQUxoT045UHdNMGM1dVJVejV4T0dGMUtCbWRSeEgvbUNOS2JKYjFRQm1HCkkwYitEUEdaTktXTU0xMzhIQXdoV0tkNjVoVHdYOWl4V3ZHMkh4TG1WQzg0L1BHT0tWQW9FNkpsYWFHdTlQVmkKdjlOSjVaZlZrcXdCd0hKbzZXdk9xVlA3SVFjZmg3d0drWm89Ci0tLS0tRU5EIENFUlRJRklDQVRFIFJFUVVFU1QtLS0tLQo=
  signerName: kubernetes.io/kube-apiserver-client
  usages:
  - client auth
EOF
```

<!-- 
Some points to note:

- `usages` has to be '`client auth`'
- `request` is the base64 encoded value of the CSR file content.
  You can get the content using this command: ```cat myuser.csr | base64 | tr -d "\n"```
-->
需要注意的几点:

- `usage` 字段必须是 '`client auth`'
- `request` 字段是 CSR 文件内容的 base64 编码值。
  要得到该值，可以执行命令 `cat myuser.csr | base64 | tr -d "\n"`。

<!-- 
### Approve certificate signing request

Use kubectl to create a CSR and approve it.

Get the list of CSRs:
-->
### 批准证书签名请求 {#approve-certificate-signing-request}

使用 kubectl 创建 CSR 并批准。

获取 CSR 列表：

```shell
kubectl get csr
```

<!-- 
Approve the CSR:
-->
批准 CSR：

```shell
kubectl certificate approve myuser
```

<!-- 
### Get the certificate

Retrieve the certificate from the CSR.
-->
### 取得证书 {#get-the-certificate}

从 CSR 取得证书：

```shell
kubectl get csr/myuser -o yaml
```

<!-- 
The Certificate value is in Base64-encoded format under `status.certificate`.

Export the issued certificate from the CertificateSigningRequest.

-->
证书的内容使用 base64 编码，存放在字段 `status.certificate`。

从 CertificateSigningRequest 导出颁发的证书。

```
kubectl get csr myuser -o jsonpath='{.status.certificate}'| base64 -d > myuser.crt
```

<!--
### Create Role and Role Binding

With the certificate created. it is time to define the Role and RoleBinding for
this user to access Kubernetes cluster resources.

This is a sample script to create Role for this new user
-->
### 创建角色和角色绑定 {#create-role-and-role-binding}

创建了证书之后，为了让这个用户能访问 Kubernetes 集群资源，现在就要创建
Role 和 RoleBinding 了。

下面是为这个新用户创建 Role 的示例脚本：

```shell
kubectl create role developer --verb=create --verb=get --verb=list --verb=update --verb=delete --resource=pods
```

<!-- 
This is a sample command to create a RoleBinding for this new user:
-->
下面是为这个新用户创建 RoleBinding 的示例命令：

```shell
kubectl create rolebinding developer-binding-myuser --role=developer --user=myuser
```

<!-- 
### Add to kubeconfig

The last step is to add this user into the kubeconfig file.

First, we need to add new credentials:
-->
### 添加到 kubeconfig   {#add-to-kubeconfig}

最后一步是将这个用户添加到 kubeconfig 文件。
我们假设私钥和证书文件存放在 “/home/vagrant/work/” 目录中。

首先，我们需要添加新的凭据：

```shell
kubectl config set-credentials myuser --client-key=myuser.key --client-certificate=myuser.crt --embed-certs=true

```

<!-- 
Then, you need to add the context:
-->
然后，你需要添加上下文：

```shell
kubectl config set-context myuser --cluster=kubernetes --user=myuser
```

<!-- 
To test it, change the context to `myuser`:
-->
来测试一下，把上下文切换为 `myuser`：

```shell
kubectl config use-context myuser
```

<!-- 
## Approval or rejection   {#approval-rejection}

### Control plane automated approval {#approval-rejection-control-plane}

The kube-controller-manager ships with a built-in approver for certificates with
a signerName of `kubernetes.io/kube-apiserver-client-kubelet` that delegates various
permissions on CSRs for node credentials to authorization.
The kube-controller-manager POSTs SubjectAccessReview resources to the API server
in order to check authorization for certificate approval.
-->
## 批准和驳回 {#approval-rejection}

### 控制平面的自动化批准 {#approval-rejection-control-plane}

kube-controller-manager 内建了一个证书批准者，其 signerName 为 
`kubernetes.io/kube-apiserver-client-kubelet`，
该批准者将 CSR 上用于节点凭据的各种权限委托给权威认证机构。
kube-controller-manager 将 SubjectAccessReview 资源发送（POST）到 API 服务器，
以便检验批准证书的授权。

<!-- 
### Approval or rejection using `kubectl` {#approval-rejection-kubectl}

A Kubernetes administrator (with appropriate permissions) can manually approve
(or deny) CertificateSigningRequests by using the `kubectl certificate
approve` and `kubectl certificate deny` commands.

To approve a CSR with kubectl:
-->
### 使用 `kubectl` 批准或驳回   {#approval-rejection-kubectl}

Kubernetes 管理员（拥有足够的权限）可以手工批准（或驳回）CertificateSigningRequests，
此操作使用 `kubectl certificate approve` 和 `kubectl certificate deny` 命令实现。

使用 kubectl 批准一个 CSR：

```shell
kubectl certificate approve <certificate-signing-request-name>
```

<!-- 
Likewise, to deny a CSR: 
-->
同样地，驳回一个 CSR：

```shell
kubectl certificate deny <certificate-signing-request-name>
```

<!-- 
### Approval or rejection using the Kubernetes API {#approval-rejection-api-client}

Users of the REST API can approve CSRs by submitting an UPDATE request to the `approval`
subresource of the CSR to be approved. For example, you could write an
{{< glossary_tooltip term_id="operator-pattern" text="operator" >}} that watches for a particular
kind of CSR and then sends an UPDATE to approve them.

When you make an approval or rejection request, set either the `Approved` or `Denied`
status condition based on the state you determine:

For `Approved` CSRs:
-->
### 使用 Kubernetes API 批准或驳回  {#approval-rejection-api-client}

REST API 的用户可以通过向待批准的 CSR 的 `approval` 子资源提交更新请求来批准 CSR。
例如，你可以编写一个
{{< glossary_tooltip term_id="operator-pattern" text="operator" >}}
来监视特定类型的 CSR，然后发送一个更新来批准它。

当你发出批准或驳回的指令时，根据你期望的状态来选择设置 `Approved` 或 `Denied`。

批准（`Approved`） 的 CSR：

```yaml
apiVersion: certificates.k8s.io/v1
kind: CertificateSigningRequest
...
status:
  conditions:
  - lastUpdateTime: "2020-02-08T11:37:35Z"
    lastTransitionTime: "2020-02-08T11:37:35Z"
    message: Approved by my custom approver controller
    reason: ApprovedByMyPolicy # You can set this to any string
    type: Approved
```
<!-- 
For `Denied` CSRs:
-->
驳回（`Denied`）的 CRS：

```yaml
apiVersion: certificates.k8s.io/v1
kind: CertificateSigningRequest
...
status:
  conditions:
  - lastUpdateTime: "2020-02-08T11:37:35Z"
    lastTransitionTime: "2020-02-08T11:37:35Z"
    message: Denied by my custom approver controller
    reason: DeniedByMyPolicy # You can set this to any string
    type: Denied
```

<!-- 
It's usual to set `status.conditions.reason` to a machine-friendly reason
code using TitleCase; this is a convention but you can set it to anything
you like. If you want to add a note for human consumption, use the
`status.conditions.message` field.
-->
`status.conditions.reason` 字段通常设置为一个首字母大写的对机器友好的原因码;
这是一个命名约定，但你也可以随你的个人喜好设置。
如果你想添加一个供人类使用的注释，那就用 `status.conditions.message`  字段。

<!-- 
## Signing

### Control plane signer {#signer-control-plane}

The Kubernetes control plane implements each of the
[Kubernetes signers](/docs/reference/access-authn-authz/certificate-signing-requests/#kubernetes-signers),
as part of the kube-controller-manager.

Prior to Kubernetes v1.18, the kube-controller-manager would sign any CSRs that
were marked as approved.
-->
## 签名   {#signing}

### 控制平面签名者    {#signer-control-plane}

Kubernetes 控制平面实现了每一个 
[Kubernetes 签名者](/zh/docs/reference/access-authn-authz/certificate-signing-requests/#kubernetes-signers)，
每个签名者的实现都是 kube-controller-manager 的一部分。

{{< note >}}
在Kubernetes v1.18 之前，
kube-controller-manager 签名所有标记为 approved  的 CSR。
{{< /note >}}

<!-- 
### API-based signers {#signer-api}

Users of the REST API can sign CSRs by submitting an UPDATE request to the `status`
subresource of the CSR to be signed.

As part of this request, the `status.certificate` field should be set to contain the
signed certificate. This field contains one or more PEM-encoded certificates.

All PEM blocks must have the "CERTIFICATE" label, contain no headers,
and the encoded data must be a BER-encoded ASN.1 Certificate structure
as described in [section 4 of RFC5280](https://tools.ietf.org/html/rfc5280#section-4.1).

Example certificate content:
-->
### 基于 API 的签名者   {#signer-api}

REST API 的用户可以通过向待签名的 CSR 的 `status` 子资源提交更新请求来对 CSR 进行签名。

作为这个请求的一部分， `status.certificate` 字段应设置为已签名的证书。
此字段可包含一个或多个 PEM 编码的证书。

所有的 PEM 块必须具备 "CERTIFICATE" 标签，且不包含文件头，且编码的数据必须是
[RFC5280 第 4 节](https://tools.ietf.org/html/rfc5280#section-4.1)
中描述的 BER 编码的 ASN.1 证书结构。

```
-----BEGIN CERTIFICATE-----
MIIDgjCCAmqgAwIBAgIUC1N1EJ4Qnsd322BhDPRwmg3b/oAwDQYJKoZIhvcNAQEL
BQAwXDELMAkGA1UEBhMCeHgxCjAIBgNVBAgMAXgxCjAIBgNVBAcMAXgxCjAIBgNV
BAoMAXgxCjAIBgNVBAsMAXgxCzAJBgNVBAMMAmNhMRAwDgYJKoZIhvcNAQkBFgF4
MB4XDTIwMDcwNjIyMDcwMFoXDTI1MDcwNTIyMDcwMFowNzEVMBMGA1UEChMMc3lz
dGVtOm5vZGVzMR4wHAYDVQQDExVzeXN0ZW06bm9kZToxMjcuMC4wLjEwggEiMA0G
CSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDne5X2eQ1JcLZkKvhzCR4Hxl9+ZmU3
+e1zfOywLdoQxrPi+o4hVsUH3q0y52BMa7u1yehHDRSaq9u62cmi5ekgXhXHzGmm
kmW5n0itRECv3SFsSm2DSghRKf0mm6iTYHWDHzUXKdm9lPPWoSOxoR5oqOsm3JEh
Q7Et13wrvTJqBMJo1GTwQuF+HYOku0NF/DLqbZIcpI08yQKyrBgYz2uO51/oNp8a
sTCsV4OUfyHhx2BBLUo4g4SptHFySTBwlpRWBnSjZPOhmN74JcpTLB4J5f4iEeA7
2QytZfADckG4wVkhH3C2EJUmRtFIBVirwDn39GXkSGlnvnMgF3uLZ6zNAgMBAAGj
YTBfMA4GA1UdDwEB/wQEAwIFoDATBgNVHSUEDDAKBggrBgEFBQcDAjAMBgNVHRMB
Af8EAjAAMB0GA1UdDgQWBBTREl2hW54lkQBDeVCcd2f2VSlB1DALBgNVHREEBDAC
ggAwDQYJKoZIhvcNAQELBQADggEBABpZjuIKTq8pCaX8dMEGPWtAykgLsTcD2jYr
L0/TCrqmuaaliUa42jQTt2OVsVP/L8ofFunj/KjpQU0bvKJPLMRKtmxbhXuQCQi1
qCRkp8o93mHvEz3mTUN+D1cfQ2fpsBENLnpS0F4G/JyY2Vrh19/X8+mImMEK5eOy
o0BMby7byUj98WmcUvNCiXbC6F45QTmkwEhMqWns0JZQY+/XeDhEcg+lJvz9Eyo2
aGgPsye1o3DpyXnyfJWAWMhOz7cikS5X2adesbgI86PhEHBXPIJ1v13ZdfCExmdd
M1fLPhLyR54fGaY+7/X8P9AZzPefAkwizeXwe9ii6/a08vWoiE4=
-----END CERTIFICATE-----
```

<!-- 
Non-PEM content may appear before or after the CERTIFICATE PEM blocks and is unvalidated,
to allow for explanatory text as described in section 5.2 of RFC7468.

When encoded in JSON or YAML, this field is base-64 encoded.
A CertificateSigningRequest containing the example certificate above would look like this:
-->
非 PEM 内容可能会出现在证书 PEM 块前后的位置，且未经验证，
以允许使用 RFC7468 第5.2节 中描述的解释性文本。

当使用 JSON 或 YAML 格式时，此字段是 base-64 编码。
包含上述示例证书的 CertificateSigningRequest 如下所示：

```yaml
apiVersion: certificates.k8s.io/v1
kind: CertificateSigningRequest
...
status:
  certificate: "LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JS..."
```

## {{% heading "whatsnext" %}}

<!-- 
* Read [Manage TLS Certificates in a Cluster](/docs/tasks/tls/managing-tls-in-a-cluster/)
* View the source code for the kube-controller-manager built in [signer](https://github.com/kubernetes/kubernetes/blob/32ec6c212ec9415f604ffc1f4c1f29b782968ff1/pkg/controller/certificates/signer/cfssl_signer.go)
* View the source code for the kube-controller-manager built in [approver](https://github.com/kubernetes/kubernetes/blob/32ec6c212ec9415f604ffc1f4c1f29b782968ff1/pkg/controller/certificates/approver/sarapprove.go)
* For details of X.509 itself, refer to [RFC 5280](https://tools.ietf.org/html/rfc5280#section-3.1) section 3.1
* For information on the syntax of PKCS#10 certificate signing requests, refer to [RFC 2986](https://tools.ietf.org/html/rfc2986)
-->
* 参阅 [管理集群中的 TLS 认证](/zh/docs/tasks/tls/managing-tls-in-a-cluster/)
* 查看 kube-controller-manager 中[签名者](https://github.com/kubernetes/kubernetes/blob/32ec6c212ec9415f604ffc1f4c1f29b782968ff1/pkg/controller/certificates/signer/cfssl_signer.go)部分的源代码
* 查看 kube-controller-manager 中[批准者](https://github.com/kubernetes/kubernetes/blob/32ec6c212ec9415f604ffc1f4c1f29b782968ff1/pkg/controller/certificates/approver/sarapprove.go)部分的源代码
* 有关 X.509 本身的详细信息，请参阅 [RFC 5280](https://tools.ietf.org/html/rfc5280#section-3.1) 第3.1节
* 有关 PKCS#10 证书签名请求语法的信息，请参阅 [RFC 2986](https://tools.ietf.org/html/rfc2986)
