---
title: Hallo Minikube
content_type: tutorial
weight: 5
menu:
  main:
    title: "Loslegen"
    weight: 10
    post: >
      <p>Sind Sie bereit, Ihre Hände schmutzig zu machen? Erstellen Sie einen einfachen Kubernetes-Cluster, auf dem "Hallo Welt" für Node.js ausgeführt wird.</p>
card:
  name: tutorials
  weight: 10
---

<!-- overview -->

Dieses Tutorial zeigt Ihnen, wie Sie eine einfache "Hallo Welt" Node.js-Anwendung auf Kubernetes mit [Minikube](https://minikube.sigs.k8s.io/docs/start/) und Katacoda ausführen.
Katacoda bietet eine kostenlose Kubernetes-Umgebung im Browser.

## {{% heading "objectives" %}}


* Stellen Sie eine Hallo-Welt-Anwendung für Minikube bereit.
* Führen Sie die App aus.
* Betrachten Sie die Log Dateien.



## {{% heading "prerequisites" %}}


Dieses Lernprogramm enthält ein aus den folgenden Dateien erstelltes Container-Image:

{{< codenew language="js" file="minikube/server.js" >}}

{{< codenew language="conf" file="minikube/Dockerfile" >}}

Weitere Informationen zum `docker build` Befehl, lesen Sie die [Docker Dokumentation](https://docs.docker.com/engine/reference/commandline/build/).



<!-- lessoncontent -->

## Erstellen Sie einen Minikube-Cluster

1. Klicken Sie auf **Launch Terminal**.

    {{< kat-button >}}

    {{< note >}}Wenn Sie Minikube lokal installiert haben, führen Sie `minikube start` aus.{{< /note >}}

2. Öffnen Sie das Kubernetes-Dashboard in einem Browser:

    ```shell
    minikube dashboard
    ```

3. In einer Katacoda-Umgebung: Klicken Sie oben im Terminalbereich auf das Pluszeichen und anschließend auf **Select port to view on Host 1**.

4. In einer Katacoda-Umgebung: Geben Sie `30000` ein und klicken Sie dann auf **Display Port**.

## Erstellen eines Deployments

Ein Kubernetes [*Pod*](/docs/concepts/workloads/pods/pod/) ist eine Gruppe von einem oder mehreren Containern, die zu Verwaltungs- und Netzwerkzwecken miteinander verbunden sind.
Der Pod in diesem Tutorial hat nur einen Container.
Ein Kubernetes [*Deployment*](/docs/concepts/workloads/controllers/deployment/) überprüft den Zustand Ihres Pods und startet den Container des Pods erneut, wenn er beendet wird.
Deployments sind die empfohlene Methode zum Verwalten der Erstellung und Skalierung von Pods.

1. Verwenden Sie den Befehl `kubectl create`, um ein Deployment zu erstellen, die einen Pod verwaltet.
Der Pod führt einen Container basierend auf dem bereitgestellten Docker-Image aus.

    ```shell
    kubectl create deployment hello-node --image=k8s.gcr.io/echoserver:1.4
    ```

2. Anzeigen des Deployments:

    ```shell
    kubectl get deployments
    ```

    Ausgabe:

    ```shell
    NAME         DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
    hello-node   1         1         1            1           1m
    ```

3. Den Pod anzeigen:

    ```shell
    kubectl get pods
    ```
    Ausgabe:

    ```shell
    NAME                          READY     STATUS    RESTARTS   AGE
    hello-node-5f76cf6ccf-br9b5   1/1       Running   0          1m
    ```

4. Cluster Events anzigen:

    ```shell
    kubectl get events
    ```

5. Die Konfiguration von `kubectl` anzeigen:

    ```shell
    kubectl config view
    ```

    {{< note >}}Weitere Informationen zu `kubectl`-Befehlen finden Sie im [kubectl Überblick](/docs/user-guide/kubectl-overview/).{{< /note >}}

## Erstellen Sie einen Service

Standardmäßig ist der Pod nur über seine interne IP-Adresse im Kubernetes-Cluster erreichbar.
Um den "Hallo-Welt"-Container außerhalb des virtuellen Netzwerks von Kubernetes zugänglich zu machen, müssen Sie den Pod als Kubernetes [*Service*](/docs/concepts/services-networking/service/) verfügbar machen.

1. Stellen Sie den Pod mit dem Befehl `kubectl expose` im öffentlichen Internet bereit:

    ```shell
    kubectl expose deployment hello-node --type=LoadBalancer --port=8080
    ```

    Das Flag `--type = LoadBalancer` zeigt an, dass Sie Ihren Service außerhalb des Clusters verfügbar machen möchten.

2. Zeigen Sie den gerade erstellten Service an:

    ```shell
    kubectl get services
    ```

    Ausgabe:

    ```shell
    NAME         TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
    hello-node   LoadBalancer   10.108.144.78   <pending>     8080:30369/TCP   21s
    kubernetes   ClusterIP      10.96.0.1       <none>        443/TCP          23m
    ```

    Bei Cloud-Anbietern, die Load-Balancer unterstützen, wird eine externe IP-Adresse für den Zugriff auf den Dienst bereitgestellt.
    Bei Minikube ermöglicht der Typ `LoadBalancer` den Dienst über den Befehl `minikube service` verfügbar zu machen.


3. Führen Sie den folgenden Befehl aus:

    ```shell
    minikube service hello-node
    ```

4. In einer Katacoda-Umgebung: Klicken Sie auf das Pluszeichen und dann auf **Select port to view on Host 1**.

5. In einer Katacoda-Umgebung: Geben Sie "30369" ein (siehe Port gegenüber "8080" in der service ausgabe), und klicken Sie dann auf

    Daraufhin wird ein Browserfenster geöffnet, in dem Ihre App ausgeführt wird und die Meldung "Hello World" (Hallo Welt) angezeigt wird.

## Addons aktivieren

Minikube verfügt über eine Reihe von integrierten Add-Ons, die in der lokalen Kubernetes-Umgebung aktiviert, deaktiviert und geöffnet werden können.

1. Listen Sie die aktuell unterstützten Addons auf:

    ```shell
    minikube addons list
    ```

    Ausgabe:

    ```shell
    addon-manager: enabled
    coredns: disabled
    dashboard: enabled
    default-storageclass: enabled
    efk: disabled
    freshpod: disabled
    heapster: disabled
    ingress: disabled
    kube-dns: enabled
    metrics-server: disabled
    nvidia-driver-installer: disabled
    nvidia-gpu-device-plugin: disabled
    registry: disabled
    registry-creds: disabled
    storage-provisioner: enabled
    ```

2. Aktivieren Sie ein Addon, zum Beispiel `heapster`:

    ```shell
    minikube addons enable heapster
    ```

    Ausgabe:

    ```shell
    heapster was successfully enabled
    ```

3. Sehen Sie sich den Pod und den Service an, den Sie gerade erstellt haben:

    ```shell
    kubectl get pod,svc -n kube-system
    ```

    Ausgabe:

    ```shell
    NAME                                        READY     STATUS    RESTARTS   AGE
    pod/heapster-9jttx                          1/1       Running   0          26s
    pod/influxdb-grafana-b29w8                  2/2       Running   0          26s
    pod/kube-addon-manager-minikube             1/1       Running   0          34m
    pod/kube-dns-6dcb57bcc8-gv7mw               3/3       Running   0          34m
    pod/kubernetes-dashboard-5498ccf677-cgspw   1/1       Running   0          34m
    pod/storage-provisioner                     1/1       Running   0          34m

    NAME                           TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)             AGE
    service/heapster               ClusterIP   10.96.241.45    <none>        80/TCP              26s
    service/kube-dns               ClusterIP   10.96.0.10      <none>        53/UDP,53/TCP       34m
    service/kubernetes-dashboard   NodePort    10.109.29.1     <none>        80:30000/TCP        34m
    service/monitoring-grafana     NodePort    10.99.24.54     <none>        80:30002/TCP        26s
    service/monitoring-influxdb    ClusterIP   10.111.169.94   <none>        8083/TCP,8086/TCP   26s
    ```

4. Deaktivieren Sie `heapster`:

    ```shell
    minikube addons disable heapster
    ```

    Ausgabe:

    ```shell
    heapster was successfully disabled
    ```

## Aufräumen

Jetzt können Sie die in Ihrem Cluster erstellten Ressourcen bereinigen:

```shell
kubectl delete service hello-node
kubectl delete deployment hello-node
```

Stoppen Sie optional die virtuelle Minikube-Maschine (VM):

```shell
minikube stop
```

Löschen Sie optional die Minikube-VM:

```shell
minikube delete
```



## {{% heading "whatsnext" %}}


* Lernen Sie mehr über [Bereitstellungsobjekte](/docs/concepts/workloads/controllers/deployment/).
* Lernen Sie mehr über [Anwendungen bereitstellen](/docs/user-guide/deploying-applications/).
* Lernen Sie mehr über [Serviceobjekte](/docs/concepts/services-networking/service/).


