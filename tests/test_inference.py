import pytest

from src.inference.inference import InferenceResult


@pytest.fixture
def sample_inference_json():
    return {
        "inference_id": "test-123",
        "user_id": "user-456",
        "rule_results": [
            {
                "id": "rule1",
                "name": "Content Safety",
                "rule_type": "safety",
                "scope": "global",
                "result": "Pass",
                "latency_ms": 100,
                "details": {"score": 0.95},
            },
            {
                "id": "rule2",
                "name": "Input Validation",
                "rule_type": "validation",
                "scope": "input",
                "result": "Fail",
                "latency_ms": 50,
                "details": {"error": "Invalid format"},
            },
        ],
    }


def test_inference_result_initialization(sample_inference_json):
    result = InferenceResult(sample_inference_json)
    assert result.inference_id == "test-123"
    assert result.user_id == "user-456"
    assert len(result.rule_results) == 2


def test_inference_result_to_dict(sample_inference_json):
    result = InferenceResult(sample_inference_json)
    dict_result = result.to_dict()
    assert dict_result["inference_id"] == "test-123"
    assert len(dict_result["rule_results"]) == 2


def test_get_pass_fail_results(sample_inference_json):
    result = InferenceResult(sample_inference_json)
    pass_fail = result.get_pass_fail_results()
    assert len(pass_fail) == 2
    assert pass_fail[0]["result"] is True  # Pass
    assert pass_fail[1]["result"] is False  # Fail


def test_get_pass_fail_string(sample_inference_json):
    result = InferenceResult(sample_inference_json)
    pass_fail_str = result.get_pass_fail_string()
    assert "Content Safety: PASS" in pass_fail_str
    assert "Input Validation: FAIL" in pass_fail_str
