---
api_metadata:
  apiVersion: "v1"
  import: "k8s.io/api/core/v1"
  kind: "Node"
content_type: "api_reference"
description: "Node is a worker node in Kubernetes."
title: "Node"
weight: 1
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


## Node {#Node}

Node is a worker node in Kubernetes. Each node will have a unique identifier in the cache (i.e. in etcd).

<hr>

- **apiVersion**: v1


- **kind**: Node


- **metadata** (<a href="{{< ref "../common-definitions/object-meta#ObjectMeta" >}}">ObjectMeta</a>)

  Standard object's metadata. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

- **spec** (<a href="{{< ref "../cluster-resources/node-v1#NodeSpec" >}}">NodeSpec</a>)

  Spec defines the behavior of a node. https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status

- **status** (<a href="{{< ref "../cluster-resources/node-v1#NodeStatus" >}}">NodeStatus</a>)

  Most recently observed status of the node. Populated by the system. Read-only. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status





## NodeSpec {#NodeSpec}

NodeSpec describes the attributes that a node is created with.

<hr>

- **configSource** (NodeConfigSource)

  Deprecated. If specified, the source of the node's configuration. The DynamicKubeletConfig feature gate must be enabled for the Kubelet to use this field. This field is deprecated as of 1.22: https://git.k8s.io/enhancements/keps/sig-node/281-dynamic-kubelet-configuration

  <a name="NodeConfigSource"></a>
  *NodeConfigSource specifies a source of node configuration. Exactly one subfield (excluding metadata) must be non-nil. This API is deprecated since 1.22*

  - **configSource.configMap** (ConfigMapNodeConfigSource)

    ConfigMap is a reference to a Node's ConfigMap

    <a name="ConfigMapNodeConfigSource"></a>
    *ConfigMapNodeConfigSource contains the information to reference a ConfigMap as a config source for the Node. This API is deprecated since 1.22: https://git.k8s.io/enhancements/keps/sig-node/281-dynamic-kubelet-configuration*

    - **configSource.configMap.kubeletConfigKey** (string), required

      KubeletConfigKey declares which key of the referenced ConfigMap corresponds to the KubeletConfiguration structure This field is required in all cases.

    - **configSource.configMap.name** (string), required

      Name is the metadata.name of the referenced ConfigMap. This field is required in all cases.

    - **configSource.configMap.namespace** (string), required

      Namespace is the metadata.namespace of the referenced ConfigMap. This field is required in all cases.

    - **configSource.configMap.resourceVersion** (string)

      ResourceVersion is the metadata.ResourceVersion of the referenced ConfigMap. This field is forbidden in Node.Spec, and required in Node.Status.

    - **configSource.configMap.uid** (string)

      UID is the metadata.UID of the referenced ConfigMap. This field is forbidden in Node.Spec, and required in Node.Status.

- **externalID** (string)

  Deprecated. Not all kubelets will set this field. Remove field after 1.13. see: https://issues.k8s.io/61966

- **podCIDR** (string)

  PodCIDR represents the pod IP range assigned to the node.

- **podCIDRs** ([]string)

  podCIDRs represents the IP ranges assigned to the node for usage by Pods on that node. If this field is specified, the 0th entry must match the podCIDR field. It may contain at most 1 value for each of IPv4 and IPv6.

- **providerID** (string)

  ID of the node assigned by the cloud provider in the format: \<ProviderName>://\<ProviderSpecificNodeID>

- **taints** ([]Taint)

  If specified, the node's taints.

  <a name="Taint"></a>
  *The node this Taint is attached to has the "effect" on any pod that does not tolerate the Taint.*

  - **taints.effect** (string), required

    Required. The effect of the taint on pods that do not tolerate the taint. Valid effects are NoSchedule, PreferNoSchedule and NoExecute.

  - **taints.key** (string), required

    Required. The taint key to be applied to a node.

  - **taints.timeAdded** (Time)

    TimeAdded represents the time at which the taint was added. It is only written for NoExecute taints.

    <a name="Time"></a>
    *Time is a wrapper around time.Time which supports correct marshaling to YAML and JSON.  Wrappers are provided for many of the factory methods that the time package offers.*

  - **taints.value** (string)

    The taint value corresponding to the taint key.

- **unschedulable** (boolean)

  Unschedulable controls node schedulability of new pods. By default, node is schedulable. More info: https://kubernetes.io/docs/concepts/nodes/node/#manual-node-administration





## NodeStatus {#NodeStatus}

NodeStatus is information about the current status of a node.

<hr>

- **addresses** ([]NodeAddress)

  *Patch strategy: merge on key `type`*
  
  List of addresses reachable to the node. Queried from cloud provider, if available. More info: https://kubernetes.io/docs/concepts/nodes/node/#addresses Note: This field is declared as mergeable, but the merge key is not sufficiently unique, which can cause data corruption when it is merged. Callers should instead use a full-replacement patch. See http://pr.k8s.io/79391 for an example.

  <a name="NodeAddress"></a>
  *NodeAddress contains information for the node's address.*

  - **addresses.address** (string), required

    The node address.

  - **addresses.type** (string), required

    Node address type, one of Hostname, ExternalIP or InternalIP.

- **allocatable** (map[string]<a href="{{< ref "../common-definitions/quantity#Quantity" >}}">Quantity</a>)

  Allocatable represents the resources of a node that are available for scheduling. Defaults to Capacity.

- **capacity** (map[string]<a href="{{< ref "../common-definitions/quantity#Quantity" >}}">Quantity</a>)

  Capacity represents the total resources of a node. More info: https://kubernetes.io/docs/concepts/storage/persistent-volumes#capacity

- **conditions** ([]NodeCondition)

  *Patch strategy: merge on key `type`*
  
  Conditions is an array of current observed node conditions. More info: https://kubernetes.io/docs/concepts/nodes/node/#condition

  <a name="NodeCondition"></a>
  *NodeCondition contains condition information for a node.*

  - **conditions.status** (string), required

    Status of the condition, one of True, False, Unknown.

  - **conditions.type** (string), required

    Type of node condition.

  - **conditions.lastHeartbeatTime** (Time)

    Last time we got an update on a given condition.

    <a name="Time"></a>
    *Time is a wrapper around time.Time which supports correct marshaling to YAML and JSON.  Wrappers are provided for many of the factory methods that the time package offers.*

  - **conditions.lastTransitionTime** (Time)

    Last time the condition transit from one status to another.

    <a name="Time"></a>
    *Time is a wrapper around time.Time which supports correct marshaling to YAML and JSON.  Wrappers are provided for many of the factory methods that the time package offers.*

  - **conditions.message** (string)

    Human readable message indicating details about last transition.

  - **conditions.reason** (string)

    (brief) reason for the condition's last transition.

- **config** (NodeConfigStatus)

  Status of the config assigned to the node via the dynamic Kubelet config feature.

  <a name="NodeConfigStatus"></a>
  *NodeConfigStatus describes the status of the config assigned by Node.Spec.ConfigSource.*

  - **config.active** (NodeConfigSource)

    Active reports the checkpointed config the node is actively using. Active will represent either the current version of the Assigned config, or the current LastKnownGood config, depending on whether attempting to use the Assigned config results in an error.

    <a name="NodeConfigSource"></a>
    *NodeConfigSource specifies a source of node configuration. Exactly one subfield (excluding metadata) must be non-nil. This API is deprecated since 1.22*

    - **config.active.configMap** (ConfigMapNodeConfigSource)

      ConfigMap is a reference to a Node's ConfigMap

      <a name="ConfigMapNodeConfigSource"></a>
      *ConfigMapNodeConfigSource contains the information to reference a ConfigMap as a config source for the Node. This API is deprecated since 1.22: https://git.k8s.io/enhancements/keps/sig-node/281-dynamic-kubelet-configuration*

      - **config.active.configMap.kubeletConfigKey** (string), required

        KubeletConfigKey declares which key of the referenced ConfigMap corresponds to the KubeletConfiguration structure This field is required in all cases.

      - **config.active.configMap.name** (string), required

        Name is the metadata.name of the referenced ConfigMap. This field is required in all cases.

      - **config.active.configMap.namespace** (string), required

        Namespace is the metadata.namespace of the referenced ConfigMap. This field is required in all cases.

      - **config.active.configMap.resourceVersion** (string)

        ResourceVersion is the metadata.ResourceVersion of the referenced ConfigMap. This field is forbidden in Node.Spec, and required in Node.Status.

      - **config.active.configMap.uid** (string)

        UID is the metadata.UID of the referenced ConfigMap. This field is forbidden in Node.Spec, and required in Node.Status.

  - **config.assigned** (NodeConfigSource)

    Assigned reports the checkpointed config the node will try to use. When Node.Spec.ConfigSource is updated, the node checkpoints the associated config payload to local disk, along with a record indicating intended config. The node refers to this record to choose its config checkpoint, and reports this record in Assigned. Assigned only updates in the status after the record has been checkpointed to disk. When the Kubelet is restarted, it tries to make the Assigned config the Active config by loading and validating the checkpointed payload identified by Assigned.

    <a name="NodeConfigSource"></a>
    *NodeConfigSource specifies a source of node configuration. Exactly one subfield (excluding metadata) must be non-nil. This API is deprecated since 1.22*

    - **config.assigned.configMap** (ConfigMapNodeConfigSource)

      ConfigMap is a reference to a Node's ConfigMap

      <a name="ConfigMapNodeConfigSource"></a>
      *ConfigMapNodeConfigSource contains the information to reference a ConfigMap as a config source for the Node. This API is deprecated since 1.22: https://git.k8s.io/enhancements/keps/sig-node/281-dynamic-kubelet-configuration*

      - **config.assigned.configMap.kubeletConfigKey** (string), required

        KubeletConfigKey declares which key of the referenced ConfigMap corresponds to the KubeletConfiguration structure This field is required in all cases.

      - **config.assigned.configMap.name** (string), required

        Name is the metadata.name of the referenced ConfigMap. This field is required in all cases.

      - **config.assigned.configMap.namespace** (string), required

        Namespace is the metadata.namespace of the referenced ConfigMap. This field is required in all cases.

      - **config.assigned.configMap.resourceVersion** (string)

        ResourceVersion is the metadata.ResourceVersion of the referenced ConfigMap. This field is forbidden in Node.Spec, and required in Node.Status.

      - **config.assigned.configMap.uid** (string)

        UID is the metadata.UID of the referenced ConfigMap. This field is forbidden in Node.Spec, and required in Node.Status.

  - **config.error** (string)

    Error describes any problems reconciling the Spec.ConfigSource to the Active config. Errors may occur, for example, attempting to checkpoint Spec.ConfigSource to the local Assigned record, attempting to checkpoint the payload associated with Spec.ConfigSource, attempting to load or validate the Assigned config, etc. Errors may occur at different points while syncing config. Earlier errors (e.g. download or checkpointing errors) will not result in a rollback to LastKnownGood, and may resolve across Kubelet retries. Later errors (e.g. loading or validating a checkpointed config) will result in a rollback to LastKnownGood. In the latter case, it is usually possible to resolve the error by fixing the config assigned in Spec.ConfigSource. You can find additional information for debugging by searching the error message in the Kubelet log. Error is a human-readable description of the error state; machines can check whether or not Error is empty, but should not rely on the stability of the Error text across Kubelet versions.

  - **config.lastKnownGood** (NodeConfigSource)

    LastKnownGood reports the checkpointed config the node will fall back to when it encounters an error attempting to use the Assigned config. The Assigned config becomes the LastKnownGood config when the node determines that the Assigned config is stable and correct. This is currently implemented as a 10-minute soak period starting when the local record of Assigned config is updated. If the Assigned config is Active at the end of this period, it becomes the LastKnownGood. Note that if Spec.ConfigSource is reset to nil (use local defaults), the LastKnownGood is also immediately reset to nil, because the local default config is always assumed good. You should not make assumptions about the node's method of determining config stability and correctness, as this may change or become configurable in the future.

    <a name="NodeConfigSource"></a>
    *NodeConfigSource specifies a source of node configuration. Exactly one subfield (excluding metadata) must be non-nil. This API is deprecated since 1.22*

    - **config.lastKnownGood.configMap** (ConfigMapNodeConfigSource)

      ConfigMap is a reference to a Node's ConfigMap

      <a name="ConfigMapNodeConfigSource"></a>
      *ConfigMapNodeConfigSource contains the information to reference a ConfigMap as a config source for the Node. This API is deprecated since 1.22: https://git.k8s.io/enhancements/keps/sig-node/281-dynamic-kubelet-configuration*

      - **config.lastKnownGood.configMap.kubeletConfigKey** (string), required

        KubeletConfigKey declares which key of the referenced ConfigMap corresponds to the KubeletConfiguration structure This field is required in all cases.

      - **config.lastKnownGood.configMap.name** (string), required

        Name is the metadata.name of the referenced ConfigMap. This field is required in all cases.

      - **config.lastKnownGood.configMap.namespace** (string), required

        Namespace is the metadata.namespace of the referenced ConfigMap. This field is required in all cases.

      - **config.lastKnownGood.configMap.resourceVersion** (string)

        ResourceVersion is the metadata.ResourceVersion of the referenced ConfigMap. This field is forbidden in Node.Spec, and required in Node.Status.

      - **config.lastKnownGood.configMap.uid** (string)

        UID is the metadata.UID of the referenced ConfigMap. This field is forbidden in Node.Spec, and required in Node.Status.

- **daemonEndpoints** (NodeDaemonEndpoints)

  Endpoints of daemons running on the Node.

  <a name="NodeDaemonEndpoints"></a>
  *NodeDaemonEndpoints lists ports opened by daemons running on the Node.*

  - **daemonEndpoints.kubeletEndpoint** (DaemonEndpoint)

    Endpoint on which Kubelet is listening.

    <a name="DaemonEndpoint"></a>
    *DaemonEndpoint contains information about a single Daemon endpoint.*

    - **daemonEndpoints.kubeletEndpoint.Port** (int32), required

      Port number of the given endpoint.

- **images** ([]ContainerImage)

  List of container images on this node

  <a name="ContainerImage"></a>
  *Describe a container image*

  - **images.names** ([]string)

    Names by which this image is known. e.g. ["k8s.gcr.io/hyperkube:v1.0.7", "dockerhub.io/google_containers/hyperkube:v1.0.7"]

  - **images.sizeBytes** (int64)

    The size of the image in bytes.

- **nodeInfo** (NodeSystemInfo)

  Set of ids/uuids to uniquely identify the node. More info: https://kubernetes.io/docs/concepts/nodes/node/#info

  <a name="NodeSystemInfo"></a>
  *NodeSystemInfo is a set of ids/uuids to uniquely identify the node.*

  - **nodeInfo.architecture** (string), required

    The Architecture reported by the node

  - **nodeInfo.bootID** (string), required

    Boot ID reported by the node.

  - **nodeInfo.containerRuntimeVersion** (string), required

    ContainerRuntime Version reported by the node through runtime remote API (e.g. docker://1.5.0).

  - **nodeInfo.kernelVersion** (string), required

    Kernel Version reported by the node from 'uname -r' (e.g. 3.16.0-0.bpo.4-amd64).

  - **nodeInfo.kubeProxyVersion** (string), required

    KubeProxy Version reported by the node.

  - **nodeInfo.kubeletVersion** (string), required

    Kubelet Version reported by the node.

  - **nodeInfo.machineID** (string), required

    MachineID reported by the node. For unique machine identification in the cluster this field is preferred. Learn more from man(5) machine-id: http://man7.org/linux/man-pages/man5/machine-id.5.html

  - **nodeInfo.operatingSystem** (string), required

    The Operating System reported by the node

  - **nodeInfo.osImage** (string), required

    OS Image reported by the node from /etc/os-release (e.g. Debian GNU/Linux 7 (wheezy)).

  - **nodeInfo.systemUUID** (string), required

    SystemUUID reported by the node. For unique machine identification MachineID is preferred. This field is specific to Red Hat hosts https://access.redhat.com/documentation/en-us/red_hat_subscription_management/1/html/rhsm/uuid

- **phase** (string)

  NodePhase is the recently observed lifecycle phase of the node. More info: https://kubernetes.io/docs/concepts/nodes/node/#phase The field is never populated, and now is deprecated.

- **volumesAttached** ([]AttachedVolume)

  List of volumes that are attached to the node.

  <a name="AttachedVolume"></a>
  *AttachedVolume describes a volume attached to a node*

  - **volumesAttached.devicePath** (string), required

    DevicePath represents the device path where the volume should be available

  - **volumesAttached.name** (string), required

    Name of the attached volume

- **volumesInUse** ([]string)

  List of attachable volumes in use (mounted) by the node.





## NodeList {#NodeList}

NodeList is the whole list of all Nodes which have been registered with master.

<hr>

- **apiVersion**: v1


- **kind**: NodeList


- **metadata** (<a href="{{< ref "../common-definitions/list-meta#ListMeta" >}}">ListMeta</a>)

  Standard list metadata. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds

- **items** ([]<a href="{{< ref "../cluster-resources/node-v1#Node" >}}">Node</a>), required

  List of nodes





## Operations {#Operations}



<hr>






### `get` read the specified Node

#### HTTP Request

GET /api/v1/nodes/{name}

#### Parameters


- **name** (*in path*): string, required

  name of the Node


- **pretty** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>



#### Response


200 (<a href="{{< ref "../cluster-resources/node-v1#Node" >}}">Node</a>): OK

401: Unauthorized


### `get` read status of the specified Node

#### HTTP Request

GET /api/v1/nodes/{name}/status

#### Parameters


- **name** (*in path*): string, required

  name of the Node


- **pretty** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>



#### Response


200 (<a href="{{< ref "../cluster-resources/node-v1#Node" >}}">Node</a>): OK

401: Unauthorized


### `list` list or watch objects of kind Node

#### HTTP Request

GET /api/v1/nodes

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


200 (<a href="{{< ref "../cluster-resources/node-v1#NodeList" >}}">NodeList</a>): OK

401: Unauthorized


### `create` create a Node

#### HTTP Request

POST /api/v1/nodes

#### Parameters


- **body**: <a href="{{< ref "../cluster-resources/node-v1#Node" >}}">Node</a>, required

  


- **dryRun** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>


- **fieldManager** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>


- **pretty** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>



#### Response


200 (<a href="{{< ref "../cluster-resources/node-v1#Node" >}}">Node</a>): OK

201 (<a href="{{< ref "../cluster-resources/node-v1#Node" >}}">Node</a>): Created

202 (<a href="{{< ref "../cluster-resources/node-v1#Node" >}}">Node</a>): Accepted

401: Unauthorized


### `update` replace the specified Node

#### HTTP Request

PUT /api/v1/nodes/{name}

#### Parameters


- **name** (*in path*): string, required

  name of the Node


- **body**: <a href="{{< ref "../cluster-resources/node-v1#Node" >}}">Node</a>, required

  


- **dryRun** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>


- **fieldManager** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>


- **pretty** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>



#### Response


200 (<a href="{{< ref "../cluster-resources/node-v1#Node" >}}">Node</a>): OK

201 (<a href="{{< ref "../cluster-resources/node-v1#Node" >}}">Node</a>): Created

401: Unauthorized


### `update` replace status of the specified Node

#### HTTP Request

PUT /api/v1/nodes/{name}/status

#### Parameters


- **name** (*in path*): string, required

  name of the Node


- **body**: <a href="{{< ref "../cluster-resources/node-v1#Node" >}}">Node</a>, required

  


- **dryRun** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>


- **fieldManager** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>


- **pretty** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>



#### Response


200 (<a href="{{< ref "../cluster-resources/node-v1#Node" >}}">Node</a>): OK

201 (<a href="{{< ref "../cluster-resources/node-v1#Node" >}}">Node</a>): Created

401: Unauthorized


### `patch` partially update the specified Node

#### HTTP Request

PATCH /api/v1/nodes/{name}

#### Parameters


- **name** (*in path*): string, required

  name of the Node


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


200 (<a href="{{< ref "../cluster-resources/node-v1#Node" >}}">Node</a>): OK

201 (<a href="{{< ref "../cluster-resources/node-v1#Node" >}}">Node</a>): Created

401: Unauthorized


### `patch` partially update status of the specified Node

#### HTTP Request

PATCH /api/v1/nodes/{name}/status

#### Parameters


- **name** (*in path*): string, required

  name of the Node


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


200 (<a href="{{< ref "../cluster-resources/node-v1#Node" >}}">Node</a>): OK

201 (<a href="{{< ref "../cluster-resources/node-v1#Node" >}}">Node</a>): Created

401: Unauthorized


### `delete` delete a Node

#### HTTP Request

DELETE /api/v1/nodes/{name}

#### Parameters


- **name** (*in path*): string, required

  name of the Node


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


### `deletecollection` delete collection of Node

#### HTTP Request

DELETE /api/v1/nodes

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

