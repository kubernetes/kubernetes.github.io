---
title: 클라이언트 라이브러리
content_type: concept
weight: 30
---

<!-- overview -->
이 페이지는 다양한 프로그래밍 언어에서 쿠버네티스 API를 사용하기 위한
클라이언트 라이브러리에 대한 개요를 포함하고 있다.


<!-- body -->
[쿠버네티스 REST API](/ko/docs/reference/using-api/)를 사용해 애플리케이션을 작성하기 위해
API 호출 또는 요청/응답 타입을 직접 구현할 필요는 없다.
사용하고 있는 프로그래밍 언어를 위한 클라이언트 라이브러리를 사용하면 된다.

클라이언트 라이브러리는 대체로 인증과 같은 공통의 태스크를 처리한다.
대부분의 클라이언트 라이브러리들은 API 클라이언트가 쿠버네티스 클러스터 내부에서 동작하는 경우 인증
또는 [kubeconfig 파일](/ko/docs/tasks/access-application-cluster/configure-access-multiple-clusters/) 포맷을 통해
자격증명과 API 서버 주소를 읽을 수 있게
쿠버네티스 서비스 어카운트를 발견하고 사용할 수 있다.

## 공식적으로 지원되는 쿠버네티스 클라이언트 라이브러리

다음의 클라이언트 라이브러리들은
[쿠버네티스 SIG API Machinery](https://github.com/kubernetes/community/tree/master/sig-api-machinery)에서 공식적으로 관리된다.


| 언어      | 클라이언트 라이브러리 | 예제 프로그램 |
|----------|----------------|-----------------|
| dotnet   | [github.com/kubernetes-client/csharp](https://github.com/kubernetes-client/csharp) | [둘러보기](https://github.com/kubernetes-client/csharp/tree/master/examples/simple)
| Go       | [github.com/kubernetes/client-go/](https://github.com/kubernetes/client-go/) | [둘러보기](https://github.com/kubernetes/client-go/tree/master/examples)
| Haskell  | [github.com/kubernetes-client/haskell](https://github.com/kubernetes-client/haskell) | [둘러보기](https://github.com/kubernetes-client/haskell/tree/master/kubernetes-client/example)
| Java     | [github.com/kubernetes-client/java](https://github.com/kubernetes-client/java/) | [둘러보기](https://github.com/kubernetes-client/java#installation)
| JavaScript   | [github.com/kubernetes-client/javascript](https://github.com/kubernetes-client/javascript) | [둘러보기](https://github.com/kubernetes-client/javascript/tree/master/examples)
| Python   | [github.com/kubernetes-client/python/](https://github.com/kubernetes-client/python/) | [둘러보기](https://github.com/kubernetes-client/python/tree/master/examples)


## 커뮤니티에 의해 관리되는 클라이언트 라이브러리

{{% thirdparty-content %}}

다음의 쿠버네티스 API 클라이언트 라이브러리들은 쿠버네티스 팀이 아닌
각각의 저자들이 제공하고 관리한다.

| 언어                  | 클라이언트 라이브러리                          |
| -------------------- | ---------------------------------------- |
| Clojure              | [github.com/yanatan16/clj-kubernetes-api](https://github.com/yanatan16/clj-kubernetes-api) |
| DotNet               | [github.com/tonnyeremin/kubernetes_gen](https://github.com/tonnyeremin/kubernetes_gen) |
| DotNet (RestSharp)   | [github.com/masroorhasan/Kubernetes.DotNet](https://github.com/masroorhasan/Kubernetes.DotNet) |
| Elixir               | [github.com/obmarg/kazan](https://github.com/obmarg/kazan/) |
| Elixir               | [github.com/coryodaniel/k8s](https://github.com/coryodaniel/k8s) |
| Go                   | [github.com/ericchiang/k8s](https://github.com/ericchiang/k8s) |
| Java (OSGi)          | [bitbucket.org/amdatulabs/amdatu-kubernetes](https://bitbucket.org/amdatulabs/amdatu-kubernetes) |
| Java (Fabric8, OSGi) | [github.com/fabric8io/kubernetes-client](https://github.com/fabric8io/kubernetes-client) |
| Java                 | [github.com/manusa/yakc](https://github.com/manusa/yakc) |
| Lisp                 | [github.com/brendandburns/cl-k8s](https://github.com/brendandburns/cl-k8s) |
| Lisp                 | [github.com/xh4/cube](https://github.com/xh4/cube) |
| Node.js (TypeScript) | [github.com/Goyoo/node-k8s-client](https://github.com/Goyoo/node-k8s-client) |
| Node.js              | [github.com/ajpauwels/easy-k8s](https://github.com/ajpauwels/easy-k8s)
| Node.js              | [github.com/godaddy/kubernetes-client](https://github.com/godaddy/kubernetes-client) |
| Node.js              | [github.com/tenxcloud/node-kubernetes-client](https://github.com/tenxcloud/node-kubernetes-client) |
| Perl                 | [metacpan.org/pod/Net::Kubernetes](https://metacpan.org/pod/Net::Kubernetes) |
| PHP                  | [github.com/allansun/kubernetes-php-client](https://github.com/allansun/kubernetes-php-client) |
| PHP                  | [github.com/maclof/kubernetes-client](https://github.com/maclof/kubernetes-client) |
| PHP                  | [github.com/travisghansen/kubernetes-client-php](https://github.com/travisghansen/kubernetes-client-php) |
| PHP                  | [github.com/renoki-co/php-k8s](https://github.com/renoki-co/php-k8s) |
| Python               | [github.com/fiaas/k8s](https://github.com/fiaas/k8s) |
| Python               | [github.com/mnubo/kubernetes-py](https://github.com/mnubo/kubernetes-py) |
| Python               | [github.com/tomplus/kubernetes_asyncio](https://github.com/tomplus/kubernetes_asyncio) |
| Python               | [github.com/Frankkkkk/pykorm](https://github.com/Frankkkkk/pykorm) |
| Ruby                 | [github.com/abonas/kubeclient](https://github.com/abonas/kubeclient) |
| Ruby                 | [github.com/Ch00k/kuber](https://github.com/Ch00k/kuber) |
| Ruby                 | [github.com/k8s-ruby/k8s-ruby](https://github.com/k8s-ruby/k8s-ruby) |
| Ruby                 | [github.com/kontena/k8s-client](https://github.com/kontena/k8s-client) |
| Rust                 | [github.com/clux/kube-rs](https://github.com/clux/kube-rs) |
| Rust                 | [github.com/ynqa/kubernetes-rust](https://github.com/ynqa/kubernetes-rust) |
| Scala                | [github.com/hagay3/skuber](https://github.com/hagay3/skuber) |
| Scala                | [github.com/joan38/kubernetes-client](https://github.com/joan38/kubernetes-client) |
| Swift                | [github.com/swiftkube/client](https://github.com/swiftkube/client) |
