---
title: Set up Ingress on Minikube with the NGINX Ingress Controller
content_type: task
weight: 100
---

<!-- overview -->

An [Ingress](/docs/concepts/services-networking/ingress/) is an API object that defines rules which allow external access
to services in a cluster. An [Ingress controller](/docs/concepts/services-networking/ingress-controllers/) fulfills the rules set in the Ingress.

This page shows you how to set up a simple Ingress which routes requests to Service web or web2 depending on the HTTP URI.



## {{% heading "prerequisites" %}}


{{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}



<!-- steps -->

## Create a Minikube cluster

1. Click **Launch Terminal**

    {{< kat-button >}}

1. (Optional) If you installed Minikube locally, run the following command:

    ```shell
    minikube start
    ```

## Enable the Ingress controller

1. To enable the NGINX Ingress controller, run the following command:

    ```shell
    minikube addons enable ingress
    ```

1. Verify that the NGINX Ingress controller is running

    ```shell
    kubectl get pods -n kube-system
    ```

    {{< note >}}This can take up to a minute.{{< /note >}}

    Output:

    ```shell
    NAME                                        READY     STATUS    RESTARTS   AGE
    default-http-backend-59868b7dd6-xb8tq       1/1       Running   0          1m
    kube-addon-manager-minikube                 1/1       Running   0          3m
    kube-dns-6dcb57bcc8-n4xd4                   3/3       Running   0          2m
    kubernetes-dashboard-5498ccf677-b8p5h       1/1       Running   0          2m
    nginx-ingress-controller-5984b97644-rnkrg   1/1       Running   0          1m
    storage-provisioner                         1/1       Running   0          2m
    ```

## Deploy a hello, world app

1. Create a Deployment using the following command:

    ```shell
    kubectl create deployment web --image=gcr.io/google-samples/hello-app:1.0
    ```

    Output:

    ```shell
    deployment.apps/web created
    ```

1. Expose the Deployment:

    ```shell
    kubectl expose deployment web --type=NodePort --port=8080
    ```

    Output:

    ```shell
    service/web exposed
    ```

1. Verify the Service is created and is available on a node port:

    ```shell
    kubectl get service web
    ```

    Output:

    ```shell
    NAME      TYPE       CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
    web       NodePort   10.104.133.249   <none>        8080:31637/TCP   12m
    ```

1. Visit the service via NodePort:

    ```shell
    minikube service web --url
    ```

    Output:

    ```shell
    http://172.17.0.15:31637
    ```

    {{< note >}}Katacoda environment only: at the top of the terminal panel, click the plus sign, and then click **Select port to view on Host 1**. Enter the NodePort, in this case `31637`, and then click **Display Port**.{{< /note >}}

    Output:

    ```shell
    Hello, world!
    Version: 1.0.0
    Hostname: web-55b8c6998d-8k564
    ```

    You can now access the sample app via the Minikube IP address and NodePort. The next step lets you access
    the app using the Ingress resource.

## Create an Ingress resource

The following file is an Ingress resource that sends traffic to your Service via hello-world.info.

1. Create the Ingress resource by running the following command:

    ```shell
    kubectl apply -f https://k8s.io/examples/service/networking/example-ingress.yaml
    ```

    Output:

    ```shell
    ingress.networking.k8s.io/example-ingress created
    ```

1. Verify the IP address is set:

    ```shell
    kubectl get ingress
    ```

    {{< note >}}This can take a couple of minutes.{{< /note >}}

    ```shell
    NAME              CLASS    HOSTS              ADDRESS        PORTS   AGE
    example-ingress   <none>   hello-world.info   172.17.0.15    80      38s
    ```

1. Add the following line to the bottom of the `/etc/hosts` file.

    {{< note >}}If you are running Minikube locally, use `minikube ip` to get the external IP. The IP address displayed within the ingress list will be the internal IP.{{< /note >}}

    ```
    172.17.0.15 hello-world.info
    ```

    This sends requests from hello-world.info to Minikube.

1. Verify that the Ingress controller is directing traffic:

    ```shell
    curl hello-world.info
    ```

    Output:

    ```shell
    Hello, world!
    Version: 1.0.0
    Hostname: web-55b8c6998d-8k564
    ```

    {{< note >}}If you are running Minikube locally, you can visit hello-world.info from your browser.{{< /note >}}

## Create Second Deployment

1. Create a v2 Deployment using the following command:

    ```shell
    kubectl create deployment web2 --image=gcr.io/google-samples/hello-app:2.0
    ```
    Output:

    ```shell
    deployment.apps/web2 created
    ```

1. Expose the Deployment:

    ```shell
    kubectl expose deployment web2 --port=8080 --type=NodePort
    ```

    Output:

    ```shell
    service/web2 exposed
    ```

## Edit Ingress

1. Edit the existing `example-ingress.yaml` and add the following lines:

    ```yaml
          - path: /v2
            pathType: Prefix
            backend:
              service:
                name: web2
                port:
                  number: 8080
    ```

1. Apply the changes:

    ```shell
    kubectl apply -f example-ingress.yaml
    ```

    Output:

    ```shell
    ingress.networking/example-ingress configured
    ```

## Test Your Ingress

1. Access the 1st version of the Hello World app.

    ```shell
    curl hello-world.info
    ```

    Output:

    ```shell
    Hello, world!
    Version: 1.0.0
    Hostname: web-55b8c6998d-8k564
    ```

1. Access the 2nd version of the Hello World app.

    ```shell
    curl hello-world.info/v2
    ```

    Output:

    ```shell
    Hello, world!
    Version: 2.0.0
    Hostname: web2-75cd47646f-t8cjk
    ```

    {{< note >}}If you are running Minikube locally, you can visit hello-world.info and hello-world.info/v2 from your browser.{{< /note >}}




## {{% heading "whatsnext" %}}

* Read more about [Ingress](/docs/concepts/services-networking/ingress/)
* Read more about [Ingress Controllers](/docs/concepts/services-networking/ingress-controllers/)
* Read more about [Services](/docs/concepts/services-networking/service/)



