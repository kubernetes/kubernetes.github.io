---
title: Operator pattern
id: operator-pattern
date: 2019-05-21
full_link: /docs/concepts/extend-kubernetes/operator/
short_description: >
  A specialized controller used to manage a custom resource

aka:
tags:
- architecture
---
 The [operator pattern](/docs/concepts/extend-kubernetes/operator/) is a system
design that links a {{< glossary_tooltip term_id="controller" >}} to one or more custom
resources.

<!--more-->

You can extend Kubernetes by adding controllers to your cluster, beyond the built-in
controllers that come as part of Kubernetes itself.

If a running application acts as a controller and has API access to carry out tasks
against a custom resource that's defined in the control plane, that's an example of
the Operator pattern.
