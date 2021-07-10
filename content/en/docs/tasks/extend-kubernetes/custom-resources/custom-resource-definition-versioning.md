---
title: Versions in CustomResourceDefinitions
reviewers:
- sttts
- liggitt
content_type: task
weight: 30
min-kubernetes-server-version: v1.16
---

<!-- overview -->
This page explains how to add versioning information to
{{< api-reference page="extend-resources/custom-resource-definition-v1" >}}, to indicate the stability
level of your CustomResourceDefinitions or advance your API to a new version with conversion between API representations. It also describes how to upgrade an object from one version to another.

## {{% heading "prerequisites" %}}


{{< include "task-tutorial-prereqs.md" >}}

You should have a initial understanding of [custom resources](/docs/concepts/extend-kubernetes/api-extension/custom-resources/).

{{< version-check >}}

<!-- steps -->

## Overview

The CustomResourceDefinition API provides a workflow for introducing and upgrading
to new versions of a CustomResourceDefinition.

When a CustomResourceDefinition is created, the first version is set in the
CustomResourceDefinition `spec.versions` list to an appropriate stability level
and a version number. For example `v1beta1` would indicate that the first
version is not yet stable. All custom resource objects will initially be stored
at this version.

Once the CustomResourceDefinition is created, clients may begin using the
`v1beta1` API.

Later it might be necessary to add new version such as `v1`.

Adding a new version:

1. Pick a conversion strategy. Since custom resource objects need to be able to
   be served at both versions, that means they will sometimes be served at a
   different version than their storage version. In order for this to be
   possible, the custom resource objects must sometimes be converted between the
   version they are stored at and the version they are served at. If the
   conversion involves schema changes and requires custom logic, a conversion
   webhook should be used. If there are no schema changes, the default `None`
   conversion strategy may be used and only the `apiVersion` field will be
   modified when serving different versions.
