---
layout: blog
title: "Writing a Controller for Pod Labels"
date: 2021-06-21
slug: writing-a-controller-for-pod-labels
---

**Authors**: Arthur Busser (Padok)

[Operators][what-is-an-operator] are proving to be an excellent solution to
running stateful distributed applications in Kubernetes. Open source tools like
the [Operator SDK][operator-sdk] provide ways to build reliable and maintainable
operators, making it easier to extend Kubernetes and implement custom
scheduling.

Kubernetes operators run complex software inside your cluster. The open source
community has already built [many operators][operatorhub] for distributed
applications like Prometheus, Elasticsearch, or Argo CD. Even outside of
open source, operators can help to bring new functionality to your Kubernetes
cluster.

An operator is a set of [custom resources][custom-resource-definitions] and a
set of [controllers][controllers]. A controller watches for changes to specific
resources in the Kubernetes API and reacts by creating, updating, or deleting
resources.

The Operator SDK is best suited for building fully-featured operators.
Nonetheless, you can use it to write a single controller. This post will walk
you through writing a Kubernetes controller in Go that will add a `pod-name`
label to pods that have a specific annotation.

## Why do we need a controller for this?

I recently worked on a project where we needed to create a Service that routed
traffic to a specific Pod in a ReplicaSet. The problem is that a Service can
only select pods by label, and all pods in a ReplicaSet have the same labels.
There are two ways to solve this problem:

1. Create a Service without a selector and manage the Endpoints or
   EndpointSlices for that Service directly. We would need to write a custom
   controller to insert our Pod's IP address into those resources.
2. Add a label to the Pod with a unique value. We could then use this label in
   our Service's selector. Again, we would need to write a custom controller to
   add this label.

A controller is a control loop that tracks one or more Kubernetes resource
types. The controller from option n°2 above only needs to track pods, which
makes it simpler to implement. This is the option we are going to walk through
by writing a Kubernetes controller that adds a `pod-name` label to our pods.

StatefulSets [do this natively][statefulset-pod-name-label] by adding a
`pod-name` label to each Pod in the set. But what if we don't want to or can't
use StatefulSets?

We rarely create pods directly; most often, we use a Deployment, ReplicaSet, or
another high-level resource. We can specify labels to add to each Pod in the
PodSpec, but not with dynamic values, so no way to replicate a StatefulSet's
`pod-name` label.

We tried using a [mutating admission webhook][mutating-admission-webhook]. When
anyone creates a Pod, the webhook patches the Pod with a label containing the
Pod's name. Disappointingly, this does not work: not all pods have a name before
being created. For instance, when the ReplicaSet controller creates a Pod, it
sends a `namePrefix` to the Kubernetes API server and not a `name`. The API
server generates a unique name before persisting the new Pod to etcd, but only
after calling our admission webhook. So in most cases, we can't know a Pod's
name with a mutating webhook.

Once a Pod exists in the Kubernetes API, it is mostly immutable, but we can
still add a label. We can even do so from the command line:

```bash
kubectl label my-pod my-label-key=my-label-value
```

We need to watch for changes to any pods in the Kubernetes API and add the label
we want. Rather than do this manually, we are going to write a controller that
does it for us.

## Bootstrapping a controller with the Operator SDK

A controller is a reconciliation loop that reads the desired state of a resource
from the Kubernetes API and takes action to bring the cluster's actual state
closer to the desired state.

In order to write this controller as quickly as possible, we are going to use
the Operator SDK. If you don't have it installed, follow the
[official documentation][operator-sdk-installation].

```terminal
$ operator-sdk version
operator-sdk version: "v1.4.2", commit: "4b083393be65589358b3e0416573df04f4ae8d9b", kubernetes version: "v1.19.4", go version: "go1.15.8", GOOS: "darwin", GOARCH: "amd64"
```

Let's create a new directory to write our controller in:

```bash
mkdir label-operator && cd label-operator
```

