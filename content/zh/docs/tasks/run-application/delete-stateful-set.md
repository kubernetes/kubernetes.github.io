---
title: 删除 StatefulSet
content_type: task
weight: 60
---

<!--
reviewers:
- bprashanth
- erictune
- foxish
- janetkuo
- smarterclayton
title: Delete a StatefulSet
content_type: task
weight: 60
-->

<!-- overview -->

<!--
This task shows you how to delete a StatefulSet.
-->
本任务展示如何删除 StatefulSet。

## {{% heading "prerequisites" %}}

<!--
* This task assumes you have an application running on your cluster represented by a StatefulSet.
-->
* 本任务假设在你的集群上已经运行了由 StatefulSet 创建的应用。

<!-- steps -->

## 删除 StatefulSet   {#deleting-a-statefulset}

<!--
You can delete a StatefulSet in the same way you delete other resources in Kubernetes: use the `kubectl delete` command, and specify the StatefulSet either by file or by name.
-->
你可以像删除 Kubernetes 中的其他资源一样删除 StatefulSet：使用 `kubectl delete` 命令，并按文件或者名字指定 StatefulSet。

```shell
kubectl delete -f <file.yaml>
```

<!--
```shell
kubectl delete statefulsets <statefulset-name>
```
-->
```shell
kubectl delete statefulsets <statefulset 名称>
```

<!--
You may need to delete the associated headless service separately after the StatefulSet itself is deleted.

```shell
kubectl delete service <service-name>
```
-->
删除 StatefulSet 之后，你可能需要单独删除关联的无头服务。

```shell
kubectl delete service <服务名称>
```

<!--
When deleting a StatefulSet through `kubectl`, the StatefulSet scales down to 0. All Pods that are part of this workload are also deleted. If you want to delete only the StatefulSet and not the Pods, use `--cascade=orphan`.
For example:
--->
当通过 `kubectl` 删除 StatefulSet 时，StatefulSet 会被缩容为 0。
属于该 StatefulSet 的所有 Pod 也被删除。
如果你只想删除 StatefulSet 而不删除 Pod，使用 `--cascade=orphan`。

```shell
kubectl delete -f <file.yaml> --cascade=orphan
```

<!--
By passing `--cascade=orphan` to `kubectl delete`, the Pods managed by the StatefulSet are left behind even after the StatefulSet object itself is deleted. If the pods have a label `app=myapp`, you can then delete them as follows:
--->
通过将 `--cascade=orphan` 传递给 `kubectl delete`，在删除 StatefulSet 对象之后，
StatefulSet 管理的 Pod 会被保留下来。如果 Pod 具有标签 `app=myapp`，则可以按照
如下方式删除它们：

```shell
kubectl delete pods -l app=myapp
```


<!--
### Persistent Volumes

Deleting the Pods in a StatefulSet will not delete the associated volumes. This is to ensure that you have the chance to copy data off the volume before deleting it. Deleting the PVC after the pods have left the [terminating state](/docs/concepts/workloads/pods/pod/#termination-of-pods) might trigger deletion of the backing Persistent Volumes depending on the storage class and reclaim policy. You should never assume ability to access a volume after claim deletion.
-->
### 持久卷  {#persistent-volumes}

删除 StatefulSet 管理的 Pod 并不会删除关联的卷。这是为了确保你有机会在删除卷之前从卷中复制数据。
在 Pod 离开[终止状态](/zh/docs/concepts/workloads/pods/pod-lifecycle/#pod-termination)
后删除 PVC 可能会触发删除背后的 PV 持久卷，具体取决于存储类和回收策略。
永远不要假定在 PVC 删除后仍然能够访问卷。

<!--
Use caution when deleting a PVC, as it may lead to data loss.
-->
{{< note >}}
删除 PVC 时要谨慎，因为这可能会导致数据丢失。
{{< /note >}}

<!--
### Complete deletion of a StatefulSet

To simply delete everything in a StatefulSet, including the associated pods, you can run a series of commands similar to the following:
-->
### 完全删除 StatefulSet  {#complete-deletion-of-a-statefulset}

要删除 StatefulSet 中的所有内容，包括关联的 pods，你可以运行
一系列如下所示的命令：

```shell
grace=$(kubectl get pods <stateful-set-pod> --template '{{.spec.terminationGracePeriodSeconds}}')
kubectl delete statefulset -l app=myapp
sleep $grace
kubectl delete pvc -l app=myapp
```

<!--
In the example above, the Pods have the label `app=myapp`; substitute your own label as appropriate.
-->
在上面的例子中，Pod 的标签为 `app=myapp`；适当地替换你自己的标签。

<!--
### Force deletion of StatefulSet pods

If you find that some pods in your StatefulSet are stuck in the 'Terminating' or 'Unknown' states for an extended period of time, you may need to manually intervene to forcefully delete the pods from the apiserver. This is a potentially dangerous task. Refer to [Deleting StatefulSet Pods](/docs/tasks/manage-stateful-set/delete-pods/) for details.
-->
### 强制删除 StatefulSet 的 Pod

如果你发现 StatefulSet 的某些 Pod 长时间处于 'Terminating' 或者 'Unknown' 状态，
则可能需要手动干预以强制从 API 服务器中删除这些 Pod。
这是一项有点危险的任务。详细信息请阅读
[删除 StatefulSet 类型的 Pods](/zh/docs/tasks/run-application/force-delete-stateful-set-pod/)。

## {{% heading "whatsnext" %}}

<!--
Learn more about [force deleting StatefulSet Pods](/docs/tasks/run-application/force-delete-stateful-set-pod/).
-->
进一步了解[强制删除 StatefulSet 的 Pods](/zh/docs/tasks/run-application/force-delete-stateful-set-pod/)。


