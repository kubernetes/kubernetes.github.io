---
title: Was ist Kubernetes?
content_type: concept
weight: 10
card:
  name: concepts
  weight: 10
---

<!-- overview -->
Diese Seite ist eine Übersicht über Kubernetes.


<!-- body -->

Kubernetes ist eine portable, erweiterbare Open-Source-Plattform zur Verwaltung von
containerisierten Arbeitslasten und Services, die sowohl die deklarative Konfiguration als auch die Automatisierung erleichtert.
Es hat einen großes, schnell wachsendes Ökosystem. Kubernetes Dienstleistungen, Support und Tools sind weit verbreitet.

Google hat das Kubernetes-Projekt 2014 als Open-Source-Projekt zur Verfügung gestellt. Kubernetes baut auf anderthalb Jahrzehnten
Erfahrung auf, die Google mit der Ausführung von Produktions-Workloads in großem Maßstab hat, kombiniert mit den besten Ideen und Praktiken der Community.

## Warum brauche ich Kubernetes und was kann ich damit tun?

Kubernetes hat eine Reihe von Funktionen. Es kann gesehen werden als:

- eine Containerplattform
- eine Microservices-Plattform
- eine portable Cloud-Plattform
und vieles mehr.

Kubernetes bietet eine **containerzentrierte** Managementumgebung. Es koordiniert die Computer-, Netzwerk- und Speicherinfrastruktur
im Namen der Benutzer-Workloads. Dies bietet einen Großteil der Einfachheit von Platform as a Service (PaaS) mit der Flexibilität
von Infrastructure as a Service (IaaS) und ermöglicht die Portabilität zwischen Infrastrukturanbietern.

## Wie ist Kubernetes eine Plattform?

Auch wenn Kubernetes eine Menge Funktionalität bietet, gibt es immer wieder neue Szenarien,
die von neuen Funktionen profitieren würden. Anwendungsspezifische Workflows können optimiert werden,
um die Entwicklungsgeschwindigkeit zu beschleunigen.
Eine zunächst akzeptable Ad-hoc-Orchestrierung erfordert oft eine robuste Automatisierung in großem Maßstab.
Aus diesem Grund wurde Kubernetes auch als Plattform für den Aufbau eines Ökosystems von Komponenten und Tools
konzipiert, um die Bereitstellung, Skalierung und Verwaltung von Anwendungen zu erleichtern.

[Labels](/docs/concepts/overview/working-with-objects/labels/) ermöglichen es den Benutzern, ihre Ressourcen
nach Belieben zu organisieren. [Anmerkungen](/docs/concepts/overview/working-with-objects/annotations/) ermöglichen es Benutzern,
Ressourcen mit benutzerdefinierten Informationen zu versehen, um ihre Arbeitsabläufe zu vereinfachen und eine einfache Möglichkeit
für Managementtools zu bieten, den Status von Kontrollpunkten zu ermitteln.


