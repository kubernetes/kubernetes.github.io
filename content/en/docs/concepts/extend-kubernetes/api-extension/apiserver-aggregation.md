---
title: Extending the Kubernetes API with the aggregation layer
reviewers:
- lavalamp
- cheftako
- chenopis
content_type: concept
weight: 20
---

<!-- overview -->

The aggregation layer allows Kubernetes to be extended with additional APIs, beyond what is offered by the core Kubernetes APIs.
The additional APIs can either be ready-made solutions such as [service-catalog](/docs/concepts/extend-kubernetes/service-catalog/), or APIs that you develop yourself.

The aggregation layer is different from [Custom Resources](/docs/concepts/extend-kubernetes/api-extension/custom-resources/), which are a way to make the {{< glossary_tooltip term_id="kube-apiserver" text="kube-apiserver" >}} recognise new kinds of object.

<!-- body -->

## Aggregation layer

The aggregation layer runs in-process with the kube-apiserver. Until an extension resource is registered, the aggregation layer will do nothing. To register an API, you add an _APIService_ object, which "claims" the URL path in the Kubernetes API. At that point, the aggregation layer will proxy anything sent to that API path (e.g. `/apis/myextension.mycompany.io/v1/…`) to the registered APIService.

The most common way to implement the APIService is to run an *extension API server* in Pod(s) that run in your cluster. If you're using the extension API server to manage resources in your cluster, the extension API server (also written as "extension-apiserver") is typically paired with one or more {{< glossary_tooltip text="controllers" term_id="controller" >}}. The apiserver-builder library provides a skeleton for both extension API servers and the associated controller(s).

### Response latency

Extension API servers should have low latency networking to and from the kube-apiserver.
Discovery requests are required to round-trip from the kube-apiserver in five seconds or less.

If your extension API server cannot achieve that latency requirement, consider making changes that let you meet it.

## {{% heading "whatsnext" %}}

* To get the aggregator working in your environment, [configure the aggregation layer](/docs/tasks/extend-kubernetes/configure-aggregation-layer/).
* Then, [setup an extension api-server](/docs/tasks/extend-kubernetes/setup-extension-api-server/) to work with the aggregation layer.
* Also, learn how to [extend the Kubernetes API using Custom Resource Definitions](/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/).
* Read the specification for {{< api-reference page="cluster-resources/api-service-v1" >}}


