<div align="center">

<img src="https://cdn.prod.website-files.com/5a749d2c4f343700013366d4/67eab9e594ec4accb58badeb_arthur-logo-symbol.svg" alt="Arthur AI Logo" width="150"/>

<i>Make AI work for Everyone.</i>

![Autogen CI](https://github.com/arthur-ai/arthur-autogen-agentic-demo/actions/workflows/checks.yml/badge.svg?branch=develop)
[![Discord](https://img.shields.io/badge/Discord-Arthur-blue?logo=discord&logoColor=white)](https://discord.gg/tdfUAtaVHz)

[Website](https://arthur.ai) - [Documentation](https://shield.docs.arthur.ai/docs) - [Talk to someone at Arthur](https://www.arthur.ai/arthur-book-a-demo)

</div>

# The Arthur AutoGen Agentic Deployment

The Arthur AutoGen Agentic Deployment provides an example of how Arthur Engine can be used to protect an Agentic Application.

The agentic use-case in this repository is a Financial Analyst Agent that utilizes a handful of tools to query external systems used in
generating responses about a user's financial queries. For a deep dive into how it's structured, see [docs/architecture.md](./docs/architecture.md).

---

![Python](https://img.shields.io/badge/python-3.11+-blue)
![Commit style](https://img.shields.io/badge/commit%20style-conventional--commits-brightgreen)

---

## 📦 Features

- **Safety First**: Integration with Arthur Engine for response validation
- **Multi-Agent System**: Coordinated interaction between specialized AI agents
- Async-ready Python API
- Built-in testing, linting, formatting

---

## 🛠 Getting Started

### 🔑 Required Environment Variables

Before running the app, set the following environment variables (see [docs/security.md](./docs/security.md) for more):

- `ARTHUR_API_KEY` — Arthur Engine API key
- `MODEL_PROVIDER_API_KEY` — Key for your LLM or embedding model provider
- `FINANCE_API_URL` — Base URL for financial data service
- `AUTH_TOKEN` — Optional auth token if needed for protected tools

You can use a `.env` file for local dev and load it via `dotenv` or your preferred method.

### ⚙️ Model Configuration

Model parameters and routing are defined in `config/model_config.json`.

### 🎯 Eval Engine Configuration

Evaluation tasks (if used) are configured in `config/arthur_engine_config.json`:
- Metrics to track (e.g., accuracy, response time)
- Conditions for test prompts
- Logging preferences (optional integration with Arthur's Eval Engine)

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
python main.py
```

---

## 🧪 Run Tests

```bash
pip install -r requirements-dev.txt
pytest
```

---

## 🧰 Developer Setup

Install dev dependencies and initialize hooks:

```bash
./setup-dev.sh
```

This will:
- Install `black`, `ruff`, `pylint`, `pytest`, `semantic-release`
- Set up `pre-commit` to enforce commit message rules

---

## 🧹 Code Quality

Run linters manually:

```bash
black --check .
ruff check .
pylint src/ tests/
```

---

## 📄 Contributing

We welcome contributions!

1. Fork the repository
2. Create a feature branch
3. Follow [Conventional Commits](https://www.conventionalcommits.org/)
4. Install `pre-commit` and run `pre-commit install`
5. Write or update tests
6. Open a pull request against `dev`

See [CONTRIBUTING.md](./CONTRIBUTING.md) for full details.

---

## 🔐 Security

This project enforces best practices including:
- Environment variable-based config
- Secrets excluded via `.gitignore`

For more advanced information, see [docs/security.md](./docs/security.md), which covers:
- Recommended environment variables
- Authentication methods
- Security hardening tips

---

## 🧯 Troubleshooting

For detailed help, see [docs/troubleshooting.md](./docs/troubleshooting.md).

Common tips:

- Ensure `src/` is on your `PYTHONPATH` if using imports
- Make sure pre-commit hooks are installed: `pre-commit install`
- Verify Python 3.11+ is being used

---

## 🪪 License

[MIT](LICENSE)
