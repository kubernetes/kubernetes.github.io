---
title: Kubernetes 弃用策略
content_type: concept
weight: 40
---
<!--
reviewers:
- bgrant0607
- lavalamp
- thockin
title: Kubernetes Deprecation Policy
content_type: concept
weight: 40
-->

<!-- overview -->
<!--
This document details the deprecation policy for various facets of the system.
-->
本文档详细解释系统中各个层面的弃用策略（Deprecation Policy）。

<!-- body -->
<!--
Kubernetes is a large system with many components and many contributors.  As
with any such software, the feature set naturally evolves over time, and
sometimes a feature may need to be removed. This could include an API, a flag,
or even an entire feature. To avoid breaking existing users, Kubernetes follows
a deprecation policy for aspects of the system that are slated to be removed.
-->
Kubernetes 是一个组件众多、贡献者人数众多的大系统。
就像很多类似的软件，所提供的功能特性集合会随着时间推移而自然发生变化，
而且有时候某个功能特性可能需要被去除。被去除的可能是一个 API、一个参数标志或者
甚至某整个功能特性。为了避免影响到现有用户，Kubernetes 对于其中渐次移除
的各个方面规定了一种弃用策略并遵从此策略。

<!--
## Deprecating parts of the API

Since Kubernetes is an API-driven system, the API has evolved over time to
reflect the evolving understanding of the problem space. The Kubernetes API is
actually a set of APIs, called "API groups", and each API group is
independently versioned.  [API versions](/docs/reference/using-api/#api-versioning) fall
into 3 main tracks, each of which has different policies for deprecation:
-->
## 弃用 API 的一部分  {#deprecating-parts-of-the-api}

由于 Kubernetes 是一个 API 驱动的系统，API 会随着时间推移而演化，以反映
人们对问题空间的认识的变化。Kubernetes API 实际上是一个 API 集合，其中每个
成员称作“API 组（API Group）”，并且每个 API 组都是独立管理版本的。
[API 版本](/zh/docs/reference/using-api/#api-versioning)会有
三类，每类有不同的废弃策略：

<!--
| Example  | Track                            |
|----------|----------------------------------|
| v1       | GA (generally available, stable) |
| v1beta1  | Beta (pre-release)               |
| v1alpha1 | Alpha (experimental)             |
-->
| 示例     | 分类                             |
|----------|----------------------------------|
| v1       | 正式发布（Generally available，GA，稳定版本） |
| v1beta1  | Beta （预发布）|
| v1alpha1 | Alpha （试验性） |

<!--
A given release of Kubernetes can support any number of API groups and any
number of versions of each.

The following rules govern the deprecation of elements of the API.  This
includes:
-->
给定的 Kubernetes 发布版本中可以支持任意数量的 API 组，且每组可以包含
任意个数的版本。

下面的规则负责指导 API 元素的弃用，具体元素包括：

<!--
   * REST resources (aka API objects)
   * Fields of REST resources
   * Annotations on REST resources, including "beta" annotations but not
     including "alpha" annotations.
   * Enumerated or constant values
   * Component config structures
-->
* REST 资源（也即 API 对象）
* REST 资源的字段
* REST 资源的注解，包含“beta”类注解但不包含“alpha”类注解
* 枚举值或者常数值
* 组件配置结构

<!--
These rules are enforced between official releases, not between
arbitrary commits to master or release branches.

**Rule #1: API elements may only be removed by incrementing the version of the
API group.**

Once an API element has been added to an API group at a particular version, it
can not be removed from that version or have its behavior significantly
changed, regardless of track.
-->
以下是跨正式发布版本时要实施的规则，不适用于对 master 或发布分支上
不同提交之间的变化。

**规则 #1：只能在增加 API 组版本号时删除 API 元素。**

一旦在某个特定 API 组版本中添加了 API 元素，则该元素不可从该版本中删除，
且其行为也不能大幅度地变化，无论属于哪一类（GA、Alpha 或 Beta）。

<!--
For historical reasons, there are 2 "monolithic" API groups - "core" (no
group name) and "extensions".  Resources will incrementally be moved from these
legacy API groups into more domain-specific API groups.
-->
{{< note >}}
由于历史原因，Kubernetes 中存在两个“单体式（Monolithic）”API 组 -
“core”（无组名）和“extensions”。这两个遗留 API 组中的资源会被逐渐迁移到
更为特定领域的 API 组中。
{{< /note >}}

<!--
**Rule #2: API objects must be able to round-trip between API versions in a given
release without information loss, with the exception of whole REST resources
that do not exist in some versions.**
-->
**规则 #2：在给定的发布版本中，API 对象必须能够在不同的 API 版本之间来回
转换且不造成信息丢失，除非整个 REST 资源在某些版本中完全不存在。**

<!--
For example, an object can be written as v1 and then read back as v2 and
converted to v1, and the resulting v1 resource will be identical to the
original.  The representation in v2 might be different from v1, but the system
knows how to convert between them in both directions.  Additionally, any new
field added in v2 must be able to round-trip to v1 and back, which means v1
might have to add an equivalent field or represent it as an annotation.
-->
例如，一个对象可被用 v1 来写入之后用 v2 来读出并转换为 v1，所得到的 v1 必须
与原来的 v1 对象完全相同。v2 中的表现形式可能与 v1 不同，但系统知道如何
在两个版本之间执行双向转换。
此外，v2 中添加的所有新字段都必须能够转换为 v1 再转换回来。这意味着 v1 必须
添加一个新的等效字段或者将其表现为一个注解。

<!--
**Rule #3: An API version in a given track may not be deprecated until a new
API version at least as stable is released.**

GA API versions can replace GA API versions as well as beta and alpha API
versions.  Beta API versions *may not* replace GA API versions.
-->
**规则 #3：给定类别的 API 版本在新的、稳定性未降低的 API 版本发布之前不可被废弃。**

一个正式发布的（GA）API 版本可替换现有的正式 API 版本或 alpha、beta API 版本。
Beta API 版本 *不可以* 替代正式的 API 版本。

<!--
**Rule #4a: Other than the most recent API versions in each track, older API
versions must be supported after their announced deprecation for a duration of
no less than:**

   * **GA: 12 months or 3 releases (whichever is longer)**
   * **Beta: 9 months or 3 releases (whichever is longer)**
   * **Alpha: 0 releases**

This covers the [maximum supported version skew of 2 releases](/docs/setup/release/version-skew-policy/).
-->
**规则 #4a：除了每类 API 版本中的最新版本，旧的 API 版本在其被宣布被废弃之后
至少以下时长内仍需被支持：**

   * **GA：12 个月或者 3 个发布版本（取其较长者）**
   * **Beta: 9 个月或者 3 个发布版本（取其较长者）**
   * **Alpha: 0 个发布版本**

这里也包含了关于[最大支持 2 个发布版本的版本偏差](/zh/docs/setup/release/version-skew-policy/)
的约定。

<!--
Until [#52185](https://github.com/kubernetes/kubernetes/issues/52185) is
resolved, no API versions that have been persisted to storage may be removed.
Serving REST endpoints for those versions may be disabled (subject to the
deprecation timelines in this document), but the API server must remain capable
of decoding/converting previously persisted data from storage.
-->
{{< note >}}
在 [#52185](https://github.com/kubernetes/kubernetes/issues/52185) 被解决之前，
已经被保存到持久性存储中的 API 版本都不可以被去除。
你可以禁止这些版本所对应的 REST 末端（在符合本文中弃用时间线的前提下），
但是 API 服务器必须仍能解析和转换存储中以前写入的数据。
{{< /note >}}

<!--
**Rule #4b: The "preferred" API version and the "storage version" for a given
group may not advance until after a release has been made that supports both the
new version and the previous version**
-->
**规则 #4b：标记为“preferred（优选的）” API 版本和给定 API 组的
“storage version（存储版本）”在既支持老版本也支持新版本的 Kubernetes 发布
版本出来以前不可以提升其版本号。**

<!--
Users must be able to upgrade to a new release of Kubernetes and then roll back
to a previous release, without converting anything to the new API version or
suffering breakages (unless they explicitly used features only available in the
newer version).  This is particularly evident in the stored representation of
objects.

All of this is best illustrated by examples.  Imagine a Kubernetes release,
version X, which introduces a new API group.  A new Kubernetes release is made
every approximately 3 months (4 per year).  The following table describes which
API versions are supported in a series of subsequent releases.
-->
用户必须能够升级到 Kubernetes 新的发行版本，之后再回滚到前一个发行版本，且
整个过程中无需针对新的 API 版本做任何转换，也不允许出现功能损坏的情况，
除非用户显式地使用了仅在较新版本中才存在的功能特性。
就对象的存储表示而言，这一点尤其是不言自明的。

以上所有规则最好通过例子来说明。假定现有 Kubernetes 发行版本为 X，其中引入了
新的 API 组。大约每隔 3 个月会有一个新的 Kubernetes 版本被发布（每年 4 个版本）。
下面的表格描述了在一系列后续的发布版本中哪些 API 版本是受支持的。

<table>
  <thead>
    <tr>
      <!-- th>Release</th>
      <th>API Versions</th>
      <th>Preferred/Storage Version</th>
      <th>Notes</th -->
      <th>发布版本</th>
      <th>API 版本</th>
      <th>优选/存储版本</th>
      <th>注释</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>X</td>
      <td>v1alpha1</td>
      <td>v1alpha1</td>
      <td></td>
    </tr>
    <tr>
      <td>X+1</td>
      <td>v1alpha2</td>
      <td>v1alpha2</td>
      <td>
        <ul>
           <!-- li>v1alpha1 is removed, "action required" relnote</li -->
           <li>v1alpha1 被去除，发布说明中会包含 "action required（采取行动）" 说明</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td>X+2</td>
      <td>v1beta1</td>
      <td>v1beta1</td>
      <td>
        <ul>
          <!-- li>v1alpha2 is removed, "action required" relnote</li -->
          <li>v1alpha2 被去除，发布说明中包含对应的 "action required（采取行动）" 说明</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td>X+3</td>
      <!-- td>v1beta2, v1beta1 (deprecated)</td -->
      <td>v1beta2、v1beta1（已弃用）</td>
      <td>v1beta1</td>
      <td>
        <ul>
          <!-- li>v1beta1 is deprecated, "action required" relnote</li -->
          <li>v1beta1 被弃用，发布说明中包含对应的 "action required（采取行动）" 说明</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td>X+4</td>
      <!-- td>v1beta2, v1beta1 (deprecated)</td -->
      <td>v1beta2、v1beta1（已弃用）</td>
      <td>v1beta2</td>
      <td></td>
    </tr>
    <tr>
      <td>X+5</td>
      <!-- td>v1, v1beta1 (deprecated), v1beta2 (deprecated)</td -->
      <td>v1、v1beta1（已弃用）、v1beta2（已弃用）</td>
      <td>v1beta2</td>
      <td>
        <ul>
          <!-- li>v1beta2 is deprecated, "action required" relnote</li -->
          <li>v1beta2 被弃用，发布说明中包含对应的 "action required（采取行动）" 说明</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td>X+6</td>
      <!-- td>v1, v1beta2 (deprecated)</td -->
      <td>v1、v1beta2（已弃用）</td>
      <td>v1</td>
      <td>
        <ul>
          <!-- li>v1beta1 is removed, "action required" relnote</li -->
          <li>v1beta1 被去除，发布说明中包含对应的 "action required（采取行动）" 说明</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td>X+7</td>
      <!-- td>v1, v1beta2 (deprecated)</td -->
      <td>v1、v1beta2（已弃用）</td>
      <td>v1</td>
      <td></td>
    </tr>
    <tr>
      <td>X+8</td>
      <td>v2alpha1、v1</td>
      <td>v1</td>
      <td>
        <ul>
          <!-- li>v1beta2 is removed, "action required" relnote</li -->
          <li>v1beta2 被去除，发布说明中包含对应的 "action required（采取行动）" 说明</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td>X+9</td>
      <td>v2alpha2、v1</td>
      <td>v1</td>
      <td>
        <ul>
           <!-- li>v2alpha1 is removed, "action required" relnote</li -->
           <li>v2alpha1 被删除，发布说明中包含对应的 "action required（采取行动）" 说明</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td>X+10</td>
      <td>v2beta1、v1</td>
      <td>v1</td>
      <td>
        <ul>
          <!-- li>v2alpha2 is removed, "action required" relnote</li -->
          <li>v2alpha2 被删除，发布说明中包含对应的 "action required（采取行动）" 说明</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td>X+11</td>
      <!-- td>v2beta2, v2beta1 (deprecated), v1</td -->
      <td>v2beta2、v2beta1（已弃用）、v1</td>
      <td>v1</td>
      <td>
        <ul>
          <!-- li>v2beta1 is deprecated, "action required" relnote</li -->
          <li>v2beta1 被弃用，发布说明中包含对应的 "action required（采取行动）" 说明</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td>X+12</td>
      <!-- td>v2, v2beta2 (deprecated), v2beta1 (deprecated), v1 (deprecated)</td -->
      <td>v2、v2beta2（已弃用）、v2beta1（已弃用）、v1（已弃用）</td>
      <td>v1</td>
      <td>
        <ul>
          <!-- li>v2beta2 is deprecated, "action required" relnote</li>
          <li>v1 is deprecated, "action required" relnote</li -->
          <li>v2beta2 已被弃用，发布说明中包含对应的 "action required（采取行动）" 说明</li>
          <li>v1 已被弃用，发布说明中包含对应的 "action required（采取行动）" 说明</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td>X+13</td>
      <!-- td>v2, v2beta1 (deprecated), v2beta2 (deprecated), v1 (deprecated)</td -->
      <td>v2、v2beta1（已弃用）、v2beta2（已弃用）、v1（已弃用）</td>
      <td>v2</td>
      <td></td>
    </tr>
    <tr>
      <td>X+14</td>
      <!-- td>v2, v2beta2 (deprecated), v1 (deprecated)</td -->
      <td>v2、v2beta2（已弃用）、v1（已弃用）</td>
      <td>v2</td>
      <td>
        <ul>
          <!-- li>v2beta1 is removed, "action required" relnote</li -->
          <li>v2beta1 被删除，发布说明中包含对应的 "action required（采取行动）" 说明</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td>X+15</td>
      <!-- td>v2, v1 (deprecated)</td -->
      <td>v2、v1（已弃用）</td>
      <td>v2</td>
      <td>
        <ul>
          <!-- li>v2beta2 is removed, "action required" relnote</li -->
          <li>v2beta2 被删除，发布说明中包含对应的 "action required（采取行动）" 说明</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td>X+16</td>
      <!-- td>v2, v1 (deprecated)</td -->
      <td>v2、v1（已弃用）</td>
      <td>v2</td>
      <td></td>
    </tr>
    <tr>
      <td>X+17</td>
      <td>v2</td>
      <td>v2</td>
      <td>
        <ul>
          <li>v1 被删除，发布说明中包含对应的 "action required（采取行动）" 说明</li>
        </ul>
      </td>
    </tr>
  </tbody>
</table>

<!--
### REST resources (aka API objects)

Consider a hypothetical REST resource named Widget, which was present in API v1
in the above timeline, and which needs to be deprecated.  We document and
[announce](https://groups.google.com/forum/#!forum/kubernetes-announce) the
deprecation in sync with release X+1.  The Widget resource still exists in API
version v1 (deprecated) but not in v2alpha1.  The Widget resource continues to
exist and function in releases up to and including X+8.  Only in release X+9,
when API v1 has aged out, does the Widget resource cease to exist, and the
behavior get removed.
-->
### REST 资源（也即 API 对象）  {#rest-resources-aka-api-objects}

考虑一个假想的名为 Widget 的 REST 资源，在上述时间线中位于 API v1，
而现在打算将其弃用。
我们会在文档和
[声明](https://groups.google.com/forum/#!forum/kubernetes-announce)
中与 X+1 版本的发布同步记述此弃用决定。
Wdiget 资源仍会在 API 版本 v1（已弃用）中存在，但不会出现在 v2alpha1 中。
Widget 资源会 X+8 发布版本之前（含 X+8）一直存在并可用。
只有在发布版本 X+9 中，API v1 寿终正寝时，Widget
才彻底消失，相应的资源行为也被移除。

<!--
Starting in Kubernetes v1.19, making an API request to a deprecated REST API endpoint:

1. Returns a `Warning` header (as defined in [RFC7234, Section 5.5](https://tools.ietf.org/html/rfc7234#section-5.5)) in the API response.
2. Adds a `"k8s.io/deprecated":"true"` annotation to the [audit event](/docs/tasks/debug-application-cluster/audit/) recorded for the request.
3. Sets an `apiserver_requested_deprecated_apis` gauge metric to `1` in the `kube-apiserver`
   process. The metric has labels for `group`, `version`, `resource`, `subresource` that can be joined
   to the `apiserver_request_total` metric, and a `removed_release` label that indicates the
   Kubernetes release in which the API will no longer be served. The following Prometheus query
   returns information about requests made to deprecated APIs which will be removed in v1.22:

   ```promql
   apiserver_requested_deprecated_apis{removed_release="1.22"} * on(group,version,resource,subresource) group_right() apiserver_request_total
   ```
-->
从 Kubernetes v1.19 开始，当 API 请求被发送到一个已弃用的 REST API 末端时：

1. API 响应中会包含一个 `Warning` 头部字段（如 [RFC7234 5.5 节](https://tools.ietf.org/html/rfc7234#section-5.5)所定义）；
2. 该请求会导致对应的 
   [审计事件](/zh/docs/tasks/debug-application-cluster/audit/)
   中会增加一个注解 `"k8s.io/deprecated":"true"`。
3. `kube-apiserver` 进程的 `apiserver_requested_deprecated_apis` 度量值会被
   设置为 `1`。
   该度量值还附带 `group`、`version`、`resource` 和 `subresource` 标签
   （可供添加到度量值 `apiserver_request_total` 上），
   和一个 `removed_release` 标签，标明该 API 将消失的 Kubernetes 发布版本。
   下面的 Prometheus 查询会返回对 v1.22 中将移除的、已弃用的 API
   的请求的信息：
   
   ```promql
   apiserver_requested_deprecated_apis{removed_release="1.22"} * on(group,version,resource,subresource) group_right() apiserver_request_total
   ```

<!--
### Fields of REST resources

As with whole REST resources, an individual field which was present in API v1
must exist and function until API v1 is removed.  Unlike whole resources, the
v2 APIs may choose a different representation for the field, as long as it can
be round-tripped.  For example a v1 field named "magnitude" which was
deprecated might be named "deprecatedMagnitude" in API v2.  When v1 is
eventually removed, the deprecated field can be removed from v2.
-->
### REST 资源的字段    {#fields-of-rest-resources}

就像整个 REST 资源一样，在 API v1 中曾经存在的各个字段在 API v1 被移除
之前必须一直存在且起作用。
与整个资源上的规定不同，v2 API 可以选择为字段提供不同的表示方式，
只要对应的资源对象可在不同版本之间来回转换即可。
例如，v1 版本中一个名为 "magnitude" 的已弃用字段可能在 API v2 中被命名
为 "deprecatedMagnitude"。当 v1 最终被移除时，废弃的字段也可以从 v2
中移除。

<!--
### Enumerated or constant values

As with whole REST resources and fields thereof, a constant value which was
supported in API v1 must exist and function until API v1 is removed.
-->
### 枚举值或常数值 {#enumerated-or-constant-values}

就像前文讲述的 REST 资源及其中的单个字段一样，API v1 中所支持的常数值
必须在 API v1 被移除之前一直存在且起作用。

<!--
### Component config structures

Component configs are versioned and managed similar to REST resources.
-->
### 组件配置结构  {#component-config-structures}

组件的配置也是有版本的，并且按 REST 资源的方式来管理。

<!--
### Future work

Over time, Kubernetes will introduce more fine-grained API versions, at which
point these rules will be adjusted as needed.
-->
### 将来的工作    {#future-work}

随着时间推移，Kubernetes 会引入粒度更细的 API 版本。
到那时，这里的规则会根据需要进行调整。

<!--
## Deprecating a flag or CLI

The Kubernetes system is comprised of several different programs cooperating.
Sometimes, a Kubernetes release might remove flags or CLI commands
(collectively "CLI elements") in these programs.  The individual programs
naturally sort into two main groups - user-facing and admin-facing programs,
which vary slightly in their deprecation policies.  Unless a flag is explicitly
prefixed or documented as "alpha" or "beta", it is considered GA.
-->
## 弃用一个标志或 CLI 命令

Kubernetes 系统中包含若干不同的、相互协作的程序。
有时，Kubernetes 可能会删除这些程序的某些标志或 CLI 命令（统称“命令行元素”）。
这些程序可以天然地划分到两个大组中：面向用户的和面向管理员的程序。
二者之间的弃用策略略有不同。
除非某个标志显示地通过前缀或文档来标明其为“alpha”或“beta”，
该标志要被视作正式发布的（GA）。

<!--
CLI elements are effectively part of the API to the system, but since they are
not versioned in the same way as the REST API, the rules for deprecation are as
follows:
-->
命令行元素相当于系统的 API 的一部分，不过因为它们并没有采用 REST API
一样的方式来管理版本，其弃用规则规定如下： 

<!--
**Rule #5a: CLI elements of user-facing components (e.g. kubectl) must function
after their announced deprecation for no less than:**

   * **GA: 12 months or 2 releases (whichever is longer)**
   * **Beta: 3 months or 1 release (whichever is longer)**
   * **Alpha: 0 releases**
-->
**规则 #5a：面向用户的命令行元素（例如，kubectl）必须在其宣布被弃用其
在以下时长内仍能使用：**

   * **GA：12 个月或者 2 个发布版本（取其较长者）**
   * **Beta：3 个月或者 1 个发布版本（取其较长者）**
   * **Alpha：0 发布版本**

<!--
**Rule #5b: CLI elements of admin-facing components (e.g. kubelet) must function
after their announced deprecation for no less than:**

   * **GA: 6 months or 1 release (whichever is longer)**
   * **Beta: 3 months or 1 release (whichever is longer)**
   * **Alpha: 0 releases**
-->
**规则 #5b：面向管理员的命令行元素（例如，kubelet）必须在其被宣布弃用
之后以下时长内保持可用：**

   * **GA：6 个月或 1 个发行版本（取其较长者）**
   * **Beta: 3 个月或 1 个发行版本（取其较长者）**
   * **Alpha: 0 个发布版本**

<!--
**Rule #6: Deprecated CLI elements must emit warnings (optionally disable)
when used.**
-->
**规则 #6：被弃用的 CLI 元素在被用到时必须能够产生警告，而警告的
产生是可以被禁止的。**

<!--
## Deprecating a feature or behavior

Occasionally a Kubernetes release needs to deprecate some feature or behavior
of the system that is not controlled by the API or CLI.  In this case, the
rules for deprecation are as follows:
-->
## 弃用某功能特性或行为  {#deprecating-a-feature-or-behavior}

在一些较偶然的情形下，某 Kubernetes 发行版本需要弃用系统的某项功能
特性或者行为，而对应的功能特性或行为并不受 API 或 CLI 控制。在这种情况下，
其弃用规则如下：

<!--
**Rule #7: Deprecated behaviors must function for no less than 1 year after their
announced deprecation.**
-->
**规则 #7：被弃用的行为必须在被宣布弃用之后至少 1 年时间内必须保持能用。**

<!--
This does not imply that all changes to the system are governed by this policy.
This applies only to significant, user-visible behaviors which impact the
correctness of applications running on Kubernetes or that impact the
administration of Kubernetes clusters, and which are being removed entirely.
-->
这并不意味着对系统的所有更改都受此策略约束。
此规则仅适用于重大的、用户可见的行为；这些行为会影响到在 Kubernetes
中运行的应用的正确性，或者影响到 Kubernetes 集群的管理。
此规则也适用于那些被整个移除的功能特性或行为。

<!--
An exception to the above rule is _feature gates_. Feature gates are key=value
pairs that allow for users to enable/disable experimental features.

Feature gates are intended to cover the development life cycle of a feature - they
are not intended to be long-term APIs. As such, they are expected to be deprecated
and removed after a feature becomes GA or is dropped.
-->
上述规则的一个例外是 _特性门控（Feature Gates）_。特性门控是一些键值偶对，
允许用户启用或禁用一些试验性的功能特性。

特性门控意在覆盖功能特性的整个开发周期，它们无意成为长期的 API。
因此，它们会在某功能特性正式发布或被抛弃之后被弃用和删除。

<!--
As a feature moves through the stages, the associated feature gate evolves.
The feature life cycle matched to its corresponding feature gate is:

  * Alpha: the feature gate is disabled by default and can be enabled by the user.
  * Beta: the feature gate is enabled by default and can be disabled by the user.
  * GA: the feature gate is deprecated (see ["Deprecation"](#deprecation)) and becomes
  non-operational.
  * GA, deprecation window complete: the feature gate is removed and calls to it are
  no longer accepted.
-->
随着一个功能特性经过不同的成熟阶段，相关的特性门控也会演化。
与功能特性生命周期对应的特性门控状态为：

* Alpha：特性门控默认被禁用，只能由用户显式启用。
* Beta：特性门控默认被弃用，可被用户显式禁用。
* GA: 特性门控被弃用（参见[弃用](#deprecation)），并且不再起作用。
* GA，弃用窗口期结束：特性门控被删除，不再接受调用。

<!--
### Deprecation

Features can be removed at any point in the life cycle prior to GA. When features are
removed prior to GA, their associated feature gates are also deprecated.

When an invocation tries to disable a non-operational feature gate, the call fails in order
to avoid unsupported scenarios that might otherwise run silently.
-->
### 弃用   {#deprecation}

功能特性在正式发布之前的生命周期内任何时间点都可被移除。
当未正式发布的功能特性被移除时，它们对应的特性门控也被弃用。

当尝试禁用一个不再起作用的特性门控时，该调用会失败，这样可以避免
毫无迹象地执行一些不受支持的场景。

<!--
In some cases, removing pre-GA features requires considerable time. Feature gates can remain
operational until their associated feature is fully removed, at which point the feature gate
itself can be deprecated.

When removing a feature gate for a GA feature also requires considerable time, calls to
feature gates may remain operational if the feature gate has no effect on the feature,
and if the feature gate causes no errors.
-->
在某些场合，移除一个即将正式发布的功能特性需要很长时间。特性门控
可以保持其功能，直到对应的功能特性被彻底去除，直到那时特性门控
自身才可被弃用。

由于移除一个已经正式发布的功能特性对应的特性门控也需要一定时间，对特性
门控的调用可能一直被允许，前提是特性门控对功能本身无影响且特性门控不会
引发任何错误。

<!--
Features intended to be disabled by users should include a mechanism for disabling the
feature in the associated feature gate.

Versioning for feature gates is different from the previously discussed components,
therefore the rules for deprecation are as follows:
-->
意在允许用户禁用的功能特性应该包含一个在相关联的特性门控中禁用该功能的机制。

特性门控的版本管理与之前讨论的组件版本管理不同，因此其对应的弃用策略如下：

<!--
**Rule #8: Feature gates must be deprecated when the corresponding feature they control
transitions a lifecycle stage as follows. Feature gates must function for no less than:**

   * **Beta feature to GA: 6 months or 2 releases (whichever is longer)**
   * **Beta feature to EOL: 3 months or 1 release (whichever is longer)**
   * **Alpha feature to EOL: 0 releases**
-->
**规则 #8：特性门控所对应的功能特性经历下面所列的成熟性阶段转换时，特性门控
必须被弃用。特性门控弃用时必须在以下时长内保持其功能可用：**

   * **Beta 特性转为 GA：6 个月或者 2 个发布版本（取其较长者）**
   * **Beta 特性转为丢弃：3 个月或者 1 个发布版本（取其较长者）**
   * **Alpha 特性转为丢弃：0 个发布版本**

<!--
**Rule #9: Deprecated feature gates must respond with a warning when used. When a feature gate
is deprecated it must be documented in both in the release notes and the corresponding CLI help.
Both warnings and documentation must indicate whether a feature gate is non-operational.**
-->
**规则 #9：已弃用的特色门控再被使用时必须给出警告回应。当特性门控被
弃用时，必须在发布说明和对应的 CLI 帮助信息中通过文档宣布。
警告信息和文档都要标明是否某特性门控不再起作用。**

<!--
## Deprecating a metric

Each component of the Kubernetes control-plane exposes metrics (usually the
`/metrics` endpoint), which are typically ingested by cluster administrators.
Not all metrics are the same: some metrics are commonly used as SLIs or used
to determine SLOs, these tend to have greater import. Other metrics are more
experimental in nature or are used primarily in the Kubernetes development
process.

Accordingly, metrics fall under two stability classes (`ALPHA` and `STABLE`);
this impacts removal of a metric during a Kubernetes release. These classes
are determined by the perceived importance of the metric. The rules for
deprecating and removing a metric are as follows:
-->
### 弃用度量值    {#deprecating-a-metric}

Kubernetes 控制平面的每个组件都公开度量值（通常是 `/metrics` 端点），它们通常由集群管理员使用。
并不是所有的度量值都是同样重要的：一些度量值通常用作 SLIs 或被使用来确定 SLOs，这些往往比较重要。
其他度量值在本质上带有实验性，或者主要用于 Kubernetes 开发过程。

因此，度量值分为两个稳定性类别（`ALPHA` 和 `STABLE`）;
此分类会影响在 Kubernetes 发布版本中移除某度量值。
所对应的分类取决于对该度量值重要性的预期。
弃用和移除度量值的规则如下：

<!--
**Rule #9a: Metrics, for the corresponding stability class, must function for no less than:**

   * **STABLE: 4 releases or 12 months (whichever is longer)**
   * **ALPHA: 0 releases**

**Rule #9b: Metrics, after their _announced deprecation_, must function for no less than:**

   * **STABLE: 3 releases or 9 months (whichever is longer)**
   * **ALPHA: 0 releases**
-->
**规则 #9a: 对于相应的稳定性类别，度量值起作用的周期必须不小于：**

* **STABLE: 4 个发布版本或者 12 个月 (取其较长者)**
* **ALPHA: 0 个发布版本**

**规则 #9b: 在度量值被宣布启用之后，它起作用的周期必须不小于：**

* **STABLE: 3 个发布版本或者 9 个月 (取其较长者)**
* **ALPHA: 0 个发布版本**

<!--
Deprecated metrics will have their description text prefixed with a deprecation notice
string '(Deprecated from x.y)' and a warning log will be emitted during metric
registration. Like their stable undeprecated counterparts, deprecated metrics will
be automatically registered to the metrics endpoint and therefore visible.
-->
已弃用的度量值将在其描述文本前加上一个已弃用通知字符串 '(Deprecated from x.y)'，
并将在度量值被记录期间发出警告日志。就像稳定的、未被弃用的度量指标一样，
被弃用的度量值将自动注册到 metrics 端点，因此被弃用的度量值也是可见的。

<!--
On a subsequent release (when the metric's `deprecatedVersion` is equal to
_current_kubernetes_version - 3_)), a deprecated metric will become a _hidden_ metric.
**_Unlike_** their deprecated counterparts, hidden metrics will _no longer_ be
automatically registered to the metrics endpoint (hence hidden). However, they
can be explicitly enabled through a command line flag on the binary
(`--show-hidden-metrics-for-version=`). This provides cluster admins an
escape hatch to properly migrate off of a deprecated metric, if they were not
able to react to the earlier deprecation warnings. Hidden metrics should be
deleted after one release.
-->
在随后的版本中（当度量值 `deprecatedVersion` 等于_当前 Kubernetes 版本 - 3_），
被弃用的度量值将变成 _隐藏（Hidden）_ metric 度量值。
与被弃用的度量值不同，隐藏的度量值将不再被自动注册到 metrics 端点（因此被隐藏）。
但是，它们可以通过可执行文件的命令行标志显式启用
（`--show-hidden-metrics-for-version=`）。
如果集群管理员不能对早期的弃用警告作出反应，这一设计就为他们提供了抓紧迁移弃用度量值的途径。
隐藏的度量值应该在再过一个发行版本后被删除。

<!--
## Exceptions

No policy can cover every possible situation.  This policy is a living
document, and will evolve over time.  In practice, there will be situations
that do not fit neatly into this policy, or for which this policy becomes a
serious impediment.  Such situations should be discussed with SIGs and project
leaders to find the best solutions for those specific cases, always bearing in
mind that Kubernetes is committed to being a stable system that, as much as
possible, never breaks users. Exceptions will always be announced in all
relevant release notes.
-->
## 例外   {#exceptions}

没有策略可以覆盖所有情况。此策略文档是一个随时被更新的文档，会随着时间
推移演化。在实践中，会有一些情况无法很好地匹配到这里的弃用策略，或者
这里的策略变成了很严重的羁绊。这类情形要与 SIG 和项目牵头人讨论，
寻求对应场景的最佳解决方案。请一直铭记，Kubernetes 承诺要成为一个
稳定的系统，至少会尽力做到不会影响到其用户。此弃用策略的任何例外情况
都会在所有相关的发布说明中公布。

