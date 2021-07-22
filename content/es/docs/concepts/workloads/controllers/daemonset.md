---
title: DaemonSet
content_type: concept
weight: 50
---

<!-- overview -->

Un _DaemonSet_ garantiza que todos (o algunos) de los nodos ejecuten una copia de un Pod.  Conforme se añade más nodos
al clúster, nuevos Pods son añadidos a los mismos.  Conforme se elimina nodos del clúster, dichos Pods se destruyen.
Al eliminar un DaemonSet se limpian todos los Pods que han sido creados.

Algunos casos de uso típicos de un DaemonSet son:

- ejecutar un proceso de almacenamiento en el clúster, como `glusterd`, `ceph`, en cada nodo.
- ejecutar un proceso de recolección de logs en cada nodo, como `fluentd` o `logstash`.
- ejecutar un proceso de monitorización de nodos en cada nodo, como [Prometheus Node Exporter](
  https://github.com/prometheus/node_exporter), [Sysdig Agent] (https://sysdigdocs.atlassian.net/wiki/spaces/Platform), `collectd`, 
  [Dynatrace OneAgent](https://www.dynatrace.com/technologies/kubernetes-monitoring/), 
  [AppDynamics Agent](https://docs.appdynamics.com/display/CLOUD/Container+Visibility+with+Kubernetes), 
  [Datadog agent](https://docs.datadoghq.com/agent/kubernetes/daemonset_setup/), 
  [New Relic agent](https://docs.newrelic.com/docs/integrations/kubernetes-integration/installation/kubernetes-installation-configuration), 
  Ganglia `gmond` o un agente de Instana.

De forma básica, se debería usar un DaemonSet, cubriendo todos los nodos, por cada tipo de proceso.
En configuraciones más complejas se podría usar múltiples DaemonSets para un único tipo de proceso, 
pero con diferentes parámetros y/o diferentes peticiones de CPU y memoria según el tipo de hardware.




<!-- body -->

## Escribir una especificación de DaemonSet

### Crear un DaemonSet

Un DaemonSet se describe por medio de un archivo YAML. Por ejemplo, el archivo `daemonset.yaml` de abajo describe un DaemonSet que ejecuta la imagen Docker de fluentd-elasticsearch:

{{< codenew file="controllers/daemonset.yaml" >}}

* Crear un DaemonSet basado en el archivo YAML:
```
kubectl apply -f https://k8s.io/examples/controllers/daemonset.yaml
```

### Campos requeridos

Como con cualquier otra configuración de Kubernetes, un DaemonSet requiere los campos `apiVersion`, `kind`, y `metadata`.  
Para información general acerca de cómo trabajar con ficheros de configuración, ver los documentos [desplegar aplicaciones](/docs/user-guide/deploying-applications/),
[configurar contenedores](/docs/tasks/), y [gestión de objetos usando kubectl](/docs/concepts/overview/object-management-kubectl/overview/).

Un DaemonSet también necesita un sección [`.spec`](https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status).

### Plantilla Pod

El campo `.spec.template` es uno de los campos obligatorios de la sección `.spec`.

El campo `.spec.template` es una [plantilla Pod](/docs/concepts/workloads/pods/pod-overview/#pod-templates). Tiene exactamente el mismo esquema que un [Pod](/docs/concepts/workloads/pods/pod/), 
excepto por el hecho de que está anidado y no tiene los campos `apiVersion` o `kind`.

Además de los campos obligatorios de un Pod, la plantilla Pod para un DaemonSet debe especificar 
las etiquetas apropiadas (ver [selector de pod](#pod-selector)).

Una plantilla Pod para un DaemonSet debe tener una [`RestartPolicy`](/docs/user-guide/pod-states)
 igual a `Always`, o no indicarse, lo cual asume por defecto el valor `Always`.

### Selector de Pod

El campo `.spec.selector` es un selector de pod. Funciona igual que el campo `.spec.selector` 
de un [Job](/docs/concepts/jobs/run-to-completion-finite-workloads/).

A partir de Kubernetes 1.8, se debe configurar un selector de pod que coincida con las
etiquetas definidas en el `.spec.template`. Así, el selector de pod ya no asume valores por defecto cuando no se indica.
Dichos valores por defecto no eran compatibles con `kubectl apply`. Además, una vez que se ha creado el DaemonSet,
su campo `.spec.selector` no puede alterarse porque, si fuera el caso, ello podría resultar
en Pods huérfanos, lo cual confundiría a los usuarios.

El campo `.spec.selector` es un objeto que, a su vez, consiste en dos campos:

* `matchLabels` - funciona igual que el campo `.spec.selector` de un [ReplicationController](/docs/concepts/workloads/controllers/replicationcontroller/).
* `matchExpressions` - permite construir selectores más sofisticados indicando la clave,
 la lista de valores y un operador para relacionar la clave y los valores.

Cuando se configura ambos campos, el resultado es conjuntivo (AND).

Si se especifica el campo `.spec.selector`, entonces debe coincidir con el campo `.spec.template.metadata.labels`. Aquellas configuraciones que no coinciden, son rechazadas por la API.

Además, normalmente no se debería crear ningún Pod con etiquetas que coincidan con el selector, bien sea de forma directa, via otro 
DaemonSet, o via otro controlador como un ReplicaSet.  De ser así, el controlador del DaemonSet
pensará que dichos Pods fueron en realidad creados por él mismo. Kubernetes, en cualquier caso, no te impide realizar esta 
operación. Un caso donde puede que necesites hacer esto es cuando quieres crear manualmente un Pod con un valor diferente en un nodo para pruebas.

### Ejecutar Pods sólo en algunos Nodos

Si se configura un `.spec.template.spec.nodeSelector`, entonces el controlador del DaemonSet
 creará los Pods en aquellos nodos que coincidan con el [selector de nodo](/docs/concepts/configuration/assign-pod-node/) indicado. 
 De forma similar, si se configura una `.spec.template.spec.affinity`,
entonces el controlador del DaemonSet creará los Pods en aquellos nodos que coincidan con la [afinidad de nodo](/docs/concepts/configuration/assign-pod-node/) indicada.
Si no se configura ninguno de los dos, entonces el controlador del DaemonSet creará los Pods en todos los nodos.

## Cómo se planifican los Pods procesos

### Planificados por el controlador del DaemonSet (deshabilitado por defecto a partir de 1.12)

Normalmente, el planificador de Kubernetes determina la máquina donde se ejecuta un Pod. Sin embargo, los Pods
creados por el controlador del DaemonSet ya tienen la máquina seleccionada (puesto que cuando se crea el Pod,
se indica el campo `.spec.nodeName`, y por ello el planificador los ignora). Por lo tanto:

 - El controlador del DaemonSet no tiene en cuenta el campo [`unschedulable`](/docs/admin/node/#manual-node-administration) de un nodo.
 - El controlador del DaemonSet puede crear Pods incluso cuando el planificador no ha arrancado, lo cual puede ayudar en el arranque del propio clúster.


### Planificados por el planificador por defecto de Kubernetes (habilitado por defecto desde 1.12)

{{< feature-state state="beta" for-kubernetes-version="1.12" >}}

Un DaemonSet garantiza que todos los nodos elegibles ejecuten una copia de un Pod. 
Normalmente, es el planificador de Kubernetes quien determina el nodo donde se ejecuta un Pod. Sin embargo,
los pods del DaemonSet son creados y planificados por el mismo controlador del DaemonSet.
Esto introduce los siguientes inconvenientes:

 * Comportamiento inconsistente de los Pods: Los Pods normales que están esperando
 a ser creados, se encuentran en estado `Pending`, pero los pods del DaemonSet no pasan por el estado `Pending`. 
 Esto confunde a los usuarios.
 * La [prioridad y el comportamiento de apropiación de Pods](/docs/concepts/configuration/pod-priority-preemption/)
   se maneja por el planificador por defecto. Cuando se habilita la contaminación, el controlador del DaemonSet
   tomará la decisiones de planificación sin considerar ni la prioridad ni la contaminación del pod.

`ScheduleDaemonSetPods` permite planificar DaemonSets usando el planificador por defecto
en vez del controlador del DaemonSet, añadiendo la condición `NodeAffinity`
a los pods del DaemonSet, en vez de la condición `.spec.nodeName`. El planificador por defecto
se usa entonces para asociar el pod a su servidor destino. Si la afinidad de nodo del 
pod del DaemonSet ya existe, se sustituye. El controlador del DaemonSet sólo realiza
estas operaciones cuando crea o modifica los pods del DaemonSet, y no se realizan cambios
al `spec.template` del DaemonSet.

```yaml
nodeAffinity:
  requiredDuringSchedulingIgnoredDuringExecution:
    nodeSelectorTerms:
    - matchFields:
      - key: metadata.name
        operator: In
        values:
        - target-host-name
```

Adicionalmente, se añade de forma automática la tolerancia `node.kubernetes.io/unschedulable:NoSchedule` 
a los Pods del DaemonSet. Así, el planificador por defecto ignora los nodos
`unschedulable` cuando planifica los Pods del DaemonSet.


### Contaminaciones (taints) y Tolerancias (tolerations)

A pesar de que los Pods de proceso respetan las
[contaminaciones y tolerancias](/docs/concepts/configuration/taint-and-toleration),
la siguientes tolerancias son añadidas a los Pods del DaemonSet de forma automática
según las siguientes características:

| Clave de tolerancia                          | Efecto     | Versión | Descripción                                                  |
| ---------------------------------------- | ---------- | ------- | ------------------------------------------------------------ |
| `node.kubernetes.io/not-ready`           | NoExecute  | 1.13+    | Los pods del DaemonSet no son expulsados cuando hay problemas de nodo como una partición de red. |
| `node.kubernetes.io/unreachable`         | NoExecute  | 1.13+    | Los pods del DaemonSet no son expulsados cuando hay problemas de nodo como una partición de red. |
| `node.kubernetes.io/disk-pressure`       | NoSchedule | 1.8+    | Los pods del DaemonSet no son expulsados cuando hay problemas de nodo como la falta de espacio en disco. |
| `node.kubernetes.io/memory-pressure`     | NoSchedule | 1.8+    | Los pods del DaemonSet no son expulsados cuando hay problemas de nodo como la falta de memoria. |
| `node.kubernetes.io/unschedulable`       | NoSchedule | 1.12+   | Los pods del DaemonSet toleran los atributos unschedulable del planificador por defecto.                                                    |
| `node.kubernetes.io/network-unavailable` | NoSchedule | 1.12+   | Los pods del DaemonSet, que usan la red del servidor anfitrión, toleran los atributos network-unavailable del planificador por defecto.                      |


## Comunicarse con los Pods de los DaemonSets

Algunos patrones posibles para la comunicación con los Pods de un DaemonSet son:

- **Push**: Los Pods del DaemonSet se configuran para enviar actualizaciones a otro servicio, 
como una base de datos de estadísticas. No tienen clientes.
- **NodeIP y Known Port**: Los Pods del DaemonSet pueden usar un `hostPort`, de forma que se les puede alcanzar via las IPs del nodo. Los clientes conocen la lista de IPs del nodo de algún modo, 
y conocen el puerto acordado.
- **DNS**: Se crea un [servicio headless](/docs/concepts/services-networking/service/#headless-services) con el mismo selector de pod,
  y entonces se descubre a los DaemonSets usando los recursos `endpoints` o mediante múltiples registros de tipo A en el DNS.
- **Service**: Se crea un servicio con el mismo selector de Pod, y se usa el servicio para llegar al proceso de uno de los nodos. (No hay forma de determinar el nodo exacto.)

## Actualizar un DaemonSet

Si se cambian las etiquetas de nodo, el DaemonSet comenzará de forma inmediata a añadir Pods a los nuevos nodos que coincidan y a eliminar
los Pods de aquellos nuevos nodos donde no coincidan.

Puedes modificar los Pods que crea un DaemonSet. Sin embargo, no se permite actualizar todos los campos de los Pods. 
 Además, el controlador del DaemonSet utilizará la plantilla original la próxima vez que se cree un nodo (incluso con el mismo nombre).

Puedes eliminar un DaemonSet. Si indicas el parámetro `--cascade=orphan` al usar `kubectl`, 
entonces los Pods continuarán ejecutándose en los nodos. Así, puedes crear entonces un nuevo DaemonSet con una plantilla diferente.
El nuevo DaemonSet con la plantilla diferente reconocerá a todos los Pods existentes que tengan etiquetas coincidentes y
no modificará o eliminará ningún Pod aunque la plantilla no coincida con los Pods desplegados.
Entonces, deberás forzar la creación del nuevo Pod eliminando el Pod mismo o el nodo.

A partir de las versión 1.6 de Kubernetes, puedes [llevar a cabo una actualización continua](/docs/tasks/manage-daemon/update-daemon-set/) en un DaemonSet.

## Alternativas al DaemonSet

### Secuencias de comandos de inicialización 

Aunque es perfectamente posible ejecutar procesos arrancándolos directamente en un nodo (ej. usando
`init`, `upstartd`, o `systemd`), existen numerosas ventajas si se realiza via un DaemonSet:

- Capacidad de monitorizar y gestionar los logs de los procesos del mismo modo que para las aplicaciones.
- Mismo lenguaje y herramientas de configuración (ej. plantillas de Pod, `kubectl`) tanto para los procesos como para las aplicaciones.
- Los procesos que se ejecutan en contenedores con límitaciones de recursos aumentan el aislamiento entre dichos procesos y el resto de contenedores de aplicaciones. 
  Sin embargo, esto también se podría conseguir ejecutando los procesos en un contenedor en vez de un Pod
  (ej. arrancarlos directamente via Docker).

### Pods individuales

Es posible crear Pods directamente sin indicar el nodo donde ejecutarse. Sin embargo,
la ventaja del DaemonSet es que sustituye los Pods que se eliminan o terminan por cualquier razón, como en el caso
de un fallo del nodo o una intervención disruptiva de mantenimiento del nodo, como la actualización del kernel.
Por esta razón, deberías siempre utilizar un DaemonSet en vez de crear Pods individuales.

### Pods estáticos

Es posible crear Pods a partir de archivos en el directorio donde está escuchando el proceso Kubelet.
Este tipo de Pods se denomina [pods estáticos](/docs/concepts/cluster-administration/static-pod/).
A diferencia del DaemonSet, los Pods estáticos no se pueden gestionar con kubectl
o cualquier otro cliente de la API de Kubernetes. Los Pods estáticos no dependen del apiserver, lo cual los hace
convenientes para el arranque inicial del clúster. Además, puede que los Pods estáticos se deprecien en el futuro.

### Deployments

Los DaemonSets son similares a los [Deployments](/docs/concepts/workloads/controllers/deployment/) en el sentido que
ambos crean Pods, y que dichos Pods tienen procesos que no se espera que terminen (ej. servidores web,
servidores de almacenamiento).

Utiliza un Deployment para definir servicios sin estado, como las interfaces de usuario, donde el escalado vertical y horizontal
del número de réplicas y las actualizaciones continuas son mucho más importantes que el control exacto del servidor donde se ejecuta el Pod. 
Utiliza un DaemonSet cuando es importante que una copia de un Pod siempre se ejecute en cada uno de los nodos, 
y cuando se necesite que arranque antes que el resto de Pods.


