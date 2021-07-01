---
reviewers:
- luxas
- jbeda
title: Implementation details
content_type: concept
weight: 100
---
<!-- overview -->

{{< feature-state for_k8s_version="v1.10" state="stable" >}}

`kubeadm init` and `kubeadm join` together provides a nice user experience for creating a best-practice but bare Kubernetes cluster from scratch.
However, it might not be obvious _how_ kubeadm does that.

This document provides additional details on what happen under the hood, with the aim of sharing knowledge on Kubernetes cluster best practices.

<!-- body -->
## Core design principles

The cluster that `kubeadm init` and `kubeadm join` set up should be:

 - **Secure**: It should adopt latest best-practices like:
   - enforcing RBAC
   - using the Node Authorizer
   - using secure communication between the control plane components
   - using secure communication between the API server and the kubelets
   - lock-down the kubelet API
   - locking down access to the API for system components like the kube-proxy and CoreDNS
   - locking down what a Bootstrap Token can access
 - **User-friendly**: The user should not have to run anything more than a couple of commands:
   - `kubeadm init`
   - `export KUBECONFIG=/etc/kubernetes/admin.conf`
   - `kubectl apply -f <network-of-choice.yaml>`
   - `kubeadm join --token <token> <endpoint>:<port>`
 - **Extendable**:
   - It should _not_ favor any particular network provider. Configuring the cluster network is out-of-scope
   - It should provide the possibility to use a config file for customizing various parameters

## Constants and well-known values and paths

In order to reduce complexity and to simplify development of higher level tools that build on top of kubeadm, it uses a
limited set of constant values for well-known paths and file names.

The Kubernetes directory `/etc/kubernetes` is a constant in the application, since it is clearly the given path
in a majority of cases, and the most intuitive location; other constants paths and file names are:

- `/etc/kubernetes/manifests` as the path where kubelet should look for static Pod manifests. Names of static Pod manifests are:
    - `etcd.yaml`
    - `kube-apiserver.yaml`
    - `kube-controller-manager.yaml`
    - `kube-scheduler.yaml`
- `/etc/kubernetes/` as the path where kubeconfig files with identities for control plane components are stored. Names of kubeconfig files are:
    - `kubelet.conf` (`bootstrap-kubelet.conf` during TLS bootstrap)
    - `controller-manager.conf`
    - `scheduler.conf`
    - `admin.conf` for the cluster admin and kubeadm itself
- Names of certificates and key files :
    - `ca.crt`, `ca.key` for the Kubernetes certificate authority
    - `apiserver.crt`, `apiserver.key` for the API server certificate
    - `apiserver-kubelet-client.crt`, `apiserver-kubelet-client.key` for the client certificate used by the API server to connect to the kubelets securely
    - `sa.pub`, `sa.key` for the key used by the controller manager when signing ServiceAccount
    - `front-proxy-ca.crt`, `front-proxy-ca.key` for the front proxy certificate authority
    - `front-proxy-client.crt`, `front-proxy-client.key` for the front proxy client

## kubeadm init workflow internal design

