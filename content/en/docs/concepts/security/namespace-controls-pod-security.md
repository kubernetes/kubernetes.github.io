---
reviewers:
- tallclair
title: Per-Namespace Controls for Pod Security
content_type: concept
weight: 20
---

<!-- overview -->

{{< feature-state for_k8s_version="v1.22" state="alpha" >}}

The Kubernetes [Pod Security Standards](/docs/concepts/security/pod-security-standards/) define different isolation levels for Pods. These standards let you define how you want to restrict the behavior of pods in a clear, consistent fashion.

As an Alpha feature, Kubernetes offers a built-in _Pod Security_ mechanism, the successor to [PodSecurityPolicies](/docs/concepts/policy/pod-security-policy/). Pod security restrictions apply at the {{< glossary_tooltip text="namespace" term_id="namespace" >}} level.

{{< note >}}
The PodSecurityPolicy API is deprecated and will be [removed](/docs/reference/using-api/deprecation-guide/#v1-25) from Kubernetes in v1.25.
{{< /note >}}

<!-- body -->

## Getting started

### Enabling the Alpha feature

Setting pod security controls by namespace is an alpha feature. You must enable the `PodSecurity` [feature gate](/docs/reference/command-line-tools-reference/feature-gates/) in order to use it.

```shell
--feature-gates="...,PodSecurity=true"
```

### Configuring namespaces

Provided that you have enabled this feature, you can configure namespaces to define the admission control mode you want to use for pod security in each namespace. Kubernetes defines a set of {{< glossary_tooltip term_id="label" text="labels" >}} that you can set to define which of the predefined Pod Security Standard levels you want to use for a namespace. The label you select defines what action the {{< glossary_tooltip text="control plane" term_id="control-plane" >}} takes if a potential violation is detected:

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

Check out the [examples](#examples) to see example usage of these labels.

#### Configuring Pods

Different policy levels (e.g. `baseline`, `restricted`) have different requirements for [Security Context](/docs/tasks/configure-pod-container/security-context/) objects and other related fields. Check out the [Pod Security Standards](/docs/concepts/security/pod-security-standards) page for an in-depth look at those requirements.

## Exemptions

You can define _exemptions_ from pod security enforcement in order allow he creation of pods that would have otherwise been prohibited due to the policy associated with a given namespace. Exemptions can be statically configured in the [Admission Controller configuration](#configuring-the-admission-controller).

Exemptions must be explicitly enumerated, and do not support indirection such as label or group selectors. Requests meeting exemption criteria are _ignored_ by the Admission Controller (all `enforce`, `audit` and `warn` behaviors), except to record an audit annotation. Exemption dimensions include:

- **Usernames:** requests from users with an exempt authenticated (or impersonated) username are ignored.
- **RuntimeClassNames:** pods and templated pods specifying an exempt runtime class name are ignored.
- **Namespaces:** pods and templated pods in an exempt namespace are ignored.

The username exemption is special in that the creating user is not persisted on the Pod object, and the Pod may be modified by different non-exempt users in the future. See the [Updates section of the Pod Security Standards KEP](https://github.com/kubernetes/enhancements/tree/master/keps/sig-auth/2579-psp-replacement#updates) for details on how non-exempt updates of a previously exempted pod are handled. Use cases for username exemptions include:

- Trusted {{< glossary_tooltip term_id="controller" text="controllers" >}} that create pods.
- Usernames that represent break-glass operations roles, for example for debugging workloads in a namespace that has restrictions configured. This mechanism only works with a username match; you cannot grant exemptions based on group membership.

## Examples

### Adding labels in YAML

This YAML file creates a Namespace `my-secure-namespace` that:

- Blocks any pods that don't satisfy the `baseline` policy requirements.
- Generates a user-facing warning and adds an audit annotation to any created pod that does not meet the `restricted` policy requirements.
- Pins the versions of the `baseline` and `restricted` policies to v1.22.

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: my-secure-namespace
  labels:
    pod-security.kubernetes.io/enforce: baseline
    pod-security.kubernetes.io/enforce-version: v1.22

    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/audit-version: v1.22
    pod-security.kubernetes.io/warn: restricted
    pod-security.kubernetes.io/warn-version: v1.22
```

### Adding labels to existing namespaces with `kubectl label`

{{< note >}}
When an `enforce` policy (or version) label is added or changed, the admission plugin will test each pod in the namespace against the new policy. Violations are returned to the user as warnings.
{{< /note >}}

#### Applying to all namespaces

If you're just getting started with the Pod Security Standards, a suitable first step would be to configure all namespaces as `privileged` but set up audit annotations for a stricter level such as `baseline`:

```shell
kubectl label --overwrite ns --all \
  pod-security.kubernetes.io/enforce=privileged \
  pod-security.kubernetes.io/audit=baseline \
  pod-security.kubernetes.io/warn=baseline
```

#### Applying to a single namespace

You can update a specific namespace as well. This command adds the `enforce=restricted` policy to `my-existing-namespace`, pinning the restricted policy version to v1.22.

```shell
kubectl label --overwrite ns my-existing-namespace \
  pod-security.kubernetes.io/enforce=restricted \
  pod-security.kubernetes.io/enforce-version=v1.22
```

## {{% heading "whatsnext" %}}

- [Pod Security Standards](/docs/concepts/security/pod-security-standards)
- [Enforcing Pod Security Standards](/docs/setup/best-practices/enforcing-pod-security-standards)
- [Enforce Pod Security Standards with the Built-in Admission Controller](/docs/tasks/configure-pod-container/enforce-standards-admission-controller)
- [Enforce Pod Security Standards with the Pod Security Webhook](/docs/tasks/configure-pod-container/enforce-standards-webhook)
- [Migrating from PodSecurityPolicy](/docs/tasks/secure-pods/migrate-from-psp)

<!-- ### Why were the Pod Security Policies deprecated?

There were numerous problems with Pod Security Policies, which led to the decision to deprecate them. [PodSecurityPolicy Deprecation: Past, Present, and Future](https://kubernetes.io/blog/2021/04/06/podsecuritypolicy-deprecation-past-present-and-future/) goes into this decision in more detail.

### When should I pin a policy version?

The Pod Security Standards will continue to evolve over time, even after the feature leaves the Alpha phase. This is because the details of the policies are based on current Pod hardening best practices, which must adapt to new threats as they arise.

**Pinning policies to specific versions will prevent you from detecting and enforcing protections against future threats.** _Only_ consider pinning versions if the default value `latest` would result in your workloads drifting toward less-restrictive configurations in ways that cannot be resolved.

If you find yourself in that situation, consider refactoring workloads to isolate privileged operations as much as possible. -->