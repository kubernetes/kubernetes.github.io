---
reviewers:
- jsafrane
- saad-ali
- thockin
- msau42
- xing-yang
title: Volumes Persistentes
feature:
  title: Orquestração de Armazenamento
  description: >
    Montar automaticamente o armazenamento de sua escolha, seja de um armazenamento local, de um provedor de cloud pública, como <a href="https://cloud.google.com/storage/">GCP</a> ou <a href="https://aws.amazon.com/products/storage/">AWS</a>, ou um armazenameto de rede, como NFS, iSCSI, Gluster, Ceph, Cinder ou Flocker.

content_type: conceito
weight: 20
---

<!-- visão geral -->

Esse documento descreve o estado atual dos _volumes persistentes_ no Kubernetes. Sugerimos que esteja familiarizado com [volumes](/docs/concepts/storage/volumes/).

<!-- body -->

## Introdução


O gerenciamento de armazenamento é uma questão bem diferente do gerenciamento de instâncias computacionais. O subsistema PersistentVolume provê uma API para usuários e administradores que mostra de forma detalhada de como o armazenamento é provido e como ele é consumido. Para isso, nós introduzimos duas novas APIs:  PersistentVolume e PersistentVolumeClaim.

Um _PersistentVolume_ (PV) é uma parte do armazenamento dentro do cluster que tenha sido provisionada por um administrador, ou dinamicamente utilizando [Classes de Armazenamento](/docs/concepts/storage/storage-classes/). Isso é um recurso dentro do cluster da mesma forma que um nó também é. PVs são plugins de volume da mesma forma que Volumes, porém eles têm um ciclo de vida independente de qualquer Pod que utilize um PV. Essa API tem por objetivo mostrar os detalhes da implementação do armazenamento, seja ele NFS, iSCSI, ou um armazenamento específico de um provedor de cloud pública.

