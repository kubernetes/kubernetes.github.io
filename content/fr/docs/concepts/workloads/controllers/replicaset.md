---
title: ReplicaSet
content_type: concept
weight: 10
---

<!-- overview -->

Un ReplicaSet (ensemble de réplicas en français) a pour but de maintenir un ensemble stable de Pods à un moment donné.
Cet objet est souvent utilisé pour garantir la disponibilité d'un certain nombre identique de Pods.



<!-- body -->

## Comment un ReplicaSet fonctionne

Un ReplicaSet est défini avec des champs, incluant un selecteur qui spécifie comment identifier les Pods qu'il peut posséder,
un nombre de replicas indiquant le nombre de Pods qu'il doit maintenir et un modèle de Pod spécifiant les données que les
nouveaux Pods que le replicatSet va créer jusqu'au nombre de replicas demandé.

Un ReplicaSet va atteindre son objectif en créant et supprimant des Pods pour atteindre le nombre de réplicas désirés.
Quand un ReplicaSet a besoin de créer de nouveaux Pods, il utilise alors son Pod template.

Le lien d'un ReplicaSet à ses Pods est fait par le champ [metadata.ownerReferences](/docs/concepts/workloads/controllers/garbage-collection/#owners-and-dependents),
qui spécifie la ressource de l'objet par lequel il est détenu. Tous les Pods acquis par un ReplicaSet ont leurs propres informations d'identification de leur Replicaset, avec leur propre champ ownerReferences. C'est par ce lien que le ReplicaSet connait l'état des Pods qu'il maintient et agit en fonction de ces derniers.

Un ReplicaSet identifie des nouveaux Pods à acquérir en utilisant son selecteur.
Si il y a un Pod qui n'a pas de OwnerReference ou que OwnerReference n'est pas un controller et qu'il correspond à un sélecteur de ReplicaSet, il va immédiatement être acquis par ce ReplicaSet.

## Quand utiliser un ReplicaSet ?

Un ReplicaSet garantit qu’un nombre spécifié de réplicas de Pod soient exécutés à un moment donné.
Cependant, un Deployment est un concept de plus haut niveau qui gère les ReplicaSets et
fournit des mises à jour déclaratives aux Pods ainsi que de nombreuses autres fonctionnalités utiles.
Par conséquent, nous vous recommandons d’utiliser des Deployments au lieu d’utiliser directement des ReplicaSets, sauf si
vous avez besoin d'une orchestration personnalisée des mises à jour ou si vous n'avez pas besoin de mises à jour.

Cela signifie qu'il est possible que vous n'ayez jamais besoin de manipuler des objets ReplicaSet :
utilisez plutôt un déploiement et définissez votre application dans la section spec.

## Exemple

{{< codenew file="controllers/frontend.yaml" >}}

Enregistrer ce manifeste dans `frontend.yaml` et le soumettre à un cluster Kubernetes va créer le ReplicaSet défini et les pods qu’il gère.

```shell
kubectl apply -f https://kubernetes.io/examples/controllers/frontend.yaml
```

Vous pouvez ensuite récupérer les ReplicaSets actuellement déployés :
```shell
kubectl get rs
```

Et voir le frontend que vous avez créé :
```shell
NAME       DESIRED   CURRENT   READY   AGE
frontend   3         3         3       6s
```

Vous pouvez également vérifier l'état du ReplicaSet :
```shell
kubectl describe rs/frontend
```

Et vous verrez une sortie similaire à :
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

Et enfin, vous pourrez afficher les Pods déployés :
```shell
kubectl get Pods
```

Vous devriez voir des informations sur les Pods avec une sortie similaire à :
```shell
NAME             READY     STATUS    RESTARTS   AGE
frontend-9si5l   1/1       Running   0          1m
frontend-dnjpy   1/1       Running   0          1m
frontend-qhloh   1/1       Running   0          1m
```

