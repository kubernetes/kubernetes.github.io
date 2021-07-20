---
title: Traces For Kubernetes System Components
reviewers:
- logicalhan
- lilic
content_type: concept
weight: 60
---

<!-- overview -->

System component traces record the latency of and relationships between operations in the cluster.

Kubernetes components emit traces in [OTLP format](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/protocol/otlp.md#opentelemetry-protocol-specification) using the grpc exporter, and can be collected and routed to tracing backends using the [OpenTelemetry Collector](https://github.com/open-telemetry/opentelemetry-collector#-opentelemetry-collector).

<!-- body -->

## Stability

Tracing instrumentation is still under active development, and may change in a variety of ways. This includes span names, attached attributes, instrumented endpoints, etc. There are currently no guarantees of backwards-compatibility for tracing instrumentation.

## Trace Collection

For a complete guide to collecting traces and using the collector, see [Getting Started with the OpenTelemetry Collector](https://opentelemetry.io/docs/collector/getting-started/). However, there are a few things to note that are specific to Kubernetes components.

By default, kubernetes componnets export traces using the grpc exporter for OTLP on the [IANA OpenTelemetry port](https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml?search=opentelemetry), 4317. As an example, if the collector is running as a sidecar to a kuberntes component, the following receiver configuration will collect spans and log them to stdout:

```yaml
receivers:
  otlp:
    protocols:
      grpc:
exporters:
  # Replace this exporter with the exporter for your backend
  logging:
    logLevel: debug
service:
  pipelines:
    traces:
      receivers: [otlp]
      exporters: [logging]
```

## Component traces

### kube-apiserver traces

The kube-apiserver generates spans for incoming http requests, and for outgoing requests to webhooks, etcd, and re-entrant requests.  It propagates the [W3C Trace Context](https://www.w3.org/TR/trace-context/) with outgoing requests, but does not make use of the trace context attached to incoming requests, as the kube-apiserver is often a public endpoint.

#### Enabling tracing in the kube-apiserver

To enable tracing, enable the [`APIServerTracing` feature gate](/docs/reference/command-line-tools-reference/feature-gates/) on the kube-apiserver.  Also, provide the kube-apiserver with a tracing configration file with `--tracing-config-file=<path-to-config>`.  This is an example config that records spans for 1 in 10000 requests, and uses the default OpenTelemetry endpoint:

```yaml
apiVersion: apiserver.config.k8s.io/v1alpha1
kind: TracingConfiguration
samplingRatePerMillion: 100
```

## {{% heading "whatsnext" %}}

* Read about [Getting Started with the OpenTelemetry Collector](https://opentelemetry.io/docs/collector/getting-started/)