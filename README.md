---
title: stt-llm-featurization-mvp
app_file: main.py
sdk: gradio
sdk_version: 4.38.1
---
# [KOR] Speech to Text x LLM Feature Extraction Demo
July, 2024
---

MVP demo showcasing use case of GenAI to process speech to text and ultimately generate features via information extraction. Done using simple 2-shot prompting. 

Live Demo: https://huggingface.co/spaces/wonseokchoi1/stt-llm-featurization-mvp 

## Code Architecture
```
root/
│
├── main.py
├── requirements.txt
├── .ini
├── context.txt
├── Dockerfile
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── audio_processing.py
│   ├── transcription.py
│   ├── data_formatting.py
│   ├── analysis.py
│   ├── ui.py
│   └── ini_to_env.py
│
├── assets/
│   ├── atf_logo_blue.svg
│   └── flow.png
│
└── tests/
    ├── __init__.py
    ├── test_config.py
    ├── test_audio_processing.py
    ├── test_transcription.py
    ├── test_data_formatting.py
    └── test_analysis.py
```

## Secrets
- OpenAI key
- HF Token
    - Access to gated pyannote models (3.1, 3.0)
- Username/Password
```
# .ini -> app/ini_to_env.py for conversion to .env

[api]
OPENAI_API_KEY=
HF_TOKEN=

[users]
user1 = id, pw
user2 = id, pw
```

## For local
> export $(cat .env | xargs)

## Docker
```
docker build -t stt-llm-mvp .

docker run --env-file .env -p 7860:7860 --memory=4g --shm-size=1g stt-llm-mvp:latest
```