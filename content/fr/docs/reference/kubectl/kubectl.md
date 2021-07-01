---
title: kubectl
content_type: tool-reference
description: Référence kubectl
notitle: true
---
## {{% heading "synopsis" %}}


kubectl contrôle le manager d'un cluster Kubernetes

Vous trouverez plus d'informations ici : https://kubernetes.io/fr/docs/reference/kubectl/overview/

```
kubectl [flags]
```



## {{% heading "options" %}}


<table style="width: 100%; table-layout: fixed;">
<colgroup>
<col span="1" style="width: 10px;" />
<col span="1" />
</colgroup>
<tbody>

<tr>
<td colspan="2">--add-dir-header</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Si vrai, ajoute le répertoire du fichier à l'entête</td>
</tr>

<tr>
<td colspan="2">--alsologtostderr</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">log sur l'erreur standard en plus d'un fichier</td>
</tr>

<tr>
<td colspan="2">--application-metrics-count-limit int&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Défaut : 100</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Nombre max de métriques d'applications à stocker (par conteneur)</td>
</tr>

<tr>
<td colspan="2">--as chaîne</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Nom d'utilisateur à utiliser pour l'opération</td>
</tr>

<tr>
<td colspan="2">--as-group tableauDeChaînes</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Groupe à utiliser pour l'opération, ce flag peut être répété pour spécifier plusieurs groupes</td>
</tr>

<tr>
<td colspan="2">--azure-container-registry-config chaîne</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Chemin du fichier contenant les informations de configuration du registre de conteneurs Azure</td>
</tr>

<tr>
<td colspan="2">--boot-id-file string&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Défaut : "/proc/sys/kernel/random/boot_id"</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Liste séparée par des virgules de fichiers dans lesquels rechercher le boot-id. Utilise le premier trouvé.</td>
</tr>

<tr>
<td colspan="2">--cache-dir chaîne&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Défaut: "/home/karen/.kube/http-cache"</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Répertoire de cache HTTP par défaut</td>
</tr>

<tr>
<td colspan="2">--certificate-authority chaîne</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Chemin vers un fichier cert pour l'autorité de certification</td>
</tr>

<tr>
<td colspan="2">--client-certificate chaîne</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Chemin vers un fichier de certificat client pour TLS</td>
</tr>

<tr>
<td colspan="2">--client-key chaîne</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Chemin vers un fichier de clé client pour TLS</td>
</tr>

<tr>
<td colspan="2">--cloud-provider-gce-lb-src-cidrs cidrs&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Défaut: 130.211.0.0/22,209.85.152.0/22,209.85.204.0/22,35.191.0.0/16</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">CIDRs ouverts dans le firewall GCE pour le proxy de trafic LB & health checks</td>
</tr>

<tr>
<td colspan="2">--cluster chaîne</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Le nom du cluster kubeconfig à utiliser</td>
</tr>

<tr>
<td colspan="2">--container-hints chaîne&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Défaut : "/etc/cadvisor/container_hints.json"</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">location du fichier hints du conteneur</td>
</tr>

<tr>
<td colspan="2">--containerd chaîne&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Défaut : "/run/containerd/containerd.sock"</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Point de terminaison de containerd</td>
</tr>

<tr>
<td colspan="2">--containerd-namespace chaîne&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Défaut : "k8s.io"</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">namespace de containerd</td>
</tr>

<tr>
<td colspan="2">--context chaîne</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Le nom du contexte kubeconfig à utiliser</td>
</tr>

<tr>
<td colspan="2">--default-not-ready-toleration-seconds int&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Défaut: 300</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Indique les tolerationSeconds de la tolérance pour notReady:NoExecute qui sont ajoutées par défaut à tous les pods qui n'ont pas défini une telle tolérance</td>
</tr>

<tr>
<td colspan="2">--default-unreachable-toleration-seconds int&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Défaut: 300</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Indique les tolerationSeconds de la tolérance pour unreachable:NoExecute qui sont ajoutées par défaut à tous les pods qui n'ont pas défini une telle tolérance</td>
</tr>

<tr>
<td colspan="2">--disable-root-cgroup-stats</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Désactive la collecte des stats du Cgroup racine</td>
</tr>

<tr>
<td colspan="2">--docker chaîne&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Défaut : "unix:///var/run/docker.sock"</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Point de terminaison docker</td>
</tr>

<tr>
<td colspan="2">--docker-env-metadata-whitelist chaîne</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">une liste séparée par des virgules de variables d'environnement qui doivent être collectées pour les conteneurs docker</td>
</tr>

<tr>
<td colspan="2">--docker-only</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Remonte uniquement les stats Docker en plus des stats racine</td>
</tr>

