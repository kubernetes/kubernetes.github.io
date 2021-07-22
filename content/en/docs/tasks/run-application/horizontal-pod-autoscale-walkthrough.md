---
reviewers:
- fgrzadkowski
- jszczepkowski
- justinsb
- directxman12
title: Horizontal Pod Autoscaler Walkthrough
content_type: task
weight: 100
---

<!-- overview -->

Horizontal Pod Autoscaler automatically scales the number of Pods
in a replication controller, deployment, replica set or stateful set based on observed CPU utilization
(or, with beta support, on some other, application-provided metrics).

This document walks you through an example of enabling Horizontal Pod Autoscaler for the php-apache server.
For more information on how Horizontal Pod Autoscaler behaves, see the
[Horizontal Pod Autoscaler user guide](/docs/tasks/run-application/horizontal-pod-autoscale/).

## {{% heading "prerequisites" %}}

This example requires a running Kubernetes cluster and kubectl, version 1.2 or later.
[Metrics server](https://github.com/kubernetes-sigs/metrics-server) monitoring needs to be deployed
in the cluster to provide metrics through the [Metrics API](https://github.com/kubernetes/metrics).
Horizontal Pod Autoscaler uses this API to collect metrics. To learn how to deploy the metrics-server,
see the [metrics-server documentation](https://github.com/kubernetes-sigs/metrics-server#deployment).

To specify multiple resource metrics for a Horizontal Pod Autoscaler, you must have a
Kubernetes cluster and kubectl at version 1.6 or later. To make use of custom metrics, your cluster
must be able to communicate with the API server providing the custom Metrics API.
Finally, to use metrics not related to any Kubernetes object you must have a
Kubernetes cluster at version 1.10 or later, and you must be able to communicate
with the API server that provides the external Metrics API.
See the [Horizontal Pod Autoscaler user guide](/docs/tasks/run-application/horizontal-pod-autoscale/#support-for-custom-metrics) for more details.

<!-- steps -->

## Run and expose php-apache server

To demonstrate Horizontal Pod Autoscaler we will use a custom docker image based on the php-apache image. The Dockerfile has the following content:

```dockerfile
FROM php:5-apache
COPY index.php /var/www/html/index.php
RUN chmod a+rx index.php
```

It defines an index.php page which performs some CPU intensive computations:

```php
<?php
  $x = 0.0001;
  for ($i = 0; $i <= 1000000; $i++) {
    $x += sqrt($x);
  }
  echo "OK!";
?>
```

First, we will start a deployment running the image and expose it as a service
using the following configuration:

{{< codenew file="application/php-apache.yaml" >}}

Run the following command:

```shell
kubectl apply -f https://k8s.io/examples/application/php-apache.yaml
```

```
deployment.apps/php-apache created
service/php-apache created
```

## Create Horizontal Pod Autoscaler

Now that the server is running, we will create the autoscaler using
[kubectl autoscale](/docs/reference/generated/kubectl/kubectl-commands#autoscale).
The following command will create a Horizontal Pod Autoscaler that maintains between 1 and 10 replicas of the Pods
controlled by the php-apache deployment we created in the first step of these instructions.
Roughly speaking, HPA will increase and decrease the number of replicas
(via the deployment) to maintain an average CPU utilization across all Pods of 50%
(since each pod requests 200 milli-cores by `kubectl run`), this means average CPU usage of 100 milli-cores).
See [here](/docs/tasks/run-application/horizontal-pod-autoscale/#algorithm-details) for more details on the algorithm.

```shell
kubectl autoscale deployment php-apache --cpu-percent=50 --min=1 --max=10
```

```
horizontalpodautoscaler.autoscaling/php-apache autoscaled
```

We may check the current status of autoscaler by running:

```shell
kubectl get hpa
```

```
NAME         REFERENCE                     TARGET    MINPODS   MAXPODS   REPLICAS   AGE
php-apache   Deployment/php-apache/scale   0% / 50%  1         10        1          18s
```

Please note that the current CPU consumption is 0% as we are not sending any requests to the server
(the ``TARGET`` column shows the average across all the pods controlled by the corresponding deployment).

## Increase load

Now, we will see how the autoscaler reacts to increased load.
We will start a container, and send an infinite loop of queries to the php-apache service (please run it in a different terminal):

```shell
kubectl run -i --tty load-generator --rm --image=busybox --restart=Never -- /bin/sh -c "while sleep 0.01; do wget -q -O- http://php-apache; done"
```

Within a minute or so, we should see the higher CPU load by executing:

```shell
kubectl get hpa
```

```
NAME         REFERENCE                     TARGET      MINPODS   MAXPODS   REPLICAS   AGE
php-apache   Deployment/php-apache/scale   305% / 50%  1         10        1          3m
```

Here, CPU consumption has increased to 305% of the request.
As a result, the deployment was resized to 7 replicas:

```shell
kubectl get deployment php-apache
```

```
NAME         READY   UP-TO-DATE   AVAILABLE   AGE
php-apache   7/7      7           7           19m
```

{{< note >}}
It may take a few minutes to stabilize the number of replicas. Since the amount
of load is not controlled in any way it may happen that the final number of replicas
will differ from this example.
{{< /note >}}

## Stop load

We will finish our example by stopping the user load.

In the terminal where we created the container with `busybox` image, terminate
the load generation by typing `<Ctrl> + C`.

Then we will verify the result state (after a minute or so):

```shell
kubectl get hpa
```

```
NAME         REFERENCE                     TARGET       MINPODS   MAXPODS   REPLICAS   AGE
php-apache   Deployment/php-apache/scale   0% / 50%     1         10        1          11m
```

```shell
kubectl get deployment php-apache
```

```
NAME         READY   UP-TO-DATE   AVAILABLE   AGE
php-apache   1/1     1            1           27m
```

Here CPU utilization dropped to 0, and so HPA autoscaled the number of replicas back down to 1.

{{< note >}}
Autoscaling the replicas may take a few minutes.
{{< /note >}}

<!-- discussion -->

## Autoscaling on multiple metrics and custom metrics

You can introduce additional metrics to use when autoscaling the `php-apache` Deployment
by making use of the `autoscaling/v2beta2` API version.

First, get the YAML of your HorizontalPodAutoscaler in the `autoscaling/v2beta2` form:

```shell
kubectl get hpa php-apache -o yaml > /tmp/hpa-v2.yaml
```

Open the `/tmp/hpa-v2.yaml` file in an editor, and you should see YAML which looks like this:

```yaml
apiVersion: autoscaling/v2beta2
kind: HorizontalPodAutoscaler
metadata:
  name: php-apache
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: php-apache
  minReplicas: 1
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 50
status:
  observedGeneration: 1
  lastScaleTime: <some-time>
  currentReplicas: 1
  desiredReplicas: 1
  currentMetrics:
  - type: Resource
    resource:
      name: cpu
      current:
        averageUtilization: 0
        averageValue: 0
```

Notice that the `targetCPUUtilizationPercentage` field has been replaced with an array called `metrics`.
The CPU utilization metric is a *resource metric*, since it is represented as a percentage of a resource
specified on pod containers.  Notice that you can specify other resource metrics besides CPU.  By default,
the only other supported resource metric is memory.  These resources do not change names from cluster
to cluster, and should always be available, as long as the `metrics.k8s.io` API is available.

You can also specify resource metrics in terms of direct values, instead of as percentages of the
requested value, by using a `target.type` of `AverageValue` instead of `Utilization`, and
setting the corresponding `target.averageValue` field instead of the `target.averageUtilization`.

There are two other types of metrics, both of which are considered *custom metrics*: pod metrics and
object metrics.  These metrics may have names which are cluster specific, and require a more
advanced cluster monitoring setup.

The first of these alternative metric types is *pod metrics*.  These metrics describe Pods, and
are averaged together across Pods and compared with a target value to determine the replica count.
They work much like resource metrics, except that they *only* support a `target` type of `AverageValue`.

Pod metrics are specified using a metric block like this:

```yaml
type: Pods
pods:
  metric:
    name: packets-per-second
  target:
    type: AverageValue
    averageValue: 1k
```

The second alternative metric type is *object metrics*. These metrics describe a different
object in the same namespace, instead of describing Pods. The metrics are not necessarily
fetched from the object; they only describe it. Object metrics support `target` types of
both `Value` and `AverageValue`.  With `Value`, the target is compared directly to the returned
metric from the API. With `AverageValue`, the value returned from the custom metrics API is divided
by the number of Pods before being compared to the target. The following example is the YAML
representation of the `requests-per-second` metric.

```yaml
type: Object
object:
  metric:
    name: requests-per-second
  describedObject:
    apiVersion: networking.k8s.io/v1beta1
    kind: Ingress
    name: main-route
  target:
    type: Value
    value: 2k
```

If you provide multiple such metric blocks, the HorizontalPodAutoscaler will consider each metric in turn.
The HorizontalPodAutoscaler will calculate proposed replica counts for each metric, and then choose the
one with the highest replica count.

For example, if you had your monitoring system collecting metrics about network traffic,
you could update the definition above using `kubectl edit` to look like this:

```yaml
apiVersion: autoscaling/v2beta2
kind: HorizontalPodAutoscaler
metadata:
  name: php-apache
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: php-apache
  minReplicas: 1
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 50
  - type: Pods
    pods:
      metric:
        name: packets-per-second
      target:
        type: AverageValue
        averageValue: 1k
  - type: Object
    object:
      metric:
        name: requests-per-second
      describedObject:
        apiVersion: networking.k8s.io/v1beta1
        kind: Ingress
        name: main-route
      target:
        type: Value
        value: 10k
status:
  observedGeneration: 1
  lastScaleTime: <some-time>
  currentReplicas: 1
  desiredReplicas: 1
  currentMetrics:
  - type: Resource
    resource:
      name: cpu
    current:
      averageUtilization: 0
      averageValue: 0
  - type: Object
    object:
      metric:
        name: requests-per-second
      describedObject:
        apiVersion: networking.k8s.io/v1beta1
        kind: Ingress
        name: main-route
      current:
        value: 10k
```

Then, your HorizontalPodAutoscaler would attempt to ensure that each pod was consuming roughly
50% of its requested CPU, serving 1000 packets per second, and that all pods behind the main-route
Ingress were serving a total of 10000 requests per second.

### Autoscaling on more specific metrics

Many metrics pipelines allow you to describe metrics either by name or by a set of additional
descriptors called _labels_. For all non-resource metric types (pod, object, and external,
described below), you can specify an additional label selector which is passed to your metric
pipeline. For instance, if you collect a metric `http_requests` with the `verb`
label, you can specify the following metric block to scale only on GET requests:

```yaml
type: Object
object:
  metric:
    name: http_requests
    selector: {matchLabels: {verb: GET}}
```

This selector uses the same syntax as the full Kubernetes label selectors. The monitoring pipeline
determines how to collapse multiple series into a single value, if the name and selector
match multiple series. The selector is additive, and cannot select metrics
that describe objects that are **not** the target object (the target pods in the case of the `Pods`
type, and the described object in the case of the `Object` type).

### Autoscaling on metrics not related to Kubernetes objects

Applications running on Kubernetes may need to autoscale based on metrics that don't have an obvious
relationship to any object in the Kubernetes cluster, such as metrics describing a hosted service with
no direct correlation to Kubernetes namespaces. In Kubernetes 1.10 and later, you can address this use case
with *external metrics*.

Using external metrics requires knowledge of your monitoring system; the setup is
similar to that required when using custom metrics. External metrics allow you to autoscale your cluster
based on any metric available in your monitoring system. Provide a `metric` block with a
`name` and `selector`, as above, and use the `External` metric type instead of `Object`.
If multiple time series are matched by the `metricSelector`,
the sum of their values is used by the HorizontalPodAutoscaler.
External metrics support both the `Value` and `AverageValue` target types, which function exactly the same
as when you use the `Object` type.

For example if your application processes tasks from a hosted queue service, you could add the following
section to your HorizontalPodAutoscaler manifest to specify that you need one worker per 30 outstanding tasks.

```yaml
- type: External
  external:
    metric:
      name: queue_messages_ready
      selector: "queue=worker_tasks"
    target:
      type: AverageValue
      averageValue: 30
```

When possible, it's preferable to use the custom metric target types instead of external metrics, since it's
easier for cluster administrators to secure the custom metrics API.  The external metrics API potentially allows
access to any metric, so cluster administrators should take care when exposing it.

## Appendix: Horizontal Pod Autoscaler Status Conditions

When using the `autoscaling/v2beta2` form of the HorizontalPodAutoscaler, you will be able to see
*status conditions* set by Kubernetes on the HorizontalPodAutoscaler.  These status conditions indicate
whether or not the HorizontalPodAutoscaler is able to scale, and whether or not it is currently restricted
in any way.

The conditions appear in the `status.conditions` field.  To see the conditions affecting a HorizontalPodAutoscaler,
we can use `kubectl describe hpa`:

```shell
kubectl describe hpa cm-test
```

```
Name:                           cm-test
Namespace:                      prom
Labels:                         <none>
Annotations:                    <none>
CreationTimestamp:              Fri, 16 Jun 2017 18:09:22 +0000
Reference:                      ReplicationController/cm-test
Metrics:                        ( current / target )
  "http_requests" on pods:      66m / 500m
Min replicas:                   1
Max replicas:                   4
ReplicationController pods:     1 current / 1 desired
Conditions:
  Type                  Status  Reason                  Message
  ----                  ------  ------                  -------
  AbleToScale           True    ReadyForNewScale        the last scale time was sufficiently old as to warrant a new scale
  ScalingActive         True    ValidMetricFound        the HPA was able to successfully calculate a replica count from pods metric http_requests
  ScalingLimited        False   DesiredWithinRange      the desired replica count is within the acceptable range
Events:
```

For this HorizontalPodAutoscaler, we can see several conditions in a healthy state.  The first,
`AbleToScale`, indicates whether or not the HPA is able to fetch and update scales, as well as
whether or not any backoff-related conditions would prevent scaling.  The second, `ScalingActive`,
indicates whether or not the HPA is enabled (i.e. the replica count of the target is not zero) and
is able to calculate desired scales. When it is `False`, it generally indicates problems with
fetching metrics.  Finally, the last condition, `ScalingLimited`, indicates that the desired scale
was capped by the maximum or minimum of the HorizontalPodAutoscaler.  This is an indication that
you may wish to raise or lower the minimum or maximum replica count constraints on your
HorizontalPodAutoscaler.

## Appendix: Quantities

All metrics in the HorizontalPodAutoscaler and metrics APIs are specified using
a special whole-number notation known in Kubernetes as a
{{< glossary_tooltip term_id="quantity" text="quantity">}}.  For example,
the quantity `10500m` would be written as `10.5` in decimal notation.  The metrics APIs
will return whole numbers without a suffix when possible, and will generally return
quantities in milli-units otherwise.  This means you might see your metric value fluctuate
between `1` and `1500m`, or `1` and `1.5` when written in decimal notation.

## Appendix: Other possible scenarios

### Creating the autoscaler declaratively

Instead of using `kubectl autoscale` command to create a HorizontalPodAutoscaler imperatively we
can use the following file to create it declaratively:

{{< codenew file="application/hpa/php-apache.yaml" >}}

We will create the autoscaler by executing the following command:

```shell
kubectl create -f https://k8s.io/examples/application/hpa/php-apache.yaml
```

```
horizontalpodautoscaler.autoscaling/php-apache created
```
