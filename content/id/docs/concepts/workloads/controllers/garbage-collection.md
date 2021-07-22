---
title: Garbage Collection
content_type: concept
weight: 60
---

<!-- overview -->

Peran daripada _garbage collector_ Kubernetes adalah untuk menghapus objek tertentu yang sebelumnya mempunyai pemilik, tetapi tidak lagi mempunyai pemilik.



<!-- body -->

## Pemilik dan dependen

Beberapa objek Kubernetes adalah pemilik dari objek lainnya. Sebagai contoh, sebuah ReplicaSet adalah pemilik dari sekumpulan Pod. Objek-objek yang dimiliki disebut *dependen* dari objek pemilik. Setiap objek dependen memiliki sebuah kolom `metadata.ownerReferences` yang menunjuk ke objek pemilik.

Terkadang, Kubernetes menentukan nilai dari `ownerReference` secara otomatis. Sebagai contoh, ketika kamu membuat sebuah ReplicaSet, Kubernetes secara otomatis akan menentukan tiap kolom `ownerReference` dari tiap Pod di dalam ReplicaSet. Pada versi 1.8, Kubernetes secara otomatis menentukan nilai dari `ownerReference` untuk objek yang diciptakan atau diadopsi oleh ReplicationController, ReplicaSet, StatefulSet, DaemonSet, Deployment, Job dan CronJob.

Kamu juga bisa menspesifikasikan hubungan antara pemilik dan dependen dengan cara menentukan kolom `ownerReference` secara manual.

Berikut adalah berkas untuk sebuah ReplicaSet yang memiliki tiga Pod:

{{< codenew file="controllers/replicaset.yaml" >}}


Jika kamu membuat ReplicaSet tersebut dan kemudian melihat metadata Pod, kamu akan melihat kolom OwnerReferences:

```shell
kubectl apply -f https://k8s.io/examples/controllers/replicaset.yaml
kubectl get pods --output=yaml
```

Keluaran menunjukkan bahwa pemilik Pod adalah sebuah ReplicaSet bernama `my-repset`:

```shell
apiVersion: v1
kind: Pod
metadata:
  ...
  ownerReferences:
  - apiVersion: apps/v1
    controller: true
    blockOwnerDeletion: true
    kind: ReplicaSet
    name: my-repset
    uid: d9607e19-f88f-11e6-a518-42010a800195
  ...
```
{{< note >}}
Referensi pemilik lintas _namespace_ tidak diperbolehkan oleh desain. Artinya:
1) Dependen dengan cakupan _namespace_ hanya bisa menspesifikasikan pemilik jika berada di _namespace_ yang sama, dan pemilik memiliki cakupan klaster.
2) Dependen dengan cakupan klaster hanya bisa menspesifikasikan pemilik yang memiliki cakupan klaster, tetapi tidak berlaku untuk pemilik yang memiliki cakupan klaster.
{{< /note >}}

## Mengontrol bagaimana _garbage collector_ menghapus dependen

Ketika kamu menghapus sebuah objek, kamu bisa menspesifikasi apakah dependen objek tersebut juga dihapus secara otomatis. Menghapus dependen secara otomatis disebut _cascading deletion_. _Cascading deletion_ memiliki dua mode: _background_ dan _foreground_.



### Foreground cascading deletion

Pada *foreground cascading deletion*, pertama objek utama akan memasuki keadaan "_deletion in progress_". Pada saat keadaan "_deletion in progress_", kondisi-kondisi berikut bernilai benar:

 * Objek masih terlihat via REST API
 * `deletionTimestamp` objek telah ditentukan
 * `metadata.finalizers` objek memiliki nilai `foregroundDeletion`.

 Ketika dalam keadaan "_deletion in progress_", _garbage collector_ menghapus dependen dari objek. Ketika _garbage collector_ telah menghapus semua "_blocking_" dependen (objek dengan `ownerReference.blockOwnerDeleteion=true`), _garbage collector_ menghapus objek pemilik.

 Jika kolom `ownerReferences` sebuah objek ditentukan oleh sebuah _controller_ (seperti Deployment atau Replicaset), `blockOwnerDeletion` akan ditentukan secara otomatis dan kamu tidak perlu memodifikasi kolom ini secara manual.

