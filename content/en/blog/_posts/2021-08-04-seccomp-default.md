---
layout: blog
title: "Hardening Kubernetes security by enabling seccomp by default"
date: 2021-08-04
slug: seccomp-default
---

**Author:** Sascha Grunert, Red Hat

_Editor's note: If you have any questions or feedback about this blog post, feel
free to reach out via the [Kubernetes slack in #sig-node][slack]._

[slack]: https://kubernetes.slack.com/messages/sig-node

---

Seccomp is a security mechanism for Linux processes to filter system calls
(syscalls) based on a set of defined rules. Applying seccomp profiles to
containerized workloads is one of the key tasks when it comes to enhancing the
security of the application deployment. Developers, site reliability engineers
and infrastructure administrators have to work hand in hand to create,
distribute and maintain the profiles over the applications life-cycle.

The [`SecurityContext`][seccontext] of Pods and Containers can be used to adjust
security related configurations of the workload. Kubernetes introduced dedicated
[seccomp related API fields][seccontext] in this `SecurityContext` with the [graduation
of seccomp to General Availability (GA)][ga] in v1.19.0. This enhancement
allowed an easier way to specify if the whole pod or a specific container should
run as:

[seccontext]: /docs/reference/kubernetes-api/workload-resources/pod-v1/#security-context-1
[ga]: https://github.com/kubernetes/enhancements/blob/cccc6fa/keps/sig-node/135-seccomp/README.md#seccomp-to-ga

- `Unconfined`: seccomp will not be enabled
- `RuntimeDefault`: the container runtimes default profile will be used
- `Localhost`: a node local profile will be applied, which is being referenced
  by a relative path to the seccomp profile root (`<kubelet-root-dir>/seccomp`)
  of the kubelet

With the graduation of seccomp, nothing has changed from an overall security
perspective, because `Unconfined` is still the default. This is totally fine if
we look from the upgrade path and backwards compatibility perspective of
Kubernetes releases. But it also means that it is more likely that a workload
runs without seccomp at all, which should be fixed in the long term.

## `SeccompDefault` to the rescue

Kubernetes v1.22.0 introduces a new kubelet [feature gate][gate]
`SeccompDefault`, which has been added in `alpha` state as every other new
feature. This means that it is disabled by default and can be enabled manually
for every single Kubernetes node.

[gate]: /docs/reference/command-line-tools-reference/feature-gates

What does the feature do? Well, it just changes the default seccomp profile from
`Unconfined` to `RuntimeDefault`. If not specified differently in the pod
manifest, then the feature will add a higher set of security constraints by
using the default profile of the container runtime. These profiles may differ
between runtimes like [CRI-O][crio] or [containerd][ctrd]. They also differ for
its used hardware architectures. But generally speaking, those default profiles
allow a common amount of syscalls while blocking the more dangerous ones, which
are unlikely or unsafe to be used in a containerized application.

[crio]: https://github.com/cri-o/cri-o/blob/fe30d62/vendor/github.com/containers/common/pkg/seccomp/default_linux.go#L45
[ctrd]: https://github.com/containerd/containerd/blob/e1445df/contrib/seccomp/seccomp_default.go#L51

### Enabling the feature

Two kubelet configuration changes have to be made to enable the feature:

- set the `SeccompDefault=true` via the command line (`--feature-gates`) or the
  [kubelet configuration][kubelet] file
- enable the feature by adding the `--seccomp-default` command line flag or via
  the [kubelet configuration][kubelet] file (`seccompDefault: true`)

[kubelet]: /docs/tasks/administer-cluster/kubelet-config-file

The kubelet will error on startup if only one of the above steps have been done.

### Trying it out

If the feature is enabled on a node, then you can create a new workload like
this:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: test-pod
spec:
  containers:
    - name: test-container
      image: nginx:1.21
```

Now it is possible to inspect the used seccomp profile by using
[`ctictl`][ctictl] while investigating the containers [runtime
specification][rspec]:

[ctictl]: https://github.com/kubernetes-sigs/cri-tools
[rspec]: https://github.com/opencontainers/runtime-spec/blob/0c021c1/config-linux.md#seccomp

```bash
CONTAINER_ID=$(sudo crictl ps -q --name=test-container)
sudo crictl inspect $CONTAINER_ID | jq .info.runtimeSpec.linux.seccomp
```

```yaml
{
  "defaultAction": "SCMP_ACT_ERRNO",
  "architectures": ["SCMP_ARCH_X86_64", "SCMP_ARCH_X86", "SCMP_ARCH_X32"],
  "syscalls": [
    {
      "names": [
        "_llseek",
        "_newselect",
        "accept",
        …
        "write",
        "writev"
      ],
      "action": "SCMP_ACT_ALLOW"
    },
    …
  ]
}
```

We can see that the lower level container runtime ([CRI-O][crio-home] and
[runc][runc] in our case), successfully applied the default seccomp profile.
This profile denies all syscalls per default, while allowing commonly used ones
like [`accept`][accept] or [`write`][write].

[crio-home]: https://github.com/cri-o/cri-o
[runc]: https://github.com/opencontainers/runc
[accept]: https://man7.org/linux/man-pages/man2/accept.2.html
[write]: https://man7.org/linux/man-pages/man2/write.2.html

Please note that the feature will not influence any Kubernetes API for now.
Therefore, it is not possible to retrieve the used seccomp profile via `kubectl`
`get` or `describe` if the [`SeccompProfile`][api] field is unset within the
`SecurityContext`.

The feature also works when using multiple containers within a pod, for example
if we create a workload like this:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: test-pod
spec:
  containers:
    - name: test-container-nginx
      image: nginx:1.21
      securityContext:
        seccompProfile:
          type: Unconfined
    - name: test-container-redis
      image: redis:6.2
```

Then we expect that the `test-container-nginx` runs without a seccomp profile:

```bash
sudo crictl inspect $(sudo crictl ps -q --name=test-container-nginx) |
    jq '.info.runtimeSpec.linux.seccomp == null'
true
```

Whereas the container `test-container-nginx` runs with `RuntimeDefault`:

```bash
sudo crictl inspect $(sudo crictl ps -q --name=test-container-redis) |
    jq '.info.runtimeSpec.linux.seccomp != null'
true
```

The same applies to the pod itself, which also runs with the default profile:

```bash
sudo crictl inspectp (sudo crictl pods -q --name test-pod) |
    jq '.info.runtimeSpec.linux.seccomp != null'
true
```

### Upgrade strategy

It is recommended to enable the feature in multiple steps, whereas different
risks and mitigations exist for each one.

#### Feature gate enabling

Enabling the feature gate at the kubelet level will not turn on the feature, but
will make it possible by using the `SeccompDefault` kubelet configuration or the
`--seccomp-default` CLI flag. This can be done by an administrator for the whole
cluster or only a set of nodes.

#### Testing the Application

We have to ensure in a dedicated test environment that the application code does
not trigger syscalls blocked by the `RuntimeDefault` profile before enabling the
feature on a node. This can be done by:

- _Recommended_: Analyzing the code (manually or by running the application with
  [strace][strace]) for any executed syscalls which may be blocked by the
  default profiles. If that's the case, then we can create a custom seccomp
  profile based on the default by adding the additional syscalls to the
  `"action": "SCMP_ACT_ALLOW"` section.

- _Recommended_: Run the application against an end-to-end test suite to trigger
  all relevant code paths with `RuntimeDefault` enabled. If a test fails, use
  the same mitigation as mentioned above.

- _Optional_: Create a custom seccomp profile based on the default and change
  its default action from `SCMP_ACT_ERRNO` to `SCMP_ACT_LOG`. This means that
  the seccomp filter for unknown syscalls will have no effect on the application
  at all, but the system logs will now indicate which syscalls may be blocked.
  This requires at least a Kernel version 4.14 as well as a recent [runc][runc]
  release. Monitor the application hosts audit logs (defaults to
  `/var/log/audit/audit.log`) or syslog entries (defaults to `/var/log/syslog`)
  for syscalls via `type=SECCOMP` (for audit) or `type=1326` (for syslog).
  Compare the syscall ID with those [listed in the Linux Kernel
  sources][syscalls] and add them to the custom profile.

- _Optional_: Use cluster additions like the [Security Profiles Operator][spo]
  for profiling the application via its [log enrichment][logs] capabilities or
  recording a profile by using its [recording feature][rec]. This makes the
  above mentioned manual log investigation obsolete.

[syscalls]: https://github.com/torvalds/linux/blob/7bb7f2a/arch/x86/entry/syscalls/syscall_64.tbl
[spo]: https://github.com/kubernetes-sigs/security-profiles-operator
[logs]: https://github.com/kubernetes-sigs/security-profiles-operator/blob/c90ef3a/installation-usage.md#record-profiles-from-workloads-with-profilerecordings
[rec]: https://github.com/kubernetes-sigs/security-profiles-operator/blob/c90ef3a/installation-usage.md#using-the-log-enricher
[strace]: https://man7.org/linux/man-pages/man1/strace.1.html

#### Deploying the modified application

Based on the outcome of the application tests, it may be required to change the
application deployment by either specifying `Unconfined` or a custom seccomp
profile. This is not the case if the application works as intended with
`RuntimeDefault`.

#### Enable the kubelet configuration

If everything went well, then the feature is ready to be enabled by the kubelet
configuration or its corresponding CLI flag. This should be done on a per-node
basis to reduce the overall risk of missing a syscall during the investigations
when running the application tests. If it's possible to monitor audit logs
within the cluster, then it's recommended to do this for eventually missed
seccomp events. If the application works as intended then the feature can be
enabled for further nodes within the cluster.

## Conclusion

Thank you for reading this blog post! I hope you enjoyed to see how the usage of
seccomp profiles has been evolved in Kubernetes over the past releases as much
as I do. Give the `SeccompDefault` a try and feel free to reach out anytime for
feedback or questions.