Uma_PersistentVolumeClaim_ (PVC) é uma requisição para armazenamento por um usuário. É similar a um Pod. Pods utilizam recursos do nó e PVCs utilizam recursos do PV. Pods podem solicitar níveis específicos de recursos (CPU e Memória). Claims podem solicitar tamanho e modos de acesso específicos (exemplo: montagem como ReadWriteOnce, ReadOnlyMany ou ReadWriteMany, veja [Modos de Acesso](#modos-de-acesso)).

Enquanto as PersistentVolumeClaims permitem que um usuário utilize recursos de armazenamento de forma limitada, é comum que usuários precisem de PersistentVolumes com diversas propriedades, como desempenho, para problemas diversos. Os administradores de cluster precisam estar aptos a oferecer uma variedade de PersistentVolumes que difiram em tamanho e modo de acesso, sem expor os usuários a detalhes de como esses volumes são implementados. Para necessidades como essas, temos o recurso de _StorageClass_.

Veja os [exemplos de passo a passo de forma detalhada](/docs/tasks/configure-pod-container/configure-persistent-volume-storage/).

## Requisição e ciclo de vida de um volume

PVs são recursos dentro um cluster. PVCs são requisições para esses recursos e também atuam como uma validação da solicitação desses recursos. O ciclo de vida da interação entre PVs e PVCs funcionam da seguinte forma:

### Provisionamento

Existem duas formas de provisionar um PV: estaticamente ou dinamicamente.

#### Estático

O administrador do cluster cria uma determinada quantidade de PVs. Eles possuem todos os detalhes do armazenamento os quais estão atrelados, que neste caso fica disponível para utilização por um usuário dentro do cluster. Eles estão presentes na API do Kubernetes e disponíveis para utilização.

#### Dinâmico

Quando nenhum dos PVs estáticos, que foram criados anteriormente pelo administrador, satisfazem os critérios de uma PersistentVolumeClaim enviado por um usuário, o cluster pode tentar realizar um provisionamento dinâmico para atender a essa PVC. Esse provisionamento é baseado em StorageClasses: a PVC deve solicitar uma [classe de armazenamento](/docs/concepts/storage/storage-classes/) e o administrador deve ter previamente criado e configurado essa classe para que o provisionamento dinâmico possa ocorrer. Requisições que solicitam a classe `""` efetivamente desabilitam o provisionamento dinâmico para elas mesmas.

Para habilitar o provisionamento de armazenamento dinâmico baseado em classe de armazenamento, o administrador do cluster precisa habilitar o [controle de admissão](/docs/reference/access-authn-authz/admission-controllers/#defaultstorageclass) `DefaultStorageClass` no servidor da API. Isso pode ser feito, por exemplo, garantindo que `DefaultStorageClass` esteja entre aspas simples, ordenado por uma lista de valores para a flag `--enable-admission-plugins`, componente do servidor da API. Para mais informações sobre os comandos das flags do servidor da API, consulte a documentação [kube-apiserver](/docs/admin/kube-apiserver/).

### Binding

Um usuário cria, ou em caso de um provisionamento dinâmico já ter criado, uma PersistentVolumeClaim solicitando uma quantidade específica de armazenamento e um determinado modo de acesso. Um controle de loop no master monitora por novas PVCs, encontra um PV (se possível) que satisfaça os requisitos e realiza o bind. Se o PV foi provisionado dinamicamente por uma PVC, o loop sempre vai fazer o bind desse PV com essa PVC em específico. Caso contrário, o usuário vai receber no mínimo o que ele havia solicitado, porém, o volume possa exceder em relação à solicitação inicial. Uma vez realizado esse processo, PersistentVolumeClaim sempre vai ter um bind exclusivo, sem levar em conta como o isso aconteceu. Um bind entre uma PVC e um PV é um mapeamento de um para um, utilizando o ClaimRef que é um bind bidirecional entre o PersistentVolume e o PersistentVolumeClaim.

As requisições permanecerão sem bind se o volume solicitado não existir. O bind ocorrerá somente se os requisitos forem atendidos exatamente da mesma forma como solicitado. Por exemplo, um bind de uma PVC de 100 GB não ocorrerá num cluster que foi provisionado com vários PVs de 50 GB. O bind ocorrerá somente no momento em que um PV de 100 GB for adicionado.

### Utilização

Pods utilizam requisições como volumes. O cluster inspeciona a requisição para encontrar o volume atrelado a ela e monta esse volume para um Pod. Para volumes que suportam múltiplos modos de acesso, o usuário especifica qual o modo desejado quando utiliza essas requisições.

Uma vez que o usuário tem a requisição atrelada a um PV, ele pertence ao usuário pelo tempo que ele precisar. Usuários agendam Pods e acessam seus PVs requisitados através da seção `persistentVolumeClaim` no bloco `volumes` do Pod. Para mais detalhes sobre isso, veja [Requisições como Volumes](#requisições-como-volumes).

### Proteção de Uso de um Objeto de Armazenamento

O propósito da funcionalidade do Objeto de Armazenamento em Proteção de Uso é garantir que as PersistentVolumeClaims (PVCs) que estejam sendo utilizadas por um Pod e PersistentVolume (PVs) que pertençam aos PVCs não sejam removidos do sistema, pois isso pode resultar numa perda de dados.

{{< note >}}
Uma PVC está sendo utilizada por um Pod quando existe um Pod que está usando essa PVC.
{{< /note >}}

Se um usuário deleta uma PVC que está sendo utilizada por um Pod, esta PVC não é removida imediatamente. A remoção da PVC é adiada até que a PVC não esteja mais sendo utilizado por nenhum Pod. Se um administrador deleta um PV que está atrelado a uma PVC, o PV não é removido imediatamente também. A remoção do PV é adiada até que o PV não esteja mais atrelado à PVC.

Note que uma PVC é protegida quando o status da PVC é `Terminating` e a lista `Finalizers` contém `kubernetes.io/pvc-protection`:

```shell
kubectl describe pvc hostpath
Name:          hostpath
Namespace:     default
StorageClass:  example-hostpath
Status:        Terminating
Volume:
Labels:        <none>
Annotations:   volume.beta.kubernetes.io/storage-class=example-hostpath
               volume.beta.kubernetes.io/storage-provisioner=example.com/hostpath
Finalizers:    [kubernetes.io/pvc-protection]
...
```

Note que um PV é protegido quando o status da PVC é `Terminating` e a lista `Finalizers` contém `kubernetes.io/pv-protection` também:

```shell
kubectl describe pv task-pv-volume
Name:            task-pv-volume
Labels:          type=local
Annotations:     <none>
Finalizers:      [kubernetes.io/pv-protection]
StorageClass:    standard
Status:          Terminating
Claim:
Reclaim Policy:  Delete
Access Modes:    RWO
Capacity:        1Gi
Message:
Source:
    Type:          HostPath (bare host directory volume)
    Path:          /tmp/data
    HostPathType:
Events:            <none>
```

### Recuperação

Quando um usuário não precisar mais utilizar um volume, ele pode deletar a PVC pela API, que, permite a recuperação do recurso. A política de recuperação para um PersistentVolume diz ao cluster o que fazer com o volume após ele ter sido liberado da sua requisição. Atualmente, volumes podem ser Retidos, Reciclados ou Deletados.

#### Retenção

A política `Retain` permite a recuperação de forma manual do recurso. Quando a PersistentVolumeClaim é deletada, ela continua existindo e o volume é considerado "livre". Mas ele ainda não está disponível para outra requisição porque os dados da requisição anterior ainda permanecem no volume. Um administrador pode manualmente recuperar o volume executando os seguintes passos: 


1. Deletar o PersistentVolume. O armazenamento associado à infraestrutura externa (AWS EBS, GCE PD, Azure Disk ou Cinder volume) ainda continuará existindo após o PV ser deletado.
1. Limpar os dados de forma manual no armazenamento associado.
1. Deletar manualmente o armazenamento associado. Caso você queira utilizar o mesmo armazenamento, crie um novo PersistentVolume com esse armazenamento.

#### Deletar

Para plugins de volume que suportam a política de recuperação `Delete`, a deleção vai remover o tanto o PersistentVolume do Kubernetes, quanto o armazenamento associado à infraestrutura externa, como AWS EBS, GCE PD, Azure Disk, ou Cinder volume. Volumes que foram provisionados dinamicamente herdam a [política de retenção da sua StorageClass](#política-de-retenção), que por padrão é `Delete`. O administrador precisa configurar a StorageClass de acordo com as necessidades dos usuários. Caso contrário, o PV deve ser editado ou reparado após sua criação. Veja [Alterar a política de retenção de um PersistentVolume](/docs/tasks/administer-cluster/change-pv-reclaim-policy/).

#### Reciclar

{{< warning >}}
A política de retenção `Recycle` está depreciada. Ao invés disso, recomendamos a utilização de provisionamento dinâmico.
{{< /warning >}}

Em caso do volume plugin ter suporte a essa operação, a política de retenção `Recycle` faz uma limpeza básica (`rm -rf /thevolume/*`) no volume e torna ele disponível novamente para outra requisição.

Contudo, um administrador pode configurar um template personalizado de um Pod reciclador utilizando a linha de comando do gerenciamento de controle do Kubernetes como descrito em [referência](/docs/reference/command-line-tools-reference/kube-controller-manager/).
O Pod reciclador personalizado deve conter a spec `volume` como é mostrado no exemplo abaixo:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pv-recycler
  namespace: default
spec:
  restartPolicy: Never
  volumes:
  - name: vol
    hostPath:
      path: /any/path/it/will/be/replaced
  containers:
  - name: pv-recycler
    image: "k8s.gcr.io/busybox"
    command: ["/bin/sh", "-c", "test -e /scrub && rm -rf /scrub/..?* /scrub/.[!.]* /scrub/*  && test -z \"$(ls -A /scrub)\" || exit 1"]
    volumeMounts:
    - name: vol
      mountPath: /scrub
```

Contudo, o caminho especificado no Pod reciclador personalizado em `volumes` é substituído pelo caminho do volume que está sendo reciclado.

### Reservando um PersistentVolume

A camada de gerenciamento pode [fazer o bind de um PersistentVolumeClaims com  PersistentVolumes equivalentes](#binding) no cluster. Contudo, se você quer que uma PVC faça um bind com um PV específico, é preciso fazer o pré-bind deles.

Especificando um PersistentVolume na PersistentVolumeClaim, você declara um bind entre uma PVC e um PV específico. O bind ocorrerá se o PersistentVolume existir e não estiver reservado por uma PersistentVolumeClaims através do seu campo `claimRef`. 

O bind ocorre independentemente se algum volume atender ao critério, incluindo afinidade de nó. A camada de gerenciamento verifica se a [classe de armazenamento](/docs/concepts/storage/storage-classes/), modo de acesso e tamanho do armazenamento solicitado ainda são válidos.

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: foo-pvc
  namespace: foo
spec:
  storageClassName: "" # Empty string must be explicitly set otherwise default StorageClass will be set
  volumeName: foo-pv
  ...
```

Esse método não garante nenhum privilégio de bind no PersistentVolume. Para evitar que alguma outra PersistentVolumeClaims possa usar o PV que você especificar, você precisa primeiro reservar esse volume de armazenamento. Especifique sua PersistentVolumeClaim no campo `claimRef` do PV para que outras PVCs não façam bind nele.

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: foo-pv
spec:
  storageClassName: ""
  claimRef:
    name: foo-pvc
    namespace: foo
  ...
```

Isso é útil se você deseja utilizar PersistentVolumes que possuem suas `claimPolicy` configuradas para `Retain`, incluindo situações onde você estiver reutilizando um PV existente.

### Expandindo Requisições de Volumes Persistentes

{{< feature-state for_k8s_version="v1.11" state="beta" >}}

Agora, o suporte à expansão de PersistentVolumeClaims (PVCs) já é habilitado por padrão. Você pode expandir os tipos de volumes abaixo:

* gcePersistentDisk
* awsElasticBlockStore
* Cinder
* glusterfs
* rbd
* Azure File
* Azure Disk
* Portworx
* FlexVolumes
* {{< glossary_tooltip text="CSI" term_id="csi" >}}

Você só pode expandir uma PVC se o campo da classe de armazenamento `allowVolumeExpansion` é `true`.

``` yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: gluster-vol-default
provisioner: kubernetes.io/glusterfs
parameters:
  resturl: "http://192.168.10.100:8080"
  restusuário: ""
  secretNamespace: ""
  secretName: ""
allowVolumeExpansion: true
```

Para solicitar um volume maior para uma PVC, edite a PVC e especifique um tamanho maior. Isso irá fazer com o que volume atrelado ao respectivo PersistentVolume seja expandido. Nunca um PersistentVolume é criado para satisfazer a requisição. Ao invés disso, um volume existente é redimensionado. 

#### Expansão de volume CSI 

{{< feature-state for_k8s_version="v1.16" state="beta" >}}

O suporte à expansão de volumes CSI é habilitada por padrão, porém é necessário um driver CSI específico para suportar a expansão do volume. Verifique a documentação do driver CSI específico para mais informações.

#### Redimensionando um volume que contém um sistema de arquivo

Só podem ser redimensionados os volumes que contém os seguintes sistemas de arquivo: XFS, Ext3 ou Ext4.

Quando um volume contém um sistema de arquivo, o sistema de arquivo somente é redimensionado quando um novo Pod está utilizando a PersistentVolumeClaim no modo `ReadWrite`. A expansão de sistema de arquivo é feita quando um Pod estiver inicializando ou quando um Pod estiver em execução e o respectivo sistema de arquivo tenha suporte para expansão a quente.

FlexVolumes permitem redimensionamento se o `RequiresFSResize` do drive é configurado como `true`. O FlexVolume pode ser redimensionado na reinicialização do Pod.

#### Redimensionamento de uma PersistentVolumeClaim em uso

{{< feature-state for_k8s_version="v1.15" state="beta" >}}

{{< note >}}
A Expansão de PVCs em uso está disponível como beta desde o Kubernetes 1.15, e como alpha desde a versão 1.11. A funcionalidade `ExpandInUsePersistentVolumes` precisa ser habilitada, o que já está automático para vários clusters que possuem funcionalidades beta. Verifique a documentação [feature gate](/docs/reference/command-line-tools-reference/feature-gates/) para mais informações.
{{< /note >}}

Neste caso, você não precisa deletar e recriar um Pod ou um deployment que está sendo utilizado por uma PVC existente.
Automaticamente, qualquer PVC em uso fica disponível para o Pod assim que o sistema de arquivo for expandido.
Essa funcionalidade não tem efeito em PVCs que não estão em uso por um Pod ou deployment. Você deve criar um Pod que utilize a PVC antes que a expansão seja completada.

Da mesma forma que outros tipos de volumes - volumes FlexVolume também podem ser expandidos quando estiverem em uso por um Pod.

{{< note >}}
Redimensionamento de FlexVolume somente é possível quando o respectivo driver suportar essa operação.
{{< /note >}}

{{< note >}}
Expandir volumes do tipo EBS é uma operação que toma muito tempo. Além disso, só é possível fazer uma modificação por volume a cada 6 horas.
{{< /note >}}

#### Recuperação em caso de falha na expansão de volumes

Se a expansão do respectivo armazenamento falhar, o administrador do cluster pode recuperar manualmente o estado da Persistent Volume Claim (PVC) e cancelar as solicitações de redimensionamento. Caso contrário, as tentativas de solicitação de redimensionamento ocorrerão de forma contínua pelo controlador sem nenhuma intervenção do administrador.

1. Marque o PersistentVolume(PV) que estiver atrelado à PersistentVolumeClaim(PVC) com a política de recuperação `Retain`.
2. Delete a PVC. Desde que o PV tenha a política de recuperação `Retain` - nenhum dado será perdido quando a PVC for recriada. 
3. Delete a entrada `claimRef` da especificação do PV para que uma PVC possa fazer bind com ele. Isso deve tornar o PV `Available`.
4. Recrie a PVC com um tamanho menor que o PV e configure o campo `volumeName` da PCV com o nome do PV. Isso deve fazer o bind de uma nova PVC a um PV existente.
5. Não esqueça de restaurar a política de recuperação do PV.

## Tipos de volumes persistentes

Tipos de PersistentVolume são implementados como plugins. Atualmente o Kubernetes suporta os plugins abaixo:

* [`awsElasticBlockStore`](/docs/concepts/storage/volumes/#awselasticblockstore) - AWS Elastic Block Store (EBS)
* [`azureDisk`](/docs/concepts/storage/volumes/#azuredisk) - Azure Disk
* [`azureFile`](/docs/concepts/storage/volumes/#azurefile) - Azure File
* [`cephfs`](/docs/concepts/storage/volumes/#cephfs) - CephFS volume
* [`cinder`](/docs/concepts/storage/volumes/#cinder) - Cinder (OpenStack block storage)
  (**depreciado**)
* [`csi`](/docs/concepts/storage/volumes/#csi) - Container Storage Interface (CSI)
* [`fc`](/docs/concepts/storage/volumes/#fc) - Fibre Channel (FC) storage
* [`flexVolume`](/docs/concepts/storage/volumes/#flexVolume) - FlexVolume
* [`flocker`](/docs/concepts/storage/volumes/#flocker) - Flocker storage
* [`gcePersistentDisk`](/docs/concepts/storage/volumes/#gcepersistentdisk) - GCE Persistent Disk
* [`glusterfs`](/docs/concepts/storage/volumes/#glusterfs) - Glusterfs volume
* [`hostPath`](/docs/concepts/storage/volumes/#hostpath) - HostPath volume
  (somente para teste de nó único; ISSO NÃO FUNCIONARÁ num cluster multi-nós; ao invés disso, considere a utilização de volume `local`.)
* [`iscsi`](/docs/concepts/storage/volumes/#iscsi) - iSCSI (SCSI over IP) storage
* [`local`](/docs/concepts/storage/volumes/#local) - storage local montados nos nós.
* [`nfs`](/docs/concepts/storage/volumes/#nfs) - Network File System (NFS) storage
* `photonPersistentDisk` - Controlador Photon para disco persistente.
  (Esse tipo de volume não funciona mais desde a removação do provedor de cloud correspondente.)
* [`portworxVolume`](/docs/concepts/storage/volumes/#portworxvolume) - Volume Portworx 
* [`quobyte`](/docs/concepts/storage/volumes/#quobyte) - Volume Quobyte
* [`rbd`](/docs/concepts/storage/volumes/#rbd) - Volume Rados Block Device (RBD)
* [`scaleIO`](/docs/concepts/storage/volumes/#scaleio) - Volume ScaleIO
  (**depreciado**)
* [`storageos`](/docs/concepts/storage/volumes/#storageos) - Volume StorageOS
* [`vsphereVolume`](/docs/concepts/storage/volumes/#vspherevolume) - Volume vSphere VMDK

## Volumes Persistentes

Cada PV contém uma `spec` e um status, que é a especificação e o status do volume. O nome do PersistentVolume deve ser um [DNS](/docs/concepts/overview/working-with-objects/names#dns-subdomain-names) válido.

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv0003
spec:
  capacity:
    storage: 5Gi
  volumeMode: Filesystem
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: slow
  mountOptions:
    - hard
    - nfsvers=4.1
  nfs:
    path: /tmp
    server: 172.17.0.2
```

{{< note >}}
Talvez sejam necessários programas auxiliares para um determinado tipo de volume utilizar um PersistentVolume no cluster. Neste exemplo, o PersistentVolume é do tipo NFS e o programa auxiliar _/sbin/mount.nfs_ é necessário para suportar a montagem dos sistemas de arquivos NFS.
{{< /note >}}

### Capacidade

Geralmente, um PV terá uma capacidade de armazenamento específica. Isso é configurado usando o atributo `capacity` do PV. Veja o [Modelo de Recurso](https://git.k8s.io/community/contributors/design-proposals/scheduling/resources.md) do Kubernetes para entender as unidades aceitas pelo atributo `capacity`.

Atualmente, o tamanho do armazenamento é o único recurso que pode ser configurado ou solicitado. Os futuros atributos podem incluir IOPS, throughput, etc.

### Modo do Volume

{{< feature-state for_k8s_version="v1.18" state="stable" >}}

O Kubernetes suporta dois `volumeModes` de PersistentVolumes: `Filesystem` e `Block`.

`volumeMode` é um parâmetro opcional da API.
`Filesystem` é o modo padrão utilizado quando o parâmetro `volumeMode` é omitido.

Um volume com `volumeMode: Filesystem` é *montado* em um diretório nos Pods. Se o volume for de um dispositivo de bloco e ele estiver vazio, o Kubernetes cria o sistema de arquivo no dispositivo antes de fazer a montagem pela primeira vez.

Você pode configurar o valor do `volumeMode` para `Block` para utilizar um disco bruto como volume. Esse volume é apresentado num Pod como um dispositivo de bloco, sem nenhum sistema de arquivo. Esse modo é útil para prover ao Pod a forma mais rápida para acessar um volume, sem nenhuma camada de sistema de arquivo entre o Pod e o volume. Por outro lado, a aplicação que estiver rodando no Pod deverá saber como tratar um dispositivo de bloco. Veja [Suporte a Volume de Bloco Bruto](#raw-block-volume-support) para um exemplo de como utilizar o volume como `volumeMode: Block` num Pod.

### Modos de Acesso

Um PersistentVolume pode ser montado num host das mais variadas formas suportadas pelo provedor. Como mostrado na tabela abaixo, os provedores terão diferentes capacidades e cada modo de acesso do PV são configurados nos modos específicos suportados para cada volume em particular. Por exemplo, o NFS pode suportar múltiplos clientes read/write, mas um PV NFS específico pode ser exportado no server como read-only. Cada PV recebe seu próprio modo de acesso que descreve suas capacidades específicas.

Os modos de acesso são:

* ReadWriteOnce -- o volume pode ser montado como leitura-escrita por um nó único
* ReadOnlyMany -- o volume pode ser montado como somente-leitura por vários nós
* ReadWriteMany -- o volume pode ser montado como leitura-escrita por vários nós

Na linha de comando, os modos de acesso ficam abreviados:

* RWO - ReadWriteOnce
* ROX - ReadOnlyMany
* RWX - ReadWriteMany

> __Importante!__ Um volume somente pode ser montado utilizando um único modo de acesso por vez, independente se ele suportar mais de um. Por exemplo, um GCEPersistentDisk pode ser montado como ReadWriteOnce por um único nó ou ReadOnlyMany por vários nós, porém não simultaneamente.


| Plugin de Volume     | ReadWriteOnce          | ReadOnlyMany          | ReadWriteMany|
| :---                 | :---:                  | :---:                 | :---:        |
| AWSElasticBlockStore | &#x2713;               | -                     | -            |
| AzureFile            | &#x2713;               | &#x2713;              | &#x2713;     |
| AzureDisk            | &#x2713;               | -                     | -            |
| CephFS               | &#x2713;               | &#x2713;              | &#x2713;     |
| Cinder               | &#x2713;               | -                     | -            |
| CSI                  | depende do driver      | depende do driver     | depende do driver |
| FC                   | &#x2713;               | &#x2713;              | -            |
| FlexVolume           | &#x2713;               | &#x2713;              | depende do driver |
| Flocker              | &#x2713;               | -                     | -            |
| GCEPersistentDisk    | &#x2713;               | &#x2713;              | -            |
| Glusterfs            | &#x2713;               | &#x2713;              | &#x2713;     |
| HostPath             | &#x2713;               | -                     | -            |
| iSCSI                | &#x2713;               | &#x2713;              | -            |
| Quobyte              | &#x2713;               | &#x2713;              | &#x2713;     |
| NFS                  | &#x2713;               | &#x2713;              | &#x2713;     |
| RBD                  | &#x2713;               | &#x2713;              | -            |
| VsphereVolume        | &#x2713;               | -                     | (funcionam quando os Pods são do tipo collocated)  |
| PortworxVolume       | &#x2713;               | -                     | &#x2713;     |
| ScaleIO              | &#x2713;               | &#x2713;              | -            |
| StorageOS            | &#x2713;               | -                     | -            |

### Classe

Um PV pode ter uma classe, que é especificada na configuração do atributo `storageClassName` com o nome da [StorageClass](/docs/concepts/storage/storage-classes/). Um PV de uma classe específica só pode ser atrelado a requisições PVCs dessa mesma classe. Um PV sem `storageClassName` não possui nenhuma classe e pode ser montado somente a PVCs que não solicitem nenhuma classe em específico.

No passado, a notação `volume.beta.kubernetes.io/storage-class` era utilizada no lugar do atributo `storageClassName`. Essa notação ainda funciona. Contudo, ela será totalmente depreciada numa futura versão do Kubernetes.

### Política de Retenção

Atualmente as políticas de retenção são:

* Retain -- recuperação manual
* Recycle -- limpeza básica (`rm -rf /thevolume/*`)
* Delete -- o volume de armazenamento associado, como AWS EBS, GCE PD, Azure Disk ou OpenStack Cinder é deletado

Atualmente, somente NFS e HostPath suportam reciclagem. Volumes AWS EBS, GCE PD, Azure Disk e Cinder suportam delete.

### Opções de Montagem

Um administrador do Kubernetes pode especificar opções de montagem adicionais quando um Volume Persistente é montado num nó.

{{< note >}}
Nem todos os tipos de Volume Persistente suportam opções de montagem.
{{< /note >}}

Seguem os tipos de volumes que suportam opções de montagem.

* AWSElasticBlockStore
* AzureDisk
* AzureFile
* CephFS
* Cinder (OpenStack block storage)
* GCEPersistentDisk
* Glusterfs
* NFS
* Quobyte Volumes
* RBD (Ceph Block Device)
* StorageOS
* VsphereVolume
* iSCSI

Não há validação em relação às opções de montagem. A montagem irá falhar se houver alguma opção inválida.

No passado, a notação `volume.beta.kubernetes.io/mount-options` era usada no lugar do atributo `mountOptions`. Essa notação ainda funciona. Contudo, ela será totalmente depreciada numa futura versão do Kubernetes.

### Afinidade de Nó

{{< note >}}
Para a maioria dos tipos de volume, a configuração desse campo não se faz necessária. Isso é automaticamente populado pelos seguintes volumes de bloco do tipo: [AWS EBS](/docs/concepts/storage/volumes/#awselasticblockstore), [GCE PD](/docs/concepts/storage/volumes/#gcepersistentdisk) e [Azure Disk](/docs/concepts/storage/volumes/#azuredisk). Você precisa deixar isso configurado para volumes do tipo [local](/docs/concepts/storage/volumes/#local).
{{< /note >}}

Um PV pode especificar uma [afinidade de nó](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#volumenodeaffinity-v1-core) para definir restrições em relação ao limite de nós que podem acessar esse volume. Pods que utilizam um PV serão somente reservados para nós selecionados pela afinidade de nó.

### Estado

Um volume sempre estará em um dos seguintes estados:

* Available -- um recurso que está livre e ainda não foi atrelado a nenhuma requisição
* Bound -- um volume atrelado a uma requisição
* Released -- a requisição foi deletada, mas o curso ainda não foi recuperado pelo cluster 
* Failed -- o volume fracassou na sua recuperação automática


A CLI mostrará o nome do PV que foi atrelado à PVC

## PersistentVolumeClaims

Cada PVC contém uma `spec` e um status, que é a especificação e estado de uma requisição. O nome de um objeto PersistentVolumeClaim precisa ser um [DNS](/docs/concepts/overview/working-with-objects/names#dns-subdomain-names) válido.

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: myclaim
spec:
  accessModes:
    - ReadWriteOnce
  volumeMode: Filesystem
  resources:
    requests:
      storage: 8Gi
  storageClassName: slow
  selector:
    matchLabels:
      release: "stable"
    matchExpressions:
      - {key: environment, operator: In, values: [dev]}
```

### Modos de Acesso

As requisições usam as mesmas convenções que os volumes quando eles solicitam um armazenamento com um modo de acesso específico.

### Modos de Volume

As requisições usam as mesmas convenções que os volumes quando eles indicam o tipo de volume, seja ele um sistema de arquivo ou dispositivo de bloco.

### Recursos


Assim como Pods, as requisições podem solicitar quantidades específicas de recurso. Neste caso, a solicitação é por armazenamento. O mesmo [modelo de recurso](https://git.k8s.io/community/contributors/design-proposals/scheduling/resources.md) vale para volumes e requisições.

### Seletor

Requisições podem especifiar um [seletor de rótulo](/docs/concepts/overview/working-with-objects/labels/#label-selectors) para posteriormente filtrar um grupo de volumes. Somente os volumes que possuam rótulos que satisfaçam os critérios do seletor podem ser atrelados à requisição. O seletor pode conter dois campos:

* `matchLabels` - o volume deve ter um rótulo com esse valor
* `matchExpressions` - uma lista de requisitos, como chave, lista de valores e operador relacionado aos valores e chaves. São operadores válidos: In, NotIn, Exists e DoesNotExist.

Todos os requisitos de `matchLabels` e `matchExpressions`, são do tipo AND - todos eles juntos devem ser atendidos.

### Classe

Uma requisição pode solicitar uma classe específica através da [StorageClass](/docs/concepts/storage/storage-classes/) utilizando o atributo `storageClassName`. Neste caso o bind ocorrerá somente com os PVs que possuírem a mesma classe do `storageClassName` dos PVCs.

As PVCs não precisam necessariamente solicitar uma classe. Uma PVC com sua `storageClassName` configurada como `""` sempre solicitará um PV sem classe, dessa forma ela sempre será atrelada a um PV sem classe (que não tenha nenhuma notação, ou seja, igual a `""`). Uma PVC sem `storageClassName` não é a mesma coisa e será tratada pelo cluster de forma diferente, porém isso dependerá se o [puglin de admissão](/docs/reference/access-authn-authz/admission-controllers/#defaultstorageclass) `DefaultStorageClass` estiver habilitado.

* Se o plugin de admissão estiver habilitado, o administrador poderá especificar a StorageClass padrão. Todas as PVCs que não tiverem `storageClassName` podem ser atreladas somente a PVs que atendam a esse padrão. A especificação de uma StorageClass padrão é feita através da notação `storageclass.kubernetes.io/is-default-class` recebendo o valor `true` no objeto da StorageClass. Se o administrador não especificar nenhum padrão, o cluster vai tratar a criação de uma PVC como se o plugin de admissão estivesse desabilitado. Se mais de um valor padrão for especificado, o plugin de admissão proíbe a criação de todas as PVCs.
* Se o plugin de admissão estiver desabilitado, não haverá nenhuma notação para a StorageClass padrão. Todas as PVCs que não tiverem `storageClassName` poderão ser atreladas somente aos PVs que não possuem classe. Neste caso, as PVCs que não tiverem `storageClassName` são tratadas da mesma forma como as PVCs que possuem suas `storageClassName` configuradas como `""`.

Dependendo do modo de instalação, uma StorageClass padrão pode ser implantada num cluster Kubernetes durante a instalação pelo addon manager.

Quando uma PVC especifica um `selector` para solicitar uma StorageClass, os requisitos são do tipo AND: somente um PV com a classe solicitada e com o rótulo requisitado pode ser atrelado à PVC.

{{< note >}}
Atualmente, uma PVC que tenha `selector` não pode ter um PV dinamicamente provisionado.
{{< /note >}}

No passado, a notação `volume.beta.kubernetes.io/storage-class` era usada no lugar do atributo `storageClassName` Essa notação ainda funciona. Contudo, ela será totalmente depreciada numa futura versão do Kubernetes. 

## Requisições como Volumes

Os Pods podem ter acesso ao armazenamento utilizando a requisição como um volume. Para isso, a requisição tem que estar no mesmo namespace que o Pod. Ao localizar a requisição no namespace do Pod, o cluster passa o PersistentVolume para a requisição.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: mypod
spec:
  containers:
    - name: myfrontend
      image: nginx
      volumeMounts:
      - mountPath: "/var/www/html"
        name: mypd
  volumes:
    - name: mypd
      persistentVolumeClaim:
        claimName: myclaim
```

### Sobre Namespaces

Os binds dos PersistentVolumes são exclusivos e, desde que as PersistentVolumeClaims são objetos do namespace, fazer a montagem das requisições com "Muitos" nós (`ROX`, `RWX`) é possível somente para um namespace.

### PersistentVolumes do tipo `hostPath`

Um PersistentVolume do tipo `hostPath` utiliza um arquivo ou diretório no nó para emular um network-attached storage (NAS). Veja [um exemplo de volume do tipo `hostPath`](/docs/tasks/configure-pod-container/configure-persistent-volume-storage/#create-a-persistentvolume).

## Suporte a Volume de Bloco Bruto

{{< feature-state for_k8s_version="v1.18" state="stable" >}}

Os plugins de volume abaixo suportam volumes de bloco bruto, incluindo provisionamento dinâmico onde for aplicável:

* AWSElasticBlockStore
* AzureDisk
* CSI
* FC (Fibre Channel)
* GCEPersistentDisk
* iSCSI
* Local volume
* OpenStack Cinder
* RBD (Ceph Block Device)
* VsphereVolume

### Utilização de PersistentVolume com Volume de Bloco Bruto {#persistent-volume-using-a-raw-block-volume}

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: block-pv
spec:
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteOnce
  volumeMode: Block
  persistentVolumeReclaimPolicy: Retain
  fc:
    targetWWNs: ["50060e801049cfd1"]
    lun: 0
    readOnly: false
```

### Requisição de PersistentVolumeClaim com Volume de Bloco Bruto {#persistent-volume-claim-requesting-a-raw-block-volume}

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: block-pvc
spec:
  accessModes:
    - ReadWriteOnce
  volumeMode: Block
  resources:
    requests:
      storage: 10Gi
```

### Especificação de Pod com Dispositivo de Bloco Bruto no contêiner 

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-with-block-volume
spec:
  containers:
    - name: fc-container
      image: fedora:26
      command: ["/bin/sh", "-c"]
      args: [ "tail -f /dev/null" ]
      volumeDevices:
        - name: data
          devicePath: /dev/xvda
  volumes:
    - name: data
      persistentVolumeClaim:
        claimName: block-pvc
```

{{< note >}}
Quando adicionar um dispositivo de bloco bruto num Pod, você especifica o caminho do dispositivo no contêiner ao invés de um ponto de montagem.
{{< /note >}}

### Bind de Volumes de Bloco

Se um usuário solicita um  volume de bloco bruto através do campo `volumeMode` na `spec` da PersistentVolumeClaim, as regras de bind agora têm uma pequena diferença em relação às versões anteriores que não consideravam esse modo como parte da `spec`.
A tabela abaixo mostra as possíveis combinações que um usuário e um administrador pode especificar para requisitar um dispositivo de bloco bruto. A tabela indica se o volume será ou não atrelado com base nas combinações:
Matriz de bind de volume para provisionamento estático de volumes:

| PV volumeMode | PVC volumeMode  | Result           |
| --------------|:---------------:| ----------------:|
|   unspecified | unspecified     | BIND             |
|   unspecified | Block           | NO BIND          |
|   unspecified | Filesystem      | BIND             |
|   Block       | unspecified     | NO BIND          |
|   Block       | Block           | BIND             |
|   Block       | Filesystem      | NO BIND          |
|   Filesystem  | Filesystem      | BIND             |
|   Filesystem  | Block           | NO BIND          |
|   Filesystem  | unspecified     | BIND             |

{{< note >}}
O provisionamento estático de volumes é suportado somente na versão alpha. Os administradores devem tomar cuidado ao considerar esses valores quando estiverem trabalhando com dispositivos de bloco bruto.
{{< /note >}}

## Snapshot de Volume e Restauração de Volume a partir de um Snapshot

{{< feature-state for_k8s_version="v1.20" state="stable" >}}

O snapshot de volume é suportado somente pelo plugin de volume CSI. Veja [Snapshot de Volume](/docs/concepts/storage/volume-snapshots/) para mais detalhes. 
Plugins de volume in-tree estão depreciados. Você pode consultar sobre os plugins de volume depreciados em [Perguntas Frequentes sobre Plugins de Volume](https://github.com/kubernetes/community/blob/master/sig-storage/volume-plugin-faq.md).

### Criar uma PersistentVolumeClaim a partir de um Snapshot de Volume {#create-persistent-volume-claim-from-volume-snapshot}

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: restore-pvc
spec:
  storageClassName: csi-hostpath-sc
  dataSource:
    name: new-snapshot-test
    kind: VolumeSnapshot
    apiGroup: snapshot.storage.k8s.io
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
```

## Clonagem de Volume

A [Clonagem de Volume](/docs/concepts/storage/volume-pvc-datasource/) é possível somente com plugins de volume CSI.

### Criação de PersistentVolumeClaim a partir de uma PVC já existente {#create-persistent-volume-claim-from-an-existing-pvc}

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: cloned-pvc
spec:
  storageClassName: my-csi-plugin
  dataSource:
    name: existing-src-pvc-name
    kind: PersistentVolumeClaim
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
```

## Boas Práticas de Configuração


Se você está criando templates ou exemplos que rodam numa grande quantidade de clusters e que precisam de armazenamento persistente, recomendamos que utilize o padrão abaixo:

- Inclua objetos PersistentVolumeClaim em seu pacote de configuração (com Deployments, ConfigMaps, etc.). 
- Não inclua objetos PersistentVolume na configuração, pois o usuário que irá instanciar a configuração talvez não tenha permissão para criar PersistentVolume.
- Dê ao usuário a opção dele informar o nome de uma classe de armazenamento quando instanciar o template.
  - Se o usuário informar o nome de uma classe de armazenamento, coloque esse valor no campo `persistentVolumeClaim.storageClassName`. Isso fará com que a PVC encontre a classe de armazenamento correta se o cluster tiver a StorageClasses habilitado pelo administrador.
  - Se o usuário não informar o nome da classe de armazenamento, deixe o campo `persistentVolumeClaim.storageClassName` sem nenhum valor (vazio). Isso fará com que o PV seja provisionado automaticamente no cluster para o usuário com o StorageClass padrão. Muitos ambientes de cluster já possuem uma StorageClass padrão, ou então os administradores podem criar suas StorageClass de acordo com seus critérios.
- Durante suas tarefas de administração, busque por PVCs que após um tempo não estão sendo atreladas, pois, isso talvez indique que o cluster não tem provisionamento dinâmico (onde o usuário deveria criar um PV que satisfaça os critérios da PVC) ou cluster não tem um sistema de armazenamento (onde usuário não pode realizar um deploy solicitando PVCs).

  ## {{% heading "whatsnext" %}}


* Saiba mais sobre [Criando um PersistentVolume](/docs/tasks/configure-pod-container/configure-persistent-volume-storage/#create-a-persistentvolume).
* Saiba mais sobre [Criando um PersistentVolumeClaim](/docs/tasks/configure-pod-container/configure-persistent-volume-storage/#create-a-persistentvolumeclaim).
* Leia a [documentação sobre planejamento de Armazenamento Persistente](https://git.k8s.io/community/contributors/design-proposals/storage/persistent-storage.md).

### Referência

* [PersistentVolume](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#persistentvolume-v1-core)
* [PersistentVolumeSpec](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#persistentvolumespec-v1-core)
* [PersistentVolumeClaim](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#persistentvolumeclaim-v1-core)
