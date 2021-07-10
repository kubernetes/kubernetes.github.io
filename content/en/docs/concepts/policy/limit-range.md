---
reviewers:
- nelvadas
title: Limit Ranges
content_type: concept
weight: 10
---

<!-- overview -->

By default, containers run with unbounded [compute resources](/docs/concepts/configuration/manage-resources-containers/) on a Kubernetes cluster.
With resource quotas, cluster administrators can restrict resource consumption and creation on a {{< glossary_tooltip text="namespace" term_id="namespace" >}} basis.
Within a namespace, a Pod or Container can consume as much CPU and memory as defined by the namespace's resource quota. There is a concern that one Pod or Container could monopolize all available resources. A LimitRange is a policy to constrain resource allocations (to Pods or Containers) in a namespace.

<!-- body -->

A _LimitRange_ provides constraints that can:

- Enforce minimum and maximum compute resources usage per Pod or Container in a namespace.
- Enforce minimum and maximum storage request per PersistentVolumeClaim in a namespace.
- Enforce a ratio between request and limit for a resource in a namespace.
- Set default request/limit for compute resources in a namespace and automatically inject them to Containers at runtime.

## Enabling LimitRange

LimitRange support has been enabled by default since Kubernetes 1.10.

A LimitRange is enforced in a particular namespace when there is a
LimitRange object in that namespace.

The name of a LimitRange object must be a valid
[DNS subdomain name](/docs/concepts/overview/working-with-objects/names#dns-subdomain-names).

### Overview of Limit Range

- The administrator creates one LimitRange in one namespace.
- Users create resources like Pods, Containers, and PersistentVolumeClaims in the namespace.
- The `LimitRanger` admission controller enforces defaults and limits for all Pods and Containers that do not set compute resource requirements and tracks usage to ensure it does not exceed resource minimum, maximum and ratio defined in any LimitRange present in the namespace.
- If creating or updating a resource (Pod, Container, PersistentVolumeClaim) that violates a LimitRange constraint, the request to the API server will fail with an HTTP status code `403 FORBIDDEN` and a message explaining the constraint that have been violated.
- If a LimitRange is activated in a namespace for compute resources like `cpu` and `memory`, users must specify
  requests or limits for those values. Otherwise, the system may reject Pod creation.
- LimitRange validations occurs only at Pod Admission stage, not on Running Pods.

Examples of policies that could be created using limit range are:

- In a 2 node cluster with a capacity of 8 GiB RAM and 16 cores, constrain Pods in a namespace to request 100m of CPU with a max limit of 500m for CPU and request 200Mi for Memory with a max limit of 600Mi for Memory.
- Define default CPU limit and request to 150m and memory default request to 300Mi for Containers started with no cpu and memory requests in their specs.

In the case where the total limits of the namespace is less than the sum of the limits of the Pods/Containers,
there may be contention for resources. In this case, the Containers or Pods will not be created.

Neither contention nor changes to a LimitRange will affect already created resources.

## {{% heading "whatsnext" %}}

Refer to the [LimitRanger design document](https://git.k8s.io/community/contributors/design-proposals/resource-management/admission_control_limit_range.md) for more information.

For examples on using limits, see:

- [how to configure minimum and maximum CPU constraints per namespace](/docs/tasks/administer-cluster/manage-resources/cpu-constraint-namespace/).
- [how to configure minimum and maximum Memory constraints per namespace](/docs/tasks/administer-cluster/manage-resources/memory-constraint-namespace/).
- [how to configure default CPU Requests and Limits per namespace](/docs/tasks/administer-cluster/manage-resources/cpu-default-namespace/).
- [how to configure default Memory Requests and Limits per namespace](/docs/tasks/administer-cluster/manage-resources/memory-default-namespace/).
- [how to configure minimum and maximum Storage consumption per namespace](/docs/tasks/administer-cluster/limit-storage-consumption/#limitrange-to-limit-requests-for-storage).
- a [detailed example on configuring quota per namespace](/docs/tasks/administer-cluster/manage-resources/quota-memory-cpu-namespace/).
- LimitRange is a top-level resource in the Kubernetes REST API.
  The {{< api-reference page="policy-resources/limit-range-v1" >}} object definition describes the object in detail.

