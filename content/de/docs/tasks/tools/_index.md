---
title: "Werkzeuge installieren"
description: Kubernetes Tools auf dem Computer einrichten.
weight: 10
no_list: true
---

## kubectl

<!-- overview -->
Das Kubernetes Kommandozeilen Programm, [kubectl](/docs/references/kubectl/kubectl/), erlaubt es Befehle gegen das Kubernetes Cluster auszuführen. Du kannst kubectl zum Bereitstellen von Anwendung, dem Inspizieren und dem Verwalten von Cluster Ressourcen sowie dem Abrufen von Logs verwenden. Für weitere Informationen und der kompletten Liste von kubectl Befehlen steht eine ausführliche[`kubectl` Referenz-Dokumentation](/docs/reference/kubectl/) zur Verfügung.

kubectl kann auf eine Vielzahl von Linux Plattformen, macOS und Windows installiert werden. Siehe in der entsprechenden Anleitung für dein Betriebssystem nach.

- [Installiere kubectl auf Linux](/docs/tasks/tools/install-kubectl-linux)
- [Installiere kubectl auf macOS](/docs/tasks/tools/install-kubectl-macos)
- [Installiere kubectl auf Windows](/docs/tasks/tools/install-kubectl-windows)

## kind

[`kind`](https://kind.sigs.k8s.io/docs/) erlaubt es Kubernetes auf deinem lokalen Computer auszuführen. Hierzu muss [Docker](https://docs.docker.com/get-docker/) installiert und konfiguriert sein.

Die kind [Schnellstart](https://kind.sigs.k8s.io/docs/user/quick-start/) Seite zeigt dir was du brauchst um mit kind loslegen zu können.

<a class="btn btn-primary" href="https://kind.sigs.k8s.io/docs/user/quick-start/" role="button" aria-label="View kind Quick Start Guide">Gehe zum kind Schnellstart Guide</a>

## minikube

[`minikube`](https://minikube.sigs.k8s.io/) ist wie `kind` ein Tool um lokal Kubernetes auszuführen. `minikube` führt einen einzelnen Kubernetes Knoten als Cluster auf deinem persönlichen Computer aus (inklusive Windows, macOS und Linux). Damit kannst du Kubernetes lokal testen oder für deine täglichen Entwicklungsaufgaben nutzen.

Der offizielle [Durchstarten!](https://minikube.sigs.k8s.io/docs/start/) Guide hilft dir beim Einrichten von minikube.

<a class="btn btn-primary" href="https://minikube.sigs.k8s.io/docs/start/" role="button" aria-label="View minikube Get Started! Guide">Gehe zum minikube Durchstarten! Guide</a>

Sobald `minikube` fumktioniert, kannst du eine [Beispielanwendung](/docs/tutorials/hello-minikube/) ausführen.

## kubeadm

Du kannst {{< glossary_tooltip term_id="kubeadm" text="kubeadm" >}} zum Erstellen und verwalten von Kubernetes Clustern verwenden.
Es führt alle Schritte aus um ein minimal nützliches, sicheres, nutzerfreundliches Cluster zu erstellen. 

Die [Installationsanleitung kubeadm](/docs/setup/production-environment/tools/kubeadm/install-kubeadm/) zeigt dir wie du kubeadm auf deinen Computer aufsetzt.
Sobald dies installiert ist, kannst du dem [Erstelle ein Cluster](/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/) Guide folgen.

<a class="btn btn-primary" href="/docs/setup/production-environment/tools/kubeadm/install-kubeadm/" role="button" aria-label="View kubeadm Install Guide">Gehe zur kubeadm Installationsanleitung</a>


