---
title: Use Cascading Deletion in a Cluster
content_type: task
---

<!--overview-->

This page shows you how to specify the type of [cascading deletion](/docs/concepts/workloads/controllers/garbage-collection/#cascading-deletion)
to use in your cluster during {{<glossary_tooltip text="garbage collection" term_id="garbage-collection">}}.

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}}

You also need to [create a sample Deployment](/docs/tasks/run-application/run-stateless-application-deployment/#creating-and-exploring-an-nginx-deployment) 
to experiment with the different types of cascading deletion. You will need to
recreate the Deployment for each type.

## Check owner references on your pods

Check that the `ownerReferences` field is present on your pods:

```shell 
kubectl get pods -l app=nginx --output=yaml
```

The output has an `ownerReferences` field similar to this:

```
apiVersion: v1
    ...
    ownerReferences:
    - apiVersion: apps/v1
      blockOwnerDeletion: true
      controller: true
      kind: ReplicaSet
      name: nginx-deployment-6b474476c4
      uid: 4fdcd81c-bd5d-41f7-97af-3a3b759af9a7
    ...
```

## Use foreground cascading deletion {#use-foreground-cascading-deletion}

By default, Kubernetes uses [background cascading deletion](/docs/concepts/workloads/controllers/garbage-collection/#background-deletion)
to delete dependents of an object. You can switch to foreground cascading deletion
using either `kubectl` or the Kubernetes API, depending on the Kubernetes
version your cluster runs. {{<version-check>}}

{{<tabs name="foreground_deletion">}}
{{% tab name="Kubernetes 1.20.x and later" %}}
You can delete objects using foreground cascading deletion using `kubectl` or the
Kubernetes API.

**Using kubectl**

Run the following command:
<!--TODO: verify release after which the --cascade flag is switched to a string in https://github.com/kubernetes/kubectl/commit/fd930e3995957b0093ecc4b9fd8b0525d94d3b4e-->

```shell
kubectl delete deployment nginx-deployment --cascade=foreground
```

**Using the Kubernetes API**

1. Start a local proxy session:

    ```shell
    kubectl proxy --port=8080
    ```

1. Use `curl` to trigger deletion:

   ```shell
   curl -X DELETE localhost:8080/apis/apps/v1/namespaces/default/deployments/nginx-deployment \
       -d '{"kind":"DeleteOptions","apiVersion":"v1","propagationPolicy":"Foreground"}' \
       -H "Content-Type: application/json"
   ```

   The output contains a `foregroundDeletion` {{<glossary_tooltip text="finalizer" term_id="finalizer">}}
   like this:

   ```
    "kind": "Deployment",
    "apiVersion": "apps/v1",
    "metadata": {
        "name": "nginx-deployment",
        "namespace": "default",
        "uid": "d1ce1b02-cae8-4288-8a53-30e84d8fa505",
        "resourceVersion": "1363097",
        "creationTimestamp": "2021-07-08T20:24:37Z",
        "deletionTimestamp": "2021-07-08T20:27:39Z",
        "finalizers": [
          "foregroundDeletion"
        ]
        ...
   ```

{{% /tab %}}
{{% tab name="Versions prior to Kubernetes 1.20.x" %}}
You can delete objects using foreground cascading deletion by calling the
Kubernetes API.

For details, read the [documentation for your Kubernetes version](/docs/home/supported-doc-versions/).

1. Start a local proxy session:

    ```shell
    kubectl proxy --port=8080
    ```

1. Use `curl` to trigger deletion:

   ```shell
   curl -X DELETE localhost:8080/apis/apps/v1/namespaces/default/deployments/nginx-deployment \
       -d '{"kind":"DeleteOptions","apiVersion":"v1","propagationPolicy":"Foreground"}' \
       -H "Content-Type: application/json"
   ```

   The output contains a `foregroundDeletion` {{<glossary_tooltip text="finalizer" term_id="finalizer">}}
   like this:

   ```
    "kind": "Deployment",
    "apiVersion": "apps/v1",
    "metadata": {
        "name": "nginx-deployment",
        "namespace": "default",
        "uid": "d1ce1b02-cae8-4288-8a53-30e84d8fa505",
        "resourceVersion": "1363097",
        "creationTimestamp": "2021-07-08T20:24:37Z",
        "deletionTimestamp": "2021-07-08T20:27:39Z",
        "finalizers": [
          "foregroundDeletion"
        ]
        ...
   ```
{{% /tab %}}
{{</tabs>}}

## Use background cascading deletion {#use-background-cascading-deletion}

1. [Create a sample Deployment](/docs/tasks/run-application/run-stateless-application-deployment/#creating-and-exploring-an-nginx-deployment).
1. Use either `kubectl` or the Kubernetes API to delete the Deployment,
   depending on the Kubernetes version your cluster runs. {{<version-check>}}

{{<tabs name="background_deletion">}}
{{% tab name="Kubernetes version 1.20.x and later" %}}

You can delete objects using background cascading deletion using `kubectl`
or the Kubernetes API.

Kubernetes uses background cascading deletion by default, and does so
even if you run the following commands without the `--cascade` flag or the
`propagationPolicy` argument.

**Using kubectl**

Run the following command:

```shell
kubectl delete deployment nginx-deployment --cascade=background
```

**Using the Kubernetes API**

1. Start a local proxy session:

    ```shell
    kubectl proxy --port=8080
    ```

1. Use `curl` to trigger deletion:

    ```shell
    curl -X DELETE localhost:8080/apis/apps/v1/namespaces/default/deployments/nginx-deployment \
        -d '{"kind":"DeleteOptions","apiVersion":"v1","propagationPolicy":"Background"}' \
        -H "Content-Type: application/json"
    ```

    The output is similar to this:

    ```
    "kind": "Status",
    "apiVersion": "v1",
    ...
    "status": "Success",
    "details": {
        "name": "nginx-deployment",
        "group": "apps",
        "kind": "deployments",
        "uid": "cc9eefb9-2d49-4445-b1c1-d261c9396456"
    }
    ```
{{% /tab %}}
{{% tab name="Versions prior to Kubernetes 1.20.x" %}}
Kubernetes uses background cascading deletion by default, and does so
even if you run the following commands without the `--cascade` flag or the
`propagationPolicy: Background` argument.

For details, read the [documentation for your Kubernetes version](/docs/home/supported-doc-versions/).

**Using kubectl**

Run the following command:

```shell
kubectl delete deployment nginx-deployment --cascade=true
```

**Using the Kubernetes API**

1. Start a local proxy session:

    ```shell
    kubectl proxy --port=8080
    ```

1. Use `curl` to trigger deletion:

    ```shell
    curl -X DELETE localhost:8080/apis/apps/v1/namespaces/default/deployments/nginx-deployment \
        -d '{"kind":"DeleteOptions","apiVersion":"v1","propagationPolicy":"Background"}' \
        -H "Content-Type: application/json"
    ```

    The output is similar to this:

    ```
    "kind": "Status",
    "apiVersion": "v1",
    ...
    "status": "Success",
    "details": {
        "name": "nginx-deployment",
        "group": "apps",
        "kind": "deployments",
        "uid": "cc9eefb9-2d49-4445-b1c1-d261c9396456"
    }
    ```
{{% /tab %}}
{{</tabs>}}


## Delete owner objects and orphan dependents {#set-orphan-deletion-policy}

By default, when you tell Kubernetes to delete an object, the
{{<glossary_tooltip text="controller" term_id="controller">}} also deletes
dependent objects. You can make Kubernetes *orphan* these dependents using
`kubectl` or the Kubernetes API, depending on the Kubernetes version your
cluster runs. {{<version-check>}}

{{<tabs name="orphan_objects">}}
{{% tab name="Kubernetes version 1.20.x and later" %}}

**Using kubectl**

Run the following command:

```shell
kubectl delete deployment nginx-deployment --cascade=orphan
```

**Using the Kubernetes API**

1. Start a local proxy session:

    ```shell
    kubectl proxy --port=8080
    ```

1. Use `curl` to trigger deletion:

    ```shell
    curl -X DELETE localhost:8080/apis/apps/v1/namespaces/default/deployments/nginx-deployment \
        -d '{"kind":"DeleteOptions","apiVersion":"v1","propagationPolicy":"Orphan"}' \
        -H "Content-Type: application/json"
    ```

    The output contains `orphan` in the `finalizers` field, similar to this:

    ```
    "kind": "Deployment",
    "apiVersion": "apps/v1",
    "namespace": "default",
    "uid": "6f577034-42a0-479d-be21-78018c466f1f",
    "creationTimestamp": "2021-07-09T16:46:37Z",
    "deletionTimestamp": "2021-07-09T16:47:08Z",
    "deletionGracePeriodSeconds": 0,
    "finalizers": [
      "orphan"
    ],
    ...
    ```

{{% /tab %}}
{{% tab name="Versions prior to Kubernetes 1.20.x" %}}

For details, read the [documentation for your Kubernetes version](/docs/home/supported-doc-versions/).

**Using kubectl**

Run the following command:

```shell
kubectl delete deployment nginx-deployment --cascade=false
```

**Using the Kubernetes API**

1. Start a local proxy session:

    ```shell
    kubectl proxy --port=8080
    ```

1. Use `curl` to trigger deletion:

    ```shell
    curl -X DELETE localhost:8080/apis/apps/v1/namespaces/default/deployments/nginx-deployment \
        -d '{"kind":"DeleteOptions","apiVersion":"v1","propagationPolicy":"Orphan"}' \
        -H "Content-Type: application/json"
    ```

    The output contains `orphan` in the `finalizers` field, similar to this:

    ```
    "kind": "Deployment",
    "apiVersion": "apps/v1",
    "namespace": "default",
    "uid": "6f577034-42a0-479d-be21-78018c466f1f",
    "creationTimestamp": "2021-07-09T16:46:37Z",
    "deletionTimestamp": "2021-07-09T16:47:08Z",
    "deletionGracePeriodSeconds": 0,
    "finalizers": [
      "orphan"
    ],
    ...
    ```
{{% /tab %}}
{{</tabs>}}

You can check that the Pods managed by the Deployment are still running:

```shell
kubectl get pods -l app=nginx
```

## {{% heading "whatsnext" %}}

* Learn about [owners and dependents](/docs/concepts/overview/working-with-objects/owners-dependents/) in Kubernetes.
* Learn about Kubernetes [finalizers](/docs/concepts/overview/working-with-objects/finalizers/).
* Learn about [garbage collection](/docs/concepts/workloads/controllers/garbage-collection/).