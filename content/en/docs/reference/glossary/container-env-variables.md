---
title: Container Environment Variables
id: container-env-variables
date: 2018-04-12
full_link: /docs/concepts/containers/container-environment/
short_description: >
  Container environment variables are name=value pairs that provide useful information into containers running in a Pod.

aka: 
tags:
- fundamental
---
 Container environment variables are name=value pairs that provide useful information into containers running in a {{< glossary_tooltip text="pod" term_id="pod" >}}

<!--more-->

Container environment variables provide information that is required by the running containerized applications along with information about important resources to the {{< glossary_tooltip text="containers" term_id="container" >}}. For example, file system details, information about the container itself, and other cluster resources such as service endpoints.
