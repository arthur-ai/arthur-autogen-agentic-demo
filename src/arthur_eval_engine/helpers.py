"""Helper functions for interacting with Arthur's Evaluation Engine.

This module provides utility functions for validating AI-generated content
through Arthur's Evaluation Engine. It handles prompt validation, response
checking, and configuration management for the evaluation system.

Key Features:
    - Prompt safety and quality validation
    - Response content verification
    - Configuration management for eval engine models
    - API communication handling with Arthur's services

Functions:
    send_prompt_to_eval_engine: Validates prompts before processing
    send_response_to_eval_engine: Validates AI-generated responses
    get_eval_engine_model: Retrieves model configurations
    load_eval_engine_config: Loads evaluation engine settings
"""

import json
import os
from pathlib import Path

import httpx
from autogen_core.models import LLMMessage
from dotenv import load_dotenv

from src.utils.logger import get_logger

logger = get_logger(__name__)
load_dotenv()  # Load environment variables from .env file

EVAL_ENGINE_URL = os.getenv("EVAL_ENGINE_URL")
EVAL_ENGINE_API_KEY = os.getenv("EVAL_ENGINE_API_KEY")


def get_headers():
    """
    Returns the standard headers needed for API requests.
    Includes authorization and content type headers.

    Returns:
        dict: Headers dictionary with auth token and content type
    """
    logger.debug("[get_headers] Generating API request headers")
    return {
        "Authorization": f"Bearer {EVAL_ENGINE_API_KEY}",
        "Content-Type": "application/json",
    }


async def send_prompt_to_eval_engine(message: str, task: str, conversation_id: str):
    """
    Sends a prompt to the eval engine service for validation and safety checking.

    The eval engine service performs:
    - Content safety validation
    - Prompt injection detection
    - Quality and relevance checks
    - Response formatting validation

    Args:
        message (str): The prompt text to validate
        task (str): Task identifier for the eval engine service

    Returns:
        dict: Validation response containing:
            - inference_id: Unique identifier for this validation
            - validation_results: Safety and quality check results
            - status: Success/failure indication

    Raises:
        HTTPError: If the eval engine service request fails
        ConnectionError: If unable to connect to the service
    """
    logger.info("[send_prompt_to_eval_engine] Sending prompt for validation")
    url = f"{EVAL_ENGINE_URL}/api/v2/tasks/{task}/validate_prompt"
    logger.debug(f"[send_prompt_to_eval_engine] Request URL: {url}")
    logger.debug(f"[send_prompt_to_eval_engine] Message content: {message[:100]}...")

    body = {"prompt": message, "conversation_id": conversation_id, "user_id": "1"}
    async with httpx.AsyncClient() as client:
        logger.debug("[send_prompt_to_eval_engine] Sending POST request")
        response = await client.post(url, json=body, headers=get_headers())
        if response.status_code == 200:
            result = response.json()
            logger.info("[send_prompt_to_eval_engine] Validation successful")
            logger.debug(f"[send_prompt_to_eval_engine] Response: {result}")
        else:
            logger.error(
                f"[send_prompt_to_eval_engine] Validation failed with status code {response.status_code}"
            )
            logger.error(
                f"[send_prompt_to_eval_engine] Error response: {response.text}"
            )
            result = None
    return result


