---
reviewers:
title: kubeadm으로 컨트롤 플레인 사용자 정의하기
content_type: concept
weight: 40
---

<!-- overview -->

{{< feature-state for_k8s_version="v1.12" state="stable" >}}

kubeadm의 `ClusterConfiguration` 오브젝트는 API 서버, 컨트롤러매니저, 스케줄러와 같은 컨트롤 플레인 구성요소에 전달되는
기본 플래그 `extraArgs` 필드를 노출한다. 이 구성요소는 다음 필드를 사용하도록 정의되어 있다.

- `apiServer`
- `controllerManager`
- `scheduler`

`extraArgs` 필드는 `key: value` 쌍으로 구성되어 있다. 컨트롤 플레인 구성요소를 위한 플래그를 대체하려면 다음을 수행한다.

1.  사용자 구성에서 적절한 필드를 추가한다.
2.  필드에 대체할 플래그를 추가한다.
3.  `kubeadm init`에 `--config <CONFIG YAML 파일>` 파라미터를 추가해서 실행한다.

각 필드의 구성에서 자세한 정보를 보려면,
[API 참고 문서](https://godoc.org/k8s.io/kubernetes/cmd/kubeadm/app/apis/kubeadm/v1beta2#ClusterConfiguration)에서 확인해 볼 수 있다.

{{< note >}}
`kubeadm config print init-defaults`를 실행하고 원하는 파일에 출력을 저장하여 기본값인 `ClusterConfiguration` 오브젝트를 생성할 수 있다.
{{< /note >}}



<!-- body -->

## APIServer 플래그

자세한 내용은 [kube-apiserver 레퍼런스 문서](/docs/reference/command-line-tools-reference/kube-apiserver/)를 확인한다.

예시:
```yaml
apiVersion: kubeadm.k8s.io/v1beta2
kind: ClusterConfiguration
kubernetesVersion: v1.16.0
apiServer:
  extraArgs:
    advertise-address: 192.168.0.103
    anonymous-auth: "false"
    enable-admission-plugins: AlwaysPullImages,DefaultStorageClass
    audit-log-path: /home/johndoe/audit.log
```

## 컨트롤러매니저 플래그

자세한 내용은 [kube-controller-manager 레퍼런스 문서](/docs/reference/command-line-tools-reference/kube-controller-manager/)를 확인한다.

예시:
```yaml
apiVersion: kubeadm.k8s.io/v1beta2
kind: ClusterConfiguration
kubernetesVersion: v1.16.0
controllerManager:
  extraArgs:
    cluster-signing-key-file: /home/johndoe/keys/ca.key
    bind-address: 0.0.0.0
    deployment-controller-sync-period: "50"
```

## 스케줄러 플래그

자세한 내용은 [kube-scheduler 레퍼런스 문서](/docs/reference/command-line-tools-reference/kube-scheduler/)를 확인한다.

예시:
```yaml
apiVersion: kubeadm.k8s.io/v1beta2
kind: ClusterConfiguration
kubernetesVersion: v1.16.0
scheduler:
  extraArgs:
    config: /etc/kubernetes/scheduler-config.yaml
  extraVolumes:
    - name: schedulerconfig
      hostPath: /home/johndoe/schedconfig.yaml
      mountPath: /etc/kubernetes/scheduler-config.yaml
      readOnly: true
      pathType: "File"
```
