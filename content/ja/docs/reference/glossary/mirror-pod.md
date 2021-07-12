---
title: ミラーPod
id: mirror-pod
date: 2019-08-06
short_description: >
  kubelet上のstatic Podを追跡するAPIサーバー内のオブジェクトです。

aka: 
tags:
- fundamental
---
kubeletが{{< glossary_tooltip text="static Pod" term_id="static-pod" >}}を代表するために使用する{{< glossary_tooltip text="Pod" term_id="pod" >}}オブジェクトです。

<!--more--> 

kubeletが設定の中にstatic Podを発見すると、static Podに対応するPodオブジェクトをKubernetes APIサーバー上に自動的に作成しようとします。つまり、APIサーバーからはPodが見えていますが、制御まではできないということです。

(たとえば、ミラーPodを削除しても、kubeletデーモンが対応するPodの実行を停止することはありません。)
