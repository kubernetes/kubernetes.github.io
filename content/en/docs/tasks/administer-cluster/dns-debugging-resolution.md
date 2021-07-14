---
reviewers:
- bowei
- zihongz
title:  Debugging DNS Resolution
content_type: task
min-kubernetes-server-version: v1.6
---

<!-- overview -->
This page provides hints on diagnosing DNS problems.

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}}  
Your cluster must be configured to use the CoreDNS
{{< glossary_tooltip text="addon" term_id="addons" >}} or its precursor,
kube-dns.  

{{% version-check %}}

<!-- steps -->

### Create a simple Pod to use as a test environment

{{< codenew file="admin/dns/dnsutils.yaml" >}}

{{< note >}}
This example creates a pod in the `default` namespace. DNS name resolution for 
services depends on the namespace of the pod. For more information, review
[DNS for Services and Pods](/docs/concepts/services-networking/dns-pod-service/#what-things-get-dns-names). 
{{< /note >}}

Use that manifest to create a Pod:

```shell
kubectl apply -f https://k8s.io/examples/admin/dns/dnsutils.yaml
```
```
pod/dnsutils created
```
…and verify its status:
```shell
kubectl get pods dnsutils
```
```
NAME      READY     STATUS    RESTARTS   AGE
dnsutils   1/1       Running   0          <some-time>
```

Once that Pod is running, you can exec `nslookup` in that environment.
If you see something like the following, DNS is working correctly.

```shell
kubectl exec -i -t dnsutils -- nslookup kubernetes.default
```
```
Server:    10.0.0.10
Address 1: 10.0.0.10

Name:      kubernetes.default
Address 1: 10.0.0.1
```

If the `nslookup` command fails, check the following:

### Check the local DNS configuration first

Take a look inside the resolv.conf file.
(See [Inheriting DNS from the node](/docs/tasks/administer-cluster/dns-custom-nameservers/#inheriting-dns-from-the-node) and
[Known issues](#known-issues) below for more information)

```shell
kubectl exec -ti dnsutils -- cat /etc/resolv.conf
```

Verify that the search path and name server are set up like the following
(note that search path may vary for different cloud providers):

```
search default.svc.cluster.local svc.cluster.local cluster.local google.internal c.gce_project_id.internal
nameserver 10.0.0.10
options ndots:5
```

Errors such as the following indicate a problem with the CoreDNS (or kube-dns)
add-on or with associated Services:

```shell
kubectl exec -i -t dnsutils -- nslookup kubernetes.default
```
```
Server:    10.0.0.10
Address 1: 10.0.0.10

nslookup: can't resolve 'kubernetes.default'
```

or

```shell
kubectl exec -i -t dnsutils -- nslookup kubernetes.default
```
```
Server:    10.0.0.10
Address 1: 10.0.0.10 kube-dns.kube-system.svc.cluster.local

nslookup: can't resolve 'kubernetes.default'
```

### Check if the DNS pod is running

Use the `kubectl get pods` command to verify that the DNS pod is running.

```shell
kubectl get pods --namespace=kube-system -l k8s-app=kube-dns
```
```
NAME                       READY     STATUS    RESTARTS   AGE
...
coredns-7b96bf9f76-5hsxb   1/1       Running   0           1h
coredns-7b96bf9f76-mvmmt   1/1       Running   0           1h
...
```

{{< note >}}
The value for label `k8s-app` is `kube-dns` for both CoreDNS and kube-dns deployments.
{{< /note >}}


If you see that no CoreDNS Pod is running or that the Pod has failed/completed,
the DNS add-on may not be deployed by default in your current environment and you
will have to deploy it manually.

### Check for errors in the DNS pod

Use the `kubectl logs` command to see logs for the DNS containers.

For CoreDNS:
```shell
kubectl logs --namespace=kube-system -l k8s-app=kube-dns
```

Here is an example of a healthy CoreDNS log:

```
.:53
2018/08/15 14:37:17 [INFO] CoreDNS-1.2.2
2018/08/15 14:37:17 [INFO] linux/amd64, go1.10.3, 2e322f6
CoreDNS-1.2.2
linux/amd64, go1.10.3, 2e322f6
2018/08/15 14:37:17 [INFO] plugin/reload: Running configuration MD5 = 24e6c59e83ce706f07bcc82c31b1ea1c
```

See if there are any suspicious or unexpected messages in the logs.

### Is DNS service up?

Verify that the DNS service is up by using the `kubectl get service` command.

```shell
kubectl get svc --namespace=kube-system
```
```
NAME         TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)             AGE
...
kube-dns     ClusterIP   10.0.0.10      <none>        53/UDP,53/TCP        1h
...
```

{{< note >}}
The service name is `kube-dns` for both CoreDNS and kube-dns deployments.
{{< /note >}}



If you have created the Service or in the case it should be created by default
but it does not appear, see
[debugging Services](/docs/tasks/debug-application-cluster/debug-service/) for
more information.

### Are DNS endpoints exposed?

You can verify that DNS endpoints are exposed by using the `kubectl get endpoints`
command.

```shell
kubectl get endpoints kube-dns --namespace=kube-system
```
```
NAME       ENDPOINTS                       AGE
kube-dns   10.180.3.17:53,10.180.3.17:53    1h
```

If you do not see the endpoints, see the endpoints section in the
[debugging Services](/docs/tasks/debug-application-cluster/debug-service/) documentation.

For additional Kubernetes DNS examples, see the
[cluster-dns examples](https://github.com/kubernetes/examples/tree/master/staging/cluster-dns)
in the Kubernetes GitHub repository.

### Are DNS queries being received/processed?

You can verify if queries are being received by CoreDNS by adding the `log` plugin to the CoreDNS configuration (aka Corefile).
The CoreDNS Corefile is held in a {{< glossary_tooltip text="ConfigMap" term_id="configmap" >}} named `coredns`. To edit it, use the command:

```
kubectl -n kube-system edit configmap coredns
```

Then add `log` in the Corefile section per the example below:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: coredns
  namespace: kube-system
data:
  Corefile: |
    .:53 {
        log
        errors
        health
        kubernetes cluster.local in-addr.arpa ip6.arpa {
          pods insecure
          upstream
          fallthrough in-addr.arpa ip6.arpa
        }
        prometheus :9153
        forward . /etc/resolv.conf
        cache 30
        loop
        reload
        loadbalance
    }
```

After saving the changes, it may take up to minute or two for Kubernetes to propagate these changes to the CoreDNS pods.

Next, make some queries and view the logs per the sections above in this document. If CoreDNS pods are receiving the queries, you should see them in the logs.

Here is an example of a query in the log:

```
.:53
2018/08/15 14:37:15 [INFO] CoreDNS-1.2.0
2018/08/15 14:37:15 [INFO] linux/amd64, go1.10.3, 2e322f6
CoreDNS-1.2.0
linux/amd64, go1.10.3, 2e322f6
2018/09/07 15:29:04 [INFO] plugin/reload: Running configuration MD5 = 162475cdf272d8aa601e6fe67a6ad42f
2018/09/07 15:29:04 [INFO] Reloading complete
172.17.0.18:41675 - [07/Sep/2018:15:29:11 +0000] 59925 "A IN kubernetes.default.svc.cluster.local. udp 54 false 512" NOERROR qr,aa,rd,ra 106 0.000066649s
```

### Are you in the right namespace for the service?

DNS queries that don't specify a namespace are limited to the pod's 
namespace. 

If the namespace of the pod and service differ, the DNS query must include 
the namespace of the service.

This query is limited to the pod's namespace:
```shell
kubectl exec -i -t dnsutils -- nslookup <service-name>
```

This query specifies the namespace:
```shell
kubectl exec -i -t dnsutils -- nslookup <service-name>.<namespace>
```

To learn more about name resolution, see 
[DNS for Services and Pods](/docs/concepts/services-networking/dns-pod-service/#what-things-get-dns-names). 

## Known issues

Some Linux distributions (e.g. Ubuntu) use a local DNS resolver by default (systemd-resolved).
Systemd-resolved moves and replaces `/etc/resolv.conf` with a stub file that can cause a fatal forwarding
loop when resolving names in upstream servers. This can be fixed manually by using kubelet's `--resolv-conf` flag
to point to the correct `resolv.conf` (With `systemd-resolved`, this is `/run/systemd/resolve/resolv.conf`).
kubeadm automatically detects `systemd-resolved`, and adjusts the kubelet flags accordingly.

Kubernetes installs do not configure the nodes' `resolv.conf` files to use the
cluster DNS by default, because that process is inherently distribution-specific.
This should probably be implemented eventually.

Linux's libc (a.k.a. glibc) has a limit for the DNS `nameserver` records to 3 by default. What's more, for the glibc versions which are older than glibc-2.17-222 ([the new versions update see this issue](https://access.redhat.com/solutions/58028)), the allowed number of DNS `search` records has been limited to 6 ([see this bug from 2005](https://bugzilla.redhat.com/show_bug.cgi?id=168253)). Kubernetes needs to consume 1 `nameserver` record and 3 `search` records. This means that if a local installation already uses 3 `nameserver`s or uses more than 3 `search`es while your glibc version is in the affected list, some of those settings will be lost. To work around the DNS `nameserver` records limit, the node can run `dnsmasq`, which will provide more `nameserver` entries. You can also use kubelet's `--resolv-conf` flag. To fix the DNS `search` records limit, consider upgrading your linux distribution or upgrading to an unaffected version of glibc.

{{< note >}}

With [Expanded DNS Configuration](/docs/concepts/services-networking/dns-pod-service/#expanded-dns-configuration),
Kubernetes allows more DNS `search` records.

{{< /note >}}

If you are using Alpine version 3.3 or earlier as your base image, DNS may not
work properly due to a known issue with Alpine.
Kubernetes [issue 30215](https://github.com/kubernetes/kubernetes/issues/30215)
details more information on this.

## {{% heading "whatsnext" %}}

- See [Autoscaling the DNS Service in a Cluster](/docs/tasks/administer-cluster/dns-horizontal-autoscaling/).
- Read [DNS for Services and Pods](/docs/concepts/services-networking/dns-pod-service/)

