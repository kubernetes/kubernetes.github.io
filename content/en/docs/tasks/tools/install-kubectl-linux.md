---
reviewers:
- mikedanese
title: Install and Set Up kubectl on Linux
content_type: task
weight: 10
card:
  name: tasks
  weight: 20
  title: Install kubectl on Linux
---

## {{% heading "prerequisites" %}}

You must use a kubectl version that is within one minor version difference of your cluster. For example, a v{{< skew latestVersion >}} client can communicate with v{{< skew prevMinorVersion >}}, v{{< skew latestVersion >}}, and v{{< skew nextMinorVersion >}} control planes.
Using the latest version of kubectl helps avoid unforeseen issues.

## Install kubectl on Linux

The following methods exist for installing kubectl on Linux:

- [Install kubectl binary with curl on Linux](#install-kubectl-binary-with-curl-on-linux)
- [Install using native package management](#install-using-native-package-management)
- [Install using other package management](#install-using-other-package-management)

### Install kubectl binary with curl on Linux

1. Download the latest release with the command:

   ```bash
   curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
   ```

   {{< note >}}
To download a specific version, replace the `$(curl -L -s https://dl.k8s.io/release/stable.txt)` portion of the command with the specific version.

For example, to download version {{< param "fullversion" >}} on Linux, type:

   ```bash
   curl -LO https://dl.k8s.io/release/{{< param "fullversion" >}}/bin/linux/amd64/kubectl
   ```
   {{< /note >}}

1. Validate the binary (optional)

   Download the kubectl checksum file:

   ```bash
   curl -LO "https://dl.k8s.io/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl.sha256"
   ```

   Validate the kubectl binary against the checksum file:

   ```bash
   echo "$(<kubectl.sha256) kubectl" | sha256sum --check
   ```

   If valid, the output is:

   ```console
   kubectl: OK
   ```

   If the check fails, `sha256` exits with nonzero status and prints output similar to:

   ```bash
   kubectl: FAILED
   sha256sum: WARNING: 1 computed checksum did NOT match
   ```

   {{< note >}}
   Download the same version of the binary and checksum.
   {{< /note >}}

1. Install kubectl

   ```bash
   sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
   ```

   {{< note >}}
   If you do not have root access on the target system, you can still install kubectl to the `~/.local/bin` directory:

   ```bash
   mkdir -p ~/.local/bin/kubectl
   mv ./kubectl ~/.local/bin/kubectl
   # and then add ~/.local/bin/kubectl to $PATH
   ```

   {{< /note >}}

1. Test to ensure the version you installed is up-to-date:

   ```bash
   kubectl version --client
   ```

### Install using native package management

{{< tabs name="kubectl_install" >}}
{{% tab name="Debian-based distributions" %}}

1. Update the `apt` package index and install packages needed to use the Kubernetes `apt` repository:

   ```shell
   sudo apt-get update
   sudo apt-get install -y apt-transport-https ca-certificates curl
   ```

2. Download the Google Cloud public signing key:

   ```shell
   sudo curl -fsSLo /usr/share/keyrings/kubernetes-archive-keyring.gpg https://packages.cloud.google.com/apt/doc/apt-key.gpg
   ```

3. Add the Kubernetes `apt` repository:

   ```shell
   echo "deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list
   ```

4. Update `apt` package index with the new repository and install kubectl:

   ```shell
   sudo apt-get update
   sudo apt-get install -y kubectl
   ```

{{% /tab %}}

{{< tab name="Red Hat-based distributions" codelang="bash" >}}
cat <<EOF > /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
EOF
yum install -y kubectl
{{< /tab >}}
{{< /tabs >}}

### Install using other package management

{{< tabs name="other_kubectl_install" >}}
{{% tab name="Snap" %}}
If you are on Ubuntu or another Linux distribution that support [snap](https://snapcraft.io/docs/core/install) package manager, kubectl is available as a [snap](https://snapcraft.io/) application.

```shell
snap install kubectl --classic
kubectl version --client
```

{{% /tab %}}

{{% tab name="Homebrew" %}}
If you are on Linux and using [Homebrew](https://docs.brew.sh/Homebrew-on-Linux) package manager, kubectl is available for [installation](https://docs.brew.sh/Homebrew-on-Linux#install).

```shell
brew install kubectl
kubectl version --client
```

{{% /tab %}}

{{< /tabs >}}

## Verify kubectl configuration

{{< include "included/verify-kubectl.md" >}}

## Optional kubectl configurations

### Enable shell autocompletion

kubectl provides autocompletion support for Bash and Zsh, which can save you a lot of typing.

Below are the procedures to set up autocompletion for Bash and Zsh.

{{< tabs name="kubectl_autocompletion" >}}
{{< tab name="Bash" include="included/optional-kubectl-configs-bash-linux.md" />}}
{{< tab name="Zsh" include="included/optional-kubectl-configs-zsh.md" />}}
{{< /tabs >}}

## {{% heading "whatsnext" %}}

{{< include "included/kubectl-whats-next.md" >}}
