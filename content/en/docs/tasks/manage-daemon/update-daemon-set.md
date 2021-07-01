---
reviewers:
- janetkuo
title: Perform a Rolling Update on a DaemonSet
content_type: task
weight: 10
---

<!-- overview -->
This page shows how to perform a rolling update on a DaemonSet.

## {{% heading "prerequisites" %}}

<!-- steps -->

## DaemonSet Update Strategy

DaemonSet has two update strategy types:

* `OnDelete`: With `OnDelete` update strategy, after you update a DaemonSet template, new
  DaemonSet pods will *only* be created when you manually delete old DaemonSet
  pods. This is the same behavior of DaemonSet in Kubernetes version 1.5 or
  before.
* `RollingUpdate`: This is the default update strategy.  
  With `RollingUpdate` update strategy, after you update a
  DaemonSet template, old DaemonSet pods will be killed, and new DaemonSet pods
  will be created automatically, in a controlled fashion. At most one pod of
  the DaemonSet will be running on each node during the whole update process.

## Performing a Rolling Update

To enable the rolling update feature of a DaemonSet, you must set its
`.spec.updateStrategy.type` to `RollingUpdate`.

You may want to set
[`.spec.updateStrategy.rollingUpdate.maxUnavailable`](/docs/concepts/workloads/controllers/deployment/#max-unavailable)
(default to 1) and
[`.spec.minReadySeconds`](/docs/concepts/workloads/controllers/deployment/#min-ready-seconds)
(default to 0) as well.

### Creating a DaemonSet with `RollingUpdate` update strategy

This YAML file specifies a DaemonSet with an update strategy as 'RollingUpdate'

{{< codenew file="controllers/fluentd-daemonset.yaml" >}}

After verifying the update strategy of the DaemonSet manifest, create the DaemonSet:

```shell
kubectl create -f https://k8s.io/examples/controllers/fluentd-daemonset.yaml
```

Alternatively, use `kubectl apply` to create the same DaemonSet if you plan to
update the DaemonSet with `kubectl apply`.

```shell
kubectl apply -f https://k8s.io/examples/controllers/fluentd-daemonset.yaml
```

### Checking DaemonSet `RollingUpdate` update strategy

Check the update strategy of your DaemonSet, and make sure it's set to
`RollingUpdate`:

```shell
kubectl get ds/fluentd-elasticsearch -o go-template='{{.spec.updateStrategy.type}}{{"\n"}}' -n kube-system
```

If you haven't created the DaemonSet in the system, check your DaemonSet
manifest with the following command instead:

```shell
kubectl apply -f https://k8s.io/examples/controllers/fluentd-daemonset.yaml --dry-run=client -o go-template='{{.spec.updateStrategy.type}}{{"\n"}}'
```

The output from both commands should be:

```shell
RollingUpdate
```

If the output isn't `RollingUpdate`, go back and modify the DaemonSet object or
manifest accordingly.


### Updating a DaemonSet template

Any updates to a `RollingUpdate` DaemonSet `.spec.template` will trigger a rolling
update. Let's update the DaemonSet by applying a new YAML file. This can be done with several different `kubectl` commands.

{{< codenew file="controllers/fluentd-daemonset-update.yaml" >}}

#### Declarative commands

If you update DaemonSets using
[configuration files](/docs/tasks/manage-kubernetes-objects/declarative-config/),
use `kubectl apply`:

```shell
kubectl apply -f https://k8s.io/examples/controllers/fluentd-daemonset-update.yaml
```

#### Imperative commands

If you update DaemonSets using
[imperative commands](/docs/tasks/manage-kubernetes-objects/imperative-command/),
use `kubectl edit` :

```shell
kubectl edit ds/fluentd-elasticsearch -n kube-system
```

##### Updating only the container image

If you only need to update the container image in the DaemonSet template, i.e.
`.spec.template.spec.containers[*].image`, use `kubectl set image`:

```shell
kubectl set image ds/fluentd-elasticsearch fluentd-elasticsearch=quay.io/fluentd_elasticsearch/fluentd:v2.6.0 -n kube-system
```

### Watching the rolling update status

Finally, watch the rollout status of the latest DaemonSet rolling update:

```shell
kubectl rollout status ds/fluentd-elasticsearch -n kube-system
```

When the rollout is complete, the output is similar to this:

```shell
daemonset "fluentd-elasticsearch" successfully rolled out
```

## Troubleshooting

### DaemonSet rolling update is stuck

Sometimes, a DaemonSet rolling update may be stuck. Here are some possible
causes:

#### Some nodes run out of resources

The rollout is stuck because new DaemonSet pods can't be scheduled on at least one
node. This is possible when the node is
[running out of resources](/docs/concepts/scheduling-eviction/node-pressure-eviction/).

When this happens, find the nodes that don't have the DaemonSet pods scheduled on
by comparing the output of `kubectl get nodes` and the output of:

```shell
kubectl get pods -l name=fluentd-elasticsearch -o wide -n kube-system
```

Once you've found those nodes, delete some non-DaemonSet pods from the node to
make room for new DaemonSet pods.

{{< note >}}
This will cause service disruption when deleted pods are not controlled by any controllers or pods are not
replicated. This does not respect [PodDisruptionBudget](/docs/tasks/run-application/configure-pdb/)
either.
{{< /note >}}

#### Broken rollout

If the recent DaemonSet template update is broken, for example, the container is
crash looping, or the container image doesn't exist (often due to a typo),
DaemonSet rollout won't progress.

To fix this, update the DaemonSet template again. New rollout won't be
blocked by previous unhealthy rollouts.

#### Clock skew

If `.spec.minReadySeconds` is specified in the DaemonSet, clock skew between
master and nodes will make DaemonSet unable to detect the right rollout
progress.

## Clean up

Delete DaemonSet from a namespace :

```shell
kubectl delete ds fluentd-elasticsearch -n kube-system
```

## {{% heading "whatsnext" %}}

* See [Performing a rollback on a DaemonSet](/docs/tasks/manage-daemon/rollback-daemon-set/)
* See [Creating a DaemonSet to adopt existing DaemonSet pods](/docs/concepts/workloads/controllers/daemonset/)

