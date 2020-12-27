---
title: Configure a Pod to Use a ConfigMap
content_type: task
weight: 150
card:
  name: tasks
  weight: 50
---

<!-- overview -->
{{< glossary_tooltip text="ConfigMaps" term_id="configmap" >}} allow you to decouple
configuration data from container image artifacts to keep containerized applications
portable. This page provides a series of usage examples demonstrating how to create
`ConfigMap`s and configure `Pod`s using data stored in `ConfigMap`s.


## {{% heading "prerequisites" %}}


{{< include "task-tutorial-prereqs.md" >}}


<!-- steps -->


## Creating ConfigMaps {#create-a-configmap}
To create a `ConfigMap`, you can use `kubectl create configmap`, or a `ConfigMap`
resource generator in `kustomization.yaml`.

### Create a ConfigMap using `kubectl create` {#create-a-configmap-using-kubectl-create-configmap} 
Use the `kubectl create configmap` command to create `ConfigMap`s
from [directories](#create-configmaps-from-directories),
[files](#create-configmaps-from-files), or
[literal values](#create-configmaps-from-literal-values):

```shell
kubectl create configmap <map-name> <data-source>
```

where \<map-name> is the name you want to assign to the `ConfigMap`, and
\<data-source> is the directory, file, or literal value to draw the data from.
The name of a `ConfigMap` object must be a valid
[DNS subdomain name](/docs/concepts/overview/working-with-objects/names#dns-subdomain-names).

When you are creating a `ConfigMap` based on a file, the key in the \<data-source>
defaults to the basename of the file, and the value defaults to the file content.

You can use
[`kubectl describe`](/docs/reference/generated/kubectl/kubectl-commands/#describe) or
[`kubectl get`](/docs/reference/generated/kubectl/kubectl-commands/#get) to retrieve
information about a `ConfigMap`.

### Create a ConfigMap from a directory {#create-configmaps-from-directories}

You can use `kubectl create configmap` to create a `ConfigMap` from multiple files in
the same directory. When you are creating a `ConfigMap` based on a directory, the
`kubectl` tool identifies files whose basename is a valid key in the directory,
then packages each of those input files into the new `ConfigMap`.
Each input must be a regular file; the `kubectl` tool ignores paths that refer to any
other kind of item (such as symbolic links, directories, devices, or pipes).

For example:

```shell
# Create a local directory
mkdir -p configure-pod-container/configmap/

# Download some sample files into the directory "configure-pod-container/configmap/"
wget https://kubernetes.io/examples/configmap/game.properties -O configure-pod-container/configmap/game.properties
wget https://kubernetes.io/examples/configmap/ui.properties -O configure-pod-container/configmap/ui.properties

# Create the ConfigMap
kubectl create configmap game-config --from-file=configure-pod-container/configmap/
```

The above command packages each file, in this case, `game.properties` and `ui.properties`
in the `configure-pod-container/configmap/` directory into the _game-config_ `ConfigMap`.
You can display details of the `ConfigMap` using the following command:

```shell
kubectl describe configmaps game-config
```

The output is similar to:
```
Name:         game-config
Namespace:    default
Labels:       <none>
Annotations:  <none>

Data
====
game.properties:
----
enemies=aliens
lives=3
enemies.cheat=true
enemies.cheat.level=noGoodRotten
secret.code.passphrase=UUDDLRLRBABAS
secret.code.allowed=true
secret.code.lives=30
ui.properties:
----
color.good=purple
color.bad=yellow
allow.textmode=true
how.nice.to.look=fairlyNice
```

The `game.properties` and `ui.properties` files in the
`configure-pod-container/configmap/` directory are represented in the `data` section
of the `ConfigMap`.

```shell
kubectl get configmaps game-config -o yaml
```
The output is similar to this:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  creationTimestamp: 2016-02-18T18:52:05Z
  name: game-config
  namespace: default
  resourceVersion: "516"
  uid: b4952dc3-d670-11e5-8cd0-68f728db1985
data:
  game.properties: |
    enemies=aliens
    lives=3
    enemies.cheat=true
    enemies.cheat.level=noGoodRotten
    secret.code.passphrase=UUDDLRLRBABAS
    secret.code.allowed=true
    secret.code.lives=30
  ui.properties: |
    color.good=purple
    color.bad=yellow
    allow.textmode=true
    how.nice.to.look=fairlyNice
```

### Create a ConfigMap from a file {#create-configmaps-from-files}

#### Arbitrary files (any format) {#arbitrary-files}

You can use `kubectl create configmap` to create a `ConfigMap` from an individual file,
or from multiple files.

For example,

```shell
kubectl create configmap game-config-2 --from-file=configure-pod-container/configmap/game.properties
```

produces a `ConfigMap` _game-config-2_.

You can display details of the game-config-2 ConfigMap by running:

```shell
kubectl describe configmaps game-config-2
```

The output is similar to:

```
Name:         game-config-2
Namespace:    default
Labels:       <none>
Annotations:  <none>

Data
====
game.properties:
----
enemies=aliens
lives=3
enemies.cheat=true
enemies.cheat.level=noGoodRotten
secret.code.passphrase=UUDDLRLRBABAS
secret.code.allowed=true
secret.code.lives=30
```

You can pass in the `--from-file` argument multiple times to create a `ConfigMap` from
multiple data sources.

```shell
kubectl create configmap game-config-2 \
  --from-file=configure-pod-container/configmap/game.properties \
  --from-file=configure-pod-container/configmap/ui.properties
```

You can display details of the _game-config-2_ `ConfigMap` using the following command:

```shell
kubectl describe configmaps game-config-2
```

The output is similar to:

```
Name:         game-config-2
Namespace:    default
Labels:       <none>
Annotations:  <none>

Data
====
game.properties:
----
enemies=aliens
lives=3
enemies.cheat=true
enemies.cheat.level=noGoodRotten
secret.code.passphrase=UUDDLRLRBABAS
secret.code.allowed=true
secret.code.lives=30
ui.properties:
----
color.good=purple
color.bad=yellow
allow.textmode=true
how.nice.to.look=fairlyNice
```

When `kubectl` creates a ConfigMap from inputs that are not ASCII or UTF-8, the tool puts
these into the `binaryData` field of the ConfigMap, and not in `data`. Both text and binary
data sources can be combined in one ConfigMap.

If you want to view the `binaryData` keys (and their values) in a ConfigMap, you can run
`kubectl get configmap -o jsonpath='{.binaryData}' <name>`.

##### Customizing the file name

You can define a key other than the file name to use in the `data` section of your
`ConfigMap` when using the `--from-file` argument:

```shell
kubectl create configmap game-config-3 --from-file=<my-key-name>=<path-to-file>
```

where `<my-key-name>` is the key you want to use in the `ConfigMap`, and `<path-to-file>`
is the location of the data source file you want the key to represent.

For example:

```shell
kubectl create configmap game-config-3 --from-file=game-special-key=configure-pod-container/configmap/game.properties
```

You can then fetch and check that `ConfigMap`, _game-config-3_:
```
kubectl get configmaps game-config-3 -o yaml
```

The output is similar to:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  creationTimestamp: 2016-02-18T18:54:22Z
  name: game-config-3
  namespace: default
  resourceVersion: "530"
  uid: 05f8da22-d671-11e5-8cd0-68f728db1985
data:
  game-special-key: |
    enemies=aliens
    lives=3
    enemies.cheat=true
    enemies.cheat.level=noGoodRotten
    secret.code.passphrase=UUDDLRLRBABAS
    secret.code.allowed=true
    secret.code.lives=30
```

#### Key-value environment files

Use the option `--from-env-file` to create a `ConfigMap` from an env-file.
env-files contain a list of environment variables.

These syntax rules apply:
- Each line in an env file has to be in VAR=VAL format.
- Lines beginning with # (i.e. comments) are ignored.
- Blank lines are ignored.
- There is no special handling of quotation marks.

If the value includes quotation marks, those are copied into the ConfigMap verbatim.

This example creates a `ConfigMap` from an env-file:

```shell
# Download the sample files into `configure-pod-container/configmap/` directory
curl -o configure-pod-container/configmap/game-env-file.properties https://kubernetes.io/examples/configmap/game-env-file.properties
```

The env-file `game-env-file.properties` looks like:
{{< codenew file="configmap/game-env-file.properties" >}}

```shell
kubectl create configmap game-config-env-file \
       --from-env-file=configure-pod-container/configmap/game-env-file.properties
```

produces a `ConfigMap` _game-config-env-file_. You can view that `ConfigMap`:

```shell
kubectl get configmap game-config-env-file -o yaml
```

where the output is similar to this:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  creationTimestamp: 2017-12-27T18:36:28Z
  name: game-config-env-file
  namespace: default
  resourceVersion: "809965"
  uid: d9d1ca5b-eb34-11e7-887b-42010a8002b8
data:
  allowed: '"true"'
  enemies: aliens
  lives: "3"
```

{{< note >}}
When passing `--from-env-file` multiple times to create a `ConfigMap` from multiple data
sources, only the last env-file is used.
{{< /note >}}

The behavior of passing `--from-env-file` multiple times is demonstrated by:

```shell
# Download the sample files into `configure-pod-container/configmap/` directory
wget https://kubernetes.io/examples/configmap/ui-env-file.properties -O configure-pod-container/configmap/ui-env-file.properties

# Create the ConfigMap
kubectl create configmap config-multi-env-files \
        --from-env-file=configure-pod-container/configmap/game-env-file.properties \
        --from-env-file=configure-pod-container/configmap/ui-env-file.properties
```

You can view the `ConfigMap` _config-multi-env-files_:

```shell
kubectl get configmap config-multi-env-files -o yaml
```

The output is similar to:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  creationTimestamp: 2017-12-27T18:38:34Z
  name: config-multi-env-files
  namespace: default
  resourceVersion: "810136"
  uid: 252c4572-eb35-11e7-887b-42010a8002b8
data:
  color: purple
  how: fairlyNice
  textmode: "true"
```


### Create ConfigMaps from literal values

You can use `kubectl create configmap` with the `--from-literal` argument to define
a literal value from the command line:

```shell
kubectl create configmap special-config --from-literal=special.how=very --from-literal=special.type=charm
```

You can pass in multiple key-value pairs. Each pair provided on the command line is
represented as a separate entry in the `data` section of the `ConfigMap`.

```shell
kubectl get configmaps special-config -o yaml
```

The output is similar to:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  creationTimestamp: 2016-02-18T19:14:38Z
  name: special-config
  namespace: default
  resourceVersion: "651"
  uid: dadce046-d673-11e5-8cd0-68f728db1985
data:
  special.how: very
  special.type: charm
```

### Generate ConfigMaps from files

You can also create a `ConfigMap` from generators and then apply it to create the object
on the API server. The generators should be specified in a `kustomization.yaml` inside
a directory.

For example, to generate a `ConfigMap` from the file
`configure-pod-container/configmap/game.properties`:

```shell
# Create a kustomization.yaml file with ConfigMapGenerator
cat <<EOF >./kustomization.yaml
configMapGenerator:
- name: game-config-4
  files:
  - configure-pod-container/configmap/game.properties
EOF
```

Apply the kustomization directory to create the ConfigMap:
```shell
kubectl apply -k .
```
```
configmap/game-config-4-m9dm2f92bt created
```

You can check that the `ConfigMap` was created like this:

```shell
kubectl get configmap
```
```
NAME                       DATA   AGE
game-config-4-m9dm2f92bt   1      37s
```
```shell
kubectl describe configmaps/game-config-4-m9dm2f92bt
```
```
Name:         game-config-4-m9dm2f92bt
Namespace:    default
Labels:       <none>
Annotations:  kubectl.kubernetes.io/last-applied-configuration:
                {"apiVersion":"v1","data":{"game.properties":"enemies=aliens\nlives=3\nenemies.cheat=true\nenemies.cheat.level=noGoodRotten\nsecret.code.p...

Data
====
game.properties:
----
enemies=aliens
lives=3
enemies.cheat=true
enemies.cheat.level=noGoodRotten
secret.code.passphrase=UUDDLRLRBABAS
secret.code.allowed=true
secret.code.lives=30
Events:  <none>
```

Notice that the generated `ConfigMap` name has a suffix appended by hashing the
contents. This ensures that a new `ConfigMap` is generated each time the content is
modified.

#### Define the key to use when generating a ConfigMap from a file

You can define a key other than the file name to use in the `ConfigMap`
generator. For example, to generate a `ConfigMap` from the file
`configure-pod-container/configmap/game.properties` with the key `game-special-key`:

```shell
# Create a kustomization.yaml file with ConfigMapGenerator
cat <<EOF >./kustomization.yaml
configMapGenerator:
- name: game-config-5
  files:
  - game-special-key=configure-pod-container/configmap/game.properties
EOF
```

Apply the kustomization directory to create the `ConfigMap`:
```shell
kubectl apply -k .
configmap/game-config-5-m67dt67794 created
```

### Generate ConfigMaps using literal data {#generate-configmaps-from-literals}

This example shows you how to creat a `ConfigMap` from two literal key/value pairs:
`special.type=charm` and `special.how=very`, using Kustomize and kubectl. To achieve
this, you can specify the `ConfigMap` generator. Create (or replace)xi
`kustomization.yaml` with the following contents:

```yaml
---
configMapGenerator:
- name: special-config-2
  literals:
  - special.how=very
  - special.type=charm
```

Apply Kustomization from the current working directory to create the `ConfigMap`:
```shell
kubectl apply -k .
```
```
configmap/special-config-2-c92b5mmcf2 created
```

---

Now that you have learned to define `ConfigMap`s, you can move on to the next
section, and learn how to use these objects with pods.

## Define container environment variables using ConfigMap data

There are several ways to use `ConfigMap`s. One of the most common is to
set environment variables for a container in a pod.

### Define a container environment variable with data from a single ConfigMap

1. Define a `ConfigMap` holding the key-value pair that you want to use:

   ```shell
   kubectl create configmap special-config --from-literal=special.how=very
   ```

2. Assign the `special.how` value defined in the ConfigMap to the `SPECIAL_LEVEL_KEY`
   environment variable in the `Pod` specification. Here's the manifest you'll use.

   {{< codenew file="pods/pod-single-configmap-env-variable.yaml" >}}

   Create the `Pod`:

   ```shell
   kubectl create -f https://kubernetes.io/examples/pods/pod-single-configmap-env-variable.yaml
   ```

   The `Pod`'s output includes environment variable `SPECIAL_LEVEL_KEY=very`.

### Define container environment variables with data from multiple ConfigMaps

As with the previous example, create the `ConfigMap`s first. Here is a manifest for
the `ConfigMap`s:

{{< codenew file="configmap/configmaps.yaml" >}}

Create the `ConfigMap`:

```shell
kubectl create -f https://kubernetes.io/examples/configmap/configmaps.yaml
```

Define the environment variables in the `Pod` specification:

{{< codenew file="pods/pod-multiple-configmap-env-variable.yaml" >}}

Create the `Pod`:

```shell
kubectl create -f https://kubernetes.io/examples/pods/pod-multiple-configmap-env-variable.yaml
```

This pod's output includes two environment variables:
`SPECIAL_LEVEL_KEY=very` and `LOG_LEVEL=INFO`.

### Configure all key-value pairs in a ConfigMap as container environment variables

Create a `ConfigMap` containing multiple key-value pairs. The manifest looks like

{{< codenew file="configmap/configmap-multikeys.yaml" >}}

Create the `ConfigMap`:

```shell
kubectl create -f https://kubernetes.io/examples/configmap/configmap-multikeys.yaml
```

Use `envFrom` to define all of the `ConfigMap`'s data as container environment
variables. The key from the `ConfigMap` becomes the environment variable name in the
pod.
Here is the `Pod` manifest to use.

{{< codenew file="pods/pod-configmap-envFrom.yaml" >}}

Create the `Pod`:

```shell
kubectl create -f https://kubernetes.io/examples/pods/pod-configmap-envFrom.yaml
```

This pod's output includes environment variables `SPECIAL_LEVEL=very` and `SPECIAL_TYPE=charm`.

### Use ConfigMap-defined environment variables in Pod commands

You can use environment variables in the `command` and `args` of a container using
the `$(VAR_NAME)` Kubernetes substitution syntax, including variables derived from a
`ConfigMap`.

For example, the following `Pod` manifest:

{{< codenew file="pods/pod-configmap-env-var-valueFrom.yaml" >}}

created by running

```shell
kubectl create -f https://kubernetes.io/examples/pods/pod-configmap-env-var-valueFrom.yaml
```

produces the following output from the _test-container_ container:

```shell
very charm
```

## Add ConfigMap data to a volume

Another way to use a `ConfigMap` with a pod is to set up read-only files in a
mounted {{< glossary_tooltip term_id="volume" >}}.

As explained in [Create ConfigMaps from files](#create-configmaps-from-files), when
you create a `ConfigMap` using `--from-file`, the filename becomes a key stored in the
`data` section of the `ConfigMap`. The file contents become the key's value. Then later
you can configure a `Pod` to see the same set of files (or just some of those files) mounted
at a path you choose.

The examples in this section refer to a `ConfigMap` named _special-config_. Here is the
manifest for the _special-config_ `ConfigMap`.

{{< codenew file="configmap/configmap-multikeys.yaml" >}}

Create the _special-config_ `ConfigMap`:

```shell
kubectl create -f https://kubernetes.io/examples/configmap/configmap-multikeys.yaml
```

### Populate a volume with data stored in a ConfigMap

Add a new entry to `volumes` section of the `Pod` specification, creating a volume
of type `configMap`, and referencing the _special-config_ `ConfigMap`. Then, set
a container in the pod to mount that new volume.
This mount adds the `ConfigMap` data to the directory specified as `volumeMounts.mountPath`
(in this case: `/etc/config`).

The `command` section lists directory files with names that match the keys in `ConfigMap`.

{{< codenew file="pods/pod-configmap-volume.yaml" >}}

Create the `Pod`:

```shell
kubectl create -f https://kubernetes.io/examples/pods/pod-configmap-volume.yaml
```

Once the pod is running, you can use `kubectl exec` to run `ls /etc/config/` inside the
pod (it only has one container). The `ls` command produces the output below:

```shell
SPECIAL_LEVEL
SPECIAL_TYPE
```

{{< note >}}
If you mount a `ConfigMap`, or any other volume, over a directory that already contains
entries, the volume mount shadows the existing entries so that they aren't accessible.

It is as if the `ConfigMap` deletes the existing files.
{{< /note >}}

Text data is exposed as files using the UTF-8 character encoding. To use some other
character encoding, use `binaryData`.

### Add ConfigMap data to a specific path in the volume

Use the `path` field to specify the desired file path for specific ConfigMap items.
In this case, the `SPECIAL_LEVEL` item will be mounted in the `config-volume` volume at
`/etc/config/keys`.

{{< codenew file="pods/pod-configmap-volume-specific-key.yaml" >}}

Create the `Pod`:

```shell
kubectl create -f https://kubernetes.io/examples/pods/pod-configmap-volume-specific-key.yaml
```

Once the pod is running, you can use `kubectl exec` to run `cat /etc/config/keys` inside the
pod (it only has one container). The contents of `/etc/config/keys` are:

```
very
```

{{< caution >}}
Even though you have set up a volume to map only a single item, this mount shadows **any**
existing entry inside `/etc/config`. Take care not to hide data that you want to retain
from the layers of the container image.
{{< /caution >}}

#### Projecting keys to specific paths and file permissions {#project-keys-to-specific-paths-and-file-permissions}

You can project keys to specific paths and specific permissions on a per-file
basis. The [Secret](/docs/concepts/configuration/secret/#using-secrets-as-files-from-a-pod) concept page explains this.

<!-- discussion -->

## Understanding ConfigMaps and Pods

The `ConfigMap` object stores configuration data as key-value pairs. The data can
be consumed in pods or provide the configurations for system components such as
controllers. A `ConfigMap` is similar to a [Secret](/docs/concepts/configuration/secret/), but
provides a means of working with strings that don't contain sensitive information. Users
and system components alike can store configuration data in `ConfigMap`s.

{{< note >}}
`ConfigMap`s should reference properties files, not replace them. Think of the `ConfigMap`
as representing something similar to the POSIX / Linux `/etc` directory and its contents.

For example, if you create a Kubernetes volume from a `ConfigMap`, each data item in the
`ConfigMap` is represented by an individual file in the volume.
{{< /note >}}

The `ConfigMap`'s `data` field contains the configuration data. The Kubernetes API does
not pay attention to the contents of the values you set. As shown in the example
below, this can be simple — like individual properties defined using `--from-literal`,
or complex — like configuration files, or JSON blobs, defined using `--from-file`.

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  creationTimestamp: 2016-02-18T19:14:38Z
  name: example-config
  namespace: default
data:
  # example of a simple property defined using --from-literal
  example.property.1: hello
  example.property.2: world
  # example of a complex property defined using --from-file
  example.property.file: |-
    property.1=value-1
    property.2=value-2
    property.3=value-3
```

### Mounted ConfigMaps are updated automatically

When a `ConfigMap` already being consumed in a volume is updated, projected keys are
eventually updated as well. The kubelet checks whether the mounted `ConfigMap` is
fresh on every periodic sync. The kubelet uses a local TTL-based cache for
getting the current value of the `ConfigMap`. As a result, the total delay from the moment
when the `ConfigMap` is updated to the moment when new keys are projected to the pod can
be as long as kubelet sync period (1 minute by default) **plus** the time-to-live of the
kubelet's `ConfigMap` cache (also 1 minute by default).

You can trigger an immediate refresh by updating one of the Pod's annotations.

{{< note >}}
A container using a `ConfigMap` as a [`subPath`](/docs/concepts/storage/volumes/#using-subpath) volume does not receive `ConfigMap` updates.
{{< /note >}}


## Restrictions

- You must create a `ConfigMap` before referencing it in a `Pod` specification, unless you
  mark the `ConfigMap` as `optional`. If you reference a `ConfigMap` that doesn't exist,
  the pod won't start. Likewise, references to keys that don't exist in the `ConfigMap`
  will prevent the pod from starting.
- If you use `envFrom` to define environment variables from `ConfigMaps`, keys that are
  considered invalid are skipped. The pod will be allowed to start, but the kubelet spots
  the invalid keys and makes a note of this by creating `Event`s for the `Pod`;
  (the reason code is `InvalidEnvironmentVariableNames`) and the log message lists each
  skipped key. For example:

  ```shell
  kubectl get events
  ```

  The output is similar to:
  ```
  LASTSEEN FIRSTSEEN COUNT NAME          KIND  SUBOBJECT  TYPE      REASON                            SOURCE                MESSAGE
   0s       0s        1     dapi-test-pod Pod              Warning   InvalidEnvironmentVariableNames   {kubelet, 127.0.0.1}  Keys [1badkey, 2alsobad] from the EnvFrom configMap default/myconfig were skipped since they are considered invalid environment variable names.
  ```
- Each `ConfigMap` resides in a specific
  {{< glossary_tooltip term_id="namespace" text="namespace" >}}. A `ConfigMap` can
  only be referenced by `Pod`s residing in the same namespace.
- You can't use `ConfigMap`s for
  {{< glossary_tooltip text="static pods" term_id="static-pod" >}}, because the kubelet
  does not support this.


## {{% heading "whatsnext" %}}

* Follow a real world example of [Configuring Redis using a ConfigMap](/docs/tutorials/configuration/configure-redis-using-configmap/).
