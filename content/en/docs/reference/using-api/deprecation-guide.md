---
reviewers:
- liggitt
- lavalamp
- thockin
- smarterclayton
title: "Deprecated API Migration Guide"
weight: 45
content_type: reference
---

<!-- overview -->

As the Kubernetes API evolves, APIs are periodically reorganized or upgraded.
When APIs evolve, the old API is deprecated and eventually removed.
This page contains information you need to know when migrating from
deprecated API versions to newer and more stable API versions.

<!-- body -->

## Removed APIs by release


### v1.25

The **v1.25** release will stop serving the following deprecated API versions:

#### CronJob {#cronjob-v125}

The **batch/v1beta1** API version of CronJob will no longer be served in v1.25.

* Migrate manifests and API clients to use the **batch/v1** API version, available since v1.21.
* All existing persisted objects are accessible via the new API
* No notable changes

#### EndpointSlice {#endpointslice-v125}

The **discovery.k8s.io/v1beta1** API version of EndpointSlice will no longer be served in v1.25.

* Migrate manifests and API clients to use the **discovery.k8s.io/v1** API version, available since v1.21.
* All existing persisted objects are accessible via the new API
* Notable changes in **discovery.k8s.io/v1**:
    * use per Endpoint `nodeName` field instead of deprecated `topology["kubernetes.io/hostname"]` field
    * use per Endpoint `zone` field instead of deprecated `topology["topology.kubernetes.io/zone"]` field
    * `topology` is replaced with the `deprecatedTopology` field which is not writable in v1

#### Event {#event-v125}

The **events.k8s.io/v1beta1** API version of Event will no longer be served in v1.25.

* Migrate manifests and API clients to use the **events.k8s.io/v1** API version, available since v1.19.
* All existing persisted objects are accessible via the new API
* Notable changes in **events.k8s.io/v1**:
    * `type` is limited to `Normal` and `Warning`
    * `involvedObject` is renamed to `regarding`
    * `action`, `reason`, `reportingComponent`, and `reportingInstance` are required when creating new **events.k8s.io/v1** Events
    * use `eventTime` instead of the deprecated `firstTimestamp` field (which is renamed to `deprecatedFirstTimestamp` and not permitted in new **events.k8s.io/v1** Events)
    * use `series.lastObservedTime` instead of the deprecated `lastTimestamp` field (which is renamed to `deprecatedLastTimestamp` and not permitted in new **events.k8s.io/v1** Events)
    * use `series.count` instead of the deprecated `count` field (which is renamed to `deprecatedCount` and not permitted in new **events.k8s.io/v1** Events)
    * use `reportingComponent` instead of the deprecated `source.component` field (which is renamed to `deprecatedSource.component` and not permitted in new **events.k8s.io/v1** Events)
    * use `reportingInstance` instead of the deprecated `source.host` field (which is renamed to `deprecatedSource.host` and not permitted in new **events.k8s.io/v1** Events)

#### PodDisruptionBudget {#poddisruptionbudget-v125}

The **policy/v1beta1** API version of PodDisruptionBudget will no longer be served in v1.25.

* Migrate manifests and API clients to use the **policy/v1** API version, available since v1.21.
* All existing persisted objects are accessible via the new API
* Notable changes in **policy/v1**:
  * an empty `spec.selector` (`{}`) written to a `policy/v1` PodDisruptionBudget selects all pods in the namespace (in `policy/v1beta1` an empty `spec.selector` selected no pods). An unset `spec.selector` selects no pods in either API version.

#### PodSecurityPolicy {#psp-v125}

PodSecurityPolicy in the **policy/v1beta1** API version will no longer be served in v1.25, and the PodSecurityPolicy admission controller will be removed.

PodSecurityPolicy replacements are still under discussion, but current use can be migrated to
[3rd-party admission webhooks](/docs/reference/access-authn-authz/extensible-admission-controllers/) now.

#### RuntimeClass {#runtimeclass-v125}

RuntimeClass in the **node.k8s.io/v1beta1** API version will no longer be served in v1.25.

