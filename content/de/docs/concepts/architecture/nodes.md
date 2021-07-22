---
title: Nodes
content_type: concept
weight: 10
---

<!-- overview -->

Ein Knoten (Node in Englisch) ist eine Arbeitsmaschine in Kubernetes. Ein Node
kann je nach Cluster eine VM oder eine physische Maschine sein. Jeder Node enthält
die für den Betrieb von [Pods](/docs/concepts/workloads/pods/pod/) notwendigen Dienste
und wird von den Master-Komponenten verwaltet.
Die Dienste auf einem Node umfassen die [Container Runtime](/docs/concepts/overview/components/#node-components), das Kubelet und den Kube-Proxy.
Weitere Informationen finden Sie im Abschnitt Kubernetes Node in der Architekturdesign-Dokumentation.




<!-- body -->

## Node Status

Der Status eines Nodes enthält folgende Informationen:

* [Adressen](#adressen)
* [Zustand](#zustand)
* [Kapazität](#kapazität)
* [Info](#info)

Jeder Abschnitt wird folgend detailliert beschrieben.

### Adressen

Die Verwendung dieser Felder hängt von Ihrem Cloud-Anbieter oder der Bare-Metal-Konfiguration ab.

* HostName: Der vom Kernel des Nodes gemeldete Hostname. Kann mit dem kubelet-Parameter `--hostname-override` überschrieben werden.
* ExternalIP: In der Regel die IP-Adresse des Nodes, die extern geroutet werden kann (von außerhalb des Clusters verfügbar).
* InternalIP: In der Regel die IP-Adresse des Nodes, die nur innerhalb des Clusters routbar ist.


### Zustand

Das `conditions` Feld beschreibt den Zustand, aller `Running` Nodes.

| Node Condition | Beschreibung |
|----------------|-------------|
| `OutOfDisk`    | `True` wenn auf dem Node nicht genügend freier Speicherplatz zum Hinzufügen neuer Pods vorhanden ist, andernfalls `False` |
| `Ready`        | `True` wenn der Node in einem guten Zustand und bereit ist Pods aufzunehmen, `False` wenn der Node nicht in einem guten Zustand ist und nicht bereit ist Pods aufzunehmeb, und `Unknown` wenn der Node-Controller seit der letzten `node-monitor-grace-period` nichts von dem Node gehört hat (Die Standardeinstellung beträgt 40 Sekunden) |
| `MemoryPressure`    | `True` wenn der verfügbare Speicher des Nodes niedrig ist; Andernfalls`False` |
| `PIDPressure`    | `True` wenn zu viele Prozesse auf dem Node vorhanden sind; Andernfalls`False` |
| `DiskPressure`    | `True` wenn die Festplattenkapazität niedrig ist. Andernfalls `False` |
| `NetworkUnavailable`    | `True` wenn das Netzwerk für den Node nicht korrekt konfiguriert ist, andernfalls `False` |

Der Zustand eines Nodes wird als JSON-Objekt dargestellt. Die folgende Antwort beschreibt beispielsweise einen fehlerfreien Node.

```json
"conditions": [
  {
    "type": "Ready",
    "status": "True"
  }
]
```

Wenn der Status der `Ready`-Bedingung `Unknown` oder `False` länger als der `pod-eviction-timeout` bleibt, wird ein Parameter an den [kube-controller-manager](/docs/admin/kube-controller-manager/) übergeben und alle Pods auf dem Node werden vom Node Controller gelöscht.

Die voreingestellte Zeit vor der Entfernung beträgt **fünf Minuten**.
In einigen Fällen, in denen der Node nicht erreichbar ist, kann der Apiserver nicht mit dem Kubelet auf dem Node kommunizieren.
Die Entscheidung, die Pods zu löschen, kann dem Kublet erst mitgeteilt werden, wenn die Kommunikation mit dem Apiserver wiederhergestellt ist.
In der Zwischenzeit können Pods, deren Löschen geplant ist, weiterhin auf dem unzugänglichen Node laufen.


In Versionen von Kubernetes vor 1.5 würde der Node Controller das Löschen dieser unerreichbaren Pods vom Apiserver [erzwingen](/docs/concepts/workloads/pods/pod/#force-deletion-of-pods). In Version 1.5 und höher erzwingt der Node Controller jedoch keine Pod Löschung, bis bestätigt wird, dass sie nicht mehr im Cluster ausgeführt werden. Pods die auf einem unzugänglichen Node laufen sind eventuell in einem einem `Terminating` oder `Unkown` Status. In Fällen, in denen Kubernetes nicht aus der zugrunde liegenden Infrastruktur schließen kann, ob ein Node einen Cluster dauerhaft verlassen hat, muss der Clusteradministrator den Node möglicherweise manuell löschen.
Das Löschen des Kubernetes-Nodeobjekts bewirkt, dass alle auf dem Node ausgeführten Pod-Objekte gelöscht und deren Namen freigegeben werden.

In Version 1.12 wurde die Funktion `TaintNodesByCondition` als Beta-Version eingeführt, die es dem Node-Lebenszyklus-Controller ermöglicht, automatisch [Markierungen](/docs/concepts/configuration/taint-and-toleration/) (*taints* in Englisch) zu erstellen, die Bedingungen darstellen.

Ebenso ignoriert der Scheduler die Bedingungen, wenn er einen Node berücksichtigt; stattdessen betrachtet er die Markierungen (taints) des Nodes und die Toleranzen eines Pod.

Anwender können jetzt zwischen dem alten Scheduling-Modell und einem neuen, flexibleren Scheduling-Modell wählen.

Ein Pod, der keine Toleranzen aufweist, wird gemäß dem alten Modell geplant.
Aber ein Pod, die die Taints eines bestimmten Node toleriert, kann auf diesem Node geplant werden.

{{< caution >}}
Wenn Sie diese Funktion aktivieren, entsteht eine kleine Verzögerung zwischen der Zeit,
in der eine Bedingung beobachtet wird, und der Zeit, in der ein Taint entsteht.
Diese Verzögerung ist in der Regel kürzer als eine Sekunde, aber sie kann die Anzahl
der Pods erhöhen, die erfolgreich geplant, aber vom Kubelet abgelehnt werden.
{{< /caution >}}

### Kapazität

Beschreibt die auf dem Node verfügbaren Ressourcen: CPU, Speicher und die maximale
Anzahl der Pods, die auf dem Node ausgeführt werden können.

### Info

Allgemeine Informationen zum Node, z. B. Kernelversion, Kubernetes-Version
(kubelet- und kube-Proxy-Version), Docker-Version (falls verwendet), Betriebssystemname.
Die Informationen werden von Kubelet vom Node gesammelt.

## Management

Im Gegensatz zu [Pods](/docs/concepts/workloads/pods/pod/) und [Services](/docs/concepts/services-networking/service/),
wird ein Node nicht von Kubernetes erstellt: Er wird extern von Cloud-Anbietern wie Google Compute Engine erstellt oder ist in Ihrem Pool physischer oder virtueller Maschinen vorhanden.
Wenn Kubernetes also einen Node erstellt, wird ein Objekt erstellt, das den Node darstellt.
Nach der Erstellung überprüft Kubernetes, ob der Node gültig ist oder nicht.

Wenn Sie beispielsweise versuchen, einen Node aus folgendem Inhalt zu erstellen:

```json
{
  "kind": "Node",
  "apiVersion": "v1",
  "metadata": {
    "name": "10.240.79.157",
    "labels": {
      "name": "my-first-k8s-node"
    }
  }
}
```


Kubernetes erstellt intern ein Node-Objekt (die Darstellung) und validiert den Node durch Zustandsprüfung basierend auf dem Feld `metadata.name`.
Wenn der Node gültig ist, d.h. wenn alle notwendigen Dienste ausgeführt werden, ist er berechtigt, einen Pod auszuführen.
Andernfalls wird er für alle Clusteraktivitäten ignoriert, bis er gültig wird.


{{< note >}}
Kubernetes behält das Objekt für den ungültigen Node und prüft ständig seine Gültigkeit.
Sie müssen das Node-Objekt explizit löschen, um diesen Prozess zu stoppen.
{{< /note >}}

Aktuell gibt es drei Komponenten, die mit dem Kubernetes Node-Interface interagieren: Node Controller, Kubelet und Kubectl.


### Node Controller

Der Node Controller ist eine Kubernetes-Master-Komponente, die verschiedene Aspekte von Nodes verwaltet.

Der Node Controller hat mehrere Rollen im Leben eines Nodes.
Der erste ist die Zuordnung eines CIDR-Blocks zu dem Node, wenn er registriert ist (sofern die CIDR-Zuweisung aktiviert ist).

Die zweite ist, die interne Node-Liste des Node Controllers mit der Liste der verfügbaren Computer des Cloud-Anbieters auf dem neuesten Stand zu halten.
Wenn ein Node in einer Cloud-Umgebung ausgeführt wird und sich in einem schlechten Zustand befindet, fragt der Node Controller den Cloud-Anbieter, ob die virtuelle Maschine für diesen Node noch verfügbar ist. Wenn nicht, löscht der Node Controller den Node aus seiner Node-Liste.

Der dritte ist die Überwachung des Zustands der Nodes. Der Node Controller ist dafür verantwortlich,
die NodeReady-Bedingung von NodeStatus auf ConditionUnknown zu aktualisieren, wenn ein Node unerreichbar wird (der Node Controller empfängt aus irgendeinem Grund keine Herzschläge mehr, z.B. weil der Node heruntergefahren ist) und später alle Pods aus dem Node zu entfernen (und diese ordnungsgemäss zu beenden), wenn der Node weiterhin unzugänglich ist. (Die Standard-Timeouts sind 40s, um ConditionUnknown zu melden und 5 Minuten, um mit der Evakuierung der Pods zu beginnen).

Der Node Controller überprüft den Zustand jedes Nodes alle `--node-monitor-period` Sekunden.


In Versionen von Kubernetes vor 1.13 ist NodeStatus der Herzschlag des Nodes.
Ab Kubernetes 1.13 wird das Node-Lease-Feature als Alpha-Feature eingeführt (Feature-Gate `NodeLease`, [KEP-0009](https://github.com/kubernetes/enhancements/blob/master/keps/sig-node/0009-node-heartbeat.md)).

Wenn die Node Lease Funktion aktiviert ist, hat jeder Node ein zugeordnetes `Lease`-Objekt im `kube-node-lease`-Namespace, das vom Node regelmäßig erneuert wird.
Sowohl NodeStatus als auch Node Lease werden als Herzschläge vom Node aus behandelt.
Node Leases werden häufig erneuert, während NodeStatus nur dann vom Node zu Master gemeldet wird, wenn sich etwas ändert oder genügend Zeit vergangen ist (Standard ist 1 Minute, was länger ist als der Standard-Timeout von 40 Sekunden für unerreichbare Nodes).
Da Node Leases viel lastärmer sind als NodeStatus, macht diese Funktion den Node Herzschlag sowohl in Bezug auf Skalierbarkeit als auch auf die Leistung deutlich effizienter.

In Kubernetes 1.4 haben wir die Logik der Node-Steuerung aktualisiert, um Fälle besser zu handhaben, in denen eine große Anzahl von Nodes Probleme hat, den Master zu erreichen (z.B. weil der Master Netzwerkprobleme hat).
Ab 1.4 betrachtet der Node-Controller den Zustand aller Nodes im Cluster, wenn er eine Entscheidung über die Enterfung eines Pods trifft.

In den meisten Fällen begrenzt der Node-Controller die Entfernungsrate auf `--node-eviction-rate` (Standard 0,1) pro Sekunde, was bedeutet, dass er die Pods nicht von mehr als einem Node pro 10 Sekunden entfernt.

Das Entfernungsverhalten von Nodes ändert sich, wenn ein Node in einer bestimmten Verfügbarkeitszone ungesund wird.
Der Node-Controller überprüft gleichzeitig, wie viel Prozent der Nodes in der Zone ungesund sind (NodeReady-Bedingung ist ConditionUnknown oder ConditionFalse).
Wenn der Anteil der ungesunden Nodes mindestens `--unhealthy-zone-threshold` (Standard 0,55) beträgt, wird die Entfernungsrate reduziert:

Wenn der Cluster klein ist (d.h. weniger als oder gleich `--large-cluster-size-threshold` Node - Standard 50), werden die Entfernungen gestoppt. Andernfalls wird die Entfernungsrate auf `--secondary-node-eviction-rate` (Standard 0,01) pro Sekunde reduziert.

Der Grund, warum diese Richtlinien pro Verfügbarkeitszone implementiert werden, liegt darin, dass eine Verfügbarkeitszone vom Master unerreichbar werden könnte, während die anderen verbunden bleiben. Wenn Ihr Cluster nicht mehrere Verfügbarkeitszonen von Cloud-Anbietern umfasst, gibt es nur eine Verfügbarkeitszone (den gesamten Cluster).

Ein wichtiger Grund für die Verteilung Ihrer Nodes auf Verfügbarkeitszonen ist, dass die Arbeitsbelastung auf gesunde Zonen verlagert werden kann, wenn eine ganze Zone ausfällt.
Wenn also alle Nodes in einer Zone ungesund sind, entfernt Node Controller mit der normalen `--node-eviction-rate` Geschwindigkeit.
Der Ausnahmefall ist, wenn alle Zonen völlig ungesund sind (d.h. es gibt keine gesunden Node im Cluster).
In diesem Fall geht der Node-Controller davon aus, dass es ein Problem mit der Master-Konnektivität gibt und stoppt alle Entfernungen, bis die Verbindung wiederhergestellt ist.

Ab Kubernetes 1.6 ist der Node-Controller auch für die Entfernung von Pods zuständig, die auf Nodes mit `NoExecute`-Taints laufen, wenn die Pods die Markierungen nicht tolerieren.
Zusätzlich ist der NodeController als Alpha-Funktion, die standardmäßig deaktiviert ist, dafür verantwortlich, Taints hinzuzufügen, die Node Probleme, wie `Node unreachable` oder `not ready` entsprechen.
Siehe [diese Dokumentation](/docs/concepts/configuration/taint-and-toleration/) für Details über `NoExecute` Taints und die Alpha-Funktion.


Ab Version 1.8 kann der Node-Controller für die Erzeugung von Taints, die Node Bedingungen darstellen, verantwortlich gemacht werden. Dies ist eine Alpha-Funktion der Version 1.8.

### Selbstregistrierung von Nodes

Wenn das Kubelet-Flag `--register-node` aktiv ist (Standard), versucht das Kubelet, sich beim API-Server zu registrieren.  Dies ist das bevorzugte Muster, das von den meisten Distributionen verwendet wird.

Zur Selbstregistrierung wird das kubelet mit den folgenden Optionen gestartet:

  - `--kubeconfig` - Pfad zu Anmeldeinformationen, um sich beim Apiserver zu authentifizieren.
  - `--cloud-provider` - Wie man sich mit einem Cloud-Anbieter unterhält, um Metadaten über sich selbst zu lesen.
  - `--register-node` - Automatisch beim API-Server registrieren.
  - `--register-with-taints` - Registrieren Sie den Node mit der angegebenen Taints-Liste (Kommagetrennt `<key>=<value>:<effect>`). No-op wenn `register-node` false ist.
  - `--node-ip` - IP-Adresse des Nodes.
  - `--node-labels` - Labels, die bei der Registrierung des Nodes im Cluster hinzugefügt werden sollen (Beachten Sie die Richlinien des [NodeRestriction admission plugin](/docs/reference/access-authn-authz/admission-controllers/#noderestriction) in 1.13+).
  - `--node-status-update-frequency` - Gibt an, wie oft kubelet den Nodestatus an den Master übermittelt.

Wenn der [Node authorization mode](/docs/reference/access-authn-authz/node/) und
[NodeRestriction admission plugin](/docs/reference/access-authn-authz/admission-controllers/#noderestriction) aktiviert sind,
dürfen kubelets nur ihre eigene Node-Ressource erstellen / ändern.

#### Manuelle Nodeverwaltung

Ein Cluster-Administrator kann Nodeobjekte erstellen und ändern.

Wenn der Administrator Nodeobjekte manuell erstellen möchte, setzen Sie das kubelet Flag `--register-node=false`.

Der Administrator kann Node-Ressourcen ändern (unabhängig von der Einstellung von `--register-node`).
Zu den Änderungen gehören das Setzen von Labels und das Markieren des Nodes.

Labels auf Nodes können in Verbindung mit node selectors auf Pods verwendet werden, um die Planung zu steuern, z.B. um einen Pod so zu beschränken, dass er nur auf einer Teilmenge der Nodes ausgeführt werden darf.

Das Markieren eines Nodes als nicht geplant, verhindert, dass neue Pods für diesen Node geplant werden. Dies hat jedoch keine Auswirkungen auf vorhandene Pods auf dem Node.
Dies ist nützlich als vorbereitender Schritt vor einem Neustart eines Nodes usw.
Um beispielsweise einen Node als nicht geplant zu markieren, führen Sie den folgenden Befehl aus:

```shell
kubectl cordon $NODENAME
```

{{< note >}}
Pods, die von einem DaemonSet-Controller erstellt wurden, umgehen den Kubernetes-Scheduler und respektieren nicht das _unschedulable_ Attribut auf einem Node.
Dies setzt voraus, dass Daemons auf dem Computer verbleiben, auch wenn während der Vorbereitung eines Neustarts keine Anwendungen mehr vorhanden sind.
{{< /note >}}

### Node Kapazität

Die Kapazität des Nodes (Anzahl der CPU und Speichermenge) ist Teil des Nodeobjekts.
Normalerweise registrieren sich Nodes selbst und melden ihre Kapazität beim Erstellen des Nodeobjekts.
Sofern Sie [Manuelle Nodeverwaltung](#Manuelle-Nodeverwaltung) betreiben, müssen Sie die Node Kapazität setzen, wenn Sie einen Node hinzufügen.

Der Kubernetes-Scheduler stellt sicher, dass für alle Pods auf einem Nodes genügend Ressourcen vorhanden sind.
Er prüft, dass die Summe der Requests von Containern auf dem Node nicht größer ist als die Kapazität des Nodes.
Er beinhaltet alle Container die vom kubelet gestarted worden, aber keine Container die direkt von der [container runtime](/docs/concepts/overview/components/#node-components) gestartet wurden, noch jegleiche Prozesse die ausserhalb von Containern laufen.

Wenn Sie Ressourcen explizit für Nicht-Pod-Prozesse reservieren möchten, folgen Sie diesem Lernprogramm um [Ressourcen für Systemdaemons zu reservieren](/docs/tasks/administer-cluster/reserve-compute-resources/#system-reserved).


## API-Objekt

Node ist eine Top-Level-Ressource in der Kubernetes-REST-API. Weitere Details zum API-Objekt finden Sie unter:
[Node API object](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#node-v1-core).


