---
title: ReplicaSet
content_type: concept
weight: 10
---

<!-- overview -->

El objeto de un ReplicaSet es el de mantener un conjunto estable de réplicas de Pods ejecutándose
en todo momento. Así, se usa en numerosas ocasiones para garantizar la disponibilidad de un
número específico de Pods idénticos.




<!-- body -->

## Cómo funciona un ReplicaSet

Un ReplicaSet se define con campos, incluyendo un selector que indica cómo identificar a los Pods que puede adquirir, 
un número de réplicas indicando cuántos Pods debería gestionar, y una plantilla pod especificando los datos de los nuevos Pods
que debería crear para conseguir el número de réplicas esperado. Un ReplicaSet alcanza entonces su propósito
 mediante la creación y eliminación de los Pods que sea necesario para alcanzar el número esperado. 
 Cuando un ReplicaSet necesita crear nuevos Pods, utiliza su plantilla Pod.

El enlace que un ReplicaSet tiene hacia sus Pods es a través del campo del Pod denominado [metadata.ownerReferences](/docs/concepts/workloads/controllers/garbage-collection/#owners-and-dependents),
el cual indica qué recurso es el propietario del objeto actual. Todos los Pods adquiridos por un ReplicaSet tienen su propia
información de identificación del ReplicaSet en su campo ownerReferences. Y es a través de este enlace
cómo el ReplicaSet conoce el estado de los Pods que está gestionando y actúa en consecuencia.

Un ReplicaSet identifica los nuevos Pods a adquirir usando su selector. Si hay un Pod que no tiene OwnerReference 
o donde OwnerReference no es un controlador, pero coincide con el selector del ReplicaSet, 
este será inmediatamente adquirido por dicho ReplicaSet.

## Cuándo usar un ReplicaSet

Un ReplicaSet garantiza que un número específico de réplicas de un pod se está ejecutando en todo momento. 
Sin embargo, un Deployment es un concepto de más alto nivel que gestiona ReplicaSets y
proporciona actualizaciones de forma declarativa de los Pods junto con muchas otras características útiles.
Por lo tanto, se recomienda el uso de Deployments en vez del uso directo de ReplicaSets, a no ser
que se necesite una orquestración personalizada de actualización o no se necesite las actualizaciones en absoluto.

En realidad, esto quiere decir que puede que nunca necesites manipular los objetos ReplicaSet:
en vez de ello, usa un Deployment, y define tu aplicación en la sección spec.

## Ejemplo

{{< codenew file="controllers/frontend.yaml" >}}

Si guardas este manifiesto en un archivo llamado `frontend.yaml` y lo lanzas en un clúster de Kubernetes,
 se creará el ReplicaSet definido y los Pods que maneja.

```shell
kubectl apply -f http://k8s.io/examples/controllers/frontend.yaml
```

Puedes ver los ReplicaSets actuales desplegados:
```shell
kubectl get rs
```

Y ver el frontend que has creado:
```shell
NAME       DESIRED   CURRENT   READY   AGE
frontend   3         3         3       6s
```

También puedes comprobar el estado del replicaset:
```shell
kubectl describe rs/frontend
```

Y verás una salida parecida a la siguiente:
```shell
Name:		frontend
Namespace:	default
Selector:	tier=frontend,tier in (frontend)
Labels:		app=guestbook
		tier=frontend
Annotations:	<none>
Replicas:	3 current / 3 desired
Pods Status:	3 Running / 0 Waiting / 0 Succeeded / 0 Failed
Pod Template:
  Labels:       app=guestbook
                tier=frontend
  Containers:
   php-redis:
    Image:      gcr.io/google_samples/gb-frontend:v3
    Port:       80/TCP
    Requests:
      cpu:      100m
      memory:   100Mi
    Environment:
      GET_HOSTS_FROM:   dns
    Mounts:             <none>
  Volumes:              <none>
Events:
  FirstSeen    LastSeen    Count    From                SubobjectPath    Type        Reason            Message
  ---------    --------    -----    ----                -------------    --------    ------            -------
  1m           1m          1        {replicaset-controller }             Normal      SuccessfulCreate  Created pod: frontend-qhloh
  1m           1m          1        {replicaset-controller }             Normal      SuccessfulCreate  Created pod: frontend-dnjpy
  1m           1m          1        {replicaset-controller }             Normal      SuccessfulCreate  Created pod: frontend-9si5l
```

Y por último, puedes comprobar los Pods que ha arrancado:
```shell
kubectl get Pods
```

Deberías ver la información de cada Pod similar a:
```shell
NAME             READY     STATUS    RESTARTS   AGE
frontend-9si5l   1/1       Running   0          1m
frontend-dnjpy   1/1       Running   0          1m
frontend-qhloh   1/1       Running   0          1m
```

También puedes verificar que la referencia de propietario de dichos pods está puesta al ReplicaSet frontend.
Para ello, obtén el yaml de uno de los Pods ejecutándose:
```shell
kubectl get pods frontend-9si5l -o yaml
```

La salida será parecida a esta, donde la información sobre el ReplicaSet aparece en el campo ownerReferences de los metadatos:
```shell
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: 2019-01-31T17:20:41Z
  generateName: frontend-
  labels:
    tier: frontend
  name: frontend-9si5l
  namespace: default
  ownerReferences:
  - apiVersion: extensions/v1beta1
    blockOwnerDeletion: true
    controller: true
    kind: ReplicaSet
    name: frontend
    uid: 892a2330-257c-11e9-aecd-025000000001
...
```

## Adquisiciones de Pods fuera de la plantilla

Aunque puedes crear Pods simples sin problemas, se recomienda encarecidamente asegurarse de que dichos Pods no tienen
etiquetas que puedan coincidir con el selector de alguno de tus ReplicaSets. 
La razón de esta recomendación es que un ReplicaSet no se limita a poseer los Pods 
especificados en su plantilla -- sino que puede adquirir otros Pods como se explicó en secciones anteriores.

Toma el ejemplo anterior del ReplicaSet frontend, y los Pods especificados en el siguiente manifiesto:

{{< codenew file="pods/pod-rs.yaml" >}}

Como estos Pods no tienen un Controlador (o cualquier otro objeto) como referencia de propietario
y como además su selector coincide con el del ReplicaSet frontend, este último los terminará adquiriendo de forma inmediata.

Supón que creas los Pods después de que el ReplicaSet frontend haya desplegado los suyos
para satisfacer su requisito de cuenta de réplicas:

```shell
kubectl apply -f http://k8s.io/examples/pods/pod-rs.yaml
```

Los nuevos Pods serán adquiridos por el ReplicaSet, e inmediatamente terminados ya que
 el ReplicaSet estaría por encima del número deseado.

Obtener los Pods:
```shell
kubectl get Pods
```

La salida muestra que los nuevos Pods se han terminado, o están en el proceso de terminarse:
```shell
NAME             READY   STATUS        RESTARTS   AGE
frontend-9si5l   1/1     Running       0          1m
frontend-dnjpy   1/1     Running       0          1m
frontend-qhloh   1/1     Running       0          1m
pod2             0/1     Terminating   0          4s
```

Si creas primero los Pods:
```shell
kubectl apply -f http://k8s.io/examples/pods/pod-rs.yaml
```

Y entonces creas el ReplicaSet:
```shell
kubectl apply -f http://k8s.io/examples/controllers/frontend.yaml
```

Verás que el ReplicaSet ha adquirido dichos Pods y simplemente ha creado tantos nuevos
como necesarios para cumplir con su especificación hasta que el número de 
sus nuevos Pods y los originales coincidan con la cuenta deseado. Al obtener los Pods:
```shell
kubectl get Pods
```

Veremos su salida:
```shell
NAME             READY   STATUS    RESTARTS   AGE
frontend-pxj4r   1/1     Running   0          5s
pod1             1/1     Running   0          13s
pod2             1/1     Running   0          13s
```

De esta forma, un ReplicaSet puede poseer un conjunto no homogéneo de Pods

## Escribir un manifiesto de ReplicaSet

Al igual que con el esto de los objeto de la API de Kubernetes, un ReplicaSet necesita los campos
`apiVersion`, `kind`, y `metadata`. Para los ReplicaSets, el tipo es siempre ReplicaSet.
En la versión 1.9 de Kubernetes, la versión `apps/v1` de la API en un tipo ReplicaSet es la versión actual y está habilitada por defecto. 
La versión `apps/v1beta2` de la API se ha desaprobado.
Consulta las primeras líneas del ejemplo `frontend.yaml` como guía.

Un ReplicaSet también necesita una [sección `.spec`](https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status).

### Plantilla Pod

El campo `.spec.template` es una [plantilla pod](/docs/concepts/workloads/Pods/pod-overview/#pod-templates) que es
 también necesita obligatoriamente tener etiquetas definidas. En nuestro ejemplo `frontend.yaml` teníamos una etiqueta: `tier: frontend`.
Lleva cuidado de que no se entremezcle con los selectores de otros controladores, no sea que traten de adquirir este Pod.

Para el campo de [regla de reinicio](/docs/concepts/workloads/Pods/pod-lifecycle/#restart-policy) de la plantilla,
`.spec.template.spec.restartPolicy`, el único valor permitido es `Always`, que es el valor predeterminado.

### Selector de Pod

El campo `.spec.selector` es un [selector de etiqueta](/docs/concepts/overview/working-with-objects/labels/). 
Como se explicó [anteriormente](#how-a-replicaset-works), estas son las etiquetas que se usan para
 identificar los Pods potenciales a adquirir. En nuestro ejemplo `frontend.yaml`, el selector era:
```shell
matchLabels:
	tier: frontend
```

El el ReplicaSet, `.spec.template.metadata.labels` debe coincidir con `spec.selector`, o será
 rechazado por la API.

{{< note >}}
Cuando 2 ReplicaSets especifican el mismo campo `.spec.selector`, pero los campos 
`.spec.template.metadata.labels` y `.spec.template.spec` diferentes, cada ReplicaSet 
ignora los Pods creados por el otro ReplicaSet.
{{< /note >}}

### Réplicas

Puedes configurar cuántos Pods deberían ejecutarse de forma concurrente indicando el campo `.spec.replicas`. 
El ReplicaSet creará/eliminará sus Pods para alcanzar este número.

Si no indicas el valor del campo `.spec.replicas`, entonces por defecto se inicializa a 1.

## Trabajar con ReplicaSets

### Eliminar un ReplicaSet y sus Pods

Para eliminar un ReplicaSet y todos sus Pods, utiliza el comando [`kubectl delete`](/docs/reference/generated/kubectl/kubectl-commands#delete). 
El [Recolector de basura](/docs/concepts/workloads/controllers/garbage-collection/) eliminará automáticamente
 todos los Pods subordinados por defecto.

Cuando se usa la API REST o la librería `client-go`, se debe poner el valor de `propagationPolicy` a `Background` o 
`Foreground` en la opción -d.
Por ejemplo:
```shell
kubectl proxy --port=8080
curl -X DELETE  'localhost:8080/apis/extensions/v1beta1/namespaces/default/replicasets/frontend' \
> -d '{"kind":"DeleteOptions","apiVersion":"v1","propagationPolicy":"Foreground"}' \
> -H "Content-Type: application/json"
```

### Eliminar sólo un ReplicaSet

Se puede eliminar un ReplicaSet sin afectar a ninguno de sus Pods usando el comando [`kubectl delete`](/docs/reference/generated/kubectl/kubectl-commands#delete) con la opción `--cascade=orphan`.
Cuando se usa la API REST o la librería `client-go`, se debe poner `propagationPolicy` a `Orphan`.
Por ejemplo:
```shell
kubectl proxy --port=8080
curl -X DELETE  'localhost:8080/apis/extensions/v1beta1/namespaces/default/replicasets/frontend' \
> -d '{"kind":"DeleteOptions","apiVersion":"v1","propagationPolicy":"Orphan"}' \
> -H "Content-Type: application/json"
```

Una vez que se ha eliminado el original, se puede crear un nuevo ReplicaSet para sustituirlo.
Mientras el viejo y el nuevo `.spec.selector` sean el mismo, el nuevo adoptará a los viejos Pods.
Sin embargo, no se esforzará en conseguir que los Pods existentes coincidan con una plantilla pod nueva, diferente.
Para actualizar dichos Pods a la nueva especificación de forma controlada, 
usa una [actualización en línea](#rolling-updates).

### Aislar Pods de un ReplicaSet

Es posible aislar Pods de un ReplicaSet cambiando sus etiquetas. Esta técnica puede usarse
para eliminar Pods de un servicio para poder depurar, recuperar datos, etc. Los Pods 
que se eliminar de esta forma serán sustituidos de forma automática (siempre que el 
número de réplicas no haya cambiado).

### Escalar un ReplicaSet

Se puede aumentar o reducir fácilmente un ReplicaSet simplemente actualizando el campo `.spec.replicas`. 
El controlador del ReplicaSet se asegura de que el número deseado de Pods con un selector
de etiquetas coincidente está disponible y operacional.

### ReplicaSet como blanco de un Horizontal Pod Autoscaler

Un ReplicaSet puede también ser el blanco de un 
[Horizontal Pod Autoscalers (HPA)](/docs/tasks/run-application/horizontal-pod-autoscale/). Esto es,
un ReplicaSet puede auto-escalarse mediante un HPA. Aquí se muestra un ejemplo de HPA dirigido
al ReplicaSet que creamos en el ejemplo anterior.

{{< codenew file="controllers/hpa-rs.yaml" >}}

Si guardas este manifiesto en un archivo `hpa-rs.yaml` y lo lanzas contra el clúster de Kubernetes,
debería crear el HPA definido que auto-escala el ReplicaSet destino dependiendo del uso
de CPU de los Pods replicados.

```shell
kubectl apply -f https://k8s.io/examples/controllers/hpa-rs.yaml
```

Alternativamente, puedes usar el comando `kubectl autoscale` para conseguir el mismo objetivo
(¡y mucho más fácil!)

```shell
kubectl autoscale rs frontend --max=10
```

## Alternativas al ReplicaSet

### Deployment (recomendado)

Un[`Deployment`](/docs/concepts/workloads/controllers/deployment/) es un objeto que puede poseer ReplicaSets 
y actualizar a estos y a sus Pods mediante actualizaciones en línea declarativas en el servidor.
Aunque que los ReplicaSets puede usarse independientemente, hoy en día se usan principalmente a través de los Deployments 
como el mecanismo para orquestrar la creación, eliminación y actualización de los Pods. 
Cuando usas Deployments no tienes que preocuparte de gestionar los ReplicaSets que crean. 
Los Deployments poseen y gestionan sus ReplicaSets.
Por tanto, se recomienda que se use Deployments cuando se quiera ReplicaSets.

### Pods simples

A diferencia del caso en que un usuario creaba Pods de forma directa, un ReplicaSet sustituye los Pods que se eliminan
o se terminan por la razón que sea, como en el caso de un fallo de un nodo o 
una intervención disruptiva de mantenimiento, como una actualización de kernel. 
Por esta razón, se recomienda que se use un ReplicaSet incluso cuando la aplicación
sólo necesita un único Pod. Entiéndelo de forma similar a un proceso supervisor, 
donde se supervisa múltiples Pods entre múltiples nodos en vez de procesos individuales
en un único nodo. Un ReplicaSet delega los reinicios del contenedor local a algún agente
del nodo (por ejemplo, Kubelet o Docker).

### Job

Usa un [`Job`](/docs/concepts/jobs/run-to-completion-finite-workloads/) en vez de un ReplicaSet para 
 aquellos Pods que se esperan que terminen por ellos mismos (esto es, trabajos por lotes).

### DaemonSet

Usa un [`DaemonSet`](/docs/concepts/workloads/controllers/daemonset/) en vez de un ReplicaSet para aquellos
 Pods que proporcionan funcionalidad a nivel de servidor, como monitorización de servidor o
 logging de servidor. Estos Pods tienen un ciclo de vida asociado al del servidor mismo: 
 el Pod necesita ejecutarse en el servidor antes de que los otros Pods comiencen, y es seguro
 que terminen cuando el servidor esté listo para ser reiniciado/apagado.

### ReplicationController
Los ReplicaSets son los sucesores de los [_ReplicationControllers_](/docs/concepts/workloads/controllers/replicationcontroller/).
Los dos sirven al mismo propósito, y se comportan de forma similar, excepto porque un ReplicationController 
no soporta los requisitos del selector basado en conjunto, como se describe en la [guía de usuario de etiquetas](/docs/concepts/overview/working-with-objects/labels/#label-selectors).
Por ello, se prefiere los ReplicaSets a los ReplicationControllers.


