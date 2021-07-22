---
reviewers:
- tallclair
- dchen1107
title: Runtime Class
content_type: concept
weight: 20
---

<!-- overview -->

{{< feature-state for_k8s_version="v1.20" state="stable" >}}

This page describes the RuntimeClass resource and runtime selection mechanism.

RuntimeClass is a feature for selecting the container runtime configuration. The container runtime
configuration is used to run a Pod's containers.




<!-- body -->

## Motivation

You can set a different RuntimeClass between different Pods to provide a balance of
performance versus security. For example, if part of your workload deserves a high
level of information security assurance, you might choose to schedule those Pods so
that they run in a container runtime that uses hardware virtualization. You'd then
benefit from the extra isolation of the alternative runtime, at the expense of some
additional overhead.

You can also use RuntimeClass to run different Pods with the same container runtime
but with different settings.

## Setup

1. Configure the CRI implementation on nodes (runtime dependent)
2. Create the corresponding RuntimeClass resources

### 1. Configure the CRI implementation on nodes

The configurations available through RuntimeClass are Container Runtime Interface (CRI)
implementation dependent. See the corresponding documentation ([below](#cri-configuration)) for your
CRI implementation for how to configure.

{{< note >}}
RuntimeClass assumes a homogeneous node configuration across the cluster by default (which means
that all nodes are configured the same way with respect to container runtimes). To support
heterogeneous node configurations, see [Scheduling](#scheduling) below.
{{< /note >}}

The configurations have a corresponding `handler` name, referenced by the RuntimeClass. The
handler must be a valid [DNS label name](/docs/concepts/overview/working-with-objects/names/#dns-label-names).

### 2. Create the corresponding RuntimeClass resources

The configurations setup in step 1 should each have an associated `handler` name, which identifies
the configuration. For each handler, create a corresponding RuntimeClass object.

The RuntimeClass resource currently only has 2 significant fields: the RuntimeClass name
(`metadata.name`) and the handler (`handler`). The object definition looks like this:

```yaml
apiVersion: node.k8s.io/v1  # RuntimeClass is defined in the node.k8s.io API group
kind: RuntimeClass
metadata:
  name: myclass  # The name the RuntimeClass will be referenced by
  # RuntimeClass is a non-namespaced resource
handler: myconfiguration  # The name of the corresponding CRI configuration
```

The name of a RuntimeClass object must be a valid
[DNS subdomain name](/docs/concepts/overview/working-with-objects/names#dns-subdomain-names).

{{< note >}}
It is recommended that RuntimeClass write operations (create/update/patch/delete) be
restricted to the cluster administrator. This is typically the default. See [Authorization
Overview](/docs/reference/access-authn-authz/authorization/) for more details.
{{< /note >}}

## Usage

Once RuntimeClasses are configured for the cluster, using them is very simple. Specify a
`runtimeClassName` in the Pod spec. For example:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: mypod
spec:
  runtimeClassName: myclass
  # ...
```

This will instruct the kubelet to use the named RuntimeClass to run this pod. If the named
RuntimeClass does not exist, or the CRI cannot run the corresponding handler, the pod will enter the
`Failed` terminal [phase](/docs/concepts/workloads/pods/pod-lifecycle/#pod-phase). Look for a
corresponding [event](/docs/tasks/debug-application-cluster/debug-application-introspection/) for an
error message.

If no `runtimeClassName` is specified, the default RuntimeHandler will be used, which is equivalent
to the behavior when the RuntimeClass feature is disabled.

### CRI Configuration

For more details on setting up CRI runtimes, see [CRI installation](/docs/setup/production-environment/container-runtimes/).

#### dockershim

RuntimeClasses with dockershim must set the runtime handler to `docker`. Dockershim does not support
custom configurable runtime handlers.

#### {{< glossary_tooltip term_id="containerd" >}}

Runtime handlers are configured through containerd's configuration at
`/etc/containerd/config.toml`. Valid handlers are configured under the runtimes section:

```
[plugins."io.containerd.grpc.v1.cri".containerd.runtimes.${HANDLER_NAME}]
```

See containerd's config documentation for more details:
https://github.com/containerd/cri/blob/master/docs/config.md

#### {{< glossary_tooltip term_id="cri-o" >}}

Runtime handlers are configured through CRI-O's configuration at `/etc/crio/crio.conf`. Valid
handlers are configured under the [crio.runtime
table](https://github.com/cri-o/cri-o/blob/master/docs/crio.conf.5.md#crioruntime-table):

```
[crio.runtime.runtimes.${HANDLER_NAME}]
  runtime_path = "${PATH_TO_BINARY}"
```

See CRI-O's [config documentation](https://github.com/cri-o/cri-o/blob/master/docs/crio.conf.5.md) for more details.

## Scheduling

{{< feature-state for_k8s_version="v1.16" state="beta" >}}

By specifying the `scheduling` field for a RuntimeClass, you can set constraints to
ensure that Pods running with this RuntimeClass are scheduled to nodes that support it.
If `scheduling` is not set, this RuntimeClass is assumed to be supported by all nodes.

To ensure pods land on nodes supporting a specific RuntimeClass, that set of nodes should have a
common label which is then selected by the `runtimeclass.scheduling.nodeSelector` field. The
RuntimeClass's nodeSelector is merged with the pod's nodeSelector in admission, effectively taking
the intersection of the set of nodes selected by each. If there is a conflict, the pod will be
rejected.

If the supported nodes are tainted to prevent other RuntimeClass pods from running on the node, you
can add `tolerations` to the RuntimeClass. As with the `nodeSelector`, the tolerations are merged
with the pod's tolerations in admission, effectively taking the union of the set of nodes tolerated
by each.

To learn more about configuring the node selector and tolerations, see [Assigning Pods to
Nodes](/docs/concepts/scheduling-eviction/assign-pod-node/).

### Pod Overhead

{{< feature-state for_k8s_version="v1.18" state="beta" >}}

You can specify _overhead_ resources that are associated with running a Pod. Declaring overhead allows
the cluster (including the scheduler) to account for it when making decisions about Pods and resources.
To use Pod overhead, you must have the PodOverhead [feature gate](/docs/reference/command-line-tools-reference/feature-gates/)
enabled (it is on by default).

Pod overhead is defined in RuntimeClass through the `overhead` fields. Through the use of these fields,
you can specify the overhead of running pods utilizing this RuntimeClass and ensure these overheads
are accounted for in Kubernetes.


## {{% heading "whatsnext" %}}


- [RuntimeClass Design](https://github.com/kubernetes/enhancements/blob/master/keps/sig-node/585-runtime-class/README.md)
- [RuntimeClass Scheduling Design](https://github.com/kubernetes/enhancements/blob/master/keps/sig-node/585-runtime-class/README.md#runtimeclass-scheduling)
- Read about the [Pod Overhead](/docs/concepts/scheduling-eviction/pod-overhead/) concept
- [PodOverhead Feature Design](https://github.com/kubernetes/enhancements/tree/master/keps/sig-node/688-pod-overhead)
