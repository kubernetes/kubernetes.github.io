---
api_metadata:
  apiVersion: "storage.k8s.io/v1"
  import: "k8s.io/api/storage/v1"
  kind: "CSINode"
content_type: "api_reference"
description: "CSINode holds information about all CSI drivers installed on a node."
title: "CSINode"
weight: 9
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

`apiVersion: storage.k8s.io/v1`

`import "k8s.io/api/storage/v1"`


## CSINode {#CSINode}

CSINode holds information about all CSI drivers installed on a node. CSI drivers do not need to create the CSINode object directly. As long as they use the node-driver-registrar sidecar container, the kubelet will automatically populate the CSINode object for the CSI driver as part of kubelet plugin registration. CSINode has the same name as a node. If the object is missing, it means either there are no CSI Drivers available on the node, or the Kubelet version is low enough that it doesn't create this object. CSINode has an OwnerReference that points to the corresponding node object.

<hr>

- **apiVersion**: storage.k8s.io/v1


- **kind**: CSINode


- **metadata** (<a href="{{< ref "../common-definitions/object-meta#ObjectMeta" >}}">ObjectMeta</a>)

  metadata.name must be the Kubernetes node name.

- **spec** (<a href="{{< ref "../config-and-storage-resources/csi-node-v1#CSINodeSpec" >}}">CSINodeSpec</a>), required

  spec is the specification of CSINode





## CSINodeSpec {#CSINodeSpec}

CSINodeSpec holds information about the specification of all CSI drivers installed on a node

<hr>

- **drivers** ([]CSINodeDriver), required

  *Patch strategy: merge on key `name`*
  
  drivers is a list of information of all CSI Drivers existing on a node. If all drivers in the list are uninstalled, this can become empty.

  <a name="CSINodeDriver"></a>
  *CSINodeDriver holds information about the specification of one CSI driver installed on a node*

  - **drivers.name** (string), required

    This is the name of the CSI driver that this object refers to. This MUST be the same name returned by the CSI GetPluginName() call for that driver.

  - **drivers.nodeID** (string), required

    nodeID of the node from the driver point of view. This field enables Kubernetes to communicate with storage systems that do not share the same nomenclature for nodes. For example, Kubernetes may refer to a given node as "node1", but the storage system may refer to the same node as "nodeA". When Kubernetes issues a command to the storage system to attach a volume to a specific node, it can use this field to refer to the node name using the ID that the storage system will understand, e.g. "nodeA" instead of "node1". This field is required.

  - **drivers.allocatable** (VolumeNodeResources)

    allocatable represents the volume resources of a node that are available for scheduling. This field is beta.

    <a name="VolumeNodeResources"></a>
    *VolumeNodeResources is a set of resource limits for scheduling of volumes.*

    - **drivers.allocatable.count** (int32)

      Maximum number of unique volumes managed by the CSI driver that can be used on a node. A volume that is both attached and mounted on a node is considered to be used once, not twice. The same rule applies for a unique volume that is shared among multiple pods on the same node. If this field is not specified, then the supported number of volumes on this node is unbounded.

  - **drivers.topologyKeys** ([]string)

    topologyKeys is the list of keys supported by the driver. When a driver is initialized on a cluster, it provides a set of topology keys that it understands (e.g. "company.com/zone", "company.com/region"). When a driver is initialized on a node, it provides the same topology keys along with values. Kubelet will expose these topology keys as labels on its own node object. When Kubernetes does topology aware provisioning, it can use this list to determine which labels it should retrieve from the node object and pass back to the driver. It is possible for different nodes to use different topology keys. This can be empty if driver does not support topology.





## CSINodeList {#CSINodeList}

CSINodeList is a collection of CSINode objects.

<hr>

- **apiVersion**: storage.k8s.io/v1


- **kind**: CSINodeList


- **metadata** (<a href="{{< ref "../common-definitions/list-meta#ListMeta" >}}">ListMeta</a>)

  Standard list metadata More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

- **items** ([]<a href="{{< ref "../config-and-storage-resources/csi-node-v1#CSINode" >}}">CSINode</a>), required

  items is the list of CSINode





## Operations {#Operations}



<hr>






### `get` read the specified CSINode

#### HTTP Request

GET /apis/storage.k8s.io/v1/csinodes/{name}

#### Parameters


- **name** (*in path*): string, required

  name of the CSINode


- **pretty** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>



#### Response


200 (<a href="{{< ref "../config-and-storage-resources/csi-node-v1#CSINode" >}}">CSINode</a>): OK

401: Unauthorized


### `list` list or watch objects of kind CSINode

#### HTTP Request

GET /apis/storage.k8s.io/v1/csinodes

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


200 (<a href="{{< ref "../config-and-storage-resources/csi-node-v1#CSINodeList" >}}">CSINodeList</a>): OK

401: Unauthorized


### `create` create a CSINode

#### HTTP Request

POST /apis/storage.k8s.io/v1/csinodes

#### Parameters


- **body**: <a href="{{< ref "../config-and-storage-resources/csi-node-v1#CSINode" >}}">CSINode</a>, required

  


- **dryRun** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>


- **fieldManager** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>


- **pretty** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>



#### Response


200 (<a href="{{< ref "../config-and-storage-resources/csi-node-v1#CSINode" >}}">CSINode</a>): OK

201 (<a href="{{< ref "../config-and-storage-resources/csi-node-v1#CSINode" >}}">CSINode</a>): Created

202 (<a href="{{< ref "../config-and-storage-resources/csi-node-v1#CSINode" >}}">CSINode</a>): Accepted

401: Unauthorized


### `update` replace the specified CSINode

#### HTTP Request

PUT /apis/storage.k8s.io/v1/csinodes/{name}

#### Parameters


- **name** (*in path*): string, required

  name of the CSINode


- **body**: <a href="{{< ref "../config-and-storage-resources/csi-node-v1#CSINode" >}}">CSINode</a>, required

  


- **dryRun** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>


- **fieldManager** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>


- **pretty** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>



#### Response


200 (<a href="{{< ref "../config-and-storage-resources/csi-node-v1#CSINode" >}}">CSINode</a>): OK

201 (<a href="{{< ref "../config-and-storage-resources/csi-node-v1#CSINode" >}}">CSINode</a>): Created

401: Unauthorized


### `patch` partially update the specified CSINode

#### HTTP Request

PATCH /apis/storage.k8s.io/v1/csinodes/{name}

#### Parameters


- **name** (*in path*): string, required

  name of the CSINode


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


200 (<a href="{{< ref "../config-and-storage-resources/csi-node-v1#CSINode" >}}">CSINode</a>): OK

201 (<a href="{{< ref "../config-and-storage-resources/csi-node-v1#CSINode" >}}">CSINode</a>): Created

401: Unauthorized


### `delete` delete a CSINode

#### HTTP Request

DELETE /apis/storage.k8s.io/v1/csinodes/{name}

#### Parameters


- **name** (*in path*): string, required

  name of the CSINode


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


200 (<a href="{{< ref "../config-and-storage-resources/csi-node-v1#CSINode" >}}">CSINode</a>): OK

202 (<a href="{{< ref "../config-and-storage-resources/csi-node-v1#CSINode" >}}">CSINode</a>): Accepted

401: Unauthorized


### `deletecollection` delete collection of CSINode

#### HTTP Request

DELETE /apis/storage.k8s.io/v1/csinodes

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

