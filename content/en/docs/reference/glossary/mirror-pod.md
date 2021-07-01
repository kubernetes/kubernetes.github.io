---
title: Mirror Pod
id: mirror-pod
date: 2019-08-06
short_description: >
  An object in the API server that tracks a static pod on a kubelet.

aka: 
tags:
- fundamental
---
 A {{< glossary_tooltip text="pod" term_id="pod" >}} object that a kubelet uses
 to represent a {{< glossary_tooltip text="static pod" term_id="static-pod" >}}

<!--more--> 

When the kubelet finds a static pod in its configuration, it automatically tries to
create a Pod object on the Kubernetes API server for it. This means that the pod
will be visible on the API server, but cannot be controlled from there.

(For example, removing a mirror pod will not stop the kubelet daemon from running it).
