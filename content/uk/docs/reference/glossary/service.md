---
title: Service
id: service
date: 2018-04-12
full_link: /docs/concepts/services-networking/service/
# A way to expose an application running on a set of Pods as a network service.
short_description: >
  Спосіб відкрити доступ до застосунку, що запущений на декількох Pod'ах у вигляді мережевої служби.

aka:
tags:
- fundamental
- core-object
---
<!--
An abstract way to expose an application running on a set of  as a network service.
-->
Це абстрактний спосіб відкрити доступ до застосунку, що працює як один (або декілька) {{< glossary_tooltip text="Pod'ів" term_id="pod" >}} у вигляді мережевої служби.

<!--more-->

<!--The set of Pods targeted by a Service is (usually) determined by a {{< glossary_tooltip text="selector" term_id="selector" >}}. If more Pods are added or removed, the set of Pods matching the selector will change. The Service makes sure that network traffic can be directed to the current set of Pods for the workload.
-->
Переважно група Pod'ів визначається як Service за допомогою {{< glossary_tooltip text="селектора" term_id="selector" >}}. Додання або вилучення Pod'ів змінить групу Pod'ів, визначених селектором. Service забезпечує надходження мережевого трафіка до актуальної групи Pod'ів для підтримки робочого навантаження.
