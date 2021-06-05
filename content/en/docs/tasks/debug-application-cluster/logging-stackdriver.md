---
reviewers:
- piosz
- x13n
title: Logging Using Stackdriver
content_type: concept
---

<!-- overview -->

Before reading this page, it's highly recommended to familiarize yourself
with the [overview of logging in Kubernetes](/docs/concepts/cluster-administration/logging).

{{< note >}}
By default, Stackdriver logging collects only your container's standard output and
standard error streams. To collect any logs your application writes to a file (for example),
see the [sidecar approach](/docs/concepts/cluster-administration/logging#sidecar-container-with-a-logging-agent)
in the Kubernetes logging overview.
{{< /note >}}




<!-- body -->

## Deploying

To ingest logs, you must deploy the Stackdriver Logging agent to each node in your cluster.
The agent is a configured `fluentd` instance, where the configuration is stored in a `ConfigMap`
and the instances are managed using a Kubernetes `DaemonSet`. The actual deployment of the
`ConfigMap` and `DaemonSet` for your cluster depends on your individual cluster setup.

### Deploying to a new cluster

#### Google Kubernetes Engine

Stackdriver is the default logging solution for clusters deployed on Google Kubernetes Engine.
Stackdriver Logging is deployed to a new cluster by default unless you explicitly opt-out.

#### Other platforms

To deploy Stackdriver Logging on a *new* cluster that you're
creating using `kube-up.sh`, do the following:

1. Set the `KUBE_LOGGING_DESTINATION` environment variable to `gcp`.
1. **If not running on GCE**, include the `beta.kubernetes.io/fluentd-ds-ready=true`
in the `KUBE_NODE_LABELS` variable.

Once your cluster has started, each node should be running the Stackdriver Logging agent.
The `DaemonSet` and `ConfigMap` are configured as addons. If you're not using `kube-up.sh`,
consider starting a cluster without a pre-configured logging solution and then deploying
Stackdriver Logging agents to the running cluster.

{{< warning >}}
The Stackdriver logging daemon has known issues on platforms other
than Google Kubernetes Engine. Proceed at your own risk.
{{< /warning >}}

### Deploying to an existing cluster

1. Apply a label on each node, if not already present.

    The Stackdriver Logging agent deployment uses node labels to determine to which nodes
    it should be allocated. These labels were introduced to distinguish nodes with the
    Kubernetes version 1.6 or higher. If the cluster was created with Stackdriver Logging
    configured and node has version 1.5.X or lower, it will have fluentd as static pod. Node
    cannot have more than one instance of fluentd, therefore only apply labels to the nodes
    that don't have fluentd pod allocated already. You can ensure that your node is labelled
    properly by running `kubectl describe` as follows:

    ```
    kubectl describe node $NODE_NAME
    ```

    The output should be similar to this:

    ```
    Name:           NODE_NAME
    Role:
    Labels:         beta.kubernetes.io/fluentd-ds-ready=true
    ...
    ```

    Ensure that the output contains the label `beta.kubernetes.io/fluentd-ds-ready=true`. If it
    is not present, you can add it using the `kubectl label` command as follows:

    ```
    kubectl label node $NODE_NAME beta.kubernetes.io/fluentd-ds-ready=true
    ```

    {{< note >}}
    If a node fails and has to be recreated, you must re-apply the label to
    the recreated node. To make this easier, you can use Kubelet's command-line parameter
    for applying node labels in your node startup script.
    {{< /note >}}

1. Deploy a `ConfigMap` with the logging agent configuration by running the following command:

    ```
    kubectl apply -f https://k8s.io/examples/debug/fluentd-gcp-configmap.yaml
    ```

    The command creates the `ConfigMap` in the `default` namespace. You can download the file
    manually and change it before creating the `ConfigMap` object.

1. Deploy the logging agent `DaemonSet` by running the following command:

    ```
    kubectl apply -f https://k8s.io/examples/debug/fluentd-gcp-ds.yaml
    ```

    You can download and edit this file before using it as well.

## Verifying your Logging Agent Deployment

After Stackdriver `DaemonSet` is deployed, you can discover logging agent deployment status
by running the following command:

```shell
kubectl get ds --all-namespaces
```

If you have 3 nodes in the cluster, the output should looks similar to this:

```
NAMESPACE     NAME               DESIRED   CURRENT   READY     NODE-SELECTOR                              AGE
...
default       fluentd-gcp-v2.0   3         3         3         beta.kubernetes.io/fluentd-ds-ready=true   5m
...
```

To understand how logging with Stackdriver works, consider the following
synthetic log generator pod specification [counter-pod.yaml](/examples/debug/counter-pod.yaml):

{{< codenew file="debug/counter-pod.yaml" >}}

This pod specification has one container that runs a bash script
that writes out the value of a counter and the datetime once per
second, and runs indefinitely. Let's create this pod in the default namespace.

```shell
kubectl apply -f https://k8s.io/examples/debug/counter-pod.yaml
```

You can observe the running pod:

```shell
kubectl get pods
```
```
NAME                                           READY     STATUS    RESTARTS   AGE
counter                                        1/1       Running   0          5m
```

For a short period of time you can observe the 'Pending' pod status, because the kubelet
has to download the container image first. When the pod status changes to `Running`
you can use the `kubectl logs` command to view the output of this counter pod.

```shell
kubectl logs counter
```
```
0: Mon Jan  1 00:00:00 UTC 2001
1: Mon Jan  1 00:00:01 UTC 2001
2: Mon Jan  1 00:00:02 UTC 2001
...
```

As described in the logging overview, this command fetches log entries
from the container log file. If the container is killed and then restarted by
Kubernetes, you can still access logs from the previous container. However,
if the pod is evicted from the node, log files are lost. Let's demonstrate this
by deleting the currently running counter container:

```shell
kubectl delete pod counter
```
```
pod "counter" deleted
```

and then recreating it:

```shell
kubectl create -f https://k8s.io/examples/debug/counter-pod.yaml
```
```
pod/counter created
```

After some time, you can access logs from the counter pod again:

```shell
kubectl logs counter
```
```
0: Mon Jan  1 00:01:00 UTC 2001
1: Mon Jan  1 00:01:01 UTC 2001
2: Mon Jan  1 00:01:02 UTC 2001
...
```

As expected, only recent log lines are present. However, for a real-world
application you will likely want to be able to access logs from all containers,
especially for the debug purposes. This is exactly when the previously enabled
Stackdriver Logging can help.

## Viewing logs

Stackdriver Logging agent attaches metadata to each log entry, for you to use later
in queries to select only the messages you're interested in: for example,
the messages from a particular pod.

The most important pieces of metadata are the resource type and log name. There are 
currently 2 [resource models](https://cloud.google.com/stackdriver/docs/solutions/gke#version) 
that use separate metadata values in Stackdriver Logging:
Legacy Logging and Monitoring and Cloud Ops for GKE. For Legacy Logging and Monitoring, 
the resource type of a container log is `container`, which is named
`GKE Containers` in the UI. For Cloud Ops for GKE, the resource type of a container
log is `k8s_container`, which is named `Kubernetes Container` in the UI. The resource
types are used even if the Kubernetes cluster is not on Google Kubernetes Engine).


In Legacy Logging and Monitoring, the log name is the name of the container, so that 
if you have a pod with two containers, named `container_1` and `container_2` in the spec, 
their logs will have log names `container_1` and `container_2` respectively. In Cloud Ops
for GKE, the log names are `stdout` and `stderr` so that logs for both `container_1` and 
`container_2` are both written to the `stdout` and `stderr` log names.


In Legacy Logging and Monitoring, system components have resource type `compute`, which is named
`GCE VM Instance` in the UI. Log names for system components are fixed.
For a Google Kubernetes Engine node, every log entry from a system component has one of the following
log names:

* docker
* kubelet
* kube-proxy

In Cloud Ops for GKE, the node resource type `k8s_node`, which is named `Kubernetes Node` in the UI. 
You can learn more about system and application logs on the [Understanding your logs page](https://cloud.google.com/stackdriver/docs/solutions/gke/using-logs#understanding_your_logs).

You can learn more about viewing logs on [the dedicated Stackdriver page](https://cloud.google.com/logging/docs/view/logs-viewer-interface).

One of the possible ways to view logs is using the
[`gcloud logging`](https://cloud.google.com/logging/docs/api/gcloud-logging)
command line interface from the [Google Cloud SDK](https://cloud.google.com/sdk/).
It uses Stackdriver Logging [query syntax](https://cloud.google.com/logging/docs/view/logging-query-language)
to query specific logs. For example, you can run the following command:

```none
gcloud logging read 'logName="projects/$YOUR_PROJECT_ID/logs/count"' --format json | jq '.[].textPayload'
```
```
...
"2: Mon Jan  1 00:01:02 UTC 2001\n"
"1: Mon Jan  1 00:01:01 UTC 2001\n"
"0: Mon Jan  1 00:01:00 UTC 2001\n"
...
"2: Mon Jan  1 00:00:02 UTC 2001\n"
"1: Mon Jan  1 00:00:01 UTC 2001\n"
"0: Mon Jan  1 00:00:00 UTC 2001\n"
```

As you can see, it outputs messages for the count container from both
the first and second runs, despite the fact that the kubelet already deleted
the logs for the first container.

### Exporting logs

You can export logs to [Google Cloud Storage](https://cloud.google.com/storage/),
 [BigQuery](https://cloud.google.com/bigquery/) or [Cloud Pub/Sub](https://cloud.google.com/pubsub/) 
to run further analysis or to integrate with other logging systems. Stackdriver Logging offers the 
concept of sinks, where you can specify the destination for all or a subset of your log entries. 
More information is available on the Stackdriver [Exporting Logs page](https://cloud.google.com/logging/docs/export/configure_export_v2).

## Configuring Stackdriver Logging Agents

Sometimes the default installation of Stackdriver Logging may not suit your needs, for example:

* You may want to add more resources because default performance doesn't suit your needs.
* You may want to introduce additional parsing to extract more metadata from your log messages,
like severity or source code reference.
* You may want to send logs not only to Stackdriver or send it to Stackdriver only partially.

In this case you need to be able to change the parameters of `DaemonSet` and `ConfigMap`.

### Prerequisites

If you're using GKE and Stackdriver Logging is enabled in your cluster, you
cannot change its configuration, because it's managed and supported by GKE. 
There are several [configuration options](https://cloud.google.com/stackdriver/docs/solutions/gke/installing#migrating) 
which allow you to collect your cluster's system and application logs. However, 
you can disable the default Stackdriver Logging integration and deploy your own. 
Another option is to select the `System logging and monitoring only (beta)` configuration
option available beginning with GKE version 1.15.7 for your cluster to collect 
system logs and metrics about your cluster while using your own configuration 
to collect your application logs. 

{{< note >}}
You will have to support and maintain a newly deployed configuration
yourself: update the image and configuration, adjust the resources and so on.
{{< /note >}}

To select the `System logging and monitoring only (beta)` option available 
beginning with GKE version 1.15.7, use the following command:

```
gcloud beta container clusters update --enable-logging-monitoring-system-only CLUSTER
```

To disable the default logging integration, use the following command:

```
gcloud beta container clusters update --logging-service=none CLUSTER
```

You can find notes on how to then install Stackdriver Logging agents into
a running cluster in the [Deploying section](#deploying).

### Changing `DaemonSet` parameters

When you have the Stackdriver Logging `DaemonSet` in your cluster, you can modify the
`template` field in its spec. The DaemonSet controller manages the pods for you.
For example, assume you've installed the Stackdriver Logging as described above. Now you want to
change the memory limit to give fluentd more memory to safely process more logs.

Get the spec of `DaemonSet` running in your cluster:

```shell
kubectl get ds fluentd-gcp-v2.0 --namespace kube-system -o yaml > fluentd-gcp-ds.yaml
```

Then edit resource requirements in the spec file and update the `DaemonSet` object
in the apiserver using the following command:

```shell
kubectl replace -f fluentd-gcp-ds.yaml
```

After some time, Stackdriver Logging agent pods will be restarted with the new configuration.

### Changing fluentd parameters

Fluentd configuration is stored in the `ConfigMap` object. It is effectively a set of configuration
files that are merged together. You can learn about fluentd configuration on the
[official site](https://docs.fluentd.org).

Imagine you want to add a new parsing logic to the configuration, so that fluentd can understand
default Python logging format. An appropriate fluentd filter looks similar to this:

```
<filter reform.**>
  type parser
  format /^(?<severity>\w):(?<logger_name>\w):(?<log>.*)/
  reserve_data true
  suppress_parse_error_log true
  key_name log
</filter>
```

Now you have to put it in the configuration and make Stackdriver Logging agents pick it up.
Get the current version of the Stackdriver Logging `ConfigMap` in your cluster
by running the following command:

```shell
kubectl get cm fluentd-gcp-config --namespace kube-system -o yaml > fluentd-gcp-configmap.yaml
```

Then in the value of the key `containers.input.conf` insert a new filter right after
the `source` section.

{{< note >}}
Order is important.
{{< /note >}}

Updating `ConfigMap` in the apiserver is more complicated than updating `DaemonSet`. It's better
to consider `ConfigMap` to be immutable. Then, in order to update the configuration, you should
create `ConfigMap` with a new name and then change `DaemonSet` to point to it
using [guide above](#changing-daemonset-parameters).

### Adding fluentd plugins

Fluentd is written in Ruby and allows to extend its capabilities using
[plugins](https://www.fluentd.org/plugins). If you want to use a plugin, which is not included
in the default Stackdriver Logging container image, you have to build a custom image. Imagine
you want to add Kafka sink for messages from a particular container for additional processing.
You can re-use the default [container image sources](https://git.k8s.io/contrib/fluentd/fluentd-gcp-image)
with minor changes:

* Change Makefile to point to your container repository, for example `PREFIX=gcr.io/<your-project-id>`.
* Add your dependency to the Gemfile, for example `gem 'fluent-plugin-kafka'`.

Then run `make build push` from this directory. After updating `DaemonSet` to pick up the
new image, you can use the plugin you installed in the fluentd configuration.


