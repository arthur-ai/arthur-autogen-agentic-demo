#!/bin/bash

commit_msg_file=$1
commit_msg=$(cat "$commit_msg_file")

if ! echo "$commit_msg" | grep -Eq '^(feat|fix|docs|style|refactor|test|chore|perf)(\(.+\))?: .+'; then
  echo "❌ Commit message does not follow Conventional Commits format."
  echo "👉 Example: feat(api): add login route"
  exit 1
fi