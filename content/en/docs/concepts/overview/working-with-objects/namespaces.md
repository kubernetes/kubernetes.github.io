---
reviewers:
- derekwaynecarr
- mikedanese
- thockin
title: Namespaces
content_type: concept
weight: 30
---

<!-- overview -->

Kubernetes supports multiple virtual clusters backed by the same physical cluster.
These virtual clusters are called namespaces.

<!-- body -->

## When to Use Multiple Namespaces

Namespaces are intended for use in environments with many users spread across multiple
teams, or projects.  For clusters with a few to tens of users, you should not
need to create or think about namespaces at all.  Start using namespaces when you
need the features they provide.

Namespaces provide a scope for names.  Names of resources need to be unique within a namespace,
but not across namespaces. Namespaces cannot be nested inside one another and each Kubernetes 
resource can only be in one namespace.

Namespaces are a way to divide cluster resources between multiple users (via [resource quota](/docs/concepts/policy/resource-quotas/)).

It is not necessary to use multiple namespaces to separate slightly different
resources, such as different versions of the same software: use
{{< glossary_tooltip text="labels" term_id="label" >}} to distinguish
resources within the same namespace.

## Working with Namespaces

Creation and deletion of namespaces are described in the
[Admin Guide documentation for namespaces](/docs/tasks/administer-cluster/namespaces).

{{< note >}}
    Avoid creating namespaces with the prefix `kube-`, since it is reserved for Kubernetes system namespaces.
{{< /note >}}

### Viewing namespaces

You can list the current namespaces in a cluster using:

```shell
kubectl get namespace
```
```
NAME              STATUS   AGE
default           Active   1d
kube-node-lease   Active   1d
kube-public       Active   1d
kube-system       Active   1d
```

Kubernetes starts with four initial namespaces:

   * `default` The default namespace for objects with no other namespace
   * `kube-system` The namespace for objects created by the Kubernetes system
   * `kube-public` This namespace is created automatically and is readable by all users (including those not authenticated). This namespace is mostly reserved for cluster usage, in case that some resources should be visible and readable publicly throughout the whole cluster. The public aspect of this namespace is only a convention, not a requirement.
   * `kube-node-lease` This namespace for the lease objects associated with each node which improves the performance of the node heartbeats as the cluster scales.
   
### Setting the namespace for a request

To set the namespace for a current request, use the `--namespace` flag.

For example:

```shell
kubectl run nginx --image=nginx --namespace=<insert-namespace-name-here>
kubectl get pods --namespace=<insert-namespace-name-here>
```

### Setting the namespace preference

You can permanently save the namespace for all subsequent kubectl commands in that
context.

```shell
kubectl config set-context --current --namespace=<insert-namespace-name-here>
# Validate it
kubectl config view --minify | grep namespace:
```

## Namespaces and DNS

When you create a [Service](/docs/concepts/services-networking/service/),
it creates a corresponding [DNS entry](/docs/concepts/services-networking/dns-pod-service/).
This entry is of the form `<service-name>.<namespace-name>.svc.cluster.local`, which means
that if a container only uses `<service-name>`, it will resolve to the service which
is local to a namespace.  This is useful for using the same configuration across
multiple namespaces such as Development, Staging and Production.  If you want to reach
across namespaces, you need to use the fully qualified domain name (FQDN).

## Not All Objects are in a Namespace

Most Kubernetes resources (e.g. pods, services, replication controllers, and others) are
in some namespaces.  However namespace resources are not themselves in a namespace.
And low-level resources, such as
[nodes](/docs/concepts/architecture/nodes/) and
persistentVolumes, are not in any namespace.

To see which Kubernetes resources are and aren't in a namespace:

```shell
# In a namespace
kubectl api-resources --namespaced=true

# Not in a namespace
kubectl api-resources --namespaced=false
```

## Automatic labelling

{{< feature-state state="beta" for_k8s_version="1.21" >}}

The Kubernetes control plane sets an immutable {{< glossary_tooltip text="label" term_id="label" >}}
`kubernetes.io/metadata.name` on all namespaces, provided that the `NamespaceDefaultLabelName`
[feature gate](/docs/reference/command-line-tools-reference/feature-gates/) is enabled.
The value of the label is the namespace name.


## {{% heading "whatsnext" %}}

* Learn more about [creating a new namespace](/docs/tasks/administer-cluster/namespaces/#creating-a-new-namespace).
* Learn more about [deleting a namespace](/docs/tasks/administer-cluster/namespaces/#deleting-a-namespace).
* Namespace is a top-level resource in the Kubernetes REST API.
  The {{< api-reference page="cluster-resources/namespace-v1" >}} object definition describes the object in detail.
