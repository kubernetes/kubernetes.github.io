---
reviewers:
- tallclair
- liggitt
title: Pod Security Admission
description: >
  An overview of the Pod Security Admission Controller, which can enforce the Pod Security
  Standards.
content_type: concept
weight: 20
min-kubernetes-server-version: v1.22
---

<!-- overview -->

{{< feature-state for_k8s_version="v1.22" state="alpha" >}}

The Kubernetes [Pod Security Standards](/docs/concepts/security/pod-security-standards/) define
different isolation levels for Pods. These standards let you define how you want to restrict the
behavior of pods in a clear, consistent fashion.

As an Alpha feature, Kubernetes offers a built-in _Pod Security_ admission plugin, the successor
to [PodSecurityPolicies](/docs/concepts/policy/pod-security-policy/). Pod security restrictions
are applied at the {{< glossary_tooltip text="namespace" term_id="namespace" >}} level when pods
are created.

{{< note >}}
The PodSecurityPolicy API is deprecated and will be 
[removed](/docs/reference/using-api/deprecation-guide/#v1-25) from Kubernetes in v1.25.
{{< /note >}}

<!-- body -->

## Enabling the Alpha feature

Setting pod security controls by namespace is an alpha feature. You must enable the `PodSecurity`
[feature gate](/docs/reference/command-line-tools-reference/feature-gates/) in order to use it.

```shell
--feature-gates="...,PodSecurity=true"
```

## Pod Security Admission configuration for pods

Different policy levels (e.g. `baseline`, `restricted`) have different requirements for
[Security Context](/docs/tasks/configure-pod-container/security-context/) objects and other related
fields. Check out the [Pod Security Standards](/docs/concepts/security/pod-security-standards) page
for an in-depth look at those requirements.

## Pod Security Admission labels for namespaces

Provided that you have enabled this feature, you can configure namespaces to define the admission
control mode you want to use for pod security in each namespace. Kubernetes defines a set of 
{{< glossary_tooltip term_id="label" text="labels" >}} that you can set to define which of the 
predefined Pod Security Standard levels you want to use for a namespace. The label you select
defines what action the {{< glossary_tooltip text="control plane" term_id="control-plane" >}}
takes if a potential violation is detected:

{{< table caption="Pod Security Admission modes" >}}
Mode | Description
:---------|:------------
**`enforce`** | Policy violations will cause the pod to be rejected.
**`audit`** | Policy violations will trigger the addition of an audit annotation, but are otherwise allowed.
**`warn`** | Policy violations will trigger a user-facing warning, but are otherwise allowed.
{{< /table >}}

For each mode, there are two labels that you can use:

```yaml
# The per-mode level label indicates which policy level to apply for the mode.
#
# MODE must be one of `enforce`, `audit`, or `warn`.
# LEVEL must be one of `privileged`, `baseline`, or `restricted`.
pod-security.kubernetes.io/<MODE>: <LEVEL>

# Optional: per-mode version label that can be used to pin the policy to the
# version that shipped with a given Kubernetes minor version (e.g. v{{< skew latestVersion >}}).
#
# MODE must be one of `enforce`, `audit`, or `warn`.
# VERSION must be a valid Kubernetes version label.
pod-security.kubernetes.io/<MODE>-version: <VERSION>
```

Check out [Enforce Pod Security Standards with Namespace Labels](/docs/tasks/configure-pod-container/enforce-standards-namespace-labels) to see example usage.

## Exemptions

You can define _exemptions_ from pod security enforcement in order allow the creation of pods that
would have otherwise been prohibited due to the policy associated with a given namespace.
Exemptions can be statically configured in the
[Admission Controller configuration](#configuring-the-admission-controller).

Exemptions must be explicitly enumerated, and do not support indirection such as label or group
selectors. Requests meeting exemption criteria are _ignored_ by the Admission Controller (all
`enforce`, `audit` and `warn` behaviors), except to record an audit annotation. Exemption
dimensions include:

- **Usernames:** requests from users with an exempt authenticated (or impersonated) username are
  ignored.
- **RuntimeClassNames:** pods and templated pods specifying an exempt runtime class name are
  ignored.
- **Namespaces:** pods and templated pods in an exempt namespace are ignored.

The username exemption is special in that the creating user is not persisted on the Pod object,
and the Pod may be modified by different non-exempt users in the future. Use cases for username
exemptions include:

- Trusted {{< glossary_tooltip term_id="controller" text="controllers" >}} that create pods.
- Usernames that represent break-glass operations roles, for example for debugging workloads
  in a namespace that has restrictions configured. This mechanism only works with a username
  match; you cannot grant exemptions based on group membership.

Updates to the following pod fields are exempt from policy checks, meaning that if a pod update request only changes these fields, it will not be denied even if the pod is in violation of the current policy level:

- Any metadata updates EXCEPT changes to the seccomp or apparmor annotations:
  - `seccomp.security.alpha.kubernetes.io/pod` (deprecated)
  - `container.seccomp.security.alpha.kubernetes.io/*` (deprecated)
  - `container.apparmor.security.beta.kubernetes.io/*`
- Valid updates to `.spec.activeDeadlineSeconds`
- Valid updates to `.spec.tolerations`
- Valid updates to Pod resources

## {{% heading "whatsnext" %}}

- [Pod Security Standards](/docs/concepts/security/pod-security-standards)
- [Enforcing Pod Security Standards](/docs/setup/best-practices/enforcing-pod-security-standards)
- [Enforce Pod Security Standards by Configuring the Built-in Admission Controller](/docs/tasks/configure-pod-container/enforce-standards-admission-controller)
- [Enforce Pod Security Standards with Namespace Labels](/docs/tasks/configure-pod-container/enforce-standards-namespace-labels)
- [Migrating from PodSecurityPolicy to PodSecurity](/docs/tasks/secure-pods/migrate-from-psp)