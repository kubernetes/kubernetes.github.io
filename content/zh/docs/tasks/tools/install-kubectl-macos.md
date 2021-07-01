---
title: 在 macOS 系统上安装和设置 kubectl
content_type: task
weight: 10
card:
  name: tasks
  weight: 20
  title: 在 macOS 系统上安装 kubectl 
---
<!-- 
reviewers:
- mikedanese
title: Install and Set Up kubectl on macOS
content_type: task
weight: 10
card:
  name: tasks
  weight: 20
  title: Install kubectl on macOS
-->

## {{% heading "prerequisites" %}}

<!-- 
You must use a kubectl version that is within one minor version difference of your cluster. For example, a v{{< skew latestVersion >}} client can communicate with v{{< skew prevMinorVersion >}}, v{{< skew latestVersion >}}, and v{{< skew nextMinorVersion >}} control planes.
Using the latest version of kubectl helps avoid unforeseen issues.
-->
kubectl 版本和集群之间的差异必须在一个小版本号之内。
例如：v{{< skew latestVersion >}} 版本的客户端能与 v{{< skew prevMinorVersion >}}、
v{{< skew latestVersion >}} 和 v{{< skew nextMinorVersion >}} 版本的控制面通信。
用最新版本的 kubectl 有助于避免不可预见的问题。

<!-- 
## Install kubectl on macOS
-->
## 在 macOS 系统上安装 kubectl {#install-kubectl-on-macos}

<!-- 
The following methods exist for installing kubectl on macOS:
-->
在 macOS 系统上安装 kubectl 有如下方法：

