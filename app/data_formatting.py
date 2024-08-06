import pandas as pd
from datetime import datetime, timedelta
import pytz
from app.audio_processing import convert_to_wav, clean_up
from pydub import AudioSegment
import tempfile

def format_as_is_data(client, diarization_pipeline, audio, transcription):
    wav_audio = convert_to_wav(audio)
    diarization = diarization_pipeline(wav_audio)
    audio_segment = AudioSegment.from_wav(wav_audio)
    
    kst = pytz.timezone('Asia/Seoul')
    start_time = datetime.now(kst)
    
    formatted_data = []
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        if turn.end - turn.start < 0.1:
            continue
        
        segment_start = start_time + timedelta(seconds=turn.start)
        segment_end = start_time + timedelta(seconds=turn.end)
        
        start_ms = int(turn.start * 1000)
        end_ms = int(turn.end * 1000)
        segment_audio = audio_segment[start_ms:end_ms]
        
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            segment_audio.export(temp_file.name, format="wav")
            temp_file_path = temp_file.name

        try:
            with open(temp_file_path, 'rb') as segment_file:
                segment_transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    language="ko",
                    file=segment_file
                ).text
        except Exception as e:
            print(f"Error transcribing segment: {e}")
            segment_transcript = ""

        clean_up(temp_file_path)
        
        formatted_data.append({
            "timestamp": segment_start.strftime("%Y-%m-%d %H:%M:%S"),
            "speaker": speaker,
            "asis_stt_fragment": segment_transcript
        })
    
    clean_up(wav_audio)
    return pd.DataFrame(formatted_data)

def format_to_be_data(as_is_data):
    aggregated_stt = ' | '.join(as_is_data['asis_stt_fragment'])
    
    to_be_data = pd.DataFrame({
        "contract_id": ['1xxxxxx'],
        "call_id": ['2024xxxxxx'],
        "start_time": [as_is_data['timestamp'].iloc[0]],
        "end_time": [as_is_data['timestamp'].iloc[-1]],
        "aggregated_stt": [aggregated_stt]
    })
    
    return to_be_data