---
title: Managing Secret using Configuration File
content_type: task
weight: 20
description: Creating Secret objects using resource configuration file.
---

<!-- overview -->

## {{% heading "prerequisites" %}}

{{< include "task-tutorial-prereqs.md" >}}

<!-- steps -->

## Create the Config file

You can create a Secret in a file first, in JSON or YAML format, and then
create that object.  The
{{< api-reference page="config-and-storage-resources/secret-v1" >}}
resource contains two maps: `data` and `stringData`.
The `data` field is used to store arbitrary data, encoded using base64. The
`stringData` field is provided for convenience, and it allows you to provide
Secret data as unencoded strings.
The keys of `data` and `stringData` must consist of alphanumeric characters,
`-`, `_` or `.`.

For example, to store two strings in a Secret using the `data` field, convert
the strings to base64 as follows:

```shell
echo -n 'admin' | base64
```

The output is similar to:

```
YWRtaW4=
```

```shell
echo -n '1f2d1e2e67df' | base64
```

The output is similar to:

```
MWYyZDFlMmU2N2Rm
```

Write a Secret config file that looks like this:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: mysecret
type: Opaque
data:
  username: YWRtaW4=
  password: MWYyZDFlMmU2N2Rm
```

Note that the name of a Secret object must be a valid
[DNS subdomain name](/docs/concepts/overview/working-with-objects/names#dns-subdomain-names).

{{< note >}}
The serialized JSON and YAML values of Secret data are encoded as base64
strings. Newlines are not valid within these strings and must be omitted. When
using the `base64` utility on Darwin/macOS, users should avoid using the `-b`
option to split long lines. Conversely, Linux users *should* add the option
`-w 0` to `base64` commands or the pipeline `base64 | tr -d '\n'` if the `-w`
option is not available.
{{< /note >}}

For certain scenarios, you may wish to use the `stringData` field instead. This
field allows you to put a non-base64 encoded string directly into the Secret,
and the string will be encoded for you when the Secret is created or updated.

A practical example of this might be where you are deploying an application
that uses a Secret to store a configuration file, and you want to populate
parts of that configuration file during your deployment process.

For example, if your application uses the following configuration file:

```yaml
apiUrl: "https://my.api.com/api/v1"
username: "<user>"
password: "<password>"
```

You could store this in a Secret using the following definition:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: mysecret
type: Opaque
stringData:
  config.yaml: |
    apiUrl: "https://my.api.com/api/v1"
    username: <user>
    password: <password>
```

## Create the Secret object

Now create the Secret using [`kubectl apply`](/docs/reference/generated/kubectl/kubectl-commands#apply):

```shell
kubectl apply -f ./secret.yaml
```

The output is similar to:

```
secret/mysecret created
```

## Check the Secret

The `stringData` field is a write-only convenience field. It is never output when
retrieving Secrets. For example, if you run the following command:

```shell
kubectl get secret mysecret -o yaml
```

The output is similar to:

```yaml
apiVersion: v1
data:
  config.yaml: YXBpVXJsOiAiaHR0cHM6Ly9teS5hcGkuY29tL2FwaS92MSIKdXNlcm5hbWU6IHt7dXNlcm5hbWV9fQpwYXNzd29yZDoge3twYXNzd29yZH19
kind: Secret
metadata:
  creationTimestamp: 2018-11-15T20:40:59Z
  name: mysecret
  namespace: default
  resourceVersion: "7225"
  uid: c280ad2e-e916-11e8-98f2-025000000001
type: Opaque
```

The commands `kubectl get` and `kubectl describe` avoid showing the contents of a `Secret` by
default. This is to protect the `Secret` from being exposed accidentally to an onlooker,
or from being stored in a terminal log.
To check the actual content of the encoded data, please refer to
[decoding secret](/docs/tasks/configmap-secret/managing-secret-using-kubectl/#decoding-secret).

If a field, such as `username`, is specified in both `data` and `stringData`,
the value from `stringData` is used. For example, the following Secret definition:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: mysecret
type: Opaque
data:
  username: YWRtaW4=
stringData:
  username: administrator
```

Results in the following Secret:

```yaml
apiVersion: v1
data:
  username: YWRtaW5pc3RyYXRvcg==
kind: Secret
metadata:
  creationTimestamp: 2018-11-15T20:46:46Z
  name: mysecret
  namespace: default
  resourceVersion: "7579"
  uid: 91460ecb-e917-11e8-98f2-025000000001
type: Opaque
```

Where `YWRtaW5pc3RyYXRvcg==` decodes to `administrator`.

## Clean Up

To delete the Secret you have created:

```shell
kubectl delete secret mysecret
```

## {{% heading "whatsnext" %}}

- Read more about the [Secret concept](/docs/concepts/configuration/secret/)
- Learn how to [manage Secret with the `kubectl` command](/docs/tasks/configmap-secret/managing-secret-using-kubectl/)
- Learn how to [manage Secret using kustomize](/docs/tasks/configmap-secret/managing-secret-using-kustomize/)

