---
reviewers:
- tallclair
title: Pod Security Standards
description: >
  A detailed look at the different policy levels defined in the Pod Security Standards.
content_type: concept
weight: 10
---

<!-- overview -->

The Pod Security Standards define three different _policies_ to broadly cover the security spectrum. These policies are _cumulative_ and range from highly-permissive to highly-restrictive. This guide outlines the requirements of each policy.

| Profile | Description |
| ------ | ----------- |
| <strong style="white-space: nowrap">Privileged</strong> | Unrestricted policy, providing the widest possible level of permissions. This policy allows for known privilege escalations. |
| <strong style="white-space: nowrap">Baseline</strong> | Minimally restrictive policy which prevents known privilege escalations. Allows the default (minimally specified) Pod configuration. |
| <strong style="white-space: nowrap">Restricted</strong> | Heavily restricted policy, following current Pod hardening best practices. |

<!-- body -->

## Profile Details

### Privileged

**The _Privileged_ policy is purposely-open, and entirely unrestricted.** This type of policy is typically aimed at system- and infrastructure-level workloads managed by privileged, trusted users.

The Privileged policy is defined by an absence of restrictions. For allow-by-default enforcement mechanisms (such as gatekeeper), the Privileged policy may be an absence of applied constraints rather than an instantiated profile. In contrast, for a deny-by-default mechanism (such as Pod Security Policy) the Privileged policy should enable all controls (disable all restrictions).

### Baseline

**The _Baseline_ policy is aimed at ease of adoption for common containerized workloads while preventing known privilege escalations.** This policy is targeted at application operators and developers of non-critical applications. The following listed controls should be enforced/disallowed:

{{< note >}}
In this table, wildcards (`*`) incidate all elements in a list. For example, `spec.containers[*].securityContext` refers to the Security Context object for _all defined containers_. If any of the listed containers fails to meet the requirements, the entire pod will fail validation.
{{< /note >}}

