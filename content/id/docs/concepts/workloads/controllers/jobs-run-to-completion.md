---
title: Job - Dijalankan Hingga Selesai
content_type: concept
feature:
  title: Eksekusi batch
  description: >
    Selain Service, Kubernetes juga dapat melakukan manajemen workload batch dan CI, melakukan penggantian Container-Container yang gagal, jika diinginkan.
weight: 70
---

<!-- overview -->

Sebuah Job membuat satu atau beberapa Pod dan menjamin bahwa jumlah Pod yang telah dispesifikasikan sebelumnya 
berhasil dijalankan. Pada saat Pod telah dihentikan, Job akan menandainya sebagai Job yang sudah berhasil dijalankan.
Ketika jumlah sukses yang dispesifikasikan sebelumnya sudah terpenuhi, maka Job tersebut dianggap selesai. 
Menghapus sebuah Job akan menghapus semua Pod yang dibuat oleh Job tersebut.

Sebuah kasus sederhana yang dapat diberikan adalah membuat sebuah objek Job untuk menjamin 
sebuah Pod dijalankan hingga selesai. Objek Job ini akan membuat sebuah Pod baru apabila 
Pod pertama gagal atau dihapus (salah satu contohnya adalah akibat adanya kegagalan pada 
perangkat keras atau terjadinya _reboot_ pada Node).

Kamu juga dapat menggunakan Job untuk menjalankan beberapa Pod secara paralel.




<!-- body -->

## Menjalankan Contoh Job

Berikut merupakan contoh konfigurasi Job. Job ini melakukan komputasi π hingga 
digit ke 2000 kemudian memberikan hasilnya sebagai keluaran. Job tersebut memerlukan 
waktu 10 detik untuk dapat diselesaikan.

{{< codenew file="controllers/job.yaml" >}}

Kamu dapat menjalankan contoh tersebut dengan menjalankan perintah berikut:

```shell
kubectl apply -f https://k8s.io/examples/controllers/job.yaml
```
```
job "pi" created
```

Perhatikan status dari Job yang baru dibuat dengan menggunakan perintah`kubectl`:

```shell
kubectl describe jobs/pi
```
```
Name:             pi
Namespace:        default
Selector:         controller-uid=b1db589a-2c8d-11e6-b324-0209dc45a495
Labels:           controller-uid=b1db589a-2c8d-11e6-b324-0209dc45a495
                  job-name=pi
Annotations:      <none>
Parallelism:      1
Completions:      1
Start Time:       Tue, 07 Jun 2016 10:56:16 +0200
Pods Statuses:    0 Running / 1 Succeeded / 0 Failed
Pod Template:
  Labels:       controller-uid=b1db589a-2c8d-11e6-b324-0209dc45a495
                job-name=pi
  Containers:
   pi:
    Image:      perl
    Port:
    Command:
      perl
      -Mbignum=bpi
      -wle
      print bpi(2000)
    Environment:        <none>
    Mounts:             <none>
  Volumes:              <none>
Events:
  FirstSeen    LastSeen    Count    From            SubobjectPath    Type        Reason            Message
  ---------    --------    -----    ----            -------------    --------    ------            -------
  1m           1m          1        {job-controller }                Normal      SuccessfulCreate  Created pod: pi-dtn4q
```

Untuk melihat Pod yang sudah selesai dari sebuah Job, kamu dapat menggunakan perintah `kubectl get pods`.

Untuk menampilkan semua Pod yang merupakan bagian dari suatu Job di mesin kamu dalam bentuk 
yang mudah dipahami, kamu dapat menggunakan perintah berikut ini:

```shell
pods=$(kubectl get pods --selector=job-name=pi --output=jsonpath='{.items[*].metadata.name}')
echo $pods
```
```
pi-aiw0a
```

Disini, selektor yang ada merupakan selektor yang sama dengan yang ada pada Job. 
Opsi `--output=jsonpath` menspesifikasikan bahwa ekspresi yang hanya 
menampilkan nama dari setiap Pod pada _list_ yang dikembalikan.

Untuk melihat keluaran standar dari salah satu pod:

