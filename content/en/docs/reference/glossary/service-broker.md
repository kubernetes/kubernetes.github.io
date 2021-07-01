---
title: Service Broker
id: service-broker
date: 2018-04-12
full_link: 
short_description: >
  An endpoint for a set of Managed Services offered and maintained by a third-party.

aka: 
tags:
- extension
---
 An endpoint for a set of {{< glossary_tooltip text="Managed Services" term_id="managed-service" >}} offered and maintained by a third-party.

<!--more--> 

{{< glossary_tooltip text="Service Brokers" term_id="service-broker" >}} implement the
[Open Service Broker API spec](https://github.com/openservicebrokerapi/servicebroker/blob/v2.13/spec.md)
and provide a standard interface for applications to use their Managed Services.
[Service Catalog](/docs/concepts/extend-kubernetes/service-catalog/) provides a way to
list, provision, and bind with Managed Services offered by Service Brokers.

