from app.audio_processing import convert_to_wav, clean_up

def transcribe_audio(client, audio):
    if audio is None:
        return "No audio detected. Please try again."
    
    wav_audio = convert_to_wav(audio)
    
    try:
        with open(wav_audio, 'rb') as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1", 
                language="ko",
                file=audio_file
            )
    finally:
        clean_up(wav_audio)
    
    return transcript.text