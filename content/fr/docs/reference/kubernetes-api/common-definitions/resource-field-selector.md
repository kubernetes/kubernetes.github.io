---
api_metadata:
  apiVersion: ""
  import: "k8s.io/api/core/v1"
  kind: "ResourceFieldSelector"
content_type: "api_reference"
description: "ResourceFieldSelector represents container resources (cpu, memory) and their output format."
title: "ResourceFieldSelector"
weight: 11
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


ResourceFieldSelector represents container resources (cpu, memory) and their output format

<hr>

- **resource** (string), requis

  Required: resource to select

- **containerName** (string)

  Container name: required for volumes, optional for env vars

- **divisor** (<a href="{{< ref "../common-definitions/quantity#Quantity" >}}">Quantity</a>)

  Specifies the output format of the exposed resources, defaults to "1"





