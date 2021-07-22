---
title: Jobs - Ejecución hasta el final
content_type: concept
feature:
  title: Ejecución en lotes
  description: >
    Además de los servicios, Kubernetes puede gestionar tus trabajos por lotes y CI, sustituyendo los contenedores que fallen, si así se desea.
weight: 70
---

<!-- overview -->

Un Job crea uno o más Pods y se asegura de que un número específico de ellos termina de forma satisfactoria.
Conforme los pods terminan satisfactoriamente, el Job realiza el seguimiento de las ejecuciones satisfactorias.
Cuando se alcanza un número específico de ejecuciones satisfactorias, la tarea (esto es, el Job) se completa.
Al eliminar un Job se eliminan los Pods que haya creado.

Un caso simple de uso es crear un objeto Job para que se ejecute un Pod de manera fiable hasta el final.
El objeto Job arrancará un nuevo Pod si el primer Pod falla o se elimina (por ejemplo
como consecuencia de un fallo de hardware o un reinicio en un nodo).

También se puede usar un Job para ejecutar múltiples Pods en paralelo.




<!-- body -->

## Ejecutar un Job de ejemplo

Aquí se muestra un ejemplo de configuración de Job. Este ejemplo calcula los primeros 2000 decimales de π y los imprime por pantalla.
Tarda unos 10s en completarse.

{{< codenew file="controllers/job.yaml" >}}

Puedes ejecutar el ejemplo con este comando:

```shell
kubectl apply -f https://k8s.io/examples/controllers/job.yaml
```
```
job "pi" created
```

Comprueba el estado del Job con `kubectl`:

```shell
kubectl describe jobs/pi
```
```
Name:             pi
Namespace:        default
Selector:         controller-uid=b1db589a-2c8d-11e6-b324-0209dc45a495
Labels:           controller-uid=b1db589a-2c8d-11e6-b324-0209dc45a495
                  job-name=pi
Annotations:      <none>
Parallelism:      1
Completions:      1
Start Time:       Tue, 07 Jun 2016 10:56:16 +0200
Pods Statuses:    0 Running / 1 Succeeded / 0 Failed
Pod Template:
  Labels:       controller-uid=b1db589a-2c8d-11e6-b324-0209dc45a495
                job-name=pi
  Containers:
   pi:
    Image:      perl
    Port:
    Command:
      perl
      -Mbignum=bpi
      -wle
      print bpi(2000)
    Environment:        <none>
    Mounts:             <none>
  Volumes:              <none>
Events:
  FirstSeen    LastSeen    Count    From            SubobjectPath    Type        Reason            Message
  ---------    --------    -----    ----            -------------    --------    ------            -------
  1m           1m          1        {job-controller }                Normal      SuccessfulCreate  Created pod: pi-dtn4q
```

Para ver los Pods de un Job que se han completado, usa `kubectl get pods`.

Para listar todos los Pods que pertenecen a un Job de forma que sea legible, puedes usar un comando como:

```shell
pods=$(kubectl get pods --selector=job-name=pi --output=jsonpath='{.items[*].metadata.name}')
echo $pods
```
```
pi-aiw0a
```

En este caso, el selector es el mismo que el selector del Job. La opción `--output=jsonpath` indica un expresión
que simplemente obtiene el nombre de cada Pod en la lista devuelta.

Mira la salida estándar de uno de los Pods:

```shell
$ kubectl logs $pods
3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679821480865132823066470938446095505822317253594081284811174502841027019385211055596446229489549303819644288109756659334461284756482337867831652712019091456485669234603486104543266482133936072602491412737245870066063155881748815209209628292540917153643678925903600113305305488204665213841469519415116094330572703657595919530921861173819326117931051185480744623799627495673518857527248912279381830119491298336733624406566430860213949463952247371907021798609437027705392171762931767523846748184676694051320005681271452635608277857713427577896091736371787214684409012249534301465495853710507922796892589235420199561121290219608640344181598136297747713099605187072113499999983729780499510597317328160963185950244594553469083026425223082533446850352619311881710100031378387528865875332083814206171776691473035982534904287554687311595628638823537875937519577818577805321712268066130019278766111959092164201989380952572010654858632788659361533818279682303019520353018529689957736225994138912497217752834791315155748572424541506959508295331168617278558890750983817546374649393192550604009277016711390098488240128583616035637076601047101819429555961989467678374494482553797747268471040475346462080466842590694912933136770289891521047521620569660240580381501935112533824300355876402474964732639141992726042699227967823547816360093417216412199245863150302861829745557067498385054945885869269956909272107975093029553211653449872027559602364806654991198818347977535663698074265425278625518184175746728909777727938000816470600161452491921732172147723501414419735685481613611573525521334757418494684385233239073941433345477624168625189835694855620992192221842725502542568876717904946016534668049886272327917860857843838279679766814541009538837863609506800642251252051173929848960841284886269456042419652850222106611863067442786220391949450471237137869609563643719172874677646575739624138908658326459958133904780275901
```

