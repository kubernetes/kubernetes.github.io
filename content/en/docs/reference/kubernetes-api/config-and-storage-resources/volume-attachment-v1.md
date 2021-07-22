---
api_metadata:
  apiVersion: "storage.k8s.io/v1"
  import: "k8s.io/api/storage/v1"
  kind: "VolumeAttachment"
content_type: "api_reference"
description: "VolumeAttachment captures the intent to attach or detach the specified volume to/from the specified node."
title: "VolumeAttachment"
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

`apiVersion: storage.k8s.io/v1`

`import "k8s.io/api/storage/v1"`


## VolumeAttachment {#VolumeAttachment}

VolumeAttachment captures the intent to attach or detach the specified volume to/from the specified node.

VolumeAttachment objects are non-namespaced.

<hr>

- **apiVersion**: storage.k8s.io/v1


- **kind**: VolumeAttachment


- **metadata** (<a href="{{< ref "../common-definitions/object-meta#ObjectMeta" >}}">ObjectMeta</a>)

  Standard object metadata. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

- **spec** (<a href="{{< ref "../config-and-storage-resources/volume-attachment-v1#VolumeAttachmentSpec" >}}">VolumeAttachmentSpec</a>), required

  Specification of the desired attach/detach volume behavior. Populated by the Kubernetes system.

- **status** (<a href="{{< ref "../config-and-storage-resources/volume-attachment-v1#VolumeAttachmentStatus" >}}">VolumeAttachmentStatus</a>)

  Status of the VolumeAttachment request. Populated by the entity completing the attach or detach operation, i.e. the external-attacher.





## VolumeAttachmentSpec {#VolumeAttachmentSpec}

VolumeAttachmentSpec is the specification of a VolumeAttachment request.

<hr>

- **attacher** (string), required

  Attacher indicates the name of the volume driver that MUST handle this request. This is the name returned by GetPluginName().

- **nodeName** (string), required

  The node that the volume should be attached to.

- **source** (VolumeAttachmentSource), required

  Source represents the volume that should be attached.

  <a name="VolumeAttachmentSource"></a>
  *VolumeAttachmentSource represents a volume that should be attached. Right now only PersistenVolumes can be attached via external attacher, in future we may allow also inline volumes in pods. Exactly one member can be set.*

  - **source.inlineVolumeSpec** (<a href="{{< ref "../config-and-storage-resources/persistent-volume-v1#PersistentVolumeSpec" >}}">PersistentVolumeSpec</a>)

    inlineVolumeSpec contains all the information necessary to attach a persistent volume defined by a pod's inline VolumeSource. This field is populated only for the CSIMigration feature. It contains translated fields from a pod's inline VolumeSource to a PersistentVolumeSpec. This field is beta-level and is only honored by servers that enabled the CSIMigration feature.

  - **source.persistentVolumeName** (string)

    Name of the persistent volume to attach.





## VolumeAttachmentStatus {#VolumeAttachmentStatus}

VolumeAttachmentStatus is the status of a VolumeAttachment request.

<hr>

- **attached** (boolean), required

  Indicates the volume is successfully attached. This field must only be set by the entity completing the attach operation, i.e. the external-attacher.

- **attachError** (VolumeError)

  The last error encountered during attach operation, if any. This field must only be set by the entity completing the attach operation, i.e. the external-attacher.

  <a name="VolumeError"></a>
  *VolumeError captures an error encountered during a volume operation.*

  - **attachError.message** (string)

    String detailing the error encountered during Attach or Detach operation. This string may be logged, so it should not contain sensitive information.

  - **attachError.time** (Time)

    Time the error was encountered.

    <a name="Time"></a>
    *Time is a wrapper around time.Time which supports correct marshaling to YAML and JSON.  Wrappers are provided for many of the factory methods that the time package offers.*

- **attachmentMetadata** (map[string]string)

  Upon successful attach, this field is populated with any information returned by the attach operation that must be passed into subsequent WaitForAttach or Mount calls. This field must only be set by the entity completing the attach operation, i.e. the external-attacher.

- **detachError** (VolumeError)

  The last error encountered during detach operation, if any. This field must only be set by the entity completing the detach operation, i.e. the external-attacher.

  <a name="VolumeError"></a>
  *VolumeError captures an error encountered during a volume operation.*

  - **detachError.message** (string)

    String detailing the error encountered during Attach or Detach operation. This string may be logged, so it should not contain sensitive information.

  - **detachError.time** (Time)

    Time the error was encountered.

    <a name="Time"></a>
    *Time is a wrapper around time.Time which supports correct marshaling to YAML and JSON.  Wrappers are provided for many of the factory methods that the time package offers.*





## VolumeAttachmentList {#VolumeAttachmentList}

VolumeAttachmentList is a collection of VolumeAttachment objects.

<hr>

- **apiVersion**: storage.k8s.io/v1


- **kind**: VolumeAttachmentList


- **metadata** (<a href="{{< ref "../common-definitions/list-meta#ListMeta" >}}">ListMeta</a>)

  Standard list metadata More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

- **items** ([]<a href="{{< ref "../config-and-storage-resources/volume-attachment-v1#VolumeAttachment" >}}">VolumeAttachment</a>), required

  Items is the list of VolumeAttachments





## Operations {#Operations}



<hr>






### `get` read the specified VolumeAttachment

#### HTTP Request

GET /apis/storage.k8s.io/v1/volumeattachments/{name}

#### Parameters


- **name** (*in path*): string, required

  name of the VolumeAttachment


- **pretty** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>



#### Response


200 (<a href="{{< ref "../config-and-storage-resources/volume-attachment-v1#VolumeAttachment" >}}">VolumeAttachment</a>): OK

401: Unauthorized


### `get` read status of the specified VolumeAttachment

#### HTTP Request

GET /apis/storage.k8s.io/v1/volumeattachments/{name}/status

#### Parameters


- **name** (*in path*): string, required

  name of the VolumeAttachment


- **pretty** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>



#### Response


200 (<a href="{{< ref "../config-and-storage-resources/volume-attachment-v1#VolumeAttachment" >}}">VolumeAttachment</a>): OK

401: Unauthorized


### `list` list or watch objects of kind VolumeAttachment

#### HTTP Request

GET /apis/storage.k8s.io/v1/volumeattachments

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


200 (<a href="{{< ref "../config-and-storage-resources/volume-attachment-v1#VolumeAttachmentList" >}}">VolumeAttachmentList</a>): OK

401: Unauthorized


### `create` create a VolumeAttachment

#### HTTP Request

POST /apis/storage.k8s.io/v1/volumeattachments

#### Parameters


- **body**: <a href="{{< ref "../config-and-storage-resources/volume-attachment-v1#VolumeAttachment" >}}">VolumeAttachment</a>, required

  


- **dryRun** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>


- **fieldManager** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>


- **pretty** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>



#### Response


200 (<a href="{{< ref "../config-and-storage-resources/volume-attachment-v1#VolumeAttachment" >}}">VolumeAttachment</a>): OK

201 (<a href="{{< ref "../config-and-storage-resources/volume-attachment-v1#VolumeAttachment" >}}">VolumeAttachment</a>): Created

202 (<a href="{{< ref "../config-and-storage-resources/volume-attachment-v1#VolumeAttachment" >}}">VolumeAttachment</a>): Accepted

401: Unauthorized


### `update` replace the specified VolumeAttachment

#### HTTP Request

PUT /apis/storage.k8s.io/v1/volumeattachments/{name}

#### Parameters


- **name** (*in path*): string, required

  name of the VolumeAttachment


- **body**: <a href="{{< ref "../config-and-storage-resources/volume-attachment-v1#VolumeAttachment" >}}">VolumeAttachment</a>, required

  


- **dryRun** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>


- **fieldManager** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>


- **pretty** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>



#### Response


200 (<a href="{{< ref "../config-and-storage-resources/volume-attachment-v1#VolumeAttachment" >}}">VolumeAttachment</a>): OK

201 (<a href="{{< ref "../config-and-storage-resources/volume-attachment-v1#VolumeAttachment" >}}">VolumeAttachment</a>): Created

401: Unauthorized


### `update` replace status of the specified VolumeAttachment

#### HTTP Request

PUT /apis/storage.k8s.io/v1/volumeattachments/{name}/status

#### Parameters


- **name** (*in path*): string, required

  name of the VolumeAttachment


- **body**: <a href="{{< ref "../config-and-storage-resources/volume-attachment-v1#VolumeAttachment" >}}">VolumeAttachment</a>, required

  


- **dryRun** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>


- **fieldManager** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>


- **pretty** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>



#### Response


200 (<a href="{{< ref "../config-and-storage-resources/volume-attachment-v1#VolumeAttachment" >}}">VolumeAttachment</a>): OK

201 (<a href="{{< ref "../config-and-storage-resources/volume-attachment-v1#VolumeAttachment" >}}">VolumeAttachment</a>): Created

401: Unauthorized


### `patch` partially update the specified VolumeAttachment

#### HTTP Request

PATCH /apis/storage.k8s.io/v1/volumeattachments/{name}

#### Parameters


- **name** (*in path*): string, required

  name of the VolumeAttachment


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


200 (<a href="{{< ref "../config-and-storage-resources/volume-attachment-v1#VolumeAttachment" >}}">VolumeAttachment</a>): OK

201 (<a href="{{< ref "../config-and-storage-resources/volume-attachment-v1#VolumeAttachment" >}}">VolumeAttachment</a>): Created

401: Unauthorized


### `patch` partially update status of the specified VolumeAttachment

#### HTTP Request

PATCH /apis/storage.k8s.io/v1/volumeattachments/{name}/status

#### Parameters


- **name** (*in path*): string, required

  name of the VolumeAttachment


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


200 (<a href="{{< ref "../config-and-storage-resources/volume-attachment-v1#VolumeAttachment" >}}">VolumeAttachment</a>): OK

201 (<a href="{{< ref "../config-and-storage-resources/volume-attachment-v1#VolumeAttachment" >}}">VolumeAttachment</a>): Created

401: Unauthorized


### `delete` delete a VolumeAttachment

#### HTTP Request

DELETE /apis/storage.k8s.io/v1/volumeattachments/{name}

#### Parameters


- **name** (*in path*): string, required

  name of the VolumeAttachment


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


200 (<a href="{{< ref "../config-and-storage-resources/volume-attachment-v1#VolumeAttachment" >}}">VolumeAttachment</a>): OK

202 (<a href="{{< ref "../config-and-storage-resources/volume-attachment-v1#VolumeAttachment" >}}">VolumeAttachment</a>): Accepted

401: Unauthorized


### `deletecollection` delete collection of VolumeAttachment

#### HTTP Request

DELETE /apis/storage.k8s.io/v1/volumeattachments

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

