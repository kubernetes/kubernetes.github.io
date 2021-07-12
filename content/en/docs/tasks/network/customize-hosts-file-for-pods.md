---
reviewers:
- rickypai
- thockin
title: Adding entries to Pod /etc/hosts with HostAliases
content_type: task
weight: 60
min-kubernetes-server-version: 1.7
---


<!-- overview -->

Adding entries to a Pod's `/etc/hosts` file provides Pod-level override of hostname resolution when DNS and other options are not applicable. You can add these custom entries with the HostAliases field in PodSpec.

Modification not using HostAliases is not suggested because the file is managed by the kubelet and can be overwritten on during Pod creation/restart.


<!-- steps -->

## Default hosts file content

Start an Nginx Pod which is assigned a Pod IP:

```shell
kubectl run nginx --image nginx
```

```
pod/nginx created
```

Examine a Pod IP:

```shell
kubectl get pods --output=wide
```

```
NAME     READY     STATUS    RESTARTS   AGE    IP           NODE
nginx    1/1       Running   0          13s    10.200.0.4   worker0
```

The hosts file content would look like this:

```shell
kubectl exec nginx -- cat /etc/hosts
```

```
# Kubernetes-managed hosts file.
127.0.0.1	localhost
::1	localhost ip6-localhost ip6-loopback
fe00::0	ip6-localnet
fe00::0	ip6-mcastprefix
fe00::1	ip6-allnodes
fe00::2	ip6-allrouters
10.200.0.4	nginx
```

By default, the `hosts` file only includes IPv4 and IPv6 boilerplates like
`localhost` and its own hostname.

## Adding additional entries with hostAliases

In addition to the default boilerplate, you can add additional entries to the
`hosts` file.
For example: to resolve `foo.local`, `bar.local` to `127.0.0.1` and `foo.remote`,
`bar.remote` to `10.1.2.3`, you can configure HostAliases for a Pod under
`.spec.hostAliases`:

{{< codenew file="service/networking/hostaliases-pod.yaml" >}}

You can start a Pod with that configuration by running:

```shell
kubectl apply -f https://k8s.io/examples/service/networking/hostaliases-pod.yaml
```

```
pod/hostaliases-pod created
```

Examine a Pod's details to see its IPv4 address and its status:

```shell
kubectl get pod --output=wide
```

```
NAME                           READY     STATUS      RESTARTS   AGE       IP              NODE
hostaliases-pod                0/1       Completed   0          6s        10.200.0.5      worker0
```

The `hosts` file content looks like this:

```shell
kubectl logs hostaliases-pod
```

```
# Kubernetes-managed hosts file.
127.0.0.1	localhost
::1	localhost ip6-localhost ip6-loopback
fe00::0	ip6-localnet
fe00::0	ip6-mcastprefix
fe00::1	ip6-allnodes
fe00::2	ip6-allrouters
10.200.0.5	hostaliases-pod

# Entries added by HostAliases.
127.0.0.1	foo.local	bar.local
10.1.2.3	foo.remote	bar.remote
```

with the additional entries specified at the bottom.

## Why does the kubelet manage the hosts file? {#why-does-kubelet-manage-the-hosts-file}

The kubelet [manages](https://github.com/kubernetes/kubernetes/issues/14633) the
`hosts` file for each container of the Pod to prevent Docker from
[modifying](https://github.com/moby/moby/issues/17190) the file after the
containers have already been started.

{{< caution >}}
Avoid making manual changes to the hosts file inside a container.

If you make manual changes to the hosts file,
those changes are lost when the container exits.
{{< /caution >}}
