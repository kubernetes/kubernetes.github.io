---
reviewers:
- piosz
- x13n
title: Logging Architecture
content_type: concept
weight: 60
---

<!-- overview -->

Application logs can help you understand what is happening inside your application. The logs are particularly useful for debugging problems and monitoring cluster activity. Most modern applications have some kind of logging mechanism. Likewise, container engines are designed to support logging. The easiest and most adopted logging method for containerized applications is writing to standard output and standard error streams.

However, the native functionality provided by a container engine or runtime is usually not enough for a complete logging solution.
For example, you may want access your application's logs if a container crashes; a pod gets evicted; or a node dies.
In a cluster, logs should have a separate storage and lifecycle independent of nodes, pods, or containers. This concept is called _cluster-level logging_.

<!-- body -->

Cluster-level logging architectures require a separate backend to store, analyze, and query logs. Kubernetes
does not provide a native storage solution for log data. Instead, there are many logging solutions that
integrate with Kubernetes. The following sections describe how to handle and store logs on nodes.

## Basic logging in Kubernetes

This example uses a `Pod` specification with a container
to write text to the standard output stream once per second.

{{< codenew file="debug/counter-pod.yaml" >}}

To run this pod, use the following command:

```shell
kubectl apply -f https://k8s.io/examples/debug/counter-pod.yaml
```

The output is:

```console
pod/counter created
```

To fetch the logs, use the `kubectl logs` command, as follows:

```shell
kubectl logs counter
```

The output is:

```console
0: Mon Jan  1 00:00:00 UTC 2001
1: Mon Jan  1 00:00:01 UTC 2001
2: Mon Jan  1 00:00:02 UTC 2001
...
```

You can use `kubectl logs --previous` to retrieve logs from a previous instantiation of a container. If your pod has multiple containers, specify which container's logs you want to access by appending a container name to the command. See the [`kubectl logs` documentation](/docs/reference/generated/kubectl/kubectl-commands#logs) for more details.

## Logging at the node level

![Node level logging](/images/docs/user-guide/logging/logging-node-level.png)

