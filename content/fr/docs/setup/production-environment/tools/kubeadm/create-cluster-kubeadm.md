---
title: Création d'un Cluster a master unique avec kubeadm
description: Création d'un Cluster a master unique avec kubeadm
content_type: task
weight: 30
---

<!-- overview -->

<img src="https://raw.githubusercontent.com/cncf/artwork/master/projects/kubernetes/certified-kubernetes/versionless/color/certified-kubernetes-color.png" align="right" width="150px">**kubeadm** vous aide à démarrer un cluster Kubernetes minimum,
viable et conforme aux meilleures pratiques. Avec kubeadm, votre cluster
doit passer les [tests de Conformance Kubernetes](https://kubernetes.io/blog/2017/10/software-conformance-certification).
 Kubeadm prend également en charge d'autres fonctions du cycle de vie, telles que les mises
 à niveau, la rétrogradation et la gestion des
 [bootstrap tokens](/docs/reference/access-authn-authz/bootstrap-tokens/).

Comme vous pouvez installer kubeadm sur différents types de machines (par exemple, un ordinateur
portable, un serveur,
Raspberry Pi, etc.), il est parfaitement adapté à l'intégration avec des systèmes d'approvisionnement
comme Terraform ou Ansible.

La simplicité de kubeadm lui permet d'être utilisé dans une large gamme de cas d'utilisation:

- Les nouveaux utilisateurs peuvent commencer par kubeadm pour essayer Kubernetes pour la première
fois.
- Les utilisateurs familiarisés avec Kubernetes peuvent créer des clusters avec kubeadm et tester
leurs applications.
- Les projets plus importants peuvent inclure kubeadm en tant que brique de base dans un système
plus complexe pouvant également inclure d'autres outils d'installation.

Kubeadm est conçu pour être un moyen simple pour les nouveaux utilisateurs de commencer à essayer
Kubernetes, pour la première fois éventuellement. C'est un moyen pour les utilisateurs avancés de
tester leur application en même temps qu'un cluster facilement, et aussi être
une brique de base dans un autre écosystème et/ou un outil d’installation avec une plus grand
portée.

Vous pouvez installer très facilement _kubeadm_ sur des systèmes d'exploitation prenant en charge
l'installation des paquets deb ou rpm. Le SIG responsable de kubeadm,
[SIG Cluster Lifecycle](https://github.com/kubernetes/community/tree/master/sig-cluster-lifecycle),
fournit ces paquets pré-construits pour vous,
mais vous pouvez également les construire à partir des sources pour d'autres systèmes d'exploitation.


###  Maturité de kubeadm

| Elément                   | Niveau de maturité |
|---------------------------|--------------------|
| Command line UX           | GA                 |
| Implementation            | GA                 |
| Config file API           | beta               |
| CoreDNS                   | GA                 |
| kubeadm alpha subcommands | alpha              |
| High availability         | alpha              |
| DynamicKubeletConfig      | alpha              |
| Self-hosting              | alpha              |

Les fonctionnalités globales de kubeadm sont **GA**. Quelques sous-fonctionnalités, comme
la configuration, les API de fichiers sont toujours en cours de développement. L'implémentation de la création du cluster
peut changer légèrement au fur et à mesure que l'outil évolue, mais la mise en œuvre globale devrait être assez stable.
Toutes les commandes sous `kubeadm alpha` sont par définition prises en charge au niveau alpha.


### Calendrier de support

Les versions de Kubernetes sont généralement prises en charge pendant neuf mois et pendant cette
période, une version de correctif peut être publiée à partir de la branche de publication si un bug grave ou un
problème de sécurité est trouvé. Voici les dernières versions de Kubernetes et le calendrier de support
 qui s'applique également à `kubeadm`.

| Version de Kubernetes | Date de sortie de la version | Fin de vie     |
|-----------------------|------------------------------|----------------|
| v1.6.x                | Mars 2017                    | Décembre 2017  |
| v1.7.x                | Juin 2017                    | Mars 2018      |
| v1.8.x                | Septembre 2017               | Juin 2018      |
| v1.9.x                | Décembre 2017                | Septembre 2018 |
| v1.10.x               | Mars 2018                    | Décembre 2018  |
| v1.11.x               | Juin 2018                    | Mars 2019      |
| v1.12.x               | Septembre 2018               | Juin 2019      |
| v1.13.x               | Décembre 2018                | Septembre 2019 |



## {{% heading "prerequisites" %}}


- Une ou plusieurs machines exécutant un système d'exploitation compatible deb/rpm, par exemple Ubuntu ou CentOS
- 2 Go ou plus de RAM par machine. Si vous essayez moins cela laissera trop peu de place pour vos applications.
- 2 processeurs ou plus sur le master
- Connectivité réseau entre toutes les machines du cluster, qu'il soit public ou privé.



<!-- steps -->

## Objectifs

* Installer un cluster Kubernetes à master unique ou un
[cluster à haute disponibilité](/fr/docs/setup/production-environment/tools/kubeadm/high-availability/)
* Installez un réseau de pods sur le cluster afin que vos pods puissent se parler

## Instructions

### Installer kubeadm sur vos hôtes

Voir ["Installation de kubeadm"](/fr/docs/setup/production-environment/tools/kubeadm/install-kubeadm/).

{{< note >}}
Si vous avez déjà installé kubeadm, lancez `apt-get update &&
apt-get upgrade` ou `yum update` pour obtenir la dernière version de kubeadm.

Lorsque vous effectuez une mise à niveau, la kubelet redémarre plusieurs fois au bout de quelques
secondes car elle attend dans une boucle de blocage
kubeadm pour lui dire quoi faire. Ce fonctionnement est normal.
Une fois que vous avez initialisé votre master, la kubelet s'exécute normalement.
{{< /note >}}

### Initialiser votre master

Le master est la machine sur laquelle s'exécutent les composants du control plane, y compris
etcd (la base de données du cluster) et l'API serveur (avec lequel la CLI kubectl communique).

1. Choisissez un add-on réseau pour les pods et vérifiez s’il nécessite des arguments à
 passer à l'initialisation de kubeadm. Selon le
fournisseur tiers que vous choisissez, vous devrez peut-être définir le `--pod-network-cidr` sur
une valeur spécifique au fournisseur. Voir [Installation d'un add-on réseau de pod](#pod-network).
1. (Facultatif) Sauf indication contraire, kubeadm utilise l'interface réseau associée
avec la passerelle par défaut pour annoncer l’IP du master. Pour utiliser une autre
interface réseau, spécifiez l'option `--apiserver-advertise-address=<ip-address>`
à `kubeadm init`. Pour déployer un cluster Kubernetes en utilisant l’adressage IPv6, vous devez
 spécifier une adresse IPv6, par exemple `--apiserver-advertise-address=fd00::101`
1. (Optional) Lancez `kubeadm config images pull` avant de faire `kubeadm init` pour vérifier la
connectivité aux registres gcr.io.

Maintenant, lancez:

```bash
kubeadm init <args>
```

### Plus d'information

Pour plus d'informations sur les arguments de `kubeadm init`, voir le
[guide de référence kubeadm](/docs/reference/setup-tools/kubeadm/).

Pour une liste complète des options de configuration, voir la
[documentation du fichier de configuration](/docs/reference/setup-tools/kubeadm/kubeadm-init/#config-file).

Pour personnaliser les composants du control plane, y compris l'affectation facultative d'IPv6
à la sonde liveness, pour les composants du control plane et du serveur etcd, fournissez des arguments
supplémentaires à chaque composant, comme indiqué dans les [arguments personnalisés](/docs/admin/kubeadm#custom-args).

Pour lancer encore une fois `kubeadm init`, vous devez d'abord [détruire le cluster](#tear-down).

Si vous joignez un nœud avec une architecture différente par rapport à votre cluster, créez un
Déploiement ou DaemonSet pour `kube-proxy` et` kube-dns` sur le nœud. C’est nécéssaire car les images Docker pour ces
 composants ne prennent actuellement pas en charge la multi-architecture.

`kubeadm init` exécute d’abord une série de vérifications préalables pour s’assurer que la machine
est prête à exécuter Kubernetes. Ces vérifications préalables exposent des avertissements et se terminent
 en cas d'erreur. Ensuite `kubeadm init` télécharge et installe les composants du control plane du cluster.
Cela peut prendre plusieurs minutes. l'output devrait ressembler à:

```none
[init] Using Kubernetes version: vX.Y.Z
[preflight] Running pre-flight checks
[preflight] Pulling images required for setting up a Kubernetes cluster
[preflight] This might take a minute or two, depending on the speed of your internet connection
[preflight] You can also perform this action in beforehand using 'kubeadm config images pull'
[kubelet-start] Writing kubelet environment file with flags to file "/var/lib/kubelet/kubeadm-flags.env"
[kubelet-start] Writing kubelet configuration to file "/var/lib/kubelet/config.yaml"
[kubelet-start] Activating the kubelet service
[certs] Using certificateDir folder "/etc/kubernetes/pki"
[certs] Generating "etcd/ca" certificate and key
[certs] Generating "etcd/server" certificate and key
[certs] etcd/server serving cert is signed for DNS names [kubeadm-master localhost] and IPs [10.138.0.4 127.0.0.1 ::1]
[certs] Generating "etcd/healthcheck-client" certificate and key
[certs] Generating "etcd/peer" certificate and key
[certs] etcd/peer serving cert is signed for DNS names [kubeadm-master localhost] and IPs [10.138.0.4 127.0.0.1 ::1]
[certs] Generating "apiserver-etcd-client" certificate and key
[certs] Generating "ca" certificate and key
[certs] Generating "apiserver" certificate and key
[certs] apiserver serving cert is signed for DNS names [kubeadm-master kubernetes kubernetes.default kubernetes.default.svc kubernetes.default.svc.cluster.local] and IPs [10.96.0.1 10.138.0.4]
[certs] Generating "apiserver-kubelet-client" certificate and key
[certs] Generating "front-proxy-ca" certificate and key
[certs] Generating "front-proxy-client" certificate and key
[certs] Generating "sa" key and public key
[kubeconfig] Using kubeconfig folder "/etc/kubernetes"
[kubeconfig] Writing "admin.conf" kubeconfig file
[kubeconfig] Writing "kubelet.conf" kubeconfig file
[kubeconfig] Writing "controller-manager.conf" kubeconfig file
[kubeconfig] Writing "scheduler.conf" kubeconfig file
[control-plane] Using manifest folder "/etc/kubernetes/manifests"
[control-plane] Creating static Pod manifest for "kube-apiserver"
[control-plane] Creating static Pod manifest for "kube-controller-manager"
[control-plane] Creating static Pod manifest for "kube-scheduler"
[etcd] Creating static Pod manifest for local etcd in "/etc/kubernetes/manifests"
[wait-control-plane] Waiting for the kubelet to boot up the control plane as static Pods from directory "/etc/kubernetes/manifests". This can take up to 4m0s
[apiclient] All control plane components are healthy after 31.501735 seconds
[uploadconfig] storing the configuration used in ConfigMap "kubeadm-config" in the "kube-system" Namespace
[kubelet] Creating a ConfigMap "kubelet-config-X.Y" in namespace kube-system with the configuration for the kubelets in the cluster
[patchnode] Uploading the CRI Socket information "/var/run/dockershim.sock" to the Node API object "kubeadm-master" as an annotation
[mark-control-plane] Marking the node kubeadm-master as control-plane by adding the label "node-role.kubernetes.io/master=''"
[mark-control-plane] Marking the node kubeadm-master as control-plane by adding the taints [node-role.kubernetes.io/master:NoSchedule]
[bootstrap-token] Using token: <token>
[bootstrap-token] Configuring bootstrap tokens, cluster-info ConfigMap, RBAC Roles
[bootstraptoken] configured RBAC rules to allow Node Bootstrap tokens to post CSRs in order for nodes to get long term certificate credentials
[bootstraptoken] configured RBAC rules to allow the csrapprover controller automatically approve CSRs from a Node Bootstrap Token
[bootstraptoken] configured RBAC rules to allow certificate rotation for all node client certificates in the cluster
[bootstraptoken] creating the "cluster-info" ConfigMap in the "kube-public" namespace
[addons] Applied essential addon: CoreDNS
[addons] Applied essential addon: kube-proxy

Your Kubernetes master has initialized successfully!

To start using your cluster, you need to run the following as a regular user:

  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config

You should now deploy a pod network to the cluster.
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
  https://kubernetes.io/fr/docs/concepts/cluster-administration/addons/

You can now join any number of machines by running the following on each node
as root:

  kubeadm join <master-ip>:<master-port> --token <token> --discovery-token-ca-cert-hash sha256:<hash>
```

Pour que kubectl fonctionne pour votre utilisateur non root, exécutez ces commandes, qui font
 également partie du resultat de la commande `kubeadm init`:

```bash
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

Alternativement, si vous êtes `root`, vous pouvez exécuter:

```bash
export KUBECONFIG=/etc/kubernetes/admin.conf
```

Faites un enregistrement du retour de la commande `kubeadm join` que` kubeadm init` génère. Vous avez
besoin de cette commande pour [joindre des noeuds à votre cluster](#join-nodes).

Le jeton est utilisé pour l'authentification mutuelle entre le master et les nœuds qui veulent le rejoindre.
Le jeton est secret. Gardez-le en sécurité, parce que n'importe qui avec ce
jeton peut ajouter des nœuds authentifiés à votre cluster. Ces jetons peuvent être listés,
créés et supprimés avec la commande `kubeadm token`. Voir le
[Guide de référence kubeadm](/docs/reference/setup-tools/kubeadm/kubeadm-token/).

### Installation d'un add-on réseau {#pod-network}

{{< caution >}}
Cette section contient des informations importantes sur l’ordre d’installation et de déploiement. Lisez-la attentivement avant de continuer.
{{< /caution >}}

Vous devez installer un add-on réseau pour pod afin que vos pods puissent communiquer les uns
avec les autres.

**Le réseau doit être déployé avant toute application. De plus, CoreDNS ne démarrera pas avant
l’installation d’un réseau.
kubeadm ne prend en charge que les réseaux basés sur un CNI (et ne prend pas
en charge kubenet).**

Plusieurs projets fournissent des réseaux de pod Kubernetes utilisant CNI, dont certains
supportent les [network policies](/docs/concepts/services-networking/networkpolicies/).
Allez voir la [page des add-ons](/docs/concepts/cluster-administration/addons/) pour une liste complète
des add-ons réseau disponibles.
- Le support IPv6 a été ajouté dans [CNI v0.6.0](https://github.com/containernetworking/cni/releases/tag/v0.6.0).
- [CNI bridge](https://github.com/containernetworking/plugins/blob/master/plugins/main/bridge/README.md) et
[local-ipam](https://github.com/containernetworking/plugins/blob/master/plugins/ipam/host-local/README.md)
sont les seuls plug-ins de réseau IPv6 pris en charge dans Kubernetes version 1.9.

Notez que kubeadm configure un cluster sécurisé par défaut et impose l’utilisation de
[RBAC](/docs/reference/access-authn-authz/rbac/).
Assurez-vous que votre manifeste de réseau prend en charge RBAC.

Veuillez également à ce que votre réseau Pod ne se superpose à aucun des réseaux hôtes,
car cela pourrait entraîner des problèmes.
Si vous constatez une collision entre le réseau de pod de votre plug-in de réseau et certains
de vos réseaux hôtes,
vous devriez penser à un remplacement de CIDR approprié et l'utiliser lors de `kubeadm init` avec
` --pod-network-cidr` et en remplacement du YAML de votre plugin réseau.
Vous pouvez installer un add-on réseau de pod avec la commande suivante:

```bash
kubectl apply -f <add-on.yaml>
```

Vous ne pouvez installer qu'un seul réseau de pod par cluster.

{{< tabs name="tabs-pod-install" >}}
{{% tab name="Choisissez-en un..." %}}
Sélectionnez l'un des onglets pour consulter les instructions d'installation du fournisseur
de réseau de pods.{{% /tab %}}

{{% tab name="Calico" %}}
Pour plus d'informations sur l'utilisation de Calico, voir
[Guide de démarrage rapide de Calico sur Kubernetes](https://docs.projectcalico.org/latest/getting-started/kubernetes/),
[Installation de Calico pour les netpols ( network policies ) et le réseau](https://docs.projectcalico.org/latest/getting-started/kubernetes/installation/calico), ainsi que d'autres resources liées à ce sujet.

Pour que Calico fonctionne correctement, vous devez passer `--pod-network-cidr = 192.168.0.0 / 16`
à` kubeadm init` ou mettre à jour le fichier `calico.yml` pour qu'il corresponde à votre réseau de Pod.
Notez que Calico fonctionne uniquement sur `amd64`,` arm64`, `ppc64le` et` s390x`.

```shell
kubectl apply -f https://docs.projectcalico.org/v3.8/manifests/calico.yaml
```

{{% /tab %}}
{{% tab name="Canal" %}}
Canal utilise Calico pour les netpols et Flannel pour la mise en réseau. Reportez-vous à la
documentation Calico pour obtenir le [guide de démarrage officiel](https://docs.projectcalico.org/latest/getting-started/kubernetes/installation/flannel).

Pour que Canal fonctionne correctement, `--pod-network-cidr = 10.244.0.0 / 16` doit être passé à
` kubeadm init`. Notez que Canal ne fonctionne que sur `amd64`.

```shell
kubectl apply -f https://docs.projectcalico.org/v3.8/manifests/canal.yaml
```

{{% /tab %}}

{{% tab name="Cilium" %}}
Pour plus d'informations sur l'utilisation de Cilium avec Kubernetes, voir
[Guide d'installation de Kubernetes pour Cilium](https://docs.cilium.io/en/stable/kubernetes/).

Ces commandes déploieront Cilium avec son propre etcd géré par l'opérateur etcd.

Note: Si vous utilisez kubeadm dans un seul noeud, veuillez enlever sa marque (taint) pour que
les pods etcd-operator puissent être déployés dans le nœud du control plane.

```shell
kubectl taint nodes <node-name> node-role.kubernetes.io/master:NoSchedule-
```

Pour déployer Cilium, il vous suffit de lancer:
```shell
kubectl create -f https://raw.githubusercontent.com/cilium/cilium/v1.4/examples/kubernetes/1.13/cilium.yaml
```

Une fois que tous les pods Cilium sont marqués «READY», vous commencez à utiliser votre cluster.
```shell
$ kubectl get pods -n kube-system --selector=k8s-app=cilium
NAME           READY   STATUS    RESTARTS   AGE
cilium-drxkl   1/1     Running   0          18m
```

{{% /tab %}}
{{% tab name="Flannel" %}}

Pour que `flannel` fonctionne correctement, vous devez passer` --pod-network-cidr = 10.244.0.0 / 16` à `kubeadm init`.
Paramétrez `/proc/sys/net/bridge/bridge-nf-call-iptables` à «1» en exécutant
` sysctl net.bridge.bridge-nf-call-iptables = 1`
passez le trafic IPv4 bridged à iptables. Ceci est nécessaire pour que certains plugins CNI
fonctionnent, pour plus d'informations
allez voir [ici](/docs/concepts/cluster-administration/network-plugins/#network-plugin-requirements).

Notez que `flannel` fonctionne sur` amd64`, `arm`,` arm64`, `ppc64le` et` s390x` sous Linux.
Windows (`amd64`) est annoncé comme supporté dans la v0.11.0 mais son utilisation n’est pas
documentée.

```shell
kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/a70459be0084506e4ec919aa1c114638878db11b/Documentation/kube-flannel.yml
```
Pour plus d’informations sur `flannel`, voir [le dépôt CoreOS sur GitHub](https://github.com/coreos/flannel).
{{% /tab %}}

{{% tab name="Kube-router" %}}
Paramétrez `/proc/sys/net/bridge/bridge-nf-call-iptables` à «1» en exécutant
`sysctl net.bridge.bridge-nf-call-iptables = 1`
Cette commande indiquera de passer le trafic IPv4 bridgé à iptables.
Ceci est nécessaire pour que certains plugins CNI fonctionnent, pour plus d'informations
s'il vous plaît allez voir [ici](/docs/concepts/cluster-administration/network-plugins/#network-plugin-requirements).

Kube-router s'appuie sur kube-controller-manager pour allouer le pod CIDR aux nœuds. Par conséquent,
utilisez `kubeadm init` avec l'option` --pod-network-cidr`.

Kube-router fournit un réseau de pod, une stratégie réseau et un proxy de service basé sur un
IP Virtual Server (IPVS) / Linux Virtual Server (LVS) hautement performant.

Pour plus d'informations sur la configuration du cluster Kubernetes avec Kube-router à l'aide de kubeadm,
veuillez consulter le [guide d'installation](https://github.com/cloudnativelabs/kube-router/blob/master/docs/kubeadm.md).
{{% /tab %}}

{{% tab name="Romana" %}}
Paramétrez `/proc/sys/net/bridge/bridge-nf-call-iptables` à` 1` en exécutant
`sysctl net.bridge.bridge-nf-call-iptables = 1`
Cette commande indiquera de passer le trafic IPv4 bridged à iptables. Ceci est nécessaire pour que certains plugins CNI fonctionnent,
pour plus d'informations
veuillez consulter la documentation [ici](/docs/concepts/cluster-administration/network-plugins/#network-plugin-requirements).

Le guide d'installation officiel de Romana est [ici](https://github.com/romana/romana/tree/master/containerize#using-kubeadm).

Romana ne fonctionne que sur `amd64`.

```shell
kubectl apply -f https://raw.githubusercontent.com/romana/romana/master/containerize/specs/romana-kubeadm.yml
```
{{% /tab %}}

{{% tab name="Weave Net" %}}
Paramétrez `/proc/sys/net/bridge/bridge-nf-call-iptables` à «1» en exécutant` sysctl net.bridge.bridge-nf-call-iptables = 1`
Cette commande indiquera de passer le trafic IPv4 bridged à iptables. Ceci est nécessaire pour que certains plugins CNI fonctionnent, pour plus d'informations
s'il vous plaît allez voir [ici](/docs/concepts/cluster-administration/network-plugins/#network-plugin-requirements).

Le guide de configuration officiel de Weave Net est [ici](https://www.weave.works/docs/net/latest/kube-addon/).

Weave Net fonctionne sur `amd64`,` arm`, `arm64` et` ppc64le` sans aucune action supplémentaire requise.
Weave Net paramètre le mode hairpin par défaut. Cela permet aux pods de se connecter via leur adresse IP de service
s'ils ne connaissent pas leur Pod IP.

```shell
kubectl apply -f "https://cloud.weave.works/k8s/net?k8s-version=$(kubectl version | base64 | tr -d '\n')"
```
{{% /tab %}}

{{% tab name="JuniperContrail/TungstenFabric" %}}
Fournit une solution SDN superposée, offrant un réseau multicouches, un réseau de cloud hybride,
prise en charge simultanée des couches superposées, application de la stratégie réseau, isolation du réseau,
chaînage de service et équilibrage de charge flexible.

Il existe de nombreuses manières flexibles d’installer JuniperContrail / TungstenFabric CNI.

Veuillez vous référer à ce guide de démarrage rapide: [TungstenFabric](https://tungstenfabric.github.io/website/)
{{% /tab %}}
{{< /tabs >}}


Une fois qu'un réseau de pod a été installé, vous pouvez vérifier qu'il fonctionne en
vérifiant que le pod CoreDNS est en cours d’exécution dans l'output de `kubectl get pods --all-namespaces`.
Et une fois que le pod CoreDNS est opérationnel, vous pouvez continuer en joignant vos nœuds.

Si votre réseau ne fonctionne pas ou si CoreDNS n'est pas en cours d'exécution, vérifiez
notre [documentation de dépannage](/fr/docs/setup/production-environment/tools/kubeadm/troubleshooting-kubeadm/).

### Isolation des nœuds du control plane

Par défaut, votre cluster ne déploie pas de pods sur le master pour des raisons de sécurité.
Si vous souhaitez pouvoir déployer des pods sur le master, par exemple, pour un
cluster Kubernetes mono-machine pour le développement, exécutez:

```bash
kubectl taint nodes --all node-role.kubernetes.io/master-
```

Avec un resultat ressemblant à quelque chose comme:

```
node "test-01" untainted
taint "node-role.kubernetes.io/master:" not found
taint "node-role.kubernetes.io/master:" not found
```

Cela supprimera la marque `node-role.kubernetes.io/master` de tous les nœuds qui
l'ont, y compris du nœud master, ce qui signifie que le scheduler sera alors capable
de déployer des pods partout.

### Faire rejoindre vos nœuds {#join-nodes}

Les nœuds sont ceux sur lesquels vos workloads (conteneurs, pods, etc.) sont exécutées.
 Pour ajouter de nouveaux nœuds à votre cluster, procédez comme suit pour chaque machine:

* SSH vers la machine
* Devenir root (par exemple, `sudo su-`)
* Exécutez la commande qui a été récupérée sur l'output de `kubeadm init`. Par exemple:

``` bash
kubeadm join --token <token> <master-ip>:<master-port> --discovery-token-ca-cert-hash sha256:<hash>
```

Si vous n'avez pas le jeton, vous pouvez l'obtenir en exécutant la commande suivante sur le nœud master:
``` bash
kubeadm token list
```

L'output est similaire à ceci:
``` console
TOKEN                    TTL  EXPIRES              USAGES           DESCRIPTION            EXTRA GROUPS
8ewj1p.9r9hcjoqgajrj4gi  23h  2018-06-12T02:51:28Z authentication,  The default bootstrap  system:
                                                   signing          token generated by     bootstrappers:
                                                                    'kubeadm init'.        kubeadm:
                                                                                           default-node-token
```

Par défaut, les jetons expirent après 24 heures. Si vous joignez un nœud au cluster après
l’expiration du jeton actuel,
vous pouvez créer un nouveau jeton en exécutant la commande suivante sur le nœud maître:
``` bash
kubeadm token create
```

L'output est similaire à ceci:
``` console
5didvk.d09sbcov8ph2amjw
```

Si vous n'avez pas la valeur `--discovery-token-ca-cert-hash`, vous pouvez l'obtenir en
exécutant la suite de commande suivante sur le nœud master:
``` bash
openssl x509 -pubkey -in /etc/kubernetes/pki/ca.crt | openssl rsa -pubin -outform der 2>/dev/null | \
   openssl dgst -sha256 -hex | sed 's/^.* //'
```

L'output est similaire à ceci:
``` console
8cb2de97839780a412b93877f8507ad6c94f73add17d5d7058e91741c9d5ec78
```

{{< note >}}
Pour spécifier un tuple IPv6 pour `<maître-ip>: <maître-port>`, l'adresse IPv6 doit être placée
entre crochets, par exemple: `[fd00 :: 101]: 2073`.{{< /note >}}

Le resultat devrait ressembler à quelque chose comme:
```
[preflight] Running pre-flight checks

... (log output of join workflow) ...

Node join complete:
* Certificate signing request sent to master and response
  received.
* Kubelet informed of new secure connection details.

Run 'kubectl get nodes' on the master to see this machine join.
```

Quelques secondes plus tard, vous remarquerez ce nœud dans l'output de `kubectl get
node`.

### (Optionnel) Contrôler votre cluster à partir de machines autres que le master

Afin d'utiliser kubectl sur une autre machine (par exemple, un ordinateur portable) pour communiquer avec votre
cluster, vous devez copier le fichier administrateur kubeconfig de votre master
sur votre poste de travail comme ceci:

``` bash
scp root@<master ip>:/etc/kubernetes/admin.conf .
kubectl --kubeconfig ./admin.conf get nodes
```

{{< note >}}
L'exemple ci-dessus suppose que l'accès SSH est activé pour root. Si ce n'est pas le cas,
 vous pouvez copier le fichier `admin.conf` pour qu'il soit accessible à un autre utilisateur.
et `scp` en utilisant cet autre utilisateur à la place.

Le fichier `admin.conf` donne à l'utilisateur _superuser_ des privilèges sur le cluster.
Ce fichier doit être utilisé avec parcimonie. Pour les utilisateurs normaux, il est recommandé de
générer une information d'identification unique pour laquelle vous ajoutez des privilèges à la liste blanche
 (whitelist).
Vous pouvez faire ceci avec `kubeadm alpha kubeconfig utilisateur --nom-client <CN>`.
Le resultat de cette commande génèrera un fichier KubeConfig qui sera envoyé sur STDOUT, que vous
devrez enregistrer dans un fichier et donner à votre utilisateur. Après cela, créez la whitelist des
privilèges en utilisant `kubectl create (cluster) rolebinding.`
{{< /note >}}

### (Facultatif) Proxifier l'API Server vers localhost

Si vous souhaitez vous connecter à l'API server à partir de l'éxterieur du cluster, vous pouvez utiliser
`kubectl proxy`:

```bash
scp root@<master ip>:/etc/kubernetes/admin.conf .
kubectl --kubeconfig ./admin.conf proxy
```

Vous pouvez maintenant accéder à l'API server localement à `http://localhost:8001/api/v1`

## Destruction {#tear-down}

Pour annuler ce que kubeadm a fait, vous devez d’abord
[drainer le nœud](/docs/reference/generated/kubectl/kubectl-commands#drain)
et assurez-vous que le nœud est vide avant de l'arrêter.
En communiquant avec le master en utilisant les informations d'identification appropriées, exécutez:
```bash
kubectl drain <node name> --delete-local-data --force --ignore-daemonsets
kubectl delete node <node name>
```

Ensuite, sur le nœud en cours de suppression, réinitialisez l'état de tout ce qui concerne kubeadm:
```bash
kubeadm reset
```

Le processus de réinitialisation ne réinitialise pas et ne nettoie pas les règles iptables ni les
tables IPVS. Si vous souhaitez réinitialiser iptables, vous devez le faire manuellement:
```bash
iptables -F && iptables -t nat -F && iptables -t mangle -F && iptables -X
```

Si vous souhaitez réinitialiser les tables IPVS, vous devez exécuter la commande suivante:
```bash
ipvsadm -C
```

Si vous souhaitez recommencer Il suffit de lancer `kubeadm init` ou` kubeadm join` avec les
arguments appropriés.
Plus d'options et d'informations sur la
[`commande de réinitialisation de kubeadm`](/docs/reference/setup-tools/kubeadm/kubeadm-reset/).

## Maintenir un cluster {#lifecycle}

Vous trouverez des instructions pour la maintenance des clusters kubeadm (mises à niveau,
rétrogradation, etc.) [ici](/docs/tasks/administer-cluster/kubeadm)

## Explorer les autres add-ons {#other-addons}

Parcourez la [liste des add-ons](/docs/concepts/cluster-administration/addons/),
y compris des outils pour la journalisation, la surveillance, la stratégie réseau, la visualisation
et le contrôle de votre cluster Kubernetes.

## Et après ? {#whats-next}

* Vérifiez que votre cluster fonctionne correctement avec [Sonobuoy](https://github.com/heptio/sonobuoy)
* En savoir plus sur l'utilisation avancée de kubeadm dans la
[documentation de référence de kubeadm](/docs/reference/setup-tools/kubeadm/kubeadm)
* En savoir plus sur Kubernetes [concepts](/docs/concepts/) et [`kubectl`](/docs/user-guide/kubectl-overview/).
* Configurez la rotation des logs. Vous pouvez utiliser **logrotate** pour cela. Lorsque vous utilisez Docker,
 vous pouvez spécifier des options de rotation des logs pour le démon Docker, par exemple
  `--log-driver = fichier_json --log-opt = taille_max = 10m --log-opt = fichier_max = 5`.
  Consultez [Configurer et dépanner le démon Docker](https://docs.docker.com/engine/admin/) pour plus de détails.

## Feedback {#feedback}

* Pour les bugs, visitez [kubeadm GitHub issue tracker](https://github.com/kubernetes/kubeadm/issues)
* Pour le support, rendez vous sur le Channel Slack kubeadm:
  [#kubeadm](https://kubernetes.slack.com/messages/kubeadm/)
* Le Channel Slack: General SIG Cluster Lifecycle Development:
  [#sig-cluster-lifecycle](https://kubernetes.slack.com/messages/sig-cluster-lifecycle/)
* [SIG Cluster Lifecycle SIG information](#TODO)
* SIG Cluster Lifecycle Mailing List:
  [kubernetes-sig-cluster-lifecycle](https://groups.google.com/forum/#!forum/kubernetes-sig-cluster-lifecycle)

## Politique de compatibilité de versions {#version-skew-policy}

L'outil CLI kubeadm de la version vX.Y peut déployer des clusters avec un control
plane de la version vX.Y ou vX. (Y-1).
kubeadm CLI vX.Y peut également mettre à niveau un cluster existant créé par kubeadm
 de la version vX. (Y-1).

Pour cette raison, nous ne pouvons pas voir plus loin, kubeadm CLI vX.Y peut ou pas être
en mesure de déployer des clusters vX. (Y + 1).

Exemple: kubeadm v1.8 peut déployer des clusters v1.7 et v1.8 et mettre à niveau des
clusters v1.7 créés par kubeadm vers
v1.8.

Ces ressources fournissent plus d'informations sur le saut de version pris en
charge entre les kubelets et le control plane, ainsi que sur d'autres composants Kubernetes:

* [politique de compatibilité de versions](/docs/setup/version-skew-policy/) de Kubernetes
* [Guide d'installation](/fr/docs/setup/production-environment/tools/kubeadm/install-kubeadm/#installing-kubeadm-kubelet-and-kubectl)
spécifique à Kubeadm

## kubeadm fonctionne sur plusieurs plates-formes {#multi-platform}

Les packages et fichiers binaires de kubeadm deb/rpm sont conçus pour amd64, arm (32 bits), arm64, ppc64le et s390x
suite à la [multiplateforme proposal](https://github.com/kubernetes/community/blob/master/contributors/design-proposals/multi-platform.md).

Les images de conteneur multiplatform pour le control plane et les addons sont également pris en charge depuis la v1.12.

Seuls certains fournisseurs de réseau proposent des solutions pour toutes les plateformes. Veuillez consulter la liste des
fournisseurs de réseau ci-dessus ou la documentation de chaque fournisseur pour déterminer si le fournisseur
prend en charge votre plate-forme.

## Limitations {#limitations}

Remarque: kubeadm évolue continuellement et ces limitations seront résolues en temps voulu.

* Le cluster créé ici a un seul master, avec une seule base de données etcd. Cela signifie que
si le master est irrécupérable, votre cluster peut perdre ses données et peut avoir besoin d'être recréé à
partir de zéro. L'ajout du support HA (plusieurs serveurs etcd, plusieurs API servers, etc.)
à kubeadm est encore en cours de developpement.

   Contournement: régulièrement [sauvegarder etcd](https://coreos.com/etcd/docs/latest/admin_guide.html).
le répertoire des données etcd configuré par kubeadm se trouve dans `/var/lib/etcd` sur le master.

## Diagnostic {#troubleshooting}

Si vous rencontrez des difficultés avec kubeadm, veuillez consulter nos
 [troubleshooting docs](/fr/docs/setup/production-environment/tools/kubeadm/troubleshooting-kubeadm/).
