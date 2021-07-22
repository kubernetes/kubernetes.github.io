---
title: Recolección de Basura
content_type: concept
weight: 60
---

<!-- overview -->

El papel del recolector de basura de Kubernetes es el de eliminar determinados objetos
que en algún momento tuvieron un propietario, pero que ahora ya no.

<!-- body -->

## Propietarios y subordinados

Algunos objetos de Kubernetes son propietarios de otros objetos. Por ejemplo, un ReplicaSet
es el propietario de un conjunto de Pods. Los objetos que se poseen se denominan *subordinados* del
objeto propietario. Cada objeto subordinado tiene un campo `metadata.ownerReferences` 
que apunta al objeto propietario.

En ocasiones, Kubernetes pone el valor del campo `ownerReference` automáticamente.
 Por ejemplo, cuando creas un ReplicaSet, Kubernetes automáticamente pone el valor del campo 
`ownerReference` de cada Pod en el ReplicaSet. A partir de la versión 1.8, Kubernetes
automáticamente pone el valor de `ownerReference` para los objetos creados o adoptados
por un ReplicationController, ReplicaSet, StatefulSet, DaemonSet, Deployment, Job
y CronJob.

También puedes configurar las relaciones entre los propietarios y sus subordinados
de forma manual indicando el valor del campo `ownerReference`.

Aquí se muestra un archivo de configuración para un ReplicaSet que tiene tres Pods:

{{< codenew file="controllers/replicaset.yaml" >}}

Si se crea el ReplicaSet y entonces se muestra los metadatos del Pod, se puede 
observar el campo OwnerReferences:

```shell
kubectl apply -f https://k8s.io/examples/controllers/replicaset.yaml
kubectl get pods --output=yaml
```

La salida muestra que el propietario del Pod es el ReplicaSet denominado `my-repset`:

```shell
apiVersion: v1
kind: Pod
metadata:
  ...
  ownerReferences:
  - apiVersion: apps/v1
    controller: true
    blockOwnerDeletion: true
    kind: ReplicaSet
    name: my-repset
    uid: d9607e19-f88f-11e6-a518-42010a800195
  ...
```

{{< note >}}
No se recomienda el uso de OwnerReferences entre Namespaces por diseño. Esto quiere decir que: 
1) Los subordinados dentro del ámbito de Namespaces sólo pueden definir propietarios en ese mismo Namespace,
y propietarios dentro del ámbito de clúster.
2) Los subordinados dentro del ámbito del clúster sólo pueden definir propietarios dentro del ámbito del clúster, pero no
propietarios dentro del ámbito de Namespaces.
{{< /note >}}

## Controlar cómo el recolector de basura elimina los subordinados

Cuando eliminas un objeto, puedes indicar si sus subordinados deben eliminarse también
de forma automática. Eliminar los subordinados automáticamente se denomina *borrado en cascada*.  
Hay dos modos de *borrado en cascada*: *en segundo plano* y *en primer plano*.

Si eliminas un objeto sin borrar sus subordinados de forma automática,
dichos subordinados se convierten en *huérfanos*.

### Borrado en cascada en primer plano

En el *borrado en cascada en primer plano*, el objeto raíz primero entra en un estado
llamado "deletion in progress". En este estado "deletion in progress",
se cumplen las siguientes premisas:

 * El objeto todavía es visible a través de la API REST
 * Se pone el valor del campo `deletionTimestamp` del objeto
 * El campo `metadata.finalizers` del objeto contiene el valor "foregroundDeletion".

Una vez que se pone el estado "deletion in progress", el recolector de basura elimina
los subordinados del objeto. Una vez que el recolector de basura ha eliminado todos
los subordinados "bloqueantes" (los objetos con `ownerReference.blockOwnerDeletion=true`), elimina
el objeto propietario.

