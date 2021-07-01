---
title: 使用 kubeadm 创建一个高可用 etcd 集群
content_type: task
weight: 70
---

<!--
reviewers:
- sig-cluster-lifecycle
title: Set up a High Availability etcd cluster with kubeadm
content_type: task
weight: 70
-->

<!-- overview -->

{{< note >}}
<!--
While kubeadm is being used as the management tool for external etcd nodes
in this guide, please note that kubeadm does not plan to support certificate rotation
or upgrades for such nodes. The long term plan is to empower the tool
[etcdadm](https://github.com/kubernetes-sigs/etcdadm) to manage these
aspects.
-->
在本指南中，当 kubeadm 用作为外部 etcd 节点管理工具，请注意 kubeadm 不计划支持此类节点的证书更换或升级。对于长期规划是使用 [etcdadm](https://github.com/kubernetes-sigs/etcdadm) 增强工具来管理这方面。
{{< /note >}}

<!--
Kubeadm defaults to running a single member etcd cluster in a static pod managed
by the kubelet on the control plane node. This is not a high availability setup
as the etcd cluster contains only one member and cannot sustain any members
becoming unavailable. This task walks through the process of creating a high
availability etcd cluster of three members that can be used as an external etcd
when using kubeadm to set up a kubernetes cluster.
-->
默认情况下，kubeadm 运行单成员的 etcd 集群，该集群由控制面节点上的 kubelet 以静态 Pod 的方式进行管理。由于 etcd 集群只包含一个成员且不能在任一成员不可用时保持运行，所以这不是一种高可用设置。本任务，将告诉你如何在使用 kubeadm 创建一个 kubernetes 集群时创建一个外部 etcd：有三个成员的高可用 etcd 集群。



## {{% heading "prerequisites" %}}


<!--
* Three hosts that can talk to each other over ports 2379 and 2380. This document assumes these default ports. However, they are configurable through the kubeadm config file.
-->
* 三个可以通过 2379 和 2380 端口相互通信的主机。本文档使用这些作为默认端口。不过，它们可以通过 kubeadm 的配置文件进行自定义。

<!--
* Each host must [have docker, kubelet, and kubeadm installed][toolbox].
-->
* 每个主机必须 [安装有 docker、kubelet 和 kubeadm][工具箱]。

<!--
* Some infrastructure to copy files between hosts. For example `ssh` and `scp` can satisfy this requirement.
-->
* 一些可以用来在主机间复制文件的基础设施。例如 `ssh` 和 `scp` 就可以满足需求。

<!--
[toolbox]: /docs/setup/production-environment/tools/kubeadm/install-kubeadm/
-->
[工具箱]: /docs/setup/production-environment/tools/kubeadm/install-kubeadm/



<!-- steps -->

<!--
## Setting up the cluster
-->
## 建立集群

<!--
The general approach is to generate all certs on one node and only distribute the *necessary* files to the other nodes.
-->
一般来说，是在一个节点上生成所有证书并且只分发这些*必要*的文件到其它节点上。

{{< note >}}
<!--
kubeadm contains all the necessary crytographic machinery to generate the certificates described below; no other cryptographic tooling is required for this example.
-->
kubeadm 包含生成下述证书所需的所有必要的密码学工具；在这个例子中，不需要其他加密工具。
{{< /note >}}

<!--
1. Configure the kubelet to be a service manager for etcd.
 
   {{< note >}}You must do this on every host where etcd should be running.{{< /note >}}
   Since etcd was created first, you must override the service priority by creating a new unit file
   that has higher precedence than the kubeadm-provided kubelet unit file.
-->
1. 将 kubelet 配置为 etcd 的服务管理器。

   {{< note >}}
   你必须在要运行 etcd 的所有主机上执行此操作。
   {{< /note >}}
   由于 etcd 是首先创建的，因此你必须通过创建具有更高优先级的新文件来覆盖
   kubeadm 提供的 kubelet 单元文件。

   ```sh
   cat << EOF > /etc/systemd/system/kubelet.service.d/20-etcd-service-manager.conf
   [Service]
   ExecStart=
   # 将下面的 "systemd" 替换为你的容器运行时所使用的 cgroup 驱动。
   # kubelet 的默认值为 "cgroupfs"。
   ExecStart=/usr/bin/kubelet --address=127.0.0.1 --pod-manifest-path=/etc/kubernetes/manifests --cgroup-driver=systemd
   Restart=always
   EOF

   systemctl daemon-reload
   systemctl restart kubelet
   ```

   <!--
   Check the kubelet status to ensure it is running.
   -->
   检查 kubelet 的状态以确保其处于运行状态：


   ```shell
   systemctl status kubelet
   ```

<!--
1. Create configuration files for kubeadm.

   Generate one kubeadm configuration file for each host that will have an etcd
   member running on it using the following script.
-->
2. 为 kubeadm 创建配置文件。

   使用以下脚本为每个将要运行 etcd 成员的主机生成一个 kubeadm 配置文件。

   ```sh
   # 使用 IP 或可解析的主机名替换 HOST0、HOST1 和 HOST2
   export HOST0=10.0.0.6
   export HOST1=10.0.0.7
   export HOST2=10.0.0.8

   # 创建临时目录来存储将被分发到其它主机上的文件
   mkdir -p /tmp/${HOST0}/ /tmp/${HOST1}/ /tmp/${HOST2}/

   ETCDHOSTS=(${HOST0} ${HOST1} ${HOST2})
   NAMES=("infra0" "infra1" "infra2")

   for i in "${!ETCDHOSTS[@]}"; do
   HOST=${ETCDHOSTS[$i]}
   NAME=${NAMES[$i]}
   cat << EOF > /tmp/${HOST}/kubeadmcfg.yaml
   apiVersion: "kubeadm.k8s.io/v1beta2"
   kind: ClusterConfiguration
   etcd:
       local:
           serverCertSANs:
           - "${HOST}"
           peerCertSANs:
           - "${HOST}"
           extraArgs:
               initial-cluster: infra0=https://${ETCDHOSTS[0]}:2380,infra1=https://${ETCDHOSTS[1]}:2380,infra2=https://${ETCDHOSTS[2]}:2380
               initial-cluster-state: new
               name: ${NAME}
               listen-peer-urls: https://${HOST}:2380
               listen-client-urls: https://${HOST}:2379
               advertise-client-urls: https://${HOST}:2379
               initial-advertise-peer-urls: https://${HOST}:2380
   EOF
   done
   ```

<!--
1. Generate the certificate authority

   If you already have a CA then the only action that is copying the CA's `crt` and
   `key` file to `/etc/kubernetes/pki/etcd/ca.crt` and
   `/etc/kubernetes/pki/etcd/ca.key`. After those files have been copied,
   proceed to the next step, "Create certificates for each member".
-->
3. 生成证书颁发机构

   如果你已经拥有 CA，那么唯一的操作是复制 CA 的 `crt` 和 `key` 文件到
   `etc/kubernetes/pki/etcd/ca.crt` 和 `/etc/kubernetes/pki/etcd/ca.key`。
   复制完这些文件后继续下一步，“为每个成员创建证书”。

   <!--
   If you do not already have a CA then run this command on `$HOST0` (where you generated the configuration files for kubeadm).
   -->
   如果你还没有 CA，则在 `$HOST0`（你为 kubeadm 生成配置文件的位置）上运行此命令。

   ```
   kubeadm init phase certs etcd-ca
   ```

   <!--
   This creates two files
   -->
   这一操作创建如下两个文件

   - `/etc/kubernetes/pki/etcd/ca.crt`
   - `/etc/kubernetes/pki/etcd/ca.key`

<!--
1. Create certificates for each member
-->
4. 为每个成员创建证书

   ```shell
   kubeadm init phase certs etcd-server --config=/tmp/${HOST2}/kubeadmcfg.yaml
   kubeadm init phase certs etcd-peer --config=/tmp/${HOST2}/kubeadmcfg.yaml
   kubeadm init phase certs etcd-healthcheck-client --config=/tmp/${HOST2}/kubeadmcfg.yaml
   kubeadm init phase certs apiserver-etcd-client --config=/tmp/${HOST2}/kubeadmcfg.yaml
   cp -R /etc/kubernetes/pki /tmp/${HOST2}/
   # 清理不可重复使用的证书
   find /etc/kubernetes/pki -not -name ca.crt -not -name ca.key -type f -delete

   kubeadm init phase certs etcd-server --config=/tmp/${HOST1}/kubeadmcfg.yaml
   kubeadm init phase certs etcd-peer --config=/tmp/${HOST1}/kubeadmcfg.yaml
   kubeadm init phase certs etcd-healthcheck-client --config=/tmp/${HOST1}/kubeadmcfg.yaml
   kubeadm init phase certs apiserver-etcd-client --config=/tmp/${HOST1}/kubeadmcfg.yaml
   cp -R /etc/kubernetes/pki /tmp/${HOST1}/
   find /etc/kubernetes/pki -not -name ca.crt -not -name ca.key -type f -delete

   kubeadm init phase certs etcd-server --config=/tmp/${HOST0}/kubeadmcfg.yaml
   kubeadm init phase certs etcd-peer --config=/tmp/${HOST0}/kubeadmcfg.yaml
   kubeadm init phase certs etcd-healthcheck-client --config=/tmp/${HOST0}/kubeadmcfg.yaml
   kubeadm init phase certs apiserver-etcd-client --config=/tmp/${HOST0}/kubeadmcfg.yaml
   # 不需要移动 certs 因为它们是给 HOST0 使用的

   # 清理不应从此主机复制的证书
   find /tmp/${HOST2} -name ca.key -type f -delete
   find /tmp/${HOST1} -name ca.key -type f -delete
   ```

<!--
1. Copy certificates and kubeadm configs
   The certificates have been generated and now they must be moved to their
   respective hosts.
-->
5. 复制证书和 kubeadm 配置

   证书已生成，现在必须将它们移动到对应的主机。

   ```shell
   USER=ubuntu
   HOST=${HOST1}
   scp -r /tmp/${HOST}/* ${USER}@${HOST}:
   ssh ${USER}@${HOST}
   USER@HOST $ sudo -Es
   root@HOST $ chown -R root:root pki
   root@HOST $ mv pki /etc/kubernetes/
   ```

<!--
1. Ensure all expected files exist

   The complete list of required files on `$HOST0` is:
-->
6. 确保已经所有预期的文件都存在

   `$HOST0` 所需文件的完整列表如下：

   ```none
   /tmp/${HOST0}
   └── kubeadmcfg.yaml
   ---
   /etc/kubernetes/pki
   ├── apiserver-etcd-client.crt
   ├── apiserver-etcd-client.key
   └── etcd
       ├── ca.crt
       ├── ca.key
       ├── healthcheck-client.crt
       ├── healthcheck-client.key
       ├── peer.crt
       ├── peer.key
       ├── server.crt
       └── server.key
   ```

   <!--
   On `$HOST1`:
   -->
   在 `$HOST1` 上：

   ```
   $HOME
   └── kubeadmcfg.yaml
   ---
   /etc/kubernetes/pki
   ├── apiserver-etcd-client.crt
   ├── apiserver-etcd-client.key
   └── etcd
       ├── ca.crt
       ├── healthcheck-client.crt
       ├── healthcheck-client.key
       ├── peer.crt
       ├── peer.key
       ├── server.crt
       └── server.key
   ```

   <!--
   On `$HOST2`
   -->
   在 `$HOST2` 上：

   ```
   $HOME
   └── kubeadmcfg.yaml
   ---
   /etc/kubernetes/pki
   ├── apiserver-etcd-client.crt
   ├── apiserver-etcd-client.key
   └── etcd
       ├── ca.crt
       ├── healthcheck-client.crt
       ├── healthcheck-client.key
       ├── peer.crt
       ├── peer.key
       ├── server.crt
       └── server.key
   ```

<!--
1. Create the static pod manifests

   Now that the certificates and configs are in place it's time to create the
   manifests. On each host run the `kubeadm` command to generate a static manifest
   for etcd.
-->
7. 创建静态 Pod 清单

   既然证书和配置已经就绪，是时候去创建清单了。
   在每台主机上运行 `kubeadm` 命令来生成 etcd 使用的静态清单。

   ```shell
   root@HOST0 $ kubeadm init phase etcd local --config=/tmp/${HOST0}/kubeadmcfg.yaml
   root@HOST1 $ kubeadm init phase etcd local --config=/tmp/${HOST1}/kubeadmcfg.yaml
   root@HOST2 $ kubeadm init phase etcd local --config=/tmp/${HOST2}/kubeadmcfg.yaml
   ```

<!--
1. Optional: Check the cluster health
-->
8. 可选：检查群集运行状况

   ```shell
   docker run --rm -it \
   --net host \
   -v /etc/kubernetes:/etc/kubernetes k8s.gcr.io/etcd:${ETCD_TAG} etcdctl \
   --cert /etc/kubernetes/pki/etcd/peer.crt \
   --key /etc/kubernetes/pki/etcd/peer.key \
   --cacert /etc/kubernetes/pki/etcd/ca.crt \
   --endpoints https://${HOST0}:2379 endpoint health --cluster
   ...
   https://[HOST0 IP]:2379 is healthy: successfully committed proposal: took = 16.283339ms
   https://[HOST1 IP]:2379 is healthy: successfully committed proposal: took = 19.44402ms
   https://[HOST2 IP]:2379 is healthy: successfully committed proposal: took = 35.926451ms
   ```
   <!--
   Set ${ETCD_TAG} to the version tag of your etcd image. For example 3.4.3-0. To see the etcd image and tag that             kubeadm uses execute kubeadm config images list --kubernetes-version ${K8S_VERSION}, where ${K8S_VERSION} is for           example v1.17.0
   Set ${HOST0}to the IP address of the host you are testing.
   -->
   - 将 `${ETCD_TAG}` 设置为你的 etcd 镜像的版本标签，例如 `3.4.3-0`。
     要查看 kubeadm 使用的 etcd 镜像和标签，请执行
     `kubeadm config images list --kubernetes-version ${K8S_VERSION}`，
     例如，其中的 `${K8S_VERSION}` 可以是 `v1.17.0`。
   - 将 `${HOST0}` 设置为要测试的主机的 IP 地址。

## {{% heading "whatsnext" %}}

<!--
Once your have a working 3 member etcd cluster, you can continue setting up a
highly available control plane using the [external etcd method with
kubeadm](/docs/setup/independent/high-availability/).
-->
一旦拥有了一个正常工作的 3 成员的 etcd 集群，你就可以基于
[使用 kubeadm 外部 etcd 的方法](/zh/docs/setup/production-environment/tools/kubeadm/high-availability/)，
继续部署一个高可用的控制平面。