Darüber hinaus basiert die [Kubernetes-Steuerungsebene](/docs/concepts/overview/components/) auf den gleichen APIs,
die Entwicklern und Anwendern zur Verfügung stehen. Benutzer können ihre eigenen Controller, wie z.B.
[Scheduler](https://github.com/kubernetes/community/blob/{{< param "githubbranch" >}}/contributors/devel/scheduler.md), mit
ihren [eigenen APIs](/docs/concepts/api-extension/custom-resources/) schreiben, die von einem
universellen [Kommandozeilen-Tool](/docs/user-guide/kubectl-overview/) angesprochen werden können.

Dieses [Design](https://git.k8s.io/community/contributors/design-proposals/architecture/architecture.md) hat es einer Reihe anderer Systeme ermöglicht, auf Kubernetes aufzubauen.

## Was Kubernetes nicht ist

Kubernetes ist kein traditionelles, allumfassendes PaaS (Plattform als ein Service) System. Da Kubernetes nicht auf Hardware-,
sondern auf Containerebene arbeitet, bietet es einige allgemein anwendbare Funktionen, die PaaS-Angeboten gemeinsam sind,
wie Bereitstellung, Skalierung, Lastausgleich, Protokollierung und Überwachung.
Kubernetes ist jedoch nicht monolithisch, und diese Standardlösungen sind optional und modular etweiterbar.
Kubernetes liefert die Bausteine für den Aufbau von Entwicklerplattformen, bewahrt aber die
Wahlmöglichkeiten und Flexibilität der Benutzer, wo es wichtig ist.

Kubernetes:

* Schränkt nicht die Art der unterstützten Anwendungen ein. Kubernetes zielt darauf ab,
  eine extrem große Vielfalt von Workloads zu unterstützen, einschließlich stateless,
  stateful und datenverarbeitender Workloads. Wenn eine Anwendung in einem Container ausgeführt
  werden kann, sollte sie auf Kubernetes hervorragend laufen.
* Verteilt keinen Quellcode und entwickelt Ihre Anwendung nicht.
  Kontinuierliche Integrations-, Liefer- und Bereitstellungs-Workflows (CI/CD) werden durch
  Unternehmenskulturen und -präferenzen sowie technische Anforderungen bestimmt.
* Bietet keine Dienste auf Anwendungsebene, wie Middleware (z.B. Nachrichtenbusse),
  Datenverarbeitungs-Frameworks (z.B. Spark), Datenbanken (z.B. mysql), Caches oder
  Cluster-Speichersysteme (z.B. Ceph) als eingebaute Dienste. Solche Komponenten können
  auf Kubernetes laufen und/oder von Anwendungen, die auf Kubernetes laufen, über
  portable Mechanismen wie den Open Service Broker angesprochen werden.
* Bietet keine Konfigurationssprache bzw. kein Konfigurationssystem (z.B. [jsonnet](https://github.com/google/jsonnet)).
  Es bietet eine deklarative API, die von beliebigen Formen deklarativer Spezifikationen angesprochen werden kann.
* Bietet keine umfassenden Systeme zur Maschinenkonfiguration, Wartung, Verwaltung oder Selbstheilung.

Außerdem ist Kubernetes nicht nur ein *Orchestrierungssystem*. Fakt ist, dass es die Notwendigkeit einer Orchestrierung
überflüssig macht. Die technische Definition von *Orchestrierung* ist die Ausführung eines
definierten Workflows: zuerst A, dann B, dann C. Im Gegensatz dazu besteht Kubernetes aus einer Reihe von unabhängigen,
komponierbaren Steuerungsprozessen, die den aktuellen Zustand kontinuierlich in Richtung des bereitgestellten Soll-Zustandes vorantreiben.
Es sollte keine Rolle spielen, wie Sie von A nach C kommen. Eine zentrale Steuerung ist ebenfalls nicht erforderlich.
Das Ergebnis ist ein System, das einfacher zu bedienen und leistungsfähiger, robuster, widerstandsfähiger und erweiterbar ist.

## Warum Container?

Sie suchen nach Gründen, warum Sie Container verwenden sollten?

![Why Containers?](/images/docs/why_containers.svg)

Der *Altbekannte* Weg zur Bereitstellung von Anwendungen war die Installation
der Anwendungen auf einem Host mit dem Betriebssystempaketmanager.
Dies hatte den Nachteil, dass die ausführbaren Dateien, Konfigurationen,
Bibliotheken und Lebenszyklen der Anwendungen untereinander und mit dem
Host-Betriebssystem verwoben waren. Man könnte unveränderliche
Virtual-Machine-Images erzeugen, um vorhersehbare Rollouts
und Rollbacks zu erreichen, aber VMs sind schwergewichtig und nicht portierbar.

Der *Neue Weg* besteht darin, Container auf Betriebssystemebene und nicht auf
Hardware-Virtualisierung bereitzustellen. Diese Container sind voneinander
und vom Host isoliert: Sie haben ihre eigenen Dateisysteme, sie können die
Prozesse des anderen nicht sehen, und ihr Ressourcenverbrauch kann begrenzt
werden. Sie sind einfacher zu erstellen als VMs, und da sie von der zugrunde
liegenden Infrastruktur und dem Host-Dateisystem entkoppelt sind,
sind sie über Clouds und Betriebssystem-Distributionen hinweg portabel.

Da Container klein und schnell sind, kann in jedes Containerimage eine Anwendung gepackt werden.
Diese 1:1-Beziehung zwischen Anwendung und Image ermöglicht es, die Vorteile von Containern
voll auszuschöpfen. Mit Containern können unveränderliche Container-Images eher zur Build-/Release-Zeit
als zur Deployment-Zeit erstellt werden, da jede Anwendung nicht mit dem Rest des Anwendungsstacks komponiert
werden muss und auch nicht mit der Produktionsinfrastrukturumgebung verbunden ist. Die Generierung von
Container-Images zum Zeitpunkt der Erstellung bzw. Freigabe ermöglicht es, eine konsistente Umgebung
von der Entwicklung bis zur Produktion zu gewährleisten.
Ebenso sind Container wesentlich transparenter als VMs, was die Überwachung und Verwaltung erleichtert.
Dies gilt insbesondere dann, wenn die Prozesslebenszyklen der Container von der Infrastruktur verwaltet
werden und nicht von einem Prozess-Supervisor im Container versteckt werden.
Schließlich, mit einer einzigen Anwendung pro Container, wird die Verwaltung
der Container gleichbedeutend mit dem Management des Deployments der Anwendung.

Zusammenfassung der Container-Vorteile:

* **Agile Anwendungserstellung und -bereitstellung**:
    Einfachere und effizientere Erstellung von Container-Images im Vergleich zur Verwendung von VM-Images.
* **Kontinuierliche Entwicklung, Integration und Bereitstellung**:
    Bietet eine zuverlässige und häufige Erstellung und Bereitstellung von Container-Images
    mit schnellen und einfachen Rollbacks (aufgrund der Unveränderlichkeit des Images).
* **Dev und Ops Trennung der Bedenken**:
    Erstellen Sie Anwendungscontainer-Images nicht zum Deployment-, sondern zum Build-Releasezeitpunkt
    und entkoppeln Sie so Anwendungen von der Infrastruktur.
* **Überwachbarkeit**
    Nicht nur Informationen und Metriken auf Betriebssystemebene werden angezeigt,
    sondern auch der Zustand der Anwendung und andere Signale.
* **Umgebungskontinuität in Entwicklung, Test und Produktion**:
    Läuft auf einem Laptop genauso wie in der Cloud.
* **Cloud- und OS-Distribution portabilität**:
    Läuft auf Ubuntu, RHEL, CoreOS, On-Prem, Google Kubernetes Engine und überall sonst.
* **Anwendungsorientiertes Management**:
    Erhöht den Abstraktionsgrad vom Ausführen eines Betriebssystems auf virtueller Hardware
    bis zum Ausführen einer Anwendung auf einem Betriebssystem unter Verwendung logischer Ressourcen.
* **Locker gekoppelte, verteilte, elastische, freie [micro-services](https://martinfowler.com/articles/microservices.html)**:
    Anwendungen werden in kleinere, unabhängige Teile zerlegt und können dynamisch bereitgestellt
    und verwaltet werden -- nicht ein monolithischer Stack, der auf einer großen Single-Purpose-Maschine läuft.
* **Ressourcenisolierung**:
    Vorhersehbare Anwendungsleistung.
* **Ressourcennutzung**:
    Hohe Effizienz und Dichte.

## Was bedeutet Kubernetes? K8s?

Der Name **Kubernetes** stammt aus dem Griechischen, bedeutet *Steuermann* oder
*Pilot*, und ist der Ursprung von *Gouverneur* und
[cybernetic](http://www.etymonline.com/index.php?term=cybernetics). *K8s*
ist eine Abkürzung, die durch Ersetzen der 8 Buchstaben "ubernete" mit "8" abgeleitet wird.



## {{% heading "whatsnext" %}}

*   [Bereit loszulegen](/docs/setup/)?
*   Weitere Einzelheiten finden Sie in der [Kubernetes Dokumentation](/docs/home/).



