---
reviewers:
- eparis
- pmorie
title: 使用 ConfigMap 来配置 Redis
content_type: tutorial
---

<!-- overview -->

<!--
This page provides a real world example of how to configure Redis using a ConfigMap and builds upon the [Configure Containers Using a ConfigMap](/docs/tasks/configure-pod-container/configure-pod-configmap/) task.
-->
这篇文档基于[使用 ConfigMap 来配置 Containers](/zh/docs/tasks/configure-pod-container/configure-pod-configmap/) 这个任务，提供了一个使用 ConfigMap 来配置 Redis 的真实案例。



## {{% heading "objectives" %}}


<!--
* Create a ConfigMap with Redis configuration values
* Create a Redis Pod that mounts and uses the created ConfigMap
* Verify that the configuration was correctly applied.
-->

* 使用 Redis 配置的值创建一个 ConfigMap
* 创建一个 Redis Pod，挂载并使用创建的 ConfigMap
* 验证配置已经被正确应用。





## {{% heading "prerequisites" %}}


* {{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}
<!--
* The example shown on this page works with `kubectl` 1.14 and above.
* Understand [Configure Containers Using a ConfigMap](/docs/tasks/configure-pod-container/configure-pod-configmap/).
-->
* 此页面上显示的示例适用于 `kubectl` 1.14和在其以上的版本。
* 理解[使用ConfigMap来配置Containers](/zh/docs/tasks/configure-pod-container/configure-pod-configmap/)。



<!-- lessoncontent -->


<!--
## Real World Example: Configuring Redis using a ConfigMap

Follow the steps below to configure a Redis cache using data stored in a ConfigMap.

First create a ConfigMap with an empty configuration block:
-->
## 真实世界的案例：使用 ConfigMap 来配置 Redis

按照下面的步骤，使用 ConfigMap 中的数据来配置 Redis 缓存。

首先创建一个配置模块为空的 ConfigMap：

```shell
cat <<EOF >./example-redis-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: example-redis-config
data:
  redis-config: ""
EOF
```

<!--
Apply the ConfigMap created above, along with a Redis pod manifest:
-->
应用上面创建的 ConfigMap 以及 Redis pod 清单：

```shell
kubectl apply -f example-redis-config.yaml
kubectl apply -f https://raw.githubusercontent.com/kubernetes/website/master/content/en/examples/pods/config/redis-pod.yaml
```

<!--
Examine the contents of the Redis pod manifest and note the following:

* A volume named `config` is created by `spec.volumes[1]`
* The `key` and `path` under `spec.volumes[1].items[0]` exposes the `redis-config` key from the 
  `example-redis-config` ConfigMap as a file named `redis.conf` on the `config` volume.
* The `config` volume is then mounted at `/redis-master` by `spec.containers[0].volumeMounts[1]`.

This has the net effect of exposing the data in `data.redis-config` from the `example-redis-config`
ConfigMap above as `/redis-master/redis.conf` inside the Pod.
-->
检查 Redis pod 清单的内容，并注意以下几点：

* 由 `spec.volumes[1]` 创建一个名为 `config` 的卷。
* `spec.volumes[1].items[0]` 下的 `key` 和 `path` 会将来自 `example-redis-config`
  ConfigMap 中的 `redis-config` 密钥公开在 `config` 卷上一个名为 `redis.conf` 的文件中。
* 然后 `config` 卷被 `spec.containers[0].volumeMounts[1]` 挂载在 `/redis-master`。

这样做的最终效果是将上面 `example-redis-config` 配置中 `data.redis-config` 的数据作为 Pod 中的 `/redis-master/redis.conf` 公开。

{{< codenew file="pods/config/redis-pod.yaml" >}}

<!-- 
Examine the created objects: 
-->
检查创建的对象：

```shell
kubectl get pod/redis configmap/example-redis-config 
```

<!--
You should see the following output:
-->
你应该可以看到以下输出：

```shell
NAME        READY   STATUS    RESTARTS   AGE
pod/redis   1/1     Running   0          8s

NAME                             DATA   AGE
configmap/example-redis-config   1      14s
```

<!--
Recall that we left `redis-config` key in the `example-redis-config` ConfigMap blank: 
-->
回顾一下，我们在 `example-redis-config` ConfigMap 保留了空的 `redis-config` 键：

```shell
kubectl describe configmap/example-redis-config
```

<!--
You should see an empty `redis-config` key:
-->
你应该可以看到一个空的 `redis-config` 键：

```shell
Name:         example-redis-config
Namespace:    default
Labels:       <none>
Annotations:  <none>

Data
====
redis-config:
```

<!--
Use `kubectl exec` to enter the pod and run the `redis-cli` tool to check the current configuration:
-->
使用 `kubectl exec` 进入 pod，运行 `redis-cli` 工具检查当前配置：

```shell
kubectl exec -it redis -- redis-cli
```

<!--
Check `maxmemory`:
-->
查看 `maxmemory`：

```shell
127.0.0.1:6379> CONFIG GET maxmemory
```

<!--
It should show the default value of 0:
-->
它应该显示默认值 0：

```shell
1) "maxmemory"
2) "0"
```

<!--
Similarly, check `maxmemory-policy`:
-->
同样，查看 `maxmemory-policy`：

```shell
127.0.0.1:6379> CONFIG GET maxmemory-policy
```

<!--
Which should also yield its default value of `noeviction`:
-->
它也应该显示默认值 `noeviction`：

```shell
1) "maxmemory-policy"
2) "noeviction"
```

<!--
Now let's add some configuration values to the `example-redis-config` ConfigMap:
-->
现在，向 `example-redis-config` ConfigMap 添加一些配置：

{{< codenew file="pods/config/example-redis-config.yaml" >}}

<!--
Apply the updated ConfigMap:
-->
应用更新的 ConfigMap:

```shell
kubectl apply -f example-redis-config.yaml
```

<!--
Confirm that the ConfigMap was updated:
-->
确认 ConfigMap 已更新：

```shell
kubectl describe configmap/example-redis-config
```

<!--
You should see the configuration values we just added:
-->
你应该可以看到我们刚刚添加的配置：

```shell
Name:         example-redis-config
Namespace:    default
Labels:       <none>
Annotations:  <none>

Data
====
redis-config:
----
maxmemory 2mb
maxmemory-policy allkeys-lru
```

<!--
Check the Redis Pod again using `redis-cli` via `kubectl exec` to see if the configuration was applied:
-->
通过 `kubectl exec` 使用 `redis-cli` 再次检查 Redis Pod，查看是否已应用配置：

```shell
kubectl exec -it redis -- redis-cli
```

<!--
Check `maxmemory`:
-->
查看 `maxmemory`：

```shell
127.0.0.1:6379> CONFIG GET maxmemory
```

<!--
It remains at the default value of 0:
-->
它保持默认值 0：

```shell
1) "maxmemory"
2) "0"
```

<!--
Similarly, `maxmemory-policy` remains at the `noeviction` default setting:
-->
同样，`maxmemory-policy` 保留为默认设置 `noeviction`：

```shell
127.0.0.1:6379> CONFIG GET maxmemory-policy
```

<!--
Returns:
-->
返回：

```shell
1) "maxmemory-policy"
2) "noeviction"
```

<!--
The configuration values have not changed because the Pod needs to be restarted to grab updated
values from associated ConfigMaps. Let's delete and recreate the Pod:
-->
配置值未更改，因为需要重新启动 Pod 才能从关联的 ConfigMap 中获取更新的值。
让我们删除并重新创建 Pod：

```shell
kubectl delete pod redis
kubectl apply -f https://raw.githubusercontent.com/kubernetes/website/master/content/en/examples/pods/config/redis-pod.yaml
```

<!--
Now re-check the configuration values one last time:
-->
现在，最后一次重新检查配置值：

```shell
kubectl exec -it redis -- redis-cli
```

<!--
Check `maxmemory`:
-->
查看 `maxmemory`：

```shell
127.0.0.1:6379> CONFIG GET maxmemory
```

<!--
It should now return the updated value of 2097152:
-->
现在，它应该返回更新后的值 2097152：

```shell
1) "maxmemory"
2) "2097152"
```

<!--
Similarly, `maxmemory-policy` has also been updated:
-->
同样，`maxmemory-policy` 也已更新：

```shell
127.0.0.1:6379> CONFIG GET maxmemory-policy
```

<!--
It now reflects the desired value of `allkeys-lru`:
-->
现在它反映了期望值 `allkeys-lru`：

```shell
1) "maxmemory-policy"
2) "allkeys-lru"
```

<!--
Clean up your work by deleting the created resources:
-->
删除创建的资源，清理你的工作：

```shell
kubectl delete pod/redis configmap/example-redis-config
```

## {{% heading "whatsnext" %}}


<!--
* Learn more about [ConfigMaps](/docs/tasks/configure-pod-container/configure-pod-configmap/).
-->
* 了解有关 [ConfigMaps](/zh/docs/tasks/configure-pod-container/configure-pod-configmap/)的更多信息。



