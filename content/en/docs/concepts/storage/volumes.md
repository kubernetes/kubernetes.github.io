---
reviewers:
- jsafrane
- saad-ali
- thockin
- msau42
title: Volumes
content_type: concept
weight: 10
---

<!-- overview -->

File storage is useful when building applications, such as to store state or cache data. Use _volumes_ to declaratively manage storage for containers. The Kubernetes {{< glossary_tooltip text="volume" term_id="volume" >}} abstraction allows files to persist even beyond the lifetime of a pod. Volumes also allow different containers within a pod to share storage and to access configuration.

Familiarity with [Pods](/docs/concepts/workloads/pods/) is suggested.

<!-- body -->

## Introduction

One use case for volumes is providing directories to pods, possibly with some data in it.  How that directory comes to be, the medium that backs it, and the contents of it are determined by the particular volume type used.

Kubernetes supports a variety of different volume types, such as directories from the host system and NFS mounts. In addition to filesystem volumes, Kubernetes also supports persistent volumes in a [raw block access mode](/docs/concepts/storage/persistent-volumes/#raw-block-volume-support). 

### Volume Lifecycle

In a standard docker container, for example, the filesystem of a container is ephemeral. When a container is restarted or destroyed, modifications to the container filesystem are lost.  

A Kubernetes volume's lifecycle is tied to the *pod* that encloses it. The pod maintains the volume as different containers are started or stopped. Multiple volumes of any type may be connected to a pod. The [PersistentVolume](/docs/concepts/storage/persistent-volumes/) abstraction builds on the volume concept to let pods access storage that outlasts the lifetime of a pod. For example, a PersistentVolume may be a NFS mount or a Google Cloud Persistent Disk. 

Kubernetes also supports [Ephemeral volumes](docs/concepts/storage/ephemeral-volumes/), such as an emptyDir or a configMap. Some application need additional storage but don't care whether that data is stored persistently across restarts. 
 
### Volume specification example
 
First, specify a pod that will provide the volume. This example uses the `emptyDir` volume type, and includes mounting the volume. The [`emptyDir` volume type](#emptydir) is merely an empty directory, available for containers to mount. The contents will be lost when the pod is terminated or restarts. 

A `Pod`'s specification defines what `volumes` are available to containers in that pod through the `.spec.volumes` field.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: sample-cache-pod
spec:
  # other specification, including container definitions
  volumes:
    - name: cache-volume
      emptyDir: {}
```

Second, specify a mount point within each container via the
`.spec.containers[*].volumeMounts` field. 

Volumes can not mount into other volumes, or have hard links to
other volumes. Each container in the pod's configuration must independently specify where to mount each volume. 

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: sample-cache-pod
spec:
  volumes:
    [...]
  containers:
    - name: test
      image: busybox
      volumeMounts:
        - name: cache-volume
          mountPath: /var/cache

```

## Specify subPaths on volumes {#using-subpath}

The `volumeMounts.subPath` property mounts the subdirectory of the volume into the container. More specifically, The `volumeMounts.subPath` property specifies a sub-path inside the referenced volume instead of its root. For example, this property may be used to to share one volume for multiple uses in a single pod.

The following example shows how to configure a Pod with a LAMP stack (Linux Apache MySQL PHP)
using a single, shared volume. This sample `subPath` configuration is not recommended
for production use.

The PHP application's code and assets map to the volume's `html` folder and
the MySQL database is stored in the volume's `mysql` folder. For example:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-lamp-site
spec:
    containers:
    - name: mysql
      image: mysql
      env:
      # password in config yaml for testing only
      # use a Kubernetes Secret in production
      - name: MYSQL_ROOT_PASSWORD
        value: "rootpasswd"
      volumeMounts:
      - mountPath: /var/lib/mysql
        name: site-data
        subPath: mysql
    - name: php
      image: php:7.0-apache
      volumeMounts:
      - mountPath: /var/www/html
        name: site-data
        subPath: html
    volumes:
    - name: site-data
      persistentVolumeClaim:
        claimName: my-lamp-site-data
```

Note: The password is defined in the config yaml, which is insecure. See Kubernetes Secrets for a secure solution.

### Kubernetes core volume types {#volume-types-core}

Kubernetes supports several types of volumes. Kubernetes core volume types are specialized volume types (mostly ephemeral) and are not used for general purpose persistent storage use cases. 

Core Volume Types:

   * [configMap](#configmap)
   * [downwardAPI](#downwardapi)
   * [emptyDir](#emptydir)
   * [gitRepo (deprecated)](#gitrepo)
   * [glusterfs](#glusterfs)
   * [hostPath](#hostpath)
   * [local](#local)
   * [projected](#projected)
   * [secret](#secret)


### Storage plugins

A [persistentVolumeClaim](#persistentvolumeclaim) is a declarative way to ask for storage, without preference for the underlying implementation. 

This is powered by storage plugins. Kubernetes implements the {{< glossary_tooltip text="Container Storage Interface" term_id="csi" >}} (CSI),
which lets developers implement storage plugins without needing to make changes to the code of
Kubernetes itself. Visit
[Kubernetes Container Storage Interface Documentation])(https://kubernetes-csi.github.io/docs/)
to learn more about CSI. 

In contrast to the CSI, some storage plugins are "in-tree" plugins. That is, storage technology specific code inserted into the code of Kubernetes itself, without using the CSI. The C  

[FlexVolume](#flexvolume) is yet another mechanism for storage plugins. Unlike CSI, FlexVolume is
more closely tied to Kubernetes and its storage implementation. FlexVolume was developed before CSI.

Storage plugin interfaces:

   * [CSI](#csi)
   * [FlexVolume](#flexvolume)
   * [persistentVolumeClaim](#persistentvolumeclaim)


### General purpose volume types

Kubernetes directly implements some volume types for communicating with externally managed volumes, such as AWS EBS or Azure Disk Storage. These volume types are described as in-tree storage plugins, and are used for general purpose persistent storage. 

The CSI was introduced to standardize connectivity to externally managed volumes, such as cloud platform storage. However, Kubernetes still includes many volume types for connecting to specific cloud storage providers. 

{{< note >}}
Using in-tree plugins is not recommended. All new storage features are only supported for CSI volumes, and in-tree plugins are being replaced by their equivalent CSI drivers."
{{< note >}}

General Purpose  Volume Types:
   * [awsElasticBlockStore](#awselasticblockstore)
   * [azureDisk](#azuredisk)
   * [azureFile](#azurefile)
   * [cephfs](#cephfs)
   * [cinder](#cinder)
   * [fc (fibre channel)](#fc)
   * [gcePersistentDisk](#gcepersistentdisk)
   * [iscsi](#iscsi)
   * [nfs](#nfs)
   * [portworxVolume](#portworxvolume)
   * [rbd](#rbd)
   * [vsphereVolume](#vspherevolume)

## Kubernetes core volume types

### configMap

A [ConfigMap](/docs/concepts/configuration/configmap/) 
exports configuration data to a pod's filesystem. A `configMap` volume references data stored in a `ConfigMap` object. Containerized applications use the data from the volume. 

You must create a [ConfigMap](/docs/tasks/configure-pod-container/configure-pod-configmap/) 
before you can use it.

{{< note >}}
A container using a ConfigMap as a [subPath](#using-subpath) volume mount does not receive ConfigMap updates.
{{< /note >}}

When referencing a ConfigMap, you provide the name of the ConfigMap in the
volume. You can customize the path to use for a specific
entry in the ConfigMap. The following configuration shows how to mount
the `log-config` ConfigMap onto a pod called `configmap-pod`:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: configmap-pod
spec:
  containers:
    - name: test
      image: busybox
      volumeMounts:
        - name: config-vol
          mountPath: /etc/config
  volumes:
    - name: config-vol
      configMap:
        name: log-config
        items:
          - key: log_level
            path: log_level
```

The `log-config` ConfigMap is mounted as a volume, and all contents stored in
its `log_level` entry are mounted into the pod at path `/etc/config/log_level`.
Note that this path is derived from the volume's `mountPath` and the `path`
keyed with `log_level`.

Values from ConfigMaps are exposed as text files, using UTF-8 character encoding. To use some other character encoding, or to store information that is not text, use the `binaryData` (rather than `data`) field in the ConfigMap.

### downwardAPI {#downwardapi}

A `downwardAPI` volume makes downward API data available to applications.
It mounts a directory and writes the requested data in plain text files.

{{< note >}}
A container using the downward API as a [`subPath`](#using-subpath) volume mount will not receive downward API updates.
{{< /note >}}

See the [downward API example](/docs/tasks/inject-data-application/downward-api-volume-expose-pod-information/) for more details.

### emptyDir {#emptydir}

An `emptyDir` volume is first created when a pod is assigned to a node, and
exists as long as that pod is running on that node. As the name says, the
`emptyDir` volume is initially empty. All containers in the pod can read and write the same
files in the `emptyDir` volume, though that volume can be mounted at the same
or different paths in each container. When a pod is removed from a node for
any reason, the data in the `emptyDir` is deleted permanently.

{{< note >}}
A container crashing does *not* remove a pod from a node. The data in an `emptyDir` volume
is safe across container crashes.
{{< /note >}}

Some uses for an `emptyDir` are:

* scratch space, such as for a disk-based merge sort
* checkpointing a long computation for recovery from crashes
* holding files that a content-manager container fetches while a webserver
  container serves the data

Depending on your environment, `emptyDir` volumes are stored on whatever medium that backs the
node such as disk or SSD, or network storage. However, if you set the `emptyDir.medium` field
to `"Memory"`, Kubernetes mounts a `tmpfs` (RAM-backed filesystem) for you instead.
While `tmpfs` is very fast, be aware that unlike disks, `tmpfs` is cleared on
node reboot and any files you write count against your container's
memory limit.

{{< note >}}
If the `SizeMemoryBackedVolumes` [feature gate](/docs/reference/command-line-tools-reference/feature-gates/) is enabled,
you can specify a size for memory backed volumes.  If no size is specified, memory
backed volumes are sized to 50% of the memory on a Linux host.
{{< /note>}}

#### Resources

//todo

The storage media (such as Disk or SSD) of an `emptyDir` volume is determined by the medium of the filesystem holding the kubelet root dir (typically
`/var/lib/kubelet`). There is no limit on how much space an `emptyDir` or
`hostPath` volume can consume, and no isolation between containers or between
pods.

A container of a pod may request ephemeral storage in it's spec. For example, `spec.containers[].resources.requests.ephemeral-storage` may be specified and set to a requested amount of storage in bytes. This storage can be used for `emptyDir` volumes. Learn more about [managing resources for containers](/docs/concepts/configuration/manage-resources-containers/#setting-requests-and-limits-for-local-ephemeral-storage).

#### emptyDir configuration example

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: test-pd
spec:
  containers:
  - image: k8s.gcr.io/test-webserver
    name: test-container
    volumeMounts:
    - mountPath: /cache
      name: cache-volume
  volumes:
  - name: cache-volume
    emptyDir: {}
```

### gitRepo (deprecated) {#gitrepo}

{{< warning >}}
The `gitRepo` volume type is deprecated. To provision a container with a git repo, mount an [EmptyDir](#emptydir) into an InitContainer that clones the repo using git, then mount the [EmptyDir](#emptydir) into the pod's container.
{{< /warning >}}

A `gitRepo` volume is an example of a volume plugin. This plugin
mounts an empty directory and clones a git repository into this directory
for your pod to use.

Here is an example of a `gitRepo` volume:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: server
spec:
  containers:
  - image: nginx
    name: nginx
    volumeMounts:
    - mountPath: /mypath
      name: git-volume
  volumes:
  - name: git-volume
    gitRepo:
      repository: "git@somewhere:me/my-git-repository.git"
      revision: "22f1d8406d464b0c0874075539c1f2e96c253775"
```

### glusterfs

A `glusterfs` volume allows a [Glusterfs](https://www.gluster.org) (an open
source networked filesystem) volume to be mounted into your pod. Unlike
`emptyDir`, which is erased when a pod is removed, the contents of a
`glusterfs` volume are preserved and the volume is merely unmounted. This
means that a glusterfs volume can be pre-populated with data, and that data can
be shared between pods. GlusterFS can be mounted by multiple writers
simultaneously.

You must have your own GlusterFS installation running before you can use it.

See the [GlusterFS example](https://github.com/kubernetes/examples/tree/{{< param "githubbranch" >}}/volumes/glusterfs) for more details.

### hostPath {#hostpath}

A `hostPath` volume mounts a file or directory from the host node's filesystem
into your pod. This volume type improperly breaks the boundary betwen host and container. However, it may be necessary in certain situations, such as testing or running legacy applications. 

For example, some uses for a `hostPath` are:

* running a container that needs access to Docker internals; use a `hostPath`
  of `/var/lib/docker`
* running cAdvisor in a container; use a `hostPath` of `/sys`
* allowing a pod to specify whether a given `hostPath` should exist prior to the
  pod running, whether it should be created, and what it should exist as

In addition to the required `path` property, you can optionally specify a `type` for a `hostPath` volume.

The supported values for field `type` are:

| Value | Behavior |
|:------|:---------|
| | Empty string (default) is for backward compatibility, which means that no checks will be performed before mounting the hostPath volume. |
| `DirectoryOrCreate` | If nothing exists at the given path, an empty directory is created there as needed with permission set to 0755, having the same group and ownership with Kubelet. |
| `Directory` | A directory must exist at the given path |
| `FileOrCreate` | If nothing exists at the given path, an empty file is be created there as needed with permission set to 0644, having the same group and ownership with Kubelet. |
| `File` | A file must exist at the given path |
| `Socket` | A UNIX socket must exist at the given path |
| `CharDevice` | A character device must exist at the given path |
| `BlockDevice` | A block device must exist at the given path |

Watch out when using this type of volume, because:

* Pods with identical configuration (such as those created from a PodTemplate) may
  behave differently on different nodes due to different files on the nodes
* The files or directories created on the underlying hosts are only writable by root. You
  either need to run your process as root in a
  [privileged container](/docs/tasks/configure-pod-container/security-context/) or modify the file
  permissions on the host to be able to write to a `hostPath` volume

#### hostPath configuration example

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: test-pd
spec:
  containers:
  - image: k8s.gcr.io/test-webserver
    name: test-container
    volumeMounts:
    - mountPath: /test-pd
      name: test-volume
  volumes:
  - name: test-volume
    hostPath:
      # directory location on host
      path: /data
      # this field is optional
      type: Directory
```

{{< caution >}}
The `FileOrCreate` mode does not create the parent directory of the file. If the parent directory
of the mounted file does not exist, the pod fails to start. To ensure that this mode works,
you can try to mount directories and files separately, as shown in the
[`FileOrCreate`configuration](#hostpath-fileorcreate-example).
{{< /caution >}}

####  hostPath FileOrCreate configuration example {#hostpath-fileorcreate-example}

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: test-webserver
spec:
  containers:
  - name: test-webserver
    image: k8s.gcr.io/test-webserver:latest
    volumeMounts:
    - mountPath: /var/local/aaa
      name: mydir
    - mountPath: /var/local/aaa/1.txt
      name: myfile
  volumes:
  - name: mydir
    hostPath:
      # Ensure the file directory is created.
      path: /var/local/aaa
      type: DirectoryOrCreate
  - name: myfile
    hostPath:
      path: /var/local/aaa/1.txt
      type: FileOrCreate
```

### local

A `local` volume represents a mounted local storage device such as a disk,
partition or directory.

Local volumes can only be used as a statically created PersistentVolume. Dynamic
provisioning is not supported.

Compared to `hostPath` volumes, `local` volumes are used in a *durable and
portable manner* without manually scheduling pods to nodes. The system is aware
of the volume's node constraints by looking at the node affinity on the PersistentVolume.

However, `local` volumes are subject to the availability of the underlying
node and are not suitable for all applications. If a node becomes unhealthy,
then the `local` volume becomes inaccessible by the pod. The pod using this volume
is unable to run. Applications using `local` volumes must be able to tolerate this
reduced availability, as well as potential data loss, depending on the
durability characteristics of the underlying disk.

The following example shows a PersistentVolume using a `local` volume and
`nodeAffinity`:

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: example-pv
spec:
  capacity:
    storage: 100Gi
  volumeMode: Filesystem
  accessModes:
  - ReadWriteOnce
  persistentVolumeReclaimPolicy: Delete
  storageClassName: local-storage
  local:
    path: /mnt/disks/ssd1
  nodeAffinity:
    required:
      nodeSelectorTerms:
      - matchExpressions:
        - key: kubernetes.io/hostname
          operator: In
          values:
          - example-node
```

You must set a PersistentVolume `nodeAffinity` when using `local` volumes.
The Kubernetes scheduler uses the PersistentVolume `nodeAffinity` to schedule
these pods to the correct node.

PersistentVolume `volumeMode` can be set to "Block" (instead of the default
value "Filesystem") to expose the local volume as a raw block device.

When using local volumes, it is recommended to create a StorageClass with
`volumeBindingMode` set to `WaitForFirstConsumer`. For more details, see the
local [StorageClass](/docs/concepts/storage/storage-classes/#local) example.
Delaying volume binding ensures that the PersistentVolumeClaim binding decision
is evaluated with any other node constraints the Pod may have,
such as node resource requirements, node selectors, Pod affinity, and Pod anti-affinity.

An external static provisioner can be run separately for improved management of
the local volume lifecycle. Note that this provisioner does not support dynamic
provisioning yet. For an example on how to run an external local provisioner,
see the [local volume provisioner user
guide](https://github.com/kubernetes-sigs/sig-storage-local-static-provisioner).

{{< note >}}
The local PersistentVolume requires manual cleanup and deletion by the
user if the external static provisioner is not used to manage the volume
lifecycle.
{{< /note >}}

### projected {#projected}

A `projected` volume maps several existing volume sources into the same directory.

Currently, the following types of volume sources can be projected:

* [`secret`](#secret)
* [`downwardAPI`](#downwardapi)
* [`configMap`](#configmap)
* `serviceAccountToken`

All sources are required to be in the same namespace as the pod. For more details,
see the [all-in-one volume design document](https://github.com/kubernetes/community/blob/{{< param "githubbranch" >}}/contributors/design-proposals/node/all-in-one-volume.md).

#### Example configuration with a secret, a downwardAPI, and a configMap {#example-configuration-secret-downwardapi-configmap}


```yaml
apiVersion: v1
kind: Pod
metadata:
  name: volume-test
spec:
  containers:
  - name: container-test
    image: busybox
    volumeMounts:
    - name: all-in-one
      mountPath: "/projected-volume"
      readOnly: true
  volumes:
  - name: all-in-one
    projected:
      sources:
      - secret:
          name: mysecret
          items:
            - key: username
              path: my-group/my-username
      - downwardAPI:
          items:
            - path: "labels"
              fieldRef:
                fieldPath: metadata.labels
            - path: "cpu_limit"
              resourceFieldRef:
                containerName: container-test
                resource: limits.cpu
      - configMap:
          name: myconfigmap
          items:
            - key: config
              path: my-group/my-config
```

#### Example configuration: secrets with a non-default permission mode set {#example-configuration-secrets-nondefault-permission-mode}

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: volume-test
spec:
  containers:
  - name: container-test
    image: busybox
    volumeMounts:
    - name: all-in-one
      mountPath: "/projected-volume"
      readOnly: true
  volumes:
  - name: all-in-one
    projected:
      sources:
      - secret:
          name: mysecret
          items:
            - key: username
              path: my-group/my-username
      - secret:
          name: mysecret2
          items:
            - key: password
              path: my-group/my-password
              mode: 511
```

Each projected volume source is listed in the spec under `sources`. The
parameters are nearly the same with two exceptions:

* For secrets, the `secretName` field has been changed to `name` to be consistent
  with ConfigMap naming.
* The `defaultMode` can only be specified at the projected level and not for each
  volume source. However, as illustrated above, you can explicitly set the `mode`
  for each individual projection.

You can inject the token
for the current [service account](/docs/reference/access-authn-authz/authentication/#service-account-tokens)
into a pod at a specified path. For example:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: sa-token-test
spec:
  containers:
  - name: container-test
    image: busybox
    volumeMounts:
    - name: token-vol
      mountPath: "/service-account"
      readOnly: true
  volumes:
  - name: token-vol
    projected:
      sources:
      - serviceAccountToken:
          audience: api
          expirationSeconds: 3600
          path: token
```

The example pod has a projected volume containing the injected service account
token. This token can be used by a Pod's containers to access the Kubernetes API
server. The `audience` field contains the intended audience of the
token. A recipient of the token must identify itself with an identifier specified
in the audience of the token, and otherwise should reject the token. This field
is optional and it defaults to the identifier of the API server.

The `expirationSeconds` is the expected duration of validity of the service account
token. It defaults to one hour and must be at least 10 minutes (600 seconds). An administrator
can also limit its maximum value by specifying the `--service-account-max-token-expiration`
option for the API server. The `path` field specifies a relative path to the mount point
of the projected volume.

{{< note >}}
A container using a projected volume source as a [`subPath`](#using-subpath) volume mount will not
receive updates for those volume sources.
{{< /note >}}

### secret 

A `secret` volume is used to pass sensitive information, such as passwords, to
Pods. You can store secrets in the Kubernetes API and mount them as files for
use by pods without coupling to Kubernetes directly. `secret` volumes are
backed by tmpfs (a RAM-backed filesystem) so they are never written to
non-volatile storage.

{{< note >}}
A container using a Secret as a [`subPath`](#using-subpath) volume mount doesn't receive Secret updates.
{{< /note >}}

For more details, see [Configuring Secrets](/docs/concepts/configuration/secret/).


## Storage plugin interfaces

The out-of-tree volume plugins include the Container Storage Interface (CSI)
and FlexVolume. They enable storage vendors to create custom storage plugins. The main Kubernetes binary implements the CSI, and communicates with any external plugins. This keeps the main binary efficient, and allows users to choose their own storage plugins. 

Before the introduction of CSI and FlexVolume, all volume plugins (like
volume types listed above) were "in-tree" meaning they were built, linked,
compiled, and shipped with the core Kubernetes binaries and extend the core
Kubernetes API. This meant that adding a new storage system to Kubernetes (a
volume plugin) required checking code into the core Kubernetes code repository.

CSI and FlexVolume allow volume plugin development independent of the Kubernetes code base. Both are deployed (installed) on Kubernetes clusters as
extensions.

For storage vendors looking to create an out-of-tree volume plugin, please refer
to the [volume plugin FAQ](https://github.com/kubernetes/community/blob/master/sig-storage/volume-plugin-faq.md).

### csi

{{< note >}}
CSI drivers may not be compatible across all Kubernetes releases.
Please check the specific CSI driver's documentation for supported
deployments steps for each Kubernetes release and a compatibility matrix.
{{< /note >}}

The {{< glossary_tooltip text="Container Storage Interface" term_id="csi" >}} defines a standard interface for container orchestration systems (like Kubernetes) to expose arbitrary storage systems to their container workloads.

Read the [CSI design proposal](https://github.com/kubernetes/community/blob/master/contributors/design-proposals/storage/container-storage-interface.md) or [CSI spec](https://github.com/container-storage-interface/spec/blob/master/spec.md) for more information.


Once a CSI compatible volume driver is deployed on a Kubernetes cluster, users
may use the `csi` volume type to attach or mount the volumes exposed by the
CSI driver.

A `csi` volume can be used in a pod in three different ways:

* through a reference to a [PersistentVolumeClaim](#persistentvolumeclaim)
* with a [generic ephemeral volume](/docs/concepts/storage/ephemeral-volumes/#generic-ephemeral-volume)
(alpha feature)
* with a [CSI ephemeral volume](/docs/concepts/storage/ephemeral-volumes/#csi-ephemeral-volume)
if the driver supports that (beta feature)

The following fields are available to storage administrators to configure a CSI
persistent volume:

* `driver`: A string value that specifies the name of the volume driver to use.
  This value must correspond to the value returned in the `GetPluginInfoResponse`
  by the CSI driver as defined in the [CSI spec](https://github.com/container-storage-interface/spec/blob/master/spec.md#getplugininfo).
  It is used by Kubernetes to identify which CSI driver to call out to, and by
  CSI driver components to identify which PV objects belong to the CSI driver.
* `volumeHandle`: A string value that uniquely identifies the volume. This value
  must correspond to the value returned in the `volume.id` field of the
  `CreateVolumeResponse` by the CSI driver as defined in the [CSI spec](https://github.com/container-storage-interface/spec/blob/master/spec.md#createvolume).
  The value is passed as `volume_id` on all calls to the CSI volume driver when
  referencing the volume.
* `readOnly`: An optional boolean value indicating whether the volume is
  "ControllerPublished" (attached) as read only. Default is false. This value is
  passed to the CSI driver via the `readonly` field in the
  `ControllerPublishVolumeRequest`.
* `fsType`: If the PV's `VolumeMode` is `Filesystem` then this field may be used
  to specify the filesystem that should be used to mount the volume. If the
  volume has not been formatted and formatting is supported, this value will be
  used to format the volume.
  This value is passed to the CSI driver via the `VolumeCapability` field of
  `ControllerPublishVolumeRequest`, `NodeStageVolumeRequest`, and
  `NodePublishVolumeRequest`.
* `volumeAttributes`: A map of string to string that specifies static properties
  of a volume. This map must correspond to the map returned in the
  `volume.attributes` field of the `CreateVolumeResponse` by the CSI driver as
  defined in the [CSI spec](https://github.com/container-storage-interface/spec/blob/master/spec.md#createvolume).
  The map is passed to the CSI driver via the `volume_context` field in the
  `ControllerPublishVolumeRequest`, `NodeStageVolumeRequest`, and
  `NodePublishVolumeRequest`.
* `controllerPublishSecretRef`: A reference to the secret object containing
  sensitive information to pass to the CSI driver to complete the CSI
  `ControllerPublishVolume` and `ControllerUnpublishVolume` calls. This field is
  optional, and may be empty if no secret is required. If the Secret
  contains more than one secret, all secrets are passed.
* `nodeStageSecretRef`: A reference to the secret object containing
  sensitive information to pass to the CSI driver to complete the CSI
  `NodeStageVolume` call. This field is optional, and may be empty if no secret
  is required. If the secret object contains more than one secret value, all secrets are passed.
* `nodePublishSecretRef`: A reference to the secret object containing
  sensitive information to pass to the CSI driver to complete the CSI
  `NodePublishVolume` call. This field is optional, and may be empty if no
  secret is required. If the secret object contains more than one secret, all
  secrets are passed.

#### CSI raw block volume support

{{< feature-state for_k8s_version="v1.18" state="stable" >}}

Vendors with external CSI drivers can implement raw block volume support
in Kubernetes workloads.

You can set up your
[PersistentVolume/PersistentVolumeClaim with raw block volume support](/docs/concepts/storage/persistent-volumes/#raw-block-volume-support) as usual, without any CSI specific changes.

#### CSI ephemeral volumes

{{< feature-state for_k8s_version="v1.16" state="beta" >}}

You can directly configure CSI volumes within the pod
specification. Volumes specified in this way are ephemeral and do not
persist across pod restarts. See [Ephemeral
Volumes](/docs/concepts/storage/ephemeral-volumes/#csi-ephemeral-volume)
for more information.

For more information on how to develop a CSI driver, refer to the
[kubernetes-csi documentation](https://kubernetes-csi.github.io/docs/).

#### Migrating to CSI drivers from in-tree plugins

{{< feature-state for_k8s_version="v1.17" state="beta" >}}

The `CSIMigration` feature, when enabled, directs operations against existing in-tree plugins to corresponding CSI plugins (which are expected to be installed and configured).  
As a result, operators do not have to make any
configuration changes to existing Storage Classes, PersistentVolumes or PersistentVolumeClaims
(referring to in-tree plugins) when transitioning to a CSI driver that supersedes an in-tree plugin.

The operations and features that are supported include:
provisioning/delete, attach/detach, mount/unmount and resizing of volumes.

To learn more about migrating from an in-tree volume plugin to a CSI driver, 
lookup the specific volume type under [Types of Volumes](#volume-types).

### flexVolume

FlexVolume is an out-of-tree plugin interface that has existed in Kubernetes
since version 1.2 (before CSI). FlexVolume is deprecated. CSI is the recommended way to develop storage plugins for Kubernetes. 

It uses an exec-based model to interface with
drivers. The FlexVolume driver binaries must be installed in a pre-defined volume
plugin path on each node and in some cases the control plane nodes as well.

Pods interact with FlexVolume drivers through the `flexvolume` in-tree volume plugin.
For more details, see the [FlexVolume](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-storage/flexvolume.md) examples.

### persistentVolumeClaim {#persistentvolumeclaim}

A `persistentVolumeClaim` volume is used to mount a
[PersistentVolume](/docs/concepts/storage/persistent-volumes/) into a pod. Notably, the lifecycle of the `persistentVolumeClaim` is independent of the pod, suitable for stateful or data storage applications. PersistentVolumeClaims are a way for cluster developers to "claim" durable storage (such as a GCE PersistentDisk or an iSCSI volume) without knowing the details of the particular cloud environment.

See the information about [PersistentVolumes](/docs/concepts/storage/persistent-volumes/) for more
details.

## General purpouse storage providers

### awsElasticBlockStore {#awselasticblockstore}

An `awsElasticBlockStore` volume mounts a filesystem stored on an Amazon Web Services (AWS) _[EBS](https://aws.amazon.com/ebs/) volume_ into your pod.  Unlike `emptyDir`, which is erased when a pod is removed, the contents of an EBS
volume are preserved and the volume is merely unmounted.  This means that an
EBS volume can be pre-populated with data, and that data can be shared
between pods.

If you manually specify an `awsElasticBlockStore` volume, you must create an EBS volume using `aws ec2 create-volume` or the AWS API before you can use it.

Dynamic provisioning is a feature of the [AWS EBS CSI driver](https://github.com/kubernetes-sigs/aws-ebs-csi-driver). The [AWS EKS documentation](https://docs.aws.amazon.com/eks/latest/userguide/ebs-csi.html) provides more information on dynamic provisioning of EBS volumes.

There are some restrictions when using an `awsElasticBlockStore` volume:

* the nodes on which pods are running must be AWS EC2 instances
* those instances need to be in the same region and availability-zone as the EBS volume
* EBS only supports a single EC2 instance mounting a volume

#### Creating an AWS EBS volume

Before you can use an EBS volume with a pod, you need to create it.

```shell
aws ec2 create-volume --availability-zone=eu-west-1a --size=10 --volume-type=gp2
```

Make sure the zone matches the zone where you want to mount that volume. Also check that the size and EBS volume type are suitable for your use.

#### AWS EBS configuration example

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: webserver-using-aws-ebs
spec:
  containers:
  - image: k8s.gcr.io/test-webserver
    name: test-container
    volumeMounts:
    - mountPath: /test-ebs
      name: test-volume
  volumes:
  - name: test-volume
    # This AWS EBS volume must already exist.
    awsElasticBlockStore:
      volumeID: <volume-id>
      fsType: ext4
```

If the EBS volume is partitioned, you can supply the optional field `partition: "<partition number>"` to specify which parition to mount on.

#### AWS EBS CSI migration

{{< feature-state for_k8s_version="v1.17" state="beta" >}}

The `CSIMigration` feature for `awsElasticBlockStore`, when enabled, redirects
all plugin operations from the existing in-tree plugin to the `ebs.csi.aws.com` Container
Storage Interface (CSI) driver. In order to use this feature, the [AWS EBS CSI
driver](https://github.com/kubernetes-sigs/aws-ebs-csi-driver)
must be installed on the cluster and the `CSIMigration` and `CSIMigrationAWS`
beta features must be enabled.

#### AWS EBS CSI migration complete
{{< feature-state for_k8s_version="v1.17" state="alpha" >}}

To turn off the awsElasticBlockStore storage plugin from being loaded by controller manager and kubelet, you need to set this feature flag to true. This requires `ebs.csi.aws.com` Container Storage Interface (CSI) driver being installed on all worker nodes.

### azureDisk {#azuredisk}

The `azureDisk` volume type mounts a Microsoft Azure [Data Disk](https://docs.microsoft.com/en-us/azure/aks/csi-storage-driver) into a pod.

For more details, see the [`azureDisk` volume plugin](https://github.com/kubernetes/examples/tree/{{< param "githubbranch" >}}/staging/volumes/azure_disk/README.md).

#### azureDisk CSI migration

{{< feature-state for_k8s_version="v1.21" state="beta" >}}

The `CSIMigration` feature for `azureFile`, when enabled, redirects all plugin operations
from the existing in-tree plugin to the `file.csi.azure.com` Container
Storage Interface (CSI) Driver. In order to use this feature, the [Azure File CSI
Driver](https://github.com/kubernetes-sigs/azurefile-csi-driver)
must be installed on the cluster and the `CSIMigration` and `CSIMigrationAzureFile`
[feature gates](/docs/reference/command-line-tools-reference/feature-gates/) must be enabled.

Azure File CSI driver does not support using same volume with different fsgroups, if Azurefile CSI migration is enabled, using same volume with different fsgroups won't be supported at all.

### azureFile {#azurefile}

A `azureFile` volume type mounts a Microsoft Azure File volume (SMB 2.1 and 3.0)
into a pod.

For more details, see the [`azureFile` volume plugin](https://github.com/kubernetes/examples/tree/{{< param "githubbranch" >}}/staging/volumes/azure_file/README.md).

#### azureFile CSI migration

{{< feature-state for_k8s_version="v1.15" state="alpha" >}}

The CSI Migration feature for azureFile, when enabled, redirects all plugin operations
from the existing in-tree plugin to the `file.csi.azure.com` Container
Storage Interface (CSI) Driver. In order to use this feature, the [Azure File CSI
Driver](https://github.com/kubernetes-sigs/azurefile-csi-driver)
must be installed on the cluster and the `CSIMigration` and `CSIMigrationAzureFile`
Alpha features must be enabled.

### cephfs

A `cephfs` volume mounts an existing CephFS volume to your pod. CephFS can be mounted by multiple writers simultaneously.

See the [CephFS example](https://github.com/kubernetes/examples/tree/{{< param "githubbranch" >}}/volumes/cephfs/) for more details.

### cinder {#cinder}

{{< note >}}
Kubernetes must be configured with the OpenStack cloud provider.
{{< /note >}}

The `cinder` volume type is used to mount the OpenStack Cinder volume into your pod. 

#### Cinder volume configuration example

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: test-cinder
spec:
  containers:
  - image: k8s.gcr.io/test-webserver
    name: test-cinder-container
    volumeMounts:
    - mountPath: /test-cinder
      name: test-volume
  volumes:
  - name: test-volume
    # This OpenStack volume must already exist.
    cinder:
      volumeID: <volume-id>
      fsType: ext4
```

#### OpenStack CSI migration

{{< feature-state for_k8s_version="v1.21" state="beta" >}}

The `CSIMigration` feature for Cinder is enabled by default in Kubernetes 1.21.
It redirects all plugin operations from the existing in-tree plugin to the
`cinder.csi.openstack.org` Container Storage Interface (CSI) Driver.
[OpenStack Cinder CSI Driver](https://github.com/kubernetes/cloud-provider-openstack/blob/master/docs/cinder-csi-plugin/using-cinder-csi-plugin.md)
must be installed on the cluster.
You can disable Cinder CSI migration for your cluster by setting the `CSIMigrationOpenStack` 
[feature gate](/docs/reference/command-line-tools-reference/feature-gates/) to `false`.
If you disable the `CSIMigrationOpenStack` feature, the in-tree Cinder volume plugin takes responsibility
for all aspects of Cinder volume storage management.

### fc (fibre channel) {#fc}

An `fc` volume type allows an existing fibre channel block storage volume
to mount in a pod. You can specify single or multiple target world wide names (WWNs)
using the parameter `targetWWNs` in your Volume configuration. If multiple WWNs are specified,
targetWWNs expect that those WWNs are from multi-path connections.

You must configure FC SAN Zoning to allocate and mask those LUNs (volumes) to the target WWNs beforehand so that Kubernetes hosts can access them.

See the [fibre channel example](https://github.com/kubernetes/examples/tree/{{< param "githubbranch" >}}/staging/volumes/fibre_channel) for more details.

### gcePersistentDisk 

A `gcePersistentDisk` volume mounts a Google Compute Engine (GCE)
[persistent disk](https://cloud.google.com/compute/docs/disks) into your pod.  Unlike `emptyDir`, which is erased when a pod is removed, the contents of a PD are
preserved and the volume is merely unmounted.  This means that a PD can be
pre-populated with data, and that data can be shared between pods.

{{< caution >}}
You must create a PD using `gcloud` or the GCE API or UI before you can use it.
{{< /caution >}}

There are some restrictions when using a `gcePersistentDisk`:

* the nodes on which pods are running must be GCE VMs
* those VMs need to be in the same GCE project and zone as the persistent disk.

One feature of GCE persistent disk is concurrent read-only access to a persistent disk.
A `gcePersistentDisk` volume permits multiple consumers to simultaneously
mount a persistent disk as read-only. This means that you can pre-populate a PD with your dataset
and then serve it in parallel from as many Pods as you need. Unfortunately,
PDs can only be mounted by a single consumer in read-write mode. Simultaneous
writers are not allowed.

Using a GCE persistent disk with a Pod controlled by a ReplicaSet will fail unless the PD is read-only or the replica count is 0 or 1.

#### GCE persistent disk {#gce-create-persistent-disk}

Before you can use a GCE persistent disk with a pod, you need to create it.

```shell
gcloud compute disks create --size=500GB --zone=us-central1-a my-data-disk
```

#### GCE persistent disk configuration example

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: webserver-using-gce-pd
spec:
  containers:
  - image: k8s.gcr.io/test-webserver
    name: test-container
    volumeMounts:
    - mountPath: /test-pd
      name: test-volume
  volumes:
  - name: test-volume
    # This GCE PD must already exist.
    gcePersistentDisk:
      pdName: my-data-disk
      fsType: ext4
```

#### Regional Persistent Disks
The [Regional Persistent Disks](https://cloud.google.com/compute/docs/disks/#repds) feature allows the creation of Persistent Disks that are available in two zones within the same region. In order to use this feature, the volume must be provisioned as a PersistentVolume; referencing the volume directly from a pod is not supported.

#### Manually provisioning a Regional PD PersistentVolume
Dynamic provisioning is possible using a [StorageClass for GCE PD](/docs/concepts/storage/storage-classes/#gce-pd).
Before creating a PersistentVolume, you must create the PD:
```shell
gcloud compute disks create --size=500GB my-data-disk
  --region us-central1
  --replica-zones us-central1-a,us-central1-b
```
#### Regional persistent disk configuration example

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: test-volume
spec:
  capacity:
    storage: 400Gi
  accessModes:
  - ReadWriteOnce
  gcePersistentDisk:
    pdName: my-data-disk
    fsType: ext4
  nodeAffinity:
    required:
      nodeSelectorTerms:
      - matchExpressions:
        - key: failure-domain.beta.kubernetes.io/zone
          operator: In
          values:
          - us-central1-a
          - us-central1-b
```

#### GCE CSI migration

{{< feature-state for_k8s_version="v1.17" state="beta" >}}

The `CSIMigration` feature for GCE PD, when enabled, redirects all plugin operations
from the existing in-tree plugin to the `pd.csi.storage.gke.io` Container
Storage Interface (CSI) Driver. In order to use this feature, the [GCE PD CSI
Driver](https://github.com/kubernetes-sigs/gcp-compute-persistent-disk-csi-driver)
must be installed on the cluster and the `CSIMigration` and `CSIMigrationGCE`
beta features must be enabled.

### iscsi

An `iscsi` volume mounts existing iSCSI (SCSI over IP) volume to into your pod. Unlike `emptyDir`, which is erased when a pod is removed, the
contents of an `iscsi` volume are preserved and the volume is merely
unmounted. This means that an iSCSI volume can be pre-populated with data, and
that data can be shared between pods.

You must have your own iSCSI server running with the volume created before you can use it.

A feature of iSCSI is that it can be mounted as read-only by multiple consumers
simultaneously. This means that you can pre-populate a volume with your dataset
and then serve it in parallel from as many pods as you need. Unfortunately,
iSCSI volumes can only be mounted by a single consumer in read-write mode.
Simultaneous writers are not allowed.

See the [iSCSI example](https://github.com/kubernetes/examples/tree/{{< param "githubbranch" >}}/volumes/iscsi) for more details.

### nfs

An `nfs` volume mounts an existing NFS (Network File System) share to into a pod. Unlike `emptyDir`, which is erased when a pod is
removed, the contents of an `nfs` volume are preserved and the volume is merely
unmounted. This means that an NFS volume can be pre-populated with data, and
that data can be shared between pods. NFS can be mounted by multiple
writers simultaneously.

You must have your own NFS server running with the share exported before you can use it.

See the [NFS example](https://github.com/kubernetes/examples/tree/{{< param "githubbranch" >}}/staging/volumes/nfs) for more details.

### portworxVolume {#portworxvolume}

A `portworxVolume` is an elastic block storage layer that runs hyperconverged with Kubernetes. [Portworx](https://portworx.com/use-case/kubernetes-storage/) fingerprints storage in a server, tiers based on capabilities,
and aggregates capacity across multiple servers. Portworx runs in-guest in virtual machines or on bare metal Linux nodes.

A `portworxVolume` can be dynamically created through Kubernetes or it can also
be pre-provisioned and referenced inside a Kubernetes pod. Here is an example pod referencing a *pre-provisioned* PortworxVolume:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: test-portworx-volume-pod
spec:
  containers:
  - image: k8s.gcr.io/test-webserver
    name: test-container
    volumeMounts:
    - mountPath: /mnt
      name: pxvol
  volumes:
  - name: pxvol
    # This Portworx volume must already exist.
    portworxVolume:
      volumeID: "pxvol"
      fsType: "<fs-type>"
```

More details and examples can be found [here](https://github.com/kubernetes/examples/tree/{{< param "githubbranch" >}}/staging/volumes/portworx/README.md).

### rbd

An `rbd` volume allows a
[Rados Block Device](https://docs.ceph.com/en/latest/rbd/) (RBD) volume to mount into your
Pod. Unlike `emptyDir`, which is erased when a pod is removed, the contents of
an `rbd` volume are preserved and the volume is unmounted. This
means that a RBD volume can be pre-populated with data, and that data can
be shared between pods.

You must have your own Ceph installation running before you can use RBD.

A feature of RBD is that it can be mounted as read-only by multiple consumers
simultaneously. This means that you can pre-populate a volume with your dataset
and then serve it in parallel from as many pods as you need. Unfortunately,
only a single consumer can mount an RBD volume in read-write mode.
Simultaneous writers are not allowed.

See the [RBD example](https://github.com/kubernetes/examples/tree/{{< param "githubbranch" >}}/volumes/rbd)
for more details.

### vsphereVolume {#vspherevolume}

A `vsphereVolume` is used to mount a VMWare vSphere VMDK Volume into your pod.  The contents of a volume are preserved when it is unmounted. It supports both VMFS and VSAN datastore.

You must configure the Kubernetes vSphere Cloud Provider. For cloudprovider configruation, refer to the [vSphere Getting Started guide](https://vmware.github.io/vsphere-storage-for-kubernetes/documentation/).

#### Creating a VMDK volume  {#creating-vmdk-volume}

Choose one of the following methods to create a VMDK.

{{< tabs name="tabs_volumes" >}}
{{% tab name="Create using vmkfstools" %}}
First ssh into ESX, then use the following command to create a VMDK:

```shell
vmkfstools -c 2G /vmfs/volumes/DatastoreName/volumes/myDisk.vmdk
```
{{% /tab %}}
{{% tab name="Create using vmware-vdiskmanager" %}}
Use the following command to create a VMDK:

```shell
vmware-vdiskmanager -c -t 0 -s 40GB -a lsilogic myDisk.vmdk
```

{{% /tab %}}

{{< /tabs >}}


#### vSphere VMDK configuration example {#vsphere-vmdk-configuration}

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: test-vmdk
spec:
  containers:
  - image: k8s.gcr.io/test-webserver
    name: test-container
    volumeMounts:
    - mountPath: /test-vmdk
      name: test-volume
  volumes:
  - name: test-volume
    # This VMDK volume must already exist.
    vsphereVolume:
      volumePath: "[DatastoreName] volumes/myDisk"
      fsType: ext4
```

For more information, see the [vSphere volume]](https://github.com/kubernetes/examples/tree/master/staging/volumes/vsphere) examples.

#### vSphere CSI migration {#vsphere-csi-migration}

{{< feature-state for_k8s_version="v1.19" state="beta" >}}

The `CSIMigration` feature for vsphereVolume, when enabled, redirects all plugin operations
from the existing in-tree plugin to the `csi.vsphere.vmware.com` {{< glossary_tooltip text="CSI" term_id="csi" >}} driver. In order to use this feature, the [vSphere CSI
Driver](https://github.com/kubernetes-sigs/vsphere-csi-driver)
must be installed on the cluster and the `CSIMigration` and `CSIMigrationvSphere`
[feature gates](/docs/reference/command-line-tools-reference/feature-gates/) must be enabled.

This also requires minimum vSphere vCenter/ESXi Version to be 7.0u1 and minimum HW Version to be VM version 15.

{{< note >}}
The following StorageClass parameters from the built-in `vsphereVolume` plugin are not supported by the vSphere CSI driver:

* `diskformat`
* `hostfailurestotolerate`
* `forceprovisioning`
* `cachereservation`
* `diskstripes`
* `objectspacereservation`
* `iopslimit`

Existing volumes created using these parameters will be migrated to the vSphere CSI driver, but new volumes created by the vSphere CSI driver will not be honoring these parameters.
{{< /note >}}

#### vSphere CSI migration complete {#vsphere-csi-migration-complete}
{{< feature-state for_k8s_version="v1.19" state="beta" >}}

To turn off the `vsphereVolume` plugin from being loaded by the controller manager and the kubelet, you need to set this feature flag to `true`. You must install a `csi.vsphere.vmware.com` {{< glossary_tooltip text="CSI" term_id="csi" >}} driver on all worker nodes.


## {{% heading "whatsnext" %}}

Learn more about [Persistent Volumes](/docs/concepts/storage/persistent-volumes/) and managing storage declaratively.

Learn about [mounting a sub-path of a volume based on an environment variable](docs/tasks/administer-cluster/subpath-env). 

Learn about sharing a volume with multiple containers via [mount propagation](docs/concepts/storage/mount-propagation). 
