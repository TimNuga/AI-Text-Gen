import pytest
from unittest.mock import MagicMock
from app.services.ai_service import AIService

def test_generate_text_success():
    provider_mock = MagicMock()
    provider_mock.generate_text.return_value = "Mocked response"
    ai_service = AIService(provider_mock)
    
    result = ai_service.generate_text("Hello")
    provider_mock.generate_text.assert_called_once_with("Hello")
    assert result == "Mocked response"

def test_generate_text_empty_prompt():
    provider_mock = MagicMock()
    ai_service = AIService(provider_mock)
    
    with pytest.raises(ValueError) as exc:
        ai_service.generate_text("")
    assert "Prompt cannot be empty" in str(exc.value)
