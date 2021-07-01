---
title: Job
id: job
date: 2018-04-12
full_link: /docs/concepts/workloads/controllers/job/
short_description: >
  A finite or batch task that runs to completion.

aka: 
tags:
- fundamental
- core-object
- workload
---
 A finite or batch task that runs to completion.

<!--more--> 

Creates one or more {{< glossary_tooltip term_id="pod" >}} objects and ensures that a specified number of them successfully terminate. As Pods successfully complete, the Job tracks the successful completions.

