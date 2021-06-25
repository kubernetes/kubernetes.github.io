---
reviewers:
- jsafrane
title: Create static Pods
weight: 170
content_type: task
---

<!-- overview -->


*Static Pods* are managed directly by the kubelet daemon on a specific node,
without the {{< glossary_tooltip text="API server" term_id="kube-apiserver" >}}
observing them.
Unlike Pods that are managed by the control plane (for example, a
{{< glossary_tooltip text="Deployment" term_id="deployment" >}});
instead, the kubelet watches each static Pod (and restarts it if it fails).

Static Pods are always bound to one {{< glossary_tooltip term_id="kubelet" >}} on a specific node.

The kubelet automatically tries to create a {{< glossary_tooltip text="mirror Pod" term_id="mirror-pod" >}}
on the Kubernetes API server for each static Pod.
This means that the Pods running on a node are visible on the API server,
but cannot be controlled from there.
The Pod names will suffixed with the node hostname with a leading hyphen

{{< note >}}
If you are running clustered Kubernetes and are using static
Pods to run a Pod on every node, you should probably be using a
{{< glossary_tooltip text="DaemonSet" term_id="daemonset" >}}
instead.
{{< /note >}}

{{< note >}}
The Spec of a Static Pod cannot refer to other API objects
(e.g., {{< glossary_tooltip text="ServiceAccount" term_id="service-account" >}},
{{< glossary_tooltip text="ConfigMap" term_id="configmap" >}},
{{< glossary_tooltip text="Secret" term_id="secret" >}}, etc).
{{< /note >}}

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}

This page assumes you're using {{< glossary_tooltip term_id="docker" >}} to run Pods,
and that your nodes are running the Fedora operating system.
Instructions for other distributions or Kubernetes installations may vary.

<!-- steps -->

## Create a static pod {#static-pod-creation}

