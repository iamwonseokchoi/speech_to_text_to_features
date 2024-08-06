from app.config import load_config
from app.ui import create_interface


if __name__ == "__main__":
    config = load_config()
    users = config['users']
    demo = create_interface(users[0][0])
    demo.launch(
        auth=users,
        auth_message="STT & LLM Featurization Demo:",
        allowed_paths=["context.txt", ".ini", "assets"],
        server_name="0.0.0.0",
        server_port=7860,
        share=True,
    )