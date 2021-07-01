---
reviewers:
  - bprashanth
  - davidopp
  - lavalamp
  - liggitt
title: Managing Service Accounts
content_type: concept
weight: 50
---

<!-- overview -->

This is a Cluster Administrator guide to service accounts. You should be familiar with
[configuring Kubernetes service accounts](/docs/tasks/configure-pod-container/configure-service-account/).

Support for authorization and user accounts is planned but incomplete. Sometimes
incomplete features are referred to in order to better describe service accounts.

<!-- body -->

## User accounts versus service accounts

Kubernetes distinguishes between the concept of a user account and a service account
for a number of reasons:

- User accounts are for humans. Service accounts are for processes, which run
  in pods.
- User accounts are intended to be global. Names must be unique across all
  namespaces of a cluster. Service accounts are namespaced.
- Typically, a cluster's user accounts might be synced from a corporate
  database, where new user account creation requires special privileges and is
  tied to complex business processes. Service account creation is intended to be
  more lightweight, allowing cluster users to create service accounts for
  specific tasks by following the principle of least privilege.
- Auditing considerations for humans and service accounts may differ.
- A config bundle for a complex system may include definition of various service
  accounts for components of that system. Because service accounts can be created
  without many constraints and have namespaced names, such config is portable.

## Service account automation

Three separate components cooperate to implement the automation around service accounts:

- A `ServiceAccount` admission controller
- A Token controller
- A `ServiceAccount` controller

### ServiceAccount Admission Controller

The modification of pods is implemented via a plugin
called an [Admission Controller](/docs/reference/access-authn-authz/admission-controllers/).
It is part of the API server.
It acts synchronously to modify pods as they are created or updated. When this plugin is active
(and it is by default on most distributions), then it does the following when a pod is created or modified:

1. If the pod does not have a `ServiceAccount` set, it sets the `ServiceAccount` to `default`.
1. It ensures that the `ServiceAccount` referenced by the pod exists, and otherwise rejects it.
1. It adds a `volume` to the pod which contains a token for API access if neither the ServiceAccount `automountServiceAccountToken` nor the Pod's `automountServiceAccountToken` is set to `false`.
1. It adds a `volumeSource` to each container of the pod mounted at `/var/run/secrets/kubernetes.io/serviceaccount`, if the previous step has created a volume for ServiceAccount token.
1. If the pod does not contain any `imagePullSecrets`, then `imagePullSecrets` of the `ServiceAccount` are added to the pod.

#### Bound Service Account Token Volume

{{< feature-state for_k8s_version="v1.22" state="stable" >}}

The ServiceAccount admission controller will add the following projected volume instead of a Secret-based volume for the non-expiring service account token created by Token Controller.

```yaml
- name: kube-api-access-<random-suffix>
  projected:
    defaultMode: 420 # 0644
    sources:
      - serviceAccountToken:
          expirationSeconds: 3600
          path: token
      - configMap:
          items:
            - key: ca.crt
              path: ca.crt
          name: kube-root-ca.crt
      - downwardAPI:
          items:
            - fieldRef:
                apiVersion: v1
                fieldPath: metadata.namespace
              path: namespace
```

This projected volume consists of three sources:

1. A ServiceAccountToken acquired from kube-apiserver via TokenRequest API. It will expire after 1 hour by default or when the pod is deleted. It is bound to the pod and has kube-apiserver as the audience.
1. A ConfigMap containing a CA bundle used for verifying connections to the kube-apiserver. This feature depends on the `RootCAConfigMap` feature gate, which publishes a "kube-root-ca.crt" ConfigMap to every namespace. `RootCAConfigMap` feature gate is graduated to GA in 1.21 and default to true. (This flag will be removed from --feature-gate arg in 1.22)
1. A DownwardAPI that references the namespace of the pod.

See more details about [projected volumes](/docs/tasks/configure-pod-container/configure-projected-volume-storage/).

### Token Controller

TokenController runs as part of `kube-controller-manager`. It acts asynchronously. It:

- watches ServiceAccount creation and creates a corresponding
  ServiceAccount token Secret to allow API access.
- watches ServiceAccount deletion and deletes all corresponding ServiceAccount
  token Secrets.
- watches ServiceAccount token Secret addition, and ensures the referenced
  ServiceAccount exists, and adds a token to the Secret if needed.
- watches Secret deletion and removes a reference from the corresponding
  ServiceAccount if needed.

You must pass a service account private key file to the token controller in
the `kube-controller-manager` using the `--service-account-private-key-file`
flag. The private key is used to sign generated service account tokens.
Similarly, you must pass the corresponding public key to the `kube-apiserver`
using the `--service-account-key-file` flag. The public key will be used to
verify the tokens during authentication.

#### To create additional API tokens

A controller loop ensures a Secret with an API token exists for each
ServiceAccount. To create additional API tokens for a ServiceAccount, create a
Secret of type `kubernetes.io/service-account-token` with an annotation
referencing the ServiceAccount, and the controller will update it with a
generated token:

Below is a sample configuration for such a Secret:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: mysecretname
  annotations:
    kubernetes.io/service-account.name: myserviceaccount
type: kubernetes.io/service-account-token
```

```shell
kubectl create -f ./secret.yaml
kubectl describe secret mysecretname
```

#### To delete/invalidate a ServiceAccount token Secret

```shell
kubectl delete secret mysecretname
```

### ServiceAccount controller

A ServiceAccount controller manages the ServiceAccounts inside namespaces, and
ensures a ServiceAccount named "default" exists in every active namespace.
