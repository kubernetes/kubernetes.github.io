---
layout: blog
title: "Implementing Traffic Policies in Kubernetes"
date: 2021-06-29
slug: implementing-traffic-policies-in-kubernetes
---

**Author:** Cody De Arkland (Kong)


In the earliest days of configuring your Kubernetes environment, one of the networking challenges you might face is how to safely grant access to services within your. By default, pods within a cluster can communicate with all other pods and services. Security focused individuals are likely to want to understand better ways to secure service to service communication following something like a zero-trust policy. 

In this post, we'll introduce you to the concept of security traffic between services using [Kuma](https://kuma.io/), a modern distributed control plane with a bundled Envoy Proxy integration. Using Kuma we will apply a set of policies known as `TrafficPermissions` that allow us to restrict communication between services.

## Setting Up a Kuma Service Mesh
Application stacks that run as individual containers need to communicate with one another and outside clients. To drive self-service and automation, along with security, routing and load-balancing — the concept of a service mesh emerged. The goal of a service mesh is to provide seamless management of application connectivity between resources in an environment. Thus, while an ingress controller handles the behavior of incoming traffic, a service mesh is responsible for enabling a higher functionality of communication across applications and services within a service mesh. 

Kuma is one example of a service mesh. It's an open source project that works across various environments, including Kubernetes and virtual machines. It allows users to extend the service mesh to supports multi-zone deployments - where users might want to connect resources between cloud environments or on-premises data centers. Kuma is supported by the same team that built [Kong](https://github.com/Kong/kong), a popular API gateway that simplifies communication with API's. Kong has a vast plugin ecosystem that enables you to easily deploy and manage HTTP requests, responses and routes across your entire fleet. Kuma works hand-in-hand with Kong, but the two projects don't rely on each other, as we'll see below.

In addition to providing fine-grained traffic control capabilities, Kuma also offers rapid metrics and observability analyses. Being able to secure your networking access is only part of the solution. Since Kuma integrates with [Prometheus](https://prometheus.io/) for native data collection and [Grafana](https://grafana.com/) for charting and viewing that data, you'll be able to see precisely how your applications are communicating across the service mesh landscape.

Installing Kuma is a snap. First, you can download and run the installer like so:

```
curl -L https://kuma.io/installer.sh | sh -
```

Then, switch to the installation directory:

```
cd kuma-1.2.0/bin
```

From here, you can run Kuma in multi-zone mode or standalone mode if Kuma is just in a single Kubernetes cluster. The command below will deploy Kuma in a single zone configuration, the default:

```
./kumactl install control-plane | kubectl apply -f -
```

For other environments, check out [the docs on deployment](https://kuma.io/docs/1.2.0/documentation/deployments/).

There are several ways to interact with Kuma.
* Read-only through its [GUI](https://kuma.io/docs/1.2.0/documentation/gui/#getting-started)
* For write/edit access - [kubectl](https://kuma.io/docs/1.2.0/policies/introduction/)
* [API](https://kuma.io/docs/1.2.0/documentation/http-api/#pagination) (note that in a Kubernetes deployment, the API is also read-only, and interactions via kubectl are the correct process.)

To access the GUI, you'll first need to forward the API service port:

```
$ kubectl port-forward svc/kuma-control-plane -n kuma-system 5681:5681
```

After that, you can navigate to http://127.0.0.1:5681/gui.

## CNI Compatibility
Before continuing, it's important to introduce a minor point about configuration, which has major implications.

Kubernetes uses [the Container Network Interface (CNI) standard](https://github.com/containernetworking/cni) to configure networking for containers. This means that no matter how you design a CNI-compatible tool, it ought to be able to rely on the same set of protocols. Kubernetes provides an API that an ingress controller can use to set and manage the network policies. Multiple CNI-based projects have sprung up in response to enterprise-grade security and ease of use requirements. For example, one such project is [Calico](https://www.projectcalico.org/).

Theres absolutely valid questions in the realm of when you should rely on native abilities of a CNI vs leveraging a service mesh such as Kuma. For example, although Calico adheres to the [Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/) Kubernetes provides, [its format for setting up traffic rules](https://docs.projectcalico.org/security/service-accounts) is more opaque than Kuma. Kuma provides a way of configuring [network policies](https://kuma.io/policies/) that run parallel to the first-class API Kubernetes provides. It should come as no surprise that Kuma is also compatible with CNI. This means you can easily swap out any network policies defined by Calico—or any project that uses a CNI-based protocol for Kuma’s traffic rules - or mix and match as needed. The main differentiator between such projects comes down to features. Kuma, for example, can act as a service mesh, an observability platform and a network policy manager all in one. Other projects may have different priorities, and it is the developer’s responsibility to make sure they can all interact with one another properly.

## Architecting Traffic Rules with Kuma
With Kuma set up and running on Kubernetes, let's see how to establish traffic rules to manage access between services.

Imagine the following scenario: an eCommerce platform that relies on two micro-services that communicate to meet the business’s needs—let's call them services backend1 and backend2. A third micro-service acts as a public API, and any incoming request to this service privately queries the other two. We'd like to expose the API to the public but keep the other two micro-services isolated from external networks.

The pure ingress way to do this is to set up a [Network Policy](https://kubernetes.io/docs/concepts/services-networking/network-policies/). However, Kuma drastically simplifies this process with an easy-to-understand YAML DSL. You can define [Traffic Permission policies](https://kuma.io/docs/1.2.0/policies/traffic-permissions/) that explicitly identify which sources the services can communicate specific destination services.

```
cat <<EOF | kumactl apply -f -
type: TrafficPermission
name: api-to-backends
mesh: default
sources:
  - match:
      service: 'publicAPI'
destinations:
  - match:
      service: 'backend1'
  - match:
      service: 'backend2'
EOF
```

In this manifest, the Traffic Permission policy gives the frontend permission to send traffic to the backend. The policy will reject any other source.

Traffic Permission is just one of the policies that Kuma provides. Among other features, you can also set up a [Health Check policy](https://kuma.io/docs/1.2.0/policies/health-check/#usage) to keep track of the health of every data plane proxy. This, too, makes use of familiar source and destination matches:

```
cat <<EOF | kumactl apply -f -
apiVersion: kuma.io/v1alpha1
kind: HealthCheck
mesh: default
metadata:
  name: web-to-backend-check
spec:
  sources:
  - match:
      service: 'publicAPI'
  destinations:
  - match:
      service: 'backend1'
  - match:
      service: 'backend2'
  conf:
    interval: 10s
    timeout: 2s
    unhealthyThreshold: 3
    healthyThreshold: 1
    tcp:
      send: Zm9v
      receive:
      - YmFy
      - YmF6
EOF
```

## Once Control Plane for Security, Observability and Routing

The goal of any service mesh is to provide a single location to configure how your ap plications communicate across your environments. A service mesh can simplify much of the communication across these services. In this brief blog we touched on traffic permissions to restrict communication between services but ultimately this is only the first step in securing an environment. Implementing a [zero-trust security policy](https://kuma.io/docs/1.2.0/policies/) with Kuma is going to extend across other policies as  well such as mTLS for encrypting traffic between resources.

If you'd like to learn more about proper access configuration, you can check out [the Kubernetes documentation on controlling access](https://kubernetes.io/docs/concepts/security/controlling-access/) or [their best practices on pod security](https://kubernetes.io/docs/concepts/security/pod-security-standards/). [Kuma's secure access patterns](https://kuma.io/docs/1.2.0/security/certificates/) also provide some guidelines on how to define commonly-required networking policies.