<table>
	<caption style="display:none">Baseline policy specification</caption>
	<tbody>
		<tr>
			<td><strong>Control</strong></td>
			<td><strong>Policy</strong></td>
		</tr>
		<tr>
			<td style="white-space: nowrap">Host Namespaces</td>
			<td>
				<p>Sharing the host namespaces must be disallowed.</p>
				<p><strong>Restricted Fields</strong></p>
				<ul>
					<li><code>spec.hostNetwork</code></li>
					<li><code>spec.hostPID</code></li>
					<li><code>spec.hostIPC</code></li>
				</ul>
				<p><strong>Allowed Values</strong></p>
				<ul>
					<li><code>false</code></li>
				</ul>
			</td>
		</tr>
		<tr>
			<td style="white-space: nowrap">Privileged Containers</td>
			<td>
				<p>Privileged Pods disable most security mechanisms and must be disallowed.</p>
				<p><strong>Restricted Fields</strong></p>
				<ul>
					<li><code>spec.containers[*].securityContext.privileged</code></li>
					<li><code>spec.initContainers[*].securityContext.privileged</code></li>
				</ul>
				<p><strong>Allowed Values</strong></p>
				<ul>
					<li>Undefined/nil</li>
					<li><code>false</code></li>
				</ul>
			</td>
		</tr>
		<tr>
			<td style="white-space: nowrap">Capabilities</td>
			<td>
				<p>Adding additional capabilities beyond the <a href="https://docs.docker.com/engine/reference/run/#runtime-privilege-and-linux-capabilities">default set</a> must be disallowed.</p>
				<p><strong>Restricted Fields</strong></p>
				<ul>
					<li><code>spec.containers[*].securityContext.capabilities.add</code></li>
					<li><code>spec.initContainers[*].securityContext.capabilities.add</code></li>
				</ul>
				<p><strong>Allowed Values</strong></p>
				<ul>
					<li>Undefined/nil</li>
					<li><code>AUDIT_WRITE</code></li>
					<li><code>CHOWN</code></li>
					<li><code>DAC_OVERRIDE</code></li>
					<li><code>FOWNER</code></li>
					<li><code>FSETID</code></li>
					<li><code>KILL</code></li>
					<li><code>MKNOD</code></li>
					<li><code>NET_BIND_SERVICE</code></li>
					<li><code>SETFCAP</code></li>
					<li><code>SETGID</code></li>
					<li><code>SETPCAP</code></li>
					<li><code>SETUID</code></li>
					<li><code>SYS_CHROOT</code></li>
				</ul>
			</td>
		</tr>
		<tr>
			<td style="white-space: nowrap">HostPath Volumes</td>
			<td>
				<p>HostPath volumes must be forbidden.</p>
				<p><strong>Restricted Fields</strong></p>
				<ul>
					<li><code>spec.volumes[*].hostPath</code></li>
				</ul>
				<p><strong>Allowed Values</strong></p>
				<ul>
					<li>Undefined/nil</li>
				</ul>
			</td>
		</tr>
		<tr>
			<td style="white-space: nowrap">Host Ports</td>
			<td>
				<p>HostPorts should be disallowed, or at minimum restricted to a known list.</p>
				<p><strong>Restricted Fields</strong></p>
				<ul>
					<li><code>spec.containers[*].ports[*].hostPort</code></li>
					<li><code>spec.initContainers[*].ports[*].hostPort</code></li>
				</ul>
				<p><strong>Allowed Values</strong></p>
				<ul>
					<li>Undefined/nil</li>
					<li>Known list</li>
					<li><code>0</code></li>
				</ul>
			</td>
		</tr>
		<tr>
			<td style="white-space: nowrap">AppArmor</td>
			<td>
				<p>On supported hosts, the <code>runtime/default</code> AppArmor profile is applied by default. The baseline policy should prevent overriding or disabling the default AppArmor profile, or restrict overrides to an allowed set of profiles.</p>
				<p><strong>Restricted Fields</strong></p>
				<ul>
					<li><code>metadata.annotations["container.apparmor.security.beta.kubernetes.io/*"]</code></li>
				</ul>
				<p><strong>Allowed Values</strong></p>
				<ul>
					<li>Undefined/nil</li>
					<li><code>runtime/default</code></li>
				</ul>
			</td>
		</tr>
		<tr>
			<td style="white-space: nowrap">SELinux</td>
			<td>
				<p>Setting the SELinux type is restricted, and setting a custom SELinux user or role option is forbidden.</p>
				<p><strong>Restricted Fields</strong></p>
				<ul>
					<li><code>spec.securityContext.seLinuxOptions.type</code></li>
					<li><code>spec.containers[*].securityContext.seLinuxOptions.type</code></li>
					<li><code>spec.initContainers[*].securityContext.seLinuxOptions.type</code></li>
				</ul>
				<p><strong>Allowed Values</strong></p>
				<ul>
					<li>Undefined/nil</li>
					<li><code>container_t</code></li>
					<li><code>container_init_t</code></li>
					<li><code>container_kvm_t</code></li>
				</ul>
				<hr />
				<p><strong>Restricted Fields</strong></p>
				<ul>
					<li><code>spec.securityContext.seLinuxOptions.user</code></li>
					<li><code>spec.containers[*].securityContext.seLinuxOptions.user</code></li>
					<li><code>spec.initContainers[*].securityContext.seLinuxOptions.user</code></li>
					<li><code>spec.securityContext.seLinuxOptions.role</code></li>
					<li><code>spec.containers[*].securityContext.seLinuxOptions.role</code></li>
					<li><code>spec.initContainers[*].securityContext.seLinuxOptions.role</code></li>
				</ul>
				<p><strong>Allowed Values</strong></p>
				<ul>
					<li>Undefined/nil</li>
				</ul>
			</td>
		</tr>
		<tr>
			<td style="white-space: nowrap"><code>/proc</code> Mount Type</td>
			<td>
				<p>The default <code>/proc</code> masks are set up to reduce attack surface, and should be required.</p>
				<p><strong>Restricted Fields</strong></p>
				<ul>
					<li><code>spec.containers[*].securityContext.procMount</code></li>
					<li><code>spec.initContainers[*].securityContext.procMount</code></li>
				</ul>
				<p><strong>Allowed Values</strong></p>
				<ul>
					<li>Undefined/nil</li>
					<li><code>Default</code></li>
				</ul>
			</td>
		</tr>
		<tr>
  			<td>Seccomp</td>
  			<td>
  				<p>Seccomp profile must not be explicitly set to <code>Unconfined</code>.</p>
  				<p><strong>Restricted Fields</strong></p>
				<ul>
					<li><code>spec.securityContext.seccompProfile.type</code></li>
					<li><code>spec.containers[*].securityContext.seccompProfile.type</code></li>
					<li><code>spec.initContainers[*].securityContext.seccompProfile.type</code></li>
				</ul>
				<p><strong>Allowed Values</strong></p>
				<ul>
					<li>Undefined/nil</li>
					<li><code>RuntimeDefault</code></li>
					<li><code>Localhost</code>*</li>
				</ul>
  				<small>* must also set <code>securityContext.SeccompProfile.localhostProfile</code></small>
  			</td>
  		</tr>
		<tr>
			<td style="white-space: nowrap">Sysctls</td>
			<td>
				<p>Sysctls can disable security mechanisms or affect all containers on a host, and should be disallowed except for an allowed "safe" subset. A sysctl is considered safe if it is namespaced in the container or the Pod, and it is isolated from other Pods or processes on the same Node.</p>
				<p><strong>Restricted Fields</strong></p>
				<ul>
					<li><code>spec.securityContext.sysctls</code></li>
				</ul>
				<p><strong>Allowed Values</strong></p>
				<ul>
					<li>Undefined/nil</li>
					<li><code>kernel.shm_rmid_forced</code></li>
					<li><code>net.ipv4.ip_local_port_range</code></li>
					<li><code>net.ipv4.ip_unprivileged_port_start</code></li>
					<li><code>net.ipv4.tcp_syncookies</code></li>
					<li><code>net.ipv4.ping_group_range</code></li>
				</ul>
			</td>
		</tr>
	</tbody>
