---
reviewers:
- sig-api-machinery
- sig-architecture
- sig-cli
- sig-cluster-lifecycle
- sig-node
- sig-release
title: Kubernetes version and version skew support policy
content_type: concept
weight: 30
---

<!-- overview -->
This document describes the maximum version skew supported between various Kubernetes components.
Specific cluster deployment tools may place additional restrictions on version skew.


<!-- body -->

## Supported versions

Kubernetes versions are expressed as **x.y.z**,
where **x** is the major version, **y** is the minor version, and **z** is the patch version, following [Semantic Versioning](https://semver.org/) terminology.
For more information, see [Kubernetes Release Versioning](https://github.com/kubernetes/community/blob/master/contributors/design-proposals/release/versioning.md#kubernetes-release-versioning).

The Kubernetes project maintains release branches for the most recent three minor releases ({{< skew latestVersion >}}, {{< skew latestVersionAddMinor -1 >}}, {{< skew latestVersionAddMinor -2 >}}).  Kubernetes 1.19 and newer receive approximately 1 year of patch support. Kubernetes 1.18 and older received approximately 9 months of patch support.

Applicable fixes, including security fixes, may be backported to those three release branches, depending on severity and feasibility.
Patch releases are cut from those branches at a [regular cadence](https://git.k8s.io/sig-release/releases/patch-releases.md#cadence), plus additional urgent releases, when required.

The [Release Managers](https://git.k8s.io/sig-release/release-managers.md) group owns this decision.

For more information, see the Kubernetes [patch releases](https://git.k8s.io/sig-release/releases/patch-releases.md) page.

## Supported version skew

### kube-apiserver

In [highly-available (HA) clusters](/docs/setup/production-environment/tools/kubeadm/high-availability/), the newest and oldest `kube-apiserver` instances must be within one minor version.

Example:

* newest `kube-apiserver` is at **{{< skew currentVersion >}}**
* other `kube-apiserver` instances are supported at **{{< skew currentVersion >}}** and **{{< skew currentVersionAddMinor -1 >}}**

### kubelet

`kubelet` must not be newer than `kube-apiserver`, and may be up to two minor versions older.

Example:

* `kube-apiserver` is at **{{< skew currentVersion >}}**
* `kubelet` is supported at **{{< skew currentVersion >}}**, **{{< skew currentVersionAddMinor -1 >}}**, and **{{< skew currentVersionAddMinor -2 >}}**

{{< note >}}
If version skew exists between `kube-apiserver` instances in an HA cluster, this narrows the allowed `kubelet` versions.
{{</ note >}}

Example:

* `kube-apiserver` instances are at **{{< skew currentVersion >}}** and **{{< skew currentVersionAddMinor -1 >}}**
* `kubelet` is supported at **{{< skew currentVersionAddMinor -1 >}}**, and **{{< skew currentVersionAddMinor -2 >}}** (**{{< skew currentVersion >}}** is not supported because that would be newer than the `kube-apiserver` instance at version **{{< skew currentVersionAddMinor -1 >}}**)

### kube-controller-manager, kube-scheduler, and cloud-controller-manager

`kube-controller-manager`, `kube-scheduler`, and `cloud-controller-manager` must not be newer than the `kube-apiserver` instances they communicate with. They are expected to match the `kube-apiserver` minor version, but may be up to one minor version older (to allow live upgrades).

Example:

* `kube-apiserver` is at **{{< skew currentVersion >}}**
* `kube-controller-manager`, `kube-scheduler`, and `cloud-controller-manager` are supported at **{{< skew currentVersion >}}** and **{{< skew currentVersionAddMinor -1 >}}**

{{< note >}}
If version skew exists between `kube-apiserver` instances in an HA cluster, and these components can communicate with any `kube-apiserver` instance in the cluster (for example, via a load balancer), this narrows the allowed versions of these components.
{{< /note >}}

Example:

* `kube-apiserver` instances are at **{{< skew currentVersion >}}** and **{{< skew currentVersionAddMinor -1 >}}**
* `kube-controller-manager`, `kube-scheduler`, and `cloud-controller-manager` communicate with a load balancer that can route to any `kube-apiserver` instance
* `kube-controller-manager`, `kube-scheduler`, and `cloud-controller-manager` are supported at **{{< skew currentVersionAddMinor -1 >}}** (**{{< skew currentVersion >}}** is not supported because that would be newer than the `kube-apiserver` instance at version **{{< skew currentVersionAddMinor -1 >}}**)

### kubectl

`kubectl` is supported within one minor version (older or newer) of `kube-apiserver`.

Example:

* `kube-apiserver` is at **{{< skew currentVersion >}}**
* `kubectl` is supported at **{{< skew nextMinorVersion >}}**, **{{< skew currentVersion >}}**, and **{{< skew currentVersionAddMinor -1 >}}**

{{< note >}}
If version skew exists between `kube-apiserver` instances in an HA cluster, this narrows the supported `kubectl` versions.
{{< /note >}}

Example:

* `kube-apiserver` instances are at **{{< skew currentVersion >}}** and **{{< skew currentVersionAddMinor -1 >}}**
* `kubectl` is supported at **{{< skew currentVersion >}}** and **{{< skew currentVersionAddMinor -1 >}}** (other versions would be more than one minor version skewed from one of the `kube-apiserver` components)

## Supported component upgrade order

The supported version skew between components has implications on the order in which components must be upgraded.
This section describes the order in which components must be upgraded to transition an existing cluster from version **{{< skew currentVersionAddMinor -1 >}}** to version **{{< skew currentVersion >}}**.

### kube-apiserver

Pre-requisites:

* In a single-instance cluster, the existing `kube-apiserver` instance is **{{< skew currentVersionAddMinor -1 >}}**
* In an HA cluster, all `kube-apiserver` instances are at **{{< skew currentVersionAddMinor -1 >}}** or **{{< skew currentVersion >}}** (this ensures maximum skew of 1 minor version between the oldest and newest `kube-apiserver` instance)
* The `kube-controller-manager`, `kube-scheduler`, and `cloud-controller-manager` instances that communicate with this server are at version **{{< skew currentVersionAddMinor -1 >}}** (this ensures they are not newer than the existing API server version, and are within 1 minor version of the new API server version)
* `kubelet` instances on all nodes are at version **{{< skew currentVersionAddMinor -1 >}}** or **{{< skew currentVersionAddMinor -2 >}}** (this ensures they are not newer than the existing API server version, and are within 2 minor versions of the new API server version)
* Registered admission webhooks are able to handle the data the new `kube-apiserver` instance will send them:
  * `ValidatingWebhookConfiguration` and `MutatingWebhookConfiguration` objects are updated to include any new versions of REST resources added in **{{< skew currentVersion >}}** (or use the [`matchPolicy: Equivalent` option](/docs/reference/access-authn-authz/extensible-admission-controllers/#matching-requests-matchpolicy) available in v1.15+)
  * The webhooks are able to handle any new versions of REST resources that will be sent to them, and any new fields added to existing versions in **{{< skew currentVersion >}}**

Upgrade `kube-apiserver` to **{{< skew currentVersion >}}**

{{< note >}}
Project policies for [API deprecation](/docs/reference/using-api/deprecation-policy/) and
[API change guidelines](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api_changes.md)
require `kube-apiserver` to not skip minor versions when upgrading, even in single-instance clusters.
{{< /note >}}

### kube-controller-manager, kube-scheduler, and cloud-controller-manager

Pre-requisites:

* The `kube-apiserver` instances these components communicate with are at **{{< skew currentVersion >}}** (in HA clusters in which these control plane components can communicate with any `kube-apiserver` instance in the cluster, all `kube-apiserver` instances must be upgraded before upgrading these components)

Upgrade `kube-controller-manager`, `kube-scheduler`, and `cloud-controller-manager` to **{{< skew currentVersion >}}**

### kubelet

Pre-requisites:

* The `kube-apiserver` instances the `kubelet` communicates with are at **{{< skew currentVersion >}}**

Optionally upgrade `kubelet` instances to **{{< skew currentVersion >}}** (or they can be left at **{{< skew currentVersionAddMinor -1 >}}** or **{{< skew currentVersionAddMinor -2 >}}**)

{{< note >}}
Before performing a minor version `kubelet` upgrade, [drain](/docs/tasks/administer-cluster/safely-drain-node/) pods from that node.
In-place minor version `kubelet` upgrades are not supported.
{{</ note >}}

{{< warning >}}
Running a cluster with `kubelet` instances that are persistently two minor versions behind `kube-apiserver` is not recommended:

* they must be upgraded within one minor version of `kube-apiserver` before the control plane can be upgraded
* it increases the likelihood of running `kubelet` versions older than the three maintained minor releases
{{</ warning >}}

### kube-proxy

* `kube-proxy` must be the same minor version as `kubelet` on the node.
* `kube-proxy` must not be newer than `kube-apiserver`.
* `kube-proxy` must be at most two minor versions older than `kube-apiserver.`

Example:

If `kube-proxy` version is **{{< skew currentVersionAddMinor -2 >}}**:

* `kubelet` version must be at the same minor version as **{{< skew currentVersionAddMinor -2 >}}**.
* `kube-apiserver` version must be between **{{< skew currentVersionAddMinor -2 >}}** and **{{< skew currentVersion >}}**, inclusive.
