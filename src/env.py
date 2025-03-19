import os

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_WEBHOOK = os.getenv("TELEGRAM_WEBHOOK")
PORT = int(os.getenv("PORT", 8443))
MODEL_PATH = os.getenv("MODEL_PATH", "model/AnimeGANv3_Hayao_36.onnx")
MAX_WORKERS = int(os.getenv("WORKERS", 4))
