---
title: Políticas de rede
content_type: concept
weight: 50
---

<!-- overview -->

Se você deseja controlar o fluxo do tráfego de rede no nível do endereço IP ou de portas TCP e UDP 
(camadas OSI 3 e 4) então você deve considerar usar Políticas de rede (`NetworkPolicies`) do Kubernetes para aplicações
no seu cluster. `NetworkPolicy` é um objeto focado em aplicações/experiência do desenvolvedor 
que permite especificar como é permitido a um {{< glossary_tooltip text="pod" term_id="pod">}} 
comunicar-se com várias "entidades" de rede.

As entidades que um Pod pode se comunicar são identificadas através de uma combinação dos 3 
identificadores à seguir:

1. Outros pods que são permitidos (exceção: um pod não pode bloquear a si próprio)
2. Namespaces que são permitidos
3. Blocos de IP (exceção: o tráfego de e para o nó que um Pod está executando sempre é permitido,
independentemente do endereço IP do Pod ou do Nó)

Quando definimos uma política de rede baseada em pod ou namespace, utiliza-se um {{< glossary_tooltip text="selector" term_id="selector">}}
para especificar qual tráfego é permitido de e para o(s) Pod(s) que correspondem ao seletor.

Quando uma política de redes baseada em IP é criada, nós definimos a política baseada em blocos de IP (faixas CIDR).

<!-- body -->
## Pré requisitos

As políticas de rede são implementadas pelo [plugin de redes](/docs/concepts/extend-kubernetes/compute-storage-net/network-plugins/).  Para usar 
uma política de redes, você deve usar uma solução de redes que suporte o objeto `NetworkPolicy`.
A criação de um objeto `NetworkPolicy` sem um controlador que implemente essas regras não tem efeito.

## Pods isolados e não isolados

Por padrão, pods não são isolados; eles aceitam tráfego de qualquer origem.

Os pods tornam-se isolados ao existir uma `NetworkPolicy` que selecione eles. Uma vez que
exista qualquer `NetworkPolicy` no namespace selecionando um pod em específico, aquele pod 
irá rejeitar qualquer conexão não permitida por qualquer `NetworkPolicy`. (Outros pod no mesmo 
namespace que não são selecionados por nenhuma outra `NetworkPolicy` irão continuar aceitando
todo tráfego de rede.)

As políticas de rede não conflitam; elas são aditivas. Se qualquer política selecionar um pod, 
o pod torna-se restrito ao que é permitido pela união das regras de entrada/saída de tráfego definidas
nas políticas. Assim, a ordem de avaliação não afeta o resultado da política.

Para o fluxo de rede entre dois pods ser permitido, tanto a política de saída no pod de origem 
e a política de entrada no pod de destino devem permitir o tráfego. Se a política de saída na 
origem, ou a política de entrada no destino negar o tráfego, o tráfego será bloqueado.

## O recurso NetworkPolicy {#networkpolicy-resource}

