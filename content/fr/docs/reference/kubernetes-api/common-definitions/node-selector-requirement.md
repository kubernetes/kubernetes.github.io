---
api_metadata:
  apiVersion: ""
  import: "k8s.io/api/core/v1"
  kind: "NodeSelectorRequirement"
content_type: "api_reference"
description: "A node selector requirement is a selector that contains values, a key, and an operator that relates the key and values."
title: "NodeSelectorRequirement"
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



`import "k8s.io/api/core/v1"`


A node selector requirement is a selector that contains values, a key, and an operator that relates the key and values.

<hr>

- **key** (string), requis

  The label key that the selector applies to.

- **operator** (string), requis

  Represents a key's relationship to a set of values. Valid operators are In, NotIn, Exists, DoesNotExist. Gt, and Lt.

- **values** ([]string)

  An array of string values. If the operator is In or NotIn, the values array must be non-empty. If the operator is Exists or DoesNotExist, the values array must be empty. If the operator is Gt or Lt, the values array must have a single element, which will be interpreted as an integer. This array is replaced during a strategic merge patch.





