---
title: Resource Types
content_type: reference
---

<!-- overview -->

This page provides information on the different resource types you can request, built into Kubernetes.

<!-- body -->

There are 3 different resource types: `cpu`, `memory`, and `storage`.

## CPU 
The `cpu` resource represents CPU in cores and can be specified as either a decimal (e.g. `1`, `0.5`) or as millicores (e.g. `500m`, `1000m`). `0.5` = `500m`.

You can request or limit the `cpu` resource for Pods and their containers, and any for object that embeds a [Pod template](https://kubernetes.io/docs/concepts/workloads/pods/#pod-templates).

## Memory
The `memory` resource represents memory in bytes and is specified with a number and a binary suffix. e.g. `500Mi` = `500MiB` = `500 * 1024 * 1024`. 

You can use the memory resource in Pods and any object that embeds a Pod template.

## Storage 
The `storage` resource represents volume size in bytes and is specified with a number and a binary suffix. e.g. `500Gi` = `500GiB` = `500 * 1024 * 1024 * 1024`

You can use the `storage` resource in a PersistentVolumeClaim.

Examples: 
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
