---
reviewers:
- thockin
- caseydavenport
- danwinship
title: Network Policies
content_type: concept
weight: 50
---

<!-- overview -->

If you want to control traffic flow at the IP address or port level (OSI layer 3 or 4), then you might consider using Kubernetes NetworkPolicies for particular applications in your cluster.  NetworkPolicies are an application-centric construct which allow you to specify how a {{< glossary_tooltip text="pod" term_id="pod">}} is allowed to communicate with various network "entities" (we use the word "entity" here to avoid overloading the more common terms such as "endpoints" and "services", which have specific Kubernetes connotations) over the network.

The entities that a Pod can communicate with are identified through a combination of the following 3 identifiers:

1. Other pods that are allowed (exception: a pod cannot block access to itself)
2. Namespaces that are allowed
3. IP blocks (exception: traffic to and from the node where a Pod is running is always allowed, regardless of the IP address of the Pod or the node)

When defining a pod- or namespace- based NetworkPolicy, you use a {{< glossary_tooltip text="selector" term_id="selector">}} to specify what traffic is allowed to and from the Pod(s) that match the selector.

Meanwhile, when IP based NetworkPolicies are created, we define policies based on IP blocks (CIDR ranges).

<!-- body -->
## Prerequisites

Network policies are implemented by the [network plugin](/docs/concepts/extend-kubernetes/compute-storage-net/network-plugins/). To use network policies, you must be using a networking solution which supports NetworkPolicy. Creating a NetworkPolicy resource without a controller that implements it will have no effect.

## Isolated and Non-isolated Pods

By default, pods are non-isolated; they accept traffic from any source.

Pods become isolated by having a NetworkPolicy that selects them. Once there is any NetworkPolicy in a namespace selecting a particular pod, that pod will reject any connections that are not allowed by any NetworkPolicy. (Other pods in the namespace that are not selected by any NetworkPolicy will continue to accept all traffic.)

Network policies do not conflict; they are additive. If any policy or policies select a pod, the pod is restricted to what is allowed by the union of those policies' ingress/egress rules. Thus, order of evaluation does not affect the policy result.

For a network flow between two pods to be allowed, both the egress policy on the source pod and the ingress policy on the destination pod need to allow the traffic. If either the egress policy on the source, or the ingress policy on the destination denies the traffic, the traffic will be denied.

## The NetworkPolicy resource {#networkpolicy-resource}

See the {{< api-reference page="policy-resources/network-policy-v1" >}}
reference for a full definition of the resource.

An example NetworkPolicy might look like this:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: test-network-policy
  namespace: default
spec:
  podSelector:
    matchLabels:
      role: db
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - ipBlock:
        cidr: 172.17.0.0/16
        except:
        - 172.17.1.0/24
    - namespaceSelector:
        matchLabels:
          project: myproject
    - podSelector:
        matchLabels:
          role: frontend
    ports:
    - protocol: TCP
      port: 6379
  egress:
  - to:
    - ipBlock:
        cidr: 10.0.0.0/24
    ports:
    - protocol: TCP
      port: 5978
