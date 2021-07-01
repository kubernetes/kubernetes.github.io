---
title: RBAC (Role-Based Access Control)
id: rbac
date: 2018-04-12
full_link: /docs/reference/access-authn-authz/rbac/
short_description: >
  Manages authorization decisions, allowing admins to dynamically configure access policies through the Kubernetes API.

aka: 
tags:
- security
- fundamental
---
 Manages authorization decisions, allowing admins to dynamically configure access policies through the {{< glossary_tooltip text="Kubernetes API" term_id="kubernetes-api" >}}.

<!--more--> 

RBAC utilizes *roles*, which contain permission rules, and *role bindings*, which grant the permissions defined in a role to a set of users.

