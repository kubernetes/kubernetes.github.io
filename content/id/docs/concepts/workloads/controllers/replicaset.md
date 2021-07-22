---
title: ReplicaSet
content_type: concept
weight: 10
---

<!-- overview -->

Tujuan dari ReplicaSet adalah untuk memelihara himpunan stabil dari replika Pod yang sedang berjalan pada satu waktu tertentu. Maka dari itu, ReplicaSet seringkali digunakan untuk menjamin ketersediaan dari beberapa Pod identik dalam jumlah tertentu. 




<!-- body -->

## Cara kerja ReplicaSet

Sebuah ReplicaSet didefinisikan dengan beberapa _field_ termasuk selektor yang menentukan bagaimana mengidentifikasi Pod yang dapat diakuisisi, jumlah replika yang mengindikasi berapa jumlah Pod yang harus dikelola, dan sebuah templat pod yang menentukan data dari berbagai Pod baru yang harus dibuat untuk memenuhi kriteria jumlah replika. Sebuah ReplicaSet selanjutnya akan memenuhi tujuannya dengan membuat dan menghapus Pod sesuai dengan kebutuhan untuk mencapai jumlah yang diinginkan. Ketika ReplicaSet butuh untuk membuat Pod baru, templat Pod akan digunakan.

Tautan dari sebuah ReplicaSet terhadap Pod yang dimiliki adalah melalui _field_ [metadata.ownerReferences](https://kubernetes.io/docs/concepts/workloads/controllers/garbage-collection/#owners-and-dependents) pada Pod, yang menentukan sumber daya yang dimiliki oleh objek saat ini. Semua Pod yang diakuisisi oleh sebuah ReplicaSet masing-masing memiliki informasi yang mengidentifikasi ReplicaSet dalam _field_ ownerReferences. Melalui tautan ini ReplicaSet dapat mengetahui keadaan dari Pod yang sedang dikelola dan melakukan perencanaan yang sesuai.

Sebuah ReplicaSet mengidentifikasi Pod baru untuk diakuisisi menggunakan selektornya. Jika terdapat sebuah Pod yang tidak memiliki OwnerReference atau OwnerReference yang dimiliki bukanlah sebuah [_Controller_](https://kubernetes.io/docs/concepts/architecture/controller) dan sesuai dengan selektor dari ReplicaSet, maka Pod akan langsung diakuisisi oleh ReplicaSet tersebut.

## Kapan menggunakan ReplicaSet

Sebuah ReplicaSet memastikan replika-replika pod dalam jumlah yang ditentukan berjalan pada satu waktu tertentu. Namun demikian, sebuah Deployment adalah konsep dengan tingkatan yang lebih tinggi yang mengatur ReplicaSet dan mengubah Pod secara deklaratif serta berbagai fitur bermanfaat lainnya. Maka dari itu, kami merekomendasikan untuk menggunakan Deployment alih-alih menggunakan ReplicaSet secara langsung, kecuali jika kamu membutuhkan orkestrasi pembaruan yang khusus atau tidak membutuhkan pembaruan sama sekali.

Hal ini berarti kamu boleh jadi tidak akan membutuhkan manipulasi objek ReplicaSet: Gunakan Deployment dan definisikan aplikasi kamu pada bagian _spec_. 

## Contoh

{{< codenew file="controllers/frontend.yaml" >}}

Menyimpan _manifest_ ini dalam `frontend.yaml` dan mengirimkannya ke klaster Kubernetes akan membuat ReplicaSet yang telah didefinisikan beserta dengan Pod yang dikelola.

```shell
kubectl apply -f https://kubernetes.io/examples/controllers/frontend.yaml
```

Selanjutnya kamu bisa mendapatkan ReplicaSet yang sedang di-_deploy_:
```shell
kubectl get rs
```

Dan melihat _frontend_ yang telah dibuat:
```shell
NAME       DESIRED   CURRENT   READY   AGE
frontend   3         3         3       6s
```

Kamu juga dapat memeriksa kondisi dari ReplicaSet:
```shell
kubectl describe rs/frontend
```

Dan kamu akan melihat keluaran yang serupa dengan:
```shell
Name:		frontend
Namespace:	default
Selector:	tier=frontend,tier in (frontend)
Labels:		app=guestbook
		tier=frontend
Annotations:	<none>
Replicas:	3 current / 3 desired
Pods Status:	3 Running / 0 Waiting / 0 Succeeded / 0 Failed
Pod Template:
  Labels:       app=guestbook
                tier=frontend
  Containers:
   php-redis:
    Image:      gcr.io/google_samples/gb-frontend:v3
    Port:       80/TCP
    Requests:
      cpu:      100m
      memory:   100Mi
    Environment:
      GET_HOSTS_FROM:   dns
    Mounts:             <none>
  Volumes:              <none>
Events:
  FirstSeen    LastSeen    Count    From                SubobjectPath    Type        Reason            Message
  ---------    --------    -----    ----                -------------    --------    ------            -------
  1m           1m          1        {replicaset-controller }             Normal      SuccessfulCreate  Created pod: frontend-qhloh
  1m           1m          1        {replicaset-controller }             Normal      SuccessfulCreate  Created pod: frontend-dnjpy
  1m           1m          1        {replicaset-controller }             Normal      SuccessfulCreate  Created pod: frontend-9si5l
```

Terakhir, kamu dapat memeriksa Pod yang dibawa:
```shell
kubectl get Pods
```

Kamu akan melihat informasi Pod yang serupa dengan:
```shell
NAME             READY     STATUS    RESTARTS   AGE
frontend-9si5l   1/1       Running   0          1m
frontend-dnjpy   1/1       Running   0          1m
frontend-qhloh   1/1       Running   0          1m
```

Kamu juga dapat memastikan bahwa referensi pemilik dari pod-pod ini telah disesuaikan terhadap ReplicaSet _frontend_.
Untuk melakukannya, _yaml_ dari Pod yang sedang berjalan bisa didapatkan dengan:
```shell
kubectl get pods frontend-9si5l -o yaml
```

Keluarannya akan terlihat serupa dengan contoh berikut ini, dengan informasi ReplicaSet _frontend_ yang ditentukan pada _field_ ownerReferences pada bagian metadata:
```shell
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: 2019-01-31T17:20:41Z
  generateName: frontend-
  labels:
    tier: frontend
  name: frontend-9si5l
  namespace: default
  ownerReferences:
  - apiVersion: extensions/v1beta1
    blockOwnerDeletion: true
    controller: true
    kind: ReplicaSet
    name: frontend
    uid: 892a2330-257c-11e9-aecd-025000000001
...
```

## Akuisisi Pod Non-Templat

Walaupun kamu bisa membuat Pod biasa tanpa masalah, sangat direkomendasikan untuk memastikan Pod tersebut tidak memiliki label yang sama dengan selektor dari salah satu ReplicaSet yang kamu miliki. Hal in disebabkan sebuah ReplicaSet tidak dibatasi untuk memilki Pod sesuai dengan templatnya -- ReplicaSet dapat mengakuisisi Pod lain dengan cara yang telah dijelaskan pada bagian sebelumnya. 

Mengambil contoh ReplicaSet _frontend_ sebelumnya, dan Pod yang ditentukan pada _manifest_ berikut: 

{{< codenew file="pods/pod-rs.yaml" >}}

Karena Pod tersebut tidak memiliki Controller (atau objek lain) sebagai referensi pemilik yang sesuai dengan selektor dari ReplicaSet _frontend_, Pod tersebut akan langsung diakuisisi oleh ReplicaSet.

Misalkan kamu membuat Pod tersebut setelah ReplicaSet _frontend_ telah di-_deploy_ dan telah mengkonfigurasi replika Pod awal untuk memenuhi kebutuhan jumlah replika:

```shell
kubectl apply -f https://kubernetes.io/examples/pods/pod-rs.yaml
```

Pod baru akan diakuisisi oleh ReplicaSet, dan setelah itu langsung diterminasi ketika ReplicaSet melebihi jumlah yang diinginkan.

Memperoleh Pod:
```shell
kubectl get Pods
```

Keluaran menunjukkan bahwa Pod baru dalam keaadan telah diterminasi, atau sedang dalam proses terminasi:
```shell
NAME             READY   STATUS        RESTARTS   AGE
frontend-9si5l   1/1     Running       0          1m
frontend-dnjpy   1/1     Running       0          1m
frontend-qhloh   1/1     Running       0          1m
pod2             0/1     Terminating   0          4s
```

Jika kamu membuat Pod terlebih dahulu:
```shell
kubectl apply -f https://kubernetes.io/examples/pods/pod-rs.yaml
```

Dan selanjutnya membuat ReplicaSet maka:
```shell
kubectl apply -f https://kubernetes.io/examples/controllers/frontend.yaml
```

Kamu akan melihat bahwa ReplicaSet telah mengakuisisi Pod dan hanya membuat Pod yang baru sesuai dengan `spec` yang ditentukan hingga jumlah dari Pod yang baru dan yang orisinil sesuai dengan jumlah yang diinginkan. Dengan memperoleh Pod: 
```shell
kubectl get Pods
```

Akan diperlihatkan pada keluarannya:
```shell
NAME             READY   STATUS    RESTARTS   AGE
frontend-pxj4r   1/1     Running   0          5s
pod1             1/1     Running   0          13s
pod2             1/1     Running   0          13s
```

Dengan cara ini, sebuah ReplicaSet dapat memiliki himpunan berbagai Pod yang tidak homogen.

## Menulis _manifest_ ReplicaSet

Seperti objek API Kubernetes lainnya, sebuah ReplicaSet membutuhkan _field_ `apiVersion`, `kind`, dan `metadata`. Untuk ReplicaSet, nilai dari `kind` yang memungkinkan hanyalah ReplicaSet. Pada Kubernetes 1.9 versi API `apps/v1` pada `kind` ReplicaSet adalah versi saat ini dan diaktifkan secara _default_. Versi API `apps/v1beta2` telah dideprekasi. Lihat baris-baris awal pada contoh `frontend.yaml` untuk petunjuk.

Sebuah ReplicaSet juga membutuhkan [bagian `.spec`](https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status).

### Templat Pod

`.spec.template` adalah sebuah [templat pod](/docs/concepts/workloads/Pods/pod-overview/#pod-templates) yang juga dibutuhkan untuk mempunyai label. Pada contoh `frontend.yaml` kita memiliki satu label: `tier: frontend`. 
Hati-hati agar tidak tumpang tindih dengan selektor dari _controller_ lain, agar mereka tidak mencoba untuk mengadopsi Pod ini.

Untuk _field_ [_restart policy_](/docs/concepts/workloads/Pods/pod-lifecycle/#restart-policy) dari templat, `.spec.template.spec.restartPolicy`, nilai yang diperbolehkan hanyalah `Always`, yang merupakan nilai _default_. 

### Selektor Pod

_Field_ `.spec.selector` adalah sebuah [selektor labe](/id/docs/concepts/overview/working-with-objects/labels/). Seperti yang telah dibahas [sebelumnya](#how-a-replicaset-works), _field_ ini adalah label yang digunakan untuk mengidentifikasi Pod yang memungkinkan untuk diakuisisi. Pada contoh `frontend.yaml`, selektornya adalah:
```shell
matchLabels:
	tier: frontend
```

Pada ReplicaSet, `.spec.template.metadata.labels` harus memiliki nilai yang sama dengan `spec.selector`, atau akan ditolak oleh API.

{{< note >}}
Untuk 2 ReplicaSet dengan nilai `.spec.selector` yang sama tetapi memiliki nilai yang berbeda pada _field_ `.spec.template.metadata.labels` dan `.spec.template.spec`, setiap ReplicaSet akan mengabaikan Pod yang dibuat oleh ReplicaSet lain.
{{< /note >}}

### Replika

Kamu dapat menentukan jumlah Pod yang seharusnya berjalan secara konkuren dengan mengatur nilai dari `.spec.replicas`. ReplicaSet akan membuat/menghapus Pod-nya hingga jumlahnya sesuai dengan _field_ ini.

Jika nilai `.spec.replicas` tidak ditentukan maka akan diatur ke nilai _default_ 1. 

## Menggunakan ReplicaSet

### Menghapus ReplicaSet dan Pod-nya

Untuk menghapus sebuah ReplicaSet beserta dengan Pod-nya, gunakan [`kubectl delete`](/docs/reference/generated/kubectl/kubectl-commands#delete). [_Garbage collector_](/id/docs/concepts/workloads/controllers/garbage-collection/) secara otomatis akan menghapus semua Pod dependen secara _default_.

Ketika menggunakan REST API atau _library_ `client-go`, kamu harus mengatur nilai `propagationPolicy` menjadi `Background` atau `Foreground` pada opsi -d.
Sebagai contoh:
```shell
kubectl proxy --port=8080
curl -X DELETE  'localhost:8080/apis/extensions/v1beta1/namespaces/default/replicasets/frontend' \
> -d '{"kind":"DeleteOptions","apiVersion":"v1","propagationPolicy":"Foreground"}' \
> -H "Content-Type: application/json"
```

### Menghapus hanya ReplicaSet

Kamu dapat menghapus ReplicaSet tanpa memengaruhi Pod-nya menggunakan [`kubectl delete`](/docs/reference/generated/kubectl/kubectl-commands#delete) dengan menggunakan opsi `--cascade=orphan`.
Ketika menggunakan REST API atau _library_ `client-go`, kamu harus mengatur nilai `propagationPolicy` menjadi `Orphan`.
Sebagai contoh:
```shell
kubectl proxy --port=8080
curl -X DELETE  'localhost:8080/apis/extensions/v1beta1/namespaces/default/replicasets/frontend' \
> -d '{"kind":"DeleteOptions","apiVersion":"v1","propagationPolicy":"Orphan"}' \
> -H "Content-Type: application/json"
```

Ketika ReplicaSet yang asli telah dihapus, kamu dapat membuat ReplicaSet baru untuk menggantikannya. Selama _field_ `.spec.selector` yang lama dan baru memilki nilai yang sama, maka ReplicaSet baru akan mengadopsi Pod lama namun tidak serta merta membuat Pod yang sudah ada sama dan sesuai dengan templat Pod yang baru.
Untuk memperbarui Pod dengan _spec_ baru dapat menggunakan [Deployment](/id/docs/concepts/workloads/controllers/deployment/#creating-a-deployment) karena ReplicaSet tidak mendukung pembaruan secara langsung.

### Mengisolasi Pod dari ReplicaSet

Kamu dapat menghapus Pod dari ReplicaSet dengan mengubah nilai labelnya. Cara ini dapat digunakan untuk menghapus Pod dari servis untuk keperluan _debugging_, _data recovery_, dan lainnya. Pod yang dihapus dengan cara ini akan digantikan seecara otomatis (dengan asumsi jumlah replika juga tidak berubah).

### Mengatur jumlah Pod pada ReplicaSet

Jumlah Pod pada ReplicaSet dapat diatur dengan mengubah nilai dari _field_ `.spec.replicas`. Pengatur ReplicaSet akan memastikan Pod dengan jumlah yang telah ditentukan dan dengan nilai selektor yang sama sedang dalam keadaan berjalan. 

### Pengaturan jumlah Pod pada ReplicaSet menggunakan Horizontal Pod Autoscaler

Pengaturan jumlah Pod pada ReplicaSet juga dapat dilakukan mengunakan [Horizontal Pod Autoscalers (HPA)](/docs/tasks/run-application/horizontal-pod-autoscale/). Berikut adalah contoh HPA terhadap ReplicaSet yang telah dibuat pada contoh sebelumnya.

{{< codenew file="controllers/hpa-rs.yaml" >}}

Menyimpan _manifest_ ini dalam `hpa-rs.yaml` dan mengirimkannya ke klaster Kubernetes akan membuat HPA tersebut yang akan mengatur jumlah Pod pada ReplicaSet yang telah didefinisikan bergantung terhadap penggunaan CPU dari Pod yang direplikasi.

```shell
kubectl apply -f https://k8s.io/examples/controllers/hpa-rs.yaml
```

Opsi lainnya adalah dengan menggunakan perintah `kubectl autoscale` untuk tujuan yang sama. 

```shell
kubectl autoscale rs frontend --max=10
```

## Alternatif selain ReplicaSet

### Deployment (direkomendasikan)

[`Deployment`](/id/docs/concepts/workloads/controllers/deployment/) adalah sebuah objek yang bisa memiliki ReplicaSet dan memperbarui ReplicaSet dan Pod-nya melalui _rolling update_ deklaratif dan _server-side_.
Walaupun ReplicaSet dapat digunakan secara independen, seringkali ReplicaSet digunakan oleh Deployments sebagai mekanisme untuk mengorkestrasi pembuatan, penghapusan dan pembaruan Pod. Ketika kamu menggunakan Deployments kamu tidak perlu khawatir akan pengaturan dari ReplicaSet yang dibuat. Deployments memiliki dan mengatur ReplicaSet-nya sendiri.
Maka dari itu penggunaan Deployments direkomendasikan jika kamu menginginkan ReplicaSet.

### Pod sederhana

Tidak seperti pada kasus ketika pengguna secara langsung membuat Pod, ReplicaSet akan menggantikan Pod yang dihapus atau diterminasi dengan alasan apapun, seperti pada kasus dimana terjadi kegagalan _node_ atau pemeliharaan _node_ yang disruptif, seperti pada kasus _upgrade_ kernel. Karena alasan ini kami merekomendasikan kamu untuk menggunakan ReplicaSet walaupun jika aplikasimu membutuhkan hanya satu Pod. Hal ini mirip dengan pengawas proses, hanya saja pada kasus ini mengawasi banyak Pod pada berbagai _node_ alih-alih berbagai proses individu pada sebuah _node_. ReplicaSet mendelegasikan proses pengulangan kembali dari kontainer lokal kepada agen yang terdapat di _node_ (sebagai contoh, Kubelet atau Docker).

### Job

Gunakan [`Job`](/docs/concepts/jobs/run-to-completion-finite-workloads/) alih-alih ReplicaSet untuk Pod yang diharapkan untuk diterminasi secara sendirinya. 

### DaemonSet

Gunakan [`DaemonSet`](/id/docs/concepts/workloads/controllers/daemonset/) alih-alih ReplicaSet untuk Pod yang menyediakan fungsi pada level mesin, seperti _monitoring_ mesin atau _logging_ mesin. Pod ini memiliki waktu hidup yang bergantung terhadap waktu hidup mesin: Pod perlu untuk berjalan pada mesin sebelum Pod lain dijalankan, dan aman untuk diterminasi ketika mesin siap untuk di-_reboot_ atau dimatikan. 

### ReplicationController

ReplicaSet adalah suksesor dari [_ReplicationControllers_](/id/docs/concepts/workloads/controllers/replicationcontroller/). Keduanya memenuhi tujuan yang sama dan memiliki perilaku yang serupa, kecuali bahwa ReplicationController tidak mendukung kebutuhan selektor _set-based_ seperti yang dijelaskan pada [panduan penggunaan label](/id/docs/concepts/overview/working-with-objects/labels/#label-selectors). Pada kasus tersebut, ReplicaSet lebih direkomendasikan dibandingkan ReplicationController.