### Background cascading deletion

 Pada *background cascading deletion*, Kubernetes segera menghapus objek pemilik dan _garbage collector_ kemudian menghapus dependen pada _background_.

### Mengatur kebijakan _cascading deletion_

 Untuk mengatur kebijakan _cascading deletion_, tambahkan kolom `propagationPolicy` pada argumen `deleteOptions` ketika menghapus sebuah Object. Nilai yang dapat digunakan adalah "Orphan", "Foreground", atau "Background".

 Sebelum Kubernetes 1.9, kebijakan _default_ dari _garbage collection_ untuk banyak _resource controller_ adalah **orphan**. Ini meliputi ReplicationController, ReplicaSet, StatefulSet, DaemonSet, dan Deployment. Untuk jenis pada kelompok versi `extensions/v1beta1`, `apps/v1beta1`, dan `apps/v1beta2`, kecuali kamu menspesifikasikan dengan cara lain, objek dependen adalah _orphan_ secara _default_. Pada Kubernetes 1.9, untuk semua jenis pada kelompok versi `apps/v1`, objek dependen dihapus secara _default_.

 Berikut sebuah contoh yang menghapus dependen di _background_:

```shell
kubectl proxy --port=8080
curl -X DELETE localhost:8080/apis/apps/v1/namespaces/default/replicasets/my-repset \
-d '{"kind":"DeleteOptions","apiVersion":"v1","propagationPolicy":"Background"}' \
-H "Content-Type: application/json"
```

Berikut adalah sebuah contoh yang mengapus dependen di _foreground_:

```shell
kubectl proxy --port=8080
curl -X DELETE localhost:8080/apis/apps/v1/namespaces/default/replicasets/my-repset \
-d '{"kind":"DeleteOptions","apiVersion":"v1","propagationPolicy":"Foreground"}' \
-H "Content-Type: application/json"
```

Berikut adalah contoh _orphan_ yang dependen:

```shell
kubectl proxy --port=8080
curl -X DELETE localhost:8080/apis/apps/v1/namespaces/default/replicasets/my-repset \
-d '{"kind":"DeleteOptions","apiVersion":"v1","propagationPolicy":"Orphan"}' \
-H "Content-Type: application/json"
```

kubectl juga mendukung _cascading deletion_. Untuk menghapus dependen secara otomatis dengan menggunakan kubectl, Ubah nilai `--cascade` menjadi _true_. Untuk _orphan_ yang dependen, ubah nilai `--cascade` menjadi _false_. Nilai _default_ untuk `--cascade` adalah _true_.

Berikut adalah contoh yang membuat dependen ReplicaSet menjadi _orphan_:

```shell
kubectl delete replicaset my-repset --cascade=orphan
```

### Catatan tambahan untuk Deployment

Sebelum versi 1.7, ketika menggunakan _cascading delete_ dengan Deployment, kamu *harus* menggunakan `propagationPolicy: Foreground` untuk menghapus tidak hanya ReplicaSet yang telah diciptakan, tetapi juga Pod yang mereka miliki. Jika tipe _propagationPolicy_ tidak digunakan, hanya ReplicaSet yag akan dihapus, dan Pod akan menjadi _orphan_. Lihat [kubeadm/#149](https://github.com/kubernetes/kubeadm/issues/149#issuecomment-284766613) untuk informasi lebih lanjut.

## Isu yang diketahui

Ditemukan pada [#26120](https://github.com/kubernetes/kubernetes/issues/26120)



## {{% heading "whatsnext" %}}


[Dokumen Desain 1](https://git.k8s.io/community/contributors/design-proposals/api-machinery/garbage-collection.md)

[Dokumen Desain 2](https://git.k8s.io/community/contributors/design-proposals/api-machinery/synchronous-garbage-collection.md)


