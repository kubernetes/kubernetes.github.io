---
title: 配置 kubelet 镜像凭据提供程序
description: 配置 kubelet 的镜像凭据提供程序插件
content_type: task
---

<!-- 
title: Configure a kubelet image credential provider
reviewers:
- liggitt
- cheftako
description: Configure the kubelet's image credential provider plugin
content_type: task
-->

{{< feature-state for_k8s_version="v1.20" state="alpha" >}}

<!-- overview -->

<!-- 
Starting from Kubernetes v1.20, the kubelet can dynamically retrieve credentials for a container image registry
using exec plugins. The kubelet and the exec plugin communicate through stdio (stdin, stdout, and stderr) using
Kubernetes versioned APIs. These plugins allow the kubelet to request credentials for a container registry dynamically
as opposed to storing static credentials on disk. For example, the plugin may talk to a local metadata server to retrieve
short-lived credentials for an image that is being pulled by the kubelet.
-->
从 Kubernetes v1.20 开始，kubelet 可以使用 exec 插件动态检索容器镜像注册中心的凭据。
kubelet 和 exec 插件使用 Kubernetes 版本化 API 通过标准输入输出（标准输入、标准输出和标准错误）通信。
这些插件允许 kubelet 动态请求容器注册中心的凭据，而不是将静态凭据存储在磁盘上。
例如，插件可能会与本地元数据通信，以检索 kubelet 正在拉取的镜像的短期凭据。

<!-- 
You may be interested in using this capability if any of the below are true:

* API calls to a cloud provider service are required to retrieve authentication information for a registry.
* Credentials have short expiration times and requesting new credentials frequently is required.
* Storing registry credentials on disk or in imagePullSecrets is not acceptable.

This guide demonstrates how to configure the kubelet's image credential provider plugin mechanism.
-->
如果以下任一情况属实，你可能对此功能感兴趣：

* 需要调用云提供商的 API 来检索注册中心的身份验证信息。
* 凭据的到期时间很短，需要频繁请求新凭据。
* 将注册中心凭据存储在磁盘或者 imagePullSecret 是不可接受的。

## {{% heading "prerequisites" %}}

<!-- 
* The kubelet image credential provider is introduced in v1.20 as an alpha feature. As with other alpha features,
a feature gate `KubeletCredentialProviders` must be enabled on only the kubelet for the feature to work.
* A working implementation of a credential provider exec plugin. You can build your own plugin or use one provided by cloud providers.
-->
* kubelet 镜像凭证提供程序在 v1.20 版本作为 alpha 功能引入。
  与其他 alpha 功能一样，当前仅当在 kubelet 启动 `KubeletCredentialProviders` 特性门禁才能使该功能正常工作。
* 凭据提供程序 exec 插件的工作实现。你可以构建自己的插件或使用云提供商提供的插件。

<!-- steps -->

<!-- 
## Installing Plugins on Nodes

A credential provider plugin is an executable binary that will be run by the kubelet. Ensure that the plugin binary exists on
every node in your cluster and stored in a known directory. The directory will be required later when configuring kubelet flags.
-->
## 在节点上安装插件  {#installing-plugins-on-nodes}

凭据提供程序插件是将由 kubelet 运行的可执行二进制文件。
确保插件二进制存在于你的集群的每个节点上，并存储在已知目录中。
稍后配置 kubelet 标志需要该目录。

<!-- 
## Configuring the Kubelet

In order to use this feature, the kubelet expects two flags to be set:
* `--image-credential-provider-config` - the path to the credential provider plugin config file.
* `--image-credential-provider-bin-dir` - the path to the directory where credential provider plugin binaries are located.
-->
## 配置 kubelet  {#configuring-the-kubelet}

为了使用这个特性，kubelet 需要设置以下两个标志：
* `--image-credential-provider-config` —— 凭据提供程序插件配置文件的路径。
* `--image-credential-provider-bin-dir` —— 凭据提供程序插件二进制文件所在目录的路径。

<!-- 
### Configure a kubelet credential provider

The configuration file passed into `--image-credential-provider-config` is read by the kubelet to determine which exec plugins
should be invoked for which container images. Here's an example configuration file you may end up using if you are using the [ECR](https://aws.amazon.com/ecr/)-based plugin:
-->
### 配置 kubelet 凭据提供程序  {#configure-a-kubelet-credential-provider}

