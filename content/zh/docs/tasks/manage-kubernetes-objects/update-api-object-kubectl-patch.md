---
title: 使用 kubectl patch 更新 API 对象
description: 使用 kubectl patch 更新 Kubernetes API 对象。做一个策略性的合并 patch 或 JSON 合并 patch。
content_type: task
weight: 50
---

<!--
title: Update API Objects in Place Using kubectl patch
description: Use kubectl patch to update Kubernetes API objects in place. Do a strategic merge patch or a JSON merge patch.
content_type: task
weight: 40
-->

<!-- overview -->

<!--
This task shows how to use `kubectl patch` to update an API object in place. The exercises
in this task demonstrate a strategic merge patch and a JSON merge patch.
-->
这个任务展示如何使用 `kubectl patch` 就地更新 API 对象。
这个任务中的练习演示了一个策略性合并 patch 和一个 JSON 合并 patch。


## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}

<!-- steps -->

<!--
## Use a strategic merge patch to update a Deployment

Here's the configuration file for a Deployment that has two replicas. Each replica
is a Pod that has one container:
-->
## 使用策略合并 patch 更新 Deployment

下面是具有两个副本的 Deployment 的配置文件。每个副本是一个 Pod，有一个容器：

{{< codenew file="application/deployment-patch.yaml" >}}

<!--
Create the Deployment:
-->
创建 Deployment：

```shell
kubectl create -f https://k8s.io/examples/application/deployment-patch.yaml
```

<!--
View the Pods associated with your Deployment:
-->
查看与 Deployment 相关的 Pod：

```shell
kubectl get pods
```

<!--
The output shows that the Deployment has two Pods. The `1/1` indicates that
each Pod has one container:
-->
输出显示 Deployment 有两个 Pod。`1/1` 表示每个 Pod 有一个容器:

```
NAME                        READY     STATUS    RESTARTS   AGE
patch-demo-28633765-670qr   1/1       Running   0          23s
patch-demo-28633765-j5qs3   1/1       Running   0          23s
```

<!--
Make a note of the names of the running Pods. Later, you will see that these Pods
get terminated and replaced by new ones.
-->
把运行的 Pod 的名字记下来。稍后，你将看到这些 Pod 被终止并被新的 Pod 替换。

<!--
At this point, each Pod has one Container that runs the nginx image. Now suppose
you want each Pod to have two containers: one that runs nginx and one that runs redis.
-->
此时，每个 Pod 都有一个运行 nginx 镜像的容器。现在假设你希望每个 Pod 有两个容器：一个运行 nginx，另一个运行 redis。

<!--
Create a file named `patch-file-containers.yaml` that has this content:
-->
创建一个名为 `patch-file-containers.yaml` 的文件。内容如下:

```yaml
spec:
  template:
    spec:
      containers:
      - name: patch-demo-ctr-2
        image: redis
```

<!--
Patch your Deployment:
-->
修补你的 Deployment：

```shell
kubectl patch deployment patch-demo --patch "$(cat patch-file-containers.yaml)"
```
<!--
View the patched Deployment:
-->
查看修补后的 Deployment：

```shell
kubectl get deployment patch-demo --output yaml
```

<!--
The output shows that the PodSpec in the Deployment has two Containers:
-->
输出显示 Deployment 中的 PodSpec 有两个容器:

```yaml
containers:
- image: redis
  imagePullPolicy: Always
  name: patch-demo-ctr-2
  ...
- image: nginx
  imagePullPolicy: Always
  name: patch-demo-ctr
  ...
```

<!--
View the Pods associated with your patched Deployment:
-->
查看与 patch Deployment 相关的 Pod:

```shell
kubectl get pods
```

<!--
The output shows that the running Pods have different names from the Pods that
were running previously. The Deployment terminated the old Pods and created two
new Pods that comply with the updated Deployment spec. The `2/2` indicates that
each Pod has two Containers:
-->
输出显示正在运行的 Pod 与以前运行的 Pod 有不同的名称。Deployment 终止了旧的 Pod，并创建了两个
符合更新的部署规范的新 Pod。`2/2` 表示每个 Pod 有两个容器:

