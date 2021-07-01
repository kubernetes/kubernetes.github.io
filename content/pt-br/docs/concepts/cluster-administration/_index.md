---
title: Administração de Cluster
weight: 100
content_type: concept
description: >
  Detalhes de baixo nível relevantes para criar ou administrar um cluster Kubernetes.
no_list: true
---

<!-- overview -->
A visão geral da administração do cluster é para qualquer pessoa que crie ou administre um cluster do Kubernetes.
É pressuposto alguma familiaridade com os [conceitos](/docs/concepts) principais do Kubernetes.

<!-- body -->
## Planejando um cluster

Consulte os guias em [Configuração](/docs/setup) para exemplos de como planejar, instalar e configurar clusters Kubernetes. As soluções listadas neste artigo são chamadas de *distros*.

   {{< note  >}}
   Nem todas as distros são mantidas ativamente. Escolha distros que foram testadas com uma versão recente do Kubernetes.
   {{< /note >}}

Antes de escolher um guia, aqui estão algumas considerações:

- Você quer experimentar o Kubernetes em seu computador ou deseja criar um cluster de vários nós com alta disponibilidade? Escolha as distros mais adequadas ás suas necessidades.
- Você vai usar um **cluster Kubernetes gerenciado** , como o [Google Kubernetes Engine](https://cloud.google.com/kubernetes-engine/), ou **vai hospedar seu próprio cluster**?
- Seu cluster será **local**, ou **na nuvem (IaaS)**? O Kubernetes não oferece suporte direto a clusters híbridos. Em vez disso, você pode configurar vários clusters.
- **Se você estiver configurando o Kubernetes local**, leve em consideração qual [modelo de rede](/docs/concepts/cluster-Administration/networking) se encaixa melhor.
- Você vai executar o Kubernetes em um hardware **bare metal** ou em **máquinas virtuais? (VMs)**?
- Você **deseja apenas executar um cluster** ou espera **participar ativamente do desenvolvimento do código do projeto Kubernetes**? Se for a segunda opção,
escolha uma distro desenvolvida ativamente. Algumas distros usam apenas versão binária, mas oferecem uma maior variedade de opções.
- Familiarize-se com os [componentes](/docs/concepts/overview/components/) necessários para executar um cluster.


## Gerenciando um cluster

* Aprenda como [gerenciar nós](/docs/concepts/architecture/nodes/).
* Aprenda a configurar e [gerenciar a quota de recursos](/docs/concepts/policy/resource-quotas/) para clusters compartilhados.

## Protegendo um cluster

* [Gerar Certificados](/docs/tasks/administer-cluster/certificates/)  descreve os passos para gerar certificados usando diferentes cadeias de ferramentas.

* [Ambiente de Contêineres do Kubernetes](/docs/concepts/containers/container-environment/) descreve o ambiente para contêineres gerenciados pelo kubelet em um nó Kubernetes.

* [Controle de Acesso a API do Kubernetes](/docs/concepts/security/controlling-access) descreve como o Kubernetes implementa o controle de acesso para sua própria API.

* [Autenticação](/docs/reference/access-authn-authz/authentication/) explica a autenticação no Kubernetes, incluindo as várias opções de autenticação.

* [Autorização](/docs/reference/access-authn-authz/authorization/) é separado da autenticação e controla como as chamadas HTTP são tratadas.

* [Usando Controladores de Admissão](/docs/reference/access-authn-authz/admission-controllers/) explica plugins que interceptam requisições para o servidor da API Kubernetes após 
a autenticação e autorização.

* [usando Sysctl em um Cluster Kubernetes](/docs/tasks/administer-cluster/sysctl-cluster/) descreve a um administrador como usar a ferramenta de linha de comando `sysctl` para
definir os parâmetros do kernel.

* [Auditoria](/docs/tasks/debug-application-cluster/audit/) descreve como interagir com *logs* de auditoria do Kubernetes.

### Protegendo o kubelet
  * [Comunicação Control Plane-Nó](/docs/concepts/architecture/control-plane-node-communication/)
  * [TLS bootstrapping](/docs/reference/command-line-tools-reference/kubelet-tls-bootstrapping/)
  * [Autenticação/autorização do kubelet](/docs/reference/command-line-tools-reference/kubelet-authentication-authorization/)

## Serviços Opcionais para o Cluster

* [Integração com DNS](/docs/concepts/services-networking/dns-pod-service/) descreve como resolver um nome DNS diretamente para um serviço Kubernetes.

* [Registro e Monitoramento da Atividade do Cluster](/docs/concepts/cluster-administration/logging/) explica como funciona o *logging* no Kubernetes e como implementá-lo.
