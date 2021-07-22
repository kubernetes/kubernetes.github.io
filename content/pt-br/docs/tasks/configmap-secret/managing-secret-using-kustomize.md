---
title: Gerenciando Secret usando Kustomize
content_type: task
weight: 30
description: Criando objetos Secret usando o arquivo kustomization.yaml
---

<!-- overview -->

Desde o Kubernetes v1.14, o `kubectl` provê suporte para [gerenciamento de objetos usando Kustomize](/docs/tasks/manage-kubernetes-objects/kustomization/).
O Kustomize provê geradores de recursos para criar Secrets e ConfigMaps. 
Os geradores Kustomize devem ser especificados em um arquivo `kustomization.yaml` dentro
de um diretório. Depois de gerar o Secret, você pode criar o Secret na API server com `kubectl apply`.
## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}}

<!-- steps -->

## Criando um arquivo de Kustomization
Você pode criar um Secret definindo um `secretGenerator` em um 
arquivo `kustomization.yaml` que referencia outros arquivos existentes.
Por exemplo, o seguinte arquivo kustomization referencia os
arquivos `./username.txt` e `./password.txt`:

```yaml
secretGenerator:
- name: db-user-pass
  files:
  - username.txt
  - password.txt
```

Você também pode definir o `secretGenerator`no arquivo `kustomization.yaml`
por meio de alguns *literais*.
Por exemplo, o seguinte arquivo `kustomization.yaml` contém dois literais
para `username` e `password` respectivamente:

```yaml
secretGenerator:
- name: db-user-pass
  literals:
  - username=admin
  - password=1f2d1e2e67df
```

Observe que nos dois casos, você não precisa codificar os valores em base64.

## Criando o Secret

Aplique o diretório que contém o arquivo `kustomization.yaml` para criar o Secret.

```shell
kubectl apply -k .
```

A saída deve ser similar a:

```
secret/db-user-pass-96mffmfh4k created
```

Observe que quando um Secret é gerado, o nome do segredo é criado usando o hash
dos dados do Secret mais o valor do hash. Isso garante que
um novo Secret é gerado cada vez que os dados são modificados.

## Verifique o Secret criado

Você pode verificar que o secret foi criado:

```shell
kubectl get secrets
```

A saída deve ser similar a:

```
NAME                             TYPE                                  DATA      AGE
db-user-pass-96mffmfh4k          Opaque                                2         51s
```

Você pode ver a descrição de um secret:

```shell
kubectl describe secrets/db-user-pass-96mffmfh4k
```
A saída deve ser similar a:

```
Name:            db-user-pass-96mffmfh4k
Namespace:       default
Labels:          <none>
Annotations:     <none>

Type:            Opaque

Data
====
password.txt:    12 bytes
username.txt:    5 bytes
```

Os comandos `kubectl get` e `kubectl describe` omitem o conteúdo de um `Secret` por padrão.
Isso para proteger o `Secret` de ser exposto acidentalmente para uma pessoa não autorizada,
ou ser armazenado em um log de terminal.
Para verificar o conteúdo atual de um dado codificado, veja [decodificando secret](/docs/tasks/configmap-secret/managing-secret-using-kubectl/#decoding-secret).

## Limpeza

Para apagar o Secret que você criou:

```shell
kubectl delete secret db-user-pass-96mffmfh4k
```

<!-- Optional section; add links to information related to this topic. -->
## {{% heading "whatsnext" %}}

- Leia mais sobre o [conceito do Secret](/docs/concepts/configuration/secret/)
- Leia sobre como [gerenciar Secret com o comando `kubectl`](/docs/tasks/configmap-secret/managing-secret-using-kubectl/)
- Leia sobre como [gerenciar Secret usando kustomize](/docs/tasks/configmap-secret/managing-secret-using-kustomize/)

