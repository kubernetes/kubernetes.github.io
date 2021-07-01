---
reviewers:
- hw-qiaolei
title: kubectl 概述
content_type: concept
weight: 20
card:
  name: reference
  weight: 20
---
<!--
reviewers:
- bgrant0607
- hw-qiaolei
title: Overview of kubectl
content_type: concept
weight: 20
card:
  name: reference
  weight: 20
-->

<!-- overview -->

<!--
The kubectl command line tool lets you control Kubernetes clusters.
For configuration, `kubectl` looks for a file named `config` in the `$HOME/.kube` directory.
You can specify other [kubeconfig](/docs/concepts/configuration/organize-cluster-access-kubeconfig/)
files by setting the KUBECONFIG environment variable or by setting the
[`--kubeconfig`](/docs/concepts/configuration/organize-cluster-access-kubeconfig/) flag.
-->
你可以使用 Kubectl 命令行工具管理 Kubernetes 集群。
`kubectl` 在 `$HOME/.kube` 目录中查找一个名为 `config` 的配置文件。
你可以通过设置 KUBECONFIG 环境变量或设置
[`--kubeconfig`](/zh/docs/concepts/configuration/organize-cluster-access-kubeconfig/)
参数来指定其它 [kubeconfig](/zh/docs/concepts/configuration/organize-cluster-access-kubeconfig/) 文件。

<!--
This overview covers `kubectl` syntax, describes the command operations, and provides common examples.
For details about each command, including all the supported flags and subcommands, see the
[kubectl](/docs/reference/generated/kubectl/kubectl-commands/) reference documentation.
For installation instructions see [installing kubectl](/docs/tasks/tools/install-kubectl/).
-->
本文概述了 `kubectl` 语法和命令操作描述，并提供了常见的示例。
有关每个命令的详细信息，包括所有受支持的参数和子命令，
请参阅 [kubectl](/docs/reference/generated/kubectl/kubectl-commands/) 参考文档。
有关安装说明，请参见[安装 kubectl](/zh/docs/tasks/tools/install-kubectl/) 。

<!-- body -->

<!--
## Syntax
-->
## 语法

<!--
Use the following syntax to run `kubectl` commands from your terminal window:
-->
使用以下语法 `kubectl` 从终端窗口运行命令：

```shell
kubectl [command] [TYPE] [NAME] [flags]
```

<!--
where `command`, `TYPE`, `NAME`, and `flags` are:
-->
其中 `command`、`TYPE`、`NAME` 和 `flags` 分别是：

<!--
* `command`: Specifies the operation that you want to perform on one or more resources, for example `create`, `get`, `describe`, `delete`.

