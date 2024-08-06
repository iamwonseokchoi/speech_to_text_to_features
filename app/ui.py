import gradio as gr
from app.config import load_config
from app.analysis import process_audio

custom_css = """
#user-greeting {
    font-size: 24px;
    font-weight: bold;
    color: #4a4a4a;
    margin-bottom: 20px;
}
.centered-image {
    display: block;
    margin-left: auto;
    margin-right: auto;
    max-width: 100%;
    height: auto;
}
#custom-button {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    padding: 10px !important;
    background-color: #4a4a4a !important;
    border: none !important;
    border-radius: 5px !important;
    cursor: pointer !important;
    transition: background-color 0.3s !important;
    width: 200px !important;
    height: auto !important;
}
#custom-button:hover {
    background-color: #3a3a3a !important;
}
#custom-button::before {
    content: '';
    display: block;
    width: 400px;
    height: 100px;
    margin-bottom: 10px;
    background-image: url('file/assets/atf_logo_blue.svg');
    background-size: contain;
    background-repeat: no-repeat;
    background-position: center;
}
#custom-button span {
    font-size: 16px !important;
    font-weight: bold !important;
    color: white !important;
}
"""

def greet(name):
    return f"**Hello, {name}!** 👋"

def create_interface(username):
    config = load_config()
    
    with gr.Blocks(css=custom_css) as demo:
        greeting = gr.Markdown(value=greet(username), elem_id="user-greeting")
        gr.Markdown("# [Artefact] Advanced Churn Management")
        gr.Markdown("## - GenAI for Call Data Featurization: Demo - ")
        gr.Markdown("---")
        gr.Markdown("### STT Featurization Flow Concept")
        gr.Markdown('<img src="file/assets/flow.png" alt="Flow Diagram" class="centered-image">')
        gr.Markdown("""
                    ```
                    This MVP demonstrates the full-funnel flow of STT data to generate features for the DT score model:
                    
                    1. As-Is (STT): Call logs are segmented into speaker turns with timestamps and transcriptions and is unusable by GenAI or for NLP.
                    2. To-Be (Data Engineered): Call logs are aggregated via engineering and condensed into a format usable by GenAI.
                    3. To-Be (LLM Featurization): The aggregated text is analyzed and useful features are extracted to improve the DT score model.
                    ```
        """)
        
        with gr.Row():
            audio_input = gr.Audio(type='filepath', label="Record or upload audio")
            custom_button = gr.Button('Run Full STT Featurization Demo', elem_id="custom-button")
        
        with gr.Column():
            gr.Markdown("## As-Is: Broken STT")
            gr.Markdown("---")
            as_is_output = gr.Dataframe(label="As-Is: Broken STT")
            gr.Markdown("## To-Be: Aggregated STT & Advanced Featurization")
            gr.Markdown("---")
            to_be_output = gr.Dataframe(label="To-Be: Aggregated STT")
            analysis_output = gr.JSON(label="To-Be: Advanced Featurization")
        
        custom_button.click(fn=lambda audio: process_audio(config, audio), inputs=audio_input, outputs=[as_is_output, to_be_output, analysis_output])

    return demo