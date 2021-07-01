---
title: 容器运行时
content_type: concept
weight: 20
---
<!--
reviewers:
- vincepri
- bart0sh
title: Container runtimes
content_type: concept
weight: 20
-->

<!-- overview -->

<!-- 
You need to install a
{{< glossary_tooltip text="container runtime" term_id="container-runtime" >}}
into each node in the cluster so that Pods can run there. This page outlines
what is involved and describes related tasks for setting up nodes.
 -->
你需要在集群内每个节点上安装一个
{{< glossary_tooltip text="容器运行时" term_id="container-runtime" >}}
以使 Pod 可以运行在上面。本文概述了所涉及的内容并描述了与节点设置相关的任务。

<!-- body -->

<!-- 
This page lists details for using several common container runtimes with
Kubernetes, on Linux:
 -->
本文列出了在 Linux 上结合 Kubernetes 使用的几种通用容器运行时的详细信息： 

- [containerd](#containerd)
- [CRI-O](#cri-o)
- [Docker](#docker)

<!-- 
{{< note >}}
For other operating systems, look for documentation specific to your platform.
{{< /note >}}
 -->
提示：对于其他操作系统，请查阅特定于你所使用平台的相关文档。

<!--
## Cgroup drivers
-->
## Cgroup 驱动程序

<!--
Control groups are used to constrain resources that are allocated to processes.

When [systemd](https://www.freedesktop.org/wiki/Software/systemd/) is chosen as the init
system for a Linux distribution, the init process generates and consumes a root control group
(`cgroup`) and acts as a cgroup manager.
Systemd has a tight integration with cgroups and allocates a cgroup per systemd unit. It's possible
to configure your container runtime and the kubelet to use `cgroupfs`. Using `cgroupfs` alongside
systemd means that there will be two different cgroup managers.
-->
控制组用来约束分配给进程的资源。

当某个 Linux 系统发行版使用 [systemd](https://www.freedesktop.org/wiki/Software/systemd/)
作为其初始化系统时，初始化进程会生成并使用一个 root 控制组 (`cgroup`), 并充当 cgroup 管理器。
Systemd 与 cgroup 集成紧密，并将为每个 systemd 单元分配一个 cgroup。
你也可以配置容器运行时和 kubelet 使用 `cgroupfs`。
连同 systemd 一起使用 `cgroupfs` 意味着将有两个不同的 cgroup 管理器。

<!--
A single cgroup manager simplifies the view of what resources are being allocated
and will by default have a more consistent view of the available and in-use resources.
When there are two cgroup managers on a system, you end up with two views of those resources.
In the field, people have reported cases where nodes that are configured to use `cgroupfs`
for the kubelet and Docker, but `systemd` for the rest of the processes, become unstable under
resource pressure.
-->
单个 cgroup 管理器将简化分配资源的视图，并且默认情况下将对可用资源和使用
中的资源具有更一致的视图。
当有两个管理器共存于一个系统中时，最终将对这些资源产生两种视图。
在此领域人们已经报告过一些案例，某些节点配置让 kubelet 和 docker 使用
`cgroupfs`，而节点上运行的其余进程则使用 systemd; 这类节点在资源压力下
会变得不稳定。

<!--
Changing the settings such that your container runtime and kubelet use `systemd` as the cgroup driver
stabilized the system. To configure this for Docker, set `native.cgroupdriver=systemd`.
-->
更改设置，令容器运行时和 kubelet 使用 `systemd` 作为 cgroup 驱动，以此使系统更为稳定。
对于 Docker, 设置 `native.cgroupdriver=systemd` 选项。

<!--
{{< caution >}}
Changing the cgroup driver of a Node that has joined a cluster is a sensitive operation. 
If the kubelet has created Pods using the semantics of one cgroup driver, changing the container
runtime to another cgroup driver can cause errors when trying to re-create the Pod sandbox
for such existing Pods. Restarting the kubelet may not solve such errors.

If you have automation that makes it feasible, replace the node with another using the updated
configuration, or reinstall it using automation.
{{< /caution >}}
-->
注意：更改已加入集群的节点的 cgroup 驱动是一项敏感的操作。
如果 kubelet 已经使用某 cgroup 驱动的语义创建了 pod，更改运行时以使用
别的 cgroup 驱动，当为现有 Pods 重新创建 PodSandbox 时会产生错误。
重启 kubelet 也可能无法解决此类问题。
如果你有切实可行的自动化方案，使用其他已更新配置的节点来替换该节点，
或者使用自动化方案来重新安装。

<!-- 
### Migrating to the `systemd` driver in kubeadm managed clusters
-->
### 将 kubeadm 托管的集群迁移到 `systemd` 驱动

<!-- 
Follow this [Migration guide](/docs/tasks/administer-cluster/kubeadm/configure-cgroup-driver)
if you wish to migrate to the `systemd` cgroup driver in existing kubeadm managed clusters.
-->
如果你想迁移到现有 kubeadm 托管集群中的 `systemd` cgroup 驱动程序，
遵循此[迁移指南](/zh/docs/tasks/administer-cluster/kubeadm/configure-cgroup-driver)。

<!-- 
## Container runtimes
 -->
## 容器运行时

{{% thirdparty-content %}}

### containerd

<!--
This section contains the necessary steps to use containerd as CRI runtime.

Use the following commands to install Containerd on your system:

Install and configure prerequisites:
-->
本节包含使用 containerd 作为 CRI 运行时的必要步骤。

使用以下命令在系统上安装 Containerd：

安装和配置的先决条件：

```shell
cat <<EOF | sudo tee /etc/modules-load.d/containerd.conf
overlay
br_netfilter
EOF

sudo modprobe overlay
sudo modprobe br_netfilter

# 设置必需的 sysctl 参数，这些参数在重新启动后仍然存在。
cat <<EOF | sudo tee /etc/sysctl.d/99-kubernetes-cri.conf
net.bridge.bridge-nf-call-iptables  = 1
net.ipv4.ip_forward                 = 1
net.bridge.bridge-nf-call-ip6tables = 1
EOF

# 应用 sysctl 参数而无需重新启动
sudo sysctl --system
```

<!--
Install containerd:
-->
安装 containerd:

{{< tabs name="tab-cri-containerd-installation" >}}
{{% tab name="Linux" %}}

<!--
1. Install the `containerd.io` package from the official Docker repositories.
   Instructions for setting up the Docker repository for your respective Linux distribution and
   installing the `containerd.io` package can be found at
   [Install Docker Engine](https://docs.docker.com/engine/install/#server).
-->
1. 从官方Docker仓库安装 `containerd.io` 软件包。可以在
   [安装 Docker 引擎](https://docs.docker.com/engine/install/#server)
   中找到有关为各自的 Linux 发行版设置 Docker 存储库和安装 `containerd.io`
   软件包的说明。

<!--
2. Configure containerd:
-->
2. 配置 containerd：

   ```shell
   sudo mkdir -p /etc/containerd
   containerd config default | sudo tee /etc/containerd/config.toml
   ```

<!--
3. Restart containerd:
-->
3. 重新启动 containerd:

   ```shell
   sudo systemctl restart containerd
   ```

{{% /tab %}}
{{% tab name="Windows (PowerShell)" %}}

<!--
Start a Powershell session, set `$Version` to the desired version (ex: `$Version=1.4.3`),
and then run the following commands:
-->
启动 Powershell 会话，将 `$Version` 设置为所需的版本（例如：`$Version=1.4.3`），
然后运行以下命令：

<!--
1. Download containerd:
-->
1. 下载 containerd：

   ```powershell
   curl.exe -L https://github.com/containerd/containerd/releases/download/v$Version/containerd-$Version-windows-amd64.tar.gz -o containerd-windows-amd64.tar.gz
   tar.exe xvf .\containerd-windows-amd64.tar.gz
   ```
<!--
2. Extract and configure:
-->
2. 提取并配置：

   ```powershell
   Copy-Item -Path ".\bin\" -Destination "$Env:ProgramFiles\containerd" -Recurse -Force
   cd $Env:ProgramFiles\containerd\
   .\containerd.exe config default | Out-File config.toml -Encoding ascii

   # 检查配置。根据你的配置，可能需要调整：
   # - sandbox_image (Kubernetes pause 镜像)
   # - cni bin_dir 和 conf_dir 位置
   Get-Content config.toml

   # (可选 - 不过强烈建议) 禁止 Windows Defender 扫描 containerd
   Add-MpPreference -ExclusionProcess "$Env:ProgramFiles\containerd\containerd.exe"
   ```
<!--
3. Start containerd:
-->
3. 启动 containerd:

   ```powershell
   .\containerd.exe --register-service
   Start-Service containerd
   ```

{{% /tab %}}
{{< /tabs >}}

<!-- 
#### Using the `systemd` cgroup driver {#containerd-systemd}
--> 

#### 使用 `systemd` cgroup 驱动程序 {#containerd-systemd}

<!-- 
To use the `systemd` cgroup driver in `/etc/containerd/config.toml` with `runc`, set
-->
结合 `runc` 使用 `systemd` cgroup 驱动，在 `/etc/containerd/config.toml` 中设置 

```
[plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc]
  ...
  [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc.options]
    SystemdCgroup = true
```

<!--
If you apply this change make sure to restart containerd again:
-->
如果您应用此更改，请确保再次重新启动 containerd：

```shell
sudo systemctl restart containerd
```

<!--
When using kubeadm, manually configure the
[cgroup driver for kubelet](/docs/setup/production-environment/tools/kubeadm/install-kubeadm/#configure-cgroup-driver-used-by-kubelet-on-control-plane-node).
-->
当使用 kubeadm 时，请手动配置
[kubelet 的 cgroup 驱动](/zh/docs/setup/production-environment/tools/kubeadm/install-kubeadm/#configure-cgroup-driver-used-by-kubelet-on-control-plane-node).

### CRI-O

<!--
This section contains the necessary steps to install CRI-O as a container runtime.

Use the following commands to install CRI-O on your system:
-->
本节包含安装 CRI-O 作为容器运行时的必要步骤。

使用以下命令在系统中安装 CRI-O：

{{< note >}}
<!--
The CRI-O major and minor versions must match the Kubernetes major and minor versions.
For more information, see the [CRI-O compatibility matrix](https://github.com/cri-o/cri-o#compatibility-matrix-cri-o--kubernetes).
-->
CRI-O 的主要以及次要版本必须与 Kubernetes 的主要和次要版本相匹配。
更多信息请查阅
[CRI-O 兼容性列表](https://github.com/cri-o/cri-o#compatibility-matrix-cri-o--kubernetes)。
{{< /note >}}

<!--
Install and configure prerequisites:
-->
安装并配置前置环境：

```shell

# 创建 .conf 文件以在启动时加载模块
cat <<EOF | sudo tee /etc/modules-load.d/crio.conf
overlay
br_netfilter
EOF

sudo modprobe overlay
sudo modprobe br_netfilter

# 配置 sysctl 参数，这些配置在重启之后仍然起作用
cat <<EOF | sudo tee /etc/sysctl.d/99-kubernetes-cri.conf
net.bridge.bridge-nf-call-iptables  = 1
net.ipv4.ip_forward                 = 1
net.bridge.bridge-nf-call-ip6tables = 1
EOF

sudo sysctl --system
```

{{< tabs name="tab-cri-cri-o-installation" >}}
{{% tab name="Debian" %}}

<!-- 
To install CRI-O on the following operating systems, set the environment variable `OS`
to the appropriate value from the following table:

| Operating system | `$OS`             |
| ---------------- | ----------------- |
| Debian Unstable  | `Debian_Unstable` |
| Debian Testing   | `Debian_Testing`  |

<br />
Then, set `$VERSION` to the CRI-O version that matches your Kubernetes version.
For instance, if you want to install CRI-O 1.20, set `VERSION=1.20`.
You can pin your installation to a specific release.
To install version 1.20.0, set `VERSION=1.20:1.20.0`.
<br />

Then run
-->
在下列操作系统上安装 CRI-O, 使用下表中合适的值设置环境变量 `OS`:

| 操作系统          | `$OS`             |
| ---------------- | ----------------- |
| Debian Unstable  | `Debian_Unstable` |
| Debian Testing   | `Debian_Testing`  |

<br />
然后，将 `$VERSION` 设置为与你的 Kubernetes 相匹配的 CRI-O 版本。
例如，如果你要安装 CRI-O 1.20, 请设置 `VERSION=1.20`.
你也可以安装一个特定的发行版本。
例如要安装 1.20.0 版本，设置 `VERSION=1.20.0:1.20.0`.
<br />

然后执行

```shell
cat <<EOF | sudo tee /etc/apt/sources.list.d/devel:kubic:libcontainers:stable.list
deb https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/$OS/ /
EOF
cat <<EOF | sudo tee /etc/apt/sources.list.d/devel:kubic:libcontainers:stable:cri-o:$VERSION.list
deb http://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable:/cri-o:/$VERSION/$OS/ /
EOF

curl -L https://download.opensuse.org/repositories/devel:kubic:libcontainers:stable:cri-o:$VERSION/$OS/Release.key | sudo apt-key --keyring /etc/apt/trusted.gpg.d/libcontainers.gpg add -
curl -L https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/$OS/Release.key | sudo apt-key --keyring /etc/apt/trusted.gpg.d/libcontainers.gpg add -

sudo apt-get update
sudo apt-get install cri-o cri-o-runc
```

{{% /tab %}}

{{% tab name="Ubuntu" %}}

<!-- 
To install on the following operating systems, set the environment variable `OS`
to the appropriate field in the following table:

| Operating system | `$OS`             |
| ---------------- | ----------------- |
| Ubuntu 20.04     | `xUbuntu_20.04`   |
| Ubuntu 19.10     | `xUbuntu_19.10`   |
| Ubuntu 19.04     | `xUbuntu_19.04`   |
| Ubuntu 18.04     | `xUbuntu_18.04`   |

<br />
Then, set `$VERSION` to the CRI-O version that matches your Kubernetes version.
For instance, if you want to install CRI-O 1.20, set `VERSION=1.20`.
You can pin your installation to a specific release.
To install version 1.20.0, set `VERSION=1.20:1.20.0`.
<br />

Then run
-->
在下列操作系统上安装 CRI-O, 使用下表中合适的值设置环境变量 `OS`:

| 操作系统          | `$OS`             |
| ---------------- | ----------------- |
| Ubuntu 20.04     | `xUbuntu_20.04`   |
| Ubuntu 19.10     | `xUbuntu_19.10`   |
| Ubuntu 19.04     | `xUbuntu_19.04`   |
| Ubuntu 18.04     | `xUbuntu_18.04`   |

<br />
然后，将 `$VERSION` 设置为与你的 Kubernetes 相匹配的 CRI-O 版本。
例如，如果你要安装 CRI-O 1.20, 请设置 `VERSION=1.20`.
你也可以安装一个特定的发行版本。
例如要安装 1.20.0 版本，设置 `VERSION=1.20:1.20.0`.
<br />

然后执行

```shell
cat <<EOF | sudo tee /etc/apt/sources.list.d/devel:kubic:libcontainers:stable.list
deb https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/$OS/ /
EOF
cat <<EOF | sudo tee /etc/apt/sources.list.d/devel:kubic:libcontainers:stable:cri-o:$VERSION.list
deb http://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable:/cri-o:/$VERSION/$OS/ /
EOF

curl -L https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/$OS/Release.key | sudo apt-key --keyring /etc/apt/trusted.gpg.d/libcontainers.gpg add -
curl -L https://download.opensuse.org/repositories/devel:kubic:libcontainers:stable:cri-o:$VERSION/$OS/Release.key | sudo apt-key --keyring /etc/apt/trusted.gpg.d/libcontainers-cri-o.gpg add -

sudo apt-get update
sudo apt-get install cri-o cri-o-runc
```
 
{{% /tab %}}

{{% tab name="CentOS" %}}

<!-- 
To install on the following operating systems, set the environment variable `OS`
to the appropriate field in the following table:

| Operating system | `$OS`             |
| ---------------- | ----------------- |
| Centos 8         | `CentOS_8`        |
| Centos 8 Stream  | `CentOS_8_Stream` |
| Centos 7         | `CentOS_7`        |

<br />
Then, set `$VERSION` to the CRI-O version that matches your Kubernetes version.
For instance, if you want to install CRI-O 1.20, set `VERSION=1.20`.
You can pin your installation to a specific release.
To install version 1.20.0, set `VERSION=1.20:1.20.0`.
<br />

Then run
-->
在下列操作系统上安装 CRI-O, 使用下表中合适的值设置环境变量 `OS`:

| 操作系统          | `$OS`             |
| ---------------- | ----------------- |
| Centos 8         | `CentOS_8`        |
| Centos 8 Stream  | `CentOS_8_Stream` |
| Centos 7         | `CentOS_7`        |

<br />
然后，将 `$VERSION` 设置为与你的 Kubernetes 相匹配的 CRI-O 版本。
例如，如果你要安装 CRI-O 1.20, 请设置 `VERSION=1.20`.
你也可以安装一个特定的发行版本。
例如要安装 1.20.0 版本，设置 `VERSION=1.20:1.20.0`.
<br />

然后执行

```shell
sudo curl -L -o /etc/yum.repos.d/devel:kubic:libcontainers:stable.repo https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/$OS/devel:kubic:libcontainers:stable.repo
sudo curl -L -o /etc/yum.repos.d/devel:kubic:libcontainers:stable:cri-o:$VERSION.repo https://download.opensuse.org/repositories/devel:kubic:libcontainers:stable:cri-o:$VERSION/$OS/devel:kubic:libcontainers:stable:cri-o:$VERSION.repo
sudo yum install cri-o
```

{{% /tab %}}

{{% tab name="openSUSE Tumbleweed" %}}

```shell
sudo zypper install cri-o
```
{{% /tab %}}
{{% tab name="Fedora" %}}

<!-- 
Set `$VERSION` to the CRI-O version that matches your Kubernetes version.
For instance, if you want to install CRI-O 1.20, `VERSION=1.20`.

You can find available versions with:
```shell
sudo dnf module list cri-o
```
CRI-O does not support pinning to specific releases on Fedora.

Then run
-->
将 `$VERSION` 设置为与你的 Kubernetes 相匹配的 CRI-O 版本。
例如，如果要安装 CRI-O 1.20，请设置 `VERSION=1.20`。
你可以用下列命令查找可用的版本：

```shell
sudo dnf module list cri-o
```

CRI-O 不支持在 Fedora 上固定到特定的版本。

然后执行

```shell
sudo dnf module enable cri-o:$VERSION
sudo dnf install cri-o --now
```

{{% /tab %}}
{{< /tabs >}}

<!-- 
Start CRI-O:
-->
启动 CRI-O：

```shell
sudo systemctl daemon-reload
sudo systemctl enable crio --now
```

<!--
Refer to the [CRI-O installation guide](https://github.com/cri-o/cri-o/blob/master/install.md)
for more information.
 -->
参阅[CRI-O 安装指南](https://github.com/cri-o/cri-o/blob/master/install.md)
了解进一步的详细信息。

<!--
#### cgroup driver

CRI-O uses the systemd cgroup driver per default. To switch to the `cgroupfs`
cgroup driver, either edit `/etc/crio/crio.conf` or place a drop-in
configuration in `/etc/crio/crio.conf.d/02-cgroup-manager.conf`, for example:
-->
#### cgroup 驱动

默认情况下，CRI-O 使用 systemd cgroup 驱动程序。要切换到 `cgroupfs`
驱动程序，或者编辑 `/ etc / crio / crio.conf` 或放置一个插件
在 `/etc/crio/crio.conf.d/02-cgroup-manager.conf` 中的配置，例如：

```toml
[crio.runtime]
conmon_cgroup = "pod"
cgroup_manager = "cgroupfs"
```

<!-- 
Please also note the changed `conmon_cgroup`, which has to be set to the value
`pod` when using CRI-O with `cgroupfs`. It is generally necessary to keep the
cgroup driver configuration of the kubelet (usually done via kubeadm) and CRI-O
in sync.
 -->
另请注意更改后的 `conmon_cgroup`，将 CRI-O 与 `cgroupfs` 一起使用时，
必须将其设置为 `pod`。通常有必要保持 kubelet 的 cgroup 驱动程序配置
（通常透过 kubeadm 完成）和 CRI-O 一致。

### Docker

<!--
1. On each of your nodes, install the Docker for your Linux distribution as per
   [Install Docker Engine](https://docs.docker.com/engine/install/#server).
   You can find the latest validated version of Docker in this
   [dependencies](https://git.k8s.io/kubernetes/build/dependencies.yaml) file.
 -->
1. 在每个节点上，根据[安装 Docker 引擎](https://docs.docker.com/engine/install/#server)
   为你的 Linux 发行版安装 Docker。
   你可以在此文件中找到最新的经过验证的 Docker 版本
   [依赖关系](https://git.k8s.io/kubernetes/build/dependencies.yaml)。

<!--
2. Configure the Docker daemon, in particular to use systemd for the management of the container’s cgroups.
 -->
2. 配置 Docker 守护程序，尤其是使用 systemd 来管理容器的 cgroup。

   ```shell
   sudo mkdir /etc/docker
   cat <<EOF | sudo tee /etc/docker/daemon.json
   {
     "exec-opts": ["native.cgroupdriver=systemd"],
     "log-driver": "json-file",
     "log-opts": {
       "max-size": "100m"
     },
     "storage-driver": "overlay2"
   }
   EOF
   ```

   {{< note >}}
   <!--
   `overlay2` is the preferred storage driver for systems running Linux kernel version 4.0 or higher,
   or RHEL or CentOS using version 3.10.0-514 and above.
   -->
   对于运行 Linux 内核版本 4.0 或更高版本，或使用 3.10.0-51 及更高版本的 RHEL
   或 CentOS 的系统，`overlay2`是首选的存储驱动程序。
   {{< /note >}}

<!--
3. Restart Docker and enable on boot:
-->
3. 重新启动 Docker 并在启动时启用：

   ```shell
   sudo systemctl enable docker
   sudo systemctl daemon-reload
   sudo systemctl restart docker
   ```

{{< note >}}
<!--
For more information refer to
  - [Configure the Docker daemon](https://docs.docker.com/config/daemon/)
  - [Control Docker with systemd](https://docs.docker.com/config/daemon/systemd/)
-->
有关更多信息，请参阅

- [配置 Docker 守护程序](https://docs.docker.com/config/daemon/)
- [使用 systemd 控制 Docker](https://docs.docker.com/config/daemon/systemd/)
{{< /note >}}

