---
title: ReplicationController
feature:
  title: Auto-reparación
  anchor: Cómo funciona un ReplicationController
  description: >
    Reinicia contenedores que fallan, sustituye y reprograma contenedores cuando los nodos mueren,
    mata los contenedores que no responden a tus pruebas de salud definidas,
    y no los expone a los clientes hasta que no están listo para servirse.

content_type: concept
weight: 20
---

<!-- overview -->

{{< note >}}
hoy en día la forma recomendada de configurar la replicación es con un [`Deployment`](/docs/concepts/workloads/controllers/deployment/) que configura un [`ReplicaSet`](/docs/concepts/workloads/controllers/replicaset/).
{{< /note >}}

Un _ReplicationController_ garantiza que un número determinado de réplicas se estén ejecutando
en todo momento. En otras palabras, un ReplicationController se asegura que un pod o un conjunto homogéneo de pods
siempre esté arriba y disponible.




<!-- body -->

## Cómo Funciona un ReplicationController

Si hay muchos pods, el ReplicationController termina los pods extra. Si hay muy pocos, el
ReplicationController arranca más pods. A difrencia de los pods creados manualmente, los pods mantenidos por un
ReplicationController se sustituyen de forma automática si fallan, se borran, o se terminan.
Por ejemplo, tus pods se re-crean en un nodo durante una intervención disruptiva de mantenimiento como una actualización del kernel.
Por esta razón, deberías usar un ReplicationController incluso cuando tu aplicación sólo necesita
un único pod. Un ReplicationController es parecido a un supervisor de procesos,
pero en vez de supervisar procesos individuales en un único nodo,
el ReplicationController supervisa múltiples pods entre múltiples nodos.

A menudo nos referimos a un ReplicationController de forma abreviada como "rc" o "rcs", así como
atajo en los comandos de kubectl.

Un caso simple es crear un objeto ReplicationController para ejecutar de manera fiable una instancia
de un Pod indefinidamente. Un caso de uso más complejo es ejecutar varias réplicas idénticas
 de un servicio replicado, como los servidores web.

## Ejecutar un ejemplo de ReplicationController

Esta configuración de un ReplicationController de ejemplo ejecuta tres copias del servidor web nginx.

{{< codenew file="controllers/replication.yaml" >}}

Ejecuta el ejemplo descargando el archivo de ejemplo y ejecutando este comando:

```shell
kubectl apply -f https://k8s.io/examples/controllers/replication.yaml
```
```
replicationcontroller/nginx created
```

Comprueba el estado del ReplicationController con este comando:

```shell
kubectl describe replicationcontrollers/nginx
```
```
Name:        nginx
Namespace:   default
Selector:    app=nginx
Labels:      app=nginx
Annotations:    <none>
Replicas:    3 current / 3 desired
Pods Status: 0 Running / 3 Waiting / 0 Succeeded / 0 Failed
Pod Template:
  Labels:       app=nginx
  Containers:
   nginx:
    Image:              nginx
    Port:               80/TCP
    Environment:        <none>
    Mounts:             <none>
  Volumes:              <none>
Events:
  FirstSeen       LastSeen     Count    From                        SubobjectPath    Type      Reason              Message
  ---------       --------     -----    ----                        -------------    ----      ------              -------
  20s             20s          1        {replication-controller }                    Normal    SuccessfulCreate    Created pod: nginx-qrm3m
  20s             20s          1        {replication-controller }                    Normal    SuccessfulCreate    Created pod: nginx-3ntk0
  20s             20s          1        {replication-controller }                    Normal    SuccessfulCreate    Created pod: nginx-4ok8v
```

Como se puede observar, se han creado tres pods, pero ninguno se está ejecutándose todavía,
puede que porque la imagen todavía se está descargando.
Unos momentos después, el mismo comando puede que muestre:

```shell
Pods Status:    3 Running / 0 Waiting / 0 Succeeded / 0 Failed
```

