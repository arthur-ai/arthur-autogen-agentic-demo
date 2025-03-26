#!/bin/bash
set -e

BRANCH_NAME=$(git rev-parse --abbrev-ref HEAD)

echo "🔍 Checking branch name: $BRANCH_NAME"

if [[ ! "$BRANCH_NAME" =~ ^(feature|bugfix|hotfix|release|chore|docs|test)/[a-z0-9._-]+$ ]]; then
  echo "❌ Invalid branch name: '$BRANCH_NAME'"
  echo "✅ Use one of these formats:"
  echo "   - feature/my-new-feature"
  echo "   - bugfix/fix-bug-123"
  echo "   - release/v1.0.0"
  echo "   - hotfix/security-patch"
  echo "   - chore/update-deps"
  echo "   - docs/update-readme"
  echo "   - test/add-new-tests"
  exit 1
fi

echo "✅ Branch name is valid!"
