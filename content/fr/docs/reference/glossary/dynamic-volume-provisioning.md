---
title: Provisionnement Dynamique de Volume
id: dynamicvolumeprovisioning
date: 2018-04-12
full_link: /docs/concepts/storage/dynamic-provisioning
short_description: >
  Permet aux utilisateurs de demander la création automatique de Volumes de stockage.

aka:
tags:
- core-object
- storage
---
 Permet aux utilisateurs de demander la création automatique de {{< glossary_tooltip text="Volumes" term_id="volume" >}} de stockage.

<!--more-->

Le provisionnement dynamique élimine le besoin, pour les administrateurs de cluster, de pré-provisionner le stockage. Au lieu de cela, il provisionne automatiquement le stockage à la demande de l'utilisateur. Le provisionnement dynamique de volume est basé sur un objet API, la {{< glossary_tooltip text="Class de Stockage" term_id="storage-class" >}}, se référant à un {{< glossary_tooltip text="Plugin de Volume" term_id="volume-plugin" >}} qui provisionne un {{< glossary_tooltip text="Volume" term_id="volume" >}} ainsi qu'un ensemble de paramètres à passer au Plugin de Volume.
