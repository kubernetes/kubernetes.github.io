---
title: "示例：使用 Redis 部署 PHP 留言板应用程序"
content_type: tutorial
weight: 20
card:
  name: tutorials
  weight: 30
  title: "无状态应用示例：基于 Redis 的 PHP Guestbook"
min-kubernetes-server-version: v1.14
source: https://cloud.google.com/kubernetes-engine/docs/tutorials/guestbook
---

<!--
title: "Example: Deploying PHP Guestbook application with Redis"
reviewers:
- ahmetb
content_type: tutorial
weight: 20
card:
  name: tutorials
  weight: 30
  title: "Stateless Example: PHP Guestbook with Redis"
min-kubernetes-server-version: v1.14
-->

<!-- overview -->

<!--
This tutorial shows you how to build and deploy a simple _(not production ready)_, multi-tier web application using Kubernetes and [Docker](https://www.docker.com/). This example consists of the following components:
-->
本教程向您展示如何使用 Kubernetes 和 [Docker](https://www.docker.com/) 构建和部署
一个简单的_(非面向生产)的_多层 web 应用程序。本例由以下组件组成：

<!--
* A single-instance [Redis](https://www.redis.com/) to store guestbook entries
* Multiple web frontend instances
-->

* 单实例 [Redis](https://www.redis.com/) 以保存留言板条目
* 多个 web 前端实例

## {{% heading "objectives" %}}

<!--
* Start up a Redis leader.
* Start up two Redis followers.
* Start up the guestbook frontend.
* Expose and view the Frontend Service.
* Clean up.
-->
* 启动 Redis 领导者（Leader）
* 启动两个 Redis 跟随者（Follower）
* 公开并查看前端服务
* 清理

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}}

{{< version-check >}}

<!-- lessoncontent -->

<!--
## Start up the Redis Database
-->
## 启动 Redis 数据库

<!--
The guestbook application uses Redis to store its data.
-->
留言板应用程序使用 Redis 存储数据。

<!--
### Creating the Redis Deployment
-->

### 创建 Redis Deployment

<!--
The manifest file, included below, specifies a Deployment controller that runs a single replica Redis Pod.
-->
下面包含的清单文件指定了一个 Deployment 控制器，该控制器运行一个 Redis Pod 副本。

{{< codenew file="application/guestbook/redis-leader-deployment.yaml" >}}

<!--
1. Launch a terminal window in the directory you downloaded the manifest files.
1. Apply the Redis Deployment from the `redis-leader-deployment.yaml` file:
-->
1. 在下载清单文件的目录中启动终端窗口。
2. 从 `mongo-deployment.yaml` 文件中应用 MongoDB Deployment：

   <!---
   for local testing of the content via relative file path
   kubectl apply -f ./content/en/examples/application/guestbook/redis-leader-deployment.yaml
   -->

   ```shell
   kubectl apply -f https://k8s.io/examples/application/guestbook/redis-leader-deployment.yaml
   ```

<!--
1. Query the list of Pods to verify that the MongoDB Pod is running:
-->
3. 查询 Pod 列表以验证 MongoDB Pod 是否正在运行：

   ```shell
   kubectl get pods
   ```

   <!--
   The response should be similar to this:
   -->
   响应应该与此类似：

   ```shell
   NAME                           READY   STATUS    RESTARTS   AGE
   redis-leader-fb76b4755-xjr2n   1/1     Running   0          13s
   ```

<!--
1. Run the following command to view the logs from the Redis leader Pod:
-->
4. 运行以下命令查看 MongoDB Deployment 中的日志：

   ```shell
   kubectl logs -f deployment/redis-leader
   ```

<!--
### Creating the Redis leader Service
-->
### 创建 Redis 领导者服务

<!--
The guestbook application needs to communicate to the Redis to write its data. You need to apply a [Service](/docs/concepts/services-networking/service/) to proxy the traffic to the Redis Pod. A Service defines a policy to access the Pods.
-->
留言板应用程序需要往 MongoDB 中写数据。因此，需要创建
[Service](/zh/docs/concepts/services-networking/service/) 来转发 Redis Pod
的流量。Service 定义了访问 Pod 的策略。

{{< codenew file="application/guestbook/redis-leader-service.yaml" >}}

<!--
1. Apply the Redis Service from the following `redis-leader-service.yaml` file:
-->
1. 使用下面的 `redis-leader-service.yaml` 文件创建 Redis的服务：

   <!---
   for local testing of the content via relative file path
   kubectl apply -f ./content/en/examples/application/guestbook/redis-leader-service.yaml
   -->
   
   ```shell
   kubectl apply -f https://k8s.io/examples/application/guestbook/redis-leader-service.yaml
   ```

<!--
1. Query the list of Services to verify that the Redis Service is running:
-->
2. 查询服务列表验证 Redis 服务是否正在运行：

   ```shell
   kubectl get service
   ```

   <!--
   The response should be similar to this:
   -->
   响应应该与此类似：

   ```shell
   NAME           TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)    AGE
   kubernetes     ClusterIP   10.0.0.1     <none>        443/TCP    1m
   redis-leader   ClusterIP   10.103.78.24 <none>        6379/TCP   16s
   ```

<!--
This manifest file creates a Service named `redis-leader` with a set of labels that match the labels previously defined, so the Service routes network traffic to the Redis Pod.
-->
{{< note >}}
这个清单文件创建了一个名为 `redis-leader` 的 Service，其中包含一组
与前面定义的标签匹配的标签，因此服务将网络流量路由到 Redis Pod 上。
{{< /note >}}

<!--
### Set up Redis followers

Although the Redis leader is a single Pod, you can make it highly available and meet traffic demands by adding a few Redis followers, or replicas.
-->
### 设置 Redis 跟随者

尽管 Redis 领导者只有一个 Pod，你可以通过添加若干 Redis 跟随者来将其配置为高可用状态，
以满足流量需求。

{{< codenew file="application/guestbook/redis-follower-deployment.yaml" >}}

<!--
1. Apply the Redis Service from the following `redis-follower-deployment.yaml` file:
-->
1. 应用下面的 `redis-follower-deployment.yaml` 文件创建 Redis Deployment：

   <!---
   for local testing of the content via relative file path
   kubectl apply -f ./content/en/examples/application/guestbook/redis-follower-deployment.yaml
   -->

   ```shell
   kubectl apply -f https://k8s.io/examples/application/guestbook/redis-follower-deployment.yaml
   ```

<!--
1. Verify that the two Redis follower replicas are running by querying the list of Pods:
-->
2. 通过查询 Pods 列表，验证两个 Redis 跟随者副本在运行：

   ```shell
   kubectl get pods
   ```

   <!--
   The response should be similar to this:
   -->
   响应应该类似于这样：

   ```
   NAME                             READY   STATUS    RESTARTS   AGE
   redis-follower-dddfbdcc9-82sfr   1/1     Running   0          37s
   redis-follower-dddfbdcc9-qrt5k   1/1     Running   0          38s
   redis-leader-fb76b4755-xjr2n     1/1     Running   0          11m
   ```

<!--
### Creating the Redis follower service

The guestbook application needs to communicate with the Redis followers to read data. To make the Redis followers discoverable, you must set up another [Service](/docs/concepts/services-networking/service/).
-->
### 创建 Redis 跟随者服务

Guestbook 应用需要与 Redis 跟随者通信以读取数据。
为了让 Redis 跟随者可被发现，你必须创建另一个
[Service](/zh/docs/concepts/services-networking/service/)。

{{< codenew file="application/guestbook/redis-follower-service.yaml" >}}

<!--
1. Apply the Redis Service from the following `redis-follower-service.yaml` file:
-->
1. 应用如下所示 `redis-follower-service.yaml` 文件中的 Redis Service：

   <!---
   for local testing of the content via relative file path
   kubectl apply -f ./content/en/examples/application/guestbook/redis-follower-service.yaml
   -->

   ```shell
   kubectl apply -f https://k8s.io/examples/application/guestbook/redis-follower-service.yaml
   ```

<!--
1. Query the list of Services to verify that the Redis Service is running:
-->
2. 查询 Service 列表，验证 Redis 服务在运行：

   ```shell
   kubectl get service
   ```

   <!--
   The response should be similar to this:
   -->
   响应应该类似于这样：

   ```
   NAME             TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
   kubernetes       ClusterIP   10.96.0.1       <none>        443/TCP    3d19h
   redis-follower   ClusterIP   10.110.162.42   <none>        6379/TCP   9s
   redis-leader     ClusterIP   10.103.78.24    <none>        6379/TCP   6m10s
   ```

{{< note >}}
<!--
This manifest file creates a Service named `redis-follower` with a set of labels that match the labels previously defined, so the Service routes network traffic to the Redis Pod.
-->
清单文件创建了一个名为 `redis-follower` 的 Service，该 Service
具有一些与之前所定义的标签相匹配的标签，因此该 Service 能够将网络流量
路由到 Redis Pod 之上。
{{< /note >}}


<!--
## Set up and Expose the Guestbook Frontend
-->
## 设置并公开留言板前端

<!-- 
Now that you have the Redis storage of your guestbook up and running, start the guestbook web servers. Like the Redis followers, the frontend is deployed using a Kubernetes Deployment.

The guestbook app uses a PHP frontend. It is configured to communicate with either the Redis follower or leader Services, depending on whether the request is a read or a write. The frontend exposes a JSON interface, and serves a jQuery-Ajax-based UX.
-->
现在你有了一个为 Guestbook 应用配置的 Redis 存储处于运行状态，
接下来可以启动 Guestbook 的 Web 服务器了。
与 Redis 跟随者类似，前端也是使用 Kubernetes Deployment 来部署的。

Guestbook 应用使用 PHP 前端。该前端被配置成与后端的 Redis 跟随者或者
领导者服务通信，具体选择哪个服务取决于请求是读操作还是写操作。
前端对外暴露一个 JSON 接口，并提供基于 jQuery-Ajax 的用户体验。

<!--
### Creating the Guestbook Frontend Deployment
-->
### 创建 Guestbook 前端 Deployment

{{< codenew file="application/guestbook/frontend-deployment.yaml" >}}

<!--
1. Apply the frontend Deployment from the `frontend-deployment.yaml` file:
-->
1. 应用来自 `frontend-deployment.yaml` 文件的前端 Deployment：

   <!---
   for local testing of the content via relative file path
   kubectl apply -f ./content/en/examples/application/guestbook/frontend-deployment.yaml
   -->
   
   ```shell
   kubectl apply -f https://k8s.io/examples/application/guestbook/frontend-deployment.yaml
      ```

<!--
1. Query the list of Pods to verify that the three frontend replicas are running:
-->
2. 查询 Pod 列表，验证三个前端副本正在运行：

   ```shell
   kubectl get pods -l app=guestbook -l tier=frontend
   ```

   <!--
   The response should be similar to this:
   -->
   响应应该与此类似：

   ```
   NAME                        READY   STATUS    RESTARTS   AGE
   frontend-85595f5bf9-5tqhb   1/1     Running   0          47s
   frontend-85595f5bf9-qbzwm   1/1     Running   0          47s
   frontend-85595f5bf9-zchwc   1/1     Running   0          47s
   ```

<!--
### Creating the Frontend Service
-->
### 创建前端服务

<!--
The `Redis` Services you applied is only accessible within the Kubernetes cluster because the default type for a Service is [ClusterIP](/docs/concepts/services-networking/service/#publishing-services-service-types). `ClusterIP` provides a single IP address for the set of Pods the Service is pointing to. This IP address is accessible only within the cluster.
-->
应用的 `Redis` 服务只能在 Kubernetes 集群中访问，因为服务的默认类型是
[ClusterIP](/zh/docs/concepts/services-networking/service/#publishing-services-service-types)。
`ClusterIP` 为服务指向的 Pod 集提供一个 IP 地址。这个 IP 地址只能在集群中访问。

<!--
If you want guests to be able to access your guestbook, you must configure the frontend Service to be externally visible, so a client can request the Service from outside the Kubernetes cluster. However a Kubernetes user you can use `kubectl port-forward` to access the service even though it uses a `ClusterIP`.
-->
如果你希望访客能够访问你的 Guestbook，你必须将前端服务配置为外部可见的，
以便客户端可以从 Kubernetes 集群之外请求服务。
然而即便使用了 `ClusterIP`，Kubernetes 用户仍可以通过
`kubectl port-forward` 访问服务。

<!--
Some cloud providers, like Google Compute Engine or Google Kubernetes Engine, support external load balancers. If your cloud provider supports load balancers and you want to use it, uncomment `type: LoadBalancer`.
-->
{{< note >}}
一些云提供商，如 Google Compute Engine 或 Google Kubernetes Engine，
支持外部负载均衡器。如果你的云提供商支持负载均衡器，并且你希望使用它，
只需取消注释 `type: LoadBalancer`。
{{< /note >}}

{{< codenew file="application/guestbook/frontend-service.yaml" >}}

<!--
1. Apply the frontend Service from the `frontend-service.yaml` file:
-->
1. 应用来自 `frontend-service.yaml` 文件中的前端服务：

   <!---
   for local testing of the content via relative file path
   kubectl apply -f ./content/en/examples/application/guestbook/frontend-service.yaml
   -->
   
   ```shell
   kubectl apply -f https://k8s.io/examples/application/guestbook/frontend-service.yaml
   ```

<!--
1. Query the list of Services to verify that the frontend Service is running:
-->
2. 查询 Service 列表以验证前端服务正在运行:

   ```shell
   kubectl get services
   ```

   <!--
   The response should be similar to this:
   -->
   响应应该与此类似：

   ```
   NAME             TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
   frontend         ClusterIP   10.97.28.230    <none>        80/TCP     19s
   kubernetes       ClusterIP   10.96.0.1       <none>        443/TCP    3d19h
   redis-follower   ClusterIP   10.110.162.42   <none>        6379/TCP   5m48s
   redis-leader     ClusterIP   10.103.78.24    <none>        6379/TCP   11m
   ```

<!--
### Viewing the Frontend Service via `kubectl port-forward`
-->

### 通过 `kubectl port-forward` 查看前端服务

<!--
1. Run the following command to forward port `8080` on your local machine to port `80` on the service.
-->
1. 运行以下命令将本机的 `8080` 端口转发到服务的 `80` 端口。

   ```shell
   kubectl port-forward svc/frontend 8080:80
   ```

   <!--
   The response should be similar to this:
   -->
   响应应该与此类似：

   ```
   Forwarding from 127.0.0.1:8080 -> 80
   Forwarding from [::1]:8080 -> 80
   ```

<!--
1. load the page [http://localhost:8080](http://localhost:8080) in your browser to view your guestbook.
-->
2. 在浏览器中加载 [http://localhost:8080](http://localhost:8080)
页面以查看 Guestbook。

<!--
### Viewing the Frontend Service via `LoadBalancer`
-->
### 通过 `LoadBalancer` 查看前端服务

<!--
If you deployed the `frontend-service.yaml` manifest with type: `LoadBalancer` you need to find the IP address to view your Guestbook.
-->
如果你部署了 `frontend-service.yaml`，需要找到用来查看 Guestbook 的
IP 地址。

<!--
1. Run the following command to get the IP address for the frontend Service.
-->
1. 运行以下命令以获取前端服务的 IP 地址。

   ```shell
   kubectl get service frontend
   ```

   <!--
   The response should be similar to this:
   -->
   响应应该与此类似：

   ```
   NAME       TYPE           CLUSTER-IP      EXTERNAL-IP        PORT(S)        AGE
   frontend   LoadBalancer   10.51.242.136   109.197.92.229     80:32372/TCP   1m
   ```

<!--
1. Copy the external IP address, and load the page in your browser to view your guestbook.
-->
2. 复制这里的外部 IP 地址，然后在浏览器中加载页面以查看留言板。

{{< note >}}
<!--
Try adding some guestbook entries by typing in a message, and clicking Submit. The message you typed appears in the frontend. This message indicates that data is successfully added to Redis through the Services you created earlier.
-->
尝试通过输入消息并点击 Submit 来添加一些留言板条目。
你所输入的消息会在前端显示。这一消息表明数据被通过你
之前所创建的 Service 添加到 Redis 存储中。
{{< /note >}}

<!--
## Scale the Web Frontend
-->
## 扩展 Web 前端

<!--
You can scale up or down as needed because your servers are defined as a Service that uses a Deployment controller.
-->
你可以根据需要执行伸缩操作，这是因为服务器本身被定义为使用一个
Deployment 控制器的 Service。

<!--
1. Run the following command to scale up the number of frontend Pods:
-->
1. 运行以下命令扩展前端 Pod 的数量：

   ```shell
   kubectl scale deployment frontend --replicas=5
   ```

<!--
1. Query the list of Pods to verify the number of frontend Pods running:
-->
2. 查询 Pod 列表验证正在运行的前端 Pod 的数量：

   ```shell
   kubectl get pods
   ```

   <!--
   The response should look similar to this:
   -->
   响应应该类似于这样：

   ```
   NAME                             READY   STATUS    RESTARTS   AGE
   frontend-85595f5bf9-5df5m        1/1     Running   0          83s
   frontend-85595f5bf9-7zmg5        1/1     Running   0          83s
   frontend-85595f5bf9-cpskg        1/1     Running   0          15m
   frontend-85595f5bf9-l2l54        1/1     Running   0          14m
   frontend-85595f5bf9-l9c8z        1/1     Running   0          14m
   redis-follower-dddfbdcc9-82sfr   1/1     Running   0          97m
   redis-follower-dddfbdcc9-qrt5k   1/1     Running   0          97m
   redis-leader-fb76b4755-xjr2n     1/1     Running   0          108m
   ```

<!--
1. Run the following command to scale down the number of frontend Pods:
-->
3. 运行以下命令缩小前端 Pod 的数量：

   ```shell
   kubectl scale deployment frontend --replicas=2
   ```

<!--
1. Query the list of Pods to verify the number of frontend Pods running:
-->
4. 查询 Pod 列表验证正在运行的前端 Pod 的数量：

   ```shell
   kubectl get pods
   ```

   <!--
   The response should look similar to this:
   -->
   响应应该类似于这样：

   ```
   NAME                             READY   STATUS    RESTARTS   AGE
   frontend-85595f5bf9-cpskg        1/1     Running   0          16m
   frontend-85595f5bf9-l9c8z        1/1     Running   0          15m
   redis-follower-dddfbdcc9-82sfr   1/1     Running   0          98m
   redis-follower-dddfbdcc9-qrt5k   1/1     Running   0          98m
   redis-leader-fb76b4755-xjr2n     1/1     Running   0          109m
   ```

## {{% heading "cleanup" %}}

<!--
Deleting the Deployments and Services also deletes any running Pods. Use labels to delete multiple resources with one command.
-->
删除 Deployments 和服务还会删除正在运行的 Pod。
使用标签用一个命令删除多个资源。

<!--
1. Run the following commands to delete all Pods, Deployments, and Services.
-->
1. 运行以下命令以删除所有 Pod，Deployments 和 Services。

   ```shell
   kubectl delete deployment -l app=redis
   kubectl delete service -l app=redis
   kubectl delete deployment frontend
   kubectl delete service frontend
   ```

   <!--
   The responses should be:
   -->
   响应应该是：

   ```
   deployment.apps "redis-follower" deleted
   deployment.apps "redis-leader" deleted
   deployment.apps "frontend" deleted
   service "frontend" deleted
   ```
<!--
1. Query the list of Pods to verify that no Pods are running:
-->
2. 查询 Pod 列表，确认没有 Pod 在运行：

   ```shell
   kubectl get pods
   ```

   <!--
   The response should be this:
   -->
   响应应该是：

   ```

   No resources found in default namespace.
   ```

## {{% heading "whatsnext" %}}

<!--
* Complete the [Kubernetes Basics](/docs/tutorials/kubernetes-basics/) Interactive Tutorials
* Use Kubernetes to create a blog using [Persistent Volumes for MySQL and Wordpress](/docs/tutorials/stateful-application/mysql-wordpress-persistent-volume/#visit-your-new-wordpress-blog)
* Read more about [connecting applications](/docs/concepts/services-networking/connect-applications-service/)
* Read more about [Managing Resources](/docs/concepts/cluster-administration/manage-deployment/#using-labels-effectively)
-->
* 完成 [Kubernetes 基础](/zh/docs/tutorials/kubernetes-basics/) 交互式教程
* 使用 Kubernetes 创建一个博客，使用
  [MySQL 和 Wordpress 的持久卷](/zh/docs/tutorials/stateful-application/mysql-wordpress-persistent-volume/#visit-your-new-wordpress-blog)
* 进一步阅读[连接应用程序](/zh/docs/concepts/services-networking/connect-applications-service/)
* 进一步阅读[管理资源](/zh/docs/concepts/cluster-administration/manage-deployment/#using-labels-effectively)