```shell
kubectl logs $pods
```
Keluaran yang dihasilkan akan sama dengan:
```shell
3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679821480865132823066470938446095505822317253594081284811174502841027019385211055596446229489549303819644288109756659334461284756482337867831652712019091456485669234603486104543266482133936072602491412737245870066063155881748815209209628292540917153643678925903600113305305488204665213841469519415116094330572703657595919530921861173819326117931051185480744623799627495673518857527248912279381830119491298336733624406566430860213949463952247371907021798609437027705392171762931767523846748184676694051320005681271452635608277857713427577896091736371787214684409012249534301465495853710507922796892589235420199561121290219608640344181598136297747713099605187072113499999983729780499510597317328160963185950244594553469083026425223082533446850352619311881710100031378387528865875332083814206171776691473035982534904287554687311595628638823537875937519577818577805321712268066130019278766111959092164201989380952572010654858632788659361533818279682303019520353018529689957736225994138912497217752834791315155748572424541506959508295331168617278558890750983817546374649393192550604009277016711390098488240128583616035637076601047101819429555961989467678374494482553797747268471040475346462080466842590694912933136770289891521047521620569660240580381501935112533824300355876402474964732639141992726042699227967823547816360093417216412199245863150302861829745557067498385054945885869269956909272107975093029553211653449872027559602364806654991198818347977535663698074265425278625518184175746728909777727938000816470600161452491921732172147723501414419735685481613611573525521334757418494684385233239073941433345477624168625189835694855620992192221842725502542568876717904946016534668049886272327917860857843838279679766814541009538837863609506800642251252051173929848960841284886269456042419652850222106611863067442786220391949450471237137869609563643719172874677646575739624138908658326459958133904780275901
```

## Menulis Spek Job

Sama halnya dengan konfigurasi Kubernetes lainnya, sebuah Job memerlukan _field_
`apiVersion`, `kind`, dan `metadata`.

Sebuah Job juga membutuhkan sebuah [bagian `.spec`](https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status).

### Templat Pod

_Field_ `.spec.template` merupakan satu-satunya _field_ wajib pada `.spec`.