A container engine handles and redirects any output generated to a containerized application's `stdout` and `stderr` streams.
For example, the Docker container engine redirects those two streams to [a logging driver](https://docs.docker.com/engine/admin/logging/overview), which is configured in Kubernetes to write to a file in JSON format.

{{< note >}}
The Docker JSON logging driver treats each line as a separate message. When using the Docker logging driver, there is no direct support for multi-line messages. You need to handle multi-line messages at the logging agent level or higher.
{{< /note >}}

By default, if a container restarts, the kubelet keeps one terminated container with its logs. If a pod is evicted from the node, all corresponding containers are also evicted, along with their logs.

An important consideration in node-level logging is implementing log rotation,
so that logs don't consume all available storage on the node. Kubernetes
is not responsible for rotating logs, but rather a deployment tool
should set up a solution to address that.
For example, in Kubernetes clusters, deployed by the `kube-up.sh` script,
there is a [`logrotate`](https://linux.die.net/man/8/logrotate)
tool configured to run each hour. You can also set up a container runtime to
rotate an application's logs automatically.

As an example, you can find detailed information about how `kube-up.sh` sets
up logging for COS image on GCP in the corresponding
[`configure-helper` script](https://github.com/kubernetes/kubernetes/blob/{{< param "githubbranch" >}}/cluster/gce/gci/configure-helper.sh).

When using a **CRI container runtime**, the kubelet is responsible for rotating the logs and managing the logging directory structure.
The kubelet sends this information to the CRI container runtime and the runtime writes the container logs to the given location.
The two kubelet parameters [`containerLogMaxSize` and `containerLogMaxFiles`](/docs/reference/config-api/kubelet-config.v1beta1/#kubelet-config-k8s-io-v1beta1-KubeletConfiguration)
in [kubelet config file](/docs/tasks/administer-cluster/kubelet-config-file/)
can be used to configure the maximum size for each log file and the maximum number of files allowed for each container respectively.

When you run [`kubectl logs`](/docs/reference/generated/kubectl/kubectl-commands#logs) as in
the basic logging example, the kubelet on the node handles the request and
reads directly from the log file. The kubelet returns the content of the log file.

{{< note >}}
If an external system has performed the rotation or a CRI container runtime is used,
only the contents of the latest log file will be available through
`kubectl logs`. For example, if there's a 10MB file, `logrotate` performs
the rotation and there are two files: one file that is 10MB in size and a second file that is empty.
`kubectl logs` returns the latest log file which in this example is an empty response.
{{< /note >}}

### System component logs

There are two types of system components: those that run in a container and those
that do not run in a container. For example:

* The Kubernetes scheduler and kube-proxy run in a container.
* The kubelet and container runtime do not run in containers.

On machines with systemd, the kubelet and container runtime write to journald. If
systemd is not present, the kubelet and container runtime write to `.log` files
in the `/var/log` directory. System components inside containers always write
to the `/var/log` directory, bypassing the default logging mechanism.
They use the [`klog`](https://github.com/kubernetes/klog)
logging library. You can find the conventions for logging severity for those
components in the [development docs on logging](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-instrumentation/logging.md).

Similar to the container logs, system component logs in the `/var/log`
directory should be rotated. In Kubernetes clusters brought up by
the `kube-up.sh` script, those logs are configured to be rotated by
the `logrotate` tool daily or once the size exceeds 100MB.

## Cluster-level logging architectures

While Kubernetes does not provide a native solution for cluster-level logging, there are several common approaches you can consider. Here are some options:

* Use a node-level logging agent that runs on every node.
* Include a dedicated sidecar container for logging in an application pod.
* Push logs directly to a backend from within an application.

### Using a node logging agent

![Using a node level logging agent](/images/docs/user-guide/logging/logging-with-node-agent.png)

You can implement cluster-level logging by including a _node-level logging agent_ on each node. The logging agent is a dedicated tool that exposes logs or pushes logs to a backend. Commonly, the logging agent is a container that has access to a directory with log files from all of the application containers on that node.

Because the logging agent must run on every node, it is recommended to run the agent
as a `DaemonSet`.

Node-level logging creates only one agent per node and doesn't require any changes to the applications running on the node.

Containers write stdout and stderr, but with no agreed format. A node-level agent collects these logs and forwards them for aggregation.

### Using a sidecar container with the logging agent {#sidecar-container-with-logging-agent}

You can use a sidecar container in one of the following ways:

* The sidecar container streams application logs to its own `stdout`.
* The sidecar container runs a logging agent, which is configured to pick up logs from an application container.

#### Streaming sidecar container

![Sidecar container with a streaming container](/images/docs/user-guide/logging/logging-with-streaming-sidecar.png)

By having your sidecar containers write to their own `stdout` and `stderr`
streams, you can take advantage of the kubelet and the logging agent that
already run on each node. The sidecar containers read logs from a file, a socket,
or journald. Each sidecar container prints a log to its own `stdout` or `stderr` stream.

This approach allows you to separate several log streams from different
parts of your application, some of which can lack support
for writing to `stdout` or `stderr`. The logic behind redirecting logs
is minimal, so it's not a significant overhead. Additionally, because
`stdout` and `stderr` are handled by the kubelet, you can use built-in tools
like `kubectl logs`.

For example, a pod runs a single container, and the container
writes to two different log files using two different formats. Here's a
configuration file for the Pod:

{{< codenew file="admin/logging/two-files-counter-pod.yaml" >}}

It is not recommended to write log entries with different formats to the same log
stream, even if you managed to redirect both components to the `stdout` stream of
the container. Instead, you can create two sidecar containers. Each sidecar
container could tail a particular log file from a shared volume and then redirect
the logs to its own `stdout` stream.

Here's a configuration file for a pod that has two sidecar containers:

{{< codenew file="admin/logging/two-files-counter-pod-streaming-sidecar.yaml" >}}

Now when you run this pod, you can access each log stream separately by
running the following commands:

```shell
kubectl logs counter count-log-1
```

The output is:

```console
0: Mon Jan  1 00:00:00 UTC 2001
1: Mon Jan  1 00:00:01 UTC 2001
2: Mon Jan  1 00:00:02 UTC 2001
...
```

```shell
kubectl logs counter count-log-2
```

The output is:

```console
Mon Jan  1 00:00:00 UTC 2001 INFO 0
Mon Jan  1 00:00:01 UTC 2001 INFO 1
Mon Jan  1 00:00:02 UTC 2001 INFO 2
...
```

The node-level agent installed in your cluster picks up those log streams
automatically without any further configuration. If you like, you can configure
the agent to parse log lines depending on the source container.

Note, that despite low CPU and memory usage (order of a couple of millicores
for cpu and order of several megabytes for memory), writing logs to a file and
then streaming them to `stdout` can double disk usage. If you have
an application that writes to a single file, it's recommended to set
`/dev/stdout` as the destination rather than implement the streaming sidecar
container approach.

Sidecar containers can also be used to rotate log files that cannot be
rotated by the application itself. An example of this approach is a small container running `logrotate` periodically.
However, it's recommended to use `stdout` and `stderr` directly and leave rotation
and retention policies to the kubelet.

#### Sidecar container with a logging agent

![Sidecar container with a logging agent](/images/docs/user-guide/logging/logging-with-sidecar-agent.png)

If the node-level logging agent is not flexible enough for your situation, you
can create a sidecar container with a separate logging agent that you have
configured specifically to run with your application.

{{< note >}}
Using a logging agent in a sidecar container can lead
to significant resource consumption. Moreover, you won't be able to access
those logs using `kubectl logs` because they are not controlled
by the kubelet.
{{< /note >}}

Here are two configuration files that you can use to implement a sidecar container with a logging agent. The first file contains
a [`ConfigMap`](/docs/tasks/configure-pod-container/configure-pod-configmap/) to configure fluentd.

{{< codenew file="admin/logging/fluentd-sidecar-config.yaml" >}}

{{< note >}}
For information about configuring fluentd, see the [fluentd documentation](https://docs.fluentd.org/).
{{< /note >}}

The second file describes a pod that has a sidecar container running fluentd.
The pod mounts a volume where fluentd can pick up its configuration data.

{{< codenew file="admin/logging/two-files-counter-pod-agent-sidecar.yaml" >}}

In the sample configurations, you can replace fluentd with any logging agent, reading from any source inside an application container.

### Exposing logs directly from the application

![Exposing logs directly from the application](/images/docs/user-guide/logging/logging-from-application.png)

Cluster-logging that exposes or pushes logs directly from every application is outside the scope of Kubernetes.
