---
title: Kubernetes 对 Windows 的支持
content_type: concept
weight: 65
---
<!--
reviewers:
- jayunit100
- jsturtevant
- marosset
- perithompson
title: Intro to Windows support in Kubernetes
content_type: concept
weight: 65
-->

<!-- overview -->

<!--
Windows applications constitute a large portion of the services and
applications that run in many organizations.
[Windows containers](https://aka.ms/windowscontainers) provide a modern way to
encapsulate processes and package dependencies, making it easier to use DevOps
practices and follow cloud native patterns for Windows applications.
Kubernetes has become the defacto standard container orchestrator, and the
release of Kubernetes 1.14 includes production support for scheduling Windows
containers on Windows nodes in a Kubernetes cluster, enabling a vast ecosystem
of Windows applications to leverage the power of Kubernetes. Organizations
with investments in Windows-based applications and Linux-based applications
don't have to look for separate orchestrators to manage their workloads,
leading to increased operational efficiencies across their deployments,
regardless of operating system.
-->
在很多组织中，其服务和应用的很大比例是 Windows 应用。
[Windows 容器](https://aka.ms/windowscontainers)提供了一种对进程和包依赖关系
进行封装的现代方式，这使得用户更容易采用 DevOps 实践，令 Windows 应用同样遵从
云原生模式。
Kubernetes 已经成为事实上的标准容器编排器，Kubernetes 1.14 发行版本中包含了将
Windows 容器调度到 Kubernetes 集群中 Windows 节点上的生产级支持，从而使得巨大
的 Windows 应用生态圈能够充分利用 Kubernetes 的能力。
对于同时投入基于 Windows 应用和 Linux 应用的组织而言，他们不必寻找不同的编排系统
来管理其工作负载，其跨部署的运维效率得以大幅提升，而不必关心所用操作系统。 

<!-- body -->

<!--
## Windows containers in Kubernetes

To enable the orchestration of Windows containers in Kubernetes, include
Windows nodes in your existing Linux cluster. Scheduling Windows containers in
{{< glossary_tooltip text="Pods" term_id="pod" >}} on Kubernetes is similar to
scheduling Linux-based containers.
-->
## kubernetes 中的 Windows 容器  {#windows-containers-in-kubernetes}

若要在 Kubernetes 中启用对 Windows 容器的编排，可以在现有的 Linux 集群中
包含 Windows 节点。在 Kubernetes 上调度 {{< glossary_tooltip text="Pods" term_id="pod" >}}
中的 Windows 容器与调用基于 Linux 的容器类似。

<!--
In order to run Windows containers, your Kubernetes cluster must include
multiple operating systems, with control plane nodes running Linux and workers
running either Windows or Linux depending on your workload needs. Windows
Server 2019 is the only Windows operating system supported, enabling
[Kubernetes Node](https://github.com/kubernetes/community/blob/master/contributors/design-proposals/architecture/architecture.md#the-kubernetes-node)
on Windows (including kubelet,
[container runtime](https://docs.microsoft.com/en-us/virtualization/windowscontainers/deploy-containers/containerd),
and kube-proxy). For a detailed explanation of Windows distribution channels
see the [Microsoft documentation](https://docs.microsoft.com/en-us/windows-server/get-started-19/servicing-channels-19).
-->
为了运行 Windows 容器，你的 Kubernetes 集群必须包含多个操作系统，控制面
节点运行 Linux，工作节点则可以根据负载需要运行 Windows 或 Linux。
Windows Server 2019 是唯一被支持的 Windows 操作系统，在 Windows 上启用
[Kubernetes 节点](https://github.com/kubernetes/community/blob/master/contributors/design-proposals/architecture/architecture.md#the-kubernetes-node)
支持（包括 kubelet, [容器运行时](https://docs.microsoft.com/en-us/virtualization/windowscontainers/deploy-containers/containerd)、
以及 kube-proxy）。关于 Windows 发行版渠道的详细讨论，可参见
[Microsoft 文档](https://docs.microsoft.com/en-us/windows-server/get-started-19/servicing-channels-19)。

<!--
The Kubernetes control plane, including the
[master components](/docs/concepts/overview/components/),
continues to run on Linux. 
There are no plans to have a Windows-only Kubernetes cluster.
-->
{{< note >}}
Kubernetes 控制面，包括[主控组件](/zh/docs/concepts/overview/components/)，
继续在 Linux 上运行。
目前没有支持完全是 Windows 节点的 Kubernetes 集群的计划。
{{< /note >}}

<!--
In this document, when we talk about Windows containers we mean Windows
containers with process isolation. Windows containers with
[Hyper-V isolation](https://docs.microsoft.com/en-us/virtualization/windowscontainers/manage-containers/hyperv-container)
is planned for a future release.
-->
{{< note >}}
在本文中，当我们讨论 Windows 容器时，我们所指的是具有进程隔离能力的 Windows
容器。具有 [Hyper-V 隔离能力](https://docs.microsoft.com/en-us/virtualization/windowscontainers/manage-containers/hyperv-container)
的 Windows 容器计划在将来发行版本中推出。
{{< /note >}}

<!--
## Supported Functionality and Limitations

### Supported Functionality

#### Windows OS Version Support

Refer to the following table for Windows operating system support in
Kubernetes. A single heterogeneous Kubernetes cluster can have both Windows
and Linux worker nodes. Windows containers have to be scheduled on Windows
nodes and Linux containers on Linux nodes.
-->
## 支持的功能与局限性  {#supported-functionality-and-limitations}

### 支持的功能    {#supported-functionality}

#### Windows 操作系统版本支持    {#windows-os-version-support}

参考下面的表格，了解 Kubernetes 中支持的 Windows 操作系统。
同一个异构的 Kubernetes 集群中可以同时包含 Windows 和 Linux 工作节点。
Windows 容器仅能调度到 Windows 节点，Linux 容器则只能调度到 Linux 节点。

| Kubernetes 版本 | Windows Server LTSC 版本 | Windows Server SAC 版本 |
| --- | --- | --- | --- |
| *Kubernetes v1.19* | Windows Server 2019 | Windows Server ver 1909, Windows Server ver 2004 |
| *Kubernetes v1.20* | Windows Server 2019 | Windows Server ver 1909, Windows Server ver 2004 |
| *Kubernetes v1.21* | Windows Server 2019 | Windows Server ver 2004, Windows Server ver 20H2 |

<!--
Information on the different Windows Server servicing channels including their
support models can be found at
[Windows Server servicing channels](https://docs.microsoft.com/en-us/windows-server/get-started-19/servicing-channels-19).
-->
关于不同的 Windows Server 版本的服务渠道，包括其支持模式等相关信息可以在
[Windows Server servicing channels](https://docs.microsoft.com/en-us/windows-server/get-started-19/servicing-channels-19)
找到。

<!--
We don't expect all Windows customers to update the operating system for their
apps frequently. Upgrading your applications is what dictates and necessitates
upgrading or introducing new nodes to the cluster. For the customers that
chose to upgrade their operating system for containers running on Kubernetes,
we will offer guidance and step-by-step instructions when we add support for a
new operating system version. This guidance will include recommended upgrade
procedures for upgrading user applications together with cluster nodes.
Windows nodes adhere to Kubernetes
[version-skew policy](/docs/setup/release/version-skew-policy/) (node to control plane
versioning) the same way as Linux nodes do today.
-->
我们并不指望所有 Windows 客户都为其应用频繁地更新操作系统。
对应用的更新是向集群中引入新代码的根本原因。
对于想要更新运行于 Kubernetes 之上的容器中操作系统的客户，我们会在添加对新
操作系统版本的支持时提供指南和分步的操作指令。
该指南会包含与集群节点一起来升级用户应用的建议升级步骤。
Windows 节点遵从 Kubernetes
[版本偏差策略](/zh/docs/setup/release/version-skew-policy/)（节点到控制面的
版本控制），与 Linux 节点的现行策略相同。

<!--
The Windows Server Host Operating System is subject to the
[Windows Server ](https://www.microsoft.com/en-us/cloud-platform/windows-server-pricing)
licensing. The Windows Container images are subject to the
[Supplemental License Terms for Windows containers](https://docs.microsoft.com/en-us/virtualization/windowscontainers/images-eula).
-->
Windows Server 主机操作系统会受
[Windows Server](https://www.microsoft.com/en-us/cloud-platform/windows-server-pricing)
授权策略控制。Windows 容器镜像则遵从
[Windows 容器的补充授权条款](https://docs.microsoft.com/en-us/virtualization/windowscontainers/images-eula)
约定。

<!--
Windows containers with process isolation have strict compatibility rules,
[where the host OS version must match the container base image OS version](https://docs.microsoft.com/en-us/virtualization/windowscontainers/deploy-containers/version-compatibility).
Once we support Windows containers with Hyper-V isolation in Kubernetes, the
limitation and compatibility rules will change.
-->
带进程隔离的 Windows 容器受一些严格的兼容性规则约束，
[其中宿主 OS 版本必须与容器基准镜像的 OS 版本相同](https://docs.microsoft.com/en-us/virtualization/windowscontainers/deploy-containers/version-compatibility)。
一旦我们在 Kubernetes 中支持带 Hyper-V 隔离的 Windows 容器，
这一约束和兼容性规则也会发生改变。

<!--
#### Pause Image

Microsoft maintains a Windows pause infrastructure container at
`mcr.microsoft.com/oss/kubernetes/pause:3.4.1`.
-->
#### Pause 镜像   {#pause-image}

Microsoft 在 `mcr.microsoft.com/oss/kubernetes/pause:3.4.1` 处维护
一个 pause 基础设施容器镜像。

<!--
#### Compute

From an API and kubectl perspective, Windows containers behave in much the
same way as Linux-based containers. However, there are some notable
differences in key functionality which are outlined in the
[limitation section](#limitations).
-->
#### 计算    {#compute}

从 API 和 kubectl 的角度，Windows 容器的表现在很大程度上与基于 Linux 的容器
是相同的。不过也有一些与关键功能相关的差别值得注意，这些差别列举于
[局限性](#limitations)小节中。

<!--
Key Kubernetes elements work the same way in Windows as they do in Linux. In
this section, we talk about some of the key workload enablers and how they map
to Windows.
-->
关键性的 Kubernetes 元素在 Windows 下与其在 Linux 下工作方式相同。我们在本节中
讨论一些关键性的负载支撑组件及其在 Windows 中的映射。

* [Pods](/zh/docs/concepts/workloads/pods/)

  <!--
  A Pod is the basic building block of Kubernetes–the smallest and simplest
  unit in the Kubernetes object model that you create or deploy. You may not
  deploy Windows and Linux containers in the same Pod. All containers in a Pod
  are scheduled onto a single Node where each Node represents a specific
  platform and architecture. The following Pod capabilities, properties and
  events are supported with Windows containers:
  -->
  Pod 是 Kubernetes 中最基本的构造模块，是 Kubernetes 对象模型中你可以创建或部署的
  最小、最简单元。你不可以在同一 Pod 中部署 Windows 和 Linux 容器。
  Pod 中的所有容器都会被调度到同一节点（Node），而每个节点代表的是一种特定的平台
  和体系结构。Windows 容器支持 Pod 的以下能力、属性和事件：

  <!--
  * Single or multiple containers per Pod with process isolation and volume sharing
  * Pod status fields
  * Readiness and Liveness probes
  * postStart & preStop container lifecycle events
  * ConfigMap, Secrets: as environment variables or volumes
  * EmptyDir
  * Named pipe host mounts
  * Resource limits
  -->
  * 在带进程隔离和卷共享支持的 Pod 中运行一个或多个容器
  * Pod 状态字段
  * 就绪态（Readiness）和活跃性（Liveness）探针
  * postStart 和 preStop 容器生命周期事件
  * ConfigMap、Secrets：用作环境变量或卷
  * emptyDir 卷
  * 从宿主系统挂载命名管道
  * 资源限制

* [控制器（Controllers）](/zh/docs/concepts/workloads/controllers/)

  <!--
  Kubernetes controllers handle the desired state of Pods. The following
  workload controllers are supported with Windows containers:
  -->
  Kubernetes 控制器处理 Pod 的期望状态。Windows 容器支持以下负载控制器：

  * ReplicaSet
  * ReplicationController
  * Deployment
  * StatefulSet
  * DaemonSet
  * Job
  * CronJob

* [服务（Services）](/zh/docs/concepts/services-networking/service/)

  <!--
  A Kubernetes Service is an abstraction which defines a logical set of Pods
  and a policy by which to access them - sometimes called a micro-service. You
  can use services for cross-operating system connectivity. In Windows, services
  can utilize the following types, properties and capabilities:
  -->
  Kubernetes Service 是一种抽象对象，用来定义 Pod 的一个逻辑集合及用来访问这些
  Pod 的策略。Service 有时也称作微服务（Micro-service）。你可以使用服务来实现
  跨操作系统的连接。在 Windows 系统中，服务可以使用下面的类型、属性和能力：

  * Service 环境变量
  * NodePort
  * ClusterIP
  * LoadBalancer
  * ExternalName
  * 无头（Headless）服务

<!--
Pods, Controllers and Services are critical elements to managing Windows
workloads on Kubernetes. However, on their own they are not enough to enable
the proper lifecycle management of Windows workloads in a dynamic cloud native
environment. We added support for the following features:

* Pod and container metrics
* Horizontal Pod Autoscaler support
* kubectl Exec
* Resource Quotas
* Scheduler preemption
-->
Pods、控制器和服务是在 Kubernetes 上管理 Windows 负载的关键元素。
不过，在一个动态的云原生环境中，这些元素本身还不足以用来正确管理
Windows 负载的生命周期。我们为此添加了如下功能特性：

* Pod 和容器的度量（Metrics）
* 对水平 Pod 自动扩展的支持
* 对 kubectl exec 命令的支持
* 资源配额
* 调度器抢占

<!--
#### Container Runtime

##### Docker EE
-->
#### 容器运行时    {#container-runtime}

##### Docker EE

{{< feature-state for_k8s_version="v1.14" state="stable" >}}

<!--
Docker EE-basic 19.03+ is the recommended container runtime for all Windows
Server versions. This works with the dockershim code included in the kubelet.
-->
Docker EE-basic 19.03+ 是建议所有 Windows Server 版本采用的容器运行时。
该容器运行时能够与 kubelet 中的 dockershim 代码协同工作。

##### CRI-ContainerD

{{< feature-state for_k8s_version="v1.20" state="stable" >}}

<!--
{{< glossary_tooltip term_id="containerd" text="ContainerD" >}} 1.4.0+ can
also be used as the container runtime for Windows Kubernetes nodes.
-->
{{< glossary_tooltip term_id="containerd" text="ContainerD" >}} 1.4.0+
也可作为 Windows Kubernetes 节点上的容器运行时。

<!--
#### Persistent Storage

Kubernetes [volumes](/docs/concepts/storage/volumes/) enable complex
applications, with data persistence and Pod volume sharing requirements, to be
deployed on Kubernetes. Management of persistent volumes associated with a
specific storage back-end or protocol includes actions such as:
provisioning/de-provisioning/resizing of volumes, attaching/detaching a volume
to/from a Kubernetes node and mounting/dismounting a volume to/from individual
containers in a pod that needs to persist data. The code implementing these
volume management actions for a specific storage back-end or protocol is
shipped in the form of a Kubernetes volume
[plugin](/docs/concepts/storage/volumes/#types-of-volumes). The following
broad classes of Kubernetes volume plugins are supported on Windows:
-->
#### 持久性存储   {#persistent-storage}

使用 Kubernetes [卷](/zh/docs/concepts/storage/volumes/)，对数据持久性和 Pod 卷
共享有需求的复杂应用也可以部署到 Kubernetes 上。
管理与特定存储后端或协议相关的持久卷时，相关的操作包括：对卷的配备（Provisioning）、
去配（De-provisioning）和调整大小，将卷挂接到 Kubernetes 节点或从节点上解除挂接，
将卷挂载到需要持久数据的 Pod 中的某容器或从容器上卸载。
负责实现为特定存储后端或协议实现卷管理动作的代码以 Kubernetes 卷
[插件](/zh/docs/concepts/storage/volumes/#types-of-volumes)的形式发布。
Windows 支持以下大类的 Kubernetes 卷插件：

<!--
##### In-Tree Volume Plugins

Code associated with in-tree volume plugins ship as part of the core
Kubernetes code base. Deployment of in-tree volume plugins do not require
installation of additional scripts or deployment of separate containerized
plugin components. These plugins can handle: provisioning/de-provisioning and
resizing of volumes in the storage backend, attaching/detaching of volumes
to/from a Kubernetes node and mounting/dismounting a volume to/from individual
containers in a pod. The following in-tree plugins support Windows nodes:
-->
##### 树内卷插件   {#in-tree-volume-plugins}

与树内卷插件（In-Tree Volume Plugin）相关的代码都作为核心 Kubernetes 代码基
的一部分发布。树内卷插件的部署不需要安装额外的脚本，也不需要额外部署独立的
容器化插件组件。这些插件可以处理：对应存储后端上存储卷的配备、去配和尺寸更改，
将卷挂接到 Kubernetes 或从其上解挂，以及将卷挂载到 Pod 中各个容器上或从其上
卸载。以下树内插件支持 Windows 节点：

* [awsElasticBlockStore](/zh/docs/concepts/storage/volumes/#awselasticblockstore)
* [azureDisk](/zh/docs/concepts/storage/volumes/#azuredisk)
* [azureFile](/zh/docs/concepts/storage/volumes/#azurefile)
* [gcePersistentDisk](/zh/docs/concepts/storage/volumes/#gcepersistentdisk)
* [vsphereVolume](/zh/docs/concepts/storage/volumes/#vspherevolume)

<!--
##### FlexVolume Plugins

Code associated with [FlexVolume](/docs/concepts/storage/volumes/#flexVolume)
plugins ship as out-of-tree scripts or binaries that need to be deployed
directly on the host. FlexVolume plugins handle attaching/detaching of volumes
to/from a Kubernetes node and mounting/dismounting a volume to/from individual
containers in a pod. Provisioning/De-provisioning of persistent volumes
associated with FlexVolume plugins may be handled through an external
provisioner that is typically separate from the FlexVolume plugins. The
following FlexVolume
[plugins](https://github.com/Microsoft/K8s-Storage-Plugins/tree/master/flexvolume/windows),
deployed as powershell scripts on the host, support Windows nodes:
-->
##### FlexVolume 插件   {#flexvolume-plugins}

与 [FlexVolume](/zh/docs/concepts/storage/volumes/#flexVolume) 插件相关的代码是作为
树外（Out-of-tree）脚本或可执行文件来发布的，因此需要在宿主系统上直接部署。
FlexVolume 插件处理将卷挂接到 Kubernetes 节点或从其上解挂、将卷挂载到 Pod 中
各个容器上或从其上卸载等操作。对于与 FlexVolume 插件相关联的持久卷的配备和
去配操作，可以通过外部的配置程序来处理。这类配置程序通常与 FlexVolume 插件
相分离。下面的 FlexVolume
[插件](https://github.com/Microsoft/K8s-Storage-Plugins/tree/master/flexvolume/windows)
可以以 PowerShell 脚本的形式部署到宿主系统上，支持 Windows 节点：

* [SMB](https://github.com/microsoft/K8s-Storage-Plugins/tree/master/flexvolume/windows/plugins/microsoft.com~smb.cmd)
* [iSCSI](https://github.com/microsoft/K8s-Storage-Plugins/tree/master/flexvolume/windows/plugins/microsoft.com~iscsi.cmd)

<!--
##### CSI Plugins
-->
##### CSI 插件   {#csi-plugins}

{{< feature-state for_k8s_version="v1.19" state="beta" >}}

<!--
Code associated with {{< glossary_tooltip text="CSI" term_id="csi" >}} plugins
ship as out-of-tree scripts and binaries that are typically distributed as
container images and deployed using standard Kubernetes constructs like
DaemonSets and StatefulSets. CSI plugins handle a wide range of volume
management actions in Kubernetes: provisioning/de-provisioning/resizing of
volumes, attaching/detaching of volumes to/from a Kubernetes node and
mounting/dismounting a volume to/from individual containers in a pod,
backup/restore of persistent data using snapshots and cloning. CSI plugins
typically consist of node plugins (that run on each node as a DaemonSet) and
controller plugins.
-->
与 {{< glossary_tooltip text="CSI" term_id="csi" >}} 插件相关联的代码作为
树外脚本和可执行文件来发布且通常发布为容器镜像形式，并使用 DaemonSet 和
StatefulSet 这类标准的 Kubernetes 构造体来部署。
CSI 插件处理 Kubernetes 中的很多卷管理操作：对卷的配备、去配和调整大小，
将卷挂接到 Kubernetes 节点或从节点上解除挂接，将卷挂载到需要持久数据的 Pod
中的某容器或从容器上卸载，使用快照和克隆来备份或恢复持久数据。
CSI 插件通常包含节点插件（以 DaemonSet 形式运行于各节点上）和控制器插件。

<!--
CSI node plugins (especially those associated with persistent volumes exposed
as either block devices or over a shared file-system) need to perform various
privileged operations like scanning of disk devices, mounting of file systems,
etc. These operations differ for each host operating system. For Linux worker
nodes, containerized CSI node plugins are typically deployed as privileged
containers. For Windows worker nodes, privileged operations for containerized
CSI node plugins is supported using
[csi-proxy](https://github.com/kubernetes-csi/csi-proxy), a community-managed,
stand-alone binary that needs to be pre-installed on each Windows node. Please
refer to the deployment guide of the CSI plugin you wish to deploy for further
details.
-->
CSI 节点插件（尤其是那些通过块设备或者共享文件系统形式来提供持久卷的插件）
需要执行很多特权级操作，例如扫描磁盘设备、挂载文件系统等等。
这些操作在不同的宿主操作系统上差别较大。对于 Linux 工作节点而言，容器化的
CSI 节点插件通常部署为特权级的容器。对于 Windows 工作节点而言，容器化的
CSI 节点插件的特权操作通过
[csi-proxy](https://github.com/kubernetes-csi/csi-proxy)
来支持；csi-proxy 是一个社区管理的、独立的可执行文件，需要预安装在每个
Windows 节点之上。请参考你要部署的 CSI 插件的部署指南以进一步了解其细节。

<!--
#### Networking

Networking for Windows containers is exposed through
[CNI plugins](/docs/concepts/extend-kubernetes/compute-storage-net/network-plugins/).
Windows containers function similarly to virtual machines in regards to
networking. Each container has a virtual network adapter (vNIC) which is
connected to a Hyper-V virtual switch (vSwitch). The Host Networking Service
(HNS) and the Host Compute Service (HCS) work together to create containers
and attach container vNICs to networks. HCS is responsible for the management
of containers whereas HNS is responsible for the management of networking
resources such as:
-->
#### 联网     {#networking}

Windows 容器的联网是通过
[CNI 插件](/zh/docs/concepts/extend-kubernetes/compute-storage-net/network-plugins/)
来暴露出来的。Windows 容器的联网行为与虚拟机的联网行为类似。
每个容器有一块虚拟的网络适配器（vNIC）连接到 Hyper-V 的虚拟交换机（vSwitch）。
宿主的联网服务（Host Networking Service，HNS）和宿主计算服务（Host Compute
Service，HCS）协同工作，创建容器并将容器的虚拟网卡连接到网络上。
HCS 负责管理容器，HNS 则负责管理网络资源，例如：

<!--
* Virtual networks (including creation of vSwitches)
* Endpoints / vNICs
* Namespaces
* Policies (Packet encapsulations, Load-balancing rules, ACLs, NAT'ing rules, etc.)

The following service spec types are supported:
-->
* 虚拟网络（包括创建 vSwitch）
* 端点（Endpoint）/ vNIC
* 名字空间（Namespace）
* 策略（报文封装、负载均衡规则、访问控制列表、网络地址转译规则等等）

支持的服务规约类型如下：

* NodePort
* ClusterIP
* LoadBalancer
* ExternalName

<!--
##### Network modes

Windows supports five different networking drivers/modes: L2bridge, L2tunnel,
Overlay, Transparent, and NAT. In a heterogeneous cluster with Windows and
Linux worker nodes, you need to select a networking solution that is
compatible on both Windows and Linux. The following out-of-tree plugins are
supported on Windows, with recommendations on when to use each CNI:
-->
##### 网络模式    {#network-modes}

Windows 支持五种不同的网络驱动/模式：二层桥接（L2bridge）、二层隧道（L2tunnel）、
覆盖网络（Overlay）、透明网络（Transparent）和网络地址转译（NAT）。
在一个包含 Windows 和 Linux 工作节点的异构集群中，你需要选择一种对 Windows 和
Linux 兼容的联网方案。下面是 Windows 上支持的一些树外插件及何时使用某种
CNI 插件的建议：

<table>
 <thead>
  <tr>
   <th><!--Network Driver-->网络驱动</th>
   <th><!--Description-->描述</th>
   <th><!--Container Packet Modifications-->容器报文更改</th>
   <th><!--Network Plugins-->网络插件</th>
   <th><!--Network Plugin Characteristics-->网络插件特点</th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>L2bridge</td>
   <td><!--Containers are attached to an external vSwitch. Containers are attached
      to the underlay network, although the physical network doesn't need to learn
      the container. MACs because they are rewritten on ingress/egress.-->
      容器挂接到外部 vSwitch 上。容器挂接到下层网络之上，但由于容器的 MAC
      地址在入站和出站时被重写，物理网络不需要这些地址。
   </td>
   <td>
      <!--MAC is rewritten to host MAC, IP may be rewritten to host IP using HNS
      OutboundNAT policy.-->
      MAC 地址被重写为宿主系统的 MAC 地址，IP 地址也可能依据 HNS OutboundNAT
      策略重写为宿主的 IP 地址。     
   </td>
   <td>
    <a href="https://github.com/containernetworking/plugins/tree/master/plugins/main/windows/win-bridge">win-bridge<a>、
    <a href="https://github.com/Azure/azure-container-networking/blob/master/docs/cni.md">Azure-CNI</a>、
    <!--Flannel host-gateway uses win-bridge-->
    Flannel 宿主网关（host-gateway）使用 win-bridge
   </td>
   <td>
     <!--win-bridge uses L2bridge network mode,
     connects containers to the underlay of hosts, offering best performance.
     Requires user-defined routes (UDR) for inter-node connectivity.-->
     win-bridge 使用二层桥接（L2bridge）网络模式，将容器连接到下层宿主系统上，
    从而提供最佳性能。需要用户定义的路由（User-Defined Routes，UDR）才能
    实现节点间的连接。
   </td>
  </tr>
  <tr>
   <td>L2Tunnel</td>
   <td>
    <!--This is a special case of l2bridge, but only used on Azure. All packets
    are sent to the virtualization host where SDN policy is applied.-->
    这是二层桥接的一种特殊情形，但仅被用于 Azure 上。
    所有报文都被发送到虚拟化环境中的宿主机上并根据 SDN 策略进行处理。
   </td>
   <td>
    <!--MAC rewritten, IP visible on the underlay network-->
    MAC 地址被改写，IP 地址在下层网络上可见。
   </td>
   <td>
    <a href="https://github.com/Azure/azure-container-networking/blob/master/docs/cni.md">Azure-CNI</a>
   </td>
   <td>
     <!-- Azure-CNI allows integration of containers with Azure vNET, and allows them
      to leverage the set of capabilities that
      <a href="https://azure.microsoft.com/en-us/services/virtual-network/">Azure Virtual Network</a>
      provides. For example, securely connect to Azure services or use Azure NSGs.
      See <a href="https://docs.microsoft.com/en-us/azure/aks/concepts-network#azure-cni-advanced-networking">azure-cni</a>
      for some examples.-->
     Azure-CNI 使得容器能够与 Azure vNET 集成，并允许容器利用
     [Azure 虚拟网络](https://azure.microsoft.com/en-us/services/virtual-network/)
     所提供的功能特性集合。例如，可以安全地连接到 Azure 服务上或者使用 Azure NSG。
     你可以参考
     [azure-cni](https://docs.microsoft.com/en-us/azure/aks/concepts-network#azure-cni-advanced-networking)
     所提供的一些示例。
   </td>
  </tr>
  <tr>
   <td><!--Overlay (Overlay networking for Windows in Kubernetes is in <B>Alpha</B> stage)-->覆盖网络（Kubernetes 中为 Windows 提供的覆盖网络支持处于 *alpha* 阶段）</td>
   <td>
    <!--Containers are given a vNIC connected to an external vSwitch. Each overlay
    network gets its own IP subnet, defined by a custom IP prefix.The overlay
    network driver uses VXLAN encapsulation.-->
    每个容器会获得一个连接到外部 vSwitch 的虚拟网卡（vNIC）。
    每个覆盖网络都有自己的、通过定制 IP 前缀来定义的 IP 子网。
    覆盖网络驱动使用 VxLAN 封装。
   </td>
   <td>
    <!--Encapsulated with an outer header.-->
    封装于外层包头内。
   </td>
   <td>
    <a href="https://github.com/containernetworking/plugins/tree/master/plugins/main/windows/win-overlay">Win-overlay</a>、
    Flannel VXLAN<!--(uses win-overlay)-->（使用 win-overlay）
   </td>
   <td>
    <!--win-overlay should be used when virtual container networks are desired to
    be isolated from underlay of hosts (e.g. for security reasons). Allows for IPs
    to be re-used for different overlay networks (which have different VNID tags)
    if you are restricted on IPs in your datacenter.  This option requires
    <a href="https://support.microsoft.com/help/4489899">KB4489899</a> on Windows Server
    2019.-->
    当（比如出于安全原因）期望虚拟容器网络与下层宿主网络隔离时，
    应该使用 win-overlay。如果你的数据中心可用 IP 地址受限，
    覆盖网络允许你在不同的网络中复用 IP 地址（每个覆盖网络有不同的 VNID 标签）。
    这一选项要求在 Windows Server 2009 上安装
    [KB4489899](https://support.microsoft.com/help/4489899) 补丁。
   </td>
  </tr>
  <tr>
   <td>
    <!--Transparent (special use case for <a href="https://github.com/openvswitch/ovn-kubernetes">ovn-kubernetes</a>)-->
    透明网络（[ovn-kubernetes](https://github.com/openvswitch/ovn-kubernetes) 的特殊用例） 
   </td>
   <td>
    <!--Requires an external vSwitch. Containers are attached to an external
    vSwitch which enables intra-pod communication via logical networks (logical
    switches and routers).-->
    需要一个外部 vSwitch。容器挂接到某外部 vSwitch 上，该 vSwitch
    通过逻辑网络（逻辑交换机和路由器）允许 Pod 间通信。
   </td>
   <td>
    <!--Packet is encapsulated either via
    <a href="https://datatracker.ietf.org/doc/draft-gross-geneve/">GENEVE</a>,
    <a href="https://datatracker.ietf.org/doc/draft-davie-stt/">STT</a> tunneling to reach
    pods which are not on the same host.<br/> Packets are forwarded or dropped
    via the tunnel metadata information supplied by the ovn network controller.
    <br/>
    NAT is done for north-south communication.
    -->
    报文或者通过 [GENEVE](https://datatracker.ietf.org/doc/draft-gross-geneve/) 来封装，
    或者通过 [STT](https://datatracker.ietf.org/doc/draft-davie-stt/) 隧道来封装，
    以便能够到达不在同一宿主系统上的每个 Pod。<br/>
    报文通过 OVN 网络控制器所提供的隧道元数据信息来判定是转发还是丢弃。<br/>
    北-南向通信通过 NAT 网络地址转译来实现。
   </td>
   <td>
    <a href="https://github.com/openvswitch/ovn-kubernetes">ovn-kubernetes</a>
   </td>
   <td>
     <!-- Deploy via <a href="https://github.com/openvswitch/ovn-kubernetes/tree/master/contrib">Ansible</a>.
     Distributed ACLs can be applied via Kubernetes policies. IPAM support.
     Load-balancing can be achieved without kube-proxy. NATing is done without
     using iptables/netsh.-->
     [通过 Ansible 来部署](https://github.com/openvswitch/ovn-kubernetes/tree/master/contrib)。
     所发布的 ACL 可以通过 Kubernetes 策略来应用实施。支持 IPAM 。
     负载均衡能力不依赖 kube-proxy。
     网络地址转译（NAT）也不需要 iptables 或 netsh。
   </td>
  </tr>
  <tr>
   <td><!--NAT (<B>not used in Kubernetes</B>)-->NAT（<B>未在 Kubernetes 中使用</B>）</td>
   <td>
    <!--Containers are given a vNIC connected to an internal vSwitch. DNS/DHCP is
    provided using an internal component called
    <a href="https://blogs.technet.microsoft.com/virtualization/2016/05/25/windows-nat-winnat-capabilities-and-limitations">WinNAT</a>.-->
    容器获得一个连接到某内部 vSwitch 的 vNIC 接口。
    DNS/DHCP 服务通过名为
    [WinNAT](https://blogs.technet.microsoft.com/virtualization/2016/05/25/windows-nat-winnat-capabilities-and-limitations/)
    的内部组件来提供。
   </td>
   <td>
    <!--MAC and IP is rewritten to host MAC/IP.-->
    MAC 地址和 IP 地址都被重写为宿主系统的 MAC 地址和 IP 地址。
   </td>
   <td>
    <a href="https://github.com/Microsoft/windows-container-networking/tree/master/plugins/nat">nat</a>
   </td>
   <td>
    <!--Included here for completeness-->
    列在此表中仅出于完整性考虑
   </td>
  </tr>
 </tbody>
</table>

<!--
As outlined above, the [Flannel](https://github.com/coreos/flannel) CNI
[meta plugin](https://github.com/containernetworking/plugins/tree/master/plugins/meta/flannel)
is also supported on
[Windows](https://github.com/containernetworking/plugins/tree/master/plugins/meta/flannel#windows-support-experimental)
via the [VXLAN network backend](https://github.com/coreos/flannel/blob/master/Documentation/backends.md#vxlan)
(**alpha support** ; delegates to win-overlay) and
[host-gateway network backend](https://github.com/coreos/flannel/blob/master/Documentation/backends.md#host-gw)
(stable support; delegates to win-bridge). This plugin supports delegating to
one of the reference CNI plugins (win-overlay, win-bridge), to work in
conjunction with Flannel daemon on Windows (Flanneld) for automatic node
subnet lease assignment and HNS network creation. This plugin reads in its own
configuration file (cni.conf), and aggregates it with the environment
variables from the FlannelD generated subnet.env file. It then delegates to
one of the reference CNI plugins for network plumbing, and sends the correct
configuration containing the node-assigned subnet to the IPAM plugin (e.g.
host-local).
-->
如前所述，[Flannel](https://github.com/coreos/flannel) CNI
[meta 插件](https://github.com/containernetworking/plugins/tree/master/plugins/meta/flannel)
在 Windows 上也是
[被支持](https://github.com/containernetworking/plugins/tree/master/plugins/meta/flannel#windows-support-experimental)
的，方法是通过 [VXLAN 网络后端](https://github.com/coreos/flannel/blob/master/Documentation/backends.md#vxlan)
（**alpha 阶段** ：委托给 win-overlay）和 
[主机-网关（host-gateway）网络后端](https://github.com/coreos/flannel/blob/master/Documentation/backends.md#host-gw)
（稳定版本；委托给 win-bridge 实现）。
此插件支持将操作委托给所引用的 CNI 插件（win-overlay、win-bridge）之一，
从而能够与 Windows 上的 Flannel 守护进程（Flanneld）一同工作，自动为节点
分配子网租期，创建 HNS 网络。
该插件读入其自身的配置文件（cni.conf），并将其与 FlannelD 所生成的 subnet.env
文件中的环境变量整合，之后将其操作委托给所引用的 CNI 插件之一以完成网络发现，
并将包含节点所被分配的子网信息的正确配置发送给 IPAM 插件（例如 host-local）。

<!--
For the node, pod, and service objects, the following network flows are
supported for TCP/UDP traffic:

* Pod -> Pod (IP)
* Pod -> Pod (Name)
* Pod -> Service (Cluster IP)
* Pod -> Service (PQDN, but only if there are no ".")
* Pod -> Service (FQDN)
* Pod -> External (IP)
* Pod -> External (DNS)
* Node -> Pod
* Pod -> Node
-->
对于节点、Pod 和服务对象，可针对 TCP/UDP 流量支持以下网络数据流：

* Pod -> Pod （IP 寻址）
* Pod -> Pod （名字寻址）
* Pod -> 服务（集群 IP）
* Pod -> 服务（部分限定域名，仅适用于名称中不包含“.”的情形）
* Pod -> 服务（全限定域名）
* Pod -> 集群外部（IP 寻址）
* Pod -> 集群外部（DNS 寻址）
* 节点 -> Pod
* Pod -> 节点

<!--
##### IP address management (IPAM) {#ipam}

The following IPAM options are supported on Windows:

* [Host-local](https://github.com/containernetworking/plugins/tree/master/plugins/ipam/host-local)
* HNS IPAM (Inbox platform IPAM, this is a fallback when no IPAM is set)
* [Azure-vnet-ipam](https://github.com/Azure/azure-container-networking/blob/master/docs/ipam.md) (for azure-cni only)
-->
##### IP 地址管理（IPAM）       {#ipam}

Windows 上支持以下 IPAM 选项：

* [host-local](https://github.com/containernetworking/plugins/tree/master/plugins/ipam/host-local)
* HNS IPAM (Inbox 平台 IPAM，未指定 IPAM 时的默认设置）
* [Azure-vnet-ipam](https://github.com/Azure/azure-container-networking/blob/master/docs/ipam.md)（仅适用于 azure-cni ）

<!--
##### Load balancing and Services

On Windows, you can use the following settings to configure Services and load
balancing behavior:
-->
##### 负载均衡与服务     {#load-balancing-and-services}

在 Windows 系统上，你可以使用以下配置来设定服务和负载均衡行为：

{{< table caption="Windows 服务设置" >}}

<table>
 <thead>
  <tr>
   <th><!--Feature-->功能特性</th>
   <th><!--Description-->描述</th>
   <th><!--Supported Kubernetes version-->所支持的 Kubernetes 版本</th>
   <th><!--Supported Windows OS build-->所支持的 Windows OS 版本</th>
   <th><!--How to enable-->如何启用</th>
  </tr>
 <thead>
 <tbody>
  <tr>
   <td><!--Session affinity-->会话亲和性</td>
   <td>
    <!--Ensures that connections from a particular client are passed to the same
    Pod each time.-->
    确保来自特定客户的连接每次都被交给同一 Pod。
   </td>
   <td>v1.20+</td>
   <td>
    <!--a href="https://blogs.windows.com/windowsexperience/2020/01/28/announcing-windows-server-vnext-insider-preview-build-19551/">Windows Server vNext Insider Preview Build 19551</a> (or higher)-->
    [Windows Server vNext Insider Preview Build 19551](https://blogs.windows.com/windowsexperience/2020/01/28/announcing-windows-server-vnext-insider-preview-build-19551/)
    或更高版本
   </td>
   <td>
    <!--Set <code>service.spec.sessionAffinity</code> to "ClientIP"-->
    将 <code>service.spec.sessionAffinitys</code> 设置为 "ClientIP"
   </td>
  </tr>
  <tr>
   <td><!--Direct Server Return (DSR)-->直接服务器返回（DSR）</td>
   <td>
    <!--Load balancing mode where the IP address fixups and the LBNAT occurs at
    the container vSwitch port directly; service traffic arrives with the source
    IP set as the originating pod IP.
    -->
    这是一种负载均衡模式，IP 地址的修正和负载均衡地址转译（LBNAT）
    直接在容器的 vSwitch 端口上处理；服务流量到达时，其源端 IP 地址
    设置为来源 Pod 的 IP。
   </td>
   <td>v1.20+</td>
   <td>
    Windows Server 2019
   </td>
   <td>
    <!--Set the following flags in kube-proxy:
    <code>--feature-gates="WinDSR=true" --enable-dsr=true</code>-->
    为 kube-proxy 设置标志：`--feature-gates="WinDSR=true" --enable-dsr=true`
   </td>
  </tr>
  <tr>
   <td><!--Preserve-Destination-->保留目标地址</td>
   <td>
    <!--Skips DNAT of service traffic, thereby preserving the virtual IP of the target
    service in packets reaching the backend Pod. Also disables node-node forwarding.-->
    对服务流量略过 DNAT 步骤，这样就可以在到达后端 Pod 的报文中保留目标服务的
    虚拟 IP 地址。还要禁止节点之间的转发。 
   </td>
   <td>v1.20+</td>
   <td><!--Windows Server, version 1903 (or higher)-->Windows Server 1903 或更高版本</td>
   <td>
    <!--Set <code>"preserve-destination": "true"</code> in service annotations
    and enable DSR in kube-proxy.-->
    在服务注解中设置 `"preserve-destination": "true"` 并启用
    kube-proxy 中的 DSR 标志。
   </td>
  </tr>
  <tr>
   <td><!--IPv4/IPv6 dual-stack networking-->IPv4/IPv6 双栈网络</td>
   <td>
    <!--Native IPv4-to-IPv4 in parallel with IPv6-to-IPv6 communications to, from,
    and within a cluster-->
    在集群内外同时支持原生的 IPv4-到-IPv4 和 IPv6-到-IPv6 通信。
   </td>
   <td>v1.19+</td>
   <td><!--Windows Server, version 2004 (or higher)-->Windows Server 2004 或更高版本</td>
   <td>
    <!--See <a href="#ipv4ipv6-dual-stack">IPv4/IPv6 dual-stack</a>-->
    参见 [IPv4/IPv6 双栈网络](#ipv4ipv6-dual-stack)
   </td>
  </tr>
  <tr>
   <td><!--Client IP preservation-->保留客户端 IP</td>
   <td>
    <!--Ensures that source IP of incoming ingress traffic gets preserved. Also
    disables node-node forwarding.-->
    确保入站流量的源 IP 地址被保留。同样要禁止节点之间的转发。
   </td>
   <td>v1.20+</td>
   <td><!--Windows Server, version 2019 (or higher)-->Windows Server 2019 或更高版本</td>
   <td>
    <!--Set <code>service.spec.externalTrafficPolicy</code> to "Local" and enable
    DSR in kube-proxy.-->
    将 <code>service.spec.externalTrafficPolicy</code> 设置为 "Local"，
    并在 kube-proxy 上启用 DSR。
   </td>
  </tr>
 </tbody>
</table>

{{< /table >}}

<!--
#### IPv4/IPv6 dual-stack

You can enable IPv4/IPv6 dual-stack networking for `l2bridge` networks using
the `IPv6DualStack` [feature gate](/docs/reference/command-line-tools-reference/feature-gates/). See
[enable IPv4/IPv6 dual stack](/docs/concepts/services-networking/dual-stack#enable-ipv4ipv6-dual-stack)
for more details.
-->
#### IPv4/IPv6 双栈支持   {#ipv4ipv6-dual-stack}

你可以通过使用 `IPv6DualStack`
[特性门控](/zh/docs/reference/command-line-tools-reference/feature-gates/)
来为 `l2bridge` 网络启用 IPv4/IPv6 双栈联网支持。
进一步的细节可参见
[启用 IPv4/IPv6 双协议栈](/zh/docs/concepts/services-networking/dual-stack#enable-ipv4ipv6-dual-stack)。

<!--
On Windows, using IPv6 with Kubernetes require Windows Server, version 2004
(kernel version 10.0.19041.610) or later.

Overlay (VXLAN) networks on Windows do not support dual-stack networking today.
-->
对 Windows 而言，在 Kubernetes 中使用 IPv6 需要
Windows Server 2004 （内核版本 10.0.19041.610）或更高版本。

目前 Windows 上的覆盖网络（VXLAN）还不支持双协议栈联网。

<!--
### Limitations

Windows is only supported as a worker node in the Kubernetes architecture and
component matrix. This means that a Kubernetes cluster must always include
Linux master nodes, zero or more Linux worker nodes, and zero or more Windows
worker nodes.
-->
### 局限性    {#limitations}

在 Kubernetes 架构和节点阵列中仅支持将 Windows 作为工作节点使用。
这意味着 Kubernetes 集群必须总是包含 Linux 主控节点，零个或者多个 Linux
工作节点以及零个或者多个 Windows 工作节点。

<!--
#### Resource Handling

Linux cgroups are used as a pod boundary for resource controls in Linux.
Containers are created within that boundary for network, process and file
system isolation. The cgroups APIs can be used to gather cpu/io/memory stats.
In contrast, Windows uses a Job object per container with a system namespace
filter to contain all processes in a container and provide logical isolation
from the host. There is no way to run a Windows container without the
namespace filtering in place. This means that system privileges cannot be
asserted in the context of the host, and thus privileged containers are not
available on Windows. Containers cannot assume an identity from the host
because the Security Account Manager (SAM) is separate.
-->
#### 资源处理 {#resource-handling}

Linux 上使用 Linux 控制组（CGroups）作为 Pod 的边界，以实现资源控制。
容器都创建于这一边界之内，从而实现网络、进程和文件系统的隔离。
控制组 CGroups API 可用来收集 CPU、I/O 和内存的统计信息。
与此相比，Windows 为每个容器创建一个带有系统名字空间过滤设置的 Job 对象，
以容纳容器中的所有进程并提供其与宿主系统间的逻辑隔离。
没有现成的名字空间过滤设置是无法运行 Windows 容器的。
这也意味着，系统特权无法在宿主环境中评估，因而 Windows 上也就不存在特权容器。
归咎于独立存在的安全账号管理器（Security Account Manager，SAM），容器也不能
获得宿主系统上的任何身份标识。

<!--
#### Resource Reservations

##### Memory Reservations

Windows does not have an out-of-memory process killer as Linux does. Windows
always treats all user-mode memory allocations as virtual, and pagefiles are
mandatory. The net effect is that Windows won't reach out of memory conditions
the same way Linux does, and processes page to disk instead of being subject
to out of memory (OOM) termination. If memory is over-provisioned and all
physical memory is exhausted, then paging can slow down performance.
-->
#### 资源预留   {#resource-reservations}

##### 内存预留    {#memory-reservations}

Windows 不像 Linux 一样有一个内存耗尽（Out-of-memory）进程杀手（Process
Killer）机制。Windows 总是将用户态的内存分配视为虚拟请求，页面文件（Pagefile）
是必需的。这一差异的直接结果是 Windows 不会像 Linux 那样出现内存耗尽的状况，
系统会将进程内存页面写入磁盘而不会因内存耗尽而终止进程。
当内存被过量使用且所有物理内存都被用光时，系统的换页行为会导致性能下降。

<!--
Keeping memory usage within reasonable bounds is possible using the kubelet
parameters `--kubelet-reserve` and/or `--system-reserve` to account for memory
usage on the node (outside of containers). This reduces
[NodeAllocatable](/docs/tasks/administer-cluster/reserve-compute-resources/#node-allocatable)).
-->
使用 kubelet 参数 `--kubelet-reserve` 与/或 `-system-reserve` 可以统计
节点上的内存用量（各容器之外），进而可能将内存用量限制在一个合理的范围，。
这样做会减少节点可分配内存
（[NodeAllocatable](/zh/docs/tasks/administer-cluster/reserve-compute-resources/#node-allocatable)）。

<!--
As you deploy workloads, use resource limits (must set only limits or limits
must equal requests) on containers. This also subtracts from NodeAllocatable
and prevents the scheduler from adding more pods once a node is full.
-->
在你部署工作负载时，对容器使用资源限制（必须仅设置 limits 或者让 limits 等于
requests 值）。这也会从 NodeAllocatable 中耗掉部分内存量，从而避免在节点
负荷已满时调度器继续向节点添加 Pods。

<!--
A best practice to avoid over-provisioning is to configure the kubelet with a
system reserved memory of at least 2GB to account for Windows, Docker, and
Kubernetes processes.
-->
避免过量分配的最佳实践是为 kubelet 配置至少 2 GB 的系统预留内存，以供
Windows、Docker 和 Kubernetes 进程使用。

<!--
##### CPU Reservations

To account for Windows, Docker and other Kubernetes host processes it is
recommended to reserve a percentage of CPU so they are able to respond to
events. This value needs to be scaled based on the number of CPU cores
available on the Windows node.To determine this percentage a user should
identify the maximum pod density for each of their nodes and monitor the CPU
usage of the system services choosing a value that meets their workload needs.
-->
##### CPU 预留   {#cpu-reservations}

为了统计 Windows、Docker 和其他 Kubernetes 宿主进程的 CPU 用量，建议
预留一定比例的 CPU，以便对事件作出相应。此值需要根据 Windows 节点上
CPU 核的个数来调整，要确定此百分比值，用户需要为其所有节点确定 Pod
密度的上线，并监控系统服务的 CPU 用量，从而选择一个符合其负载需求的值。

<!--
Keeping CPU usage within reasonable bounds is possible using the kubelet
parameters `--kubelet-reserve` and/or `--system-reserve` to account for CPU
usage on the node (outside of containers). This reduces
[NodeAllocatable](/docs/tasks/administer-cluster/reserve-compute-resources/#node-allocatable). 
-->
使用 kubelet 参数 `--kubelet-reserve` 与/或 `-system-reserve` 可以统计
节点上的 CPU 用量（各容器之外），进而可能将 CPU 用量限制在一个合理的范围，。
这样做会减少节点可分配 CPU
（[NodeAllocatable](/zh/docs/tasks/administer-cluster/reserve-compute-resources/#node-allocatable)）。

<!--
##### Feature Restrictions

* TerminationGracePeriod: not implemented
* Single file mapping: to be implemented with CRI-ContainerD
* Termination message: to be implemented with CRI-ContainerD
* Privileged Containers: not currently supported in Windows containers
* HugePages: not currently supported in Windows containers
* The existing node problem detector is Linux-only and requires privileged
  containers. In general, we don't expect this to be used on Windows because
  privileged containers are not supported
* Not all features of shared namespaces are supported (see API section for
  more details)
-->
##### 功能特性限制    {#feature-restrictions}

* 终止宽限期（Termination Grace Period）：未实现
* 单文件映射：将用 CRI-ContainerD 来实现
* 终止消息（Termination message）：将用 CRI-ContainerD 来实现
* 特权容器：Windows 容器当前不支持
* 巨页（Huge Pages）：Windows 容器当前不支持
* 现有的节点问题探测器（Node Problem Detector）仅适用于 Linux，且要求使用特权容器。
  一般而言，我们不设想此探测器能用于 Windows 节点，因为 Windows 不支持特权容器。
* 并非支持共享名字空间的所有功能特性（参见 API 节以了解详细信息）

<!--
#### Difference in behavior of flags when compared to Linux

The behavior of the following kubelet flags is different on Windows nodes as described below:

* `--kubelet-reserve`, `--system-reserve` , and `--eviction-hard` flags update
  Node Allocatable
* Eviction by using `--enforce-node-allocable` is not implemented
* Eviction by using `--eviction-hard` and `--eviction-soft` are not implemented
* MemoryPressure Condition is not implemented
* There are no OOM eviction actions taken by the kubelet
* Kubelet running on the windows node does not have memory restrictions.
  `--kubelet-reserve` and `--system-reserve` do not set limits on kubelet or
  processes running on the host. This means kubelet or a process on the host
  could cause memory resource starvation outside the node-allocatable and
  scheduler
* An additional flag to set the priority of the kubelet process is available
  on the Windows nodes called `--windows-priorityclass`. This flag allows
  kubelet process to get more CPU time slices when compared to other processes
  running on the Windows host. More information on the allowable values and
  their meaning is available at
  [Windows Priority Classes](https://docs.microsoft.com/en-us/windows/win32/procthread/scheduling-priorities#priority-class).
  In order for kubelet to always have enough CPU cycles it is recommended to set
  this flag to `ABOVE_NORMAL_PRIORITY_CLASS` and above
-->
#### 与 Linux 相比参数行为的差别

以下 kubelet 参数的行为在 Windows 节点上有些不同，描述如下：

* `--kubelet-reserve`、`--system-reserve` 和 `--eviction-hard` 标志
  会更新节点可分配资源量
* 未实现通过使用 `--enforce-node-allocable` 来完成的 Pod 驱逐
* 未实现通过使用 `--eviction-hard` 和 `--eviction-soft` 来完成的 Pod 驱逐
* `MemoryPressure` 状况未实现
* `kubelet` 不会采取措施来执行基于 OOM 的驱逐动作
* Windows 节点上运行的 kubelet 没有内存约束。
  `--kubelet-reserve` 和 `--system-reserve` 不会为 kubelet 或宿主系统上运行
  的进程设限。这意味着 kubelet 或宿主系统上的进程可能导致内存资源紧张，
  而这一情况既不受节点可分配量影响，也不会被调度器感知。
* 在 Windows 节点上存在一个额外的参数用来设置 kubelet 进程的优先级，称作
  `--windows-priorityclass`。此参数允许 kubelet 进程获得与 Windows 宿主上
  其他进程相比更多的 CPU 时间片。
  关于可用参数值及其含义的进一步信息可参考
  [Windows Priority Classes](https://docs.microsoft.com/en-us/windows/win32/procthread/scheduling-priorities#priority-class)。
  为了让 kubelet 总能够获得足够的 CPU 周期，建议将此参数设置为
  `ABOVE_NORMAL_PRIORITY_CLASS` 或更高。

<!--
#### Storage

Windows has a layered filesystem driver to mount container layers and create a
copy filesystem based on NTFS. All file paths in the container are resolved
only within the context of that container.

* With Docker Volume mounts can only target a directory in the container, and
  not an individual file. This limitation does not exist with CRI-containerD.

* Volume mounts cannot project files or directories back to the host
  filesystem

* Read-only filesystems are not supported because write access is always
  required for the Windows registry and SAM database. However, read-only
  volumes are supported
* Volume user-masks and permissions are not available. Because the SAM is not
  shared between the host & container, there's no mapping between them. All
  permissions are resolved within the context of the container
-->
#### 存储     {#storage}

Windows 上包含一个分层的文件系统来挂载容器的分层，并会基于 NTFS 来创建一个
拷贝文件系统。容器中的所有文件路径都仅在该容器的上下文内完成解析。

* Docker 卷挂载仅可针对容器中的目录进行，不可针对独立的文件。
  这一限制不适用于 CRI-containerD。
* 卷挂载无法将文件或目录投射回宿主文件系统。
* 不支持只读文件系统，因为 Windows 注册表和 SAM 数据库总是需要写访问权限。
  不过，Windows 支持只读的卷。
* 不支持卷的用户掩码和访问许可，因为宿主与容器之间并不共享 SAM，二者之间不存在
  映射关系。所有访问许可都是在容器上下文中解析的。

<!--
As a result, the following storage functionality is not supported on Windows nodes

* Volume subpath mounts. Only the entire volume can be mounted in a Windows container.
* Subpath volume mounting for Secrets
* Host mount projection
* DefaultMode (due to UID/GID dependency)
* Read-only root filesystem. Mapped volumes still support readOnly
* Block device mapping
* Memory as the storage medium
* File system features like uui/guid, per-user Linux filesystem permissions
* NFS based storage/volume support
* Expanding the mounted volume (resizefs)
-->
因此，Windows 节点上不支持以下存储功能特性：

* 卷的子路径挂载；只能在 Windows 容器上挂载整个卷。
* 为 Secret 执行子路径挂载；
* 宿主挂载投射；
* 默认访问模式 defaultMode（因为该特性依赖 UID/GID）；
* 只读的根文件系统；映射的卷仍然支持 `readOnly`；
* 块设备映射；
* 将内存作为存储介质；
* 类似 UUID/GUID、每用户不同的 Linux 文件系统访问许可等文件系统特性；
* 基于 NFS 的存储和卷支持；
* 扩充已挂载卷（resizefs）。

<!--
#### Networking {#networking-limitations}

Windows Container Networking differs in some important ways from Linux
networking. The [Microsoft documentation for Windows Container Networking](https://docs.microsoft.com/en-us/virtualization/windowscontainers/container-networking/architecture)
contains additional details and background.
-->
#### 联网   {#networking-limitations}

Windows 容器联网与 Linux 联网有着非常重要的差别。
[Microsoft documentation for Windows Container Networking](https://docs.microsoft.com/en-us/virtualization/windowscontainers/container-networking/architecture)
中包含额外的细节和背景信息。

<!--
The Windows host networking service and virtual switch implement namespacing
and can create virtual NICs as needed for a pod or container. However, many
configurations such as DNS, routes, and metrics are stored in the Windows
registry database rather than /etc/... files as they are on Linux. The Windows
registry for the container is separate from that of the host, so concepts like
mapping /etc/resolv.conf from the host into a container don't have the same
effect they would on Linux. These must be configured using Windows APIs run in
the context of that container. Therefore CNI implementations need to call the
HNS instead of relying on file mappings to pass network details into the pod
or container.
-->
Windows 宿主联网服务和虚拟交换机实现了名字空间隔离，可以根据需要为 Pod 或容器
创建虚拟的网络接口（NICs）。不过，很多类似 DNS、路由、度量值之类的配置数据都
保存在 Windows 注册表数据库中而不是像 Linux 一样保存在 `/etc/...` 文件中。
Windows 为容器提供的注册表与宿主系统的注册表是分离的，因此类似于将 /etc/resolv.conf
文件从宿主系统映射到容器中的做法不会产生与 Linux 系统相同的效果。
这些信息必须在容器内部使用 Windows API 来配置。
因此，CNI 实现需要调用 HNS，而不是依赖文件映射来将网络细节传递到 Pod
或容器中。

<!--
The following networking functionality is not supported on Windows nodes

* Host networking mode is not available for Windows pods

* Local NodePort access from the node itself fails (works for other nodes or
  external clients)

* Accessing service VIPs from nodes will be available with a future release of
  Windows Server

* A single service can only support up to 64 backend pods / unique destination IPs

* Overlay networking support in kube-proxy is a beta feature. In addition, it
  requires
  [KB4482887](https://support.microsoft.com/en-us/help/4482887/windows-10-update-kb4482887)
  to be installed on Windows Server 2019

* Local Traffic Policy in non-DSR mode
* Windows containers connected to overlay networks do not support
  communicating over the IPv6 stack. There is outstanding Windows platform
  work required to enable this network driver to consume IPv6 addresses and
  subsequent Kubernetes work in kubelet, kube-proxy, and CNI plugins.
-->
Windows 节点不支持以下联网功能：

* Windows Pod 不能使用宿主网络模式；
* 从节点本地访问 NodePort 会失败（但从其他节点或外部客户端可访问）
* Windows Server 的未来版本中会支持从节点访问服务的 VIP；
* 每个服务最多支持 64 个后端 Pod 或独立的目标 IP 地址；
* kube-proxy 的覆盖网络支持是 Beta 特性。此外，它要求在 Windows Server 2019 上安装
  [KB4482887](https://support.microsoft.com/en-us/help/4482887/windows-10-update-kb4482887) 补丁；
* 非 DSR（保留目标地址）模式下的本地流量策略；
* 连接到覆盖网络的 Windows 容器不支持使用 IPv6 协议栈通信。
  要使得这一网络驱动支持 IPv6 地址需要在 Windows 平台上开展大量的工作，
  还需要在 Kubernetes 侧修改 kubelet、kube-proxy 以及 CNI 插件。
<!--
* Outbound communication using the ICMP protocol via the win-overlay,
  win-bridge, and Azure-CNI plugin. Specifically, the Windows data plane
  ([VFP](https://www.microsoft.com/en-us/research/project/azure-virtual-filtering-platform/))
  doesn't support ICMP packet transpositions. This means:

  * ICMP packets directed to destinations within the same network (e.g. pod to
    pod communication via ping) work as expected and without any limitations

  * TCP/UDP packets work as expected and without any limitations

  * ICMP packets directed to pass through a remote network (e.g. pod to
    external internet communication via ping) cannot be transposed and thus
    will not be routed back to their source

  * Since TCP/UDP packets can still be transposed, one can substitute `ping
    <destination>` with `curl <destination>` to be able to debug connectivity
    to the outside world.
-->
* 通过 win-overlay、win-bridge 和 Azure-CNI 插件使用 ICMP 协议向集群外通信。
  尤其是，Windows 数据面
  （[VFP](https://www.microsoft.com/en-us/research/project/azure-virtual-filtering-platform/)）
  不支持转换 ICMP 报文。这意味着：

  * 指向同一网络内目标地址的 ICMP 报文（例如 Pod 之间的 ping 通信）是可以工作的，
    没有局限性；
  * TCP/UDP 报文可以正常工作，没有局限性；
  * 指向远程网络的 ICMP 报文（例如，从 Pod 中 ping 外部互联网的通信）无法被转换，
    因此也无法被路由回到其源点；
  * 由于 TCP/UDP 包仍可被转换，用户可以将 `ping <目标>` 操作替换为 `curl <目标>`
    以便能够调试与外部世界的网络连接。

<!--
These features were added in Kubernetes v1.15:

* `kubectl port-forward`
-->
Kubernetes v1.15 中添加了以下功能特性：

* `kubectl port-forward`

<!--
##### CNI Plugins

* Windows reference network plugins win-bridge and win-overlay do not
  currently implement [CNI spec](https://github.com/containernetworking/cni/blob/master/SPEC.md) v0.4.0
  due to missing "CHECK" implementation.
* The Flannel VXLAN CNI has the following limitations on Windows:

  1. Node-pod connectivity isn't possible by design. It's only possible for
     local pods with Flannel v0.12.0 (or higher).
  1. We are restricted to using VNI 4096 and UDP port 4789. The VNI limitation
     is being worked on and will be overcome in a future release (open-source
     flannel changes). See the official
     [Flannel VXLAN](https://github.com/coreos/flannel/blob/master/Documentation/backends.md#vxlan)
     backend docs for more details on these parameters.
-->
##### CNI 插件    {#cni-plugins}

* Windows 参考网络插件 win-bridge 和 win-overlay 当前未实现
  [CNI spec](https://github.com/containernetworking/cni/blob/master/SPEC.md) v0.4.0，
  原因是缺少检查（CHECK）用的实现。

* Windows 上的 Flannel VXLAN CNI 有以下局限性：

  1. 其设计上不支持从节点到 Pod 的连接。
     只有在 Flannel v0.12.0 或更高版本后才有可能访问本地 Pods。
  2. 我们被限制只能使用 VNI 4096 和 UDP 端口 4789。
     VNI 的限制正在被解决，会在将来的版本中消失（开源的 Flannel 更改）。
     参见官方的 [Flannel VXLAN](https://github.com/coreos/flannel/blob/master/Documentation/backends.md#vxlan)
     后端文档以了解关于这些参数的详细信息。

##### DNS {#dns-limitations}

<!--
* ClusterFirstWithHostNet is not supported for DNS. Windows treats all names
  with a '.' as a FQDN and skips PQDN resolution

* On Linux, you have a DNS suffix list, which is used when trying to resolve
  PQDNs. On Windows, we only have 1 DNS suffix, which is the DNS suffix
  associated with that pod's namespace (`mydns.svc.cluster.local` for example).
  Windows can resolve FQDNs and services or names resolvable with just that
  suffix. For example, a pod spawned in the default namespace, will have the DNS
  suffix `default.svc.cluster.local`. On a Windows pod, you can resolve both
  `kubernetes.default.svc.cluster.local` and `kubernetes`, but not the
  in-betweens, like `kubernetes.default` or `kubernetes.default.svc`.

* On Windows, there are multiple DNS resolvers that can be used. As these come
  with slightly different behaviors, using the `Resolve-DNSName` utility for
  name query resolutions is recommended.
-->
* 不支持 DNS 的 ClusterFirstWithHostNet 配置。Windows 将所有包含 “.” 的名字
  视为全限定域名（FQDN），因而不会对其执行部分限定域名（PQDN）解析。

* 在 Linux 上，你可以有一个 DNS 后缀列表供解析部分限定域名时使用。
  在 Windows 上，我们只有一个 DNS 后缀，即与该 Pod 名字空间相关联的 DNS
  后缀（例如 `mydns.svc.cluster.local`）。
  Windows 可以解析全限定域名、或者恰好可用该后缀来解析的服务名称。
  例如，在 default 名字空间中生成的 Pod 会获得 DNS 后缀
  `default.svc.cluster.local`。在 Windows Pod 中，你可以解析
  `kubernetes.default.svc.cluster.local` 和 `kubernetes`，但无法解析二者
  之间的形式，如 `kubernetes.default` 或 `kubernetes.default.svc`。

* 在 Windows 上，可以使用的 DNS 解析程序有很多。由于这些解析程序彼此之间
  会有轻微的行为差别，建议使用 `Resolve-DNSName` 工具来完成名字查询解析。

<!--
##### IPv6

Kubernetes on Windows does not support single-stack "IPv6-only" networking.
However,dual-stack IPv4/IPv6 networking for pods and nodes with single-family
services is supported.
See [IPv4/IPv6 dual-stack networking](#ipv4ipv6-dual-stack) for more details.
-->
##### IPv6

Windows 上的 Kubernetes 不支持单协议栈的“只用 IPv6”联网选项。
不过，系统支持在 IPv4/IPv6 双协议栈的 Pod 和节点上运行单协议家族的服务。
更多细节可参阅 [IPv4/IPv6 双协议栈联网](#ipv4ipv6-dual-stack)一节。

<!--
##### Session affinity

Setting the maximum session sticky time for Windows services using
`service.spec.sessionAffinityConfig.clientIP.timeoutSeconds` is not supported.
-->
##### 会话亲和性    {#session-affinity}

不支持使用 `service.spec.sessionAffinityConfig.clientIP.timeoutSeconds` 来为
Windows 服务设置最大会话粘滞时间。

<!--
##### Security

Secrets are written in clear text on the node's volume (as compared to
tmpfs/in-memory on linux). This means customers have to do two things

1. Use file ACLs to secure the secrets file location
1. Use volume-level encryption using
   [BitLocker](https://docs.microsoft.com/en-us/windows/security/information-protection/bitlocker/bitlocker-how-to-deploy-on-windows-server)
-->
##### 安全性     {#security}

Secret 以明文形式写入节点的卷中（而不是像 Linux 那样写入内存或 tmpfs 中）。
这意味着客户必须做以下两件事：

1. 使用文件访问控制列表来保护 Secret 文件所在的位置
1. 使用 [BitLocker](https://docs.microsoft.com/en-us/windows/security/information-protection/bitlocker/bitlocker-how-to-deploy-on-windows-server)
   来执行卷层面的加密

<!--
[RunAsUserName](/docs/tasks/configure-pod-container/configure-runasusername)
can be specified for Windows Pod's or Container's to execute the Container
processes as a node-default user. This is roughly equivalent to
[RunAsUser](/docs/concepts/policy/pod-security-policy/#users-and-groups).

Linux specific pod security context privileges such as SELinux, AppArmor,
Seccomp, Capabilities (POSIX Capabilities), and others are not supported.

In addition, as mentioned already, privileged containers are not supported on
Windows.
-->
用户可以为 Windows Pods 或 Container 设置
[`RunAsUserName`](/zh/docs/tasks/configure-pod-container/configure-runasusername)
以便以非节点默认用户来执行容器中的进程。这大致等价于设置
[`RunAsUser`](/zh/docs/concepts/policy/pod-security-policy/#users-and-groups)。

不支持特定于 Linux 的 Pod 安全上下文特权，例如 SELinux、AppArmor、Seccomp、
权能字（POSIX 权能字）等等。

此外，如前所述，Windows 不支持特权容器。

<!--
#### API

There are no differences in how most of the Kubernetes APIs work for Windows.
The subtleties around what's different come down to differences in the OS and
container runtime. In certain situations, some properties on workload APIs
such as Pod or Container were designed with an assumption that they are
implemented on Linux, failing to run on Windows.

At a high level, these OS concepts are different:
-->
#### API

对 Windows 而言，大多数 Kubernetes API 的工作方式没有变化。
一些不易察觉的差别通常体现在 OS 和容器运行时上的不同。
在某些场合，负载 API （如 Pod 或 Container）的某些属性在设计时假定其
在 Linux 上实现，因此会无法在 Windows 上运行。

在较高层面，不同的 OS 概念有：

<!--
* Identity - Linux uses userID (UID) and groupID (GID) which are represented
  as integer types. User and group names are not canonical - they are an alias
  in `/etc/groups` or `/etc/passwd` back to UID+GID. Windows uses a larger
  binary security identifier (SID) which is stored in the Windows Security
  Access Manager (SAM) database. This database is not shared between the host
  and containers, or between containers.

* File permissions - Windows uses an access control list based on SIDs, rather
  than a bitmask of permissions and UID+GID
-->
* 身份标识 - Linux 使用证书类型来表示用户 ID（UID）和组 ID（GID）。用户和组名
  没有特定标准，它们是 `/etc/groups` 或 `/etc/passwd` 中的别名表项，会映射回
  UID+GID。Windows 使用一个更大的二进制安全标识符（SID），保存在 Windows
  安全访问管理器（Security Access Manager，SAM）数据库中。此数据库并不在宿主系统
  与容器间，或者任意两个容器之间共享。

* 文件许可 - Windows 使用基于 SID 的访问控制列表，而不是基于 UID+GID 的访问权限位掩码。

<!--
* File paths - convention on Windows is to use `\` instead of `/`. The Go IO
  libraries accept both types of file path separators. However, when you're
  setting a path or command line that's interpreted inside a container, `\` may
  be needed.

* Signals - Windows interactive apps handle termination differently, and can
  implement one or more of these:

  * A UI thread handles well-defined messages including `WM_CLOSE`

  * Console apps handle ctrl-c or ctrl-break using a Control Handler

  * Services register a Service Control Handler function that can accept
    `SERVICE_CONTROL_STOP` control codes
-->
* 文件路径 - Windows 上的习惯是使用 `\` 而非 `/`。Go 语言的 IO
  库同时接受这两种文件路径分隔符。不过，当你在指定要在容器内解析的路径或命令行时，
  可能需要使用 `\`。

* 信号（Signal） - Windows 交互式应用以不同方式来处理终止事件，并可实现以下方式之一或组合：

  * UI 线程处理包含 `WM_CLOSE` 在内的良定的消息

  * 控制台应用使用控制处理程序来处理 Ctrl-C 或 Ctrl-Break

  * 服务会注册服务控制处理程序，接受 `SERVICE_CONTROL_STOP` 控制代码

<!--
Exit Codes follow the same convention where 0 is success, nonzero is failure.
The specific error codes may differ across Windows and Linux. However, exit
codes passed from the Kubernetes components (kubelet, kube-proxy) are
unchanged.
-->
退出代码遵从相同的习惯，0 表示成功，非 0 值表示失败。
特定的错误代码在 Windows 和 Linux 上可能会不同。不过，从 Kubernetes 组件
（kubelet、kube-proxy）所返回的退出代码是没有变化的。

<!--
##### V1.Container

* V1.Container.ResourceRequirements.limits.cpu and
  V1.Container.ResourceRequirements.limits.memory - Windows doesn't use hard
  limits for CPU allocations. Instead, a share system is used. The existing
  fields based on millicores are scaled into relative shares that are followed
  by the Windows scheduler.
  See [kuberuntime/helpers_windows.go](https://github.com/kubernetes/kubernetes/blob/master/pkg/kubelet/kuberuntime/helpers_windows.go),
  and [resource controls in Microsoft docs](https://docs.microsoft.com/en-us/virtualization/windowscontainers/manage-containers/resource-controls)

  * Huge pages are not implemented in the Windows container runtime, and are
    not available. They require
    [asserting a user privilege](https://docs.microsoft.com/en-us/windows/desktop/Memory/large-page-support)
    that's not configurable for containers.
-->
* `v1.Container.ResourceRequirements.limits.cpu` 和
  `v1.Container.ResourceRequirements.limits.memory` - Windows
  不对 CPU 分配设置硬性的限制。与之相反，Windows 使用一个份额（share）系统。
  基于毫核（millicores）的现有字段值会被缩放为相对的份额值，供 Windows 调度器使用。
  参见 [kuberuntime/helpers_windows.go](https://github.com/kubernetes/kubernetes/blob/master/pkg/kubelet/kuberuntime/helpers_windows.go) 和
  [Microsoft 文档中关于资源控制的部分](https://docs.microsoft.com/en-us/virtualization/windowscontainers/manage-containers/resource-controls)。

  * Windows 容器运行时中没有实现巨页支持，因此相关特性不可用。
    巨页支持需要[判定用户的特权](https://docs.microsoft.com/en-us/windows/desktop/Memory/large-page-support)
    而这一特性无法在容器级别配置。

<!--
* V1.Container.ResourceRequirements.requests.cpu and
  V1.Container.ResourceRequirements.requests.memory - Requests are subtracted
  from node available resources, so they can be used to avoid overprovisioning a
  node. However, they cannot be used to guarantee resources in an
  overprovisioned node. They should be applied to all containers as a best
  practice if the operator wants to avoid overprovisioning entirely.

* V1.Container.SecurityContext.allowPrivilegeEscalation - not possible on
  Windows, none of the capabilities are hooked up
-->
* `v1.Container.ResourceRequirements.requests.cpu` 和
  `v1.Container.ResourceRequirements.requests.memory` - 请求
  值会从节点可分配资源中扣除，从而可用来避免节点上的资源过量分配。
  但是，它们无法用来在一个已经过量分配的节点上提供资源保障。
  如果操作员希望彻底避免过量分配，作为最佳实践，他们就需要为所有容器设置资源请求值。

* `v1.Container.SecurityContext.allowPrivilegeEscalation` - 在 Windows
  上无法实现，对应的权能无一可在 Windows 上生效。

<!--
* V1.Container.SecurityContext.Capabilities - POSIX capabilities are not
  implemented on Windows

* V1.Container.SecurityContext.privileged - Windows doesn't support privileged
  containers

* V1.Container.SecurityContext.procMount - Windows doesn't have a /proc
  filesystem

* V1.Container.SecurityContext.readOnlyRootFilesystem - not possible on
  Windows, write access is required for registry & system processes to run
  inside the container
-->
* `v1.Container.SecurityContext.Capabilities` - Windows 上未实现 POSIX 权能机制
* `v1.Container.SecurityContext.privileged` - Windows 不支持特权容器
* `v1.Container.SecurityContext.procMount` - Windows 不包含 `/proc` 文件系统
* `v1.Container.SecurityContext.readOnlyRootFilesystem` - 在 Windows 上无法实现，
  要在容器内使用注册表或运行系统进程就必需写访问权限。

<!--
* V1.Container.SecurityContext.runAsGroup - not possible on Windows, no GID
  support

* V1.Container.SecurityContext.runAsNonRoot - Windows does not have a root
  user. The closest equivalent is ContainerAdministrator which is an identity
  that doesn't exist on the node.

* V1.Container.SecurityContext.runAsUser - not possible on Windows, no UID
  support as int.

* V1.Container.SecurityContext.seLinuxOptions - not possible on Windows, no SELinux

* V1.Container.terminationMessagePath - this has some limitations in that
  Windows doesn't support mapping single files. The default value is
  `/dev/termination-log`, which does work because it does not exist on Windows by
  default.
-->
* `v1.Container.SecurityContext.runAsGroup` - 在 Windows 上无法实现，没有 GID 支持

* `v1.Container.SecurityContext.runAsNonRoot` - Windows 上没有 root 用户。
  与之最接近的等价用户是 `ContainerAdministrator`，而该身份标识在节点上并不存在。

* `v1.Container.SecurityContext.runAsUser` - 在 Windows 上无法实现，
  因为没有作为整数支持的 GID。

* `v1.Container.SecurityContext.seLinuxOptions` - 在 Windows 上无法实现，
  因为没有 SELinux

* `V1.Container.terminationMessagePath` - 因为 Windows 不支持单个文件的映射，这一功能
  在 Windows 上也受限。默认值 `/dev/termination-log` 在 Windows 上也无法使用因为
  对应路径在 Windows 上不存在。

<!--
##### V1.Pod

* V1.Pod.hostIPC, v1.pod.hostpid - host namespace sharing is not possible on Windows

* V1.Pod.hostNetwork - There is no Windows OS support to share the host network

* V1.Pod.dnsPolicy - ClusterFirstWithHostNet - is not supported because Host
  Networking is not supported on Windows.

* V1.Pod.podSecurityContext - see V1.PodSecurityContext below

* V1.Pod.shareProcessNamespace - this is a beta feature, and depends on Linux
  namespaces which are not implemented on Windows. Windows cannot share
  process namespaces or the container's root filesystem. Only the network can be
  shared.
-->
##### V1.Pod

* `v1.Pod.hostIPC`、`v1.Pod.hostPID` - Windows 不支持共享宿主系统的名字空间
* `v1.Pod.hostNetwork` - Windows 操作系统不支持共享宿主网络
* `v1.Pod.dnsPolicy` - 不支持 `ClusterFirstWithHostNet`，因为 Windows 不支持宿主网络
* `v1.Pod.podSecurityContext` - 参见下面的 `v1.PodSecurityContext`
* `v1.Pod.shareProcessNamespace` - 此为 Beta 特性且依赖于 Windows 上未实现
  的 Linux 名字空间。
  Windows 无法共享进程名字空间或者容器的根文件系统。只能共享网络。

<!--
* V1.Pod.terminationGracePeriodSeconds - this is not fully implemented in
  Docker on Windows, see:
  [reference](https://github.com/moby/moby/issues/25982). The behavior today is
  that the `ENTRYPOINT` process is sent `CTRL_SHUTDOWN_EVENT`, then Windows waits 5
  seconds by default, and finally shuts down all processes using the normal
  Windows shutdown behavior. The 5 second default is actually in the Windows
  registry [inside the container](https://github.com/moby/moby/issues/25982#issuecomment-426441183),
  so it can be overridden when the container is built.

* V1.Pod.volumeDevices - this is a beta feature, and is not implemented on
  Windows. Windows cannot attach raw block devices to pods.
-->
* `v1.Pod.terminationGracePeriodSeconds` - 这一特性未在 Windows 版本的 Docker 中完全实现。
  参见[问题报告](https://github.com/moby/moby/issues/25982)。
  目前实现的行为是向 `ENTRYPOINT` 进程发送 `CTRL_SHUTDOWN_EVENT` 事件，之后 Windows 默认
  等待 5 秒钟，并最终使用正常的 Windows 关机行为关闭所有进程。
  这里的 5 秒钟默认值实际上保存在
  [容器内](https://github.com/moby/moby/issues/25982#issuecomment-426441183)
  的 Windows 注册表中，因此可以在构造容器时重载。

* `v1.Pod.volumeDevices` - 此为 Beta 特性且未在 Windows 上实现。Windows 无法挂接
  原生的块设备到 Pod 中。

<!--
* V1.Pod.volumes - EmptyDir, Secret, ConfigMap, HostPath - all work and have
  tests in TestGrid

  * V1.emptyDirVolumeSource - the Node default medium is disk on Windows.
    Memory is not supported, as Windows does not have a built-in RAM disk.

* V1.VolumeMount.mountPropagation - mount propagation is not supported on Windows.
-->
* `v1.Pod.volumes` - `emptyDir`、`secret`、`configMap` 和 `hostPath`
  都可正常工作且在 TestGrid 中测试。

  * `v1.emptyDir.volumeSource` - Windows 上节点的默认介质是磁盘。
    不支持将内存作为介质，因为 Windows 不支持内置的 RAM 磁盘。

* `v1.VolumeMount.mountPropagation` - Windows 上不支持挂载传播。

<!--
##### V1.PodSecurityContext

None of the PodSecurityContext fields work on Windows. They're listed here for
reference.

* V1.PodSecurityContext.SELinuxOptions - SELinux is not available on Windows

* V1.PodSecurityContext.RunAsUser - provides a UID, not available on Windows

* V1.PodSecurityContext.RunAsGroup - provides a GID, not available on Windows

* V1.PodSecurityContext.RunAsNonRoot - Windows does not have a root user. The
  closest equivalent is ContainerAdministrator which is an identity that
  doesn't exist on the node.

* V1.PodSecurityContext.SupplementalGroups - provides GID, not available on Windows

* V1.PodSecurityContext.Sysctls - these are part of the Linux sysctl
  interface. There's no equivalent on Windows.
-->
##### V1.PodSecurityContext

PodSecurityContext 的所有选项在 Windows 上都无法工作。这些选项列在下面仅供参考。

* `v1.PodSecurityContext.seLinuxOptions` - Windows 上无 SELinux

* `v1.PodSecurityContext.runAsUser` - 提供 UID；Windows 不支持

* `v1.PodSecurityContext.runAsGroup` - 提供 GID；Windows 不支持

* `v1.PodSecurityContext.runAsNonRoot` - Windows 上没有 root 用户
  最接近的等价账号是 `ContainerAdministrator`，而该身份标识在节点上不存在

* `v1.PodSecurityContext.supplementalGroups` - 提供 GID；Windows 不支持

* `v1.PodSecurityContext.sysctls` - 这些是 Linux sysctl 接口的一部分；Windows 上
  没有等价机制。

<!--
#### Operating System Version Restrictions

Windows has strict compatibility rules, where the host OS version must match
the container base image OS version. Only Windows containers with a container
operating system of Windows Server 2019 are supported. Hyper-V isolation of
containers, enabling some backward compatibility of Windows container image
versions, is planned for a future release.
-->
#### 操作系统版本限制  {#operating-system-version-restrictions}

Windows 有着严格的兼容性规则，宿主 OS 的版本必须与容器基准镜像 OS 的版本匹配。
目前仅支持容器操作系统为 Windows Server 2019 的 Windows 容器。
对于容器的 Hyper-V 隔离、允许一定程度上的 Windows 容器镜像版本向后兼容性等等，
都是将来版本计划的一部分。

<!--
## Getting Help and Troubleshooting {#troubleshooting}

Your main source of help for troubleshooting your Kubernetes cluster should
start with this
[section](/docs/tasks/debug-application-cluster/troubleshooting/). Some
additional, Windows-specific troubleshooting help is included in this section.
Logs are an important element of troubleshooting issues in Kubernetes. Make
sure to include them any time you seek troubleshooting assistance from other
contributors. Follow the instructions in the SIG-Windows
[contributing guide on gathering logs](https://github.com/kubernetes/community/blob/master/sig-windows/CONTRIBUTING.md#gathering-logs).
-->
## 获取帮助和故障排查     {#troubleshooting}

对你的 Kubernetes 集群进行排查的主要帮助信息来源应该是
[这份文档](/docs/tasks/debug-application-cluster/troubleshooting/)。
该文档中包含了一些额外的、特定于 Windows 系统的故障排查帮助信息。
Kubernetes 中日志是故障排查的一个重要元素。确保你在尝试从其他贡献者那里获得
故障排查帮助时提供日志信息。你可以按照 SIG-Windows
[贡献指南和收集日志](https://github.com/kubernetes/community/blob/master/sig-windows/CONTRIBUTING.md#gathering-logs)
所给的指令来操作。

<!--
* How do I know start.ps1 completed successfully?

  You should see kubelet, kube-proxy, and (if you chose Flannel as your
  networking solution) flanneld host-agent processes running on your node, with
  running logs being displayed in separate PowerShell windows. In addition to
  this, your Windows node should be listed as "Ready" in your Kubernetes
  cluster.
-->
* 我怎样知道 `start.ps1` 是否已成功完成？

  你应该能看到节点上运行的 kubelet、kube-proxy 和（如果你选择 Flannel
  作为联网方案）flanneld 宿主代理进程，它们的运行日志显示在不同的
  PowerShell 窗口中。此外，你的 Windows 节点应该在你的 Kubernetes 集群
  列举为 "Ready" 节点。

<!--
* Can I configure the Kubernetes node processes to run in the background as services?

  Kubelet and kube-proxy are already configured to run as native Windows
  Services, offering resiliency by re-starting the services automatically in the
  event of failure (for example a process crash). You have two options for
  configuring these node components as services.
-->
* 我可以将 Kubernetes 节点进程配置为服务运行在后台么？

  kubelet 和 kube-proxy 都已经被配置为以本地 Windows 服务运行，
  并且在出现失效事件（例如进程意外结束）时通过自动重启服务来提供一定的弹性。
  你有两种办法将这些节点组件配置为服务。

  <!--
  * As native Windows Services

    Kubelet & kube-proxy can be run as native Windows Services using `sc.exe`.

    ```powershell
    # Create the services for kubelet and kube-proxy in two separate commands
    sc.exe create <component_name> binPath= "<path_to_binary> -service <other_args>"

    # Please note that if the arguments contain spaces, they must be escaped.
    sc.exe create kubelet binPath= "C:\kubelet.exe --service --hostname-override 'minion' <other_args>"

    # Start the services
    Start-Service kubelet
    Start-Service kube-proxy

    # Stop the service
    Stop-Service kubelet (-Force)
    Stop-Service kube-proxy (-Force)

    # Query the service status
    Get-Service kubelet
    Get-Service kube-proxy
    ```
  -->
  * 以本地 Windows 服务的形式

    Kubelet 和 kube-proxy 可以用 `sc.exe` 以本地 Windows 服务的形式运行：

    ```powershell
    # 用两个单独的命令为 kubelet 和 kube-proxy 创建服务
    sc.exe create <组件名称> binPath="<可执行文件路径> -service <其它参数>"

    # 请注意如果参数中包含空格，必须使用转义
    sc.exe create kubelet binPath= "C:\kubelet.exe --service --hostname-override 'minion' <其它参数>"

    # 启动服务
    Start-Service kubelet
    Start-Service kube-proxy

    # 停止服务
    Stop-Service kubelet (-Force)
    Stop-Service kube-proxy (-Force)

    # 查询服务状态
    Get-Service kubelet
    Get-Service kube-proxy
    ```

  <!--
  * Using nssm.exe

    You can also always use alternative service managers like
    [nssm.exe](https://nssm.cc/) to run these processes (flanneld, kubelet &
    kube-proxy) in the background for you. You can use this [sample
    script](https://github.com/Microsoft/SDN/tree/master/Kubernetes/flannel/register-svc.ps1),
    leveraging `nssm.exe` to register kubelet, kube-proxy, and `flanneld.exe` to run
    as Windows services in the background.
  -->
  * 使用 nssm.exe

    你也总是可以使用替代的服务管理器，例如[nssm.exe](https://nssm.cc/)，来为你在后台运行
    这些进程（`flanneld`、`kubelet` 和 `kube-proxy`）。你可以使用这一
    [示例脚本](https://github.com/Microsoft/SDN/tree/master/Kubernetes/flannel/register-svc.ps1)，
    利用 `nssm.exe` 将 `kubelet`、`kube-proxy` 和 `flanneld.exe` 注册为要在后台运行的
    Windows 服务。

    <!--
    ```powershell
    register-svc.ps1 -NetworkMode <Network mode> -ManagementIP <Windows Node IP> -ClusterCIDR <Cluster subnet> -KubeDnsServiceIP <Kube-dns Service IP> -LogDir <Directory to place logs>
    ```
    -->
    ```powershell
    register-svc.ps1 -NetworkMode <网络模式> -ManagementIP <Windows 节点 IP> -ClusterCIDR <集群子网> -KubeDnsServiceIP <kube-dns 服务 IP> -LogDir <日志目录>
    ```

    <!--
    The parameters are explained below:
    -->
    这里的参数解释如下：

    <!--
    - `NetworkMode`: The network mode l2bridge (flannel host-gw, also the
      default value) or overlay (flannel vxlan) chosen as a network solution
    - `ManagementIP`: The IP address assigned to the Windows node. You can use
      `ipconfig` to find this.
    - `ClusterCIDR`: The cluster subnet range. (Default: 10.244.0.0/16)
    - `KubeDnsServiceIP`: The Kubernetes DNS service IP. (Default: 10.96.0.10)
    - `LogDir`: The directory where kubelet and kube-proxy logs are redirected
      into their respective output files. (Default value C:\k)
    -->
    - `NetworkMode`：网络模式 l2bridge（flannel host-gw，也是默认值）或
      overlay（flannel vxlan）选做网络方案
    - `ManagementIP`：分配给 Windows 节点的 IP 地址。你可以使用 ipconfig 得到此值
    - `ClusterCIDR`：集群子网范围（默认值为 10.244.0.0/16）
    - `KubeDnsServiceIP`：Kubernetes DNS 服务 IP（默认值为 10.96.0.10）
    - `LogDir`：kubelet 和 kube-proxy 的日志会被重定向到这一目录中的对应输出文件，
      默认值为 `C:\k`。

    <!--
    If the above referenced script is not suitable, you can manually configure
    `nssm.exe` using the following examples.

    Register flanneld.exe:
    -->
    若以上所引用的脚本不适合，你可以使用下面的例子手动配置 `nssm.exe`。

    注册 flanneld.exe：

    ```powershell
    nssm install flanneld C:\flannel\flanneld.exe
    nssm set flanneld AppParameters --kubeconfig-file=c:\k\config --iface=<ManagementIP> --ip-masq=1 --kube-subnet-mgr=1
    nssm set flanneld AppEnvironmentExtra NODE_NAME=<hostname>
    nssm set flanneld AppDirectory C:\flannel
    nssm start flanneld
    ```

    <!--
    Register kubelet.exe:
    -->
    注册 kubelet.exe：

    ```powershell
    # Microsoft 在 mcr.microsoft.com/oss/kubernetes/pause:3.4.1
    # 发布其基础设施容器镜像
    nssm install kubelet C:\k\kubelet.exe
    nssm set kubelet AppParameters --hostname-override=<hostname> --v=6 --pod-infra-container-image=mcr.microsoft.com/oss/kubernetes/pause:3.4.1 --resolv-conf="" --allow-privileged=true --enable-debugging-handlers --cluster-dns=<DNS-service-IP> --cluster-domain=cluster.local --kubeconfig=c:\k\config --hairpin-mode=promiscuous-bridge --image-pull-progress-deadline=20m --cgroups-per-qos=false  --log-dir=<log directory> --logtostderr=false --enforce-node-allocatable="" --network-plugin=cni --cni-bin-dir=c:\k\cni --cni-conf-dir=c:\k\cni\config
    nssm set kubelet AppDirectory C:\k
    nssm start kubelet
    ```

    <!--
    Register kube-proxy.exe (l2bridge / host-gw):
    -->
    注册 kube-proxy.exe（二层网桥模式和主机网关模式）

    ```powershell
    nssm install kube-proxy C:\k\kube-proxy.exe
    nssm set kube-proxy AppDirectory c:\k
    nssm set kube-proxy AppParameters --v=4 --proxy-mode=kernelspace --hostname-override=<hostname>--kubeconfig=c:\k\config --enable-dsr=false --log-dir=<log directory> --logtostderr=false
    nssm.exe set kube-proxy AppEnvironmentExtra KUBE_NETWORK=cbr0
    nssm set kube-proxy DependOnService kubelet
    nssm start kube-proxy
    ```

    <!--
    Register kube-proxy.exe (overlay / vxlan):
    -->
    注册 kube-proxy.exe（覆盖网络模式或 VxLAN 模式）

    ```powershell
    nssm install kube-proxy C:\k\kube-proxy.exe
    nssm set kube-proxy AppDirectory c:\k
    nssm set kube-proxy AppParameters --v=4 --proxy-mode=kernelspace --feature-gates="WinOverlay=true" --hostname-override=<hostname> --kubeconfig=c:\k\config --network-name=vxlan0 --source-vip=<source-vip> --enable-dsr=false --log-dir=<log directory> --logtostderr=false
    nssm set kube-proxy DependOnService kubelet
    nssm start kube-proxy
    ```

    <!--
    For initial troubleshooting, you can use the following flags in
    [nssm.exe](https://nssm.cc/) to redirect stdout and stderr to a output file:

    ```powershell
    nssm set <Service Name> AppStdout C:\k\mysvc.log
    nssm set <Service Name> AppStderr C:\k\mysvc.log
    ```

    For additional details, see official [nssm usage](https://nssm.cc/usage) docs.
    -->
    作为初始的故障排查操作，你可以使用在 [nssm.exe](https://nssm.cc/) 中使用下面的标志
    以便将标准输出和标准错误输出重定向到一个输出文件：

    ```powershell
    nssm set <服务名称> AppStdout C:\k\mysvc.log
    nssm set <服务名称> AppStderr C:\k\mysvc.log
    ```

    要了解更多的细节，可参见官方的 [nssm 用法](https://nssm.cc/usage)文档。

<!--
* My Windows Pods do not have network connectivity

  If you are using virtual machines, ensure that MAC spoofing is enabled on
  all the VM network adapter(s).
-->
* 我的 Windows Pods 无发连接网络

  如果你在使用虚拟机，请确保 VM 网络适配器均已开启 MAC 侦听（Spoofing）。

<!--
* My Windows Pods cannot ping external resources

  Windows Pods do not have outbound rules programmed for the ICMP protocol
  today. However, TCP/UDP is supported. When trying to demonstrate connectivity
  to resources outside of the cluster, please substitute `ping <IP>` with
  corresponding `curl <IP>` commands.
-->
* 我的 Windows Pods 无法 ping 外部资源

  Windows Pods 目前没有为 ICMP 协议提供出站规则。不过 TCP/UDP 是支持的。
  尝试与集群外资源连接时，可以将 `ping <IP>` 命令替换为对应的 `curl <IP>` 命令。

  <!--
  If you are still facing problems, most likely your network configuration in
  [cni.conf](https://github.com/Microsoft/SDN/blob/master/Kubernetes/flannel/l2bridge/cni/config/cni.conf)
  deserves some extra attention. You can always edit this static file. The
  configuration update will apply to any newly created Kubernetes resources.
  -->
  如果你还遇到问题，很可能你在
  [cni.conf](https://github.com/Microsoft/SDN/blob/master/Kubernetes/flannel/l2bridge/cni/config/cni.conf)
  中的网络配置值得额外的注意。你总是可以编辑这一静态文件。
  配置的更新会应用到所有新创建的 Kubernetes 资源上。

  <!--
  One of the Kubernetes networking requirements (see
  [Kubernetes network model](/docs/concepts/cluster-administration/networking/))
  is for cluster communication to occur without NAT internally. To honor this
  requirement, there is an
  [ExceptionList](https://github.com/Microsoft/SDN/blob/master/Kubernetes/flannel/l2bridge/cni/config/cni.conf#L20)
  for all the communication where we do not want outbound NAT to occur. However,
  this also means that you need to exclude the external IP you are trying to
  query from the ExceptionList. Only then will the traffic originating from your
  Windows pods be SNAT'ed correctly to receive a response from the outside
  world. In this regard, your ExceptionList in `cni.conf` should look as
  follows:
  -->
  Kubernetes 网络的需求之一（参见
  [Kubernetes 网络模型](/zh/docs/concepts/cluster-administration/networking/)）
  是集群内部无需网络地址转译（NAT）即可实现通信。
  为了符合这一要求，对所有我们不希望出站时发生 NAT 的通信都存在一个
  [ExceptionList](https://github.com/Microsoft/SDN/blob/master/Kubernetes/flannel/l2bridge/cni/config/cni.conf#L20)。
  然而这也意味着你需要将你要查询的外部 IP 从 ExceptionList 中移除。
  只有这时，从你的 Windows Pod 发起的网络请求才会被正确地通过 SNAT 转换以接收到
  来自外部世界的响应。
  就此而言，你在 `cni.conf` 中的 `ExceptionList` 应该看起来像这样：

  <!--
  ```conf
  "ExceptionList": [
       "10.244.0.0/16",  # Cluster subnet
       "10.96.0.0/12",   # Service subnet
       "10.127.130.0/24" # Management (host) subnet
  ]
  ```
  -->
  ```conf
  "ExceptionList": [
      "10.244.0.0/16",  # 集群子网
      "10.96.0.0/12",   # 服务子网
      "10.127.130.0/24" # 管理（主机）子网
  ]
  ```

<!--
* My Windows node cannot access NodePort service

  Local NodePort access from the node itself fails. This is a known
  limitation. NodePort access works from other nodes or external clients.
-->
* 我的 Windows 节点无法访问 NodePort 服务

  从节点自身发起的本地 NodePort 请求会失败。这是一个已知的局限。
  NodePort 服务的访问从其他节点或者外部客户端都可正常进行。

<!--
* vNICs and HNS endpoints of containers are being deleted

  This issue can be caused when the `hostname-override` parameter is not
  passed to
  [kube-proxy](/docs/reference/command-line-tools-reference/kube-proxy/).
  To resolve it, users need to pass the hostname to kube-proxy as follows:
-->
* 容器的 vNICs 和 HNS 端点被删除了

  这一问题可能因为 `hostname-override` 参数未能传递给
  [kube-proxy](/zh/docs/reference/command-line-tools-reference/kube-proxy/)
  而导致。解决这一问题时，用户需要按如下方式将主机名传递给 kube-proxy：

  ```powershell
  C:\k\kube-proxy.exe --hostname-override=$(hostname)
  ```

<!--
* With flannel my nodes are having issues after rejoining a cluster

  Whenever a previously deleted node is being re-joined to the cluster,
  flannelD tries to assign a new pod subnet to the node. Users should remove the
  old pod subnet configuration files in the following paths:
-->
* 使用 Flannel 时，我的节点在重新加入集群时遇到问题

  无论何时，当一个之前被删除的节点被重新添加到集群时，flannelD 都会将为节点分配
  一个新的 Pod 子网。 
  用户需要将将下面路径中的老的 Pod 子网配置文件删除：

  ```powershell
  Remove-Item C:\k\SourceVip.json
  Remove-Item C:\k\SourceVipRequest.json
  ```

<!--
* After launching `start.ps1`, flanneld is stuck in "Waiting for the Network
  to be created"

  There are numerous reports of this
  [issue](https://github.com/coreos/flannel/issues/1066); most likely it is a
  timing issue for when the management IP of the flannel network is set. A
  workaround is to simply relaunch start.ps1 or relaunch it manually as follows:

  ```powershell
  PS C:> [Environment]::SetEnvironmentVariable("NODE_NAME", "<Windows_Worker_Hostname>")
  PS C:> C:\flannel\flanneld.exe --kubeconfig-file=c:\k\config --iface=<Windows_Worker_Node_IP> --ip-masq=1 --kube-subnet-mgr=1
  ```
-->
* 在启动了 `start.ps1` 之后，flanneld 一直停滞在 "Waiting for the Network
  to be created" 状态

  关于这一[问题](https://github.com/coreos/flannel/issues/1066)有很多的报告；
  最可能的一种原因是关于何时设置 Flannel 网络的管理 IP 的时间问题。
  一种解决办法是重新启动 `start.ps1` 或者按如下方式手动重启之：

  ```powershell
  [Environment]::SetEnvironmentVariable("NODE_NAME", "<Windows 工作节点主机名>")
  C:\flannel\flanneld.exe --kubeconfig-file=c:\k\config --iface=<Windows 工作节点 IP> --ip-masq=1 --kube-subnet-mgr=1
  ```

<!--
* My Windows Pods cannot launch because of missing `/run/flannel/subnet.env`

  This indicates that Flannel didn't launch correctly. You can either try to
  restart flanneld.exe or you can copy the files over manually from
  `/run/flannel/subnet.env` on the Kubernetes master to
  `C:\run\flannel\subnet.env` on the Windows worker node and modify the
  `FLANNEL_SUBNET` row to a different number. For example, if node subnet
  10.244.4.1/24 is desired:
-->
* 我的 Windows Pods 无法启动，因为缺少 `/run/flannel/subnet.env` 文件

  这表明 Flannel 网络未能正确启动。你可以尝试重启 flanneld.exe 或者将文件手动地
  从 Kubernetes 主控节点的 `/run/flannel/subnet.env` 路径复制到 Windows 工作
  节点的 `C:\run\flannel\subnet.env` 路径，并将 `FLANNEL_SUBNET` 行改为一个
  不同的数值。例如，如果期望节点子网为 `10.244.4.1/24`：

  ```none
  FLANNEL_NETWORK=10.244.0.0/16
  FLANNEL_SUBNET=10.244.4.1/24
  FLANNEL_MTU=1500
  FLANNEL_IPMASQ=true
  ```
<!--
* My Windows node cannot access my services using the service IP

  This is a known limitation of the current networking stack on Windows.
  Windows Pods are able to access the service IP however.
-->
* 我的 Windows 节点无法使用服务 IP 访问我的服务

  这是 Windows 上当前网络协议栈的一个已知的限制。
  Windows Pods 能够访问服务 IP。

<!--
* No network adapter is found when starting kubelet

  The Windows networking stack needs a virtual adapter for Kubernetes
  networking to work. If the following commands return no results (in an admin
  shell), virtual network creation — a necessary prerequisite for Kubelet to
  work — has failed:
-->
* 启动 kubelet 时找不到网络适配器

  Windows 网络堆栈需要一个虚拟的适配器，这样 Kubernetes 网络才能工作。
  如果下面的命令（在管理员 Shell 中）没有任何返回结果，证明虚拟网络创建
  （kubelet 正常工作的必要前提之一）失败了：

  ```powershell
  Get-HnsNetwork | ? Name -ieq "cbr0"
  Get-NetAdapter | ? Name -Like "vEthernet (Ethernet*"
  ```

  <!--
  Often it is worthwhile to modify the
  [InterfaceName](https://github.com/microsoft/SDN/blob/master/Kubernetes/flannel/start.ps1#L7)
  parameter of the start.ps1 script, in cases where the host's network adapter
  isn't "Ethernet". Otherwise, consult the output of the `start-kubelet.ps1`
  script to see if there are errors during virtual network creation.
  -->
  当宿主系统的网络适配器名称不是 "Ethernet" 时，通常值得更改 `start.ps1` 脚本中的
  [InterfaceName](https://github.com/microsoft/SDN/blob/master/Kubernetes/flannel/start.ps1#L7)
  参数来重试。否则可以查验 `start-kubelet.ps1` 的输出，看看是否在虚拟网络创建
  过程中报告了其他错误。

<!--
* My Pods are stuck at "Container Creating" or restarting over and over

  Check that your pause image is compatible with your OS version. The
  [instructions](https://docs.microsoft.com/en-us/virtualization/windowscontainers/kubernetes/deploying-resources)
  assume that both the OS and the containers are version 1803. If you have a
  later version of Windows, such as an Insider build, you need to adjust the
  images accordingly. Please refer to the Microsoft's [Docker
  repository](https://hub.docker.com/u/microsoft/) for images. Regardless, both
  the pause image Dockerfile and the sample service expect the image to be
  tagged as :latest.
-->
* 我的 Pods 停滞在 "Container Creating" 状态或者反复重启

  检查你的 pause 镜像是与你的 OS 版本兼容的。
  [这里的指令](https://docs.microsoft.com/en-us/virtualization/windowscontainers/kubernetes/deploying-resources)
  假定你的 OS 和容器版本都是 1803。如果你安装的是更新版本的 Windows，比如说
  某个 Insider 构造版本，你需要相应地调整要使用的镜像。
  请参照 Microsoft 的 [Docker 仓库](https://hub.docker.com/u/microsoft/)
  了解镜像。不管怎样，pause 镜像的 Dockerfile 和示例服务都期望镜像的标签
  为 `:latest`。

<!--
* DNS resolution is not properly working

  Check the DNS limitations for Windows in this [section](#dns-limitations).
-->
* DNS 解析无法正常工作

  参阅 Windows 上 [DNS 相关的局限](#dns-limitations) 节。

<!--
* `kubectl port-forward` fails with "unable to do port forwarding: wincat not found"

  This was implemented in Kubernetes 1.15 by including wincat.exe in the pause
  infrastructure container `mcr.microsoft.com/oss/kubernetes/pause:3.4.1`. Be
  sure to use these versions or newer ones. If you would like to build your
  own pause infrastructure container, be sure to include
  [wincat](https://github.com/kubernetes-sigs/sig-windows-tools/tree/master/cmd/wincat).
-->
* `kubectl port-forward` 失败，错误信息为 "unable to do port forwarding: wincat not found"

  此功能是在 Kubernetes v1.15 中实现的，pause 基础设施容器
  `mcr.microsoft.com/oss/kubernetes/pause:3.4.1` 中包含了 wincat.exe。
  请确保你使用的是这些版本或者更新版本。
  如果你想要自行构造你自己的 pause 基础设施容器，要确保其中包含了
  [wincat](https://github.com/kubernetes-sigs/sig-windows-tools/tree/master/cmd/wincat)

<!--
* My Kubernetes installation is failing because my Windows Server node is
  behind a proxy

  If you are behind a proxy, the following PowerShell environment variables must be defined:
-->
* 我的 Kubernetes 安装失败，因为我的 Windows Server 节点在防火墙后面

  如果你处于防火墙之后，那么必须定义如下 PowerShell 环境变量：

  ```PowerShell
  [Environment]::SetEnvironmentVariable("HTTP_PROXY", "http://proxy.example.com:80/", [EnvironmentVariableTarget]::Machine)
  [Environment]::SetEnvironmentVariable("HTTPS_PROXY", "http://proxy.example.com:443/", [EnvironmentVariableTarget]::Machine)
  ```

<!--
* What is a `pause` container?

  In a Kubernetes Pod, an infrastructure or "pause" container is first created
  to host the container endpoint. Containers that belong to the same pod,
  including infrastructure and worker containers, share a common network
  namespace and endpoint (same IP and port space). Pause containers are needed
  to accommodate worker containers crashing or restarting without losing any of
  the networking configuration.

  The "pause" (infrastructure) image is hosted on Microsoft Container Registry
  (MCR). You can access it using `mcr.microsoft.com/oss/kubernetes/pause:3.4.1`.
  For more details, see the
  [DOCKERFILE](https://github.com/kubernetes-sigs/sig-windows-tools/tree/master/cmd/wincat).
-->
* `pause` 容器是什么？

  在一个 Kubernetes Pod 中，一个基础设施容器，或称 "pause" 容器，会被首先创建出来，
  用以托管容器端点。属于同一 Pod 的容器，包括基础设施容器和工作容器，会共享相同的
  网络名字空间和端点（相同的 IP 和端口空间）。我们需要 pause 容器来工作容器崩溃或
  重启的状况，以确保不会丢失任何网络配置。

  "pause" （基础设施）镜像托管在 Microsoft Container Registry (MCR) 上。
  你可以使用 `mcr.microsoft.com/oss/kubernetes/pause:3.4.1` 来访问它。
  要了解进一步的细节，可参阅
  [DOCKERFILE](https://github.com/kubernetes-sigs/sig-windows-tools/tree/master/cmd/wincat)。

<!--
### Further investigation

If these steps don't resolve your problem, you can get help running Windows
containers on Windows nodes in Kubernetes through:

* StackOverflow [Windows Server Container](https://stackoverflow.com/questions/tagged/windows-server-container) topic

* Kubernetes Official Forum [discuss.kubernetes.io](https://discuss.kubernetes.io/)

* Kubernetes Slack [#SIG-Windows Channel](https://kubernetes.slack.com/messages/sig-windows)
-->
### 进一步探究    {#further-investigation}

如果以上步骤未能解决你遇到的问题，你可以通过以下方式获得在 Kubernetes 
中的 Windows 节点上运行 Windows 容器的帮助：

* StackOverflow [Windows Server Container](https://stackoverflow.com/questions/tagged/windows-server-container) 主题
* Kubernetes 官方论坛 [discuss.kubernetes.io](https://discuss.kubernetes.io/)
* Kubernetes Slack [#SIG-Windows 频道](https://kubernetes.slack.com/messages/sig-windows)

<!--
## Reporting Issues and Feature Requests

If you have what looks like a bug, or you would like to make a feature
request, please use the
[GitHub issue tracking system](https://github.com/kubernetes/kubernetes/issues).
You can open issues on
[GitHub](https://github.com/kubernetes/kubernetes/issues/new/choose) and
assign them to SIG-Windows. You should first search the list of issues in case
it was reported previously and comment with your experience on the issue and
add additional logs. SIG-Windows Slack is also a great avenue to get some
initial support and troubleshooting ideas prior to creating a ticket.
-->
## 报告问题和功能需求  {#reporting-issues-and-feature-requests}

如果你遇到看起来像是软件缺陷的问题，或者你想要提起某种功能需求，请使用
[GitHub 问题跟踪系统](https://github.com/kubernetes/kubernetes/issues)。
你可以在 [GitHub](https://github.com/kubernetes/kubernetes/issues/new/choose)
上发起 Issue 并将其指派给 SIG-Windows。你应该首先搜索 Issue 列表，看看是否
该 Issue 以前曾经被报告过，以评论形式将你在该 Issue 上的体验追加进去，并附上
额外的日志信息。SIG-Windows Slack 频道也是一个获得初步支持的好渠道，可以在
生成新的 Ticket 之前对一些想法进行故障分析。

<!--
If filing a bug, please include detailed information about how to reproduce
the problem, such as:

* Kubernetes version: kubectl version
* Environment details: Cloud provider, OS distro, networking choice and
  configuration, and Docker version
* Detailed steps to reproduce the problem
* [Relevant logs](https://github.com/kubernetes/community/blob/master/sig-windows/CONTRIBUTING.md#gathering-logs)
* Tag the issue sig/windows by commenting on the issue with `/sig windows` to
  bring it to a SIG-Windows member's attention
-->
在登记软件缺陷时，请给出如何重现该问题的详细信息，例如：

* Kubernetes 版本：kubectl 版本
* 环境细节：云平台、OS 版本、网络选型和配置情况以及 Docker 版本
* 重现该问题的详细步骤
* [相关的日志](https://github.com/kubernetes/community/blob/master/sig-windows/CONTRIBUTING.md#gathering-logs)
* 通过为该 Issue 添加 `/sig windows` 评论为其添加 `sig/windows` 标签，
  进而引起 SIG-Windows 成员的注意。

## {{% heading "whatsnext" %}}

<!--
We have a lot of features in our roadmap. An abbreviated high level list is
included below, but we encourage you to view our
[roadmap project](https://github.com/orgs/kubernetes/projects/8) and help us make
Windows support better by
[contributing](https://github.com/kubernetes/community/blob/master/sig-windows/).
-->
在我们的未来蓝图中包含很多功能特性（要实现）。下面是一个浓缩的简要列表，不过我们
鼓励你查看我们的 [roadmap 项目](https://github.com/orgs/kubernetes/projects/8)并
通过[贡献](https://github.com/kubernetes/community/blob/master/sig-windows/)的方式
帮助我们把 Windows 支持做得更好。

<!--
### Hyper-V isolation

Hyper-V isolation is requried to enable the following use cases for Windows
containers in Kubernetes:

* Hypervisor-based isolation between pods for additional security

* Backwards compatibility allowing a node to run a newer Windows Server
  version without requiring containers to be rebuilt

* Specific CPU/NUMA settings for a pod

* Memory isolation and reservations
-->
### Hyper-V 隔离  {#hyper-v-isolation}

要满足 Kubernetes 中 Windows 容器的如下用例，需要利用 Hyper-V 隔离：

* 在 Pod 之间实施基于监管程序（Hypervisor）的隔离，以增强安全性
* 出于向后兼容需要，允许添加运行新 Windows Server 版本的节点时不必
  重新创建容器
* 为 Pod 设置特定的 CPU/NUMA 配置
* 实施内存隔离与预留

<!--
### Deployment with kubeadm and cluster API

Kubeadm is becoming the de facto standard for users to deploy a Kubernetes
cluster. Windows node support in kubeadm is currently a work-in-progress but a
guide is available
[here](/docs/tasks/administer-cluster/kubeadm/adding-windows-nodes/). We are
also making investments in cluster API to ensure Windows nodes are properly
provisioned.
-->
### 使用 kubeadm 和 Cluster API 来部署  {#deployment-with-kubeadm-and-cluster-api}

kubeadm 已经成为用户部署 Kubernetes 集群的事实标准。
kubeadm 对 Windows 节点的支持目前还在开发过程中，不过你可以阅读相关的
[指南](/zh/docs/tasks/administer-cluster/kubeadm/adding-windows-nodes/)。
我们也在投入资源到 Cluster API，以确保 Windows 节点被正确配置。

