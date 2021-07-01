---
title: Kops
id: kops
date: 2018-04-12
full_link: /docs/getting-started-guides/kops/
short_description: >
  A CLI tool that helps you create, destroy, upgrade and maintain production-grade, highly available, Kubernetes clusters.

aka: 
tags:
- tool
- operation
---
 A CLI tool that helps you create, destroy, upgrade and maintain production-grade, highly available, Kubernetes clusters.

<!--more--> 

{{< note >}}
kops has general availability support only for AWS.
Support for using kops with GCE and VMware vSphere are in alpha.
{{< /note >}}

`kops` provisions your cluster with&#58;

  * Fully automated installation
  * DNS-based cluster identification
  * Self-healing&#58; everything runs in Auto-Scaling Groups
  * Limited OS support (Debian preferred, Ubuntu 16.04 supported, early support for CentOS & RHEL)
  * High availability (HA) support
  * The ability to directly provision, or to generate Terraform manifests

You can also build your own cluster using {{< glossary_tooltip term_id="kubeadm" >}} as a building block. `kops` builds on the kubeadm work.
