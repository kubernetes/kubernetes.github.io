---
title: Secret
id: secret
date: 2018-04-12
full_link: /docs/concepts/configuration/secret/
short_description: >
  Stores sensitive information, such as passwords, OAuth tokens, and ssh keys.

aka: 
tags:
- core-object
- security
---
 Stores sensitive information, such as passwords, OAuth tokens, and ssh keys.

<!--more--> 

Allows for more control over how sensitive information is used and reduces the risk of accidental exposure, including [encryption](/docs/tasks/administer-cluster/encrypt-data/#ensure-all-secrets-are-encrypted) at rest.  A {{< glossary_tooltip text="Pod" term_id="pod" >}} references the secret as a file in a volume mount or by the kubelet pulling images for a pod. Secrets are great for confidential data and [ConfigMaps](/docs/tasks/configure-pod-container/configure-pod-configmap/) for non-confidential data.
