---
title: DaemonSet
content_type: concept
weight: 50
---

<!-- overview -->

DaemonSet memastikan semua atau sebagian Node memiliki salinan sebuah Pod.
Ketika Node baru ditambahkan ke klaster, Pod ditambahkan ke Node tersebut.
Ketika Node dihapus dari klaster, Pod akan dibersihkan oleh _garbage collector_.
Menghapus DaemonSet akan menghapus semua Pod yang ia buat.

Beberapa penggunaan umum DaemonSet, yaitu:

- menjalankan _daemon_ penyimpanan di klaster, seperti `glusterd`, `ceph`, di
  setiap Node.
- menjalankan _daemon_ pengumpulan log di semua Node, seperti `fluentd` atau
  `logstash`.
- menjalankan _daemon_ pemantauan Node di setiap Node, seperti [Prometheus Node Exporter](https://github.com/prometheus/node_exporter), [Flowmill](https://github.com/Flowmill/flowmill-k8s/), [Sysdig Agent](https://docs.sysdig.com), `collectd`, [Dynatrace OneAgent](https://www.dynatrace.com/technologies/kubernetes-monitoring/), [AppDynamics Agent](https://docs.appdynamics.com/display/CLOUD/Container+Visibility+with+Kubernetes), [Datadog agent](https://docs.datadoghq.com/agent/kubernetes/daemonset_setup/), [New Relic agent](https://docs.newrelic.com/docs/integrations/kubernetes-integration/installation/kubernetes-installation-configuration), Ganglia `gmond` atau [Instana Agent](https://www.instana.com/supported-integrations/kubernetes-monitoring/).

Dalam kasus sederhana, satu DaemonSet, mencakup semua Node, akan digunakan untuk
setiap jenis _daemon_. Pengaturan yang lebih rumit bisa saja menggunakan lebih
dari satu DaemonSet untuk satu jenis _daemon_, tapi dengan _flag_ dan/atau
permintaan cpu/memori yang berbeda untuk jenis _hardware_ yang berbeda.




<!-- body -->

## Menulis Spek DaemonSet

### Buat DaemonSet

Kamu bisa definisikan DaemonSet dalam berkas YAML. Contohnya, berkas
`daemonset.yaml` di bawah mendefinisikan DaemonSet yang menjalankan _image_ Docker
fluentd-elasticsearch:

{{< codenew file="controllers/daemonset.yaml" >}}

* Buat DaemonSet berdasarkan berkas YAML:
```
kubectl apply -f https://k8s.io/examples/controllers/daemonset.yaml
```

### _Field_ Wajib

Seperti semua konfigurasi Kubernetes lainnya, DaemonSet membutuhkan _field_
`apiVersion`, `kind`, dan `metadata`.  Untuk informasi umum tentang berkas konfigurasi, lihat dokumen [men-_deploy_ aplikasi](/docs/user-guide/deploying-applications/),
[pengaturan kontainer](/docs/tasks/), dan [pengelolaan objek dengan kubectl](/id/docs/concepts/overview/working-with-objects/object-management/).

DaemonSet juga membutuhkan bagian [`.spec`](https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status).

### Templat Pod

`.spec.template` adalah salah satu _field_ wajib di dalam `.spec`.

`.spec.template` adalah sebuah [templat Pod](/id/docs/concepts/workloads/pods/pod-overview/#templat-pod). Skemanya benar-benar sama dengan [Pod](/id/docs/concepts/workloads/pods/pod/), kecuali bagian bahwa ia bersarang/_nested_ dan tidak memiliki `apiVersion` atau `kind`.

Selain _field_ wajib untuk Pod, templat Pod di DaemonSet harus
menspesifikasikan label yang sesuai (lihat [selektor Pod](#selektor-pod)).

Templat Pod di DaemonSet harus memiliki [`RestartPolicy`](/id/docs/concepts/workloads/pods/pod-lifecycle/#restart-policy)
yang bernilai `Always`, atau tidak dispesifikasikan, sehingga _default_ menjadi `Always`.
DaemonSet dengan nilai `Always` membuat Pod akan selalu di-_restart_ saat kontainer
keluar/berhenti atau terjadi _crash_.

### Selektor Pod

_Field_ `.spec.selector` adalah selektor Pod. Cara kerjanya sama dengan `.spec.selector` pada [Job](/docs/concepts/jobs/run-to-completion-finite-workloads/).

Pada Kubernetes 1.8, kamu harus menspesifikasikan selektor Pod yang cocok dengan label pada `.spec.template`.
Selektor Pod tidak akan lagi diberi nilai _default_ ketika dibiarkan kosong. Nilai _default_ selektor tidak
cocok dengan `kubectl apply`. Juga, sesudah DaemonSet dibuat, `.spec.selector` tidak dapat diubah.
Mengubah selektor Pod dapat menyebabkan Pod _orphan_ yang tidak disengaja, dan membingungkan pengguna.

Objek `.spec.selector` memiliki dua _field_:

* `matchLabels` - bekerja seperti `.spec.selector` pada [ReplicationController](/id/docs/concepts/workloads/controllers/replicationcontroller/).
* `matchExpressions` - bisa digunakan untuk membuat selektor yang lebih canggih
  dengan mendefinisikan _key_, daftar _value_ dan operator yang menyatakan
  hubungan antara _key_ dan _value_.

Ketika keduanya dispesifikasikan hasilnya diperoleh dari operasi AND.

Jika `.spec.selector` dispesifikasikan, nilainya harus cocok dengan `.spec.template.metadata.labels`. Konfigurasi yang tidak cocok akan ditolak oleh API.

Selain itu kamu tidak seharusnya membuat Pod apapun yang labelnya cocok dengan
selektor tersebut, entah secara langsung, via DaemonSet lain, atau via _workload resource_ lain seperti ReplicaSet.
Jika kamu coba buat, {{< glossary_tooltip term_id="controller" >}} DaemonSet akan
berpikir bahwa Pod tersebut dibuat olehnya. Kubernetes tidak akan menghentikan
kamu melakukannya. Contoh kasus di mana kamu mungkin melakukan ini dengan
membuat Pod dengan nilai yang berbeda di sebuah Node untuk _testing_.

### Menjalankan Pod di Sebagian Node

Jika kamu menspesifikasikan `.spec.template.spec.nodeSelector`, maka _controller_ DaemonSet akan
membuat Pod pada Node yang cocok dengan [selektor
Node](/id/docs/concepts/scheduling-eviction/assign-pod-node/). Demikian juga, jika kamu menspesifikasikan `.spec.template.spec.affinity`,
maka _controller_ DaemonSet akan membuat Pod pada Node yang cocok dengan [Node affinity](/id/docs/concepts/scheduling-eviction/assign-pod-node/).
Jika kamu tidak menspesifikasikan sama sekali, maka _controller_ DaemonSet akan
membuat Pod pada semua Node.

## Bagaimana Pod Daemon Dijadwalkan

### Dijadwalkan oleh _default scheduler_

{{< feature-state state="stable" for-kubernetes-version="1.17" >}}

DaemonSet memastikan bahwa semua Node yang memenuhi syarat menjalankan salinan
Pod. Normalnya, Node yang menjalankan Pod dipilih oleh _scheduler_ Kubernetes.
Namun, Pod DaemonSet dibuat dan dijadwalkan oleh _controller_ DaemonSet. Hal ini
mendatangkan masalah-masalah berikut:

 * Inkonsistensi perilaku Pod: Pod normal yang menunggu dijadwalkan akan dibuat
   dalam keadaan `Pending`, tapi Pod DaemonSet tidak seperti itu. Ini
   membingungkan untuk pengguna.
 * [Pod preemption](/id/docs/concepts/configuration/pod-priority-preemption/)
   ditangani oleh _default scheduler_. Ketika _preemption_ dinyalakan,
   _controller_ DaemonSet akan membuat keputusan penjadwalan tanpa
   memperhitungkan prioritas Pod dan _preemption_.

`ScheduleDaemonSetPods` mengizinkan kamu untuk menjadwalkan DaemonSet
menggunakan _default scheduler_ daripada _controller_ DaemonSet, dengan
menambahkan syarat `NodeAffinity` pada Pod DaemonSet daripada syarat
`.spec.nodeName`. Kemudian, _default scheduler_ digunakan untuk mengikat Pod ke
host target. Jika afinitas Node dari Pod DaemonSet sudah ada, maka ini
akan diganti. _Controller DaemonSet_ hanya akan melakukan operasi-operasi ini
ketika membuat atau mengubah Pod DaemonSet, dan tidak ada perubahan yang terjadi
pada `spec.template` DaemonSet.

```yaml
nodeAffinity:
  requiredDuringSchedulingIgnoredDuringExecution:
    nodeSelectorTerms:
    - matchFields:
      - key: metadata.name
        operator: In
        values:
        - target-host-name
```

Sebagai tambahan, _toleration_ `node.kubernetes.io/unschedulable:NoSchedule`
ditambahkan secara otomatis pada Pod DaemonSet. _Default scheduler_ akan
mengabaikan Node `unschedulable` ketika menjadwalkan Pod DaemonSet.

### _Taint_ dan _Toleration_

Meskipun Pod Daemon menghormati
[taint dan toleration](/id/docs/concepts/configuration/taint-and-toleration),
_toleration_ berikut ini akan otomatis ditambahkan ke Pod DaemonSet sesuai
dengan fitur yang bersangkutan.

| _Toleration Key_                         | _Effect_   | Versi   | Deskripsi                                                                                                    |
| ---------------------------------------- | ---------- | ------- | ------------------------------------------------------------------------------------------------------------ |
| `node.kubernetes.io/not-ready`           | NoExecute  | 1.13+   | Pod DaemonSet tidak akan menjadi _evicted_ ketika ada masalah Node seperti partisi jaringan.                 |
| `node.kubernetes.io/unreachable`         | NoExecute  | 1.13+   | Pod DaemonSet tidak akan menjadi _evicted_ ketika ada masalah Node seperti partisi jaringan.                 |
| `node.kubernetes.io/disk-pressure`       | NoSchedule | 1.8+    |                                                                                                              |
| `node.kubernetes.io/memory-pressure`     | NoSchedule | 1.8+    |                                                                                                              |
| `node.kubernetes.io/unschedulable`       | NoSchedule | 1.12+   | Pod DaemonSet mentoleransi atribut `unschedulable` _default scheduler_.                                      |
| `node.kubernetes.io/network-unavailable` | NoSchedule | 1.12+   | Pod DaemonSet yang menggunakan jaringan host mentoleransi atribut `network-unavailable` _default scheduler_. |



## Berkomunikasi dengan Pod Daemon

Beberapa pola yang mungkin digunakan untuk berkomunikasi dengan Pod dalam DaemonSet, yaitu:

- **Push**: Pod dalam DaemonSet diatur untuk mengirim pembaruan status ke servis lain,
  contohnya _stats database_. Pod ini tidak memiliki klien.
- **IP Node dan Konvensi Port**: Pod dalam DaemonSet dapat menggunakan `hostPort`, sehingga Pod dapat diakses menggunakan IP Node. Klien tahu daftar IP Node dengan suatu cara, dan tahu port berdasarkan konvensi.
- **DNS**: Buat [headless service](/id/docs/concepts/services-networking/service/#headless-services) dengan Pod selektor yang sama,
  dan temukan DaemonSet menggunakan _resource_ `endpoints` atau mengambil beberapa A _record_ dari DNS.
- **Service**: Buat Servis dengan Pod selektor yang sama, dan gunakan Servis untuk mengakses _daemon_ pada
  Node random. (Tidak ada cara mengakses spesifik Node)

## Melakukan Pembaruan DaemonSet

Jika label Node berubah, DaemonSet akan menambahkan Pod ke Node cocok yang baru dan menghapus Pod dari
Node tidak cocok yang baru.

Kamu bisa mengubah Pod yang dibuat DaemonSet. Namun, Pod tidak membolehkan perubahan semua _field_.
Perlu diingat, _controller_ DaemonSet akan menggunakan templat yang asli di waktu selanjutnya 
Node baru (bahkan dengan nama yang sama) dibuat.

Kamu bisa menghapus DaemonSet. Jika kamu spesifikasikan `--cascade=orphan` dengan `kubectl`, maka
Pod akan dibiarkan pada Node. Jika kamu pada waktu kemudian membuat DaemonSet baru dengan selektor
yang sama, DaemonSet yang baru akan mengadopsi Pod yang sudah ada. Jika ada Pod yang perlu diganti,
DaemonSet akan mengganti sesuai dengan `updateStrategy`.

Kamu bisa [melakukan rolling update](/docs/tasks/manage-daemon/update-daemon-set/) pada DaemonSet.

## Alternatif DaemonSet

### _Init Scripts_

Kamu mungkin menjalankan proses _daemon_ dengan cara menjalankan mereka langsung pada Node (e.g. 
menggunakan `init`, `upstartd`, atau `systemd`). Tidak ada salahnya seperti itu. Namun, ada beberapa
keuntungan menjalankan proses _daemon_ via DaemonSet.

- Kemampuan memantau dan mengatur log _daemon_ dengan cara yang sama dengan aplikasi.
- Bahasa dan alat Konfigurasi yang sama (e.g. Templat Pod, `kubectl`) untuk _daemon_ dan aplikasi.
- Menjalankan _daemon_ dalam kontainer dengan batasan _resource_ meningkatkan isolasi antar _daemon_ dari
  kontainer aplikasi. Namun, hal ini juga bisa didapat dengan menjalankan _daemon_ dalam kontainer tapi
  tanpa Pod (e.g. dijalankan langsung via Docker).

### Pod Polosan

Dimungkinkan untuk membuat Pod langsung dengan menspesifikasikan Node mana untuk dijalankan. Namun,
DaemonSet akan menggantikan Pod yang untuk suatu alasan dihapus atau dihentikan, seperti pada saat
kerusakan Node atau pemeliharaan Node yang mengganggu seperti pembaruan _kernel_. Oleh karena itu, kamu
perlu menggunakan DaemonSet daripada membuat Pod satu per satu.

### Pod Statis

Dimungkinkan untuk membuat Pod dengan menulis sebuah berkas ke direktori tertentu yang di-_watch_ oleh Kubelet.
Pod ini disebut dengan istilah [Pod statis](/docs/concepts/cluster-administration/static-pod/).
Berbeda dengan DaemonSet, Pod statis tidak dapat dikelola menggunakan kubectl atau klien API Kubernetes
yang lain. Pod statis tidak bergantung kepada apiserver, membuat Pod statis berguna pada kasus-kasus
_bootstrapping_ klaster.


### Deployment

DaemonSet mirip dengan [Deployment](/id/docs/concepts/workloads/controllers/deployment/) sebab mereka
sama-sama membuat Pod, dan Pod yang mereka buat punya proses yang seharusnya tidak berhenti (e.g. peladen web,
peladen penyimpanan)

Gunakan Deployment untuk layanan _stateless_, seperti _frontend_, di mana proses _scaling_ naik
dan turun jumlah replika dan _rolling update_ lebih penting daripada mengatur secara tepat di
host mana Pod berjalan. Gunakan DaemonSet ketika penting untuk satu salinan Pod
selalu berjalan di semua atau sebagian host, dan ketika Pod perlu berjalan
sebelum Pod lainnya.


