---
title: Name
id: name
date: 2019-15-05
full_link: /docs/concepts/overview/working-with-objects/names
short_description: >
  String yang dihasilkan oleh klien yang mengacu pada sebuah objek dalam suatu URL resource, seperti `/api/v1/pods/some-name`.

aka:
tags:
- fundamental
---
 String yang dihasilkan oleh klien yang mengacu pada sebuah objek dalam suatu URL *resource*, seperti `/api/v1/pods/some-name`.

<!--more-->

Sebuah objek dengan kind yang sama tidak boleh memiliki nama yang sama pada suatu waktu tertentu. Meskipun begitu, apabila kamu menghapus sebuah objek, kamu membuat sebuah objek baru (yang memiliki kind yang sama) dengan nama yang sama dengan objek yang kamu hapus sebelumnya.
