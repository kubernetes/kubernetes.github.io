---
api_metadata:
  apiVersion: "storage.k8s.io/v1"
  import: "k8s.io/api/storage/v1"
  kind: "CSIDriver"
content_type: "api_reference"
description: "CSIDriver captures information about a Container Storage Interface (CSI) volume driver deployed on the cluster."
title: "CSIDriver"
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

`apiVersion: storage.k8s.io/v1`

`import "k8s.io/api/storage/v1"`


## CSIDriver {#CSIDriver}

CSIDriver captures information about a Container Storage Interface (CSI) volume driver deployed on the cluster. Kubernetes attach detach controller uses this object to determine whether attach is required. Kubelet uses this object to determine whether pod information needs to be passed on mount. CSIDriver objects are non-namespaced.

<hr>

- **apiVersion**: storage.k8s.io/v1


- **kind**: CSIDriver


- **metadata** (<a href="{{< ref "../common-definitions/object-meta#ObjectMeta" >}}">ObjectMeta</a>)

  Standard object metadata. metadata.Name indicates the name of the CSI driver that this object refers to; it MUST be the same name returned by the CSI GetPluginName() call for that driver. The driver name must be 63 characters or less, beginning and ending with an alphanumeric character ([a-z0-9A-Z]) with dashes (-), dots (.), and alphanumerics between. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

- **spec** (<a href="{{< ref "../config-and-storage-resources/csi-driver-v1#CSIDriverSpec" >}}">CSIDriverSpec</a>), required

  Specification of the CSI Driver.





## CSIDriverSpec {#CSIDriverSpec}

CSIDriverSpec is the specification of a CSIDriver.

<hr>

- **attachRequired** (boolean)

  attachRequired indicates this CSI volume driver requires an attach operation (because it implements the CSI ControllerPublishVolume() method), and that the Kubernetes attach detach controller should call the attach volume interface which checks the volumeattachment status and waits until the volume is attached before proceeding to mounting. The CSI external-attacher coordinates with CSI volume driver and updates the volumeattachment status when the attach operation is complete. If the CSIDriverRegistry feature gate is enabled and the value is specified to false, the attach operation will be skipped. Otherwise the attach operation will be called.
  
  This field is immutable.

- **fsGroupPolicy** (string)

  Defines if the underlying volume supports changing ownership and permission of the volume before being mounted. Refer to the specific FSGroupPolicy values for additional details. This field is beta, and is only honored by servers that enable the CSIVolumeFSGroupPolicy feature gate.
  
  This field is immutable.
  
  Defaults to ReadWriteOnceWithFSType, which will examine each volume to determine if Kubernetes should modify ownership and permissions of the volume. With the default policy the defined fsGroup will only be applied if a fstype is defined and the volume's access mode contains ReadWriteOnce.

- **podInfoOnMount** (boolean)

  If set to true, podInfoOnMount indicates this CSI volume driver requires additional pod information (like podName, podUID, etc.) during mount operations. If set to false, pod information will not be passed on mount. Default is false. The CSI driver specifies podInfoOnMount as part of driver deployment. If true, Kubelet will pass pod information as VolumeContext in the CSI NodePublishVolume() calls. The CSI driver is responsible for parsing and validating the information passed in as VolumeContext. The following VolumeConext will be passed if podInfoOnMount is set to true. This list might grow, but the prefix will be used. "csi.storage.k8s.io/pod.name": pod.Name "csi.storage.k8s.io/pod.namespace": pod.Namespace "csi.storage.k8s.io/pod.uid": string(pod.UID) "csi.storage.k8s.io/ephemeral": "true" if the volume is an ephemeral inline volume
                                  defined by a CSIVolumeSource, otherwise "false"
  
  "csi.storage.k8s.io/ephemeral" is a new feature in Kubernetes 1.16. It is only required for drivers which support both the "Persistent" and "Ephemeral" VolumeLifecycleMode. Other drivers can leave pod info disabled and/or ignore this field. As Kubernetes 1.15 doesn't support this field, drivers can only support one mode when deployed on such a cluster and the deployment determines which mode that is, for example via a command line parameter of the driver.
  
  This field is immutable.

- **requiresRepublish** (boolean)

  RequiresRepublish indicates the CSI driver wants `NodePublishVolume` being periodically called to reflect any possible change in the mounted volume. This field defaults to false.
  
  Note: After a successful initial NodePublishVolume call, subsequent calls to NodePublishVolume should only update the contents of the volume. New mount points will not be seen by a running container.

- **storageCapacity** (boolean)

  If set to true, storageCapacity indicates that the CSI volume driver wants pod scheduling to consider the storage capacity that the driver deployment will report by creating CSIStorageCapacity objects with capacity information.
  
  The check can be enabled immediately when deploying a driver. In that case, provisioning new volumes with late binding will pause until the driver deployment has published some suitable CSIStorageCapacity object.
  
  Alternatively, the driver can be deployed with the field unset or false and it can be flipped later when storage capacity information has been published.
  
  This field is immutable.
  
  This is a beta field and only available when the CSIStorageCapacity feature is enabled. The default is false.

- **tokenRequests** ([]TokenRequest)

  *Atomic: will be replaced during a merge*
  
  TokenRequests indicates the CSI driver needs pods' service account tokens it is mounting volume for to do necessary authentication. Kubelet will pass the tokens in VolumeContext in the CSI NodePublishVolume calls. The CSI driver should parse and validate the following VolumeContext: "csi.storage.k8s.io/serviceAccount.tokens": {
    "\<audience>": {
      "token": \<token>,
      "expirationTimestamp": \<expiration timestamp in RFC3339>,
    },
    ...
  }
  
  Note: Audience in each TokenRequest should be different and at most one token is empty string. To receive a new token after expiry, RequiresRepublish can be used to trigger NodePublishVolume periodically.

  <a name="TokenRequest"></a>
  *TokenRequest contains parameters of a service account token.*

  - **tokenRequests.audience** (string), required

    Audience is the intended audience of the token in "TokenRequestSpec". It will default to the audiences of kube apiserver.

  - **tokenRequests.expirationSeconds** (int64)

    ExpirationSeconds is the duration of validity of the token in "TokenRequestSpec". It has the same default value of "ExpirationSeconds" in "TokenRequestSpec".

- **volumeLifecycleModes** ([]string)

  *Set: unique values will be kept during a merge*
  
  volumeLifecycleModes defines what kind of volumes this CSI volume driver supports. The default if the list is empty is "Persistent", which is the usage defined by the CSI specification and implemented in Kubernetes via the usual PV/PVC mechanism. The other mode is "Ephemeral". In this mode, volumes are defined inline inside the pod spec with CSIVolumeSource and their lifecycle is tied to the lifecycle of that pod. A driver has to be aware of this because it is only going to get a NodePublishVolume call for such a volume. For more information about implementing this mode, see https://kubernetes-csi.github.io/docs/ephemeral-local-volumes.html A driver can support one or more of these modes and more modes may be added in the future. This field is beta.
  
  This field is immutable.





## CSIDriverList {#CSIDriverList}

CSIDriverList is a collection of CSIDriver objects.

<hr>

- **apiVersion**: storage.k8s.io/v1


- **kind**: CSIDriverList


- **metadata** (<a href="{{< ref "../common-definitions/list-meta#ListMeta" >}}">ListMeta</a>)

  Standard list metadata More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

- **items** ([]<a href="{{< ref "../config-and-storage-resources/csi-driver-v1#CSIDriver" >}}">CSIDriver</a>), required

  items is the list of CSIDriver





## Operations {#Operations}



<hr>






### `get` read the specified CSIDriver

#### HTTP Request

GET /apis/storage.k8s.io/v1/csidrivers/{name}

#### Parameters


- **name** (*in path*): string, required

  name of the CSIDriver


- **pretty** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>



#### Response


200 (<a href="{{< ref "../config-and-storage-resources/csi-driver-v1#CSIDriver" >}}">CSIDriver</a>): OK

401: Unauthorized


### `list` list or watch objects of kind CSIDriver

#### HTTP Request

GET /apis/storage.k8s.io/v1/csidrivers

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


200 (<a href="{{< ref "../config-and-storage-resources/csi-driver-v1#CSIDriverList" >}}">CSIDriverList</a>): OK

401: Unauthorized


### `create` create a CSIDriver

#### HTTP Request

POST /apis/storage.k8s.io/v1/csidrivers

#### Parameters


- **body**: <a href="{{< ref "../config-and-storage-resources/csi-driver-v1#CSIDriver" >}}">CSIDriver</a>, required

  


- **dryRun** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>


- **fieldManager** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>


- **pretty** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>



#### Response


200 (<a href="{{< ref "../config-and-storage-resources/csi-driver-v1#CSIDriver" >}}">CSIDriver</a>): OK

201 (<a href="{{< ref "../config-and-storage-resources/csi-driver-v1#CSIDriver" >}}">CSIDriver</a>): Created

202 (<a href="{{< ref "../config-and-storage-resources/csi-driver-v1#CSIDriver" >}}">CSIDriver</a>): Accepted

401: Unauthorized


### `update` replace the specified CSIDriver

#### HTTP Request

PUT /apis/storage.k8s.io/v1/csidrivers/{name}

#### Parameters


- **name** (*in path*): string, required

  name of the CSIDriver


- **body**: <a href="{{< ref "../config-and-storage-resources/csi-driver-v1#CSIDriver" >}}">CSIDriver</a>, required

  


- **dryRun** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>


- **fieldManager** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>


- **pretty** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>



#### Response


200 (<a href="{{< ref "../config-and-storage-resources/csi-driver-v1#CSIDriver" >}}">CSIDriver</a>): OK

201 (<a href="{{< ref "../config-and-storage-resources/csi-driver-v1#CSIDriver" >}}">CSIDriver</a>): Created

401: Unauthorized


### `patch` partially update the specified CSIDriver

#### HTTP Request

PATCH /apis/storage.k8s.io/v1/csidrivers/{name}

#### Parameters


- **name** (*in path*): string, required

  name of the CSIDriver


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


200 (<a href="{{< ref "../config-and-storage-resources/csi-driver-v1#CSIDriver" >}}">CSIDriver</a>): OK

201 (<a href="{{< ref "../config-and-storage-resources/csi-driver-v1#CSIDriver" >}}">CSIDriver</a>): Created

401: Unauthorized


### `delete` delete a CSIDriver

#### HTTP Request

DELETE /apis/storage.k8s.io/v1/csidrivers/{name}

#### Parameters


- **name** (*in path*): string, required

  name of the CSIDriver


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


200 (<a href="{{< ref "../config-and-storage-resources/csi-driver-v1#CSIDriver" >}}">CSIDriver</a>): OK

202 (<a href="{{< ref "../config-and-storage-resources/csi-driver-v1#CSIDriver" >}}">CSIDriver</a>): Accepted

401: Unauthorized


### `deletecollection` delete collection of CSIDriver

#### HTTP Request

DELETE /apis/storage.k8s.io/v1/csidrivers

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

