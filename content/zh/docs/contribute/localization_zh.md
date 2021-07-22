---
title: 中文本地化样式指南
content_type: concept
---

<!-- overview -->

本节详述文档中文本地化过程中须注意的事项。
这里列举的内容包含了*中文本地化小组*早期给出的指导性建议和后续实践过程中积累的经验。
在阅读、贡献、评阅中文本地化文档的过程中，如果对本文的指南有任何改进建议，
都请直接提出 PR。我们欢迎任何形式的补充和更正！

<!-- body -->

## 一般规定

本节列举一些译文中常见问题和约定。

### 英文原文的保留

为便于译文审查和变更追踪，所有中文本地化 Markdown 文件中都应使用 HTML 注释
`<!--` 和 `-->` 将英文原文逐段注释起来，后跟对应中文译文。例如：

```
<!--
This is English text ... 
-->
中文译文对应 ...
```

不建议采用下面的方式注释英文段落，除非英文段落非常非常短：

```
<!-- This is English text ...  -->
中文译文对应 ...

```

无论英文原文或者中文译文中，都不要保留过多的、不必要的空白行。

#### 段落划分

请避免大段大段地注释和翻译。一般而言，每段翻译可对应两三个自然段。
段落过长会导致译文很难评阅。但也不必每个段落都单独翻译。例如：

```
<!--
## Overview

### Concept

First paragraph, not very long.
-->
## 概述 {#overview}

### 概念 {#concept}

第一段落，不太长。
```

以下风格是不必要的：

```
<!--
## Overview
-->
## 概述 {#overview}

<!--
### Concept
-->
### 概念 {#concept}

<!--
First paragraph, not very long.
-->
第一段落，不太长。
```

#### 编号列表的处理

编号列表需要编号的连续性，处理不好的话可能导致输出结果错误。
由于有些列表可能很长，一次性等将整个列表注释掉再翻译也不现实。
推荐采用下面的方式。

假定英文为：

```
1. Prepare something
1. Followed by a long step with code snippets and notes ...
   this is a really long item
1. Another long item ...
   .. continues here
1. Almost done ...
```

本地化处理：

```
<!--
1. Prepare something
-->
1. 准备工作，...
   这里每行缩进 3 个空格

<!--
1. Followed by a long step with code snippets and notes ...
   this is a really long item
-->
2. 这里是第二个编号，但需要显式给出数字，不能沿用英文编号。
   缩进内容同上，3 个空格。
   即使有三个反引号的代码段或者短代码，都按 3 个空格缩进。

<!--
1. Another long item ...
   .. continues here
1. Almost done ...
-->
3. 继续列表。

   如果条目有多个段落，也要
   保持缩进对齐以确保排版正确。

4. 列表终于结束
```

#### Frontmatter 的处理

页面中的 Frontmatter 指的是文件头的两个 `---` 中间的部分。
对这一部分，解析器有特殊处理，因此不能将英文部分放在前面，中文跟在后面。
需要将二者顺序颠倒。如下所示：

```
---
title: 译文标题
type: concept
weight: 30
---

<!--
title: English title
type: concept
reviewers:
  - john
  - doe
weight: 30
-->
```

这里要注意的是：

- `title`、`description` 的内容要翻译，其他字段一般不必（甚至不可）翻译。
- `reviewers` 部分要删除，不然中文译文会转给英文作者来审阅。


#### 短代码（shortcode）处理

通过 HTML 注释的短代码仍会被运行，因此需要额外小心。建议处理方式：

```
<!--
English text
-->
{{</* note */>}}
中文译文
{{</* /note */>}}
```

评阅人应该不难理解中英文段落的对应关系。但是如果采用下面的方式，
则会出现两个 `note`，因此需要避免。这是因为被注释起来的短代码仍会起作用！

```
<!--
{{</* note */>}}
English text
{{</* /note */>}}
-->
{{</* note */>}}
中文译文
{{</* /note */>}}
```

### 译与不译

#### 资源名称或字段不译

根据英文原文写作风格约定【也在持续修订改进】，对 Kubernetes 中的 API
资源均按其规范中所给的大小写形式书写，例如：英文中会使用 Deployment 而不是
deployment 来表示名为 "Deployment" 的 API 资源类型和对象实例。

对这类词语，一般不应翻译。

{{< note >}}
英文原文在这方面并不严谨，译者或中文译文的评阅者要非常留心。
比如 Secret 资源，很多时候被误写为 secret。
这时在本地化版本中一定不能译为“秘密”，以免与原文的语义不符。
{{< /note >}}

#### 代码中的注释

一般而言，代码中的注释需要翻译，包括存放在 `content/zh/examples/`
目录下的清单文件中的注释。


#### 出站链接

