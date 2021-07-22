---
reviewers:
- jayunit100
- jsturtevant
- marosset
- perithompson
title: Guide for scheduling Windows containers in Kubernetes
content_type: concept
weight: 75
---

<!-- overview -->

Windows applications constitute a large portion of the services and applications that run in many organizations. 
This guide walks you through the steps to configure and deploy a Windows container in Kubernetes.



<!-- body -->

## Objectives

* Configure an example deployment to run Windows containers on the Windows node
* (Optional) Configure an Active Directory Identity for your Pod using Group Managed Service Accounts (GMSA)

## Before you begin

* Create a Kubernetes cluster that includes a 
control plane and a [worker node running Windows Server](/docs/tasks/administer-cluster/kubeadm/adding-windows-nodes/)
* It is important to note that creating and deploying services and workloads on Kubernetes 
behaves in much the same way for Linux and Windows containers. 
[Kubectl commands](/docs/reference/kubectl/overview/) to interface with the cluster are identical. 
The example in the section below is provided to jumpstart your experience with Windows containers.

## Getting Started: Deploying a Windows container

To deploy a Windows container on Kubernetes, you must first create an example application. 
The example YAML file below creates a simple webserver application. 
Create a service spec named `win-webserver.yaml` with the contents below:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: win-webserver
  labels:
    app: win-webserver
spec:
  ports:
    # the port that this service should serve on
    - port: 80
      targetPort: 80
  selector:
    app: win-webserver
  type: NodePort
---
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: win-webserver
  name: win-webserver
spec:
  replicas: 2
  selector:
    matchLabels:
      app: win-webserver
  template:
    metadata:
      labels:
        app: win-webserver
      name: win-webserver
    spec:
     containers:
      - name: windowswebserver
        image: mcr.microsoft.com/windows/servercore:ltsc2019
        command:
        - powershell.exe
        - -command
        - "<#code used from https://gist.github.com/19WAS85/5424431#> ; $$listener = New-Object System.Net.HttpListener ; $$listener.Prefixes.Add('http://*:80/') ; $$listener.Start() ; $$callerCounts = @{} ; Write-Host('Listening at http://*:80/') ; while ($$listener.IsListening) { ;$$context = $$listener.GetContext() ;$$requestUrl = $$context.Request.Url ;$$clientIP = $$context.Request.RemoteEndPoint.Address ;$$response = $$context.Response ;Write-Host '' ;Write-Host('> {0}' -f $$requestUrl) ;  ;$$count = 1 ;$$k=$$callerCounts.Get_Item($$clientIP) ;if ($$k -ne $$null) { $$count += $$k } ;$$callerCounts.Set_Item($$clientIP, $$count) ;$$ip=(Get-NetAdapter | Get-NetIpAddress); $$header='<html><body><H1>Windows Container Web Server</H1>' ;$$callerCountsString='' ;$$callerCounts.Keys | % { $$callerCountsString+='<p>IP {0} callerCount {1} ' -f $$ip[1].IPAddress,$$callerCounts.Item($$_) } ;$$footer='</body></html>' ;$$content='{0}{1}{2}' -f $$header,$$callerCountsString,$$footer ;Write-Output $$content ;$$buffer = [System.Text.Encoding]::UTF8.GetBytes($$content) ;$$response.ContentLength64 = $$buffer.Length ;$$response.OutputStream.Write($$buffer, 0, $$buffer.Length) ;$$response.Close() ;$$responseStatus = $$response.StatusCode ;Write-Host('< {0}' -f $$responseStatus)  } ; "
     nodeSelector:
      kubernetes.io/os: windows
