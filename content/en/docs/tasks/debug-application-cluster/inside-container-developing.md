---
title: Developing and debugging services with local IDE inside container
content_type: task
---

Kubernetes applications are generally composed of many microservices. Due to environmental and resource constraints, These microservices are sometimes difficult to run locally as source code. If you use Minikube as a development environment locally, you have to rebuild docker image after writing the code, and modify the image version of the waiting to take effect, which leads to a lot of waste of time and low development efficiency.

`Nocalhost` is a tool that simplifies the development of microservices in the Kubernetes environment. The core function it provides is: use IDE plug-ins (including VSCode and Jetbrains) to develop directly in the container with a graphical interface, And realized real-time synchronization of local code and remote container, Get rid of the trouble of relying on CI/CD to verify the code in some scenarios and rebuilding the docker image.

This document describes how to use `Nocalhost` to directly develop microservices in a container under Kubernetes environment.

## {{% heading "prerequisites" %}}

* Kubernetes cluster is installed
* Install [Nocalhost](https://nocalhost.dev/installation/) plugin (support VSCode and Jetbrains)

## Add Kubeconfig for Nocalhost

Take the VSCode plug-in as an example, you can select context under `~/.kube/config` or "Paste kubeconfig".

After add Kubeconfig has been completed, you can view the workload under the cluster in the plugin. For example, the cluster has been deployed with the Istio sample [bookinfo](https://raw.githubusercontent.com/istio/istio/release-1.10/samples/bookinfo/platform/kube/bookinfo.yaml).

![Nocalhost VSCode Plugin](/images/docs/nocalhost-vscode-plugin.png)

## Develop and debug the workload of the cluster

Using the Nocalhost plug-in, you can easily perform port forwarding, view logs, and enter the terminal.

For example, to forward the remote `9080` port of `productpage-v1` to the local `9080` port, just right-click the service, select "Port Forward", and enter `9080:9080`.

At this point, open the browser `127.0.0.1:9080`, you should see the following interface.

![Nocalhost Bookinfo Productpage](/images/docs/nocalhost-bookinfo-productpage.png)

Now, suppose you want to change the line of "The Comedy of Errors" on the web (it is known that the text is output by the `productpage-v1` service). Generally speaking, we have two solutions:

* The first way: modify the source code locally, run `docker build` to build the image, update the workload image version and wait for it to take effect.
* The second way: Use tools such as `Telepresence` to run the `productpage-v1` service locally with source code, and hijack the local domain name to resolve to the remote cluster so that it can access the remote `details`, `ratings `, `reviews` service.

For some complex microservices, because of differences in resources and environments, it is difficult to run the services to be developed locally with source code, So most people will choose the first solution, which is difficult to accept.

Now, with Nocalhost, you can choose a new development method: develop directly in the container.

For example, to develop the `productpage-v1` service. 

first step: clone the source code of the project (it may take a few minutes).

```
git clone https://github.com/istio/istio.git
```

second step: change `productpage-v1` to development mode.

back to the Nocalhost plugin and click the green "hammer" icon on the right side of the `productpage-v1` service. It only takes two steps to enter the `productpage-v1` service into development mode:

* Select `Open local directory`, and select the `istio/samples/bookinfo/src/productpage/` directory.
* Select "Custom" in the new window and enter `python:3.7.7-slim`

After entering the development mode, the VSCode plugin will get the `Terminal` of the **remote container**.

![Nocalhost Remote Dev Container](/images/docs/nocalhost-remote-dev-container.png)

Execute the `ls` command in `Terminal`:

```
/home/nocalhost-dev # ls
Dockerfile productpage.py requirements.txt static templates test-requirements.txt tests
```

It can be found that the source code of `productpage-v1` has been synchronized to the remote container. 

third step: run code inside container:

```
pip install -r requirements.txt && python productpage.py 9080
```

After a while, the `productpage` service will start.


fourth step: edit local code.

use `VSCode` to edit line `355` of `productpage.py` file under `workspace`, change `The Comedy of Errors` to `The Comedy of Errors Code Change Here`, and save the changes.

![Nocalhost Bookinfo Productpage Code Change](/images/docs/nocalhost-bookinfo-productpage-code-change.png)

Reopen the browser `127.0.0.1:9080`, and you should see the following interface:

![Nocalhost Bookinfo Productpage New Web](/images/docs/nocalhost-bookinfo-productpage-new-web.png)

Now, any local code modification will be synchronized to the remote in real time. Because the `productpage-v1` service has the capability of hot reloading, it will automatically restart the service.

So far, we have completed the demonstration of using Nocalhost to develop the `productpage-v1` service.

In this process, developers do not need to learn additional tool commands, and directly develop services in a graphical interface in the IDE which is closest to the developer, improves the development experience and efficiency in the Kubernetes environment.

## {{% heading "whatsnext" %}}

If you are interested in this tutorial, please check [quick start](https://nocalhost.dev/getting-started/).

For more information, please visit [Nocalhost website](https://nocalhost.dev).