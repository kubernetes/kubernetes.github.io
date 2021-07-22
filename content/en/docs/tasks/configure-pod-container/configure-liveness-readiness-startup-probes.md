---
title: Configure Liveness, Readiness and Startup Probes
content_type: task
weight: 110
---

<!-- overview -->

This page shows how to configure liveness, readiness and startup probes for containers.

The [kubelet](/docs/reference/command-line-tools-reference/kubelet/) uses liveness probes to know when to
restart a container. For example, liveness probes could catch a deadlock,
where an application is running, but unable to make progress. Restarting a
container in such a state can help to make the application more available
despite bugs.

The kubelet uses readiness probes to know when a container is ready to start
accepting traffic. A Pod is considered ready when all of its containers are ready.
One use of this signal is to control which Pods are used as backends for Services.
When a Pod is not ready, it is removed from Service load balancers.

The kubelet uses startup probes to know when a container application has started.
If such a probe is configured, it disables liveness and readiness checks until
it succeeds, making sure those probes don't interfere with the application startup.
This can be used to adopt liveness checks on slow starting containers, avoiding them
getting killed by the kubelet before they are up and running.



## {{% heading "prerequisites" %}}


{{< include "task-tutorial-prereqs.md" >}}



<!-- steps -->

## Define a liveness command

Many applications running for long periods of time eventually transition to
broken states, and cannot recover except by being restarted. Kubernetes provides
liveness probes to detect and remedy such situations.

In this exercise, you create a Pod that runs a container based on the
`k8s.gcr.io/busybox` image. Here is the configuration file for the Pod:

{{< codenew file="pods/probe/exec-liveness.yaml" >}}

In the configuration file, you can see that the Pod has a single `Container`.
The `periodSeconds` field specifies that the kubelet should perform a liveness
probe every 5 seconds. The `initialDelaySeconds` field tells the kubelet that it
should wait 5 seconds before performing the first probe. To perform a probe, the
kubelet executes the command `cat /tmp/healthy` in the target container. If the
command succeeds, it returns 0, and the kubelet considers the container to be alive and
healthy. If the command returns a non-zero value, the kubelet kills the container
and restarts it.

When the container starts, it executes this command:

```shell
/bin/sh -c "touch /tmp/healthy; sleep 30; rm -rf /tmp/healthy; sleep 600"
```

For the first 30 seconds of the container's life, there is a `/tmp/healthy` file.
So during the first 30 seconds, the command `cat /tmp/healthy` returns a success
code. After 30 seconds, `cat /tmp/healthy` returns a failure code.

Create the Pod:

```shell
kubectl apply -f https://k8s.io/examples/pods/probe/exec-liveness.yaml
```

Within 30 seconds, view the Pod events:

```shell
kubectl describe pod liveness-exec
```

The output indicates that no liveness probes have failed yet:

```
FirstSeen    LastSeen    Count   From            SubobjectPath           Type        Reason      Message
--------- --------    -----   ----            -------------           --------    ------      -------
24s       24s     1   {default-scheduler }                    Normal      Scheduled   Successfully assigned liveness-exec to worker0
23s       23s     1   {kubelet worker0}   spec.containers{liveness}   Normal      Pulling     pulling image "k8s.gcr.io/busybox"
23s       23s     1   {kubelet worker0}   spec.containers{liveness}   Normal      Pulled      Successfully pulled image "k8s.gcr.io/busybox"
23s       23s     1   {kubelet worker0}   spec.containers{liveness}   Normal      Created     Created container with docker id 86849c15382e; Security:[seccomp=unconfined]
23s       23s     1   {kubelet worker0}   spec.containers{liveness}   Normal      Started     Started container with docker id 86849c15382e
```

After 35 seconds, view the Pod events again:

```shell
kubectl describe pod liveness-exec
```

At the bottom of the output, there are messages indicating that the liveness
probes have failed, and the containers have been killed and recreated.

```
FirstSeen LastSeen    Count   From            SubobjectPath           Type        Reason      Message
--------- --------    -----   ----            -------------           --------    ------      -------
37s       37s     1   {default-scheduler }                    Normal      Scheduled   Successfully assigned liveness-exec to worker0
36s       36s     1   {kubelet worker0}   spec.containers{liveness}   Normal      Pulling     pulling image "k8s.gcr.io/busybox"
36s       36s     1   {kubelet worker0}   spec.containers{liveness}   Normal      Pulled      Successfully pulled image "k8s.gcr.io/busybox"
36s       36s     1   {kubelet worker0}   spec.containers{liveness}   Normal      Created     Created container with docker id 86849c15382e; Security:[seccomp=unconfined]
36s       36s     1   {kubelet worker0}   spec.containers{liveness}   Normal      Started     Started container with docker id 86849c15382e
2s        2s      1   {kubelet worker0}   spec.containers{liveness}   Warning     Unhealthy   Liveness probe failed: cat: can't open '/tmp/healthy': No such file or directory
```

