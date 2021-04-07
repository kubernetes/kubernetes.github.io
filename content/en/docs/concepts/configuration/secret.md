---
reviewers:
- mikedanese
title: Secrets
content_type: concept
feature:
  title: Secret and configuration management
  description: >
    Deploy and update secrets and application configuration without rebuilding your image and without exposing secrets in your stack configuration.
weight: 30
---

<!-- overview -->

A Secret is an object that contains a small amount of sensitive data such as
a password, a token, or a key. Such information might otherwise be put in a
{{< glossary_tooltip term_id="pod" >}} specification or in a 
{{< glossary_tooltip text="container image" term_id="image" >}}; using a
Secret means that you don't need to include confidential data in your
application code.

Because Secrets can be created independently of the Pods that use them, there
is less risk of the Secret (and its data) being exposed during the workflow of
creating, viewing, and editing Pods. Kubernetes, and applications that run in
your cluster, can also take additional precautions with Secrets, such as avoiding
writing secret data to nonvolatile storage.

Secrets are similar to {{< glossary_tooltip text="ConfigMaps" term_id="configmap" >}}
but are specifically intended to hold confidential data.

{{< caution >}}
Kubernetes Secrets are, by default, stored as unencrypted base64-encoded
strings. By default they can be retrieved - as plain text - by anyone with API
access, or anyone with access to Kubernetes' underlying data store, etcd. In
order to safely use Secrets, it is recommended you (at a minimum):

1. [Enable Encryption at Rest](/docs/tasks/administer-cluster/encrypt-data/) for Secrets.
2. [Enable or configure RBAC rules](/docs/reference/access-authn-authz/authorization/) that
   restrict reading and writing the Secret. Be aware that secrets can be obtained
   implicitly by anyone with the permission to create a Pod.

{{< /caution >}}

