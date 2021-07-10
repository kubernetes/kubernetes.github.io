---
reviewers:
- jsafrane
- saad-ali
- msau42
- xing-yang
- pohly
title: Ephemeral Volumes
content_type: concept
weight: 50
---

<!-- overview -->

This document describes _ephemeral volumes_ in Kubernetes. Familiarity
with [volumes](/docs/concepts/storage/volumes/) is suggested, in
particular PersistentVolumeClaim and PersistentVolume.

<!-- body -->

Some application need additional storage but don't care whether that
data is stored persistently across restarts. For example, caching
services are often limited by memory size and can move infrequently
used data into storage that is slower than memory with little impact
on overall performance.

Other applications expect some read-only input data to be present in
files, like configuration data or secret keys.

_Ephemeral volumes_ are designed for these use cases. Because volumes
follow the Pod's lifetime and get created and deleted along with the
Pod, Pods can be stopped and restarted without being limited to where
some persistent volume is available.

Ephemeral volumes are specified _inline_ in the Pod spec, which
simplifies application deployment and management.

### Types of ephemeral volumes

Kubernetes supports several different kinds of ephemeral volumes for
different purposes:
- [emptyDir](/docs/concepts/storage/volumes/#emptydir): empty at Pod startup,
  with storage coming locally from the kubelet base directory (usually
  the root disk) or RAM
- [configMap](/docs/concepts/storage/volumes/#configmap),
  [downwardAPI](/docs/concepts/storage/volumes/#downwardapi),
  [secret](/docs/concepts/storage/volumes/#secret): inject different
  kinds of Kubernetes data into a Pod
- [CSI ephemeral volumes](#csi-ephemeral-volumes):
  similar to the previous volume kinds, but provided by special
  [CSI drivers](https://github.com/container-storage-interface/spec/blob/master/spec.md)
  which specifically [support this feature](https://kubernetes-csi.github.io/docs/drivers.html)
- [generic ephemeral volumes](#generic-ephemeral-volumes), which
  can be provided by all storage drivers that also support persistent volumes

`emptyDir`, `configMap`, `downwardAPI`, `secret` are provided as
[local ephemeral
storage](/docs/concepts/configuration/manage-resources-containers/#local-ephemeral-storage).
They are managed by kubelet on each node.

CSI ephemeral volumes *must* be provided by third-party CSI storage
drivers.

Generic ephemeral volumes *can* be provided by third-party CSI storage
drivers, but also by any other storage driver that supports dynamic
provisioning. Some CSI drivers are written specifically for CSI
ephemeral volumes and do not support dynamic provisioning: those then
cannot be used for generic ephemeral volumes.

The advantage of using third-party drivers is that they can offer
functionality that Kubernetes itself does not support, for example
storage with different performance characteristics than the disk that
is managed by kubelet, or injecting different data.

### CSI ephemeral volumes

{{< feature-state for_k8s_version="v1.16" state="beta" >}}

This feature requires the `CSIInlineVolume` [feature gate](/docs/reference/command-line-tools-reference/feature-gates/) to be enabled. It
is enabled by default starting with Kubernetes 1.16.

{{< note >}}
CSI ephemeral volumes are only supported by a subset of CSI drivers.
The Kubernetes CSI [Drivers list](https://kubernetes-csi.github.io/docs/drivers.html)
shows which drivers support ephemeral volumes.
{{< /note >}}

Conceptually, CSI ephemeral volumes are similar to `configMap`,
`downwardAPI` and `secret` volume types: the storage is managed locally on each
 node and is created together with other local resources after a Pod has been
scheduled onto a node. Kubernetes has no concept of rescheduling Pods
anymore at this stage. Volume creation has to be unlikely to fail,
otherwise Pod startup gets stuck. In particular, [storage capacity
aware Pod scheduling](/docs/concepts/storage/storage-capacity/) is *not*
supported for these volumes. They are currently also not covered by
the storage resource usage limits of a Pod, because that is something
that kubelet can only enforce for storage that it manages itself.


Here's an example manifest for a Pod that uses CSI ephemeral storage:

```yaml
kind: Pod
apiVersion: v1
metadata:
  name: my-csi-app
spec:
  containers:
    - name: my-frontend
      image: busybox
      volumeMounts:
      - mountPath: "/data"
        name: my-csi-inline-vol
      command: [ "sleep", "1000000" ]
  volumes:
    - name: my-csi-inline-vol
      csi:
        driver: inline.storage.kubernetes.io
        volumeAttributes:
          foo: bar
```

The `volumeAttributes` determine what volume is prepared by the
driver. These attributes are specific to each driver and not
standardized. See the documentation of each CSI driver for further
instructions.

As a cluster administrator, you can use a [PodSecurityPolicy](/docs/concepts/policy/pod-security-policy/) to control which CSI drivers can be used in a Pod, specified with the {{< api-reference page="policy-resources/pod-security-policy-v1beta1" anchor="AllowedCSIDriver" text="`allowedCSIDrivers` field">}} structure.

### Generic ephemeral volumes

{{< feature-state for_k8s_version="v1.21" state="beta" >}}

This feature requires the `GenericEphemeralVolume` [feature gate](/docs/reference/command-line-tools-reference/feature-gates/) to be
enabled. Because this is a beta feature, it is enabled by default.

Generic ephemeral volumes are similar to `emptyDir` volumes in the
sense that they provide a per-pod directory for scratch data that is
usually empty after provisioning. But they may also have additional
features:

- Storage can be local or network-attached.
- Volumes can have a fixed size that Pods are not able to exceed.
- Volumes may have some initial data, depending on the driver and
  parameters.
- Typical operations on volumes are supported assuming that the driver
  supports them, including
  ([snapshotting](/docs/concepts/storage/volume-snapshots/),
  [cloning](/docs/concepts/storage/volume-pvc-datasource/),
  [resizing](/docs/concepts/storage/persistent-volumes/#expanding-persistent-volumes-claims),
  and [storage capacity tracking](/docs/concepts/storage/storage-capacity/).

Example:

```yaml
kind: Pod
apiVersion: v1
metadata:
  name: my-app
spec:
  containers:
    - name: my-frontend
      image: busybox
      volumeMounts:
      - mountPath: "/scratch"
        name: scratch-volume
      command: [ "sleep", "1000000" ]
  volumes:
    - name: scratch-volume
      ephemeral:
        volumeClaimTemplate:
          metadata:
            labels:
              type: my-frontend-volume
          spec:
            accessModes: [ "ReadWriteOnce" ]
            storageClassName: "scratch-storage-class"
            resources:
              requests:
                storage: 1Gi
```

### Lifecycle and PersistentVolumeClaim

The key design idea is that the
{{< api-reference page="config-and-storage-resources/volume" anchor="EphemeralVolumeSource" text="parameters for a volume claim" >}}
are allowed inside a volume source of the Pod. Labels, annotations and
the whole set of fields for a PersistentVolumeClaim are supported. When such a Pod gets
created, the ephemeral volume controller then creates an actual PersistentVolumeClaim
object in the same namespace as the Pod and ensures that the PersistentVolumeClaim
gets deleted when the Pod gets deleted.

That triggers volume binding and/or provisioning, either immediately if
the {{< glossary_tooltip text="StorageClass" term_id="storage-class" >}} uses immediate volume binding or when the Pod is
tentatively scheduled onto a node (`WaitForFirstConsumer` volume
binding mode). The latter is recommended for generic ephemeral volumes
because then the scheduler is free to choose a suitable node for
the Pod. With immediate binding, the scheduler is forced to select a node that has
access to the volume once it is available.

In terms of [resource ownership](/docs/concepts/workloads/controllers/garbage-collection/#owners-and-dependents),
a Pod that has generic ephemeral storage is the owner of the PersistentVolumeClaim(s)
that provide that ephemeral storage. When the Pod is deleted,
the Kubernetes garbage collector deletes the PVC, which then usually
triggers deletion of the volume because the default reclaim policy of
storage classes is to delete volumes. You can create quasi-ephemeral local storage
using a StorageClass with a reclaim policy of `retain`: the storage outlives the Pod, 
and in this case you need to ensure that volume clean up happens separately.

While these PVCs exist, they can be used like any other PVC. In
particular, they can be referenced as data source in volume cloning or
snapshotting. The PVC object also holds the current status of the
volume.

### PersistentVolumeClaim naming

Naming of the automatically created PVCs is deterministic: the name is
a combination of Pod name and volume name, with a hyphen (`-`) in the
middle. In the example above, the PVC name will be
`my-app-scratch-volume`.  This deterministic naming makes it easier to
interact with the PVC because one does not have to search for it once
the Pod name and volume name are known.

The deterministic naming also introduces a potential conflict between different
Pods (a Pod "pod-a" with volume "scratch" and another Pod with name
"pod" and volume "a-scratch" both end up with the same PVC name
"pod-a-scratch") and between Pods and manually created PVCs.

Such conflicts are detected: a PVC is only used for an ephemeral
volume if it was created for the Pod. This check is based on the
ownership relationship. An existing PVC is not overwritten or
modified. But this does not resolve the conflict because without the
right PVC, the Pod cannot start.

{{< caution >}}
Take care when naming Pods and volumes inside the
same namespace, so that these conflicts can't occur.
{{< /caution >}}

### Security

Enabling the GenericEphemeralVolume feature allows users to create
PVCs indirectly if they can create Pods, even if they do not have
permission to create PVCs directly. Cluster administrators must be
aware of this. If this does not fit their security model, they have
two choices:
- Explicitly disable the feature through the feature gate.
- Use a [Pod Security
  Policy](/docs/concepts/policy/pod-security-policy/) where the
  `volumes` list does not contain the `ephemeral` volume type
  (deprecated in Kubernetes 1.21).
- Use an [admission webhook](/docs/reference/access-authn-authz/extensible-admission-controllers/)
  which rejects objects like Pods that have a generic ephemeral
  volume.

The normal [namespace quota for PVCs](/docs/concepts/policy/resource-quotas/#storage-resource-quota) still applies, so
even if users are allowed to use this new mechanism, they cannot use
it to circumvent other policies.

## {{% heading "whatsnext" %}}

### Ephemeral volumes managed by kubelet

See [local ephemeral storage](/docs/concepts/configuration/manage-resources-containers/#local-ephemeral-storage).

### CSI ephemeral volumes

- For more information on the design, see the [Ephemeral Inline CSI
  volumes KEP](https://github.com/kubernetes/enhancements/blob/ad6021b3d61a49040a3f835e12c8bb5424db2bbb/keps/sig-storage/20190122-csi-inline-volumes.md).
- For more information on further development of this feature, see the [enhancement tracking issue #596](https://github.com/kubernetes/enhancements/issues/596).

### Generic ephemeral volumes

- For more information on the design, see the
[Generic ephemeral inline volumes KEP](https://github.com/kubernetes/enhancements/blob/master/keps/sig-storage/1698-generic-ephemeral-volumes/README.md).
- For more information on further development of this feature, see the [enhancement tracking issue #1698](https://github.com/kubernetes/enhancements/issues/1698).
