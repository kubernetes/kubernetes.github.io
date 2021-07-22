---
title: "Example: Deploying PHP Guestbook application with Redis"
reviewers:
- ahmetb
- jimangel
content_type: tutorial
weight: 20
card:
  name: tutorials
  weight: 30
  title: "Stateless Example: PHP Guestbook with Redis"
min-kubernetes-server-version: v1.14
source: https://cloud.google.com/kubernetes-engine/docs/tutorials/guestbook
---

<!-- overview -->
This tutorial shows you how to build and deploy a simple _(not production
ready)_, multi-tier web application using Kubernetes and
[Docker](https://www.docker.com/). This example consists of the following
components:

* A single-instance [Redis](https://www.redis.io/) to store guestbook entries
* Multiple web frontend instances

## {{% heading "objectives" %}}

* Start up a Redis leader.
* Start up two Redis followers.
* Start up the guestbook frontend.
* Expose and view the Frontend Service.
* Clean up.

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}}

{{< version-check >}}

<!-- lessoncontent -->

## Start up the Redis Database

The guestbook application uses Redis to store its data.

### Creating the Redis Deployment

The manifest file, included below, specifies a Deployment controller that runs a single replica Redis Pod.

{{< codenew file="application/guestbook/redis-leader-deployment.yaml" >}}

1. Launch a terminal window in the directory you downloaded the manifest files.
1. Apply the Redis Deployment from the `redis-leader-deployment.yaml` file:

   <!---
   for local testing of the content via relative file path
   kubectl apply -f ./content/en/examples/application/guestbook/redis-leader-deployment.yaml
   -->

   ```shell
   kubectl apply -f https://k8s.io/examples/application/guestbook/redis-leader-deployment.yaml
   ```

1. Query the list of Pods to verify that the Redis Pod is running:

   ```shell
   kubectl get pods
   ```

   The response should be similar to this:

   ```
   NAME                           READY   STATUS    RESTARTS   AGE
   redis-leader-fb76b4755-xjr2n   1/1     Running   0          13s
   ```

1. Run the following command to view the logs from the Redis leader Pod:

   ```shell
   kubectl logs -f deployment/redis-leader
   ```

### Creating the Redis leader Service

The guestbook application needs to communicate to the Redis to write its data.
You need to apply a [Service](/docs/concepts/services-networking/service/) to
proxy the traffic to the Redis Pod. A Service defines a policy to access the
Pods.

{{< codenew file="application/guestbook/redis-leader-service.yaml" >}}

1. Apply the Redis Service from the following `redis-leader-service.yaml` file:

   <!---
   for local testing of the content via relative file path
   kubectl apply -f ./content/en/examples/application/guestbook/redis-leader-service.yaml
   -->

   ```shell
   kubectl apply -f https://k8s.io/examples/application/guestbook/redis-leader-service.yaml
   ```

1. Query the list of Services to verify that the Redis Service is running:

   ```shell
   kubectl get service
   ```

   The response should be similar to this:

   ```
   NAME           TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)    AGE
   kubernetes     ClusterIP   10.0.0.1     <none>        443/TCP    1m
   redis-leader   ClusterIP   10.103.78.24 <none>        6379/TCP   16s
   ```

{{< note >}}
This manifest file creates a Service named `redis-leader` with a set of labels
that match the labels previously defined, so the Service routes network
traffic to the Redis Pod.
{{< /note >}}

### Set up Redis followers

Although the Redis leader is a single Pod, you can make it highly available
and meet traffic demands by adding a few Redis followers, or replicas.

{{< codenew file="application/guestbook/redis-follower-deployment.yaml" >}}

1. Apply the Redis Deployment from the following `redis-follower-deployment.yaml` file:

   <!---
   for local testing of the content via relative file path
   kubectl apply -f ./content/en/examples/application/guestbook/redis-follower-deployment.yaml
   -->

   ```shell
   kubectl apply -f https://k8s.io/examples/application/guestbook/redis-follower-deployment.yaml
   ```

1. Verify that the two Redis follower replicas are running by querying the list of Pods:

   ```shell
   kubectl get pods
   ```

   The response should be similar to this:

   ```
   NAME                             READY   STATUS    RESTARTS   AGE
   redis-follower-dddfbdcc9-82sfr   1/1     Running   0          37s
   redis-follower-dddfbdcc9-qrt5k   1/1     Running   0          38s
   redis-leader-fb76b4755-xjr2n     1/1     Running   0          11m
   ```

