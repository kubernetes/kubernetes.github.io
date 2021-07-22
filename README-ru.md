# Документация по Kubernetes

[![Netlify Status](https://api.netlify.com/api/v1/badges/be93b718-a6df-402a-b4a4-855ba186c97d/deploy-status)](https://app.netlify.com/sites/kubernetes-io-main-staging/deploys) [![GitHub release](https://img.shields.io/github/release/kubernetes/website.svg)](https://github.com/kubernetes/website/releases/latest)

Данный репозиторий содержит все необходимые файлы для сборки [сайта Kubernetes и документации](https://kubernetes.io/). Мы благодарим вас за желание внести свой вклад!

# Использование этого репозитория

Запустить сайт локально можно с помощью Hugo (Extended version) или же в исполняемой среде для контейнеров. Мы настоятельно рекомендуем воспользоваться контейнерной средой, поскольку она обеспечивает консистивность развёртывания с оригинальным сайтом.

## Предварительные требования

Чтобы работать с этим репозиторием, понадобятся следующие компоненты, установленные локально:

- [npm](https://www.npmjs.com/)
- [Go](https://golang.org/)
- [Hugo (Extended version)](https://gohugo.io/)
- Исполняемая среда для контейнеров вроде [Docker](https://www.docker.com/)

Перед тем, как начать, установите зависимости. Склонируйте репозиторий и перейдите в его директорию:

```
git clone https://github.com/kubernetes/website.git
cd website
```

Сайт Kubernetes использует [тему для Hugo под названием Docsy](https://github.com/google/docsy). Даже если вы планируете запускать сайт в контейнере, мы настоятельно рекомендуем загрузить соответствующий подмодуль и другие зависимости для разработки, выполнив следующую команду:

```
# загружаем Git-подмодуль Docsy
git submodule update --init --recursive --depth 1
```

## Запуск сайта в контейнере

Чтобы собрать сайт в контейнере, выполните следующие команды — они собирают образ контейнера и запускают его:

```
make container-image
make container-serve
```

Откройте браузер и перейдите по ссылке http://localhost:1313, чтобы увидеть сайт. Если вы отредактируете исходные файлы сайта, Hugo автоматически обновит сам сайт и выполнит обновление страницы в браузере.
 
## Запуск сайта с помощью Hugo

Убедитесь, что вы установили расширенную версию Hugo (extended version): она определена в переменной окружения `HUGO_VERSION` в файле [`netlify.toml`](netlify.toml#L10).

Чтобы собрать и протестировать сайт локально, выполните:

```bash
# install dependencies
npm ci
make serve
```

Эти команды запустят локальный сервер Hugo на порту 1313. Откройте браузер и перейдите по ссылке http://localhost:1313, чтобы увидеть сайт. Если вы отредактируете исходные файлы сайта, Hugo автоматически обновит сам сайт и выполнит обновление страницы в браузере.

## Решение проблем
### error: failed to transform resource: TOCSS: failed to transform "scss/main.scss" (text/x-scss): this feature is not available in your current Hugo version

По техническим причинам Hugo поставляется с двумя наборами бинарников. Текущий сайт Kubernetes работает только в версии **Hugo Extended**. На [странице релизов](https://github.com/gohugoio/hugo/releases) ищите архивы со словом `extended` в названии. Чтобы убедиться в корректности, запустите команду `hugo version` и найдите в выводе слово `extended`.

### Решение проблемы на macOS с "too many open files"

Если вы запускаете `make serve` на macOS и получаете следующую ошибку:

```
ERROR 2020/08/01 19:09:18 Error: listen tcp 127.0.0.1:1313: socket: too many open files
make: *** [serve] Error 1
```

Попробуйте проверить текущий лимит для открытых файлов:

`launchctl limit maxfiles`

Затем выполните следующие команды (они взяты и адаптированы из https://gist.github.com/tombigel/d503800a282fcadbee14b537735d202c):

```shell
#!/bin/sh

# Ссылки на оригинальные gist-файлы закомментированы в пользу моих адаптированных.
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

Данное решение работает для macOS Catalina и Mojave.

# Участие в SIG Docs

Узнайте о Kubernetes-сообществе SIG Docs и его встречах на [странице сообщества](https://github.com/kubernetes/community/tree/master/sig-docs#meetings).

Вы можете связаться с сопровождающими этот проект по следующим ссылкам:

- [Канал в Slack](https://kubernetes.slack.com/messages/sig-docs) ([получите приглашение в этот Slack](https://slack.k8s.io/))
- [Почтовая рассылка](https://groups.google.com/forum/#!forum/kubernetes-sig-docs)

# Вклад в документацию

Нажмите на кнопку **Fork** в правом верхнем углу, чтобы создать копию этого репозитория для вашего GitHub-аккаунта. Эта копия называется *форк-репозиторием*. Делайте любые изменения в своем форк-репозитории и, когда будете готовы опубликовать изменения, зайдите в свой форк-репозиторий и создайте новый pull-запрос (PR), чтобы уведомить нас.

После того, как вы отправите pull-запрос, ревьювер из проекта Kubernetes даст по нему обратную связь. Вы, как автор pull-запроса, **должны обновить свой PR после его рассмотрения ревьювером Kubernetes.**

Вполне возможно, что более одного ревьювера Kubernetes оставят свои комментарии. Может быть даже так, что вы будете получать обратную связь уже не от того ревьювера, что был первоначально вам назначен. Кроме того, в некоторых случаях один из ревьюверов может запросить техническую рецензию от [технического ревьювера Kubernetes](https://github.com/kubernetes/website/wiki/Tech-reviewers), если это потребуется. Ревьюверы сделают все возможное, чтобы как можно оперативнее оставить свои предложения и пожелания, но время ответа может варьироваться в зависимости от обстоятельств.

Узнать подробнее о том, как поучаствовать в документации Kubernetes, вы можете по ссылкам ниже:

* [Начните вносить свой вклад](https://kubernetes.io/docs/contribute/)
* [Использование шаблонов страниц](https://kubernetes.io/docs/contribute/style/page-content-types/)
* [Руководство по оформлению документации](https://kubernetes.io/docs/contribute/style/style-guide/)
* [Руководство по локализации Kubernetes](https://kubernetes.io/docs/contribute/localization/)

# Файл `README.md` на других языках

|           другие языки        |       другие языки            |
|-------------------------------|-------------------------------|
| [Английский](README.md)       | [Немецкий](README-de.md)      |
| [Вьетнамский](README-vi.md)   | [Польский]( README-pl.md)     |
| [Индонезийский](README-id.md) | [Португальский](README-pt.md) |
| [Испанский](README-es.md)     | [Украинский](README-uk.md)    |
| [Итальянский](README-it.md)   | [Французский](README-fr.md)   |
| [Китайский](README-zh.md)     | [Хинди](README-hi.md)         |
| [Корейский](README-ko.md)     | [Японский](README-ja.md)      |

# Кодекс поведения

Участие в сообществе Kubernetes регулируется [кодексом поведения CNCF](https://github.com/cncf/foundation/blob/master/code-of-conduct-languages/ru.md).

# Спасибо!

Kubernetes процветает благодаря сообществу и мы ценим ваш вклад в сайт и документацию!