</table>

### Restricted

**The _Restricted_ policy is aimed at enforcing current Pod hardening best practices, at the expense ofsome compatibility.** It is targeted at operators and developers of security-critical applications, as well as lower-trust users. The following listed controls should be enforced/disallowed:

{{< note >}}
In this table, wildcards (`*`) incidate all elements in a list. For example, `spec.containers[*].securityContext` refers to the Security Context object for _all defined containers_. If any of the listed containers fails to meet the requirements, the entire pod will fail validation.
{{< /note >}}

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
			<td style="white-space: nowrap">Volume Types</td>
			<td>
				<p>In addition to restricting HostPath volumes, the restricted policy limits usage of non-core volume types to those defined through PersistentVolumes.</p>
				<p><strong>Restricted Fields</strong></p>
				<ul>
					<li><code>spec.volumes[*].hostPath</code></li>
					<li><code>spec.volumes[*].gcePersistentDisk</code></li>
					<li><code>spec.volumes[*].awsElasticBlockStore</code></li>
					<li><code>spec.volumes[*].gitRepo</code></li>
					<li><code>spec.volumes[*].nfs</code></li>
					<li><code>spec.volumes[*].iscsi</code></li>
					<li><code>spec.volumes[*].glusterfs</code></li>
					<li><code>spec.volumes[*].rbd</code></li>
					<li><code>spec.volumes[*].flexVolume</code></li>
					<li><code>spec.volumes[*].cinder</code></li>
					<li><code>spec.volumes[*].cephfs</code></li>
					<li><code>spec.volumes[*].flocker</code></li>
					<li><code>spec.volumes[*].fc</code></li>
					<li><code>spec.volumes[*].azureFile</code></li>
					<li><code>spec.volumes[*].vsphereVolume</code></li>
					<li><code>spec.volumes[*].quobyte</code></li>
					<li><code>spec.volumes[*].azureDisk</code></li>
					<li><code>spec.volumes[*].portworxVolume</code></li>
					<li><code>spec.volumes[*].scaleIO</code></li>
					<li><code>spec.volumes[*].storageos</code></li>
					<li><code>spec.volumes[*].csi</code></li>
				</ul>
				<p><strong>Allowed Values</strong></p>
				<ul>
					<li>Undefined/nil</li>
				</ul>
			</td>
		</tr>
		<tr>
			<td style="white-space: nowrap">Privilege Escalation</td>
			<td>
				<p>Privilege escalation (such as via set-user-ID or set-group-ID file mode) should not be allowed.</p>
				<p><strong>Restricted Fields</strong></p>
				<ul>
					<li><code>spec.containers[*].securityContext.allowPrivilegeEscalation</code></li>
					<li><code>spec.initContainers[*].securityContext.allowPrivilegeEscalation</code></li>
				</ul>
				<p><strong>Allowed Values</strong></p>
				<ul>
					<li><code>false</code></li>
				</ul>
			</td>
		</tr>
		<tr>
			<td style="white-space: nowrap">Running as Non-root</td>
			<td>
				<p>Containers must be required to run as non-root users.</p>
				<p><strong>Restricted Fields</strong></p>
				<ul>
					<li><code>spec.securityContext.runAsNonRoot</code></li>
					<li><code>spec.containers[*].securityContext.runAsNonRoot</code></li>
					<li><code>spec.initContainers[*].securityContext.runAsNonRoot</code></li>
				</ul>
				<p><strong>Allowed Values</strong></p>
				<ul>
					<li><code>true</code></li>
				</ul>
			</td>
		</tr>
		<tr>
			<td style="white-space: nowrap">Non-root groups <em>(optional)</em></td>
			<td>
				<p>Containers should be forbidden from running with a root primary or supplementary GID.</p>
				<p><strong>Restricted Fields</strong></p>
				<ul>
					<li><code>spec.securityContext.runAsGroup</code></li>
					<li><code>spec.securityContext.supplementalGroups[*]</code></li>
					<li><code>spec.securityContext.fsGroup</code></li>
					<li><code>spec.containers[*].securityContext.runAsGroup</code></li>
					<li><code>spec.initContainers[*].securityContext.runAsGroup</code></li>
				</ul>
				<p><strong>Allowed Values</strong></p>
				<ul>
					<li>Undefined/nil (except for <code>*.runAsGroup</code>)</li>
					<li>Non-zero</li>
				</ul>
			</td>
		</tr>
		<tr>
  			<td>Seccomp</td>
  			<td>
  				<p>Seccomp profile must be explicitly set to one of the allowed values. Both the <code>Unconfined</code> profile and the <em>absence</em> of a profile are prohibited.</p>
  				<p><strong>Restricted Fields</strong></p>
				<ul>
					<li><code>spec.securityContext.seccompProfile.type</code></li>
					<li><code>spec.containers[*].securityContext.seccompProfile.type</code></li>
					<li><code>spec.initContainers[*].securityContext.seccompProfile.type</code></li>
				</ul>
				<p><strong>Allowed Values</strong></p>
				<ul>
					<li><code>RuntimeDefault</code></li>
					<li><code>Localhost</code>*</li>
				</ul>
  				<small>* must also set <code>securityContext.SeccompProfile.localhostProfile</code></small>
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

