#!/bin/bash
set -e

echo "📘 Running semantic-release changelog..."

python -m semantic_release changelog

echo "✅ CHANGELOG.md updated."
