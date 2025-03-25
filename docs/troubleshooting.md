# 🧯 Troubleshooting Guide

This guide helps debug common issues encountered while working with this repo.

## Common Issues

In progress

### 🐍 Import Errors

Ensure the `src/` folder is on your `PYTHONPATH`:
```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)/src
```

### 🔧 Pre-commit Not Running

Run:
```bash
pre-commit install --hook-type commit-msg
```

### 🧪 Tests Failing

Check:
- Test paths: `tests/`
- Async tests use `pytest-asyncio`
- Use Python 3.11+
