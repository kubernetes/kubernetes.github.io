---
draft: true
layout: blog
title: 'Updating NGINX-Ingress to use the stable Ingress API'
date: 2021-07-15
slug: update-with-ingress-nginx
---

**Authors:** James Strong, Ricardo Katz

With all Kubernetes APIs, there is a process to creating, maintaining, and
ultimately deprecating them once they become GA. The networking.k8s.io API group is no
different. The upcoming Kubernetes 1.22 release will remove several deprecated APIs
that are relevant to networking:

- the `networking.k8s.io/v1beta1` API version of [IngressClass](/docs/concepts/services-networking/ingress/#ingress-class)
- all beta versions of [Ingress](/docs/concepts/services-networking/ingress/): `extensions/v1beta1` and `networking.k8s.io/v1beta1`

On a v1.22 Kubernetes cluster, you'll be able to access Ingress and IngressClass
objects through the stable (v1) APIs, but access via their beta APIs won't be possible.
This change has been in
in discussion since
[2017](https://github.com/kubernetes/kubernetes/issues/43214),
[2019](https://kubernetes.io/blog/2019/07/18/api-deprecations-in-1-16/) with 
1.16 Kubernetes API deprecations, and most recently in
KEP-1453: 
[Graduate Ingress API to GA](https://github.com/kubernetes/enhancements/tree/master/keps/sig-network/1453-ingress-api#122).

During community meetings, the networking Special Interest Group has decided to continue 
supporting Kubernetes versions older than 1.22 with Ingress-NGINX version 0.47.0. 
Support for Ingress-NGINX will continue for six months after Kubernetes 1.22 
is released. Any additional bug fixes and CVEs for Ingress-NGINX will be 
addressed on a need-by-need basis.

Ingress-NGINX will have separate branches and releases of Ingress-NGINX to 
support this model, mirroring the Kubernetes project process. Future 
releases of the Ingress-NGINX project will track and support the latest 
versions of Kubernetes.

{{< table caption="Ingress NGINX supported version with Kubernetes Versions" >}}
Kubernetes version  | Ingress-NGINX version | Notes
:-------------------|:----------------------|:------------
v1.22              | v1.0.0-alpha.2     | New features, plus bug fixes.
v1.21              | v0.47.x        | Bugfixes only, and just for security issues or crashes. No end-of-support date announced.
v1.20              | v0.47.x        | Bugfixes only, and just  for security issues or crashes. No end-of-support date announced.
v1.19              | v0.47.x        | Bugfixes only, and just  for security issues or crashes. Fixes only provided until 6 months after Kubernetes v1.22.0 is released.
{{< /table >}}    

Because of the updates in Kubernetes 1.22, **v0.47.0** will not work with 
Kubernetes 1.22. 

# What you need to do

The team is currently in the process of upgrading ingress-nginx to support 
the v1 migration, you can track the progress 
[here](https://github.com/kubernetes/ingress-nginx/pull/7156).  
We're not making feature improvements to `ingress-nginx` until after the support for
Ingress v1 is complete.

In the meantime to ensure no compatibility issues: 

* Update to the latest version of Ingress-NGINX; currently
  [v0.47.0](https://github.com/kubernetes/ingress-nginx/releases/tag/controller-v0.47.0) 
* After Kubernetes 1.22 is released, ensure you are using the latest version of 
  Ingress-NGINX that supports the stable APIs for Ingress and IngressClass.
* Test Ingress-NGINX version v1.0.0-alpha.2 with Cluster versions >= 1.19 
  and report any issues to the projects Github page. 

The community’s feedback and support in this effort is welcome. The
Ingress-NGINX Sub-project regularly holds community meetings where we discuss
this and other issues facing the project. For more information on the sub-project, 
please see [SIG Network](https://github.com/kubernetes/community/tree/master/sig-network).
