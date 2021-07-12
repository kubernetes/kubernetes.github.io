---
reviewers:
- bprashanth
- liggitt
- thockin
title: Configure Service Accounts for Pods
content_type: task
weight: 90
---

<!-- overview -->
A service account provides an identity for processes that run in a Pod.

{{< note >}}
This document is a user introduction to Service Accounts and describes how service accounts behave in a cluster set up
as recommended by the Kubernetes project. Your cluster administrator may have
customized the behavior in your cluster, in which case this documentation may
not apply.
{{< /note >}}

When you (a human) access the cluster (for example, using `kubectl`), you are
authenticated by the apiserver as a particular User Account (currently this is
usually `admin`, unless your cluster administrator has customized your cluster). Processes in containers inside pods can also contact the apiserver.
When they do, they are authenticated as a particular Service Account (for example, `default`).

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}

<!-- steps -->

## Use the Default Service Account to access the API server.

When you create a pod, if you do not specify a service account, it is
automatically assigned the `default` service account in the same namespace.
If you get the raw json or yaml for a pod you have created (for example, `kubectl get pods/<podname> -o yaml`),
you can see the `spec.serviceAccountName` field has been
[automatically set](/docs/concepts/overview/working-with-objects/object-management/).

You can access the API from inside a pod using automatically mounted service account credentials, as described in
[Accessing the Cluster](/docs/tasks/access-application-cluster/access-cluster).
The API permissions of the service account depend on the
[authorization plugin and policy](/docs/reference/access-authn-authz/authorization/#authorization-modules) in use.

In version 1.6+, you can opt out of automounting API credentials for a service account by setting `automountServiceAccountToken: false` on the service account:

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: build-robot
automountServiceAccountToken: false
...
```

In version 1.6+, you can also opt out of automounting API credentials for a particular pod:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  serviceAccountName: build-robot
  automountServiceAccountToken: false
  ...
```

The pod spec takes precedence over the service account if both specify a `automountServiceAccountToken` value.

## Use Multiple Service Accounts.

Every namespace has a default service account resource called `default`.
You can list this and any other serviceAccount resources in the namespace with this command:

```shell
kubectl get serviceaccounts
```

The output is similar to this:

```
NAME      SECRETS    AGE
default   1          1d
```

You can create additional ServiceAccount objects like this:

```shell
kubectl apply -f - <<EOF
apiVersion: v1
kind: ServiceAccount
metadata:
  name: build-robot
EOF
```

The name of a ServiceAccount object must be a valid
[DNS subdomain name](/docs/concepts/overview/working-with-objects/names#dns-subdomain-names).

If you get a complete dump of the service account object, like this:

```shell
kubectl get serviceaccounts/build-robot -o yaml
```

The output is similar to this:

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  creationTimestamp: 2015-06-16T00:12:59Z
  name: build-robot
  namespace: default
  resourceVersion: "272500"
  uid: 721ab723-13bc-11e5-aec2-42010af0021e
secrets:
- name: build-robot-token-bvbk5
```

then you will see that a token has automatically been created and is referenced by the service account.

You may use authorization plugins to [set permissions on service accounts](/docs/reference/access-authn-authz/rbac/#service-account-permissions).

To use a non-default service account, set the `spec.serviceAccountName`
field of a pod to the name of the service account you wish to use.

The service account has to exist at the time the pod is created, or it will be rejected.

You cannot update the service account of an already created pod.

You can clean up the service account from this example like this:

```shell
kubectl delete serviceaccount/build-robot
```

## Manually create a service account API token.

Suppose we have an existing service account named "build-robot" as mentioned above, and we create
a new secret manually.

```shell
kubectl apply -f - <<EOF
apiVersion: v1
kind: Secret
metadata:
  name: build-robot-secret
  annotations:
    kubernetes.io/service-account.name: build-robot
type: kubernetes.io/service-account-token
EOF
```

Now you can confirm that the newly built secret is populated with an API token for the "build-robot" service account.

Any tokens for non-existent service accounts will be cleaned up by the token controller.

```shell
kubectl describe secrets/build-robot-secret
```

The output is similar to this:

```
Name:           build-robot-secret
Namespace:      default
Labels:         <none>
Annotations:    kubernetes.io/service-account.name: build-robot
                kubernetes.io/service-account.uid: da68f9c6-9d26-11e7-b84e-002dc52800da

Type:   kubernetes.io/service-account-token

Data
====
ca.crt:         1338 bytes
namespace:      7 bytes
token:          ...
```

{{< note >}}
The content of `token` is elided here.
{{< /note >}}

## Add ImagePullSecrets to a service account

### Create an imagePullSecret

- Create an imagePullSecret, as described in [Specifying ImagePullSecrets on a Pod](/docs/concepts/containers/images/#specifying-imagepullsecrets-on-a-pod).

    ```shell
    kubectl create secret docker-registry myregistrykey --docker-server=DUMMY_SERVER \
            --docker-username=DUMMY_USERNAME --docker-password=DUMMY_DOCKER_PASSWORD \
            --docker-email=DUMMY_DOCKER_EMAIL
    ```

- Verify it has been created.
   ```shell
   kubectl get secrets myregistrykey
   ```

    The output is similar to this:

    ```
    NAME             TYPE                              DATA    AGE
    myregistrykey    kubernetes.io/.dockerconfigjson   1       1d
    ```

### Add image pull secret to service account

Next, modify the default service account for the namespace to use this secret as an imagePullSecret.


```shell
kubectl patch serviceaccount default -p '{"imagePullSecrets": [{"name": "myregistrykey"}]}'
```

You can instead use `kubectl edit`, or manually edit the YAML manifests as shown below:

```shell
kubectl get serviceaccounts default -o yaml > ./sa.yaml
```

The output of the `sa.yaml` file is similar to this:

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  creationTimestamp: 2015-08-07T22:02:39Z
  name: default
  namespace: default
  resourceVersion: "243024"
  uid: 052fb0f4-3d50-11e5-b066-42010af0d7b6
secrets:
- name: default-token-uudge
```

Using your editor of choice (for example `vi`), open the `sa.yaml` file, delete line with key `resourceVersion`, add lines with `imagePullSecrets:` and save.

The output of the `sa.yaml` file is similar to this:

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  creationTimestamp: 2015-08-07T22:02:39Z
  name: default
  namespace: default
  uid: 052fb0f4-3d50-11e5-b066-42010af0d7b6
secrets:
- name: default-token-uudge
imagePullSecrets:
- name: myregistrykey
```

Finally replace the serviceaccount with the new updated `sa.yaml` file

```shell
kubectl replace serviceaccount default -f ./sa.yaml
```

### Verify imagePullSecrets was added to pod spec

Now, when a new Pod is created in the current namespace and using the default ServiceAccount, the new Pod has its  `spec.imagePullSecrets` field set automatically:

```shell
kubectl run nginx --image=nginx --restart=Never
kubectl get pod nginx -o=jsonpath='{.spec.imagePullSecrets[0].name}{"\n"}'
```

The output is:

```
myregistrykey
```

<!--## Adding Secrets to a service account.

TODO: Test and explain how to use additional non-K8s secrets with an existing service account.
-->

## Service Account Token Volume Projection

{{< feature-state for_k8s_version="v1.20" state="stable" >}}

{{< note >}}
To enable and use token request projection, you must specify each of the following
command line arguments to `kube-apiserver`:

* `--service-account-issuer`
* `--service-account-key-file`
* `--service-account-signing-key-file`
* `--api-audiences`

{{< /note >}}

The kubelet can also project a service account token into a Pod. You can
specify desired properties of the token, such as the audience and the validity
duration. These properties are not configurable on the default service account
token. The service account token will also become invalid against the API when
the Pod or the ServiceAccount is deleted.

This behavior is configured on a PodSpec using a ProjectedVolume type called
[ServiceAccountToken](/docs/concepts/storage/volumes/#projected). To provide a
pod with a token with an audience of "vault" and a validity duration of two
hours, you would configure the following in your PodSpec:

{{< codenew file="pods/pod-projected-svc-token.yaml" >}}

Create the Pod:

```shell
kubectl create -f https://k8s.io/examples/pods/pod-projected-svc-token.yaml
```

The kubelet will request and store the token on behalf of the pod, make the
token available to the pod at a configurable file path, and refresh the token as it approaches expiration.
The kubelet proactively rotates the token if it is older than 80% of its total TTL, or if the token is older than 24 hours.

The application is responsible for reloading the token when it rotates. Periodic reloading (e.g. once every 5 minutes) is sufficient for most use cases.

## Service Account Issuer Discovery

{{< feature-state for_k8s_version="v1.21" state="stable" >}}

The Service Account Issuer Discovery feature is enabled when the Service Account
Token Projection feature is enabled, as described
[above](#service-account-token-volume-projection).

{{< note >}}
The issuer URL must comply with the
[OIDC Discovery Spec](https://openid.net/specs/openid-connect-discovery-1_0.html). In
practice, this means it must use the `https` scheme, and should serve an OpenID
provider configuration at `{service-account-issuer}/.well-known/openid-configuration`.

If the URL does not comply, the `ServiceAccountIssuerDiscovery` endpoints will
not be registered, even if the feature is enabled.
{{< /note >}}

The Service Account Issuer Discovery feature enables federation of Kubernetes
service account tokens issued by a cluster (the _identity provider_) with
external systems (_relying parties_).

When enabled, the Kubernetes API server provides an OpenID Provider
Configuration document at `/.well-known/openid-configuration` and the associated
JSON Web Key Set (JWKS) at `/openid/v1/jwks`. The OpenID Provider Configuration
is sometimes referred to as the _discovery document_.

Clusters include a default RBAC ClusterRole called
`system:service-account-issuer-discovery`. No role bindings are provided
by default. Administrators may, for example, choose whether to bind the role to
`system:authenticated` or `system:unauthenticated` depending on their security
requirements and which external systems they intend to federate with.

{{< note >}}
The responses served at `/.well-known/openid-configuration` and
`/openid/v1/jwks` are designed to be OIDC compatible, but not strictly OIDC
compliant. Those documents contain only the parameters necessary to perform
validation of Kubernetes service account tokens.
{{< /note >}}

The JWKS response contains public keys that a relying party can use to validate
the Kubernetes service account tokens. Relying parties first query for the
OpenID Provider Configuration, and use the `jwks_uri` field in the response to
find the JWKS.

In many cases, Kubernetes API servers are not available on the public internet,
but public endpoints that serve cached responses from the API server can be made
available by users or service providers. In these cases, it is possible to
override the `jwks_uri` in the OpenID Provider Configuration so that it points
to the public endpoint, rather than the API server's address, by passing the
`--service-account-jwks-uri` flag to the API server. Like the issuer URL, the
JWKS URI is required to use the `https` scheme.


## {{% heading "whatsnext" %}}

See also:

- [Cluster Admin Guide to Service Accounts](/docs/reference/access-authn-authz/service-accounts-admin/)
- [Service Account Signing Key Retrieval KEP](https://github.com/kubernetes/enhancements/tree/master/keps/sig-auth/1393-oidc-discovery)
- [OIDC Discovery Spec](https://openid.net/specs/openid-connect-discovery-1_0.html)
