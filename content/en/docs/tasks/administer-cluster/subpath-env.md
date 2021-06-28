---
title: Using SubPath with Expanded Environment Variables 
content_type: task
min-kubernetes-server-version: v1.15
---
{{< feature-state for_k8s_version="v1.17" state="stable" >}}

<!-- overview -->

Use the `subPathExpr` field to construct `subPath` directory names from
downward API environment variables. In other words, the `subPath` mounted by a pod may determined using variables, such as pod name. For example, you can create a folder for logs from each pod.

The `subPath` and `subPathExpr` properties are mutually exclusive.

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}

<!-- steps -->

## Example manifest

In this example, a pod uses `subPathExpr` to create a directory `pod1` within
the `hostPath` volume `/var/log/pods`. All containers see this as simply `/logs`. Thus, logs may be collected from multiple pods in directories such as `/var/log/pods/pod1/` and `.../pods/pod2/`.

First, the spec defines an environment variable `POD_NAME` using the _downward API_.

Second, a subpath on the volume mount is defined using a `subPathExpr`. This allows the subpath to change based on environment variables. The subpath `pod1` is determined using an environment variable. 

Overall, the host directory `/var/log/pods/pod1` is mounted at `/logs` in the container.


```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod1
spec:
  containers:
  - name: container1
    env:
    - name: POD_NAME
      valueFrom:
        fieldRef:
          apiVersion: v1
          fieldPath: metadata.name
    image: busybox
    command: [ "sh", "-c", "while [ true ]; do echo 'Hello'; sleep 10; done | tee -a /logs/hello.txt" ]
    volumeMounts:
    - name: workdir1
      mountPath: /logs
      subPathExpr: $(POD_NAME)
  restartPolicy: Never
  volumes:
  - name: workdir1
    hostPath:
      path: /var/log/pods
```

## {{% heading "whatsnext" %}}

* Learn more about [PersistentVolumeClaims] and automating the provisioning of volumes. (/docs/concepts/storage/persistent-volumes/#persistentvolumeclaims).
* Learn more about [Persistent Volumes] and managing storage declaratively. (/docs/concepts/storage/volumes/).