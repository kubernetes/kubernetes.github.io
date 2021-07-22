---
reviewers:
- tallclair
title: Windows Pod Security Policy
description: >
  Clarification of which pod security policies apply to Windows pods
content_type: concept
weight: 10
---

<!-- overview -->

Windows in Kubernetes has some differentiators from standard Linux-based workloads. Many of the Pod SecurityContext fields [have no effect on
Windows](/docs/setup/production-environment/windows/intro-windows-in-kubernetes/#v1-podsecuritycontext). Windows HostProcess containers also differ from traditional privileged containers, which causes some additional policies to lose their applicability for Windows.

This guide outlines the applicable _policies_ for Windows Pod Security Standards and redefines the [existing profiles](/docs/concepts/security/pod-security-standards) for the Windows context.

| Profile | Description |
| ------ | ----------- |
| <strong style="white-space: nowrap">Privileged</strong> | Unrestricted policy, providing the widest possible level of permissions. This policy allows for full access to the Windows host |
| <strong style="white-space: nowrap">Baseline</strong> | Minimally restrictive policy which prevents known privilege escalations. Allows the default (minimally specified) Pod configuration while blocking HostProcess container support. |
| <strong style="white-space: nowrap">Restricted</strong> | Unsupported until a standardized identifier for Windows pods is implemented. Windows pods _may_ be broken by the restricted field, which requires setting linux-specific settings (such as seccomp profile, run as non root, and disallow privilege escalation). If the Kubelet and/or container runtime choose to ignore these linux-specific values at runtime, then windows pods should still be allowed under the restricted profile, although the profile will not add additional enforcement over baseline (for Windows). |

<!-- body -->

## Profile Details
Each of the profiles below detail which policies must be explicitly set. Any policy **not** in the profile which is also not in the [list of policies](./#policies-ignored-on-windows) ignored by Windows can assume supported configuration on a Windows node.

### Privileged

**As is true in the default Privileged policy, the _Windows Privileged_ policy is purposely-open, and entirely unrestricted.** This type of policy is aimed at system- and infrastructure-level workloads managed by privileged, trusted users. Pods running under this policy will be limited to only HostProcess containers and will have full visibility into the Windows node.

<table>
	<caption style="display:none">Privileged policy specification</caption>
	<tbody>
		<tr>
			<td><strong>Control</strong></td>
			<td><strong>Windows Applicable</strong></td>
			<td><strong>Policy</strong></td>
		</tr>
		<tr>
			<td style="white-space: nowrap">Windows HostProcess</td>
			<td>
				<p>Windows pods offer the ability to run <a href="/docs/tasks/configure-pod-container/create-hostprocess-container">HostProcess containers</a> which enables privileged access to the Windows node. </p>
				<p><strong>Restricted Fields</strong></p>
				<ul>
					<li><code>spec.securityContext.windowsOptions.hostProcess</code></li>
					<li><code>spec.containers[*].securityContext.windowsOptions.hostProcess</code></li>
				</ul>
				<p><strong>Allowed Values</strong></p>
				<ul>
					<li><code>true</code></li>
				</ul>
			</td>
		</tr>
		<tr>
			<td style="white-space: nowrap">Host Namespaces</td>
			<td>
				<p>Will be in host network by default initially. Support to set network to a different compartment may be desirable in the future.</p>
				<p><strong>Restricted Fields</strong></p>
				<ul>
					<li><code>spec.hostNetwork</code></li>
					<li><code>spec.hostPID</code></li>
					<li><code>spec.hostIPC</code></li>
				</ul>
				<p><strong>Allowed Values</strong></p>
				<ul>
					<li><code>true</code></li>
				</ul>
			</td>
		</tr>
	</tbody>
</table>

### Baseline

**The _Baseline_ policy is aimed at ease of adoption for common containerized workloads while preventing known privilege escalations.** This policy is targeted at application operators and developers of non-critical applications. The following listed controls should be enforced/disallowed:

<table>
	<caption style="display:none">Baseline policy specification</caption>
	<tbody>
		<tr>
			<td><strong>Control</strong></td>
			<td><strong>Policy</strong></td>
		</tr>
		<tr>
			<td style="white-space: nowrap">Windows HostProcess</td>
			<td>
				<p>As is similar to  privileged containers this must be disallowed in the baseline policy. </p>
				<p><strong>Restricted Fields</strong></p>
				<ul>
					<li><code>spec.securityContext.windowsOptions.hostProcess</code></li>
					<li><code>spec.containers[*].securityContext.windowsOptions.hostProcess</code></li>
				</ul>
				<p><strong>Allowed Values</strong></p>
				<ul>
					<li>Undefined/nil</li>
					<li><code>false</code></li>
				</ul>
			</td>
		</tr>
		<tr>
			<td style="white-space: nowrap">Host Namespaces</td>
			<td>
				<p>Not applicable. Windows privileged containers will be controlled with a new `WindowsSecurityContextOptions.HostProcess` instead of the existing `privileged` field due to fundamental differences in their implementation on Windows.</p>
				<p><strong>Restricted Fields</strong></p>
				<ul>
					<li><code>spec.hostNetwork</code></li>
					<li><code>spec.hostPID</code></li>
					<li><code>spec.hostIPC</code></li>
				</ul>
				<p><strong>Allowed Values</strong></p>
				<ul>
					<li>Undefined</li>
					<li><code>false</code></li>
				</ul>
			</td>
		</tr>
	</tbody>
</table>

## Policies Ignored on Windows
Several policies in the Pod Security Standards do not apply to Windows nodes due to architectural differences between Linux and Windows. These policies are as follows:

<table>
	<caption style="display:none">Privileged policy specification</caption>
	<tbody>
		<tr>
			<td><strong>Control</strong></td>
			<td><strong>Policy</strong></td>
		</tr>
		<tr>
			<td style="white-space: nowrap">Host Namespaces</td>
			<td>
				<p>Windows does not have configurable PID/IPC namespaces (unlike Linux). Windows containers are always assigned their own process namespace. HostProcess containers always run in the host's process namespace. These behaviors are not configurable. Future plans in this area include improvements to enable scheduling pods that can contain both Windows Server and HostProcess containers. These fields would not makes in this scenario because Windows cannot configure PID/IPC namespaces like in Linux.</p>
				<p><strong>Unsupported Fields</strong></p>
				<ul>
					<li><code>spec.hostNetwork</code></li>
					<li><code>spec.hostPID</code></li>
					<li><code>spec.hostIPC</code></li>
				</ul>
			</td>
		</tr>
		<tr>
			<td style="white-space: nowrap">Privileged Containers</td>
			<td>
				<p>Not applicable. Windows privileged containers will be controlled with a new `WindowsSecurityContextOptions.HostProcess` instead of the existing `privileged` field due to fundamental differences in their implementation on Windows.</p>
				<p><strong>Unsupported Fields</strong></p>
				<ul>
					<li><code>spec.containers[*].securityContext.privileged</code></li>
					<li><code>spec.initContainers[*].securityContext.privileged</code></li>
				</ul>
			</td>
		</tr>
		<tr>
			<td style="white-space: nowrap">Capabilities</td>
			<td>
				<p>Windows OS has a concept of “capabilities” (referred to as “privileged constants” but they are not supported in the platform today.</p>
				<p><strong>Unsupported Fields</strong></p>
				<ul>
					<li><code>spec.containers[*].securityContext.capabilities.add</code></li>
					<li><code>spec.initContainers[*].securityContext.capabilities.add</code></li>
				</ul>
			</td>
		</tr>
		<tr>
			<td style="white-space: nowrap">AppArmor</td>
			<td>
				<p>AppArmor is not supported on Windows nodes.</p>
				<p><strong>Unsupported Fields</strong></p>
				<ul>
					<li><code>metadata.annotations["container.apparmor.security.beta.kubernetes.io/*"]</code></li>
				</ul>
			</td>
		</tr>
		<tr>
			<td style="white-space: nowrap">SELinux</td>
			<td>
				<p>SELinux is not supported by Windows nodes.</p>
				<p><strong>Unsupported Fields</strong></p>
				<ul>
					<li><code>spec.securityContext.seLinuxOptions.*</code></li>
					<li><code>spec.containers[*].securityContext.seLinuxOptions.*</code></li>
					<li><code>spec.initContainers[*].securityContext.seLinuxOptions.*</code></li>
				</ul>
			</td>
		</tr>
		<tr>
			<td style="white-space: nowrap"><code>/proc</code> Mount Type</td>
			<td>
				<p><code>/proc</code> masks are not supported on Windows nodes.</p>
				<p><strong>Unsupported Fields</strong></p>
				<ul>
					<li><code>spec.containers[*].securityContext.procMount</code></li>
					<li><code>spec.initContainers[*].securityContext.procMount</code></li>
				</ul>
			</td>
		</tr>
		<tr>
  			<td>Seccomp</td>
  			<td>
  				<p>Seccomp is not supported by Windows nodes.</p>
  				<p><strong>Unsupported Fields</strong></p>
				<ul>
					<li><code>spec.securityContext.seccompProfile.*</code></li>
					<li><code>spec.containers[*].securityContext.seccompProfile.*</code></li>
					<li><code>spec.initContainers[*].securityContext.seccompProfile.*</code></li>
				</ul>
  			</td>
  		</tr>
		<tr>
			<td style="white-space: nowrap">Sysctls</td>
			<td>
				<p>These are part of the Linux sysctl interface, which has no equivalent on Windows.</p>
				<p><strong>Unsupported Fields</strong></p>
				<ul>
					<li><code>spec.securityContext.sysctls</code></li>
				</ul>
			</td>
		</tr>
	</tbody>
</table>

## FAQ

