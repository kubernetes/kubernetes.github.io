---
title: Resource Types
content_type: reference
---

<!-- overview -->

This page provides information on the different resource types you can request, built into Kubernetes.

<!-- body -->

There are several different resource types: `cpu`, `memory`, `storage`, `hugepages-*`, and `emphemeral-storage`.


Resource requests on Pods are an integral part of scheduling and 
limiting and managing resource consumption in a Kubernetes 
cluster. 
See [Kubernetes Scheduler](/docs/concepts/scheduling-eviction/kube-scheduler/) and [Requests and Limits](/docs/concepts/configuration/manage-resources-containers/#requests-and-limits) for more details.
## CPU 
The `cpu` resource represents CPU in cores and can be specified as either a decimal (e.g. `1`, `0.5`) or as millicores (e.g. `500m`, `1000m`). `0.5` = `500m`.

You can request or limit the `cpu` resource for Pods and their containers, and any for object that embeds a [Pod template](/docs/concepts/workloads/pods/#pod-templates).

When the cpu limit is reached, the Pod is throttled.

See [Meaning of CPU](/docs/concepts/configuration/manage-resources-containers/#meaning-of-cpu) for more details on what CPU means in kubernetes.

## Memory
The `memory` resource represents memory in bytes and is specified with a number and a binary suffix. e.g. `500Mi` = `500MiB` = `500 * 1024 * 1024`. 

You can request or limit the `memory` resource in Pods and their containers, and any object that embeds a Pod template.

In contrast with cpu, when the memory limit is reached, the 
Pod is killed.

See [Meaning of Memory](/docs/concepts/configuration/manage-resources-containers/#meaning-of-memory) for more details on what memory means in kubernetes.

## Storage 
The `storage` resource represents volume size in bytes and is specified with a number and a binary suffix. e.g. `500Gi` = `500GiB` = `500 * 1024 * 1024 * 1024`

You can use the `storage` resource in a [PersistentVolumeClaim](/docs/concepts/storage/persistent-volumes/#introduction).

## Huge pages

On Kubernetes v1.14 and newer you can request the `hugepages-*` 
resource. Huge pages are a Linux-specific feature where the node 
kernel allocates blocks of memory that are much larger than the 
default page size.

You cannot overcommit `hugepages-*` resources. This is different from the `memory` and `cpu` resources.

You request huge pages with a combination of two binary
suffixes. The first is part of the resource name in the request: 
e.g. `hugepages-2Mi`. It specifies the size of the pages. The second part is the value of allocatable pages e.g. `80Mi`. 

## Emphemeral storage

Emphemeral storage is storage provided to pods that has no 
long-term gurantee of durablity. Empheral Storage is in beta. 
Empheral storage is represented in bytes and is specified with a 
number and a binary suffix. e.g. `500Mi` = `500MiB` = `500 * 1024 * 1024`. 

You can specify the `ephemeral-storage` resource in Pods and any object that embeds a Pod template.

See [Local emphemeral storage](/docs/concepts/configuration/manage-resources-containers/#local-ephemeral-storage) for more details.

## Examples
### CPU and memory

```yaml
apiVersion: v1
kind: Pod
metadata:
  ...
spec:
  ...
  requests:
    cpu: 500m
    memory: 250Mi
  limits:
    cpu: 700m
    memory: 500Mi
```

### Storage

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  ...
spec:
  ...
  requests:
    storage: 20Gi
```

### Huge pages
```yaml
apiVersion: v1
kind: Pod
metadata:
  ...
spec:
  ...
  requests:
    hugepages-2Mi: 80Mi
  limits:
    hugepages-2Mi: 100Mi
```

### Emphemeral Storage

```yaml
apiVersion: v1
kind: Pod
metadata:
  ...
spec:
  ...
  requests:
    emphemeral-storage: 100Mi
  limits:
    emphemeral-storage: 500Mi
```