<!--
- [Install kubectl binary with curl on macOS](#install-kubectl-binary-with-curl-on-macos)
- [Install with Homebrew on macOS](#install-with-homebrew-on-macos)
- [Install with Macports on macOS](#install-with-macports-on-macos)
- [Install on macOS as part of the Google Cloud SDK](#install-on-macos-as-part-of-the-google-cloud-sdk)
-->
- [用 curl 在 macOS 系统上安装 kubectl](#install-kubectl-binary-with-curl-on-macos)
- [用 Homebrew 在 macOS 系统上安装](#install-with-homebrew-on-macos)
- [用 Macports 在 macOS 上安装](#install-with-macports-on-macos)
- [作为谷歌云 SDK 的一部分，在 macOS 上安装](#install-on-macos-as-part-of-the-google-cloud-sdk)

<!-- 
### Install kubectl binary with curl on macOS {#install-kubectl-binary-with-curl-on-macos}
-->
### 用 curl 在 macOS 系统上安装 kubectl {#install-kubectl-binary-with-curl-on-macos}

<!-- 
1. Download the latest release:
-->
1. 下载最新的发行版：

   {{< tabs name="download_binary_macos" >}}
   {{< tab name="Intel" codelang="bash" >}}
   curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/darwin/amd64/kubectl"
   {{< /tab >}}
   {{< tab name="Apple Silicon" codelang="bash" >}}
   curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/darwin/arm64/kubectl"
   {{< /tab >}}
   {{< /tabs >}}

   {{< note >}}
   <!-- 
   To download a specific version, replace the `$(curl -L -s https://dl.k8s.io/release/stable.txt)` portion of the command with the specific version.

   For example, to download version {{< param "fullversion" >}} on Intel macOS, type:

   ```bash
   curl -LO "https://dl.k8s.io/release/{{< param "fullversion" >}}/bin/darwin/arm64/kubectl"
   ```

   -->
   如果需要下载某个指定的版本，用该指定版本号替换掉命令的这个部分：`$(curl -L -s https://dl.k8s.io/release/stable.txt)`。
   例如：要为 Intel macOS 系统下载 {{< param "fullversion" >}} 版本，则输入：

   ```bash
   curl -LO "https://dl.k8s.io/release/{{< param "fullversion" >}}/bin/darwin/amd64/kubectl"
   ```

   <!--
   And for macOS on Apple Silicon, type:
   -->
   对于 Apple Silicon 版本的 macOS，输入：

   ```bash
   curl -LO "https://dl.k8s.io/release/{{< param "fullversion" >}}/bin/darwin/arm64/kubectl"
   ```
   {{< /note >}}

<!-- 
1. Validate the binary (optional)

   Download the kubectl checksum file:
-->
2. 验证可执行文件（可选操作）

   下载 kubectl 的校验和文件：

   {{< tabs name="download_checksum_macos" >}}
   {{< tab name="Intel" codelang="bash" >}}
   curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/darwin/amd64/kubectl.sha256"
   {{< /tab >}}
   {{< tab name="Apple Silicon" codelang="bash" >}}
   curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/darwin/arm64/kubectl.sha256"
   {{< /tab >}}
   {{< /tabs >}}

   <!-- 
   Validate the kubectl binary against the checksum file:
   -->
   根据校验和文件，验证 kubectl：

   ```bash
   echo "$(<kubectl.sha256)  kubectl" | shasum -a 256 --check
   ```
   <!-- 
   If valid, the output is:
   -->
   验证通过时，输出如下：

   ```console
   kubectl: OK
   ```

   <!-- 
   If the check fails, `shasum` exits with nonzero status and prints output similar to:
   -->
   验证失败时，`shasum` 将以非零值退出，并打印如下输出：

   ```
   kubectl: FAILED
   shasum: WARNING: 1 computed checksum did NOT match
   ```

   {{< note >}}
   <!-- 
   Download the same version of the binary and checksum.
   -->
   下载的 kubectl 与校验和文件版本要相同。
   {{< /note >}}

<!-- 
1. Make the kubectl binary executable.
-->
3. 将 kubectl 置为可执行文件：

   ```bash
   chmod +x ./kubectl
   ```

<!-- 
1. Move the kubectl binary to a file location on your system `PATH`.
-->
4. 将可执行文件 kubectl 移动到系统可寻址路径 `PATH` 内的一个位置：

   ```bash
   sudo mv ./kubectl /usr/local/bin/kubectl
   sudo chown root: /usr/local/bin/kubectl
   ```

   {{< note >}}
   <!--
   Make sure `/usr/local/bin` is in your PATH environment variable.
   -->
   确保 `/usr/local/bin` 在你的 PATH 环境变量中。
   {{< /note >}}

<!-- 
1. Test to ensure the version you installed is up-to-date:
-->
5. 测试一下，确保你安装的是最新的版本：

   ```bash
   kubectl version --client
   ```

<!-- 
### Install with Homebrew on macOS {#install-with-homebrew-on-macos}
-->
### 用 Homebrew 在 macOS 系统上安装 {#install-with-homebrew-on-macos}

<!-- 
If you are on macOS and using [Homebrew](https://brew.sh/) package manager, you can install kubectl with Homebrew.
-->
如果你是 macOS 系统，且用的是 [Homebrew](https://brew.sh/) 包管理工具，
则可以用 Homebrew 安装 kubectl。

<!-- 
1. Run the installation command:
-->
1. 运行安装命令：

   ```bash
   brew install kubectl 
   ```

   或

   ```bash
   brew install kubernetes-cli
   ```

<!-- 
1. Test to ensure the version you installed is up-to-date:
-->
2. 测试一下，确保你安装的是最新的版本：

   ```bash
   kubectl version --client
   ```

<!-- 
### Install with Macports on macOS {#install-with-macports-on-macos}
-->
### 用 Macports 在 macOS 上安装 {#install-with-macports-on-macos}

<!-- 
If you are on macOS and using [Macports](https://macports.org/) package manager, you can install kubectl with Macports.
-->
如果你用的是 macOS，且用 [Macports](https://macports.org/) 包管理工具，则你可以用 Macports 安装kubectl。

<!-- 
1. Run the installation command:
-->
1. 运行安装命令：

   ```bash
   sudo port selfupdate
   sudo port install kubectl
   ```

<!-- 
1. Test to ensure the version you installed is up-to-date:
-->
2. 测试一下，确保你安装的是最新的版本：

   ```bash
   kubectl version --client
   ```

<!-- 
### Install on macOS as part of the Google Cloud SDK {#install-on-macos-as-part-of-the-google-cloud-sdk}
-->
### 作为谷歌云 SDK 的一部分，在 macOS 上安装 {#install-on-macos-as-part-of-the-google-cloud-sdk}

{{< include "included/install-kubectl-gcloud.md" >}}

<!-- 
## Verify kubectl configuration {#verify-kubectl-configuration}
-->
## 验证 kubectl 配置 {#verify-kubectl-configuration}

{{< include "included/verify-kubectl.md" >}}

<!-- 
## Optional kubectl configurations {#optional-kubectl-configurations}

### Enable shell autocompletion {#enable-shell-autocompletion}
-->
## 可选的 kubectl 配置 {#optional-kubectl-configurations}

### 启用 shell 自动补全功能 {#enable-shell-autocompletion}

<!-- 
kubectl provides autocompletion support for Bash and Zsh, which can save you a lot of typing.

Below are the procedures to set up autocompletion for Bash and Zsh.
-->
kubectl 为 Bash 和 Zsh 提供自动补全功能，这可以节省许多输入的麻烦。

下面是为 Bash 和 Zsh 设置自动补全功能的操作步骤。

{{< tabs name="kubectl_autocompletion" >}}
{{< tab name="Bash" include="included/optional-kubectl-configs-bash-mac.md" />}}
{{< tab name="Zsh" include="included/optional-kubectl-configs-zsh.md" />}}
{{< /tabs >}}

## {{% heading "whatsnext" %}}

{{< include "included/kubectl-whats-next.md" >}}

