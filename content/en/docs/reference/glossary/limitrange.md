---
title: LimitRange
id: limitrange
date: 2019-04-15
full_link:  /docs/concepts/policy/limit-range/
short_description: >
  Provides constraints to limit resource consumption per Containers or Pods in a namespace.

aka: 
tags:
- core-object
- fundamental
- architecture
related:
 - pod
 - container

---
 Provides constraints to limit resource consumption per {{< glossary_tooltip text="Containers" term_id="container" >}} or {{< glossary_tooltip text="Pods" term_id="pod" >}} in a namespace.

<!--more--> 
LimitRange limits the quantity of objects that can be created  by type, 
as well as the amount of compute resources that may be requested/consumed by individual {{< glossary_tooltip text="Containers" term_id="container" >}} or {{< glossary_tooltip text="Pods" term_id="pod" >}} in a namespace.