<tr>
<td colspan="2">--docker-root chaîne&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Défaut : "/var/lib/docker"</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">DÉPRÉCIÉ : la racine de docker est lue depuis docker info (ceci est une solution de secours, défaut : /var/lib/docker)</td>
</tr>

<tr>
<td colspan="2">--docker-tls</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">utiliser TLS pour se connecter à docker</td>
</tr>

<tr>
<td colspan="2">--docker-tls-ca chaîne&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Défaut : "ca.pem"</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">chemin vers CA de confiance</td>
</tr>

<tr>
<td colspan="2">--docker-tls-cert chaîne&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Défaut : "cert.pem"</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">chemin vers le certificat client</td>
</tr>

<tr>
<td colspan="2">--docker-tls-key chaîne&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Défaut : "key.pem"</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">chemin vers la clef privée</td>
</tr>

<tr>
<td colspan="2">--enable-load-reader</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Activer le lecteur de la charge CPU</td>
</tr>

<tr>
<td colspan="2">--event-storage-age-limit chaîne&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Défaut : "default=0"</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Durée maximale pendant laquelle stocker les événements  (par type). La valeur est une liste séparée par des virgules de clefs/valeurs, où les clefs sont des types d'événements (par ex: creation, oom) ou "default" et la valeur est la durée. La valeur par défaut est appliquée à tous les types d'événements non spécifiés</td>
</tr>

<tr>
<td colspan="2">--event-storage-event-limit chaîne&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Défaut : "default=0"</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Nombre max d'événements à stocker (par type). La valeur est une liste séparée par des virgules de clefs/valeurs, où les clefs sont les types d'événements (par ex: creation, oom) ou "default" et la valeur est un entier. La valeur par défaut est appliquée à tous les types d'événements non spécifiés</td>
</tr>

<tr>
<td colspan="2">--global-housekeeping-interval durée&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Défaut : 1m0s</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Intevalle entre ménages globaux</td>
</tr>

<tr>
<td colspan="2">-h, --help</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">aide pour kubectl</td>
</tr>

<tr>
<td colspan="2">--housekeeping-interval durée&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Défaut : 10s</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Intervalle entre ménages des conteneurs</td>
</tr>

<tr>
<td colspan="2">--insecure-skip-tls-verify</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Si vrai, la validité du certificat du serveur ne sera pas vérifiée. Ceci rend vos connexions HTTPS non sécurisées</td>
</tr>

<tr>
<td colspan="2">--kubeconfig chaîne</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Chemin du fichier kubeconfig à utiliser pour les requêtes du CLI</td>
</tr>

<tr>
<td colspan="2">--log-backtrace-at traceLocation&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Défaut: :0</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">lorsque les logs arrivent à la ligne fichier:N, émet une stack trace</td>
</tr>

<tr>
<td colspan="2">--log-cadvisor-usage</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Activer les logs d'usage du conteneur cAdvisor</td>
</tr>

<tr>
<td colspan="2">--log-dir chaîne</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Si non vide, écrit les fichiers de log dans ce répertoire</td>
</tr>

<tr>
<td colspan="2">--log-file chaîne</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Si non vide, utilise ce fichier de log</td>
</tr>

<tr>
<td colspan="2">--log-file-max-size uint&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Défaut : 1800</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Définit la taille maximale d'un fichier de log. L'unité est le mega-octet. Si la valeur est 0, la taille de fichier maximale est illimitée.</td>
</tr>

<tr>
<td colspan="2">--log-flush-frequency durée&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Défaut: 5s</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Nombre de secondes maximum entre flushs des logs</td>
</tr>

<tr>
<td colspan="2">--logtostderr&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Défaut: true</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">log sur l'erreur standard plutôt que dans un fichier</td>
</tr>

<tr>
<td colspan="2">--machine-id-file chaîne&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Défaut : "/etc/machine-id,/var/lib/dbus/machine-id"</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">liste séparée par des virgules de fichiers dans lesquels rechercher le machine-id. Utiliser le premier trouvé.</td>
</tr>

<tr>
<td colspan="2">--match-server-version</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">La version du serveur doit correspondre à la version du client</td>
</tr>

<tr>
<td colspan="2">-n, --namespace chaîne</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Si présent, la portée de namespace pour la requête du CLI</td>
</tr>

<tr>
<td colspan="2">--password chaîne</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Mot de passe pour l'authentification de base au serveur d'API</td>
</tr>

<tr>
<td colspan="2">--profile chaîne&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Défaut: "none"</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Nom du profil à capturer. Parmi (none|cpu|heap|goroutine|threadcreate|block|mutex)</td>
</tr>

<tr>
<td colspan="2">--profile-output chaîne&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Défaut: "profile.pprof"</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Nom du fichier dans lequel écrire le profil</td>
</tr>

