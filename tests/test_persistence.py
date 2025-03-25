
from src.core.persistence import MockPersistence


def test_mock_persistence_init():
    persistence = MockPersistence()
    assert persistence.load_content() == {}


def test_mock_persistence_save_and_load():
    persistence = MockPersistence()
    test_content = {"key": "value", "number": 42}

    persistence.save_content(test_content)
    loaded_content = persistence.load_content()

    assert loaded_content == test_content
    assert loaded_content["key"] == "value"
    assert loaded_content["number"] == 42


def test_mock_persistence_overwrite():
    persistence = MockPersistence()

    # Save initial content
    initial_content = {"key": "value"}
    persistence.save_content(initial_content)

    # Overwrite with new content
    new_content = {"new_key": "new_value"}
    persistence.save_content(new_content)

    loaded_content = persistence.load_content()
    assert loaded_content == new_content
    assert "key" not in loaded_content
