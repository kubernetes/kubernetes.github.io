---
title: StorageClass
content_type: concept
weight: 30
---

<!-- overview -->

Dokumen ini mendeskripsikan konsep StorageClass yang ada pada Kubernetes.
Sebelum lanjut membaca, sangat dianjurkan untuk memiliki pengetahuan terhadap
[volumes](/id/docs/concepts/storage/volumes/) dan
[peristent volume](/id/docs/concepts/storage/persistent-volumes) terlebih dahulu.



<!-- body -->

## Pengenalan

Sebuah StorageClass menyediakan cara bagi administrator untuk
mendeskripsikan "kelas" dari penyimpanan yang mereka sediakan.
Kelas yang berbeda bisa saja memiliki perbedaan dari segi kualitas
servis yang disediakan, pemulihan (_backup_) kebijakan, atau kebijakan lain yang ditentukan
oleh administrator klaster. Kubernetes sendiri tidak dipengaruhi oleh
kelas apakah yang digunakan pada mekanisme penyimpanan yang digunakan.
Mekanisme ini seringkali disebut sebagai _"profiles"_ pada sistem penyimpanan
yang lain.

## Sumber daya StorageClass

Setiap StorageClass (kelas penyimpanan) memiliki _field-field_ mendasar seperti
`provisioner`, `parameters`, dan `reclaimPolicy`, yang digunakan ketika
`PersistentVolume` yang dimiliki oleh kelas tersebut perlu disediakan (di-_provision_).

Nama yang digunakan oleh suatu StorageClass sifatnya penting, karena
ini merupakan cara yang digunakan oleh pengguna untuk meminta
penyimpanan dengan kelas tertentu. Administrator dapat menentukan
nama dan parameter lain dari suatu kelas ketika membuat suatu objek `StorageClass`,
dan objek yang sudah dibuat tidak dapat diubah lagi definisinya.

Administrator dapat memberikan spesifikasi StorageClass _default_ bagi
PVC yang tidak membutuhkan kelas tertentu untuk dapat melakukan mekanisme _bind_:
kamu dapat membaca [bagian `PersistentVolumeClaim`](/id/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims)
untuk penjelasan lebih lanjut.

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: standard
provisioner: kubernetes.io/aws-ebs
parameters:
  type: gp2
reclaimPolicy: Retain
mountOptions:
  - debug
