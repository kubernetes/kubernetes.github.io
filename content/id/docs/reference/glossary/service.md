---
title: Service
id: service
date: 2020-04-05
full_link: /docs/concepts/services-networking/service/
short_description: >
  Sebuah Cara untuk mengekspos aplikasi yang berjalan pada sebuah kumpulan Pod sebagai layanan jaringan.

aka:
tags:
- fundamental
- core-object
---
Suatu cara yang abstrak untuk mengekspos aplikasi yang berjalan pada sebuah kumpulan
{{<glossary_tooltip text="Pod" term_id="pod">}} sebagai layanan jaringan.
<!--more-->

Rangkaian Pod yang ditargetkan oleh Service (biasanya) ditentukan oleh 
{{<glossary_tooltip text="selector" term_id="selector">}}.
Jika lebih banyak Pod ditambahkan atau dihapus, maka kumpulan Pod yang cocok 
dengan Selector juga akan berubah. Service memastikan bahwa lalu lintas 
jaringan dapat diarahkan ke kumpulan Pod yang ada saat ini sebagai
Workload.