* Migrate manifests and API clients to use the **node.k8s.io/v1** API version, available since v1.20.
* All existing persisted objects are accessible via the new API
* No notable changes

### v1.22

The **v1.22** release will stop serving the following deprecated API versions:

#### Webhook resources {#webhook-resources-v122}

The **admissionregistration.k8s.io/v1beta1** API version of MutatingWebhookConfiguration and ValidatingWebhookConfiguration will no longer be served in v1.22.

* Migrate manifests and API clients to use the **admissionregistration.k8s.io/v1** API version, available since v1.16.
* All existing persisted objects are accessible via the new APIs
* Notable changes:
    * `webhooks[*].failurePolicy` default changed from `Ignore` to `Fail` for v1
    * `webhooks[*].matchPolicy` default changed from `Exact` to `Equivalent` for v1
    * `webhooks[*].timeoutSeconds` default changed from `30s` to `10s` for v1
    * `webhooks[*].sideEffects` default value is removed, and the field made required, and only `None` and `NoneOnDryRun` are permitted for v1
    * `webhooks[*].admissionReviewVersions` default value is removed and the field made required for v1 (supported versions for AdmissionReview are `v1` and `v1beta1`)
    * `webhooks[*].name` must be unique in the list for objects created via `admissionregistration.k8s.io/v1`

#### CustomResourceDefinition {#customresourcedefinition-v122}

The **apiextensions.k8s.io/v1beta1** API version of CustomResourceDefinition will no longer be served in v1.22.

