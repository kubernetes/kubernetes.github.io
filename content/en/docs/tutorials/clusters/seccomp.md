---
reviewers:
- hasheddan
- pjbgf
- saschagrunert
title: Restrict a Container's Syscalls with seccomp
content_type: tutorial
weight: 20
min-kubernetes-server-version: v1.22
---

<!-- overview -->

{{< feature-state for_k8s_version="v1.19" state="stable" >}}

Seccomp stands for secure computing mode and has been a feature of the Linux
kernel since version 2.6.12. It can be used to sandbox the privileges of a
process, restricting the calls it is able to make from userspace into the
kernel. Kubernetes lets you automatically apply seccomp profiles loaded onto a
Node to your Pods and containers.

Identifying the privileges required for your workloads can be difficult. In this
tutorial, you will go through how to load seccomp profiles into a local
Kubernetes cluster, how to apply them to a Pod, and how you can begin to craft
profiles that give only the necessary privileges to your container processes.

## {{% heading "objectives" %}}

* Learn how to load seccomp profiles on a node
* Learn how to apply a seccomp profile to a container
* Observe auditing of syscalls made by a container process
* Observe behavior when a missing profile is specified
* Observe a violation of a seccomp profile
* Learn how to create fine-grained seccomp profiles
* Learn how to apply a container runtime default seccomp profile

## {{% heading "prerequisites" %}}

{{< version-check >}}

