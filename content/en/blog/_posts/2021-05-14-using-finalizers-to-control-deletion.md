---
layout: blog
title: 'Using Finalizers to Control Deletion'
date: 2021-05-14
slug: using-finalizers-to-control-deletion
---

**Authors:** Aaron Alpar (Kasten)

Deleting objects in Kubernetes can be challenging. You may think you’ve deleted something, only to find it still persists. While issuing a `kubectl delete` command and hoping for the best might work for day-to-day operations, understanding how Kubernetes `delete` commands operate will help you understand why some objects linger after deletion. 

In this post, I’ll look at:

- What properties of a resource govern deletion
- How finalizers and owner references impact object deletion
- How the propagation policy can be used to change the order of deletions
- How deletion works, with examples

For simplicity, all examples will use ConfigMaps and basic shell commands to demonstrate the process. We’ll explore how the commands work and discuss repercussions and results from using them in practice.

## The basic `delete`

Kubernetes has several different commands you can use that allow you to create, read, update, and delete objects. For the purpose of this blog post, we’ll focus on four `kubectl` commands: `create`, `get`, `patch`, and `delete`. 

Here are examples of the basic `kubectl delete` command:

```
kubectl create configmap mymap
configmap/mymap created
```

```
kubectl get configmap/mymap
NAME    DATA   AGE
mymap   0      12s
```

```
kubectl delete configmap/mymap
configmap "mymap" deleted
```

```
kubectl get configmap/mymap
Error from server (NotFound): configmaps "mymap" not found
```

Shell commands preceded by `$` are followed by their output. You can see that we begin with a `kubectl create configmap mymap`, which will create the empty configmap `mymap`. Next, we need to `get` the configmap to prove it exists. We can then delete that configmap. Attempting to `get` it again produces an HTTP 404 error, which means the configmap is not found.

The state diagram for the basic `delete` command is very simple:


{{<figure width="495" src="/images/blog/2021-05-14-using-finalizers-to-control-deletion/state-diagram-delete.png" caption="State diagram for delete">}}

Although this operation is straightforward, other factors may interfere with the deletion, including finalizers and owner references.

## Understanding Finalizers

When it comes to understanding resource deletion in Kubernetes, knowledge of how finalizers work is helpful and can help you understand why some objects don’t get deleted. 

Finalizers are keys on resources that signal pre-delete operations. They control the garbage collection on resources, and are designed to alert controllers what cleanup operations to perform prior to removing a resource. However, they don’t necessarily name code that should be executed; finalizers on resources are basically just lists of keys much like annotations. Like annotations, they can be manipulated.

Some common finalizers you’ve likely encountered are:

- `kubernetes.io/pv-protection`
- `kubernetes.io/pvc-protection`

The finalizers above are used on volumes to prevent accidental deletion. Similarly, some finalizers can be used to prevent deletion of any resource but are not managed by any controller.

Below with a custom configmap, which has no properties but contains a finalizer:

```
cat <<EOF | kubectl create -f -
apiVersion: v1
kind: ConfigMap
metadata:
  name: mymap
  finalizers:
  - kubernetes
EOF
```

The configmap resource controller doesn't understand what to do with the `kubernetes` finalizer key. I term these “dead” finalizers for configmaps as it is normally used on namespaces. Here’s what happen upon attempting to delete the configmap:

```
kubectl delete configmap/mymap &
configmap "mymap" deleted
jobs
[1]+  Running kubectl delete configmap/mymap
```

Kubernetes will report back that the object has been deleted, however, it hasn’t been deleted in a traditional sense. Rather, it’s in the process of deletion. When we attempt to `get` that object again, we discover the object has been modified to include the deletion timestamp. 

```
kubectl get configmap/mymap -o yaml
apiVersion: v1
kind: ConfigMap
metadata:
  creationTimestamp: "2020-10-22T21:30:18Z"
  deletionGracePeriodSeconds: 0
  deletionTimestamp: "2020-10-22T21:30:34Z"
  finalizers:
  - kubernetes
  name: mymap
  namespace: default
  resourceVersion: "311456"
  selfLink: /api/v1/namespaces/default/configmaps/mymap
  uid: 93a37fed-23e3-45e8-b6ee-b2521db81638
```

In short, what’s happened is that the object was updated, not deleted. That’s because Kubernetes saw that the object contained finalizers and put it into a read-only state. The deletion timestamp signals that the object can only be read, with the exception of removing the finalizer key updates. In other words, the deletion will not be complete until we edit the object and remove the finalizer.

Here's a demonstration of using the `patch` command to remove finalizers. If we want to delete an object, we can simply patch it on the command line to remove the finalizers. In this way, the deletion that was running in the background will complete and the object will be deleted. When we attempt to `get` that configmap, it will be gone. 

```
kubectl patch configmap/mymap \
    --type json \
    --patch='[ { "op": "remove", "path": "/metadata/finalizers" } ]'
configmap/mymap patched
[1]+  Done  kubectl delete configmap/mymap

kubectl get configmap/mymap -o yaml
Error from server (NotFound): configmaps "mymap" not found
```

Here's a state diagram for finalization: 

{{<figure width="617" src="/images/blog/2021-05-14-using-finalizers-to-control-deletion/state-diagram-finalize.png" caption="State diagram for finalize">}}

So, if you attempt to delete an object that has a finalizer on it, it will remain in finalization until the controller has removed the finalizer keys or the finalizers are removed using Kubectl. Once that finalizer list is empty, the object can actually be reclaimed by Kubernetes and put into a queue to be deleted from the registry.