1. If using conversion webhooks, create and deploy the conversion webhook. See
   the [Webhook conversion](#webhook-conversion) for more details.
1. Update the CustomResourceDefinition to include the new version in the
   `spec.versions` list with `served:true`.  Also, set `spec.conversion` field
   to the selected conversion strategy. If using a conversion webhook, configure
   `spec.conversion.webhookClientConfig` field to call the webhook.

Once the new version is added, clients may incrementally migrate to the new
version. It is perfectly safe for some clients to use the old version while
others use the new version.

Migrate stored objects to the new version:

1. See the [upgrade existing objects to a new stored version](#upgrade-existing-objects-to-a-new-stored-version) section.

It is safe for clients to use both the old and new version before, during and
after upgrading the objects to a new stored version.

Removing an old version:

1. Ensure all clients are fully migrated to the new version. The kube-apiserver
   logs can be reviewed to help identify any clients that are still accessing via
   the old version.
1. Set `served` to `false` for the old version in the `spec.versions` list. If
   any clients are still unexpectedly using the old version they may begin reporting
   errors attempting to access the custom resource objects at the old version.
   If this occurs, switch back to using `served:true` on the old version, migrate the 
   remaining clients to the new version and repeat this step.
1. Ensure the [upgrade of existing objects to the new stored version](#upgrade-existing-objects-to-a-new-stored-version) step has been completed.
    1. Verify that the `storage` is set to `true` for the new version in the `spec.versions` list in the CustomResourceDefinition.
    1. Verify that the old version is no longer listed in the CustomResourceDefinition `status.storedVersions`.
1. Remove the old version from the CustomResourceDefinition `spec.versions` list.
1. Drop conversion support for the old version in conversion webhooks.

## Specify multiple versions

The CustomResourceDefinition API `versions` field can be used to support multiple versions of custom resources that you
have developed. Versions can have different schemas, and conversion webhooks can convert custom resources between versions.
Webhook conversions should follow the [Kubernetes API conventions](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md) wherever applicable.
Specifically, See the [API change documentation](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api_changes.md) for a set of useful gotchas and suggestions.

{{< note >}}
In `apiextensions.k8s.io/v1beta1`, there was a `version` field instead of `versions`. The
`version` field is deprecated and optional, but if it is not empty, it must
match the first item in the `versions` field.
{{< /note >}}

This example shows a CustomResourceDefinition with two versions. For the first
example, the assumption is all versions share the same schema with no conversion
between them. The comments in the YAML provide more context.

{{< tabs name="CustomResourceDefinition_versioning_example_1" >}}
{{% tab name="apiextensions.k8s.io/v1" %}}
```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  # name must match the spec fields below, and be in the form: <plural>.<group>
  name: crontabs.example.com
spec:
  # group name to use for REST API: /apis/<group>/<version>
  group: example.com
  # list of versions supported by this CustomResourceDefinition
  versions:
  - name: v1beta1
    # Each version can be enabled/disabled by Served flag.
    served: true
    # One and only one version must be marked as the storage version.
    storage: true
    # A schema is required
    schema:
      openAPIV3Schema:
        type: object
        properties:
          host:
            type: string
          port:
            type: string
  - name: v1
    served: true
    storage: false
    schema:
      openAPIV3Schema:
        type: object
        properties:
          host:
            type: string
          port:
            type: string
  # The conversion section is introduced in Kubernetes 1.13+ with a default value of
  # None conversion (strategy sub-field set to None).
  conversion:
    # None conversion assumes the same schema for all versions and only sets the apiVersion
    # field of custom resources to the proper value
    strategy: None
  # either Namespaced or Cluster
  scope: Namespaced
  names:
    # plural name to be used in the URL: /apis/<group>/<version>/<plural>
    plural: crontabs
    # singular name to be used as an alias on the CLI and for display
    singular: crontab
    # kind is normally the CamelCased singular type. Your resource manifests use this.
    kind: CronTab
    # shortNames allow shorter string to match your resource on the CLI
    shortNames:
    - ct
```
{{% /tab %}}
{{% tab name="apiextensions.k8s.io/v1beta1" %}}
```yaml
# Deprecated in v1.16 in favor of apiextensions.k8s.io/v1
apiVersion: apiextensions.k8s.io/v1beta1
kind: CustomResourceDefinition
metadata:
  # name must match the spec fields below, and be in the form: <plural>.<group>
  name: crontabs.example.com
spec:
  # group name to use for REST API: /apis/<group>/<version>
  group: example.com
  # list of versions supported by this CustomResourceDefinition
  versions:
  - name: v1beta1
    # Each version can be enabled/disabled by Served flag.
    served: true
    # One and only one version must be marked as the storage version.
    storage: true
  - name: v1
    served: true
    storage: false
  validation:
    openAPIV3Schema:
      type: object
      properties:
        host:
          type: string
        port:
          type: string
  # The conversion section is introduced in Kubernetes 1.13+ with a default value of
  # None conversion (strategy sub-field set to None).
  conversion:
    # None conversion assumes the same schema for all versions and only sets the apiVersion
    # field of custom resources to the proper value
    strategy: None
  # either Namespaced or Cluster
  scope: Namespaced
  names:
    # plural name to be used in the URL: /apis/<group>/<version>/<plural>
    plural: crontabs
    # singular name to be used as an alias on the CLI and for display
    singular: crontab
    # kind is normally the CamelCased singular type. Your resource manifests use this.
    kind: CronTab
    # shortNames allow shorter string to match your resource on the CLI
    shortNames:
    - ct
```
{{% /tab %}}
{{< /tabs >}}

You can save the CustomResourceDefinition in a YAML file, then use
`kubectl apply` to create it.

```shell
kubectl apply -f my-versioned-crontab.yaml
```

After creation, the API server starts to serve each enabled version at an HTTP
REST endpoint. In the above example, the API versions are available at
`/apis/example.com/v1beta1` and `/apis/example.com/v1`.

### Version priority

Regardless of the order in which versions are defined in a
CustomResourceDefinition, the version with the highest priority is used by
kubectl as the default version to access objects. The priority is determined
by parsing the _name_ field to determine the version number, the stability
(GA, Beta, or Alpha), and the sequence within that stability level.

The algorithm used for sorting the versions is designed to sort versions in the
same way that the Kubernetes project sorts Kubernetes versions. Versions start with a
`v` followed by a number, an optional `beta` or `alpha` designation, and
optional additional numeric versioning information. Broadly, a version string might look
like `v2` or `v2beta1`. Versions are sorted using the following algorithm:

- Entries that follow Kubernetes version patterns are sorted before those that
  do not.
- For entries that follow Kubernetes version patterns, the numeric portions of
  the version string is sorted largest to smallest.
- If the strings `beta` or `alpha` follow the first numeric portion, they sorted
  in that order, after the equivalent string without the `beta` or `alpha`
  suffix (which is presumed to be the GA version).
- If another number follows the `beta`, or `alpha`, those numbers are also
  sorted from largest to smallest.
- Strings that don't fit the above format are sorted alphabetically and the
  numeric portions are not treated specially. Notice that in the example below,
  `foo1` is sorted above `foo10`. This is different from the sorting of the
  numeric portion of entries that do follow the Kubernetes version patterns.

This might make sense if you look at the following sorted version list:

```none
- v10
- v2
- v1
- v11beta2
- v10beta3
- v3beta1
- v12alpha1
- v11alpha2
- foo1
- foo10
```

For the example in [Specify multiple versions](#specify-multiple-versions), the
version sort order is `v1`, followed by `v1beta1`. This causes the kubectl
command to use `v1` as the default version unless the provided object specifies
the version.

### Version deprecation

{{< feature-state state="stable" for_k8s_version="v1.19" >}}

Starting in v1.19, a CustomResourceDefinition can indicate a particular version of the resource it defines is deprecated.
When API requests to a deprecated version of that resource are made, a warning message is returned in the API response as a header.
The warning message for each deprecated version of the resource can be customized if desired.

A customized warning message should indicate the deprecated API group, version, and kind,
and should indicate what API group, version, and kind should be used instead, if applicable.

{{< tabs name="CustomResourceDefinition_versioning_deprecated" >}}
{{% tab name="apiextensions.k8s.io/v1" %}}
```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
  name: crontabs.example.com
spec:
  group: example.com
  names:
    plural: crontabs
    singular: crontab
    kind: CronTab
  scope: Namespaced
  versions:
  - name: v1alpha1
    served: true
    # This indicates the v1alpha1 version of the custom resource is deprecated.
    # API requests to this version receive a warning header in the server response.
    deprecated: true
    # This overrides the default warning returned to API clients making v1alpha1 API requests.
    deprecationWarning: "example.com/v1alpha1 CronTab is deprecated; see http://example.com/v1alpha1-v1 for instructions to migrate to example.com/v1 CronTab"
    schema: ...
  - name: v1beta1
    served: true
    # This indicates the v1beta1 version of the custom resource is deprecated.
    # API requests to this version receive a warning header in the server response.
    # A default warning message is returned for this version.
    deprecated: true
    schema: ...
  - name: v1
    served: true
    storage: true
    schema: ...
```
{{% /tab %}}
{{% tab name="apiextensions.k8s.io/v1beta1" %}}
```yaml
# Deprecated in v1.16 in favor of apiextensions.k8s.io/v1
apiVersion: apiextensions.k8s.io/v1beta1
kind: CustomResourceDefinition
metadata:
  name: crontabs.example.com
spec:
  group: example.com
  names:
    plural: crontabs
    singular: crontab
    kind: CronTab
  scope: Namespaced
  validation: ...
  versions:
  - name: v1alpha1
    served: true
    # This indicates the v1alpha1 version of the custom resource is deprecated.
    # API requests to this version receive a warning header in the server response.
    deprecated: true
    # This overrides the default warning returned to API clients making v1alpha1 API requests.
    deprecationWarning: "example.com/v1alpha1 CronTab is deprecated; see http://example.com/v1alpha1-v1 for instructions to migrate to example.com/v1 CronTab"
  - name: v1beta1
    served: true
    # This indicates the v1beta1 version of the custom resource is deprecated.
    # API requests to this version receive a warning header in the server response.
    # A default warning message is returned for this version.
    deprecated: true
  - name: v1
    served: true
    storage: true
```
{{% /tab %}}
{{< /tabs >}}


## Webhook conversion

{{< feature-state state="stable" for_k8s_version="v1.16" >}}

{{< note >}}
Webhook conversion is available as beta since 1.15, and as alpha since Kubernetes 1.13. The
`CustomResourceWebhookConversion` feature must be enabled, which is the case automatically for many clusters for beta features. Please refer to the [feature gate](/docs/reference/command-line-tools-reference/feature-gates/) documentation for more information.
{{< /note >}}

The above example has a None conversion between versions which only sets the `apiVersion` field
on conversion and does not change the rest of the object. The API server also supports webhook
conversions that call an external service in case a conversion is required. For example when:

* custom resource is requested in a different version than stored version.
* Watch is created in one version but the changed object is stored in another version.
* custom resource PUT request is in a different version than storage version.

To cover all of these cases and to optimize conversion by the API server, 
the conversion requests may contain multiple objects in order to minimize the external calls.
The webhook should perform these conversions independently.

### Write a conversion webhook server

Please refer to the implementation of the [custom resource conversion webhook
server](https://github.com/kubernetes/kubernetes/tree/v1.15.0/test/images/crd-conversion-webhook/main.go)
that is validated in a Kubernetes e2e test. The webhook handles the
`ConversionReview` requests sent by the API servers, and sends back conversion
results wrapped in `ConversionResponse`. Note that the request
contains a list of custom resources that need to be converted independently without
changing the order of objects.
The example server is organized in a way to be reused for other conversions.
Most of the common code are located in the
[framework file](https://github.com/kubernetes/kubernetes/tree/v1.15.0/test/images/crd-conversion-webhook/converter/framework.go)
that leaves only
[one function](https://github.com/kubernetes/kubernetes/blob/v1.15.0/test/images/crd-conversion-webhook/converter/example_converter.go#L29-L80)
to be implemented for different conversions.

{{< note >}}
The example conversion webhook server leaves the `ClientAuth` field
[empty](https://github.com/kubernetes/kubernetes/tree/v1.13.0/test/images/crd-conversion-webhook/config.go#L47-L48),
which defaults to `NoClientCert`. This means that the webhook server does not
authenticate the identity of the clients, supposedly API servers. If you need
mutual TLS or other ways to authenticate the clients, see
how to [authenticate API servers](/docs/reference/access-authn-authz/extensible-admission-controllers/#authenticate-apiservers).
{{< /note >}}

#### Permissible mutations

A conversion webhook must not mutate anything inside of `metadata` of the converted object
other than `labels` and `annotations`.
Attempted changes to `name`, `UID` and `namespace` are rejected and fail the request
which caused the conversion. All other changes are ignored.  

### Deploy the conversion webhook service

Documentation for deploying the conversion webhook is the same as for the
[admission webhook example service](/docs/reference/access-authn-authz/extensible-admission-controllers/#deploy_the_admission_webhook_service).
The assumption for next sections is that the conversion webhook server is deployed to a service
named `example-conversion-webhook-server` in `default` namespace and serving traffic on path `/crdconvert`.

{{< note >}}
When the webhook server is deployed into the Kubernetes cluster as a
service, it has to be exposed via a service on port 443 (The server
itself can have an arbitrary port but the service object should map it to port 443).
The communication between the API server and the webhook service may fail
if a different port is used for the service.
{{< /note >}}

### Configure CustomResourceDefinition to use conversion webhooks

The `None` conversion example can be extended to use the conversion webhook by modifying `conversion`
section of the `spec`:

{{< tabs name="CustomResourceDefinition_versioning_example_2" >}}
{{% tab name="apiextensions.k8s.io/v1" %}}
```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  # name must match the spec fields below, and be in the form: <plural>.<group>
  name: crontabs.example.com
spec:
  # group name to use for REST API: /apis/<group>/<version>
  group: example.com
  # list of versions supported by this CustomResourceDefinition
  versions:
  - name: v1beta1
    # Each version can be enabled/disabled by Served flag.
    served: true
    # One and only one version must be marked as the storage version.
    storage: true
    # Each version can define it's own schema when there is no top-level
    # schema is defined.
    schema:
      openAPIV3Schema:
        type: object
        properties:
          hostPort:
            type: string
  - name: v1
    served: true
    storage: false
    schema:
      openAPIV3Schema:
        type: object
        properties:
          host:
            type: string
          port:
            type: string
  conversion:
    # a Webhook strategy instruct API server to call an external webhook for any conversion between custom resources.
    strategy: Webhook
    # webhook is required when strategy is `Webhook` and it configures the webhook endpoint to be called by API server.
    webhook:
      # conversionReviewVersions indicates what ConversionReview versions are understood/preferred by the webhook.
      # The first version in the list understood by the API server is sent to the webhook.
      # The webhook must respond with a ConversionReview object in the same version it received.
      conversionReviewVersions: ["v1","v1beta1"]
      clientConfig:
        service:
          namespace: default
          name: example-conversion-webhook-server
          path: /crdconvert
        caBundle: "Ci0tLS0tQk...<base64-encoded PEM bundle>...tLS0K"
  # either Namespaced or Cluster
  scope: Namespaced
  names:
    # plural name to be used in the URL: /apis/<group>/<version>/<plural>
    plural: crontabs
    # singular name to be used as an alias on the CLI and for display
    singular: crontab
    # kind is normally the CamelCased singular type. Your resource manifests use this.
    kind: CronTab
    # shortNames allow shorter string to match your resource on the CLI
    shortNames:
    - ct
```
{{% /tab %}}
{{% tab name="apiextensions.k8s.io/v1beta1" %}}
```yaml
# Deprecated in v1.16 in favor of apiextensions.k8s.io/v1
apiVersion: apiextensions.k8s.io/v1beta1
kind: CustomResourceDefinition
metadata:
  # name must match the spec fields below, and be in the form: <plural>.<group>
  name: crontabs.example.com
spec:
  # group name to use for REST API: /apis/<group>/<version>
  group: example.com
  # prunes object fields that are not specified in OpenAPI schemas below.
  preserveUnknownFields: false
  # list of versions supported by this CustomResourceDefinition
  versions:
  - name: v1beta1
    # Each version can be enabled/disabled by Served flag.
    served: true
    # One and only one version must be marked as the storage version.
    storage: true
    # Each version can define it's own schema when there is no top-level
    # schema is defined.
    schema:
      openAPIV3Schema:
        type: object
        properties:
          hostPort:
            type: string
  - name: v1
    served: true
    storage: false
    schema:
      openAPIV3Schema:
        type: object
        properties:
          host:
            type: string
          port:
            type: string
  conversion:
    # a Webhook strategy instruct API server to call an external webhook for any conversion between custom resources.
    strategy: Webhook
    # webhookClientConfig is required when strategy is `Webhook` and it configures the webhook endpoint to be called by API server.
    webhookClientConfig:
      service:
        namespace: default
        name: example-conversion-webhook-server
        path: /crdconvert
      caBundle: "Ci0tLS0tQk...<base64-encoded PEM bundle>...tLS0K"
  # either Namespaced or Cluster
  scope: Namespaced
  names:
    # plural name to be used in the URL: /apis/<group>/<version>/<plural>
    plural: crontabs
    # singular name to be used as an alias on the CLI and for display
    singular: crontab
    # kind is normally the CamelCased singular type. Your resource manifests use this.
    kind: CronTab
    # shortNames allow shorter string to match your resource on the CLI
    shortNames:
    - ct
```
{{% /tab %}}
{{< /tabs >}}

You can save the CustomResourceDefinition in a YAML file, then use
`kubectl apply` to apply it.

```shell
kubectl apply -f my-versioned-crontab-with-conversion.yaml
```

Make sure the conversion service is up and running before applying new changes.

### Contacting the webhook

Once the API server has determined a request should be sent to a conversion webhook,
it needs to know how to contact the webhook. This is specified in the `webhookClientConfig`
stanza of the webhook configuration.

Conversion webhooks can either be called via a URL or a service reference,
and can optionally include a custom CA bundle to use to verify the TLS connection.

### URL

`url` gives the location of the webhook, in standard URL form
(`scheme://host:port/path`).

The `host` should not refer to a service running in the cluster; use
a service reference by specifying the `service` field instead.
The host might be resolved via external DNS in some apiservers
(i.e., `kube-apiserver` cannot resolve in-cluster DNS as that would
be a layering violation). `host` may also be an IP address.

Please note that using `localhost` or `127.0.0.1` as a `host` is
risky unless you take great care to run this webhook on all hosts
which run an apiserver which might need to make calls to this
webhook. Such installations are likely to be non-portable or not readily run in a new cluster.

The scheme must be "https"; the URL must begin with "https://".

Attempting to use a user or basic auth (for example "user:password@") is not allowed.
Fragments ("#...") and query parameters ("?...") are also not allowed.

Here is an example of a conversion webhook configured to call a URL
(and expects the TLS certificate to be verified using system trust roots, so does not specify a caBundle):

{{< tabs name="CustomResourceDefinition_versioning_example_3" >}}
{{% tab name="apiextensions.k8s.io/v1" %}}
```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
...
spec:
  ...
  conversion:
    strategy: Webhook
    webhook:
      clientConfig:
        url: "https://my-webhook.example.com:9443/my-webhook-path"
...
```
{{% /tab %}}
{{% tab name="apiextensions.k8s.io/v1beta1" %}}
```yaml
# Deprecated in v1.16 in favor of apiextensions.k8s.io/v1
apiVersion: apiextensions.k8s.io/v1beta1
kind: CustomResourceDefinition
...
spec:
  ...
  conversion:
    strategy: Webhook
    webhookClientConfig:
      url: "https://my-webhook.example.com:9443/my-webhook-path"
...
```
{{% /tab %}}
{{< /tabs >}}

### Service Reference

The `service` stanza inside `webhookClientConfig` is a reference to the service for a conversion webhook.
If the webhook is running within the cluster, then you should use `service` instead of `url`.
The service namespace and name are required. The port is optional and defaults to 443.
The path is optional and defaults to "/".

Here is an example of a webhook that is configured to call a service on port "1234"
at the subpath "/my-path", and to verify the TLS connection against the ServerName
`my-service-name.my-service-namespace.svc` using a custom CA bundle.

{{< tabs name="CustomResourceDefinition_versioning_example_4" >}}
{{% tab name="apiextensions.k8s.io/v1" %}}
```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
...
spec:
  ...
  conversion:
    strategy: Webhook
    webhook:
      clientConfig:
        service:
          namespace: my-service-namespace
          name: my-service-name
          path: /my-path
          port: 1234
        caBundle: "Ci0tLS0tQk...<base64-encoded PEM bundle>...tLS0K"
...
```
{{% /tab %}}
{{% tab name="apiextensions.k8s.io/v1beta1" %}}
```yaml
# Deprecated in v1.16 in favor of apiextensions.k8s.io/v1
apiVersion: apiextensions.k8s.io/v1beta1
kind: CustomResourceDefinition
...
spec:
  ...
  conversion:
    strategy: Webhook
    webhookClientConfig:
      service:
        namespace: my-service-namespace
        name: my-service-name
        path: /my-path
        port: 1234
      caBundle: "Ci0tLS0tQk...<base64-encoded PEM bundle>...tLS0K"
...
```
{{% /tab %}}
{{< /tabs >}}

## Webhook request and response

### Request

Webhooks are sent a POST request, with `Content-Type: application/json`,
with a `ConversionReview` API object in the `apiextensions.k8s.io` API group
serialized to JSON as the body.

Webhooks can specify what versions of `ConversionReview` objects they accept
with the `conversionReviewVersions` field in their CustomResourceDefinition:

{{< tabs name="conversionReviewVersions" >}}
{{% tab name="apiextensions.k8s.io/v1" %}}
```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
...
spec:
  ...
  conversion:
    strategy: Webhook
    webhook:
      conversionReviewVersions: ["v1", "v1beta1"]
      ...
```

`conversionReviewVersions` is a required field when creating 
`apiextensions.k8s.io/v1` custom resource definitions.
Webhooks are required to support at least one `ConversionReview`
version understood by the current and previous API server.
{{% /tab %}}
{{% tab name="apiextensions.k8s.io/v1beta1" %}}
```yaml
# Deprecated in v1.16 in favor of apiextensions.k8s.io/v1
apiVersion: apiextensions.k8s.io/v1beta1
kind: CustomResourceDefinition
...
spec:
  ...
  conversion:
    strategy: Webhook
    conversionReviewVersions: ["v1", "v1beta1"]
    ...
```

If no `conversionReviewVersions` are specified, the default when creating 
`apiextensions.k8s.io/v1beta1` custom resource definitions is `v1beta1`.
{{% /tab %}}
{{< /tabs >}}

API servers send the first `ConversionReview` version in the `conversionReviewVersions` list they support.
If none of the versions in the list are supported by the API server, the custom resource definition will not be allowed to be created.
If an API server encounters a conversion webhook configuration that was previously created and does not support any of the `ConversionReview`
versions the API server knows how to send, attempts to call to the webhook will fail.

This example shows the data contained in an `ConversionReview` object
for a request to convert `CronTab` objects to `example.com/v1`:


{{< tabs name="ConversionReview_request" >}}
{{% tab name="apiextensions.k8s.io/v1" %}}
```yaml
{
  "apiVersion": "apiextensions.k8s.io/v1",
  "kind": "ConversionReview",
  "request": {
    # Random uid uniquely identifying this conversion call
    "uid": "705ab4f5-6393-11e8-b7cc-42010a800002",
    
    # The API group and version the objects should be converted to
    "desiredAPIVersion": "example.com/v1",
    
    # The list of objects to convert.
    # May contain one or more objects, in one or more versions.
    "objects": [
      {
        "kind": "CronTab",
        "apiVersion": "example.com/v1beta1",
        "metadata": {
          "creationTimestamp": "2019-09-04T14:03:02Z",
          "name": "local-crontab",
          "namespace": "default",
          "resourceVersion": "143",
          "uid": "3415a7fc-162b-4300-b5da-fd6083580d66"
        },
        "hostPort": "localhost:1234"
      },
      {
        "kind": "CronTab",
        "apiVersion": "example.com/v1beta1",
        "metadata": {
          "creationTimestamp": "2019-09-03T13:02:01Z",
          "name": "remote-crontab",
          "resourceVersion": "12893",
          "uid": "359a83ec-b575-460d-b553-d859cedde8a0"
        },
        "hostPort": "example.com:2345"
      }
    ]
  }
}
```
{{% /tab %}}
{{% tab name="apiextensions.k8s.io/v1beta1" %}}
```yaml
{
  # Deprecated in v1.16 in favor of apiextensions.k8s.io/v1
  "apiVersion": "apiextensions.k8s.io/v1beta1",
  "kind": "ConversionReview",
  "request": {
    # Random uid uniquely identifying this conversion call
    "uid": "705ab4f5-6393-11e8-b7cc-42010a800002",
    
    # The API group and version the objects should be converted to
    "desiredAPIVersion": "example.com/v1",
    
    # The list of objects to convert.
    # May contain one or more objects, in one or more versions.
    "objects": [
      {
        "kind": "CronTab",
        "apiVersion": "example.com/v1beta1",
        "metadata": {
          "creationTimestamp": "2019-09-04T14:03:02Z",
          "name": "local-crontab",
          "namespace": "default",
          "resourceVersion": "143",
          "uid": "3415a7fc-162b-4300-b5da-fd6083580d66"
        },
        "hostPort": "localhost:1234"
      },
      {
        "kind": "CronTab",
        "apiVersion": "example.com/v1beta1",
        "metadata": {
          "creationTimestamp": "2019-09-03T13:02:01Z",
          "name": "remote-crontab",
          "resourceVersion": "12893",
          "uid": "359a83ec-b575-460d-b553-d859cedde8a0"
        },
        "hostPort": "example.com:2345"
      }
    ]
  }
}
```
{{% /tab %}}
{{< /tabs >}}

### Response

Webhooks respond with a 200 HTTP status code, `Content-Type: application/json`,
and a body containing a `ConversionReview` object (in the same version they were sent),
with the `response` stanza populated, serialized to JSON.

If conversion succeeds, a webhook should return a `response` stanza containing the following fields:
* `uid`, copied from the `request.uid` sent to the webhook
* `result`, set to `{"status":"Success"}`
* `convertedObjects`, containing all of the objects from `request.objects`, converted to `request.desiredVersion`

Example of a minimal successful response from a webhook:

{{< tabs name="ConversionReview_response_success" >}}
{{% tab name="apiextensions.k8s.io/v1" %}}
```yaml
{
  "apiVersion": "apiextensions.k8s.io/v1",
  "kind": "ConversionReview",
  "response": {
    # must match <request.uid>
    "uid": "705ab4f5-6393-11e8-b7cc-42010a800002",
    "result": {
      "status": "Success"
    },
    # Objects must match the order of request.objects, and have apiVersion set to <request.desiredAPIVersion>.
    # kind, metadata.uid, metadata.name, and metadata.namespace fields must not be changed by the webhook.
    # metadata.labels and metadata.annotations fields may be changed by the webhook.
    # All other changes to metadata fields by the webhook are ignored.
    "convertedObjects": [
      {
        "kind": "CronTab",
        "apiVersion": "example.com/v1",
        "metadata": {
          "creationTimestamp": "2019-09-04T14:03:02Z",
          "name": "local-crontab",
          "namespace": "default",
          "resourceVersion": "143",
          "uid": "3415a7fc-162b-4300-b5da-fd6083580d66"
        },
        "host": "localhost",
        "port": "1234"
      },
      {
        "kind": "CronTab",
        "apiVersion": "example.com/v1",
        "metadata": {
          "creationTimestamp": "2019-09-03T13:02:01Z",
          "name": "remote-crontab",
          "resourceVersion": "12893",
          "uid": "359a83ec-b575-460d-b553-d859cedde8a0"
        },
        "host": "example.com",
        "port": "2345"
      }
    ]
  }
}
```
{{% /tab %}}
{{% tab name="apiextensions.k8s.io/v1beta1" %}}
```yaml
{
  # Deprecated in v1.16 in favor of apiextensions.k8s.io/v1
  "apiVersion": "apiextensions.k8s.io/v1beta1",
  "kind": "ConversionReview",
  "response": {
    # must match <request.uid>
    "uid": "705ab4f5-6393-11e8-b7cc-42010a800002",
    "result": {
      "status": "Failed"
    },
    # Objects must match the order of request.objects, and have apiVersion set to <request.desiredAPIVersion>.
    # kind, metadata.uid, metadata.name, and metadata.namespace fields must not be changed by the webhook.
    # metadata.labels and metadata.annotations fields may be changed by the webhook.
    # All other changes to metadata fields by the webhook are ignored.
    "convertedObjects": [
      {
        "kind": "CronTab",
        "apiVersion": "example.com/v1",
        "metadata": {
          "creationTimestamp": "2019-09-04T14:03:02Z",
          "name": "local-crontab",
          "namespace": "default",
          "resourceVersion": "143",
          "uid": "3415a7fc-162b-4300-b5da-fd6083580d66"
        },
        "host": "localhost",
        "port": "1234"
      },
      {
        "kind": "CronTab",
        "apiVersion": "example.com/v1",
        "metadata": {
          "creationTimestamp": "2019-09-03T13:02:01Z",
          "name": "remote-crontab",
          "resourceVersion": "12893",
          "uid": "359a83ec-b575-460d-b553-d859cedde8a0"
        },
        "host": "example.com",
        "port": "2345"
      }
    ]
  }
}
```
{{% /tab %}}
{{< /tabs >}}

If conversion fails, a webhook should return a `response` stanza containing the following fields:
* `uid`, copied from the `request.uid` sent to the webhook
* `result`, set to `{"status":"Failed"}`

{{< warning >}}
Failing conversion can disrupt read and write access to the custom resources,
including the ability to update or delete the resources. Conversion failures 
should be avoided whenever possible, and should not be used to enforce validation
 constraints (use validation schemas or webhook admission instead).
{{< /warning >}}

Example of a response from a webhook indicating a conversion request failed, with an optional message:
{{< tabs name="ConversionReview_response_failure" >}}
{{% tab name="apiextensions.k8s.io/v1" %}}
```yaml
{
  "apiVersion": "apiextensions.k8s.io/v1",
  "kind": "ConversionReview",
  "response": {
    "uid": "<value from request.uid>",
    "result": {
      "status": "Failed",
      "message": "hostPort could not be parsed into a separate host and port"
    }
  }
}
```
{{% /tab %}}
{{% tab name="apiextensions.k8s.io/v1beta1" %}}
```yaml
{
  # Deprecated in v1.16 in favor of apiextensions.k8s.io/v1
  "apiVersion": "apiextensions.k8s.io/v1beta1",
  "kind": "ConversionReview",
  "response": {
    "uid": "<value from request.uid>",
    "result": {
      "status": "Failed",
      "message": "hostPort could not be parsed into a separate host and port"
    }
  }
}
```
{{% /tab %}}
{{< /tabs >}}

## Writing, reading, and updating versioned CustomResourceDefinition objects

When an object is written, it is persisted at the version designated as the
storage version at the time of the write. If the storage version changes,
existing objects are never converted automatically. However, newly-created
or updated objects are written at the new storage version. It is possible for an
object to have been written at a version that is no longer served.

When you read an object, you specify the version as part of the path. If you
specify a version that is different from the object's persisted version,
Kubernetes returns the object to you at the version you requested, but the
persisted object is neither changed on disk, nor converted in any way
(other than changing the `apiVersion` string) while serving the request.
You can request an object at any version that is currently served.

If you update an existing object, it is rewritten at the version that is
currently the storage version. This is the only way that objects can change from
one version to another.

To illustrate this, consider the following hypothetical series of events:

1.  The storage version is `v1beta1`. You create an object. It is persisted in
    storage at version `v1beta1`
2.  You add version `v1` to your CustomResourceDefinition and designate it as
    the storage version.
3.  You read your object at version `v1beta1`, then you read the object again at
    version `v1`. Both returned objects are identical except for the apiVersion
    field.
4.  You create a new object. It is persisted in storage at version `v1`. You now
    have two objects, one of which is at `v1beta1`, and the other of which is at
    `v1`.
5.  You update the first object. It is now persisted at version `v1` since that
    is the current storage version.

### Previous storage versions

The API server records each version which has ever been marked as the storage
version in the status field `storedVersions`. Objects may have been persisted
at any version that has ever been designated as a storage version. No objects
can exist in storage at a version that has never been a storage version.

## Upgrade existing objects to a new stored version

When deprecating versions and dropping support, select a storage upgrade
procedure. 

*Option 1:* Use the Storage Version Migrator

1. Run the [storage Version migrator](https://github.com/kubernetes-sigs/kube-storage-version-migrator)
2. Remove the old version from the CustomResourceDefinition `status.storedVersions` field.

*Option 2:* Manually upgrade the existing objects to a new stored version

The following is an example procedure to upgrade from `v1beta1` to `v1`.

1.  Set `v1` as the storage in the CustomResourceDefinition file and apply it
    using kubectl. The `storedVersions` is now `v1beta1, v1`.
2.  Write an upgrade procedure to list all existing objects and write them with
    the same content. This forces the backend to write objects in the current
    storage version, which is `v1`.
2. Remove `v1beta1` from the CustomResourceDefinition `status.storedVersions` field.


