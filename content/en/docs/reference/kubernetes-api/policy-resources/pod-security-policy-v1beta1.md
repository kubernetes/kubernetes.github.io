---
api_metadata:
  apiVersion: "policy/v1beta1"
  import: "k8s.io/api/policy/v1beta1"
  kind: "PodSecurityPolicy"
content_type: "api_reference"
description: "PodSecurityPolicy governs the ability to make requests that affect the Security Context that will be applied to a pod and container."
title: "PodSecurityPolicy v1beta1"
weight: 5
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

`apiVersion: policy/v1beta1`

`import "k8s.io/api/policy/v1beta1"`


## PodSecurityPolicy {#PodSecurityPolicy}

PodSecurityPolicy governs the ability to make requests that affect the Security Context that will be applied to a pod and container. Deprecated in 1.21.

<hr>

- **apiVersion**: policy/v1beta1


- **kind**: PodSecurityPolicy


- **metadata** (<a href="{{< ref "../common-definitions/object-meta#ObjectMeta" >}}">ObjectMeta</a>)

  Standard object's metadata. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

- **spec** (<a href="{{< ref "../policy-resources/pod-security-policy-v1beta1#PodSecurityPolicySpec" >}}">PodSecurityPolicySpec</a>)

  spec defines the policy enforced.





## PodSecurityPolicySpec {#PodSecurityPolicySpec}

PodSecurityPolicySpec defines the policy enforced.

<hr>

- **runAsUser** (RunAsUserStrategyOptions), required

  runAsUser is the strategy that will dictate the allowable RunAsUser values that may be set.

  <a name="RunAsUserStrategyOptions"></a>
  *RunAsUserStrategyOptions defines the strategy type and any options used to create the strategy.*

  - **runAsUser.rule** (string), required

    rule is the strategy that will dictate the allowable RunAsUser values that may be set.

  - **runAsUser.ranges** ([]IDRange)

    ranges are the allowed ranges of uids that may be used. If you would like to force a single uid then supply a single range with the same start and end. Required for MustRunAs.

    <a name="IDRange"></a>
    *IDRange provides a min/max of an allowed range of IDs.*

    - **runAsUser.ranges.max** (int64), required

      max is the end of the range, inclusive.

    - **runAsUser.ranges.min** (int64), required

      min is the start of the range, inclusive.

- **runAsGroup** (RunAsGroupStrategyOptions)

  RunAsGroup is the strategy that will dictate the allowable RunAsGroup values that may be set. If this field is omitted, the pod's RunAsGroup can take any value. This field requires the RunAsGroup feature gate to be enabled.

  <a name="RunAsGroupStrategyOptions"></a>
  *RunAsGroupStrategyOptions defines the strategy type and any options used to create the strategy.*

  - **runAsGroup.rule** (string), required

    rule is the strategy that will dictate the allowable RunAsGroup values that may be set.

  - **runAsGroup.ranges** ([]IDRange)

    ranges are the allowed ranges of gids that may be used. If you would like to force a single gid then supply a single range with the same start and end. Required for MustRunAs.

    <a name="IDRange"></a>
    *IDRange provides a min/max of an allowed range of IDs.*

    - **runAsGroup.ranges.max** (int64), required

      max is the end of the range, inclusive.

    - **runAsGroup.ranges.min** (int64), required

      min is the start of the range, inclusive.

- **fsGroup** (FSGroupStrategyOptions), required

  fsGroup is the strategy that will dictate what fs group is used by the SecurityContext.

  <a name="FSGroupStrategyOptions"></a>
  *FSGroupStrategyOptions defines the strategy type and options used to create the strategy.*

  - **fsGroup.ranges** ([]IDRange)

    ranges are the allowed ranges of fs groups.  If you would like to force a single fs group then supply a single range with the same start and end. Required for MustRunAs.

    <a name="IDRange"></a>
    *IDRange provides a min/max of an allowed range of IDs.*

    - **fsGroup.ranges.max** (int64), required

      max is the end of the range, inclusive.

    - **fsGroup.ranges.min** (int64), required

      min is the start of the range, inclusive.

  - **fsGroup.rule** (string)

    rule is the strategy that will dictate what FSGroup is used in the SecurityContext.

- **supplementalGroups** (SupplementalGroupsStrategyOptions), required

  supplementalGroups is the strategy that will dictate what supplemental groups are used by the SecurityContext.

  <a name="SupplementalGroupsStrategyOptions"></a>
  *SupplementalGroupsStrategyOptions defines the strategy type and options used to create the strategy.*

  - **supplementalGroups.ranges** ([]IDRange)

    ranges are the allowed ranges of supplemental groups.  If you would like to force a single supplemental group then supply a single range with the same start and end. Required for MustRunAs.

    <a name="IDRange"></a>
    *IDRange provides a min/max of an allowed range of IDs.*

    - **supplementalGroups.ranges.max** (int64), required

      max is the end of the range, inclusive.

    - **supplementalGroups.ranges.min** (int64), required

      min is the start of the range, inclusive.

  - **supplementalGroups.rule** (string)

    rule is the strategy that will dictate what supplemental groups is used in the SecurityContext.

- **seLinux** (SELinuxStrategyOptions), required

  seLinux is the strategy that will dictate the allowable labels that may be set.

  <a name="SELinuxStrategyOptions"></a>
  *SELinuxStrategyOptions defines the strategy type and any options used to create the strategy.*

  - **seLinux.rule** (string), required

    rule is the strategy that will dictate the allowable labels that may be set.

  - **seLinux.seLinuxOptions** (SELinuxOptions)

    seLinuxOptions required to run as; required for MustRunAs More info: https://kubernetes.io/docs/tasks/configure-pod-container/security-context/

    <a name="SELinuxOptions"></a>
    *SELinuxOptions are the labels to be applied to the container*

    - **seLinux.seLinuxOptions.level** (string)

      Level is SELinux level label that applies to the container.

    - **seLinux.seLinuxOptions.role** (string)

      Role is a SELinux role label that applies to the container.

    - **seLinux.seLinuxOptions.type** (string)

      Type is a SELinux type label that applies to the container.

    - **seLinux.seLinuxOptions.user** (string)

      User is a SELinux user label that applies to the container.

- **readOnlyRootFilesystem** (boolean)

  readOnlyRootFilesystem when set to true will force containers to run with a read only root file system.  If the container specifically requests to run with a non-read only root file system the PSP should deny the pod. If set to false the container may run with a read only root file system if it wishes but it will not be forced to.

- **privileged** (boolean)

  privileged determines if a pod can request to be run as privileged.

- **allowPrivilegeEscalation** (boolean)

  allowPrivilegeEscalation determines if a pod can request to allow privilege escalation. If unspecified, defaults to true.

- **defaultAllowPrivilegeEscalation** (boolean)

  defaultAllowPrivilegeEscalation controls the default setting for whether a process can gain more privileges than its parent process.

- **allowedCSIDrivers** ([]AllowedCSIDriver)

  AllowedCSIDrivers is an allowlist of inline CSI drivers that must be explicitly set to be embedded within a pod spec. An empty value indicates that any CSI driver can be used for inline ephemeral volumes. This is a beta field, and is only honored if the API server enables the CSIInlineVolume feature gate.

  <a name="AllowedCSIDriver"></a>
  *AllowedCSIDriver represents a single inline CSI Driver that is allowed to be used.*

  - **allowedCSIDrivers.name** (string), required

    Name is the registered name of the CSI driver

- **allowedCapabilities** ([]string)

  allowedCapabilities is a list of capabilities that can be requested to add to the container. Capabilities in this field may be added at the pod author's discretion. You must not list a capability in both allowedCapabilities and requiredDropCapabilities.

- **requiredDropCapabilities** ([]string)

  requiredDropCapabilities are the capabilities that will be dropped from the container.  These are required to be dropped and cannot be added.

- **defaultAddCapabilities** ([]string)

  defaultAddCapabilities is the default set of capabilities that will be added to the container unless the pod spec specifically drops the capability.  You may not list a capability in both defaultAddCapabilities and requiredDropCapabilities. Capabilities added here are implicitly allowed, and need not be included in the allowedCapabilities list.

- **allowedFlexVolumes** ([]AllowedFlexVolume)

  allowedFlexVolumes is an allowlist of Flexvolumes.  Empty or nil indicates that all Flexvolumes may be used.  This parameter is effective only when the usage of the Flexvolumes is allowed in the "volumes" field.

  <a name="AllowedFlexVolume"></a>
  *AllowedFlexVolume represents a single Flexvolume that is allowed to be used.*

  - **allowedFlexVolumes.driver** (string), required

    driver is the name of the Flexvolume driver.

- **allowedHostPaths** ([]AllowedHostPath)

  allowedHostPaths is an allowlist of host paths. Empty indicates that all host paths may be used.

  <a name="AllowedHostPath"></a>
  *AllowedHostPath defines the host volume conditions that will be enabled by a policy for pods to use. It requires the path prefix to be defined.*

  - **allowedHostPaths.pathPrefix** (string)

    pathPrefix is the path prefix that the host volume must match. It does not support `*`. Trailing slashes are trimmed when validating the path prefix with a host path.
    
    Examples: `/foo` would allow `/foo`, `/foo/` and `/foo/bar` `/foo` would not allow `/food` or `/etc/foo`

  - **allowedHostPaths.readOnly** (boolean)

    when set to true, will allow host volumes matching the pathPrefix only if all volume mounts are readOnly.

- **allowedProcMountTypes** ([]string)

  AllowedProcMountTypes is an allowlist of allowed ProcMountTypes. Empty or nil indicates that only the DefaultProcMountType may be used. This requires the ProcMountType feature flag to be enabled.

- **allowedUnsafeSysctls** ([]string)

  allowedUnsafeSysctls is a list of explicitly allowed unsafe sysctls, defaults to none. Each entry is either a plain sysctl name or ends in "*" in which case it is considered as a prefix of allowed sysctls. Single * means all unsafe sysctls are allowed. Kubelet has to allowlist all allowed unsafe sysctls explicitly to avoid rejection.
  
  Examples: e.g. "foo/*" allows "foo/bar", "foo/baz", etc. e.g. "foo.*" allows "foo.bar", "foo.baz", etc.

- **forbiddenSysctls** ([]string)

  forbiddenSysctls is a list of explicitly forbidden sysctls, defaults to none. Each entry is either a plain sysctl name or ends in "*" in which case it is considered as a prefix of forbidden sysctls. Single * means all sysctls are forbidden.
  
  Examples: e.g. "foo/*" forbids "foo/bar", "foo/baz", etc. e.g. "foo.*" forbids "foo.bar", "foo.baz", etc.

- **hostIPC** (boolean)

  hostIPC determines if the policy allows the use of HostIPC in the pod spec.

- **hostNetwork** (boolean)

  hostNetwork determines if the policy allows the use of HostNetwork in the pod spec.

- **hostPID** (boolean)

  hostPID determines if the policy allows the use of HostPID in the pod spec.

- **hostPorts** ([]HostPortRange)

  hostPorts determines which host port ranges are allowed to be exposed.

  <a name="HostPortRange"></a>
  *HostPortRange defines a range of host ports that will be enabled by a policy for pods to use.  It requires both the start and end to be defined.*

  - **hostPorts.max** (int32), required

    max is the end of the range, inclusive.

  - **hostPorts.min** (int32), required

    min is the start of the range, inclusive.

- **runtimeClass** (RuntimeClassStrategyOptions)

  runtimeClass is the strategy that will dictate the allowable RuntimeClasses for a pod. If this field is omitted, the pod's runtimeClassName field is unrestricted. Enforcement of this field depends on the RuntimeClass feature gate being enabled.

  <a name="RuntimeClassStrategyOptions"></a>
  *RuntimeClassStrategyOptions define the strategy that will dictate the allowable RuntimeClasses for a pod.*

  - **runtimeClass.allowedRuntimeClassNames** ([]string), required

    allowedRuntimeClassNames is an allowlist of RuntimeClass names that may be specified on a pod. A value of "*" means that any RuntimeClass name is allowed, and must be the only item in the list. An empty list requires the RuntimeClassName field to be unset.

  - **runtimeClass.defaultRuntimeClassName** (string)

    defaultRuntimeClassName is the default RuntimeClassName to set on the pod. The default MUST be allowed by the allowedRuntimeClassNames list. A value of nil does not mutate the Pod.

- **volumes** ([]string)

  volumes is an allowlist of volume plugins. Empty indicates that no volumes may be used. To allow all volumes you may use '*'.





## PodSecurityPolicyList {#PodSecurityPolicyList}

PodSecurityPolicyList is a list of PodSecurityPolicy objects.

<hr>

- **apiVersion**: policy/v1beta1


- **kind**: PodSecurityPolicyList


- **metadata** (<a href="{{< ref "../common-definitions/list-meta#ListMeta" >}}">ListMeta</a>)

  Standard list metadata. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

- **items** ([]<a href="{{< ref "../policy-resources/pod-security-policy-v1beta1#PodSecurityPolicy" >}}">PodSecurityPolicy</a>), required

  items is a list of schema objects.





## Operations {#Operations}



<hr>






### `get` read the specified PodSecurityPolicy

#### HTTP Request

GET /apis/policy/v1beta1/podsecuritypolicies/{name}

#### Parameters


- **name** (*in path*): string, required

  name of the PodSecurityPolicy


- **pretty** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>



#### Response


200 (<a href="{{< ref "../policy-resources/pod-security-policy-v1beta1#PodSecurityPolicy" >}}">PodSecurityPolicy</a>): OK

401: Unauthorized


### `list` list or watch objects of kind PodSecurityPolicy

#### HTTP Request

GET /apis/policy/v1beta1/podsecuritypolicies

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


200 (<a href="{{< ref "../policy-resources/pod-security-policy-v1beta1#PodSecurityPolicyList" >}}">PodSecurityPolicyList</a>): OK

401: Unauthorized


### `create` create a PodSecurityPolicy

#### HTTP Request

POST /apis/policy/v1beta1/podsecuritypolicies

#### Parameters


- **body**: <a href="{{< ref "../policy-resources/pod-security-policy-v1beta1#PodSecurityPolicy" >}}">PodSecurityPolicy</a>, required

  


- **dryRun** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>


- **fieldManager** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>


- **pretty** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>



#### Response


200 (<a href="{{< ref "../policy-resources/pod-security-policy-v1beta1#PodSecurityPolicy" >}}">PodSecurityPolicy</a>): OK

201 (<a href="{{< ref "../policy-resources/pod-security-policy-v1beta1#PodSecurityPolicy" >}}">PodSecurityPolicy</a>): Created

202 (<a href="{{< ref "../policy-resources/pod-security-policy-v1beta1#PodSecurityPolicy" >}}">PodSecurityPolicy</a>): Accepted

401: Unauthorized


### `update` replace the specified PodSecurityPolicy

#### HTTP Request

PUT /apis/policy/v1beta1/podsecuritypolicies/{name}

#### Parameters


- **name** (*in path*): string, required

  name of the PodSecurityPolicy


- **body**: <a href="{{< ref "../policy-resources/pod-security-policy-v1beta1#PodSecurityPolicy" >}}">PodSecurityPolicy</a>, required

  


- **dryRun** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>


- **fieldManager** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>


- **pretty** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>



#### Response


200 (<a href="{{< ref "../policy-resources/pod-security-policy-v1beta1#PodSecurityPolicy" >}}">PodSecurityPolicy</a>): OK

201 (<a href="{{< ref "../policy-resources/pod-security-policy-v1beta1#PodSecurityPolicy" >}}">PodSecurityPolicy</a>): Created

401: Unauthorized


### `patch` partially update the specified PodSecurityPolicy

#### HTTP Request

PATCH /apis/policy/v1beta1/podsecuritypolicies/{name}

#### Parameters


- **name** (*in path*): string, required

  name of the PodSecurityPolicy


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


200 (<a href="{{< ref "../policy-resources/pod-security-policy-v1beta1#PodSecurityPolicy" >}}">PodSecurityPolicy</a>): OK

201 (<a href="{{< ref "../policy-resources/pod-security-policy-v1beta1#PodSecurityPolicy" >}}">PodSecurityPolicy</a>): Created

401: Unauthorized


### `delete` delete a PodSecurityPolicy

#### HTTP Request

DELETE /apis/policy/v1beta1/podsecuritypolicies/{name}

#### Parameters


- **name** (*in path*): string, required

  name of the PodSecurityPolicy


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


200 (<a href="{{< ref "../policy-resources/pod-security-policy-v1beta1#PodSecurityPolicy" >}}">PodSecurityPolicy</a>): OK

202 (<a href="{{< ref "../policy-resources/pod-security-policy-v1beta1#PodSecurityPolicy" >}}">PodSecurityPolicy</a>): Accepted

401: Unauthorized


### `deletecollection` delete collection of PodSecurityPolicy

#### HTTP Request

DELETE /apis/policy/v1beta1/podsecuritypolicies

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

