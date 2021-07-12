---
draft: True
title: Nodi
content_type: concept
weight: 10
---

<!-- overview -->

Un nodo è una macchina worker in Kubernetes, precedentemente noto come `minion`. Un nodo
può essere una VM o una macchina fisica, a seconda del cluster. Ogni nodo contiene
i servizi necessari per eseguire [pods](/docs/concepts/workloads/pods/pod/) ed è gestito dal master
componenti. I servizi su un nodo includono il [container runtime](/docs/concepts/overview/components/#node-components), kubelet e kube-proxy. Vedere
[The Kubernetes Node](https://git.k8s.io/community/contributors/design-proposals/architecture/architecture.md#the-kubernetes-node) sezione in
documento di progettazione dell'architettura per maggiori dettagli.




<!-- body -->

## Node Status

Lo stato di un nodo contiene le seguenti informazioni:

* [Addresses](#addresses)
* [Condition](#condition)
* [Capacity](#capacity)
* [Info](#info)

Ogni sezione è descritta in dettaglio di seguito.

### Addresses

L'utilizzo di questi campi varia a seconda del provider cloud o della configurazione bare metal.

* HostName: il nome host riportato dal kernel del nodo. Può essere sovrascritto tramite il parametro kubelet `--hostname-override`.
* ExternalIP: in genere l'indirizzo IP del nodo che è esternamente instradabile (disponibile dall'esterno del cluster).
* InternalIP: in genere l'indirizzo IP del nodo che è instradabile solo all'interno del cluster.


### Condition

l campo `conditions` descrive lo stato di tutti i nodi` Running`.


| Condizione del nodo | Descrizione |
| ---------------- | ------------- |
| `OutOfDisk` | `True` se lo spazio disponibile sul nodo non è sufficiente per aggiungere nuovi pod, altrimenti` False` |
| `Pronto` | `True` se il nodo è integro e pronto ad accettare i pod,` False` se il nodo non è integro e non accetta i pod e `Sconosciuto` se il controller del nodo non è stato ascoltato dal nodo nell'ultimo` nodo-monitor -grace-periodo` (il valore predefinito è 40 secondi) |
| `MemoryPressure` | `Vero` se la pressione esiste sulla memoria del nodo, ovvero se la memoria del nodo è bassa; altrimenti `False` |
    | `PIDPressure` | `True` se la pressione esiste sui processi, ovvero se ci sono troppi processi sul nodo; altrimenti `False` |
| `DiskPressure` | `True` se esiste una pressione sulla dimensione del disco, ovvero se la capacità del disco è bassa; altrimenti `False` |
| `NetworkUnavailable` | `True` se la rete per il nodo non è configurata correttamente, altrimenti` False` |

La condizione del nodo è rappresentata come un oggetto JSON. Ad esempio, la seguente risposta descrive un nodo sano.

```json
"conditions": [
  {
    "type": "Ready",
    "status": "True"
  }
]
```

Se lo stato della condizione Ready rimane `Unknown` o` False` per un tempo superiore a `pod-eviction-timeout`, viene passato un argomento al [gestore-kube-controller](/docs/admin/kube-controller-manager/) e tutti i pod sul nodo sono programmati per la cancellazione dal controller del nodo. La durata predefinita del timeout di sfratto è di ** cinque minuti **. In alcuni casi, quando il nodo non è raggiungibile, l'apiserver non è in grado di comunicare con kubelet sul nodo. La decisione di eliminare i pod non può essere comunicata al kubelet fino a quando non viene ristabilita la comunicazione con l'apiserver. Nel frattempo, i pod che sono programmati per la cancellazione possono continuare a funzionare sul nodo partizionato.

Nelle versioni di Kubernetes precedenti alla 1.5, il controllore del nodo [forzerebbe la cancellazione](/docs/concepts/workloads/pods/pod/#force-deletion-of-pods)
questi pod non raggiungibili dall'apiserver. Tuttavia, in 1.5 e versioni successive, il controller del nodo non impone l'eliminazione dei pod finché non lo è
confermato che hanno smesso di funzionare nel cluster. Puoi vedere i pod che potrebbero essere in esecuzione su un nodo irraggiungibile
lo stato `Terminating` o` Unknown`. Nei casi in cui Kubernetes non può dedurre dall'infrastruttura sottostante se ha un nodo
lasciato permanentemente un cluster, potrebbe essere necessario che l'amministratore del cluster elimini manualmente l'oggetto nodo. Cancellare l'oggetto nodo da
Kubernetes fa sì che tutti gli oggetti Pod in esecuzione sul nodo vengano eliminati dal server apis e libera i loro nomi.


Nella versione 1.12, la funzione `TaintNodesByCondition` è promossa in versione beta, quindi il controller del ciclo di vita del nodo crea automaticamente
[taints](/docs/concepts/configuration/taint-and-toleration/) che rappresentano le condizioni.
Allo stesso modo lo schedulatore ignora le condizioni quando si considera un nodo; anziché
guarda le tinte del Nodo e le tolleranze di un Pod.

Ora gli utenti possono scegliere tra il vecchio modello di pianificazione e un nuovo modello di pianificazione più flessibile.
Un pod che non ha tolleranze viene pianificato in base al vecchio modello. Ma un baccello quello
tollera che i nodi di un nodo particolare possano essere programmati su quel nodo.

{{< caution >}}
ESe si disabilita questa funzione si crea un leggero ritardo tra il
tempo in cui una condizione viene osservata e quando viene creata una contaminazione. Questo ritardo è in genere inferiore a un secondo, ma può aumentare il numero di pod pianificati correttamente ma rifiutati dal kubelet.
{{< /caution >}}

### Capacity


Descrive le risorse disponibili sul nodo: CPU, memoria e il massimo
numero di pod che possono essere programmati sul nodo.

### Info

Informazioni generali sul nodo, come la versione del kernel, la versione di Kubernetes
(versione kubelet e kube-proxy), versione Docker (se utilizzata), nome del sistema operativo.
Le informazioni sono raccolte da Kubelet dal nodo.

## Management

Unlike [pods](/docs/concepts/workloads/pods/pod/) and [services](/docs/concepts/services-networking/service/),
a node is not inherently created by Kubernetes: it is created externally by cloud
providers like Google Compute Engine, or it exists in your pool of physical or virtual
machines. So when Kubernetes creates a node, it creates
an object that represents the node. After creation, Kubernetes
checks whether the node is valid or not. For example, if you try to create
a node from the following content:

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

Kubernetes crea un oggetto nodo internamente (la rappresentazione), e
convalida il nodo tramite il controllo dello stato in base al campo `metadata.name`. Se il nodo è valido - cioè, se necessario
i servizi sono in esecuzione, è idoneo per l'esecuzione di un pod. Altrimenti, lo è
ignorato per qualsiasi attività del cluster finché non diventa valido.

{{<note>}}
Kubernetes mantiene l'oggetto per il nodo non valido e continua a verificare se diventa valido.
È necessario eliminare esplicitamente l'oggetto Nodo per interrompere questo processo.
{{</ note>}}

Attualmente, ci sono tre componenti che interagiscono con il nodo di Kubernetes
interfaccia: controller del nodo, kubelet e kubectl.

### Node Controller

Il controller del nodo è un componente master di Kubernetes che gestisce vari
aspetti dei nodi.

Il controller del nodo ha più ruoli nella vita di un nodo. Il primo sta assegnando a
Blocco CIDR sul nodo quando è registrato (se l'assegnazione CIDR è attivata).

Il secondo è mantenere aggiornato l'elenco interno dei nodi del controller del nodo
l'elenco delle macchine disponibili del provider cloud. Quando si corre in una nuvola
ambiente, ogni volta che un nodo non è sano, il controller del nodo chiede al cloud
fornitore se la VM per quel nodo è ancora disponibile. Altrimenti, il nodo
controller cancella il nodo dalla sua lista di nodi.

Il terzo è il monitoraggio della salute dei nodi. Il controller del nodo è
responsabile dell'aggiornamento della condizione NodeReady di NodeStatus a
Condizione Notata quando un nodo diventa irraggiungibile (ad esempio, il controller del nodo si arresta
ricevere heartbeat per qualche motivo, ad es. a causa del fatto che il nodo si trova in basso), e poi in seguito sfratto
tutti i pod dal nodo (usando una terminazione elegante) se il nodo continua
essere irraggiungibile. (I timeout predefiniti sono 40 secondi per iniziare la segnalazione
ConditionUnknown e 5m dopo di ciò per iniziare a sfrattare i pod.) 

Il controller del nodo controlla lo stato di ogni nodo ogni `--node-monitor-period` secondi.

Nelle versioni di Kubernetes precedenti alla 1.13, NodeStatus è l'heartbeat di
nodo. A partire da Kubernetes 1.13, la funzionalità di lease del nodo viene introdotta come un
funzione alfa (porta caratteristica `NodeLease`,
[KEP-0009](https://github.com/kubernetes/enhancements/blob/master/keps/sig-node/0009-node-heartbeat.md)).
Quando la funzione di lease del nodo è abilitata, ogni nodo ha un oggetto `Lease` associato in
spazio dei nomi `kube-node-lease` che viene rinnovato periodicamente dal nodo ed entrambi
NodeStatus e lease del nodo vengono considerati heartbeat dal nodo. Locazioni di nodi
si rinnovano frequentemente mentre NodeStatus viene segnalato solo dal nodo al master
quando c'è qualche cambiamento o è passato abbastanza tempo (il default è 1 minuto, che
è più lungo del timeout predefinito di 40 secondi per i nodi non raggiungibili). Da
il lease del nodo è molto più leggero di NodeStatus, questa caratteristica rende nodo
battito cardiaco significativamente più economico sia per la scalabilità che per le prestazioni
prospettive.

In Kubernetes 1.4, abbiamo aggiornato la logica del controller del nodo per gestire meglio
casi in cui un numero elevato di nodi ha problemi con il raggiungimento del master
(ad esempio perché il master ha problemi di rete). A partire da 1.4, il nodo
controller controlla lo stato di tutti i nodi nel cluster quando si effettua un
decisione sullo sfratto del pod.

Nella maggior parte dei casi, il controller del nodo limita il tasso di sfratto a
`--node-eviction-rate` (default 0.1) al secondo, il che significa che non eliminerà i pod
da più di 1 nodo per 10 secondi.

Il comportamento di sfratto del nodo cambia quando un nodo in una determinata zona di disponibilità
diventa malsano. Il controller del nodo controlla quale percentuale di nodi nella zona
sono malsani (la condizione NodeReady è ConditionUnknown o ConditionFalse) a
lo stesso tempo. Se la frazione di nodi malsani è almeno
`--unhealthy-zone-threshold` (default 0.55) quindi il tasso di sfratto è ridotto:
se il cluster è piccolo (cioè ha meno o uguale a
`--large-cluster-size-threshold` nodes - default 50) quindi gli sfratti sono
fermato, altrimenti il ​​tasso di sfratto è ridotto a
`--secondary-node-eviction-rate` (default 0.01) al secondo. 

La ragione per cui le politiche sono implementate per zona di disponibilità è perché una zona di disponibilità
potrebbe divenire partizionato dal master mentre gli altri rimangono connessi. Se
il tuo cluster non si estende su più zone di disponibilità del provider cloud, quindi
c'è solo una zona di disponibilità (l'intero cluster).

Un motivo chiave per diffondere i nodi tra le zone di disponibilità è che
il carico di lavoro può essere spostato in zone sane quando un'intera zona viene interrotta.
Pertanto, se tutti i nodi in una zona non sono sani, il controller del nodo viene sottratto a
la normale frequenza `--node-eviction-rate`. Il caso d'angolo è quando tutte le zone sono
completamente malsano (cioè non ci sono nodi sani nel cluster). In tale
caso, il controller del nodo presuppone che ci sia qualche problema con il master
connettività e interrompe tutti gli sfratti fino a quando non viene ripristinata la connettività.

A partire da Kubernetes 1.6, il NodeController è anche responsabile della rimozione
i pod che sono in esecuzione sui nodi con `NoExecute`, quando i pod non tollerano
i taints. Inoltre, come caratteristica alfa che è disabilitata per impostazione predefinita, il
NodeController è responsabile per l'aggiunta di taints corrispondenti ai problemi del nodo come
nodo irraggiungibile o non pronto. Vedi [questa documentazione](/docs/concepts/configuration/taint-and-toleration/)
per i dettagli su `NoExecute` taints e la funzione alpha.

partire dalla versione 1.8, il controller del nodo può essere reso responsabile della creazione di taints che rappresentano le condizioni del nodo.
Questa è una caratteristica alfa della versione 1.8.

### Self-Registration of Nodes

Quando il flag kubelet `--register-node` è vero (il default), il kubelet tenterà di farlo
registrarsi con il server API. Questo è il modello preferito, utilizzato dalla maggior parte delle distro.

Per l'autoregistrazione, il kubelet viene avviato con le seguenti opzioni:

  - `--kubeconfig` - Percorso delle credenziali per autenticarsi sull'apiserver.
  - `--cloud-provider` - Come parlare con un provider cloud per leggere i metadati su se stesso.
  - `--register-node` - Si registra automaticamente con il server API.
  - `--register-with-taints` - Registra il nodo con la lista data di taints (separati da virgola` <chiave> = <valore>: <effetto> `). No-op se `register-node` è falso.
  - `--node-ip` - Indirizzo IP del nodo.
  - `--node-labels` - Etichette da aggiungere quando si registra il nodo nel cluster (vedere le restrizioni dell'etichetta applicate dal [plugin di accesso NodeRestriction](/docs/reference/access-authn-authz/admission-controller/#noderestriction) in 1.13+).
  - `--node-status-update-frequency` - Specifica la frequenza con cui kubelet invia lo stato del nodo al master

Quando [Node authorization mode](/docs/reference/access-authn-authz/node/) e
[NodeRestriction admission plugin](/docs/reference/access-authn-authz/admission-controllers/#noderestriction) sono abilitati,
kubelets è autorizzato solo a creare / modificare la propria risorsa nodo.

#### Manual Node Administration

Un amministratore di cluster può creare e modificare oggetti nodo.

Se l'amministratore desidera creare manualmente oggetti nodo, imposta il flag kubelet
`--Register nodo = false`.

L'amministratore può modificare le risorse del nodo (indipendentemente dall'impostazione di `--register-node`).
Le modifiche includono l'impostazione di etichette sul nodo e la marcatura non programmabile.

Le etichette sui nodi possono essere utilizzate insieme ai selettori di nodo sui pod per controllare la pianificazione,
per esempio. vincolare un pod per poter essere eseguito solo su un sottoinsieme di nodi.

Contrassegnare un nodo come unschedulable impedisce a nuovi pod di essere programmati per quello
nodo, ma non ha alcun effetto sui pod esistenti sul nodo. Questo è utile come
fase preparatoria prima del riavvio del nodo, ecc. Ad esempio, per contrassegnare un nodo
unschedulable, esegui questo comando:

```shell
kubectl cordon $NODENAME
```

{{< note >}}
I pod creati da un controller DaemonSet bypassano lo scheduler di Kubernetes
e non rispettare l'attributo unschedulable su un nodo. Questo presuppone che i demoni appartengano
la macchina anche se viene scaricata dalle applicazioni mentre si prepara per un riavvio.
{{< /note >}}

### Node capacity

La capacità del nodo (numero di cpu e quantità di memoria) è parte dell'oggetto nodo.
Normalmente, i nodi si registrano e segnalano la loro capacità durante la creazione dell'oggetto nodo. Se
stai facendo [amministrazione manuale del nodo](#manual-node-administration), quindi devi impostare il nodo
capacità quando si aggiunge un nodo.

Lo scheduler di Kubernetes garantisce che ci siano risorse sufficienti per tutti i pod su un nodo. esso
controlla che la somma delle richieste di container sul nodo non sia maggiore della capacità del nodo. esso
include tutti i contenitori avviati da kubelet, ma non i contenitori avviati direttamente dal [contenitore runtime](/docs/concepts/overview/components/#node-components) né qualsiasi processo eseguito all'esterno dei contenitori.

Se si desidera riservare esplicitamente risorse per processi non Pod, seguire questo tutorial su
[riserva risorse per i demoni di sistema](/docs/tasks/administration-cluster/reserve-compute-resources/#system-reserved).


## API Object

Il nodo è una risorsa di livello superiore nell'API REST di Kubernetes. Maggiori dettagli su
L'oggetto API può essere trovato a:
[Node API object](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#node-v1-core).


