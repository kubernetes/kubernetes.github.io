---
reviewers:
- tallclair
title: Enforcing Pod Security Standards
weight: 40
---

<!-- overview -->

This page provides an overview of best practices when it comes to enforcing [Pod Security Standards](/docs/concepts/security/pod-security-standards).

<!-- body -->

## Configure all cluster namespaces

Even if the initial configurations are most permissive (i.e. everything is `privileged`), any Namespaces that lack any configuration at all will become significant gaps in your cluster security model.

We provide an [example](/docs/concepts/security/namespace-controls-pod-security/#applying-to-all-namespaces) that illustrates how you can do this.

## Embrace the principle of least privilege

In an ideal world, every pod in every namespace would meet the requirements of the `restricted` policy. However, this is not possible nor practical, as some workloads will require elevated privileges for legitimate reasons.

- Namespaces allowing `privileged` workloads should establish and enforce appropriate access controls.
- For workloads running in those permissive namespaces, maintain documentation about their unique security requirements. If at all possible, consider how those requirements could be further constrained.

## Adopt a multi-mode strategy

The `audit` and `warn` modes of the Pod Security Standards admission controller make it easy to collect important security insights about your pods without breaking existing workloads.

It is good practice to enable these modes for all namespaces, except maybe for those that will _absolutely_ always require `privileged` access or those that enforce the `restricted` policy. Further, these modes should usually be set to policies at least one level higher than the policy for the `enforce` mode.

- Namespaces enforcing the `privileged` policy (i.e. no restrictions) should set audit and warn labels to `baseline`.
- Namespaces enforcing the `baseline` policy should set audit and warn labels to `restricted`.

Monitoring these annotations and warnings over time will help you identify workloads that can be migrated to namespaces with stricter policies.