如果超级链接的目标是 Kubernetes 网站之外的纯英文网页，链接中的内容*可以*不翻译。
例如：

```
<!--
Please check [installation caveats](https://acme.com/docs/v1/caveats) ...
-->
请参阅 [installation caveats](https://acme.com/docs/v1/caveats) ...
```

注意，这里的 `installation` 与 `参阅` 之间留白，因为解析后属于中英文混排的情况。

### 标点符号

译文中标点符号要使用全角字符，除非以下两种情况：

- 标点符号是英文命令的一部分；
- 标点符号是 Markdown 语法的一部分。

英文排比句式中采用的逗号，在译文中要使用顿号代替，以便符合中文书写习惯。

## 更新译文

由于整个文档站点会随着 Kubernetes 项目的开发进展而演化，英文版本的网站内容会不断更新。
鉴于中文站点的基本翻译工作在 1.19 版本已完成，
从 1.20 版本开始本地化的工作会集中在追踪英文内容变化上。

为确保准确跟踪中文化版本与英文版本之间的差异，中文内容的 PR 所包含的每个页面都必须是“最新的”。
这里的“最新”指的是对应的英文页面中的更改已全部同步到中文页面。
如果某中文 PR 中包含对 `content/zh/docs/foo/bar.md` 的更改，且文件 `bar.md`
的上次更改日期是 `2020-10-01 01:02:03 UTC`，对应 GIT 标签 `abcd1234`，
则 `bar.md` 应包含自 `abcd1234` 以来 `content/en/docs/foo/bar.md` 的所有变更，
否则视此 PR 为不完整 PR，会破坏我们对上游变更的跟踪。

这一要求适用于所有更改，包括拼写错误、格式更正、链接修订等等。要查看文件
`bar.md` 上次提交以来发生的所有变更，可使用：

```
./scripts/lsync.sh content/zh/docs/foo/bar.md
```

## 关于链接

### 链接锚点

英文 Markdown 中的各级标题会自动生成锚点，以便从其他页面中链接。
在译为中文后，相应的链接必然会失效。为防止这类问题，
建议在翻译各级标题时，使用英文方式显式给出链接锚点。例如：

```
<!--
### Create a Pod
-->
### 创建 Pod   {#create-a-pod}
```

此类问题对于概念部分的页面最为突出，需要格外注意。


### 中文链接目标

由于大部分页面已经完成中文本地化，这意味着很多链接可以使用中文版本作为目标。
例如：

```
<!--
For more information, please check [volumes](/docs/concepts/storage/)
...
-->
更多的信息可参考[卷](/zh/docs/concepts/storage/)页面。
```

如果对应目标页面尚未本地化，建议登记一个 Issue。

{{< note >}}
Website 的仓库中 `scripts/linkchecker.py` 是一个工具，可用来检查页面中的链接。
例如，下面的命令检查中文本地化目录 `/content/zh/docs/concepts/containers/`
中所有 Markdown 文件中的链接合法性：

```
./scripts/linkchecker.py -l zh -f /docs/concepts/containers/**/*.md
```
{{< /note >}}

## 排版格式

以下为译文 Markdown 排版格式要求：

- 中英文之间留一个空格
  * 这里的“英文”包括以英文呈现的超级链接
  * 这里的中文、英文都不包括标点符号
- 译文 Markdown 中不要使用长行，应适当断行。
  * 可根据需要在 80-120 列断行
  * 最好结合句子的边界断行，即一句话在一行，不必留几个字转到下一行
  * 不要在两个中文字符中间断行，因为这样会造成中文字符中间显示一个多余空格，
    如果句子太长，可以从中文与非中文符号之间断行
  * 超级链接文字一般较长，可独立成行

{{< warning >}}
我们注意到有些贡献者可能使用了某种自动化工具，在 Markdown 英文原文中自动添加空格。
虽然这些工具可一定程度提高效率，仍然需要提请作者注意，某些工具所作的转换可能是不对的，
例如将 `foo=bar` 转换为 `foo = bar`、将 `），另一些文字` 转换为 `） ，另一些文字` 等等，
甚至将超级链接中的半角井号（`#`）转换为全角，导致链接失效。
{{< /warning >}}

