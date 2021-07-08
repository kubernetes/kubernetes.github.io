---
title: Update API Objects in Place Using kubectl patch
description: Use kubectl patch to update Kubernetes API objects in place. Do a strategic merge patch or a JSON merge patch.
content_type: task
weight: 50
---

<!-- overview -->

This task shows how to use `kubectl patch` to update an API object in place. The exercises
in this task demonstrate a strategic merge patch and a JSON merge patch.



## {{% heading "prerequisites" %}}


{{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}




<!-- steps -->

## Use a strategic merge patch to update a Deployment

Here's the configuration file for a Deployment that has two replicas. Each replica
is a Pod that has one container:

{{< codenew file="application/deployment-patch.yaml" >}}

Create the Deployment:

```shell
kubectl apply -f https://k8s.io/examples/application/deployment-patch.yaml
```

View the Pods associated with your Deployment:

```shell
kubectl get pods
```

The output shows that the Deployment has two Pods. The `1/1` indicates that
each Pod has one container:


```
NAME                        READY     STATUS    RESTARTS   AGE
patch-demo-28633765-670qr   1/1       Running   0          23s
patch-demo-28633765-j5qs3   1/1       Running   0          23s
```

Make a note of the names of the running Pods. Later, you will see that these Pods
get terminated and replaced by new ones.

At this point, each Pod has one Container that runs the nginx image. Now suppose
you want each Pod to have two containers: one that runs nginx and one that runs redis.

Create a file named `patch-file.yaml` that has this content:

```yaml
spec:
  template:
    spec:
      containers:
      - name: patch-demo-ctr-2
        image: redis
```

Patch your Deployment:

{{< tabs name="kubectl_patch_example" >}}
{{{< tab name="Bash" codelang="bash" >}}
kubectl patch deployment patch-demo --patch "$(cat patch-file.yaml)"
{{< /tab >}}
{{< tab name="PowerShell" codelang="posh" >}}
kubectl patch deployment patch-demo --patch $(Get-Content patch-file.yaml -Raw)
{{< /tab >}}}
{{< /tabs >}}

View the patched Deployment:

```shell
kubectl get deployment patch-demo --output yaml
```

The output shows that the PodSpec in the Deployment has two Containers:

```shell
containers:
- image: redis
  imagePullPolicy: Always
  name: patch-demo-ctr-2
  ...
- image: nginx
  imagePullPolicy: Always
  name: patch-demo-ctr
  ...
```

View the Pods associated with your patched Deployment:

```shell
kubectl get pods
```

The output shows that the running Pods have different names from the Pods that
were running previously. The Deployment terminated the old Pods and created two
new Pods that comply with the updated Deployment spec. The `2/2` indicates that
each Pod has two Containers:

```
NAME                          READY     STATUS    RESTARTS   AGE
patch-demo-1081991389-2wrn5   2/2       Running   0          1m
patch-demo-1081991389-jmg7b   2/2       Running   0          1m
```

Take a closer look at one of the patch-demo Pods:

```shell
kubectl get pod <your-pod-name> --output yaml
```

The output shows that the Pod has two Containers: one running nginx and one running redis:

```
containers:
- image: redis
  ...
- image: nginx
  ...
```

### Notes on the strategic merge patch

The patch you did in the preceding exercise is called a *strategic merge patch*.
Notice that the patch did not replace the `containers` list. Instead it added a new
Container to the list. In other words, the list in the patch was merged with the
existing list. This is not always what happens when you use a strategic merge patch on a list.
In some cases, the list is replaced, not merged.

With a strategic merge patch, a list is either replaced or merged depending on its
patch strategy. The patch strategy is specified by the value of the `patchStrategy` key
in a field tag in the Kubernetes source code. For example, the `Containers` field of `PodSpec`
struct has a `patchStrategy` of `merge`:

```go
type PodSpec struct {
  ...
  Containers []Container `json:"containers" patchStrategy:"merge" patchMergeKey:"name" ...`
```

You can also see the patch strategy in the
[OpenApi spec](https://raw.githubusercontent.com/kubernetes/kubernetes/master/api/openapi-spec/swagger.json):

```json
"io.k8s.api.core.v1.PodSpec": {
    ...
     "containers": {
      "description": "List of containers belonging to the pod. ...
      },
      "x-kubernetes-patch-merge-key": "name",
      "x-kubernetes-patch-strategy": "merge"
     },
```

And you can see the patch strategy in the
{{< api-reference page="workload-resources/pod-v1" anchor="PodSpec" text="Kubernetes API documentation" >}}.

Create a file named `patch-file-tolerations.yaml` that has this content:

```yaml
spec:
  template:
    spec:
      tolerations:
      - effect: NoSchedule
        key: disktype
        value: ssd
```

Patch your Deployment:

```shell
kubectl patch deployment patch-demo --patch "$(cat patch-file-tolerations.yaml)"
```

View the patched Deployment:

```shell
kubectl get deployment patch-demo --output yaml
```

The output shows that the PodSpec in the Deployment has only one Toleration:

```shell
tolerations:
      - effect: NoSchedule
        key: disktype
        value: ssd
```

Notice that the `tolerations` list in the PodSpec was replaced, not merged. This is because
the Tolerations field of PodSpec does not have a `patchStrategy` key in its field tag. So the
strategic merge patch uses the default patch strategy, which is `replace`.

```go
type PodSpec struct {
  ...
  Tolerations []Toleration `json:"tolerations,omitempty" protobuf:"bytes,22,opt,name=tolerations"`
```

## Use a JSON merge patch to update a Deployment

A strategic merge patch is different from a
[JSON merge patch](https://tools.ietf.org/html/rfc7386).
With a JSON merge patch, if you
want to update a list, you have to specify the entire new list. And the new list completely
replaces the existing list.

The `kubectl patch` command has a `type` parameter that you can set to one of these values:

<table>
  <tr><th>Parameter value</th><th>Merge type</th></tr>
  <tr><td>json</td><td><a href="https://tools.ietf.org/html/rfc6902">JSON Patch, RFC 6902</a></td></tr>
  <tr><td>merge</td><td><a href="https://tools.ietf.org/html/rfc7386">JSON Merge Patch, RFC 7386</a></td></tr>
  <tr><td>strategic</td><td>Strategic merge patch</td></tr>
</table>

For a comparison of JSON patch and JSON merge patch, see
[JSON Patch and JSON Merge Patch](https://erosb.github.io/post/json-patch-vs-merge-patch/).

The default value for the `type` parameter is `strategic`. So in the preceding exercise, you
did a strategic merge patch.

Next, do a JSON merge patch on your same Deployment. Create a file named `patch-file-2.yaml`
that has this content:

```yaml
spec:
  template:
    spec:
      containers:
      - name: patch-demo-ctr-3
        image: gcr.io/google-samples/node-hello:1.0
```

In your patch command, set `type` to `merge`:

```shell
kubectl patch deployment patch-demo --type merge --patch "$(cat patch-file-2.yaml)"
```

View the patched Deployment:

```shell
kubectl get deployment patch-demo --output yaml
```

The `containers` list that you specified in the patch has only one Container.
The output shows that your list of one Container replaced the existing `containers` list.

```shell
spec:
  containers:
  - image: gcr.io/google-samples/node-hello:1.0
    ...
    name: patch-demo-ctr-3
```

List the running Pods:

```shell
kubectl get pods
```

In the output, you can see that the existing Pods were terminated, and new Pods
were created. The `1/1` indicates that each new Pod is running only one Container.

```shell
NAME                          READY     STATUS    RESTARTS   AGE
patch-demo-1307768864-69308   1/1       Running   0          1m
patch-demo-1307768864-c86dc   1/1       Running   0          1m
```

## Use strategic merge patch to update a Deployment using the retainKeys strategy

Here's the configuration file for a Deployment that uses the `RollingUpdate` strategy:

{{< codenew file="application/deployment-retainkeys.yaml" >}}

Create the deployment:

```shell
kubectl apply -f https://k8s.io/examples/application/deployment-retainkeys.yaml
```

At this point, the deployment is created and is using the `RollingUpdate` strategy.

Create a file named `patch-file-no-retainkeys.yaml` that has this content:

```yaml
spec:
  strategy:
    type: Recreate
```

Patch your Deployment:

{{< tabs name="kubectl_retainkeys_example" >}}
{{{< tab name="Bash" codelang="bash" >}}
kubectl patch deployment retainkeys-demo --type merge --patch "$(cat patch-file-no-retainkeys.yaml)"
{{< /tab >}}
{{< tab name="PowerShell" codelang="posh" >}}
kubectl patch deployment retainkeys-demo --type merge --patch $(Get-Content patch-file-no-retainkeys.yaml -Raw)
{{< /tab >}}}
{{< /tabs >}}

In the output, you can see that it is not possible to set `type` as `Recreate` when a value is defined for `spec.strategy.rollingUpdate`:

```shell
The Deployment "retainkeys-demo" is invalid: spec.strategy.rollingUpdate: Forbidden: may not be specified when strategy `type` is 'Recreate'
```

The way to remove the value for `spec.strategy.rollingUpdate` when updating the value for `type` is to use the `retainKeys` strategy for the strategic merge.

Create another file named `patch-file-retainkeys.yaml` that has this content:

```yaml
spec:
  strategy:
    $retainKeys:
    - type
    type: Recreate
```

With this patch, we indicate that we want to retain only the `type` key of the `strategy` object. Thus, the `rollingUpdate` will be removed during the patch operation.

Patch your Deployment again with this new patch:

{{< tabs name="kubectl_retainkeys2_example" >}}
{{{< tab name="Bash" codelang="bash" >}}
kubectl patch deployment retainkeys-demo --type merge --patch "$(cat patch-file-retainkeys.yaml)"
{{< /tab >}}
{{< tab name="PowerShell" codelang="posh" >}}
kubectl patch deployment retainkeys-demo --type merge --patch $(Get-Content patch-file-retainkeys.yaml -Raw)
{{< /tab >}}}
{{< /tabs >}}

Examine the content of the Deployment:

```shell
kubectl get deployment retainkeys-demo --output yaml
```

The output shows that the strategy object in the Deployment does not contain the `rollingUpdate` key anymore:

```shell
spec:
  strategy:
    type: Recreate
  template:
```

### Notes on the strategic merge patch using the retainKeys strategy

The patch you did in the preceding exercise is called a *strategic merge patch with retainKeys strategy*. This method introduces a new directive `$retainKeys` that has the following strategies:

- It contains a list of strings.
- All fields needing to be preserved must be present in the `$retainKeys` list.
- The fields that are present will be merged with live object.
- All of the missing fields will be cleared when patching.
- All fields in the `$retainKeys` list must be a superset or the same as the fields present in the patch.

The `retainKeys` strategy does not work for all objects. It only works when the value of the `patchStrategy` key in a field tag in the Kubernetes source code contains `retainKeys`. For example, the `Strategy` field of the `DeploymentSpec` struct has a `patchStrategy` of `retainKeys`:

```go
type DeploymentSpec struct {
  ...
  // +patchStrategy=retainKeys
  Strategy DeploymentStrategy `json:"strategy,omitempty" patchStrategy:"retainKeys" ...`
```

You can also see the `retainKeys` strategy in the [OpenApi spec](https://raw.githubusercontent.com/kubernetes/kubernetes/master/api/openapi-spec/swagger.json):

```json
"io.k8s.api.apps.v1.DeploymentSpec": {
   ...
  "strategy": {
    "$ref": "#/definitions/io.k8s.api.apps.v1.DeploymentStrategy",
    "description": "The deployment strategy to use to replace existing pods with new ones.",
    "x-kubernetes-patch-strategy": "retainKeys"
  },
```

And you can see the `retainKeys` strategy in the
{{< api-reference page="workload-resources/deployment-v1" anchor="DeploymentSpec" text="Kubernetes API documentation" >}}.

## Alternate forms of the kubectl patch command

The `kubectl patch` command takes YAML or JSON. It can take the patch as a file or
directly on the command line.

Create a file named `patch-file.json` that has this content:

```json
{
   "spec": {
      "template": {
         "spec": {
            "containers": [
               {
                  "name": "patch-demo-ctr-2",
                  "image": "redis"
               }
            ]
         }
      }
   }
}
```

The following commands are equivalent:


```shell
kubectl patch deployment patch-demo --patch "$(cat patch-file.yaml)"
kubectl patch deployment patch-demo --patch 'spec:\n template:\n  spec:\n   containers:\n   - name: patch-demo-ctr-2\n     image: redis'

kubectl patch deployment patch-demo --patch "$(cat patch-file.json)"
kubectl patch deployment patch-demo --patch '{"spec": {"template": {"spec": {"containers": [{"name": "patch-demo-ctr-2","image": "redis"}]}}}}'
```

## Summary

In this exercise, you used `kubectl patch` to change the live configuration
of a Deployment object. You did not change the configuration file that you originally used to
create the Deployment object. Other commands for updating API objects include
[kubectl annotate](/docs/reference/generated/kubectl/kubectl-commands/#annotate),
[kubectl edit](/docs/reference/generated/kubectl/kubectl-commands/#edit),
[kubectl replace](/docs/reference/generated/kubectl/kubectl-commands/#replace),
[kubectl scale](/docs/reference/generated/kubectl/kubectl-commands/#scale),
and
[kubectl apply](/docs/reference/generated/kubectl/kubectl-commands/#apply).


{{< note >}}
Strategic merge patch is not supported for custom resources.
{{< /note >}}


## {{% heading "whatsnext" %}}


* [Kubernetes Object Management](/docs/concepts/overview/working-with-objects/object-management/)
* [Managing Kubernetes Objects Using Imperative Commands](/docs/tasks/manage-kubernetes-objects/imperative-command/)
* [Imperative Management of Kubernetes Objects Using Configuration Files](/docs/tasks/manage-kubernetes-objects/imperative-config/)
* [Declarative Management of Kubernetes Objects Using Configuration Files](/docs/tasks/manage-kubernetes-objects/declarative-config/)


