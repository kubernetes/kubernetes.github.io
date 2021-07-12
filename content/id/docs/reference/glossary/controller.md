---
title: Pengontrol
id: controller
date: 2018-04-12
full_link: /id/docs/concepts/architecture/controller/
short_description: >
  Kontrol tertutup yang mengawasi kondisi bersama dari klaster melalui apiserver dan membuat perubahan yang mencoba untuk membawa kondisi saat ini ke kondisi yang diinginkan.

aka:
- Controller
tags:
- architecture
- fundamental
---
Di Kubernetes, pengontrol adalah kontrol tertutup yang mengawasi kondisi {{< glossary_tooltip term_id="cluster" text="klaster">}}, lalu membuat atau meminta perubahan jika diperlukan. Setiap pengontrol mencoba untuk memindahkan status klaster saat ini lebih dekat ke kondisi yang diinginkan.

<!--more-->

Pengontrol mengawasi keadaan bersama (_shared state_) dari klastermu melalui {{< glossary_tooltip text="apiserver" term_id="kube-apiserver" >}} (bagian dari {{< glossary_tooltip term_id="control-plane" >}}).

Beberapa pengontrol juga berjalan di dalam _control plane_, menyediakan kontrol tertutup yang merupakan inti dari operasi Kubernetes. Sebagai contoh: pengontrol Deployment, pengontrol DaemonSet, pengontrol Namespace, dan pengontrol PersistentVolume (dan lainnya) semuanya berjalan di dalam {{< glossary_tooltip term_id="kube-controller-manager" >}}.
