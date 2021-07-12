---
title: "Menginstal Peralatan"
description: Peralatan untuk melakukan instalasi Kubernetes dalam komputer kamu.
weight: 10
no_list: true
---

## kubectl

<!-- overview -->

Perangkat baris perintah Kubernetes, [kubectl](/id/docs/reference/kubectl/kubectl/), 
memungkinkan kamu untuk menjalankan perintah pada klaster Kubernetes.
Kamu dapat menggunakan kubectl untuk menerapkan aplikasi, memeriksa dan mengelola sumber daya klaster,
dan melihat *log* (catatan). Untuk informasi lebih lanjut termasuk daftar lengkap operasi kubectl, lihat
[referensi dokumentasi `kubectl`](/id/docs/reference/kubectl/).

kubectl dapat diinstal pada berbagai platform Linux, macOS dan Windows.
Pilihlah sistem operasi pilihan kamu di bawah ini.

- [Instalasi kubectl pada Linux](/en/docs/tasks/tools/install-kubectl-linux)
- [Instalasi kubectl pada macOS](/en/docs/tasks/tools/install-kubectl-macos)
- [Instalasi kubectl pada Windows](/en/docs/tasks/tools/install-kubectl-windows)

## kind

[`kind`](https://kind.sigs.k8s.io/docs/) memberikan kamu kemampuan untuk
menjalankan Kubernetes pada komputer lokal kamu. Perangkat ini membutuhkan
[Docker](https://docs.docker.com/get-docker/) yang sudah diinstal dan
terkonfigurasi.

Halaman [Memulai Cepat](https://kind.sigs.k8s.io/docs/user/quick-start/) `kind`
memperlihatkan kepada kamu tentang apa yang perlu kamu lakukan untuk `kind`
berjalan dan bekerja.

<a class="btn btn-primary" href="https://kind.sigs.k8s.io/docs/user/quick-start/" role="button" aria-label="Melihat Memulai Cepat Kind">Melihat Memulai Cepat Kind</a>

## minikube

Seperti halnya dengan `kind`, [`minikube`](https://minikube.sigs.k8s.io/) 
merupakan perangkat yang memungkinkan kamu untuk menjalankan Kubernetes
secara lokal. `minikube` menjalankan sebuah klaster Kubernetes dengan
satu node saja dalam komputer pribadi (termasuk Windows, macOS dan Linux)
sehingga kamu dapat mencoba Kubernetes atau untuk pekerjaan pengembangan
sehari-hari.

Kamu bisa mengikuti petunjuk resmi
[Memulai!](https://minikube.sigs.k8s.io/docs/start/) 
`minikube` jika kamu ingin fokus agar perangkat ini terinstal.

<a class="btn btn-primary" href="https://minikube.sigs.k8s.io/docs/start/" role="button" aria-label="Lihat Panduan Memulai! Minikube">Lihat Panduan Memulai! Minikube</a>

Setelah kamu memiliki `minikube` yang bekerja, kamu bisa menggunakannya
untuk  [menjalankan aplikasi contoh](/id/docs/tutorials/hello-minikube/).

## kubeadm

Kamu dapat menggunakan {{< glossary_tooltip term_id="kubeadm" text="kubeadm" >}} 
untuk membuat dan mengatur klaster Kubernetes.
`kubeadm` menjalankan langkah-langkah yang diperlukan untuk mendapatkan klaster
dengan kelaikan dan keamanan minimum, aktif dan berjalan dengan cara yang mudah
bagi pengguna.

[Instalasi kubeadm](/id/docs/setup/production-environment/tools/kubeadm/install-kubeadm/) memperlihatkan tentang bagaimana melakukan instalasi kubeadm.
Setelah terinstal, kamu dapat menggunakannya untuk [membuat klaster](/id/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/).

<a class="btn btn-primary" href="/docs/setup/production-environment/tools/kubeadm/install-kubeadm/" role="button" aria-label="Lihat panduan instalasi kubeadm">Lihat panduan instalasi kubeadm</a>
