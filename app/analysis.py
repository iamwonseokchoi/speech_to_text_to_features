import json
from app.config import load_context
from app.transcription import transcribe_audio
from app.data_formatting import format_as_is_data, format_to_be_data

def analyze_text(client, transcribed_text):
    context = load_context()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": transcribed_text}
        ],
        temperature=0.0
    )
    
    analysis = response.choices[0].message.content
    
    try:
        analysis_json = json.loads(analysis)
        return json.dumps(analysis_json, indent=2, ensure_ascii=False)
    except json.JSONDecodeError:
        return "Error: The model's response was not in the expected JSON format."

def process_audio(config, audio):
    from app.transcription import transcribe_audio
    from app.data_formatting import format_as_is_data, format_to_be_data
    
    transcription = transcribe_audio(config['openai_client'], audio)
    as_is_data = format_as_is_data(config['openai_client'], config['diarization_pipeline'], audio, transcription)
    to_be_data = format_to_be_data(as_is_data)
    analysis = analyze_text(config['openai_client'], to_be_data['aggregated_stt'].iloc[0])
    return as_is_data, to_be_data, analysis