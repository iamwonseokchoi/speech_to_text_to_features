import pytest
from unittest.mock import Mock, patch
from app.transcription import transcribe_audio

@pytest.fixture
def mock_openai_client():
    client = Mock()
    client.audio.transcriptions.create.return_value = Mock(text="Test transcription")
    return client

@pytest.fixture
def sample_audio(tmp_path):
    audio_path = tmp_path / "test_audio.wav"
    audio_path.write_bytes(b"fake audio content")
    return str(audio_path)

@patch('app.transcription.convert_to_wav')
@patch('app.transcription.clean_up')
def test_transcribe_audio(mock_clean_up, mock_convert_to_wav, mock_openai_client, sample_audio):
    mock_convert_to_wav.return_value = sample_audio

    result = transcribe_audio(mock_openai_client, sample_audio)

    assert result == "Test transcription"
    mock_convert_to_wav.assert_called_once_with(sample_audio)
    mock_openai_client.audio.transcriptions.create.assert_called_once()
    mock_clean_up.assert_called_once_with(sample_audio)

def test_transcribe_audio_no_audio():
    result = transcribe_audio(Mock(), None)
    assert result == "No audio detected. Please try again."

@patch('app.transcription.convert_to_wav')
def test_transcribe_audio_conversion_error(mock_convert_to_wav):
    mock_convert_to_wav.side_effect = Exception("Conversion error")
    
    with pytest.raises(Exception, match="Conversion error"):
        transcribe_audio(Mock(), "fake_audio.mp3")

@patch('app.transcription.convert_to_wav')
@patch('app.transcription.clean_up')
def test_transcribe_audio_api_error(mock_clean_up, mock_convert_to_wav, mock_openai_client, sample_audio):
    mock_convert_to_wav.return_value = sample_audio
    mock_openai_client.audio.transcriptions.create.side_effect = Exception("API error")

    with pytest.raises(Exception, match="API error"):
        transcribe_audio(mock_openai_client, sample_audio)

    mock_clean_up.assert_called_once_with(sample_audio)