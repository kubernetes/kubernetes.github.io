---
title: Cloud Controller Manager
id: cloud-controller-manager
date: 2018-04-12
full_link: /docs/tasks/administer-cluster/running-cloud-controller/
short_description: >
  Le Cloud Controller Manager est une fonctionnalité alpha de la version 1.8. Dans les prochaines versions, il deviendra le moyen privilégié pour l'intégration de Kubernetes à n'importe quel cloud.

aka:
tags:
- core-object
- architecture
- operation
---
 Le Cloud Controller Manager est une fonctionnalité alpha de la version 1.8. Dans les prochaines versions, il deviendra le moyen privilégié pour l'intégration de Kubernetes à n'importe quel cloud.

<!--more-->

Kubernetes v1.6 contient un nouveau binaire appelé cloud-controller-manager. Le cloud-controller-manager est un service qui intègre des boucles de contrôle propres au cloud. Ces boucles de contrôle spécifiques au cloud se trouvaient à l'origine dans le kube-controller-manager. Étant donné que les fournisseurs de cloud développent et mettent à jour leurs produits à un rythme différent de celui du projet Kubernetes, l'abstraction du code spécifique au fournisseur, au niveau du binaire cloud-controller-manager, permet aux fournisseurs de cloud d'évoluer indépendamment du code principal de Kubernetes.