<tr>
<td colspan="2">--request-timeout chaîne&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Défaut: "0"</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">La durée à attendre avant d'abandonner une requête au serveur. Les valeurs non égales à zéro doivent contenir une unité de temps correspondante (ex 1s, 2m, 3h). Une valeur à zéro indique de ne pas abandonner les requêtes</td>
</tr>

<tr>
<td colspan="2">-s, --server chaîne</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">L'adresse et le port de l'API server Kubernetes</td>
</tr>

<tr>
<td colspan="2">--skip-headers</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Si vrai, n'affiche pas les entêtes dans les messages de log</td>
</tr>

<tr>
<td colspan="2">--skip-log-headers</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Si vrai, évite les entêtes lors de l'ouverture des fichiers de log</td>
</tr>

<tr>
<td colspan="2">--stderrthreshold sévérité&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Défaut: 2</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">logs à cette sévérité et au dessus de ce seuil vont dans stderr</td>
</tr>

<tr>
<td colspan="2">--storage-driver-buffer-duration durée&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Défaut : 1m0s</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Les écritures dans le driver de stockage seront bufferisés pour cette durée, et seront envoyés aux backends non-mémoire en une seule transaction</td>
</tr>

<tr>
<td colspan="2">--storage-driver-db chaîne&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Défaut : "cadvisor"</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">nom de la base de données</td>
</tr>

<tr>
<td colspan="2">--storage-driver-host chaîne&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Défaut : "localhost:8086"</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">hôte:port de la base de données</td>
</tr>

<tr>
<td colspan="2">--storage-driver-password chaîne&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Défaut : "root"</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Mot de passe de la base de données</td>
</tr>

<tr>
<td colspan="2">--storage-driver-secure</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">utiliser une connexion sécurisée avec la base de données</td>
</tr>

<tr>
<td colspan="2">--storage-driver-table chaîne&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Défaut : "stats"</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Nom de la table dans la base de données</td>
</tr>

<tr>
<td colspan="2">--storage-driver-user chaîne&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Défaut : "root"</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">nom d'utilisateur de la base de données</td>
</tr>

<tr>
<td colspan="2">--token chaîne</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Bearer token pour l'authentification auprès de l'API server</td>
</tr>

<tr>
<td colspan="2">--update-machine-info-interval durée&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Défaut : 5m0s</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Intevalle entre mises à jour des infos machine.</td>
</tr>

<tr>
<td colspan="2">--user chaîne</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Le nom de l'utilisateur kubeconfig à utiliser</td>
</tr>

<tr>
<td colspan="2">--username chaîne</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Nom d'utilisateur pour l'authentification de base au serveur  d'API</td>
</tr>

<tr>
<td colspan="2">-v, --v Niveau</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Niveau de verbosité des logs</td>
</tr>

<tr>
<td colspan="2">--version version[=true]</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Affiche les informations de version et quitte</td>
</tr>

<tr>
<td colspan="2">--vmodule moduleSpec</td>
</tr>
<tr>
<td></td><td style="line-height: 130%; word-wrap: break-word;">Liste de settings pattern=N séparés par des virgules pour le logging filtré par fichiers</td>
</tr>

</tbody>
</table>





## {{% heading "seealso" %}}


