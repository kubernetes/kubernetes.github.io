---
title: Kubernetes API health endpoints
reviewers:
- logicalhan
content_type: concept
weight: 50
---

<!-- overview -->
The Kubernetes {{< glossary_tooltip term_id="kube-apiserver" text="API server" >}} provides API endpoints to indicate the current status of the API server.
This page describes these API endpoints and explains how you can use them.

<!-- body -->

## API endpoints for health

The Kubernetes API server provides 3 API endpoints (`healthz`, `livez` and `readyz`) to indicate the current status of the API server.
The `healthz` endpoint is deprecated (since Kubernetes v1.16), and you should use the more specific `livez` and `readyz` endpoints instead.
The `livez` endpoint can be used with the `--livez-grace-period` [flag](/docs/reference/command-line-tools-reference/kube-apiserver) to specify the startup duration.
For a graceful shutdown you can specify the `--shutdown-delay-duration` [flag](/docs/reference/command-line-tools-reference/kube-apiserver) with the `/readyz` endpoint.
Machines that check the `health`/`livez`/`readyz` of the API server should rely on the HTTP status code.
A status code `200` indicates the API server is `healthy`/`live`/`ready`, depending of the called endpoint.
The more verbose options shown below are intended to be used by human operators to debug their cluster or specially the state of the API server.

The following examples will show how you can interact with the health API endpoints.

For all endpoints you can use the `verbose` parameter to print out the checks and their status.
This can be useful for a human operator to debug the current status of the API server, it is not intended to be consumed by a machine:

```shell
curl -k https://localhost:6443/livez?verbose
```

or from a remote host with authentication:

```shell
kubectl get --raw='/readyz?verbose'
```

The output will look like this:

    [+]ping ok
    [+]log ok
    [+]etcd ok
    [+]poststarthook/start-kube-apiserver-admission-initializer ok
    [+]poststarthook/generic-apiserver-start-informers ok
    [+]poststarthook/start-apiextensions-informers ok
    [+]poststarthook/start-apiextensions-controllers ok
    [+]poststarthook/crd-informer-synced ok
    [+]poststarthook/bootstrap-controller ok
    [+]poststarthook/rbac/bootstrap-roles ok
    [+]poststarthook/scheduling/bootstrap-system-priority-classes ok
    [+]poststarthook/start-cluster-authentication-info-controller ok
    [+]poststarthook/start-kube-aggregator-informers ok
    [+]poststarthook/apiservice-registration-controller ok
    [+]poststarthook/apiservice-status-available-controller ok
    [+]poststarthook/kube-apiserver-autoregistration ok
    [+]autoregister-completion ok
    [+]poststarthook/apiservice-openapi-controller ok
    healthz check passed

The Kubernetes API server also supports to exclude specific checks.
The query parameters can also be combined like in this example:

```shell
curl -k 'https://localhost:6443/readyz?verbose&exclude=etcd'
```

The output show that the `etcd` check is excluded:

    [+]ping ok
    [+]log ok
    [+]etcd excluded: ok
    [+]poststarthook/start-kube-apiserver-admission-initializer ok
    [+]poststarthook/generic-apiserver-start-informers ok
    [+]poststarthook/start-apiextensions-informers ok
    [+]poststarthook/start-apiextensions-controllers ok
    [+]poststarthook/crd-informer-synced ok
    [+]poststarthook/bootstrap-controller ok
    [+]poststarthook/rbac/bootstrap-roles ok
    [+]poststarthook/scheduling/bootstrap-system-priority-classes ok
    [+]poststarthook/start-cluster-authentication-info-controller ok
    [+]poststarthook/start-kube-aggregator-informers ok
    [+]poststarthook/apiservice-registration-controller ok
    [+]poststarthook/apiservice-status-available-controller ok
    [+]poststarthook/kube-apiserver-autoregistration ok
    [+]autoregister-completion ok
    [+]poststarthook/apiservice-openapi-controller ok
    [+]shutdown ok
    healthz check passed

## Individual health checks

{{< feature-state state="alpha" >}}

Each individual health check exposes an HTTP endpoint and could can be checked individually.
The schema for the individual health checks is `/livez/<healthcheck-name>` where `livez` and `readyz` and be used to indicate if you want to check the liveness or the readiness of the API server.
The `<healthcheck-name>` path can be discovered using the `verbose` flag from above and take the path between `[+]` and `ok`.
These individual health checks should not be consumed by machines but can be helpful for a human operator to debug a system:

```shell
curl -k https://localhost:6443/livez/etcd
```
