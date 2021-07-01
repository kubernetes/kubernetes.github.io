---
reviewers:
- tallclair
title: Pod Security Standards
content_type: concept
weight: 10
---

<!-- overview -->

Security settings for Pods are typically applied by using [security
contexts](/docs/tasks/configure-pod-container/security-context/). Security Contexts allow for the
definition of privilege and access controls on a per-Pod basis.

The enforcement and policy-based definition of cluster requirements of security contexts has
previously been achieved using [Pod Security Policy](/docs/concepts/policy/pod-security-policy/). A
_Pod Security Policy_ is a cluster-level resource that controls security sensitive aspects of the
Pod specification.

However, numerous means of policy enforcement have arisen that augment or replace the use of
PodSecurityPolicy. The intent of this page is to detail recommended Pod security profiles, decoupled
from any specific instantiation.



<!-- body -->

## Policy Types

There is an immediate need for base policy definitions to broadly cover the security spectrum. These
should range from highly restricted to highly flexible:

- **_Privileged_** - Unrestricted policy, providing the widest possible level of permissions. This
  policy allows for known privilege escalations.
- **_Baseline_** - Minimally restrictive policy while preventing known privilege
  escalations. Allows the default (minimally specified) Pod configuration.
- **_Restricted_** - Heavily restricted policy, following current Pod hardening best practices.

## Policies

### Privileged

The Privileged policy is purposely-open, and entirely unrestricted. This type of policy is typically
aimed at system- and infrastructure-level workloads managed by privileged, trusted users.

The privileged policy is defined by an absence of restrictions. For allow-by-default enforcement
mechanisms (such as gatekeeper), the privileged profile may be an absence of applied constraints
rather than an instantiated policy. In contrast, for a deny-by-default mechanism (such as Pod
Security Policy) the privileged policy should enable all controls (disable all restrictions).

### Baseline

The Baseline policy is aimed at ease of adoption for common containerized workloads while
preventing known privilege escalations. This policy is targeted at application operators and
developers of non-critical applications. The following listed controls should be
enforced/disallowed:

<table>
	<caption style="display:none">Baseline policy specification</caption>
	<tbody>
		<tr>
			<td><strong>Control</strong></td>
			<td><strong>Policy</strong></td>
		</tr>
		<tr>
			<td>Host Namespaces</td>
			<td>
				Sharing the host namespaces must be disallowed.<br>
				<br><b>Restricted Fields:</b><br>
				spec.hostNetwork<br>
				spec.hostPID<br>
				spec.hostIPC<br>
				<br><b>Allowed Values:</b> false<br>
			</td>
		</tr>
		<tr>
			<td>Privileged Containers</td>
			<td>
				Privileged Pods disable most security mechanisms and must be disallowed.<br>
				<br><b>Restricted Fields:</b><br>
				spec.containers[*].securityContext.privileged<br>
				spec.initContainers[*].securityContext.privileged<br>
				<br><b>Allowed Values:</b> false, undefined/nil<br>
			</td>
		</tr>
		<tr>
			<td>Capabilities</td>
			<td>
				Adding additional capabilities beyond the <a href="https://docs.docker.com/engine/reference/run/#runtime-privilege-and-linux-capabilities">default set</a> must be disallowed.<br>
				<br><b>Restricted Fields:</b><br>
				spec.containers[*].securityContext.capabilities.add<br>
				spec.initContainers[*].securityContext.capabilities.add<br>
				<br><b>Allowed Values:</b> empty (or restricted to a known list)<br>
			</td>
		</tr>
		<tr>
			<td>HostPath Volumes</td>
			<td>
				HostPath volumes must be forbidden.<br>
				<br><b>Restricted Fields:</b><br>
				spec.volumes[*].hostPath<br>
				<br><b>Allowed Values:</b> undefined/nil<br>
			</td>
		</tr>
		<tr>
			<td>Host Ports</td>
			<td>
				HostPorts should be disallowed, or at minimum restricted to a known list.<br>
				<br><b>Restricted Fields:</b><br>
				spec.containers[*].ports[*].hostPort<br>
				spec.initContainers[*].ports[*].hostPort<br>
				<br><b>Allowed Values:</b> 0, undefined (or restricted to a known list)<br>
			</td>
		</tr>
		<tr>
			<td>AppArmor</td>
			<td>
				On supported hosts, the 'runtime/default' AppArmor profile is applied by default.
				The baseline policy should prevent overriding or disabling the default AppArmor
				profile, or restrict overrides to an allowed set of profiles.<br>
				<br><b>Restricted Fields:</b><br>
				metadata.annotations['container.apparmor.security.beta.kubernetes.io/*']<br>
				<br><b>Allowed Values:</b> 'runtime/default', undefined<br>
			</td>
		</tr>
		<tr>
			<td>SELinux</td>
			<td>
				Setting the SELinux type is restricted, and setting a custom SELinux user or role option is forbidden.<br>
				<br><b>Restricted Fields:</b><br>
				spec.securityContext.seLinuxOptions.type<br>
				spec.containers[*].securityContext.seLinuxOptions.type<br>
				spec.initContainers[*].securityContext.seLinuxOptions.type<br>
				<br><b>Allowed Values:</b><br>
				undefined/empty<br>
				container_t<br>
				container_init_t<br>
				container_kvm_t<br>
				<br><b>Restricted Fields:</b><br>
				spec.securityContext.seLinuxOptions.user<br>
				spec.containers[*].securityContext.seLinuxOptions.user<br>
				spec.initContainers[*].securityContext.seLinuxOptions.user<br>
				spec.securityContext.seLinuxOptions.role<br>
				spec.containers[*].securityContext.seLinuxOptions.role<br>
				spec.initContainers[*].securityContext.seLinuxOptions.role<br>
				<br><b>Allowed Values:</b> undefined/empty<br>
			</td>
		</tr>
		<tr>
			<td>/proc Mount Type</td>
			<td>
				The default /proc masks are set up to reduce attack surface, and should be required.<br>
				<br><b>Restricted Fields:</b><br>
				spec.containers[*].securityContext.procMount<br>
				spec.initContainers[*].securityContext.procMount<br>
				<br><b>Allowed Values:</b> undefined/nil, 'Default'<br>
			</td>
		</tr>
		<tr>
			<td>Sysctls</td>
			<td>
				Sysctls can disable security mechanisms or affect all containers on a host, and should be disallowed except for an allowed "safe" subset.
				A sysctl is considered safe if it is namespaced in the container or the Pod, and it is isolated from other Pods or processes on the same Node.<br>
				<br><b>Restricted Fields:</b><br>
				spec.securityContext.sysctls<br>
				<br><b>Allowed Values:</b><br>
				kernel.shm_rmid_forced<br>
				net.ipv4.ip_local_port_range<br>
				net.ipv4.tcp_syncookies<br>
				net.ipv4.ping_group_range<br>
				undefined/empty<br>
			</td>
		</tr>
	</tbody>
