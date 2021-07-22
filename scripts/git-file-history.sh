#!/usr/bin/env bash

set -euo pipefail

SEARCH_DIR='./content/en/docs'

query_stale_files() {
    # find markdown files in content/en/docs excluding _index.md, glossary, and reference files
    SEARCH_FILES=($(find $SEARCH_DIR -name '*.md' -not -name '_index.md' -not -path '*/glossary/*' -not -path '*/reference/*'))
    MOD_FILES=($(git log --since '6 months ago' --name-only --pretty=format: content/en/docs | sort  | uniq | awk '{print "./"$1}' ))

    declare -a output=()
    for i in "${SEARCH_FILES[@]}"; do
        if [[ ! " ${MOD_FILES[@]} " =~ " $i " ]]; then
            timestamp=$(git log -1 --pretty='format:%as' $i)
            output+=("$timestamp $i")
        fi
    done

    IFS=$'\n'
    sorted=($(sort <<<"${output[*]}"))
    unset IFS

    for row in "${sorted[@]}"; do
        echo "$row"
    done
}

query_stale_files