```
NAME                          READY     STATUS    RESTARTS   AGE
patch-demo-1081991389-2wrn5   2/2       Running   0          1m
patch-demo-1081991389-jmg7b   2/2       Running   0          1m
```

<!--
Take a closer look at one of the patch-demo Pods:
-->
仔细查看其中一个 patch-demo Pod:

```shell
kubectl get pod <your-pod-name> --output yaml
```

<!--
The output shows that the Pod has two Containers: one running nginx and one running redis:
-->
输出显示 Pod 有两个容器:一个运行 nginx，一个运行 redis:

```
containers:
- image: redis
  ...
- image: nginx
  ...
```

<!--
### Notes on the strategic merge patch

The patch you did in the preceding exercise is called a *strategic merge patch*.
Notice that the patch did not replace the `containers` list. Instead it added a new
Container to the list. In other words, the list in the patch was merged with the
existing list. This is not always what happens when you use a strategic merge patch on a list.
In some cases, the list is replaced, not merged.
-->
### 策略性合并类的 patch 的说明

你在前面的练习中所做的 patch 称为`策略性合并 patch（Strategic Merge Patch)`。
请注意，patch 没有替换`containers` 列表。相反，它向列表中添加了一个新 Container。换句话说，
patch 中的列表与现有列表合并。当你在列表中使用策略性合并 patch 时，并不总是这样。
在某些情况下，列表是替换的，而不是合并的。

<!--
With a strategic merge patch, a list is either replaced or merged depending on its
patch strategy. The patch strategy is specified by the value of the `patchStrategy` key
in a field tag in the Kubernetes source code. For example, the `Containers` field of `PodSpec`
struct has a `patchStrategy` of `merge`:
-->
对于策略性合并 patch，列表可以根据其 patch 策略进行替换或合并。
patch 策略由 Kubernetes 源代码中字段标记中的 `patchStrategy` 键的值指定。
例如，`PodSpec` 结构体的 `Containers` 字段的 `patchStrategy` 为 `merge`：

```go
type PodSpec struct {
  ...
  Containers []Container `json:"containers" patchStrategy:"merge" patchMergeKey:"name" ...`
```

