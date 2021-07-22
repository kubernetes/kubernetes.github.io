---
title: Padrão Operador
content_type: concept
weight: 30
---

<!-- overview -->

Operadores são extensões de software para o Kubernetes que
fazem uso de [*recursos personalizados*](/docs/concepts/extend-kubernetes/api-extension/custom-resources/)
para gerir aplicações e os seus componentes. Operadores seguem os  
princípios do Kubernetes, notavelmente o [ciclo de controle](/docs/concepts/#kubernetes-control-plane).




<!-- body -->

## Motivação

O padrão Operador tem como objetivo capturar o principal objetivo de um operador
humano que gere um serviço ou um conjunto de serviços. Operadores humanos 
responsáveis por aplicações e serviços específicos têm um conhecimento
profundo da forma como o sistema é suposto se comportar, como é instalado
e como deve reagir na ocorrência de problemas.

As pessoas que executam cargas de trabalho no Kubernetes habitualmente gostam
de usar automação para cuidar de tarefas repetitivas. O padrão Operador captura
a forma como pode escrever código para automatizar uma tarefa para além do que
o Kubernetes fornece.

## Operadores no Kubernetes

O Kubernetes é desenhado para automação. *Out of the box*, você tem bastante
automação embutida no núcleo do Kubernetes. Pode usar
o Kubernetes para automatizar instalações e executar cargas de trabalho,
e pode ainda automatizar a forma como o Kubernetes faz isso.

O conceito de {{< glossary_tooltip text="controlador" term_id="controller" >}} no
Kubernetes permite a extensão do comportamento sem modificar o código do próprio
Kubernetes.
Operadores são clientes da API do Kubernetes que atuam como controladores para
um dado [*Custom Resource*](/docs/concepts/api-extension/custom-resources/)

## Exemplo de um Operador {#exemplo}

Algumas das coisas que um operador pode ser usado para automatizar incluem:

* instalar uma aplicação a pedido
* obter e restaurar backups do estado dessa aplicação
* manipular atualizações do código da aplicação juntamente com alterações
  como esquemas de base de dados ou definições de configuração extra
* publicar um *Service* para aplicações que não suportam a APIs do Kubernetes
  para as descobrir
* simular una falha em todo ou parte do cluster de forma a testar a resiliência
* escolher um lider para uma aplicação distribuída sem um processo
  de eleição de membro interno

Como deve um Operador parecer em mais detalhe? Aqui está um exemplo em mais
detalhe:

1. Um recurso personalizado (*custom resource*) chamado SampleDB, que você pode
  configurar para dentro do *cluster*.
2. Um *Deployment* que garante que um *Pod* está a executar que contém a
  parte controlador do operador.
3. Uma imagem do *container* do código do operador.
4. Código do controlador que consulta o plano de controle para descobrir quais
  recursos *SampleDB* estão configurados.
5. O núcleo do Operador é o código para informar ao servidor da API (*API server*) como fazer
   a realidade coincidir com os recursos configurados.
   * Se você adicionar um novo *SampleDB*, o operador configurará *PersistentVolumeClaims*
     para fornecer armazenamento de base de dados durável, um *StatefulSet* para executar *SampleDB* e
     um *Job* para lidar com a configuração inicial.
   * Se você apagá-lo, o Operador tira um *snapshot* e então garante que
     o *StatefulSet* e *Volumes* também são removidos.
6. O operador também gere backups regulares da base de dados. Para cada recurso *SampleDB*,
  o operador determina quando deve criar um *Pod* que possa se conectar
   à base de dados e faça backups. Esses *Pods* dependeriam de um *ConfigMap*
   e / ou um *Secret* que possui detalhes e credenciais de conexão com à base de dados.
7. Como o Operador tem como objetivo fornecer automação robusta para o recurso
   que gere, haveria código de suporte adicional. Para este exemplo,
   O código verifica se a base de dados está a executar uma versão antiga e, se estiver,
   cria objetos *Job* que o atualizam para si.

## Instalar Operadores

A forma mais comum de instalar um Operador é a de adicionar a
definição personalizada de recurso (*Custom Resource Definition*) e
o seu Controlador associado ao seu cluster.
O Controlador vai normalmente executar fora do
{{< glossary_tooltip text="plano de controle" term_id="control-plane" >}},
como você faria com qualquer aplicação containerizada.
Por exemplo, você pode executar o controlador no seu cluster como um *Deployment*.

## Usando um Operador

Uma vez que você tenha um Operador instalado, usaria-o adicionando, modificando
ou apagando a espécie de recurso que o Operador usa. Seguindo o exemplo acima,
você configuraria um *Deployment* para o próprio Operador, e depois:

```shell
kubectl get SampleDB                   # encontra a base de dados configurada

kubectl edit SampleDB/example-database # mudar manualmente algumas definições
```

&hellip;e é isso! O Operador vai tomar conta de aplicar
as mudanças assim como manter o serviço existente em boa forma.

## Escrevendo o seu próprio Operador {#escrevendo-operador}

Se não existir no ecosistema um Operador que implementa
o comportamento que pretende, pode codificar o seu próprio.
[Qual é o próximo](#qual-é-o-próximo) você vai encontrar
alguns *links* para bibliotecas e ferramentas que pode usar
para escrever o seu próprio Operador *cloud native*.

Pode também implementar um Operador (isto é, um Controlador) usando qualquer linguagem / *runtime*
que pode atuar como um [cliente da API do Kubernetes](/docs/reference/using-api/client-libraries/).



## {{% heading "whatsnext" %}}


* Aprenda mais sobre [Recursos Personalizados](/docs/concepts/extend-kubernetes/api-extension/custom-resources/)
* Encontre operadores prontos em [OperatorHub.io](https://operatorhub.io/) para o seu caso de uso
* Use ferramentes existentes para escrever os seus Operadores:
  * usando [KUDO](https://kudo.dev/) (Kubernetes Universal Declarative Operator)
  * usando [kubebuilder](https://book.kubebuilder.io/)
  * usando [Metacontroller](https://metacontroller.github.io/metacontroller/intro.html) juntamente com WebHooks que
    implementa você mesmo
  * usando o [Operator Framework](https://github.com/operator-framework/getting-started)
* [Publique](https://operatorhub.io/) o seu operador para que outras pessoas o possam usar
* Leia o [artigo original da CoreOS](https://coreos.com/blog/introducing-operators.html) que introduz o padrão Operador
* Leia um [artigo](https://cloud.google.com/blog/products/containers-kubernetes/best-practices-for-building-kubernetes-operators-and-stateful-apps) da Google Cloud sobre as melhores práticas para contruir Operadores


