---
api_metadata:
  apiVersion: "node.k8s.io/v1"
  import: "k8s.io/api/node/v1"
  kind: "RuntimeClass"
content_type: "api_reference"
description: "RuntimeClass defines a class of container runtime supported in the cluster."
title: "RuntimeClass"
weight: 6
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

`apiVersion: node.k8s.io/v1`

`import "k8s.io/api/node/v1"`


## RuntimeClass {#RuntimeClass}

RuntimeClass defines a class of container runtime supported in the cluster. The RuntimeClass is used to determine which container runtime is used to run all containers in a pod. RuntimeClasses are manually defined by a user or cluster provisioner, and referenced in the PodSpec. The Kubelet is responsible for resolving the RuntimeClassName reference before running the pod.  For more details, see https://kubernetes.io/docs/concepts/containers/runtime-class/

<hr>

- **apiVersion**: node.k8s.io/v1


- **kind**: RuntimeClass


- **metadata** (<a href="{{< ref "../common-definitions/object-meta#ObjectMeta" >}}">ObjectMeta</a>)

  More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

- **handler** (string), required

  Handler specifies the underlying runtime and configuration that the CRI implementation will use to handle pods of this class. The possible values are specific to the node & CRI configuration.  It is assumed that all handlers are available on every node, and handlers of the same name are equivalent on every node. For example, a handler called "runc" might specify that the runc OCI runtime (using native Linux containers) will be used to run the containers in a pod. The Handler must be lowercase, conform to the DNS Label (RFC 1123) requirements, and is immutable.

- **overhead** (Overhead)

  Overhead represents the resource overhead associated with running a pod for a given RuntimeClass. For more details, see
   https://kubernetes.io/docs/concepts/scheduling-eviction/pod-overhead/
  This field is in beta starting v1.18 and is only honored by servers that enable the PodOverhead feature.

  <a name="Overhead"></a>
  *Overhead structure represents the resource overhead associated with running a pod.*

  - **overhead.podFixed** (map[string]<a href="{{< ref "../common-definitions/quantity#Quantity" >}}">Quantity</a>)

    PodFixed represents the fixed resource overhead associated with running a pod.

- **scheduling** (Scheduling)

  Scheduling holds the scheduling constraints to ensure that pods running with this RuntimeClass are scheduled to nodes that support it. If scheduling is nil, this RuntimeClass is assumed to be supported by all nodes.

  <a name="Scheduling"></a>
  *Scheduling specifies the scheduling constraints for nodes supporting a RuntimeClass.*

  - **scheduling.nodeSelector** (map[string]string)

    nodeSelector lists labels that must be present on nodes that support this RuntimeClass. Pods using this RuntimeClass can only be scheduled to a node matched by this selector. The RuntimeClass nodeSelector is merged with a pod's existing nodeSelector. Any conflicts will cause the pod to be rejected in admission.

  - **scheduling.tolerations** ([]Toleration)

    *Atomic: will be replaced during a merge*
    
    tolerations are appended (excluding duplicates) to pods running with this RuntimeClass during admission, effectively unioning the set of nodes tolerated by the pod and the RuntimeClass.

    <a name="Toleration"></a>
    *The pod this Toleration is attached to tolerates any taint that matches the triple <key,value,effect> using the matching operator <operator>.*

    - **scheduling.tolerations.key** (string)

      Key is the taint key that the toleration applies to. Empty means match all taint keys. If the key is empty, operator must be Exists; this combination means to match all values and all keys.

    - **scheduling.tolerations.operator** (string)

      Operator represents a key's relationship to the value. Valid operators are Exists and Equal. Defaults to Equal. Exists is equivalent to wildcard for value, so that a pod can tolerate all taints of a particular category.

    - **scheduling.tolerations.value** (string)

      Value is the taint value the toleration matches to. If the operator is Exists, the value should be empty, otherwise just a regular string.

    - **scheduling.tolerations.effect** (string)

      Effect indicates the taint effect to match. Empty means match all taint effects. When specified, allowed values are NoSchedule, PreferNoSchedule and NoExecute.

    - **scheduling.tolerations.tolerationSeconds** (int64)

      TolerationSeconds represents the period of time the toleration (which must be of effect NoExecute, otherwise this field is ignored) tolerates the taint. By default, it is not set, which means tolerate the taint forever (do not evict). Zero and negative values will be treated as 0 (evict immediately) by the system.





## RuntimeClassList {#RuntimeClassList}

RuntimeClassList is a list of RuntimeClass objects.

<hr>

- **apiVersion**: node.k8s.io/v1


- **kind**: RuntimeClassList


- **metadata** (<a href="{{< ref "../common-definitions/list-meta#ListMeta" >}}">ListMeta</a>)

  Standard list metadata. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

- **items** ([]<a href="{{< ref "../cluster-resources/runtime-class-v1#RuntimeClass" >}}">RuntimeClass</a>), required

  Items is a list of schema objects.





## Operations {#Operations}



<hr>






### `get` read the specified RuntimeClass

#### HTTP Request

GET /apis/node.k8s.io/v1/runtimeclasses/{name}

#### Parameters


- **name** (*in path*): string, required

  name of the RuntimeClass


- **pretty** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>



#### Response


200 (<a href="{{< ref "../cluster-resources/runtime-class-v1#RuntimeClass" >}}">RuntimeClass</a>): OK

401: Unauthorized


### `list` list or watch objects of kind RuntimeClass

#### HTTP Request

GET /apis/node.k8s.io/v1/runtimeclasses

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


200 (<a href="{{< ref "../cluster-resources/runtime-class-v1#RuntimeClassList" >}}">RuntimeClassList</a>): OK

401: Unauthorized


### `create` create a RuntimeClass

#### HTTP Request

POST /apis/node.k8s.io/v1/runtimeclasses

#### Parameters


- **body**: <a href="{{< ref "../cluster-resources/runtime-class-v1#RuntimeClass" >}}">RuntimeClass</a>, required

  


- **dryRun** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>


- **fieldManager** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>


- **pretty** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>



#### Response


200 (<a href="{{< ref "../cluster-resources/runtime-class-v1#RuntimeClass" >}}">RuntimeClass</a>): OK

201 (<a href="{{< ref "../cluster-resources/runtime-class-v1#RuntimeClass" >}}">RuntimeClass</a>): Created

202 (<a href="{{< ref "../cluster-resources/runtime-class-v1#RuntimeClass" >}}">RuntimeClass</a>): Accepted

401: Unauthorized


### `update` replace the specified RuntimeClass

#### HTTP Request

PUT /apis/node.k8s.io/v1/runtimeclasses/{name}

#### Parameters


- **name** (*in path*): string, required

  name of the RuntimeClass


- **body**: <a href="{{< ref "../cluster-resources/runtime-class-v1#RuntimeClass" >}}">RuntimeClass</a>, required

  


- **dryRun** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>


- **fieldManager** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>


- **pretty** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>



#### Response


200 (<a href="{{< ref "../cluster-resources/runtime-class-v1#RuntimeClass" >}}">RuntimeClass</a>): OK

201 (<a href="{{< ref "../cluster-resources/runtime-class-v1#RuntimeClass" >}}">RuntimeClass</a>): Created

401: Unauthorized


### `patch` partially update the specified RuntimeClass

#### HTTP Request

PATCH /apis/node.k8s.io/v1/runtimeclasses/{name}

#### Parameters


- **name** (*in path*): string, required

  name of the RuntimeClass


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


200 (<a href="{{< ref "../cluster-resources/runtime-class-v1#RuntimeClass" >}}">RuntimeClass</a>): OK

201 (<a href="{{< ref "../cluster-resources/runtime-class-v1#RuntimeClass" >}}">RuntimeClass</a>): Created

401: Unauthorized


### `delete` delete a RuntimeClass

#### HTTP Request

DELETE /apis/node.k8s.io/v1/runtimeclasses/{name}

#### Parameters


- **name** (*in path*): string, required

  name of the RuntimeClass


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


### `deletecollection` delete collection of RuntimeClass

#### HTTP Request

DELETE /apis/node.k8s.io/v1/runtimeclasses

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