The `kubeadm init` [internal workflow](/docs/reference/setup-tools/kubeadm/kubeadm-init/#init-workflow) consists of a sequence of atomic work tasks to perform,
as described in `kubeadm init`.

The [`kubeadm init phase`](/docs/reference/setup-tools/kubeadm/kubeadm-init-phase/) command allows users to invoke each task individually, and ultimately offers a reusable and composable
API/toolbox that can be used by other Kubernetes bootstrap tools, by any IT automation tool or by an advanced user
for creating custom clusters.

### Preflight checks

Kubeadm executes a set of preflight checks before starting the init, with the aim to verify preconditions and avoid common cluster startup problems.
The user can skip specific preflight checks or all of them with the `--ignore-preflight-errors` option.

- [warning] If the Kubernetes version to use (specified with the `--kubernetes-version` flag) is at least one minor version higher than the kubeadm CLI version.
- Kubernetes system requirements:
  - if running on linux:
    - [error] if Kernel is older than the minimum required version
    - [error] if required cgroups subsystem aren't in set up
  - if using docker:
    - [warning/error] if Docker service does not exist, if it is disabled, if it is not active.
    - [error] if Docker endpoint does not exist or does not work
    - [warning] if docker version is not in the list of validated docker versions
  - If using other cri engine:
    - [error] if crictl socket does not answer
- [error] if user is not root
- [error] if the machine hostname is not a valid DNS subdomain
- [warning] if the host name cannot be reached via network lookup
- [error] if kubelet version is lower that the minimum kubelet version supported by kubeadm (current minor -1)
- [error] if kubelet version is at least one minor higher than the required controlplane version (unsupported version skew)
- [warning] if kubelet service does not exist or if it is disabled
- [warning] if firewalld is active
- [error] if API server bindPort or ports 10250/10251/10252 are used
- [Error] if `/etc/kubernetes/manifest` folder already exists and it is not empty
- [Error] if `/proc/sys/net/bridge/bridge-nf-call-iptables` file does not exist/does not contain 1
- [Error] if advertise address is ipv6 and `/proc/sys/net/bridge/bridge-nf-call-ip6tables` does not exist/does not contain 1.
- [Error] if swap is on
- [Error] if `conntrack`, `ip`, `iptables`,  `mount`, `nsenter` commands are not present in the command path
- [warning] if `ebtables`, `ethtool`, `socat`, `tc`, `touch`, `crictl` commands are not present in the command path
- [warning] if extra arg flags for API server, controller manager,  scheduler contains some invalid options
- [warning] if connection to https://API.AdvertiseAddress:API.BindPort goes through proxy
- [warning] if connection to services subnet goes through proxy (only first address checked)
- [warning] if connection to Pods subnet goes through proxy (only first address checked)
- If external etcd is provided:
  - [Error] if etcd version is older than the minimum required version
  - [Error] if etcd certificates or keys are specified, but not provided
- If external etcd is NOT provided (and thus local etcd will be installed):
  - [Error] if ports 2379 is used
  - [Error] if Etcd.DataDir folder already exists and it is not empty
- If authorization mode is ABAC:
  - [Error] if abac_policy.json does not exist
- If authorization mode is WebHook
  - [Error] if webhook_authz.conf does not exist

Please note that:

1. Preflight checks can be invoked individually with the [`kubeadm init phase preflight`](/docs/reference/setup-tools/kubeadm/kubeadm-init-phase/#cmd-phase-preflight) command

### Generate the necessary certificates

Kubeadm generates certificate and private key pairs for different purposes:

 - A self signed certificate authority for the Kubernetes cluster saved into `ca.crt` file and `ca.key` private key file
 - A serving certificate for the API server, generated using `ca.crt` as the CA, and saved into `apiserver.crt` file with
   its private key `apiserver.key`. This certificate should contain following alternative names:
     - The Kubernetes service's internal clusterIP (the first address in the services CIDR, e.g. `10.96.0.1` if service subnet is `10.96.0.0/12`)
     - Kubernetes DNS names, e.g.  `kubernetes.default.svc.cluster.local` if `--service-dns-domain` flag value is `cluster.local`, plus default DNS names `kubernetes.default.svc`, `kubernetes.default`, `kubernetes`
     - The node-name
     - The `--apiserver-advertise-address`
     - Additional alternative names specified by the user
 - A client certificate for the API server to connect to the kubelets securely, generated using `ca.crt` as the CA and saved into
   `apiserver-kubelet-client.crt` file with its private key `apiserver-kubelet-client.key`.
   This certificate should be in the `system:masters` organization
 - A private key for signing ServiceAccount Tokens saved into `sa.key` file along with its public key `sa.pub`
 - A certificate authority for the front proxy saved into `front-proxy-ca.crt` file with its key `front-proxy-ca.key`
 - A client cert for the front proxy client, generate using `front-proxy-ca.crt` as the CA and saved into `front-proxy-client.crt` file
   with its private key`front-proxy-client.key`

Certificates are stored by default in `/etc/kubernetes/pki`, but this directory is configurable using the `--cert-dir` flag.

 Please note that:

1. If a given certificate and private key pair both exist, and its content is evaluated compliant with the above specs, the existing files will
   be used and the generation phase for the given certificate skipped. This means the user can, for example, copy an existing CA to
   `/etc/kubernetes/pki/ca.{crt,key}`, and then kubeadm will use those files for signing the rest of the certs.
   See also [using custom certificates](/docs/tasks/administer-cluster/kubeadm/kubeadm-certs#custom-certificates)
2. Only for the CA, it is possible to provide the `ca.crt` file but not the `ca.key` file, if all other certificates and kubeconfig files
   already are in place kubeadm recognize this condition and activates the ExternalCA , which also implies the `csrsigner`controller in
   controller-manager won't be started
3. If kubeadm is running in [external CA mode](/docs/tasks/administer-cluster/kubeadm/kubeadm-certs#external-ca-mode);
   all the certificates must be provided by the user, because kubeadm cannot generate them by itself
4. In case of kubeadm is executed in the `--dry-run` mode, certificates files are written in a temporary folder
5. Certificate generation can be invoked individually with the [`kubeadm init phase certs all`](/docs/reference/setup-tools/kubeadm/kubeadm-init-phase/#cmd-phase-certs) command

### Generate kubeconfig files for control plane components

Kubeadm generates kubeconfig files with identities for control plane components:

- A kubeconfig file for the kubelet to use during TLS bootstrap - /etc/kubernetes/bootstrap-kubelet.conf. Inside this file there is a bootstrap-token or embedded client certificates for authenticating this node with the cluster.
  This client cert should:
    - Be in the `system:nodes` organization, as required by the [Node Authorization](/docs/reference/access-authn-authz/node/) module
    - Have the Common Name (CN) `system:node:<hostname-lowercased>`
- A kubeconfig file for controller-manager, `/etc/kubernetes/controller-manager.conf`; inside this file is embedded a client
  certificate with controller-manager identity. This client cert should have the CN `system:kube-controller-manager`, as defined
by default [RBAC core components roles](/docs/reference/access-authn-authz/rbac/#core-component-roles)
- A kubeconfig file for scheduler, `/etc/kubernetes/scheduler.conf`; inside this file is embedded a client certificate with scheduler identity.
  This client cert should have the CN `system:kube-scheduler`, as defined by default [RBAC core components roles](/docs/reference/access-authn-authz/rbac/#core-component-roles)

Additionally, a kubeconfig file for kubeadm itself and the admin is generated and saved into the `/etc/kubernetes/admin.conf` file.
The "admin" here is defined as the actual person(s) that is administering the cluster and wants to have full control (**root**) over the cluster.
The embedded client certificate for admin should be in the `system:masters` organization, as defined by default
[RBAC user facing role bindings](/docs/reference/access-authn-authz/rbac/#user-facing-roles). It should also include a
CN. Kubeadm uses the `kubernetes-admin` CN.

Please note that:

1. `ca.crt` certificate is embedded in all the kubeconfig files.
2. If a given kubeconfig file exists, and its content is evaluated compliant with the above specs, the existing file will be used and the generation phase for the given kubeconfig skipped
3. If kubeadm is running in [ExternalCA mode](/docs/reference/setup-tools/kubeadm/kubeadm-init/#external-ca-mode), all the required kubeconfig must be provided by the user as well, because kubeadm cannot generate any of them by itself
4. In case of kubeadm is executed in the `--dry-run` mode, kubeconfig files are written in a temporary folder
5. Kubeconfig files generation can be invoked individually with the [`kubeadm init phase kubeconfig all`](/docs/reference/setup-tools/kubeadm/kubeadm-init-phase/#cmd-phase-kubeconfig) command

### Generate static Pod manifests for control plane components

Kubeadm writes static Pod manifest files for control plane components to `/etc/kubernetes/manifests`. The kubelet watches this directory for Pods to create on startup.

Static Pod manifest share a set of common properties:

- All static Pods are deployed on `kube-system` namespace
- All static Pods get `tier:control-plane` and `component:{component-name}` labels
- All static Pods use the `system-node-critical` priority class
- `hostNetwork: true` is set on all static Pods to allow control plane startup before a network is configured; as a consequence:
  * The `address` that the controller-manager and the scheduler use to refer the API server is `127.0.0.1`
  * If using a local etcd server, `etcd-servers` address will be set to `127.0.0.1:2379`
- Leader election is enabled for both the controller-manager and the scheduler
- Controller-manager and the scheduler will reference kubeconfig files with their respective, unique identities
- All static Pods get any extra flags specified by the user as described in [passing custom arguments to control plane components](/docs/setup/production-environment/tools/kubeadm/control-plane-flags/)
- All static Pods get any extra Volumes specified by the user (Host path)

Please note that:

1. All images will be pulled from k8s.gcr.io by default. See [using custom images](/docs/reference/setup-tools/kubeadm/kubeadm-init/#custom-images) for customizing the image repository
2. In case of kubeadm is executed in the `--dry-run` mode, static Pods files are written in a temporary folder
3. Static Pod manifest generation for control plane components can be invoked individually with the [`kubeadm init phase control-plane all`](/docs/reference/setup-tools/kubeadm/kubeadm-init-phase/#cmd-phase-control-plane) command

#### API server

The static Pod manifest for the API server is affected by following parameters provided by the users:

 - The `apiserver-advertise-address` and `apiserver-bind-port` to bind to; if not provided, those value defaults to the IP address of
   the default network interface on the machine and port 6443
 - The `service-cluster-ip-range` to use for services
 - If an external etcd server is specified, the `etcd-servers` address and related TLS settings (`etcd-cafile`, `etcd-certfile`, `etcd-keyfile`);
   if an external etcd server is not be provided, a local etcd will be used (via host network)
 - If a cloud provider is specified, the corresponding `--cloud-provider` is configured, together with the  `--cloud-config` path
   if such file exists (this is experimental, alpha and will be removed in a future version)

Other API server flags that are set unconditionally are:

 - `--insecure-port=0` to avoid insecure connections to the api server
 - `--enable-bootstrap-token-auth=true` to enable the `BootstrapTokenAuthenticator` authentication module.
   See [TLS Bootstrapping](/docs/reference/command-line-tools-reference/kubelet-tls-bootstrapping/) for more details
 - `--allow-privileged` to `true` (required e.g. by kube proxy)
 - `--requestheader-client-ca-file` to `front-proxy-ca.crt`
 - `--enable-admission-plugins` to:
    - [`NamespaceLifecycle`](/docs/reference/access-authn-authz/admission-controllers/#namespacelifecycle) e.g. to avoid deletion of
      system reserved namespaces
    - [`LimitRanger`](/docs/reference/access-authn-authz/admission-controllers/#limitranger) and [`ResourceQuota`](/docs/reference/access-authn-authz/admission-controllers/#resourcequota) to enforce limits on namespaces
    - [`ServiceAccount`](/docs/reference/access-authn-authz/admission-controllers/#serviceaccount) to enforce service account automation
    - [`PersistentVolumeLabel`](/docs/reference/access-authn-authz/admission-controllers/#persistentvolumelabel) attaches region or zone labels to
      PersistentVolumes as defined by the cloud provider (This admission controller is deprecated and will be removed in a future version.
      It is not deployed by kubeadm by default with v1.9 onwards when not explicitly opting into using `gce` or `aws` as cloud providers)
    - [`DefaultStorageClass`](/docs/reference/access-authn-authz/admission-controllers/#defaultstorageclass) to enforce default storage class on `PersistentVolumeClaim` objects
    - [`DefaultTolerationSeconds`](/docs/reference/access-authn-authz/admission-controllers/#defaulttolerationseconds)
    - [`NodeRestriction`](/docs/reference/access-authn-authz/admission-controllers/#noderestriction) to limit what a kubelet can modify
      (e.g. only pods on this node)
 - `--kubelet-preferred-address-types` to `InternalIP,ExternalIP,Hostname;` this makes `kubectl logs` and other API server-kubelet
   communication work in environments where the hostnames of the nodes aren't resolvable
 - Flags for using certificates generated in previous steps:
    - `--client-ca-file` to `ca.crt`
    - `--tls-cert-file` to `apiserver.crt`
    - `--tls-private-key-file` to `apiserver.key`
    - `--kubelet-client-certificate` to `apiserver-kubelet-client.crt`
    - `--kubelet-client-key` to `apiserver-kubelet-client.key`
    - `--service-account-key-file` to `sa.pub`
    - `--requestheader-client-ca-file` to`front-proxy-ca.crt`
    - `--proxy-client-cert-file` to `front-proxy-client.crt`
    - `--proxy-client-key-file` to `front-proxy-client.key`
 - Other flags for securing the front proxy ([API Aggregation](/docs/concepts/extend-kubernetes/api-extension/apiserver-aggregation/)) communications:
    - `--requestheader-username-headers=X-Remote-User`
    - `--requestheader-group-headers=X-Remote-Group`
    - `--requestheader-extra-headers-prefix=X-Remote-Extra-`
    - `--requestheader-allowed-names=front-proxy-client`

#### Controller manager

The static Pod manifest for the API server is affected by following parameters provided by the users:

- If kubeadm is invoked specifying a `--pod-network-cidr`, the subnet manager feature required for some CNI network plugins is enabled by
   setting:
   - `--allocate-node-cidrs=true`
   - `--cluster-cidr` and `--node-cidr-mask-size` flags according to the given CIDR
 - If a cloud provider is specified, the corresponding `--cloud-provider` is specified, together with the  `--cloud-config` path
   if such configuration file exists (this is experimental, alpha and will be removed in a future version)

Other flags that are set unconditionally are:

 - `--controllers` enabling all the default controllers plus `BootstrapSigner` and `TokenCleaner` controllers for TLS bootstrap.
   See [TLS Bootstrapping](/docs/reference/command-line-tools-reference/kubelet-tls-bootstrapping/) for more details
 - `--use-service-account-credentials` to `true`
 - Flags for using certificates generated in previous steps:
    - `--root-ca-file` to `ca.crt`
    - `--cluster-signing-cert-file` to `ca.crt`, if External CA mode is disabled, otherwise to `""`
    - `--cluster-signing-key-file` to `ca.key`, if External CA mode is disabled, otherwise to `""`
    - `--service-account-private-key-file` to `sa.key`

#### Scheduler

The static Pod manifest for the scheduler is not affected by parameters provided by the users.

### Generate static Pod manifest for local etcd

If the user specified an external etcd this step will be skipped, otherwise kubeadm generates a static Pod manifest file for creating
a local etcd instance running in a Pod with following attributes:

- listen on `localhost:2379` and use `HostNetwork=true`
- make a `hostPath` mount out from the `dataDir` to the host's filesystem
- Any extra flags specified by the user

Please note that:

1. The etcd image will be pulled from `k8s.gcr.io` by default. See [using custom images](/docs/reference/setup-tools/kubeadm/kubeadm-init/#custom-images) for customizing the image repository
2. in case of kubeadm is executed in the `--dry-run` mode, the etcd static Pod manifest is written in a temporary folder
3. Static Pod manifest generation for local etcd can be invoked individually with the [`kubeadm init phase etcd local`](/docs/reference/setup-tools/kubeadm/kubeadm-init-phase/#cmd-phase-etcd) command

### Wait for the control plane to come up

kubeadm waits (upto 4m0s) until `localhost:6443/healthz` (kube-apiserver liveness) returns `ok`. However in order to detect
deadlock conditions, kubeadm fails fast if `localhost:10255/healthz` (kubelet liveness) or
`localhost:10255/healthz/syncloop` (kubelet readiness) don't return `ok` within 40s and 60s respectively.

kubeadm relies on the kubelet to pull the control plane images and run them properly as static Pods.
After the control plane is up, kubeadm completes the tasks described in following paragraphs.

### Save the kubeadm ClusterConfiguration in a ConfigMap for later reference

kubeadm saves the configuration passed to `kubeadm init` in a ConfigMap named `kubeadm-config` under `kube-system` namespace.

This will ensure that kubeadm actions executed in future (e.g `kubeadm upgrade`) will be able to determine the actual/current cluster
state and make new decisions based on that data.

Please note that:

1. Before saving the ClusterConfiguration, sensitive information like the token is stripped from the configuration
2. Upload of control plane node configuration can be invoked individually with the [`kubeadm init phase upload-config`](/docs/reference/setup-tools/kubeadm/kubeadm-init-phase/#cmd-phase-upload-config) command

### Mark the node as control-plane

As soon as the control plane is available, kubeadm executes following actions:

- Labels the node as control-plane with `node-role.kubernetes.io/master=""`
- Taints the node with `node-role.kubernetes.io/master:NoSchedule`

Please note that:

1. Mark control-plane phase phase can be invoked individually with the [`kubeadm init phase mark-control-plane`](/docs/reference/setup-tools/kubeadm/kubeadm-init-phase/#cmd-phase-mark-control-plane) command

### Configure TLS-Bootstrapping for node joining

Kubeadm uses [Authenticating with Bootstrap Tokens](/docs/reference/access-authn-authz/bootstrap-tokens/) for joining new nodes to an
existing cluster; for more details see also [design proposal](https://github.com/kubernetes/community/blob/master/contributors/design-proposals/cluster-lifecycle/bootstrap-discovery.md).

`kubeadm init` ensures that everything is properly configured for this process, and this includes following steps as well as
setting API server and controller flags as already described in previous paragraphs.
Please note that:

1. TLS bootstrapping for nodes can be configured with the [`kubeadm init phase bootstrap-token`](/docs/reference/setup-tools/kubeadm/kubeadm-init-phase/#cmd-phase-bootstrap-token)
   command, executing all the configuration steps described in following paragraphs; alternatively, each step can be invoked individually

#### Create a bootstrap token

`kubeadm init` create a first bootstrap token, either generated automatically or provided by the user with the `--token` flag; as documented
in bootstrap token specification, token should be saved as secrets with name `bootstrap-token-<token-id>` under `kube-system` namespace.
Please note that:

1. The default token created by `kubeadm init` will be used to validate temporary user during TLS bootstrap process; those users will
   be member of  `system:bootstrappers:kubeadm:default-node-token` group
2. The token has a limited validity, default 24 hours (the interval may be changed with the `—token-ttl` flag)
3. Additional tokens can be created with the [`kubeadm token`](/docs/reference/setup-tools/kubeadm/kubeadm-token/) command, that provide as well other useful functions
   for token management

#### Allow joining nodes to call CSR API

Kubeadm ensures that users in  `system:bootstrappers:kubeadm:default-node-token` group are able to access the certificate signing API.

This is implemented by creating a ClusterRoleBinding named `kubeadm:kubelet-bootstrap` between the group above and the default
RBAC role `system:node-bootstrapper`.

#### Setup auto approval for new bootstrap tokens

Kubeadm ensures that the Bootstrap Token will get its CSR request automatically approved by the csrapprover controller.

This is implemented by creating ClusterRoleBinding named `kubeadm:node-autoapprove-bootstrap` between
the  `system:bootstrappers:kubeadm:default-node-token` group and the default role `system:certificates.k8s.io:certificatesigningrequests:nodeclient`.

The role `system:certificates.k8s.io:certificatesigningrequests:nodeclient` should be created as well, granting
POST permission to `/apis/certificates.k8s.io/certificatesigningrequests/nodeclient`.

#### Setup nodes certificate rotation with auto approval

Kubeadm ensures that certificate rotation is enabled for nodes, and that new certificate request for nodes will get its CSR request
automatically approved by the csrapprover controller.

This is implemented by creating ClusterRoleBinding named `kubeadm:node-autoapprove-certificate-rotation` between the  `system:nodes` group
and the default role `system:certificates.k8s.io:certificatesigningrequests:selfnodeclient`.

#### Create the public cluster-info ConfigMap

This phase creates the `cluster-info` ConfigMap in the `kube-public` namespace.

Additionally it creates a Role and a RoleBinding granting access to the ConfigMap for unauthenticated users
(i.e. users in RBAC group `system:unauthenticated`).

Please note that:

1. The access to the `cluster-info` ConfigMap _is not_ rate-limited. This may or may not be a problem if you expose your cluster's API server
to the internet; worst-case scenario here is a DoS attack where an attacker uses all the in-flight requests the kube-apiserver
can handle to serving the `cluster-info` ConfigMap.

### Install addons

Kubeadm installs the internal DNS server and the kube-proxy addon components via the API server.
Please note that:

1. This phase can be invoked individually with the [`kubeadm init phase addon all`](/docs/reference/setup-tools/kubeadm/kubeadm-init-phase/#cmd-phase-addon) command.

#### proxy

A ServiceAccount for `kube-proxy` is created in the `kube-system` namespace; then kube-proxy is deployed as a DaemonSet:

- The credentials (`ca.crt` and `token`) to the control plane come from the ServiceAccount
- The location (URL) of the API server comes from a ConfigMap
- The `kube-proxy` ServiceAccount is bound to the privileges in the `system:node-proxier` ClusterRole

#### DNS

- The CoreDNS service is named `kube-dns`. This is done to prevent any interruption
  in service when the user is switching the cluster DNS from kube-dns to CoreDNS
  the `--config` method described [here](/docs/reference/setup-tools/kubeadm/kubeadm-init-phase/#cmd-phase-addon).
- A ServiceAccount for CoreDNS is created in the `kube-system` namespace.
- The `coredns` ServiceAccount is bound to the privileges in the `system:coredns` ClusterRole

In Kubernetes version 1.21, support for using `kube-dns` with kubeadm was removed.
You can use CoreDNS with kubeadm even when the related Service is named `kube-dns`.

## kubeadm join phases internal design

Similarly to `kubeadm init`, also `kubeadm join` internal workflow consists of a sequence of atomic work tasks to perform.

This is split into discovery (having the Node trust the Kubernetes Master) and TLS bootstrap (having the Kubernetes Master trust the Node).

see [Authenticating with Bootstrap Tokens](/docs/reference/access-authn-authz/bootstrap-tokens/) or the corresponding [design proposal](https://github.com/kubernetes/community/blob/master/contributors/design-proposals/cluster-lifecycle/bootstrap-discovery.md).

### Preflight checks

`kubeadm` executes a set of preflight checks before starting the join, with the aim to verify preconditions and avoid common
cluster startup problems.

Please note that:

1. `kubeadm join` preflight checks are basically a subset `kubeadm init` preflight checks
1. Starting from 1.9, kubeadm provides better support for CRI-generic functionality; in that case, docker specific controls
   are skipped or replaced by similar controls for crictl.
1. Starting from 1.9, kubeadm provides support for joining nodes running on Windows; in that case, linux specific controls are skipped.
1. In any case the user can skip specific preflight checks (or eventually all preflight checks) with the `--ignore-preflight-errors` option.

### Discovery cluster-info

There are 2 main schemes for discovery. The first is to use a shared token along with the IP address of the API server.
The second is to provide a file (that is a subset of the standard kubeconfig file).

#### Shared token discovery

If `kubeadm join` is invoked with `--discovery-token`, token discovery is used; in this case the node basically retrieves
the cluster CA certificates from the  `cluster-info` ConfigMap in the `kube-public` namespace.

In order to prevent "man in the middle" attacks, several steps are taken:

- First, the CA certificate is retrieved via insecure connection (this is possible because `kubeadm init` granted access to  `cluster-info` users for `system:unauthenticated` )
- Then the CA certificate goes trough following validation steps:
  - Basic validation: using the token ID against a JWT signature
  - Pub key validation: using provided `--discovery-token-ca-cert-hash`. This value is available in the output of `kubeadm init` or can
    be calculated using standard tools (the hash is calculated over the bytes of the Subject Public Key Info (SPKI) object as in RFC7469).
    The `--discovery-token-ca-cert-hash flag` may be repeated multiple times to allow more than one public key.
  - As a additional validation, the CA certificate is retrieved via secure connection and then compared with the CA retrieved initially

Please note that:

1.  Pub key validation can be skipped passing `--discovery-token-unsafe-skip-ca-verification` flag; This weakens the kubeadm security
    model since others can potentially impersonate the Kubernetes Master.

#### File/https discovery

If `kubeadm join` is invoked with `--discovery-file`, file discovery is used; this file can be a local file or downloaded via an HTTPS URL; in case of HTTPS, the host installed CA bundle is used to verify the connection.

With file discovery, the cluster CA certificates is provided into the file itself; in fact, the discovery file is a kubeconfig
file with only `server` and `certificate-authority-data` attributes set, as described in [`kubeadm join`](/docs/reference/setup-tools/kubeadm/kubeadm-join/#file-or-https-based-discovery) reference doc;
when the connection with the cluster is established, kubeadm try to access the `cluster-info` ConfigMap, and if available, uses it.

## TLS Bootstrap

Once the cluster info are known, the file `bootstrap-kubelet.conf` is written, thus allowing kubelet to do TLS Bootstrapping.

The TLS bootstrap mechanism uses the shared token to temporarily authenticate with the Kubernetes API server to submit a certificate
signing request (CSR) for a locally created key pair.

The request is then automatically approved and the operation completes saving `ca.crt` file and `kubelet.conf` file to be used
by kubelet for joining the cluster, while`bootstrap-kubelet.conf` is deleted.

Please note that:

- The temporary authentication is validated against the token saved during the `kubeadm init` process (or with additional tokens
  created with `kubeadm token`)
- The temporary authentication resolve to a user member of `system:bootstrappers:kubeadm:default-node-token` group which was granted
  access to CSR api during the `kubeadm init` process
- The automatic CSR approval is managed by the csrapprover controller, according with configuration done the `kubeadm init` process