<!--
You can also see the patch strategy in the
[OpenApi spec](https://raw.githubusercontent.com/kubernetes/kubernetes/master/api/openapi-spec/swagger.json):
-->
你还可以在 [OpenApi spec](https://raw.githubusercontent.com/kubernetes/kubernetes/master/api/openapi-spec/swagger.json)
规范中看到 patch 策略：

```json
"io.k8s.api.core.v1.PodSpec": {
    ...
     "containers": {
      "description": "List of containers belonging to the pod. ...
      },
      "x-kubernetes-patch-merge-key": "name",
      "x-kubernetes-patch-strategy": "merge"
     },
```

<!--
And you can see the patch strategy in the
[Kubernetes API documentation](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#podspec-v1-core).
-->
你可以在 [Kubernetes API 文档](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#podspec-v1-core)
中看到 patch 策略。

<!--
Create a file named `patch-file-tolerations.yaml` that has this content:
-->
创建一个名为 `patch-file-tolerations.yaml` 的文件。内容如下:

```yaml
spec:
  template:
    spec:
      tolerations:
      - effect: NoSchedule
        key: disktype
        value: ssd
```

<!--
Patch your Deployment:
-->
对 Deployment 执行 patch 操作：

```
kubectl patch deployment patch-demo --patch "$(cat patch-file-containers.yaml)"
```

<!--
View the patched Deployment:
-->
查看修补后的 Deployment：

```shell
kubectl get deployment patch-demo --output yaml
```

<!--
The output shows that the PodSpec in the Deployment has only one Toleration:
-->
输出结果显示 Deployment 中的 PodSpec 只有一个容忍度设置：

```shell

containers:
- image: redis
  imagePullPolicy: Always
  name: patch-demo-ctr-2
  ...
- image: nginx
  imagePullPolicy: Always
  name: patch-demo-ctr
  ...
```
```shell


tolerations:
      - effect: NoSchedule
        key: disktype
        value: ssd
```

<!--
Notice that the `tolerations` list in the PodSpec was replaced, not merged. This is because
the Tolerations field of PodSpec does not have a `patchStrategy` key in its field tag. So the
strategic merge patch uses the default patch strategy, which is `replace`.
-->
请注意，PodSpec 中的 `tolerations` 列表被替换，而不是合并。这是因为 PodSpec 的 `tolerations` 
的字段标签中没有 `patchStrategy` 键。所以策略合并 patch 操作使用默认的 patch 策略，也就是 `replace`。

```go
type PodSpec struct {
  ...
  Tolerations []Toleration `json:"tolerations,omitempty" protobuf:"bytes,22,opt,name=tolerations"`
```

<!--
## Use a JSON merge patch to update a Deployment

A strategic merge patch is different from a
[JSON merge patch](https://tools.ietf.org/html/rfc7386).
With a JSON merge patch, if you
want to update a list, you have to specify the entire new list. And the new list completely
replaces the existing list.
-->
## 使用 JSON 合并 patch 更新 Deployment

策略性合并 patch 不同于 [JSON 合并 patch](https://tools.ietf.org/html/rfc7386)。
使用 JSON 合并 patch，如果你想更新列表，你必须指定整个新列表。新的列表完全取代现有的列表。

<!--
The `kubectl patch` command has a `type` parameter that you can set to one of these values:
-->
`kubectl patch` 命令有一个 `type` 参数，你可以将其设置为以下值之一:

<table>
  <!-- tr><th>Parameter value</th><th>Merge type</th></tr -->
  <tr><th>参数值</th><th>合并类型</th></tr>
  <tr><td>json</td><td><a href="https://tools.ietf.org/html/rfc6902">JSON Patch, RFC 6902</a></td></tr>
  <tr><td>merge</td><td><a href="https://tools.ietf.org/html/rfc7386">JSON Merge Patch, RFC 7386</a></td></tr>
  <!-- tr><td>strategic</td><td>Strategic merge patch</td></tr -->
  <tr><td>strategic</td><td>策略合并 patch</td></tr>
</table>

<!--
For a comparison of JSON patch and JSON merge patch, see
[JSON Patch and JSON Merge Patch](https://erosb.github.io/post/json-patch-vs-merge-patch/).
-->
有关 JSON patch 和 JSON 合并 patch 的比较，查看
[JSON patch 和 JSON 合并 patch](https://erosb.github.io/post/json-patch-vs-merge-patch/)。

<!--
The default value for the `type` parameter is `strategic`. So in the preceding exercise, you
did a strategic merge patch.
-->
`type` 参数的默认值是 `strategic`。在前面的练习中，我们做了一个策略性的合并 patch。

<!--
Next, do a JSON merge patch on your same Deployment. Create a file named `patch-file-2.yaml`
that has this content:
-->
下一步，在相同的 Deployment 上执行 JSON 合并 patch。创建一个名为 `patch-file-2` 的文件。内容如下:

```yaml
spec:
  template:
    spec:
      containers:
      - name: patch-demo-ctr-3
        image: gcr.io/google-samples/node-hello:1.0
```

<!--
In your patch command, set `type` to `merge`:
-->
在 patch 命令中，将 `type` 设置为 `merge`：

```shell
kubectl patch deployment patch-demo --type merge --patch "$(cat patch-file-2.yaml)"
```

<!--
View the patched Deployment:
-->
查看修补后的 Deployment：

```shell
kubectl get deployment patch-demo --output yaml
```

<!--
The `containers` list that you specified in the patch has only one Container.
The output shows that your list of one Container replaced the existing `containers` list.
-->
patch 中指定的`containers`列表只有一个 Container。
输出显示你所给出的 Contaier 列表替换了现有的 `containers` 列表。

```yaml
spec:
  containers:
  - image: gcr.io/google-samples/node-hello:1.0
    ...
    name: patch-demo-ctr-3
```

<!--
List the running Pods:
-->
列表中运行的 Pod：

```shell
kubectl get pods
```

<!--
In the output, you can see that the existing Pods were terminated, and new Pods
were created. The `1/1` indicates that each new Pod is running only one Container.
-->
在输出中，你可以看到已经终止了现有的 Pod，并创建了新的 Pod。`1/1` 表示每个新 Pod只运行一个容器。

```shell
NAME                          READY     STATUS    RESTARTS   AGE
patch-demo-1307768864-69308   1/1       Running   0          1m
patch-demo-1307768864-c86dc   1/1       Running   0          1m
```

<!--
## Use strategic merge patch to update a Deployment using the retainKeys strategy

Here's the configuration file for a Deployment that uses the `RollingUpdate` strategy:
-->
## 使用带 retainKeys 策略的策略合并 patch 更新 Deployment

{{< codenew file="application/deployment-retainkeys.yaml" >}}

<!-- Create the deployment: -->
创建 Deployment：

```shell
kubectl apply -f https://k8s.io/examples/application/deployment-retainkeys.yaml
```

<!--
At this point, the deployment is created and is using the `RollingUpdate` strategy.

Create a file named `patch-file-no-retainkeys.yaml` that has this content:
-->
这时，Deployment 被创建，并使用 `RollingUpdate` 策略。

创建一个名为 `patch-file-no-retainkeys.yaml` 的文件，内容如下：

```yaml
spec:
  strategy:
    type: Recreate
```

<!-- Patch your Deployment: -->
修补你的 Deployment:

{{< tabs name="kubectl_retainkeys_example" >}}
{{{< tab name="Bash" codelang="bash" >}}
kubectl patch deployment retainkeys-demo --type strategic --patch "$(cat patch-file-no-retainkeys.yaml)"
{{< /tab >}}
{{< tab name="PowerShell" codelang="posh" >}}
kubectl patch deployment retainkeys-demo --type strategic --patch $(Get-Content patch-file-no-retainkeys.yaml -Raw)
{{< /tab >}}}
{{< /tabs >}}

<!--
In the output, you can see that it is not possible to set `type` as `Recreate` when a value is defined for `spec.strategy.rollingUpdate`:
-->
在输出中，你可以看到，当 `spec.strategy.rollingUpdate` 已经拥有取值定义时，
将其 `type` 设置为 `Recreate` 是不可能的。

```shell
The Deployment "retainkeys-demo" is invalid: spec.strategy.rollingUpdate: Forbidden: may not be specified when strategy `type` is 'Recreate'
```

<!--
The way to remove the value for `spec.strategy.rollingUpdate` when updating the value for `type` is to use the `retainKeys` strategy for the strategic merge.

Create another file named `patch-file-retainkeys.yaml` that has this content:
-->
更新 `type` 取值的同时移除 `spec.strategy.rollingUpdate` 现有值的方法是
为策略性合并操作设置 `retainKeys` 策略：

创建另一个名为 `patch-file-retainkeys.yaml` 的文件，内容如下：

```yaml
spec:
  strategy:
    $retainKeys:
    - type
    type: Recreate
```

<!--
With this patch, we indicate that we want to retain only the `type` key of the `strategy` object. Thus, the `rollingUpdate` will be removed during the patch operation.

Patch your Deployment again with this new patch:
-->
使用此 patch，我们表达了希望只保留 `strategy` 对象的 `type` 键。
这样，在 patch 操作期间 `rollingUpdate` 会被删除。

使用新的 patch 重新修补 Deployment：

{{< tabs name="kubectl_retainkeys2_example" >}}
{{{< tab name="Bash" codelang="bash" >}}
kubectl patch deployment retainkeys-demo --type merge --patch "$(cat patch-file-retainkeys.yaml)"
{{< /tab >}}
{{< tab name="PowerShell" codelang="posh" >}}
kubectl patch deployment retainkeys-demo --type merge --patch $(Get-Content patch-file-retainkeys.yaml -Raw)
{{< /tab >}}}
{{< /tabs >}}

<!-- Examine the content of the Deployment: -->
检查 Deployment 的内容：

```shell
kubectl get deployment retainkeys-demo --output yaml
```

<!--
The output shows that the strategy object in the Deployment does not contain the `rollingUpdate` key anymore:
-->
输出显示 Deployment 中的 `strategy` 对象不再包含 `rollingUpdate` 键：

```shell
spec:
  strategy:
    type: Recreate
  template:
```

<!--
### Notes on the strategic merge patch using the retainKeys strategy

The patch you did in the preceding exercise is called a *strategic merge patch with retainKeys strategy*. This method introduces a new directive `$retainKeys` that has the following strategies:

- It contains a list of strings.
- All fields needing to be preserved must be present in the `$retainKeys` list.
- The fields that are present will be merged with live object.
- All of the missing fields will be cleared when patching.
- All fields in the `$retainKeys` list must be a superset or the same as the fields present in the patch.
-->
### 关于使用 retainKeys 策略的策略合并 patch 操作的说明

在前文练习中所执行的称作 *带 `retainKeys` 策略的策略合并 patch（Strategic Merge
Patch with retainKeys Strategy）*。
这种方法引入了一种新的 `$retainKey` 指令，具有如下策略： 

- 其中包含一个字符串列表；
- 所有需要被保留的字段必须在 `$retainKeys` 列表中给出；
- 对于已有的字段，会和对象上对应的内容合并；
- 在修补操作期间，未找到的字段都会被清除；
- 列表 `$retainKeys` 中的所有字段必须 patch 操作所给字段的超集，或者与之完全一致。

<!--
The `retainKeys` strategy does not work for all objects. It only works when the value of the `patchStrategy` key in a field tag in the Kubernetes source code contains `retainKeys`. For example, the `Strategy` field of the `DeploymentSpec` struct has a `patchStrategy` of `retainKeys`:
-->
策略 `retainKeys` 并不能对所有对象都起作用。它仅对那些 Kubernetes 源码中
`patchStrategy` 字段标志值包含 `retainKeys` 的字段有用。
例如 `DeploymentSpec` 结构的 `Strategy` 字段就包含了 `patchStrategy` 为
`retainKeys` 的标志。 

```go
type DeploymentSpec struct {
  ...
  // +patchStrategy=retainKeys
  Strategy DeploymentStrategy `json:"strategy,omitempty" patchStrategy:"retainKeys" ...`
```

<!--
You can also see the `retainKeys` strategy in the [OpenApi spec](https://raw.githubusercontent.com/kubernetes/kubernetes/master/api/openapi-spec/swagger.json):
-->
你也可以查看 [OpenAPI 规范](https://raw.githubusercontent.com/kubernetes/kubernetes/master/api/openapi-spec/swagger.json)中的 `retainKeys` 策略：

```json
"io.k8s.api.apps.v1.DeploymentSpec": {
   ...
  "strategy": {
    "$ref": "#/definitions/io.k8s.api.apps.v1.DeploymentStrategy",
    "description": "The deployment strategy to use to replace existing pods with new ones.",
    "x-kubernetes-patch-strategy": "retainKeys"
  },
```

<!--
And you can see the `retainKeys` strategy in the
[Kubernetes API documentation](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#deploymentspec-v1-apps).
-->
而且你也可以在
[Kubernetes API 文档](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#deploymentspec-v1-apps).
中看到 `retainKey` 策略。

<!--
## Alternate forms of the kubectl patch command

The `kubectl patch` command takes YAML or JSON. It can take the patch as a file or
directly on the command line.
-->
## kubectl patch 命令的其他形式

`kubectl patch` 命令使用 YAML 或 JSON。它可以接受以文件形式提供的补丁，也可以
接受直接在命令行中给出的补丁。

<!--
Create a file named `patch-file.json` that has this content:
-->
创建一个文件名称是 `patch-file.json` 内容如下：

```json
{
   "spec": {
      "template": {
         "spec": {
            "containers": [
               {
                  "name": "patch-demo-ctr-2",
                  "image": "redis"
               }
            ]
         }
      }
   }
}
```

<!--
The following commands are equivalent:
-->
以下命令是等价的：

```shell
kubectl patch deployment patch-demo --patch "$(cat patch-file.yaml)"
kubectl patch deployment patch-demo --patch 'spec:\n template:\n  spec:\n   containers:\n   - name: patch-demo-ctr-2\n     image: redis'

kubectl patch deployment patch-demo --patch "$(cat patch-file.json)"
kubectl patch deployment patch-demo --patch '{"spec": {"template": {"spec": {"containers": [{"name": "patch-demo-ctr-2","image": "redis"}]}}}}'
```

<!--
## Summary

In this exercise, you used `kubectl patch` to change the live configuration
of a Deployment object. You did not change the configuration file that you originally used to
create the Deployment object. Other commands for updating API objects include
[kubectl annotate](/docs/reference/generated/kubectl/kubectl-commands/#annotate),
[kubectl edit](/docs/reference/generated/kubectl/kubectl-commands/#edit),
[kubectl replace](/docs/reference/generated/kubectl/kubectl-commands/#replace),
[kubectl scale](/docs/reference/generated/kubectl/kubectl-commands/#scale),
and
[kubectl apply](/docs/reference/generated/kubectl/kubectl-commands/#apply).
-->
## 总结

在本练习中，你使用 `kubectl patch` 更改了 Deployment 对象的当前配置。
你没有更改最初用于创建 Deployment 对象的配置文件。
用于更新 API 对象的其他命令包括
[`kubectl annotate`](/docs/reference/generated/kubectl/kubectl-commands/#annotate)，
[`kubectl edit`](/docs/reference/generated/kubectl/kubectl-commands/#edit)，
[`kubectl replace`](/docs/reference/generated/kubectl/kubectl-commands/#replace)，
[`kubectl scale`](/docs/reference/generated/kubectl/kubectl-commands/#scale)，
和
[`kubectl apply`](/docs/reference/generated/kubectl/kubectl-commands/#apply)。


<!--
{{< note >}}
Strategic merge patch is not supported for custom resources.
{{< /note >}}
-->
{{< note >}}
定制资源不支持策略性合并 patch。
{{< /note >}}


## {{% heading "whatsnext" %}}

<!--
* [Kubernetes Object Management](/docs/concepts/overview/working-with-objects/object-management/)
* [Managing Kubernetes Objects Using Imperative Commands](/docs/tasks/manage-kubernetes-objects/imperative-command/)
* [Imperative Management of Kubernetes Objects Using Configuration Files](/docs/tasks/manage-kubernetes-objects/imperative-config/)
* [Declarative Management of Kubernetes Objects Using Configuration Files](/docs/tasks/manage-kubernetes-objects/declarative-config/)
-->
* [Kubernetes 对象管理](/zh/docs/concepts/overview/working-with-objects/object-management/)
* [使用指令式命令管理 Kubernetes 对象](/zh/docs/tasks/manage-kubernetes-objects/imperative-command/)
* [使用配置文件执行 Kubernetes 对象的指令式管理](/zh/docs/tasks/manage-kubernetes-objects/imperative-config)
* [使用配置文件对 Kubernetes 对象进行声明式管理](/zh/docs/tasks/manage-kubernetes-objects/declarative-config/)




