import pytest
from unittest.mock import patch, Mock
import gradio as gr
from app.ui import create_interface, greet

@pytest.fixture
def mock_gradio_context():
    with patch('gradio.Blocks') as mock_blocks:
        with patch('gradio.events.get_blocks_context') as mock_context:
            mock_context.return_value = mock_blocks.return_value
            yield mock_blocks

def test_greet():
    result = greet("Test User")
    assert result == "**Hello, Test User!** 👋"

@patch('app.ui.gr.Markdown')
@patch('app.ui.gr.Audio')
@patch('app.ui.gr.Button')
@patch('app.ui.gr.Dataframe')
@patch('app.ui.gr.JSON')
@patch('app.ui.load_config')
def test_create_interface(mock_load_config, mock_JSON, mock_Dataframe, mock_Button, mock_Audio, mock_Markdown, mock_gradio_context):
    mock_config = {
        'users': [('test_user', 'test_password')]
    }
    mock_load_config.return_value = mock_config
    
    result = create_interface('test_user')
    
    assert isinstance(result, Mock)
    mock_gradio_context.assert_called_once()
    mock_Markdown.assert_called()
    mock_Audio.assert_called_once()
    mock_Button.assert_called_once()
    mock_Dataframe.assert_called()
    mock_JSON.assert_called_once()

@patch('app.ui.load_config')
def test_interface_creation_error(mock_load_config, mock_gradio_context):
    mock_load_config.side_effect = Exception("Configuration error")
    
    with pytest.raises(Exception, match="Configuration error"):
        create_interface('test_user')


if __name__ == "__main__":
    pytest.main()