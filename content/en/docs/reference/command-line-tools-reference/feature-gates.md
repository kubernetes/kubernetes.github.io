---
title: Feature Gates
weight: 10
content_type: concept
---

<!-- overview -->
This page contains an overview of the various feature gates an administrator
can specify on different Kubernetes components.

See [feature stages](#feature-stages) for an explanation of the stages for a feature.


<!-- body -->
## Overview

Feature gates are a set of key=value pairs that describe Kubernetes features.
You can turn these features on or off using the `--feature-gates` command line flag
on each Kubernetes component.


Each Kubernetes component lets you enable or disable a set of feature gates that
are relevant to that component.
Use `-h` flag to see a full set of feature gates for all components.
To set feature gates for a component, such as kubelet, use the `--feature-gates` flag assigned to a list of feature pairs:

```shell
--feature-gates="...,DynamicKubeletConfig=true"
```

The following tables are a summary of the feature gates that you can set on
different Kubernetes components.

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

### Feature gates for Alpha or Beta features

{{< table caption="Feature gates for features in Alpha or Beta states" >}}

| Feature | Default | Stage | Since | Until |
|---------|---------|-------|-------|-------|
| `APIListChunking` | `false` | Alpha | 1.8 | 1.8 |
| `APIListChunking` | `true` | Beta | 1.9 | |
| `APIPriorityAndFairness` | `false` | Alpha | 1.17 | 1.19 |
| `APIPriorityAndFairness` | `true` | Beta | 1.20 | |
| `APIResponseCompression` | `false` | Alpha | 1.7 | 1.15 |
| `APIResponseCompression` | `true` | Beta | 1.16 | |
| `APIServerIdentity` | `false` | Alpha | 1.20 | |
| `APIServerTracing` | `false` | Alpha | 1.22 | |
| `AllowInsecureBackendProxy` | `true` | Beta | 1.17 | |
| `AnyVolumeDataSource` | `false` | Alpha | 1.18 | |
| `AppArmor` | `true` | Beta | 1.4 | |
| `ControllerManagerLeaderMigration` | `false` | Alpha | 1.21 | |
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
| `CSIStorageCapacity` | `false` | Alpha | 1.19 | 1.20 |
| `CSIStorageCapacity` | `true` | Beta | 1.21 | |
| `CSIVolumeFSGroupPolicy` | `false` | Alpha | 1.19 | 1.19 |
| `CSIVolumeFSGroupPolicy` | `true` | Beta | 1.20 | |
| `CSIVolumeHealth` | `false` | Alpha | 1.21 | |
| `CSRDuration` | `true` | Beta | 1.22 | |
| `ConfigurableFSGroupPolicy` | `false` | Alpha | 1.18 | 1.19 |
| `ConfigurableFSGroupPolicy` | `true` | Beta | 1.20 | |
| `ControllerManagerLeaderMigration` | `false` | Alpha | 1.21 | |
| `CustomCPUCFSQuotaPeriod` | `false` | Alpha | 1.12 | |
| `DaemonSetUpdateSurge` | `false` | Alpha | 1.21 | 1.21 |
| `DaemonSetUpdateSurge` | `true` | Beta | 1.22 | |
| `DefaultPodTopologySpread` | `false` | Alpha | 1.19 | 1.19 |
| `DefaultPodTopologySpread` | `true` | Beta | 1.20 | |
| `DevicePlugins` | `false` | Alpha | 1.8 | 1.9 |
| `DevicePlugins` | `true` | Beta | 1.10 | |
| `DisableAcceleratorUsageMetrics` | `false` | Alpha | 1.19 | 1.19 |
| `DisableAcceleratorUsageMetrics` | `true` | Beta | 1.20 | |
| `DisableCloudProviders` | `false` | Alpha | 1.22 | |
| `DownwardAPIHugePages` | `false` | Alpha | 1.20 | 1.20 |
| `DownwardAPIHugePages` | `false` | Beta | 1.21 | |
| `DynamicKubeletConfig` | `false` | Alpha | 1.4 | 1.10 |
| `DynamicKubeletConfig` | `true` | Beta | 1.11 | |
| `EfficientWatchResumption` | `false` | Alpha | 1.20 | 1.20 |
| `EfficientWatchResumption` | `true` | Beta | 1.21 | |
| `EndpointSliceProxying` | `false` | Alpha | 1.18 | 1.18 |
| `EndpointSliceProxying` | `true` | Beta | 1.19 | |
| `EndpointSliceTerminatingCondition` | `false` | Alpha | 1.20 | |
| `EphemeralContainers` | `false` | Alpha | 1.16 | |
| `ExpandCSIVolumes` | `false` | Alpha | 1.14 | 1.15 |
| `ExpandCSIVolumes` | `true` | Beta | 1.16 | |
| `ExpandedDNSConfig` | `false` | Alpha | 1.22 | |
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
| `IndexedJob` | `false` | Alpha | 1.21 | 1.21 |
| `IndexedJob` | `true` | Beta | 1.22 | |
| `IngressClassNamespacedParams` | `false` | Alpha | 1.21 | 1.21 |
| `IngressClassNamespacedParams` | `true` | Beta | 1.22 | |
| `IPv6DualStack` | `false` | Alpha | 1.15 | 1.20 |
| `IPv6DualStack` | `true` | Beta | 1.21 | |
| `KubeletCredentialProviders` | `false` | Alpha | 1.20 | |
| `LocalStorageCapacityIsolation` | `false` | Alpha | 1.7 | 1.9 |
| `LocalStorageCapacityIsolation` | `true` | Beta | 1.10 | |
| `LocalStorageCapacityIsolationFSQuotaMonitoring` | `false` | Alpha | 1.15 | |
| `LogarithmicScaleDown` | `false` | Alpha | 1.21 | |
| `LogarithmicScaleDown` | `true` | Beta | 1.22 | |
| `KubeletPodResourcesGetAllocatable` | `false` | Alpha | 1.21 | |
| `MemoryManager` | `false` | Alpha | 1.21 | 1.21 |
| `MemoryManager` | `true` | Beta | 1.22 | |
| `MixedProtocolLBService` | `false` | Alpha | 1.20 | |
| `NetworkPolicyEndPort` | `false` | Alpha | 1.21 | 1.21 |
| `NetworkPolicyEndPort` | `true` | Beta | 1.22 |  |
| `NonPreemptingPriority` | `false` | Alpha | 1.15 | 1.18 |
| `NonPreemptingPriority` | `true` | Beta | 1.19 | |
| `PodDeletionCost` | `false` | Alpha | 1.21 | 1.21 |
| `PodDeletionCost` | `true` | Beta | 1.22 | |
| `PodAffinityNamespaceSelector` | `false` | Alpha | 1.21 | 1.21 |
| `PodAffinityNamespaceSelector` | `true` | Beta | 1.22 | |
| `PodOverhead` | `false` | Alpha | 1.16 | 1.17 |
| `PodOverhead` | `true` | Beta | 1.18 | |
| `PodSecurity` | `false` | Alpha | 1.22 | |
| `PreferNominatedNode` | `false` | Alpha | 1.21 | 1.21 |
| `PreferNominatedNode` | `true` | Beta | 1.22 | |
| `ProbeTerminationGracePeriod` | `false` | Alpha | 1.21 | |
| `ProxyTerminatingEndpoints` | `false` | Alpha | 1.22 | |
| `ProcMountType` | `false` | Alpha | 1.12 | |
| `QOSReserved` | `false` | Alpha | 1.11 | |
| `ReadWriteOncePod` | `false` | Alpha | 1.22 | |
| `RemainingItemCount` | `false` | Alpha | 1.15 | 1.15 |
| `RemainingItemCount` | `true` | Beta | 1.16 | |
| `RemoveSelfLink` | `false` | Alpha | 1.16 | 1.19 |
| `RemoveSelfLink` | `true` | Beta | 1.20 | |
| `RotateKubeletServerCertificate` | `false` | Alpha | 1.7 | 1.11 |
| `RotateKubeletServerCertificate` | `true` | Beta | 1.12 | |
| `SeccompDefault` | `false` | Alpha | 1.22 | |
| `ServiceInternalTrafficPolicy` | `false` | Alpha | 1.21 | |
| `ServiceLBNodePortControl` | `false` | Alpha | 1.20 | 1.21 |
| `ServiceLBNodePortControl` | `true` | Beta | 1.22 | |
| `ServiceLoadBalancerClass` | `false` | Alpha | 1.21 | 1.21 |
| `ServiceLoadBalancerClass` | `true` | Beta | 1.22 | |
| `SizeMemoryBackedVolumes` | `false` | Alpha | 1.20 | 1.21 |
| `SizeMemoryBackedVolumes` | `true` | Beta | 1.22 | |
| `StatefulSetMinReadySeconds` | `false` | Alpha | 1.22 | |
| `StorageVersionAPI` | `false` | Alpha | 1.20 | |
| `StorageVersionHash` | `false` | Alpha | 1.14 | 1.14 |
| `StorageVersionHash` | `true` | Beta | 1.15 | |
| `SuspendJob` | `false` | Alpha | 1.21 | 1.21 |
| `SuspendJob` | `true` | Beta | 1.22 | |
| `TTLAfterFinished` | `false` | Alpha | 1.12 | 1.20 |
| `TTLAfterFinished` | `true` | Beta | 1.21 | |
| `TopologyAwareHints` | `false` | Alpha | 1.21 | |
| `TopologyManager` | `false` | Alpha | 1.16 | 1.17 |
| `TopologyManager` | `true` | Beta | 1.18 | |
| `VolumeCapacityPriority` | `false` | Alpha | 1.21 | - |
| `WinDSR` | `false` | Alpha | 1.14 | |
| `WinOverlay` | `false` | Alpha | 1.14 | 1.19 |
| `WinOverlay` | `true` | Beta | 1.20 | |
| `WindowsEndpointSliceProxying` | `false` | Alpha | 1.19 | 1.20 |
| `WindowsEndpointSliceProxying` | `true` | Beta | 1.21 | |
| `WindowsHostProcessContainers` | `false` | Alpha | 1.22 | |
{{< /table >}}

### Feature gates for graduated or deprecated features

{{< table caption="Feature Gates for Graduated or Deprecated Features" >}}

| Feature | Default | Stage | Since | Until |
|---------|---------|-------|-------|-------|
| `Accelerators` | `false` | Alpha | 1.6 | 1.10 |
| `Accelerators` | - | Deprecated | 1.11 | - |
| `AdvancedAuditing` | `false` | Alpha | 1.7 | 1.7 |
| `AdvancedAuditing` | `true` | Beta | 1.8 | 1.11 |
| `AdvancedAuditing` | `true` | GA | 1.12 | - |
| `AffinityInAnnotations` | `false` | Alpha | 1.6 | 1.7 |
| `AffinityInAnnotations` | - | Deprecated | 1.8 | - |
| `AllowExtTrafficLocalEndpoints` | `false` | Beta | 1.4 | 1.6 |
| `AllowExtTrafficLocalEndpoints` | `true` | GA | 1.7 | - |
| `AttachVolumeLimit` | `false` | Alpha | 1.11 | 1.11 |
| `AttachVolumeLimit` | `true` | Beta | 1.12 | 1.16 |
| `AttachVolumeLimit` | `true` | GA | 1.17 | - |
| `BalanceAttachedNodeVolumes` | `false` | Alpha | 1.11 | 1.21 |
| `BalanceAttachedNodeVolumes` | `false` | Deprecated | 1.22 | |
| `BlockVolume` | `false` | Alpha | 1.9 | 1.12 |
| `BlockVolume` | `true` | Beta | 1.13 | 1.17 |
| `BlockVolume` | `true` | GA | 1.18 | - |
| `BoundServiceAccountTokenVolume` | `false` | Alpha | 1.13 | 1.20 |
| `BoundServiceAccountTokenVolume` | `true` | Beta | 1.21 | 1.21 |
| `BoundServiceAccountTokenVolume` | `true` | GA | 1.22 | - |
| `CRIContainerLogRotation` | `false` | Alpha | 1.10 | 1.10 |
| `CRIContainerLogRotation` | `true` | Beta | 1.11 | 1.20 |
| `CRIContainerLogRotation` | `true` | GA | 1.21 | - |
| `CSIBlockVolume` | `false` | Alpha | 1.11 | 1.13 |
| `CSIBlockVolume` | `true` | Beta | 1.14 | 1.17 |
| `CSIBlockVolume` | `true` | GA | 1.18 | - |
| `CSIDriverRegistry` | `false` | Alpha | 1.12 | 1.13 |
| `CSIDriverRegistry` | `true` | Beta | 1.14 | 1.17 |
| `CSIDriverRegistry` | `true` | GA | 1.18 | |
| `CSIMigrationvSphereComplete` | `false` | Beta | 1.19 | 1.21 |
| `CSIMigrationvSphereComplete` | `false` | Deprecated | 1.22 | - |
| `CSINodeInfo` | `false` | Alpha | 1.12 | 1.13 |
| `CSINodeInfo` | `true` | Beta | 1.14 | 1.16 |
| `CSINodeInfo` | `true` | GA | 1.17 | |
| `CSIPersistentVolume` | `false` | Alpha | 1.9 | 1.9 |
| `CSIPersistentVolume` | `true` | Beta | 1.10 | 1.12 |
| `CSIPersistentVolume` | `true` | GA | 1.13 | - |
| `CSIServiceAccountToken` | `false` | Alpha | 1.20 | 1.20 |
| `CSIServiceAccountToken` | `true` | Beta | 1.21 | 1.21 |
| `CSIServiceAccountToken` | `true` | GA | 1.22 | |
| `CronJobControllerV2` | `false` | Alpha | 1.20 | 1.20 |
| `CronJobControllerV2` | `true` | Beta | 1.21 | 1.21 |
| `CronJobControllerV2` | `true` | GA | 1.22 | - |
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
| `EndpointSliceNodeName` | `false` | Alpha | 1.20 | 1.20 |
| `EndpointSliceNodeName` | `true` | GA | 1.21 | - |
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
| `LegacyNodeRoleBehavior` | `false` | Alpha | 1.16 | 1.18 |
| `LegacyNodeRoleBehavior` | `true` | Beta | 1.19 | 1.20 |
| `LegacyNodeRoleBehavior` | `false` | GA | 1.21 | - |
| `MountContainers` | `false` | Alpha | 1.9 | 1.16 |
| `MountContainers` | `false` | Deprecated | 1.17 | - |
| `MountPropagation` | `false` | Alpha | 1.8 | 1.9 |
| `MountPropagation` | `true` | Beta | 1.10 | 1.11 |
| `MountPropagation` | `true` | GA | 1.12 | - |
| `NodeDisruptionExclusion` | `false` | Alpha | 1.16 | 1.18 |
| `NodeDisruptionExclusion` | `true` | Beta | 1.19 | 1.20 |
| `NodeDisruptionExclusion` | `true` | GA | 1.21 | - |
| `NodeLease` | `false` | Alpha | 1.12 | 1.13 |
| `NodeLease` | `true` | Beta | 1.14 | 1.16 |
| `NodeLease` | `true` | GA | 1.17 | - |
| `NamespaceDefaultLabelName` | `true` | Beta | 1.21 | 1.21 |
| `NamespaceDefaultLabelName` | `true` | GA | 1.22 | - |
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
| `RunAsGroup` | `true` | Beta | 1.14 | 1.20 |
| `RunAsGroup` | `true` | GA | 1.21 | - |
| `RuntimeClass` | `false` | Alpha | 1.12 | 1.13 |
| `RuntimeClass` | `true` | Beta | 1.14 | 1.19 |
| `RuntimeClass` | `true` | GA | 1.20 | - |
| `SCTPSupport` | `false` | Alpha | 1.12 | 1.18 |
| `SCTPSupport` | `true` | Beta | 1.19 | 1.19 |
| `SCTPSupport` | `true` | GA | 1.20 | - |
| `ScheduleDaemonSetPods` | `false` | Alpha | 1.11 | 1.11 |
| `ScheduleDaemonSetPods` | `true` | Beta | 1.12 | 1.16  |
| `ScheduleDaemonSetPods` | `true` | GA | 1.17 | - |
| `SelectorIndex` | `false` | Alpha | 1.18 | 1.18 |
| `SelectorIndex` | `true` | Beta | 1.19 | 1.19 |
| `SelectorIndex` | `true` | GA | 1.20 | - |
| `ServerSideApply` | `false` | Alpha | 1.14 | 1.15 |
| `ServerSideApply` | `true` | Beta | 1.16 | 1.21 |
| `ServerSideApply` | `true` | GA | 1.22 | - |
| `ServiceAccountIssuerDiscovery` | `false` | Alpha | 1.18 | 1.19 |
| `ServiceAccountIssuerDiscovery` | `true` | Beta | 1.20 | 1.20 |
| `ServiceAccountIssuerDiscovery` | `true` | GA | 1.21 | - |
| `ServiceAppProtocol` | `false` | Alpha | 1.18 | 1.18 |
| `ServiceAppProtocol` | `true` | Beta | 1.19 | 1.19 |
| `ServiceAppProtocol` | `true` | GA | 1.20 | - |
| `ServiceLoadBalancerFinalizer` | `false` | Alpha | 1.15 | 1.15 |
| `ServiceLoadBalancerFinalizer` | `true` | Beta | 1.16 | 1.16 |
| `ServiceLoadBalancerFinalizer` | `true` | GA | 1.17 | - |
| `ServiceNodeExclusion` | `false` | Alpha | 1.8 | 1.18 |
| `ServiceNodeExclusion` | `true` | Beta | 1.19 | 1.20 |
| `ServiceNodeExclusion` | `true` | GA | 1.21 | - |
| `ServiceTopology` | `false` | Alpha | 1.17 | 1.19 |
| `ServiceTopology` | `false` | Deprecated | 1.20 | - |
| `SetHostnameAsFQDN` | `false` | Alpha | 1.19 | 1.19 |
| `SetHostnameAsFQDN` | `true` | Beta | 1.20 | 1.21 |
| `SetHostnameAsFQDN` | `true` | GA | 1.22 | - |
| `StartupProbe` | `false` | Alpha | 1.16 | 1.17 |
| `StartupProbe` | `true` | Beta | 1.18 | 1.19 |
| `StartupProbe` | `true` | GA | 1.20 | - |
| `StorageObjectInUseProtection` | `true` | Beta | 1.10 | 1.10 |
| `StorageObjectInUseProtection` | `true` | GA | 1.11 | - |
| `StreamingProxyRedirects` | `false` | Beta | 1.5 | 1.5 |
| `StreamingProxyRedirects` | `true` | Beta | 1.6 | 1.17 |
| `StreamingProxyRedirects` | `true` | Deprecated | 1.18 | 1.21 |
| `StreamingProxyRedirects` | `false` | Deprecated | 1.22 | - |
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
| `ValidateProxyRedirects` | `false` | Alpha | 1.12 | 1.13 |
| `ValidateProxyRedirects` | `true` | Beta | 1.14 | 1.21 |
| `ValidateProxyRedirects` | `true` | Deprecated | 1.22 | - |
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
| `WarningHeaders` | `true` | Beta | 1.19 | 1.21 |
| `WarningHeaders` | `true` | GA | 1.22 | - |
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

## Using a feature

### Feature stages

A feature can be in *Alpha*, *Beta* or *GA* stage.
An *Alpha* feature means:

* Disabled by default.
* Might be buggy. Enabling the feature may expose bugs.
* Support for feature may be dropped at any time without notice.
* The API may change in incompatible ways in a later software release without notice.
* Recommended for use only in short-lived testing clusters, due to increased
  risk of bugs and lack of long-term support.

A *Beta* feature means:

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

{{< note >}}
Please do try *Beta* features and give feedback on them!
After they exit beta, it may not be practical for us to make more changes.
{{< /note >}}

A *General Availability* (GA) feature is also referred to as a *stable* feature. It means:

* The feature is always enabled; you cannot disable it.
* The corresponding feature gate is no longer needed.
* Stable versions of features will appear in released software for many subsequent versions.

## List of feature gates {#feature-gates}

Each feature gate is designed for enabling/disabling a specific feature:

- `APIListChunking`: Enable the API clients to retrieve (`LIST` or `GET`)
  resources from API server in chunks.
- `APIPriorityAndFairness`: Enable managing request concurrency with
  prioritization and fairness at each server. (Renamed from `RequestManagement`)
- `APIResponseCompression`: Compress the API responses for `LIST` or `GET` requests.
- `APIServerIdentity`: Assign each API server an ID in a cluster.
- `APIServerTracing`: Add support for distributed tracing in the API server.
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
- `ControllerManagerLeaderMigration`: Enables Leader Migration for 
  [kube-controller-manager](/docs/tasks/administer-cluster/controller-manager-leader-migration/#initial-leader-migration-configuration) and 
  [cloud-controller-manager](/docs/tasks/administer-cluster/controller-manager-leader-migration/#deploy-cloud-controller-manager) which allows a cluster operator to live migrate 
  controllers from the kube-controller-manager into an external controller-manager 
  (e.g. the cloud-controller-manager) in an HA cluster without downtime.
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
- `CSIMigrationGCE`: Enables shims and translation logic to route volume
  operations from the GCE-PD in-tree plugin to PD CSI plugin. Supports falling
  back to in-tree GCE plugin if a node does not have PD CSI plugin installed and
  configured. Requires CSIMigration feature flag enabled.
- `CSIMigrationGCEComplete`: Stops registering the GCE-PD in-tree plugin in
  kubelet and volume controllers and enables shims and translation logic to
  route volume operations from the GCE-PD in-tree plugin to PD CSI plugin.
  Requires CSIMigration and CSIMigrationGCE feature flags enabled and PD CSI
  plugin installed and configured on all nodes in the cluster.
- `CSIMigrationOpenStack`: Enables shims and translation logic to route volume
  operations from the Cinder in-tree plugin to Cinder CSI plugin. Supports
  falling back to in-tree Cinder plugin if a node does not have Cinder CSI
  plugin installed and configured. Requires CSIMigration feature flag enabled.
- `CSIMigrationOpenStackComplete`: Stops registering the Cinder in-tree plugin in
  kubelet and volume controllers and enables shims and translation logic to route
  volume operations from the Cinder in-tree plugin to Cinder CSI plugin.
  Requires CSIMigration and CSIMigrationOpenStack feature flags enabled and Cinder
  CSI plugin installed and configured on all nodes in the cluster.
- `CSIMigrationvSphere`: Enables shims and translation logic to route volume operations
  from the vSphere in-tree plugin to vSphere CSI plugin.
  Supports falling back to in-tree vSphere plugin if a node does not have vSphere
  CSI plugin installed and configured. Requires CSIMigration feature flag enabled.
- `CSIMigrationvSphereComplete`: Stops registering the vSphere in-tree plugin in kubelet
  and volume controllers and enables shims and translation logic to route volume operations
  from the vSphere in-tree plugin to vSphere CSI plugin. Requires CSIMigration and
  CSIMigrationvSphere feature flags enabled and vSphere CSI plugin installed and
  configured on all nodes in the cluster.
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
- `CSIVolumeFSGroupPolicy`: Allows CSIDrivers to use the `fsGroupPolicy` field.
  This field controls whether volumes created by a CSIDriver support volume ownership
  and permission modifications when these volumes are mounted.
- `CSIVolumeHealth`: Enable support for CSI volume health monitoring on node.
- `CSRDuration`: Allows clients to request a duration for certificates issued
  via the Kubernetes CSR API.
- `ConfigurableFSGroupPolicy`: Allows user to configure volume permission change policy
  for fsGroups when mounting a volume in a Pod. See
  [Configure volume permission and ownership change policy for Pods](/docs/tasks/configure-pod-container/security-context/#configure-volume-permission-and-ownership-change-policy-for-pods)
  for more details.
- `ControllerManagerLeaderMigration`: Enables leader migration for
  `kube-controller-manager` and `cloud-controller-manager`.
- `CronJobControllerV2`: Use an alternative implementation of the
  {{< glossary_tooltip text="CronJob" term_id="cronjob" >}} controller. Otherwise,
  version 1 of the same controller is selected.
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
- `DaemonSetUpdateSurge`: Enables the DaemonSet workloads to maintain
  availability during update per node.
- `DefaultPodTopologySpread`: Enables the use of `PodTopologySpread` scheduling plugin to do
  [default spreading](/docs/concepts/workloads/pods/pod-topology-spread-constraints/#internal-default-constraints).
- `DevicePlugins`: Enable the [device-plugins](/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/)
  based resource provisioning on nodes.
- `DisableAcceleratorUsageMetrics`:
  [Disable accelerator metrics collected by the kubelet](/docs/concepts/cluster-administration/system-metrics/#disable-accelerator-metrics).
- `DisableCloudProviders`: Disables any functionality in `kube-apiserver`,
  `kube-controller-manager` and `kubelet` related to the `--cloud-provider`
  component flag.
- `DownwardAPIHugePages`: Enables usage of hugepages in
  [downward API](/docs/tasks/inject-data-application/downward-api-volume-expose-pod-information).
- `DryRun`: Enable server-side [dry run](/docs/reference/using-api/api-concepts/#dry-run) requests
  so that validation, merging, and mutation can be tested without committing.
- `DynamicAuditing`: Used to enable dynamic auditing before v1.19.
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
- `EphemeralContainers`: Enable the ability to add
  {{< glossary_tooltip text="ephemeral containers" term_id="ephemeral-container" >}}
  to running pods.
- `EvenPodsSpread`: Enable pods to be scheduled evenly across topology domains. See
  [Pod Topology Spread Constraints](/docs/concepts/workloads/pods/pod-topology-spread-constraints/).
- `ExecProbeTimeout`: Ensure kubelet respects exec probe timeouts.
  This feature gate exists in case any of your existing workloads depend on a
  now-corrected fault where Kubernetes ignored exec probe timeouts. See
  [readiness probes](/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/#configure-probes).
- `ExpandCSIVolumes`: Enable the expanding of CSI volumes.
- `ExpandedDNSConfig`: Enable kubelet and kube-apiserver to allow more DNS
  search paths and longer list of DNS search paths. See
  [Expanded DNS Configuration](/docs/concepts/services-networking/dns-pod-service/#expanded-dns-configuration).
- `ExpandInUsePersistentVolumes`: Enable expanding in-use PVCs. See
  [Resizing an in-use PersistentVolumeClaim](/docs/concepts/storage/persistent-volumes/#resizing-an-in-use-persistentvolumeclaim).
- `ExpandPersistentVolumes`: Enable the expanding of persistent volumes. See
  [Expanding Persistent Volumes Claims](/docs/concepts/storage/persistent-volumes/#expanding-persistent-volumes-claims).
- `ExperimentalCriticalPodAnnotation`: Enable annotating specific pods as *critical*
  so that their [scheduling is guaranteed](/docs/tasks/administer-cluster/guaranteed-scheduling-critical-addon-pods/).
  This feature is deprecated by Pod Priority and Preemption as of v1.13.
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
- `HPAContainerMetrics`: Enable the `HorizontalPodAutoscaler` to scale based on
  metrics from individual containers in target pods.
- `HPAScaleToZero`: Enables setting `minReplicas` to 0 for `HorizontalPodAutoscaler`
  resources when using custom or external metrics.
- `HugePages`: Enable the allocation and consumption of pre-allocated
  [huge pages](/docs/tasks/manage-hugepages/scheduling-hugepages/).
- `HugePageStorageMediumSize`: Enable support for multiple sizes pre-allocated
  [huge pages](/docs/tasks/manage-hugepages/scheduling-hugepages/).
- `HyperVContainer`: Enable
  [Hyper-V isolation](https://docs.microsoft.com/en-us/virtualization/windowscontainers/manage-containers/hyperv-container)
  for Windows containers.
- `ImmutableEphemeralVolumes`: Allows for marking individual Secrets and ConfigMaps as
  immutable for better safety and performance.
- `IndexedJob`: Allows the [Job](/docs/concepts/workloads/controllers/job/)
  controller to manage Pod completions per completion index.
- `IngressClassNamespacedParams`: Allow namespace-scoped parameters reference in
  `IngressClass` resource. This feature adds two fields - `Scope` and `Namespace`
  to `IngressClass.spec.parameters`.
- `Initializers`: Allow asynchronous coordination of object creation using the
  Initializers admission plugin.
- `IPv6DualStack`: Enable [dual stack](/docs/concepts/services-networking/dual-stack/)
  support for IPv6.
- `KubeletConfigFile`: Enable loading kubelet configuration from
  a file specified using a config file.
  See [setting kubelet parameters via a config file](/docs/tasks/administer-cluster/kubelet-config-file/)
  for more details.
- `KubeletCredentialProviders`: Enable kubelet exec credential providers for image pull credentials.
- `KubeletPluginsWatcher`: Enable probe-based plugin watcher utility to enable kubelet
  to discover plugins such as [CSI volume drivers](/docs/concepts/storage/volumes/#csi).
- `KubeletPodResources`: Enable the kubelet's pod resources gRPC endpoint. See
  [Support Device Monitoring](https://github.com/kubernetes/enhancements/blob/master/keps/sig-node/606-compute-device-assignment/README.md)
  for more details.
- `KubeletPodResourcesGetAllocatable`: Enable the kubelet's pod resources `GetAllocatableResources` functionality.
  This API augments the [resource allocation reporting](/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/#monitoring-device-plugin-resources)
  with informations about the allocatable resources, enabling clients to properly track the free compute resources on a node.
- `LegacyNodeRoleBehavior`: When disabled, legacy behavior in service load balancers and
  node disruption will ignore the `node-role.kubernetes.io/master` label in favor of the
  feature-specific labels provided by `NodeDisruptionExclusion` and `ServiceNodeExclusion`.
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
- `MemoryManager`: Allows setting memory affinity for a container based on
  NUMA topology.
- `MixedProtocolLBService`: Enable using different protocols in the same `LoadBalancer` type
  Service instance.
- `MountContainers`: Enable using utility containers on host as the volume mounter.
- `MountPropagation`: Enable sharing volume mounted by one container to other containers or pods.
  For more details, please see [mount propagation](/docs/concepts/storage/volumes/#mount-propagation).
- `NamespaceDefaultLabelName`: Configure the API Server to set an immutable {{< glossary_tooltip text="label" term_id="label" >}}
  `kubernetes.io/metadata.name` on all namespaces, containing the namespace name.
- `NetworkPolicyEndPort`: Enable use of the field `endPort` in NetworkPolicy objects, allowing the selection of a port range instead of a single port.
- `NodeDisruptionExclusion`: Enable use of the Node label `node.kubernetes.io/exclude-disruption`
  which prevents nodes from being evacuated during zone failures.
- `NodeLease`: Enable the new Lease API to report node heartbeats, which could be used as a node health signal.
- `NonPreemptingPriority`: Enable `preemptionPolicy` field for PriorityClass and Pod.
- `PVCProtection`: Enable the prevention of a PersistentVolumeClaim (PVC) from
  being deleted when it is still used by any Pod.
- `PodDeletionCost`: Enable the [Pod Deletion Cost](/docs/concepts/workloads/controllers/replicaset/#pod-deletion-cost)
   feature which allows users to influence ReplicaSet downscaling order.
- `PersistentLocalVolumes`: Enable the usage of `local` volume type in Pods.
  Pod affinity has to be specified if requesting a `local` volume.
- `PodDisruptionBudget`: Enable the [PodDisruptionBudget](/docs/tasks/run-application/configure-pdb/) feature.
- `PodAffinityNamespaceSelector`: Enable the [Pod Affinity Namespace Selector](/docs/concepts/scheduling-eviction/assign-pod-node/#namespace-selector)
  and [CrossNamespacePodAffinity](/docs/concepts/policy/resource-quotas/#cross-namespace-pod-affinity-quota) quota scope features.
- `PodOverhead`: Enable the [PodOverhead](/docs/concepts/scheduling-eviction/pod-overhead/)
  feature to account for pod overheads.
- `PodPriority`: Enable the descheduling and preemption of Pods based on their
  [priorities](/docs/concepts/scheduling-eviction/pod-priority-preemption/).
- `PodReadinessGates`: Enable the setting of `PodReadinessGate` field for extending
  Pod readiness evaluation.  See [Pod readiness gate](/docs/concepts/workloads/pods/pod-lifecycle/#pod-readiness-gate)
  for more details.
- `PodSecurity`: Enables the `PodSecurity` admission plugin.
- `PodShareProcessNamespace`: Enable the setting of `shareProcessNamespace` in a Pod for sharing
  a single process namespace between containers running in a pod.  More details can be found in
  [Share Process Namespace between Containers in a Pod](/docs/tasks/configure-pod-container/share-process-namespace/).
- `PreferNominatedNode`: This flag tells the scheduler whether the nominated
  nodes will be checked first before looping through all the other nodes in
  the cluster.
- `ProbeTerminationGracePeriod`: Enable [setting probe-level
  `terminationGracePeriodSeconds`](/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/#probe-level-terminationgraceperiodseconds)
   on pods.  See the [enhancement proposal](https://github.com/kubernetes/enhancements/tree/master/keps/sig-node/2238-liveness-probe-grace-period) for more details.
- `ProcMountType`: Enables control over the type proc mounts for containers
  by setting the `procMount` field of a SecurityContext.
- `ProxyTerminatingEndpoints`: Enable the kube-proxy to handle terminating
  endpoints when `ExternalTrafficPolicy=Local`.
- `QOSReserved`: Allows resource reservations at the QoS level preventing pods
  at lower QoS levels from bursting into resources requested at higher QoS levels
  (memory only for now).
- `ReadWriteOncePod`: Enables the usage of `ReadWriteOncePod` PersistentVolume
  access mode.
- `RemainingItemCount`: Allow the API servers to show a count of remaining
  items in the response to a
  [chunking list request](/docs/reference/using-api/api-concepts/#retrieving-large-results-sets-in-chunks).
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
- `SCTPSupport`: Enables the _SCTP_ `protocol` value in Pod, Service,
  Endpoints, EndpointSlice, and NetworkPolicy definitions.
- `SeccompDefault`: Enables the use of `RuntimeDefault` as the default seccomp profile for all workloads. 
  The seccomp profile is specified in the `securityContext` of a Pod and/or a Container.
- `SelectorIndex`: Allows label and field based indexes in API server watch
  cache to accelerate list operations.
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
- `StartupProbe`: Enable the
  [startup](/docs/concepts/workloads/pods/pod-lifecycle/#when-should-you-use-a-startup-probe)
  probe in the kubelet.
- `StatefulSetMinReadySeconds`: Allows `minReadySeconds` to be respected by
  the StatefulSet controller.
- `StorageObjectInUseProtection`: Postpone the deletion of PersistentVolume or
  PersistentVolumeClaim objects if they are still being used.
- `StorageVersionAPI`: Enable the
  [storage version API](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#storageversion-v1alpha1-internal-apiserver-k8s-io).
- `StorageVersionHash`: Allow API servers to expose the storage version hash in the
  discovery.
- `StreamingProxyRedirects`: Instructs the API server to intercept (and follow)
  redirects from the backend (kubelet) for streaming requests.
  Examples of streaming requests include the `exec`, `attach` and `port-forward` requests.
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
- `WindowsHostProcessContainers`: Enables the support for `HostProcess`
  containers on Windows nodes.


## {{% heading "whatsnext" %}}

* The [deprecation policy](/docs/reference/using-api/deprecation-policy/) for Kubernetes explains
  the project's approach to removing features and components.