```

{{< note >}}
POSTing this to the API server for your cluster will have no effect unless your chosen networking solution supports network policy.
{{< /note >}}

__Mandatory Fields__: As with all other Kubernetes config, a NetworkPolicy
needs `apiVersion`, `kind`, and `metadata` fields.  For general information
about working with config files, see
[Configure Containers Using a ConfigMap](/docs/tasks/configure-pod-container/configure-pod-configmap/),
and [Object Management](/docs/concepts/overview/working-with-objects/object-management).

__spec__: NetworkPolicy [spec](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md#spec-and-status) has all the information needed to define a particular network policy in the given namespace.

__podSelector__: Each NetworkPolicy includes a `podSelector` which selects the grouping of pods to which the policy applies. The example policy selects pods with the label "role=db". An empty `podSelector` selects all pods in the namespace.

__policyTypes__: Each NetworkPolicy includes a `policyTypes` list which may include either `Ingress`, `Egress`, or both. The `policyTypes` field indicates whether or not the given policy applies to ingress traffic to selected pod, egress traffic from selected pods, or both. If no `policyTypes` are specified on a NetworkPolicy then by default `Ingress` will always be set and `Egress` will be set if the NetworkPolicy has any egress rules.

__ingress__: Each NetworkPolicy may include a list of allowed `ingress` rules.  Each rule allows traffic which matches both the `from` and `ports` sections. The example policy contains a single rule, which matches traffic on a single port, from one of three sources, the first specified via an `ipBlock`, the second via a `namespaceSelector` and the third via a `podSelector`.

__egress__: Each NetworkPolicy may include a list of allowed `egress` rules.  Each rule allows traffic which matches both the `to` and `ports` sections. The example policy contains a single rule, which matches traffic on a single port to any destination in `10.0.0.0/24`.

So, the example NetworkPolicy:

1. isolates "role=db" pods in the "default" namespace for both ingress and egress traffic (if they weren't already isolated)
2. (Ingress rules) allows connections to all pods in the "default" namespace with the label "role=db" on TCP port 6379 from:

   * any pod in the "default" namespace with the label "role=frontend"
   * any pod in a namespace with the label "project=myproject"
   * IP addresses in the ranges 172.17.0.0–172.17.0.255 and 172.17.2.0–172.17.255.255 (ie, all of 172.17.0.0/16 except 172.17.1.0/24)
3. (Egress rules) allows connections from any pod in the "default" namespace with the label "role=db" to CIDR 10.0.0.0/24 on TCP port 5978

See the [Declare Network Policy](/docs/tasks/administer-cluster/declare-network-policy/) walkthrough for further examples.

## Behavior of `to` and `from` selectors

There are four kinds of selectors that can be specified in an `ingress` `from` section or `egress` `to` section:

__podSelector__: This selects particular Pods in the same namespace as the NetworkPolicy which should be allowed as ingress sources or egress destinations.

__namespaceSelector__: This selects particular namespaces for which all Pods should be allowed as ingress sources or egress destinations.

__namespaceSelector__ *and* __podSelector__: A single `to`/`from` entry that specifies both `namespaceSelector` and `podSelector` selects particular Pods within particular namespaces. Be careful to use correct YAML syntax; this policy:

```yaml
  ...
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          user: alice
      podSelector:
        matchLabels:
          role: client
  ...
```

contains a single `from` element allowing connections from Pods with the label `role=client` in namespaces with the label `user=alice`. But *this* policy:

```yaml
  ...
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          user: alice
    - podSelector:
        matchLabels:
          role: client
  ...
```

contains two elements in the `from` array, and allows connections from Pods in the local Namespace with the label `role=client`, *or* from any Pod in any namespace with the label `user=alice`.

When in doubt, use `kubectl describe` to see how Kubernetes has interpreted the policy.

__ipBlock__: This selects particular IP CIDR ranges to allow as ingress sources or egress destinations. These should be cluster-external IPs, since Pod IPs are ephemeral and unpredictable.

Cluster ingress and egress mechanisms often require rewriting the source or destination IP
of packets. In cases where this happens, it is not defined whether this happens before or
after NetworkPolicy processing, and the behavior may be different for different
combinations of network plugin, cloud provider, `Service` implementation, etc.

In the case of ingress, this means that in some cases you may be able to filter incoming
packets based on the actual original source IP, while in other cases, the "source IP" that
the NetworkPolicy acts on may be the IP of a `LoadBalancer` or of the Pod's node, etc.

For egress, this means that connections from pods to `Service` IPs that get rewritten to
cluster-external IPs may or may not be subject to `ipBlock`-based policies.

## Default policies

By default, if no policies exist in a namespace, then all ingress and egress traffic is allowed to and from pods in that namespace. The following examples let you change the default behavior
in that namespace.

### Default deny all ingress traffic

You can create a "default" isolation policy for a namespace by creating a NetworkPolicy that selects all pods but does not allow any ingress traffic to those pods.

{{< codenew file="service/networking/network-policy-default-deny-ingress.yaml" >}}

This ensures that even pods that aren't selected by any other NetworkPolicy will still be isolated. This policy does not change the default egress isolation behavior.

### Default allow all ingress traffic

If you want to allow all traffic to all pods in a namespace (even if policies are added that cause some pods to be treated as "isolated"), you can create a policy that explicitly allows all traffic in that namespace.

{{< codenew file="service/networking/network-policy-allow-all-ingress.yaml" >}}

### Default deny all egress traffic

You can create a "default" egress isolation policy for a namespace by creating a NetworkPolicy that selects all pods but does not allow any egress traffic from those pods.

{{< codenew file="service/networking/network-policy-default-deny-egress.yaml" >}}

This ensures that even pods that aren't selected by any other NetworkPolicy will not be allowed egress traffic. This policy does not
change the default ingress isolation behavior.

### Default allow all egress traffic

If you want to allow all traffic from all pods in a namespace (even if policies are added that cause some pods to be treated as "isolated"), you can create a policy that explicitly allows all egress traffic in that namespace.

{{< codenew file="service/networking/network-policy-allow-all-egress.yaml" >}}

### Default deny all ingress and all egress traffic

You can create a "default" policy for a namespace which prevents all ingress AND egress traffic by creating the following NetworkPolicy in that namespace.

{{< codenew file="service/networking/network-policy-default-deny-all.yaml" >}}

This ensures that even pods that aren't selected by any other NetworkPolicy will not be allowed ingress or egress traffic.

## SCTP support

{{< feature-state for_k8s_version="v1.20" state="stable" >}}

As a stable feature, this is enabled by default. To disable SCTP at a cluster level, you (or your cluster administrator) will need to disable the `SCTPSupport` [feature gate](/docs/reference/command-line-tools-reference/feature-gates/) for the API server with `--feature-gates=SCTPSupport=false,…`.
When the feature gate is enabled, you can set the `protocol` field of a NetworkPolicy to `SCTP`.

{{< note >}}
You must be using a {{< glossary_tooltip text="CNI" term_id="cni" >}} plugin that supports SCTP protocol NetworkPolicies.
{{< /note >}}

## Targeting a range of Ports

{{< feature-state for_k8s_version="v1.21" state="alpha" >}}

When writing a NetworkPolicy, you can target a range of ports instead of a single port.

This is achievable with the usage of the `endPort` field, as the following example:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: multi-port-egress
  namespace: default
spec:
  podSelector:
    matchLabels:
      role: db
  policyTypes:
  - Egress
  egress:
  - to:
    - ipBlock:
        cidr: 10.0.0.0/24
    ports:
    - protocol: TCP
      port: 32000
      endPort: 32768
```