Next, let's initialize a new operator, to which we will add a single controller.
To do this, you will need to specify a domain and a repository. The domain
serves as a prefix for the group your custom Kubernetes resources will belong
to. Because we are not going to be defining custom resources, the domain does
not matter. The repository is going to be the name of the Go module we are going
to write. By convention, this is the repository where you will be storing your
code.

As an example, here is the command I ran:

```bash
# Feel free to change the domain and repo values.
operator-sdk init --domain=padok.fr --repo=github.com/busser/label-operator
```

Next, we need a create a new controller. This controller will handle pods and
not a custom resource, so no need to generate the resource code. Let's run this
command to scaffold the code we need:

```bash
operator-sdk create api --group=core --version=v1 --kind=Pod --controller=true --resource=false
```

We now have a new file: `controllers/pod_controller.go`. This file contains a
`PodReconciler` type with two methods that we need to implement. The first is
`Reconcile`, and it looks like this for now:

```go
func (r *PodReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    _ = r.Log.WithValues("pod", req.NamespacedName)

    // your logic here

    return ctrl.Result{}, nil
}
```

The `Reconcile` method is called whenever a Pod is created, updated, or deleted.
The name and namespace of the Pod are in the `ctrl.Request` the method receives
as a parameter.

The second method is `SetupWithManager` and for now it looks like this:

```go
func (r *PodReconciler) SetupWithManager(mgr ctrl.Manager) error {
    return ctrl.NewControllerManagedBy(mgr).
        // Uncomment the following line adding a pointer to an instance of the controlled resource as an argument
        // For().
        Complete(r)
}
```

The `SetupWithManager` method is called when the operator starts. It serves to
tell the operator framework what types our `PodReconciler` needs to watch. To
use the same `Pod` type used by Kubernetes internally, we need to import some of
its code. All of the Kubernetes source code is open source, so you can import
any part you like in your own Go code. You can find a complete list of available
packages in the Kubernetes source code or [here on pkg.go.dev][pkg-go-dev]. To
use pods, we need the `k8s.io/api/core/v1` package.

```go
package controllers

import (
    // other imports...
    corev1 "k8s.io/api/core/v1"
    // other imports...
)
```

Lets use the `Pod` type in `SetupWithManager` to tell the operator framework we
want to watch pods:

```go
func (r *PodReconciler) SetupWithManager(mgr ctrl.Manager) error {
    return ctrl.NewControllerManagedBy(mgr).
        For(&corev1.Pod{}).
        Complete(r)
}
```

Before moving on, we should set the RBAC permissions our controller needs. Above
the `Reconcile` method, we have some default permissions:

```go
// +kubebuilder:rbac:groups=core,resources=pods,verbs=get;list;watch;create;update;patch;delete
// +kubebuilder:rbac:groups=core,resources=pods/status,verbs=get;update;patch
// +kubebuilder:rbac:groups=core,resources=pods/finalizers,verbs=update
```

We don't need all of those. Our controller will never interact with a Pod's
status or its finalizers. It only needs to read and update pods. Lets remove the
unnecessary permissions and keep only what we need:

```go
// +kubebuilder:rbac:groups=core,resources=pods,verbs=get;list;watch;update;patch
```

We are now ready to write our controller's reconciliation logic.

## Implementing reconciliation

Here is what we want our `Reconcile` method to do:

1. Use the Pod's name and namespace from the `ctrl.Request` to fetch the Pod
   from the Kubernetes API.
2. If the Pod has an `add-pod-name-label` annotation, add a `pod-name` label to
   the Pod; if the annotation is missing, don't add the label.
3. Update the Pod in the Kubernetes API to persist the changes made.

Lets define some constants for the annotation and label:

```go
const (
    addPodNameLabelAnnotation = "padok.fr/add-pod-name-label"
    podNameLabel              = "padok.fr/pod-name"
)
```

The first step in our reconciliation function is to fetch the Pod we are working
on from the Kubernetes API:

