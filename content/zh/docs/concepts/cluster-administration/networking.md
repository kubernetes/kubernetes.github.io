---
reviewers:
- thockin
title: 集群网络系统
content_type: concept
weight: 50
---

<!-- overview -->
<!--
Networking is a central part of Kubernetes, but it can be challenging to
understand exactly how it is expected to work.  There are 4 distinct networking
problems to address:

1. Highly-coupled container-to-container communications: this is solved by
   {{< glossary_tooltip text="Pods" term_id="pod" >}} and `localhost` communications.
2. Pod-to-Pod communications: this is the primary focus of this document.
3. Pod-to-Service communications: this is covered by [services](/docs/concepts/services-networking/service/).
4. External-to-Service communications: this is covered by [services](/docs/concepts/services-networking/service/).
-->
集群网络系统是 Kubernetes 的核心部分，但是想要准确了解它的工作原理可是个不小的挑战。
下面列出的是网络系统的的四个主要问题：

1. 高度耦合的容器间通信：这个已经被 {{< glossary_tooltip text="Pods" term_id="pod" >}}
   和 `localhost` 通信解决了。
2. Pod 间通信：这个是本文档的重点要讲述的。
3. Pod 和服务间通信：这个已经在[服务](/zh/docs/concepts/services-networking/service/)里讲述过了。
4. 外部和服务间通信：这也已经在[服务](/zh/docs/concepts/services-networking/service/)讲述过了。

<!-- body -->

<!--
Kubernetes is all about sharing machines between applications.  Typically,
sharing machines requires ensuring that two applications do not try to use the
same ports.  Coordinating ports across multiple developers is very difficult to
do at scale and exposes users to cluster-level issues outside of their control.

Dynamic port allocation brings a lot of complications to the system - every
application has to take ports as flags, the API servers have to know how to
insert dynamic port numbers into configuration blocks, services have to know
how to find each other, etc.  Rather than deal with this, Kubernetes takes a
different approach.
-->
Kubernetes 的宗旨就是在应用之间共享机器。
通常来说，共享机器需要两个应用之间不能使用相同的端口，但是在多个应用开发者之间
去大规模地协调端口是件很困难的事情，尤其是还要让用户暴露在他们控制范围之外的集群级别的问题上。

动态分配端口也会给系统带来很多复杂度 - 每个应用都需要设置一个端口的参数，
而 API 服务器还需要知道如何将动态端口数值插入到配置模块中，服务也需要知道如何找到对方等等。
与其去解决这些问题，Kubernetes 选择了其他不同的方法。

<!--
## The Kubernetes network model

Every `Pod` gets its own IP address. This means you do not need to explicitly
create links between `Pods` and you almost never need to deal with mapping
container ports to host ports.  This creates a clean, backwards-compatible
model where `Pods` can be treated much like VMs or physical hosts from the
perspectives of port allocation, naming, service discovery, load balancing,
application configuration, and migration.

Kubernetes imposes the following fundamental requirements on any networking
implementation (barring any intentional network segmentation policies):

   * pods on a node can communicate with all pods on all nodes without NAT
   * agents on a node (e.g. system daemons, kubelet) can communicate with all
     pods on that node

Note: For those platforms that support `Pods` running in the host network (e.g.
Linux):

   * pods in the host network of a node can communicate with all pods on all
     nodes without NAT
-->
## Kubernetes 网络模型   {#the-kubernetes-network-model}

每一个 `Pod` 都有它自己的IP地址，这就意味着你不需要显式地在每个 `Pod` 之间创建链接，
你几乎不需要处理容器端口到主机端口之间的映射。
这将创建一个干净的、向后兼容的模型，在这个模型里，从端口分配、命名、服务发现、
负载均衡、应用配置和迁移的角度来看，`Pod` 可以被视作虚拟机或者物理主机。

Kubernetes 对所有网络设施的实施，都需要满足以下的基本要求（除非有设置一些特定的网络分段策略）：

* 节点上的 Pod 可以不通过 NAT 和其他任何节点上的 Pod 通信
* 节点上的代理（比如：系统守护进程、kubelet）可以和节点上的所有Pod通信

备注：仅针对那些支持 `Pods` 在主机网络中运行的平台（比如：Linux）：

* 那些运行在节点的主机网络里的 Pod 可以不通过 NAT 和所有节点上的 Pod 通信

<!--
This model is not only less complex overall, but it is principally compatible
with the desire for Kubernetes to enable low-friction porting of apps from VMs
to containers.  If your job previously ran in a VM, your VM had an IP and could
talk to other VMs in your project.  This is the same basic model.

Kubernetes IP addresses exist at the `Pod` scope - containers within a `Pod`
share their network namespaces - including their IP address and MAC address.
This means that containers within a `Pod` can all reach each other's ports on
`localhost`. This also means that containers within a `Pod` must coordinate port
usage, but this is no different from processes in a VM.  This is called the
-->
这个模型不仅不复杂，而且还和 Kubernetes 的实现廉价的从虚拟机向容器迁移的初衷相兼容，
如果你的工作开始是在虚拟机中运行的，你的虚拟机有一个 IP ，
这样就可以和其他的虚拟机进行通信，这是基本相同的模型。

Kubernetes 的 IP 地址存在于 `Pod` 范围内 - 容器共享它们的网络命名空间 - 包括它们的 IP 地址和 MAC 地址。
这就意味着 `Pod` 内的容器都可以通过 `localhost` 到达各个端口。
这也意味着 `Pod` 内的容器都需要相互协调端口的使用，但是这和虚拟机中的进程似乎没有什么不同，
这也被称为“一个 Pod 一个 IP”模型。

<!--
How this is implemented is a detail of the particular container runtime in use.

