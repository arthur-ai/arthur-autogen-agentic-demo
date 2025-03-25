#!/bin/bash

set -e  # Stop on first error (except where handled manually)

# Load .env file if it exists
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

echo "🔧 Ensuring formatters & linters are installed..."
python -m pip install --upgrade pip
pip install black isort ruff pylint

echo "📂 Running per-file auto-fix + lint on all Python files under src/..."

find src -name "*.py" | while read file; do
  echo "------------------------------------------------------------"
  echo "📄 Processing: $file"

  echo "🎨 Formatting with black..."
  black "$file" || echo "⚠️ black failed on $file"

  echo "📦 Sorting imports with isort..."
  isort "$file" || echo "⚠️ isort failed on $file"

  echo "🧹 Lint-fixing with ruff..."
  ruff check "$file" --fix || echo "⚠️ ruff failed on $file"

  echo "🔍 Linting with pylint..."
  pylint "$file" || echo "⚠️ Skipping $file due to pylint crash"

done

echo "✅ All files processed."
