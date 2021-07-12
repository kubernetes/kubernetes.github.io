---
title: Local Persistent Volumes for Kubernetes Goes Beta
date: 2018-04-13
slug: local-persistent-volumes-beta
---

The [Local Persistent Volumes](/docs/concepts/storage/volumes/#local) beta feature in Kubernetes 1.10 makes it possible to leverage local disks in your StatefulSets. You can specify directly-attached local disks as PersistentVolumes, and use them in StatefulSets with the same PersistentVolumeClaim objects that previously only supported remote volume types.

Persistent storage is important for running stateful applications, and Kubernetes has supported these workloads with StatefulSets, PersistentVolumeClaims and PersistentVolumes. These primitives have supported remote volume types well, where the volumes can be accessed from any node in the cluster, but did not support local volumes, where the volumes can only be accessed from a specific node. The demand for using local, fast SSDs in replicated, stateful workloads has increased with demand to run more workloads in Kubernetes.

## Addressing hostPath challenges

The prior mechanism of accessing local storage through hostPath volumes had many challenges. hostPath volumes were difficult to use in production at scale: operators needed to care for local disk management, topology, and scheduling of individual pods when using hostPath volumes, and could not use many Kubernetes features (like StatefulSets). Existing Helm charts that used remote volumes could not be easily ported to use hostPath volumes. The Local Persistent Volumes feature aims to address hostPath volumes’ portability, disk accounting, and scheduling challenges.

## Disclaimer

Before going into details about how to use Local Persistent Volumes, note that local volumes are not suitable for most applications. Using local storage ties your application to that specific node, making your application harder to schedule. If that node or local volume encounters a failure and becomes inaccessible, then that pod also becomes inaccessible. In addition, many cloud providers do not provide extensive data durability guarantees for local storage, so you could lose all your data in certain scenarios.

For those reasons, most applications should continue to use highly available, remotely accessible, durable storage.

## Suitable workloads

Some use cases that are suitable for local storage include:

* Caching of datasets that can leverage data gravity for fast processing
* Distributed storage systems that shard or replicate data across multiple
  nodes. Examples include distributed datastores like Cassandra, or distributed
  file systems like Gluster or Ceph.

Suitable workloads are tolerant of node failures, data unavailability, and data loss. They provide critical, latency-sensitive infrastructure services to the rest of the cluster, and should run with high priority compared to other workloads.

## Enabling smarter scheduling and volume binding

An administrator must enable smarter scheduling for local persistent volumes. Before any PersistentVolumeClaims for your local PersistentVolumes are created, a StorageClass must be created with the volumeBindingMode set to “WaitForFirstConsumer”:

```
kind: StorageClass
apiVersion: storage.k8s.io/v1
metadata:
  name: local-storage
provisioner: kubernetes.io/no-provisioner
volumeBindingMode: WaitForFirstConsumer
```

This setting tells the PersistentVolume controller to not immediately bind a PersistentVolumeClaim. Instead, the system waits until a Pod that needs to use a volume is scheduled. The scheduler then chooses an appropriate local PersistentVolume to bind to, taking into account the Pod’s other scheduling constraints and policies. This ensures that the initial volume binding is compatible with any Pod resource requirements, selectors, affinity and anti-affinity policies, and more.

Note that dynamic provisioning is not supported in beta. All local PersistentVolumes must be statically created.

## Creating a local persistent volume

For this initial beta offering, local disks must first be pre-partitioned, formatted, and mounted on the local node by an administrator. Directories on a shared file system are also supported, but must also be created before use.

Once you set up the local volume, you can create a PersistentVolume for it. In this example, the local volume is mounted at “/mnt/disks/vol1” on node “my-node”:

```
apiVersion: v1
kind: PersistentVolume
metadata:
  name: example-local-pv
spec:
  capacity:
    storage: 500Gi
  accessModes:
  - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: local-storage
  local:
    path: /mnt/disks/vol1
  nodeAffinity:
    required:
      nodeSelectorTerms:
      - matchExpressions:
        - key: kubernetes.io/hostname
          operator: In
          values:
          - my-node
```

Note that there’s a new nodeAffinity field in the PersistentVolume object: this is how the Kubernetes scheduler understands that this PersistentVolume is tied to a specific node. nodeAffinity is a required field for local PersistentVolumes.

When local volumes are manually created like this, the only supported persistentVolumeReclaimPolicy is “Retain”. When the PersistentVolume is released from the PersistentVolumeClaim, an administrator must manually clean up and set up the local volume again for reuse.

## Automating local volume creation and deletion

Manually creating and cleaning up local volumes is a big administrative burden, so we’ve written a simple local volume manager to automate some of these pieces. It’s available in the [external-storage repo](https://github.com/kubernetes-incubator/external-storage/tree/master/local-volume) as an optional program that you can deploy in your cluster, including instructions and example deployment specs for how to run it.

To use this, the local volumes must still first be set up and mounted on the local node by an administrator. The administrator needs to mount the local volume into a configurable “discovery directory” that the local volume manager recognizes. Directories on a shared file system are supported, but they must be bind-mounted into the discovery directory.

This local volume manager monitors the discovery directory, looking for any new mount points. The manager creates a PersistentVolume object with the appropriate storageClassName, path, nodeAffinity, and capacity for any new mount point that it detects. These PersistentVolume objects can eventually be claimed by PersistentVolumeClaims, and then mounted in Pods.

After a Pod is done using the volume and deletes the PersistentVolumeClaim for it, the local volume manager cleans up the local mount by deleting all files from it, then deleting the PersistentVolume object. This triggers the discovery cycle: a new PersistentVolume is created for the volume and can be reused by a new PersistentVolumeClaim.

Once the administrator initially sets up the local volume mount, this local volume manager takes over the rest of the PersistentVolume lifecycle without any further administrator intervention required.

## Using local volumes in a pod

After all that administrator work, how does a user actually mount a local volume into their Pod? Luckily from the user’s perspective, a local volume can be requested in exactly the same way as any other PersistentVolume type: through a PersistentVolumeClaim. Just specify the appropriate StorageClassName for local volumes in the PersistentVolumeClaim object, and the system takes care of the rest!

```
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  name: example-local-claim
spec:
  accessModes:
  - ReadWriteOnce
  storageClassName: local-storage
  resources:
    requests:
      storage: 500Gi
```      

Or in a StatefulSet as a volumeClaimTemplate:

```
kind: StatefulSet
...
 volumeClaimTemplates:
  - metadata:
      name: example-local-claim
    spec:
      accessModes:
      - ReadWriteOnce
      storageClassName: local-storage
      resources:
        requests:
          storage: 500Gi
```          

## Documentation

The Kubernetes website provides full documentation for [local persistent volumes](/docs/concepts/storage/volumes/#local).

## Future enhancements

The local persistent volume beta feature is not complete by far. Some notable enhancements under development:

* Starting in 1.10, local raw block volumes is available as an alpha feature. This is useful for workloads that need to directly access block devices and manage their own data format.
* Dynamic provisioning of local volumes using LVM is under design and an alpha implementation will follow in a future release. This will eliminate the current need for an administrator to pre-partition, format and mount local volumes, as long as the workload’s performance requirements can tolerate sharing disks.

## Complementary features

[Pod priority and preemption](/docs/concepts/scheduling-eviction/pod-priority-preemption/) is another Kubernetes feature that is complementary to local persistent volumes. When your application uses local storage, it must be scheduled to the specific node where the local volume resides. You can give your local storage workload high priority so if that node ran out of room to run your workload, Kubernetes can preempt lower priority workloads to make room for it.

[Pod disruption budget](/docs/concepts/workloads/pods/disruptions/) is also very important for those workloads that must maintain quorum. Setting a disruption budget for your workload ensures that it does not drop below quorum due to voluntary disruption events, such as node drains during upgrade.

[Pod affinity and anti-affinity](/docs/concepts/scheduling-eviction/assign-pod-node/#inter-pod-affinity-and-anti-affinity-beta-feature) ensures that your workloads stay either co-located or spread out across failure domains. If you have multiple local persistent volumes available on a single node, it may be preferable to specify an pod anti-affinity policy to spread your workload across nodes. Note that if you want multiple pods to share the same local persistent volume, you do not need to specify a pod affinity policy. The scheduler understands the locality constraints of the local persistent volume and schedules your pod to the correct node.

## Getting involved

If you have feedback for this feature or are interested in getting involved with the design and development, join the [Kubernetes Storage Special-Interest-Group](https://github.com/kubernetes/community/tree/master/sig-storage) (SIG). We’re rapidly growing and always welcome new contributors.

Special thanks to all the contributors from multiple companies that helped bring this feature to beta, including Cheng Xing ([verult](https://github.com/verult)), David Zhu ([davidz627](https://github.com/davidz627)), Deyuan Deng ([ddysher](https://github.com/ddysher)), Dhiraj Hedge ([dhirajh](https://github.com/dhirajh)), Ian Chakeres ([ianchakeres](https://github.com/ianchakeres)), Jan Šafránek ([jsafrane](https://github.com/jsafrane)), Matthew Wong ([wongma7](https://github.com/wongma7)), Michelle Au ([msau42](https://github.com/msau42)), Serguei Bezverkhi ([sbezverk](https://github.com/sbezverk)), and Yuquan Ren ([nickrenren](https://github.com/nickrenren)).
