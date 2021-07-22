---
title: Kubernetes Komponenten
content_type: concept
weight: 20
card:
  name: concepts
  weight: 20
---

<!-- overview -->
In diesem Dokument werden die verschiedenen binären Komponenten beschrieben, die zur Bereitstellung eines funktionsfähigen Kubernetes-Clusters erforderlich sind.


<!-- body -->
## Master-Komponenten

Master-Komponenten stellen die Steuerungsebene des Clusters bereit. Master-Komponenten treffen globale Entscheidungen über den Cluster (z. B. Zeitplanung) und das Erkennen und Reagieren auf Clusterereignisse (Starten eines neuen Pods, wenn das `replicas`-Feld eines Replikationscontrollers nicht zufriedenstellend ist).

Master-Komponenten können auf jedem Computer im Cluster ausgeführt werden.
Der Einfachheit halber starten Setup-Skripts normalerweise alle Master-Komponenten auf demselben Computer, und es werden keine Benutzercontainer auf diesem Computer ausgeführt.
Lesen Sie [Cluster mit hoher Verfügbarkeit erstellen](/docs/admin/high-availability/) für ein Beispiel für ein Multi-Master-VM-Setup.

### kube-apiserver

{{< glossary_definition term_id="kube-apiserver" length="all" >}}

### etcd

{{< glossary_definition term_id="etcd" length="all" >}}

### kube-scheduler

{{< glossary_definition term_id="kube-scheduler" length="all" >}}

### kube-controller-manager

{{< glossary_definition term_id="kube-controller-manager" length="all" >}}

Diese Controller umfassen:

  * Node Controller: Verantwortlich für das Erkennen und Reagieren, wenn Nodes ausfallen.
  * Replication Controller: Verantwortlich für die Aufrechterhaltung der korrekten Anzahl von Pods für jedes Replikationscontrollerobjekt im System.
  * Endpoints Controller: Füllt das Endpoints-Objekt aus (d.h. verbindet Services & Pods).
  * Service Account & Token Controllers: Erstellt Standardkonten und API-Zugriffstoken für neue Namespaces.

### cloud-controller-manager

[cloud-controller-manager](/docs/tasks/administer-cluster/running-cloud-controller/) führt Controller aus, die mit den entsprechenden Cloud-Anbietern interagieren.
Der cloud-controller-manager ist eine Alpha-Funktion, die in Kubernetes Version 1.6 eingeführt wurde.

cloud-controller-manager führt nur Cloud-Provider-spezifische Controller-Schleifen aus. Sie müssen diese Controller-Schleifen im Cube-Controller-Manager deaktivieren. Sie können die Controller-Schleifen deaktivieren, indem Sie beim Starten des kube-controller-manager das Flag `--cloud-provider` auf `external` setzen.

cloud-controller-manager erlaubt es dem Cloud-Anbieter Code und dem Kubernetes-Code, sich unabhängig voneinander zu entwickeln.
In früheren Versionen war der Kerncode von Kubernetes für die Funktionalität von Cloud-Provider-spezifischem Code abhängig.
In zukünftigen Versionen sollte der für Cloud-Anbieter spezifische Code vom Cloud-Anbieter selbst verwaltet und mit dem Cloud-Controller-Manager verknüpft werden, während Kubernetes ausgeführt wird.

Die folgenden Controller haben Abhängigkeiten von Cloud-Anbietern:

  * Node Controller: Zum Überprüfen, ob ein Node in der Cloud beim Cloud-Anbieter gelöscht wurde, nachdem er nicht mehr reagiert
  * Route Controller: Zum Einrichten von Routen in der zugrunde liegenden Cloud-Infrastruktur
  * Service Controller: Zum Erstellen, Aktualisieren und Löschen von Lastverteilern von Cloud-Anbietern
  * Volume Controller: Zum Erstellen, Verbinden und Bereitstellen von Volumes und zur Interaktion mit dem Cloud-Provider zum Orchestrieren von Volumes

## Node-Komponenten

Node Komponenten werden auf jedem Knoten ausgeführt, halten laufende Pods aufrecht und stellen die Kubernetes-Laufzeitumgebung bereit.

### kubelet

{{< glossary_definition term_id="kubelet" length="all" >}}

### kube-proxy

[kube-proxy](/docs/admin/kube-proxy/) ermöglicht die Kubernetes Service-Abstraktion, indem die Netzwerkregeln auf dem Host beibehalten und die Verbindungsweiterleitung durchgeführt wird.

### Container Runtime

Die Containerlaufzeit ist die Software, die für das Ausführen von Containern verantwortlich ist.
Kubernetes unterstützt mehrere Laufzeiten: [Docker](http://www.docker.com), [containerd](https://containerd.io), [cri-o](https://cri-o.io/), [rktlet](https://github.com/kubernetes-incubator/rktlet) und jede Implementierung des [Kubernetes CRI (Container Runtime Interface)](https://github.com/kubernetes/community/blob/master/contributors/devel/sig-node/container-runtime-interface.md).

## Addons

Addons sind Pods und Dienste, die Clusterfunktionen implementieren. Die Pods können verwaltet werden
durch Deployments, ReplicationControllers, und so weiter.
Namespace-Addon-Objekte werden im Namespace `kube-system` erstellt.

Ausgewählte Addons werden unten beschrieben. Eine erweiterte Liste verfügbarer Addons finden Sie unter [Addons](/docs/concepts/cluster-administration/addons/).

### DNS

Während die anderen Addons nicht unbedingt erforderlich sind, sollte [cluster DNS](/docs/concepts/services-networking/dns-pod-service/) in allen Kubernetes-Cluster vorhanden sein, da viele Beispiele davon abhängen.

Cluster-DNS ist neben anderen DNS-Servern in Ihrer Umgebung ein DNS-Server, der DNS-Einträge für Kubernetes-Dienste bereitstellt.

Von Kubernetes gestartete Container schließen diesen DNS-Server automatisch in ihre DNS-Suchen ein.

### Web UI (Dashboard)

[Dashboard](/docs/tasks/access-application-cluster/web-ui-dashboard/) ist eine allgemeine, webbasierte Benutzeroberfläche für Kubernetes-Cluster. Benutzer können damit Anwendungen, die im Cluster ausgeführt werden, sowie den Cluster selbst verwalten und Fehler beheben.

### Container Resource Monitoring

[Container Resource Monitoring](/docs/tasks/debug-application-cluster/resource-usage-monitoring/) zeichnet generische Zeitreihenmessdaten zu Containern in einer zentralen Datenbank auf und stellt eine Benutzeroberfläche zum Durchsuchen dieser Daten bereit.


### Cluster-level Logging

Ein [Cluster-level logging](/docs/concepts/cluster-administration/logging/) Mechanismus ist für das Speichern von Containerprotokollen in einem zentralen Protokollspeicher mit Such- / Browsing-Schnittstelle verantwortlich.




