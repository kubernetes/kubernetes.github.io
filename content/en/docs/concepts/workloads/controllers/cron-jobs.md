---
reviewers:
- erictune
- soltysh
- janetkuo
title: CronJob
content_type: concept
weight: 80
---

<!-- overview -->

{{< feature-state for_k8s_version="v1.21" state="stable" >}}

A _CronJob_ creates {{< glossary_tooltip term_id="job" text="Jobs" >}} on a repeating schedule.

One CronJob object is like one line of a _crontab_ (cron table) file. It runs a job periodically
on a given schedule, written in [Cron](https://en.wikipedia.org/wiki/Cron) format.

{{< caution >}}
All **CronJob** `schedule:` times are based on the timezone of the
{{< glossary_tooltip term_id="kube-controller-manager" text="kube-controller-manager" >}}.

If your control plane runs the kube-controller-manager in Pods or bare
containers, the timezone set for the kube-controller-manager container determines the timezone
that the cron job controller uses.
{{< /caution >}}

When creating the manifest for a CronJob resource, make sure the name you provide
is a valid [DNS subdomain name](/docs/concepts/overview/working-with-objects/names#dns-subdomain-names).
The name must be no longer than 52 characters. This is because the CronJob controller will automatically
append 11 characters to the job name provided and there is a constraint that the
maximum length of a Job name is no more than 63 characters.

<!-- body -->

## CronJob

CronJobs are meant for performing regular scheduled actions such as backups,
report generation, and so on. Each of those tasks should be configured to recur
indefinitely (for example: once a day / week / month); you can define the point
in time within that interval when the job should start.

### Example

This example CronJob manifest prints the current time and a hello message every minute:

{{< codenew file="application/job/cronjob.yaml" >}}

([Running Automated Tasks with a CronJob](/docs/tasks/job/automated-tasks-with-cron-jobs/)
takes you through this example in more detail).

### Cron schedule syntax

```
# ┌───────────── minute (0 - 59)
# │ ┌───────────── hour (0 - 23)
# │ │ ┌───────────── day of the month (1 - 31)
# │ │ │ ┌───────────── month (1 - 12)
# │ │ │ │ ┌───────────── day of the week (0 - 6) (Sunday to Saturday;
# │ │ │ │ │                                   7 is also Sunday on some systems)
# │ │ │ │ │
# │ │ │ │ │
# * * * * *
```


| Entry 										| Description																									| Equivalent to |
| ------------- 						| ------------- 																							|-------------  |
| @yearly (or @annually)		| Run once a year at midnight of 1 January										| 0 0 1 1 * 		|
| @monthly 									| Run once a month at midnight of the first day of the month	| 0 0 1 * * 		|
| @weekly 									| Run once a week at midnight on Sunday morning								| 0 0 * * 0 		|
| @daily (or @midnight)			| Run once a day at midnight																	| 0 0 * * * 		|
| @hourly 									| Run once an hour at the beginning of the hour								| 0 * * * * 		|



For example, the line below states that the task must be started every Friday at midnight, as well as on the 13th of each month at midnight:

`0 0 13 * 5`

To generate CronJob schedule expressions, you can also use web tools like [crontab.guru](https://crontab.guru/).

## CronJob limitations {#cron-job-limitations}

A cron job creates a job object _about_ once per execution time of its schedule. We say "about" because there
are certain circumstances where two jobs might be created, or no job might be created. We attempt to make these rare,
but do not completely prevent them. Therefore, jobs should be _idempotent_.

If `startingDeadlineSeconds` is set to a large value or left unset (the default)
and if `concurrencyPolicy` is set to `Allow`, the jobs will always run
at least once.

{{< caution >}}
If `startingDeadlineSeconds` is set to a value less than 10 seconds, the CronJob may not be scheduled. This is because the CronJob controller checks things every 10 seconds.
{{< /caution >}}


For every CronJob, the CronJob {{< glossary_tooltip term_id="controller" >}} checks how many schedules it missed in the duration from its last scheduled time until now. If there are more than 100 missed schedules, then it does not start the job and logs the error

````
Cannot determine if job needs to be started. Too many missed start time (> 100). Set or decrease .spec.startingDeadlineSeconds or check clock skew.
````

It is important to note that if the `startingDeadlineSeconds` field is set (not `nil`), the controller counts how many missed jobs occurred from the value of `startingDeadlineSeconds` until now rather than from the last scheduled time until now. For example, if `startingDeadlineSeconds` is `200`, the controller counts how many missed jobs occurred in the last 200 seconds.

A CronJob is counted as missed if it has failed to be created at its scheduled time. For example, If `concurrencyPolicy` is set to `Forbid` and a CronJob was attempted to be scheduled when there was a previous schedule still running, then it would count as missed.

For example, suppose a CronJob is set to schedule a new Job every one minute beginning at `08:30:00`, and its
`startingDeadlineSeconds` field is not set. If the CronJob controller happens to
be down from `08:29:00` to `10:21:00`, the job will not start as the number of missed jobs which missed their schedule is greater than 100.

To illustrate this concept further, suppose a CronJob is set to schedule a new Job every one minute beginning at `08:30:00`, and its
`startingDeadlineSeconds` is set to 200 seconds. If the CronJob controller happens to
be down for the same period as the previous example (`08:29:00` to `10:21:00`,) the Job will still start at 10:22:00. This happens as the controller now checks how many missed schedules happened in the last 200 seconds (ie, 3 missed schedules), rather than from the last scheduled time until now.

The CronJob is only responsible for creating Jobs that match its schedule, and
the Job in turn is responsible for the management of the Pods it represents.

## Controller version {#new-controller}

Starting with Kubernetes v1.21 the second version of the CronJob controller
is the default implementation. To disable the default CronJob controller
and use the original CronJob controller instead, one pass the `CronJobControllerV2`
[feature gate](/docs/reference/command-line-tools-reference/feature-gates/)
flag to the {{< glossary_tooltip term_id="kube-controller-manager" text="kube-controller-manager" >}},
and set this flag to `false`. For example:

```
--feature-gates="CronJobControllerV2=false"
```


## {{% heading "whatsnext" %}}

[Cron expression format](https://en.wikipedia.org/wiki/Cron)
documents the format of CronJob `schedule` fields.

For instructions on creating and working with cron jobs, and for an example of CronJob
manifest, see [Running automated tasks with cron jobs](/docs/tasks/job/automated-tasks-with-cron-jobs).

