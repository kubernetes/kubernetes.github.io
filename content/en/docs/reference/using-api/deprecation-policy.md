---
reviewers:
- bgrant0607
- lavalamp
- thockin
title: Kubernetes Deprecation Policy
content_type: concept
weight: 40
---

<!-- overview -->
This document details the deprecation policy for various facets of the system.


<!-- body -->
Kubernetes is a large system with many components and many contributors.  As
with any such software, the feature set naturally evolves over time, and
sometimes a feature may need to be removed. This could include an API, a flag,
or even an entire feature. To avoid breaking existing users, Kubernetes follows
a deprecation policy for aspects of the system that are slated to be removed.

## Deprecating parts of the API

Since Kubernetes is an API-driven system, the API has evolved over time to
reflect the evolving understanding of the problem space. The Kubernetes API is
actually a set of APIs, called "API groups", and each API group is
independently versioned.  [API versions](/docs/reference/using-api/#api-versioning) fall
into 3 main tracks, each of which has different policies for deprecation:

| Example  | Track                            |
|----------|----------------------------------|
| v1       | GA (generally available, stable) |
| v1beta1  | Beta (pre-release)               |
| v1alpha1 | Alpha (experimental)             |

A given release of Kubernetes can support any number of API groups and any
number of versions of each.

The following rules govern the deprecation of elements of the API.  This
includes:

   * REST resources (aka API objects)
   * Fields of REST resources
   * Annotations on REST resources, including "beta" annotations but not
     including "alpha" annotations.
   * Enumerated or constant values
   * Component config structures

These rules are enforced between official releases, not between
arbitrary commits to master or release branches.

**Rule #1: API elements may only be removed by incrementing the version of the
API group.**

Once an API element has been added to an API group at a particular version, it
can not be removed from that version or have its behavior significantly
changed, regardless of track.

{{< note >}}
For historical reasons, there are 2 "monolithic" API groups - "core" (no
group name) and "extensions".  Resources will incrementally be moved from these
legacy API groups into more domain-specific API groups.
{{< /note >}}

**Rule #2: API objects must be able to round-trip between API versions in a given
release without information loss, with the exception of whole REST resources
that do not exist in some versions.**

For example, an object can be written as v1 and then read back as v2 and
converted to v1, and the resulting v1 resource will be identical to the
original.  The representation in v2 might be different from v1, but the system
knows how to convert between them in both directions.  Additionally, any new
field added in v2 must be able to round-trip to v1 and back, which means v1
might have to add an equivalent field or represent it as an annotation.

**Rule #3: An API version in a given track may not be deprecated until a new
API version at least as stable is released.**

GA API versions can replace GA API versions as well as beta and alpha API
versions.  Beta API versions *may not* replace GA API versions.

**Rule #4a: Other than the most recent API versions in each track, older API
versions must be supported after their announced deprecation for a duration of
no less than:**

   * **GA: 12 months or 3 releases (whichever is longer)**
   * **Beta: 9 months or 3 releases (whichever is longer)**
   * **Alpha: 0 releases**

This covers the [maximum supported version skew of 2 releases](/docs/setup/release/version-skew-policy/).

{{< note >}}
Until [#52185](https://github.com/kubernetes/kubernetes/issues/52185) is
resolved, no API versions that have been persisted to storage may be removed.
Serving REST endpoints for those versions may be disabled (subject to the
deprecation timelines in this document), but the API server must remain capable
of decoding/converting previously persisted data from storage.
{{< /note >}}

**Rule #4b: The "preferred" API version and the "storage version" for a given
group may not advance until after a release has been made that supports both the
new version and the previous version**

Users must be able to upgrade to a new release of Kubernetes and then roll back
to a previous release, without converting anything to the new API version or
suffering breakages (unless they explicitly used features only available in the
newer version).  This is particularly evident in the stored representation of
objects.

All of this is best illustrated by examples.  Imagine a Kubernetes release,
version X, which introduces a new API group.  A new Kubernetes release is made
every approximately 3 months (4 per year).  The following table describes which
API versions are supported in a series of subsequent releases.

<table>
  <thead>
    <tr>
      <th>Release</th>
      <th>API Versions</th>
      <th>Preferred/Storage Version</th>
      <th>Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>X</td>
      <td>v1alpha1</td>
      <td>v1alpha1</td>
      <td></td>
    </tr>
    <tr>
      <td>X+1</td>
      <td>v1alpha2</td>
      <td>v1alpha2</td>
      <td>
        <ul>
           <li>v1alpha1 is removed, "action required" relnote</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td>X+2</td>
      <td>v1beta1</td>
      <td>v1beta1</td>
      <td>
        <ul>
          <li>v1alpha2 is removed, "action required" relnote</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td>X+3</td>
      <td>v1beta2, v1beta1 (deprecated)</td>
      <td>v1beta1</td>
      <td>
        <ul>
          <li>v1beta1 is deprecated, "action required" relnote</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td>X+4</td>
      <td>v1beta2, v1beta1 (deprecated)</td>
      <td>v1beta2</td>
      <td></td>
    </tr>
    <tr>
      <td>X+5</td>
      <td>v1, v1beta1 (deprecated), v1beta2 (deprecated)</td>
      <td>v1beta2</td>
      <td>
        <ul>
          <li>v1beta2 is deprecated, "action required" relnote</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td>X+6</td>
      <td>v1, v1beta2 (deprecated)</td>
      <td>v1</td>
      <td>
        <ul>
          <li>v1beta1 is removed, "action required" relnote</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td>X+7</td>
      <td>v1, v1beta2 (deprecated)</td>
      <td>v1</td>
      <td></td>
    </tr>
    <tr>
      <td>X+8</td>
      <td>v2alpha1, v1</td>
      <td>v1</td>
      <td>
        <ul>
          <li>v1beta2 is removed, "action required" relnote</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td>X+9</td>
      <td>v2alpha2, v1</td>
      <td>v1</td>
      <td>
        <ul>
           <li>v2alpha1 is removed, "action required" relnote</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td>X+10</td>
      <td>v2beta1, v1</td>
      <td>v1</td>
      <td>
        <ul>
          <li>v2alpha2 is removed, "action required" relnote</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td>X+11</td>
      <td>v2beta2, v2beta1 (deprecated), v1</td>
      <td>v1</td>
      <td>
        <ul>
          <li>v2beta1 is deprecated, "action required" relnote</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td>X+12</td>
      <td>v2, v2beta2 (deprecated), v2beta1 (deprecated), v1 (deprecated)</td>
      <td>v1</td>
      <td>
        <ul>
          <li>v2beta2 is deprecated, "action required" relnote</li>
          <li>v1 is deprecated, "action required" relnote</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td>X+13</td>
      <td>v2, v2beta1 (deprecated), v2beta2 (deprecated), v1 (deprecated)</td>
      <td>v2</td>
      <td></td>
    </tr>
    <tr>
      <td>X+14</td>
      <td>v2, v2beta2 (deprecated), v1 (deprecated)</td>
      <td>v2</td>
      <td>
        <ul>
          <li>v2beta1 is removed, "action required" relnote</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td>X+15</td>
      <td>v2, v1 (deprecated)</td>
      <td>v2</td>
      <td>
        <ul>
          <li>v2beta2 is removed, "action required" relnote</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td>X+16</td>
      <td>v2, v1 (deprecated)</td>
      <td>v2</td>
      <td></td>
    </tr>
    <tr>
      <td>X+17</td>
      <td>v2</td>
      <td>v2</td>
      <td>
        <ul>
          <li>v1 is removed, "action required" relnote</li>
        </ul>
      </td>
    </tr>
  </tbody>
</table>

### REST resources (aka API objects)

Consider a hypothetical REST resource named Widget, which was present in API v1
in the above timeline, and which needs to be deprecated.  We document and
[announce](https://groups.google.com/forum/#!forum/kubernetes-announce) the
deprecation in sync with release X+1.  The Widget resource still exists in API
version v1 (deprecated) but not in v2alpha1.  The Widget resource continues to
exist and function in releases up to and including X+8.  Only in release X+9,
when API v1 has aged out, does the Widget resource cease to exist, and the
behavior get removed.

Starting in Kubernetes v1.19, making an API request to a deprecated REST API endpoint:

1. Returns a `Warning` header (as defined in [RFC7234, Section 5.5](https://tools.ietf.org/html/rfc7234#section-5.5)) in the API response.
2. Adds a `"k8s.io/deprecated":"true"` annotation to the [audit event](/docs/tasks/debug-application-cluster/audit/) recorded for the request.
3. Sets an `apiserver_requested_deprecated_apis` gauge metric to `1` in the `kube-apiserver`
   process. The metric has labels for `group`, `version`, `resource`, `subresource` that can be joined
   to the `apiserver_request_total` metric, and a `removed_release` label that indicates the
   Kubernetes release in which the API will no longer be served. The following Prometheus query
   returns information about requests made to deprecated APIs which will be removed in v1.22:

   ```promql
   apiserver_requested_deprecated_apis{removed_release="1.22"} * on(group,version,resource,subresource) group_right() apiserver_request_total
   ```

### Fields of REST resources

As with whole REST resources, an individual field which was present in API v1
must exist and function until API v1 is removed.  Unlike whole resources, the
v2 APIs may choose a different representation for the field, as long as it can
be round-tripped.  For example a v1 field named "magnitude" which was
deprecated might be named "deprecatedMagnitude" in API v2.  When v1 is
eventually removed, the deprecated field can be removed from v2.

### Enumerated or constant values

As with whole REST resources and fields thereof, a constant value which was
supported in API v1 must exist and function until API v1 is removed.

### Component config structures

Component configs are versioned and managed similar to REST resources.

### Future work

Over time, Kubernetes will introduce more fine-grained API versions, at which
point these rules will be adjusted as needed.

## Deprecating a flag or CLI

The Kubernetes system is comprised of several different programs cooperating.
Sometimes, a Kubernetes release might remove flags or CLI commands
(collectively "CLI elements") in these programs.  The individual programs
naturally sort into two main groups - user-facing and admin-facing programs,
which vary slightly in their deprecation policies.  Unless a flag is explicitly
prefixed or documented as "alpha" or "beta", it is considered GA.

CLI elements are effectively part of the API to the system, but since they are
not versioned in the same way as the REST API, the rules for deprecation are as
follows:

**Rule #5a: CLI elements of user-facing components (e.g. kubectl) must function
after their announced deprecation for no less than:**

   * **GA: 12 months or 2 releases (whichever is longer)**
   * **Beta: 3 months or 1 release (whichever is longer)**
   * **Alpha: 0 releases**

**Rule #5b: CLI elements of admin-facing components (e.g. kubelet) must function
after their announced deprecation for no less than:**

   * **GA: 6 months or 1 release (whichever is longer)**
   * **Beta: 3 months or 1 release (whichever is longer)**
   * **Alpha: 0 releases**

**Rule #6: Deprecated CLI elements must emit warnings (optionally disable)
when used.**

## Deprecating a feature or behavior

Occasionally a Kubernetes release needs to deprecate some feature or behavior
of the system that is not controlled by the API or CLI.  In this case, the
rules for deprecation are as follows:

**Rule #7: Deprecated behaviors must function for no less than 1 year after their
announced deprecation.**

This does not imply that all changes to the system are governed by this policy.
This applies only to significant, user-visible behaviors which impact the
correctness of applications running on Kubernetes or that impact the
administration of Kubernetes clusters, and which are being removed entirely.

An exception to the above rule is _feature gates_. Feature gates are key=value
pairs that allow for users to enable/disable experimental features.

Feature gates are intended to cover the development life cycle of a feature - they
are not intended to be long-term APIs. As such, they are expected to be deprecated
and removed after a feature becomes GA or is dropped.

As a feature moves through the stages, the associated feature gate evolves.
The feature life cycle matched to its corresponding feature gate is:

  * Alpha: the feature gate is disabled by default and can be enabled by the user.
  * Beta: the feature gate is enabled by default and can be disabled by the user.
  * Deprecated: the feature gate is disabled by default and can be enabled
  by the user for the duration of deprecation window. See ["Deprecation"](#deprecation).
  * GA: the feature gate is deprecated and becomes non-operational - enabled by
  default and cannot be disabled by the user.
  * GA or Deprecated, deprecation window complete: the feature gate is removed
  and calls to it are no longer accepted.

### Deprecation

Features can be removed at any point in the life cycle prior to GA. When features are
removed prior to GA, their associated feature gates are also deprecated.

When an invocation tries to disable a non-operational feature gate, the call fails in order
to avoid unsupported scenarios that might otherwise run silently.

In some cases, removing pre-GA features requires considerable time. Feature gates can remain
operational until their associated feature is fully removed, at which point the feature gate
itself can be deprecated.

When removing a feature gate for a GA feature also requires considerable time, calls to
feature gates may remain operational if the feature gate has no effect on the feature,
and if the feature gate causes no errors.

Features intended to be disabled by users should include a mechanism for disabling the
feature in the associated feature gate.

Versioning for feature gates is different from the previously discussed components,
therefore the rules for deprecation are as follows:

**Rule #8: Feature gates must be deprecated when the corresponding feature they control
transitions a lifecycle stage as follows. Feature gates must function for no less than:**

   * **Beta feature to GA: 6 months or 2 releases (whichever is longer)**
   * **Beta feature to EOL: 3 months or 1 release (whichever is longer)**
   * **Alpha feature to EOL: 0 releases**

**Rule #9: Deprecated feature gates must respond with a warning when used. When a feature gate
is deprecated it must be documented in both in the release notes and the corresponding CLI help.
Both warnings and documentation must indicate whether a feature gate is non-operational.
Throughout the deprecation period, the feature gate must be disabled by default.**

## Deprecating a metric

Each component of the Kubernetes control-plane exposes metrics (usually the
`/metrics` endpoint), which are typically ingested by cluster administrators.
Not all metrics are the same: some metrics are commonly used as SLIs or used
to determine SLOs, these tend to have greater import. Other metrics are more
experimental in nature or are used primarily in the Kubernetes development
process.

Accordingly, metrics fall under two stability classes (`ALPHA` and `STABLE`);
this impacts removal of a metric during a Kubernetes release. These classes
are determined by the perceived importance of the metric. The rules for
deprecating and removing a metric are as follows:

**Rule #9a: Metrics, for the corresponding stability class, must function for no less than:**

   * **STABLE: 4 releases or 12 months (whichever is longer)**
   * **ALPHA: 0 releases**

**Rule #9b: Metrics, after their _announced deprecation_, must function for no less than:**

   * **STABLE: 3 releases or 9 months (whichever is longer)**
   * **ALPHA: 0 releases**

Deprecated metrics will have their description text prefixed with a deprecation notice
string '(Deprecated from x.y)' and a warning log will be emitted during metric
registration. Like their stable undeprecated counterparts, deprecated metrics will
be automatically registered to the metrics endpoint and therefore visible.

On a subsequent release (when the metric's `deprecatedVersion` is equal to
_current_kubernetes_version - 3_)), a deprecated metric will become a _hidden_ metric.
**_Unlike_** their deprecated counterparts, hidden metrics will _no longer_ be
automatically registered to the metrics endpoint (hence hidden). However, they
can be explicitly enabled through a command line flag on the binary
(`--show-hidden-metrics-for-version=`). This provides cluster admins an
escape hatch to properly migrate off of a deprecated metric, if they were not
able to react to the earlier deprecation warnings. Hidden metrics should be
deleted after one release.


## Exceptions

No policy can cover every possible situation.  This policy is a living
document, and will evolve over time.  In practice, there will be situations
that do not fit neatly into this policy, or for which this policy becomes a
serious impediment.  Such situations should be discussed with SIGs and project
leaders to find the best solutions for those specific cases, always bearing in
mind that Kubernetes is committed to being a stable system that, as much as
possible, never breaks users. Exceptions will always be announced in all
relevant release notes.
