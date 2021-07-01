---
title: sysctl
id: sysctl
date: 2019-02-12
full_link: /docs/tasks/administer-cluster/sysctl-cluster/
short_description: >
  An interface for getting and setting Unix kernel parameters

aka:
tags:
- tool
---
 `sysctl` is a semi-standardized interface for reading or changing the
 attributes of the running Unix kernel.

<!--more-->

On Unix-like systems, `sysctl` is both the name of the tool that administrators
use to view and modify these settings, and also the system call that the tool
uses.

{{< glossary_tooltip text="Container" term_id="container" >}} runtimes and
network plugins may rely on `sysctl` values being set a certain way.