</table>

### Restricted

The Restricted policy is aimed at enforcing current Pod hardening best practices, at the expense of
some compatibility. It is targeted at operators and developers of security-critical applications, as
well as lower-trust users.The following listed controls should be enforced/disallowed:


<table>
	<caption style="display:none">Restricted policy specification</caption>
	<tbody>
		<tr>
			<td><strong>Control</strong></td>
			<td><strong>Policy</strong></td>
		</tr>
		<tr>
			<td colspan="2"><em>Everything from the baseline profile.</em></td>
		</tr>
		<tr>
			<td>Volume Types</td>
			<td>
				In addition to restricting HostPath volumes, the restricted profile limits usage of non-core volume types to those defined through PersistentVolumes.<br>
				<br><b>Restricted Fields:</b><br>
				spec.volumes[*].hostPath<br>
				spec.volumes[*].gcePersistentDisk<br>
				spec.volumes[*].awsElasticBlockStore<br>
				spec.volumes[*].gitRepo<br>
				spec.volumes[*].nfs<br>
				spec.volumes[*].iscsi<br>
				spec.volumes[*].glusterfs<br>
				spec.volumes[*].rbd<br>
				spec.volumes[*].flexVolume<br>
				spec.volumes[*].cinder<br>
				spec.volumes[*].cephFS<br>
				spec.volumes[*].flocker<br>
				spec.volumes[*].fc<br>
				spec.volumes[*].azureFile<br>
				spec.volumes[*].vsphereVolume<br>
				spec.volumes[*].quobyte<br>
				spec.volumes[*].azureDisk<br>
				spec.volumes[*].portworxVolume<br>
				spec.volumes[*].scaleIO<br>
				spec.volumes[*].storageos<br>
				spec.volumes[*].csi<br>
				<br><b>Allowed Values:</b> undefined/nil<br>
			</td>
		</tr>
		<tr>
			<td>Privilege Escalation</td>
			<td>
				Privilege escalation (such as via set-user-ID or set-group-ID file mode) should not be allowed.<br>
				<br><b>Restricted Fields:</b><br>
				spec.containers[*].securityContext.allowPrivilegeEscalation<br>
				spec.initContainers[*].securityContext.allowPrivilegeEscalation<br>
				<br><b>Allowed Values:</b> false<br>
			</td>
		</tr>
		<tr>
			<td>Running as Non-root</td>
			<td>
				Containers must be required to run as non-root users.<br>
				<br><b>Restricted Fields:</b><br>
				spec.securityContext.runAsNonRoot<br>
				spec.containers[*].securityContext.runAsNonRoot<br>
				spec.initContainers[*].securityContext.runAsNonRoot<br>
				<br><b>Allowed Values:</b> true<br>
			</td>
		</tr>
		<tr>
			<td>Non-root groups <em>(optional)</em></td>
			<td>
				Containers should be forbidden from running with a root primary or supplementary GID.<br>
				<br><b>Restricted Fields:</b><br>
				spec.securityContext.runAsGroup<br>
				spec.securityContext.supplementalGroups[*]<br>
				spec.securityContext.fsGroup<br>
				spec.containers[*].securityContext.runAsGroup<br>
				spec.initContainers[*].securityContext.runAsGroup<br>
				<br><b>Allowed Values:</b><br>
				non-zero<br>
				undefined / nil (except for `*.runAsGroup`)<br>
			</td>
		</tr>
		<tr>
			<td>Seccomp</td>
			<td>
				The RuntimeDefault seccomp profile must be required, or allow specific additional profiles.<br>
				<br><b>Restricted Fields:</b><br>
				spec.securityContext.seccompProfile.type<br>
				spec.containers[*].securityContext.seccompProfile<br>
				spec.initContainers[*].securityContext.seccompProfile<br>
				<br><b>Allowed Values:</b><br>
				'runtime/default'<br>
				undefined / nil<br>
			</td>
		</tr>
	</tbody>