volumeBindingMode: Immediate
```

### _Provisioner_

Setiap kelas penyimpanan (_storage class_) memiliki sebuah _provisioner_ yang
menentukan _plugin_ manakah yang digunakan ketika sebuah PV disediakan (di-_provision_).
_Field_ ini haruslah didefinisikan.

| Plugin Volume        | Provisioner Internal| Contoh Konfigurasi                        |
| :---                 |     :---:           |    :---:                             |
| AWSElasticBlockStore | &#x2713;            | [AWS EBS](#aws-ebs)                          |
| AzureFile            | &#x2713;            | [Azure File](#azure-file)            |
| AzureDisk            | &#x2713;            | [Azure Disk](#azure-disk)            |
| CephFS               | -                   | -                                    |
| Cinder               | &#x2713;            | [OpenStack Cinder](#openstack-cinder)|
| FC                   | -                   | -                                    |
| Flexvolume           | -                   | -                                    |
| Flocker              | &#x2713;            | -                                    |
| GCEPersistentDisk    | &#x2713;            | [GCE PD](#gce-pd)                          |
| Glusterfs            | &#x2713;            | [Glusterfs](#glusterfs)              |
| iSCSI                | -                   | -                                    |
| Quobyte              | &#x2713;            | [Quobyte](#quobyte)                  |
| NFS                  | -                   | -                                    |
| RBD                  | &#x2713;            | [Ceph RBD](#ceph-rbd)                |
| VsphereVolume        | &#x2713;            | [vSphere](#vsphere)                  |
| PortworxVolume       | &#x2713;            | [Portworx Volume](#portworx-volume)  |
| ScaleIO              | &#x2713;            | [ScaleIO](#scaleio)                  |
| StorageOS            | &#x2713;            | [StorageOS](#storageos)              |
| Local                | -                   | [Local](#local)              |

Kamu tidak dibatasi untuk hanya menggunakan _provisioner_ internal yang disediakan
pada list yang tersedia (yang memiliki nama dengan prefix "kubernetes.io" dan
didistribusikan bersamaan dengan Kubernetes). Kamu juga dapat menjalankan dan
mendefinisikan _provisioner_ eksternal yang merupakan program independen selama
program tersebut menerapkan [spesifikasi](https://git.k8s.io/community/contributors/design-proposals/storage/volume-provisioning.md)
yang didefinisikan oleh Kubernetes. Penulis dari _provisioner_ eksternal Kubernetes
memiliki kuasa penuh akan tempat dimana kode sumber yang mereka tulis, bagaimana
mekanisme penyediaan (_provisioning_) dilakukan, serta bagaimana hal tersebut dapat dijalankan,
serta _plugin_ volume apakah yang digunakan (termasuk Flex), dkk.
Repositori [kubernetes-incubator/external-storage](https://github.com/kubernetes-incubator/external-storage)
menyimpan _library_ yang dibutukan untuk menulis _provisioner_ eksternal
yang mengimplementasi spesifikasi serta beberapa _provisioner_ eksternal yang
dipelihara oleh komunitas.

Sebagai contoh, NFS tidak menyediakan _provisioner_ internal, tetapi
sebuah _provisioner_ eksternal dapat digunakan. Beberapa _provisioner_ eksternal
dapat ditemukan di bawah repositori [kubernetes-incubator/external-storage](https://github.com/kubernetes-incubator/external-storage).
Di sana juga terdapat beberapa kasus dimana vendor penyimpanan _3rd party_
menyediakan _provisioner_ eksternal yang mereka sediakan sendiri.

### Perolehan Kembali untuk Kebijakan (_Reclaim Policy_)

_Persistent Volumes_ yang secara dinamis dibuat oleh sebuah kelas penyimpanan
akan memiliki _reclaim policy_ yang didefinisikan di dalam _field_ `reclaimPolicy`
dari kelas tersebut, yang nilainya dapat diisi dengan `Delete` atau `Retain`.
Jika tidak terdapat `reclaimPolicy` yang dispesifikasikan ketika sebuah objek
StorageClass dibuat, maka nilai default bagi kelas tersebut adalah `Delete`.

PersistentVolume yang dibuat secara manual dan diatur dengan menggunakan
kelas penyimpanan akan menggunakan _reclaim policy_ apapun yang diberikan
pada saat objek tersebut dibuat.

### Pilihan _Mount_

PersistentVolume yang secara dinamis dibuat oleh sebuah kelas penyimpanan
akan memiliki pilihan _mount_ yang dapat dispesifikasikan pada _field_
`mountOptions` dari kelas tersebut.

Jika sebuah _plugin_ volume tidak mendukung pilihan _mount_
yang dispesifikasikan, mekanisme penyediaan (_provision_) akan digagalkan. Pilihan _mount_
yang akan divalidasi pada kelas penyimpanan maupun PV, maka _mount_ tersebut
akan gagal apabila salah satu dari keduanya bersifat invalid.

### Mode Volume _Binding_

_Field_ `volumeBindingMode` mengontrol kapan mekanisme [_binding_ volume dan
_provisioning_ dinamis](/id/docs/concepts/storage/persistent-volumes/#provisioning)
harus dilakukan.

Secara _default_, ketika mode `Immediate` yang mengindikasikan
terjadinya volume _binding_ dan _provisioning_ dinamis terjadi ketika
PersistentVolumeClaim dibuat. Untuk _backend_ penyimpanan yang dibatasi oleh
topologi tertentu dan tidak dapat diakses secara global dari semua Node
yang ada di klaster, PersistentVolume akan di-_bound_ atau di-_provision_
tanpa perlu memenuhi persyaratan _scheduling_ dari Pod. Hal ini dapat menyebabkan
adanya Pod yang tidak mendapatkan mekanisme _scheduling_.

Seorang administrator klaster dapat mengatasi hal tersebut dengan cara memberikan
spesifikasi mode `WaitForFirstConsumer` yang akan memperlambat mekanisme _provisioning_
dan _binding_ dari sebuah PersistentVolume hingga sebuah Pod yang menggunakan
PersistentVolumeClaim dibuat. PersistentVolume akan dipilih atau di-_provisioning_
sesuai dengan topologi yang dispesifikasikan oleh limitasi yang diberikan
oleh mekanisme _scheduling_ Pod. Hal ini termasuk, tetapi tidak hanya terbatas pada,
[persyaratan sumber daya](/id/docs/concepts/configuration/manage-compute-resources-container),
[_node selector_](/id/docs/concepts/scheduling-eviction/assign-pod-node/#nodeselector),
[afinitas dan
anti-afinitas Pod](/id/docs/concepts/scheduling-evictionassign-pod-node/#affinity-and-anti-affinity),
serta [_taint_ dan _toleration_](/id/docs/concepts/scheduling-eviction/taint-and-toleration).

Beberapa _plugin_ di bawah ini mendukung `WaitForFirstConsumer` dengan _provisioning_
dinamis:

* [AWSElasticBlockStore](#aws-ebs)
* [GCEPersistentDisk](#gce-pd)
* [AzureDisk](#azure-disk)

Beberapa _plugin_ di bawah ini mendukung `WaitForFirstConsumer` dengan _binding_
PersistentVolume yang terlebih dahulu dibuat:

* Semua hal di atas
* [Lokal](#lokal)

{{< feature-state state="beta" for_k8s_version="1.14" >}}
[Volume-volume CSI](/id/docs/concepts/storage/volumes/#csi) juga didukung
dengan adanya _provisioning_ dinamis serta PV yang telah terlebih dahulu dibuat,
meskipun demikian, akan lebih baik apabila kamu melihat dokumentasi
untuk driver spesifik CSI untuk melihat topologi _key_ yang didukung
beserta contoh penggunaannya. _Feature gate_ `CSINodeInfo` haruslah diaktifkan.

### Topologi yang Diizinkan

Ketika sebuah operator klaster memberikan spesifikasi `WaitForFirstConsumer` pada
mode `binding` volume, mekanisme pembatasan (restriksi) `provisioning` tidak lagi dibutuhkan
pada sebagian besar kasus. Meskipun begitu, apabila hal tersebut masih dibutuhkan,
`field` `allowedTopologies` dapat dispesifikasikan.

Contoh ini memberikan demonstrasi bagaimana cara membatasi topologi
dari volume yang di-_provision_ pada suatu zona spesifik serta harus digunakan
sebagai pengganti parameter `zone` dam `zones` untuk `plugin` yang akan digunakan.

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: standard
provisioner: kubernetes.io/gce-pd
parameters:
  type: pd-standard
volumeBindingMode: WaitForFirstConsumer
allowedTopologies:
- matchLabelExpressions:
  - key: failure-domain.beta.kubernetes.io/zone
    values:
    - us-central1-a
    - us-central1-b
```