See [Information security for Secrets](#information-security-for-secrets) for more details.

<!-- body -->

## Uses for Secrets

There are three main ways for a Pod to use a Secret:
- As [files](#using-secrets-as-files-from-a-pod) in a
  {{< glossary_tooltip text="volume" term_id="volume" >}} mounted on one or more of
  its containers.
- As [container environment variable](#using-secrets-as-environment-variables).
- By the [kubelet when pulling images](#using-imagepullsecrets) for the Pod.

The Kubernetes control plane also uses Secrets; for example,
[bootstrap token Secrets](#bootstrap-token-secrets) are a mechanism to
help automate node registration.

### Alternatives to Secrets

Rather than using a Secret to protect confidential data, you can pick from alternatives.

Here are some of your options:

- if your cloud-native component needs to authenticate to another application that you
  know is running within the same Kubernetes cluster, you can use a
  [service account](/docs/reference/access-authn-authz/authentication/#service-account-tokens)
  and its tokens to identify your client.
- there are third party tools that you can run, either within or outside your cluster,
  that provide secrets management. For example, a service that Pods access over HTTPS,
  that reveals a secret if the client correctly authenticates (for example, with a ServiceAccount
  token).
- for authentication, you can implement a custom signer for X.509 certificates, and use
  [CertificateSigningRequests](/docs/reference/access-authn-authz/certificate-signing-requests/)
  to let that custom signer issue certificates to Pods that need them.
- you can use a [device plugin](/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/)
  to expose node-local encryption hardware to a specific Pod. For example, you can schedule
  trusted Pods onto nodes that provide a Trusted Platform Module, configured out-of-band.

You can also combine two or more of those options, including the option to use Secret objects themselves.

For example: implement (or deploy) an {{< glossary_tooltip text="operator" term_id="operator-pattern" >}}
that fetches short-lived session tokens from an external service, and then creates Secrets based
on those short-lived session tokens. Pods running in your cluster can make use of the session tokens,
and operator ensures they are valid. This separation means that you can run Pods that are unaware of
the exact mechanisms for issuing and refreshing those session tokens.

## Working with Secrets

### Creating a Secret

There are several options to create a Secret:

- [create Secret using `kubectl` command](/docs/tasks/configmap-secret/managing-secret-using-kubectl/)
- [create Secret from config file](/docs/tasks/configmap-secret/managing-secret-using-config-file/)
- [create Secret using kustomize](/docs/tasks/configmap-secret/managing-secret-using-kustomize/)

#### Constraints on Secret names and data {#restriction-names-data}

The name of a Secret object must be a valid
[DNS subdomain name](/docs/concepts/overview/working-with-objects/names#dns-subdomain-names).

You can specify the `data` and/or the `stringData` field when creating a
configuration file for a Secret.  The `data` and the `stringData` fields are optional.
The values for all keys in the `data` field have to be base64-encoded strings.
If the conversion to base64 string is not desirable, you can choose to specify
the `stringData` field instead, which accepts arbitrary strings as values.

The keys of `data` and `stringData` must consist of alphanumeric characters,
`-`, `_` or `.`. All key-value pairs in the `stringData` field are internally
merged into the `data` field. If a key appears in both the `data` and the
`stringData` field, the value specified in the `stringData` field takes
precedence.

#### Size limit {#restriction-data-size}

Individual secrets are limited to 1MiB in size. This is to discourage creation
of very large secrets that could exhaust the API server and kubelet memory.
However, creation of many smaller secrets could also exhaust memory. You can
use a [resource quota](/docs/concepts/policy/resource-quotas/) to limit the
number of Secrets (or other resources) in a namespace.

### Editing a Secret

You can edit an existing Secret using kubectl:

```shell
kubectl edit secrets mysecret
```

This opens your default editor and allows you to update the base64 encoded Secret
values in the `data` field; for example:

```yaml
# Please edit the object below. Lines beginning with a '#' will be ignored,
# and an empty file will abort the edit. If an error occurs while saving this file will be
# reopened with the relevant failures.
#
apiVersion: v1
data:
  username: YWRtaW4=
  password: MWYyZDFlMmU2N2Rm
kind: Secret
metadata:
  annotations:
    kubectl.kubernetes.io/last-applied-configuration: { ... }
  creationTimestamp: 2020-01-22T18:41:56Z
  name: mysecret
  namespace: default
  resourceVersion: "164619"
  uid: cfee02d6-c137-11e5-8d73-42010af00002
type: Opaque
```

That example manifest defines a Secret with two keys in the `data` field: `username` and `password`.
The values are Base64 strings in the manifest; however, when you use the Secret with a Pod
then the kubelet provides the _decoded_ data to the Pod and its containers.

You can package many keys and values into one Secret, or use many Secrets, whichever is convenient.

### Using a Secret

Secrets can be mounted as data volumes or exposed as
{{< glossary_tooltip text="environment variables" term_id="container-env-variables" >}}
to be used by a container in a Pod. Secrets can also be used by other parts of the
system, without being directly exposed to the Pod. For example, Secrets can hold
credentials that other parts of the system should use to interact with external
systems on your behalf.

Secret volume sources are validated to ensure that the specified object
reference actually points to an object of type Secret. Therefore, a Secret
needs to be created before any Pods that depend on it.  

If the Secret cannot be fetched (perhaps because it does not exist, or
due to a temporary lack of connection to the API server) the kubelet
periodically retries running that Pod. The kubelet also reports an Event
for that Pod, including details of the problem fetching the Secret.

#### Optional Secrets {#restriction-secret-must-exist}

When you define a container environment variable based on a Secret,
you can mark it as _optional_. The default is for the Secret to be
required.

None of a Pod's containers will start until all non-optional Secrets are
available.

If a Pod references a specific key in a Secret and that Secret does exist, but
is missing the named key, the Pod fails during startup.

### Using Secrets as files from a Pod

To consume a Secret in a volume in a Pod:

1. Create a secret or use an existing one. Multiple Pods can reference the same secret.
1. Modify your Pod definition to add a volume under `.spec.volumes[]`. Name the volume anything, and have a `.spec.volumes[].secret.secretName` field equal to the name of the Secret object.
1. Add a `.spec.containers[].volumeMounts[]` to each container that needs the secret. Specify `.spec.containers[].volumeMounts[].readOnly = true` and `.spec.containers[].volumeMounts[].mountPath` to an unused directory name where you would like the secrets to appear.
1. Modify your image or command line so that the program looks for files in that directory. Each key in the secret `data` map becomes the filename under `mountPath`.

This is an example of a Pod that mounts a Secret named `mysecret` in a volume:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: mypod
spec:
  containers:
  - name: mypod
    image: redis
    volumeMounts:
    - name: foo
      mountPath: "/etc/foo"
      readOnly: true
  volumes:
  - name: foo
    secret:
      secretName: mysecret
      optional: false # default setting; "mysecret" must exist
```

Each Secret you want to use needs to be referred to in `.spec.volumes`.

If there are multiple containers in the Pod, then each container needs its
own `volumeMounts` block, but only one `.spec.volumes` is needed per Secret.

{{< note >}}
Secret volume sources are validated to ensure that the specified object
reference actually points to an object of type Secret. Therefore, a secret
needs to be created before any Pods that depend on it.
{{< /note >}}

#### Projection of Secret keys to specific paths

You can also control the paths within the volume where Secret keys are projected.
You can use the `.spec.volumes[].secret.items` field to change the target path of each key:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: mypod
spec:
  containers:
  - name: mypod
    image: redis
    volumeMounts:
    - name: foo
      mountPath: "/etc/foo"
      readOnly: true
  volumes:
  - name: foo
    secret:
      secretName: mysecret
      items:
      - key: username
        path: my-group/my-username
```

What will happen:

* the `username` key from `mysecret` is available to the container at the path
  `/etc/foo/my-group/my-username` instead of at `/etc/foo/username`.
* the `password` key from that Secret object is not projected.

If `.spec.volumes[].secret.items` is used, only keys specified in `items` are projected.
To consume all keys from the Secret, all of them must be listed in the `items` field.

If you list keys explicitly, then all listed keys must exist in the corresponding Secret.
Otherwise, the volume is not created.

#### Secret files permissions

You can set the POSIX file access permission bits for a single Secret key.
If you don't specify any permissions, `0644` is used by default.
You can also set a default mode for the entire Secret volume and override per key if needed.

For example, you can specify a default mode like this:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: mypod
spec:
  containers:
  - name: mypod
    image: redis
    volumeMounts:
    - name: foo
      mountPath: "/etc/foo"
  volumes:
  - name: foo
    secret:
      secretName: mysecret
      defaultMode: 0400
```

The secret is mounted on `/etc/foo`; all the files created by the
secret volume mount have permission `0400`.


{{< note >}}
If you're defining a Pod or a Pod template using JSON, beware that the JSON
specification doesn't support octal notation. You can use the decimal value
for the `defaultMode` (for example, 0400 in octal is 256 in decimal) instead.  
If you're writing YAML, you can write the `defaultMode` in octal.
{{< /note >}}

#### Consuming Secret values from volumes

Inside the container that mounts a secret volume, the secret keys appear as
files. The secret values are base64 decoded and stored inside these files.

This is the result of commands executed inside the container from the example above:

```shell
ls /etc/foo/
```

The output is similar to:

```
username
password
```

```shell
cat /etc/foo/username
```

The output is similar to:

```
admin
```

```shell
cat /etc/foo/password
```

The output is similar to:

```
1f2d1e2e67df
```

The program in a container is responsible for reading the secret data from these
files, as needed.

#### Mounted Secrets are updated automatically

When a volume contains data from a Secret, and that Secret is updated, Kubernetes tracks
this and updates the data in the volume, using an eventually-consistent approach.

{{< note >}}
A container using a Secret as a
[subPath](/docs/concepts/storage/volumes#using-subpath) volume mount does not receive
automated Secret updates.
{{< /note >}}

The kubelet keeps a cache of the current keys and values for the Secrets that are used in
volumes for pods on that node.
You can configure the way that the kubelet detects changes from the cached values. The `configMapAndSecretChangeDetectionStrategy` field in
the [kubelet configuration](/docs/reference/config-api/kubelet-config.v1beta1/) controls which strategy the kubelet uses. The default strategy is `Watch`.

Updates to Secrets can be either propagated by an API watch mechanism (the default), based on
a cache with a defined time-to-live, or polled from the cluster API server on each kubelet
synchronisation loop.

As a result, the total delay from the moment when the Secret is updated to the moment
when new keys are projected to the Pod can be as long as the kubelet sync period + cache
propagation delay, where the cache propagation delay depends on the chosen cache type
(following the same order listed in the previous paragraph, these are:
watch propagation delay, the configured cache TTL, or zero for direct polling).

### Using Secrets as environment variables

To use a Secret in an {{< glossary_tooltip text="environment variable" term_id="container-env-variables" >}}
in a Pod:

1. Create a Secret (or use an existing one).  Multiple Pods can reference the same Secret.
1. Modify your Pod definition in each container that you wish to consume the value of a secret
   key to add an environment variable for each secret key you wish to consume. The environment
   variable that consumes the secret key should populate the secret's name and key in `env[].valueFrom.secretKeyRef`.
1. Modify your image and/or command line so that the program looks for values in the specified
   environment variables.

This is an example of a Pod that uses a Secret via environment variables:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secret-env-pod
spec:
  containers:
  - name: mycontainer
    image: redis
    env:
      - name: SECRET_USERNAME
        valueFrom:
          secretKeyRef:
            name: mysecret
            key: username
            optional: false # same as default; "mysecret" must exist
                            # and include a key named "username"
      - name: SECRET_PASSWORD
        valueFrom:
          secretKeyRef:
            name: mysecret
            key: password
            optional: false # same as default; "mysecret" must exist
                            # and include a key named "password"
  restartPolicy: Never
```


#### Invalid environment variables {#restriction-env-from-invalid}

Secrets used to populate environment variables by the `envFrom` field that have keys
that are considered invalid environment variable names will have those keys
skipped. The Pod is allowed to start.

If you define a Pod with an invalid variable name, the failed Pod startup includes
an event with the reason set to `InvalidVariableNames` and a message that lists the
skipped invalid keys. The following example shows a Pod that refers to a Secret
named `mysecret`, where `mysecret` contains 2 invalid keys: `1badkey` and `2alsobad`.

```shell
kubectl get events
```

The output is similar to:

```
LASTSEEN   FIRSTSEEN   COUNT     NAME            KIND      SUBOBJECT                         TYPE      REASON
0s         0s          1         dapi-test-pod   Pod                                         Warning   InvalidEnvironmentVariableNames   kubelet, 127.0.0.1      Keys [1badkey, 2alsobad] from the EnvFrom secret default/mysecret were skipped since they are considered invalid environment variable names.
```


#### Consuming Secret values from environment variables

Inside a container that consumes a Secret using environment variables, the secret keys appear
as normal environment variables. The values of those variables are the base64 decoded values
of the secret data.

This is the result of commands executed inside the container from the example above:

```shell
echo "$SECRET_USERNAME"
```

The output is similar to:

```
admin
```

```shell
echo "$SECRET_PASSWORD"
```

The output is similar to:

```
1f2d1e2e67df
```

{{< note >}}
If a container already consumes a Secret in an environment variable,
a Secret update will not be seen by the container unless it is
restarted. There are third party solutions for triggering restarts when
secrets change.
{{< /note >}}

### Container image pull secrets {#using-imagepullsecrets}

If you want to fetch container images from a private repository, you need a way for
the kubelet on each node to authenticate to that repository. You can configure
_image pull secrets_ to make this possible. These secrets are configured at the Pod
level.

The `imagePullSecrets` field for a Pod is a list of references to Secrets in the same namespace
as the Pod.
You can use an `imagePullSecrets` to pass image registry access crendentials to
the kubelet. The kubelet uses this information to pull a private image on behalf of your Pod.
See the [PodSpec API](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#podspec-v1-core)
for more information about the `imagePullSecrets` field.

##### Manually specifying an imagePullSecret

You can learn how to specify `imagePullSecrets` from the [container images documentation](/docs/concepts/containers/images/#specifying-imagepullsecrets-on-a-pod).

##### Arranging for imagePullSecrets to be automatically attached

Pods inherit `imagePullSecrets` from their ServiceAccount if none are
explicitly configured.

You can define `imagePullSecrets` for a ServiceAccount
in a Namespace. Once you do this, creating a new Pod that uses the ServiceAccount
with `imagePullSecrets` defined means that the new Pod inherits the `imagePullSecrets`.
from the Pod's ServiceAccount.  
See [Add ImagePullSecrets to a service account](/docs/tasks/configure-pod-container/configure-service-account/#add-imagepullsecrets-to-a-service-account)
 for a detailed explanation of that process.


### Using Secrets with static Pods {#restriction-static-pod}

You cannot use ConfigMaps or Secrets with
{{< glossary_tooltip text="static Pods" term_id="static-pod" >}}.

## Use cases

### Use case: As container environment variables

Create a secret
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: mysecret
type: Opaque
data:
  USER_NAME: YWRtaW4=
  PASSWORD: MWYyZDFlMmU2N2Rm
```

Create the Secret:
```shell
kubectl apply -f mysecret.yaml
```

Use `envFrom` to define all of the Secret's data as container environment variables. The key from the Secret becomes the environment variable name in the Pod.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secret-test-pod
spec:
  containers:
    - name: test-container
      image: k8s.gcr.io/busybox
      command: [ "/bin/sh", "-c", "env" ]
      envFrom:
      - secretRef:
          name: mysecret
  restartPolicy: Never
```

### Use case: Pod with SSH keys

Create a Secret containing some SSH keys:

```shell
kubectl create secret generic ssh-key-secret --from-file=ssh-privatekey=/path/to/.ssh/id_rsa --from-file=ssh-publickey=/path/to/.ssh/id_rsa.pub
```

The output is similar to:

```
secret "ssh-key-secret" created
```

You can also create a `kustomization.yaml` with a `secretGenerator` field containing ssh keys.

{{< caution >}}
Think carefully before sending your own SSH keys: other users of the cluster may have access
to the Secret.

You could instead create an SSH private key representing a service identity that you want to be
accessible to all the users with whom you share the Kubernetes cluster, and that you can revoke
if the credentials are compromised.
{{< /caution >}}

Now you can create a Pod which references the secret with the SSH key and
consumes it in a volume:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secret-test-pod
  labels:
    name: secret-test
spec:
  volumes:
  - name: secret-volume
    secret:
      secretName: ssh-key-secret
  containers:
  - name: ssh-test-container
    image: mySshImage
    volumeMounts:
    - name: secret-volume
      readOnly: true
      mountPath: "/etc/secret-volume"
```

When the container's command runs, the pieces of the key will be available in:

```
/etc/secret-volume/ssh-publickey
/etc/secret-volume/ssh-privatekey
```

The container is then free to use the secret data to establish an SSH connection.

### Use case: Pods with prod / test credentials

This example illustrates a Pod which consumes a secret containing production
credentials and another Pod which consumes a secret with test environment
credentials.

You can create a `kustomization.yaml` with a `secretGenerator` field or run
`kubectl create secret`.

```shell
kubectl create secret generic prod-db-secret --from-literal=username=produser --from-literal=password=Y4nys7f11
```

The output is similar to:

```
secret "prod-db-secret" created
```

You can also create a secret for test environment credentials.

```shell
kubectl create secret generic test-db-secret --from-literal=username=testuser --from-literal=password=iluvtests
```

The output is similar to:

```
secret "test-db-secret" created
```

{{< note >}}
Special characters such as `$`, `\`, `*`, `=`, and `!` will be interpreted by your [shell](https://en.wikipedia.org/wiki/Shell_(computing)) and require escaping.

In most shells, the easiest way to escape the password is to surround it with single quotes (`'`).
For example, if your actual password is `S!B\*d$zDsb=`, you should execute the command this way:

```shell
kubectl create secret generic dev-db-secret --from-literal=username=devuser --from-literal=password='S!B\*d$zDsb='
```

You do not need to escape special characters in passwords from files (`--from-file`).
{{< /note >}}

Now make the Pods:

```shell
cat <<EOF > pod.yaml
apiVersion: v1
kind: List
items:
- kind: Pod
  apiVersion: v1
  metadata:
    name: prod-db-client-pod
    labels:
      name: prod-db-client
  spec:
    volumes:
    - name: secret-volume
      secret:
        secretName: prod-db-secret
    containers:
    - name: db-client-container
      image: myClientImage
      volumeMounts:
      - name: secret-volume
        readOnly: true
        mountPath: "/etc/secret-volume"
- kind: Pod
  apiVersion: v1
  metadata:
    name: test-db-client-pod
    labels:
      name: test-db-client
  spec:
    volumes:
    - name: secret-volume
      secret:
        secretName: test-db-secret
    containers:
    - name: db-client-container
      image: myClientImage
      volumeMounts:
      - name: secret-volume
        readOnly: true
        mountPath: "/etc/secret-volume"
EOF
```

Add the pods to the same `kustomization.yaml`:

```shell
cat <<EOF >> kustomization.yaml
resources:
- pod.yaml
EOF
```

Apply all those objects on the API server by running:

```shell
kubectl apply -k .
```

Both containers will have the following files present on their filesystems with the values
for each container's environment:

```
/etc/secret-volume/username
/etc/secret-volume/password
```

Note how the specs for the two Pods differ only in one field; this facilitates
creating Pods with different capabilities from a common Pod template.

You could further simplify the base Pod specification by using two service accounts:

1. `prod-user` with the `prod-db-secret`
1. `test-user` with the `test-db-secret`

The Pod specification is shortened to:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: prod-db-client-pod
  labels:
    name: prod-db-client
spec:
  serviceAccount: prod-db-client
  containers:
  - name: db-client-container
    image: myClientImage
```

### Use case: dotfiles in a secret volume

You can make your data "hidden" by defining a key that begins with a dot.
This key represents a dotfile or "hidden" file. For example, when the following secret
is mounted into a volume, `secret-volume`:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: dotfile-secret
data:
  .secret-file: dmFsdWUtMg0KDQo=
---
apiVersion: v1
kind: Pod
metadata:
  name: secret-dotfiles-pod
spec:
  volumes:
  - name: secret-volume
    secret:
      secretName: dotfile-secret
  containers:
  - name: dotfile-test-container
    image: k8s.gcr.io/busybox
    command:
    - ls
    - "-l"
    - "/etc/secret-volume"
    volumeMounts:
    - name: secret-volume
      readOnly: true
      mountPath: "/etc/secret-volume"
```

The volume will contain a single file, called `.secret-file`, and
the `dotfile-test-container` will have this file present at the path
`/etc/secret-volume/.secret-file`.

{{< note >}}
Files beginning with dot characters are hidden from the output of  `ls -l`;
you must use `ls -la` to see them when listing directory contents.
{{< /note >}}

### Use case: Secret visible to one container in a Pod

Consider a program that needs to handle HTTP requests, do some complex business
logic, and then sign some messages with an HMAC. Because it has complex
application logic, there might be an unnoticed remote file reading exploit in
the server, which could expose the private key to an attacker.

This could be divided into two processes in two containers: a frontend container
which handles user interaction and business logic, but which cannot see the
private key; and a signer container that can see the private key, and responds
to simple signing requests from the frontend (for example, over localhost networking).

With this partitioned approach, an attacker now has to trick the application
server into doing something rather arbitrary, which may be harder than getting
it to read a file.

<!-- TODO: explain how to do this while still using automation. -->

## Types of Secret {#secret-types}

When creating a Secret, you can specify its type using the `type` field of
the [`Secret`](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#secret-v1-core)
resource, or certain equivalent `kubectl` command line flags (if available).
The Secret type is used to facilitate programmatic handling of the Secret data.

Kubernetes provides several built-in types for some common usage scenarios.
These types vary in terms of the validations performed and the constraints
Kubernetes imposes on them.

| Built-in Type | Usage |
|--------------|-------|
| `Opaque`     |  arbitrary user-defined data |
| `kubernetes.io/service-account-token` | ServiceAccount token |
| `kubernetes.io/dockercfg` | serialized `~/.dockercfg` file |
| `kubernetes.io/dockerconfigjson` | serialized `~/.docker/config.json` file |
| `kubernetes.io/basic-auth` | credentials for basic authentication |
| `kubernetes.io/ssh-auth` | credentials for SSH authentication |
| `kubernetes.io/tls` | data for a TLS client or server |
| `bootstrap.kubernetes.io/token` | bootstrap token data |

You can define and use your own Secret type by assigning a non-empty string as the
`type` value for a Secret object. An empty string is treated as an `Opaque` type.
Kubernetes doesn't impose any constraints on the type name. However, if you
are using one of the built-in types, you must meet all the requirements defined
for that type.

### Opaque secrets

`Opaque` is the default Secret type if omitted from a Secret configuration file.
When you create a Secret using `kubectl`, you will use the `generic`
subcommand to indicate an `Opaque` Secret type. For example, the following
command creates an empty Secret of type `Opaque`.

```shell
kubectl create secret generic empty-secret
kubectl get secret empty-secret
```

The output looks like:

```
NAME           TYPE     DATA   AGE
empty-secret   Opaque   0      2m6s
```

The `DATA` column shows the number of data items stored in the Secret.
In this case, `0` means you have created an empty Secret.

### Service account token Secrets

A `kubernetes.io/service-account-token` type of Secret is used to store a
token that identifies a
{{< glossary_tooltip text="service account" term_id="service-account" >}}.
When using this Secret type, you need to ensure that the
`kubernetes.io/service-account.name` annotation is set to an existing
service account name. A Kubernetes
{{< glossary_tooltip text="controller" term_id="controller" >}} fills in some
other fields such as the `kubernetes.io/service-account.uid` annotation, and the
`token` key in the `data` field, which is set to contain an authentication
token.

The following example configuration declares a service account token Secret:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: secret-sa-sample
  annotations:
    kubernetes.io/service-account.name: "sa-name"
type: kubernetes.io/service-account-token
data:
  # You can include additional key value pairs as you do with Opaque Secrets
  extra: YmFyCg==
```

When creating a `Pod`, Kubernetes automatically finds or creates a service account
Secret and then automatically modifies your Pod to use this Secret. The service account
token Secret contains credentials for accessing the Kubernetes API.

The automatic creation and use of API credentials can be disabled or
overridden if desired. However, if all you need to do is securely access the
API server, this is the recommended workflow.

See the [ServiceAccount](/docs/tasks/configure-pod-container/configure-service-account/)
documentation for more information on how service accounts work.  
You can also check the `automountServiceAccountToken` field and the
`serviceAccountName` field of the
[`Pod`](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#pod-v1-core)
for information on referencing service account from Pods.

### Docker config Secrets

You can use one of the following `type` values to create a Secret to
store the credentials for accessing a Docker registry for images.

- `kubernetes.io/dockercfg`
- `kubernetes.io/dockerconfigjson`

The `kubernetes.io/dockercfg` type is reserved to store a serialized
`~/.dockercfg` which is the legacy format for configuring Docker command line.
When using this Secret type, you have to ensure the Secret `data` field
contains a `.dockercfg` key whose value is content of a `~/.dockercfg` file
encoded in the base64 format.

The `kubernetes.io/dockerconfigjson` type is designed for storing a serialized
JSON that follows the same format rules as the `~/.docker/config.json` file
which is a new format for `~/.dockercfg`.
When using this Secret type, the `data` field of the Secret object must
contain a `.dockerconfigjson` key, in which the content for the
`~/.docker/config.json` file is provided as a base64 encoded string.

Below is an example for a `kubernetes.io/dockercfg` type of Secret:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: secret-dockercfg
type: kubernetes.io/dockercfg
data:
  .dockercfg: |
    "<base64 encoded ~/.dockercfg file>"
```

{{< note >}}
If you do not want to perform the base64 encoding, you can choose to use the
`stringData` field instead.
{{< /note >}}

When you create these types of Secrets using a manifest, the API
server checks whether the expected key does exists in the `data` field, and
it verifies if the value provided can be parsed as a valid JSON. The API
server doesn't validate if the JSON actually is a Docker config file.

When you do not have a Docker config file, or you want to use `kubectl`
to create a Docker registry Secret, you can do:

```shell
kubectl create secret docker-registry secret-tiger-docker \
  --docker-username=tiger \
  --docker-password=pass113 \
  --docker-email=tiger@acme.com
```

This command creates a Secret of type `kubernetes.io/dockerconfigjson`.
If you dump the `.dockerconfigjson` content from the `data` field, you will
get the following JSON content which is a valid Docker configuration created
on the fly:

```json
{
  "auths": {
    "https://index.docker.io/v1/": {
      "username": "tiger",
      "password": "pass113",
      "email": "tiger@acme.com",
      "auth": "dGlnZXI6cGFzczExMw=="
    }
  }
}
```

### Basic authentication Secret

The `kubernetes.io/basic-auth` type is provided for storing credentials needed
for basic authentication. When using this Secret type, the `data` field of the
Secret must contain the following two keys:

- `username`: the user name for authentication;
- `password`: the password or token for authentication.

Both values for the above two keys are base64 encoded strings. You can, of
course, provide the clear text content using the `stringData` for Secret
creation.

The following YAML is an example config for a basic authentication Secret:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: secret-basic-auth
type: kubernetes.io/basic-auth
stringData:
  username: admin
  password: t0p-Secret
```

The basic authentication Secret type is provided only for user's convenience.
You can create an `Opaque` for credentials used for basic authentication.
However, using the builtin Secret type helps unify the formats of your credentials
and the API server does verify if the required keys are provided in a Secret
configuration.

### SSH authentication secrets

The builtin type `kubernetes.io/ssh-auth` is provided for storing data used in
SSH authentication. When using this Secret type, you will have to specify a
`ssh-privatekey` key-value pair in the `data` (or `stringData`) field
as the SSH credential to use.

The following YAML is an example config for a SSH authentication Secret:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: secret-ssh-auth
type: kubernetes.io/ssh-auth
data:
  # the data is abbreviated in this example
  ssh-privatekey: |
     MIIEpQIBAAKCAQEAulqb/Y ...
```

The SSH authentication Secret type is provided only for user's convenience.
You can create an `Opaque` for credentials used for SSH authentication.
However, using the builtin Secret type helps unify the formats of your credentials
and the API server does verify if the required keys are provided in a Secret
configuration.

{{< caution >}}
SSH private keys do not establish trusted communication between an SSH client and
host server on their own. A secondary means of establishing trust is needed to
mitigate "man in the middle" attacks, such as a `known_hosts` file added to a
ConfigMap.
{{< /caution >}}

### TLS secrets

Kubernetes provides a builtin Secret type `kubernetes.io/tls` for storing
a certificate and its associated key that are typically used for TLS . This
data is primarily used with TLS termination of the Ingress resource, but may
be used with other resources or directly by a workload.
When using this type of Secret, the `tls.key` and the `tls.crt` key must be provided
in the `data` (or `stringData`) field of the Secret configuration, although the API
server doesn't actually validate the values for each key.

The following YAML contains an example config for a TLS Secret:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: secret-tls
type: kubernetes.io/tls
data:
  # the data is abbreviated in this example
  tls.crt: |
    MIIC2DCCAcCgAwIBAgIBATANBgkqh ...
  tls.key: |
    MIIEpgIBAAKCAQEA7yn3bRHQ5FHMQ ...
```

The TLS Secret type is provided for user's convenience. You can create an `Opaque`
for credentials used for TLS server and/or client. However, using the builtin Secret
type helps ensure the consistency of Secret format in your project; the API server
does verify if the required keys are provided in a Secret configuration.

When creating a TLS Secret using `kubectl`, you can use the `tls` subcommand
as shown in the following example:

```shell
kubectl create secret tls my-tls-secret \
  --cert=path/to/cert/file \
  --key=path/to/key/file
```

The public/private key pair must exist before hand. The public key certificate
for `--cert` must be .PEM encoded (Base64-encoded DER format), and match the
given private key for `--key`.
The private key must be in what is commonly called PEM private key format,
unencrypted. In both cases, the initial and the last lines from PEM (for
example, `--------BEGIN CERTIFICATE-----` and `-------END CERTIFICATE----` for
a cetificate) are *not* included.

### Bootstrap token Secrets

A bootstrap token Secret can be created by explicitly specifying the Secret
`type` to `bootstrap.kubernetes.io/token`. This type of Secret is designed for
tokens used during the node bootstrap process. It stores tokens used to sign
well known ConfigMaps.

A bootstrap token Secret is usually created in the `kube-system` namespace and
named in the form `bootstrap-token-<token-id>` where `<token-id>` is a 6 character
string of the token ID.

As a Kubernetes manifest, a bootstrap token Secret might look like the
following:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: bootstrap-token-5emitj
  namespace: kube-system
type: bootstrap.kubernetes.io/token
data:
  auth-extra-groups: c3lzdGVtOmJvb3RzdHJhcHBlcnM6a3ViZWFkbTpkZWZhdWx0LW5vZGUtdG9rZW4=
  expiration: MjAyMC0wOS0xM1QwNDozOToxMFo=
  token-id: NWVtaXRq
  token-secret: a3E0Z2lodnN6emduMXAwcg==
  usage-bootstrap-authentication: dHJ1ZQ==
  usage-bootstrap-signing: dHJ1ZQ==
```

A bootstrap type Secret has the following keys specified under `data`:

- `token-id`: A random 6 character string as the token identifier. Required.
- `token-secret`: A random 16 character string as the actual token secret. Required.
- `description`: A human-readable string that describes what the token is
  used for. Optional.
- `expiration`: An absolute UTC time using RFC3339 specifying when the token
  should be expired. Optional.
- `usage-bootstrap-<usage>`: A boolean flag indicating additional usage for
  the bootstrap token.
- `auth-extra-groups`: A comma-separated list of group names that will be
  authenticated as in addition to the `system:bootstrappers` group.

The above YAML may look confusing because the values are all in base64 encoded
strings. In fact, you can create an identical Secret using the following YAML:

```yaml
apiVersion: v1
kind: Secret
metadata:
  # Note how the Secret is named
  name: bootstrap-token-5emitj
  # A bootstrap token Secret usually resides in the kube-system namespace
  namespace: kube-system
type: bootstrap.kubernetes.io/token
stringData:
  auth-extra-groups: "system:bootstrappers:kubeadm:default-node-token"
  expiration: "2020-09-13T04:39:10Z"
  # This token ID is used in the name
  token-id: "5emitj"
  token-secret: "kq4gihvszzgn1p0r"
  # This token can be used for authentication
  usage-bootstrap-authentication: "true"
  # and it can be used for signing
  usage-bootstrap-signing: "true"
```


## Immutable Secrets {#secret-immutable}

{{< feature-state for_k8s_version="v1.19" state="beta" >}}

The Kubernetes beta feature _Immutable Secrets and ConfigMaps_ provides an option to set
individual Secrets and ConfigMaps as immutable. For clusters that extensively use Secrets
(at least tens of thousands of unique Secret to Pod mounts), preventing changes to their
data has the following advantages:

- protects you from accidental (or unwanted) updates that could cause applications outages
- improves performance of your cluster by significantly reducing load on the kube-apiserver,
by closing watches for secrets marked as immutable.

This feature is controlled by the `ImmutableEphemeralVolumes` [feature
gate](/docs/reference/command-line-tools-reference/feature-gates/),
which is enabled by default since v1.19.

You can create an immutable Secret by setting the `immutable` field to `true`. For example:
```yaml
apiVersion: v1
kind: Secret
metadata:
  ...
data:
  ...
immutable: true
```

{{< note >}}
Once a Secret or ConfigMap is marked as immutable, it is _not_ possible to revert this change
nor to mutate the contents of the `data` field. You can only delete and recreate the Secret.  
Existing Pods maintain a mount point that refers to the deleted Secret - it is recommended to
recreate these pods.
{{< /note >}}


## Information security for Secrets

Although ConfigMap and Secret work similarly, Kubernetes applies some additional
protection for Secret objects.

Secrets often hold values that span a spectrum of importance, many of which can
cause escalations within Kubernetes (e.g. service account tokens) and to
external systems. Even if an individual app can reason about the power of the
Secrets it expects to interact with, other apps within the same namespace can
render those assumptions invalid.

A Secret is only sent to a node if a Pod on that node requires it.
For mounting secrets into Pods, the kubelet stores a copy of the data into a `tmpfs`
so that the confidential data is not written to durable storage.
Once the Pod that depends on the Secret is deleted, the kubelet deletes its local copy
of the confidential data from the Secret.

There may be several containers in a Pod. By default, containers you define
only have access to the default ServiceAccount and its related Secret.
You must explicitly define environment variables or map a volume into a
container in order to provide access to any other Secret.

There may be Secrets for several Pods on the same node. However, only the
Secrets that a Pod requests are potentially visible within its containers.
Therefore, one Pod does not have access to the Secrets of another Pod.

{{< warning >}}
Any privileged containers on a node are liable to have access to all Secrets used
on that node.
{{< /warning >}}


### Security recommendations for developers

- Applications still need to protect the value of confidential information after reading it
  from an environment variable or volume. For example, your application must avoid logging
  the secret data in the clear or transmitting it to an untrusted party.
- If you are defining multiple containers in a Pod, and only one of those
  containers needs access to a Secret, define the volume mount or environment
  variable configuration so that the other containers do not have access to that
  Secret.
- If you configure a Secret through a {{< glossary_tooltip text="manifest" term_id="manifest" >}},
  with the secret data encoded as base64, sharing this file or checking it in to a
  source repository means the secret is available to everyone who can read the manifest.
  Base64 encoding is _not_ an encryption method, it provides no additional confidentiality
  over plain text.
- When deploying applications that interact with the Secret API, you should
  limit access using
  [authorization policies](/docs/reference/access-authn-authz/authorization/) such as
  [RBAC]( /docs/reference/access-authn-authz/rbac/).
- In the Kubernetes API, `watch` and `list` requests for Secrets within a namespace
  are extremely powerful capabilities. Avoid granting this access where feasible, since
  listing Secrets allows the clients to inspect the values of every Secret in that
  namespace.

### Security recommendations for cluster administrators

{{< caution >}}
A user who can create a Pod that uses a Secret can also see the value of that Secret. Even
if cluster policies do not allow a user to read the Secret directly, the same user could
have access to run a Pod that then exposes the Secret.
{{< /caution >}}

- Reserve the ability to `watch` or `list` all secrets in a cluster (using the Kubernetes
  API), so that only the most privileged, system-level components can perform this action.
- When deploying applications that interact with the Secret API, you should
  limit access using
  [authorization policies](/docs/reference/access-authn-authz/authorization/) such as
  [RBAC]( /docs/reference/access-authn-authz/rbac/).
- In the API server, objects (including Secrets) are persisted into
  {{< glossary_tooltip term_id="etcd" >}}; therefore:
  - only allow cluster admistrators to access etcd (this includes read-only access);
  - enable [encryption at rest](/docs/tasks/administer-cluster/encrypt-data/)
    for Secret objects, so that the data of these Secrets are not stored in the clear
    into {{< glossary_tooltip term_id="etcd" >}};
  - consider wiping / shredding the durable storage used by etcd once it is
    no longer in use;
  - if there are multiple etcd instances, make sure that etcd is
    using SSL/TLS for communication between etcd peers.

## {{% heading "whatsnext" %}}

- Learn how to [manage Secrets using `kubectl`](/docs/tasks/configmap-secret/managing-secret-using-kubectl/)
- Learn how to [manage Secrets using config file](/docs/tasks/configmap-secret/managing-secret-using-config-file/)
- Learn how to [manage Secrets using kustomize](/docs/tasks/configmap-secret/managing-secret-using-kustomize/)
- Refer to the [Secret design document](https://git.k8s.io/community/contributors/design-proposals/auth/secrets.md) to understand the original context for this feature.
