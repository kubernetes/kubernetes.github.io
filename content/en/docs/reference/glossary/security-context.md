---
title: Security Context
id: security-context
date: 2018-04-12
full_link: /docs/tasks/configure-pod-container/security-context/
short_description: >
  The securityContext field defines privilege and access control settings for a Pod or container.

aka: 
tags:
- security
---
 The `securityContext` field defines privilege and access control settings for
a {{< glossary_tooltip text="Pod" term_id="pod" >}} or
{{< glossary_tooltip text="container" term_id="container" >}}.

<!--more-->

In a `securityContext`, you can define: the user that processes run as,
the group that processes run as, and privilege settings.
You can also configure security policies (for example: SELinux, AppArmor or seccomp).

The `PodSpec.securityContext` setting applies to all containers in a Pod.
