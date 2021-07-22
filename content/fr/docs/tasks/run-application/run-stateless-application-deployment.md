---
title: Exécuter une application sans état en utilisant un objet Déploiement.
min-kubernetes-server-version: v1.9
content_type: tutorial
weight: 10
---

<!-- overview -->

Cette page montre comment exécuter une application à l’aide d’un objet Déploiement Kubernetes.




## {{% heading "objectives" %}}


* Créer un déploiement Nginx.
* Utilisez kubectl pour lister les informations sur le déploiement.
* Mettre à jour le déploiement.




## {{% heading "prerequisites" %}}


{{< include "task-tutorial-prereqs.md" >}} {{< version-check >}}




<!-- lessoncontent -->

## Créer et explorer un déploiement Nginx

Vous pouvez exécuter une application en créant un objet Déploiement Kubernetes, et vous
pouvez décrire ce déploiement dans un fichier YAML. Par exemple, ce fichier YAML décrit
un déploiement qui exécute l’image nginx:1.14.2 Docker :


{{< codenew file="application/deployment.yaml" >}}


1. Créer un déploiement en fonction du fichier YAML :

        kubectl apply -f https://k8s.io/examples/application/deployment.yaml

2. Afficher des informations sur le déploiement :

        kubectl describe deployment nginx-deployment

    L'output est similaire à ceci :

        Name:     nginx-deployment
        Namespace:    default
        CreationTimestamp:  Tue, 30 Aug 2016 18:11:37 -0700
        Labels:     app=nginx
        Annotations:    deployment.kubernetes.io/revision=1
        Selector:   app=nginx
        Replicas:   2 desired | 2 updated | 2 total | 2 available | 0 unavailable
        StrategyType:   RollingUpdate
        MinReadySeconds:  0
        RollingUpdateStrategy:  1 max unavailable, 1 max surge
        Pod Template:
          Labels:       app=nginx
          Containers:
           nginx:
            Image:              nginx:1.14.2
            Port:               80/TCP
            Environment:        <none>
            Mounts:             <none>
          Volumes:              <none>
        Conditions:
          Type          Status  Reason
          ----          ------  ------
          Available     True    MinimumReplicasAvailable
          Progressing   True    NewReplicaSetAvailable
        OldReplicaSets:   <none>
        NewReplicaSet:    nginx-deployment-1771418926 (2/2 replicas created)
        No events.

3. Énumérer les modules créés par le déploiement :

        kubectl get pods -l app=nginx

    L'output est similaire à ceci :

        NAME                                READY     STATUS    RESTARTS   AGE
        nginx-deployment-1771418926-7o5ns   1/1       Running   0          16h
        nginx-deployment-1771418926-r18az   1/1       Running   0          16h

4. Afficher les informations d'un module (Pod) :

        kubectl describe pod <pod-name>

    où `<pod-name>` est le nom d'un de vos module (Pods).

## Mettre à jour le déploiement

Vous pouvez mettre à jour le déploiement en appliquant un nouveau fichier YAML. Ce fichier YAML
spécifie que le déploiement doit être mis à jour pour utiliser nginx 1.16.1.

{{< codenew file="application/deployment-update.yaml" >}}

1. Appliquer le nouveau fichier YAML :

         kubectl apply -f https://k8s.io/examples/application/deployment-update.yaml

2. Regardez le déploiement créer des modules avec de nouveaux noms et supprimer les anciens modules :

         kubectl get pods -l app=nginx

## Mise à l’échelle de l’application en augmentant le nombre de répliques

Vous pouvez augmenter le nombre de modules (Pods) dans votre déploiement en appliquant un nouveau fichier YAML.
fichier. Ce fichier YAML définit les répliques à 4, qui spécifie que le
devrait avoir quatre modules :

{{< codenew file="application/deployment-scale.yaml" >}}

1. Appliquer le nouveau fichier YAML :

        kubectl apply -f https://k8s.io/examples/application/deployment-scale.yaml

1. Vérifier que le déploiement comporte quatres modules :

        kubectl get pods -l app=nginx

    L'output est similaire à ceci :

        NAME                               READY     STATUS    RESTARTS   AGE
        nginx-deployment-148880595-4zdqq   1/1       Running   0          25s
        nginx-deployment-148880595-6zgi1   1/1       Running   0          25s
        nginx-deployment-148880595-fxcez   1/1       Running   0          2m
        nginx-deployment-148880595-rwovn   1/1       Running   0          2m

## Supprimer un déploiement

Supprimer le déploiement par son nom :

    kubectl delete deployment nginx-deployment

## ReplicationControllers -- the Old Way

La meilleure façon de créer une application répliquée est d’utiliser un déploiement,
qui à son tour utilise un ReplicaSet. Avant que le déploiement et ReplicaSet soient
ajoutés à Kubernetes, les applications répliquées ont été configurées utilisant un [ReplicationController](/docs/concepts/workloads/controllers/replicationcontroller/).


## {{% heading "whatsnext" %}}


* Apprendre plus à propos des [Deployment objects](/docs/concepts/workloads/controllers/deployment/).



