---
title: 이름(Name)
id: name
date: 2018-04-12
full_link: /ko/docs/concepts/overview/working-with-objects/names
short_description: >
  `/api/v1/pods/some-name`과 같이, 리소스 URL에서 오브젝트를 가리키는 클라이언트 제공 문자열.

aka: 
tags:
- fundamental
---
 `/api/v1/pods/some-name`과 같이, 리소스 URL에서 오브젝트를 가리키는 클라이언트 제공 문자열.

<!--more--> 

특정 시점에 같은 종류(kind) 내에서는 하나의 이름은 하나의 오브젝트에만 지정될 수 있다. 하지만, 오브젝트를 삭제한 경우, 삭제된 오브젝트와 같은 이름을 새로운 오브젝트에 지정 가능하다.