### Creating the Redis follower service

The guestbook application needs to communicate with the Redis followers to
read data. To make the Redis followers discoverable, you must set up another
[Service](/docs/concepts/services-networking/service/).

{{< codenew file="application/guestbook/redis-follower-service.yaml" >}}

1. Apply the Redis Service from the following `redis-follower-service.yaml` file:

   <!---
   for local testing of the content via relative file path
   kubectl apply -f ./content/en/examples/application/guestbook/redis-follower-service.yaml
   -->

   ```shell
   kubectl apply -f https://k8s.io/examples/application/guestbook/redis-follower-service.yaml
   ```

1. Query the list of Services to verify that the Redis Service is running:

   ```shell
   kubectl get service
   ```

   The response should be similar to this:

   ```
   NAME             TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
   kubernetes       ClusterIP   10.96.0.1       <none>        443/TCP    3d19h
   redis-follower   ClusterIP   10.110.162.42   <none>        6379/TCP   9s
   redis-leader     ClusterIP   10.103.78.24    <none>        6379/TCP   6m10s
   ```

{{< note >}}
This manifest file creates a Service named `redis-follower` with a set of
labels that match the labels previously defined, so the Service routes network
traffic to the Redis Pod.
{{< /note >}}

## Set up and Expose the Guestbook Frontend

Now that you have the Redis storage of your guestbook up and running, start
the guestbook web servers. Like the Redis followers, the frontend is deployed
using a Kubernetes Deployment.

The guestbook app uses a PHP frontend. It is configured to communicate with
either the Redis follower or leader Services, depending on whether the request
is a read or a write. The frontend exposes a JSON interface, and serves a
jQuery-Ajax-based UX.

### Creating the Guestbook Frontend Deployment

{{< codenew file="application/guestbook/frontend-deployment.yaml" >}}

1. Apply the frontend Deployment from the `frontend-deployment.yaml` file:

   <!---
   for local testing of the content via relative file path
   kubectl apply -f ./content/en/examples/application/guestbook/frontend-deployment.yaml
   -->

   ```shell
   kubectl apply -f https://k8s.io/examples/application/guestbook/frontend-deployment.yaml
   ```

1. Query the list of Pods to verify that the three frontend replicas are running:

   ```shell
   kubectl get pods -l app=guestbook -l tier=frontend
   ```

   The response should be similar to this:

   ```
   NAME                        READY   STATUS    RESTARTS   AGE
   frontend-85595f5bf9-5tqhb   1/1     Running   0          47s
   frontend-85595f5bf9-qbzwm   1/1     Running   0          47s
   frontend-85595f5bf9-zchwc   1/1     Running   0          47s
   ```

### Creating the Frontend Service

