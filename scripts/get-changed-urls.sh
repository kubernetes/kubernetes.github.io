#!/bin/bash

# This script lists URLs changed by the target PR. You can jump to target page quickly by clicking those.
# Syntax: get-changed-urls.sh <PR number> [<page top URL>]
# Example: 
# $ get-changed-urls.sh 28542
# http://localhost:1313/ja/docs/concepts/configuration/manage-resources-containers
# http://localhost:1313/ja/docs/concepts/policy/limit-range
# http://localhost:1313/ja/docs/concepts/policy/resource-quotas
# http://localhost:1313/ja/docs/reference/command-line-tools-reference/feature-gates
# http://localhost:1313/ja/docs/setup/best-practices/cluster-large
#
# If no <page top URL> is passed, it will assume "http://localhost:1313".
# It's the default endpoint for "make container-serve" or "make serve".
# Please look at the README(https://github.com/kubernetes/website#using-this-repository) to serve endpoint.
# Or you can pass any strings to <page top URL>.
# You can get URLs for upstream by passing <page top URL> as "https://kubernetes.io".

set -e

if [[ ${1} == "" ]]
then
	echo "This script prints all URLs updated by target PR number."
	echo "You can jump to updated pages quickly when PR review."
	echo "This is intended for using with \"make container-serve\"."
	echo ""
	echo "Syntax: get-changed-urls.sh <PR number> [<page top URL>]"
	echo "Example: get-changed-urls.sh 12345"
	echo "If no <page top URL> is passed, it will assume \"http://localhost:1313\""
	exit 1
fi

PAGE_TOP=${2:-"http://localhost:1313"}

GITHUB_REPOSITORY="kubernetes/website"
PR_NUM=${1}

# URL for calling GitHub API
# For detail: https://docs.github.com/en/rest/reference/pulls#list-pull-requests-files
GITHUB_API_URL="https://api.github.com/repos/${GITHUB_REPOSITORY}/pulls/${PR_NUM}/files"

# Get files included in target PR
URLS=$(curl --silent -X GET ${GITHUB_API_URL} | jq -r '.[].filename' | \
	sed -e "s/^content\/en//g" -e "s/^content//g" -e "s/.md$//g" | grep "docs" | xargs -I {} echo ${PAGE_TOP}{})
for u in ${URLS}
do
	echo ${u}
done
