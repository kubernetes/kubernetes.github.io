---
title: Migrating from compose workflows to Kubernetes
weight: 60
---

## Disclaimer

The [compose specification](https://github.com/compose-spec/compose-spec) is evolving, this documentation aims to cover the latest version of this compose specification.
We will assume that we are talking about the latest compose specifications.
If your compose files at not at the latest version specification, we suggest you try to upgrade to the latest spec version first. 

## Differences between compose specification and Kubernetes specification

A set of workflows defined using the compose specification cannot be automated translated to a unique set of Kubernetes objects.
While some notions are very similar, there is not a single way to translate concepts from compose to Kubernetes.
For instance, a [service](https://github.com/compose-spec/compose-spec/blob/master/spec.md#services-top-level-element) concept in compose can be translated in different way in Kubernetes.
In particular a service in compose **IS NOT** equivalent to a service in Kubernetes.

Also, you have features that are available in the compose specifications that do not have a clear equivalent in Kubernetes.

Therefore, these content are only there to be suggestions and not a definitive and absolute guide.

There is an [ongoing work](https://github.com/compose-spec/compose-spec/blob/wip_kube_mapping/KUBERNETES_MAPPING.md) on the compose specification side to give some information about compose to Kubernetes mapping.

## Stateful and stateless workloads

One of the first step to migrate from compose to Kubernetes is to analyze among the different components of the compose files the sub-systems that are stateless, and the one that are stateful.

### Stateless applications

Stateless applications is one which depends on no persistent storage.
The only thing your cluster is responsible for is the code, and other static content, being hosted on it.
That's it, no changing databases, no writes and no left over files when the pod is deleted.

Stateless components are often migrated as [Deployment](/docs/concepts/workloads/controllers/deployment/) objects in Kubernetes.

### Stateful applications

Stateful applications save data to persistent disk storage for use by the server, by clients, and by other applications.
An example of a stateful application is a database or key-value store to which data is saved and retrieved by other applications.
In the case of compose, this data could be persisted either on disk or on a different host.

Stateful applications can use [StatefulSet](/docs/concepts/workloads/controllers/statefulset/) objects to migrate.

## Tools

Some tools provide support to create automated translation from compose to Kubernetes.
Be aware that automated translations don't always work as there is no exact mapping:

- [Kompose](https://kompose.io/) (To get started, checkout [this tutorial](/docs/tasks/configure-pod-container/translate-compose-kubernetes/))
