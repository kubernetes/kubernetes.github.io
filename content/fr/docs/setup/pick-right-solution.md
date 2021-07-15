---
reviewers:
- yastij
title: Choisir la bonne solution
description: Panorama de solutions Kubernetes
weight: 10
content_type: concept
---

<!-- overview -->

Kubernetes peut fonctionner sur des plateformes variées: sur votre PC portable, sur des VMs d'un fournisseur de cloud, ou un rack
de serveurs bare-metal. L'effort demandé pour configurer un cluster varie de l'éxécution d'une simple commande à la création
de votre propre cluster personnalisé. Utilisez ce guide pour choisir la solution qui correspond le mieux à vos besoins.

Si vous voulez simplement jeter un coup d'oeil rapide, utilisez alors de préférence les [solutions locales basées sur Docker](#solutions-locales).

Lorsque vous êtes prêts à augmenter le nombre de machines et souhaitez bénéficier de la haute disponibilité, une
[solution hébergée](#solutions-hebergées) est la plus simple à déployer et à maintenir.

[Les solutions cloud clés en main](#solutions-clés-en-main) ne demandent que peu de commande pour déployer et couvrent un large panel de
 fournisseurs de cloud. [Les solutions clés en main pour cloud privé](#solutions-on-premises-clés-en-main) possèdent la simplicité des solutions cloud clés en main combinées avec la sécurité de votre propre réseau privé.

Si vous avez déjà un moyen de configurer vos resources, utilisez [kubeadm](/fr/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/) pour facilement
déployer un cluster grâce à une seule ligne de commande par machine.

[Les solutions personnalisées](#solutions-personnalisées) varient d'instructions pas à pas, à des conseils relativement généraux pour déployer un

cluster Kubernetes en partant du début.



<!-- body -->

## Solutions locales

* [Minikube](/fr/docs/setup/learning-environment/minikube/) est une méthode pour créer un cluster Kubernetes local à noeud unique pour le développement et le test. L'installation est entièrement automatisée et ne nécessite pas de compte de fournisseur de cloud.

* [Docker Desktop](https://www.docker.com/products/docker-desktop) est une
application facile à installer pour votre environnement Mac ou Windows qui vous permet de
commencer à coder et déployer votre code dans des conteneurs en quelques minutes sur un nœud unique Kubernetes.

* [Minishift](https://docs.okd.io/latest/minishift/) installe la version communautaire de la plate-forme d'entreprise OpenShift
de Kubernetes pour le développement local et les tests. Il offre une VM tout-en-un (`minishift start`) pour Windows, macOS et Linux,
 le `oc cluster up` containerisé (Linux uniquement) et [est livré avec quelques Add Ons faciles à installer](https://github.com/minishift/minishift-addons/tree/master/add-ons).

* [MicroK8s](https://microk8s.io/) fournit une commande unique d'installation de la dernière version de Kubernetes sur une machine locale
pour le développement et les tests. L'installation est rapide (~30 sec) et supporte de nombreux plugins dont Istio avec une seule commande.

* [IBM Cloud Private-CE (Community Edition)](https://github.com/IBM/deploy-ibm-cloud-private) peut utiliser VirtualBox sur votre machine
pour déployer Kubernetes sur une ou plusieurs machines virtuelles afin de développer et réaliser des scénarios de test. Cette solution
peut créer un cluster multi-nœuds complet.

* [IBM Cloud Private-CE (Community Edition) sur Linux Containers](https://github.com/HSBawa/icp-ce-on-linux-containers) est un script IaC (Infrastructure as Code) basé sur Terraform/Packer/BASH pour créer un cluster LXD à sept nœuds (1 Boot, 1 Master, 1 Management, 1 Proxy et 3 Workers) sur une machine Linux.

* [Kubeadm-dind](https://github.com/kubernetes-sigs/kubeadm-dind-cluster) est un cluster Kubernetes multi-nœuds (tandis que minikube est
un nœud unique) qui ne nécessite qu'un docker-engine. Il utilise la technique du docker-in-docker pour déployer le cluster Kubernetes.

* [Ubuntu sur LXD](/docs/getting-start-guides/ubuntu/local/) supporte un déploiement de 9 instances sur votre machine locale.

## Solutions hebergées

* [AppsCode.com](https://appscode.com/products/cloud-deployment/) fournit des clusters Kubernetes managés pour divers clouds publics, dont AWS et Google Cloud Platform.

* [APPUiO](https://appuio.ch) propose une plate-forme de cloud public OpenShift, supportant n'importe quel workload Kubernetes. De plus, APPUiO propose des Clusters OpenShift privés et managés, fonctionnant sur n'importe quel cloud public ou privé.

* [Amazon Elastic Container Service for Kubernetes](https://aws.amazon.com/eks/) offre un service managé de Kubernetes.

* [Azure Kubernetes Service](https://azure.microsoft.com/services/container-service/) offre des clusters Kubernetes managés.

* [Containership Kubernetes Engine (CKE)](https://containership.io/containership-platform) Approvisionnement et gestion intuitive de clusters
 Kubernetes sur GCP, Azure, AWS, Packet, et DigitalOcean. Mises à niveau transparentes, auto-scaling, métriques, création de
workloads, et plus encore.

* [DigitalOcean Kubernetes](https://www.digitalocean.com/products/kubernetes/) offre un service managé de Kubernetes.

* [Giant Swarm](https://giantswarm.io/product/) offre des clusters Kubernetes managés dans leur propre centre de données, on-premises ou sur des clouds public.

* [Google Kubernetes Engine](https://cloud.google.com/kubernetes-engine/) offre des clusters Kubernetes managés.

* [IBM Cloud Kubernetes Service](https://cloud.ibm.com/docs/containers?topic=containers-getting-started) offre des clusters Kubernetes managés avec choix d'isolation, des outils opérationnels, une vision intégrée de la sécurité des images et des conteneurs et une intégration avec Watson, IoT et les données.

* [Kubermatic](https://www.loodse.com) fournit des clusters Kubernetes managés pour divers clouds publics, y compris AWS et Digital Ocean, ainsi que sur site avec intégration OpenStack.

* [Kublr](https://kublr.com) offre des clusters Kubernetes sécurisés, évolutifs et hautement fiables sur AWS, Azure, GCP et on-premises,
 de qualité professionnelle. Il inclut la sauvegarde et la reprise après sinistre prêtes à l'emploi, la journalisation et la surveillance centralisées multi-clusters, ainsi qu'une fonction d'alerte intégrée.

* [Madcore.Ai](https://madcore.ai) est un outil CLI orienté développement pour déployer l'infrastructure Kubernetes dans AWS. Les masters, un groupe d'autoscaling pour les workers sur des spot instances, les ingress-ssl-lego, Heapster, et Grafana.

* [Nutanix Karbon](https://www.nutanix.com/products/karbon/) est une plateforme de gestion et d'exploitation Kubernetes multi-clusters hautement disponibles qui simplifie l'approvisionnement, les opérations et la gestion du cycle de vie de Kubernetes.

* [OpenShift Dedicated](https://www.openshift.com/dedicated/) offre des clusters Kubernetes gérés et optimisés par OpenShift.

* [OpenShift Online](https://www.openshift.com/features/) fournit un accès hébergé gratuit aux applications Kubernetes.

* [Oracle Container Engine for Kubernetes](https://docs.us-phoenix-1.oraclecloud.com/Content/ContEng/Concepts/contengoverview.htm) est un service entièrement géré, évolutif et hautement disponible que vous pouvez utiliser pour déployer vos applications conteneurisées dans le cloud.

* [Platform9](https://platform9.com/products/kubernetes/) offre des Kubernetes gérés on-premises ou sur n'importe quel cloud public, et fournit une surveillance et des alertes de santé 24h/24 et 7j/7. (Kube2go, une plate-forme de service de déploiement de cluster Kubernetes pour le déploiement de l'interface utilisateur Web9, a été intégrée à Platform9 Sandbox.)

* [Scaleway Kapsule](https://www.scaleway.com/fr/kubernetes-kapsule/) fournit des clusters Kubernetes gérés, évolutifs, avec un large choix d'instances (CPU, mémoire, GPU, etc...) basé sur le cloud public Scaleway et propose aussi les services associés tel que les répartiteurs de charge et registre de conteneurs.

* [Stackpoint.io](https://stackpoint.io) fournit l'automatisation et la gestion de l'infrastructure Kubernetes pour plusieurs clouds publics.

* [SysEleven MetaKube](https://www.syseleven.io/products-services/managed-kubernetes/) offre un Kubernetes-as-a-Service sur un cloud public OpenStack. Il inclut la gestion du cycle de vie, les tableaux de bord d'administration, la surveillance, la mise à l'échelle automatique et bien plus encore.

* [VMware Cloud PKS](https://cloud.vmware.com/vmware-cloud-pks) est une offre d'entreprise Kubernetes-as-a-Service faisant partie du catalogue de services Cloud VMware qui fournit des clusters Kubernetes faciles à utiliser, sécurisés par défaut, rentables et basés sur du SaaS.

## Solutions clés en main

Ces solutions vous permettent de créer des clusters Kubernetes sur une gamme de fournisseurs de Cloud IaaaS avec seulement
quelques commandes. Ces solutions sont activement développées et bénéficient du soutien actif de la communauté.

* [Agile Stacks](https://www.agilestacks.com/products/kubernetes)
* [Alibaba Cloud](/docs/setup/turnkey/alibaba-cloud/)
* [APPUiO](https://appuio.ch)
* [AWS](/docs/setup/turnkey/aws/)
* [Azure](/docs/setup/turnkey/azure/)
* [CenturyLink Cloud](/docs/setup/turnkey/clc/)
* [Conjure-up Kubernetes with Ubuntu on AWS, Azure, Google Cloud, Oracle Cloud](/docs/getting-started-guides/ubuntu/)
* [Containership](https://containership.io/containership-platform)
* [Docker Enterprise](https://www.docker.com/products/docker-enterprise)
* [Gardener](https://gardener.cloud/)
* [Giant Swarm](https://giantswarm.io)
* [Google Compute Engine (GCE)](/docs/setup/turnkey/gce/)
* [IBM Cloud](https://github.com/patrocinio/kubernetes-softlayer)
* [Kontena Pharos](https://kontena.io/pharos/)
* [Kubermatic](https://cloud.kubermatic.io)
* [Kublr](https://kublr.com/)
* [Madcore.Ai](https://madcore.ai/)
* [Nirmata](https://nirmata.com/)
* [Nutanix Karbon](https://www.nutanix.com/products/karbon/)
* [Oracle Container Engine for K8s](https://docs.us-phoenix-1.oraclecloud.com/Content/ContEng/Concepts/contengprerequisites.htm)
* [Pivotal Container Service](https://pivotal.io/platform/pivotal-container-service)
* [Rancher 2.0](https://rancher.com/docs/rancher/v2.x/en/)
* [Stackpoint.io](/docs/setup/turnkey/stackpoint/)
* [Tectonic by CoreOS](https://coreos.com/tectonic)
* [VMware Cloud PKS](https://cloud.vmware.com/vmware-cloud-pks)

## Solutions On-Premises clés en main

Ces solutions vous permettent de créer des clusters Kubernetes sur votre cloud privé sécurisé avec seulement quelques commandes.

* [Agile Stacks](https://www.agilestacks.com/products/kubernetes)
* [APPUiO](https://appuio.ch)
* [Docker Enterprise](https://www.docker.com/products/docker-enterprise)
* [Giant Swarm](https://giantswarm.io)
* [GKE On-Prem | Google Cloud](https://cloud.google.com/gke-on-prem/)
* [IBM Cloud Private](https://www.ibm.com/cloud-computing/products/ibm-cloud-private/)
* [Kontena Pharos](https://kontena.io/pharos/)
* [Kubermatic](https://www.loodse.com)
* [Kublr](https://kublr.com/)
* [Mirantis Cloud Platform](https://www.mirantis.com/software/kubernetes/)
* [Nirmata](https://nirmata.com/)
* [OpenShift Container Platform](https://www.openshift.com/products/container-platform/) (OCP) by [Red Hat](https://www.redhat.com)
* [Pivotal Container Service](https://pivotal.io/platform/pivotal-container-service)
* [Rancher 2.0](https://rancher.com/docs/rancher/v2.x/en/)
* [SUSE CaaS Platform](https://www.suse.com/products/caas-platform)
* [SUSE Cloud Application Platform](https://www.suse.com/products/cloud-application-platform/)

## Solutions personnalisées

Kubernetes peut fonctionner sur une large gamme de fournisseurs de Cloud et d'environnements bare-metal, ainsi qu'avec de nombreux
systèmes d'exploitation.

Si vous pouvez trouver un guide ci-dessous qui correspond à vos besoins, utilisez-le. C'est peut-être un peu dépassé, mais...
ce sera plus facile que de partir de zéro. Si vous voulez repartir de zéro, soit parce que vous avez des exigences particulières,
ou simplement parce que vous voulez comprendre ce qu'il y a à l'interieur de Kubernetes
essayez le guide [Getting Started from Scratch](/docs/setup/release/building-from-source/).

### Universel

Si vous avez déjà un moyen de configurer les ressources d'hébergement, utilisez
[kubeadm](/fr/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/) pour déployer facilement un cluster
avec une seule commande par machine.

### Cloud

Ces solutions sont des combinaisons de fournisseurs de cloud computing et de systèmes d'exploitation qui ne sont pas couverts par les solutions ci-dessus.

* [Cloud Foundry Container Runtime (CFCR)](https://docs-cfcr.cfapps.io/)
* [CoreOS on AWS or GCE](/docs/setup/custom-cloud/coreos/)
* [Gardener](https://gardener.cloud/)
* [Kublr](https://kublr.com/)
* [Kubernetes on Ubuntu](/docs/getting-started-guides/ubuntu/)
* [Kubespray](/docs/setup/custom-cloud/kubespray/)
* [Rancher Kubernetes Engine (RKE)](https://github.com/rancher/rke)

### VMs On-Premises

* [Cloud Foundry Container Runtime (CFCR)](https://docs-cfcr.cfapps.io/)
* [CloudStack](/docs/setup/on-premises-vm/cloudstack/) (uses Ansible, CoreOS and flannel)
* [Fedora (Multi Node)](/docs/getting-started-guides/fedora/flannel_multi_node_cluster/) (uses Fedora and flannel)
* [Nutanix AHV](https://www.nutanix.com/products/acropolis/virtualization/)
* [OpenShift Container Platform](https://www.openshift.com/products/container-platform/) (OCP) Kubernetes platform by [Red Hat](https://www.redhat.com)
* [oVirt](/docs/setup/on-premises-vm/ovirt/)
* [Vagrant](/docs/setup/custom-cloud/coreos/) (uses CoreOS and flannel)
* [VMware](/docs/setup/custom-cloud/coreos/) (uses CoreOS and flannel)
* [VMware vSphere](https://vmware.github.io/vsphere-storage-for-kubernetes/documentation/)
* [VMware vSphere, OpenStack, or Bare Metal](/docs/getting-started-guides/ubuntu/) (uses Juju, Ubuntu and flannel)

### Bare Metal

* [CoreOS](/docs/setup/custom-cloud/coreos/)
* [Digital Rebar](/docs/setup/on-premises-metal/krib/)
* [Docker Enterprise](https://www.docker.com/products/docker-enterprise)
* [Fedora (Single Node)](/docs/getting-started-guides/fedora/fedora_manual_config/)
* [Fedora (Multi Node)](/docs/getting-started-guides/fedora/flannel_multi_node_cluster/)
* [Kubernetes on Ubuntu](/docs/getting-started-guides/ubuntu/)
* [OpenShift Container Platform](https://www.openshift.com/products/container-platform/) (OCP) Kubernetes platform by [Red Hat](https://www.redhat.com)

### Integrations

Ces solutions fournissent une intégration avec des orchestrateurs, des resources managers ou des plateformes tierces.

* [DCOS](/docs/setup/on-premises-vm/dcos/)
  * Community Edition DCOS utilise AWS
  * Enterprise Edition DCOS supporte l'hébergement cloud, les VMs on-premises, et le bare-metal

## Tableau des Solutions

Ci-dessous vous trouverez un tableau récapitulatif de toutes les solutions listées précédemment.

| Fournisseur de IaaS                            | Config. Mgmt.                                                                | OS                                                                       | Réseau                                                                                                           | Docs                                                                                          | Niveau de support                                                                                                                                                                                                                              |
|------------------------------------------------|------------------------------------------------------------------------------|--------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| tous                                           | tous                                                                         | multi-support                                                            | tout les CNI                                                                                                     | [docs](/fr/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/)                                       | Project ([SIG-cluster-lifecycle](https://git.k8s.io/community/sig-cluster-lifecycle))                                                                                                                                                          |
| Google Kubernetes Engine                       |                                                                              |                                                                          | GCE                                                                                                              | [docs](https://cloud.google.com/kubernetes-engine/docs/)                                      | Commercial                                                                                                                                                                                                                                     |
| Docker Enterprise                              | personnalisé                                                                 | [multi-support](https://success.docker.com/article/compatibility-matrix) | [multi-support](https://docs.docker.com/ee/ucp/kubernetes/install-cni-plugin/)                                   | [docs](https://docs.docker.com/ee/)                                                           | Commercial                                                                                                                                                                                                                                     |
| IBM Cloud Private                              | Ansible                                                                      | multi-support                                                            | multi-support                                                                                                    | [docs](https://www.ibm.com/support/knowledgecenter/SSBS6K/product_welcome_cloud_private.html) | [Commercial](https://www.ibm.com/mysupport/s/topic/0TO500000001o0fGAA/ibm-cloud-private?language=en_US&productId=01t50000004X1PWAA0) and [Community](https://www.ibm.com/support/knowledgecenter/SSBS6K_3.1.2/troubleshoot/support_types.html) |
| Red Hat OpenShift                              | Ansible & CoreOS                                                             | RHEL & CoreOS                                                            | [multi-support](https://docs.openshift.com/container-platform/3.11/architecture/networking/network_plugins.html) | [docs](https://docs.openshift.com/container-platform/3.11/welcome/index.html)                 | Commercial                                                                                                                                                                                                                                     |
| Stackpoint.io                                  |                                                                              | multi-support                                                            | multi-support                                                                                                    | [docs](https://stackpoint.io/)                                                                | Commercial                                                                                                                                                                                                                                     |
| AppsCode.com                                   | Saltstack                                                                    | Debian                                                                   | multi-support                                                                                                    | [docs](https://appscode.com/products/cloud-deployment/)                                       | Commercial                                                                                                                                                                                                                                     |
| Madcore.Ai                                     | Jenkins DSL                                                                  | Ubuntu                                                                   | flannel                                                                                                          | [docs](https://madcore.ai)                                                                    | Community ([@madcore-ai](https://github.com/madcore-ai))                                                                                                                                                                                       |
| Platform9                                      |                                                                              | multi-support                                                            | multi-support                                                                                                    | [docs](https://platform9.com/managed-kubernetes/)                                             | Commercial                                                                                                                                                                                                                                     |
| Kublr                                          | personnalisé                                                                 | multi-support                                                            | multi-support                                                                                                    | [docs](http://docs.kublr.com/)                                                                | Commercial                                                                                                                                                                                                                                     |
| Kubermatic                                     |                                                                              | multi-support                                                            | multi-support                                                                                                    | [docs](http://docs.kubermatic.io/)                                                            | Commercial                                                                                                                                                                                                                                     |
| IBM Cloud Kubernetes Service                   |                                                                              | Ubuntu                                                                   | IBM Cloud Networking + Calico                                                                                    | [docs](https://cloud.ibm.com/docs/containers?topic=containers-getting-started)                                         | Commercial                                                                                                                                                                                                                                     |
| Giant Swarm                                    |                                                                              | CoreOS                                                                   | flannel and/or Calico                                                                                            | [docs](https://docs.giantswarm.io/)                                                           | Commercial                                                                                                                                                                                                                                     |
| GCE                                            | Saltstack                                                                    | Debian                                                                   | GCE                                                                                                              | [docs](/docs/setup/turnkey/gce/)                                                              | Project                                                                                                                                                                                                                                        |
| Azure Kubernetes Service                       |                                                                              | Ubuntu                                                                   | Azure                                                                                                            | [docs](https://docs.microsoft.com/en-us/azure/aks/)                                           | Commercial                                                                                                                                                                                                                                     |
| Azure (IaaS)                                   |                                                                              | Ubuntu                                                                   | Azure                                                                                                            | [docs](/docs/setup/turnkey/azure/)                                                            | [Community (Microsoft)](https://github.com/Azure/acs-engine)                                                                                                                                                                                   |
| Bare-metal                                     | personnalisé                                                                 | Fedora                                                                   | _none_                                                                                                           | [docs](/docs/getting-started-guides/fedora/fedora_manual_config/)                             | Project                                                                                                                                                                                                                                        |
| Bare-metal                                     | personnalisé                                                                 | Fedora                                                                   | flannel                                                                                                          | [docs](/docs/getting-started-guides/fedora/flannel_multi_node_cluster/)                       | Community ([@aveshagarwal](https://github.com/aveshagarwal))                                                                                                                                                                                   |
| libvirt                                        | personnalisé                                                                 | Fedora                                                                   | flannel                                                                                                          | [docs](/docs/getting-started-guides/fedora/flannel_multi_node_cluster/)                       | Community ([@aveshagarwal](https://github.com/aveshagarwal))                                                                                                                                                                                   |
| KVM                                            | personnalisé                                                                 | Fedora                                                                   | flannel                                                                                                          | [docs](/docs/getting-started-guides/fedora/flannel_multi_node_cluster/)                       | Community ([@aveshagarwal](https://github.com/aveshagarwal))                                                                                                                                                                                   |
| DCOS                                           | Marathon                                                                     | CoreOS/Alpine                                                            | personnalisé                                                                                                     | [docs](/docs/getting-started-guides/dcos/)                                                    | Community ([Kubernetes-Mesos Authors](https://github.com/mesosphere/kubernetes-mesos/blob/master/AUTHORS.md))                                                                                                                                  |
| AWS                                            | CoreOS                                                                       | CoreOS                                                                   | flannel                                                                                                          | [docs](/docs/setup/turnkey/aws/)                                                              | Community                                                                                                                                                                                                                                      |
| GCE                                            | CoreOS                                                                       | CoreOS                                                                   | flannel                                                                                                          | [docs](/docs/getting-started-guides/coreos/)                                                  | Community ([@pires](https://github.com/pires))                                                                                                                                                                                                 |
| Vagrant                                        | CoreOS                                                                       | CoreOS                                                                   | flannel                                                                                                          | [docs](/docs/getting-started-guides/coreos/)                                                  | Community ([@pires](https://github.com/pires), [@AntonioMeireles](https://github.com/AntonioMeireles))                                                                                                                                         |
| CloudStack                                     | Ansible                                                                      | CoreOS                                                                   | flannel                                                                                                          | [docs](/docs/getting-started-guides/cloudstack/)                                              | Community ([@sebgoa](https://github.com/sebgoa))                                                                                                                                                                                               |
| VMware vSphere                                 | tous                                                                         | multi-support                                                            | multi-support                                                                                                    | [docs](https://vmware.github.io/vsphere-storage-for-kubernetes/documentation/)                | [Community](https://vmware.github.io/vsphere-storage-for-kubernetes/documentation/contactus.html)                                                                                                                                              |
| Bare-metal                                     | personnalisé                                                                 | CentOS                                                                   | flannel                                                                                                          | [docs](/docs/getting-started-guides/centos/centos_manual_config/)                             | Community ([@coolsvap](https://github.com/coolsvap))                                                                                                                                                                                           |
| lxd                                            | Juju                                                                         | Ubuntu                                                                   | flannel/canal                                                                                                    | [docs](/docs/getting-started-guides/ubuntu/local/)                                            | [Commercial](https://www.ubuntu.com/kubernetes) and [Community](https://jujucharms.com/kubernetes)                                                                                                                                             |
| AWS                                            | Juju                                                                         | Ubuntu                                                                   | flannel/calico/canal                                                                                             | [docs](/docs/getting-started-guides/ubuntu/)                                                  | [Commercial](https://www.ubuntu.com/kubernetes) and [Community](https://jujucharms.com/kubernetes)                                                                                                                                             |
| Azure                                          | Juju                                                                         | Ubuntu                                                                   | flannel/calico/canal                                                                                             | [docs](/docs/getting-started-guides/ubuntu/)                                                  | [Commercial](https://www.ubuntu.com/kubernetes) and [Community](https://jujucharms.com/kubernetes)                                                                                                                                             |
| GCE                                            | Juju                                                                         | Ubuntu                                                                   | flannel/calico/canal                                                                                             | [docs](/docs/getting-started-guides/ubuntu/)                                                  | [Commercial](https://www.ubuntu.com/kubernetes) and [Community](https://jujucharms.com/kubernetes)                                                                                                                                             |
| Oracle Cloud                                   | Juju                                                                         | Ubuntu                                                                   | flannel/calico/canal                                                                                             | [docs](/docs/getting-started-guides/ubuntu/)                                                  | [Commercial](https://www.ubuntu.com/kubernetes) and [Community](https://jujucharms.com/kubernetes)                                                                                                                                             |
| Rackspace                                      | personnalisé                                                                 | CoreOS                                                                   | flannel/calico/canal                                                                                             | [docs](https://developer.rackspace.com/docs/rkaas/latest/)                                    | [Commercial](https://www.rackspace.com/managed-kubernetes)                                                                                                                                                                                     |
| VMware vSphere                                 | Juju                                                                         | Ubuntu                                                                   | flannel/calico/canal                                                                                             | [docs](/docs/getting-started-guides/ubuntu/)                                                  | [Commercial](https://www.ubuntu.com/kubernetes) and [Community](https://jujucharms.com/kubernetes)                                                                                                                                             |
| Bare Metal                                     | Juju                                                                         | Ubuntu                                                                   | flannel/calico/canal                                                                                             | [docs](/docs/getting-started-guides/ubuntu/)                                                  | [Commercial](https://www.ubuntu.com/kubernetes) and [Community](https://jujucharms.com/kubernetes)                                                                                                                                             |
| AWS                                            | Saltstack                                                                    | Debian                                                                   | AWS                                                                                                              | [docs](/docs/setup/turnkey/aws/)                                                              | Community ([@justinsb](https://github.com/justinsb))                                                                                                                                                                                           |
| AWS                                            | kops                                                                         | Debian                                                                   | AWS                                                                                                              | [docs](https://github.com/kubernetes/kops/)                                                   | Community ([@justinsb](https://github.com/justinsb))                                                                                                                                                                                           |
| Bare-metal                                     | personnalisé                                                                 | Ubuntu                                                                   | flannel                                                                                                          | [docs](/docs/getting-started-guides/ubuntu/)                                                  | Community ([@resouer](https://github.com/resouer), [@WIZARD-CXY](https://github.com/WIZARD-CXY))                                                                                                                                               |
| oVirt                                          |                                                                              |                                                                          |                                                                                                                  | [docs](/docs/setup/on-premises-vm/ovirt/)                                                     | Community ([@simon3z](https://github.com/simon3z))                                                                                                                                                                                             |
| tous                                           | tous                                                                         | tous                                                                     | tous                                                                                                             | [docs](/docs/setup/release/building-from-source/)                                             | Community ([@erictune](https://github.com/erictune))                                                                                                                                                                                           |
| tous                                           | tous                                                                         | tous                                                                     | tous                                                                                                             | [docs](http://docs.projectcalico.org/v2.2/getting-started/kubernetes/installation/)           | Commercial and Community                                                                                                                                                                                                                       |
| tous                                           | RKE                                                                          | multi-support                                                            | flannel or canal                                                                                                 | [docs](https://rancher.com/docs/rancher/v2.x/en/quick-start-guide/)                           | [Commercial](https://rancher.com/what-is-rancher/overview/) and [Community](https://github.com/rancher/rancher)                                                                                                                                |
| tous                                           | [Gardener Cluster-Operator](https://kubernetes.io/blog/2018/05/17/gardener/) | multi-support                                                            | multi-support                                                                                                    | [docs](https://gardener.cloud)                                                                | [Project/Community](https://github.com/gardener) and [Commercial]( https://cloudplatform.sap.com/)                                                                                                                                             |
| Alibaba Cloud Container Service For Kubernetes | ROS                                                                          | CentOS                                                                   | flannel/Terway                                                                                                   | [docs](https://www.aliyun.com/product/containerservice)                                       | Commercial                                                                                                                                                                                                                                     |
| Agile Stacks                                   | Terraform                                                                    | CoreOS                                                                   | multi-support                                                                                                    | [docs](https://www.agilestacks.com/products/kubernetes)                                       | Commercial                                                                                                                                                                                                                                     |
| IBM Cloud Kubernetes Service                   |                                                                              | Ubuntu                                                                   | calico                                                                                                           | [docs](https://cloud.ibm.com/docs/containers?topic=containers-container_index#container_index)                      | Commercial                                                                                                                                                                                                                                     |
| Digital Rebar                                  | kubeadm                                                                      | tous                                                                     | metal                                                                                                            | [docs](/docs/setup/on-premises-metal/krib/)                                                   | Community ([@digitalrebar](https://github.com/digitalrebar))                                                                                                                                                                                   |
| VMware Cloud PKS                               |                                                                              | Photon OS                                                                | Canal                                                                                                            | [docs](https://docs.vmware.com/en/VMware-Kubernetes-Engine/index.html)                        | Commercial                                                                                                                                                                                                                                     |
| Mirantis Cloud Platform                        | Salt                                                                         | Ubuntu                                                                   | multi-support                                                                                                    | [docs](https://docs.mirantis.com/mcp/)                                                        | Commercial                                                                                                                                                                                                                                     |

{{< note >}}
Le tableau ci-dessus est ordonné par versions testées et utilisées dans les noeuds, suivis par leur niveau de support.
{{< /note >}}

### Définition des colonnes

* **IaaS Provider** est le produit ou l'organisation qui fournit les machines virtuelles ou physiques (nœuds) sur lesquelles Kubernetes fonctionne.
* **OS** est le système d'exploitation de base des nœuds.
* **Config. Mgmt.** est le système de gestion de configuration qui permet d'installer et de maintenir Kubernetes sur les
  nœuds.
* **Le réseau** est ce qui implémente le [modèle de réseau](/docs/concepts/cluster-administration/networking/). Ceux qui ont le type de réseautage
  Aucun_ ne peut pas prendre en charge plus d'un nœud unique, ou peut prendre en charge plusieurs nœuds VM dans un nœud physique unique.
* **Conformité** indique si un cluster créé avec cette configuration a passé la conformité du projet.
  pour le support de l'API et des fonctionnalités de base de Kubernetes v1.0.0.
* **Niveaux de soutien**
  * **Projet** : Les contributeurs de Kubernetes utilisent régulièrement cette configuration, donc elle fonctionne généralement avec la dernière version.
    de Kubernetes.
  * **Commercial** : Une offre commerciale avec son propre dispositif d'accompagnement.
  * **Communauté** : Soutenu activement par les contributions de la communauté. Peut ne pas fonctionner avec les versions récentes de Kubernetes.
  * **Inactif** : Pas de maintenance active. Déconseillé aux nouveaux utilisateurs de Kubernetes et peut être retiré.
* **Note** contient d'autres informations pertinentes, telles que la version de Kubernetes utilisée.

<!-- reference style links below here -->
<!-- GCE conformance test result -->
[1]: https://gist.github.com/erictune/4cabc010906afbcc5061
<!-- Vagrant conformance test result -->
[2]: https://gist.github.com/derekwaynecarr/505e56036cdf010bf6b6
<!-- Google Kubernetes Engine conformance test result -->
[3]: https://gist.github.com/erictune/2f39b22f72565365e59b


