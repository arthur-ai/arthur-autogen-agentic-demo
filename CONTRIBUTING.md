# 👋 Contributing Guide

Welcome, and thank you for considering contributing to this project!

This repository follows modern Python tooling and automation using:
- ✅ `python-semantic-release` for automated versioning and changelogs  
- ✅ `Conventional Commits` for clean commit messages  
- ✅ Linters (`black`, `ruff`, `pylint`) for clean code  
- ✅ `pytest` for testing  
- ✅ GitHub Actions for CI  

Please read this guide before submitting a pull request or commit.

---

## ✅ Commit Message Format (Conventional Commits)

We use **[Conventional Commits](https://www.conventionalcommits.org/)** to automatically:
- Bump version numbers (`patch`, `minor`, `major`)
- Generate changelogs
- Tag releases

### 🎯 Format

```
<type>(optional-scope): short description

(optional body)

(optional footer for breaking changes or issue refs)
```

---

## 🚀 Commit Types

| Type       | Description |
|------------|-------------|
| `feat`     | New feature → bumps **minor** version |
| `fix`      | Bug fix → bumps **patch** version |
| `docs`     | Documentation changes only |
| `style`    | Code formatting (no logic change) |
| `refactor` | Code refactoring (no feature or fix) |
| `test`     | Adding or updating tests |
| `chore`    | Tooling, config, setup |
| `perf`     | Performance improvement |

---

### 💥 Breaking Changes

To trigger a **major version bump**, add a `BREAKING CHANGE:` footer in your commit message:

```
feat(auth): migrate to JWT

BREAKING CHANGE: removes legacy session-based authentication
```

---

## 📦 Examples

- `feat: add async endpoint to main.py`
- `fix: prevent crash on missing config`
- `docs: update README with setup instructions`
- `style: reformat files with black and isort`
- `refactor: simplify token verification logic`
- `test: add test for /ping route`
- `chore: update ruff complexity thresholds`

---

## 🧪 Running Tests

Run all tests locally using:

```bash
pytest
```

---

## 🩰 Dev Setup (Recommended)

Install dev dependencies:

```bash
pip install -r requirements-dev.txt
```

---

## ✅ Enforcing Commit Message Format with Pre-commit

This project uses [pre-commit](https://pre-commit.com/) to enforce Conventional Commit formatting locally.

### 1. Install pre-commit (if not already):
```bash
pip install pre-commit
```

### 2. Create the hook script:
Save the following as `scripts/check-commit-msg.sh`:
```bash
#!/bin/bash

commit_msg_file=$1
commit_msg=$(cat "$commit_msg_file")

if ! echo "$commit_msg" | grep -Eq '^(feat|fix|docs|style|refactor|test|chore|perf)(\(.+\))?: .+'; then
  echo "❌ Commit message does not follow Conventional Commits format."
  echo "👉 Example: feat(api): add login route"
  exit 1
fi
```

Make it executable:
```bash
chmod +x scripts/check-commit-msg.sh
```

### 3. Configure pre-commit
Create a `.pre-commit-config.yaml` in the root of your project:
```yaml
repos:
  - repo: local
    hooks:
      - id: commit-msg-format
        name: Check commit message format
        entry: ./scripts/check-commit-msg.sh
        language: system
        stages: [commit-msg]
```

### 4. Install the hook
```bash
pre-commit install --hook-type commit-msg
```

Now all commit messages will be validated automatically before committing.

---

## ✅ Thanks for contributing! 🙌

