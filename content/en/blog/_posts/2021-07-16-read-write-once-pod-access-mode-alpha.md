---
layout: blog
title: "Introducing Single Pod Access Mode for PersistentVolumes"
date: 2021-07-16
slug: read-write-once-pod-access-mode-alpha
---

**Author:** Chris Henzie (Google)

Kubernetes 1.22 introduces a new ReadWriteOncePod access mode for PersistentVolumes and PersistentVolumeClaims that allows users to restrict volume access to a single pod in the cluster.

## What are access modes and why are they important?

When using storage, there are different ways we can model how it is consumed.

For example, a storage system like a network file share can have many users all reading and writing data simultaneously.
In other cases maybe everyone is allowed to read data but not write it.
For highly sensitive data, maybe only one user is allowed to read and write data but nobody else.

In the world of Kubernetes, access modes are the way we model how storage is consumed.
These access modes are a part of the spec for PersistentVolumes (PVs) and PersistentVolumeClaims (PVCs).

<!-- TODO: Is there a way to strongly highlight the accessModes section inside this block? -->
```yaml
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  name: cat-pictures
spec:
  accessModes:
  - ReadWriteMany
  resources:
    requests:
      storage: 1Gi
```

In Kubernetes, we currently have three access modes for PVs and PVCs:

- ReadWriteOnce -- the volume can be mounted as read-write by a single node
- ReadOnlyMany -- the volume can be mounted read-only by many nodes
- ReadWriteMany -- the volume can be mounted as read-write by many nodes

These access modes are enforced by Kubernetes components like the kube-controller-manager and kubelet to ensure only certain pods are allowed to access a given PersistentVolume.
This allows users to follow the principle of least privilege to mitigate the impact of bad actors.

## What is this new access mode and how does it work?

In Kubernetes 1.22, a fourth access mode for PVs and PVCs is introduced:

- ReadWriteOncePod -- the volume can be mounted as read-write by a single pod

When a user creates a pod with a PVC that has the ReadWriteOncePod access mode, Kubernetes will ensure that pod is the only pod in the cluster that can read and write to it.

If you create another pod that references the same PVC with this access mode, the pod will fail to start like so:

```shell
Events:
  Type     Reason            Age   From               Message
  ----     ------            ----  ----               -------
  Warning  FailedScheduling  1s    default-scheduler  0/1 nodes are available: 1 node has pod using PersistentVolumeClaim with the same name and ReadWriteOncePod access mode.
```

### How is this different than the ReadWriteOnce access mode?

The ReadWriteOnce access mode restricts volume access to a single *node*, which means it is possible for multiple pods on the same node to write to the same volume.

## How do I use it?

The ReadWriteOncePod access mode is in alpha for Kubernetes 1.22. As a first step we need to enable the ReadWriteOncePod feature gate for `kube-apiserver`, `kube-scheduler`, and `kubelet`. The feature gate can be enabled or disabled as follows (as described in more detail [here]).

```shell
--feature-gates="...,ReadWriteOncePod=true"
```

[here]: https://kubernetes.io/docs/reference/command-line-tools-reference/feature-gates/

### Creating a PersistentVolumeClaim

In order to use the ReadWriteOncePod access mode for your PVs and PVCs, you will need to create a new PVC with the access mode:

```yaml
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  name: top-secret
spec:
  accessModes:
  - ReadWriteOncePod
  resources:
    requests:
      storage: 1Gi
```

## What volume plugins support this?

## As a storage vendor, how do I add support for this access mode to my CSI driver?

### New Controller and Node Service Capabilities

## What’s next?

## How can I learn more?

## How do I get involved?
