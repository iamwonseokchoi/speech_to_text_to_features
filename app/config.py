import os
from openai import OpenAI
from pyannote.audio import Pipeline
from dotenv import load_dotenv


def load_config():
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    hf_token = os.getenv('HF_TOKEN')

    if not api_key or not hf_token:
        raise ValueError("OPENAI_API_KEY and HF_TOKEN must be set")

    users = []
    user_env = os.getenv('USERS', '')
    if user_env:
        for user_data in user_env.split(';'):
            parts = user_data.split(',')
            if len(parts) == 2:
                username, password = parts
                users.append((username.strip(), password.strip()))
            else:
                print(f"Warning: Invalid user data format: {user_data}")

    if not users:
        raise ValueError("No valid users found")

    return {
        'api_key': api_key,
        'hf_token': hf_token,
        'openai_client': OpenAI(api_key=api_key),
        'diarization_pipeline': Pipeline.from_pretrained("pyannote/speaker-diarization-3.1", use_auth_token=hf_token),
        'users': users
    }

def load_context():
    context_path = os.getenv('CONTEXT_PATH', 'context.txt')
    with open(context_path, 'r', encoding='utf-8') as file:
        return file.read()