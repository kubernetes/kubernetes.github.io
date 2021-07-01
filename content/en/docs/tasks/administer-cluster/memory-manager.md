---
title: Memory Manager

reviewers:
- klueska
- derekwaynecarr

content_type: task
min-kubernetes-server-version: v1.21
---

<!-- overview -->

{{< feature-state state="alpha" for_k8s_version="v1.21" >}}

The Kubernetes *Memory Manager* enables the feature of guaranteed memory (and hugepages) allocation for pods in the `Guaranteed` {{< glossary_tooltip text="QoS class" term_id="qos-class" >}}.

The Memory Manager employs hint generation protocol to yield the most suitable NUMA affinity for a pod. The Memory Manager feeds the central manager (*Topology Manager*) with these affinity hints. Based on both the hints and Topology Manager policy, the pod is rejected or admitted to the node.

Moreover, the Memory Manager ensures that the memory which a pod requests is allocated from a minimum number of NUMA nodes.

The Memory Manager is only pertinent to Linux based hosts.

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}

To align memory resources with other requested resources in a Pod Spec:
- the CPU Manager should be enabled and proper CPU Manager policy should be configured on a Node. See [control CPU Management Policies](/docs/tasks/administer-cluster/cpu-management-policies/);
- the Topology Manager should be enabled and proper Topology Manager policy should be configured on a Node. See [control Topology Management Policies](/docs/tasks/administer-cluster/topology-manager/).

Support for the Memory Manager requires `MemoryManager` [feature gate](/docs/reference/command-line-tools-reference/feature-gates/) to be enabled. 

That is, the `kubelet` must be started with the following flag:

`--feature-gates=MemoryManager=true`

## How Memory Manager Operates?

