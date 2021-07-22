# 쿠버네티스 문서화

[![Netlify Status](https://api.netlify.com/api/v1/badges/be93b718-a6df-402a-b4a4-855ba186c97d/deploy-status)](https://app.netlify.com/sites/kubernetes-io-main-staging/deploys) [![GitHub release](https://img.shields.io/github/release/kubernetes/website.svg)](https://github.com/kubernetes/website/releases/latest)

이 저장소에는 [쿠버네티스 웹사이트 및 문서](https://kubernetes.io/)를 빌드하는 데 필요한 자산이 포함되어 있습니다. 기여해주셔서 감사합니다!

# 저장소 사용하기

Hugo(확장 버전)를 사용하여 웹사이트를 로컬에서 실행하거나, 컨테이너 런타임에서 실행할 수 있습니다. 라이브 웹사이트와의 배포 일관성을 제공하므로, 컨테이너 런타임을 사용하는 것을 적극 권장합니다.

## 사전 준비 사항

이 저장소를 사용하기 위해, 로컬에 다음의 소프트웨어들이 설치되어 있어야 합니다.

- [npm](https://www.npmjs.com/)
- [Go](https://golang.org/)
- [Hugo(확장 버전)](https://gohugo.io/)
- [도커](https://www.docker.com/)와 같은 컨테이너 런타임.

시작하기 전에 의존성이 있는 소프트웨어를 설치합니다. 저장소를 복제(clone)하고 디렉터리로 이동합니다.

```
git clone https://github.com/kubernetes/website.git
cd website
```

쿠버네티스 웹사이트는 [Docsy Hugo 테마](https://github.com/google/docsy#readme)를 사용합니다. 웹사이트를 컨테이너에서 실행하려는 경우에도, 다음을 실행하여 하위 모듈 및 기타 개발 종속성을 가져오는 것이 좋습니다.

```
# Docsy 하위 모듈 가져오기
git submodule update --init --recursive --depth 1
```

## 컨테이너를 사용하여 웹사이트 실행하기

컨테이너에서 사이트를 빌드하려면, 다음을 실행하여 컨테이너 이미지를 빌드하고 실행합니다.

```
make container-image
make container-serve
```

웹사이트를 보려면 브라우저를 http://localhost:1313 으로 엽니다. 소스 파일을 변경하면 Hugo가 웹사이트를 업데이트하고 브라우저를 강제로 새로 고칩니다.

## Hugo를 사용하여 로컬에서 웹사이트 실행하기

[`netlify.toml`](netlify.toml#L10) 파일의 `HUGO_VERSION` 환경 변수에 지정된 Hugo 확장 버전을 설치해야 합니다.

사이트를 로컬에서 빌드하고 테스트하려면, 다음을 실행합니다.

```bash
# 의존성 있는 소프트웨어 설치
npm ci
make serve
```

그러면 포트 1313에서 로컬 Hugo 서버가 시작됩니다. 웹사이트를 보려면 http://localhost:1313 으로 브라우저를 엽니다. 소스 파일을 변경하면, Hugo가 웹사이트를 업데이트하고 브라우저를 강제로 새로 고칩니다.

## 문제 해결
### error: failed to transform resource: TOCSS: failed to transform "scss/main.scss" (text/x-scss): this feature is not available in your current Hugo version

Hugo는 기술적인 이유로 2개의 바이너리 세트로 제공됩니다. 현재 웹사이트는 **Hugo 확장** 버전 기반에서만 실행됩니다. [릴리스 페이지](https://github.com/gohugoio/hugo/releases)에서 이름에 `extended` 가 포함된 아카이브를 찾습니다. 확인하려면, `hugo version` 을 실행하고 `extended` 라는 단어를 찾습니다.

### too many open files 이슈에 대한 macOS 문제 해결

macOS에서 `make serve` 를 실행하면 다음의 오류 메시지가 출력됩니다.

```
ERROR 2020/08/01 19:09:18 Error: listen tcp 127.0.0.1:1313: socket: too many open files
make: *** [serve] Error 1
```

파일 오픈 개수에 대한 현재 제한값을 확인합니다.

`launchctl limit maxfiles`

그리고 다음의 명령을 실행합니다(https://gist.github.com/tombigel/d503800a282fcadbee14b537735d202c 를 참고하여 적용).

```
#!/bin/sh

# 코멘트 처리한 것은 원래 gist 링크들이며, 그 아래는 수정된 tombigel의 gist 링크입니다.
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

이 내용은 Catalina와 Mojave macOS에서 작동합니다.


# SIG Docs에 참여하기

[커뮤니티 페이지](https://github.com/kubernetes/community/tree/master/sig-docs#meetings)에서 SIG Docs 쿠버네티스 커뮤니티 및 회의에 대한 자세한 내용을 확인합니다.

이 프로젝트의 메인테이너에게 연락을 할 수도 있습니다.

- [슬랙](https://kubernetes.slack.com/messages/sig-docs) [슬랙에 초대 받기](https://slack.k8s.io/)
- [메일링 리스트](https://groups.google.com/forum/#!forum/kubernetes-sig-docs)

# 문서에 기여하기

이 저장소에 대한 복제본을 여러분의 GitHub 계정에 생성하기 위해 화면 오른쪽 위 영역에 있는 **Fork** 버튼을 클릭하면 됩니다. 이 복제본은 *fork* 라고 부릅니다. 여러분의 fork에서 원하는 임의의 변경 사항을 만들고, 해당 변경 사항을 보낼 준비가 되었다면, 여러분의 fork로 이동하여 새로운 풀 리퀘스트를 만들어 우리에게 알려주시기 바랍니다.

여러분의 풀 리퀘스트가 생성된 이후에는, 쿠버네티스 리뷰어가 명료하고 실행 가능한 피드백을 제공하는 책임을 담당할 것입니다. 풀 리퀘스트의 오너로서, **쿠버네티스 리뷰어로부터 제공받은 피드백을 수용하기 위해 풀 리퀘스트를 수정하는 것은 여러분의 책임입니다.**

또한, 참고로 한 명 이상의 쿠버네티스 리뷰어가 여러분에게 피드백을 제공하는 상황이거나, 또는 원래 여러분에게 피드백을 제공하기로 할당된 사람이 아닌 다른 쿠버네티스 리뷰어로부터 피드백을 받는 상황도 있습니다.

그뿐만 아니라, 몇몇 상황에서는, 필요에 따라 리뷰어 중 한 명이 [쿠버네티스 기술 리뷰어](https://github.com/kubernetes/website/wiki/Tech-reviewers)로부터의 기술 리뷰를 요청할지도 모릅니다. 리뷰어는 제시간에 피드백을 제공하기 위해 최선을 다할 것이지만, 응답 시간은 상황에 따라 달라질 수도 있습니다.

쿠버네티스 문서화에 기여하기와 관련된 보다 자세한 정보는, 다음을 참고합니다.

* [쿠버네티스 문서에 기여하기](https://kubernetes.io/docs/contribute/)
* [페이지 콘텐트 타입](https://kubernetes.io/docs/contribute/style/page-content-types/)
* [문서화 스타일 가이드](http://kubernetes.io/docs/contribute/style/style-guide/)
* [쿠버네티스 문서 현지화](https://kubernetes.io/docs/contribute/localization/)

# `README.md`에 대한 쿠버네티스 문서 현지화(localization)

## 한국어

`README.md` 번역 및 한국어 기여자를 위한 보다 자세한 가이드는 [쿠버네티스 문서 한글화 가이드](https://kubernetes.io/ko/docs/contribute/localization_ko/)를 참고합니다.

한국어 번역 메인테이너에게 다음을 통해 연락할 수 있습니다.

* 손석호 ([GitHub - @seokho-son](https://github.com/seokho-son))
* [슬랙 채널](https://kubernetes.slack.com/messages/kubernetes-docs-ko)

# 행동 강령

쿠버네티스 커뮤니티 참여는 [CNCF 행동 강령](https://github.com/cncf/foundation/blob/master/code-of-conduct-languages/ko.md)을 따릅니다.

# 감사합니다!

쿠버네티스는 커뮤니티 참여를 통해 번창하며, 우리는 웹사이트 및 문서화에 대한 당신의 기여에 감사드립니다!
