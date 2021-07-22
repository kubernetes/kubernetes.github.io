---
title: Gerenciando Secret usando kubectl
content_type: task
weight: 10
description: Criando objetos Secret usando a linha de comando kubectl.
---

<!-- overview -->

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}}

<!-- steps -->

## Criando um Secret

Um `Secret` pode conter credenciais de usuário requeridas por Pods para acesso a um banco de dados.
Por exemplo, uma string de conexão de banco de dados é composta por um usuário e senha.
Você pode armazenar o usuário em um arquivo `./username.txt` e a senha em um 
arquivo `./password.txt` na sua máquina local.

```shell
echo -n 'admin' > ./username.txt
echo -n '1f2d1e2e67df' > ./password.txt
```

A opção `-n` nos comandos acima garante que os arquivos criados não vão conter 
uma nova linha extra no final do arquivo de texto. Isso é importante porque
quando o `kubectl` lê um arquivo e codifica o conteúdo em uma string base64,
o caractere da nova linha extra também é codificado.

O comando `kubectl create secret` empacota os arquivos em um Secret e cria um
objeto no API server.


```shell
kubectl create secret generic db-user-pass \
  --from-file=./username.txt \
  --from-file=./password.txt
```

A saída deve ser similar a:

```
secret/db-user-pass created
```

O nome da chave padrão é o nome do arquivo. Opcionalmente, você pode definir
o nome da chave usando `--from-file=[key=]source`. Por exemplo:

```shell
kubectl create secret generic db-user-pass \
  --from-file=username=./username.txt \
  --from-file=password=./password.txt
```
Você não precisa escapar o caractere especial em senhas a partir de arquivos (`--from-file`).

Você também pode prover dados para Secret usando a tag `--from-literal=<key>=<value>`.
Essa tag pode ser especificada mais de uma vez para prover múltiplos pares de chave-valor.
Observe que caracteres especiais como `$`, `\`, `*`, `=`, e `!` vão ser interpretados
pelo seu [shell](https://en.wikipedia.org/wiki/Shell_(computing)) e precisam ser escapados.
Na maioria dos shells, a forma mais fácil de escapar as senhas é usar aspas simples (`'`).
Por exemplo, se sua senha atual é `S!B\*d$zDsb=`, você precisa executar o comando dessa forma:

```shell
kubectl create secret generic dev-db-secret \
  --from-literal=username=devuser \
  --from-literal=password='S!B\*d$zDsb='
```

## Verificando o Secret

Você pode verificar se o secret foi criado:

```shell
kubectl get secrets
```

A saída deve ser similar a:

```
NAME                  TYPE                                  DATA      AGE
db-user-pass          Opaque                                2         51s
```

Você pode ver a descrição do `Secret`:

```shell
kubectl describe secrets/db-user-pass
```
A saída deve ser similar a:

```
Name:            db-user-pass
Namespace:       default
Labels:          <none>
Annotations:     <none>

Type:            Opaque

Data
====
password:    12 bytes
username:    5 bytes
```

Os comandos `kubectl get` e `kubectl describe` omitem o conteúdo de um `Secret` por padrão.
Isso para proteger o `Secret` de ser exposto acidentalmente para uma pessoa não autorizada,
ou ser armazenado em um log de terminal.

## Decodificando o Secret  {#decoding-secret} 

Para ver o conteúdo de um Secret que você criou, execute o seguinte comando:

```shell
kubectl get secret db-user-pass -o jsonpath='{.data}'
```

A saída deve ser similar a:

```json
{"password":"MWYyZDFlMmU2N2Rm","username":"YWRtaW4="}
```

Agora, você pode decodificar os dados de `password`:

```shell
echo 'MWYyZDFlMmU2N2Rm' | base64 --decode
```

A saída deve ser similar a:

```
1f2d1e2e67df
```

## Limpeza

Para apagar o Secret que você criou:

```shell
kubectl delete secret db-user-pass
```

<!-- discussion -->

## {{% heading "whatsnext" %}}

- Leia mais sobre o [conceito do Secret](/docs/concepts/configuration/secret/)
- Leia sobre como [gerenciar Secret com o comando `kubectl`](/docs/tasks/configmap-secret/managing-secret-using-kubectl/)
- Leia sobre como [gerenciar Secret usando kustomize](/docs/tasks/configmap-secret/managing-secret-using-kustomize/)
