---
api_metadata:
  apiVersion: ""
  import: "k8s.io/apimachinery/pkg/apis/meta/v1"
  kind: "Status"
content_type: "api_reference"
description: "Status is a return value for calls that don't return other objects."
title: "Status"
weight: 12
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



`import "k8s.io/apimachinery/pkg/apis/meta/v1"`


Status is a return value for calls that don't return other objects.

<hr>

- **apiVersion** (string)

  APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources

- **code** (int32)

  Suggested HTTP return code for this status, 0 if not set.

- **details** (StatusDetails)

  Extended data associated with the reason.  Each reason may define its own extended details. This field is optional and the data returned is not guaranteed to conform to any schema except that defined by the reason type.

  <a name="StatusDetails"></a>
  *StatusDetails is a set of additional properties that MAY be set by the server to provide additional information about a response. The Reason field of a Status object defines what attributes will be set. Clients must ignore fields that do not match the defined type of each attribute, and should assume that any attribute may be empty, invalid, or under defined.*

  - **details.causes** ([]StatusCause)

    The Causes array includes more details associated with the StatusReason failure. Not all StatusReasons may provide detailed causes.

    <a name="StatusCause"></a>
    *StatusCause provides more information about an api.Status failure, including cases when multiple errors are encountered.*

    - **details.causes.field** (string)

      The field of the resource that has caused this error, as named by its JSON serialization. May include dot and postfix notation for nested attributes. Arrays are zero-indexed.  Fields may appear more than once in an array of causes due to fields having multiple errors. Optional.Examples:  "name" - the field "name" on the current resource  "items[0].name" - the field "name" on the first array entry in "items"

    - **details.causes.message** (string)

      A human-readable description of the cause of the error.  This field may be presented as-is to a reader.

    - **details.causes.reason** (string)

      A machine-readable description of the cause of the error. If this value is empty there is no information available.

  - **details.group** (string)

    The group attribute of the resource associated with the status StatusReason.

  - **details.kind** (string)

    The kind attribute of the resource associated with the status StatusReason. On some operations may differ from the requested resource Kind. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds

  - **details.name** (string)

    The name attribute of the resource associated with the status StatusReason (when there is a single name which can be described).

  - **details.retryAfterSeconds** (int32)

    If specified, the time in seconds before the operation should be retried. Some errors may indicate the client must take an alternate action - for those errors this field may indicate how long to wait before taking the alternate action.

  - **details.uid** (string)

    UID of the resource. (when there is a single resource which can be described). More info: http://kubernetes.io/docs/user-guide/identifiers#uids

- **kind** (string)

  Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds

- **message** (string)

  A human-readable description of the status of this operation.

- **metadata** (<a href="{{< ref "../common-definitions/list-meta#ListMeta" >}}">ListMeta</a>)

  Standard list metadata. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds

- **reason** (string)

  A machine-readable description of why this operation is in the "Failure" status. If this value is empty there is no information available. A Reason clarifies an HTTP status code but does not override it.

- **status** (string)

  Status of the operation. One of: "Success" or "Failure". More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status





