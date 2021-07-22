---
title: 在容器内使用本地 IDE 开发和调试服务
content_type: task
---

Kubernetes 的应用程序一般是由很多微服务组成，由于环境不一致和资源限制，这些微服务有时候很难在本地以源码的方式运行。如果在本地使用 Minikube 作为开发环境，编写完代码后又不得不重新构建镜像，并且修改工作负载的镜像版本等待生效，这导致了大量的时间浪费和开发效率低下的问题。

Nocalhost 是一个简化在 Kubernetes 环境下开发微服务的工具，他提供的核心功能是：利用 IDE 插件（包括 VSCode 和 Jetbrains 插件），以图形化的形式直接在容器内进行开发，并实现了本地代码和远端容器实时同步，本地修改代码远端容器实时生效，摆脱了在一些场景下验证代码需要依赖于 CI/CD 以及重新构建镜像的烦恼。

本文档介绍如何在 Kubernetes 环境下使用 `Nocalhost` 直接在容器内开发微服务。

## {{% heading "prerequisites" %}}

* Kubernetes 集群安装完毕
* 安装 [Nocalhost](https://nocalhost.dev/installation/) 插件（支持 VSCode 和 Jetbrains）

## 为 Nocalhost 添加 Kubeconfig

以 VSCode 插件为例，打开 Nocalhost 插件后，你可以选择 `~/.kube/config` 下的 context 或者 "黏贴 kubeconfig"。

添加完成后，便能够在插件中查看该集群下的工作负载，例如该集群已经提前部署了 Istio 示例 [bookinfo](https://raw.githubusercontent.com/istio/istio/release-1.10/samples/bookinfo/platform/kube/bookinfo.yaml)。

![Nocalhost VSCode Plugin](/images/docs/nocalhost-vscode-plugin.png)

## 开发和调试集群的工作负载

在 Nocalhost 插件内，可以很方便实现端口转发、查看日志、进入终端的功能。

例如转发 `productpage-v1` 的 `9080` 端口到本地的 `9080` 端口，只需要右键点击该服务，选择 "Port Forward"，输入 `9080:9080` 即可。

此时，打开浏览器 `127.0.0.1:9080`，应该能看到以下界面。

![Nocalhost Bookinfo Productpage](/images/docs/nocalhost-bookinfo-productpage.png)

现在，假设要修改界面上 “The Comedy of Errors” 这行文字（已知该文字是由 `productpage-v1` 服务输出），一般来说我们有两种方案：

* 第一种：本地修改源码，运行 `docker build` 构建镜像，更新工作负载镜像版本并等待生效。
* 第二种：使用诸如 `Telepresence` 的工具，本地以源码的方式运行 `productpage-v1` 服务，并劫持本机的域名解析到远端集群，使其能够访问远端 `details`, `ratings`, `reviews` 服务。

对于一些复杂的微服务来说，因为资源和环境差异，本地很难以源码的方式运行要开发的服务，那么事情就会回到第一种方案上，这是很难接受的。

现在，有了 Nocalhost，您可以选择全新的开发方式：直接在容器内进行开发。

例如，要开发 `productpage-v1` 服务，首先克隆该项目源码（可能需要几分钟时间）：

```
git clone https://github.com/istio/istio.git
```

返回 Nocalhost 插件，点击 `productpage-v1` 服务右侧的绿色“锤子”图标，只需要两个步骤即可进入 `productpage-v1` 的开发模式：

* 选择 `Open local directory`，并选择 `istio/samples/bookinfo/src/productpage/` 目录。 
* 在新窗口中选择 "Custom"，并输入 `python:3.7.7-slim`

进入开发模式后，VSCode 插件将会得到**远端容器**的 `Terminal`。

![Nocalhost Remote Dev Container](/images/docs/nocalhost-remote-dev-container.png)

在 `Terminal` 中执行 `ls` 命令：

```
/home/nocalhost-dev # ls
Dockerfile             productpage.py         requirements.txt       static                 templates              test-requirements.txt  tests
```

可以发现 `productpage-v1` 的源码已经同步到远端容器。现在，运行：

```
pip install -r requirements.txt && python productpage.py 9080
```

稍等片刻，`productpage` 服务将会启动。

接下来，使用 `VSCode` 编辑 `workspace` 下的 `productpage.py` 文件的 `355` 行，将 `The Comedy of Errors` 修改为 `The Comedy of Errors Code Change Here`，注意保存修改。

![Nocalhost Bookinfo Productpage Code Change](/images/docs/nocalhost-bookinfo-productpage-code-change.png)

重新打开浏览器 `127.0.0.1:9080`，此时应该能看到以下界面：

![Nocalhost Bookinfo Productpage New Web](/images/docs/nocalhost-bookinfo-productpage-new-web.png)

现在，本地的任何代码修改，都将实时同步到远端，由于 `productpage-v1` 服务具备热加载的能力，所以他将自动重启服务。

至此，我们完成了使用 Nocalhost 对 `productpage-v1` 服务进行开发的演示。

在这个过程中，开发人员无需学习额外的工具命令，在最接近开发者的 IDE 内，以图形化的方式直接对服务进行开发，提高了在 Kubernetes 环境下的开发体验和效率。

## {{% heading "whatsnext" %}}

如果你对该教程感兴趣，请查看 [quick start](https://nocalhost.dev/getting-started/)。

要了解更多信息，请访问 [Nocalhost 网站](https://nocalhost.dev)。