The above rule allows any Pod with label `db` on the namespace `default` to communicate with any IP within the range `10.0.0.0/24` over TCP, provided that the target port is between the range 32000 and 32768.

The following restrictions apply when using this field:
* As an alpha feature, this is disabled by default. To enable the `endPort` field at a cluster level, you (or your cluster administrator) need to enable the `NetworkPolicyEndPort` [feature gate](/docs/reference/command-line-tools-reference/feature-gates/) for the API server with `--feature-gates=NetworkPolicyEndPort=true,…`.
* The `endPort` field must be equal than or greater to the `port` field.
* `endPort` can only be defined if `port` is also defined.
* Both ports must be numeric.

{{< note >}}
Your cluster must be using a {{< glossary_tooltip text="CNI" term_id="cni" >}} plugin that
supports the `endPort` field in NetworkPolicy specifications.
{{< /note >}}

## Targeting a Namespace by its name

{{< feature-state state="beta" for_k8s_version="1.21" >}}

The Kubernetes control plane sets an immutable label `kubernetes.io/metadata.name` on all
namespaces, provided that the `NamespaceDefaultLabelName`
[feature gate](/docs/reference/command-line-tools-reference/feature-gates/) is enabled.
The value of the label is the namespace name.

While NetworkPolicy cannot target a namespace by its name with some object field, you can use the
standardized label to target a specific namespace.

## What you can't do with network policies (at least, not yet)

As of Kubernetes {{< skew latestVersion >}}, the following functionality does not exist in the NetworkPolicy API, but you might be able to implement workarounds using Operating System components (such as SELinux, OpenVSwitch, IPTables, and so on) or Layer 7 technologies (Ingress controllers, Service Mesh implementations) or admission controllers.  In case you are new to network security in Kubernetes, its worth noting that the following User Stories cannot (yet) be implemented using the NetworkPolicy API.

- Forcing internal cluster traffic to go through a common gateway (this might be best served with a service mesh or other proxy).
- Anything TLS related (use a service mesh or ingress controller for this).
- Node specific policies (you can use CIDR notation for these, but you cannot target nodes by their Kubernetes identities specifically).
- Targeting of services by name (you can, however, target pods or namespaces by their {{< glossary_tooltip text="labels" term_id="label" >}}, which is often a viable workaround).
- Creation or management of "Policy requests" that are fulfilled by a third party.
- Default policies which are applied to all namespaces or pods (there are some third party Kubernetes distributions and projects which can do this).
- Advanced policy querying and reachability tooling.
- The ability to log network security events (for example connections that are blocked or accepted).
- The ability to explicitly deny policies (currently the model for NetworkPolicies are deny by default, with only the ability to add allow rules).
- The ability to prevent loopback or incoming host traffic (Pods cannot currently block localhost access, nor do they have the ability to block access from their resident node).

## {{% heading "whatsnext" %}}


- See the [Declare Network Policy](/docs/tasks/administer-cluster/declare-network-policy/)
  walkthrough for further examples.
- See more [recipes](https://github.com/ahmetb/kubernetes-network-policy-recipes) for common scenarios enabled by the NetworkPolicy resource.
- NetworkPolicy is a top-level resource in the Kubernetes REST API.
  The {{< api-reference page="policy-resources/network-policy-v1" >}} object definition describes the object in detail.
