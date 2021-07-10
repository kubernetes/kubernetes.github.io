---
title: Monitor Node Health
content_type: task
reviewers:
- Random-Liu
- dchen1107
---

<!-- overview -->

*Node problem detector* is a daemon for monitoring and reporting about a node's health.
You can run Node Problem Detector as a `DaemonSet` or as a standalone daemon.
Node Problem Detector collects information about node problems from various daemons
and reports these conditions to the API server as [NodeCondition](/docs/concepts/architecture/nodes/#condition)
and {{< api-reference page="cluster-resources/event-v1" >}}.

To learn how to install and use Node Problem Detector, see
[Node Problem Detector project documentation](https://github.com/kubernetes/node-problem-detector).

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}}

<!-- steps -->

## Limitations

* Node Problem Detector only supports file based kernel log.
  Log tools such as `journald` are not supported.

* Node Problem Detector uses the kernel log format for reporting kernel issues.
  To learn how to extend the kernel log format, see [Add support for another log format](#support-other-log-format).

## Enabling Node Problem Detector

Some cloud providers enable Node Problem Detector as an {{< glossary_tooltip text="Addon" term_id="addons" >}}.
You can also enable Node Problem Detector with `kubectl` or by creating an Addon pod.

### Using kubectl to enable Node Problem Detector {#using-kubectl}

`kubectl` provides the most flexible management of Node Problem Detector.
You can overwrite the default configuration to fit it into your environment or
to detect customized node problems. For example:

1. Create a Node Problem Detector configuration similar to `node-problem-detector.yaml`:

   {{< codenew file="debug/node-problem-detector.yaml" >}}

   {{< note >}}
   You should verify that the system log directory is right for your operating system distribution.
   {{< /note >}}

1. Start node problem detector with `kubectl`:

   ```shell
   kubectl apply -f https://k8s.io/examples/debug/node-problem-detector.yaml
   ```

### Using an Addon pod to enable Node Problem Detector {#using-addon-pod}

If you are using a custom cluster bootstrap solution and don't need
to overwrite the default configuration, you can leverage the Addon pod to
further automate the deployment.

Create `node-problem-detector.yaml`, and save the configuration in the Addon pod's
directory `/etc/kubernetes/addons/node-problem-detector` on a control plane node.

## Overwrite the configuration

The [default configuration](https://github.com/kubernetes/node-problem-detector/tree/v0.1/config)
is embedded when building the Docker image of Node Problem Detector.

However, you can use a [`ConfigMap`](/docs/tasks/configure-pod-container/configure-pod-configmap/)
to overwrite the configuration:

1. Change the configuration files in `config/`
1. Create the `ConfigMap` `node-problem-detector-config`:

   ```shell
   kubectl create configmap node-problem-detector-config --from-file=config/
   ```

1. Change the `node-problem-detector.yaml` to use the `ConfigMap`:

   {{< codenew file="debug/node-problem-detector-configmap.yaml" >}}

1. Recreate the Node Problem Detector with the new configuration file:

   ```shell
   # If you have a node-problem-detector running, delete before recreating
   kubectl delete -f https://k8s.io/examples/debug/node-problem-detector.yaml
   kubectl apply -f https://k8s.io/examples/debug/node-problem-detector-configmap.yaml
   ```

{{< note >}}
This approach only applies to a Node Problem Detector started with `kubectl`.
{{< /note >}}

Overwriting a configuration is not supported if a Node Problem Detector runs as a cluster Addon.
The Addon manager does not support `ConfigMap`.

## Kernel Monitor

*Kernel Monitor* is a system log monitor daemon supported in the Node Problem Detector.
Kernel monitor watches the kernel log and detects known kernel issues following predefined rules.

The Kernel Monitor matches kernel issues according to a set of predefined rule list in
[`config/kernel-monitor.json`](https://github.com/kubernetes/node-problem-detector/blob/v0.1/config/kernel-monitor.json). The rule list is extensible. You can expand the rule list by overwriting the
configuration.

### Add new NodeConditions

To support a new `NodeCondition`, create a condition definition within the `conditions` field in
`config/kernel-monitor.json`, for example:

```json
{
  "type": "NodeConditionType",
  "reason": "CamelCaseDefaultNodeConditionReason",
  "message": "arbitrary default node condition message"
}
```

### Detect new problems

To detect new problems, you can extend the `rules` field in `config/kernel-monitor.json`
with a new rule definition:

```json
{
  "type": "temporary/permanent",
  "condition": "NodeConditionOfPermanentIssue",
  "reason": "CamelCaseShortReason",
  "message": "regexp matching the issue in the kernel log"
}
```

### Configure path for the kernel log device {#kernel-log-device-path}

Check your kernel log path location in your operating system (OS) distribution.
The Linux kernel [log device](https://www.kernel.org/doc/Documentation/ABI/testing/dev-kmsg) is usually presented as `/dev/kmsg`. However, the log path location varies by OS distribution.
The `log` field in `config/kernel-monitor.json` represents the log path inside the container.
You can configure the `log` field to match the device path as seen by the Node Problem Detector.

### Add support for another log format {#support-other-log-format}

Kernel monitor uses the
[`Translator`](https://github.com/kubernetes/node-problem-detector/blob/v0.1/pkg/kernelmonitor/translator/translator.go) plugin to translate the internal data structure of the kernel log.
You can implement a new translator for a new log format.

<!-- discussion -->

## Recommendations and restrictions

It is recommended to run the Node Problem Detector in your cluster to monitor node health.
When running the Node Problem Detector, you can expect extra resource overhead on each node.
Usually this is fine, because:

* The kernel log grows relatively slowly.
* A resource limit is set for the Node Problem Detector.
* Even under high load, the resource usage is acceptable. For more information, see the Node Problem Detector
[benchmark result](https://github.com/kubernetes/node-problem-detector/issues/2#issuecomment-220255629).
