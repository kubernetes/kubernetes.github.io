---
title: Organizing Cluster Access Using kubeconfig Files
content_type: concept
weight: 60
---

<!-- overview -->

Use kubeconfig files to organize information about clusters, users, namespaces, and
authentication mechanisms. The `kubectl` command-line tool uses kubeconfig files to
find the information it needs to choose a cluster and communicate with the API server
of a cluster.

{{< note >}}
A file that is used to configure access to clusters is called
a *kubeconfig file*. This is a generic way of referring to configuration files.
It does not mean that there is a file named `kubeconfig`.
{{< /note >}}

{{< warning >}}
Only use kubeconfig files from trusted sources. Using a specially-crafted kubeconfig file could result in malicious code execution or file exposure. 
If you must use an untrusted kubeconfig file, inspect it carefully first, much as you would a shell script.
{{< /warning>}}

By default, `kubectl` looks for a file named `config` in the `$HOME/.kube` directory.
You can specify other kubeconfig files by setting the `KUBECONFIG` environment
variable or by setting the
[`--kubeconfig`](/docs/reference/generated/kubectl/kubectl/) flag.

For step-by-step instructions on creating and specifying kubeconfig files, see
[Configure Access to Multiple Clusters](/docs/tasks/access-application-cluster/configure-access-multiple-clusters).




<!-- body -->

## Supporting multiple clusters, users, and authentication mechanisms

Suppose you have several clusters, and your users and components authenticate
in a variety of ways. For example:

- A running kubelet might authenticate using certificates.
- A user might authenticate using tokens.
- Administrators might have sets of certificates that they provide to individual users.

With kubeconfig files, you can organize your clusters, users, and namespaces.
You can also define contexts to quickly and easily switch between
clusters and namespaces.

## Context

A *context* element in a kubeconfig file is used to group access parameters
under a convenient name. Each context has three parameters: cluster, namespace, and user.
By default, the `kubectl` command-line tool uses parameters from
the *current context* to communicate with the cluster. 

To choose the current context:
```
kubectl config use-context
```

## The KUBECONFIG environment variable

The `KUBECONFIG` environment variable holds a list of kubeconfig files.
For Linux and Mac, the list is colon-delimited. For Windows, the list
is semicolon-delimited. The `KUBECONFIG` environment variable is not
required. If the `KUBECONFIG` environment variable doesn't exist,
`kubectl` uses the default kubeconfig file, `$HOME/.kube/config`.

If the `KUBECONFIG` environment variable does exist, `kubectl` uses
an effective configuration that is the result of merging the files
listed in the `KUBECONFIG` environment variable.

## Merging kubeconfig files

To see your configuration, enter this command:

```shell
kubectl config view
```

As described previously, the output might be from a single kubeconfig file,
or it might be the result of merging several kubeconfig files.

Here are the rules that `kubectl` uses when it merges kubeconfig files:

1. If the `--kubeconfig` flag is set, use only the specified file. Do not merge.
   Only one instance of this flag is allowed.

   Otherwise, if the `KUBECONFIG` environment variable is set, use it as a
   list of files that should be merged.
   Merge the files listed in the `KUBECONFIG` environment variable
   according to these rules:

   * Ignore empty filenames.
   * Produce errors for files with content that cannot be deserialized.
   * The first file to set a particular value or map key wins.
   * Never change the value or map key.
     Example: Preserve the context of the first file to set `current-context`.
     Example: If two files specify a `red-user`, use only values from the first file's `red-user`.
     Even if the second file has non-conflicting entries under `red-user`, discard them.

   For an example of setting the `KUBECONFIG` environment variable, see
   [Setting the KUBECONFIG environment variable](/docs/tasks/access-application-cluster/configure-access-multiple-clusters/#set-the-kubeconfig-environment-variable).

   Otherwise, use the default kubeconfig file, `$HOME/.kube/config`, with no merging.

1. Determine the context to use based on the first hit in this chain:

    1. Use the `--context` command-line flag if it exists.
    1. Use the `current-context` from the merged kubeconfig files.

   An empty context is allowed at this point.

1. Determine the cluster and user. At this point, there might or might not be a context.
   Determine the cluster and user based on the first hit in this chain,
   which is run twice: once for user and once for cluster:

   1. Use a command-line flag if it exists: `--user` or `--cluster`.
   1. If the context is non-empty, take the user or cluster from the context.

   The user and cluster can be empty at this point.

1. Determine the actual cluster information to use. At this point, there might or
   might not be cluster information.
   Build each piece of the cluster information based on this chain; the first hit wins:

   1. Use command line flags if they exist: `--server`, `--certificate-authority`, `--insecure-skip-tls-verify`.
   1. If any cluster information attributes exist from the merged kubeconfig files, use them.
   1. If there is no server location, fail.

1. Determine the actual user information to use. Build user information using the same
   rules as cluster information, except allow only one authentication
   technique per user:

   1. Use command line flags if they exist: `--client-certificate`, `--client-key`, `--username`, `--password`, `--token`.
   1. Use the `user` fields from the merged kubeconfig files.
   1. If there are two conflicting techniques, fail.

1. For any information still missing, use default values and potentially
   prompt for authentication information.

## File references

File and path references in a kubeconfig file are relative to the location of the kubeconfig file.
File references on the command line are relative to the current working directory.
In `$HOME/.kube/config`, relative paths are stored relatively, and absolute paths
are stored absolutely.




## {{% heading "whatsnext" %}}


* [Configure Access to Multiple Clusters](/docs/tasks/access-application-cluster/configure-access-multiple-clusters/)
* [`kubectl config`](/docs/reference/generated/kubectl/kubectl-commands#config)