```go
// Reconcile handles a reconciliation request for a Pod.
// If the Pod has the addPodNameLabelAnnotation annotation, then Reconcile
// will make sure the podNameLabel label is present with the correct value.
// If the annotation is absent, then Reconcile will make sure the label is too.
func (r *PodReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    log := r.Log.WithValues("pod", req.NamespacedName)

    /*
        Step 0: Fetch the Pod from the Kubernetes API.
    */

    var pod corev1.Pod
    if err := r.Get(ctx, req.NamespacedName, &pod); err != nil {
        log.Error(err, "unable to fetch Pod")
        return ctrl.Result{}, err
    }

    return ctrl.Result{}, nil
}
```

Our `Reconcile` method will be called when a Pod is created, updated, or
deleted. In the deletion case, our call to `r.Get` will return a specific error.
Let's import the package that defines this error:

```go
package controllers

import (
    // other imports...
    apierrors "k8s.io/apimachinery/pkg/api/errors"
    // other imports...
)
```

We can now handle this specific error and — since our controller does not care
about deleted pods — explicitly ignore it:

```go
    /*
        Step 0: Fetch the Pod from the Kubernetes API.
    */

    var pod corev1.Pod
    if err := r.Get(ctx, req.NamespacedName, &pod); err != nil {
        if apierrors.IsNotFound(err) {
            // we'll ignore not-found errors, since we can get them on deleted requests.
            return ctrl.Result{}, nil
        }
        log.Error(err, "unable to fetch Pod")
        return ctrl.Result{}, err
    }
```

Next, lets edit our Pod so that our dynamic label is present if and only if our
annotation is present:

```go
    /*
        Step 1: Add or remove the label.
    */

    labelShouldBePresent := pod.Annotations[addPodNameLabelAnnotation] == "true"
    labelIsPresent := pod.Labels[podNameLabel] == pod.Name

    if labelShouldBePresent == labelIsPresent {
        // The desired state and actual state of the Pod are the same.
        // No further action is required by the operator at this moment.
        log.Info("no update required")
        return ctrl.Result{}, nil
    }

    if labelShouldBePresent {
        // If the label should be set but is not, set it.
        if pod.Labels == nil {
            pod.Labels = make(map[string]string)
        }
        pod.Labels[podNameLabel] = pod.Name
        log.Info("adding label")
    } else {
        // If the label should not be set but is, remove it.
        delete(pod.Labels, podNameLabel)
        log.Info("removing label")
    }
```

Finally, let's push our updated Pod to the Kubernetes API:

```go
    /*
        Step 2: Update the Pod in the Kubernetes API.
    */

    if err := r.Update(ctx, &pod); err != nil {
        log.Error(err, "unable to update Pod")
        return ctrl.Result{}, err
    }
```

When writing our updated Pod to the Kubernetes API, there is a risk that the Pod
has been updated or deleted since we first read it. When writing a Kubernetes
controller, we should keep in mind that we are not the only actors in the
cluster. When this happens, the best thing to do is start the reconciliation
from scratch, by requeuing the event. Lets do exactly that:

```go
    /*
        Step 2: Update the Pod in the Kubernetes API.
    */

    if err := r.Update(ctx, &pod); err != nil {
        if apierrors.IsConflict(err) {
            // The Pod has been updated since we read it.
            // Requeue the Pod to try to reconciliate again.
            return ctrl.Result{Requeue: true}, nil
        }
        if apierrors.IsNotFound(err) {
            // The Pod has been deleted since we read it.
            // Requeue the Pod to try to reconciliate again.
            return ctrl.Result{Requeue: true}, nil
        }
        log.Error(err, "unable to update Pod")
        return ctrl.Result{}, err
    }
```

Let's remember to return successfully at the end of the method:

```go
    return ctrl.Result{}, nil
}
```

And that's it! We are now ready to run the controller on our cluster.

## Run the controller on your cluster

To run our controller on your cluster, we need to run the operator. For that,
all you will need is `kubectl`. If you don't have a Kubernetes cluster at hand,
I recommend you start one locally with [KinD (Kubernetes in Docker)][kind].

