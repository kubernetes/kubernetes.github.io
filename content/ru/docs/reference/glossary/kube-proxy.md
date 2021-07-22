---
title: kube-proxy
id: kube-proxy
date: 2018-04-12
full_link: /docs/reference/command-line-tools-reference/kube-proxy/
short_description: >
  `kube-proxy` — сетевой прокси, работающий на каждом узле в кластере.

aka:
tags:
- fundamental
- networking
---
 [kube-proxy](/docs/reference/command-line-tools-reference/kube-proxy/) — сетевой прокси, работающий на каждом узле в кластере, и реализующий часть концепции {{< glossary_tooltip text="сервис" term_id="service">}}.

<!--more-->

kube-proxy конфигурирует правила сети на узлах. При помощи них разрешаются сетевые подключения к вашими подам изнутри и снаружи кластера.

kube-proxy использует уровень фильтрации пакетов в операционной системы, если он доступен. В противном случае, kube-proxy сам обрабатывает передачу сетевого трафика.