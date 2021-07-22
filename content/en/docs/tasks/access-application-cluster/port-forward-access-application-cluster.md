---
title: Use Port Forwarding to Access Applications in a Cluster
content_type: task
weight: 40
min-kubernetes-server-version: v1.10
---

<!-- overview -->

This page shows how to use `kubectl port-forward` to connect to a MongoDB
server running in a Kubernetes cluster. This type of connection can be useful
for database debugging.




## {{% heading "prerequisites" %}}


* {{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}

* Install [MongoDB Shell](https://www.mongodb.com/try/download/shell).




<!-- steps -->

## Creating MongoDB deployment and service

1. Create a Deployment that runs MongoDB:

    ```shell
    kubectl apply -f https://k8s.io/examples/application/mongodb/mongo-deployment.yaml
    ```

    The output of a successful command verifies that the deployment was created:

    ```
    deployment.apps/mongo created
    ```

    View the pod status to check that it is ready:

    ```shell
    kubectl get pods
    ```

    The output displays the pod created:

    ```
    NAME                     READY   STATUS    RESTARTS   AGE
    mongo-75f59d57f4-4nd6q   1/1     Running   0          2m4s
    ```

    View the Deployment's status:

    ```shell
    kubectl get deployment
    ```

    The output displays that the Deployment was created:

    ```
    NAME    READY   UP-TO-DATE   AVAILABLE   AGE
    mongo   1/1     1            1           2m21s
    ```

    The Deployment automatically manages a ReplicaSet.
    View the ReplicaSet status using:

    ```shell
    kubectl get replicaset
    ```

    The output displays that the ReplicaSet was created:

    ```
    NAME               DESIRED   CURRENT   READY   AGE
    mongo-75f59d57f4   1         1         1       3m12s
    ```


2. Create a Service to expose MongoDB on the network:

    ```shell
    kubectl apply -f https://k8s.io/examples/application/mongodb/mongo-service.yaml
    ```

    The output of a successful command verifies that the Service was created:

    ```
    service/mongo created
    ```

    Check the Service created:

    ```shell
    kubectl get service mongo
    ```

    The output displays the service created:

    ```
    NAME    TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)     AGE
    mongo   ClusterIP   10.96.41.183   <none>        27017/TCP   11s
    ```

3. Verify that the MongoDB server is running in the Pod, and listening on port 27017:

    ```shell
    # Change mongo-75f59d57f4-4nd6q to the name of the Pod
    kubectl get pod mongo-75f59d57f4-4nd6q --template='{{(index (index .spec.containers 0).ports 0).containerPort}}{{"\n"}}'
    ```

    The output displays the port for MongoDB in that Pod:

    ```
    27017
    ```

    (this is the TCP port allocated to MongoDB on the internet).

## Forward a local port to a port on the Pod

1.  `kubectl port-forward` allows using resource name, such as a pod name, to select a matching pod to port forward to.


    ```shell
    # Change mongo-75f59d57f4-4nd6q to the name of the Pod
    kubectl port-forward mongo-75f59d57f4-4nd6q 28015:27017
    ```

    which is the same as

    ```shell
    kubectl port-forward pods/mongo-75f59d57f4-4nd6q 28015:27017
    ```

    or

    ```shell
    kubectl port-forward deployment/mongo 28015:27017
    ```

    or

    ```shell
    kubectl port-forward replicaset/mongo-75f59d57f4 28015:27017
    ```

    or

    ```shell
    kubectl port-forward service/mongo 28015:27017
    ```

    Any of the above commands works. The output is similar to this:

    ```
    Forwarding from 127.0.0.1:28015 -> 27017
    Forwarding from [::1]:28015 -> 27017
    ```

{{< note >}}

`kubectl port-forward` does not return. To continue with the exercises, you will need to open another terminal.

{{< /note >}}

2.  Start the MongoDB command line interface:

    ```shell
    mongosh --port 28015
    ```

3.  At the MongoDB command line prompt, enter the `ping` command:

    ```
    db.runCommand( { ping: 1 } )
    ```

    A successful ping request returns:

    ```
    { ok: 1 }
    ```

### Optionally let _kubectl_ choose the local port {#let-kubectl-choose-local-port}

If you don't need a specific local port, you can let `kubectl` choose and allocate 
the local port and thus relieve you from having to manage local port conflicts, with 
the slightly simpler syntax:

```shell
kubectl port-forward deployment/mongo :27017
```

The `kubectl` tool finds a local port number that is not in use (avoiding low ports numbers,
because these might be used by other applications). The output is similar to:

```
Forwarding from 127.0.0.1:63753 -> 27017
Forwarding from [::1]:63753 -> 27017
```


<!-- discussion -->

## Discussion

Connections made to local port 28015 are forwarded to port 27017 of the Pod that
is running the MongoDB server. With this connection in place, you can use your
local workstation to debug the database that is running in the Pod.

{{< note >}}
`kubectl port-forward` is implemented for TCP ports only.
The support for UDP protocol is tracked in
[issue 47862](https://github.com/kubernetes/kubernetes/issues/47862).
{{< /note >}}




## {{% heading "whatsnext" %}}

Learn more about [kubectl port-forward](/docs/reference/generated/kubectl/kubectl-commands/#port-forward).
