---
api_metadata:
  apiVersion: "authorization.k8s.io/v1"
  import: "k8s.io/api/authorization/v1"
  kind: "SelfSubjectRulesReview"
content_type: "api_reference"
description: "SelfSubjectRulesReview enumerates the set of actions the current user can perform within a namespace."
title: "SelfSubjectRulesReview"
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

`apiVersion: authorization.k8s.io/v1`

`import "k8s.io/api/authorization/v1"`


## SelfSubjectRulesReview {#SelfSubjectRulesReview}

SelfSubjectRulesReview enumerates the set of actions the current user can perform within a namespace. The returned list of actions may be incomplete depending on the server's authorization mode, and any errors experienced during the evaluation. SelfSubjectRulesReview should be used by UIs to show/hide actions, or to quickly let an end user reason about their permissions. It should NOT Be used by external systems to drive authorization decisions as this raises confused deputy, cache lifetime/revocation, and correctness concerns. SubjectAccessReview, and LocalAccessReview are the correct way to defer authorization decisions to the API server.

<hr>

- **apiVersion**: authorization.k8s.io/v1


- **kind**: SelfSubjectRulesReview


- **metadata** (<a href="{{< ref "../common-definitions/object-meta#ObjectMeta" >}}">ObjectMeta</a>)

  Standard list metadata. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

- **spec** (<a href="{{< ref "../authorization-resources/self-subject-rules-review-v1#SelfSubjectRulesReviewSpec" >}}">SelfSubjectRulesReviewSpec</a>), required

  Spec holds information about the request being evaluated.

- **status** (SubjectRulesReviewStatus)

  Status is filled in by the server and indicates the set of actions a user can perform.

  <a name="SubjectRulesReviewStatus"></a>
  *SubjectRulesReviewStatus contains the result of a rules check. This check can be incomplete depending on the set of authorizers the server is configured with and any errors experienced during evaluation. Because authorization rules are additive, if a rule appears in a list it's safe to assume the subject has that permission, even if that list is incomplete.*

  - **status.incomplete** (boolean), required

    Incomplete is true when the rules returned by this call are incomplete. This is most commonly encountered when an authorizer, such as an external authorizer, doesn't support rules evaluation.

  - **status.nonResourceRules** ([]NonResourceRule), required

    NonResourceRules is the list of actions the subject is allowed to perform on non-resources. The list ordering isn't significant, may contain duplicates, and possibly be incomplete.

    <a name="NonResourceRule"></a>
    *NonResourceRule holds information that describes a rule for the non-resource*

    - **status.nonResourceRules.verbs** ([]string), required

      Verb is a list of kubernetes non-resource API verbs, like: get, post, put, delete, patch, head, options.  "*" means all.

    - **status.nonResourceRules.nonResourceURLs** ([]string)

      NonResourceURLs is a set of partial urls that a user should have access to.  *s are allowed, but only as the full, final step in the path.  "*" means all.

  - **status.resourceRules** ([]ResourceRule), required

    ResourceRules is the list of actions the subject is allowed to perform on resources. The list ordering isn't significant, may contain duplicates, and possibly be incomplete.

    <a name="ResourceRule"></a>
    *ResourceRule is the list of actions the subject is allowed to perform on resources. The list ordering isn't significant, may contain duplicates, and possibly be incomplete.*

    - **status.resourceRules.verbs** ([]string), required

      Verb is a list of kubernetes resource API verbs, like: get, list, watch, create, update, delete, proxy.  "*" means all.

    - **status.resourceRules.apiGroups** ([]string)

      APIGroups is the name of the APIGroup that contains the resources.  If multiple API groups are specified, any action requested against one of the enumerated resources in any API group will be allowed.  "*" means all.

    - **status.resourceRules.resourceNames** ([]string)

      ResourceNames is an optional white list of names that the rule applies to.  An empty set means that everything is allowed.  "*" means all.

    - **status.resourceRules.resources** ([]string)

      Resources is a list of resources this rule applies to.  "*" means all in the specified apiGroups.
       "*/foo" represents the subresource 'foo' for all resources in the specified apiGroups.

  - **status.evaluationError** (string)

    EvaluationError can appear in combination with Rules. It indicates an error occurred during rule evaluation, such as an authorizer that doesn't support rule evaluation, and that ResourceRules and/or NonResourceRules may be incomplete.





## SelfSubjectRulesReviewSpec {#SelfSubjectRulesReviewSpec}

SelfSubjectRulesReviewSpec defines the specification for SelfSubjectRulesReview.

<hr>

- **namespace** (string)

  Namespace to evaluate rules for. Required.





## Operations {#Operations}



<hr>






### `create` create a SelfSubjectRulesReview

#### HTTP Request

POST /apis/authorization.k8s.io/v1/selfsubjectrulesreviews

#### Parameters


- **body**: <a href="{{< ref "../authorization-resources/self-subject-rules-review-v1#SelfSubjectRulesReview" >}}">SelfSubjectRulesReview</a>, required

  


- **dryRun** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>


- **fieldManager** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>


- **pretty** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>



#### Response


200 (<a href="{{< ref "../authorization-resources/self-subject-rules-review-v1#SelfSubjectRulesReview" >}}">SelfSubjectRulesReview</a>): OK

201 (<a href="{{< ref "../authorization-resources/self-subject-rules-review-v1#SelfSubjectRulesReview" >}}">SelfSubjectRulesReview</a>): Created

202 (<a href="{{< ref "../authorization-resources/self-subject-rules-review-v1#SelfSubjectRulesReview" >}}">SelfSubjectRulesReview</a>): Accepted

401: Unauthorized

