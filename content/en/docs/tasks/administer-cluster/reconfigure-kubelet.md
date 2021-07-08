---
reviewers:
- mtaufen
- dawnchen
title: Reconfigure a Node's Kubelet in a Live Cluster
content_type: task
min-kubernetes-server-version: v1.11
---

<!-- overview -->
{{< feature-state for_k8s_version="v1.11" state="beta" >}}

[Dynamic Kubelet Configuration](https://github.com/kubernetes/enhancements/issues/281)
allows you to change the configuration of each
{{< glossary_tooltip text="kubelet" term_id="kubelet" >}} in a running Kubernetes cluster,
by deploying a {{< glossary_tooltip text="ConfigMap" term_id="configmap" >}} and configuring
each {{< glossary_tooltip term_id="node" >}} to use it.

{{< warning >}}
All kubelet configuration parameters can be changed dynamically,
but this is unsafe for some parameters. Before deciding to change a parameter
dynamically, you need a strong understanding of how that change will affect your
cluster's behavior. Always carefully test configuration changes on a small set
of nodes before rolling them out cluster-wide. Advice on configuring specific
fields is available in the inline
[`KubeletConfiguration`](/docs/reference/config-api/kubelet-config.v1beta1/).
{{< /warning >}}


## {{% heading "prerequisites" %}}

You need to have a Kubernetes cluster.
You also need kubectl v1.11 or higher, configured to communicate with your cluster.
{{< version-check >}}
Your cluster API server version (eg v1.12) must be no more than one minor
version away from the version of kubectl that you are using. For example,
if your cluster is running v1.16 then you can use kubectl v1.15, v1.16
or v1.17; other combinations
[aren't supported](/docs/setup/release/version-skew-policy/#kubectl).

Some of the examples use the command line tool
[jq](https://stedolan.github.io/jq/). You do not need `jq` to complete the task,
because there are manual alternatives.

For each node that you're reconfiguring, you must set the kubelet
`--dynamic-config-dir` flag to a writable directory.


<!-- steps -->

## Reconfiguring the kubelet on a running node in your cluster

### Basic workflow overview

The basic workflow for configuring a kubelet in a live cluster is as follows:

1. Write a YAML or JSON configuration file containing the
   kubelet's configuration.
2. Wrap this file in a ConfigMap and save it to the Kubernetes control plane.
3. Update the kubelet's corresponding Node object to use this ConfigMap.

Each kubelet watches a configuration reference on its respective Node object.
When this reference changes, the kubelet downloads the new configuration,
updates a local reference to refer to the file, and exits.
For the feature to work correctly, you must be running an OS-level service
manager (such as systemd), which will restart the kubelet if it exits. When the
kubelet is restarted, it will begin using the new configuration.

The new configuration completely overrides configuration provided by `--config`,
and is overridden by command-line flags. Unspecified values in the new configuration
will receive default values appropriate to the configuration version
(e.g. `kubelet.config.k8s.io/v1beta1`), unless overridden by flags.

The status of the Node's kubelet configuration is reported via
`Node.Status.Config`. Once you have updated a Node to use the new
ConfigMap, you can observe this status to confirm that the Node is using the
intended configuration.

This document describes editing Nodes using `kubectl edit`.
There are other ways to modify a Node's spec, including `kubectl patch`, for
example, which facilitate scripted workflows.

This document only describes a single Node consuming each ConfigMap. Keep in
mind that it is also valid for multiple Nodes to consume the same ConfigMap.

{{< warning >}}
While it is *possible* to change the configuration by
updating the ConfigMap in-place, this causes all kubelets configured with
that ConfigMap to update simultaneously. It is much safer to treat ConfigMaps
as immutable by convention, aided by `kubectl`'s `--append-hash` option,
and incrementally roll out updates to `Node.Spec.ConfigSource`.
{{< /warning >}}

### Automatic RBAC rules for Node Authorizer

Previously, you were required to manually create RBAC rules
to allow Nodes to access their assigned ConfigMaps. The Node Authorizer now
automatically configures these rules.

### Generating a file that contains the current configuration

The Dynamic Kubelet Configuration feature allows you to provide an override for
the entire configuration object, rather than a per-field overlay. This is a
simpler model that makes it easier to trace the source of configuration values
and debug issues. The compromise, however, is that you must start with knowledge
of the existing configuration to ensure that you only change the fields you
intend to change.

The kubelet loads settings from its configuration file, but you can set command
line flags to override the configuration in the file. This means that if you
only know the contents of the configuration file, and you don't know the
command line overrides, then you do not know the running configuration either.

Because you need to know the running configuration in order to override it,
you can fetch the running configuration from the kubelet. You can generate a
config file containing a Node's current configuration by accessing the kubelet's
`configz` endpoint, through `kubectl proxy`. The next section explains how to
do this.

{{< caution >}}
The kubelet's `configz` endpoint is there to help with debugging, and is not
a stable part of kubelet behavior.
Do not rely on the behavior of this endpoint for production scenarios or for
use with automated tools.
{{< /caution >}}

For more information on configuring the kubelet via a configuration file, see
[Set kubelet parameters via a config file](/docs/tasks/administer-cluster/kubelet-config-file)).

#### Generate the configuration file

{{< note >}}
The steps below use the `jq` command to streamline working with JSON.
To follow the tasks as written, you need to have `jq` installed. You can
adapt the steps if you prefer to extract the `kubeletconfig` subobject manually.
{{< /note >}}

1. Choose a Node to reconfigure. In this example, the name of this Node is
   referred to as `NODE_NAME`.
2. Start the kubectl proxy in the background using the following command:

   ```shell
   kubectl proxy --port=8001 &
   ```
3. Run the following command to download and unpack the configuration from the
   `configz` endpoint. The command is long, so be careful when copying and
   pasting. **If you use zsh**, note that common zsh configurations add backslashes
   to escape the opening and closing curly braces around the variable name in the URL.
   For example: `${NODE_NAME}` will be rewritten as `$\{NODE_NAME\}` during the paste.
   You must remove the backslashes before running the command, or the command will fail.


   ```bash
   NODE_NAME="the-name-of-the-node-you-are-reconfiguring"; curl -sSL "http://localhost:8001/api/v1/nodes/${NODE_NAME}/proxy/configz" | jq '.kubeletconfig|.kind="KubeletConfiguration"|.apiVersion="kubelet.config.k8s.io/v1beta1"' > kubelet_configz_${NODE_NAME}
   ```

{{< note >}}
You need to manually add the `kind` and `apiVersion` to the downloaded
object, because those fields are not reported by the `configz` endpoint.
{{< /note >}}

#### Edit the configuration file

Using a text editor, change one of the parameters in the
file generated by the previous procedure. For example, you
might edit the parameter `eventRecordQPS`, that controls
rate limiting for event recording.

#### Push the configuration file to the control plane

Push the edited configuration file to the control plane with the
following command:

```bash
kubectl -n kube-system create configmap my-node-config --from-file=kubelet=kubelet_configz_${NODE_NAME} --append-hash -o yaml
```

This is an example of a valid response:

```none
apiVersion: v1
kind: ConfigMap
metadata:
  creationTimestamp: 2017-09-14T20:23:33Z
  name: my-node-config-gkt4c2m4b2
  namespace: kube-system
  resourceVersion: "119980"
  uid: 946d785e-998a-11e7-a8dd-42010a800006
data:
  kubelet: |
    {...}
```

You created that ConfigMap inside the `kube-system` namespace because the kubelet
is a Kubernetes system component.

The `--append-hash` option appends a short checksum of the ConfigMap contents
to the name. This is convenient for an edit-then-push workflow, because it
automatically, yet deterministically, generates new names for new resources.
The name that includes this generated hash is referred to as `CONFIG_MAP_NAME`
in the following examples.

#### Set the Node to use the new configuration

Edit the Node's reference to point to the new ConfigMap with the
following command:

```bash
kubectl edit node ${NODE_NAME}
```

In your text editor, add the following YAML under `spec`:

```yaml
configSource:
    configMap:
        name: CONFIG_MAP_NAME # replace CONFIG_MAP_NAME with the name of the ConfigMap
        namespace: kube-system
        kubeletConfigKey: kubelet
```

You must specify all three of `name`, `namespace`, and `kubeletConfigKey`.
The `kubeletConfigKey` parameter shows the kubelet which key of the ConfigMap
contains its config.

#### Observe that the Node begins using the new configuration

Retrieve the Node using the `kubectl get node ${NODE_NAME} -o yaml` command and inspect
`Node.Status.Config`. The config sources corresponding to the `active`,
`assigned`, and `lastKnownGood` configurations are reported in the status.

- The `active` configuration is the version the kubelet is currently running with.
- The `assigned` configuration is the latest version the kubelet has resolved based on
  `Node.Spec.ConfigSource`.
- The `lastKnownGood` configuration is the version the
  kubelet will fall back to if an invalid config is assigned in `Node.Spec.ConfigSource`.

The`lastKnownGood` configuration might not be present if it is set to its default value,
the local config deployed with the node. The status will update `lastKnownGood` to
match a valid `assigned` config after the kubelet becomes comfortable with the config.
The details of how the kubelet determines a config should become the `lastKnownGood` are
not guaranteed by the API, but is currently implemented as a 10-minute grace period.

You can use the following command (using `jq`) to filter down
to the config status:

```bash
kubectl get no ${NODE_NAME} -o json | jq '.status.config'
```

The following is an example response:

```json
{
  "active": {
    "configMap": {
      "kubeletConfigKey": "kubelet",
      "name": "my-node-config-9mbkccg2cc",
      "namespace": "kube-system",
      "resourceVersion": "1326",
      "uid": "705ab4f5-6393-11e8-b7cc-42010a800002"
    }
  },
  "assigned": {
    "configMap": {
      "kubeletConfigKey": "kubelet",
      "name": "my-node-config-9mbkccg2cc",
      "namespace": "kube-system",
      "resourceVersion": "1326",
      "uid": "705ab4f5-6393-11e8-b7cc-42010a800002"
    }
  },
  "lastKnownGood": {
    "configMap": {
      "kubeletConfigKey": "kubelet",
      "name": "my-node-config-9mbkccg2cc",
      "namespace": "kube-system",
      "resourceVersion": "1326",
      "uid": "705ab4f5-6393-11e8-b7cc-42010a800002"
    }
  }
}

```

(if you do not have `jq`, you can look at the whole response and find `Node.Status.Config`
by eye).

If an error occurs, the kubelet reports it in the `Node.Status.Config.Error`
structure. Possible errors are listed in
[Understanding Node.Status.Config.Error messages](#understanding-node-config-status-errors).
You can search for the identical text in the kubelet log for additional details
and context about the error.

#### Make more changes

Follow the workflow above to make more changes and push them again. Each time
you push a ConfigMap with new contents, the `--append-hash` kubectl option creates
the ConfigMap with a new name. The safest rollout strategy is to first create a
new ConfigMap, and then update the Node to use the new ConfigMap.

#### Reset the Node to use its local default configuration

To reset the Node to use the configuration it was provisioned with, edit the
Node using `kubectl edit node ${NODE_NAME}` and remove the
`Node.Spec.ConfigSource` field.

#### Observe that the Node is using its local default configuration

After removing this subfield, `Node.Status.Config` eventually becomes
empty, since all config sources have been reset to `nil`, which indicates that
the local default config is `assigned`, `active`, and `lastKnownGood`, and no
error is reported.

<!-- discussion -->
## `kubectl patch` example

You can change a Node's configSource using several different mechanisms.
This example uses `kubectl patch`:

```bash
kubectl patch node ${NODE_NAME} -p "{\"spec\":{\"configSource\":{\"configMap\":{\"name\":\"${CONFIG_MAP_NAME}\",\"namespace\":\"kube-system\",\"kubeletConfigKey\":\"kubelet\"}}}}"
```

## Understanding how the kubelet checkpoints config

When a new config is assigned to the Node, the kubelet downloads and unpacks the
config payload as a set of files on the local disk. The kubelet also records metadata
that locally tracks the assigned and last-known-good config sources, so that the
kubelet knows which config to use across restarts, even if the API server becomes
unavailable. After checkpointing a config and the relevant metadata, the kubelet
exits if it detects that the assigned config has changed. When the kubelet is
restarted by the OS-level service manager (such as `systemd`), it reads the new
metadata and uses the new config.

The recorded metadata is fully resolved, meaning that it contains all necessary
information to choose a specific config version - typically a `UID` and `ResourceVersion`.
This is in contrast to `Node.Spec.ConfigSource`, where the intended config is declared
via the idempotent `namespace/name` that identifies the target ConfigMap; the kubelet
tries to use the latest version of this ConfigMap.

When you are debugging problems on a node, you can inspect the kubelet's config
metadata and checkpoints. The structure of the kubelet's checkpointing directory is:

```none
- --dynamic-config-dir (root for managing dynamic config)
| - meta
  | - assigned (encoded kubeletconfig/v1beta1.SerializedNodeConfigSource object, indicating the assigned config)
  | - last-known-good (encoded kubeletconfig/v1beta1.SerializedNodeConfigSource object, indicating the last-known-good config)
| - checkpoints
  | - uid1 (dir for versions of object identified by uid1)
    | - resourceVersion1 (dir for unpacked files from resourceVersion1 of object with uid1)
    | - ...
  | - ...
```

## Understanding `Node.Status.Config.Error` messages {#understanding-node-config-status-errors}

The following table describes error messages that can occur
when using Dynamic Kubelet Config. You can search for the identical text
in the Kubelet log for additional details and context about the error.

{{< table caption = "Understanding Node.Status.Config.Error messages" >}}

Error Message | Possible Causes
:-------------| :--------------
failed to load config, see Kubelet log for details | The kubelet likely could not parse the downloaded config payload, or encountered a filesystem error attempting to load the payload from disk.
failed to validate config, see Kubelet log for details | The configuration in the payload, combined with any command-line flag overrides, and the sum of feature gates from flags, the config file, and the remote payload, was determined to be invalid by the kubelet.
invalid NodeConfigSource, exactly one subfield must be non-nil, but all were nil | Since Node.Spec.ConfigSource is validated by the API server to contain at least one non-nil subfield, this likely means that the kubelet is older than the API server and does not recognize a newer source type.
failed to sync: failed to download config, see Kubelet log for details | The kubelet could not download the config. It is possible that Node.Spec.ConfigSource could not be resolved to a concrete API object, or that network errors disrupted the download attempt. The kubelet will retry the download when in this error state.
failed to sync: internal failure, see Kubelet log for details | The kubelet encountered some internal problem and failed to update its config as a result. Examples include filesystem errors and reading objects from the internal informer cache.
internal failure, see Kubelet log for details | The kubelet encountered some internal problem while manipulating config, outside of the configuration sync loop.

{{< /table >}}


## {{% heading "whatsnext" %}}

- For more information on configuring the kubelet via a configuration file, see
[Set kubelet parameters via a config file](/docs/tasks/administer-cluster/kubelet-config-file).
- See the reference documentation for {{< api-reference page="cluster-resources/node-v1" anchor="NodeConfigSource" >}}.
- Learn more about kubelet configuration by checking the
  [`KubeletConfiguration`](/docs/reference/config-api/kubelet-config.v1beta1/)
  reference.
