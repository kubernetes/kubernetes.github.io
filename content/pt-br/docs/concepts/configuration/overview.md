---
title: Melhores Práticas de Configuração
content_type: concept
weight: 10
---

<!-- overview -->
Esse documento destaca e consolida as melhores práticas de configuração apresentadas em todo o guia de usuário,
na documentação de introdução e nos exemplos.

Este é um documento vivo. Se você pensar em algo que não está nesta lista, mas pode ser útil para outras pessoas,
não hesite em criar uma *issue* ou submeter um PR.


<!-- body -->
## Dicas Gerais de Configuração

- Ao definir configurações, especifique a versão mais recente estável da API.

- Os arquivos de configuração devem ser armazenados em um sistema de controle antes de serem enviados ao cluster.
Isso permite que você reverta rapidamente uma alteração de configuração, caso necessário. Isso também auxilia na recriação e restauração do cluster.

- Escreva seus arquivos de configuração usando YAML ao invés de JSON. Embora esses formatos possam ser usados alternadamente em quase todos os cenários, YAML tende a ser mais amigável.

- Agrupe objetos relacionados em um único arquivo sempre que fizer sentido. Geralmente, um arquivo é mais fácil de
gerenciar do que vários. Veja o [guestbook-all-in-one.yaml](https://github.com/kubernetes/examples/tree/{{< param "githubbranch" >}}/guestbook/all-in-one/guestbook-all-in-one.yaml) como exemplo dessa sintaxe.

- Observe também que vários comandos `kubectl` podem ser chamados em um diretório. Por exemplo, você pode chamar
`kubectl apply` em um diretório de arquivos de configuração.

- Não especifique valores padrões desnecessariamente: configurações simples e mínimas diminuem a possibilidade de erros.

- Coloque descrições de objetos nas anotações para permitir uma melhor análise.


## "Naked" Pods comparados a ReplicaSets, Deployments, e Jobs {#naked-pods-vs-replicasets-deployments-and-jobs}

- Se você puder evitar, não use "naked" Pods (ou seja, se você puder evitar, pods não vinculados a um [ReplicaSet](/docs/concepts/workloads/controllers/replicaset/) ou [Deployment](/docs/concepts/workloads/controllers/deployment/)). 
Os "naked" pods não serão reconfigurados em caso de falha de um nó.

  Criar um Deployment, que cria um ReplicaSet para garantir que o número desejado de Pods esteja disponível e especifica uma estratégia para substituir os Pods (como [RollingUpdate](/docs/concepts/workloads/controllers/deployment/#rolling-update-deployment)), é quase sempre preferível do que criar Pods diretamente, exceto para alguns cenários explícitos de restartPolicy:Never. Um Job também pode ser apropriado.


## Services

- Crie o [Service](/docs/concepts/services-networking/service/) antes de suas cargas de trabalho de backend correspondentes (Deployments ou ReplicaSets) e antes de quaisquer cargas de trabalho que precisem acessá-lo. Quando o 
Kubernetes inicia um contêiner, ele fornece variáveis de ambiente apontando para todos os Services que estavam em execução quando o contêiner foi iniciado. Por exemplo, se um Service chamado `foo` existe, todos os contêineres vão
receber as seguintes variáveis em seu ambiente inicial:

  ```shell
  FOO_SERVICE_HOST=<o host em que o Service está executando>
  FOO_SERVICE_PORT=<a porta em que o Service está executando>
  ```

*Isso implica em um requisito de pedido* - qualquer `Service` que um `Pod` quer acessar precisa ser criado antes do `Pod` em si, ou então as variáveis de ambiente não serão populadas. O DNS não possui essa restrição.

- Um [cluster add-on](/docs/concepts/cluster-administration/addons/) opcional (embora fortemente recomendado) é um servidor DNS. O
servidor DNS monitora a API do Kubernetes buscando novos `Services` e cria um conjunto de DNS para cada um. Se o DNS foi habilitado em todo o cluster, então todos os `Pods` devem ser capazes de fazer a resolução de `Services` automaticamente.

- Não especifique um `hostPort` para um Pod a menos que isso seja absolutamente necessário. Quando você vincula um Pod a um `hostPort`, isso limita o número de lugares em que o Pod pode ser agendado, porque cada
combinação de <`hostIP`, `hostPort`, `protocol`> deve ser única. Se você não especificar o `hostIP` e `protocol` explicitamente, o Kubernetes vai usar `0.0.0.0` como o `hostIP` padrão e `TCP` como `protocol` padrão.

  Se você precisa de acesso a porta apenas para fins de depuração, pode usar o [apiserver proxy](/docs/tasks/access-application-cluster/access-cluster/#manually-constructing-apiserver-proxy-urls) ou o [`kubectl port-forward`](/docs/tasks/access-application-cluster/port-forward-access-application-cluster/).

  Se você precisa expor explicitamente a porta de um Pod no nó, considere usar um Service do tipo [NodePort](/docs/concepts/services-networking/service/#nodeport) antes de recorrer a `hostPort`.

- Evite usar `hostNetwork` pelos mesmos motivos do `hostPort`.

- Use [headless Services](/docs/concepts/services-networking/service/#headless-services) (que tem um `ClusterIP` ou `None`) para descoberta de serviço quando você não precisar de um balanceador de carga `kube-proxy`.
## Usando Labels

- Defina e use [labels](/docs/concepts/overview/working-with-objects/labels/) que identifiquem _atributos semânticos_ da sua aplicação ou Deployment, como `{ app: myapp, tier: frontend, phase: test, deployment: v3 }`. Você pode usar essas labels para selecionar os Pods apropriados para outros recursos; por exemplo, um Service que seleciona todos os Pods `tier: frontend`, ou todos
os componentes de `app: myapp`. Veja o app [guestbook](https://github.com/kubernetes/examples/tree/{{< param "githubbranch" >}}/guestbook/) para exemplos dessa abordagem.

Um Service pode ser feito para abranger vários Deployments, omitindo labels específicas de lançamento de seu seletor. Quando você
precisar atualizar um serviço em execução sem _downtime_, use um [Deployment](/docs/concepts/workloads/controllers/deployment/).

Um estado desejado de um objeto é descrito por um Deployment, e se as alterações nesse _spec_ forem _aplicadas_ o controlador 
do Deployment altera o estado real para o estado desejado em uma taxa controlada.

- Use as [labels comuns do Kubernetes](/docs/concepts/overview/working-with-objects/common-labels/) para casos de uso comuns.
Essas labels padronizadas enriquecem os metadados de uma forma que permite que ferramentas, incluindo `kubectl` e a [dashboard](/docs/tasks/access-application-cluster/web-ui-dashboard), funcionem de uma forma interoperável.

- Você pode manipular labels para depuração. Como os controladores do Kubernetes (como ReplicaSet) e Services se relacionam com os Pods usando seletor de labels, remover as labels relevantes de um Pod impedirá que ele seja considerado por um controlador ou que
seja atendido pelo tráfego de um Service. Se você remover as labels de um Pod existente, seu controlador criará um novo Pod para
substituí-lo. Essa é uma maneira útil de depurar um Pod anteriormente "ativo" em um ambiente de "quarentena". Para remover ou
alterar labels interativamente, use [`kubectl label`](/docs/reference/generated/kubectl/kubectl-commands#label).


## Imagens de Contêiner

A [imagePullPolicy](/docs/concepts/containers/images/#updating-images)  e tag da imagem afetam quando o [kubelet](/docs/reference/command-line-tools-reference/kubelet/) tenta puxar a imagem especificada.

- `imagePullPolicy: IfNotPresent`: a imagem é puxada apenas se ainda não estiver presente localmente.

- `imagePullPolicy: Always`: sempre que o kubelet inicia um contêiner, ele consulta o *registry* da imagem do contêiner para verificar o resumo de assinatura da imagem. Se o kubelet tiver uma imagem do contêiner com o mesmo resumo de assinatura
armazenado em cache localmente, o kubelet usará a imagem em cache, caso contrário, o kubelet baixa(*pulls*) a imagem com o resumo de assinatura resolvido, e usa essa imagem para iniciar o contêiner.

- `imagePullPolicy` é omitido se a tag da imagem é `:latest` ou se `imagePullPolicy` é omitido é automaticamente definido como `Always`. Observe que _não_ será utilizado para `ifNotPresent`se o valor da tag mudar.

- `imagePullPolicy` é omitido se uma tag da imagem existe mas não `:latest`: `imagePullPolicy` é automaticamente definido como `ifNotPresent`. Observe que isto _não_ será atualizado para `Always` se a tag for removida ou alterada para `:latest`.

- `imagePullPolicy: Never`: presume-se que a imagem exista localmente. Não é feita nenhuma tentativa de puxar a imagem.

{{< note >}}
Para garantir que seu contêiner sempre use a mesma versão de uma imagem, você pode especificar seu [resumo de assinatura](https://docs.docker.com/engine/reference/commandline/pull/#pull-an-image-by-digest-immutable-identifier); 
substitua `<nome-da-imagem>:<tag>` por `<nome-da-imagem>@<hash>` (por exemplo, `image@sha256:45b23dee08af5e43a7fea6c4cf9c25ccf269ee113168c19722f87876677c5cb2`). Esse resumo de assinatura identifica exclusivamente uma versão 
específica de uma imagem, então isso nunca vai ser atualizado pelo Kubernetes a menos que você mude o valor do resumo de assinatura da imagem.
{{< /note >}}

{{< note >}}
Você deve evitar o uso da tag `:latest` em produção, pois é mais difícil rastrear qual versão da imagem está sendo executada e mais difícil reverter adequadamente. 
{{< /note >}}

{{< note >}}
A semântica de cache do provedor de imagem subjacente torna até mesmo `imagePullPolicy: Always` eficiente, contanto que o registro esteja acessível de forma confiável. Com o Docker, por exemplo, se a imagem já existe, a tentativa de baixar(pull) é rápida porque todas as camadas da imagem são armazenadas em cache e nenhum download de imagem é necessário.
{{< /note >}}

## Usando kubectl

- Use `kubectl apply -f <directory>`. Isso procura por configurações do Kubernetes em todos os arquivos `.yaml`, `.yml` em `<directory>` e passa isso para `apply`.

- Use *labels selectors* para operações `get` e `delete` em vez de nomes de objetos específicos. Consulte as seções sobre [label selectors](/docs/concepts/overview/working-with-objects/labels/#label-selectors)
e [usando Labels efetivamente](/docs/concepts/cluster-administration/manage-deployment/#using-labels-effectively).

- Use `kubectl create deployment` e `kubectl expose` para criar rapidamente Deployments e Services de um único contêiner. Consulte [Use um Service para acessar uma aplicação em um cluster](/docs/tasks/access-application-cluster/service-access-application-cluster/) para obter um exemplo.
