---
title: user namespace
id: userns
date: 2021-07-13
full_link: https://man7.org/linux/man-pages/man7/user_namespaces.7.html
short_description: >
  A kernel feature to emulate root. Used for "rootless containers".

aka:
tags:
- security
---

A kernel feature to emulate root. Used for "rootless containers".

<!--more-->

User namespace is a Linux kernel feature that allows a non-root user to emulate fake root privileges that are enough to
run containers.

User namespace is effective for mitigating damage of potential container break-out attacks.

User namespace is a namespace of Linux kernel, not a {{< glossary_tooltip text="namespace" term_id="namespace" >}} of Kubernetes.
