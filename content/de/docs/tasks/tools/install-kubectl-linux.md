---
title: Installiere und Konfiguriere kubectl auf Linux
content_type: task
weight: 10
card:
  name: tasks
  weight: 20
  title: Installiere kubectl auf Linux
---

## {{% heading "prerequisites" %}}

Zur optimalen Nutzung von kubectl sollte diese maximal eine Version unterschied zu der Version im Cluster aufweisen. Als Beispiel, ein v{{< skew latestVersion >}} Client kann mit v{{< skew prevMinorVersion >}}, v{{< skew latestVersion >}}, und v{{< skew nextMinorVersion >}} Control Planes kommunizieren. Das Verwenden der aktuellsten Version kann unvorhersehbare Probleme vorbeugen.

## Installiere kubectl auf Linux

Über folgende Wege kann kubectl auf Linux installiert werden:

- [Installiere die kubectl binary mit curl auf Linux](#installiere-die-kubectl-binary-mit-curl-auf-linux)
- [Nutze deinen nativen Paket-Manager](#nutze-deinen-nativen-paket-manager)
- [Nutze einen alternativen Paket-Manager](#nutze-einen-alternativen-paket-manager)
- [Installiere auf Linux als Teil der Google Cloud SDK](#installiere-auf-linux-als-teil-der-google-cloud-sdk)

### Installiere die kubectl binary mit curl auf Linux

1. Lade die aktuellste Version mit folgendem Befehl herunter:

   ```bash
   curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
   ```

   {{< note >}}
Um eine spezifische Version herunterzuladen ersetze den folgenden Teil `$(curl -L -s https://dl.k8s.io/release/stable.txt)` mit der Version die du beziehen möchtest.

Als Beispiel, um die Version {{< param "fullversion" >}} für Linux herunterzuladen, schreibe:

   ```bash
   curl -LO https://dl.k8s.io/release/{{< param "fullversion" >}}/bin/linux/amd64/kubectl
   ```
   {{< /note >}}

1. Validiere die Binary-Datei (Optional)

   Beziehe die kubectl Checksum Datei:

   ```bash
   curl -LO "https://dl.k8s.io/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl.sha256"
   ```

   Validiere die kubectl Binary gegenüber der Checksum Datei:

   ```bash
   echo "$(<kubectl.sha256) kubectl" | sha256sum --check
   ```

   Wenn diese valide ist, bekommst du folgende Ausgabe:

   ```console
   kubectl: OK
   ```
   Wenn die Prüfung fehl schlägt, wirft `sha256` einen Nicht-Null-Status und gibt eine ähnliche Ausgabe zurück:

   ```bash
   kubectl: FAILED
   sha256sum: WARNING: 1 computed checksum did NOT match
   ```

   {{< note >}}
   Nutze dieselbe Version für die Binary und die Checksum.
   {{< /note >}}

1. Installiere kubectl

   ```bash
   sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
   ```

   {{< note >}}
   Solltest du keinen Admin Zugang zu deinem Zielsystem haben, kannst du kubectl auch unter `~/.local/bin` installieren: 

   ```bash
   mkdir -p ~/.local/bin/kubectl
   mv ./kubectl ~/.local/bin/kubectl
   # und füge dann ~/.local/bin/kubectl zu deinem $PATH
   ```

   {{< /note >}}

1. Stelle sicher, dass die installierte Version auf dem letzte Stand ist:

   ```bash
   kubectl version --client
   ```

### Nutze deinen nativen Paket-Manager

{{< tabs name="kubectl_install" >}}
{{% tab name="Debian-basierende Distributionen" %}}

1. Aktualisiere den `apt` Paket Index und installiere die Pakete die für den Kubernetes `apt` Repository benötigt werden:

   ```shell
   sudo apt-get update
   sudo apt-get install -y apt-transport-https ca-certificates curl
   ```

2. Lade den öffentlichen Signing Key von der Google Cloud herunter:

   ```shell
   sudo curl -fsSLo /usr/share/keyrings/kubernetes-archive-keyring.gpg https://packages.cloud.google.com/apt/doc/apt-key.gpg
   ```

3. Füge nun das Kubernetes `apt` Repository hinzu:

   ```shell
   echo "deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list
   ```

4. Aktualisiere den `apt` Paket Index mit dem neuen Repository und installiere kubectl:

   ```shell
   sudo apt-get update
   sudo apt-get install -y kubectl
   ```

{{% /tab %}}

{{< tab name="Red Hat-basierende Distributionen" codelang="bash" >}}
cat <<EOF > /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
EOF
yum install -y kubectl
{{< /tab >}}
{{< /tabs >}}

### Nutze einen alternativen Paket-Manager

{{< tabs name="other_kubectl_install" >}}
{{% tab name="Snap" %}}
Wenn du Ubuntu oder eine andere Linux Distribution verwendest die den [snap](https://snapcraft.io/docs/core/install) Paket-Manager unterstützt, kannst du kubectl über [snap](https://snapcraft.io/) beziehen.

```shell
snap install kubectl --classic
kubectl version --client
```

{{% /tab %}}

{{% tab name="Homebrew" %}}
Solltest du Linux in Kombination mit [Homebrew](https://docs.brew.sh/Homebrew-on-Linux) Paket Manager verwenden, kannst du auch darüber kubectl [installieren](https://docs.brew.sh/Homebrew-on-Linux#install).

```shell
brew install kubectl
kubectl version --client
```

{{% /tab %}}

{{< /tabs >}}

### Installiere auf Linux als Teil der Google Cloud SDK

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
