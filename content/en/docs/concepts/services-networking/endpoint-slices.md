---
reviewers:
- freehan
title: EndpointSlices
content_type: concept
weight: 45
---


<!-- overview -->

{{< feature-state for_k8s_version="v1.21" state="stable" >}}

_EndpointSlices_ provide a simple way to track network endpoints within a
Kubernetes cluster. They offer a more scalable and extensible alternative to
Endpoints.



<!-- body -->

## Motivation

The Endpoints API has provided a simple and straightforward way of
tracking network endpoints in Kubernetes. Unfortunately as Kubernetes clusters
and {{< glossary_tooltip text="Services" term_id="service" >}} have grown to handle and
send more traffic to more backend Pods, limitations of that original API became
more visible.
Most notably, those included challenges with scaling to larger numbers of
network endpoints.

Since all network endpoints for a Service were stored in a single Endpoints
resource, those resources could get quite large. That affected the performance
of Kubernetes components (notably the master control plane) and resulted in
significant amounts of network traffic and processing when Endpoints changed.
EndpointSlices help you mitigate those issues as well as provide an extensible
platform for additional features such as topological routing.

## EndpointSlice resources {#endpointslice-resource}

In Kubernetes, an EndpointSlice contains references to a set of network
endpoints. The control plane automatically creates EndpointSlices
for any Kubernetes Service that has a {{< glossary_tooltip text="selector"
term_id="selector" >}} specified. These EndpointSlices include
references to all the Pods that match the Service selector. EndpointSlices group
network endpoints together by unique combinations of protocol, port number, and
Service name.
The name of a EndpointSlice object must be a valid
[DNS subdomain name](/docs/concepts/overview/working-with-objects/names#dns-subdomain-names).

As an example, here's a sample EndpointSlice resource for the `example`
Kubernetes Service.

```yaml
apiVersion: discovery.k8s.io/v1
kind: EndpointSlice
metadata:
  name: example-abc
  labels:
    kubernetes.io/service-name: example
addressType: IPv4
ports:
  - name: http
    protocol: TCP
    port: 80
endpoints:
  - addresses:
      - "10.1.2.3"
    conditions:
      ready: true
    hostname: pod-1
    nodeName: node-1
    zone: us-west2-a
```

By default, the control plane creates and manages EndpointSlices to have no
more than 100 endpoints each. You can configure this with the
`--max-endpoints-per-slice`
{{< glossary_tooltip text="kube-controller-manager" term_id="kube-controller-manager" >}}
flag, up to a maximum of 1000.

EndpointSlices can act as the source of truth for
{{< glossary_tooltip term_id="kube-proxy" text="kube-proxy" >}} when it comes to
how to route internal traffic. When enabled, they should provide a performance
improvement for services with large numbers of endpoints.

### Address types

EndpointSlices support three address types:

* IPv4
* IPv6
* FQDN (Fully Qualified Domain Name)

### Conditions

The EndpointSlice API stores conditions about endpoints that may be useful for consumers.
The three conditions are `ready`, `serving`, and `terminating`.

#### Ready

`ready` is a condition that maps to a Pod's `Ready` condition. A running Pod with the `Ready`
condition set to `True` should have this EndpointSlice condition also set to `true`. For
compatibility reasons, `ready` is NEVER `true` when a Pod is terminating. Consumers should refer
to the `serving` condition to inspect the readiness of terminating Pods. The only exception to
this rule is for Services with `spec.publishNotReadyAddresses` set to `true`. Endpoints for these
Services will always have the `ready` condition set to `true`.

#### Serving

{{< feature-state for_k8s_version="v1.20" state="alpha" >}}

`serving` is identical to the `ready` condition, except it does not account for terminating states.
Consumers of the EndpointSlice API should check this condition if they care about pod readiness while
the pod is also terminating.

{{< note >}}

Although `serving` is almost identical to `ready`, it was added to prevent break the existing meaning
of `ready`. It may be unexpected for existing clients if `ready` could be `true` for terminating
endpoints, since historically terminating endpoints were never included in the Endpoints or
EndpointSlice API to begin with. For this reason, `ready` is _always_ `false` for terminating
endpoints, and a new condition `serving` was added in v1.20 so that clients can track readiness
for terminating pods independent of the existing semantics for `ready`.

{{< /note >}}

#### Terminating

{{< feature-state for_k8s_version="v1.20" state="alpha" >}}

`Terminating` is a condition that indicates whether an endpoint is terminating.
For pods, this is any pod that has a deletion timestamp set.

### Topology information {#topology}

Each endpoint within an EndpointSlice can contain relevant topology information.
The topology information includes the location of the endpoint and information
about the corresponding Node and zone. These are available in the following
per endpoint fields on EndpointSlices:

* `nodeName` - The name of the Node this endpoint is on.
* `zone` - The zone this endpoint is in.

{{< note >}}
In the v1 API, the per endpoint `topology` was effectively removed in favor of
the dedicated fields `nodeName` and `zone`.

Setting arbitrary topology fields on the `endpoint` field of an `EndpointSlice`
resource has been deprecated and is not be supported in the v1 API. Instead,
the v1 API supports setting individual `nodeName` and `zone` fields. These
fields are automatically translated between API versions. For example, the
value of the `"topology.kubernetes.io/zone"` key in the `topology` field in
the v1beta1 API is accessible as the `zone` field in the v1 API.
{{< /note >}}

### Management

Most often, the control plane (specifically, the endpoint slice
{{< glossary_tooltip text="controller" term_id="controller" >}}) creates and
manages EndpointSlice objects. There are a variety of other use cases for
EndpointSlices, such as service mesh implementations, that could result in other
entities or controllers managing additional sets of EndpointSlices.

To ensure that multiple entities can manage EndpointSlices without interfering
with each other, Kubernetes defines the
{{< glossary_tooltip term_id="label" text="label" >}}
`endpointslice.kubernetes.io/managed-by`, which indicates the entity managing
an EndpointSlice.
The endpoint slice controller sets `endpointslice-controller.k8s.io` as the value
for this label on all EndpointSlices it manages. Other entities managing
EndpointSlices should also set a unique value for this label.

### Ownership

In most use cases, EndpointSlices are owned by the Service that the endpoint
slice object tracks endpoints for. This ownership is indicated by an owner
reference on each EndpointSlice as well as a `kubernetes.io/service-name`
label that enables simple lookups of all EndpointSlices belonging to a Service.

### EndpointSlice mirroring

In some cases, applications create custom Endpoints resources. To ensure that
these applications do not need to concurrently write to both Endpoints and
EndpointSlice resources, the cluster's control plane mirrors most Endpoints
resources to corresponding EndpointSlices.

The control plane mirrors Endpoints resources unless:

* the Endpoints resource has a `endpointslice.kubernetes.io/skip-mirror` label
  set to `true`.
* the Endpoints resource has a `control-plane.alpha.kubernetes.io/leader`
  annotation.
* the corresponding Service resource does not exist.
* the corresponding Service resource has a non-nil selector.

Individual Endpoints resources may translate into multiple EndpointSlices. This
will occur if an Endpoints resource has multiple subsets or includes endpoints
with multiple IP families (IPv4 and IPv6). A maximum of 1000 addresses per
subset will be mirrored to EndpointSlices.

### Distribution of EndpointSlices

Each EndpointSlice has a set of ports that applies to all endpoints within the
resource. When named ports are used for a Service, Pods may end up with
different target port numbers for the same named port, requiring different
EndpointSlices. This is similar to the logic behind how subsets are grouped
with Endpoints.

The control plane tries to fill EndpointSlices as full as possible, but does not
actively rebalance them. The logic is fairly straightforward:

1. Iterate through existing EndpointSlices, remove endpoints that are no longer
   desired and update matching endpoints that have changed.
2. Iterate through EndpointSlices that have been modified in the first step and
   fill them up with any new endpoints needed.
3. If there's still new endpoints left to add, try to fit them into a previously
   unchanged slice and/or create new ones.

Importantly, the third step prioritizes limiting EndpointSlice updates over a
perfectly full distribution of EndpointSlices. As an example, if there are 10
new endpoints to add and 2 EndpointSlices with room for 5 more endpoints each,
this approach will create a new EndpointSlice instead of filling up the 2
existing EndpointSlices. In other words, a single EndpointSlice creation is
preferrable to multiple EndpointSlice updates.

With kube-proxy running on each Node and watching EndpointSlices, every change
to an EndpointSlice becomes relatively expensive since it will be transmitted to
every Node in the cluster. This approach is intended to limit the number of
changes that need to be sent to every Node, even if it may result with multiple
EndpointSlices that are not full.

In practice, this less than ideal distribution should be rare. Most changes
processed by the EndpointSlice controller will be small enough to fit in an
existing EndpointSlice, and if not, a new EndpointSlice is likely going to be
necessary soon anyway. Rolling updates of Deployments also provide a natural
repacking of EndpointSlices with all Pods and their corresponding endpoints
getting replaced.

### Duplicate endpoints

Due to the nature of EndpointSlice changes, endpoints may be represented in more
than one EndpointSlice at the same time. This naturally occurs as changes to
different EndpointSlice objects can arrive at the Kubernetes client watch/cache
at different times. Implementations using EndpointSlice must be able to have the
endpoint appear in more than one slice. A reference implementation of how to
perform endpoint deduplication can be found in the `EndpointSliceCache`
implementation in `kube-proxy`.

## {{% heading "whatsnext" %}}

* Read [Connecting Applications with Services](/docs/concepts/services-networking/connect-applications-service/)
