---
reviewers:
- luxas
- jbeda
title: kubeadm join
content_type: concept
weight: 30
---
<!-- overview -->
This command initializes a Kubernetes worker node and joins it to the cluster.

<!-- body -->
{{< include "generated/kubeadm_join.md" >}}

### The join workflow {#join-workflow}

`kubeadm join` bootstraps a Kubernetes worker node or a control-plane node and adds it to the cluster.
This action consists of the following steps for worker nodes:

1. kubeadm downloads necessary cluster information from the API server.
   By default, it uses the bootstrap token and the CA key hash to verify the
   authenticity of that data. The root CA can also be discovered directly via a
   file or URL.

1. Once the cluster information is known, kubelet can start the TLS bootstrapping
   process.

   The TLS bootstrap uses the shared token to temporarily authenticate
   with the Kubernetes API server to submit a certificate signing request (CSR); by
   default the control plane signs this CSR request automatically.

1. Finally, kubeadm configures the local kubelet to connect to the API
   server with the definitive identity assigned to the node.

For control-plane nodes additional steps are performed:

1. Downloading certificates shared among control-plane nodes from the cluster
  (if explicitly requested by the user).

1. Generating control-plane component manifests, certificates and kubeconfig.

1. Adding new local etcd member.

1. Adding this node to the ClusterStatus of the kubeadm cluster.

### Using join phases with kubeadm {#join-phases}

Kubeadm allows you join a node to the cluster in phases using `kubeadm join phase`.

To view the ordered list of phases and sub-phases you can call `kubeadm join --help`. The list will be located
at the top of the help screen and each phase will have a description next to it.
Note that by calling `kubeadm join` all of the phases and sub-phases will be executed in this exact order.

Some phases have unique flags, so if you want to have a look at the list of available options add `--help`, for example:

```shell
kubeadm join phase kubelet-start --help
```