Wait another 30 seconds, and verify that the container has been restarted:

```shell
kubectl get pod liveness-exec
```

The output shows that `RESTARTS` has been incremented:

```
NAME            READY     STATUS    RESTARTS   AGE
liveness-exec   1/1       Running   1          1m
```

## Define a liveness HTTP request

Another kind of liveness probe uses an HTTP GET request. Here is the configuration
file for a Pod that runs a container based on the `k8s.gcr.io/liveness`
image.

{{< codenew file="pods/probe/http-liveness.yaml" >}}

In the configuration file, you can see that the Pod has a single container.
The `periodSeconds` field specifies that the kubelet should perform a liveness
probe every 3 seconds. The `initialDelaySeconds` field tells the kubelet that it
should wait 3 seconds before performing the first probe. To perform a probe, the
kubelet sends an HTTP GET request to the server that is running in the container
and listening on port 8080. If the handler for the server's `/healthz` path
returns a success code, the kubelet considers the container to be alive and
healthy. If the handler returns a failure code, the kubelet kills the container
and restarts it.

Any code greater than or equal to 200 and less than 400 indicates success. Any
other code indicates failure.

You can see the source code for the server in
[server.go](https://github.com/kubernetes/kubernetes/blob/{{< param "githubbranch" >}}/test/images/agnhost/liveness/server.go).

For the first 10 seconds that the container is alive, the `/healthz` handler
returns a status of 200. After that, the handler returns a status of 500.

```go
http.HandleFunc("/healthz", func(w http.ResponseWriter, r *http.Request) {
    duration := time.Now().Sub(started)
    if duration.Seconds() > 10 {
        w.WriteHeader(500)
        w.Write([]byte(fmt.Sprintf("error: %v", duration.Seconds())))
    } else {
        w.WriteHeader(200)
        w.Write([]byte("ok"))
    }
})
```

The kubelet starts performing health checks 3 seconds after the container starts.
So the first couple of health checks will succeed. But after 10 seconds, the health
checks will fail, and the kubelet will kill and restart the container.

To try the HTTP liveness check, create a Pod:

```shell
kubectl apply -f https://k8s.io/examples/pods/probe/http-liveness.yaml
```

After 10 seconds, view Pod events to verify that liveness probes have failed and
the container has been restarted:

```shell
kubectl describe pod liveness-http
```

In releases prior to v1.13 (including v1.13), if the environment variable
`http_proxy` (or `HTTP_PROXY`) is set on the node where a Pod is running,
the HTTP liveness probe uses that proxy.
In releases after v1.13, local HTTP proxy environment variable settings do not
affect the HTTP liveness probe.

## Define a TCP liveness probe

A third type of liveness probe uses a TCP socket. With this configuration, the
kubelet will attempt to open a socket to your container on the specified port.
If it can establish a connection, the container is considered healthy, if it
can't it is considered a failure.

{{< codenew file="pods/probe/tcp-liveness-readiness.yaml" >}}

As you can see, configuration for a TCP check is quite similar to an HTTP check.
This example uses both readiness and liveness probes. The kubelet will send the
first readiness probe 5 seconds after the container starts. This will attempt to
connect to the `goproxy` container on port 8080. If the probe succeeds, the Pod
will be marked as ready. The kubelet will continue to run this check every 10
seconds.

In addition to the readiness probe, this configuration includes a liveness probe.
The kubelet will run the first liveness probe 15 seconds after the container
starts. Similar to the readiness probe, this will attempt to connect to the
`goproxy` container on port 8080. If the liveness probe fails, the container
will be restarted.

To try the TCP liveness check, create a Pod:

```shell
kubectl apply -f https://k8s.io/examples/pods/probe/tcp-liveness-readiness.yaml
```

After 15 seconds, view Pod events to verify that liveness probes:

```shell
kubectl describe pod goproxy
```

## Use a named port

You can use a named
[ContainerPort](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#containerport-v1-core)
for HTTP or TCP liveness checks:

```yaml
ports:
- name: liveness-port
  containerPort: 8080
  hostPort: 8080

livenessProbe:
  httpGet:
    path: /healthz
    port: liveness-port
```

## Protect slow starting containers with startup probes {#define-startup-probes}

Sometimes, you have to deal with legacy applications that might require
an additional startup time on their first initialization.
In such cases, it can be tricky to set up liveness probe parameters without
compromising the fast response to deadlocks that motivated such a probe.
The trick is to set up a startup probe with the same command, HTTP or TCP
check, with a `failureThreshold * periodSeconds` long enough to cover the
worse case startup time.

So, the previous example would become:

```yaml
ports:
- name: liveness-port
  containerPort: 8080
  hostPort: 8080

livenessProbe:
  httpGet:
    path: /healthz
    port: liveness-port
  failureThreshold: 1
  periodSeconds: 10

startupProbe:
  httpGet:
    path: /healthz
    port: liveness-port
  failureThreshold: 30
  periodSeconds: 10
```

Thanks to the startup probe, the application will have a maximum of 5 minutes
(30 * 10 = 300s) to finish its startup.
Once the startup probe has succeeded once, the liveness probe takes over to
provide a fast response to container deadlocks.
If the startup probe never succeeds, the container is killed after 300s and
subject to the pod's `restartPolicy`.

## Define readiness probes

Sometimes, applications are temporarily unable to serve traffic.
For example, an application might need to load large data or configuration
files during startup, or depend on external services after startup.
In such cases, you don't want to kill the application,
but you don't want to send it requests either. Kubernetes provides
readiness probes to detect and mitigate these situations. A pod with containers
reporting that they are not ready does not receive traffic through Kubernetes
Services.

{{< note >}}
Readiness probes runs on the container during its whole lifecycle.
{{< /note >}}

{{< caution >}}
Liveness probes *do not* wait for readiness probes to succeed. If you want to wait before executing a liveness probe you should use initialDelaySeconds or a startupProbe.
{{< /caution >}}

Readiness probes are configured similarly to liveness probes. The only difference
is that you use the `readinessProbe` field instead of the `livenessProbe` field.

```yaml
readinessProbe:
  exec:
    command:
    - cat
    - /tmp/healthy
  initialDelaySeconds: 5
  periodSeconds: 5
```

Configuration for HTTP and TCP readiness probes also remains identical to
liveness probes.

Readiness and liveness probes can be used in parallel for the same container.
Using both can ensure that traffic does not reach a container that is not ready
for it, and that containers are restarted when they fail.

## Configure Probes

{{< comment >}}
Eventually, some of this section could be moved to a concept topic.
{{< /comment >}}

[Probes](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#probe-v1-core) have a number of fields that
you can use to more precisely control the behavior of liveness and readiness
checks:

* `initialDelaySeconds`: Number of seconds after the container has started
before liveness or readiness probes are initiated. Defaults to 0 seconds. Minimum value is 0.
* `periodSeconds`: How often (in seconds) to perform the probe. Default to 10
seconds. Minimum value is 1.
* `timeoutSeconds`: Number of seconds after which the probe times out. Defaults
to 1 second. Minimum value is 1.
* `successThreshold`: Minimum consecutive successes for the probe to be
considered successful after having failed. Defaults to 1. Must be 1 for liveness
and startup Probes. Minimum value is 1.
* `failureThreshold`: When a probe fails, Kubernetes will
try `failureThreshold` times before giving up. Giving up in case of liveness probe means restarting the container. In case of readiness probe the Pod will be marked Unready.
Defaults to 3. Minimum value is 1.

{{< note >}}
Before Kubernetes 1.20, the field `timeoutSeconds` was not respected for exec probes:
probes continued running indefinitely, even past their configured deadline,
until a result was returned.

This defect was corrected in Kubernetes v1.20. You may have been relying on the previous behavior,
even without realizing it, as the default timeout is 1 second.
As a cluster administrator, you can disable the [feature gate](/docs/reference/command-line-tools-reference/feature-gates/) `ExecProbeTimeout` (set it to `false`)
on each kubelet to restore the  behavior from older versions, then remove that override
once all the exec probes in the cluster have a `timeoutSeconds` value set.  
If you have pods that are impacted from the default 1 second timeout,
you should update their probe timeout so that you're ready for the
eventual removal of that feature gate.

With the fix of the defect, for exec probes, on Kubernetes `1.20+` with the `dockershim` container runtime,
the process inside the container may keep running even after probe returned failure because of the timeout.
{{< /note >}}
{{< caution >}}
Incorrect implementation of readiness probes may result in an ever growing number
of processes in the container, and resource starvation if this is left unchecked.
{{< /caution >}}

### HTTP probes

[HTTP probes](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#httpgetaction-v1-core)
have additional fields that can be set on `httpGet`:

* `host`: Host name to connect to, defaults to the pod IP. You probably want to
set "Host" in httpHeaders instead.
* `scheme`: Scheme to use for connecting to the host (HTTP or HTTPS). Defaults to HTTP.
* `path`: Path to access on the HTTP server. Defaults to /.
* `httpHeaders`: Custom headers to set in the request. HTTP allows repeated headers.
* `port`: Name or number of the port to access on the container. Number must be
in the range 1 to 65535.

For an HTTP probe, the kubelet sends an HTTP request to the specified path and
port to perform the check. The kubelet sends the probe to the pod's IP address,
unless the address is overridden by the optional `host` field in `httpGet`. If
`scheme` field is set to `HTTPS`, the kubelet sends an HTTPS request skipping the
certificate verification. In most scenarios, you do not want to set the `host` field.
Here's one scenario where you would set it. Suppose the container listens on 127.0.0.1
and the Pod's `hostNetwork` field is true. Then `host`, under `httpGet`, should be set
to 127.0.0.1. If your pod relies on virtual hosts, which is probably the more common
case, you should not use `host`, but rather set the `Host` header in `httpHeaders`.

For an HTTP probe, the kubelet sends two request headers in addition to the mandatory `Host` header:
`User-Agent`, and `Accept`. The default values for these headers are `kube-probe/{{< skew latestVersion >}}`
(where `{{< skew latestVersion >}}` is the version of the kubelet ), and `*/*` respectively.

You can override the default headers by defining `.httpHeaders` for the probe; for example

```yaml
livenessProbe:
  httpGet:
    httpHeaders:
      - name: Accept
        value: application/json

startupProbe:
  httpGet:
    httpHeaders:
      - name: User-Agent
        value: MyUserAgent
```

You can also remove these two headers by defining them with an empty value.

```yaml
livenessProbe:
  httpGet:
    httpHeaders:
      - name: Accept
        value: ""

startupProbe:
  httpGet:
    httpHeaders:
      - name: User-Agent
        value: ""
```

### TCP probes

For a TCP probe, the kubelet makes the probe connection at the node, not in the pod, which
means that you can not use a service name in the `host` parameter since the kubelet is unable
to resolve it.

### Probe-level `terminationGracePeriodSeconds`

{{< feature-state for_k8s_version="v1.22" state="beta" >}}

Prior to release 1.21, the pod-level `terminationGracePeriodSeconds` was used
for terminating a container that failed its liveness or startup probe. This
coupling was unintended and may have resulted in failed containers taking an
unusually long time to restart when a pod-level `terminationGracePeriodSeconds`
was set.

In 1.21 and beyond, when the feature gate `ProbeTerminationGracePeriod` is
enabled, users can specify a probe-level `terminationGracePeriodSeconds` as
part of the probe specification. When the feature gate is enabled, and both a
pod- and probe-level `terminationGracePeriodSeconds` are set, the kubelet will
use the probe-level value.

{{< note >}}
As of Kubernetes 1.22, the `ProbeTerminationGracePeriod` feature gate is only
available on the API Server. The kubelet always honors the probe-level
`terminationGracePeriodSeconds` field if it is present on a Pod.

If you have existing Pods where the `terminationGracePeriodSeconds` field is set and
you no longer wish to use per-probe termination grace periods, you must delete
those existing Pods.

When you (or the control plane, or some other component) create replacement
Pods, and the feature gate `ProbeTerminationGracePeriod` is disabled, then the
API server ignores the Pod-level `terminationGracePeriodSeconds` field, even if
a Pod or pod template specifies it.
{{< /note >}}

For example,

```yaml
spec:
  terminationGracePeriodSeconds: 3600  # pod-level
  containers:
  - name: test
    image: ...

    ports:
    - name: liveness-port
      containerPort: 8080
      hostPort: 8080

    livenessProbe:
      httpGet:
        path: /healthz
        port: liveness-port
      failureThreshold: 1
      periodSeconds: 60
      # Override pod-level terminationGracePeriodSeconds #
      terminationGracePeriodSeconds: 60
```

Probe-level `terminationGracePeriodSeconds` cannot be set for readiness probes.
It will be rejected by the API server.

## {{% heading "whatsnext" %}}


* Learn more about
[Container Probes](/docs/concepts/workloads/pods/pod-lifecycle/#container-probes).

You can also read the API references for:

* [Pod](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#pod-v1-core)
* [Container](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#container-v1-core)
* [Probe](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#probe-v1-core)
