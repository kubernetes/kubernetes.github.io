---
title: Expose Pod Information to Containers Through Environment Variables
content_type: task
weight: 30
---

<!-- overview -->

This page shows how a Pod can use environment variables to expose information
about itself to Containers running in the Pod. Environment variables can expose
Pod fields and Container fields.




## {{% heading "prerequisites" %}}


{{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}




<!-- steps -->

## The Downward API

There are two ways to expose Pod and Container fields to a running Container:

* Environment variables
* [Volume Files](/docs/tasks/inject-data-application/downward-api-volume-expose-pod-information/#the-downward-api)

Together, these two ways of exposing Pod and Container fields are called the
*Downward API*.


## Use Pod fields as values for environment variables

In this exercise, you create a Pod that has one Container. Here is the
configuration file for the Pod:

{{< codenew file="pods/inject/dapi-envars-pod.yaml" >}}

In the configuration file, you can see five environment variables. The `env`
field is an array of {{< api-reference page="workload-resources/pod-v1" anchor="EnvVar" text="EnvVars" >}}.
The first element in the array specifies that the `MY_NODE_NAME` environment
variable gets its value from the Pod's `spec.nodeName` field. Similarly, the
other environment variables get their names from Pod fields.

{{< note >}}
The fields in this example are Pod fields. They are not fields of the
Container in the Pod.
{{< /note >}}

Create the Pod:

```shell
kubectl apply -f https://k8s.io/examples/pods/inject/dapi-envars-pod.yaml
```

Verify that the Container in the Pod is running:

```shell
kubectl get pods
```

View the Container's logs:

```shell
kubectl logs dapi-envars-fieldref
```

The output shows the values of selected environment variables:

```
minikube
dapi-envars-fieldref
default
172.17.0.4
default
```

To see why these values are in the log, look at the `command` and `args` fields
in the configuration file. When the Container starts, it writes the values of
five environment variables to stdout. It repeats this every ten seconds.

Next, get a shell into the Container that is running in your Pod:

```shell
kubectl exec -it dapi-envars-fieldref -- sh
```

In your shell, view the environment variables:

```shell
/# printenv
```

The output shows that certain environment variables have been assigned the
values of Pod fields:

```
MY_POD_SERVICE_ACCOUNT=default
...
MY_POD_NAMESPACE=default
MY_POD_IP=172.17.0.4
...
MY_NODE_NAME=minikube
...
MY_POD_NAME=dapi-envars-fieldref
```

## Use Container fields as values for environment variables

In the preceding exercise, you used Pod fields as the values for environment
variables. In this next exercise, you use Container fields as the values for
environment variables. Here is the configuration file for a Pod that has one
container:

{{< codenew file="pods/inject/dapi-envars-container.yaml" >}}

In the configuration file, you can see four environment variables. The `env`
field is an array of {{< api-reference page="workload-resources/pod-v1" anchor="EnvVar" text="EnvVars" >}}.
The first element in the array specifies that the `MY_CPU_REQUEST` environment
variable gets its value from the `requests.cpu` field of a Container named
`test-container`. Similarly, the other environment variables get their values
from Container fields.

Create the Pod:

```shell
kubectl apply -f https://k8s.io/examples/pods/inject/dapi-envars-container.yaml
```

Verify that the Container in the Pod is running:

```shell
kubectl get pods
```

View the Container's logs:

```shell
kubectl logs dapi-envars-resourcefieldref
```

The output shows the values of selected environment variables:

```
1
1
33554432
67108864
```



## {{% heading "whatsnext" %}}


* [Defining Environment Variables for a Container](/docs/tasks/inject-data-application/define-environment-variable-container/)
* {{< api-reference page="workload-resources/pod-v1" anchor="PodSpec" >}}
* {{< api-reference page="workload-resources/pod-v1" anchor="Container" >}}
* {{< api-reference page="workload-resources/pod-v1" anchor="EnvVar" >}}
* {{< api-reference page="workload-resources/pod-v1" anchor="EnvVarSource" >}}
* {{< api-reference page="common-definitions/object-field-selector" >}}
* {{< api-reference page="common-definitions/resource-field-selector" >}}



