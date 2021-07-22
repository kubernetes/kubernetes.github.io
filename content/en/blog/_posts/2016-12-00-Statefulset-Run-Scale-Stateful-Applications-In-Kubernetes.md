---
title: " StatefulSet: Run and Scale Stateful Applications Easily in Kubernetes "
date: 2016-12-20
slug: statefulset-run-scale-stateful-applications-in-kubernetes
url: /blog/2016/12/Statefulset-Run-Scale-Stateful-Applications-In-Kubernetes
---
_Editor’s note: this post is part of a [series of in-depth articles](https://kubernetes.io/blog/2016/12/five-days-of-kubernetes-1-5/) on what's new in Kubernetes 1.5_

In the latest release, [Kubernetes 1.5](https://kubernetes.io/blog/2016/12/kubernetes-1-5-supporting-production-workloads/), we’ve moved the feature formerly known as PetSet into beta as [StatefulSet](/docs/concepts/abstractions/controllers/statefulsets/). There were no major changes to the API Object, other than the community selected name, but we added the semantics of “at most one pod per index” for deployment of the Pods in the set. Along with ordered deployment, ordered termination, unique network names, and persistent stable storage, we think we have the right primitives to support many containerized stateful workloads. We don’t claim that the feature is 100% complete (it is software after all), but we believe that it is useful in its current form, and that we can extend the API in a backwards-compatible way as we progress toward an eventual GA release.

**When is StatefulSet the Right Choice for my Storage Application?**  

[Deployments](/docs/user-guide/deployments/) and [ReplicaSets](/docs/user-guide/replicasets/) are a great way to run stateless replicas of an application on Kubernetes, but their semantics aren’t really right for deploying stateful applications. The purpose of StatefulSet is to provide a controller with the correct semantics for deploying a wide range of stateful workloads. However, moving your storage application onto Kubernetes isn’t always the correct choice. Before you go all in on converging your storage tier and your orchestration framework, you should ask yourself a few questions.  

**Can your application run using remote storage or does it require local storage media?**  

Currently, we recommend using StatefulSets with remote storage. Therefore, you must be ready to tolerate the performance implications of network attached storage. Even with storage optimized instances, you won’t likely realize the same performance as locally attached, solid state storage media. Does the performance of network attached storage, on your cloud, allow your storage application to meet its SLAs? If so, running your application in a StatefulSet provides compelling benefits from the perspective of automation. If the node on which your storage application is running fails, the Pod containing the application can be rescheduled onto another node, and, as it’s using network attached storage media, its data are still available after it’s rescheduled.  

**Do you need to scale your storage application?**  

What is the benefit you hope to gain by running your application in a StatefulSet? Do you have a single instance of your storage application for your entire organization? Is scaling your storage application a problem that you actually have? If you have a few instances of your storage application, and they are successfully meeting the demands of your organization, and those demands are not rapidly increasing, you’re already at a local optimum.   

If, however, you have an ecosystem of microservices, or if you frequently stamp out new service footprints that include storage applications, then you might benefit from automation and consolidation.  If you’re already using Kubernetes to manage the stateless tiers of your ecosystem, you should consider using the same infrastructure to manage your storage applications.  

**How important is predictable performance?**  

Kubernetes doesn’t yet support isolation for network or storage I/O across containers. Colocating your storage application with a noisy neighbor can reduce the QPS that your application can handle. You can mitigate this by scheduling the Pod containing your storage application as the only tenant on a node (thus providing it a dedicated machine) or by using Pod anti-affinity rules to segregate Pods that contend for network or disk, but this means that you have to actively identify and mitigate hot spots.  

If squeezing the absolute maximum QPS out of your storage application isn’t your primary concern, if you’re willing and able to mitigate hotspots to ensure your storage applications meet their SLAs, and if the ease of turning up new "footprints" (services or collections of services), scaling them, and flexibly re-allocating resources is your primary concern, Kubernetes and StatefulSet might be the right solution to address it.  

**Does your application require specialized hardware or instance types?**  

If you run your storage application on high-end hardware or extra-large instance sizes, and your other workloads on commodity hardware or smaller, less expensive images, you may not want to deploy a heterogenous cluster. If you can standardize on a single instance size for all types of apps, then you may benefit from the flexible resource reallocation and consolidation, that you get from Kubernetes.  

**A Practical Example - ZooKeeper**  

[ZooKeeper](https://zookeeper.apache.org/doc/current/) is an interesting use case for StatefulSet for two reasons. First, it demonstrates that StatefulSet can be used to run a distributed, strongly consistent storage application on Kubernetes. Second, it's a prerequisite for running workloads like [Apache Hadoop](http://hadoop.apache.org/) and [Apache Kakfa](https://kafka.apache.org/) on Kubernetes. An [in-depth tutorial](/docs/tutorials/stateful-application/zookeeper/) on deploying a ZooKeeper ensemble on Kubernetes is available in the Kubernetes documentation, and we’ll outline a few of the key features below.  

**Creating a ZooKeeper Ensemble**  
Creating an ensemble is as simple as using [kubectl create](/docs/reference/generated/kubectl/kubectl-commands#create) to generate the objects stored in the manifest.  


```
$ kubectl create -f [http://k8s.io/docs/tutorials/stateful-application/zookeeper.yaml](https://raw.githubusercontent.com/kubernetes/kubernetes.github.io/master/docs/tutorials/stateful-application/zookeeper.yaml)

service "zk-headless" created

configmap "zk-config" created

poddisruptionbudget "zk-budget" created

statefulset "zk" created
 ```


When you create the manifest, the StatefulSet controller creates each Pod, with respect to its ordinal, and waits for each to be Running and Ready prior to creating its successor.  



```
$ kubectl get -w -l app=zk

NAME      READY     STATUS    RESTARTS   AGE

zk-0      0/1       Pending   0          0s

zk-0      0/1       Pending   0         0s

zk-0      0/1       Pending   0         7s

zk-0      0/1       ContainerCreating   0         7s

zk-0      0/1       Running   0         38s

zk-0      1/1       Running   0         58s

zk-1      0/1       Pending   0         1s

zk-1      0/1       Pending   0         1s

zk-1      0/1       ContainerCreating   0         1s

zk-1      0/1       Running   0         33s

zk-1      1/1       Running   0         51s

zk-2      0/1       Pending   0         0s

zk-2      0/1       Pending   0         0s

zk-2      0/1       ContainerCreating   0         0s

zk-2      0/1       Running   0         25s

zk-2      1/1       Running   0         40s
 ```



Examining the hostnames of each Pod in the StatefulSet, you can see that the Pods’ hostnames also contain the Pods’ ordinals.  




```
$ for i in 0 1 2; do kubectl exec zk-$i -- hostname; done

zk-0

zk-1

zk-2
 ```



ZooKeeper stores the unique identifier of each server in a file called “myid”. The identifiers used for ZooKeeper servers are just natural numbers. For the servers in the ensemble, the “myid” files are populated by adding one to the ordinal extracted from the Pods’ hostnames.  


```
$ for i in 0 1 2; do echo "myid zk-$i";kubectl exec zk-$i -- cat /var/lib/zookeeper/data/myid; done

myid zk-0

1

myid zk-1

2

myid zk-2

3
 ```



Each Pod has a unique network address based on its hostname and the network domain controlled by the zk-headless Headless Service.  





```
$  for i in 0 1 2; do kubectl exec zk-$i -- hostname -f; done

zk-0.zk-headless.default.svc.cluster.local

zk-1.zk-headless.default.svc.cluster.local

zk-2.zk-headless.default.svc.cluster.local
 ```



The combination of a unique Pod ordinal and a unique network address allows you to populate the ZooKeeper servers’ configuration files with a consistent ensemble membership.  



```
$  kubectl exec zk-0 -- cat /opt/zookeeper/conf/zoo.cfg

clientPort=2181

dataDir=/var/lib/zookeeper/data

dataLogDir=/var/lib/zookeeper/log

tickTime=2000

initLimit=10

syncLimit=2000

maxClientCnxns=60

minSessionTimeout= 4000

maxSessionTimeout= 40000

autopurge.snapRetainCount=3

autopurge.purgeInteval=1

server.1=zk-0.zk-headless.default.svc.cluster.local:2888:3888

server.2=zk-1.zk-headless.default.svc.cluster.local:2888:3888

server.3=zk-2.zk-headless.default.svc.cluster.local:2888:3888
 ```



StatefulSet lets you deploy ZooKeeper in a consistent and reproducible way. You won’t create more than one server with the same id, the servers can find each other via a stable network addresses, and they can perform leader election and replicate writes because the ensemble has consistent membership.  


The simplest way to verify that the ensemble works is to write a value to one server and to read it from another. You can use the “zkCli.sh” script that ships with the ZooKeeper distribution, to create a ZNode containing some data.  




```
$  kubectl exec zk-0 zkCli.sh create /hello world

...


WATCHER::


WatchedEvent state:SyncConnected type:None path:null

Created /hello
 ```



You can use the same script to read the data from another server in the ensemble.  




```
$  kubectl exec zk-1 zkCli.sh get /hello

...


WATCHER::


WatchedEvent state:SyncConnected type:None path:null

world

...
 ```


You can take the ensemble down by deleting the zk StatefulSet.  




```
$  kubectl delete statefulset zk

statefulset "zk" deleted
 ```



The cascading delete destroys each Pod in the StatefulSet, with respect to the reverse order of the Pods’ ordinals, and it waits for each to terminate completely before terminating its predecessor.




```
$  kubectl get pods -w -l app=zk

NAME      READY     STATUS    RESTARTS   AGE

zk-0      1/1       Running   0          14m

zk-1      1/1       Running   0          13m

zk-2      1/1       Running   0          12m

NAME      READY     STATUS        RESTARTS   AGE

zk-2      1/1       Terminating   0          12m

zk-1      1/1       Terminating   0         13m

zk-0      1/1       Terminating   0         14m

zk-2      0/1       Terminating   0         13m

zk-2      0/1       Terminating   0         13m

zk-2      0/1       Terminating   0         13m

zk-1      0/1       Terminating   0         14m

zk-1      0/1       Terminating   0         14m

zk-1      0/1       Terminating   0         14m

zk-0      0/1       Terminating   0         15m

zk-0      0/1       Terminating   0         15m

zk-0      0/1       Terminating   0         15m
 ```





You can use [kubectl apply](/docs/reference/generated/kubectl/kubectl-commands#apply) to recreate the zk StatefulSet and redeploy the ensemble.






```
$  kubectl apply -f [http://k8s.io/docs/tutorials/stateful-application/zookeeper.yaml](https://raw.githubusercontent.com/kubernetes/kubernetes.github.io/master/docs/tutorials/stateful-application/zookeeper.yaml)

service "zk-headless" configured

configmap "zk-config" configured

statefulset "zk" created
 ```



If you use the “zkCli.sh” script to get the value entered prior to deleting the StatefulSet, you will find that the ensemble still serves the data.




```
$  kubectl exec zk-2 zkCli.sh get /hello

...


WATCHER::


WatchedEvent state:SyncConnected type:None path:null

world

...
 ```



StatefulSet ensures that, even if all Pods in the StatefulSet are destroyed, when they are rescheduled, the ZooKeeper ensemble can elect a new leader and continue to serve requests.



**Tolerating Node Failures**



ZooKeeper replicates its state machine to different servers in the ensemble for the explicit purpose of tolerating node failure. By default, the Kubernetes Scheduler could deploy more than one Pod in the zk StatefulSet to the same node. If the zk-0 and zk-1 Pods were deployed on the same node, and that node failed, the ZooKeeper ensemble couldn’t form a quorum to commit writes, and the ZooKeeper service would experience an outage until one of the Pods could be rescheduled.



You should always provision headroom capacity for critical processes in your cluster, and if you do, in this instance, the Kubernetes Scheduler will reschedule the Pods on another node and the outage will be brief.



If the SLAs for your service preclude even brief outages due to a single node failure, you should use a [PodAntiAffinity](/docs/user-guide/node-selection/) annotation. The manifest used to create the ensemble contains such an annotation, and it tells the Kubernetes Scheduler to not place more than one Pod from the zk StatefulSet on the same node.





**Tolerating Planned Maintenance**




The manifest used to create the ZooKeeper ensemble also creates a [PodDistruptionBudget](/docs/admin/disruptions/), zk-budget. The zk-budget informs Kubernetes about the upper limit of disruptions (unhealthy Pods) that the service can tolerate.




```
 {

              "podAntiAffinity": {

                "requiredDuringSchedulingRequiredDuringExecution": [{

                  "labelSelector": {

                    "matchExpressions": [{

                      "key": "app",

                      "operator": "In",

                      "values": ["zk-headless"]

                    }]

                  },

                  "topologyKey": "kubernetes.io/hostname"

                }]

              }

            }

}
 ```




```
$ kubectl get poddisruptionbudget zk-budget

NAME        MIN-AVAILABLE   ALLOWED-DISRUPTIONS   AGE

zk-budget   2               1                     2h
 ```





zk-budget indicates that at least two members of the ensemble must be available at all times for the ensemble to be healthy. If you attempt to drain a node prior taking it offline, and if draining it would terminate a Pod that violates the budget, the drain operation will fail. If you use [kubectl drain](/docs/reference/generated/kubectl/kubectl-commands#drain), in conjunction with PodDisruptionBudgets, to cordon your nodes and to evict all Pods prior to maintenance or decommissioning, you can ensure that the procedure won’t be disruptive to your stateful applications.




**Looking Forward**



As the Kubernetes development looks towards GA, we are looking at a long list of suggestions from users. If you want to dive into our backlog, checkout the [GitHub issues with the stateful label](https://github.com/kubernetes/kubernetes/labels/area%2Fstateful-apps). However, as the resulting API would be hard to comprehend, we don't expect to implement all of these feature requests. Some feature requests, like support for rolling updates, better integration with node upgrades, and using fast local storage, would benefit most types of stateful applications, and we expect to prioritize these. The intention of StatefulSet is to be able to run a large number of applications well, and not to be able to run all applications perfectly. With this in mind, we avoided implementing StatefulSets in a way that relied on hidden mechanisms or inaccessible features. Anyone can write a controller that works similarly to StatefulSets. We call this "making it forkable."

Over the next year, we expect many popular storage applications to each have their own community-supported, dedicated controllers or "[operators](https://coreos.com/blog/introducing-operators.html)". We've already heard of work on custom controllers for etcd, Redis, and ZooKeeper. We expect to write some more ourselves and to support the community in developing others.   



The Operators for [etcd](https://coreos.com/blog/introducing-the-etcd-operator.html) and [Prometheus](https://coreos.com/blog/the-prometheus-operator.html) from CoreOS, demonstrate an approach to running stateful applications on Kubernetes that provides a level of automation and integration beyond that which is possible with StatefulSet alone. On the other hand, using a generic controller like StatefulSet or Deployment means that a wide range of applications can be managed by understanding a single config object. We think Kubernetes users will appreciate having the choice of these two approaches.



_--Kenneth Owens & Eric Tune, Software Engineers, Google_



- [Download](http://get.k8s.io/) Kubernetes
- Get involved with the Kubernetes project on [GitHub](https://github.com/kubernetes/kubernetes)
- Post questions (or answer questions) on [Stack Overflow](http://stackoverflow.com/questions/tagged/kubernetes)
- Connect with the community on [Slack](http://slack.k8s.io/)
- Follow us on Twitter [@Kubernetesio](https://twitter.com/kubernetesio) for latest updates
