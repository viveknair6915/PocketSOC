import os
from dotenv import load_dotenv

load_dotenv()

class AgentConfig:
    BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
    AGENT_ID = os.getenv("AGENT_ID", "agent_007")
    AGENT_SECRET_KEY = os.getenv("AGENT_SECRET_KEY", "agentsecretkey12345678901234567890") # 32 chars for AES-256
    CONFIDENCE_THRESHOLD = 0.5
    MODEL_PATH = "model/scam_detection.tflite"
    TOKENIZER_PATH = "model/tokenizer.pickle"

config = AgentConfig()
