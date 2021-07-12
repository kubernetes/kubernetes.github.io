---
title: kube-controller-manager
id: kube-controller-manager
date: 2018-04-12
full_link: /docs/reference/command-line-tools-reference/kube-controller-manager/
short_description: >
  Składnik *master* odpowiedzialny za uruchamianie kontrolerów.

aka: 
tags:
- architecture
- fundamental
---
 Składnik warstwy sterowania odpowiedzialny za uruchamianie {{< glossary_tooltip text="kontrolerów" term_id="controller" >}}.

<!--more-->

Z poziomu podziału logicznego, każdy {{< glossary_tooltip text="kontroler" term_id="controller" >}} jest oddzielnym procesem, ale w celu zmniejszenia złożoności, wszystkie kontrolery są skompilowane do jednego programu binarnego i uruchamiane jako jeden proces.