* [kubectl alpha](/docs/reference/generated/kubectl/kubectl-commands#alpha)     - Commandes pour fonctionnalités alpha
* [kubectl annotate](/docs/reference/generated/kubectl/kubectl-commands#annotate)	 - Met à jour les annotations d'une ressource
* [kubectl api-resources](/docs/reference/generated/kubectl/kubectl-commands#api-resources)	 - Affiche les ressources de l'API prises en charge sur le serveur
* [kubectl api-versions](/docs/reference/generated/kubectl/kubectl-commands#api-versions)	 - Affiche les versions de l'API prises en charge sur le serveur, sous la forme "groupe/version"
* [kubectl apply](/docs/reference/generated/kubectl/kubectl-commands#apply)	 - Applique une configuration à une ressource depuis un fichier ou stdin
* [kubectl attach](/docs/reference/generated/kubectl/kubectl-commands#attach)	 - Attache à un conteneur en cours d'exécution
* [kubectl auth](/docs/reference/generated/kubectl/kubectl-commands#auth)	 - Inspecte les autorisations
* [kubectl autoscale](/docs/reference/generated/kubectl/kubectl-commands#autoscale)	 - Auto-scale un Deployment, ReplicaSet, ou ReplicationController
* [kubectl certificate](/docs/reference/generated/kubectl/kubectl-commands#certificate)	 - Modifie des ressources certificat
* [kubectl cluster-info](/docs/reference/generated/kubectl/kubectl-commands#cluster-info)	 - Affiche les informations du cluster
* [kubectl completion](/docs/reference/generated/kubectl/kubectl-commands#completion)	 - Génère le code de complétion pour le shell spécifié (bash ou zsh)
* [kubectl config](/docs/reference/generated/kubectl/kubectl-commands#config)	 - Modifie les fichiers kubeconfig
* [kubectl convert](/docs/reference/generated/kubectl/kubectl-commands#convert)	 - Convertit des fichiers de config entre différentes versions d'API
* [kubectl cordon](/docs/reference/generated/kubectl/kubectl-commands#cordon)	 - Marque un nœud comme non assignable (unschedulable)
* [kubectl cp](/docs/reference/generated/kubectl/kubectl-commands#cp)	 - Copie des fichiers et répertoires depuis et vers des conteneurs
* [kubectl create](/docs/reference/generated/kubectl/kubectl-commands#create)	 - Crée une ressource depuis un fichier ou stdin
* [kubectl delete](/docs/reference/generated/kubectl/kubectl-commands#delete)	 - Supprime des ressources par fichiers ou stdin, par ressource et nom, ou par ressource et sélecteur de label
* [kubectl describe](/docs/reference/generated/kubectl/kubectl-commands#describe)	 - Affiche les informations d'une ressource spécifique ou d'un groupe de ressources
* [kubectl diff](/docs/reference/generated/kubectl/kubectl-commands#diff)	 - Différence entre la version live et la version désirée
* [kubectl drain](/docs/reference/generated/kubectl/kubectl-commands#drain)	 - Draine un nœud en préparation d'une mise en maintenance
* [kubectl edit](/docs/reference/generated/kubectl/kubectl-commands#edit)	 - Édite une ressource du serveur
* [kubectl exec](/docs/reference/generated/kubectl/kubectl-commands#exec)	 - Exécute une commande dans un conteneur
* [kubectl explain](/docs/reference/generated/kubectl/kubectl-commands#explain)	 - Documentation sur les ressources
* [kubectl expose](/docs/reference/generated/kubectl/kubectl-commands#expose)	 - Prend un replication controller, service, deployment ou pod et l'expose comme un nouveau Service Kubernetes
* [kubectl get](/docs/reference/generated/kubectl/kubectl-commands#get)	 - Affiche une ou plusieurs ressources
* [kubectl kustomize](/docs/reference/generated/kubectl/kubectl-commands#kustomize)     - Construit une cible kustomization à partir d'un répertoire ou d'une URL distante.
* [kubectl label](/docs/reference/generated/kubectl/kubectl-commands#label)	 - Met à jour les labels d'une ressource
* [kubectl logs](/docs/reference/generated/kubectl/kubectl-commands#logs)	 - Affiche les logs d'un conteneur dans un pod
* [kubectl options](/docs/reference/generated/kubectl/kubectl-commands#options)	 - Affiche la liste des flags hérités par toutes les commandes
* [kubectl patch](/docs/reference/generated/kubectl/kubectl-commands#patch)	 - Met à jour un ou plusieurs champs d'une ressource par merge patch stratégique
* [kubectl plugin](/docs/reference/generated/kubectl/kubectl-commands#plugin)	 - Fournit des utilitaires pour interagir avec des plugins
* [kubectl port-forward](/docs/reference/generated/kubectl/kubectl-commands#port-forward)	 - Redirige un ou plusieurs ports vers un pod
* [kubectl proxy](/docs/reference/generated/kubectl/kubectl-commands#proxy)	 - Exécute un proxy vers l'API server Kubernetes
* [kubectl replace](/docs/reference/generated/kubectl/kubectl-commands#replace)	 - Remplace une ressource par fichier ou stdin
* [kubectl rollout](/docs/reference/generated/kubectl/kubectl-commands#rollout)	 - Gère le rollout d'une ressource
* [kubectl run](/docs/reference/generated/kubectl/kubectl-commands#run)	 - Exécute une image donnée dans le cluster
* [kubectl scale](/docs/reference/generated/kubectl/kubectl-commands#scale)	 - Définit une nouvelle taille pour un Deployment, ReplicaSet ou Replication Controller
* [kubectl set](/docs/reference/generated/kubectl/kubectl-commands#set)	 - Définit des fonctionnalités spécifiques sur des objets
* [kubectl taint](/docs/reference/generated/kubectl/kubectl-commands#taint)	 - Met à jour les marques (taints) sur un ou plusieurs nœuds
* [kubectl top](/docs/reference/generated/kubectl/kubectl-commands#top)	 - Affiche l'utilisation de ressources matérielles (CPU/Memory/Storage)
* [kubectl uncordon](/docs/reference/generated/kubectl/kubectl-commands#uncordon)	 - Marque un nœud comme assignable (schedulable)
* [kubectl version](/docs/reference/generated/kubectl/kubectl-commands#version)	 - Affiche les informations de version du client et du serveur
* [kubectl wait](/docs/reference/generated/kubectl/kubectl-commands#wait)	 - Expérimental : Attend une condition particulière sur une ou plusieurs ressources


