#!/bin/bash

set -e

# Load .env
if [ -f .env ]; then
  set -o allexport
  source .env
  set +o allexport
fi

# Ensure PROJECT_PATH is set
if [ -z "$PROJECT_PATH" ]; then
  echo "❌ PROJECT_PATH is not set in your .env file."
  exit 1
fi

export PYTHONPATH="$PROJECT_PATH"

echo "📂 Running auto-fix + lint on all Python files in src/..."

find src -name "*.py" | while read file; do
  echo "------------------------------------------------------------"
  echo "📄 Processing: $file"

  echo "🎨 black..."
  black "$file" || echo "⚠️ black failed on $file"

  echo "📦 isort..."
  isort "$file" || echo "⚠️ isort failed on $file"

  echo "🧹 ruff..."
  ruff check "$file" --fix || echo "⚠️ ruff failed on $file"

  echo "🔍 pylint..."
  pylint "$file" || echo "⚠️ pylint failed on $file"
done

echo "✅ All files processed."
