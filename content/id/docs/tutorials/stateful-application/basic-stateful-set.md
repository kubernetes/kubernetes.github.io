---
title: Dasar-dasar StatefulSet
content_type: tutorial
weight: 10
---

<!-- overview -->
Tutorial ini memberikan pengantar untuk manajemen aplikasi dengan
{{< glossary_tooltip text="StatefulSet" term_id="statefulset" >}}.
Di sini dicontohkan bagaimana cara untuk membuat, menghapus, melakukan penyekalaan, 
dan memperbarui Pod dari StatefulSet.


## {{% heading "prerequisites" %}}

Sebelum memulai tutorial ini, kamu harus mengakrabkan dirimu dengan
konsep-konsep Kubernetes sebagai berikut:

* [Pod](/id/docs/concepts/workloads/pods/)
* [DNS klaster](/id/docs/concepts/services-networking/dns-pod-service/)
* [Service _headless_](/id/docs/concepts/services-networking/service/#service-headless)
* [PersistentVolume](/id/docs/concepts/storage/persistent-volumes/)
* [Penyediaan PersistentVolume](https://github.com/kubernetes/examples/tree/{{< param "githubbranch" >}}/staging/persistent-volume-provisioning/)
* [StatefulSet](/id/docs/concepts/workloads/controllers/statefulset/)
* Alat baris perintah (_command line tool_) [kubectl](/docs/reference/kubectl/kubectl/)

{{< note >}}
Tutorial ini mengasumsikan bahwa klastermu telah dikonfigurasikan untuk 
melakukan penyediaan PersistentVolume secara dinamis. Jika klastermu belum 
dikonfigurasikan seperti itu, kamu harus menyediakan dua volume masing-masing dengan 
ukuran 1 GiB sebelum memulai tutorial.
{{< /note >}}

## {{% heading "objectives" %}}

StatefulSet ditujukan untuk digunakan dengan aplikasi-aplikasi _stateful_ 
dan sistem terdistribusi. Akan tetapi, tata kelola aplikasi-aplikasi _stateful_ 
dan sistem terdistribusi pada Kubernetes merupakan topik yang luas dan kompleks. 
Untuk menunjukkan fitur-fitur dasar dari StatefulSet dan tidak mencampuradukkan 
topik sebelum dan terakhir, kamu akan menggelar sebuah aplikasi web sederhana 
menggunakan StatefulSet. 

Setelah tutorial ini, kamu akan akrab hal-hal berikut:

* Bagaimana cara membuat sebuah StatefulSet
* Bagaimana suatu StatefulSet mengelola Pod
* Bagaimana cara menghapus StatefulSet
* Bagaimana cara melakukan penyekalaan terhadap suatu StatefulSet
* Bagaimana cara memperbarui Pod dari StatefulSet

<!-- lessoncontent -->

## Membuat Sebuah StatefulSet

Mulailah dengan membuat sebuah Statefulset dengan menggunakan contoh di bawah ini.
Hal ini mirip dengan contoh yang ditunjukkan di dalam konsep 
[StatefulSet](/id/docs/concepts/workloads/controllers/statefulset/).
Contoh ini menciptakan sebuah 
[Service _headless_](/id/docs/concepts/services-networking/service/#service-headless), 
`nginx`, untuk mempublikasikan alamat IP Pod di dalam StatefulSet, `web`.

{{< codenew file="application/web/web.yaml" >}}

Unduh contoh di atas, dan simpan ke dalam berkas dengan nama `web.yaml`.

Kamu perlu menggunakan dua jendela terminal. Pada terminal yang pertama, gunakan perintah
[`kubectl get`](/docs/reference/generated/kubectl/kubectl-commands/#get) untuk mengamati
pembuatan Pod dari StatefulSet.

```shell
kubectl get pods -w -l app=nginx
```

Pada terminal yang kedua, gunakan
[`kubectl apply`](/docs/reference/generated/kubectl/kubectl-commands/#apply) untuk membuat
Service _headless_ dan StatefulSet yang didefinisikan di dalam `web.yaml`.

```shell
kubectl apply -f web.yaml
```
```
service/nginx created
statefulset.apps/web created
```

Perintah di atas menciptakan dua Pod, masing-masing menjalankan server web
[NGINX](https://www.nginx.com). Dapatkan Service `nginx`...
```shell
kubectl get service nginx
```
```
NAME      TYPE         CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
nginx     ClusterIP    None         <none>        80/TCP    12s
```
...kemudian dapatkan StatefulSet `web`, untuk memastikan keduanya berhasil dibuat:
```shell
kubectl get statefulset web
```
```
NAME      DESIRED   CURRENT   AGE
web       2         1         20s
```

### Pembuatan Pod Berurutan

Untuk StatefulSet dengan _n_ replika, ketika Pod sedang digelar, kesemuanya
akan dibuat secara berurutan, terurut dari _{0..n-1}_. Periksa keluaran dari
perintah `kubectl get` pada terminal pertama. Pada akhirnya, keluaran yang dihasilkan
akan seperti contoh di bawah ini.

```shell
kubectl get pods -w -l app=nginx
```
```
NAME      READY     STATUS    RESTARTS   AGE
web-0     0/1       Pending   0          0s
web-0     0/1       Pending   0         0s
web-0     0/1       ContainerCreating   0         0s
web-0     1/1       Running   0         19s
web-1     0/1       Pending   0         0s
web-1     0/1       Pending   0         0s
web-1     0/1       ContainerCreating   0         0s
web-1     1/1       Running   0         18s
```
Perhatikan Pod `web-1` tidak dijalankan hingga `web-0` berganti status menjadi _Running_
(lihat [Fase Pod](/id/docs/concepts/workloads/pods/pod-lifecycle/#fase-pod)) dan _Ready_
(lihat `type` di [Kondisi Pod](/id/docs/concepts/workloads/pods/pod-lifecycle/#kondisi-pod)).

## Pod pada StatefulSet

Pod pada StatefulSet memiliki satu indeks urutan unik dan satu identitas jaringan yang tetap.

### Memeriksa Indeks Urutan Pod

Dapatkan Pod dari StatefulSet:

```shell
kubectl get pods -l app=nginx
```
```
NAME      READY     STATUS    RESTARTS   AGE
web-0     1/1       Running   0          1m
web-1     1/1       Running   0          1m
```

Sebagaimana telah disebutkan di dalam konsep 
[StatefulSet](/id/docs/concepts/workloads/controllers/statefulset/),
Pod pada StatefulSet memiliki suatu identitas yang melekat (_sticky_) dan unik.
Identitas ini didasarkan pada sebuah indeks urutan yang unik yang di tetapkan 
ke masing-masing Pod oleh {{< glossary_tooltip term_id="controller" text="pengontrol">}} StatefulSet.
Nama Pod memiliki format `<nama statefulset>-<indeks urutan>`.
Karena StatefulSet `web` memiliki dua replika, maka ada dua Pod yang tercipta, `web-0` dan `web-1`.

### Menggunakan Identitas Jaringan yang Tetap

Setiap Pod memiliki nama hos yang tetep berdasarkan indeks urutannya. Gunakan perintah
[`kubectl exec`](/docs/reference/generated/kubectl/kubectl-commands/#exec) untuk menjalankan
perintah `hostname` di tiap Pod:

```shell
for i in 0 1; do kubectl exec "web-$i" -- sh -c 'hostname'; done
```
```
web-0
web-1
```

Gunakan perintah [`kubectl run`](/docs/reference/generated/kubectl/kubectl-commands/#run) untuk
menjalankan sebuah Container yang menyediakan perintah `nslookup` dari paket `dnsutils`.
Dengan menjalankan perintah `nslookup` dengan nama hos dari Pod, kamu dapat memeriksa alamat
DNS mereka di dalam klaster:

```shell
kubectl run -i --tty --image busybox:1.28 dns-test --restart=Never --rm
```
perintah itu akan memulai sebuah _shell_ baru. Pada _shell_ tersebut, jalankan:
```shell
# Jalankan ini di dalam shell Container dns-test
nslookup web-0.nginx
```
Keluarannya akan seperti:
```
Server:    10.0.0.10
Address 1: 10.0.0.10 kube-dns.kube-system.svc.cluster.local

Name:      web-0.nginx
Address 1: 10.244.1.6

nslookup web-1.nginx
Server:    10.0.0.10
Address 1: 10.0.0.10 kube-dns.kube-system.svc.cluster.local

Name:      web-1.nginx
Address 1: 10.244.2.6
```

(dan selanjutnya keluarlah dari _shell_ Container dengan menjalankan: `exit`)

CNAME dari _headless service_ mengarah ke SRV _record_ (satu untuk tiap Pod yang
Running dan Ready). SRC _record_ mengarah ke entri A _record_ yang memuat
alamat IP Pod.

Pada salah satu terminal, amati Pod dari StatefulSet:

```shell
kubectl get pod -w -l app=nginx
```
Pada terminal yang lain, gunakan perintah
[`kubectl delete`](/docs/reference/generated/kubectl/kubectl-commands/#delete) untuk menghapus
semua Pod pada StatefulSet:

```shell
kubectl delete pod -l app=nginx
```
```
pod "web-0" deleted
pod "web-1" deleted
```

Tunggu sampai StatefulSet menjalankan mereka kembali, dan untuk keduanya menjadi
Running dan Ready:

```shell
kubectl get pod -w -l app=nginx
```
```
NAME      READY     STATUS              RESTARTS   AGE
web-0     0/1       ContainerCreating   0          0s
NAME      READY     STATUS    RESTARTS   AGE
web-0     1/1       Running   0          2s
web-1     0/1       Pending   0         0s
web-1     0/1       Pending   0         0s
web-1     0/1       ContainerCreating   0         0s
web-1     1/1       Running   0         34s
```

Gunakan perintah `kubectl exec` dan `kubectl run` untuk menampilkan nama hos Pod
dan entri DNS mereka dalam klaster. Pertama-tama, tampilkan nama hos Pod:

```shell
for i in 0 1; do kubectl exec web-$i -- sh -c 'hostname'; done
```
```
web-0
web-1
```
selanjutnya, jalankan:
```
kubectl run -i --tty --image busybox:1.28 dns-test --restart=Never --rm /bin/sh
```
perintah itu akan menjalankan _shell_ baru.
Di dalam _shell_ yang baru jalankan:
```shell
# Jalankan ini di dalam shell Container dns-test
nslookup web-0.nginx
```
Keluarannya akan seperti:
```
Server:    10.0.0.10
Address 1: 10.0.0.10 kube-dns.kube-system.svc.cluster.local

Name:      web-0.nginx
Address 1: 10.244.1.7

nslookup web-1.nginx
Server:    10.0.0.10
Address 1: 10.0.0.10 kube-dns.kube-system.svc.cluster.local

Name:      web-1.nginx
Address 1: 10.244.2.8
```

(dan selanjutnya keluarlah dari _shell_ Container dengan menjalankan: `exit`)

Urutan, nama hos, SRV _record_, dan nama A _record_ dari Pod tidak berubah,
akan tetapi alamat IP yang terkait dengan Pod bisa jadi mengalami perubahan. Pada klaster
yang digunakan dalam tutorial ini terjadi perubahan. Karena itulah mengapa sangat penting
untuk menghindari pengaturan terhadap aplikasi lain yang terhubung ke Pod di dalam
StatefulSet menggunakan alamat IP.

Jika kamu ingin mencari dan terhubung dengan anggota aktif dari StatefulSet, kamu
perlu melakukan kueri CNAME dari Service _headless_ (`nginx.default.svc.cluster.local`).
SRV _record_ yang terkait dengan CNAME hanya akan memuat Pod dari StatefulSet yang
Running dan Ready.

Jika aplikasimu telah menerapkan logika koneksi yang menguji keaktifan
(_liveness_) dan kesiapan (_readiness_), kamu dapat menggunakan SRV _record_ dari Pod (
`web-0.nginx.default.svc.cluster.local`,
`web-1.nginx.default.svc.cluster.local`), karena mereka tidak akan berubah, dan
aplikasimu akan bisa menemukan alamat-alamat Pod ketika mereka mengalami peralihan
ke Running dan Ready.

### Menulis ke Penyimpanan Tetap

Dapatkan PersistentVolumeClaim untuk `web-0` dan `web-1`:

```shell
kubectl get pvc -l app=nginx
```
Keluarannya akan seperti:
```
NAME        STATUS    VOLUME                                     CAPACITY   ACCESSMODES   AGE
www-web-0   Bound     pvc-15c268c7-b507-11e6-932f-42010a800002   1Gi        RWO           48s
www-web-1   Bound     pvc-15c79307-b507-11e6-932f-42010a800002   1Gi        RWO           48s
```

Pengontrol StatefulSet membuat dua
{{< glossary_tooltip text="PersistentVolumeClaim" term_id="persistent-volume-claim" >}}
yang terikat ke dua
{{< glossary_tooltip text="PersistentVolume" term_id="persistent-volume" >}}.

Karena klaster yang digunakan dalam tutorial ini dikonfigurasi untuk melakukan penyediaan
PersistentVolume secara dinamis, maka PersistentVolume dibuat dan terikat secara otomatis.

Server web NGINX, secara bawaan, menyajikan berkas indeks dari
`/usr/share/nginx/html/index.html`. _Field_ `volumeMounts` pada `spec` StatefulSet
memastikan direktori `/usr/share/nginx/html` didukung oleh sebuah PersistentVolume.

Tulis nama hos Pod ke dalam berkas `index.html` mereka masing-masing dan periksa
apakah server web NGINX menyajikan nama hos tersebut:

```shell
for i in 0 1; do kubectl exec "web-$i" -- sh -c 'echo "$(hostname)" > /usr/share/nginx/html/index.html'; done

for i in 0 1; do kubectl exec -i -t "web-$i" -- curl http://localhost/; done
```
```
web-0
web-1
```

{{< note >}}
Jika kamu melihat respon **403 Forbidden** untuk perintah curl di atas,
kamu perlu untuk memperbaiki izin (_permission_) dari direktori yang dipasang
oleh `volumeMounts` (disebabkan oleh sebuah
[_bug_ ketika menggunakan volume hostPath](https://github.com/kubernetes/kubernetes/issues/2630)),
dengan menjalankan:

`for i in 0 1; do kubectl exec web-$i -- chmod 755 /usr/share/nginx/html; done`

sebelum mencoba kembali perintah `curl` di atas.
{{< /note >}}

Di salah satu terminal, amati Pod dari StatefulSet:

```shell
kubectl get pod -w -l app=nginx
```

Di terminal yang lain, hapus semua Pod dari StatefulSet:

```shell
kubectl delete pod -l app=nginx
```
```
pod "web-0" deleted
pod "web-1" deleted
```
Periksa keluaran dari perintah `kubectl get` pada terminal yang pertama dan tunggu
semua Pod berubah menjadi Running dan Ready.

```shell
kubectl get pod -w -l app=nginx
```
```
NAME      READY     STATUS              RESTARTS   AGE
web-0     0/1       ContainerCreating   0          0s
NAME      READY     STATUS    RESTARTS   AGE
web-0     1/1       Running   0          2s
web-1     0/1       Pending   0         0s
web-1     0/1       Pending   0         0s
web-1     0/1       ContainerCreating   0         0s
web-1     1/1       Running   0         34s
```

Periksa apakah server web masih terus menyajikan nama hosnya:

```
for i in 0 1; do kubectl exec -i -t "web-$i" -- curl http://localhost/; done
```
```
web-0
web-1
```

Walaupun `web-0` dan `web-1` telah dijadwalkan ulang, mereka masih menyajikan
nama hos masing-masing karena PersistentVolume yang terkait dengan 
PersistentVolumeClaim-nya dipasang kembali (_remounted_) ke setiap `volumeMounts`.
Di Node manapun `web-0` dan `web-1` dijadwalkan, PersistentVolume-nya akan
dipasangkan ke titik pasang (_mount point_) yang sesuai.

## Penyekalaan StatefulSet

Melakukan penyekalaan pada StatefulSet berarti meningkatkan atau mengurangi jumlah
replika. Hal ini dicapai dengan memperbarui _field_ `replicas`. Kamu dapat menggunakan
[`kubectl scale`](/docs/reference/generated/kubectl/kubectl-commands/#scale) atau
[`kubectl patch`](/docs/reference/generated/kubectl/kubectl-commands/#patch) untuk
melakukan penyekalaan terhadap StatefulSet.

### Penyekalaan Naik

Pada salah satu jendela terminal, amati Pod pada StatefulSet:

```shell
kubectl get pods -w -l app=nginx
```

Di jendela terminal yang lain gunakan perintah `kubectl scale` untuk melakukan
penyekalaan jumlah replika menjadi 5:

```shell
kubectl scale sts web --replicas=5
```
```
statefulset.apps/web scaled
```

Periksa keluaran dari perintah `kubectl get` pada terminal pertama dan tunggu
tambahan tiga Pod yang baru berubah menjadi Running dan Ready.

```shell
kubectl get pods -w -l app=nginx
```
```
NAME      READY     STATUS    RESTARTS   AGE
web-0     1/1       Running   0          2h
web-1     1/1       Running   0          2h
NAME      READY     STATUS    RESTARTS   AGE
web-2     0/1       Pending   0          0s
web-2     0/1       Pending   0         0s
web-2     0/1       ContainerCreating   0         0s
web-2     1/1       Running   0         19s
web-3     0/1       Pending   0         0s
web-3     0/1       Pending   0         0s
web-3     0/1       ContainerCreating   0         0s
web-3     1/1       Running   0         18s
web-4     0/1       Pending   0         0s
web-4     0/1       Pending   0         0s
web-4     0/1       ContainerCreating   0         0s
web-4     1/1       Running   0         19s
```

Pengontrol StatefulSet telah melakukan penyekalaan terhadap jumlah replika.
Sama seperti [pembuatan StatefulSet](#pembuatan-pod-dengan-urutan), pengontrol
StatefulSet membuat tiap Pod berurutan sesuai dengan indeks urutan masing-masing
dan menunggu setiap Pod yang dibuat sebelumnya menjadi Running dan Ready sebelum
menjalankan Pod berikutnya.

### Penyekalaan Turun

Di salah satu terminal, amati Pod pada StatefulSet:

```shell
kubectl get pods -w -l app=nginx
```

Di terminal yang lain, gunakan perintah `kubectl patch` untuk melakukan penyekalaan
StatefulSet turun menjadi tiga replika:

```shell
kubectl patch sts web -p '{"spec":{"replicas":3}}'
```
```
statefulset.apps/web patched
```

Tunggu hingga `web-4` dan `web-3` berubah menjadi Terminating.

```shell
kubectl get pods -w -l app=nginx
```
```
NAME      READY     STATUS              RESTARTS   AGE
web-0     1/1       Running             0          3h
web-1     1/1       Running             0          3h
web-2     1/1       Running             0          55s
web-3     1/1       Running             0          36s
web-4     0/1       ContainerCreating   0          18s
NAME      READY     STATUS    RESTARTS   AGE
web-4     1/1       Running   0          19s
web-4     1/1       Terminating   0         24s
web-4     1/1       Terminating   0         24s
web-3     1/1       Terminating   0         42s
web-3     1/1       Terminating   0         42s
```

### Penghentian Pod Berurutan

Pengontrol menghapus satu Pod dalam satu waktu, dengan urutan terbalik dari indeks
urutannya, dan setiap Pod akan ditunggu sampai benar-benar mati terlebih dahulu
sebelum menghapus Pod berikutnya.

Dapatkan PersistentVolumeClaim dari StatefulSet:

```shell
kubectl get pvc -l app=nginx
```
```
NAME        STATUS    VOLUME                                     CAPACITY   ACCESSMODES   AGE
www-web-0   Bound     pvc-15c268c7-b507-11e6-932f-42010a800002   1Gi        RWO           13h
www-web-1   Bound     pvc-15c79307-b507-11e6-932f-42010a800002   1Gi        RWO           13h
www-web-2   Bound     pvc-e1125b27-b508-11e6-932f-42010a800002   1Gi        RWO           13h
www-web-3   Bound     pvc-e1176df6-b508-11e6-932f-42010a800002   1Gi        RWO           13h
www-web-4   Bound     pvc-e11bb5f8-b508-11e6-932f-42010a800002   1Gi        RWO           13h

```

Di sana masih ada lima PersistentVolumeClaim dan lima PersistentVolume.
Ketika mengeksplorasi [penyimpanan tetap](#menulis-ke-penyimpanan-tetap) pada Pod,
kita dapat melihat bahwa PersistentVolume yang terpasang pada Pod dari suatu StatefulSet 
tidak terhapus ketika Pod-nya dihapus. Hal ini tetap berlaku ketika penghapusan Pod
terjadi karena penyekalaan turun pada suatu StatefulSet.

## Memperbarui StatefulSet

Di Kubernetes 1.7 dan yang lebih baru, pengontrol StatefulSet mendukung
pembaruan otomatis. Strategi yang digunakan ditentukan oleh _field_ 
`spec.updateStrategy` dari objek API StatefulSet. Fitur ini dapat digunakan untuk
memperbarui _image_ Container, permintaan sumber daya dan/atau pembatasan, label,
dan anotasi Pod dalam suatu StatefulSet. Ada dua strategi pembaruan yang berlaku,
`RollingUpdate` dan `OnDelete`.

Pembaruan dengan `RollingUpdate` adalah strategi bawaan untuk StatefulSet.

### Pembaruan Bertahap (RollingUpdate)

Pembaruan dengan strategi `RollingUpdate` akan memperbarui semua Pod di dalam
StatefulSet dalam urutan indeks terbalik, dengan tetap memperhatikan 
jaminan dari StatefulSet.

Lakukan _patch_ pada StatefulSet `web` dengan menerapkan `RollingUpdate`:

```shell
kubectl patch statefulset web -p '{"spec":{"updateStrategy":{"type":"RollingUpdate"}}}'
```
```
statefulset.apps/web patched
```

Pada salah satu jendela terminal, _patch_ StatefulSet `web` untuk mengubah 
_image_ Container lagi:

```shell
kubectl patch statefulset web --type='json' -p='[{"op": "replace", "path": "/spec/template/spec/containers/0/image", "value":"gcr.io/google_containers/nginx-slim:0.8"}]'
```
```
statefulset.apps/web patched
```

Pada terminal yang lain, amati Pod pada StatefulSet:

```shell
kubectl get pod -l app=nginx -w
```
Keluarannya akan seperti:
```
NAME      READY     STATUS    RESTARTS   AGE
web-0     1/1       Running   0          7m
web-1     1/1       Running   0          7m
web-2     1/1       Running   0          8m
web-2     1/1       Terminating   0         8m
web-2     1/1       Terminating   0         8m
web-2     0/1       Terminating   0         8m
web-2     0/1       Terminating   0         8m
web-2     0/1       Terminating   0         8m
web-2     0/1       Terminating   0         8m
web-2     0/1       Pending   0         0s
web-2     0/1       Pending   0         0s
web-2     0/1       ContainerCreating   0         0s
web-2     1/1       Running   0         19s
web-1     1/1       Terminating   0         8m
web-1     0/1       Terminating   0         8m
web-1     0/1       Terminating   0         8m
web-1     0/1       Terminating   0         8m
web-1     0/1       Pending   0         0s
web-1     0/1       Pending   0         0s
web-1     0/1       ContainerCreating   0         0s
web-1     1/1       Running   0         6s
web-0     1/1       Terminating   0         7m
web-0     1/1       Terminating   0         7m
web-0     0/1       Terminating   0         7m
web-0     0/1       Terminating   0         7m
web-0     0/1       Terminating   0         7m
web-0     0/1       Terminating   0         7m
web-0     0/1       Pending   0         0s
web-0     0/1       Pending   0         0s
web-0     0/1       ContainerCreating   0         0s
web-0     1/1       Running   0         10s
```

Pod dalam StatefulSet diperbarui dengan urutan indeks terbalik. Pengontrol
StatefulSet mengakhiri setiap Pod, dan menunggunya beralih menjadi Running dan Ready
sebelum melakukan pembaruan ke Pod berikutnya. Sebagai catatan, walaupun pengontrol
StatefulSet tidak akan melanjutkan pembaruan terhadap Pod berikutnya hingga penggantinya
Running dan Ready, pengontrol akan memulihkan Pod apa pun yang mengalami kegagalan selama
proses pembaruan berlangsung.

Pod yang telah menerima pembaruan akan dipulihkan ke versi yang diperbarui, sedangkan
Pod yang belum menerima pembaruan akan dipulihkan ke versi sebelumnya. Dengan cara inilah
pengontrol mencoba untuk terus mempertahankan kesehatan aplikasi dan
pembaruan tetap konsisten ditengah adanya kemungkinan kegagalan intermiten.

Dapatkan Pod untuk melihat _image_ Container-nya:

```shell
for p in 0 1 2; do kubectl get pod "web-$p" --template '{{range $i, $c := .spec.containers}}{{$c.image}}{{end}}'; echo; done
```
```
k8s.gcr.io/nginx-slim:0.8
k8s.gcr.io/nginx-slim:0.8
k8s.gcr.io/nginx-slim:0.8

```

Semua Pod pada StatefulSet saat ini sedang menjalankan _image_ Container sebelumnya.

{{< note >}}
Kamu juga bisa menggunakan perintah `kubectl rollout status sts/<name>`
untuk menampilkan status pembaruan bertahap terhadap sebuah StatefulSet
{{< /note >}}

#### Pembaruan dengan _Staging_

Kamu dapat melakukan _staging_ terhadap suatu pembaruan StatefulSet dengan
menggunakan parameter `partition` dari strategi pembaruan `RollingUpdate`. Suatu
pembaruan yang di-_staging_ akan akan mempertahankan semua Pod dalam StatefulSet
tersebut pada versi yang digunakan saat ini sembari mengizinkan terjadinya
perubahan pada `.spec.template` dari StatefulSet.

Lakukan _patch_ terhadap StatefulSet `web` untuk menambahkan partisi pada
_field_ `updateStrategy`:

```shell
kubectl patch statefulset web -p '{"spec":{"updateStrategy":{"type":"RollingUpdate","rollingUpdate":{"partition":3}}}}'
```
```
statefulset.apps/web patched
```

Lakukan _patch_ terhadap StatefulSet lagi, untuk mengubah _image_ Container:

```shell
kubectl patch statefulset web --type='json' -p='[{"op": "replace", "path": "/spec/template/spec/containers/0/image", "value":"k8s.gcr.io/nginx-slim:0.7"}]'
```
```
statefulset.apps/web patched
```

Hapus sebuah Pod dari StatefulSet:

```shell
kubectl delete pod web-2
```
```
pod "web-2" deleted
```

Tunggu hingga Pod menjadi Running dan Ready.

```shell
kubectl get pod -l app=nginx -w
```
```
NAME      READY     STATUS              RESTARTS   AGE
web-0     1/1       Running             0          4m
web-1     1/1       Running             0          4m
web-2     0/1       ContainerCreating   0          11s
web-2     1/1       Running   0         18s
```

Dapatkan _image_ Container Pod:

```shell
kubectl get pod web-2 --template '{{range $i, $c := .spec.containers}}{{$c.image}}{{end}}'
```
```
k8s.gcr.io/nginx-slim:0.8
```

Perhatikan, walaupun strategi pembaruan yang digunakan adalah `RollingUpdate`,
StatefulSet mengembalikan Pod dengan Container-nya yang semula. Hal ini karena
urutan Pod kurang dari nilai `partition` yang ditetapkan pada `updateStrategy`.

#### Meluncurkan _Canary_

Kamu dapat meluncurkan _canary_ untuk mencoba suatu perubahan dengan mengurangi
`partition` yang kamu tentukan sebelumnya di [atas](#pembaruan-dengan-staging).

Lakukan _patch_ terhadap StatefulSet untuk mengurangi jumlah partisi:

```shell
kubectl patch statefulset web -p '{"spec":{"updateStrategy":{"type":"RollingUpdate","rollingUpdate":{"partition":2}}}}'
```
```
statefulset.apps/web patched
```

Tunggu hingga `web-2` menjadi Running dan Ready.

```shell
kubectl get pod -l app=nginx -w
```
```
NAME      READY     STATUS              RESTARTS   AGE
web-0     1/1       Running             0          4m
web-1     1/1       Running             0          4m
web-2     0/1       ContainerCreating   0          11s
web-2     1/1       Running   0         18s
```

Dapatkan _image_ Container Pod:

```shell
kubectl get pod web-2 --template '{{range $i, $c := .spec.containers}}{{$c.image}}{{end}}'
```
```
k8s.gcr.io/nginx-slim:0.7

```

Ketika kamu mengubah `partition`, pengontrol StatefulSet secara otomatis memperbarui Pod
`web-2` karena urutan dari Pod tersebut lebih besar dari atau sama dengan
nilai `partition`.

Hapus Pod `web-1`:

```shell
kubectl delete pod web-1
```
```
pod "web-1" deleted
```

Tunggu sampai Pod `web-1` menjadi Running dan Ready.

```shell
kubectl get pod -l app=nginx -w
```
Keluarannya akan seperti:
```
NAME      READY     STATUS        RESTARTS   AGE
web-0     1/1       Running       0          6m
web-1     0/1       Terminating   0          6m
web-2     1/1       Running       0          2m
web-1     0/1       Terminating   0         6m
web-1     0/1       Terminating   0         6m
web-1     0/1       Terminating   0         6m
web-1     0/1       Pending   0         0s
web-1     0/1       Pending   0         0s
web-1     0/1       ContainerCreating   0         0s
web-1     1/1       Running   0         18s
```

Dapatkan _image_ Container dari Pod `web-1`:

```shell
kubectl get pod web-1 --template '{{range $i, $c := .spec.containers}}{{$c.image}}{{end}}'
```
```
k8s.gcr.io/nginx-slim:0.8
```

`web-1` dikembalikan ke konfigurasinya yang semula karena urutan Pod lebih kecil
dari partisi. Ketika partisi ditentukan, semua Pod dengan urutan yang lebih besar
dari atau sama dengan jumlah partisi akan diperbarui ketika `.spec.template` dari
StatefulSet diubah. Jika suatu Pod yang memiliki urutan lebih kecil dari partisi
dihapus atau diakhiri, Pod tersebut akan dikembalikan ke konfigurasinya yang semula.

#### Peluncuran Bertahap

Kamu dapat melakukan peluncuran bertahap (misalkan peluncuran: linier, geometris, atau eksponensial)
dengan menggunakan pembaruan bertahap yang terpartisi dengan cara yang serupa
ketika kamu meluncurkan [_canary_](#meluncurkan-canary). Untuk melakukan peluncuran bertahap,
atur `partition` ke urutan di mana kamu menginginkan pengontrol untuk melakukan 
pause terhadap pembaruan.

Saat ini partisi sedang di atur menjadi `2`. Ganti partisi menjadi `0`:

```shell
kubectl patch statefulset web -p '{"spec":{"updateStrategy":{"type":"RollingUpdate","rollingUpdate":{"partition":0}}}}'
```
```
statefulset.apps/web patched
```

Tunggu semua Pod pada StatefulSet menjadi Running dan Ready.

```shell
kubectl get pod -l app=nginx -w
```
Keluarannya akan seperti:
```
NAME      READY     STATUS              RESTARTS   AGE
web-0     1/1       Running             0          3m
web-1     0/1       ContainerCreating   0          11s
web-2     1/1       Running             0          2m
web-1     1/1       Running   0         18s
web-0     1/1       Terminating   0         3m
web-0     1/1       Terminating   0         3m
web-0     0/1       Terminating   0         3m
web-0     0/1       Terminating   0         3m
web-0     0/1       Terminating   0         3m
web-0     0/1       Terminating   0         3m
web-0     0/1       Pending   0         0s
web-0     0/1       Pending   0         0s
web-0     0/1       ContainerCreating   0         0s
web-0     1/1       Running   0         3s
```

Dapatkan detail _image_ Container dari Pod pada StatefulSet:

```shell
for p in 0 1 2; do kubectl get pod "web-$p" --template '{{range $i, $c := .spec.containers}}{{$c.image}}{{end}}'; echo; done
```
```
k8s.gcr.io/nginx-slim:0.7
k8s.gcr.io/nginx-slim:0.7
k8s.gcr.io/nginx-slim:0.7
```

Dengan mengubah nilai `partition` menjadi `0`, kamu mengizinkan StatefulSet
untuk melanjutkan proses pembaruan.

### Pembaruan OnDelete

Strategi pembaruan `OnDelete` menerapkan mekanisme lama (versi 1.6 dan sebelumnya).
Ketika kamu memilih strategi pembaruan ini, pengontrol StatefulSet tidak akan secara
otomatis melakukan pembaruan terhadap Pod ketika suatu perubahan terjadi pada _field_
`.spec.template` pada StatefulSet. Strategi ini dapat dipilih dengan mengatur
`.spec.template.updateStrategy.type` menjadi `OnDelete`.

## Menghapus StatefulSet

StatefulSet mendukung penghapusan tidak berjenjang (_non-cascading_) dan berjenjang (_cascading_).
Dalam penghapusan tidak berjenjang (_non-cascading delete_), Pod pada StatefulSet 
tidak dihapus ketika StatefulSet terhapus. Pada penghapusan berjenjang (Cascading Delete),
StatefulSet bersama Pod-nya dihapus semua.

### Penghapusan Tidak Berjenjang (_Non-Cascading_)

Pada salah satu jendela terminal, amati Pod pada StatefulSet.

```
kubectl get pods -w -l app=nginx
```

Gunakan perintah [`kubectl delete`](/docs/reference/generated/kubectl/kubectl-commands/#delete)
untuk menghapus StatefulSet. Pastikan kamu menambahkan parameter `--cascade=orphan` ke
perintah tersebut. Parameter ini memberitahukan Kubernetes untuk hanya menghapus StatefulSet
dan agar tidak menghapus Pod yang ada padanya.

```shell
kubectl delete statefulset web --cascade=orphan
```
```
statefulset.apps "web" deleted
```

Dapatkan Pod untuk melihat statusnya masing-masing:

```shell
kubectl get pods -l app=nginx
```
```
NAME      READY     STATUS    RESTARTS   AGE
web-0     1/1       Running   0          6m
web-1     1/1       Running   0          7m
web-2     1/1       Running   0          5m
```

Walaupun `web` telah dihapus, semua Pod masih Running dan Ready.
Hapus `web-0`:

```shell
kubectl delete pod web-0
```
```
pod "web-0" deleted
```

Dapatkan Pod dari StatefulSet:

```shell
kubectl get pods -l app=nginx
```
```
NAME      READY     STATUS    RESTARTS   AGE
web-1     1/1       Running   0          10m
web-2     1/1       Running   0          7m
```

Karena StatefulSet `web` telah dihapus, maka `web-0` tidak dijalankan lagi.

Di salah satu terminal, amati Pod pada StatefulSet.

```shell
kubectl get pods -w -l app=nginx
```

Pada terminal yang lain, buat kembali StatefulSet. Perhatikan, terkecuali
jika kamu telah menghapus Service `ngingx` (yang seharusnya belum kamu lakukan), 
kamu akan melihat sebuah galat yang mengindikasikan bahwa Service tersebut sudah ada.

```shell
kubectl apply -f web.yaml
```
```
statefulset.apps/web created
service/nginx unchanged
```

Abaikan galat yang terjadi. Hal itu hanya menunjukkan bahwa suatu upaya telah dilakukan
untuk membuat Service _headless_ `nginx` walaupun Service tersebut sebenarnya sudah ada.

Perhatikan keluaran dari perintah `kubectl get` yang dijalankan pada terminal
yang pertama.

```shell
kubectl get pods -w -l app=nginx
```
```
NAME      READY     STATUS    RESTARTS   AGE
web-1     1/1       Running   0          16m
web-2     1/1       Running   0          2m
NAME      READY     STATUS    RESTARTS   AGE
web-0     0/1       Pending   0          0s
web-0     0/1       Pending   0         0s
web-0     0/1       ContainerCreating   0         0s
web-0     1/1       Running   0         18s
web-2     1/1       Terminating   0         3m
web-2     0/1       Terminating   0         3m
web-2     0/1       Terminating   0         3m
web-2     0/1       Terminating   0         3m
```

Ketika StatefulSet `web` dibuat ulang, yang dijalankan pertama kali adalah `web-0`.
Karena `web-1` telah menjadi Running dan Ready, ketika `web-0` berubah menjadi
Running dan Ready, `web-0` mengadopsi Pod tersebut. Karena kamu membuat ulang
StatefulSet dengan `replicas` sama dengan 2, ketika `web-0` selesai dibuat ulang, dan
ketika `web-1` telah ditetapkan menjadi Running dan Ready, maka `web-2` diakhiri.

Mari kita lihat kembali konten dari berkas `index.html` yang disajikan oleh server
web Pod:

```shell
for i in 0 1; do kubectl exec -i -t "web-$i" -- curl http://localhost/; done
```
```
web-0
web-1
```

Walaupun kamu sebelumnya pernah menghapus StatefulSet dan Pod `web-0`, server web
masih terus menyajikan nama hos sebelumnya yang dimasukkan ke dalam berkas
`index.html`. Hal ini terjadi karena StatefulSet tidak menghapus PersistentVolume
yang terkait dengan Pod. Ketika kamu membuat ulang StatefulSet dan menjalankan
kembali `web-0`, PersistentVolume yang digunakan sebelumnya akan dipasang kembali.

### Penghapusan Berjenjang (Cascading)

Pada salah satu jendela terminal, amati Pod pada StatefulSet.

```shell
kubectl get pods -w -l app=nginx
```

Pada terminal yang lain, hapus StatefulSet lagi. Kali ini, hilangkan parameter
`--cascade=orphan`.

```shell
kubectl delete statefulset web
```
```
statefulset.apps "web" deleted
```
Perhatikan keluaran dari perintah `kubectl get` yang dijalankan di terminal
yang pertama, dan tunggu semua status Pod berubah menjadi Terminating.

```shell
kubectl get pods -w -l app=nginx
```
```
NAME      READY     STATUS    RESTARTS   AGE
web-0     1/1       Running   0          11m
web-1     1/1       Running   0          27m
NAME      READY     STATUS        RESTARTS   AGE
web-0     1/1       Terminating   0          12m
web-1     1/1       Terminating   0         29m
web-0     0/1       Terminating   0         12m
web-0     0/1       Terminating   0         12m
web-0     0/1       Terminating   0         12m
web-1     0/1       Terminating   0         29m
web-1     0/1       Terminating   0         29m
web-1     0/1       Terminating   0         29m

```

Seperti yang telah kamu saksikan pada bagian [Penyekalaan Turun](#penyekalaan-turun),
Pod diakhiri satu demi satu dengan urutan terbalik dari indeks urutan mereka. Sebelum
mengakhiri suatu Pod, pengontrol StatefulSet menunggu Pod pengganti hingga benar-benar
berakhir.

{{< note >}}
Walaupun penghapusan berjenjang menghapus suatu StatefulSet bersama Pod yang ada,
penghapusan ini tidak menghapus Service _headless_ yang terkait dengan StatefulSet.
Kamu hapus menghapus Service `nginx` secara manual.
{{< /note >}}


```shell
kubectl delete service nginx
```
```
service "nginx" deleted
```

Buat ulang StatefulSet dan Service _headless_ sekali lagi:

```shell
kubectl apply -f web.yaml
```
```
service/nginx created
statefulset.apps/web created
```

Saat semua Pod StatefulSet mengalami transisi ke Running dan Ready, dapatkan
konten dari berkas `index.html` masing-masing:

```shell
for i in 0 1; do kubectl exec -i -t "web-$i" -- curl http://localhost/; done
```
```
web-0
web-1
```

Walaupun kamu telah menghapus StatefulSet dan semua Pod di dalamnya, Pod dibuat
lagi dengan PersistentVolume yang sama terpasang, dan `web-0` dan `web-1` masih
menyajikan nama hos masing-masing.

Akhirnya, hapus Service `nginx`...

```shell
kubectl delete service nginx
```
```
service "nginx" deleted
```
...dan StatefulSet `web`:
```shell
kubectl delete statefulset web
```
```
statefulset "web" deleted
```

## Kebijakan Manajemen Pod

Untuk beberapa sistem terdistribusi, jaminan pengurutan StatefulSet tidak
penting dan/atau tidak diharapkan. Sistem-sistem tersebut hanya membutuhkan
keunikan dan identitas. Untuk mengatasi ini, pada Kubernetes 1.7, kami
memperkenalkan `.spec.podManagementPolicy` pada objek API StatefulSet.

### Manajemen Pod OrderedReady

Manajemen Pod `OrderedReady` adalah bawaan dari StatefulSet. Manajemen
dengan cara ini memberitahukan pengontrol StatefulSet untuk menghormati
jaminan pengurutan yang sudah ditunjukkan sebelumnya.

### Manajemen Pod Parallel

Manajemen Pod `Parallel` memberitahukan pengontrol StatefulSet untuk
menjalankan atau mengakhiri semua Pod secara bersamaan (paralel), dan tidak menunggu
suatu Pod menjadi Running dan Ready atau benar-benar berakhir sebelum menjalankan atau 
mengakhiri Pod yang lain.

{{< codenew file="application/web/web-parallel.yaml" >}}

Unduh contoh di atas, dan simpan ke sebuah berkas dengan nama `web-parallel.yaml`.

Manifes ini serupa dengan yang telah kamu unduh sebelumnya kecuali `.spec.podManagementPolicy`
dari StatefulSet `web` diatur ke `Parallel`.

Di salah satu terminal, amati Pod pada StatefulSet.

```shell
kubectl get pod -l app=nginx -w
```

Pada terminal yang lain, buat StatefulSet dan Service dari manifes tadi:

```shell
kubectl apply -f web-parallel.yaml
```
```
service/nginx created
statefulset.apps/web created
```

Perhatikan keluaran dari perintah `kubectl get` yang kamu jalankan pada
terminal yang pertama.

```shell
kubectl get pod -l app=nginx -w
```
```
NAME      READY     STATUS    RESTARTS   AGE
web-0     0/1       Pending   0          0s
web-0     0/1       Pending   0         0s
web-1     0/1       Pending   0         0s
web-1     0/1       Pending   0         0s
web-0     0/1       ContainerCreating   0         0s
web-1     0/1       ContainerCreating   0         0s
web-0     1/1       Running   0         10s
web-1     1/1       Running   0         10s
```

Pengontrol StatefulSet menjalankan `web-0` dan `web-` berbarengan.

Biarkan terminal kedua tetap terbuka, kemudian, di jendela terminal
yang lain lakukan penyekalaan terhadap StatefulSet:

```shell
kubectl scale statefulset/web --replicas=4
```
```
statefulset.apps/web scaled
```

Perhatikan keluaran terminal di mana perintah `kubectl get` dijalankan.

```
web-3     0/1       Pending   0         0s
web-3     0/1       Pending   0         0s
web-3     0/1       Pending   0         7s
web-3     0/1       ContainerCreating   0         7s
web-2     1/1       Running   0         10s
web-3     1/1       Running   0         26s
```

StatefulSet menjalankan dua Pod baru dan tidak menunggu Pod pertama
menjadi Running dan Ready terlebih dahulu sebelum menjalankan Pod
yang kedua.

## {{% heading "cleanup" %}}

Kamu harus membuka dua terminal yang siap untuk menjalankan perintah `kubectl`
sebagai bagian dari pembersihan.

```shell
kubectl delete sts web
# sts adalah singkatan dari statefulset
```

Kamu dapat mengamati `kubectl get` untuk melihat semua Pod yang sedang dihapus.
```shell
kubectl get pod -l app=nginx -w
```
```
web-3     1/1       Terminating   0         9m
web-2     1/1       Terminating   0         9m
web-3     1/1       Terminating   0         9m
web-2     1/1       Terminating   0         9m
web-1     1/1       Terminating   0         44m
web-0     1/1       Terminating   0         44m
web-0     0/1       Terminating   0         44m
web-3     0/1       Terminating   0         9m
web-2     0/1       Terminating   0         9m
web-1     0/1       Terminating   0         44m
web-0     0/1       Terminating   0         44m
web-2     0/1       Terminating   0         9m
web-2     0/1       Terminating   0         9m
web-2     0/1       Terminating   0         9m
web-1     0/1       Terminating   0         44m
web-1     0/1       Terminating   0         44m
web-1     0/1       Terminating   0         44m
web-0     0/1       Terminating   0         44m
web-0     0/1       Terminating   0         44m
web-0     0/1       Terminating   0         44m
web-3     0/1       Terminating   0         9m
web-3     0/1       Terminating   0         9m
web-3     0/1       Terminating   0         9m
```

Selama penghapusan, StatefulSet menghapus semua Pod secara serentak; tidak menghentikan
Pod berdasarkan urutan indeksnya terlebih dahulu sebelum menghapus Pod tersebut.

Tutup terminal di mana perintah `kubectl get` dijalankan dan hapus Service `nginx`:

```shell
kubectl delete svc nginx
```

{{< note >}}
Kamu juga perlu menghapus media penyimpanan persisten untuk PersistentVolume
yang digunakan dalam tutorial ini.

Ikuti langkah-langkah yang dibutuhkan, berdasarkan lingkungan yang kamu gunakan,
konfigurasi penyimpanan, dan metode penyediaannya, untuk memastikan semua
penyimpanan dapat dimanfaatkan lagi.
{{< /note >}}
