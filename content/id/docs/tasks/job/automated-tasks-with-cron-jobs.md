---
title: Menjalankan Tugas-Tugas Otomatis dengan CronJob
min-kubernetes-server-version: v1.8
content_type: task
weight: 10
---

<!-- overview -->

Kamu dapat menggunakan {{< glossary_tooltip text="CronJob" term_id="cronjob" >}} untuk menjalankan {{< glossary_tooltip text="Job" term_id="job" >}} yang dijadwalkan berbasis waktu. Job akan berjalan seperti pekerjaan-pekerjaan [Cron](https://en.wikipedia.org/wiki/Cron) di Linux atau sistem UNIX.

CronJob sangat berguna untuk membuat pekerjaan yang berjalan secara periodik dan berulang, misalnya menjalankan (_backup_) atau mengirim email.
CronJob  juga dapat menjalankan pekerjaan individu pada waktu tertentu, misalnya jika kamu ingin menjadwalkan sebuah pekerjaan dengan periode aktivitas yang rendah.

CronJob  memiliki keterbatasan dan kekhasan.
Misalnya, dalam keadaan tertentu, sebuah CronJob  dapat membuat banyak Job.
Karena itu, Job haruslah _idempotent._

Untuk informasi lanjut mengenai keterbatasan, lihat [CronJob](/id/docs/concepts/workloads/controllers/cron-jobs).



## {{% heading "prerequisites" %}}


* {{< include "task-tutorial-prereqs.md" >}}



<!-- steps -->

## Membuat Sebuah CronJob

CronJob  membutuhkan sebuah berkas konfigurasi.
Ini adalah contoh dari berkas konfigurasi CronJob `.spec` yang akan mencetak waktu sekarang dan pesan "hello" setiap menit:

{{< codenew file="application/job/cronjob.yaml" >}}

Jalankan contoh CronJob menggunakan perintah berikut:

```shell
kubectl create -f https://k8s.io/examples/application/job/cronjob.yaml
```
Keluaran akan mirip dengan ini:

```
cronjob.batch/hello created
```

Kamu juga dapat menggunakan `kubectl run` untuk membuat sebuah CronJob tanpa menulis sebuah konfigurasi yang lengkap:

```shell
kubectl run hello --schedule="*/1 * * * *" --restart=OnFailure --image=busybox -- /bin/sh -c "date; echo Hello from the Kubernetes cluster"
```

Setelah membuat sebuah CronJob, untuk mengecek statusnya kamu dapat menggunakan perintah berikut:

```shell
kubectl get cronjob hello
```
Keluaran akan mirip dengan ini:

```
NAME    SCHEDULE      SUSPEND   ACTIVE   LAST SCHEDULE   AGE
hello   */1 * * * *   False     0        <none>          10s
```

Seperti yang kamu lihat dari hasil perintah di atas, CronJob belum menjadwalkan atau menjalankan pekerjaan apa pun.
Waktu yang biasanya dibutuhkan untuk mengamati Job hingga Job tersebut dibuat akan membutuhkan sekitar satu menit:

```shell
kubectl get jobs --watch
```

Keluaran akan mirip dengan ini:

```
NAME               COMPLETIONS   DURATION   AGE
hello-4111706356   0/1                      0s
hello-4111706356   0/1           0s         0s
hello-4111706356   1/1           5s         5s
```

Sekarang kamu telah melihat satu Job berjalan yang dijadwalkan oleh "hello" CronJob.
Kamu dapat berhenti mengamati Job dan melihat CronJob lagi untuk melihat CronJob menjadwalkan sebuah Job:

```shell
kubectl get cronjob hello
```
Keluaran akan mirip dengan ini:

```
NAME    SCHEDULE      SUSPEND   ACTIVE   LAST SCHEDULE   AGE
hello   */1 * * * *   False     0        50s             75s
```

Kamu dapat melihat bahwa CronJob `hello` berhasil menjadwalkan sebuah Job pada waktu yang ditentukan dalam `LAST SCHEDULE`. Saat ini ada 0 Job yang aktif,  berarti sebuah Job telah selesai atau gagal.

Sekarang, temukan Pod yang dibuat oleh jadwal Job terakhir dan melihat keluaran bawaan dari salah satu Pod.

{{< note >}}
Nama Job dan nama Pod itu berbeda.
{{< /note >}}

```shell
# Ganti "hello-4111706356" dengan nama Job di sistem kamu
pods=$(kubectl get pods --selector=job-name=hello-4111706356 --output=jsonpath={.items[*].metadata.name})
```
Menampilkan log sebuah Pod:

```shell
kubectl logs $pods
```
Keluaran akan mirip dengan ini:

```
Fri Feb 22 11:02:09 UTC 2019
Hello from the Kubernetes cluster
```

## Menghapus sebuah CronJob

Ketika kamu tidak membutuhkan sebuah CronJob lagi, kamu dapat megnhapusnya dengan perintah `kubectl delete cronjob <cronjob name>`:

```shell
kubectl delete cronjob hello
```

Menghapus CronJob akan menghapus semua Job dan Pod yang telah terbuat dan menghentikanya dari pembuatan Job tambahan.
Kamu dapat membaca lebih lanjut tentang menghapus Job di [_garbage collection_](/id/docs/concepts/workloads/controllers/garbage-collection/).

## Menulis Speifikasi Sebuah Cron

Seperti semua konfigurasi Kubernetes, sebuah CronJob membutuhkan _field_ `apiVersion`, `kind`, dan `metadata`. Untuk informasi
umum tentang bekerja dengan berkas konfigurasi, lihat dokumentasi [men-_deploy_ aplikasi](/docs/user-guide/deploying-applications),
dan [mengunakan kubectl untuk manajemen sumber daya](/docs/user-guide/working-with-resources).

Sebuah konfigurasi CronJob juga membutuhkan sebuah [bagian `.spec`](https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status).

{{< note >}}
Semua modifikasi pada sebuah CronJob, terutama `.spec`, akan diterapkan pada proses berikut.
{{< /note >}}

### Penjadwalan

`.spec.schedule` adalah _field_ yang wajib diisi dari sebuah `.spec`
Dibutuhkan sebuah format string [Cron](https://en.wikipedia.org/wiki/Cron), misalnya `0 * * * *` atau `@hourly`, sebagai jadwal Job untuk dibuat dan dieksekusi.

Format ini juga mencakup nilai langkah "Vixie cron". Seperti penjelasan di [FreeBSD manual](https://www.freebsd.org/cgi/man.cgi?crontab%285%29):

> Nilai langkah dapat digunakan bersama dengan rentang. Sebuah rentang diikuti dengan
> `/<number>` menentukan lompatan angka melalui rentang. 
> Misalnya, `0-23/2` dapat digunakan dalam jam untuk menentukan
> perintah akan dieksekusi setiap jam (alternatif dalam bawaan v7 adalah
> `0,2,4,6,8,10,12,14,16,18,20,22`). Langkah-langkah juga diizinkan setelah
> tanda bintang, jadi jika kamu menginginkan "setiap dua jam", gunakan saja `*/2`.

{{< note >}}
Sebuah tanda tanya (`?`) dalam penjadwalan memiliki makna yang sama dengan tanda bintang `*`, yaitu, singkatan dari nilai apa pun yang tersedia untuk _field_ tertentu.
{{< /note >}}

### Templat Job

`.spec.JobTemplate` adalah templat untuk sebuah Job, dan itu wajib.
Templat Job memiliki skema yang sama dengan [Job](/id/docs/concepts/workloads/controllers/jobs-run-to-completion/), kecuali jika bersarang dan tidak memiliki sebuah `apiVersion` atau `kind`.
Untuk informasi lebih lanjut tentang menulis sebuah Job `.spec` lihat [Menulis spesifikasi Job](/id/docs/concepts/workloads/controllers/jobs-run-to-completion/#writing-a-job-spec).

### _Starting Deadline_

_Field_ `.spec.startingDeadlineSeconds` adalah _field_ opsional.
_Field_ tersebut berarti batas waktu dalam satuan detik untuk memulai sebuah Job jika Job melewatkan waktu yang telah dijadwalkan karena alasan apapun.
Setelah mencapai batas waktu, CronJob tidak akan memulai sebuah Job.
Job yang tidak memenuhi batas waktu, dengan cara ini dianggap sebagai Job yang gagal.
Jika _field_ ini tidak ditentukan, maka Job tidak memiliki batas waktu.

_Controller_ CronJob menghitung berapa banyak jadwal yang terlewat untuk sebuah CronJob. jika lebih dari 100 jadwal yang terlewat, maka tidak ada lagi CronJob yang akan dijadwalkan. Ketika `.spec.startingDeadlineSeconds` tidak disetel, CronJob Controller menghitung jadwal yang terlewat dari `status.lastScheduleTime` hingga sekarang.

Misalnya, sebuah CronJob seharusnya berjalan setiap menit, `status.lastScheduleTime` CronJob adalah pukul 5:00am, tetapi sekarang pukul 07:00am. Itu berarti ada 120 jadwal yang terlewat, maka tidak ada lagi CronJob yang akan dijadwalkan.

Jika _field_ `.spec.startingDeadlineSeconds` disetel (tidak kosong), CronJob Controller akah menghitung berapa banyak Job yang terlewat dari nilai `.spec.startingDeadlineSeconds` hingga sekarang.

Misalnya, jika disetel ke `200`, CronJob Controller akan menghitung jadwal yang terlewat dalam 200 detik terakhir. Pada kasus ini, jika terdapat lebih dari 100 jadwal yang terlewat dalam 200 detik terakhir, maka tidak ada lagi CronJob yang akan dijadwalkan. 

### Kebijakan _Concurrency_

_Field_ `.spec.concurrencyPolicy` juga opsional.
_Field_ tersebut menentukan bagaimana memperlakukan eksekusi _concurrent_ dari sebuah Job yang dibuat oleh CronJob.
Kamu dapat menetapkan hanya satu dari kebijakan _concurrency_:

* `Allow` (bawaan): CronJob mengizinkan Job berjalan secara _concurrent_
* `Forbid` : Job tidak mengizinkan Job berjalan secara _concurrent_; jika sudah saatnya untuk menjalankan Job baru dan Job sebelumnya belum selesai, maka CronJob akan melewatkan Job baru yang akan berjalan
* `Replace`: Jika sudah saatnya untuk menjalankan Job baru dan Job sebelumnya belum selesai, maka CronJob akan mengganti Job yang sedang berjalan dengan Job baru.

Perhatikan bahwa kebijakan _concurrency_ hanya berlaku untuk Job yang dibuat dengan CronJob yang sama.
Jika terdapat banyak CronJob, Job akan selalu diizinkan untuk berjalan secara _concurrent_.

### Penangguhan

_Field_ `.spec.suspend` juga opsional.
Jika _field_ tersebut disetel `true`, semua eksekusi selanjutnya akan ditangguhkan.
Konfigurasi ini tidak dapat berlaku untuk eksekusi yang sudah dimulai.
Secara bawaan _false_.

{{< caution >}}
Eksekusi yang ditangguhkan selama waktu yang dijadwalkan dihitung sebagai Job yang terlewat.
Ketika `.spec.suspend` diubah dari `true` ke `false` pada CronJob yang memiliki konfigurasi tanpa [batas waktu](#starting-deadline), Job yang terlewat akan dijadwalkan segera.
{{< /caution >}}

### Batas Riwayat Pekerjaan

_Field_ `.spec.successfulJobHistoryLimit` dan `.spec.failedJobHistoryLimit` juga opsional.
_Field_ tersebut menentukan berapa banyak Job yang sudah selesai dan gagal yang harus disimpan.
Secara bawaan, masing-masing _field_ tersebut disetel 3 dan 1. Mensetel batas ke `0` untuk menjaga tidak ada Job yang sesuai setelah Job tersebut selesai.


