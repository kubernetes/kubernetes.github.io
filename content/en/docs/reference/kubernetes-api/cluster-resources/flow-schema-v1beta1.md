---
api_metadata:
  apiVersion: "flowcontrol.apiserver.k8s.io/v1beta1"
  import: "k8s.io/api/flowcontrol/v1beta1"
  kind: "FlowSchema"
content_type: "api_reference"
description: "FlowSchema defines the schema of a group of flows."
title: "FlowSchema v1beta1"
weight: 7
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


## FlowSchema {#FlowSchema}

FlowSchema defines the schema of a group of flows. Note that a flow is made up of a set of inbound API requests with similar attributes and is identified by a pair of strings: the name of the FlowSchema and a "flow distinguisher".

<hr>

- **apiVersion**: flowcontrol.apiserver.k8s.io/v1beta1


- **kind**: FlowSchema


- **metadata** (<a href="{{< ref "../common-definitions/object-meta#ObjectMeta" >}}">ObjectMeta</a>)

  `metadata` is the standard object's metadata. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

- **spec** (<a href="{{< ref "../cluster-resources/flow-schema-v1beta1#FlowSchemaSpec" >}}">FlowSchemaSpec</a>)

  `spec` is the specification of the desired behavior of a FlowSchema. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status

- **status** (<a href="{{< ref "../cluster-resources/flow-schema-v1beta1#FlowSchemaStatus" >}}">FlowSchemaStatus</a>)

  `status` is the current status of a FlowSchema. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status





## FlowSchemaSpec {#FlowSchemaSpec}

FlowSchemaSpec describes how the FlowSchema's specification looks like.

<hr>

- **priorityLevelConfiguration** (PriorityLevelConfigurationReference), required

  `priorityLevelConfiguration` should reference a PriorityLevelConfiguration in the cluster. If the reference cannot be resolved, the FlowSchema will be ignored and marked as invalid in its status. Required.

  <a name="PriorityLevelConfigurationReference"></a>
  *PriorityLevelConfigurationReference contains information that points to the "request-priority" being used.*

  - **priorityLevelConfiguration.name** (string), required

    `name` is the name of the priority level configuration being referenced Required.

- **distinguisherMethod** (FlowDistinguisherMethod)

  `distinguisherMethod` defines how to compute the flow distinguisher for requests that match this schema. `nil` specifies that the distinguisher is disabled and thus will always be the empty string.

  <a name="FlowDistinguisherMethod"></a>
  *FlowDistinguisherMethod specifies the method of a flow distinguisher.*

  - **distinguisherMethod.type** (string), required

    `type` is the type of flow distinguisher method The supported types are "ByUser" and "ByNamespace". Required.

- **matchingPrecedence** (int32)

  `matchingPrecedence` is used to choose among the FlowSchemas that match a given request. The chosen FlowSchema is among those with the numerically lowest (which we take to be logically highest) MatchingPrecedence.  Each MatchingPrecedence value must be ranged in [1,10000]. Note that if the precedence is not specified, it will be set to 1000 as default.

- **rules** ([]PolicyRulesWithSubjects)

  *Atomic: will be replaced during a merge*
  
  `rules` describes which requests will match this flow schema. This FlowSchema matches a request if and only if at least one member of rules matches the request. if it is an empty slice, there will be no requests matching the FlowSchema.

  <a name="PolicyRulesWithSubjects"></a>
  *PolicyRulesWithSubjects prescribes a test that applies to a request to an apiserver. The test considers the subject making the request, the verb being requested, and the resource to be acted upon. This PolicyRulesWithSubjects matches a request if and only if both (a) at least one member of subjects matches the request and (b) at least one member of resourceRules or nonResourceRules matches the request.*

  - **rules.subjects** ([]Subject), required

    *Atomic: will be replaced during a merge*
    
    subjects is the list of normal user, serviceaccount, or group that this rule cares about. There must be at least one member in this slice. A slice that includes both the system:authenticated and system:unauthenticated user groups matches every request. Required.

    <a name="Subject"></a>
    *Subject matches the originator of a request, as identified by the request authentication system. There are three ways of matching an originator; by user, group, or service account.*

    - **rules.subjects.kind** (string), required

      `kind` indicates which one of the other fields is non-empty. Required

    - **rules.subjects.group** (GroupSubject)

      `group` matches based on user group name.

      <a name="GroupSubject"></a>
      *GroupSubject holds detailed information for group-kind subject.*

      - **rules.subjects.group.name** (string), required

        name is the user group that matches, or "*" to match all user groups. See https://github.com/kubernetes/apiserver/blob/master/pkg/authentication/user/user.go for some well-known group names. Required.

    - **rules.subjects.serviceAccount** (ServiceAccountSubject)

      `serviceAccount` matches ServiceAccounts.

      <a name="ServiceAccountSubject"></a>
      *ServiceAccountSubject holds detailed information for service-account-kind subject.*

      - **rules.subjects.serviceAccount.name** (string), required

        `name` is the name of matching ServiceAccount objects, or "*" to match regardless of name. Required.

      - **rules.subjects.serviceAccount.namespace** (string), required

        `namespace` is the namespace of matching ServiceAccount objects. Required.

    - **rules.subjects.user** (UserSubject)

      `user` matches based on username.

      <a name="UserSubject"></a>
      *UserSubject holds detailed information for user-kind subject.*

      - **rules.subjects.user.name** (string), required

        `name` is the username that matches, or "*" to match all usernames. Required.

  - **rules.nonResourceRules** ([]NonResourcePolicyRule)

    *Atomic: will be replaced during a merge*
    
    `nonResourceRules` is a list of NonResourcePolicyRules that identify matching requests according to their verb and the target non-resource URL.

    <a name="NonResourcePolicyRule"></a>
    *NonResourcePolicyRule is a predicate that matches non-resource requests according to their verb and the target non-resource URL. A NonResourcePolicyRule matches a request if and only if both (a) at least one member of verbs matches the request and (b) at least one member of nonResourceURLs matches the request.*

    - **rules.nonResourceRules.nonResourceURLs** ([]string), required

      *Set: unique values will be kept during a merge*
      
      `nonResourceURLs` is a set of url prefixes that a user should have access to and may not be empty. For example:
        - "/healthz" is legal
        - "/hea*" is illegal
        - "/hea" is legal but matches nothing
        - "/hea/*" also matches nothing
        - "/healthz/*" matches all per-component health checks.
      "*" matches all non-resource urls. if it is present, it must be the only entry. Required.

    - **rules.nonResourceRules.verbs** ([]string), required

      *Set: unique values will be kept during a merge*
      
      `verbs` is a list of matching verbs and may not be empty. "*" matches all verbs. If it is present, it must be the only entry. Required.

  - **rules.resourceRules** ([]ResourcePolicyRule)

    *Atomic: will be replaced during a merge*
    
    `resourceRules` is a slice of ResourcePolicyRules that identify matching requests according to their verb and the target resource. At least one of `resourceRules` and `nonResourceRules` has to be non-empty.

    <a name="ResourcePolicyRule"></a>
    *ResourcePolicyRule is a predicate that matches some resource requests, testing the request's verb and the target resource. A ResourcePolicyRule matches a resource request if and only if: (a) at least one member of verbs matches the request, (b) at least one member of apiGroups matches the request, (c) at least one member of resources matches the request, and (d) least one member of namespaces matches the request.*

    - **rules.resourceRules.apiGroups** ([]string), required

      *Set: unique values will be kept during a merge*
      
      `apiGroups` is a list of matching API groups and may not be empty. "*" matches all API groups and, if present, must be the only entry. Required.

    - **rules.resourceRules.resources** ([]string), required

      *Set: unique values will be kept during a merge*
      
      `resources` is a list of matching resources (i.e., lowercase and plural) with, if desired, subresource.  For example, [ "services", "nodes/status" ].  This list may not be empty. "*" matches all resources and, if present, must be the only entry. Required.

    - **rules.resourceRules.verbs** ([]string), required

      *Set: unique values will be kept during a merge*
      
      `verbs` is a list of matching verbs and may not be empty. "*" matches all verbs and, if present, must be the only entry. Required.

    - **rules.resourceRules.clusterScope** (boolean)

      `clusterScope` indicates whether to match requests that do not specify a namespace (which happens either because the resource is not namespaced or the request targets all namespaces). If this field is omitted or false then the `namespaces` field must contain a non-empty list.

    - **rules.resourceRules.namespaces** ([]string)

      *Set: unique values will be kept during a merge*
      
      `namespaces` is a list of target namespaces that restricts matches.  A request that specifies a target namespace matches only if either (a) this list contains that target namespace or (b) this list contains "*".  Note that "*" matches any specified namespace but does not match a request that _does not specify_ a namespace (see the `clusterScope` field for that). This list may be empty, but only if `clusterScope` is true.





## FlowSchemaStatus {#FlowSchemaStatus}

FlowSchemaStatus represents the current state of a FlowSchema.

<hr>

- **conditions** ([]FlowSchemaCondition)

  *Map: unique values on key type will be kept during a merge*
  
  `conditions` is a list of the current states of FlowSchema.

  <a name="FlowSchemaCondition"></a>
  *FlowSchemaCondition describes conditions for a FlowSchema.*

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





## FlowSchemaList {#FlowSchemaList}

FlowSchemaList is a list of FlowSchema objects.

<hr>

- **apiVersion**: flowcontrol.apiserver.k8s.io/v1beta1


- **kind**: FlowSchemaList


- **metadata** (<a href="{{< ref "../common-definitions/list-meta#ListMeta" >}}">ListMeta</a>)

  `metadata` is the standard list metadata. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

- **items** ([]<a href="{{< ref "../cluster-resources/flow-schema-v1beta1#FlowSchema" >}}">FlowSchema</a>), required

  `items` is a list of FlowSchemas.





## Operations {#Operations}



<hr>






### `get` read the specified FlowSchema

#### HTTP Request

GET /apis/flowcontrol.apiserver.k8s.io/v1beta1/flowschemas/{name}

#### Parameters


- **name** (*in path*): string, required

  name of the FlowSchema


- **pretty** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>



#### Response


200 (<a href="{{< ref "../cluster-resources/flow-schema-v1beta1#FlowSchema" >}}">FlowSchema</a>): OK

401: Unauthorized


### `get` read status of the specified FlowSchema

#### HTTP Request

GET /apis/flowcontrol.apiserver.k8s.io/v1beta1/flowschemas/{name}/status

#### Parameters


- **name** (*in path*): string, required

  name of the FlowSchema


- **pretty** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>



#### Response


200 (<a href="{{< ref "../cluster-resources/flow-schema-v1beta1#FlowSchema" >}}">FlowSchema</a>): OK

401: Unauthorized


### `list` list or watch objects of kind FlowSchema

#### HTTP Request

GET /apis/flowcontrol.apiserver.k8s.io/v1beta1/flowschemas

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


200 (<a href="{{< ref "../cluster-resources/flow-schema-v1beta1#FlowSchemaList" >}}">FlowSchemaList</a>): OK

401: Unauthorized


### `create` create a FlowSchema

#### HTTP Request

POST /apis/flowcontrol.apiserver.k8s.io/v1beta1/flowschemas

#### Parameters


- **body**: <a href="{{< ref "../cluster-resources/flow-schema-v1beta1#FlowSchema" >}}">FlowSchema</a>, required

  


- **dryRun** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>


- **fieldManager** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>


- **pretty** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>



#### Response


200 (<a href="{{< ref "../cluster-resources/flow-schema-v1beta1#FlowSchema" >}}">FlowSchema</a>): OK

201 (<a href="{{< ref "../cluster-resources/flow-schema-v1beta1#FlowSchema" >}}">FlowSchema</a>): Created

202 (<a href="{{< ref "../cluster-resources/flow-schema-v1beta1#FlowSchema" >}}">FlowSchema</a>): Accepted

401: Unauthorized


### `update` replace the specified FlowSchema

#### HTTP Request

PUT /apis/flowcontrol.apiserver.k8s.io/v1beta1/flowschemas/{name}

#### Parameters


- **name** (*in path*): string, required

  name of the FlowSchema


- **body**: <a href="{{< ref "../cluster-resources/flow-schema-v1beta1#FlowSchema" >}}">FlowSchema</a>, required

  


- **dryRun** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>


- **fieldManager** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>


- **pretty** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>



#### Response


200 (<a href="{{< ref "../cluster-resources/flow-schema-v1beta1#FlowSchema" >}}">FlowSchema</a>): OK

201 (<a href="{{< ref "../cluster-resources/flow-schema-v1beta1#FlowSchema" >}}">FlowSchema</a>): Created

401: Unauthorized


### `update` replace status of the specified FlowSchema

#### HTTP Request

PUT /apis/flowcontrol.apiserver.k8s.io/v1beta1/flowschemas/{name}/status

#### Parameters


- **name** (*in path*): string, required

  name of the FlowSchema


- **body**: <a href="{{< ref "../cluster-resources/flow-schema-v1beta1#FlowSchema" >}}">FlowSchema</a>, required

  


- **dryRun** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>


- **fieldManager** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>


- **pretty** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>



#### Response


200 (<a href="{{< ref "../cluster-resources/flow-schema-v1beta1#FlowSchema" >}}">FlowSchema</a>): OK

201 (<a href="{{< ref "../cluster-resources/flow-schema-v1beta1#FlowSchema" >}}">FlowSchema</a>): Created

401: Unauthorized


### `patch` partially update the specified FlowSchema

#### HTTP Request

PATCH /apis/flowcontrol.apiserver.k8s.io/v1beta1/flowschemas/{name}

#### Parameters


- **name** (*in path*): string, required

  name of the FlowSchema


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


200 (<a href="{{< ref "../cluster-resources/flow-schema-v1beta1#FlowSchema" >}}">FlowSchema</a>): OK

201 (<a href="{{< ref "../cluster-resources/flow-schema-v1beta1#FlowSchema" >}}">FlowSchema</a>): Created

401: Unauthorized


### `patch` partially update status of the specified FlowSchema

#### HTTP Request

PATCH /apis/flowcontrol.apiserver.k8s.io/v1beta1/flowschemas/{name}/status

#### Parameters


- **name** (*in path*): string, required

  name of the FlowSchema


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


200 (<a href="{{< ref "../cluster-resources/flow-schema-v1beta1#FlowSchema" >}}">FlowSchema</a>): OK

201 (<a href="{{< ref "../cluster-resources/flow-schema-v1beta1#FlowSchema" >}}">FlowSchema</a>): Created

401: Unauthorized


### `delete` delete a FlowSchema

#### HTTP Request

DELETE /apis/flowcontrol.apiserver.k8s.io/v1beta1/flowschemas/{name}

#### Parameters


- **name** (*in path*): string, required

  name of the FlowSchema


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


### `deletecollection` delete collection of FlowSchema

#### HTTP Request

DELETE /apis/flowcontrol.apiserver.k8s.io/v1beta1/flowschemas

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

