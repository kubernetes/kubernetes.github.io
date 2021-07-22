---
title: API-сервер
id: kube-apiserver
date: 2018-04-12
full_link: /docs/reference/generated/kube-apiserver/
short_description: >
  Компонент панели управления, обслуживающий API Kubernetes.

aka:
- kube-apiserver
tags:
- architecture
- fundamental
---
 Сервер API — компонент Kubernetes
{{< glossary_tooltip text="панели управления" term_id="control-plane" >}}, который представляет API Kubernetes.
API-сервер — это клиентская часть панели управления Kubernetes

<!--more-->

Основной реализацией API-сервера Kubernetes является [kube-apiserver](/docs/reference/generated/kube-apiserver/).
kube-apiserver предназначен для горизонтального масштабирования, то есть развёртывание на несколько экземпляров.
Вы можете запустить несколько экземпляров kube-apiserver и сбалансировать трафик между этими экземплярами.
