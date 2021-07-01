---
title: Contrôleur
id: controller
date: 2018-04-12
full_link: /docs/admin/kube-controller-manager/
short_description: >
  Boucle de contrôle surveillant l'état partagé du cluster à travers l'apiserver et effectuant des changements en essayant de déplacer l'état actuel vers l'état désiré.

aka:
tags:
- architecture
- fundamental
---
 Boucle de contrôle surveillant l'état partagé du cluster à travers l'{{< glossary_tooltip text="apiserver" term_id="kube-apiserver" >}} et effectuant des changements en essayant de déplacer l'état actuel vers l'état désiré.

<!--more-->

Parmis les contrôleurs livrés aujourd'hui avec Kubernetes se trouvent le contrôleur de réplication, le contrôleur d'endpoints, de namespace et de serviceaccounts.
