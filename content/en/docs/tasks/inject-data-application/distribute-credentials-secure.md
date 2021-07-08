---
title: Distribute Credentials Securely Using Secrets
content_type: task
weight: 50
min-kubernetes-server-version: v1.6
---

<!-- overview -->
This page shows how to securely inject sensitive data, such as passwords and
encryption keys, into Pods.


## {{% heading "prerequisites" %}}


{{< include "task-tutorial-prereqs.md" >}}

### Convert your secret data to a base-64 representation

Suppose you want to have two pieces of secret data: a username `my-app` and a password
`39528$vdg7Jb`. First, use a base64 encoding tool to convert your username and password to a base64 representation. Here's an example using the commonly available base64 program:

```shell
echo -n 'my-app' | base64
echo -n '39528$vdg7Jb' | base64
```

The output shows that the base-64 representation of your username is `bXktYXBw`,
and the base-64 representation of your password is `Mzk1MjgkdmRnN0pi`.

{{< caution >}}
Use a local tool trusted by your OS to decrease the security risks of external tools.
{{< /caution >}}

<!-- steps -->

## Create a Secret

Here is a configuration file you can use to create a Secret that holds your
username and password:

{{< codenew file="pods/inject/secret.yaml" >}}

1. Create the Secret

    ```shell
    kubectl apply -f https://k8s.io/examples/pods/inject/secret.yaml
    ```

1. View information about the Secret:

    ```shell
    kubectl get secret test-secret
    ```

    Output:

    ```
    NAME          TYPE      DATA      AGE
    test-secret   Opaque    2         1m
    ```

1. View more detailed information about the Secret:

    ```shell
    kubectl describe secret test-secret
    ```

    Output:

    ```
    Name:       test-secret
    Namespace:  default
    Labels:     <none>
    Annotations:    <none>

    Type:   Opaque

    Data
    ====
    password:   13 bytes
    username:   7 bytes
    ```

### Create a Secret directly with kubectl

If you want to skip the Base64 encoding step, you can create the
same Secret using the `kubectl create secret` command. For example:

```shell
kubectl create secret generic test-secret --from-literal='username=my-app' --from-literal='password=39528$vdg7Jb'
```

This is more convenient. The detailed approach shown earlier runs
through each step explicitly to demonstrate what is happening.


## Create a Pod that has access to the secret data through a Volume

Here is a configuration file you can use to create a Pod:

{{< codenew file="pods/inject/secret-pod.yaml" >}}

1. Create the Pod:

   ```shell
   kubectl apply -f https://k8s.io/examples/pods/inject/secret-pod.yaml
   ```

1. Verify that your Pod is running:

   ```shell
   kubectl get pod secret-test-pod
   ```

   Output:
   ```
   NAME              READY     STATUS    RESTARTS   AGE
   secret-test-pod   1/1       Running   0          42m
   ```

1. Get a shell into the Container that is running in your Pod:
   ```shell
   kubectl exec -i -t secret-test-pod -- /bin/bash
   ```

1. The secret data is exposed to the Container through a Volume mounted under
`/etc/secret-volume`.

   In your shell, list the files in the `/etc/secret-volume` directory:
   ```shell
   # Run this in the shell inside the container
   ls /etc/secret-volume
   ```
   The output shows two files, one for each piece of secret data:
   ```
   password username
   ```

1. In your shell, display the contents of the `username` and `password` files:
   ```shell
   # Run this in the shell inside the container
   echo "$( cat /etc/secret-volume/username )"
   echo "$( cat /etc/secret-volume/password )"
   ```
   The output is your username and password:
   ```
   my-app
   39528$vdg7Jb
   ```

## Define container environment variables using Secret data

### Define a container environment variable with data from a single Secret

*  Define an environment variable as a key-value pair in a Secret:

   ```shell
   kubectl create secret generic backend-user --from-literal=backend-username='backend-admin'
   ```

*  Assign the `backend-username` value defined in the Secret to the `SECRET_USERNAME` environment variable in the Pod specification.

   {{< codenew file="pods/inject/pod-single-secret-env-variable.yaml" >}}

*  Create the Pod:

   ```shell
   kubectl create -f https://k8s.io/examples/pods/inject/pod-single-secret-env-variable.yaml
   ```

*  In your shell, display the content of `SECRET_USERNAME` container environment variable

   ```shell
   kubectl exec -i -t env-single-secret -- /bin/sh -c 'echo $SECRET_USERNAME'
   ```

   The output is
   ```
   backend-admin
   ```

### Define container environment variables with data from multiple Secrets

*  As with the previous example, create the Secrets first.

   ```shell
   kubectl create secret generic backend-user --from-literal=backend-username='backend-admin'
   kubectl create secret generic db-user --from-literal=db-username='db-admin'
   ```

*  Define the environment variables in the Pod specification.

   {{< codenew file="pods/inject/pod-multiple-secret-env-variable.yaml" >}}

*  Create the Pod:

   ```shell
   kubectl create -f https://k8s.io/examples/pods/inject/pod-multiple-secret-env-variable.yaml
   ```

*  In your shell, display the container environment variables

   ```shell
   kubectl exec -i -t envvars-multiple-secrets -- /bin/sh -c 'env | grep _USERNAME'
   ```
   The output is
   ```
   DB_USERNAME=db-admin
   BACKEND_USERNAME=backend-admin
   ```


## Configure all key-value pairs in a Secret as container environment variables

{{< note >}}
This functionality is available in Kubernetes v1.6 and later.
{{< /note >}}

*  Create a Secret containing multiple key-value pairs

   ```shell
   kubectl create secret generic test-secret --from-literal=username='my-app' --from-literal=password='39528$vdg7Jb'
   ```

*  Use envFrom to define all of the Secret's data as container environment variables. The key from the Secret becomes the environment variable name in the Pod.

    {{< codenew file="pods/inject/pod-secret-envFrom.yaml" >}}

*  Create the Pod:

   ```shell
   kubectl create -f https://k8s.io/examples/pods/inject/pod-secret-envFrom.yaml
   ```

* In your shell, display `username` and `password` container environment variables

  ```shell
  kubectl exec -i -t envfrom-secret -- /bin/sh -c 'echo "username: $username\npassword: $password\n"'
  ```

  The output is
  ```
  username: my-app
  password: 39528$vdg7Jb
  ```

### References

* {{< api-reference page="config-and-storage-resources/secret-v1" >}}
* {{< api-reference page="config-and-storage-resources/volume" >}}
* {{< api-reference page="workload-resources/pod-v1" >}}

## {{% heading "whatsnext" %}}

* Learn more about [Secrets](/docs/concepts/configuration/secret/).
* Learn about [Volumes](/docs/concepts/storage/volumes/).
