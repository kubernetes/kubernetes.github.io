---


title: 서비스 내부 트래픽 정책
content_type: concept
weight: 45
---


<!-- overview -->

{{< feature-state for_k8s_version="v1.21" state="alpha" >}}

_서비스 내부 트래픽 정책_ 을 사용하면 내부 트래픽 제한이 트래픽이 시작된 
노드 내의 엔드포인트로만 내부 트래픽을 라우팅하도록 한다. 
여기서 "내부" 트래픽은 현재 클러스터의 파드로부터 시작된 트래픽을 지칭한다.
이를 통해 비용을 절감하고 성능을 개선할 수 있다.

<!-- body -->

## 서비스 내부 트래픽 정책 사용


[기능 게이트](/ko/docs/reference/command-line-tools-reference/feature-gates/)에서 
`ServiceInternalTrafficPolicy`를 활성화한 후에 
{{< glossary_tooltip text="서비스" term_id="service" >}}의 
`.spec.internalTrafficPolicy`를 `Local`로 설정하여 내부 전용 트래픽 정책을 활성화 할 수 있다.
이것은 kube-proxy가 클러스터 내부 트래픽을 위해 노드 내부 엔드포인트로만 사용하도록 한다.

{{< note >}}
지정된 서비스에 대한 엔드포인트가 없는 노드의 파드인 경우에 
서비스는 다른 노드에 엔드포인트가 있더라도 엔드포인트가 없는 것처럼 작동한다. 
(이 노드의 파드에 대해서)
{{< /note >}}

다음 예제는 서비스의 `.spec.internalTrafficPolicy`를 `Local`로 
설정하는 것을 보여 준다:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  selector:
    app: MyApp
  ports:
    - protocol: TCP
      port: 80
      targetPort: 9376
  internalTrafficPolicy: Local
```

## 작동 방식

kube-proxy는 `spec.internalTrafficPolicy` 의 설정에 따라서 라우팅되는 
엔드포인트를 필터링한다. 
이것을 `Local`로 설정하면, 노드 내부 엔드포인트만 고려한다. 
이 설정이 `Cluster`이거나 누락되었다면 모든 엔드포인트를 고려한다.
[기능 게이트](/ko/docs/reference/command-line-tools-reference/feature-gates/)의 
`ServiceInternalTrafficPolicy`를 활성화한다면, `spec.internalTrafficPolicy`는 기본값 "Cluster"로 설정된다.

## 제약조건

* 같은 서비스에서 `externalTrafficPolicy` 가 `Local`로 설정된 경우 
서비스 내부 트래픽 정책이 사용되지 않는다. 
클러스터에서 동일하지 않은 다른 서비스에서 이 두 가지 기능은 동시에 사용할 수 있다.

## {{% heading "whatsnext" %}}

* [토폴로지 인식 힌트 활성화](/docs/tasks/administer-cluster/enabling-topology-aware-hints)에 대해서 읽기
* [서비스 외부 트래픽 정책](/docs/tasks/access-application-cluster/create-external-load-balancer/#preserving-the-client-source-ip)에 대해서 읽기
* [서비스와 애플리케이션 연결하기](/ko/docs/concepts/services-networking/connect-applications-service/) 읽기