Vous pouvez également vérifier que la OwnerReference de ces pods est définie sur le frontend ReplicaSet.
Pour ce faire, récupérez le yaml de l’un des pods :
```shell
kubectl get pods frontend-9si5l -o yaml
```

La sortie sera similaire à celle-ci, avec les informations de l'interface ReplicaSet frontend définies dans le champ ownerReferences des métadonnées:
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

## Acquisitions de Pod en dehors du template

Bien que vous puissiez créer des pods manuellement sans problème, il est fortement recommandé de s’assurer que ces pods n'ont pas de
labels correspondant au sélecteur de l’un de vos ReplicaSets. Car un ReplicaSet n’est pas limité
à posséder les pods spécifiés par son modèle - il peut acquérir d’autres pods de la manière spécifiée dans les sections précédentes.

Prenez l'exemple précédent de ReplicaSet, ainsi que les pods spécifiés dans le manifeste suivant :

{{< codenew file="pods/pod-rs.yaml" >}}

Ces pods n’ayant pas de contrôleur (ni d’objet) en tant que référence propriétaire, ils correspondent au sélecteur de du ReplicaSet frontend, ils seront donc immédiatement acquis par ce ReplicaSet.

Supposons que vous créiez les pods une fois le ReplicaSet frontend déployé et qui a déjà déployé ses replicas de Pods initiaux afin de
remplir son exigence de nombre de replicas :

```shell
kubectl apply -f https://kubernetes.io/examples/pods/pod-rs.yaml
```

Les nouveaux pods seront acquis par le ReplicaSet, puis immédiatement terminés car le ReplicaSet dépasserait alors le compte désiré.

En récupérant les pods :
```shell
kubectl get Pods
```

La sortie montre que les nouveaux pods sont soit déjà terminés, soit en voie de l'être :
```shell
NAME             READY   STATUS        RESTARTS   AGE
frontend-9si5l   1/1     Running       0          1m
frontend-dnjpy   1/1     Running       0          1m
frontend-qhloh   1/1     Running       0          1m
pod2             0/1     Terminating   0          4s
```

Cependant, si vous créez d'abord les pods :
```shell
kubectl apply -f https://kubernetes.io/examples/pods/pod-rs.yaml
```

Et puis créez le ReplicaSet :
```shell
kubectl apply -f https://kubernetes.io/examples/controllers/frontend.yaml
```

Vous verrez que le ReplicaSet a acquis les pods et n'a créé que les nouveaux Pods manquants, conformément à ses spécifications,
jusqu'au nombre souhaité de Pods. En récupérant les Pods :
```shell
kubectl get Pods
```

La sortie va donner :
```shell
NAME             READY   STATUS    RESTARTS   AGE
frontend-pxj4r   1/1     Running   0          5s
pod1             1/1     Running   0          13s
pod2             1/1     Running   0          13s
```

De cette manière, un ReplicaSet peut avoir un ensemble de Pods hétérogène.

## Écrire un manifest de ReplicaSet

Comme avec tous les autres objets API Kubernetes, un ReplicaSet a besoin des champs `apiVersion`, `kind` et `metadata`.
Pour ReplicaSets, l'attribut `kind` est toujours ReplicaSet.

Dans Kubernetes 1.9, la version de l'API `apps/v1` pour le type ReplicaSet est la version actuelle et activée par défaut. La version de l'API `apps/v1beta2` est obsolète.

Reportez-vous aux premières lignes de l'exemple `frontend.yaml` pour obtenir des conseils.

Un ReplicaSet a également besoin de [`.spec` section](https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status).

### Pod Template

L'attribut `.spec.template` est un [modèle de pod](/docs/concepts/workloads/Pods/pod-overview/#pod-templates) qui requiert d'avoir des labels. Dans notre exemple `frontend.yaml`, nous avons un label : `tier: frontend`.
Il faut faire attention à ne pas avoir des selecteurs que d'autres controllers utilisent, afin d'éviter que le ReplicaSet n'adopte ce pod.