Veja a referência [NetworkPolicy](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#networkpolicy-v1-networking-k8s-io) para uma definição completa do recurso.

Uma `NetworkPolicy` de exemplo é similar ao abaixo:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: test-network-policy
  namespace: default
spec:
  podSelector:
    matchLabels:
      role: db
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - ipBlock:
        cidr: 172.17.0.0/16
        except:
        - 172.17.1.0/24
    - namespaceSelector:
        matchLabels:
          project: myproject
    - podSelector:
        matchLabels:
          role: frontend
    ports:
    - protocol: TCP
      port: 6379
  egress:
  - to:
    - ipBlock:
        cidr: 10.0.0.0/24
    ports:
    - protocol: TCP
      port: 5978
```

{{< note >}}
Criar esse objeto no seu cluster não terá efeito a não ser que você escolha uma 
solução de redes que suporte políticas de rede.
{{< /note >}}

__Campos obrigatórios__: Assim como todas as outras configurações do Kubernetes, uma `NetworkPolicy`
necessita dos campos `apiVersion`, `kind` e `metadata`. Para maiores informações sobre 
trabalhar com arquivos de configuração, veja 
[Configurando containeres usando ConfigMap](/docs/tasks/configure-pod-container/configure-pod-configmap/),
e [Gerenciamento de objetos](/docs/concepts/overview/working-with-objects/object-management).

__spec__: A [spec](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md#spec-and-status) contém todas as informações necessárias
para definir uma política de redes em um namespace.

__podSelector__: Cada `NetworkPolicy` inclui um `podSelector` que seleciona o grupo de pods
que a política se aplica. A política acima seleciona os pods com a _label_ "role=db". Um `podSelector`
vazio seleciona todos os pods no namespace.

__policyTypes__: Cada `NetworkPolicy` inclui uma lista de `policyTypes` que pode incluir `Ingress`, 
`Egress` ou ambos. O campo `policyTypes` indica se a política se aplica ao tráfego de entrada 
com destino aos pods selecionados, o tráfego de saída com origem dos pods selecionados ou ambos.
Se nenhum `policyType` for definido então por padrão o tipo `Ingress` será sempre utilizado, e o 
tipo `Egress` será configurado apenas se o objeto contiver alguma regra de saída. (campo `egress` a seguir).

__ingress__:  Cada `NetworkPolicy` pode incluir uma lista de regras de entrada permitidas através do campo `ingress`. 
Cada regra permite o tráfego que corresponde simultaneamente às sessões `from` (de) e `ports` (portas). 
A política de exemplo acima contém uma regra simples, que corresponde ao tráfego em uma única porta, 
de uma das três origens definidas, sendo a primeira definida via `ipBlock`, a segunda via `namespaceSelector` e 
a terceira via `podSelector`.

__egress__: Cada política pode incluir uma lista de regras de regras de saída permitidas através do campo `egress`.
Cada regra permite o tráfego que corresponde simultaneamente às sessões `to` (para) e `ports` (portas).
A política de exemplo acima contém uma regra simples, que corresponde ao tráfego destinado a uma 
porta em qualquer destino pertencente à faixa de IPs em `10.0.0.0/24`.

Então a `NetworkPolicy` acima:

1. Isola os pods no namespace "default" com a _label_ "role=db" para ambos os tráfegos de entrada
e saída (se eles ainda não estavam isolados)
2. (Regras de entrada/ingress) permite conexões para todos os pods no namespace "default" com a _label_ "role=db" na porta TCP 6379 de:

   * qualquer pod no namespace "default" com a _label_ "role=frontend"
   * qualquer pod em um namespace que tenha a _label_ "project=myproject" (aqui cabe ressaltar que o namespace que deve ter a _label_ e não os pods dentro desse namespace)
   * IPs dentro das faixas 172.17.0.0–172.17.0.255 e 172.17.2.0–172.17.255.255 (ex.:, toda 172.17.0.0/16 exceto 172.17.1.0/24)

3. (Regras de saída/egress) permite conexões de qualquer pod no namespace "default" com a _label_
"role=db" para a faixa de destino 10.0.0.0/24 na porta TCP 5978.

Veja o tutorial [Declarando uma política de redes](/docs/tasks/administer-cluster/declare-network-policy/) para mais exemplos.

## Comportamento dos seletores `to` e `from`

Existem quatro tipos de seletores que podem ser especificados nas sessões `ingress.from` ou 
`egress.to`:

__podSelector__: Seleciona Pods no mesmo namespace que a política de rede foi criada, e que deve 
ser permitido origens no tráfego de entrada ou destinos no tráfego de saída.

__namespaceSelector__: Seleciona namespaces para o qual todos os Pods devem ser permitidos como 
origens no caso de tráfego de entrada ou destino no tráfego de saída.

__namespaceSelector__ *e* __podSelector__: Uma entrada `to`/`from` única que permite especificar 
ambos `namespaceSelector` e `podSelector` e seleciona um conjunto de Pods dentro de um namespace.
Seja cuidadoso em utilizar a sintaxe YAML correta; essa política:

```yaml
  ...
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          user: alice
      podSelector:
        matchLabels:
          role: client
  ...
```
contém um único elemento `from` permitindo conexões de Pods com a label `role=client` em 
namespaces com a _label_  `user=alice`. Mas *essa* política:

```yaml
  ...
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          user: alice
    - podSelector:
        matchLabels:
          role: client
  ...
```

contém dois elementos no conjunto `from` e permite conexões de Pods no namespace local com 
a _label_ `role=client`, *OU* de qualquer outro Pod em qualquer outro namespace que tenha 
a label `user=alice`.

Quando estiver em dúvida, utilize o comando `kubectl describe` para verificar como o 
Kubernetes interpretou a política.

__ipBlock__: Isso seleciona um conjunto particular de faixas de IP a serem permitidos como 
origens no caso de entrada ou destinos no caso de saída. Devem ser considerados IPs externos
ao cluster, uma vez que os IPs dos Pods são efêmeros e imprevisíveis.

Os mecanismos de entrada e saída do cluster geralmente requerem que os IPs de origem ou destino
sejam reescritos. Em casos em que isso aconteça, não é definido se deve acontecer antes ou 
depois do processamento da `NetworkPolicy` que corresponde a esse tráfego, e o comportamento
pode ser diferente para cada plugin de rede, provedor de nuvem, implementação de `Service`, etc.

No caso de tráfego de entrada, isso significa que em alguns casos você pode filtrar os pacotes 
de entrada baseado no IP de origem atual, enquanto que em outros casos o IP de origem que 
a `NetworkPolicy` atua pode ser o IP de um `LoadBalancer` ou do Nó em que o Pod está executando.

No caso de tráfego de saída, isso significa que conexões de Pods para `Services` que são reescritos
para IPs externos ao cluster podem ou não estar sujeitos a políticas baseadas no campo `ipBlock`.

## Políticas padrão

Por padrão, se nenhuma política existir no namespace, então todo o tráfego de entrada e saída é 
permitido de e para os pods nesse namespace. Os exemplos a seguir permitem a você mudar o 
comportamento padrão nesse namespace.

### Bloqueio padrão de todo tráfego de entrada

Você pode criar uma política padrão de isolamento para um namespace criando um objeto `NetworkPolicy` 
que seleciona todos os pods mas não permite o tráfego de entrada para esses pods.

{{< codenew file="service/networking/network-policy-default-deny-ingress.yaml" >}}

Isso garante que mesmo pods que não são selecionados por nenhuma outra política de rede ainda 
serão isolados. Essa política não muda o comportamento padrão de isolamento de tráfego de saída 
nesse namespace.

### Permitir por padrão todo tráfego de entrada

Se você deseja permitir todo o tráfego de todos os pods em um namespace (mesmo que políticas que 
sejam adicionadas faça com que alguns pods sejam tratados como "isolados"), você pode criar 
uma política que permite explicitamente todo o tráfego naquele namespace.

{{< codenew file="service/networking/network-policy-allow-all-ingress.yaml" >}}

### Bloqueio padrão de todo tráfego de saída

Você pode criar uma política de isolamento de saída padrão para um namespace criando uma 
política de redes que selecione todos os pods, mas não permita o tráfego de saída a partir 
de nenhum desses pods.

{{< codenew file="service/networking/network-policy-default-deny-egress.yaml" >}}

Isso garante que mesmo pods que não são selecionados por outra política de rede não seja permitido 
tráfego de saída. Essa política não muda o comportamento padrão de tráfego de entrada.

### Permitir por padrão todo tráfego de saída

Caso você queira permitir todo o tráfego de todos os pods em um namespace (mesmo que políticas sejam 
adicionadas e cause com que alguns pods sejam tratados como "isolados"), você pode criar uma 
política explicita que permite todo o tráfego de saída no namespace.

{{< codenew file="service/networking/network-policy-allow-all-egress.yaml" >}}

### Bloqueio padrão de todo tráfego de entrada e saída

Você pode criar uma política padrão em um namespace que previne todo o tráfego de entrada 
E saída criando a política a seguir no namespace.

{{< codenew file="service/networking/network-policy-default-deny-all.yaml" >}}

Isso garante que mesmo pods que não são selecionados por nenhuma outra política de redes não 
possuam permissão de tráfego de entrada ou saída.

## Selecionando uma faixa de portas

{{< feature-state for_k8s_version="v1.21" state="alpha" >}}

Ao escrever uma política de redes, você pode selecionar uma faixa de portas ao invés de uma 
porta única, utilizando-se do campo `endPort` conforme a seguir:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: multi-port-egress
  namespace: default
spec:
  podSelector:
    matchLabels:
      role: db
  policyTypes:
  - Egress
  egress:
  - to:
    - ipBlock:
        cidr: 10.0.0.0/24
    ports:
    - protocol: TCP
      port: 32000
      endPort: 32768
```

A regra acima permite a qualquer Pod com a _label_ "role=db" no namespace `default` de se comunicar 
com qualquer IP na faixa `10.0.0.0/24` através de protocolo TCP, desde que a porta de destino 
esteja na faixa entre 32000 e 32768.

As seguintes restrições aplicam-se ao se utilizar esse campo:

* Por ser uma funcionalidade "alpha", ela é desativada por padrão. Para habilitar o campo `endPort` 
no cluster, você (ou o seu administrador do cluster) deve habilitar o [feature gate](/docs/reference/command-line-tools-reference/feature-gates/) `NetworkPolicyEndPort` no `kube-apiserver` com a flag `--feature-gates=NetworkPolicyEndPort=true,...`.
* O valor de `endPort` deve ser igual ou maior ao valor do campo `port`.
* O campo `endPort` só pode ser definido se o campo `port` também for definido.
* Ambos os campos `port` e `endPort` devem ser números.

{{< note >}}
Seu cluster deve utilizar um plugin {{< glossary_tooltip text="CNI" term_id="cni" >}}
que suporte o campo `endPort` na especificação da política de redes.
{{< /note >}}

## Selecionando um Namespace pelo seu nome

{{< feature-state state="beta" for_k8s_version="1.21" >}}

A camada de gerenciamento do Kubernetes configura uma _label_ imutável `kubernetes.io/metadata.name` em 
todos os namespaces, uma vez que o [feature gate](/docs/reference/command-line-tools-reference/feature-gates/) esteja habilitado por padrão.
O valor dessa _label_  é o nome do namespace.

Enquanto que um objeto `NetworkPolicy` não pode selecionar um namespace pelo seu nome através de 
um campo específico, você pode utilizar essa _label_ padrão para selecionar um namespace pelo seu nome.

## O que você não pode fazer com `NetworkPolicies` (ao menos por enquanto!)
Por enquanto no Kubernetes {{< skew latestVersion >}} as funcionalidades a seguir não existem 
mas você pode conseguir implementar de forma alternativa utilizando componentes do Sistema Operacional 
(como SELinux, OpenVSwitch, IPtables, etc) ou tecnologias da camada 7 OSI (Ingress controllers, implementações de service mesh) ou ainda _admission controllers_. 
No caso do assunto "segurança de redes no Kubernetes" ser novo para você, vale notar que as 
histórias de usuário a seguir ainda não podem ser implementadas:

- Forçar o tráfego interno do cluster passar por um gateway comum (pode ser implementado via service mesh ou outros proxies)
- Qualquer coisa relacionada a TLS/mTLS (use um service mesh ou ingress controller para isso)
- Políticas específicas a nível do nó kubernetes (você pode utilizar as notações de IP CIDR para isso, mas não pode selecionar nós Kubernetes por suas identidades)
- Selecionar `Services` pelo seu nome (você pode, contudo, selecionar pods e namespaces por seus {{< glossary_tooltip text="labels" term_id="label" >}} o que torna-se uma solução de contorno viável).
- Criação ou gerenciamento 
- Políticas padrão que são aplicadas a todos os namespaces e pods (existem alguns plugins externos do Kubernetes e projetos que podem fazer isso, e a comunidade está trabalhando nessa especificação).
- Ferramental de testes para validação de políticas de redes.
- Possibilidade de logar eventos de segurança de redes (conexões bloqueadas, aceitas). Existem plugins CNI que conseguem fazer isso à parte.
- Possibilidade de explicitamente negar políticas de rede (o modelo das `NetworkPolicies` são "negar por padrão e conforme a necessidade, deve-se adicionar regras que permitam o tráfego).
- Bloquear o tráfego que venha da interface de loopback/localhost ou que venham do nó em que o Pod se encontre.

## {{% heading "whatsnext" %}}


- Veja o tutorial [Declarando políticas de redes](/docs/tasks/administer-cluster/declare-network-policy/) para mais exemplos.
- Veja mais [cenários comuns e exemplos](https://github.com/ahmetb/kubernetes-network-policy-recipes) de políticas de redes.
