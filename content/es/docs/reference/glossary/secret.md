---
title: Secret
id: secret
date: 2019-05-16
full_link: /docs/concepts/configuration/secret/
short_description: >
  Almacena información sensible, como contraseñas, tokens OAuth o claves ssh.

aka:
tags:
- core-object
- security
---
 Un Secret, secreto en castellano, almacena información sensible, como contraseñas, tokens OAuth o claves ssh.

<!--more-->

Ofrece un mayor control sobre cómo usar información sensible y reduce el riesgo de exposición accidental, incluyendo [encriptado](/docs/tasks/administer-cluster/encrypt-data/#ensure-all-secrets-are-encrypted) en reposo. Un {{< glossary_tooltip text="Pod" term_id="pod" >}} referencia el secreto como un simple fichero en un volumen montado o como variables de entorno accesibles en los Containers. Los secretos son ideales para datos confidenciales y los [ConfigMaps](/docs/tasks/configure-pod-container/configure-pod-configmap/) para datos no confidenciales.