The `Redis` Services you applied is only accessible within the Kubernetes
cluster because the default type for a Service is
[ClusterIP](/docs/concepts/services-networking/service/#publishing-services-service-types).
`ClusterIP` provides a single IP address for the set of Pods the Service is
pointing to. This IP address is accessible only within the cluster.

If you want guests to be able to access your guestbook, you must configure the
frontend Service to be externally visible, so a client can request the Service
from outside the Kubernetes cluster. However a Kubernetes user you can use
`kubectl port-forward` to access the service even though it uses a
`ClusterIP`.

{{< note >}}
Some cloud providers, like Google Compute Engine or Google Kubernetes Engine,
support external load balancers. If your cloud provider supports load
balancers and you want to use it, uncomment `type: LoadBalancer`.
{{< /note >}}

{{< codenew file="application/guestbook/frontend-service.yaml" >}}

1. Apply the frontend Service from the `frontend-service.yaml` file:

   <!---
   for local testing of the content via relative file path
   kubectl apply -f ./content/en/examples/application/guestbook/frontend-service.yaml
   -->

   ```shell
   kubectl apply -f https://k8s.io/examples/application/guestbook/frontend-service.yaml
   ```

1. Query the list of Services to verify that the frontend Service is running:

   ```shell
   kubectl get services
   ```

   The response should be similar to this:

   ```
   NAME             TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
   frontend         ClusterIP   10.97.28.230    <none>        80/TCP     19s
   kubernetes       ClusterIP   10.96.0.1       <none>        443/TCP    3d19h
   redis-follower   ClusterIP   10.110.162.42   <none>        6379/TCP   5m48s
   redis-leader     ClusterIP   10.103.78.24    <none>        6379/TCP   11m
   ```

### Viewing the Frontend Service via `kubectl port-forward`

1. Run the following command to forward port `8080` on your local machine to port `80` on the service.

   ```shell
   kubectl port-forward svc/frontend 8080:80
   ```

   The response should be similar to this:

   ```
   Forwarding from 127.0.0.1:8080 -> 80
   Forwarding from [::1]:8080 -> 80
   ```

1. load the page [http://localhost:8080](http://localhost:8080) in your browser to view your guestbook.

### Viewing the Frontend Service via `LoadBalancer`

If you deployed the `frontend-service.yaml` manifest with type: `LoadBalancer`
you need to find the IP address to view your Guestbook.

1. Run the following command to get the IP address for the frontend Service.

   ```shell
   kubectl get service frontend
   ```

   The response should be similar to this:

   ```
   NAME       TYPE           CLUSTER-IP      EXTERNAL-IP        PORT(S)        AGE
   frontend   LoadBalancer   10.51.242.136   109.197.92.229     80:32372/TCP   1m
   ```

1. Copy the external IP address, and load the page in your browser to view your guestbook.

{{< note >}}
Try adding some guestbook entries by typing in a message, and clicking Submit.
The message you typed appears in the frontend. This message indicates that
data is successfully added to Redis through the Services you created earlier.
{{< /note >}}

## Scale the Web Frontend

You can scale up or down as needed because your servers are defined as a
Service that uses a Deployment controller.

1. Run the following command to scale up the number of frontend Pods:

   ```shell
   kubectl scale deployment frontend --replicas=5
   ```

1. Query the list of Pods to verify the number of frontend Pods running:

   ```shell
   kubectl get pods
   ```

   The response should look similar to this:

   ```
   NAME                             READY   STATUS    RESTARTS   AGE
   frontend-85595f5bf9-5df5m        1/1     Running   0          83s
   frontend-85595f5bf9-7zmg5        1/1     Running   0          83s
   frontend-85595f5bf9-cpskg        1/1     Running   0          15m
   frontend-85595f5bf9-l2l54        1/1     Running   0          14m
   frontend-85595f5bf9-l9c8z        1/1     Running   0          14m
   redis-follower-dddfbdcc9-82sfr   1/1     Running   0          97m
   redis-follower-dddfbdcc9-qrt5k   1/1     Running   0          97m
   redis-leader-fb76b4755-xjr2n     1/1     Running   0          108m
   ```

1. Run the following command to scale down the number of frontend Pods:

   ```shell
   kubectl scale deployment frontend --replicas=2
   ```

1. Query the list of Pods to verify the number of frontend Pods running:

   ```shell
   kubectl get pods
   ```

   The response should look similar to this:

   ```
   NAME                             READY   STATUS    RESTARTS   AGE
   frontend-85595f5bf9-cpskg        1/1     Running   0          16m
   frontend-85595f5bf9-l9c8z        1/1     Running   0          15m
   redis-follower-dddfbdcc9-82sfr   1/1     Running   0          98m
   redis-follower-dddfbdcc9-qrt5k   1/1     Running   0          98m
   redis-leader-fb76b4755-xjr2n     1/1     Running   0          109m
   ```

## {{% heading "cleanup" %}}

Deleting the Deployments and Services also deletes any running Pods. Use
labels to delete multiple resources with one command.

1. Run the following commands to delete all Pods, Deployments, and Services.

   ```shell
   kubectl delete deployment -l app=redis
   kubectl delete service -l app=redis
   kubectl delete deployment frontend
   kubectl delete service frontend
   ```

   The response should look similar to this:

   ```
   deployment.apps "redis-follower" deleted
   deployment.apps "redis-leader" deleted
   deployment.apps "frontend" deleted
   service "frontend" deleted
   ```

1. Query the list of Pods to verify that no Pods are running:

   ```shell
   kubectl get pods
   ```

   The response should look similar to this:

   ```
   No resources found in default namespace.
   ```

## {{% heading "whatsnext" %}}

* Complete the [Kubernetes Basics](/docs/tutorials/kubernetes-basics/) Interactive Tutorials
* Use Kubernetes to create a blog using [Persistent Volumes for MySQL and Wordpress](/docs/tutorials/stateful-application/mysql-wordpress-persistent-volume/#visit-your-new-wordpress-blog)
* Read more about [connecting applications](/docs/concepts/services-networking/connect-applications-service/)
* Read more about [Managing Resources](/docs/concepts/cluster-administration/manage-deployment/#using-labels-effectively)
