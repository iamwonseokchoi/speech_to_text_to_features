import pytest
import os
from pydub import AudioSegment
from app.audio_processing import convert_to_wav, clean_up

@pytest.fixture
def sample_audio(tmp_path):
    audio = AudioSegment.silent(duration=1000)  
    mp3_path = tmp_path / "test_audio.mp3"
    audio.export(mp3_path, format="mp3")
    return str(mp3_path)

def test_convert_to_wav(sample_audio):
    wav_path = convert_to_wav(sample_audio)
    assert os.path.exists(wav_path)
    assert wav_path.endswith('.wav')
    
    wav_audio = AudioSegment.from_wav(wav_path)
    assert len(wav_audio) == 1000  

    clean_up(wav_path)

def test_clean_up(tmp_path):
    test_file = tmp_path / "test_file.txt"
    test_file.write_text("Test content")
    
    assert os.path.exists(str(test_file))
    clean_up(str(test_file))
    assert not os.path.exists(str(test_file))

def test_convert_to_wav_file_not_found():
    with pytest.raises(FileNotFoundError):
        convert_to_wav("non_existent_file.mp3")

def test_clean_up_file_not_found():
    with pytest.raises(FileNotFoundError):
        clean_up("non_existent_file.txt")