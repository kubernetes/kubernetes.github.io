---
title: Configurer un cluster etcd en haute disponibilité avec kubeadm
description: Configuration d'un cluster etcd en haute disponibilité avec kubeadm
content_type: task
weight: 70
---

<!-- overview -->

Par défaut, Kubeadm exécute un cluster etcd mono nœud dans un pod statique géré
par la kubelet sur le nœud du plan de contrôle (control plane). Ce n'est pas une configuration haute disponibilité puisque le cluster etcd ne contient qu'un seul membre et ne peut donc supporter
qu'aucun membre ne devienne indisponible. Cette page vous accompagne dans le processus de création
d'un cluster etcd à trois membres en haute disponibilité, pouvant être utilisé en tant que cluster externe lors de l’utilisation de kubeadm pour configurer un cluster kubernetes.



## {{% heading "prerequisites" %}}


* Trois machines pouvant communiquer entre elles via les ports 2379 et 2380. Cette 
methode utilise ces ports par défaut. Cependant, ils sont configurables via 
le fichier de configuration kubeadm.
* Chaque hôte doit avoir [docker, kubelet et kubeadm installés][toolbox].
* Certains paquets pour copier des fichiers entre les hôtes. Par exemple, `ssh` et` scp`.

[toolbox]: /fr/docs/setup/production-environment/tools/kubeadm/install-kubeadm/



<!-- steps -->

## Mise en place du cluster

L’approche générale consiste à générer tous les certificats sur un nœud et à ne distribuer que
les fichiers *nécessaires* aux autres nœuds.

{{< note >}}
kubeadm contient tout ce qui est nécessaire pour générer les certificats décrits ci-dessous;
 aucun autre outil de chiffrement n'est requis pour cet exemple.
{{< /note >}}


1. Configurez la kubelet pour qu'elle soit un gestionnaire de service pour etcd.

    Etant donné qu'etcd a été créé en premier, vous devez remplacer la priorité de service en
    créant un nouveau fichier unit qui a une priorité plus élevée que le fichier unit de la kubelet fourni
    par kubeadm.

    ```sh
    cat << EOF > /etc/systemd/system/kubelet.service.d/20-etcd-service-manager.conf
    [Service]
    ExecStart=
    ExecStart=/usr/bin/kubelet --address=127.0.0.1 --pod-manifest-path=/etc/kubernetes/manifests
    Restart=always
    EOF

    systemctl daemon-reload
    systemctl restart kubelet
    ```

1. Créez des fichiers de configuration pour kubeadm.

    Générez un fichier de configuration kubeadm pour chaque machine qui éxécutera un membre etcd
    en utilisant le script suivant.

    ```sh
    # Update HOST0, HOST1, and HOST2 with the IPs or resolvable names of your hosts
    export HOST0=10.0.0.6
    export HOST1=10.0.0.7
    export HOST2=10.0.0.8

    # Create temp directories to store files that will end up on other hosts.
    mkdir -p /tmp/${HOST0}/ /tmp/${HOST1}/ /tmp/${HOST2}/

    ETCDHOSTS=(${HOST0} ${HOST1} ${HOST2})
    NAMES=("infra0" "infra1" "infra2")

    for i in "${!ETCDHOSTS[@]}"; do
    HOST=${ETCDHOSTS[$i]}
    NAME=${NAMES[$i]}
    cat << EOF > /tmp/${HOST}/kubeadmcfg.yaml
    apiVersion: "kubeadm.k8s.io/v1beta1"
    kind: ClusterConfiguration
    etcd:
        local:
            serverCertSANs:
            - "${HOST}"
            peerCertSANs:
            - "${HOST}"
            extraArgs:
                initial-cluster: ${NAMES[0]}=https://${ETCDHOSTS[0]}:2380,${NAMES[1]}=https://${ETCDHOSTS[1]}:2380,${NAMES[2]}=https://${ETCDHOSTS[2]}:2380
                initial-cluster-state: new
                name: ${NAME}
                listen-peer-urls: https://${HOST}:2380
                listen-client-urls: https://${HOST}:2379
                advertise-client-urls: https://${HOST}:2379
                initial-advertise-peer-urls: https://${HOST}:2380
    EOF
    done
    ```

1. Générer l'autorité de certification

    Si vous avez déjà une autorité de certification, alors la seule action qui est faite copie
	 les fichiers `crt` et `key` de la CA dans `/etc/kubernetes/pki/etcd/ca.crt` et
	 `/etc/kubernetes/pki/etcd/ca.key`. Une fois ces fichiers copiés,
    passez à l'étape suivante, "Créer des certificats pour chaque membre".

    Si vous ne possédez pas déjà de CA, exécutez cette commande sur `$HOST0` (où vous
    avez généré les fichiers de configuration pour kubeadm).

    ```
    kubeadm init phase certs etcd-ca
    ```

    Cela crée deux fichiers

    - `/etc/kubernetes/pki/etcd/ca.crt`
    - `/etc/kubernetes/pki/etcd/ca.key`

