import pytest
from unittest.mock import Mock, patch
import json
from app.analysis import analyze_text, process_audio

@pytest.fixture
def mock_openai_client():
    client = Mock()
    client.chat.completions.create.return_value = Mock(
        choices=[Mock(message=Mock(content='{"key": "value"}'))]
    )
    return client

@patch('app.analysis.load_context')
def test_analyze_text(mock_load_context, mock_openai_client):
    mock_load_context.return_value = "Test context"
    
    result = analyze_text(mock_openai_client, "Test transcription")
    
    assert json.loads(result) == {"key": "value"}
    mock_openai_client.chat.completions.create.assert_called_once()

@patch('app.analysis.load_context')
def test_analyze_text_invalid_json(mock_load_context, mock_openai_client):
    mock_load_context.return_value = "Test context"
    mock_openai_client.chat.completions.create.return_value = Mock(
        choices=[Mock(message=Mock(content='Invalid JSON'))]
    )
    
    result = analyze_text(mock_openai_client, "Test transcription")
    
    assert result == "Error: The model's response was not in the expected JSON format."
