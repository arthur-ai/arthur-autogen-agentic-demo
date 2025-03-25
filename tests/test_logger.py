import logging
import os

from src.utils.logger import get_logger, setup_logging


def test_get_logger():
    logger = get_logger("test_module")
    assert isinstance(logger, logging.Logger)
    assert logger.name == "test_module"


def test_setup_logging_default():
    logger = setup_logging(default_level=logging.INFO)
    assert isinstance(logger, logging.Logger)
    assert logger.level <= logging.INFO


def test_setup_logging_custom_path(tmp_path):
    config_path = tmp_path / "test_logging_config.yaml"
    config_content = """
version: 1
formatters:
  simple:
    format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
handlers:
  console:
    class: logging.StreamHandler
    formatter: simple
    stream: ext://sys.stdout
root:
  level: INFO
  handlers: [console]
    """
    config_path.write_text(config_content)

    logger = setup_logging(default_path=str(config_path))
    assert isinstance(logger, logging.Logger)


def test_setup_logging_env_override(monkeypatch):
    monkeypatch.setenv("LOG_CFG", "nonexistent_path.yaml")
    logger = setup_logging()
    assert isinstance(logger, logging.Logger)


def test_log_directory_creation():
    setup_logging()
    assert os.path.exists("logs/tools")
    assert os.path.exists("logs/assistant")
