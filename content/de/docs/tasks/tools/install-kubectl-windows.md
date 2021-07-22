---
title: Installiere und Konfiguriere kubectl auf Windows
content_type: task
weight: 10
card:
  name: tasks
  weight: 20
  title: Installiere kubectl auf Windows
---

## {{% heading "prerequisites" %}}

Zur optimalen Nutzung von kubectl sollte diese maximal eine Version unterschied zu der Version im Cluster aufweisen. Als Beispiel, ein v{{< skew latestVersion >}} Client kann mit v{{< skew prevMinorVersion >}}, v{{< skew latestVersion >}}, und v{{< skew nextMinorVersion >}} Control Planes kommunizieren. Das Verwenden der aktuellsten Version kann unvorhersehbare Probleme vorbeugen.

## Installiere kubectl auf Windows

Über folgende Wege kann kubectl auf Windows installiert werden:

- [Installiere die kubectl binary mit curl auf Windows](#installiere-die-kubectl-binary-mit-curl-auf-windows)
- [Nutze Chocolatey oder Scoop auf Windows](#nutze-chocolatey-oder-scoop-auf-windows)
- [Installiere auf Windows als Teil der Google Cloud SDK](#installiere-auf-windows-als-teil-der-google-cloud-sdk)


### Installiere die kubectl binary mit curl auf Windows

1. Lade die [aktuellste Version {{< param "fullversion" >}}](https://dl.k8s.io/release/{{< param "fullversion" >}}/bin/windows/amd64/kubectl.exe) mit folgendem Befehl herunter.

   Oder wenn du `curl` verwendest, nutze deine Shell um die letzte Version zu beziehen:

   ```powershell
   curl -LO https://dl.k8s.io/release/{{< param "fullversion" >}}/bin/windows/amd64/kubectl.exe
   ```

   {{< note >}}
   Um die letzte stabile Version (zum Beispiel zum Skript schreiben) zu finden schaue in die [https://dl.k8s.io/release/stable.txt](https://dl.k8s.io/release/stable.txt) Datei.
   {{< /note >}}

1. Validiere die Binary-Datei (Optional)

   Beziehe die kubectl Checksum Datei:

   ```powershell
   curl -LO https://dl.k8s.io/{{< param "fullversion" >}}/bin/windows/amd64/kubectl.exe.sha256
   ```

   Validiere die kubectl Binary gegenüber der Checksum Datei:

   - Nutze die Command Prompt um manuell die `CertUtil` Ausgabe mit der Checksum Datei zu vergleichen:

     ```cmd
     CertUtil -hashfile kubectl.exe SHA256
     type kubectl.exe.sha256
     ```

   - Nutze die PowerShell um die Verifizierung zu automatisieren, dafür musst du den `-eq` Operator verwenden um ein `True` oder `False` Ergebnis zu erhalten:

     ```powershell
     $($(CertUtil -hashfile .\kubectl.exe SHA256)[1] -replace " ", "") -eq $(type .\kubectl.exe.sha256)
     ```

1. Füge die Binary Datei in deinem `PATH` ein.

1. Stelle sicher, dass die installierte Version auf dem letzte Stand ist:

   ```cmd
   kubectl version --client
   ```

{{< note >}}
[Docker Desktop für Windows](https://docs.docker.com/docker-for-windows/#kubernetes) fügt seine eigene Version von `kubectl` in den `PATH` ein.
Wenn du zuvor schon Docker Dekstop installiert hast, musst du womöglich deinen Eintrag vor den von Docker Desktop platzieren oder diesen entfernen.
{{< /note >}}

### Nutze Chocolatey oder Scoop auf Windows

1. Um kubectl auf Windows zu installieren, kannst du entweder den [Chocolatey](https://chocolatey.org) Paket Manager oder den [Scoop](https://scoop.sh) Befehlszeilen Programm verwenden.

   {{< tabs name="kubectl_win_install" >}}
   {{% tab name="choco" %}}
   ```powershell
   choco install kubernetes-cli
   ```
   {{% /tab %}}
   {{% tab name="scoop" %}}
   ```powershell
   scoop install kubectl
   ```
   {{% /tab %}}
   {{< /tabs >}}


1. Stelle sicher, dass die installierte Version auf dem letzte Stand ist:

   ```powershell
   kubectl version --client
   ```

1. Navigiere in deinen Home Ordner:

   ```powershell
   # If you're using cmd.exe, run: cd %USERPROFILE%
   cd ~
   ```

1. Erstelle einen `.kube` Ordner:

   ```powershell
   mkdir .kube
   ```

1. Gehe in den `.kube` Ordner den du eben erstell hast:

   ```powershell
   cd .kube
   ```

1. Konfiguriere kubectl, um einen entfernten Kubernetes Cluster zu nutzen:

   ```powershell
   New-Item config -type file
   ```

{{< note >}}
Passe die Konfigurationsdatei in einem Text-Editor deiner Wahl an, bspw. Notepad.
{{< /note >}}

### Installiere auf Windows als Teil der Google Cloud SDK

{{< include "included/install-kubectl-gcloud.md" >}}

## Verifiziere die kubectl Konfiguration

{{< include "included/verify-kubectl.md" >}}

## Optionale kubectl Konfigurationen

### Aktiviere die Shell Autovervollständigung

kubectl unterstützt die Autovervollständigung für Bash und Zsh, was Einiges an Schreibarbeit abnimmt.

Nachfolgend findest du die Anleitungen zum Aktivieren der Autovervollständigung für Bash und Zsh.

{{< include "included/optional-kubectl-configs-zsh.md" >}}

## {{% heading "whatsnext" %}}

{{< include "included/kubectl-whats-next.md" >}}