Para listar todos los pods que pertenecen al ReplicationController de forma legible,
puedes usar un comando como el siguiente:

```shell
pods=$(kubectl get pods --selector=app=nginx --output=jsonpath={.items..metadata.name})
echo $pods
```
```
nginx-3ntk0 nginx-4ok8v nginx-qrm3m
```

Como se puede ver, el selector es el mismo que el selector del ReplicationController (mostrado en la salida de
`kubectl describe`), y con una forma diferente a lo definido en el archivo `replication.yaml`.
La opción `--output=jsonpath` especifica una expresión que simplemente muestra el nombre
de cada pod en la lista devuelta.


## Escribir una especificación de ReplicationController

Al igual que con el resto de configuraciones de Kubernetes, un ReplicationController necesita los campos `apiVersion`, `kind`, y `metadata`.
Para información general acerca del trabajo con archivos de configuración, ver la [gestión de objetos](/docs/concepts/overview/object-management-kubectl/overview/).

Un ReplicationController también necesita un [sección `.spec`](https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status).

### Plantilla Pod

El campo `.spec.template` es el único campo requerido de `.spec`.

El campo `.spec.template` es una [plantilla pod](/docs/concepts/workloads/pods/pod-overview/#pod-templates).
Tiene exactamente el mismo esquema que un [pod](/docs/concepts/workloads/pods/pod/), excepto por el hecho de que está anidado y no tiene los campos `apiVersion` ni `kind`.

Además de los campos obligatorios de un Pod, una plantilla pod de un ReplicationController debe especificar las etiquetas apropiadas
y la regla de reinicio apropiada. En el caso de las etiquetas, asegúrate que no se entremezclan con otros controladores. Ver el [selector de pod](#pod-selector).

Sólo se permite el valor `Always` para el campo [`.spec.template.spec.restartPolicy`](/docs/concepts/workloads/pods/pod-lifecycle/#restart-policy),
que es el valor predeterminado si no se indica.

Para los reinicios locales de los contenedores, los ReplicationControllers delegan en los agentes del nodo,
por ejmplo el [Kubelet](/docs/admin/kubelet/) o Docker.

### Etiquetas en los ReplicationController

los ReplicationController puede tener sus propias (`.metadata.labels`). Normalmente, se indicaría dichas etiquetas
con los mismos valores que el campo `.spec.template.metadata.labels`; si el campo `.metadata.labels` no se indica,
entonces se predetermina al valor de `.spec.template.metadata.labels`. Sin embargo, se permite que sean diferentes,
y el valor de `.metadata.labels` no afecta al comportamiento del ReplicationController.

### Selector de Pod

El campo `.spec.selector` es un [selector de etiqueta](/docs/concepts/overview/working-with-objects/labels/#label-selectors). Un ReplicationController
gestiona todos los pods con etiquetas que coinciden con el selector. No distingue entre
pods que creó o eliminó, y pods que otra persona o proceso creó o eliminó. Esto permite sustituir al ReplicationController sin impactar a ninguno de sus pods que se esté ejecutando.

Si se indica, el valor de `.spec.template.metadata.labels` debe ser igual al de `.spec.selector`, o será rechazado por la API.
Si no se indica el valor de `.spec.selector`, se tomará como predeterminado el de `.spec.template.metadata.labels`.

Tampoco deberías crear ningún pod cuyas etiquetas coincidan con las de este selector, ni directamente con
otro ReplicationController, ni con otro controlador como un Job. Si lo haces, el
ReplicationController piensa que el creó también los otros pods. Kubernetes no te impide hacerlo.

Si al final terminas con múltiples controladores que tienen selectores que se entremezclan,
tendrás que gestionar la eliminación tú mismo (ver [abajo](#working-with-replicationcontrollers)).

### Múltiples Réplicas

Puedes configurar cuántos pods deberían ejecutarse de forma concurrente poniendo el valor de `.spec.replicas` al número
de pods que te gustaría tener ejecutándose a la vez. El número de ejecuciones en cualquier momento puede que sea superior
 o inferior, dependiendo de si las réplicas se han incrementado o decrementado, o si un pod se ha apagado de forma controlada,
  y su sustituto arranca más pronto.

Si no se indica el valor de `.spec.replicas`, entonces se predetermina a 1.

## Trabajar con ReplicationControllers

### Eliminar un ReplicationController y sus Pods

Para eliminar un ReplicationController y todos sus pods, usa el comando [`kubectl
delete`](/docs/reference/generated/kubectl/kubectl-commands#delete). Kubectl reducirá el ReplicationController a cero y esperará
que elimine cada pod antes de eliminar al ReplicationController mismo. Si este comando kubectl
se interrumpe, puede ser reiniciado.

Cuando uses la API REST o la librería Go, necesitas realizar los pasos de forma explícita (reducir las réplicas a cero,
esperar a que se eliminen los pods, y entonces eliminar el ReplicationController).

### Eliminar sólo el ReplicationController

Puedes eliminar un ReplicationController sin impactar a ninguno de sus Pods.

Usando kubectl, indica la opción `--cascade=orphan` en el comando [`kubectl delete`](/docs/reference/generated/kubectl/kubectl-commands#delete).

Cuando uses la API REST o la librería Go, simplemente elimina objeto ReplicationController.

Una vez que el objeto original se ha eliminado, puedes crear un nuevo ReplicationController para sustituirlo.
  Mientras el viejo y el nuevo valor del `.spec.selector` sea el mismo, el nuevo adoptará a los viejos pods.
Sin embargo, no se molestará en hacer que los pods actuales coincidan con una plantilla pod nueva, diferente.
Para actualizar los pods con una nueva especificación de forma controlada, utiliza la [actualización en línea](#rolling-updates).

### Aislar pods de un ReplicationController

Se puede aislar Pods del conjunto destino de un ReplicationController cambiando sus etiquetas.
Esta técnica puede usarse para eliminar pods de un servicio para poder depurarlos, recuperar datos, etc.
Los Pods que se eliminan de esta forma serán sustituidos de forma automática (asumiendo que el número de réplicas no ha cambiado tampoco).

## Patrones comunes de uso

### Reprogramación

Como se comentó arriba, cuando tienes 1 pod que quieres mantener ejecutándose, o 1000, un ReplicationController se asegura de que el número indicado de pods exista,
incluso si falla un nodo o se termina algún pod (por ejemplo, debido a alguna acción de otro agente de control).

### Escalado

El ReplicationController facilita el escalado del número de réplicas tanto para su aumento como para su disminución,
bien manualmente o mediante un agente de auto-escalado, simplemente actualizando el campo `replicas`.

### Actualizaciones en línea

El ReplicationController se ha diseñado para facilitar las actualizaciones en línea de un servicio mediante la sustitución de sus pods uno por uno.

Cómo se explicó en [#1353](http://issue.k8s.io/1353), la estrategia recomendada es crear un nuevo ReplicationController con 1 réplica,
escalar el nuevo (+1) y el viejo (-1) controlador uno por uno, y entonces eliminar el viejo controlador una vez que alcanza las 0 réplicas.
Esto actualiza de forma predecible el conjunto de pods independientemente de que se produzcan fallos inesperados.

De forma ideal, el controlador de actualización en línea tendrá en cuenta si la aplicación está lista, y
se asegurará de que un número suficiente de pods está en servicio en todo momento.

Los dos ReplicationControllers necesitarán crear pods con al menos una etiqueta diferenciadora, como la etiqueta de imagen del contenedor primario del pod,
ya que las actualizaciones de imagen son las que normalmente desencadenan las actualizaciones en línea.

La actualización en línea se implementa a través de la herramienta cliente mediante
[`kubectl rolling-update`](/docs/reference/generated/kubectl/kubectl-commands#rolling-update).
Echa un vistazo a la [tarea `kubectl rolling-update`](/docs/tasks/run-application/rolling-update-replication-controller/) para más ejemplos concretos.

### Múltiples operaciones de despliegue

Además de llevar a cabo múltiples despliegues de una aplicación cuando una actualización en línea está en progreso,
es común ejecutar varios despliegues durante un período extendido de tiempo, o incluso de forma contínua, usando múltiples operaciones de despliegue. Dichas operaciones se diferenciarían por etiquetas.

Por ejemplo, un servicio puede que exponga todos los pods con etiquetas `tier in (frontend), environment in (prod)`. Ahora digamos que tenemos 10 pods replicados que forman este grupo.
Pero queremos poder desplegar una nueva versión 'canary' de este component. Se podría configurar un ReplicationController con el valor de `replicas` puesto a 9 para la mayor parte de las réplicas,
con etiquetas `tier=frontend, environment=prod, track=stable`, y otro ReplicationController con el valor de `replicas` puesto a 1 para el 'canary',
con las etiquetas `tier=frontend, environment=prod, track=canary`. Así el servicio cubriría tanto los pods canary como el resto.
Pero también es posible trastear con los ReplicationControllers de forma separada para probar cosas, monitorizar los resultados, etc.

### Usar ReplicationControllers con servicios

Un único servicio puede exponer múltiples ReplicationControllers, de forma que, por ejemplo, algo de tráfico
vaya a la versión vieja, y otro tanto vaya a la versión nueva.

Un ReplicationController nunca se terminará por sí mismo, pero tampoco se espera que se ejecute permanentemente como los servicios.
Los servicios puede que estén compuestos de pods controlados por múltiples ReplicationControllers,
y se espera que muchos ReplicationControllers se creen y se destruyan durante el ciclo de vida de un servicio (por ejemplo,
para realizar una actualización de los pods que ejecutan el servicio). Ambos servicios mismos y sus clientes deberían permanecer
ajenos a los ReplicationControllers que mantienen los pods que proporcionan los servicios.

## Escribir aplicaciones que se repliquen

Los Pods creados por un ReplicationController están pensados para que sean intercambiables y semánticamente idénticos,
aunque sus configuraciones puede que sean heterogéneas a lo largo del tiempo. Este es un ajuste obvio para los servidores sin estado replicados,
pero los ReplicationControllers también pueden utilizarse para mantener la disponibilidad de aplicaciones que se elijen por un maestro, las particionadas, y las de grupos de trabajadores.
Dichas aplicaciones deberían usar los mecanismos de asignación dinámica de trabajo, como las [colas de trabajo RabbitMQ](https://www.rabbitmq.com/tutorials/tutorial-two-python.html),
en vez de la personalización estática/de una sola vez en la configuración de cada pod,
ya que se considera un anti-patrón. Cualquier personalización de pod que se haga, como el calibrado vertical automático de recursos (por ejemplo, cpu o memoria),
debería realizarse a través de otro proceso de controlador en línea, no con el mismo ReplicationController.

## Responsabilidades de un ReplicationController

El ReplicationController simplemente garantiza que el número deseado de pods coincide con su selector de etiqueta y que son operacionales.
Actualmente, sólo los pods que han terminado se excluyen de la cuenta. En el futuro, la [disponibilidad](http://issue.k8s.io/620) y otra información disponible en el sistema
se tendrá en cuenta, se añadirá más controles sobre la regla de sussitución, y se está planificando
emitir eventos que podrían ser aprovechados por clientes externos para implementar reglas complejas de sustitución y escalado de forma arbitraria.

El ReplicationController está siempre condicionado a esta reducida responsabilidad.
Él mismo no llevará a cabo ni pruebas de estar listo ni vivo. En vez de aplicar el auto-escalado,
se pretende que este sea realizado por un auto-escalador externo (como se vio en [#492](http://issue.k8s.io/492)), que sería el encargado de cambiar su campo `replicas`.
No se añadirá reglas de programación (por ejemplo, [propagación](http://issue.k8s.io/367#issuecomment-48428019)) al ReplicationController.
Ni se debería validar que los pods controlados coincidan con la plantilla actual especificada, ya que eso obstruiría el auto-calibrado y otros procesos automáticos.
De forma similar, los vencimientos de término, las dependencias de orden, la extensión de la configuración, y otras características se aplican en otro lado.
Incluso se plantea excluir el mecanismo de creación de pods a granel ([#170](http://issue.k8s.io/170)).

El ReplicationController está pensado para ser una primitiva de bloques is intended to be a composable building-block primitive. We expect higher-level APIs and/or tools to be built on top of it and other complementary primitives for user convenience in the future. The "macro" operations currently supported by kubectl (run, scale, rolling-update) are proof-of-concept examples of this. For instance, we could imagine something like [Asgard](http://techblog.netflix.com/2012/06/asgard-web-based-cloud-management-and.html) managing ReplicationControllers, auto-scalers, services, scheduling policies, canaries, etc.


## Objeto API

El ReplicationController es un recurso de alto nivel en la API REST de Kubernetes. Más detalles acerca del
objeto API se pueden encontrar aquí:
[Objeto API ReplicationController](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#replicationcontroller-v1-core).

## Alternativas al ReplicationController

### ReplicaSet

El [`ReplicaSet`](/docs/concepts/workloads/controllers/replicaset/) es el ReplicationController de nueva generación que soporta el nuevo [selector de etiqueta basado en conjunto](/docs/concepts/overview/working-with-objects/labels/#set-based-requirement).
Se usa principalmente por el [`Deployment`](/docs/concepts/workloads/controllers/deployment/) como un mecanismo para orquestrar la creación de pods, la eliminación y las actualizaciones.
Nótese que se recomienda usar Deployments en vez de directamente usar los ReplicaSets, a menos que necesites una orquestración personalizada de actualizaciones o no quieras actualizaciones en absoluto.


### Deployment (Recomendado)

El [`Deployment`](/docs/concepts/workloads/controllers/deployment/) es un objeto de alto nivel de la API que actualiza sus ReplicaSets subyacenetes y sus Pods
de forma similar a cómo lo hace el comando `kubectl rolling-update`. Se recomienda el uso de Deployments si se quiere esta functionalidad de actualización en línea,
porque a diferencia del comando `kubectl rolling-update`, son declarativos, se ejecutan del lado del servidor, y tienen características adicionales.

### Pods simples

A diferencia del caso en que un usuario ha creado directamente pods, un ReplicationController sustituye los pods que han sido eliminador o terminados por cualquier motivo,
como en el caso de un fallo de un nodo o una intervención disruptiva de mantenimiento, como la actualización del kernel.
Por esta razón, se recomienda que se usa un ReplicationController incluso si tu aplicación sólo necesita un único pod.
Piensa que es similar a un supervisor de proceso, sólo que supervisa múltiples pods entre múltiples nodos en vez de
procesos individuales en un único nodo.  Un ReplicationController delega los reinicios locales de
 los contenedores a algún agente del nodo (por ejemplo, Kubelet o Docker).

### Job

Usa un [`Job`](/docs/concepts/jobs/run-to-completion-finite-workloads/) en vez de un ReplicationController para aquellos pods que se espera que terminen por sí mismos
(esto es, trabajos por lotes).

### DaemonSet

Usa un [`DaemonSet`](/docs/concepts/workloads/controllers/daemonset/) en vez de un ReplicationController para aquellos pods que proporcionan
una función a nivel de servidor, como la monitorización o el loggin de servidor. Estos pods tienen un ciclo de vida que está asociado
al del servidor: el pod necesita ejecutarse en el servidor antes que los otros pods arranquen, y es seguro
terminarlo cuando el servidor está listo para reiniciarse/apagarse.

## Para más información

Lee [Ejecutar Aplicaciones sin Estado con un ReplicationController](/docs/tutorials/stateless-application/run-stateless-ap-replication-controller/).