In order to complete all steps in this tutorial, you must install
[kind](https://kind.sigs.k8s.io/docs/user/quick-start/) and
[kubectl](/docs/tasks/tools/). This tutorial will show examples
both alpha (new in v1.22) and generally available seccomp functionality. You should
make sure that your cluster is [configured
correctly](https://kind.sigs.k8s.io/docs/user/quick-start/#setting-kubernetes-version)
for the version you are using.

<!-- steps -->

## Enable the use of `RuntimeDefault` as the default seccomp profile for all workloads

{{< feature-state state="alpha" for_k8s_version="v1.22" >}}

`SeccompDefault` is an optional kubelet
[feature gate](/docs/reference/command-line-tools-reference/feature-gates) as
well as corresponding `--seccomp-default`
[command line flag](/docs/reference/command-line-tools-reference/kubelet).
Both have to be enabled simultaneously to use the feature.

If enabled, the kubelet will use the `RuntimeDefault` seccomp profile by default, which is 
defined by the container runtime, instead of using the `Unconfined` (seccomp disabled) mode. 
The default profiles aim to provide a strong set
of security defaults while preserving the functionality of the workload. It is
possible that the default profiles differ between container runtimes and their
release versions, for example when comparing those from CRI-O and containerd.

Some workloads may require a lower amount of syscall restrictions than others.
This means that they can fail during runtime even with the `RuntimeDefault`
profile. To mitigate such a failure, you can:

- Run the workload explicitly as `Unconfined`.
- Disable the `SeccompDefault` feature for the nodes. Also making sure that
  workloads get scheduled on nodes where the feature is disabled.
- Create a custom seccomp profile for the workload.

If you were introducing this feature into production-like cluster, the Kubernetes project
recommends that you enable this feature gate on a subset of your nodes and then
test workload execution before rolling the change out cluster-wide.

More detailed information about a possible upgrade and downgrade strategy can be
found in the [related Kubernetes Enhancement Proposal (KEP)](https://github.com/kubernetes/enhancements/tree/a70cc18/keps/sig-node/2413-seccomp-by-default#upgrade--downgrade-strategy).

Since the feature is in alpha state it is disabled per default. To enable it,
pass the flags `--feature-gates=SeccompDefault=true --seccomp-default` to the
`kubelet` CLI or enable it via the [kubelet configuration
file](/docs/tasks/administer-cluster/kubelet-config-file/). To enable the
feature gate in [kind](https://kind.sigs.k8s.io), ensure that `kind` provides
the minimum required Kubernetes version and enables the `SeccompDefault` feature
[in the kind configuration](https://kind.sigs.k8s.io/docs/user/quick-start/#enable-feature-gates-in-your-cluster):

```yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
featureGates:
  SeccompDefault: true
```

## Create Seccomp Profiles

The contents of these profiles will be explored later on, but for now go ahead
and download them into a directory named `profiles/` so that they can be loaded
into the cluster.

{{< tabs name="tab_with_code" >}}
{{{< tab name="audit.json" >}}
{{< codenew file="pods/security/seccomp/profiles/audit.json" >}}
{{< /tab >}}
{{< tab name="violation.json" >}}
{{< codenew file="pods/security/seccomp/profiles/violation.json" >}}
{{< /tab >}}}
{{< tab name="fine-grained.json" >}}
{{< codenew file="pods/security/seccomp/profiles/fine-grained.json" >}}
{{< /tab >}}}
{{< /tabs >}}

## Create a Local Kubernetes Cluster with Kind

For simplicity, [kind](https://kind.sigs.k8s.io/) can be used to create a single
node cluster with the seccomp profiles loaded. Kind runs Kubernetes in Docker,
so each node of the cluster is a container. This allows for files
to be mounted in the filesystem of each container similar to loading files
onto a node.

{{< codenew file="pods/security/seccomp/kind.yaml" >}}
<br>

Download the example above, and save it to a file named `kind.yaml`. Then create
the cluster with the configuration.

```
kind create cluster --config=kind.yaml
```

Once the cluster is ready, identify the container running as the single node
cluster:

```
docker ps
```

You should see output indicating that a container is running with name
`kind-control-plane`.

```
CONTAINER ID        IMAGE                  COMMAND                  CREATED             STATUS              PORTS                       NAMES
6a96207fed4b        kindest/node:v1.18.2   "/usr/local/bin/entr…"   27 seconds ago      Up 24 seconds       127.0.0.1:42223->6443/tcp   kind-control-plane
```

If observing the filesystem of that container, one should see that the
`profiles/` directory has been successfully loaded into the default seccomp path
of the kubelet. Use `docker exec` to run a command in the Pod:

```
docker exec -it 6a96207fed4b ls /var/lib/kubelet/seccomp/profiles
```

```
audit.json  fine-grained.json  violation.json
```

## Create a Pod with a seccomp profile for syscall auditing

To start off, apply the `audit.json` profile, which will log all syscalls of the
process, to a new Pod.

Download the correct manifest for your Kubernetes version:

{{< tabs name="audit_pods" >}}
{{< tab name="v1.19 or Later (GA)" >}}
{{< codenew file="pods/security/seccomp/ga/audit-pod.yaml" >}}
{{< /tab >}}}
{{{< tab name="Pre-v1.19 (alpha)" >}}
{{< codenew file="pods/security/seccomp/alpha/audit-pod.yaml" >}}
{{< /tab >}}
{{< /tabs >}}
<br>

Create the Pod in the cluster:

```
kubectl apply -f audit-pod.yaml
```

This profile does not restrict any syscalls, so the Pod should start
successfully.

```
kubectl get pod/audit-pod
```

```
NAME        READY   STATUS    RESTARTS   AGE
audit-pod   1/1     Running   0          30s
```

In order to be able to interact with this endpoint exposed by this
container,create a NodePort Service that allows access to the endpoint from
inside the kind control plane container.

```
kubectl expose pod/audit-pod --type NodePort --port 5678
```

Check what port the Service has been assigned on the node.

```
kubectl get svc/audit-pod
```

```
NAME        TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
audit-pod   NodePort   10.111.36.142   <none>        5678:32373/TCP   72s
```

Now you can `curl` the endpoint from inside the kind control plane container at
the port exposed by this Service. Use `docker exec` to run a command in the Pod:

```
docker exec -it 6a96207fed4b curl localhost:32373
```

```
just made some syscalls!
```

You can see that the process is running, but what syscalls did it actually make?
Because this Pod is running in a local cluster, you should be able to see those
in `/var/log/syslog`. Open up a new terminal window and `tail` the output for
calls from `http-echo`:

```
tail -f /var/log/syslog | grep 'http-echo'
```

You should already see some logs of syscalls made by `http-echo`, and if you
`curl` the endpoint in the control plane container you will see more written.

```
Jul  6 15:37:40 my-machine kernel: [369128.669452] audit: type=1326 audit(1594067860.484:14536): auid=4294967295 uid=0 gid=0 ses=4294967295 pid=29064 comm="http-echo" exe="/http-echo" sig=0 arch=c000003e syscall=51 compat=0 ip=0x46fe1f code=0x7ffc0000
Jul  6 15:37:40 my-machine kernel: [369128.669453] audit: type=1326 audit(1594067860.484:14537): auid=4294967295 uid=0 gid=0 ses=4294967295 pid=29064 comm="http-echo" exe="/http-echo" sig=0 arch=c000003e syscall=54 compat=0 ip=0x46fdba code=0x7ffc0000
Jul  6 15:37:40 my-machine kernel: [369128.669455] audit: type=1326 audit(1594067860.484:14538): auid=4294967295 uid=0 gid=0 ses=4294967295 pid=29064 comm="http-echo" exe="/http-echo" sig=0 arch=c000003e syscall=202 compat=0 ip=0x455e53 code=0x7ffc0000
Jul  6 15:37:40 my-machine kernel: [369128.669456] audit: type=1326 audit(1594067860.484:14539): auid=4294967295 uid=0 gid=0 ses=4294967295 pid=29064 comm="http-echo" exe="/http-echo" sig=0 arch=c000003e syscall=288 compat=0 ip=0x46fdba code=0x7ffc0000
Jul  6 15:37:40 my-machine kernel: [369128.669517] audit: type=1326 audit(1594067860.484:14540): auid=4294967295 uid=0 gid=0 ses=4294967295 pid=29064 comm="http-echo" exe="/http-echo" sig=0 arch=c000003e syscall=0 compat=0 ip=0x46fd44 code=0x7ffc0000
Jul  6 15:37:40 my-machine kernel: [369128.669519] audit: type=1326 audit(1594067860.484:14541): auid=4294967295 uid=0 gid=0 ses=4294967295 pid=29064 comm="http-echo" exe="/http-echo" sig=0 arch=c000003e syscall=270 compat=0 ip=0x4559b1 code=0x7ffc0000
Jul  6 15:38:40 my-machine kernel: [369188.671648] audit: type=1326 audit(1594067920.488:14559): auid=4294967295 uid=0 gid=0 ses=4294967295 pid=29064 comm="http-echo" exe="/http-echo" sig=0 arch=c000003e syscall=270 compat=0 ip=0x4559b1 code=0x7ffc0000
Jul  6 15:38:40 my-machine kernel: [369188.671726] audit: type=1326 audit(1594067920.488:14560): auid=4294967295 uid=0 gid=0 ses=4294967295 pid=29064 comm="http-echo" exe="/http-echo" sig=0 arch=c000003e syscall=202 compat=0 ip=0x455e53 code=0x7ffc0000
```

You can begin to understand the syscalls required by the `http-echo` process by
looking at the `syscall=` entry on each line. While these are unlikely to
encompass all syscalls it uses, it can serve as a basis for a seccomp profile
for this container.

Clean up that Pod and Service before moving to the next section:

```
kubectl delete pod/audit-pod
kubectl delete svc/audit-pod
```

## Create Pod with seccomp Profile that Causes Violation

For demonstration, apply a profile to the Pod that does not allow for any
syscalls.

Download the correct manifest for your Kubernetes version:

{{< tabs name="violation_pods" >}}
{{< tab name="v1.19 or Later (GA)" >}}
{{< codenew file="pods/security/seccomp/ga/violation-pod.yaml" >}}
{{< /tab >}}}
{{{< tab name="Pre-v1.19 (alpha)" >}}
{{< codenew file="pods/security/seccomp/alpha/violation-pod.yaml" >}}
{{< /tab >}}
{{< /tabs >}}
<br>

Create the Pod in the cluster:

```
kubectl apply -f violation-pod.yaml
```

If you check the status of the Pod, you should see that it failed to start.

```
kubectl get pod/violation-pod
```

```
NAME            READY   STATUS             RESTARTS   AGE
violation-pod   0/1     CrashLoopBackOff   1          6s
```

As seen in the previous example, the `http-echo` process requires quite a few
syscalls. Here seccomp has been instructed to error on any syscall by setting
`"defaultAction": "SCMP_ACT_ERRNO"`. This is extremely secure, but removes the
ability to do anything meaningful. What you really want is to give workloads
only the privileges they need.

Clean up that Pod and Service before moving to the next section:

```
kubectl delete pod/violation-pod
kubectl delete svc/violation-pod
```

## Create Pod with seccomp Profile that Only Allows Necessary Syscalls

If you take a look at the `fine-pod.json`, you will notice some of the syscalls
seen in the first example where the profile set `"defaultAction":
"SCMP_ACT_LOG"`. Now the profile is setting `"defaultAction": "SCMP_ACT_ERRNO"`,
but explicitly allowing a set of syscalls in the `"action": "SCMP_ACT_ALLOW"`
block. Ideally, the container will run successfully and you will see no messages
sent to `syslog`.

Download the correct manifest for your Kubernetes version:

{{< tabs name="fine_pods" >}}
{{< tab name="v1.19 or Later (GA)" >}}
{{< codenew file="pods/security/seccomp/ga/fine-pod.yaml" >}}
{{< /tab >}}}
{{{< tab name="Pre-v1.19 (alpha)" >}}
{{< codenew file="pods/security/seccomp/alpha/fine-pod.yaml" >}}
{{< /tab >}}
{{< /tabs >}}
<br>

Create the Pod in your cluster:

```
kubectl apply -f fine-pod.yaml
```

The Pod should start successfully.

```
kubectl get pod/fine-pod
```

```
NAME        READY   STATUS    RESTARTS   AGE
fine-pod   1/1     Running   0          30s
```

Open up a new terminal window and `tail` the output for calls from `http-echo`:

```
tail -f /var/log/syslog | grep 'http-echo'
```

Expose the Pod with a NodePort Service:

```
kubectl expose pod/fine-pod --type NodePort --port 5678
```

Check what port the Service has been assigned on the node:

```
kubectl get svc/fine-pod
```

```
NAME        TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
fine-pod    NodePort   10.111.36.142   <none>        5678:32373/TCP   72s
```

`curl` the endpoint from inside the kind control plane container:

```
docker exec -it 6a96207fed4b curl localhost:32373
```

```
just made some syscalls!
```

You should see no output in the `syslog` because the profile allowed all
necessary syscalls and specified that an error should occur if one outside of
the list is invoked. This is an ideal situation from a security perspective, but
required some effort in analyzing the program. It would be nice if there was a
simple way to get closer to this security without requiring as much effort.

Clean up that Pod and Service before moving to the next section:

```
kubectl delete pod/fine-pod
kubectl delete svc/fine-pod
```

## Create Pod that uses the Container Runtime Default seccomp Profile

Most container runtimes provide a sane set of default syscalls that are allowed
or not. The defaults can easily be applied in Kubernetes by using the
`runtime/default` annotation or setting the seccomp type in the security context
of a pod or container to `RuntimeDefault`.

Download the correct manifest for your Kubernetes version:

{{< tabs name="default_pods" >}}
{{< tab name="v1.19 or Later (GA)" >}}
{{< codenew file="pods/security/seccomp/ga/default-pod.yaml" >}}
{{< /tab >}}}
{{{< tab name="Pre-v1.19 (alpha)" >}}
{{< codenew file="pods/security/seccomp/alpha/default-pod.yaml" >}}
{{< /tab >}}
{{< /tabs >}}
<br>

The default seccomp profile should provide adequate access for most workloads.

## {{% heading "whatsnext" %}}

Additional resources:

* [A seccomp Overview](https://lwn.net/Articles/656307/)
* [Seccomp Security Profiles for Docker](https://docs.docker.com/engine/security/seccomp/)
