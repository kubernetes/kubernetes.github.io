---
title: Running Kubernetes node components as a non-root user (`KubeletInUserNamespace`)
content_type: task
min-kubernetes-server-version: 1.22
---

<!-- overview -->

{{< feature-state for_k8s_version="v1.22" state="alpha" >}}

This document describes how to run Kubernetes node components such as kubelet, CRI, OCI, and CNI
without root privileges, by using a {{< glossary_tooltip text="user namespace" term_id="userns" >}}.

This technique is also known as _rootless mode_.

{{< note >}}
This document describes how to run Kubernetes node components (and hence pods) a non-root user.

If you are just looking for how to run a pod as a non-root user, see [SecurityContext](/docs/tasks/configure-pod-container/security-context/).
{{< /note >}}

## {{% heading "prerequisites" %}}

* [cgroup v2](https://rootlesscontaine.rs/getting-started/common/cgroup2/)
* [systemd with user session](https://rootlesscontaine.rs/getting-started/common/login/)
* [several sysctl values, depending on host Linux distribution](https://rootlesscontaine.rs/getting-started/common/sysctl/)
* [`/etc/subuid` and `/etc/subgid`](https://rootlesscontaine.rs/getting-started/common/subuid/)

* [`KubeletInUserNamespace` feature gate](/docs/reference/command-line-tools-reference/feature-gates/)

<!-- steps -->

## Running Kubernetes inside Rootless Docker/Podman

[kind](https://kind.sigs.k8s.io/) supports running Kubernetes inside a Rootless Docker or Rootless Podman.

See [Running kind with Rootless Docker](https://kind.sigs.k8s.io/docs/user/rootless/).

[minikube](https://minikube.sigs.k8s.io/docs/) also plans to support Rootless Docker/Podman drivers.
See [minikube issue #10836](https://github.com/kubernetes/minikube/issues/10836) to track the progress.

## Running Rootless Kubernetes directly on a host

{{% thirdparty-content %}}

### K3s

[K3s](https://k3s.io/) experimentally supports rootless mode.

See [Running K3s with Rootless mode](https://rancher.com/docs/k3s/latest/en/advanced/#running-k3s-with-rootless-mode-experimental) for the usage.

### Usernetes
[Usernetes](https://github.com/rootless-containers/usernetes) is a reference distribution of Kubernetes that can be installed under `$HOME` directory without the root privilege.

Usernetes supports both containerd and CRI-O as CRI runtimes.
Usernetes supports multi-node clusters using Flannel (VXLAN).

See [the Usernetes repo](https://github.com/rootless-containers/usernetes) for the usage.

## "Hard way"

This section provides hints for running Kubernetes in a user namespace manually.

{{< note >}}
This section is intended to be read by developers of Kubernetes distributions, not by end users.
{{< /note >}}

### Creating a user namespace

{{% thirdparty-content %}}

The first step is to create a {{< glossary_tooltip text="user namespace" term_id="userns" >}}.

If you are trying to run Kubernetes in a user-namespaced container such as
Rootless Docker/Podman or LXC/LXD, you are all set, and you can go to the next subsection.

Otherwise you have to create a user namespace by yourself, by calling `unshare(2)` with `CLONE_NEWUSER`.

A user namespace can be also unshared by using command line tools such as:
- [RootlessKit](https://github.com/rootless-containers/rootlesskit)
- [become-root](https://github.com/giuseppe/become-root)
- [`unshare(1)`](https://man7.org/linux/man-pages/man1/unshare.1.html)

After unsharing the user namespace, you will also have to unshare other namespaces such as mount namespace.

You do *not* need to call `chroot(2)` nor `pivot_root(2)` after unsharing the mount namespace,
however, you have to mount writable filesystems on several directories *in* the namespace.

At least, the following directories need to be writable *in* the namespace (not *outside* the namespace):

- `/etc`
- `/run`
- `/var/logs`
- `/var/lib/kubelet`
- `/var/lib/cni`
- `/var/lib/containerd` (for containerd)
- `/var/lib/containers` (for CRI-O)

### Creating a delegated cgroup tree

In addition to the user namespace, you also need to have a writable cgroup tree with cgroup v2.
Note that cgroup v1 is not supported.

If you are trying to run Kubernetes in Rootless Docker/Podman or LXC/LXD on a systemd-based host, you are all set.

Otherwise you have to create a systemd unit with `Delegate=yes` property to delegate a cgroup tree with writable permission.

Systemd has to be configured to allow delegation, see https://rootlesscontaine.rs/getting-started/common/cgroup2/ .

### Configuring network
{{% thirdparty-content %}}

Ports such as the kubelet port (10250/TCP) and `NodePort` service ports have to be exposed from the network namespace to
the host with an external port forwarder, such as RootlessKit, slirp4netns, or socat.

K3s implementation of port forwarder can be found at https://github.com/k3s-io/k3s/blob/v1.21.2+k3s1/pkg/rootlessports/controller.go

For multi-node networking, Flannel (VXLAN, 8472/UDP) is known to work.

### Configuring CRI

Before running kubelet, you have to run a CRI runtime such as containerd or CRI-O in the namespace and the cgroup tree.

#### containerd

Running CRI plugin of containerd in a user namespace is supported since containerd 1.4.

Running containerd in a user namespace requires the following configuration:

```toml
version = 2

[plugins."io.containerd.grpc.v1.cri"]
# Disable AppArmor
  disable_apparmor = true
# Ignore an error during setting oom_score_adj
  restrict_oom_score_adj = true
# Disable hugetlb cgroup v2 controller (because systemd does not support delegating hugetlb controller)
  disable_hugetlb_controller = true

[plugins."io.containerd.grpc.v1.cri".containerd]
# Using non-fuse overlayfs is also possible for kernel >= 5.11, but requires SELinux to be disabled
  snapshotter = "fuse-overlayfs"

[plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc.options]
# We use cgroupfs that is delegated by systemd, so we do not use SystemdCgroup driver
# (unless you run another systemd in the namespace)
  SystemdCgroup = false
```

#### CRI-O

Running CRI-O in a user namespace is supported since CRI-O 1.22.

CRI-O requires an environment variable `_CRIO_ROOTLESS=1` to be set.

The following configuration is also recommended:

```toml
[crio]
  storage_driver = "overlay"
# Using non-fuse overlayfs is also possible for kernel >= 5.11, but requires SELinux to be disabled
  storage_option = ["overlay.mount_program=/usr/local/bin/fuse-overlayfs"]

[crio.runtime]
# We use cgroupfs that is delegated by systemd, so we do not use "systemd" driver
# (unless you run another systemd in the namespace)
  cgroup_manager = "cgroupfs"
```

### Configuring kubelet

Running kubelet in a user namespace requires the following configuration:

```yaml
kind: KubeletConfiguration
apiVersion: kubelet.config.k8s.io/v1beta1
featureGates:
  KubeletInUserNamespace: true
# We use cgroupfs that is delegated by systemd, so we do not use "systemd" driver
# (unless you run another systemd in the namespace)
cgroupDriver: "cgroupfs"
```

When the `KubeletInUserNamespace` feature gate is enabled, kubelet ignores errors that may happen during setting the following sysctl values:
- `vm.overcommit_memory`
- `vm.panic_on_oom`
- `kernel.panic`
- `kernel.panic_on_oops`
- `kernel.keys.root_maxkeys`
- `kernel.keys.root_maxbytes`.
   (these sysctl values for the host, not for the containers).

Kubelet also ignores an error during opening `/dev/kmsg`.
This feature gate also allows kube-proxy to ignore an error during setting `RLIMIT_NOFILE`.

The `KubeletInUserNamespace` feature gate was introduced in Kubernetes v1.22 with "alpha" status.

Running kubelet in a user namespace without using this feature gate is also possible by mounting a specially crafted proc filesystem,
but not officially supported.
Actually, `kind` v0.11 supports running Kubernetes v1.21 in a Rootless Docker/Podman container without using the feature gate, but the
behavior will change in a future version of `kind` that supports Kubernetes v1.22.

### Configuring kube-proxy

Running kube-proxy in a user namespace requires the following configuration:

```yaml
apiVersion: kubeproxy.config.k8s.io/v1alpha1
kind: KubeProxyConfiguration
mode: "iptables" # or "userspace"
conntrack:
# Skip setting sysctl value "net.netfilter.nf_conntrack_max"
  maxPerCore: 0
# Skip setting "net.netfilter.nf_conntrack_tcp_timeout_established"
  tcpEstablishedTimeout: 0s
# Skip setting "net.netfilter.nf_conntrack_tcp_timeout_close"
  tcpCloseWaitTimeout: 0s
```

## Caveats

- Most of "non-local" volume drivers such as `nfs` and `iscsi` do not work.
  Local volumes like `local`, `hostPath`, `emptyDir`, `configMap`, `secret`, and `downwardAPI` are known to work.

- Some CNI plugins may not work. Flannel (VXLAN) is known to work.

See also ["Caveats and Future work" page of rootlesscontaine.rs](https://rootlesscontaine.rs/caveats/).

## {{% heading "seealso" %}}
- [rootlesscontaine.rs](https://rootlesscontaine.rs/)
- [Rootless Containers 2020 (KubeCon NA 2020)](https://www.slideshare.net/AkihiroSuda/kubecon-na-2020-containerd-rootless-containers-2020)
- [Running kind with Rootless Docker](https://kind.sigs.k8s.io/docs/user/rootless/)
- [Usernetes](https://github.com/rootless-containers/usernetes)
- [Running K3s with rootless mode](https://rancher.com/docs/k3s/latest/en/advanced/#running-k3s-with-rootless-mode-experimental)
- [KEP-2033: Kubelet-in-UserNS (aka Rootless mode)](https://github.com/kubernetes/enhancements/tree/master/keps/sig-node/2033-kubelet-in-userns-aka-rootless)
