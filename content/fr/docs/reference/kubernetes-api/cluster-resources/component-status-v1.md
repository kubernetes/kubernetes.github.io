---
api_metadata:
  apiVersion: "v1"
  import: "k8s.io/api/core/v1"
  kind: "ComponentStatus"
content_type: "api_reference"
description: "ComponentStatus (and ComponentStatusList) holds the cluster validation info."
title: "ComponentStatus"
weight: 10
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

`apiVersion: v1`

`import "k8s.io/api/core/v1"`


## ComponentStatus {#ComponentStatus}

ComponentStatus (and ComponentStatusList) holds the cluster validation info. Deprecated: This API is deprecated in v1.19+

<hr>

- **apiVersion**: v1


- **kind**: ComponentStatus


- **metadata** (<a href="{{< ref "../common-definitions/object-meta#ObjectMeta" >}}">ObjectMeta</a>)

  Méta-données d'un objet standard. Plus d'infos : https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

- **conditions** ([]ComponentCondition)

  *Stratégie de patch : merge sur la clé `type`*
  
  List of component conditions observed

  <a name="ComponentCondition"></a>
  *Information about the condition of a component.*

  - **conditions.status** (string), requis

    Status of the condition for a component. Valid values for "Healthy": "True", "False", or "Unknown".

  - **conditions.type** (string), requis

    Type of condition for a component. Valid value: "Healthy"

  - **conditions.error** (string)

    Condition error code for a component. For example, a health check error code.

  - **conditions.message** (string)

    Message about the condition for a component. For example, information about a health check.





## ComponentStatusList {#ComponentStatusList}

Status of all the conditions for the component as a list of ComponentStatus objects. Deprecated: This API is deprecated in v1.19+

<hr>

- **apiVersion**: v1


- **kind**: ComponentStatusList


- **metadata** (<a href="{{< ref "../common-definitions/list-meta#ListMeta" >}}">ListMeta</a>)

  Standard list metadata. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds

- **items** ([]<a href="{{< ref "../cluster-resources/component-status-v1#ComponentStatus" >}}">ComponentStatus</a>), requis

  List of ComponentStatus objects.





## Operations {#Operations}



<hr>






### `get` read the specified ComponentStatus

#### HTTP Request

GET /api/v1/componentstatuses/{name}

#### Parameters


- **name** (*in path*): string, required

  name of the ComponentStatus


- **pretty** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>



#### Response


200 (<a href="{{< ref "../cluster-resources/component-status-v1#ComponentStatus" >}}">ComponentStatus</a>): OK

401: Unauthorized


### `list` list objects of kind ComponentStatus

#### HTTP Request

GET /api/v1/componentstatuses

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


200 (<a href="{{< ref "../cluster-resources/component-status-v1#ComponentStatusList" >}}">ComponentStatusList</a>): OK

401: Unauthorized

