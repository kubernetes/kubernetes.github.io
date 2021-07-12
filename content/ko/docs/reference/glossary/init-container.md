---
title: 초기화 컨테이너(Init Container)
id: init-container
date: 2018-04-12
full_link:
short_description: >
  앱 컨테이너가 동작하기 전에 완료되기 위해 실행되는 하나 이상의 초기화 컨테이너.

aka:
tags:
- fundamental
---
 앱 컨테이너가 동작하기 전에 완료되기 위해 실행되는 하나 이상의 초기화 {{< glossary_tooltip text="컨테이너" term_id="container" >}}.

<!--more-->

한 가지 차이점을 제외하면, 초기화 컨테이너는 일반적인 앱 컨테이너와 동일하다. 초기화 컨테이너는 앱 컨테이너가 시작되기 전에 완료되는 것을 목표로 실행되어야 한다. 초기화 컨테이너는 연달아 실행된다. 다시말해, 각 초기화 컨테이너의 실행은 다음 초기화 컨테이너가 시작되기 전에 완료되어야 한다.
