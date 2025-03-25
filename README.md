<div>
   <div align="center">
   <img src="https://cdn.prod.website-files.com/6230fe4706acf355d38b2d54/65b98b3564bb58c88c0a1b66_arthur-logo-light-nav.svg" alt="Arthur AI Logo" width="300" style="background-color: white;"/>
   </div>
</div>

# Arthur AutoGen Agent Demo

## Overview
This project provides an example of how Arthur Engine can be used to protect an Agentic Application. 

The agentic use-case in this repository is a Financial Analyst Agent that utilizes a handful of tools to query external systems used in 
generating responses about a user's financial queries.

## Key Features
- **Intelligent Stock Analysis**: Real-time market data processing and analysis
- **Safety First**: Integration with Arthur Engine for response validation
- **Multi-Agent System**: Coordinated interaction between specialized AI agents

## Prerequisites
- Python 3.11 or higher
- Required Python packages (detailed in requirements.txt)
- Azure OpenAI API access and credentials
- Alpha Vantage API key for financial data access
- Arthur Engine API credentials and access

## Installation

### 1. Repository Setup
```bash
git clone https://github.com/arthur-ai/arthur-autogen-agentic-demo.git
cd arthur-autogen-agentic-demo
```

### 2. Python Environment
#### Option 1: Using venv
```bash
# Create virtual environment
python -m venv venv

# Activate on Unix/macOS
source venv/bin/activate

# Activate on Windows
venv\Scripts\activate

# Deactivate when done
deactivate
```

#### Option 2: Using conda
```bash
# Create conda environment
conda create -n arthur-demo python=3.11

# Activate conda environment
conda activate arthur-demo

# Deactivate when done
conda deactivate
```


### 3. Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the project root:
```env
AZURE_OPENAI_API_KEY=your_azure_openai_key
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key
EVAL_ENGINE_API_KEY=your_eval_engine_api_key
```


## Configuration Files

### 1. Model Configuration
Create `model_config.json` in the project root:
```json
{
    "provider": "azure",
    "config": {
        "model": "gpt-4",
        "azure_endpoint": "https://<your-resource-name>.openai.azure.com",
        "azure_deployment": "gpt-4-deployment",
        "api_version": "2023-07-01-preview",
        "api_key": ""
    }
}
{
   "provider": "openai",
   "config": {
         "model": "gpt-4-1106-preview",
         "api_key": "",
         "temperature": 0.7,
         "max_tokens": 4096
   }
}
```

### 2. Eval Engine Configuration
Create `eval_engine_config.json` in the project root:
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

## System Architecture

### Agent System
The application uses a multi-agent architecture:

1. **Orchestrator Agent**
   - Manages conversation flow and task delegation
   - Coordinates between user inputs and assistant responses
   - Ensures proper sequencing of operations

2. **Assistant Agent**
   - Processes specific user requests
   - Generates detailed market analysis
   - Provides stock predictions and insights

### Safety Integration
The system leverages Arthur Engine's capabilities for:
- Content validation and quality assurance
- Response appropriateness checking
- Safety boundary enforcement

## Usage

### Starting the System
```bash
python main.py
```

## System Requirements
- Memory: Minimum 4GB RAM recommended
- Network: Stable internet connection required
- Supported OS: Windows 10+, macOS 10.15+, Ubuntu 20.04+

## Configuration Details
### Azure OpenAI
- Supported Models: GPT-4, GPT-3.5-turbo
- Required Permissions: Completion API access
- Rate Limits: Depends on your Azure OpenAI tier

### OpenAI (Non-Azure)
- Supported Models: 
  - GPT-4 (4-turbo-preview, 4-1106-preview)
  - GPT-3.5-turbo (3.5-turbo-1106)
- Required Permissions: OpenAI API access
- Rate Limits: 
  - Free tier: 3 requests/minute
  - Pay-as-you-go: Based on usage tier

### Alpha Vantage API
- Rate Limits: 5 API calls per minute (free tier)
- Data Freshness: 15-minute delayed market data

## Troubleshooting
Common issues and solutions:
1. API Connection Errors
   - Verify API keys are correctly set in .env
   - Check network connectivity
   - Ensure API service status is operational

2. Rate Limiting
   - Implement exponential backoff
   - Monitor API usage
   - Consider upgrading API tiers for production use

## Security Best Practices
- Store API keys in environment variables
- Use secrets management in production
- Implement request logging
- Regular security audits
- Rate limit user requests

## Example Usage
When you run the system, you'll see an interface like this:
```

--------------------------QUESTION_FOR_USER--------------------------
Hi! How can I help you?
---------------------------------------------------------------------
Enter your input: Give me info about AAPL
```

The agent will then process your request and provide detailed financial analysis about Apple Inc.

## Testing
```bash
pytest tests/
```

## Contributing
We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Support and Resources
- GitHub Issues: For bug reports and feature requests
- Wiki: Additional guides and best practices
- Email Support: support@arthur.ai

## Acknowledgments
- AutoGen team for the multi-agent framework
- Arthur AI team for the Evaluation Engine
- Azure OpenAI for API access
- Alpha Vantage for market data services