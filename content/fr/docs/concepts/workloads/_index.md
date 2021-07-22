---
title: Workloads
weight: 50
description: >
  Comprendre les Pods, le plus petit objet déployable sur Kubernetes, et les abstractions de haut niveaux vous permettant de les lancer.
no_list: true
---


<!-- definition -->

Un workload (charge de travail) est une application fonctionnant sur Kubernetes. Que votre workload soit un composant unique ou un agrégat de composants, sur Kubernetes celui-ci fonctionnera dans une série de pods. Dans Kubernetes, un Pod represente un ensemble de conteneur (containers) en fonctionnement sur votre cluster.

Les pods Kubernetes ont un cycle de vie définit (defined lifecycle). Par exemple, quand un pod est en fonction sur votre cluster et qu’une panne critique survient sur le noeud (node) où se situe ce pod, tous les pods du noeud seront en échec. Kubernetes traite ce niveau d’échec comme un état final :
Vous devez créer un nouveau Pod pour retrouver l’état initial même si le noeud redevient sain.

Cependant, pour vous simplifier la vie, vous n’avez pas a gérer chaque Pod directement. Vous pouvez utiliser une ressource workload qui gère votre groupe de pods à votre place. Ces ressources configurent des controleurs (controllers) qui s’assurent que le bon nombre et le bon type de pod soit en fonction pour égaler l’état que vous avez spécifié.

Kubernetes fournit plusieurs ressources workload pré-faites :

* [`Deployment`](/docs/concepts/workloads/controllers/deployment/) et [`ReplicaSet`](/docs/concepts/workloads/controllers/replicaset/) 
(qui remplacent l’ancienne ressource {{< glossary_tooltip text="ReplicationController" term_id="replication-controller" >}})).
Le `Deployment` (déploiement) est une bonne approche pour manager une application stateless sur votre cluster, tous les `Pods` d’un `Deployment` sont interchangeables et peuvent être remplacés si besoin.
* Le [`StatefulSet`](/docs/concepts/workloads/controllers/statefulset/)  vous permet de lancer un ou plusieurs Pods en relation qui garde plus ou moins la trace de leurs état.
Par exemple si votre workload enregistre des données de façon persistente, vous pouvez lancer un `StatefulSet` qui fera le lien entre les `Pods` et un volume persistent ([`PersistentVolume`](/docs/concepts/storage/persistent-volumes/)).
Votre code, présent dans les `Pods` du `StatefulSet`, peut répliquer des données dans les autres `Pods` qui sont dans le même `StatefulSet`,
pour améliorer la résilience global.
* Le [`DaemonSet`](/docs/concepts/workloads/controllers/daemonset/) permet de définir les `Pods` qui effectuent des actions sur le noeud local.
Ceux-ci peuvent être fondamental aux opérations de votre cluster, comme un outil d’aide réseau, ou peuvent faire part d’un module complémentaire (add-on).
Pour chaque nouveau noeud ajouté au cluster, le controle plane organise l'ajout d'un `Pod` pour ce `DaemonSet` sur le nouveau noeud.
* Les [`Job`](/docs/concepts/workloads/controllers/job/) et  [`CronJob`](/docs/concepts/workloads/controllers/cron-jobs/) sont des tâchent lancées jusqu’à accomplissement puis s’arrêtent. Les `Jobs` réprésentent une tâche ponctuelle, les `CronJob` sont des tâches récurrentes planifiés.

Dans l’écosystème étendu de Kubernetes, vous pouvez trouver des ressources workload de fournisseurs tiers qui permetent des fonctionnalités supplémentaires. L’utilisation d’un [`CustomResourceDefinition`](/docs/concepts/extend-kubernetes/api-extension/custom-resources/) permet d’ajouter une ressource workload d’un fournisseur tiers si vous souhaites une fonctionnalité ou un comportement spécifique qui ne fait pas partie du noyau de Kubernetes. Par exemple, si vous voulez lancer un groupe de `Pods` pour votre application mais vous devez arrêter leurs fonctionnement tant qu’ils ne sont pas tous disponibles, alors vous pouvez implémenter ou installer une extension qui permet cette fonctionnalité.

## {{% heading "whatsnext" %}}
Vous pouvez continuer la lecture des ressources, vous pouvez aussi apprendre à connaitre les taches qui leurs sont liées :
* Lancer une [application stateless en utilisant un `Deployment`](/docs/tasks/run-application/run-stateless-application-deployment/).
* Lancer une application statefull, soit comme [instance unique](/docs/tasks/run-application/run-single-instance-stateful-application/)
  ou alors comme un [ensemble répliqué](/docs/tasks/run-application/run-replicated-stateful-application/).
* Lancer une [tâche automatisée avec un `CronJob`](/docs/tasks/job/automated-tasks-with-cron-jobs/).

Pour en apprendre plus sur les méchanismes de Kubernetes, de séparation du code et de la configuration,
allez voir [Configuration](/docs/concepts/configuration/).

Il y a deux concepts supportés qui fournissent un contexte sur le sujet : comment Kubernetes gère les pods pour les applications :
* Le [ramasse-miettes](/docs/concepts/workloads/controllers/garbage-collection/), fait le ménage dans votre cluster après qu’une de _vos ressource_ soit supprimé.
* Le [temps de vie d’un controlleur éteint](/docs/concepts/workloads/controllers/ttlafterfinished/) supprime les Jobs une fois qu’un temps définit soit passé après son accomplissement.

Une fois que votre application est lancée, vous souhaitez peut etre la rendre disponible sur internet comme un [Service](/docs/concepts/services-networking/service/) ou comme une application web uniquement en utilsant un [Ingress](/docs/concepts/services-networking/ingress).
