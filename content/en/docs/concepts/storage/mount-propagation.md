---
reviewers:
- saad-ali
- jsafrane
- thockin
- msau42
title: Mount Propagation
content_type: concept
weight: 40
---

<!-- overview -->

Mount propagation allows for sharing a {{< glossary_tooltip text="volume" term_id="volume" >}} mounted
by a container to other containers in the same {{< glossary_tooltip text="pod" term_id="pod" >}}, or even to other pods on the same {{< glossary_tooltip text="node" term_id="node" >}}.

<!-- body -->

Mount propagation of a volume is controlled by the `mountPropagation` field within `volumeMounts`.
Its values are:

* `None` (Default) - This volume mount does not receive any subsequent mounts
  that are mounted to this volume or any of its subdirectories by the host.
  In similar fashion, no mounts created by the container will be visible on
  the host. This is the default mode.

  This mode is equal to `private` mount propagation as described in the
  [Linux kernel documentation](https://www.kernel.org/doc/Documentation/filesystems/sharedsubtree.txt)

* `HostToContainer` - This volume mount receives all subsequent mounts
  that are mounted to this volume or any of its subdirectories.

  In other words, if the host mounts anything inside the volume mount, the
  container will see it mounted there.

  Similarly, if any pod with `Bidirectional` mount propagation to the same
  volume mounts anything there, the container with `HostToContainer` mount
  propagation will see it.

  This mode is equal to `rslave` mount propagation as described in the
  [Linux kernel documentation](https://www.kernel.org/doc/Documentation/filesystems/sharedsubtree.txt)

* `Bidirectional` - This volume mount behaves the same as the `HostToContainer` mount. In addition, all volume mounts created by the container are propagated
  back to the host and to all containers of all pods that use the same volume.

  A typical use case for this mode is a pod with a FlexVolume or CSI driver or
  a pod that needs to mount something on the host using a `hostPath` volume.

  This mode is equal to `rshared` mount propagation as described in the
  [Linux kernel documentation](https://www.kernel.org/doc/Documentation/filesystems/sharedsubtree.txt)

  {{< warning >}}
  `Bidirectional` mount propagation can be dangerous. It can damage
  the host operating system and therefore it is allowed only in privileged  
   containers. Familiarity with Linux kernel behavior is strongly recommended.
  {{< /warning >}}

### Docker mount propagation configuration
Before mount propagation can work properly on some deployments (CoreOS,
RedHat/Centos, Ubuntu), mount share must be configured correctly in
Docker as shown below.

Edit your Docker's `systemd` service file. Set `MountFlags` as follows:
```shell
MountFlags=shared
```

Or, remove `MountFlags=slave` if present. Then restart the Docker daemon:

```shell
sudo systemctl daemon-reload
sudo systemctl restart docker
```

## {{% heading "whatsnext" %}}

Learn more about managing storage declaratively using [Persistent Volumes](docs/concepts/storage/persistent-volumes/).