Pour le champ [restart policy](/docs/concepts/workloads/pods/pod-lifecycle/#restart-policy),
`.spec.template.spec.restartPolicy`, la seule valeur autorisée est `Always`, qui est la valeur par défaut.

### Sélecteur de Pod

Le champ `.spec.selector` est un [label selector](/docs/concepts/overview/working-with-objects/labels/). Tel que discuté
[précédemment](#how-a-replicaset-works), ce sont les labels utilisés pour identifier les Pods potentiels à acquérir. Dans notre
exemple avec `frontend.yaml`, le sélecteur était :
```shell
matchLabels:
	tier: frontend
```

Dans le ReplicaSet, `.spec.template.metadata.labels` doit correspondre à `spec.selector`, ou sinon il sera rejeté par l'API.

{{< note >}}
Pour 2 ReplicaSets spécifiant le même `.spec.selector` mais différents `.spec.template.metadata.labels` et `.spec.template.spec`, chaque ReplicaSet ignore les pods créés par l'autre ReplicaSet.
{{< /note >}}

### Replicas

Vous pouvez spécifier le nombre de pods à exécuter simultanément en définissant `.spec.replicas`. Le ReplicaSet va créer/supprimer
ses pods pour correspondre à ce nombre.

Si vous ne spécifiez pas `.spec.replicas`, la valeur par défaut est 1.

## Travailler avec des ReplicaSets

### Suppression d'un ReplicaSet et de ses pods

Pour supprimer un ReplicaSet et tous ses pods, utilisez [`kubectl delete`](/docs/reference/generated/kubectl/kubectl-commands#delete). The [Garbage collector](/docs/concepts/workloads/controllers/garbage-collection/) supprime automatiquement tous les pods associés par défaut.

Lors de l’utilisation de l’API REST ou de la bibliothèque `client-go`, vous devez définir `propagationPolicy` sur `Background` ou `Foreground` dans
l'option -d.
Par exemple :
```shell
kubectl proxy --port=8080
curl -X DELETE  'localhost:8080/apis/extensions/v1beta1/namespaces/default/replicasets/frontend' \
> -d '{"kind":"DeleteOptions","apiVersion":"v1","propagationPolicy":"Foreground"}' \
> -H "Content-Type: application/json"
```

### Supprimer juste un ReplicaSet

Vous pouvez supprimer un ReplicaSet sans affecter ses pods à l’aide de [`kubectl delete`](/docs/reference/generated/kubectl/kubectl-commands#delete) avec l'option `--cascade=orphan`.
Lorsque vous utilisez l'API REST ou la bibliothèque `client-go`, vous devez définir `propagationPolicy` sur `Orphan`.
Par exemple :
```shell
kubectl proxy --port=8080
curl -X DELETE  'localhost:8080/apis/extensions/v1beta1/namespaces/default/replicasets/frontend' \
> -d '{"kind":"DeleteOptions","apiVersion":"v1","propagationPolicy":"Orphan"}' \
> -H "Content-Type: application/json"
```

Une fois l’original supprimé, vous pouvez créer un nouveau ReplicaSet pour le remplacer. Tant que l'ancien et le nouveau `.spec.selector` sont identiques, le nouveau adoptera les anciens Pods.
Cependant, le ReplicaSet ne fera aucun effort pour que les pods existants correspondent à un nouveau Pod template.
Pour mettre à jour les Pods à une nouvelle spec de manière contrôlée, utilisez un
[Deployment](/docs/concepts/workloads/controllers/deployment/#creating-a-deployment), car les ReplicaSets ne supportent pas de rolling update directement.

### Isoler les pods d'un ReplicaSet

Vous pouvez supprimer les pods d'un ReplicaSet en modifiant leurs labels. Cette technique peut être utilisée pour enlever les pods
pour le débogage, récupération de données, etc. Les pods ainsi supprimés seront automatiquement remplacés
(en supposant que le nombre de réplicas n’est pas également modifié).

### Scaling d'un ReplicaSet

Un ReplicaSet peut facilement être scalé en mettant simplement à jour le champ `.spec.replicas`. Le contrôleur ReplicaSet
garantit que le nombre souhaité de pods avec un sélecteur de label correspondant soient disponibles et opérationnels.

### ReplicaSet en tant que Horizontal Pod Autoscaler Target

Un ReplicaSet peut également être une cible pour
[Horizontal Pod Autoscalers (HPA)](/docs/tasks/run-application/horizontal-pod-autoscale/).
Un ReplicaSet peut être mis à l'échelle automatiquement par un HPA. Voici un exemple HPA qui cible
le ReplicaSet que nous avons créé dans l'exemple précédent.

{{< codenew file="controllers/hpa-rs.yaml" >}}

Enregistrer ce manifeste dans `hpa-rs.yaml` et le soumettre à un cluster Kubernetes devrait
créer le HPA défini qui scale automatiquement le ReplicaSet cible en fonction de l'utilisation du processeur
des pods répliqués.

```shell
kubectl apply -f https://k8s.io/examples/controllers/hpa-rs.yaml
```

Vous pouvez aussi utiliser la commande `kubectl autoscale` pour accomplir la même chose.
(et c'est plus facile !)

```shell
kubectl autoscale rs frontend --max=10
```

## Alternatives au ReplicaSet

### Deployment (recommandé)

Le [`Deployment`](/docs/concepts/workloads/controllers/deployment/) est un object qui peut posséder les ReplicaSets et les mettres à jour ainsi que leurs Pods de façon déclarative, côté serveur et avec des rolling updates.

Alors que les ReplicaSets peuvent être utilisés indépendamment, ils sont principalement utilisés aujourd'hui par Deployments comme mécanisme pour orchestrer la création, suppresion et mises à jour des Pods.
Lorsque vous utilisez des Deployments, vous n’aurez plus à vous soucier de la gestion des ReplicaSets ainsi créés.
Les déploiements possèdent et gèrent leurs ReplicaSets.
C'est pourquoi il est recommandé d’utiliser les déploiements lorsque vous voulez des ReplicaSets.

### Pods nus

Contrairement au cas où un utilisateur a créé directement des pods, un ReplicaSet remplace les pods supprimés ou terminés pour quelque raison que ce soit, par exemple en cas de défaillance d'un nœud ou de maintenance de nœud perturbateur, telle qu'une mise à jour kernel. Pour cette raison, nous vous recommandons d'utiliser un ReplicaSet même si votre application ne nécessite qu'un seul pod. Pensez-y de la même manière qu’un superviseur de processus, mais il supervise plusieurs pods sur plusieurs nœuds au lieu de processus individuels sur un seul nœud. Un ReplicaSet délègue les redémarrages de conteneurs locaux à un agent du nœud (par exemple, Kubelet ou Docker).

### Job

Utilisez un [`Job`](/docs/concepts/jobs/run-to-completion-finite-workloads/) au lieu d'un ReplicaSet pour les pods qui doivent se terminer seuls
(c'est à dire des batch jobs).

### DaemonSet

Utilisez un [`DaemonSet`](/docs/concepts/workloads/controllers/daemonset/) au lieu d’un ReplicaSet pour les pods qui fournissent une
fonction au niveau du noeud, comme le monitoring ou la gestion des logs de ce noeud. Ces pods ont une durée de vie qui est liée
durée de vie d’une machine : le pod doit être en cours d’exécution sur la machine avant le démarrage des autres Pods et sont
sûrs de se terminer lorsque la machine est prête à être redémarrée/arrêtée.

### ReplicationController

Les ReplicaSets sont les successeurs de [_ReplicationControllers_](/docs/concepts/workloads/controllers/replicationcontroller/).
Les deux servent le même objectif et se comportent de la même manière, à la différence près que ReplicationController ne prend pas en charge les
les exigences de sélecteur décrites dans le [labels user guide](/docs/concepts/overview/working-with-objects/labels/#label-selectors).
En tant que tels, les ReplicaSets sont préférés aux ReplicationControllers.


