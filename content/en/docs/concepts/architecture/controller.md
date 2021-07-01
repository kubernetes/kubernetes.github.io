---
title: Controllers
content_type: concept
weight: 30
---

<!-- overview -->

In robotics and automation, a _control loop_ is
a non-terminating loop that regulates the state of a system.

Here is one example of a control loop: a thermostat in a room.

When you set the temperature, that's telling the thermostat
about your *desired state*. The actual room temperature is the
*current state*. The thermostat acts to bring the current state
closer to the desired state, by turning equipment on or off.

{{< glossary_definition term_id="controller" length="short">}}




<!-- body -->

## Controller pattern

A controller tracks at least one Kubernetes resource type.
These [objects](/docs/concepts/overview/working-with-objects/kubernetes-objects/#kubernetes-objects)
have a spec field that represents the desired state. The
controller(s) for that resource are responsible for making the current
state come closer to that desired state.

The controller might carry the action out itself; more commonly, in Kubernetes,
a controller will send messages to the
{{< glossary_tooltip text="API server" term_id="kube-apiserver" >}} that have
useful side effects. You'll see examples of this below.

{{< comment >}}
Some built-in controllers, such as the namespace controller, act on objects
that do not have a spec. For simplicity, this page omits explaining that
detail.
{{< /comment >}}

### Control via API server

The {{< glossary_tooltip term_id="job" >}} controller is an example of a
Kubernetes built-in controller. Built-in controllers manage state by
interacting with the cluster API server.

Job is a Kubernetes resource that runs a
{{< glossary_tooltip term_id="pod" >}}, or perhaps several Pods, to carry out
a task and then stop.

(Once [scheduled](/docs/concepts/scheduling-eviction/), Pod objects become part of the
desired state for a kubelet).

When the Job controller sees a new task it makes sure that, somewhere
in your cluster, the kubelets on a set of Nodes are running the right
number of Pods to get the work done.
The Job controller does not run any Pods or containers
itself. Instead, the Job controller tells the API server to create or remove
Pods.
Other components in the
{{< glossary_tooltip text="control plane" term_id="control-plane" >}}
act on the new information (there are new Pods to schedule and run),
and eventually the work is done.

After you create a new Job, the desired state is for that Job to be completed.
The Job controller makes the current state for that Job be nearer to your
desired state: creating Pods that do the work you wanted for that Job, so that
the Job is closer to completion.

Controllers also update the objects that configure them.
For example: once the work is done for a Job, the Job controller
updates that Job object to mark it `Finished`.

(This is a bit like how some thermostats turn a light off to
indicate that your room is now at the temperature you set).

### Direct control

By contrast with Job, some controllers need to make changes to
things outside of your cluster.

For example, if you use a control loop to make sure there
are enough {{< glossary_tooltip text="Nodes" term_id="node" >}}
in your cluster, then that controller needs something outside the
current cluster to set up new Nodes when needed.

Controllers that interact with external state find their desired state from
the API server, then communicate directly with an external system to bring
the current state closer in line.

(There actually is a [controller](https://github.com/kubernetes/autoscaler/)
that horizontally scales the nodes in your cluster.)

The important point here is that the controller makes some change to bring about
your desired state, and then reports current state back to your cluster's API server.
Other control loops can observe that reported data and take their own actions.

In the thermostat example, if the room is very cold then a different controller
might also turn on a frost protection heater. With Kubernetes clusters, the control
plane indirectly works with IP address management tools, storage services,
cloud provider APIs, and other services by
[extending Kubernetes](/docs/concepts/extend-kubernetes/) to implement that.

## Desired versus current state {#desired-vs-current}

Kubernetes takes a cloud-native view of systems, and is able to handle
constant change.

Your cluster could be changing at any point as work happens and
control loops automatically fix failures. This means that,
potentially, your cluster never reaches a stable state.

As long as the controllers for your cluster are running and able to make
useful changes, it doesn't matter if the overall state is stable or not.

## Design

As a tenet of its design, Kubernetes uses lots of controllers that each manage
a particular aspect of cluster state. Most commonly, a particular control loop
(controller) uses one kind of resource as its desired state, and has a different
kind of resource that it manages to make that desired state happen. For example,
a controller for Jobs tracks Job objects (to discover new work) and Pod objects
(to run the Jobs, and then to see when the work is finished). In this case
something else creates the Jobs, whereas the Job controller creates Pods.

It's useful to have simple controllers rather than one, monolithic set of control
loops that are interlinked. Controllers can fail, so Kubernetes is designed to
allow for that.

{{< note >}}
There can be several controllers that create or update the same kind of object.
Behind the scenes, Kubernetes controllers make sure that they only pay attention
to the resources linked to their controlling resource.

For example, you can have Deployments and Jobs; these both create Pods.
The Job controller does not delete the Pods that your Deployment created,
because there is information ({{< glossary_tooltip term_id="label" text="labels" >}})
the controllers can use to tell those Pods apart.
{{< /note >}}

## Ways of running controllers {#running-controllers}

Kubernetes comes with a set of built-in controllers that run inside
the {{< glossary_tooltip term_id="kube-controller-manager" >}}. These
built-in controllers provide important core behaviors.

The Deployment controller and Job controller are examples of controllers that
come as part of Kubernetes itself ("built-in" controllers).
Kubernetes lets you run a resilient control plane, so that if any of the built-in
controllers were to fail, another part of the control plane will take over the work.

You can find controllers that run outside the control plane, to extend Kubernetes.
Or, if you want, you can write a new controller yourself.
You can run your own controller as a set of Pods,
or externally to Kubernetes. What fits best will depend on what that particular
controller does.

## {{% heading "whatsnext" %}}

* Read about the [Kubernetes control plane](/docs/concepts/overview/components/#control-plane-components)
* Discover some of the basic [Kubernetes objects](/docs/concepts/overview/working-with-objects/kubernetes-objects/)
* Learn more about the [Kubernetes API](/docs/concepts/overview/kubernetes-api/)
* If you want to write your own controller, see
  [Extension Patterns](/docs/concepts/extend-kubernetes/#extension-patterns)
  in Extending Kubernetes.

