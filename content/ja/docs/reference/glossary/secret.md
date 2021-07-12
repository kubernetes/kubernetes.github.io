---
title: Secret
id: secret
date: 2018-04-12
full_link: /ja/docs/concepts/configuration/secret/
short_description: >
  パスワードやOAuthトークン、SSHキーのような機密の情報を保持します。

aka: 
tags:
- core-object
- security
---
 パスワードやOAuthトークン、SSHキーのような機密の情報を保持します。

<!--more--> 

機密情報の取り扱い方法を細かく制御することができ、保存時には[暗号化](/ja/docs/tasks/administer-cluster/encrypt-data/#ensure-all-secrets-are-encrypted)するなど、誤って公開してしまうリスクを減らすことができます。{{< glossary_tooltip text="Pod" term_id="pod" >}}は、ボリュームマウントされたファイルとして、またはPodのイメージをPullするkubeletによって、Secretを参照します。Secretは機密情報を扱うのに最適で、機密でない情報には[ConfigMap](/ja/docs/tasks/configure-pod-container/configure-pod-configmap/)が適しています。