The Memory Manager currently offers the guaranteed memory (and hugepages) allocation for Pods in Guaranteed QoS class. To immediately put the Memory Manager into operation follow the guidelines in the section [Memory Manager configuration](#memory-manager-configuration), and subsequently, prepare and deploy a `Guaranteed` pod as illustrated in the section [Placing a Pod in the Guaranteed QoS class](#placing-a-pod-in-the-guaranteed-qos-class).

The Memory Manager is a Hint Provider, and it provides topology hints for the Topology Manager which then aligns the requested resources according to these topology hints. It also enforces `cgroups` (i.e. `cpuset.mems`) for pods. The complete flow diagram concerning pod admission and deployment process is illustrated in [Memory Manager KEP: Design Overview][4] and below:

![Memory Manager in the pod admission and deployment process](/images/docs/memory-manager-diagram.svg)

During this process, the Memory Manager updates its internal counters stored in [Node Map and Memory Maps][2] to manage guaranteed memory allocation. 

The Memory Manager updates the Node Map during the startup and runtime as follows.

### Startup

This occurs once a node administrator employs `--reserved-memory` (section [Reserved memory flag](#reserved-memory-flag)). In this case, the Node Map becomes updated to reflect this reservation as illustrated in [Memory Manager KEP: Memory Maps at start-up (with examples)][5].

The administrator must provide `--reserved-memory` flag when `Static` policy is configured.

### Runtime

Reference [Memory Manager KEP: Memory Maps at runtime (with examples)][6] illustrates how a successful pod deployment affects the Node Map, and it also relates to how potential Out-of-Memory (OOM) situations are handled further by Kubernetes or operating system.

Important topic in the context of Memory Manager operation is the management of NUMA groups. Each time pod's memory request is in excess of single NUMA node capacity, the Memory Manager attempts to create a group that comprises several NUMA nodes and features extend memory capacity. The problem has been solved as elaborated in [Memory Manager KEP: How to enable the guaranteed memory allocation over many NUMA nodes?][3]. Also, reference [Memory Manager KEP: Simulation - how the Memory Manager works? (by examples)][1] illustrates how the management of groups occurs. 

## Memory Manager configuration

Other Managers should be first pre-configured (section [Pre-configuration](#pre-configuration)). Next, the Memory Manger feature should be enabled (section [Enable the Memory Manager feature](#enable-the-memory-manager-feature)) and be run with `Static` policy (section [Static policy](#static-policy)). Optionally, some amount of memory can be reserved for system or kubelet processes to increase node stability (section [Reserved memory flag](#reserved-memory-flag)).

### Policies 

Memory Manager supports two policies. You can select a policy via a `kubelet` flag `--memory-manager-policy`.

Two policies can be selected:

* `None` (default)
* `Static`

#### None policy {#policy-none}

This is the default policy and does not affect the memory allocation in any way.
It acts the same as if the Memory Manager is not present at all.

The `None` policy returns default topology hint. This special hint denotes that Hint Provider (Memory Manger in this case) has no preference for NUMA affinity with any resource.

#### Static policy {#policy-static}

In the case of the `Guaranteed` pod, the `Static` Memory Manger policy returns topology hints relating to the set of NUMA nodes where the memory can be guaranteed, and reserves the memory through updating the internal [NodeMap][2] object.

In the case of the `BestEffort` or `Burstable` pod, the `Static` Memory Manager policy sends back the default topology hint as there is no request for the guaranteed memory, and does not reserve the memory in the internal [NodeMap][2] object.

### Reserved memory flag

The [Node Allocatable](/docs/tasks/administer-cluster/reserve-compute-resources/) mechanism is commonly used by node administrators to reserve K8S node system resources for the kubelet or operating system processes in order to enhance the node stability. A dedicated set of flags can be used for this purpose to set the total amount of reserved memory for a node. This pre-configured value is subsequently utilized to calculate the real amount of node's "allocatable" memory available to pods.

The Kubernetes scheduler incorporates "allocatable" to optimise pod scheduling process. The foregoing flags include `--kube-reserved`, `--system-reserved` and `--eviction-threshold`. The sum of their values will account for the total amount of reserved memory.


A new `--reserved-memory` flag was added to Memory Manager to allow for this total reserved memory to be split (by a node administrator) and accordingly reserved across many NUMA nodes. 

The flag specifies a comma-separated list of memory reservations per NUMA node.
This parameter is only useful in the context of the Memory Manager feature. 
The Memory Manager will not use this reserved memory for the allocation of container workloads.

For example, if you have a NUMA node "NUMA0" with `10Gi` of memory available, and the `--reserved-memory` was specified to reserve `1Gi` of memory at "NUMA0", the Memory Manager assumes that only `9Gi` is available for containers.

You can omit this parameter, however, you should be aware that the quantity of reserved memory from all NUMA nodes should be equal to the quantity of memory specified by the [Node Allocatable feature](/docs/tasks/administer-cluster/reserve-compute-resources/). If at least one node allocatable parameter is non-zero, you will need to specify `--reserved-memory` for at least one NUMA node. In fact, `eviction-hard` threshold value is equal to `100Mi` by default, so if `Static` policy is used, `--reserved-memory` is obligatory.

Also, avoid the following configurations:
1. duplicates, i.e. the same NUMA node or memory type, but with a different value;
2. setting zero limit for any of memory types;
3. NUMA node IDs that do not exist in the machine hardware;
4. memory type names different than `memory` or `hugepages-<size>` (hugepages of particular `<size>` should also exist).

Syntax: 

`--reserved-memory N:memory-type1=value1,memory-type2=value2,...`
* `N` (integer) - NUMA node index, e.g. `0`
* `memory-type` (string) - represents memory type:
  * `memory` - conventional memory
  * `hugepages-2Mi` or `hugepages-1Gi` - hugepages 
* `value` (string) - the quantity of reserved memory, e.g. `1Gi`

Example usage:

`--reserved-memory 0:memory=1Gi,hugepages-1Gi=2Gi`

or

`--reserved-memory 0:memory=1Gi --reserved-memory 1:memory=2Gi`

When you specify values for `--reserved-memory` flag, you must comply with the setting that you prior provided via Node Allocatable Feature flags. That is, the following rule must be obeyed for each memory type: 

`sum(reserved-memory(i)) = kube-reserved + system-reserved + eviction-threshold`, 

where `i` is an index of a NUMA node. 

If you do not follow the formula above, the Memory Manager will show an error on startup.

In other words, the example above illustrates that for the conventional memory (`type=memory`), we reserve `3Gi` in total, i.e.: 

`sum(reserved-memory(i)) = reserved-memory(0) + reserved-memory(1) = 1Gi + 2Gi = 3Gi`

An example of kubelet command-line arguments relevant to the node Allocatable configuration:
* `--kube-reserved=cpu=500m,memory=50Mi`
* `--system-reserved=cpu=123m,memory=333Mi`
* `--eviction-hard=memory.available<500Mi`

{{< note >}} 
The default hard eviction threshold is 100MiB, and **not** zero. Remember to increase the quantity of memory that you reserve by setting `--reserved-memory` by that hard eviction threshold. Otherwise, the kubelet will not start Memory Manager and display an error. 
{{< /note >}}

Here is an example of a correct configuration:

```shell
--feature-gates=MemoryManager=true 
--kube-reserved=cpu=4,memory=4Gi 
--system-reserved=cpu=1,memory=1Gi 
--memory-manager-policy=Static 
--reserved-memory 0:memory=3Gi --reserved-memory 1:memory=2148Mi
```
Let us validate the configuration above:
1. `kube-reserved + system-reserved + eviction-hard(default) = reserved-memory(0) + reserved-memory(1)`
2. `4GiB + 1GiB + 100MiB = 3GiB + 2148MiB`
3. `5120MiB + 100MiB = 3072MiB + 2148MiB`
4. `5220MiB = 5220MiB` (which is correct)

## Placing a Pod in the Guaranteed QoS class

If the selected policy is anything other than `None`, the Memory Manager identifies pods that are in the `Guaranteed` QoS class. The Memory Manager provides specific topology hints to the Topology Manager for each `Guaranteed` pod. For pods in a QoS class other than `Guaranteed`, the Memory Manager provides default topology hints to the Topology Manager.

The following excerpts from pod manifests assign a pod to the `Guaranteed` QoS class.

Pod with integer CPU(s) runs in the `Guaranteed` QoS class, when `requests` are equal to `limits`:

```yaml
spec:
  containers:
  - name: nginx
    image: nginx
    resources:
      limits:
        memory: "200Mi"
        cpu: "2"
        example.com/device: "1"
      requests:
        memory: "200Mi"
        cpu: "2"
        example.com/device: "1"
```

Also, a pod sharing CPU(s) runs in the `Guaranteed` QoS class, when `requests` are equal to `limits`.

```yaml
spec:
  containers:
  - name: nginx
    image: nginx
    resources:
      limits:
        memory: "200Mi"
        cpu: "300m"
        example.com/device: "1"
      requests:
        memory: "200Mi"
        cpu: "300m"
        example.com/device: "1"
```

Notice that both CPU and memory requests must be specified for a Pod to lend it to Guaranteed QoS class.

## Troubleshooting

The following means can be used to troubleshoot the reason why a pod could not be deployed or became rejected at a node:
- pod status - indicates topology affinity errors
- system logs - include valuable information for debugging, e.g., about generated hints
- state file - the dump of internal state of the Memory Manager (includes [Node Map and Memory Maps][2]) 

### Pod status (TopologyAffinityError) {#TopologyAffinityError}

This error typically occurs in the following situations:
* a node has not enough resources available to satisfy the pod's request
* the pod's request is rejected due to particular Topology Manager policy constraints 

The error appears in the status of a pod:
```shell
# kubectl get pods
NAME         READY   STATUS                  RESTARTS   AGE
guaranteed   0/1     TopologyAffinityError   0          113s
```

Use `kubectl describe pod <id>` or `kubectl get events` to obtain detailed error message:
```shell
Warning  TopologyAffinityError  10m   kubelet, dell8  Resources cannot be allocated with Topology locality
```

### System logs

Search system logs with respect to a particular pod.

The set of hints that Memory Manager generated for the pod can be found in the logs. 
Also, the set of hints generated by CPU Manager should be present in the logs.

Topology Manager merges these hints to calculate a single best hint.
The best hint should be also present in the logs.

The best hint indicates where to allocate all the resources. Topology Manager tests this hint against its current policy, and based on the verdict, it either admits the pod to the node or rejects it.  

Also, search the logs for occurrences associated with the Memory Manager, e.g. to find out information about `cgroups` and `cpuset.mems` updates.

### Examine the memory manager state on a node

Let us first deploy a sample `Guaranteed` pod whose specification is as follows:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: guaranteed
spec:
  containers:
  - name: guaranteed
    image: consumer
    imagePullPolicy: Never
    resources:
      limits:
        cpu: "2"
        memory: 150Gi
      requests:
        cpu: "2"
        memory: 150Gi
    command: ["sleep","infinity"]
``` 

Next, let us log into the node where it was deployed and examine the state file in `/var/lib/kubelet/memory_manager_state`:
```json
{
   "policyName":"Static",
   "machineState":{
      "0":{
         "numberOfAssignments":1,
         "memoryMap":{
            "hugepages-1Gi":{
               "total":0,
               "systemReserved":0,
               "allocatable":0,
               "reserved":0,
               "free":0
            },
            "memory":{
               "total":134987354112,
               "systemReserved":3221225472,
               "allocatable":131766128640,
               "reserved":131766128640,
               "free":0
            }
         },
         "nodes":[
            0,
            1
         ]
      },
      "1":{
         "numberOfAssignments":1,
         "memoryMap":{
            "hugepages-1Gi":{
               "total":0,
               "systemReserved":0,
               "allocatable":0,
               "reserved":0,
               "free":0
            },
            "memory":{
               "total":135286722560,
               "systemReserved":2252341248,
               "allocatable":133034381312,
               "reserved":29295144960,
               "free":103739236352
            }
         },
         "nodes":[
            0,
            1
         ]
      }
   },
   "entries":{
      "fa9bdd38-6df9-4cf9-aa67-8c4814da37a8":{
         "guaranteed":[
            {
               "numaAffinity":[
                  0,
                  1
               ],
               "type":"memory",
               "size":161061273600
            }
         ]
      }
   },
   "checksum":4142013182
}
```

It can be deduced from the state file that the pod was pinned to both NUMA nodes, i.e.:

```json
"numaAffinity":[
   0,
   1
],
``` 

Pinned term means that pod's memory consumption is constrained (through `cgroups` configuration) to these NUMA nodes.

This automatically implies that Memory Manager instantiated a new group that comprises these two NUMA nodes, i.e. `0` and `1` indexed NUMA nodes. 

Notice that the management of groups is handled in a relatively complex manner, and further elaboration is provided in Memory Manager KEP in [this][1] and [this][3] sections.

In order to analyse memory resources available in a group, the corresponding entries from NUMA nodes belonging to the group must be added up.  

For example, the total amount of free "conventional" memory in the group can be computed by adding up the free memory available at every NUMA node in the group, i.e., in the `"memory"` section of NUMA node `0` (`"free":0`) and NUMA node `1` (`"free":103739236352`). So, the total amount of free "conventional" memory in this group is equal to `0 + 103739236352` bytes.  

The line `"systemReserved":3221225472` indicates that the administrator of this node reserved `3221225472` bytes (i.e. `3Gi`) to serve kubelet and system processes at NUMA node `0`, by using `--reserved-memory` flag.

## {{% heading "whatsnext" %}}

- [Memory Manager KEP: Design Overview][4] 

- [Memory Manager KEP: Memory Maps at start-up (with examples)][5]

- [Memory Manager KEP: Memory Maps at runtime (with examples)][6]

- [Memory Manager KEP: Simulation - how the Memory Manager works? (by examples)][1]

- [Memory Manager KEP: The Concept of Node Map and Memory Maps][2]

- [Memory Manager KEP: How to enable the guaranteed memory allocation over many NUMA nodes?][3]

[1]: https://github.com/kubernetes/enhancements/tree/master/keps/sig-node/1769-memory-manager#simulation---how-the-memory-manager-works-by-examples
[2]: https://github.com/kubernetes/enhancements/tree/master/keps/sig-node/1769-memory-manager#the-concept-of-node-map-and-memory-maps
[3]: https://github.com/kubernetes/enhancements/tree/master/keps/sig-node/1769-memory-manager#how-to-enable-the-guaranteed-memory-allocation-over-many-numa-nodes
[4]: https://github.com/kubernetes/enhancements/tree/master/keps/sig-node/1769-memory-manager#design-overview
[5]: https://github.com/kubernetes/enhancements/tree/master/keps/sig-node/1769-memory-manager#memory-maps-at-start-up-with-examples
[6]: https://github.com/kubernetes/enhancements/tree/master/keps/sig-node/1769-memory-manager#memory-maps-at-runtime-with-examples