</table>

## Policy Instantiation

Decoupling policy definition from policy instantiation allows for a common understanding and
consistent language of policies across clusters, independent of the underlying enforcement
mechanism.

As mechanisms mature, they will be defined below on a per-policy basis. The methods of enforcement
of individual policies are not defined here.

[**PodSecurityPolicy**](/docs/concepts/policy/pod-security-policy/)

- {{< example file="policy/privileged-psp.yaml" >}}Privileged{{< /example >}}
- {{< example file="policy/baseline-psp.yaml" >}}Baseline{{< /example >}}
- {{< example file="policy/restricted-psp.yaml" >}}Restricted{{< /example >}}

## FAQ

### Why isn't there a profile between privileged and baseline?

The three profiles defined here have a clear linear progression from most secure (restricted) to least
secure (privileged), and cover a broad set of workloads. Privileges required above the baseline
policy are typically very application specific, so we do not offer a standard profile in this
niche. This is not to say that the privileged profile should always be used in this case, but that
policies in this space need to be defined on a case-by-case basis.

SIG Auth may reconsider this position in the future, should a clear need for other profiles arise.

### What's the difference between a security policy and a security context?

[Security Contexts](/docs/tasks/configure-pod-container/security-context/) configure Pods and
Containers at runtime. Security contexts are defined as part of the Pod and container specifications
in the Pod manifest, and represent parameters to the container runtime.

Security policies are control plane mechanisms to enforce specific settings in the Security Context,
as well as other parameters outside the Security Context. As of February 2020, the current native
solution for enforcing these security policies is [Pod Security
Policy](/docs/concepts/policy/pod-security-policy/) - a mechanism for centrally enforcing security
policy on Pods across a cluster. Other alternatives for enforcing security policy are being
developed in the Kubernetes ecosystem, such as [OPA
Gatekeeper](https://github.com/open-policy-agent/gatekeeper).

### What profiles should I apply to my Windows Pods?

Windows in Kubernetes has some limitations and differentiators from standard Linux-based
workloads. Specifically, the Pod SecurityContext fields [have no effect on
Windows](/docs/setup/production-environment/windows/intro-windows-in-kubernetes/#v1-podsecuritycontext). As
such, no standardized Pod Security profiles currently exists.

### What about sandboxed Pods?

There is not currently an API standard that controls whether a Pod is considered sandboxed or
not. Sandbox Pods may be identified by the use of a sandboxed runtime (such as gVisor or Kata
Containers), but there is no standard definition of what a sandboxed runtime is.

The protections necessary for sandboxed workloads can differ from others. For example, the need to
restrict privileged permissions is lessened when the workload is isolated from the underlying
kernel. This allows for workloads requiring heightened permissions to still be isolated.

Additionally, the protection of sandboxed workloads is highly dependent on the method of
sandboxing. As such, no single recommended policy is recommended for all sandboxed workloads.


