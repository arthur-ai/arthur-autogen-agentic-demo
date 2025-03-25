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

## ✅ Thanks for contributing! 🙌