kubelet 会读取传入 `--image-credential-provider-config` 的配置文件文件，
以确定应该为哪些容器镜像调用哪些 exec 插件。
如果你正在使用基于 [ECR](https://aws.amazon.com/ecr/) 插件，
这里有个样例配置文件你可能最终会使用到：

```yaml
kind: CredentialProviderConfig
apiVersion: kubelet.config.k8s.io/v1alpha1
# providers 是将由 kubelet 启用的凭证提供程序插件列表。
# 多个提供程序可能与单个镜像匹配，在这种情况下，来自所有提供程序的凭据将返回到 kubelet。
# 如果为单个镜像调用多个提供程序，则结果会合并。
# 如果提供程序返回重叠的身份验证密钥，则使用提供程序列表中较早的值。
providers:
  # name 是凭据提供程序的必需名称。 
  # 它必须与 kubelet 看到的提供程序可执行文件的名称相匹配。
  # 可执行文件必须在 kubelet 的 bin 目录中
  # （由 --image-credential-provider-bin-dir 标志设置）。
  - name: ecr
    # matchImages 是一个必需的字符串列表，用于匹配镜像以确定是否应调用此提供程序。
    # 如果其中一个字符串与 kubelet 请求的镜像相匹配，则该插件将被调用并有机会提供凭据。
    # 镜像应包含注册域和 URL 路径。
    #
    # matchImages 中的每个条目都是一个模式，可以选择包含端口和路径。
    # 通配符可以在域中使用，但不能在端口或路径中使用。
    # 支持通配符作为子域（例如“*.k8s.io”或“k8s.*.io”）和顶级域（例如“k8s.*”）。
    # 还支持匹配部分子域，如“app*.k8s.io”。
    # 每个通配符只能匹配一个子域段，因此 *.io 不匹配 *.k8s.io。
    #
    # 当以下所有条件都为真时，镜像和 matchImage 之间存在匹配：
    # - 两者都包含相同数量的域部分并且每个部分都匹配。
    # - imageMatch 的 URL 路径必须是目标镜像 URL 路径的前缀。
    # - 如果 imageMatch 包含端口，则该端口也必须在图像中匹配。
    #
    # matchImages 的示例值：
    # - 123456789.dkr.ecr.us-east-1.amazonaws.com
    # - *.azurecr.io
    # - gcr.io
    # - *.*.registry.io
    # - registry.io:8080/path
    matchImages:
    - "*.dkr.ecr.*.amazonaws.com"
    - "*.dkr.ecr.*.amazonaws.cn"
    - "*.dkr.ecr-fips.*.amazonaws.com"
    - "*.dkr.ecr.us-iso-east-1.c2s.ic.gov"
    - "*.dkr.ecr.us-isob-east-1.sc2s.sgov.gov"
    # defaultCacheDuration 是插件将在内存中缓存凭据的默认持续时间
    # 如果插件响应中未提供缓存持续时间。此字段是必需的。
    defaultCacheDuration: "12h"
    # exec CredentialProviderRequest 的必需输入版本。
    # 返回的 CredentialProviderResponse 必须使用与输入相同的编码版本。当前支持的值为：
    # - credentialprovider.kubelet.k8s.io/v1alpha1
    apiVersion: credentialprovider.kubelet.k8s.io/v1alpha1
    # 执行命令时传递给命令的参数。
    # +可选
    args:
    - get-credentials
    # env 定义了额外的环境变量以暴露给进程。
    # 这些与主机环境以及 client-go 用于将参数传递给插件的变量结合在一起。
    # +可选
    env:
    - name: AWS_PROFILE
      value: example_profile
```

<!-- 
The `providers` field is a list of enabled plugins used by the kubelet. Each entry has a few required fields:
* `name`: the name of the plugin which MUST match the name of the executable binary that exists in the directory passed into `--image-credential-provider-bin-dir`.
* `matchImages`: a list of strings used to match against images in order to determine if this provider should be invoked. More on this below.
* `defaultCacheDuration`: the default duration the kubelet will cache credentials in-memory if a cache duration was not specified by the plugin.
* `apiVersion`: the api version that the kubelet and the exec plugin will use when communicating.

Each credential provider can also be given optional args and environment variables as well. Consult the plugin implementors to determine what set of arguments and environment variables are required for a given plugin.
-->
`providers` 字段是 kubelet 使用的已启用插件列表。每个条目都有几个必填字段：
* `name`：插件的名称，必须与传入`--image-credential-provider-bin-dir`
  的目录中存在的可执行二进制文件的名称相匹配。
* `matchImages`：用于匹配图像以确定是否应调用此提供程序的字符串列表。更多相关信息如下。
* `defaultCacheDuration`：如果插件未指定缓存持续时间，kubelet 将在内存中缓存凭据的默认持续时间。
* `apiVersion`：kubelet 和 exec 插件在通信时将使用的 api 版本。

每个凭证提供程序也可以被赋予可选的参数和环境变量。
咨询插件实现者以确定给定插件需要哪些参数和环境变量集。

<!-- 
#### Configure image matching

The `matchImages` field for each credential provider is used by the kubelet to determine whether a plugin should be invoked
for a given image that a Pod is using. Each entry in `matchImages` is an image pattern which can optionally contain a port and a path.
Globs can be used in the domain, but not in the port or the path. Globs are supported as subdomains like `*.k8s.io` or `k8s.*.io`,
and top-level domains such as `k8s.*`. Matching partial subdomains like `app*.k8s.io` is also supported. Each glob can only match
a single subdomain segment, so `*.io` does NOT match `*.k8s.io`.
-->
#### 配置镜像匹配  {#configure-image-matching}

kubelet 使用每个凭证提供程序的 `matchImages` 字段来确定是否应该为 Pod 正在使用的给定镜像调用插件。
`matchImages` 中的每个条目都是一个镜像模式，可以选择包含端口和路径。
通配符可以在域中使用，但不能在端口或路径中使用。
支持通配符作为子域，如 `*.k8s.io` 或 `k8s.*.io`，以及顶级域，如 `k8s.*`。
还支持匹配部分子域，如 `app*.k8s.io`。每个通配符只能匹配一个子域段，
因此 `*.io` 不匹配 `*.k8s.io`。

<!-- 
A match exists between an image name and a `matchImage` entry when all of the below are true:

* Both contain the same number of domain parts and each part matches.
* The URL path of match image must be a prefix of the target image URL path.
* If the imageMatch contains a port, then the port must match in the image as well.

Some example values of `matchImages` patterns are:
-->
当以下所有条件都为真时，镜像名称和 `matchImage` 条目之间存在匹配：

* 两者都包含相同数量的域部分并且每个部分都匹配。
* 匹配图片的 URL 路径必须是目标图片 URL 路径的前缀。
* 如果 imageMatch 包含端口，则该端口也必须在镜像中匹配。

`matchImages` 模式的一些示例值：
* `123456789.dkr.ecr.us-east-1.amazonaws.com`
* `*.azurecr.io`
* `gcr.io`
* `*.*.registry.io`
* `foo.registry.io:8080/path`