* `TYPE`: Specifies the [resource type](#resource-types). Resource types are case-insensitive and you can specify the singular, plural, or abbreviated forms. For example, the following commands produce the same output:
-->
* `command`：指定要对一个或多个资源执行的操作，例如 `create`、`get`、`describe`、`delete`。

* `TYPE`：指定[资源类型](#资源类型)。资源类型不区分大小写，
  可以指定单数、复数或缩写形式。例如，以下命令输出相同的结果:

  ```shell
  kubectl get pod pod1
  kubectl get pods pod1
  kubectl get po pod1
  ```

<!--
* `NAME`: Specifies the name of the resource. Names are case-sensitive. If the name is omitted, details for all resources are displayed, for example `kubectl get pods`.

   When performing an operation on multiple resources, you can specify each resource by type and name or specify one or more files:
-->

* `NAME`：指定资源的名称。名称区分大小写。
  如果省略名称，则显示所有资源的详细信息 `kubectl get pods`。

  在对多个资源执行操作时，你可以按类型和名称指定每个资源，或指定一个或多个文件：

  <!--
   * To specify resources by type and name:

      * To group resources if they are all the same type:  `TYPE1 name1 name2 name<#>`.<br/>
      Example: `kubectl get pod example-pod1 example-pod2`

      * To specify multiple resource types individually:  `TYPE1/name1 TYPE1/name2 TYPE2/name3 TYPE<#>/name<#>`.<br/>
      Example: `kubectl get pod/example-pod1 replicationcontroller/example-rc1`

   * To specify resources with one or more files:  `-f file1 -f file2 -f file<#>`

      * [Use YAML rather than JSON](/docs/concepts/configuration/overview/#general-configuration-tips)
        since YAML tends to be more user-friendly, especially for configuration files.<br/>
     Example: `kubectl get -f ./pod.yaml`
  -->
  * 要按类型和名称指定资源：

      * 要对所有类型相同的资源进行分组，请执行以下操作：`TYPE1 name1 name2 name<#>`。

        例子：`kubectl get pod example-pod1 example-pod2`

      * 分别指定多个资源类型：`TYPE1/name1 TYPE1/name2 TYPE2/name3 TYPE<#>/name<#>`。

        例子：`kubectl get pod/example-pod1 replicationcontroller/example-rc1`

  * 用一个或多个文件指定资源：`-f file1 -f file2 -f file<#>`

    * [使用 YAML 而不是 JSON](/zh/docs/concepts/configuration/overview/#general-configuration-tips)
      因为 YAML 更容易使用，特别是用于配置文件时。
      例子：`kubectl get -f ./pod.yaml`

<!--
* `flags`: Specifies optional flags. For example, you can use the `-s` or `--server` flags to specify the address and port of the Kubernetes API server.
-->
* `flags`: 指定可选的参数。例如，可以使用 `-s` 或 `-server` 参数指定
  Kubernetes API 服务器的地址和端口。

{{< caution >}}
<!--
Flags that you specify from the command line override default values and any corresponding environment variables.
-->
从命令行指定的参数会覆盖默认值和任何相应的环境变量。
{{< /caution >}}

<!--
If you need help, run `kubectl help` from the terminal window.
-->
如果你需要帮助，从终端窗口运行 `kubectl help` 。

<!--
## Operations
-->
## 操作

<!--
The following table includes short descriptions and the general syntax for all of the `kubectl` operations:
-->
下表包含所有 kubectl 操作的简短描述和普通语法：

<!--
Operation       | Syntax    |       Description
-------------------- | -------------------- | --------------------
`alpha`    | `kubectl alpha SUBCOMMAND [flags]` | List the available commands that correspond to alpha features, which are not enabled in Kubernetes clusters by default.
`annotate`    | <code>kubectl annotate (-f FILENAME &#124; TYPE NAME &#124; TYPE/NAME) KEY_1=VAL_1 ... KEY_N=VAL_N [--overwrite] [--all] [--resource-version=version] [flags]</code> | Add or update the annotations of one or more resources.
`api-resources`    | `kubectl api-resources [flags]` | List the API resources that are available.
`api-versions`    | `kubectl api-versions [flags]` | List the API versions that are available.
`apply`            | `kubectl apply -f FILENAME [flags]`| Apply a configuration change to a resource from a file or stdin.
`attach`        | `kubectl attach POD -c CONTAINER [-i] [-t] [flags]` | Attach to a running container either to view the output stream or interact with the container (stdin).
`auth`    | `kubectl auth [flags] [options]` | Inspect authorization.
`autoscale`    | <code>kubectl autoscale (-f FILENAME &#124; TYPE NAME &#124; TYPE/NAME) [--min=MINPODS] --max=MAXPODS [--cpu-percent=CPU] [flags]</code> | Automatically scale the set of pods that are managed by a replication controller.
`certificate`    | `kubectl certificate SUBCOMMAND [options]` | Modify certificate resources.
`cluster-info`    | `kubectl cluster-info [flags]` | Display endpoint information about the master and services in the cluster.
`completion`    | `kubectl completion SHELL [options]` | Output shell completion code for the specified shell (bash or zsh).
`config`        | `kubectl config SUBCOMMAND [flags]` | Modifies kubeconfig files. See the individual subcommands for details.
`convert`    | `kubectl convert -f FILENAME [options]` | Convert config files between different API versions. Both YAML and JSON formats are accepted.
`cordon`    | `kubectl cordon NODE [options]` | Mark node as unschedulable.
`cp`    | `kubectl cp <file-spec-src> <file-spec-dest> [options]` | Copy files and directories to and from containers.
`create`        | `kubectl create -f FILENAME [flags]` | Create one or more resources from a file or stdin.
`delete`        | <code>kubectl delete (-f FILENAME &#124; TYPE [NAME &#124; /NAME &#124; -l label &#124; --all]) [flags]</code> | Delete resources either from a file, stdin, or specifying label selectors, names, resource selectors, or resources.
`describe`    | <code>kubectl describe (-f FILENAME &#124; TYPE [NAME_PREFIX &#124; /NAME &#124; -l label]) [flags]</code> | Display the detailed state of one or more resources.
`diff`        | `kubectl diff -f FILENAME [flags]`| Diff file or stdin against live configuration.
`drain`    | `kubectl drain NODE [options]` | Drain node in preparation for maintenance.
`edit`        | <code>kubectl edit (-f FILENAME &#124; TYPE NAME &#124; TYPE/NAME) [flags]</code> | Edit and update the definition of one or more resources on the server by using the default editor.
`exec`        | `kubectl exec POD [-c CONTAINER] [-i] [-t] [flags] [-- COMMAND [args...]]` | Execute a command against a container in a pod.
`explain`    | `kubectl explain  [--recursive=false] [flags]` | Get documentation of various resources. For instance pods, nodes, services, etc.
`expose`        | <code>kubectl expose (-f FILENAME &#124; TYPE NAME &#124; TYPE/NAME) [--port=port] [--protocol=TCP&#124;UDP] [--target-port=number-or-name] [--name=name] [--external-ip=external-ip-of-service] [--type=type] [flags]</code> | Expose a replication controller, service, or pod as a new Kubernetes service.
`get`        | <code>kubectl get (-f FILENAME &#124; TYPE [NAME &#124; /NAME &#124; -l label]) [--watch] [--sort-by=FIELD] [[-o &#124; --output]=OUTPUT_FORMAT] [flags]</code> | List one or more resources.
`kustomize`    | `kubectl kustomize <dir> [flags] [options]` | List a set of API resources generated from instructions in a kustomization.yaml file. The argument must be the path to the directory containing the file, or a git repository URL with a path suffix specifying same with respect to the repository root.
`label`        | <code>kubectl label (-f FILENAME &#124; TYPE NAME &#124; TYPE/NAME) KEY_1=VAL_1 ... KEY_N=VAL_N [--overwrite] [--all] [--resource-version=version] [flags]</code> | Add or update the labels of one or more resources.
`logs`        | `kubectl logs POD [-c CONTAINER] [--follow] [flags]` | Print the logs for a container in a pod.
`options`    | `kubectl options` | List of global command-line options, which apply to all commands.
`patch`        | <code>kubectl patch (-f FILENAME &#124; TYPE NAME &#124; TYPE/NAME) --patch PATCH [flags]</code> | Update one or more fields of a resource by using the strategic merge patch process.
`plugin`    | `kubectl plugin [flags] [options]` | Provides utilities for interacting with plugins.
`port-forward`    | `kubectl port-forward POD [LOCAL_PORT:]REMOTE_PORT [...[LOCAL_PORT_N:]REMOTE_PORT_N] [flags]` | Forward one or more local ports to a pod.
`proxy`        | `kubectl proxy [--port=PORT] [--www=static-dir] [--www-prefix=prefix] [--api-prefix=prefix] [flags]` | Run a proxy to the Kubernetes API server.
`replace`        | `kubectl replace -f FILENAME` | Replace a resource from a file or stdin.
`rollout`    | `kubectl rollout SUBCOMMAND [options]` | Manage the rollout of a resource. Valid resource types include: deployments, daemonsets and statefulsets.
`run`        | <code>kubectl run NAME --image=image [--env="key=value"] [--port=port] [--dry-run=server&#124;client&#124;none] [--overrides=inline-json] [flags]</code> | Run a specified image on the cluster.
`scale`        | <code>kubectl scale (-f FILENAME &#124; TYPE NAME &#124; TYPE/NAME) --replicas=COUNT [--resource-version=version] [--current-replicas=count] [flags]</code> | Update the size of the specified replication controller.
`set`    | `kubectl set SUBCOMMAND [options]` | Configure application resources.
`taint`    | `kubectl taint NODE NAME KEY_1=VAL_1:TAINT_EFFECT_1 ... KEY_N=VAL_N:TAINT_EFFECT_N [options]` | Update the taints on one or more nodes.
`top`    | `kubectl top [flags] [options]` | Display Resource (CPU/Memory/Storage) usage.
`uncordon`    | `kubectl uncordon NODE [options]` | Mark node as schedulable.
`version`        | `kubectl version [--client] [flags]` | Display the Kubernetes version running on the client and server.
`wait`    | <code>kubectl wait ([-f FILENAME] &#124; resource.group/resource.name &#124; resource.group [(-l label &#124; --all)]) [--for=delete&#124;--for condition=available] [options]</code> | Experimental: Wait for a specific condition on one or many resources.
-->

操作             | 语法      |       描述
-------------------- | -------------------- | --------------------
`alpha`    | `kubectl alpha SUBCOMMAND [flags]` | 列出与 alpha 特性对应的可用命令，这些特性在 Kubernetes 集群中默认情况下是不启用的。
`annotate`    | <code>kubectl annotate (-f FILENAME &#124; TYPE NAME &#124; TYPE/NAME) KEY_1=VAL_1 ... KEY_N=VAL_N [--overwrite] [--all] [--resource-version=version] [flags]</code> | 添加或更新一个或多个资源的注解。
`api-resources`    | `kubectl api-resources [flags]` | 列出可用的 API 资源。
`api-versions`    | `kubectl api-versions [flags]` | 列出可用的 API 版本。
`apply`            | `kubectl apply -f FILENAME [flags]`| 从文件或 stdin 对资源应用配置更改。
`attach`        | `kubectl attach POD -c CONTAINER [-i] [-t] [flags]` | 附加到正在运行的容器，查看输出流或与容器（stdin）交互。
`auth`    | `kubectl auth [flags] [options]` | 检查授权。
`autoscale`    | <code>kubectl autoscale (-f FILENAME &#124; TYPE NAME &#124; TYPE/NAME) [--min=MINPODS] --max=MAXPODS [--cpu-percent=CPU] [flags]</code> | 自动伸缩由副本控制器管理的一组 pod。
`certificate`    | `kubectl certificate SUBCOMMAND [options]` | 修改证书资源。
`cluster-info`    | `kubectl cluster-info [flags]` | 显示有关集群中主服务器和服务的端口信息。
`completion`    | `kubectl completion SHELL [options]` | 为指定的 shell （bash 或 zsh）输出 shell 补齐代码。
`config`        | `kubectl config SUBCOMMAND [flags]` | 修改 kubeconfig 文件。有关详细信息，请参阅各个子命令。
`convert`    | `kubectl convert -f FILENAME [options]` | 在不同的 API 版本之间转换配置文件。配置文件可以是 YAML 或 JSON 格式。
`cordon`    | `kubectl cordon NODE [options]` | 将节点标记为不可调度。
`cp`    | `kubectl cp <file-spec-src> <file-spec-dest> [options]` | 在容器之间复制文件和目录。
`create`        | `kubectl create -f FILENAME [flags]` | 从文件或 stdin 创建一个或多个资源。
`delete`        | <code>kubectl delete (-f FILENAME &#124; TYPE [NAME &#124; /NAME &#124; -l label &#124; --all]) [flags]</code> | 从文件、标准输入或指定标签选择器、名称、资源选择器或资源中删除资源。
`describe`    | <code>kubectl describe (-f FILENAME &#124; TYPE [NAME_PREFIX &#124; /NAME &#124; -l label]) [flags]</code> | 显示一个或多个资源的详细状态。
`diff`        | `kubectl diff -f FILENAME [flags]`| 将 live 配置和文件或标准输入做对比 (**BETA**)
`drain`    | `kubectl drain NODE [options]` | 腾空节点以准备维护。
`edit`        | <code>kubectl edit (-f FILENAME &#124; TYPE NAME &#124; TYPE/NAME) [flags]</code> | 使用默认编辑器编辑和更新服务器上一个或多个资源的定义。
`exec`        | `kubectl exec POD [-c CONTAINER] [-i] [-t] [flags] [-- COMMAND [args...]]` | 对 pod 中的容器执行命令。
`explain`    | `kubectl explain  [--recursive=false] [flags]` | 获取多种资源的文档。例如 pod, node, service 等。
`expose`        | <code>kubectl expose (-f FILENAME &#124; TYPE NAME &#124; TYPE/NAME) [--port=port] [--protocol=TCP&#124;UDP] [--target-port=number-or-name] [--name=name] [--external-ip=external-ip-of-service] [--type=type] [flags]</code> | 将副本控制器、服务或 pod 作为新的 Kubernetes 服务暴露。
`get`        | <code>kubectl get (-f FILENAME &#124; TYPE [NAME &#124; /NAME &#124; -l label]) [--watch] [--sort-by=FIELD] [[-o &#124; --output]=OUTPUT_FORMAT] [flags]</code> | 列出一个或多个资源。
`kustomize`    | `kubectl kustomize <dir> [flags] [options]` | 列出从 kustomization.yaml 文件中的指令生成的一组 API 资源。参数必须是包含文件的目录的路径，或者是 git 存储库 URL，其路径后缀相对于存储库根目录指定了相同的路径。
`label`        | <code>kubectl label (-f FILENAME &#124; TYPE NAME &#124; TYPE/NAME) KEY_1=VAL_1 ... KEY_N=VAL_N [--overwrite] [--all] [--resource-version=version] [flags]</code> | 添加或更新一个或多个资源的标签。
`logs`        | `kubectl logs POD [-c CONTAINER] [--follow] [flags]` | 在 pod 中打印容器的日志。
`options`    | `kubectl options` | 全局命令行选项列表，适用于所有命令。
`patch`        | <code>kubectl patch (-f FILENAME &#124; TYPE NAME &#124; TYPE/NAME) --patch PATCH [flags]</code> | 使用策略合并 patch 程序更新资源的一个或多个字段。
`plugin`    | `kubectl plugin [flags] [options]` | 提供用于与插件交互的实用程序。
`port-forward`    | `kubectl port-forward POD [LOCAL_PORT:]REMOTE_PORT [...[LOCAL_PORT_N:]REMOTE_PORT_N] [flags]` | 将一个或多个本地端口转发到一个 pod。
`proxy`        | `kubectl proxy [--port=PORT] [--www=static-dir] [--www-prefix=prefix] [--api-prefix=prefix] [flags]` | 运行 Kubernetes API 服务器的代理。
`replace`        | `kubectl replace -f FILENAME` | 从文件或标准输入中替换资源。
`rollout`    | `kubectl rollout SUBCOMMAND [options]` | 管理资源的部署。有效的资源类型包括：Deployments, DaemonSets 和 StatefulSets。
`run`        | <code>kubectl run NAME --image=image [--env="key=value"] [--port=port] [--dry-run=server &#124; client &#124; none] [--overrides=inline-json] [flags]</code> | 在集群上运行指定的镜像。
`scale`        | <code>kubectl scale (-f FILENAME &#124; TYPE NAME &#124; TYPE/NAME) --replicas=COUNT [--resource-version=version] [--current-replicas=count] [flags]</code> | 更新指定副本控制器的大小。
`set`    | `kubectl set SUBCOMMAND [options]` | 配置应用程序资源。
`taint`    | `kubectl taint NODE NAME KEY_1=VAL_1:TAINT_EFFECT_1 ... KEY_N=VAL_N:TAINT_EFFECT_N [options]` | 更新一个或多个节点上的污点。
`top`    | `kubectl top [flags] [options]` | 显示资源（CPU/内存/存储）的使用情况。
`uncordon`    | `kubectl uncordon NODE [options]` | 将节点标记为可调度。
`version`        | `kubectl version [--client] [flags]` | 显示运行在客户端和服务器上的 Kubernetes 版本。
`wait`    | <code>kubectl wait ([-f FILENAME] &#124; resource.group/resource.name &#124; resource.group [(-l label &#124; --all)]) [--for=delete&#124;--for condition=available] [options]</code> | 实验性：等待一种或多种资源的特定条件。


<!--
To learn more about command operations, see the [kubectl](/docs/reference/kubectl/kubectl/) reference documentation.
-->
了解更多有关命令操作的信息，请参阅 [kubectl](/zh/docs/reference/kubectl/kubectl/) 参考文档。

<!--
## Resource types
-->

## 资源类型

<!--
The following table includes a list of all the supported resource types and their abbreviated aliases:
-->
下表列出所有受支持的资源类型及其缩写别名:

<!--
(This output can be retrieved from `kubectl api-resources`, and was accurate as of Kubernetes 1.19.1.)
-->
(以下输出可以通过 `kubectl api-resources` 获取，内容以 Kubernetes 1.19.1 版本为准。)

<!--
| NAME | SHORTNAMES | APIGROUP | NAMESPACED | KIND |
|---|---|---|---|---|
| `bindings` | | | true | Binding |
| `componentstatuses` | `cs` | | false | ComponentStatus |
| `configmaps` | `cm` | | true | ConfigMap |
| `endpoints` | `ep` | | true | Endpoints |
| `events` | `ev` | | true | Event |
| `limitranges` | `limits` | | true | LimitRange |
| `namespaces` | `ns` | | false | Namespace |
| `nodes` | `no` | | false | Node |
| `persistentvolumeclaims` | `pvc` | | true | PersistentVolumeClaim |
| `persistentvolumes` | `pv` | | false | PersistentVolume |
| `pods` | `po` | | true | Pod |
| `podtemplates` | | | true | PodTemplate |
| `replicationcontrollers` | `rc` | | true | ReplicationController |
| `resourcequotas` | `quota` | | true | ResourceQuota |
| `secrets` | | | true | Secret |
| `serviceaccounts` | `sa` | | true | ServiceAccount |
| `services` | `svc` | | true | Service |
| `mutatingwebhookconfigurations` | | admissionregistration.k8s.io | false | MutatingWebhookConfiguration |
| `validatingwebhookconfigurations` | | admissionregistration.k8s.io | false | ValidatingWebhookConfiguration |
| `customresourcedefinitions` | `crd,crds` | apiextensions.k8s.io | false | CustomResourceDefinition |
| `apiservices` | | apiregistration.k8s.io | false | APIService |
| `controllerrevisions` | | apps | true | ControllerRevision |
| `daemonsets` | `ds` | apps | true | DaemonSet |
| `deployments` | `deploy` | apps | true | Deployment |
| `replicasets` | `rs` | apps | true | ReplicaSet |
| `statefulsets` | `sts` | apps | true | StatefulSet |
| `tokenreviews` | | authentication.k8s.io | false | TokenReview |
| `localsubjectaccessreviews` | | authorization.k8s.io | true | LocalSubjectAccessReview |
| `selfsubjectaccessreviews` | | authorization.k8s.io | false | SelfSubjectAccessReview |
| `selfsubjectrulesreviews` | | authorization.k8s.io | false | SelfSubjectRulesReview |
| `subjectaccessreviews` | | authorization.k8s.io | false | SubjectAccessReview |
| `horizontalpodautoscalers` | `hpa` | autoscaling | true | HorizontalPodAutoscaler |
| `cronjobs` | `cj` | batch | true | CronJob |
| `jobs` | | batch | true | Job |
| `certificatesigningrequests` | `csr` | certificates.k8s.io | false | CertificateSigningRequest |
| `leases` | | coordination.k8s.io | true | Lease |
| `endpointslices` |  | discovery.k8s.io | true | EndpointSlice |
| `events` | `ev` | events.k8s.io | true | Event |
| `ingresses` | `ing` | extensions | true | Ingress |
| `flowschemas` |  | flowcontrol.apiserver.k8s.io | false | FlowSchema |
| `prioritylevelconfigurations` |  | flowcontrol.apiserver.k8s.io | false | PriorityLevelConfiguration |
| `ingressclasses` |  | networking.k8s.io | false | IngressClass |
| `ingresses` | `ing` | networking.k8s.io | true | Ingress |
| `networkpolicies` | `netpol` | networking.k8s.io | true | NetworkPolicy |
| `runtimeclasses` |  | node.k8s.io | false | RuntimeClass |
| `poddisruptionbudgets` | `pdb` | policy | true | PodDisruptionBudget |
| `podsecuritypolicies` | `psp` | policy | false | PodSecurityPolicy |
| `clusterrolebindings` | | rbac.authorization.k8s.io | false | ClusterRoleBinding |
| `clusterroles` | | rbac.authorization.k8s.io | false | ClusterRole |
| `rolebindings` | | rbac.authorization.k8s.io | true | RoleBinding |
| `roles` | | rbac.authorization.k8s.io | true | Role |
| `priorityclasses` | `pc` | scheduling.k8s.io | false | PriorityClass |
| `csidrivers` | | storage.k8s.io | false | CSIDriver |
| `csinodes` | | storage.k8s.io | false | CSINode |
| `storageclasses` | `sc` | storage.k8s.io | false | StorageClass |
| `volumeattachments` | | storage.k8s.io | false | VolumeAttachment |
-->
| 资源名 | 缩写名 | API 分组 | 按命名空间 | 资源类型 |
|---|---|---|---|---|
| `bindings` | | | true | Binding |
| `componentstatuses` | `cs` | | false | ComponentStatus |
| `configmaps` | `cm` | | true | ConfigMap |
| `endpoints` | `ep` | | true | Endpoints |
| `events` | `ev` | | true | Event |
| `limitranges` | `limits` | | true | LimitRange |
| `namespaces` | `ns` | | false | Namespace |
| `nodes` | `no` | | false | Node |
| `persistentvolumeclaims` | `pvc` | | true | PersistentVolumeClaim |
| `persistentvolumes` | `pv` | | false | PersistentVolume |
| `pods` | `po` | | true | Pod |
| `podtemplates` | | | true | PodTemplate |
| `replicationcontrollers` | `rc` | | true | ReplicationController |
| `resourcequotas` | `quota` | | true | ResourceQuota |
| `secrets` | | | true | Secret |
| `serviceaccounts` | `sa` | | true | ServiceAccount |
| `services` | `svc` | | true | Service |
| `mutatingwebhookconfigurations` | | admissionregistration.k8s.io | false | MutatingWebhookConfiguration |
| `validatingwebhookconfigurations` | | admissionregistration.k8s.io | false | ValidatingWebhookConfiguration |
| `customresourcedefinitions` | `crd,crds` | apiextensions.k8s.io | false | CustomResourceDefinition |
| `apiservices` | | apiregistration.k8s.io | false | APIService |
| `controllerrevisions` | | apps | true | ControllerRevision |
| `daemonsets` | `ds` | apps | true | DaemonSet |
| `deployments` | `deploy` | apps | true | Deployment |
| `replicasets` | `rs` | apps | true | ReplicaSet |
| `statefulsets` | `sts` | apps | true | StatefulSet |
| `tokenreviews` | | authentication.k8s.io | false | TokenReview |
| `localsubjectaccessreviews` | | authorization.k8s.io | true | LocalSubjectAccessReview |
| `selfsubjectaccessreviews` | | authorization.k8s.io | false | SelfSubjectAccessReview |
| `selfsubjectrulesreviews` | | authorization.k8s.io | false | SelfSubjectRulesReview |
| `subjectaccessreviews` | | authorization.k8s.io | false | SubjectAccessReview |
| `horizontalpodautoscalers` | `hpa` | autoscaling | true | HorizontalPodAutoscaler |
| `cronjobs` | `cj` | batch | true | CronJob |
| `jobs` | | batch | true | Job |
| `certificatesigningrequests` | `csr` | certificates.k8s.io | false | CertificateSigningRequest |
| `leases` | | coordination.k8s.io | true | Lease |
| `endpointslices` |  | discovery.k8s.io | true | EndpointSlice |
| `events` | `ev` | events.k8s.io | true | Event |
| `ingresses` | `ing` | extensions | true | Ingress |
| `flowschemas` |  | flowcontrol.apiserver.k8s.io | false | FlowSchema |
| `prioritylevelconfigurations` |  | flowcontrol.apiserver.k8s.io | false | PriorityLevelConfiguration |
| `ingressclasses` |  | networking.k8s.io | false | IngressClass |
| `ingresses` | `ing` | networking.k8s.io | true | Ingress |
| `networkpolicies` | `netpol` | networking.k8s.io | true | NetworkPolicy |
| `runtimeclasses` |  | node.k8s.io | false | RuntimeClass |
| `poddisruptionbudgets` | `pdb` | policy | true | PodDisruptionBudget |
| `podsecuritypolicies` | `psp` | policy | false | PodSecurityPolicy |
| `clusterrolebindings` | | rbac.authorization.k8s.io | false | ClusterRoleBinding |
| `clusterroles` | | rbac.authorization.k8s.io | false | ClusterRole |
| `rolebindings` | | rbac.authorization.k8s.io | true | RoleBinding |
| `roles` | | rbac.authorization.k8s.io | true | Role |
| `priorityclasses` | `pc` | scheduling.k8s.io | false | PriorityClass |
| `csidrivers` | | storage.k8s.io | false | CSIDriver |
| `csinodes` | | storage.k8s.io | false | CSINode |
| `storageclasses` | `sc` | storage.k8s.io | false | StorageClass |
| `volumeattachments` | | storage.k8s.io | false | VolumeAttachment |


<!--
## Output options
-->

## 输出选项

<!--
Use the following sections for information about how you can format or sort the output of certain commands. For details about which commands support the various output options, see the [kubectl](/docs/reference/kubectl/kubectl/) reference documentation.
-->
有关如何格式化或排序某些命令的输出的信息，请使用以下部分。有关哪些命令支持各种输出选项的详细信息，请参阅[kubectl](/zh/docs/reference/kubectl/kubectl/) 参考文档。

<!--
### Formatting output
-->
### 格式化输出

<!--
The default output format for all `kubectl` commands is the human readable plain-text format. To output details to your terminal window in a specific format, you can add either the `-o` or `--output` flags to a supported `kubectl` command.
-->
所有 `kubectl` 命令的默认输出格式都是人类可读的纯文本格式。要以特定格式向终端窗口输出详细信息，可以将 `-o` 或 `--output` 参数添加到受支持的 `kubectl` 命令中。

<!--
#### Syntax
-->
#### 语法

```shell
kubectl [command] [TYPE] [NAME] -o=<output_format>
```

<!--
Depending on the `kubectl` operation, the following output formats are supported:
-->
根据 `kubectl` 操作，支持以下输出格式：

<!--
Output format | Description
--------------| -----------
`-o custom-columns=<spec>` | Print a table using a comma separated list of [custom columns](#custom-columns).
`-o custom-columns-file=<filename>` | Print a table using the [custom columns](#custom-columns) template in the `<filename>` file.
`-o json`     | Output a JSON formatted API object.
`-o jsonpath=<template>` | Print the fields defined in a [jsonpath](/docs/reference/kubectl/jsonpath/) expression.
`-o jsonpath-file=<filename>` | Print the fields defined by the [jsonpath](/docs/reference/kubectl/jsonpath/) expression in the `<filename>` file.
`-o name`     | Print only the resource name and nothing else.
`-o wide`     | Output in the plain-text format with any additional information. For pods, the node name is included.
`-o yaml`     | Output a YAML formatted API object.
-->
Output format | Description
--------------| -----------
`-o custom-columns=<spec>` | 使用逗号分隔的[自定义列](#custom-columns)列表打印表。
`-o custom-columns-file=<filename>` | 使用 `<filename>` 文件中的[自定义列](#custom-columns)模板打印表。
`-o json`     | 输出 JSON 格式的 API 对象
`-o jsonpath=<template>` | 打印 [jsonpath](/zh/docs/reference/kubectl/jsonpath/) 表达式定义的字段
`-o jsonpath-file=<filename>` | 打印 `<filename>` 文件中 [jsonpath](/zh/docs/reference/kubectl/jsonpath/) 表达式定义的字段。
`-o name`     | 仅打印资源名称而不打印任何其他内容。
`-o wide`     | 以纯文本格式输出，包含任何附加信息。对于 pod 包含节点名。
`-o yaml`     | 输出 YAML 格式的 API 对象。


<!--
##### Example
-->

##### 示例

<!--
In this example, the following command outputs the details for a single pod as a YAML formatted object:
-->
在此示例中，以下命令将单个 pod 的详细信息输出为 YAML 格式的对象：

```shell
kubectl get pod web-pod-13je7 -o yaml
```

<!--
Remember: See the [kubectl](/docs/reference/kubectl/kubectl/) reference documentation
for details about which output format is supported by each command.
-->
请记住：有关每个命令支持哪种输出格式的详细信息，请参阅 [kubectl](/zh/docs/reference/kubectl/kubectl/) 参考文档。

<!--
#### Custom columns
-->
#### 自定义列

<!--
To define custom columns and output only the details that you want into a table, you can use the `custom-columns` option. You can choose to define the custom columns inline or use a template file: `-o=custom-columns=<spec>` or `-o=custom-columns-file=<filename>`.
-->
要定义自定义列并仅将所需的详细信息输出到表中，可以使用该 custom-columns 选项。你可以选择内联定义自定义列或使用模板文件：`-o=custom-columns=<spec>` 或 `-o=custom-columns-file=<filename>`。

<!--
##### Examples
-->
##### 示例

<!--
Inline:
-->
内联：

```shell
kubectl get pods <pod-name> -o custom-columns=NAME:.metadata.name,RSRC:.metadata.resourceVersion
```

<!--
Template file:
-->
模板文件：

```shell
kubectl get pods <pod-name> -o custom-columns-file=template.txt
```

<!--
where the `template.txt` file contains:
-->
其中，`template.txt` 文件包含：

```
NAME          RSRC
metadata.name metadata.resourceVersion
```

<!--
The result of running either command is similar to:
-->
运行任何一个命令的结果类似于:

```shell
NAME           RSRC
submit-queue   610995
```

<!--
#### Server-side columns
-->
#### Server-side 列

<!--
`kubectl` supports receiving specific column information from the server about objects.
This means that for any given resource, the server will return columns and rows relevant to that resource, for the client to print.
This allows for consistent human-readable output across clients used against the same cluster, by having the server encapsulate the details of printing.
-->
`kubectl` 支持从服务器接收关于对象的特定列信息。
这意味着对于任何给定的资源，服务器将返回与该资源相关的列和行，以便客户端打印。
通过让服务器封装打印的细节，这允许在针对同一集群使用的客户端之间提供一致的人类可读输出。

<!--
This feature is enabled by default. To disable it, add the
`--server-print=false` flag to the `kubectl get` command.
-->
此功能默认启用。要禁用它，请将该 `--server-print=false` 参数添加到 `kubectl get` 命令中。

<!--
##### Examples
-->
##### 例子：

<!--
To print information about the status of a pod, use a command like the following:
-->
要打印有关 pod 状态的信息，请使用如下命令：

```shell
kubectl get pods <pod-name> --server-print=false
```

<!--
The output is similar to:
-->
输出类似于：

```shell
NAME       AGE
pod-name   1m
```

<!--
### Sorting list objects
-->
### 排序列表对象

<!--
To output objects to a sorted list in your terminal window, you can add the `--sort-by` flag to a supported `kubectl` command. Sort your objects by specifying any numeric or string field with the `--sort-by` flag. To specify a field, use a [jsonpath](/docs/reference/kubectl/jsonpath/) expression.
-->
要将对象排序后输出到终端窗口，可以将 `--sort-by` 参数添加到支持的 `kubectl` 命令。通过使用 `--sort-by` 参数指定任何数字或字符串字段来对对象进行排序。要指定字段，请使用 [jsonpath](/zh/docs/reference/kubectl/jsonpath/) 表达式。

<!--
#### Syntax
-->
#### 语法

```shell
kubectl [command] [TYPE] [NAME] --sort-by=<jsonpath_exp>
```

<!--
##### Example
-->
##### 示例

<!--
To print a list of pods sorted by name, you run:
-->
要打印按名称排序的 pod 列表，请运行：

```shell
kubectl get pods --sort-by=.metadata.name
```

<!--
## Examples: Common operations
-->
## 示例：常用操作

<!--
Use the following set of examples to help you familiarize yourself with running the commonly used `kubectl` operations:
-->
使用以下示例集来帮助你熟悉运行常用 kubectl 操作：

<!--
`kubectl apply` - Apply or Update a resource from a file or stdin.
-->
`kubectl apply` - 以文件或标准输入为准应用或更新资源。

<!--
```shell
# Create a service using the definition in example-service.yaml.
kubectl apply -f example-service.yaml

# Create a replication controller using the definition in example-controller.yaml.
kubectl apply -f example-controller.yaml

# Create the objects that are defined in any .yaml, .yml, or .json file within the <directory> directory.
kubectl apply -f <directory>
```
-->
```shell
# 使用 example-service.yaml 中的定义创建服务。
kubectl apply -f example-service.yaml

# 使用 example-controller.yaml 中的定义创建 replication controller。
kubectl apply -f example-controller.yaml

# 使用 <directory> 路径下的任意 .yaml, .yml, 或 .json 文件 创建对象。
kubectl apply -f <directory>
```

<!--
`kubectl get` - List one or more resources.
-->
`kubectl get` - 列出一个或多个资源。

<!--
# List all pods in plain-text output format.
# List all pods in plain-text output format and include additional information (such as node name).
# List the replication controller with the specified name in plain-text output format. Tip: You can shorten and replace the 'replicationcontroller' resource type with the alias 'rc'.
# List all replication controllers and services together in plain-text output format.
# List all daemon sets, including uninitialized ones, in plain-text output format.
# List all pods running on node server01
-->

```shell
# 以纯文本输出格式列出所有 pod。
kubectl get pods

# 以纯文本输出格式列出所有 pod，并包含附加信息(如节点名)。
kubectl get pods -o wide

# 以纯文本输出格式列出具有指定名称的副本控制器。提示：你可以使用别名 'rc' 缩短和替换 'replicationcontroller' 资源类型。
kubectl get replicationcontroller <rc-name>

# 以纯文本输出格式列出所有副本控制器和服务。
kubectl get rc,services

# 以纯文本输出格式列出所有守护程序集，包括未初始化的守护程序集。
kubectl get ds --include-uninitialized

# 列出在节点 server01 上运行的所有 pod
kubectl get pods --field-selector=spec.nodeName=server01
```

<!--
`kubectl describe` - Display detailed state of one or more resources, including the uninitialized ones by default.
-->
`kubectl describe` - 显示一个或多个资源的详细状态，默认情况下包括未初始化的资源。

<!--
# Display the details of the node with name <node-name>.
kubectl describe nodes <node-name>

# Display the details of the pod with name <pod-name>.
kubectl describe pods/<pod-name>

# Display the details of all the pods that are managed by the replication controller named <rc-name>.
# Remember: Any pods that are created by the replication controller get prefixed with the name of the replication controller.
kubectl describe pods <rc-name>

# Describe all pods, not including uninitialized ones
kubectl describe pods
-->

```shell
# 显示名称为 <node-name> 的节点的详细信息。
kubectl describe nodes <node-name>

# 显示名为 <pod-name> 的 pod 的详细信息。
kubectl describe pods/<pod-name>

# 显示由名为 <rc-name> 的副本控制器管理的所有 pod 的详细信息。
# 记住：副本控制器创建的任何 pod 都以复制控制器的名称为前缀。
kubectl describe pods <rc-name>

# 描述所有的 pod，不包括未初始化的 pod
kubectl describe pods
```

{{< note >}}

<!--
The `kubectl get` command is usually used for retrieving one or more
resources of the same resource type. It features a rich set of flags that allows
you to customize the output format using the `-o` or `--output` flag, for example.
You can specify the `-w` or `--watch` flag to start watching updates to a particular
object. The `kubectl describe` command is more focused on describing the many
related aspects of a specified resource. It may invoke several API calls to the
API server to build a view for the user. For example, the `kubectl describe node`
command retrieves not only the information about the node, but also a summary of
the pods running on it, the events generated for the node etc.
-->
`kubectl get` 命令通常用于检索同一资源类型的一个或多个资源。
它具有丰富的参数，允许你使用 `-o` 或 `--output` 参数自定义输出格式。你可以指定 `-w` 或 `--watch` 参数以开始观察特定对象的更新。
`kubectl describe` 命令更侧重于描述指定资源的许多相关方面。它可以调用对 `API 服务器` 的多个 API 调用来为用户构建视图。
例如，该 `kubectl describe node` 命令不仅检索有关节点的信息，还检索在其上运行的 pod 的摘要，为节点生成的事件等。

{{< /note >}}

<!--
`kubectl delete` - Delete resources either from a file, stdin, or specifying label selectors, names, resource selectors, or resources.
-->
`kubectl delete` - 从文件、stdin 或指定标签选择器、名称、资源选择器或资源中删除资源。

<!--
```shell
# Delete a pod using the type and name specified in the pod.yaml file.
kubectl delete -f pod.yaml

# Delete all the pods and services that have the label '<label-key>=<label-value>'.
kubectl delete pods,services -l <label-key>=<label-value>

# Delete all pods, including uninitialized ones.
kubectl delete pods --all
```

-->

```shell
# 使用 pod.yaml 文件中指定的类型和名称删除 pod。
kubectl delete -f pod.yaml

# 删除所有带有 '<label-key>=<label-value>' 标签的 Pod 和服务。
kubectl delete pods,services -l <label-key>=<label-value>

# 删除所有 pod，包括未初始化的 pod。
kubectl delete pods --all
```

<!--
`kubectl exec` - Execute a command against a container in a pod.
-->
`kubectl exec` - 对 pod 中的容器执行命令。

<!--
# Get output from running 'date' from pod <pod-name>. By default, output is from the first container.
kubectl exec <pod-name> -- date

# Get output from running 'date' in container <container-name> of pod <pod-name>.
kubectl exec <pod-name> -c <container-name> -- date

# Get an interactive TTY and run /bin/bash from pod <pod-name>. By default, output is from the first container.
kubectl exec -ti <pod-name> -- /bin/bash
-->

```shell
# 从 pod <pod-name> 中获取运行 'date' 的输出。默认情况下，输出来自第一个容器。
kubectl exec <pod-name> -- date

# 运行输出 'date' 获取在容器的 <container-name> 中 pod <pod-name> 的输出。
kubectl exec <pod-name> -c <container-name> -- date

# 获取一个交互 TTY 并运行 /bin/bash <pod-name >。默认情况下，输出来自第一个容器。
kubectl exec -ti <pod-name> -- /bin/bash
```

<!--
`kubectl logs` - Print the logs for a container in a pod.
-->
`kubectl logs` - 打印 Pod 中容器的日志。

<!--
# Return a snapshot of the logs from pod <pod-name>.
kubectl logs <pod-name>

# Start streaming the logs from pod <pod-name>. This is similar to the 'tail -f' Linux command.
kubectl logs -f <pod-name>
-->

```shell
# 从 pod 返回日志快照。
kubectl logs <pod-name>

# 从 pod <pod-name> 开始流式传输日志。这类似于 'tail -f' Linux 命令。
kubectl logs -f <pod-name>
```

<!--
## Examples: Creating and using plugins
-->

## 示例：创建和使用插件

<!--
Use the following set of examples to help you familiarize yourself with writing and using `kubectl` plugins:
-->
使用以下示例来帮助你熟悉编写和使用 `kubectl` 插件：

<!--
```shell
# create a simple plugin in any language and name the resulting executable file
# so that it begins with the prefix "kubectl-"
cat ./kubectl-hello
#!/bin/sh

# this plugin prints the words "hello world"
echo "hello world"
```
With a plugin written, let's make it executable:
```bash
chmod a+x ./kubectl-hello

# and move it to a location in our PATH
sudo mv ./kubectl-hello /usr/local/bin
sudo chown root:root /usr/local/bin

# You have now created and "installed" a kubectl plugin.
# You can begin using this plugin by invoking it from kubectl as if it were a regular command
kubectl hello
```
-->
```shell
# 用任何语言创建一个简单的插件，并为生成的可执行文件命名
# 以前缀 "kubectl-" 开始
cat ./kubectl-hello
```

```shell
#!/bin/sh

# 这个插件打印单词 "hello world"
echo "hello world"
```
这个插件写好了，把它变成可执行的：
```bash
sudo chmod a+x ./kubectl-hello

# 并将其移动到路径中的某个位置
sudo mv ./kubectl-hello /usr/local/bin
sudo chown root:root /usr/local/bin

# 你现在已经创建并"安装了"一个 kubectl 插件。
# 你可以开始使用这个插件，从 kubectl 调用它，就像它是一个常规命令一样
kubectl hello
```
```
hello world
```
<!--
```shell
# You can "uninstall" a plugin, by removing it from the folder in your
# $PATH where you placed it
sudo rm /usr/local/bin/kubectl-hello
```
-->
```shell
# 你可以"卸载"一个插件，只需从你的路径中删除它
sudo rm /usr/local/bin/kubectl-hello
```

<!--
In order to view all of the plugins that are available to `kubectl`, use
the `kubectl plugin list` subcommand:
-->
为了查看可用的所有 `kubectl` 插件，你可以使用 `kubectl plugin list` 子命令：
```shell
kubectl plugin list
```
<!--
The output is similar to:
```
The following kubectl-compatible plugins are available:

/usr/local/bin/kubectl-hello
/usr/local/bin/kubectl-foo
/usr/local/bin/kubectl-bar
```
-->
输出类似于：
```
The following kubectl-compatible plugins are available:

/usr/local/bin/kubectl-hello
/usr/local/bin/kubectl-foo
/usr/local/bin/kubectl-bar
```
<!--
`kubectl plugin list` also warns you about plugins that are not
executable, or that are shadowed by other plugins; for example:
```shell
sudo chmod -x /usr/local/bin/kubectl-foo # remove execute permission
kubectl plugin list
```
-->
`kubectl plugin list`指令也可以向你告警哪些插件被运行，或是被其它插件覆盖了,例如:
```shell
sudo chmod -x /usr/local/bin/kubectl-foo # 删除执行权限
kubectl plugin list
```
<!--
```
The following kubectl-compatible plugins are available:

/usr/local/bin/kubectl-hello
/usr/local/bin/kubectl-foo
  - warning: /usr/local/bin/kubectl-foo identified as a plugin, but it is not executable
/usr/local/bin/kubectl-bar

error: one plugin warning was found
```
-->
```
The following kubectl-compatible plugins are available:

/usr/local/bin/kubectl-hello
/usr/local/bin/kubectl-foo
  - warning: /usr/local/bin/kubectl-foo identified as a plugin, but it is not executable
/usr/local/bin/kubectl-bar

error: one plugin warning was found
```

<!--
You can think of plugins as a means to build more complex functionality on top
of the existing kubectl commands:
-->
你可以将插件视为在现有 kubectl 命令之上构建更复杂功能的一种方法：

<!--
```shell
cat ./kubectl-whoami```
-->
```shell
cat ./kubectl-whoami
```

<!--
The next few examples assume that you already made `kubectl-whoami` have
the following contents:
-->
接下来的几个示例假设你已经将 `kubectl-whoami` 设置为以下内容:

<!--
```shell
#!/bin/bash

# this plugin makes use of the `kubectl config` command in order to output
# information about the current user, based on the currently selected context
kubectl config view --template='{{ range .contexts }}{{ if eq .name "'$(kubectl config current-context)'" }}Current user: {{ printf "%s\n" .context.user }}{{ end }}{{ end }}'
```
-->
```shell
#!/bin/bash

#这个插件利用 `kubectl config` 命令基于当前所选上下文输出当前用户的信息
kubectl config view --template='{{ range .contexts }}{{ if eq .name "'$(kubectl config current-context)'" }}Current user: {{ printf "%s\n" .context.user }}{{ end }}{{ end }}'
```

<!--
Running the above command gives you an output containing the user for the
current context in your KUBECONFIG file:
-->
运行以上命令将为你提供一个输出，其中包含 KUBECONFIG 文件中当前上下文的用户:

<!--
```shell
# make the file executable
sudo chmod +x ./kubectl-whoami

# and move it into your PATH
sudo mv ./kubectl-whoami /usr/local/bin

kubectl whoami
Current user: plugins-user
```
-->
```shell
#!/bin/bash
# 使文件成为可执行的
sudo chmod +x ./kubectl-whoami

# 然后移动到你的路径中
sudo mv ./kubectl-whoami /usr/local/bin

kubectl whoami
Current user: plugins-user
```

<!--
To find out more about plugins, take a look at the [example cli plugin](https://github.com/kubernetes/sample-cli-plugin).
-->
要了解关于插件的更多信息，请查看[示例 cli 插件](https://github.com/kubernetes/sample-cli-plugin)。



## {{% heading "whatsnext" %}}


<!--
* Start using the [kubectl](/docs/reference/generated/kubectl/kubectl-commands/) commands.

* To find out more about plugins, take a look at the [example cli plugin](https://github.com/kubernetes/sample-cli-plugin).
-->
* 开始使用 [kubectl](/docs/reference/generated/kubectl/kubectl-commands/) 命令。

* 查看更多[示例 cli 插件](https://github.com/kubernetes/sample-cli-plugin)。
