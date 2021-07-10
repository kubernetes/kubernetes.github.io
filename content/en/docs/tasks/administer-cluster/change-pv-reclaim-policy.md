---
title: Change the Reclaim Policy of a PersistentVolume
content_type: task
---

<!-- overview -->
This page shows how to change the reclaim policy of a Kubernetes
PersistentVolume.


## {{% heading "prerequisites" %}}


{{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}



<!-- steps -->

## Why change reclaim policy of a PersistentVolume

PersistentVolumes can have various reclaim policies, including "Retain",
"Recycle", and "Delete". For dynamically provisioned PersistentVolumes,
the default reclaim policy is "Delete". This means that a dynamically provisioned
volume is automatically deleted when a user deletes the corresponding
PersistentVolumeClaim. This automatic behavior might be inappropriate if the volume
contains precious data. In that case, it is more appropriate to use the "Retain"
policy. With the "Retain" policy, if a user deletes a PersistentVolumeClaim,
the corresponding PersistentVolume will not be deleted. Instead, it is moved to the
Released phase, where all of its data can be manually recovered.

## Changing the reclaim policy of a PersistentVolume

1. List the PersistentVolumes in your cluster:

    ```shell
    kubectl get pv
    ```

    The output is similar to this:

        NAME                                       CAPACITY   ACCESSMODES   RECLAIMPOLICY   STATUS    CLAIM             STORAGECLASS     REASON    AGE
        pvc-b6efd8da-b7b5-11e6-9d58-0ed433a7dd94   4Gi        RWO           Delete          Bound     default/claim1    manual                     10s
        pvc-b95650f8-b7b5-11e6-9d58-0ed433a7dd94   4Gi        RWO           Delete          Bound     default/claim2    manual                     6s
        pvc-bb3ca71d-b7b5-11e6-9d58-0ed433a7dd94   4Gi        RWO           Delete          Bound     default/claim3    manual                     3s

     This list also includes the name of the claims that are bound to each volume
   for easier identification of dynamically provisioned volumes.

1. Choose one of your PersistentVolumes and change its reclaim policy:

    ```shell
    kubectl patch pv <your-pv-name> -p '{"spec":{"persistentVolumeReclaimPolicy":"Retain"}}'
    ```

    where `<your-pv-name>` is the name of your chosen PersistentVolume.

    {{< note >}}
    On Windows, you must _double_ quote any JSONPath template that contains spaces (not single quote as shown above for bash). This in turn means that you must use a single quote or escaped double quote around any literals in the template. For example:

```cmd
kubectl patch pv <your-pv-name> -p "{\"spec\":{\"persistentVolumeReclaimPolicy\":\"Retain\"}}"
```

    {{< /note >}}

1. Verify that your chosen PersistentVolume has the right policy:

    ```shell
    kubectl get pv
    ```

    The output is similar to this:

        NAME                                       CAPACITY   ACCESSMODES   RECLAIMPOLICY   STATUS    CLAIM             STORAGECLASS     REASON    AGE
        pvc-b6efd8da-b7b5-11e6-9d58-0ed433a7dd94   4Gi        RWO           Delete          Bound     default/claim1    manual                     40s
        pvc-b95650f8-b7b5-11e6-9d58-0ed433a7dd94   4Gi        RWO           Delete          Bound     default/claim2    manual                     36s
        pvc-bb3ca71d-b7b5-11e6-9d58-0ed433a7dd94   4Gi        RWO           Retain          Bound     default/claim3    manual                     33s

    In the preceding output, you can see that the volume bound to claim
    `default/claim3` has reclaim policy `Retain`. It will not be automatically
    deleted when a user deletes claim `default/claim3`.



## {{% heading "whatsnext" %}}

* Learn more about [PersistentVolumes](/docs/concepts/storage/persistent-volumes/).
* Learn more about [PersistentVolumeClaims](/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims).

### Reference

* {{< api-reference page="config-and-storage-resources/persistent-volume-v1" >}}
* {{< api-reference page="config-and-storage-resources/persistent-volume-claim-v1" >}}
* See the `persistentVolumeReclaimPolicy` field of {{< api-reference page="config-and-storage-resources/persistent-volume-v1" anchor="PersistentVolumeSpec" >}}.