* Migrate manifests and API clients to use the **apiextensions.k8s.io/v1** API version, available since v1.16.
* All existing persisted objects are accessible via the new API
* Notable changes:
    * `spec.scope` is no longer defaulted to `Namespaced` and must be explicitly specified
    * `spec.version` is removed in v1; use `spec.versions` instead
    * `spec.validation` is removed in v1; use `spec.versions[*].schema` instead
    * `spec.subresources` is removed in v1; use `spec.versions[*].subresources` instead
    * `spec.additionalPrinterColumns` is removed in v1; use `spec.versions[*].additionalPrinterColumns` instead
    * `spec.conversion.webhookClientConfig` is moved to `spec.conversion.webhook.clientConfig` in v1
    * `spec.conversion.conversionReviewVersions` is moved to `spec.conversion.webhook.conversionReviewVersions` in v1
    * `spec.versions[*].schema.openAPIV3Schema` is now required when creating v1 CustomResourceDefinition objects, and must be a [structural schema](/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/#specifying-a-structural-schema)
    * `spec.preserveUnknownFields: true` is disallowed when creating v1 CustomResourceDefinition objects; it must be specified within schema definitions as `x-kubernetes-preserve-unknown-fields: true`
    * In `additionalPrinterColumns` items, the `JSONPath` field was renamed to `jsonPath` in v1 (fixes [#66531](https://github.com/kubernetes/kubernetes/issues/66531))

#### APIService {#apiservice-v122}

The **apiregistration.k8s.io/v1beta1** API version of APIService will no longer be served in v1.22.

* Migrate manifests and API clients to use the **apiregistration.k8s.io/v1** API version, available since v1.10.
* All existing persisted objects are accessible via the new API
* No notable changes

#### TokenReview {#tokenreview-v122}

The **authentication.k8s.io/v1beta1** API version of TokenReview will no longer be served in v1.22.

* Migrate manifests and API clients to use the **authentication.k8s.io/v1** API version, available since v1.6.
* No notable changes

#### SubjectAccessReview resources {#subjectaccessreview-resources-v122}

The **authorization.k8s.io/v1beta1** API version of LocalSubjectAccessReview, SelfSubjectAccessReview, and SubjectAccessReview will no longer be served in v1.22.

* Migrate manifests and API clients to use the **authorization.k8s.io/v1** API version, available since v1.6.
* Notable changes:
    * `spec.group` was renamed to `spec.groups` in v1 (fixes [#32709](https://github.com/kubernetes/kubernetes/issues/32709))

#### CertificateSigningRequest {#certificatesigningrequest-v122}

The **certificates.k8s.io/v1beta1** API version of CertificateSigningRequest will no longer be served in v1.22.

* Migrate manifests and API clients to use the **certificates.k8s.io/v1** API version, available since v1.19.
* All existing persisted objects are accessible via the new API
* Notable changes in `certificates.k8s.io/v1`:
    * For API clients requesting certificates:
        * `spec.signerName` is now required (see [known Kubernetes signers](/docs/reference/access-authn-authz/certificate-signing-requests/#kubernetes-signers)), and requests for `kubernetes.io/legacy-unknown` are not allowed to be created via the `certificates.k8s.io/v1` API
        * `spec.usages` is now required, may not contain duplicate values, and must only contain known usages
    * For API clients approving or signing certificates:
        * `status.conditions` may not contain duplicate types
        * `status.conditions[*].status` is now required
        * `status.certificate` must be PEM-encoded, and contain only `CERTIFICATE` blocks

#### Lease {#lease-v122}

The **coordination.k8s.io/v1beta1** API version of Lease will no longer be served in v1.22.

* Migrate manifests and API clients to use the **coordination.k8s.io/v1** API version, available since v1.14.
* All existing persisted objects are accessible via the new API
* No notable changes

#### Ingress {#ingress-v122}

The **extensions/v1beta1** and **networking.k8s.io/v1beta1** API versions of Ingress will no longer be served in v1.22.

* Migrate manifests and API clients to use the **networking.k8s.io/v1** API version, available since v1.19.
* All existing persisted objects are accessible via the new API
* Notable changes:
    * `spec.backend` is renamed to `spec.defaultBackend`
    * The backend `serviceName` field is renamed to `service.name`
    * Numeric backend `servicePort` fields are renamed to `service.port.number`
    * String backend `servicePort` fields are renamed to `service.port.name`
    * `pathType` is now required for each specified path. Options are `Prefix`, `Exact`, and `ImplementationSpecific`. To match the undefined `v1beta1` behavior, use `ImplementationSpecific`.

#### IngressClass {#ingressclass-v122}

The **networking.k8s.io/v1beta1** API version of IngressClass will no longer be served in v1.22.

* Migrate manifests and API clients to use the **networking.k8s.io/v1** API version, available since v1.19.
* All existing persisted objects are accessible via the new API
* No notable changes

#### RBAC resources {#rbac-resources-v122}

The **rbac.authorization.k8s.io/v1beta1** API version of ClusterRole, ClusterRoleBinding, Role, and RoleBinding will no longer be served in v1.22.

* Migrate manifests and API clients to use the **rbac.authorization.k8s.io/v1** API version, available since v1.8.
* All existing persisted objects are accessible via the new APIs
* No notable changes

#### PriorityClass {#priorityclass-v122}

The **scheduling.k8s.io/v1beta1** API version of PriorityClass will no longer be served in v1.22.

* Migrate manifests and API clients to use the **scheduling.k8s.io/v1** API version, available since v1.14.
* All existing persisted objects are accessible via the new API
* No notable changes

#### Storage resources {#storage-resources-v122}

The **storage.k8s.io/v1beta1** API version of CSIDriver, CSINode, StorageClass, and VolumeAttachment will no longer be served in v1.22.

* Migrate manifests and API clients to use the **storage.k8s.io/v1** API version
  * CSIDriver is available in **storage.k8s.io/v1** since v1.19.
  * CSINode is available in **storage.k8s.io/v1** since v1.17
  * StorageClass is available in **storage.k8s.io/v1** since v1.6
  * VolumeAttachment is available in **storage.k8s.io/v1** v1.13
* All existing persisted objects are accessible via the new APIs
* No notable changes

### v1.16

The **v1.16** release stopped serving the following deprecated API versions:

#### NetworkPolicy {#networkpolicy-v116}

The **extensions/v1beta1** API version of NetworkPolicy is no longer served as of v1.16.

* Migrate manifests and API clients to use the **networking.k8s.io/v1** API version, available since v1.8.
* All existing persisted objects are accessible via the new API

#### DaemonSet {#daemonset-v116}

The **extensions/v1beta1** and **apps/v1beta2** API versions of DaemonSet are no longer served as of v1.16.

* Migrate manifests and API clients to use the **apps/v1** API version, available since v1.9.
* All existing persisted objects are accessible via the new API
* Notable changes:
    * `spec.templateGeneration` is removed
    * `spec.selector` is now required and immutable after creation; use the existing template labels as the selector for seamless upgrades
    * `spec.updateStrategy.type` now defaults to `RollingUpdate` (the default in `extensions/v1beta1` was `OnDelete`)

#### Deployment {#deployment-v116}

The **extensions/v1beta1**, **apps/v1beta1**, and **apps/v1beta2** API versions of Deployment are no longer served as of v1.16.

* Migrate manifests and API clients to use the **apps/v1** API version, available since v1.9.
* All existing persisted objects are accessible via the new API
* Notable changes:
    * `spec.rollbackTo` is removed
    * `spec.selector` is now required and immutable after creation; use the existing template labels as the selector for seamless upgrades
    * `spec.progressDeadlineSeconds` now defaults to `600` seconds (the default in `extensions/v1beta1` was no deadline)
    * `spec.revisionHistoryLimit` now defaults to `10` (the default in `apps/v1beta1` was `2`, the default in `extensions/v1beta1` was to retain all)
    * `maxSurge` and `maxUnavailable` now default to `25%` (the default in `extensions/v1beta1` was `1`)

#### StatefulSet {#statefulset-v116}

The **apps/v1beta1** and **apps/v1beta2** API versions of StatefulSet are no longer served as of v1.16.

* Migrate manifests and API clients to use the **apps/v1** API version, available since v1.9.
* All existing persisted objects are accessible via the new API
* Notable changes:
    * `spec.selector` is now required and immutable after creation; use the existing template labels as the selector for seamless upgrades
    * `spec.updateStrategy.type` now defaults to `RollingUpdate` (the default in `apps/v1beta1` was `OnDelete`)

#### ReplicaSet {#replicaset-v116}

The **extensions/v1beta1**, **apps/v1beta1**, and **apps/v1beta2** API versions of ReplicaSet are no longer served as of v1.16.

* Migrate manifests and API clients to use the **apps/v1** API version, available since v1.9.
* All existing persisted objects are accessible via the new API
* Notable changes:
    * `spec.selector` is now required and immutable after creation; use the existing template labels as the selector for seamless upgrades

#### PodSecurityPolicy {#psp-v116}

The **extensions/v1beta1** API version of PodSecurityPolicy is no longer served as of v1.16.

* Migrate manifests and API client to use the **policy/v1beta1** API version, available since v1.10.
* Note that the **policy/v1beta1** API version of PodSecurityPolicy will be removed in v1.25.

## What to do

### Test with deprecated APIs disabled

You can test your clusters by starting an API server with specific API versions disabled
to simulate upcoming removals. Add the following flag to the API server startup arguments:

`--runtime-config=<group>/<version>=false`

For example:

`--runtime-config=admissionregistration.k8s.io/v1beta1=false,apiextensions.k8s.io/v1beta1,...`

### Locate use of deprecated APIs

Use [client warnings, metrics, and audit information available in 1.19+](https://kubernetes.io/blog/2020/09/03/warnings/#deprecation-warnings)
to locate use of deprecated APIs.

### Migrate to non-deprecated APIs

* Update custom integrations and controllers to call the non-deprecated APIs
* Change YAML files to reference the non-deprecated APIs

    You can use the `kubectl-convert` command (`kubectl convert` prior to v1.20)
    to automatically convert an existing object:
    
    `kubectl-convert -f <file> --output-version <group>/<version>`.

    For example, to convert an older Deployment to `apps/v1`, you can run:
    
    `kubectl-convert -f ./my-deployment.yaml --output-version apps/v1`

    Note that this may use non-ideal default values. To learn more about a specific
    resource, check the Kubernetes [API reference](/docs/reference/kubernetes-api/).