All it takes to run the operator from your machine is this command:

```bash
make run
```

After a few seconds, you should see the operator's logs. Notice that our
controller's `Reconcile` method was called for all pods already running in the
cluster.

Let's keep the operator running and, in another terminal, create a new Pod:

```bash
kubectl run --image=nginx my-nginx
```

The operator should quickly print some logs, indicating that it reacted to the
Pod's creation and subsequent changes in status:

```text
INFO    controllers.Pod no update required  {"pod": "default/my-nginx"}
INFO    controllers.Pod no update required  {"pod": "default/my-nginx"}
INFO    controllers.Pod no update required  {"pod": "default/my-nginx"}
INFO    controllers.Pod no update required  {"pod": "default/my-nginx"}
```

Lets check the Pod's labels:

```terminal
$ kubectl get pod my-nginx --show-labels
NAME       READY   STATUS    RESTARTS   AGE   LABELS
my-nginx   1/1     Running   0          11m   run=my-nginx
```

Let's add an annotation to the Pod so that our controller knows to add our
dynamic label to it:

```bash
kubectl annotate pod my-nginx padok.fr/add-pod-name-label=true
```

Notice that the controller immediately reacted and produced a new line in its
logs:

```text
INFO    controllers.Pod adding label    {"pod": "default/my-nginx"}
```

```terminal
$ kubectl get pod my-nginx --show-labels
NAME       READY   STATUS    RESTARTS   AGE   LABELS
my-nginx   1/1     Running   0          13m   padok.fr/pod-name=my-nginx,run=my-nginx
```

Bravo! You just successfully wrote a Kubernetes controller capable of adding
labels with dynamic values to resources in your cluster.

Controllers and operators, both big and small, can be an important part of your
Kubernetes journey. Writing operators is easier now than it has ever been. The
possibilities are endless.

## What next?

If you want to go further, I recommend starting by deploying your controller or
operator inside a cluster. The `Makefile` generated by the Operator SDK will do
most of the work.

When deploying an operator to production, it is always a good idea to implement
robust testing. The first step in that direction is to write unit tests.
[This documentation][operator-sdk-testing] will guide you in writing tests for
your operator. I wrote tests for the operator we just wrote; you can find all of
my code in [this GitHub repository][github-repo].

## How to learn more?

The [Operator SDK documentation][operator-sdk-docs] goes into detail on how you
can go further and implement more complex operators.

When modeling a more complex use-case, a single controller acting on built-in
Kubernetes types may not be enough. You may need to build a more complex
operator with [Custom Resource Definitions (CRDs)][custom-resource-definitions]
and multiple controllers. The Operator SDK is a great tool to help you do this.

If you want to discuss building an operator, join the [#kubernetes-operator][slack-channel]
channel in the [Kubernetes Slack workspace][slack-workspace]!

<!-- Links -->

[controllers]: https://kubernetes.io/docs/concepts/architecture/controller/
[custom-resource-definitions]: https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/
[kind]: https://kind.sigs.k8s.io/docs/user/quick-start/#installation
[github-repo]: https://github.com/busser/label-operator
[mutating-admission-webhook]: https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/#mutatingadmissionwebhook
[operator-sdk]: https://sdk.operatorframework.io/
[operator-sdk-docs]: https://sdk.operatorframework.io/docs/
[operator-sdk-installation]: https://sdk.operatorframework.io/docs/installation/
[operator-sdk-testing]: https://sdk.operatorframework.io/docs/building-operators/golang/testing/
[operatorhub]: https://operatorhub.io/
[pkg-go-dev]: https://pkg.go.dev/k8s.io/api
[slack-channel]: https://kubernetes.slack.com/messages/kubernetes-operators
[slack-workspace]: https://slack.k8s.io/
[statefulset-pod-name-label]: https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/#pod-name-label
[what-is-an-operator]: https://kubernetes.io/docs/concepts/extend-kubernetes/operator/
