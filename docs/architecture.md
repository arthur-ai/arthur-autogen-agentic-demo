# 🏗 Architecture

This document describes the internal structure of the Financial Analyst Agent protected by Arthur Engine.

## Overview

- `src/` contains the main logic and components.
- Agents utilize tools to access external systems for answering financial queries.
- Arthur Engine acts as a policy layer or enforcement gateway.

## Modules

- **agent/**: Core decision loop and tool orchestration
- **tools/**: External integrations
- **policy/**: Arthur-protected enforcement layer

## Implementation Architecture

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

3.  **Validator Agent**
   - Validates interactions between tools and Orchestrator
   - Ensures outputs conform to business logic and security constraints
   - Acts as a guardrail between the Orchestrator and external systems

### Example Architecture
![Agent System Diagram](https://cdn.prod.website-files.com/6230fe4706acf3c7e68b2d7c/67e1816b265b9ca1c4e6ae75_AD_4nXcDhap_AxMKWM3AguIycNEAQ5wjM5evAlP76B7lMj-MqN5qIFedLbkxTmlugpR9q8rTQa6VJrh2NvAh1-DAsiivLtI0B0ppRAL9wj3p-dsdxg-WQzKSehu8G-TY25cXyaememHz3w.png)

