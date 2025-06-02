import subprocess
import time

def start_ollama_server():
    """Запускает Ollama сервер в фоновом режиме."""
    process = subprocess.Popen(
        ["ollama", "serve"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    return process