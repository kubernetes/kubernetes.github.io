---
api_metadata:
  apiVersion: "autoscaling/v2beta2"
  import: "k8s.io/api/autoscaling/v2beta2"
  kind: "HorizontalPodAutoscaler"
content_type: "api_reference"
description: "HorizontalPodAutoscaler is the configuration for a horizontal pod autoscaler, which automatically manages the replica count of any resource implementing the scale subresource based on the metrics specified."
title: "HorizontalPodAutoscaler v2beta2"
weight: 12
auto_generated: true
---

<!--
The file is auto-generated from the Go source code of the component using a generic
[generator](https://github.com/kubernetes-sigs/reference-docs/). To learn how
to generate the reference documentation, please read
[Contributing to the reference documentation](/docs/contribute/generate-ref-docs/).
To update the reference content, please follow the 
[Contributing upstream](/docs/contribute/generate-ref-docs/contribute-upstream/)
guide. You can file document formatting bugs against the
[reference-docs](https://github.com/kubernetes-sigs/reference-docs/) project.
-->

`apiVersion: autoscaling/v2beta2`

`import "k8s.io/api/autoscaling/v2beta2"`


## HorizontalPodAutoscaler {#HorizontalPodAutoscaler}

HorizontalPodAutoscaler is the configuration for a horizontal pod autoscaler, which automatically manages the replica count of any resource implementing the scale subresource based on the metrics specified.

<hr>

- **apiVersion**: autoscaling/v2beta2


- **kind**: HorizontalPodAutoscaler


- **metadata** (<a href="{{< ref "../common-definitions/object-meta#ObjectMeta" >}}">ObjectMeta</a>)

  metadata is the standard object metadata. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

- **spec** (<a href="{{< ref "../workload-resources/horizontal-pod-autoscaler-v2beta2#HorizontalPodAutoscalerSpec" >}}">HorizontalPodAutoscalerSpec</a>)

  spec is the specification for the behaviour of the autoscaler. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status.

- **status** (<a href="{{< ref "../workload-resources/horizontal-pod-autoscaler-v2beta2#HorizontalPodAutoscalerStatus" >}}">HorizontalPodAutoscalerStatus</a>)

  status is the current information about the autoscaler.





## HorizontalPodAutoscalerSpec {#HorizontalPodAutoscalerSpec}

HorizontalPodAutoscalerSpec describes the desired functionality of the HorizontalPodAutoscaler.

<hr>

- **maxReplicas** (int32), required

  maxReplicas is the upper limit for the number of replicas to which the autoscaler can scale up. It cannot be less that minReplicas.

- **scaleTargetRef** (CrossVersionObjectReference), required

  scaleTargetRef points to the target resource to scale, and is used to the pods for which metrics should be collected, as well as to actually change the replica count.

  <a name="CrossVersionObjectReference"></a>
  *CrossVersionObjectReference contains enough information to let you identify the referred resource.*

  - **scaleTargetRef.kind** (string), required

    Kind of the referent; More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds"

  - **scaleTargetRef.name** (string), required

    Name of the referent; More info: http://kubernetes.io/docs/user-guide/identifiers#names

  - **scaleTargetRef.apiVersion** (string)

    API version of the referent

- **minReplicas** (int32)

  minReplicas is the lower limit for the number of replicas to which the autoscaler can scale down.  It defaults to 1 pod.  minReplicas is allowed to be 0 if the alpha feature gate HPAScaleToZero is enabled and at least one Object or External metric is configured.  Scaling is active as long as at least one metric value is available.

- **behavior** (HorizontalPodAutoscalerBehavior)

  behavior configures the scaling behavior of the target in both Up and Down directions (scaleUp and scaleDown fields respectively). If not set, the default HPAScalingRules for scale up and scale down are used.

  <a name="HorizontalPodAutoscalerBehavior"></a>
  *HorizontalPodAutoscalerBehavior configures the scaling behavior of the target in both Up and Down directions (scaleUp and scaleDown fields respectively).*

  - **behavior.scaleDown** (HPAScalingRules)

    scaleDown is scaling policy for scaling Down. If not set, the default value is to allow to scale down to minReplicas pods, with a 300 second stabilization window (i.e., the highest recommendation for the last 300sec is used).

    <a name="HPAScalingRules"></a>
    *HPAScalingRules configures the scaling behavior for one direction. These Rules are applied after calculating DesiredReplicas from metrics for the HPA. They can limit the scaling velocity by specifying scaling policies. They can prevent flapping by specifying the stabilization window, so that the number of replicas is not set instantly, instead, the safest value from the stabilization window is chosen.*

    - **behavior.scaleDown.policies** ([]HPAScalingPolicy)

      policies is a list of potential scaling polices which can be used during scaling. At least one policy must be specified, otherwise the HPAScalingRules will be discarded as invalid

      <a name="HPAScalingPolicy"></a>
      *HPAScalingPolicy is a single policy which must hold true for a specified past interval.*

      - **behavior.scaleDown.policies.type** (string), required

        Type is used to specify the scaling policy.

      - **behavior.scaleDown.policies.value** (int32), required

        Value contains the amount of change which is permitted by the policy. It must be greater than zero

      - **behavior.scaleDown.policies.periodSeconds** (int32), required

        PeriodSeconds specifies the window of time for which the policy should hold true. PeriodSeconds must be greater than zero and less than or equal to 1800 (30 min).

    - **behavior.scaleDown.selectPolicy** (string)

      selectPolicy is used to specify which policy should be used. If not set, the default value MaxPolicySelect is used.

    - **behavior.scaleDown.stabilizationWindowSeconds** (int32)

      StabilizationWindowSeconds is the number of seconds for which past recommendations should be considered while scaling up or scaling down. StabilizationWindowSeconds must be greater than or equal to zero and less than or equal to 3600 (one hour). If not set, use the default values: - For scale up: 0 (i.e. no stabilization is done). - For scale down: 300 (i.e. the stabilization window is 300 seconds long).

  - **behavior.scaleUp** (HPAScalingRules)

    scaleUp is scaling policy for scaling Up. If not set, the default value is the higher of:
      * increase no more than 4 pods per 60 seconds
      * double the number of pods per 60 seconds
    No stabilization is used.

    <a name="HPAScalingRules"></a>
    *HPAScalingRules configures the scaling behavior for one direction. These Rules are applied after calculating DesiredReplicas from metrics for the HPA. They can limit the scaling velocity by specifying scaling policies. They can prevent flapping by specifying the stabilization window, so that the number of replicas is not set instantly, instead, the safest value from the stabilization window is chosen.*

    - **behavior.scaleUp.policies** ([]HPAScalingPolicy)

      policies is a list of potential scaling polices which can be used during scaling. At least one policy must be specified, otherwise the HPAScalingRules will be discarded as invalid

      <a name="HPAScalingPolicy"></a>
      *HPAScalingPolicy is a single policy which must hold true for a specified past interval.*

      - **behavior.scaleUp.policies.type** (string), required

        Type is used to specify the scaling policy.

      - **behavior.scaleUp.policies.value** (int32), required

        Value contains the amount of change which is permitted by the policy. It must be greater than zero

      - **behavior.scaleUp.policies.periodSeconds** (int32), required

        PeriodSeconds specifies the window of time for which the policy should hold true. PeriodSeconds must be greater than zero and less than or equal to 1800 (30 min).

    - **behavior.scaleUp.selectPolicy** (string)

      selectPolicy is used to specify which policy should be used. If not set, the default value MaxPolicySelect is used.

    - **behavior.scaleUp.stabilizationWindowSeconds** (int32)

      StabilizationWindowSeconds is the number of seconds for which past recommendations should be considered while scaling up or scaling down. StabilizationWindowSeconds must be greater than or equal to zero and less than or equal to 3600 (one hour). If not set, use the default values: - For scale up: 0 (i.e. no stabilization is done). - For scale down: 300 (i.e. the stabilization window is 300 seconds long).

- **metrics** ([]MetricSpec)

  metrics contains the specifications for which to use to calculate the desired replica count (the maximum replica count across all metrics will be used).  The desired replica count is calculated multiplying the ratio between the target value and the current value by the current number of pods.  Ergo, metrics used must decrease as the pod count is increased, and vice-versa.  See the individual metric source types for more information about how each type of metric must respond. If not set, the default metric will be set to 80% average CPU utilization.

  <a name="MetricSpec"></a>
  *MetricSpec specifies how to scale based on a single metric (only `type` and one other matching field should be set at once).*

  - **metrics.type** (string), required

    type is the type of metric source.  It should be one of "ContainerResource", "External", "Object", "Pods" or "Resource", each mapping to a matching field in the object. Note: "ContainerResource" type is available on when the feature-gate HPAContainerMetrics is enabled

  - **metrics.containerResource** (ContainerResourceMetricSource)

    container resource refers to a resource metric (such as those specified in requests and limits) known to Kubernetes describing a single container in each pod of the current scale target (e.g. CPU or memory). Such metrics are built in to Kubernetes, and have special scaling options on top of those available to normal per-pod metrics using the "pods" source. This is an alpha feature and can be enabled by the HPAContainerMetrics feature flag.

    <a name="ContainerResourceMetricSource"></a>
    *ContainerResourceMetricSource indicates how to scale on a resource metric known to Kubernetes, as specified in requests and limits, describing each pod in the current scale target (e.g. CPU or memory).  The values will be averaged together before being compared to the target.  Such metrics are built in to Kubernetes, and have special scaling options on top of those available to normal per-pod metrics using the "pods" source.  Only one "target" type should be set.*

    - **metrics.containerResource.container** (string), required

      container is the name of the container in the pods of the scaling target

    - **metrics.containerResource.name** (string), required

      name is the name of the resource in question.

    - **metrics.containerResource.target** (MetricTarget), required

      target specifies the target value for the given metric

      <a name="MetricTarget"></a>
      *MetricTarget defines the target value, average value, or average utilization of a specific metric*

      - **metrics.containerResource.target.type** (string), required

        type represents whether the metric type is Utilization, Value, or AverageValue

      - **metrics.containerResource.target.averageUtilization** (int32)

        averageUtilization is the target value of the average of the resource metric across all relevant pods, represented as a percentage of the requested value of the resource for the pods. Currently only valid for Resource metric source type

      - **metrics.containerResource.target.averageValue** (<a href="{{< ref "../common-definitions/quantity#Quantity" >}}">Quantity</a>)

        averageValue is the target value of the average of the metric across all relevant pods (as a quantity)

      - **metrics.containerResource.target.value** (<a href="{{< ref "../common-definitions/quantity#Quantity" >}}">Quantity</a>)

        value is the target value of the metric (as a quantity).

  - **metrics.external** (ExternalMetricSource)

    external refers to a global metric that is not associated with any Kubernetes object. It allows autoscaling based on information coming from components running outside of cluster (for example length of queue in cloud messaging service, or QPS from loadbalancer running outside of cluster).

    <a name="ExternalMetricSource"></a>
    *ExternalMetricSource indicates how to scale on a metric not associated with any Kubernetes object (for example length of queue in cloud messaging service, or QPS from loadbalancer running outside of cluster).*

    - **metrics.external.metric** (MetricIdentifier), required

      metric identifies the target metric by name and selector

      <a name="MetricIdentifier"></a>
      *MetricIdentifier defines the name and optionally selector for a metric*

      - **metrics.external.metric.name** (string), required

        name is the name of the given metric

      - **metrics.external.metric.selector** (<a href="{{< ref "../common-definitions/label-selector#LabelSelector" >}}">LabelSelector</a>)

        selector is the string-encoded form of a standard kubernetes label selector for the given metric When set, it is passed as an additional parameter to the metrics server for more specific metrics scoping. When unset, just the metricName will be used to gather metrics.

    - **metrics.external.target** (MetricTarget), required

      target specifies the target value for the given metric

      <a name="MetricTarget"></a>
      *MetricTarget defines the target value, average value, or average utilization of a specific metric*

      - **metrics.external.target.type** (string), required

        type represents whether the metric type is Utilization, Value, or AverageValue

      - **metrics.external.target.averageUtilization** (int32)

        averageUtilization is the target value of the average of the resource metric across all relevant pods, represented as a percentage of the requested value of the resource for the pods. Currently only valid for Resource metric source type

      - **metrics.external.target.averageValue** (<a href="{{< ref "../common-definitions/quantity#Quantity" >}}">Quantity</a>)

        averageValue is the target value of the average of the metric across all relevant pods (as a quantity)

      - **metrics.external.target.value** (<a href="{{< ref "../common-definitions/quantity#Quantity" >}}">Quantity</a>)

        value is the target value of the metric (as a quantity).

  - **metrics.object** (ObjectMetricSource)

    object refers to a metric describing a single kubernetes object (for example, hits-per-second on an Ingress object).

    <a name="ObjectMetricSource"></a>
    *ObjectMetricSource indicates how to scale on a metric describing a kubernetes object (for example, hits-per-second on an Ingress object).*

    - **metrics.object.describedObject** (CrossVersionObjectReference), required


      <a name="CrossVersionObjectReference"></a>
      *CrossVersionObjectReference contains enough information to let you identify the referred resource.*

      - **metrics.object.describedObject.kind** (string), required

        Kind of the referent; More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds"

      - **metrics.object.describedObject.name** (string), required

        Name of the referent; More info: http://kubernetes.io/docs/user-guide/identifiers#names

      - **metrics.object.describedObject.apiVersion** (string)

        API version of the referent

    - **metrics.object.metric** (MetricIdentifier), required

      metric identifies the target metric by name and selector

      <a name="MetricIdentifier"></a>
      *MetricIdentifier defines the name and optionally selector for a metric*

      - **metrics.object.metric.name** (string), required

        name is the name of the given metric

      - **metrics.object.metric.selector** (<a href="{{< ref "../common-definitions/label-selector#LabelSelector" >}}">LabelSelector</a>)

        selector is the string-encoded form of a standard kubernetes label selector for the given metric When set, it is passed as an additional parameter to the metrics server for more specific metrics scoping. When unset, just the metricName will be used to gather metrics.

    - **metrics.object.target** (MetricTarget), required

      target specifies the target value for the given metric

      <a name="MetricTarget"></a>
      *MetricTarget defines the target value, average value, or average utilization of a specific metric*

      - **metrics.object.target.type** (string), required

        type represents whether the metric type is Utilization, Value, or AverageValue

      - **metrics.object.target.averageUtilization** (int32)

        averageUtilization is the target value of the average of the resource metric across all relevant pods, represented as a percentage of the requested value of the resource for the pods. Currently only valid for Resource metric source type

      - **metrics.object.target.averageValue** (<a href="{{< ref "../common-definitions/quantity#Quantity" >}}">Quantity</a>)

        averageValue is the target value of the average of the metric across all relevant pods (as a quantity)

      - **metrics.object.target.value** (<a href="{{< ref "../common-definitions/quantity#Quantity" >}}">Quantity</a>)

        value is the target value of the metric (as a quantity).

  - **metrics.pods** (PodsMetricSource)

    pods refers to a metric describing each pod in the current scale target (for example, transactions-processed-per-second).  The values will be averaged together before being compared to the target value.

    <a name="PodsMetricSource"></a>
    *PodsMetricSource indicates how to scale on a metric describing each pod in the current scale target (for example, transactions-processed-per-second). The values will be averaged together before being compared to the target value.*

    - **metrics.pods.metric** (MetricIdentifier), required

      metric identifies the target metric by name and selector

      <a name="MetricIdentifier"></a>
      *MetricIdentifier defines the name and optionally selector for a metric*

      - **metrics.pods.metric.name** (string), required

        name is the name of the given metric

      - **metrics.pods.metric.selector** (<a href="{{< ref "../common-definitions/label-selector#LabelSelector" >}}">LabelSelector</a>)

        selector is the string-encoded form of a standard kubernetes label selector for the given metric When set, it is passed as an additional parameter to the metrics server for more specific metrics scoping. When unset, just the metricName will be used to gather metrics.

    - **metrics.pods.target** (MetricTarget), required

      target specifies the target value for the given metric

      <a name="MetricTarget"></a>
      *MetricTarget defines the target value, average value, or average utilization of a specific metric*

      - **metrics.pods.target.type** (string), required

        type represents whether the metric type is Utilization, Value, or AverageValue

      - **metrics.pods.target.averageUtilization** (int32)

        averageUtilization is the target value of the average of the resource metric across all relevant pods, represented as a percentage of the requested value of the resource for the pods. Currently only valid for Resource metric source type

      - **metrics.pods.target.averageValue** (<a href="{{< ref "../common-definitions/quantity#Quantity" >}}">Quantity</a>)

        averageValue is the target value of the average of the metric across all relevant pods (as a quantity)

      - **metrics.pods.target.value** (<a href="{{< ref "../common-definitions/quantity#Quantity" >}}">Quantity</a>)

        value is the target value of the metric (as a quantity).

  - **metrics.resource** (ResourceMetricSource)

    resource refers to a resource metric (such as those specified in requests and limits) known to Kubernetes describing each pod in the current scale target (e.g. CPU or memory). Such metrics are built in to Kubernetes, and have special scaling options on top of those available to normal per-pod metrics using the "pods" source.

    <a name="ResourceMetricSource"></a>
    *ResourceMetricSource indicates how to scale on a resource metric known to Kubernetes, as specified in requests and limits, describing each pod in the current scale target (e.g. CPU or memory).  The values will be averaged together before being compared to the target.  Such metrics are built in to Kubernetes, and have special scaling options on top of those available to normal per-pod metrics using the "pods" source.  Only one "target" type should be set.*

    - **metrics.resource.name** (string), required

      name is the name of the resource in question.

    - **metrics.resource.target** (MetricTarget), required

      target specifies the target value for the given metric

      <a name="MetricTarget"></a>
      *MetricTarget defines the target value, average value, or average utilization of a specific metric*

      - **metrics.resource.target.type** (string), required

        type represents whether the metric type is Utilization, Value, or AverageValue

      - **metrics.resource.target.averageUtilization** (int32)

        averageUtilization is the target value of the average of the resource metric across all relevant pods, represented as a percentage of the requested value of the resource for the pods. Currently only valid for Resource metric source type

      - **metrics.resource.target.averageValue** (<a href="{{< ref "../common-definitions/quantity#Quantity" >}}">Quantity</a>)

        averageValue is the target value of the average of the metric across all relevant pods (as a quantity)

      - **metrics.resource.target.value** (<a href="{{< ref "../common-definitions/quantity#Quantity" >}}">Quantity</a>)

        value is the target value of the metric (as a quantity).





## HorizontalPodAutoscalerStatus {#HorizontalPodAutoscalerStatus}

HorizontalPodAutoscalerStatus describes the current status of a horizontal pod autoscaler.

<hr>

- **conditions** ([]HorizontalPodAutoscalerCondition), required

  conditions is the set of conditions required for this autoscaler to scale its target, and indicates whether or not those conditions are met.

  <a name="HorizontalPodAutoscalerCondition"></a>
  *HorizontalPodAutoscalerCondition describes the state of a HorizontalPodAutoscaler at a certain point.*

  - **conditions.status** (string), required

    status is the status of the condition (True, False, Unknown)

  - **conditions.type** (string), required

    type describes the current condition

  - **conditions.lastTransitionTime** (Time)

    lastTransitionTime is the last time the condition transitioned from one status to another

    <a name="Time"></a>
    *Time is a wrapper around time.Time which supports correct marshaling to YAML and JSON.  Wrappers are provided for many of the factory methods that the time package offers.*

  - **conditions.message** (string)

    message is a human-readable explanation containing details about the transition

  - **conditions.reason** (string)

    reason is the reason for the condition's last transition.

- **currentReplicas** (int32), required

  currentReplicas is current number of replicas of pods managed by this autoscaler, as last seen by the autoscaler.

- **desiredReplicas** (int32), required

  desiredReplicas is the desired number of replicas of pods managed by this autoscaler, as last calculated by the autoscaler.

- **currentMetrics** ([]MetricStatus)

  currentMetrics is the last read state of the metrics used by this autoscaler.

  <a name="MetricStatus"></a>
  *MetricStatus describes the last-read state of a single metric.*

  - **currentMetrics.type** (string), required

    type is the type of metric source.  It will be one of "ContainerResource", "External", "Object", "Pods" or "Resource", each corresponds to a matching field in the object. Note: "ContainerResource" type is available on when the feature-gate HPAContainerMetrics is enabled

  - **currentMetrics.containerResource** (ContainerResourceMetricStatus)

    container resource refers to a resource metric (such as those specified in requests and limits) known to Kubernetes describing a single container in each pod in the current scale target (e.g. CPU or memory). Such metrics are built in to Kubernetes, and have special scaling options on top of those available to normal per-pod metrics using the "pods" source.

    <a name="ContainerResourceMetricStatus"></a>
    *ContainerResourceMetricStatus indicates the current value of a resource metric known to Kubernetes, as specified in requests and limits, describing a single container in each pod in the current scale target (e.g. CPU or memory).  Such metrics are built in to Kubernetes, and have special scaling options on top of those available to normal per-pod metrics using the "pods" source.*

    - **currentMetrics.containerResource.container** (string), required

      Container is the name of the container in the pods of the scaling target

    - **currentMetrics.containerResource.current** (MetricValueStatus), required

      current contains the current value for the given metric

      <a name="MetricValueStatus"></a>
      *MetricValueStatus holds the current value for a metric*

      - **currentMetrics.containerResource.current.averageUtilization** (int32)

        currentAverageUtilization is the current value of the average of the resource metric across all relevant pods, represented as a percentage of the requested value of the resource for the pods.

      - **currentMetrics.containerResource.current.averageValue** (<a href="{{< ref "../common-definitions/quantity#Quantity" >}}">Quantity</a>)

        averageValue is the current value of the average of the metric across all relevant pods (as a quantity)

      - **currentMetrics.containerResource.current.value** (<a href="{{< ref "../common-definitions/quantity#Quantity" >}}">Quantity</a>)

        value is the current value of the metric (as a quantity).

    - **currentMetrics.containerResource.name** (string), required

      Name is the name of the resource in question.

  - **currentMetrics.external** (ExternalMetricStatus)

    external refers to a global metric that is not associated with any Kubernetes object. It allows autoscaling based on information coming from components running outside of cluster (for example length of queue in cloud messaging service, or QPS from loadbalancer running outside of cluster).

    <a name="ExternalMetricStatus"></a>
    *ExternalMetricStatus indicates the current value of a global metric not associated with any Kubernetes object.*

    - **currentMetrics.external.current** (MetricValueStatus), required

      current contains the current value for the given metric

      <a name="MetricValueStatus"></a>
      *MetricValueStatus holds the current value for a metric*

      - **currentMetrics.external.current.averageUtilization** (int32)

        currentAverageUtilization is the current value of the average of the resource metric across all relevant pods, represented as a percentage of the requested value of the resource for the pods.

      - **currentMetrics.external.current.averageValue** (<a href="{{< ref "../common-definitions/quantity#Quantity" >}}">Quantity</a>)

        averageValue is the current value of the average of the metric across all relevant pods (as a quantity)

      - **currentMetrics.external.current.value** (<a href="{{< ref "../common-definitions/quantity#Quantity" >}}">Quantity</a>)

        value is the current value of the metric (as a quantity).

    - **currentMetrics.external.metric** (MetricIdentifier), required

      metric identifies the target metric by name and selector

      <a name="MetricIdentifier"></a>
      *MetricIdentifier defines the name and optionally selector for a metric*

      - **currentMetrics.external.metric.name** (string), required

        name is the name of the given metric

      - **currentMetrics.external.metric.selector** (<a href="{{< ref "../common-definitions/label-selector#LabelSelector" >}}">LabelSelector</a>)

        selector is the string-encoded form of a standard kubernetes label selector for the given metric When set, it is passed as an additional parameter to the metrics server for more specific metrics scoping. When unset, just the metricName will be used to gather metrics.

  - **currentMetrics.object** (ObjectMetricStatus)

    object refers to a metric describing a single kubernetes object (for example, hits-per-second on an Ingress object).

    <a name="ObjectMetricStatus"></a>
    *ObjectMetricStatus indicates the current value of a metric describing a kubernetes object (for example, hits-per-second on an Ingress object).*

    - **currentMetrics.object.current** (MetricValueStatus), required

      current contains the current value for the given metric

      <a name="MetricValueStatus"></a>
      *MetricValueStatus holds the current value for a metric*

      - **currentMetrics.object.current.averageUtilization** (int32)

        currentAverageUtilization is the current value of the average of the resource metric across all relevant pods, represented as a percentage of the requested value of the resource for the pods.

      - **currentMetrics.object.current.averageValue** (<a href="{{< ref "../common-definitions/quantity#Quantity" >}}">Quantity</a>)

        averageValue is the current value of the average of the metric across all relevant pods (as a quantity)

      - **currentMetrics.object.current.value** (<a href="{{< ref "../common-definitions/quantity#Quantity" >}}">Quantity</a>)

        value is the current value of the metric (as a quantity).

    - **currentMetrics.object.describedObject** (CrossVersionObjectReference), required


      <a name="CrossVersionObjectReference"></a>
      *CrossVersionObjectReference contains enough information to let you identify the referred resource.*

      - **currentMetrics.object.describedObject.kind** (string), required

        Kind of the referent; More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds"

      - **currentMetrics.object.describedObject.name** (string), required

        Name of the referent; More info: http://kubernetes.io/docs/user-guide/identifiers#names

      - **currentMetrics.object.describedObject.apiVersion** (string)

        API version of the referent

    - **currentMetrics.object.metric** (MetricIdentifier), required

      metric identifies the target metric by name and selector

      <a name="MetricIdentifier"></a>
      *MetricIdentifier defines the name and optionally selector for a metric*

      - **currentMetrics.object.metric.name** (string), required

        name is the name of the given metric

      - **currentMetrics.object.metric.selector** (<a href="{{< ref "../common-definitions/label-selector#LabelSelector" >}}">LabelSelector</a>)

        selector is the string-encoded form of a standard kubernetes label selector for the given metric When set, it is passed as an additional parameter to the metrics server for more specific metrics scoping. When unset, just the metricName will be used to gather metrics.

  - **currentMetrics.pods** (PodsMetricStatus)

    pods refers to a metric describing each pod in the current scale target (for example, transactions-processed-per-second).  The values will be averaged together before being compared to the target value.

    <a name="PodsMetricStatus"></a>
    *PodsMetricStatus indicates the current value of a metric describing each pod in the current scale target (for example, transactions-processed-per-second).*

    - **currentMetrics.pods.current** (MetricValueStatus), required

      current contains the current value for the given metric

      <a name="MetricValueStatus"></a>
      *MetricValueStatus holds the current value for a metric*

      - **currentMetrics.pods.current.averageUtilization** (int32)

        currentAverageUtilization is the current value of the average of the resource metric across all relevant pods, represented as a percentage of the requested value of the resource for the pods.

      - **currentMetrics.pods.current.averageValue** (<a href="{{< ref "../common-definitions/quantity#Quantity" >}}">Quantity</a>)

        averageValue is the current value of the average of the metric across all relevant pods (as a quantity)

      - **currentMetrics.pods.current.value** (<a href="{{< ref "../common-definitions/quantity#Quantity" >}}">Quantity</a>)

        value is the current value of the metric (as a quantity).

    - **currentMetrics.pods.metric** (MetricIdentifier), required

      metric identifies the target metric by name and selector

      <a name="MetricIdentifier"></a>
      *MetricIdentifier defines the name and optionally selector for a metric*

      - **currentMetrics.pods.metric.name** (string), required

        name is the name of the given metric

      - **currentMetrics.pods.metric.selector** (<a href="{{< ref "../common-definitions/label-selector#LabelSelector" >}}">LabelSelector</a>)

        selector is the string-encoded form of a standard kubernetes label selector for the given metric When set, it is passed as an additional parameter to the metrics server for more specific metrics scoping. When unset, just the metricName will be used to gather metrics.

  - **currentMetrics.resource** (ResourceMetricStatus)

    resource refers to a resource metric (such as those specified in requests and limits) known to Kubernetes describing each pod in the current scale target (e.g. CPU or memory). Such metrics are built in to Kubernetes, and have special scaling options on top of those available to normal per-pod metrics using the "pods" source.

    <a name="ResourceMetricStatus"></a>
    *ResourceMetricStatus indicates the current value of a resource metric known to Kubernetes, as specified in requests and limits, describing each pod in the current scale target (e.g. CPU or memory).  Such metrics are built in to Kubernetes, and have special scaling options on top of those available to normal per-pod metrics using the "pods" source.*

    - **currentMetrics.resource.current** (MetricValueStatus), required

      current contains the current value for the given metric

      <a name="MetricValueStatus"></a>
      *MetricValueStatus holds the current value for a metric*

      - **currentMetrics.resource.current.averageUtilization** (int32)

        currentAverageUtilization is the current value of the average of the resource metric across all relevant pods, represented as a percentage of the requested value of the resource for the pods.

      - **currentMetrics.resource.current.averageValue** (<a href="{{< ref "../common-definitions/quantity#Quantity" >}}">Quantity</a>)

        averageValue is the current value of the average of the metric across all relevant pods (as a quantity)

      - **currentMetrics.resource.current.value** (<a href="{{< ref "../common-definitions/quantity#Quantity" >}}">Quantity</a>)

        value is the current value of the metric (as a quantity).

    - **currentMetrics.resource.name** (string), required

      Name is the name of the resource in question.

- **lastScaleTime** (Time)

  lastScaleTime is the last time the HorizontalPodAutoscaler scaled the number of pods, used by the autoscaler to control how often the number of pods is changed.

  <a name="Time"></a>
  *Time is a wrapper around time.Time which supports correct marshaling to YAML and JSON.  Wrappers are provided for many of the factory methods that the time package offers.*

- **observedGeneration** (int64)

  observedGeneration is the most recent generation observed by this autoscaler.





## HorizontalPodAutoscalerList {#HorizontalPodAutoscalerList}

HorizontalPodAutoscalerList is a list of horizontal pod autoscaler objects.

<hr>

- **apiVersion**: autoscaling/v2beta2


- **kind**: HorizontalPodAutoscalerList


- **metadata** (<a href="{{< ref "../common-definitions/list-meta#ListMeta" >}}">ListMeta</a>)

  metadata is the standard list metadata.

- **items** ([]<a href="{{< ref "../workload-resources/horizontal-pod-autoscaler-v2beta2#HorizontalPodAutoscaler" >}}">HorizontalPodAutoscaler</a>), required

  items is the list of horizontal pod autoscaler objects.





## Operations {#Operations}



<hr>






### `get` read the specified HorizontalPodAutoscaler

#### HTTP Request

GET /apis/autoscaling/v2beta2/namespaces/{namespace}/horizontalpodautoscalers/{name}

#### Parameters


- **name** (*in path*): string, required

  name of the HorizontalPodAutoscaler


- **namespace** (*in path*): string, required

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>


- **pretty** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>



#### Response


200 (<a href="{{< ref "../workload-resources/horizontal-pod-autoscaler-v2beta2#HorizontalPodAutoscaler" >}}">HorizontalPodAutoscaler</a>): OK

401: Unauthorized


### `get` read status of the specified HorizontalPodAutoscaler

#### HTTP Request

GET /apis/autoscaling/v2beta2/namespaces/{namespace}/horizontalpodautoscalers/{name}/status

#### Parameters


- **name** (*in path*): string, required

  name of the HorizontalPodAutoscaler


- **namespace** (*in path*): string, required

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>


- **pretty** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>



#### Response


200 (<a href="{{< ref "../workload-resources/horizontal-pod-autoscaler-v2beta2#HorizontalPodAutoscaler" >}}">HorizontalPodAutoscaler</a>): OK

401: Unauthorized


### `list` list or watch objects of kind HorizontalPodAutoscaler

#### HTTP Request

GET /apis/autoscaling/v2beta2/namespaces/{namespace}/horizontalpodautoscalers

#### Parameters


- **namespace** (*in path*): string, required

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>


- **allowWatchBookmarks** (*in query*): boolean

  <a href="{{< ref "../common-parameters/common-parameters#allowWatchBookmarks" >}}">allowWatchBookmarks</a>


- **continue** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#continue" >}}">continue</a>


- **fieldSelector** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldSelector" >}}">fieldSelector</a>


- **labelSelector** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#labelSelector" >}}">labelSelector</a>


- **limit** (*in query*): integer

  <a href="{{< ref "../common-parameters/common-parameters#limit" >}}">limit</a>


- **pretty** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>


- **resourceVersion** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersion" >}}">resourceVersion</a>


- **resourceVersionMatch** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersionMatch" >}}">resourceVersionMatch</a>


- **timeoutSeconds** (*in query*): integer

  <a href="{{< ref "../common-parameters/common-parameters#timeoutSeconds" >}}">timeoutSeconds</a>


- **watch** (*in query*): boolean

  <a href="{{< ref "../common-parameters/common-parameters#watch" >}}">watch</a>



#### Response


200 (<a href="{{< ref "../workload-resources/horizontal-pod-autoscaler-v2beta2#HorizontalPodAutoscalerList" >}}">HorizontalPodAutoscalerList</a>): OK

401: Unauthorized


### `list` list or watch objects of kind HorizontalPodAutoscaler

#### HTTP Request

GET /apis/autoscaling/v2beta2/horizontalpodautoscalers

#### Parameters


- **allowWatchBookmarks** (*in query*): boolean

  <a href="{{< ref "../common-parameters/common-parameters#allowWatchBookmarks" >}}">allowWatchBookmarks</a>


- **continue** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#continue" >}}">continue</a>


- **fieldSelector** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldSelector" >}}">fieldSelector</a>


- **labelSelector** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#labelSelector" >}}">labelSelector</a>


- **limit** (*in query*): integer

  <a href="{{< ref "../common-parameters/common-parameters#limit" >}}">limit</a>


- **pretty** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>


- **resourceVersion** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersion" >}}">resourceVersion</a>


- **resourceVersionMatch** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersionMatch" >}}">resourceVersionMatch</a>


- **timeoutSeconds** (*in query*): integer

  <a href="{{< ref "../common-parameters/common-parameters#timeoutSeconds" >}}">timeoutSeconds</a>


- **watch** (*in query*): boolean

  <a href="{{< ref "../common-parameters/common-parameters#watch" >}}">watch</a>



#### Response


200 (<a href="{{< ref "../workload-resources/horizontal-pod-autoscaler-v2beta2#HorizontalPodAutoscalerList" >}}">HorizontalPodAutoscalerList</a>): OK

401: Unauthorized


### `create` create a HorizontalPodAutoscaler

#### HTTP Request

POST /apis/autoscaling/v2beta2/namespaces/{namespace}/horizontalpodautoscalers

#### Parameters


- **namespace** (*in path*): string, required

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>


- **body**: <a href="{{< ref "../workload-resources/horizontal-pod-autoscaler-v2beta2#HorizontalPodAutoscaler" >}}">HorizontalPodAutoscaler</a>, required

  


- **dryRun** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>


- **fieldManager** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>


- **pretty** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>



#### Response


200 (<a href="{{< ref "../workload-resources/horizontal-pod-autoscaler-v2beta2#HorizontalPodAutoscaler" >}}">HorizontalPodAutoscaler</a>): OK

201 (<a href="{{< ref "../workload-resources/horizontal-pod-autoscaler-v2beta2#HorizontalPodAutoscaler" >}}">HorizontalPodAutoscaler</a>): Created

202 (<a href="{{< ref "../workload-resources/horizontal-pod-autoscaler-v2beta2#HorizontalPodAutoscaler" >}}">HorizontalPodAutoscaler</a>): Accepted

401: Unauthorized


### `update` replace the specified HorizontalPodAutoscaler

#### HTTP Request

PUT /apis/autoscaling/v2beta2/namespaces/{namespace}/horizontalpodautoscalers/{name}

#### Parameters


- **name** (*in path*): string, required

  name of the HorizontalPodAutoscaler


- **namespace** (*in path*): string, required

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>


- **body**: <a href="{{< ref "../workload-resources/horizontal-pod-autoscaler-v2beta2#HorizontalPodAutoscaler" >}}">HorizontalPodAutoscaler</a>, required

  


- **dryRun** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>


- **fieldManager** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>


- **pretty** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>



#### Response


200 (<a href="{{< ref "../workload-resources/horizontal-pod-autoscaler-v2beta2#HorizontalPodAutoscaler" >}}">HorizontalPodAutoscaler</a>): OK

201 (<a href="{{< ref "../workload-resources/horizontal-pod-autoscaler-v2beta2#HorizontalPodAutoscaler" >}}">HorizontalPodAutoscaler</a>): Created

401: Unauthorized


### `update` replace status of the specified HorizontalPodAutoscaler

#### HTTP Request

PUT /apis/autoscaling/v2beta2/namespaces/{namespace}/horizontalpodautoscalers/{name}/status

#### Parameters


- **name** (*in path*): string, required

  name of the HorizontalPodAutoscaler


- **namespace** (*in path*): string, required

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>


- **body**: <a href="{{< ref "../workload-resources/horizontal-pod-autoscaler-v2beta2#HorizontalPodAutoscaler" >}}">HorizontalPodAutoscaler</a>, required

  


- **dryRun** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>


- **fieldManager** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>


- **pretty** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>



#### Response


200 (<a href="{{< ref "../workload-resources/horizontal-pod-autoscaler-v2beta2#HorizontalPodAutoscaler" >}}">HorizontalPodAutoscaler</a>): OK

201 (<a href="{{< ref "../workload-resources/horizontal-pod-autoscaler-v2beta2#HorizontalPodAutoscaler" >}}">HorizontalPodAutoscaler</a>): Created

401: Unauthorized


### `patch` partially update the specified HorizontalPodAutoscaler

#### HTTP Request

PATCH /apis/autoscaling/v2beta2/namespaces/{namespace}/horizontalpodautoscalers/{name}

#### Parameters


- **name** (*in path*): string, required

  name of the HorizontalPodAutoscaler


- **namespace** (*in path*): string, required

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>


- **body**: <a href="{{< ref "../common-definitions/patch#Patch" >}}">Patch</a>, required

  


- **dryRun** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>


- **fieldManager** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>


- **force** (*in query*): boolean

  <a href="{{< ref "../common-parameters/common-parameters#force" >}}">force</a>


- **pretty** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>



#### Response


200 (<a href="{{< ref "../workload-resources/horizontal-pod-autoscaler-v2beta2#HorizontalPodAutoscaler" >}}">HorizontalPodAutoscaler</a>): OK

201 (<a href="{{< ref "../workload-resources/horizontal-pod-autoscaler-v2beta2#HorizontalPodAutoscaler" >}}">HorizontalPodAutoscaler</a>): Created

401: Unauthorized


### `patch` partially update status of the specified HorizontalPodAutoscaler

#### HTTP Request

PATCH /apis/autoscaling/v2beta2/namespaces/{namespace}/horizontalpodautoscalers/{name}/status

#### Parameters


- **name** (*in path*): string, required

  name of the HorizontalPodAutoscaler


- **namespace** (*in path*): string, required

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>


- **body**: <a href="{{< ref "../common-definitions/patch#Patch" >}}">Patch</a>, required

  


- **dryRun** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>


- **fieldManager** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>


- **force** (*in query*): boolean

  <a href="{{< ref "../common-parameters/common-parameters#force" >}}">force</a>


- **pretty** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>



#### Response


200 (<a href="{{< ref "../workload-resources/horizontal-pod-autoscaler-v2beta2#HorizontalPodAutoscaler" >}}">HorizontalPodAutoscaler</a>): OK

201 (<a href="{{< ref "../workload-resources/horizontal-pod-autoscaler-v2beta2#HorizontalPodAutoscaler" >}}">HorizontalPodAutoscaler</a>): Created

401: Unauthorized


### `delete` delete a HorizontalPodAutoscaler

#### HTTP Request

DELETE /apis/autoscaling/v2beta2/namespaces/{namespace}/horizontalpodautoscalers/{name}

#### Parameters


- **name** (*in path*): string, required

  name of the HorizontalPodAutoscaler


- **namespace** (*in path*): string, required

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>


- **body**: <a href="{{< ref "../common-definitions/delete-options#DeleteOptions" >}}">DeleteOptions</a>

  


- **dryRun** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>


- **gracePeriodSeconds** (*in query*): integer

  <a href="{{< ref "../common-parameters/common-parameters#gracePeriodSeconds" >}}">gracePeriodSeconds</a>


- **pretty** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>


- **propagationPolicy** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#propagationPolicy" >}}">propagationPolicy</a>



#### Response


200 (<a href="{{< ref "../common-definitions/status#Status" >}}">Status</a>): OK

202 (<a href="{{< ref "../common-definitions/status#Status" >}}">Status</a>): Accepted

401: Unauthorized


### `deletecollection` delete collection of HorizontalPodAutoscaler

#### HTTP Request

DELETE /apis/autoscaling/v2beta2/namespaces/{namespace}/horizontalpodautoscalers

#### Parameters


- **namespace** (*in path*): string, required

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>


- **body**: <a href="{{< ref "../common-definitions/delete-options#DeleteOptions" >}}">DeleteOptions</a>

  


- **continue** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#continue" >}}">continue</a>


- **dryRun** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>


- **fieldSelector** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldSelector" >}}">fieldSelector</a>


- **gracePeriodSeconds** (*in query*): integer

  <a href="{{< ref "../common-parameters/common-parameters#gracePeriodSeconds" >}}">gracePeriodSeconds</a>


- **labelSelector** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#labelSelector" >}}">labelSelector</a>


- **limit** (*in query*): integer

  <a href="{{< ref "../common-parameters/common-parameters#limit" >}}">limit</a>


- **pretty** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>


- **propagationPolicy** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#propagationPolicy" >}}">propagationPolicy</a>


- **resourceVersion** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersion" >}}">resourceVersion</a>


- **resourceVersionMatch** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersionMatch" >}}">resourceVersionMatch</a>


- **timeoutSeconds** (*in query*): integer

  <a href="{{< ref "../common-parameters/common-parameters#timeoutSeconds" >}}">timeoutSeconds</a>



#### Response


200 (<a href="{{< ref "../common-definitions/status#Status" >}}">Status</a>): OK

401: Unauthorized

