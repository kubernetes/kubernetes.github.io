---
title: 使用 Service 把前端连接到后端
content_type: tutorial
weight: 70
---
<!--
title: Connect a Frontend to a Backend Using Services
content_type: tutorial
weight: 70
-->

<!-- overview -->

<!--
This task shows how to create a _frontend_ and a _backend_ microservice. The backend 
microservice is a hello greeter. The frontend exposes the backend using nginx and a 
Kubernetes {{< glossary_tooltip term_id="service" >}} object.
-->

本任务会描述如何创建前端（Frontend）微服务和后端（Backend）微服务。后端微服务是一个 hello 欢迎程序。
前端通过 nginx 和一个 Kubernetes {{< glossary_tooltip term_id="service" text="服务" >}}
暴露后端所提供的服务。

## {{% heading "objectives" %}}

<!--
* Create and run a sample `hello` backend microservice using a
  {{< glossary_tooltip term_id="deployment" >}} object.
* Use a Service object to send traffic to the backend microservice's multiple replicas.
* Create and run a `nginx` frontend microservice, also using a Deployment object.
* Configure the frontend microservice to send traffic to the backend microservice.
* Use a Service object of `type=LoadBalancer` to expose the frontend microservice
  outside the cluster.
-->
* 使用部署对象（Deployment object）创建并运行一个 `hello` 后端微服务
* 使用一个 Service 对象将请求流量发送到后端微服务的多个副本
* 同样使用一个 Deployment 对象创建并运行一个 `nginx` 前端微服务
* 配置前端微服务将请求流量发送到后端微服务
* 使用 `type=LoadBalancer` 的 Service 对象将全段微服务暴露到集群外部

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}

