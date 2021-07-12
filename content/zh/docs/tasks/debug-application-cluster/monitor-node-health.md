---
content_type: task
title: 节点健康监测
---
<!-- 
title: Monitor Node Health
content_type: task
reviewers:
- Random-Liu
- dchen1107
-->

<!-- overview -->
<!-- 
*Node Problem Detector* is a daemon for monitoring and reporting about a node's health.
You can run Node Problem Detector as a `DaemonSet` or as a standalone daemon.
Node Problem Detector collects information about node problems from various daemons
and reports these conditions to the API server as [NodeCondition](/docs/concepts/architecture/nodes/#condition)
and [Event](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#event-v1-core). 

To learn how to install and use Node Problem Detector, see
[Node Problem Detector project documentation](https://github.com/kubernetes/node-problem-detector).
-->

*节点问题检测器（Node Problem Detector）* 是一个守护程序，用于监视和报告节点的健康状况。
你可以将节点问题探测器以 `DaemonSet` 或独立守护程序运行。
节点问题检测器从各种守护进程收集节点问题，并以
[NodeCondition](/zh/docs/concepts/architecture/nodes/#condition) 和
[Event](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#event-v1-core)
的形式报告给 API 服务器。 

要了解如何安装和使用节点问题检测器，请参阅
[节点问题探测器项目文档](https://github.com/kubernetes/node-problem-detector)。

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}}

<!-- steps -->

<!-- 
## Limitations 

* Node Problem Detector only supports file based kernel log.
  Log tools such as `journald` are not supported.

* Node Problem Detector uses the kernel log format for reporting kernel issues.
  To learn how to extend the kernel log format, see [Add support for another log format](#support-other-log-format).
-->
## 局限性  {#limitations}

* 节点问题检测器只支持基于文件类型的内核日志。
  它不支持像 journald 这样的命令行日志工具。
* 节点问题检测器使用内核日志格式来报告内核问题。
  要了解如何扩展内核日志格式，请参阅[添加对另一个日志格式的支持](#support-other-log-format)。

<!-- 
## Enabling Node Problem Detector

Some cloud providers enable Node Problem Detector as an {{< glossary_tooltip text="Addon" term_id="addons" >}}.
You can also enable Node Problem Detector with `kubectl` or by creating an Addon pod.
-->
## 启用节点问题检测器

一些云供应商将节点问题检测器以{{< glossary_tooltip text="插件" term_id="addons" >}}形式启用。
你还可以使用 `kubectl` 或创建插件 Pod 来启用节点问题探测器。

<!-- 
## Using kubectl to enable Node Problem Detector {#using-kubectl}

`kubectl` provides the most flexible management of Node Problem Detector.
You can overwrite the default configuration to fit it into your environment or
to detect customized node problems. For example:
-->
## 使用 kubectl 启用节点问题检测器 {#using-kubectl}

`kubectl` 提供了节点问题探测器最灵活的管理。
你可以覆盖默认配置使其适合你的环境或检测自定义节点问题。例如：

<!-- 
1. Create a Node Problem Detector configuration similar to `node-problem-detector.yaml`:

   {{< codenew file="debug/node-problem-detector.yaml" >}}

   {{< note >}}
   You should verify that the system log directory is right for your operating system distribution.
   {{< /note >}}

1. Start node problem detector with `kubectl`:

   ```shell
   kubectl apply -f https://k8s.io/examples/debug/node-problem-detector.yaml
   ```
-->
1. 创建类似于 `node-strought-detector.yaml` 的节点问题检测器配置：
   {{< codenew file="debug/node-problem-detector.yaml" >}}

   {{< note >}}
   你应该检查系统日志目录是否适用于操作系统发行版本。
   {{< /note >}}

1. 使用 `kubectl` 启动节点问题检测器：

   ```shell
   kubectl apply -f https://k8s.io/examples/debug/node-problem-detector.yaml
   ```

<!-- 
### Using an Addon pod to enable Node Problem Detector {#using-addon-pod}

If you are using a custom cluster bootstrap solution and don't need
to overwrite the default configuration, you can leverage the Addon pod to
further automate the deployment.

Create `node-problem-detector.yaml`, and save the configuration in the Addon pod's
directory `/etc/kubernetes/addons/node-problem-detector` on a control plane node.
-->
### 使用插件 pod 启用节点问题检测器 {#using-addon-pod}

如果你使用的是自定义集群引导解决方案，不需要覆盖默认配置，
可以利用插件 Pod 进一步自动化部署。

创建 `node-strick-detector.yaml`，并在控制平面节点上保存配置到插件 Pod 的目录
`/etc/kubernetes/addons/node-problem-detector`。

<!-- 
## Overwrite the Configuration 

The [default configuration](https://github.com/kubernetes/node-problem-detector/tree/v0.1/config)
is embedded when building the Docker image of Node Problem Detector.
-->
## 覆盖配置文件

构建节点问题检测器的 docker 镜像时，会嵌入
[默认配置](https://github.com/kubernetes/node-problem-detector/tree/v0.1/config)。

<!-- 
However, you can use a [`ConfigMap`](/docs/tasks/configure-pod-container/configure-pod-configmap/)
to overwrite the configuration:
-->
不过，你可以像下面这样使用 [`ConfigMap`](/zh/docs/tasks/configure-pod-container/configure-pod-configmap/)
将其覆盖：

<!-- 
1. Change the configuration files in `config/`
1. Create the `ConfigMap` `node-problem-detector-config`:

   ```shell
   kubectl create configmap node-problem-detector-config --from-file=config/
   ```

1. Change the `node-problem-detector.yaml` to use the `ConfigMap`:

   {{< codenew file="debug/node-problem-detector-configmap.yaml" >}}

1. Recreate the Node Problem Detector with the new configuration file:

   ```shell
   # If you have a node-problem-detector running, delete before recreating
   kubectl delete -f https://k8s.io/examples/debug/node-problem-detector.yaml
   kubectl apply -f https://k8s.io/examples/debug/node-problem-detector-configmap.yaml
   ```
 -->
1. 更改 `config/` 中的配置文件
1. 创建 `ConfigMap` `node-strick-detector-config`：
   
   ```shell
   kubectl create configmap node-problem-detector-config --from-file=config/
   ```

1. 更改 `node-problem-detector.yaml` 以使用 ConfigMap:
   
   {{< codenew file="debug/node-problem-detector-configmap.yaml" >}}

1. 使用新的配置文件重新创建节点问题检测器：

    ```shell
   # 如果你正在运行节点问题检测器，请先删除，然后再重新创建
   kubectl delete -f https://k8s.io/examples/debug/node-problem-detector.yaml
   kubectl apply -f https://k8s.io/examples/debug/node-problem-detector-configmap.yaml
   ```

<!--  
{{< note >}}
This approach only applies to a Node Problem Detector started with `kubectl`.
{{< /note >}}

Overwriting a configuration is not supported if a Node Problem Detector runs as a cluster Addon.
The Addon manager does not support `ConfigMap`.
-->
{{< note >}}
此方法仅适用于通过 `kubectl` 启动的节点问题检测器。
{{< /note >}}

如果节点问题检测器作为集群插件运行，则不支持覆盖配置。
插件管理器不支持 `ConfigMap`。

<!-- 
## Kernel Monitor 

*Kernel Monitor* is a system log monitor daemon supported in the Node Problem Detector.
Kernel monitor watches the kernel log and detects known kernel issues following predefined rules.
-->
## 内核监视器

*内核监视器（Kernel Monitor）* 是节点问题检测器中支持的系统日志监视器守护进程。
内核监视器观察内核日志并根据预定义规则检测已知的内核问题。

<!-- 
The Kernel Monitor matches kernel issues according to a set of predefined rule list in
[`config/kernel-monitor.json`](https://github.com/kubernetes/node-problem-detector/blob/v0.1/config/kernel-monitor.json). The rule list is extensible. You can expand the rule list by overwriting the
configuration.
-->
内核监视器根据 [`config/kernel-monitor.json`](https://github.com/kubernetes/node-problem-detector/blob/v0.1/config/kernel-monitor.json)
中的一组预定义规则列表匹配内核问题。
规则列表是可扩展的，你始终可以通过覆盖配置来扩展它。

<!-- 
### Add new NodeConditions 

To support a new `NodeCondition`, create a condition definition within the `conditions` field in
`config/kernel-monitor.json`, for example:
```
-->
### 添加新的 NodeCondition

要支持新的 `NodeCondition`，请在 `config/kernel-monitor.json` 中的
`conditions` 字段中创建一个条件定义：

```json
{
  "type": "NodeConditionType",
  "reason": "CamelCaseDefaultNodeConditionReason",
  "message": "arbitrary default node condition message"
}
```

<!-- 
### Detect new problems 

To detect new problems, you can extend the `rules` field in `config/kernel-monitor.json`
with a new rule definition:
-->
### 检测新的问题

你可以使用新的规则描述来扩展 `config/kernel-monitor.json` 中的 `rules` 字段以检测新问题：

```json
{
  "type": "temporary/permanent",
  "condition": "NodeConditionOfPermanentIssue",
  "reason": "CamelCaseShortReason",
  "message": "regexp matching the issue in the kernel log"
}
```

<!-- 
### Configure path for the kernel log device {#kernel-log-device-path}

Check your kernel log path location in your operating system (OS) distribution.
The Linux kernel [log device](https://www.kernel.org/doc/Documentation/ABI/testing/dev-kmsg) is usually presented as `/dev/kmsg`. However, the log path location varies by OS distribution.
The `log` field in `config/kernel-monitor.json` represents the log path inside the container.
You can configure the `log` field to match the device path as seen by the Node Problem Detector.
-->
### 配置内核日志设备的路径 {#kernel-log-device-path}

检查你的操作系统（OS）发行版本中的内核日志路径位置。
Linux 内核[日志设备](https://www.kernel.org/doc/documentation/abi/testing/dev-kmsg)
通常呈现为 `/dev/kmsg`。
但是，日志路径位置因 OS 发行版本而异。
`config/kernel-monitor.json` 中的 `log` 字段表示容器内的日志路径。
你可以配置 `log` 字段以匹配节点问题检测器所示的设备路径。

<!-- 
### Add support for another log format {#support-other-log-format}

Kernel monitor uses the
[`Translator`](https://github.com/kubernetes/node-problem-detector/blob/v0.1/pkg/kernelmonitor/translator/translator.go) plugin to translate the internal data structure of the kernel log.
You can implement a new translator for a new log format.
-->
### 添加对其它日志格式的支持  {#support-other-log-format}

内核监视器使用 
[`Translator`](https://github.com/kubernetes/node-problem-detector/blob/v0.1/pkg/kernelmonitor/translator.go)
插件转换内核日志的内部数据结构。
你可以为新的日志格式实现新的转换器。

<!-- discussion -->

<!-- 
## Recommendations and restrictions

It is recommended to run the Node Problem Detector in your cluster to monitor node health.
When running the Node Problem Detector, you can expect extra resource overhead on each node.
Usually this is fine, because:

* The kernel log grows relatively slowly.
* A resource limit is set for the Node Problem Detector.
* Even under high load, the resource usage is acceptable. For more information, see the Node Problem Detector
[benchmark result](https://github.com/kubernetes/node-problem-detector/issues/2#issuecomment-220255629).
-->
## 建议和限制

建议在集群中运行节点问题检测器以监控节点运行状况。
运行节点问题检测器时，你可以预期每个节点上的额外资源开销。
通常这是可接受的，因为：

* 内核日志增长相对缓慢。
* 已经为节点问题检测器设置了资源限制。
* 即使在高负载下，资源使用也是可接受的。有关更多信息，请参阅节点问题检测器
  [基准结果](https://github.com/kubernetes/node-problem-detector/issues/2.suecomment-220255629)。
