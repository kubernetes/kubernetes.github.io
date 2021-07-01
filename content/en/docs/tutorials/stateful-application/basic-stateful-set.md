---
reviewers:
- enisoc
- erictune
- foxish
- janetkuo
- kow3ns
- smarterclayton
title: StatefulSet Basics
content_type: tutorial
weight: 10
---

<!-- overview -->
This tutorial provides an introduction to managing applications with
{{< glossary_tooltip text="StatefulSets" term_id="statefulset" >}}.
It demonstrates how to create, delete, scale, and update the Pods of StatefulSets.


## {{% heading "prerequisites" %}}

Before you begin this tutorial, you should familiarize yourself with the
following Kubernetes concepts:

* [Pods](/docs/concepts/workloads/pods/)
* [Cluster DNS](/docs/concepts/services-networking/dns-pod-service/)
* [Headless Services](/docs/concepts/services-networking/service/#headless-services)
* [PersistentVolumes](/docs/concepts/storage/persistent-volumes/)
* [PersistentVolume Provisioning](https://github.com/kubernetes/examples/tree/{{< param "githubbranch" >}}/staging/persistent-volume-provisioning/)
* [StatefulSets](/docs/concepts/workloads/controllers/statefulset/)
* The [kubectl](/docs/reference/kubectl/kubectl/) command line tool

{{< note >}}
This tutorial assumes that your cluster is configured to dynamically provision
PersistentVolumes. If your cluster is not configured to do so, you
will have to manually provision two 1 GiB volumes prior to starting this
tutorial.
{{< /note >}}

## {{% heading "objectives" %}}

StatefulSets are intended to be used with stateful applications and distributed
systems. However, the administration of stateful applications and
distributed systems on Kubernetes is a broad, complex topic. In order to
demonstrate the basic features of a StatefulSet, and not to conflate the former
topic with the latter, you will deploy a simple web application using a StatefulSet.

After this tutorial, you will be familiar with the following.

* How to create a StatefulSet
* How a StatefulSet manages its Pods
* How to delete a StatefulSet
* How to scale a StatefulSet
* How to update a StatefulSet's Pods

<!-- lessoncontent -->

## Creating a StatefulSet

Begin by creating a StatefulSet using the example below. It is similar to the
example presented in the
[StatefulSets](/docs/concepts/workloads/controllers/statefulset/) concept.
It creates a [headless Service](/docs/concepts/services-networking/service/#headless-services),
`nginx`, to publish the IP addresses of Pods in the StatefulSet, `web`.

{{< codenew file="application/web/web.yaml" >}}

Download the example above, and save it to a file named `web.yaml`

You will need to use two terminal windows. In the first terminal, use
[`kubectl get`](/docs/reference/generated/kubectl/kubectl-commands/#get) to watch the creation
of the StatefulSet's Pods.

```shell
kubectl get pods -w -l app=nginx
```

In the second terminal, use
[`kubectl apply`](/docs/reference/generated/kubectl/kubectl-commands/#apply) to create the
headless Service and StatefulSet defined in `web.yaml`.

```shell
kubectl apply -f web.yaml
```
```
service/nginx created
statefulset.apps/web created
```

The command above creates two Pods, each running an
[NGINX](https://www.nginx.com) webserver. Get the `nginx` Service...
```shell
kubectl get service nginx
```
```
NAME      TYPE         CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
nginx     ClusterIP    None         <none>        80/TCP    12s
```
...then get the `web` StatefulSet, to verify that both were created successfully:
```shell
kubectl get statefulset web
```
```
NAME      DESIRED   CURRENT   AGE
web       2         1         20s
```

### Ordered Pod Creation

For a StatefulSet with _n_ replicas, when Pods are being deployed, they are
created sequentially, ordered from _{0..n-1}_. Examine the output of the
`kubectl get` command in the first terminal. Eventually, the output will
look like the example below.

```shell
kubectl get pods -w -l app=nginx
```
```
NAME      READY     STATUS    RESTARTS   AGE
web-0     0/1       Pending   0          0s
web-0     0/1       Pending   0         0s
web-0     0/1       ContainerCreating   0         0s
web-0     1/1       Running   0         19s
web-1     0/1       Pending   0         0s
web-1     0/1       Pending   0         0s
web-1     0/1       ContainerCreating   0         0s
web-1     1/1       Running   0         18s
```

Notice that the `web-1` Pod is not launched until the `web-0` Pod is
_Running_ (see [Pod Phase](/docs/concepts/workloads/pods/pod-lifecycle/#pod-phase))
and _Ready_ (see `type` in [Pod Conditions](/docs/concepts/workloads/pods/pod-lifecycle/#pod-conditions)).

## Pods in a StatefulSet

Pods in a StatefulSet have a unique ordinal index and a stable network identity.

### Examining the Pod's Ordinal Index

Get the StatefulSet's Pods:

```shell
kubectl get pods -l app=nginx
```
```
NAME      READY     STATUS    RESTARTS   AGE
web-0     1/1       Running   0          1m
web-1     1/1       Running   0          1m
```

As mentioned in the [StatefulSets](/docs/concepts/workloads/controllers/statefulset/)
concept, the Pods in a StatefulSet have a sticky, unique identity. This identity
is based on a unique ordinal index that is assigned to each Pod by the
StatefulSet {{< glossary_tooltip term_id="controller" text="controller">}}.  
The Pods' names take the form `<statefulset name>-<ordinal index>`.
Since the `web` StatefulSet has two replicas, it creates two Pods, `web-0` and `web-1`.

### Using Stable Network Identities

Each Pod has a stable hostname based on its ordinal index. Use
[`kubectl exec`](/docs/reference/generated/kubectl/kubectl-commands/#exec) to execute the
`hostname` command in each Pod:

```shell
for i in 0 1; do kubectl exec "web-$i" -- sh -c 'hostname'; done
```
```
web-0
web-1
```

Use [`kubectl run`](/docs/reference/generated/kubectl/kubectl-commands/#run) to execute
a container that provides the `nslookup` command from the `dnsutils` package.
Using `nslookup` on the Pods' hostnames, you can examine their in-cluster DNS
addresses:

```shell
kubectl run -i --tty --image busybox:1.28 dns-test --restart=Never --rm
```
which starts a new shell. In that new shell, run:
```shell
# Run this in the dns-test container shell
nslookup web-0.nginx
```
The output is similar to:
```
Server:    10.0.0.10
Address 1: 10.0.0.10 kube-dns.kube-system.svc.cluster.local

Name:      web-0.nginx
Address 1: 10.244.1.6

nslookup web-1.nginx
Server:    10.0.0.10
Address 1: 10.0.0.10 kube-dns.kube-system.svc.cluster.local

Name:      web-1.nginx
Address 1: 10.244.2.6
```

(and now exit the container shell: `exit`)

The CNAME of the headless service points to SRV records (one for each Pod that
is Running and Ready). The SRV records point to A record entries that
contain the Pods' IP addresses.

In one terminal, watch the StatefulSet's Pods:

```shell
kubectl get pod -w -l app=nginx
```
In a second terminal, use
[`kubectl delete`](/docs/reference/generated/kubectl/kubectl-commands/#delete) to delete all
the Pods in the StatefulSet:

```shell
kubectl delete pod -l app=nginx
```
```
pod "web-0" deleted
pod "web-1" deleted
```

Wait for the StatefulSet to restart them, and for both Pods to transition to
Running and Ready:

```shell
kubectl get pod -w -l app=nginx
```
```
NAME      READY     STATUS              RESTARTS   AGE
web-0     0/1       ContainerCreating   0          0s
NAME      READY     STATUS    RESTARTS   AGE
web-0     1/1       Running   0          2s
web-1     0/1       Pending   0         0s
web-1     0/1       Pending   0         0s
web-1     0/1       ContainerCreating   0         0s
web-1     1/1       Running   0         34s
```

Use `kubectl exec` and `kubectl run` to view the Pods' hostnames and in-cluster
DNS entries. First, view the Pods' hostnames:

```shell
for i in 0 1; do kubectl exec web-$i -- sh -c 'hostname'; done
```
```
web-0
web-1
```
then, run:
```
kubectl run -i --tty --image busybox:1.28 dns-test --restart=Never --rm /bin/sh
```
which starts a new shell.  
In that new shell, run:
```shell
# Run this in the dns-test container shell
nslookup web-0.nginx
```
The output is similar to:
```
Server:    10.0.0.10
Address 1: 10.0.0.10 kube-dns.kube-system.svc.cluster.local

Name:      web-0.nginx
Address 1: 10.244.1.7

nslookup web-1.nginx
Server:    10.0.0.10
Address 1: 10.0.0.10 kube-dns.kube-system.svc.cluster.local

Name:      web-1.nginx
Address 1: 10.244.2.8
```

(and now exit the container shell: `exit`)

The Pods' ordinals, hostnames, SRV records, and A record names have not changed,
but the IP addresses associated with the Pods may have changed. In the cluster
used for this tutorial, they have. This is why it is important not to configure
other applications to connect to Pods in a StatefulSet by IP address.


If you need to find and connect to the active members of a StatefulSet, you
should query the CNAME of the headless Service
(`nginx.default.svc.cluster.local`). The SRV records associated with the
CNAME will contain only the Pods in the StatefulSet that are Running and
Ready.

If your application already implements connection logic that tests for
liveness and readiness, you can use the SRV records of the Pods (
`web-0.nginx.default.svc.cluster.local`,
`web-1.nginx.default.svc.cluster.local`), as they are stable, and your
application will be able to discover the Pods' addresses when they transition
to Running and Ready.

### Writing to Stable Storage

Get the PersistentVolumeClaims for `web-0` and `web-1`:

```shell
kubectl get pvc -l app=nginx
```
The output is similar to:
```
NAME        STATUS    VOLUME                                     CAPACITY   ACCESSMODES   AGE
www-web-0   Bound     pvc-15c268c7-b507-11e6-932f-42010a800002   1Gi        RWO           48s
www-web-1   Bound     pvc-15c79307-b507-11e6-932f-42010a800002   1Gi        RWO           48s
```

The StatefulSet controller created two
{{< glossary_tooltip text="PersistentVolumeClaims" term_id="persistent-volume-claim" >}}
that are bound to two
{{< glossary_tooltip text="PersistentVolumes" term_id="persistent-volume" >}}.

As the cluster used in this tutorial is configured to dynamically provision PersistentVolumes,
the PersistentVolumes were created and bound automatically.

The NGINX webserver, by default, serves an index file from
`/usr/share/nginx/html/index.html`. The `volumeMounts` field in the
StatefulSet's `spec` ensures that the `/usr/share/nginx/html` directory is
backed by a PersistentVolume.

Write the Pods' hostnames to their `index.html` files and verify that the NGINX
webservers serve the hostnames:

```shell
for i in 0 1; do kubectl exec "web-$i" -- sh -c 'echo "$(hostname)" > /usr/share/nginx/html/index.html'; done

for i in 0 1; do kubectl exec -i -t "web-$i" -- curl http://localhost/; done
```
```
web-0
web-1
```

{{< note >}}
If you instead see **403 Forbidden** responses for the above curl command,
you will need to fix the permissions of the directory mounted by the `volumeMounts`
(due to a [bug when using hostPath volumes](https://github.com/kubernetes/kubernetes/issues/2630)),
by running:

`for i in 0 1; do kubectl exec web-$i -- chmod 755 /usr/share/nginx/html; done`

before retrying the `curl` command above.
{{< /note >}}

In one terminal, watch the StatefulSet's Pods:

```shell
kubectl get pod -w -l app=nginx
```

In a second terminal, delete all of the StatefulSet's Pods:

```shell
kubectl delete pod -l app=nginx
```
```
pod "web-0" deleted
pod "web-1" deleted
```
Examine the output of the `kubectl get` command in the first terminal, and wait
for all of the Pods to transition to Running and Ready.

```shell
kubectl get pod -w -l app=nginx
```
```
NAME      READY     STATUS              RESTARTS   AGE
web-0     0/1       ContainerCreating   0          0s
NAME      READY     STATUS    RESTARTS   AGE
web-0     1/1       Running   0          2s
web-1     0/1       Pending   0         0s
web-1     0/1       Pending   0         0s
web-1     0/1       ContainerCreating   0         0s
web-1     1/1       Running   0         34s
```

Verify the web servers continue to serve their hostnames:

```
for i in 0 1; do kubectl exec -i -t "web-$i" -- curl http://localhost/; done
```
```
web-0
web-1
```

Even though `web-0` and `web-1` were rescheduled, they continue to serve their
hostnames because the PersistentVolumes associated with their
PersistentVolumeClaims are remounted to their `volumeMounts`. No matter what
node `web-0`and `web-1` are scheduled on, their PersistentVolumes will be
mounted to the appropriate mount points.

## Scaling a StatefulSet

Scaling a StatefulSet refers to increasing or decreasing the number of replicas.
This is accomplished by updating the `replicas` field. You can use either
[`kubectl scale`](/docs/reference/generated/kubectl/kubectl-commands/#scale) or
[`kubectl patch`](/docs/reference/generated/kubectl/kubectl-commands/#patch) to scale a StatefulSet.

### Scaling Up

In one terminal window, watch the Pods in the StatefulSet:

```shell
kubectl get pods -w -l app=nginx
```

In another terminal window, use `kubectl scale` to scale the number of replicas
to 5:

```shell
kubectl scale sts web --replicas=5
```
```
statefulset.apps/web scaled
```

Examine the output of the `kubectl get` command in the first terminal, and wait
for the three additional Pods to transition to Running and Ready.

```shell
kubectl get pods -w -l app=nginx
```
```
NAME      READY     STATUS    RESTARTS   AGE
web-0     1/1       Running   0          2h
web-1     1/1       Running   0          2h
NAME      READY     STATUS    RESTARTS   AGE
web-2     0/1       Pending   0          0s
web-2     0/1       Pending   0         0s
web-2     0/1       ContainerCreating   0         0s
web-2     1/1       Running   0         19s
web-3     0/1       Pending   0         0s
web-3     0/1       Pending   0         0s
web-3     0/1       ContainerCreating   0         0s
web-3     1/1       Running   0         18s
web-4     0/1       Pending   0         0s
web-4     0/1       Pending   0         0s
web-4     0/1       ContainerCreating   0         0s
web-4     1/1       Running   0         19s
```

The StatefulSet controller scaled the number of replicas. As with
[StatefulSet creation](#ordered-pod-creation), the StatefulSet controller
created each Pod sequentially with respect to its ordinal index, and it
waited for each Pod's predecessor to be Running and Ready before launching the
subsequent Pod.

### Scaling Down

In one terminal, watch the StatefulSet's Pods:

```shell
kubectl get pods -w -l app=nginx
```

In another terminal, use `kubectl patch` to scale the StatefulSet back down to
three replicas:

```shell
kubectl patch sts web -p '{"spec":{"replicas":3}}'
```
```
statefulset.apps/web patched
```

Wait for `web-4` and `web-3` to transition to Terminating.

```shell
kubectl get pods -w -l app=nginx
```
```
NAME      READY     STATUS              RESTARTS   AGE
web-0     1/1       Running             0          3h
web-1     1/1       Running             0          3h
web-2     1/1       Running             0          55s
web-3     1/1       Running             0          36s
web-4     0/1       ContainerCreating   0          18s
NAME      READY     STATUS    RESTARTS   AGE
web-4     1/1       Running   0          19s
web-4     1/1       Terminating   0         24s
web-4     1/1       Terminating   0         24s
web-3     1/1       Terminating   0         42s
web-3     1/1       Terminating   0         42s
```

### Ordered Pod Termination

The controller deleted one Pod at a time, in reverse order with respect to its
ordinal index, and it waited for each to be completely shutdown before
deleting the next.

Get the StatefulSet's PersistentVolumeClaims:

```shell
kubectl get pvc -l app=nginx
```
```
NAME        STATUS    VOLUME                                     CAPACITY   ACCESSMODES   AGE
www-web-0   Bound     pvc-15c268c7-b507-11e6-932f-42010a800002   1Gi        RWO           13h
www-web-1   Bound     pvc-15c79307-b507-11e6-932f-42010a800002   1Gi        RWO           13h
www-web-2   Bound     pvc-e1125b27-b508-11e6-932f-42010a800002   1Gi        RWO           13h
www-web-3   Bound     pvc-e1176df6-b508-11e6-932f-42010a800002   1Gi        RWO           13h
www-web-4   Bound     pvc-e11bb5f8-b508-11e6-932f-42010a800002   1Gi        RWO           13h

```

There are still five PersistentVolumeClaims and five PersistentVolumes.
When exploring a Pod's [stable storage](#writing-to-stable-storage), we saw that the PersistentVolumes mounted to the Pods of a StatefulSet are not deleted when the StatefulSet's Pods are deleted. This is still true when Pod deletion is caused by scaling the StatefulSet down.

## Updating StatefulSets

In Kubernetes 1.7 and later, the StatefulSet controller supports automated updates.  The
strategy used is determined by the `spec.updateStrategy` field of the
StatefulSet API Object. This feature can be used to upgrade the container
images, resource requests and/or limits, labels, and annotations of the Pods in a
StatefulSet. There are two valid update strategies, `RollingUpdate` and
`OnDelete`.

`RollingUpdate` update strategy is the default for StatefulSets.

### Rolling Update

The `RollingUpdate` update strategy will update all Pods in a StatefulSet, in
reverse ordinal order, while respecting the StatefulSet guarantees.

Patch the `web` StatefulSet to apply the `RollingUpdate` update strategy:

```shell
kubectl patch statefulset web -p '{"spec":{"updateStrategy":{"type":"RollingUpdate"}}}'
```
```
statefulset.apps/web patched
```

In one terminal window, patch the `web` StatefulSet to change the container
image again:

```shell
kubectl patch statefulset web --type='json' -p='[{"op": "replace", "path": "/spec/template/spec/containers/0/image", "value":"gcr.io/google_containers/nginx-slim:0.8"}]'
```
```
statefulset.apps/web patched
```

In another terminal, watch the Pods in the StatefulSet:

```shell
kubectl get pod -l app=nginx -w
```
The output is similar to:
```
NAME      READY     STATUS    RESTARTS   AGE
web-0     1/1       Running   0          7m
web-1     1/1       Running   0          7m
web-2     1/1       Running   0          8m
web-2     1/1       Terminating   0         8m
web-2     1/1       Terminating   0         8m
web-2     0/1       Terminating   0         8m
web-2     0/1       Terminating   0         8m
web-2     0/1       Terminating   0         8m
web-2     0/1       Terminating   0         8m
web-2     0/1       Pending   0         0s
web-2     0/1       Pending   0         0s
web-2     0/1       ContainerCreating   0         0s
web-2     1/1       Running   0         19s
web-1     1/1       Terminating   0         8m
web-1     0/1       Terminating   0         8m
web-1     0/1       Terminating   0         8m
web-1     0/1       Terminating   0         8m
web-1     0/1       Pending   0         0s
web-1     0/1       Pending   0         0s
web-1     0/1       ContainerCreating   0         0s
web-1     1/1       Running   0         6s
web-0     1/1       Terminating   0         7m
web-0     1/1       Terminating   0         7m
web-0     0/1       Terminating   0         7m
web-0     0/1       Terminating   0         7m
web-0     0/1       Terminating   0         7m
web-0     0/1       Terminating   0         7m
web-0     0/1       Pending   0         0s
web-0     0/1       Pending   0         0s
web-0     0/1       ContainerCreating   0         0s
web-0     1/1       Running   0         10s
```

The Pods in the StatefulSet are updated in reverse ordinal order. The
StatefulSet controller terminates each Pod, and waits for it to transition to Running and
Ready prior to updating the next Pod. Note that, even though the StatefulSet
controller will not proceed to update the next Pod until its ordinal successor
is Running and Ready, it will restore any Pod that fails during the update to
its current version.

Pods that have already received the update will be restored to the updated version,
and Pods that have not yet received the update will be restored to the previous
version. In this way, the controller attempts to continue to keep the application
healthy and the update consistent in the presence of intermittent failures.

Get the Pods to view their container images:

```shell
for p in 0 1 2; do kubectl get pod "web-$p" --template '{{range $i, $c := .spec.containers}}{{$c.image}}{{end}}'; echo; done
```
```
k8s.gcr.io/nginx-slim:0.8
k8s.gcr.io/nginx-slim:0.8
k8s.gcr.io/nginx-slim:0.8

```

All the Pods in the StatefulSet are now running the previous container image.

{{< note >}}
You can also use `kubectl rollout status sts/<name>` to view
the status of a rolling update to a StatefulSet
{{< /note >}}

#### Staging an Update

You can stage an update to a StatefulSet by using the `partition` parameter of
the `RollingUpdate` update strategy. A staged update will keep all of the Pods
in the StatefulSet at the current version while allowing mutations to the
StatefulSet's `.spec.template`.

Patch the `web` StatefulSet to add a partition to the `updateStrategy` field:

```shell
kubectl patch statefulset web -p '{"spec":{"updateStrategy":{"type":"RollingUpdate","rollingUpdate":{"partition":3}}}}'
```
```
statefulset.apps/web patched
```

Patch the StatefulSet again to change the container's image:

```shell
kubectl patch statefulset web --type='json' -p='[{"op": "replace", "path": "/spec/template/spec/containers/0/image", "value":"k8s.gcr.io/nginx-slim:0.7"}]'
```
```
statefulset.apps/web patched
```

Delete a Pod in the StatefulSet:

```shell
kubectl delete pod web-2
```
```
pod "web-2" deleted
```

Wait for the Pod to be Running and Ready.

```shell
kubectl get pod -l app=nginx -w
```
```
NAME      READY     STATUS              RESTARTS   AGE
web-0     1/1       Running             0          4m
web-1     1/1       Running             0          4m
web-2     0/1       ContainerCreating   0          11s
web-2     1/1       Running   0         18s
```

Get the Pod's container image:

```shell
kubectl get pod web-2 --template '{{range $i, $c := .spec.containers}}{{$c.image}}{{end}}'
```
```
k8s.gcr.io/nginx-slim:0.8
```

Notice that, even though the update strategy is `RollingUpdate` the StatefulSet
restored the Pod with its original container. This is because the
ordinal of the Pod is less than the `partition` specified by the
`updateStrategy`.

#### Rolling Out a Canary

You can roll out a canary to test a modification by decrementing the `partition`
you specified [above](#staging-an-update).

Patch the StatefulSet to decrement the partition:

```shell
kubectl patch statefulset web -p '{"spec":{"updateStrategy":{"type":"RollingUpdate","rollingUpdate":{"partition":2}}}}'
```
```
statefulset.apps/web patched
```

Wait for `web-2` to be Running and Ready.

```shell
kubectl get pod -l app=nginx -w
```
```
NAME      READY     STATUS              RESTARTS   AGE
web-0     1/1       Running             0          4m
web-1     1/1       Running             0          4m
web-2     0/1       ContainerCreating   0          11s
web-2     1/1       Running   0         18s
```

Get the Pod's container:

```shell
kubectl get pod web-2 --template '{{range $i, $c := .spec.containers}}{{$c.image}}{{end}}'
```
```
k8s.gcr.io/nginx-slim:0.7

```

When you changed the `partition`, the StatefulSet controller automatically
updated the `web-2` Pod because the Pod's ordinal was greater than or equal to
the `partition`.

Delete the `web-1` Pod:

```shell
kubectl delete pod web-1
```
```
pod "web-1" deleted
```

Wait for the `web-1` Pod to be Running and Ready.

```shell
kubectl get pod -l app=nginx -w
```
The output is similar to:
```
NAME      READY     STATUS        RESTARTS   AGE
web-0     1/1       Running       0          6m
web-1     0/1       Terminating   0          6m
web-2     1/1       Running       0          2m
web-1     0/1       Terminating   0         6m
web-1     0/1       Terminating   0         6m
web-1     0/1       Terminating   0         6m
web-1     0/1       Pending   0         0s
web-1     0/1       Pending   0         0s
web-1     0/1       ContainerCreating   0         0s
web-1     1/1       Running   0         18s
```

Get the `web-1` Pod's container image:

```shell
kubectl get pod web-1 --template '{{range $i, $c := .spec.containers}}{{$c.image}}{{end}}'
```
```
k8s.gcr.io/nginx-slim:0.8
```

`web-1` was restored to its original configuration because the Pod's ordinal
was less than the partition. When a partition is specified, all Pods with an
ordinal that is greater than or equal to the partition will be updated when the
StatefulSet's `.spec.template` is updated. If a Pod that has an ordinal less
than the partition is deleted or otherwise terminated, it will be restored to
its original configuration.

#### Phased Roll Outs

You can perform a phased roll out (e.g. a linear, geometric, or exponential
roll out) using a partitioned rolling update in a similar manner to how you
rolled out a [canary](#rolling-out-a-canary). To perform a phased roll out, set
the `partition` to the ordinal at which you want the controller to pause the
update.

The partition is currently set to `2`. Set the partition to `0`:

```shell
kubectl patch statefulset web -p '{"spec":{"updateStrategy":{"type":"RollingUpdate","rollingUpdate":{"partition":0}}}}'
```
```
statefulset.apps/web patched
```

Wait for all of the Pods in the StatefulSet to become Running and Ready.

```shell
kubectl get pod -l app=nginx -w
```
The output is similar to:
```
NAME      READY     STATUS              RESTARTS   AGE
web-0     1/1       Running             0          3m
web-1     0/1       ContainerCreating   0          11s
web-2     1/1       Running             0          2m
web-1     1/1       Running   0         18s
web-0     1/1       Terminating   0         3m
web-0     1/1       Terminating   0         3m
web-0     0/1       Terminating   0         3m
web-0     0/1       Terminating   0         3m
web-0     0/1       Terminating   0         3m
web-0     0/1       Terminating   0         3m
web-0     0/1       Pending   0         0s
web-0     0/1       Pending   0         0s
web-0     0/1       ContainerCreating   0         0s
web-0     1/1       Running   0         3s
```

Get the container image details for the Pods in the StatefulSet:

```shell
for p in 0 1 2; do kubectl get pod "web-$p" --template '{{range $i, $c := .spec.containers}}{{$c.image}}{{end}}'; echo; done
```
```
k8s.gcr.io/nginx-slim:0.7
k8s.gcr.io/nginx-slim:0.7
k8s.gcr.io/nginx-slim:0.7
```

By moving the `partition` to `0`, you allowed the StatefulSet to
continue the update process.

### On Delete

The `OnDelete` update strategy implements the legacy (1.6 and prior) behavior,
When you select this update strategy, the StatefulSet controller will not
automatically update Pods when a modification is made to the StatefulSet's
`.spec.template` field. This strategy can be selected by setting the
`.spec.template.updateStrategy.type` to `OnDelete`.


## Deleting StatefulSets

StatefulSet supports both Non-Cascading and Cascading deletion. In a
Non-Cascading Delete, the StatefulSet's Pods are not deleted when the StatefulSet is deleted. In a Cascading Delete, both the StatefulSet and its Pods are
deleted.

### Non-Cascading Delete

In one terminal window, watch the Pods in the StatefulSet.

```
kubectl get pods -w -l app=nginx
```

Use [`kubectl delete`](/docs/reference/generated/kubectl/kubectl-commands/#delete) to delete the
StatefulSet. Make sure to supply the `--cascade=orphan` parameter to the
command. This parameter tells Kubernetes to only delete the StatefulSet, and to
not delete any of its Pods.

```shell
kubectl delete statefulset web --cascade=orphan
```
```
statefulset.apps "web" deleted
```

Get the Pods, to examine their status:

```shell
kubectl get pods -l app=nginx
```
```
NAME      READY     STATUS    RESTARTS   AGE
web-0     1/1       Running   0          6m
web-1     1/1       Running   0          7m
web-2     1/1       Running   0          5m
```

Even though `web` has been deleted, all of the Pods are still Running and Ready.
Delete `web-0`:

```shell
kubectl delete pod web-0
```
```
pod "web-0" deleted
```

Get the StatefulSet's Pods:

```shell
kubectl get pods -l app=nginx
```
```
NAME      READY     STATUS    RESTARTS   AGE
web-1     1/1       Running   0          10m
web-2     1/1       Running   0          7m
```

As the `web` StatefulSet has been deleted, `web-0` has not been relaunched.

In one terminal, watch the StatefulSet's Pods.

```shell
kubectl get pods -w -l app=nginx
```

In a second terminal, recreate the StatefulSet. Note that, unless
you deleted the `nginx` Service (which you should not have), you will see
an error indicating that the Service already exists.

```shell
kubectl apply -f web.yaml
```
```
statefulset.apps/web created
service/nginx unchanged
```

Ignore the error. It only indicates that an attempt was made to create the _nginx_
headless Service even though that Service already exists.

Examine the output of the `kubectl get` command running in the first terminal.

```shell
kubectl get pods -w -l app=nginx
```
```
NAME      READY     STATUS    RESTARTS   AGE
web-1     1/1       Running   0          16m
web-2     1/1       Running   0          2m
NAME      READY     STATUS    RESTARTS   AGE
web-0     0/1       Pending   0          0s
web-0     0/1       Pending   0         0s
web-0     0/1       ContainerCreating   0         0s
web-0     1/1       Running   0         18s
web-2     1/1       Terminating   0         3m
web-2     0/1       Terminating   0         3m
web-2     0/1       Terminating   0         3m
web-2     0/1       Terminating   0         3m
```

When the `web` StatefulSet was recreated, it first relaunched `web-0`.
Since `web-1` was already Running and Ready, when `web-0` transitioned to
Running and Ready, it adopted this Pod. Since you recreated the StatefulSet
with `replicas` equal to 2, once `web-0` had been recreated, and once
`web-1` had been determined to already be Running and Ready, `web-2` was
terminated.

Let's take another look at the contents of the `index.html` file served by the
Pods' webservers:

```shell
for i in 0 1; do kubectl exec -i -t "web-$i" -- curl http://localhost/; done
```

```
web-0
web-1
```

Even though you deleted both the StatefulSet and the `web-0` Pod, it still
serves the hostname originally entered into its `index.html` file. This is
because the StatefulSet never deletes the PersistentVolumes associated with a
Pod. When you recreated the StatefulSet and it relaunched `web-0`, its original
PersistentVolume was remounted.

### Cascading Delete

In one terminal window, watch the Pods in the StatefulSet.

```shell
kubectl get pods -w -l app=nginx
```

In another terminal, delete the StatefulSet again. This time, omit the
`--cascade=orphan` parameter.

```shell
kubectl delete statefulset web
```

```
statefulset.apps "web" deleted
```

Examine the output of the `kubectl get` command running in the first terminal,
and wait for all of the Pods to transition to Terminating.

```shell
kubectl get pods -w -l app=nginx
```

```
NAME      READY     STATUS    RESTARTS   AGE
web-0     1/1       Running   0          11m
web-1     1/1       Running   0          27m
NAME      READY     STATUS        RESTARTS   AGE
web-0     1/1       Terminating   0          12m
web-1     1/1       Terminating   0         29m
web-0     0/1       Terminating   0         12m
web-0     0/1       Terminating   0         12m
web-0     0/1       Terminating   0         12m
web-1     0/1       Terminating   0         29m
web-1     0/1       Terminating   0         29m
web-1     0/1       Terminating   0         29m

```

As you saw in the [Scaling Down](#scaling-down) section, the Pods
are terminated one at a time, with respect to the reverse order of their ordinal
indices. Before terminating a Pod, the StatefulSet controller waits for
the Pod's successor to be completely terminated.

{{< note >}}
Although a cascading delete removes a StatefulSet together with its Pods,
the cascade does not delete the headless Service associated with the StatefulSet.
You must delete the `nginx` Service manually.
{{< /note >}}

```shell
kubectl delete service nginx
```

```
service "nginx" deleted
```

Recreate the StatefulSet and headless Service one more time:

```shell
kubectl apply -f web.yaml
```

```
service/nginx created
statefulset.apps/web created
```

When all of the StatefulSet's Pods transition to Running and Ready, retrieve
the contents of their `index.html` files:

```shell
for i in 0 1; do kubectl exec -i -t "web-$i" -- curl http://localhost/; done
```

```
web-0
web-1
```

Even though you completely deleted the StatefulSet, and all of its Pods, the
Pods are recreated with their PersistentVolumes mounted, and `web-0` and
`web-1` continue to serve their hostnames.

Finally, delete the `nginx` Service...

```shell
kubectl delete service nginx
```

```
service "nginx" deleted
```

...and the `web` StatefulSet:

```shell
kubectl delete statefulset web
```

```
statefulset "web" deleted
```

## Pod Management Policy

For some distributed systems, the StatefulSet ordering guarantees are
unnecessary and/or undesirable. These systems require only uniqueness and
identity. To address this, in Kubernetes 1.7, we introduced
`.spec.podManagementPolicy` to the StatefulSet API Object.

### OrderedReady Pod Management

`OrderedReady` pod management is the default for StatefulSets. It tells the
StatefulSet controller to respect the ordering guarantees demonstrated
above.

### Parallel Pod Management

`Parallel` pod management tells the StatefulSet controller to launch or
terminate all Pods in parallel, and not to wait for Pods to become Running
and Ready or completely terminated prior to launching or terminating another
Pod. This option only affects the behavior for scaling operations. Updates are not affected.

{{< codenew file="application/web/web-parallel.yaml" >}}

Download the example above, and save it to a file named `web-parallel.yaml`

This manifest is identical to the one you downloaded above except that the `.spec.podManagementPolicy`
of the `web` StatefulSet is set to `Parallel`.

In one terminal, watch the Pods in the StatefulSet.

```shell
kubectl get pod -l app=nginx -w
```

In another terminal, create the StatefulSet and Service in the manifest:

```shell
kubectl apply -f web-parallel.yaml
```
```
service/nginx created
statefulset.apps/web created
```

Examine the output of the `kubectl get` command that you executed in the first terminal.

```shell
kubectl get pod -l app=nginx -w
```
```
NAME      READY     STATUS    RESTARTS   AGE
web-0     0/1       Pending   0          0s
web-0     0/1       Pending   0         0s
web-1     0/1       Pending   0         0s
web-1     0/1       Pending   0         0s
web-0     0/1       ContainerCreating   0         0s
web-1     0/1       ContainerCreating   0         0s
web-0     1/1       Running   0         10s
web-1     1/1       Running   0         10s
```

The StatefulSet controller launched both `web-0` and `web-1` at the same time.

Keep the second terminal open, and, in another terminal window scale the
StatefulSet:

```shell
kubectl scale statefulset/web --replicas=4
```
```
statefulset.apps/web scaled
```

Examine the output of the terminal where the `kubectl get` command is running.

```
web-3     0/1       Pending   0         0s
web-3     0/1       Pending   0         0s
web-3     0/1       Pending   0         7s
web-3     0/1       ContainerCreating   0         7s
web-2     1/1       Running   0         10s
web-3     1/1       Running   0         26s
```


The StatefulSet launched two new Pods, and it did not wait for
the first to become Running and Ready prior to launching the second.

## {{% heading "cleanup" %}}

You should have two terminals open, ready for you to run `kubectl` commands as
part of cleanup.

```shell
kubectl delete sts web
# sts is an abbreviation for statefulset
```

You can watch `kubectl get` to see those Pods being deleted.
```shell
kubectl get pod -l app=nginx -w
```
```
web-3     1/1       Terminating   0         9m
web-2     1/1       Terminating   0         9m
web-3     1/1       Terminating   0         9m
web-2     1/1       Terminating   0         9m
web-1     1/1       Terminating   0         44m
web-0     1/1       Terminating   0         44m
web-0     0/1       Terminating   0         44m
web-3     0/1       Terminating   0         9m
web-2     0/1       Terminating   0         9m
web-1     0/1       Terminating   0         44m
web-0     0/1       Terminating   0         44m
web-2     0/1       Terminating   0         9m
web-2     0/1       Terminating   0         9m
web-2     0/1       Terminating   0         9m
web-1     0/1       Terminating   0         44m
web-1     0/1       Terminating   0         44m
web-1     0/1       Terminating   0         44m
web-0     0/1       Terminating   0         44m
web-0     0/1       Terminating   0         44m
web-0     0/1       Terminating   0         44m
web-3     0/1       Terminating   0         9m
web-3     0/1       Terminating   0         9m
web-3     0/1       Terminating   0         9m
```

During deletion, a StatefulSet removes all Pods concurrently; it does not wait for
a Pod's ordinal successor to terminate prior to deleting that Pod.

Close the terminal where the `kubectl get` command is running and delete the `nginx`
Service:

```shell
kubectl delete svc nginx
```


{{< note >}}
You also need to delete the persistent storage media for the PersistentVolumes
used in this tutorial.


Follow the necessary steps, based on your environment, storage configuration,
and provisioning method, to ensure that all storage is reclaimed.
{{< /note >}}
