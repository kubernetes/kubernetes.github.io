---
title: Define a Command and Arguments for a Container
content_type: task
weight: 10
---

<!-- overview -->

This page shows how to define commands and arguments when you run a container
in a {{< glossary_tooltip term_id="pod" >}}.




## {{% heading "prerequisites" %}}


{{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}




<!-- steps -->

## Define a command and arguments when you create a Pod

When you create a Pod, you can define a command and arguments for the
containers that run in the Pod. To define a command, include the `command`
field in the configuration file. To define arguments for the command, include
the `args` field in the configuration file. The command and arguments that
you define cannot be changed after the Pod is created.

The command and arguments that you define in the configuration file
override the default command and arguments provided by the container image.
If you define args, but do not define a command, the default command is used
with your new arguments.

{{< note >}}
The `command` field corresponds to `entrypoint` in some container
runtimes. Refer to the [Notes](#notes) below.
{{< /note >}}

In this exercise, you create a Pod that runs one container. The configuration
file for the Pod defines a command and two arguments:

{{< codenew file="pods/commands.yaml" >}}

1. Create a Pod based on the YAML configuration file:

    ```shell
    kubectl apply -f https://k8s.io/examples/pods/commands.yaml
    ```

1. List the running Pods:

    ```shell
    kubectl get pods
    ```

    The output shows that the container that ran in the command-demo Pod has
    completed.

1. To see the output of the command that ran in the container, view the logs
from the Pod:

    ```shell
    kubectl logs command-demo
    ```

    The output shows the values of the HOSTNAME and KUBERNETES_PORT environment
    variables:

    ```
    command-demo
    tcp://10.3.240.1:443
    ```

## Use environment variables to define arguments

In the preceding example, you defined the arguments directly by
providing strings. As an alternative to providing strings directly,
you can define arguments by using environment variables:

```yaml
env:
- name: MESSAGE
  value: "hello world"
command: ["/bin/echo"]
args: ["$(MESSAGE)"]
```

This means you can define an argument for a Pod using any of
the techniques available for defining environment variables, including
[ConfigMaps](/docs/tasks/configure-pod-container/configure-pod-configmap/)
and
[Secrets](/docs/concepts/configuration/secret/).

{{< note >}}
The environment variable appears in parentheses, `"$(VAR)"`. This is
required for the variable to be expanded in the `command` or `args` field.
{{< /note >}}

## Run a command in a shell

In some cases, you need your command to run in a shell. For example, your
command might consist of several commands piped together, or it might be a shell
script. To run your command in a shell, wrap it like this:

```shell
command: ["/bin/sh"]
args: ["-c", "while true; do echo hello; sleep 10;done"]
```

## Notes

This table summarizes the field names used by Docker and Kubernetes.

|              Description               |    Docker field name   | Kubernetes field name |
|----------------------------------------|------------------------|-----------------------|
|  The command run by the container      |   Entrypoint           |      command          |
|  The arguments passed to the command   |   Cmd                  |      args             |

When you override the default Entrypoint and Cmd, these rules apply:

* If you do not supply `command` or `args` for a Container, the defaults defined
in the Docker image are used.

* If you supply a `command` but no `args` for a Container, only the supplied
`command` is used. The default EntryPoint and the default Cmd defined in the Docker
image are ignored.

* If you supply only `args` for a Container, the default Entrypoint defined in
the Docker image is run with the `args` that you supplied.

* If you supply a `command` and `args`, the default Entrypoint and the default
Cmd defined in the Docker image are ignored. Your `command` is run with your
`args`.

Here are some examples:

| Image Entrypoint   |    Image Cmd     | Container command   |  Container args    |    Command run   |
|--------------------|------------------|---------------------|--------------------|------------------|
|     `[/ep-1]`      |   `[foo bar]`    |   &lt;not set&gt;   |   &lt;not set&gt;  | `[ep-1 foo bar]` |
|     `[/ep-1]`      |   `[foo bar]`    |      `[/ep-2]`      |   &lt;not set&gt;  |     `[ep-2]`     |
|     `[/ep-1]`      |   `[foo bar]`    |   &lt;not set&gt;   |     `[zoo boo]`    | `[ep-1 zoo boo]` |
|     `[/ep-1]`      |   `[foo bar]`    |   `[/ep-2]`         |     `[zoo boo]`    | `[ep-2 zoo boo]` |




## {{% heading "whatsnext" %}}


* Learn more about [configuring pods and containers](/docs/tasks/).
* Learn more about [running commands in a container](/docs/tasks/debug-application-cluster/get-shell-running-container/).
* See {{< api-reference page="workload-resources/pod-v1" anchor="Container" >}}.