_Field_  `.spec.template` merupakan sebuah [templat Pod](/id/docs/concepts/workloads/pods/pod-overview/#pod-templates). _Field_ ini memiliki skema yang sama dengan yang ada pada [Pod](/docs/user-guide/pods), 
kecuali _field_ ini bersifat _nested_ dan tidak memiliki _field_ `apiVersion` atau _field_ `kind`.

Sebagai tambahan dari _field_ wajib pada sebuah Job, sebuah tempat pod pada Job 
haruslah menspesifikasikan label yang sesuai (perhatikan [selektor pod](#pod-selektor)) 
dan sebuah mekanisme _restart_ yang sesuai.

Hanya sebuah [`RestartPolicy`](/id/docs/concepts/workloads/pods/pod-lifecycle/#restart-policy) yang sesuai dengan `Never` atau `OnFailure` yang bersifat valid.

### Selektor Pod

_Field_ `.spec.selector` bersifat opsional. Dan dalam sebagian besar kasus, kamu tidak perlu memberikan 
spesifikasi untuk hal ini. Perhatikan bagian [menspesifikasikan selektor Pod kamu sendiri](#menspesifikasikan-selektor-pod-kamu-sendiri).

### Job Paralel

Terdapat tiga jenis utama dari _task_ yang sesuai untuk dijalankan sebagai sebuah Job:

1. Job non-paralel
  - secara umum, hanya sebuah Pod yang dimulai, kecuali jika Pod tersebut gagal.
  - Job akan dianggap sudah selesai dikerjakan apabila Pod dari Job tersebut sudah selesai dijalankan dan mengalami terminasi dengan status sukses.
1. Job paralel dengan *jumlah nilai penyelesaian tetap*:
  - berikan spesifikasi pada `.spec.completions` dengan nilai non-negatif.
  - Job yang ada merupakan representasi dari _task_ yang dikerjakan, dan akan dianggap selesai apabila terdapat lebih dari satu Pod yang sukses untuk setiap nilai yang ada dalam jangkauan 1 hingga `.spec.completions`.
  - **belum diimplementasikan saat ini:** Setiap Pod diberikan nilai indeks yang berbeda di dalam jangkauan 1 hingga `.spec.completions`.
1. Job paralel dengan sebuah *_work queue_*:
  - jangan berikan spesifikasi pada `.spec.completions`, nilai _default_-nya merupakan `.spec.parallelism`.
  - Pod yang ada haruslah dapat berkoordinasi satu sama lain atau dengan Service eksternal lain untuk menentukan apa yang setiap Pod tadi perlu lakukan. Sebagai contohnya, sebuah Pod bisa saja melakukan _fetch_ job _batch_ hingga N kali pada _work queue_
  - setiap Pod secara independen mampu menentukan apakah Pod lainnya telah menyelesaikan tugasnya dengan baik atau belum, dengan kata lain suatu Job telah dikatakan selesai
  - ketika Pod mana pun dari sebuah Job berhenti dalam keadaan sukses, maka tidak ada Pod lain yang akan dibuat untuk Job tersebut.
  - apabila salah satu Pod sudah dihentikan sekali dalam keadaan sukses, maka Job akan ditandai sebagai sukses.
  - apabila sebuah Pod sudah dihentikan dalam keadaan sukses, tidak boleh ada Pod lain yang mengerjakan _task_ tersebut. Dengan kata lain, semua Pod tersebut haruslah dalam keadaan akan dihentikan.

Untuk sebuah Job yang non-paralel, kamu tidak perlu menspesifikasikan _field_ `.spec.completions` dan `.spec.parallelism`. Ketika kedua _field_ tersebut 
dalam keadaan tidak dispesifikasikan, maka nilai _defult_-nya akan diubah menjadi 1.

Untuk sebuah Job dengan jumlah nilai penyelesaian tetap, kamu harus memberikan spesifikasi nilai 
dari `.spec.completions` dengan nilai yang diinginkan. Kamu dapat menspesifikasikan `.spec.parallelism`, 
atau jika kamu tidak melakukannya nilai dari _field_ ini akan memiliki nilai default 1.

Untuk sebuah Job _work queue_, kamu harus meninggalkan spesifikasi _field_ `.spec.completions` menjadi kosong, serta 
memberikan nilai pada `.spec.parallelism` menjadi sebuah bilangan bulat non negatif.

Untuk informasi lebih lanjut mengenai bagaimana menggunakan Job dengan jenis yang berbeda, kamu 
dapat melihat bagian [pola job](#pola-job).


#### Mengendalikan Paralelisme

Paralelisme yang diminta (`.spec.parallelism`) dapat diaktifkan dengan cara 
memberikan nilai bilangan bulat non-negatif. Jika tidak dispesifikasikan maka nilainya akan 
secara default yaitu 1. Jika dispesifikasikan sebagai 0, maka Job akan secara otomatis dihentikan sementara 
hingga nilainya dinaikkan.

Paralelisme yang sebenarnya (jumlah Pod yang dijalankan pada satu waktu tertentu) 
bisa saja lebih atau kurang dari nilai yang diharapkan karena adanya alasan berikut:

- Untuk Job _fixed completion count_, nilai sebenarnya dari jumlah Pod yang dijalankan secara paralel tidak akan melebihi jumlah  
  _completion_ yang tersisa. Nilai yang lebih tinggi dari `.spec.parallelism` secara efektif, akan diabaikan.
- Untuk Job _work queue_, tidak akan ada Pod yang dimulai setelah ada Pod yang berhasil -- meskipun begitu, sisa Pod yang ada akan diizinkan untuk menyelesaikan tugasnya.
- Jika sebuah {{< glossary_tooltip term_id="controller" >}} Job tidak memiliki waktu untuk memberikan reaksi.
- Jika sebuah _controller_ Job gagal membuat Pod dengan alasan apa pun (kurangnya `ResourceQuota`, kurangnya _permission_, dkk.),
  maka bisa saja terdapat lebih sedikit Pod dari yang diminta.
- Jika _controller_ Job melakukan _throttle_ pembuatan Pod karena terdapat gagalnya pembuatan Pod yang berlebihan sebelumnya pada Job yang sama.
- Ketika sebuah Pod dihentikan secara _graceful_, maka Pod tersebut akan membutuhkan waktu untuk berhenti.

## Mengatasi Kegagalan Pod dan Container 

Sebuah Container pada sebuah Pod bisa saja mengalami kegagalan karena berbagai alasan 
yang berbeda, misalnya saja karena proses yang ada di dalamnya berakhir dengan _exit code_ 
yang tidak sama dengan nol, atau Container yang ada di-_kill_ karena menyalahi batasan memori, dkk. 
Jika hal ini terjadi, dan `.spec.template.spec.restartPolicy = "OnFailure"`, maka Pod 
akan tetap ada di dalam node, tetapi Container tersebut akan dijalankan kembali. Dengan demikian, 
program kamu harus dapat mengatasi kasus dimana program tersebut di-_restart_ secara lokal, atau jika 
tidak maka spesifikasikan `.spec.template.spec.restartPolicy = "Never"`. Perhatikan 
[_lifecycle_ pod](/id/docs/concepts/workloads/pods/pod-lifecycle/#example-states) untuk informasi lebih lanjut mengenai `restartPolicy`.

Sebuah Pod juga dapat gagal secara menyeluruh, untuk beberapa alasan yang mungkin, misalnya saja, 
ketika Pod tersebut dipindahkan dari Node (ketika Node diperbarui, di-_restart_, dihapus, dsb.), atau 
jika sebuah Container dalam Pod gagal dan `.spec.template.spec.restartPolicy = "Never"`. Ketika 
sebuah Pod gagal, maka _controller_ Job akan membuat sebuah Pod baru. Ini berarti aplikasi kamu haruslah 
bisa mengatasi kasus dimana aplikasimu dimulai pada Pod yang baru. Secara khusus apabila aplikasi kamu 
berurusan dengan berkas temporer, _locks_, keluaran yang tak lengkap dan hal-hal terkait dengan 
program yang dijalankan sebelumnya.

Perhatikan bahwa bahakan apabila kamu menspesifikasikan `.spec.parallelism = 1` dan `.spec.completions = 1` dan 
`.spec.template.spec.restartPolicy = "Never"`, program yang sama bisa saja tetap dijalankan lebih dari sekali.

Jika kamu menspesifikasikan `.spec.parallelism` dan `.spec.completions` dengan nilai yang lebih besar dari 1, 
maka bisa saja terdapat keadaan dimana terdapat beberapa Pod yang dijalankan pada waktu yang sama. 
Dengan demikian, Pod kamu haruslah fleksibel terhadap adanya konkurensi.

### Mekanisme Kebijakan _Backoff_ apabila Terjadi Kegagalan

Terdapat situasi dimana kamu ingin membuat suatu Job gagal 
setelah dijalankan mekanisme _retry_ beberapa kali akibat adanya kesalahan pada konfigurasi 
dsb. Untuk melakukan hal tersebut, spesifikasikan `.spec.backoffLimit` dengan nilai _retry_ yang diinginkan 
sebelum menerjemahkan Job dalam keadaan gagal. Secara default, nilai dari _field_ tersebut adalah 6.
Pod yang gagal dijalankan dan terkait dengan suatu Job tertentu akan dibuat kembali oleh 
_controller_ Job dengan _delay_ _back-off_ eksponensial (10 detik, 20 detik, 40 detik ...) 
yang dibatasi pada 6 menit. Penghitungan _back-off_ akan diulang jika tidak terdapat Pod baru yang gagal 
sebelum siklus pengecekan status Job selanjutnya.

{{< note >}}
Isu [#54870](https://github.com/kubernetes/kubernetes/issues/54870) masih ada untuk versi Kubernetes sebelum 1.12. 
{{< /note >}}
{{< note >}}
Jika Job yang kamu miliki memiliki `restartPolicy = "OnFailure"`, perhatikan bahwa Container kamu yang menjalankan 
Job tersebut akan dihentikan ketika limit _back-off_ telah dicapai. Hal ini akan membuat proses _debugging_ semakin sulit. 
Dengan demikian, kami memberikan saran untuk menspesifikasikan `restartPolicy = "Never"` ketika melakukan 
proses _debugging_ atau menggunakan mekanisme _logging_ untuk menjamin keluaran 
dari Job yang gagal agar tidak terus menerus hilang.
{{< /note >}}

## Terminasi dan _Clean Up_ Job

Ketika sebuah Job selesai dijalankan, tidak akan ada lagi Pod yang dibuat, 
meskipun begitu Pod yang ada juga tidak akan dihapus. Dengan demikian kamu masih bisa mengakses log 
yang ada dari Pod yang sudah dalam status _complete_ untuk mengecek apabila terjadi eror, _warning_, atau hal-hal 
yang dapat digunakan untuk proses pelaporan dan identifikasi. Objek Job itu sendiri akan tetap ada, 
sehingga kamu tetap bisa melihat statusnya. Penghapusan objek akan diserahkan sepenuhnya pada pengguna 
apabila Job tidak lagi digunakan. Penghapusan Job dengan perintah `kubectl` (misalnya, `kubectl delete jobs/pi` atau `kubectl delete -f ./job.yaml`). 
Ketika kamu menghapus Job menggunakan perintah `kubectl`, semua Pod yang terkait dengan Job tersebut akan ikut dihapus.

Secara _default_, sebuah Job akan dijalankan tanpa adanya interupsi kecuali terdapat Pod yang gagal,  (`restartPolicy=Never`) atau terdapat 
Container yang dihentikan dalam kondisi error (`restartPolicy=OnFailure`), suatu keadaan dimana Job akan dijalankan dengan mekanisme 
yang dijelaskan di atas berdasarkan pada `.spec.backoffLimit`. 
Apabila `.spec.backoffLimit` telah mencapai limit, maka Job akan ditandai sebagai gagal dan Pod yang saat ini sedang dijalankan juga akan dihentikan.

Cara lain untuk menghentikan sebuah Job adalah dengan mengatur _deadline_ aktif. 
Untuk melakukannya kamu dapat menspesifikasikan _field_ `.spec.activeDeadlineSeconds` 
dari sebuah Job dengan suatu angka dalam satuan detik. _Field_ `activeDeadlineSeconds` 
diterapkan pada durasi dari sebuah Job, tidak peduli seberapa banyak Pod yang dibuat. 
Setelah sebuah Job mencapai limit `activeDeadlineSeconds`, semua Pod yang dijalankan akan dihentikan 
dan status dari Job tersebut akan berubah menjadi `type: Failed` dengan `reason: DeadlineExceeded`.

Perhatikan bahwa _field_ `.spec.activeDeadlineSeconds` pada Job memiliki tingkat 
presedensi di atas `.spec.backoffLimit`. Dengan demikian, sebuah Job 
yang sedang mencoba melakukan _restart_ pada suatu Pod-nya tidak akan melakukan 
pembuatan Pod yang baru apabila Job tersebut telah mencapai limit yang didefinisikan pada 
`activeDeadlineSeconds`, bahkan apabila nilai dari `backoffLimit` belum tercapai.

Contoh:

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: pi-with-timeout
spec:
  backoffLimit: 5
  activeDeadlineSeconds: 100
  template:
    spec:
      Containers:
      - name: pi
        image: perl
        command: ["perl",  "-Mbignum=bpi", "-wle", "print bpi(2000)"]
      restartPolicy: Never
```

Perhatikan bahwa baik spek Job dan [spek templat Pod](/docs/concepts/workloads/pods/init-Containers/#detailed-behavior) di dalam Job memiliki _field_ `activeDeadlineSeconds`. 
Pastikan kamu telah menspesifikasikan nilai tersebut pada level yang dibutuhkan.

## Mekanisme _Clean Up_ Otomatis pada Job yang Sudah Selesai

Job yang sudah selesai biasanya tidak lagi dibutuhkan di dalam sistem. Tetap menjaga keberadaan 
objek-objek tersebut di dalam sistem akan memberikan tekanan tambahan pada API server. Jika sebuah Job 
yang diatur secara langsung oleh _controller_ dengan level yang lebih tinggi, seperti 
[CronJob](/id/docs/concepts/workloads/controllers/cron-jobs/), maka Job ini dapat 
di-_clean up_ oleh CronJob berdasarkan _policy_ berbasis kapasitas yang dispesifikasikan.

### Mekanisme TTL untuk Job yang Telah Selesai Dijalankan

{{< feature-state for_k8s_version="v1.12" state="alpha" >}}

Salah satu cara untuk melakukan _clean up_ Job yang telah selesai dijalankan
(baik dengan status `Complete` atau `Failed`) secara otomatis adalah dengan 
menerapkan mekanisme TTL yang disediakan oleh 
[_controller_ TTL](/id/docs/concepts/workloads/controllers/ttlafterfinished/) untuk 
sumber daya yang telah selesai digunakan, dengan cara menspesifikasikan 
_field_ `.spec.ttlSecondsAfterFinished` dari Job tersebut.

Ketika _controller_ TTL melakukan proses _clean up_ pada Job,
 maka _controller_ tersebut akan menghapus objek-objek terkait seperti Pod, serta Job itu sendiri. 
 Perhatikan bahwa ketika suatu Job dihapus, maka _lifecycle_-nya akan menjamin, mekanisme 
 _finalizer_ yang ada akan tetap dihargai.

Sebagai contoh:

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: pi-with-ttl
spec:
  ttlSecondsAfterFinished: 100
  template:
    spec:
      Containers:
      - name: pi
        image: perl
        command: ["perl",  "-Mbignum=bpi", "-wle", "print bpi(2000)"]
      restartPolicy: Never
```

Job `pi-with-ttl` akan dihapus secara otomatis, dalam jangka waktu `100`
detik setelah Job tersebut selesai dijalankan.

Jika _field_ ini dispesifikasikan sebagai `0`, maka Job akan secara otomatis dihapus 
segera setelah Job tersebut selesai dijalankan. Jika _field_ tersebut tidak dispesifikasikan, 
maka Job ini tidak akan dihapus oleh _controller_ TTL setelah Job ini selesai dijalankan.

Perhatikan bahwa mekanisme TTL ini merupakan fitur alpha, dengan gerbang fitur `TTLAfterFinished`. 
Untuk informasi lebih lanjut, kamu dapat membaca dokumentasi untuk 
[_controller_ TTL](/id/docs/concepts/workloads/controllers/ttlafterfinished/) untuk 
sumber daya yang telah selesai dijalankan.

## Pola Job

Sebuah objek Job dapat digunakan untuk mendukung eksekusi paralel yang dapat diandalkan pada Pod. 
Objek Job tidak di-desain untuk mendukung proses paralel bersifat _closely-communicating_, 
seperti yang secara umum ditemukan dalam komputasi ilmiah. Meskipun begitu objek ini mendukung 
set *work item* yang independen namun saling terkait satu sama lainnya. Ini termasuk surel yang harus dikirim, 
_frame_ yang harus di-_render_, berkas yang harus di-_transcoded_, jangkauan _key_ yang ada 
di dalam basis data NoSQL, dsb.

Pada suatu sistem yang kompleks, terdapat beberapa set _work item_ yang berbeda. 
Di sini, kami hanya mempertimbangkan _work item_ yang ingin digunakan oleh pengguna 
untuk melakukan manajemen secara bersamaan &mdash; sebuah *batch job*.

Terdapat beberapa perbedaan pola pada komputasi paralel, 
setiap pola memiliki kelebihan dan kekurangannya masing-masing. Kekurangan dan kelebihan ini 
dijabarkan sebagai berikut:

- Satu objek Job untuk setiap _work item_, atau sebuah Job untuk semua _work item_. Pilihan kedua akan lebih baik apabila digunakan untuk jumlah _work item_ yang lebih besar.
  Sementara itu, pilihan pertama akan mengakibatkan _overhead_ bagi pengguna dan juga sistem 
  untuk mengaur jumlah objek Job yang cukup banyak.
- Jumlah Pod yang dibuat sesuai dengan jumlah _work item_ atau setiap Pod dapat memproses beberapa _work item_ sekaligus.
  Pilihan pertama secara umum memerlukan modifikasi lebih sedikit untuk kode dan Container yang suda ada. Pilihan kedua 
  akan lebih baik jika digunakan untuk jumlah _work item_ yang lebih banyak, untuk alasan yang sama dengan poin sebelumnya.
- Beberapa pendekatan menggunakan prinsip _work queue_. Hal ini membutuhkan sebuah _service queue_ yang dijalankan, 
  serta modifikasi untuk program atau Container yang sudah ada untuk mengizinkannya menggunakan _working queue_. 
  Pendekatan lain akan lebih mudah untuk digunakan bagi aplikasi yang sudah ada.


_Tradeoff_ yang dirangkum di sini, dengan kolom 2 dan 4 berkaitan dengan _tradeoff_ yang dijelaskan di atas.
Nama dari pola yang ada juga terkait dengan contoh dan deskripsi lebih lanjut.

|                            Pola                                      | Objek dengan satu Job | Pod yang lebih sedikit tadi _work items_? | Penggunaan app tanpa modifikasi? |  Dapat dijalankan pada Kube versi 1.1? |
| -------------------------------------------------------------------- |:-----------------:|:---------------------------:|:-------------------:|:-------------------:|
| [Perluasan Templat Job](/docs/tasks/job/parallel-processing-expansion/)            |                   |                             |          ✓          |          ✓          |
| [Queue dengan Pod untuk setiap _Work Item_](/docs/tasks/job/coarse-parallel-processing-work-queue/)   |         ✓         |                             |      sometimes      |          ✓          |
| [Queue dengan Variabel _Pod Count_](/docs/tasks/job/fine-parallel-processing-work-queue/)  |         ✓         |             ✓               |                     |          ✓          |
| Job Single dengan penempatan Kerja Statis                              |         ✓         |                             |          ✓          |                     |

Ketika kamu menspesifikasikan _completion_ dengan `.spec.completions`, setiap Pod yang dibuat oleh _controller_ Job 
memiliki [`spec`](https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status) yang identik. Artinya 
semua Pod untuk sebuah _task_ akan memiliki perintah yang sama serta _image_, volume, serta variabel _environment_ yang (hampir) sama. 
Pola ini merupakan salah satu cara berbeda yang diterapkan untuk mengatur Pod agar dapat bekerja untuk hal yang berbeda-beda.

Tabel ini menunjukkan pengaturan yang dibutuhkan untuk `.spec.parallelism` dan `.spec.completions` bagi setiap pola.
Disini, `W` merupakan jumlah dari _work item_.

|                             Pattern                                  | `.spec.completions` |  `.spec.parallelism` |
| -------------------------------------------------------------------- |:-------------------:|:--------------------:|
| [Job Template Expansion](/docs/tasks/job/parallel-processing-expansion/)           |          1          |     should be 1      |
| [Queue with Pod Per Work Item](/docs/tasks/job/coarse-parallel-processing-work-queue/)   |          W          |        any           |
| [Queue with Variable Pod Count](/docs/tasks/job/fine-parallel-processing-work-queue/)  |          1          |        any           |
| Single Job with Static Work Assignment                               |          W          |        any           |


## Penggunaan Tingkat Lanjut

### Menspesifikasikan Selektor Pod Kamu Sendiri

Secara umum, ketika kamu membuat sebuah objek Job, kamu 
tidak menspesifikasikan  `.spec.selector`. Sistem akan memberikan nilai 
default pada _field_ ini ketika Job dibuat. Sistem akan memilih nilai dari selektor yang ada 
dan memastikan nilainya tidak akan beririsan dengan Job lainnya.

Meskipun demikian, pada beberapa kasus, kamu bisa saja memiliki kebutuhan untuk meng-_override_ 
nilai dari selektor ini. Untuk melakukannya, kamu dapat menspesifikasikan `.spec.selector`
dari Job.

Berhati-hatilah ketika kamu melakukan proses ini. Jika kamu menspesifikasikan sebuah label 
selektor yang tidak unik pada Pod yang ada di dalam Job tersebut, serta sesuai dengan Pod yang tidak 
terkait dengan Job tadi, maka Pod dari Job yang tidak terkait dengan Job tadi akna dihapus, atau Job ini 
akan menghitung _completion_ dari Pod lain sebagai tolak ukur suksesnya Job tersebut, atau bisa saja salah satu 
atau kedua Job tidak dapat membuat Pod baru yang digunakan untuk menyelesaikan Job tersebut. 
Jika selektor yang tidak unik dipilih, maka _controller_ lain (misalnya ReplicationController) dan Pod 
yang ada di dalamnya bisa saja memiliki perilaku yang tidak dapat diprediksi. Kubernetes tidak akan 
mencegah kemungkinan terjadinya hal ini ketika kamu menspesifikasikan nilai `.spec.selector`.

Berikut merupakan contoh skenario dimana kamu ingin menggunakan fitur ini.

Misalnya saja Job dengan nama `old` sudah dijalankan. 
Dan kamu ingin Pod yang sudah dijalankan untuk tetap berada pada state tersebut, 
tapi kamu juga ingin Pod selanjutnya yang dibuat untuk menggunakan templat Pod yang berbeda dan agar 
Job tersebut memiliki nama yang berbeda. Kamu tidak dapat mengubah Job karena _field_ ini 
merupakan nilai yang tidak bisa diubah. Dengan demikian, kamu menghapus Job `old` 
tetapi tetap membiarkan Pod yang ada untuk jalan, menggunakan perintah `kubectl delete jobs/old --cascade=orphan`.
Sebelum menghapus Job tadi, kamu mencatat selektor yang digunakan oleh Job tadi:

```
kubectl get job old -o yaml
```
```
kind: Job
metadata:
  name: old
  ...
spec:
  selector:
    matchLabels:
      controller-uid: a8f3d00d-c6d2-11e5-9f87-42010af00002
  ...
```

Kemudian kamu membuat sebuah Job baru dengan nama  `new` 
dan kamu secara eksplisit menspesifikasikan selektor yang sama.
Karena Pod dengan selektor yang sama memiliki label `controller-uid=a8f3d00d-c6d2-11e5-9f87-42010af00002`,
maka Pod-Pod lama tadi dikendalikan juga oleh Job `new`.

Kamu harus menspesifikasikan `manualSelector: true` pada Job yang baru 
karena kamu tidak menggunakan selektor yang diberikan secara default oleh sistem.

```
kind: Job
metadata:
  name: new
  ...
spec:
  manualSelector: true
  selector:
    matchLabels:
      controller-uid: a8f3d00d-c6d2-11e5-9f87-42010af00002
  ...
```

Job yang baru tadi kemudian akan memiliki uid yang berbeda dari `a8f3d00d-c6d2-11e5-9f87-42010af00002`.  Pengaturan 
`manualSelector: true` memberikan perintah pada sistem bahwa kamu mengetahui apa yang kamu lakukan 
dan untuk mengizikan ketidaksesuaian ini untuk terjadi.

## Alternatif

### _Pod Polosan_

Ketika node dimana Pod dijalankan berada dalam kondisi _reboot_ atau gagal, Pod tadi akan dihentikan 
dan tidak akan di-restart. Meskipun demikian, sebuah Job akan membuat Pod baru yang menggantikan 
Pod lama yang dihentikan. Untuk alasan inilah, kami memberikan rekomendasi agar kamu menggunakan sebuah Job dibandingkan dengan 
Pod yang biasa, bahkan jika aplikasi yang kamu gunakan hanya memerlukan sebuah Pod.

### Replication Controller

Job merupakan komplemen dari [Replication Controller](/docs/user-guide/replication-controller).
Sebuah Replication Controller mengatur Pod yang diharapkan untuk tidak dihentikan (misalnya, _web server_), dan sebuah Job
mengatur Pod yang diharapkan untuk berhenti (misalnya, _batch task_).

Seperti yang sudah dibahas pada [_Lifecycle_ Pod](/id/docs/concepts/workloads/pods/pod-lifecycle/), `Job` *hanya* pantas 
digunakan untuk Pod dengan `RestartPolicy` yang sama dengan `OnFailure` atau `Never`.
(Perhatikan bahwa: Jika `RestartPolicy` tidak dispesifikasikan, nilai defaultnya adalah `Always`.)

### Job Tunggal akan menginisiasi Kontroller Pod

Pola lain yang mungkin diterapkan adalah untuk sebuah Job tunggal untuk membuat 
sebuah Pod yang kemudian akan membuat Pod lainnya, bersifat selayaknya _controller_ kustom 
bagi Pod tersebut. Hal ini mengizinkan fleksibilitas optimal, tetapi cukup kompleks untuk digunakan 
dan memiliki integrasi terbatas dengan Kubernetes.

Salah satu contoh dari pola ini adalah sebuah Job yang akan menginisiasi sebuah Pod 
yang menjalankan _script_ yang kemudian akan 
menjalankan _controller_ master Spark (kamu dapat melihatnya di [contoh Spark](https://github.com/kubernetes/examples/tree/{{< param "githubbranch" >}}/staging/spark/README.md)), 
yang menjalankan _driver_ Spark, dan kemudian melakukan mekanisme _clean up_.

Keuntungan dari pendekatan ini adalah proses keseluruhan yang memiliki jaminan _completion_ 
dari sebuah Job, tetapi kontrol secara mutlak atas Pod yang dibuat serta tugas yang diberikan pada Pod tersebut.

## CronJob {#cron-jobs}

Kamu dapat menggunakan [`CronJob`](/id/docs/concepts/workloads/controllers/cron-jobs/) untuk membuat Job yang akan 
dijalankan pada waktu/tanggal yang spesifik, mirip dengan perangkat lunak `cron` yang ada pada Unix.


