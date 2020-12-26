---
title: Configure a Pod to Use a ConfigMap
content_type: task
weight: 150
card:
  name: tasks
  weight: 50
---

<!-- overview -->
ConfigMaps allow you to decouple configuration artifacts from image content to keep
containerized applications portable. This page provides a series of usage examples
demonstrating how to create ConfigMaps and configure Pods using data stored in
ConfigMaps.



## {{% heading "prerequisites" %}}


{{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}



<!-- steps -->


## Create a ConfigMap

You can use either `kubectl create configmap` or a ConfigMap generator in
`kustomization.yaml` to create a ConfigMap. Note that `kubectl` starts to support
`kustomization.yaml` since 1.14.

### Create a ConfigMap Using kubectl create configmap

Use the `kubectl create configmap` command to create ConfigMaps
from [directories](#create-configmaps-from-directories),
[files](#create-configmaps-from-files), or
[literal values](#create-configmaps-from-literal-values):

```shell
kubectl create configmap <map-name> <data-source>
```

where \<map-name> is the name you want to assign to the ConfigMap and \<data-source>
is the directory, file, or literal value to draw the data from.
The name of a ConfigMap object must be a valid
[DNS subdomain name](/docs/concepts/overview/working-with-objects/names#dns-subdomain-names).

When you are creating a ConfigMap based on a file, the key in the \<data-source>
defaults to the basename of the file, and the value defaults to the file content.

You can use [`kubectl describe`](/docs/reference/generated/kubectl/kubectl-commands/#describe) or
[`kubectl get`](/docs/reference/generated/kubectl/kubectl-commands/#get) to retrieve information
about a ConfigMap.

#### Create ConfigMaps from directories

You can use `kubectl create configmap` to create a ConfigMap from multiple files in
the same directory. When you are creating a ConfigMap based on a directory, kubectl
identifies files whose basename is a valid key in the directory and packages each of
those files into the new ConfigMap. Any directory entries except regular files are
ignored (e.g. subdirectories, symlinks, devices, pipes, etc).

For example:

```shell
# Create the local directory
mkdir -p configure-pod-container/configmap/

# Download the sample files into `configure-pod-container/configmap/` directory
wget https://kubernetes.io/examples/configmap/game.properties -O configure-pod-container/configmap/game.properties
wget https://kubernetes.io/examples/configmap/ui.properties -O configure-pod-container/configmap/ui.properties

# Create the configmap
kubectl create configmap game-config --from-file=configure-pod-container/configmap/
```

The above command packages each file, in this case, `game.properties` and `ui.properties`
in the `configure-pod-container/configmap/` directory into the game-config ConfigMap. You
can display details of the ConfigMap using the following command:

```shell
kubectl describe configmaps game-config
```

The output is similar to this:
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
of the ConfigMap.

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

#### Create ConfigMaps from files

You can use `kubectl create configmap` to create a ConfigMap from an individual file,
or from multiple files.

For example,

```shell
kubectl create configmap game-config-2 --from-file=configure-pod-container/configmap/game.properties
```

would produce the following ConfigMap:

```shell
kubectl describe configmaps game-config-2
```

where the output is similar to this:

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

You can pass in the `--from-file` argument multiple times to create a ConfigMap from
multiple data sources.

```shell
kubectl create configmap game-config-2 --from-file=configure-pod-container/configmap/game.properties --from-file=configure-pod-container/configmap/ui.properties
```

You can display details of the `game-config-2` ConfigMap using the following command:

```shell
kubectl describe configmaps game-config-2
```

The output is similar to this:

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

When `kubectl` creates a ConfigMap from inputs that are not ASCII or UTF-8, the tool puts these into the `binaryData` field of the ConfigMap, and not in `data`. Both text and binary data sources can be combined in one ConfigMap.
If you want to view the `binaryData` keys (and their values) in a ConfigMap, you can run `kubectl get configmap -o jsonpath='{.binaryData}' <name>`.

Use the option `--from-env-file` to create a ConfigMap from an env-file, for example:

```shell
# Env-files contain a list of environment variables.
# These syntax rules apply:
#   Each line in an env file has to be in VAR=VAL format.
#   Lines beginning with # (i.e. comments) are ignored.
#   Blank lines are ignored.
#   There is no special handling of quotation marks
#    (i.e. they will be part of the ConfigMap value)).

# Download the sample files into `configure-pod-container/configmap/` directory
wget https://kubernetes.io/examples/configmap/game-env-file.properties -O configure-pod-container/configmap/game-env-file.properties

# The env-file `game-env-file.properties` looks like below
cat configure-pod-container/configmap/game-env-file.properties
enemies=aliens
lives=3
allowed="true"

# This comment and the empty line above it are ignored
```

```shell
kubectl create configmap game-config-env-file \
       --from-env-file=configure-pod-container/configmap/game-env-file.properties
```

would produce the following ConfigMap:

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

{{< caution >}}
When passing `--from-env-file` multiple times to create a ConfigMap from multiple data sources, only the last env-file is used.
{{< /caution >}}

The behavior of passing `--from-env-file` multiple times is demonstrated by:

```shell
# Download the sample files into `configure-pod-container/configmap/` directory
wget https://kubernetes.io/examples/configmap/ui-env-file.properties -O configure-pod-container/configmap/ui-env-file.properties

# Create the configmap
kubectl create configmap config-multi-env-files \
        --from-env-file=configure-pod-container/configmap/game-env-file.properties \
        --from-env-file=configure-pod-container/configmap/ui-env-file.properties
```

would produce the following ConfigMap:

```shell
kubectl get configmap config-multi-env-files -o yaml
```

where the output is similar to this:
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

#### Define the key to use when creating a ConfigMap from a file

You can define a key other than the file name to use in the `data` section of your
ConfigMap when using the `--from-file` argument:

```shell
kubectl create configmap game-config-3 --from-file=<my-key-name>=<path-to-file>
```

where `<my-key-name>` is the key you want to use in the ConfigMap and `<path-to-file>`
is the location of the data source file you want the key to represent.

For example:

```shell
kubectl create configmap game-config-3 --from-file=game-special-key=configure-pod-container/configmap/game.properties
```

would produce the following ConfigMap:
```
kubectl get configmaps game-config-3 -o yaml
```

where the output is similar to this:
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

#### Create ConfigMaps from literal values

You can use `kubectl create configmap` with the `--from-literal` argument to define
a literal value from the command line:

```shell
kubectl create configmap special-config --from-literal=special.how=very --from-literal=special.type=charm
```

You can pass in multiple key-value pairs. Each pair provided on the command line is
represented as a separate entry in the `data` section of the ConfigMap.

```shell
kubectl get configmaps special-config -o yaml
```

The output is similar to this:
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

### Create a ConfigMap from generator

`kubectl` supports `kustomization.yaml` since 1.14.
You can also create a ConfigMap from generators and then apply it to create the object on
the Apiserver. The generators
should be specified in a `kustomization.yaml` inside a directory.

#### Generate ConfigMaps from files

For example, to generate a ConfigMap from files
`configure-pod-container/configmap/game.properties`

```shell
# Create a kustomization.yaml file with ConfigMapGenerator
cat <<EOF >./kustomization.yaml
configMapGenerator:
- name: game-config-4
  files:
  - configure-pod-container/configmap/game.properties
EOF
```

Apply the kustomization directory to create the ConfigMap object.

```shell
kubectl apply -k .
configmap/game-config-4-m9dm2f92bt created
```

You can check that the ConfigMap was created like this:

```shell
kubectl get configmap
NAME                       DATA   AGE
game-config-4-m9dm2f92bt   1      37s


kubectl describe configmaps/game-config-4-m9dm2f92bt
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

Note that the generated ConfigMap name has a suffix appended by hashing the
contents. This ensures that a new ConfigMap is generated each time the content is
modified.

#### Define the key to use when generating a ConfigMap from a file

You can define a key other than the file name to use in the ConfigMap generator.
For example, to generate a ConfigMap from files
`configure-pod-container/configmap/game.properties` with the key `game-special-key`

```shell
# Create a kustomization.yaml file with ConfigMapGenerator
cat <<EOF >./kustomization.yaml
configMapGenerator:
- name: game-config-5
  files:
  - game-special-key=configure-pod-container/configmap/game.properties
EOF
```

Apply the kustomization directory to create the ConfigMap object.
```shell
kubectl apply -k .
configmap/game-config-5-m67dt67794 created
```

#### Generate ConfigMaps from Literals
To generate a ConfigMap from literals `special.type=charm` and `special.how=very`,
you can specify the ConfigMap generator in `kustomization.yaml` as
```shell
# Create a kustomization.yaml file with ConfigMapGenerator
cat <<EOF >./kustomization.yaml
configMapGenerator:
- name: special-config-2
  literals:
  - special.how=very
  - special.type=charm
EOF
```
Apply the kustomization directory to create the ConfigMap object.
```shell
kubectl apply -k .
configmap/special-config-2-c92b5mmcf2 created
```

## Define container environment variables using ConfigMap data

### Define a container environment variable with data from a single ConfigMap

1.  Define an environment variable as a key-value pair in a ConfigMap:

    ```shell
    kubectl create configmap special-config --from-literal=special.how=very
    ```

2.  Assign the `special.how` value defined in the ConfigMap to the `SPECIAL_LEVEL_KEY` environment variable in the Pod specification.

   {{< codenew file="pods/pod-single-configmap-env-variable.yaml" >}}

   Create the Pod:

 ```shell
 kubectl create -f https://kubernetes.io/examples/pods/pod-single-configmap-env-variable.yaml
 ```

   Now, the Pod's output includes environment variable `SPECIAL_LEVEL_KEY=very`.

### Define container environment variables with data from multiple ConfigMaps

 * As with the previous example, create the ConfigMaps first.

   {{< codenew file="configmap/configmaps.yaml" >}}

   Create the ConfigMap:

 ```shell
 kubectl create -f https://kubernetes.io/examples/configmap/configmaps.yaml
 ```

* Define the environment variables in the Pod specification.

  {{< codenew file="pods/pod-multiple-configmap-env-variable.yaml" >}}

  Create the Pod:

 ```shell
 kubectl create -f https://kubernetes.io/examples/pods/pod-multiple-configmap-env-variable.yaml
 ```

  Now, the Pod's output includes environment variables `SPECIAL_LEVEL_KEY=very` and
  `LOG_LEVEL=INFO`.

## Configure all key-value pairs in a ConfigMap as container environment variables

{{< note >}}
This functionality is available in Kubernetes v1.6 and later.
{{< /note >}}

* Create a ConfigMap containing multiple key-value pairs.

  {{< codenew file="configmap/configmap-multikeys.yaml" >}}

  Create the ConfigMap:

 ```shell
 kubectl create -f https://kubernetes.io/examples/configmap/configmap-multikeys.yaml
 ```

* Use `envFrom` to define all of the ConfigMap's data as container environment
  variables. The key from the ConfigMap becomes the environment variable name in
  the Pod.

 {{< codenew file="pods/pod-configmap-envFrom.yaml" >}}

 Create the Pod:

 ```shell
 kubectl create -f https://kubernetes.io/examples/pods/pod-configmap-envFrom.yaml
 ```

 Now, the Pod's output includes environment variables `SPECIAL_LEVEL=very` and
 `SPECIAL_TYPE=charm`.


## Use ConfigMap-defined environment variables in Pod commands

You can use ConfigMap-defined environment variables in the `command` and `args` of a
container using the `$(VAR_NAME)` Kubernetes substitution syntax.

For example, the following Pod specification

{{< codenew file="pods/pod-configmap-env-var-valueFrom.yaml" >}}

created by running

```shell
kubectl create -f https://kubernetes.io/examples/pods/pod-configmap-env-var-valueFrom.yaml
```

produces the following output in the `test-container` container:

```shell
very charm
```

## Add ConfigMap data to a Volume

As explained in [Create ConfigMaps from files](#create-configmaps-from-files), when
you create a ConfigMap using ``--from-file``, the filename becomes a key stored in the
`data` section of the ConfigMap. The file contents become the key's value.

The examples in this section refer to a ConfigMap named special-config, shown below.

{{< codenew file="configmap/configmap-multikeys.yaml" >}}

Create the ConfigMap:

```shell
kubectl create -f https://kubernetes.io/examples/configmap/configmap-multikeys.yaml
```

### Populate a Volume with data stored in a ConfigMap

Add the ConfigMap name under the `volumes` section of the Pod specification.
This adds the ConfigMap data to the directory specified as `volumeMounts.mountPath`
(in this case, `/etc/config`).
The `command` section lists directory files with names that match the keys in ConfigMap.

{{< codenew file="pods/pod-configmap-volume.yaml" >}}

Create the Pod:

```shell
kubectl create -f https://kubernetes.io/examples/pods/pod-configmap-volume.yaml
```

When the pod runs, the command `ls /etc/config/` produces the output below:

```shell
SPECIAL_LEVEL
SPECIAL_TYPE
```

{{< caution >}}
If there are some files in the `/etc/config/` directory, they will be deleted.
{{< /caution >}}

{{< note >}}
Text data is exposed as files using the UTF-8 character encoding. To use some other
character encoding, use binaryData.
{{< /note >}}

### Add ConfigMap data to a specific path in the Volume

Use the `path` field to specify the desired file path for specific ConfigMap items.
In this case, the `SPECIAL_LEVEL` item will be mounted in the `config-volume` volume at
`/etc/config/keys`.

{{< codenew file="pods/pod-configmap-volume-specific-key.yaml" >}}

Create the Pod:

```shell
kubectl create -f https://kubernetes.io/examples/pods/pod-configmap-volume-specific-key.yaml
```

When the pod runs, the command `cat /etc/config/keys` produces the output below:

```shell
very
```

{{< caution >}}
Like before, all previous files in the `/etc/config/` directory will be deleted.
{{< /caution >}}

### Project keys to specific paths and file permissions

You can project keys to specific paths and specific permissions on a per-file
basis. The
[Secrets](/docs/concepts/configuration/secret/#using-secrets-as-files-from-a-pod)
user guide explains the syntax.

### Mounted ConfigMaps are updated automatically

When a ConfigMap already being consumed in a volume is updated, projected keys are
eventually updated as well. Kubelet is checking whether the mounted ConfigMap is fresh
on every periodic sync. However, it is using its local ttl-based cache for getting the
current value of the ConfigMap. As a result, the total delay from the moment when the
ConfigMap is updated to the moment when new keys are projected to the pod can be as
long as kubelet sync period (1 minute by default) + ttl of ConfigMaps cache (1 minute
by default) in kubelet.

You can trigger an immediate refresh by updating one of the pod's annotations.

{{< note >}}
A container using a ConfigMap as a [subPath](/docs/concepts/storage/volumes/#using-subpath) volume will not receive ConfigMap updates.
{{< /note >}}



<!-- discussion -->

## Understanding ConfigMaps and Pods

The ConfigMap API resource stores configuration data as key-value pairs. The data
can be consumed in pods or provide the configurations for system components such as
controllers. ConfigMap is similar to [Secrets](/docs/concepts/configuration/secret/), but
provides a means of working with strings that don't contain sensitive information. Users
and system components alike can store configuration data in ConfigMap.

{{< note >}}
ConfigMaps should reference properties files, not replace them. Think of the ConfigMap
as representing something similar to the Linux `/etc` directory and its contents. For
example, if you create a [Kubernetes Volume](/docs/concepts/storage/volumes/) from
a ConfigMap, each data item in the ConfigMap is represented by an individual file in
the volume.
{{< /note >}}

The ConfigMap's `data` field contains the configuration data. As shown in the example
below, this can be simple -- like individual properties defined using `--from-literal`
-- or complex -- like configuration files or JSON blobs defined using `--from-file`.

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

### Restrictions

- You must create a ConfigMap before referencing it in a Pod specification (unless you
mark the ConfigMap as "optional"). If you reference a ConfigMap that doesn't exist,
the Pod won't start. Likewise, references to keys that don't exist in the ConfigMap
will prevent the pod from starting.

- If you use `envFrom` to define environment variables from ConfigMaps, keys that are
considered invalid will be skipped. The pod will be allowed to start, but the invalid
names will be recorded in the event log (`InvalidVariableNames`). The log message
lists each skipped key. For example:

   ```shell
   kubectl get events
   ```

   The output is similar to this:
   ```
   LASTSEEN FIRSTSEEN COUNT NAME          KIND  SUBOBJECT  TYPE      REASON                            SOURCE                MESSAGE
   0s       0s        1     dapi-test-pod Pod              Warning   InvalidEnvironmentVariableNames   {kubelet, 127.0.0.1}  Keys [1badkey, 2alsobad] from the EnvFrom configMap default/myconfig were skipped since they are considered invalid environment variable names.
   ```

- ConfigMaps reside in a specific {{< glossary_tooltip term_id="namespace" >}}. A
  ConfigMap can only be referenced by pods residing in the same namespace.

- You can't use ConfigMaps for
  {{< glossary_tooltip text="static pods" term_id="static-pod" >}}, because the
  Kubelet does not support this.


## {{% heading "whatsnext" %}}

* Follow a real world example of
  [Configuring Redis using a ConfigMap](/docs/tutorials/configuration/configure-redis-using-configmap/).
