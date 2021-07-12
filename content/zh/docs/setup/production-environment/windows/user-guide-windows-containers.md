---
title: Kubernetes 中 Windows 容器的调度指南
content_type: concept
weight: 75
---
<!--
reviewers:
- jayunit100
- jsturtevant
- marosset
- perithompson
title: Guide for scheduling Windows containers in Kubernetes
content_type: concept
weight: 75
-->

<!-- overview -->

<!--
Windows applications constitute a large portion of the services and applications that run in many organizations.
This guide walks you through the steps to configure and deploy a Windows container in Kubernetes.
-->
Windows 应用程序构成了许多组织中运行的服务和应用程序的很大一部分。
本指南将引导您完成在 Kubernetes 中配置和部署 Windows 容器的步骤。

<!-- body -->

<!--
## Objectives

* Configure an example deployment to run Windows containers on the Windows node
* (Optional) Configure an Active Directory Identity for your Pod using Group Managed Service Accounts (GMSA)
-->
## 目标

* 配置一个示例 deployment 以在 Windows 节点上运行 Windows 容器
* （可选）使用组托管服务帐户（GMSA）为您的 Pod 配置 Active Directory 身份

<!--
## Before you begin

* Create a Kubernetes cluster that includes a
[master and a worker node running Windows Server](../user-guide-windows-nodes)
* It is important to note that creating and deploying services and workloads on Kubernetes
behaves in much the same way for Linux and Windows containers.
[Kubectl commands](/docs/reference/kubectl/overview/) to interface with the cluster are identical.
The example in the section below is provided to jumpstart your experience with Windows containers.
-->
## 在你开始之前

* 创建一个 Kubernetes 集群，其中包括一个
  [运行 Windows 服务器的主节点和工作节点](/zh/docs/tasks/administer-cluster/kubeadm/adding-windows-nodes/)
* 重要的是要注意，对于 Linux 和 Windows 容器，在 Kubernetes 
  上创建和部署服务和工作负载的行为几乎相同。
  与集群接口的 [kubectl 命令](/zh/docs/reference/kubectl/overview/)相同。
  提供以下部分中的示例只是为了快速启动  Windows 容器的使用体验。

<!--
## Getting Started: Deploying a Windows container

To deploy a Windows container on Kubernetes, you must first create an example application.
The example YAML file below creates a simple webserver application.
Create a service spec named `win-webserver.yaml` with the contents below:
-->
## 入门：部署 Windows 容器

要在 Kubernetes 上部署 Windows 容器，您必须首先创建一个示例应用程序。
下面的示例 YAML  文件创建了一个简单的 Web 服务器应用程序。
创建一个名为  `win-webserver.yaml`  的服务规约，其内容如下：

```yaml
apiVersion: v1
kind: Service
metadata:
  name: win-webserver
  labels:
    app: win-webserver
spec:
  ports:
    # the port that this service should serve on
    - port: 80
      targetPort: 80
  selector:
    app: win-webserver
  type: NodePort
---
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: win-webserver
  name: win-webserver
spec:
  replicas: 2
  selector:
    matchLabels:
      app: win-webserver
  template:
    metadata:
      labels:
        app: win-webserver
      name: win-webserver
    spec:
     containers:
      - name: windowswebserver
        image: mcr.microsoft.com/windows/servercore:ltsc2019
        command:
        - powershell.exe
        - -command
        - "<#code used from https://gist.github.com/19WAS85/5424431#> ; $$listener = New-Object System.Net.HttpListener ; $$listener.Prefixes.Add('http://*:80/') ; $$listener.Start() ; $$callerCounts = @{} ; Write-Host('Listening at http://*:80/') ; while ($$listener.IsListening) { ;$$context = $$listener.GetContext() ;$$requestUrl = $$context.Request.Url ;$$clientIP = $$context.Request.RemoteEndPoint.Address ;$$response = $$context.Response ;Write-Host '' ;Write-Host('> {0}' -f $$requestUrl) ;  ;$$count = 1 ;$$k=$$callerCounts.Get_Item($$clientIP) ;if ($$k -ne $$null) { $$count += $$k } ;$$callerCounts.Set_Item($$clientIP, $$count) ;$$ip=(Get-NetAdapter | Get-NetIpAddress); $$header='<html><body><H1>Windows Container Web Server</H1>' ;$$callerCountsString='' ;$$callerCounts.Keys | % { $$callerCountsString+='<p>IP {0} callerCount {1} ' -f $$ip[1].IPAddress,$$callerCounts.Item($$_) } ;$$footer='</body></html>' ;$$content='{0}{1}{2}' -f $$header,$$callerCountsString,$$footer ;Write-Output $$content ;$$buffer = [System.Text.Encoding]::UTF8.GetBytes($$content) ;$$response.ContentLength64 = $$buffer.Length ;$$response.OutputStream.Write($$buffer, 0, $$buffer.Length) ;$$response.Close() ;$$responseStatus = $$response.StatusCode ;Write-Host('< {0}' -f $$responseStatus)  } ; "
     nodeSelector:
      kubernetes.io/os: windows
```

