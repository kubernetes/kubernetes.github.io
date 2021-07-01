---
title: Service
id: service
date: 2018-04-12
full_link: /docs/concepts/services-networking/service/
short_description: >
  A way to expose an application running on a set of Pods as a network service.

aka:
tags:
- fundamental
- core-object
---
An abstract way to expose an application running on a set of {{< glossary_tooltip text="Pods" term_id="pod" >}} as a network service.

<!--more-->

 The set of Pods targeted by a Service is (usually) determined by a {{< glossary_tooltip text="selector" term_id="selector" >}}. If more Pods are added or removed, the set of Pods matching the selector will change. The Service makes sure that network traffic can be directed to the current set of Pods for the workload.
