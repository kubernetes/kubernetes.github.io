---
api_metadata:
  apiVersion: "authentication.k8s.io/v1"
  import: "k8s.io/api/authentication/v1"
  kind: "TokenRequest"
content_type: "api_reference"
description: "TokenRequest requests a token for a given service account."
title: "TokenRequest"
weight: 2
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


## TokenRequest {#TokenRequest}

TokenRequest requests a token for a given service account.

<hr>

- **apiVersion**: authentication.k8s.io/v1


- **kind**: TokenRequest


- **metadata** (<a href="{{< ref "../common-definitions/object-meta#ObjectMeta" >}}">ObjectMeta</a>)

  Standard object's metadata. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

- **spec** (<a href="{{< ref "../authentication-resources/token-request-v1#TokenRequestSpec" >}}">TokenRequestSpec</a>), required

  Spec holds information about the request being evaluated

- **status** (<a href="{{< ref "../authentication-resources/token-request-v1#TokenRequestStatus" >}}">TokenRequestStatus</a>)

  Status is filled in by the server and indicates whether the token can be authenticated.





## TokenRequestSpec {#TokenRequestSpec}

TokenRequestSpec contains client provided parameters of a token request.

<hr>

- **audiences** ([]string), required

  Audiences are the intendend audiences of the token. A recipient of a token must identitfy themself with an identifier in the list of audiences of the token, and otherwise should reject the token. A token issued for multiple audiences may be used to authenticate against any of the audiences listed but implies a high degree of trust between the target audiences.

- **boundObjectRef** (BoundObjectReference)

  BoundObjectRef is a reference to an object that the token will be bound to. The token will only be valid for as long as the bound object exists. NOTE: The API server's TokenReview endpoint will validate the BoundObjectRef, but other audiences may not. Keep ExpirationSeconds small if you want prompt revocation.

  <a name="BoundObjectReference"></a>
  *BoundObjectReference is a reference to an object that a token is bound to.*

  - **boundObjectRef.apiVersion** (string)

    API version of the referent.

  - **boundObjectRef.kind** (string)

    Kind of the referent. Valid kinds are 'Pod' and 'Secret'.

  - **boundObjectRef.name** (string)

    Name of the referent.

  - **boundObjectRef.uid** (string)

    UID of the referent.

- **expirationSeconds** (int64)

  ExpirationSeconds is the requested duration of validity of the request. The token issuer may return a token with a different validity duration so a client needs to check the 'expiration' field in a response.





## TokenRequestStatus {#TokenRequestStatus}

TokenRequestStatus is the result of a token request.

<hr>

- **expirationTimestamp** (Time), required

  ExpirationTimestamp is the time of expiration of the returned token.

  <a name="Time"></a>
  *Time is a wrapper around time.Time which supports correct marshaling to YAML and JSON.  Wrappers are provided for many of the factory methods that the time package offers.*

- **token** (string), required

  Token is the opaque bearer token.





## Operations {#Operations}



<hr>






### `create` create token of a ServiceAccount

#### HTTP Request

POST /api/v1/namespaces/{namespace}/serviceaccounts/{name}/token

#### Parameters


- **name** (*in path*): string, required

  name of the TokenRequest


- **namespace** (*in path*): string, required

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>


- **body**: <a href="{{< ref "../authentication-resources/token-request-v1#TokenRequest" >}}">TokenRequest</a>, required

  


- **dryRun** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>


- **fieldManager** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>


- **pretty** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>



#### Response


200 (<a href="{{< ref "../authentication-resources/token-request-v1#TokenRequest" >}}">TokenRequest</a>): OK

201 (<a href="{{< ref "../authentication-resources/token-request-v1#TokenRequest" >}}">TokenRequest</a>): Created

202 (<a href="{{< ref "../authentication-resources/token-request-v1#TokenRequest" >}}">TokenRequest</a>): Accepted

401: Unauthorized

