---
reviewers:
- tallclair
- liggitt
title: Enforcing Pod Security Standards
weight: 40
---

<!-- overview -->

This page provides an overview of best practices when it comes to enforcing [Pod Security Standards](/docs/concepts/security/pod-security-standards).

<!-- body -->

## Using the built-in Pod Security Admission Controller

{{< feature-state for_k8s_version="v1.22" state="alpha" >}}

The Pod Security Admission Controller intends to replace the deprecated PodSecurityPolicies. 

### Configure all cluster namespaces

Even if the initial configurations are most permissive (i.e. everything is `privileged`), any Namespaces that lack any configuration at all will become significant gaps in your cluster security model.

We provide an [example](/docs/concepts/security/pod-security-admission/#applying-to-all-namespaces) that illustrates how you can do this.

### Embrace the principle of least privilege

In an ideal world, every pod in every namespace would meet the requirements of the `restricted` policy. However, this is not possible nor practical, as some workloads will require elevated privileges for legitimate reasons.

- Namespaces allowing `privileged` workloads should establish and enforce appropriate access controls.
- For workloads running in those permissive namespaces, maintain documentation about their unique security requirements. If at all possible, consider how those requirements could be further constrained.

### Adopt a multi-mode strategy

The `audit` and `warn` modes of the Pod Security Standards admission controller make it easy to collect important security insights about your pods without breaking existing workloads.

It is good practice to enable these modes for all namespaces, setting them to the _desired_ level and version you would eventually like to `enforce`. The warnings and annotations generated in this phase can guide you toward that state.

When you have the `enforce` mode set to your desired value, these modes can still be useful in a few different ways:

- By setting `warn` to the same level as `enforce`, clients will receive warnings when attempting to create Pods (or resources that have Pod templates) that do not pass validation. This will help them update those resources to become compliant.
- In Namespaces that pin `enforce` to a specific non-latest version, setting the `audit` and `warn` modes to the same level as `enforce`, but to the `latest` version, gives visibility into settings that were allowed by previous versions but are not allowed per current best practices.

## Using PodSecurityPolicies



## Third-party alternatives

Other alternatives for enforcing security profiles are being developed in the Kubernetes
ecosystem:

- [OPA Gatekeeper](https://github.com/open-profile-agent/gatekeeper).

The decision to go with a _native_ solution (e.g. PodSecurity admission controller) versus a
third-party tool is entirely dependent on your own situation. When evaluating any solution,
trust of your supply chain is crucial. Ultimately, using _any_ of the aforementioned approaches
will be better than doing nothing.