```

{{< note >}}
Port mapping is also supported, but for simplicity in this example 
the container port 80 is exposed directly to the service.
{{< /note >}}

1. Check that all nodes are healthy:

    ```bash
    kubectl get nodes
    ```

1. Deploy the service and watch for pod updates:

    ```bash
    kubectl apply -f win-webserver.yaml
    kubectl get pods -o wide -w
    ```

    When the service is deployed correctly both Pods are marked as Ready. To exit the watch command, press Ctrl+C.

1. Check that the deployment succeeded. To verify:

    * Two containers per pod on the Windows node, use `docker ps` 
    * Two pods listed from the Linux control plane node, use `kubectl get pods` 
    * Node-to-pod communication across the network, `curl` port 80 of your pod IPs from the Linux control plane node 
      to check for a web server response
    * Pod-to-pod communication, ping between pods (and across hosts, if you have more than one Windows node) 
      using docker exec or kubectl exec
    * Service-to-pod communication, `curl` the virtual service IP (seen under `kubectl get services`) 
      from the Linux control plane node and from individual pods
    * Service discovery, `curl` the service name with the Kubernetes [default DNS suffix](/docs/concepts/services-networking/dns-pod-service/#services)
    * Inbound connectivity, `curl` the NodePort from the Linux control plane node or machines outside of the cluster
    * Outbound connectivity, `curl` external IPs from inside the pod using kubectl exec

{{< note >}}
Windows container hosts are not able to access the IP of services scheduled on them due to current platform limitations of the Windows networking stack. 
Only Windows pods are able to access service IPs.
{{< /note >}}

## Observability

### Capturing logs from workloads

Logs are an important element of observability; they enable users to gain insights 
into the operational aspect of workloads and are a key ingredient to troubleshooting issues. 
Because Windows containers and workloads inside Windows containers behave differently from Linux containers, 
users had a hard time collecting logs, limiting operational visibility. 
Windows workloads for example are usually configured to log to ETW (Event Tracing for Windows) 
or push entries to the application event log. 
[LogMonitor](https://github.com/microsoft/windows-container-tools/tree/master/LogMonitor), an open source tool by Microsoft, 
is the recommended way to monitor configured log sources inside a Windows container. 
LogMonitor supports monitoring event logs, ETW providers, and custom application logs, 
piping them to STDOUT for consumption by `kubectl logs <pod>`.

Follow the instructions in the LogMonitor GitHub page to copy its binaries and configuration files 
to all your containers and add the necessary entrypoints for LogMonitor to push your logs to STDOUT.

## Using configurable Container usernames

Starting with Kubernetes v1.16, Windows containers can be configured to run their entrypoints and processes 
with different usernames than the image defaults. 
The way this is achieved is a bit different from the way it is done for Linux containers. 
Learn more about it [here](/docs/tasks/configure-pod-container/configure-runasusername/).

## Managing Workload Identity with Group Managed Service Accounts

Starting with Kubernetes v1.14, Windows container workloads can be configured to use Group Managed Service Accounts (GMSA). 
Group Managed Service Accounts are a specific type of Active Directory account that provides automatic password management, 
simplified service principal name (SPN) management, and the ability to delegate the management to other administrators across multiple servers. 
Containers configured with a GMSA can access external Active Directory Domain resources while carrying the identity configured with the GMSA. 
Learn more about configuring and using GMSA for Windows containers [here](/docs/tasks/configure-pod-container/configure-gmsa/).

## Taints and Tolerations

Users today need to use some combination of taints and node selectors in order to 
keep Linux and Windows workloads on their respective OS-specific nodes. 
This likely imposes a burden only on Windows users. The recommended approach is outlined below, 
with one of its main goals being that this approach should not break compatibility for existing Linux workloads.

### Ensuring OS-specific workloads land on the appropriate container host

Users can ensure Windows containers can be scheduled on the appropriate host using Taints and Tolerations. 
All Kubernetes nodes today have the following default labels:

* kubernetes.io/os = [windows|linux]
* kubernetes.io/arch = [amd64|arm64|...]

If a Pod specification does not specify a nodeSelector like `"kubernetes.io/os": windows`, 
it is possible the Pod can be scheduled on any host, Windows or Linux. 
This can be problematic since a Windows container can only run on Windows and a Linux container can only run on Linux. 
The best practice is to use a nodeSelector.

However, we understand that in many cases users have a pre-existing large number of deployments for Linux containers, 
as well as an ecosystem of off-the-shelf configurations, such as community Helm charts, and programmatic Pod generation cases, such as with Operators. 
In those situations, you may be hesitant to make the configuration change to add nodeSelectors. 
The alternative is to use Taints. Because the kubelet can set Taints during registration, 
it could easily be modified to automatically add a taint when running on Windows only.

For example:  `--register-with-taints='os=windows:NoSchedule'`

By adding a taint to all Windows nodes, nothing will be scheduled on them (that includes existing Linux Pods). 
In order for a Windows Pod to be scheduled on a Windows node, 
it would need both the nodeSelector and the appropriate matching toleration to choose Windows.

```yaml
nodeSelector:
    kubernetes.io/os: windows
    node.kubernetes.io/windows-build: '10.0.17763'
tolerations:
    - key: "os"
      operator: "Equal"
      value: "windows"
      effect: "NoSchedule"
```

### Handling multiple Windows versions in the same cluster

The Windows Server version used by each pod must match that of the node. If you want to use multiple Windows
Server versions in the same cluster, then you should set additional node labels and nodeSelectors.

Kubernetes 1.17 automatically adds a new label `node.kubernetes.io/windows-build` to simplify this. 
If you're running an older version, then it's recommended to add this label manually to Windows nodes.

This label reflects the Windows major, minor, and build number that need to match for compatibility. 
Here are values used today for each Windows Server version.

| Product Name                         |   Build Number(s)      |
|--------------------------------------|------------------------|
| Windows Server 2019                  | 10.0.17763             |
| Windows Server version 1809          | 10.0.17763             |
| Windows Server version 1903          | 10.0.18362             |


### Simplifying with RuntimeClass

[RuntimeClass] can be used to simplify the process of using taints and tolerations. 
A cluster administrator can create a `RuntimeClass` object which is used to encapsulate these taints and tolerations.


1. Save this file to `runtimeClasses.yml`. It includes the appropriate `nodeSelector` 
for the Windows OS, architecture, and version.

```yaml
apiVersion: node.k8s.io/v1
kind: RuntimeClass
metadata:
  name: windows-2019
handler: 'docker'
scheduling:
  nodeSelector:
    kubernetes.io/os: 'windows'
    kubernetes.io/arch: 'amd64'
    node.kubernetes.io/windows-build: '10.0.17763'
  tolerations:
  - effect: NoSchedule
    key: os
    operator: Equal
    value: "windows"
```

1. Run `kubectl create -f runtimeClasses.yml` using as a cluster administrator
1. Add `runtimeClassName: windows-2019` as appropriate to Pod specs

For example:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: iis-2019
  labels:
    app: iis-2019
spec:
  replicas: 1
  template:
    metadata:
      name: iis-2019
      labels:
        app: iis-2019
    spec:
      runtimeClassName: windows-2019
      containers:
      - name: iis
        image: mcr.microsoft.com/windows/servercore/iis:windowsservercore-ltsc2019
        resources:
          limits:
            cpu: 1
            memory: 800Mi
          requests:
            cpu: .1
            memory: 300Mi
        ports:
          - containerPort: 80
 selector:
    matchLabels:
      app: iis-2019
---
apiVersion: v1
kind: Service
metadata:
  name: iis
spec:
  type: LoadBalancer
  ports:
  - protocol: TCP
    port: 80
  selector:
    app: iis-2019
```




[RuntimeClass]: https://kubernetes.io/docs/concepts/containers/runtime-class/