You can configure a static Pod with either a [file system hosted configuration file](/docs/tasks/configure-pod-container/static-pod/#configuration-files) or a [web hosted configuration file](/docs/tasks/configure-pod-container/static-pod/#pods-created-via-http).

### Filesystem-hosted static Pod manifest {#configuration-files}

Manifests are standard Pod definitions in JSON or YAML format in a specific directory. Use the `staticPodPath: <the directory>` field in the
[kubelet configuration file](/docs/reference/config-api/kubelet-config.v1beta1/),
which periodically scans the directory and creates/deletes static Pods as YAML/JSON files appear/disappear there.
Note that the kubelet will ignore files starting with dots when scanning the specified directory.

For example, this is how to start a simple web server as a static Pod:

1. Choose a node where you want to run the static Pod. In this example, it's `my-node1`.

    ```shell
    ssh my-node1
    ```

2. Choose a directory, say `/etc/kubelet.d` and place a web server Pod definition there, for example `/etc/kubelet.d/static-web.yaml`:

    ```shell
    # Run this command on the node where kubelet is running
    mkdir /etc/kubelet.d/
    cat <<EOF >/etc/kubelet.d/static-web.yaml
    apiVersion: v1
    kind: Pod
    metadata:
      name: static-web
      labels:
        role: myrole
    spec:
      containers:
        - name: web
          image: nginx
          ports:
            - name: web
              containerPort: 80
              protocol: TCP
    EOF
    ```

3. Configure your kubelet on the node to use this directory by running it with `--pod-manifest-path=/etc/kubelet.d/` argument. On Fedora edit `/etc/kubernetes/kubelet` to include this line:

   ```
   KUBELET_ARGS="--cluster-dns=10.254.0.10 --cluster-domain=kube.local --pod-manifest-path=/etc/kubelet.d/"
   ```
   or add the `staticPodPath: <the directory>` field in the
   [kubelet configuration file](/docs/reference/config-api/kubelet-config.v1beta1/).

4. Restart the kubelet. On Fedora, you would run:

   ```shell
   # Run this command on the node where the kubelet is running
   systemctl restart kubelet
   ```

### Web-hosted static pod manifest {#pods-created-via-http}

Kubelet periodically downloads a file specified by `--manifest-url=<URL>` argument
and interprets it as a JSON/YAML file that contains Pod definitions.
Similar to how [filesystem-hosted manifests](#configuration-files) work, the kubelet
refetches the manifest on a schedule. If there are changes to the list of static
Pods, the kubelet applies them.

To use this approach: 

1. Create a YAML file and store it on a web server so that you can pass the URL of that file to the kubelet.

    ```yaml
    apiVersion: v1
    kind: Pod
    metadata:
      name: static-web
      labels:
        role: myrole
    spec:
      containers:
        - name: web
          image: nginx
          ports:
            - name: web
              containerPort: 80
              protocol: TCP
    ```

2. Configure the kubelet on your selected node to use this web manifest by running it with `--manifest-url=<manifest-url>`. On Fedora, edit `/etc/kubernetes/kubelet` to include this line:

    ```
    KUBELET_ARGS="--cluster-dns=10.254.0.10 --cluster-domain=kube.local --manifest-url=<manifest-url>"
    ```

3. Restart the kubelet. On Fedora, you would run:

    ```shell
    # Run this command on the node where the kubelet is running
    systemctl restart kubelet
    ```

## Observe static pod behavior {#behavior-of-static-pods}

When the kubelet starts, it automatically starts all defined static Pods. As you have
defined a static Pod and restarted the kubelet, the new static Pod should
already be running.

You can view running containers (including static Pods) by running (on the node):
```shell
# Run this command on the node where the kubelet is running
docker ps
```

The output might be something like:

```
CONTAINER ID IMAGE         COMMAND  CREATED        STATUS         PORTS     NAMES
f6d05272b57e nginx:latest  "nginx"  8 minutes ago  Up 8 minutes             k8s_web.6f802af4_static-web-fk-node1_default_67e24ed9466ba55986d120c867395f3c_378e5f3c
```

You can see the mirror Pod on the API server:

```shell
kubectl get pods
```
```
NAME                       READY     STATUS    RESTARTS   AGE
static-web-my-node1        1/1       Running   0          2m
```

{{< note >}}
Make sure the kubelet has permission to create the mirror Pod in the API server. If not, the creation request is rejected by the API server. See
[PodSecurityPolicy](/docs/concepts/policy/pod-security-policy/).
{{< /note >}}


{{< glossary_tooltip term_id="label" text="Labels" >}} from the static Pod are
propagated into the mirror Pod. You can use those labels as normal via
{{< glossary_tooltip term_id="selector" text="selectors" >}}, etc.

If you try to use `kubectl` to delete the mirror Pod from the API server,
the kubelet _doesn't_ remove the static Pod:

```shell
kubectl delete pod static-web-my-node1
```
```
pod "static-web-my-node1" deleted
```
You can see that the Pod is still running:
```shell
kubectl get pods
```
```
NAME                       READY     STATUS    RESTARTS   AGE
static-web-my-node1        1/1       Running   0          12s
```

Back on your node where the kubelet is running, you can try to stop the Docker
container manually.
You'll see that, after a time, the kubelet will notice and will restart the Pod
automatically:

```shell
# Run these commands on the node where the kubelet is running
docker stop f6d05272b57e # replace with the ID of your container
sleep 20
docker ps
```
```
CONTAINER ID        IMAGE         COMMAND                CREATED       ...
5b920cbaf8b1        nginx:latest  "nginx -g 'daemon of   2 seconds ago ...
```

## Dynamic addition and removal of static pods

The running kubelet periodically scans the configured directory (`/etc/kubelet.d` in our example) for changes and adds/removes Pods as files appear/disappear in this directory.

```shell
# This assumes you are using filesystem-hosted static Pod configuration
# Run these commands on the node where the kubelet is running
#
mv /etc/kubelet.d/static-web.yaml /tmp
sleep 20
docker ps
# You see that no nginx container is running
mv /tmp/static-web.yaml  /etc/kubelet.d/
sleep 20
docker ps
```
```
CONTAINER ID        IMAGE         COMMAND                CREATED           ...
e7a62e3427f1        nginx:latest  "nginx -g 'daemon of   27 seconds ago
```