1. Créer des certificats pour chaque membre

    ```sh
    kubeadm init phase certs etcd-server --config=/tmp/${HOST2}/kubeadmcfg.yaml
    kubeadm init phase certs etcd-peer --config=/tmp/${HOST2}/kubeadmcfg.yaml
    kubeadm init phase certs etcd-healthcheck-client --config=/tmp/${HOST2}/kubeadmcfg.yaml
    kubeadm init phase certs apiserver-etcd-client --config=/tmp/${HOST2}/kubeadmcfg.yaml
    cp -R /etc/kubernetes/pki /tmp/${HOST2}/
    # cleanup non-reusable certificates
    find /etc/kubernetes/pki -not -name ca.crt -not -name ca.key -type f -delete

    kubeadm init phase certs etcd-server --config=/tmp/${HOST1}/kubeadmcfg.yaml
    kubeadm init phase certs etcd-peer --config=/tmp/${HOST1}/kubeadmcfg.yaml
    kubeadm init phase certs etcd-healthcheck-client --config=/tmp/${HOST1}/kubeadmcfg.yaml
    kubeadm init phase certs apiserver-etcd-client --config=/tmp/${HOST1}/kubeadmcfg.yaml
    cp -R /etc/kubernetes/pki /tmp/${HOST1}/
    find /etc/kubernetes/pki -not -name ca.crt -not -name ca.key -type f -delete

    kubeadm init phase certs etcd-server --config=/tmp/${HOST0}/kubeadmcfg.yaml
    kubeadm init phase certs etcd-peer --config=/tmp/${HOST0}/kubeadmcfg.yaml
    kubeadm init phase certs etcd-healthcheck-client --config=/tmp/${HOST0}/kubeadmcfg.yaml
    kubeadm init phase certs apiserver-etcd-client --config=/tmp/${HOST0}/kubeadmcfg.yaml
    # No need to move the certs because they are for HOST0

    # clean up certs that should not be copied off this host
    find /tmp/${HOST2} -name ca.key -type f -delete
    find /tmp/${HOST1} -name ca.key -type f -delete
    ```

1. Copier les certificats et les configurations kubeadm

    Les certificats ont été générés et doivent maintenant être déplacés vers leur
    hôtes respectifs.

     ```sh
     USER=ubuntu
     HOST=${HOST1}
     scp -r /tmp/${HOST}/* ${USER}@${HOST}:
     ssh ${USER}@${HOST}
     USER@HOST $ sudo -Es
     root@HOST $ chown -R root:root pki
     root@HOST $ mv pki /etc/kubernetes/
     ```

1. S'assurer que tous les fichiers attendus existent

    La liste complète des fichiers requis sur `$HOST0` est la suivante:

    ```
    /tmp/${HOST0}
    └── kubeadmcfg.yaml
    ---
    /etc/kubernetes/pki
    ├── apiserver-etcd-client.crt
    ├── apiserver-etcd-client.key
    └── etcd
        ├── ca.crt
        ├── ca.key
        ├── healthcheck-client.crt
        ├── healthcheck-client.key
        ├── peer.crt
        ├── peer.key
        ├── server.crt
        └── server.key
    ```

    Sur `$HOST1`:

    ```
    $HOME
    └── kubeadmcfg.yaml
    ---
    /etc/kubernetes/pki
    ├── apiserver-etcd-client.crt
    ├── apiserver-etcd-client.key
    └── etcd
        ├── ca.crt
        ├── healthcheck-client.crt
        ├── healthcheck-client.key
        ├── peer.crt
        ├── peer.key
        ├── server.crt
        └── server.key
    ```

    Sur `$HOST2`:

    ```
    $HOME
    └── kubeadmcfg.yaml
    ---
    /etc/kubernetes/pki
    ├── apiserver-etcd-client.crt
    ├── apiserver-etcd-client.key
    └── etcd
        ├── ca.crt
        ├── healthcheck-client.crt
        ├── healthcheck-client.key
        ├── peer.crt
        ├── peer.key
        ├── server.crt
        └── server.key
    ```

1. Créer les manifestes de pod statiques

    Maintenant que les certificats et les configurations sont en place, il est temps de créer les
    manifestes. Sur chaque hôte, exécutez la commande `kubeadm` pour générer un manifeste statique
    pour etcd.

    ```sh
    root@HOST0 $ kubeadm init phase etcd local --config=/tmp/${HOST0}/kubeadmcfg.yaml
    root@HOST1 $ kubeadm init phase etcd local --config=/tmp/${HOST1}/kubeadmcfg.yaml
    root@HOST2 $ kubeadm init phase etcd local --config=/tmp/${HOST2}/kubeadmcfg.yaml
    ```

1. Facultatif: Vérifiez la santé du cluster

    ```sh
    docker run --rm -it \
    --net host \
    -v /etc/kubernetes:/etc/kubernetes quay.io/coreos/etcd:${ETCD_TAG} etcdctl \
    --cert-file /etc/kubernetes/pki/etcd/peer.crt \
    --key-file /etc/kubernetes/pki/etcd/peer.key \
    --ca-file /etc/kubernetes/pki/etcd/ca.crt \
    --endpoints https://${HOST0}:2379 cluster-health
    ...
    cluster is healthy
    ```
    - Configurez `${ETCD_TAG}` avec la version de votre image etcd. Par exemple `v3.2.24`.
    - Configurez `${HOST0}` avec l'adresse IP de l'hôte que vous testez.



## {{% heading "whatsnext" %}}


Une fois que vous avez un cluster de 3 membres etcd qui fonctionne, vous pouvez continuer à
 configurer un control plane hautement disponible utilisant la
[méthode etcd externe avec kubeadm](/fr/docs/setup/production-environment/tools/kubeadm/high-availability/).




