---
title: ConfigMap
id: configmap
date: 2018-04-12
full_link: /docs/concepts/configuration/configmap/
short_description: >
  An API object used to store non-confidential data in key-value pairs. Can be consumed as environment variables, command-line arguments, or configuration files in a volume.

aka: 
tags:
- core-object
---
 An API object used to store non-confidential data in key-value pairs.
{{< glossary_tooltip text="Pods" term_id="pod" >}} can consume ConfigMaps as
environment variables, command-line arguments, or as configuration files in a
{{< glossary_tooltip text="volume" term_id="volume" >}}.

<!--more--> 

A ConfigMap allows you to decouple environment-specific configuration from your {{< glossary_tooltip text="container images" term_id="image" >}}, so that your applications are easily portable.
