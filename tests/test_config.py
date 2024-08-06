import pytest
import os
from app.config import load_config, load_context

@pytest.fixture
def mock_env_variables(monkeypatch):
    monkeypatch.setenv('OPENAI_API_KEY', 'test_openai_key')
    monkeypatch.setenv('HF_TOKEN', 'test_hf_token')
    monkeypatch.setenv('USERS', 'user1,password1;user2,password2')

def test_load_config(mock_env_variables):
    config = load_config()
    assert config['api_key'] == 'test_openai_key'
    assert config['hf_token'] == 'test_hf_token'
    assert isinstance(config['openai_client'], object)  # Just check if it's an object. No ping
    assert callable(config['diarization_pipeline'])
    assert config['users'] == [('user1', 'password1'), ('user2', 'password2')]

def test_load_config_invalid_users(monkeypatch):
    monkeypatch.setenv('OPENAI_API_KEY', 'test_key')
    monkeypatch.setenv('HF_TOKEN', 'test_token')
    monkeypatch.setenv('USERS', 'invalid_user_data')
    with pytest.raises(ValueError, match="No valid users found"):
        load_config()

def test_load_context(tmp_path, monkeypatch):
    context_content = "Test context content"
    context_file = tmp_path / "test_context.txt"
    context_file.write_text(context_content)
    
    monkeypatch.setenv('CONTEXT_PATH', str(context_file))
    
    loaded_context = load_context()
    assert loaded_context == context_content

def test_load_context_file_not_found(monkeypatch):
    monkeypatch.setenv('CONTEXT_PATH', '/non/existent/path.txt')
    with pytest.raises(FileNotFoundError):
        load_context()