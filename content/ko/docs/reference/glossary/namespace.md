---
title: 네임스페이스(Namespace)
id: namespace
date: 2018-04-12
full_link: /ko/docs/concepts/overview/working-with-objects/namespaces
short_description: >
  쿠버네티스에서 동일한 물리 클러스터에서 다중의 가상 클러스터를 지원하기 위해 사용하는 추상화.

aka: 
tags:
- fundamental
---
 쿠버네티스에서 동일한 물리 {{< glossary_tooltip text="클러스터" term_id="cluster" >}}에서 다중의 가상 클러스터를 지원하기 위해 사용하는 추상화.

<!--more--> 

네임스페이스는 클러스터의 오브젝트를 체계화하고 클러스터의 리소스를 분리하는 방법을 제공한다. 리소스의 이름은 네임스페이스 내에서 유일해야 한다. 그러나, 네임스페이스 간에서 유일할 필요는 없다.

