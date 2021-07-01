---
reviewers:
- mikedanese
title: Install and Set Up kubectl on Windows
content_type: task
weight: 10
card:
  name: tasks
  weight: 20
  title: Install kubectl on Windows
---

## {{% heading "prerequisites" %}}

You must use a kubectl version that is within one minor version difference of your cluster. For example, a v{{< skew latestVersion >}} client can communicate with v{{< skew prevMinorVersion >}}, v{{< skew latestVersion >}}, and v{{< skew nextMinorVersion >}} control planes.
Using the latest version of kubectl helps avoid unforeseen issues.

## Install kubectl on Windows

The following methods exist for installing kubectl on Windows:

- [Install kubectl binary with curl on Windows](#install-kubectl-binary-with-curl-on-windows)
- [Install on Windows using Chocolatey or Scoop](#install-on-windows-using-chocolatey-or-scoop)


### Install kubectl binary with curl on Windows

1. Download the [latest release {{< param "fullversion" >}}](https://dl.k8s.io/release/{{< param "fullversion" >}}/bin/windows/amd64/kubectl.exe).

   Or if you have `curl` installed, use this command:

   ```powershell
   curl -LO https://dl.k8s.io/release/{{< param "fullversion" >}}/bin/windows/amd64/kubectl.exe
   ```

   {{< note >}}
   To find out the latest stable version (for example, for scripting), take a look at [https://dl.k8s.io/release/stable.txt](https://dl.k8s.io/release/stable.txt).
   {{< /note >}}

1. Validate the binary (optional)

   Download the kubectl checksum file:

   ```powershell
   curl -LO https://dl.k8s.io/{{< param "fullversion" >}}/bin/windows/amd64/kubectl.exe.sha256
   ```

   Validate the kubectl binary against the checksum file:

   - Using Command Prompt to manually compare `CertUtil`'s output to the checksum file downloaded:

     ```cmd
     CertUtil -hashfile kubectl.exe SHA256
     type kubectl.exe.sha256
     ```

   - Using PowerShell to automate the verification using the `-eq` operator to get a `True` or `False` result:

     ```powershell
     $($(CertUtil -hashfile .\kubectl.exe SHA256)[1] -replace " ", "") -eq $(type .\kubectl.exe.sha256)
     ```

1. Add the binary in to your `PATH`.

1. Test to ensure the version of `kubectl` is the same as downloaded:

   ```cmd
   kubectl version --client
   ```

{{< note >}}
[Docker Desktop for Windows](https://docs.docker.com/docker-for-windows/#kubernetes) adds its own version of `kubectl` to `PATH`.
If you have installed Docker Desktop before, you may need to place your `PATH` entry before the one added by the Docker Desktop installer or remove the Docker Desktop's `kubectl`.
{{< /note >}}

### Install on Windows using Chocolatey or Scoop

1. To install kubectl on Windows you can use either [Chocolatey](https://chocolatey.org) package manager or [Scoop](https://scoop.sh) command-line installer.

   {{< tabs name="kubectl_win_install" >}}
   {{% tab name="choco" %}}
   ```powershell
   choco install kubernetes-cli
   ```
   {{% /tab %}}
   {{% tab name="scoop" %}}
   ```powershell
   scoop install kubectl
   ```
   {{% /tab %}}
   {{< /tabs >}}


1. Test to ensure the version you installed is up-to-date:

   ```powershell
   kubectl version --client
   ```

1. Navigate to your home directory:

   ```powershell
   # If you're using cmd.exe, run: cd %USERPROFILE%
   cd ~
   ```

1. Create the `.kube` directory:

   ```powershell
   mkdir .kube
   ```

1. Change to the `.kube` directory you just created:

   ```powershell
   cd .kube
   ```

1. Configure kubectl to use a remote Kubernetes cluster:

   ```powershell
   New-Item config -type file
   ```

{{< note >}}
Edit the config file with a text editor of your choice, such as Notepad.
{{< /note >}}

## Verify kubectl configuration

{{< include "included/verify-kubectl.md" >}}

## Optional kubectl configurations

### Enable shell autocompletion

kubectl provides autocompletion support for Bash and Zsh, which can save you a lot of typing.

Below are the procedures to set up autocompletion for Zsh, if you are running that on Windows.

{{< include "included/optional-kubectl-configs-zsh.md" >}}

## {{% heading "whatsnext" %}}

{{< include "included/kubectl-whats-next.md" >}}
