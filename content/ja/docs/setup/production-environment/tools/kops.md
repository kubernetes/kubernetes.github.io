---
title: kopsを使ったAWS上でのKubernetesのインストール
content_type: task
weight: 20
---

<!-- overview -->

This quickstart shows you how to easily install a Kubernetes cluster on AWS.
It uses a tool called [`kops`](https://github.com/kubernetes/kops).

kops is an automated provisioning system:

* Fully automated installation
* Uses DNS to identify clusters
* Self-healing: everything runs in Auto-Scaling Groups
* Multiple OS support (Debian, Ubuntu 16.04 supported, CentOS & RHEL, Amazon Linux and CoreOS) - see the [images.md](https://github.com/kubernetes/kops/blob/master/docs/operations/images.md)
* High-Availability support - see the [high_availability.md](https://github.com/kubernetes/kops/blob/master/docs/operations/high_availability.md)
* Can directly provision, or generate terraform manifests - see the [terraform.md](https://github.com/kubernetes/kops/blob/master/docs/terraform.md)



## {{% heading "prerequisites" %}}


* You must have [kubectl](/docs/tasks/tools/install-kubectl/) installed.

* You must [install](https://github.com/kubernetes/kops#installing) `kops` on a 64-bit (AMD64 and Intel 64) device architecture.

* You must have an [AWS account](https://docs.aws.amazon.com/polly/latest/dg/setting-up.html), generate [IAM keys](https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html#access-keys-and-secret-access-keys) and [configure](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html#cli-quick-configuration) them. The IAM user will need [adequate permissions](https://github.com/kubernetes/kops/blob/master/docs/getting_started/aws.md#setup-iam-user).



<!-- steps -->

## クラスタの作成

### (1/5) kopsのインストール

#### インストール

Download kops from the [releases page](https://github.com/kubernetes/kops/releases) (it is also easy to build from source):

{{< tabs name="kops_installation" >}}
{{% tab name="macOS" %}}

Download the latest release with the command:

```shell
curl -LO https://github.com/kubernetes/kops/releases/download/$(curl -s https://api.github.com/repos/kubernetes/kops/releases/latest | grep tag_name | cut -d '"' -f 4)/kops-darwin-amd64
```

To download a specific version, replace the following portion of the command with the specific kops version.

```shell
$(curl -s https://api.github.com/repos/kubernetes/kops/releases/latest | grep tag_name | cut -d '"' -f 4)
```

For example, to download kops version v1.20.0 type:

```shell
curl -LO https://github.com/kubernetes/kops/releases/download/v1.20.0/kops-darwin-amd64
```

Make the kops binary executable.

```shell
chmod +x kops-darwin-amd64
```

Move the kops binary in to your PATH.

```shell
sudo mv kops-darwin-amd64 /usr/local/bin/kops
```

You can also install kops using [Homebrew](https://brew.sh/).

```shell
brew update && brew install kops
```
{{% /tab %}}
{{% tab name="Linux" %}}

Download the latest release with the command:

```shell
curl -LO https://github.com/kubernetes/kops/releases/download/$(curl -s https://api.github.com/repos/kubernetes/kops/releases/latest | grep tag_name | cut -d '"' -f 4)/kops-linux-amd64
```

To download a specific version of kops, replace the following portion of the command with the specific kops version.

```shell
$(curl -s https://api.github.com/repos/kubernetes/kops/releases/latest | grep tag_name | cut -d '"' -f 4)
```

For example, to download kops version v1.20.0 type:

```shell
curl -LO https://github.com/kubernetes/kops/releases/download/v1.20.0/kops-linux-amd64
```

Make the kops binary executable

```shell
chmod +x kops-linux-amd64
```

Move the kops binary in to your PATH.

```shell
sudo mv kops-linux-amd64 /usr/local/bin/kops
```

You can also install kops using [Homebrew](https://docs.brew.sh/Homebrew-on-Linux).

```shell
brew update && brew install kops
```

{{% /tab %}}
{{< /tabs >}}


### (2/5) クラスタ用のroute53ドメインの作成

kops uses DNS for discovery, both inside the cluster and outside, so that you can reach the kubernetes API server
from clients.

kops has a strong opinion on the cluster name: it should be a valid DNS name.  By doing so you will
no longer get your clusters confused, you can share clusters with your colleagues unambiguously,
and you can reach them without relying on remembering an IP address.

You can, and probably should, use subdomains to divide your clusters.  As our example we will use
`useast1.dev.example.com`.  The API server endpoint will then be `api.useast1.dev.example.com`.

A Route53 hosted zone can serve subdomains.  Your hosted zone could be `useast1.dev.example.com`,
but also `dev.example.com` or even `example.com`.  kops works with any of these, so typically
you choose for organization reasons (e.g. you are allowed to create records under `dev.example.com`,
but not under `example.com`).

Let's assume you're using `dev.example.com` as your hosted zone.  You create that hosted zone using
the [normal process](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/CreatingNewSubdomain.html), or
with a command such as `aws route53 create-hosted-zone --name dev.example.com --caller-reference 1`.

You must then set up your NS records in the parent domain, so that records in the domain will resolve.  Here,
you would create NS records in `example.com` for `dev`.  If it is a root domain name you would configure the NS
records at your domain registrar (e.g. `example.com` would need to be configured where you bought `example.com`).

This step is easy to mess up (it is the #1 cause of problems!)  You can double-check that
your cluster is configured correctly if you have the dig tool by running:

`dig NS dev.example.com`

You should see the 4 NS records that Route53 assigned your hosted zone.

### (3/5) クラスタの状態を保存するS3バケットの作成

kops lets you manage your clusters even after installation.  To do this, it must keep track of the clusters
that you have created, along with their configuration, the keys they are using etc.  This information is stored
in an S3 bucket.  S3 permissions are used to control access to the bucket.

Multiple clusters can use the same S3 bucket, and you can share an S3 bucket between your colleagues that
administer the same clusters - this is much easier than passing around kubecfg files.  But anyone with access
to the S3 bucket will have administrative access to all your clusters, so you don't want to share it beyond
the operations team.

So typically you have one S3 bucket for each ops team (and often the name will correspond
to the name of the hosted zone above!)

In our example, we chose `dev.example.com` as our hosted zone, so let's pick `clusters.dev.example.com` as
the S3 bucket name.

* Export `AWS_PROFILE` (if you need to select a profile for the AWS CLI to work)

* Create the S3 bucket using `aws s3 mb s3://clusters.dev.example.com`

* You can `export KOPS_STATE_STORE=s3://clusters.dev.example.com` and then kops will use this location by default.
   We suggest putting this in your bash profile or similar.


### (4/5) クラスタ設定の構築

Run `kops create cluster` to create your cluster configuration:

`kops create cluster --zones=us-east-1c useast1.dev.example.com`

kops will create the configuration for your cluster.  Note that it _only_ creates the configuration, it does
not actually create the cloud resources - you'll do that in the next step with a `kops update cluster`.  This
give you an opportunity to review the configuration or change it.

It prints commands you can use to explore further:

* List your clusters with: `kops get cluster`
* Edit this cluster with: `kops edit cluster useast1.dev.example.com`
* Edit your node instance group: `kops edit ig --name=useast1.dev.example.com nodes`
* Edit your master instance group: `kops edit ig --name=useast1.dev.example.com master-us-east-1c`

If this is your first time using kops, do spend a few minutes to try those out!  An instance group is a
set of instances, which will be registered as kubernetes nodes.  On AWS this is implemented via auto-scaling-groups.
You can have several instance groups, for example if you wanted nodes that are a mix of spot and on-demand instances, or
GPU and non-GPU instances.


### (5/5) AWSにクラスタを作成

Run "kops update cluster" to create your cluster in AWS:

`kops update cluster useast1.dev.example.com --yes`

That takes a few seconds to run, but then your cluster will likely take a few minutes to actually be ready.
`kops update cluster` will be the tool you'll use whenever you change the configuration of your cluster; it
applies the changes you have made to the configuration to your cluster - reconfiguring AWS or kubernetes as needed.

For example, after you `kops edit ig nodes`, then `kops update cluster --yes` to apply your configuration, and
sometimes you will also have to `kops rolling-update cluster` to roll out the configuration immediately.

Without `--yes`, `kops update cluster` will show you a preview of what it is going to do.  This is handy
for production clusters!

### 他のアドオンの参照

See the [list of add-ons](/docs/concepts/cluster-administration/addons/) to explore other add-ons, including tools for logging, monitoring, network policy, visualization, and control of your Kubernetes cluster.

## クリーンアップ

* To delete your cluster: `kops delete cluster useast1.dev.example.com --yes`



## {{% heading "whatsnext" %}}


* Learn more about Kubernetes [concepts](/docs/concepts/) and [`kubectl`](/docs/reference/kubectl/overview/).
* Learn more about `kops` [advanced usage](https://kops.sigs.k8s.io/) for tutorials, best practices and advanced configuration options.
* Follow `kops` community discussions on Slack: [community discussions](https://github.com/kubernetes/kops#other-ways-to-communicate-with-the-contributors)
* Contribute to `kops` by addressing or raising an issue [GitHub Issues](https://github.com/kubernetes/kops/issues)


