---
reviewers:
- jsafrane
- saad-ali
- msau42
- xing-yang
- pohly
title: Storage Capacity
content_type: concept
weight: 45
---

<!-- overview -->

Storage capacity is limited and may vary depending on the node on
which a pod runs: network-attached storage might not be accessible by
all nodes, or storage is local to a node to begin with.

{{< feature-state for_k8s_version="v1.19" state="alpha" >}}
{{< feature-state for_k8s_version="v1.21" state="beta" >}}

This page describes how Kubernetes keeps track of storage capacity and
how the scheduler uses that information to schedule Pods onto nodes
that have access to enough storage capacity for the remaining missing
volumes. Without storage capacity tracking, the scheduler may choose a
node that doesn't have enough capacity to provision a volume and
multiple scheduling retries will be needed.

Tracking storage capacity is supported for {{< glossary_tooltip
text="Container Storage Interface" term_id="csi" >}} (CSI) drivers and
[needs to be enabled](#enabling-storage-capacity-tracking) when installing a CSI driver.

<!-- body -->

## API

There are two API extensions for this feature:
- `CSIStorageCapacity` objects:
  these get produced by a CSI driver in the namespace
  where the driver is installed. Each object contains capacity
  information for one storage class and defines which nodes have
  access to that storage.
- The {{< api-reference page="config-and-storage-resources/csi-driver-v1" anchor="CSIDriverSpec" text="`CSIDriverSpec.StorageCapacity` field" >}}:
  when set to `true`, the Kubernetes scheduler will consider storage
  capacity for volumes that use the CSI driver.

## Scheduling

Storage capacity information is used by the Kubernetes scheduler if:
- the `CSIStorageCapacity` feature gate is true,
- a Pod uses a volume that has not been created yet,
- that volume uses a {{< glossary_tooltip text="StorageClass" term_id="storage-class" >}} which references a CSI driver and
  uses `WaitForFirstConsumer` [volume binding
  mode](/docs/concepts/storage/storage-classes/#volume-binding-mode),
  and
- the `CSIDriver` object for the driver has `StorageCapacity` set to
  true.

In that case, the scheduler only considers nodes for the Pod which
have enough storage available to them. This check is very
simplistic and only compares the size of the volume against the
capacity listed in `CSIStorageCapacity` objects with a topology that
includes the node.

For volumes with `Immediate` volume binding mode, the storage driver
decides where to create the volume, independently of Pods that will
use the volume. The scheduler then schedules Pods onto nodes where the
volume is available after the volume has been created.

For [CSI ephemeral volumes](/docs/concepts/storage/volumes/#csi),
scheduling always happens without considering storage capacity. This
is based on the assumption that this volume type is only used by
special CSI drivers which are local to a node and do not need
significant resources there.

## Rescheduling

When a node has been selected for a Pod with `WaitForFirstConsumer`
volumes, that decision is still tentative. The next step is that the
CSI storage driver gets asked to create the volume with a hint that the
volume is supposed to be available on the selected node.

Because Kubernetes might have chosen a node based on out-dated
capacity information, it is possible that the volume cannot really be
created. The node selection is then reset and the Kubernetes scheduler
tries again to find a node for the Pod.

## Limitations

Storage capacity tracking increases the chance that scheduling works
on the first try, but cannot guarantee this because the scheduler has
to decide based on potentially out-dated information. Usually, the
same retry mechanism as for scheduling without any storage capacity
information handles scheduling failures.

One situation where scheduling can fail permanently is when a Pod uses
multiple volumes: one volume might have been created already in a
topology segment which then does not have enough capacity left for
another volume. Manual intervention is necessary to recover from this,
for example by increasing capacity or deleting the volume that was
already created. [Further
work](https://github.com/kubernetes/enhancements/pull/1703) is needed
to handle this automatically.

## Enabling storage capacity tracking

Storage capacity tracking is a beta feature and enabled by default in
a Kubernetes cluster since Kubernetes 1.21. In addition to having the
feature enabled in the cluster, a CSI driver also has to support
it. Please refer to the driver's documentation for details.

## {{% heading "whatsnext" %}}

 - For more information on the design, see the
[Storage Capacity Constraints for Pod Scheduling KEP](https://github.com/kubernetes/enhancements/blob/master/keps/sig-storage/1472-storage-capacity-tracking/README.md).
- For more information on further development of this feature, see the [enhancement tracking issue #1472](https://github.com/kubernetes/enhancements/issues/1472).
- Learn about [Kubernetes Scheduler](/docs/concepts/scheduling-eviction/kube-scheduler/)
