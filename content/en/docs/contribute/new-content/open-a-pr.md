---
title: Opening a pull request
content_type: concept
weight: 10
card:
  name: contribute
  weight: 40
---

<!-- overview -->

{{< note >}}
**Code developers**: If you are documenting a new feature for an
upcoming Kubernetes release, see
[Document a new feature](/docs/contribute/new-content/new-features/).
{{< /note >}}

To contribute new content pages or improve existing content pages, open a pull request (PR). Make sure you follow all the requirements in the [Before you begin](/docs/contribute/new-content/overview/#before-you-begin) section.

If your change is small, or you're unfamiliar with git, read [Changes using GitHub](#changes-using-github) to learn how to edit a page.

If your changes are large, read [Work from a local fork](#fork-the-repo) to learn how to make changes locally on your computer.



<!-- body -->

## Changes using GitHub

If you're less experienced with git workflows, here's an easier method of
opening a pull request.

1.  On the page where you see the issue, select the pencil icon at the top right.
    You can also scroll to the bottom of the page and select **Edit this page**.

2.  Make your changes in the GitHub markdown editor.

3.  Below the editor, fill in the **Propose file change**
    form. In the first field, give your commit message a title. In
    the second field, provide a description.

    {{< note >}}
    Do not use any [GitHub Keywords](https://help.github.com/en/github/managing-your-work-on-github/linking-a-pull-request-to-an-issue#linking-a-pull-request-to-an-issue-using-a-keyword) in your commit message. You can add those to the pull request
    description later.
    {{< /note >}}

4.  Select **Propose file change**.

5.  Select **Create pull request**.

6.  The **Open a pull request** screen appears. Fill in the form:

    - The **Subject** field of the pull request defaults to the commit summary.
    You can change it if needed.
    - The **Body** contains your extended commit message, if you have one,
    and some template text. Add the
    details the template text asks for, then delete the extra template text.
    - Leave the **Allow edits from maintainers** checkbox selected.

    {{< note >}}
    PR descriptions are a great way to help reviewers understand your change. For more information, see [Opening a PR](#open-a-pr).
    {{</ note >}}

7.  Select **Create pull request**.

### Addressing feedback in GitHub

Before merging a pull request, Kubernetes community members review and
approve it. The `k8s-ci-robot` suggests reviewers based on the nearest
owner mentioned in the pages. If you have someone specific in mind,
leave a comment with their GitHub username in it.

If a reviewer asks you to make changes:

1. Go to the **Files changed** tab.
2. Select the pencil (edit) icon on any files changed by the
pull request.
3. Make the changes requested.
4. Commit the changes.

If you are waiting on a reviewer, reach out once every 7 days. You can also post a message in the `#sig-docs` Slack channel.

When your review is complete, a reviewer merges your PR and your changes go live a few minutes later.

## Work from a local fork {#fork-the-repo}

If you're more experienced with git, or if your changes are larger than a few lines,
work from a local fork.

Make sure you have [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) installed on your computer. You can also use a git UI application.

### Fork the kubernetes/website repository

1. Navigate to the [`kubernetes/website`](https://github.com/kubernetes/website/) repository.
2. Select **Fork**.

### Create a local clone and set the upstream

3. In a terminal window, clone your fork and update the [Docsy Hugo theme](https://github.com/google/docsy#readme):

    ```bash
    git clone git@github.com/<github_username>/website
    cd website
    git submodule update --init --recursive --depth 1
    ```

4. Navigate to the new `website` directory. Set the `kubernetes/website` repository as the `upstream` remote:

      ```bash
      cd website

      git remote add upstream https://github.com/kubernetes/website.git
      ```

5. Confirm your `origin` and `upstream` repositories:

    ```bash
    git remote -v
    ```

    Output is similar to:

    ```bash
    origin	git@github.com:<github_username>/website.git (fetch)
    origin	git@github.com:<github_username>/website.git (push)
    upstream	https://github.com/kubernetes/website.git (fetch)
    upstream	https://github.com/kubernetes/website.git (push)
    ```

6. Fetch commits from your fork's `origin/main` and `kubernetes/website`'s `upstream/main`:

    ```bash
    git fetch origin
    git fetch upstream
    ```

    This makes sure your local repository is up to date before you start making changes.

    {{< note >}}
    This workflow is different than the [Kubernetes Community GitHub Workflow](https://github.com/kubernetes/community/blob/master/contributors/guide/github-workflow.md). You do not need to merge your local copy of `main` with `upstream/main` before pushing updates to your fork.
    {{< /note >}}

### Create a branch

1. Decide which branch base to your work on:

  - For improvements to existing content, use `upstream/main`.
  - For new content about existing features, use `upstream/main`.
  - For localized content, use the localization's conventions. For more information, see [localizing Kubernetes documentation](/docs/contribute/localization/).
  - For new features in an upcoming Kubernetes release, use the feature branch. For more information, see [documenting for a release](/docs/contribute/new-content/new-features/).
  - For long-running efforts that multiple SIG Docs contributors collaborate on,
    like content reorganization, use a specific feature branch created for that
    effort.

    If you need help choosing a branch, ask in the `#sig-docs` Slack channel.

2. Create a new branch based on the branch identified in step 1. This example assumes the base branch is `upstream/main`:

    ```bash
    git checkout -b <my_new_branch> upstream/main
    ```

3.  Make your changes using a text editor.

At any time, use the `git status` command to see what files you've changed.

### Commit your changes

When you are ready to submit a pull request, commit your changes.

1. In your local repository, check which files you need to commit:

    ```bash
    git status
    ```

    Output is similar to:

    ```bash
    On branch <my_new_branch>
    Your branch is up to date with 'origin/<my_new_branch>'.

    Changes not staged for commit:
    (use "git add <file>..." to update what will be committed)
    (use "git checkout -- <file>..." to discard changes in working directory)

    modified:   content/en/docs/contribute/new-content/contributing-content.md

    no changes added to commit (use "git add" and/or "git commit -a")
    ```

2. Add the files listed under **Changes not staged for commit** to the commit:

    ```bash
    git add <your_file_name>
    ```

    Repeat this for each file.

3.  After adding all the files, create a commit:

    ```bash
    git commit -m "Your commit message"
    ```

    {{< note >}}
    Do not use any [GitHub Keywords](https://help.github.com/en/github/managing-your-work-on-github/linking-a-pull-request-to-an-issue#linking-a-pull-request-to-an-issue-using-a-keyword) in your commit message. You can add those to the pull request
    description later.
    {{< /note >}}

4. Push your local branch and its new commit to your remote fork:

    ```bash
    git push origin <my_new_branch>
    ```

### Preview your changes locally {#preview-locally}

It's a good idea to preview your changes locally before pushing them or opening a pull request. A preview lets you catch build errors or markdown formatting problems.

You can either build the website's container image or run Hugo locally. Building the container image is slower but displays [Hugo shortcodes](/docs/contribute/style/hugo-shortcodes/), which can be useful for debugging.

{{< tabs name="tab_with_hugo" >}}
{{% tab name="Hugo in a container" %}}

{{< note >}}
The commands below use Docker as default container engine. Set the `CONTAINER_ENGINE` environment variable to override this behaviour.
{{< /note >}}

1.  Build the image locally:

      ```bash
      # Use docker (default)
      make container-image

      ### OR ###

      # Use podman
      CONTAINER_ENGINE=podman make container-image
      ```

2. After building the `kubernetes-hugo` image locally, build and serve the site:

      ```bash
      # Use docker (default)
      make container-serve

      ### OR ###

      # Use podman
      CONTAINER_ENGINE=podman make container-serve
      ```

3.  In a web browser, navigate to `https://localhost:1313`. Hugo watches the
    changes and rebuilds the site as needed.

4.  To stop the local Hugo instance, go back to the terminal and type `Ctrl+C`,
    or close the terminal window.

{{% /tab %}}
{{% tab name="Hugo on the command line" %}}

Alternately, install and use the `hugo` command on your computer:

1.  Install the [Hugo](https://gohugo.io/getting-started/installing/) version specified in [`website/netlify.toml`](https://raw.githubusercontent.com/kubernetes/website/main/netlify.toml).

2.  If you have not updated your website repository, the `website/themes/docsy` directory is empty.
    The site cannot build without a local copy of the theme. To update the website theme, run:

    ```bash
    git submodule update --init --recursive --depth 1
    ```

3.  In a terminal, go to your Kubernetes website repository and start the Hugo server:

      ```bash
      cd <path_to_your_repo>/website
      hugo server --buildFuture
      ```

4.  In a web browser, navigate to `https://localhost:1313`. Hugo watches the
    changes and rebuilds the site as needed.

5.  To stop the local Hugo instance, go back to the terminal and type `Ctrl+C`,
    or close the terminal window.

{{% /tab %}}
{{< /tabs >}}

### Open a pull request from your fork to kubernetes/website {#open-a-pr}

1. In a web browser, go to the [`kubernetes/website`](https://github.com/kubernetes/website/) repository.
2. Select **New Pull Request**.
3. Select **compare across forks**.
4. From the **head repository** drop-down menu, select your fork.
5. From the **compare** drop-down menu, select your branch.
6. Select **Create Pull Request**.
7. Add a description for your pull request:
    - **Title** (50 characters or less): Summarize the intent of the change.
    - **Description**: Describe the change in more detail.
      - If there is a related GitHub issue, include `Fixes #12345` or `Closes #12345` in the description. GitHub's automation closes the mentioned issue after merging the PR if used. If there are other related PRs, link those as well.
      - If you want advice on something specific, include any questions you'd like reviewers to think about in your description.

8. Select the **Create pull request** button.

  Congratulations! Your pull request is available in [Pull requests](https://github.com/kubernetes/website/pulls).


After opening a PR, GitHub runs automated tests and tries to deploy a preview using [Netlify](https://www.netlify.com/).

  - If the Netlify build fails, select **Details** for more information.
  - If the Netlify build succeeds, select **Details** opens a staged version of the Kubernetes website with your changes applied. This is how reviewers check your changes.

GitHub also automatically assigns labels to a PR, to help reviewers. You can add them too, if needed. For more information, see [Adding and removing issue labels](/docs/contribute/review/for-approvers/#adding-and-removing-issue-labels).

### Addressing feedback locally

1. After making your changes, amend your previous commit:

    ```bash
    git commit -a --amend
    ```

    - `-a`: commits all changes
    - `--amend`: amends the previous commit, rather than creating a new one

2. Update your commit message if needed.

3. Use `git push origin <my_new_branch>` to push your changes and re-run the Netlify tests.

    {{< note >}}
      If you use `git commit -m` instead of amending, you must [squash your commits](#squashing-commits) before merging.
    {{< /note >}}

#### Changes from reviewers

Sometimes reviewers commit to your pull request. Before making any other changes, fetch those commits.

1. Fetch commits from your remote fork and rebase your working branch:

    ```bash
    git fetch origin
    git rebase origin/<your-branch-name>
    ```

2. After rebasing, force-push new changes to your fork:

    ```bash
    git push --force-with-lease origin <your-branch-name>
    ```

#### Merge conflicts and rebasing

{{< note >}}
For more information, see [Git Branching - Basic Branching and Merging](https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging#_basic_merge_conflicts), [Advanced Merging](https://git-scm.com/book/en/v2/Git-Tools-Advanced-Merging), or ask in the `#sig-docs` Slack channel for help.
{{< /note >}}

If another contributor commits changes to the same file in another PR, it can create a merge conflict. You must resolve all merge conflicts in your PR.

1. Update your fork and rebase your local branch:

    ```bash
    git fetch origin
    git rebase origin/<your-branch-name>
    ```

    Then force-push the changes to your fork:

    ```bash
    git push --force-with-lease origin <your-branch-name>
    ```

2. Fetch changes from `kubernetes/website`'s `upstream/main` and rebase your branch:

    ```bash
    git fetch upstream
    git rebase upstream/main
    ```

3. Inspect the results of the rebase:

    ```bash
    git status
    ```

  This results in a number of files marked as conflicted.

4. Open each conflicted file and look for the conflict markers: `>>>`, `<<<`, and `===`. Resolve the conflict and delete the conflict marker.

    {{< note >}}
    For more information, see [How conflicts are presented](https://git-scm.com/docs/git-merge#_how_conflicts_are_presented).
    {{< /note >}}

5. Add the files to the changeset:

    ```bash
    git add <filename>
    ```
6.  Continue the rebase:

    ```bash
    git rebase --continue
    ```

7.  Repeat steps 2 to 5 as needed.

    After applying all commits, the `git status` command shows that the rebase is complete.

8. Force-push the branch to your fork:

    ```bash
    git push --force-with-lease origin <your-branch-name>
    ```

    The pull request no longer shows any conflicts.


### Squashing commits

{{< note >}}
For more information, see [Git Tools - Rewriting History](https://git-scm.com/book/en/v2/Git-Tools-Rewriting-History), or ask in the `#sig-docs` Slack channel for help.
{{< /note >}}

If your PR has multiple commits, you must squash them into a single commit before merging your PR. You can check the number of commits on your PR's **Commits** tab or by running the `git log` command locally.

{{< note >}}
This topic assumes `vim` as the command line text editor.
{{< /note >}}

1. Start an interactive rebase:

    ```bash
    git rebase -i HEAD~<number_of_commits_in_branch>
    ```

    Squashing commits is a form of rebasing. The `-i` switch tells git you want to rebase interactively. `HEAD~<number_of_commits_in_branch` indicates how many commits to look at for the rebase.

    Output is similar to:

    ```bash
    pick d875112ca Original commit
    pick 4fa167b80 Address feedback 1
    pick 7d54e15ee Address feedback 2

    # Rebase 3d18sf680..7d54e15ee onto 3d183f680 (3 commands)

    ...

    # These lines can be re-ordered; they are executed from top to bottom.
    ```

    The first section of the output lists the commits in the rebase. The second section lists the options for each commit. Changing the word `pick` changes the status of the commit once the rebase is complete.

    For the purposes of rebasing, focus on `squash` and `pick`.

    {{< note >}}
    For more information, see [Interactive Mode](https://git-scm.com/docs/git-rebase#_interactive_mode).
    {{< /note >}}

2. Start editing the file.

    Change the original text:

    ```bash
    pick d875112ca Original commit
    pick 4fa167b80 Address feedback 1
    pick 7d54e15ee Address feedback 2
    ```

    To:

    ```bash
    pick d875112ca Original commit
    squash 4fa167b80 Address feedback 1
    squash 7d54e15ee Address feedback 2
    ```

    This squashes commits `4fa167b80 Address feedback 1` and `7d54e15ee Address feedback 2` into `d875112ca Original commit`, leaving only `d875112ca Original commit` as a part of the timeline.

3. Save and exit your file.

4. Push your squashed commit:

    ```bash
    git push --force-with-lease origin <branch_name>
    ```

## Contribute to other repos

The [Kubernetes project](https://github.com/kubernetes) contains 50+ repositories. Many of these repositories contain documentation: user-facing help text, error messages, API references or code comments.

If you see text you'd like to improve, use GitHub to search all repositories in the Kubernetes organization.
This can help you figure out where to submit your issue or PR.

Each repository has its own processes and procedures. Before you file an
issue or submit a PR, read that repository's `README.md`, `CONTRIBUTING.md`, and
`code-of-conduct.md`, if they exist.

Most repositories use issue and PR templates. Have a look through some open
issues and PRs to get a feel for that team's processes. Make sure to fill out
the templates with as much detail as possible when you file issues or PRs.



## {{% heading "whatsnext" %}}


- Read [Reviewing](/docs/contribute/review/reviewing-prs) to learn more about the review process.


