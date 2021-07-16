---
title: Enforce Pod Security Standards with the Built-in Admission Controller
reviewers:
- tallclair
content_type: task
---

You can set cluster-wide defaults and [exemptions](#exemptions) for pod security.

```yaml
apiVersion: apiserver.config.k8s.io/v1
kind: AdmissionConfiguration
plugins:
- name: PodSecurity
  configuration:
    defaults:  # Defaults applied when a mode label is not set.
      enforce:         <default enforce policy level>
      enforce-version: <default enforce policy version>
      audit:           <default audit policy level>
      audit-version:   <default audit policy version>
      warn:            <default warn policy level>
      warn-version:    <default warn policy version>
    exemptions:
      usernames:         [ <array of authenticated usernames to exempt> ]
      runtimeClassNames: [ <array of runtime class names to exempt> ]
      namespaces:        [ <array of namespaces to exempt> ]
```