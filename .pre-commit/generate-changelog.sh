#!/bin/bash
set -e


# Use virtualenv Python explicitly
source .venv/bin/activate

echo "📘 Running semantic-release changelog..."

python -m semantic_release changelog

echo "✅ CHANGELOG.md updated."