英文中 "you" 翻译成 "你" 不必是 “您"。
文章内的链接用英文，例如 (#deploying)，在对应的标题上后面加上 {#deploying}


## 术语

### 术语拼写

按中文译文习惯，尽量不要在中文译文中使用首字母小写的拼写。例如：

```
列举所有 pods，查看其创建时间 ...       [No]
列举所有 Pod，查看其创建时间 ...        [Yes]
```

*第一次*使用首字母缩写时，应标注其全称和中文译文。例如：

```
你可以创建一个 Pod 干扰预算（Pod Disruption Budget，PDB）来解决这一问题。
所谓 PDB 实际上是 ...
```

对于某些特定于 Kubernetes 语境的术语，也应在*第一次*出现在页面中时给出其英文原文，
以便读者对照阅读。例如：

```
镜像策略（Image Policy）用来控制集群可拉取的镜像仓库（Image Registry）源。
```

### 术语对照

本节列举常见术语的统一译法。除极个别情况，对于专业术语应使用本节所列举的译法：

- API Server，API 服务器
- GA (general availability)，正式发布
- addons，插件
- admission controller，准入控制器
- affinity，亲和性
- annotation，注解
- anti-affinity，反亲和性
- attach，挂接
- autoscale，自动扩缩容
- bearer token，持有者令牌
- capabilities权能字
  * 当泛指某主体执行某操作的能力时，可直译为“能力”
  * 当特指 Linux 操作系统上的[权限控制](https://man7.org/linux/man-pages/man7/capabilities.7.html)机制时，译为“权能字”
- certificate authority，证书机构
- certificate，证书
- claim，申领
- cloud provider
  * 当用来指代下层云服务的提供厂商时，译为“云服务供应商”
  * 当特指 Kubernetes 中对不同云平台的支持时，可酌情译为“云驱动”
- cluster，集群
- condition
  * 大多数上下文中，可译为“条件”
  * 在讨论 Kubernetes 资源的 condition 时，应译为“状况”
- control loop，控制回路
- control plane，控制平面，或控制面
- controller，控制器
- controller manager，控制器管理器
- credential，登录凭据，凭据
- custom，定制，或自定义
- daemon，守护进程
- dashboard，仪表板
- dependent，附属或附属者
- deprecated，已弃用的
- deprecation，弃用
- desired，预期的
- desired state，预期状态
- detach，解除挂接
- distribution，发行版本
- disruption，干扰（请勿译为“中断”）
- drain，腾空
- endpoint，端点
- egress，出站
- evict，驱逐
- eviction，驱逐
- feature gate，特性门控
- federation，联邦
- flags，命令行参数，参数
- grace period，宽限期限
- graceful termination，体面终止
- hairpin，发夹
- hash，哈希
- headless service，无头服务
- healthcheck，健康检查
- hook，回调
- host，主机，宿主机
- hosting，托管
- idempotent，幂等的
- image，镜像
- image registry，镜像仓库
- ingress，入站
- init container，Init 容器
- key
  * 在加密解密、安全认证上下文中，译为密钥
  * 在配置文件、数据结构上下文中，译为主键，或键
- label，标签
- label selector，标签选择算符
- lifecycle，生命周期
- limit，限制，限值
- liveness probe，存活态探针
- load balance，负载均衡
- load balancer，负载均衡器
- log flush，清刷日志数据
- loopback，本地回路
- manifest，清单，清单文件
- master node，主控节点
- metric
  * 用来指代被测量的数据源时，译为指标
  * 用来指代测量观测结果时，译为度量值
- mount，挂载
- namespace，名字空间，命名空间
- orphans，孤立或孤立的
- override，覆写
- owner，所有者，属主
- pending，悬决的
- persistent volume，持久卷
- persistent volume claim，持久卷申领
- pipeline，流水线
- prerequisites，依赖，前提条件（根据上下文判断）
- priority class，优先级类
- probe，探针
- provision，供应
- pull，拉取
- push，推送
- quota，配额
- readiness probe，就绪态探针
- replica，副本
- repo，仓库
- repository，仓库
- revision，修订版本
- role，角色
- role binding，角色绑定
- rolling update，滚动更新
- rollout，上线
- rotate，轮换
- round robin，轮转
- runtime，运行时
- scale in/out，横向缩容/扩容
- scale up/down，纵向扩容/缩容
- scale
  * 做动词用时，译为“扩缩”，或者“改变...的规模”
  * 做名词用时，译为“规模”
- scheduler，调度器
- service，服务
- service account，服务账号
- service account token，服务账号令牌
- service discovery，服务发现
- service mesh，服务网格
- session，会话
- sidecar，边车
- skew，偏移
- spec，规约
- specification，规约
- startup probe，启动探针
- stateless，无状态的
- static pod，静态 Pod
- stderr，标准错误输出
- stdin，标准输入
- stdout，标准输出
- storage class，存储类
- taint，污点
- threshold，阈值
- toleration，容忍度
- topology，拓扑
- topology spread constraint，拓扑分布约束
- traffic，流量
  * 在某些上下文中，可以根据情况译为“服务请求”，“服务响应”
- unmount，卸载
- use case，用例，使用场景
- volume，卷
- worker node，工作节点
- workload，工作负载
