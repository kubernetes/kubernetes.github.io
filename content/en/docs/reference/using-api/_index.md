---
title: API Overview
reviewers:
- erictune
- lavalamp
- jbeda
content_type: concept
weight: 10
no_list: true
card:
  name: reference
  weight: 50
  title: Overview of API
---

<!-- overview -->

This section provides reference information for the Kubernetes API.

The REST API is the fundamental fabric of Kubernetes. All operations and
communications between components, and external user commands are REST API
calls that the API Server handles. Consequently, everything in the Kubernetes
platform is treated as an API object and has a corresponding entry in the
[API](/docs/reference/kubernetes-api/).

The [Kubernetes API reference](/docs/reference/kubernetes-api/)
lists the API for Kubernetes version {{< param "version" >}}.

For general background information, read
[The Kubernetes API](/docs/concepts/overview/kubernetes-api/).
[Controlling Access to the Kubernetes API](/docs/concepts/security/controlling-access/)
describes how clients can authenticate to the Kubernetes API server, and how their
requests are authorized.


## API versioning

The JSON and Protobuf serialization schemas follow the same guidelines for
schema changes. The following descriptions cover both formats.

The API versioning and software versioning are indirectly related.
The [API and release versioning proposal](https://git.k8s.io/community/contributors/design-proposals/release/versioning.md)
describes the relationship between API versioning and software versioning.

Different API versions indicate different levels of stability and support. You
can find more information about the criteria for each level in the
[API Changes documentation](https://git.k8s.io/community/contributors/devel/sig-architecture/api_changes.md#alpha-beta-and-stable-versions).

Here's a summary of each level:

- Alpha:
  - The version names contain `alpha` (for example, `v1alpha1`).
  - The software may contain bugs. Enabling a feature may expose bugs. A
    feature may be disabled by default.
  - The support for a feature may be dropped at any time without notice.
  - The API may change in incompatible ways in a later software release without notice.
  - The software is recommended for use only in short-lived testing clusters,
    due to increased risk of bugs and lack of long-term support.

- Beta:
  - The version names contain `beta` (for example, `v2beta3`).
  - The software is well tested. Enabling a feature is considered safe.
    Features are enabled by default.
  - The support for a feature will not be dropped, though the details may change.

  - The schema and/or semantics of objects may change in incompatible ways in
    a subsequent beta or stable release. When this happens, migration
    instructions are provided. Schema changes may require deleting, editing, and
    re-creating API objects. The editing process may not be straightforward.
    The migration may require downtime for applications that rely on the feature.
  - The software is not recommended for production uses. Subsequent releases
    may introduce incompatible changes. If you have multiple clusters which
    can be upgraded independently, you may be able to relax this restriction.

  {{< note >}}
  Please try beta features and provide feedback. After the features exit beta, it
  may not be practical to make more changes.
  {{< /note >}}

- Stable:
  - The version name is `vX` where `X` is an integer.
  - The stable versions of features appear in released software for many subsequent versions.

## API groups

[API groups](https://git.k8s.io/community/contributors/design-proposals/api-machinery/api-group.md)
make it easier to extend the Kubernetes API.
The API group is specified in a REST path and in the `apiVersion` field of a
serialized object.

There are several API groups in Kubernetes:

*  The *core* (also called *legacy*) group is found at REST path `/api/v1`.
   The core group is not specified as part of the `apiVersion` field, for
   example, `apiVersion: v1`.
*  The named groups are at REST path `/apis/$GROUP_NAME/$VERSION` and use
   `apiVersion: $GROUP_NAME/$VERSION` (for example, `apiVersion: batch/v1`).
   You can find the full list of supported API groups in
   [Kubernetes API reference](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#-strong-api-groups-strong-).

## Enabling or disabling API groups   {#enabling-or-disabling}

Certain resources and API groups are enabled by default. You can enable or
disable them by setting `--runtime-config` on the API server.  The
`--runtime-config` flag accepts comma separated `<key>[=<value>]` pairs
describing the runtime configuration of the API server. If the `=<value>`
part is omitted, it is treated as if `=true` is specified. For example:

 - to disable `batch/v1`, set `--runtime-config=batch/v1=false`
 - to enable `batch/v2alpha1`, set `--runtime-config=batch/v2alpha1`

{{< note >}}
When you enable or disable groups or resources, you need to restart the API
server and controller manager to pick up the `--runtime-config` changes.
{{< /note >}}

## Persistence

Kubernetes stores its serialized state in terms of the API resources by writing them into
{{< glossary_tooltip term_id="etcd" >}}.

## {{% heading "whatsnext" %}}

- Learn more about [API conventions](https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#api-conventions)
- Read the design documentation for
  [aggregator](https://github.com/kubernetes/community/blob/master/contributors/design-proposals/api-machinery/aggregated-api-servers.md)
