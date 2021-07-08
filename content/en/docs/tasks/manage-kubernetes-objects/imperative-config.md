---
title: Imperative Management of Kubernetes Objects Using Configuration Files
content_type: task
weight: 40
---

<!-- overview -->
Kubernetes objects can be created, updated, and deleted by using the `kubectl`
command-line tool along with an object configuration file written in YAML or JSON.
This document explains how to define and manage objects using configuration files.


## {{% heading "prerequisites" %}}


Install [`kubectl`](/docs/tasks/tools/).

{{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}



<!-- steps -->

## Trade-offs

The `kubectl` tool supports three kinds of object management:

* Imperative commands
* Imperative object configuration
* Declarative object configuration

See [Kubernetes Object Management](/docs/concepts/overview/working-with-objects/object-management/)
for a discussion of the advantages and disadvantage of each kind of object management.

## How to create objects

You can use `kubectl create -f` to create an object from a configuration file.
Refer to the [kubernetes API reference](/docs/reference/kubernetes-api/)
for details.

* `kubectl create -f <filename|url>`

## How to update objects

{{< warning >}}
Updating objects with the `replace` command drops all
parts of the spec not specified in the configuration file.  This
should not be used with objects whose specs are partially managed
by the cluster, such as Services of type `LoadBalancer`, where
the `externalIPs` field is managed independently from the configuration
file.  Independently managed fields must be copied to the configuration
file to prevent `replace` from dropping them.
{{< /warning >}}

You can use `kubectl replace -f` to update a live object according to a
configuration file.

* `kubectl replace -f <filename|url>`

## How to delete objects

You can use `kubectl delete -f` to delete an object that is described in a
configuration file.

* `kubectl delete -f <filename|url>`

{{< note >}}
If configuration file has specified the `generateName` field in the `metadata`
section instead of the `name` field, you cannot delete the object using
`kubectl delete -f <filename|url>`.
You will have to use other flags for deleting the object. For example:

```shell
kubectl delete <type> <name>
kubectl delete <type> -l <label>
```
{{< /note >}}

## How to view an object

You can use `kubectl get -f` to view information about an object that is
described in a configuration file.

* `kubectl get -f <filename|url> -o yaml`

The `-o yaml` flag specifies that the full object configuration is printed.
Use `kubectl get -h` to see a list of options.

## Limitations

The `create`, `replace`, and `delete` commands work well when each object's
configuration is fully defined and recorded in its configuration
file. However when a live object is updated, and the updates are not merged
into its configuration file, the updates will be lost the next time a `replace`
is executed. This can happen if a controller, such as
a HorizontalPodAutoscaler, makes updates directly to a live object. Here's
an example:

1. You create an object from a configuration file.
1. Another source updates the object by changing some field.
1. You replace the object from the configuration file. Changes made by
the other source in step 2 are lost.

If you need to support multiple writers to the same object, you can use
`kubectl apply` to manage the object.

## Creating and editing an object from a URL without saving the configuration

Suppose you have the URL of an object configuration file. You can use
`kubectl create --edit` to make changes to the configuration before the
object is created. This is particularly useful for tutorials and tasks
that point to a configuration file that could be modified by the reader.

```shell
kubectl create -f <url> --edit
```

## Migrating from imperative commands to imperative object configuration

Migrating from imperative commands to imperative object configuration involves
several manual steps.

1. Export the live object to a local object configuration file:

    ```shell
    kubectl get <kind>/<name> -o yaml > <kind>_<name>.yaml
    ```

1. Manually remove the status field from the object configuration file.

1. For subsequent object management, use `replace` exclusively.

    ```shell
    kubectl replace -f <kind>_<name>.yaml
    ```

## Defining controller selectors and PodTemplate labels

{{< warning >}}
Updating selectors on controllers is strongly discouraged.
{{< /warning >}}

The recommended approach is to define a single, immutable PodTemplate label
used only by the controller selector with no other semantic meaning.

Example label:

```yaml
selector:
  matchLabels:
      controller-selector: "apps/v1/deployment/nginx"
template:
  metadata:
    labels:
      controller-selector: "apps/v1/deployment/nginx"
```



## {{% heading "whatsnext" %}}


* [Managing Kubernetes Objects Using Imperative Commands](/docs/tasks/manage-kubernetes-objects/imperative-command/)
* [Managing Kubernetes Objects Using Object Configuration (Declarative)](/docs/tasks/manage-kubernetes-objects/declarative-config/)
* [Kubectl Command Reference](/docs/reference/generated/kubectl/kubectl-commands/)
* [Kubernetes API Reference](/docs/reference/kubernetes-api/)


