---
title: kubectl for Docker Users
content_type: concept
reviewers:
- brendandburns
- thockin
---

<!-- overview -->
You can use the Kubernetes command line tool `kubectl` to interact with the API Server. Using docker is straightforward if you are familiar with the Docker command line tool. However, there are a few differences between the Docker commands and the kubectl commands. The following sections show a Docker sub-command and describe the equivalent `kubectl` command.


<!-- body -->
## docker run

To run an nginx Deployment and expose the Deployment, see [kubectl create deployment](/docs/reference/generated/kubectl/kubectl-commands#-em-deployment-em-).
docker:

```shell
docker run -d --restart=always -e DOMAIN=cluster --name nginx-app -p 80:80 nginx
```
```
55c103fa129692154a7652490236fee9be47d70a8dd562281ae7d2f9a339a6db
```

```shell
docker ps
```
```
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                NAMES
55c103fa1296        nginx               "nginx -g 'daemon of…"   9 seconds ago       Up 9 seconds        0.0.0.0:80->80/tcp   nginx-app
```

kubectl:

```shell
# start the pod running nginx
kubectl create deployment --image=nginx nginx-app
```
```
deployment.apps/nginx-app created
```

```shell
# add env to nginx-app
kubectl set env deployment/nginx-app  DOMAIN=cluster
```
```
deployment.apps/nginx-app env updated
```

{{< note >}}
`kubectl` commands print the type and name of the resource created or mutated, which can then be used in subsequent commands. You can expose a new Service after a Deployment is created.
{{< /note >}}

```shell
# expose a port through with a service
kubectl expose deployment nginx-app --port=80 --name=nginx-http
```
```
service "nginx-http" exposed
```

By using kubectl, you can create a [Deployment](/docs/concepts/workloads/controllers/deployment/) to ensure that N pods are running nginx, where N is the number of replicas stated in the spec and defaults to 1. You can also create a [service](/docs/concepts/services-networking/service/) with a selector that matches the pod labels. For more information, see [Use a Service to Access an Application in a Cluster](/docs/tasks/access-application-cluster/service-access-application-cluster).

By default images run in the background, similar to `docker run -d ...`. To run things in the foreground, use [`kubectl run`](/docs/reference/generated/kubectl/kubectl-commands/#run) to create pod:
```shell
kubectl run [-i] [--tty] --attach <name> --image=<image>
```

Unlike `docker run ...`, if you specify `--attach`, then you attach `stdin`, `stdout` and `stderr`. You cannot control which streams are attached (`docker -a ...`).
To detach from the container, you can type the escape sequence Ctrl+P followed by Ctrl+Q.

## docker ps

To list what is currently running, see [kubectl get](/docs/reference/generated/kubectl/kubectl-commands/#get).

docker:

```shell
docker ps -a
```
```
CONTAINER ID        IMAGE               COMMAND                  CREATED              STATUS                     PORTS                NAMES
14636241935f        ubuntu:16.04        "echo test"              5 seconds ago        Exited (0) 5 seconds ago                        cocky_fermi
55c103fa1296        nginx               "nginx -g 'daemon of…"   About a minute ago   Up About a minute          0.0.0.0:80->80/tcp   nginx-app
```

kubectl:

```shell
kubectl get po
```
```
NAME                        READY     STATUS      RESTARTS   AGE
nginx-app-8df569cb7-4gd89   1/1       Running     0          3m
ubuntu                      0/1       Completed   0          20s
```

## docker attach

To attach a process that is already running in a container, see [kubectl attach](/docs/reference/generated/kubectl/kubectl-commands/#attach).

docker:

```shell
docker ps
```
```
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                NAMES
55c103fa1296        nginx               "nginx -g 'daemon of…"   5 minutes ago       Up 5 minutes        0.0.0.0:80->80/tcp   nginx-app
```

```shell
docker attach 55c103fa1296
...
```

kubectl:

```shell
kubectl get pods
```
```
NAME              READY     STATUS    RESTARTS   AGE
nginx-app-5jyvm   1/1       Running   0          10m
```

```shell
kubectl attach -it nginx-app-5jyvm
...
```

To detach from the container, you can type the escape sequence Ctrl+P followed by Ctrl+Q.

## docker exec

To execute a command in a container, see [kubectl exec](/docs/reference/generated/kubectl/kubectl-commands/#exec).

docker:

```shell
docker ps
```
```
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                NAMES
55c103fa1296        nginx               "nginx -g 'daemon of…"   6 minutes ago       Up 6 minutes        0.0.0.0:80->80/tcp   nginx-app
```
```shell
docker exec 55c103fa1296 cat /etc/hostname
```
```
55c103fa1296
```

kubectl:

```shell
kubectl get po
```
```
NAME              READY     STATUS    RESTARTS   AGE
nginx-app-5jyvm   1/1       Running   0          10m
```

```shell
kubectl exec nginx-app-5jyvm -- cat /etc/hostname
```
```
nginx-app-5jyvm
```

To use interactive commands.


docker:

```shell
docker exec -ti 55c103fa1296 /bin/sh
# exit
```

kubectl:

```shell
kubectl exec -ti nginx-app-5jyvm -- /bin/sh
# exit
```

For more information, see [Get a Shell to a Running Container](/docs/tasks/debug-application-cluster/get-shell-running-container/).

## docker logs

To follow stdout/stderr of a process that is running, see [kubectl logs](/docs/reference/generated/kubectl/kubectl-commands/#logs).


docker:

```shell
docker logs -f a9e
```
```
192.168.9.1 - - [14/Jul/2015:01:04:02 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.35.0" "-"
192.168.9.1 - - [14/Jul/2015:01:04:03 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.35.0" "-"
```

kubectl:

```shell
kubectl logs -f nginx-app-zibvs
```
```
10.240.63.110 - - [14/Jul/2015:01:09:01 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.26.0" "-"
10.240.63.110 - - [14/Jul/2015:01:09:02 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.26.0" "-"
```

There is a slight difference between pods and containers; by default pods do not terminate if their processes exit. Instead the pods restart the process. This is similar to the docker run option `--restart=always` with one major difference. In docker, the output for each invocation of the process is concatenated, but for Kubernetes, each invocation is separate. To see the output from a previous run in Kubernetes, do this:

```shell
kubectl logs --previous nginx-app-zibvs
```
```
10.240.63.110 - - [14/Jul/2015:01:09:01 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.26.0" "-"
10.240.63.110 - - [14/Jul/2015:01:09:02 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.26.0" "-"
```

For more information, see [Logging Architecture](/docs/concepts/cluster-administration/logging/).

## docker stop and docker rm

To stop and delete a running process, see [kubectl delete](/docs/reference/generated/kubectl/kubectl-commands/#delete).

docker:

```shell
docker ps
```
```
CONTAINER ID        IMAGE               COMMAND                CREATED             STATUS              PORTS                         NAMES
a9ec34d98787        nginx               "nginx -g 'daemon of"  22 hours ago        Up 22 hours         0.0.0.0:80->80/tcp, 443/tcp   nginx-app
```

```shell
docker stop a9ec34d98787
```
```
a9ec34d98787
```

```shell
docker rm a9ec34d98787
```
```
a9ec34d98787
```

kubectl:

```shell
kubectl get deployment nginx-app
```
```
NAME         READY   UP-TO-DATE   AVAILABLE   AGE
nginx-app    1/1     1            1           2m
```

```shell
kubectl get po -l app=nginx-app
```
```
NAME                         READY     STATUS    RESTARTS   AGE
nginx-app-2883164633-aklf7   1/1       Running   0          2m
```
```shell
kubectl delete deployment nginx-app
```
```
deployment "nginx-app" deleted
```

```shell
kubectl get po -l app=nginx-app
# Return nothing
```

{{< note >}}
When you use kubectl, you don't delete the pod directly. You have to first delete the Deployment that owns the pod. If you delete the pod directly, the Deployment recreates the pod.
{{< /note >}}

## docker login

There is no direct analog of `docker login` in kubectl. If you are interested in using Kubernetes with a private registry, see [Using a Private Registry](/docs/concepts/containers/images/#using-a-private-registry).

## docker version

To get the version of client and server, see [kubectl version](/docs/reference/generated/kubectl/kubectl-commands/#version).

docker:

```shell
docker version
```
```
Client version: 1.7.0
Client API version: 1.19
Go version (client): go1.4.2
Git commit (client): 0baf609
OS/Arch (client): linux/amd64
Server version: 1.7.0
Server API version: 1.19
Go version (server): go1.4.2
Git commit (server): 0baf609
OS/Arch (server): linux/amd64
```

kubectl:

```shell
kubectl version
```
```
Client Version: version.Info{Major:"1", Minor:"6", GitVersion:"v1.6.9+a3d1dfa6f4335", GitCommit:"9b77fed11a9843ce3780f70dd251e92901c43072", GitTreeState:"dirty", BuildDate:"2017-08-29T20:32:58Z", OpenPaasKubernetesVersion:"v1.03.02", GoVersion:"go1.7.5", Compiler:"gc", Platform:"linux/amd64"}
Server Version: version.Info{Major:"1", Minor:"6", GitVersion:"v1.6.9+a3d1dfa6f4335", GitCommit:"9b77fed11a9843ce3780f70dd251e92901c43072", GitTreeState:"dirty", BuildDate:"2017-08-29T20:32:58Z", OpenPaasKubernetesVersion:"v1.03.02", GoVersion:"go1.7.5", Compiler:"gc", Platform:"linux/amd64"}
```

## docker info

To get miscellaneous information about the environment and configuration, see [kubectl cluster-info](/docs/reference/generated/kubectl/kubectl-commands/#cluster-info).

docker:

```shell
docker info
```
```
Containers: 40
Images: 168
Storage Driver: aufs
 Root Dir: /usr/local/google/docker/aufs
 Backing Filesystem: extfs
 Dirs: 248
 Dirperm1 Supported: false
Execution Driver: native-0.2
Logging Driver: json-file
Kernel Version: 3.13.0-53-generic
Operating System: Ubuntu 14.04.2 LTS
CPUs: 12
Total Memory: 31.32 GiB
Name: k8s-is-fun.mtv.corp.google.com
ID: ADUV:GCYR:B3VJ:HMPO:LNPQ:KD5S:YKFQ:76VN:IANZ:7TFV:ZBF4:BYJO
WARNING: No swap limit support
```

kubectl:

```shell
kubectl cluster-info
```
```
Kubernetes master is running at https://203.0.113.141
KubeDNS is running at https://203.0.113.141/api/v1/namespaces/kube-system/services/kube-dns/proxy
kubernetes-dashboard is running at https://203.0.113.141/api/v1/namespaces/kube-system/services/kubernetes-dashboard/proxy
Grafana is running at https://203.0.113.141/api/v1/namespaces/kube-system/services/monitoring-grafana/proxy
Heapster is running at https://203.0.113.141/api/v1/namespaces/kube-system/services/monitoring-heapster/proxy
InfluxDB is running at https://203.0.113.141/api/v1/namespaces/kube-system/services/monitoring-influxdb/proxy
```

