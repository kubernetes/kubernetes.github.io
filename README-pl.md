# Dokumentacja projektu Kubernetes

[![Netlify Status](https://api.netlify.com/api/v1/badges/be93b718-a6df-402a-b4a4-855ba186c97d/deploy-status)](https://app.netlify.com/sites/kubernetes-io-main-staging/deploys) [![GitHub release](https://img.shields.io/github/release/kubernetes/website.svg)](https://github.com/kubernetes/website/releases/latest)

W tym repozytorium znajdziesz wszystko, czego potrzebujesz do zbudowania [strony internetowej Kubernetesa wraz z dokumentacją](https://kubernetes.io/). Bardzo nam miło, że chcesz wziąć udział w jej współtworzeniu!

+ [Twój wkład w dokumentację](#twój-wkład-w-dokumentację)
+ [Informacje o wersjach językowych](#informacje-o-wersjach-językowych)

# Jak używać tego repozytorium

Możesz uruchomić serwis lokalnie poprzez Hugo (Extended version) lub ze środowiska kontenerowego. Zdecydowanie zalecamy korzystanie z kontenerów, bo dzięki temu lokalna wersja będzie spójna z tym, co jest na oficjalnej stronie.

## Wymagania wstępne

Aby móc skorzystać z tego repozytorium, musisz lokalnie zainstalować:

- [npm](https://www.npmjs.com/)
- [Go](https://golang.org/)
- [Hugo (Extended version)](https://gohugo.io/)
- Środowisko obsługi kontenerów, np. [Docker-a](https://www.docker.com/).

Przed rozpoczęciem zainstaluj niezbędne zależności. Sklonuj repozytorium i przejdź do odpowiedniego katalogu:

```
git clone https://github.com/kubernetes/website.git
cd website
```

Strona Kubernetesa używa [Docsy Hugo theme](https://github.com/google/docsy#readme). Nawet jeśli planujesz uruchomić serwis w środowisku kontenerowym, zalecamy pobranie podmodułów i innych zależności za pomocą polecenia:

```
# pull in the Docsy submodule
git submodule update --init --recursive --depth 1
```

## Uruchomienie serwisu w kontenerze

Aby zbudować i uruchomić serwis wewnątrz środowiska kontenerowego, wykonaj następujące polecenia:

```
make container-image
make container-serve
```

Aby obejrzeć zawartość serwisu otwórz w przeglądarce adres http://localhost:1313. Po każdej zmianie plików źródłowych, Hugo automatycznie aktualizuje stronę i odświeża jej widok w przeglądarce.

## Jak uruchomić lokalną kopię strony przy pomocy Hugo?

Upewnij się, że zainstalowałeś odpowiednią wersję Hugo "extended", określoną przez zmienną środowiskową `HUGO_VERSION` w pliku [`netlify.toml`](netlify.toml#L10).

Aby uruchomić i przetestować serwis lokalnie, wykonaj:

```bash
# install dependencies
npm ci
make serve
```

Zostanie uruchomiony lokalny serwer Hugo na porcie 1313. Otwórz w przeglądarce adres http://localhost:1313, aby obejrzeć zawartość serwisu. Po każdej zmianie plików źródłowych, Hugo automatycznie aktualizuje stronę i odświeża jej widok w przeglądarce.

## Budowanie dokumentacji źródłowej API

Budowanie dokumentacji źródłowej API zostało opisane w [angielskiej wersji pliku README.md](README.md#building-the-api-reference-pages).

## Rozwiązywanie problemów
### error: failed to transform resource: TOCSS: failed to transform "scss/main.scss" (text/x-scss): this feature is not available in your current Hugo version

Z przyczyn technicznych, Hugo jest rozprowadzany w dwóch wersjach. Aktualny serwis używa tylko wersji **Hugo Extended**. Na stronie z [wydaniami](https://github.com/gohugoio/hugo/releases) poszukaj archiwum z `extended` w nazwie. Dla potwierdzenia, uruchom `hugo version` i poszukaj słowa `extended`.

### Błąd w środowisku macOS: "too many open files"

Jeśli po uruchomieniu `make serve` na macOS widzisz następujący błąd:

```
ERROR 2020/08/01 19:09:18 Error: listen tcp 127.0.0.1:1313: socket: too many open files
make: *** [serve] Error 1
```

sprawdź aktualny limit otwartych plików:

`launchctl limit maxfiles`

Uruchom następujące polecenia: (na podstawie https://gist.github.com/tombigel/d503800a282fcadbee14b537735d202c):

```shell
#!/bin/sh

# These are the original gist links, linking to my gists now.
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

Przedstawiony sposób powinien działać dla MacOS w wersji Catalina i Mojave.


# Zaangażowanie w prace SIG Docs

O społeczności SIG Docs i terminach spotkań dowiesz z [jej strony](https://github.com/kubernetes/community/tree/master/sig-docs#meetings).

Możesz kontaktować się z gospodarzami projektu za pomocą:

- [Komunikatora Slack](https://kubernetes.slack.com/messages/sig-docs) [Tutaj możesz dostać zaproszenie do tej grupy Slack-a](https://slack.k8s.io/)
- [List dyskusyjnych](https://groups.google.com/forum/#!forum/kubernetes-sig-docs)

# Twój wkład w dokumentację

Możesz kliknąć w przycisk **Fork** w prawym górnym rogu ekranu, aby stworzyć kopię tego repozytorium na swoim koncie GitHub. Taki rodzaj kopii (odgałęzienia) nazywa się *fork*. Zmieniaj w nim, co chcesz, a kiedy będziesz już gotowy/a przesłać te zmiany do nas, przejdź do swojej kopii i stwórz nowy *pull request*, abyśmy zostali o tym poinformowani.

Po stworzeniu *pull request*, jeden z recenzentów projektu Kubernetes podejmie się przekazania jasnych wskazówek pozwalających podjąć następne działania. Na Tobie, jako właścicielu *pull requesta*, **spoczywa odpowiedzialność za wprowadzenie poprawek zgodnie z uwagami recenzenta.** 

Może też się zdarzyć, że swoje uwagi zgłosi więcej niż jeden recenzent, lub że recenzję będzie robił ktoś inny, niż ten, kto został przydzielony na początku.

W niektórych przypadkach, jeśli zajdzie taka potrzeba, recenzent może poprosić dodatkowo o recenzję jednego z [recenzentów technicznych](https://github.com/kubernetes/website/wiki/Tech-reviewers). Recenzenci zrobią wszystko, aby odpowiedzieć sprawnie, ale konkretny czas odpowiedzi zależy od wielu czynników.

Więcej informacji na temat współpracy przy tworzeniu dokumentacji znajdziesz na stronach:

* [Udział w rozwijaniu dokumentacji](https://kubernetes.io/docs/contribute/)
* [Rodzaje stron](https://kubernetes.io/docs/contribute/style/page-content-types/)
* [Styl pisania dokumentacji](http://kubernetes.io/docs/contribute/style/style-guide/)
* [Lokalizacja dokumentacji Kubernetes](https://kubernetes.io/docs/contribute/localization/)

# Różne wersje językowe `README.md`

| Język  | Język |
|---|---|
| [angielski](README.md)       | [francuski](README-fr.md)    |
| [koreański](README-ko.md)    | [niemiecki](README-de.md)    |
| [portugalski](README-pt.md)  | [hindi](README-hi.md)        |
| [hiszpański](README-es.md)   | [indonezyjski](README-id.md) |
| [chiński](README-zh.md)      | [japoński](README-ja.md)     |
| [wietnamski](README-vi.md)   | [rosyjski](README-ru.md)     |
| [włoski](README-it.md)       | [ukraiński](README-uk.md)    |

# Zasady postępowania

Udział w działaniach społeczności Kubernetesa jest regulowany przez [Kodeks postępowania CNCF](https://github.com/cncf/foundation/blob/master/code-of-conduct-languages/pl.md).

# Dziękujemy!

Kubernetes rozkwita dzięki zaangażowaniu społeczności — doceniamy twój wkład w tworzenie naszego serwisu i dokumentacji!
