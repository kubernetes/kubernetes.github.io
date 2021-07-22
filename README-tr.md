# Kubernetes dökümantasyonu

[![Netlify Status](https://api.netlify.com/api/v1/badges/be93b718-a6df-402a-b4a4-855ba186c97d/deploy-status)](https://app.netlify.com/sites/kubernetes-io-master-staging/deploys) [![GitHub release](https://img.shields.io/github/release/kubernetes/website.svg)](https://github.com/kubernetes/website/releases/latest)

Bu depo, [Kubernetes web sitesini ve dökümantasyonunu](https://kubernetes.io/) oluşturmak için gerekli varlıkları içerir. Katkıda bulunmak istemenize sevindik!

+ [Dokümanlara katkıda bulunmak](#contributing-to-the-docs)
+ [Yerelleştirme BeniOku](#localization-readmemds)

# Bu depoyu kullanma

Web sitesini Hugo (Genişletilmiş sürüm) kullanarak yerel olarak çalıştırabilirsiniz, veya bir konteynır çalışma zamanında çalıştırabilirsiniz. Canlı web sitesiyle dağıtım tutarlılığı sağladığı için konteynır çalışma zamanını kullanmanızı şiddetle tavsiye ederiz.

## Önkoşullar

Bu depoyu kullanmak için, aşağıdakilerin yerel olarak yüklenmesi gerekir:

- [npm](https://www.npmjs.com/)
- [Go](https://golang.org/)
- [Hugo (Genişletilmiş sürüm)](https://gohugo.io/)
- [Docker](https://www.docker.com/) gibi bir konteynır çalışma zamanı. 

Başlamadan önce bağımlılıkları kurun. Depoyu klonlayın ve dizine gidin:

```
git clone https://github.com/kubernetes/website.git
cd website
```

Kubernetes web sitesi [Docsy Hugo temasını](https://github.com/google/docsy#readme) kullanır. Web sitesini bir konteynırda çalıştırmayı planlasanız bile, aşağıdakileri çalıştırarak alt modülü ve diğer geliştirme bağımlılıklarını çekmenizi şiddetle tavsiye ederiz:

```
# pull in the Docsy submodule
git submodule update --init --recursive --depth 1
```

## Web sitesini bir konteynır kullanarak çalıştırmak

Siteyi bir konteynırda oluşturmak için, konteynır görüntüsünü oluşturmak üzere aşağıdakileri çalıştırın:

```
make container-image
make container-serve
```

Web sitesini görüntülemek için tarayıcınızı http://localhost:1313 de açın. Kaynak dosyalarda değişiklik yaptıkça, Hugo web sitesini günceller ve bir tarayıcının yenilenmesini zorlar.

## Web sitesini Hugo kullanarak yerel olarak çalıştırmak

[`netlify.toml`](netlify.toml#L10) dosyasında `HUGO_VERSION` ortam değişkeni tarafından belirtilen Hugo genişletilmiş sürümünü kurduğunuzdan emin olun.

Siteyi yerel olarak oluşturmak ve test etmek için şunu çalıştırın:

```bash
# install dependencies
npm ci
make serve
```

Bu, yerel Hugo sunucusunu 1313 numaralı bağlantı noktasından başlatacak. Web sitesini görüntülemek için tarayıcınızı http://localhost:1313 de açın.  Kaynak dosyalarda değişiklik yaptıkça, Hugo web sitesini günceller ve bir tarayıcının yenilenmesini zorlar.

## API referans sayfalarını oluşturma

`content/en/docs/reference/kubernetes-api` de bulunan API referans sayfaları, https://github.com/kubernetes-sigs/reference-docs/tree/master/gen-resourcesdocs kullanılarak, Swagger şartnamesinden oluşturulmuştur.

Yeni bir Kubernetes sürümünün referans sayfalarını güncellemek için (aşağıdaki örneklerde v1.20'yi güncelleme yapılacak sürümle değiştirin):

1. `kubernetes-resources-reference` alt modülünü çekin: 

```
git submodule update --init --recursive --depth 1
```

2. Alt modüle yeni bir API revizyonu oluşturun ve Swagger şartnamesini ekleyin:

```
mkdir api-ref-generator/gen-resourcesdocs/api/v1.20
curl 'https://raw.githubusercontent.com/kubernetes/kubernetes/master/api/openapi-spec/swagger.json' > api-ref-generator/gen-resourcesdocs/api/v1.20/swagger.json
```

3. Yeni sürümün içindekiler ve alan yapılandırmasını bir öncekinden kopyalayın:

```
mkdir api-ref-generator/gen-resourcesdocs/api/v1.20
cp api-ref-generator/gen-resourcesdocs/api/v1.19/* api-ref-generator/gen-resourcesdocs/api/v1.20/
```

4. Dosyaları, iki sürüm arasındaki değişiklikleri yansıtacak şekilde `toc.yaml` ve `fields.yaml` biçimlerine uyarlayın.

5. Ardından, sayfaları oluşturun:

```
make api-reference
```

Siteyi bir konteynır görüntüsünden oluşturup sunarak sonuçları yerel olarak test edebilirsiniz:

```
make container-image
make container-serve
```

Bir web tarayıcısında, API referansını görüntülemek için http://localhost:1313/docs/reference/kubernetes-api/ adresine gidin.

6. Yeni sözleşmedeki tüm değişiklikler, `toc.yaml` ve `fields.yaml` yapılandırma dosyalarına yansıtıldığında, yeni oluşturulan API referans sayfalarıyla bir çekme isteği oluşturun.

## Sorun giderme

### hata: kaynak dönüştürülemedi:TOCSS: dönüştürülemedi "scss/main.scss" (text/x-scss): bu özellik mevcut Hugo sürümünüzde mevcut değil

Hugo, teknik nedenlerden dolayı iki grup ikili dosyada gönderilir. Mevcut web sitesi yalnızca **Hugo Extended** versiyonuna göre çalışmaktadır. [Yayın sayfasında](https://github.com/gohugoio/hugo/releases) adında `genişletilmiş` arşivleri arayın. Onaylamak için `hugo sürümünü` çalıştırın ve `genişletilmiş` kelimeyi arayın.

### macOS'ta çok fazla açık dosya için sorun giderme

macOS üzerinde `make serve` çalıştırırsanız ve aşağıdaki hatayı alırsanız:

```
ERROR 2020/08/01 19:09:18 Error: listen tcp 127.0.0.1:1313: socket: too many open files
make: *** [serve] Error 1
```

Açık dosyalar için mevcut sınırı kontrol etmeyi deneyin:

`launchctl limit maxfiles`

Ardından aşağıdaki komutları çalıştırın (https://gist.github.com/tombigel/d503800a282fcadbee14b537735d202c adresinden uyarlanmıştır):

```shell
#!/bin/sh

# Bunlar orijinal gist bağlantıları, şimdi benim gistlerime bağlanıyor.
# curl -O https://gist.githubusercontent.com/a2ikm/761c2ab02b7b3935679e55af5d81786a/raw/ab644cb92f216c019a2f032bbf25e258b01d87f9/limit.maxfiles.plist
# curl -O https://gist.githubusercontent.com/a2ikm/761c2ab02b7b3935679e55af5d81786a/raw/ab644cb92f216c019a2f032bbf25e258b01d87f9/limit.maxproc.plist

curl -O https://gist.githubusercontent.com/tombigel/d503800a282fcadbee14b537735d202c/raw/ed73cacf82906fdde59976a0c8248cce8b44f906/limit.maxfiles.plist
curl -O https://gist.githubusercontent.com/tombigel/d503800a282fcadbee14b537735d202c/raw/ed73cacf82906fdde59976a0c8248cce8b44f906/limit.maxproc.plist

sudo mv limit.maxfiles.plist /Library/LaunchDaemons
sudo mv limit.maxproc.plist /Library/LaunchDaemons

sudo chown root:wheel /Library/LaunchDaemons/limit.maxfiles.plist
sudo chown root:wheel /Library/LaunchDaemons/limit.maxproc.plist

sudo launchctl load -w /Library/LaunchDaemons/limit.maxfiles.plist
```

Bu, Catalina ve Mojave macOS için çalışır.


# SIG Docs'a katılın

[Topluluk sayfasından](https://github.com/kubernetes/community/tree/master/sig-docs#meetings) SIG Docs Kubernetes topluluğu ve toplantıları hakkında daha fazla bilgi edinin.

Bu projenin sorumlularına şu adresten de ulaşabilirsiniz: 

- [Slack](https://kubernetes.slack.com/messages/sig-docs) [Bu Slack için bir davet alın](https://slack.k8s.io/)
- [Mail Listesi](https://groups.google.com/forum/#!forum/kubernetes-sig-docs)

# Dokümanlara katkıda bulunmak

GitHub hesabınızda bu deponun bir kopyasını oluşturmak için ekranın sağ üst kısmındaki **Fork(Çatal)** düğmesine tıklayabilirsiniz. Bu kopyaya *fork* adı verilir. Çatalınızda istediğiniz değişiklikleri yapın ve bu değişiklikleri bize göndermeye hazır olduğunuzda çatalınıza gidin ve bunu bize bildirmek için yeni bir çekme isteği oluşturun.

Çekme talebiniz oluşturulduktan sonra, bir Kubernetes incelemecisi açık, eyleme geçirilebilir geri bildirim sağlama sorumluluğunu üstlenecektir. Çekme talebinin sahibi olarak, **Kubernetes incelemecisi tarafından size sağlanan geri bildirimi ele alacak şekilde çekme isteğinizi değiştirmek sizin sorumluluğunuzdadır.**

Ayrıca, birden fazla Kubernetes incelemecisine sahip olabileceğinizi veya size geri bildirim sağlamak için başlangıçta atanandan farklı bir Kubernetes incelemecisinden geri bildirim alabileceğinizi unutmayın.

Buna ek olarak, bazı durumlarda incelemecilerinizden biri, gerektiğinde bir Kubernetes teknoloji incelemecisinden teknik inceleme isteyebilir. İncelemeciler zamanında geri bildirim sağlamak için ellerinden geleni yapacaklardır ancak yanıt süresi koşullara göre değişebilir.

Kubernetes dökümantasyonuna katkıda bulunma hakkında daha fazla bilgi için bakınız:

* [Kubernetes belgelerine katkıda bulunma](https://kubernetes.io/docs/contribute/)
* [Sayfa İçerik Türleri](https://kubernetes.io/docs/contribute/style/page-content-types/)
* [Dokümantasyon Stil Kılavuzu](https://kubernetes.io/docs/contribute/style/style-guide/)
* [Kubernetes Dokümantasyonunu Yerelleştirme](https://kubernetes.io/docs/contribute/localization/)

#  `README.md`'nin Yerelleştirmesi

| Dil  | Dil |
|---|---|
|[Çince](README-zh.md)|[Korece](README-ko.md)|
|[Fransızca](README-fr.md)|[Lehçe](README-pl.md)|
|[Almanca](README-de.md)|[Portekizce](README-pt.md)|
|[Hintçe](README-hi.md)|[Rusça](README-ru.md)|
|[Endonazca](README-id.md)|[İspanyolca](README-es.md)|
|[İtalyanca](README-it.md)|[Ukraynaca](README-uk.md)|
|[Japonca](README-ja.md)|[Vietnamca](README-vi.md)|


# Davranış kodu

Kubernetes topluluğuna katılım, [CNCF Davranış Kuralları'na](https://github.com/cncf/foundation/blob/master/code-of-conduct.md) tabidir .

# Teşekkürler!

Kubernetes, topluluk katılımıyla gelişir ve web sitemize ve dökümantasyonumuza yaptığınız katkılar için teşekkür ederiz!
