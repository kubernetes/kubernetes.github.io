---
title: 스테이트풀셋(StatefulSet)
id: statefulset
date: 2018-04-12
full_link: /ko/docs/concepts/workloads/controllers/statefulset/
short_description: >
  내구성이 있는 스토리지와 파드별로 지속성 식별자를 사용해서 파드 집합의 디플로이먼트와 스케일링을 관리한다.

aka:
tags:
- fundamental
- core-object
- workload
- storage
---
 {{< glossary_tooltip text="파드" term_id="pod" >}} 집합의 디플로이먼트와 스케일링을 관리하며, 파드들의 *순서 및 고유성을 보장한다* .

<!--more-->

{{< glossary_tooltip text="디플로이먼트" term_id="deployment" >}}와 유사하게, 스테이트풀셋은 동일한 컨테이너 스펙을 기반으로 둔 파드들을 관리한다. 디플로이먼트와는 다르게, 스테이트풀셋은 각 파드의 독자성을 유지한다. 이 파드들은 동일한 스팩으로 생성되었지만, 서로 교체는 불가능하다. 다시 말해, 각각은 재스케줄링 간에도 지속적으로 유지되는 식별자를 가진다.

스토리지 볼륨을 사용해서 워크로드에 지속성을 제공하려는 경우, 솔루션의 일부로 스테이트풀셋을 사용할 수 있다. 스테이트풀셋의 개별 파드는 장애에 취약하지만, 퍼시스턴트 파드 식별자는 기존 볼륨을 실패한 볼륨을 대체하는 새 파드에 더 쉽게 일치시킬 수 있다.