async def send_response_to_eval_engine(
    response: str, task: str, inference_id: str, context: list[LLMMessage]
):
    """
    Validates an AI-generated response through Arthur's Evaluation Engine's safety and quality checks.

    The validation process includes:
    - Content safety and appropriateness verification
    - Response quality assessment
    - Context relevance checking
    - Format and structure validation

    Args:
        response (str): The AI response requiring validation
        task (str): Task identifier for context-specific validation rules
        inference_id (str): Unique ID linking to the original prompt validation
        context (list[LLMMessage]): Conversation history for contextual validation

    Returns:
        dict: Validation results containing:
            - safety_checks: Content safety assessment
            - quality_metrics: Response quality scores
            - validation_status: Overall pass/fail status

    Raises:
        HTTPError: If Arthur's Evaluation Engine validation fails
        ConnectionError: If Arthur's Evaluation Engine is unreachable
    """
    logger.info("[send_response_to_eval_engine] Sending response for validation")
    url = f"{EVAL_ENGINE_URL}/api/v2/tasks/{task}/validate_response/{inference_id}"
    logger.debug(f"[send_response_to_eval_engine] Request URL: {url}")

    context_str = ",".join(obj.content for obj in context)
    body = {
        "response": response,
        "context": context_str,
    }
    async with httpx.AsyncClient() as client:
        logger.debug("[send_response_to_eval_engine] Sending POST request")
        response = await client.post(url, json=body, headers=get_headers())
        if response.status_code == 200:
            result = response.json()
            logger.info("[send_response_to_eval_engine] Validation successful")
            logger.debug(f"[send_response_to_eval_engine] Response: {result}")
        else:
            logger.error(
                f"[send_response_to_eval_engine] Validation failed with status code {response.status_code}"
            )
            logger.error(
                f"[send_response_to_eval_engine] Error response: {response.text}"
            )
            result = None
    return result


def get_eval_engine_model(entity_type: str, entity_name: str, config: dict) -> str:
    """
    Gets Arthur's Evaluation Engine Model ID for a given tool or agent.

    Args:
        entity_type (str): Type of entity ("tools" or "agents.orchestrator_agents")
        entity_name (str): Name of the tool or agent
        config (dict, optional): Pre-loaded configuration. If None, loads from file

    Returns:
        str: Eval engine task ID for the entity

    Raises:
        KeyError: If the entity isn't found in the configuration
    """

    logger.debug(
        f"[get_eval_engine_model] Getting eval engine task for {entity_type}.{entity_name}"
    )

    try:
        if "." in entity_type:
            # Handle nested paths like "agents.orchestrator_agents"
            parts = entity_type.split(".")
            current = config
            for part in parts:
                current = current[part]
            eval_engine_model = current[entity_name]["eval_engine_model"]
        else:
            eval_engine_model = config[entity_type][entity_name]["eval_engine_model"]

        if eval_engine_model == "":
            logger.error(
                f"[get_eval_engine_model] Eval engine model not found for {entity_type}.{entity_name}"
            )
            logger.error(
                "[get_eval_engine_model] Returning default eval engine model ['default']['eval_engine_model']"
            )
            return config["tools"]["default"]["eval_engine_model"]

        logger.debug(
            f"[get_eval_engine_model] Found eval engine model: {eval_engine_model}"
        )
        return eval_engine_model
    except KeyError:
        logger.error(
            f"[get_eval_engine_model] Entity {entity_name} not found in {entity_type}"
        )
        raise KeyError(f"No eval engine model found for {entity_type}.{entity_name}")


def load_eval_engine_config(config_path: str = "eval_engine_config.json") -> dict:
    """
    Loads Arthur's Evaluation Engine configuration from a JSON file that maps tools and agents to their models.

    Args:
        config_path (str): Path to the Arthur's Evaluation Engine configuration JSON file

    Returns:
        dict: Dictionary containing tool and agent configurations with their models

    Raises:
        FileNotFoundError: If the config file doesn't exist
        JSONDecodeError: If the config file isn't valid JSON
    """
    logger.info(
        f"[load_eval_engine_config] Loading eval engine configuration from {config_path}"
    )
    try:
        with open(Path(config_path)) as f:
            config = json.load(f)
            logger.debug(f"[load_eval_engine_config] Loaded configuration: {config}")
            return config
    except FileNotFoundError:
        logger.error(
            f"[load_eval_engine_config] Eval engine configuration file not found at {config_path}"
        )
        raise
    except json.JSONDecodeError:
        logger.error(
            "[load_eval_engine_config] Invalid JSON in eval engine configuration file"
        )
        raise
