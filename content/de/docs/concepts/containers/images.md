---
title: Images
content_type: concept
weight: 10
---
<!-- overview -->

Sie erstellen ihr Docker Image und laden es in eine Registry hoch, bevor es in einem Kubernetes Pod referenziert werden kann.

Die `image` Eigenschaft eines Containers unterstüzt die gleiche Syntax wie die des `docker` Kommandos, inklusive privater Registries und Tags.




<!-- body -->

## Aktualisieren von Images

Die Standardregel für das Herunterladen von Images ist `IfNotPresent`, dies führt dazu, dass das Kubelet Images überspringt, die bereits auf einem Node vorliegen.
Wenn sie stattdessen möchten, dass ein Image immer forciert heruntergeladen wird, können sie folgendes tun:


- Die `imagePullPolicy` des Containers auf `Always` setzen.
- Die `imagePullPolicy` auslassen und `:latest` als Image Tag nutzen.
- Die `imagePullPolicy` und den Tag des Images auslassen.
- Den [AlwaysPullImages](/docs/reference/access-authn-authz/admission-controllers/#alwayspullimages) Admission Controller aktivieren.

Beachten Sie, dass Sie die Nutzung des `:latest` Tags vermeiden sollten. Für weitere Informationen siehe: [Best Practices for Configuration](/docs/concepts/configuration/overview/#container-images).

## Multi-Architektur Images mit Manifesten bauen

Das Docker Kommandozeilenwerkzeug unterstützt jetzt das Kommando `docker manifest` mit den Subkommandos `create`, `annotate` and `push`.
Diese Kommandos können dazu genutzt werden Manifeste zu bauen und diese hochzuladen. 

Weitere Informationen finden sie in der Docker Dokumentation:
https://docs.docker.com/edge/engine/reference/commandline/manifest/

Hier einige Beispiele wie wir dies in unserem Build - Prozess nutzen:
https://cs.k8s.io/?q=docker%20manifest%20(create%7Cpush%7Cannotate)&i=nope&files=&repos=

Diese Kommandos basieren rein auf dem Docker Kommandozeileninterface und werden auch damit ausgeführt. Sie sollten entweder die Datei `$HOME/.docker/config.json` bearbeiten und den `experimental` Schlüssel auf `enabled` setzen, oder einfach die Umgebungsvariable `DOCKER_CLI_EXPERIMENTAL` auf `enabled` setzen, wenn Sie das Docker Kommandozeileninterface aufrufen.


{{< note >}}
Nutzen die bitte Docker *18.06 oder neuer*, ältere Versionen haben entweder Bugs oder unterstützen die experimentelle Kommandozeilenoption nicht. Beispiel: https://github.com/docker/cli/issues/1135 verursacht Probleme unter containerd.

{{< /note >}}

Wenn mit alten Manifesten Probleme auftreten, können sie die alten Manifeste in `$HOME/.docker/manifests` entfernen, um von vorne zu beginnen.

Für Kubernetes selbst nutzen wir typischerweise Images mit dem Suffix `-$(ARCH)`. Um die Abwärtskompatibilität zu erhalten, bitten wir Sie, die älteren Images mit diesen Suffixen zu generieren. Die Idee dahinter ist z.B., das `pause` image zu generieren, welches das Manifest für alle Architekturen hat, `pause-amd64` wäre dann abwärtskompatibel zu älteren Konfigurationen, oder YAML - Dateien, die ein Image mit Suffixen hart kodiert enthalten.


## Nutzung einer privaten Registry

Private Registries könnten Schlüssel erfordern um Images von ihnen herunterzuladen.
Authentifizierungsdaten können auf verschiedene Weisen hinterlegt werden:


  - Bei der Google Container Registry
    - Je Cluster
    - Automatisch in der Google Compute Engine oder Google Kubernetes Engine
    - Allen Pods erlauben von der privaten Registry des Projektes lesen zu können
  - Bei der Amazon Elastic Container Registry (ECR)
    - IAM Rollen und Richtlinien nutzen um den Zugriff auf ECR Repositories zu kontrollieren
    - Automatisch ECR Authentifizierungsdaten aktualisieren
  - Bei der Oracle Cloud Infrastructure Registry (OCIR)
    - IAM Rollen und Richtlinien nutzen um den Zugriff auf OCIR Repositories zu kontrollieren
  - Bei der Azure Container Registry (ACR)
  - Bei der IBM Cloud Container Registry
  -  Nodes konfigurieren sich bei einer privaten Registry authentifizieren zu können
    - Allen Pods erlauben von jeder konfigurierten privaten Registry lesen zu können
    - Setzt die Konfiguration der Nodes durch einen Cluster - Aministrator voraus
  - Im Voraus heruntergeladene Images
    - Alle Pods können jedes gecachte Image auf einem Node nutzen
    - Setzt root - Zugriff auf allen Nodes zum Einrichten voraus
  - Spezifizieren eines ImagePullSecrets auf einem Pod
    - Nur Pods, die eigene Secret tragen, haben Zugriff auf eine private Registry

Jede Option wird im Folgenden im Detail beschrieben


### Bei Nutzung der Google Container Registry

Kubernetes hat eine native Unterstützung für die [Google Container
Registry (GCR)](https://cloud.google.com/tools/container-registry/) wenn es auf der Google Compute
Engine (GCE) läuft. Wenn Sie ihren Cluster auf GCE oder der Google Kubernetes Engine betreiben, genügt es, einfach den vollen Image Namen zu nutzen (z.B. gcr.io/my_project/image:tag ).

Alle Pods in einem Cluster haben dann Lesezugriff auf Images in dieser Registry.

Das Kubelet authentifiziert sich bei GCR mit Nutzung des Google service Kontos der jeweiligen Instanz.
Das Google Servicekonto der Instanz hat einen `https://www.googleapis.com/auth/devstorage.read_only`, so kann es vom GCR des Projektes herunter, aber nicht hochladen.


### Bei Nutzung der Amazon Elastic Container Registry

Kubernetes bietet native Unterstützung für die [Amazon Elastic Container Registry](https://aws.amazon.com/ecr/), wenn Knoten AWS EC2 Instanzen sind.

Es muss einfach nur der komplette Image Name (z.B. `ACCOUNT.dkr.ecr.REGION.amazonaws.com/imagename:tag`) in der Pod - Definition genutzt werden.

Alle Benutzer eines Clusters, die Pods erstellen dürfen, können dann jedes der Images in der ECR Registry zum Ausführen von Pods nutzen.

Das Kubelet wird periodisch ECR Zugriffsdaten herunterladen und auffrischen, es benötigt hierfür die folgenden Berechtigungen:

- `ecr:GetAuthorizationToken`
- `ecr:BatchCheckLayerAvailability`
- `ecr:GetDownloadUrlForLayer`
- `ecr:GetRepositoryPolicy`
- `ecr:DescribeRepositories`
- `ecr:ListImages`
- `ecr:BatchGetImage`

Voraussetzungen:

- Sie müssen Kubelet in der Version `v1.2.0` nutzen. (Führen sie z.B. (e.g. run `/usr/bin/kubelet --version=true` aus um die Version zu prüfen)
- Sie benötigen Version `v1.3.0` oder neuer wenn ihre Knoten in einer A - Region sind und sich ihre Registry in einer anderen B - Region befindet.
- ECR muss in ihrer Region angeboten werden

Fehlerbehebung:

- Die oben genannten Voraussetzungen müssen erfüllt sein.
- Laden sie die $REGION (z.B. `us-west-2`) Zugriffsdaten auf ihren Arbeitsrechner. Verbinden sie sich per SSH auf den Host und nutzen die Docker mit diesen Daten. Funktioniert es?
- Prüfen sie ob das Kubelet it dem Parameter `--cloud-provider=aws` läuft.
- Prüfen sie die Logs des Kubelets (z.B. mit `journalctl -u kubelet`) auf Zeilen wie:
  - `plugins.go:56] Registering credential provider: aws-ecr-key`
  - `provider.go:91] Refreshing cache for provider: *aws_credentials.ecrProvider`

### Bei Nutzung der Azure Container Registry (ACR)
Bei Nutzung der [Azure Container Registry](https://azure.microsoft.com/en-us/services/container-registry/) können sie sich entweder als ein administrativer Nutzer, oder als ein Service Principal authentifizieren.
In jedem Fall wird die Authentifizierung über die Standard - Docker Authentifizierung ausgeführt. Diese Anleitung bezieht sich auf das [azure-cli](https://github.com/azure/azure-cli) Kommandozeilenwerkzeug.

Sie müssen zunächst eine Registry und Authentifizierungsdaten erstellen, eine komplette Dokumentation dazu finden sie hier: [Azure container registry documentation](https://docs.microsoft.com/en-us/azure/container-registry/container-registry-get-started-azure-cli).

Sobald sie ihre Container Registry erstellt haben, nutzen sie die folgenden Authentifizierungsdaten:

   * `DOCKER_USER` : Service Principal oder Administratorbenutzername
   * `DOCKER_PASSWORD`: Service Principal Password oder Administratorpasswort
   * `DOCKER_REGISTRY_SERVER`: `${some-registry-name}.azurecr.io`
   * `DOCKER_EMAIL`: `${some-email-address}`

Wenn sie diese Variablen befüllt haben, können sie:
[Kubernetes konfigurieren und damit einen Pod deployen](/docs/concepts/containers/images/#specifying-imagepullsecrets-on-a-pod).

### Bei Nutzung der IBM Cloud Container Registry
Die IBM Cloud Container Registry bietet eine mandantenfähige Private Image Registry, die Sie nutzen können, um ihre Docker Images sicher zu speichern und zu teilen.
Standardmäßig werden Images in ihrer Private Registry vom integrierten Schwachstellenscaner durchsucht, um Sicherheitsprobleme und potentielle Schwachstellen zu finden. Benutzer können ihren IBM Cloud Account nutzen, um Zugang zu ihren Images zu erhalten, oder um einen Token zu generieren, der Zugriff auf die Registry Namespaces erlaubt.

Um das IBM Cloud Container Registry Kommandozeilenwerkzeug zu installieren und einen Namespace für ihre Images zu erstellen, folgen sie dieser Dokumentation [Getting started with IBM Cloud Container Registry](https://cloud.ibm.com/docs/services/Registry?topic=registry-getting-started).

Sie können die IBM Cloud Container Registry nutzen, um Container aus [IBM Cloud public images](https://cloud.ibm.com/docs/services/Registry?topic=registry-public_images) und ihren eigenen Images in den `default` Namespace ihres IBM Cloud Kubernetes Service Clusters zu deployen.
Um einen Container in einen anderen Namespace, oder um ein Image aus einer anderen IBM Cloud Container Registry Region oder einem IBM Cloud account zu deployen, erstellen sie ein Kubernetes `imagePullSecret`.
Weitere Informationen finden sie unter: [Building containers from images](https://cloud.ibm.com/docs/containers?topic=containers-images).

### Knoten für die Nutzung einer Private Registry konfigurieren

{{< note >}}
Wenn sie  Google Kubernetes Engine verwenden, gibt es schon eine `.dockercfg` auf jedem Knoten, die Zugriffsdaten für ihre Google Container Registry beinhaltet. Dann kann die folgende Vorgehensweise nicht angewendet werden.
{{< /note >}}

{{< note >}}
Wenn sie AWS EC2 verwenden und die EC2 Container Registry (ECR) nutzen, wird das Kubelet auf jedem Knoten die ECR Zugriffsdaten verwalten und aktualisieren. Dann kann die folgende Vorgehensweise nicht angewendet werden.
{{< /note >}}

{{< note >}}
Diese Vorgehensweise ist anwendbar, wenn sie ihre Knoten-Konfiguration ändern können; Sie wird nicht zuverlässig auf GCE oder einem anderen Cloud - Provider funktionieren, der automatisch Knoten ersetzt.
{{< /note >}}

{{< note >}}
Kubernetes unterstützt zurzeit nur die `auths` und `HttpHeaders` Abschnitte der Dockerkonfiguration. Das bedeutet, dass die Hilfswerkzeuge (`credHelpers` ooderr `credsStore`) nicht unterstützt werden.
{{< /note >}}

Docker speichert Schlüssel für eigene Registries entweder unter `$HOME/.dockercfg` oder `$HOME/.docker/config.json`. Wenn sie die gleiche Datei in einen der unten aufgeführten Suchpfade speichern, wird Kubelet sie als Hilfswerkzeug für Zugriffsdaten beim Beziehen von Images nutzen.


*   `{--root-dir:-/var/lib/kubelet}/config.json`
*   `{cwd of kubelet}/config.json`
*   `${HOME}/.docker/config.json`
*   `/.docker/config.json`
*   `{--root-dir:-/var/lib/kubelet}/.dockercfg`
*   `{cwd of kubelet}/.dockercfg`
*   `${HOME}/.dockercfg`
*   `/.dockercfg`

{{< note >}}
Eventuell müssen sie `HOME=/root` in ihrer Umgebungsvariablendatei setzen.
{{< /note >}}

Dies sind die empfohlenen Schritte, um ihre Knoten für eine Nutzung einer eigenen Registry zu konfigurieren.
In diesem Beispiel führen sie folgende Schritte auf ihrem Desktop/Laptop aus:

   1. Führen sie `docker login [server]` für jeden Satz ihrer Zugriffsdaten aus.  Dies aktualisiert `$HOME/.docker/config.json`.
   2. Prüfen Sie `$HOME/.docker/config.json` in einem Editor darauf, ob dort nur Zugriffsdaten enthalten sind, die Sie nutzen möchten.
   3. Erhalten sie eine Liste ihrer Knoten:
      - Wenn sie die Namen benötigen: `nodes=$(kubectl get nodes -o jsonpath='{range.items[*].metadata}{.name} {end}')`
      - Wenn sie die IP - Adressen benötigen: `nodes=$(kubectl get nodes -o jsonpath='{range .items[*].status.addresses[?(@.type=="ExternalIP")]}{.address} {end}')`
   4. Kopieren sie ihre lokale `.docker/config.json` in einen der oben genannten Suchpfade.
      - Zum Beispiel: `for n in $nodes; do scp ~/.docker/config.json root@$n:/var/lib/kubelet/config.json; done`

Prüfen durch das Erstellen eines Pods, der ein eigenes Image nutzt, z.B.:

```yaml
kubectl apply -f - <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: private-image-test-1
spec:
  containers:
    - name: uses-private-image
      image: $PRIVATE_IMAGE_NAME
      imagePullPolicy: Always
      command: [ "echo", "SUCCESS" ]
EOF
pod/private-image-test-1 created
```
Wenn alles funktioniert, sollten sie nach einigen Momenten folgendes sehen:

```shell
kubectl logs private-image-test-1
SUCCESS
```
Wenn es nicht funktioniert, sehen Sie:

```shell
kubectl describe pods/private-image-test-1 | grep "Failed"
  Fri, 26 Jun 2015 15:36:13 -0700    Fri, 26 Jun 2015 15:39:13 -0700    19    {kubelet node-i2hq}    spec.containers{uses-private-image}    failed        Failed to pull image "user/privaterepo:v1": Error: image user/privaterepo:v1 not found
```

Sie müssen sich darum kümmern, dass alle Knoten im Cluster die gleiche `.docker/config.json` haben, andernfalls werden Pods auf einigen Knoten starten, auf anderen jedoch nicht.
Wenn sie zum Beispiel Knoten automatisch skalieren lassen, sollte dann jedes Instanztemplate die `.docker/config.json` beinhalten, oder ein Laufwerk einhängen, das diese beinhaltet.

Alle Pods haben Lesezugriff auf jedes Image in ihrer eigenen Registry, sobald die Registry - Schlüssel zur `.docker/config.json` hinzugefügt wurden.

### Im Voraus heruntergeladene Images

{{< note >}}
Wenn sie Google Kubernetes Engine verwenden, gibt es schon eine `.dockercfg` auf jedem Knoten die Zugriffsdaten für ihre Google Container Registry beinhaltet. Dann kann die folgende Vorgehensweise nicht angewendet werden.
{{< /note >}}

{{< note >}}
Diese Vorgehensweise ist anwendbar, wenn sie ihre Knoten-Konfiguration ändern können; Sie wird nicht zuverlässig auf GCE oder einem anderen Cloud - Provider funktionieren, der automatisch Knoten ersetzt.
{{< /note >}}

Standardmäßig wird das Kubelet versuchen, jedes Image von der spezifizierten Registry herunterzuladen.
Falls jedoch die `imagePullPolicy` Eigenschaft der Containers auf `IfNotPresent` oder `Never` gesetzt wurde, wird ein lokales Image genutzt (präferiert oder exklusiv, jenachdem).

Wenn Sie sich auf im Voraus heruntergeladene Images als Ersatz für eine Registry - Authentifizierung verlassen möchten, müssen sie sicherstellen, dass alle Knoten die gleichen, im Voraus heruntergeladenen Images aufweisen.

Diese Medthode kann dazu genutzt werden, bestimmte Images aus Geschwindigkeitsgründen im Voraus zu laden, oder als Alternative zur Authentifizierung an einer eigenen Registry zu nutzen.

Alle Pods haben Leserechte auf alle im Voraus geladenen Images.

### Spezifizieren eines ImagePullSecrets für einen Pod

{{< note >}}
Diese Vorgehensweise ist aktuell die empfohlene Vorgehensweise für Google Kubernetes Engine, GCE, und jeden Cloud - Provider bei dem die Knotenerstelltung automatisiert ist.
{{< /note >}}

Kubernetes unterstützt die Spezifikation von Registrierungsschlüsseln für einen Pod.

#### Erstellung eines Secrets mit einer Docker Konfiguration

Führen sie folgenden Befehl mit Ersetzung der groß geschriebenen Werte aus:

```shell
kubectl create secret docker-registry <name> --docker-server=DOCKER_REGISTRY_SERVER --docker-username=DOCKER_USER --docker-password=DOCKER_PASSWORD --docker-email=DOCKER_EMAIL
```

Wenn Sie bereits eine Datei mit Docker-Zugriffsdaten haben, können Sie die Zugriffsdaten als ein Kubernetes Secret importieren:
[Create a Secret based on existing Docker credentials](/docs/tasks/configure-pod-container/pull-image-private-registry/#registry-secret-existing-credentials) beschreibt die Erstellung.
Dies ist insbesondere dann sinnvoll, wenn sie mehrere eigene Container Registries nutzen, da `kubectl create secret docker-registry` ein Secret erstellt, das nur mit einer einzelnen eigenen Registry funktioniert.

{{< note >}}
Pods können nur eigene Image Pull Secret in ihrem eigenen Namespace referenzieren, somit muss dieser Prozess jedes mal einzeln für jeden Namespace angewendet werden.

{{< /note >}}

#### Referenzierung eines imagePullSecrets bei einem Pod

Nun können Sie Pods erstellen, die dieses Secret referenzieren, indem Sie einen Aschnitt `imagePullSecrets` zu ihrer Pod - Definition hinzufügen.

```shell
cat <<EOF > pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: foo
  namespace: awesomeapps
spec:
  containers:
    - name: foo
      image: janedoe/awesomeapp:v1
  imagePullSecrets:
    - name: myregistrykey
EOF

cat <<EOF >> ./kustomization.yaml
resources:
- pod.yaml
EOF
```

Dies muss für jeden Pod getan werden, der eine eigene Registry nutzt.

Die Erstellung dieser Sektion kann jedoch automatisiert werden, indem man imagePullSecrets einer [serviceAccount](/docs/user-guide/service-accounts) Ressource hinzufügt.
[Add ImagePullSecrets to a Service Account](/docs/tasks/configure-pod-container/configure-service-account/#add-imagepullsecrets-to-a-service-account) bietet detaillierte Anweisungen hierzu.

Sie können dies in Verbindung mit einer auf jedem Knoten genutzten `.docker/config.json` benutzen, die Zugriffsdaten werden dann zusammengeführt. Dieser Vorgehensweise wird in der Google Kubernetes Engine funktionieren.


### Anwendungsfälle

Es gibt eine Anzahl an Lösungen um eigene Registries zu konfigurieren, hier sind einige Anwendungsfälle und empfohlene Lösungen.

1. Cluster die nur nicht-proprietäre Images (z.B. open-source) ausführen. Images müssen nicht versteckt werden.
   - Nutzung von öffentlichen Images auf Docker Hub.
     - Keine Konfiguration notwendig.
     - Auf GCE/Google Kubernetes Engine, wird automatisch ein lokaler Spiegel für eine verbesserte Geschwindigkeit und Verfügbarkeit genutzt.
2. Cluster die einige proprietäre Images ausführen die für Außenstehende nicht sichtbar sein dürfen, aber für alle Cluster - Benutzer sichtbar sein sollen.
   - Nutzung einer gehosteten privaten Registry [Docker registry](https://docs.docker.com/registry/).
     - Kann auf [Docker Hub](https://hub.docker.com/signup), oder woanders gehostet werden.
     - Manuelle Konfiguration der .docker/config.json auf jedem Knoten, wie oben beschrieben.
   - Der Betrieb einer internen privaten Registry hinter ihrer Firewall mit offenen Leseberechtigungen.
     - Keine Kubernetes - Konfiguration notwendig
   - Wenn GCE/Google Kubernetes Engine genutzt wird, nutzen sie die Google Container Registry des Projektes.
     - Funktioniert besser mit Cluster - Autoskalierung als mit manueller Knotenkonfiguration.
   - Auf einem Cluster bei dem die Knotenkonfiguration ungünstig ist können `imagePullSecrets` genutzt werden.
3. Cluster mit proprieritären Images, mit einigen Images die eine erweiterte Zugriffskontrolle erfordern.
   - Stellen sie sicher, dass [AlwaysPullImages admission controller](/docs/reference/access-authn-authz/admission-controllers/#alwayspullimages) aktiv ist, anderenfalls können alle Pods potenziell Zugriff auf alle Images haben.
   - Verschieben sie sensitive Daten in eine "Secret" Ressource statt sie im Image abzulegen.
4. Ein mandantenfähiger Cluster in dem jeder Mandant eine eigene private Registry benötigt.
   - Stellen sie sicher, dass [AlwaysPullImages admission controller](/docs/reference/access-authn-authz/admission-controllers/#alwayspullimages) aktiv ist, anderenfalls können alle Pods potenziell Zugriff auf alle Images haben.
   - Nutzen sie eine private Registry die eine Authorisierung erfordert. 
   - Generieren sie Registry - Zugriffsdaten für jeden Mandanten, abgelegt in einem Secret das in jedem Mandanten - Namespace vorhanden ist.
   - Der Mandant fügt dieses Sercret zu den imagePullSecrets in jedem seiner Namespace hinzu.



Falls sie Zugriff auf mehrere Registries benötigen, können sie ein Secret für jede Registry erstellen, Kubelet wird jedwede `imagePullSecrets` in einer einzelnen `.docker/config.json` zusammenfassen.

