---
title: Kustomizeを使用してSecretを管理する
content_type: task
weight: 30
description: kustomization.yamlを使用してSecretを作成する
---

<!-- overview -->

Kubernetes v1.14以降、`kubectl`は[Kustomizeを使ったオブジェクト管理](/docs/tasks/manage-kubernetes-objects/kustomization/)をサポートしています。
KustomizeはSecretやConfigMapを作成するためのリソースジェネレーターを提供します。
Kustomizeジェネレーターは、ディレクトリ内の`kustomization.yaml`ファイルで指定します。
Secretを生成したら、`kubectl apply`でAPIサーバー上にSecretを作成します。

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}}

<!-- steps -->

## Kustomizationファイルを作成する

`kustomization.yaml`ファイルの中で`secretGenerator`を定義し、他の既存のファイルを参照することで、Secretを生成することができます。
たとえば、以下のkustomizationファイルは`./username.txt`と`./password.txt`を参照しています。

```yaml
secretGenerator:
- name: db-user-pass
  files:
  - username.txt
  - password.txt
```

また、`kustomization.yaml`ファイルの中でリテラルを指定して`secretGenerator`を定義することもできます。
たとえば、以下の`kustomization.yaml`ファイルには`username`と`password`の2つのリテラルが含まれています。

```yaml
secretGenerator:
- name: db-user-pass
  literals:
  - username=admin
  - password=1f2d1e2e67df
```

また、`kustomization.yaml`ファイルに`.env`ファイルを用意して`secretGenerator`を定義することもできます。
たとえば、以下の`kustomization.yaml`ファイルは、`.env.secret`ファイルからデータを取り込みます。

```yaml
secretGenerator:
- name: db-user-pass
  envs:
  - .env.secret
```

なお、いずれの場合も、値をbase64エンコードする必要はありません。

## Secretを作成する

`kustomization.yaml`を含むディレクトリを適用して、Secretを作成します。

```shell
kubectl apply -k .
```

出力は次のようになります:

```
secret/db-user-pass-96mffmfh4k created
```

なお、Secretを生成する際には、データをハッシュ化し、そのハッシュ値を付加することでSecret名を生成します。
これにより、データが変更されるたびに、新しいSecretが生成されます。

## 作成したSecretを確認する

Secretが作成されたことを確認できます:

```shell
kubectl get secrets
```

出力は次のようになります:

```
NAME                             TYPE                                  DATA      AGE
db-user-pass-96mffmfh4k          Opaque                                2         51s
```

Secretの説明を参照できます:

```shell
kubectl describe secrets/db-user-pass-96mffmfh4k
```

出力は次のようになります:

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

`kubectl get`と`kubectl describe`コマンドはデフォルトではSecretの内容を表示しません。
これは、Secretが不用意に他人にさらされたり、ターミナルログに保存されたりしないようにするためです。
エンコードされたデータの実際の内容を確認するには、[Secretのデコード](/ja/docs/tasks/configmap-secret/managing-secret-using-kubectl/#decoding-secret)を参照してください。

## クリーンアップ

作成したSecretを削除するには次のコマンドを実行します:

```shell
kubectl delete secret db-user-pass-96mffmfh4k
```

<!-- Optional section; add links to information related to this topic. -->
## {{% heading "whatsnext" %}}

- [Secretのコンセプト](/ja/docs/concepts/configuration/secret/)を読む
- [kubectlを使用してSecretを管理する](/ja/docs/tasks/configmap-secret/managing-secret-using-kubectl/)方法を知る
- [設定ファイルを使用してSecretを管理する](/ja/docs/tasks/configmap-secret/managing-secret-using-config-file/)方法を知る

