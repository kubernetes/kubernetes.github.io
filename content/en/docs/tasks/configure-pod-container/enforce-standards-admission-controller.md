---
title: Enforce Pod Security Standards by Configuring the Built-in Admission Controller
reviewers:
- tallclair
- liggitt
content_type: task
min-kubernetes-server-version: v1.22
---

As of v1.22, Kubernetes provides a built-in admission controller to enforce the
[Pod Security Standards](/docs/concepts/security/pod-security-standards). You can configure
this admission controller to set cluster-wide defaults and [exemptions](#exemptions).

## {{% heading "prerequisites" %}}

- Enable the `PodSecurity` [feature gate](/docs/reference/command-line-tools-reference/feature-gates/#feature-gates-for-alpha-or-beta-features).

## Configure the Admission Controller

```yaml
apiVersion: apiserver.config.k8s.io/v1
kind: AdmissionConfiguration
plugins:
- name: PodSecurity
  configuration:
    apiVersion: pod-security.admission.config.k8s.io/v1alpha1
    kind: PodSecurityConfiguration
    # Defaults applied when a mode label is not set.
    #
    # Level label values must be one of:
    # - "privileged" (default)
    # - "baseline"
    # - "restricted"
    #
    # Version label values must be one of:
    # - "latest" (default) 
    # - specific version like "v{{< skew latestVersion >}}"
    defaults:
      enforce: "privileged"
      enforce-version: "latest"
      audit: "privileged"
      audit-version: "latest"
      warn: "privileged"
      warn-version: "latest"
    exemptions:
      # Array of authenticated usernames to exempt.
      usernames: []
      # Array of runtime class names to exempt.
      runtimeClassNames: []
      # Array of namespaces to exempt.
      namespaces: []
```