---
title: フィーチャーゲート
weight: 10
content_type: concept
---

<!-- overview -->
このページでは管理者がそれぞれのKubernetesコンポーネントで指定できるさまざまなフィーチャーゲートの概要について説明しています。

各機能におけるステージの説明については、[機能のステージ](#feature-stages)を参照してください。


<!-- body -->
## 概要

フィーチャーゲートはアルファ機能または実験的機能を記述するkey=valueのペアのセットです。管理者は各コンポーネントで`--feature-gates`コマンドラインフラグを使用することで機能をオンまたはオフにできます。

各コンポーネントはそれぞれのコンポーネント固有のフィーチャーゲートの設定をサポートします。すべてのコンポーネントのフィーチャーゲートの全リストを表示するには`-h`フラグを使用します。kubeletなどのコンポーネントにフィーチャーゲートを設定するには以下のようにリストの機能ペアを`--feature-gates`フラグを使用して割り当てます。

```shell
--feature-gates="...,DynamicKubeletConfig=true"
```

次の表は各Kubernetesコンポーネントに設定できるフィーチャーゲートの概要です。

- 「導入開始バージョン」列は機能が導入されたとき、またはリリース段階が変更されたときのKubernetesリリースバージョンとなります。
- 「最終利用可能バージョン」列は空ではない場合はフィーチャーゲートを使用できる最後のKubernetesリリースバージョンとなります。
- アルファまたはベータ状態の機能は[AlphaまたはBetaのフィーチャーゲート](#feature-gates-for-alpha-or-beta-features)に載っています。
- 安定している機能は、[graduatedまたはdeprecatedのフィーチャーゲート](#feature-gates-for-graduated-or-deprecated-features)に載っています。
- graduatedまたはdeprecatedのフィーチャーゲートには、非推奨および廃止された機能もリストされています。

### AlphaまたはBetaのフィーチャーゲート {#feature-gates-for-alpha-or-beta-features}

{{< table caption="AlphaまたはBetaのフィーチャーゲート" >}}

| 機能名 | デフォルト値 | ステージ | 導入開始バージョン | 最終利用可能バージョン |
|---------|---------|-------|-------|-------|
| `AnyVolumeDataSource` | `false` | Alpha | 1.18 | |
| `APIListChunking` | `false` | Alpha | 1.8 | 1.8 |
| `APIListChunking` | `true` | Beta | 1.9 | |
| `APIPriorityAndFairness` | `false` | Alpha | 1.17 | |
| `APIResponseCompression` | `false` | Alpha | 1.7 | |
| `AppArmor` | `true` | Beta | 1.4 | |
| `BalanceAttachedNodeVolumes` | `false` | Alpha | 1.11 | |
| `BoundServiceAccountTokenVolume` | `false` | Alpha | 1.13 | |
| `CPUManager` | `false` | Alpha | 1.8 | 1.9 |
| `CPUManager` | `true` | Beta | 1.10 | |
| `CRIContainerLogRotation` | `false` | Alpha | 1.10 | 1.10 |
| `CRIContainerLogRotation` | `true` | Beta| 1.11 | |
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
| `CSIMigrationAzureFile` | `false` | Alpha | 1.15 | |
| `CSIMigrationAzureFileComplete` | `false` | Alpha | 1.17 | |
| `CSIMigrationGCE` | `false` | Alpha | 1.14 | 1.16 |
| `CSIMigrationGCE` | `false` | Beta | 1.17 | |
| `CSIMigrationGCEComplete` | `false` | Alpha | 1.17 | |
| `CSIMigrationOpenStack` | `false` | Alpha | 1.14 | |
| `CSIMigrationOpenStackComplete` | `false` | Alpha | 1.17 | |
| `CSIMigrationvSphere` | `false` | Beta | 1.19 | |
| `CSIMigrationvSphereComplete` | `false` | Beta | 1.19 | |
| `CSIStorageCapacity` | `false` | Alpha | 1.19 | |
| `CSIVolumeFSGroupPolicy` | `false` | Alpha | 1.19 | |
| `ConfigurableFSGroupPolicy` | `false` | Alpha | 1.18 | |
| `CustomCPUCFSQuotaPeriod` | `false` | Alpha | 1.12 | |
| `DefaultPodTopologySpread` | `false` | Alpha | 1.19 | |
| `DevicePlugins` | `false` | Alpha | 1.8 | 1.9 |
| `DevicePlugins` | `true` | Beta | 1.10 | |
| `DisableAcceleratorUsageMetrics` | `false` | Alpha | 1.19 | 1.20 |
| `DryRun` | `false` | Alpha | 1.12 | 1.12 |
| `DryRun` | `true` | Beta | 1.13 | |
| `DynamicKubeletConfig` | `false` | Alpha | 1.4 | 1.10 |
| `DynamicKubeletConfig` | `true` | Beta | 1.11 | |
| `EndpointSlice` | `false` | Alpha | 1.16 | 1.16 |
| `EndpointSlice` | `false` | Beta | 1.17 | |
| `EndpointSlice` | `true` | Beta | 1.18 | |
| `EndpointSliceProxying` | `false` | Alpha | 1.18 | 1.18 |
| `EndpointSliceProxying` | `true` | Beta | 1.19 | |
| `EphemeralContainers` | `false` | Alpha | 1.16 | |
| `ExpandCSIVolumes` | `false` | Alpha | 1.14 | 1.15 |
| `ExpandCSIVolumes` | `true` | Beta | 1.16 | |
| `ExpandInUsePersistentVolumes` | `false` | Alpha | 1.11 | 1.14 |
| `ExpandInUsePersistentVolumes` | `true` | Beta | 1.15 | |
| `ExpandPersistentVolumes` | `false` | Alpha | 1.8 | 1.10 |
| `ExpandPersistentVolumes` | `true` | Beta | 1.11 | |
| `ExperimentalHostUserNamespaceDefaulting` | `false` | Beta | 1.5 | |
| `GenericEphemeralVolume` | `false` | Alpha | 1.19 | |
| `HPAScaleToZero` | `false` | Alpha | 1.16 | |
| `HugePageStorageMediumSize` | `false` | Alpha | 1.18 | 1.18 |
| `HugePageStorageMediumSize` | `true` | Beta | 1.19 | |
| `HyperVContainer` | `false` | Alpha | 1.10 | |
| `ImmutableEphemeralVolumes` | `false` | Alpha | 1.18 | 1.18 |
| `ImmutableEphemeralVolumes` | `true` | Beta | 1.19 | |
| `IPv6DualStack` | `false` | Alpha | 1.16 | |
| `KubeletPodResources` | `false` | Alpha | 1.13 | 1.14 |
| `KubeletPodResources` | `true` | Beta | 1.15 | |
| `LegacyNodeRoleBehavior` | `true` | Alpha | 1.16 | |
| `LocalStorageCapacityIsolation` | `false` | Alpha | 1.7 | 1.9 |
| `LocalStorageCapacityIsolation` | `true` | Beta | 1.10 | |
| `LocalStorageCapacityIsolationFSQuotaMonitoring` | `false` | Alpha | 1.15 | |
| `MountContainers` | `false` | Alpha | 1.9 | |
| `NodeDisruptionExclusion` | `false` | Alpha | 1.16 | 1.18 |
| `NodeDisruptionExclusion` | `true` | Beta | 1.19 | |
| `NonPreemptingPriority` | `false` | Alpha | 1.15 | 1.18 |
| `NonPreemptingPriority` | `true` | Beta | 1.19 | |
| `PodDisruptionBudget` | `false` | Alpha | 1.3 | 1.4 |
| `PodDisruptionBudget` | `true` | Beta | 1.5 | |
| `PodOverhead` | `false` | Alpha | 1.16 | - |
| `ProcMountType` | `false` | Alpha | 1.12 | |
| `QOSReserved` | `false` | Alpha | 1.11 | |
| `RemainingItemCount` | `false` | Alpha | 1.15 | |
| `RotateKubeletServerCertificate` | `false` | Alpha | 1.7 | 1.11 |
| `RotateKubeletServerCertificate` | `true` | Beta | 1.12 | |
| `RunAsGroup` | `true` | Beta | 1.14 | |
| `RuntimeClass` | `false` | Alpha | 1.12 | 1.13 |
| `RuntimeClass` | `true` | Beta | 1.14 | |
| `SCTPSupport` | `false` | Alpha | 1.12 | 1.18 |
| `SCTPSupport` | `true` | Beta | 1.19 | |
| `ServerSideApply` | `false` | Alpha | 1.14 | 1.15 |
| `ServerSideApply` | `true` | Beta | 1.16 | |
| `ServiceAccountIssuerDiscovery` | `false` | Alpha | 1.18 | |
| `ServiceAppProtocol` | `false` | Alpha | 1.18 | 1.18 |
| `ServiceAppProtocol` | `true` | Beta | 1.19 | |
| `ServiceNodeExclusion` | `false` | Alpha | 1.8 | 1.18 |
| `ServiceNodeExclusion` | `true` | Beta | 1.19 | |
| `ServiceTopology` | `false` | Alpha | 1.17 | |
| `SetHostnameAsFQDN` | `false` | Alpha | 1.19 | |
| `StartupProbe` | `false` | Alpha | 1.16 | 1.17 |
| `StartupProbe` | `true` | Beta | 1.18 | |
| `StorageVersionHash` | `false` | Alpha | 1.14 | 1.14 |
| `StorageVersionHash` | `true` | Beta | 1.15 | |
| `SupportNodePidsLimit` | `false` | Alpha | 1.14 | 1.14 |
| `SupportNodePidsLimit` | `true` | Beta | 1.15 | |
| `SupportPodPidsLimit` | `false` | Alpha | 1.10 | 1.13 |
| `SupportPodPidsLimit` | `true` | Beta | 1.14 | |
| `Sysctls` | `true` | Beta | 1.11 | |
| `TokenRequest` | `false` | Alpha | 1.10 | 1.11 |
| `TokenRequest` | `true` | Beta | 1.12 | |
| `TokenRequestProjection` | `false` | Alpha | 1.11 | 1.11 |
| `TokenRequestProjection` | `true` | Beta | 1.12 | |
| `TTLAfterFinished` | `false` | Alpha | 1.12 | |
| `TopologyManager` | `false` | Alpha | 1.16 | 1.17 |
| `TopologyManager` | `true` | Beta | 1.18 | |
| `ValidateProxyRedirects` | `false` | Alpha | 1.12 | 1.13 |
| `ValidateProxyRedirects` | `true` | Beta | 1.14 | |
| `VolumeSnapshotDataSource` | `false` | Alpha | 1.12 | 1.16 |
| `VolumeSnapshotDataSource` | `true` | Beta | 1.17 | - |
| `WindowsEndpointSliceProxying` | `false` | Alpha | 1.19 | |
| `WindowsGMSA` | `false` | Alpha | 1.14 | |
| `WindowsGMSA` | `true` | Beta | 1.16 | |
| `WinDSR` | `false` | Alpha | 1.14 | |
| `WinOverlay` | `false` | Alpha | 1.14 | |
{{< /table >}}

### GraduatedまたはDeprecatedのフィーチャーゲート {#feature-gates-for-graduated-or-deprecated-features}

{{< table caption="GraduatedまたはDeprecatedのフィーチャーゲート" >}}

| 機能名 | デフォルト値 | ステージ | 導入開始バージョン | 最終利用可能バージョン |
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
| `BlockVolume` | `false` | Alpha | 1.9 | 1.12 |
| `BlockVolume` | `true` | Beta | 1.13 | 1.17 |
| `BlockVolume` | `true` | GA | 1.18 | - |
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
| `DynamicAuditing` | `false` | Alpha | 1.13 | 1.18 |
| `DynamicAuditing` | - | Deprecated | 1.19 | - |
| `DynamicProvisioningScheduling` | `false` | Alpha | 1.11 | 1.11 |
| `DynamicProvisioningScheduling` | - | Deprecated| 1.12 | - |
| `DynamicVolumeProvisioning` | `true` | Alpha | 1.3 | 1.7 |
| `DynamicVolumeProvisioning` | `true` | GA | 1.8 | - |
| `EnableEquivalenceClassCache` | `false` | Alpha | 1.8 | 1.14 |
| `EnableEquivalenceClassCache` | - | Deprecated | 1.15 | - |
| `ExperimentalCriticalPodAnnotation` | `false` | Alpha | 1.5 | 1.12 |
| `ExperimentalCriticalPodAnnotation` | `false` | Deprecated | 1.13 | - |
| `EvenPodsSpread` | `false` | Alpha | 1.16 | 1.17 |
| `EvenPodsSpread` | `true` | Beta | 1.18 | 1.18 |
| `EvenPodsSpread` | `true` | GA | 1.19 | - |
| `GCERegionalPersistentDisk` | `true` | Beta | 1.10 | 1.12 |
| `GCERegionalPersistentDisk` | `true` | GA | 1.13 | - |
| `HugePages` | `false` | Alpha | 1.8 | 1.9 |
| `HugePages` | `true` | Beta| 1.10 | 1.13 |
| `HugePages` | `true` | GA | 1.14 | - |
| `Initializers` | `false` | Alpha | 1.7 | 1.13 |
| `Initializers` | - | Deprecated | 1.14 | - |
| `KubeletConfigFile` | `false` | Alpha | 1.8 | 1.9 |
| `KubeletConfigFile` | - | Deprecated | 1.10 | - |
| `KubeletPluginsWatcher` | `false` | Alpha | 1.11 | 1.11 |
| `KubeletPluginsWatcher` | `true` | Beta | 1.12 | 1.12 |
| `KubeletPluginsWatcher` | `true` | GA | 1.13 | - |
| `MountPropagation` | `false` | Alpha | 1.8 | 1.9 |
| `MountPropagation` | `true` | Beta | 1.10 | 1.11 |
| `MountPropagation` | `true` | GA | 1.12 | - |
| `NodeLease` | `false` | Alpha | 1.12 | 1.13 |
| `NodeLease` | `true` | Beta | 1.14 | 1.16 |
| `NodeLease` | `true` | GA | 1.17 | - |
| `PersistentLocalVolumes` | `false` | Alpha | 1.7 | 1.9 |
| `PersistentLocalVolumes` | `true` | Beta | 1.10 | 1.13 |
| `PersistentLocalVolumes` | `true` | GA | 1.14 | - |
| `PodPriority` | `false` | Alpha | 1.8 | 1.10 |
| `PodPriority` | `true` | Beta | 1.11 | 1.13 |
| `PodPriority` | `true` | GA | 1.14 | - |
| `PodReadinessGates` | `false` | Alpha | 1.11 | 1.11 |
| `PodReadinessGates` | `true` | Beta | 1.12 | 1.13 |
| `PodReadinessGates` | `true` | GA | 1.14 | - |
| `PodShareProcessNamespace` | `false` | Alpha | 1.10 | 1.11 |
| `PodShareProcessNamespace` | `true` | Beta | 1.12 | 1.16 |
| `PodShareProcessNamespace` | `true` | GA | 1.17 | - |
| `PVCProtection` | `false` | Alpha | 1.9 | 1.9 |
| `PVCProtection` | - | Deprecated | 1.10 | - |
| `RequestManagement` | `false` | Alpha | 1.15 | 1.16 |
| `ResourceLimitsPriorityFunction` | `false` | Alpha | 1.9 | 1.18 |
| `ResourceLimitsPriorityFunction` | - | Deprecated | 1.19 | - |
| `ResourceQuotaScopeSelectors` | `false` | Alpha | 1.11 | 1.11 |
| `ResourceQuotaScopeSelectors` | `true` | Beta | 1.12 | 1.16 |
| `ResourceQuotaScopeSelectors` | `true` | GA | 1.17 | - |
| `RotateKubeletClientCertificate` | `true` | Beta | 1.8 | 1.18 |
| `RotateKubeletClientCertificate` | `true` | GA | 1.19 | - |
| `ScheduleDaemonSetPods` | `false` | Alpha | 1.11 | 1.11 |
| `ScheduleDaemonSetPods` | `true` | Beta | 1.12 | 1.16  |
| `ScheduleDaemonSetPods` | `true` | GA | 1.17 | - |
| `ServiceLoadBalancerFinalizer` | `false` | Alpha | 1.15 | 1.15 |
| `ServiceLoadBalancerFinalizer` | `true` | Beta | 1.16 | 1.16 |
| `ServiceLoadBalancerFinalizer` | `true` | GA | 1.17 | - |
| `StorageObjectInUseProtection` | `true` | Beta | 1.10 | 1.10 |
| `StorageObjectInUseProtection` | `true` | GA | 1.11 | - |
| `StreamingProxyRedirects` | `false` | Beta | 1.5 | 1.5 |
| `StreamingProxyRedirects` | `true` | Beta | 1.6 | 1.18 |
| `StreamingProxyRedirects` | - | Deprecated| 1.19 | - |
| `SupportIPVSProxyMode` | `false` | Alpha | 1.8 | 1.8 |
| `SupportIPVSProxyMode` | `false` | Beta | 1.9 | 1.9 |
| `SupportIPVSProxyMode` | `true` | Beta | 1.10 | 1.10 |
| `SupportIPVSProxyMode` | `true` | GA | 1.11 | - |
| `TaintBasedEvictions` | `false` | Alpha | 1.6 | 1.12 |
| `TaintBasedEvictions` | `true` | Beta | 1.13 | 1.17 |
| `TaintBasedEvictions` | `true` | GA | 1.18 | - |
| `TaintNodesByCondition` | `false` | Alpha | 1.8 | 1.11 |
| `TaintNodesByCondition` | `true` | Beta | 1.12 | 1.16 |
| `TaintNodesByCondition` | `true` | GA | 1.17 | - |
| `VolumePVCDataSource` | `false` | Alpha | 1.15 | 1.15 |
| `VolumePVCDataSource` | `true` | Beta | 1.16 | 1.17 |
| `VolumePVCDataSource` | `true` | GA | 1.18 | - |
| `VolumeScheduling` | `false` | Alpha | 1.9 | 1.9 |
| `VolumeScheduling` | `true` | Beta | 1.10 | 1.12 |
| `VolumeScheduling` | `true` | GA | 1.13 | - |
| `VolumeSubpath` | `true` | GA | 1.13 | - |
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

## 機能を使用する

### 機能のステージ {#feature-stages}

機能には*Alpha* 、*Beta* 、*GA* の段階があります。*Alpha* 機能とは：

* デフォルトでは無効になっています。
* バグがあるかもしれません。機能を有効にするとバグが発生する可能性があります。
* 機能のサポートは予告無しにいつでも削除される場合があります。
* APIは今後のソフトウェアリリースで予告なく互換性の無い変更が行われる場合があります。
* バグが発生するリスクが高く長期的なサポートはないため、短期間のテストクラスターでのみ使用することをお勧めします。

*Beta* 機能とは：

* デフォルトで有効になっています。
* この機能は十分にテストされていて、有効にすることは安全と考えられます。
* 詳細は変更される可能性がありますが、機能全体のサポートは削除されません。
* オブジェクトのスキーマやセマンティックは、その後のベータ版または安定版リリースで互換性の無い変更が行われる場合があります。互換性の無い変更が行われた場合には次のバージョンへの移行手順を提供します。これにはAPIオブジェクトの削除、編集、および再作成が必要になる場合があります。バージョンアップにはいくつかの対応が必要な場合があります。これには機能に依存するアプリケーションのダウンタイムが発生する場合があります。
* 今後のリリースで互換性の無い変更が行われる可能性があるため、ビジネスクリティカルでない使用のみが推奨されます。個別にアップグレードできる複数のクラスターがある場合はこの制限を緩和できる場合があります。

{{< note >}}
*ベータ版* の機能を試してフィードバックをお寄せください！
GAになってからさらなる変更を加えることは現実的ではない場合があります。
{{< /note >}}

*GA* 機能とは(*GA* 機能は*安定版* 機能とも呼ばれます):

* 機能は常に有効となり、無効にすることはできません。
* フィーチャーゲートの設定は不要になります。
* 機能の安定版は後続バージョンでリリースされたソフトウェアで使用されます。

### フィーチャーゲート

各フィーチャーゲートは特定の機能を有効/無効にするように設計されています。

- `Accelerators`: DockerでのNvidia GPUのサポートを有効にします。
- `AdvancedAuditing`: [高度な監査機能](/docs/tasks/debug-application-cluster/audit/#advanced-audit)を有効にします。
- `AffinityInAnnotations`(*非推奨*): [Podのアフィニティまたはアンチアフィニティ](/ja/docs/concepts/scheduling-eviction/assign-pod-node/#affinity-and-anti-affinity)を有効にします。
- `AnyVolumeDataSource`: {{< glossary_tooltip text="PVC" term_id="persistent-volume-claim" >}}の`DataSource`としてカスタムリソースの使用を有効にします。
- `AllowExtTrafficLocalEndpoints`: サービスが外部へのリクエストをノードのローカルエンドポイントにルーティングできるようにします。
- `APIListChunking`: APIクライアントがAPIサーバーからチャンク単位で（`LIST`や`GET`の）リソースを取得できるようにします。
- `APIPriorityAndFairness`: 各サーバーで優先順位付けと公平性を備えた要求の並行性を管理できるようにします(`RequestManagement`から名前が変更されました)。
- `APIResponseCompression`:`LIST`や`GET`リクエストのAPIレスポンスを圧縮します。
- `AppArmor`: Dockerを使用する場合にLinuxノードでAppArmorによる強制アクセスコントロールを有効にします。詳細は[AppArmorチュートリアル](/ja/docs/tutorials/clusters/apparmor/)で確認できます。
- `AttachVolumeLimit`: ボリュームプラグインを有効にすることでノードにアタッチできるボリューム数の制限を設定できます。詳細は[dynamic volume limits](/docs/concepts/storage/storage-limits/#dynamic-volume-limits)で確認できます。
- `BalanceAttachedNodeVolumes`: スケジューリング中にバランスのとれたリソース割り当てを考慮するノードのボリュームカウントを含めます。判断を行う際に、CPU、メモリー使用率、およびボリュームカウントが近いノードがスケジューラーによって優先されます。
- `BlockVolume`: PodでRawブロックデバイスの定義と使用を有効にします。詳細は[Rawブロックボリュームのサポート](/ja/docs/concepts/storage/persistent-volumes/#raw-block-volume-support)で確認できます。
- `BoundServiceAccountTokenVolume`: ServiceAccountTokenVolumeProjectionによって構成される計画ボリュームを使用するにはServiceAccountボリュームを移行します。クラスター管理者は、メトリクス`serviceaccount_stale_tokens_total`を使用して、拡張トークンに依存するワークロードを監視できます。そのようなワークロードがない場合は、フラグ`--service-account-extend-token-expiration=false`を指定し`kube-apiserver`を起動することで、拡張トークンをオフにします。詳細は[Service Account Token Volumes](https://github.com/kubernetes/enhancements/blob/master/keps/sig-auth/1205-bound-service-account-tokens/README.md)で確認できます。
- `ConfigurableFSGroupPolicy`: Podにボリュームをマウントするときに、ユーザーがfsGroupsのボリューム権限変更ポリシーを設定できるようにします。詳細については、[Podのボリューム権限と所有権変更ポリシーの設定](/docs/tasks/configure-pod-container/security-context/#configure-volume-permission-and-ownership-change-policy-for-pods)をご覧ください。
- `CPUManager`: コンテナレベルのCPUアフィニティサポートを有効します。[CPUマネジメントポリシー](/docs/tasks/administer-cluster/cpu-management-policies/)を見てください。
- `CRIContainerLogRotation`: criコンテナランタイムのコンテナログローテーションを有効にします。
- `CSIBlockVolume`: 外部CSIボリュームドライバーを有効にしてブロックストレージをサポートします。詳細は[`csi`Rawブロックボリュームのサポート](/docs/concepts/storage/volumes/#csi-raw-block-volume-support)で確認できます。
- `CSIDriverRegistry`: csi.storage.k8s.ioのCSIDriver APIオブジェクトに関連するすべてのロジックを有効にします。
- `CSIInlineVolume`: PodのCSIインラインボリュームサポートを有効にします。
- `CSIMigration`: シムと変換ロジックを有効にしてボリューム操作をKubernetesリポジトリー内のプラグインから対応した事前インストール済みのCSIプラグインにルーティングします。
- `CSIMigrationAWS`: シムと変換ロジックを有効にしてボリューム操作をKubernetesリポジトリー内のAWS-EBSプラグインからEBS CSIプラグインにルーティングします。ノードにEBS CSIプラグインがインストールおよび設定されていない場合、ツリー内のEBSプラグインへのフォールバックをサポートします。CSIMigration機能フラグを有効にする必要があります。
- `CSIMigrationAWSComplete`: EBSツリー内プラグインのkubeletおよびボリュームコントローラーへの登録を停止し、シムと変換ロジックを有効にして、AWS-EBSツリー内プラグインからEBS CSIプラグインにボリューム操作をルーティングします。CSIMigrationおよびCSIMigrationAWS機能フラグを有効にし、クラスター内のすべてのノードにEBS CSIプラグインをインストールおよび設定する必要があります。
- `CSIMigrationAzureDisk`: シムと変換ロジックを有効にしてボリューム操作をKubernetesリポジトリー内のAzure-DiskプラグインからAzure Disk CSIプラグインにルーティングします。ノードにAzureDisk CSIプラグインがインストールおよび設定されていない場合、ツリー内のAzureDiskプラグインへのフォールバックをサポートします。CSIMigration機能フラグを有効にする必要があります。
- `CSIMigrationAzureDiskComplete`: Azure-Diskツリー内プラグインのkubeletおよびボリュームコントローラーへの登録を停止し、シムと変換ロジックを有効にして、Azure-Diskツリー内プラグインからAzureDisk CSIプラグインにボリューム操作をルーティングします。CSIMigrationおよびCSIMigrationAzureDisk機能フラグを有効にし、クラスター内のすべてのノードにAzureDisk CSIプラグインをインストールおよび設定する必要があります。
- `CSIMigrationAzureFile`: シムと変換ロジックを有効にしてボリューム操作をKubernetesリポジトリー内のAzure-FileプラグインからAzure File CSIプラグインにルーティングします。ノードにAzureFile CSIプラグインがインストールおよび設定されていない場合、ツリー内のAzureFileプラグインへのフォールバックをサポートします。CSIMigration機能フラグを有効にする必要があります。
- `CSIMigrationAzureFileComplete`: Azure-Fileツリー内プラグインのkubeletおよびボリュームコントローラーへの登録を停止し、シムと変換ロジックを有効にして、Azure-Fileツリー内プラグインからAzureFile CSIプラグインにボリューム操作をルーティングします。CSIMigrationおよびCSIMigrationAzureFile機能フラグを有効にし、クラスター内のすべてのノードにAzureFile CSIプラグインをインストールおよび設定する必要があります。
- `CSIMigrationGCE`: シムと変換ロジックを有効にしてボリューム操作をKubernetesリポジトリー内のGCE-PDプラグインからPD CSIプラグインにルーティングします。ノードにPD CSIプラグインがインストールおよび設定されていない場合、ツリー内のGCEプラグインへのフォールバックをサポートします。CSIMigration機能フラグを有効にする必要があります。
- `CSIMigrationGCEComplete`: GCE-PDのツリー内プラグインのkubeletおよびボリュームコントローラーへの登録を停止し、シムと変換ロジックがGCE-PDのツリー内プラグインからPD CSIプラグインにボリューム操作をルーティングできるようにします。CSIMigrationおよびCSIMigrationGCE機能フラグを有効にし、クラスター内のすべてのノードにPD CSIプラグインをインストールおよび設定する必要があります。
- `CSIMigrationOpenStack`: シムと変換ロジックを有効にしてボリューム操作をKubernetesリポジトリー内のCinderプラグインからCinder CSIプラグインにルーティングします。ノードにCinder CSIプラグインがインストールおよび設定されていない場合、ツリー内のCinderプラグインへのフォールバックをサポートします。CSIMigration機能フラグを有効にする必要があります。
- `CSIMigrationOpenStackComplete`: Cinderのツリー内プラグインのkubeletおよびボリュームコントローラーへの登録を停止し、シムと変換ロジックがCinderのツリー内プラグインからCinder CSIプラグインにボリューム操作をルーティングできるようにします。CSIMigrationおよびCSIMigrationOpenStack機能フラグを有効にし、クラスター内のすべてのノードにCinder CSIプラグインをインストールおよび設定する必要があります。
- `CSIMigrationvSphere`: シムと変換ロジックを有効にしてボリューム操作をKubernetesリポジトリー内のvSphereプラグインからvSphere CSIプラグインにルーティングします。ノードにvSphere CSIプラグインがインストールおよび設定されていない場合、ツリー内のvSphereプラグインへのフォールバックをサポートします。CSIMigration機能フラグを有効にする必要があります。
- `CSIMigrationvSphereComplete`: vSphereのツリー内プラグインのkubeletおよびボリュームコントローラーへの登録を停止し、シムと変換ロジックがvSphereのツリー内プラグインからvSphere CSIプラグインにボリューム操作をルーティングできるようにします。CSIMigrationおよびCSIMigrationvSphere機能フラグを有効にし、クラスター内のすべてのノードにvSphere CSIプラグインをインストールおよび設定する必要があります。
- `CSINodeInfo`: csi.storage.k8s.ioのCSINodeInfo APIオブジェクトに関連するすべてのロジックを有効にします。
- `CSIPersistentVolume`: [CSI(Container Storage Interface)](https://github.com/kubernetes/community/blob/master/contributors/design-proposals/storage/container-storage-interface.md)互換のボリュームプラグインを通してプロビジョニングされたボリュームの検出とマウントを有効にします。
- `CSIStorageCapacity`: CSIドライバーがストレージの容量情報を公開し、KubernetesのスケジューラーがPodをスケジュールするときにその情報を使用できるようにします。[ストレージ容量](/ja/docs/concepts/storage/storage-capacity/)を参照してください。
  詳細については[`csi`ボリュームタイプ](/docs/concepts/storage/volumes/#csi)ドキュメントを確認してください。
- `CSIVolumeFSGroupPolicy`: CSIドライバーが`fsGroupPolicy`フィールドを使用できるようにします。このフィールドは、CSIドライバーによって作成されたボリュームがボリュームのマウント時にボリュームの所有権とアクセス許可の変更をサポートするかどうかを制御します。
- `CustomCPUCFSQuotaPeriod`: ノードがCPUCFSQuotaPeriodを変更できるようにします。
- `CustomPodDNS`: `dnsConfig`プロパティを使用したPodのDNS設定のカスタマイズを有効にします。詳細は[PodのDNS構成](/ja/docs/concepts/services-networking/dns-pod-service/#pods-dns-config)で確認できます。
- `CustomResourceDefaulting`: OpenAPI v3バリデーションスキーマにおいて、デフォルト値のCRDサポートを有効にします。
- `CustomResourcePublishOpenAPI`: CRDのOpenAPI仕様での公開を有効にします。
- `CustomResourceSubresources`: [CustomResourceDefinition](/ja/docs/concepts/extend-kubernetes/api-extension/custom-resources/)から作成されたリソースの`/status`および`/scale`サブリソースを有効にします。
- `CustomResourceValidation`: [CustomResourceDefinition](/ja/docs/concepts/extend-kubernetes/api-extension/custom-resources/)から作成されたリソースのスキーマによる検証を有効にします。
- `CustomResourceWebhookConversion`: [CustomResourceDefinition](/ja/docs/concepts/extend-kubernetes/api-extension/custom-resources/)から作成されたリソースのWebhookベースの変換を有効にします。
- `DisableAcceleratorUsageMetrics`: [kubeletによって収集されたアクセラレータメトリクスを無効にします。](/docs/concepts/cluster-administration/system-metrics/)
- `DevicePlugins`: [device-plugins](/docs/concepts/cluster-administration/device-plugins/)によるノードでのリソースプロビジョニングを有効にします。
- `DefaultPodTopologySpread`: [デフォルトの配置](/docs/concepts/workloads/pods/pod-topology-spread-constraints/#internal-default-constraints)に`PodTopologySpread`スケジューリングプラグインの使用を有効にします。
- `DryRun`: サーバーサイドでの[dry run](/docs/reference/using-api/api-concepts/#dry-run)リクエストを有効にします。
- `DynamicAuditing`(*非推奨*): v1.19より前で動的監査を有効にするために使用されました。
- `DynamicKubeletConfig`: kubeletの動的構成を有効にします。[kubeletの再設定](/docs/tasks/administer-cluster/reconfigure-kubelet/)を参照してください。
- `DynamicProvisioningScheduling`: デフォルトのスケジューラーを拡張してボリュームトポロジーを認識しPVプロビジョニングを処理します。この機能は、v1.12の`VolumeScheduling`機能に完全に置き換えられました。
- `DynamicVolumeProvisioning`(*非推奨*): Podへの永続ボリュームの[動的プロビジョニング](/ja/docs/concepts/storage/dynamic-provisioning/)を有効にします。
- `EnableAggregatedDiscoveryTimeout` (*非推奨*): 集約されたディスカバリーコールで5秒のタイムアウトを有効にします。
- `EnableEquivalenceClassCache`: Podをスケジュールするときにスケジューラーがノードの同等をキャッシュできるようにします。
- `EphemeralContainers`: 稼働するPodに{{< glossary_tooltip text="ephemeral containers" term_id="ephemeral-container" >}}を追加する機能を有効にします。
- `EvenPodsSpread`: Podをトポロジードメイン全体で均等にスケジュールできるようにします。[Pod Topology Spread Constraints](/docs/concepts/workloads/pods/pod-topology-spread-constraints/)をご覧ください。
- `ExpandInUsePersistentVolumes`: 使用中のPVCのボリューム拡張を有効にします。[使用中のPersistentVolumeClaimのサイズ変更](/docs/concepts/storage/persistent-volumes/#resizing-an-in-use-persistentvolumeclaim)を参照してください。
- `ExpandPersistentVolumes`: 永続ボリュームの拡張を有効にします。[永続ボリューム要求の拡張](/docs/concepts/storage/persistent-volumes/#expanding-persistent-volumes-claims)を参照してください。
- `ExperimentalCriticalPodAnnotation`: [スケジューリングが保証されるよう](/docs/tasks/administer-cluster/guaranteed-scheduling-critical-addon-pods/)に特定のPodへの *クリティカル* の注釈を加える設定を有効にします。v1.13以降、この機能はPod PriorityおよびPreemptionによって非推奨になりました。
- `ExperimentalHostUserNamespaceDefaultingGate`: ホストするデフォルトのユーザー名前空間を有効にします。これは他のホストの名前空間やホストのマウントを使用しているコンテナ、特権を持つコンテナ、または名前空間のない特定の機能（たとえば`MKNODE`、`SYS_MODULE`など）を使用しているコンテナ用です。これはDockerデーモンでユーザー名前空間の再マッピングが有効になっている場合にのみ有効にすべきです。
- `EndpointSlice`: よりスケーラブルで拡張可能なネットワークエンドポイントのエンドポイントスライスを有効にします。[Enabling Endpoint Slices](/docs/tasks/administer-cluster/enabling-endpointslices/)をご覧ください。
- `EndpointSliceProxying`: このフィーチャーゲートを有効にすると、Linuxで実行されているkube-proxyはエンドポイントの代わりにエンドポイントスライスをプライマリデータソースとして使用し、スケーラビリティとパフォーマンスの向上を実現します。[Enabling Endpoint Slices](/ja/docs/tasks/administer-cluster/enabling-endpointslices/)をご覧ください。
- `WindowsEndpointSliceProxying`: このフィーチャーゲートを有効にすると、Windowsで実行されているkube-proxyはエンドポイントの代わりにエンドポイントスライスをプライマリデータソースとして使用し、スケーラビリティとパフォーマンスの向上を実現します。[Enabling Endpoint Slices](/ja/docs/tasks/administer-cluster/enabling-endpointslices/)をご覧ください。
- `GCERegionalPersistentDisk`: GCEでリージョナルPD機能を有効にします。
- `GenericEphemeralVolume`: 通常のボリュームのすべての機能をサポートする一時的なインラインボリュームを有効にします (サードパーティのストレージベンダー、ストレージ容量の追跡、スナップショットからの復元などによって提供されます)。[Ephemeral Volumes](/docs/concepts/storage/ephemeral-volumes/)をご覧ください。
- `HugePages`: 事前に割り当てられた[huge pages](/docs/tasks/manage-hugepages/scheduling-hugepages/)の割り当てと消費を有効にします。
- `HugePageStorageMediumSize`: 事前に割り当てられた複数のサイズの[huge pages](/docs/tasks/manage-hugepages/scheduling-hugepages/)のサポートを有効にします。
- `HyperVContainer`: Windowsコンテナの[Hyper-Vによる分離](https://docs.microsoft.com/en-us/virtualization/windowscontainers/manage-containers/hyperv-container)を有効にします。
- `HPAScaleToZero`: カスタムメトリクスまたは外部メトリクスを使用するときに、`HorizontalPodAutoscaler`リソースの`minReplicas`を0に設定できるようにします。
- `ImmutableEphemeralVolumes`: 安全性とパフォーマンスを向上させるために、個々のSecretとConfigMapが不変となるように指定できるようにします。
- `KubeletConfigFile`: 設定ファイルを使用して指定されたファイルからのkubelet設定の読み込みを有効にします。詳細は[設定ファイルによるkubeletパラメーターの設定](/docs/tasks/administer-cluster/kubelet-config-file/)で確認できます。
- `KubeletPluginsWatcher`: 調査ベースのプラグイン監視ユーティリティを有効にしてkubeletが[CSIボリュームドライバー](/docs/concepts/storage/volumes/#csi)などのプラグインを検出できるようにします。
- `KubeletPodResources`: kubeletのPodのリソースgrpcエンドポイントを有効にします。詳細は[デバイスモニタリングのサポート](https://github.com/kubernetes/enhancements/blob/master/keps/sig-node/compute-device-assignment.md)で確認できます。
- `LegacyNodeRoleBehavior`: 無効にすると、サービスロードバランサーの従来の動作とノードの中断により、`NodeDisruptionExclusion`と`ServiceNodeExclusion`によって提供される機能固有のラベルが優先され、`node-role.kubernetes.io/master`ラベルが無視されます。
- `LocalStorageCapacityIsolation`: [ローカルの一時ストレージ](/ja/docs/concepts/configuration/manage-resources-containers/)の消費を有効にして、[emptyDirボリューム](/docs/concepts/storage/volumes/#emptydir)の`sizeLimit`プロパティも有効にします。
- `LocalStorageCapacityIsolationFSQuotaMonitoring`: `LocalStorageCapacityIsolation`が[ローカルの一時ストレージ](/ja/docs/concepts/configuration/manage-resources-containers/)で有効になっていて、[emptyDirボリューム](/docs/concepts/storage/volumes/#emptydir)のbacking filesystemがプロジェクトクォータをサポートし有効になっている場合、プロジェクトクォータを使用して、パフォーマンスと精度を向上させるために、ファイルシステムへのアクセスではなく[emptyDirボリューム](/docs/concepts/storage/volumes/#emptydir)ストレージ消費を監視します。
- `MountContainers`: ホスト上のユーティリティコンテナをボリュームマウンターとして使用できるようにします。
- `MountPropagation`: あるコンテナによってマウントされたボリュームを他のコンテナまたはPodに共有できるようにします。詳細は[マウントの伝播](/docs/concepts/storage/volumes/#mount-propagation)で確認できます。
- `NodeDisruptionExclusion`: ノードラベル`node.kubernetes.io/exclude-disruption`の使用を有効にします。これにより、ゾーン障害時にノードが退避するのを防ぎます。
- `NodeLease`: 新しいLease APIを有効にしてノードヘルスシグナルとして使用できるノードのハートビートをレポートします。
- `NonPreemptingPriority`: PriorityClassとPodのNonPreemptingオプションを有効にします。
- `PersistentLocalVolumes`: Podで`local`ボリュームタイプの使用を有効にします。`local`ボリュームを要求する場合、Podアフィニティを指定する必要があります。
- `PodOverhead`: [PodOverhead](/docs/concepts/scheduling-eviction/pod-overhead/)機能を有効にして、Podのオーバーヘッドを考慮するようにします。
- `PodDisruptionBudget`: [PodDisruptionBudget](/docs/tasks/run-application/configure-pdb/)機能を有効にします。
- `PodPriority`: [優先度](/ja/docs/concepts/configuration/pod-priority-preemption/)に基づいてPodの再スケジューリングとプリエンプションを有効にします。
- `PodReadinessGates`: Podのreadinessの評価を拡張するために`PodReadinessGate`フィールドの設定を有効にします。詳細は[Pod readiness gate](/ja/docs/concepts/workloads/pods/pod-lifecycle/#pod-readiness-gate)で確認できます。
- `PodShareProcessNamespace`: Podで実行されているコンテナ間で単一のプロセス名前空間を共有するには、Podで`shareProcessNamespace`の設定を有効にします。詳細については、[Pod内のコンテナ間でプロセス名前空間を共有する](/docs/tasks/configure-pod-container/share-process-namespace/)をご覧ください。
- `ProcMountType`: コンテナのProcMountTypeの制御を有効にします。
- `PVCProtection`: 永続ボリューム要求（PVC）がPodでまだ使用されているときに削除されないようにします。
- `QOSReserved`: QoSレベルでのリソース予約を許可して、低いQoSレベルのポッドが高いQoSレベルで要求されたリソースにバーストするのを防ぎます（現時点ではメモリのみ）。
- `ResourceLimitsPriorityFunction`(*非推奨*): 入力したPodのCPU制限とメモリ制限の少なくとも1つを満たすノードに対して最低スコアを1に割り当てるスケジューラー優先機能を有効にします。その目的は同じスコアを持つノード間の関係を断つことです。
- `ResourceQuotaScopeSelectors`: リソース割当のスコープセレクターを有効にします。
- `RotateKubeletClientCertificate`: kubeletでクライアントTLS証明書のローテーションを有効にします。詳細は[kubeletの設定](/docs/reference/command-line-tools-reference/kubelet-tls-bootstrapping/#kubelet-configuration)で確認できます。
- `RotateKubeletServerCertificate`: kubeletでサーバーTLS証明書のローテーションを有効にします。詳細は[kubeletの設定](/docs/reference/command-line-tools-reference/kubelet-tls-bootstrapping/#kubelet-configuration)で確認できます。
- `RunAsGroup`: コンテナの初期化プロセスで設定されたプライマリグループIDの制御を有効にします。
- `RuntimeClass`: コンテナのランタイム構成を選択するには[RuntimeClass](/ja/docs/concepts/containers/runtime-class/)機能を有効にします。
- `ScheduleDaemonSetPods`: DaemonSetのPodをDaemonSetコントローラーではなく、デフォルトのスケジューラーによってスケジュールされるようにします。
- `SCTPSupport`: Pod、Service、Endpoints、EndpointSlice、およびNetworkPolicy定義で _SCTP_ `protocol`値を有効にします。
- `ServerSideApply`: APIサーバーで[サーバーサイドApply(SSA)](/docs/reference/using-api/server-side-apply/)のパスを有効にします。
- `ServiceAccountIssuerDiscovery`: APIサーバーにてサービスアカウント発行者のOIDC検出エンドポイント（発行者とJWKS URL）を有効にします。詳細については、[Podのサービスアカウント設定](/docs/tasks/configure-pod-container/configure-service-account/#service-account-issuer-discovery)をご覧ください。
- `ServiceAppProtocol`: サービスとエンドポイントで`AppProtocol`フィールドを有効にします。
- `ServiceLoadBalancerFinalizer`: サービスロードバランサーのファイナライザー保護を有効にします。
- `ServiceNodeExclusion`: クラウドプロバイダーによって作成されたロードバランサーからのノードの除外を有効にします。"`alpha.service-controller.kubernetes.io/exclude-balancer`"キーまたは`node.kubernetes.io/exclude-from-external-load-balancers`でラベル付けされている場合ノードは除外の対象となります。
- `ServiceTopology`: クラスタのノードトポロジーに基づいてトラフィックをルーティングするサービスを有効にします。詳細については、[Serviceトポロジー](/ja/docs/concepts/services-networking/service-topology/)を参照してください。
- `SetHostnameAsFQDN`: Podのホスト名として完全修飾ドメイン名（FQDN）を設定する機能を有効にします。[PodのsetHostnameAsFQDNフィールド](/ja/docs/concepts/services-networking/dns-pod-service/#pod-sethostnameasfqdn-field)を参照してください。
- `StartupProbe`: kubeletで[startup](/ja/docs/concepts/workloads/pods/pod-lifecycle/#when-should-you-use-a-startup-probe)プローブを有効にします。
- `StorageObjectInUseProtection`: PersistentVolumeまたはPersistentVolumeClaimオブジェクトがまだ使用されている場合、それらの削除を延期します。
- `StorageVersionHash`: apiserversがディスカバリーでストレージのバージョンハッシュを公開できるようにします。
- `StreamingProxyRedirects`: ストリーミングリクエストのバックエンド(kubelet)からのリダイレクトをインターセプト（およびフォロー）するようAPIサーバーに指示します。ストリーミングリクエストの例には`exec`、`attach`、`port-forward`リクエストが含まれます。
- `SupportIPVSProxyMode`: IPVSを使用したクラスター内サービスの負荷分散の提供を有効にします。詳細は[サービスプロキシー](/ja/docs/concepts/services-networking/service/#virtual-ips-and-service-proxies)で確認できます。
- `SupportPodPidsLimit`: PodのPID制限のサポートを有効にします。
- `Sysctls`: 各Podに設定できる名前空間付きのカーネルパラメーター(sysctl)のサポートを有効にします。詳細は[sysctls](/docs/tasks/administer-cluster/sysctl-cluster/)で確認できます。
- `TaintBasedEvictions`: ノードのTaintとPodのTolerationに基づいてノードからPodを排除できるようにします。詳細は[TaintとToleration](/ja/docs/concepts/scheduling-eviction/taint-and-toleration/)で確認できます。
- `TaintNodesByCondition`: [ノードの条件](/ja/docs/concepts/architecture/nodes/#condition)に基づいてノードの自動Taintを有効にします。
- `TokenRequest`: サービスアカウントリソースで`TokenRequest`エンドポイントを有効にします。
- `TokenRequestProjection`: [Projectedボリューム](/docs/concepts/storage/volumes/#projected)を使用したPodへのサービスアカウントのトークンの注入を有効にします。
- `TopologyManager`: Kubernetesのさまざまなコンポーネントのきめ細かいハードウェアリソース割り当てを調整するメカニズムを有効にします。[ノードのトポロジー管理ポリシーの制御](/docs/tasks/administer-cluster/topology-manager/)を参照してください。
- `TTLAfterFinished`: [TTLコントローラー](/ja/docs/concepts/workloads/controllers/ttlafterfinished/)が実行終了後にリソースをクリーンアップできるようにします。
- `VolumePVCDataSource`: 既存のPVCをデータソースとして指定するサポートを有効にします。
- `VolumeScheduling`: ボリュームトポロジー対応のスケジューリングを有効にし、PersistentVolumeClaim（PVC）バインディングにスケジューリングの決定を認識させます。また`PersistentLocalVolumes`フィーチャーゲートと一緒に使用すると[`local`](/docs/concepts/storage/volumes/#local)ボリュームタイプの使用が可能になります。
- `VolumeSnapshotDataSource`: ボリュームスナップショットのデータソースサポートを有効にします。
- `VolumeSubpathEnvExpansion`: 環境変数を`subPath`に展開するための`subPathExpr`フィールドを有効にします。
- `WatchBookmark`: ブックマークイベントの監視サポートを有効にします。
- `WindowsGMSA`: GMSA資格仕様をPodからコンテナランタイムに渡せるようにします。
- `WindowsRunAsUserName`: デフォルト以外のユーザーでWindowsコンテナアプリケーションを実行するためのサポートを有効にします。詳細については、[RunAsUserNameの設定](/docs/tasks/configure-pod-container/configure-runasusername)を参照してください。
- `WinDSR`: kube-proxyがWindows用のDSRロードバランサーを作成できるようにします。
- `WinOverlay`: kube-proxyをWindowsのオーバーレイモードで実行できるようにします。


## {{% heading "whatsnext" %}}

* Kubernetesの[非推奨ポリシー](/docs/reference/using-api/deprecation-policy/)では、機能とコンポーネントを削除するためのプロジェクトのアプローチを説明しています。