It is possible to request ports on the `Node` itself which forward to your `Pod`
(called host ports), but this is a very niche operation. How that forwarding is
implemented is also a detail of the container runtime. The `Pod` itself is
blind to the existence or non-existence of host ports.
-->
如何实现这一点是正在使用的容器运行时的特定信息。

也可以在 `node` 本身通过端口去请求你的 `Pod`（称之为主机端口），
但这是一个很特殊的操作。转发方式如何实现也是容器运行时的细节。
`Pod` 自己并不知道这些主机端口是否存在。

<!--
## How to implement the Kubernetes networking model

There are a number of ways that this network model can be implemented.  This
document is not an exhaustive study of the various methods, but hopefully serves
as an introduction to various technologies and serves as a jumping-off point.

The following networking options are sorted alphabetically - the order does not
imply any preferential status.
-->
## 如何实现 Kubernetes 的网络模型

有很多种方式可以实现这种网络模型，本文档并不是对各种实现技术的详细研究，
但是希望可以作为对各种技术的详细介绍，并且成为你研究的起点。

接下来的网络技术是按照首字母排序，顺序本身并无其他意义。

{{% thirdparty-content %}}

<!--
### ACI

[Cisco Application Centric Infrastructure](https://www.cisco.com/c/en/us/solutions/data-center-virtualization/application-centric-infrastructure/index.html) offers an integrated overlay and underlay SDN solution that supports containers, virtual machines, and bare metal servers. [ACI](https://www.github.com/noironetworks/aci-containers) provides container networking integration for ACI. An overview of the integration is provided [here](https://www.cisco.com/c/dam/en/us/solutions/collateral/data-center-virtualization/application-centric-infrastructure/solution-overview-c22-739493.pdf).
-->
### ACI
[Cisco Application Centric Infrastructure](https://www.cisco.com/c/en/us/solutions/data-center-virtualization/application-centric-infrastructure/index.html)
提供了一个集成覆盖网络和底层 SDN 的解决方案来支持容器、虚拟机和其他裸机服务器。
[ACI](https://www.github.com/noironetworks/aci-containers) 为 ACI 提供了容器网络集成。
点击[这里](https://www.cisco.com/c/dam/en/us/solutions/collateral/data-center-virtualization/application-centric-infrastructure/solution-overview-c22-739493.pdf)查看概述。

<!--
### Antrea

Project [Antrea](https://github.com/vmware-tanzu/antrea) is an opensource Kubernetes networking solution intended to be Kubernetes native. It leverages Open vSwitch as the networking data plane. Open vSwitch is a high-performance programmable virtual switch that supports both Linux and Windows. Open vSwitch enables Antrea to implement Kubernetes Network Policies in a high-performance and efficient manner.
Thanks to the "programmable" characteristic of Open vSwitch, Antrea is able to implement an extensive set of networking and security features and services on top of Open vSwitch.
-->
### Antrea

[Antrea](https://github.com/vmware-tanzu/antrea) 项目是一个开源的联网解决方案，旨在成为
Kubernetes 原生的网络解决方案。它利用 Open vSwitch 作为网络数据平面。
Open vSwitch 是一个高性能可编程的虚拟交换机，支持 Linux 和 Windows 平台。
Open vSwitch 使 Antrea 能够以高性能和高效的方式实现 Kubernetes 的网络策略。
借助 Open vSwitch 可编程的特性，Antrea 能够在 Open vSwitch 之上实现广泛的联网、安全功能和服务。

<!--
### AOS from Apstra

[AOS](https://www.apstra.com/products/aos/) is an Intent-Based Networking system that creates and manages complex datacenter environments from a simple integrated platform.  AOS leverages a highly scalable distributed design to eliminate network outages while minimizing costs.

The AOS Reference Design currently supports Layer-3 connected hosts that eliminate legacy Layer-2 switching problems.  These Layer-3 hosts can be Linux servers (Debian, Ubuntu, CentOS) that create BGP neighbor relationships directly with the top of rack switches (TORs).  AOS automates the routing adjacencies and then provides fine grained control over the route health injections (RHI) that are common in a Kubernetes deployment.

AOS has a rich set of REST API endpoints that enable Kubernetes to quickly change the network policy based on application requirements.  Further enhancements will integrate the AOS Graph model used for the network design with the workload provisioning, enabling an end to end management system for both private and public clouds.

AOS supports the use of common vendor equipment from manufacturers including Cisco, Arista, Dell, Mellanox, HPE, and a large number of white-box systems and open network operating systems like Microsoft SONiC, Dell OPX, and Cumulus Linux.

Details on how the AOS system works can be accessed here: https://www.apstra.com/products/how-it-works/
-->
### Apstra 的 AOS 

[AOS](https://www.apstra.com/products/aos/) 是一个基于意图的网络系统，
可以通过一个简单的集成平台创建和管理复杂的数据中心环境。
AOS 利用高度可扩展的分布式设计来消除网络中断，同时将成本降至最低。

AOS 参考设计当前支持三层连接的主机，这些主机消除了旧的两层连接的交换问题。
这些三层连接的主机可以是 Linux（Debian、Ubuntu、CentOS）系统，
它们直接在机架式交换机（TOR）的顶部创建 BGP 邻居关系。
AOS 自动执行路由邻接，然后提供对 Kubernetes 部署中常见的路由运行状况注入（RHI）的精细控制。

AOS 具有一组丰富的 REST API 端点，这些端点使 Kubernetes 能够根据应用程序需求快速更改网络策略。
进一步的增强功能将用于网络设计的 AOS Graph 模型与工作负载供应集成在一起，
从而为私有云和公共云提供端到端管理系统。

AOS 支持使用包括 Cisco、Arista、Dell、Mellanox、HPE 在内的制造商提供的通用供应商设备，
以及大量白盒系统和开放网络操作系统，例如 Microsoft SONiC、Dell OPX 和 Cumulus Linux。

想要更详细地了解 AOS 系统是如何工作的可以点击这里：https://www.apstra.com/products/how-it-works/

<!--
### AWS VPC CNI for Kubernetes

The [AWS VPC CNI](https://github.com/aws/amazon-vpc-cni-k8s) offers integrated AWS Virtual Private Cloud (VPC) networking for Kubernetes clusters. This CNI plugin offers high throughput and availability, low latency, and minimal network jitter. Additionally, users can apply existing AWS VPC networking and security best practices for building Kubernetes clusters. This includes the ability to use VPC flow logs, VPC routing policies, and security groups for network traffic isolation.

Using this CNI plugin allows Kubernetes pods to have the same IP address inside the pod as they do on the VPC network. The CNI allocates AWS Elastic Networking Interfaces (ENIs) to each Kubernetes node and using the secondary IP range from each ENI for pods on the node. The CNI includes controls for pre-allocation of ENIs and IP addresses for fast pod startup times and enables large clusters of up to 2,000 nodes.

Additionally, the CNI can be run alongside [Calico for network policy enforcement](https://docs.aws.amazon.com/eks/latest/userguide/calico.html). The AWS VPC CNI project is open source with [documentation on GitHub](https://github.com/aws/amazon-vpc-cni-k8s).
-->
### Kubernetes 的 AWS VPC CNI 

[AWS VPC CNI](https://github.com/aws/amazon-vpc-cni-k8s) 为 Kubernetes 集群提供了集成的
AWS 虚拟私有云（VPC）网络。该 CNI 插件提供了高吞吐量和可用性，低延迟以及最小的网络抖动。
此外，用户可以使用现有的 AWS VPC 网络和安全最佳实践来构建 Kubernetes 集群。
这包括使用 VPC 流日志、VPC 路由策略和安全组进行网络流量隔离的功能。

使用该 CNI 插件，可使 Kubernetes Pod 拥有与在 VPC 网络上相同的 IP 地址。
CNI 将 AWS 弹性网络接口（ENI）分配给每个 Kubernetes 节点，并将每个 ENI 的辅助 IP 范围用于该节点上的 Pod 。
CNI 包含用于 ENI 和 IP 地址的预分配的控件，以便加快 Pod 的启动时间，并且能够支持多达 2000 个节点的大型集群。

此外，CNI 可以与
[用于执行网络策略的 Calico](https://docs.aws.amazon.com/eks/latest/userguide/calico.html) 一起运行。
AWS VPC CNI 项目是开源的，请查看 [GitHub 上的文档](https://github.com/aws/amazon-vpc-cni-k8s)。

<!--
### Azure CNI for Kubernetes 
[Azure CNI](https://docs.microsoft.com/en-us/azure/virtual-network/container-networking-overview) is an [open source](https://github.com/Azure/azure-container-networking/blob/master/docs/cni.md) plugin that integrates Kubernetes Pods with an Azure Virtual Network (also known as VNet) providing network performance at par with VMs. Pods can connect to peered VNet and to on-premises over Express Route or site-to-site VPN and are also directly reachable from these networks. Pods can access Azure services, such as storage and SQL, that are protected by Service Endpoints or Private Link. You can use VNet security policies and routing to filter Pod traffic. The plugin assigns VNet IPs to Pods by utilizing a pool of secondary IPs pre-configured on the Network Interface of a Kubernetes node.

Azure CNI is available natively in the [Azure Kubernetes Service (AKS)](https://docs.microsoft.com/en-us/azure/aks/configure-azure-cni).
-->
### Kubernetes 的 Azure CNI 

[Azure CNI](https://docs.microsoft.com/en-us/azure/virtual-network/container-networking-overview)
是一个[开源插件](https://github.com/Azure/azure-container-networking/blob/master/docs/cni.md)，
将 Kubernetes Pods 和 Azure 虚拟网络（也称为 VNet）集成在一起，可提供与 VM 相当的网络性能。
Pod 可以通过 Express Route 或者 站点到站点的 VPN 来连接到对等的 VNet ，
也可以从这些网络来直接访问 Pod。Pod 可以访问受服务端点或者受保护链接的 Azure 服务，比如存储和 SQL。
你可以使用 VNet 安全策略和路由来筛选 Pod 流量。
该插件通过利用在 Kubernetes 节点的网络接口上预分配的辅助 IP 池将 VNet 分配给 Pod 。

Azure CNI 可以在
[Azure Kubernetes Service (AKS)](https://docs.microsoft.com/en-us/azure/aks/configure-azure-cni) 中获得。

<!--
### Big Cloud Fabric from Big Switch Networks

[Big Cloud Fabric](https://www.bigswitch.com/container-network-automation) is a cloud native networking architecture, designed to run Kubernetes in private cloud/on-premises environments. Using unified physical & virtual SDN, Big Cloud Fabric tackles inherent container networking problems such as load balancing, visibility, troubleshooting, security policies & container traffic monitoring.

With the help of the Big Cloud Fabric's virtual pod multi-tenant architecture, container orchestration systems such as Kubernetes, RedHat OpenShift, Mesosphere DC/OS & Docker Swarm will be natively integrated alongside with VM orchestration systems such as VMware, OpenStack & Nutanix. Customers will be able to securely inter-connect any number of these clusters and enable inter-tenant communication between them if needed.

BCF was recognized by Gartner as a visionary in the latest [Magic Quadrant](https://go.bigswitch.com/17GatedDocuments-MagicQuadrantforDataCenterNetworking_Reg.html). One of the BCF Kubernetes on-premises deployments (which includes Kubernetes, DC/OS & VMware running on multiple DCs across different geographic regions) is also referenced [here](https://portworx.com/architects-corner-kubernetes-satya-komala-nio/).
-->
### Big Switch Networks 的 Big Cloud Fabric

[Big Cloud Fabric](https://www.bigswitch.com/container-network-automation) 是一个基于云原生的网络架构，
旨在在私有云或者本地环境中运行 Kubernetes。
它使用统一的物理和虚拟 SDN，Big Cloud Fabric 解决了固有的容器网络问题，
比如负载均衡、可见性、故障排除、安全策略和容器流量监控。

在 Big Cloud Fabric 的虚拟 Pod 多租户架构的帮助下，容器编排系统
（比如 Kubernetes、RedHat OpenShift、Mesosphere DC/OS 和 Docker Swarm）
将与 VM 本地编排系统（比如 VMware、OpenStack 和 Nutanix）进行本地集成。
客户将能够安全地互联任意数量的这些集群，并且在需要时启用他们之间的租户间通信。

在最新的 [Magic Quadrant](https://go.bigswitch.com/17GatedDocuments-MagicQuadrantforDataCenterNetworking_Reg.html) 上，
BCF 被 Gartner 认为是非常有远见的。
而 BCF 的一条关于 Kubernetes 的本地部署（其中包括 Kubernetes、DC/OS 和在不同地理区域的多个
DC 上运行的 VMware）也在[这里](https://portworx.com/architects-corner-kubernetes-satya-komala-nio/)被引用。

<!--
### Calico

[Calico](https://docs.projectcalico.org/) is an open source networking and network security solution for containers, virtual machines, and native host-based workloads. Calico supports multiple data planes including: a pure Linux eBPF dataplane, a standard Linux networking dataplane, and a Windows HNS dataplane. Calico provides a full networking stack but can also be used in conjunction with [cloud provider CNIs](https://docs.projectcalico.org/networking/determine-best-networking#calico-compatible-cni-plugins-and-cloud-provider-integrations) to provide network policy enforcement.
-->
### Calico

[Calico](https://docs.projectcalico.org/) 是一个开源的联网及网络安全方案，
用于基于容器、虚拟机和本地主机的工作负载。
Calico 支持多个数据面，包括：纯 Linux eBPF 的数据面、标准的 Linux 联网数据面
以及 Windows HNS 数据面。Calico 在提供完整的联网堆栈的同时，还可与
[云驱动 CNIs](https://docs.projectcalico.org/networking/determine-best-networking#calico-compatible-cni-plugins-and-cloud-provider-integrations) 联合使用，以保证网络策略实施。

<!--
### Cilium

[Cilium](https://github.com/cilium/cilium) is open source software for
providing and transparently securing network connectivity between application
containers. Cilium is L7/HTTP aware and can enforce network policies on L3-L7
using an identity based security model that is decoupled from network
addressing, and it can be used in combination with other CNI plugins.
-->
### Cilium

[Cilium](https://github.com/cilium/cilium) 是一个开源软件，用于提供并透明保护应用容器间的网络连接。
Cilium 支持 L7/HTTP，可以在 L3-L7 上通过使用与网络分离的基于身份的安全模型寻址来实施网络策略，
并且可以与其他 CNI 插件结合使用。

<!--
### CNI-Genie from Huawei

[CNI-Genie](https://github.com/Huawei-PaaS/CNI-Genie) is a CNI plugin that enables Kubernetes to [simultaneously have access to different implementations](https://github.com/Huawei-PaaS/CNI-Genie/blob/master/docs/multiple-cni-plugins/README.md#what-cni-genie-feature-1-multiple-cni-plugins-enables) of the [Kubernetes network model](https://github.com/kubernetes/website/blob/master/content/en/docs/concepts/cluster-administration/networking.md#the-kubernetes-network-model) in runtime. This includes any implementation that runs as a [CNI plugin](https://github.com/containernetworking/cni#3rd-party-plugins), such as [Flannel](https://github.com/coreos/flannel#flannel), [Calico](https://docs.projectcalico.org/), [Romana](https://romana.io), [Weave-net](https://www.weave.works/products/weave-net/).

CNI-Genie also supports [assigning multiple IP addresses to a pod](https://github.com/Huawei-PaaS/CNI-Genie/blob/master/docs/multiple-ips/README.md#feature-2-extension-cni-genie-multiple-ip-addresses-per-pod), each from a different CNI plugin.
-->
### 华为的 CNI-Genie

[CNI-Genie](https://github.com/Huawei-PaaS/CNI-Genie) 是一个 CNI 插件，
可以让 Kubernetes 在运行时使用不同的[网络模型](#the-kubernetes-network-model)的
[实现同时被访问](https://github.com/Huawei-PaaS/CNI-Genie/blob/master/docs/multiple-cni-plugins/README.md#what-cni-genie-feature-1-multiple-cni-plugins-enables)。
这包括以
[CNI 插件](https://github.com/containernetworking/cni#3rd-party-plugins)运行的任何实现，比如
[Flannel](https://github.com/coreos/flannel#flannel)、
[Calico](https://docs.projectcalico.org/)、
[Romana](https://romana.io)、
[Weave-net](https://www.weave.works/products/weave-net/)。

CNI-Genie 还支持[将多个 IP 地址分配给 Pod](https://github.com/Huawei-PaaS/CNI-Genie/blob/master/docs/multiple-ips/README.md#feature-2-extension-cni-genie-multi-ip-addresses-per-pod)，
每个都来自不同的 CNI 插件。

<!--
### cni-ipvlan-vpc-k8s
[cni-ipvlan-vpc-k8s](https://github.com/lyft/cni-ipvlan-vpc-k8s) contains a set
of CNI and IPAM plugins to provide a simple, host-local, low latency, high
throughput, and compliant networking stack for Kubernetes within Amazon Virtual
Private Cloud (VPC) environments by making use of Amazon Elastic Network
Interfaces (ENI) and binding AWS-managed IPs into Pods using the Linux kernel's
IPvlan driver in L2 mode.

The plugins are designed to be straightforward to configure and deploy within a
VPC. Kubelets boot and then self-configure and scale their IP usage as needed
without requiring the often recommended complexities of administering overlay
networks, BGP, disabling source/destination checks, or adjusting VPC route
tables to provide per-instance subnets to each host (which is limited to 50-100
entries per VPC). In short, cni-ipvlan-vpc-k8s significantly reduces the
network complexity required to deploy Kubernetes at scale within AWS.
-->
### cni-ipvlan-vpc-k8s

[cni-ipvlan-vpc-k8s](https://github.com/lyft/cni-ipvlan-vpc-k8s)
包含了一组 CNI 和 IPAM 插件来提供一个简单的、本地主机、低延迟、高吞吐量
以及通过使用 Amazon 弹性网络接口（ENI）并使用 Linux 内核的 IPv2 驱动程序
以 L2 模式将 AWS 管理的 IP 绑定到 Pod 中，
在 Amazon Virtual Private Cloud（VPC）环境中为 Kubernetes 兼容的网络堆栈。

这些插件旨在直接在 VPC 中进行配置和部署，Kubelets 先启动，
然后根据需要进行自我配置和扩展它们的 IP 使用率，而无需经常建议复杂的管理
覆盖网络、BGP、禁用源/目标检查或调整 VPC 路由表以向每个主机提供每个实例子网的
复杂性（每个 VPC 限制为50-100个条目）。
简而言之，cni-ipvlan-vpc-k8s 大大降低了在 AWS 中大规模部署 Kubernetes 所需的网络复杂性。

<!--
### Coil

[Coil](https://github.com/cybozu-go/coil) is a CNI plugin designed for ease of integration, providing flexible egress networking.
Coil operates with a low overhead compared to bare metal, and allows you to define arbitrary egress NAT gateways for external networks.

-->
### Coil

[Coil](https://github.com/cybozu-go/coil) 是一个为易于集成、提供灵活的出站流量网络而设计的 CNI 插件。
与裸机相比，Coil 的额外操作开销低，并允许针对外部网络的出站流量任意定义 NAT 网关。

<!--
### Contiv

[Contiv](https://github.com/contiv/netplugin) provides configurable networking (native l3 using BGP, overlay using vxlan,  classic l2, or Cisco-SDN/ACI) for various use cases. [Contiv](https://contiv.io) is all open sourced.
-->
### Contiv

[Contiv](https://github.com/contiv/netplugin)
为各种使用情况提供了一个可配置网络（使用了 BGP 的本地 L3，
使用 vxlan 、经典 L2 或 Cisco-SDN/ACI 的覆盖网络）。
[Contiv](https://contiv.io) 是完全开源的。

<!--
### Contrail/Tungsten Fabric

[Contrail](https://www.juniper.net/us/en/products-services/sdn/contrail/contrail-networking/), based on [Tungsten Fabric](https://tungsten.io), is a truly open, multi-cloud network virtualization and policy management platform. Contrail and Tungsten Fabric are integrated with various orchestration systems such as Kubernetes, OpenShift, OpenStack and Mesos, and provide different isolation modes for virtual machines, containers/pods and bare metal workloads.
-->
### Contrail/Tungsten Fabric

[Contrail](https://www.juniper.net/us/en/products-services/sdn/contrail/contrail-networking/)
是基于 [Tungsten Fabric](https://tungsten.io) 的，真正开放的多云网络虚拟化和策略管理平台。
Contrail 和 Tungsten Fabric 与各种编排系统集成在一起，例如 Kubernetes、OpenShift、OpenStack 和 Mesos，
并为虚拟机、容器或 Pods 以及裸机工作负载提供了不同的隔离模式。

<!--
### DANM

[DANM](https://github.com/nokia/danm) is a networking solution for telco workloads running in a Kubernetes cluster. It's built up from the following components:

   * A CNI plugin capable of provisioning IPVLAN interfaces with advanced features
   * An in-built IPAM module with the capability of managing multiple, cluster-wide, discontinuous L3 networks and provide a dynamic, static, or no IP allocation scheme on-demand
   * A CNI metaplugin capable of attaching multiple network interfaces to a container, either through its own CNI, or through delegating the job to any of the popular CNI solution like SRI-OV, or Flannel in parallel
   * A Kubernetes controller capable of centrally managing both VxLAN and VLAN interfaces of all Kubernetes hosts
   * Another Kubernetes controller extending Kubernetes' Service-based service discovery concept to work over all network interfaces of a Pod

With this toolset DANM is able to provide multiple separated network interfaces, the possibility to use different networking back ends and advanced IPAM features for the pods.
-->
### DANM

[DANM](https://github.com/nokia/danm) 是一个针对在 Kubernetes 集群中运行的电信工作负载的网络解决方案。
它由以下几个组件构成：

* 能够配置具有高级功能的 IPVLAN 接口的 CNI 插件
* 一个内置的 IPAM 模块，能够管理多个、群集内的、不连续的 L3 网络，并按请求提供动态、静态或无 IP 分配方案
* CNI 元插件能够通过自己的 CNI 或通过将任务授权给其他任何流行的 CNI 解决方案（例如 SRI-OV 或 Flannel）来实现将多个网络接口连接到容器
* Kubernetes 控制器能够集中管理所有 Kubernetes 主机的 VxLAN 和 VLAN 接口
* 另一个 Kubernetes 控制器扩展了 Kubernetes 的基于服务的服务发现概念，以在 Pod 的所有网络接口上工作

通过这个工具集，DANM 可以提供多个分离的网络接口，可以为 Pod 使用不同的网络后端和高级 IPAM 功能。

<!--
### Flannel

[Flannel](https://github.com/coreos/flannel#flannel) is a very simple overlay
network that satisfies the Kubernetes requirements. Many
people have reported success with Flannel and Kubernetes.
-->
### Flannel

[Flannel](https://github.com/coreos/flannel#flannel) 是一个非常简单的能够满足
Kubernetes 所需要的覆盖网络。已经有许多人报告了使用 Flannel 和 Kubernetes 的成功案例。

<!--
### Google Compute Engine (GCE)

For the Google Compute Engine cluster configuration scripts, [advanced
routing](https://cloud.google.com/vpc/docs/routes) is used to
assign each VM a subnet (default is `/24` - 254 IPs).  Any traffic bound for that
subnet will be routed directly to the VM by the GCE network fabric.  This is in
addition to the "main" IP address assigned to the VM, which is NAT'ed for
outbound internet access.  A linux bridge (called `cbr0`) is configured to exist
on that subnet, and is passed to docker's `-bridge` flag.

Docker is started with:

```shell
DOCKER_OPTS="--bridge=cbr0 --iptables=false --ip-masq=false"
```

This bridge is created by Kubelet (controlled by the `--network-plugin=kubenet`
flag) according to the `Node`'s `.spec.podCIDR`.

Docker will now allocate IPs from the `cbr-cidr` block.  Containers can reach
each other and `Nodes` over the `cbr0` bridge.  Those IPs are all routable
within the GCE project network.

GCE itself does not know anything about these IPs, though, so it will not NAT
them for outbound internet traffic.  To achieve that an iptables rule is used
to masquerade (aka SNAT - to make it seem as if packets came from the `Node`
itself) traffic that is bound for IPs outside the GCE project network
(10.0.0.0/8).

```shell
iptables -t nat -A POSTROUTING ! -d 10.0.0.0/8 -o eth0 -j MASQUERADE
```

Lastly IP forwarding is enabled in the kernel (so the kernel will process
packets for bridged containers):

```shell
sysctl net.ipv4.ip_forward=1
```

The result of all this is that all `Pods` can reach each other and can egress
traffic to the internet.
-->
### Google Compute Engine (GCE)

对于 Google Compute Engine 的集群配置脚本，
[高级路由器](https://cloud.google.com/vpc/docs/routes) 用于为每个虚机分配一个子网（默认是 `/24` - 254个 IP），
绑定到该子网的任何流量都将通过 GCE 网络结构直接路由到虚机。
这是除了分配给虚机的“主” IP 地址之外的一个补充，该 IP 地址经过 NAT 转换以用于访问外网。
Linux 网桥（称为“cbr0”）被配置为存在于该子网中，并被传递到 Docker 的 --bridge 参数上。

Docker 会以这样的参数启动：

```shell
DOCKER_OPTS="--bridge=cbr0 --iptables=false --ip-masq=false"
```

这个网桥是由 Kubelet（由 `--network-plugin=kubenet` 参数控制）根据节点的 `.spec.podCIDR` 参数创建的。

Docker 将会从 `cbr-cidr` 块分配 IP。
容器之间可以通过 `cbr0` 网桥相互访问，也可以访问节点。
这些 IP 都可以在 GCE 的网络中被路由。
而 GCE 本身并不知道这些 IP，所以不会对访问外网的流量进行 NAT。
为了实现此目的，使用了 `iptables` 规则来伪装（又称为 SNAT，使数据包看起来好像是来自“节点”本身），
将通信绑定到 GCE 项目网络（10.0.0.0/8）之外的 IP。

```shell
iptables -t nat -A POSTROUTING ! -d 10.0.0.0/8 -o eth0 -j MASQUERADE
```

最后，在内核中启用了 IP 转发（因此内核将处理桥接容器的数据包）：

```shell
sysctl net.ipv4.ip_forward=1
```

所有这些的结果是所有 Pod 都可以互相访问，并且可以将流量发送到互联网。

<!--
### Jaguar

[Jaguar](https://gitlab.com/sdnlab/jaguar) is an open source solution for Kubernetes's network based on OpenDaylight. Jaguar provides overlay network using vxlan and Jaguar CNIPlugin provides one IP address per pod.

### k-vswitch

[k-vswitch](https://github.com/k-vswitch/k-vswitch) is a simple Kubernetes networking plugin based on [Open vSwitch](https://www.openvswitch.org/). It leverages existing functionality in Open vSwitch to provide a robust networking plugin that is easy-to-operate, performant and secure.
-->
### Jaguar

[Jaguar](https://gitlab.com/sdnlab/jaguar) 是一个基于 OpenDaylight 的 Kubernetes 网络开源解决方案。
Jaguar 使用 vxlan 提供覆盖网络，而 Jaguar CNIPlugin 为每个 Pod 提供一个 IP 地址。

### k-vswitch

[k-vswitch](https://github.com/k-vswitch/k-vswitch) 是一个基于
[Open vSwitch](https://www.openvswitch.org/) 的简易 Kubernetes 网络插件。
它利用 Open vSwitch 中现有的功能来提供强大的网络插件，该插件易于操作，高效且安全。

<!--
### Knitter

[Knitter](https://github.com/ZTE/Knitter/) is a network solution which supports multiple networking in Kubernetes. It provides the ability of tenant management and network management. Knitter includes a set of end-to-end NFV container networking solutions besides multiple network planes, such as keeping IP address for applications, IP address migration, etc.

### Kube-OVN

[Kube-OVN](https://github.com/alauda/kube-ovn) is an OVN-based kubernetes network fabric for enterprises. With the help of OVN/OVS, it provides some advanced overlay network features like subnet, QoS, static IP allocation, traffic mirroring, gateway, openflow-based network policy and service proxy.
-->
### Knitter

[Knitter](https://github.com/ZTE/Knitter/) 是一个支持 Kubernetes 中实现多个网络系统的解决方案。
它提供了租户管理和网络管理的功能。除了多个网络平面外，Knitter 还包括一组端到端的 NFV 容器网络解决方案，
例如为应用程序保留 IP 地址、IP 地址迁移等。

### Kube-OVN

[Kube-OVN](https://github.com/alauda/kube-ovn) 是一个基于 OVN 的用于企业的 Kubernetes 网络架构。
借助于 OVN/OVS ，它提供了一些高级覆盖网络功能，例如子网、QoS、静态 IP 分配、流量镜像、网关、
基于 openflow 的网络策略和服务代理。

<!--
### Kube-router

[Kube-router](https://github.com/cloudnativelabs/kube-router) is a purpose-built networking solution for Kubernetes that aims to provide high performance and operational simplicity. Kube-router provides a Linux [LVS/IPVS](https://www.linuxvirtualserver.org/software/ipvs.html)-based service proxy, a Linux kernel forwarding-based pod-to-pod networking solution with no overlays, and iptables/ipset-based network policy enforcer.
-->
### Kube-router

[Kube-router](https://github.com/cloudnativelabs/kube-router) 是 Kubernetes 的专用网络解决方案，
旨在提供高性能和易操作性。 
Kube-router 提供了一个基于 Linux [LVS/IPVS](https://www.linuxvirtualserver.org/software/ipvs.html)
的服务代理、一个基于 Linux 内核转发的无覆盖 Pod-to-Pod 网络解决方案和基于 iptables/ipset 的网络策略执行器。

<!--
### L2 networks and linux bridging

If you have a "dumb" L2 network, such as a simple switch in a "bare-metal"
environment, you should be able to do something similar to the above GCE setup.
Note that these instructions have only been tried very casually - it seems to
work, but has not been thoroughly tested.  If you use this technique and
perfect the process, please let us know.

Follow the "With Linux Bridge devices" section of [this very nice
tutorial](https://blog.oddbit.com/2014/08/11/four-ways-to-connect-a-docker/) from
Lars Kellogg-Stedman.
-->
### L2 networks and linux bridging

如果你具有一个“哑”的L2网络，例如“裸机”环境中的简单交换机，则应该能够执行与上述 GCE 设置类似的操作。
请注意，这些说明仅是非常简单的尝试过-似乎可行，但尚未经过全面测试。
如果您使用此技术并完善了流程，请告诉我们。

根据 Lars Kellogg-Stedman 的这份非常不错的“Linux 网桥设备”
[使用说明](https://blog.oddbit.com/2014/08/11/four-ways-to-connect-a-docker/)来进行操作。

<!--
### Multus (a Multi Network plugin)

[Multus](https://github.com/Intel-Corp/multus-cni) is a Multi CNI plugin to support the Multi Networking feature in Kubernetes using CRD based network objects in Kubernetes.

Multus supports all [reference plugins](https://github.com/containernetworking/plugins) (eg. [Flannel](https://github.com/containernetworking/plugins/tree/master/plugins/meta/flannel), [DHCP](https://github.com/containernetworking/plugins/tree/master/plugins/ipam/dhcp), [Macvlan](https://github.com/containernetworking/plugins/tree/master/plugins/main/macvlan)) that implement the CNI specification and 3rd party plugins (eg. [Calico](https://github.com/projectcalico/cni-plugin), [Weave](https://github.com/weaveworks/weave), [Cilium](https://github.com/cilium/cilium), [Contiv](https://github.com/contiv/netplugin)). In addition to it, Multus supports [SRIOV](https://github.com/hustcat/sriov-cni), [DPDK](https://github.com/Intel-Corp/sriov-cni), [OVS-DPDK & VPP](https://github.com/intel/vhost-user-net-plugin) workloads in Kubernetes with both cloud native and NFV based applications in Kubernetes.
-->
### Multus (a Multi Network plugin)

[Multus](https://github.com/Intel-Corp/multus-cni) 是一个多 CNI 插件，
使用 Kubernetes 中基于 CRD 的网络对象来支持实现 Kubernetes 多网络系统。

Multus 支持所有[参考插件](https://github.com/containernetworking/plugins)（比如：
[Flannel](https://github.com/containernetworking/plugins/tree/master/plugins/meta/flannel)、
[DHCP](https://github.com/containernetworking/plugins/tree/master/plugins/ipam/dhcp)、
[Macvlan](https://github.com/containernetworking/plugins/tree/master/plugins/main/macvlan) ）
来实现 CNI 规范和第三方插件（比如：
[Calico](https://github.com/projectcalico/cni-plugin)、
[Weave](https://github.com/weaveworks/weave)、
[Cilium](https://github.com/cilium/cilium)、
[Contiv](https://github.com/contiv/netplugin)）。
除此之外， Multus 还支持
[SRIOV](https://github.com/hustcat/sriov-cni)、
[DPDK](https://github.com/Intel-Corp/sriov-cni)、
[OVS-DPDK & VPP](https://github.com/intel/vhost-user-net-plugin) 的工作负载，
以及 Kubernetes 中基于云的本机应用程序和基于 NFV 的应用程序。

<!--
### NSX-T

[VMware NSX-T](https://docs.vmware.com/en/VMware-NSX-T/index.html) is a network virtualization and security platform. NSX-T can provide network virtualization for a multi-cloud and multi-hypervisor environment and is focused on emerging application frameworks and architectures that have heterogeneous endpoints and technology stacks. In addition to vSphere hypervisors, these environments include other hypervisors such as KVM, containers, and bare metal.

[NSX-T Container Plug-in (NCP)](https://docs.vmware.com/en/VMware-NSX-T/2.0/nsxt_20_ncp_kubernetes.pdf) provides integration between NSX-T and container orchestrators such as Kubernetes, as well as integration between NSX-T and container-based CaaS/PaaS platforms such as Pivotal Container Service (PKS) and OpenShift.
-->
### NSX-T

[VMware NSX-T](https://docs.vmware.com/en/VMware-NSX-T/index.html) 是一个网络虚拟化和安全平台。
NSX-T 可以为多云及多系统管理程序环境提供网络虚拟化，并专注于具有异构端点和技术堆栈的新兴应用程序框架和体系结构。
除了 vSphere 管理程序之外，这些环境还包括其他虚拟机管理程序，例如 KVM、容器和裸机。

[NSX-T Container Plug-in (NCP)](https://docs.vmware.com/en/VMware-NSX-T/2.0/nsxt_20_ncp_kubernetes.pdf)
提供了 NSX-T 与容器协调器（例如 Kubernetes）之间的结合，
以及 NSX-T 与基于容器的 CaaS/PaaS 平台（例如 Pivotal Container Service（PKS）和 OpenShift）之间的集成。

<!--
### Nuage Networks VCS (Virtualized Cloud Services)

[Nuage](https://www.nuagenetworks.net) provides a highly scalable policy-based Software-Defined Networking (SDN) platform. Nuage uses the open source Open vSwitch for the data plane along with a feature rich SDN Controller built on open standards.

The Nuage platform uses overlays to provide seamless policy-based networking between Kubernetes Pods and non-Kubernetes environments (VMs and bare metal servers). Nuage's policy abstraction model is designed with applications in mind and makes it easy to declare fine-grained policies for applications.The platform's real-time analytics engine enables visibility and security monitoring for Kubernetes applications.
-->
### Nuage Networks VCS (Virtualized Cloud Services)

[Nuage](https://www.nuagenetworks.net) 提供了一个高度可扩展的基于策略的软件定义网络（SDN）平台。
Nuage 使用开源的 Open vSwitch 作为数据平面，以及基于开放标准构建具有丰富功能的 SDN 控制器。

Nuage 平台使用覆盖层在 Kubernetes Pod 和非 Kubernetes 环境（VM 和裸机服务器）之间提供基于策略的无缝联网。
Nuage 的策略抽象模型在设计时就考虑到了应用程序，并且可以轻松声明应用程序的细粒度策略。
该平台的实时分析引擎可为 Kubernetes 应用程序提供可见性和安全性监控。

<!--
### OpenVSwitch

[OpenVSwitch](https://www.openvswitch.org/) is a somewhat more mature but also
complicated way to build an overlay network.  This is endorsed by several of the
"Big Shops" for networking.

### OVN (Open Virtual Networking)

OVN is an opensource network virtualization solution developed by the
Open vSwitch community.  It lets one create logical switches, logical routers,
stateful ACLs, load-balancers etc to build different virtual networking
topologies.  The project has a specific Kubernetes plugin and documentation
at [ovn-kubernetes](https://github.com/openvswitch/ovn-kubernetes).
-->
### OpenVSwitch

[OpenVSwitch](https://www.openvswitch.org/) 是一个较为成熟的解决方案，但同时也增加了构建覆盖网络的复杂性。
这也得到了几个网络系统的“大商店”的拥护。

### OVN (开放式虚拟网络)

OVN 是一个由 Open vSwitch 社区开发的开源的网络虚拟化解决方案。
它允许创建逻辑交换器、逻辑路由、状态 ACL、负载均衡等等来建立不同的虚拟网络拓扑。
该项目有一个特定的Kubernetes插件和文档 [ovn-kubernetes](https://github.com/openvswitch/ovn-kubernetes)。

<!--
### Romana

[Romana](https://romana.io) is an open source network and security automation solution that lets you deploy Kubernetes without an overlay network. Romana supports Kubernetes [Network Policy](/docs/concepts/services-networking/network-policies/) to provide isolation across network namespaces.
-->
### Romana

[Romana](https://romana.io) 是一个开源网络和安全自动化解决方案。
它可以让你在没有覆盖网络的情况下部署 Kubernetes。
Romana 支持 Kubernetes [网络策略](/zh/docs/concepts/services-networking/network-policies/)，
来提供跨网络命名空间的隔离。

<!--
### Weave Net from Weaveworks

[Weave Net](https://www.weave.works/products/weave-net/) is a
resilient and simple to use network for Kubernetes and its hosted applications.
Weave Net runs as a [CNI plug-in](https://www.weave.works/docs/net/latest/cni-plugin/)
or stand-alone.  In either version, it doesn't require any configuration or extra code
to run, and in both cases, the network provides one IP address per pod - as is standard for Kubernetes.
-->
### Weaveworks 的 Weave Net

[Weave Net](https://www.weave.works/products/weave-net/) 是 Kubernetes 及其
托管应用程序的弹性且易于使用的网络系统。
Weave Net 可以作为 [CNI 插件](https://www.weave.works/docs/net/latest/cni-plugin/) 运行或者独立运行。
在这两种运行方式里，都不需要任何配置或额外的代码即可运行，并且在两种情况下，
网络都为每个 Pod 提供一个 IP 地址 -- 这是 Kubernetes 的标准配置。

## {{% heading "whatsnext" %}}

<!--
The early design of the networking model and its rationale, and some future
plans are described in more detail in the [networking design
document](https://git.k8s.io/community/contributors/design-proposals/network/networking.md).
-->
网络模型的早期设计、运行原理以及未来的一些计划，都在
[联网设计文档](https://git.k8s.io/community/contributors/design-proposals/network/networking.md)
里有更详细的描述。
