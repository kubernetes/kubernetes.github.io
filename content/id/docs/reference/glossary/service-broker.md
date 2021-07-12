---
title: Makelar Servis
id: service-broker
date: 2018-04-12
full_link: 
short_description: >
  Sebuah _endpoint_ untuk kumpulan servis terlola yang ditawarkan dan dikelola
  oleh penyedia layanan pihak ketiga.

aka: 
tags:
- extension
---
 Sebuah _endpoint_ untuk kumpulan {{< glossary_tooltip text="servis terkelola" term_id="managed-service" >}} yang ditawarkan dan dikelola oleh penyedia layanan pihak
 ketiga.

<!--more--> 

{{< glossary_tooltip text="Makelar servis" term_id="service-broker" >}} mengimplementasikan
[_Open Service Broker API spec_]
(https://github.com/openservicebrokerapi/servicebroker/blob/v2.13/spec.md) dan menyediakan
standar baku untuk aplikasi menggunakan servis yang dikelolanya. [Katalog Servis]
(/docs/concepts/service-catalog) menyediakan cara untuk membuat daftar, melakukan _provision_,
dan mengikat dengan servis terkelola yang ditawarkan oleh makelar servis.