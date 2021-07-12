---
title: 컨피그맵(ConfigMap)
id: configmap
date: 2018-04-12
full_link: /docs/concepts/configuration/configmap/
short_description: >
  키-값 쌍으로 기밀이 아닌 데이터를 저장하는 데 사용하는 API 오브젝트이다. 볼륨에서 환경 변수, 커맨드-라인 인수 또는 구성 파일로 사용될 수 있다.

aka:
tags:
- core-object
---
 키-값 쌍으로 기밀이 아닌 데이터를 저장하는 데 사용하는 API 오브젝트이다.
{{< glossary_tooltip text="파드" term_id="pod" >}}는
{{< glossary_tooltip text="볼륨" term_id="volume" >}}에서
환경 변수, 커맨드-라인 인수 또는 구성 파일로 컨피그맵을 사용할 수 있다.

<!--more-->

컨피그맵을 사용하면 {{< glossary_tooltip text="컨테이너 이미지" term_id="image" >}}에서 환경별 구성을 분리하여, 애플리케이션을 쉽게 이식할 수 있다.
