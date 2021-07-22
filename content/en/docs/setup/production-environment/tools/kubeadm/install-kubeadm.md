---
title: Installing kubeadm
content_type: task
weight: 10
card:
  name: setup
  weight: 20
  title: Install the kubeadm setup tool
---

<!-- overview -->

<img src="https://raw.githubusercontent.com/kubernetes/kubeadm/master/logos/stacked/color/kubeadm-stacked-color.png" align="right" width="150px">This page shows how to install the `kubeadm` toolbox.
For information on how to create a cluster with kubeadm once you have performed this installation process, see the [Using kubeadm to Create a Cluster](/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/) page.



## {{% heading "prerequisites" %}}


* A compatible Linux host. The Kubernetes project provides generic instructions for Linux distributions based on Debian and Red Hat, and those distributions without a package manager.
* 2 GB or more of RAM per machine (any less will leave little room for your apps).
* 2 CPUs or more.
* Full network connectivity between all machines in the cluster (public or private network is fine).
* Unique hostname, MAC address, and product_uuid for every node. See [here](#verify-mac-address) for more details.
* Certain ports are open on your machines. See [here](#check-required-ports) for more details.
* Swap disabled. You **MUST** disable swap in order for the kubelet to work properly.



<!-- steps -->

## Verify the MAC address and product_uuid are unique for every node {#verify-mac-address}

* You can get the MAC address of the network interfaces using the command `ip link` or `ifconfig -a`
* The product_uuid can be checked by using the command `sudo cat /sys/class/dmi/id/product_uuid`

It is very likely that hardware devices will have unique addresses, although some virtual machines may have
identical values. Kubernetes uses these values to uniquely identify the nodes in the cluster.
If these values are not unique to each node, the installation process
may [fail](https://github.com/kubernetes/kubeadm/issues/31).

## Check network adapters

If you have more than one network adapter, and your Kubernetes components are not reachable on the default
route, we recommend you add IP route(s) so Kubernetes cluster addresses go via the appropriate adapter.

## Letting iptables see bridged traffic

Make sure that the `br_netfilter` module is loaded. This can be done by running `lsmod | grep br_netfilter`. To load it explicitly call `sudo modprobe br_netfilter`.

As a requirement for your Linux Node's iptables to correctly see bridged traffic, you should ensure `net.bridge.bridge-nf-call-iptables` is set to 1 in your `sysctl` config, e.g.

```bash
cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
br_netfilter
EOF

cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
EOF
sudo sysctl --system
```

For more details please see the [Network Plugin Requirements](/docs/concepts/extend-kubernetes/compute-storage-net/network-plugins/#network-plugin-requirements) page.

## Check required ports

### Control-plane node(s)

| Protocol | Direction | Port Range | Purpose                 | Used By                   |
|----------|-----------|------------|-------------------------|---------------------------|
| TCP      | Inbound   | 6443\*      | Kubernetes API server   | All                       |
| TCP      | Inbound   | 2379-2380  | etcd server client API  | kube-apiserver, etcd      |
| TCP      | Inbound   | 10250      | kubelet API             | Self, Control plane       |
| TCP      | Inbound   | 10251      | kube-scheduler          | Self                      |
| TCP      | Inbound   | 10252      | kube-controller-manager | Self                      |

### Worker node(s)

| Protocol | Direction | Port Range  | Purpose               | Used By                 |
|----------|-----------|-------------|-----------------------|-------------------------|
| TCP      | Inbound   | 10250       | kubelet API           | Self, Control plane     |
| TCP      | Inbound   | 30000-32767 | NodePort Services†    | All                     |

† Default port range for [NodePort Services](/docs/concepts/services-networking/service/).

Any port numbers marked with * are overridable, so you will need to ensure any
custom ports you provide are also open.

Although etcd ports are included in control-plane nodes, you can also host your own
etcd cluster externally or on custom ports.

The pod network plugin you use (see below) may also require certain ports to be
open. Since this differs with each pod network plugin, please see the
documentation for the plugins about what port(s) those need.

## Installing runtime {#installing-runtime}

To run containers in Pods, Kubernetes uses a
{{< glossary_tooltip term_id="container-runtime" text="container runtime" >}}.

{{< tabs name="container_runtime" >}}
{{% tab name="Linux nodes" %}}

By default, Kubernetes uses the
{{< glossary_tooltip term_id="cri" text="Container Runtime Interface">}} (CRI)
to interface with your chosen container runtime.

If you don't specify a runtime, kubeadm automatically tries to detect an installed
container runtime by scanning through a list of well known Unix domain sockets.
The following table lists container runtimes and their associated socket paths:

{{< table caption = "Container runtimes and their socket paths" >}}
| Runtime    | Path to Unix domain socket        |
|------------|-----------------------------------|
| Docker     | `/var/run/dockershim.sock`        |
| containerd | `/run/containerd/containerd.sock` |
| CRI-O      | `/var/run/crio/crio.sock`         |
{{< /table >}}

<br />
If both Docker and containerd are detected, Docker takes precedence. This is
needed because Docker 18.09 ships with containerd and both are detectable even if you only
installed Docker.
If any other two or more runtimes are detected, kubeadm exits with an error.

The kubelet integrates with Docker through the built-in `dockershim` CRI implementation.

See [container runtimes](/docs/setup/production-environment/container-runtimes/)
for more information.
{{% /tab %}}
{{% tab name="other operating systems" %}}
By default, kubeadm uses {{< glossary_tooltip term_id="docker" >}} as the container runtime.
The kubelet integrates with Docker through the built-in `dockershim` CRI implementation.

See [container runtimes](/docs/setup/production-environment/container-runtimes/)
for more information.
{{% /tab %}}
{{< /tabs >}}


## Installing kubeadm, kubelet and kubectl

You will install these packages on all of your machines:

* `kubeadm`: the command to bootstrap the cluster.

* `kubelet`: the component that runs on all of the machines in your cluster
    and does things like starting pods and containers.

* `kubectl`: the command line util to talk to your cluster.

kubeadm **will not** install or manage `kubelet` or `kubectl` for you, so you will
need to ensure they match the version of the Kubernetes control plane you want
kubeadm to install for you. If you do not, there is a risk of a version skew occurring that
can lead to unexpected, buggy behaviour. However, _one_ minor version skew between the
kubelet and the control plane is supported, but the kubelet version may never exceed the API
server version. For example, the kubelet running 1.7.0 should be fully compatible with a 1.8.0 API server,
but not vice versa.

For information about installing `kubectl`, see [Install and set up kubectl](/docs/tasks/tools/).

{{< warning >}}
These instructions exclude all Kubernetes packages from any system upgrades.
This is because kubeadm and Kubernetes require
[special attention to upgrade](/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/).
{{</ warning >}}

For more information on version skews, see:

* Kubernetes [version and version-skew policy](/docs/setup/release/version-skew-policy/)
* Kubeadm-specific [version skew policy](/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/#version-skew-policy)

{{< tabs name="k8s_install" >}}
{{% tab name="Debian-based distributions" %}}

1. Update the `apt` package index and install packages needed to use the Kubernetes `apt` repository:

   ```shell
   sudo apt-get update
   sudo apt-get install -y apt-transport-https ca-certificates curl
   ```

2. Download the Google Cloud public signing key:

   ```shell
   sudo curl -fsSLo /usr/share/keyrings/kubernetes-archive-keyring.gpg https://packages.cloud.google.com/apt/doc/apt-key.gpg
   ```

3. Add the Kubernetes `apt` repository:

   ```shell
   echo "deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list
   ```

4. Update `apt` package index, install kubelet, kubeadm and kubectl, and pin their version:

   ```shell
   sudo apt-get update
   sudo apt-get install -y kubelet kubeadm kubectl
   sudo apt-mark hold kubelet kubeadm kubectl
   ```

{{% /tab %}}
{{% tab name="Red Hat-based distributions" %}}
```bash
cat <<EOF | sudo tee /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-\$basearch
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
exclude=kubelet kubeadm kubectl
EOF

# Set SELinux in permissive mode (effectively disabling it)
sudo setenforce 0
sudo sed -i 's/^SELINUX=enforcing$/SELINUX=permissive/' /etc/selinux/config

sudo yum install -y kubelet kubeadm kubectl --disableexcludes=kubernetes

sudo systemctl enable --now kubelet
```

  **Notes:**

  - Setting SELinux in permissive mode by running `setenforce 0` and `sed ...` effectively disables it.
    This is required to allow containers to access the host filesystem, which is needed by pod networks for example.
    You have to do this until SELinux support is improved in the kubelet.

  - You can leave SELinux enabled if you know how to configure it but it may require settings that are not supported by kubeadm.

{{% /tab %}}
{{% tab name="Without a package manager" %}}
Install CNI plugins (required for most pod network):

```bash
CNI_VERSION="v0.8.2"
ARCH="amd64"
sudo mkdir -p /opt/cni/bin
curl -L "https://github.com/containernetworking/plugins/releases/download/${CNI_VERSION}/cni-plugins-linux-${ARCH}-${CNI_VERSION}.tgz" | sudo tar -C /opt/cni/bin -xz
```

Define the directory to download command files

{{< note >}}
The `DOWNLOAD_DIR` variable must be set to a writable directory.
If you are running Flatcar Container Linux, set `DOWNLOAD_DIR=/opt/bin`.
{{< /note >}}

```bash
DOWNLOAD_DIR=/usr/local/bin
sudo mkdir -p $DOWNLOAD_DIR
```

Install crictl (required for kubeadm / Kubelet Container Runtime Interface (CRI))

```bash
CRICTL_VERSION="v1.17.0"
ARCH="amd64"
curl -L "https://github.com/kubernetes-sigs/cri-tools/releases/download/${CRICTL_VERSION}/crictl-${CRICTL_VERSION}-linux-${ARCH}.tar.gz" | sudo tar -C $DOWNLOAD_DIR -xz
```

Install `kubeadm`, `kubelet`, `kubectl` and add a `kubelet` systemd service:

```bash
RELEASE="$(curl -sSL https://dl.k8s.io/release/stable.txt)"
ARCH="amd64"
cd $DOWNLOAD_DIR
sudo curl -L --remote-name-all https://storage.googleapis.com/kubernetes-release/release/${RELEASE}/bin/linux/${ARCH}/{kubeadm,kubelet,kubectl}
sudo chmod +x {kubeadm,kubelet,kubectl}

RELEASE_VERSION="v0.4.0"
curl -sSL "https://raw.githubusercontent.com/kubernetes/release/${RELEASE_VERSION}/cmd/kubepkg/templates/latest/deb/kubelet/lib/systemd/system/kubelet.service" | sed "s:/usr/bin:${DOWNLOAD_DIR}:g" | sudo tee /etc/systemd/system/kubelet.service
sudo mkdir -p /etc/systemd/system/kubelet.service.d
curl -sSL "https://raw.githubusercontent.com/kubernetes/release/${RELEASE_VERSION}/cmd/kubepkg/templates/latest/deb/kubeadm/10-kubeadm.conf" | sed "s:/usr/bin:${DOWNLOAD_DIR}:g" | sudo tee /etc/systemd/system/kubelet.service.d/10-kubeadm.conf
```

Enable and start `kubelet`:

```bash
systemctl enable --now kubelet
```

{{< note >}}
The Flatcar Container Linux distribution mounts the `/usr` directory as a read-only filesystem.
Before bootstrapping your cluster, you need to take additional steps to configure a writable directory.
See the [Kubeadm Troubleshooting guide](/docs/setup/production-environment/tools/kubeadm/troubleshooting-kubeadm/#usr-mounted-read-only/) to learn how to set up a writable directory.
{{< /note >}}
{{% /tab %}}
{{< /tabs >}}


The kubelet is now restarting every few seconds, as it waits in a crashloop for
kubeadm to tell it what to do.

## Configuring a cgroup driver

Both the container runtime and the kubelet have a property called
["cgroup driver"](/docs/setup/production-environment/container-runtimes/), which is important
for the management of cgroups on Linux machines.

{{< warning >}}
Matching the container runtime and kubelet cgroup drivers is required or otherwise the kubelet process will fail.

See [Configuring a cgroup driver](/docs/tasks/administer-cluster/kubeadm/configure-cgroup-driver/) for more details.
{{< /warning >}}

## Troubleshooting

If you are running into difficulties with kubeadm, please consult our [troubleshooting docs](/docs/setup/production-environment/tools/kubeadm/troubleshooting-kubeadm/).

## {{% heading "whatsnext" %}}

* [Using kubeadm to Create a Cluster](/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/)
