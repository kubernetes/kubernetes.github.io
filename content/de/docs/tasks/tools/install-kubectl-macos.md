---
title: Installiere und Konfiguriere kubectl oauf macOS
content_type: task
weight: 10
card:
  name: tasks
  weight: 20
  title: Install kubectl on macOS
---

## {{% heading "prerequisites" %}}

Zur optimalen Nutzung von kubectl sollte diese maximal eine Version unterschied zu der Version im Cluster aufweisen. Als Beispiel, ein v{{< skew latestVersion >}} Client kann mit v{{< skew prevMinorVersion >}}, v{{< skew latestVersion >}}, und v{{< skew nextMinorVersion >}} Control Planes kommunizieren. Das Verwenden der aktuellsten Version kann unvorhersehbare Probleme vorbeugen.

## Installiere kubectl auf macOS

Über folgende Wege kann kubectl auf macOS installiert werden:

- [Installiere die kubectl binary mit curl auf macOS](#installiere-die-kubectl-binary-mit-curl-auf-macos)
- [Installiere mit Homebrew auf macOS](#installiere-mit-homebrew-auf-macos)
- [Installiere mit Macports auf macOS](#installiere-mit-macports-auf-macos)
- [Installiere auf macOS als Teil der Google Cloud SDK](#installiere-auf-macOS-als-teil-der-google-cloud-sdk)

### Installiere die kubectl binary mit curl auf macOS

1. Lade die aktuellste Version mit folgendem Befehl herunter:

   {{< tabs name="download_binary_macos" >}}
   {{< tab name="Intel" codelang="bash" >}}
   curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/darwin/amd64/kubectl"
   {{< /tab >}}
   {{< tab name="Apple Silicon" codelang="bash" >}}
   curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/darwin/arm64/kubectl"
   {{< /tab >}}
   {{< /tabs >}}

   {{< note >}}
   Um eine spezifische Version herunterzuladen ersetze den folgenden Teil `$(curl -L -s https://dl.k8s.io/release/stable.txt)` mit der Version die du beziehen möchtest.

   Als Beispiel, um die Version {{< param "fullversion" >}} für Linux herunterzuladen, schreibe:

   ```bash
   curl -LO "https://dl.k8s.io/release/{{< param "fullversion" >}}/bin/darwin/amd64/kubectl"
   ```

   Für macOS mit Apple Silicon, schreibe:

   ```bash
   curl -LO "https://dl.k8s.io/release/{{< param "fullversion" >}}/bin/darwin/arm64/kubectl"
   ```

   {{< /note >}}

1. Validiere die Binary-Datei (Optional)

   Beziehe die kubectl Checksum Datei:

   {{< tabs name="download_checksum_macos" >}}
   {{< tab name="Intel" codelang="bash" >}}
   curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/darwin/amd64/kubectl.sha256"
   {{< /tab >}}
   {{< tab name="Apple Silicon" codelang="bash" >}}
   curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/darwin/arm64/kubectl.sha256"
   {{< /tab >}}
   {{< /tabs >}}
  
   Validiere die kubectl Binary gegenüber der Checksum Datei:

   ```bash
   echo "$(<kubectl.sha256)  kubectl" | shasum -a 256 --check
   ```

   Wenn diese valide ist, bekommst du folgende Ausgabe:

   ```console
   kubectl: OK
   ```

   Wenn die Prüfung fehl schlägt, wirft `shasum` einen Nicht-Null-Status und gibt eine ähnliche Ausgabe zurück:

   ```bash
   kubectl: FAILED
   shasum: WARNING: 1 computed checksum did NOT match
   ```

   {{< note >}}
   Nutze dieselbe Version für die Binary und die Checksum.
   {{< /note >}}

1. Mache die kubectl Binary ausführbar.

   ```bash
   chmod +x ./kubectl
   ```

1. Bewege die kubectl Binary zu einem Ordner innerhalb deines System `PATH`.

   ```bash
   sudo mv ./kubectl /usr/local/bin/kubectl
   sudo chown root: /usr/local/bin/kubectl
   ```

1. Stelle sicher, dass die installierte Version auf dem letzte Stand ist:

   ```bash
   kubectl version --client
   ```

### Installiere mit Homebrew auf macOS

Wenn du macOS und [Homebrew](https://brew.sh/) Paket Manager verwendest, kannst du kubectl mit Homebrew installieren.

1. Führe den Installationsbefehl aus:

   ```bash
   brew install kubectl 
   ```

   oder

   ```bash
   brew install kubernetes-cli
   ```

1. Stelle sicher, dass die installierte Version auf dem letzte Stand ist:

   ```bash
   kubectl version --client
   ```

### Installiere mit Macports auf macOS

Wenn du macOS und  [Macports](https://macports.org/)Paket Manager verwendest, kannst du kubectl mit Macports installieren.

1. Führe den Installationsbefehl aus:

   ```bash
   sudo port selfupdate
   sudo port install kubectl
   ```

1. Stelle sicher, dass die installierte Version auf dem letzte Stand ist:

   ```bash
   kubectl version --client
   ```


### Installiere auf macOS als Teil der Google Cloud SDK

{{< include "included/install-kubectl-gcloud.md" >}}

## Verifiziere die kubectl Konfiguration

{{< include "included/verify-kubectl.md" >}}

## Optionale kubectl Konfigurationen

### Aktiviere die Shell Autovervollständigung

kubectl unterstützt die Autovervollständigung für Bash und Zsh, was Einiges an Schreibarbeit abnimmt.

Nachfolgend findest du die Anleitungen zum Aktivieren der Autovervollständigung für Bash und Zsh.

{{< tabs name="kubectl_autocompletion" >}}
{{< tab name="Bash" include="included/optional-kubectl-configs-bash-linux.md" />}}
{{< tab name="Zsh" include="included/optional-kubectl-configs-zsh.md" />}}
{{< /tabs >}}

## {{% heading "whatsnext" %}}

{{< include "included/kubectl-whats-next.md" >}}
