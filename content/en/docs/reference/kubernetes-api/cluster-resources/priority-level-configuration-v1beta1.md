---
api_metadata:
  apiVersion: "flowcontrol.apiserver.k8s.io/v1beta1"
  import: "k8s.io/api/flowcontrol/v1beta1"
  kind: "PriorityLevelConfiguration"
content_type: "api_reference"
description: "PriorityLevelConfiguration represents the configuration of a priority level."
title: "PriorityLevelConfiguration v1beta1"
weight: 8
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

`apiVersion: flowcontrol.apiserver.k8s.io/v1beta1`

`import "k8s.io/api/flowcontrol/v1beta1"`


## PriorityLevelConfiguration {#PriorityLevelConfiguration}

PriorityLevelConfiguration represents the configuration of a priority level.

<hr>

- **apiVersion**: flowcontrol.apiserver.k8s.io/v1beta1


- **kind**: PriorityLevelConfiguration


- **metadata** (<a href="{{< ref "../common-definitions/object-meta#ObjectMeta" >}}">ObjectMeta</a>)

  `metadata` is the standard object's metadata. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

- **spec** (<a href="{{< ref "../cluster-resources/priority-level-configuration-v1beta1#PriorityLevelConfigurationSpec" >}}">PriorityLevelConfigurationSpec</a>)

  `spec` is the specification of the desired behavior of a "request-priority". More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status

- **status** (<a href="{{< ref "../cluster-resources/priority-level-configuration-v1beta1#PriorityLevelConfigurationStatus" >}}">PriorityLevelConfigurationStatus</a>)

  `status` is the current status of a "request-priority". More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status





## PriorityLevelConfigurationSpec {#PriorityLevelConfigurationSpec}

PriorityLevelConfigurationSpec specifies the configuration of a priority level.

<hr>

- **type** (string), required

  `type` indicates whether this priority level is subject to limitation on request execution.  A value of `"Exempt"` means that requests of this priority level are not subject to a limit (and thus are never queued) and do not detract from the capacity made available to other priority levels.  A value of `"Limited"` means that (a) requests of this priority level _are_ subject to limits and (b) some of the server's limited capacity is made available exclusively to this priority level. Required.

- **limited** (LimitedPriorityLevelConfiguration)

  `limited` specifies how requests are handled for a Limited priority level. This field must be non-empty if and only if `type` is `"Limited"`.

  <a name="LimitedPriorityLevelConfiguration"></a>
  *LimitedPriorityLevelConfiguration specifies how to handle requests that are subject to limits. It addresses two issues:
   * How are requests for this priority level limited?
   * What should be done with requests that exceed the limit?*

  - **limited.assuredConcurrencyShares** (int32)

    `assuredConcurrencyShares` (ACS) configures the execution limit, which is a limit on the number of requests of this priority level that may be exeucting at a given time.  ACS must be a positive number. The server's concurrency limit (SCL) is divided among the concurrency-controlled priority levels in proportion to their assured concurrency shares. This produces the assured concurrency value (ACV) --- the number of requests that may be executing at a time --- for each such priority level:
    
                ACV(l) = ceil( SCL * ACS(l) / ( sum[priority levels k] ACS(k) ) )
    
    bigger numbers of ACS mean more reserved concurrent requests (at the expense of every other PL). This field has a default value of 30.

  - **limited.limitResponse** (LimitResponse)

    `limitResponse` indicates what to do with requests that can not be executed right now

    <a name="LimitResponse"></a>
    *LimitResponse defines how to handle requests that can not be executed right now.*

    - **limited.limitResponse.type** (string), required

      `type` is "Queue" or "Reject". "Queue" means that requests that can not be executed upon arrival are held in a queue until they can be executed or a queuing limit is reached. "Reject" means that requests that can not be executed upon arrival are rejected. Required.

    - **limited.limitResponse.queuing** (QueuingConfiguration)

      `queuing` holds the configuration parameters for queuing. This field may be non-empty only if `type` is `"Queue"`.

      <a name="QueuingConfiguration"></a>
      *QueuingConfiguration holds the configuration parameters for queuing*

      - **limited.limitResponse.queuing.handSize** (int32)

        `handSize` is a small positive number that configures the shuffle sharding of requests into queues.  When enqueuing a request at this priority level the request's flow identifier (a string pair) is hashed and the hash value is used to shuffle the list of queues and deal a hand of the size specified here.  The request is put into one of the shortest queues in that hand. `handSize` must be no larger than `queues`, and should be significantly smaller (so that a few heavy flows do not saturate most of the queues).  See the user-facing documentation for more extensive guidance on setting this field.  This field has a default value of 8.

      - **limited.limitResponse.queuing.queueLengthLimit** (int32)

        `queueLengthLimit` is the maximum number of requests allowed to be waiting in a given queue of this priority level at a time; excess requests are rejected.  This value must be positive.  If not specified, it will be defaulted to 50.

      - **limited.limitResponse.queuing.queues** (int32)

        `queues` is the number of queues for this priority level. The queues exist independently at each apiserver. The value must be positive.  Setting it to 1 effectively precludes shufflesharding and thus makes the distinguisher method of associated flow schemas irrelevant.  This field has a default value of 64.





## PriorityLevelConfigurationStatus {#PriorityLevelConfigurationStatus}

PriorityLevelConfigurationStatus represents the current state of a "request-priority".

<hr>

- **conditions** ([]PriorityLevelConfigurationCondition)

  *Map: unique values on key type will be kept during a merge*
  
  `conditions` is the current state of "request-priority".

  <a name="PriorityLevelConfigurationCondition"></a>
  *PriorityLevelConfigurationCondition defines the condition of priority level.*

  - **conditions.lastTransitionTime** (Time)

    `lastTransitionTime` is the last time the condition transitioned from one status to another.

    <a name="Time"></a>
    *Time is a wrapper around time.Time which supports correct marshaling to YAML and JSON.  Wrappers are provided for many of the factory methods that the time package offers.*

  - **conditions.message** (string)

    `message` is a human-readable message indicating details about last transition.

  - **conditions.reason** (string)

    `reason` is a unique, one-word, CamelCase reason for the condition's last transition.

  - **conditions.status** (string)

    `status` is the status of the condition. Can be True, False, Unknown. Required.

  - **conditions.type** (string)

    `type` is the type of the condition. Required.





## PriorityLevelConfigurationList {#PriorityLevelConfigurationList}

PriorityLevelConfigurationList is a list of PriorityLevelConfiguration objects.

<hr>

- **apiVersion**: flowcontrol.apiserver.k8s.io/v1beta1


- **kind**: PriorityLevelConfigurationList


- **metadata** (<a href="{{< ref "../common-definitions/list-meta#ListMeta" >}}">ListMeta</a>)

  `metadata` is the standard object's metadata. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

- **items** ([]<a href="{{< ref "../cluster-resources/priority-level-configuration-v1beta1#PriorityLevelConfiguration" >}}">PriorityLevelConfiguration</a>), required

  `items` is a list of request-priorities.





## Operations {#Operations}



<hr>






### `get` read the specified PriorityLevelConfiguration

#### HTTP Request

GET /apis/flowcontrol.apiserver.k8s.io/v1beta1/prioritylevelconfigurations/{name}

#### Parameters


- **name** (*in path*): string, required

  name of the PriorityLevelConfiguration


- **pretty** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>



#### Response


200 (<a href="{{< ref "../cluster-resources/priority-level-configuration-v1beta1#PriorityLevelConfiguration" >}}">PriorityLevelConfiguration</a>): OK

401: Unauthorized


### `get` read status of the specified PriorityLevelConfiguration

#### HTTP Request

GET /apis/flowcontrol.apiserver.k8s.io/v1beta1/prioritylevelconfigurations/{name}/status

#### Parameters


- **name** (*in path*): string, required

  name of the PriorityLevelConfiguration


- **pretty** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>



#### Response


200 (<a href="{{< ref "../cluster-resources/priority-level-configuration-v1beta1#PriorityLevelConfiguration" >}}">PriorityLevelConfiguration</a>): OK

401: Unauthorized


### `list` list or watch objects of kind PriorityLevelConfiguration

#### HTTP Request

GET /apis/flowcontrol.apiserver.k8s.io/v1beta1/prioritylevelconfigurations

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


200 (<a href="{{< ref "../cluster-resources/priority-level-configuration-v1beta1#PriorityLevelConfigurationList" >}}">PriorityLevelConfigurationList</a>): OK

401: Unauthorized


### `create` create a PriorityLevelConfiguration

#### HTTP Request

POST /apis/flowcontrol.apiserver.k8s.io/v1beta1/prioritylevelconfigurations

#### Parameters


- **body**: <a href="{{< ref "../cluster-resources/priority-level-configuration-v1beta1#PriorityLevelConfiguration" >}}">PriorityLevelConfiguration</a>, required

  


- **dryRun** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>


- **fieldManager** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>


- **pretty** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>



#### Response


200 (<a href="{{< ref "../cluster-resources/priority-level-configuration-v1beta1#PriorityLevelConfiguration" >}}">PriorityLevelConfiguration</a>): OK

201 (<a href="{{< ref "../cluster-resources/priority-level-configuration-v1beta1#PriorityLevelConfiguration" >}}">PriorityLevelConfiguration</a>): Created

202 (<a href="{{< ref "../cluster-resources/priority-level-configuration-v1beta1#PriorityLevelConfiguration" >}}">PriorityLevelConfiguration</a>): Accepted

401: Unauthorized


### `update` replace the specified PriorityLevelConfiguration

#### HTTP Request

PUT /apis/flowcontrol.apiserver.k8s.io/v1beta1/prioritylevelconfigurations/{name}

#### Parameters


- **name** (*in path*): string, required

  name of the PriorityLevelConfiguration


- **body**: <a href="{{< ref "../cluster-resources/priority-level-configuration-v1beta1#PriorityLevelConfiguration" >}}">PriorityLevelConfiguration</a>, required

  


- **dryRun** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>


- **fieldManager** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>


- **pretty** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>



#### Response


200 (<a href="{{< ref "../cluster-resources/priority-level-configuration-v1beta1#PriorityLevelConfiguration" >}}">PriorityLevelConfiguration</a>): OK

201 (<a href="{{< ref "../cluster-resources/priority-level-configuration-v1beta1#PriorityLevelConfiguration" >}}">PriorityLevelConfiguration</a>): Created

401: Unauthorized


### `update` replace status of the specified PriorityLevelConfiguration

#### HTTP Request

PUT /apis/flowcontrol.apiserver.k8s.io/v1beta1/prioritylevelconfigurations/{name}/status

#### Parameters


- **name** (*in path*): string, required

  name of the PriorityLevelConfiguration


- **body**: <a href="{{< ref "../cluster-resources/priority-level-configuration-v1beta1#PriorityLevelConfiguration" >}}">PriorityLevelConfiguration</a>, required

  


- **dryRun** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>


- **fieldManager** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>


- **pretty** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>



#### Response


200 (<a href="{{< ref "../cluster-resources/priority-level-configuration-v1beta1#PriorityLevelConfiguration" >}}">PriorityLevelConfiguration</a>): OK

201 (<a href="{{< ref "../cluster-resources/priority-level-configuration-v1beta1#PriorityLevelConfiguration" >}}">PriorityLevelConfiguration</a>): Created

401: Unauthorized


### `patch` partially update the specified PriorityLevelConfiguration

#### HTTP Request

PATCH /apis/flowcontrol.apiserver.k8s.io/v1beta1/prioritylevelconfigurations/{name}

#### Parameters


- **name** (*in path*): string, required

  name of the PriorityLevelConfiguration


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


200 (<a href="{{< ref "../cluster-resources/priority-level-configuration-v1beta1#PriorityLevelConfiguration" >}}">PriorityLevelConfiguration</a>): OK

201 (<a href="{{< ref "../cluster-resources/priority-level-configuration-v1beta1#PriorityLevelConfiguration" >}}">PriorityLevelConfiguration</a>): Created

401: Unauthorized


### `patch` partially update status of the specified PriorityLevelConfiguration

#### HTTP Request

PATCH /apis/flowcontrol.apiserver.k8s.io/v1beta1/prioritylevelconfigurations/{name}/status

#### Parameters


- **name** (*in path*): string, required

  name of the PriorityLevelConfiguration


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


200 (<a href="{{< ref "../cluster-resources/priority-level-configuration-v1beta1#PriorityLevelConfiguration" >}}">PriorityLevelConfiguration</a>): OK

201 (<a href="{{< ref "../cluster-resources/priority-level-configuration-v1beta1#PriorityLevelConfiguration" >}}">PriorityLevelConfiguration</a>): Created

401: Unauthorized


### `delete` delete a PriorityLevelConfiguration

#### HTTP Request

DELETE /apis/flowcontrol.apiserver.k8s.io/v1beta1/prioritylevelconfigurations/{name}

#### Parameters


- **name** (*in path*): string, required

  name of the PriorityLevelConfiguration


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


### `deletecollection` delete collection of PriorityLevelConfiguration

#### HTTP Request

DELETE /apis/flowcontrol.apiserver.k8s.io/v1beta1/prioritylevelconfigurations

#### Parameters


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

