---
reviewers:
- mikedanese
title: Install and Set Up kubectl on macOS
content_type: task
weight: 10
card:
  name: tasks
  weight: 20
  title: Install kubectl on macOS
---

## {{% heading "prerequisites" %}}

You must use a kubectl version that is within one minor version difference of your cluster. For example, a v{{< skew latestVersion >}} client can communicate with v{{< skew prevMinorVersion >}}, v{{< skew latestVersion >}}, and v{{< skew nextMinorVersion >}} control planes.
Using the latest version of kubectl helps avoid unforeseen issues.

## Install kubectl on macOS

The following methods exist for installing kubectl on macOS:

- [Install kubectl binary with curl on macOS](#install-kubectl-binary-with-curl-on-macos)
- [Install with Homebrew on macOS](#install-with-homebrew-on-macos)
- [Install with Macports on macOS](#install-with-macports-on-macos)

### Install kubectl binary with curl on macOS

1. Download the latest release:

   {{< tabs name="download_binary_macos" >}}
   {{< tab name="Intel" codelang="bash" >}}
   curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/darwin/amd64/kubectl"
   {{< /tab >}}
   {{< tab name="Apple Silicon" codelang="bash" >}}
   curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/darwin/arm64/kubectl"
   {{< /tab >}}
   {{< /tabs >}}

   {{< note >}}
   To download a specific version, replace the `$(curl -L -s https://dl.k8s.io/release/stable.txt)` portion of the command with the specific version.

   For example, to download version {{< param "fullversion" >}} on Intel macOS, type:

   ```bash
   curl -LO "https://dl.k8s.io/release/{{< param "fullversion" >}}/bin/darwin/amd64/kubectl"
   ```

   And for macOS on Apple Silicon, type:

   ```bash
   curl -LO "https://dl.k8s.io/release/{{< param "fullversion" >}}/bin/darwin/arm64/kubectl"
   ```

   {{< /note >}}

1. Validate the binary (optional)

   Download the kubectl checksum file:

   {{< tabs name="download_checksum_macos" >}}
   {{< tab name="Intel" codelang="bash" >}}
   curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/darwin/amd64/kubectl.sha256"
   {{< /tab >}}
   {{< tab name="Apple Silicon" codelang="bash" >}}
   curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/darwin/arm64/kubectl.sha256"
   {{< /tab >}}
   {{< /tabs >}}
  
   Validate the kubectl binary against the checksum file:

   ```bash
   echo "$(<kubectl.sha256)  kubectl" | shasum -a 256 --check
   ```

   If valid, the output is:

   ```console
   kubectl: OK
   ```

   If the check fails, `shasum` exits with nonzero status and prints output similar to:

   ```bash
   kubectl: FAILED
   shasum: WARNING: 1 computed checksum did NOT match
   ```

   {{< note >}}
   Download the same version of the binary and checksum.
   {{< /note >}}

1. Make the kubectl binary executable.

   ```bash
   chmod +x ./kubectl
   ```

1. Move the kubectl binary to a file location on your system `PATH`.

   ```bash
   sudo mv ./kubectl /usr/local/bin/kubectl
   sudo chown root: /usr/local/bin/kubectl
   ```

   {{< note >}}
   Make sure `/usr/local/bin` is in your PATH environment variable.
   {{< /note >}}

1. Test to ensure the version you installed is up-to-date:

   ```bash
   kubectl version --client
   ```

### Install with Homebrew on macOS

If you are on macOS and using [Homebrew](https://brew.sh/) package manager, you can install kubectl with Homebrew.

1. Run the installation command:

   ```bash
   brew install kubectl 
   ```

   or

   ```bash
   brew install kubernetes-cli
   ```

1. Test to ensure the version you installed is up-to-date:

   ```bash
   kubectl version --client
   ```

### Install with Macports on macOS

If you are on macOS and using [Macports](https://macports.org/) package manager, you can install kubectl with Macports.

1. Run the installation command:

   ```bash
   sudo port selfupdate
   sudo port install kubectl
   ```

1. Test to ensure the version you installed is up-to-date:

   ```bash
   kubectl version --client
   ```

## Verify kubectl configuration

{{< include "included/verify-kubectl.md" >}}

## Optional kubectl configurations

### Enable shell autocompletion

kubectl provides autocompletion support for Bash and Zsh, which can save you a lot of typing.

Below are the procedures to set up autocompletion for Bash and Zsh.

{{< tabs name="kubectl_autocompletion" >}}
{{< tab name="Bash" include="included/optional-kubectl-configs-bash-mac.md" />}}
{{< tab name="Zsh" include="included/optional-kubectl-configs-zsh.md" />}}
{{< /tabs >}}

## {{% heading "whatsnext" %}}

{{< include "included/kubectl-whats-next.md" >}}
