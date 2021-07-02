---
title: Create a Windows HostProcess Container
content_type: task
weight: 20
---

<!-- overview -->

{{< feature-state for_k8s_version="v1.22" state="alpha" >}}

Windows HostProcess containers enable you to run containerized administrative workloads on a Windows host. These containers operate as normal processes and have access to the host network namespace, storage, and devices when given the associated user privileges. HostProcess containers can be used to deploy networking policies, storage configurations, device plugins, kube-proxy, and other components to Windows nodes without the need for dedicated proxies or the direct installation of services on the Windows nodes.

Administrative tasks such as installation of security patches, event log collection, and more can be performed without requiring cluster operations to log onto each Window node. HostProcess containers can run as any user that is available on the host or is in the domain of the host machine, allowing administrators to restrict resource access through user permissions. While neither filesystem or process isolation are supported, a new volume is created on the host upon starting the container to give it a clean and consolidated workspace. HostProcess containers can also be built on top of existing Windows base images and do not inherit the same [compatibility requirements](https://docs.microsoft.com/virtualization/windowscontainers/deploy-containers/version-compatibility) as Windows server containers.

### When should I use a Windows HostProcess container?

- When you need to perform tasks which require the networking namespace of the host. HostProcess containers have access to the host's network interfaces and IP.
- You need access to the host's filesystem
- Installation of specific devices drivers or services
- Consolidation of administrative tasks and security policies. This reduces the degree of privileges needed by Windows nodes.

### Important Notes

- HostProcess container will **only run via containerd**.
- As of v1.22 HostProcess containers cannot share the same pod as non-privileged containers. This is a current limitation of the Windows OS; non-privileged containers cannot share a vNIC with the host IP namespace.
- HostProcess containers run as a process on the host and do not have any degree of isolation other than resource constraints imposed on the HostProcess user account. Neither filesystem or Hyper-V isolation are supported for HostProcess containers.
- Resource limits (disk, memory, cpu count) are supported in the same fashion as processes on the host.
- Named pipe mounts will **not** be supported and should instead be accessed via their path on the host (\\.\pipe\*).
    - Unix domain sockets, however, are supported
- Volume mounts are supported and are mounted under the container volume.
- [todo] Skipping host file mounting

## {{% heading "prerequisites" %}}
[todo] Enabling the feature

[todo] Version requirements

## Creating HostProcess containers

[todo] Testing HostProcess containers in a dev environment

[todo] Deploying HostProcess containers

## Choosing a User Account

[todo] Recommended user accounts

[todo] Using runas + changing the user

## Example Specs

[todo] example specs
