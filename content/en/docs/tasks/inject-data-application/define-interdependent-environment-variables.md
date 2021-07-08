---
title: Define Dependent Environment Variables
content_type: task
weight: 20
---

<!-- overview -->

This page shows how to define dependent environment variables for a container
in a Kubernetes Pod.


## {{% heading "prerequisites" %}}


{{< include "task-tutorial-prereqs.md" >}}


<!-- steps -->

## Define an environment dependent variable for a container

When you create a Pod, you can set dependent environment variables for the containers that run in the Pod. To set dependent environment variables, you can use $(VAR_NAME) in the `value` of `env` in the configuration file.

In this exercise, you create a Pod that runs one container. The configuration
file for the Pod defines an dependent environment variable with common usage defined. Here is the configuration manifest for the
Pod:

{{< codenew file="pods/inject/dependent-envars.yaml" >}}

1. Create a Pod based on that manifest:

    ```shell
    kubectl apply -f https://k8s.io/examples/pods/inject/dependent-envars.yaml
    ```
    ```
    pod/dependent-envars-demo created
    ```

2. List the running Pods:

    ```shell
    kubectl get pods dependent-envars-demo
    ```
    ```
    NAME                      READY     STATUS    RESTARTS   AGE
    dependent-envars-demo     1/1       Running   0          9s
    ```

3. Check the logs for the container running in your Pod:

    ```shell
    kubectl logs pod/dependent-envars-demo
    ```
    ```

    UNCHANGED_REFERENCE=$(PROTOCOL)://172.17.0.1:80
    SERVICE_ADDRESS=https://172.17.0.1:80
    ESCAPED_REFERENCE=$(PROTOCOL)://172.17.0.1:80
    ```

As shown above, you have defined the correct dependency reference of `SERVICE_ADDRESS`, bad dependency reference of `UNCHANGED_REFERENCE` and skip dependent references of `ESCAPED_REFERENCE`.

When an environment variable is already defined when being referenced,
the reference can be correctly resolved, such as in the `SERVICE_ADDRESS` case.

When the environment variable is undefined or only includes some variables, the undefined environment variable is treated as a normal string, such as `UNCHANGED_REFERENCE`. Note that incorrectly parsed environment variables, in general, will not block the container from starting.

The `$(VAR_NAME)` syntax can be escaped with a double `$`, ie: `$$(VAR_NAME)`.
Escaped references are never expanded, regardless of whether the referenced variable
is defined or not. This can be seen from the `ESCAPED_REFERENCE` case above.

## {{% heading "whatsnext" %}}


* Learn more about [environment variables](/docs/tasks/inject-data-application/environment-variable-expose-pod-information/).
* See {{< api-reference page="workload-resources/pod-v1" anchor="EnvVarSource" >}}.

