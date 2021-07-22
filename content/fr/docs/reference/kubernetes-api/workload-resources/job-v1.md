---
api_metadata:
  apiVersion: "batch/v1"
  import: "k8s.io/api/batch/v1"
  kind: "Job"
content_type: "api_reference"
description: "Job représente la configuration d'un seul job."
title: "Job"
weight: 10
auto_generated: true
---

<!--
The file is auto-generated from the Go source code of the component using a generic
[generator](https://github.com/kubernetes-sigs/reference-docs/). To learn how
to generate the reference documentation, please read
[Contributing to the reference documentation](/docs/contribute/generate-ref-docs/).
To update the reference content, please follow the 
[Contributing upstream](/docs/contribute/generate-ref-docs/contribute-upstream/)
guide. You can file document formatting bugs against the
[reference-docs](https://github.com/kubernetes-sigs/reference-docs/) project.
-->

`apiVersion: batch/v1`

`import "k8s.io/api/batch/v1"`


## Job {#Job}

Job représente la configuration d'un seul job.

<hr>

- **apiVersion**: batch/v1


- **kind**: Job


- **metadata** (<a href="{{< ref "../common-definitions/object-meta#ObjectMeta" >}}">ObjectMeta</a>)

  Meta-données standard d'objet. Plus d'infos : https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

- **spec** (<a href="{{< ref "../workload-resources/job-v1#JobSpec" >}}">JobSpec</a>)

  Spécifications du comportement désiré d'un job. Plus d'infos : https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status

- **status** (<a href="{{< ref "../workload-resources/job-v1#JobStatus" >}}">JobStatus</a>)

  Statut courant d'un job. Plus d'infos : https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status





## JobSpec {#JobSpec}

JobSpec décrit à quoi ressemblera l'exécution du job.

<hr>



### Replicas


- **template** (<a href="{{< ref "../workload-resources/pod-template-v1#PodTemplateSpec" >}}">PodTemplateSpec</a>), requis

  Décrit le Pod qui sera créé lors de l'exécution d'unJob. Plus d'infos : https://kubernetes.io/docs/concepts/workloads/controllers/jobs-run-to-completion/

- **parallelism** (int32)

  Spécifie le nombre maximum désiré de Pods que le Job doit exécuter à n'importe quel moment. Le nombre effectif de Pods s'exécutant en état stationnaire sera inférieur à ce nombre lorsque ((.spec.completions - .status.successful) \< .spec.parallelism), c'est-à-dire lorsque le travail restant à exécuter est inférieur au parallèlisme maximal. Plus d'infos : https://kubernetes.io/docs/concepts/workloads/controllers/jobs-run-to-completion/

### Lifecycle


- **completions** (int32)

  Spécifie le nombre désiré de pods terminés avec succès que le job doit exécuter.  Une valeur nil indique que le succès de n'importe quel pod signale le succès de tous les pods, et permet à parallelism d'avoir n'importe quelle valeur.  Une valeur à 1 indique que parallelism est limité à 1 et que le succès de ce pod signale le succès du job. Plus d'infos : https://kubernetes.io/docs/concepts/workloads/controllers/jobs-run-to-completion/

- **completionMode** (string)

  CompletionMode spécifie comment les complétions de Pods sont suivis. Il peut êre `NonIndexed` (par défaut) ou `Indexed`.
  
  `NonIndexed` indique que le Job est considéré complet lorsqu'il y a eu .spec.completions Pods complétés avec succès. Toutes les complétions de Pod sont homologues.
  
  `Indexed` indique que les Pods d'un Job ont un index de complétion associé, de 0 à (.spec.completions - 1), disponible dans l'annotation batch.kubernetes.io/job-completion-index. Le Job is est considéré complet lorsqu'il y a une complétion de Pod réussie pour chaque index. Lorsque la valeur est `Indexed`, .spec.completions doit être spécifié et `.spec.parallelism` doit être inférieur ou égal à 10^5.
  
  Ce champ est en niveau alpha et est pris en compte par les serveurs ayant activé la fonctionnalité IndexedJob. D'autres modes de complétion peuvent êre ajoutés dans le futur. Si le contrôleur de Job observe un mode qu'il ne reconnaît pas, le contrôleur saute les mises à jour pour le Job.

- **backoffLimit** (int32)

  Spécifie le nombre de nouvelles tentatives avant de marquer ce Job comme en échec. La valeur par défaut est 6

- **activeDeadlineSeconds** (int64)

  Spécifie la durée en secondes relativement au startTime pendant laquelle le Job peut être continuellement actif avant que le système essaie de le terminer ; la valeur doit être un entier positif. Si un Job est suspendu (à la création ou via une mise à jour), ce minuteur sera effectivement arrêté, et sera réinitialisé lorsque le Job sera redémarré.

- **ttlSecondsAfterFinished** (int32)

  ttlSecondsAfterFinished limite la durée de vie d'un Job ayant terminé son exécution (soit Complete, soit Failed). Si ce champ est renseigné, ttlSecondsAfterFinished après que le Job se termine, il est elligible à être supprimé automatiquement. Lorsque le Job est en cours de suppression, ses garanties de cycle de vie (par exemple ses finalizers) seront honorées. Si ce champ n'est pas renseigné, le Job ne sera pas supprimé automatiquement. Si ce champ est mis à zéro, le Job devient elligible à la suppression immédiatement après qu'il se termine. Ce champ est en niveau alpha et est uniquement pris en compte par les serveurs ayant activé la fonctionnalité TTLAfterFinished.

- **suspend** (boolean)

  Suspend indique si le contrôleur de Job doit ou non créer des Pods. Si un Job est créé avec suspend à true, aucun Pod n'est créé par le contrôleur de Job. Si un Job est suspedu après sa création (c'est-a-dire le drapeau est changé de false à true), le contrôleur de Job va supprimer tous les Pods actifs associés à ce Job. Les utilisateurs doivent concevoir leurs charges de travail pour supporter ce comportement correctement. Suspendre un Job va réinitialiser le champ StartTime du Job, en réinitialisant aussi le minuteur ActiveDeadlineSeconds. Ce champ est en niveau alpha et nécessite que la fonctionnalité SuspendJob soit activée ; dans le cas contraire, ce champ ne devrait pas être mis à true. La valeur par défaut est false.

### Selector


- **selector** (<a href="{{< ref "../common-definitions/label-selector#LabelSelector" >}}">LabelSelector</a>)

  Une requête d'étiquettes sur les Pods qui doivent correspondre au nombre de Pods. Normalement, le système renseigne ce champ pour vous. Plus d'infos : https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/#label-selectors

- **manualSelector** (boolean)

  manualSelector contrôle la génération des étiquettes et sélecteurs des pods. Laissez `manualSelector` sans valeur à moins de savoir exactement ce que vous faites. Lorsque false ou non défini, le système choisit des étiquettes uniques pour ce job et ajoute ces étiquettes au template de pod.  Lorsque true, l'utilisateur a la responsabilité de choisir des étiquettes uniques et de spécifier des sélecteurs.  Le choix d'étiquettes non uniques peut rendre ce job et d'autres instables.  Cependant, vous pourriez voir `manualSelector=true` dans des jobs ayant été créés avec l'ancienne API `extensions/v1beta1`. Plus d'infos : https://kubernetes.io/docs/concepts/workloads/controllers/jobs-run-to-completion/#specifying-your-own-pod-selector



## JobStatus {#JobStatus}

JobStatus représente l'état courant d'un Job.

<hr>

- **startTime** (Time)

  Représente l'heure à laquelle le contrôleur de job a commencé à gérer un job. Lorsqu'un Job est créé dans un état suspendu, ce champ n'est pas renseigné avant qu'il soit une première fois démarré. Ce champ est réinitialisé chaque fois qu'un Job est relancé suite à une suspension. Représenté au format RFC3339 en UTC.

  <a name="Time"></a>
  *Time is a wrapper around time.Time which supports correct marshaling to YAML and JSON.  Wrappers are provided for many of the factory methods that the time package offers.*

- **completionTime** (Time)

  Représente l'heure à laquelle le job termine. Il n'est pas garanti d'être renseigné dans l'ordre d'arrivée à travers plusieurs opérations. Est représenté dans le format RFC3339 en UTC. L'heure de complétion est renseignée uniquement lorsque le job termine avec succès.

  <a name="Time"></a>
  *Time is a wrapper around time.Time which supports correct marshaling to YAML and JSON.  Wrappers are provided for many of the factory methods that the time package offers.*

- **active** (int32)

  Le nombre de pods activement en cours d'exécution.

- **failed** (int32)

  Le nombre de pods ayant atteint la phase Failed.

- **succeeded** (int32)

  Le nombre de pods ayant atteint la phase Succeeded.

- **completedIndexes** (string)

  CompletedIndexes contient les indices terminés lorsque .spec.completionMode = "Indexed" dans un format texte. Les indices sont représentés par des entiers décimaux séparés par des virgules. Les nombres sont listés dans l'ordre croissant. Au moins trois nombres consécutifs sont compressés et représentés par le premier et le dernier élément de la série, séparés par un tiret. Par exemple, si les indices terminés sont 1, 3, 4, 5 et 7, ils sont représentés par "1,3-5,7".

- **conditions** ([]JobCondition)

  *Stratégie de patch : merge sur la clé `type`*
  
  *Atomique : sera remplacé lors d'un merge*
  
  Les dernières observations disponibles de l'état courant d'un objet. Lorsqu'un Job échoue, une des conditions aura un type à "Failed" et un statut à true. Lorsqu'un Job est suspendu, une des conditions aura un type à "Suspended" et un statut à true ; lorsque le Job est relancé, le statut de cette condition deviendra false. Lorsqu'un Job est complété, une des conditions aura un type à "Complete" et un statut à true. Plus d'infos : https://kubernetes.io/docs/concepts/workloads/controllers/jobs-run-to-completion/

  <a name="JobCondition"></a>
  *JobCondition décrit l'état courant d'un job.*

  - **conditions.status** (string), requis

    Statut de la condition, parmi True, False, Unknown.

  - **conditions.type** (string), requis

    Type de la condition de job, Complete ou Failed.

  - **conditions.lastProbeTime** (Time)

    Dernière fois que la condition a été vérifiée.

    <a name="Time"></a>
    *Time is a wrapper around time.Time which supports correct marshaling to YAML and JSON.  Wrappers are provided for many of the factory methods that the time package offers.*

  - **conditions.lastTransitionTime** (Time)

    Dernière fois que la condition est passée d'un statut à un autre.

    <a name="Time"></a>
    *Time is a wrapper around time.Time which supports correct marshaling to YAML and JSON.  Wrappers are provided for many of the factory methods that the time package offers.*

  - **conditions.message** (string)

    Message lisible par l'homme indiquant les détails de la dernière transition.

  - **conditions.reason** (string)

    Raison (brève) de la dernière transition de la condition.





## JobList {#JobList}

JobList est une collection de jobs.

<hr>

- **apiVersion**: batch/v1


- **kind**: JobList


- **metadata** (<a href="{{< ref "../common-definitions/list-meta#ListMeta" >}}">ListMeta</a>)

  Meta-données standard de liste. Plus d'infos : https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata

- **items** ([]<a href="{{< ref "../workload-resources/job-v1#Job" >}}">Job</a>), requis

  items est la liste de Jobs.





## Operations {#Operations}



<hr>






### `get` read the specified Job

#### HTTP Request

GET /apis/batch/v1/namespaces/{namespace}/jobs/{name}

#### Parameters


- **name** (*in path*): string, required

  name of the Job


- **namespace** (*in path*): string, required

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>


- **pretty** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>



#### Response


200 (<a href="{{< ref "../workload-resources/job-v1#Job" >}}">Job</a>): OK

401: Unauthorized


### `get` read status of the specified Job

#### HTTP Request

GET /apis/batch/v1/namespaces/{namespace}/jobs/{name}/status

#### Parameters


- **name** (*in path*): string, required

  name of the Job


- **namespace** (*in path*): string, required

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>


- **pretty** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>



#### Response


200 (<a href="{{< ref "../workload-resources/job-v1#Job" >}}">Job</a>): OK

401: Unauthorized


### `list` list or watch objects of kind Job

#### HTTP Request

GET /apis/batch/v1/namespaces/{namespace}/jobs

#### Parameters


- **namespace** (*in path*): string, required

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>


- **allowWatchBookmarks** (*in query*): boolean

  <a href="{{< ref "../common-parameters/common-parameters#allowWatchBookmarks" >}}">allowWatchBookmarks</a>


- **continue** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#continue" >}}">continue</a>


- **fieldSelector** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldSelector" >}}">fieldSelector</a>


- **labelSelector** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#labelSelector" >}}">labelSelector</a>


- **limit** (*in query*): integer

  <a href="{{< ref "../common-parameters/common-parameters#limit" >}}">limit</a>


- **pretty** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>


- **resourceVersion** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersion" >}}">resourceVersion</a>


- **resourceVersionMatch** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersionMatch" >}}">resourceVersionMatch</a>


- **timeoutSeconds** (*in query*): integer

  <a href="{{< ref "../common-parameters/common-parameters#timeoutSeconds" >}}">timeoutSeconds</a>


- **watch** (*in query*): boolean

  <a href="{{< ref "../common-parameters/common-parameters#watch" >}}">watch</a>



#### Response


200 (<a href="{{< ref "../workload-resources/job-v1#JobList" >}}">JobList</a>): OK

401: Unauthorized


### `list` list or watch objects of kind Job

#### HTTP Request

GET /apis/batch/v1/jobs

#### Parameters


- **allowWatchBookmarks** (*in query*): boolean

  <a href="{{< ref "../common-parameters/common-parameters#allowWatchBookmarks" >}}">allowWatchBookmarks</a>


- **continue** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#continue" >}}">continue</a>


- **fieldSelector** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldSelector" >}}">fieldSelector</a>


- **labelSelector** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#labelSelector" >}}">labelSelector</a>


- **limit** (*in query*): integer

  <a href="{{< ref "../common-parameters/common-parameters#limit" >}}">limit</a>


- **pretty** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>


- **resourceVersion** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersion" >}}">resourceVersion</a>


- **resourceVersionMatch** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersionMatch" >}}">resourceVersionMatch</a>


- **timeoutSeconds** (*in query*): integer

  <a href="{{< ref "../common-parameters/common-parameters#timeoutSeconds" >}}">timeoutSeconds</a>


- **watch** (*in query*): boolean

  <a href="{{< ref "../common-parameters/common-parameters#watch" >}}">watch</a>



#### Response


200 (<a href="{{< ref "../workload-resources/job-v1#JobList" >}}">JobList</a>): OK

401: Unauthorized


### `create` create a Job

#### HTTP Request

POST /apis/batch/v1/namespaces/{namespace}/jobs

#### Parameters


- **namespace** (*in path*): string, required

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>


- **body**: <a href="{{< ref "../workload-resources/job-v1#Job" >}}">Job</a>, required

  


- **dryRun** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>


- **fieldManager** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>


- **pretty** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>



#### Response


200 (<a href="{{< ref "../workload-resources/job-v1#Job" >}}">Job</a>): OK

201 (<a href="{{< ref "../workload-resources/job-v1#Job" >}}">Job</a>): Created

202 (<a href="{{< ref "../workload-resources/job-v1#Job" >}}">Job</a>): Accepted

401: Unauthorized


### `update` replace the specified Job

#### HTTP Request

PUT /apis/batch/v1/namespaces/{namespace}/jobs/{name}

#### Parameters


- **name** (*in path*): string, required

  name of the Job


- **namespace** (*in path*): string, required

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>


- **body**: <a href="{{< ref "../workload-resources/job-v1#Job" >}}">Job</a>, required

  


- **dryRun** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>


- **fieldManager** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>


- **pretty** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>



#### Response


200 (<a href="{{< ref "../workload-resources/job-v1#Job" >}}">Job</a>): OK

201 (<a href="{{< ref "../workload-resources/job-v1#Job" >}}">Job</a>): Created

401: Unauthorized


### `update` replace status of the specified Job

#### HTTP Request

PUT /apis/batch/v1/namespaces/{namespace}/jobs/{name}/status

#### Parameters


- **name** (*in path*): string, required

  name of the Job


- **namespace** (*in path*): string, required

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>


- **body**: <a href="{{< ref "../workload-resources/job-v1#Job" >}}">Job</a>, required

  


- **dryRun** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>


- **fieldManager** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>


- **pretty** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>



#### Response


200 (<a href="{{< ref "../workload-resources/job-v1#Job" >}}">Job</a>): OK

201 (<a href="{{< ref "../workload-resources/job-v1#Job" >}}">Job</a>): Created

401: Unauthorized


### `patch` partially update the specified Job

#### HTTP Request

PATCH /apis/batch/v1/namespaces/{namespace}/jobs/{name}

#### Parameters


- **name** (*in path*): string, required

  name of the Job


- **namespace** (*in path*): string, required

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>


- **body**: <a href="{{< ref "../common-definitions/patch#Patch" >}}">Patch</a>, required

  


- **dryRun** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>


- **fieldManager** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>


- **force** (*in query*): boolean

  <a href="{{< ref "../common-parameters/common-parameters#force" >}}">force</a>


- **pretty** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>



#### Response


200 (<a href="{{< ref "../workload-resources/job-v1#Job" >}}">Job</a>): OK

401: Unauthorized


### `patch` partially update status of the specified Job

#### HTTP Request

PATCH /apis/batch/v1/namespaces/{namespace}/jobs/{name}/status

#### Parameters


- **name** (*in path*): string, required

  name of the Job


- **namespace** (*in path*): string, required

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>


- **body**: <a href="{{< ref "../common-definitions/patch#Patch" >}}">Patch</a>, required

  


- **dryRun** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>


- **fieldManager** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldManager" >}}">fieldManager</a>


- **force** (*in query*): boolean

  <a href="{{< ref "../common-parameters/common-parameters#force" >}}">force</a>


- **pretty** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>



#### Response


200 (<a href="{{< ref "../workload-resources/job-v1#Job" >}}">Job</a>): OK

401: Unauthorized


### `delete` delete a Job

#### HTTP Request

DELETE /apis/batch/v1/namespaces/{namespace}/jobs/{name}

#### Parameters


- **name** (*in path*): string, required

  name of the Job


- **namespace** (*in path*): string, required

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>


- **body**: <a href="{{< ref "../common-definitions/delete-options#DeleteOptions" >}}">DeleteOptions</a>

  


- **dryRun** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>


- **gracePeriodSeconds** (*in query*): integer

  <a href="{{< ref "../common-parameters/common-parameters#gracePeriodSeconds" >}}">gracePeriodSeconds</a>


- **pretty** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>


- **propagationPolicy** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#propagationPolicy" >}}">propagationPolicy</a>



#### Response


200 (<a href="{{< ref "../common-definitions/status#Status" >}}">Status</a>): OK

202 (<a href="{{< ref "../common-definitions/status#Status" >}}">Status</a>): Accepted

401: Unauthorized


### `deletecollection` delete collection of Job

#### HTTP Request

DELETE /apis/batch/v1/namespaces/{namespace}/jobs

#### Parameters


- **namespace** (*in path*): string, required

  <a href="{{< ref "../common-parameters/common-parameters#namespace" >}}">namespace</a>


- **body**: <a href="{{< ref "../common-definitions/delete-options#DeleteOptions" >}}">DeleteOptions</a>

  


- **continue** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#continue" >}}">continue</a>


- **dryRun** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#dryRun" >}}">dryRun</a>


- **fieldSelector** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#fieldSelector" >}}">fieldSelector</a>


- **gracePeriodSeconds** (*in query*): integer

  <a href="{{< ref "../common-parameters/common-parameters#gracePeriodSeconds" >}}">gracePeriodSeconds</a>


- **labelSelector** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#labelSelector" >}}">labelSelector</a>


- **limit** (*in query*): integer

  <a href="{{< ref "../common-parameters/common-parameters#limit" >}}">limit</a>


- **pretty** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#pretty" >}}">pretty</a>


- **propagationPolicy** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#propagationPolicy" >}}">propagationPolicy</a>


- **resourceVersion** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersion" >}}">resourceVersion</a>


- **resourceVersionMatch** (*in query*): string

  <a href="{{< ref "../common-parameters/common-parameters#resourceVersionMatch" >}}">resourceVersionMatch</a>


- **timeoutSeconds** (*in query*): integer

  <a href="{{< ref "../common-parameters/common-parameters#timeoutSeconds" >}}">timeoutSeconds</a>



#### Response


200 (<a href="{{< ref "../common-definitions/status#Status" >}}">Status</a>): OK

401: Unauthorized

