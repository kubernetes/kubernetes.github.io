---
title: 스토리지로 퍼시스턴트볼륨(PersistentVolume)을 사용하도록 파드 설정하기
content_type: task
weight: 60
---

<!-- overview -->

이 페이지는 스토리지에 대해
{{< glossary_tooltip text="퍼시스턴트볼륨클레임(PersistentVolumeClaim)" term_id="persistent-volume-claim" >}}을
사용하도록 파드를 설정하는 방법을 보여준다.
과정의 요약은 다음과 같다.

1. 클러스터 관리자로서, 물리적 스토리지와 연결되는 퍼시스턴트볼륨을 
생성한다. 볼륨을 특정 파드와 연결하지 않는다.

1. 그 다음 개발자 / 클러스터 사용자의 역할로서, 적합한 
퍼시스턴트볼륨에 자동으로 바인딩되는 퍼시스턴트볼륨클레임을 
생성한다.

1. 스토리지에 대해 위의 퍼시스턴트볼륨클레임을 사용하는 파드를 생성한다.



## {{% heading "prerequisites" %}}


* 사용자는 노드가 단 하나만 있는 쿠버네티스 클러스터가 필요하고,
{{< glossary_tooltip text="kubectl" term_id="kubectl" >}}
커맨드라인 툴이 사용자의 클러스터와 통신할 수 있도록 설정되어 있어야 한다. 만약 사용자가 
아직 단일 노드 클러스터를 가지고 있지 않다면, [Minikube](/ko/docs/tasks/tools/#minikube)를 
사용하여 클러스터 하나를 생성할 수 있다.

* [퍼시스턴트 볼륨](https://minikube.sigs.k8s.io/docs/)의 
관련 자료에 익숙해지도록 한다.

<!-- steps -->

## 사용자 노드에 index.html 파일 생성하기

사용자 클러스터의 단일 노드에 연결되는 셸을 연다. 셸을 여는 방법은 
클러스터 설정에 따라 달라진다. 예를 들어 Minikube를 사용하는 경우, 
`minikube ssh` 명령어를 입력하여 노드로 연결되는 셸을 열 수 있다. 

해당 노드의 셸에서 `/mnt/data` 디렉터리를 생성한다.

```shell
# 사용자 노드에서 슈퍼유저로 명령을 수행하기 위하여
# "sudo"를 사용한다고 가정한다
sudo mkdir /mnt/data
```


`/mnt/data` 디렉터리에서 `index.html` 파일을 생성한다.

```shell
# 이번에도 사용자 노드에서 슈퍼유저로 명령을 수행하기 위하여
# "sudo"를 사용한다고 가정한다
sudo sh -c "echo 'Hello from Kubernetes storage' > /mnt/data/index.html"
```

{{< note >}}
사용자 노드에서 `sudo` 이외의 슈퍼유저 접근 툴을 사용하는 경우,
`sudo` 를 해당 툴의 이름으로 바꾸면, 동일하게 작업을 수행할 수 있다.
{{< /note >}}

`index.html` 파일이 존재하는지 테스트한다.

```shell
cat /mnt/data/index.html
```

결과는 다음과 같다.
```
Hello from Kubernetes storage
```

이제 사용자 노드에서 셸을 종료해도 된다.

## 퍼시스턴트볼륨 생성하기

이 예제에서, 사용자는 *hostPath* 퍼시스턴트볼륨을 생성한다. 쿠버네티스는 단일 노드에서의 
개발과 테스트를 위해 hostPath를 지원한다. hostPath 퍼시스턴트볼륨은 
네트워크로 연결된 스토리지를 모방하기 위해, 노드의 파일이나 디렉터리를 사용한다.

운영 클러스터에서, 사용자가 hostPath를 사용하지는 않는다. 대신, 클러스터 관리자는 
Google Compute Engine 영구 디스크, NFS 공유 또는 Amazone Elastic 
Block Store 볼륨과 같은 네트워크 자원을 프로비저닝한다. 클러스터 관리자는 
[스토리지클래스(StorageClasses)](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#storageclass-v1-storage)를 
사용하여 
[동적 프로비저닝](https://kubernetes.io/blog/2016/10/dynamic-provisioning-and-storage-in-kubernetes)을 설정할 수도 있다. 

hostPath 퍼시스턴트볼륨의 설정 파일은 아래와 같다.

{{< codenew file="pods/storage/pv-volume.yaml" >}}

설정 파일에 클러스터 노드의 `/mnt/data` 에 볼륨이 있다고
지정한다. 또한 설정에서 볼륨 크기를 10 기가바이트로 지정하고 단일 노드가
읽기-쓰기 모드로 볼륨을 마운트할 수 있는 `ReadWriteOnce` 접근 모드를
지정한다. 여기서는 
퍼시스턴트볼륨클레임의 [스토리지클래스 이름](/ko/docs/concepts/storage/persistent-volumes/#클래스)을 
`manual` 로 정의하며, 퍼시스턴트볼륨클레임의 요청을 
이 퍼시스턴트볼륨에 바인딩하는데 사용한다.

퍼시스턴트볼륨을 생성한다.

```shell
kubectl apply -f https://k8s.io/examples/pods/storage/pv-volume.yaml
```

퍼시스턴트볼륨에 대한 정보를 조회한다.

```shell
kubectl get pv task-pv-volume
```

결과는 퍼시스턴트볼륨의 `STATUS` 가 `Available` 임을 보여준다. 이는 
아직 퍼시스턴트볼륨클레임이 바인딩되지 않았다는 것을 의미한다.

    NAME             CAPACITY   ACCESSMODES   RECLAIMPOLICY   STATUS      CLAIM     STORAGECLASS   REASON    AGE
    task-pv-volume   10Gi       RWO           Retain          Available             manual                   4s

## 퍼시스턴트볼륨클레임 생성하기

다음 단계는 퍼시스턴트볼륨클레임을 생성하는 단계이다. 파드는 퍼시스턴트볼륨클레임을 
사용하여 물리적인 스토리지를 요청한다. 이 예제에서, 사용자는 적어도 
하나 이상의 노드에 대해 읽기-쓰기 접근을 지원하며 최소 3 기가바이트의 볼륨을 요청하는
퍼시스턴트볼륨클레임을 생성한다.

퍼시스턴트볼륨클레임에 대한 설정 파일은 다음과 같다.

{{< codenew file="pods/storage/pv-claim.yaml" >}}

퍼시스턴트볼륨클레임을 생성한다.

    kubectl apply -f https://k8s.io/examples/pods/storage/pv-claim.yaml

사용자가 퍼시스턴트볼륨클레임을 생성한 후에, 쿠버네티스 컨트롤 플레인은 
클레임의 요구사항을 만족하는 퍼시스턴트볼륨을 찾는다. 컨트롤 플레인이 
동일한 스토리지클래스를 갖는 적절한 퍼시스턴트볼륨을 찾으면, 
볼륨에 클레임을 바인딩한다.

퍼시스턴트볼륨을 다시 확인한다.

```shell
kubectl get pv task-pv-volume
```

이제 결과는 `STATUS` 가 `Bound` 임을 보여준다.

    NAME             CAPACITY   ACCESSMODES   RECLAIMPOLICY   STATUS    CLAIM                   STORAGECLASS   REASON    AGE
    task-pv-volume   10Gi       RWO           Retain          Bound     default/task-pv-claim   manual                   2m

퍼시스턴트볼륨클레임을 확인한다.

```shell
kubectl get pvc task-pv-claim
```

결과는 퍼시스턴트볼륨클레임이 사용자의 퍼시스턴트볼륨인 `task-pv-volume` 에 
바인딩되어 있음을 보여준다.

    NAME            STATUS    VOLUME           CAPACITY   ACCESSMODES   STORAGECLASS   AGE
    task-pv-claim   Bound     task-pv-volume   10Gi       RWO           manual         30s

## 파드 생성하기

다음 단계는 볼륨으로 퍼시스턴트볼륨클레임을 사용하는 파드를 만드는 단계이다.

파드에 대한 설정 파일은 다음과 같다.

{{< codenew file="pods/storage/pv-pod.yaml" >}}

파드의 설정 파일은 퍼시스턴트볼륨클레임을 지정하지만, 
퍼시스턴트볼륨을 지정하지는 않는다는 것을 유념하자. 파드의 관점에서 볼때, 
클레임은 볼륨이다.

파드를 생성한다.

```shell
kubectl apply -f https://k8s.io/examples/pods/storage/pv-pod.yaml
```

파드의 컨테이너가 실행 중임을 확인한다.

```shell
kubectl get pod task-pv-pod
```

사용자 파드에서 구동되고 있는 컨테이너에 셸로 접근한다.

```shell
kubectl exec -it task-pv-pod -- /bin/bash
```

사용자의 셸에서, nginx가 hostPath 볼륨으로부터 `index.html` 파일을 
제공하는지 확인한다.

```shell
# 이전 단계에서 "kubectl exec" 명령을 실행한 root 셸 안에서 
# 다음의 3개 명령을 실행해야 한다.
apt update
apt install curl
curl http://localhost/
```

결과는 hostPath 볼륨에 있는 `index.html` 파일에 사용자가 작성한 텍스트를
보여준다.

    Hello from Kubernetes storage


만약 사용자가 위와 같은 메시지를 확인하면, 파드가 퍼시스턴트볼륨클레임의 스토리지를 
사용하도록 성공적으로 설정한 것이다.

## 정리하기

파드, 퍼시스턴트볼륨클레임, 퍼시스턴트볼륨을 삭제한다.

```shell
kubectl delete pod task-pv-pod
kubectl delete pvc task-pv-claim
kubectl delete pv task-pv-volume
```

만약 클러스터의 노드에 대한 셸이 열려져 있지 않은 경우, 
이전과 동일한 방식으로 새로운 셸을 연다.

사용자 노드의 셸에서, 생성한 파일과 디렉터리를 제거한다.

```shell
# 사용자 노드에서 슈퍼유저로 명령을 수행하기 위하여
# "sudo"를 사용한다고 가정한다
sudo rm /mnt/data/index.html
sudo rmdir /mnt/data
```

이제 사용자 노드에서 셸을 종료해도 된다.




<!-- discussion -->

## 접근 제어

그룹 ID(GID)로 설정된 스토리지는 동일한 GID를 사용하는 파드에서만 쓰기 
작업을 허용한다. GID가 일치하지 않거나 누락되었을 경우 권한 
거부 오류가 발생한다. 사용자와의 조정 필요성을 줄이기 위하여 관리자는 
퍼시스턴트 볼륨에 GID로 어노테이션을 달 수 있다. 그 뒤에, 퍼시스턴트볼륨을 
사용하는 모든 파드에 대하여 GID가 자동으로 추가된다.

다음과 같이 `pv.beta.kubernetes.io/gid` 어노테이션을 사용한다.
```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv1
  annotations:
    pv.beta.kubernetes.io/gid: "1234"
```
파드가 GID 어노테이션이 있는 퍼시스턴트볼륨을 사용하면, 어노테이션으로
달린 GID가 파드의 보안 컨텍스트에 지정된 GID와 동일한 방식으로
파드의 모든 컨테이너에 적용된다. 파드의 명세 혹은 퍼시스턴트볼륨의
어노테이션으로부터 생성된 모든 GID는, 각 컨테이너에서 실행되는 첫 번째
프로세스에 적용된다.

{{< note >}}
파드가 퍼시스턴트볼륨을 사용할 때, 퍼시스턴트볼륨과 연관된 
GID는 파드 리소스 자체에는 존재하지 않는다.
{{< /note >}}




## {{% heading "whatsnext" %}}


* [퍼시스턴트볼륨](/ko/docs/concepts/storage/persistent-volumes/)에 대해 더 보기.
* [퍼시스턴트 스토리지 디자인 문서](https://git.k8s.io/community/contributors/design-proposals/storage/persistent-storage.md)에 대해 읽어보기.

### Reference

* [퍼시스턴트볼륨](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#persistentvolume-v1-core)
* [PersistentVolumeSpec](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#persistentvolumespec-v1-core)
* [퍼시스턴트볼륨클레임](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#persistentvolumeclaim-v1-core)
* [PersistentVolumeClaimSpec](/docs/reference/generated/kubernetes-api/{{< param "version" >}}/#persistentvolumeclaimspec-v1-core)
