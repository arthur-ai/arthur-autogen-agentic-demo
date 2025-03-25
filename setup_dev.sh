#!/bin/bash
set -e

echo "🔧 Setting up development environment..."

# Check for Python
if ! command -v python3 &>/dev/null; then
  echo "❌ Python 3 is not installed. Please install it and retry."
  exit 1
fi

# Create virtual environment
if [ ! -d ".venv" ]; then
  echo "📦 Creating virtual environment in .venv..."
  python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📦 Installing project dependencies..."
pip install -r requirements.txt

if [ -f requirements-dev.txt ]; then
  echo "📦 Installing development tools..."
  pip install -r requirements-dev.txt
fi

# Install pre-commit hooks
if command -v pre-commit &>/dev/null; then
  echo "✅ Installing pre-commit hooks..."
  pre-commit install --hook-type commit-msg
else
  echo "⚠️  pre-commit not found. Installing it..."
  pip install pre-commit
  pre-commit install --hook-type commit-msg
fi

echo "✅ Setup complete. Activate your virtualenv with:"
echo "source .venv/bin/activate"