<!--
This task uses
[Services with external load balancers](/docs/tasks/access-application-cluster/create-external-load-balancer/), which
require a supported environment. If your environment does not support this, you can use a Service of type
[NodePort](/docs/concepts/services-networking/service/#nodeport) instead.
-->
本任务使用[外部负载均衡服务](/zh/docs/tasks/access-application-cluster/create-external-load-balancer/)，
所以需要对应的可支持此功能的环境。如果你的环境不能支持，你可以使用
[NodePort](/zh/docs/concepts/services-networking/service/#nodeport)
类型的服务代替。

<!-- lessoncontent -->

<!--
## Creating the backend using a Deployment

The backend is a simple hello greeter microservice. Here is the configuration
file for the backend Deployment:
-->
### 使用部署对象（Deployment）创建后端

后端是一个简单的 hello 欢迎微服务应用。这是后端应用的 Deployment 配置文件：

{{< codenew file="service/access/backend-deployment.yaml" >}}

<!-- 
Create the backend Deployment:
-->
创建后端 Deployment：

```shell
kubectl apply -f https://k8s.io/examples/service/access/backend-deployment.yaml
```

<!--
View information about the backend Deployment:
-->
查看后端的 Deployment 信息：

```shell
kubectl describe deployment backend
```

<!--
The output is similar to this:
-->
输出类似于：

```
Name:                           backend
Namespace:                      default
CreationTimestamp:              Mon, 24 Oct 2016 14:21:02 -0700
Labels:                         app=hello
                                tier=backend
                                track=stable
Annotations:                    deployment.kubernetes.io/revision=1
Selector:                       app=hello,tier=backend,track=stable
Replicas:                       3 desired | 3 updated | 3 total | 3 available | 0 unavailable
StrategyType:                   RollingUpdate
MinReadySeconds:                0
RollingUpdateStrategy:          1 max unavailable, 1 max surge
Pod Template:
  Labels:       app=hello
                tier=backend
                track=stable
  Containers:
   hello:
    Image:              "gcr.io/google-samples/hello-go-gke:1.0"
    Port:               80/TCP
    Environment:        <none>
    Mounts:             <none>
  Volumes:              <none>
Conditions:
  Type          Status  Reason
  ----          ------  ------
  Available     True    MinimumReplicasAvailable
  Progressing   True    NewReplicaSetAvailable
OldReplicaSets:                 <none>
NewReplicaSet:                  hello-3621623197 (3/3 replicas created)
Events:
...
```

<!--
## Creating the `hello` Service object

The key to sending requests from a frontend to a backend is the backend
Service. A Service creates a persistent IP address and DNS name entry
so that the backend microservice can always be reached. A Service uses
{{< glossary_tooltip text="selectors" term_id="selector" >}} to find
the Pods that it routes traffic to.

First, explore the Service configuration file:
-->
### 创建 `hello` Service 对象

将请求从前端发送到到后端的关键是后端 Service。Service 创建一个固定 IP 和 DNS 解析名入口，
使得后端微服务总是可达。Service 使用
{{< glossary_tooltip text="选择算符" term_id="selector" >}} 
来寻找目标 Pod。

首先，浏览 Service 的配置文件：

{{< codenew file="service/access/backend-service.yaml" >}}

<!--
In the configuration file, you can see that the Service named `hello` routes
traffic to Pods that have the labels `app: hello` and `tier: backend`.
-->
配置文件中，你可以看到名为 `hello` 的 Service 将流量路由到包含 `app: hello`
和 `tier: backend` 标签的 Pod。

<!--
Create the backend Service:
-->
创建后端 Service：

```shell
kubectl apply -f https://k8s.io/examples/service/access/backend-service.yaml
```

<!--
At this point, you have a `backend` Deployment running three replicas of your `hello`
application, and you have a Service that can route traffic to them. However, this
service is neither available nor resolvable outside the cluster.
-->
此时，你已经有了一个运行着 `hello` 应用的三个副本的 `backend` Deployment，你也有了
一个 Service 用于路由网络流量。不过，这个服务在集群外部无法访问也无法解析。

<!--
## Creating the frontend

Now that you have your backend running, you can create a frontend that is accessible 
outside the cluster, and connects to the backend by proxying requests to it.

The frontend sends requests to the backend worker Pods by using the DNS name
given to the backend Service. The DNS name is `hello`, which is the value
of the `name` field in the `examples/service/access/backend-service.yaml` 
configuration file.

The Pods in the frontend Deployment run an nginx image that is configured
to proxy requests to the hello backend Service. Here is the nginx configuration file:
-->
### 创建前端应用

现在你已经有了运行中的后端应用，你可以创建一个可在集群外部访问的前端，并通过代理
前端的请求连接到后端。

前端使用被赋予后端 Service 的 DNS 名称将请求发送到后端工作 Pods。这一 DNS
名称为 `hello`，也就是 `examples/service/access/backend-service.yaml` 配置
文件中 `name` 字段的取值。

前端 Deployment 中的 Pods 运行一个 nginx 镜像，这个已经配置好的镜像会将请求转发
给后端的 hello Service。下面是  nginx 的配置文件：

{{< codenew file="service/access/frontend-nginx.conf" >}}

<!--
Similar to the backend, the frontend has a Deployment and a Service. An important
difference to notice between the backend and frontend services, is that the
configuration for the frontend Service has `type: LoadBalancer`, which means that
the Service uses a load balancer provisioned by your cloud provider and will be
accessible from outside the cluster.
-->
与后端类似，前端用包含一个 Deployment 和一个 Service。后端与前端服务之间的一个
重要区别是前端 Service 的配置文件包含了 `type: LoadBalancer`，也就是说，Service
会使用你的云服务商的默认负载均衡设备，从而实现从集群外访问的目的。

{{< codenew file="service/access/frontend-service.yaml" >}}

{{< codenew file="service/access/frontend-deployment.yaml" >}}


<!--
Create the frontend Deployment and Service:
-->
创建前端 Deployment 和 Service：

```shell
kubectl apply -f https://k8s.io/examples/service/access/frontend-deployment.yaml
kubectl apply -f https://k8s.io/examples/service/access/frontend-service.yaml
```

<!--
The output verifies that both resources were created:
-->
通过输出确认两个资源都已经被创建：

```
deployment.apps/frontend created
service/frontend created
```

<!--
The nginx configuration is baked into the
[container image](/examples/service/access/Dockerfile). A better way to do this would
be to use a
[ConfigMap](/docs/tasks/configure-pod-container/configure-pod-configmap/),
so that you can change the configuration more easily.
-->
{{< note >}}
这个 nginx 配置文件是被打包在
[容器镜像](/examples/service/access/Dockerfile) 里的。
更好的方法是使用
[ConfigMap](/zh/docs/tasks/configure-pod-container/configure-pod-configmap/)，
这样的话你可以更轻易地更改配置。
{{< /note >}}

<!--
## Interact with the frontend Service

Once you've created a Service of type LoadBalancer, you can use this
command to find the external IP:
-->
### 与前端 Service 交互   {#interact-with-the-frontend-service}

一旦你创建了 LoadBalancer 类型的 Service，你可以使用这条命令查看外部 IP：

```shell
kubectl get service frontend
```

<!--
This displays the configuration for the `frontend` Service and watches for
changes. Initially, the external IP is listed as `<pending>`:
-->
外部 IP 字段的生成可能需要一些时间。如果是这种情况，外部 IP 会显示为 `<pending>`。

```
NAME       CLUSTER-IP      EXTERNAL-IP   PORT(S)  AGE
frontend   10.51.252.116   <pending>     80/TCP   10s
```

<!--
As soon as an external IP is provisioned, however, the configuration updates
to include the new IP under the `EXTERNAL-IP` heading:
-->
当外部 IP 地址被分配可用时，配置会更新，在 `EXTERNAL-IP` 头部下显示新的 IP：

```
NAME       CLUSTER-IP      EXTERNAL-IP        PORT(S)  AGE
frontend   10.51.252.116   XXX.XXX.XXX.XXX    80/TCP   1m
```

<!--
That IP can now be used to interact with the `frontend` service from outside the
cluster.
-->
这一新的 IP 地址就可以用来从集群外与 `frontend` 服务交互了。


<!--
## Send traffic through the frontend

The frontend and backend are now connected. You can hit the endpoint
by using the curl command on the external IP of your frontend Service.
-->
### 通过前端发送流量

前端和后端已经完成连接了。你可以使用 curl 命令通过你的前端 Service 的外部
IP 访问服务端点。

```shell
curl http://${EXTERNAL_IP} # 将 EXTERNAL_P 替换为你之前看到的外部 IP
```

<!--
The output shows the message generated by the backend:
-->
输出显示后端生成的消息：

```json
{"message":"Hello"}
```

## {{% heading "cleanup" %}}

<!--
To delete the Services, enter this command:
-->
要删除服务，输入下面的命令：

```shell
kubectl delete services frontend backend
```

<!--
To delete the Deployments, the ReplicaSets and the Pods that are running the backend and frontend applications, enter this command:
-->
要删除在前端和后端应用中运行的 Deployment、ReplicaSet 和 Pod，输入下面的命令：

```shell
kubectl delete deployment frontend backend
```
## {{% heading "whatsnext" %}}

<!--
* Learn more about [Services](/docs/concepts/services-networking/service/)
* Learn more about [ConfigMaps](/docs/tasks/configure-pod-container/configure-pod-configmap/)
* Learn more about [DNS for Service and Pods](/docs/concepts/services-networking/dns-pod-service/)
-->
* 进一步了解 [Service](/zh/docs/concepts/services-networking/service/)
* 进一步了解 [ConfigMap](/zh/docs/tasks/configure-pod-container/configure-pod-configmap/)
* 进一步了解 [Service 和 Pods 的 DNS](/zh/docs/concepts/services-networking/dns-pod-service/)

