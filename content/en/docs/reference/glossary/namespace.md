---
title: Namespace
id: namespace
date: 2018-04-12
full_link: /docs/concepts/overview/working-with-objects/namespaces
short_description: >
  An abstraction used by Kubernetes to support multiple virtual clusters on the same physical cluster.

aka: 
tags:
- fundamental
---
 An abstraction used by Kubernetes to support multiple virtual clusters on the same physical {{< glossary_tooltip text="cluster" term_id="cluster" >}}.

<!--more--> 

Namespaces are used to organize objects in a cluster and provide a way to divide cluster resources. Names of resources need to be unique within a namespace, but not across namespaces.

