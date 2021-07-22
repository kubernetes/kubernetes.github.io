---
title: Gerenciando Secret usando Arquivo de Configuração
content_type: task
weight: 20
description: Criando objetos Secret usando arquivos de configuração de recursos.
---

<!-- overview -->

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}}

<!-- steps -->

## Crie o arquivo de configuração

Você pode criar um Secret primeiramente em um arquivo, no formato JSON ou YAML, e depois
criar o objeto. O recurso [Secret](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#secret-v1-core)
contém dois *maps*: `data` e `stringData`.
O campo `data` é usado para armazenar dados arbitrários, codificados usando base64. O
campo `stringData` é usado por conveniência, e permite que você use dados para um Secret
como *strings* não codificadas.
As chaves para `data` e `stringData` precisam ser compostas por caracteres alfanuméricos,
`_`, `-` ou `.`.

Por exemplo, para armazenar duas strings em um Secret usando o campo `data`, converta
as strings para base64 da seguinte forma:

```shell
echo -n 'admin' | base64
```
A saída deve ser similar a:

```
YWRtaW4=
```

```shell
echo -n '1f2d1e2e67df' | base64
```

A saída deve ser similar a:

```
MWYyZDFlMmU2N2Rm
```

Escreva o arquivo de configuração do Secret, que ser parecido com:
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: mysecret
type: Opaque
data:
  username: YWRtaW4=
  password: MWYyZDFlMmU2N2Rm
```

Perceba que o nome do objeto Secret precisa ser um 
[nome de subdomínio DNS](/docs/concepts/overview/working-with-objects/names#dns-subdomain-name) válido.

{{< note >}}
Os valores serializados dos dados JSON e YAML de um Secret são codificados em strings
base64. Novas linhas não são válidas com essas strings e devem ser omitidas. Quando
usar o utilitário `base64` em Darwin/MacOS, os usuários devem evitar usar a opção `-b`
para separar linhas grandes. Por outro lado, usuários de Linux *devem* adicionar a opção
`-w 0` ao comando `base64` ou o *pipe* `base64 | tr -d '\n'` se a opção `w` não for disponível 
{{< /note >}}

Para cenários específicos, você pode querer usar o campo `stringData` ao invés de `data`.
Esse campo permite que você use strings não-base64 diretamente dentro do Secret, 
e a string vai ser codificada para você quando o Secret for criado ou atualizado.

Um exemplo prático para isso pode ser quando você esteja fazendo *deploy* de uma aplicação
que usa um Secret para armazenar um arquivo de configuração, e você quer popular partes desse
arquivo de configuração durante o processo de *deployment*.

Por exemplo, se sua aplicação usa o seguinte arquivo de configuração:

```yaml
apiUrl: "https://my.api.com/api/v1"
username: "<user>"
password: "<password>"
```

Você pode armazenar isso em um Secret usando a seguinte definição:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: mysecret
type: Opaque
stringData:
  config.yaml: |
    apiUrl: "https://my.api.com/api/v1"
    username: <user>
    password: <password>
```

## Crie o objeto Secret

Agora, crie o Secret usando [`kubectl apply`](/docs/reference/generated/kubectl/kubectl-commands#apply):

```shell
kubectl apply -f ./secret.yaml
```

A saída deve ser similar a:

```
secret/mysecret created
```

## Verifique o Secret

O campo `stringData` é um campo de conveniência apenas de leitura. Ele nunca vai ser exibido
ao buscar um Secret. Por exemplo, se você executar o seguinte comando:

```shell
kubectl get secret mysecret -o yaml
```

A saída deve ser similar a:

```yaml
apiVersion: v1
kind: Secret
metadata:
  creationTimestamp: 2018-11-15T20:40:59Z
  name: mysecret
  namespace: default
  resourceVersion: "7225"
  uid: c280ad2e-e916-11e8-98f2-025000000001
type: Opaque
data:
  config.yaml: YXBpVXJsOiAiaHR0cHM6Ly9teS5hcGkuY29tL2FwaS92MSIKdXNlcm5hbWU6IHt7dXNlcm5hbWV9fQpwYXNzd29yZDoge3twYXNzd29yZH19
```

Os comandos `kubectl get` e `kubectl describe` omitem o conteúdo de um `Secret` por padrão.
Isso para proteger o `Secret` de ser exposto acidentalmente para uma pessoa não autorizada,
ou ser armazenado em um log de terminal.
Para verificar o conteúdo atual de um dado codificado, veja [decodificando secret](/docs/tasks/configmap-secret/managing-secret-using-kubectl/#decoding-secret).

Se um campo, como `username`, é especificado em `data` e `stringData`,
o valor de `stringData` é o usado. Por exemplo, dado a seguinte definição do Secret:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: mysecret
type: Opaque
data:
  username: YWRtaW4=
stringData:
  username: administrator
```

Resulta no seguinte Secret:

```yaml
apiVersion: v1
kind: Secret
metadata:
  creationTimestamp: 2018-11-15T20:46:46Z
  name: mysecret
  namespace: default
  resourceVersion: "7579"
  uid: 91460ecb-e917-11e8-98f2-025000000001
type: Opaque
data:
  username: YWRtaW5pc3RyYXRvcg==
```

Onde `YWRtaW5pc3RyYXRvcg==` é decodificado em `administrator`.

## Limpeza

Para apagar o Secret que você criou:

```shell
kubectl delete secret mysecret
```

## {{% heading "whatsnext" %}}

- Leia mais sobre o [conceito do Secret](/docs/concepts/configuration/secret/)
- Leia sobre como [gerenciar Secret com o comando `kubectl`](/docs/tasks/configmap-secret/managing-secret-using-kubectl/)
- Leia sobre como [gerenciar Secret usando kustomize](/docs/tasks/configmap-secret/managing-secret-using-kustomize/)

