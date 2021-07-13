---
title: Migrate from PodSecurityPolicy
reviewers:
- tallclair
content_type: task
---

<!-- overview -->

Migrating to the replacement policy from PodSecurityPolicies can be done effectively using a combination of dry-run and `audit` and `warn` modes, although this becomes harder if mutating PSPs are used).

<!-- body -->

- [Enable the Pod Security Standards feature gate.](/docs/concepts/security/namespace-controls-pod-security#enabling-the-alpha-feature)
- **Temporarily set the default `enforce` mode to `privileged` for all Namespaces.** This can be done by [configuring the Admission Controller](/docs/concepts/security/namespace-controls-pod-security#configuring-the-admission-controller) or with [`kubectl label`](/docs/concepts/security/namespace-controls-pod-security#applying-to-all-namespaces).
- **Eliminate mutating Pod Security Policies, if your cluster has any set up.**
  - Clone all mutating PSPs into a non-mutating version.
  - Update all ClusterRoles authorizing use of those mutating PSPs to also authorize use of the non-mutating variant.
  - Watch for Pods using the mutating PSPs and work with code owners to migrate to valid, non-mutating resources.
  - Delete mutating PSPs.
- **Select a compatible policy level for each namespace.** Analyze existing resources in the namespace to drive this decision; strive for the `restricted` and `baseline` levels.
  - Review the requirements of the different [Pod Security Standards](/docs/concepts/security/pod-security-standards).
  - Evaluate the difference in privileges that would come from disabling the PSP controller.
- **Apply the selected profiles in `warn` and `audit` mode.** This will give you an idea of how your Pods will respond to the new policies, without breaking existing workloads. Iterate on your [Pods' configuration](/docs/concepts/security/namespace-controls-pod-security#configuring-pods) until they are in compliance with the selected profiles.
- Apply the profiles in enforce mode.
- Disable PodSecurityPolicy!