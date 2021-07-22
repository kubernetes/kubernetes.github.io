# Documentation de Kubernetes

[![Build Status](https://api.travis-ci.org/kubernetes/website.svg?branch=master)](https://travis-ci.org/kubernetes/website)
[![GitHub release](https://img.shields.io/github/release/kubernetes/website.svg)](https://github.com/kubernetes/website/releases/latest)

Bienvenue !
Ce référentiel contient toutes les informations nécessaires à la construction du site web et de la documentation de Kubernetes.
Nous sommes très heureux que vous vouliez contribuer !

## Contribuer à la rédaction des docs

Vous pouvez cliquer sur le bouton **Fork** en haut à droite de l'écran pour créer une copie de ce dépôt dans votre compte GitHub.
Cette copie s'appelle un *fork*.
Faites tous les changements que vous voulez dans votre fork, et quand vous êtes prêt à nous envoyer ces changements, allez dans votre fork et créez une nouvelle pull request pour nous le faire savoir.

Une fois votre pull request créée, un examinateur de Kubernetes se chargera de vous fournir une revue claire et exploitable.
En tant que propriétaire de la pull request, **il est de votre responsabilité de modifier votre pull request pour tenir compte des commentaires qui vous ont été fournis par l'examinateur de Kubernetes.**
Notez également que vous pourriez vous retrouver avec plus d'un examinateur de Kubernetes pour vous fournir des commentaires ou vous pourriez finir par recevoir des commentaires d'un autre examinateur que celui qui vous a été initialement affecté pour vous fournir ces commentaires.
De plus, dans certains cas, l'un de vos examinateurs peut demander un examen technique à un [examinateur technique de Kubernetes](https://github.com/kubernetes/website/wiki/Tech-reviewers) au besoin.
Les examinateurs feront de leur mieux pour fournir une revue rapidement, mais le temps de réponse peut varier selon les circonstances.

Pour plus d'informations sur la contribution à la documentation Kubernetes, voir :

* [Commencez à contribuer](https://kubernetes.io/docs/contribute/start/)
* [Aperçu des modifications apportées à votre documentation](http://kubernetes.io/docs/contribute/intermediate#view-your-changes-locally)
* [Utilisation des modèles de page](https://kubernetes.io/docs/contribute/style/page-content-types/)
* [Documentation Style Guide](http://kubernetes.io/docs/contribute/style/style-guide/)
* [Traduction de la documentation Kubernetes](https://kubernetes.io/docs/contribute/localization/)

## Exécuter le site localement en utilisant Docker

La façon recommandée d'exécuter le site web Kubernetes localement est d'utiliser une image spécialisée [Docker](https://docker.com) qui inclut le générateur de site statique [Hugo](https://gohugo.io).

> Si vous êtes sous Windows, vous aurez besoin de quelques outils supplémentaires que vous pouvez installer avec [Chocolatey](https://chocolatey.org). `choco install make`

> Si vous préférez exécuter le site Web localement sans Docker, voir [Exécuter le site localement avec Hugo](#exécuter-le-site-localement-en-utilisant-hugo) ci-dessous.

Si vous avez Docker [up and running](https://www.docker.com/get-started), construisez l'image Docker `kubernetes-hugo' localement:

```bash
make container-image
```

Une fois l'image construite, vous pouvez exécuter le site localement :

```bash
make container-serve
```

Ouvrez votre navigateur à l'adresse: http://localhost:1313 pour voir le site.
Lorsque vous apportez des modifications aux fichiers sources, Hugo met à jour le site et force le navigateur à rafraîchir la page.

## Exécuter le site localement en utilisant Hugo

Voir la [documentation officielle Hugo](https://gohugo.io/getting-started/installing/) pour les instructions d'installation Hugo.
Assurez-vous d'installer la version Hugo spécifiée par la variable d'environnement `HUGO_VERSION` dans le fichier [`netlify.toml`](netlify.toml#L9).

Pour exécuter le site localement lorsque vous avez Hugo installé :

```bash
make serve
```

Le serveur Hugo local démarrera sur le port 1313.
Ouvrez votre navigateur à l'adresse: http://localhost:1313 pour voir le site.
Lorsque vous apportez des modifications aux fichiers sources, Hugo met à jour le site et force le navigateur à rafraîchir la page.

## Communauté, discussion, contribution et assistance

Apprenez comment vous engager avec la communauté Kubernetes sur la [page communauté](http://kubernetes.io/community/).

Vous pouvez joindre les responsables de ce projet à l'adresse :

- [Slack](https://kubernetes.slack.com/messages/sig-docs)
- [Mailing List](https://groups.google.com/forum/#!forum/kubernetes-sig-docs)

### Code de conduite

La participation à la communauté Kubernetes est régie par le [Code de conduite de Kubernetes](code-of-conduct.md).

## Merci !

Kubernetes prospère grâce à la participation de la communauté, et nous apprécions vraiment vos contributions à notre site et à notre documentation !
