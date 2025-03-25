# 🔐 Security Guide

This document outlines security-related configurations and practices used in this project.

## Environment Variables

We recommend storing all secrets and configuration in environment variables or `.env` files (ignored via `.gitignore`).

Ensure all secrets and API keys are set via environment variables:
- `ALPHA_VANTAGE_API_KEY` - API key for Alpha Vantage service
- `MODEL_CONFIG_PATH` - Path to model configuration file
- `ENGINE_URL` - URL for the Arthur engine service
- `ENGINE_API_KEY` - API key for Arthur engine authentication
- `PROJECT_PATH` - Path to the project


Use a `.envTemplate` file to indicate required settings:

```env
# .env.example
ALPHA_VANTAGE_API_KEY=your-api-key
ENGINE_URL=https://your-arthur-instance.com
ENGINE_API_KEY=your-auth-token
MODEL_CONFIG_PATH=./config/model_config.json
```

Load them in development with tools like [`python-dotenv`](https://github.com/theskumar/python-dotenv).

## 🔐 Authentication & Secrets Management

- All API access requires authentication tokens
- Store secrets using your cloud platform's secret manager or CI/CD secret storage (e.g., GitHub Secrets, AWS Secrets Manager)
- Do **not** commit secrets to the repository

---

## 🔁 Token Rotation

- Rotate all API keys at least every 30–90 days
- Use CI/CD secrets to manage token injection at runtime
- Avoid exposing tokens in logs or `echo` statements

---

## 🛡 Hardening Tips

- Never hardcode credentials in Python files or YAML configs
- Use `.env`, `os.environ`, or CI secrets
- Use the principle of least privilege for API keys
- Disable debug logs in production

---

## Configuration Files
The project uses several configuration files located in the `/config` directory:
- `model_config.json` - Model-specific configurations
- `eval_engine_config.json` - Evaluation engine settings
- `logging_config.yaml` - Logging configurations

### Model Configuration (`model_config.json`)
This file contains model-specific settings and should include:
- Model parameters and configurations
- API endpoints and timeouts
- Version control using `model_config.jsonTEMPLATE`
- Never commit actual model keys or sensitive parameters
- Keep sensitive values in environment variables

#### Example
```json
[
    {
        "provider": "azure",
        "config": {
            "model": "gpt-4",
            "azure_endpoint": "https://<your-resource-name>.openai.azure.com",
            "azure_deployment": "gpt-4-deployment",
            "api_version": "2023-07-01-preview",
            "api_key": ""
            },
    },
    {
        "provider": "openai",
        "config": {
            "model": "gpt-4-1106-preview",
            "api_key": "",
            "temperature": 0.7,
            "max_tokens": 4096
        }
    }
]
```

### Evaluation Engine Configuration (`eval_engine_config.json`)
This file manages evaluation engine settings:
- Engine-specific parameters
- Performance thresholds
- Monitoring configurations
- Use `eval_engine_config.jsonTEMPLATE` for version control
- Keep actual configuration private
- Store sensitive credentials in environment variables

#### Example
```json
{
  "tools": {
    "fetch_stock_data": {
      "name": "StockInfoTool",
      "eval_engine_model": "INSERT_EVAL_ENGINE_MODEL_ID_HERE"
    }
  },
  "agents": {
    "OrchestratorAgent": {
      "name": "orchestrator",
      "eval_engine_model": "INSERT_EVAL_ENGINE_MODEL_ID_HERE"
    }
  }
}
```

### Logging Configuration (`logging_config.yaml`)
This YAML file controls logging behavior:
- Log levels and rotation policies
- Output formats and destinations
- Sensitive data masking rules
- Never log credentials or API keys
- Configure appropriate log retention periods
- Use secure log storage locations
- Implement log rotation to manage file sizes

Security Considerations for Config Files:
- Always use template files (*.jsonTEMPLATE) in version control
- Keep actual config files in .gitignore
- Regularly audit configurations for exposed secrets
- Use environment variable substitution for sensitive values
- Implement file permission restrictions on config files
- Regular backup and versioning of configurations
- Document all configuration changes

---

## 🔍 Secrets Scanning

Use open-source tools to proactively scan for accidentally committed secrets:

```bash
gitleaks detect --source .
# or
trufflehog filesystem .
```

Enable GitHub’s built-in secret scanning on your repository.

---

## ⚙️ CI/CD Security Practices

- Store secrets as encrypted variables (e.g., `${{ secrets.ENGINE_API_KEY }}` in GitHub Actions)
- Avoid outputting secrets via `echo` or logging steps
- Scope secrets to the least number of jobs needed

---

## ✅ Security Checklist

- [x] `.env` is excluded from Git
- [x] `.envTemplate` is provided
- [x] All tokens are injected via env vars
- [x] Secrets never appear in logs
- [x] Token rotation plan is defined
- [] Secrets scanning is part of CI or dev workflow

---