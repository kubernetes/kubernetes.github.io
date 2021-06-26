---
api_metadata:
  apiVersion: "authentication.k8s.io/v1"
  import: "k8s.io/api/authentication/v1"
  kind: "TokenReview"
content_type: "api_reference"
description: "TokenReview attempts to authenticate a token to a known user."
title: "TokenReview"
weight: 3
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

`apiVersion: authentication.k8s.io/v1`

`import "k8s.io/api/authentication/v1"`


## TokenReview {#TokenReview}

TokenReview attempts to authenticate a token to a known user. Note: TokenReview requests may be cached by the webhook token authenticator plugin in the kube-apiserver.

<hr>

- **apiVersion**: authentication.k8s.io/v1


- **kind**: TokenReview


- **metadata** (<a href="{{< ref "../common-definitions/object-meta#ObjectMeta" >}}">ObjectMeta</a>)

  Standard object's metadata. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

- **spec** (<a href="{{< ref "../authentication-resources/token-review-v1#TokenReviewSpec" >}}">TokenReviewSpec</a>), required

  Spec holds information about the request being evaluated

- **status** (<a href="{{< ref "../authentication-resources/token-review-v1#TokenReviewStatus" >}}">TokenReviewStatus</a>)

  Status is filled in by the server and indicates whether the request can be authenticated.





## TokenReviewSpec {#TokenReviewSpec}

TokenReviewSpec is a description of the token authentication request.

<hr>

- **audiences** ([]string)

  Audiences is a list of the identifiers that the resource server presented with the token identifies as. Audience-aware token authenticators will verify that the token was intended for at least one of the audiences in this list. If no audiences are provided, the audience will default to the audience of the Kubernetes apiserver.

- **token** (string)

  Token is the opaque bearer token.





## TokenReviewStatus {#TokenReviewStatus}

TokenReviewStatus is the result of the token authentication request.

<hr>

- **audiences** ([]string)

  Audiences are audience identifiers chosen by the authenticator that are compatible with both the TokenReview and token. An identifier is any identifier in the intersection of the TokenReviewSpec audiences and the token's audiences. A client of the TokenReview API that sets the spec.audiences field should validate that a compatible audience identifier is returned in the status.audiences field to ensure that the TokenReview server is audience aware. If a TokenReview returns an empty status.audience field where status.authenticated is "true", the token is valid against the audience of the Kubernetes API server.

- **authenticated** (boolean)

  Authenticated indicates that the token was associated with a known user.

- **error** (string)

  Error indicates that the token couldn't be checked

- **user** (UserInfo)

  User is the UserInfo associated with the provided token.

  <a name="UserInfo"></a>
  *UserInfo holds the information about the user needed to implement the user.Info interface.*

  - **user.extra** (map[string][]string)

    Any additional information provided by the authenticator.

  - **user.groups** ([]string)

    The names of groups this user is a part of.

  - **user.uid** (string)

    A unique value that identifies this user across time. If this user is deleted and another user by the same name is added, they will have different UIDs.

  - **user.username** (string)

    The name that uniquely identifies this user among all active users.





## Operations {#Operations}



<hr>






### `create` create a TokenReview

#### HTTP Request

POST /apis/authentication.k8s.io/v1/tokenreviews

#### Parameters


- **body**: <a href="{{< ref "../authentication-resources/token-review-v1#TokenReview" >}}">TokenReview</a>, required

  


- **dryRun** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>


- **fieldManager** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>


- **pretty** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>



#### Response


200 (<a href="{{< ref "../authentication-resources/token-review-v1#TokenReview" >}}">TokenReview</a>): OK

201 (<a href="{{< ref "../authentication-resources/token-review-v1#TokenReview" >}}">TokenReview</a>): Created

202 (<a href="{{< ref "../authentication-resources/token-review-v1#TokenReview" >}}">TokenReview</a>): Accepted

401: Unauthorized

