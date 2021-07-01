---
title: ServiceAccount
id: service-account
date: 2018-04-12
full_link: /docs/tasks/configure-pod-container/configure-service-account/
short_description: >
  Provides an identity for processes that run in a Pod.

aka: 
tags:
- fundamental
- core-object
---
 Provides an identity for processes that run in a {{< glossary_tooltip text="Pod" term_id="pod" >}}.

<!--more--> 

When processes inside Pods access the cluster, they are authenticated by the API server as a particular service account, for example, `default`. When you create a Pod, if you do not specify a service account, it is automatically assigned the default service account in the same {{< glossary_tooltip text="Namespace" term_id="namespace" >}}.
