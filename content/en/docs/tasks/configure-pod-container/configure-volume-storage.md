---
title: Configure a Pod to Use a Volume for Storage
content_type: task
weight: 50
---

<!-- overview -->

This page shows how to configure a Pod to use a Volume for storage.

A Container's file system lives only as long as the Container does. So when a
Container terminates and restarts, filesystem changes are lost. For more
consistent storage that is independent of the Container, you can use a
[Volume](/docs/concepts/storage/volumes/). This is especially important for stateful
applications, such as key-value stores (such as Redis) and databases. 



## {{% heading "prerequisites" %}}


{{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}



<!-- steps -->

## Configure a volume for a Pod

In this exercise, you create a Pod that runs one Container. This Pod has a
Volume of type
[emptyDir](/docs/concepts/storage/volumes/#emptydir)
that lasts for the life of the Pod, even if the Container terminates and
restarts. Here is the configuration file for the Pod:

{{< codenew file="pods/storage/redis.yaml" >}}

1. Create the Pod:

    ```shell
    kubectl apply -f https://k8s.io/examples/pods/storage/redis.yaml
    ```

1. Verify that the Pod's Container is running, and then watch for changes to
the Pod:

    ```shell
    kubectl get pod redis --watch
    ```
    
    The output looks like this:

    ```shell
    NAME      READY     STATUS    RESTARTS   AGE
    redis     1/1       Running   0          13s
    ```

1. In another terminal, get a shell to the running Container:

    ```shell
    kubectl exec -it redis -- /bin/bash
    ```

1. In your shell, go to `/data/redis`, and then create a file:

    ```shell
    root@redis:/data# cd /data/redis/
    root@redis:/data/redis# echo Hello > test-file
    ```

1. In your shell, list the running processes:

    ```shell
    root@redis:/data/redis# apt-get update
    root@redis:/data/redis# apt-get install procps
    root@redis:/data/redis# ps aux
    ```

    The output is similar to this:

    ```shell
    USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
    redis        1  0.1  0.1  33308  3828 ?        Ssl  00:46   0:00 redis-server *:6379
    root        12  0.0  0.0  20228  3020 ?        Ss   00:47   0:00 /bin/bash
    root        15  0.0  0.0  17500  2072 ?        R+   00:48   0:00 ps aux
    ```

1. In your shell, kill the Redis process:

    ```shell
    root@redis:/data/redis# kill <pid>
    ```

    where `<pid>` is the Redis process ID (PID).

1. In your original terminal, watch for changes to the Redis Pod. Eventually,
you will see something like this:

    ```shell
    NAME      READY     STATUS     RESTARTS   AGE
    redis     1/1       Running    0          13s
    redis     0/1       Completed  0         6m
    redis     1/1       Running    1         6m
    ```

At this point, the Container has terminated and restarted. This is because the
Redis Pod has a {{< api-reference page="workload-resources/pod-v1" anchor="Lifecycle" text="restartPolicy" >}} of `Always`.

1. Get a shell into the restarted Container:

    ```shell
    kubectl exec -it redis -- /bin/bash
    ```

1. In your shell, go to `/data/redis`, and verify that `test-file` is still there.
    ```shell
    root@redis:/data/redis# cd /data/redis/
    root@redis:/data/redis# ls
    test-file
    ```

1. Delete the Pod that you created for this exercise:

    ```shell
    kubectl delete pod redis
    ```



## {{% heading "whatsnext" %}}


* See {{< api-reference page="config-and-storage-resources/volume" >}}.

* See {{< api-reference page="workload-resources/pod-v1" >}}.

* In addition to the local disk storage provided by `emptyDir`, Kubernetes
supports many different network-attached storage solutions, including PD on
GCE and EBS on EC2, which are preferred for critical data and will handle
details such as mounting and unmounting the devices on the nodes. See
[Volumes](/docs/concepts/storage/volumes/) for more details.