Cabe mencionar que usando "foregroundDeletion", sólo los subordinados con valor en 
`ownerReference.blockOwnerDeletion` bloquean la eliminación del objeto propietario.
A partir de la versión 1.7, Kubernetes añadió un [controlador de admisión](/docs/reference/access-authn-authz/admission-controllers/#ownerreferencespermissionenforcement) 
que controla el acceso de usuario cuando se intenta poner el campo `blockOwnerDeletion` a true 
con base a los permisos de borrado del objeto propietario, de forma que aquellos subordinados no autorizados
no puedan retrasar la eliminación del objeto propietario.

Si un controlador (como un Deployment o un ReplicaSet) establece el valor del campo `ownerReferences` de un objeto,
se pone blockOwnerDeletion automáticamente y no se necesita modificar de forma manual este campo.

### Borrado en cascada en segundo plano

En el *borrado en cascada en segundo plano*, Kubernetes elimina el objeto propietario
inmediatamente y es el recolector de basura quien se encarga de eliminar los subordinados en segundo plano.

### Configurar la regla de borrado en cascada

Para controlar la regla de borrado en cascada, configura el campo `propagationPolicy`
del parámetro `deleteOptions` cuando elimines un objeto. Los valores posibles incluyen "Orphan",
"Foreground", o "Background".

Antes de la versión 1.9 de Kubernetes, la regla predeterminada del recolector de basura para la mayoría de controladores era `orphan`.
Esto incluía al ReplicationController, ReplicaSet, StatefulSet, DaemonSet, y al Deployment. 
Para los tipos dentro de las versiones de grupo `extensions/v1beta1`, `apps/v1beta1`, y `apps/v1beta2`, a menos que
se indique de otra manera, los objetos subordinados se quedan huérfanos por defecto. 
En Kubernetes 1.9, para todos los tipos de la versión de grupo `apps/v1`, los objetos subordinados se eliminan por defecto.

Aquí se muestra un ejemplo que elimina los subordinados en segundo plano:

```shell
kubectl proxy --port=8080
curl -X DELETE localhost:8080/apis/apps/v1/namespaces/default/replicasets/my-repset \
-d '{"kind":"DeleteOptions","apiVersion":"v1","propagationPolicy":"Background"}' \
-H "Content-Type: application/json"
```

Aquí se muestra un ejemplo que elimina los subordinados en primer plano:

```shell
kubectl proxy --port=8080
curl -X DELETE localhost:8080/apis/apps/v1/namespaces/default/replicasets/my-repset \
-d '{"kind":"DeleteOptions","apiVersion":"v1","propagationPolicy":"Foreground"}' \
-H "Content-Type: application/json"
```

Aquí se muestra un ejemplo de subordinados huérfanos:

```shell
kubectl proxy --port=8080
curl -X DELETE localhost:8080/apis/apps/v1/namespaces/default/replicasets/my-repset \
-d '{"kind":"DeleteOptions","apiVersion":"v1","propagationPolicy":"Orphan"}' \
-H "Content-Type: application/json"
```

kubectl también permite el borrado en cascada.
Para eliminar los subordinados automáticamente, utiliza el parámetro `--cascade` a true.
  Usa false para subordinados huérfanos. Por defecto, el valor de `--cascade`
es true.

Aquí se muestra un ejemplo de huérfanos de subordinados de un ReplicaSet:

```shell
kubectl delete replicaset my-repset --cascade=orphan
```

### Nota adicional sobre los Deployments

Antes de la versión 1.7, cuando se usaba el borrado en cascada con Deployments se *debía* usar `propagationPolicy: Foreground`
para eliminar no sólo los ReplicaSets creados, sino también sus Pods correspondientes. Si este tipo de _propagationPolicy_
no se usa, solo se elimina los ReplicaSets, y los Pods se quedan huérfanos.
Ver [kubeadm/#149](https://github.com/kubernetes/kubeadm/issues/149#issuecomment-284766613) para más información.

## Problemas conocidos

Seguimiento en [#26120](https://github.com/kubernetes/kubernetes/issues/26120)



## {{% heading "whatsnext" %}}


[Documento de Diseño 1](https://git.k8s.io/community/contributors/design-proposals/api-machinery/garbage-collection.md)

[Documento de Diseño 2](https://git.k8s.io/community/contributors/design-proposals/api-machinery/synchronous-garbage-collection.md)