<!--
Port mapping is also supported, but for simplicity in this example
the container port 80 is exposed directly to the service.
-->
{{< note >}}
端口映射也是支持的，但为简单起见，在此示例中容器端口 80 直接暴露给服务。
{{< /note >}}

<!--
1. Check that all nodes are healthy:

    ```bash
    kubectl get nodes
    ```

1. Deploy the service and watch for pod updates:

    ```bash
    kubectl apply -f win-webserver.yaml
    kubectl get pods -o wide -w
    ```

    When the service is deployed correctly both Pods are marked as Ready. To exit the watch command, press Ctrl+C.

1. Check that the deployment succeeded. To verify:

    * Two containers per pod on the Windows node, use `docker ps` 
    * Two pods listed from the Linux master, use `kubectl get pods` 
    * Node-to-pod communication across the network, `curl` port 80 of your pod IPs from the Linux master
      to check for a web server response
    * Pod-to-pod communication, ping between pods (and across hosts, if you have more than one Windows node)
      using docker exec or kubectl exec
    * Service-to-pod communication, `curl` the virtual service IP (seen under `kubectl get services`)
      from the Linux master and from individual pods
    * Service discovery, `curl` the service name with the Kubernetes [default DNS suffix](/docs/concepts/services-networking/dns-pod-service/#services)
    * Inbound connectivity, `curl` the NodePort from the Linux master or machines outside of the cluster
    * Outbound connectivity, `curl` external IPs from inside the pod using kubectl exec
-->
1. 检查所有节点是否健康：

   ```bash
   kubectl get nodes
   ```

1. 部署服务并观察 pod 更新：

   ```bash
   kubectl apply -f win-webserver.yaml
   kubectl get pods -o wide -w
   ```

   正确部署服务后，两个 Pod 都标记为“Ready”。要退出 watch 命令，请按 Ctrl + C。

1. 检查部署是否成功。验证：

   * Windows 节点上每个 Pod 有两个容器，使用  `docker ps` 
   * Linux 主机列出两个 Pod，使用  `kubectl get pods` 
   * 跨网络的节点到 Pod 通信，从 Linux 主服务器 `curl` 您的 pod IPs 的端口80，以检查 Web 服务器响应
   * Pod 到 Pod 的通信，使用 docker exec 或 kubectl exec 在 Pod 之间
     （以及跨主机，如果你有多个 Windows 节点）进行 ping 操作
   * 服务到 Pod 的通信，从 Linux 主服务器和各个 Pod 中 `curl` 虚拟服务 IP
     （在 `kubectl get services` 下可见）
   * 服务发现，使用 Kubernetes `curl` 服务名称
     [默认 DNS 后缀](/zh/docs/concepts/services-networking/dns-pod-service/#services)
   * 入站连接，从 Linux 主服务器或集群外部的计算机 `curl` NodePort
   * 出站连接，使用 kubectl exec 从 Pod 内部 curl 外部 IP

<!--
Windows container hosts are not able to access the IP of services scheduled on them due to current platform limitations of the Windows networking stack.
Only Windows pods are able to access service IPs.
-->
{{< note >}}
由于当前平台对 Windows 网络堆栈的限制，Windows 容器主机无法访问在其上调度的服务的 IP。只有 Windows pods 才能访问服务 IP。
{{< /note >}}

<!--
## Observability

### Capturing logs from workloads
-->
## 可观测性  {#observability}

### 抓取来自工作负载的日志

<!--
Logs are an important element of observability; they enable users to gain insights
into the operational aspect of workloads and are a key ingredient to troubleshooting issues.
Because Windows containers and workloads inside Windows containers behave differently from Linux containers,
users had a hard time collecting logs, limiting operational visibility.
Windows workloads for example are usually configured to log to ETW (Event Tracing for Windows)
or push entries to the application event log.
[LogMonitor](https://github.com/microsoft/windows-container-tools/tree/master/LogMonitor), an open source tool by Microsoft,
is the recommended way to monitor configured log sources inside a Windows container.
LogMonitor supports monitoring event logs, ETW providers, and custom application logs,
piping them to STDOUT for consumption by `kubectl logs <pod>`.
-->
日志是可观测性的重要一环；使用日志用户可以获得对负载运行状况的洞察，
因而日志是故障排查的一个重要手法。
因为 Windows 容器中的 Windows 容器和负载与 Linux 容器的行为不同，
用户很难收集日志，因此运行状态的可见性很受限。
例如，Windows 工作负载通常被配置为将日志输出到 Windows 事件跟踪
（Event Tracing for Windows，ETW），或者将日志条目推送到应用的事件日志中。
[LogMonitor](https://github.com/microsoft/windows-container-tools/tree/master/LogMonitor)
是 Microsoft 提供的一个开源工具，是监视 Windows 容器中所配置的日志源
的推荐方式。
LogMonitor 支持监视时间日志、ETW 提供者模块以及自定义的应用日志，
并使用管道的方式将其输出到标准输出（stdout），以便 `kubectl logs <pod>`
这类命令能够读取这些数据。

<!--
Follow the instructions in the LogMonitor GitHub page to copy its binaries and configuration files
to all your containers and add the necessary entrypoints for LogMonitor to push your logs to STDOUT.
-->
请遵照 LogMonitor GitHub 页面上的指令，将其可执行文件和配置文件复制到
你的所有容器中，并为其添加必要的入口点（Entrypoint），以便 LogMonitor
能够将你的日志输出推送到标准输出（stdout）。


<!--
## Using configurable Container usernames

Starting with Kubernetes v1.16, Windows containers can be configured to run their entrypoints and processes
with different usernames than the image defaults.
The way this is achieved is a bit different from the way it is done for Linux containers.
Learn more about it [here](/docs/tasks/configure-pod-container/configure-runasusername/).
-->
## 使用可配置的容器用户名

从 Kubernetes v1.16 开始，可以为 Windows  容器配置与其镜像默认值不同的用户名
来运行其入口点和进程。
此能力的实现方式和 Linux 容器有些不同。
在[此处](/zh/docs/tasks/configure-pod-container/configure-runasusername/)
可了解更多信息。

<!--
## Managing Workload Identity with Group Managed Service Accounts

Starting with Kubernetes v1.14, Windows container workloads can be configured to use Group Managed Service Accounts (GMSA).
Group Managed Service Accounts are a specific type of Active Directory account that provides automatic password management,
simplified service principal name (SPN) management, and the ability to delegate the management to other administrators across multiple servers.
Containers configured with a GMSA can access external Active Directory Domain resources while carrying the identity configured with the GMSA.
Learn more about configuring and using GMSA for Windows containers [here](/docs/tasks/configure-pod-container/configure-gmsa/).
-->
## 使用组托管服务帐户管理工作负载身份

从 Kubernetes v1.14 开始，可以将 Windows 容器工作负载配置为使用组托管服务帐户（GMSA）。
组托管服务帐户是 Active Directory 帐户的一种特定类型，它提供自动密码管理，
简化的服务主体名称（SPN）管理以及将管理委派给跨多台服务器的其他管理员的功能。
配置了 GMSA 的容器可以访问外部 Active Directory 域资源，同时携带通过 GMSA 配置的身份。
在[此处](/zh/docs/tasks/configure-pod-container/configure-gmsa/)了解有关为
Windows 容器配置和使用 GMSA 的更多信息。

<!--
## Taints and Tolerations
-->
## 污点和容忍度

<!--
Users today need to use some combination of taints and node selectors in order to
keep Linux and Windows workloads on their respective OS-specific nodes.
This likely imposes a burden only on Windows users. The recommended approach is outlined below,
with one of its main goals being that this approach should not break compatibility for existing Linux workloads.
-->
目前，用户需要将 Linux 和 Windows 工作负载运行在各自特定的操作系统的节点上，
因而需要结合使用污点和节点选择算符。 这可能仅给 Windows 用户造成不便。
推荐的方法概述如下，其主要目标之一是该方法不应破坏与现有 Linux 工作负载的兼容性。

<!--
### Ensuring OS-specific workloads land on the appropriate container host
-->
### 确保特定操作系统的工作负载落在适当的容器主机上

<!--
Users can ensure Windows containers can be scheduled on the appropriate host using Taints and Tolerations.
All Kubernetes nodes today have the following default labels:
-->
用户可以使用污点和容忍度确保 Windows 容器可以调度在适当的主机上。目前所有 Kubernetes 节点都具有以下默认标签：

* kubernetes.io/os = [windows|linux]
* kubernetes.io/arch = [amd64|arm64|...]

<!--
If a Pod specification does not specify a nodeSelector like `"kubernetes.io/os": windows`,
it is possible the Pod can be scheduled on any host, Windows or Linux.
This can be problematic since a Windows container can only run on Windows and a Linux container can only run on Linux.
The best practice is to use a nodeSelector.
-->
如果 Pod 规范未指定诸如 `"kubernetes.io/os": windows` 之类的 nodeSelector，则该 Pod 
可能会被调度到任何主机（Windows 或 Linux）上。
这是有问题的，因为 Windows 容器只能在 Windows 上运行，而 Linux 容器只能在 Linux 上运行。
最佳实践是使用 nodeSelector。

<!--
However, we understand that in many cases users have a pre-existing large number of deployments for Linux containers,
as well as an ecosystem of off-the-shelf configurations, such as community Helm charts, and programmatic Pod generation cases, such as with Operators.
In those situations, you may be hesitant to make the configuration change to add nodeSelectors.
The alternative is to use Taints. Because the kubelet can set Taints during registration,
it could easily be modified to automatically add a taint when running on Windows only.
-->
但是，我们了解到，在许多情况下，用户都有既存的大量的 Linux 容器部署，以及一个现成的配置生态系统，
例如社区 Helm charts，以及程序化 Pod 生成案例，例如 Operators。
在这些情况下，您可能会不愿意更改配置添加 nodeSelector。替代方法是使用污点。
由于 kubelet 可以在注册期间设置污点，因此可以轻松修改它，使其仅在 Windows 上运行时自动添加污点。

<!--
For example:  `--register-with-taints='os=windows:NoSchedule'`
-->
例如：`--register-with-taints='os=windows:NoSchedule'`

<!--
By adding a taint to all Windows nodes, nothing will be scheduled on them (that includes existing Linux Pods).
In order for a Windows Pod to be scheduled on a Windows node,
it would need both the nodeSelector to choose Windows, and the appropriate matching toleration.
-->
向所有 Windows 节点添加污点后，Kubernetes 将不会在它们上调度任何负载（包括现有的 Linux Pod）。
为了使某 Windows Pod 调度到 Windows 节点上，该 Pod 既需要 nodeSelector 选择 Windows，
也需要合适的匹配的容忍度设置。

```yaml
nodeSelector:
  kubernetes.io/os: windows
  node.kubernetes.io/windows-build: '10.0.17763'
tolerations:
  - key: "os"
    operator: "Equal"
    value: "windows"
    effect: "NoSchedule"
```

<!--
### Handling multiple Windows versions in the same cluster
-->
### 处理同一集群中的多个 Windows 版本

<!--
The Windows Server version used by each pod must match that of the node. If you want to use multiple Windows
Server versions in the same cluster, then you should set additional node labels and nodeSelectors.
-->
每个 Pod 使用的 Windows Server 版本必须与该节点的 Windows Server 版本相匹配。
如果要在同一集群中使用多个 Windows Server 版本，则应该设置其他节点标签和
nodeSelector。

<!--
Kubernetes 1.17 automatically adds a new label `node.kubernetes.io/windows-build` to simplify this.
If you're running an older version, then it's recommended to add this label manually to Windows nodes.
-->
Kubernetes 1.17 自动添加了一个新标签 `node.kubernetes.io/windows-build` 来简化此操作。 
如果您运行的是旧版本，则建议手动将此标签添加到 Windows 节点。

<!--
This label reflects the Windows major, minor, and build number that need to match for compatibility.
Here are values used today for each Windows Server version.
-->
此标签反映了需要兼容的 Windows 主要、次要和内部版本号。以下是当前每个
Windows Server 版本使用的值。

| 产品名称                             |   内部编号             |
|--------------------------------------|------------------------|
| Windows Server 2019                  | 10.0.17763             |
| Windows Server version 1809          | 10.0.17763             |
| Windows Server version 1903          | 10.0.18362             |


<!--
### Simplifying with RuntimeClass
-->
### 使用 RuntimeClass 简化

<!--
[RuntimeClass] can be used to simplify the process of using taints and tolerations.
A cluster administrator can create a `RuntimeClass` object which is used to encapsulate these taints and tolerations.
-->
[RuntimeClass](/zh/docs/concepts/containers/runtime-class/) 可用于
简化使用污点和容忍度的过程。
集群管理员可以创建 `RuntimeClass` 对象，用于封装这些污点和容忍度。

<!--
1. Save this file to `runtimeClasses.yml`. It includes the appropriate `nodeSelector`
   for the Windows OS, architecture, and version.
-->
1. 将此文件保存到 `runtimeClasses.yml` 文件。
   它包括适用于 Windows 操作系统、体系结构和版本的 `nodeSelector`。

   ```yaml
   apiVersion: node.k8s.io/v1
   kind: RuntimeClass
   metadata:
     name: windows-2019
   handler: 'docker'
   scheduling:
     nodeSelector:
       kubernetes.io/os: 'windows'
       kubernetes.io/arch: 'amd64'
       node.kubernetes.io/windows-build: '10.0.17763'
     tolerations:
     - effect: NoSchedule
       key: os
       operator: Equal
       value: "windows"
   ```

<!--
1. Run `kubectl create -f runtimeClasses.yml` using as a cluster administrator
1. Add `runtimeClassName: windows-2019` as appropriate to Pod specs
-->
2. 集群管理员执行 `kubectl create -f runtimeClasses.yml` 操作
3. 根据需要向 Pod 规约中添加 `runtimeClassName: windows-2019`

<!--
For example:
-->
例如：

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: iis-2019
  labels:
    app: iis-2019
spec:
  replicas: 1
  template:
    metadata:
      name: iis-2019
      labels:
        app: iis-2019
    spec:
      runtimeClassName: windows-2019
      containers:
      - name: iis
        image: mcr.microsoft.com/windows/servercore/iis:windowsservercore-ltsc2019
        resources:
          limits:
            cpu: 1
            memory: 800Mi
          requests:
            cpu: .1
            memory: 300Mi
        ports:
          - containerPort: 80
 selector:
    matchLabels:
      app: iis-2019
---
apiVersion: v1
kind: Service
metadata:
  name: iis
spec:
  type: LoadBalancer
  ports:
  - protocol: TCP
    port: 80
  selector:
    app: iis-2019
```