[**PodSecurityPolicy**](/docs/concepts/profile/pod-security-profile/)

- {{< example file="profile/privileged-psp.yaml" >}}Privileged{{< /example >}}
- {{< example file="profile/baseline-psp.yaml" >}}Baseline{{< /example >}}
- {{< example file="profile/restricted-psp.yaml" >}}Restricted{{< /example >}}

## FAQ

### Why isn't there a policy between privileged and baseline?

The three profiles defined here have a clear linear progression from most secure (restricted) to least
secure (privileged), and cover a broad set of workloads. Privileges required above the baseline
policy are typically very application specific, so we do not offer a standard policy in this
niche. This is not to say that the privileged policy should always be used in this case, but that
policies in this space need to be defined on a case-by-case basis.

SIG Auth may reconsider this position in the future, should a clear need for other profiles arise.

### What's the difference between a security policy and a security context?

[Security Contexts](/docs/tasks/configure-pod-container/security-context/) configure Pods and
Containers at runtime. Security contexts are defined as part of the Pod and container specifications
in the Pod manifest, and represent parameters to the container runtime.

Security policies are control plane mechanisms to enforce specific settings in the Security Context,
as well as other parameters outside the Security Context. As of February 2020, the current native
solution for enforcing these security policies is [Pod Security
Policy](/docs/concepts/profile/pod-security-profile/) - a mechanism for centrally enforcing security
profile on Pods across a cluster. Other alternatives for enforcing security profile are being
developed in the Kubernetes ecosystem, such as [OPA
Gatekeeper](https://github.com/open-profile-agent/gatekeeper).

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
sandboxing. As such, no single recommended profile is recommended for all sandboxed workloads.