## Escribir una especificación de Job

Como con el resto de configuraciones de Kubernetes, un Job necesita los campos `apiVersion`, `kind`, y `metadata`.

Un Job también necesita la [sección `.spec`](https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status).

### Plantilla Pod

El campo `.spec.template` es el único campo obligatorio de `.spec`.

El campo `.spec.template` es una [plantilla Pod](/docs/concepts/workloads/pods/pod-overview/#pod-templates). Tiene exactamente el mismo esquema que un [pod](/docs/user-guide/pods), 
excepto por el hecho de que está anidado y no tiene el campo `apiVersion` o `kind`.

Además de los campos olbigatorios de un Pod, una plantilla Pod de un Job debe indicar las etiquetas apropiadas
(ver [selector de pod](#pod-selector)) y una regla de reinicio apropiada.

Sólo se permite los valores `Never` o `OnFailure` para [`RestartPolicy`](/docs/concepts/workloads/pods/pod-lifecycle/#restart-policy).

### Selector de Pod

El campo `.spec.selector` es opcional. En la práctica mayoría de los casos no deberías configurarlo.
Mira la sección sobre [configurar tu propio selector de pod](#specifying-your-own-pod-selector).


### Jobs en paralelo

Hay tres tipos principales de tarea aptos para ejecutarse como un Job:

1. Jobs no paralelos
  - normalmente, sólo se arranca un Pod, a menos que el Pod falle.
  - el Job se completa tan pronto como su Pod termine de forma satisfactoria.
1. Jobs en paralelo con un *cupo fijo de terminación*:
  - se configura un valor positivo distinto de cero para el campo `.spec.completions`.
  - el Job representa la tarea en general, y se completa cuando hay una ejecución satisfactoria de un Pod por cada valor dentro del rango de 1 a `.spec.completions`.
  - **no implementado todavía:** A cada Pod se le pasa un índice diferenente dentro del rango de 1 a `.spec.completions`.
1. Jobs en paralelo con una *cola de trabajo*:
  - no se especifica el campo `.spec.completions`, por defecto `.spec.parallelism`.
  - los Pods deben coordinarse entre ellos mismos o a través de un servicio externo que determine quién debe trabajar en qué. 
    Por ejemplo, un Pod podría ir a buscar un lote de hasta N ítems de una cola de trabajo.
  - cada Pod es capaz de forma independiente de determinar si sus compañeros han terminado o no, y como consecuencia el Job entero ha terminado.
  - cuando _cualquier_ Pod del Job termina con éxito, no se crean nuevos Pods.
  - una vez que al menos uno de los Pods ha terminado con éxito y todos los Pods han terminado, entonces el Job termina con éxito.
  - una vez que cualquier Pod ha terminado con éxito, ningún otro Pod debería continuar trabajando en la misma tarea o escribiendo ningún resultado. Todos ellos deberían estar en proceso de terminarse.

En un Job _no paralelo_, no debes indicar el valor de `.spec.completions` ni `.spec.parallelism`. Cuando ambos se dejan
 sin valor, ambos se predeterminan a 1.

En un Job con _cupo fijo de terminación_, deberías poner el valor de `.spec.completions` al número de terminaciones que se necesiten.
Puedes dar un valor a `.spec.parallelism`, o dejarlo sin valor, en cuyo caso se predetermina a 1.

En un Job con _cola de trabajo_, no debes indicar el valor de `.spec.completions`, y poner el valor de `.spec.parallelism` a
un entero no negativo.

Para más información acerca de cómo usar los distintos tipos de Job, ver la sección de [patrones de job](#job-patterns).


#### Controlar el paralelismo

El paralelismo solicitado (`.spec.parallelism`) puede usar cualquier valor no negativo.
Si no se indica, se predeterminad a 1.
Si se indica como 0, entonces el Job se pausa de forma efectiva hasta que se incremente.

El paralelismo actual (número de pods ejecutándose en cada momento) puede que sea mayor o menor que el solicitado, 
por los siguientes motivos:

- Para los Jobs con _cupo fijo de terminaciones_, el número actual de pods ejecutándose en paralelo no excede el número de terminaciones pendientes.
  Los valores superiores de `.spec.parallelism` se ignoran.
- Para los Jobs con _cola de trabajo_, no se arranca nuevos Pods después de que cualquier Pod se haya completado -- sin embargo, se permite que se completen los Pods pendientes.
- Cuando el controlador no ha tenido tiempo para reaccionar.
- Cuando el controlador no pudo crear los Pods por el motivo que fuera (falta de `ResourceQuota`, falta de permisos, etc.),
  entonces puede que haya menos pods que los solicitados.
- El controlador puede que regule la creación de nuevos Pods debido al excesivo número de fallos anteriores en el mismo Job.
- Cuando un Pod se para de forma controlada, lleva tiempo pararlo.

## Gestionar Fallos de Pod y Contenedor

Un contenedor de un Pod puede fallar por cualquier motivo, como porque el proceso que se estaba ejecutando termina con un código de salida distinto de cero, 
o porque se mató el contenedor por exceder un límite de memoria, etc. Si esto ocurre, y se tiene
`.spec.template.spec.restartPolicy = "OnFailure"`, entonces el Pod permance en el nodo,
pero el contenedor se vuelve a ejecutar. Por lo tanto, tu aplicación debe poder gestionar el caso en que se reinicia de forma local,
o bien especificar `.spec.template.spec.restartPolicy = "Never"`.
Ver el [ciclo de vida de un pod](/docs/concepts/workloads/pods/pod-lifecycle/#example-states) para más información sobre `restartPolicy`.

Un Pod entero puede también fallar por cualquier motivo, como cuando se expulsa al Pod del nodo
(porque el nodo se actualiza, reinicia, elimina, etc.), o si un contenedor del Pod falla
cuando `.spec.template.spec.restartPolicy = "Never"`. Cuando un Pod falla, entonces el controlador del Job
arranca un nuevo Pod. Esto quiere decir que tu aplicación debe ser capaz de gestionar el caso en que se reinicia en un nuevo pod.
En particular, debe ser capaz de gestionar los ficheros temporales, los bloqueos, los resultados incompletos, y cualquier otra dependencia
de ejecuciones previas.

Nótese que incluso si se configura `.spec.parallelism = 1` y `.spec.completions = 1` y
`.spec.template.spec.restartPolicy = "Never"`, el mismo programa puede arrancarse dos veces.

Si se especifica `.spec.parallelism` y `.spec.completions` con valores mayores que 1, 
entonces puede que haya múltiples pods ejecutándose a la vez. Por ello, tus pods deben tolerar la concurrencia.

### Regla de retroceso de Pod por fallo

Hay situaciones en que quieres que el Job falle después de intentar ejecutarlo unas cuantas veces debido
a un error lógico en la configuración, etc.
Para hacerlo, pon el valor de `.spec.backoffLimit` al número de reintentos que quieres
antes de considerar el Job como fallido. El límite de retroceso se predetermina a 6. 
Los Pods fallidos asociados al Job son recreados por el controlador del Job con un
retroceso exponencial (10s, 20s, 40s ...) limitado a seis minutos. El contador
de retroceso se resetea si no aparecen Pods fallidos antes del siguiente chequeo de estado del Job.

{{< note >}}
El problema [#54870](https://github.com/kubernetes/kubernetes/issues/54870) todavía existe en las versiones de Kubernetes anteriores a la versión 1.12
{{< /note >}}

## Terminación y Limpieza de un Job

Cuando un Job se completa, ya no se crea ningún Pod, pero tampoco se elimina los Pods. Guardarlos permite
ver todavía los logs de los pods acabados para comprobar errores, avisos, o cualquier otro resultado de diagnóstico.
El objeto job también se conserva una vez que se ha completado para que se pueda ver su estado. Es decisión del usuario si elimina
los viejos jobs después de comprobar su estado. Eliminar el job con el comando `kubectl` (ej. `kubectl delete jobs/pi` o `kubectl delete -f ./job.yaml`). 
Cuando eliminas un job usando el comando `kubectl`, todos los pods que creó se eliminan también.

Por defecto, un Job se ejecutará de forma ininterrumpida a menos que uno de los Pods falle, en cuyo caso el Job se fija en el valor de
`.spec.backoffLimit` descrito arriba. Otra forma de acabar un Job es poniéndole un vencimiento activo.
Haz esto poniendo el valor del campo `.spec.activeDeadlineSeconds` del Job a un número de segundos.

El campo `activeDeadlineSeconds` se aplica a la duración del job, independientemente de cuántos Pods se hayan creado.
Una vez que el Job alcanza `activeDeadlineSeconds`, se terminan todos sus Pods y el estado del Job se pone como `type: Failed` con `reason: DeadlineExceeded`.

Fíjate que el campo `.spec.activeDeadlineSeconds` de un Job tiene precedencia sobre el campo `.spec.backoffLimit`. 
Por lo tanto, un Job que está reintentando uno o más Pods fallidos no desplegará nuevos Pods una vez que alcance el límite de tiempo especificado por `activeDeadlineSeconds`, 
incluso si todavía no se ha alcanzado el `backoffLimit`.

Ejemplo:

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: pi-with-timeout
spec:
  backoffLimit: 5
  activeDeadlineSeconds: 100
  template:
    spec:
      containers:
      - name: pi
        image: perl
        command: ["perl",  "-Mbignum=bpi", "-wle", "print bpi(2000)"]
      restartPolicy: Never
```

Fíjate que tanto la especificación del Job como la [especificación de la plantilla Pod](/docs/concepts/workloads/pods/init-containers/#detailed-behavior) 
dentro del Job tienen un campo `activeDeadlineSeconds`. Asegúrate que pones el valor de este campo de forma adecuada.

## Limpiar los Jobs terminados automáticamente

Normalmente, los Jobs que han terminado ya no se necesitan en el sistema. Conservarlos sólo añade
más presión al servidor API. Si dichos Jobs no se gestionan de forma directa por un controlador de más alto nivel, 
como los [CronJobs](/docs/concepts/workloads/controllers/cron-jobs/), los Jobs pueden
limpiarse por medio de CronJobs en base a la regla de limpieza basada en capacidad que se haya especificado.

### Mecanismo TTL para Jobs terminados

{{< feature-state for_k8s_version="v1.12" state="alpha" >}}

Otra forma de limpiar los Jobs terminados (bien `Complete` o `Failed`)
de forma automática es usando un mecanismo TTL proporcionado por un
[controlador TTL](/docs/concepts/workloads/controllers/ttlafterfinished/) de recursos finalizados, 
indicando el valor `.spec.ttlSecondsAfterFinished` del Job.

Cuando el controlador TTL limpia el Job, lo eliminará en cascada,
esto es, eliminará sus objetos subordinados, como Pods, junto con el Job. Nótese
que cuando se elimina el Job, sus garantías de ciclo de vida, como los finalizadores,
se tendrán en cuenta.

Por ejemplo:

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: pi-with-ttl
spec:
  ttlSecondsAfterFinished: 100
  template:
    spec:
      containers:
      - name: pi
        image: perl
        command: ["perl",  "-Mbignum=bpi", "-wle", "print bpi(2000)"]
      restartPolicy: Never
```

Aquí el Job `pi-with-ttl` será candidato a ser automáticamente eliminado, `100`
segundos después de que termine.

Si el campo se pone a `0`, el Job será candidato a ser automáticamente eliminado
inmediatamente después de haber terminado. Si no se pone valor al campo, este Job no será eliminado
por el controlador TTL una vez concluya.

Nótese que este mecanismo TTL está todavía en alpha, a través de la característica denominada `TTLAfterFinished`. 
Para más información, ver la documentación del [controlador TTL](/docs/concepts/workloads/controllers/ttlafterfinished/) para
recursos terminados.

## Patrones de Job

El objeto Job puede usarse para dar soporte a la ejecución fiable de Pods en paralelo. El objeto Job
no se diseñó para dar soporte a procesos paralelos estrechamente comunicados, como los que comúnmente
se encuentran en la computación científica. Eso sí, permite el proceso paralelo de un conjunto de *ítems de trabajo* independientes, pero relacionados entre sí.
Estos pueden ser correos a enviar, marcos a renderizar, archivos a codificar, rangos de claves en una base de datos NoSQL a escanear, y demás.

En un sistema complejo, puede haber múltiples diferentes conjuntos de ítems de trabajo. Aquí sólo se está
considerando un conjunto de ítems de trabajo que el usuario quiere gestionar de forma conjunta &mdash; un *proceso por lotes*.

Hay varios patrones diferentes para computación en paralelo, cada uno con sus fortalezas y sus debilidades.
Los sacrificios a tener en cuenta son:

- Un objeto Job para cada ítem de trabajo vs. un objeto Job simple para todos los ítems de trabajo. El último es mejor
  para grandes números de ítems de trabajo. El primero añade sobrecarga para el usuario y para el sistema
  al tener que gestionar grandes números de objetos Job.
- El número de pods creados es igual al número de ítems de trabajo vs. cada Pod puede procesar múltiplese ítems de trabajo.
  El primero típicamente requiere menos modificaciones al código existente y a los contenedores.
  El último es mejor cuanto mayor sea el número de ítems de trabajo, por las mismas razones que antes..
- Varios enfoques usan una cola de trabajo.  Ello requiere ejecutar un servicio de colas,
  y modificaciones a las aplicaciones o contenedores existentes para que hagan uso de la cola de trabajo.
  Otras estrategias son más fáciles de adaptar a una aplicación ya usando contenedores.


Los sacrificios a tener en cuenta se indican a continuación, donde las columnas 2 a 4 representan los sacrificios de arriba.
Los nombres de los patrones son también enlaces a ejemplos e información más detallada.

|                            Patrón                                   | Objeto Job simple | ¿Menos pods que ítems de trabajo? | ¿No modificar la aplicación? |  ¿Funciona en Kube 1.1? |
| -------------------------------------------------------------------- |:-----------------:|:---------------------------:|:-------------------:|:-------------------:|
| [Extensión de la Plantilla Job](/docs/tasks/job/parallel-processing-expansion/)            |                   |                             |          ✓          |          ✓          |
| [Cola con Pod por Ítem de Trabajo](/docs/tasks/job/coarse-parallel-processing-work-queue/)   |         ✓         |                             |      a veces      |          ✓          |
| [Cola con Cuenta Variable de Pods](/docs/tasks/job/fine-parallel-processing-work-queue/)  |         ✓         |             ✓               |                     |          ✓          |
| Job simple con Asignación Estática de Trabajo                               |         ✓         |                             |          ✓          |                     |

Cuando se especifican terminaciones con `.spec.completions`, cada Pod creado por el controlado del Job
tiene un [`spec`](https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status)idéntico.
Esto significa que todos los pods de una tarea tendrán la misma línea de comandos y la
misma imagne, los mismo volúmenes, y (casi) las mismas variables de entorno.
Estos patrones otorgan diferentes formas de organizar los pods para que trabajen en cosas distintas.

Esta tabla muestra la configuración necesaria para `.spec.parallelism` y `.spec.completions` para cada uno de los patrones.
Aquí, `T` es el número de ítems de trabajo.

|                             Patrón                                  | `.spec.completions` |  `.spec.parallelism` |
| -------------------------------------------------------------------- |:-------------------:|:--------------------:|
| [Extensión de la Plantilla Job](/docs/tasks/job/parallel-processing-expansion/)           |          1          |     debería ser 1      |
| [Cola con Pod por Ítem de Trabajo](/docs/tasks/job/coarse-parallel-processing-work-queue/)   |          T          |        cualquiera           |
| [Cola con Cuenta Variable de Pods](/docs/tasks/job/fine-parallel-processing-work-queue/)  |          1          |        cualquiera           |
| Job simple con Asignación Estática de Trabajo                                |          T          |        cualquiera           |


## Uso Avanzado

### Especificar tu propio selector de pod 

Normalmente, cuando creas un objeto Job, no especificas el campo `.spec.selector`.
La lógica por defecto del sistema añade este campo cuando se crea el Job.
Se elige un valor de selector que no se entremezcle con otras tareas.

Sin embargo, en algunos casos, puede que necesites sobreescribir este selector que se configura de forma automática.
Para ello, puedes indicar el valor de `.spec.selector` en el Job.

Pero ten mucho cuidado cuando lo hagas. Si configuras un selector de etiquta que no
 es único para los pods de ese Job, y que selecciona Pods que no tienen que ver, 
 entonces estos últimos pueden ser eliminados, o este Job puede contar los otros
 Pods para terminarse, o uno o ambos Jobs pueden negarse a crear Pods o ejecutarse hasta el final.
 Si se elige un selector que no es único, entonces otros controladores (ej. ReplicationController) 
 y sus Pods puede comportarse de forma impredecibles también. Kubernetes no te impide cometer un error 
 especificando el `.spec.selector`.

Aquí se muestra un ejemplo de un caso en que puede que necesites usar esta característica.

Digamos que el Job `viejo` todavía está ejeuctándose. Quieres que los Pods existentes
sigan corriendo, pero quieres que el resto de los Pods que se creen
usen una plantilla pod diferente y que el Job tenga un nombre nuevo.
Como no puedes modificar el Job porque esos campos no son modificables, eliminas el Job `old`,
 pero _dejas sus pods ejecutándose_ mediante el comando `kubectl delete jobs/old --cascade=orphan`.
Antes de eliminarlo, apúntate el selector actual que está usando:

```
kind: Job
metadata:
  name: viejo
  ...
spec:
  selector:
    matchLabels:
      job-uid: a8f3d00d-c6d2-11e5-9f87-42010af00002
  ...
```

Entonces, creas un nuevo Job con el nombre `nuevo` y le configuras explícitamente el mismo selector.
Puesto que los Pods existentes tienen la etiqueta `job-uid=a8f3d00d-c6d2-11e5-9f87-42010af00002`,
son controlados por el Job `nuevo` igualmente.

Necesitas configurar `manualSelector: true` en el nuevo Job, ya qye no estás usando
 el selector que normalmente se genera de forma automática por el sistema.

```
kind: Job
metadata:
  name: nuevo
  ...
spec:
  manualSelector: true
  selector:
    matchLabels:
      job-uid: a8f3d00d-c6d2-11e5-9f87-42010af00002
  ...
```

El mismo Job nuevo tendrá un uid distinto a `a8f3d00d-c6d2-11e5-9f87-42010af00002`.
Poniendo `manualSelector: true` le dice al sistema que sabes lo que estás haciendo
 y que te permita hacer este desajuste.

## Alternativas

### Pods simples

Cuando el nodo donde un Pod simple se estaba ejecutando se reinicia o falla, dicho pod se termina
y no será reinicado. Sin embargo, un Job creará nuevos Pods para sustituir a los que se han terminando.
Por esta razón, se recomienda que se use un Job en vez de un Pod simple, incluso si tu aplicación
sólo necesita un único Pod.

### Replication Controller

Los Jobs son complementarios a los [Replication Controllers](/docs/user-guide/replication-controller).
Un Replication Controller gestiona aquellos Pods que se espera que no terminen (ej. servidores web), y un Job
gestiona aquellos Pods que se espera que terminen (ej. tareas por lotes).

Como se discutió en el [Ciclo de vida de un Pod](/docs/concepts/workloads/pods/pod-lifecycle/), un `Job` *sólo* es apropiado
para aquellos pods con `RestartPolicy` igual a `OnFailure` o `Never`.
(Nota: Si `RestartPolicy` no se pone, el valor predeterminado es `Always`.)

### Job simple arranca que arranca un controlador de Pod

Otro patrón es aquel donde un Job simple crea un Pod que, a su vez, crea otros Pods, actuando como una especie
de controlador personalizado para esos Pods. Esto da la máxima flexibilidad, pero puede que
cueste un poco más de entender y ofrece menos integración con Kubernetes.

Un ejemplo de este patrón sería un Job que arranca un Pod que ejecuta una secuencia de comandos que, a su vez,
arranca un controlador maestro de Spark (ver el [ejemplo de spark](https://github.com/kubernetes/examples/tree/{{< param "githubbranch" >}}/staging/spark/README.md)), 
ejecuta un manejador de spark, y a continuación lo limpia todo.

Una ventaja de este enfoque es que el proceso general obtiene la garantía del objeto Job,
además del control completo de los Pods que se crean y cómo se les asigna trabajo.

## Cron Jobs {#cron-jobs}

Puedes utilizar un [`CronJob`](/docs/concepts/workloads/controllers/cron-jobs/) para crear un Job que se ejecute en una hora/fecha determinadas, de forma similar
a la herramienta `cron` de Unix.


