---
reviewers:
- cdrage
title: Translate a Docker Compose File to Kubernetes Resources
content_type: task
weight: 200
---

<!-- overview -->

What's Kompose? It's a conversion tool for all things compose (namely Docker Compose) to container orchestrators (Kubernetes or OpenShift).

More information can be found on the Kompose website at [http://kompose.io](http://kompose.io).

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}

<!-- steps -->

## Install Kompose

We have multiple ways to install Kompose. Our preferred method is downloading the binary from the latest GitHub release.

{{< tabs name="install_ways" >}}
{{% tab name="GitHub download" %}}

Kompose is released via GitHub on a three-week cycle, you can see all current releases on the [GitHub release page](https://github.com/kubernetes/kompose/releases).

```sh
# Linux
curl -L https://github.com/kubernetes/kompose/releases/download/v1.22.0/kompose-linux-amd64 -o kompose

# macOS
curl -L https://github.com/kubernetes/kompose/releases/download/v1.22.0/kompose-darwin-amd64 -o kompose

# Windows
curl -L https://github.com/kubernetes/kompose/releases/download/v1.22.0/kompose-windows-amd64.exe -o kompose.exe

chmod +x kompose
sudo mv ./kompose /usr/local/bin/kompose
```

Alternatively, you can download the [tarball](https://github.com/kubernetes/kompose/releases).

{{% /tab %}}
{{% tab name="Build from source" %}}

Installing using `go get` pulls from the master branch with the latest development changes.

```sh
go get -u github.com/kubernetes/kompose
```

{{% /tab %}}
{{% tab name="CentOS package" %}}

Kompose is in [EPEL](https://fedoraproject.org/wiki/EPEL) CentOS repository.
If you don't have [EPEL](https://fedoraproject.org/wiki/EPEL) repository already installed and enabled you can do it by running  `sudo yum install epel-release`

If you have [EPEL](https://fedoraproject.org/wiki/EPEL) enabled in your system, you can install Kompose like any other package.

```bash
sudo yum -y install kompose
```

{{% /tab %}}
{{% tab name="Fedora package" %}}

Kompose is in Fedora 24, 25 and 26 repositories. You can install it like any other package.

```bash
sudo dnf -y install kompose
```

{{% /tab %}}
{{% tab name="Homebrew (macOS)" %}}

On macOS you can install latest release via [Homebrew](https://brew.sh):

```bash
brew install kompose
```

{{% /tab %}}
{{< /tabs >}}

## Use Kompose

In a few steps, we'll take you from Docker Compose to Kubernetes. All
you need is an existing `docker-compose.yml` file.

1. Go to the directory containing your `docker-compose.yml` file. If you don't have one, test using this one.

   ```yaml
   version: "2"

   services:

     redis-master:
       image: k8s.gcr.io/redis:e2e
       ports:
         - "6379"

     redis-slave:
       image: gcr.io/google_samples/gb-redisslave:v3
       ports:
         - "6379"
       environment:
         - GET_HOSTS_FROM=dns

     frontend:
       image: gcr.io/google-samples/gb-frontend:v4
       ports:
         - "80:80"
       environment:
         - GET_HOSTS_FROM=dns
       labels:
         kompose.service.type: LoadBalancer
   ```

2. To convert the `docker-compose.yml` file to files that you can use with
   `kubectl`, run `kompose convert` and then `kubectl apply -f <output file>`.

   ```bash
   kompose convert
   ```

   The output is similar to:

   ```none
   INFO Kubernetes file "frontend-service.yaml" created
      INFO Kubernetes file "frontend-service.yaml" created
   INFO Kubernetes file "frontend-service.yaml" created
   INFO Kubernetes file "redis-master-service.yaml" created
      INFO Kubernetes file "redis-master-service.yaml" created
   INFO Kubernetes file "redis-master-service.yaml" created
   INFO Kubernetes file "redis-slave-service.yaml" created
      INFO Kubernetes file "redis-slave-service.yaml" created
   INFO Kubernetes file "redis-slave-service.yaml" created
   INFO Kubernetes file "frontend-deployment.yaml" created
      INFO Kubernetes file "frontend-deployment.yaml" created
   INFO Kubernetes file "frontend-deployment.yaml" created
   INFO Kubernetes file "redis-master-deployment.yaml" created
      INFO Kubernetes file "redis-master-deployment.yaml" created
   INFO Kubernetes file "redis-master-deployment.yaml" created
   INFO Kubernetes file "redis-slave-deployment.yaml" created
      INFO Kubernetes file "redis-slave-deployment.yaml" created
   INFO Kubernetes file "redis-slave-deployment.yaml" created
   ```

   ```bash
    kubectl apply -f frontend-service.yaml,redis-master-service.yaml,redis-slave-service.yaml,frontend-deployment.yaml,redis-master-deployment.yaml,redis-slave-deployment.yaml
   ```

   The output is similar to:

   ```none
   service/frontend created
   service/redis-master created
   service/redis-slave created
   deployment.apps/frontend created
   deployment.apps/redis-master created
   deployment.apps/redis-slave created
   ```

    Your deployments are running in Kubernetes.

3. Access your application.

   If you're already using `minikube` for your development process:

   ```bash
   minikube service frontend
   ```

   Otherwise, let's look up what IP your service is using!

   ```sh
   kubectl describe svc frontend
   ```

   ```none
   Name:                   frontend
   Namespace:              default
   Labels:                 service=frontend
   Selector:               service=frontend
   Type:                   LoadBalancer
   IP:                     10.0.0.183
   LoadBalancer Ingress:   192.0.2.89
   Port:                   80      80/TCP
   NodePort:               80      31144/TCP
   Endpoints:              172.17.0.4:80
   Session Affinity:       None
   No events.
   ```

   If you're using a cloud provider, your IP will be listed next to `LoadBalancer Ingress`.

   ```sh
   curl http://192.0.2.89
   ```

<!-- discussion -->

## User Guide

- CLI
  - [`kompose convert`](#kompose-convert)
  - [`kompose up`](#kompose-up)
  - [`kompose down`](#kompose-down)
- Documentation
  - [Build and Push Docker Images](#build-and-push-docker-images)
  - [Alternative Conversions](#alternative-conversions)
  - [Labels](#labels)
  - [Restart](#restart)
  - [Docker Compose Versions](#docker-compose-versions)

Kompose has support for two providers: OpenShift and Kubernetes.
You can choose a targeted provider using global option `--provider`. If no provider is specified, Kubernetes is set by default.

## `kompose convert`

Kompose supports conversion of V1, V2, and V3 Docker Compose files into Kubernetes and OpenShift objects.

### Kubernetes `kompose convert` example

```shell
kompose --file docker-voting.yml convert
```

```none
WARN Unsupported key networks - ignoring
WARN Unsupported key build - ignoring
INFO Kubernetes file "worker-svc.yaml" created
INFO Kubernetes file "db-svc.yaml" created
INFO Kubernetes file "redis-svc.yaml" created
INFO Kubernetes file "result-svc.yaml" created
INFO Kubernetes file "vote-svc.yaml" created
INFO Kubernetes file "redis-deployment.yaml" created
INFO Kubernetes file "result-deployment.yaml" created
INFO Kubernetes file "vote-deployment.yaml" created
INFO Kubernetes file "worker-deployment.yaml" created
INFO Kubernetes file "db-deployment.yaml" created
```

```shell
ls
```

```none
db-deployment.yaml  docker-compose.yml         docker-gitlab.yml  redis-deployment.yaml  result-deployment.yaml  vote-deployment.yaml  worker-deployment.yaml
db-svc.yaml         docker-voting.yml          redis-svc.yaml     result-svc.yaml        vote-svc.yaml           worker-svc.yaml
```

You can also provide multiple docker-compose files at the same time:

```shell
kompose -f docker-compose.yml -f docker-guestbook.yml convert
```

```none
INFO Kubernetes file "frontend-service.yaml" created         
INFO Kubernetes file "mlbparks-service.yaml" created         
INFO Kubernetes file "mongodb-service.yaml" created          
INFO Kubernetes file "redis-master-service.yaml" created     
INFO Kubernetes file "redis-slave-service.yaml" created      
INFO Kubernetes file "frontend-deployment.yaml" created      
INFO Kubernetes file "mlbparks-deployment.yaml" created      
INFO Kubernetes file "mongodb-deployment.yaml" created       
INFO Kubernetes file "mongodb-claim0-persistentvolumeclaim.yaml" created
INFO Kubernetes file "redis-master-deployment.yaml" created  
INFO Kubernetes file "redis-slave-deployment.yaml" created   
```

```shell
ls
```

```none
mlbparks-deployment.yaml  mongodb-service.yaml                       redis-slave-service.jsonmlbparks-service.yaml  
frontend-deployment.yaml  mongodb-claim0-persistentvolumeclaim.yaml  redis-master-service.yaml
frontend-service.yaml     mongodb-deployment.yaml                    redis-slave-deployment.yaml
redis-master-deployment.yaml
```

When multiple docker-compose files are provided the configuration is merged. Any configuration that is common will be over ridden by subsequent file.

### OpenShift `kompose convert` example

```sh
kompose --provider openshift --file docker-voting.yml convert
```

```none
WARN [worker] Service cannot be created because of missing port.
INFO OpenShift file "vote-service.yaml" created             
INFO OpenShift file "db-service.yaml" created               
INFO OpenShift file "redis-service.yaml" created            
INFO OpenShift file "result-service.yaml" created           
INFO OpenShift file "vote-deploymentconfig.yaml" created    
INFO OpenShift file "vote-imagestream.yaml" created         
INFO OpenShift file "worker-deploymentconfig.yaml" created  
INFO OpenShift file "worker-imagestream.yaml" created       
INFO OpenShift file "db-deploymentconfig.yaml" created      
INFO OpenShift file "db-imagestream.yaml" created           
INFO OpenShift file "redis-deploymentconfig.yaml" created   
INFO OpenShift file "redis-imagestream.yaml" created        
INFO OpenShift file "result-deploymentconfig.yaml" created  
INFO OpenShift file "result-imagestream.yaml" created  
```

It also supports creating buildconfig for build directive in a service. By default, it uses the remote repo for the current git branch as the source repo, and the current branch as the source branch for the build. You can specify a different source repo and branch using ``--build-repo`` and ``--build-branch`` options respectively.

```sh
kompose --provider openshift --file buildconfig/docker-compose.yml convert
```

```none
WARN [foo] Service cannot be created because of missing port.
INFO OpenShift Buildconfig using git@github.com:rtnpro/kompose.git::master as source.
INFO OpenShift file "foo-deploymentconfig.yaml" created     
INFO OpenShift file "foo-imagestream.yaml" created          
INFO OpenShift file "foo-buildconfig.yaml" created
```

{{< note >}}
If you are manually pushing the OpenShift artifacts using ``oc create -f``, you need to ensure that you push the imagestream artifact before the buildconfig artifact, to workaround this OpenShift issue: https://github.com/openshift/origin/issues/4518 .
{{< /note >}}

## `kompose up`

Kompose supports a straightforward way to deploy your "composed" application to Kubernetes or OpenShift via `kompose up`.

### Kubernetes `kompose up` example

```shell
kompose --file ./examples/docker-guestbook.yml up
```

```none
We are going to create Kubernetes deployments and services for your Dockerized application.
If you need different kind of resources, use the 'kompose convert' and 'kubectl apply -f' commands instead.

INFO Successfully created service: redis-master
INFO Successfully created service: redis-slave
INFO Successfully created service: frontend
INFO Successfully created deployment: redis-master
INFO Successfully created deployment: redis-slave
INFO Successfully created deployment: frontend

Your application has been deployed to Kubernetes. You can run 'kubectl get deployment,svc,pods' for details.
```

```shell
kubectl get deployment,svc,pods
```

```none
NAME                                              DESIRED       CURRENT       UP-TO-DATE   AVAILABLE   AGE
deployment.extensions/frontend                    1             1             1            1           4m
deployment.extensions/redis-master                1             1             1            1           4m
deployment.extensions/redis-slave                 1             1             1            1           4m

NAME                         TYPE               CLUSTER-IP    EXTERNAL-IP   PORT(S)      AGE
service/frontend             ClusterIP          10.0.174.12   <none>        80/TCP       4m
service/kubernetes           ClusterIP          10.0.0.1      <none>        443/TCP      13d
service/redis-master         ClusterIP          10.0.202.43   <none>        6379/TCP     4m
service/redis-slave          ClusterIP          10.0.1.85     <none>        6379/TCP     4m

NAME                                READY         STATUS        RESTARTS     AGE
pod/frontend-2768218532-cs5t5       1/1           Running       0            4m
pod/redis-master-1432129712-63jn8   1/1           Running       0            4m
pod/redis-slave-2504961300-nve7b    1/1           Running       0            4m
```

{{< note >}}

- You must have a running Kubernetes cluster with a pre-configured kubectl context.
- Only deployments and services are generated and deployed to Kubernetes. If you need different kind of resources, use the `kompose convert` and `kubectl apply -f` commands instead.
{{< /note >}}

### OpenShift `kompose up` example

```shell
kompose --file ./examples/docker-guestbook.yml --provider openshift up
```

```none
We are going to create OpenShift DeploymentConfigs and Services for your Dockerized application.
If you need different kind of resources, use the 'kompose convert' and 'oc create -f' commands instead.

INFO Successfully created service: redis-slave    
INFO Successfully created service: frontend       
INFO Successfully created service: redis-master   
INFO Successfully created deployment: redis-slave
INFO Successfully created ImageStream: redis-slave
INFO Successfully created deployment: frontend    
INFO Successfully created ImageStream: frontend   
INFO Successfully created deployment: redis-master
INFO Successfully created ImageStream: redis-master

Your application has been deployed to OpenShift. You can run 'oc get dc,svc,is' for details.
```

```shell
oc get dc,svc,is
```

```none
NAME               REVISION                              DESIRED       CURRENT    TRIGGERED BY
dc/frontend        0                                     1             0          config,image(frontend:v4)
dc/redis-master    0                                     1             0          config,image(redis-master:e2e)
dc/redis-slave     0                                     1             0          config,image(redis-slave:v1)
NAME               CLUSTER-IP                            EXTERNAL-IP   PORT(S)    AGE
svc/frontend       172.30.46.64                          <none>        80/TCP     8s
svc/redis-master   172.30.144.56                         <none>        6379/TCP   8s
svc/redis-slave    172.30.75.245                         <none>        6379/TCP   8s
NAME               DOCKER REPO                           TAGS          UPDATED
is/frontend        172.30.12.200:5000/fff/frontend                     
is/redis-master    172.30.12.200:5000/fff/redis-master                 
is/redis-slave     172.30.12.200:5000/fff/redis-slave    v1  
```

{{< note >}}
You must have a running OpenShift cluster with a pre-configured `oc` context (`oc login`).
{{< /note >}}

## `kompose down`

Once you have deployed "composed" application to Kubernetes, `kompose down` will help you to take the application out by deleting its deployments and services. If you need to remove other resources, use the 'kubectl' command.

```shell
kompose --file docker-guestbook.yml down
INFO Successfully deleted service: redis-master   
INFO Successfully deleted deployment: redis-master
INFO Successfully deleted service: redis-slave    
INFO Successfully deleted deployment: redis-slave
INFO Successfully deleted service: frontend       
INFO Successfully deleted deployment: frontend
```

{{< note >}}
You must have a running Kubernetes cluster with a pre-configured `kubectl` context.
{{< /note >}}

## Build and Push Docker Images

Kompose supports both building and pushing Docker images. When using the `build` key within your Docker Compose file, your image will:

- Automatically be built with Docker using the `image` key specified within your file
- Be pushed to the correct Docker repository using local credentials (located at `.docker/config`)

Using an [example Docker Compose file](https://raw.githubusercontent.com/kubernetes/kompose/master/examples/buildconfig/docker-compose.yml):

```yaml
version: "2"

services:
    foo:
        build: "./build"
        image: docker.io/foo/bar
```

Using `kompose up` with a `build` key:

```none
kompose up
INFO Build key detected. Attempting to build and push image 'docker.io/foo/bar'
INFO Building image 'docker.io/foo/bar' from directory 'build'
INFO Image 'docker.io/foo/bar' from directory 'build' built successfully
INFO Pushing image 'foo/bar:latest' to registry 'docker.io'
INFO Attempting authentication credentials 'https://index.docker.io/v1/
INFO Successfully pushed image 'foo/bar:latest' to registry 'docker.io'
INFO We are going to create Kubernetes Deployments, Services and PersistentVolumeClaims for your Dockerized application. If you need different kind of resources, use the 'kompose convert' and 'kubectl apply -f' commands instead.

INFO Deploying application in "default" namespace
INFO Successfully created Service: foo            
INFO Successfully created Deployment: foo         

Your application has been deployed to Kubernetes. You can run 'kubectl get deployment,svc,pods,pvc' for details.
```

In order to disable the functionality, or choose to use BuildConfig generation (with OpenShift) `--build (local|build-config|none)` can be passed.

```sh
# Disable building/pushing Docker images
kompose up --build none

# Generate Build Config artifacts for OpenShift
kompose up --provider openshift --build build-config
```

## Alternative Conversions

The default `kompose` transformation will generate Kubernetes [Deployments](/docs/concepts/workloads/controllers/deployment/) and [Services](/docs/concepts/services-networking/service/), in yaml format. You have alternative option to generate json with `-j`. Also, you can alternatively generate [Replication Controllers](/docs/concepts/workloads/controllers/replicationcontroller/) objects, [Daemon Sets](/docs/concepts/workloads/controllers/daemonset/), or [Helm](https://github.com/helm/helm) charts.

```sh
kompose convert -j
INFO Kubernetes file "redis-svc.json" created
INFO Kubernetes file "web-svc.json" created
INFO Kubernetes file "redis-deployment.json" created
INFO Kubernetes file "web-deployment.json" created
```

The `*-deployment.json` files contain the Deployment objects.

```sh
kompose convert --replication-controller
INFO Kubernetes file "redis-svc.yaml" created
INFO Kubernetes file "web-svc.yaml" created
INFO Kubernetes file "redis-replicationcontroller.yaml" created
INFO Kubernetes file "web-replicationcontroller.yaml" created
```

The `*-replicationcontroller.yaml` files contain the Replication Controller objects. If you want to specify replicas (default is 1), use `--replicas` flag: `kompose convert --replication-controller --replicas 3`

```shell
kompose convert --daemon-set
INFO Kubernetes file "redis-svc.yaml" created
INFO Kubernetes file "web-svc.yaml" created
INFO Kubernetes file "redis-daemonset.yaml" created
INFO Kubernetes file "web-daemonset.yaml" created
```

The `*-daemonset.yaml` files contain the DaemonSet objects

If you want to generate a Chart to be used with [Helm](https://github.com/kubernetes/helm) run:

```shell
kompose convert -c
```

```none
INFO Kubernetes file "web-svc.yaml" created
INFO Kubernetes file "redis-svc.yaml" created
INFO Kubernetes file "web-deployment.yaml" created
INFO Kubernetes file "redis-deployment.yaml" created
chart created in "./docker-compose/"
```

```shell
tree docker-compose/
```

```none
docker-compose
├── Chart.yaml
├── README.md
└── templates
    ├── redis-deployment.yaml
    ├── redis-svc.yaml
    ├── web-deployment.yaml
    └── web-svc.yaml
```

The chart structure is aimed at providing a skeleton for building your Helm charts.

## Labels

`kompose` supports Kompose-specific labels within the `docker-compose.yml` file in order to explicitly define a service's behavior upon conversion.

- `kompose.service.type` defines the type of service to be created.

For example:

```yaml
version: "2"
services:
  nginx:
    image: nginx
    dockerfile: foobar
    build: ./foobar
    cap_add:
      - ALL
    container_name: foobar
    labels:
      kompose.service.type: nodeport
```

- `kompose.service.expose` defines if the service needs to be made accessible from outside the cluster or not. If the value is set to "true", the provider sets the endpoint automatically, and for any other value, the value is set as the hostname. If multiple ports are defined in a service, the first one is chosen to be the exposed.
  - For the Kubernetes provider, an ingress resource is created and it is assumed that an ingress controller has already been configured.
  - For the OpenShift provider, a route is created.

For example:

```yaml
version: "2"
services:
  web:
    image: tuna/docker-counter23
    ports:
     - "5000:5000"
    links:
     - redis
    labels:
      kompose.service.expose: "counter.example.com"
  redis:
    image: redis:3.0
    ports:
     - "6379"
```

The currently supported options are:

| Key                  | Value                               |
|----------------------|-------------------------------------|
| kompose.service.type | nodeport / clusterip / loadbalancer |
| kompose.service.expose| true / hostname |

{{< note >}}
The `kompose.service.type` label should be defined with `ports` only, otherwise `kompose` will fail.
{{< /note >}}

## Restart

If you want to create normal pods without controllers you can use `restart` construct of docker-compose to define that. Follow table below to see what happens on the `restart` value.

| `docker-compose` `restart` | object created    | Pod `restartPolicy` |
|----------------------------|-------------------|---------------------|
| `""`                       | controller object | `Always`            |
| `always`                   | controller object | `Always`            |
| `on-failure`               | Pod               | `OnFailure`         |
| `no`                       | Pod               | `Never`             |

{{< note >}}
The controller object could be `deployment` or `replicationcontroller`.
{{< /note >}}

For example, the `pival` service will become pod down here. This container calculated value of `pi`.

```yaml
version: '2'

services:
  pival:
    image: perl
    command: ["perl",  "-Mbignum=bpi", "-wle", "print bpi(2000)"]
    restart: "on-failure"
```

### Warning about Deployment Configurations

If the Docker Compose file has a volume specified for a service, the Deployment (Kubernetes) or DeploymentConfig (OpenShift) strategy is changed to "Recreate" instead of "RollingUpdate" (default). This is done to avoid multiple instances of a service from accessing a volume at the same time.

If the Docker Compose file has service name with `_` in it (eg.`web_service`), then it will be replaced by `-` and the service name will be renamed accordingly (eg.`web-service`). Kompose does this because "Kubernetes" doesn't allow `_` in object name.

Please note that changing service name might break some `docker-compose` files.

## Docker Compose Versions

Kompose supports Docker Compose versions: 1, 2 and 3. We have limited support on versions 2.1 and 3.2 due to their experimental nature.

A full list on compatibility between all three versions is listed in our [conversion document](https://github.com/kubernetes/kompose/blob/master/docs/conversion.md) including a list of all incompatible Docker Compose keys.