## Owner References

Owner references describe how groups of objects are related. They are properties on resources that specify the relationship to one another, so entire trees of resources can be deleted.

Finalizer rules are processed when there are owner references. An owner reference consists of a name and a UID. Owner references link resources within the same namespace, and it also needs a UID for that reference to work. Pods typically have owner references to the owning replica set. So, when deployments or stateful sets are deleted, then the child replica sets and pods are deleted in the process. 

Here are some examples of owner references and how they work. In the first example, we create a parent object first, then the child. The result is a very simple configmap that contains an owner reference to its parent:

```
cat <<EOF | kubectl create -f -
apiVersion: v1
kind: ConfigMap
metadata:
  name: mymap-parent
EOF
CM_UID=$(kubectl get configmap mymap-parent -o jsonpath="{.metadata.uid}")

cat <<EOF | kubectl create -f -
apiVersion: v1
kind: ConfigMap
metadata:
  name: mymap-child
  ownerReferences:
  - apiVersion: v1
    kind: ConfigMap
    name: mymap-parent
    uid: $CM_UID
EOF
```

Deleting the child object when an owner reference is involved does not delete the parent:

```
kubectl get configmap
NAME           DATA   AGE
mymap-child    0      12m4s
mymap-parent   0      12m4s

kubectl delete configmap/mymap-child
configmap "mymap-child" deleted

kubectl get configmap
NAME           DATA   AGE
mymap-parent   0      12m10s
```

In this example, we re-created the parent-child configmaps from above. Now, when deleting from the parent (instead of the child) with an owner reference from the child to the parent, when we `get` the configmaps, none are in the namespace:

```
kubectl get configmap
NAME           DATA   AGE
mymap-child    0      10m2s
mymap-parent   0      10m2s

kubectl delete configmap/mymap-parent
configmap "mymap-parent" deleted

kubectl get configmap
No resources found in default namespace.
```

To sum things up, when there's an override owner reference from a child to a parent, deleting the parent deletes the children automatically. This is called `cascade`. The default for cascade is `true`, however, you can use the --cascade=orphan option for `kubectl delete` to delete an object and orphan its children. 

In the following example, there is a parent and a child. Notice the owner references are still included. If I delete the parent using --cascade=orphan, the parent is deleted but the child still exists:

```
kubectl get configmap
NAME           DATA   AGE
mymap-child    0      13m8s
mymap-parent   0      13m8s

kubectl delete --cascade=orphan configmap/mymap-parent
configmap "mymap-parent" deleted

kubectl get configmap
NAME          DATA   AGE
mymap-child   0      13m21s
```

The --cascade option links to the propagation policy in the API, which allows you to change the order in which objects are deleted within a tree. In the following example uses API access to craft a custom delete API call with the background propagation policy:

```
kubectl proxy --port=8080 &
Starting to serve on 127.0.0.1:8080

curl -X DELETE \
  localhost:8080/api/v1/namespaces/default/configmaps/mymap-parent \
  -d '{ "kind":"DeleteOptions", "apiVersion":"v1", "propagationPolicy":"Background" }' \
  -H "Content-Type: application/json"
{
  "kind": "Status",
  "apiVersion": "v1",
  "metadata": {},
  "status": "Success",
  "details": { ... }
}
```

Note that the propagation policy cannot be specified on the command line using kubectl. You have to specify it using a custom API call. Simply create a proxy, so you have access to the API server from the client, and execute a `curl` command with just a URL to execute that `delete` command. 

There are three different options for the propagation policy:

- `Foreground`: Children are deleted before the parent (post-order)
- `Background`: Parent is deleted before the children (pre-order)
- `Orphan`: Owner references are ignored

Keep in mind that when you delete an object and owner references have been specified, finalizers will be honored in the process. This can result in trees of objects persisting, and you end up with a partial deletion. At that point, you have to look at any existing owner references on your objects, as well as any finalizers, to understand what’s happening. 

## Forcing a Deletion of a Namespace

There's one situation that may require forcing finalization for a namespace. If you've deleted a namespace and you've cleaned out all of the objects under it, but the namespace still exists, deletion can be forced by updating the namespace subresource, `finalize`. This informs the namespace controller that it needs to remove the finalizer from the namespace and perform any cleanup:

```
cat <<EOF | curl -X PUT \
  localhost:8080/api/v1/namespaces/test/finalize \
  -H "Content-Type: application/json" \
  --data-binary @-
{
  "kind": "Namespace",
  "apiVersion": "v1",
  "metadata": {
    "name": "test"
  },
  "spec": {
    "finalizers": null
  }
}
EOF
```

This should be done with caution as it may delete the namespace only and leave orphan objects within the, now non-exiting, namespace - a confusing state for Kubernetes. If this happens, the namespace can be re-created manually and sometimes the orphaned objects will re-appear under the just-created namespace which will allow manual cleanup and recovery.

## Key Takeaways

As these examples demonstrate, finalizers can get in the way of deleting resources in Kubernetes, especially when there are parent-child relationships between objects. Often, there is a reason for adding a finalizer into the code, so you should always investigate before manually deleting it. Owner references allow you to specify and remove trees of resources, although finalizers will be honored in the process. Finally, the propagation policy can be used to specify the order of deletion via a custom API call, giving you control over how objects are deleted. Now that you know a little more about how deletions work in Kubernetes, we recommend you try it out on your own, using a test cluster. 

{{< youtube class="youtube-quote-sm" id="F7-ZxWwf4sY" title="Clean Up Your Room! What Does It Mean to Delete Something in K8s">}}
