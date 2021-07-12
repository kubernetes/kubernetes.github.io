---
title: 特性门控
weight: 10
content_type: concept
---

<!--
title: Feature Gates
weight: 10
content_type: concept
-->

<!-- overview -->
<!--
This page contains an overview of the various feature gates an administrator
can specify on different Kubernetes components.

See [feature stages](#feature-stages) for an explanation of the stages for a feature.
-->
本页详述了管理员可以在不同的 Kubernetes 组件上指定的各种特性门控。

关于特性各个阶段的说明，请参见[特性阶段](#feature-stages)。

<!-- body -->

<!--
## Overview

Feature gates are a set of key=value pairs that describe Kubernetes features.
You can turn these features on or off using the `--feature-gates` command line flag
on each Kubernetes component.
-->
## 概述

特性门控是描述 Kubernetes 特性的一组键值对。你可以在 Kubernetes 的各个组件中使用
`--feature-gates` flag 来启用或禁用这些特性。

<!--
Each Kubernetes component lets you enable or disable a set of feature gates that
are relevant to that component.
Use `-h` flag to see a full set of feature gates for all components.
To set feature gates for a component, such as kubelet, use the `--feature-gates` flag assigned to a list of feature pairs:
-->
每个 Kubernetes 组件都支持启用或禁用与该组件相关的一组特性门控。
使用 `-h` 参数来查看所有组件支持的完整特性门控。
要为诸如 kubelet 之类的组件设置特性门控，请使用 `--feature-gates` 参数，并向其
传递一个特性设置键值对列表：

```shell
--feature-gates="...,DynamicKubeletConfig=true"
```

<!--
The following tables are a summary of the feature gates that you can set on
different Kubernetes components.
-->
下表总结了在不同的 Kubernetes 组件上可以设置的特性门控。

<!--
- The "Since" column contains the Kubernetes release when a feature is introduced
  or its release stage is changed.
- The "Until" column, if not empty, contains the last Kubernetes release in which
  you can still use a feature gate.
- If a feature is in the Alpha or Beta state, you can find the feature listed
  in the [Alpha/Beta feature gate table](#feature-gates-for-alpha-or-beta-features).
- If a feature is stable you can find all stages for that feature listed in the
  [Graduated/Deprecated feature gate table](#feature-gates-for-graduated-or-deprecated-features).
- The [Graduated/Deprecated feature gate table](#feature-gates-for-graduated-or-deprecated-features)
  also lists deprecated and withdrawn features.
-->
- 引入特性或更改其发布阶段后，"开始（Since）" 列将包含 Kubernetes 版本。
- "结束（Until）" 列（如果不为空）包含最后一个 Kubernetes 版本，你仍可以在其中使用特性门控。
- 如果某个特性处于 Alpha 或 Beta 状态，你可以在
  [Alpha 和 Beta 特性门控表](#feature-gates-for-alpha-or-beta-features)中找到该特性。
- 如果某个特性处于稳定状态，你可以在
  [已毕业和废弃特性门控表](#feature-gates-for-graduated-or-deprecated-features)
  中找到该特性的所有阶段。
- [已毕业和废弃特性门控表](#feature-gates-for-graduated-or-deprecated-features)
  还列出了废弃的和已被移除的特性。

<!--
### Feature gates for Alpha or Beta features

{{< table caption="Feature gates for features in Alpha or Beta states" >}}

| Feature | Default | Stage | Since | Until |

{{< /table >}}
-->
### Alpha 和 Beta 状态的特性门控  {#feature-gates-for-alpha-or-beta-features}

{{< table caption="处于 Alpha 或 Beta 状态的特性门控" >}}

| 特性    | 默认值  | 状态  | 开始（Since） | 结束（Until） |
|---------|---------|-------|---------------|---------------|
| `APIListChunking` | `false` | Alpha | 1.8 | 1.8 |
| `APIListChunking` | `true` | Beta | 1.9 | |
| `APIPriorityAndFairness` | `false` | Alpha | 1.17 | 1.19 |
| `APIPriorityAndFairness` | `true` | Beta | 1.20 | |
| `APIResponseCompression` | `false` | Alpha | 1.7 | 1.15 |
| `APIResponseCompression` | `true` | Beta | 1.16 | |
| `APIServerIdentity` | `false` | Alpha | 1.20 | |
| `AllowInsecureBackendProxy` | `true` | Beta | 1.17 | |
| `AnyVolumeDataSource` | `false` | Alpha | 1.18 | |
| `AppArmor` | `true` | Beta | 1.4 | |
| `BalanceAttachedNodeVolumes` | `false` | Alpha | 1.11 | |
| `BoundServiceAccountTokenVolume` | `false` | Alpha | 1.13 | 1.20 |
| `BoundServiceAccountTokenVolume` | `true` | Beta | 1.21 | |
| `CPUManager` | `false` | Alpha | 1.8 | 1.9 |
| `CPUManager` | `true` | Beta | 1.10 | |
| `CSIInlineVolume` | `false` | Alpha | 1.15 | 1.15 |
| `CSIInlineVolume` | `true` | Beta | 1.16 | - |
| `CSIMigration` | `false` | Alpha | 1.14 | 1.16 |
| `CSIMigration` | `true` | Beta | 1.17 | |
| `CSIMigrationAWS` | `false` | Alpha | 1.14 | |
| `CSIMigrationAWS` | `false` | Beta | 1.17 | |
| `CSIMigrationAWSComplete` | `false` | Alpha | 1.17 | |
| `CSIMigrationAzureDisk` | `false` | Alpha | 1.15 | 1.18 |
| `CSIMigrationAzureDisk` | `false` | Beta | 1.19 | |
| `CSIMigrationAzureDiskComplete` | `false` | Alpha | 1.17 | |
| `CSIMigrationAzureFile` | `false` | Alpha | 1.15 | 1.19 |
| `CSIMigrationAzureFile` | `false` | Beta | 1.21 | |
| `CSIMigrationAzureFileComplete` | `false` | Alpha | 1.17 | |
| `CSIMigrationGCE` | `false` | Alpha | 1.14 | 1.16 |
| `CSIMigrationGCE` | `false` | Beta | 1.17 | |
| `CSIMigrationGCEComplete` | `false` | Alpha | 1.17 | |
| `CSIMigrationOpenStack` | `false` | Alpha | 1.14 | 1.17 |
| `CSIMigrationOpenStack` | `true` | Beta | 1.18 | |
| `CSIMigrationOpenStackComplete` | `false` | Alpha | 1.17 | |
| `CSIMigrationvSphere` | `false` | Beta | 1.19 | |
| `CSIMigrationvSphereComplete` | `false` | Beta | 1.19 | |
| `CSIServiceAccountToken` | `false` | Alpha | 1.20 | 1.20 |
| `CSIServiceAccountToken` | `true` | Beta | 1.21 | |
| `CSIStorageCapacity` | `false` | Alpha | 1.19 | 1.20 |
| `CSIStorageCapacity` | `true` | Beta | 1.21 | |
| `CSIVolumeFSGroupPolicy` | `false` | Alpha | 1.19 | 1.19 |
| `CSIVolumeFSGroupPolicy` | `true` | Beta | 1.20 | |
| `CSIVolumeHealth` | `false` | Alpha | 1.21 | |
| `ConfigurableFSGroupPolicy` | `false` | Alpha | 1.18 | 1.19 |
| `ConfigurableFSGroupPolicy` | `true` | Beta | 1.20 | |
| `CronJobControllerV2` | `false` | Alpha | 1.20 | 1.20 |
| `CronJobControllerV2` | `true` | Beta | 1.21 | |
| `CustomCPUCFSQuotaPeriod` | `false` | Alpha | 1.12 | |
| `DefaultPodTopologySpread` | `false` | Alpha | 1.19 | 1.19 |
| `DefaultPodTopologySpread` | `true` | Beta | 1.20 | |
| `DevicePlugins` | `false` | Alpha | 1.8 | 1.9 |
| `DevicePlugins` | `true` | Beta | 1.10 | |
| `DisableAcceleratorUsageMetrics` | `false` | Alpha | 1.19 | 1.19 |
| `DisableAcceleratorUsageMetrics` | `true` | Beta | 1.20 | |
| `DownwardAPIHugePages` | `false` | Alpha | 1.20 | 1.20 |
| `DownwardAPIHugePages` | `false` | Beta | 1.21 | |
| `DynamicKubeletConfig` | `false` | Alpha | 1.4 | 1.10 |
| `DynamicKubeletConfig` | `true` | Beta | 1.11 | |
| `EfficientWatchResumption` | `false` | Alpha | 1.20 | |
| `EndpointSliceProxying` | `false` | Alpha | 1.18 | 1.18 |
| `EndpointSliceProxying` | `true` | Beta | 1.19 | |
| `EndpointSliceTerminatingCondition` | `false` | Alpha | 1.20 | |
| `EphemeralContainers` | `false` | Alpha | 1.16 | |
| `ExpandCSIVolumes` | `false` | Alpha | 1.14 | 1.15 |
| `ExpandCSIVolumes` | `true` | Beta | 1.16 | |
| `ExpandInUsePersistentVolumes` | `false` | Alpha | 1.11 | 1.14 |
| `ExpandInUsePersistentVolumes` | `true` | Beta | 1.15 | |
| `ExpandPersistentVolumes` | `false` | Alpha | 1.8 | 1.10 |
| `ExpandPersistentVolumes` | `true` | Beta | 1.11 | |
| `ExperimentalHostUserNamespaceDefaulting` | `false` | Beta | 1.5 | |
| `GenericEphemeralVolume` | `false` | Alpha | 1.19 | 1.20 |
| `GenericEphemeralVolume` | `true` | Beta | 1.21 | |
| `GracefulNodeShutdown` | `false` | Alpha | 1.20 | 1.20 |
| `GracefulNodeShutdown` | `true` | Beta | 1.21 | |
| `HPAContainerMetrics` | `false` | Alpha | 1.20 | |
| `HPAScaleToZero` | `false` | Alpha | 1.16 | |
| `HugePageStorageMediumSize` | `false` | Alpha | 1.18 | 1.18 |
| `HugePageStorageMediumSize` | `true` | Beta | 1.19 | |
| `IndexedJob` | `false` | Alpha | 1.21 | |
| `IngressClassNamespacedParams` | `false` | Alpha | 1.21 | |
| `IPv6DualStack` | `false` | Alpha | 1.15 | 1.20 |
| `IPv6DualStack` | `true` | Beta | 1.21 | |
| `KubeletCredentialProviders` | `false` | Alpha | 1.20 | |
| `LegacyNodeRoleBehavior` | `false` | Alpha | 1.16 | 1.18 |
| `LegacyNodeRoleBehavior` | `true` | True | 1.19 | 1.20 |
| `LocalStorageCapacityIsolation` | `false` | Alpha | 1.7 | 1.9 |
| `LocalStorageCapacityIsolation` | `true` | Beta | 1.10 | |
| `LocalStorageCapacityIsolationFSQuotaMonitoring` | `false` | Alpha | 1.15 | |
| `LogarithmicScaleDown` | `false` | Alpha | 1.21 | |
| `KubeletPodResourcesGetAllocatable` | `false` | Alpha | 1.21 | |
| `MixedProtocolLBService` | `false` | Alpha | 1.20 | |
| `NamespaceDefaultLabelName` | `true` | Beta | 1.21 | |
| `NetworkPolicyEndPort` | `false` | Alpha | 1.21 |  |
| `NodeDisruptionExclusion` | `false` | Alpha | 1.16 | 1.18 |
| `NodeDisruptionExclusion` | `true` | Beta | 1.19 | 1.20 |
| `NonPreemptingPriority` | `false` | Alpha | 1.15 | 1.18 |
| `NonPreemptingPriority` | `true` | Beta | 1.19 | |
| `PodDeletionCost` | `false` | Alpha | 1.21 | |
| `PodAffinityNamespaceSelector` | `false` | Alpha | 1.21 | |
| `PodOverhead` | `false` | Alpha | 1.16 | 1.17 |
| `PodOverhead` | `true` | Beta | 1.18 |  |
| `ProbeTerminationGracePeriod` | `false` | Alpha | 1.21 | |
| `ProcMountType` | `false` | Alpha | 1.12 | |
| `QOSReserved` | `false` | Alpha | 1.11 | |
| `RemainingItemCount` | `false` | Alpha | 1.15 | |
| `RemoveSelfLink` | `false` | Alpha | 1.16 | 1.19 |
| `RemoveSelfLink` | `true` | Beta | 1.20 | |
| `RotateKubeletServerCertificate` | `false` | Alpha | 1.7 | 1.11 |
| `RotateKubeletServerCertificate` | `true` | Beta | 1.12 | |
| `RunAsGroup` | `true` | Beta | 1.14 | |
| `ServerSideApply` | `false` | Alpha | 1.14 | 1.15 |
| `ServerSideApply` | `true` | Beta | 1.16 | |
| `ServiceInternalTrafficPolicy` | `false` | Alpha | 1.21 | |
| `ServiceLBNodePortControl` | `false` | Alpha | 1.20 | |
| `ServiceLoadBalancerClass` | `false` | Alpha | 1.21 | |
| `ServiceNodeExclusion` | `false` | Alpha | 1.8 | 1.18 |
| `ServiceNodeExclusion` | `true` | Beta | 1.19 | 1.20 |
| `ServiceTopology` | `false` | Alpha | 1.17 | |
| `SetHostnameAsFQDN` | `false` | Alpha | 1.19 | 1.19 |
| `SetHostnameAsFQDN` | `true` | Beta | 1.20 | |
| `SizeMemoryBackedVolumes` | `false` | Alpha | 1.20 | |
| `StorageVersionAPI` | `false` | Alpha | 1.20 | |
| `StorageVersionHash` | `false` | Alpha | 1.14 | 1.14 |
| `StorageVersionHash` | `true` | Beta | 1.15 | |
| `SuspendJob` | `false` | Alpha | 1.21 | |
| `TTLAfterFinished` | `false` | Alpha | 1.12 | 1.20 |
| `TTLAfterFinished` | `false` | Beta | 1.21 | |
| `TopologyAwareHints` | `false` | Alpha | 1.21 | |
| `TopologyManager` | `false` | Alpha | 1.16 | 1.17 |
| `TopologyManager` | `true` | Beta | 1.18 | |
| `ValidateProxyRedirects` | `false` | Alpha | 1.12 | 1.13 |
| `ValidateProxyRedirects` | `true` | Beta | 1.14 | |
| `VolumeCapacityPriority` | `false` | Alpha | 1.21 | - |
| `WarningHeaders` | `true` | Beta | 1.19 | |
| `WinDSR` | `false` | Alpha | 1.14 | |
| `WinOverlay` | `false` | Alpha | 1.14 | 1.19 |
| `WinOverlay` | `true` | Beta | 1.20 | |
| `WindowsEndpointSliceProxying` | `false` | Alpha | 1.19 | 1.20 |
| `WindowsEndpointSliceProxying` | `true` | Beta | 1.21 | |
{{< /table >}}

<!--
### Feature gates for graduated or deprecated features

{{< table caption="Feature Gates for Graduated or Deprecated Features" >}}

| Feature | Default | Stage | Since | Until |

{{< /table >}}
-->
### 已毕业和已废弃的特性门控  {#feature-gates-for-graduated-or-deprecated-features}

{{< table caption="已毕业或不推荐使用的特性门控" >}}

| 特性    | 默认值  | 状态  | 开始（Since） | 结束（Until） |
|---------|---------|-------|---------------|---------------|
| `Accelerators` | `false` | Alpha | 1.6 | 1.10 |
| `Accelerators` | - | Deprecated | 1.11 | - |
| `AdvancedAuditing` | `false` | Alpha | 1.7 | 1.7 |
| `AdvancedAuditing` | `true` | Beta | 1.8 | 1.11 |
| `AdvancedAuditing` | `true` | GA | 1.12 | - |
| `AffinityInAnnotations` | `false` | Alpha | 1.6 | 1.7 |
| `AffinityInAnnotations` | - | Deprecated | 1.8 | - |
| `AllowExtTrafficLocalEndpoints` | `false` | Beta | 1.4 | 1.6 |
| `AllowExtTrafficLocalEndpoints` | `true` | GA | 1.7 | - |
| `BlockVolume` | `false` | Alpha | 1.9 | 1.12 |
| `BlockVolume` | `true` | Beta | 1.13 | 1.17 |
| `BlockVolume` | `true` | GA | 1.18 | - |
| `CRIContainerLogRotation` | `false` | Alpha | 1.10 | 1.10 |
| `CRIContainerLogRotation` | `true` | Beta | 1.11 | 1.20 |
| `CRIContainerLogRotation` | `true` | GA | 1.21 | - |
| `CSIBlockVolume` | `false` | Alpha | 1.11 | 1.13 |
| `CSIBlockVolume` | `true` | Beta | 1.14 | 1.17 |
| `CSIBlockVolume` | `true` | GA | 1.18 | - |
| `CSIDriverRegistry` | `false` | Alpha | 1.12 | 1.13 |
| `CSIDriverRegistry` | `true` | Beta | 1.14 | 1.17 |
| `CSIDriverRegistry` | `true` | GA | 1.18 | |
| `CSINodeInfo` | `false` | Alpha | 1.12 | 1.13 |
| `CSINodeInfo` | `true` | Beta | 1.14 | 1.16 |
| `CSINodeInfo` | `true` | GA | 1.17 | |
| `AttachVolumeLimit` | `false` | Alpha | 1.11 | 1.11 |
| `AttachVolumeLimit` | `true` | Beta | 1.12 | 1.16 |
| `AttachVolumeLimit` | `true` | GA | 1.17 | - |
| `CSIPersistentVolume` | `false` | Alpha | 1.9 | 1.9 |
| `CSIPersistentVolume` | `true` | Beta | 1.10 | 1.12 |
| `CSIPersistentVolume` | `true` | GA | 1.13 | - |
| `CustomPodDNS` | `false` | Alpha | 1.9 | 1.9 |
| `CustomPodDNS` | `true` | Beta| 1.10 | 1.13 |
| `CustomPodDNS` | `true` | GA | 1.14 | - |
| `CustomResourceDefaulting` | `false` | Alpha| 1.15 | 1.15 |
| `CustomResourceDefaulting` | `true` | Beta | 1.16 | 1.16 |
| `CustomResourceDefaulting` | `true` | GA | 1.17 | - |
| `CustomResourcePublishOpenAPI` | `false` | Alpha| 1.14 | 1.14 |
| `CustomResourcePublishOpenAPI` | `true` | Beta| 1.15 | 1.15 |
| `CustomResourcePublishOpenAPI` | `true` | GA | 1.16 | - |
| `CustomResourceSubresources` | `false` | Alpha | 1.10 | 1.10 |
| `CustomResourceSubresources` | `true` | Beta | 1.11 | 1.15 |
| `CustomResourceSubresources` | `true` | GA | 1.16 | - |
| `CustomResourceValidation` | `false` | Alpha | 1.8 | 1.8 |
| `CustomResourceValidation` | `true` | Beta | 1.9 | 1.15 |
| `CustomResourceValidation` | `true` | GA | 1.16 | - |
| `CustomResourceWebhookConversion` | `false` | Alpha | 1.13 | 1.14 |
| `CustomResourceWebhookConversion` | `true` | Beta | 1.15 | 1.15 |
| `CustomResourceWebhookConversion` | `true` | GA | 1.16 | - |
| `DryRun` | `false` | Alpha | 1.12 | 1.12 |
| `DryRun` | `true` | Beta | 1.13 | 1.18 |
| `DryRun` | `true` | GA | 1.19 | - |
| `DynamicAuditing` | `false` | Alpha | 1.13 | 1.18 |
| `DynamicAuditing` | - | Deprecated | 1.19 | - |
| `DynamicProvisioningScheduling` | `false` | Alpha | 1.11 | 1.11 |
| `DynamicProvisioningScheduling` | - | Deprecated| 1.12 | - |
| `DynamicVolumeProvisioning` | `true` | Alpha | 1.3 | 1.7 |
| `DynamicVolumeProvisioning` | `true` | GA | 1.8 | - |
| `EnableAggregatedDiscoveryTimeout` | `true` | Deprecated | 1.16 | - |
| `EnableEquivalenceClassCache` | `false` | Alpha | 1.8 | 1.14 |
| `EnableEquivalenceClassCache` | - | Deprecated | 1.15 | - |
| `EndpointSlice` | `false` | Alpha | 1.16 | 1.16 |
| `EndpointSlice` | `false` | Beta | 1.17 | 1.17 |
| `EndpointSlice` | `true` | Beta | 1.18 | 1.20 |
| `EndpointSlice` | `true` | GA | 1.21 | -  |
| `EndpointSliceNodeName` | `false` | Alpha | 1.20 | 1.21 |
| `EndpointSliceNodeName` | `true` | Beta | 1.18 | 1.20 |
| `ExperimentalCriticalPodAnnotation` | `false` | Alpha | 1.5 | 1.12 |
| `ExperimentalCriticalPodAnnotation` | `false` | Deprecated | 1.13 | - |
| `EvenPodsSpread` | `false` | Alpha | 1.16 | 1.17 |
| `EvenPodsSpread` | `true` | Beta | 1.18 | 1.18 |
| `EvenPodsSpread` | `true` | GA | 1.19 | - |
| `ExecProbeTimeout` | `true` | GA | 1.20 | - |
| `ExternalPolicyForExternalIP` | `true` | GA | 1.18 | - |
| `GCERegionalPersistentDisk` | `true` | Beta | 1.10 | 1.12 |
| `GCERegionalPersistentDisk` | `true` | GA | 1.13 | - |
| `HugePages` | `false` | Alpha | 1.8 | 1.9 |
| `HugePages` | `true` | Beta| 1.10 | 1.13 |
| `HugePages` | `true` | GA | 1.14 | - |
| `HyperVContainer` | `false` | Alpha | 1.10 | 1.19 |
| `HyperVContainer` | `false` | Deprecated | 1.20 | - |
| `ImmutableEphemeralVolumes` | `false` | Alpha | 1.18 | 1.18 |
| `ImmutableEphemeralVolumes` | `true` | Beta | 1.19 | 1.20 |
| `ImmutableEphemeralVolumes` | `true` | GA | 1.21 | |
| `Initializers` | `false` | Alpha | 1.7 | 1.13 |
| `Initializers` | - | Deprecated | 1.14 | - |
| `KubeletConfigFile` | `false` | Alpha | 1.8 | 1.9 |
| `KubeletConfigFile` | - | Deprecated | 1.10 | - |
| `KubeletPluginsWatcher` | `false` | Alpha | 1.11 | 1.11 |
| `KubeletPluginsWatcher` | `true` | Beta | 1.12 | 1.12 |
| `KubeletPluginsWatcher` | `true` | GA | 1.13 | - |
| `KubeletPodResources` | `false` | Alpha | 1.13 | 1.14 |
| `KubeletPodResources` | `true` | Beta | 1.15 | |
| `KubeletPodResources` | `true` | GA | 1.20 | |
| `LegacyNodeRoleBehavior` | `false` | GA | 1.21 | - |
| `MountContainers` | `false` | Alpha | 1.9 | 1.16 |
| `MountContainers` | `false` | Deprecated | 1.17 | - |
| `MountPropagation` | `false` | Alpha | 1.8 | 1.9 |
| `MountPropagation` | `true` | Beta | 1.10 | 1.11 |
| `MountPropagation` | `true` | GA | 1.12 | - |
| `NodeDisruptionExclusion` | `true` | GA | 1.21 | - |
| `NodeLease` | `false` | Alpha | 1.12 | 1.13 |
| `NodeLease` | `true` | Beta | 1.14 | 1.16 |
| `NodeLease` | `true` | GA | 1.17 | - |
| `PVCProtection` | `false` | Alpha | 1.9 | 1.9 |
| `PVCProtection` | - | Deprecated | 1.10 | - |
| `PersistentLocalVolumes` | `false` | Alpha | 1.7 | 1.9 |
| `PersistentLocalVolumes` | `true` | Beta | 1.10 | 1.13 |
| `PersistentLocalVolumes` | `true` | GA | 1.14 | - |
| `PodDisruptionBudget` | `false` | Alpha | 1.3 | 1.4 |
| `PodDisruptionBudget` | `true` | Beta | 1.5 | 1.20 |
| `PodDisruptionBudget` | `true` | GA | 1.21 | - |
| `PodPriority` | `false` | Alpha | 1.8 | 1.10 |
| `PodPriority` | `true` | Beta | 1.11 | 1.13 |
| `PodPriority` | `true` | GA | 1.14 | - |
| `PodReadinessGates` | `false` | Alpha | 1.11 | 1.11 |
| `PodReadinessGates` | `true` | Beta | 1.12 | 1.13 |
| `PodReadinessGates` | `true` | GA | 1.14 | - |
| `PodShareProcessNamespace` | `false` | Alpha | 1.10 | 1.11 |
| `PodShareProcessNamespace` | `true` | Beta | 1.12 | 1.16 |
| `PodShareProcessNamespace` | `true` | GA | 1.17 | - |
| `RequestManagement` | `false` | Alpha | 1.15 | 1.16 |
| `RequestManagement` | - | Derecated | 1.17 | - |
| `ResourceLimitsPriorityFunction` | `false` | Alpha | 1.9 | 1.18 |
| `ResourceLimitsPriorityFunction` | - | Deprecated | 1.19 | - |
| `ResourceQuotaScopeSelectors` | `false` | Alpha | 1.11 | 1.11 |
| `ResourceQuotaScopeSelectors` | `true` | Beta | 1.12 | 1.16 |
| `ResourceQuotaScopeSelectors` | `true` | GA | 1.17 | - |
| `RootCAConfigMap` | `false` | Alpha | 1.13 | 1.19 |
| `RootCAConfigMap` | `true` | Beta | 1.20 | 1.20 |
| `RootCAConfigMap` | `true` | GA | 1.21 | - |
| `RotateKubeletClientCertificate` | `true` | Beta | 1.8 | 1.18 |
| `RotateKubeletClientCertificate` | `true` | GA | 1.19 | - |
| `RuntimeClass` | `false` | Alpha | 1.12 | 1.13 |
| `RuntimeClass` | `true` | Beta | 1.14 | 1.19 |
| `RuntimeClass` | `true` | GA | 1.20 | - |
| `ScheduleDaemonSetPods` | `false` | Alpha | 1.11 | 1.11 |
| `ScheduleDaemonSetPods` | `true` | Beta | 1.12 | 1.16  |
| `ScheduleDaemonSetPods` | `true` | GA | 1.17 | - |
| `SCTPSupport` | `false` | Alpha | 1.12 | 1.18 |
| `SCTPSupport` | `true` | Beta | 1.19 | 1.19 |
| `SCTPSupport` | `true` | GA | 1.20 | - |
| `ServiceAccountIssuerDiscovery` | `false` | Alpha | 1.18 | 1.19 |
| `ServiceAccountIssuerDiscovery` | `true` | Beta | 1.20 | 1.20 |
| `ServiceAccountIssuerDiscovery` | `true` | GA | 1.21 | - |
| `ServiceAppProtocol` | `false` | Alpha | 1.18 | 1.18 |
| `ServiceAppProtocol` | `true` | Beta | 1.19 | 1.19 |
| `ServiceAppProtocol` | `true` | GA | 1.20 | - |
| `ServiceLoadBalancerFinalizer` | `false` | Alpha | 1.15 | 1.15 |
| `ServiceLoadBalancerFinalizer` | `true` | Beta | 1.16 | 1.16 |
| `ServiceLoadBalancerFinalizer` | `true` | GA | 1.17 | - |
| `ServiceNodeExclusion` | `true` | GA | 1.21 | - |
| `StartupProbe` | `false` | Alpha | 1.16 | 1.17 |
| `StartupProbe` | `true` | Beta | 1.18 | 1.19 |
| `StartupProbe` | `true` | GA | 1.20 | - |
| `StorageObjectInUseProtection` | `true` | Beta | 1.10 | 1.10 |
| `StorageObjectInUseProtection` | `true` | GA | 1.11 | - |
| `StreamingProxyRedirects` | `false` | Beta | 1.5 | 1.5 |
| `StreamingProxyRedirects` | `true` | Beta | 1.6 | 1.18 |
| `StreamingProxyRedirects` | - | GA | 1.19 | - |
| `SupportIPVSProxyMode` | `false` | Alpha | 1.8 | 1.8 |
| `SupportIPVSProxyMode` | `false` | Beta | 1.9 | 1.9 |
| `SupportIPVSProxyMode` | `true` | Beta | 1.10 | 1.10 |
| `SupportIPVSProxyMode` | `true` | GA | 1.11 | - |
| `SupportNodePidsLimit` | `false` | Alpha | 1.14 | 1.14 |
| `SupportNodePidsLimit` | `true` | Beta | 1.15 | 1.19 |
| `SupportNodePidsLimit` | `true` | GA | 1.20 | - |
| `SupportPodPidsLimit` | `false` | Alpha | 1.10 | 1.13 |
| `SupportPodPidsLimit` | `true` | Beta | 1.14 | 1.19 |
| `SupportPodPidsLimit` | `true` | GA | 1.20 | - |
| `Sysctls` | `true` | Beta | 1.11 | 1.20 |
| `Sysctls` | `true` | GA | 1.21 | |
| `TaintBasedEvictions` | `false` | Alpha | 1.6 | 1.12 |
| `TaintBasedEvictions` | `true` | Beta | 1.13 | 1.17 |
| `TaintBasedEvictions` | `true` | GA | 1.18 | - |
| `TaintNodesByCondition` | `false` | Alpha | 1.8 | 1.11 |
| `TaintNodesByCondition` | `true` | Beta | 1.12 | 1.16 |
| `TaintNodesByCondition` | `true` | GA | 1.17 | - |
| `TokenRequest` | `false` | Alpha | 1.10 | 1.11 |
| `TokenRequest` | `true` | Beta | 1.12 | 1.19 |
| `TokenRequest` | `true` | GA | 1.20 | - |
| `TokenRequestProjection` | `false` | Alpha | 1.11 | 1.11 |
| `TokenRequestProjection` | `true` | Beta | 1.12 | 1.19 |
| `TokenRequestProjection` | `true` | GA | 1.20 | - |
| `VolumePVCDataSource` | `false` | Alpha | 1.15 | 1.15 |
| `VolumePVCDataSource` | `true` | Beta | 1.16 | 1.17 |
| `VolumePVCDataSource` | `true` | GA | 1.18 | - |
| `VolumeScheduling` | `false` | Alpha | 1.9 | 1.9 |
| `VolumeScheduling` | `true` | Beta | 1.10 | 1.12 |
| `VolumeScheduling` | `true` | GA | 1.13 | - |
| `VolumeSnapshotDataSource` | `false` | Alpha | 1.12 | 1.16 |
| `VolumeSnapshotDataSource` | `true` | Beta | 1.17 | 1.19 |
| `VolumeSnapshotDataSource` | `true` | GA | 1.20 | - |
| `VolumeSubpath` | `true` | GA | 1.10 | - |
| `VolumeSubpathEnvExpansion` | `false` | Alpha | 1.14 | 1.14 |
| `VolumeSubpathEnvExpansion` | `true` | Beta | 1.15 | 1.16 |
| `VolumeSubpathEnvExpansion` | `true` | GA | 1.17 | - |
| `WatchBookmark` | `false` | Alpha | 1.15 | 1.15 |
| `WatchBookmark` | `true` | Beta | 1.16 | 1.16 |
| `WatchBookmark` | `true` | GA | 1.17 | - |
| `WindowsGMSA` | `false` | Alpha | 1.14 | 1.15 |
| `WindowsGMSA` | `true` | Beta | 1.16 | 1.17 |
| `WindowsGMSA` | `true` | GA | 1.18 | - |
| `WindowsRunAsUserName` | `false` | Alpha | 1.16 | 1.16 |
| `WindowsRunAsUserName` | `true` | Beta | 1.17 | 1.17 |
| `WindowsRunAsUserName` | `true` | GA | 1.18 | - |
{{< /table >}}

<!--
## Using a feature

### Feature stages
-->
## 使用特性   {#using-a-feature}

### 特性阶段    {#feature-stages}

<!--
A feature can be in *Alpha*, *Beta* or *GA* stage.
An *Alpha* feature means:
-->

处于 *Alpha* 、*Beta* 、 *GA* 阶段的特性。

*Alpha* 特性代表：

<!--
* Disabled by default.
* Might be buggy. Enabling the feature may expose bugs.
* Support for feature may be dropped at any time without notice.
* The API may change in incompatible ways in a later software release without notice.
* Recommended for use only in short-lived testing clusters, due to increased
  risk of bugs and lack of long-term support.
-->
* 默认禁用。
* 可能有错误，启用此特性可能会导致错误。
* 随时可能删除对此特性的支持，恕不另行通知。
* 在以后的软件版本中，API 可能会以不兼容的方式更改，恕不另行通知。
* 建议将其仅用于短期测试中，因为开启特性会增加错误的风险，并且缺乏长期支持。

<!--
A *Beta* feature means:
-->
*Beta* 特性代表：

<!--
* Enabled by default.
* The feature is well tested. Enabling the feature is considered safe.
* Support for the overall feature will not be dropped, though details may change.
* The schema and/or semantics of objects may change in incompatible ways in a
  subsequent beta or stable release. When this happens, we will provide instructions
  for migrating to the next version. This may require deleting, editing, and
  re-creating API objects. The editing process may require some thought.
  This may require downtime for applications that rely on the feature.
* Recommended for only non-business-critical uses because of potential for
  incompatible changes in subsequent releases. If you have multiple clusters
  that can be upgraded independently, you may be able to relax this restriction.
-->
* 默认启用。
* 该特性已经经过良好测试。启用该特性是安全的。
* 尽管详细信息可能会更改，但不会放弃对整体特性的支持。
* 对象的架构或语义可能会在随后的 Beta 或稳定版本中以不兼容的方式更改。当发生这种情况时，我们将提供迁移到下一版本的说明。此特性可能需要删除、编辑和重新创建 API 对象。编辑过程可能需要慎重操作，因为这可能会导致依赖该特性的应用程序停机。
* 推荐仅用于非关键业务用途，因为在后续版本中可能会发生不兼容的更改。如果你具有多个可以独立升级的，则可以放宽此限制。

{{< note >}}
<!--
Please do try *Beta* features and give feedback on them!
After they exit beta, it may not be practical for us to make more changes.
-->
请试用 *Beta* 特性并提供相关反馈！
一旦特性结束 Beta 状态，我们就不太可能再对特性进行大幅修改。
{{< /note >}}

<!--
A *General Availability* (GA) feature is also referred to as a *stable* feature. It means:
-->
*General Availability* (GA) 特性也称为 *稳定* 特性，*GA* 特性代表着：

<!--
* The feature is always enabled; you cannot disable it.
* The corresponding feature gate is no longer needed.
* Stable versions of features will appear in released software for many subsequent versions.
-->
* 此特性会一直启用；你不能禁用它。
* 不再需要相应的特性门控。
* 对于许多后续版本，特性的稳定版本将出现在发行的软件中。

<!--
## List of feature gates {#feature-gates}

Each feature gate is designed for enabling/disabling a specific feature:
-->

### 特性门控列表

每个特性门控均用于启用或禁用某个特定的特性：

<!--
- `APIListChunking`: Enable the API clients to retrieve (`LIST` or `GET`)
  resources from API server in chunks.
- `APIPriorityAndFairness`: Enable managing request concurrency with
  prioritization and fairness at each server. (Renamed from `RequestManagement`)
- `APIResponseCompression`: Compress the API responses for `LIST` or `GET` requests.
- `APIServerIdentity`: Assign each API server an ID in a cluster.
-->
- `APIListChunking`：启用 API 客户端以块的形式从 API 服务器检索（“LIST” 或 “GET”）资源。
- `APIPriorityAndFairness`: 在每个服务器上启用优先级和公平性来管理请求并发。（由 `RequestManagement` 重命名而来）
- `APIResponseCompression`：压缩 “LIST” 或 “GET” 请求的 API 响应。
- `APIServerIdentity`：为集群中的每个 API 服务器赋予一个 ID。
<!--
- `Accelerators`: Enable Nvidia GPU support when using Docker
- `AdvancedAuditing`: Enable [advanced auditing](/docs/tasks/debug-application-cluster/audit/#advanced-audit)
- `AffinityInAnnotations`: Enable setting
  [Pod affinity or anti-affinity](/docs/concepts/scheduling-eviction/assign-pod-node/#affinity-and-anti-affinity).
- `AllowExtTrafficLocalEndpoints`: Enable a service to route external requests to node local endpoints.
- `AllowInsecureBackendProxy`: Enable the users to skip TLS verification of
  kubelets on Pod log requests.
- `AnyVolumeDataSource`: Enable use of any custom resource as the `DataSource` of a
  {{< glossary_tooltip text="PVC" term_id="persistent-volume-claim" >}}.
- `AppArmor`: Enable AppArmor based mandatory access control on Linux nodes when using Docker.
   See [AppArmor Tutorial](/docs/tutorials/clusters/apparmor/) for more details.
-->
- `Accelerators`：使用 Docker 时启用 Nvidia GPU 支持。
- `AdvancedAuditing`：启用[高级审计功能](/zh/docs/tasks/debug-application-cluster/audit/#advanced-audit)。
- `AffinityInAnnotations`：启用 [Pod 亲和或反亲和](/zh/docs/concepts/scheduling-eviction/assign-pod-node/#affinity-and-anti-affinity)。
- `AllowExtTrafficLocalEndpoints`：启用服务用于将外部请求路由到节点本地终端。
- `AllowInsecureBackendProxy`：允许用户在执行 Pod 日志访问请求时跳过 TLS 验证。
- `AnyVolumeDataSource`: 允许使用任何自定义的资源来做作为
  {{< glossary_tooltip text="PVC" term_id="persistent-volume-claim" >}} 中的 `DataSource`.
- `AppArmor`：使用 Docker 时，在 Linux 节点上启用基于 AppArmor 机制的强制访问控制。
  请参见 [AppArmor 教程](/zh/docs/tutorials/clusters/apparmor/) 获取详细信息。
<!--
- `AttachVolumeLimit`: Enable volume plugins to report limits on number of volumes
  that can be attached to a node.
  See [dynamic volume limits](/docs/concepts/storage/storage-limits/#dynamic-volume-limits) for more details.
- `BalanceAttachedNodeVolumes`: Include volume count on node to be considered for balanced resource allocation
  while scheduling. A node which has closer CPU, memory utilization, and volume count is favored by the scheduler
  while making decisions.
- `BlockVolume`: Enable the definition and consumption of raw block devices in Pods.
  See [Raw Block Volume Support](/docs/concepts/storage/persistent-volumes/#raw-block-volume-support)
   for more details.
- `BoundServiceAccountTokenVolume`: Migrate ServiceAccount volumes to use a projected volume consisting of a
  ServiceAccountTokenVolumeProjection. Cluster admins can use metric `serviceaccount_stale_tokens_total` to
  monitor workloads that are depending on the extended tokens. If there are no such workloads, turn off
  extended tokens by starting `kube-apiserver` with flag `--service-account-extend-token-expiration=false`.
  Check [Bound Service Account Tokens](https://github.com/kubernetes/enhancements/blob/master/keps/sig-auth/1205-bound-service-account-tokens/README.md)
  for more details.
-->
- `AttachVolumeLimit`：启用卷插件用于报告可连接到节点的卷数限制。有关更多详细信息，请参阅
  [动态卷限制](/zh/docs/concepts/storage/storage-limits/#dynamic-volume-limits)。
- `BalanceAttachedNodeVolumes`：在进行平衡资源分配的调度时，考虑节点上的卷数。
  调度器在决策时会优先考虑 CPU、内存利用率和卷数更近的节点。
- `BlockVolume`：在 Pod 中启用原始块设备的定义和使用。有关更多详细信息，请参见
  [原始块卷支持](/zh/docs/concepts/storage/persistent-volumes/#raw-block-volume-support)。
- `BoundServiceAccountTokenVolume`：迁移 ServiceAccount 卷以使用由
  ServiceAccountTokenVolumeProjection 组成的投射卷。集群管理员可以使用
  `serviceaccount_stale_tokens_total` 度量值来监控依赖于扩展令牌的负载。
  如果没有这种类型的负载，你可以在启动 `kube-apiserver` 时添加
  `--service-account-extend-token-expiration=false` 参数关闭扩展令牌。查看 
  [绑定服务账号令牌](https://github.com/kubernetes/enhancements/blob/master/keps/sig-auth/1205-bound-service-account-tokens/README.md)
  获取更多详细信息。
<!--
- `CPUManager`: Enable container level CPU affinity support, see
  [CPU Management Policies](/docs/tasks/administer-cluster/cpu-management-policies/).
- `CRIContainerLogRotation`: Enable container log rotation for CRI container runtime. The default max size of a log file is 10MB and the
  default max number of log files allowed for a container is 5. These values can be configured in the kubelet config.
  See the [logging at node level](/docs/concepts/cluster-administration/logging/#logging-at-the-node-level) documentation for more details.
- `CSIBlockVolume`: Enable external CSI volume drivers to support block storage.
  See the [`csi` raw block volume support](/docs/concepts/storage/volumes/#csi-raw-block-volume-support)
  documentation for more details.
- `CSIDriverRegistry`: Enable all logic related to the CSIDriver API object in
  csi.storage.k8s.io.
- `CSIInlineVolume`: Enable CSI Inline volumes support for pods.
- `CSIMigration`: Enables shims and translation logic to route volume
  operations from in-tree plugins to corresponding pre-installed CSI plugins
-->
- `CPUManager`：启用容器级别的 CPU 亲和性支持，有关更多详细信息，请参见
  [CPU 管理策略](/zh/docs/tasks/administer-cluster/cpu-management-policies/)。
- `CRIContainerLogRotation`：为 CRI 容器运行时启用容器日志轮换。日志文件的默认最大大小为10MB,缺省情况下，一个容器允许的最大日志文件数为5。这些值可以在kubelet配置中配置。
    更多细节请参见[日志架构]( /zh/docs/concepts/cluster-administration/logging/#logging-at-the-node-level)。
- `CSIBlockVolume`：启用外部 CSI 卷驱动程序用于支持块存储。有关更多详细信息，请参见
  [`csi` 原始块卷支持](/zh/docs/concepts/storage/volumes/#csi-raw-block-volume-support)。
- `CSIDriverRegistry`：在 csi.storage.k8s.io 中启用与 CSIDriver API 对象有关的所有逻辑。
- `CSIInlineVolume`：为 Pod 启用 CSI 内联卷支持。
- `CSIMigration`：确保封装和转换逻辑能够将卷操作从内嵌插件路由到相应的预安装 CSI 插件。
<!--
- `CSIMigrationAWS`: Enables shims and translation logic to route volume
  operations from the AWS-EBS in-tree plugin to EBS CSI plugin. Supports
  falling back to in-tree EBS plugin if a node does not have EBS CSI plugin
  installed and configured. Requires CSIMigration feature flag enabled.
- `CSIMigrationAWSComplete`: Stops registering the EBS in-tree plugin in
  kubelet and volume controllers and enables shims and translation logic to
  route volume operations from the AWS-EBS in-tree plugin to EBS CSI plugin.
  Requires CSIMigration and CSIMigrationAWS feature flags enabled and EBS CSI
  plugin installed and configured on all nodes in the cluster.
- `CSIMigrationAzureDisk`: Enables shims and translation logic to route volume
  operations from the Azure-Disk in-tree plugin to AzureDisk CSI plugin.
  Supports falling back to in-tree AzureDisk plugin if a node does not have
  AzureDisk CSI plugin installed and configured. Requires CSIMigration feature
  flag enabled.
- `CSIMigrationAzureDiskComplete`: Stops registering the Azure-Disk in-tree
  plugin in kubelet and volume controllers and enables shims and translation
  logic to route volume operations from the Azure-Disk in-tree plugin to
  AzureDisk CSI plugin. Requires CSIMigration and CSIMigrationAzureDisk feature
  flags enabled and AzureDisk CSI plugin installed and configured on all nodes
  in the cluster.
-->
- `CSIMigrationAWS`：确保填充和转换逻辑能够将卷操作从 AWS-EBS 内嵌插件路由到 EBS CSI 插件。
  如果节点未安装和配置 EBS CSI 插件，则支持回退到内嵌 EBS 插件。
  这需要启用 CSIMigration 特性标志。
- `CSIMigrationAWSComplete`：停止在 kubelet 和卷控制器中注册 EBS 内嵌插件，
  并启用 shims 和转换逻辑将卷操作从AWS-EBS 内嵌插件路由到 EBS CSI 插件。
  这需要启用 CSIMigration 和 CSIMigrationAWS 特性标志，并在集群中的所有节点上安装和配置
  EBS CSI 插件。
- `CSIMigrationAzureDisk`：确保填充和转换逻辑能够将卷操作从 Azure 磁盘内嵌插件路由到
  Azure 磁盘 CSI 插件。如果节点未安装和配置 AzureDisk CSI 插件，
  支持回退到内建 AzureDisk 插件。这需要启用 CSIMigration 特性标志。
- `CSIMigrationAzureDiskComplete`：停止在 kubelet 和卷控制器中注册 Azure 磁盘内嵌插件，
  并启用 shims 和转换逻辑以将卷操作从 Azure 磁盘内嵌插件路由到 AzureDisk CSI 插件。
  这需要启用 CSIMigration 和 CSIMigrationAzureDisk 特性标志，
  并在集群中的所有节点上安装和配置 AzureDisk CSI 插件。
<!--
- `CSIMigrationAzureFile`: Enables shims and translation logic to route volume
  operations from the Azure-File in-tree plugin to AzureFile CSI plugin.
  Supports falling back to in-tree AzureFile plugin if a node does not have
  AzureFile CSI plugin installed and configured. Requires CSIMigration feature
  flag enabled.
- `CSIMigrationAzureFileComplete`: Stops registering the Azure-File in-tree
  plugin in kubelet and volume controllers and enables shims and translation
  logic to route volume operations from the Azure-File in-tree plugin to
  AzureFile CSI plugin. Requires CSIMigration and CSIMigrationAzureFile feature
  flags  enabled and AzureFile CSI plugin installed and configured on all nodes
  in the cluster.
-->
- `CSIMigrationAzureFile`：确保封装和转换逻辑能够将卷操作从 Azure 文件内嵌插件路由到
  Azure 文件 CSI 插件。如果节点未安装和配置 AzureFile CSI 插件，
  支持回退到内嵌 AzureFile 插件。这需要启用 CSIMigration 特性标志。
- `CSIMigrationAzureFileComplete`：停止在 kubelet 和卷控制器中注册 Azure-File 内嵌插件，
  并启用 shims 和转换逻辑以将卷操作从 Azure-File 内嵌插件路由到 AzureFile CSI 插件。
  这需要启用 CSIMigration 和 CSIMigrationAzureFile 特性标志，
  并在集群中的所有节点上安装和配置 AzureFile CSI 插件。
<!--
- `CSIMigrationGCE`: Enables shims and translation logic to route volume
  operations from the GCE-PD in-tree plugin to PD CSI plugin. Supports falling
  back to in-tree GCE plugin if a node does not have PD CSI plugin installed and
  configured. Requires CSIMigration feature flag enabled.
- `CSIMigrationGCEComplete`: Stops registering the GCE-PD in-tree plugin in
  kubelet and volume controllers and enables shims and translation logic to
  route volume operations from the GCE-PD in-tree plugin to PD CSI plugin.
  Requires CSIMigration and CSIMigrationGCE feature flags enabled and PD CSI
  plugin installed and configured on all nodes in the cluster.
-->
- `CSIMigrationGCE`：启用 shims 和转换逻辑，将卷操作从 GCE-PD 内嵌插件路由到
  PD CSI 插件。如果节点未安装和配置 PD CSI 插件，支持回退到内嵌 GCE 插件。
  这需要启用 CSIMigration 特性标志。
- `CSIMigrationGCEComplete`：停止在 kubelet 和卷控制器中注册 GCE-PD 内嵌插件，
  并启用 shims 和转换逻辑以将卷操作从 GCE-PD 内嵌插件路由到 PD CSI 插件。
  这需要启用 CSIMigration 和 CSIMigrationGCE 特性标志，并在集群中的所有节点上
  安装和配置 PD CSI 插件。
<!--
- `CSIMigrationOpenStack`: Enables shims and translation logic to route volume
  operations from the Cinder in-tree plugin to Cinder CSI plugin. Supports
  falling back to in-tree Cinder plugin if a node does not have Cinder CSI
  plugin installed and configured. Requires CSIMigration feature flag enabled.
- `CSIMigrationOpenStackComplete`: Stops registering the Cinder in-tree plugin in
  kubelet and volume controllers and enables shims and translation logic to route
  volume operations from the Cinder in-tree plugin to Cinder CSI plugin.
  Requires CSIMigration and CSIMigrationOpenStack feature flags enabled and Cinder
  CSI plugin installed and configured on all nodes in the cluster.
-->
- `CSIMigrationOpenStack`：确保填充和转换逻辑能够将卷操作从 Cinder 内嵌插件路由到
  Cinder CSI 插件。如果节点未安装和配置 Cinder CSI 插件，支持回退到内嵌 Cinder 插件。
  这需要启用 CSIMigration 特性标志。
- `CSIMigrationOpenStackComplete`：停止在 kubelet 和卷控制器中注册 Cinder 内嵌插件，
  并启用 shims 和转换逻辑将卷操作从 Cinder 内嵌插件路由到 Cinder CSI 插件。
  这需要启用 CSIMigration 和 CSIMigrationOpenStack 特性标志，并在集群中的所有节点上
  安装和配置 Cinder CSI 插件。
<!--
- `CSIMigrationvSphere`: Enables shims and translation logic to route volume operations
  from the vSphere in-tree plugin to vSphere CSI plugin.
  Supports falling back to in-tree vSphere plugin if a node does not have vSphere
  CSI plugin installed and configured. Requires CSIMigration feature flag enabled.
- `CSIMigrationvSphereComplete`: Stops registering the vSphere in-tree plugin in kubelet
  and volume controllers and enables shims and translation logic to route volume operations
  from the vSphere in-tree plugin to vSphere CSI plugin. Requires CSIMigration and
  CSIMigrationvSphere feature flags enabled and vSphere CSI plugin installed and
  configured on all nodes in the cluster.
-->
- `CSIMigrationvSphere`: 允许封装和转换逻辑将卷操作从 vSphere 内嵌插件路由到
  vSphere CSI 插件。如果节点未安装和配置 vSphere CSI 插件，则支持回退到
  vSphere 内嵌插件。这需要启用 CSIMigration 特性标志。
- `CSIMigrationvSphereComplete`: 停止在 kubelet 和卷控制器中注册 vSphere 内嵌插件，
  并启用 shims 和转换逻辑以将卷操作从 vSphere 内嵌插件路由到 vSphere CSI 插件。
  这需要启用 CSIMigration 和 CSIMigrationvSphere 特性标志，并在集群中的所有节点上
  安装和配置 vSphere CSI 插件。
<!--
- `CSINodeInfo`: Enable all logic related to the CSINodeInfo API object in csi.storage.k8s.io.
- `CSIPersistentVolume`: Enable discovering and mounting volumes provisioned through a
  [CSI (Container Storage Interface)](https://github.com/kubernetes/community/blob/master/contributors/design-proposals/storage/container-storage-interface.md)
  compatible volume plugin.
- `CSIServiceAccountToken`: Enable CSI drivers to receive the pods' service account token
  that they mount volumes for. See
  [Token Requests](https://kubernetes-csi.github.io/docs/token-requests.html).
- `CSIStorageCapacity`: Enables CSI drivers to publish storage capacity information
  and the Kubernetes scheduler to use that information when scheduling pods. See
  [Storage Capacity](/docs/concepts/storage/storage-capacity/).
  Check the [`csi` volume type](/docs/concepts/storage/volumes/#csi) documentation for more details.
-->
- `CSINodeInfo`：在 csi.storage.k8s.io 中启用与 CSINodeInfo API 对象有关的所有逻辑。
- `CSIPersistentVolume`：启用发现和挂载通过
  [CSI（容器存储接口）](https://github.com/kubernetes/community/blob/master/contributors/design-proposals/storage/container-storage-interface.md)
  兼容卷插件配置的卷。
- `CSIServiceAccountToken`: 允许 CSI 驱动接收挂载卷目标 Pods 的服务账户令牌。
  参阅[令牌请求（Token Requests）](https://kubernetes-csi.github.io/docs/token-requests.html)。
- `CSIStorageCapacity`: 使 CSI 驱动程序可以发布存储容量信息，并使 Kubernetes
  调度程序在调度 Pod 时使用该信息。参见
  [存储容量](/zh/docs/concepts/storage/storage-capacity/)。
  详情请参见 [`csi` 卷类型](/zh/docs/concepts/storage/volumes/#csi)。
<!--
- `CSIVolumeFSGroupPolicy`: Allows CSIDrivers to use the `fsGroupPolicy` field.
  This field controls whether volumes created by a CSIDriver support volume ownership
  and permission modifications when these volumes are mounted.
- `CSIVolumeHealth`: Enable support for CSI volume health monitoring on node.
- `ConfigurableFSGroupPolicy`: Allows user to configure volume permission change policy
  for fsGroups when mounting a volume in a Pod. See
  [Configure volume permission and ownership change policy for Pods](/docs/tasks/configure-pod-container/security-context/#configure-volume-permission-and-ownership-change-policy-for-pods)
  for more details.
- `CronJobControllerV2`: Use an alternative implementation of the
  {{< glossary_tooltip text="CronJob" term_id="cronjob" >}} controller. Otherwise,
  version 1 of the same controller is selected.
  The version 2 controller provides experimental performance improvements.
-->
- `CSIVolumeFSGroupPolicy`: 允许 CSIDrivers 使用 `fsGroupPolicy` 字段. 
  该字段能控制由 CSIDriver 创建的卷在挂载这些卷时是否支持卷所有权和权限修改。
- `CSIVolumeHealth`: 启用对节点上的 CSI volume 运行状况监控的支持
- `ConfigurableFSGroupPolicy`：在 Pod 中挂载卷时，允许用户为 fsGroup
  配置卷访问权限和属主变更策略。请参见
  [为 Pod 配置卷访问权限和属主变更策略](/zh/docs/tasks/configure-pod-container/security-context/#configure-volume-permission-and-ownership-change-policy-for-pods)。
- `CronJobControllerV2`：使用 {{< glossary_tooltip text="CronJob" term_id="cronjob" >}}
  控制器的一种替代实现。否则，系统会选择同一控制器的 v1 版本。
  控制器的 v2 版本提供试验性的性能改进。
<!--
- `CustomCPUCFSQuotaPeriod`: Enable nodes to change `cpuCFSQuotaPeriod` in
  [kubelet config](/docs/tasks/administer-cluster/kubelet-config-file/).
- `CustomPodDNS`: Enable customizing the DNS settings for a Pod using its `dnsConfig` property.
   Check [Pod's DNS Config](/docs/concepts/services-networking/dns-pod-service/#pods-dns-config)
   for more details.
- `CustomResourceDefaulting`: Enable CRD support for default values in OpenAPI v3 validation schemas.
- `CustomResourcePublishOpenAPI`: Enables publishing of CRD OpenAPI specs.
- `CustomResourceSubresources`: Enable `/status` and `/scale` subresources
  on resources created from [CustomResourceDefinition](/docs/concepts/extend-kubernetes/api-extension/custom-resources/).
- `CustomResourceValidation`: Enable schema based validation on resources created from
  [CustomResourceDefinition](/docs/concepts/extend-kubernetes/api-extension/custom-resources/).
- `CustomResourceWebhookConversion`: Enable webhook-based conversion
  on resources created from [CustomResourceDefinition](/docs/concepts/extend-kubernetes/api-extension/custom-resources/).
-->
- `CustomCPUCFSQuotaPeriod`：使节点能够更改
  [kubelet 配置](/zh/docs/tasks/administer-cluster/kubelet-config-file/).
  中的 `cpuCFSQuotaPeriod`。
- `CustomPodDNS`：允许使用 Pod 的 `dnsConfig` 属性自定义其 DNS 设置。
  更多详细信息，请参见
  [Pod 的 DNS 配置](/zh/docs/concepts/services-networking/dns-pod-service/#pods-dns-config)。
- `CustomResourceDefaulting`：为 CRD 启用在其 OpenAPI v3 验证模式中提供默认值的支持。
- `CustomResourcePublishOpenAPI`：启用 CRD OpenAPI 规范的发布。
- `CustomResourceSubresources`：对于用
  [CustomResourceDefinition](/zh/docs/concepts/extend-kubernetes/api-extension/custom-resources/)
  创建的资源启用其 `/status` 和 `/scale` 子资源。
- `CustomResourceValidation`：对于用
  [CustomResourceDefinition](/zh/docs/concepts/extend-kubernetes/api-extension/custom-resources/)
  创建的资源启用基于模式的验证。
- `CustomResourceWebhookConversion`：对于用
  [CustomResourceDefinition](/zh/docs/concepts/extend-kubernetes/api-extension/custom-resources/)
  创建的资源启用基于 Webhook 的转换。
<!--
- `DefaultPodTopologySpread`: Enables the use of `PodTopologySpread` scheduling plugin to do
  [default spreading](/docs/concepts/workloads/pods/pod-topology-spread-constraints/#internal-default-constraints).
- `DevicePlugins`: Enable the [device-plugins](/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/)
  based resource provisioning on nodes.
- `DisableAcceleratorUsageMetrics`:
  [Disable accelerator metrics collected by the kubelet](/docs/concepts/cluster-administration/system-metrics/#disable-accelerator-metrics).
- `DownwardAPIHugePages`: Enables usage of hugepages in
  [downward API](/docs/tasks/inject-data-application/downward-api-volume-expose-pod-information).
- `DryRun`: Enable server-side [dry run](/docs/reference/using-api/api-concepts/#dry-run) requests
  so that validation, merging, and mutation can be tested without committing.
- `DynamicAuditing`: Used to enable dynamic auditing before v1.19.
-->
- `DefaultPodTopologySpread`: 启用 `PodTopologySpread` 调度插件来完成
  [默认的调度传播](/zh/docs/concepts/workloads/pods/pod-topology-spread-constraints/#internal-default-constraints).
- `DevicePlugins`：在节点上启用基于
  [设备插件](/zh/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/)的
  资源制备。
- `DisableAcceleratorUsageMetrics`： 
  [禁用 kubelet 收集加速器指标](/zh/docs/concepts/cluster-administration/system-metrics/#disable-accelerator-metrics).
- `DownwardAPIHugePages`：允许在
  [下行（Downward）API](/zh/docs/tasks/inject-data-application/downward-api-volume-expose-pod-information)
  中使用巨页信息。
- `DryRun`：启用在服务器端对请求进行
  [彩排（Dry Run）](/zh/docs/reference/using-api/api-concepts/#dry-run)，
  以便测试验证、合并和修改，同时避免提交更改。
- `DynamicAuditing`：在 v1.19 版本前用于启用动态审计。
<!--
- `DynamicKubeletConfig`: Enable the dynamic configuration of kubelet. See
  [Reconfigure kubelet](/docs/tasks/administer-cluster/reconfigure-kubelet/).
- `DynamicProvisioningScheduling`: Extend the default scheduler to be aware of
  volume topology and handle PV provisioning.
  This feature is superseded by the `VolumeScheduling` feature completely in v1.12.
- `DynamicVolumeProvisioning`: Enable the
  [dynamic provisioning](/docs/concepts/storage/dynamic-provisioning/) of persistent volumes to Pods.
- `EfficientWatchResumption`: Allows for storage-originated bookmark (progress
  notify) events to be delivered to the users. This is only applied to watch
  operations.
- `EnableAggregatedDiscoveryTimeout`: Enable the five second
  timeout on aggregated discovery calls.
-->
- `DynamicKubeletConfig`：启用 kubelet 的动态配置。请参阅
  [重新配置 kubelet](/zh/docs/tasks/administer-cluster/reconfigure-kubelet/)。
- `DynamicProvisioningScheduling`：扩展默认调度器以了解卷拓扑并处理 PV 配置。
  此特性已在 v1.12 中完全被 `VolumeScheduling` 特性取代。
- `DynamicVolumeProvisioning`：启用持久化卷到 Pod 的
  [动态预配置](/zh/docs/concepts/storage/dynamic-provisioning/)。
- `EfficientWatchResumption`：允许从存储发起的 bookmark（进度通知）事件被
  通知到用户。此特性仅适用于 watch 操作。
- `EnableAggregatedDiscoveryTimeout`：对聚集的发现调用启用五秒钟超时设置。
<!--
- `EnableEquivalenceClassCache`: Enable the scheduler to cache equivalence of
  nodes when scheduling Pods.
- `EndpointSlice`: Enables EndpointSlices for more scalable and extensible
   network endpoints. See [Enabling EndpointSlices](/docs/tasks/administer-cluster/enabling-endpointslices/).
- `EndpointSliceNodeName`: Enables EndpointSlice `nodeName` field.
- `EndpointSliceProxying`: When enabled, kube-proxy running
   on Linux will use EndpointSlices as the primary data source instead of
   Endpoints, enabling scalability and performance improvements. See
   [Enabling Endpoint Slices](/docs/tasks/administer-cluster/enabling-endpointslices/).
- `EndpointSliceTerminatingCondition`: Enables EndpointSlice `terminating` and `serving`
   condition fields.
-->
- `EnableEquivalenceClassCache`：调度 Pod 时，使 scheduler 缓存节点的等效项。
- `EndpointSlice`：启用 EndpointSlice 以实现可扩缩性和可扩展性更好的网络端点。
   参阅[启用 EndpointSlice](/zh/docs/tasks/administer-cluster/enabling-endpointslices/)。
- `EndpointSliceNodeName`：允许使用 EndpointSlice 的 `nodeName` 字段。
- `EndpointSliceProxying`：启用此特性门控时，Linux 上运行的 kube-proxy 会使用
   EndpointSlices 而不是 Endpoints 作为其主要数据源，从而使得可扩缩性和性能
   提升成为可能。参阅
   [启用 EndpointSlice](/zh/docs/tasks/administer-cluster/enabling-endpointslices/)。
- `EndpointSliceTerminatingCondition`：允许使用 EndpointSlice 的 `terminating` 和
  `serving` 状况字段。
<!--
- `EphemeralContainers`: Enable the ability to add
  {{< glossary_tooltip text="ephemeral containers" term_id="ephemeral-container" >}}
  to running pods.
- `EvenPodsSpread`: Enable pods to be scheduled evenly across topology domains. See
  [Pod Topology Spread Constraints](/docs/concepts/workloads/pods/pod-topology-spread-constraints/).
- `ExecProbeTimeout`: Ensure kubelet respects exec probe timeouts.
  This feature gate exists in case any of your existing workloads depend on a
  now-corrected fault where Kubernetes ignored exec probe timeouts. See
  [readiness probes](/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/#configure-probes).
-->
- `EphemeralContainers`：启用添加
  {{< glossary_tooltip text="临时容器" term_id="ephemeral-container" >}}
  到正在运行的 Pod 的特性。
- `EvenPodsSpread`：使 Pod 能够在拓扑域之间平衡调度。请参阅
  [Pod 拓扑扩展约束](/zh/docs/concepts/workloads/pods/pod-topology-spread-constraints/)。
- `ExecProbeTimeout`：确保 kubelet 会遵从 exec 探针的超时值设置。
  此特性门控的主要目的是方便你处理现有的、依赖于已被修复的缺陷的工作负载；
  该缺陷导致 Kubernetes 会忽略 exec 探针的超时值设置。
  参阅[就绪态探针](/zh/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/#configure-probes).
<!--
- `ExpandCSIVolumes`: Enable the expanding of CSI volumes.
- `ExpandInUsePersistentVolumes`: Enable expanding in-use PVCs. See
  [Resizing an in-use PersistentVolumeClaim](/docs/concepts/storage/persistent-volumes/#resizing-an-in-use-persistentvolumeclaim).
- `ExpandPersistentVolumes`: Enable the expanding of persistent volumes. See
  [Expanding Persistent Volumes Claims](/docs/concepts/storage/persistent-volumes/#expanding-persistent-volumes-claims).
- `ExperimentalCriticalPodAnnotation`: Enable annotating specific pods as *critical*
  so that their [scheduling is guaranteed](/docs/tasks/administer-cluster/guaranteed-scheduling-critical-addon-pods/).
  This feature is deprecated by Pod Priority and Preemption as of v1.13.
-->
- `ExpandCSIVolumes`: 启用扩展 CSI 卷。
- `ExpandInUsePersistentVolumes`：启用扩充使用中的 PVC 的尺寸。请查阅
  [调整使用中的 PersistentVolumeClaim 的大小](/zh/docs/concepts/storage/persistent-volumes/#resizing-an-in-use-persistentvolumeclaim)。
- `ExpandPersistentVolumes`：允许扩充持久卷。请查阅
  [扩展持久卷申领](/zh/docs/concepts/storage/persistent-volumes/#expanding-persistent-volumes-claims)。
- `ExperimentalCriticalPodAnnotation`：启用将特定 Pod 注解为 *critical* 的方式，用于
  [确保其被调度](/zh/docs/tasks/administer-cluster/guaranteed-scheduling-critical-addon-pods/)。
  从 v1.13 开始已弃用此特性，转而使用 Pod 优先级和抢占功能。
<!--
- `ExperimentalHostUserNamespaceDefaulting`: Enabling the defaulting user
   namespace to host. This is for containers that are using other host namespaces,
   host mounts, or containers that are privileged or using specific non-namespaced
   capabilities (e.g. `MKNODE`, `SYS_MODULE` etc.). This should only be enabled
   if user namespace remapping is enabled in the Docker daemon.
- `ExternalPolicyForExternalIP`: Fix a bug where ExternalTrafficPolicy is not applied to Service ExternalIPs.
- `GCERegionalPersistentDisk`: Enable the regional PD feature on GCE.
- `GenericEphemeralVolume`: Enables ephemeral, inline volumes that support all features
  of normal volumes (can be provided by third-party storage vendors, storage capacity tracking,
  restore from snapshot, etc.).
  See [Ephemeral Volumes](/docs/concepts/storage/ephemeral-volumes/).
- `GracefulNodeShutdown`: Enables support for graceful shutdown in kubelet.
  During a system shutdown, kubelet will attempt to detect the shutdown event
  and gracefully terminate pods running on the node. See
  [Graceful Node Shutdown](/docs/concepts/architecture/nodes/#graceful-node-shutdown)
  for more details.
-->
- `ExperimentalHostUserNamespaceDefaulting`：启用主机默认的用户名字空间。
  这适用于使用其他主机名字空间、主机安装的容器，或具有特权或使用特定的非名字空间功能
  （例如 MKNODE、SYS_MODULE 等）的容器。
  如果在 Docker 守护程序中启用了用户名字空间重新映射，则启用此选项。
- `ExternalPolicyForExternalIP`： 修复 ExternalPolicyForExternalIP 没有应用于 Service ExternalIPs 的 bug。
- `GCERegionalPersistentDisk`：在 GCE 上启用带地理区域信息的 PD 特性。
- `GenericEphemeralVolume`：启用支持临时的内联卷，这些卷支持普通卷
  （可以由第三方存储供应商提供、存储容量跟踪、从快照还原等等）的所有功能。请参见
  [临时卷](/zh/docs/concepts/storage/ephemeral-volumes/)。
- `GracefulNodeShutdown`：在 kubelet 中启用体面地关闭节点的支持。
  在系统关闭时，kubelet 会尝试监测该事件并体面地终止节点上运行的 Pods。参阅
  [体面地关闭节点](/zh/docs/concepts/architecture/nodes/#graceful-node-shutdown)
  以了解更多细节。
<!--
- `HPAContainerMetrics`: Enable the `HorizontalPodAutoscaler` to scale based on
  metrics from individual containers in target pods.
- `HPAScaleToZero`: Enables setting `minReplicas` to 0 for `HorizontalPodAutoscaler`
  resources when using custom or external metrics.
- `HugePages`: Enable the allocation and consumption of pre-allocated
  [huge pages](/docs/tasks/manage-hugepages/scheduling-hugepages/).
- `HugePageStorageMediumSize`: Enable support for multiple sizes pre-allocated
  [huge pages](/docs/tasks/manage-hugepages/scheduling-hugepages/).
-->
- `HPAContainerMetrics`：允许 `HorizontalPodAutoscaler` 基于目标 Pods 中各容器
  的度量值来执行扩缩操作。
- `HPAScaleToZero`：使用自定义指标或外部指标时，可将 `HorizontalPodAutoscaler`
  资源的 `minReplicas` 设置为 0。
- `HugePages`：启用分配和使用预分配的
  [巨页资源](/zh/docs/tasks/manage-hugepages/scheduling-hugepages/)。
- `HugePageStorageMediumSize`：启用支持多种大小的预分配
  [巨页资源](/zh/docs/tasks/manage-hugepages/scheduling-hugepages/)。

<!--
- `HyperVContainer`: Enable
  [Hyper-V isolation](https://docs.microsoft.com/en-us/virtualization/windowscontainers/manage-containers/hyperv-container)
  for Windows containers.
- `ImmutableEphemeralVolumes`: Allows for marking individual Secrets and ConfigMaps as
  immutable for better safety and performance.
- `IPv6DualStack`: Enable [dual stack](/docs/concepts/services-networking/dual-stack/)
  support for IPv6.
- `IndexedJob`: Allows the [Job](/docs/concepts/workloads/controllers/job/)
  controller to manage Pod completions per completion index.
- `IngressClassNamespacedParams`: Allow namespace-scoped parameters reference in
  `IngressClass` resource. This feature adds two fields - `Scope` and `Namespace`
  to `IngressClass.spec.parameters`.
- `Initializers`: Allow asynchronous coordination of object creation using the
  Initializers admission plugin.
- `KubeletConfigFile`: Enable loading kubelet configuration 
  from a file specified using a config file.
  See [setting kubelet parameters via a config file](/docs/tasks/administer-cluster/kubelet-config-file/)
  for more details.
- `KubeletCredentialProviders`: Enable kubelet exec credential providers for image pull credentials.
- `KubeletPluginsWatcher`: Enable probe-based plugin watcher utility to enable kubelet
  to discover plugins such as [CSI volume drivers](/docs/concepts/storage/volumes/#csi).
-->
- `HyperVContainer`：为 Windows 容器启用
  [Hyper-V 隔离](https://docs.microsoft.com/en-us/virtualization/windowscontainers/manage-containers/hyperv-container)。
- `ImmutableEphemeralVolumes`：允许将各个 Secret 和 ConfigMap 标记为不可变更的，
  以提高安全性和性能。
- `IPv6DualStack`：启用[双协议栈](/zh/docs/concepts/services-networking/dual-stack/)
  以支持 IPv6。
- `IndexedJob`：允许 [Job](/zh/docs/concepts/workloads/controllers/job/) 控制器按每个完成的索引去管理 Pod 完成。
- `IngressClassNamespacedParams`：允许引用命名空间范围的参数引用 `IngressClass`资源。该特性增加了两个字段 —— `Scope` 和 `Namespace` 到 `IngressClass.spec.parameters`。
- `Initializers`： 使用 Initializers 准入插件允许异步协调对象创建。
- `KubeletConfigFile`：启用从使用配置文件指定的文件中加载 kubelet 配置。
  有关更多详细信息，请参见
  [通过配置文件设置 kubelet 参数](/zh/docs/tasks/administer-cluster/kubelet-config-file/)。
- `KubeletCredentialProviders`：允许使用 kubelet exec 凭据提供程序来设置
  镜像拉取凭据。
- `KubeletPluginsWatcher`：启用基于探针的插件监视应用程序，使 kubelet 能够发现
  类似 [CSI 卷驱动程序](/zh/docs/concepts/storage/volumes/#csi)这类插件。
<!--
- `KubeletPodResources`: Enable the kubelet's pod resources gRPC endpoint. See
  [Support Device Monitoring](https://github.com/kubernetes/enhancements/blob/master/keps/sig-node/606-compute-device-assignment/README.md)
  for more details.
- `KubeletPodResourcesGetAllocatable`: Enable the kubelet's pod resources `GetAllocatableResources` functionality.
  This API augments the [resource allocation reporting](/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/#monitoring-device-plugin-resources)
  with informations about the allocatable resources, enabling clients to properly track the free compute resources on a node.
- `LegacyNodeRoleBehavior`: When disabled, legacy behavior in service load balancers and
  node disruption will ignore the `node-role.kubernetes.io/master` label in favor of the
  feature-specific labels provided by `NodeDisruptionExclusion` and `ServiceNodeExclusion`.
-->
- `KubeletPodResources`：启用 kubelet 的 Pod 资源 GRPC 端点。更多详细信息，请参见
  [支持设备监控](https://github.com/kubernetes/enhancements/blob/master/keps/sig-node/compute-device-assignment.md)。
- `KubeletPodResourcesGetAllocatable`：启用 kubelet 的 pod 资源 `GetAllocatableResources` 功能。
  该 API 增强了[资源分配报告]（/zh/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/#monitoring-device-plugin-resources）
  包含有关可分配资源的信息，使客户端能够正确跟踪节点上的可用计算资源。
- `LegacyNodeRoleBehavior`：禁用此门控时，服务负载均衡器中和节点干扰中的原先行为
  会忽略 `node-role.kubernetes.io/master` 标签，使用 `NodeDisruptionExclusion` 和
  `ServiceNodeExclusion` 对应特性所提供的标签。
<!--
- `LocalStorageCapacityIsolation`: Enable the consumption of
  [local ephemeral storage](/docs/concepts/configuration/manage-resources-containers/)
  and also the `sizeLimit` property of an
  [emptyDir volume](/docs/concepts/storage/volumes/#emptydir).
- `LocalStorageCapacityIsolationFSQuotaMonitoring`: When `LocalStorageCapacityIsolation`
  is enabled for
  [local ephemeral storage](/docs/concepts/configuration/manage-resources-containers/)
  and the backing filesystem for [emptyDir volumes](/docs/concepts/storage/volumes/#emptydir)
  supports project quotas and they are enabled, use project quotas to monitor
  [emptyDir volume](/docs/concepts/storage/volumes/#emptydir) storage consumption rather than
  filesystem walk for better performance and accuracy.
- `LogarithmicScaleDown`: Enable semi-random selection of pods to evict on controller scaledown
  based on logarithmic bucketing of pod timestamps.
- `MixedProtocolLBService`: Enable using different protocols in the same `LoadBalancer` type
  Service instance.
- `MountContainers`: Enable using utility containers on host as
  the volume mounter.
-->
- `LocalStorageCapacityIsolation`：允许使用
  [本地临时存储](/zh/docs/concepts/configuration/manage-resources-containers/)
  以及 [emptyDir 卷](/zh/docs/concepts/storage/volumes/#emptydir) 的 `sizeLimit` 属性。
- `LocalStorageCapacityIsolationFSQuotaMonitoring`：如果
  [本地临时存储](/zh/docs/concepts/configuration/manage-resources-containers/)
  启用了 `LocalStorageCapacityIsolation`，并且
  [emptyDir 卷](/zh/docs/concepts/storage/volumes/#emptydir)
  的后备文件系统支持项目配额，并且启用了这些配额，将使用项目配额来监视
  [emptyDir 卷](/zh/docs/concepts/storage/volumes/#emptydir)的存储消耗
  而不是遍历文件系统，以此获得更好的性能和准确性。
- `LogarithmicScaleDown`：启用Pod的半随机（semi-random）选择，控制器将根据 Pod 时间戳的对数桶按比例缩小去驱逐 Pod。
- `MixedProtocolLBService`：允许在同一 `LoadBalancer` 类型的 Service 实例中使用不同
  的协议。
- `MountContainers`：允许使用主机上的工具容器作为卷挂载程序。
<!--
- `MountPropagation`: Enable sharing volume mounted by one container to other containers or pods.
  For more details, please see [mount propagation](/docs/concepts/storage/volumes/#mount-propagation).
- `NamespaceDefaultLabelName`: Configure the API Server to set an immutable {{< glossary_tooltip text="label" term_id="label" >}}
  `kubernetes.io/metadata.name` on all namespaces, containing the namespace name.
- `NetworkPolicyEndPort`: Enable use of the field `endPort` in NetworkPolicy objects, allowing the selection of a port range instead of a single port.
- `NodeDisruptionExclusion`: Enable use of the node label `node.kubernetes.io/exclude-disruption`
  which prevents nodes from being evacuated during zone failures.
- `NodeLease`: Enable the new Lease API to report node heartbeats, which could be used as a node health signal.
- `NonPreemptingPriority`: Enable `preemptionPolicy` field for PriorityClass and Pod.
- `PVCProtection`: Enable the prevention of a PersistentVolumeClaim (PVC) from
  being deleted when it is still used by any Pod.
- `PodDeletionCost`: Enable the [Pod Deletion Cost](/docs/content/en/docs/concepts/workloads/controllers/replicaset/#pod-deletion-cost)
   feature which allows users to influence ReplicaSet downscaling order.
- `PersistentLocalVolumes`: Enable the usage of `local` volume type in Pods.
  Pod affinity has to be specified if requesting a `local` volume.
- `PodDisruptionBudget`: Enable the [PodDisruptionBudget](/docs/tasks/run-application/configure-pdb/) feature.
- `PodAffinityNamespaceSelector`: Enable the [Pod Affinity Namespace Selector](/docs/concepts/scheduling-eviction/assign-pod-node/#namespace-selector)
  and [CrossNamespacePodAffinity](/docs/concepts/policy/resource-quotas/#cross-namespace-pod-affinity-quota) quota scope features.
- `PodOverhead`: Enable the [PodOverhead](/docs/concepts/scheduling-eviction/pod-overhead/)
  feature to account for pod overheads.
-->
- `MountPropagation`：启用将一个容器安装的共享卷共享到其他容器或 Pod。
  更多详细信息，请参见[挂载传播](/zh/docs/concepts/storage/volumes/#mount-propagation)。
- `NamespaceDefaultLabelName`：配置 API 服务器以在所有名字空间上设置一个不可变的 {{< glossary_tooltip text="label" term_id="label" >}} 
   `kubernetes.io/metadata.name`，也包括名字空间。
- `NodeDisruptionExclusion`：启用节点标签 `node.kubernetes.io/exclude-disruption`，
  以防止在可用区发生故障期间驱逐节点。
- `NodeLease`：启用新的 Lease（租期）API 以报告节点心跳，可用作节点运行状况信号。
- `NonPreemptingPriority`：为 PriorityClass 和 Pod 启用 `preemptionPolicy` 选项。
- `PVCProtection`：启用防止仍被某 Pod 使用的 PVC 被删除的特性。
- `PodDeletionCost`：启用[Pod 删除成本](/zh/docs/concepts/workloads/controllers/replicaset/#pod-deletion-cost)功能。
  该功能使用户可以影响 ReplicaSet 的降序顺序。
- `PersistentLocalVolumes`：允许在 Pod 中使用 `local（本地）`卷类型。
  如果请求 `local` 卷，则必须指定 Pod 亲和性属性。
- `PodDisruptionBudget`：启用 [PodDisruptionBudget](/zh/docs/tasks/run-application/configure-pdb/) 特性。
- `PodAffinityNamespaceSelector`：启用[Pod 亲和性名称空间选择器](/zh/docs/concepts/scheduling-eviction/assign-pod-node/#namespace-selector)
   和[CrossNamespacePodAffinity](/zh/docs/concepts/policy/resource-quotas/#cross-namespace-pod-affinity-quota)资源配额功能。
- `PodOverhead`：启用 [PodOverhead](/zh/docs/concepts/scheduling-eviction/pod-overhead/)
  特性以考虑 Pod 开销。
<!--
- `PodPriority`: Enable the descheduling and preemption of Pods based on their
  [priorities](/docs/concepts/configuration/pod-priority-preemption/).
- `PodReadinessGates`: Enable the setting of `PodReadinessGate` field for extending
  Pod readiness evaluation.  See [Pod readiness gate](/docs/concepts/workloads/pods/pod-lifecycle/#pod-readiness-gate)
  for more details.
- `PodShareProcessNamespace`: Enable the setting of `shareProcessNamespace` in a Pod for sharing
  a single process namespace between containers running in a pod.  More details can be found in
  [Share Process Namespace between Containers in a Pod](/docs/tasks/configure-pod-container/share-process-namespace/).
- `ProbeTerminationGracePeriod`: Enable [setting probe-level
  `terminationGracePeriodSeconds`](/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/#probe-level-terminationgraceperiodseconds)
   on pods.  See the [enhancement proposal](https://github.com/kubernetes/enhancements/tree/master/keps/sig-node/2238-liveness-probe-grace-period) for more details.
- `ProcMountType`: Enables control over the type proc mounts for containers
  by setting the `procMount` field of a SecurityContext.
- `QOSReserved`: Allows resource reservations at the QoS level preventing pods
  at lower QoS levels from bursting into resources requested at higher QoS levels
  (memory only for now).
- `RemainingItemCount`: Allow the API servers to show a count of remaining
  items in the response to a
  [chunking list request](/docs/reference/using-api/api-concepts/#retrieving-large-results-sets-in-chunks).
-->
- `PodPriority`：根据[优先级](/zh/docs/concepts/configuration/pod-priority-preemption/)
  启用 Pod 的调度和抢占。
- `PodReadinessGates`：启用 `podReadinessGate` 字段的设置以扩展 Pod 准备状态评估。
  有关更多详细信息，请参见
  [Pod 就绪状态判别](/zh/docs/concepts/workloads/pods/pod-lifecycle/#pod-readiness-gate)。
- `PodShareProcessNamespace`：在 Pod 中启用 `shareProcessNamespace` 的设置，
  以便在 Pod 中运行的容器之间共享同一进程名字空间。更多详细信息，请参见
  [在 Pod 中的容器间共享同一进程名字空间](/zh/docs/tasks/configure-pod-container/share-process-namespace/)。
- `ProbeTerminationGracePeriod`：在 Pod 上 启用 
  [设置探测器级别 `terminationGracePeriodSeconds`](/zh/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/#probe-level-terminationgraceperiodseconds)。
  有关更多信息，请参见 [enhancement proposal](https://github.com/kubernetes/enhancements/tree/master/keps/sig-node/2238-liveness-probe-grace-period)。
- `ProcMountType`：允许容器通过设置 SecurityContext 的 `procMount` 字段来控制
  对 proc 文件系统的挂载方式。
- `QOSReserved`：允许在 QoS 级别进行资源预留，以防止处于较低 QoS 级别的 Pod
  突发进入处于较高 QoS 级别的请求资源（目前仅适用于内存）。
- `RemainingItemCount`：允许 API 服务器在
  [分块列表请求](/zh/docs/reference/using-api/api-concepts/#retrieving-large-results-sets-in-chunks)
  的响应中显示剩余条目的个数。
<!--
- `RemoveSelfLink`: Deprecates and removes `selfLink` from ObjectMeta and
  ListMeta.
- `RequestManagement`: Enables managing request concurrency with prioritization and fairness
  at each API server. Deprecated by `APIPriorityAndFairness` since 1.17.
- `ResourceLimitsPriorityFunction`: Enable a scheduler priority function that
  assigns a lowest possible score of 1 to a node that satisfies at least one of
  the input Pod's cpu and memory limits. The intent is to break ties between
  nodes with same scores.
- `ResourceQuotaScopeSelectors`: Enable resource quota scope selectors.
- `RootCAConfigMap`: Configure the `kube-controller-manager` to publish a
  {{< glossary_tooltip text="ConfigMap" term_id="configmap" >}} named `kube-root-ca.crt`
  to every namespace. This ConfigMap contains a CA bundle used for verifying connections
  to the kube-apiserver. See
  [Bound Service Account Tokens](https://github.com/kubernetes/enhancements/blob/master/keps/sig-auth/1205-bound-service-account-tokens/README.md)
  for more details.
-->
- `RemoveSelfLink`：将 ObjectMeta 和 ListMeta 中的 `selfLink` 字段废弃并删除。
- `RequestManagement`：允许在每个 API 服务器上通过优先级和公平性管理请求并发性。
  自 1.17 以来已被 `APIPriorityAndFairness` 弃用。
- `ResourceLimitsPriorityFunction`：启用某调度器优先级函数，
  该函数将最低得分 1 指派给至少满足输入 Pod 的 CPU 和内存限制之一的节点，
  目的是打破得分相同的节点之间的关联。
- `ResourceQuotaScopeSelectors`：启用资源配额范围选择器。
- `RootCAConfigMap`：配置 `kube-controller-manager`，使之发布一个名为 `kube-root-ca.crt`
  的 {{< glossary_tooltip text="ConfigMap" term_id="configmap" >}}，到
  所有名字空间中。该 ConfigMap 包含用来验证与 kube-apiserver 之间连接的
  CA 证书包。参阅
  [绑定服务账户令牌](https://github.com/kubernetes/enhancements/blob/master/keps/sig-auth/1205-bound-service-account-tokens/README.md)
  以了解更多细节。
<!--
- `RotateKubeletClientCertificate`: Enable the rotation of the client TLS certificate on the kubelet.
  See [kubelet configuration](/docs/reference/command-line-tools-reference/kubelet-tls-bootstrapping/#kubelet-configuration) for more details.
- `RotateKubeletServerCertificate`: Enable the rotation of the server TLS certificate on the kubelet.
  See [kubelet configuration](/docs/reference/command-line-tools-reference/kubelet-tls-bootstrapping/#kubelet-configuration)
  for more details.
- `RunAsGroup`: Enable control over the primary group ID set on the init
  processes of containers.
- `RuntimeClass`: Enable the [RuntimeClass](/docs/concepts/containers/runtime-class/) feature
  for selecting container runtime configurations.
- `ScheduleDaemonSetPods`: Enable DaemonSet Pods to be scheduled by the default scheduler
  instead of the DaemonSet controller.
-->
- `RotateKubeletClientCertificate`：在 kubelet 上启用客户端 TLS 证书的轮换。
  更多详细信息，请参见
  [kubelet 配置](/zh/docs/reference/command-line-tools-reference/kubelet-tls-bootstrapping/#kubelet-configuration)。
- `RotateKubeletServerCertificate`：在 kubelet 上启用服务器 TLS 证书的轮换。
  更多详细信息，请参见
  [kubelet 配置](/zh/docs/reference/command-line-tools-reference/kubelet-tls-bootstrapping/#kubelet-configuration)。
- `RunAsGroup`：启用对容器初始化过程中设置的主要组 ID 的控制。
- `RuntimeClass`：启用 [RuntimeClass](/zh/docs/concepts/containers/runtime-class/)
  特性用于选择容器运行时配置。
- `ScheduleDaemonSetPods`：启用 DaemonSet Pods 由默认调度程序而不是
  DaemonSet 控制器进行调度。
<!--
- `SCTPSupport`: Enables the _SCTP_ `protocol` value in Pod, Service,
  Endpoints, EndpointSlice, and NetworkPolicy definitions.
- `ServerSideApply`: Enables the [Sever Side Apply (SSA)](/docs/reference/using-api/server-side-apply/)
  feature on the API Server.
- `ServiceAccountIssuerDiscovery`: Enable OIDC discovery endpoints (issuer and
  JWKS URLs) for the service account issuer in the API server. See
  [Configure Service Accounts for Pods](/docs/tasks/configure-pod-container/configure-service-account/#service-account-issuer-discovery)
  for more details.
- `ServiceAppProtocol`: Enables the `appProtocol` field on Services and Endpoints.
- `ServiceInternalTrafficPolicy`: Enables the `internalTrafficPolicy` field on Services
- `ServiceLBNodePortControl`: Enables the `allocateLoadBalancerNodePorts` field on Services.
- `ServiceLoadBalancerClass`: Enables the `loadBalancerClass` field on Services. See
  [Specifying class of load balancer implementation](/docs/concepts/services-networking/service/#load-balancer-class) for more details.
- `ServiceLoadBalancerFinalizer`: Enable finalizer protection for Service load balancers.
-->
- `SCTPSupport`：在 Pod、Service、Endpoints、NetworkPolicy 定义中
  允许将 _SCTP_ 用作 `protocol` 值。
- `ServerSideApply`：在 API 服务器上启用
  [服务器端应用（SSA）](/zh/docs/reference/using-api/server-side-apply/) 。
- `ServiceAccountIssuerDiscovery`：在 API 服务器中为服务帐户颁发者启用 OIDC 发现端点
  （颁发者和 JWKS URL）。详情参见
  [为 Pod 配置服务账户](/zh/docs/tasks/configure-pod-container/configure-service-account/#service-account-issuer-discovery) 。
- `ServiceAppProtocol`：为 Service 和 Endpoints 启用 `appProtocol` 字段。
- `ServiceInternalTrafficPolicy`：为服务启用 `internalTrafficPolicy` 字段。
- `ServiceLBNodePortControl`：为服务启用 `allocateLoadBalancerNodePorts` 字段。
 `ServiceLoadBalancerClass`: 为服务启用 `loadBalancerClass` 字段。 
  有关更多信息，请参见 [负载均衡器类的定义 implementation](/zh/docs/concepts/services-networking/service/#load-balancer-class)。
- `ServiceLoadBalancerFinalizer`：为服务负载均衡启用终结器（finalizers）保护。
<!--
- `ServiceNodeExclusion`: Enable the exclusion of nodes from load balancers
  created by a cloud provider. A node is eligible for exclusion if labelled with
  "`node.kubernetes.io/exclude-from-external-load-balancers`".
- `ServiceTopology`: Enable service to route traffic based upon the Node
  topology of the cluster. See
  [ServiceTopology](/docs/concepts/services-networking/service-topology/)
  for more details.
- `SetHostnameAsFQDN`: Enable the ability of setting Fully Qualified Domain
  Name(FQDN) as the hostname of a pod. See
  [Pod's `setHostnameAsFQDN` field](/docs/concepts/services-networking/dns-pod-service/#pod-sethostnameasfqdn-field).
- `SizeMemoryBackedVolumes`: Enable kubelets to determine the size limit for
  memory-backed volumes (mainly `emptyDir` volumes).
-->
- `ServiceNodeExclusion`：启用从云提供商创建的负载均衡中排除节点。
  如果节点标记有 `node.kubernetes.io/exclude-from-external-load-balancers`，
  标签，则可以排除该节点。
- `ServiceTopology`：启用服务拓扑可以让一个服务基于集群的节点拓扑进行流量路由。
  有关更多详细信息，请参见
  [服务拓扑](/zh/docs/concepts/services-networking/service-topology/)。
- `SetHostnameAsFQDN`：启用将全限定域名（FQDN）设置为 Pod 主机名的功能。
  请参见[为 Pod 设置 `setHostnameAsFQDN` 字段](/zh/docs/concepts/services-networking/dns-pod-service/#pod-sethostnameasfqdn-field)。
- `SizeMemoryBackedVolumes`：允许 kubelet 检查基于内存制备的卷的尺寸约束
  （目前主要针对 `emptyDir` 卷）。
<!--
- `StartupProbe`: Enable the
  [startup](/docs/concepts/workloads/pods/pod-lifecycle/#when-should-you-use-a-startup-probe)
  probe in the kubelet.
- `StorageObjectInUseProtection`: Postpone the deletion of PersistentVolume or
  PersistentVolumeClaim objects if they are still being used.
- `StorageVersionAPI`: Enable the
  [storage version API](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#storageversion-v1alpha1-internal-apiserver-k8s-io).
- `StorageVersionHash`: Allow API servers to expose the storage version hash in the
  discovery.
- `StreamingProxyRedirects`: Instructs the API server to intercept (and follow)
   redirects from the backend (kubelet) for streaming requests.
  Examples of streaming requests include the `exec`, `attach` and `port-forward` requests.
-->
- `StartupProbe`：在 kubelet 中启用
  [启动探针](/zh/docs/concepts/workloads/pods/pod-lifecycle/#when-should-you-use-a-startup-probe)。
- `StorageObjectInUseProtection`：如果仍在使用 PersistentVolume 或
  PersistentVolumeClaim 对象，则将其删除操作推迟。
- `StorageVersionAPI`: 启用
  [存储版本 API](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#storageversion-v1alpha1-internal-apiserver-k8s-io)。
- `StorageVersionHash`：允许 API 服务器在版本发现中公开存储版本的哈希值。
- `StreamingProxyRedirects`：指示 API 服务器拦截（并跟踪）后端（kubelet）
  的重定向以处理流请求。
  流请求的例子包括 `exec`、`attach` 和 `port-forward` 请求。
<!--
- `SupportIPVSProxyMode`: Enable providing in-cluster service load balancing using IPVS.
  See [service proxies](/docs/concepts/services-networking/service/#virtual-ips-and-service-proxies) for more details.
- `SupportNodePidsLimit`: Enable the support to limiting PIDs on the Node.
  The parameter `pid=<number>` in the `--system-reserved` and `--kube-reserved`
  options can be specified to ensure that the specified number of process IDs
  will be reserved for the system as a whole and for Kubernetes system daemons
  respectively.
- `SupportPodPidsLimit`: Enable the support to limiting PIDs in Pods.
- `SuspendJob`: Enable support to suspend and resume Jobs. See
  [the Jobs docs](/docs/concepts/workloads/controllers/job/) for
  more details.
- `Sysctls`: Enable support for namespaced kernel parameters (sysctls) that can be
  set for each pod. See
  [sysctls](/docs/tasks/administer-cluster/sysctl-cluster/) for more details.
-->
- `SupportIPVSProxyMode`：启用使用 IPVS 提供内服务负载平衡。更多详细信息，请参见
  [服务代理](/zh/docs/concepts/services-networking/service/#virtual-ips-and-service-proxies)。
- `SupportNodePidsLimit`：启用支持，限制节点上的 PID 用量。
  `--system-reserved` 和 `--kube-reserved` 中的参数 `pid=<数值>` 可以分别用来
  设定为整个系统所预留的进程 ID 个数和为 Kubernetes 系统守护进程预留的进程
  ID 个数。
- `SupportPodPidsLimit`：启用支持限制 Pod 中的进程 PID。
- `SuspendJob`： 启用支持以暂停和恢复作业。 更多详细信息，请参见
  [Jobs 文档](zh//docs/concepts/workloads/controllers/job/)。
- `Sysctls`：允许为每个 Pod 设置的名字空间内核参数（sysctls）。
  更多详细信息，请参见 [sysctls](/zh/docs/tasks/administer-cluster/sysctl-cluster/)。
<!--
- `TTLAfterFinished`: Allow a
  [TTL controller](/docs/concepts/workloads/controllers/ttlafterfinished/)
  to clean up resources after they finish execution.
- `TaintBasedEvictions`: Enable evicting pods from nodes based on taints on Nodes
  and tolerations on Pods.
  See [taints and tolerations](/docs/concepts/scheduling-eviction/taint-and-toleration/)
  for more details.
- `TaintNodesByCondition`: Enable automatic tainting nodes based on
  [node conditions](/docs/concepts/architecture/nodes/#condition).
- `TokenRequest`: Enable the `TokenRequest` endpoint on service account resources.
- `TokenRequestProjection`: Enable the injection of service account tokens into a
  Pod through a [`projected` volume](/docs/concepts/storage/volumes/#projected).
- `TopologyAwareHints`: Enables topology aware routing based on topology hints
  in EndpointSlices. See [Topology Aware
  Hints](/docs/concepts/services-networking/topology-aware-hints/) for more
  details.
- `TopologyManager`: Enable a mechanism to coordinate fine-grained hardware resource
  assignments for different components in Kubernetes. See
  [Control Topology Management Policies on a node](/docs/tasks/administer-cluster/topology-manager/).
-->
- `TTLAfterFinished`：资源完成执行后，允许
  [TTL 控制器](/zh/docs/concepts/workloads/controllers/ttlafterfinished/)清理资源。
- `TaintBasedEvictions`：根据节点上的污点和 Pod 上的容忍度启用从节点驱逐 Pod 的特性。
  更多详细信息可参见[污点和容忍度](/zh/docs/concepts/scheduling-eviction/taint-and-toleration/)。
- `TaintNodesByCondition`：根据[节点状况](/zh/docs/concepts/scheduling-eviction/taint-and-toleration/)
  启用自动为节点标记污点。
- `TokenRequest`：在服务帐户资源上启用 `TokenRequest` 端点。
- `TokenRequestProjection`：启用通过
  [`projected` 卷](/zh/docs/concepts/storage/volumes/#projected)
  将服务帐户令牌注入到 Pod 中的特性。
- `TopologyAwareHints`： 在 EndpointSlices 中启用基于拓扑提示的拓扑感知路由。
  更多详细信息可参见[Topology Aware Hints](/docs/concepts/services-networking/topology-aware-hints/)
- `TopologyManager`：启用一种机制来协调 Kubernetes 不同组件的细粒度硬件资源分配。
  详见[控制节点上的拓扑管理策略](/zh/docs/tasks/administer-cluster/topology-manager/)。
<!--
- `ValidateProxyRedirects`: This flag controls whether the API server should
  validate that redirects are only followed to the same host. Only used if the
  `StreamingProxyRedirects` flag is enabled.
- `VolumeCapacityPriority`: Enable support for prioritizing nodes in different
  topologies based on available PV capacity.
- `VolumePVCDataSource`: Enable support for specifying an existing PVC as a DataSource.
- `VolumeScheduling`: Enable volume topology aware scheduling and make the
  PersistentVolumeClaim (PVC) binding aware of scheduling decisions. It also
  enables the usage of [`local`](/docs/concepts/storage/volumes/#local) volume
  type when used together with the `PersistentLocalVolumes` feature gate.
- `VolumeSnapshotDataSource`: Enable volume snapshot data source support.
- `VolumeSubpath`: Allow mounting a subpath of a volume in a container.
-->
- `ValidateProxyRedirects`： 这个标志控制 API 服务器是否应该验证只跟随到相同的主机的重定向。
  仅在启用 `StreamingProxyRedirects` 标志时被使用。
- `VolumeCapacityPriority`: 基于可用 PV 容量的拓扑，启用对不同节点的优先级支持。
- `VolumePVCDataSource`：启用对将现有 PVC 指定数据源的支持。
- `VolumeScheduling`：启用卷拓扑感知调度，并使 PersistentVolumeClaim（PVC）
  绑定能够了解调度决策；当与 PersistentLocalVolumes 特性门控一起使用时，
  还允许使用 [`local`](/docs/concepts/storage/volumes/#local) 卷类型。
- `VolumeSnapshotDataSource`：启用卷快照数据源支持。
- `VolumeSubpath`： 允许在容器中挂载卷的子路径。
<!--
- `VolumeSubpathEnvExpansion`: Enable `subPathExpr` field for expanding environment
  variables into a `subPath`.
- `WarningHeaders`: Allow sending warning headers in API responses.
- `WatchBookmark`: Enable support for watch bookmark events.
- `WinDSR`: Allows kube-proxy to create DSR loadbalancers for Windows.
- `WinOverlay`: Allows kube-proxy to run in overlay mode for Windows.
- `WindowsGMSA`: Enables passing of GMSA credential specs from pods to container runtimes.
- `WindowsRunAsUserName` : Enable support for running applications in Windows containers
  with as a non-default user. See
  [Configuring RunAsUserName](/docs/tasks/configure-pod-container/configure-runasusername)
  for more details.
- `WindowsEndpointSliceProxying`: When enabled, kube-proxy running on Windows
  will use EndpointSlices as the primary data source instead of Endpoints,
  enabling scalability and performance improvements. See
  [Enabling Endpoint Slices](/docs/tasks/administer-cluster/enabling-endpointslices/).
-->
- `VolumeSubpathEnvExpansion`：启用 `subPathExpr` 字段用于将环境变量在 `subPath`
  中展开。
- `WarningHeaders`：允许在 API 响应中发送警告头部。
- `WatchBookmark`：启用对 watch 操作中 bookmark 事件的支持。
- `WinDSR`：允许 kube-proxy 为 Windows 创建 DSR 负载均衡。
- `WinOverlay`：允许 kube-proxy 在 Windows 的覆盖网络模式下运行。
- `WindowsGMSA`：允许将 GMSA 凭据规范从 Pod 传递到容器运行时。
- `WindowsRunAsUserName`：提供使用非默认用户在 Windows 容器中运行应用程序的支持。
  详情请参见
  [配置 RunAsUserName](/zh/docs/tasks/configure-pod-container/configure-runasusername)。
- `WindowsEndpointSliceProxying`：启用此特性门控后，Windows 上运行的 kube-proxy
  将使用 EndpointSlices 取代 Endpoints 作为主要数据源，进而提高扩展性和性能。参见
  [启用 EndpointSlice](/zh/docs/tasks/administer-cluster/enabling-endpointslices/)。

## {{% heading "whatsnext" %}}

<!--
* The [deprecation policy](/docs/reference/using-api/deprecation-policy/) for Kubernetes explains
  the project's approach to removing features and components.
-->
* Kubernetes 的[弃用策略](/zh/docs/reference/using-api/deprecation-policy/)
  介绍了项目针对已移除特性和组件的处理方法。

