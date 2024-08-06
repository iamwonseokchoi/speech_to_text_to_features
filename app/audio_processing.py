from pydub import AudioSegment
import tempfile
import os

def convert_to_wav(audio_path):
    audio = AudioSegment.from_file(audio_path)
    wav_path = tempfile.mktemp(suffix=".wav")
    audio.export(wav_path, format="wav")
    return wav_path

def clean_up(file_path):
    os.remove(file_path)