---
reviewers:
title: EndpointSlices
feature:
  title: EndpointSlices
  description: >
    Suivi évolutif des réseaux Endpoints dans un cluster Kubernetes.

content_type: concept
weight: 10
---


<!-- overview -->

{{< feature-state for_k8s_version="v1.17" state="beta" >}}

_EndpointSlices_ offrent une méthode simple pour suivre les Endpoints d'un réseau au sein d'un cluster de Kubernetes. Ils offrent une alternative plus évolutive et extensible aux Endpoints.



<!-- body -->

## Ressource pour EndpointSlice {#endpointslice-resource}

Dans Kubernetes, un EndpointSlice contient des références à un ensemble de Endpoints.
Le controleur d'EndpointSlice crée automatiquement des EndpointSlices pour un Service quand un {{< glossary_tooltip text="sélecteur" term_id="selector" >}} est spécifié.
Ces EndpointSlices vont inclure des références à n'importe quels Pods qui correspondent aux selecteurs de Service.
EndpointSlices groupent ensemble les Endpoints d'un réseau par combinaisons uniques de Services et de Ports.

Par exemple, voici un échantillon d'une ressource EndpointSlice pour le Kubernetes Service `exemple`.

```yaml
apiVersion: discovery.k8s.io/v1beta1
kind: EndpointSlice
metadata:
  name: exemple-abc
  labels:
    kubernetes.io/service-name: exemple
addressType: IPv4
ports:
  - name: http
    protocol: TCP
    port: 80
endpoints:
  - addresses:
      - "10.1.2.3"
    conditions:
      ready: true
    hostname: pod-1
    topology:
      kubernetes.io/hostname: node-1
      topology.kubernetes.io/zone: us-west2-a
```

Les EndpointSlices gérés par le contrôleur d'EndpointSlice n'auront, par défaut, pas plus de 100 Endpoints chacun.
En dessous de cette échelle, EndpointSlices devraient mapper 1:1 les Endpoints et les Services et devraient avoir une performance similaire.

EndpointSlices peuvent agir en tant que source de vérité pour kube-proxy quand il s'agit du routage d'un trafic interne.
Lorsqu'ils sont activés, ils devraient offrir une amélioration de performance pour les services qui ont une grand quantité d'Endpoints.

### Types d'addresses

Les EndpointSlices supportent 3 types d'addresses :

* IPv4
* IPv6
* FQDN (Fully Qualified Domain Name) - [nom de domaine entièrement qualifié]

### Topologie

Chaque Endpoint dans un EndpointSlice peut contenir des informations de topologie pertinentes.
Ceci est utilisé pour indiquer où se trouve un Endpoint, qui contient les informations sur le Node, zone et région correspondantes. Lorsque les valeurs sont disponibles, les labels de Topologies suivants seront définis par le contrôleur EndpointSlice:

* `kubernetes.io/hostname` - Nom du Node sur lequel l'Endpoint se situe.
* `topology.kubernetes.io/zone` - Zone dans laquelle l'Endpoint se situe.
* `topology.kubernetes.io/region` - Région dans laquelle l'Endpoint se situe.

Le contrôleur EndpointSlice surveille les Services et les Pods pour assurer que leurs correspondances avec les EndpointSlices sont à jour.
Le contrôleur gère les EndpointSlices pour tous les Services qui ont un sélecteur - [référence: {{< glossary_tooltip text="sélecteur" term_id="selector" >}}] - specifié. Celles-ci représenteront les IPs des Pods qui correspondent au sélecteur.

### Capacité d'EndpointSlices

Les EndpointSlices sont limités à une capacité de 100 Endpoints chacun, par défaut. Vous pouvez configurer ceci avec l'indicateur `--max-endpoints-per-slice` {{< glossary_tooltip text="kube-controller-manager" term_id="kube-controller-manager" >}} jusqu'à un maximum de 1000.

### Distribution d'EndpointSlices

Chaque EndpointSlice a un ensemble de ports qui s'applique à tous les Endpoints dans la ressource.
Lorsque les ports nommés sont utilisés pour un Service, les Pods peuvent se retrouver avec différents ports cibles pour le même port nommé, nécessitant différents EndpointSlices.

Le contrôleur essaie de remplir les EndpointSlices aussi complètement que possible, mais ne les rééquilibre pas activement. La logique du contrôleur est assez simple:

1. Itérer à travers les EndpointSlices existants, retirer les Endpoints qui ne sont plus voulus et mettre à jour les Endpoints qui ont changé.
2. Itérer à travers les EndpointSlices qui ont été modifiés dans la première étape et les remplir avec n'importe quel Endpoint nécéssaire.
3. S'il reste encore des Endpoints nouveaux à ajouter, essayez de les mettre dans une slice qui n'a pas été changée et/ou en créer une nouvelle.

Par-dessus tout, la troisième étape priorise la limitation de mises à jour d'EndpointSlice sur une distribution complètement pleine d'EndpointSlices. Par exemple, s'il y avait 10 nouveaux Endpoints à ajouter et 2 EndpointSlices qui peuvent contenir 5 Endpoints en plus chacun; cette approche créera un nouveau EndpointSlice au lieu de remplir les EndpointSlice existants. C'est à dire, une seule création EndpointSlice est préférable à plusieurs mises à jour d'EndpointSlices.

Avec kube-proxy exécuté sur chaque Node et surveillant EndpointSlices, chaque changement d'un EndpointSlice devient relativement coûteux puisqu'ils seront transmis à chaque Node du cluster.
Cette approche vise à limiter le nombre de modifications qui doivent être envoyées à chaque Node, même si ça peut causer plusieurs EndpointSlices non remplis.

En pratique, cette distribution bien peu idéale devrait être rare. La plupart des changements traités par le contrôleur EndpointSlice seront suffisamment petits pour tenir dans un EndpointSlice existant, et sinon, un nouveau EndpointSlice aurait probablement été bientôt nécessaire de toute façon. Les mises à jour continues des déploiements fournissent également une compaction naturelle des EndpointSlices avec tous leurs pods et les Endpoints correspondants qui se feront remplacer.

## Motivation

L'API des Endpoints fournit une méthode simple et facile à suivre pour les Endpoints dans Kubernetes. Malheureusement, comme les clusters Kubernetes et Services sont devenus plus grands, les limitations de cette API sont devenues plus visibles. Plus particulièrement, celles-ci comprennent des limitations liées au dimensionnement vers un plus grand nombre d'Endpoints d'un réseau.

Puisque tous les Endpoints d'un réseau pour un Service ont été stockés dans une seule ressource Endpoints, ces ressources pourraient devenir assez lourdes. Cela affecte les performances des composants Kubernetes (notamment le plan de contrôle) et cause une grande quantité de trafic réseau et de traitements lorsque les Endpoints changent. Les EndpointSlices aident à atténuer ces problèmes ainsi qu'à fournir une plate-forme extensible pour des fonctionnalités supplémentaires telles que le routage topologique.



## {{% heading "whatsnext" %}}


* [Activer EndpointSlices](/docs/tasks/administer-cluster/enabling-endpointslices)
* Lire [Connecter des applications aux Services](/docs/concepts/services-networking/connect-applications-service/)

