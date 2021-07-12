---
title: 잡(Job)
id: job
date: 2018-04-12
full_link: /docs/concepts/workloads/controllers/job
short_description: >
  완료를 목표로 실행되는 유한 또는 배치 작업.

aka: 
tags:
- fundamental
- core-object
- workload
---
 완료를 목표로 실행되는 유한 또는 배치 작업.

<!--more--> 

하나 이상의 {{< glossary_tooltip text="파드" term_id="pod" >}} 오브젝트를 생성하고 지정된 수의 파드가 성공적으로 종료되는지 확인한다. 파드가 성공적으로 완료됨에 따라, 잡은 해당 성공적인 완료를 추적한다.