Similar to the [kubeadm init phase](/docs/reference/setup-tools/kubeadm/kubeadm-init/#init-phases)
command, `kubeadm join phase` allows you to skip a list of phases using the `--skip-phases` flag.

For example:

```shell
sudo kubeadm join --skip-phases=preflight --config=config.yaml
```

{{< feature-state for_k8s_version="v1.22" state="beta" >}}

Alternatively, you can use the `skipPhases` field in `JoinConfiguration`.

### Discovering what cluster CA to trust

The kubeadm discovery has several options, each with security tradeoffs.
The right method for your environment depends on how you provision nodes and the
security expectations you have about your network and node lifecycles.

#### Token-based discovery with CA pinning

This is the default mode in kubeadm. In this mode, kubeadm downloads
the cluster configuration (including root CA) and validates it using the token
as well as validating that the root CA public key matches the provided hash and
that the API server certificate is valid under the root CA.

The CA key hash has the format `sha256:<hex_encoded_hash>`. By default, the hash value is returned in the `kubeadm join` command printed at the end of `kubeadm init` or in the output of `kubeadm token create --print-join-command`. It is in a standard format (see [RFC7469](https://tools.ietf.org/html/rfc7469#section-2.4)) and can also be calculated by 3rd party tools or provisioning systems. For example, using the OpenSSL CLI:

```shell
openssl x509 -pubkey -in /etc/kubernetes/pki/ca.crt | openssl rsa -pubin -outform der 2>/dev/null | openssl dgst -sha256 -hex | sed 's/^.* //'
```

**Example `kubeadm join` commands:**

For worker nodes:

```shell
kubeadm join --discovery-token abcdef.1234567890abcdef --discovery-token-ca-cert-hash sha256:1234..cdef 1.2.3.4:6443
```

For control-plane nodes:

```shell
kubeadm join --discovery-token abcdef.1234567890abcdef --discovery-token-ca-cert-hash sha256:1234..cdef --control-plane 1.2.3.4:6443
```

You can also call `join` for a control-plane node with `--certificate-key` to copy certificates to this node,
if the `kubeadm init` command was called with `--upload-certs`.

**Advantages:**

- Allows bootstrapping nodes to securely discover a root of trust for the
  control-plane node even if other worker nodes or the network are compromised.

- Convenient to execute manually since all of the information required fits
  into a single `kubeadm join` command.

**Disadvantages:**

- The CA hash is not normally known until the control-plane node has been provisioned,
  which can make it more difficult to build automated provisioning tools that
  use kubeadm. By generating your CA in beforehand, you may workaround this
  limitation.

#### Token-based discovery without CA pinning

This mode relies only on the symmetric token to sign
(HMAC-SHA256) the discovery information that establishes the root of trust for
the control-plane. To use the mode the joining nodes must skip the hash validation of the
CA public key, using `--discovery-token-unsafe-skip-ca-verification`. You should consider
using one of the other modes if possible.

**Example `kubeadm join` command:**

```shell
kubeadm join --token abcdef.1234567890abcdef --discovery-token-unsafe-skip-ca-verification 1.2.3.4:6443
```

**Advantages:**

- Still protects against many network-level attacks.

- The token can be generated ahead of time and shared with the control-plane node and
  worker nodes, which can then bootstrap in parallel without coordination. This
  allows it to be used in many provisioning scenarios.

**Disadvantages:**

- If an attacker is able to steal a bootstrap token via some vulnerability,
  they can use that token (along with network-level access) to impersonate the
  control-plane node to other bootstrapping nodes. This may or may not be an appropriate
  tradeoff in your environment.

#### File or HTTPS-based discovery

This provides an out-of-band way to establish a root of trust between the control-plane node
and bootstrapping nodes. Consider using this mode if you are building automated provisioning
using kubeadm. The format of the discovery file is a regular Kubernetes
[kubeconfig](/docs/tasks/access-application-cluster/configure-access-multiple-clusters/) file.

In case the discovery file does not contain credentials, the TLS discovery token will be used.

**Example `kubeadm join` commands:**

- `kubeadm join --discovery-file path/to/file.conf` (local file)

- `kubeadm join --discovery-file https://url/file.conf` (remote HTTPS URL)

**Advantages:**

- Allows bootstrapping nodes to securely discover a root of trust for the
  control-plane node even if the network or other worker nodes are compromised.

**Disadvantages:**

- Requires that you have some way to carry the discovery information from
  the control-plane node to the bootstrapping nodes. If the discovery file contains credentials
  you must keep it secret and transfer it over a secure channel. This might be possible with your
  cloud provider or provisioning tool.

### Securing your installation even more {#securing-more}

The defaults for kubeadm may not work for everyone. This section documents how to tighten up a kubeadm installation
at the cost of some usability.

#### Turning off auto-approval of node client certificates

By default, there is a CSR auto-approver enabled that basically approves any client certificate request
for a kubelet when a Bootstrap Token was used when authenticating. If you don't want the cluster to
automatically approve kubelet client certs, you can turn it off by executing this command:

```shell
kubectl delete clusterrolebinding kubeadm:node-autoapprove-bootstrap
```

After that, `kubeadm join` will block until the admin has manually approved the CSR in flight:

```shell
kubectl get csr
```

The output is similar to this:

```
NAME                                                   AGE       REQUESTOR                 CONDITION
node-csr-c69HXe7aYcqkS1bKmH4faEnHAWxn6i2bHZ2mD04jZyQ   18s       system:bootstrap:878f07   Pending
```

```shell
kubectl certificate approve node-csr-c69HXe7aYcqkS1bKmH4faEnHAWxn6i2bHZ2mD04jZyQ
```

The output is similar to this:

```
certificatesigningrequest "node-csr-c69HXe7aYcqkS1bKmH4faEnHAWxn6i2bHZ2mD04jZyQ" approved
```

```shell
kubectl get csr
```

The output is similar to this:

```
NAME                                                   AGE       REQUESTOR                 CONDITION
node-csr-c69HXe7aYcqkS1bKmH4faEnHAWxn6i2bHZ2mD04jZyQ   1m        system:bootstrap:878f07   Approved,Issued
```

This forces the workflow that `kubeadm join` will only succeed if `kubectl certificate approve` has been run.

#### Turning off public access to the cluster-info ConfigMap

In order to achieve the joining flow using the token as the only piece of validation information, a
 ConfigMap with some data needed for validation of the control-plane node's identity is exposed publicly by
default. While there is no private data in this ConfigMap, some users might wish to turn
it off regardless. Doing so will disable the ability to use the `--discovery-token` flag of the
`kubeadm join` flow. Here are the steps to do so:

* Fetch the `cluster-info` file from the API Server:

```shell
kubectl -n kube-public get cm cluster-info -o yaml | grep "kubeconfig:" -A11 | grep "apiVersion" -A10 | sed "s/    //" | tee cluster-info.yaml
```

The output is similar to this:

```
apiVersion: v1
kind: Config
clusters:
- cluster:
    certificate-authority-data: <ca-cert>
    server: https://<ip>:<port>
  name: ""
contexts: []
current-context: ""
preferences: {}
users: []
```

* Use the `cluster-info.yaml` file as an argument to `kubeadm join --discovery-file`.

* Turn off public access to the `cluster-info` ConfigMap:

```shell
kubectl -n kube-public delete rolebinding kubeadm:bootstrap-signer-clusterinfo
```

These commands should be run after `kubeadm init` but before `kubeadm join`.

### Using kubeadm join with a configuration file {#config-file}

{{< caution >}}
The config file is still considered beta and may change in future versions.
{{< /caution >}}

It's possible to configure `kubeadm join` with a configuration file instead of command
line flags, and some more advanced features may only be available as
configuration file options. This file is passed using the `--config` flag and it must
contain a `JoinConfiguration` structure. Mixing `--config` with others flags may not be
allowed in some cases.

The default configuration can be printed out using the
[kubeadm config print](/docs/reference/setup-tools/kubeadm/kubeadm-config/) command.

If your configuration is not using the latest version it is **recommended** that you migrate using
the [kubeadm config migrate](/docs/reference/setup-tools/kubeadm/kubeadm-config/) command.

For more information on the fields and usage of the configuration you can navigate to our API reference
page and pick a version from [the list](https://godoc.org/k8s.io/kubernetes/cmd/kubeadm/app/apis/kubeadm#pkg-subdirectories).

## {{% heading "whatsnext" %}}

* [kubeadm init](/docs/reference/setup-tools/kubeadm/kubeadm-init/) to bootstrap a Kubernetes control-plane node
* [kubeadm token](/docs/reference/setup-tools/kubeadm/kubeadm-token/) to manage tokens for `kubeadm join`
* [kubeadm reset](/docs/reference/setup-tools/kubeadm/kubeadm-reset/) to revert any changes made to this host by `kubeadm init` or `kubeadm join`
