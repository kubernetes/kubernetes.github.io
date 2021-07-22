---
title: 定义相互依赖的环境变量
content_type: task
weight: 20
---
<!-- 
title: Define Dependent Environment Variables
-->

<!-- overview -->

<!-- 
This page shows how to define dependent environment variables for a container
in a Kubernetes Pod.
-->
本页展示了如何为 Kubernetes Pod 中的容器定义相互依赖的环境变量。

## {{% heading "prerequisites" %}}


{{< include "task-tutorial-prereqs.md" >}}


<!-- steps -->

<!-- 
## Define an environment dependent variable for a container

When you create a Pod, you can set dependent environment variables for the containers that run in the Pod. To set dependent environment variables, you can use $(VAR_NAME) in the `value` of `env` in the configuration file.

In this exercise, you create a Pod that runs one container. The configuration
file for the Pod defines an dependent environment variable with common usage defined. Here is the configuration manifest for the
Pod:
-->
## 为容器定义相互依赖的环境变量   {#define-an-environment-dependent-variable-for-a-container}

当创建一个 Pod 时，你可以为运行在 Pod 中的容器设置相互依赖的环境变量。 
设置相互依赖的环境变量，你就可以在配置清单文件的 `env` 的 `value` 中使用 $(VAR_NAME)。

在本练习中，你会创建一个单容器的 Pod。
此 Pod 的配置文件定义了一个已定义常用用法的相互依赖的环境变量。
下面是 Pod 的配置清单：

{{< codenew file="pods/inject/dependent-envars.yaml" >}}

<!-- 1. Create a Pod based on that manifest: -->
1. 依据清单创建 Pod：
    ```shell
    kubectl apply -f https://k8s.io/examples/pods/inject/dependent-envars.yaml
    ```
    ```
    pod/dependent-envars-demo created
    ```
    <!-- 2. List the running Pods: -->
2. 列出运行的 Pod：

    ```shell
    kubectl get pods dependent-envars-demo
    ```
    ```
    NAME                      READY     STATUS    RESTARTS   AGE
    dependent-envars-demo     1/1       Running   0          9s
    ```

    <!-- 3. Check the logs for the container running in your Pod: -->
3. 检查 Pod 中运行容器的日志：

    ```shell
    kubectl logs pod/dependent-envars-demo
    ```
    ```

    UNCHANGED_REFERENCE=$(PROTOCOL)://172.17.0.1:80
    SERVICE_ADDRESS=https://172.17.0.1:80
    ESCAPED_REFERENCE=$(PROTOCOL)://172.17.0.1:80
    ```

<!-- 
As shown above, you have defined the correct dependency reference of `SERVICE_ADDRESS`, bad dependency reference of `UNCHANGED_REFERENCE` and skip dependent references of `ESCAPED_REFERENCE`.

When an environment variable is already defined when being referenced,
the reference can be correctly resolved, such as in the `SERVICE_ADDRESS` case.
-->
如上所示，你已经定义了 `SERVICE_ADDRESS` 的正确依赖引用，
`UNCHANGED_REFERENCE` 的错误依赖引用，
并跳过了 `ESCAPED_REFERENCE` 的依赖引用。

如果环境变量被引用时已事先定义，则引用可以正确解析，
比如 `SERVICE_ADDRESS` 的例子。

<!-- 
When the environment variable is undefined or only includes some variables, the undefined environment variable is treated as a normal string, such as `UNCHANGED_REFERENCE`. Note that incorrectly parsed environment variables, in general, will not block the container from starting.

The `$(VAR_NAME)` syntax can be escaped with a double `$`, ie: `$$(VAR_NAME)`.
Escaped references are never expanded, regardless of whether the referenced variable
is defined or not. This can be seen from the `ESCAPED_REFERENCE` case above.
-->
当环境变量未定义或仅包含部分变量时，未定义的变量会被当做普通字符串对待，
比如 `UNCHANGED_REFERENCE` 的例子。
注意，解析不正确的环境变量通常不会阻止容器启动。

`$(VAR_NAME)` 这样的语法可以用两个 `$` 转义，即：`$$(VAR_NAME)`。
无论引用的变量是否定义，转义的引用永远不会展开。
这一点可以从上面 `ESCAPED_REFERENCE` 的例子得到印证。

## {{% heading "whatsnext" %}}


<!--
* Learn more about [environment variables](/docs/tasks/inject-data-application/environment-variable-expose-pod-information/).
* See [EnvVarSource](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#envvarsource-v1-core).
-->
* 进一步了解[环境变量](/zh/docs/tasks/inject-data-application/environment-variable-expose-pod-information/).
* 参阅 [EnvVarSource](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#envvarsource-v1-core).

