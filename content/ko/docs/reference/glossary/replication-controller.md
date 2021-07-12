---
title: 레플리케이션 컨트롤러(ReplicationController)
id: replication-controller
date: 2018-04-12
full_link: 
short_description: >
  (사용 중단된) 복제된 애플리케이션을 관리하는 API 오브젝트

aka: 
tags:
- workload
- core-object
---
 특정한 수의 {{< glossary_tooltip text="파드" term_id="pod" >}} 인스턴스가
실행 중인지 확인하면서 복제된 애플리케이션을 관리하는 워크로드 리소스이다.

<!--more--> 

컨트롤 플레인은 일부 파드에 장애가 발생하거나, 수동으로 파드를 삭제하거나,
실수로 너무 많은 수의 파드가 시작된 경우에도 정의된 수량의 파드가 실행되도록 한다.

{{< note >}}
레플리케이션컨트롤러는 사용 중단되었다. 유사한
것으로는 {{< glossary_tooltip text="디플로이먼트" term_id="deployment" >}}를 본다.
{{< /note >}}
