---
weight: 10
title: 기능 게이트
content_type: concept
---

<!-- overview -->
이 페이지에는 관리자가 다른 쿠버네티스 컴포넌트에서 지정할 수 있는 다양한
기능 게이트에 대한 개요가 포함되어 있다.

기능의 단계(stage)에 대한 설명은 [기능 단계](#기능-단계)를 참고한다.


<!-- body -->
## 개요

기능 게이트는 쿠버네티스 기능을 설명하는 일련의 키=값 쌍이다.
각 쿠버네티스 컴포넌트에서 `--feature-gates` 커맨드 라인 플래그를 사용하여
이러한 기능을 켜거나 끌 수 있다.


각 쿠버네티스 컴포넌트를 사용하면 해당 컴포넌트와 관련된 기능 게이트 집합을
활성화 또는 비활성화할 수 있다.
모든 컴포넌트에 대한 전체 기능 게이트 집합을 보려면 `-h` 플래그를 사용한다.
kubelet과 같은 컴포넌트의 기능 게이트를 설정하려면, 기능 쌍 목록에 지정된 `--feature-gates` 플래그를 사용한다.

```shell
--feature-gates="...,DynamicKubeletConfig=true"
```

다음 표는 다른 쿠버네티스 컴포넌트에서 설정할 수 있는 기능 게이트를
요약한 것이다.

- "도입" 열에는 기능이 소개되거나 릴리스 단계가 변경될 때의
  쿠버네티스 릴리스가 포함된다.
- "종료" 열이 비어 있지 않으면, 여전히 기능 게이트를 사용할 수 있는 마지막
  쿠버네티스 릴리스가 포함된다.
- 기능이 알파 또는 베타 상태인 경우,
  [알파/베타 기능 게이트 테이블](#알파-또는-베타-기능을-위한-기능-게이트)에서 나열된 기능을 찾을 수 있다.
- 기능이 안정된 경우 해당 기능에 대한 모든 단계를
  [GA(graduated)/사용 중단(deprecated) 기능 게이트 테이블](#GA-또는-사용-중단된-기능을-위한-기능-게이트)에 나열할 수 있다.
- [GA/사용 중단 기능 게이트 테이블](#GA-또는-사용-중단된-기능을-위한-기능-게이트)에는
  사용 중단된 기능과 철회(withdrawn) 기능의 목록도 있다.

### 알파 또는 베타 기능을 위한 기능 게이트

{{< table caption="알파 또는 베타 단계에 있는 기능을 위한 기능 게이트" >}}

| 기능     | 디폴트    | 단계   | 도입   | 종료   |
|---------|---------|-------|-------|-------|
| `APIListChunking` | `false` | 알파 | 1.8 | 1.8 |
| `APIListChunking` | `true` | 베타 | 1.9 | |
| `APIPriorityAndFairness` | `false` | 알파 | 1.17 | 1.19 |
| `APIPriorityAndFairness` | `true` | 베타 | 1.20 | |
| `APIResponseCompression` | `false` | 알파 | 1.7 | 1.15 |
| `APIResponseCompression` | `true` | 베타 | 1.16 | |
| `APIServerIdentity` | `false` | 알파 | 1.20 | |
| `AllowInsecureBackendProxy` | `true` | 베타 | 1.17 | |
| `AnyVolumeDataSource` | `false` | 알파 | 1.18 | |
| `AppArmor` | `true` | 베타 | 1.4 | |
| `BalanceAttachedNodeVolumes` | `false` | 알파 | 1.11 | |
| `BoundServiceAccountTokenVolume` | `false` | 알파 | 1.13 | 1.20 |
| `BoundServiceAccountTokenVolume` | `true` | 베타 | 1.21 | |
| `CPUManager` | `false` | 알파 | 1.8 | 1.9 |
| `CPUManager` | `true` | 베타 | 1.10 | |
| `CSIInlineVolume` | `false` | 알파 | 1.15 | 1.15 |
| `CSIInlineVolume` | `true` | 베타 | 1.16 | - |
| `CSIMigration` | `false` | 알파 | 1.14 | 1.16 |
| `CSIMigration` | `true` | 베타 | 1.17 | |
| `CSIMigrationAWS` | `false` | 알파 | 1.14 | |
| `CSIMigrationAWS` | `false` | 베타 | 1.17 | |
| `CSIMigrationAWSComplete` | `false` | 알파 | 1.17 | |
| `CSIMigrationAzureDisk` | `false` | 알파 | 1.15 | 1.18 |
| `CSIMigrationAzureDisk` | `false` | 베타 | 1.19 | |
| `CSIMigrationAzureDiskComplete` | `false` | 알파 | 1.17 | |
| `CSIMigrationAzureFile` | `false` | 알파 | 1.15 | 1.19 |
| `CSIMigrationAzureFile` | `false` | 베타 | 1.21 | |
| `CSIMigrationAzureFileComplete` | `false` | 알파 | 1.17 | |
| `CSIMigrationGCE` | `false` | 알파 | 1.14 | 1.16 |
| `CSIMigrationGCE` | `false` | 베타 | 1.17 | |
| `CSIMigrationGCEComplete` | `false` | 알파 | 1.17 | |
| `CSIMigrationOpenStack` | `false` | 알파 | 1.14 | 1.17 |
| `CSIMigrationOpenStack` | `true` | 베타 | 1.18 | |
| `CSIMigrationOpenStackComplete` | `false` | 알파 | 1.17 | |
| `CSIMigrationvSphere` | `false` | 베타 | 1.19 | |
| `CSIMigrationvSphereComplete` | `false` | 베타 | 1.19 | |
| `CSIServiceAccountToken` | `false` | 알파 | 1.20 | 1.20 |
| `CSIServiceAccountToken` | `true` | 베타 | 1.21 | |
| `CSIStorageCapacity` | `false` | 알파 | 1.19 | 1.20 |
| `CSIStorageCapacity` | `true` | 베타 | 1.21 | |
| `CSIVolumeFSGroupPolicy` | `false` | 알파 | 1.19 | 1.19 |
| `CSIVolumeFSGroupPolicy` | `true` | 베타 | 1.20 | |
| `CSIVolumeHealth` | `false` | 알파 | 1.21 | |
| `ConfigurableFSGroupPolicy` | `false` | 알파 | 1.18 | 1.19 |
| `ConfigurableFSGroupPolicy` | `true` | 베타 | 1.20 | |
| `CronJobControllerV2` | `false` | 알파 | 1.20 | 1.20 |
| `CronJobControllerV2` | `true` | 베타 | 1.21 | |
| `CustomCPUCFSQuotaPeriod` | `false` | 알파 | 1.12 | |
| `DefaultPodTopologySpread` | `false` | 알파 | 1.19 | 1.19 |
| `DefaultPodTopologySpread` | `true` | 베타 | 1.20 | |
| `DevicePlugins` | `false` | 알파 | 1.8 | 1.9 |
| `DevicePlugins` | `true` | 베타 | 1.10 | |
| `DisableAcceleratorUsageMetrics` | `false` | 알파 | 1.19 | 1.19 |
| `DisableAcceleratorUsageMetrics` | `true` | 베타 | 1.20 | |
| `DownwardAPIHugePages` | `false` | 알파 | 1.20 | 1.20 |
| `DownwardAPIHugePages` | `false` | 베타 | 1.21 | |
| `DynamicKubeletConfig` | `false` | 알파 | 1.4 | 1.10 |
| `DynamicKubeletConfig` | `true` | 베타 | 1.11 | |
| `EfficientWatchResumption` | `false` | 알파 | 1.20 | |
| `EndpointSliceProxying` | `false` | 알파 | 1.18 | 1.18 |
| `EndpointSliceProxying` | `true` | 베타 | 1.19 | |
| `EndpointSliceTerminatingCondition` | `false` | 알파 | 1.20 | |
| `EphemeralContainers` | `false` | 알파 | 1.16 | |
| `ExpandCSIVolumes` | `false` | 알파 | 1.14 | 1.15 |
| `ExpandCSIVolumes` | `true` | 베타 | 1.16 | |
| `ExpandInUsePersistentVolumes` | `false` | 알파 | 1.11 | 1.14 |
| `ExpandInUsePersistentVolumes` | `true` | 베타 | 1.15 | |
| `ExpandPersistentVolumes` | `false` | 알파 | 1.8 | 1.10 |
| `ExpandPersistentVolumes` | `true` | 베타 | 1.11 | |
| `ExperimentalHostUserNamespaceDefaulting` | `false` | 베타 | 1.5 | |
| `GenericEphemeralVolume` | `false` | 알파 | 1.19 | 1.20 |
| `GenericEphemeralVolume` | `true` | 베타 | 1.21 | |
| `GracefulNodeShutdown` | `false` | 알파 | 1.20 | 1.20 |
| `GracefulNodeShutdown` | `true` | 베타 | 1.21 | |
| `HPAContainerMetrics` | `false` | 알파 | 1.20 | |
| `HPAScaleToZero` | `false` | 알파 | 1.16 | |
| `HugePageStorageMediumSize` | `false` | 알파 | 1.18 | 1.18 |
| `HugePageStorageMediumSize` | `true` | 베타 | 1.19 | |
| `IndexedJob` | `false` | 알파 | 1.21 | |
| `IngressClassNamespacedParams` | `false` | 알파 | 1.21 | |
| `IPv6DualStack` | `false` | 알파 | 1.15 | 1.20 |
| `IPv6DualStack` | `true` | 베타 | 1.21 | |
| `KubeletCredentialProviders` | `false` | 알파 | 1.20 | |
| `LegacyNodeRoleBehavior` | `false` | 알파 | 1.16 | 1.18 |
| `LegacyNodeRoleBehavior` | `true` | 베타 | 1.19 | 1.20 |
| `LocalStorageCapacityIsolation` | `false` | 알파 | 1.7 | 1.9 |
| `LocalStorageCapacityIsolation` | `true` | 베타 | 1.10 | |
| `LocalStorageCapacityIsolationFSQuotaMonitoring` | `false` | 알파 | 1.15 | |
| `LogarithmicScaleDown` | `false` | 알파 | 1.21 | |
| `KubeletPodResourcesGetAllocatable` | `false` | 알파 | 1.21 | |
| `MixedProtocolLBService` | `false` | 알파 | 1.20 | |
| `NamespaceDefaultLabelName` | `true` | 베타 | 1.21 | |
| `NetworkPolicyEndPort` | `false` | 알파 | 1.21 |  |
| `NodeDisruptionExclusion` | `false` | 알파 | 1.16 | 1.18 |
| `NodeDisruptionExclusion` | `true` | 베타 | 1.19 | 1.20 |
| `NonPreemptingPriority` | `false` | 알파 | 1.15 | 1.18 |
| `NonPreemptingPriority` | `true` | 베타 | 1.19 | |
| `PodDeletionCost` | `false` | 알파 | 1.21 | |
| `PodAffinityNamespaceSelector` | `false` | 알파 | 1.21 | |
| `PodOverhead` | `false` | 알파 | 1.16 | 1.17 |
| `PodOverhead` | `true` | 베타 | 1.18 |  |
| `ProbeTerminationGracePeriod` | `false` | 알파 | 1.21 | |
| `ProcMountType` | `false` | 알파 | 1.12 | |
| `QOSReserved` | `false` | 알파 | 1.11 | |
| `RemainingItemCount` | `false` | 알파 | 1.15 | |
| `RemoveSelfLink` | `false` | 알파 | 1.16 | 1.19 |
| `RemoveSelfLink` | `true` | 베타 | 1.20 | |
| `RotateKubeletServerCertificate` | `false` | 알파 | 1.7 | 1.11 |
| `RotateKubeletServerCertificate` | `true` | 베타 | 1.12 | |
| `RunAsGroup` | `true` | 베타 | 1.14 | |
| `ServerSideApply` | `false` | 알파 | 1.14 | 1.15 |
| `ServerSideApply` | `true` | 베타 | 1.16 | |
| `ServiceInternalTrafficPolicy` | `false` | 알파 | 1.21 | |
| `ServiceLBNodePortControl` | `false` | 알파 | 1.20 | |
| `ServiceLoadBalancerClass` | `false` | 알파 | 1.21 | |
| `ServiceNodeExclusion` | `false` | 알파 | 1.8 | 1.18 |
| `ServiceNodeExclusion` | `true` | 베타 | 1.19 | 1.20 |
| `ServiceTopology` | `false` | 알파 | 1.17 | |
| `SetHostnameAsFQDN` | `false` | 알파 | 1.19 | 1.19 |
| `SetHostnameAsFQDN` | `true` | 베타 | 1.20 | |
| `SizeMemoryBackedVolumes` | `false` | 알파 | 1.20 | |
| `StorageVersionAPI` | `false` | 알파 | 1.20 | |
| `StorageVersionHash` | `false` | 알파 | 1.14 | 1.14 |
| `StorageVersionHash` | `true` | 베타 | 1.15 | |
| `SuspendJob` | `false` | 알파 | 1.21 | |
| `TTLAfterFinished` | `false` | 알파 | 1.12 | 1.20 |
| `TTLAfterFinished` | `true` | 베타 | 1.21 | |
| `TopologyAwareHints` | `false` | 알파 | 1.21 | |
| `TopologyManager` | `false` | 알파 | 1.16 | 1.17 |
| `TopologyManager` | `true` | 베타 | 1.18 | |
| `ValidateProxyRedirects` | `false` | 알파 | 1.12 | 1.13 |
| `ValidateProxyRedirects` | `true` | 베타 | 1.14 | |
| `VolumeCapacityPriority` | `false` | 알파 | 1.21 | - |
| `WarningHeaders` | `true` | 베타 | 1.19 | |
| `WinDSR` | `false` | 알파 | 1.14 | |
| `WinOverlay` | `false` | 알파 | 1.14 | 1.19 |
| `WinOverlay` | `true` | 베타 | 1.20 | |
| `WindowsEndpointSliceProxying` | `false` | 알파 | 1.19 | 1.20 |
| `WindowsEndpointSliceProxying` | `true` | 베타 | 1.21 | |
{{< /table >}}

### GA 또는 사용 중단된 기능을 위한 기능 게이트

{{< table caption="GA 또는 사용 중단 기능을 위한 기능 게이트" >}}

| 기능     | 디폴트    | 단계   | 도입   | 종료   |
|---------|---------|-------|-------|-------|
| `Accelerators` | `false` | 알파 | 1.6 | 1.10 |
| `Accelerators` | - | 사용중단 | 1.11 | - |
| `AdvancedAuditing` | `false` | 알파 | 1.7 | 1.7 |
| `AdvancedAuditing` | `true` | 베타 | 1.8 | 1.11 |
| `AdvancedAuditing` | `true` | GA | 1.12 | - |
| `AffinityInAnnotations` | `false` | 알파 | 1.6 | 1.7 |
| `AffinityInAnnotations` | - | 사용중단 | 1.8 | - |
| `AllowExtTrafficLocalEndpoints` | `false` | 베타 | 1.4 | 1.6 |
| `AllowExtTrafficLocalEndpoints` | `true` | GA | 1.7 | - |
| `BlockVolume` | `false` | 알파 | 1.9 | 1.12 |
| `BlockVolume` | `true` | 베타 | 1.13 | 1.17 |
| `BlockVolume` | `true` | GA | 1.18 | - |
| `CRIContainerLogRotation` | `false` | 알파 | 1.10 | 1.10 |
| `CRIContainerLogRotation` | `true` | 베타 | 1.11 | 1.20 |
| `CRIContainerLogRotation` | `true` | GA | 1.21 | - |
| `CSIBlockVolume` | `false` | 알파 | 1.11 | 1.13 |
| `CSIBlockVolume` | `true` | 베타 | 1.14 | 1.17 |
| `CSIBlockVolume` | `true` | GA | 1.18 | - |
| `CSIDriverRegistry` | `false` | 알파 | 1.12 | 1.13 |
| `CSIDriverRegistry` | `true` | 베타 | 1.14 | 1.17 |
| `CSIDriverRegistry` | `true` | GA | 1.18 | |
| `CSINodeInfo` | `false` | 알파 | 1.12 | 1.13 |
| `CSINodeInfo` | `true` | 베타 | 1.14 | 1.16 |
| `CSINodeInfo` | `true` | GA | 1.17 | |
| `AttachVolumeLimit` | `false` | 알파 | 1.11 | 1.11 |
| `AttachVolumeLimit` | `true` | 베타 | 1.12 | 1.16 |
| `AttachVolumeLimit` | `true` | GA | 1.17 | - |
| `CSIPersistentVolume` | `false` | 알파 | 1.9 | 1.9 |
| `CSIPersistentVolume` | `true` | 베타 | 1.10 | 1.12 |
| `CSIPersistentVolume` | `true` | GA | 1.13 | - |
| `CustomPodDNS` | `false` | 알파 | 1.9 | 1.9 |
| `CustomPodDNS` | `true` | 베타| 1.10 | 1.13 |
| `CustomPodDNS` | `true` | GA | 1.14 | - |
| `CustomResourceDefaulting` | `false` | 알파| 1.15 | 1.15 |
| `CustomResourceDefaulting` | `true` | 베타 | 1.16 | 1.16 |
| `CustomResourceDefaulting` | `true` | GA | 1.17 | - |
| `CustomResourcePublishOpenAPI` | `false` | 알파| 1.14 | 1.14 |
| `CustomResourcePublishOpenAPI` | `true` | 베타| 1.15 | 1.15 |
| `CustomResourcePublishOpenAPI` | `true` | GA | 1.16 | - |
| `CustomResourceSubresources` | `false` | 알파 | 1.10 | 1.10 |
| `CustomResourceSubresources` | `true` | 베타 | 1.11 | 1.15 |
| `CustomResourceSubresources` | `true` | GA | 1.16 | - |
| `CustomResourceValidation` | `false` | 알파 | 1.8 | 1.8 |
| `CustomResourceValidation` | `true` | 베타 | 1.9 | 1.15 |
| `CustomResourceValidation` | `true` | GA | 1.16 | - |
| `CustomResourceWebhookConversion` | `false` | 알파 | 1.13 | 1.14 |
| `CustomResourceWebhookConversion` | `true` | 베타 | 1.15 | 1.15 |
| `CustomResourceWebhookConversion` | `true` | GA | 1.16 | - |
| `DryRun` | `false` | 알파 | 1.12 | 1.12 |
| `DryRun` | `true` | 베타 | 1.13 | 1.18 |
| `DryRun` | `true` | GA | 1.19 | - |
| `DynamicAuditing` | `false` | 알파 | 1.13 | 1.18 |
| `DynamicAuditing` | - | 사용중단 | 1.19 | - |
| `DynamicProvisioningScheduling` | `false` | 알파 | 1.11 | 1.11 |
| `DynamicProvisioningScheduling` | - | 사용중단| 1.12 | - |
| `DynamicVolumeProvisioning` | `true` | 알파 | 1.3 | 1.7 |
| `DynamicVolumeProvisioning` | `true` | GA | 1.8 | - |
| `EnableAggregatedDiscoveryTimeout` | `true` | 사용중단 | 1.16 | - |
| `EnableEquivalenceClassCache` | `false` | 알파 | 1.8 | 1.14 |
| `EnableEquivalenceClassCache` | - | 사용중단 | 1.15 | - |
| `EndpointSlice` | `false` | 알파 | 1.16 | 1.16 |
| `EndpointSlice` | `false` | 베타 | 1.17 | 1.17 |
| `EndpointSlice` | `true` | 베타 | 1.18 | 1.20 |
| `EndpointSlice` | `true` | GA | 1.21 | -  |
| `EndpointSliceNodeName` | `false` | 알파 | 1.20 | 1.20 |
| `EndpointSliceNodeName` | `true` | GA | 1.21 | - |
| `ExperimentalCriticalPodAnnotation` | `false` | 알파 | 1.5 | 1.12 |
| `ExperimentalCriticalPodAnnotation` | `false` | 사용중단 | 1.13 | - |
| `EvenPodsSpread` | `false` | 알파 | 1.16 | 1.17 |
| `EvenPodsSpread` | `true` | 베타 | 1.18 | 1.18 |
| `EvenPodsSpread` | `true` | GA | 1.19 | - |
| `ExecProbeTimeout` | `true` | GA | 1.20 | - |
| `ExternalPolicyForExternalIP` | `true` | GA | 1.18 | - |
| `GCERegionalPersistentDisk` | `true` | 베타 | 1.10 | 1.12 |
| `GCERegionalPersistentDisk` | `true` | GA | 1.13 | - |
| `HugePages` | `false` | 알파 | 1.8 | 1.9 |
| `HugePages` | `true` | 베타| 1.10 | 1.13 |
| `HugePages` | `true` | GA | 1.14 | - |
| `HyperVContainer` | `false` | 알파 | 1.10 | 1.19 |
| `HyperVContainer` | `false` | 사용중단 | 1.20 | - |
| `ImmutableEphemeralVolumes` | `false` | 알파 | 1.18 | 1.18 |
| `ImmutableEphemeralVolumes` | `true` | 베타 | 1.19 | 1.20 |
| `ImmutableEphemeralVolumes` | `true` | GA | 1.21 | |
| `Initializers` | `false` | 알파 | 1.7 | 1.13 |
| `Initializers` | - | 사용중단 | 1.14 | - |
| `KubeletConfigFile` | `false` | 알파 | 1.8 | 1.9 |
| `KubeletConfigFile` | - | 사용중단 | 1.10 | - |
| `KubeletPluginsWatcher` | `false` | 알파 | 1.11 | 1.11 |
| `KubeletPluginsWatcher` | `true` | 베타 | 1.12 | 1.12 |
| `KubeletPluginsWatcher` | `true` | GA | 1.13 | - |
| `KubeletPodResources` | `false` | 알파 | 1.13 | 1.14 |
| `KubeletPodResources` | `true` | 베타 | 1.15 | |
| `KubeletPodResources` | `true` | GA | 1.20 | |
| `LegacyNodeRoleBehavior` | `false` | GA | 1.21 | - |
| `MountContainers` | `false` | 알파 | 1.9 | 1.16 |
| `MountContainers` | `false` | 사용중단 | 1.17 | - |
| `MountPropagation` | `false` | 알파 | 1.8 | 1.9 |
| `MountPropagation` | `true` | 베타 | 1.10 | 1.11 |
| `MountPropagation` | `true` | GA | 1.12 | - |
| `NodeDisruptionExclusion` | `true` | GA | 1.21 | - |
| `NodeLease` | `false` | 알파 | 1.12 | 1.13 |
| `NodeLease` | `true` | 베타 | 1.14 | 1.16 |
| `NodeLease` | `true` | GA | 1.17 | - |
| `PVCProtection` | `false` | 알파 | 1.9 | 1.9 |
| `PVCProtection` | - | 사용중단 | 1.10 | - |
| `PersistentLocalVolumes` | `false` | 알파 | 1.7 | 1.9 |
| `PersistentLocalVolumes` | `true` | 베타 | 1.10 | 1.13 |
| `PersistentLocalVolumes` | `true` | GA | 1.14 | - |
| `PodDisruptionBudget` | `false` | 알파 | 1.3 | 1.4 |
| `PodDisruptionBudget` | `true` | 베타 | 1.5 | 1.20 |
| `PodDisruptionBudget` | `true` | GA | 1.21 | - |
| `PodPriority` | `false` | 알파 | 1.8 | 1.10 |
| `PodPriority` | `true` | 베타 | 1.11 | 1.13 |
| `PodPriority` | `true` | GA | 1.14 | - |
| `PodReadinessGates` | `false` | 알파 | 1.11 | 1.11 |
| `PodReadinessGates` | `true` | 베타 | 1.12 | 1.13 |
| `PodReadinessGates` | `true` | GA | 1.14 | - |
| `PodShareProcessNamespace` | `false` | 알파 | 1.10 | 1.11 |
| `PodShareProcessNamespace` | `true` | 베타 | 1.12 | 1.16 |
| `PodShareProcessNamespace` | `true` | GA | 1.17 | - |
| `RequestManagement` | `false` | 알파 | 1.15 | 1.16 |
| `RequestManagement` | - | 사용중단 | 1.17 | - |
| `ResourceLimitsPriorityFunction` | `false` | 알파 | 1.9 | 1.18 |
| `ResourceLimitsPriorityFunction` | - | 사용중단 | 1.19 | - |
| `ResourceQuotaScopeSelectors` | `false` | 알파 | 1.11 | 1.11 |
| `ResourceQuotaScopeSelectors` | `true` | 베타 | 1.12 | 1.16 |
| `ResourceQuotaScopeSelectors` | `true` | GA | 1.17 | - |
| `RootCAConfigMap` | `false` | 알파 | 1.13 | 1.19 |
| `RootCAConfigMap` | `true` | 베타 | 1.20 | 1.20 |
| `RootCAConfigMap` | `true` | GA | 1.21 | - |
| `RotateKubeletClientCertificate` | `true` | 베타 | 1.8 | 1.18 |
| `RotateKubeletClientCertificate` | `true` | GA | 1.19 | - |
| `RuntimeClass` | `false` | 알파 | 1.12 | 1.13 |
| `RuntimeClass` | `true` | 베타 | 1.14 | 1.19 |
| `RuntimeClass` | `true` | GA | 1.20 | - |
| `ScheduleDaemonSetPods` | `false` | 알파 | 1.11 | 1.11 |
| `ScheduleDaemonSetPods` | `true` | 베타 | 1.12 | 1.16  |
| `ScheduleDaemonSetPods` | `true` | GA | 1.17 | - |
| `SCTPSupport` | `false` | 알파 | 1.12 | 1.18 |
| `SCTPSupport` | `true` | 베타 | 1.19 | 1.19 |
| `SCTPSupport` | `true` | GA | 1.20 | - |
| `ServiceAccountIssuerDiscovery` | `false` | 알파 | 1.18 | 1.19 |
| `ServiceAccountIssuerDiscovery` | `true` | 베타 | 1.20 | 1.20 |
| `ServiceAccountIssuerDiscovery` | `true` | GA | 1.21 | - |
| `ServiceAppProtocol` | `false` | 알파 | 1.18 | 1.18 |
| `ServiceAppProtocol` | `true` | 베타 | 1.19 | 1.19 |
| `ServiceAppProtocol` | `true` | GA | 1.20 | - |
| `ServiceLoadBalancerFinalizer` | `false` | 알파 | 1.15 | 1.15 |
| `ServiceLoadBalancerFinalizer` | `true` | 베타 | 1.16 | 1.16 |
| `ServiceLoadBalancerFinalizer` | `true` | GA | 1.17 | - |
| `ServiceNodeExclusion` | `true` | GA | 1.21 | - |
| `StartupProbe` | `false` | 알파 | 1.16 | 1.17 |
| `StartupProbe` | `true` | 베타 | 1.18 | 1.19 |
| `StartupProbe` | `true` | GA | 1.20 | - |
| `StorageObjectInUseProtection` | `true` | 베타 | 1.10 | 1.10 |
| `StorageObjectInUseProtection` | `true` | GA | 1.11 | - |
| `StreamingProxyRedirects` | `false` | 베타 | 1.5 | 1.5 |
| `StreamingProxyRedirects` | `true` | 베타 | 1.6 | 1.18 |
| `StreamingProxyRedirects` | - | GA | 1.19 | - |
| `SupportIPVSProxyMode` | `false` | 알파 | 1.8 | 1.8 |
| `SupportIPVSProxyMode` | `false` | 베타 | 1.9 | 1.9 |
| `SupportIPVSProxyMode` | `true` | 베타 | 1.10 | 1.10 |
| `SupportIPVSProxyMode` | `true` | GA | 1.11 | - |
| `SupportNodePidsLimit` | `false` | 알파 | 1.14 | 1.14 |
| `SupportNodePidsLimit` | `true` | 베타 | 1.15 | 1.19 |
| `SupportNodePidsLimit` | `true` | GA | 1.20 | - |
| `SupportPodPidsLimit` | `false` | 알파 | 1.10 | 1.13 |
| `SupportPodPidsLimit` | `true` | 베타 | 1.14 | 1.19 |
| `SupportPodPidsLimit` | `true` | GA | 1.20 | - |
| `Sysctls` | `true` | 베타 | 1.11 | 1.20 |
| `Sysctls` | `true` | GA | 1.21 | |
| `TaintBasedEvictions` | `false` | 알파 | 1.6 | 1.12 |
| `TaintBasedEvictions` | `true` | 베타 | 1.13 | 1.17 |
| `TaintBasedEvictions` | `true` | GA | 1.18 | - |
| `TaintNodesByCondition` | `false` | 알파 | 1.8 | 1.11 |
| `TaintNodesByCondition` | `true` | 베타 | 1.12 | 1.16 |
| `TaintNodesByCondition` | `true` | GA | 1.17 | - |
| `TokenRequest` | `false` | 알파 | 1.10 | 1.11 |
| `TokenRequest` | `true` | 베타 | 1.12 | 1.19 |
| `TokenRequest` | `true` | GA | 1.20 | - |
| `TokenRequestProjection` | `false` | 알파 | 1.11 | 1.11 |
| `TokenRequestProjection` | `true` | 베타 | 1.12 | 1.19 |
| `TokenRequestProjection` | `true` | GA | 1.20 | - |
| `VolumeCapacityPriority` | `false` | 알파 | 1.21 | - |
| `VolumePVCDataSource` | `false` | 알파 | 1.15 | 1.15 |
| `VolumePVCDataSource` | `true` | 베타 | 1.16 | 1.17 |
| `VolumePVCDataSource` | `true` | GA | 1.18 | - |
| `VolumeScheduling` | `false` | 알파 | 1.9 | 1.9 |
| `VolumeScheduling` | `true` | 베타 | 1.10 | 1.12 |
| `VolumeScheduling` | `true` | GA | 1.13 | - |
| `VolumeSnapshotDataSource` | `false` | 알파 | 1.12 | 1.16 |
| `VolumeSnapshotDataSource` | `true` | 베타 | 1.17 | 1.19 |
| `VolumeSnapshotDataSource` | `true` | GA | 1.20 | - |
| `VolumeSubpath` | `true` | GA | 1.10 | - |
| `VolumeSubpathEnvExpansion` | `false` | 알파 | 1.14 | 1.14 |
| `VolumeSubpathEnvExpansion` | `true` | 베타 | 1.15 | 1.16 |
| `VolumeSubpathEnvExpansion` | `true` | GA | 1.17 | - |
| `WatchBookmark` | `false` | 알파 | 1.15 | 1.15 |
| `WatchBookmark` | `true` | 베타 | 1.16 | 1.16 |
| `WatchBookmark` | `true` | GA | 1.17 | - |
| `WindowsGMSA` | `false` | 알파 | 1.14 | 1.15 |
| `WindowsGMSA` | `true` | 베타 | 1.16 | 1.17 |
| `WindowsGMSA` | `true` | GA | 1.18 | - |
| `WindowsRunAsUserName` | `false` | 알파 | 1.16 | 1.16 |
| `WindowsRunAsUserName` | `true` | 베타 | 1.17 | 1.17 |
| `WindowsRunAsUserName` | `true` | GA | 1.18 | - |
{{< /table >}}

## 기능 사용

### 기능 단계

기능은 *알파*, *베타* 또는 *GA* 단계일 수 있다.
*알파* 기능은 다음을 의미한다.

* 기본적으로 비활성화되어 있다.
* 버그가 있을 수 있다. 이 기능을 사용하면 버그에 노출될 수 있다.
* 기능에 대한 지원은 사전 통지없이 언제든지 중단될 수 있다.
* API는 이후 소프트웨어 릴리스에서 예고없이 호환되지 않는 방식으로 변경될 수 있다.
* 버그의 위험이 증가하고 장기 지원이 부족하여, 단기 테스트
  클러스터에서만 사용하는 것이 좋다.

*베타* 기능은 다음을 의미한다.

* 기본적으로 활성화되어 있다.
* 이 기능은 잘 테스트되었다. 이 기능을 활성화하면 안전한 것으로 간주된다.
* 세부 내용은 변경될 수 있지만, 전체 기능에 대한 지원은 중단되지 않는다.
* 오브젝트의 스키마 및/또는 시맨틱은 후속 베타 또는 안정 릴리스에서
  호환되지 않는 방식으로 변경될 수 있다. 이러한 상황이 발생하면, 다음 버전으로 마이그레이션하기 위한
  지침을 제공한다. API 오브젝트를 삭제, 편집 및 재작성해야
  할 수도 있다. 편집 과정에서 약간의 생각이 필요할 수 있다.
 해당 기능에 의존하는 애플리케이션의 경우 다운타임이 필요할 수 있다.
* 후속 릴리스에서 호환되지 않는 변경이 발생할 수 있으므로
  업무상 중요하지 않은(non-business-critical) 용도로만
  권장한다. 독립적으로 업그레이드할 수 있는 여러 클러스터가 있는 경우, 이 제한을 완화할 수 있다.

{{< note >}}
*베타* 기능을 사용해 보고 의견을 보내주길 바란다!
베타 기간이 종료된 후에는, 더 많은 변경을 하는 것이 실용적이지 않을 수 있다.
{{< /note >}}

*GA*(General Availability) 기능은 *안정* 기능이라고도 한다. 이 의미는 다음과 같다.

* 이 기능은 항상 활성화되어 있다. 비활성화할 수 없다.
* 해당 기능 게이트는 더 이상 필요하지 않다.
* 여러 후속 버전의 릴리스된 소프트웨어에 안정적인 기능의 버전이 포함된다.

## 기능 게이트 목록 {#feature-gates}

각 기능 게이트는 특정 기능을 활성화/비활성화하도록 설계되었다.

- `APIListChunking`: API 클라이언트가 API 서버에서 (`LIST` 또는 `GET`)
  리소스를 청크(chunks)로 검색할 수 있도록 한다.
- `APIPriorityAndFairness`: 각 서버의 우선 순위와 공정성을 통해 동시 요청을
  관리할 수 있다. (`RequestManagement` 에서 이름이 변경됨)
- `APIResponseCompression`: `LIST` 또는 `GET` 요청에 대한 API 응답을 압축한다.
- `APIServerIdentity`: 클러스터의 각 API 서버에 ID를 할당한다.
- `Accelerators`: 도커 사용 시 Nvidia GPU 지원 활성화한다.
- `AdvancedAuditing`: [고급 감사](/docs/tasks/debug-application-cluster/audit/#advanced-audit) 기능을 활성화한다.
- `AffinityInAnnotations`: [파드 어피니티 또는 안티-어피니티](/ko/docs/concepts/scheduling-eviction/assign-pod-node/#어피니티-affinity-와-안티-어피니티-anti-affinity)
  설정을 활성화한다.
- `AllowExtTrafficLocalEndpoints`: 서비스가 외부 요청을 노드의 로컬 엔드포인트로 라우팅할 수 있도록 한다.
- `AllowInsecureBackendProxy`: 사용자가 파드 로그 요청에서 kubelet의
  TLS 확인을 건너뛸 수 있도록 한다.
- `AnyVolumeDataSource`: {{< glossary_tooltip text="PVC" term_id="persistent-volume-claim" >}}의
  `DataSource` 로 모든 사용자 정의 리소스 사용을 활성화한다.
- `AppArmor`: 도커를 사용할 때 리눅스 노드에서 AppArmor 기반의 필수 접근 제어를 활성화한다.
  자세한 내용은 [AppArmor 튜토리얼](/ko/docs/tutorials/clusters/apparmor/)을 참고한다.
- `AttachVolumeLimit`: 볼륨 플러그인이 노드에 연결될 수 있는 볼륨 수에
  대한 제한을 보고하도록 한다.
  자세한 내용은 [동적 볼륨 제한](/ko/docs/concepts/storage/storage-limits/#동적-볼륨-한도)을 참고한다.
- `BalanceAttachedNodeVolumes`: 스케줄링 시 균형 잡힌 리소스 할당을 위해 고려할 노드의 볼륨 수를
  포함한다. 스케줄러가 결정을 내리는 동안 CPU, 메모리 사용률 및 볼륨 수가
  더 가까운 노드가 선호된다.
- `BlockVolume`: 파드에서 원시 블록 장치의 정의와 사용을 활성화한다.
  자세한 내용은 [원시 블록 볼륨 지원](/ko/docs/concepts/storage/persistent-volumes/#원시-블록-볼륨-지원)을
  참고한다.
- `BoundServiceAccountTokenVolume`: ServiceAccountTokenVolumeProjection으로 구성된 프로젝션 볼륨을 사용하도록 서비스어카운트 볼륨을
  마이그레이션한다. 클러스터 관리자는 `serviceaccount_stale_tokens_total` 메트릭을 사용하여
  확장 토큰에 의존하는 워크로드를 모니터링 할 수 있다. 이러한 워크로드가 없는 경우 `--service-account-extend-token-expiration=false` 플래그로
  `kube-apiserver`를 시작하여 확장 토큰 기능을 끈다.
  자세한 내용은 [바운드 서비스 계정 토큰](https://github.com/kubernetes/enhancements/blob/master/keps/sig-auth/1205-bound-service-account-tokens/README.md)을
  확인한다.
- `CPUManager`: 컨테이너 수준의 CPU 어피니티 지원을 활성화한다.
  [CPU 관리 정책](/docs/tasks/administer-cluster/cpu-management-policies/)을 참고한다.
- `CRIContainerLogRotation`: cri 컨테이너 런타임에 컨테이너 로그 로테이션을 활성화한다. 로그 파일 사이즈 기본값은 10MB이며,
컨테이너 당 최대 로그 파일 수 기본값은 5이다. 이 값은 kubelet 환경설정으로 변경할 수 있다.
더 자세한 내용은 [노드 레벨에서의 로깅](/ko/docs/concepts/cluster-administration/logging/#노드-레벨에서의-로깅)을 참고한다.
- `CSIBlockVolume`: 외부 CSI 볼륨 드라이버가 블록 스토리지를 지원할 수 있게 한다.
  자세한 내용은 [`csi` 원시 블록 볼륨 지원](/ko/docs/concepts/storage/volumes/#csi-원시-raw-블록-볼륨-지원)
  문서를 참고한다.
- `CSIDriverRegistry`: csi.storage.k8s.io에서 CSIDriver API 오브젝트와 관련된
  모든 로직을 활성화한다.
- `CSIInlineVolume`: 파드에 대한 CSI 인라인 볼륨 지원을 활성화한다.
- `CSIMigration`: shim 및 변환 로직을 통해 볼륨 작업을 인-트리 플러그인에서
  사전 설치된 해당 CSI 플러그인으로 라우팅할 수 있다.
- `CSIMigrationAWS`: shim 및 변환 로직을 통해 볼륨 작업을
  AWS-EBS 인-트리 플러그인에서 EBS CSI 플러그인으로 라우팅할 수 있다. 노드에
  EBS CSI 플러그인이 설치와 구성이 되어 있지 않은 경우 인-트리 EBS 플러그인으로
  폴백(falling back)을 지원한다. CSIMigration 기능 플래그가 필요하다.
- `CSIMigrationAWSComplete`: kubelet 및 볼륨 컨트롤러에서 EBS 인-트리
  플러그인 등록을 중지하고 shim 및 변환 로직을 사용하여 볼륨 작업을 AWS-EBS
  인-트리 플러그인에서 EBS CSI 플러그인으로 라우팅할 수 있다.
  클러스터의 모든 노드에 CSIMigration과 CSIMigrationAWS 기능 플래그가 활성화되고
  EBS CSI 플러그인이 설치 및 구성이 되어 있어야 한다.
- `CSIMigrationAzureDisk`: shim 및 변환 로직을 통해 볼륨 작업을
  Azure-Disk 인-트리 플러그인에서 AzureDisk CSI 플러그인으로 라우팅할 수 있다.
  노드에 AzureDisk CSI 플러그인이 설치와 구성이 되어 있지 않은 경우 인-트리
  AzureDisk 플러그인으로 폴백을 지원한다. CSIMigration 기능 플래그가
  필요하다.
- `CSIMigrationAzureDiskComplete`: kubelet 및 볼륨 컨트롤러에서 Azure-Disk 인-트리
  플러그인 등록을 중지하고 shim 및 변환 로직을 사용하여 볼륨 작업을
  Azure-Disk 인-트리 플러그인에서 AzureDisk CSI 플러그인으로
  라우팅할 수 있다. 클러스터의 모든 노드에 CSIMigration과 CSIMigrationAzureDisk 기능
  플래그가 활성화되고 AzureDisk CSI 플러그인이 설치 및 구성이 되어
  있어야 한다.
- `CSIMigrationAzureFile`: shim 및 변환 로직을 통해 볼륨 작업을
  Azure-File 인-트리 플러그인에서 AzureFile CSI 플러그인으로 라우팅할 수 있다.
  노드에 AzureFile CSI 플러그인이 설치 및 구성이 되어 있지 않은 경우 인-트리
  AzureFile 플러그인으로 폴백을 지원한다. CSIMigration 기능 플래그가
  필요하다.
- `CSIMigrationAzureFileComplete`: kubelet 및 볼륨 컨트롤러에서 Azure 파일 인-트리
  플러그인 등록을 중지하고 shim 및 변환 로직을 통해 볼륨 작업을
  Azure 파일 인-트리 플러그인에서 AzureFile CSI 플러그인으로
  라우팅할 수 있다. 클러스터의 모든 노드에 CSIMigration과 CSIMigrationAzureFile 기능
  플래그가 활성화되고 AzureFile CSI 플러그인이 설치 및 구성이 되어
  있어야 한다.
- `CSIMigrationGCE`: shim 및 변환 로직을 통해 볼륨 작업을
  GCE-PD 인-트리 플러그인에서 PD CSI 플러그인으로 라우팅할 수 있다. 노드에
  PD CSI 플러그인이 설치 및 구성이 되어 있지 않은 경우 인-트리 GCE 플러그인으로 폴백을
  지원한다. CSIMigration 기능 플래그가 필요하다.
- `CSIMigrationGCEComplete`: kubelet 및 볼륨 컨트롤러에서 GCE-PD
  인-트리 플러그인 등록을 중지하고 shim 및 변환 로직을 통해 볼륨 작업을 GCE-PD
  인-트리 플러그인에서 PD CSI 플러그인으로 라우팅할 수 있다.
  CSIMigration과 CSIMigrationGCE 기능 플래그가 활성화되고 PD CSI
  플러그인이 클러스터의 모든 노드에 설치 및 구성이 되어 있어야 한다.
- `CSIMigrationOpenStack`: shim 및 변환 로직을 통해 볼륨 작업을
  Cinder 인-트리 플러그인에서 Cinder CSI 플러그인으로 라우팅할 수 있다. 노드에
  Cinder CSI 플러그인이 설치 및 구성이 되어 있지 않은 경우 인-트리
  Cinder 플러그인으로 폴백을 지원한다. CSIMigration 기능 플래그가 필요하다.
- `CSIMigrationOpenStackComplete`: kubelet 및 볼륨 컨트롤러에서
  Cinder 인-트리 플러그인 등록을 중지하고 shim 및 변환 로직이 Cinder 인-트리
  플러그인에서 Cinder CSI 플러그인으로 볼륨 작업을 라우팅할 수 있도록 한다.
  클러스터의 모든 노드에 CSIMigration과 CSIMigrationOpenStack 기능 플래그가 활성화되고
  Cinder CSI 플러그인이 설치 및 구성이 되어 있어야 한다.
- `CSIMigrationvSphere`: vSphere 인-트리 플러그인에서 vSphere CSI 플러그인으로 볼륨 작업을
  라우팅하는 shim 및 변환 로직을 사용한다.
  노드에 vSphere CSI 플러그인이 설치 및 구성이 되어 있지 않은 경우
  인-트리 vSphere 플러그인으로 폴백을 지원한다. CSIMigration 기능 플래그가 필요하다.
- `CSIMigrationvSphereComplete`: kubelet 및 볼륨 컨트롤러에서 vSphere 인-트리
  플러그인 등록을 중지하고 shim 및 변환 로직을 활성화하여 vSphere 인-트리 플러그인에서
  vSphere CSI 플러그인으로 볼륨 작업을 라우팅할 수 있도록 한다. CSIMigration 및
  CSIMigrationvSphere 기능 플래그가 활성화되고 vSphere CSI 플러그인이
  클러스터의 모든 노드에 설치 및 구성이 되어 있어야 한다.
- `CSINodeInfo`: csi.storage.k8s.io에서 CSINodeInfo API 오브젝트와 관련된 모든 로직을 활성화한다.
- `CSIPersistentVolume`: [CSI (Container Storage Interface)](https://github.com/kubernetes/community/blob/master/contributors/design-proposals/storage/container-storage-interface.md)
  호환 볼륨 플러그인을 통해 프로비저닝된 볼륨을 감지하고
  마운트할 수 있다.
- `CSIServiceAccountToken` : 볼륨을 마운트하는 파드의 서비스 계정 토큰을 받을 수 있도록
  CSI 드라이버를 활성화한다.
  [토큰 요청](https://kubernetes-csi.github.io/docs/token-requests.html)을 참조한다.
- `CSIStorageCapacity`: CSI 드라이버가 스토리지 용량 정보를 게시하고
  쿠버네티스 스케줄러가 파드를 스케줄할 때 해당 정보를 사용하도록 한다.
  [스토리지 용량](/docs/concepts/storage/storage-capacity/)을 참고한다.
  자세한 내용은 [`csi` 볼륨 유형](/ko/docs/concepts/storage/volumes/#csi) 문서를 확인한다.
- `CSIVolumeFSGroupPolicy`: CSI드라이버가 `fsGroupPolicy` 필드를 사용하도록 허용한다.
  이 필드는 CSI드라이버에서 생성된 볼륨이 마운트될 때 볼륨 소유권과
  권한 수정을 지원하는지 여부를 제어한다.
- `CSIVolumeHealth`: 노드에서의 CSI 볼륨 상태 모니터링 기능을 활성화한다.
- `ConfigurableFSGroupPolicy`: 사용자가 파드에 볼륨을 마운트할 때 fsGroups에 대한
  볼륨 권한 변경 정책을 구성할 수 있다. 자세한 내용은
  [파드의 볼륨 권한 및 소유권 변경 정책 구성](/docs/tasks/configure-pod-container/security-context/#configure-volume-permission-and-ownership-change-policy-for-pods)을
  참고한다.
- `CronJobControllerV2`: {{< glossary_tooltip text="크론잡(CronJob)" term_id="cronjob" >}}
  컨트롤러의 대체 구현을 사용한다. 그렇지 않으면,
  동일한 컨트롤러의 버전 1이 선택된다.
  버전 2 컨트롤러는 실험적인 성능 향상을 제공한다.
- `CustomCPUCFSQuotaPeriod`: [kubelet config](/docs/tasks/administer-cluster/kubelet-config-file/)에서
  `cpuCFSQuotaPeriod` 를 노드가 변경할 수 있도록 한다.
- `CustomPodDNS`: `dnsConfig` 속성을 사용하여 파드의 DNS 설정을 사용자 정의할 수 있다.
  자세한 내용은 [파드의 DNS 설정](/ko/docs/concepts/services-networking/dns-pod-service/#pod-dns-config)을
  확인한다.
- `CustomResourceDefaulting`: OpenAPI v3 유효성 검사 스키마에서 기본값에 대한 CRD 지원을 활성화한다.
- `CustomResourcePublishOpenAPI`: CRD OpenAPI 사양을 게시할 수 있다.
- `CustomResourceSubresources`: [커스텀리소스데피니션](/ko/docs/concepts/extend-kubernetes/api-extension/custom-resources/)에서
  생성된 리소스에서 `/status` 및 `/scale` 하위 리소스를 활성화한다.
- `CustomResourceValidation`: [커스텀리소스데피니션](/ko/docs/concepts/extend-kubernetes/api-extension/custom-resources/)에서
  생성된 리소스에서 스키마 기반 유효성 검사를 활성화한다.
- `CustomResourceWebhookConversion`: [커스텀리소스데피니션](/ko/docs/concepts/extend-kubernetes/api-extension/custom-resources/)에서
  생성된 리소스에 대해 웹 훅 기반의 변환을 활성화한다.
- `DefaultPodTopologySpread`: `PodTopologySpread` 스케줄링 플러그인을 사용하여
  [기본 분배](/ko/docs/concepts/workloads/pods/pod-topology-spread-constraints/#내부-기본-제약)를 수행한다.
- `DevicePlugins`: 노드에서 [장치 플러그인](/ko/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/)
  기반 리소스 프로비저닝을 활성화한다.
- `DisableAcceleratorUsageMetrics`:
  [kubelet이 수집한 액셀러레이터 지표 비활성화](/ko/docs/concepts/cluster-administration/system-metrics/#액셀러레이터-메트릭-비활성화).
- `DownwardAPIHugePages`: [다운워드 API](/docs/tasks/inject-data-application/downward-api-volume-expose-pod-information)에서
  hugepages 사용을 활성화한다.
- `DryRun`: 서버 측의 [dry run](/docs/reference/using-api/api-concepts/#dry-run) 요청을
  요청을 활성화하여 커밋하지 않고 유효성 검사, 병합 및 변화를 테스트할 수 있다.
- `DynamicAuditing`: v1.19 이전의 버전에서 동적 감사를 활성화하는 데 사용된다.
- `DynamicKubeletConfig`: kubelet의 동적 구성을 활성화한다.
  [kubelet 재구성](/docs/tasks/administer-cluster/reconfigure-kubelet/)을 참고한다.
- `DynamicProvisioningScheduling`: 볼륨 토폴로지를 인식하고 PV 프로비저닝을 처리하도록
  기본 스케줄러를 확장한다.
  이 기능은 v1.12의 `VolumeScheduling` 기능으로 대체되었다.
- `DynamicVolumeProvisioning`: 파드에 퍼시스턴트 볼륨의
  [동적 프로비저닝](/ko/docs/concepts/storage/dynamic-provisioning/)을 활성화한다.
- `EfficientWatchResumption`: 스토리지에서 생성된 북마크(진행
  알림) 이벤트를 사용자에게 전달할 수 있다. 이것은 감시 작업에만
  적용된다.
- `EnableAggregatedDiscoveryTimeout`: 수집된 검색 호출에서 5초
  시간 초과를 활성화한다.
- `EnableEquivalenceClassCache`: 스케줄러가 파드를 스케줄링할 때 노드의
  동등성을 캐시할 수 있게 한다.
- `EndpointSlice`: 보다 스케일링 가능하고 확장 가능한 네트워크 엔드포인트에 대한
  엔드포인트슬라이스(EndpointSlices)를 활성화한다. [엔드포인트슬라이스 활성화](/ko/docs/concepts/services-networking/endpoint-slices/)를 참고한다.
- `EndpointSliceNodeName` : 엔드포인트슬라이스 `nodeName` 필드를 활성화한다.
- `EndpointSliceProxying`: 활성화되면, 리눅스에서 실행되는
  kube-proxy는 엔드포인트 대신 엔드포인트슬라이스를
  기본 데이터 소스로 사용하여 확장성과 성능을 향상시킨다.
  [엔드포인트슬라이스 활성화](/ko/docs/concepts/services-networking/endpoint-slices/)를 참고한다.
- `EndpointSliceTerminatingCondition`: 엔드포인트슬라이스 `terminating` 및 `serving`
  조건 필드를 활성화한다.
- `EphemeralContainers`: 파드를 실행하기 위한
  {{< glossary_tooltip text="임시 컨테이너" term_id="ephemeral-container" >}}를
  추가할 수 있다.
- `EvenPodsSpread`: 토폴로지 도메인 간에 파드를 균등하게 스케줄링할 수 있다.
  [파드 토폴로지 분배 제약 조건](/ko/docs/concepts/workloads/pods/pod-topology-spread-constraints/)을 참고한다.
- `ExecProbeTimeout` : kubelet이 exec 프로브 시간 초과를 준수하는지 확인한다.
  이 기능 게이트는 기존 워크로드가 쿠버네티스가 exec 프로브 제한 시간을 무시한
  현재 수정된 결함에 의존하는 경우 존재한다.
  [준비성 프로브](/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/#configure-probes)를 참조한다.
- `ExpandCSIVolumes`: CSI 볼륨 확장을 활성화한다.
- `ExpandInUsePersistentVolumes`: 사용 중인 PVC를 확장할 수 있다.
  [사용 중인 퍼시스턴트볼륨클레임 크기 조정](/ko/docs/concepts/storage/persistent-volumes/#사용-중인-퍼시스턴트볼륨클레임-크기-조정)을 참고한다.
- `ExpandPersistentVolumes`: 퍼시스턴트 볼륨 확장을 활성화한다.
  [퍼시스턴트 볼륨 클레임 확장](/ko/docs/concepts/storage/persistent-volumes/#퍼시스턴트-볼륨-클레임-확장)을 참고한다.
- `ExperimentalCriticalPodAnnotation`: 특정 파드에 *critical* 로
  어노테이션을 달아서 [스케줄링이 보장되도록](/docs/tasks/administer-cluster/guaranteed-scheduling-critical-addon-pods/) 한다.
  이 기능은 v1.13부터 파드 우선 순위 및 선점으로 인해 사용 중단되었다.
- `ExperimentalHostUserNamespaceDefaultingGate`: 사용자 네임스페이스를 호스트로
  기본 활성화한다. 이것은 다른 호스트 네임스페이스, 호스트 마운트,
  권한이 있는 컨테이너 또는 특정 비-네임스페이스(non-namespaced) 기능(예: `MKNODE`, `SYS_MODULE` 등)을
  사용하는 컨테이너를 위한 것이다. 도커 데몬에서 사용자 네임스페이스
  재 매핑이 활성화된 경우에만 활성화해야 한다.
- `ExternalPolicyForExternalIP`: ExternalTrafficPolicy가 서비스(Service) ExternalIP에 적용되지 않는 버그를 수정한다.
- `GCERegionalPersistentDisk`: GCE에서 지역 PD 기능을 활성화한다.
- `GenericEphemeralVolume`: 일반 볼륨의 모든 기능을 지원하는 임시, 인라인
  볼륨을 활성화한다(타사 스토리지 공급 업체, 스토리지 용량 추적, 스냅샷으로부터 복원
  등에서 제공할 수 있음).
  [임시 볼륨](/docs/concepts/storage/ephemeral-volumes/)을 참고한다.
- `GracefulNodeShutdown` : kubelet에서 정상 종료를 지원한다.
  시스템 종료 중에 kubelet은 종료 이벤트를 감지하고 노드에서 실행 중인
  파드를 정상적으로 종료하려고 시도한다. 자세한 내용은
  [Graceful Node Shutdown](/ko/docs/concepts/architecture/nodes/#그레이스풀-graceful-노드-셧다운)을
  참조한다.
- `HPAContainerMetrics`: `HorizontalPodAutoscaler`를 활성화하여 대상 파드의
  개별 컨테이너 메트릭을 기반으로 확장한다.
- `HPAScaleToZero`: 사용자 정의 또는 외부 메트릭을 사용할 때 `HorizontalPodAutoscaler` 리소스에 대해
  `minReplicas` 를 0으로 설정한다.
- `HugePages`: 사전 할당된 [huge page](/ko/docs/tasks/manage-hugepages/scheduling-hugepages/)의
  할당 및 사용을 활성화한다.
- `HugePageStorageMediumSize`: 사전 할당된 [huge page](/ko/docs/tasks/manage-hugepages/scheduling-hugepages/)의
  여러 크기를 지원한다.
- `HyperVContainer`: 윈도우 컨테이너를 위한
  [Hyper-V 격리](https://docs.microsoft.com/ko-kr/virtualization/windowscontainers/manage-containers/hyperv-container)
  기능을 활성화한다.
- `ImmutableEphemeralVolumes`: 안정성과 성능 향상을 위해 개별 시크릿(Secret)과 컨피그맵(ConfigMap)을
  변경할 수 없는(immutable) 것으로 표시할 수 있다.
- `IndexedJob`: [잡](/ko/docs/concepts/workloads/controllers/job/) 컨트롤러가
  완료 횟수를 기반으로 파드 완료를 관리할 수 있도록 한다.
- `IngressClassNamespacedParams`: `IngressClass` 리소스가 네임스페이스 범위로
  한정된 파라미터를 이용할 수 있도록 한다. 이 기능은 `IngressClass.spec.parameters` 에
  `Scope` 와 `Namespace` 2개의 필드를 추가한다.
- `Initializers`: Initializers 어드미션 플러그인을 사용하여 오브젝트 생성의
  비동기 조정을 허용한다.
- `IPv6DualStack`: IPv6을 위한 [이중 스택](/ko/docs/concepts/services-networking/dual-stack/)
  기능을 활성화한다.
- `KubeletConfigFile`: 구성 파일을 사용하여 지정된 파일에서
  kubelet 구성을 로드할 수 있다.
  자세한 내용은 [구성 파일을 통해 kubelet 파라미터 설정](/docs/tasks/administer-cluster/kubelet-config-file/)을
  참고한다.
- `KubeletCredentialProviders`: 이미지 풀 자격 증명에 대해 kubelet exec 자격 증명 공급자를 활성화한다.
- `KubeletPluginsWatcher`: kubelet이 [CSI 볼륨 드라이버](/ko/docs/concepts/storage/volumes/#csi)와 같은
  플러그인을 검색할 수 있도록 프로브 기반 플러그인 감시자(watcher) 유틸리티를 사용한다.
- `KubeletPodResources`: kubelet의 파드 리소스 gPRC 엔드포인트를 활성화한다. 자세한 내용은
  [장치 모니터링 지원](https://github.com/kubernetes/enhancements/blob/master/keps/sig-node/606-compute-device-assignment/README.md)을
  참고한다.
- `KubeletPodResourcesGetAllocatable`: kubelet의 파드 리소스 `GetAllocatableResources` 기능을 활성화한다.
  이 API는 클라이언트가 노드의 여유 컴퓨팅 자원을 잘 파악할 수 있도록, 할당 가능 자원에 대한 정보를
  [자원 할당 보고](/ko/docs/concepts/extend-kubernetes/compute-storage-net/device-plugins/#장치-플러그인-리소스-모니터링)한다.
- `LegacyNodeRoleBehavior`: 비활성화되면, 서비스 로드 밸런서 및 노드 중단의 레거시 동작은
  `NodeDisruptionExclusion` 과 `ServiceNodeExclusion` 에 의해 제공된 기능별 레이블을 대신하여
  `node-role.kubernetes.io/master` 레이블을 무시한다.
- `LocalStorageCapacityIsolation`:
  [로컬 임시 스토리지](/ko/docs/concepts/configuration/manage-resources-containers/)와
  [emptyDir 볼륨](/ko/docs/concepts/storage/volumes/#emptydir)의
  `sizeLimit` 속성을 사용할 수 있게 한다.
- `LocalStorageCapacityIsolationFSQuotaMonitoring`: [로컬 임시 스토리지](/ko/docs/concepts/configuration/manage-resources-containers/)에
  `LocalStorageCapacityIsolation` 이 활성화되고
  [emptyDir 볼륨](/ko/docs/concepts/storage/volumes/#emptydir)의
  백업 파일시스템이 프로젝트 쿼터를 지원하고 활성화된 경우, 파일시스템 사용보다는
  프로젝트 쿼터를 사용하여 [emptyDir 볼륨](/ko/docs/concepts/storage/volumes/#emptydir)
  스토리지 사용을 모니터링하여 성능과 정확성을
  향상시킨다.
- `LogarithmicScaleDown`: 컨트롤러 스케일 다운 시에 파드 타임스탬프를 로그 스케일로 버켓화하여
  축출할 파드를 반-랜덤하게 선택하는 기법을 활성화한다.
- `MixedProtocolLBService`: 동일한 로드밸런서 유형 서비스 인스턴스에서 다른 프로토콜
  사용을 활성화한다.
- `MountContainers`: 호스트의 유틸리티 컨테이너를 볼륨 마운터로 사용할 수 있다.
- `MountPropagation`: 한 컨테이너에서 다른 컨테이너 또는 파드로 마운트된 볼륨을 공유할 수 있다.
  자세한 내용은 [마운트 전파(propagation)](/ko/docs/concepts/storage/volumes/#마운트-전파-propagation)을 참고한다.
- `NamespaceDefaultLabelName`: API 서버로 하여금 모든 네임스페이스에 대해 변경할 수 없는 (immutable)
  {{< glossary_tooltip text="레이블" term_id="label" >}} `kubernetes.io/metadata.name`을 설정하도록 한다. (네임스페이스의 이름도 변경 불가)
- `NetworkPolicyEndPort`: 네트워크폴리시(NetworkPolicy)	오브젝트에서 단일 포트를 지정하는 것 대신에 포트 범위를 지정할 수 있도록, `endPort` 필드의 사용을 활성화한다.
- `NodeDisruptionExclusion`: 영역(zone) 장애 시 노드가 제외되지 않도록 노드 레이블 `node.kubernetes.io/exclude-disruption`
  사용을 활성화한다.
- `NodeLease`: 새로운 리스(Lease) API가 노드 상태 신호로 사용될 수 있는 노드 하트비트(heartbeats)를 보고할 수 있게 한다.
- `NonPreemptingPriority`: 프라이어리티클래스(PriorityClass)와 파드에 `preemptionPolicy` 필드를 활성화한다.
- `PVCProtection`: 파드에서 사용 중일 때 퍼시스턴트볼륨클레임(PVC)이
  삭제되지 않도록 한다.
- `PodDeletionCost`: 레플리카셋 다운스케일 시 삭제될 파드의 우선순위를 사용자가 조절할 수 있도록,
   [파드 삭제 비용](/ko/docs/concepts/workloads/controllers/replicaset/#파드-삭제-비용) 기능을 활성화한다.
- `PersistentLocalVolumes`: 파드에서 `local` 볼륨 유형의 사용을 활성화한다.
  `local` 볼륨을 요청하는 경우 파드 어피니티를 지정해야 한다.
- `PodDisruptionBudget`: [PodDisruptionBudget](/docs/tasks/run-application/configure-pdb/) 기능을 활성화한다.
- `PodAffinityNamespaceSelector`: [파드 어피니티 네임스페이스 셀렉터](/ko/docs/concepts/scheduling-eviction/assign-pod-node/#네임스페이스-셀렉터) 기능과
  [CrossNamespacePodAffinity](/ko/docs/concepts/policy/resource-quotas/#네임스페이스-간-파드-어피니티-쿼터) 쿼터 범위 기능을 활성화한다.
- `PodOverhead`: 파드 오버헤드를 판단하기 위해 [파드오버헤드(PodOverhead)](/ko/docs/concepts/scheduling-eviction/pod-overhead/)
  기능을 활성화한다.
- `PodPriority`: [우선 순위](/ko/docs/concepts/scheduling-eviction/pod-priority-preemption/)를
  기반으로 파드의 스케줄링 취소와 선점을 활성화한다.
- `PodReadinessGates`: 파드 준비성 평가를 확장하기 위해
  `PodReadinessGate` 필드 설정을 활성화한다. 자세한 내용은 [파드의 준비성 게이트](/ko/docs/concepts/workloads/pods/pod-lifecycle/#pod-readiness-gate)를
  참고한다.
- `PodShareProcessNamespace`: 파드에서 실행되는 컨테이너 간에 단일 프로세스 네임스페이스를
  공유하기 위해 파드에서 `shareProcessNamespace` 설정을 활성화한다. 자세한 내용은
  [파드의 컨테이너 간 프로세스 네임스페이스 공유](/docs/tasks/configure-pod-container/share-process-namespace/)에서 확인할 수 있다.
- `ProbeTerminationGracePeriod`: 파드의 [프로브-수준
  `terminationGracePeriodSeconds` 설정하기](/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/#probe-level-terminationgraceperiodseconds) 기능을 활성화한다.
  더 자세한 사항은 [기능개선 제안](https://github.com/kubernetes/enhancements/tree/master/keps/sig-node/2238-liveness-probe-grace-period)을 참고한다.
- `ProcMountType`: SecurityContext의 `procMount` 필드를 설정하여
  컨테이너의 proc 타입의 마운트를 제어할 수 있다.
- `QOSReserved`: QoS 수준에서 리소스 예약을 허용하여 낮은 QoS 수준의 파드가
  더 높은 QoS 수준에서 요청된 리소스로 파열되는 것을 방지한다
  (현재 메모리만 해당).
- `RemainingItemCount`: API 서버가
  [청크(chunking) 목록 요청](/docs/reference/using-api/api-concepts/#retrieving-large-results-sets-in-chunks)에 대한
  응답에서 남은 항목 수를 표시하도록 허용한다.
- `RemoveSelfLink`: ObjectMeta 및 ListMeta에서 `selfLink` 를 사용하지 않고
  제거한다.
- `RequestManagement`: 각 API 서버에서 우선 순위 및 공정성으로 요청 동시성을
  관리할 수 있다. 1.17 이후 `APIPriorityAndFairness` 에서 사용 중단되었다.
- `ResourceLimitsPriorityFunction`: 입력 파드의 CPU 및 메모리 한도 중
  하나 이상을 만족하는 노드에 가능한 최저 점수 1을 할당하는
  스케줄러 우선 순위 기능을 활성화한다. 의도는 동일한 점수를 가진
  노드 사이의 관계를 끊는 것이다.
- `ResourceQuotaScopeSelectors`: 리소스 쿼터 범위 셀렉터를 활성화한다.
- `RootCAConfigMap`: 모든 네임스페이스에 `kube-root-ca.crt`라는
  {{< glossary_tooltip text="컨피그맵" term_id="configmap" >}}을 게시하도록
  `kube-controller-manager` 를 구성한다. 이 컨피그맵에는 kube-apiserver에 대한 연결을 확인하는 데
  사용되는 CA 번들이 포함되어 있다. 자세한 내용은
  [바운드 서비스 계정 토큰](https://github.com/kubernetes/enhancements/blob/master/keps/sig-auth/1205-bound-service-account-tokens/README.md)을
  참조한다.
- `RotateKubeletClientCertificate`: kubelet에서 클라이언트 TLS 인증서의 로테이션을 활성화한다.
  자세한 내용은 [kubelet 구성](/docs/reference/command-line-tools-reference/kubelet-tls-bootstrapping/#kubelet-configuration)을 참고한다.
- `RotateKubeletServerCertificate`: kubelet에서 서버 TLS 인증서의 로테이션을 활성화한다.
- `RunAsGroup`: 컨테이너의 init 프로세스에 설정된 기본 그룹 ID 제어를
  활성화한다.
- `RuntimeClass`: 컨테이너 런타임 구성을 선택하기 위해 [런타임클래스(RuntimeClass)](/ko/docs/concepts/containers/runtime-class/)
  기능을 활성화한다.
- `ScheduleDaemonSetPods`: 데몬셋(DaemonSet) 컨트롤러 대신 기본 스케줄러로 데몬셋 파드를
  스케줄링할 수 있다.
- `SCTPSupport`: 파드, 서비스, 엔드포인트, 엔드포인트슬라이스 및 네트워크폴리시 정의에서
  _SCTP_ `protocol` 값을 활성화한다.
- `ServerSideApply`: API 서버에서 [SSA(Sever Side Apply)](/docs/reference/using-api/server-side-apply/)
  경로를 활성화한다.
- `ServiceAccountIssuerDiscovery`: API 서버에서 서비스 어카운트 발행자에 대해 OIDC 디스커버리 엔드포인트(발급자 및
  JWKS URL)를 활성화한다. 자세한 내용은
  [파드의 서비스 어카운트 구성](/docs/tasks/configure-pod-container/configure-service-account/#service-account-issuer-discovery)을
  참고한다.
- `ServiceAppProtocol`: 서비스와 엔드포인트에서 `appProtocol` 필드를 활성화한다.
- `ServiceInternalTrafficPolicy`: 서비스에서 `internalTrafficPolicy` 필드를 활성화한다.
- `ServiceLBNodePortControl`: 서비스에서 `allocateLoadBalancerNodePorts` 필드를 활성화한다.
- `ServiceLoadBalancerClass`: 서비스에서 `loadBalancerClass` 필드를 활성화한다. 자세한 내용은
  [로드밸런서 구현체의 종류 확인하기](/ko/docs/concepts/services-networking/service/#load-balancer-class)를 참고한다.
- `ServiceLoadBalancerFinalizer`: 서비스 로드 밸런서에 대한 Finalizer 보호를 활성화한다.
- `ServiceNodeExclusion`: 클라우드 제공자가 생성한 로드 밸런서에서 노드를
  제외할 수 있다. "`node.kubernetes.io/exclude-from-external-load-balancers`"로
  레이블이 지정된 경우 노드를 제외할 수 있다.
- `ServiceTopology`: 서비스가 클러스터의 노드 토폴로지를 기반으로 트래픽을 라우팅할 수
  있도록 한다. 자세한 내용은
  [서비스토폴로지(ServiceTopology)](/ko/docs/concepts/services-networking/service-topology/)를
  참고한다.
- `SetHostnameAsFQDN`: 전체 주소 도메인 이름(FQDN)을 파드의 호스트 이름으로
  설정하는 기능을 활성화한다.
  [파드의 `setHostnameAsFQDN` 필드](/ko/docs/concepts/services-networking/dns-pod-service/#pod-sethostnameasfqdn-field)를 참고한다.
- `StartupProbe`: kubelet에서
  [스타트업](/ko/docs/concepts/workloads/pods/pod-lifecycle/#언제-스타트업-프로브를-사용해야-하는가)
  프로브를 활성화한다.
- `StorageObjectInUseProtection`: 퍼시스턴트볼륨 또는 퍼시스턴트볼륨클레임 오브젝트가 여전히
  사용 중인 경우 삭제를 연기한다.
- `StorageVersionAPI`: [스토리지 버전 API](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#storageversion-v1alpha1-internal-apiserver-k8s-io)를
  활성화한다.
- `StorageVersionHash`: API 서버가 디스커버리에서 스토리지 버전 해시를 노출하도록
  허용한다.
- `StreamingProxyRedirects`: 스트리밍 요청을 위해 백엔드(kubelet)에서 리디렉션을
  가로채서 따르도록 API 서버에 지시한다.
  스트리밍 요청의 예로는 `exec`, `attach` 및 `port-forward` 요청이 있다.
- `SupportIPVSProxyMode`: IPVS를 사용하여 클러스터 내 서비스 로드 밸런싱을 제공한다.
  자세한 내용은 [서비스 프록시](/ko/docs/concepts/services-networking/service/#가상-ip와-서비스-프록시)를 참고한다.
- `SupportNodePidsLimit`: 노드에서 PID 제한 지원을 활성화한다.
  `--system-reserved` 및 `--kube-reserved` 옵션의 `pid=<number>`
  파라미터를 지정하여 지정된 수의 프로세스 ID가
  시스템 전체와 각각 쿠버네티스 시스템 데몬에 대해 예약되도록
  할 수 있다.
- `SupportPodPidsLimit`: 파드의 PID 제한에 대한 지원을 활성화한다.
- `SuspendJob`: 잡 중지/재시작 기능을 활성화한다.
  자세한 내용은 [잡 문서](/ko/docs/concepts/workloads/controllers/job/)를
  참고한다.
- `Sysctls`: 각 파드에 설정할 수 있는 네임스페이스 커널
  파라미터(sysctl)를 지원한다. 자세한 내용은
  [sysctl](/docs/tasks/administer-cluster/sysctl-cluster/)을 참고한다.
- `TTLAfterFinished`: [TTL 컨트롤러](/ko/docs/concepts/workloads/controllers/ttlafterfinished/)가
  실행이 끝난 후 리소스를 정리하도록
  허용한다.
- `TaintBasedEvictions`: 노드의 테인트(taint) 및 파드의 톨러레이션(toleration)을 기반으로
  노드에서 파드를 축출할 수 있다.
  자세한 내용은 [테인트와 톨러레이션](/ko/docs/concepts/scheduling-eviction/taint-and-toleration/)을
  참고한다.
- `TaintNodesByCondition`: [노드 컨디션](/ko/docs/concepts/architecture/nodes/#condition)을
  기반으로 자동 테인트 노드를 활성화한다.
- `TokenRequest`: 서비스 어카운트 리소스에서 `TokenRequest` 엔드포인트를 활성화한다.
- `TokenRequestProjection`: [`projected` 볼륨](/ko/docs/concepts/storage/volumes/#projected)을 통해
  서비스 어카운트 토큰을 파드에 주입할 수 있다.
- `TopologyAwareHints`: 엔드포인트슬라이스(EndpointSlices)에서 토폴로지 힌트 기반
  토폴로지-어웨어 라우팅을 활성화한다. 자세한 내용은
  [토폴로지 어웨어 힌트](/docs/concepts/services-networking/topology-aware-hints/)
  를 참고한다.
- `TopologyManager`: 쿠버네티스의 다른 컴포넌트에 대한 세분화된 하드웨어 리소스
  할당을 조정하는 메커니즘을 활성화한다.
  [노드의 토폴로지 관리 정책 제어](/docs/tasks/administer-cluster/topology-manager/)를 참고한다.
- `ValidateProxyRedirects`: 이 플래그는 API 서버가 동일한 호스트로만 리디렉션되는가를
  확인해야 하는지 여부를 제어한다. `StreamingProxyRedirects`
  플래그가 활성화된 경우에만 사용된다.
- `VolumeCapacityPriority`: 가용 PV 용량을 기반으로
  여러 토폴로지에 있는 노드들의 우선순위를 정하는 기능을 활성화한다.
- `VolumePVCDataSource`: 기존 PVC를 데이터 소스로 지정하는 기능을 지원한다.
- `VolumeScheduling`: 볼륨 토폴로지 인식 스케줄링을 활성화하고
  퍼시스턴트볼륨클레임(PVC) 바인딩이 스케줄링 결정을 인식하도록 한다. 또한
  `PersistentLocalVolumes` 기능 게이트와 함께 사용될 때
  [`local`](/ko/docs/concepts/storage/volumes/#local) 볼륨 유형을 사용할 수 있다.
- `VolumeSnapshotDataSource`: 볼륨 스냅샷 데이터 소스 지원을 활성화한다.
- `VolumeSubpath`: 컨테이너에 볼륨의 하위 경로(subpath)를 마운트할 수 있다.
- `VolumeSubpathEnvExpansion`: 환경 변수를 `subPath`로 확장하기 위해
  `subPathExpr` 필드를 활성화한다.
- `WarningHeaders`: API 응답에서 경고 헤더를 보낼 수 있다.
- `WatchBookmark`: 감시자 북마크(watch bookmark) 이벤트 지원을 활성화한다.
- `WinDSR`: kube-proxy가 윈도우용 DSR 로드 밸런서를 생성할 수 있다.
- `WinOverlay`: kube-proxy가 윈도우용 오버레이 모드에서 실행될 수 있도록 한다.
- `WindowsGMSA`: 파드에서 컨테이너 런타임으로 GMSA 자격 증명 스펙을 전달할 수 있다.
- `WindowsRunAsUserName` : 기본 사용자가 아닌(non-default) 사용자로 윈도우 컨테이너에서
  애플리케이션을 실행할 수 있도록 지원한다. 자세한 내용은
  [RunAsUserName 구성](/ko/docs/tasks/configure-pod-container/configure-runasusername/)을
  참고한다.
- `WindowsEndpointSliceProxying`: 활성화되면, 윈도우에서 실행되는 kube-proxy는
  엔드포인트 대신 엔드포인트슬라이스를 기본 데이터 소스로 사용하여
  확장성과 성능을 향상시킨다.
  [엔드포인트슬라이스 활성화하기](/ko/docs/concepts/services-networking/endpoint-slices/)를 참고한다.


## {{% heading "whatsnext" %}}

* [사용 중단 정책](/docs/reference/using-api/deprecation-policy/)은 쿠버네티스에 대한
  기능과 컴포넌트를 제거하는 프로젝트의 접근 방법을 설명한다.
