# Kubernetes 文档

<!--
# The Kubernetes documentation
-->

[![Netlify Status](https://api.netlify.com/api/v1/badges/be93b718-a6df-402a-b4a4-855ba186c97d/deploy-status)](https://app.netlify.com/sites/kubernetes-io-main-staging/deploys) [![GitHub release](https://img.shields.io/github/release/kubernetes/website.svg)](https://github.com/kubernetes/website/releases/latest)

<!--
This repository contains the assets required to build the [Kubernetes website and documentation](https://kubernetes.io/). We're glad that you want to contribute!
-->
本仓库包含了所有用于构建 [Kubernetes 网站和文档](https://kubernetes.io/) 的软件资产。
我们非常高兴您想要参与贡献！

<!--
# Using this repository

You can run the website locally using Hugo (Extended version), or you can run it in a container runtime. We strongly recommend using the container runtime, as it gives deployment consistency with the live website.
-->
## 使用这个仓库

可以使用 Hugo（扩展版）在本地运行网站，也可以在容器中运行它。强烈建议使用容器，因为这样可以和在线网站的部署保持一致。

<!--
## Prerequisites

To use this repository, you need the following installed locally:

- [npm](https://www.npmjs.com/)
- [Go](https://golang.org/)
- [Hugo (Extended version)](https://gohugo.io/)
- A container runtime, like [Docker](https://www.docker.com/).

-->
## 前提条件

使用这个仓库，需要在本地安装以下软件：

- [npm](https://www.npmjs.com/)
- [Go](https://golang.org/)
- [Hugo (Extended version)](https://gohugo.io/)
- 容器运行时，比如 [Docker](https://www.docker.com/).

<!--
Before you start, install the dependencies. Clone the repository and navigate to the directory:
-->
开始前，先安装这些依赖。克隆本仓库并进入对应目录：

```
git clone https://github.com/kubernetes/website.git
cd website
```

<!--
The Kubernetes website uses the [Docsy Hugo theme](https://github.com/google/docsy#readme). Even if you plan to run the website in a container, we strongly recommend pulling in the submodule and other development dependencies by running the following:
-->

Kubernetes 网站使用的是 [Docsy Hugo 主题](https://github.com/google/docsy#readme)。 即使你打算在容器中运行网站，我们也强烈建议你通过运行以下命令来引入子模块和其他开发依赖项：

```
# pull in the Docsy submodule
git submodule update --init --recursive --depth 1
```

<!--
## Running the website using a container

To build the site in a container, run the following to build the container image and run it:

-->
## 在容器中运行网站

要在容器中构建网站，请通过以下命令来构建容器镜像并运行：

```
make container-image
make container-serve
```

<!--
Open up your browser to http://localhost:1313 to view the website. As you make changes to the source files, Hugo updates the website and forces a browser refresh.
-->
启动浏览器，打开 http://localhost:1313 来查看网站。
当你对源文件作出修改时，Hugo 会更新网站并强制浏览器执行刷新操作。

<!--
## Running the website locally using Hugo

Make sure to install the Hugo extended version specified by the `HUGO_VERSION` environment variable in the [`netlify.toml`](netlify.toml#L10) file.

To build and test the site locally, run:
-->
## 在本地使用 Hugo 来运行网站

请确保安装的是 [`netlify.toml`](netlify.toml#L10) 文件中环境变量 `HUGO_VERSION` 所指定的
Hugo 扩展版本。

若要在本地构造和测试网站，请运行：

```bash
# install dependencies
npm ci
make serve
```

<!--
This will start the local Hugo server on port 1313. Open up your browser to http://localhost:1313 to view the website. As you make changes to the source files, Hugo updates the website and forces a browser refresh.
-->
上述命令会在端口 1313 上启动本地 Hugo 服务器。
启动浏览器，打开 http://localhost:1313 来查看网站。
当你对源文件作出修改时，Hugo 会更新网站并强制浏览器执行刷新操作。

<!--
## Troubleshooting
### error: failed to transform resource: TOCSS: failed to transform "scss/main.scss" (text/x-scss): this feature is not available in your current Hugo version

Hugo is shipped in two set of binaries for technical reasons. The current website runs based on the **Hugo Extended** version only. In the [release page](https://github.com/gohugoio/hugo/releases) look for archives with `extended` in the name. To confirm, run `hugo version` and look for the word `extended`.

-->
## 故障排除

###  error: failed to transform resource: TOCSS: failed to transform "scss/main.scss" (text/x-scss): this feature is not available in your current Hugo version

由于技术原因，Hugo 会发布两套二进制文件。
当前网站仅基于 **Hugo Extended** 版本运行。
在 [发布页面](https://github.com/gohugoio/hugo/releases) 中查找名称为 `extended` 的归档。可以运行 `huge version` 查看是否有单词 `extended` 来确认。

<!--
### Troubleshooting macOS for too many open files

If you run `make serve` on macOS and receive the following error:

-->
### 对 macOs 上打开太多文件的故障排除

如果在 macOS 上运行 `make serve` 收到以下错误：

```
ERROR 2020/08/01 19:09:18 Error: listen tcp 127.0.0.1:1313: socket: too many open files
make: *** [serve] Error 1
```

试着查看一下当前打开文件数的限制：

`launchctl limit maxfiles`

然后运行以下命令（参考https://gist.github.com/tombigel/d503800a282fcadbee14b537735d202c）：

```
#!/bin/sh

# These are the original gist links, linking to my gists now.
# curl -O https://gist.githubusercontent.com/a2ikm/761c2ab02b7b3935679e55af5d81786a/raw/ab644cb92f216c019a2f032bbf25e258b01d87f9/limit.maxfiles.plist
# curl -O https://gist.githubusercontent.com/a2ikm/761c2ab02b7b3935679e55af5d81786a/raw/ab644cb92f216c019a2f032bbf25e258b01d87f9/limit.maxproc.plist

curl -O https://gist.githubusercontent.com/tombigel/d503800a282fcadbee14b537735d202c/raw/ed73cacf82906fdde59976a0c8248cce8b44f906/limit.maxfiles.plist
curl -O https://gist.githubusercontent.com/tombigel/d503800a282fcadbee14b537735d202c/raw/ed73cacf82906fdde59976a0c8248cce8b44f906/limit.maxproc.plist

sudo mv limit.maxfiles.plist /Library/LaunchDaemons
sudo mv limit.maxproc.plist /Library/LaunchDaemons

sudo chown root:wheel /Library/LaunchDaemons/limit.maxfiles.plist
sudo chown root:wheel /Library/LaunchDaemons/limit.maxproc.plist

sudo launchctl load -w /Library/LaunchDaemons/limit.maxfiles.plist
```

这适用于 Catalina 和 Mojave macOS。

<!--
## Get involved with SIG Docs

Learn more about SIG Docs Kubernetes community and meetings on the [community page](https://github.com/kubernetes/community/tree/master/sig-docs#meetings).

You can also reach the maintainers of this project at:

- [Slack](https://kubernetes.slack.com/messages/sig-docs) [Get an invite for this Slack](https://slack.k8s.io/)
- [Mailing List](https://groups.google.com/forum/#!forum/kubernetes-sig-docs)
-->
# 参与 SIG Docs 工作

通过 [社区页面](https://github.com/kubernetes/community/tree/master/sig-docs#meetings)
进一步了解 SIG Docs Kubernetes 社区和会议信息。

你也可以通过以下渠道联系本项目的维护人员：

- [Slack](https://kubernetes.slack.com/messages/sig-docs) [加入Slack](https://slack.k8s.io/)
- [邮件列表](https://groups.google.com/forum/#!forum/kubernetes-sig-docs)

<!--
## Contributing to the docs

You can click the **Fork** button in the upper-right area of the screen to create a copy of this repository in your GitHub account. This copy is called a *fork*. Make any changes you want in your fork, and when you are ready to send those changes to us, go to your fork and create a new pull request to let us know about it.

Once your pull request is created, a Kubernetes reviewer will take responsibility for providing clear, actionable feedback.  As the owner of the pull request, **it is your responsibility to modify your pull request to address the feedback that has been provided to you by the Kubernetes reviewer.**
-->
# 为文档做贡献

你也可以点击屏幕右上方区域的 **Fork** 按钮，在你自己的 GitHub
账号下创建本仓库的拷贝。此拷贝被称作 *fork*。
你可以在自己的拷贝中任意地修改文档，并在你已准备好将所作修改提交给我们时，
在你自己的拷贝下创建一个拉取请求（Pull Request），以便让我们知道。

一旦你创建了拉取请求，某个 Kubernetes 评审人会负责提供明确的、可执行的反馈意见。
作为拉取请求的拥有者，*修改拉取请求以解决 Kubernetes
评审人所提出的反馈是你的责任*。

<!--
Also, note that you may end up having more than one Kubernetes reviewer provide you feedback or you may end up getting feedback from a Kubernetes reviewer that is different than the one initially assigned to provide you feedback.

Furthermore, in some cases, one of your reviewers might ask for a technical review from a Kubernetes tech reviewer when needed.  Reviewers will do their best to provide feedback in a timely fashion but response time can vary based on circumstances.
-->
还要提醒的一点，有时可能会有不止一个 Kubernetes 评审人为你提供反馈意见。
有时候，某个评审人的意见和另一个最初被指派的评审人的意见不同。

更进一步，在某些时候，评审人之一可能会在需要的时候请求 Kubernetes
技术评审人来执行技术评审。
评审人会尽力及时地提供反馈意见，不过具体的响应时间可能会因时而异。

<!--
For more information about contributing to the Kubernetes documentation, see:

* [Contribute to Kubernetes docs](https://kubernetes.io/docs/contribute/)
* [Page Content Types](https://kubernetes.io/docs/contribute/style/page-content-types/)
* [Documentation Style Guide](https://kubernetes.io/docs/contribute/style/style-guide/)
* [Localizing Kubernetes Documentation](https://kubernetes.io/docs/contribute/localization/)
-->
有关为 Kubernetes 文档做出贡献的更多信息，请参阅：

* [贡献 Kubernetes 文档](https://kubernetes.io/docs/contribute/)
* [页面内容类型](https://kubernetes.io/docs/contribute/style/page-content-types/)
* [文档风格指南](https://kubernetes.io/docs/contribute/style/style-guide/)
* [本地化 Kubernetes 文档](https://kubernetes.io/docs/contribute/localization/)

# 中文本地化

可以通过以下方式联系中文本地化的维护人员：

* Rui Chen ([GitHub - @chenrui333](https://github.com/chenrui333))
* He Xiaolong ([GitHub - @markthink](https://github.com/markthink))
* [Slack channel](https://kubernetes.slack.com/messages/kubernetes-docs-zh)

<!--
### Code of conduct

Participation in the Kubernetes community is governed by the [CNCF Code of Conduct](https://github.com/cncf/foundation/blob/master/code-of-conduct.md).
-->
# 行为准则

参与 Kubernetes 社区受 [CNCF 行为准则](https://github.com/cncf/foundation/blob/master/code-of-conduct.md) 约束。

<!--
## Thank you!

Kubernetes thrives on community participation, and we appreciate your contributions to our website and our documentation!
-->
# 感谢！

Kubernetes 因为社区的参与而蓬勃发展，感谢您对我们网站和文档的贡献！
