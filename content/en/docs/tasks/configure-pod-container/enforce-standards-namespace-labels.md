---
title: Enforce Pod Security Standards with Namespace Labels
reviewers:
- tallclair
- liggitt
content_type: task
min-kubernetes-server-version: v1.22
---

Namespaces can be labeled to enforce the [Pod Security Standards](/docs/concepts/security/pod-security-standards).

## {{% heading "prerequisites" %}}

- Enable the `PodSecurity` [feature gate](/docs/reference/command-line-tools-reference/feature-gates/#feature-gates-for-alpha-or-beta-features).

## Requiring the `baseline` Pod Security Standard with namespace labels

This manifest defines a Namespace `my-baseline-namespace` that:

- _Blocks_ any pods that don't satisfy the `baseline` policy requirements.
- Generates a user-facing warning and adds an audit annotation to any created pod that does not
  meet the `restricted` policy requirements.
- Pins the versions of the `baseline` and `restricted` policies to v{{< skew latestVersion >}}.

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: my-baseline-namespace
  labels:
    pod-security.kubernetes.io/enforce: baseline
    pod-security.kubernetes.io/enforce-version: v{{< skew latestVersion >}}

    # We are setting these to our _desired_ `enforce` level.
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/audit-version: v{{< skew latestVersion >}}
    pod-security.kubernetes.io/warn: restricted
    pod-security.kubernetes.io/warn-version: v{{< skew latestVersion >}}
```

## Add labels to existing namespaces with `kubectl label`

{{< note >}}
When an `enforce` policy (or version) label is added or changed, the admission plugin will test
each pod in the namespace against the new policy. Violations are returned to the user as warnings.
{{< /note >}}

It is helpful to apply the `--dry-run` flag when initially evaluating security profile changes for
namespaces. The Pod Security Standard checks will still be run in _dry run_ mode, giving you
information about breakages without actually updating a policy.

```shell
kubectl label --dry-run=server --overwrite ns --all \
    pod-security.kubernetes.io/enforce=baseline
```

### Applying to all namespaces

If you're just getting started with the Pod Security Standards, a suitable first step would be to
configure all namespaces as `privileged` but set up audit annotations for a stricter level such as
`baseline`:

```shell
kubectl label --overwrite ns --all \
  pod-security.kubernetes.io/enforce=privileged \
  pod-security.kubernetes.io/audit=baseline \
  pod-security.kubernetes.io/warn=baseline
```

### Applying to a single namespace

You can update a specific namespace as well. This command adds the `enforce=restricted`
policy to `my-existing-namespace`, pinning the restricted policy version to v{{< skew latestVersion >}}.

```shell
kubectl label --overwrite ns my-existing-namespace \
  pod-security.kubernetes.io/enforce=restricted \
  pod-security.kubernetes.io/enforce-version=v{{< skew latestVersion >}}
```