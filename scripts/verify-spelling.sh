#!/usr/bin/env bash

# Copyright 2019 The Kubernetes Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##########
# This script verifies mispellings in location. Today it only supports
# verifying English locale but can be modified in a future to support
# also other locales.
# You need to run this script inside the root directory of "website" git repo.
#
# Syntax: verify-spelling.sh LOCALE
# Example: verify-spelling.sh en
# If no locale is passed, it will assume "en"
#
# Requirements:
# - go v1.14 or superior version



set -o errexit
set -o nounset
set -o pipefail

TOOL_VERSION="v0.3.4"

KUBE_ROOT=$(dirname "${BASH_SOURCE[0]}")/..
export KUBE_ROOT

LANGUAGE="${1:-en}"
# cd to the root path
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
cd "${ROOT}"

# create a temporary directory
TMP_DIR=$(mktemp -d)

# cleanup
exitHandler() (
  echo "Cleaning up..."
  rm -rf "${TMP_DIR}"
)
trap exitHandler EXIT

# perform go get in a temp dir as we are not tracking this version in a go module
# if we do the go get in the repo, it will create / update a go.mod and go.sum
cd "${TMP_DIR}"
GO111MODULE=on GOBIN="${TMP_DIR}" go get "github.com/client9/misspell/cmd/misspell@${TOOL_VERSION}"
export PATH="${TMP_DIR}:${PATH}"
cd "${ROOT}"

# check spelling
RES=0
echo "Checking spelling..."
ERROR_LOG="${TMP_DIR}/errors.log"

# NOTE we usually don't correct old blog articles, so we ignore them in
# this file.
skipping_file="${KUBE_ROOT}/scripts/.spelling_failures"
failing_packages=$(sed "s| | -e |g" "${skipping_file}")
git ls-files | grep content/${LANGUAGE} | grep -v -e "${failing_packages}" | xargs misspell > "${ERROR_LOG}"
if [[ -s "${ERROR_LOG}" ]]; then
  sed 's/^/error: /' "${ERROR_LOG}" # add 'error' to each line to highlight in e2e status
  echo "Found spelling errors!"
  RES=1
fi
exit "${RES}"