## Parameter-Parameter

Kelas-kelas penyimpanan memiliki parameter yang mendeskripsikan
volume yang dimiliki oleh kelas penyimpanan tersebut. Parameter yang berbeda
bisa saja diterima bergantung pada `provisioner`. Sebagai contohnya, nilai `io1`,
untuk parameter `type`, dan parameter `iopsPerGB` spesifik terhadap EBS.
Ketika sebuah parameter diabaikan, beberapa nilai _default_ akan digunakan sebagai
gantinya.

### AWS EBS

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: slow
provisioner: kubernetes.io/aws-ebs
parameters:
  type: io1
  iopsPerGB: "10"
  fsType: ext4
```

* `type`: `io1`, `gp2`, `sc1`, `st1`. Lihat
  [dokumentasi AWS](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSVolumeTypes.html)
  untuk detail lebih lanjut. Nilai _default_: `gp2`.
* `zone` (_deprecated_): zona AWS. Jika tidak terdapat nilai `zone` atau `zones`
  yang dispesifikasikan, volume secara generik dijadwalkan dengan menggunakan
  penjadwalan `round-robin-ed` pada semua zona aktif yang ada pada klaster Kubernetes
  yang memiliki _node_.
* `zones` (_deprecated_): Nilai terpisahkan koma yang merupakan barisan zona pada AWS.
  Jika tidak terdapat nilai `zone` atau `zones` yang dispesifikasikan,
  volume secara generik dijadwalkan dengan menggunakan penjadwalan
  `round-robin-ed` pada semua zona aktif yang ada pada klaster Kubernetes
  yang memiliki _node_.
* `iopsPerGB`: hanya untuk volume `io1`. Operasi per detik per GiB. Volume _plugin_
  AWS mengalikan nilai ini dengan ukuran volume yang dibutuhkan untuk menghitung IOPS
  dari volume (nilai maksimum yang didukung adalah 20,000 IOPS baca [dokumentasi
  AWS](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSVolumeTypes.html).
  Nilai masukan yang diharapkan merupakan string, misalnya `"10"`, bukan `10`.
* `fsType`: fsType yang didukung oleh Kubernetes. Nilai _default_-nya adalah: `"ext4"`.
* `encrypted`: menyatakan dimana volume EBS harus dienkripsi atau tidak.
  Nilai yang valid adalah `"true"` atau `"false"` (dalam string bukan boolean i.e. `"true"`, bukan `true`).
* `kmsKeyId`: opsional. Merupakan nama dari Amazon Resource Name dari _key_ yang digunakan
  untuk melakukan enkripsi volume. Jika nilai ini tidak disediakan tetapi nilai dari
  _field_ `encrypted` adalah _true_, sebuah _key_ akan dibuat oleh AWS. Perhatikan dokumentasi AWS
  untuk mengetahui nilai yang valid bagi ARN.

{{< note >}}
Parameter `zone` dan `zones` sudah terdeprekasi dan digantikan oleh
[allowedTopologies](#topologi-yang-diizinkan)
{{< /note >}}

### PD GCE

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: slow
provisioner: kubernetes.io/gce-pd
parameters:
  type: pd-standard
  replication-type: none
```

* `type`: `pd-standard` atau `pd-ssd`. Nilai _default_: `pd-standard`
* `zone` (_deprecated_): zona GCE. Jika tidak terdapat nilai `zone` atau `zones`
   yang dispesifikasikan, volume secara generik dijadwalkan dengan menggunakan
   penjadwalan `round-robin-ed` pada semua zona aktif yang ada pada klaster Kubernetes
   yang memiliki _node_.
* `zones` (_deprecated_): Nilai terpisahkan koma yang merupakan barisan zona.
  Jika tidak terdapat nilai `zone` atau `zones` yang dispesifikasikan,
  volume secara generik dijadwalkan dengan menggunakan penjadwalan
  `round-robin-ed` pada semua zona aktif yang ada pada klaster Kubernetes
  yang memiliki _node_.
* `replication-type`: `none` atau `regional-pd`. Nilai _default_: `none`.

Jika `replication-type` diubah menjadi `none`, sebuah PD reguler (zonal) akan
di-_provisioning_.

