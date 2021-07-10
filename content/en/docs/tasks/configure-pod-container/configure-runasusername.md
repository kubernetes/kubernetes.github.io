---
title: Configure RunAsUserName for Windows pods and containers
content_type: task
weight: 20
---

<!-- overview -->

{{< feature-state for_k8s_version="v1.18" state="stable" >}}

This page shows how to use the `runAsUserName` setting for Pods and containers that will run on Windows nodes. This is roughly equivalent of the Linux-specific `runAsUser` setting, allowing you to run applications in a container as a different username than the default.



## {{% heading "prerequisites" %}}


You need to have a Kubernetes cluster and the kubectl command-line tool must be configured to communicate with your cluster. The cluster is expected to have Windows worker nodes where pods with containers running Windows workloads will get scheduled.



<!-- steps -->

## Set the Username for a Pod

To specify the username with which to execute the Pod's container processes, include the `securityContext` field ({{< api-reference page="workload-resources/pod-v1" anchor="PodSecurityContext" >}}) in the Pod specification, and within it, the `windowsOptions` ({{< api-reference page="workload-resources/pod-v1" anchor="WindowsSecurityContextOptions" >}}) field containing the `runAsUserName` field.

The Windows security context options that you specify for a Pod apply to all Containers and init Containers in the Pod.

Here is a configuration file for a Windows Pod that has the `runAsUserName` field set:

{{< codenew file="windows/run-as-username-pod.yaml" >}}

Create the Pod:

```shell
kubectl apply -f https://k8s.io/examples/windows/run-as-username-pod.yaml
```

Verify that the Pod's Container is running:

```shell
kubectl get pod run-as-username-pod-demo
```

Get a shell to the running Container:

```shell
kubectl exec -it run-as-username-pod-demo -- powershell
```

Check that the shell is running user the correct username:

```powershell
echo $env:USERNAME
```

The output should be:

```shell
ContainerUser
```

## Set the Username for a Container

To specify the username with which to execute a Container's processes, include the `securityContext` field ({{< api-reference page="workload-resources/pod-v1" anchor="SecurityContext" >}}) in the Container manifest, and within it, the `windowsOptions` ({{< api-reference page="workload-resources/pod-v1" anchor="WindowsSecurityContextOptions" >}}) field containing the `runAsUserName` field.

The Windows security context options that you specify for a Container apply only to that individual Container, and they override the settings made at the Pod level.

Here is the configuration file for a Pod that has one Container, and the `runAsUserName` field is set at the Pod level and the Container level:

{{< codenew file="windows/run-as-username-container.yaml" >}}

Create the Pod:

```shell
kubectl apply -f https://k8s.io/examples/windows/run-as-username-container.yaml
```

Verify that the Pod's Container is running:

```shell
kubectl get pod run-as-username-container-demo
```

Get a shell to the running Container:

```shell
kubectl exec -it run-as-username-container-demo -- powershell
```

Check that the shell is running user the correct username (the one set at the Container level):

```powershell
echo $env:USERNAME
```

The output should be:

```shell
ContainerAdministrator
```

## Windows Username limitations

In order to use this feature, the value set in the `runAsUserName` field must be a valid username. It must have the following format: `DOMAIN\USER`, where `DOMAIN\` is optional. Windows user names are case insensitive. Additionally, there are some restrictions regarding the `DOMAIN` and `USER`:

- The `runAsUserName` field cannot be empty, and it cannot contain control characters (ASCII values: `0x00-0x1F`, `0x7F`)
- The `DOMAIN` must be either a NetBios name, or a DNS name, each with their own restrictions:
  - NetBios names: maximum 15 characters, cannot start with `.` (dot), and cannot contain the following characters: `\ / : * ? " < > |`
  - DNS names: maximum 255 characters, contains only alphanumeric characters, dots, and dashes, and it cannot start or end with a `.` (dot) or `-` (dash).
- The `USER` must have at most 20 characters, it cannot contain *only* dots or spaces, and it cannot contain the following characters: `" / \ [ ] : ; | = , + * ? < > @`.

Examples of acceptable values for the `runAsUserName` field: `ContainerAdministrator`, `ContainerUser`, `NT AUTHORITY\NETWORK SERVICE`, `NT AUTHORITY\LOCAL SERVICE`.

For more information about these limtations, check [here](https://support.microsoft.com/en-us/help/909264/naming-conventions-in-active-directory-for-computers-domains-sites-and) and [here](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.localaccounts/new-localuser?view=powershell-5.1).



## {{% heading "whatsnext" %}}


* [Guide for scheduling Windows containers in Kubernetes](/docs/setup/production-environment/windows/user-guide-windows-containers/)
* [Managing Workload Identity with Group Managed Service Accounts (GMSA)](/docs/setup/production-environment/windows/user-guide-windows-containers/#managing-workload-identity-with-group-managed-service-accounts)
* [Configure GMSA for Windows pods and containers](/docs/tasks/configure-pod-container/configure-gmsa/)