Jika `replication-type` diubah menjadi `regional-pd`, sebuah
[_Persistent_ Disk Regional (PD Regional)](https://cloud.google.com/compute/docs/disks/#repds)
akan di-_provisioning_. Pada kasus ini, pengguna harus menggunakan `zones`
dan bukan `zone` untuk menspesifikasikan zona replikasi yang diinginkan. Jika terdapat
tepat dua zona yang dispesifikasikan, PD Regional akan di-_provisioning_ pada
zona replikasi yang diinginkan. Jika terdapat lebih dari 2 zona yang dispesifikasikan,
Kubernetes akan memilih secara acak zona dari zona-zona yang dispesifikasikan. Jika
parameter `zones` tidak diinisialisasi, Kubernetes akan memilih secara acak dari
zona yang diatur oleh klaster Kubernetes.

{{< note >}}
Parameter `zone` dan `zones` sudah _deprecated_ dan digantikan oleh
[allowedTopologies](#topologi-yang-diizinkan)
{{< /note >}}

### Glusterfs

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: slow
provisioner: kubernetes.io/glusterfs
parameters:
  resturl: "http://127.0.0.1:8081"
  clusterid: "630372ccdc720a92c681fb928f27b53f"
  restauthenabled: "true"
  restuser: "admin"
  secretNamespace: "default"
  secretName: "heketi-secret"
  gidMin: "40000"
  gidMax: "50000"
  volumetype: "replicate:3"
```

* `resturl`: Servis REST Gluster/URL servis Heketi yang digunakan untuk
  melakukan _provisioning_ volume gluster sesuai dengan kebutuhan. Format secara umum
  haruslah dalam bentuk `IPaddress:Port` dan hal ini merupakan parameter wajib untuk
  _provisioner_ dinamis GlusterFS. Jika servis Heketi diekspos sebagai servis yang dapat
  melakukan _routing_ pada pengaturan openshift/kubernetes, ini dapat memiliki
  format yang sesuai dengan `http://heketi-storage-project.cloudapps.mystorage.com`
  dimana fqdn yang ada merupakan URL servis Heketi yang dapat di-_resolve_.
* `restauthenabled` : Servis REST Gluster menyediakan nilai boolean yang dapat digunakan
  untuk mengajukan `authentication` untuk server REST yang ada. Jika nilai yang disediakan
  adalah `"true"`, dengan kondisi dimana `restuser` dan `restuserkey` atau `secretNamespace` + `secretName`
  harus diisi. Opsi ini sudah_deprecated_, mekanisme otentikasi akan diizinkan apabila
  salah satu dari _field_ `restuser`, `restuserkey`, `secretName` atau `secretNamespace` diterapkan.
* `restuser` : Pengguna servis REST Gluster/Heketi yang memiliki akses
  untuk membuat volume di dalam Trusted Pool Gluster.
* `restuserkey` : Password pengguna servis REST Gluster/Heketi
  yang digunakan untuk mekanisme otentikasi server REST. Parameter ini _deprecated_
  dan digantikan dengan parameter `secretNamespace` + `secretName`.
* `secretNamespace`, `secretName` : Identifikasi instans Secret yang mengandung
  password pengguna yang digunakan untuk berkomunikasi dengan servis REST Gluster.
  Parameter ini dianggap opsional, password kosong dapat digunakan ketika
  nilai dari `secretNamespace` dan `secretName` tidak dispesifikasikan.
  Secret yang disediakan haruslah memiliki tipe `"kubernetes.io/glusterfs"`,
  yang dapat dibuat dengan menggunakan mekanisme dibawah ini:

    ```
    kubectl create secret generic heketi-secret \
      --type="kubernetes.io/glusterfs" --from-literal=key='opensesame' \
      --namespace=default
    ```

    Contoh Secret dapat ditemukan pada berkas berikut
    [glusterfs-provisioning-secret.yaml](https://github.com/kubernetes/examples/tree/master/staging/persistent-volume-provisioning/glusterfs/glusterfs-secret.yaml).

* `clusterid`: `630372ccdc720a92c681fb928f27b53f` merupakan ID dari klaster
  yang akan digunakan oleh Heketi ketikan melakukan _provisioning_ volume. ID ini juga
  dapat berupa serangkaian list, misalnya: `"8452344e2becec931ece4e33c4674e4e,42982310de6c63381718ccfa6d8cf397"`.
  Parameter ini merupakan parameter opsional.
* `gidMin`, `gidMax` : Nilai minimum dan maksimum dari GID untuk kelas penyimpanan (_storage class_).
  Sebuah nilai unik dari GID di dalam _range_ ( gidMin-gidMax ) ini akan digunakan untuk melakukan
  _provisioning_ volume secara dinamis. Nilai ini bersifat opsional. Jika tidak dispesifikasikan,
  volume akan secara default di-_provisioning_ dalam _range_ 2000-2147483647 yang merupakan nilai default
  dari gidMin dan gidMax.
* `volumetype` : Tipe volume beserta paremeter-nya dapat diatur dengan menggunakan nilai opsional
  berikut. Jika tipe dari volume tidak dispesifikasikan, maka _provisioner_ akan memutuskan tipe
  volume apakah yang akan digunakan.

  Sebagai contoh:

  * Volume replika: `volumetype: replicate:3` dimana '3' merupakan jumlah replika.

  * Persebaran (_Disperse_)/EC volume: `volumetype: disperse:4:2` dimana'4' merupakan data dan '2' merupakan jumlah redundansi.

  * Distribusi volume: `volumetype: none`

  Untuk tipe volume apa saja yang tersedia dan berbagai opsi administrasi yang ada, kamu dapat membaca
  [Petunjuk Administrasi](https://access.redhat.com/documentation/en-US/Red_Hat_Storage/3.1/html/Administration_Guide/part-Overview.html).

  Untuk informasi lebih lanjut, kamu dapat membaca
  [Bagaimana Cara Mengatur Heketi](https://github.com/heketi/heketi/wiki/Setting-up-the-topology).

  Ketika PersistentVolume di-_provisioning_ secara dinamis, plugin Gluster secara otomatis
  akan membuat _endpoint_ serta sebuah servis _headless_ dengan nama `gluster-dynamic-<claimname>`.
  _Endpoint_ dinamis dan servis secara otomatis akan dihapus ketika PVC dihapus.

### OpenStack Cinder

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: gold
provisioner: kubernetes.io/cinder
parameters:
  availability: nova
```

* `availability`: Zona _Availability_. Jika tidak dispesifikasikan, secara umum volume akan
  diatur dengan menggunakan algoritma _round-robin_ pada semua zona aktif
  dimana klaster Kubernetes memiliki sebuah node.

{{< note >}}
{{< feature-state state="deprecated" for_k8s_version="1.11" >}}
_Provisioner_ internal OpenStack ini sudah _deprecated_. Kamu dapat menggunakan [_provider_ eksternal penyedia layanan _cloud_ untuk OpenStack](https://github.com/kubernetes/cloud-provider-openstack).
{{< /note >}}

### vSphere

1. Buatlah sebuah StorageClass dengan menggunakan sebuah format disk yang dispesifikasikan oleh pengguna.

    ```yaml
    apiVersion: storage.k8s.io/v1
    kind: StorageClass
    metadata:
      name: fast
    provisioner: kubernetes.io/vsphere-volume
    parameters:
      diskformat: zeroedthick
    ```

    `diskformat`: `thin`, `zeroedthick` dan `eagerzeroedthick`. Nilai default: `"thin"`.

2. Buatlah sebuah StorageClass dengan menggunakan sebuah format disk pada _datastore_ yang dispesifikasikan oleh pengguna.

    ```yaml
    apiVersion: storage.k8s.io/v1
    kind: StorageClass
    metadata:
      name: fast
    provisioner: kubernetes.io/vsphere-volume
    parameters:
        diskformat: zeroedthick
        datastore: VSANDatastore
    ```

    `datastore`: Pengguna juga dapat menspesifikasikan _datastore_ pada StorageClass.
    Volume akan dibuat pada datastore yang dispesifikasikan pada kelas penyimpanan,
    dalam hal ini adalah `VSANDatastore`. _Field_ ini bersifat opsional. Jika _datastore_
    tidak dispesifikasikan, maka volume akan dibuat dengan menggunakan _datastore_ yang dispesifikasikan
    pada berkas konfigurasi vSphere yang digunakan untuk menginisialisasi penyedia layanan cloud vSphere.

3. Manajemen Kebijakan Penyimpanan di dalam Kubernetes

    * Menggunakan kebijakan (_policy_) yang ada pada vCenter

        Salah satu dari fitur paling penting yang ada pada vSphere untuk manajemen penyimpanan
        adalah manajemen bebasis _policy_. Storage Policy Based Management (SPBM) adalah _framework_
        yang menyediakan sebuah _control plane_ terpadu pada _data service_ yang meluas dan
        solusi penyimpanannya yang tersedia. SPBM memungkinkan administrator vSphere menghadapi
        permasalahan yang mungkin muncul seperti _capacity planning_, membedakan level servis, dan
        melakukan manajemen _headroom capacity_.

        _Policy_ SPBM dapat dispesifikasikan pada StorageClass menggunakan parameter
        `storagePolicyName`.

    * Dukungan _policy_ SAN virtual di dalam Kubernetes

        Administrator _Vsphere Infrastructure_ (VI) akan memiliki kemampuan
        untuk menspesifikasikan Virtual SAN Storage Capabilities khusus
        selama masa _provisioning_ volume secara dinamis. Persyaratan kapabilitas
        penyimpanan diubah menjadi sebuah _policy_ Virtual SAN yang nantinya akan
        dimasukkan ke dalam lapisan Virtual SAN ketika sebuah _persitent volume_ (penyimpanan
        virtual) dibuat. Penyimpanan virtual kemudian akan didistribusikan pada semua
        _datastore_ Virtual SAN untuk memenuhi kebutuhan ini.

        Kamu dapat melihat [_Policy_ Penyimpanan Berdasarkan Manajemen untuk _Provisioning_ Dinamis Volume](https://vmware.github.io/vsphere-storage-for-kubernetes/documentation/policy-based-mgmt.html)
        untuk detil lebih lanjut mengenai penggunaan _policy_ penyimpanan untuk manajemen _persistent volume_.

Terdapat beberapa
[contoh vSphere](https://github.com/kubernetes/examples/tree/master/staging/volumes/vsphere)
yang dapat kamu gunakan untuk mencoba manajemen _persistent volume_ di dalam Kubernetes untuk vSpehere.

### RBD Ceph

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast
provisioner: kubernetes.io/rbd
parameters:
  monitors: 10.16.153.105:6789
  adminId: kube
  adminSecretName: ceph-secret
  adminSecretNamespace: kube-system
  pool: kube
  userId: kube
  userSecretName: ceph-secret-user
  userSecretNamespace: default
  fsType: ext4
  imageFormat: "2"
  imageFeatures: "layering"
```

* `monitors`: Monitor Ceph, merupakan nilai yang dipisahkan oleh koma (csv). Parameter ini dibutuhkan.
* `adminId`: ID klien Ceph yang dapat digunakan untuk membuat images di dalam pool.
  Nilai _default_-nya adalah "admin".
* `adminSecretName`: Nama Secret untuk `adminId`. Parameter ini dibutuhkan.
  Secret yang dibutuhkan haruslah memiliki tipe "kubernetes.io/rbd".
* `adminSecretNamespace`: Namespace untuk `adminSecretName`. Nilai _default_-nya adalah "default".
* `pool`: Pool Ceph RBD. Nilai _default_-nya adalah "rbd".
* `userId`: Klien ID Ceph yang digunakan untuk melakukan pemetaan image RBD. Nilai _default_-nya sama dengan
  `adminId`.
* `userSecretName`: Nama Secret Ceph untuk `userId` yang digunakan untuk memetakan image RBD.
  Secret ini harus berada pada namespace yang sama dengan PVC. Parameter ini dibutuhkan.
  Secret yang disediakan haruslah memiliki tipe "kubernetes.io/rbd", dibuat dengan cara:

    ```shell
    kubectl create secret generic ceph-secret --type="kubernetes.io/rbd" \
      --from-literal=key='QVFEQ1pMdFhPUnQrSmhBQUFYaERWNHJsZ3BsMmNjcDR6RFZST0E9PQ==' \
      --namespace=kube-system
    ```
* `userSecretNamespace`: Namespace untuk `userSecretName`.
* `fsType`: fsType yang didukung oleh kubernetes. Nilai _default_-nya adalah: `"ext4"`.
* `imageFormat`: Format image Ceph RBD, nilai yang mungkin adalah "1" atau "2". Nilai _default_-nya adalah "2".
* `imageFeatures`: Parameter ini bersifat opsional dan hanya dapat digunakan jika kamu mengganti nilai
  dari `imageFormat` ke "2". Saat ini fitur yang didukung hanyalah `layering`.
  Nilai _default_-nya adalah "", dan tidak ada fitur yang diaktifkan.

### Quobyte

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
   name: slow
provisioner: kubernetes.io/quobyte
parameters:
    quobyteAPIServer: "http://138.68.74.142:7860"
    registry: "138.68.74.142:7861"
    adminSecretName: "quobyte-admin-secret"
    adminSecretNamespace: "kube-system"
    user: "root"
    group: "root"
    quobyteConfig: "BASE"
    quobyteTenant: "DEFAULT"
```

* `quobyteAPIServer`: API Server dari Quobyte dalam format
  `"http(s)://api-server:7860"`
* `registry`: Registri Quobyte yang digunakan untuk melakukan _mount_ volume. Kamu dapat menspesifikasikan
  registri yang kamu inginkan dengan format pasangan ``<host>:<port>`` atau jika kamu ingin mendefinisikan
  beberapa registri sekaligus kamu dapat menempatkan koma diantara setiap pasangan ``<host>:<port>``  yang ada,
  misalnya ``<host1>:<port>,<host2>:<port>,<host3>:<port>``.
  Host dapat berupa alamat IP atau DNS.
* `adminSecretNamespace`: Namespace `adminSecretName`. Nilai default-nya adalah "default".
* `adminSecretName`: Secret yang mengandung informasi mengenai pengguna Quobyte dan
  password yang digunakan untuk melakukan otentikasi API server. Secret yang digunakan
  haruslah memiliki tipe "kubernetes.io/quobyte", yang dibuat dengan mekanisme berikut:

    ```shell
    kubectl create secret generic quobyte-admin-secret \
      --type="kubernetes.io/quobyte" --from-literal=key='opensesame' \
      --namespace=kube-system
    ```

* `user`: Melakukan pemetaan terhadap semua akses yang dimiliki pengguna.
   Nilai _default_-nya adalah "root".
* `group`: Melakukan pemetaan terhadap semua group. Nilai _default_-nya adalah "nfsnobody".
* `quobyteConfig`: Menggunakan konfigurasi spesifik untuk membuat volume.
  Kamu dapat membuat sebuah file konfigurasi atau melakukan modifikasi terhadap konfigurasi yang sudah ada
  dengan menggunakan tatap muka Web atau CLI quobyte. Nilai _default_-nya adalah "BASE".
* `quobyteTenant`: Menggunakan ID tenant yang dispesifikasikan untuk membuat/menghapus volume.
  _Tenant_ Quobyte haruslah sudah berada di dalam Quobyte. Nilai _default_-nya adalah "DEFAULT".

### Azure Disk

#### Kelas Penyimpanan Disk Azure yang Tidak Dikelola

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: slow
provisioner: kubernetes.io/azure-disk
parameters:
  skuName: Standard_LRS
  location: eastus
  storageAccount: azure_storage_account_name
```

* `skuName`: Akun penyimpanan Azure yang ada pada tingkatan Sku. Nilai _default_-nya adalah kosong.
* `location`: Lokasi akun penyimpanan Azure. Nilai _default_-nya adalah kosong.
* `storageAccount`: Nama akun penyimpanan Azure. Jika sebuan akun penyimpanan disediakan,
  akun tersebut haruslah berada pada grup sumber daya yang ada dengan klaster,
  dan `location` akan diabaikan. Jika sebuah akun penyimpanan tidak disediakan, sebuah akun penyimpanan
  baru akan dibuat pada grup sumber daya yang ada dengan klaster.

#### Kelas Penyimpanan Disk Azure yang Baru (mulai versi v1.7.2)

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: slow
provisioner: kubernetes.io/azure-disk
parameters:
  storageaccounttype: Standard_LRS
  kind: managed
```

* `storageaccounttype`: Akun penyimpanan Azure yang ada pada tingkatan Sku. Nilai _default_-nya adalah kosong.
* `kind`: Nilai yang mungkin adalah `shared`, `dedicated`, dan `managed` (default).
  Ketika `kind` yang digunakan adalah `shared`, semua disk yang tidak di-_manage_ akan
  dibuat pada beberapa akun penyimpanan yang ada pada grup sumber daya yang sama dengan klaster.
  Ketika `kind` yang digunakan adalah `dedicated`, sebuah akun penyimpanan
  baru akan dibuat pada grup sumber daya yang ada dengan klaster. Ketika `kind` yang digunakan adalah
  `managed`, semua disk yang dikelola akan dibuat pada grup sumber daya yang ada dengan klaster.

- VM premium dapat di-_attach_ baik pada Standard_LRS dan Premium_LRS disks, sementara Standard
  VM hanya dapat di-_attach_ pada disk Standard_LRS.
- VM yang dikelola hanya dapat meng-_attach_ disk yang dikelola dan VM yang tidak dikelola hanya dapat
  meng-_attach_ disk yang tidak dikelola.

### Berkas Azure

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: azurefile
provisioner: kubernetes.io/azure-file
parameters:
  skuName: Standard_LRS
  location: eastus
  storageAccount: azure_storage_account_name
```

* `skuName`: Akun penyimpanan Azure yang ada pada tingkatan Sku. Nilai _default_-nya adalah kosong.
* `location`: Lokasi akun penyimpanan Azure. Nilai _default_-nya adalah kosong.
* `storageAccount`: Nama akun penyimpanan Azure. Nilai _default_-nya adalah kosong. Jika sebuah penyimpanan
  tidak memiliki sebuah akun yang disediakan, semua akun penyimpanan yang diasosiasikan dengan
  grup sumber daya yang ada dan kemudian melakukan pencarian terhadap akun yang sesuai dengan
  `skuName` dan `location`. Jika sebuah akun penyimpanan disediakan, akun tersebut haruslah berada
  di dalam grup sumber daya yang sama dengan klaster, serta `skuName` dan `location` akan diabaikan.

Selama _provision_, sebuah secret dibuat untuk menyimpan _credentials_. Jika klaster
menggunakan konsep [RBAC](/id/docs/reference/access-authn-authz/rbac/) dan
[_Roles_ Controller](/id/docs/reference/access-authn-authz/rbac/#controller-roles),
menambahkan kapabilitas `create` untuk sumber daya `secret` bagi clusterrole
`system:controller:persistent-volume-binder`.

### Volume Portworx

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: portworx-io-priority-high
provisioner: kubernetes.io/portworx-volume
parameters:
  repl: "1"
  snap_interval:   "70"
  io_priority:  "high"

```

* `fs`: filesystem yang akan digunakan: `none/xfs/ext4` (nilai default-nya: `ext4`).
* `block_size`: ukuran block dalam Kbytes (nilai _default_-nya: `32`).
* `repl`: jumlah replika _synchronous_ yang dapat disediakan dalam bentuk
  faktor replikasi `1..3` (nilai _default_-nya: `1`) Nilai yang diharapkan dalam bentuk String
  `"1"` dan bukan `1`.
* `io_priority`: menentukan apakah volume yang dibuat akan dari penyimpanan dengan kualitas
  tinggi atau rendah dengan urutan prioritas `high/medium/low` (nilai _default_-nya: `low`).
* `snap_interval`: interval waktu dalam menit yang digunakan untuk melakukan _trigger_ _snapshots_.
  _Snapshots_ dibuat secara inkremen berdasarkan perbedaan yang ada dengan _snapshot_ yang dibuat sebelumnya,
  nilai perbedaan 0 akan menonaktifkan pembuatan _snapshot_ (nilai default-nya: `0`). Sebuah string merupakan nilai
  yang diharapkan `"70"` dan bukan `70`.
* `aggregation_level`: menspesifikasikan jumlah _chunks_ dimana volume akan didistribusikan,
  0 mengindikasikan volume yang _non-aggregate_ (nilai default-nya: `0`). Sebuah string merupakan nilai
  yang diharapkan `"0"` dan bukan `0`.
* `ephemeral`: menentukan apakah volume harus dihapus setelah di-_unmount_
  atau harus tetap ada. Penggunaan `emptyDir` dapat diubah menjadi true dan penggunaan
  `persistent volumes` untuk basisdata seperti Cassandra harus diubah menjadi false`,
  true/false` (nilai default-nya: `false`). Sebuah string merupakan nilai
  yang diharapkan `"true"` dan bukan `true`.

### ScaleIO

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: slow
provisioner: kubernetes.io/scaleio
parameters:
  gateway: https://192.168.99.200:443/api
  system: scaleio
  protectionDomain: pd0
  storagePool: sp1
  storageMode: ThinProvisioned
  secretRef: sio-secret
  readOnly: false
  fsType: xfs
```

* `provisioner`: atribut yang nilainya merupakan `kubernetes.io/scaleio`
* `gateway`: alamat _gateway_ ScaleIO (wajib)
* `system`: nama sistem ScaleIO (wajib)
* `protectionDomain`: nama domain proteksi ScaleIO (wajib)
* `storagePool`: nama pool volume penyimpanan (wajib)
* `storageMode`: mode _provisioning_ penyimpanan: `ThinProvisioned` (default) atau
  `ThickProvisioned`
* `secretRef`: penunjuk pada objek Secret yang dikonfigurasi (wajib)
* `readOnly`: menentukan mode akses terhadap volume yang di-_mount_  (nilai default-nya: false)
* `fsType`: filesystem yang digunakan untuk volume (nilai default-nya: ext4)

Plugin volume ScaleIO Kubernetes membutuhkan objek Secret yang suda dikonfigurasi sebelumnya.
Secret ini harus dibuat dengan tipe `kubernetes.io/scaleio` dan menggunakan namespace yang sama
dengan PVC yang dirujuk, seperti ditunjukkan pada contoh yang ada:

```shell
kubectl create secret generic sio-secret --type="kubernetes.io/scaleio" \
--from-literal=username=sioadmin --from-literal=password=d2NABDNjMA== \
--namespace=default
```

### StorageOS

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast
provisioner: kubernetes.io/storageos
parameters:
  pool: default
  description: Kubernetes volume
  fsType: ext4
  adminSecretNamespace: default
  adminSecretName: storageos-secret
```

* `pool`: Nama kapasitas distribusi StorageOS yang digunakan untuk melakukan
  _provisioning_ volume. _Pool_ default akan digunakan apabila nilainya tidak dispesifikasikan.
* `description`: Deskripsi untuk melakukan _assignment_ volume yang baru dibuat secara dinamis.
  Semua deskripsi volume akan bernilai sama untuk kelas penyimpanan yang sama, meskipun begitu
  kelas penyimpanan yang berbeda dapat digunakan untuk membuat deskripsi yang berbeda untuk penggunaan
  yang berbeda. Nilai default-nya adalah `Kubernetes volume`.
* `fsType`: Tipe filesystem default yang digunakan. Perhatikan bahwa aturan
  yang didefinisikan oleh pengguna di dalam StirageOS dapat meng-_override_ nilai ini.
  Nilai default-nya adalah `ext4`.
* `adminSecretNamespace`: Namespace dimana konfigurasi secret API berada. Hal ini bersifat wajib
  apabila adminSecretName diaktifkan.
* `adminSecretName`: Nama secret yang digunakan untuk memperoleh _credentials_ StorageOS
  API. Jika tidak dispesifikasikan, nilaidefault akan digunakan.

Plugin volume dapat menggunakan objek Secret untuk menspesifikasikan
endpoint dan kredensial yang digunakan untuk mengakses API StorageOS.
Hal ini hanya akan dibutuhkan apabila terdapat perubahan pada nilai _default_.
Secret ini harus dibuat dengan tipe `kubernetes.io/storageos`,
seperti ditunjukkan pada contoh yang ada:

```shell
kubectl create secret generic storageos-secret \
--type="kubernetes.io/storageos" \
--from-literal=apiAddress=tcp://localhost:5705 \
--from-literal=apiUsername=storageos \
--from-literal=apiPassword=storageos \
--namespace=default
```

Secret yang digunakan untuk melakukan _provisioning_ volume secara dinamis
dapat dibuat di namespace apapun dan dirujuk dengan menggunakan parameter `adminSecretNamespace`.
Secret yang digunakan oleh volume yang sedang di-_provisioning_ harus dibuat pada namespace yang sama
dengan PVC yang merujuk secret tersebut.

### Lokal

{{< feature-state for_k8s_version="v1.14" state="stable" >}}

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: local-storage
provisioner: kubernetes.io/no-provisioner
volumeBindingMode: WaitForFirstConsumer
```

Volume lokal tidak mendukung adanya _provisioning_ secara dinamis,
meskipun begitu sebuah StorageClass akan tetap dibuat untuk mencegah terjadinya _bind_ volume
sampai _scheduling_ pod dilakukan. Hal ini dispesifikasikan oleh mode _binding_ volume
`WaitForFirstConsumer`.

Memperlambat _binding_ volume mengizinkan _scheduler_ untuk memastikan
batasan _scheduling_ semua pod ketika memilih PersistentVolume untuk sebuah PersistentVolumeClaim.


